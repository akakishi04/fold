import inspect
import unittest
from pathlib import Path

import numpy as np

from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205


def canonical_rows(delta=0.0):
    rows=[]
    for b in c205.BASE_SEEDS:
        for h in c205.HEAD_SEEDS:
            rows.append(dict(
                base_seed=b,head_seed=h,prefix_errors=0,expanded_prefix_mismatches=0,
                necessity_prediction_errors=0,target_prediction_errors=0,
                necessity_max_abs_logit_difference=delta,
                target_max_abs_logit_difference=delta,
            ))
    return rows


def expanded_rows(delta=2e-6):
    rows=[]
    for b in c205.BASE_SEEDS:
        for h in c205.HEAD_SEEDS:
            rows.append(dict(
                base_seed=b,head_seed=h,prefix_errors=0,
                necessity_prediction_errors=0,target_prediction_errors=0,
                necessity_max_abs_logit_difference=delta,
                target_max_abs_logit_difference=delta,
            ))
    return rows


def match_rows(diff=0.0):
    rows=[]
    for b in c205.BASE_SEEDS:
        for h in c205.HEAD_SEEDS:
            rows.append(dict(
                base_seed=b,head_seed=h,
                necessity_parent_max_delta_difference=diff,
                target_parent_max_delta_difference=diff,
            ))
    return rows


def workload():
    return dict(
        canonical_rows=15912,expanded_rows=85824,
        canonical_forward_calls=18,expanded_forward_calls=90,
        canonical_cell_calls=126,expanded_cell_calls=630,
    )


def arrays():
    p=np.zeros((9536,),dtype=np.int8)
    t=np.zeros((9536,),dtype=np.int8)
    z=np.zeros((9536,2),dtype=np.float32)
    tz=np.zeros((9536,4),dtype=np.float32)
    return dict(
        necessity_predictions=p,target_predictions=t,
        necessity_logits=z,target_logits=tz,
    )


def c204_parent_rows():
    rows=[]
    for idx,(b,h) in enumerate((x for x in [(b,h) for b in c205.BASE_SEEDS for h in c205.HEAD_SEEDS])):
        rows.append(dict(
            block=idx,base_seed=b,head_seed=h,
            necessity_prediction_errors=0,target_prediction_errors=0,
            necessity_max_abs_logit_difference=3e-6,
            target_max_abs_logit_difference=4e-6,
        ))
    return {"prediction_replay":rows}


