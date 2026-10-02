"""C295 behavioral fixtures; mocked scorers are not evidence about actual FOLD capability."""
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
from fold_lm.v05_benchmarks import model_c295_ce_budget as b


def dataset():
    data={"TRAIN":[],"HOLDOUT":[]}
    for e,v,language in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),("en","ja")):
        split="HOLDOUT" if (v[1]-v[0])%4==2 else "TRAIN"
        for order,q in itertools.product((e,e[::-1]),e):
            data[split].append(dict(id=str((language,e,v,order,q)),language=language,entities=list(e),values=list(v),permutation=list(order),query=q,target=48+v[e.index(q)]))
    return data


def tables(data):
    y=torch.tensor([r["target"] for r in data["TRAIN"]]);x=torch.zeros((2,3,192,48),dtype=torch.int64);x[:,:,:,0]=y-48
    return x,y


class Toy(torch.nn.Module):
    def __init__(self):
        super().__init__();self.embedding=torch.nn.Embedding(4,4,dtype=torch.float64);self.output=torch.nn.Linear(4,256,dtype=torch.float64)
        self.calls=0;self.rows=0
    def forward(self,tokens,tasks):
        assert tokens.shape==(len(tokens),48) and tasks.shape==(len(tokens),) and not bool(tasks.any())
        self.calls+=1;self.rows+=len(tokens)
        return self.output(self.embedding(tokens[:,0]))


def fingerprint(m):return b.digest({k:v.detach().tolist() for k,v in m.state_dict().items()})


def fixtures():
    data=dataset();zs={}
    for split,rows in data.items():
        z=torch.zeros((len(rows),256),dtype=torch.float64);z[torch.arange(len(rows)),torch.tensor([r["target"] for r in rows])]=4.;zs[split]=z
    trajectories=[];records=[]
    for seed in b.SEEDS:
        trajectories.append(dict(seed=seed,steps=1600,training_rows=76800,optimizer_creations=1,initial_sha256="a"*64,
            snapshot_sha256={"ce800":"b"*64,"ce1600":"c"*64},ce_history=[1.]*1600,prefix_loss_sha256=b.digest([1.]*800),**b.schedule(seed,data["TRAIN"])[3]))
        for arm in b.ARMS:
            raw={t:{s:{str(p):{v:zs[s] for v in ("normal","evidence_blind","query_blind")} for p in range(3)} for s in data} for t in b.TASKS}
            records.append(dict(seed=seed,arm=arm,steps_at_snapshot=b.BUDGETS[arm],parameters=14256,final_sha256=trajectories[-1]["snapshot_sha256"][arm],raw=raw,
                evaluation_forward_calls=81,evaluation_rows=7776,evaluation_core_calls=324,checkpoint_roundtrip=True,reload_max_error=0.,
                replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324))
    return records,trajectories,data


