import ast
import inspect
import re
import unittest
from pathlib import Path

import numpy as np
import torch

from fold_lm.v05 import memory_port_selector as selector
from fold_lm.v05_benchmarks import gate_f_c217_learned_port_selector as c217


class C217Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = c217.query_dataset()
        cls.rows, cls.downstream_counts = c217.downstream_fixture()

    def test_01_manifest_hash(self):
        self.assertEqual(c217.digest(c217.manifest()), c217.MANIFEST_SHA)

    def test_02_parent_c216_identity_is_exact(self):
        self.assertEqual(
            (c217.PARENT_C216_EXECUTION, c217.PARENT_C216_SHA),
            (
                "99d4254c09f38a433374fb2a073403d6e0ec764a",
                "7542625a054725d3a70dfa1c19f706fe8fce26af379e24b92aa1ae478483acc9",
            ),
        )
        self.assertEqual(
            c217.PARENT_C216_VALIDATION_SHA,
            "dddd27d04917f810a68dc83aa98cddabf1cd78cd67357c52b913e2ff3fe239be",
        )
        self.assertEqual(
            c217.PARENT_READER_CHECKPOINT_SHA,
            "bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af",
        )

    def test_03_query_data_hash_is_fixed(self):
        self.assertEqual(
            self.data["content_sha256"],
            "a9ec25d8079e27177567dd4ca85c7aee18f511eb8e8db6b774a61af82e91ac3d",
        )

    def test_04_query_dataset_profile_is_exact(self):
        self.assertEqual(tuple(self.data["features"].shape), (8, 4))
        self.assertEqual(int((self.data["split_codes"] == 0).sum()), 6)
        self.assertEqual(int((self.data["split_codes"] == 1).sum()), 2)

    def test_05_train_query_targets_are_balanced(self):
        train = self.data["split_codes"] == 0
        self.assertEqual(
            np.bincount(self.data["labels"][train], minlength=2).tolist(),
            [3, 3],
        )

    def test_06_eval_query_targets_are_balanced(self):
        ev = self.data["split_codes"] == 1
        self.assertEqual(
            np.bincount(self.data["labels"][ev], minlength=2).tolist(),
            [1, 1],
        )

    def test_07_train_and_eval_nuisance_are_disjoint(self):
        train = {
            tuple(row["nuisance"])
            for row in self.data["metadata"]
            if row["split"] == "TRAIN"
        }
        ev = {
            tuple(row["nuisance"])
            for row in self.data["metadata"]
            if row["split"] == "EVAL"
        }
        self.assertEqual(train, set(c217.TRAIN_NUISANCE))
        self.assertEqual(ev, set(c217.EVAL_NUISANCE))
        self.assertFalse(train & ev)

    def test_08_both_factor_roles_exist_in_both_splits(self):
        for split in ("TRAIN", "EVAL"):
            factors = {
                row["factor"]
                for row in self.data["metadata"]
                if row["split"] == split
            }
            self.assertEqual(factors, {"alpha", "beta"})

    def test_09_eval_role_blind_features_collapse_to_same_vector(self):
        ev = self.data["split_codes"] == 1
        x = self.data["features"][ev].copy()
        x[:, :2] = 0.0
        self.assertTrue(np.array_equal(x[0], x[1]))
        self.assertEqual(x[0].tolist(), [0.0, 0.0, 1.0, 1.0])

    def test_10_selector_config_is_exact(self):
        config = selector.MemoryPortSelectorConfig()
        self.assertEqual(
            (config.input_width, config.hidden_width, config.port_count),
            (4, 8, 2),
        )

    def test_11_selector_parameter_count_is_58(self):
        self.assertEqual(selector.parameter_count(c217.new_selector()), 58)

    def test_12_selector_rejects_wrong_shape(self):
        model = c217.new_selector()
        with self.assertRaises(ValueError):
            model(torch.zeros((2, 3), dtype=torch.float32))

    def test_13_selector_rejects_nonfloat(self):
        model = c217.new_selector()
        with self.assertRaises(TypeError):
            model(torch.zeros((2, 4), dtype=torch.int64))

    def test_14_selector_rejects_nonfinite(self):
        model = c217.new_selector()
        with self.assertRaises(ValueError):
            model(torch.tensor([[0.0, 0.0, 0.0, float("nan")]], dtype=torch.float32))

    def test_15_selector_forward_shape_is_two_ports(self):
        model = c217.new_selector()
        logits = model(torch.zeros((5, 4), dtype=torch.float32))
        self.assertEqual(tuple(logits.shape), (5, 2))

    def test_16_selector_module_does_not_accept_memory_values(self):
        source = inspect.getsource(selector.MemoryPortSelector.forward)
        self.assertIn("query_features", source)
        self.assertNotIn("memory", source.lower())
        self.assertNotIn("readout", source.lower())
        self.assertNotIn("reader", source.lower())

    def test_17_downstream_uses_only_unequal_semantic_pairs(self):
        self.assertEqual(len(c217.UNEQUAL_PAIRS), 6)
        self.assertTrue(all(a != b for a, b in c217.UNEQUAL_PAIRS))
        self.assertEqual(
            set(c217.UNEQUAL_PAIRS),
            {(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)},
        )

    def test_18_downstream_fixture_has_24_rows(self):
        self.assertEqual(len(self.rows), 24)

    def test_19_downstream_fixture_has_hot_and_committed(self):
        self.assertEqual({row["placement"] for row in self.rows}, {"HOT", "COMMITTED"})
        self.assertEqual(
            sum(row["placement"] == "HOT" for row in self.rows),
            12,
        )
        self.assertEqual(
            sum(row["placement"] == "COMMITTED" for row in self.rows),
            12,
        )

    def test_20_downstream_fixture_has_both_queries(self):
        self.assertEqual({row["query"] for row in self.rows}, {"alpha", "beta"})
        self.assertEqual(sum(row["query"] == "alpha" for row in self.rows), 12)
        self.assertEqual(sum(row["query"] == "beta" for row in self.rows), 12)

    def test_21_downstream_correct_and_wrong_ports_have_different_targets(self):
        for row in self.rows:
            self.assertNotEqual(row["alpha_class"], row["beta_class"])
            self.assertNotEqual(
                row["target_class"],
                row["beta_class"] if row["query"] == "alpha" else row["alpha_class"],
            )

    def test_22_oracle_writer_workload_is_exact(self):
        self.assertEqual(
            self.downstream_counts,
            {"oracle_writer_operations": 12, "chunk_commits": 12},
        )

    def test_23_reader_checkpoints_are_frozen_registered_parent_artifacts(self):
        self.assertEqual(c217.READER_SEEDS, (216001, 216002, 216003))
        self.assertEqual(
            c217.READER_FINAL_SHA256,
            (
                "6f1219b4277e3d4af6494ecf2280f2442887df05d5d133f2e2566b29bf804336",
                "1b7b2f96ad3e33d4ac0422cd7ca72b7f6e53707acf52aa17a44f188b7c2ed199",
                "3d26451e54a8e4327f2dcc9128e73c7e3fc60605c3e2d894876bd65057d2dd7f",
            ),
        )

    def test_24_training_registration_is_exact(self):
        m = c217.manifest()
        self.assertEqual(m["selector_seeds"], [217001, 217002, 217003])
        self.assertEqual((m["steps"], m["batch_size"], m["lr"]), (400, 6, 0.02))
        self.assertEqual(m["training_steps_total"], 1200)
        self.assertEqual(m["training_examples_drawn"], 7200)

    def test_25_gate_requires_all_three_selector_seeds(self):
        reader_records = [
            dict(
                reader_seed=s,
                downstream_accuracy=1.0,
                downstream_hot_accuracy=1.0,
                downstream_committed_accuracy=1.0,
                wrong_port_downstream_accuracy=0.0,
                placement_prediction_mismatches=0,
            )
            for s in c217.READER_SEEDS
        ]
        records = [
            dict(
                seed=s,
                checkpoint_roundtrip=True,
                train_port_accuracy=1.0,
                eval_port_accuracy=1.0,
                query_blind_eval_accuracy=0.5,
                reader_records=reader_records,
            )
            for s in c217.SELECTOR_SEEDS
        ]
        summary = dict(
            selector_seed_records=records,
            all_selector_checkpoint_roundtrips=True,
            all_reader_checkpoint_roundtrips=True,
            query_data_sha256=c217.QUERY_DATA_SHA,
            downstream_rows=24,
            learned_selector_calls=1209,
            frozen_reader_forward_calls=18,
            reader_training_steps=0,
            learned_writer_calls=0,
            coverage_classifier_calls=0,
            oracle_writer_operations=12,
            chunk_commits=12,
        )
        self.assertTrue(c217.gate(summary))

    def test_26_gate_rejects_one_port_error(self):
        record = dict(
            checkpoint_roundtrip=True,
            train_port_accuracy=1.0,
            eval_port_accuracy=0.5,
            query_blind_eval_accuracy=0.5,
            reader_records=[],
        )
        self.assertFalse(c217.selector_seed_pass(record))

    def test_27_gate_rejects_query_blind_success(self):
        record = dict(
            checkpoint_roundtrip=True,
            train_port_accuracy=1.0,
            eval_port_accuracy=1.0,
            query_blind_eval_accuracy=1.0,
            reader_records=[
                dict(
                    downstream_accuracy=1.0,
                    downstream_hot_accuracy=1.0,
                    downstream_committed_accuracy=1.0,
                    wrong_port_downstream_accuracy=0.0,
                    placement_prediction_mismatches=0,
                )
                for _ in range(3)
            ],
        )
        self.assertFalse(c217.selector_seed_pass(record))

    def test_28_gate_rejects_wrong_port_downstream_success(self):
        record = dict(
            checkpoint_roundtrip=True,
            train_port_accuracy=1.0,
            eval_port_accuracy=1.0,
            query_blind_eval_accuracy=0.5,
            reader_records=[
                dict(
                    downstream_accuracy=1.0,
                    downstream_hot_accuracy=1.0,
                    downstream_committed_accuracy=1.0,
                    wrong_port_downstream_accuracy=0.5,
                    placement_prediction_mismatches=0,
                )
                for _ in range(3)
            ],
        )
        self.assertFalse(c217.selector_seed_pass(record))

    def test_29_scope_freezes_reader_and_writer(self):
        m = c217.manifest()
        self.assertTrue(m["learned_port_selector"])
        self.assertFalse(m["learned_reader"])
        self.assertFalse(m["learned_writer"])
        self.assertFalse(m["coverage_classifier"])
        self.assertEqual(m["reader_training_steps"], 0)

    def test_30_precheck_uses_c216_as_checkpoint_root(self):
        source = inspect.getsource(c217.precheck)
        self.assertIn("PARENT_C216_SHA", source)
        self.assertIn("PARENT_C216_VALIDATION_SHA", source)
        self.assertIn("PARENT_READER_CHECKPOINT_SHA", source)
        self.assertIn('p216["source_blobs"]', source)
        self.assertNotIn("c215_summary", source)

    def test_31_direct_repo_dependencies_are_registered(self):
        self.assertEqual(len(c217.DIRECT_REPO_DEPENDENCIES), 9)
        self.assertIn("fold_lm/v05/memory_port_selector.py", c217.DIRECT_REPO_DEPENDENCIES)
        self.assertIn(
            "fold_lm/v05_benchmarks/gate_f_c216_learned_reader.py",
            c217.DIRECT_REPO_DEPENDENCIES,
        )

    def test_32_regression_suite_semantic_counts(self):
        root = Path(__file__).resolve().parents[1]
        names = c217.regression_modules(root)
        loaded = unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids = [t.id() for t in c217.c205._iter_tests(loaded)]
        self.assertEqual((len(names), len(all_ids)), (102, 2222))
        suite = c217.regression_suite(root)
        kept = [t.id() for t in c217.c205._iter_tests(suite)]
        self.assertEqual(len(kept), 2221)
        for excluded in c217.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded), 1)
            self.assertNotIn(excluded, kept)

    def test_33_python_alias_bindings_are_complete(self):
        root = Path(__file__).resolve().parents[1]
        for path in (
            root / "fold_lm" / "v05" / "memory_port_selector.py",
            root / "fold_lm" / "v05_benchmarks" / "gate_f_c217_learned_port_selector.py",
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
        m = c217.manifest()
        self.assertEqual(m["selector_forward_calls_expected"], 3 * (400 + 3))
        self.assertEqual(m["frozen_reader_forward_calls_expected"], 3 * 3 * 2)
        self.assertEqual(
            m["model_forward_calls_expected"],
            m["selector_forward_calls_expected"] + m["frozen_reader_forward_calls_expected"],
        )

    def test_35_powershell_guards_and_parent_path(self):
        root = Path(__file__).resolve().parents[1]
        launcher = (root / "tools" / "invoke_c217.ps1").read_text(encoding="utf-8")
        runner = (root / "tools" / "run_c217.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2221", runner)
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile", launcher)
        self.assertIn("RUNNER_PARSE_ERROR", launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c217.ps1"', launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "217"', launcher)
        self.assertIn(
            "runs\\c216-v5f-learned-reader-5fb7ef1e99ec4ee189a3047cc60953d0\\summary.json",
            launcher,
        )
        self.assertIn("$failure = $null", launcher)
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )

    def test_36_scope_is_not_gate_f_decision(self):
        self.assertFalse(c217.manifest()["gate_f_candidate"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
