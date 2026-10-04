"""C300 hook,provenance and persistence fixtures; no FOLD capability claims."""
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
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c300_frozen_readout_terms as b


class Encoder(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.embedding = torch.nn.Embedding(259, 16, dtype=torch.float64)
    def forward(self, x): return (self.embedding(x),)


class Core(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.linear = torch.nn.Linear(16, 16, dtype=torch.float64)
    def forward(self, x, local, route_index): return torch.tanh(self.linear(x)+local*.1)


class Backbone(torch.nn.Module):
    def __init__(self):
        super().__init__(); self.local_encoder = Encoder(); self.core = Core()
        self.readout_norm = torch.nn.LayerNorm(16, dtype=torch.float64)
        self.classifier = torch.nn.Linear(16, 256, dtype=torch.float64)
        self.config = NS(width=16, max_tokens=48, next_route=0, instruction_route=1, internal_steps=2)
        self.padding = torch.nn.Parameter(torch.zeros(13488-sum(p.numel() for p in self.parameters()), dtype=torch.float64))
    def forward(self, x, tasks):
        valid = x != 256; local = self.local_encoder(x)[0]*valid[:,:,None]; state = local
        for _ in range(2):
            nxt = self.core(state, local, route_index=0)
            self.core(state, local, route_index=1); state = nxt
        eos = valid.sum(1)-1
        return self.classifier(self.readout_norm(state[torch.arange(len(x)), eos]))


class Reader(torch.nn.Module):
    def __init__(self, *args):
        super().__init__()
        for n in ("key", "query", "output"): setattr(self, n, torch.nn.Linear(16,16,bias=False,dtype=torch.float64))


class Toy(torch.nn.Module):
    """A dynamic-hook model with C278's registration order,for unit-level failure injection."""
    def __init__(self):
        super().__init__(); self.backbone = Backbone(); self.read = Reader(); self.offset = 0.; self.fail = False
    def forward(self, x, tasks):
        def add(module, args):
            if self.fail: raise RuntimeError("fixture failure")
            return (args[0]+self.read.output(args[0]) + self.offset,)
        handle = self.backbone.readout_norm.register_forward_pre_hook(add)
        try: return self.backbone(x, tasks)
        finally: handle.remove()


def inputs(n=4):
    x = torch.full((n,48),256,dtype=torch.int64); x[:,:3] = torch.tensor([0,1,2]); x[:,3] = 258
    return x, torch.zeros(n,dtype=torch.int64)


def frozen_model():
    torch.manual_seed(10); m = Toy(); m.eval(); m.requires_grad_(False); return m


def fingerprint(m): return b.digest({n:t.detach().tolist() for n,t in m.state_dict().items()})


def raw_fixture(data, passes):
    raw = {}
    for task in b.TASKS:
        raw[task] = {}
        for split,rows in data.items():
            z = torch.zeros((len(rows),256),dtype=torch.float64)
            y = torch.tensor([r["target"] for r in rows]); z[torch.arange(len(rows)),y] = 5.
            if not passes[task]: z[0,70] = 9.
            raw[task][split] = {str(p):{v:z for v in ("normal","evidence_blind","query_blind")} for p in range(3)}
    return raw


def fixtures():
    data = {s:[dict(target=48+i%2) for i in range(n)] for s,n in (("TRAIN",192),("HOLDOUT",96))}
    records,anchors = [],[]; matrices = b.expected_matrices()
    for i,(rest,core) in enumerate(b.identities()):
        raw = raw_fixture(data,{t:matrices[t][i//3][i%3] for t in b.TASKS}); h = b.digest([rest,core])
        anchors.append(dict(remaining_seed=rest,core_seed=core,final_sha256=h,raw=raw))
        records.append(dict(remaining_seed=rest,core_seed=core,final_sha256=h,
            raw={m:raw for m in b.MODES},mode_attestations={m:dict(calls=81,formula_checks=81) for m in b.MODES},
            before_error=0.,after_error=0.,restoration_error=0.,weights_preserved=True,hooks_restored=True))
    return records,anchors,data


def replay_error(left,right,data,c):
    error = 0.
    b.require(set(left)==set(right)==set(b.TASKS),"replay tasks")
    for task,split,p,v in itertools.product(b.TASKS,b.SPLITS,map(str,range(3)),("normal","evidence_blind","query_blind")):
        a,z = left[task][split][p][v],right[task][split][p][v]
        error = max(error,float((a-z).abs().max()))
        b.require(error<=1e-9 and torch.equal(a.argmax(1),z.argmax(1)),"fixture replay")
    return error


def scorers():
    def score(data,raw):
        rows=[]
        for split,items in data.items():
            y=torch.tensor([r["target"] for r in items]);correct=sum(int((vs["normal"].argmax(1)==y).sum()) for vs in raw[split].values())
            rows.append(dict(split=split,rows=3*len(items),correct=correct,direct_pass=correct==3*len(items),final_normal_nll=.1))
        return dict(passed=all(r["direct_pass"] for r in rows),totals=rows)
    diag=NS(normalize_task=lambda scored,*_:scored["totals"],partition=lambda rows:{k:v for k,v in rows[0].items() if k!="split"})
    c=NS(p267=NS(score=score),c270=NS(score=lambda data,raw,p:score(data,raw)))
    return diag,NS(replay_error=replay_error),NS(score_quad=lambda data,raw,c:score(data,raw)),c


@contextlib.contextmanager
def counted(model, core):
    calls=[0,0];cores=[0]
    def mh(m,args,out):calls[0]+=1;calls[1]+=len(args[0])
    def ch(m,args,out):cores[0]+=1
    h=model.register_forward_hook(mh);g=model.backbone.core.register_forward_hook(ch)
    try:yield calls,cores
    finally:h.remove();g.remove()


def evaluator(model,data,triple,quad,transfer,c):
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


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB;pins[b.READOUT_SOURCE]=b.READOUT_BLOB
    while len(pins)<646:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1191)}


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


class C300Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();cls.det=torch.are_deterministic_algorithms_enabled();torch.set_num_threads(2)
        cls.records,cls.anchors,cls.data=fixtures();cls.metrics,cls.summary=b.analyze(cls.records,cls.anchors,cls.data,*scorers())
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads);torch.use_deterministic_algorithms(cls.det)

    def test_01_manifest(self):b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seal(self):
        for value in ("UNSEALED","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",value),self.assertRaises(ValueError):b.validate_seal()

    def test_03_unknown_mode(self):
        with torch.no_grad(),self.assertRaises(ValueError),b.intervene(frozen_model(),"select_best"):pass

    def test_04_require_frozen(self):
        m=Toy()
        with torch.no_grad(),self.assertRaises(ValueError),b.intervene(m,"full_before"):pass

    def test_05_require_no_grad(self):
        with self.assertRaises(ValueError),b.intervene(frozen_model(),"full_before"):pass

    def test_06_identity_and_counts(self):
        m=frozen_model()
        with torch.no_grad():
            expected=m(*inputs())
            with b.intervene(m,"full_before") as stats:actual=m(*inputs())
        self.assertTrue(torch.equal(actual,expected));self.assertEqual(stats,dict(calls=1,formula_checks=1))

    def test_07_residual_exact(self):
        m=frozen_model();captured=[]
        h=m.backbone.readout_norm.register_forward_pre_hook(lambda module,args:captured.append(args[0].clone()))
        with torch.no_grad():
            m(*inputs());expected=m.backbone.classifier(m.backbone.readout_norm(captured[0]))
        h.remove()
        with torch.no_grad(),b.intervene(m,"residual_only"):actual=m(*inputs())
        self.assertTrue(torch.equal(actual,expected))

    def test_08_reader_exact(self):
        m=frozen_model();captured=[]
        h=m.read.output.register_forward_hook(lambda module,args,out:captured.append(out.clone()))
        with torch.no_grad():
            m(*inputs());expected=m.backbone.classifier(m.backbone.readout_norm(captured[0]))
        h.remove()
        with torch.no_grad(),b.intervene(m,"reader_only"):actual=m(*inputs())
        self.assertTrue(torch.equal(actual,expected))

    def test_09_all_modes_weight_and_hook_restoration(self):
        m=frozen_model();state=fingerprint(m);hooks=b.hook_snapshot(m)
        with torch.no_grad():
            first=m(*inputs())
            for mode in b.MODES:
                with b.intervene(m,mode):m(*inputs())
            final=m(*inputs())
        self.assertTrue(torch.equal(first,final));self.assertEqual(state,fingerprint(m));self.assertEqual(hooks,b.hook_snapshot(m))

    def test_10_repeated_calls(self):
        m=frozen_model()
        with torch.no_grad(),b.intervene(m,"reader_only") as stats:
            for n in (1,7,96):self.assertEqual(m(*inputs(n)).shape,(n,256))
        self.assertEqual(stats,dict(calls=3,formula_checks=3))

    def test_11_exception_cleans_dynamic_hooks(self):
        m=frozen_model();m.fail=True;before=b.hook_snapshot(m)
        with torch.no_grad(),self.assertRaisesRegex(RuntimeError,"fixture failure"),b.intervene(m,"reader_only"):m(*inputs())
        self.assertEqual(b.hook_snapshot(m),before)
        m.fail=False
        with torch.no_grad(),b.intervene(m,"full_after"):m(*inputs())

    def test_12_sum_mismatch_fails_closed(self):
        m=frozen_model();m.offset=.5;before=b.hook_snapshot(m)
        with torch.no_grad(),self.assertRaisesRegex(ValueError,"sum identity"),b.intervene(m,"full_before"):m(*inputs())
        self.assertEqual(before,b.hook_snapshot(m))

    def test_13_empty_intervention_rejected(self):
        with torch.no_grad(),self.assertRaisesRegex(ValueError,"call coverage"),b.intervene(frozen_model(),"full_before"):pass

    def test_14_wrong_dtype_rejected(self):
        m=frozen_model().float()
        with torch.no_grad(),self.assertRaisesRegex(ValueError,"summand contract"),b.intervene(m,"reader_only"):m(*inputs())

    def test_15_existing_hooks_preserved(self):
        m=frozen_model();called=[];h=m.register_forward_hook(lambda *args:called.append(1));before=b.hook_snapshot(m)
        with torch.no_grad(),b.intervene(m,"full_before"):m(*inputs())
        self.assertEqual(before,b.hook_snapshot(m));self.assertEqual(called,[1]);h.remove()

    def test_16_no_optimizer_or_state_reload_in_hook(self):
        m=frozen_model()
        with patch.object(torch.optim,"AdamW",side_effect=AssertionError("optimizer")),patch.object(torch.nn.Module,"load_state_dict",side_effect=AssertionError("reload")),torch.no_grad(),b.intervene(m,"reader_only"):
            m(*inputs())

    def test_17_complete_cohort(self):
        self.assertEqual((len(self.metrics),len(self.summary["cell_results"]),len(self.summary["final_partitions"]),len(self.summary["comparisons"])),(36,36,216,108))
        self.assertEqual(sum(x["rows"] for x in self.summary["comparisons"]),46656)
        with self.assertRaises(ValueError):b.analyze(self.records[:-1],self.anchors,self.data,*scorers())

    def test_18_exact_rescues_and_regressions(self):
        data=[dict(target=48),dict(target=49)];a=torch.zeros((2,256),dtype=torch.float64);z=a.clone()
        a[0,70]=2;a[1,49]=2;z[0,48]=2;z[1,70]=2
        r=b.compare_normal({"p":dict(normal=a)},{"p":dict(normal=z)},data)
        self.assertEqual((r["rescued"],r["regressed"],r["argmax_flips"]),(1,1,2))

    def test_19_wrong_to_wrong_is_not_rescue(self):
        a=torch.zeros((1,256),dtype=torch.float64);z=a.clone();a[0,70]=2;z[0,71]=2
        r=b.compare_normal({"p":dict(normal=a)},{"p":dict(normal=z)},[dict(target=48)])
        self.assertEqual((r["rescued"],r["regressed"],r["argmax_flips"]),(0,0,1))

    def test_20_reproduction_mismatch(self):
        records=copy.deepcopy(self.records);records[0]["before_error"]=.1
        with self.assertRaisesRegex(ValueError,"reproduction"):b.analyze(records,self.anchors,self.data,*scorers())

    def test_21_mode_counts_and_state_tamper(self):
        for fn in (lambda r:r.update(weights_preserved=False),lambda r:r["mode_attestations"]["reader_only"].update(calls=80),lambda r:r.update(final_sha256="bad")):
            records=copy.deepcopy(self.records);fn(records[0])
            with self.assertRaises(ValueError):b.analyze(records,self.anchors,self.data,*scorers())

    def test_22_all_ablations_fail_still_diagnostic(self):
        records=copy.deepcopy(self.records)
        for r in records:
            for m in b.MODES[1:3]:r["raw"][m]=raw_fixture(self.data,dict.fromkeys(b.TASKS,False))
        _,summary=b.analyze(records,self.anchors,self.data,*scorers());b.validate_result(payload_fixture(summary))
        self.assertFalse(any(x for row in summary["task_pass_matrices"]["reader_only"]["quad"] for x in row))

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c300-fixture")/str(i)/"summary.json").resolve() for i in range(26)]
        objects={n:{"name":n} for n in b.PARENT_OUTPUTS[1:4]}
        parent=NS(context=lambda:(None,),parent_hashes=lambda _:tuple(str(i%10)*64 for i in range(25)),validate_result=Mock(),verify_artifacts=Mock(),check_grid=Mock(),DATA_HASHES=tuple(map(b.digest,objects.values())))
        p=dict(experiment_id="C299-v5b-core-initialization-grid",commit_sha=b.PARENT_EXECUTION,status="PASS",
            source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB,b.READOUT_SOURCE:b.READOUT_BLOB},artifacts=[dict(file=n) for n in b.PARENT_OUTPUTS],
            validation_summary=dict(task_pass_matrices=b.expected_matrices(),diagnostic_complete=True,capability_gate_applicable=False,components_matched=True,all_replays=True))
        parent.verify_artifacts.return_value=(p,{})
        mapping=dict(zip(map(str,paths),(b.PARENT_SHA,*parent.parent_hashes(None)),strict=True))
        c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:objects[p.name]))
        archive=dict(schema="fold-c299-core-eval-v1",records=self.anchors)
        with patch.object(b,"context",return_value=(parent,NS(no_neural=contextlib.nullcontext),None,None,None,None,c)),patch.object(torch,"load",return_value=archive):yield paths,mapping,parent,p

    def test_23_all26_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,p):
            self.assertEqual(b.load_parent(paths)[0],p);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="f"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_24_parent_and_readout_contract(self):
        for fn in (lambda p:p.update(status="FAIL"),lambda p:p["source_blobs"].pop(b.READOUT_SOURCE),lambda p:p["artifacts"].pop()):
            with self.loader_fixture() as (paths,_,_,p):
                fn(p)
                with self.assertRaises(ValueError):b.load_parent(paths)

    def test_25_protection_actual_count_and_missing_helper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);names=[b.PARENT_SOURCE,b.READOUT_SOURCE]+[f"accepted/{i}" for i in range(638)]
            pins={n:"b"*40 for n in names};pins[b.PARENT_SOURCE]=b.PARENT_BLOB;pins[b.READOUT_SOURCE]=b.READOUT_BLOB
            for n in names+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n,encoding="utf-8")
            protected={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1176-len(protected)):
                p=root/f"input{i}";p.write_text("input",encoding="utf-8");protected[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent";directory.mkdir();path=directory/"summary.json";path.write_text("summary",encoding="utf-8");mapping={str(path.resolve()):b.PARENT_SHA};artifacts=[]
            for n in b.PARENT_OUTPUTS:
                p=directory/n;p.write_text("parent",encoding="utf-8");mapping[str(p.resolve())]="a"*64;artifacts.append(dict(file=n,sha256="a"*64))
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            parent=types.ModuleType("parent");parent.__file__=str(root/b.PARENT_SOURCE);parent.context=lambda:()
            c=NS(audit=NS(sha=sha,git=lambda root,*a:(pins.get(a[1][5:],"c"*40)+"\n").encode(),safe_child=Audit.safe_child,
                protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            payload=dict(source_blobs=pins,input_sha256=protected,artifacts=artifacts)
            with patch.object(b,"context",return_value=(parent,None,None,None,None,None,c)),patch.object(b,"load_parent",return_value=(payload,None,None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([path]*26,root))),(646,1191))
                c.missing=types.ModuleType("missing");c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"):b.precheck([path]*26,root)

    def test_26_real_infer_cell_full_count(self):
        m=frozen_model();c=NS(base=NS(fingerprint=fingerprint),p267=NS(counted=counted),core=None)
        evaluation=NS(evaluate=evaluator,replay_error=replay_error)
        with torch.no_grad():raw=evaluator(m,self.data,None,None,None,c)
        anchor=dict(remaining_seed=b.LEVELS[0],core_seed=b.LEVELS[0],final_sha256=fingerprint(m),raw=raw)
        with contextlib.redirect_stdout(io.StringIO()):r=b.infer_cell(m,m.state_dict(),anchor,self.data,None,None,evaluation,None,c)
        self.assertEqual(r["mode_attestations"],{mode:dict(calls=81,formula_checks=81) for mode in b.MODES})
        self.assertEqual(r["restoration_error"],0.);self.assertTrue(r["weights_preserved"])

    def test_27_runtime_frozen_smoke(self):
        m=frozen_model();state=copy.deepcopy(m.state_dict());anchor=dict(final_sha256=fingerprint(m))
        parent=NS(load_bundle=lambda p:[state]*9,make_grid=lambda c:dict.fromkeys(b.identities(),m))
        tokens=inputs(192)[0][None,None].expand(2,3,-1,-1).clone()
        c=NS(base=NS(fingerprint=fingerprint),p267=NS(check_logits=lambda x,n:self.assertEqual(x.shape,(n,256))))
        with patch.object(b,"precheck",return_value=protection()),patch.object(b,"context",return_value=(parent,None,None,None,None,NS(training_tables=lambda *a:(tokens,None)),c)),patch.object(b,"load_parent",return_value=({},self.data,None,None,[anchor]*9)),contextlib.redirect_stdout(io.StringIO()):b.runtime_preflight(["x"]*26,Path.cwd())

    @contextlib.contextmanager
    def run_fixture(self):
        diag,evaluation,transfer,c=scorers();c.audit=Audit();events=[]
        parent=NS(load_bundle=lambda p:[{}]*9,make_grid=lambda c:dict.fromkeys(b.identities()))
        def infer(*a):events.append("infer");return self.records[b.identities().index((a[2]["remaining_seed"],a[2]["core_seed"]))]
        def load(*a):events.append("load_parent");return {},self.data,None,None,self.anchors
        def pc(*a):events.append("precheck");return protection()
        with patch.object(b,"context",return_value=(parent,NS(no_neural=contextlib.nullcontext),diag,evaluation,transfer,None,c)),patch.object(b,"load_parent",side_effect=load),patch.object(b,"precheck",side_effect=pc),patch.object(b,"infer_cell",side_effect=infer):yield events

    def test_28_run_order_and_roundtrip(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*26,output_dir=out,expected_head="f"*40)
            self.assertEqual(events[:2],["precheck","load_parent"]);self.assertEqual(events.count("infer"),9)
            q,_=b.verify_artifacts(out,["x"]*26,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*26,output_dir=out,expected_head="f"*40)

    def test_29_hash_and_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*26,output_dir=out,expected_head="f"*40);path=out/"measurements.json";path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*26,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size);(out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*26,"f"*40)

    def test_30_payload_scopes_and_counts(self):
        b.validate_result(payload_fixture(self.summary))
        for fn in (lambda p:p.update(capability_gate_applicable=True),lambda p:p["validation_summary"].update(train_steps=False),lambda p:p["validation_summary"]["reproductions"][0].update(matched=False)):
            p=payload_fixture(copy.deepcopy(self.summary));fn(p)
            with self.assertRaises(ValueError):b.validate_result(p)

    def test_31_semantic_suite(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(4597)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(n) for n in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual(suite.countTestCases(),4597);self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})

    def test_32_cli(self):
        argv=["prog","--summaries"]+[str(i) for i in range(26)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:b.main();self.assertEqual(len(run.call_args.kwargs["summaries"]),26)

    def test_33_cp932_explicit_reads(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN:self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        for path in (Path(b.__file__),Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="read_text":
                    self.assertTrue(any(k.arg=="encoding" and isinstance(k.value,ast.Constant) and k.value.value=="utf-8" for k in node.keywords))

    def test_34_runner_contract(self):
        root=Path(__file__).resolve().parents[1];runner=(root/b.OWN[2]).read_text(encoding="utf-8");launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:28]",blocks[2]);self.assertIn("head = sys.argv[28]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),26)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"));self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_35_context_and_modules(self):
        parent=NS(context=lambda:tuple(range(9)),regression_modules=lambda root:["f"+str(i) for i in range(184)])
        package=types.ModuleType("fold_lm.v05_benchmarks");package.model_c299_core_initialization=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):self.assertEqual(b.context(),(parent,3,4,5,6,7,8));self.assertEqual(len(b.regression_modules(Path.cwd())),185)

    def test_36_guard(self):
        b.guard(Path.cwd(),"f"*40,NS(audit=Audit()))
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))

    def test_37_direct_imports_and_count(self):
        tree=ast.parse(Path(b.__file__).read_text(encoding="utf-8"))
        imports=[n.names[0].name for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(imports,["model_c299_core_initialization"]);self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),40)

    def test_38_reproduction_old_gate_is_not_replaced(self):
        records=copy.deepcopy(self.records)
        for r in records:r["raw"]["full_after"]=raw_fixture(self.data,dict.fromkeys(b.TASKS,True))
        with self.assertRaises(ValueError):b.analyze(records,self.anchors,self.data,*scorers())

    def test_39_no_new_model_checkpoint(self):
        saved=[];real=torch.save
        def save(v,path,*a,**k):saved.append(Path(path).name);return real(v,path,*a,**k)
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,patch.object(torch,"save",side_effect=save),contextlib.redirect_stdout(io.StringIO()):
            b.run(summaries=["x"]*26,output_dir=Path(tmp)/"run",expected_head="f"*40)
        self.assertEqual(saved,["intervention-evaluations.pt"]);self.assertEqual(b.WORK["new_checkpoint_writes"],0)

    def test_40_actual_accepted_c278_class_hook_protocol(self):
        # Execute the actual accepted class AST,not an independently rewritten forward.
        # The surrounding backbone/reader are fixtures;this is not FOLD capability testing.
        root=Path(__file__).resolve().parents[1];path=root/b.READOUT_SOURCE
        tree=ast.parse(path.read_text(encoding="utf-8"));node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="MeanFinalDualReadout")
        space=dict(torch=torch,nn=torch.nn,Counter=Counter,req=b.require,__name__="c300_c278_fixture")
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),"exec"),space)
        def span(x):
            out=torch.zeros_like(x,dtype=torch.bool);out[:,1:3]=True;return out
        torch.manual_seed(90);m=space["MeanFinalDualReadout"](Backbone(),1,NS(ResidualHead=Reader),span)
        m.eval();m.requires_grad_(False);before=b.hook_snapshot(m);h=fingerprint(m)
        with torch.no_grad():
            plain=m(*inputs())
            for mode in b.MODES:
                with b.intervene(m,mode) as stats:out=m(*inputs())
                self.assertEqual(stats,dict(calls=1,formula_checks=1))
                if mode.startswith("full"):self.assertTrue(torch.equal(plain,out))
        self.assertEqual(before,b.hook_snapshot(m));self.assertEqual(h,fingerprint(m))


if __name__=="__main__":unittest.main()
