"""C298 control fixtures; substitute models/data do not establish FOLD capability."""
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
from fold_lm.v05_benchmarks import model_c298_component_initialization as b


def dataset():
    data={"TRAIN":[],"HOLDOUT":[]}
    for e,v,language in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (v[1]-v[0])%4==2 else "TRAIN"
        for order,q in itertools.product((e,e[::-1]),e):
            data[split].append(dict(language=language,entities=list(e),values=list(v),permutation=list(order),query=q,target=48+v[e.index(q)]))
    return data


def pairs(rows):
    groups={}
    for i,r in enumerate(rows):
        key=(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups.setdefault(key,[]).append(i)
    return torch.tensor([sorted(groups[k],key=lambda i:rows[i]["query"]) for k in sorted(groups)],dtype=torch.int64)


def schedule(order,rows,builder):
    pair_table=builder(rows); events=torch.empty((800,24,4),dtype=torch.int64)
    for epoch in range(200):
        order_ids=torch.randperm(96,generator=torch.Generator().manual_seed(order+297000+epoch))
        for block in range(4):
            i=epoch*4+block; events[i,:,0]=epoch%2; events[i,:,1]=epoch%3
            events[i,:,2:]=pair_table[order_ids[24*block:24*(block+1)]]
    return events


def render(tokens,targets,events):
    return tokens[events[:,0].repeat_interleave(2),events[:,1].repeat_interleave(2),events[:,2:].flatten()],targets[events[:,2:].flatten()]


def tables(data):
    targets=torch.tensor([r["target"] for r in data["TRAIN"]]); tokens=torch.zeros((2,3,192,48),dtype=torch.int64)
    tokens[:,:,:,0]=targets-48
    return tokens,targets


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.backbone=torch.nn.Embedding(4,4,dtype=torch.float64); self.read=torch.nn.Linear(4,256,dtype=torch.float64)
        self.calls=0; self.rows=0
    def forward(self,tokens,tasks):
        assert tokens.shape==(len(tokens),48) and tasks.shape==(len(tokens),) and not bool(tasks.any())
        self.calls+=1; self.rows+=len(tokens); return self.read(self.backbone(tokens[:,0]))


def fingerprint(model): return b.digest({k:v.detach().tolist() for k,v in model.state_dict().items()})


def check_fit(f,order,data,pair_source):
    assert order==b.ORDER
    b.require(f["steps"]==800 and f["fit_rng"]==b.FIT_RNG and f["optimizer_creations"]==1,"fit contract")
    events=schedule(order,data["TRAIN"],pair_source.pairs_from_rows)
    b.require(torch.equal(events,f["schedule_events"]) and f["event_sha256"]==b.digest(events.tolist()),"fit plan")
    b.require(len(f["ce_history"])==800,"fit losses")


def decompose(matrix):
    x=torch.tensor(matrix,dtype=torch.float64); mean=x.mean(); rows=x.mean(1)-mean; cols=x.mean(0)-mean
    residual=x-mean-rows[:,None]-cols[None,:]
    return dict(matrix=x.tolist(),mean=float(mean),initial_means=x.mean(1).tolist(),order_means=x.mean(0).tolist(),
        initial_ss=float(3*rows.square().sum()),order_ss=float(3*cols.square().sum()),interaction_ss=float(residual.square().sum()),
        total_ss=float((x-mean).square().sum()),interaction=residual.tolist())


def parents():
    return NS(schedule=schedule,check_fit=check_fit,decompose=decompose),NS(pairs_from_rows=pairs,render_batch=render)


def records_fixture():
    data=dataset(); events=schedule(b.ORDER,data["TRAIN"],pairs); records=[]
    for i,bs in enumerate(b.LEVELS):
        for j,rs in enumerate(b.LEVELS):
            raw={t:dict(passed=True,totals=[dict(split=s,rows=n,correct=n,normal_nll=.1) for s,n in (("TRAIN",576),("HOLDOUT",288))]) for t in b.TASKS}
            records.append(dict(backbone_seed=bs,reader_seed=rs,initial_sha256=b.digest([bs,rs]),final_sha256=b.digest([bs,rs,"final"]),
                backbone_initial_sha256="abc"[i]*64,reader_initial_sha256="def"[j]*64,parameters=14256,raw=raw,
                fit=dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=b.FIT_RNG,ce_history=[.1]*800,event_sha256=b.digest(events.tolist()),schedule_events=events),
                forward_calls=881,row_presentations=46176,core_forward_calls=3524,checkpoint_roundtrip=True,reload_max_error=0.,
                replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324))
    anchors=[]
    for i,seed in enumerate(b.LEVELS):
        r=copy.deepcopy(records[4*i]); r.update(initial_seed=seed,order_seed=b.ORDER); anchors.append(r)
    return records,anchors,data


