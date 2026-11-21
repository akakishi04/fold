"""C312 software tests; synthetic training does not establish actual FOLD capability."""
import ast
import contextlib
import copy
import hashlib
import io
import itertools
import json
from pathlib import Path
import re
import sys
import tempfile
import types
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c312_value_balanced_batches as b


def dataset():
    out={"TRAIN":[],"HOLDOUT":[]}
    for entities,values,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (values[1]-values[0])%4==2 else "TRAIN"
        for perm,query in itertools.product((entities,entities[::-1]),entities):
            out[split].append(dict(id=f"{lang}:{entities}:{values}:{perm}:{query}",entities=list(entities),values=list(values),language=lang,
                permutation=list(perm),query=query,target=48+values[entities.index(query)]))
    return out


def pairs_from_rows(rows):
    groups={}
    for i,r in enumerate(rows):
        k=(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups.setdefault(k,[]).append(i)
    return torch.tensor([sorted(groups[k],key=lambda i:rows[i]["query"]) for k in sorted(groups)],dtype=torch.int64)


def stats(e):
    return dict(per_length_row_exposures=[torch.bincount(e[e[:,:,0]==k][:,2:].flatten(),minlength=192).tolist() for k in range(3)],
        length_profile_updates=[[int(((e[:,0,0]==k)&(e[:,0,1]==p)).sum()) for p in range(3)] for k in range(3)],
        event_sha256=b.digest(e.tolist()),logical_pair_sha256=b.digest(e[:,:,2:].tolist()),profile_sha256=b.digest(e[:,:,1].tolist()))


def tables(data):
    y=torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)
    x=torch.zeros((3,3,192,64),dtype=torch.int64); x[:,:,:,0]=y-48
    return x,y


def fingerprint(model):
    h=hashlib.sha256()
    for n,p in sorted(model.state_dict().items()): h.update(n.encode()); h.update(p.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


class Core(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.linear=torch.nn.Linear(8,8,dtype=torch.float64)
        self.padding=torch.nn.Parameter(torch.zeros(3256,dtype=torch.float64)); self.config=NS(slots=64)
    def forward(self,x): return torch.tanh(self.linear(x))


class Toy(torch.nn.Module):
    def __init__(self,reference=None):
        super().__init__()
        if reference is not None:
            clone=copy.deepcopy(reference); self.backbone=clone.backbone; self.read=clone.read; return
        self.backbone=torch.nn.Module(); self.backbone.embed=torch.nn.Embedding(4,8,dtype=torch.float64); self.backbone.core=Core()
        self.backbone.config=NS(max_tokens=64); self.read=torch.nn.Linear(8,256,dtype=torch.float64)
        self.backbone.padding=torch.nn.Parameter(torch.zeros(14256-sum(p.numel() for p in self.parameters()),dtype=torch.float64))
    def forward(self,x,t):
        assert t.shape==(len(x),) and not bool(t.any())
        h=self.backbone.embed(x[:,0])
        for _ in range(4): h=self.backbone.core(h)
        return self.read(h)


def policy_fixture():
    def groups(m,a):
        assert a=="core_slow"
        return [dict(params=[p for n,p in m.named_parameters() if not n.startswith("backbone.core.")],lr=.005),
                dict(params=list(m.backbone.core.parameters()),lr=.0005)]
    def optimizer(m,a): return torch.optim.AdamW(groups(m,a),betas=(.9,.999),eps=1e-8,weight_decay=0.)
    def verify(o,m,a):
        for got,want in zip(o.param_groups,groups(m,a),strict=True):
            b.require(got["lr"]==want["lr"] and [id(p) for p in got["params"]]==[id(p) for p in want["params"]],"fixture optimizer")
    return NS(configure=lambda m,a:m.requires_grad_(True),parameter_groups=groups,optimizer_for=optimizer,verify_optimizer=verify,CORE_LR=.0005,BASE_LR=.005)


def factory_fixture():
    def new(seed):
        with torch.random.fork_rng(): torch.manual_seed(seed); return Toy()
    return NS(factory=NS(new_model=new,language_module=lambda:None),c278=NS(MeanFinalDualReadout=lambda model,*_:model),
        reader=None,c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint))


def scoring():
    diag=NS(normalize_task=lambda s,*_:s["totals"],partition=lambda x:{k:v for k,v in x[0].items() if k!="split"})
    wide=NS(schedule_stats=stats,LengthReadout=Toy,score_length=lambda data,raw,c:raw)
    return wide,diag


def make_records(data):
    records=[]; wide,_=scoring(); ps=NS(pairs_from_rows=pairs_from_rows)
    for seed,arm in b.identities():
        events=b.schedule(seed,arm,data,ps)
        raw={str(n):dict(passed=True,totals=[dict(split=s,rows=k,correct=k,direct_pass=True,full_pass=True) for s,k in (("TRAIN",576),("HOLDOUT",288))]) for n in b.LENGTHS}
        records.append(dict(seed=seed,arm=arm,parameters=14256,slots=64,initial_sha256=b.digest([seed]),final_sha256=b.digest([seed,arm,"final"]),
            core_initial_sha256=b.digest([seed,"core"]),core_final_sha256=b.digest([seed,arm,"corefinal"]),raw=raw,
            forward_calls=1308,row_presentations=67968,core_forward_calls=5232,checkpoint_roundtrip=True,reload_max_error=0.,
            replay_forward_calls=108,replay_row_presentations=10368,replay_core_forward_calls=432,
            fit=dict(steps=1200,training_rows=57600,optimizer_creations=1,fit_rng=b.FIT_RNG,trainable_parameters=14256,
                ce_history=[.1]*1200,optimizer_group_lrs=[[.005,.0005]]*1200,gradient_parameter_counts=[1]*1200,gradient_union={"fixture":1},
                schedule_events=events,value_pair_counts=b.batch_value_counts(events,data["TRAIN"]),**stats(events))))
    return records


def protection():
    pins={n:"a"*40 for n in b.OWN}; pins.update(b.PINNED)
    while len(pins)<718: pins["fixture/"+str(len(pins))]="a"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1343)}


