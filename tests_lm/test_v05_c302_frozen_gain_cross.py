"""C302 software-control fixtures; no claims about actual FOLD scientific outcomes."""
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
from fold_lm.v05_benchmarks import model_c302_frozen_gain_cross as b


class Encoder(torch.nn.Module):
    def __init__(self): super().__init__(); self.embed=torch.nn.Embedding(259,16,dtype=torch.float64)
    def forward(self,x): return (self.embed(x),)


class Core(torch.nn.Module):
    def __init__(self): super().__init__(); self.linear=torch.nn.Linear(16,16,dtype=torch.float64)
    def forward(self,x,local,route_index): return torch.tanh(self.linear(x)+.1*local)


class Backbone(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.local_encoder=Encoder(); self.core=Core()
        self.readout_norm=torch.nn.LayerNorm(16,dtype=torch.float64); self.classifier=torch.nn.Linear(16,256,dtype=torch.float64)
        self.config=NS(width=16,max_tokens=48,next_route=0,instruction_route=1,internal_steps=2)
        self.padding=torch.nn.Parameter(torch.zeros(13488-sum(p.numel() for p in self.parameters()),dtype=torch.float64))
    def forward(self,x,t):
        valid=x!=256; local=self.local_encoder(x)[0]*valid[:,:,None]; state=local
        for _ in range(2):
            nxt=self.core(state,local,route_index=0); self.core(state,local,route_index=1); state=nxt
        return self.classifier(self.readout_norm(state[torch.arange(len(x)),valid.sum(1)-1]))


class Reader(torch.nn.Module):
    def __init__(self,*_):
        super().__init__()
        for n in ("query","key","output"): setattr(self,n,torch.nn.Linear(16,16,bias=False,dtype=torch.float64))


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.backbone=Backbone(); self.read=Reader(); self.offset=0.; self.fail=False
    def forward(self,x,t):
        def add(module,args):
            if self.fail: raise RuntimeError("fixture failure")
            return (args[0]+self.read.output(args[0])+self.offset,)
        h=self.backbone.readout_norm.register_forward_pre_hook(add)
        try: return self.backbone(x,t)
        finally: h.remove()


def source_wrapper(base,arm):
    class Wrapper(torch.nn.Module):
        def __init__(self):
            super().__init__(); self.model=base; self.register_parameter("gain_logit",torch.nn.Parameter(torch.tensor(-.6,dtype=torch.float64)) if arm==b.ARMS[1] else None)
        def gain(self): return 2*self.gain_logit.sigmoid() if self.gain_logit is not None else next(self.model.parameters()).new_tensor(1.)
        def forward(self,x,t):
            # Independent oracle: capture raw residual,then apply its numerical formula directly.
            captured=[]; h=self.model.backbone.readout_norm.register_forward_pre_hook(lambda module,args:captured.append(args[0]))
            try: self.model(x,t)
            finally: h.remove()
            r=captured[0]
            return self.model.backbone.classifier(self.model.backbone.readout_norm(self.gain()*r+self.model.read.output(r)))
    return Wrapper()


def inputs(n=4):
    x=torch.full((n,48),256,dtype=torch.int64); x[:,:4]=torch.tensor([0,1,2,258])
    return x,torch.zeros(n,dtype=torch.int64)


def frozen():
    torch.manual_seed(8); m=Toy(); m.eval(); m.requires_grad_(False); return m


def fingerprint(m): return b.digest({n:v.detach().tolist() for n,v in m.state_dict().items()})


def parent_flags(seed,arm):
    seen=seed in (301002,301003) or (arm==b.ARMS[1] and seed==301005)
    return dict(two_char=seen,triple=seen,quad=seed in (301002,301003) if arm==b.ARMS[0] else seed==301002)


def raw_fixture(data,flags):
    out={}
    for task in b.TASKS:
        out[task]={}
        for split,rows in data.items():
            z=torch.zeros((len(rows),256),dtype=torch.float64); y=torch.tensor([r["target"] for r in rows]); z[torch.arange(len(rows)),y]=4.
            if not flags[task]: z[0,70]=9.
            out[task][split]={str(p):{v:z for v in ("normal","evidence_blind","query_blind")} for p in range(3)}
    return out


def fixtures():
    data={s:[dict(target=48+i%2) for i in range(n)] for s,n in (("TRAIN",192),("HOLDOUT",96))}
    gains={s:.7+.02*i for i,s in enumerate(b.SEEDS)}; flags={}; records=[]; anchors=[]
    for seed,arm in b.identities():
        flag=parent_flags(seed,arm); flags[(seed,arm)]=flag; raw=raw_fixture(data,flag); h=b.digest([seed,arm]); plan=b.pass_plan(arm,gains[seed])
        original=1. if arm==b.ARMS[0] else gains[seed]
        anchors.append(dict(seed=seed,arm=arm,final_sha256=h,fit=dict(final_gain=original),parameters=14256 if arm==b.ARMS[0] else 14257,checkpoint_roundtrip=True,raw=raw))
        records.append(dict(seed=seed,arm=arm,final_sha256=h,original_gain=original,trained_gain=gains[seed],
            pass_gains={n:a for n,_,a in plan},pass_labels={n:l for n,l,_ in plan},raw={n:raw for n in b.PASSES},
            attestations={n:dict(calls=81,formula_checks=81) for n in b.PASSES},reproduction_errors=[0.,0.,0.],weights_preserved=True,hooks_restored=True))
    return records,anchors,gains,flags,data


def replay_error(left,right,data,c):
    error=0.
    b.require(set(left)==set(right)==set(b.TASKS),"raw tasks")
    for task,split,profile,view in itertools.product(b.TASKS,b.SPLITS,map(str,range(3)),("normal","evidence_blind","query_blind")):
        a,z=left[task][split][profile][view],right[task][split][profile][view]
        error=max(error,float((a-z).abs().max())); b.require(error<=1e-9 and torch.equal(a.argmax(1),z.argmax(1)),"raw replay")
    return error


def scorers():
    def score(data,raw):
        rows=[]
        for split,items in data.items():
            y=torch.tensor([r["target"] for r in items]); n=3*len(items)
            correct=sum(int((v["normal"].argmax(1)==y).sum()) for v in raw[split].values())
            rows.append(dict(split=split,rows=n,correct=correct,direct_pass=correct==n,final_normal_nll=.1))
        return dict(passed=all(r["direct_pass"] for r in rows),totals=rows)
    diag=NS(normalize_task=lambda s,*_:s["totals"],partition=lambda r:{k:v for k,v in r[0].items() if k!="split"})
    return diag,NS(replay_error=replay_error),NS(score_quad=lambda d,r,c:score(d,r)),NS(p267=NS(score=score),c270=NS(score=lambda d,r,p:score(d,r)))


def parent_payload(anchors):
    results=[dict(seed=r["seed"],arm=r["arm"],final_gain=r["fit"]["final_gain"],**{t+"_pass":v for t,v in parent_flags(r["seed"],r["arm"]).items()}) for r in anchors]
    return dict(experiment_id="C301-v5b-learned-residual-gain",commit_sha=b.PARENT_EXECUTION,status="FAIL",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB,b.READOUT_SOURCE:b.READOUT_BLOB},
        artifacts=[dict(file=n) for n in ("architecture-plan.json","dataset.json","triple-dataset.json","quad-dataset.json","trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")],
        validation_summary=dict(seed_results=results,task_pass_counts=b.expected_parent_counts(),candidate_gate=False,all_pairs_matched=True,all_replays=True))


