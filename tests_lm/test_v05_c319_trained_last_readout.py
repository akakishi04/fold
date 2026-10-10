"""C319 software controls;synthetic models and scores are not FOLD capability evidence."""
import ast
from collections import Counter
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
from fold_lm.v05_benchmarks import model_c319_trained_last_readout as b

VIEWS=("normal","evidence_blind","query_blind")
def profiles(n): return b.PROFILES[:1] if n==1 else b.PROFILES


def dataset():
    out={s:[] for s in b.SPLITS}
    for ent,val,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (val[1]-val[0])%4==2 else "TRAIN"
        for order,q in itertools.product((ent,ent[::-1]),ent):
            out[split].append(dict(id=f"{lang}:{ent}:{val}:{order}:{q}",entities=list(ent),values=list(val),language=lang,permutation=list(order),query=q,target=48+val[ent.index(q)]))
    return out


def prompts_for(data):
    def render(r,n,p,v):
        chars="abc" if r["language"]=="en" else "甲乙丙"; i,j=r["entities"]
        names={i:chars[i]*n,j:chars[j]*n if p==b.PROFILES[0] else chars[i]*(n-1)+chars[j] if p==b.PROFILES[1] else chars[j]+chars[i]*(n-1)}
        return ";".join(names[k]+"="+("?" if v=="evidence_blind" else str(r["values"][r["entities"].index(k)])) for k in r["permutation"])+";"+("?" if v=="query_blind" else names[r["query"]])+"="
    return {str(n):{s:{p:[dict(source_id=r["id"],target=r["target"],views={v:render(r,n,p,v) for v in VIEWS}) for r in data[s]] for p in profiles(n)} for s in b.SPLITS} for n in range(1,7)}


def prefix(text):
    raw=list(text.encode("utf-8")); b.require(len(raw)+2<=64,"overflow")
    return torch.tensor([257,*raw,258,*([256]*(62-len(raw)))],dtype=torch.int64)


def pairs(rows,unused):
    groups={}
    for i,r in enumerate(rows): groups.setdefault((r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"])),[]).append(i)
    pp=torch.tensor([sorted(groups[k],key=lambda i:rows[i]["query"]) for k in sorted(groups)],dtype=torch.int64)
    assert pp.shape==(96,2) and sorted(pp.flatten().tolist())==list(range(192))
    return pp,[]


def accepted_functions():
    root=Path(__file__).resolve().parents[1]
    tree=ast.parse((root/b.WIDE_SOURCE).read_text(encoding="utf-8"))
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="LengthReadout")
    forward=copy.deepcopy(next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=="forward"))
    span=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="span_mask")
    env=dict(torch=torch,require=b.require,SLOTS=64,Counter=Counter)
    exec(compile(ast.Module(body=[span,forward],type_ignores=[]),"accepted_C304","exec"),env)
    tree=ast.parse((root/"fold_lm/v05_benchmarks/model_c315_single_character_mix.py").read_text(encoding="utf-8"))
    names={"training_tables","plan_for_order","schedule","schedule_stats","fit","evaluate","validate_raw","replay_error","replay"}
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]; assert {n.name for n in nodes}==names
    env2=dict(torch=torch,F=F,math=__import__("math"),require=b.require,digest=b.digest,DATA_SHA=b.DATA_SHA,itertools=itertools,
        SPLITS=b.SPLITS,VIEWS=VIEWS,profiles=profiles,PROFILES=b.PROFILES,ARMS=("two_to_four","one_to_four"),
        TRAIN_LENGTHS={"two_to_four":(2,3,4),"one_to_four":(1,2,3,4)},STEPS=1200,FIT_RNG=b.FIT_RNG,
        SEEDS=tuple(range(315001,315006)),ORDERS=tuple(range(315101,315106)))
    exec(compile(ast.Module(body=nodes,type_ignores=[]),"accepted_C315","exec"),env2)
    return env["forward"],env["span_mask"],NS(**{n:env2[n] for n in names},profiles=profiles,STEPS=1200,FIT_RNG=b.FIT_RNG,context=lambda:())


