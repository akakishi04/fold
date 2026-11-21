"""C317 software controls. Toy representations are not actual FOLD capability evidence."""
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
from fold_lm.v05_benchmarks import model_c317_query_endpoint_probe as b

PROFILES=("repeat","shared_prefix","shared_suffix")
def profiles(n): return PROFILES[:1] if n==1 else PROFILES


def dataset():
    out={"TRAIN":[],"HOLDOUT":[]}
    for ent,val,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (val[1]-val[0])%4==2 else "TRAIN"
        for order,q in itertools.product((ent,ent[::-1]),ent):
            out[split].append(dict(id=f"{lang}:{ent}:{val}:{order}:{q}",entities=list(ent),values=list(val),language=lang,permutation=list(order),query=q,target=48+val[ent.index(q)]))
    return out


def prompts_for(data):
    def render(r,n,p,v):
        chars="abc" if r["language"]=="en" else "甲乙丙";i,j=r["entities"]
        names={i:chars[i]*n,j:chars[j]*n if p==PROFILES[0] else chars[i]*(n-1)+chars[j] if p==PROFILES[1] else chars[j]+chars[i]*(n-1)}
        return ";".join(names[k]+"="+("?" if v=="evidence_blind" else str(r["values"][r["entities"].index(k)])) for k in r["permutation"])+";"+("?" if v=="query_blind" else names[r["query"]])+"="
    return {str(n):{s:{p:[dict(source_id=r["id"],target=r["target"],views={v:render(r,n,p,v) for v in b.VIEWS}) for r in data[s]] for p in profiles(n)} for s in b.SPLITS} for n in range(1,7)}


def prefix(text):
    raw=list(text.encode("utf-8")); b.require(len(raw)+2<=64,"overflow")
    return torch.tensor([257,*raw,258,*([256]*(62-len(raw)))],dtype=torch.int64)


def span(tokens):
    out=torch.zeros_like(tokens,dtype=torch.bool)
    for i,row in enumerate(tokens.tolist()):
        stop=row.index(258)-1; start=max(j for j,c in enumerate(row[:stop]) if c==59)+1; out[i,start:stop]=True
    return out


def check_logits(z,n):
    b.require(z.shape==(n,256) and z.dtype==torch.float64 and z.device.type=="cpu" and bool(torch.isfinite(z).all()),"logits")


def accepted_functions():
    root=Path(__file__).resolve().parents[1]
    tree=ast.parse((root/"fold_lm/v05_benchmarks/model_c315_single_character_mix.py").read_text(encoding="utf-8"))
    names={"evaluate","validate_raw","replay_error"}; nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==names
    env=dict(torch=torch,require=b.require,itertools=itertools,SPLITS=b.SPLITS,VIEWS=b.VIEWS,profiles=profiles)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),"accepted_C315_functions","exec"),env)
    parent=NS(**{n:env[n] for n in names},profiles=profiles,PINNED={},context=lambda:(),validate_prompts=lambda *a:None)
    tree=ast.parse((root/b.WIDE_SOURCE).read_text(encoding="utf-8"))
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="LengthReadout")
    forward=copy.deepcopy(next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=="forward"))
    forward.name="accepted_forward"
    sn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="span_mask")
    env=dict(torch=torch,require=b.require,SLOTS=64,Counter=Counter)
    exec(compile(ast.Module(body=[sn,forward],type_ignores=[]),"accepted_C304_functions","exec"),env)
    return parent,env["accepted_forward"],env["span_mask"]


