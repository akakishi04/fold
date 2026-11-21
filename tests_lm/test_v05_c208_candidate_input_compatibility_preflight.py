import ast
import re
import unittest
from dataclasses import replace
from pathlib import Path

from fold_lm.v05_benchmarks import gate_e_c208_candidate_input_compatibility_preflight as c208


def row_for(family, unit=0, condition=0):
    visible,_=c208.c207.make_case(family,unit,condition)
    return visible


def synthetic_stale_four_fact():
    row=row_for("sufficient_reasoning_hard",0,0)
    packet=c208.packet_from_record(row)
    typed=c208.v2.decode(packet)
    facts=list(typed.base.facts)
    facts[0]=c208.v1.Fact(
        facts[0].fact_id,"STALE",None,("stale:synthetic:A",)
    )
    base=replace(typed.base,facts=tuple(facts))
    packet2=c208.v2.encode(c208.v2.TaskView(base,typed.channels))
    return dict(
        case_id="synthetic-stale",
        unit_id="synthetic-stale-u00",
        family="synthetic",
        condition=0,
        packet={
            "schema":packet2.schema,
            "features":list(packet2.features),
            "binding":{
                "request_id":packet2.binding.request_id,
                "scope_id":packet2.binding.scope_id,
                "fact_ids":list(packet2.binding.fact_ids),
                "reference_ids":[list(x) for x in packet2.binding.reference_ids],
            },
        },
    )


