"""Software controls for C315; fixtures are not actual FOLD generalization evidence."""
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
from unittest.mock import Mock,patch
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import model_c315_single_character_mix as b


def dataset():
    out={"TRAIN":[],"HOLDOUT":[]}
    for entities,values,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (values[1]-values[0])%4==2 else "TRAIN"
        for order,query in itertools.product((entities,entities[::-1]),entities):
            out[split].append(dict(id=f"{lang}:{entities}:{values}:{order}:{query}",entities=list(entities),values=list(values),language=lang,
                permutation=list(order),query=query,target=48+values[entities.index(query)]))
    return out


def render(row,n,profile,view="normal"):
    chars="abc" if row["language"]=="en" else "甲乙丙"; a,z=row["entities"]
    names={a:chars[a]*n,z:chars[z]*n}
    if profile=="shared_prefix": names[z]=chars[a]*(n-1)+chars[z]
    if profile=="shared_suffix": names[z]=chars[z]+chars[a]*(n-1)
    return ";".join(names[k]+"="+("?" if view=="evidence_blind" else str(row["values"][row["entities"].index(k)])) for k in row["permutation"])+";"+("?" if view=="query_blind" else names[row["query"]])+"="


def prefix(text):
    raw=list(text.encode("utf-8")); b.require(len(raw)+2<=64,"overflow")
    return torch.tensor([257,*raw,258,*([256]*(62-len(raw)))],dtype=torch.int64)


def span(x):
    out=torch.zeros_like(x,dtype=torch.bool)
    for i,row in enumerate(x.tolist()):
        end=row.index(258)-1; start=max(j for j,v in enumerate(row[:end]) if v==59)+1
        out[i,start:end]=True
    return out


