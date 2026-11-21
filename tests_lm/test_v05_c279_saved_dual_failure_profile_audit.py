"""C279 authoring tests for saved mean/final dual-query failure-profile attribution."""
import inspect,re,unittest
from pathlib import Path
from unittest.mock import patch
from fold_lm.v05_benchmarks import model_c279_saved_dual_failure_profile_audit as b

def cell(*,passed=True,criterion=None,profile="shared_suffix2",split="HOLDOUT"):
    vals=dict(accuracy=.95,query_pair_accuracy=.9,evidence_drop=.5,query_drop=.5)
    if criterion=="accuracy": vals["accuracy"]=.75
    if criterion=="query_pair_accuracy": vals["query_pair_accuracy"]=.5
    if criterion=="evidence_drop": vals["evidence_drop"]=.1
    if criterion=="query_drop": vals["query_drop"]=.1
    return dict(split=split,profile=profile,language="en",entities=["a","b","c"],permutation=[0,1,2],
        rows=10,correct=9,pairs=5,collapsed_pairs=0,passed=passed,**vals)

def order(*,passed=True,profile="shared_suffix2",split="HOLDOUT"):
    return dict(split=split,profile=profile,language="en",entities=["a","b","c"],groups=5,both_correct=5,
        accuracy=.9 if passed else .5,passed=passed)

def task(*,fail=None,profile="shared_suffix2",split="HOLDOUT"):
    oc=(fail=="two_order_accuracy")
    c=cell(passed=fail not in ("accuracy","query_pair_accuracy","evidence_drop","query_drop"),
           criterion=fail,profile=profile,split=split)
    o=order(passed=not oc,profile=profile,split=split)
    return dict(cells=[c],two_order=[o],passed=(fail is None))

def metrics(fail_candidate=None,fail_control=None,profile="shared_suffix2"):
    out=[]
    for seed,arm in b.PARENT_IDENTITIES:
        fail=None
        if seed==278001 and arm=="mean_final_dual": fail=fail_candidate
        if seed==278001 and arm=="mean_span": fail=fail_control
        two=task()
        tri=task(fail=fail,profile=profile)
        out.append(dict(seed=seed,arm=arm,two_char=two,triple=tri,passed=two["passed"] and tri["passed"]))
    return out

