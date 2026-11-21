"""C297 fixtures test mechanics, not FOLD binding capability or real parent artifacts."""
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
from fold_lm.v05_benchmarks import model_c297_init_order_grid as b


def dataset():
    data={"TRAIN":[],"HOLDOUT":[]}
    for e,v,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (v[1]-v[0])%4==2 else "TRAIN"
        for order,q in itertools.product((e,e[::-1]),e):
            data[split].append(dict(id=str((lang,e,v,order,q)),language=lang,entities=list(e),values=list(v),permutation=list(order),query=q,target=48+v[e.index(q)]))
    return data


def pair_builder(rows):
    groups={}
    for i,r in enumerate(rows):
        key=(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups.setdefault(key,[]).append(i)
    return torch.tensor([sorted(groups[k],key=lambda i:rows[i]["query"]) for k in sorted(groups)],dtype=torch.int64)


def render(tokens,targets,events):
    rows=events[:,2:].flatten(); ll=events[:,0].repeat_interleave(2); pp=events[:,1].repeat_interleave(2)
    return tokens[ll,pp,rows],targets[rows]


def tables(data):
    y=torch.tensor([r["target"] for r in data["TRAIN"]]); x=torch.zeros((2,3,192,48),dtype=torch.int64)
    x[:,:,:,0]=y-48
    return x,y


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.backbone=torch.nn.Embedding(4,4,dtype=torch.float64); self.read=torch.nn.Linear(4,256,dtype=torch.float64)
        self.calls=0; self.rows=0
    def forward(self,tokens,tasks):
        assert tokens.shape==(len(tokens),48) and tasks.shape==(len(tokens),) and not bool(tasks.any())
        self.calls+=1; self.rows+=len(tokens)
        return self.read(self.backbone(tokens[:,0]))


def fingerprint(model): return b.digest({k:v.detach().tolist() for k,v in model.state_dict().items()})


def fixtures():
    data=dataset(); parent=NS(pairs_from_rows=pair_builder,render_batch=render); records=[]
    for i,initial in enumerate(b.INITIALS):
        for order in b.ORDERS:
            events=b.schedule(order,data["TRAIN"],pair_builder)
            raw={t:dict(passed=True,totals=[dict(split=s,profile=str(p),language=l,rows=n,pairs=n//2,correct=n,collapsed_pairs=0,normal_nll=.1)
                 for s,n in (("TRAIN",96),("HOLDOUT",48)) for p in range(3) for l in ("en","ja")]) for t in b.TASKS}
            records.append(dict(initial_seed=initial,order_seed=order,initial_sha256="abc"[i]*64,final_sha256="d"*64,parameters=14256,
                fit=dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=b.FIT_RNG,ce_history=[1.]*800,
                    event_sha256=b.digest(events.tolist()),schedule_events=events),raw=raw,
                forward_calls=881,row_presentations=46176,core_forward_calls=3524,checkpoint_roundtrip=True,reload_max_error=0.,
                replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324))
    return records,data,parent


def scorers():
    def partition(rows):
        n=sum(r["rows"] for r in rows); correct=sum(r["correct"] for r in rows)
        return dict(rows=n,correct=correct,direct_pass=n==correct,final_normal_nll=sum(r["normal_nll"]*r["rows"] for r in rows)/n)
    diag=NS(normalize_task=lambda s,*_:s["totals"],partition=partition)
    transfer=NS(score_quad=lambda data,raw,c:raw)
    c=NS(p267=NS(score=lambda data,raw:raw),c270=NS(score=lambda data,raw,p:raw))
    return diag,transfer,c


def protection():
    pins={n:"b"*40 for n in b.OWN}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<628: pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1146)}


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


def result_fixture(summary):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)