def scoring():
    diag=NS(normalize_task=lambda scored,*_:scored["totals"],partition=lambda rows:dict(rows=rows[0]["rows"],correct=rows[0]["correct"],direct_pass=rows[0]["correct"]==rows[0]["rows"],final_normal_nll=rows[0]["normal_nll"]))
    def replay_error(a,c,*_):
        b.require(b.digest(a)==b.digest(c),"raw mismatch"); return 0.
    evaluation=NS(replay_error=replay_error)
    transfer=NS(score_quad=lambda data,raw,c:raw)
    c=NS(p267=NS(score=lambda data,raw:raw),c270=NS(score=lambda data,raw,p:raw))
    return diag,evaluation,transfer,c


def protection():
    pins={n:"b"*40 for n in b.OWN}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<634: pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1161)}


class Audit:
    @staticmethod
    def sha(path):
        path=Path(path); return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "a"*64
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name): return Path(root)/name
    @staticmethod
    def git(root,*args):
        if args[0]=="rev-parse": return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0]=="branch": return b"feat/sft-target-loss\n"
        return b""


def payload_fixture(summary):
    pins,protected=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)


def fake_factory():
    class Component(torch.nn.Module):
        def __init__(self,n,seed):
            super().__init__(); self.weight=torch.nn.Parameter(torch.randn(n,dtype=torch.float64,generator=torch.Generator().manual_seed(seed)))
    class Model(torch.nn.Module):
        def __init__(self,backbone,seed,*_):
            super().__init__(); self.backbone=backbone; self.read=Component(768,seed+111)
    return NS(c278=NS(MeanFinalDualReadout=Model),factory=NS(new_model=lambda s:Component(13488,s)),
              reader=None,c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint))