def pairs_from_rows(rows):
    groups={}
    for i,r in enumerate(rows):
        key=(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups.setdefault(key,[]).append(i)
    return torch.tensor([sorted(groups[k],key=lambda i:rows[i]["query"]) for k in sorted(groups)],dtype=torch.int64)


def pair_inventory(rows,pairs):
    b.require(len(rows)==192,"TRAIN rows"); pp=pairs.pairs_from_rows(rows)
    b.require(pp.shape==(96,2) and sorted(pp.flatten().tolist())==list(range(192)),"pairs")
    for a,z in pp.tolist():
        b.require(all(rows[a][k]==rows[z][k] for k in ("entities","values","permutation","language")) and rows[a]["query"]!=rows[z]["query"],"paired facts")
    return pp,[]


def legacy_plan(order,arm,rows,pairs):
    assert arm=="random_pairs"
    pp=pairs.pairs_from_rows(rows); events=torch.empty((1200,24,4),dtype=torch.int64)
    for epoch in range(300):
        rank=torch.randperm(96,generator=torch.Generator().manual_seed(order+306000+epoch))
        for j in range(4):
            events[epoch*4+j,:,0]=epoch%3; events[epoch*4+j,:,1]=(epoch//3+epoch%3)%3
            events[epoch*4+j,:,2:]=pp[rank[24*j:24*(j+1)]]
    return events


def old_policy(): return NS(pair_inventory=pair_inventory,plan_for_order=legacy_plan,FIT_RNG=612000)


def check_logits(z,n):
    b.require(z.shape==(n,256) and z.dtype==torch.float64 and z.device.type=="cpu" and bool(torch.isfinite(z).all()),"logit contract")


def raw(data):
    zs={}
    for s in b.SPLITS:
        z=torch.zeros((len(data[s]),256),dtype=torch.float64); y=torch.tensor([r["target"] for r in data[s]]); z[torch.arange(len(y)),y]=5.; zs[s]=z
    return {str(n):{s:{p:{v:zs[s] for v in b.VIEWS} for p in b.profiles(n)} for s in b.SPLITS} for n in range(1,7)}


def score(data,rr,c):
    totals=[]
    for s in b.SPLITS:
        y=torch.tensor([r["target"] for r in data[s]]); correct=sum(int((rr[s][p]["normal"].argmax(1)==y).sum()) for p in b.PROFILES)
        totals.append(dict(split=s,rows=3*len(y),correct=correct,direct_pass=correct==3*len(y),full_pass=correct==3*len(y)))
    return dict(passed=all(t["full_pass"] for t in totals),totals=totals)


def scoring():
    wide=NS(prefix_tensor=prefix,span_mask=span,score_length=score)
    diag=NS(normalize_task=lambda s,*_:s["totals"],partition=lambda r:{k:v for k,v in r[0].items() if k!="split"})
    return wide,diag,NS(p267=NS(check_logits=check_logits))


def fixture_records(data,p312,pairs):
    rr=[]; predicted=raw(data)
    for seed,arm in b.identities():
        e=b.schedule(seed,arm,data,p312,pairs)
        rr.append(dict(seed=seed,arm=arm,initial_sha256=b.digest([seed]),core_initial_sha256=b.digest([seed,"core"]),final_sha256=b.digest([seed,arm,"final"]),
            core_final_sha256=b.digest([seed,arm,"corefinal"]),raw=predicted,checkpoint_roundtrip=True,reload_max_error=0.,
            forward_calls=1344,row_presentations=71424,core_forward_calls=5376,replay_forward_calls=144,replay_row_presentations=13824,replay_core_forward_calls=576,
            fit=dict(steps=1200,training_rows=57600,fit_rng=612000,optimizer_creations=1,trainable_parameters=14256,ce_history=[.1]*1200,
                optimizer_group_lrs=[[.005,.0005]]*1200,gradient_parameter_counts=[1]*1200,gradient_union={"fixture":1},schedule_events=e,**b.schedule_stats(e))))
    return rr


def fingerprint(m):
    h=hashlib.sha256()
    for n,z in sorted(m.state_dict().items()): h.update(n.encode()); h.update(z.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


class Core(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.linear=torch.nn.Linear(8,8,dtype=torch.float64); self.padding=torch.nn.Parameter(torch.zeros(3256,dtype=torch.float64)); self.config=NS(slots=64)
    def forward(self,x): return torch.tanh(self.linear(x))


class Toy(torch.nn.Module):
    def __init__(self,reference=None):
        super().__init__()
        if reference is not None:
            self.backbone=copy.deepcopy(reference.backbone); self.read=copy.deepcopy(reference.read); return
        self.backbone=torch.nn.Module(); self.backbone.embed=torch.nn.Embedding(4,8,dtype=torch.float64); self.backbone.core=Core(); self.backbone.config=NS(max_tokens=64)
        self.read=torch.nn.Linear(8,256,dtype=torch.float64); self.backbone.padding=torch.nn.Parameter(torch.zeros(14256-sum(p.numel() for p in self.parameters()),dtype=torch.float64))
    def forward(self,x,t):
        assert x.shape==(len(x),64) and t.shape==(len(x),) and not bool(t.any())
        h=self.backbone.embed(x[:,0]%4)
        for _ in range(4): h=self.backbone.core(h)
        return self.read(h)


def optimizer_policy():
    def groups(m,arm):
        assert arm=="core_slow"
        return [dict(params=[p for n,p in m.named_parameters() if not n.startswith("backbone.core.")],lr=.005),dict(params=list(m.backbone.core.parameters()),lr=.0005)]
    def opt(m,arm): return torch.optim.AdamW(groups(m,arm),betas=(.9,.999),eps=1e-8,weight_decay=0.)
    def verify(o,m,arm):
        for got,want in zip(o.param_groups,groups(m,arm),strict=True):
            b.require(got["lr"]==want["lr"] and [id(p) for p in got["params"]]==[id(p) for p in want["params"]],"optimizer policy")
    return NS(configure=lambda m,a:m.requires_grad_(True),parameter_groups=groups,optimizer_for=opt,verify_optimizer=verify,CORE_LR=.0005,BASE_LR=.005)


def factory():
    def new(seed):
        with torch.random.fork_rng(): torch.manual_seed(seed); return Toy()
    return NS(factory=NS(new_model=new,language_module=lambda:None),c278=NS(MeanFinalDualReadout=lambda m,*_:m),reader=None,
        c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint),p267=NS(check_logits=check_logits,counted=counted),core=None)


@contextlib.contextmanager
def counted(model,core):
    calls=[0,0]; cores=[0]
    def m(_,args,out): calls[0]+=1; calls[1]+=len(args[0])
    def c(*a): cores[0]+=1
    mh=model.register_forward_hook(m); ch=model.backbone.core.register_forward_hook(c)
    try: yield calls,cores
    finally: mh.remove(); ch.remove()


def protection():
    pins={n:"a"*40 for n in b.OWN}; pins.update(b.PINNED)
    while len(pins)<736: pins["fixture/"+str(len(pins))]="a"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1379)}


class Audit:
    @staticmethod
    def sha(path):
        p=Path(path); return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n): return Path(root)/n
    @staticmethod
    def git(root,*a): return b"f"*40 if a[0]=="rev-parse" else b"feat/sft-target-loss" if a[0]=="branch" else b""


