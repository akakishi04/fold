"""C316 software controls; synthetic fixtures are not FOLD scientific results."""
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
from fold_lm.v05_benchmarks import model_c316_single_mix_replication as b


def dataset():
    out={"TRAIN":[],"HOLDOUT":[]}
    for entities,values,language in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (values[1]-values[0])%4==2 else "TRAIN"
        for order,query in itertools.product((entities,entities[::-1]),entities):
            out[split].append(dict(id=f"{language}:{entities}:{values}:{order}:{query}",entities=list(entities),values=list(values),language=language,
                permutation=list(order),query=query,target=48+values[entities.index(query)]))
    return out


def prompts_for(data):
    def render(r,n,p,v):
        chars="abc" if r["language"]=="en" else "甲乙丙"; i,j=r["entities"]
        names={i:chars[i]*n,j:chars[j]*n if p=="repeat" else chars[i]*(n-1)+chars[j] if p=="shared_prefix" else chars[j]+chars[i]*(n-1)}
        return ";".join(names[e]+"="+("?" if v=="evidence_blind" else str(r["values"][r["entities"].index(e)])) for e in r["permutation"])+";"+("?" if v=="query_blind" else names[r["query"]])+"="
    return {str(n):{s:{p:[dict(source_id=r["id"],target=r["target"],views={v:render(r,n,p,v) for v in ("normal","evidence_blind","query_blind")}) for r in data[s]]
                      for p in (b.PROFILES[:1] if n==1 else b.PROFILES)} for s in b.SPLITS} for n in range(1,7)}


def prefix(text):
    raw=list(text.encode("utf-8")); b.require(len(raw)+2<=64,"overflow")
    return torch.tensor([257,*raw,258,*([256]*(62-len(raw)))],dtype=torch.int64)


def pair_inventory(rows,pairs):
    groups={}
    for i,r in enumerate(rows): groups.setdefault((r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"])),[]).append(i)
    pp=torch.tensor([sorted(groups[k],key=lambda i:rows[i]["query"]) for k in sorted(groups)])
    b.require(pp.shape==(96,2) and sorted(pp.flatten().tolist())==list(range(192)),"pair partition")
    return pp,[]


def legacy_plan(order,arm,rows,pairs):
    assert arm=="random_pairs"; pp,_=pair_inventory(rows,pairs); e=torch.empty((1200,24,4),dtype=torch.int64)
    for epoch in range(300):
        perm=torch.randperm(96,generator=torch.Generator().manual_seed(order+306000+epoch))
        for j in range(4): e[4*epoch+j,:,0]=epoch%3; e[4*epoch+j,:,1]=(epoch//3+epoch%3)%3; e[4*epoch+j,:,2:]=pp[perm[24*j:24*(j+1)]]
    return e


def parent_functions():
    path=Path(__file__).resolve().parents[1]/b.PARENT_SOURCE
    tree=ast.parse(path.read_text(encoding="utf-8"))
    names={"profiles","plan_for_order","schedule_stats","schedule","fit","evaluate","validate_raw","replay_error","replay"}
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==names
    env=dict(torch=torch,F=F,itertools=itertools,require=b.require,digest=b.digest,PROFILES=b.PROFILES,ARMS=b.ARMS,
        TRAIN_LENGTHS=b.LENGTHS,STEPS=1200,FIT_RNG=612000,SPLITS=b.SPLITS,VIEWS=("normal","evidence_blind","query_blind"),
        SEEDS=tuple(range(315001,315006)),ORDERS=tuple(range(315101,315106)))
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),"exec"),env)
    p=NS(**{n:env[n] for n in names},STEPS=1200,FIT_RNG=612000,ARMS=b.ARMS,TRAIN_LENGTHS=b.LENGTHS,PROFILES=b.PROFILES,
        MANIFEST_SHA=b.PARENT_MANIFEST,validate_seal=lambda:None,PINNED={})
    p.training_tables=lambda data,pr,w:({(n,k):torch.stack([w.prefix_tensor(r["views"]["normal"]) for r in pr[str(n)]["TRAIN"][k]])
        for n in range(1,5) for k in p.profiles(n)},torch.tensor([r["target"] for r in data["TRAIN"]]))
    p.validate_prompts=lambda *args:None
    return p


def check_logits(z,n):
    b.require(z.shape==(n,256) and z.dtype==torch.float64 and z.device.type=="cpu" and bool(torch.isfinite(z).all()),"logits")


