import ast
import inspect
import re
import unittest
from pathlib import Path

import numpy as np
import torch

from fold_lm.v05 import memory_writer as writer
from fold_lm.v05_benchmarks import gate_f_c218_learned_writer as c218


class C218Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = c218.writer_dataset()
        cls.wrong_semantic_rows, cls.semantic_counts = c218.control_replace_rows(
            "WRONG_SEMANTIC"
        )
        cls.wrong_factor_rows, cls.factor_counts = c218.control_replace_rows(
            "WRONG_FACTOR"
        )

    def test_01_manifest_hash(self):
        self.assertEqual(c218.digest(c218.manifest()), c218.MANIFEST_SHA)

    def test_02_parent_c217_identity_is_exact(self):
        self.assertEqual(
            (c218.PARENT_C217_EXECUTION, c218.PARENT_C217_SHA),
            (
                "a6aac1273951b6e321573445e9f759f35fffb726",
                "cb27e93c9a6dc9d03875938c55c37f146c12278dec4c9ebb5a20da150fd847ab",
            ),
        )
        self.assertEqual(
            c218.PARENT_C217_VALIDATION_SHA,
            "7e46f83fc7c6702e36ede2d05f016018cf8d219c51248ef7d395815168409cf0",
        )

    def test_03_frozen_selector_artifact_identity_is_exact(self):
        self.assertEqual(
            c218.PARENT_SELECTOR_CHECKPOINT_SHA,
            "ab8892e6562a4801a30fea853fdbc712d69d9c5077e32c0b8fab6e555fead215",
        )

    def test_04_inherited_reader_artifact_identity_is_exact(self):
        self.assertEqual(
            c218.INHERITED_READER_CHECKPOINT_SHA,
            "bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af",
        )

    def test_05_writer_data_hash_is_fixed(self):
        self.assertEqual(
            self.data["content_sha256"],
            "06f8df444119f0332168a956e7f32e9690b88fa9c39749d3ecc2283c70213714",
        )

    def test_06_writer_dataset_profile_is_exact(self):
        train = self.data["split_codes"] == 0
        ev = self.data["split_codes"] == 1
        self.assertEqual(tuple(self.data["features"].shape), (24, 5))
        self.assertEqual((int(train.sum()), int(ev.sum())), (18, 6))
        self.assertEqual(
            np.bincount(self.data["labels"][train], minlength=6).tolist(),
            [3,3,3,3,3,3],
        )
        self.assertEqual(
            np.bincount(self.data["labels"][ev], minlength=6).tolist(),
            [1,1,1,1,1,1],
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
        self.assertEqual(train, set(c218.TRAIN_NUISANCE))
        self.assertEqual(ev, set(c218.EVAL_NUISANCE))
        self.assertFalse(train & ev)

    def test_08_both_factors_and_all_values_exist_in_both_splits(self):
        for split in ("TRAIN", "EVAL"):
            rows = [row for row in self.data["metadata"] if row["split"] == split]
            self.assertEqual({row["factor"] for row in rows}, {"alpha","beta"})
            for factor in ("alpha","beta"):
                self.assertEqual(
                    {row["class_id"] for row in rows if row["factor"] == factor},
                    {0,1,2},
                )

    def test_09_relation_class_vocabulary_is_exact(self):
        self.assertEqual(
            c218.RELATION_CLASSES,
            (
                "alpha-class-0","alpha-class-1","alpha-class-2",
                "beta-class-0","beta-class-1","beta-class-2",
            ),
        )

    def test_10_factor_blind_eval_collapses_factor_pairs(self):
        ev = self.data["split_codes"] == 1
        x = self.data["features"][ev].copy()
        y = self.data["labels"][ev]
        x[:, :2] = 0.0
        for semantic_class in range(3):
            rows = x[(y % 3) == semantic_class]
            self.assertEqual(len(rows), 2)
            self.assertTrue(np.array_equal(rows[0], rows[1]))

    def test_11_semantic_blind_eval_collapses_three_values_per_factor(self):
        ev = self.data["split_codes"] == 1
        x = self.data["features"][ev].copy()
        y = self.data["labels"][ev]
        x[:, 2] = 0.0
        for factor_index in (0,1):
            rows = x[(y // 3) == factor_index]
            self.assertEqual(len(rows), 3)
            self.assertTrue(all(np.array_equal(rows[0], row) for row in rows[1:]))

    def test_12_writer_config_is_exact(self):
        config = writer.MemoryWriterConfig()
        self.assertEqual(
            (config.input_width, config.hidden_width, config.relation_classes),
            (5,12,6),
        )

    def test_13_writer_parameter_count_is_150(self):
        self.assertEqual(writer.parameter_count(c218.new_writer()), 150)

    def test_14_writer_rejects_wrong_shape(self):
        model = c218.new_writer()
        with self.assertRaises(ValueError):
            model(torch.zeros((2,4), dtype=torch.float32))

    def test_15_writer_rejects_nonfloat(self):
        model = c218.new_writer()
        with self.assertRaises(TypeError):
            model(torch.zeros((2,5), dtype=torch.int64))

    def test_16_writer_rejects_nonfinite(self):
        model = c218.new_writer()
        with self.assertRaises(ValueError):
            model(torch.tensor([[0.0,0.0,0.0,0.0,float("nan")]], dtype=torch.float32))

    def test_17_writer_forward_shape_is_six_relations(self):
        model = c218.new_writer()
        logits = model(torch.zeros((7,5), dtype=torch.float32))
        self.assertEqual(tuple(logits.shape), (7,6))

    def test_18_writer_module_does_not_accept_operation_or_memory_state(self):
        source = inspect.getsource(writer.MemoryWriter.forward).lower()
        self.assertIn("observation_features", source)
        self.assertNotIn("operation", source)
        self.assertNotIn("memory", source)
        self.assertNotIn("revision", source)

    def test_19_decode_write_class_is_exact(self):
        got = [c218.decode_write_class(i) for i in range(6)]
        self.assertEqual(
            got,
            [
                ("alpha",0,"global","alpha-class-0"),
                ("alpha",1,"global","alpha-class-1"),
                ("alpha",2,"global","alpha-class-2"),
                ("beta",0,"project","beta-class-0"),
                ("beta",1,"project","beta-class-1"),
                ("beta",2,"project","beta-class-2"),
            ],
        )

    def test_20_operation_kind_is_supplied_outside_writer(self):
        source = inspect.getsource(c218.memory_op)
        self.assertIn("kind=kind", source)
        writer_source = inspect.getsource(writer.MemoryWriter)
        self.assertNotIn("MemoryOpKind", writer_source)

    def test_21_assert_pairs_are_exactly_unequal(self):
        self.assertEqual(
            set(c218.UNEQUAL_PAIRS),
            {(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)},
        )
        self.assertTrue(all(a != b for a,b in c218.UNEQUAL_PAIRS))

    def test_22_wrong_semantic_control_has_six_valid_rows(self):
        self.assertEqual(len(self.wrong_semantic_rows), 6)
        self.assertTrue(all(row["valid"] for row in self.wrong_semantic_rows))
        self.assertEqual(
            self.semantic_counts,
            dict(
                learned_writer_operation_attempts=0,
                oracle_writer_operations=12,
                control_writer_operations=6,
                chunk_commits=12,
                write_rejections=0,
            ),
        )

    def test_23_wrong_factor_control_has_six_valid_rows(self):
        self.assertEqual(len(self.wrong_factor_rows), 6)
        self.assertTrue(all(row["valid"] for row in self.wrong_factor_rows))
        self.assertEqual(
            self.factor_counts,
            dict(
                learned_writer_operation_attempts=0,
                oracle_writer_operations=12,
                control_writer_operations=6,
                chunk_commits=12,
                write_rejections=0,
            ),
        )

    def test_24_training_registration_is_exact(self):
        m = c218.manifest()
        self.assertEqual(m["writer_seeds"], [218001,218002,218003])
        self.assertEqual((m["steps"],m["batch_size"],m["lr"]),(400,18,0.02))
        self.assertEqual(m["training_steps_total"],1200)
        self.assertEqual(m["training_examples_drawn"],21600)

    def test_25_gate_accepts_registered_complete_fixture(self):
        assert_metrics = dict(
            accuracy=1.0,
            hot_accuracy=1.0,
            committed_accuracy=1.0,
            placement_mismatches=0,
        )
        replace_metrics = dict(accuracy=1.0)
        records = [
            dict(
                seed=s,
                checkpoint_roundtrip=True,
                train_relation_accuracy=1.0,
                eval_relation_accuracy=1.0,
                factor_blind_eval_accuracy=0.5,
                semantic_blind_eval_accuracy=1.0/3.0,
                write_rejections=0,
                assert_metrics=assert_metrics,
                replace_metrics=replace_metrics,
            )
            for s in c218.WRITER_SEEDS
        ]
        summary = dict(
            writer_seed_records=records,
            all_writer_checkpoint_roundtrips=True,
            all_selector_checkpoint_roundtrips=True,
            all_reader_checkpoint_roundtrips=True,
            writer_data_sha256=c218.WRITER_DATA_SHA,
            wrong_semantic_control=dict(accuracy=0.0),
            wrong_factor_control=dict(accuracy=0.0),
            learned_writer_calls=1212,
            frozen_selector_forward_calls=3,
            frozen_reader_forward_calls=72,
            reader_training_steps=0,
            selector_training_steps=0,
            coverage_classifier_calls=0,
            learned_writer_operation_slots=54,
            actual_learned_writer_operation_attempts=54,
            oracle_writer_operations=60,
            control_writer_operations=12,
            chunk_commit_slots=96,
            successful_chunk_commits=96,
        )
        self.assertTrue(c218.gate(summary))

    def test_26_gate_rejects_one_relation_error(self):
        record = dict(
            checkpoint_roundtrip=True,
            train_relation_accuracy=1.0,
            eval_relation_accuracy=5.0/6.0,
            factor_blind_eval_accuracy=0.5,
            semantic_blind_eval_accuracy=1.0/3.0,
            write_rejections=0,
            assert_metrics=dict(
                accuracy=1.0,hot_accuracy=1.0,committed_accuracy=1.0,placement_mismatches=0
            ),
            replace_metrics=dict(accuracy=1.0),
        )
        self.assertFalse(c218.writer_seed_pass(record))

    def test_27_gate_rejects_factor_blind_success(self):
        record = dict(
            checkpoint_roundtrip=True,
            train_relation_accuracy=1.0,
            eval_relation_accuracy=1.0,
            factor_blind_eval_accuracy=1.0,
            semantic_blind_eval_accuracy=1.0/3.0,
            write_rejections=0,
            assert_metrics=dict(
                accuracy=1.0,hot_accuracy=1.0,committed_accuracy=1.0,placement_mismatches=0
            ),
            replace_metrics=dict(accuracy=1.0),
        )
        self.assertFalse(c218.writer_seed_pass(record))

    def test_28_gate_rejects_semantic_blind_success(self):
        record = dict(
            checkpoint_roundtrip=True,
            train_relation_accuracy=1.0,
            eval_relation_accuracy=1.0,
            factor_blind_eval_accuracy=0.5,
            semantic_blind_eval_accuracy=1.0,
            write_rejections=0,
            assert_metrics=dict(
                accuracy=1.0,hot_accuracy=1.0,committed_accuracy=1.0,placement_mismatches=0
            ),
            replace_metrics=dict(accuracy=1.0),
        )
        self.assertFalse(c218.writer_seed_pass(record))

    def test_29_gate_rejects_write_rejection(self):
        record = dict(
            checkpoint_roundtrip=True,
            train_relation_accuracy=1.0,
            eval_relation_accuracy=1.0,
            factor_blind_eval_accuracy=0.5,
            semantic_blind_eval_accuracy=1.0/3.0,
            write_rejections=1,
            assert_metrics=dict(
                accuracy=1.0,hot_accuracy=1.0,committed_accuracy=1.0,placement_mismatches=0
            ),
            replace_metrics=dict(accuracy=1.0),
        )
        self.assertFalse(c218.writer_seed_pass(record))

    def test_30_gate_rejects_wrong_relation_control_success(self):
        good = dict(
            seed=218001,
            checkpoint_roundtrip=True,
            train_relation_accuracy=1.0,
            eval_relation_accuracy=1.0,
            factor_blind_eval_accuracy=0.5,
            semantic_blind_eval_accuracy=1.0/3.0,
            write_rejections=0,
            assert_metrics=dict(
                accuracy=1.0,hot_accuracy=1.0,committed_accuracy=1.0,placement_mismatches=0
            ),
            replace_metrics=dict(accuracy=1.0),
        )
        summary = dict(
            writer_seed_records=[
                good,
                dict(good,seed=218002),
                dict(good,seed=218003),
            ],
            all_writer_checkpoint_roundtrips=True,
            all_selector_checkpoint_roundtrips=True,
            all_reader_checkpoint_roundtrips=True,
            writer_data_sha256=c218.WRITER_DATA_SHA,
            wrong_semantic_control=dict(accuracy=0.5),
            wrong_factor_control=dict(accuracy=0.0),
            learned_writer_calls=1212,
            frozen_selector_forward_calls=3,
            frozen_reader_forward_calls=72,
            reader_training_steps=0,
            selector_training_steps=0,
            coverage_classifier_calls=0,
            learned_writer_operation_slots=54,
            actual_learned_writer_operation_attempts=54,
            oracle_writer_operations=60,
            control_writer_operations=12,
            chunk_commit_slots=96,
            successful_chunk_commits=96,
        )
        self.assertFalse(c218.gate(summary))

    def test_31_precheck_uses_c217_as_checkpoint_root(self):
        source = inspect.getsource(c218.precheck)
        self.assertIn("PARENT_C217_SHA", source)
        self.assertIn("PARENT_C217_VALIDATION_SHA", source)
        self.assertIn("PARENT_SELECTOR_CHECKPOINT_SHA", source)
        self.assertIn('p217["input_sha256"]', source)
        self.assertNotIn("c216_summary", source)

    def test_32_direct_repo_dependencies_are_registered(self):
        self.assertEqual(len(c218.DIRECT_REPO_DEPENDENCIES),11)
        self.assertIn("fold_lm/v05/memory_writer.py",c218.DIRECT_REPO_DEPENDENCIES)
        self.assertIn(
            "fold_lm/v05_benchmarks/gate_f_c217_learned_port_selector.py",
            c218.DIRECT_REPO_DEPENDENCIES,
        )

    def test_33_inherited_reader_checkpoint_is_resolved_from_parent_protection(self):
        source = inspect.getsource(c218.restore_readers)
        self.assertIn("find_protected_input", source)
        self.assertIn("INHERITED_READER_CHECKPOINT_SHA", source)

    def test_34_regression_suite_semantic_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=c218.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids=[t.id() for t in c218.c205._iter_tests(loaded)]
        self.assertEqual((len(names),len(all_ids)),(103,2260))
        suite=c218.regression_suite(root)
        kept=[t.id() for t in c218.c205._iter_tests(suite)]
        self.assertEqual(len(kept),2259)
        for excluded in c218.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded),1)
            self.assertNotIn(excluded,kept)

    def test_35_python_alias_bindings_are_complete(self):
        root=Path(__file__).resolve().parents[1]
        for path in (
            root/"fold_lm"/"v05"/"memory_writer.py",
            root/"fold_lm"/"v05_benchmarks"/"gate_f_c218_learned_writer.py",
            Path(__file__),
        ):
            tree=ast.parse(path.read_text(encoding="utf-8"))
            bound=set()
            for node in tree.body:
                if isinstance(node,ast.Import):
                    bound.update(a.asname or a.name.split(".")[0] for a in node.names)
                elif isinstance(node,ast.ImportFrom):
                    bound.update(a.asname or a.name for a in node.names)
            refs={
                node.value.id for node in ast.walk(tree)
                if isinstance(node,ast.Attribute)
                and isinstance(node.value,ast.Name)
                and re.fullmatch(r"c\d{3}",node.value.id)
            }
            self.assertEqual(refs-bound,set())

    def test_36_manifest_workload_forward_count_is_consistent(self):
        m=c218.manifest()
        self.assertEqual(m["learned_writer_forward_calls_expected"],3*(400+4))
        self.assertEqual(m["frozen_selector_forward_calls_expected"],3)
        self.assertEqual(m["frozen_reader_forward_calls_expected"],72)
        self.assertEqual(
            m["model_forward_calls_expected"],
            m["learned_writer_forward_calls_expected"]
            +m["frozen_selector_forward_calls_expected"]
            +m["frozen_reader_forward_calls_expected"],
        )
        self.assertEqual(
            (
                m["learned_writer_operation_slots"],
                m["oracle_writer_operations"],
                m["control_writer_operations"],
                m["chunk_commit_slots"],
            ),
            (54,60,12,96),
        )

    def test_37_powershell_guards_and_parent_path(self):
        root=Path(__file__).resolve().parents[1]
        launcher=(root/"tools"/"invoke_c218.ps1").read_text(encoding="utf-8")
        runner=(root/"tools"/"run_c218.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2259",runner)
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",launcher)
        self.assertIn("RUNNER_PARSE_ERROR",launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c218.ps1"',launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "218"',launcher)
        self.assertIn(
            "runs\\c217-v5f-learned-port-selector-6dfc0082313d48aa826750203c887bc6\\summary.json",
            launcher,
        )
        self.assertIn("$failure = $null",launcher)
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )

    def test_38_scope_is_writer_only_and_not_gate_f(self):
        m=c218.manifest()
        self.assertEqual(m["operation_kind"],"oracle ASSERT/REPLACE")
        self.assertEqual(m["reader_training_steps"],0)
        self.assertEqual(m["selector_training_steps"],0)
        self.assertFalse(m["coverage_classifier"])
        self.assertFalse(m["gate_f_candidate"])


if __name__=="__main__":
    unittest.main(verbosity=2)
