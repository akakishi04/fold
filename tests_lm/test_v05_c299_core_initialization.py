"""C299 software-control fixtures; not evidence of actual FOLD generalization."""
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
from fold_lm.v05_benchmarks import model_c299_core_initialization as b


def dataset():
    data={"TRAIN":[],"HOLDOUT":[]}
    for e,v,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (v[1]-v[0])%4==2 else "TRAIN"
        for perm,q in itertools.product((e,e[::-1]),e):
            data[split].append(dict(language=lang,entities=list(e),values=list(v),permutation=list(perm),query=q,target=48+v[e.index(q)]))
    return data


def pairs(rows):
    groups={}
    for i,r in enumerate(rows):
        key=(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups.setdefault(key,[]).append(i)
    return torch.tensor([sorted(groups[k],key=lambda i:rows[i]["query"]) for k in sorted(groups)],dtype=torch.int64)


def schedule(order,rows,builder):
    events=torch.empty((800,24,4),dtype=torch.int64);pp=builder(rows)
    for epoch in range(200):
        ids=torch.randperm(96,generator=torch.Generator().manual_seed(order+297000+epoch))
        for block in range(4):
            i=epoch*4+block;events[i,:,0]=epoch%2;events[i,:,1]=epoch%3;events[i,:,2:]=pp[ids[24*block:24*(block+1)]]
    return events


def render(tokens,targets,events):
    rr=events[:,2:].flatten()
    return tokens[events[:,0].repeat_interleave(2),events[:,1].repeat_interleave(2),rr],targets[rr]


def tables(data):
    y=torch.tensor([r["target"] for r in data["TRAIN"]]);x=torch.zeros((2,3,192,48),dtype=torch.int64);x[:,:,:,0]=y-48
    return x,y


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__();self.backbone=torch.nn.Module();self.backbone.embed=torch.nn.Embedding(4,4,dtype=torch.float64)
        self.backbone.core=torch.nn.Linear(4,4,dtype=torch.float64);self.read=torch.nn.Linear(4,256,dtype=torch.float64);self.calls=0;self.rows=0
    def forward(self,x,t):
        assert x.shape==(len(x),48) and t.shape==(len(x),) and not bool(t.any())
        self.calls+=1;self.rows+=len(x)
        return self.read(torch.tanh(self.backbone.core(self.backbone.embed(x[:,0]))))


def fingerprint(m):return b.digest({k:v.detach().tolist() for k,v in m.state_dict().items()})


def check_fit(f,order,data,ps):
    b.require(order==b.ORDER and f["fit_rng"]==b.FIT_RNG and f["steps"]==800 and f["optimizer_creations"]==1,"fit contract")
    expected=schedule(order,data["TRAIN"],ps.pairs_from_rows)
    b.require(torch.equal(expected,f["schedule_events"]) and f["event_sha256"]==b.digest(expected.tolist()),"fit plan")
    b.require(len(f["ce_history"])==800,"fit losses")


def decompose(matrix):
    x=torch.tensor(matrix,dtype=torch.float64);mean=x.mean();rows=x.mean(1)-mean;cols=x.mean(0)-mean;res=x-mean-rows[:,None]-cols[None,:]
    return dict(matrix=x.tolist(),mean=float(mean),initial_means=x.mean(1).tolist(),order_means=x.mean(0).tolist(),
        initial_ss=float(3*rows.square().sum()),order_ss=float(3*cols.square().sum()),interaction_ss=float(res.square().sum()),
        total_ss=float((x-mean).square().sum()),interaction=res.tolist())


def parents():return NS(schedule=schedule,check_fit=check_fit,decompose=decompose),NS(pairs_from_rows=pairs,render_batch=render)


def records_fixture():
    data=dataset();events=schedule(b.ORDER,data["TRAIN"],pairs);records=[]
    for i,rest in enumerate(b.LEVELS):
        for j,core in enumerate(b.LEVELS):
            raw={t:dict(passed=True,totals=[dict(split=s,rows=n,correct=n,normal_nll=.1) for s,n in (("TRAIN",576),("HOLDOUT",288))]) for t in b.TASKS}
            records.append(dict(remaining_seed=rest,core_seed=core,reader_seed=b.READER_SEED,initial_sha256=b.digest([rest,core]),final_sha256=b.digest([rest,core,"final"]),
                remaining_initial_sha256="abc"[i]*64,core_initial_sha256="def"[j]*64,reader_initial_sha256="g"*64,parameters=14256,raw=raw,
                fit=dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=b.FIT_RNG,ce_history=[.1]*800,event_sha256=b.digest(events.tolist()),schedule_events=events),
                forward_calls=881,row_presentations=46176,core_forward_calls=3524,checkpoint_roundtrip=True,reload_max_error=0.,
                replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324))
    anchors=[]
    for i,seed in enumerate(b.LEVELS):
        r=copy.deepcopy(records[4*i]);r.update(backbone_seed=seed,reader_seed=b.READER_SEED);anchors.append(r)
    return records,anchors,data