def fingerprint(model):
    h=hashlib.sha256()
    for n,z in sorted(model.state_dict().items()): h.update(n.encode()); h.update(z.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def check_logits(z,n):
    b.require(z.shape==(n,256) and z.dtype==torch.float64 and z.device.type=="cpu" and bool(torch.isfinite(z).all()),"logits")


class Encoder(torch.nn.Module):
    def __init__(self): super().__init__(); self.embed=torch.nn.Embedding(259,16,dtype=torch.float64)
    def forward(self,tokens): return (self.embed(tokens),)
class Core(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.linear=torch.nn.Linear(16,16,dtype=torch.float64)
        self.pad=torch.nn.Parameter(torch.zeros(3056,dtype=torch.float64)); self.config=NS(slots=64)
    def forward(self,state,local,route_index): return torch.tanh(self.linear(state)+local*.1)
class Backbone(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.local_encoder=Encoder(); self.core=Core(); self.readout_norm=torch.nn.LayerNorm(16,dtype=torch.float64)
        self.classifier=torch.nn.Linear(16,256,dtype=torch.float64)
        self.config=NS(max_tokens=64,width=16,next_route=0,instruction_route=1,internal_steps=2)
    def forward(self,tokens,tasks):
        valid=tokens!=256; local=self.local_encoder(tokens)[0]*valid[:,:,None]; state=local
        for _ in range(2): state=self.core(state,local,route_index=0); self.core(state,local,route_index=1)
        return self.classifier(self.readout_norm(state[torch.arange(len(tokens)),valid.sum(1)-1]))
class Toy(torch.nn.Module):
    forward_impl=None
    def __init__(self,reference=None):
        super().__init__()
        if reference is not None:
            self.backbone=copy.deepcopy(reference.backbone); self.read=copy.deepcopy(reference.read)
        else:
            self.backbone=Backbone(); self.read=torch.nn.Module()
            for n in ("key","query","output"): setattr(self.read,n,torch.nn.Linear(16,16,bias=False,dtype=torch.float64))
            self.backbone.pad=torch.nn.Parameter(torch.zeros(14256-sum(p.numel() for p in self.parameters()),dtype=torch.float64))
        self.forward=types.MethodType(type(self).forward_impl,self)


class LoopToy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.backbone=torch.nn.Module(); self.backbone.core=torch.nn.Linear(4,4,dtype=torch.float64)
        self.out=torch.nn.Linear(4,256,dtype=torch.float64)
    def forward(self,tokens,tasks):
        x=F.one_hot(tokens[:,0]%4,4).to(torch.float64); return self.out(torch.tanh(self.backbone.core(x)))


@contextlib.contextmanager
def counted(model,core):
    calls=[0,0]; cores=[0]
    def mh(_,args,out): calls[0]+=1; calls[1]+=len(args[0])
    def ch(*_): cores[0]+=1
    h=model.register_forward_hook(mh); k=model.backbone.core.register_forward_hook(ch)
    try: yield calls,cores
    finally: h.remove(); k.remove()


def optimizer_policy():
    def groups(m,arm):
        assert arm=="core_slow"
        return [dict(params=[p for n,p in m.named_parameters() if not n.startswith("backbone.core.")],lr=.005),dict(params=list(m.backbone.core.parameters()),lr=.0005)]
    def opt(m,arm): return torch.optim.AdamW(groups(m,arm),betas=(.9,.999),eps=1e-8,weight_decay=0.)
    def verify(o,m,arm):
        for g,w in zip(o.param_groups,groups(m,arm),strict=True):
            b.require(g["lr"]==w["lr"] and [id(p) for p in g["params"]]==[id(p) for p in w["params"]],"optimizer contract")
    return NS(configure=lambda m,a:m.requires_grad_(True),parameter_groups=groups,optimizer_for=opt,verify_optimizer=verify,CORE_LR=.0005,BASE_LR=.005)


class Audit:
    @staticmethod
    def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest() if Path(path).is_file() else "a"*64
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name): return Path(root)/name
    @staticmethod
    def git(root,*args): return b"f"*40 if args[0]=="rev-parse" else b"feat/sft-target-loss" if args[0]=="branch" else b""


@contextlib.contextmanager
def no_neural():
    with torch.no_grad(),patch.object(torch.nn.Module,"_call_impl",side_effect=AssertionError("model forbidden")),patch.object(torch.nn.Module,"load_state_dict",side_effect=AssertionError("state load forbidden")): yield


def fixture_context():
    forward,span,p315=accepted_functions(); Toy.forward_impl=forward
    def new(seed):
        with torch.random.fork_rng(): torch.manual_seed(seed); return Toy()
    def score(data,raw,c):
        rows=[]
        for s in b.SPLITS:
            y=torch.tensor([r["target"] for r in data[s]]); correct=sum(int((raw[s][p]["normal"].argmax(1)==y).sum()) for p in b.PROFILES)
            rows.append(dict(split=s,rows=len(y)*3,correct=correct,full_pass=correct==len(y)*3,direct_pass=correct==len(y)*3))
        return dict(passed=all(z["full_pass"] for z in rows),totals=rows)
    c=NS(audit=Audit(),base=NS(fingerprint=fingerprint),p267=NS(check_logits=check_logits,counted=counted),core=None,
        factory=NS(new_model=new,language_module=lambda:None),c278=NS(MeanFinalDualReadout=lambda m,*a:m),c269=NS(query_span_mask=None),reader=None)
    return NS(parent=p315,p312=NS(pair_inventory=pairs,context=lambda:()),pairs=None,wide=NS(LengthReadout=Toy,span_mask=span,prefix_tensor=prefix,score_length=score,context=lambda:()),
        policy=optimizer_policy(),guarded=NS(no_neural=no_neural),diag=NS(normalize_task=lambda z,*a:z["totals"],partition=lambda z:{k:v for k,v in z[0].items() if k!="split"}),c=c)


def reference_last(model,tokens,tasks,span_fn):
    valid=tokens!=256; local=model.backbone.local_encoder(tokens)[0]*valid[:,:,None]; state=local
    for _ in range(2): state=model.backbone.core(state,local,route_index=0)
    span=span_fn(tokens); rows=torch.arange(len(tokens)); last=torch.where(span,torch.arange(64),-1).max(1).values
    q=model.read.query(local[rows,last]); k=model.read.key(local)
    weights=((k*q[:,None,:]).sum(-1)/4.).masked_fill(~valid,float("-inf")).softmax(-1)
    memory=(weights[:,:,None]*local).sum(1)
    return model.backbone.classifier(model.backbone.readout_norm(state[rows,valid.sum(1)-1]+model.read.output(memory)))


def perfect_raw(data):
    by_split={}
    for s in b.SPLITS:
        z=torch.zeros((len(data[s]),256),dtype=torch.float64); y=torch.tensor([r["target"] for r in data[s]])
        z[torch.arange(len(y)),y]=5.; by_split[s]=z
    return {str(n):{s:{p:{v:by_split[s] for v in VIEWS} for p in profiles(n)} for s in b.SPLITS} for n in range(1,7)}


def fixtures(data,x):
    records=[]; raw=perfect_raw(data)
    for seed,arm in b.identities():
        events=b.schedule(seed,data,x)
        fit=dict(steps=1200,training_rows=57600,fit_rng=b.FIT_RNG,optimizer_creations=1,trainable_parameters=14256,
            ce_history=[.1]*1200,optimizer_group_lrs=[[.005,.0005]]*1200,gradient_parameter_counts=[1]*1200,
            gradient_union={"fixture":1},schedule_events=events,**x.parent.schedule_stats(events))
        records.append(dict(seed=seed,arm=arm,readout_policy=arm,initial_sha256=b.digest([seed]),core_initial_sha256=b.digest([seed,"core"]),
            final_sha256=b.digest([seed,arm]),core_final_sha256=b.digest([seed,arm,"core"]),fit=fit,raw=raw,
            policy_receipt=dict(calls=1344,query_calls=2688,rows=71424,grad_calls=1200),replay_policy_receipt=dict(calls=144,query_calls=288,rows=13824,grad_calls=0),
            checkpoint_roundtrip=True,reload_max_error=0.,forward_calls=1344,row_presentations=71424,core_forward_calls=5376,
            replay_forward_calls=144,replay_row_presentations=13824,replay_core_forward_calls=576))
    return records


def protection():
    pins={n:"a"*40 for n in b.OWN}; pins.update({b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB})
    while len(pins)<760: pins["fixture/"+str(len(pins))]="a"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1429)}


