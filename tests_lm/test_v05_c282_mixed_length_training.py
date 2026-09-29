"""C282 behavioral tests; inherited models/archives are mocked unless explicitly stated."""
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
from fold_lm.v05_benchmarks import model_c282_mixed_length_training as b


def data_fixture():
    rows = [dict(language="en", entities=[0,1], values=[i,i+1], permutation=[0,1], query=q,
                 target=48+q, id=f"{i}:{q}") for i in range(96) for q in range(2)]
    return dict(TRAIN=rows, HOLDOUT=[dict(id="HOLDOUT-SENTINEL", target=55)])


def prefix(raw):
    return torch.tensor([257]+list(raw)+[258]+[256]*(46-len(raw)),dtype=torch.int64)


def score_fixture(task, passed=True):
    profiles = ("doubled","shared_prefix","shared_suffix") if task == "two" else ("tripled","shared_prefix2","shared_suffix2")
    totals = [dict(split=s,profile=p,language=l,rows=n,pairs=n//2,correct=n,collapsed_pairs=0)
              for s,n in (("TRAIN",96),("HOLDOUT",48)) for p in profiles for l in ("en","ja")]
    return dict(passed=passed,totals=totals,cells=[],two_order=[])


def fingerprint(model):
    return hashlib.sha256(b"".join(x.detach().cpu().numpy().tobytes() for x in model.state_dict().values())).hexdigest()


class Backbone(torch.nn.Module):
    def __init__(self, n=13488):
        super().__init__(); self.weight=torch.nn.Parameter(torch.ones(n,dtype=torch.float64))


class Readout(torch.nn.Module):
    def __init__(self,backbone,seed,reader,span):
        super().__init__(); self.backbone=backbone; self.read=Backbone(768)


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
    def renderer(tag):
        def render(row,profile,view):
            assert view=="normal" and "HOLDOUT" not in row["id"]
            return tag+":"+profile+":"+row["id"]
        return render
    p267=NS(validate_data=lambda d:None,dataset=data_fixture,render=renderer("two"),PROFILES=("a","b","c"),score=lambda d,r:r)
    c270=NS(render=renderer("tri"),PROFILES=("x","y","z"),score=lambda d,r,p:r,
            prompt_dataset=lambda d,p:{"fixture":True},validate_dataset=lambda *a:None)
    return NS(p267=p267,c270=c270,factory=NS(prefix_tensor=prefix,new_model=lambda s:Backbone()),
              c278=NS(MeanFinalDualReadout=Readout),c269=NS(query_span_mask=None),base=NS(fingerprint=fingerprint),
              reader=None,core=None,audit=Audit(),previous=NS(replay_one=Mock()),parent=NS())


def protection():
    pins={n:"b"*40 for n in b.OWN}; pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<538: pins["fixture/source/"+str(len(pins))]="b"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(950)}


def records_fixture():
    c=fixture_context();data=data_fixture();x,y=b.training_tables(data,c);thash=b.table_hash(x,y)
    records=[]
    for seed,arm in b.identities():
        plan=b.schedule(seed,arm,data["TRAIN"])[3]
        records.append(dict(seed=seed,arm=arm,parameters=14256,weights_changed=True,checkpoint_roundtrip=True,
                            initial_sha256="same",final_sha256="changed",reload_max_error=0.,
                            forward_calls=854,row_presentations=43584,core_forward_calls=3416,
                            replay_forward_calls=54,replay_row_presentations=5184,replay_core_forward_calls=216,
                            fit=dict(steps=800,training_rows=38400,last_ce=.01,table_sha256=thash,**plan),
                            raw_two=score_fixture("two"),raw_triple=score_fixture("triple")))
    return c,data,records


def result_fixture():
    c,d,rr=records_fixture();_,summary=b.analyze(rr,d,c);pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,commit_sha="f"*40,status="PASS",
                diagnostic_execution_valid=True,gate_f_candidate=False,production_adoption=False,unseen_length_success_claim=False,
                source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=summary)


