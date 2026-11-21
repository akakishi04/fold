import ast
import inspect
import re
import unittest
from dataclasses import fields
from pathlib import Path

from fold_lm.v05 import memory_bank as bankmod
from fold_lm.v05 import memory_bridge as memory
from fold_lm.v05_benchmarks import gate_f_c215_h1_h2_chunk_commit as c215


class C215Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state,cls.trace,cls.snapshots,cls.commits,cls.controls,cls.summary=c215.collect_fixture()
        cls.by_label={x["label"]:x for x in cls.snapshots}
        cls.trace_by={x["label"]:x for x in cls.trace}

    def test_01_manifest_hash(self):
        self.assertEqual(c215.digest(c215.manifest()),c215.MANIFEST_SHA)

    def test_02_parent_c214_identity_is_exact(self):
        self.assertEqual(
            (c215.PARENT_C214_EXECUTION,c215.PARENT_C214_SHA),
            (
                "b4a020aeb006ec758e06ce1dc6d1b0ad5784e150",
                "bd7a310fc89873b4571d1748a96fa1a121d147a0617d48e2d8824d4769deb37d",
            ),
        )
        self.assertEqual(
            c215.PARENT_C214_VALIDATION_SHA,
            "974546ca0e93bd0b936a68cdfcc9068bbdf6d8a53be9c7f2e8c6edafc50b543f",
        )

    def test_03_bank_schema_is_fixed(self):
        self.assertEqual(bankmod.SCHEMA,"fold-v5f-h1-h2-bank-v1")

    def test_04_initial_read_is_h2_supported(self):
        row=self.by_label["initial"]
        self.assertEqual(row["status"],"SUPPORTED")
        self.assertEqual(row["storage_epoch"],0)
        self.assertEqual(row["h2_factor_ids"],[])
        self.assertEqual(row["hot_observed_factor_ids"],[])

    def test_05_assert_enters_h1_and_requires_hot_read(self):
        row=self.by_label["after_assert_alpha"]
        self.assertEqual(row["status"],"HOT_REQUIRED")
        self.assertEqual(row["hot_observed_factor_ids"],["alpha"])
        self.assertEqual(row["h2_factor_ids"],[])

    def test_06_first_commit_is_representation_only(self):
        row=self.commits[0]
        self.assertEqual(row["status"],"COMMITTED")
        self.assertTrue(row["semantic_clocks_unchanged"])
        self.assertEqual((row["before_storage_epoch"],row["after_storage_epoch"]),(0,1))

    def test_07_first_commit_readout_is_identical(self):
        self.assertEqual(self.commits[0]["readout_delta"],0.0)
        self.assertEqual(
            self.by_label["after_assert_alpha"]["value"],
            self.by_label["after_commit_alpha"]["value"],
        )

    def test_08_replace_committed_factor_updates_h2_without_new_commit(self):
        before=self.by_label["after_commit_alpha"]
        after=self.by_label["after_replace_alpha"]
        self.assertEqual(after["status"],"SUPPORTED")
        self.assertEqual(after["h2_factor_ids"],["alpha"])
        self.assertEqual(after["hot_observed_factor_ids"],[])
        self.assertEqual(after["storage_epoch"],before["storage_epoch"])
        self.assertNotEqual(after["value"],before["value"])

    def test_09_second_assert_returns_to_hot_required(self):
        row=self.by_label["after_assert_beta"]
        self.assertEqual(row["status"],"HOT_REQUIRED")
        self.assertEqual(row["h2_factor_ids"],["alpha"])
        self.assertEqual(row["hot_observed_factor_ids"],["beta"])

    def test_10_second_commit_moves_beta_into_h2_without_semantic_change(self):
        row=self.commits[1]
        self.assertEqual(row["status"],"COMMITTED")
        self.assertTrue(row["semantic_clocks_unchanged"])
        self.assertEqual((row["before_storage_epoch"],row["after_storage_epoch"]),(1,2))
        self.assertEqual(row["readout_delta"],0.0)
        snap=self.by_label["after_commit_beta"]
        self.assertEqual(snap["h2_factor_ids"],["alpha","beta"])
        self.assertEqual(snap["hot_observed_factor_ids"],[])

    def test_11_retract_committed_factor_removes_h2_contribution_without_commit(self):
        before=self.by_label["after_commit_beta"]
        after=self.by_label["after_retract_alpha"]
        self.assertEqual(after["h2_factor_ids"],["beta"])
        self.assertEqual(after["storage_epoch"],before["storage_epoch"])
        self.assertNotEqual(after["value"],before["value"])

    def test_12_assumption_is_hot_hypothesis_but_numeric_status_stays_supported(self):
        row=self.by_label["after_assume_temp"]
        self.assertEqual(row["status"],"SUPPORTED")
        self.assertEqual(row["hot_observed_factor_ids"],[])
        self.assertEqual(row["hot_hypothesis_factor_ids"],["temp"])
        self.assertEqual(
            row["value"],
            self.by_label["after_retract_alpha"]["value"],
        )

    def test_13_end_scope_removes_hypothesis_without_numeric_change(self):
        row=self.by_label["after_end_sandbox"]
        self.assertEqual(row["status"],"SUPPORTED")
        self.assertEqual(row["hot_hypothesis_factor_ids"],[])
        self.assertEqual(
            row["value"],
            self.by_label["after_retract_alpha"]["value"],
        )

    def test_14_registered_status_sequence_is_exact(self):
        self.assertEqual(self.summary["status_sequence"],[
            "SUPPORTED","HOT_REQUIRED","SUPPORTED","SUPPORTED","HOT_REQUIRED",
            "SUPPORTED","SUPPORTED","SUPPORTED","SUPPORTED",
        ])
        self.assertEqual(self.summary["status_counts"],{"SUPPORTED":7,"HOT_REQUIRED":2})

    def test_15_hot_observed_count_sequence_is_exact(self):
        self.assertEqual(self.summary["hot_observed_counts"],[0,1,0,0,1,0,0,0,0])

    def test_16_h2_factor_count_sequence_is_exact(self):
        self.assertEqual(self.summary["h2_factor_counts"],[0,0,1,1,1,2,1,1,1])

    def test_17_total_observed_count_sequence_is_exact(self):
        self.assertEqual(self.summary["total_observed_counts"],[0,1,1,1,2,2,1,1,1])

    def test_18_full_reference_status_matches_all_main_snapshots(self):
        self.assertTrue(self.summary["full_statuses_match"])
        self.assertTrue(all(x["status"]==x["full_status"] for x in self.snapshots))

    def test_19_numeric_error_is_within_registered_tolerance(self):
        self.assertLessEqual(self.summary["max_abs_error"],1e-10)
        self.assertEqual(self.summary["tolerance"],1e-10)

    def test_20_final_semantic_and_storage_clocks_are_exact(self):
        self.assertEqual(
            (
                self.summary["final_memory_revision"],
                self.summary["final_evidence_revision"],
                self.summary["final_evidence_time"],
                self.summary["final_storage_epoch"],
                self.summary["final_h2_reflected_evidence_revision"],
            ),
            (6,4,3,2,4),
        )

    def test_21_final_authoritative_factor_is_beta_only(self):
        self.assertEqual(self.summary["final_h2_factor_ids"],["beta"])
        self.assertEqual(self.summary["final_hot_records"],0)
        self.assertEqual(self.summary["final_export_factor_ids"],["beta"])

    def test_22_operation_history_is_not_stored(self):
        self.assertEqual(self.summary["operation_history_entries"],0)
        self.assertEqual(bankmod.ChunkedMemoryBank.operation_history_entries(self.state),0)

    def test_23_noop_commit_does_not_create_storage_epoch(self):
        self.assertEqual(self.summary["noop_commit_status"],"NOOP")
        self.assertEqual(self.controls["noop"]["storage_epoch"],0)
        self.assertTrue(self.controls["noop"]["semantic_same"])

    def test_24_out_of_scope_hot_read_is_explicit(self):
        self.assertEqual(self.summary["out_of_scope_read_status"],"OUT_OF_SCOPE")
        self.assertFalse(self.controls["out_of_scope"]["value_exposed"])

    def test_25_out_of_scope_commit_is_rejected_without_state_change(self):
        self.assertEqual(self.summary["out_of_scope_commit_status"],"OUT_OF_SCOPE")
        self.assertTrue(self.summary["out_of_scope_commit_preserved"])
        self.assertEqual(self.controls["out_of_scope"]["storage_epoch"],0)

    def test_26_numeric_unsafe_hot_read_is_explicit(self):
        self.assertEqual(self.summary["numeric_unsafe_read_status"],"NUMERIC_UNSAFE")
        self.assertFalse(self.controls["numeric_unsafe"]["value_exposed"])

    def test_27_numeric_unsafe_commit_is_rejected_without_state_change(self):
        self.assertEqual(self.summary["numeric_unsafe_commit_status"],"NUMERIC_UNSAFE")
        self.assertTrue(self.summary["numeric_unsafe_commit_preserved"])
        self.assertEqual(self.controls["numeric_unsafe"]["storage_epoch"],0)

    def test_28_non_supported_controls_never_expose_value(self):
        self.assertEqual(self.summary["non_supported_value_exposures"],0)

    def test_29_state_schema_has_no_operation_history_field(self):
        names={x.name for x in fields(bankmod.ChunkedMemoryState)}
        names|={x.name for x in fields(bankmod.H2CapsuleState)}
        self.assertNotIn("history",names)
        self.assertNotIn("operations",names)
        self.assertNotIn("operation_history",names)

    def test_30_scope_has_no_learned_memory_policy(self):
        self.assertEqual(self.summary["learned_writer_calls"],0)
        self.assertEqual(self.summary["learned_reader_calls"],0)
        self.assertEqual(self.summary["port_selector_calls"],0)
        self.assertEqual(self.summary["coverage_classifier_calls"],0)
        self.assertEqual(self.summary["model_forward_calls"],0)
        source=inspect.getsource(c215.collect_fixture)
        self.assertNotIn("optimizer",source.lower())
        self.assertNotIn("backward(",source)

    def test_31_precheck_pins_c214_parent_validation(self):
        source=inspect.getsource(c215.precheck)
        self.assertIn("PARENT_C214_SHA",source)
        self.assertIn("PARENT_C214_VALIDATION_SHA",source)
        self.assertIn('artifact["file"]=="validation-summary.json"',source)

    def test_32_regression_suite_semantic_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=c215.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids=[t.id() for t in c215.c205._iter_tests(loaded)]
        self.assertEqual((len(names),len(all_ids)),(100,2150))
        suite=c215.regression_suite(root)
        kept=[t.id() for t in c215.c205._iter_tests(suite)]
        self.assertEqual(len(kept),2149)
        for excluded in c215.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded),1)
            self.assertNotIn(excluded,kept)

    def test_33_python_alias_bindings_are_complete(self):
        root=Path(__file__).resolve().parents[1]
        for path in (
            root/"fold_lm"/"v05"/"memory_bank.py",
            root/"fold_lm"/"v05_benchmarks"/"gate_f_c215_h1_h2_chunk_commit.py",
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

    def test_34_powershell_guards_and_parent_path(self):
        root=Path(__file__).resolve().parents[1]
        launcher=(root/"tools"/"invoke_c215.ps1").read_text(encoding="utf-8")
        runner=(root/"tools"/"run_c215.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2149",runner)
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",launcher)
        self.assertIn("RUNNER_PARSE_ERROR",launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c215.ps1"',launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "215"',launcher)
        self.assertIn(
            "runs\\c214-v5f-memory-capsule-closure-c243403ed49c4ed38d9d82cff1eef2a5\\summary.json",
            launcher,
        )
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )


if __name__=="__main__":
    unittest.main(verbosity=2)
