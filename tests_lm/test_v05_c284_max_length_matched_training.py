"""C284 behavioral authoring tests; real archives and inherited models are runtime gates."""
import ast
import contextlib
import copy
import hashlib
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

import torch
from fold_lm.v05_benchmarks import model_c284_max_length_matched_training as b


def data_fixture():
    rows = [dict(language="en",entities=[0,1],values=[i,i+1],permutation=[0,1],query=q,
                 target=48+q,id=f"{i}:{q}") for i in range(96) for q in range(2)]
    return dict(TRAIN=rows,HOLDOUT=[dict(id="HOLDOUT-SENTINEL",target=55)])


def score_fixture(task):
    profiles = {"two_char":("doubled","shared_prefix","shared_suffix"),
                "triple":("tripled","shared_prefix2","shared_suffix2"),
                "quad":("quadrupled","shared_prefix3","shared_suffix3")}[task]
    totals = [dict(split=s,profile=p,language=l,rows=n,pairs=n//2,correct=n,collapsed_pairs=0)
              for s,n in (("TRAIN",96),("HOLDOUT",48)) for p in profiles for l in ("en","ja")]
    return dict(passed=True,totals=totals,cells=[],two_order=[])


def fingerprint(model):
    return hashlib.sha256(b"".join(x.detach().cpu().numpy().tobytes() for x in model.state_dict().values())).hexdigest()


class Weights(torch.nn.Module):
    def __init__(self,n):
        super().__init__(); self.weight=torch.nn.Parameter(torch.ones(n,dtype=torch.float64))


class Readout(torch.nn.Module):
    def __init__(self,backbone,seed,reader,span):
        super().__init__(); self.backbone=backbone; self.read=Weights(768)


class Audit:
    @staticmethod
    def git(root,*args):
        if args[0]=="rev-parse": return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0]=="branch": return b"feat/sft-target-loss\n"
        return b""
    @staticmethod
    def sha(path):
        p=Path(path)
        return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,name): return Path(root)/name


def fixture_context():
    p267=NS(dataset=data_fixture,validate_data=lambda d:None,score=lambda d,r:r,
            check_logits=lambda x,n: b.require(x.shape==(n,256) and x.dtype==torch.float64 and bool(torch.isfinite(x).all()),"logits"))
    c=NS(p267=p267,c270=NS(score=lambda d,r,p:r,prompt_dataset=lambda *a:{"triple":True},validate_dataset=lambda *a:None),
         c278=NS(MeanFinalDualReadout=Readout),c269=NS(query_span_mask=None),
         factory=NS(new_model=lambda seed:Weights(13488)),reader=None,base=NS(fingerprint=fingerprint),core=None,audit=Audit())
    parent=NS(score_quad=lambda d,r,c:r,dataset=lambda d:{"quad":True},validate_dataset=lambda *a:None)
    c282=NS(training_tables=lambda d,c:(torch.zeros((2,3,192,48),dtype=torch.int64),torch.tensor([48,49]*96)))
    return parent,c282,c


def records_fixture():
    parent,c282,c=fixture_context(); d=data_fixture(); records=[]
    for seed,arm in b.identities():
        plan=b.schedule(seed,arm,d["TRAIN"])[3]
        records.append(dict(seed=seed,arm=arm,parameters=14256,weights_changed=True,checkpoint_roundtrip=True,
                            initial_sha256="same",final_sha256="changed",reload_max_error=0.,
                            forward_calls=881,row_presentations=46176,core_forward_calls=3524,
                            replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324,
                            fit=dict(steps=800,training_rows=38400,last_ce=.01,**plan),
                            raw={t:score_fixture(t) for t in b.TASKS}))
    return parent,c282,c,d,records


def protection():
    pins={n:"b"*40 for n in b.OWN}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<b.manifest()["source_pins"]: pins["fixture/source/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(b.manifest()["protected_inputs"])}


def result_fixture():
    parent,_,c,d,rr=records_fixture(); _,summary=b.analyze(rr,d,parent,c); pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",diagnostic_execution_valid=True,
                gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False,source_blobs=pins,input_sha256=inputs,
                artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary)