def fingerprint(m):
    h=hashlib.sha256()
    for n,z in sorted(m.state_dict().items()): h.update(n.encode()); h.update(z.detach().contiguous().numpy().tobytes())
    return h.hexdigest()


class Core(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.linear=torch.nn.Linear(8,8,dtype=torch.float64); self.pad=torch.nn.Parameter(torch.zeros(3256,dtype=torch.float64)); self.config=NS(slots=64)
    def forward(self,x): return torch.tanh(self.linear(x))


class Toy(torch.nn.Module):
    def __init__(self,reference=None):
        super().__init__()
        if reference is not None:
            self.backbone=copy.deepcopy(reference.backbone); self.read=copy.deepcopy(reference.read); return
        self.backbone=torch.nn.Module(); self.backbone.embed=torch.nn.Embedding(4,8,dtype=torch.float64); self.backbone.core=Core(); self.backbone.config=NS(max_tokens=64)
        self.read=torch.nn.Linear(8,256,dtype=torch.float64)
        self.backbone.pad=torch.nn.Parameter(torch.zeros(14256-sum(p.numel() for p in self.parameters()),dtype=torch.float64))
    def forward(self,x,t):
        assert x.shape==(len(x),64) and t.shape==(len(x),) and not bool(t.any())
        h=self.backbone.embed(x[:,0]%4)
        for _ in range(4): h=self.backbone.core(h)
        return self.read(h)


@contextlib.contextmanager
def counted(model,core):
    calls=[0,0]; cores=[0]
    def hook(_,args,output): calls[0]+=1; calls[1]+=len(args[0])
    def ch(*_): cores[0]+=1
    a=model.register_forward_hook(hook); z=model.backbone.core.register_forward_hook(ch)
    try: yield calls,cores
    finally: a.remove(); z.remove()


def optimizer_policy():
    def groups(m,a):
        assert a=="core_slow"
        return [dict(params=[p for n,p in m.named_parameters() if not n.startswith("backbone.core.")],lr=.005),dict(params=list(m.backbone.core.parameters()),lr=.0005)]
    def optimizer(m,a): return torch.optim.AdamW(groups(m,a),betas=(.9,.999),eps=1e-8,weight_decay=0.)
    def verify(o,m,a):
        for g,w in zip(o.param_groups,groups(m,a),strict=True):
            b.require(g["lr"]==w["lr"] and [id(p) for p in g["params"]]==[id(p) for p in w["params"]],"optimizer mismatch")
    return NS(configure=lambda m,a:m.requires_grad_(True),parameter_groups=groups,optimizer_for=optimizer,verify_optimizer=verify,CORE_LR=.0005,BASE_LR=.005)


class Audit:
    @staticmethod
    def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).is_file() else "a"*64
    @staticmethod
    def read_json(p): return json.loads(Path(p).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n): return Path(root)/n
    @staticmethod
    def git(root,*a): return b"f"*40 if a[0]=="rev-parse" else b"feat/sft-target-loss" if a[0]=="branch" else b""


@contextlib.contextmanager
def no_neural():
    with torch.no_grad(),patch.object(torch.nn.Module,"_call_impl",side_effect=AssertionError("model forbidden")),patch.object(torch.nn.Module,"load_state_dict",side_effect=AssertionError("model load forbidden")):
        yield


def fixture_context():
    p=parent_functions(); policy=optimizer_policy()
    def new(seed):
        with torch.random.fork_rng(): torch.manual_seed(seed); return Toy()
    def score(data,raw,c):
        totals=[]
        for s in b.SPLITS:
            y=torch.tensor([r["target"] for r in data[s]])
            correct=sum(int((raw[s][k]["normal"].argmax(1)==y).sum()) for k in b.PROFILES)
            totals.append(dict(split=s,rows=3*len(y),correct=correct,full_pass=correct==3*len(y),direct_pass=correct==3*len(y)))
        return dict(passed=all(z["full_pass"] for z in totals),totals=totals)
    c=NS(base=NS(fingerprint=fingerprint),factory=NS(new_model=new,language_module=lambda:None),c278=NS(MeanFinalDualReadout=lambda m,*_:m),
        c269=NS(query_span_mask=None),reader=None,core=None,audit=Audit(),p267=NS(check_logits=check_logits,counted=counted,validate_data=lambda _:None))
    return NS(parent=p,p314=None,p313=None,p312=NS(pair_inventory=pair_inventory,plan_for_order=legacy_plan,context=lambda:()),
        guarded=NS(no_neural=no_neural),wide=NS(LengthReadout=Toy,prefix_tensor=prefix,score_length=score,PINNED={},context=lambda:()),policy=policy,pairs=None,
        diag=NS(normalize_task=lambda z,*_:z["totals"],partition=lambda z:{k:v for k,v in z[0].items() if k!="split"}),c=c)