def payload(summary):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if summary["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary,gate_f_candidate=False,production_adoption=False)


class C319Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.det=torch.are_deterministic_algorithms_enabled(); cls.rng=torch.get_rng_state(); torch.set_num_threads(2)
        cls.data=dataset(); cls.prompts=prompts_for(cls.data); cls.x=fixture_context()
        cls.full_tables,cls.y=cls.x.parent.training_tables(cls.data,cls.prompts,cls.x.wide)
        cls.tables={k:v for k,v in cls.full_tables.items() if k[0]>=2}; cls.records=fixtures(cls.data,cls.x)
        cls.metrics,cls.summary=b.analyze(cls.records,cls.data,cls.x)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.det); torch.set_rng_state(cls.rng)
    def toy(self):
        torch.manual_seed(13); return Toy()
    def inp(self,texts=("aaaa=0;baaa=1;baaa=","甲甲甲甲=0;乙甲甲甲=1;乙甲甲甲=")):
        return torch.stack([prefix(v) for v in texts]),torch.zeros(len(texts),dtype=torch.int64)
    def test_01_seal(self):
        b.validate_seal()
        with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaises(ValueError): b.validate_seal()
    def test_02_inputs(self):
        self.assertEqual(b.digest(self.data),b.DATA_SHA); self.assertEqual(b.digest(self.prompts),b.PROMPTS_SHA)
        self.assertEqual({n for n,p in self.tables},{2,3,4}); self.assertEqual(set(self.prompts["1"]["TRAIN"]),{"repeat"})
    def test_03_initial_state_independence(self):
        models=b.make_models(b.SEEDS[0],self.x); self.assertEqual(len({fingerprint(m) for m in models.values()}),1)
        addresses=[p.data_ptr() for m in models.values() for p in m.parameters()]; self.assertEqual(len(addresses),len(set(addresses)))
        self.assertEqual({sum(p.numel() for p in m.parameters()) for m in models.values()},{14256})
        with self.assertRaises(ValueError): b.make_models(316001,self.x)
    def test_04_schedule_all_seeds(self):
        for seed in b.SEEDS:
            torch.manual_seed(2); state=torch.get_rng_state(); events=b.schedule(seed,self.data,self.x)
            self.assertTrue(torch.equal(state,torch.get_rng_state()))
            self.assertEqual(self.x.parent.schedule_stats(events)["per_length_row_exposures"],[[n]*192 for n in (0,100,100,100)])
        with self.assertRaises(ValueError): b.schedule(316001,self.data,self.x)
    def test_05_native_control_outputs_and_gradients(self):
        a=self.toy(); z=copy.deepcopy(a); args=self.inp(); y=torch.tensor([48,49])
        original=a(*args); F.cross_entropy(original,y).backward()
        with b.trained_readout(z,self.x.wide,"mean_last") as stats: actual=z(*args)
        F.cross_entropy(actual,y).backward(); self.assertTrue(torch.equal(original,actual)); self.assertEqual(stats["grad_calls"],1)
        for (n,p),(m,q) in zip(a.named_parameters(),z.named_parameters(),strict=True):
            self.assertEqual(n,m); self.assertEqual(p.grad is None,q.grad is None)
            if p.grad is not None: self.assertTrue(torch.equal(p.grad,q.grad))
    def test_06_last_output_and_autograd_oracle(self):
        a=self.toy(); z=copy.deepcopy(a); tokens,tasks=self.inp(); y=torch.tensor([48,49])
        expected=reference_last(a,tokens,tasks,self.x.wide.span_mask); F.cross_entropy(expected,y).backward()
        with b.trained_readout(z,self.x.wide,"last_only"): actual=z(tokens,tasks)
        F.cross_entropy(actual,y).backward(); self.assertTrue(torch.allclose(expected,actual,atol=1e-13,rtol=0))
        for (n,p),(m,q) in zip(a.named_parameters(),z.named_parameters(),strict=True):
            self.assertEqual(p.grad is None,q.grad is None,n)
            if p.grad is not None: self.assertTrue(torch.allclose(p.grad,q.grad,atol=1e-12,rtol=0),n)
        self.assertGreater(float(z.backbone.local_encoder.embed.weight.grad.abs().sum()),0.)
        self.assertGreater(float(z.read.query.weight.grad.abs().sum()),0.)
    def test_07_one_byte_controls(self):
        m=self.toy(); args=self.inp(("a=0;b=1;a=","甲甲=0;乙甲=1;?="))
        with torch.no_grad():
            native=m(*args)
            with b.trained_readout(m,self.x.wide,"last_only"): changed=m(*args)
        self.assertTrue(torch.equal(native,changed))
    def test_08_repeated_training_steps_no_retained_graph(self):
        m=self.toy(); before=b.hook_snapshot(m); opt=self.x.policy.optimizer_for(m,"core_slow")
        with b.trained_readout(m,self.x.wide,"last_only") as stats:
            for _ in range(3):
                opt.zero_grad(set_to_none=True); z=m(*self.inp()); F.cross_entropy(z,torch.tensor([48,49])).backward(); opt.step()
        self.assertEqual(stats["grad_calls"],3); self.assertEqual(before,b.hook_snapshot(m))
    def test_09_provenance_detach_exception_cleanup(self):
        m=self.toy(); h=m.read.query.register_forward_pre_hook(lambda _,a:(a[0]+1,)); hooks=b.hook_snapshot(m)
        with self.assertRaisesRegex(ValueError,"provenance"),b.trained_readout(m,self.x.wide,"last_only"): m(*self.inp())
        self.assertEqual(hooks,b.hook_snapshot(m)); h.remove()
        h=m.backbone.local_encoder.register_forward_hook(lambda _,a,out:(out[0].detach(),))
        with self.assertRaisesRegex(ValueError,"detached"),b.trained_readout(m,self.x.wide,"last_only"): m(*self.inp())
        h.remove(); before=b.hook_snapshot(m)
        with patch.object(m.read.output,"forward",side_effect=RuntimeError("test")),self.assertRaises(RuntimeError),b.trained_readout(m,self.x.wide,"mean_last"): m(*self.inp())
        self.assertEqual(before,b.hook_snapshot(m))
    def test_10_full_control_optimization_loop_matches_parent(self):
        torch.manual_seed(3); a=LoopToy(); z=copy.deepcopy(a)
        events=self.x.parent.plan_for_order(315101,"two_to_four",self.data["TRAIN"],self.x.p312,self.x.pairs)
        with contextlib.redirect_stdout(io.StringIO()):
            actual=b.optimize(a,self.tables,self.y,events,self.x,"reference")
            expected=self.x.parent.fit(z,self.data,self.full_tables,self.y,315001,"two_to_four",self.x.p312,self.x.pairs,self.x.policy)
        for key in expected:
            if isinstance(expected[key],torch.Tensor): self.assertTrue(torch.equal(actual[key],expected[key]),key)
            else: self.assertEqual(actual[key],expected[key],key)
        self.assertEqual(fingerprint(a),fingerprint(z))
    def test_11_full_candidate_train_and_policy_replay(self):
        m=self.toy()
        with contextlib.redirect_stdout(io.StringIO()):
            record,state=b.train_one(m,self.data,self.prompts,self.tables,self.y,b.SEEDS[0],"last_only",self.x)
            b.replay(self.toy(),state,record,self.data,self.prompts,self.x)
        self.assertEqual(record["reload_max_error"],0.); self.assertEqual(record["policy_receipt"]["grad_calls"],1200)
        wrong=copy.deepcopy(state); wrong["read.output.weight"]+=1.
        with self.assertRaises(ValueError): b.replay(self.toy(),wrong,record,self.data,self.prompts,self.x)
        bad=copy.deepcopy(record); bad["arm"]="mean_last"
        with self.assertRaises(ValueError): b.replay(self.toy(),state,bad,self.data,self.prompts,self.x)
    def test_12_analysis_inventory_and_primary(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["single_character_diagnostics"])),(10,100,20))
        b.validate_result(payload(self.summary))
        rr=copy.deepcopy(self.records); rr[1]["raw"]=perfect_raw(self.data); rr[1]["raw"]["6"]=copy.deepcopy(rr[1]["raw"]["6"])
        rr[1]["raw"]["6"]["HOLDOUT"]["repeat"]["normal"][0,70]=9.
        _,s=b.analyze(rr,self.data,self.x); p=payload(s); b.validate_result(p); self.assertEqual(p["status"],"FAIL")
        self.assertEqual(s["length_pass_counts"]["6"]["mean_last"],5)
    def test_13_policy_pairing_and_fit_tamper(self):
        for fn in (lambda r:r.update(readout_policy="wrong"),lambda r:r["policy_receipt"].update(grad_calls=0),lambda r:r["replay_policy_receipt"].update(calls=1),lambda r:r["fit"].update(ce_history=[])):
            rr=copy.deepcopy(self.records); fn(rr[1])
            with self.assertRaises(ValueError): b.analyze(rr,self.data,self.x)
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.data,self.x)
    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c319-fixture")/str(i)/"summary.json").resolve() for i in range(45)]
        hashes=dict(zip(map(str,paths),(b.PARENT_SHA,*[str(i%10)*64 for i in range(44)]),strict=True))
        evidence=dict(experiment_id="C318-v5b-frozen-readout-branches",commit_sha=b.PARENT_EXECUTION,status="PASS",capability_gate_applicable=False,
            artifacts=[dict(file=n) for n in ("audit-plan.json","evaluations.pt","measurements.json","validation-summary.json")],validation_summary=dict(length_pass_counts=b.parent_counts()))
        tail=tuple(list(hashes.values())[1:])
        parent=NS(OUTPUTS=tuple(a["file"] for a in evidence["artifacts"]),parent_hashes=lambda *a:tail,
            verify_artifacts=Mock(return_value=(evidence,[])),validate_result=Mock(),load_parent=Mock(return_value=({},self.data,self.prompts,[])))
        x=NS(guarded=NS(no_neural=no_neural),c=NS(audit=NS(sha=lambda p:hashes[str(p)])))
        with patch.object(b,"context",return_value=(parent,None,None,x)): yield paths,hashes,parent,evidence
    def test_14_all45_hash_guards(self):
        with self.loader_fixture() as (paths,hashes,parent,evidence):
            self.assertEqual(b.load_parent(paths)[0],evidence)
            parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION); parent.load_parent.assert_called_once_with(paths[1:])
            for path in paths:
                old=hashes[str(path)]; hashes[str(path)]="f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); hashes[str(path)]=old
    def test_15_parent_semantics(self):
        for fn in (lambda p:p.update(status="FAIL"),lambda p:p.update(capability_gate_applicable=True),lambda p:p["artifacts"].pop()):
            with self.loader_fixture() as (paths,_,_,e):
                fn(e)
                with self.assertRaises(ValueError): b.load_parent(paths)
    def test_16_precheck_source_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pins={b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB}
            while len(pins)<754: pins["accepted/"+str(len(pins))]="a"*40
            for n in list(pins)+list(b.OWN): p=root/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1418-len(inputs)):
                p=root/("input"+str(i)); p.write_text("data",encoding="utf-8"); inputs[str(p.resolve())]=Audit.sha(p)
            folder=root/"parent"; folder.mkdir(); summary=folder/"summary.json"; summary.write_text("summary",encoding="utf-8"); artifacts=[]
            for n in ("audit-plan.json","evaluations.pt","measurements.json","validation-summary.json"):
                p=folder/n; p.write_text("data",encoding="utf-8"); artifacts.append(dict(file=n,sha256=Audit.sha(p)))
            def sha(p): return b.PARENT_SHA if Path(p)==summary else Audit.sha(p)
            parent=types.ModuleType("parent"); parent.__file__=str(root/b.PARENT_SOURCE)
            x=NS(parent=NS(context=lambda:(),STEPS=1200,FIT_RNG=b.FIT_RNG),policy=NS(CORE_LR=.0005,BASE_LR=.005),p312=NS(context=lambda:()),wide=NS(context=lambda:()),
                c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,safe_child=Audit.safe_child,git=lambda root,*a:(pins.get(a[1][5:],"b"*40)+"\n").encode(),protect_tree_files=lambda root,pp:{str((root/n).resolve()):sha(root/n) for n in pp})))
            with patch.object(b,"context",return_value=(parent,None,None,x)),patch.object(b,"load_parent",return_value=(dict(source_blobs=pins,input_sha256=inputs,artifacts=artifacts),None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*45,root))),(760,1429))
                x.c.missing=types.ModuleType("missing"); x.c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([summary]*45,root)
    def test_17_runtime_preflight_independent_reference(self):
        @contextlib.contextmanager
        def probe(model,wide,mode):
            native=model.forward
            if mode=="last_only": model.forward=types.MethodType(lambda m,t,k:reference_last(m,t,k,wide.span_mask),model)
            try: yield
            finally: model.forward=native
        parent=NS(branch_probe=probe)
        with patch.object(b,"precheck",return_value=protection()),patch.object(b,"context",return_value=(parent,None,None,self.x)),patch.object(b,"load_parent",return_value=({},self.data,self.prompts)),contextlib.redirect_stdout(io.StringIO()):
            b.runtime_preflight(["x"]*45,Path.cwd())
    @contextlib.contextmanager
    def run_fixture(self):
        events=[]
        def guard(*a): events.append("guard")
        def train(*a): events.append("train"); return copy.deepcopy(self.records[b.identities().index((a[5],a[6]))]),{}
        def replay(*a): events.append("replay")
        with patch.object(b,"context",return_value=(None,NS(guard=guard),None,self.x)),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,self.prompts)),patch.object(b,"make_models",return_value=dict.fromkeys(b.ARMS)),patch.object(b,"train_one",side_effect=train),patch.object(b,"replay",side_effect=replay): yield events
    def test_18_run_persistence_loader_order(self):
        real=b.load_bundle
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,patch.object(b,"load_bundle",wraps=real) as load,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*45,output_dir=out,expected_head="f"*40)
            self.assertEqual((events.count("train"),events.count("replay"),load.call_count),(10,10,1))
            self.assertLess(max(i for i,v in enumerate(events) if v=="train"),events.index("replay"))
            q,_=b.verify_artifacts(out,["x"]*45,"f"*40); self.assertEqual(p,q)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*45,output_dir=out,expected_head="f"*40)
    def test_19_artifact_tamper_and_resealed_metadata(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*45,output_dir=out,expected_head="f"*40)
            file=out/"measurements.json"; file.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*45,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==file.name); a.update(sha256=Audit.sha(file),serialized_bytes=file.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*45,"f"*40)
    def test_20_suite_semantic_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["f."+str(i) for i in range(5197)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            self.assertEqual({t.id() for t in b.flatten(b.regression_suite(Path.cwd()))},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError): b.regression_suite(Path.cwd())
    def test_21_cli_context_dispatch(self):
        argv=["program","--summaries"]+[str(i) for i in range(45)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),45)
        parent=NS(context=lambda:("p317","p316","x"),regression_modules=lambda root:["m"+str(i) for i in range(203)])
        package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c318_readout_branch_isolation=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}): self.assertEqual(b.context(),(parent,"p317","p316","x")); self.assertEqual(len(b.regression_modules(Path.cwd())),204)
    def test_22_utf8_and_sealed_docs(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="read_text": self.assertTrue(any(k.arg=="encoding" for k in n.keywords))
    def test_23_runner_indices_and_paths(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: compile(code,"embedded","exec")
        self.assertIn("sys.argv[2:47]",blocks[2]); self.assertIn("head = sys.argv[47]",blocks[2]); self.assertIn("len(sys.argv) == 48",blocks[2])
        self.assertEqual(re.findall(r'runs\\c(\d{3})-.*?\\summary.json',launcher),[str(n) for n in range(318,273,-1)])
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute")); self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))
    def test_24_scope_loader_and_training_boundary(self):
        for fn in (lambda p:p.update(gate_f_candidate=True),lambda p:p["validation_summary"].update(train_steps=False)):
            p=payload(copy.deepcopy(self.summary)); fn(p)
            with self.assertRaises(ValueError): b.validate_result(p)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"state.pt"; obj=dict(schema="fold-c319-trained-readout-models-v1",identities=[list(v) for v in b.identities()],states=[{}]*10)
            torch.save(obj,path); self.assertEqual(len(b.load_bundle(path)),10); obj["identities"].reverse(); torch.save(obj,path)
            with self.assertRaises(ValueError): b.load_bundle(path)
        bad=dict(self.tables); bad[6,"repeat"]=next(iter(bad.values()))
        with self.assertRaises(ValueError): b.optimize(LoopToy(),bad,self.y,b.schedule(b.SEEDS[0],self.data,self.x),self.x,"invalid")
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),24)
        imports=[n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c318_readout_branch_isolation"])


if __name__=="__main__": unittest.main()
