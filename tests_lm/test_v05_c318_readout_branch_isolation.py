"""C318 software controls; synthetic scores do not measure actual FOLD competence."""
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
from fold_lm.v05_benchmarks import model_c318_readout_branch_isolation as b
from fold_lm.v05_benchmarks import model_c317_query_endpoint_probe as parent

VIEWS=("normal","evidence_blind","query_blind")
PROFILES=("repeat","shared_prefix","shared_suffix")
def profiles(n): return PROFILES[:1] if n==1 else PROFILES


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
        names={i:chars[i]*n,j:chars[j]*n if p==PROFILES[0] else chars[i]*(n-1)+chars[j] if p==PROFILES[1] else chars[j]+chars[i]*(n-1)}
        return ";".join(names[k]+"="+("?" if v=="evidence_blind" else str(r["values"][r["entities"].index(k)])) for k in r["permutation"])+";"+("?" if v=="query_blind" else names[r["query"]])+"="
    return {str(n):{s:{p:[dict(source_id=r["id"],target=r["target"],views={v:render(r,n,p,v) for v in VIEWS}) for r in data[s]] for p in profiles(n)} for s in b.SPLITS} for n in range(1,7)}


def prefix(text):
    raw=list(text.encode("utf-8")); b.require(len(raw)+2<=64,"overflow")
    return torch.tensor([257,*raw,258,*([256]*(62-len(raw)))],dtype=torch.int64)


def fingerprint(m):
    h=hashlib.sha256()
    for n,z in sorted(m.state_dict().items()): h.update(n.encode()); h.update(z.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def check_logits(z,n):
    b.require(z.shape==(n,256) and z.dtype==torch.float64 and z.device.type=="cpu" and bool(torch.isfinite(z).all()),"logits")


def accepted_functions():
    root=Path(__file__).resolve().parents[1]
    tree=ast.parse((root/b.WIDE_SOURCE).read_text(encoding="utf-8")); cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="LengthReadout")
    forward=copy.deepcopy(next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=="forward")); forward.name="forward"
    span=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="span_mask")
    env=dict(torch=torch,require=b.require,SLOTS=64,Counter=Counter)
    exec(compile(ast.Module(body=[span,forward],type_ignores=[]),"accepted_C304","exec"),env)
    tree=ast.parse((root/"fold_lm/v05_benchmarks/model_c315_single_character_mix.py").read_text(encoding="utf-8"))
    names={"evaluate","validate_raw","replay_error"}; nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==names
    env2=dict(torch=torch,require=b.require,itertools=itertools,SPLITS=b.SPLITS,VIEWS=VIEWS,profiles=profiles)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),"accepted_C315","exec"),env2)
    return env["forward"],env["span_mask"],NS(**{n:env2[n] for n in names},profiles=profiles,context=lambda:())


class Encoder(torch.nn.Module):
    def __init__(self): super().__init__(); self.embed=torch.nn.Embedding(259,16,dtype=torch.float64)
    def forward(self,tokens): return (self.embed(tokens),)
class Core(torch.nn.Module):
    def __init__(self): super().__init__(); self.linear=torch.nn.Linear(16,16,dtype=torch.float64)
    def forward(self,state,local,route_index): return torch.tanh(self.linear(state)+local*.1)