def fingerprint(m):
    h=hashlib.sha256()
    for n,z in sorted(m.state_dict().items()): h.update(n.encode()); h.update(z.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


class Encoder(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.embed=torch.nn.Embedding(259,16,dtype=torch.float64)
    def forward(self,tokens): return (self.embed(tokens),)


class Core(torch.nn.Module):
    def __init__(self): super().__init__(); self.linear=torch.nn.Linear(16,16,dtype=torch.float64)
    def forward(self,state,local,route_index): return torch.tanh(self.linear(state)+local*.1)


class Backbone(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.local_encoder=Encoder(); self.core=Core(); self.readout_norm=torch.nn.LayerNorm(16,dtype=torch.float64)
        self.classifier=torch.nn.Linear(16,256,dtype=torch.float64)
        self.config=NS(max_tokens=64,width=16,next_route=0,instruction_route=1,internal_steps=2)
    def forward(self,tokens,tasks):
        valid=tokens!=256; local=self.local_encoder(tokens)[0]*valid[:,:,None]; state=local
        for _ in range(2):
            state=self.core(state,local,route_index=0); self.core(state,local,route_index=1)
        return self.classifier(self.readout_norm(state[torch.arange(len(tokens)),valid.sum(1)-1]))


class Toy(torch.nn.Module):
    def __init__(self,forward):
        super().__init__(); self.backbone=Backbone(); self.read=torch.nn.Module()
        for n in ("key","query","output"): setattr(self.read,n,torch.nn.Linear(16,16,bias=False,dtype=torch.float64))
        self.forward=types.MethodType(forward,self)


@contextlib.contextmanager
def counted(model,core):
    calls=[0,0]; cores=[0]
    def mh(_,args,out): calls[0]+=1; calls[1]+=len(args[0])
    def ch(*a): cores[0]+=1
    a=model.register_forward_hook(mh); c=model.backbone.core.register_forward_hook(ch)
    try: yield calls,cores
    finally: a.remove(); c.remove()


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
    with torch.no_grad(),patch.object(torch.nn.Module,"_call_impl",side_effect=AssertionError("model forbidden")),patch.object(torch.nn.Module,"load_state_dict",side_effect=AssertionError("model load forbidden")): yield


def fixture_context():
    parent,forward,realspan=accepted_functions()
    def score(data,raw,c):
        totals=[]
        for s in b.SPLITS:
            y=torch.tensor([r["target"] for r in data[s]]); correct=sum(int((raw[s][p]["normal"].argmax(1)==y).sum()) for p in PROFILES)
            totals.append(dict(split=s,rows=3*len(y),correct=correct,full_pass=correct==3*len(y),direct_pass=correct==3*len(y)))
        return dict(passed=all(z["full_pass"] for z in totals),totals=totals)
    return NS(parent=parent,wide=NS(span_mask=realspan,prefix_tensor=prefix,score_length=score,PINNED={},context=lambda:()),
        p312=NS(context=lambda:()),p313=None,guarded=NS(no_neural=no_neural),
        diag=NS(normalize_task=lambda z,*a:z["totals"],partition=lambda z:{k:v for k,v in z[0].items() if k!="split"}),
        c=NS(p267=NS(check_logits=check_logits,counted=counted,validate_data=lambda _:None),core=None,base=NS(fingerprint=fingerprint),audit=Audit(),factory=NS(language_module=lambda:None))),forward


def perfect_raw(data):
    zs={}
    for s in b.SPLITS:
        z=torch.zeros((len(data[s]),256),dtype=torch.float64); y=torch.tensor([r["target"] for r in data[s]]); z[torch.arange(len(y)),y]=5.; zs[s]=z
    return {str(n):{s:{p:{v:zs[s] for v in b.VIEWS} for p in profiles(n)} for s in b.SPLITS} for n in range(1,7)}


def fixtures(data):
    anchors=[]; records=[]
    for f in b.expected_parent_results():
        raw=perfect_raw(data)
        if not f["six_pass"]:
            raw["6"]=copy.deepcopy(raw["6"])
            for s in b.SPLITS:
                raw["6"][s]["repeat"]["normal"]=raw["6"][s]["repeat"]["normal"].clone()
                raw["6"][s]["repeat"]["normal"][0,70]=9.
        h=b.digest([f["seed"],f["arm"]]); key=dict(seed=f["seed"],arm=f["arm"],final_sha256=h)
        anchors.append(dict(**key,raw=raw))
        records.append(dict(**key,raw={m:raw for m in b.MODES},attestations={m:dict(calls=144,query_calls=288,rows=13824,different_positions=8928) for m in b.MODES},
            replay_errors=[0.,0.],weights_preserved=True,hooks_restored=True))
    return anchors,records


def protection():
    pins={n:"a"*40 for n in b.OWN}; pins.update({b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB})
    while len(pins)<748: pins["fixture/"+str(len(pins))]="a"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1407)}


def payload(s):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)


