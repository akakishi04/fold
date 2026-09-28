"""C275 authoring tests for saved gate-failure attribution."""
import ast,copy,hashlib,inspect,re,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
import torch
from fold_lm.v05_benchmarks import model_c275_saved_gate_failure_audit as b

def cell(*,passed=True,criterion=None,seed=None):
    vals=dict(accuracy=1.0,query_pair_accuracy=1.0,evidence_drop=.5,query_drop=.5)
    if criterion=="accuracy":vals["accuracy"]=.75
    if criterion=="query_pair_accuracy":vals["query_pair_accuracy"]=.5
    if criterion=="evidence_drop":vals["evidence_drop"]=.1
    if criterion=="query_drop":vals["query_drop"]=.1
    return dict(split="HOLDOUT",profile="shared_prefix2",language="en",entities=[0,1],permutation=[0,1],
        rows=8,correct=8 if vals["accuracy"]>=.9 else 6,pairs=4,collapsed_pairs=0,answer_nll=.1,
        passed=passed,**vals)

def order(*,passed=True):
    return dict(split="HOLDOUT",profile="shared_prefix2",language="en",entities=[0,1],
        groups=8,both_correct=8 if passed else 4,accuracy=1.0 if passed else .5,passed=passed)

def task(*,fail=None):
    c=cell(passed=fail not in ("accuracy","query_pair_accuracy","evidence_drop","query_drop"),criterion=fail)
    o=order(passed=fail!="two_order_accuracy")
    return dict(cells=[c],two_order=[o],totals=[],passed=c["passed"] and o["passed"])

def metrics():
    out=[]
    for seed,arm in b.PARENT_IDENTITIES:
        two=task()
        if arm=="first_boundary":
            two=task(fail="accuracy")
        tri=task()
        if arm=="final_boundary":
            # Every final-boundary triple seed must have at least one registered failure.
            fail={274001:"query_pair_accuracy",274002:"evidence_drop",274003:"accuracy",274004:"query_drop",274005:"two_order_accuracy"}[seed]
            tri=task(fail=fail)
        else:
            tri=task(fail="accuracy")
        out.append(dict(seed=seed,arm=arm,two_char=two,triple=tri))
    return out

def protection():
    pins={f"old-{i}":"fixture" for i in range(490)}
    pins.update({x:"fixture" for x in b.OWN})
    return pins,{f"input-{i}":"0"*64 for i in range(868)}

