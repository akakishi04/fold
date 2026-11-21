import ast
import re
import unittest
from dataclasses import replace
from pathlib import Path

import torch

from fold_lm.v05 import candidate_input_projection as projection
from fold_lm.v05_benchmarks import gate_e_c209_visible_only_candidate_projection as c209


def visible_rows():
    return [
        c209.c208.c207.make_case(f,u,c)[0]
        for f in c209.c208.c207.FAMILIES
        for u in range(c209.c208.c207.UNITS_PER_FAMILY)
        for c in c209.c208.c207.CONDITIONS
    ]


def view_for(family, unit=0, condition=0):
    row=c209.c208.c207.make_case(family,unit,condition)[0]
    return c209.v2.decode(c209.packet_from_record(row))


class C209Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.visible=visible_rows()
        cls.records,cls.family,cls.semantic,cls.summary=c209.collect(cls.visible)

    def test_01_manifest_hash(self):
        self.assertEqual(c209.digest(c209.manifest()),c209.MANIFEST_SHA)

    def test_02_projection_schema_and_scope(self):
        m=c209.manifest()
        self.assertEqual(m["projection_schema"],projection.SCHEMA)
        self.assertEqual(m["model_forward_calls"],0)
        self.assertFalse(m["scorer_used"])
        self.assertFalse(m["baseline_measurement"])

    def test_03_one_fact_projection_reaches_seven_nodes_four_facts(self):
        p=projection.project(view_for("sufficient_known"))
        v=c209.v1.decode(p.packet)
        self.assertEqual((len(v.nodes),len(v.facts)),(7,4))
        self.assertEqual(p.original_fact_count,1)
        self.assertEqual(p.dummy_fact_indices,(1,2,3))

    def test_04_two_fact_projection_reaches_seven_nodes_four_facts(self):
        p=projection.project(view_for("answer_critical_hidden"))
        v=c209.v1.decode(p.packet)
        self.assertEqual((len(v.nodes),len(v.facts)),(7,4))
        self.assertEqual(p.original_fact_count,2)
        self.assertEqual(p.dummy_fact_indices,(2,3))

    def test_05_four_fact_projection_adds_no_dummy(self):
        p=projection.project(view_for("sufficient_reasoning_hard"))
        self.assertEqual(p.original_fact_count,4)
        self.assertEqual(p.dummy_fact_indices,())
        self.assertEqual(p.normalized_status_changes,0)

    def test_06_original_fact_indices_and_ids_are_preserved(self):
        source=view_for("answer_critical_hidden")
        p=projection.project(source)
        v=c209.v1.decode(p.packet)
        self.assertEqual(p.projected_to_original,(0,1,-1,-1))
        self.assertEqual(
            tuple(f.fact_id for f in v.facts[:2]),
            tuple(f.fact_id for f in source.base.facts),
        )

    def test_07_observed_original_fact_is_preserved_exactly(self):
        source=view_for("answer_critical_hidden")
        p=projection.project(source)
        v=c209.v1.decode(p.packet)
        self.assertEqual(v.facts[0],source.base.facts[0])

    def test_08_conflict_is_normalized_only_in_projection(self):
        source=view_for("conflicting_evidence")
        before=source.base.facts[1]
        p=projection.project(source)
        v=c209.v1.decode(p.packet)
        self.assertEqual(before.status,"CONFLICT")
        self.assertEqual(len(before.reference_ids),2)
        self.assertEqual(v.facts[1].status,"UNOBSERVED")
        self.assertIsNone(v.facts[1].value)
        self.assertEqual(v.facts[1].reference_ids,())
        self.assertEqual(source.base.facts[1],before)
        self.assertEqual(p.normalized_status_changes,1)

    def test_09_stale_is_normalized_only_in_projection(self):
        source=view_for("stale_evidence")
        p=projection.project(source)
        v=c209.v1.decode(p.packet)
        self.assertEqual(source.base.facts[1].status,"STALE")
        self.assertEqual(v.facts[1].status,"UNOBSERVED")
        self.assertEqual(p.normalized_status_changes,1)

    def test_10_dummy_facts_are_observed_true_constants(self):
        p=projection.project(view_for("sufficient_known"))
        v=c209.v1.decode(p.packet)
        for i in p.dummy_fact_indices:
            self.assertEqual(v.facts[i].status,"OBSERVED")
            self.assertEqual(v.facts[i].value,1)
            self.assertEqual(v.facts[i].fact_id,f"{projection.DUMMY_PREFIX}{i}")

    def test_11_dummy_facts_are_not_target_missing(self):
        p=projection.project(view_for("answer_critical_hidden"))
        raw=torch.tensor([p.packet.features],dtype=torch.int32)
        missing=c209.c188.missing_mask(raw)
        self.assertFalse(any(bool(missing[0,i].item()) for i in p.dummy_fact_indices))

    def test_12_projection_passes_c178_and_c188_contracts(self):
        for family in ("sufficient_known","answer_critical_hidden","conflicting_evidence","sufficient_reasoning_hard"):
            p=projection.project(view_for(family))
            raw=torch.tensor([p.packet.features],dtype=torch.int32)
            c209.c178.prepare_pair(raw)
            c209.c188.missing_mask(raw)
            c209.c188.leaf_positions(raw)

    def test_13_projection_preserves_source_digest_and_packet(self):
        source=view_for("user_only_information")
        before=c209.v2.encode(source)
        before_sha=projection.source_digest(source)
        p=projection.project(source)
        self.assertEqual(p.source_v2_sha256,before_sha)
        self.assertEqual(c209.v2.encode(source),before)
        self.assertEqual(projection.source_digest(source),before_sha)

    def test_14_projection_exhaustively_preserves_one_fact_semantics(self):
        row=c209.c208.c207.make_case("sufficient_known",0,0)[0]
        rec=c209.analyze_record(row)
        self.assertEqual((rec["semantic_checks"],rec["semantic_errors"]),(2,0))

    def test_15_projection_exhaustively_preserves_two_fact_semantics(self):
        row=c209.c208.c207.make_case("answer_critical_hidden",0,0)[0]
        rec=c209.analyze_record(row)
        self.assertEqual((rec["semantic_checks"],rec["semantic_errors"]),(4,0))

    def test_16_projection_exhaustively_preserves_four_fact_semantics(self):
        row=c209.c208.c207.make_case("sufficient_reasoning_hard",0,0)[0]
        rec=c209.analyze_record(row)
        self.assertEqual((rec["semantic_checks"],rec["semantic_errors"]),(16,0))

    def test_17_full_fixture_gate_passes(self):
        self.assertTrue(c209.gate(self.summary))

    def test_18_full_fixture_registered_totals(self):
        self.assertEqual(self.summary["original_fact_counts"],{"1":16,"2":112,"4":16})
        self.assertEqual(self.summary["dummy_facts_total"],272)
        self.assertEqual(self.summary["normalized_status_changes"],32)
        self.assertEqual(self.summary["semantic_assignments"],736)
        self.assertEqual(self.summary["semantic_errors"],0)

    def test_19_full_fixture_all_144_are_contract_compatible(self):
        self.assertEqual(self.summary["necessity_compatible"],144)
        self.assertEqual(self.summary["target_compatible"],144)
        self.assertEqual(self.summary["combined_compatible"],144)
        self.assertEqual(self.summary["dummy_missing_errors"],0)

    def test_20_equal_visible_pairs_remain_equal_after_projection(self):
        self.assertEqual(self.summary["equal_source_units"],50)
        self.assertEqual(self.summary["equal_projected_units"],50)
        self.assertEqual(self.summary["pair_projection_errors"],0)

    def test_21_projection_api_rejects_wrong_type(self):
        with self.assertRaises(TypeError):
            projection.project(object())
        with self.assertRaises(TypeError):
            projection.source_digest(object())

    def test_22_regression_suite_semantic_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=c209.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids=[t.id() for t in c209.c205._iter_tests(loaded)]
        self.assertEqual((len(names),len(all_ids)),(94,1974))
        suite=c209.regression_suite(root)
        kept=[t.id() for t in c209.c205._iter_tests(suite)]
        self.assertEqual(len(kept),1973)
        for excluded in c209.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded),1)
            self.assertNotIn(excluded,kept)

    def test_23_python_alias_bindings_are_complete(self):
        root=Path(__file__).resolve().parents[1]
        for path in (
            root/"fold_lm"/"v05"/"candidate_input_projection.py",
            root/"fold_lm"/"v05_benchmarks"/"gate_e_c209_visible_only_candidate_projection.py",
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

    def test_24_powershell_guards_are_static_and_parse_runner(self):
        root=Path(__file__).resolve().parents[1]
        launcher=(root/"tools"/"invoke_c209.ps1").read_text(encoding="utf-8")
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",launcher)
        self.assertIn("RUNNER_PARSE_ERROR",launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c209.ps1"',launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "209"',launcher)
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )
        self.assertNotIn("C209 ACTIVE / NOT YET JUDGED",launcher)


if __name__=="__main__":
    unittest.main(verbosity=2)
