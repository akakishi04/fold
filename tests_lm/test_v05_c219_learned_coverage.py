import ast
import inspect
import re
import unittest
from pathlib import Path

import numpy as np
import torch

from fold_lm.v05 import memory_coverage as coverage
from fold_lm.v05_benchmarks import gate_f_c219_learned_coverage as c219


class C219Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = c219.coverage_dataset()

    def test_01_manifest_hash(self):
        self.assertEqual(c219.digest(c219.manifest()), c219.MANIFEST_SHA)

    def test_02_parent_c218_identity_is_exact(self):
        self.assertEqual(
            (c219.PARENT_C218_EXECUTION, c219.PARENT_C218_SHA),
            (
                "ce5ae96f5fe3a08213ee41bffa17ba97c10bb368",
                "50ec397534901bb865731b615232c555cfcf0222571f42b09098eae77f49f021",
            ),
        )
        self.assertEqual(
            c219.PARENT_C218_VALIDATION_SHA,
            "a0b235393fe3cd267534ecaa6de7190b534eb59a5fb8b95b1de083b6b4563359",
        )

    def test_03_inherited_checkpoint_identities_are_exact(self):
        self.assertEqual(
            c219.INHERITED_SELECTOR_CHECKPOINT_SHA,
            "ab8892e6562a4801a30fea853fdbc712d69d9c5077e32c0b8fab6e555fead215",
        )
        self.assertEqual(
            c219.INHERITED_READER_CHECKPOINT_SHA,
            "bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af",
        )

    def test_04_coverage_taxonomy_is_exact(self):
        self.assertEqual(
            tuple(x.name for x in coverage.CoverageClass),
            ("SUPPORTED","HOT_REQUIRED","MISSING","OUT_OF_SCOPE"),
        )
        self.assertEqual(tuple(int(x) for x in coverage.CoverageClass),(0,1,2,3))

    def test_05_numeric_unsafe_is_not_coverage_class(self):
        self.assertNotIn("NUMERIC_UNSAFE", {x.name for x in coverage.CoverageClass})
        self.assertTrue(c219.manifest()["numeric_unsafe_excluded"])

    def test_06_data_hash_is_fixed(self):
        self.assertEqual(
            self.data["content_sha256"],
            "3e9c74b7675439c3118f6a87bc7594455360512e906d69c1c739cae9edc34d65",
        )

    def test_07_dataset_shape_is_exact(self):
        self.assertEqual(tuple(self.data["features"].shape),(32,7))
        self.assertEqual(tuple(self.data["labels"].shape),(32,))

    def test_08_train_eval_rows_are_exact(self):
        self.assertEqual(int((self.data["split_codes"]==0).sum()),24)
        self.assertEqual(int((self.data["split_codes"]==1).sum()),8)

    def test_09_train_classes_are_balanced(self):
        mask=self.data["split_codes"]==0
        self.assertEqual(np.bincount(self.data["labels"][mask],minlength=4).tolist(),[6,6,6,6])

    def test_10_eval_classes_are_balanced(self):
        mask=self.data["split_codes"]==1
        self.assertEqual(np.bincount(self.data["labels"][mask],minlength=4).tolist(),[2,2,2,2])

    def test_11_train_eval_nuisance_are_disjoint(self):
        train={tuple(x["nuisance"]) for x in self.data["metadata"] if x["split"]=="TRAIN"}
        ev={tuple(x["nuisance"]) for x in self.data["metadata"] if x["split"]=="EVAL"}
        self.assertEqual(train,set(c219.TRAIN_NUISANCE))
        self.assertEqual(ev,set(c219.EVAL_NUISANCE))
        self.assertFalse(train&ev)

    def test_12_both_queries_have_all_four_statuses(self):
        for query in ("alpha","beta"):
            self.assertEqual(
                {x["coverage"] for x in self.data["metadata"] if x["query"]==query},
                set(c219.COVERAGE_NAMES),
            )

    def test_13_target_summary_supported_bits_are_exact(self):
        _,state,factor,scope=c219.build_state(0,int(coverage.CoverageClass.SUPPORTED))
        feature,status=coverage.target_summary(
            state,query_role=0,scope_id=scope,factor_id=factor,nuisance=(1.0,1.0)
        )
        self.assertEqual(int(status),0)
        self.assertEqual(feature.tolist(),[1.0,0.0,1.0,0.0,1.0,1.0,1.0])

    def test_14_target_summary_hot_bits_are_exact(self):
        _,state,factor,scope=c219.build_state(0,int(coverage.CoverageClass.HOT_REQUIRED))
        feature,status=coverage.target_summary(
            state,query_role=0,scope_id=scope,factor_id=factor,nuisance=(1.0,1.0)
        )
        self.assertEqual(int(status),1)
        self.assertEqual(feature.tolist(),[1.0,0.0,0.0,1.0,1.0,1.0,1.0])

    def test_15_target_summary_missing_bits_are_exact(self):
        _,state,factor,scope=c219.build_state(1,int(coverage.CoverageClass.MISSING))
        feature,status=coverage.target_summary(
            state,query_role=1,scope_id=scope,factor_id=factor,nuisance=(1.0,1.0)
        )
        self.assertEqual(int(status),2)
        self.assertEqual(feature.tolist(),[0.0,1.0,0.0,0.0,1.0,1.0,1.0])

    def test_16_target_summary_out_of_scope_bits_are_exact(self):
        _,state,factor,scope=c219.build_state(1,int(coverage.CoverageClass.OUT_OF_SCOPE))
        feature,status=coverage.target_summary(
            state,query_role=1,scope_id=scope,factor_id=factor,nuisance=(1.0,1.0)
        )
        self.assertEqual(int(status),3)
        self.assertEqual(feature.tolist(),[0.0,1.0,0.0,0.0,0.0,1.0,1.0])

    def test_17_classifier_config_is_exact(self):
        config=coverage.MemoryCoverageConfig()
        self.assertEqual((config.input_width,config.hidden_width,config.class_count),(7,12,4))

    def test_18_classifier_parameter_count_is_148(self):
        self.assertEqual(coverage.parameter_count(c219.new_classifier()),148)

    def test_19_classifier_rejects_wrong_shape(self):
        with self.assertRaises(ValueError):
            c219.new_classifier()(torch.zeros((2,6),dtype=torch.float32))

    def test_20_classifier_rejects_nonfloat(self):
        with self.assertRaises(TypeError):
            c219.new_classifier()(torch.zeros((2,7),dtype=torch.int64))

    def test_21_classifier_rejects_nonfinite(self):
        with self.assertRaises(ValueError):
            c219.new_classifier()(
                torch.tensor([[0,0,0,0,0,0,float("nan")]],dtype=torch.float32)
            )

    def test_22_classifier_forward_shape_is_four_classes(self):
        logits=c219.new_classifier()(torch.zeros((5,7),dtype=torch.float32))
        self.assertEqual(tuple(logits.shape),(5,4))

    def test_23_state_blind_eval_collapses_each_query_across_four_classes(self):
        ev=self.data["split_codes"]==1
        x=self.data["features"][ev].copy()
        y=self.data["labels"][ev]
        x[:,2:5]=0.0
        for role in (0,1):
            rows=x[x[:,role]==1.0]
            self.assertEqual(len(rows),4)
            self.assertTrue(all(np.array_equal(rows[0],r) for r in rows[1:]))
        self.assertEqual(np.bincount(y,minlength=4).tolist(),[2,2,2,2])

    def test_24_tier_blind_readable_pairs_collapse(self):
        ev=self.data["split_codes"]==1
        y=self.data["labels"]
        mask=ev&((y==0)|(y==1))
        x=self.data["features"][mask].copy()
        x[:,2:4]=0.0
        for role in (0,1):
            rows=x[x[:,role]==1.0]
            self.assertEqual(len(rows),2)
            self.assertTrue(np.array_equal(rows[0],rows[1]))

    def test_25_scope_blind_missing_oos_pairs_collapse(self):
        ev=self.data["split_codes"]==1
        y=self.data["labels"]
        mask=ev&((y==2)|(y==3))
        x=self.data["features"][mask].copy()
        x[:,4]=0.0
        for role in (0,1):
            rows=x[x[:,role]==1.0]
            self.assertEqual(len(rows),2)
            self.assertTrue(np.array_equal(rows[0],rows[1]))

    def test_26_training_registration_is_exact(self):
        m=c219.manifest()
        self.assertEqual(m["seeds"],[219001,219002,219003])
        self.assertEqual((m["steps"],m["batch_size"],m["lr"]),(400,24,0.02))
        self.assertEqual(m["training_steps_total"],1200)
        self.assertEqual(m["training_examples_drawn"],28800)

    def test_27_gate_accepts_registered_complete_fixture(self):
        rows=[
            dict(
                seed=s,checkpoint_roundtrip=True,
                train_accuracy=1.0,eval_accuracy=1.0,
                state_blind_eval_accuracy=0.25,
                tier_blind_readable_accuracy=0.0,
                scope_blind_missing_oos_accuracy=0.5,
                readable_gate_accuracy=1.0,
                nonreadable_suppression_accuracy=1.0,
                missing_oos_confusions=0,
            )
            for s in c219.COVERAGE_SEEDS
        ]
        summary=dict(
            coverage_seed_records=rows,
            all_coverage_checkpoint_roundtrips=True,
            all_selector_checkpoint_roundtrips=True,
            all_reader_checkpoint_roundtrips=True,
            coverage_data_sha256=c219.COVERAGE_DATA_SHA,
            readable_reference=dict(accuracy=1.0,rows=4),
            learned_coverage_calls=1215,
            frozen_selector_forward_calls=3,
            frozen_reader_forward_calls=9,
            writer_training_steps=0,
            selector_training_steps=0,
            reader_training_steps=0,
            numeric_unsafe_classified=0,
        )
        self.assertTrue(c219.gate(summary))

    def test_28_gate_rejects_missing_oos_confusion(self):
        row=dict(
            checkpoint_roundtrip=True,train_accuracy=1.0,eval_accuracy=1.0,
            state_blind_eval_accuracy=0.25,tier_blind_readable_accuracy=0.0,
            scope_blind_missing_oos_accuracy=0.5,readable_gate_accuracy=1.0,
            nonreadable_suppression_accuracy=1.0,missing_oos_confusions=1,
        )
        self.assertFalse(c219.seed_pass(row))

    def test_29_gate_rejects_state_blind_success(self):
        row=dict(
            checkpoint_roundtrip=True,train_accuracy=1.0,eval_accuracy=1.0,
            state_blind_eval_accuracy=1.0,tier_blind_readable_accuracy=0.0,
            scope_blind_missing_oos_accuracy=0.5,readable_gate_accuracy=1.0,
            nonreadable_suppression_accuracy=1.0,missing_oos_confusions=0,
        )
        self.assertFalse(c219.seed_pass(row))

    def test_30_gate_rejects_scope_blind_missing_oos_success(self):
        row=dict(
            checkpoint_roundtrip=True,train_accuracy=1.0,eval_accuracy=1.0,
            state_blind_eval_accuracy=0.25,tier_blind_readable_accuracy=0.0,
            scope_blind_missing_oos_accuracy=1.0,readable_gate_accuracy=1.0,
            nonreadable_suppression_accuracy=1.0,missing_oos_confusions=0,
        )
        self.assertFalse(c219.seed_pass(row))

    def test_31_precheck_uses_c218_checkpoint_root(self):
        source=inspect.getsource(c219.precheck)
        self.assertIn("PARENT_C218_SHA",source)
        self.assertIn("PARENT_C218_VALIDATION_SHA",source)
        self.assertIn('p218["input_sha256"]',source)
        self.assertNotIn("c217_summary",source)

    def test_32_inherited_selector_reader_resolve_from_parent_protection(self):
        self.assertIn("find_protected_input",inspect.getsource(c219.restore_selectors))
        self.assertIn("find_protected_input",inspect.getsource(c219.restore_readers))

    def test_33_direct_dependencies_are_registered(self):
        self.assertEqual(len(c219.DIRECT_REPO_DEPENDENCIES),11)
        self.assertIn("fold_lm/v05/memory_coverage.py",c219.DIRECT_REPO_DEPENDENCIES)
        self.assertIn(
            "fold_lm/v05_benchmarks/gate_f_c218_learned_writer.py",
            c219.DIRECT_REPO_DEPENDENCIES,
        )

    def test_34_regression_suite_semantic_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=c219.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids=[t.id() for t in c219.c205._iter_tests(loaded)]
        self.assertEqual((len(names),len(all_ids)),(104,2298))
        suite=c219.regression_suite(root)
        kept=[t.id() for t in c219.c205._iter_tests(suite)]
        self.assertEqual(len(kept),2297)
        for excluded in c219.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded),1)
            self.assertNotIn(excluded,kept)

    def test_35_python_alias_bindings_are_complete(self):
        root=Path(__file__).resolve().parents[1]
        for path in (
            root/"fold_lm"/"v05"/"memory_coverage.py",
            root/"fold_lm"/"v05_benchmarks"/"gate_f_c219_learned_coverage.py",
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

    def test_36_manifest_workload_count_is_consistent(self):
        m=c219.manifest()
        self.assertEqual(m["learned_coverage_forward_calls_expected"],3*(400+5))
        self.assertEqual(m["frozen_selector_forward_calls_expected"],3)
        self.assertEqual(m["frozen_reader_forward_calls_expected"],9)
        self.assertEqual(
            m["model_forward_calls_expected"],
            m["learned_coverage_forward_calls_expected"]
            +m["frozen_selector_forward_calls_expected"]
            +m["frozen_reader_forward_calls_expected"],
        )

    def test_37_powershell_guards_and_parent_path(self):
        root=Path(__file__).resolve().parents[1]
        launcher=(root/"tools"/"invoke_c219.ps1").read_text(encoding="utf-8")
        runner=(root/"tools"/"run_c219.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2297",runner)
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",launcher)
        self.assertIn("RUNNER_PARSE_ERROR",launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c219.ps1"',launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "219"',launcher)
        self.assertIn(
            "runs\\c218-v5f-learned-writer-7ccc565edaba498c9af8f7caea7d17a4\\summary.json",
            launcher,
        )
        self.assertIn("$failure = $null",launcher)
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )

    def test_38_scope_is_coverage_only_and_not_gate_f(self):
        m=c219.manifest()
        self.assertTrue(m["numeric_unsafe_excluded"])
        self.assertEqual(m["writer_training_steps"],0)
        self.assertEqual(m["selector_training_steps"],0)
        self.assertEqual(m["reader_training_steps"],0)
        self.assertFalse(m["gate_f_candidate"])


if __name__=="__main__":
    unittest.main(verbosity=2)
