"""C285 behavioral fixtures. Real parent archives remain authoritative runtime gates."""
import ast
import contextlib
import copy
import hashlib
import io
import itertools
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock,patch
import torch
from fold_lm.v05_benchmarks import model_c285_saved_length_transfer_audit as b


def sync(metrics):
    for m in metrics:
        for task in b.PROFILES:
            tm=m[task]
            for r in tm["cells"]: r["passed"]=all(r[k]>=v for k,v in b.THRESHOLDS.items() if k!="two_order_accuracy")
            for r in tm["two_order"]: r["passed"]=r["accuracy"]>=.8
            tm["passed"]=all(r["passed"] for r in tm["cells"]+tm["two_order"])
    return metrics


def fail(cell):
    n=cell["rows"];cell.update(correct=n-2,accuracy=(n-2)/n,query_pair_accuracy=(n-2)/n)


def fixture(accepted=True):
    metrics=[]
    for row in b.expected_results():
        m=dict(seed=row["seed"],arm=row["arm"])
        for task,profiles in b.PROFILES.items():
            cells=[];orders=[]
            for split,profile,lang,entities in itertools.product(("TRAIN","HOLDOUT"),profiles,("en","ja"),((0,1),(0,2),(1,2))):
                n=16 if split=="TRAIN" else 8
                common=dict(split=split,profile=profile,language=lang,entities=list(entities),accuracy=1.)
                for perm in (entities,entities[::-1]):
                    cells.append(dict(**common,permutation=list(perm),rows=n,correct=n,pairs=n//2,
                                      collapsed_pairs=0,query_pair_accuracy=1.,evidence_drop=.5,query_drop=.5))
                orders.append(dict(**common,groups=n,both_correct=n))
            if accepted and not row[task+"_pass"]: fail(cells[0])
            m[task]=dict(cells=cells,two_order=orders)
        metrics.append(m)
    return sync(metrics)


def target(m,arm=1,task="quad",split="TRAIN"):
    return next(c for c in m[arm][task]["cells"] if c["split"]==split)


def parent_fixture():
    return dict(commit_sha=b.PARENT_EXECUTION,status="FAIL",source_blobs={b.PARENT_SOURCE:b.PARENT_BLOB},
                artifacts=[dict(file=n,sha256=v[0],serialized_bytes=v[1]) for n,v in b.PARENT_ARTIFACTS.items()],
                validation_summary=dict(candidate_gate=False,all_replays=True,all_pairs_matched=True,seed_results=b.expected_results()))


def protection():
    pins={n:"a"*40 for n in b.OWN};pins[b.PARENT_SOURCE]=b.PARENT_BLOB
    while len(pins)<556: pins["fixture/"+str(len(pins))]="a"*40
    return pins,{"fixture/input/"+str(i):"a"*64 for i in range(991)}


def result_fixture():
    _,s=b.analyze(fixture());pins,inputs=protection()
    return dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,status="PASS",commit_sha="f"*40,
                diagnostic_execution_valid=True,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,
                source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],validation_summary=s)


class Audit:
    @staticmethod
    def sha(path):
        p=Path(path);return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "a"*64
    @staticmethod
    def read_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))
    @staticmethod
    def safe_child(root,n): return Path(root)/n
    @staticmethod
    def git(root,*args):
        if args[0]=="rev-parse": return b"ffffffffffffffffffffffffffffffffffffffff\n"
        if args[0]=="branch": return b"feat/sft-target-loss\n"
        return b""