def payload(s):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if s["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,production_adoption=False)


class C315Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.det=torch.are_deterministic_algorithms_enabled(); torch.set_num_threads(2)
        cls.data=dataset(); cls.pairs=NS(pairs_from_rows=pairs_from_rows); cls.p312=old_policy(); cls.p313=NS(render=render)
        cls.wide,cls.diag,cls.c=scoring(); cls.wide.LengthReadout=Toy; cls.policy=optimizer_policy()
        cls.prompts=b.prompt_dataset(cls.data,cls.p313); cls.old={str(n):cls.prompts[str(n)] for n in (2,3,4,5)}; cls.six=cls.prompts["6"]
        cls.tables,cls.y=b.training_tables(cls.data,cls.prompts,cls.wide)
        cls.fit_tables={k:torch.zeros_like(x) for k,x in cls.tables.items()}
        for x in cls.fit_tables.values(): x[:,0]=cls.y-48
        cls.records=fixture_records(cls.data,cls.p312,cls.pairs)
        cls.metrics,cls.summary=b.analyze(cls.records,cls.data,cls.p312,cls.pairs,cls.wide,cls.diag,cls.c)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.det)

    def test_01_seal_and_json(self):
        b.validate_seal(); self.assertEqual(json.loads(b.blob(b.manifest())),b.manifest())
        with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaises(ValueError): b.validate_seal()

    def test_02_canonical_data_and_old_prompts(self):
        self.assertEqual(b.digest(self.data),b.DATA_SHA); self.assertEqual(b.digest(self.old),b.OLD_SHA); self.assertEqual(b.digest(self.six),b.SIX_SHA)
        b.validate_prompts(self.data,self.prompts,self.old,self.six,self.p313,self.wide)

    def test_03_single_profile_not_tripled(self):
        self.assertEqual(b.profiles(1),("repeat",)); self.assertEqual(len(self.prompts["1"]["TRAIN"]),1)
        for s in b.SPLITS:
            for row in self.data[s]:
                self.assertEqual({render(row,1,p) for p in b.PROFILES},{b.render_one(row)})
        self.assertEqual(sum(len(pp) for s in self.prompts["1"].values() for pp in s.values()),288)

    def test_04_query_span_and_no_truncation(self):
        for s in b.SPLITS:
            for row in self.data[s]:
                for v in b.VIEWS:
                    text=b.render_one(row,v); x=prefix(text); expected=1 if v=="query_blind" or row["language"]=="en" else 3
                    self.assertEqual(int(span(x[None,:]).sum()),expected)
        with self.assertRaises(ValueError): prefix("甲"*22)
        with self.assertRaises(ValueError): b.profiles(True)

    def test_05_tables_training_boundary(self):
        self.assertEqual(len(self.tables),10); self.assertEqual(set(n for n,p in self.tables),{1,2,3,4})
        self.assertEqual(sum(len(x) for x in self.tables.values()),1920)
        self.assertEqual(self.y.tolist(),[r["target"] for r in self.data["TRAIN"]])

    def test_06_every_seed_budget_and_order(self):
        for seed in b.SEEDS:
            plans=b.check_plans(seed,self.data,self.p312,self.pairs)
            self.assertTrue(torch.equal(plans[b.ARMS[0]][:,:,2:],plans[b.ARMS[1]][:,:,2:]))
        stats=b.schedule_stats(plans[b.ARMS[1]])
        self.assertEqual(stats["length_profile_updates"],[[300,0,0],[100,100,100],[100,100,100],[100,100,100]])

    def test_07_independent_candidate_schedule(self):
        pp=pairs_from_rows(self.data["TRAIN"]); got=b.schedule(b.SEEDS[0],b.ARMS[1],self.data,self.p312,self.pairs)
        for epoch in (0,1,4,57,299):
            n=1+epoch%4; p=0 if n==1 else (epoch//4+n-2)%3
            rank=torch.randperm(96,generator=torch.Generator().manual_seed(b.ORDERS[0]+306000+epoch))
            for j in range(4):
                self.assertTrue(torch.equal(got[4*epoch+j,:,2:],pp[rank[24*j:24*(j+1)]])); self.assertEqual(got[4*epoch+j,0,:2].tolist(),[n,p])

    def test_08_global_rng_unchanged_and_epoch_coverage(self):
        torch.manual_seed(99); before=torch.get_rng_state().clone(); p=b.schedule(b.SEEDS[0],b.ARMS[1],self.data,self.p312,self.pairs)
        self.assertTrue(torch.equal(before,torch.get_rng_state()))
        for epoch in range(300): self.assertEqual(sorted(p[4*epoch:4*epoch+4,:,2:].flatten().tolist()),list(range(192)))
        with self.assertRaises(ValueError): b.schedule(312002,b.ARMS[0],self.data,self.p312,self.pairs)

    def test_09_actual_parent_control_schedule(self):
        path=Path(__file__).resolve().parents[1]/"fold_lm/v05_benchmarks/model_c312_value_balanced_batches.py"
        tree=ast.parse(path.read_text(encoding="utf-8")); names={"pair_inventory","plan_for_order"}
        space=dict(torch=torch,require=b.require,STEPS=1200,ARMS=("random_pairs","value_balanced"),TRAIN_VALUES=tuple((a,z) for a in range(4) for z in range(4) if (z-a)%4 in (1,3)))
        exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(path),"exec"),space)
        actual=space["plan_for_order"](b.ORDERS[0],"random_pairs",self.data["TRAIN"],self.pairs); actual[:,:,0]+=2
        self.assertTrue(torch.equal(actual,b.schedule(b.SEEDS[0],b.ARMS[0],self.data,self.p312,self.pairs)))
        broken=list(self.data["TRAIN"]); broken[0]=dict(broken[0],target=77)
        with self.assertRaises(ValueError): space["pair_inventory"](broken,self.pairs)

    def test_10_initial_models_and_storage(self):
        models=b.make_models(b.SEEDS[0],self.wide,self.policy,factory()); self.assertEqual(len({fingerprint(m) for m in models.values()}),1)
        ptr=[p.data_ptr() for m in models.values() for p in m.parameters()]; self.assertEqual(len(ptr),len(set(ptr)))
        self.assertEqual({sum(p.numel() for p in m.parameters()) for m in models.values()},{14256})

    def test_11_fit_independent_full_loop(self):
        torch.manual_seed(5); a=Toy(); ref=copy.deepcopy(a)
        with contextlib.redirect_stdout(io.StringIO()): f=b.fit(a,self.data,self.fit_tables,self.y,b.SEEDS[0],b.ARMS[1],self.p312,self.pairs,self.policy)
        torch.manual_seed(b.FIT_RNG); opt=self.policy.optimizer_for(ref,"core_slow"); losses=[]
        for event in b.schedule(b.SEEDS[0],b.ARMS[1],self.data,self.p312,self.pairs):
            n,p=event[0,:2].tolist(); ids=event[:,2:].flatten(); opt.zero_grad(set_to_none=True)
            loss=F.cross_entropy(ref(self.fit_tables[n,b.PROFILES[p]][ids],torch.zeros(48,dtype=torch.int64)),self.y[ids]); losses.append(float(loss.detach()))
            loss.backward(); torch.nn.utils.clip_grad_norm_(list(ref.parameters()),1.,error_if_nonfinite=True); opt.step()
        self.assertEqual(losses,f["ce_history"]); self.assertEqual(fingerprint(a),fingerprint(ref)); b.check_fit(f,b.SEEDS[0],b.ARMS[1],self.data,self.p312,self.pairs)

    def test_12_fit_trace_tamper(self):
        for k in ("ce_history","optimizer_group_lrs","gradient_parameter_counts"):
            f=copy.deepcopy(self.records[0]["fit"]); f[k]=[]
            with self.assertRaises(ValueError): b.check_fit(f,b.SEEDS[0],b.ARMS[0],self.data,self.p312,self.pairs)
        f=copy.deepcopy(self.records[0]["fit"]); f["schedule_events"][0,0,0]=1
        with self.assertRaises(ValueError): b.check_fit(f,b.SEEDS[0],b.ARMS[0],self.data,self.p312,self.pairs)

    def test_13_real_train_eval_replay_counts(self):
        torch.manual_seed(7); m=Toy(); c=factory()
        with contextlib.redirect_stdout(io.StringIO()): r,state=b.train_one(m,self.data,self.prompts,self.fit_tables,self.y,b.SEEDS[0],b.ARMS[0],self.p312,self.pairs,self.policy,self.wide,c)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(1344,71424)); b.replay(Toy(),state,r,self.data,self.prompts,self.wide,c)
        self.assertEqual(r["reload_max_error"],0.); self.assertEqual(r["replay_forward_calls"],144)
        state=copy.deepcopy(state); state["read.bias"]+=1
        with self.assertRaises(ValueError): b.replay(Toy(),state,r,self.data,self.prompts,self.wide,c)

    def test_14_real_evaluation_single_not_tripled(self):
        m=Toy(); m.eval(); m.requires_grad_(False); c=factory()
        with counted(m,None) as (calls,cores): z=b.evaluate(m,self.prompts,self.data,self.wide,c)
        self.assertEqual(calls,[144,13824]); self.assertEqual(cores,[576]); self.assertEqual(set(z["1"]["TRAIN"]),{"repeat"}); b.validate_raw(z,self.data,c)
        with self.assertRaises(ValueError): b.evaluate(Toy(),self.prompts,self.data,self.wide,c)

    def test_15_raw_replay_contract(self):
        z=raw(self.data); self.assertEqual(b.replay_error(z,z,self.data,self.c),0.)
        wrong=copy.deepcopy(z); wrong["1"]["TRAIN"]["shared_prefix"]=wrong["1"]["TRAIN"]["repeat"]
        with self.assertRaises(ValueError): b.validate_raw(wrong,self.data,self.c)
        wrong=copy.deepcopy(z); wrong["6"]["HOLDOUT"]["repeat"]["normal"]=torch.zeros(1)
        with self.assertRaises(ValueError): b.replay_error(z,wrong,self.data,self.c)

    def test_16_gate_and_single_diagnostics(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["single_character_diagnostics"])),(10,100,20)); b.validate_result(payload(self.summary))
        self.assertEqual({r["rows"] for r in self.summary["single_character_diagnostics"]},{192,96})
        rr=copy.deepcopy(self.records); rr[1]["raw"]=raw(self.data); rr[1]["raw"]["6"]=copy.deepcopy(rr[1]["raw"]["6"])
        rr[1]["raw"]["6"]["HOLDOUT"]["repeat"]["normal"][0,70]=9.
        _,s=b.analyze(rr,self.data,self.p312,self.pairs,self.wide,self.diag,self.c); p=payload(s); b.validate_result(p); self.assertEqual(p["status"],"FAIL")
        p["status"]="PASS"
        with self.assertRaises(ValueError): b.validate_result(p)

    def test_17_cohort_and_pairing(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.data,self.p312,self.pairs,self.wide,self.diag,self.c)
        rr=copy.deepcopy(self.records); rr[1]["initial_sha256"]="different"
        with self.assertRaises(ValueError): b.analyze(rr,self.data,self.p312,self.pairs,self.wide,self.diag,self.c)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c315-fixture")/str(i)/"summary.json").resolve() for i in range(41)]
        names=("audit-plan.json","boundary-report.json","validation-summary.json")
        p=dict(experiment_id="C314-v5b-saved-six-boundary-profile",commit_sha=b.PARENT_EXECUTION,status="PASS",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},artifacts=[dict(file=n) for n in names],
            validation_summary=dict(paired_rows=8640,observations=17280,new_error=89,both_wrong=3,six_correct=8548,capability_gate_applicable=False))
        parent=NS(context=lambda:(None,),parent_hashes=lambda _:tuple(str(i%10)*64 for i in range(40)),OUTPUTS=names,verify_artifacts=Mock(return_value=(p,{})),validate_result=Mock())
        hashes=dict(zip(map(str,paths),(b.PARENT_SHA,*parent.parent_hashes(None)),strict=True)); seen=[]
        def read(path):
            seen.append(str(path)); return {"dataset.json":self.data,"length-datasets.json":self.old,"six-dataset.json":self.six}[path.name]
        c=NS(audit=NS(sha=lambda p:hashes[str(p)],read_json=read),p267=NS(validate_data=lambda d:None))
        with patch.object(b,"context",return_value=(parent,self.p313,None,NS(no_neural=contextlib.nullcontext),self.wide,None,None,None,c)):
            yield paths,hashes,parent,p,seen

    def test_18_all41_parent_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,hashes,parent,p,seen):
            self.assertEqual(b.load_parent(paths)[0],p); parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            self.assertIn(str(paths[2].parent/"dataset.json"),seen); self.assertIn(str(paths[1].parent/"six-dataset.json"),seen)
            for path in paths:
                old=hashes[str(path)]; hashes[str(path)]="f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); hashes[str(path)]=old

    def test_19_parent_scope_and_artifacts(self):
        for change in (lambda p:p.update(status="FAIL"),lambda p:p["artifacts"].pop(),lambda p:p["validation_summary"].update(new_error=88)):
            with self.loader_fixture() as (paths,_,_,p,_):
                change(p)
                with self.assertRaises(ValueError): b.load_parent(paths)

    def test_20_actual_precheck_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pins=dict(b.PINNED)
            while len(pins)<730: pins["accepted/"+str(len(pins))]="a"*40
            for n in list(pins)+list(b.OWN): p=root/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1369-len(inputs)):
                p=root/("input"+str(i)); p.write_text("data",encoding="utf-8"); inputs[str(p.resolve())]=Audit.sha(p)
            folder=root/"parent"; folder.mkdir(); path=folder/"summary.json"; path.write_text("summary",encoding="utf-8"); special={str(path.resolve()):b.PARENT_SHA}; arts=[]
            for n in ("audit-plan.json","boundary-report.json","validation-summary.json"):
                p=folder/n; p.write_text("artifact",encoding="utf-8"); arts.append(dict(file=n,sha256=Audit.sha(p)))
            def sha(p): return special.get(str(Path(p).resolve()),Audit.sha(p))
            parent=types.ModuleType("parent"); parent.__file__=str(root/b.PARENT_SOURCE); parent.context=lambda:()
            p313=NS(context=lambda:()); p312=NS(context=lambda:(),FIT_RNG=612000); wide=NS(context=lambda:(),PINNED=b.PINNED)
            c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,git=lambda root,*a:(pins.get(a[1][5:],"b"*40)+"\n").encode(),safe_child=Audit.safe_child,
                protect_tree_files=lambda root,pp:{str((root/n).resolve()):sha(root/n) for n in pp}))
            p=dict(source_blobs=pins,input_sha256=inputs,artifacts=arts)
            with patch.object(b,"context",return_value=(parent,p313,p312,None,wide,self.policy,None,None,c)),patch.object(b,"load_parent",return_value=(p,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([path]*41,root))),(736,1379))
                c.missing=types.ModuleType("missing"); c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([path]*41,root)

    def test_21_real_runtime_preflight(self):
        with patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,self.prompts)),patch.object(b,"context",return_value=(None,None,self.p312,None,self.wide,self.policy,self.pairs,None,factory())),contextlib.redirect_stdout(io.StringIO()):
            b.runtime_preflight(["x"]*41,Path.cwd())

    @contextlib.contextmanager
    def run_fixture(self):
        c=NS(audit=Audit(),p267=NS(check_logits=check_logits)); events=[]
        def pc(*_): events.append("precheck"); return protection()
        def train(*a): events.append("train"); return self.records[b.identities().index((a[5],a[6]))],{}
        def replay(*a): events.append("replay")
        with patch.object(b,"context",return_value=(None,None,self.p312,NS(no_neural=contextlib.nullcontext),self.wide,self.policy,self.pairs,self.diag,c)),patch.object(b,"load_parent",return_value=({},self.data,self.prompts)),patch.object(b,"precheck",side_effect=pc),patch.object(b,"make_models",return_value=dict.fromkeys(b.ARMS)),patch.object(b,"train_one",side_effect=train),patch.object(b,"replay",side_effect=replay): yield events

    def test_22_production_run_bundle_and_roundtrip(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*41,output_dir=out,expected_head="f"*40)
            self.assertEqual(events.count("train"),10); self.assertEqual(events.count("replay"),10)
            self.assertLess(max(i for i,v in enumerate(events) if v=="train"),events.index("replay"))
            q,_=b.verify_artifacts(out,["x"]*41,"f"*40); self.assertEqual(p,q)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*41,output_dir=out,expected_head="f"*40)

    def test_23_byte_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*41,output_dir=out,expected_head="f"*40); path=out/"measurements.json"; path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*41,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name); a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*41,"f"*40)

    def test_24_bundle_and_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"m.pt"; bundle=dict(schema="fold-c315-single-mix-models-v1",identities=[list(x) for x in b.identities()],states=[{}]*10); torch.save(bundle,path)
            self.assertEqual(len(b.load_bundle(path)),10); bundle["identities"].reverse(); torch.save(bundle,path)
            with self.assertRaises(ValueError): b.load_bundle(path)
        with self.assertRaises(ValueError): b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))

    def test_25_semantic_suite_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["f."+str(i) for i in range(5085)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            self.assertEqual({t.id() for t in b.flatten(b.regression_suite(Path.cwd()))},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError): b.regression_suite(Path.cwd())

    def test_26_cli_modules_context(self):
        argv=["program","--summaries"]+[str(i) for i in range(41)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),41)
        c=NS(); p312=NS(context=lambda:(0,1,2,3,4,5,6,7,c)); p313=NS(context=lambda:(p312,1,2,3,4,c)); parent=NS(context=lambda:(p313,1,3,c),regression_modules=lambda _:["m"+str(i) for i in range(199)])
        package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c314_six_boundary_profile=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}): self.assertEqual(b.context(),(parent,p313,p312,1,3,2,5,4,c)); self.assertEqual(len(b.regression_modules(Path.cwd())),200)

    def test_27_utf8_and_seal_document(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for name in b.OWN: self.assertTrue((root/name).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="read_text": self.assertTrue(any(k.arg=="encoding" for k in n.keywords))

    def test_28_runner_indices_and_paths(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: compile(code,"embedded","exec")
        self.assertIn("sys.argv[2:43]",blocks[2]); self.assertIn("head = sys.argv[43]",blocks[2]); self.assertIn("len(sys.argv) == 44",blocks[2])
        self.assertEqual(re.findall(r'runs\\c(\d{3})-.*?\\summary.json',launcher),[str(i) for i in range(314,273,-1)])
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute")); self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_29_actual_parent_span_and_prefix(self):
        path=Path(__file__).resolve().parents[1]/"fold_lm/v05_benchmarks/model_c304_length_breadth.py"; tree=ast.parse(path.read_text(encoding="utf-8"))
        space=dict(torch=torch,require=b.require,SLOTS=64)
        exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ("span_mask","prefix_tensor")],type_ignores=[]),str(path),"exec"),space)
        for row in self.data["TRAIN"]:
            for v in b.VIEWS:
                text=b.render_one(row,v); x=space["prefix_tensor"](text)
                self.assertTrue(torch.equal(x,prefix(text))); self.assertTrue(torch.equal(space["span_mask"](x[None,:]),span(x[None,:])))

    def test_30_actual_parent_optimizer(self):
        path=Path(__file__).resolve().parents[1]/"fold_lm/v05_benchmarks/model_c308_core_learning_rate.py"; tree=ast.parse(path.read_text(encoding="utf-8"))
        space=dict(torch=torch,require=b.require,ARMS=("full_train","core_frozen","core_slow"),BASE_LR=.005,CORE_LR=.0005,
            manifest=lambda:dict(trainable_parameters=dict(full_train=14256,core_frozen=10928,core_slow=14256)))
        exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ("configure","parameter_groups","optimizer_for","verify_optimizer")],type_ignores=[]),str(path),"exec"),space)
        m=Toy(); space["configure"](m,"core_slow"); opt=space["optimizer_for"](m,"core_slow"); space["verify_optimizer"](opt,m,"core_slow")
        self.assertEqual([g["lr"] for g in opt.param_groups],[.005,.0005])
        opt.param_groups[1]["lr"]*=10
        with self.assertRaises(ValueError): space["verify_optimizer"](opt,m,"core_slow")

    def test_31_single_diagnostic_not_used_to_pass_six(self):
        p=payload(copy.deepcopy(self.summary)); p["gate_f_candidate"]=True
        with self.assertRaises(ValueError): b.validate_result(p)
        p=payload(copy.deepcopy(self.summary)); p["validation_summary"]["train_steps"]=False
        with self.assertRaises(ValueError): b.validate_result(p)
        self.assertTrue(all(r["capability_gate_applicable"] is False for r in self.summary["single_character_diagnostics"]))

    def test_32_count_and_direct_imports(self):
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),32)
        imports=[n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c314_six_boundary_profile"])


if __name__=="__main__": unittest.main()