class C205Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c205.digest(c205.manifest()),c205.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m=c205.manifest()
        self.assertEqual((m["canonical_unique_rows"],m["expanded_rows"],m["blocks"]),(1768,9536,9))
        self.assertEqual(m["atol"],1e-6)

    def test_03_manifest_does_not_relax_tolerance(self):
        self.assertEqual(c205.ATOL,1e-6)
        self.assertIn("no threshold relaxation",c205.manifest()["scope"])

    def test_04_gate_accepts_batch_attribution_profile(self):
        self.assertTrue(c205.gate(canonical_rows(),expanded_rows(),match_rows(),workload()))

    def test_05_gate_rejects_canonical_over_tolerance(self):
        self.assertFalse(c205.gate(canonical_rows(2e-6),expanded_rows(),match_rows(),workload()))

    def test_06_gate_rejects_expanded_under_tolerance(self):
        self.assertFalse(c205.gate(canonical_rows(),expanded_rows(5e-7),match_rows(),workload()))

    def test_07_gate_rejects_parent_max_mismatch(self):
        self.assertFalse(c205.gate(canonical_rows(),expanded_rows(),match_rows(1e-7),workload()))

    def test_08_gate_rejects_workload_drift(self):
        w=workload();w["expanded_rows"]-=1
        self.assertFalse(c205.gate(canonical_rows(),expanded_rows(),match_rows(),w))

    def test_09_gate_rejects_prefix_mismatch(self):
        rows=canonical_rows();rows[0]["expanded_prefix_mismatches"]=1
        self.assertFalse(c205.gate(rows,expanded_rows(),match_rows(),workload()))

    def test_10_compare_exact(self):
        a=arrays()
        m=c205.compare(a,a)
        self.assertEqual(m["necessity_prediction_errors"],0)
        self.assertEqual(m["target_prediction_errors"],0)
        self.assertEqual(m["necessity_max_abs_logit_difference"],0.0)
        self.assertEqual(m["target_max_abs_logit_difference"],0.0)

    def test_11_compare_counts_prediction_errors(self):
        ref=arrays();live={k:v.copy() for k,v in ref.items()}
        live["necessity_predictions"][0]=1
        live["target_predictions"][1]=2
        m=c205.compare(live,ref)
        self.assertEqual((m["necessity_prediction_errors"],m["target_prediction_errors"]),(1,1))

    def test_12_compare_rejects_target_finite_mask_drift(self):
        ref=arrays();live={k:v.copy() for k,v in ref.items()}
        ref["target_logits"][0,0]=-np.inf
        with self.assertRaises(ValueError):
            c205.compare(live,ref)

    def test_13_c204_replay_map_accepts_nine_pairs(self):
        m=c205.c204_replay_map(c204_parent_rows())
        self.assertEqual(len(m),9)
        self.assertIn((181001,188001),m)

    def test_14_c204_replay_map_rejects_duplicate_pair(self):
        p=c204_parent_rows()
        p["prediction_replay"][1]["base_seed"]=181001
        p["prediction_replay"][1]["head_seed"]=188001
        with self.assertRaises(ValueError):
            c205.c204_replay_map(p)

    def test_15_unique_path_uses_v2_prefix_and_local_expansion(self):
        source=inspect.getsource(c205.infer_v2_unique)
        self.assertIn("c204.encode_live_v2",source)
        self.assertIn("c189.combined_predict",source)
        self.assertIn("p[local_rows]",source)
        self.assertIn("z[local_rows]",source)

    def test_16_expanded_path_uses_direct_world_views(self):
        source=inspect.getsource(c205.infer_v2_expanded)
        self.assertIn("c190.make_views",source)
        self.assertIn("c204.encode_live_v2",source)
        self.assertIn("c189.combined_predict",source)

    def test_17_cohort_reconstructs_and_checks_parent_identity(self):
        source=inspect.getsource(c205.reconstruct_phase0_cohort)
        self.assertIn("c190.expand_worlds",source)
        self.assertIn("np.array_equal(source2, source_rows)",source)
        self.assertIn("np.array_equal(local2, local_rows)",source)
        self.assertIn("np.array_equal(world2, world_codes)",source)

    def test_18_run_compares_exact_input_prefix_rows(self):
        source=inspect.getsource(c205.run)
        self.assertIn('unique["raw"][cohort["local_rows"]] != direct["raw"]',source)
        self.assertIn("mismatch_rows",source)

    def test_19_run_compares_expanded_max_to_c204_parent(self):
        source=inspect.getsource(c205.run)
        self.assertIn("necessity_parent_max_delta_difference",source)
        self.assertIn("target_parent_max_delta_difference",source)
        self.assertIn("parent_map[b, h]",source)

    def test_20_precheck_requires_valid_negative_parent(self):
        source=inspect.getsource(c205.precheck)
        self.assertIn('p204.get("status") == "FAIL"',source)
        self.assertIn('p204["summary"].get("max_necessity_logit_delta", 0) > ATOL',source)
        self.assertIn("not c204.gate",source)

    def test_21_precheck_pins_c204_execution_source(self):
        source=inspect.getsource(c205.precheck)
        self.assertIn('PARENT_C204_EXECUTION + ":" + name',source)
        self.assertIn("Accepted C204 source changed:",source)

    def test_22_run_sets_parent_deterministic_environment(self):
        source=inspect.getsource(c205.run)
        self.assertIn("torch.set_num_threads(2)",source)
        self.assertIn("torch.use_deterministic_algorithms(True)",source)

    def test_23_run_has_no_runtime_acquisition_dispatch(self):
        source=inspect.getsource(c205.run)
        self.assertNotIn("owner.dispatch",source)
        self.assertNotIn("mapper.propose_selected",source)
        self.assertIn("acquisitions=0",source)

    def test_24_regression_adds_one_module(self):
        source=inspect.getsource(c205.regression_modules)
        self.assertIn("== 89",source)
        self.assertIn("test_v05_c205_phase0_batch_composition_attribution",source)


    def test_25_c205_launcher_parses_runner_before_logging(self):
        root=Path(__file__).resolve().parents[1]
        source=(root/"tools"/"invoke_c205.ps1").read_text(encoding="utf-8")
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",source)
        self.assertIn('RUNNER_PARSE_ERROR',source)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c205.ps1"',source)
        self.assertLess(source.index("[System.Management.Automation.Language.Parser]::ParseFile"),source.index("$failure = $null"))


    def test_26_regression_suite_excludes_only_mutable_historical_active_state(self):
        root=Path(__file__).resolve().parents[1]
        suite=c205.regression_suite(root)
        ids=[test.id() for test in c205._iter_tests(suite)]
        self.assertEqual(len(ids),1871)
        self.assertEqual(
            c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS,
            ("tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state",),
        )
        self.assertFalse(any(x in ids for x in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS))


if __name__=="__main__":
    unittest.main(verbosity=2)
