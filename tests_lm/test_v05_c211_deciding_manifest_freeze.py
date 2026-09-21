import ast
import math
import re
import unittest
from pathlib import Path

from fold_lm.v05_benchmarks import gate_e_c211_deciding_manifest_freeze as c211


class C211Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.visible,cls.scorer,cls.units=c211.generate_holdout()
        cls.dev_visible=c211.c210.c209.c208.c207.collect()[0]
        cls.summary=c211.validate_holdout(
            cls.visible,cls.scorer,cls.units,cls.dev_visible
        )
        cls.visible_by={x["case_id"]:x for x in cls.visible}
        cls.scorer_by={x["case_id"]:x for x in cls.scorer}
        cls.units_by={x["unit_id"]:x for x in cls.units}

    def test_01_manifest_hash(self):
        self.assertEqual(c211.digest(c211.manifest()),c211.MANIFEST_SHA)

    def test_02_candidate_identity_is_fully_pinned(self):
        c=c211.decision_rules()["candidate"]
        self.assertEqual(c["policy_id"],"CANDIDATE-181001-188001")
        self.assertEqual(c["base_seed"],181001)
        self.assertEqual(c["head_seed"],188001)
        self.assertEqual(
            c211.PARENT_C210_EXECUTION,
            "002543b8d1394c127b915b3bfe4591ce20c8939d",
        )
        self.assertEqual(
            c211.PARENT_C210_SHA,
            "1b4242f15fdf3ca48374660d5c3339ff5c17dc9cd4f4833852f5e1bccb349366",
        )
        self.assertEqual(
            c["candidate_policy_blob"],
            "309e1a54a00ef828cea29f705e69d9a56df899d9",
        )
        self.assertEqual(
            c["base_checkpoint_sha256"],
            "3f1bad426640c58ad8479a226cb2292991e014ec88bfbc0931a538e0f81e8289",
        )
        self.assertEqual(
            c["selector_checkpoint_sha256"],
            "02547ed98ce155f6c260b5dbdf8fe5e2bb7dc4ce40248c77d511ab8089e6178d",
        )

    def test_03_numerical_margins_and_multiplicity_are_frozen(self):
        r=c211.decision_rules()
        self.assertEqual(r["fixed_noninferiority"]["margin_episodes"],0)
        self.assertEqual(r["internal_improvement"]["minimum_margin_episodes"],1)
        self.assertEqual(r["internal_improvement"]["familywise_alpha"],0.05)
        self.assertEqual(r["internal_improvement"]["holm_thresholds"],[0.025,0.05])
        self.assertEqual(r["coverage"]["noninferiority_margin_episodes"],0)

    def test_04_unsupported_assertion_floor_is_explicit(self):
        floor=c211.decision_rules()["unsupported_assertion_floor"]
        self.assertEqual(floor["candidate_post_guard_required"],0)
        self.assertEqual(floor["internal_post_guard_development"],0)
        self.assertEqual(
            floor["strict_reduction_claim"],
            "NOT_DEMONSTRATED_ZERO_FLOOR",
        )

    def test_05_holdout_shape_is_fixed(self):
        self.assertEqual(
            (len(self.visible),len(self.scorer),len(self.units)),
            (144,144,72),
        )

    def test_06_family_counts_are_balanced(self):
        self.assertEqual(
            self.summary["family_counts"],
            {f:16 for f in c211.FAMILIES},
        )

    def test_07_fault_counts_are_fixed(self):
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

    def test_08_action_and_channel_counts_are_fixed(self):
        self.assertEqual(
            self.summary["action_counts"],
            {"ANSWER":48,"RETRIEVE":48,"OBSERVE":32,"ASK_USER":16},
        )
        self.assertEqual(
            self.summary["channel_episode_counts"],
            {"RETRIEVE":64,"OBSERVE":32,"ASK_USER":16},
        )
        self.assertEqual(self.summary["answerable_with_budget"],128)

    def test_09_expression_signatures_are_independent_of_development(self):
        self.assertGreater(self.summary["development_expression_signatures"],0)
        self.assertGreater(self.summary["holdout_expression_signatures"],0)
        self.assertEqual(self.summary["expression_signature_overlap"],0)

    def test_10_case_and_unit_identities_are_disjoint(self):
        self.assertEqual(self.summary["development_unit_overlap"],0)
        self.assertEqual(self.summary["development_case_overlap"],0)

    def test_11_sufficient_known_uses_unseen_leaf_negation(self):
        row=self.visible_by["H-sufficient_known-u00-c0"]
        view=c211._view_from_visible(row)
        self.assertEqual(len(view.base.nodes),1)
        self.assertEqual(view.base.nodes[0].kind,"FACT")
        self.assertEqual(int(view.base.nodes[0].negate),1)

    def test_12_answer_critical_pair_is_visible_identical_and_semantically_split(self):
        u=self.units_by["H-answer_critical_hidden-u00"]
        v0,v1=(self.visible_by[x] for x in u["cases"])
        s0,s1=(self.scorer_by[x] for x in u["cases"])
        self.assertEqual(v0["packet"],v1["packet"])
        self.assertEqual((s0["source_value"],s1["source_value"]),(0,1))
        self.assertNotEqual(s0["semantic_conclusion"],s1["semantic_conclusion"])
        self.assertEqual(s0["necessary_fact_indices"],[1])

    def test_13_irrelevant_pair_is_visible_identical_and_same_conclusion(self):
        u=self.units_by["H-conclusion_irrelevant_missing-u00"]
        v0,v1=(self.visible_by[x] for x in u["cases"])
        s0,s1=(self.scorer_by[x] for x in u["cases"])
        self.assertEqual(v0["packet"],v1["packet"])
        self.assertEqual((s0["source_value"],s1["source_value"]),(0,1))
        self.assertEqual(s0["semantic_conclusion"],s1["semantic_conclusion"])
        self.assertEqual(s0["unnecessary_fact_indices"],[1])

    def test_14_conflict_and_stale_preserve_runtime_status(self):
        conflict=c211._view_from_visible(
            self.visible_by["H-conflicting_evidence-u00-c0"]
        )
        stale=c211._view_from_visible(
            self.visible_by["H-stale_evidence-u00-c0"]
        )
        self.assertEqual(conflict.base.facts[1].status,"CONFLICT")
        self.assertEqual(len(conflict.base.facts[1].reference_ids),2)
        self.assertEqual(stale.base.facts[1].status,"STALE")
        self.assertEqual(len(stale.base.facts[1].reference_ids),1)

    def test_15_malformed_pair_is_visible_identical(self):
        u=self.units_by["H-noisy_malformed_evidence-u00"]
        v0,v1=(self.visible_by[x] for x in u["cases"])
        s0,s1=(self.scorer_by[x] for x in u["cases"])
        self.assertEqual(v0["packet"],v1["packet"])
        self.assertEqual((s0["fault"],s1["fault"]),("NONE","MALFORMED_PAYLOAD"))
        self.assertEqual(
            (s0["answerable_with_budget"],s1["answerable_with_budget"]),
            (True,False),
        )

    def test_16_unavailable_permission_and_budget_are_visible_runtime_state(self):
        p=self.visible_by["H-unavailable_acquisition-u00-c1"]
        b=self.visible_by["H-unavailable_acquisition-u01-c1"]
        pv=c211._view_from_visible(p)
        bv=c211._view_from_visible(b)
        self.assertEqual(self.scorer_by[p["case_id"]]["fault"],"PERMISSION_DENIED")
        self.assertEqual(pv.base.resources.permitted,(False,False,False))
        self.assertEqual(self.scorer_by[b["case_id"]]["fault"],"BUDGET_EXHAUSTED")
        self.assertEqual(bv.base.resources.acquisitions_remaining,0)

    def test_17_missing_delivery_pair_remains_visible_identical(self):
        u=self.units_by["H-unavailable_acquisition-u02"]
        v0,v1=(self.visible_by[x] for x in u["cases"])
        s1=self.scorer_by[u["cases"][1]]
        self.assertEqual(s1["fault"],"MISSING_DELIVERY")
        self.assertEqual(v0["packet"],v1["packet"])

    def test_18_reasoning_hard_has_unseen_negated_structures(self):
        for unit in (0,1):
            row=self.visible_by[f"H-sufficient_reasoning_hard-u{unit:02d}-c0"]
            view=c211._view_from_visible(row)
            self.assertEqual((len(view.base.facts),len(view.base.nodes)),(4,7))
            self.assertTrue(any(bool(n.negate) for n in view.base.nodes if n.kind=="FACT"))

    def test_19_pair_and_payload_controls_pass(self):
        self.assertEqual(self.summary["equal_visible_units"],50)
        self.assertEqual(self.summary["pair_errors"],0)
        self.assertEqual(self.summary["hidden_payload_errors"],0)

    def test_20_no_holdout_policy_or_model_evaluation_occurs(self):
        self.assertFalse(self.summary["holdout_evaluated"])
        self.assertEqual(self.summary["policy_calls"],0)
        self.assertEqual(self.summary["model_forward_calls"],0)
        m=c211.manifest()
        self.assertFalse(m["holdout_evaluated"])
        self.assertEqual(m["model_forward_calls"],0)
        self.assertEqual(m["baseline_policy_calls"],0)

    def test_21_mcnemar_exact_tail(self):
        out=c211.one_sided_mcnemar([1]*80,[0]*80)
        self.assertEqual((out["better"],out["worse"],out["discordant"]),(80,0,80))
        self.assertEqual(out["p_one_sided"],1/(2**80))

    def test_22_mcnemar_tie_has_p_one(self):
        out=c211.one_sided_mcnemar([1,0,1,0],[1,0,1,0])
        self.assertEqual(out["discordant"],0)
        self.assertEqual(out["p_one_sided"],1.0)

    def test_23_holm_two_claim_rule(self):
        out=c211.holm_two({"a":0.01,"b":0.04})
        self.assertTrue(out["decisions"]["a"])
        self.assertTrue(out["decisions"]["b"])
        self.assertTrue(out["all_pass"])
        fail=c211.holm_two({"a":0.03,"b":0.031})
        self.assertFalse(fail["all_pass"])

    def test_24_candidate_tie_break_uses_exact_full_summaries(self):
        source=__import__("inspect").getsource(c211.freeze_candidate)
        self.assertIn('p210["policy_summary"][x]==first_policy',source)
        self.assertIn('p210["family_summary"][x]==first_family',source)
        self.assertIn("selected=min(candidate_ids)",source)

    def test_25_gate_accepts_frozen_registration_fixture(self):
        self.assertTrue(
            c211.gate(
                self.summary,
                c211.decision_rules()["candidate"],
                c211.decision_rules(),
            )
        )

    def test_26_regression_suite_semantic_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=c211.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids=[t.id() for t in c211.c205._iter_tests(loaded)]
        self.assertEqual((len(names),len(all_ids)),(96,2026))
        suite=c211.regression_suite(root)
        kept=[t.id() for t in c211.c205._iter_tests(suite)]
        self.assertEqual(len(kept),2025)
        for excluded in c211.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded),1)
            self.assertNotIn(excluded,kept)

    def test_27_python_alias_bindings_are_complete(self):
        root=Path(__file__).resolve().parents[1]
        for path in (
            root/"fold_lm"/"v05_benchmarks"/"gate_e_c211_deciding_manifest_freeze.py",
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

    def test_28_powershell_guards_are_static_and_parse_runner(self):
        root=Path(__file__).resolve().parents[1]
        launcher=(root/"tools"/"invoke_c211.ps1").read_text(encoding="utf-8")
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",launcher)
        self.assertIn("RUNNER_PARSE_ERROR",launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c211.ps1"',launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "211"',launcher)
        self.assertIn(
            "runs\\c210-v5e-baseline-development-ed5d0ad0a17d41b9a576fc41683005cd\\summary.json",
            launcher,
        )
        self.assertNotIn(
            "c210-v5e-baseline-development-4dc4cf58d73b4621a7d7b6b96edc4fc6",
            launcher,
        )
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )
        self.assertNotIn("C211 ACTIVE / NOT YET JUDGED",launcher)


if __name__=="__main__":
    unittest.main(verbosity=2)
