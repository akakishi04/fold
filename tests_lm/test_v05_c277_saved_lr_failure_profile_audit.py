"""C277 authoring tests for saved LR failure-profile attribution."""
import ast,copy,hashlib,inspect,re,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
import torch
from fold_lm.v05_benchmarks import model_c277_saved_lr_failure_profile_audit as b

def cell(*,passed=True,criterion=None,profile="shared_suffix2",split="HOLDOUT"):
    vals=dict(accuracy=1.0,query_pair_accuracy=1.0,evidence_drop=.5,query_drop=.5)
    if criterion=="accuracy":vals["accuracy"]=.75
    if criterion=="query_pair_accuracy":vals["query_pair_accuracy"]=.5
    if criterion=="evidence_drop":vals["evidence_drop"]=.1
    if criterion=="query_drop":vals["query_drop"]=.1
    return dict(split=split,profile=profile,language="en",entities=[0,1],permutation=[0,1],
        rows=8,correct=8 if vals["accuracy"]>=.9 else 6,pairs=4,collapsed_pairs=0,answer_nll=.1,
        passed=passed,**vals)

def order(*,passed=True,profile="shared_suffix2",split="HOLDOUT"):
    return dict(split=split,profile=profile,language="en",entities=[0,1],
        groups=8,both_correct=8 if passed else 4,accuracy=1.0 if passed else .5,passed=passed)

def task(*,fail=None,profile="shared_suffix2"):
    c=cell(passed=fail not in ("accuracy","query_pair_accuracy","evidence_drop","query_drop"),criterion=fail,profile=profile)
    o=order(passed=fail!="two_order_accuracy",profile=profile)
    return dict(cells=[c],two_order=[o],totals=[],passed=c["passed"] and o["passed"])

def metrics():
    out=[]
    for seed,arm in b.PARENT_IDENTITIES:
        two=task()
        if arm=="lr005" and seed==276003:two=task(fail="accuracy",profile="shared_prefix")
        # Every triple state fails, but arm failure signatures differ.
        if arm=="lr005":
            fail="accuracy" if seed!=276003 else "two_order_accuracy"
        else:
            fail="query_pair_accuracy" if seed!=276003 else "evidence_drop"
        tri=task(fail=fail)
        out.append(dict(seed=seed,arm=arm,two_char=two,triple=tri,passed=False))
    return out

def protection():
    pins={f"old-{i}":"fixture" for i in range(502)};pins.update({x:"fixture" for x in b.OWN})
    return pins,{f"input-{i}":"0"*64 for i in range(892)}