def protection():
    pins={n:"b"*40 for n in b.OWN}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB; pins[b.READOUT_SOURCE]=b.READOUT_BLOB
    while len(pins)<658: pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1217)}


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
        if args[0]=="rev-parse": return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0]=="branch": return b"feat/sft-target-loss\n"
        return b""


def payload(s):
    pins,protected=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)


@contextlib.contextmanager
def counted(model,core):
    calls=[0,0]; cores=[0]
    def mh(module,args,out): calls[0]+=1; calls[1]+=len(args[0])
    def ch(module,args,out): cores[0]+=1
    h=model.register_forward_hook(mh); g=model.backbone.core.register_forward_hook(ch)
    try: yield calls,cores
    finally: h.remove(); g.remove()


def evaluator(model,data,*_):
    raw={}
    for task in b.TASKS:
        raw[task]={}
        for split,rows in data.items():
            raw[task][split]={}
            for p in map(str,range(3)):
                raw[task][split][p]={}
                for v in ("normal","evidence_blind","query_blind"):
                    raw[task][split][p][v]=torch.cat([model(*inputs(min(96,len(rows)-i))) for i in range(0,len(rows),96)])
    return raw


class C302Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.det=torch.are_deterministic_algorithms_enabled(); torch.set_num_threads(2)
        cls.records,cls.anchors,cls.gains,cls.flags,cls.data=fixtures()
        cls.metrics,cls.summary=b.analyze(cls.records,cls.anchors,cls.gains,cls.flags,cls.data,*scorers())
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.det)

    def test_01_seal(self): b.validate_seal(); self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seal(self):
        for h in ("UNSEALED","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",h),self.assertRaises(ValueError): b.validate_seal()

    def test_03_pass_assignment(self):
        self.assertEqual([v[2] for v in b.pass_plan(b.ARMS[0],.8)],[1.,.8,1.])
        self.assertEqual([v[2] for v in b.pass_plan(b.ARMS[1],.8)],[.8,1.,.8])
        with self.assertRaises(ValueError): b.pass_plan("wrong",.8)

    def test_04_gain_validation(self):
        for a in (float("nan"),float("inf"),-1.,3.,True,None):
            with self.assertRaises(ValueError): b.valid_gain(a)
        for a in (0.,1.,2.): self.assertEqual(b.valid_gain(a),a)

    def test_05_exact_unit_identity(self):
        m=frozen(); hooks=b.hook_snapshot(m); state=fingerprint(m)
        with torch.no_grad():
            expected=m(*inputs())
            with b.frozen_gain(m,1.) as stats: z=m(*inputs())
        self.assertTrue(torch.equal(z,expected)); self.assertEqual(stats,dict(calls=1,formula_checks=1))
        self.assertEqual(hooks,b.hook_snapshot(m)); self.assertEqual(state,fingerprint(m))

    def test_06_nonunit_formula(self):
        m=frozen(); captures=[]; h=m.backbone.readout_norm.register_forward_pre_hook(lambda mod,args:captures.append(args[0].clone()))
        with torch.no_grad(): m(*inputs())
        h.remove(); r=captures[0]
        for a in (0.,.7,2.):
            with torch.no_grad():
                expected=m.backbone.classifier(m.backbone.readout_norm(r.new_tensor(a)*r+m.read.output(r)))
                with b.frozen_gain(m,a): actual=m(*inputs())
            self.assertTrue(torch.equal(expected,actual))

    def test_07_frozen_only(self):
        with self.assertRaises(ValueError),b.frozen_gain(frozen(),.8): pass
        m=Toy()
        with torch.no_grad(),self.assertRaises(ValueError),b.frozen_gain(m,.8): pass
        m.eval()
        with torch.no_grad(),self.assertRaises(ValueError),b.frozen_gain(m,.8): pass

    def test_08_exception_and_sum_cleanup(self):
        m=frozen(); hooks=b.hook_snapshot(m); m.fail=True
        with torch.no_grad(),self.assertRaisesRegex(RuntimeError,"fixture failure"),b.frozen_gain(m,.8): m(*inputs())
        self.assertEqual(hooks,b.hook_snapshot(m)); m.fail=False; m.offset=.2
        with torch.no_grad(),self.assertRaisesRegex(ValueError,"sum identity"),b.frozen_gain(m,.8): m(*inputs())
        self.assertEqual(hooks,b.hook_snapshot(m))

    def test_09_repeated_calls_existing_hooks(self):
        m=frozen(); seen=[]; h=m.register_forward_hook(lambda *a:seen.append(1)); hooks=b.hook_snapshot(m)
        with torch.no_grad(),b.frozen_gain(m,.8) as stats:
            for n in (1,7,96): m(*inputs(n))
        self.assertEqual(stats,dict(calls=3,formula_checks=3)); self.assertEqual(len(seen),3); self.assertEqual(hooks,b.hook_snapshot(m)); h.remove()
        with torch.no_grad(),self.assertRaisesRegex(ValueError,"call coverage"),b.frozen_gain(m,.8): pass

    def test_10_no_parameter_changes_or_optimizer(self):
        m=frozen(); state=fingerprint(m)
        with torch.no_grad(),patch.object(torch.optim,"AdamW",side_effect=AssertionError("optimizer")),patch.object(torch.nn.Module,"load_state_dict",side_effect=AssertionError("state reload")),b.frozen_gain(m,.8): m(*inputs())
        self.assertEqual(state,fingerprint(m))
        with torch.no_grad(),self.assertRaises(ValueError),b.frozen_gain(m.float(),.8): m(*inputs())

    def test_11_full_inventory_and_counts(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["within_weight"]),len(self.summary["across_weight"])),(30,180,60,60))
        self.assertEqual(sum(r["rows"] for r in self.summary["within_weight"]+self.summary["across_weight"]),51840)
        b.validate_result(payload(self.summary))

    def test_12_rescues_regressions_wrong_to_wrong(self):
        y=[dict(target=48),dict(target=49),dict(target=50)]; a=torch.zeros((3,256)); c=a.clone()
        a[0,70]=3; a[1,49]=3; a[2,71]=3; c[0,48]=3; c[1,70]=3; c[2,72]=3
        v=b.compare_normal({"p":dict(normal=a)},{"p":dict(normal=c)},y)
        self.assertEqual((v["rescued"],v["regressed"],v["argmax_flips"]),(1,1,3))

    def test_13_profile_alignment(self):
        z=torch.zeros((1,256))
        with self.assertRaises(ValueError): b.compare_normal({"a":dict(normal=z)},{"b":dict(normal=z)},[dict(target=48)])

    def test_14_cohort_and_gain_source_tamper(self):
        with self.assertRaises(ValueError): b.analyze(self.records[:-1],self.anchors,self.gains,self.flags,self.data,*scorers())
        for fn in (lambda r:r["pass_gains"].update(swapped=.123),lambda r:r.update(trained_gain=.1),lambda r:r.update(weights_preserved=False)):
            records=copy.deepcopy(self.records); fn(records[0])
            with self.assertRaises(ValueError): b.analyze(records,self.anchors,self.gains,self.flags,self.data,*scorers())

    def test_15_original_restoration_mismatch(self):
        records=copy.deepcopy(self.records); records[0]["reproduction_errors"][0]=.1
        with self.assertRaises(ValueError): b.analyze(records,self.anchors,self.gains,self.flags,self.data,*scorers())
        records=copy.deepcopy(self.records); records[0]["raw"]["original_after"]=raw_fixture(self.data,dict.fromkeys(b.TASKS,True))
        with self.assertRaises(ValueError): b.analyze(records,self.anchors,self.gains,self.flags,self.data,*scorers())

    def test_16_parent_adapter(self):
        p=parent_payload(self.anchors); g,f=b.adapt_anchors(p,self.anchors); self.assertEqual(g,self.gains); self.assertEqual(f,self.flags)
        p["validation_summary"]["seed_results"][1]["final_gain"]+=.01
        with self.assertRaises(ValueError): b.adapt_anchors(p,self.anchors)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c302-fixture")/str(i)/"summary.json").resolve() for i in range(28)]
        p=parent_payload(self.anchors); parent=NS(context=lambda:(None,),parent_hashes=lambda _:tuple(str(i%10)*64 for i in range(27)),OUTPUTS=tuple(a["file"] for a in p["artifacts"]),verify_artifacts=Mock(return_value=(p,{})),validate_result=Mock())
        mapping=dict(zip(map(str,paths),(b.PARENT_SHA,*parent.parent_hashes(None)),strict=True))
        c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:self.data))
        archive=dict(schema="fold-c301-gain-eval-v1",records=copy.deepcopy(self.anchors))
        with patch.object(b,"context",return_value=(parent,NS(no_neural=contextlib.nullcontext),None,None,None,None,c)),patch.object(torch,"load",return_value=archive): yield paths,mapping,parent,p,archive

    def test_17_all28_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,p,_):
            self.assertEqual(b.load_parent(paths)[0],p); parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)]; mapping[str(path)]="f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); mapping[str(path)]=old

    def test_18_parent_scope_schema(self):
        for fn in (lambda p,a:p.update(status="PASS"),lambda p,a:p["source_blobs"].pop(b.READOUT_SOURCE),lambda p,a:a.update(schema="wrong")):
            with self.loader_fixture() as (paths,_,_,p,a):
                fn(p,a)
                with self.assertRaises(ValueError): b.load_parent(paths)

    def test_19_protection_and_missing_helper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); names=[b.PARENT_SOURCE,b.READOUT_SOURCE]+[f"accepted/{i}" for i in range(650)]
            pins={n:"b"*40 for n in names}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB; pins[b.READOUT_SOURCE]=b.READOUT_BLOB
            for n in names+list(b.OWN): p=root/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(n,encoding="utf-8")
            protected={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1202-len(protected)):
                p=root/f"input{i}"; p.write_text("input",encoding="utf-8"); protected[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent"; directory.mkdir(); path=directory/"summary.json"; path.write_text("summary",encoding="utf-8"); mapping={str(path.resolve()):b.PARENT_SHA}; artifacts=[]
            for n in tuple(a["file"] for a in parent_payload(self.anchors)["artifacts"]):
                p=directory/n; p.write_text("parent",encoding="utf-8"); mapping[str(p.resolve())]="a"*64; artifacts.append(dict(file=n,sha256="a"*64))
            def sha(p): return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            parent=types.ModuleType("parent"); parent.__file__=str(root/b.PARENT_SOURCE); parent.context=lambda:()
            c=NS(audit=NS(sha=sha,git=lambda root,*a:(pins.get(a[1][5:],"c"*40)+"\n").encode(),safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            p=dict(source_blobs=pins,input_sha256=protected,artifacts=artifacts)
            with patch.object(b,"context",return_value=(parent,None,None,None,None,None,c)),patch.object(b,"load_parent",return_value=(p,None,None,None,None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([path]*28,root))),(658,1217))
                c.missing=types.ModuleType("missing"); c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([path]*28,root)

    def test_20_actual_infer_state_counts_and_strict_restore(self):
        m=source_wrapper(frozen(),b.ARMS[1]); m.eval(); m.requires_grad_(False); gain=float(m.gain().detach())
        c=NS(base=NS(fingerprint=fingerprint),p267=NS(counted=counted),core=None); evaluation=NS(evaluate=evaluator,replay_error=replay_error)
        with torch.no_grad(): raw=evaluator(m,self.data)
        anchor=dict(seed=b.SEEDS[0],arm=b.ARMS[1],final_sha256=fingerprint(m),fit=dict(final_gain=gain),raw=raw)
        with contextlib.redirect_stdout(io.StringIO()): r=b.infer_state(m,m.state_dict(),anchor,gain,self.data,None,None,evaluation,None,c)
        self.assertEqual(r["attestations"],{n:dict(calls=81,formula_checks=81) for n in b.PASSES}); self.assertEqual(r["reproduction_errors"],[0.,0.,0.])
        state=copy.deepcopy(m.state_dict()); state["gain_logit"]+=.1
        with self.assertRaisesRegex(ValueError,"strict original"): b.infer_state(m,state,anchor,gain,self.data,None,None,evaluation,None,c)

    def test_21_real_preflight(self):
        models={a:source_wrapper(frozen(),a) for a in b.ARMS}; states=[m.state_dict() for m in models.values()]
        anchors=[dict(final_sha256=fingerprint(m)) for m in models.values()]; gains={b.SEEDS[0]:float(models[b.ARMS[1]].gain().detach())}
        parent=NS(load_bundle=lambda p:states,make_models=lambda seed,c:models)
        tokens=inputs(192)[0][None,None].expand(2,3,-1,-1).clone(); c=NS(base=NS(fingerprint=fingerprint),p267=NS(check_logits=lambda z,n:self.assertEqual(z.shape,(n,256))))
        with patch.object(b,"precheck",return_value=protection()),patch.object(b,"context",return_value=(parent,None,None,None,None,NS(training_tables=lambda *a:(tokens,None)),c)),patch.object(b,"load_parent",return_value=({},self.data,None,None,anchors,gains,None)),contextlib.redirect_stdout(io.StringIO()): b.runtime_preflight(["x"]*28,Path.cwd())

    @contextlib.contextmanager
    def run_fixture(self):
        diag,evaluation,transfer,c=scorers(); c.audit=Audit(); events=[]
        def bundle(path): events.append("bundle"); return [{}]*10
        def infer(*args): events.append("infer"); return self.records[b.identities().index((args[2]["seed"],args[2]["arm"]))]
        def pc(*a): events.append("precheck"); return protection()
        parent=NS(load_bundle=bundle,make_models=lambda seed,c:dict.fromkeys(b.ARMS))
        with patch.object(b,"context",return_value=(parent,NS(no_neural=contextlib.nullcontext),diag,evaluation,transfer,None,c)),patch.object(b,"load_parent",return_value=({},self.data,None,None,self.anchors,self.gains,self.flags)),patch.object(b,"precheck",side_effect=pc),patch.object(b,"infer_state",side_effect=infer): yield events

    def test_22_run_order_bundle_roundtrip(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*28,output_dir=out,expected_head="f"*40)
            self.assertEqual(events[:2],["precheck","bundle"]); self.assertEqual(events.count("bundle"),1); self.assertEqual(events.count("infer"),10)
            q,_=b.verify_artifacts(out,["x"]*28,"f"*40); self.assertEqual(p,q)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*28,output_dir=out,expected_head="f"*40)

    def test_23_hash_and_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*28,output_dir=out,expected_head="f"*40); path=out/"measurements.json"; path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*28,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name); a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*28,"f"*40)

    def test_24_result_no_capability_promotion(self):
        b.validate_result(payload(self.summary))
        for fn in (lambda p:p.update(capability_gate_applicable=True),lambda p:p["validation_summary"].update(train_steps=False),lambda p:p["validation_summary"]["trained_gains"][0].update(gain=.01)):
            p=payload(copy.deepcopy(self.summary)); fn(p)
            with self.assertRaises(ValueError): b.validate_result(p)

    def test_25_all_swaps_fail_still_diagnostic(self):
        records=copy.deepcopy(self.records)
        for r in records: r["raw"]["swapped"]=raw_fixture(self.data,dict.fromkeys(b.TASKS,False))
        _,s=b.analyze(records,self.anchors,self.gains,self.flags,self.data,*scorers()); b.validate_result(payload(s))
        self.assertEqual(s["task_pass_counts"][b.ARMS[0]]["trained"]["quad"],0)

    def test_26_no_model_checkpoint_written(self):
        saved=[]; real=torch.save
        def save(value,path,*args,**kwargs): saved.append(Path(path).name); return real(value,path,*args,**kwargs)
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,patch.object(torch,"save",side_effect=save),contextlib.redirect_stdout(io.StringIO()): b.run(summaries=["x"]*28,output_dir=Path(tmp)/"run",expected_head="f"*40)
        self.assertEqual(saved,["gain-evaluations.pt"])

    def test_27_semantic_regression_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["fixture."+str(i) for i in range(4669)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite=b.regression_suite(Path.cwd()); self.assertEqual(suite.countTestCases(),4669); self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError): b.regression_suite(Path.cwd())

    def test_28_cli_context_guard(self):
        args=["prog","--summaries"]+[str(i) for i in range(28)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",args),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),28)
        parent=NS(context=lambda:tuple(range(7)),regression_modules=lambda root:["f"+str(i) for i in range(186)])
        package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c301_learned_residual_gain=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}): self.assertEqual(b.context(),(parent,1,2,3,4,5,6)); self.assertEqual(len(b.regression_modules(Path.cwd())),187)
        b.guard(Path.cwd(),"f"*40,NS(audit=Audit()))
        with self.assertRaises(ValueError): b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))

    def test_29_utf8_inventory(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="read_text":
                    self.assertTrue(any(k.arg=="encoding" and isinstance(k.value,ast.Constant) and k.value.value=="utf-8" for k in node.keywords))

    def test_30_runner_and_count(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: ast.parse(code)
        self.assertIn("sys.argv[2:30]",blocks[2]); self.assertIn("head = sys.argv[30]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),28)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute")); self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),32)

    def test_31_actual_c278_c301_class_identity(self):
        root=Path(__file__).resolve().parents[1]; space=dict(torch=torch,nn=torch.nn,Counter=Counter,req=b.require,require=b.require,hook_snapshot=b.hook_snapshot,ARMS=b.ARMS,__name__="c302_parent_class_fixture")
        for name,class_name in ((b.READOUT_SOURCE,"MeanFinalDualReadout"),(b.PARENT_SOURCE,"ResidualGain")):
            path=root/name; tree=ast.parse(path.read_text(encoding="utf-8")); cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==class_name)
            exec(compile(ast.Module(body=[cls],type_ignores=[]),str(path),"exec"),space)
        def span(x): out=torch.zeros_like(x,dtype=torch.bool); out[:,1:3]=True; return out
        torch.manual_seed(8); model=space["MeanFinalDualReadout"](Backbone(),1,NS(ResidualHead=Reader),span)
        for arm in b.ARMS:
            wrapper=space["ResidualGain"](copy.deepcopy(model),arm)
            if wrapper.gain_logit is not None:
                with torch.no_grad(): wrapper.gain_logit.fill_(-.6)
            wrapper.eval(); wrapper.requires_grad_(False); before=fingerprint(wrapper); hooks=b.hook_snapshot(wrapper)
            with torch.no_grad():
                reference=wrapper(*inputs())
                for name,_,alpha in b.pass_plan(arm,float(2*torch.tensor(-.6,dtype=torch.float64).sigmoid())):
                    with b.frozen_gain(wrapper.model,alpha): z=wrapper.model(*inputs())
                    if name!=b.PASSES[1]: self.assertTrue(torch.equal(reference,z))
            self.assertEqual(before,fingerprint(wrapper)); self.assertEqual(hooks,b.hook_snapshot(wrapper))

    def test_32_explicit_source_dependency_and_payload(self):
        imports=[n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c301_learned_residual_gain"])
        self.assertEqual(b.manifest()["raw_logit_payload_bytes"],10*3*7776*256*8)


if __name__=="__main__": unittest.main()
