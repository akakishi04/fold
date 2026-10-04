"""C301 software and gradient fixtures; synthetic inputs are not FOLD capability evidence."""
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
from fold_lm.v05_benchmarks import model_c301_learned_residual_gain as b


def data_fixture():
    data={"TRAIN":[],"HOLDOUT":[]}
    for e,v,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (v[1]-v[0])%4==2 else "TRAIN"
        for perm,q in itertools.product((e,e[::-1]),e):
            data[split].append(dict(language=lang,entities=list(e),values=list(v),permutation=list(perm),query=q,target=48+v[e.index(q)]))
    return data


def pairs(rows):
    groups={}
    for i,r in enumerate(rows):
        groups.setdefault((r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"])),[]).append(i)
    return torch.tensor([sorted(groups[k],key=lambda i:rows[i]["query"]) for k in sorted(groups)],dtype=torch.int64)


def render(x,y,e): return x[e[:,0].repeat_interleave(2),e[:,1].repeat_interleave(2),e[:,2:].flatten()],y[e[:,2:].flatten()]
PS=NS(pairs_from_rows=pairs,render_batch=render)


def tables(data):
    y=torch.tensor([r["target"] for r in data["TRAIN"]]); x=torch.zeros((2,3,192,48),dtype=torch.int64); x[:,:,:,0]=y-48
    return x,y


class Encoder(torch.nn.Module):
    def __init__(self): super().__init__(); self.embed=torch.nn.Embedding(4,16,dtype=torch.float64)
    def forward(self,x): return self.embed(x[:,0])


class Backbone(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.local_encoder=Encoder(); self.core=torch.nn.Linear(16,16,dtype=torch.float64)
        self.readout_norm=torch.nn.LayerNorm(16,dtype=torch.float64); self.classifier=torch.nn.Linear(16,256,dtype=torch.float64)
        self.padding=torch.nn.Parameter(torch.zeros(13488-sum(p.numel() for p in self.parameters()),dtype=torch.float64))
    def forward(self,x,t):
        z=self.local_encoder(x)
        for _ in range(4): z=torch.tanh(self.core(z))
        return self.classifier(self.readout_norm(z))


class Reader(torch.nn.Module):
    def __init__(self,*a):
        super().__init__()
        for name in ("key","query","output"): setattr(self,name,torch.nn.Linear(16,16,bias=False,dtype=torch.float64))


class Toy(torch.nn.Module):
    def __init__(self,backbone=None,*args):
        super().__init__(); self.backbone=backbone if backbone is not None else Backbone(); self.read=Reader(); self.fail=False; self.offset=0.
    def forward(self,x,t):
        def add(module,args):
            if self.fail: raise RuntimeError("injected failure")
            return (args[0]+self.read.output(args[0])+self.offset,)
        h=self.backbone.readout_norm.register_forward_pre_hook(add)
        try: return self.backbone(x,t)
        finally: h.remove()


def fingerprint(m): return b.tensor_hash(m.state_dict().items())

def factory():
    def new(seed): torch.manual_seed(seed); return Backbone()
    return NS(c278=NS(MeanFinalDualReadout=Toy),factory=NS(new_model=new),reader=None,c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint))


def fit_fixture(seed,arm,data):
    e=b.schedule(b.order_for(seed),data["TRAIN"],PS)
    return dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=b.FIT_RNG,ce_history=[.1]*800,
        gain_history=[1.]*800,gain_logit_history=[0.]*800,final_gain=1.,final_gain_logit=0.,
        first_common_gradient_sha256="a"*64,event_sha256=b.digest(e.tolist()),schedule_events=e)


def records_fixture():
    data=data_fixture(); records=[]
    for seed,arm in b.identities():
        raw={t:dict(passed=True,totals=[dict(split=s,rows=n,correct=n,normal_nll=.1) for s,n in (("TRAIN",576),("HOLDOUT",288))]) for t in b.TASKS}
        records.append(dict(seed=seed,arm=arm,initial_sha256="a"*64,initial_common_sha256="b"*64,final_sha256="c"*64,
            parameters=b.manifest()["parameters"][arm],fit=fit_fixture(seed,arm,data),raw=raw,forward_calls=881,row_presentations=46176,
            core_forward_calls=3524,formula_checks=881,checkpoint_roundtrip=True,reload_max_error=0.,
            replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324))
    return records,data


def scorers():
    diag=NS(normalize_task=lambda s,*_:s["totals"],partition=lambda rows:dict(rows=rows[0]["rows"],correct=rows[0]["correct"],
        direct_pass=rows[0]["rows"]==rows[0]["correct"],final_normal_nll=rows[0]["normal_nll"]))
    return diag,NS(score_quad=lambda data,raw,c:raw),NS(p267=NS(score=lambda data,raw:raw),c270=NS(score=lambda data,raw,p:raw))


def protection():
    pins={n:"b"*40 for n in b.OWN}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB; pins[b.READOUT_SOURCE]=b.READOUT_BLOB
    while len(pins)<652: pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1202)}