class C297Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads(); cls.det=torch.are_deterministic_algorithms_enabled(); torch.set_num_threads(2)
        cls.records,cls.data,cls.parent=fixtures(); cls.x,cls.y=tables(cls.data)
        cls.metrics,cls.summary=b.analyze(cls.records,cls.data,cls.parent,*scorers())
        torch.manual_seed(77); cls.initial=Toy(); cls.model=copy.deepcopy(cls.initial)
        with contextlib.redirect_stdout(io.StringIO()):
            cls.fitted=b.fit(cls.model,cls.data,cls.x,cls.y,b.INITIALS[0],b.ORDERS[0],cls.parent)
    @classmethod
    def tearDownClass(cls):
        torch.set_num_threads(cls.threads); torch.use_deterministic_algorithms(cls.det)

    def test_01_manifest(self):
        b.validate_seal(); self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seals(self):
        for value in ("UNSEALED","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",value), self.assertRaises(ValueError): b.validate_seal()

    def test_03_complete_grid(self):
        self.assertEqual(b.identities(),list(itertools.product(b.INITIALS,b.ORDERS)))
        b.check_grid(self.records)
        with self.assertRaises(ValueError): b.check_grid(self.records[:-1])

    def test_04_exposures_and_private_rng(self):
        for order in b.ORDERS:
            torch.manual_seed(9); state=torch.get_rng_state().clone(); events=b.schedule(order,self.data["TRAIN"],pair_builder)
            self.assertTrue(torch.equal(state,torch.get_rng_state())); self.assertEqual(events.shape,(800,24,4))
            for ll in range(2): self.assertTrue(torch.equal(torch.bincount(events[events[:,:,0]==ll][:,2:].flatten()),torch.full((192,),100)))

    def test_05_orders_distinct_but_same_multiset(self):
        from collections import Counter
        plans=[b.schedule(o,self.data["TRAIN"],pair_builder) for o in b.ORDERS]
        self.assertEqual(len({b.digest(p.tolist()) for p in plans}),3)
        self.assertTrue(all(Counter(map(tuple,p.reshape(-1,4).tolist()))==Counter(map(tuple,plans[0].reshape(-1,4).tolist())) for p in plans))

    def test_06_blocked_reference(self):
        p=b.schedule(b.ORDERS[0],self.data["TRAIN"],pair_builder); pairs=pair_builder(self.data["TRAIN"])
        for epoch in (0,1,5,199):
            perm=torch.randperm(96,generator=torch.Generator().manual_seed(b.ORDERS[0]+297000+epoch))
            self.assertTrue(torch.equal(p[epoch*4:epoch*4+4,:,2:].reshape(96,2),pairs[perm]))
            self.assertTrue(bool((p[epoch*4:epoch*4+4,:,0]==epoch%2).all()))
            self.assertTrue(bool((p[epoch*4:epoch*4+4,:,1]==epoch%3).all()))

    def test_07_wrong_schedule_inputs(self):
        with self.assertRaises(ValueError): b.schedule(296001,self.data["TRAIN"],pair_builder)
        with self.assertRaises(ValueError): b.schedule(b.ORDERS[0],self.data["TRAIN"],lambda _:torch.zeros((95,2),dtype=torch.int64))

    def test_08_actual_fit_and_rng_replay(self):
        self.assertEqual((self.model.calls,self.model.rows),(800,38400)); self.assertLess(self.fitted["ce_history"][-1],self.fitted["ce_history"][0])
        other=copy.deepcopy(self.initial); torch.manual_seed(9999)
        with contextlib.redirect_stdout(io.StringIO()): f=b.fit(other,self.data,self.x,self.y,b.INITIALS[0],b.ORDERS[0],self.parent)
        self.assertEqual(f["ce_history"],self.fitted["ce_history"]); self.assertEqual(fingerprint(other),fingerprint(self.model))

    def test_09_one_optimizer_and_different_order(self):
        real=torch.optim.AdamW; made=[]
        def factory(*a,**kw):
            opt=real(*a,**kw); made.append(opt); return opt
        other=copy.deepcopy(self.initial)
        with patch.object(torch.optim,"AdamW",side_effect=factory),contextlib.redirect_stdout(io.StringIO()):
            f=b.fit(other,self.data,self.x,self.y,b.INITIALS[0],b.ORDERS[1],self.parent)
        self.assertEqual(len(made),1); self.assertEqual({int(v["step"]) for v in made[0].state.values()},{800})
        self.assertNotEqual(f["event_sha256"],self.fitted["event_sha256"]); self.assertEqual(f["fit_rng"],b.FIT_RNG)

    def test_10_fit_guards(self):
        for fn in (lambda f:f.update(fit_rng=1),lambda f:f["schedule_events"].__setitem__((0,0,0),9),lambda f:f["ce_history"].__setitem__(2,float("nan"))):
            f=copy.deepcopy(self.fitted); fn(f)
            with self.assertRaises(ValueError): b.check_fit(f,b.ORDERS[0],self.data,self.parent)
        y=self.y.clone(); y[0]=99
        with self.assertRaises(ValueError): b.fit(copy.deepcopy(self.initial),self.data,self.x,y,b.INITIALS[0],b.ORDERS[0],self.parent)

    def test_11_initial_storage(self):
        class Fake(torch.nn.Module):
            def __init__(self,*_): super().__init__(); self.weight=torch.nn.Parameter(torch.ones(14256,dtype=torch.float64))
        c=NS(c278=NS(MeanFinalDualReadout=Fake),factory=NS(new_model=lambda _:None),reader=None,c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint))
        models=b.make_models(b.INITIALS[0],c); self.assertEqual(len({m.weight.data_ptr() for m in models}),3)
        self.assertEqual(len({fingerprint(m) for m in models}),1)
        with self.assertRaises(ValueError): b.make_models(b.ORDERS[0],c)

    def test_12_grid_matching_tamper(self):
        for key,value in (("initial_sha256","e"*64),("event_sha256","0"*64)):
            rr=copy.deepcopy(self.records)
            if key=="event_sha256": rr[3]["fit"][key]=value
            else: rr[1][key]=value
            with self.assertRaises(ValueError): b.check_grid(rr)

    def test_13_decomposition_constant(self):
        s=b.decompose([[2.]*3]*3)
        self.assertEqual((s["initial_ss"],s["order_ss"],s["interaction_ss"],s["total_ss"]),(0.,0.,0.,0.))

    def test_14_decomposition_additive(self):
        s=b.decompose([[i+2*j for j in range(3)] for i in range(3)])
        self.assertAlmostEqual(s["interaction_ss"],0.); self.assertAlmostEqual(s["initial_ss"],6.); self.assertAlmostEqual(s["order_ss"],24.)

    def test_15_interaction_only(self):
        s=b.decompose([[1.,-1.,0.],[-1.,1.,0.],[0.,0.,0.]])
        self.assertEqual(s["initial_ss"],0.); self.assertEqual(s["order_ss"],0.); self.assertEqual(s["interaction_ss"],4.)
        with self.assertRaises(ValueError): b.decompose([[float("nan")]*3]*3)

    def test_16_analysis_inventory(self):
        self.assertEqual((len(self.metrics),len(self.summary["cell_results"]),len(self.summary["final_partitions"]),len(self.summary["grids"])),(9,9,54,12))
        self.assertTrue(all(x for row in self.summary["task_pass_matrices"]["quad"] for x in row))
        b.validate_result(result_fixture(self.summary))

    def test_17_all_failed_still_diagnostic_not_capability(self):
        records=copy.deepcopy(self.records)
        for r in records:
            for t in b.TASKS: r["raw"][t]["passed"]=False
        _,s=b.analyze(records,self.data,self.parent,*scorers())
        p=result_fixture(s); b.validate_result(p)
        self.assertFalse(p["capability_gate_applicable"]); self.assertFalse(any(x for row in s["task_pass_matrices"]["quad"] for x in row))

    def test_18_replay_integrity(self):
        for key,value in (("reload_max_error",.1),("forward_calls",800),("checkpoint_roundtrip",False)):
            records=copy.deepcopy(self.records); records[0][key]=value
            with self.assertRaises(ValueError): b.analyze(records,self.data,self.parent,*scorers())

    def test_19_train_cell_actual_count_and_freeze(self):
        model=copy.deepcopy(self.initial)
        @contextlib.contextmanager
        def counted(m,core):
            calls=[0,0]; cores=[0]; yield calls,cores; calls[:]=[m.calls,m.rows]; cores[0]=4*m.calls
        def evaluate(m,*a):
            self.assertFalse(m.training); self.assertFalse(any(p.requires_grad for p in m.parameters()))
            with torch.no_grad():
                for _ in range(81): m(torch.zeros((96,48),dtype=torch.int64),torch.zeros(96,dtype=torch.int64))
            return {}
        c=NS(base=NS(fingerprint=fingerprint),p267=NS(counted=counted),core=None)
        with contextlib.redirect_stdout(io.StringIO()):
            r,state=b.train_cell(model,self.data,{},{},self.x,self.y,b.INITIALS[0],b.ORDERS[0],self.parent,NS(evaluate=evaluate),None,c)
        self.assertEqual((r["forward_calls"],r["row_presentations"]),(881,46176)); self.assertEqual(list(state),list(model.state_dict()))

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c297-fixture")/str(i)/"summary.json").resolve() for i in range(23)]
        old=(NS(PARENT_SHA="8"*64),NS(SUMMARY_SHAS=("9"*64,)*15))
        p291=NS(PARENT_SHA="7"*64,context=lambda:old); p292=NS(PARENT_SHA="6"*64)
        p293=NS(PARENT_SHA="5"*64,context=lambda:(p292,p291)); audit=NS(PARENT_SHA="4"*64,no_neural=contextlib.nullcontext)
        p295=NS(PARENT_SHA="3"*64,context=lambda:(audit,p293))
        parent=NS(PARENT_SHA="2"*64,context=lambda:(p295,audit),validate_result=Mock(),verify_artifacts=Mock())
        payload=dict(experiment_id="C296-v5b-render-balanced-minibatches",commit_sha=b.PARENT_EXECUTION,status="FAIL",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
            artifacts=[dict(file=n,sha256="a"*64) for n in b.OUTPUTS],validation_summary=dict(quad_pass_counts=dict(blocked=2,balanced=3),all_pairs_matched=True,all_replays=True,candidate_gate=False))
        parent.verify_artifacts.return_value=(payload,{})
        mapping=dict(zip(map(str,paths),b.parent_hashes(parent),strict=True))
        objects={n:{"fixture":n} for n in b.OUTPUTS[1:4]}
        c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:objects[p.name]))
        with patch.object(b,"context",return_value=(parent,audit,None,None,None,None,c)),patch.object(b,"DATA_HASHES",tuple(map(b.digest,objects.values()))):
            yield paths,mapping,parent,payload

    def test_20_all_23_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,payload):
            self.assertEqual(b.load_parent(paths)[0],payload)
            parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                before=mapping[str(path)]; mapping[str(path)]="0"*64; parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called(); mapping[str(path)]=before

    def test_21_parent_contract(self):
        for fn in (lambda p:p.update(status="PASS"),lambda p:p["artifacts"].pop(),lambda p:p["validation_summary"].update(all_replays=False)):
            with self.loader_fixture() as (paths,_,_,p):
                fn(p)
                with self.assertRaises(ValueError): b.load_parent(paths)

    def test_22_protection_and_missing_helper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); names=[b.PARENT_SOURCE]+[f"accepted/{i}" for i in range(621)]
            pins={n:b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40 for n in names}
            for n in names+list(b.OWN):
                path=root/n; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1131-len(inputs)):
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
            with patch.object(b,"context",return_value=(parent,None,None,None,None,None,c)),patch.object(b,"load_parent",return_value=(p,None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([path]*23,root))),(628,1146))
                c.missing=types.ModuleType("missing"); c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"): b.precheck([path]*23,root)

    def test_23_semantic_suite(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__(); self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["fixture."+str(i) for i in range(4493)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite=b.regression_suite(Path.cwd()); self.assertEqual(suite.countTestCases(),4493)
            self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})

    def test_24_result_flags_and_bundle(self):
        for fn in (lambda p:p.update(capability_gate_applicable=True),lambda p:p["validation_summary"].update(models=False),lambda p:p["validation_summary"]["grids"].pop()):
            p=result_fixture(copy.deepcopy(self.summary)); fn(p)
            with self.assertRaises(ValueError): b.validate_result(p)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"models.pt"; v=dict(schema="fold-c297-grid-models-v1",identities=[list(i) for i in b.identities()],states=[{} for _ in range(9)])
            torch.save(v,path); self.assertEqual(len(b.load_bundle(path)),9); v["identities"].reverse(); torch.save(v,path)
            with self.assertRaises(ValueError): b.load_bundle(path)

    @contextlib.contextmanager
    def run_fixture(self):
        records=copy.deepcopy(self.records); diag,transfer,c=scorers(); c.audit=Audit(); events=[]
        def train(*a): events.append("train"); return records[b.identities().index((a[6],a[7]))],{}
        def replay(*a): events.append("replay")
        def load(*a): events.append("load_parent"); return {},self.data,{"triple":1},{"quad":1}
        def precheck(*a): events.append("precheck"); return protection()
        audit=NS(no_neural=contextlib.nullcontext)
        with patch.object(b,"context",return_value=(self.parent,audit,diag,NS(replay_one=replay),transfer,NS(training_tables=lambda *_:(self.x,self.y)),c)),patch.object(b,"precheck",side_effect=precheck),patch.object(b,"load_parent",side_effect=load),patch.object(b,"make_models",return_value=[None]*3),patch.object(b,"train_cell",side_effect=train):
            yield events

    def test_25_production_order_roundtrip_no_overwrite(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*23,output_dir=out,expected_head="f"*40)
            self.assertEqual(events[:2],["precheck","load_parent"]); self.assertEqual(events.count("train"),9); self.assertEqual(events.count("replay"),9)
            self.assertLess(max(i for i,v in enumerate(events) if v=="train"),events.index("replay"))
            q,_=b.verify_artifacts(out,["x"]*23,"f"*40); self.assertEqual(p,q)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*23,output_dir=out,expected_head="f"*40)

    def test_26_hash_and_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run"; p=b.run(summaries=["x"]*23,output_dir=out,expected_head="f"*40)
            path=out/"measurements.json"; path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"): b.verify_artifacts(out,["x"]*23,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name); a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size)
            (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"): b.verify_artifacts(out,["x"]*23,"f"*40)

    def test_27_runtime_preflight(self):
        with patch.object(b,"precheck",return_value=protection()),patch.object(b,"context",return_value=(self.parent,None,None,None,None,NS(training_tables=lambda *_:(self.x,self.y)),None)),patch.object(b,"load_parent",return_value=({},self.data,{},{})),patch.object(b,"make_models") as make,contextlib.redirect_stdout(io.StringIO()):
            b.runtime_preflight(["x"]*23,Path.cwd()); self.assertEqual(make.call_count,3)

    def test_28_cli(self):
        argv=["prog","--summaries"]+[str(i) for i in range(23)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run: b.main(); self.assertEqual(len(run.call_args.kwargs["summaries"]),23)

    def test_29_cp932_and_explicit_reads(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN: self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="read_text":
                    self.assertTrue(any(k.arg=="encoding" and isinstance(k.value,ast.Constant) and k.value.value=="utf-8" for k in node.keywords))

    def test_30_runner_contract(self):
        root=Path(__file__).resolve().parents[1]; runner=(root/b.OWN[2]).read_text(encoding="utf-8"); launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S); self.assertEqual(len(blocks),3)
        for code in blocks: ast.parse(code)
        self.assertIn("sys.argv[2:25]",blocks[2]); self.assertIn("head = sys.argv[25]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),23)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"))
        self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_31_context_modules(self):
        c=NS(); parent=NS(context=lambda:(0,1,2,3,4,5,c),regression_modules=lambda root:["f"+str(i) for i in range(181)])
        package=types.ModuleType("fold_lm.v05_benchmarks"); package.model_c296_render_balanced_batches=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):
            self.assertEqual(b.context(),(parent,1,2,3,4,5,c)); self.assertEqual(len(b.regression_modules(Path.cwd())),182)

    def test_32_guard_and_count(self):
        b.guard(Path.cwd(),"f"*40,NS(audit=Audit()))
        with self.assertRaises(ValueError): b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),32)


if __name__=="__main__": unittest.main()