class Audit:
    @staticmethod
    def sha(path):
        p=Path(path); return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n): return Path(root)/n
    @staticmethod
    def git(root,*args):
        return b"f"*40 if args[0]=="rev-parse" else b"feat/sft-target-loss" if args[0]=="branch" else b""


def payload(summary):
    pins,protected=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=[dict(file=n) for n in b.OUTPUTS],
        validation_summary=summary,gate_f_candidate=False,production_adoption=False)


@contextlib.contextmanager
def counted(model,core):
    calls=[0,0]; cores=[0]
    def m(_,args,out): calls[0]+=1; calls[1]+=len(args[0])
    def c(*args): cores[0]+=1
    h=model.register_forward_hook(m); g=model.backbone.core.register_forward_hook(c)
    try: yield calls,cores
    finally: h.remove(); g.remove()


def evaluate_toy(model,prompts,data,c):
    b.require(not model.training and not any(p.requires_grad for p in model.parameters()),"frozen evaluator")
    with torch.no_grad():
        for _ in range(108): model(torch.zeros((96,64),dtype=torch.int64),torch.zeros(96,dtype=torch.int64))
    return {"fixture":fingerprint(model)}


class C312Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.deterministic=torch.are_deterministic_algorithms_enabled(); torch.set_num_threads(2)
        cls.data=dataset(); cls.ps=NS(pairs_from_rows=pairs_from_rows); cls.wide,cls.diag=scoring(); cls.policy=policy_fixture(); cls.x,cls.y=tables(cls.data)
        cls.records=make_records(cls.data); cls.metrics,cls.summary=b.analyze(cls.records,cls.data,cls.ps,cls.wide,cls.diag,None)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.deterministic)

    def test_01_seal(self): b.validate_seal(); self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_unsealed(self):
        with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaises(ValueError): b.validate_seal()

    def test_03_canonical_dataset(self):
        self.assertEqual(b.digest(self.data),b.DATA_SHA); pp,strata=b.pair_inventory(self.data["TRAIN"],self.ps)
        self.assertEqual([strata.count(i) for i in range(8)],[12]*8); self.assertEqual(pp.shape,(96,2))

    def test_04_all_seeds_epoch_exposure(self):
        for seed in b.SEEDS:
            plans=b.check_plan_pair(seed,self.data,self.ps,self.wide)
            for p in plans.values(): self.assertEqual(stats(p)["per_length_row_exposures"],[[100]*192]*3)

    def test_05_independent_random_reference(self):
        seed=b.SEEDS[0]; order=b.ORDERS[0]; got=b.schedule(seed,b.ARMS[0],self.data,self.ps); pp=pairs_from_rows(self.data["TRAIN"])
        for epoch in range(300):
            perm=torch.randperm(96,generator=torch.Generator().manual_seed(order+306000+epoch))
            for j in range(4): self.assertTrue(torch.equal(got[4*epoch+j,:,2:],pp[perm[j*24:(j+1)*24]]))

    def test_06_independent_balanced_reference(self):
        pp=pairs_from_rows(self.data["TRAIN"]); seed=b.SEEDS[0]; got=b.schedule(seed,b.ARMS[1],self.data,self.ps)
        for epoch in (0,1,73,299):
            rank=torch.randperm(96,generator=torch.Generator().manual_seed(b.ORDERS[0]+306000+epoch)).tolist(); counts={v:0 for v in b.TRAIN_VALUES}; groups=[[] for _ in range(4)]
            for i in rank:
                v=tuple(self.data["TRAIN"][int(pp[i,0])]["values"]); groups[counts[v]//3].append(i); counts[v]+=1
            for j,g in enumerate(groups): self.assertTrue(torch.equal(got[4*epoch+j,:,2:],pp[g]))

    def test_07_target_balance_and_pair_integrity(self):
        plan=b.schedule(b.SEEDS[0],b.ARMS[1],self.data,self.ps)
        for e in plan:
            self.assertEqual(torch.bincount(self.y[e[:,2:].flatten()]-48,minlength=4).tolist(),[12]*4)
            for a,z in e[:,2:].tolist(): self.assertNotEqual(self.data["TRAIN"][a]["query"],self.data["TRAIN"][z]["query"])

    def test_08_no_extra_rng_or_inputs(self):
        torch.manual_seed(99); before=torch.get_rng_state().clone(); p=b.schedule(b.SEEDS[0],b.ARMS[1],self.data,self.ps)
        self.assertTrue(torch.equal(before,torch.get_rng_state())); self.assertLess(int(p[:,:,2:].max()),192)
        with self.assertRaises(ValueError): b.schedule(309002,b.ARMS[0],self.data,self.ps)

    def test_09_bad_pair_contract(self):
        for bad in (torch.zeros((96,2),dtype=torch.int64),pairs_from_rows(self.data["TRAIN"]).float()):
            with self.assertRaises(ValueError): b.pair_inventory(self.data["TRAIN"],NS(pairs_from_rows=lambda _:bad))
        rows=copy.deepcopy(self.data["TRAIN"]); rows[0]["target"]=52
        with self.assertRaises(ValueError): b.pair_inventory(rows,self.ps)

    def test_10_holdout_never_augmented(self):
        rows=copy.deepcopy(self.data["TRAIN"]); key=rows[0]["values"]
        for r in rows:
            if r["values"]==key: r["values"]=[0,2]; r["target"]=48+r["values"][r["entities"].index(r["query"])]
        with self.assertRaises(ValueError): b.pair_inventory(rows,self.ps)

    def test_11_model_factory_shared_initial_independent_storage(self):
        models=b.make_models(b.SEEDS[0],self.policy,self.wide,factory_fixture())
        self.assertEqual(len({fingerprint(m) for m in models.values()}),1)
        ptrs=[p.data_ptr() for m in models.values() for p in m.parameters()]; self.assertEqual(len(ptrs),len(set(ptrs)))
        self.assertEqual({sum(p.numel() for p in m.parameters()) for m in models.values()},{14256})

    def test_12_full_fit_independent_reference(self):
        torch.manual_seed(5); a=Toy(); z=copy.deepcopy(a)
        with contextlib.redirect_stdout(io.StringIO()): f=b.fit(a,self.data,self.x,self.y,b.SEEDS[0],b.ARMS[1],self.ps,self.wide,self.policy)
        torch.manual_seed(b.FIT_RNG); opt=self.policy.optimizer_for(z,"core_slow"); history=[]
        for e in b.schedule(b.SEEDS[0],b.ARMS[1],self.data,self.ps):
            opt.zero_grad(set_to_none=True); ids=e[:,2:].flatten(); out=z(self.x[e[:,0].repeat_interleave(2),e[:,1].repeat_interleave(2),ids],torch.zeros(48,dtype=torch.int64))
            loss=F.cross_entropy(out,self.y[ids]); history.append(float(loss.detach())); loss.backward(); torch.nn.utils.clip_grad_norm_(list(z.parameters()),1.,error_if_nonfinite=True); opt.step()
        self.assertEqual(history,f["ce_history"]); self.assertEqual(fingerprint(a),fingerprint(z)); b.check_fit(f,b.SEEDS[0],b.ARMS[1],self.data,self.ps,self.wide)

    def test_13_bad_history_and_schedule(self):
        for k in ("ce_history","optimizer_group_lrs","value_pair_counts"):
            f=copy.deepcopy(self.records[0]["fit"]); f[k]=[]
            with self.assertRaises(ValueError): b.check_fit(f,b.SEEDS[0],b.ARMS[0],self.data,self.ps,self.wide)
        f=copy.deepcopy(self.records[0]["fit"]); f["schedule_events"][0,0,2]=999
        with self.assertRaises(ValueError): b.check_fit(f,b.SEEDS[0],b.ARMS[0],self.data,self.ps,self.wide)

    def test_14_train_and_replay_actual_path(self):
        torch.manual_seed(7); m=Toy(); c=NS(base=NS(fingerprint=fingerprint),p267=NS(counted=counted),core=None)
        wide=NS(schedule_stats=stats,evaluate=evaluate_toy,replay_error=lambda x,y,*_:0. if x==y else float("inf"))
        with contextlib.redirect_stdout(io.StringIO()): r,state=b.train_one(m,self.data,{},self.x,self.y,b.SEEDS[0],b.ARMS[0],self.ps,wide,c,self.policy)
        b.replay(Toy(),state,r,self.data,{},wide,c); self.assertTrue(r["checkpoint_roundtrip"]); self.assertEqual(r["reload_max_error"],0.)
        wrong=copy.deepcopy(state); wrong["read.bias"]+=1
        with self.assertRaises(ValueError): b.replay(Toy(),wrong,r,self.data,{},wide,c)

    def test_15_analysis_gate_and_totals(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["contrasts"])),(10,80,40)); b.validate_result(payload(self.summary))
        self.assertEqual(self.summary["paired_five"],[dict(both_pass=5,control_only=0,candidate_only=0,both_fail=0)][0])

    def test_16_candidate_negative_not_relabelled(self):
        records=copy.deepcopy(self.records); records[1]["raw"]["5"]["passed"]=False
        _,s=b.analyze(records,self.data,self.ps,self.wide,self.diag,None); p=payload(s); self.assertEqual(p["status"],"FAIL"); b.validate_result(p)
        p["status"]="PASS"
        with self.assertRaises(ValueError): b.validate_result(p)

    def test_17_missing_cohort_and_mismatch(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.data,self.ps,self.wide,self.diag,None)
        records=copy.deepcopy(self.records); records[1]["initial_sha256"]="different"
        with self.assertRaises(ValueError): b.analyze(records,self.data,self.ps,self.wide,self.diag,None)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c312-fixture")/str(i)/"summary.json").resolve() for i in range(38)]
        p=dict(experiment_id="C311-v5b-saved-error-context",commit_sha=b.PARENT_EXECUTION,status="PASS",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
            artifacts=[dict(file=n) for n in ("audit-plan.json","error-context-report.json","validation-summary.json")],validation_summary=dict(observations=51840,capability_gate_applicable=False))
        parent=NS(context=lambda:(None,),parent_hashes=lambda _:tuple(str(i%10)*64 for i in range(37)),OUTPUTS=tuple(a["file"] for a in p["artifacts"]),verify_artifacts=Mock(return_value=(p,{})),validate_result=Mock())
        hashes=dict(zip(map(str,paths),(b.PARENT_SHA,*parent.parent_hashes(None)),strict=True)); prompts={"synthetic":1}
        c=NS(audit=NS(sha=lambda path:hashes[str(path)],read_json=lambda path:self.data if path.name=="dataset.json" else prompts),p267=NS(validate_data=lambda d:self.assertEqual(d,self.data)))
        wide=NS(prompt_dataset=lambda d:prompts,validate_prompts=lambda *a:None)
        with patch.object(b,"context",return_value=(parent,NS(no_neural=contextlib.nullcontext),None,None,wide,None,None,None,c)),patch.object(b,"PROMPTS_SHA",b.digest(prompts)):
            yield paths,hashes,parent,p

    def test_18_all38_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,hashes,parent,p):
            self.assertEqual(b.load_parent(paths)[0],p); parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=hashes[str(path)]; hashes[str(path)]="f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); hashes[str(path)]=old

    def test_19_parent_identity_and_scope(self):
        for fn in (lambda p:p.update(status="FAIL"),lambda p:p["artifacts"].pop(),lambda p:p["validation_summary"].update(capability_gate_applicable=True)):
            with self.loader_fixture() as (paths,_,_,p):
                fn(p)
                with self.assertRaises(ValueError): b.load_parent(paths)

    def test_20_protection_actual_precheck(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pins=dict(b.PINNED)
            while len(pins)<712: pins["accepted/"+str(len(pins))]="b"*40
            for n in list(pins)+list(b.OWN): p=root/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(n,encoding="utf-8")
            protected={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1333-len(protected)):
                p=root/("input"+str(i)); p.write_text("data",encoding="utf-8"); protected[str(p.resolve())]=Audit.sha(p)
            folder=root/"parent"; folder.mkdir(); path=folder/"summary.json"; path.write_text("summary",encoding="utf-8"); special={str(path.resolve()):b.PARENT_SHA}; artifacts=[]
            for n in ("audit-plan.json","error-context-report.json","validation-summary.json"):
                p=folder/n; p.write_text("artifact",encoding="utf-8"); artifacts.append(dict(file=n,sha256=Audit.sha(p)))
            def sha(p): return special.get(str(Path(p).resolve()),Audit.sha(p))
            parent=types.ModuleType("parent"); parent.__file__=str(root/b.PARENT_SOURCE)
            p309=NS(context=lambda:(),FIT_RNG=b.FIT_RNG); wide=NS(PINNED=b.PINNED,context=lambda:()); c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,git=lambda root,*a:(pins.get(a[1][5:],"c"*40)+"\n").encode(),safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            p=dict(source_blobs=pins,input_sha256=protected,artifacts=artifacts)
            with patch.object(b,"context",return_value=(parent,None,p309,self.policy,wide,None,None,None,c)),patch.object(b,"load_parent",return_value=(p,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([path]*38,root))),(718,1343))
                c.missing=types.ModuleType("missing"); c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([path]*38,root)

    def test_21_semantic_regression(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["f."+str(i) for i in range(4997)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            self.assertEqual({t.id() for t in b.flatten(b.regression_suite(Path.cwd()))},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError): b.regression_suite(Path.cwd())

    @contextlib.contextmanager
    def run_fixture(self):
        wide,diag=scoring(); wide.training_tables=lambda d:tables(d); c=NS(audit=Audit()); events=[]
        def train(*a): events.append("train"); return copy.deepcopy(self.records[b.identities().index((a[5],a[6]))]),{}
        def replay(*a): events.append("replay")
        def pc(*a): events.append("precheck"); return protection()
        with patch.object(b,"context",return_value=(None,NS(no_neural=contextlib.nullcontext),None,self.policy,wide,self.ps,diag,None,c)),patch.object(b,"precheck",side_effect=pc),patch.object(b,"load_parent",return_value=({},self.data,{"synthetic":1})),patch.object(b,"make_models",return_value=dict.fromkeys(b.ARMS)),patch.object(b,"train_one",side_effect=train),patch.object(b,"replay",side_effect=replay):
            yield events

    def test_22_run_order_and_roundtrip(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*38,output_dir=out,expected_head="f"*40)
            self.assertEqual(events.count("train"),10); self.assertEqual(events.count("replay"),10); self.assertLess(max(i for i,v in enumerate(events) if v=="train"),events.index("replay"))
            q,_=b.verify_artifacts(out,["x"]*38,"f"*40); self.assertEqual(p,q)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*38,output_dir=out,expected_head="f"*40)

    def test_23_tampering(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*38,output_dir=out,expected_head="f"*40); target=out/"measurements.json"; target.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*38,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==target.name); a.update(sha256=Audit.sha(target),serialized_bytes=target.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*38,"f"*40)

    def test_24_bundle_and_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"m.pt"; v=dict(schema="fold-c312-value-batches-models-v1",identities=[list(x) for x in b.identities()],states=[{}]*10); torch.save(v,path)
            self.assertEqual(len(b.load_bundle(path)),10); v["identities"].reverse(); torch.save(v,path)
            with self.assertRaises(ValueError): b.load_bundle(path)
        with self.assertRaises(ValueError): b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))

    def test_25_runtime_preflight_actual_call_path(self):
        c=factory_fixture(); wide=NS(**vars(self.wide),training_tables=lambda d:tables(d))
        p309=NS(SEEDS=(309001,),ORDERS=(309101,),schedule=lambda seed,rows,pairs:b.plan_for_order(309101,b.ARMS[0],rows,pairs))
        with patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,{})),patch.object(b,"context",return_value=(None,None,p309,self.policy,wide,self.ps,None,None,c)),contextlib.redirect_stdout(io.StringIO()): b.runtime_preflight(["x"]*38,Path.cwd())

    def test_26_cli_and_modules(self):
        argv=["prog","--summaries"]+[str(i) for i in range(38)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),38)
        parent=NS(regression_modules=lambda root:["m"+str(i) for i in range(196)])
        with patch.object(b,"context",return_value=(parent,)): self.assertEqual(len(b.regression_modules(Path.cwd())),197)

    def test_27_utf8_and_seal_document(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for p in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="read_text": self.assertTrue(any(k.arg=="encoding" for k in n.keywords))

    def test_28_runner_indices_and_paths(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: compile(code,"runner","exec")
        self.assertIn("sys.argv[2:40]",blocks[2]); self.assertIn("head = sys.argv[40]",blocks[2]); self.assertIn("len(sys.argv) == 41",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),38)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute")); self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_29_accepted_schedule_and_stats_functions(self):
        root=Path(__file__).resolve().parents[1]; space=dict(torch=torch,require=b.require,STEPS=1200,SEEDS=(309001,),ORDERS=(309101,),digest=b.digest)
        for path,fn in (("fold_lm/v05_benchmarks/model_c309_core_lr_replication.py","schedule"),("fold_lm/v05_benchmarks/model_c304_length_breadth.py","schedule_stats")):
            tree=ast.parse((root/path).read_text(encoding="utf-8")); node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==fn)
            exec(compile(ast.Module(body=[node],type_ignores=[]),path,"exec"),space)
        ref=space["schedule"](309001,self.data["TRAIN"],self.ps); actual=b.plan_for_order(309101,b.ARMS[0],self.data["TRAIN"],self.ps)
        self.assertTrue(torch.equal(ref,actual)); self.assertEqual(space["schedule_stats"](actual),stats(actual))

    def test_30_actual_accepted_optimizer_functions(self):
        root=Path(__file__).resolve().parents[1]; path=root/"fold_lm/v05_benchmarks/model_c308_core_learning_rate.py"
        names=("configure","parameter_groups","optimizer_for","verify_optimizer"); tree=ast.parse(path.read_text(encoding="utf-8"))
        space=dict(torch=torch,require=b.require,ARMS=("full_train","core_frozen","core_slow"),BASE_LR=.005,CORE_LR=.0005,manifest=lambda:dict(trainable_parameters=dict(full_train=14256,core_frozen=10928,core_slow=14256)))
        exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(path),"exec"),space)
        m=Toy(); space["configure"](m,"core_slow"); o=space["optimizer_for"](m,"core_slow"); space["verify_optimizer"](o,m,"core_slow")
        self.assertEqual([g["lr"] for g in o.param_groups],[.005,.0005]); o.param_groups[1]["lr"]*=10
        with self.assertRaises(ValueError): space["verify_optimizer"](o,m,"core_slow")

    def test_31_context_adapter(self):
        c=NS(); p309=NS(context=lambda:(1,2,3,4,5,6,7,8,c)); p310=NS(context=lambda:(p309,)); parent=NS(context=lambda:(p310,c))
        package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c311_saved_error_context=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}): self.assertEqual(b.context(),(parent,p310,p309,1,5,6,7,8,c))

    def test_32_imports_count_and_original_flags(self):
        tree=ast.parse(Path(b.__file__).read_text(encoding="utf-8")); imports=[n.names[0].name for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c311_saved_error_context"]); self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),32)
        p=payload(copy.deepcopy(self.summary)); p["gate_f_candidate"]=True
        with self.assertRaises(ValueError): b.validate_result(p)


if __name__=="__main__": unittest.main()