class C277Tests(unittest.TestCase):
    def test_01_manifest_is_final_and_matches_digest(self):
        self.assertNotEqual(b.MANIFEST_SHA,"PENDING_FINAL_SEAL")
        self.assertRegex(b.MANIFEST_SHA,r"^[0-9a-f]{64}$")
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)

    def test_02_signed_margin(self):
        self.assertAlmostEqual(b.signed_margin(.9,.9),0.)
        self.assertLess(b.signed_margin(.8,.9),0.)
        with self.assertRaises(ValueError):b.signed_margin(float("nan"),.9)

    def test_03_answer_accuracy_failure(self):
        r=b.answer_record(1,"lr005","triple",cell(passed=False,criterion="accuracy"))
        self.assertEqual(r["failed_criteria"],["accuracy"])

    def test_04_answer_query_pair_failure(self):
        r=b.answer_record(1,"lr0025","triple",cell(passed=False,criterion="query_pair_accuracy"))
        self.assertEqual(r["failed_criteria"],["query_pair_accuracy"])

    def test_05_answer_mask_failures(self):
        for c in ("evidence_drop","query_drop"):
            r=b.answer_record(1,"lr0025","triple",cell(passed=False,criterion=c))
            self.assertEqual(r["failed_criteria"],[c])

    def test_06_two_order_failure(self):
        r=b.two_order_record(1,"lr005","triple",order(passed=False))
        self.assertEqual(r["failed_criteria"],["two_order_accuracy"]);self.assertLess(r["margins"]["two_order_accuracy"],0)

    def test_07_pass_margin_inconsistency_rejected(self):
        with self.assertRaises(ValueError):b.answer_record(1,"lr005","triple",cell(passed=True,criterion="accuracy"))
        bad=order(passed=True);bad["accuracy"]=.5
        with self.assertRaises(ValueError):b.two_order_record(1,"lr005","triple",bad)

    def test_08_audit_parent_identity_and_counts(self):
        a,s=b.audit_metrics(metrics())
        self.assertEqual(s["parent_records"],10)
        self.assertEqual(s["parent_seed_pass_counts"],{"lr005":0,"lr0025":0})
        self.assertEqual(s["parent_two_char_pass_counts"],{"lr005":4,"lr0025":5})
        self.assertEqual(s["parent_triple_pass_counts"],{"lr005":0,"lr0025":0})
        self.assertEqual(len(a["parent_passes"]),10)

    def test_09_triple_delta_direction(self):
        _,s=b.audit_metrics(metrics())
        self.assertEqual(s["triple_criterion_delta"]["accuracy"],-4)
        self.assertEqual(s["triple_criterion_delta"]["query_pair_accuracy"],4)
        self.assertEqual(s["triple_criterion_delta"]["two_order_accuracy"],-1)
        self.assertEqual(s["triple_criterion_delta"]["evidence_drop"],1)

    def test_10_shared_suffix_primary_view_exists(self):
        a,_=b.audit_metrics(metrics());p=a["primary"]
        self.assertIn("shared_suffix2_train",p);self.assertIn("shared_suffix2_holdout",p)
        self.assertIn("candidate_minus_control",p["shared_suffix2_holdout"])

    def test_11_recovery_seed_and_stable_seed_views_exist(self):
        a,_=b.audit_metrics(metrics());p=a["primary"]
        self.assertIn("recovery_seed276003",p);self.assertIn("stable_seeds",p)
        self.assertEqual(set(p["per_seed_triple"]),{"276001","276002","276003","276004","276005"})

    def test_12_task_pass_must_equal_fixed_records(self):
        m=metrics();m[1]["triple"]["passed"]=True
        with self.assertRaises(ValueError):b.audit_metrics(m)

    def test_13_whole_pass_must_equal_both_tasks(self):
        m=metrics();m[1]["passed"]=True
        with self.assertRaises(ValueError):b.audit_metrics(m)

    def test_14_parent_identity_order_required(self):
        m=metrics();m[0],m[1]=m[1],m[0]
        with self.assertRaises(ValueError):b.audit_metrics(m)

    def test_15_aggregate_negative_ranges_are_negative(self):
        a,_=b.audit_metrics(metrics())
        for v in a["aggregates"]["negative_margin_range"].values():
            self.assertLess(v["min"],0);self.assertLess(v["max"],0)

    def test_16_parent_loader_models_three_hashes_independently(self):
        payload=dict(status="FAIL",commit_sha=b.PARENT_EXECUTION,
            validation_summary={"candidate_gate":False,"seed_pass_counts":{"lr0025":0,"lr005":0},
                "two_char_pass_counts":{"lr0025":5,"lr005":4},"triple_pass_counts":{"lr0025":0,"lr005":0}},
            artifacts=[dict(file=k,sha256=v) for k,v in b.PARENT_ARTIFACTS.items()])
        pm=metrics()
        fake=SimpleNamespace(verify_artifacts=Mock(return_value=(payload,pm)),validate_result=Mock())
        sha=Mock(side_effect=lambda path:{ "p":b.PARENT_SHA,"q":b.C275_SHA,"r":b.C274_SHA}.get(Path(path).name,"unexpected"))
        class Audit:
            read_json=staticmethod(lambda path:pm)
        audit=SimpleNamespace(sha=sha,read_json=Audit.read_json)
        with patch.object(b,"context",return_value=(fake,None,None,None,None,None,None,None,None,None,None,audit)):
            got,mm=b.load_parent(Path("p"),Path("q"),Path("r"));self.assertEqual(got,payload);self.assertEqual(mm,pm)
            self.assertEqual([Path(x.args[0]).name for x in sha.call_args_list[:3]],["p","q","r"])
            sha.reset_mock();sha.side_effect=lambda path:b.PARENT_SHA
            with self.assertRaisesRegex(ValueError,"parent hash"):b.load_parent(Path("p"),Path("q"),Path("r"))

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
        src=inspect.getsource(b.run);self.assertNotIn("torch.optim",src);self.assertNotIn(".backward(",src)

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
            self.assertEqual(b.regression_suite(Path.cwd()).countTestCases(),3813)

    def test_21_dependency_resource_and_registration(self):
        tree=ast.parse(inspect.getsource(b.precheck))
        pattern=next(n.value.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="pattern" for t in n.targets))
        names=["fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"]+[f"fold_lm/v05_benchmarks/model_c{i}_fixture.py" for i in range(231,277)]
        self.assertTrue(all(re.fullmatch(pattern,n) for n in names));self.assertEqual(5+len(names)+1,53)
        self.assertEqual(878+1+len(b.PARENT_ARTIFACTS)+len(b.OWN),892)
        self.assertEqual((b.manifest()["source_pins"],b.manifest()["protected_inputs"]),(508,892))
        self.assertIn('registration["protected_inputs"]',inspect.getsource(b.validate_result))
        self.assertIn('registration["protected_inputs"]',inspect.getsource(b.precheck))

    def test_22_runner_validate_execute_and_cli_contract(self):
        root=Path(__file__).resolve().parents[1];runner=(root/"tools/run_c277.ps1").read_text(encoding="utf-8");launcher=(root/"tools/invoke_c277.ps1").read_text(encoding="utf-8")
        self.assertIn('[ValidateSet("Validate","Execute")]',runner);self.assertIn("AUTHORING_RUNTIME_PREFLIGHT_FAILED",launcher)
        self.assertLess(launcher.index("-Mode Validate"),launcher.index("$failure = $null"));self.assertGreater(launcher.index("-Mode Execute"),launcher.index("$failure = $null"))
        blocks=re.findall(r"@'\n(.*?)\n'@",runner,re.S);self.assertEqual(len(blocks),3)
        sets=[]
        for x in blocks:compile(x,"embedded","exec");sets.append({int(m.group(1)) for m in re.finditer(r"sys\.argv\[(\d+)\]",x)})
        self.assertEqual(sets,[{1,2,3},set(),{1,2,3,4,5}])

    def test_23_run_phase_order_uses_unique_markers(self):
        src=inspect.getsource(b.run)
        phases=("pins,protected=precheck(c276_summary,c275_summary,c274_summary,root)",
                "_,metrics=load_parent(c276_summary,c275_summary,c274_summary)",
                "profile,summary=audit_metrics(metrics)","out=Path(output_dir)")
        pos=[]
        for p in phases:self.assertEqual(src.count(p),1,p);pos.append(src.index(p))
        self.assertEqual(pos,sorted(pos));self.assertEqual(len({src[:p].count("\n") for p in pos}),len(pos))

    def test_24_manifest_lifecycle_and_legacy_compatibility(self):
        root=Path(__file__).resolve().parents[1];prereg=(root/"docs/experiment-ledger-addendum-c277-preregistration.md").read_text(encoding="utf-8");handoff=(root/"docs/experiment-ledger-and-handoff.md").read_text(encoding="utf-8")
        self.assertNotEqual(b.MANIFEST_SHA,"PENDING_FINAL_SEAL");self.assertIn(b.MANIFEST_SHA,prereg)
        formal=re.search(r"(?ms)^## Formal state\s+(?P<body>.*?)(?=^## |\Z)",handoff);self.assertIsNotNone(formal)
        if re.search(r"\bC277 ACTIVE /",formal.group("body")):self.assertIn(b.MANIFEST_SHA,handoff)
        else:
            accepted=root/"docs/experiment-ledger-addendum-c277-c278.md";self.assertTrue(accepted.is_file());self.assertIn(b.MANIFEST_SHA,accepted.read_text(encoding="utf-8"))
        self.assertIn("89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604",handoff)
        legacy=(root/"tools/invoke_active.ps1").read_text(encoding="utf-8").encode();active=(root/"tools/invoke_active_v2.ps1").read_text(encoding="utf-8")
        self.assertEqual(hashlib.sha1(b"blob "+str(len(legacy)).encode()+b"\0"+legacy).hexdigest(),"86b5606a5b212b12f416abedac0923da634f88e3")
        self.assertEqual(hashlib.sha256(active.encode()).hexdigest(),"68faee42a7870d407e38cfb95c75f0f4fc51dbd41cfa972af423825eaa85ab10")

if __name__=="__main__":unittest.main(verbosity=2)