def recount(p):
    s=p["validation_summary"];rr=s["seed_results"]
    for r in rr:
        r["passed"]=r["quad_pass"];r["all_tasks_pass"]=all(r[t+"_pass"] for t in b.TASKS)
    for out,field in (("seed_pass_counts","passed"),("two_char_pass_counts","two_char_pass"),
                      ("triple_pass_counts","triple_pass"),("quad_pass_counts","quad_pass"),("all_tasks_pass_counts","all_tasks_pass")):
        s[out]={a:sum(r[field] for r in rr if r["arm"]==a) for a in b.ARMS}
    return p


def parent_fixture():
    return dict(commit_sha=b.PARENT_EXECUTION,status="FAIL",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
                artifacts=[dict(file=n,sha256=v[0],serialized_bytes=v[1]) for n,v in b.PARENT_ARTIFACTS.items()],
                validation_summary=dict(candidate_gate=False,seed_pass_counts={"two_char_only":0,"mixed_length":3},all_replays=True,all_weights_preserved=True))


class C284Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.threads=torch.get_num_threads();torch.set_num_threads(2)
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.threads)

    def test_01_seal_is_really_executed(self):
        b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_invalid_and_mismatched_seals_rejected(self):
        for seal in ("UNSEALED","F"*64,"0"*64):
            with patch.object(b,"MANIFEST_SHA",seal),self.assertRaises(ValueError):b.validate_seal()

    def test_03_logical_batches_and_profiles_match(self):
        a=b.schedule(b.SEEDS[0],b.ARMS[0],data_fixture()["TRAIN"])
        c=b.schedule(b.SEEDS[0],b.ARMS[1],data_fixture()["TRAIN"])
        self.assertTrue(torch.equal(a[0],c[0]));self.assertTrue(torch.equal(a[1],c[1]))
        self.assertEqual(a[3]["logical_batch_sha256"],c[3]["logical_batch_sha256"])

    def test_04_maximum_length_and_exposures_match_registration(self):
        for arm in b.ARMS:
            x,p,l,plan=b.schedule(b.SEEDS[0],arm,data_fixture()["TRAIN"])
            self.assertEqual(int(l.max()),1);self.assertEqual(plan["row_exposures"],[200]*192)
            self.assertEqual(plan["per_length_row_exposures"],[[n]*192 for n in b.manifest()["per_length_row_exposures"][arm]])
            self.assertEqual(plan["length_profile_updates"],b.manifest()["length_profile_updates"][arm])
        self.assertEqual(b.manifest()["maximum_training_length"],3)

    def test_05_epochs_are_complete_query_pairs(self):
        x,_,_,_=b.schedule(b.SEEDS[0],b.ARMS[1],data_fixture()["TRAIN"])
        for epoch in range(200):self.assertEqual(sorted(x[4*epoch:4*epoch+4].flatten().tolist()),list(range(192)))
        self.assertTrue(bool((x[:,1::2]==x[:,::2]+1).all()))

    def test_06_schedule_reproduces_and_changes_with_seed(self):
        r=data_fixture()["TRAIN"]
        self.assertEqual(b.schedule(b.SEEDS[0],b.ARMS[0],r)[3],b.schedule(b.SEEDS[0],b.ARMS[0],r)[3])
        self.assertNotEqual(b.schedule(b.SEEDS[0],b.ARMS[0],r)[3]["logical_batch_sha256"],b.schedule(b.SEEDS[1],b.ARMS[0],r)[3]["logical_batch_sha256"])

    def test_07_bad_pairs_and_unknown_identity_rejected(self):
        r=data_fixture()["TRAIN"];r[1]["query"]=0
        with self.assertRaises(ValueError):b.schedule(b.SEEDS[0],b.ARMS[0],r)
        with self.assertRaises(ValueError):b.schedule(282001,b.ARMS[0],data_fixture()["TRAIN"])
        with self.assertRaises(ValueError):b.schedule(b.SEEDS[0],"two_char_only",data_fixture()["TRAIN"])

    def test_08_paired_model_capacity_and_independent_storage(self):
        _,_,c=fixture_context();models=b.make_models(b.SEEDS[0],c)
        self.assertEqual(fingerprint(models[b.ARMS[0]]),fingerprint(models[b.ARMS[1]]))
        with torch.no_grad():next(models[b.ARMS[1]].parameters()).add_(1.)
        self.assertNotEqual(fingerprint(models[b.ARMS[0]]),fingerprint(models[b.ARMS[1]]))

    def test_09_wrong_capacity_rejected(self):
        _,_,c=fixture_context();c.factory.new_model=lambda s:Weights(13489)
        with self.assertRaisesRegex(ValueError,"capacity"):b.make_models(b.SEEDS[0],c)

    def test_10_fit_real_updates_only_choose_registered_lengths(self):
        class Toy(torch.nn.Module):
            def __init__(self):super().__init__();self.bias=torch.nn.Parameter(torch.zeros(256,dtype=torch.float64));self.seen=[]
            def forward(self,x,t):
                self.seen.append(int(x[0,0]));assert len(x)==48 and bool((t==0).all())
                return self.bias.expand(len(x),-1)
        x=torch.zeros((2,3,192,48),dtype=torch.int64);x[1]=1;y=torch.tensor([48,49]*96)
        for arm in b.ARMS:
            m=Toy()
            with contextlib.redirect_stdout(io.StringIO()):r=b.fit(m,data_fixture(),x,y,b.SEEDS[0],arm)
            expected=[1]*800 if arm==b.ARMS[0] else [e%2 for e in range(200) for _ in range(4)]
            self.assertEqual(m.seen,expected);self.assertEqual((r["steps"],r["training_rows"]),(800,38400))
            self.assertFalse(m.training);self.assertTrue(bool((m.bias.detach()!=0).any()))

    def test_11_fit_bad_shape_stops_before_model(self):
        with self.assertRaises(ValueError):b.fit(None,{},torch.zeros(1),torch.zeros(1),b.SEEDS[0],b.ARMS[0])

    def test_12_train_then_freeze_then_evaluate_order(self):
        parent,_,c=fixture_context();model=b.make_models(b.SEEDS[0],c)[b.ARMS[0]];events=[]
        @contextlib.contextmanager
        def counted(*a):yield [881,46176],[3524]
        c.p267.counted=counted
        def fitted(m,*a):
            events.append("fit")
            with torch.no_grad():
                for p in m.parameters():p.add_(1.)
            m.eval();return {"steps":800}
        def evaluation(m,*a):
            events.append("evaluate");self.assertFalse(m.training);self.assertFalse(any(p.requires_grad for p in m.parameters()))
            return {}
        with patch.object(b,"fit",side_effect=fitted),patch.object(b,"evaluate",side_effect=evaluation):
            record,state=b.train_one(model,{}, {}, {},None,None,b.SEEDS[0],b.ARMS[0],parent,c)
        self.assertEqual(events,["fit","evaluate"]);self.assertTrue(record["weights_changed"]);self.assertTrue(state)

    def test_13_evaluate_requires_frozen_and_dispatches_all_tasks(self):
        parent,_,c=fixture_context();m=Weights(1);events=[]
        c.p267.evaluate=lambda *a:(events.append("two") or {})
        c.c270.evaluate_new=lambda *a:(events.append("three") or {})
        parent.evaluate_quad=lambda *a:(events.append("four") or {})
        with self.assertRaisesRegex(ValueError,"frozen"):b.evaluate(m,{}, {}, {},parent,c)
        m.eval();m.requires_grad_(False);raw=b.evaluate(m,{}, {}, {},parent,c)
        self.assertEqual(events,["two","three","four"]);self.assertEqual(set(raw),set(b.TASKS))

    def test_14_replay_raw_drift_rejected(self):
        _,_,c=fixture_context();d=dict(TRAIN=[0],HOLDOUT=[0])
        raw={t:{s:{"p":{v:torch.zeros((1,256),dtype=torch.float64) for v in ("normal","evidence_blind","query_blind")}} for s in d} for t in b.TASKS}
        self.assertEqual(b.replay_error(raw,copy.deepcopy(raw),d,c),0.)
        changed=copy.deepcopy(raw);changed["quad"]["TRAIN"]["p"]["normal"][0,0]=1e-4
        with self.assertRaisesRegex(ValueError,"replay"):b.replay_error(changed,raw,d,c)

    def test_15_strict_state_replay_freezes_and_records_work(self):
        parent,_,c=fixture_context();m=Weights(2);ref=Weights(2)
        with torch.no_grad():ref.weight.add_(1.)
        record=dict(final_sha256=fingerprint(ref),raw={})
        @contextlib.contextmanager
        def counted(*a):yield [81,7776],[324]
        c.p267.counted=counted
        def ev(model,*a):
            self.assertFalse(model.training);self.assertFalse(any(p.requires_grad for p in model.parameters()));return {}
        with patch.object(b,"evaluate",side_effect=ev),patch.object(b,"replay_error",return_value=0.):
            b.replay_one(m,ref.state_dict(),record,{}, {}, {},parent,c)
        self.assertTrue(record["checkpoint_roundtrip"]);self.assertEqual(record["replay_forward_calls"],81)

    def test_16_analyze_all_models_tasks_and_contrasts(self):
        parent,_,c,d,rr=records_fixture();metrics,s=b.analyze(rr,d,parent,c)
        self.assertEqual((len(metrics),len(s["contrasts"])),(10,180));self.assertEqual(s["quad_pass_counts"],dict.fromkeys(b.ARMS,5))
        self.assertEqual({x["task"] for x in s["contrasts"]},set(b.TASKS))

    def test_17_control_quad_failure_cannot_fail_candidate(self):
        p=result_fixture();p["validation_summary"]["seed_results"][0]["quad_pass"]=False
        b.validate_result(recount(p))

    def test_18_single_candidate_failure_requires_negative(self):
        p=result_fixture();p["validation_summary"]["seed_results"][1]["quad_pass"]=False;recount(p)
        with self.assertRaises(ValueError):b.validate_result(p)
        p["validation_summary"]["candidate_gate"]=False;p["status"]="FAIL";b.validate_result(p)

    def test_19_seen_task_failure_does_not_redefine_primary(self):
        p=result_fixture();r=p["validation_summary"]["seed_results"][1];r["two_char_pass"]=False;recount(p)
        b.validate_result(p);self.assertTrue(r["quad_pass"]);self.assertFalse(r["all_tasks_pass"])

    def test_20_claims_boolean_workload_and_gate_mismatch_rejected(self):
        p=result_fixture()
        for k in ("gate_f_candidate","production_adoption","arbitrary_length_claim"):
            q=copy.deepcopy(p);q[k]=True
            with self.assertRaises(ValueError):b.validate_result(q)
        p["validation_summary"]["new_checkpoint_writes"]=True
        with self.assertRaises(ValueError):b.validate_result(p)

    def test_21_nonfinite_and_missing_record_rejected(self):
        parent,_,c,d,rr=records_fixture();rr[0]["reload_max_error"]=float("nan")
        with self.assertRaises(ValueError):b.analyze(rr,d,parent,c)
        rr[0]["reload_max_error"]=0.;rr.pop()
        with self.assertRaises(ValueError):b.analyze(rr,d,parent,c)

    def test_22_wrong_schedule_and_mismatched_initial_pair_rejected(self):
        parent,_,c,d,rr=records_fixture();rr[0]["fit"]["steps"]+=1
        with self.assertRaisesRegex(ValueError,"fit plan"):b.analyze(rr,d,parent,c)
        rr[0]["fit"]["steps"]-=1;rr[1]["initial_sha256"]="different"
        with self.assertRaisesRegex(ValueError,"matched states"):b.analyze(rr,d,parent,c)

    def test_23_contrast_pair_identity_checked(self):
        parent,_,c,d,rr=records_fixture();rr[1]["raw"]["quad"]["totals"][0]["profile"]="wrong"
        with self.assertRaisesRegex(ValueError,"contrast identity"):b.analyze(rr,d,parent,c)

    def test_24_all_parent_hashes_and_correct_dispatch(self):
        paths=[(Path("/c284-fixture")/str(i)/"summary.json").resolve() for i in range(10)]
        mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True));payload=parent_fixture()
        parent=NS(verify_artifacts=Mock(return_value=(payload,[])),validate_result=Mock());c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
        with patch.object(b,"context",return_value=(parent,None,c)):
            b.load_parent(paths);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for p in paths:
                old=mapping[str(p)];mapping[str(p)]="0"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError):b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(p)]=old
            del payload["source_blobs"][b.PARENT_SOURCE]
            with self.assertRaisesRegex(ValueError,"source"):b.load_parent(paths)

    def test_25_parent_neural_calls_and_writes_blocked(self):
        paths=[Path(str(i)).resolve() for i in range(10)];mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True))
        parent=NS(verify_artifacts=Mock());c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
        with patch.object(b,"context",return_value=(parent,None,c)):
            parent.verify_artifacts.side_effect=lambda *a:torch.nn.Identity()(torch.ones(1))
            with self.assertRaisesRegex(RuntimeError,"forbids neural"):b.load_parent(paths)
            parent.verify_artifacts.side_effect=lambda *a:torch.save({},"MUST_NOT_BE_WRITTEN.pt")
            with self.assertRaisesRegex(RuntimeError,"forbids writes"):b.load_parent(paths)
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]),1.)

    def test_26_suite_constructed_with_exact_exclusion(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(b.manifest()["loaded_tests"]-1)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            suite=b.regression_suite(Path.cwd());self.assertEqual({t.id() for t in b.flatten(suite)},set(ids)-{b.EXCLUDED})
            self.assertEqual(suite.countTestCases(),b.manifest()["focused_tests"])

    def test_27_real_run_dispatch_persistence_and_no_overwrite(self):
        parent,c282,c,d,rr=records_fixture();events=[]
        def pc(*a):events.append("precheck");return protection()
        def train(model,data,triple,quad,tokens,targets,seed,arm,par,ctx):
            events.append("train");return copy.deepcopy(rr[b.identities().index((seed,arm))]),{"x":torch.ones(1)}
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(parent,c282,c)),\
             patch.object(b,"precheck",side_effect=pc),patch.object(b,"load_parent",return_value=parent_fixture()),\
             patch.object(b,"train_one",side_effect=train),patch.object(b,"replay_one",side_effect=lambda *a:events.append("replay")),\
             contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*10,output_dir=out,expected_head="f"*40)
            self.assertEqual(events,["precheck"]+["train"]*10+["replay"]*10+["precheck"])
            q,_=b.verify_artifacts(out,["x"]*10,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*10,output_dir=out,expected_head="f"*40)

    def test_28_artifact_hash_and_semantic_tampering_rejected(self):
        parent,c282,c,d,rr=records_fixture()
        def train(m,d,t,q,x,y,s,a,p,c):return copy.deepcopy(rr[b.identities().index((s,a))]),{"x":torch.ones(1)}
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(parent,c282,c)),\
             patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=parent_fixture()),\
             patch.object(b,"train_one",side_effect=train),patch.object(b,"replay_one"),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*10,output_dir=out,expected_head="f"*40)
            f=out/"measurements.json";f.write_text("[]")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*10,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==f.name);a.update(sha256=Audit.sha(f),serialized_bytes=f.stat().st_size)
            (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*10,"f"*40)

    def test_29_bad_checkpoint_schema_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"bad.pt";torch.save(dict(schema="wrong",identities=[],states=[]),p)
            with self.assertRaises(ValueError):b.load_bundle(p)

    def test_30_cli_ten_summaries_order(self):
        args=["prog","--summaries"]+[str(i) for i in range(10)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",args),patch.object(b,"run") as run:
            b.main();self.assertEqual(run.call_args.kwargs["summaries"],[Path(str(i)) for i in range(10)])

    def test_31_runner_embedded_python_phase_and_path_count(self):
        root=Path(__file__).resolve().parents[1];r=(root/"tools/run_c284.ps1").read_text(encoding="utf-8");l=(root/"tools/invoke_c284.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",r,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:12]",blocks[2]);self.assertIn("head = sys.argv[12]",blocks[2])
        self.assertLess(l.index("-Mode Validate"),l.index("-Mode Execute"));self.assertLess(l.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),l.index("publish_experiment_log.ps1"))
        self.assertIn("Parser]::ParseFile",l);self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',l)),10)

    def test_32_immutable_inventory_import_and_protection_counts(self):
        root=Path(__file__).resolve().parents[1]
        self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()["own_tests"])
        for n in b.OWN:self.assertTrue((root/n).is_file())
        imports=[n for n in ast.walk(ast.parse(Path(b.__file__).read_text(encoding="utf-8"))) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual([n.names[0].name for n in imports],["model_c283_frozen_four_character_transfer"])
        self.assertEqual(b.manifest()["source_pins"],544+len(b.OWN));self.assertEqual(b.manifest()["protected_inputs"],964+1+len(b.PARENT_ARTIFACTS)+len(b.OWN))


if __name__=="__main__":unittest.main()