class C317Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.det=torch.are_deterministic_algorithms_enabled(); torch.set_num_threads(2)
        cls.data=dataset(); cls.prompts=prompts_for(cls.data); cls.x,cls.forward_fn=fixture_context()
        cls.anchors,cls.records=fixtures(cls.data); cls.metrics,cls.summary=b.analyze(cls.records,cls.anchors,cls.data,cls.x)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.det)
    def toy(self):
        torch.manual_seed(11); m=Toy(type(self).forward_fn); m.eval(); m.requires_grad_(False); return m
    def inp(self,texts=("aaaa=0;baaa=1;baaa=", "甲甲甲甲=0;乙甲甲甲=1;乙甲甲甲=")):
        x=torch.stack([prefix(s) for s in texts]); return x,torch.zeros(len(x),dtype=torch.int64)

    def test_01_seal(self): b.validate_seal(); self.assertEqual(json.loads(b.blob(b.manifest())),b.manifest())
    def test_02_bad_seal(self):
        with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaises(ValueError): b.validate_seal()
    def test_03_input_hashes(self):
        self.assertEqual(b.digest(self.data),b.DATA_SHA); self.assertEqual(b.digest(self.prompts),b.PROMPTS_SHA)
    def test_04_native_pass_through_identity(self):
        m=self.toy(); state=fingerprint(m); hooks=b.hook_snapshot(m)
        with torch.no_grad():
            expected=m(*self.inp())
            with b.endpoint_probe(m,self.x.wide,False) as stats: actual=m(*self.inp())
        self.assertTrue(torch.equal(expected,actual)); self.assertEqual(stats,dict(calls=1,query_calls=2,rows=2,different_positions=2))
        self.assertEqual(state,fingerprint(m)); self.assertEqual(hooks,b.hook_snapshot(m))
    def test_05_first_anchor_matches_independent_formula(self):
        m=self.toy(); tokens,tasks=self.inp(); sp=span(tokens); valid=tokens!=256; rows=torch.arange(len(tokens))
        with torch.no_grad():
            local=m.backbone.local_encoder(tokens)[0]*valid[:,:,None]; state=local
            for _ in range(2): state=m.backbone.core(state,local,route_index=0)
            mean=(local*sp[:,:,None]).sum(1)/sp.sum(1,keepdim=True); first=sp.to(torch.int64).argmax(1)
            k=m.read.key(local); qmean=m.read.query(mean); qfirst=m.read.query(local[rows,first]); memory=0
            for q in (qmean,qfirst):
                weights=((k*q[:,None,:]).sum(-1)/4.).masked_fill(~valid,float("-inf")).softmax(-1)
                memory=memory+(weights[:,:,None]*local).sum(1)*.5
            expected=m.backbone.classifier(m.backbone.readout_norm(state[rows,valid.sum(1)-1]+m.read.output(memory)))
            native=m(tokens,tasks)
            with b.endpoint_probe(m,self.x.wide,True): got=m(tokens,tasks)
        self.assertTrue(torch.allclose(expected,got,atol=1e-14,rtol=0)); self.assertFalse(torch.equal(native,got))
    def test_06_one_byte_and_blind_identity(self):
        m=self.toy(); args=self.inp(("a=0;b=1;a=","甲甲=0;乙甲=1;?="))
        with torch.no_grad():
            native=m(*args)
            with b.endpoint_probe(m,self.x.wide,True): changed=m(*args)
        self.assertTrue(torch.equal(native,changed))
    def test_07_unicode_byte_not_character(self):
        tokens,_=self.inp(("甲=0;乙=1;乙=",)); sp=self.x.wide.span_mask(tokens)
        self.assertEqual(int(sp.sum()),3); self.assertEqual(tokens[sp].tolist(),list("乙".encode("utf-8")))
    def test_08_frozen_only(self):
        with self.assertRaises(ValueError),b.endpoint_probe(self.toy(),self.x.wide,True): pass
        for m in (self.toy().train(),self.toy().requires_grad_(True)):
            with torch.no_grad(),self.assertRaises(ValueError),b.endpoint_probe(m,self.x.wide,True): pass
        with torch.no_grad(),self.assertRaises(ValueError),b.endpoint_probe(self.toy(),self.x.wide,1): pass
    def test_09_query_provenance_rejection_cleanup(self):
        m=self.toy(); h=m.read.query.register_forward_pre_hook(lambda mod,args:(args[0]+1.,)); hooks=b.hook_snapshot(m)
        with torch.no_grad(),self.assertRaisesRegex(ValueError,"provenance"),b.endpoint_probe(m,self.x.wide,True): m(*self.inp())
        self.assertEqual(hooks,b.hook_snapshot(m)); h.remove()
    def test_10_exception_cleanup(self):
        m=self.toy(); hooks=b.hook_snapshot(m)
        with patch.object(m.read.output,"forward",side_effect=RuntimeError("fixture")),torch.no_grad(),self.assertRaisesRegex(RuntimeError,"fixture"),b.endpoint_probe(m,self.x.wide,True): m(*self.inp())
        self.assertEqual(hooks,b.hook_snapshot(m))
    def test_11_existing_hooks_repeated_calls_no_optimizer(self):
        m=self.toy(); calls=[]; h=m.read.query.register_forward_hook(lambda *a:calls.append(1)); hooks=b.hook_snapshot(m); fp=fingerprint(m)
        with torch.no_grad(),patch.object(torch.optim,"AdamW",side_effect=AssertionError("optimizer")),b.endpoint_probe(m,self.x.wide,True) as stats:
            m(*self.inp()); m(*self.inp())
        self.assertEqual(stats["query_calls"],4); self.assertEqual(len(calls),4); self.assertEqual(hooks,b.hook_snapshot(m)); self.assertEqual(fp,fingerprint(m)); h.remove()
        with torch.no_grad(),self.assertRaisesRegex(ValueError,"coverage"),b.endpoint_probe(m,self.x.wide,True): pass
    def test_12_actual_infer_and_parent_evaluator(self):
        m=self.toy(); raw=self.x.parent.evaluate(m,self.prompts,self.data,self.x.wide,self.x.c)
        anchor=dict(seed=b.SEEDS[0],arm=b.ARMS[0],final_sha256=fingerprint(m),raw=raw)
        with contextlib.redirect_stdout(io.StringIO()): r=b.infer_one(m,m.state_dict(),anchor,self.data,self.prompts,self.x)
        self.assertEqual(r["replay_errors"],[0.,0.]); self.assertEqual(r["attestations"]["first_byte"]["different_positions"],8928)
        changed=copy.deepcopy(m.state_dict()); changed["read.output.weight"]+=.1
        with self.assertRaises(ValueError): b.infer_one(m,changed,anchor,self.data,self.prompts,self.x)
    def test_13_degenerate_reconstruction_rejects_tamper(self):
        raw=perfect_raw(self.data); changed=copy.deepcopy(raw)
        changed["6"]["TRAIN"]["repeat"]["query_blind"]=changed["6"]["TRAIN"]["repeat"]["query_blind"].clone()+1
        with self.assertRaisesRegex(ValueError,"query-blind"): b.degenerate_controls(raw,changed,self.data)
    def test_14_paired_rescues_regressions(self):
        rows=[dict(target=48),dict(target=49),dict(target=50)]; a=torch.zeros((3,256)); z=a.clone()
        a[0,70]=1; a[1,49]=1; a[2,71]=1; z[0,48]=1; z[1,70]=1; z[2,72]=1
        d=b.paired_counts(a,z,rows,[0,1,2]); self.assertEqual((d["rescued"],d["regressed"],d["argmax_flips"]),(1,1,3))
    def test_15_inventory_and_baseline_gates(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["paired_local_groups"])),(20,200,640))
        self.assertEqual(sum(r["rows"] for r in self.summary["paired_local_groups"]),46080); b.validate_result(payload(self.summary))
    def test_16_no_capability_from_diagnostic(self):
        rr=copy.deepcopy(self.records)
        for r in rr:
            changed=copy.deepcopy(r["raw"]["first_byte"])
            for n,s,p in itertools.product(range(2,7),b.SPLITS,PROFILES):
                changed[str(n)][s][p]["normal"]=torch.zeros_like(changed[str(n)][s][p]["normal"])
            r["raw"]["first_byte"]=changed
        _,s=b.analyze(rr,self.anchors,self.data,self.x); b.validate_result(payload(s))
        self.assertEqual(s["length_pass_counts"]["first_byte"]["6"],dict.fromkeys(b.ARMS,0))
    def test_17_cohort_receipts_and_replay_rejection(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.anchors,self.data,self.x)
        for key,value in (("weights_preserved",False),("final_sha256","wrong"),("replay_errors",[.1,0.])):
            rr=copy.deepcopy(self.records); rr[0][key]=value
            with self.assertRaises(ValueError): b.analyze(rr,self.anchors,self.data,self.x)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c317-fixture")/str(i)/"summary.json").resolve() for i in range(43)]
        outputs=("architecture-plan.json","dataset.json","length-datasets.json","trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")
        p=dict(experiment_id="C316-v5b-single-mix-replication",status="FAIL",commit_sha=b.PARENT_EXECUTION,source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB},
            artifacts=[dict(file=n) for n in outputs],validation_summary=dict(seed_results=b.expected_parent_results(),candidate_gate=False,all_pairs_matched=True,all_replays=True))
        parent=NS(OUTPUTS=outputs,parent_hashes=lambda p:tuple(str(i%10)*64 for i in range(42)),verify_artifacts=Mock(return_value=(p,[])),validate_result=Mock())
        hashes=dict(zip(map(str,paths),(b.PARENT_SHA,*parent.parent_hashes(None)),strict=True)); x=copy.copy(self.x)
        x.c=NS(p267=NS(validate_data=lambda _:None),audit=NS(sha=lambda p:hashes[str(p)],read_json=lambda p:self.data if p.name=="dataset.json" else self.prompts))
        archive=dict(schema="fold-c316-single-replication-eval-v1",records=self.anchors)
        with patch.object(b,"context",return_value=(parent,x)),patch.object(torch,"load",return_value=archive): yield paths,hashes,parent,p,archive
    def test_18_all43_hash_guards(self):
        with self.loader_fixture() as (paths,hashes,parent,p,_):
            self.assertEqual(b.load_parent(paths)[0],p); parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=hashes[str(path)]; hashes[str(path)]="f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); hashes[str(path)]=old
    def test_19_parent_semantics(self):
        for fn in (lambda p,a:p.update(status="PASS"),lambda p,a:a.update(schema="wrong"),lambda p,a:p["validation_summary"]["seed_results"].reverse()):
            with self.loader_fixture() as (paths,_,_,p,a):
                fn(p,a)
                with self.assertRaises(ValueError): b.load_parent(paths)
    def test_20_actual_precheck_protection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pins={b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB}
            while len(pins)<742: pins["accepted/"+str(len(pins))]="a"*40
            for n in list(pins)+list(b.OWN): p=root/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1393-len(inputs)):
                p=root/("input"+str(i));p.write_text("data",encoding="utf-8");inputs[str(p.resolve())]=Audit.sha(p)
            folder=root/"parent";folder.mkdir();summary=folder/"summary.json";summary.write_text("summary",encoding="utf-8");arts=[]
            for n in ("architecture-plan.json","dataset.json","length-datasets.json","trained-models.pt","evaluations.pt","measurements.json","validation-summary.json"):
                p=folder/n;p.write_text("artifact",encoding="utf-8");arts.append(dict(file=n,sha256=Audit.sha(p)))
            def sha(p): return b.PARENT_SHA if Path(p)==summary else Audit.sha(p)
            parent=types.ModuleType("parent");parent.__file__=str(root/b.PARENT_SOURCE)
            x=NS(parent=NS(PINNED={},context=lambda:()),p312=NS(context=lambda:()),wide=NS(PINNED={},context=lambda:()),
                c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,safe_child=Audit.safe_child,
                    git=lambda root,*a:(pins.get(a[1][5:],"b"*40)+"\n").encode(),protect_tree_files=lambda root,pp:{str((root/n).resolve()):sha(root/n) for n in pp})))
            with patch.object(b,"context",return_value=(parent,x)),patch.object(b,"load_parent",return_value=(dict(source_blobs=pins,input_sha256=inputs,artifacts=arts),None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*43,root))),(748,1407))
                x.c.missing=types.ModuleType("missing");x.c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([summary]*43,root)
    def test_21_runtime_preflight_both_actual_forwards(self):
        models={a:self.toy() for a in b.ARMS}; states=[m.state_dict() for m in models.values()]; anchors=[dict(final_sha256=fingerprint(m)) for m in models.values()]
        parent=NS(load_bundle=lambda p:states,make_models=lambda s,x:models)
        with patch.object(b,"precheck",return_value=protection()),patch.object(b,"context",return_value=(parent,self.x)),patch.object(b,"load_parent",return_value=({},self.data,self.prompts,anchors)),contextlib.redirect_stdout(io.StringIO()): b.runtime_preflight(["x"]*43,Path.cwd())

    @contextlib.contextmanager
    def run_fixture(self):
        events=[]
        def pre(*a): events.append("precheck"); return protection()
        def load(*a): events.append("load"); return [{}]*10
        def infer(*a): events.append("infer"); return self.records[b.identities().index((a[2]["seed"],a[2]["arm"]))]
        parent=NS(load_bundle=load,make_models=lambda *a:dict.fromkeys(b.ARMS))
        with patch.object(b,"context",return_value=(parent,self.x)),patch.object(b,"precheck",side_effect=pre),patch.object(b,"load_parent",return_value=({},self.data,self.prompts,self.anchors)),patch.object(b,"infer_one",side_effect=infer): yield events
    def test_22_run_loader_once_no_checkpoint_write(self):
        names=[]; real=torch.save
        def save(obj,p): names.append(Path(p).name); real(obj,p)
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,patch.object(torch,"save",side_effect=save),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*43,output_dir=out,expected_head="f"*40)
            self.assertEqual(events.count("load"),1);self.assertEqual(events.count("infer"),10);self.assertEqual(names,["evaluations.pt"])
            q,_=b.verify_artifacts(out,["x"]*43,"f"*40);self.assertEqual(p,q)
    def test_23_persisted_tamper_resealed_descriptor(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*43,output_dir=out,expected_head="f"*40);path=out/"measurements.json";path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*43,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size);(out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*43,"f"*40)
    def test_24_no_overwrite_or_wrong_head(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()),self.assertRaises(FileExistsError): b.run(summaries=["x"]*43,output_dir=tmp,expected_head="f"*40)
        with self.assertRaises(ValueError): b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))
    def test_25_result_scope_and_work(self):
        for fn in (lambda p:p.update(capability_gate_applicable=True),lambda p:p["validation_summary"].update(train_steps=False),lambda p:p["validation_summary"]["cell_results"][0].update(six_pass=False)):
            p=payload(copy.deepcopy(self.summary));fn(p)
            with self.assertRaises(ValueError):b.validate_result(p)
    def test_26_suite_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["f."+str(i) for i in range(5149)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            self.assertEqual({t.id() for t in b.flatten(b.regression_suite(Path.cwd()))},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())
    def test_27_cli_context(self):
        argv=["program","--summaries"]+[str(i) for i in range(43)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:b.main();self.assertEqual(len(run.call_args.kwargs["summaries"]),43)
        p=NS(context=lambda:"context",regression_modules=lambda _:["m"+str(i) for i in range(201)])
        package=types.ModuleType("fold_lm.v05_benchmarks");package.model_c316_single_mix_replication=p
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):self.assertEqual(b.context(),(p,"context"));self.assertEqual(len(b.regression_modules(Path.cwd())),202)
    def test_28_utf8_inventory(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN:self.assertTrue((root/n).read_text(encoding="utf-8"))
        for p in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="read_text":self.assertTrue(any(k.arg=="encoding" for k in n.keywords))
    def test_29_runner_indices_paths(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for s in blocks:compile(s,"embedded","exec")
        self.assertIn("sys.argv[2:45]",blocks[2]);self.assertIn("head = sys.argv[45]",blocks[2]);self.assertIn("len(sys.argv) == 46",blocks[2])
        self.assertEqual(re.findall(r'runs\\c(\d{3})-.*?\\summary.json',launcher),[str(n) for n in range(316,273,-1)])
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"));self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))
    def test_30_actual_span_matches_independent(self):
        for text in ("a=0;b=1;a=","aaaaaa=0;baaaaa=1;baaaaa=","甲甲甲甲甲甲=0;乙甲甲甲甲甲=1;乙甲甲甲甲甲=","甲=0;乙=1;?="):
            tokens=prefix(text)[None,:];self.assertTrue(torch.equal(span(tokens),self.x.wide.span_mask(tokens)))
    def test_31_input_receipts_and_original_gates(self):
        rr=copy.deepcopy(self.records);rr[0]["attestations"]["first_byte"]["query_calls"]-=1
        with self.assertRaises(ValueError):b.analyze(rr,self.anchors,self.data,self.x)
        self.assertEqual(self.summary["length_pass_counts"]["original_before"]["6"],dict.fromkeys(b.ARMS,4))
    def test_32_count_direct_import_and_payload(self):
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),32)
        imports=[n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c316_single_mix_replication"]);self.assertEqual(b.manifest()["raw_logit_payload_bytes"],10*3*13824*256*8)


if __name__=="__main__":unittest.main()