class C275Tests(unittest.TestCase):
    def test_01_manifest_is_final_and_matches_digest(self):
        self.assertNotEqual(b.MANIFEST_SHA,"PENDING_FINAL_SEAL")
        self.assertRegex(b.MANIFEST_SHA,r"^[0-9a-f]{64}$")
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_signed_margin(self):
        self.assertAlmostEqual(b.signed_margin(.9,.9),0.)
        self.assertLess(b.signed_margin(.8,.9),0.)
        with self.assertRaises(ValueError):b.signed_margin(float("nan"),.9)

    def test_03_answer_failure_accuracy(self):
        r=b.answer_failure(1,"a","triple",cell(passed=False,criterion="accuracy"))
        self.assertEqual(r["failed_criteria"],["accuracy"]);self.assertLess(r["margins"]["accuracy"],0)

    def test_04_answer_failure_query_pair(self):
        r=b.answer_failure(1,"a","triple",cell(passed=False,criterion="query_pair_accuracy"))
        self.assertEqual(r["failed_criteria"],["query_pair_accuracy"])

    def test_05_answer_failure_evidence_drop(self):
        r=b.answer_failure(1,"a","triple",cell(passed=False,criterion="evidence_drop"))
        self.assertEqual(r["failed_criteria"],["evidence_drop"])

    def test_06_answer_failure_query_drop(self):
        r=b.answer_failure(1,"a","triple",cell(passed=False,criterion="query_drop"))
        self.assertEqual(r["failed_criteria"],["query_drop"])

    def test_07_two_order_failure(self):
        r=b.two_order_failure(1,"a","triple",order(passed=False))
        self.assertEqual(r["failed_criteria"],["two_order_accuracy"])
        self.assertLess(r["margins"]["two_order_accuracy"],0)

    def test_08_pass_margin_inconsistency_rejected(self):
        with self.assertRaises(ValueError):b.answer_failure(1,"a","triple",cell(passed=True,criterion="accuracy"))
        bad=order(passed=True);bad["accuracy"]=.5
        with self.assertRaises(ValueError):b.two_order_failure(1,"a","triple",bad)

    def test_09_audit_covers_all_parent_identities(self):
        a,s=b.audit_metrics(metrics())
        self.assertEqual(s["parent_records"],10)
        self.assertTrue(all(s["primary_seed_coverage"].values()))
        self.assertEqual(len(a["parent_passes"]),10)

    def test_10_primary_final_triple_has_near_and_broad_cohorts(self):
        a,_=b.audit_metrics(metrics());p=a["primary_final_boundary_triple"]
        self.assertGreater(p["near_seed_count"],0);self.assertGreater(p["broad_seed_count"],0)
        self.assertEqual({x["seed"] for x in p["near_seed_failure_records"]},set(b.NEAR_SEEDS))
        self.assertEqual({x["seed"] for x in p["broad_seed_failure_records"]},{b.BROAD_SEED})

    def test_11_all_five_failure_criteria_are_attributed(self):
        a,_=b.audit_metrics(metrics())
        counts=a["primary_final_boundary_triple"]["aggregates"]["criterion_counts"]
        self.assertEqual(set(counts),{"accuracy","query_pair_accuracy","evidence_drop","query_drop","two_order_accuracy"})

    def test_12_task_pass_must_equal_all_fixed_records(self):
        m=metrics();m[1]["triple"]["passed"]=True
        with self.assertRaises(ValueError):b.audit_metrics(m)

    def test_13_missing_final_seed_failure_rejected(self):
        m=metrics()
        target=next(x for x in m if x["seed"]==274005 and x["arm"]=="final_boundary")
        target["triple"]=task()
        with self.assertRaises(ValueError):b.audit_metrics(m)

    def test_14_parent_identity_order_required(self):
        m=metrics();m[0],m[1]=m[1],m[0]
        with self.assertRaises(ValueError):b.audit_metrics(m)

    def test_15_aggregate_failure_ranges_negative(self):
        a,_=b.audit_metrics(metrics())
        for v in a["aggregates"]["negative_margin_range"].values():
            self.assertLess(v["min"],0);self.assertLess(v["max"],0)

    def test_16_parent_loader_requires_exact_c274_diagnostic(self):
        payload=dict(status="PASS",commit_sha=b.PARENT_EXECUTION,
            validation_summary={"diagnostic_complete":True,"capability_gate_applicable":False,
                "task_pass_counts":{"final_boundary":{"triple":0,"two_char":4},"first_boundary":{"triple":0,"two_char":0}}},
            artifacts=[dict(file=k,sha256=v) for k,v in b.PARENT_ARTIFACTS.items()])
        pm=metrics()
        fake=SimpleNamespace(verify_artifacts=Mock(return_value=(payload,pm)),validate_result=Mock())
        class Audit:
            @staticmethod
            def sha(path): return b.PARENT_SHA
            @staticmethod
            def read_json(path): return pm
        with patch.object(b,"context",return_value=(fake,None,None,None,None,None,None,None,None,Audit)):
            got,mm=b.load_parent(Path("summary.json"));self.assertEqual(got,payload);self.assertEqual(mm,pm)
            payload["status"]="FAIL"
            with self.assertRaises(ValueError):b.load_parent(Path("summary.json"))

    def test_17_result_validation_is_diagnostic_only(self):
        _,s=b.audit_metrics(metrics());pins,inputs=protection()
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,status="PASS",
            source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],
            validation_summary=s,gate_f_candidate=False,production_adoption=False,capability_gate_applicable=False)
        b.validate_result(p)
        with self.assertRaises(ValueError):b.validate_result(dict(p,status="FAIL"))
        with self.assertRaises(ValueError):b.validate_result(dict(p,capability_gate_applicable=True))

    def test_18_zero_neural_workload_contract(self):
        m=b.manifest()
        for k in ("model_forward_calls","row_presentations","core_forward_calls","train_steps","new_checkpoint_writes","model_state_loads"):
            self.assertEqual(m[k],0)
        src=inspect.getsource(b.run)
        self.assertNotIn("torch.optim",src);self.assertNotIn(".backward(",src)

    def test_19_parent_verification_blocks_module_calls(self):
        src=inspect.getsource(b.load_parent)
        self.assertIn('patch.object(torch.nn.Module,"_call_impl"',src)
        self.assertIn("forbids model calls",src)

    def test_20_semantic_suite_count_and_exact_filter(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromTestCase(type(self)).countTestCases(),24)
        class D(unittest.TestCase):
            def __init__(self,n):super().__init__();self.n=n
            def id(self):return self.n
        suite=unittest.TestSuite([D(b.EXCLUDED)]+[D(f"x{i}") for i in range(b.manifest()["focused_tests"])])
        with patch.object(b,"regression_modules",return_value=[]),patch.object(unittest.defaultTestLoader,"loadTestsFromNames",return_value=suite):
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),3765)

    def test_21_dependency_resource_and_single_source_registration(self):
        tree=ast.parse(inspect.getsource(b.precheck))
        pattern=next(n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="pattern" for t in n.targets))
        names=["fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"]+[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,275)]
        self.assertTrue(all(re.fullmatch(pattern,n) for n in names));self.assertEqual(5+len(names)+1,51)
        self.assertEqual(854+1+len(b.PARENT_ARTIFACTS)+len(b.OWN),868)
        self.assertEqual((b.manifest()["source_pins"],b.manifest()["protected_inputs"]),(496,868))
        self.assertIn('registration["protected_inputs"]',inspect.getsource(b.validate_result))
        self.assertIn('registration["protected_inputs"]',inspect.getsource(b.precheck))

    def test_22_runner_validate_execute_and_cli_contract(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c275.ps1").read_text(encoding="utf-8")
        launcher=(root/"tools/invoke_c275.ps1").read_text(encoding="utf-8")
        self.assertIn('[ValidateSet("Validate","Execute")]',runner)
        self.assertIn("AUTHORING_RUNTIME_PREFLIGHT_FAILED",launcher)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("$failure = $null"))
        self.assertGreater(launcher.index("-Mode Execute"),launcher.index("$failure = $null"))
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        sets=[]
        for x in blocks:
            compile(x,"embedded","exec");sets.append({int(m.group(1)) for m in re.finditer(r"sys\.argv\[(\d+)\]",x)})
        self.assertEqual(sets,[{1},set(),{1,2,3}])

    def test_23_run_phase_order_uses_unique_markers(self):
        src=inspect.getsource(b.run)
        phases=("pins,protected=precheck(c274_summary,root)","_,metrics=load_parent(c274_summary)",
                "audit_result,summary=audit_metrics(metrics)","out=Path(output_dir)")
        pos=[]
        for p in phases:self.assertEqual(src.count(p),1,p);pos.append(src.index(p))
        self.assertEqual(pos,sorted(pos));self.assertEqual(len({src[:p].count("\n") for p in pos}),len(pos))

    def test_24_manifest_lifecycle_and_legacy_compatibility(self):
        root=Path(__file__).resolve().parents[1]
        prereg=(root/"docs/experiment-ledger-addendum-c275-preregistration.md").read_text(encoding="utf-8")
        handoff=(root/"docs/experiment-ledger-and-handoff.md").read_text(encoding="utf-8")
        self.assertNotEqual(b.MANIFEST_SHA,"PENDING_FINAL_SEAL");self.assertIn(b.MANIFEST_SHA,prereg)
        formal=re.search(r"(?ms)^## Formal state\s+(?P<body>.*?)(?=^## |\Z)",handoff);self.assertIsNotNone(formal)
        if re.search(r"\bC275 ACTIVE /",formal.group("body")):
            self.assertIn(b.MANIFEST_SHA,handoff)
        else:
            accepted=root/"docs/experiment-ledger-addendum-c275-c276.md"
            self.assertTrue(accepted.is_file());self.assertIn(b.MANIFEST_SHA,accepted.read_text(encoding="utf-8"))
        self.assertIn("89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604",handoff)
        legacy=(root/"tools/invoke_active.ps1").read_text(encoding="utf-8").encode()
        active=(root/"tools/invoke_active_v2.ps1").read_text(encoding="utf-8")
        self.assertEqual(hashlib.sha1(b"blob "+str(len(legacy)).encode()+b"\0"+legacy).hexdigest(),"86b5606a5b212b12f416abedac0923da634f88e3")
        self.assertEqual(hashlib.sha256(active.encode()).hexdigest(),"68faee42a7870d407e38cfb95c75f0f4fc51dbd41cfa972af423825eaa85ab10")

if __name__=="__main__":unittest.main(verbosity=2)