class Backbone(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.local_encoder=Encoder(); self.core=Core(); self.readout_norm=torch.nn.LayerNorm(16,dtype=torch.float64); self.classifier=torch.nn.Linear(16,256,dtype=torch.float64)
        self.config=NS(max_tokens=64,width=16,next_route=0,instruction_route=1,internal_steps=2)
    def forward(self,tokens,tasks):
        valid=tokens!=256; local=self.local_encoder(tokens)[0]*valid[:,:,None]; state=local
        for _ in range(2): state=self.core(state,local,route_index=0); self.core(state,local,route_index=1)
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
    def ch(*_): cores[0]+=1
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
    with torch.no_grad(),patch.object(torch.nn.Module,"_call_impl",side_effect=AssertionError("model forbidden")),patch.object(torch.nn.Module,"load_state_dict",side_effect=AssertionError("state load forbidden")): yield


def fixture_context():
    forward,span,p315=accepted_functions()
    def score(data,raw,c):
        rows=[]
        for split in b.SPLITS:
            y=torch.tensor([r["target"] for r in data[split]]); correct=sum(int((raw[split][p]["normal"].argmax(1)==y).sum()) for p in PROFILES)
            rows.append(dict(split=split,rows=3*len(y),correct=correct,full_pass=correct==3*len(y),direct_pass=correct==3*len(y)))
        return dict(passed=all(r["full_pass"] for r in rows),totals=rows)
    x=NS(parent=p315,p312=NS(context=lambda:()),wide=NS(span_mask=span,prefix_tensor=prefix,score_length=score,context=lambda:()),guarded=NS(no_neural=no_neural),
        diag=NS(normalize_task=lambda z,*_:z["totals"],partition=lambda z:{k:v for k,v in z[0].items() if k!="split"}),
        c=NS(audit=Audit(),base=NS(fingerprint=fingerprint),p267=NS(check_logits=check_logits,counted=counted),core=None,factory=NS(language_module=lambda:None)))
    return x,forward


def perfect_raw(data):
    zs={}
    for s in b.SPLITS:
        z=torch.zeros((len(data[s]),256),dtype=torch.float64); y=torch.tensor([r["target"] for r in data[s]]); z[torch.arange(len(y)),y]=5.; zs[s]=z
    return {str(n):{s:{p:{v:zs[s] for v in VIEWS} for p in profiles(n)} for s in b.SPLITS} for n in range(1,7)}


def fixtures(data):
    anchors=[]; records=[]
    for f in parent.expected_parent_results():
        raw=perfect_raw(data)
        if not f["six_pass"]:
            raw["6"]=copy.deepcopy(raw["6"]); raw["6"]["HOLDOUT"]["repeat"]["normal"]=raw["6"]["HOLDOUT"]["repeat"]["normal"].clone(); raw["6"]["HOLDOUT"]["repeat"]["normal"][0,70]=9.
        key=dict(seed=f["seed"],arm=f["arm"],final_sha256=b.digest([f["seed"],f["arm"]]))
        anchors.append(dict(**key,raw=raw)); records.append(dict(**key,raw={m:raw for m in b.MODES},receipts={m:dict(calls=144,query_calls=288,rows=13824,one_byte_rows=4896) for m in b.MODES},replay_errors=[0.,0.],weights_preserved=True,hooks_restored=True))
    return anchors,records


def protection():
    pins={n:"a"*40 for n in b.OWN}; pins.update({b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB})
    while len(pins)<754: pins["fixture/"+str(len(pins))]="a"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1418)}


def payload(s):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)