class C279Tests(unittest.TestCase):
    def test_01_manifest_is_final_and_matches_digest(self):
        self.assertEqual(b.digest(b.manifest()),b.MANIFEST_SHA)
        self.assertEqual(b.manifest()["acceptance_base"],b.BASE)

    def test_02_signed_margin(self):
        self.assertAlmostEqual(b.signed_margin(.9,.8),.1)
        with self.assertRaises(ValueError): b.signed_margin(float("nan"),.8)

    def test_03_answer_accuracy_failure(self):
        r=b.answer_record(1,"mean_span","triple",cell(passed=False,criterion="accuracy"))
        self.assertEqual(r["failed_criteria"],["accuracy"])

    def test_04_answer_mask_failure(self):
        r=b.answer_record(1,"mean_final_dual","triple",cell(passed=False,criterion="evidence_drop"))
        self.assertEqual(r["failed_criteria"],["evidence_drop"])

    def test_05_two_order_failure(self):
        r=b.two_order_record(1,"mean_final_dual","triple",order(passed=False))
        self.assertEqual(r["failed_criteria"],["two_order_accuracy"])

    def test_06_pass_margin_inconsistency_rejected(self):
        with self.assertRaises(ValueError):
            b.answer_record(1,"mean_span","triple",cell(passed=True,criterion="accuracy"))

    def test_07_audit_parent_identity_and_counts(self):
        p,s=b.audit_metrics(metrics())
        self.assertEqual(s["parent_records"],10)
        self.assertEqual(len(p["parent_passes"]),10)

    def test_08_parent_pass_count_reconstruction(self):
        _,s=b.audit_metrics(metrics(fail_candidate="accuracy",fail_control="query_drop"))
        self.assertEqual(s["parent_seed_pass_counts"]["mean_final_dual"],4)
        self.assertEqual(s["parent_seed_pass_counts"]["mean_span"],4)

    def test_09_candidate_minus_control_direction(self):
        _,s=b.audit_metrics(metrics(fail_candidate="accuracy",fail_control="query_drop"))
        self.assertEqual(s["triple_criterion_delta"]["accuracy"],1)
        self.assertEqual(s["triple_criterion_delta"]["query_drop"],-1)

    def test_10_prefix_primary_view_exists(self):
        p,_=b.audit_metrics(metrics(profile="shared_prefix2"))
        self.assertIn("shared_prefix2_holdout",p["primary"])

    def test_11_suffix_train_and_holdout_views_exist(self):
        p,_=b.audit_metrics(metrics())
        self.assertIn("shared_suffix2_train",p["primary"])
        self.assertIn("shared_suffix2_holdout",p["primary"])

    def test_12_per_seed_view_complete(self):
        p,_=b.audit_metrics(metrics())
        self.assertEqual(set(p["primary"]["per_seed_triple"]),{str(x) for x in range(278001,278006)})

    def test_13_task_pass_must_equal_fixed_records(self):
        m=metrics();m[0]["triple"]["passed"]=False;m[0]["passed"]=False
        with self.assertRaises(ValueError): b.audit_metrics(m)

    def test_14_whole_pass_must_equal_both_tasks(self):
        m=metrics();m[0]["passed"]=False
        with self.assertRaises(ValueError): b.audit_metrics(m)

    def test_15_aggregate_negative_ranges_are_negative(self):
        p,_=b.audit_metrics(metrics(fail_candidate="two_order_accuracy"))
        ranges=p["aggregates"]["negative_margin_range"]
        self.assertLess(ranges["mean_final_dual|two_order_accuracy"]["max"],0)

    def test_16_result_validation_is_diagnostic_only(self):
        pins={n:"x" for n in b.OWN}
        while len(pins)<520: pins[f"x/{len(pins)}"]="x"
        inputs={f"i/{i}":"x" for i in range(916)}
        s=dict(parent_seed_pass_counts={"mean_span":0,"mean_final_dual":0},
               parent_two_char_pass_counts={"mean_span":5,"mean_final_dual":5},
               parent_triple_pass_counts={"mean_span":0,"mean_final_dual":0},
               diagnostic_complete=True,capability_gate_applicable=False,
               model_forward_calls=0,row_presentations=0,core_forward_calls=0,train_steps=0,
               new_checkpoint_writes=0,model_state_loads=0)
        p=dict(experiment_id=b.EXPERIMENT_ID,stage=b.STAGE,diagnostic_execution_valid=True,
               source_blobs=pins,input_sha256=inputs,artifacts=[dict(file=n) for n in b.OUTPUTS],
               validation_summary=s,status="PASS",gate_f_candidate=False,production_adoption=False,
               capability_gate_applicable=False)
        b.validate_result(p)

    def test_17_zero_neural_workload_contract(self):
        m=b.manifest()
        for k in ("model_forward_calls","row_presentations","core_forward_calls","train_steps","new_checkpoint_writes","model_state_loads"):
            self.assertEqual(m[k],0)

    def test_18_output_contract(self):
        self.assertEqual(set(b.OUTPUTS),{"audit-plan.json","failure-profile.json","validation-summary.json"})

    def test_19_parent_verification_blocks_module_calls(self):
        src=inspect.getsource(b.load_parent)
        self.assertIn('patch.object(torch.nn.Module,"_call_impl"',src)
        self.assertIn("parent.verify_artifacts",src)

    def test_20_suite_count_contract_is_manifest_derived(self):
        m=b.manifest()
        self.assertEqual(m["modules"],164)
        self.assertEqual(m["loaded_tests"]-m["focused_tests"],1)

    def test_21_dependency_resource_and_registration(self):
        m=b.manifest()
        self.assertEqual((m["source_pins"],m["protected_inputs"],m["direct_dependencies"]),(520,916,55))
        self.assertIn("27[0-8]",inspect.getsource(b.precheck))

    def test_22_runner_validate_execute_and_cli_contract(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c279.ps1").read_text(encoding="utf-8")
        launcher=(root/"tools/invoke_c279.ps1").read_text(encoding="utf-8")
        self.assertIn('ValidateSet("Validate","Execute")',runner)
        self.assertIn("expected_focused_tests = 3861",runner)
        self.assertIn("AUTHORING_RUNTIME_PREFLIGHT_FAILED",launcher)
        self.assertIn("publish_experiment_log.ps1 -ExperimentId C279",launcher)

    def test_23_run_phase_order_uses_unique_markers(self):
        src=inspect.getsource(b.run)
        phases=("pins,protected=precheck(","_,metrics=load_parent(","profile,summary=audit_metrics(metrics)",
                "out=Path(output_dir)","artifacts=[dict(","payload=dict(")
        pos=[src.index(x) for x in phases]
        self.assertEqual(pos,sorted(pos))

    def test_24_manifest_lifecycle_and_legacy_compatibility(self):
        root=Path(__file__).resolve().parents[1]
        handoff=(root/"docs/experiment-ledger-and-handoff.md").read_text(encoding="utf-8")
        formal=re.search(r"(?ms)^## Formal state\s+(.*?)(?=^## |\Z)",handoff)
        self.assertIsNotNone(formal)
        if re.search(r"\bC279 ACTIVE /",formal.group(1)):
            self.assertIn(b.MANIFEST_SHA,handoff)
        else:
            accepted=root/"docs/experiment-ledger-addendum-c279-c280.md"
            self.assertTrue(accepted.is_file())
            self.assertIn(b.MANIFEST_SHA,accepted.read_text(encoding="utf-8"))

if __name__=="__main__": unittest.main()