def perfect_raw(data,p):
    zs={}
    for s in b.SPLITS:
        z=torch.zeros((len(data[s]),256),dtype=torch.float64); y=torch.tensor([r["target"] for r in data[s]]); z[torch.arange(len(y)),y]=5.; zs[s]=z
    return {str(n):{s:{k:{v:zs[s] for v in ("normal","evidence_blind","query_blind")} for k in p.profiles(n)} for s in b.SPLITS} for n in range(1,7)}


def records(data,x):
    rr=[]; raw=perfect_raw(data,x.parent)
    for seed,arm in b.identities():
        events=b.schedule(seed,arm,data,x)
        f=dict(steps=1200,training_rows=57600,fit_rng=612000,optimizer_creations=1,trainable_parameters=14256,ce_history=[.1]*1200,
            optimizer_group_lrs=[[.005,.0005]]*1200,gradient_parameter_counts=[1]*1200,gradient_union={"fixture":1},schedule_events=events,**x.parent.schedule_stats(events))
        rr.append(dict(seed=seed,arm=arm,initial_sha256=b.digest([seed]),core_initial_sha256=b.digest([seed,"core"]),final_sha256=b.digest([seed,arm]),core_final_sha256=b.digest([seed,arm,"core"]),
            fit=f,raw=raw,checkpoint_roundtrip=True,reload_max_error=0.,forward_calls=1344,row_presentations=71424,core_forward_calls=5376,replay_forward_calls=144,replay_row_presentations=13824,replay_core_forward_calls=576))
    return rr


def protection():
    pins={n:"a"*40 for n in b.OWN}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<742: pins["fixture/"+str(len(pins))]="a"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1393)}