def scoring():
    diag=NS(normalize_task=lambda s,*_:s["totals"],partition=lambda rr:dict(rows=rr[0]["rows"],correct=rr[0]["correct"],direct_pass=rr[0]["rows"]==rr[0]["correct"],final_normal_nll=rr[0]["normal_nll"]))
    def replay_error(a,c,*_):b.require(b.digest(a)==b.digest(c),"raw mismatch");return 0.
    return diag,NS(replay_error=replay_error),NS(score_quad=lambda data,raw,c:raw),NS(p267=NS(score=lambda data,raw:raw),c270=NS(score=lambda data,raw,p:raw))


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<640:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1176)}


class Audit:
    @staticmethod
    def sha(path):
        path=Path(path);return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "a"*64
    @staticmethod
    def read_json(path):return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name):return Path(root)/name
    @staticmethod
    def git(root,*args):
        if args[0]=="rev-parse":return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0]=="branch":return b"feat/sft-target-loss\n"
        return b""


def payload_fixture(summary):
    pins,protected=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)


class FakeComponent(torch.nn.Module):
    def __init__(self,n,seed):
        super().__init__();self.weight=torch.nn.Parameter(torch.randn(n,dtype=torch.float64,generator=torch.Generator().manual_seed(seed)))


def fake_factory():
    class Backbone(torch.nn.Module):
        def __init__(self,seed):
            super().__init__();self.rest=FakeComponent(10160,seed);self.core=FakeComponent(3328,seed+7)
    class Model(torch.nn.Module):
        def __init__(self,backbone,seed,*_):
            super().__init__();self.backbone=backbone;self.read=FakeComponent(768,seed+11)
    return NS(c278=NS(MeanFinalDualReadout=Model),factory=NS(new_model=Backbone),reader=None,c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint))