class Audit:
    @staticmethod
    def sha(path):
        p=Path(path); return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name): return Path(root)/name
    @staticmethod
    def git(root,*args):
        if args[0]=="rev-parse": return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0]=="branch": return b"feat/sft-target-loss\n"
        return b""


def payload(summary):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],
        validation_summary=summary,gate_f_candidate=False,production_adoption=False)


def evaluate(model,data,*args):
    assert not model.training and not any(p.requires_grad for p in model.parameters())
    with torch.no_grad():
        return [model(torch.zeros((96,48),dtype=torch.int64),torch.zeros(96,dtype=torch.int64)).detach().clone() for _ in range(81)]


def replay_error(a,c,*args):
    error=max(float((x-y).abs().max()) for x,y in zip(a,c,strict=True))
    b.require(error<=1e-9 and all(torch.equal(x.argmax(1),y.argmax(1)) for x,y in zip(a,c,strict=True)),"replay")
    return error


class C301Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.det=torch.are_deterministic_algorithms_enabled(); torch.set_num_threads(2)
        cls.records,cls.data=records_fixture(); cls.x,cls.y=tables(cls.data); cls.metrics,cls.summary=b.analyze(cls.records,cls.data,PS,*scorers())
        torch.manual_seed(4); cls.initial=Toy(); cls.models={a:b.ResidualGain(copy.deepcopy(cls.initial),a) for a in b.ARMS}; cls.fits={}
        with contextlib.redirect_stdout(io.StringIO()):
            for arm,m in cls.models.items(): cls.fits[arm]=b.fit(m,cls.data,cls.x,cls.y,b.SEEDS[0],arm,PS)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.det)

    def test_01_manifest(self): b.validate_seal(); self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seals(self):
        for value in ("UNSEALED","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",value),self.assertRaises(ValueError): b.validate_seal()

    def test_03_gain_initial_and_range(self):
        m=b.ResidualGain(Toy(),b.ARMS[1]); self.assertEqual(float(m.gain().detach()),1.)
        for value in (-100.,-3.,0.,3.,100.):
            with torch.no_grad(): m.gain_logit.fill_(value)
            self.assertTrue(0.<=float(m.gain().detach())<=2.)

    def test_04_unknown_arm(self):
        with self.assertRaises(ValueError): b.ResidualGain(Toy(),"select_best")

    def test_05_initial_output_and_common_gradient_identity(self):
        models=[copy.deepcopy(self.initial)]+[b.ResidualGain(copy.deepcopy(self.initial),a) for a in b.ARMS]; outputs=[]; grads=[]
        for m in models:
            z=m(self.x[0,0,:48],torch.zeros(48,dtype=torch.int64)); F.cross_entropy(z,self.y[:48]).backward(); outputs.append(z)
            common=m.model if isinstance(m,b.ResidualGain) else m; grads.append(b.tensor_hash((n,p.grad) for n,p in common.named_parameters()))
        self.assertTrue(all(torch.equal(outputs[0],z) for z in outputs[1:])); self.assertEqual(len(set(grads)),1)
        self.assertIsNotNone(models[-1].gain_logit.grad)

    def test_06_finite_difference_gain(self):
        m=b.ResidualGain(copy.deepcopy(self.initial),b.ARMS[1]); x=self.x[0,0,:8]; y=self.y[:8]; t=torch.zeros(8,dtype=torch.int64)
        loss=F.cross_entropy(m(x,t),y); grad=torch.autograd.grad(loss,m.gain_logit)[0]
        with torch.no_grad():
            m.gain_logit.fill_(1e-6); plus=F.cross_entropy(m(x,t),y); m.gain_logit.fill_(-1e-6); minus=F.cross_entropy(m(x,t),y)
        self.assertAlmostEqual(float(grad),float((plus-minus)/(2e-6)),places=7)

    def test_07_both_summands_keep_gradients(self):
        m=b.ResidualGain(copy.deepcopy(self.initial),b.ARMS[1]); m.gain_logit.data.fill_(.8)
        F.cross_entropy(m(self.x[0,0,:8],torch.zeros(8,dtype=torch.int64)),self.y[:8]).backward()
        for p in (m.backbone.core.weight,m.read.output.weight,m.gain_logit):
            self.assertIsNotNone(p.grad); self.assertTrue(bool(torch.isfinite(p.grad).all())); self.assertGreater(float(p.grad.abs().sum()),0.)

    def test_08_hook_restoration_success(self):
        m=b.ResidualGain(copy.deepcopy(self.initial),b.ARMS[1]); before=b.hook_snapshot(m.model)
        for _ in range(3): m(self.x[0,0,:8],torch.zeros(8,dtype=torch.int64))
        self.assertEqual(m.verified_calls,3); self.assertEqual(b.hook_snapshot(m.model),before)

    def test_09_hook_restoration_exception(self):
        m=b.ResidualGain(copy.deepcopy(self.initial),b.ARMS[1]); m.model.fail=True; before=b.hook_snapshot(m.model)
        with self.assertRaisesRegex(RuntimeError,"injected"): m(self.x[0,0,:8],torch.zeros(8,dtype=torch.int64))
        self.assertEqual(b.hook_snapshot(m.model),before); m.model.fail=False; m(self.x[0,0,:8],torch.zeros(8,dtype=torch.int64))

    def test_10_wrong_sum_fails(self):
        m=b.ResidualGain(copy.deepcopy(self.initial),b.ARMS[1]); m.model.offset=.5
        with self.assertRaisesRegex(ValueError,"actual C278 sum"): m(self.x[0,0,:8],torch.zeros(8,dtype=torch.int64))

    def test_11_dtype_and_gain_nonfinite(self):
        m=b.ResidualGain(copy.deepcopy(self.initial),b.ARMS[1]).float()
        with self.assertRaisesRegex(ValueError,"summand contract"): m(self.x[0,0,:8],torch.zeros(8,dtype=torch.int64))
        m=b.ResidualGain(copy.deepcopy(self.initial),b.ARMS[1]); m.gain_logit.data.fill_(float("nan"))
        with self.assertRaisesRegex(ValueError,"gain bounds"): m(self.x[0,0,:8],torch.zeros(8,dtype=torch.int64))

    def test_12_nonunit_formula_reference(self):
        m=b.ResidualGain(copy.deepcopy(self.initial),b.ARMS[1]); m.gain_logit.data.fill_(.7); captures=[]
        h=m.backbone.readout_norm.register_forward_pre_hook(lambda mod,args:captures.append(args[0]))
        m.model(self.x[0,0,:8],torch.zeros(8,dtype=torch.int64)); h.remove(); r=captures[0]
        expected=m.backbone.classifier(m.backbone.readout_norm(m.gain()*r+m.read.output(r)))
        actual=m(self.x[0,0,:8],torch.zeros(8,dtype=torch.int64)); self.assertTrue(torch.equal(actual,expected))

    def test_13_factory_counts_and_storage(self):
        models=b.make_models(b.SEEDS[0],factory())
        self.assertEqual([sum(p.numel() for p in m.parameters()) for m in models.values()],[14256,14257])
        self.assertEqual(len({fingerprint(m.model) for m in models.values()}),1)
        ptrs=[p.data_ptr() for m in models.values() for p in m.parameters()]; self.assertEqual(len(ptrs),len(set(ptrs)))

    def test_14_factory_bad_seed_or_capacity(self):
        with self.assertRaises(ValueError): b.make_models(1,factory())
        c=factory(); c.factory.new_model=lambda s:torch.nn.Linear(1,1,dtype=torch.float64)
        with self.assertRaises(ValueError): b.make_models(b.SEEDS[0],c)

    def test_15_all_five_schedules_and_exposures(self):
        hashes=[]
        for order in b.ORDERS:
            e=b.schedule(order,self.data["TRAIN"],PS); hashes.append(b.digest(e.tolist())); self.assertEqual(e.shape,(800,24,4))
            for length in (0,1): self.assertTrue(torch.equal(torch.bincount(e[e[:,:,0]==length][:,2:].flatten(),minlength=192),torch.full((192,),100)))
        self.assertEqual(len(set(hashes)),5)

    def test_16_pairs_and_determinism(self):
        e=b.schedule(b.ORDERS[0],self.data["TRAIN"],PS)
        self.assertTrue(torch.equal(e,b.schedule(b.ORDERS[0],self.data["TRAIN"],PS)))
        for event in e[0]:
            a,c=[self.data["TRAIN"][i] for i in event[2:]]
            self.assertEqual(a["values"],c["values"]); self.assertNotEqual(a["query"],c["query"])
        with self.assertRaises(ValueError): b.schedule(1,self.data["TRAIN"],PS)

    def test_17_actual_fit_both800(self):
        for arm,f in self.fits.items():
            b.check_fit(f,b.SEEDS[0],arm,self.data,PS); self.assertEqual(self.models[arm].verified_calls,800)
            self.assertLess(f["ce_history"][-1],f["ce_history"][0]); self.assertFalse(self.models[arm].training)
        self.assertEqual(self.fits[b.ARMS[0]]["first_common_gradient_sha256"],self.fits[b.ARMS[1]]["first_common_gradient_sha256"])
        self.assertEqual(self.fits[b.ARMS[0]]["gain_history"],[1.]*800)

    def test_18_fit_rng_and_one_optimizer(self):
        real=torch.optim.AdamW; made=[]
        def make(*a,**kw): o=real(*a,**kw); made.append(o); return o
        m=b.ResidualGain(copy.deepcopy(self.initial),b.ARMS[1]); torch.manual_seed(123)
        with patch.object(torch.optim,"AdamW",side_effect=make),contextlib.redirect_stdout(io.StringIO()): f=b.fit(m,self.data,self.x,self.y,b.SEEDS[0],b.ARMS[1],PS)
        self.assertEqual(len(made),1); self.assertEqual({int(v["step"]) for v in made[0].state.values()},{800})
        self.assertEqual(f["ce_history"],self.fits[b.ARMS[1]]["ce_history"]); self.assertEqual(fingerprint(m),fingerprint(self.models[b.ARMS[1]]))

    def test_19_fit_inputs(self):
        m=b.ResidualGain(Toy(),b.ARMS[0]); y=self.y.clone(); y[0]=99
        with self.assertRaises(ValueError): b.fit(m,self.data,self.x,y,b.SEEDS[0],b.ARMS[0],PS)
        with self.assertRaises(ValueError): b.fit(m,self.data,self.x,self.y,b.SEEDS[0],b.ARMS[1],PS)

    def test_20_gain_history_and_budget_tamper(self):
        for fn in (lambda f:f["gain_history"].__setitem__(2,2.),lambda f:f.update(steps=799),lambda f:f.update(final_gain=99.)):
            f=copy.deepcopy(self.fits[b.ARMS[1]]); fn(f)
            with self.assertRaises(ValueError): b.check_fit(f,b.SEEDS[0],b.ARMS[1],self.data,PS)

    def test_21_paired_gradient_order_guard(self):
        b.check_pair(self.records[:2]); rows=copy.deepcopy(self.records[:2]); rows[1]["fit"]["first_common_gradient_sha256"]="z"*64
        with self.assertRaises(ValueError): b.check_pair(rows)

    def test_22_analysis_inventory(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["contrasts"])),(10,60,30))
        b.validate_result(payload(self.summary))

    def test_23_all_five_gate(self):
        rows=copy.deepcopy(self.records); rows[1]["raw"]["quad"]["passed"]=False
        _,s=b.analyze(rows,self.data,PS,*scorers()); self.assertFalse(s["candidate_gate"]); self.assertEqual(s["task_pass_counts"]["quad"][b.ARMS[1]],4)
        b.validate_result(payload(s))

    def test_24_wrong_replay_and_counts(self):
        for key,value in (("reload_max_error",.1),("parameters",10),("formula_checks",0)):
            rows=copy.deepcopy(self.records); rows[0][key]=value
            with self.assertRaises(ValueError): b.analyze(rows,self.data,PS,*scorers())

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c301-fixture")/str(i)/"summary.json").resolve() for i in range(27)]
        objects={n:{"file":n} for n in b.OUTPUTS[1:4]}; p299=NS(parent_hashes=lambda p:tuple(str(i%10)*64 for i in range(25)),context=lambda:(None,),DATA_HASHES=tuple(map(b.digest,objects.values())))
        parent=NS(PARENT_SHA="e"*64,context=lambda:(p299,),expected_matrices=lambda:{"fixed":True},OUTPUTS=tuple("abcd"),verify_artifacts=Mock(),validate_result=Mock())
        p=dict(experiment_id="C300-v5b-frozen-readout-term-ablation",commit_sha=b.PARENT_EXECUTION,status="PASS",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB,b.READOUT_SOURCE:b.READOUT_BLOB},
            artifacts=[dict(file=n) for n in parent.OUTPUTS],validation_summary=dict(diagnostic_complete=True,capability_gate_applicable=False,all_weights_preserved=True,all_hooks_restored=True,
                task_pass_matrices={"full_before":{"fixed":True},"full_after":{"fixed":True}}))
        parent.verify_artifacts.return_value=(p,{})
        mapping=dict(zip(map(str,paths),b.parent_hashes(parent),strict=True)); c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:objects[p.name]))
        with patch.object(b,"context",return_value=(parent,NS(no_neural=contextlib.nullcontext),None,None,None,None,c)): yield paths,mapping,parent,p

    def test_25_all27_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,p):
            self.assertEqual(b.load_parent(paths)[0],p); parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)]; mapping[str(path)]="f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); mapping[str(path)]=old

    def test_26_parent_schema_scope(self):
        for fn in (lambda p:p.update(status="FAIL"),lambda p:p["artifacts"].pop(),lambda p:p["validation_summary"].update(all_weights_preserved=False)):
            with self.loader_fixture() as (paths,_,_,p):
                fn(p)
                with self.assertRaises(ValueError): b.load_parent(paths)

    def test_27_protection_counts_and_helpers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); names=[b.PARENT_SOURCE,b.READOUT_SOURCE]+[f"accepted/{i}" for i in range(644)]; pins={n:"b"*40 for n in names}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB; pins[b.READOUT_SOURCE]=b.READOUT_BLOB
            for n in names+list(b.OWN): p=root/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(n,encoding="utf-8")
            protected={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1191-len(protected)):
                p=root/f"input{i}"; p.write_text("input",encoding="utf-8"); protected[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent"; directory.mkdir(); path=directory/"summary.json"; path.write_text("summary",encoding="utf-8"); mapping={str(path.resolve()):b.PARENT_SHA}; artifacts=[]
            for n in ("a","b","c","d"):
                p=directory/n; p.write_text("parent",encoding="utf-8"); mapping[str(p.resolve())]="a"*64; artifacts.append(dict(file=n,sha256="a"*64))
            def sha(p): return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            parent=types.ModuleType("parent"); parent.__file__=str(root/b.PARENT_SOURCE); parent.context=lambda:()
            c=NS(audit=NS(sha=sha,git=lambda root,*a:(pins.get(a[1][5:],"c"*40)+"\n").encode(),safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            p=dict(source_blobs=pins,input_sha256=protected,artifacts=artifacts)
            with patch.object(b,"context",return_value=(parent,None,None,None,None,None,c)),patch.object(b,"pair_source",return_value=PS),patch.object(b,"load_parent",return_value=(p,None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([path]*27,root))),(652,1202))
                c.missing=types.ModuleType("missing"); c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([path]*27,root)

    @contextlib.contextmanager
    def run_fixture(self):
        records=copy.deepcopy(self.records); diag,transfer,c=scorers(); c.audit=Audit(); events=[]
        def train(*a): events.append("train"); return records[b.identities().index((a[6],a[7]))],{}
        def replay(*a): events.append("replay")
        def pc(*a): events.append("precheck"); return protection()
        with patch.object(b,"context",return_value=(None,NS(no_neural=contextlib.nullcontext),diag,None,transfer,NS(training_tables=lambda *_:(self.x,self.y)),c)),patch.object(b,"pair_source",return_value=PS),patch.object(b,"precheck",side_effect=pc),patch.object(b,"load_parent",return_value=({},self.data,{"triple":True},{"quad":True})),patch.object(b,"make_models",return_value=dict.fromkeys(b.ARMS)),patch.object(b,"train_one",side_effect=train),patch.object(b,"replay_one",side_effect=replay): yield events

    def test_28_run_order_loader_and_roundtrip(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*27,output_dir=out,expected_head="f"*40)
            self.assertEqual(events[0],"precheck"); self.assertEqual(events.count("train"),10); self.assertEqual(events.count("replay"),10)
            self.assertLess(max(i for i,v in enumerate(events) if v=="train"),events.index("replay")); q,_=b.verify_artifacts(out,["x"]*27,"f"*40); self.assertEqual(p,q)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*27,output_dir=out,expected_head="f"*40)

    def test_29_byte_and_semantic_tampering(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*27,output_dir=out,expected_head="f"*40); path=out/"measurements.json"; path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*27,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name); a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size); (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*27,"f"*40)

    def test_30_semantic_suite(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["fixture."+str(i) for i in range(4637)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite=b.regression_suite(Path.cwd()); self.assertEqual(suite.countTestCases(),4637); self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})

    def test_31_cli_bundle(self):
        argv=["prog","--summaries"]+[str(i) for i in range(27)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),27)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"m.pt"; v=dict(schema="fold-c301-gain-models-v1",identities=[list(i) for i in b.identities()],states=[{} for _ in range(10)])
            torch.save(v,p); self.assertEqual(len(b.load_bundle(p)),10); v["identities"].reverse(); torch.save(v,p)
            with self.assertRaises(ValueError): b.load_bundle(p)

    def test_32_cp932_and_explicit_reads(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="read_text":
                    self.assertTrue(any(k.arg=="encoding" and isinstance(k.value,ast.Constant) and k.value.value=="utf-8" for k in node.keywords))

    def test_33_runner_indices_order(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: ast.parse(code)
        self.assertIn("sys.argv[2:29]",blocks[2]); self.assertIn("head = sys.argv[29]",blocks[2]); self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),27)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute")); self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_34_context_helper_dispatch(self):
        ps=object(); p299=NS(context=lambda:(0,1,ps)); parent=NS(context=lambda:(p299,1,2,3,4,5,6),regression_modules=lambda _:["f"+str(i) for i in range(185)])
        package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c300_frozen_readout_terms=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):
            self.assertEqual(b.context(),(parent,1,2,3,4,5,6)); self.assertIs(b.pair_source(parent),ps); self.assertEqual(len(b.regression_modules(Path.cwd())),186)

    def test_35_real_toy_train_and_replay_counts(self):
        model=b.ResidualGain(copy.deepcopy(self.initial),b.ARMS[1]); c=NS(base=NS(fingerprint=fingerprint)); evaluation=NS(evaluate=evaluate,replay_error=replay_error)
        with contextlib.redirect_stdout(io.StringIO()): r,state=b.train_one(model,self.data,None,None,self.x,self.y,b.SEEDS[0],b.ARMS[1],PS,evaluation,None,c)
        self.assertEqual((r["forward_calls"],r["row_presentations"],r["core_forward_calls"]),(881,46176,3524))
        other=b.ResidualGain(copy.deepcopy(self.initial),b.ARMS[1]); b.replay_one(other,state,r,self.data,None,None,evaluation,None,c)
        self.assertEqual(other.verified_calls,81); self.assertEqual(r["reload_max_error"],0.)

    def test_36_strict_gain_restore(self):
        model=copy.deepcopy(self.models[b.ARMS[1]]); model.requires_grad_(False); evaluation=NS(evaluate=evaluate,replay_error=replay_error); c=NS(base=NS(fingerprint=fingerprint))
        record=dict(final_sha256=fingerprint(model),fit=self.fits[b.ARMS[1]],raw=evaluate(model,self.data))
        state=copy.deepcopy(model.state_dict()); state["gain_logit"]+=.2
        with self.assertRaisesRegex(ValueError,"strict checkpoint"): b.replay_one(model,state,record,self.data,None,None,evaluation,None,c)

    def test_37_real_preflight_forward_gradient(self):
        with patch.object(b,"precheck",return_value=protection()),patch.object(b,"pair_source",return_value=PS),patch.object(b,"context",return_value=(None,None,None,None,None,NS(training_tables=lambda *_:(self.x,self.y)),factory())),patch.object(b,"load_parent",return_value=({},self.data,None,None)),contextlib.redirect_stdout(io.StringIO()): b.runtime_preflight(["x"]*27,Path.cwd())

    def test_38_result_scope_and_count_tamper(self):
        for fn in (lambda p:p.update(gate_f_candidate=True),lambda p:p["validation_summary"].update(models=False),lambda p:p["validation_summary"].update(candidate_gate=False)):
            p=payload(copy.deepcopy(self.summary)); fn(p)
            with self.assertRaises(ValueError): b.validate_result(p)

    def test_39_guard_imports_count(self):
        b.guard(Path.cwd(),"f"*40,NS(audit=Audit()))
        with self.assertRaises(ValueError): b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))
        imports=[n.names[0].name for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c300_frozen_readout_terms"]); self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),40)

    def test_40_actual_c278_class_gradient_protocol(self):
        path=Path(__file__).resolve().parents[1]/b.READOUT_SOURCE
        tree=ast.parse(path.read_text(encoding="utf-8")); node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="MeanFinalDualReadout")
        space=dict(torch=torch,nn=torch.nn,Counter=Counter,req=b.require,__name__="c301_actual_class_fixture")
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),"exec"),space)
        class WideEncoder(torch.nn.Module):
            def __init__(self): super().__init__(); self.embed=torch.nn.Embedding(259,16,dtype=torch.float64)
            def forward(self,x): return (self.embed(x),)
        class WideCore(torch.nn.Module):
            def __init__(self): super().__init__(); self.linear=torch.nn.Linear(16,16,dtype=torch.float64)
            def forward(self,state,local,route_index): return torch.tanh(self.linear(state)+local*.1)
        class WideBackbone(torch.nn.Module):
            def __init__(self):
                super().__init__(); self.local_encoder=WideEncoder(); self.core=WideCore(); self.readout_norm=torch.nn.LayerNorm(16,dtype=torch.float64); self.classifier=torch.nn.Linear(16,256,dtype=torch.float64)
                self.config=NS(width=16,max_tokens=48,next_route=0,instruction_route=1,internal_steps=2)
                self.padding=torch.nn.Parameter(torch.zeros(13488-sum(p.numel() for p in self.parameters()),dtype=torch.float64))
            def forward(self,x,t):
                valid=x!=256; local=self.local_encoder(x)[0]*valid[:,:,None]; state=local
                for _ in range(2):
                    nxt=self.core(state,local,route_index=0); self.core(state,local,route_index=1); state=nxt
                return self.classifier(self.readout_norm(state[torch.arange(len(x)),valid.sum(1)-1]))
        def span(x): mask=torch.zeros_like(x,dtype=torch.bool); mask[:,1:3]=True; return mask
        torch.manual_seed(123); base=space["MeanFinalDualReadout"](WideBackbone(),1,NS(ResidualHead=Reader),span)
        x=torch.full((4,48),256,dtype=torch.int64); x[:,:4]=torch.tensor([0,1,2,258]); y=torch.tensor([48,49,50,51]); t=torch.zeros(4,dtype=torch.int64)
        models=[copy.deepcopy(base)]+[b.ResidualGain(copy.deepcopy(base),a) for a in b.ARMS]; grads=[]; outputs=[]
        for m in models:
            z=m(x,t); F.cross_entropy(z,y).backward(); outputs.append(z.detach()); common=m.model if isinstance(m,b.ResidualGain) else m
            grads.append(b.tensor_hash((n,p.grad) for n,p in common.named_parameters()))
        self.assertTrue(all(torch.equal(outputs[0],z) for z in outputs[1:])); self.assertEqual(len(set(grads)),1)
        candidate=models[-1]; self.assertIsNotNone(candidate.gain_logit.grad); self.assertTrue(bool(torch.isfinite(candidate.gain_logit.grad)))
        self.assertEqual(b.hook_snapshot(candidate.model),b.hook_snapshot(base))


if __name__=="__main__": unittest.main()