def payload(s):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if s["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,gate_f_candidate=False,production_adoption=False)


class C316Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.det=torch.are_deterministic_algorithms_enabled(); torch.set_num_threads(2)
        cls.data=dataset(); cls.prompts=prompts_for(cls.data); cls.x=fixture_context()
        cls.tables,cls.y=cls.x.parent.training_tables(cls.data,cls.prompts,cls.x.wide)
        cls.fit_tables={k:torch.zeros_like(v) for k,v in cls.tables.items()}
        for v in cls.fit_tables.values(): v[:,0]=cls.y-48
        cls.records=records(cls.data,cls.x); cls.metrics,cls.summary=b.analyze(cls.records,cls.data,cls.x)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.det)

    def test_01_manifest_seal(self): b.validate_seal(); self.assertEqual(json.loads(b.blob(b.manifest())),b.manifest())
    def test_02_bad_seal(self):
        with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaises(ValueError): b.validate_seal()
    def test_03_canonical_inputs(self):
        self.assertEqual(b.digest(self.data),b.DATA_SHA); self.assertEqual(b.digest(self.prompts),b.PROMPTS_SHA)
    def test_04_no_old_seed_reuse(self):
        self.assertFalse(set(b.SEEDS)&set(range(315001,315006)))
        with self.assertRaises(ValueError): b.schedule(315001,b.ARMS[0],self.data,self.x)
        with self.assertRaises(ValueError): b.make_models(315001,self.x)
    def test_05_policy_drift(self):
        b.policy_check(self.x)
        with patch.object(self.x.policy,"CORE_LR",.001),self.assertRaises(ValueError): b.policy_check(self.x)
        with patch.object(self.x.parent,"FIT_RNG",1),self.assertRaises(ValueError): b.policy_check(self.x)
    def test_06_all_schedules_budget(self):
        for seed in b.SEEDS: b.check_plans(seed,self.data,self.x)
        e=b.schedule(b.SEEDS[0],b.ARMS[1],self.data,self.x)
        self.assertEqual(self.x.parent.schedule_stats(e)["length_profile_updates"],[[300,0,0],[100,100,100],[100,100,100],[100,100,100]])
    def test_07_schedule_rng_unchanged(self):
        torch.manual_seed(17); old=torch.get_rng_state(); b.schedule(b.SEEDS[0],b.ARMS[0],self.data,self.x); self.assertTrue(torch.equal(old,torch.get_rng_state()))
    def test_08_independent_candidate_schedule(self):
        got=b.schedule(b.SEEDS[0],b.ARMS[1],self.data,self.x); pp,_=pair_inventory(self.data["TRAIN"],None)
        for epoch in (0,1,4,100,299):
            perm=torch.randperm(96,generator=torch.Generator().manual_seed(b.ORDERS[0]+306000+epoch)); n=epoch%4+1; p=0 if n==1 else (epoch//4+n-2)%3
            for j in range(4): self.assertEqual(got[4*epoch+j,0,:2].tolist(),[n,p]); self.assertTrue(torch.equal(got[4*epoch+j,:,2:],pp[perm[24*j:24*(j+1)]]))
    def test_09_factory_identity_storage(self):
        models=b.make_models(b.SEEDS[0],self.x); self.assertEqual(len({fingerprint(m) for m in models.values()}),1)
        ptr=[p.data_ptr() for m in models.values() for p in m.parameters()]; self.assertEqual(len(ptr),len(set(ptr)))
        self.assertEqual({sum(p.numel() for p in m.parameters()) for m in models.values()},{14256})
    def test_10_actual_parent_loop_equivalence_both_arms(self):
        for arm in b.ARMS:
            torch.manual_seed(3); a=Toy(); z=copy.deepcopy(a)
            events=self.x.parent.plan_for_order(315101,arm,self.data["TRAIN"],self.x.p312,self.x.pairs)
            with contextlib.redirect_stdout(io.StringIO()):
                got=b.optimize(a,self.fit_tables,self.y,events,self.x)
                ref=self.x.parent.fit(z,self.data,self.fit_tables,self.y,315001,arm,self.x.p312,self.x.pairs,self.x.policy)
            for k in got:
                if isinstance(got[k],torch.Tensor): self.assertTrue(torch.equal(got[k],ref[k]))
                else: self.assertEqual(got[k],ref[k])
            self.assertEqual(fingerprint(a),fingerprint(z))
    def test_11_fit_checks(self):
        b.check_fit(self.records[0]["fit"],b.SEEDS[0],b.ARMS[0],self.data,self.x)
        for k in ("ce_history","optimizer_group_lrs","gradient_parameter_counts"):
            f=copy.deepcopy(self.records[0]["fit"]); f[k]=[]
            with self.assertRaises(ValueError): b.check_fit(f,b.SEEDS[0],b.ARMS[0],self.data,self.x)
    def test_12_train_and_parent_replay_accounting(self):
        torch.manual_seed(7); m=Toy()
        with contextlib.redirect_stdout(io.StringIO()): r,state=b.train_one(m,self.data,self.prompts,self.fit_tables,self.y,b.SEEDS[0],b.ARMS[0],self.x)
        self.x.parent.replay(Toy(),state,r,self.data,self.prompts,self.x.wide,self.x.c)
        self.assertEqual((r["forward_calls"],r["replay_forward_calls"],r["reload_max_error"]),(1344,144,0.))
        changed=copy.deepcopy(state); changed["read.bias"]+=1.
        with self.assertRaises(ValueError): self.x.parent.replay(Toy(),changed,r,self.data,self.prompts,self.x.wide,self.x.c)
    def test_13_training_boundary(self):
        self.assertEqual(set(n for n,p in self.tables),{1,2,3,4}); bad=dict(self.fit_tables); bad[5,"repeat"]=next(iter(bad.values()))
        with self.assertRaises(ValueError): b.train_one(Toy(),self.data,self.prompts,bad,self.y,b.SEEDS[0],b.ARMS[0],self.x)
    def test_14_gate_new_only(self):
        rr=copy.deepcopy(self.records); rr[1]["raw"]=perfect_raw(self.data,self.x.parent); rr[1]["raw"]["6"]=copy.deepcopy(rr[1]["raw"]["6"])
        rr[1]["raw"]["6"]["HOLDOUT"]["repeat"]["normal"][0,70]=9.
        _,s=b.analyze(rr,self.data,self.x); p=payload(s); b.validate_result(p); self.assertEqual(p["status"],"FAIL")
        p["status"]="PASS"
        with self.assertRaises(ValueError): b.validate_result(p)
    def test_15_inventory_single_not_tripled(self):
        self.assertEqual((len(self.summary["final_partitions"]),len(self.summary["single_character_diagnostics"])),(100,20))
        self.assertEqual({r["rows"] for r in self.summary["single_character_diagnostics"]},{192,96}); b.validate_result(payload(self.summary))
    def test_16_incomplete_cohort_and_initial_mismatch(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.data,self.x)
        rr=copy.deepcopy(self.records); rr[1]["initial_sha256"]="different"
        with self.assertRaises(ValueError): b.analyze(rr,self.data,self.x)
    def test_17_actual_runtime_preflight(self):
        with patch.object(b,"context",return_value=self.x),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,self.prompts)),contextlib.redirect_stdout(io.StringIO()): b.runtime_preflight(["x"]*42,Path.cwd())

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c316-fixture")/str(i)/"summary.json").resolve() for i in range(42)]
        p=dict(experiment_id="C315-v5b-single-character-mix",commit_sha=b.PARENT_EXECUTION,status="FAIL",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},artifacts=[dict(file=n) for n in b.OUTPUTS],
            validation_summary=dict(seed_results=b.expected_parent_results(),candidate_gate=False,all_pairs_matched=True,all_replays=True))
        parent=NS(context=lambda:(None,),parent_hashes=lambda _:tuple(str(i%10)*64 for i in range(41)),verify_artifacts=Mock(return_value=(p,[])),validate_result=Mock(),validate_prompts=Mock())
        hashes=dict(zip(map(str,paths),(b.PARENT_SHA,*parent.parent_hashes(None)),strict=True)); reads=[]
        def read(path): reads.append(path); return self.data if path.name=="dataset.json" else self.prompts
        x=NS(parent=parent,guarded=NS(no_neural=no_neural),p313=None,wide=None,c=NS(audit=NS(sha=lambda p:hashes[str(p)],read_json=read),p267=NS(validate_data=lambda _:None)))
        with patch.object(b,"context",return_value=x): yield paths,hashes,parent,p,reads

    def test_18_all42_hashes_before_verifier(self):
        with self.loader_fixture() as (paths,hashes,parent,p,reads):
            self.assertEqual(b.load_parent(paths)[0],p); parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            self.assertEqual([p.parent for p in reads],[paths[0].parent]*2)
            for path in paths:
                old=hashes[str(path)]; hashes[str(path)]="f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); hashes[str(path)]=old
    def test_19_parent_semantics_rejections(self):
        for fn in (lambda p:p.update(status="PASS"),lambda p:p["artifacts"].pop(),lambda p:p["validation_summary"]["seed_results"].reverse()):
            with self.loader_fixture() as (paths,_,_,p,_):
                fn(p)
                with self.assertRaises(ValueError): b.load_parent(paths)
    def test_20_actual_precheck_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pins={b.PARENT_SOURCE:b.PARENT_BLOB}
            while len(pins)<736: pins["accepted/"+str(len(pins))]="a"*40
            for n in list(pins)+list(b.OWN): p=root/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1379-len(inputs)):
                p=root/("input"+str(i)); p.write_text("data",encoding="utf-8"); inputs[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent"; directory.mkdir(); summary=directory/"summary.json"; summary.write_text("summary",encoding="utf-8"); arts=[]
            for n in b.OUTPUTS:
                p=directory/n; p.write_text("artifact",encoding="utf-8"); arts.append(dict(file=n,sha256=Audit.sha(p)))
            def sha(p): return b.PARENT_SHA if Path(p)==summary else Audit.sha(p)
            parent=types.ModuleType("parent"); parent.__file__=str(root/b.PARENT_SOURCE); parent.PINNED={}; parent.context=lambda:()
            c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,safe_child=Audit.safe_child,
                git=lambda root,*a:(pins.get(a[1][5:],"b"*40)+"\n").encode(),protect_tree_files=lambda root,pp:{str((root/n).resolve()):sha(root/n) for n in pp}))
            x=NS(parent=parent,p312=NS(context=lambda:()),wide=NS(context=lambda:(),PINNED={}),c=c)
            with patch.object(b,"context",return_value=x),patch.object(b,"policy_check"),patch.object(b,"load_parent",return_value=(dict(source_blobs=pins,input_sha256=inputs,artifacts=arts),None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*42,root))),(742,1393))
                c.missing=types.ModuleType("missing"); c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([summary]*42,root)

    @contextlib.contextmanager
    def run_fixture(self):
        x=fixture_context(); events=[]
        def pre(*_): events.append("precheck"); return protection()
        def train(*a): events.append("train"); return self.records[b.identities().index((a[5],a[6]))],{}
        x.parent.replay=lambda *a:events.append("replay")
        with patch.object(b,"context",return_value=x),patch.object(b,"precheck",side_effect=pre),patch.object(b,"load_parent",return_value=({},self.data,self.prompts)),patch.object(b,"make_models",return_value=dict.fromkeys(b.ARMS)),patch.object(b,"train_one",side_effect=train): yield events
    def test_21_production_order_loader_roundtrip(self):
        real=b.load_bundle
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,patch.object(b,"load_bundle",wraps=real) as loader,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*42,output_dir=out,expected_head="f"*40)
            self.assertEqual(events.count("train"),10); self.assertEqual(events.count("replay"),10); self.assertEqual(loader.call_count,1)
            self.assertLess(max(i for i,z in enumerate(events) if z=="train"),events.index("replay")); q,_=b.verify_artifacts(out,["x"]*42,"f"*40); self.assertEqual(p,q)
    def test_22_tampering_resealed_descriptor(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*42,output_dir=out,expected_head="f"*40); path=out/"measurements.json"; path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*42,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name); a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*42,"f"*40)
    def test_23_no_overwrite_and_wrong_head(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()),self.assertRaises(FileExistsError): b.run(summaries=["x"]*42,output_dir=tmp,expected_head="f"*40)
        with self.assertRaises(ValueError): b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))
    def test_24_bundle_schema_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"bundle.pt"; obj=dict(schema="fold-c316-single-replication-models-v1",identities=[list(x) for x in b.identities()],states=[{}]*10); torch.save(obj,p)
            self.assertEqual(len(b.load_bundle(p)),10); obj["identities"].reverse(); torch.save(obj,p)
            with self.assertRaises(ValueError): b.load_bundle(p)
    def test_25_semantic_suite_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["f."+str(i) for i in range(5117)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            self.assertEqual({t.id() for t in b.flatten(b.regression_suite(Path.cwd()))},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError): b.regression_suite(Path.cwd())
    def test_26_cli_context_module_dispatch(self):
        argv=["program","--summaries"]+[str(i) for i in range(42)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),42)
        parent=NS(context=lambda:tuple(range(9)),regression_modules=lambda _:["m"+str(i) for i in range(200)])
        package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c315_single_character_mix=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):
            x=b.context(); self.assertIs(x.parent,parent); self.assertEqual((x.p312,x.guarded,x.wide,x.policy,x.pairs,x.diag,x.c),(2,3,4,5,6,7,8)); self.assertEqual(len(b.regression_modules(Path.cwd())),201)
    def test_27_explicit_utf8_inventory(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding="utf-8"))
        for p in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="read_text": self.assertTrue(any(k.arg=="encoding" for k in n.keywords))
    def test_28_runner_cli_and_paths(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: compile(code,"embedded","exec")
        self.assertIn("sys.argv[2:44]",blocks[2]); self.assertIn("head = sys.argv[44]",blocks[2]); self.assertIn("len(sys.argv) == 45",blocks[2])
        self.assertEqual(re.findall(r'runs\\c(\d{3})-.*?\\summary.json',launcher),[str(n) for n in range(315,273,-1)])
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute")); self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))
    def test_29_evaluation_single_profile_counts(self):
        m=Toy(); m.eval(); m.requires_grad_(False)
        with counted(m,None) as (calls,cores): raw=self.x.parent.evaluate(m,self.prompts,self.data,self.x.wide,self.x.c)
        self.assertEqual(calls,[144,13824]); self.assertEqual(cores,[576]); self.assertEqual(set(raw["1"]["TRAIN"]),{"repeat"})
    def test_30_parent_negative_identity(self):
        rr=b.expected_parent_results(); self.assertEqual(sum(r["six_pass"] for r in rr if r["arm"]==b.ARMS[1]),4)
        self.assertEqual(sum(r["six_pass"] for r in rr if r["arm"]==b.ARMS[0]),3)
    def test_31_scope_and_invalid_work(self):
        for fn in (lambda p:p.update(gate_f_candidate=True),lambda p:p["validation_summary"].update(train_steps=False)):
            p=payload(copy.deepcopy(self.summary)); fn(p)
            with self.assertRaises(ValueError): b.validate_result(p)
        self.assertTrue(all(r["capability_gate_applicable"] is False for r in self.summary["single_character_diagnostics"]))
    def test_32_count_and_single_direct_import(self):
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),32)
        imports=[n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c315_single_character_mix"])


if __name__=="__main__": unittest.main()
