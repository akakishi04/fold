import ast
import inspect
import re
import unittest
from pathlib import Path

import numpy as np
import torch

from fold_lm.v05 import memory_bank as bankmod
from fold_lm.v05 import memory_reader as reader
from fold_lm.v05_benchmarks import gate_f_c216_learned_reader as c216


class C216Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = c216.dataset()

    def test_01_manifest_hash(self):
        self.assertEqual(c216.digest(c216.manifest()), c216.MANIFEST_SHA)

    def test_02_parent_c215_identity_is_exact(self):
        self.assertEqual(
            (c216.PARENT_C215_EXECUTION, c216.PARENT_C215_SHA),
            (
                "663f42ca21f977b6530e4df8709fc306c2ebd8c9",
                "96b3e5b9cf465b9dea33920de095fc5d7d8e4c0cba960d64597c95fc15eda237",
            ),
        )
        self.assertEqual(
            c216.PARENT_C215_VALIDATION_SHA,
            "1aa90b651d2f25a2ae72173e2e4e072236572e4057f40a35180a592980e90bd3",
        )

    def test_03_data_hash_is_fixed(self):
        self.assertEqual(self.data["content_sha256"], c216.DATA_SHA)

    def test_04_dataset_profile_is_exact(self):
        self.assertEqual(
            self.data["profile"],
            dict(
                rows=36,
                train_rows=24,
                eval_rows=12,
                train_pairs=6,
                eval_pairs=3,
                train_class_counts=[8, 8, 8],
                eval_class_counts=[4, 4, 4],
                selector_calls=36,
                writer_operations=18,
                chunk_commits=18,
            ),
        )

    def test_05_eval_pairs_are_exactly_preregistered(self):
        rows = self.data["metadata"]
        pairs = {
            (r["alpha_class"], r["beta_class"])
            for r in rows
            if r["split"] == "EVAL"
        }
        self.assertEqual(pairs, set(c216.EVAL_PAIRS))

    def test_06_train_and_eval_pair_sets_are_disjoint(self):
        rows = self.data["metadata"]
        train = {
            (r["alpha_class"], r["beta_class"])
            for r in rows
            if r["split"] == "TRAIN"
        }
        ev = {
            (r["alpha_class"], r["beta_class"])
            for r in rows
            if r["split"] == "EVAL"
        }
        self.assertFalse(train & ev)
        self.assertEqual(len(train | ev), 9)

    def test_07_each_semantic_value_occurs_in_both_splits(self):
        rows = self.data["metadata"]
        for split in ("TRAIN", "EVAL"):
            for factor in ("alpha_class", "beta_class"):
                self.assertEqual({r[factor] for r in rows if r["split"] == split}, {0, 1, 2})

    def test_08_train_targets_are_balanced(self):
        mask = self.data["split_codes"] == 0
        self.assertEqual(
            np.bincount(self.data["labels"][mask], minlength=3).tolist(),
            [8, 8, 8],
        )

    def test_09_eval_targets_are_balanced(self):
        mask = self.data["split_codes"] == 1
        self.assertEqual(
            np.bincount(self.data["labels"][mask], minlength=3).tolist(),
            [4, 4, 4],
        )

    def test_10_each_pair_has_hot_and_committed_rows(self):
        rows = self.data["metadata"]
        for combo_id in range(9):
            self.assertEqual(
                {r["placement"] for r in rows if r["combo_id"] == combo_id},
                {"HOT", "COMMITTED"},
            )

    def test_11_each_pair_has_both_queries(self):
        rows = self.data["metadata"]
        for combo_id in range(9):
            self.assertEqual(
                {r["query"] for r in rows if r["combo_id"] == combo_id},
                {"alpha", "beta"},
            )

    def test_12_hot_and_committed_selected_features_are_identical(self):
        rows = self.data["metadata"]
        x = self.data["features"]
        keyed = {}
        for i, row in enumerate(rows):
            key = (row["combo_id"], row["query"])
            keyed.setdefault(key, {})[row["placement"]] = float(x[i, 0])
        self.assertEqual(len(keyed), 18)
        for value in keyed.values():
            self.assertEqual(value["HOT"], value["COMMITTED"])

    def test_13_selected_feature_has_only_three_values(self):
        values = sorted(set(float(v) for v in self.data["features"][:, 0]))
        self.assertEqual(len(values), 3)
        self.assertAlmostEqual(values[0], -0.75 / 4.25, places=15)
        self.assertEqual(values[1], 0.0)
        self.assertAlmostEqual(values[2], 0.75 / 4.25, places=15)

    def test_14_reader_config_is_exact(self):
        config = reader.MemoryReaderConfig()
        self.assertEqual(
            (config.input_width, config.hidden_width, config.answer_classes),
            (1, 8, 3),
        )

    def test_15_reader_parameter_count_is_43(self):
        self.assertEqual(reader.parameter_count(c216.new_reader()), 43)

    def test_16_reader_rejects_wrong_shape(self):
        model = c216.new_reader()
        with self.assertRaises(ValueError):
            model(torch.zeros((2, 2), dtype=torch.float32))

    def test_17_reader_rejects_nonfloat(self):
        model = c216.new_reader()
        with self.assertRaises(TypeError):
            model(torch.zeros((2, 1), dtype=torch.int64))

    def test_18_reader_rejects_nonfinite(self):
        model = c216.new_reader()
        with self.assertRaises(ValueError):
            model(torch.tensor([[float("nan")]], dtype=torch.float32))

    def test_19_reader_forward_shape_is_three_class(self):
        model = c216.new_reader()
        logits = model(torch.zeros((5, 1), dtype=torch.float32))
        self.assertEqual(tuple(logits.shape), (5, 3))

    def test_20_model_input_has_no_query_feature(self):
        self.assertEqual(c216.manifest()["reader_query_features"], 0)
        source = inspect.getsource(reader.MemoryReader.forward)
        self.assertNotIn("query", source.lower())

    def test_21_model_input_has_no_status_feature(self):
        self.assertEqual(c216.manifest()["reader_status_features"], 0)
        source = inspect.getsource(reader.MemoryReader.forward)
        self.assertNotIn("status", source.lower())

    def test_22_oracle_selector_is_outside_reader(self):
        source = inspect.getsource(c216.dataset)
        self.assertIn("read.value[query_id]", source)
        reader_source = inspect.getsource(reader.MemoryReader)
        self.assertNotIn("query_id", reader_source)
        self.assertNotIn("argmax", reader_source)

    def test_23_writer_and_selector_are_not_learned(self):
        m = c216.manifest()
        self.assertTrue(m["learned_reader"])
        self.assertFalse(m["learned_writer"])
        self.assertFalse(m["port_selector"])
        self.assertFalse(m["coverage_classifier"])

    def test_24_training_registration_is_exact(self):
        m = c216.manifest()
        self.assertEqual(m["seeds"], [216001, 216002, 216003])
        self.assertEqual((m["steps"], m["batch_size"], m["lr"]), (400, 24, 0.02))
        self.assertEqual(m["optimizer"], "Adam")
        self.assertEqual(m["sampling"], "full-batch deterministic")

    def test_25_gate_requires_all_three_seed_records(self):
        good = dict(
            train_accuracy=1.0,
            eval_accuracy=1.0,
            eval_hot_accuracy=1.0,
            eval_committed_accuracy=1.0,
            zero_readout_eval_accuracy=1.0 / 3.0,
            placement_prediction_mismatches=0,
        )
        summary = dict(
            seed_records=[dict(seed=s, **good) for s in c216.SEEDS],
            all_checkpoint_roundtrips=True,
            data_sha256=c216.DATA_SHA,
            oracle_selector_calls=36,
            oracle_writer_operations=18,
            chunk_commits=18,
            reader_query_features=0,
            reader_status_features=0,
            learned_reader_calls=1215,
            learned_writer_calls=0,
            port_selector_learned_calls=0,
            coverage_classifier_calls=0,
        )
        self.assertTrue(c216.gate(summary))

    def test_26_gate_rejects_one_eval_error(self):
        good = dict(
            train_accuracy=1.0,
            eval_accuracy=1.0,
            eval_hot_accuracy=1.0,
            eval_committed_accuracy=1.0,
            zero_readout_eval_accuracy=1.0 / 3.0,
            placement_prediction_mismatches=0,
        )
        records = [dict(seed=s, **good) for s in c216.SEEDS]
        records[1]["eval_accuracy"] = 11.0 / 12.0
        summary = dict(
            seed_records=records,
            all_checkpoint_roundtrips=True,
            data_sha256=c216.DATA_SHA,
            oracle_selector_calls=36,
            oracle_writer_operations=18,
            chunk_commits=18,
            reader_query_features=0,
            reader_status_features=0,
            learned_reader_calls=1215,
            learned_writer_calls=0,
            port_selector_learned_calls=0,
            coverage_classifier_calls=0,
        )
        self.assertFalse(c216.gate(summary))

    def test_27_gate_rejects_readout_blind_success(self):
        good = dict(
            train_accuracy=1.0,
            eval_accuracy=1.0,
            eval_hot_accuracy=1.0,
            eval_committed_accuracy=1.0,
            zero_readout_eval_accuracy=1.0,
            placement_prediction_mismatches=0,
        )
        summary = dict(
            seed_records=[dict(seed=s, **good) for s in c216.SEEDS],
            all_checkpoint_roundtrips=True,
            data_sha256=c216.DATA_SHA,
            oracle_selector_calls=36,
            oracle_writer_operations=18,
            chunk_commits=18,
            reader_query_features=0,
            reader_status_features=0,
            learned_reader_calls=1215,
            learned_writer_calls=0,
            port_selector_learned_calls=0,
            coverage_classifier_calls=0,
        )
        self.assertFalse(c216.gate(summary))

    def test_28_gate_rejects_placement_flip(self):
        score = dict(
            train_accuracy=1.0,
            eval_accuracy=1.0,
            eval_hot_accuracy=1.0,
            eval_committed_accuracy=1.0,
            zero_readout_eval_accuracy=1.0 / 3.0,
            placement_prediction_mismatches=1,
        )
        self.assertFalse(c216.seed_pass(score))

    def test_29_zero_readout_expected_accuracy_is_one_third(self):
        self.assertAlmostEqual(c216.ZERO_EXPECTED, 1.0 / 3.0, places=15)

    def test_30_precheck_uses_c215_as_checkpoint_root(self):
        source = inspect.getsource(c216.precheck)
        self.assertIn("PARENT_C215_SHA", source)
        self.assertIn("PARENT_C215_VALIDATION_SHA", source)
        self.assertIn('p215["source_blobs"]', source)
        self.assertNotIn("c214_summary", source)
        self.assertNotIn("c213_summary", source)

    def test_31_direct_repo_dependencies_are_registered(self):
        self.assertEqual(len(c216.DIRECT_REPO_DEPENDENCIES), 7)
        self.assertIn("fold_lm/v05/memory_reader.py", c216.DIRECT_REPO_DEPENDENCIES)
        self.assertIn("fold_lm/v05/memory_bank.py", c216.DIRECT_REPO_DEPENDENCIES)
        self.assertIn(
            "fold_lm/v05_benchmarks/gate_f_c215_h1_h2_chunk_commit.py",
            c216.DIRECT_REPO_DEPENDENCIES,
        )
        self.assertEqual(c216.HISTORICAL_REGRESSION_RUNNER, "tools/run_c167.ps1")
        self.assertEqual(
            c216.HISTORICAL_REGRESSION_RUNNER_BLOB,
            "7c5d6e9838d4ce7bd2bfec0e43458eb749fd1789",
        )

    def test_32_regression_suite_semantic_counts(self):
        root = Path(__file__).resolve().parents[1]
        names = c216.regression_modules(root)
        loaded = unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids = [t.id() for t in c216.c205._iter_tests(loaded)]
        self.assertEqual((len(names), len(all_ids)), (101, 2186))
        suite = c216.regression_suite(root)
        kept = [t.id() for t in c216.c205._iter_tests(suite)]
        self.assertEqual(len(kept), 2185)
        for excluded in c216.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded), 1)
            self.assertNotIn(excluded, kept)

    def test_33_python_alias_bindings_are_complete(self):
        root = Path(__file__).resolve().parents[1]
        for path in (
            root / "fold_lm" / "v05" / "memory_reader.py",
            root / "fold_lm" / "v05_benchmarks" / "gate_f_c216_learned_reader.py",
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

    def test_34_manifest_workload_forward_count_is_consistent(self):
        m = c216.manifest()
        self.assertEqual(m["training_steps_total"], 3 * m["steps"])
        self.assertEqual(m["training_examples_drawn"], 3 * m["steps"] * m["batch_size"])
        self.assertEqual(m["model_forward_calls_expected"], 3 * (m["steps"] + 5))

    def test_35_powershell_guards_and_parent_path(self):
        root = Path(__file__).resolve().parents[1]
        launcher = (root / "tools" / "invoke_c216.ps1").read_text(encoding="utf-8")
        runner = (root / "tools" / "run_c216.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2185", runner)
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile", launcher)
        self.assertIn("RUNNER_PARSE_ERROR", launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c216.ps1"', launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "216"', launcher)
        self.assertIn(
            "runs\\c215-v5f-h1-h2-chunk-commit-06e5fce5f05f46d0be1f86b8ec119877\\summary.json",
            launcher,
        )
        self.assertIn("$failure = $null", launcher)
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )

    def test_36_scope_has_no_writer_selector_or_coverage_training(self):
        m = c216.manifest()
        self.assertTrue(m["learned_reader"])
        self.assertFalse(m["learned_writer"])
        self.assertFalse(m["port_selector"])
        self.assertFalse(m["coverage_classifier"])
        self.assertFalse(m["gate_f_candidate"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