def parent_fixture():
    primary={task:dict(totals={arm:dict(mask_only_cells=0) for arm in ("all_token_dual","evidence_only_dual")})
             for task in ("two_char_all","triple_all")}
    primary["triple_all"]["criteria"]={"accuracy":{"candidate_fail":85}}
    return dict(commit_sha=b.PARENT_EXECUTION,status="PASS",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
                artifacts=[dict(file=n,sha256=v[0],serialized_bytes=v[1]) for n,v in b.PARENT_ARTIFACTS.items()],
                validation_summary=dict(diagnostic_complete=True,capability_gate_applicable=False,model_forward_calls=0,primary=primary))


class C282Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old_threads=torch.get_num_threads();torch.set_num_threads(2)

    @classmethod
    def tearDownClass(cls):
        torch.set_num_threads(cls.old_threads)

    def test_01_real_seal_validates(self):
        b.validate_seal(); self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_bad_seals_rejected(self):
        for seal in ("UNSEALED","0"*64,"F"*64):
            with patch.object(b,"MANIFEST_SHA",seal),self.assertRaises(ValueError): b.validate_seal()

    def test_03_logical_batches_match(self):
        rows=data_fixture()["TRAIN"]
        a=b.schedule(b.SEEDS[0],b.ARMS[0],rows);c=b.schedule(b.SEEDS[0],b.ARMS[1],rows)
        self.assertTrue(torch.equal(a[0],c[0]));self.assertTrue(torch.equal(a[1],c[1]))
        self.assertEqual(a[3]["logical_batch_sha256"],c[3]["logical_batch_sha256"])
        self.assertEqual(tuple(a[0].shape),(800,48))

    def test_04_length_exposures_are_exact(self):
        for arm in b.ARMS:
            ids,p,l,plan=b.schedule(b.SEEDS[0],arm,data_fixture()["TRAIN"])
            self.assertEqual(plan["row_exposures"],[200]*192)
            self.assertEqual(plan["length_profile_updates"],b.manifest()["length_profile_updates"][arm])
            self.assertEqual(plan["per_length_row_exposures"],[[n]*192 for n in b.manifest()["per_length_row_exposures"][arm]])
        self.assertEqual(int((l==1).sum()),400)

    def test_05_each_epoch_is_complete_and_paired(self):
        rows=data_fixture()["TRAIN"];ids,_,_,_=b.schedule(b.SEEDS[0],b.ARMS[1],rows)
        for epoch in range(200): self.assertEqual(sorted(ids[epoch*4:epoch*4+4].flatten().tolist()),list(range(192)))
        self.assertTrue(bool((ids[:,1::2]==ids[:,::2]+1).all()))

    def test_06_schedule_reproducible_and_seed_sensitive(self):
        r=data_fixture()["TRAIN"]
        a=b.schedule(b.SEEDS[0],b.ARMS[0],r);c=b.schedule(b.SEEDS[0],b.ARMS[0],r)
        self.assertEqual(a[3],c[3]);self.assertTrue(torch.equal(a[0],c[0]))
        self.assertNotEqual(a[3]["logical_batch_sha256"],b.schedule(b.SEEDS[1],b.ARMS[0],r)[3]["logical_batch_sha256"])

    def test_07_bad_pairs_and_unknown_seed_rejected(self):
        r=data_fixture()["TRAIN"];r[1]["query"]=0
        with self.assertRaises(ValueError): b.schedule(b.SEEDS[0],b.ARMS[0],r)
        with self.assertRaises(ValueError): b.schedule(280004,b.ARMS[0],data_fixture()["TRAIN"])

    def test_08_train_tables_exclude_holdout_and_blind_views(self):
        c=fixture_context();d=data_fixture();x,y=b.training_tables(d,c)
        self.assertEqual(tuple(x.shape),(2,3,192,48));self.assertEqual(y.tolist(),[48,49]*96)
        self.assertFalse(torch.equal(x[0],x[1]))
        d["HOLDOUT"][0]["target"]=99;x2,y2=b.training_tables(d,c)
        self.assertTrue(torch.equal(x,x2));self.assertTrue(torch.equal(y,y2))

    def test_09_unchanged_architecture_capacity_and_independent_storage(self):
        c=fixture_context();m=b.make_models(b.SEEDS[0],c)
        self.assertTrue(all(type(x) is Readout for x in m.values()))
        self.assertEqual(fingerprint(m[b.ARMS[0]]),fingerprint(m[b.ARMS[1]]))
        with torch.no_grad(): next(m[b.ARMS[1]].parameters()).add_(1)
        self.assertNotEqual(fingerprint(m[b.ARMS[0]]),fingerprint(m[b.ARMS[1]]))

    def test_10_wrong_capacity_rejected(self):
        c=fixture_context();c.factory.new_model=lambda s:Backbone(13489)
        with self.assertRaises(ValueError): b.make_models(b.SEEDS[0],c)

    def test_11_fit_runs_real_800_update_length_schedule(self):
        class Toy(torch.nn.Module):
            def __init__(self):
                super().__init__();self.bias=torch.nn.Parameter(torch.zeros(256,dtype=torch.float64));self.seen=[]
            def forward(self,x,t):
                self.seen.append(int(x[0,0]));assert len(x)==48 and bool((t==0).all())
                return self.bias.expand(len(x),-1)
        x=torch.zeros((2,3,192,48),dtype=torch.int64);x[1]=1;y=torch.tensor([48,49]*96)
        m=Toy()
        with contextlib.redirect_stdout(io.StringIO()): r=b.fit(m,data_fixture(),x,y,b.SEEDS[0],b.ARMS[1])
        self.assertEqual((len(m.seen),sum(m.seen)),(800,400))
        self.assertEqual((r["steps"],r["training_rows"]),(800,38400));self.assertFalse(m.training)
        self.assertTrue(bool((m.bias.detach()!=0).any()))
        self.assertEqual(m.seen,[e%2 for e in range(200) for _ in range(4)])

    def test_12_fit_bad_shape_fails_before_training(self):
        with self.assertRaises(ValueError): b.fit(None,{},torch.zeros(1),torch.zeros(1),b.SEEDS[0],b.ARMS[0])

    def test_13_control_failure_cannot_fail_candidate(self):
        p=result_fixture();s=p["validation_summary"];s["seed_results"][0].update(two_char_pass=False,passed=False)
        s["seed_pass_counts"][b.ARMS[0]]=4;s["two_char_pass_counts"][b.ARMS[0]]=4
        b.validate_result(p)

    def test_14_one_candidate_failure_requires_negative(self):
        p=result_fixture();s=p["validation_summary"];s["seed_results"][1].update(triple_pass=False,passed=False)
        s["seed_pass_counts"][b.ARMS[1]]=4;s["triple_pass_counts"][b.ARMS[1]]=4
        with self.assertRaises(ValueError): b.validate_result(p)
        s["candidate_gate"]=False;p["status"]="FAIL";b.validate_result(p)

    def test_15_unseen_length_and_gate_f_claims_forbidden(self):
        p=result_fixture()
        for k in ("unseen_length_success_claim","gate_f_candidate","production_adoption"):
            q=copy.deepcopy(p);q[k]=True
            with self.assertRaises(ValueError): b.validate_result(q)

    def test_16_all_eight_parent_hashes_and_dispatch(self):
        payload=parent_fixture();paths=[(Path("/c282-fixture")/str(i)/"summary.json").resolve() for i in range(8)]
        sm=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True))
        c=NS(audit=NS(sha=lambda p:sm[str(p)]),parent=NS(verify_artifacts=Mock(return_value=(payload,{})),validate_result=Mock()))
        b.load_parent(paths,c)
        c.parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
        for p in paths:
            old=sm[str(p)];sm[str(p)]="0"*64;c.parent.verify_artifacts.reset_mock()
            with self.assertRaises(ValueError): b.load_parent(paths,c)
            c.parent.verify_artifacts.assert_not_called();sm[str(p)]=old

    def test_17_parent_source_pin_and_artifact_sizes_checked(self):
        payload=parent_fixture();paths=[Path(str(i)).resolve() for i in range(8)]
        sm=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True))
        c=NS(audit=NS(sha=lambda p:sm[str(p)]),parent=NS(verify_artifacts=Mock(return_value=(payload,{})),validate_result=Mock()))
        del payload["source_blobs"][b.PARENT_SOURCE]
        with self.assertRaises(ValueError): b.load_parent(paths,c)
        payload["source_blobs"][b.PARENT_SOURCE]=b.PARENT_BLOB;payload["artifacts"][0]["serialized_bytes"]+=1
        with self.assertRaises(ValueError): b.load_parent(paths,c)

    def test_18_parent_neural_execution_blocked(self):
        paths=[Path(str(i)).resolve() for i in range(8)];sm=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True))
        c=NS(audit=NS(sha=lambda p:sm[str(p)]),parent=NS(verify_artifacts=lambda *a:torch.nn.Identity()(torch.ones(1))))
        with self.assertRaisesRegex(RuntimeError,"forbids neural"): b.load_parent(paths,c)
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]),1.)

    def test_19_analyze_reconstructs_tasks_and_all_contrasts(self):
        c,d,rr=records_fixture();metrics,s=b.analyze(rr,d,c)
        self.assertEqual((len(metrics),len(s["contrasts"])),(10,90))
        self.assertEqual(s["seed_pass_counts"],dict.fromkeys(b.ARMS,5))
        self.assertTrue(s["candidate_gate"]);self.assertFalse(s["unseen_length_success_claim"])

    def test_20_training_table_identity_checked(self):
        c,d,rr=records_fixture();rr[0]["fit"]["table_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"fit plan"): b.analyze(rr,d,c)

    def test_21_logical_initial_pair_mismatch_rejected(self):
        c,d,rr=records_fixture();rr[1]["initial_sha256"]="different"
        with self.assertRaisesRegex(ValueError,"matched states"): b.analyze(rr,d,c)

    def test_22_replay_and_record_order_rejected(self):
        c,d,rr=records_fixture();rr[0]["reload_max_error"]=float("nan")
        with self.assertRaises(ValueError): b.analyze(rr,d,c)
        rr[0]["reload_max_error"]=0.;rr.reverse()
        with self.assertRaises(ValueError): b.analyze(rr,d,c)

    def test_23_no_extra_steps_or_wrong_length_exposures(self):
        c,d,rr=records_fixture();rr[1]["fit"]["per_length_row_exposures"][1][0]+=1
        with self.assertRaises(ValueError): b.analyze(rr,d,c)
        p=result_fixture();p["validation_summary"]["train_steps"]+=1
        with self.assertRaises(ValueError): b.validate_result(p)

    def test_24_real_suite_construction_and_exact_exclusion(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n): super().__init__();self.n=n
            def runTest(self): pass
            def id(self): return self.n
        ids=["fixture."+str(i) for i in range(b.manifest()["loaded_tests"]-1)]+[b.EXCLUDED]
        suite=unittest.TestSuite(Dummy(i) for i in ids)
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=suite):
            got=b.regression_suite(Path.cwd())
            self.assertEqual({t.id() for t in b.flatten(got)},set(ids)-{b.EXCLUDED})
            self.assertEqual(got.countTestCases(),b.manifest()["focused_tests"])

    def test_25_real_run_and_persistence_roundtrip(self):
        c,d,rr=records_fixture();events=[]
        def train(model,data,prompts,tokens,targets,seed,arm,ctx):
            events.append("train");return copy.deepcopy(rr[b.identities().index((seed,arm))]),{"x":torch.ones(1)}
        def pc(*a): events.append("precheck");return protection()
        c.previous.replay_one=Mock(side_effect=lambda *a:events.append("replay"))
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=c),patch.object(b,"precheck",side_effect=pc),\
             patch.object(b,"load_parent",return_value=parent_fixture()),patch.object(b,"train_one",side_effect=train),\
             contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"run";p=b.run(summaries=["x"]*8,output_dir=out,expected_head="f"*40)
            self.assertEqual(events,["precheck"]+["train"]*10+["replay"]*10+["precheck"])
            q,_=b.verify_artifacts(out,["x"]*8,"f"*40);self.assertEqual(p,q)
            with self.assertRaises(FileExistsError): b.run(summaries=["x"]*8,output_dir=out,expected_head="f"*40)

    def test_26_bundle_schema_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"bad.pt";torch.save(dict(schema="wrong",identities=[],states=[]),p)
            with self.assertRaises(ValueError): b.load_bundle(p)

    def test_27_whole_flags_and_boolean_counts_rejected(self):
        p=result_fixture();p["validation_summary"]["seed_results"][0]["passed"]=False
        with self.assertRaises(ValueError): b.validate_result(p)
        p=result_fixture();p["validation_summary"]["new_checkpoint_writes"]=True
        with self.assertRaises(ValueError): b.validate_result(p)

    def test_28_scoring_contrast_identity_must_match(self):
        c,d,rr=records_fixture();rr[1]["raw_triple"]["totals"][0]["profile"]="wrong"
        with self.assertRaisesRegex(ValueError,"contrast identity"): b.analyze(rr,d,c)

    def test_29_cli_eight_summary_order(self):
        args=["prog","--summaries"]+[str(i) for i in range(8)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",args),patch.object(b,"run") as run:
            b.main();self.assertEqual(run.call_args.kwargs["summaries"],[Path(str(i)) for i in range(8)])

    def test_30_runner_embedded_python_and_phase_order(self):
        root=Path(__file__).resolve().parents[1];r=(root/"tools/run_c282.ps1").read_text(encoding="utf-8")
        l=(root/"tools/invoke_c282.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",r,re.S);self.assertEqual(len(blocks),3)
        for code in blocks: ast.parse(code)
        self.assertIn("sys.argv[2:10]",blocks[2]);self.assertIn("head = sys.argv[10]",blocks[2])
        self.assertLess(l.index("-Mode Validate"),l.index("-Mode Execute"))
        self.assertLess(l.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),l.index("publish_experiment_log.ps1"))
        self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',l)),8)

    def test_31_only_new_parent_is_direct_import(self):
        source=Path(b.__file__).read_text(encoding="utf-8");tree=ast.parse(source)
        imports=[n for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual(len(imports),1);self.assertEqual(imports[0].names[0].name,"model_c281_saved_support_transition_audit")
        self.assertEqual(b.manifest()["source_pins"],532+len(b.OWN))
        self.assertEqual(b.manifest()["protected_inputs"],940+1+len(b.PARENT_ARTIFACTS)+len(b.OWN))

    def test_32_lifecycle_and_own_test_inventory(self):
        root=Path(__file__).resolve().parents[1];h=(root/"docs/experiment-ledger-and-handoff.md").read_text(encoding="utf-8")
        formal=re.search(r"(?ms)^## Formal state\s+(.*?)(?=^## |\Z)",h);self.assertIsNotNone(formal)
        self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        if re.search(r"\bC282 ACTIVE /",formal.group(1)): self.assertIn(b.MANIFEST_SHA,h)
        else:
            accepted=root/"docs/experiment-ledger-addendum-c282-c283.md"
            self.assertTrue(accepted.is_file());self.assertIn(b.MANIFEST_SHA,accepted.read_text(encoding="utf-8"))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()["own_tests"])
        for n in b.OWN:self.assertTrue((root/n).is_file())


if __name__=="__main__":unittest.main()