class C298Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.det=torch.are_deterministic_algorithms_enabled(); torch.set_num_threads(2)
        cls.records,cls.anchors,cls.data=records_fixture(); cls.parent,cls.pair=parents(); cls.x,cls.y=tables(cls.data)
        cls.metrics,cls.summary=b.analyze(cls.records,cls.anchors,cls.data,cls.parent,cls.pair,*scoring())
        torch.manual_seed(7); cls.initial=Toy(); cls.model=copy.deepcopy(cls.initial)
        with contextlib.redirect_stdout(io.StringIO()): cls.fitted=b.fit(cls.model,cls.data,cls.x,cls.y,b.LEVELS[0],b.LEVELS[0],cls.parent,cls.pair)
    @classmethod
    def tearDownClass(cls):
        torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.det)

    def test_01_manifest(self): b.validate_seal(); self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_manifest(self):
        for value in ("PENDING","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",value),self.assertRaises(ValueError): b.validate_seal()

    def test_03_component_grid_provenance(self):
        c=fake_factory(); grid=b.make_grid(c); self.assertEqual(list(grid),b.identities())
        for seed in b.LEVELS:
            self.assertEqual(len({fingerprint(m.backbone) for (bs,_),m in grid.items() if bs==seed}),1)
            self.assertEqual(len({fingerprint(m.read) for (_,rs),m in grid.items() if rs==seed}),1)
        self.assertEqual(len({fingerprint(m) for m in grid.values()}),9)

    def test_04_no_shared_storage(self):
        grid=b.make_grid(fake_factory()); pointers=[p.data_ptr() for m in grid.values() for p in m.parameters()]
        self.assertEqual(len(pointers),len(set(pointers)))
        before=fingerprint(grid[(b.LEVELS[0],b.LEVELS[1])])
        with torch.no_grad(): grid[(b.LEVELS[0],b.LEVELS[0])].backbone.weight.add_(1)
        self.assertEqual(before,fingerprint(grid[(b.LEVELS[0],b.LEVELS[1])]))

    def test_05_diagonal_reference_initial(self):
        c=fake_factory(); grid=b.make_grid(c)
        for seed in b.LEVELS:
            ref=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,None,None)
            self.assertEqual(fingerprint(grid[(seed,seed)]),fingerprint(ref))

    def test_06_invalid_component_boundary(self):
        c=fake_factory(); real=c.factory.new_model
        c.factory.new_model=lambda s:real(1)
        with self.assertRaisesRegex(ValueError,"distinct backbone"): b.make_grid(c)
        c=fake_factory(); c.factory.new_model=lambda _:torch.nn.Linear(2,2,dtype=torch.float64)
        with self.assertRaisesRegex(ValueError,"component sizes"): b.make_grid(c)

    def test_07_actual800_and_independent_reference(self):
        self.assertEqual((self.model.calls,self.model.rows),(800,38400))
        self.assertLess(self.fitted["ce_history"][-1],self.fitted["ce_history"][0])
        model=copy.deepcopy(self.initial); events=schedule(b.ORDER,self.data["TRAIN"],pairs)
        torch.manual_seed(b.FIT_RNG); optimizer=torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
        losses=[]; model.train()
        for event in events:
            optimizer.zero_grad(set_to_none=True); x,y=render(self.x,self.y,event)
            loss=F.cross_entropy(model(x,torch.zeros(48,dtype=torch.int64)),y); losses.append(float(loss.detach()))
            loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True); optimizer.step()
        self.assertEqual(losses,self.fitted["ce_history"]); self.assertEqual(fingerprint(model),fingerprint(self.model))

    def test_08_rng_and_optimizer(self):
        real=torch.optim.AdamW; made=[]
        def factory(*args,**kwargs):
            optimizer=real(*args,**kwargs); made.append(optimizer); return optimizer
        model=copy.deepcopy(self.initial); torch.manual_seed(999)
        with patch.object(torch.optim,"AdamW",side_effect=factory),contextlib.redirect_stdout(io.StringIO()):
            f=b.fit(model,self.data,self.x,self.y,b.LEVELS[0],b.LEVELS[1],self.parent,self.pair)
        self.assertEqual(len(made),1); self.assertEqual({int(v["step"]) for v in made[0].state.values()},{800})
        self.assertEqual(f["ce_history"],self.fitted["ce_history"])

    def test_09_fit_rejects_labels_and_ids(self):
        y=self.y.clone(); y[0]=99
        with self.assertRaises(ValueError): b.fit(copy.deepcopy(self.initial),self.data,self.x,y,b.LEVELS[0],b.LEVELS[0],self.parent,self.pair)
        with self.assertRaises(ValueError): b.fit(copy.deepcopy(self.initial),self.data,self.x,self.y,298001,b.LEVELS[0],self.parent,self.pair)

    def test_10_component_matching(self):
        b.check_components(self.records)
        for field in ("backbone_initial_sha256","reader_initial_sha256"):
            records=copy.deepcopy(self.records); records[1][field]="z"*64
            with self.assertRaises(ValueError): b.check_components(records)
        with self.assertRaises(ValueError): b.check_components(self.records[:-1])

    def test_11_diagonal_training_identity(self):
        checks=b.diagonal_checks(self.records,self.anchors,self.data,scoring()[1],None); self.assertEqual(len(checks),3)
        for field in ("initial_sha256","final_sha256"):
            records=copy.deepcopy(self.records); records[0][field]="z"*64
            with self.assertRaises(ValueError): b.diagonal_checks(records,self.anchors,self.data,scoring()[1],None)

    def test_12_diagonal_loss_or_order_mismatch(self):
        for fn in (lambda f:f["ce_history"].__setitem__(3,2.),lambda f:f["schedule_events"].__setitem__((0,0,0),9)):
            records=copy.deepcopy(self.records); fn(records[0]["fit"])
            with self.assertRaises(ValueError): b.diagonal_checks(records,self.anchors,self.data,scoring()[1],None)
        anchors=copy.deepcopy(self.anchors); anchors[0]["order_seed"]=297102
        with self.assertRaises(ValueError): b.diagonal_checks(self.records,anchors,self.data,scoring()[1],None)

    def test_13_diagonal_raw_mismatch(self):
        records=copy.deepcopy(self.records); records[0]["raw"]["quad"]["passed"]=False
        with self.assertRaisesRegex(ValueError,"raw mismatch"): b.diagonal_checks(records,self.anchors,self.data,scoring()[1],None)

    def test_14_train_cell_counts_and_frozen_eval(self):
        model=copy.deepcopy(self.initial)
        @contextlib.contextmanager
        def counted(m,core):
            calls=[0,0]; cores=[0]; yield calls,cores; calls[:]=[m.calls,m.rows]; cores[0]=m.calls*4
        def evaluate(m,*_):
            self.assertFalse(m.training); self.assertFalse(any(p.requires_grad for p in m.parameters()))
            with torch.no_grad():
                for _ in range(81): m(torch.zeros((96,48),dtype=torch.int64),torch.zeros(96,dtype=torch.int64))
            return {}
        c=NS(base=NS(fingerprint=fingerprint),p267=NS(counted=counted),core=None)
        with contextlib.redirect_stdout(io.StringIO()):
            r,state=b.train_cell(model,self.data,{},{},self.x,self.y,b.LEVELS[0],b.LEVELS[1],self.parent,self.pair,NS(evaluate=evaluate),None,c)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(881,46176)); self.assertEqual(list(state),list(model.state_dict()))

    def test_15_grid_analysis_and_names(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["grids"])),(9,54,12))
        for row in self.summary["grids"]:
            self.assertIn("backbone_ss",row); self.assertIn("reader_ss",row); self.assertNotIn("order_ss",row)
        b.validate_result(payload_fixture(self.summary))

    def test_16_diagnostic_not_capability(self):
        records=copy.deepcopy(self.records); anchors=copy.deepcopy(self.anchors)
        for r in records+anchors:
            for task in b.TASKS: r["raw"][task]["passed"]=False
        _,summary=b.analyze(records,anchors,self.data,self.parent,self.pair,*scoring())
        b.validate_result(payload_fixture(summary)); self.assertFalse(any(x for row in summary["task_pass_matrices"]["quad"] for x in row))

    def test_17_replay_counts_and_scope_rejected(self):
        for field,value in (("reload_max_error",.1),("forward_calls",800),("checkpoint_roundtrip",False)):
            records=copy.deepcopy(self.records); records[0][field]=value
            with self.assertRaises(ValueError): b.analyze(records,self.anchors,self.data,self.parent,self.pair,*scoring())
        for fn in (lambda p:p.update(capability_gate_applicable=True),lambda p:p["validation_summary"].update(models=False)):
            p=payload_fixture(copy.deepcopy(self.summary)); fn(p)
            with self.assertRaises(ValueError): b.validate_result(p)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c298-fixture")/str(i)/"summary.json").resolve() for i in range(24)]
        parent=NS(parent_hashes=lambda _:tuple(str(i%10)*64 for i in range(23)),validate_result=Mock(),verify_artifacts=Mock(),check_grid=Mock())
        matrices={"two_char":[[True]*3 for _ in range(3)],"triple":[[True]*3 for _ in range(3)],"quad":[[True]*3,[False]*3,[True]*3]}
        payload=dict(experiment_id="C297-v5b-initialization-order-grid",commit_sha=b.PARENT_EXECUTION,status="PASS",
            source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},artifacts=[dict(file=n) for n in b.OUTPUTS],
            validation_summary=dict(task_pass_matrices=matrices,diagnostic_complete=True,capability_gate_applicable=False,grid_matched=True,all_replays=True))
        parent.verify_artifacts.return_value=(payload,{})
        mapping=dict(zip(map(str,paths),(b.PARENT_SHA,*parent.parent_hashes(None)),strict=True))
        objects={n:{"file":n} for n in b.OUTPUTS[1:4]}; c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:objects[p.name]))
        archive=dict(schema="fold-c297-grid-eval-v1",records=copy.deepcopy(self.anchors))
        with patch.object(b,"context",return_value=(parent,None,NS(no_neural=contextlib.nullcontext),None,None,None,None,c)),patch.object(b,"DATA_HASHES",tuple(map(b.digest,objects.values()))),patch.object(torch,"load",return_value=archive):
            yield paths,mapping,parent,payload,archive

    def test_18_all_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,payload,_):
            self.assertEqual(b.load_parent(paths)[0],payload); parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)]; mapping[str(path)]="f"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); mapping[str(path)]=old

    def test_19_parent_and_anchor_contract(self):
        for fn in (lambda p,a:p.update(status="FAIL"),lambda p,a:p["artifacts"].pop(),lambda p,a:a.update(schema="wrong"),lambda p,a:a["records"].pop()):
            with self.loader_fixture() as (paths,_,_,payload,archive):
                fn(payload,archive)
                with self.assertRaises(ValueError): b.load_parent(paths)

    def test_20_protection_and_helper_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); names=[b.PARENT_SOURCE]+[f"accepted/{i}" for i in range(627)]
            pins={n:b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40 for n in names}
            for n in names+list(b.OWN):
                path=root/n; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1146-len(inputs)):
                path=root/f"input{i}"; path.write_text("input",encoding="utf-8"); inputs[str(path.resolve())]=Audit.sha(path)
            directory=root/"parent"; directory.mkdir(); path=directory/"summary.json"; path.write_text("summary",encoding="utf-8")
            mapping={str(path.resolve()):b.PARENT_SHA}; artifacts=[]
            for n in b.OUTPUTS:
                f=directory/n; f.write_text("parent",encoding="utf-8"); mapping[str(f.resolve())]="a"*64; artifacts.append(dict(file=n,sha256="a"*64))
            def sha(p): return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            def git(root,*args): return (pins.get(args[1][5:],"c"*40)+"\n").encode()
            parent=types.ModuleType("parent"); parent.__file__=str(root/b.PARENT_SOURCE); parent.context=lambda:()
            c=NS(audit=NS(sha=sha,git=git,safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            p=dict(source_blobs=pins,input_sha256=inputs,artifacts=artifacts)
            with patch.object(b,"context",return_value=(parent,None,None,None,None,None,None,c)),patch.object(b,"load_parent",return_value=(p,None,None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([path]*24,root))),(634,1161))
                c.missing=types.ModuleType("missing"); c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([path]*24,root)

    def test_21_semantic_suite(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["fixture."+str(i) for i in range(4525)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite=b.regression_suite(Path.cwd()); self.assertEqual(suite.countTestCases(),4525)
            self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})

    def test_22_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"models.pt"; v=dict(schema="fold-c298-components-models-v1",identities=[list(i) for i in b.identities()],states=[{} for _ in range(9)])
            torch.save(v,path); self.assertEqual(len(b.load_bundle(path)),9); v["identities"].reverse(); torch.save(v,path)
            with self.assertRaises(ValueError): b.load_bundle(path)

    @contextlib.contextmanager
    def run_fixture(self):
        records=copy.deepcopy(self.records); diag,evaluation,transfer,c=scoring(); c.audit=Audit(); events=[]
        def train(*args): events.append("train"); return records[b.identities().index((args[6],args[7]))],{}
        def replay(*args): events.append("replay")
        def load(*args): events.append("load_parent"); return {},self.data,{"triple":1},{"quad":1},self.anchors
        def precheck(*args): events.append("precheck"); return protection()
        evaluation.replay_one=replay
        with patch.object(b,"context",return_value=(self.parent,self.pair,NS(no_neural=contextlib.nullcontext),diag,evaluation,transfer,NS(training_tables=lambda *_:(self.x,self.y)),c)),patch.object(b,"precheck",side_effect=precheck),patch.object(b,"load_parent",side_effect=load),patch.object(b,"make_grid",return_value=dict.fromkeys(b.identities())),patch.object(b,"train_cell",side_effect=train):
            yield events

    def test_23_run_order_and_roundtrip(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; payload=b.run(summaries=["x"]*24,output_dir=out,expected_head="f"*40)
            self.assertEqual(events[:2],["precheck","load_parent"]); self.assertEqual(events.count("train"),9); self.assertEqual(events.count("replay"),9)
            self.assertLess(max(i for i,v in enumerate(events) if v=="train"),events.index("replay"))
            result,_=b.verify_artifacts(out,["x"]*24,"f"*40); self.assertEqual(result,payload)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*24,output_dir=out,expected_head="f"*40)

    def test_24_byte_and_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; payload=b.run(summaries=["x"]*24,output_dir=out,expected_head="f"*40)
            path=out/"measurements.json"; path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*24,"f"*40)
            a=next(a for a in payload["artifacts"] if a["file"]==path.name); a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size)
            (out/"summary.json").write_bytes(b.blob(payload))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*24,"f"*40)

    def test_25_preflight_anchors(self):
        c=fake_factory(); grid=b.make_grid(c); anchors=copy.deepcopy(self.anchors)
        for row in anchors: row["initial_sha256"]=fingerprint(grid[(row["initial_seed"],row["initial_seed"])])
        parent=NS(schedule=schedule,INITIALS=b.LEVELS,ORDERS=(297101,297102,297103),FIT_RNG=b.FIT_RNG)
        with patch.object(b,"precheck",return_value=protection()),patch.object(b,"context",return_value=(parent,self.pair,None,None,None,None,NS(training_tables=lambda *_:(self.x,self.y)),c)),patch.object(b,"load_parent",return_value=({},self.data,{},{},anchors)),contextlib.redirect_stdout(io.StringIO()):
            b.runtime_preflight(["x"]*24,Path.cwd())
            anchors[0]["initial_sha256"]="z"*64
            with self.assertRaisesRegex(ValueError,"real diagonal"): b.runtime_preflight(["x"]*24,Path.cwd())

    def test_26_cli(self):
        args=["prog","--summaries"]+[str(i) for i in range(24)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",args),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),24)

    def test_27_cp932_explicit_reads(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="read_text":
                    self.assertTrue(any(k.arg=="encoding" and isinstance(k.value,ast.Constant) and k.value.value=="utf-8" for k in node.keywords))

    def test_28_runner_contract(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: ast.parse(code)
        self.assertIn("sys.argv[2:26]",blocks[2]); self.assertIn("head = sys.argv[26]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),24)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"))
        self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_29_context_and_modules(self):
        parent=NS(context=lambda:tuple(range(8))[1:],regression_modules=lambda root:["f"+str(i) for i in range(182)])
        package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c297_init_order_grid=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):
            self.assertEqual(b.context(),(parent,1,2,3,4,5,6,7)); self.assertEqual(len(b.regression_modules(Path.cwd())),183)

    def test_30_guard(self):
        b.guard(Path.cwd(),"f"*40,NS(audit=Audit()))
        with self.assertRaises(ValueError): b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))

    def test_31_single_direct_import(self):
        tree=ast.parse(Path(b.__file__).read_text(encoding="utf-8"))
        imports=[n.names[0].name for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c297_init_order_grid"])

    def test_32_diagonal_attestation_and_test_count(self):
        payload=payload_fixture(copy.deepcopy(self.summary)); payload["validation_summary"]["diagonal_checks"][0]["matched"]=False
        with self.assertRaises(ValueError): b.validate_result(payload)
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()["own_tests"])


if __name__=="__main__": unittest.main()