class C318Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.det=torch.are_deterministic_algorithms_enabled(); torch.set_num_threads(2)
        cls.data=dataset(); cls.prompts=prompts_for(cls.data); cls.x,cls.forward_fn=fixture_context(); cls.anchors,cls.records=fixtures(cls.data)
        cls.metrics,cls.summary=b.analyze(cls.records,cls.anchors,cls.data,parent,cls.x)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.det)
    def toy(self):
        torch.manual_seed(11); m=Toy(type(self).forward_fn); m.eval(); m.requires_grad_(False); return m
    def inp(self,texts=("aaaa=0;baaa=1;baaa=","甲甲甲甲=0;乙甲甲甲=1;乙甲甲甲=")):
        return torch.stack([prefix(t) for t in texts]),torch.zeros(len(texts),dtype=torch.int64)
    def test_01_seal(self):
        b.validate_seal()
        with patch.object(b,"MANIFEST_SHA","0"*64),self.assertRaises(ValueError): b.validate_seal()
    def test_02_original_identity(self):
        m=self.toy(); h=b.hooks(m); fp=fingerprint(m)
        with torch.no_grad():
            native=m(*self.inp())
            for mode in (b.MODES[0],b.MODES[-1]):
                with b.branch_probe(m,self.x.wide,mode) as stats: z=m(*self.inp())
                self.assertTrue(torch.equal(native,z)); self.assertEqual(stats,dict(calls=1,query_calls=2,rows=2,one_byte_rows=0))
        self.assertEqual(h,b.hooks(m)); self.assertEqual(fp,fingerprint(m))
    def test_03_independent_single_branch_formula(self):
        m=self.toy(); tokens,tasks=self.inp(); valid=tokens!=256; span=self.x.wide.span_mask(tokens); rows=torch.arange(len(tokens))
        with torch.no_grad():
            local=m.backbone.local_encoder(tokens)[0]*valid[:,:,None]; state=local
            for _ in range(2): state=m.backbone.core(state,local,route_index=0)
            mean=(local*span[:,:,None]).sum(1)/span.sum(1,keepdim=True); last=torch.where(span,torch.arange(64),-1).max(1).values
            outputs=[]
            for mode,q in (("mean_only",mean),("last_only",local[rows,last])):
                k=m.read.key(local); query=m.read.query(q); attention=((k*query[:,None,:]).sum(-1)/4.).masked_fill(~valid,float("-inf")).softmax(-1)
                memory=(attention[:,:,None]*local).sum(1)
                expected=m.backbone.classifier(m.backbone.readout_norm(state[rows,valid.sum(1)-1]+m.read.output(memory)))
                with b.branch_probe(m,self.x.wide,mode): z=m(tokens,tasks)
                self.assertTrue(torch.allclose(expected,z,atol=1e-14,rtol=0)); outputs.append(z)
            self.assertFalse(torch.equal(*outputs))
    def test_04_one_byte_controls(self):
        m=self.toy(); args=self.inp(("a=0;b=1;a=","甲甲=0;乙甲=1;?="))
        with torch.no_grad():
            native=m(*args)
            for mode in b.MODES[1:3]:
                with b.branch_probe(m,self.x.wide,mode) as stats: z=m(*args)
                self.assertTrue(torch.equal(native,z)); self.assertEqual(stats["one_byte_rows"],2)
    def test_05_frozen_modes(self):
        with self.assertRaises(ValueError),b.branch_probe(self.toy(),self.x.wide,"mean_only"): pass
        for m,mode in ((self.toy().train(),"last_only"),(self.toy().requires_grad_(True),"mean_only"),(self.toy(),"unknown")):
            with torch.no_grad(),self.assertRaises(ValueError),b.branch_probe(m,self.x.wide,mode): pass
    def test_06_native_provenance_cleanup(self):
        m=self.toy(); h=m.read.query.register_forward_pre_hook(lambda _,a:(a[0]+1.,)); before=b.hooks(m)
        with torch.no_grad(),self.assertRaisesRegex(ValueError,"provenance"),b.branch_probe(m,self.x.wide,"last_only"): m(*self.inp())
        self.assertEqual(before,b.hooks(m)); h.remove()
    def test_07_exception_and_empty_cleanup(self):
        m=self.toy(); before=b.hooks(m)
        with torch.no_grad(),patch.object(m.read.output,"forward",side_effect=RuntimeError("fixture")),self.assertRaises(RuntimeError),b.branch_probe(m,self.x.wide,"mean_only"): m(*self.inp())
        self.assertEqual(before,b.hooks(m))
        with torch.no_grad(),self.assertRaises(ValueError),b.branch_probe(m,self.x.wide,"last_only"): pass
    def test_08_existing_hooks_and_no_optimizer(self):
        m=self.toy(); seen=[]; h=m.read.query.register_forward_hook(lambda *a:seen.append(1)); before=b.hooks(m); fp=fingerprint(m)
        with torch.no_grad(),patch.object(torch.optim,"AdamW",side_effect=AssertionError("no training")),b.branch_probe(m,self.x.wide,"mean_only") as stats:
            m(*self.inp()); m(*self.inp())
        self.assertEqual((stats["calls"],len(seen)),(2,4)); self.assertEqual(before,b.hooks(m)); self.assertEqual(fp,fingerprint(m)); h.remove()
    def test_09_actual_inference_pipeline(self):
        m=self.toy(); raw=self.x.parent.evaluate(m,self.prompts,self.data,self.x.wide,self.x.c); anchor=dict(seed=b.SEEDS[0],arm=b.ARMS[0],final_sha256=fingerprint(m),raw=raw)
        with contextlib.redirect_stdout(io.StringIO()): r=b.infer_one(m,m.state_dict(),anchor,self.data,self.prompts,parent,self.x)
        self.assertEqual(r["replay_errors"],[0.,0.]); self.assertEqual(r["receipts"]["last_only"]["one_byte_rows"],4896)
        changed=copy.deepcopy(m.state_dict()); changed["read.output.weight"]+=1
        with self.assertRaises(ValueError): b.infer_one(m,changed,anchor,self.data,self.prompts,parent,self.x)
    def test_10_inventory_and_baseline(self):
        self.assertEqual(tuple(map(len,(self.metrics,self.summary["final_partitions"],self.summary["single_character_diagnostics"],self.summary["paired_local_groups"]))),(30,300,60,1280))
        self.assertEqual(sum(z["rows"] for z in self.summary["paired_local_groups"]),92160); b.validate_result(payload(self.summary))
    def test_11_changed_failures_still_diagnostic(self):
        rr=copy.deepcopy(self.records)
        for r in rr:
            for mode in b.MODES[1:3]:
                r["raw"][mode]=copy.deepcopy(r["raw"][mode])
                for n,s,p in itertools.product(range(2,7),b.SPLITS,PROFILES): r["raw"][mode][str(n)][s][p]["normal"]=torch.zeros_like(r["raw"][mode][str(n)][s][p]["normal"])
        _,s=b.analyze(rr,self.anchors,self.data,parent,self.x); b.validate_result(payload(s)); self.assertEqual(s["length_pass_counts"]["mean_only"]["6"],dict.fromkeys(b.ARMS,0))
    def test_12_cohort_replay_receipts(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.anchors,self.data,parent,self.x)
        for key,val in (("weights_preserved",False),("final_sha256","wrong"),("replay_errors",[.1,0.])):
            rr=copy.deepcopy(self.records); rr[0][key]=val
            with self.assertRaises(ValueError): b.analyze(rr,self.anchors,self.data,parent,self.x)
    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c318")/str(i)/"summary.json").resolve() for i in range(44)]; hashes=dict(zip(map(str,paths),(b.PARENT_SHA,*[str(i%10)*64 for i in range(43)]),strict=True))
        counts={m:{str(n):dict.fromkeys(b.ARMS,0 if m=="first_byte" else 4 if n==6 else 5) for n in range(2,7)} for m in ("original_before","first_byte")}
        evidence=dict(commit_sha=b.PARENT_EXECUTION,experiment_id="C317-v5b-frozen-query-endpoint",status="PASS",capability_gate_applicable=False,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=dict(length_pass_counts=counts))
        tail=tuple(list(hashes.values())[1:])
        p=NS(OUTPUTS=b.OUTPUTS,parent_hashes=lambda *a:tail,verify_artifacts=Mock(return_value=(evidence,[])),validate_result=Mock(),load_parent=Mock(return_value=({},self.data,self.prompts,self.anchors)))
        x=NS(guarded=NS(no_neural=no_neural),c=NS(audit=NS(sha=lambda p:hashes[str(p)])))
        with patch.object(b,"context",return_value=(p,None,x)): yield paths,hashes,p,evidence
    def test_13_all44_hashes_before_parent(self):
        with self.loader_fixture() as (paths,hashes,p,e):
            self.assertEqual(b.load_parent(paths)[0],e); p.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION); p.load_parent.assert_called_once_with(paths[1:])
            for path in paths:
                old=hashes[str(path)]; hashes[str(path)]="f"*64; p.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                p.verify_artifacts.assert_not_called(); hashes[str(path)]=old
    def test_14_wrong_parent_semantics(self):
        for fn in (lambda e:e.update(status="FAIL"),lambda e:e.update(capability_gate_applicable=True),lambda e:e["artifacts"].pop()):
            with self.loader_fixture() as (paths,_,p,e):
                fn(e)
                with self.assertRaises(ValueError): b.load_parent(paths)
    def test_15_precheck_actual_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pins={b.PARENT_SOURCE:b.PARENT_BLOB,b.WIDE_SOURCE:b.WIDE_BLOB}
            while len(pins)<748: pins["accepted/"+str(len(pins))]="a"*40
            for n in list(pins)+list(b.OWN): path=root/n; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in pins}
            for i in range(1407-len(inputs)):
                path=root/("input"+str(i)); path.write_text("input",encoding="utf-8"); inputs[str(path)]=Audit.sha(path)
            folder=root/"parent"; folder.mkdir(); summary=folder/"summary.json"; summary.write_text("summary",encoding="utf-8"); arts=[]
            for n in b.OUTPUTS: path=folder/n; path.write_text("data",encoding="utf-8"); arts.append(dict(file=n,sha256=Audit.sha(path)))
            def sha(path): return b.PARENT_SHA if Path(path)==summary else Audit.sha(path)
            p=types.ModuleType("p"); p.__file__=str(root/b.PARENT_SOURCE)
            x=NS(parent=NS(context=lambda:()),p312=NS(context=lambda:()),wide=NS(context=lambda:()),c=NS(factory=NS(language_module=lambda:None),audit=NS(sha=sha,safe_child=Audit.safe_child,git=lambda root,*a:(pins.get(a[1][5:],"b"*40)+"\n").encode(),protect_tree_files=lambda root,pp:{str((root/n).resolve()):sha(root/n) for n in pp})))
            with patch.object(b,"context",return_value=(p,None,x)),patch.object(b,"load_parent",return_value=(dict(source_blobs=pins,input_sha256=inputs,artifacts=arts),None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([summary]*44,root))),(754,1418)); x.c.missing=types.ModuleType("missing"); x.c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([summary]*44,root)
    @contextlib.contextmanager
    def run_fixture(self):
        events=[]
        def load(path): events.append(("load",path)); return [{}]*10
        def infer(*a): events.append(("infer",None)); return self.records[b.identities().index((a[2]["seed"],a[2]["arm"]))]
        p316=NS(load_bundle=load,make_models=lambda *a:dict.fromkeys(b.ARMS))
        with patch.object(b,"context",return_value=(parent,p316,self.x)),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,self.prompts,self.anchors)),patch.object(b,"infer_one",side_effect=infer): yield events
    def test_16_run_correct_checkpoint_owner_and_roundtrip(self):
        paths=["C317/summary.json","C316/summary.json"]+["ancestor"]*42; saved=[]; real=torch.save
        def save(obj,path): saved.append(Path(path).name); real(obj,path)
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,patch.object(torch,"save",side_effect=save),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=paths,output_dir=out,expected_head="f"*40)
            loads=[v for k,v in events if k=="load"]; self.assertEqual(loads,[(Path(paths[1]).resolve().parent/"trained-models.pt")]); self.assertEqual(sum(k=="infer" for k,v in events),10); self.assertEqual(saved,["evaluations.pt"])
            q,_=b.verify_artifacts(out,paths,"f"*40); self.assertEqual(p,q)
    def test_17_tampering_and_overwrite(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*44,output_dir=out,expected_head="f"*40); path=out/"measurements.json"; path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*44,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name); a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*44,"f"*40)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*44,output_dir=out,expected_head="f"*40)
    def test_18_runtime_preflight(self):
        models={a:self.toy() for a in b.ARMS}; states=[m.state_dict() for m in models.values()]; anchors=[dict(final_sha256=fingerprint(m)) for m in models.values()]
        p316=NS(load_bundle=lambda p:states,make_models=lambda *a:models)
        with patch.object(b,"context",return_value=(parent,p316,self.x)),patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=({},self.data,self.prompts,anchors)),contextlib.redirect_stdout(io.StringIO()): b.runtime_preflight(["x"]*44,Path.cwd())
    def test_19_suite_semantic_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["f."+str(i) for i in range(5173)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            self.assertEqual({t.id() for t in b.flatten(b.regression_suite(Path.cwd()))},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError): b.regression_suite(Path.cwd())
    def test_20_cli_context_modules(self):
        argv=["program","--summaries"]+[str(i) for i in range(44)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),44)
        p=NS(context=lambda:("p316","x"),regression_modules=lambda _:["m"+str(i) for i in range(202)]); package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c317_query_endpoint_probe=p
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}): self.assertEqual(b.context(),(p,"p316","x")); self.assertEqual(len(b.regression_modules(Path.cwd())),203)
    def test_21_result_scope_and_work(self):
        for fn in (lambda p:p.update(capability_gate_applicable=True),lambda p:p["validation_summary"].update(train_steps=False),lambda p:p["validation_summary"]["cell_results"][0].update(six_pass=False)):
            p=payload(copy.deepcopy(self.summary)); fn(p)
            with self.assertRaises(ValueError): b.validate_result(p)
    def test_22_utf8_inventory(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for n in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="read_text": self.assertTrue(any(k.arg=="encoding" for k in n.keywords))
    def test_23_runner_paths_and_arguments(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: compile(code,"embedded","exec")
        self.assertIn("sys.argv[2:46]",blocks[2]); self.assertIn("head = sys.argv[46]",blocks[2]); self.assertIn("len(sys.argv) == 47",blocks[2])
        self.assertEqual(re.findall(r'runs\\c(\d{3})-.*?\\summary.json',launcher),[str(n) for n in range(317,273,-1)])
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute")); self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))
    def test_24_inputs_direct_dependency_payload(self):
        self.assertEqual(b.digest(self.data),"1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1")
        self.assertEqual(b.digest(self.prompts),"2a850d72af8c99321fd3dd4243ec2d01df6fda0bb2696329e29e3995a487fffd")
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),24); self.assertEqual(b.manifest()["raw_logit_payload_bytes"],10*4*13824*256*8)
        imports=[n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c317_query_endpoint_probe"])


if __name__=="__main__": unittest.main()
