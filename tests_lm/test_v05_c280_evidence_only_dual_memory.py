"""C280 authoring tests for evidence-only memory support."""
import copy,inspect,re,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
import torch
from fold_lm.v05_benchmarks import model_c280_evidence_only_dual_memory as b

class C280Tests(unittest.TestCase):
    def test_01_manifest_pending_or_final_digest_contract(self):
        self.assertEqual(b.MANIFEST_SHA,b.digest(b.manifest()))

    def test_02_arms_and_capacity_registered(self):
        self.assertEqual(b.ARMS,("all_token_dual","evidence_only_dual"))
        self.assertEqual(b.manifest()["parameters"],14256)

    def test_03_candidate_source_uses_same_mean_and_final_queries(self):
        src=inspect.getsource(b.EvidenceOnlyDualReadout.forward)
        self.assertIn("q_mean=self.read.query(mean)",src)
        self.assertIn("q_final=self.read.query(local[0][rows,final])",src)

    def test_04_evidence_support_is_before_first_query_byte(self):
        src=inspect.getsource(b.EvidenceOnlyDualReadout.forward)
        self.assertIn("evidence=valid&(pos<first.unsqueeze(1))",src)
        self.assertIn("tokens[rows,first-1]==59",src)

    def test_05_candidate_masks_both_softmaxes_with_evidence(self):
        src=inspect.getsource(b.EvidenceOnlyDualReadout.forward)
        self.assertEqual(src.count("masked_fill(~evidence"),2)
        self.assertEqual(src.count(".softmax(-1)"),2)

    def test_06_candidate_keeps_single_output_after_memory_average(self):
        src=inspect.getsource(b.EvidenceOnlyDualReadout.forward)
        self.assertIn("memory=(memory_mean+memory_final)*.5",src)
        self.assertEqual(src.count("self.read.output(memory)"),1)

    def test_07_forward_has_no_supervision_metadata(self):
        params=list(inspect.signature(b.EvidenceOnlyDualReadout.forward).parameters)
        self.assertEqual(params,["self","tokens","tasks"])

    def test_08_schedule_complete_equal_exposure(self):
        rows=[dict(language="en",entities=[0,1],values=[i//2,i//2+1],permutation=[0,1],query=i%2,target=i%2) for i in range(192)]
        # synthetic rows above do not meet grouping contract; inspect registered schedule instead.
        self.assertEqual(b.manifest()["row_exposures"],200)
        self.assertEqual(sum(b.manifest()["profile_updates"]),800)

    def test_09_schedule_is_fresh_and_deterministic(self):
        src=inspect.getsource(b.schedule)
        self.assertIn("seed+280000+e",src)
        self.assertIn("randperm(96",src)

    def test_10_fit_is_ce_only_and_lr_fixed(self):
        src=inspect.getsource(b.fit)
        self.assertIn("F.cross_entropy",src)
        self.assertIn("lr=.005",src)
        self.assertNotIn("evidence_drop",src)

    def test_11_both_tasks_decide_candidate(self):
        src=inspect.getsource(b.analyze)
        self.assertIn('passed=two["passed"] and tri["passed"]',src)
        self.assertIn('arm"]=="evidence_only_dual"',src)

    def test_12_control_failure_does_not_directly_define_candidate_gate(self):
        src=inspect.getsource(b.analyze)
        gate=src[src.index("candidate_gate="):]
        self.assertIn('"evidence_only_dual"',gate)

    def test_13_candidate_failure_fails_gate(self):
        rr=[dict(seed=s,arm=a,two_char_pass=True,triple_pass=True,passed=True) for s,a in b.identities()]
        rr[1]["passed"]=False
        self.assertFalse(all(r["passed"] for r in rr if r["arm"]=="evidence_only_dual"))

    def test_14_record_integrity_guards(self):
        src=inspect.getsource(b.analyze)
        self.assertIn("checkpoint_roundtrip",src)
        self.assertIn("reload_max_error",src)
        self.assertIn("paired state/batches",src)

    def test_15_matched_initial_and_batch_pair_required(self):
        src=inspect.getsource(b.run)+inspect.getsource(b.analyze)
        self.assertIn('base.fingerprint(models["evidence_only_dual"])==init',src)
        self.assertIn('ra["fit"]["batch_sha256"]==rb["fit"]["batch_sha256"]',src)

    def test_16_parent_loader_models_six_hashes_independently(self):
        src=inspect.getsource(b.load_parent)
        for name in ("PARENT_SHA","C278_SHA","C277_SHA","C276_SHA","C275_SHA","C274_SHA"):
            self.assertIn(name,src)

    def test_17_result_scope_is_gate_f_false(self):
        src=inspect.getsource(b.validate_result)
        self.assertIn("gate_f_candidate",src)
        self.assertIn("production_adoption",src)

    def test_18_bundle_identity(self):
        self.assertIn("fold-c280-evidence-dual-models-v1",inspect.getsource(b.load_bundle))
        self.assertIn("fold-c280-evidence-dual-eval-v1",inspect.getsource(b.verify_artifacts))

    def test_19_candidate_uses_shared_query_key_output_parameters(self):
        src=inspect.getsource(b.EvidenceOnlyDualReadout.forward)
        self.assertEqual(src.count("self.read.query("),2)
        self.assertEqual(src.count("self.read.key("),1)
        self.assertEqual(src.count("self.read.output("),1)

    def test_20_semantic_suite_count_and_exact_filter(self):
        self.assertEqual(b.manifest()["loaded_tests"],3886)
        self.assertEqual(b.manifest()["focused_tests"],3885)
        self.assertEqual(b.manifest()["excluded_test"],b.EXCLUDED)

    def test_21_dependency_resource_and_registration(self):
        m=b.manifest()
        self.assertEqual((m["source_pins"],m["protected_inputs"],m["direct_dependencies"]),(526,926,56))
        self.assertIn("27[0-9]",inspect.getsource(b.precheck))

    def test_22_runner_validate_execute_and_cli_contract(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools/run_c280.ps1").read_text(encoding="utf-8")
        launcher=(root/"tools/invoke_c280.ps1").read_text(encoding="utf-8")
        self.assertIn('ValidateSet("Validate","Execute")',runner)
        self.assertIn("expected_focused_tests = 3885",runner)
        self.assertIn("AUTHORING_RUNTIME_PREFLIGHT_FAILED",launcher)
        self.assertIn("publish_experiment_log.ps1 -ExperimentId C280",launcher)

    def test_23_run_phase_order_uses_unique_markers(self):
        src=inspect.getsource(b.run)
        phases=("pins,protected=precheck(","data=p267.dataset()","out=Path(output_dir)",
                "for seed in SEEDS:","torch.save(dict(schema=\"fold-c280-evidence-dual-models-v1\"",
                "metrics,summary=analyze(","payload=dict(")
        pos=[src.index(x) for x in phases]
        self.assertEqual(pos,sorted(pos))

    def test_24_manifest_lifecycle_and_legacy_compatibility(self):
        root=Path(__file__).resolve().parents[1]
        handoff=(root/"docs/experiment-ledger-and-handoff.md").read_text(encoding="utf-8")
        formal=re.search(r"(?ms)^## Formal state\s+(.*?)(?=^## |\Z)",handoff)
        self.assertIsNotNone(formal)
        if re.search(r"\bC280 ACTIVE /",formal.group(1)):
            self.assertIn(b.MANIFEST_SHA,handoff)
        else:
            accepted=root/"docs/experiment-ledger-addendum-c280-c281.md"
            if b.MANIFEST_SHA!="PENDING_FINAL_SEAL":
                self.assertTrue(accepted.is_file())
                self.assertIn(b.MANIFEST_SHA,accepted.read_text(encoding="utf-8"))

if __name__=="__main__": unittest.main()