class C208Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c208.digest(c208.manifest()),c208.MANIFEST_SHA)

    def test_02_manifest_has_no_forward_or_adapter(self):
        m=c208.manifest()
        self.assertEqual(m["model_forward_calls"],0)
        self.assertFalse(m["adapter_implementation"])
        self.assertFalse(m["candidate_measurement"])
        self.assertFalse(m["baseline_measurement"])

    def test_03_contract_blobs_fixed(self):
        self.assertEqual(
            c208.CONTRACT_FILES,
            {
                "fold_lm/v05_benchmarks/gate_e_c178_visible_leaf_binding.py":
                    "2ec87851f1f75533dd2225243d0c1baeda9c9a2a",
                "fold_lm/v05_benchmarks/gate_e_c188_multimissing_target_selection.py":
                    "0819bc70377a949fe1c17a66be559336bbda96e1",
            },
        )

    def test_04_reasoning_hard_is_as_is_compatible(self):
        r=c208.analyze_record(row_for("sufficient_reasoning_hard"))
        self.assertTrue(r["necessity_compatible"])
        self.assertTrue(r["target_compatible"])
        self.assertTrue(r["combined_compatible"])
        self.assertEqual((r["active_fact_slots"],r["active_fact_leaves"]),(4,4))

    def test_05_answer_critical_binary_is_shape_incompatible(self):
        r=c208.analyze_record(row_for("answer_critical_hidden"))
        self.assertFalse(r["header_7_nodes_4_facts"])
        self.assertFalse(r["necessity_compatible"])
        self.assertFalse(r["target_compatible"])
        self.assertFalse(r["combined_compatible"])

    def test_06_sufficient_known_is_shape_incompatible(self):
        r=c208.analyze_record(row_for("sufficient_known"))
        self.assertEqual(r["active_fact_slots"],1)
        self.assertFalse(r["combined_compatible"])

    def test_07_conflict_marks_target_status_incompatible(self):
        r=c208.analyze_record(row_for("conflicting_evidence"))
        self.assertFalse(r["target_status_compatible"])
        self.assertFalse(r["target_compatible"])

    def test_08_stale_marks_target_status_incompatible(self):
        r=c208.analyze_record(row_for("stale_evidence"))
        self.assertFalse(r["target_status_compatible"])
        self.assertFalse(r["target_compatible"])

    def test_09_four_fact_stale_is_necessity_but_not_target_compatible(self):
        r=c208.analyze_record(synthetic_stale_four_fact())
        self.assertTrue(r["header_7_nodes_4_facts"])
        self.assertTrue(r["necessity_compatible"])
        self.assertFalse(r["target_status_compatible"])
        self.assertFalse(r["target_compatible"])
        self.assertFalse(r["combined_compatible"])

    def test_10_packet_roundtrip_is_exact(self):
        row=row_for("user_only_information")
        packet=c208.packet_from_record(row)
        self.assertEqual(c208.v2.encode(c208.v2.decode(packet)),packet)

    def test_11_collect_classifies_all_rows(self):
        visible=[
            c208.c207.make_case(f,u,c)[0]
            for f in c208.c207.FAMILIES
            for u in range(c208.c207.UNITS_PER_FAMILY)
            for c in c208.c207.CONDITIONS
        ]
        records,family,_,summary=c208.collect(visible)
        self.assertEqual((len(records),len(family),summary["classified_rows"]),(144,9,144))
        self.assertEqual(summary["unexpected_errors"],0)

    def test_12_collect_family_coverage_is_balanced(self):
        visible=[
            c208.c207.make_case(f,u,c)[0]
            for f in c208.c207.FAMILIES
            for u in range(8)
            for c in (0,1)
        ]
        _,family,_,_=c208.collect(visible)
        self.assertEqual({k:v["episodes"] for k,v in family.items()},
                         {f:16 for f in c208.c207.FAMILIES})

    def test_13_candidate_gate_requires_all_144_compatible(self):
        s=dict(
            episodes=144,families=9,classified_rows=144,unexpected_errors=0,
            combined_compatible=144,incompatible=0,model_forward_calls=0,
            adapter_used=False,scorer_used=False,
        )
        self.assertTrue(c208.candidate_gate(s))
        s["combined_compatible"]=143;s["incompatible"]=1
        self.assertFalse(c208.candidate_gate(s))

    def test_14_execution_valid_accepts_complete_scientific_negative(self):
        records=[{} for _ in range(144)]
        family={f:{"episodes":16} for f in c208.c207.FAMILIES}
        summary=dict(
            episodes=144,classified_rows=144,unexpected_errors=0,
            model_forward_calls=0,adapter_used=False,scorer_used=False,
            combined_compatible=16,incompatible=128,
        )
        self.assertTrue(c208.execution_valid(summary,records,family))

    def test_15_reason_text_is_bounded(self):
        self.assertEqual(c208._reason(ValueError("x")),"x")
        with self.assertRaises(ValueError):
            c208._reason(ValueError(""))

    def test_16_precheck_pins_parent_visible_and_contract_sources(self):
        source=__import__("inspect").getsource(c208.precheck)
        self.assertIn("p207.get(\"visible_sha256\") == VISIBLE_SHA",source)
        self.assertIn("CONTRACT_FILES.items()",source)
        self.assertIn('audit.git(root,"rev-parse","HEAD:"+rel)',source)

    def test_17_validate_result_allows_valid_complete_fail(self):
        source=__import__("inspect").getsource(c208.validate_result)
        self.assertIn("execution_valid(",source)
        self.assertIn('"PASS" if candidate_gate',source)

    def test_18_regression_suite_semantic_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=c208.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids=[t.id() for t in c208.c205._iter_tests(loaded)]
        self.assertEqual((len(names),len(all_ids)),(93,1950))
        suite=c208.regression_suite(root)
        kept=[t.id() for t in c208.c205._iter_tests(suite)]
        self.assertEqual(len(kept),1949)
        for excluded in c208.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded),1)
            self.assertNotIn(excluded,kept)

    def test_19_python_alias_bindings_are_complete(self):
        root=Path(__file__).resolve().parents[1]
        for path in (
            root/"fold_lm"/"v05_benchmarks"/"gate_e_c208_candidate_input_compatibility_preflight.py",
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

    def test_20_powershell_guards_are_static_and_parse_runner(self):
        root=Path(__file__).resolve().parents[1]
        launcher=(root/"tools"/"invoke_c208.ps1").read_text(encoding="utf-8")
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",launcher)
        self.assertIn("RUNNER_PARSE_ERROR",launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c208.ps1"',launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "208"',launcher)
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )
        self.assertNotIn("C208 ACTIVE / NOT YET JUDGED",launcher)


if __name__=="__main__":
    unittest.main(verbosity=2)
