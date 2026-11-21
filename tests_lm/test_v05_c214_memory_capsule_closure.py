import ast
import inspect
import re
import unittest
from pathlib import Path

import torch

from fold_lm.v05 import memory_bridge as memory
from fold_lm.v05 import memory_capsule_bridge as capsule_bridge
from fold_lm.v05_benchmarks import gate_f_c214_memory_capsule_closure as c214


class C214Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state,cls.trace,cls.comparisons,cls.controls,cls.summary=c214.collect_fixture()
        cls.by_label={x["label"]:x for x in cls.comparisons}

    def test_01_manifest_hash(self):
        self.assertEqual(c214.digest(c214.manifest()),c214.MANIFEST_SHA)

    def test_02_parent_c213_identity_is_exact(self):
        self.assertEqual(
            (c214.PARENT_C213_EXECUTION,c214.PARENT_C213_SHA),
            (
                "f59f615b5d409400c9fc5247270a37960ffac197",
                "370ee39bcd32da4ce797ecfb21ce3b863013c788f6daaaf0fb9a10edac643b43",
            ),
        )
        self.assertEqual(
            c214.PARENT_C213_VALIDATION_SHA,
            "fca1e55a4da9715292523c84bb490dda7dcb75aead4cf9ad98f76fc0a867b521",
        )

    def test_03_capsule_source_identity_is_pinned(self):
        self.assertEqual(
            c214.CAPSULE_SOURCE_BLOB,
            "7f1090fe95b2e3eab3967d00c6730165e34fadfb",
        )

    def test_04_bridge_shape_contract(self):
        bridge=c214.build_bridge()
        self.assertEqual((bridge.variable_dim,bridge.update_rank,bridge.readout_dim),(4,2,2))

    def test_05_relation_registry_is_registered(self):
        bridge=c214.build_bridge()
        self.assertEqual(
            bridge.relation_keys,
            ("rel-alpha-v1","rel-alpha-v2","rel-beta-v1","rel-unsafe"),
        )

    def test_06_initial_capsule_matches_full_reference(self):
        row=self.by_label["initial"]
        self.assertEqual(row["capsule_status"],"SUPPORTED")
        self.assertEqual(row["full_status"],"SUPPORTED")
        self.assertLessEqual(row["max_abs_error"],c214.TOLERANCE)

    def test_07_assert_alpha_matches_full_reference(self):
        row=self.by_label["after_assert_alpha"]
        self.assertEqual(row["observed_factor_ids"],["alpha"])
        self.assertLessEqual(row["max_abs_error"],c214.TOLERANCE)

    def test_08_replace_alpha_preserves_factor_identity(self):
        row=self.by_label["after_replace_alpha"]
        self.assertEqual(row["observed_factor_ids"],["alpha"])
        self.assertLessEqual(row["max_abs_error"],c214.TOLERANCE)
        self.assertNotEqual(
            row["capsule_value"],
            self.by_label["after_assert_alpha"]["capsule_value"],
        )

    def test_09_assert_beta_adds_second_factor(self):
        row=self.by_label["after_assert_beta"]
        self.assertEqual(row["observed_factor_ids"],["alpha","beta"])
        self.assertLessEqual(row["max_abs_error"],c214.TOLERANCE)

    def test_10_retract_alpha_removes_its_numeric_contribution(self):
        row=self.by_label["after_retract_alpha"]
        self.assertEqual(row["observed_factor_ids"],["beta"])
        self.assertLessEqual(row["max_abs_error"],c214.TOLERANCE)

    def test_11_assumption_does_not_change_numeric_readout(self):
        before=self.by_label["after_retract_alpha"]["capsule_value"]
        after=self.by_label["after_assume_temp"]["capsule_value"]
        self.assertEqual(before,after)
        self.assertEqual(self.summary["assumption_readout_delta"],0.0)

    def test_12_end_scope_does_not_change_observed_numeric_readout(self):
        before=self.by_label["after_retract_alpha"]["capsule_value"]
        after=self.by_label["after_end_sandbox"]["capsule_value"]
        self.assertEqual(before,after)
        self.assertEqual(self.summary["end_scope_readout_delta"],0.0)

    def test_13_all_seven_registered_snapshots_are_supported(self):
        self.assertEqual(self.summary["supported_snapshots"],7)
        self.assertEqual(self.summary["supported_status_counts"],{"SUPPORTED":7})

    def test_14_max_abs_error_is_registered_float64_bound(self):
        self.assertLessEqual(self.summary["max_abs_error"],1e-10)
        self.assertEqual(self.summary["tolerance"],1e-10)

    def test_15_full_reference_status_matches_every_supported_snapshot(self):
        self.assertTrue(self.summary["all_full_reference_statuses_match"])
        self.assertTrue(all(
            row["capsule_status"]==row["full_status"]=="SUPPORTED"
            for row in self.comparisons
        ))

    def test_16_factor_count_sequence_tracks_replace_and_retract(self):
        self.assertEqual(self.summary["factor_count_sequence"],[0,1,1,2,1,1,1])

    def test_17_final_state_matches_c213_semantic_clock(self):
        self.assertEqual(
            (
                self.summary["final_memory_revision"],
                self.summary["final_evidence_revision"],
                self.summary["final_evidence_time"],
            ),
            (6,4,3),
        )

    def test_18_final_export_contains_only_beta_observation(self):
        self.assertEqual(self.summary["final_export_observations"],1)
        self.assertEqual(self.summary["final_export_factor_ids"],["beta"])

    def test_19_out_of_scope_is_not_numeric_unsafe(self):
        self.assertEqual(self.summary["out_of_scope_status"],"OUT_OF_SCOPE")
        self.assertEqual(self.summary["out_of_scope_full_status"],"OUT_OF_SCOPE")
        self.assertNotEqual(self.summary["out_of_scope_status"],"NUMERIC_UNSAFE")

    def test_20_numeric_unsafe_is_not_out_of_scope(self):
        self.assertEqual(self.summary["numeric_unsafe_status"],"NUMERIC_UNSAFE")
        self.assertEqual(self.summary["numeric_unsafe_full_status"],"NUMERIC_UNSAFE")
        self.assertNotEqual(self.summary["numeric_unsafe_status"],"OUT_OF_SCOPE")

    def test_21_non_supported_controls_expose_no_value(self):
        self.assertEqual(self.summary["non_supported_value_exposures"],0)
        self.assertFalse(self.controls["out_of_scope"]["value_exposed"])
        self.assertFalse(self.controls["numeric_unsafe"]["value_exposed"])

    def test_22_hypothesis_record_is_excluded_even_when_unmapped(self):
        bridge=c214.build_bridge()
        state=memory.MemoryState()
        state,_=memory.apply_memory_op(state,memory.MemoryOp(
            memory.MemoryOpKind.ASSUME,0,"sandbox",
            factor_id="hyp",relation_key="completely-unmapped",
        ))
        read=bridge.read(state)
        self.assertEqual(read.status,capsule_bridge.CapsuleReadStatus.SUPPORTED)
        self.assertEqual(read.observed_factor_ids,())

    def test_23_unknown_observed_relation_is_out_of_scope(self):
        bridge=c214.build_bridge()
        state=memory.MemoryState()
        state,_=memory.apply_memory_op(state,memory.MemoryOp(
            memory.MemoryOpKind.ASSERT,0,memory.GLOBAL_SCOPE,
            factor_id="x",relation_key="unknown",source_id="src",evidence_time=1,
        ))
        self.assertEqual(
            bridge.read(state).status,
            capsule_bridge.CapsuleReadStatus.OUT_OF_SCOPE,
        )

    def test_24_port_contribution_rejects_nonfinite_and_asymmetric(self):
        with self.assertRaises(ValueError):
            capsule_bridge.PortContribution(
                "bad",
                torch.tensor([[1.0,float("nan")],[float("nan"),1.0]]),
                torch.zeros(2),
            )
        with self.assertRaises(ValueError):
            capsule_bridge.PortContribution(
                "bad2",
                torch.tensor([[0.0,1.0],[0.0,0.0]]),
                torch.zeros(2),
            )

    def test_25_bridge_rejects_rank_mismatch_and_duplicate_keys(self):
        good=capsule_bridge.PortContribution("x",torch.zeros((2,2)),torch.zeros(2))
        bad=capsule_bridge.PortContribution("y",torch.zeros((3,3)),torch.zeros(3))
        J=torch.eye(4,dtype=torch.float64)
        eta=torch.zeros(4,dtype=torch.float64)
        Q=torch.zeros((2,4),dtype=torch.float64)
        U=torch.tensor([[1.,0.],[0.,1.],[0.,0.],[0.,0.]],dtype=torch.float64)
        with self.assertRaises(ValueError):
            capsule_bridge.MemoryCapsuleBridge(J,eta,Q,U,(bad,))
        with self.assertRaises(ValueError):
            capsule_bridge.MemoryCapsuleBridge(J,eta,Q,U,(good,good))

    def test_26_bridge_copies_base_tensors(self):
        J=torch.eye(4,dtype=torch.float64)*3
        eta=torch.arange(4,dtype=torch.float64)
        Q=torch.tensor([[1.,0.,0.,0.],[0.,1.,0.,0.]],dtype=torch.float64)
        U=torch.tensor([[1.,0.],[0.,1.],[0.,0.],[0.,0.]],dtype=torch.float64)
        contribution=capsule_bridge.PortContribution("x",torch.zeros((2,2)),torch.zeros(2))
        bridge=capsule_bridge.MemoryCapsuleBridge(J,eta,Q,U,(contribution,))
        state=memory.MemoryState()
        before=bridge.read(state).value.clone()
        J[0,0]=999
        eta[0]=999
        Q[0,0]=999
        U[0,0]=999
        torch.testing.assert_close(bridge.read(state).value,before,rtol=0,atol=0)

    def test_27_read_status_vocabulary_is_exact(self):
        self.assertEqual(
            [x.value for x in capsule_bridge.CapsuleReadStatus],
            ["SUPPORTED","OUT_OF_SCOPE","NUMERIC_UNSAFE"],
        )

    def test_28_no_learned_or_h1_h2_path(self):
        self.assertEqual(self.summary["learned_writer_calls"],0)
        self.assertEqual(self.summary["learned_reader_calls"],0)
        self.assertEqual(self.summary["port_selector_calls"],0)
        self.assertEqual(self.summary["model_forward_calls"],0)
        source=inspect.getsource(c214.collect_fixture)
        self.assertNotIn("optimizer",source.lower())
        self.assertNotIn("backward(",source)
        self.assertNotIn("PortSelector",source)

    def test_29_precheck_pins_c213_and_capsule_source(self):
        source=inspect.getsource(c214.precheck)
        self.assertIn("PARENT_C213_SHA",source)
        self.assertIn("PARENT_C213_VALIDATION_SHA",source)
        self.assertIn("CAPSULE_SOURCE_BLOB",source)
        self.assertIn('"fold_lm/capsule.py"',source)

    def test_30_regression_suite_semantic_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=c214.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids=[t.id() for t in c214.c205._iter_tests(loaded)]
        self.assertEqual((len(names),len(all_ids)),(99,2116))
        suite=c214.regression_suite(root)
        kept=[t.id() for t in c214.c205._iter_tests(suite)]
        self.assertEqual(len(kept),2115)
        for excluded in c214.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded),1)
            self.assertNotIn(excluded,kept)

    def test_31_python_alias_bindings_are_complete(self):
        root=Path(__file__).resolve().parents[1]
        for path in (
            root/"fold_lm"/"v05"/"memory_capsule_bridge.py",
            root/"fold_lm"/"v05_benchmarks"/"gate_f_c214_memory_capsule_closure.py",
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

    def test_32_powershell_guards_and_parent_path(self):
        root=Path(__file__).resolve().parents[1]
        launcher=(root/"tools"/"invoke_c214.ps1").read_text(encoding="utf-8")
        runner=(root/"tools"/"run_c214.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2115",runner)
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",launcher)
        self.assertIn("RUNNER_PARSE_ERROR",launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c214.ps1"',launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "214"',launcher)
        self.assertIn(
            "runs\\c213-v5f-memory-operation-contract-04a2bd0ef91b4a4998de8c1c1b6214df\\summary.json",
            launcher,
        )
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )


if __name__=="__main__":
    unittest.main(verbosity=2)
