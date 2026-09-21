import ast
import re
import unittest
from pathlib import Path

from fold_lm.v05_benchmarks import gate_e_c207_nine_family_development_manifest as c207


def decode_visible(row):
    p=row["packet"]
    packet=c207.v2.PolicyInput(
        p["schema"],
        tuple(p["features"]),
        c207.v1.Binding(
            p["binding"]["request_id"],
            p["binding"]["scope_id"],
            tuple(p["binding"]["fact_ids"]),
            tuple(tuple(x) for x in p["binding"]["reference_ids"]),
        ),
    )
    return c207.v2.decode(packet)


class C207Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.visible,cls.scorer,cls.units,cls.roundtrips=c207.collect()
        cls.summary=c207.validate_fixture(
            cls.visible,cls.scorer,cls.units,cls.roundtrips
        )
        cls.visible_by={row["case_id"]:row for row in cls.visible}
        cls.scorer_by={row["case_id"]:row for row in cls.scorer}
        cls.units_by={row["unit_id"]:row for row in cls.units}

    def test_01_manifest_hash(self):
        self.assertEqual(c207.digest(c207.manifest()),c207.MANIFEST_SHA)

    def test_02_manifest_family_scope(self):
        m=c207.manifest()
        self.assertEqual(tuple(m["families"]),c207.FAMILIES)
        self.assertEqual(
            (m["units_per_family"],m["conditions_per_unit"],m["dependence_units"],m["episodes"]),
            (8,2,72,144),
        )

    def test_03_collect_shape_and_roundtrip(self):
        self.assertEqual(
            (len(self.visible),len(self.scorer),len(self.units),self.roundtrips),
            (144,144,72,144),
        )

    def test_04_gate_accepts_registered_fixture(self):
        self.assertTrue(c207.gate(self.summary))

    def test_05_family_counts_are_balanced(self):
        self.assertEqual(
            self.summary["family_counts"],
            {family:16 for family in c207.FAMILIES},
        )

    def test_06_fault_counts_are_fixed(self):
        self.assertEqual(
            self.summary["fault_counts"],
            {
                "NONE":128,
                "MALFORMED_PAYLOAD":8,
                "MISSING_DELIVERY":2,
                "PERMISSION_DENIED":3,
                "BUDGET_EXHAUSTED":3,
            },
        )

    def test_07_action_counts_are_fixed(self):
        self.assertEqual(
            self.summary["action_counts"],
            {"ANSWER":48,"RETRIEVE":48,"OBSERVE":32,"ASK_USER":16},
        )

    def test_08_channel_episode_counts_are_fixed(self):
        self.assertEqual(
            self.summary["channel_episode_counts"],
            {"RETRIEVE":64,"OBSERVE":32,"ASK_USER":16},
        )

    def test_09_answerable_denominator_is_fixed(self):
        self.assertEqual(self.summary["answerable_with_budget"],128)

    def test_10_sufficient_known_is_observed_and_answerable(self):
        row=self.visible_by["sufficient_known-u00-c0"]
        view=decode_visible(row)
        score=self.scorer_by[row["case_id"]]
        self.assertEqual(view.base.facts[0].status,"OBSERVED")
        self.assertEqual(c207.v2.declared_channels(view,0),())
        self.assertEqual(score["expected_proposal"],"ANSWER")
        self.assertTrue(score["answerable_with_budget"])

    def test_11_answer_critical_pair_is_visible_identical_and_semantically_split(self):
        u=self.units_by["answer_critical_hidden-u00"]
        v0,v1=(self.visible_by[x] for x in u["cases"])
        s0,s1=(self.scorer_by[x] for x in u["cases"])
        self.assertEqual(v0["packet"],v1["packet"])
        self.assertEqual((s0["source_value"],s1["source_value"]),(0,1))
        self.assertNotEqual(s0["semantic_conclusion"],s1["semantic_conclusion"])
        self.assertEqual(s0["necessary_fact_indices"],[1])

    def test_12_irrelevant_pair_is_visible_identical_and_same_conclusion(self):
        u=self.units_by["conclusion_irrelevant_missing-u00"]
        v0,v1=(self.visible_by[x] for x in u["cases"])
        s0,s1=(self.scorer_by[x] for x in u["cases"])
        self.assertEqual(v0["packet"],v1["packet"])
        self.assertEqual((s0["source_value"],s1["source_value"]),(0,1))
        self.assertEqual(s0["semantic_conclusion"],s1["semantic_conclusion"])
        self.assertEqual(s0["expected_proposal"],"ANSWER")
        self.assertEqual(s0["unnecessary_fact_indices"],[1])

    def test_13_conflict_family_preserves_two_references_and_observe_channel(self):
        row=self.visible_by["conflicting_evidence-u00-c0"]
        view=decode_visible(row)
        fact=view.base.facts[1]
        self.assertEqual(fact.status,"CONFLICT")
        self.assertEqual(len(fact.reference_ids),2)
        self.assertEqual(c207.v2.declared_channels(view,1),("OBSERVE",))

    def test_14_stale_family_preserves_reference_and_observe_channel(self):
        row=self.visible_by["stale_evidence-u00-c0"]
        view=decode_visible(row)
        fact=view.base.facts[1]
        self.assertEqual(fact.status,"STALE")
        self.assertEqual(len(fact.reference_ids),1)
        self.assertEqual(c207.v2.declared_channels(view,1),("OBSERVE",))

    def test_15_malformed_pair_changes_only_scorer_fault(self):
        u=self.units_by["noisy_malformed_evidence-u00"]
        v0,v1=(self.visible_by[x] for x in u["cases"])
        s0,s1=(self.scorer_by[x] for x in u["cases"])
        self.assertEqual(v0["packet"],v1["packet"])
        self.assertEqual((s0["fault"],s1["fault"]),("NONE","MALFORMED_PAYLOAD"))
        self.assertEqual((s0["answerable_with_budget"],s1["answerable_with_budget"]),(True,False))

    def test_16_unavailable_permission_denial_is_visible_authority_state(self):
        row=self.visible_by["unavailable_acquisition-u00-c1"]
        view=decode_visible(row)
        score=self.scorer_by[row["case_id"]]
        self.assertEqual(score["fault"],"PERMISSION_DENIED")
        self.assertEqual(view.base.resources.available,(True,False,False))
        self.assertEqual(view.base.resources.permitted,(False,False,False))

    def test_17_unavailable_budget_exhaustion_is_visible_budget_state(self):
        row=self.visible_by["unavailable_acquisition-u01-c1"]
        view=decode_visible(row)
        score=self.scorer_by[row["case_id"]]
        self.assertEqual(score["fault"],"BUDGET_EXHAUSTED")
        self.assertEqual(view.base.resources.acquisitions_remaining,0)

    def test_18_missing_delivery_pair_keeps_visible_packet_equal(self):
        u=self.units_by["unavailable_acquisition-u02"]
        v0,v1=(self.visible_by[x] for x in u["cases"])
        s0,s1=(self.scorer_by[x] for x in u["cases"])
        self.assertEqual(s1["fault"],"MISSING_DELIVERY")
        self.assertEqual(v0["packet"],v1["packet"])
        self.assertNotEqual(s0["answerable_with_budget"],s1["answerable_with_budget"])

    def test_19_reasoning_hard_has_four_observed_facts_and_three_ops(self):
        row=self.visible_by["sufficient_reasoning_hard-u00-c0"]
        view=decode_visible(row)
        self.assertEqual((len(view.base.facts),len(view.base.nodes)),(4,7))
        self.assertTrue(all(f.status=="OBSERVED" for f in view.base.facts))
        self.assertEqual(sum(n.kind!="FACT" for n in view.base.nodes),3)
        self.assertTrue(all(c207.v2.declared_channels(view,i)==() for i in range(4)))

    def test_20_user_only_exposes_only_ask_user_channel(self):
        row=self.visible_by["user_only_information-u00-c0"]
        view=decode_visible(row)
        score=self.scorer_by[row["case_id"]]
        self.assertEqual(c207.v2.declared_channels(view,1),("ASK_USER",))
        self.assertEqual(view.base.resources.available,(False,False,True))
        self.assertEqual(view.base.resources.permitted,(False,False,True))
        self.assertEqual(score["expected_proposal"],"ASK_USER")

    def test_21_visible_records_have_no_scorer_fields(self):
        allowed={"case_id","unit_id","family","condition","packet"}
        forbidden={
            "source_value","semantic_conclusion","answerable_with_budget",
            "necessary_fact_indices","unnecessary_fact_indices",
            "expected_proposal","expected_terminal","fault",
        }
        for row in self.visible:
            self.assertEqual(set(row),allowed)
            self.assertTrue(forbidden.isdisjoint(row))

    def test_22_nonobserved_visible_facts_never_carry_payload(self):
        for row in self.visible:
            view=decode_visible(row)
            for fact in view.base.facts:
                if fact.status!="OBSERVED":
                    self.assertIsNone(fact.value)

    def test_23_dependence_units_are_unique_two_case_groups(self):
        ids=[u["unit_id"] for u in self.units]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertTrue(all(len(u["cases"])==2 for u in self.units))
        flattened=[case for u in self.units for case in u["cases"]]
        self.assertEqual(set(flattened),set(self.visible_by))

    def test_24_manifest_registers_development_only_no_measurement(self):
        m=c207.manifest()
        self.assertEqual(m["split"],"development")
        self.assertFalse(m["independent_holdout_created"])
        self.assertFalse(m["candidate_measurement"])
        self.assertFalse(m["baseline_measurement"])
        self.assertFalse(m["numerical_margin_registration"])

    def test_25_gate_rejects_validation_failure(self):
        bad=dict(self.summary)
        bad["failed_checks"]=1
        self.assertFalse(c207.gate(bad))

    def test_26_gate_rejects_holdout_claim(self):
        bad=dict(self.summary)
        bad["independent_holdout_created"]=True
        self.assertFalse(c207.gate(bad))

    def test_27_regression_suite_semantic_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=c207.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids=[test.id() for test in c207.c205._iter_tests(loaded)]
        self.assertEqual(len(names),92)
        self.assertEqual(len(all_ids),1930)
        for excluded in c207.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded),1)
        suite=c207.regression_suite(root)
        kept_ids=[test.id() for test in c207.c205._iter_tests(suite)]
        self.assertEqual(len(kept_ids),1929)
        self.assertFalse(any(
            x in kept_ids for x in c207.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
        ))

    def test_28_authoring_alias_and_powershell_guards(self):
        root=Path(__file__).resolve().parents[1]

        for path in (
            root/"fold_lm"/"v05_benchmarks"/"gate_e_c207_nine_family_development_manifest.py",
            Path(__file__),
        ):
            source=path.read_text(encoding="utf-8")
            tree=ast.parse(source)
            bound=set()
            for node in tree.body:
                if isinstance(node,ast.Import):
                    bound.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node,ast.ImportFrom):
                    bound.update(alias.asname or alias.name for alias in node.names)
            refs={
                node.value.id
                for node in ast.walk(tree)
                if isinstance(node,ast.Attribute)
                and isinstance(node.value,ast.Name)
                and re.fullmatch(r"c\d{3}",node.value.id)
            }
            self.assertEqual(refs-bound,set())

        launcher=(root/"tools"/"invoke_c207.ps1").read_text(encoding="utf-8")
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",launcher)
        self.assertIn("RUNNER_PARSE_ERROR",launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c207.ps1"',launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "207"',launcher)
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )
        self.assertNotIn("C207 ACTIVE / NOT YET JUDGED",launcher)


if __name__=="__main__":
    unittest.main(verbosity=2)