def scorers():
    def score(data,raw):
        totals=[]
        for split,profiles in raw.items():
            for profile,views in profiles.items():
                pred=views["normal"].argmax(1).tolist()
                for lang in ("en","ja"):
                    ii=[i for i,r in enumerate(data[split]) if r["language"]==lang];correct=sum(pred[i]==data[split][i]["target"] for i in ii)
                    totals.append(dict(split=split,profile=profile,language=lang,rows=len(ii),pairs=len(ii)//2,correct=correct,collapsed_pairs=0))
        return dict(passed=all(x["correct"]==x["rows"] for x in totals),totals=totals)
    def measure(z,rows):return [dict(correct=int(p)==r["target"]) for p,r in zip(z.argmax(1).tolist(),rows,strict=True)]
    def aggregate(rows):
        n=sum(r["correct"] for r in rows)
        return dict(rows=len(rows),correct=n,conditional_correct=n,output_role_counts=dict(target=n,other_fact=len(rows)-n,absent_known_value=0,non_value_byte=0))
    parent=NS(measure=measure,aggregate=aggregate,no_neural=contextlib.nullcontext)
    diagnostic=NS(normalize_task=lambda s,*_:s["totals"],partition=lambda rs:dict(rows=sum(r["rows"] for r in rs),correct=sum(r["correct"] for r in rs),direct_pass=all(r["correct"]==r["rows"] for r in rs)))
    transfer=NS(score_quad=lambda data,raw,c:score(data,raw));c=NS(p267=NS(score=score),c270=NS(score=lambda data,raw,p:score(data,raw)))
    return parent,diagnostic,transfer,c


def protection():
    pins={n:"b"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<616:pins["fixture/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(1116)}


class Audit:
    @staticmethod
    def sha(p):
        p=Path(p);return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(p):return json.loads(Path(p).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n):return Path(root)/n
    @staticmethod
    def git(root,*a):
        if a[0]=="rev-parse":return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if a[0]=="branch":return b"feat/sft-target-loss\n"
        return b""


def result_fixture(summary):
    pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary,gate_f_candidate=False,production_adoption=False)


class C295Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();cls.det=torch.are_deterministic_algorithms_enabled();torch.set_num_threads(2)
        cls.data=dataset();cls.x,cls.y=tables(cls.data);torch.manual_seed(295);cls.initial=Toy();cls.long=copy.deepcopy(cls.initial);cls.short=copy.deepcopy(cls.initial)
        with contextlib.redirect_stdout(io.StringIO()):
            cls.trajectory,cls.states=b.fit_trajectory(cls.long,cls.data,cls.x,cls.y,b.SEEDS[0],fingerprint,1600)
            cls.short_trace,cls.short_states=b.fit_trajectory(cls.short,cls.data,cls.x,cls.y,b.SEEDS[0],fingerprint,800)
        cls.records,cls.traces,_=fixtures();cls.metrics,cls.summary=b.analyze(cls.records,cls.traces,cls.data,*scorers())
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads);torch.use_deterministic_algorithms(cls.det)

    def test_01_seal(self):b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seals(self):
        for h in ("UNSEALED","0"*64,"A"*64):
            with patch.object(b,"MANIFEST_SHA",h),self.assertRaises(ValueError):b.validate_seal()

    def test_03_all_seed_schedule_prefixes(self):
        for seed in b.SEEDS:
            a=b.schedule(seed,self.data["TRAIN"],800);c=b.schedule(seed,self.data["TRAIN"],1600)
            self.assertTrue(all(torch.equal(x,y[:800]) for x,y in zip(a[:3],c[:3],strict=True)))
            self.assertEqual(c[3]["per_length_exposures"],[[200]*192]*2)

    def test_04_pair_integrity(self):
        x,*_=b.schedule(b.SEEDS[0],self.data["TRAIN"])
        for batch in x[:800].tolist():
            for i,j in zip(batch[::2],batch[1::2],strict=True):
                a,c=self.data["TRAIN"][i],self.data["TRAIN"][j]
                self.assertNotEqual(a["target"],c["target"])
                for k in ("language","entities","values","permutation"):self.assertEqual(a[k],c[k])

    def test_05_bad_schedule(self):
        for seed,steps,rows in ((1,1600,self.data["TRAIN"]),(b.SEEDS[0],1200,self.data["TRAIN"]),(b.SEEDS[0],1600,self.data["TRAIN"][:-1])):
            with self.assertRaises(ValueError):b.schedule(seed,rows,steps)
        rows=copy.deepcopy(self.data["TRAIN"]);rows[1]["target"]=88
        with self.assertRaises(ValueError):b.schedule(b.SEEDS[0],rows)

    def test_06_exact_standalone_800_prefix(self):
        self.assertEqual(self.short_trace["ce_history"],self.trajectory["ce_history"][:800])
        for k,v in self.short_states["ce800"].items():self.assertTrue(torch.equal(v,self.states["ce800"][k]))
        self.assertEqual(self.short_trace["snapshot_sha256"]["ce800"],self.trajectory["snapshot_sha256"]["ce800"])

    def test_07_actual_updates_and_loss(self):
        self.assertEqual((self.long.calls,self.long.rows),(1600,76800));self.assertEqual((self.short.calls,self.short.rows),(800,38400))
        b.check_trajectory(self.trajectory,self.data);self.assertLess(self.trajectory["ce_history"][-1],self.trajectory["ce_history"][0])
        self.assertFalse(self.long.training)

    def test_08_snapshot_no_shared_storage(self):
        for k,v in self.states["ce800"].items():
            self.assertNotEqual(v.data_ptr(),self.states["ce1600"][k].data_ptr());self.assertNotEqual(v.data_ptr(),self.long.state_dict()[k].data_ptr())
        self.assertTrue(any(not torch.equal(v,self.states["ce1600"][k]) for k,v in self.states["ce800"].items()))

    def test_09_optimizer_continuity(self):
        real=torch.optim.AdamW;made=[]
        def factory(*a,**kw):
            opt=real(*a,**kw);made.append(opt);return opt
        with patch.object(torch.optim,"AdamW",side_effect=factory),contextlib.redirect_stdout(io.StringIO()):
            t,_=b.fit_trajectory(copy.deepcopy(self.initial),self.data,self.x,self.y,b.SEEDS[0],fingerprint,1600)
        self.assertEqual(len(made),1);self.assertEqual({int(v["step"]) for v in made[0].state.values()},{1600})
        self.assertEqual(t,self.trajectory)

    def test_10_no_forward_labels_and_plain_ce(self):
        x=self.x[0,0,:48];m=copy.deepcopy(self.initial);z=m(x,torch.zeros(48,dtype=torch.int64))
        from torch.nn import functional as F
        ids,profiles,lengths,_=b.schedule(b.SEEDS[0],self.data["TRAIN"])
        first=m(self.x[lengths[0],profiles[0],ids[0]],torch.zeros(48,dtype=torch.int64))
        self.assertAlmostEqual(float(F.cross_entropy(first,self.y[ids[0]]).detach()),self.trajectory["ce_history"][0])

    def test_11_bad_targets(self):
        y=self.y.clone();y[0]=100
        with self.assertRaises(ValueError):b.fit_trajectory(copy.deepcopy(self.initial),self.data,self.x,y,b.SEEDS[0],fingerprint)

    def test_12_tampered_trajectory(self):
        for f in (lambda t:t.update(steps=800),lambda t:t.update(optimizer_creations=2),lambda t:t["ce_history"].__setitem__(0,float("nan")),lambda t:t["snapshot_sha256"].pop("ce800"),lambda t:t.update(prefix_loss_sha256="0"*64)):
            t=copy.deepcopy(self.trajectory);f(t)
            with self.assertRaises(ValueError):b.check_trajectory(t,self.data)

    def test_13_factory_capacity(self):
        class Fake(torch.nn.Module):
            def __init__(self,*a):super().__init__();self.w=torch.nn.Parameter(torch.ones(14256,dtype=torch.float64))
        c=NS(c278=NS(MeanFinalDualReadout=Fake),factory=NS(new_model=lambda seed:None),reader=None,c269=NS(query_span_mask=None))
        self.assertEqual(sum(p.numel() for p in b.new_model(b.SEEDS[0],c).parameters()),14256)
        with self.assertRaises(ValueError):b.new_model(1,c)

    def test_14_snapshot_evaluation_freeze_and_counts(self):
        @contextlib.contextmanager
        def counted(model,core):
            calls=[0,0];cores=[0];yield calls,cores;calls[:]=[model.calls,model.rows];cores[0]=model.calls*4
        def evaluate(model,*a):
            self.assertFalse(model.training);self.assertFalse(any(p.requires_grad for p in model.parameters()))
            with torch.no_grad():
                for _ in range(81):model(torch.zeros((96,48),dtype=torch.int64),torch.zeros(96,dtype=torch.int64))
            return {}
        c=NS(base=NS(fingerprint=fingerprint),p267=NS(counted=counted),core=None)
        r=b.score_snapshot(copy.deepcopy(self.initial),self.states["ce800"],b.SEEDS[0],"ce800",self.trajectory,self.data,{},{},NS(evaluate=evaluate),None,c)
        self.assertEqual((r["evaluation_forward_calls"],r["evaluation_rows"]),(81,7776))

    def test_15_analysis_counts(self):
        self.assertEqual((len(self.metrics),len(self.summary["final_partitions"]),len(self.summary["contrasts"])),(10,60,180))
        self.assertEqual(self.summary["quad_pass_counts"],dict.fromkeys(b.ARMS,5))

    def test_16_candidate_failure(self):
        r=copy.deepcopy(self.records);v=r[1]["raw"]["quad"]["HOLDOUT"]["0"];v["normal"]=v["normal"].clone();v["normal"][0,88]=20.
        _,s=b.analyze(r,self.traces,self.data,*scorers());self.assertFalse(s["candidate_gate"]);self.assertEqual(s["quad_pass_counts"]["ce1600"],4)
        b.validate_result(result_fixture(s))

    def test_17_snapshot_and_replay_rejection(self):
        for key,value in (("steps_at_snapshot",1600),("final_sha256","d"*64),("reload_max_error",.1),("checkpoint_roundtrip",False),("evaluation_rows",1)):
            r=copy.deepcopy(self.records);r[0][key]=value
            with self.assertRaises(ValueError):b.analyze(r,self.traces,self.data,*scorers())

    def test_18_result_workload_and_scope(self):
        b.validate_result(result_fixture(self.summary))
        for f in (lambda p:p.update(gate_f_candidate=True),lambda p:p["validation_summary"].update(train_steps=12000),lambda p:p["validation_summary"]["final_partitions"].pop()):
            p=result_fixture(copy.deepcopy(self.summary));f(p)
            with self.assertRaises(ValueError):b.validate_result(p)

    @contextlib.contextmanager
    def loader_fixture(self):
        paths=[(Path("/c295-fixture")/str(i)/"summary.json").resolve() for i in range(21)]
        old=(NS(PARENT_SHA="f"*64),NS(SUMMARY_SHAS=("1"*64,)*15));p291=NS(PARENT_SHA="e"*64,context=lambda:old)
        p292=NS(PARENT_SHA="d"*64);p293=NS(PARENT_SHA="c"*64,context=lambda:(p292,p291))
        parent=NS(PARENT_SHA="b"*64,no_neural=contextlib.nullcontext,validate_result=Mock(),verify_artifacts=Mock())
        payload=dict(commit_sha=b.PARENT_EXECUTION,status="PASS",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
            artifacts=[dict(file=n,sha256=v[0],serialized_bytes=v[1]) for n,v in b.PARENT_ARTIFACTS.items()],validation_summary=dict(diagnostic_complete=True,capability_gate_applicable=False))
        parent.verify_artifacts.return_value=(payload,{})
        mapping=dict(zip(map(str,paths),[b.PARENT_SHA,"b"*64,"c"*64,"d"*64,"e"*64,"f"*64]+["1"*64]*15,strict=True))
        objects={n:{"fixture":n} for n in ("dataset.json","triple-dataset.json","quad-dataset.json")}
        c=NS(audit=NS(sha=lambda p:mapping[str(p)],read_json=lambda p:objects[p.name]));m=b.manifest()
        for k,n in zip(("data_sha256","triple_sha256","quad_sha256"),objects,strict=True):m[k]=b.digest(objects[n])
        with patch.object(b,"context",return_value=(parent,p293,None,None,None,None,c)),patch.object(b,"manifest",return_value=m):yield paths,mapping,parent,payload

    def test_19_all_hashes_before_dispatch(self):
        with self.loader_fixture() as (paths,mapping,parent,payload):
            self.assertEqual(b.load_parent(paths)[0],payload);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for path in paths:
                old=mapping[str(path)];mapping[str(path)]="0"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(path)]=old

    def test_20_parent_descriptors(self):
        for f in (lambda p:p.update(status="FAIL"),lambda p:p["artifacts"][0].update(serialized_bytes=1),lambda p:p["validation_summary"].update(capability_gate_applicable=True)):
            with self.loader_fixture() as (paths,_,_,p):
                f(p)
                with self.assertRaises(ValueError):b.load_parent(paths)

    def test_21_real_protection_and_missing_helper(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);names=[b.PARENT_SOURCE]+[f"accepted/{i}" for i in range(609)];pins={n:b.PARENT_BLOB if n==b.PARENT_SOURCE else "b"*40 for n in names}
            for n in names+list(b.OWN):p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(n,encoding="utf-8")
            inputs={str((root/n).resolve()):Audit.sha(root/n) for n in names}
            for i in range(1106-len(inputs)):
                p=root/f"input{i}";p.write_text("input",encoding="utf-8");inputs[str(p.resolve())]=Audit.sha(p)
            directory=root/"parent";directory.mkdir();s=directory/"summary.json";s.write_text("summary",encoding="utf-8");mapping={str(s.resolve()):b.PARENT_SHA}
            for n,v in b.PARENT_ARTIFACTS.items():p=directory/n;p.write_text("parent",encoding="utf-8");mapping[str(p.resolve())]=v[0]
            def sha(p):return mapping.get(str(Path(p).resolve()),Audit.sha(p))
            def git(root,*a):return (pins.get(a[1][5:],"c"*40)+"\n").encode()
            parent=types.ModuleType("parent");parent.__file__=str(root/b.PARENT_SOURCE);p293=NS(context=lambda:())
            c=NS(audit=NS(sha=sha,git=git,safe_child=Audit.safe_child,protect_tree_files=lambda root,ps:{str((root/n).resolve()):sha(root/n) for n in ps}))
            with patch.object(b,"context",return_value=(parent,p293,None,None,None,None,c)),patch.object(b,"load_parent",return_value=(dict(source_blobs=pins,input_sha256=inputs),None,None,None)),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(tuple(map(len,b.precheck([s]*21,root))),(616,1116))
                c.missing=types.ModuleType("missing");c.missing.__file__=str(root/"missing.py")
                with self.assertRaisesRegex(ValueError,"unprotected helper"):b.precheck([s]*21,root)

    def test_22_semantic_test_ids(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(4421)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(x) for x in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual(suite.countTestCases(),4421);self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite([Dummy("x"),Dummy("x")])),self.assertRaises(ValueError):b.regression_suite(Path.cwd())

    def test_23_bundle_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"states.pt";v=dict(schema="fold-c295-budget-states-v1",identities=[list(x) for x in b.identities()],states=[{} for _ in range(10)])
            torch.save(v,p);self.assertEqual(len(b.load_bundle(p)),10);v["identities"].reverse();torch.save(v,p)
            with self.assertRaises(ValueError):b.load_bundle(p)

    @contextlib.contextmanager
    def run_fixture(self):
        records,traces,data=fixtures();events=[];parent,diag,transfer,c=scorers();c.audit=Audit();c.core=None;c.base=NS(fingerprint=lambda m:"b"*64)
        @contextlib.contextmanager
        def counted(*a):yield [1600,76800],[6400]
        c.p267.counted=counted
        def fit(*args):events.append("train");return copy.deepcopy(traces[b.SEEDS.index(args[4])]),{a:{} for a in b.ARMS}
        def score(*args):events.append("evaluate");return copy.deepcopy(records[b.identities().index((args[2],args[3]))])
        def replay(*args):events.append("replay")
        def load(*a):events.append("load_parent");return {},data,{"triple":1},{"quad":1}
        def precheck(*a):events.append("precheck");return protection()
        with patch.object(b,"context",return_value=(parent,None,diag,NS(replay_one=replay),transfer,NS(training_tables=lambda *_:(self.x,self.y)),c)),patch.object(b,"precheck",side_effect=precheck),patch.object(b,"load_parent",side_effect=load),patch.object(b,"new_model",return_value=None),patch.object(b,"fit_trajectory",side_effect=fit),patch.object(b,"score_snapshot",side_effect=score):yield events

    def test_24_production_order_and_roundtrip(self):
        with self.run_fixture() as events,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*21,output_dir=out,expected_head="f"*40)
            self.assertEqual(events[:2],["precheck","load_parent"]);self.assertEqual(events.count("train"),5)
            self.assertLess(max(i for i,x in enumerate(events) if x=="train"),events.index("evaluate"))
            self.assertEqual(events.count("evaluate"),10);self.assertEqual(events.count("replay"),10)
            q,_=b.verify_artifacts(out,["x"]*21,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*21,output_dir=out,expected_head="f"*40)

    def test_25_hash_and_semantic_tamper(self):
        with self.run_fixture(),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*21,output_dir=out,expected_head="f"*40);path=out/"measurements.json";path.write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*21,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==path.name);a.update(sha256=Audit.sha(path),serialized_bytes=path.stat().st_size);(out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*21,"f"*40)

    def test_26_runtime_dryrun(self):
        with patch.object(b,"precheck",return_value=protection()),patch.object(b,"context",return_value=(None,None,None,None,None,NS(training_tables=lambda *_:(self.x,self.y)),None)),patch.object(b,"load_parent",return_value=({},self.data,{},{})),patch.object(b,"new_model") as factory,contextlib.redirect_stdout(io.StringIO()):
            b.runtime_preflight(["x"]*21,Path.cwd());factory.assert_called_once()

    def test_27_cli(self):
        argv=["prog","--summaries"]+[str(i) for i in range(21)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:b.main();self.assertEqual(len(run.call_args.kwargs["summaries"]),21)

    def test_28_cp932_actual_files(self):
        root=Path(__file__).resolve().parents[1]
        with patch.object(io,"text_encoding",side_effect=lambda encoding,stacklevel=2:"cp932" if encoding is None else encoding):
            for n in b.OWN:self.assertTrue((root/n).read_text(encoding="utf-8"))
            self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))

    def test_29_explicit_utf8(self):
        for path in (Path(b.__file__),Path(__file__)):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=="read_text":
                    self.assertTrue(any(k.arg=="encoding" and isinstance(k.value,ast.Constant) and k.value.value=="utf-8" for k in node.keywords))

    def test_30_runner_contract(self):
        root=Path(__file__).resolve().parents[1];runner=(root/b.OWN[2]).read_text(encoding="utf-8");launcher=(root/b.OWN[3]).read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:23]",blocks[2]);self.assertIn("head = sys.argv[23]",blocks[2])
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',launcher)),21)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("-Mode Execute"));self.assertLess(launcher.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),launcher.index("publish_experiment_log.ps1"))

    def test_31_context_and_modules(self):
        c=NS();p293=NS(context=lambda:(0,1,2,3,4,5,c));parent=NS(context=lambda:(p293,c),regression_modules=lambda root:["f"+str(i) for i in range(179)])
        package=types.ModuleType("fold_lm.v05_benchmarks");package.model_c294_saved_support_choice_audit=parent
        with patch.dict(sys.modules,{"fold_lm.v05_benchmarks":package}):self.assertEqual(b.context(),(parent,p293,2,3,4,5,c));self.assertEqual(len(b.regression_modules(Path.cwd())),180)

    def test_32_guard_and_test_count(self):
        b.guard(Path.cwd(),"f"*40,NS(audit=Audit()))
        with self.assertRaises(ValueError):b.guard(Path.cwd(),"e"*40,NS(audit=Audit()))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()["own_tests"])


if __name__=="__main__":unittest.main()
