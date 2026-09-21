import ast
import inspect
import re
import unittest
from pathlib import Path

from fold_lm.v05 import memory_bridge as bridge
from fold_lm.v05 import state as vstate
from fold_lm.v05_benchmarks import gate_f_c213_memory_operation_contract as c213


class C213Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state,cls.trace,cls.reads,cls.mid,cls.final,cls.summary=c213.collect_fixture()
        cls.read_by={x["label"]:x for x in cls.reads}

    def test_01_manifest_hash(self):
        self.assertEqual(c213.digest(c213.manifest()),c213.MANIFEST_SHA)

    def test_02_bridge_schema_and_operation_vocabulary(self):
        self.assertEqual(bridge.SCHEMA,"fold-v5f-memory-bridge-v1")
        self.assertEqual(
            [x.value for x in bridge.MemoryOpKind],
            ["ASSERT","RETRACT","REPLACE","ASSUME","END_SCOPE","QUERY"],
        )

    def test_03_read_status_vocabulary_is_distinct(self):
        self.assertEqual(
            [x.value for x in bridge.MemoryReadStatus],
            ["SUPPORTED","MISSING","RETRACTED","OUT_OF_SCOPE","STALE_REVISION"],
        )

    def test_04_fixture_gate_passes(self):
        self.assertTrue(c213.gate(self.summary))

    def test_05_assert_advances_memory_and_evidence_revision(self):
        row=self.trace[0]
        self.assertEqual(row["label"],"assert_alpha")
        self.assertEqual(row["before"],{
            "memory_revision":0,"evidence_revision":0,"evidence_time":0,
        })
        self.assertEqual(row["after"],{
            "memory_revision":1,"evidence_revision":1,"evidence_time":1,
        })

    def test_06_replace_preserves_factor_identity_and_updates_relation(self):
        row=self.read_by["alpha_after_replace"]
        self.assertEqual(row["status"],"SUPPORTED")
        self.assertEqual(row["factor_id"],"alpha")
        self.assertEqual(row["relation_key"],"rel-alpha-v2")
        self.assertEqual(row["provenance"]["kind"],"observed")

    def test_07_retract_is_not_missing(self):
        row=self.read_by["alpha_after_retract"]
        self.assertEqual(row["status"],"RETRACTED")
        self.assertNotEqual(row["status"],"MISSING")

    def test_08_unknown_factor_is_missing_not_out_of_scope(self):
        self.assertEqual(self.read_by["missing_gamma"]["status"],"MISSING")
        self.assertEqual(self.read_by["missing_delta"]["status"],"MISSING")

    def test_09_assumption_is_hypothesis_and_live_inside_scope(self):
        row=self.read_by["assumption_live"]
        self.assertEqual(row["status"],"SUPPORTED")
        self.assertEqual(row["relation_key"],"rel-temp-hypothesis")
        self.assertEqual(row["provenance"]["kind"],"hypothesis")

    def test_10_assumption_does_not_advance_evidence_revision(self):
        row=next(x for x in self.trace if x["label"]=="assume_temp")
        self.assertEqual(row["before"]["evidence_revision"],row["after"]["evidence_revision"])
        self.assertEqual(row["before"]["evidence_time"],row["after"]["evidence_time"])
        self.assertEqual(row["after"]["memory_revision"],row["before"]["memory_revision"]+1)

    def test_11_end_scope_does_not_advance_evidence_revision(self):
        row=next(x for x in self.trace if x["label"]=="end_sandbox")
        self.assertEqual(row["before"]["evidence_revision"],row["after"]["evidence_revision"])
        self.assertEqual(row["before"]["evidence_time"],row["after"]["evidence_time"])
        self.assertEqual(row["after"]["memory_revision"],row["before"]["memory_revision"]+1)

    def test_12_ended_scope_is_out_of_scope(self):
        row=self.read_by["ended_scope_query"]
        self.assertEqual(row["status"],"OUT_OF_SCOPE")
        self.assertNotEqual(row["status"],"MISSING")

    def test_13_stale_query_is_explicit(self):
        self.assertEqual(self.read_by["stale_query"]["status"],"STALE_REVISION")
        self.assertTrue(self.summary["stale_mutation_rejected"])

    def test_14_observed_scope_cannot_be_ended_silently(self):
        self.assertTrue(self.summary["observed_scope_end_rejected"])

    def test_15_ended_scope_cannot_accept_new_assumption(self):
        self.assertTrue(self.summary["ended_scope_mutation_rejected"])

    def test_16_hypothesis_never_exports_to_evidence_state(self):
        self.assertEqual(self.summary["hypothesis_exported"],0)
        self.assertTrue(all(
            x.provenance.kind is vstate.ProvenanceKind.OBSERVED
            for x in self.mid.evidence.observations
        ))

    def test_17_retracted_record_is_absent_from_export(self):
        self.assertEqual(len(self.final.evidence.observations),1)
        self.assertEqual(len(self.final.bindings),1)
        self.assertEqual(self.final.bindings[0].factor_id,"beta")

    def test_18_export_revision_and_time_match_observed_history(self):
        self.assertEqual(
            (self.final.evidence.revision,self.final.evidence.evidence_time),
            (4,3),
        )
        self.assertEqual(
            (self.state.evidence_revision,self.state.evidence_time),
            (4,3),
        )

    def test_19_final_memory_revision_counts_all_mutations(self):
        self.assertEqual(self.state.memory_revision,6)
        self.assertEqual(self.summary["operations"],6)
        self.assertEqual(self.summary["observed_mutations"],4)
        self.assertEqual(self.summary["hypothesis_memory_mutations"],2)

    def test_20_read_status_counts_are_registered(self):
        self.assertEqual(self.summary["read_status_counts"],{
            "SUPPORTED":3,
            "MISSING":2,
            "RETRACTED":1,
            "STALE_REVISION":1,
            "OUT_OF_SCOPE":1,
        })

    def test_21_evidence_state_rejects_hypothesis_if_forced(self):
        ref=vstate.EvidenceRef(
            "bad",
            vstate.Provenance("hyp",vstate.ProvenanceKind.HYPOTHESIS,0,0),
        )
        with self.assertRaises(ValueError):
            vstate.EvidenceState(0,0,(ref,))

    def test_22_memory_op_field_contract_rejects_invalid_shapes(self):
        with self.assertRaises(ValueError):
            bridge.MemoryOp(bridge.MemoryOpKind.ASSUME,0,bridge.GLOBAL_SCOPE,
                            factor_id="x",relation_key="r")
        with self.assertRaises(ValueError):
            bridge.MemoryOp(bridge.MemoryOpKind.QUERY,0,"s",factor_id="x",
                            relation_key="not-allowed")

    def test_23_stale_mutation_does_not_change_state(self):
        state=bridge.MemoryState()
        state,_=bridge.apply_memory_op(state,bridge.MemoryOp(
            bridge.MemoryOpKind.ASSERT,0,bridge.GLOBAL_SCOPE,
            factor_id="x",relation_key="r1",source_id="src",evidence_time=1,
        ))
        before=state
        with self.assertRaisesRegex(ValueError,"STALE_REVISION"):
            bridge.apply_memory_op(state,bridge.MemoryOp(
                bridge.MemoryOpKind.REPLACE,0,bridge.GLOBAL_SCOPE,
                factor_id="x",relation_key="r2",source_id="src2",evidence_time=2,
            ))
        self.assertIs(state,before)
        self.assertEqual(state.memory_revision,1)

    def test_24_scope_end_rejects_observed_record(self):
        state=bridge.MemoryState()
        state,_=bridge.apply_memory_op(state,bridge.MemoryOp(
            bridge.MemoryOpKind.ASSERT,0,"scope-a",
            factor_id="x",relation_key="r1",source_id="src",evidence_time=1,
        ))
        with self.assertRaisesRegex(ValueError,"observed records"):
            bridge.apply_memory_op(state,bridge.MemoryOp(
                bridge.MemoryOpKind.END_SCOPE,1,"scope-a",
            ))

    def test_25_scope_has_no_learned_or_capsule_path(self):
        self.assertEqual(self.summary["learned_writer_calls"],0)
        self.assertEqual(self.summary["learned_reader_calls"],0)
        self.assertEqual(self.summary["fold_r_capsule_calls"],0)
        self.assertEqual(self.summary["model_forward_calls"],0)
        source=inspect.getsource(c213.collect_fixture)
        self.assertNotIn("torch.",source)
        self.assertNotIn("compile_capsule",source)

    def test_26_regression_suite_semantic_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=c213.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids=[t.id() for t in c213.c205._iter_tests(loaded)]
        self.assertEqual((len(names),len(all_ids)),(98,2084))
        suite=c213.regression_suite(root)
        kept=[t.id() for t in c213.c205._iter_tests(suite)]
        self.assertEqual(len(kept),2083)
        for excluded in c213.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded),1)
            self.assertNotIn(excluded,kept)

    def test_27_python_alias_bindings_are_complete(self):
        root=Path(__file__).resolve().parents[1]
        for path in (
            root/"fold_lm"/"v05"/"memory_bridge.py",
            root/"fold_lm"/"v05_benchmarks"/"gate_f_c213_memory_operation_contract.py",
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

    def test_28_powershell_guards_and_parent_path(self):
        root=Path(__file__).resolve().parents[1]
        launcher=(root/"tools"/"invoke_c213.ps1").read_text(encoding="utf-8")
        runner=(root/"tools"/"run_c213.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2083",runner)
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",launcher)
        self.assertIn("RUNNER_PARSE_ERROR",launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c213.ps1"',launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "213"',launcher)
        self.assertIn(
            "runs\\c212-v5e-deciding-holdout-4660a8313d344cc7a7859cdd0afba186\\summary.json",
            launcher,
        )
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )


if __name__=="__main__":
    unittest.main(verbosity=2)