class C299Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();cls.det=torch.are_deterministic_algorithms_enabled();torch.set_num_threads(2)
        cls.records,cls.anchors,cls.data=records_fixture();cls.gp,cls.ps=parents();cls.x,cls.y=tables(cls.data)
        cls.metrics,cls.summary=b.analyze(cls.records,cls.anchors,cls.data,cls.gp,cls.ps,*scoring())
        torch.manual_seed(7);cls.initial=Toy();cls.model=copy.deepcopy(cls.initial)
        with contextlib.redirect_stdout(io.StringIO()):cls.fitted=b.fit(cls.model,cls.data,cls.x,cls.y,b.LEVELS[0],b.LEVELS[0],cls.gp,cls.ps)
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads);torch.use_deterministic_algorithms(cls.det)

    def test_01_seal(self):b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seal(self):
        for value in ("PENDING","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",value),self.assertRaises(ValueError):b.validate_seal()

    def test_03_component_provenance(self):
        c=fake_factory();grid=b.make_grid(c);self.assertEqual(list(grid),b.identities())
        for seed in b.LEVELS:
            self.assertEqual(len({b.remaining_fingerprint(m.backbone) for (s,_),m in grid.items() if s==seed}),1)
            self.assertEqual(len({fingerprint(m.backbone.core) for (_,s),m in grid.items() if s==seed}),1)
        self.assertEqual(len({fingerprint(m.read) for m in grid.values()}),1);self.assertEqual(len({fingerprint(m) for m in grid.values()}),9)

    def test_04_independent_storage(self):
        grid=b.make_grid(fake_factory());ptrs=[p.data_ptr() for m in grid.values() for p in m.parameters()];self.assertEqual(len(ptrs),len(set(ptrs)))
        before=fingerprint(grid[(b.LEVELS[0],b.LEVELS[1])])
        with torch.no_grad():grid[(b.LEVELS[0],b.LEVELS[0])].backbone.core.weight.add_(1)
        self.assertEqual(before,fingerprint(grid[(b.LEVELS[0],b.LEVELS[1])]))

    def test_05_fixed_reader_diagonal(self):
        c=fake_factory();grid=b.make_grid(c)
        for seed in b.LEVELS:
            ref=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),b.READER_SEED,None,None)
            self.assertEqual(fingerprint(ref),fingerprint(grid[(seed,seed)]))

    def test_06_remaining_fingerprint_boundary(self):
        m=Toy();a=b.remaining_fingerprint(m.backbone)
        with torch.no_grad():m.backbone.core.weight.add_(1)
        self.assertEqual(a,b.remaining_fingerprint(m.backbone))
        with torch.no_grad():m.backbone.embed.weight.add_(1)
        self.assertNotEqual(a,b.remaining_fingerprint(m.backbone))
        with self.assertRaises(ValueError):b.remaining_fingerprint(torch.nn.Module())

    def test_07_invalid_capacity_and_levels(self):
        c=fake_factory();real=c.factory.new_model;c.factory.new_model=lambda _:real(1)
        with self.assertRaises(ValueError):b.make_grid(c)
        c=fake_factory();c.factory.new_model=lambda _:torch.nn.Linear(2,2,dtype=torch.float64)
        with self.assertRaises((ValueError,AttributeError)):b.make_grid(c)

    def test_08_actual_fit_independent_reference(self):
        self.assertEqual((self.model.calls,self.model.rows),(800,38400));self.assertLess(self.fitted["ce_history"][-1],self.fitted["ce_history"][0])
        model=copy.deepcopy(self.initial);torch.manual_seed(b.FIT_RNG);opt=torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.);history=[]
        for event in schedule(b.ORDER,self.data["TRAIN"],pairs):
            opt.zero_grad(set_to_none=True);x,y=render(self.x,self.y,event);loss=F.cross_entropy(model(x,torch.zeros(48,dtype=torch.int64)),y)
            history.append(float(loss.detach()));loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True);opt.step()
        self.assertEqual(history,self.fitted["ce_history"]);self.assertEqual(fingerprint(model),fingerprint(self.model))

    def test_09_fixed_rng_and_optimizer(self):
        real=torch.optim.AdamW;made=[]
        def factory(*a,**kw):o=real(*a,**kw);made.append(o);return o
        m=copy.deepcopy(self.initial);torch.manual_seed(999)
        with patch.object(torch.optim,"AdamW",side_effect=factory),contextlib.redirect_stdout(io.StringIO()):f=b.fit(m,self.data,self.x,self.y,b.LEVELS[1],b.LEVELS[2],self.gp,self.ps)
        self.assertEqual(len(made),1);self.assertEqual({int(v["step"]) for v in made[0].state.values()},{800});self.assertEqual(f["ce_history"],self.fitted["ce_history"])

    def test_10_fit_inputs(self):
        y=self.y.clone();y[0]=99
        with self.assertRaises(ValueError):b.fit(copy.deepcopy(self.initial),self.data,self.x,y,b.LEVELS[0],b.LEVELS[0],self.gp,self.ps)
        with self.assertRaises(ValueError):b.fit(copy.deepcopy(self.initial),self.data,self.x,self.y,299001,b.LEVELS[0],self.gp,self.ps)

    def test_11_grid_tamper(self):
        b.check_grid(self.records)
        for field in ("remaining_initial_sha256","core_initial_sha256","reader_initial_sha256"):
            r=copy.deepcopy(self.records);r[1][field]="z"*64
            with self.assertRaises(ValueError):b.check_grid(r)
        with self.assertRaises(ValueError):b.check_grid(self.records[:-1])

    def test_12_diagonal_identity(self):
        self.assertEqual(len(b.diagonal_checks(self.records,self.anchors,self.data,scoring()[1],None)),3)
        for key in ("initial_sha256","final_sha256"):
            r=copy.deepcopy(self.records);r[0][key]="z"*64
            with self.assertRaises(ValueError):b.diagonal_checks(r,self.anchors,self.data,scoring()[1],None)

    def test_13_diagonal_losses_and_anchors(self):
        for fn in (lambda f:f["ce_history"].__setitem__(1,9.),lambda f:f["schedule_events"].__setitem__((0,0,0),9)):
            r=copy.deepcopy(self.records);fn(r[0]["fit"])
            with self.assertRaises(ValueError):b.diagonal_checks(r,self.anchors,self.data,scoring()[1],None)
        a=copy.deepcopy(self.anchors);a[0]["reader_seed"]=297002
        with self.assertRaises(ValueError):b.diagonal_checks(self.records,a,self.data,scoring()[1],None)

    def test_14_raw_mismatch(self):
        r=copy.deepcopy(self.records);r[0]["raw"]["quad"]["passed"]=False
        with self.assertRaisesRegex(ValueError,"raw mismatch"):b.diagonal_checks(r,self.anchors,self.data,scoring()[1],None)

    def test_15_actual_train_cell(self):
        m=copy.deepcopy(self.initial)
        @contextlib.contextmanager
        def counted(model,_):
            calls=[0,0];cores=[0];yield calls,cores;calls[:]=[model.calls,model.rows];cores[0]=model.calls*4
        def evaluate(model,*_):
            self.assertFalse(model.training);self.assertFalse(any(p.requires_grad for p in model.parameters()))
            with torch.no_grad():
                for _ in range(81):model(torch.zeros((96,48),dtype=torch.int64),torch.zeros(96,dtype=torch.int64))
            return {}
        c=NS(base=NS(fingerprint=fingerprint),p267=NS(counted=counted),core=None)
        with contextlib.redirect_stdout(io.StringIO()):r,state=b.train_cell(m,self.data,{},{},self.x,self.y,b.LEVELS[0],b.LEVELS[1],self.gp,self.ps,NS(evaluate=evaluate),None,c)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(881,46176));self.assertEqual(list(state),list(m.state_dict()))

    def test_16_analysis_and_field_names(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["grids"])),(9,54,12))
        for row in self.summary["grids"]:self.assertIn("core_ss",row);self.assertIn("remaining_ss",row);self.assertNotIn("order_ss",row)
        b.validate_result(payload_fixture(self.summary))

    def test_17_capability_not_diagnostic(self):
        r=copy.deepcopy(self.records);a=copy.deepcopy(self.anchors)
        for rec in r+a:
            for t in b.TASKS:rec["raw"][t]["passed"]=False
        _,s=b.analyze(r,a,self.data,self.gp,self.ps,*scoring());b.validate_result(payload_fixture(s));self.assertFalse(any(x for row in s["task_pass_matrices"]["quad"] for x in row))

    def test_18_replay_workload_scope(self):
        for field,value in (("reload_max_error",.1),("forward_calls",800),("checkpoint_roundtrip",False)):
            r=copy.deepcopy(self.records);r[0][field]=value
            with self.assertRaises(ValueError):b.analyze(r,self.anchors,self.data,self.gp,self.ps,*scoring())
        for fn in (lambda p:p.update(capability_gate_applicable=True),lambda p:p["validation_summary"].update(models=False),lambda p:p["validation_summary"]["diagonal_checks"][0].update(matched=False)):
            p=payload_fixture(copy.deepcopy(self.summary));fn(p)
            with self.assertRaises(ValueError):b.validate_result(p)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c299-fixture")/str(i)/"summary.json").resolve() for i in range(25)]
        gp=NS(parent_hashes=lambda _:tuple(str(i%10)*64 for i in range(23)))
        parent=NS(PARENT_SHA="e"*64,context=lambda:(gp,None),validate_result=Mock(),verify_artifacts=Mock(),check_components=Mock())
        matrices={"two_char":[[True]*3 for _ in b.LEVELS],"triple":[[True]*3 for _ in b.LEVELS],"quad":[[True]*3,[False]*3,[True]*3]}
        p=dict(experiment_id="C298-v5b-component-initialization-grid",commit_sha=b.PARENT_EXECUTION,status="PASS",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},artifacts=[dict(file=n) for n in b.OUTPUTS],
            validation_summary=dict(task_pass_matrices=matrices,diagnostic_complete=True,capability_gate_applicable=False,components_matched=True,all_replays=True))
        parent.verify_artifacts.return_value=(p,{})
        mapping=dict(zip(map(str,paths),b.parent_hashes(parent),strict=True));objects={n:{"fixture":n} for n in b.OUTPUTS[1:4]}
        c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:objects[p.name]));archive=dict(schema="fold-c298-components-eval-v1",records=copy.deepcopy(self.anchors))
        with patch.object(b,"context",return_value=(parent,None,None,NS(no_neural=contextlib.nullcontext),None,None,None,None,c)),patch.object(b,"DATA_HASHES",tuple(map(b.digest,objects.values()))),patch.object(torch,"load",return_value=archive):
            yield paths,mapping,parent,p,archive

    def test_19_all_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,p,_):
            self.assertEqual(b.load_parent(paths)[0],p);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="f"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_20_parent_contract(self):
        for fn in (lambda p,a:p.update(status="FAIL"),lambda p,a:p["artifacts"].pop(),lambda p,a:a.update(schema="wrong"),lambda p,a:a["records"].pop()):
            with self.loader_fixture() as (paths,_,_,p,a):
                fn(p,a)
                with self.assertRaises(ValueError):b.load_parent(paths)

    def test_21_protection_and_missing_helper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);names=[b.PARENT_SOURCE]+[f"accepted/{i}" for i in range(633)];pins={n:b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40 for n in names}
            for n in names+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1161-len(inputs)):
                p=root/f"input{i}";p.write_text("input",encoding="utf-8");inputs[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent";directory.mkdir();path=directory/"summary.json";path.write_text("summary",encoding="utf-8");mapping={str(path.resolve()):b.PARENT_SHA};artifacts=[]
            for n in b.OUTPUTS:
                p=directory/n;p.write_text("parent",encoding="utf-8");mapping[str(p.resolve())]="a"*64;artifacts.append(dict(file=n,sha256="a"*64))
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            def git(root,*a):return (pins.get(a[1][5:],"c"*40)+"\n").encode()
            parent=types.ModuleType("parent");parent.__file__=str(root/b.PARENT_SOURCE);parent.context=lambda:()
            c=NS(audit=NS(sha=sha,git=git,safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            payload=dict(source_blobs=pins,input_sha256=inputs,artifacts=artifacts)
            with patch.object(b,"context",return_value=(parent,None,None,None,None,None,None,None,c)),patch.object(b,"load_parent",return_value=(payload,None,None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([path]*25,root))),(640,1176))
                c.missing=types.ModuleType("missing");c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"):b.precheck([path]*25,root)

    def test_22_semantic_suite(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(4557)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual(suite.countTestCases(),4557);self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())

    def test_23_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"m.pt";v=dict(schema="fold-c299-core-models-v1",identities=[list(i) for i in b.identities()],states=[{} for _ in range(9)])
            torch.save(v,path);self.assertEqual(len(b.load_bundle(path)),9);v["identities"].reverse();torch.save(v,path)
            with self.assertRaises(ValueError):b.load_bundle(path)

    @contextlib.contextmanager
    def run_fixture(self):
        records=copy.deepcopy(self.records);diag,evaluation,transfer,c=scoring();c.audit=Audit();events=[]
        def train(*a):events.append("train");return records[b.identities().index((a[6],a[7]))],{}
        def replay(*a):events.append("replay")
        def load(*a):events.append("load_parent");return {},self.data,{"triple":1},{"quad":1},self.anchors
        def pc(*a):events.append("precheck");return protection()
        evaluation.replay_one=replay
        with patch.object(b,"context",return_value=(None,self.gp,self.ps,NS(no_neural=contextlib.nullcontext),diag,evaluation,transfer,NS(training_tables=lambda *_:(self.x,self.y)),c)),patch.object(b,"precheck",side_effect=pc),patch.object(b,"load_parent",side_effect=load),patch.object(b,"make_grid",return_value=dict.fromkeys(b.identities())),patch.object(b,"train_cell",side_effect=train):yield events

    def test_24_run_order_roundtrip(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*25,output_dir=out,expected_head="f"*40)
            self.assertEqual(events[:2],["precheck","load_parent"]);self.assertEqual(events.count("train"),9);self.assertEqual(events.count("replay"),9)
            self.assertLess(max(i for i,v in enumerate(events) if v=="train"),events.index("replay"));q,_=b.verify_artifacts(out,["x"]*25,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*25,output_dir=out,expected_head="f"*40)

    def test_25_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*25,output_dir=out,expected_head="f"*40);path=out/"measurements.json";path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*25,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size);(out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*25,"f"*40)

    def test_26_runtime_diagonal_preflight(self):
        c=fake_factory();grid=b.make_grid(c);anchors=copy.deepcopy(self.anchors)
        for r in anchors:r["initial_sha256"]=fingerprint(grid[(r["backbone_seed"],r["backbone_seed"])])
        parent=NS(LEVELS=b.LEVELS,ORDER=b.ORDER,FIT_RNG=b.FIT_RNG);pins,_=protection();pins[Path(__file__).name]="a"*40
        with patch.object(b,"precheck",return_value=(pins,{})),patch.object(b,"context",return_value=(parent,self.gp,self.ps,None,None,None,None,NS(training_tables=lambda *_:(self.x,self.y)),c)),patch.object(b,"load_parent",return_value=({},self.data,{},{},anchors)),contextlib.redirect_stdout(io.StringIO()):
            with tempfile.TemporaryDirectory() as tmp:b.runtime_preflight(["x"]*25,Path(tmp))
            pins.pop("tests_lm/"+Path(__file__).name)
            with self.assertRaisesRegex(ValueError,"core implementation pin"):b.runtime_preflight(["x"]*25,Path(__file__).resolve().parents[1])
            pins["tests_lm/"+Path(__file__).name]="b"*40
            b.runtime_preflight(["x"]*25,Path(__file__).resolve().parents[1])
            anchors[0]["initial_sha256"]="z"*64
            with self.assertRaisesRegex(ValueError,"real diagonal"):b.runtime_preflight(["x"]*25,Path.cwd())

    def test_27_cli(self):
        argv=["prog","--summaries"]+[str(i) for i in range(25)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:b.main();self.assertEqual(len(run.call_args.kwargs["summaries"]),25)

    def test_28_cp932_and_explicit_reads(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN:self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="read_text":
                    self.assertTrue(any(k.arg=="encoding" and isinstance(k.value,ast.Constant) and k.value.value=="utf-8" for k in node.keywords))

    def test_29_runner(self):
        root=Path(__file__).resolve().parents[1];runner=(root/b.OWN[2]).read_text(encoding="utf-8");launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:27]",blocks[2]);self.assertIn("head = sys.argv[27]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),25)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"));self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_30_context_modules(self):
        parent=NS(context=lambda:tuple(range(8)),regression_modules=lambda _:["f"+str(i) for i in range(183)])
        package=types.ModuleType("fold_lm.v05_benchmarks");package.model_c298_component_initialization=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):self.assertEqual(b.context(),(parent,*range(8)));self.assertEqual(len(b.regression_modules(Path.cwd())),184)

    def test_31_guard(self):
        b.guard(Path.cwd(),"f"*40,NS(audit=Audit()))
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))

    def test_32_imports_and_count(self):
        tree=ast.parse(Path(b.__file__).read_text(encoding="utf-8"))
        imports=[n.names[0].name for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c298_component_initialization"]);self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),32)


if __name__=="__main__":unittest.main()
