import ast
import inspect
import re
import unittest
from pathlib import Path

import torch

from fold_lm.v05 import memory_coverage as coverage
from fold_lm.v05 import memory_stack as stack
from fold_lm.v05_benchmarks import gate_f_c220_frozen_learned_stack as c220


class C220Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = c220.episode_plan()
        cls.oracle_map = {0: 0, 5: 5, 1: 1, 3: 3}
        cls.episodes, cls.counts = c220.build_episode_set(cls.oracle_map, 218001)
        cls.by_label = {row["label"]: row for row in cls.episodes}

    def test_01_manifest_hash(self):
        self.assertEqual(c220.digest(c220.manifest()), c220.MANIFEST_SHA)

    def test_02_parent_c219_identity_is_exact(self):
        self.assertEqual(
            (c220.PARENT_C219_EXECUTION, c220.PARENT_C219_SHA),
            (
                "5a613ed07c34d1735d20c5849464116cc00d333c",
                "dbf54bd3cdc5b2fbd82a68a62bcdbaad806b8946b817776d94527a5bdcbaee14",
            ),
        )
        self.assertEqual(
            c220.PARENT_C219_VALIDATION_SHA,
            "a380cbb38c686757d4a296c8e557d7b2f304ea72ce4b583185c02099958685d4",
        )

    def test_03_checkpoint_artifact_identities_are_exact(self):
        self.assertEqual(
            (
                c220.COVERAGE_CHECKPOINT_SHA,
                c220.WRITER_CHECKPOINT_SHA,
                c220.SELECTOR_CHECKPOINT_SHA,
                c220.READER_CHECKPOINT_SHA,
            ),
            (
                "1ba50ab3b621b75a0b5c0528f2eb03c6f11e8a0000122563357709d386cee0a1",
                "3313bb507527b7e4798333c8b8c7f1e0e2ea2f9f2cd513060b505184c87d5c9d",
                "ab8892e6562a4801a30fea853fdbc712d69d9c5077e32c0b8fab6e555fead215",
                "bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af",
            ),
        )

    def test_04_episode_plan_hash_is_fixed(self):
        self.assertEqual(c220.digest(self.plan), c220.EPISODE_PLAN_SHA)

    def test_05_episode_labels_are_exact(self):
        self.assertEqual(
            [row["label"] for row in self.plan],
            [
                "missing_alpha",
                "out_of_scope_beta",
                "hot_alpha",
                "supported_alpha",
                "hot_beta",
                "supported_beta",
                "replace_alpha",
                "replace_beta",
            ],
        )

    def test_06_episode_readable_nonreadable_counts_are_exact(self):
        self.assertEqual(
            (
                sum(row["target_class"] is not None for row in self.plan),
                sum(row["target_class"] is None for row in self.plan),
            ),
            (6, 2),
        )

    def test_07_supported_maps_to_read(self):
        gate = stack.gate_for_coverage(coverage.CoverageClass.SUPPORTED)
        self.assertTrue(gate.readable)
        self.assertIs(gate.action, stack.StackAction.READ)

    def test_08_hot_required_maps_to_read(self):
        gate = stack.gate_for_coverage(coverage.CoverageClass.HOT_REQUIRED)
        self.assertTrue(gate.readable)
        self.assertIs(gate.action, stack.StackAction.READ)

    def test_09_missing_maps_to_distinct_suppression(self):
        gate = stack.gate_for_coverage(coverage.CoverageClass.MISSING)
        self.assertFalse(gate.readable)
        self.assertIs(gate.action, stack.StackAction.SUPPRESS_MISSING)

    def test_10_out_of_scope_maps_to_distinct_suppression(self):
        gate = stack.gate_for_coverage(coverage.CoverageClass.OUT_OF_SCOPE)
        self.assertFalse(gate.readable)
        self.assertIs(gate.action, stack.StackAction.SUPPRESS_OUT_OF_SCOPE)

    def test_11_unknown_coverage_is_rejected(self):
        with self.assertRaises(ValueError):
            stack.gate_for_coverage(99)

    def test_12_selected_scalar_returns_reader_shape(self):
        value = stack.selected_scalar(torch.tensor([1.0, 2.0]), 1)
        self.assertEqual(tuple(value.shape), (1, 1))
        self.assertEqual(float(value.item()), 2.0)

    def test_13_writer_checkpoint_fingerprints_are_exact(self):
        self.assertEqual(c220.WRITER_SEEDS, (218001, 218002, 218003))
        self.assertEqual(len(c220.WRITER_FINAL_SHA256), 3)

    def test_14_coverage_checkpoint_fingerprints_are_exact(self):
        self.assertEqual(c220.COVERAGE_SEEDS, (219001, 219002, 219003))
        self.assertEqual(len(c220.COVERAGE_FINAL_SHA256), 3)

    def test_15_selector_checkpoint_fingerprints_are_exact(self):
        self.assertEqual(c220.SELECTOR_SEEDS, (217001, 217002, 217003))
        self.assertEqual(len(c220.SELECTOR_FINAL_SHA256), 3)

    def test_16_reader_checkpoint_fingerprints_are_exact(self):
        self.assertEqual(c220.READER_SEEDS, (216001, 216002, 216003))
        self.assertEqual(len(c220.READER_FINAL_SHA256), 3)

    def test_17_writer_eval_feature_batch_is_exact(self):
        targets, x = c220.writer_eval_features()
        self.assertEqual(targets, (0, 5, 1, 3))
        self.assertEqual(tuple(x.shape), (4, 5))

    def test_18_writer_eval_targets_cover_registered_episode_writes(self):
        self.assertEqual(
            {row["writer_target"] for row in self.plan if row["writer_target"] is not None},
            {0, 1, 3, 5},
        )

    def test_19_oracle_writer_map_builds_expected_coverage_sequence(self):
        self.assertEqual(
            [row["actual_coverage"] for row in self.episodes],
            [
                "MISSING",
                "OUT_OF_SCOPE",
                "HOT_REQUIRED",
                "SUPPORTED",
                "HOT_REQUIRED",
                "SUPPORTED",
                "SUPPORTED",
                "SUPPORTED",
            ],
        )
        self.assertTrue(all(row["valid"] for row in self.episodes))

    def test_20_episode_operation_counts_are_exact(self):
        self.assertEqual(
            self.counts,
            dict(
                learned_writer_operation_applications=6,
                oracle_initialization_writes=4,
                oracle_end_scope_ops=1,
                chunk_commits=6,
                operation_failures=0,
            ),
        )

    def test_21_missing_and_out_of_scope_are_distinct(self):
        self.assertEqual(self.by_label["missing_alpha"]["actual_coverage"], "MISSING")
        self.assertEqual(
            self.by_label["out_of_scope_beta"]["actual_coverage"], "OUT_OF_SCOPE"
        )

    def test_22_hot_and_supported_pairs_are_exact(self):
        self.assertEqual(self.by_label["hot_alpha"]["actual_coverage"], "HOT_REQUIRED")
        self.assertEqual(self.by_label["supported_alpha"]["actual_coverage"], "SUPPORTED")
        self.assertEqual(self.by_label["hot_beta"]["actual_coverage"], "HOT_REQUIRED")
        self.assertEqual(self.by_label["supported_beta"]["actual_coverage"], "SUPPORTED")

    def test_23_replace_episodes_are_supported(self):
        self.assertEqual(self.by_label["replace_alpha"]["actual_coverage"], "SUPPORTED")
        self.assertEqual(self.by_label["replace_beta"]["actual_coverage"], "SUPPORTED")

    def test_24_wrong_port_is_detectable_in_all_readable_episodes(self):
        for row in self.episodes:
            if row["target_class"] is None:
                continue
            self.assertIsNotNone(row["readout"])
            intended_port = 0 if row["query"] == "alpha" else 1
            self.assertNotEqual(
                row["readout"][intended_port],
                row["readout"][1 - intended_port],
            )

    def test_25_expected_and_actual_coverage_match_under_oracle_writer(self):
        expected = {row["label"]: row["expected_coverage"] for row in self.plan}
        for row in self.episodes:
            self.assertEqual(row["actual_coverage"], expected[row["label"]])

    def test_26_gate_accepts_complete_registered_summary(self):
        summary = dict(
            all_writer_checkpoint_roundtrips=True,
            all_coverage_checkpoint_roundtrips=True,
            all_selector_checkpoint_roundtrips=True,
            all_reader_checkpoint_roundtrips=True,
            writer_target_accuracy=1.0,
            selector_route_accuracy=1.0,
            coverage_teacher_accuracy=1.0,
            checkpoint_combinations=81,
            decision_rows=648,
            readable_decisions=486,
            nonreadable_decisions=162,
            integration_accuracy=1.0,
            expected_coverage_accuracy=1.0,
            readable_answer_accuracy=1.0,
            nonreadable_suppression_accuracy=1.0,
            missing_oos_confusions=0,
            placement_mismatches=0,
            operation_failures=0,
            learned_writer_operation_applications=18,
            oracle_initialization_writes=12,
            oracle_end_scope_ops=3,
            chunk_commits=18,
            frozen_writer_forward_calls=3,
            frozen_coverage_forward_calls=9,
            frozen_selector_forward_calls=3,
            frozen_reader_forward_calls=27,
            new_training_steps=0,
        )
        self.assertTrue(c220.gate(summary))

    def test_27_gate_rejects_integration_error(self):
        summary = dict(
            all_writer_checkpoint_roundtrips=True,
            all_coverage_checkpoint_roundtrips=True,
            all_selector_checkpoint_roundtrips=True,
            all_reader_checkpoint_roundtrips=True,
            writer_target_accuracy=1.0,
            selector_route_accuracy=1.0,
            coverage_teacher_accuracy=1.0,
            checkpoint_combinations=81,
            decision_rows=648,
            readable_decisions=486,
            nonreadable_decisions=162,
            integration_accuracy=647.0 / 648.0,
            expected_coverage_accuracy=1.0,
            readable_answer_accuracy=1.0,
            nonreadable_suppression_accuracy=1.0,
            missing_oos_confusions=0,
            placement_mismatches=0,
            operation_failures=0,
            learned_writer_operation_applications=18,
            oracle_initialization_writes=12,
            oracle_end_scope_ops=3,
            chunk_commits=18,
            frozen_writer_forward_calls=3,
            frozen_coverage_forward_calls=9,
            frozen_selector_forward_calls=3,
            frozen_reader_forward_calls=27,
            new_training_steps=0,
        )
        self.assertFalse(c220.gate(summary))

    def test_28_gate_rejects_missing_oos_confusion(self):
        self.assertFalse(c220.gate(dict(
            all_writer_checkpoint_roundtrips=True,
            all_coverage_checkpoint_roundtrips=True,
            all_selector_checkpoint_roundtrips=True,
            all_reader_checkpoint_roundtrips=True,
            writer_target_accuracy=1.0, selector_route_accuracy=1.0,
            coverage_teacher_accuracy=1.0, checkpoint_combinations=81,
            decision_rows=648, readable_decisions=486, nonreadable_decisions=162,
            integration_accuracy=1.0, expected_coverage_accuracy=1.0,
            readable_answer_accuracy=1.0, nonreadable_suppression_accuracy=1.0,
            missing_oos_confusions=1, placement_mismatches=0, operation_failures=0,
            learned_writer_operation_applications=18, oracle_initialization_writes=12,
            oracle_end_scope_ops=3, chunk_commits=18, frozen_writer_forward_calls=3,
            frozen_coverage_forward_calls=9, frozen_selector_forward_calls=3,
            frozen_reader_forward_calls=27, new_training_steps=0,
        )))

    def test_29_operation_kind_remains_oracle(self):
        m = c220.manifest()
        self.assertEqual(m["operation_kind"], "oracle ASSERT/REPLACE/END_SCOPE")
        self.assertEqual(m["new_training_steps"], 0)

    def test_30_precheck_uses_c219_checkpoint_root(self):
        source = inspect.getsource(c220.precheck)
        self.assertIn("PARENT_C219_SHA", source)
        self.assertIn("PARENT_C219_VALIDATION_SHA", source)
        self.assertIn('p219["input_sha256"]', source)
        self.assertNotIn("c218_summary", source)

    def test_31_all_four_checkpoint_families_are_resolved(self):
        self.assertIn("writer-checkpoints.pt", inspect.getsource(c220.restore_writer_models))
        self.assertIn("coverage-checkpoints.pt", inspect.getsource(c220.restore_coverage_models))
        self.assertIn("selector-checkpoints.pt", inspect.getsource(c220.restore_selector_models))
        self.assertIn("reader-checkpoints.pt", inspect.getsource(c220.restore_reader_models))

    def test_32_direct_repo_dependencies_are_registered(self):
        self.assertEqual(len(c220.DIRECT_REPO_DEPENDENCIES), 14)
        self.assertIn("fold_lm/v05/memory_stack.py", c220.DIRECT_REPO_DEPENDENCIES)
        self.assertIn(
            "fold_lm/v05_benchmarks/gate_f_c219_learned_coverage.py",
            c220.DIRECT_REPO_DEPENDENCIES,
        )

    def test_33_regression_suite_semantic_counts(self):
        root = Path(__file__).resolve().parents[1]
        names = c220.regression_modules(root)
        loaded = unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids = [t.id() for t in c220.c205._iter_tests(loaded)]
        self.assertEqual((len(names), len(all_ids)), (105, 2336))
        suite = c220.regression_suite(root)
        kept = [t.id() for t in c220.c205._iter_tests(suite)]
        self.assertEqual(len(kept), 2335)
        for excluded in c220.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded), 1)
            self.assertNotIn(excluded, kept)

    def test_34_python_alias_bindings_are_complete(self):
        root = Path(__file__).resolve().parents[1]
        for path in (
            root / "fold_lm" / "v05" / "memory_stack.py",
            root / "fold_lm" / "v05_benchmarks" / "gate_f_c220_frozen_learned_stack.py",
            Path(__file__),
        ):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            bound = set()
            for node in tree.body:
                if isinstance(node, ast.Import):
                    bound.update(a.asname or a.name.split(".")[0] for a in node.names)
                elif isinstance(node, ast.ImportFrom):
                    bound.update(a.asname or a.name for a in node.names)
            refs = {
                node.value.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and re.fullmatch(r"c\d{3}", node.value.id)
            }
            self.assertEqual(refs - bound, set())

    def test_35_manifest_forward_and_decision_counts_are_consistent(self):
        m = c220.manifest()
        self.assertEqual(
            (
                m["checkpoint_combinations"],
                m["decision_rows"],
                m["readable_decisions"],
                m["nonreadable_decisions"],
            ),
            (81, 648, 486, 162),
        )
        self.assertEqual(
            m["model_forward_calls"],
            m["frozen_writer_forward_calls"]
            + m["frozen_coverage_forward_calls"]
            + m["frozen_selector_forward_calls"]
            + m["frozen_reader_forward_calls"],
        )

    def test_36_powershell_guards_and_parent_path(self):
        root = Path(__file__).resolve().parents[1]
        launcher = (root / "tools" / "invoke_c220.ps1").read_text(encoding="utf-8")
        runner = (root / "tools" / "run_c220.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2335", runner)
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile", launcher)
        self.assertIn("RUNNER_PARSE_ERROR", launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c220.ps1"', launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "220"', launcher)
        self.assertIn(
            "runs\\c219-v5f-learned-coverage-5c3f67fd3c36442ca332ddfc76717e19\\summary.json",
            launcher,
        )
        self.assertIn("$failure = $null", launcher)
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )

    def test_37_scope_is_integration_only_and_not_gate_f(self):
        m = c220.manifest()
        self.assertTrue(m["learned_components_frozen"])
        self.assertEqual(m["new_training_steps"], 0)
        self.assertEqual(m["operation_kind"], "oracle ASSERT/REPLACE/END_SCOPE")
        self.assertFalse(m["gate_f_candidate"])

    def test_38_run_has_no_optimizer_or_training_loop(self):
        source = inspect.getsource(c220.run)
        self.assertNotIn("optim.", source)
        self.assertNotIn(".backward(", source)
        self.assertEqual(c220.manifest()["new_training_steps"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