class C285Tests(unittest.TestCase):
    def test_01_seal_executes(self):
        b.validate_seal();self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_malformed_and_mismatched_seals(self):
        for seal in ("UNSEALED","0"*64,"F"*64):
            with patch.object(b,"MANIFEST_SHA",seal),self.assertRaises(ValueError): b.validate_seal()

    def test_03_complete_grid_and_parent_flags(self):
        report,s=b.analyze(fixture())
        self.assertEqual(len(report["records"]),3240);self.assertEqual(s["parent_results"],b.expected_results())
        self.assertEqual(s["primary"]["quad_between_arms"]["paired_records"],540)

    def test_04_duplicate_rejected(self):
        m=fixture();m[0]["quad"]["cells"].append(copy.deepcopy(m[0]["quad"]["cells"][0]))
        with self.assertRaisesRegex(ValueError,"unique grid"): b.analyze(m)

    def test_05_missing_rejected(self):
        m=fixture();m[0]["quad"]["two_order"].pop()
        with self.assertRaisesRegex(ValueError,"unique grid"): b.analyze(m)

    def test_06_wrong_profile_or_entities(self):
        for k,v in (("profile","bad"),("entities",[0,3])):
            m=fixture();m[0]["quad"]["cells"][0][k]=v
            with self.assertRaises(ValueError): b.analyze(m)

    def test_07_order_independence(self):
        m=fixture();expected=b.analyze(m)
        for r in m:
            for t in b.PROFILES: r[t]["cells"].reverse();r[t]["two_order"].reverse()
        self.assertEqual(b.analyze(m),expected)

    def test_08_nonfinite_and_boolean_metrics(self):
        for v in (float("nan"),float("inf"),True):
            m=fixture();m[0]["quad"]["cells"][0]["accuracy"]=v
            with self.assertRaises(ValueError): b.analyze(m)

    def test_09_discrete_mask_counts(self):
        for drop in (.31,-.5):
            m=fixture(False);target(m)["evidence_drop"]=drop;sync(m)
            with self.assertRaisesRegex(ValueError,"discrete ratio"): b.analyze(m)

    def test_10_correct_count_consistency(self):
        m=fixture();m[0]["quad"]["cells"][0]["correct"]-=1
        with self.assertRaisesRegex(ValueError,"cell counts"): b.analyze(m)

    def test_11_cell_flags(self):
        m=fixture();m[0]["quad"]["cells"][0]["passed"]=False
        with self.assertRaisesRegex(ValueError,"cell pass flag"): b.analyze(m)

    def test_12_task_flags(self):
        m=fixture();m[0]["quad"]["passed"]=False
        with self.assertRaisesRegex(ValueError,"task pass flag"): b.analyze(m)

    def test_13_order_counts(self):
        m=fixture();m[0]["quad"]["two_order"][0]["both_correct"]-=1
        with self.assertRaisesRegex(ValueError,"order counts"): b.analyze(m)

    def test_14_pair_consistency(self):
        m=fixture(False);target(m)["collapsed_pairs"]=1
        with self.assertRaisesRegex(ValueError,"cell counts"): b.analyze(m)

    def test_15_arm_rescue_direction(self):
        m=fixture(False);target(m,0)["evidence_drop"]=0.;_,s=b.analyze(sync(m))
        r=s["primary"]["quad_between_arms"]["criteria"]["evidence_drop"]
        self.assertEqual((r["left_fail_right_pass"],r["left_pass_right_fail"],r["right_minus_left"]),(1,0,-1))

    def test_16_net_zero_does_not_hide_turnover(self):
        m=fixture(False);target(m,0)["evidence_drop"]=0.;target(m,1,split="HOLDOUT")["evidence_drop"]=0.
        _,s=b.analyze(sync(m));r=s["primary"]["quad_between_arms"]["criteria"]["evidence_drop"]
        self.assertEqual((r["left_fail_right_pass"],r["left_pass_right_fail"],r["right_minus_left"]),(1,1,0))

    def test_17_longitudinal_new_failure(self):
        m=fixture(False);target(m)["query_drop"]=0.;_,s=b.analyze(sync(m))
        r=s["primary"]["triple_to_quad"][b.ARMS[1]]["criteria"]["query_drop"]
        self.assertEqual((r["left_fail"],r["right_fail"],r["left_pass_right_fail"]),(0,1,1))

    def test_18_longitudinal_cofailure_and_recovery(self):
        m=fixture(False);target(m,task="triple")["query_drop"]=0.;target(m)["query_drop"]=0.
        target(m,task="triple",split="HOLDOUT")["query_drop"]=0.
        _,s=b.analyze(sync(m));r=s["primary"]["triple_to_quad"][b.ARMS[1]]["criteria"]["query_drop"]
        self.assertEqual((r["both_fail"],r["left_fail_right_pass"]),(1,1,0)[:2])

    def test_19_denominators_and_profile_scope(self):
        _,s=b.analyze(fixture());v=s["primary"]["quad_between_arms"]
        self.assertEqual(v["criteria"]["accuracy"]["evaluable"],360)
        self.assertEqual(v["criteria"]["two_order_accuracy"]["evaluable"],180)
        self.assertEqual(v["totals"]["left"]["rows"],4320)
        self.assertEqual(s["quad_profiles"]["HOLDOUT:shared_suffix3"]["totals"]["left"]["rows"],480)

    def test_20_all_seed_partition_additive(self):
        _,s=b.analyze(fixture());self.assertEqual(set(s["per_seed"]),set(map(str,b.SEEDS)))
        for crit in b.THRESHOLDS:
            for field in ("both_fail","both_pass","left_fail_right_pass","left_pass_right_fail"):
                total=sum(v["quad_between_arms"]["criteria"][crit][field] for v in s["per_seed"].values())
                self.assertEqual(total,s["primary"]["quad_between_arms"]["criteria"][crit][field])

    def test_21_model_identity_and_accepted_flags(self):
        m=fixture();m.reverse()
        with self.assertRaisesRegex(ValueError,"model identities"): b.analyze(m)
        p=result_fixture();p["validation_summary"]["parent_results"][0]["quad_pass"]=False
        with self.assertRaisesRegex(ValueError,"accepted grids"): b.validate_result(p)

    def test_22_mask_only_classification(self):
        m=fixture(False);target(m)["evidence_drop"]=0.
        report,s=b.analyze(sync(m));r=next(r for r in report["records"] if r["failure_class"]=="mask_only")
        self.assertEqual(r["evidence_blind_correct"],16)
        self.assertEqual(s["primary"]["quad_between_arms"]["totals"]["right"]["mask_only_cells"],1)

    def test_23_all_hashes_and_loader_dispatch(self):
        paths=[(Path("/c285-fixture")/str(i)/"summary.json").resolve() for i in range(11)]
        mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True))
        parent=NS(verify_artifacts=Mock(return_value=(parent_fixture(),fixture())),validate_result=Mock())
        c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
        with patch.object(b,"context",return_value=(parent,c)):
            b.load_parent(paths);parent.verify_artifacts.assert_called_once_with(paths[0].parent,paths[1:],b.PARENT_EXECUTION)
            for p in paths:
                old=mapping[str(p)];mapping[str(p)]="0"*64;parent.verify_artifacts.reset_mock()
                with self.assertRaises(ValueError): b.load_parent(paths)
                parent.verify_artifacts.assert_not_called();mapping[str(p)]=old

    def test_24_parent_forbidden_operations(self):
        paths=[Path(str(i)).resolve() for i in range(11)];mapping=dict(zip(map(str,paths),b.SUMMARY_SHAS,strict=True))
        parent=NS(verify_artifacts=Mock());c=NS(audit=NS(sha=lambda p:mapping[str(p)]))
        for action in (lambda *a:torch.nn.Identity()(torch.ones(1)),lambda *a:torch.nn.Linear(1,1).load_state_dict({}),lambda *a:torch.save({},"FORBIDDEN.pt")):
            parent.verify_artifacts.side_effect=action
            with patch.object(b,"context",return_value=(parent,c)),self.assertRaisesRegex(RuntimeError,"C285 forbids"): b.load_parent(paths)
        self.assertEqual(float(torch.nn.Identity()(torch.ones(1))[0]),1.)

    def test_25_parent_pin_artifacts_and_verdict(self):
        b.validate_parent(parent_fixture())
        for mutation in (lambda p:p["source_blobs"].clear(),lambda p:p["artifacts"][0].update(serialized_bytes=0),lambda p:p.update(status="PASS")):
            p=parent_fixture();mutation(p)
            with self.assertRaises(ValueError):b.validate_parent(p)

    def test_26_result_zero_work_and_scope(self):
        p=result_fixture();b.validate_result(p)
        for k in b.ZERO_KEYS:
            for value in (1,False):
                q=copy.deepcopy(p);q["validation_summary"][k]=value
                with self.assertRaises(ValueError):b.validate_result(q)
        p["gate_f_candidate"]=True
        with self.assertRaisesRegex(ValueError,"scope"):b.validate_result(p)

    def test_27_run_roundtrip_and_no_overwrite(self):
        m=fixture();events=[]
        def pc(*a):events.append("precheck");return protection()
        def lp(*a):events.append("parent");return parent_fixture(),m
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(None,NS(audit=Audit()))),\
             patch.object(b,"precheck",side_effect=pc),patch.object(b,"load_parent",side_effect=lp),contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"audit";p=b.run(summaries=["x"]*11,output_dir=out,expected_head="f"*40)
            self.assertEqual(events,["precheck","parent","precheck"])
            q,_=b.verify_artifacts(out,["x"]*11,"f"*40);self.assertEqual(q,p)
            self.assertEqual({f.name for f in out.iterdir()},set(b.OUTPUTS)|{"summary.json"})
            with self.assertRaises(FileExistsError):b.run(summaries=["x"]*11,output_dir=out,expected_head="f"*40)

    def test_28_hash_and_semantic_tamper(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(b,"context",return_value=(None,NS(audit=Audit()))),\
             patch.object(b,"precheck",return_value=protection()),patch.object(b,"load_parent",return_value=(parent_fixture(),fixture())),\
             contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/"audit";p=b.run(summaries=["x"]*11,output_dir=out,expected_head="f"*40)
            f=out/"cell-attribution.json";f.write_text("{}")
            with self.assertRaisesRegex(ValueError,"output bytes"):b.verify_artifacts(out,["x"]*11,"f"*40)
            a=next(a for a in p["artifacts"] if a["file"]==f.name);a.update(sha256=Audit.sha(f),serialized_bytes=f.stat().st_size)
            (out/"summary.json").write_bytes(b.blob(p))
            with self.assertRaisesRegex(ValueError,"persisted"):b.verify_artifacts(out,["x"]*11,"f"*40)

    def test_29_actual_suite_filter(self):
        class Dummy(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def runTest(self):pass
            def id(self):return self.n
        ids=["fixture."+str(i) for i in range(b.manifest()["loaded_tests"]-1)]+[b.EXCLUDED]
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=unittest.TestSuite(Dummy(i) for i in ids)):
            s=b.regression_suite(Path.cwd());self.assertEqual(s.countTestCases(),b.manifest()["focused_tests"])
            self.assertEqual({t.id() for t in b.flatten(s)},set(ids)-{b.EXCLUDED})

    def test_30_cli_paths(self):
        argv=["prog","--summaries"]+[str(i) for i in range(11)]+["--output-dir","out","--expected-head","f"*40]
        with patch.object(sys,"argv",argv),patch.object(b,"run") as run:
            b.main();self.assertEqual(run.call_args.kwargs["summaries"],[Path(str(i)) for i in range(11)])

    def test_31_runner_blocks_order_and_paths(self):
        root=Path(__file__).resolve().parents[1];r=(root/"tools/run_c285.ps1").read_text(encoding="utf-8");l=(root/"tools/invoke_c285.ps1").read_text(encoding="utf-8")
        blocks=re.findall(r"@'\n(.*?)\n'@",r,re.S);self.assertEqual(len(blocks),3)
        for code in blocks:ast.parse(code)
        self.assertIn("sys.argv[2:13]",blocks[2]);self.assertIn("head = sys.argv[13]",blocks[2])
        self.assertLess(l.index("-Mode Validate"),l.index("-Mode Execute"));self.assertLess(l.index("AUTHORING_RUNTIME_PREFLIGHT_FAILED"),l.index("publish_experiment_log.ps1"))
        self.assertIn("Parser]::ParseFile",l);self.assertEqual(len(re.findall(r'runs\\c\d{3}-.*?\\summary.json',l)),11)

    def test_32_immutable_inventory_and_import_pins(self):
        root=Path(__file__).resolve().parents[1];self.assertIn(b.MANIFEST_SHA,(root/b.OWN[4]).read_text(encoding="utf-8"))
        self.assertEqual(len(unittest.defaultTestLoader.getTestCaseNames(type(self))),b.manifest()["own_tests"])
        for n in b.OWN:self.assertTrue((root/n).is_file())
        tree=ast.parse(Path(b.__file__).read_text(encoding="utf-8"))
        imports=[n for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and (n.module or "").startswith("fold_lm")]
        self.assertEqual([n.names[0].name for n in imports],["model_c284_max_length_matched_training"])
        self.assertEqual(b.manifest()["source_pins"],550+len(b.OWN))
        self.assertEqual(b.manifest()["protected_inputs"],976+1+len(b.PARENT_ARTIFACTS)+len(b.OWN))


if __name__=="__main__":unittest.main()
