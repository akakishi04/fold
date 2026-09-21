import ast
import inspect
import re
import unittest
from pathlib import Path

from fold_lm.v05_benchmarks import gate_e_c210_baseline_development_measurement as c210


def make_rows():
    visible=[]
    scorer=[]
    c207=c210.c209.c208.c207
    for family in c207.FAMILIES:
        for unit in range(c207.UNITS_PER_FAMILY):
            for condition in c207.CONDITIONS:
                v,s=c207.make_case(family,unit,condition)
                visible.append(v);scorer.append(s)
    return visible,scorer


def scored_policy(policy):
    visible,scorer=make_rows()
    rows=[]
    for v,s in zip(visible,scorer,strict=True):
        env=c210.build_environment(v,s)
        raw=policy(env)
        rows.extend(c210.attach_scores([raw],[v],[s]))
    return rows


class C210Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.visible,cls.scorer=make_rows()
        cls.internal=scored_policy(c210.internal_only_policy)
        cls.fixed=scored_policy(c210.fixed_acquisition_policy)
        cls.internal_summary=c210.summarize_policy(cls.internal)
        cls.fixed_summary=c210.summarize_policy(cls.fixed)

    def test_01_manifest_hash(self):
        self.assertEqual(c210.digest(c210.manifest()),c210.MANIFEST_SHA)

    def test_02_policy_identity_scope(self):
        self.assertEqual(len(c210.CANDIDATE_PAIRS),9)
        self.assertEqual(len(c210.POLICY_IDS),11)
        self.assertEqual(c210.POLICY_IDS[:2],(c210.POLICY_INTERNAL,c210.POLICY_FIXED))

    def test_03_shared_resolver_answers_sufficient_known(self):
        v,_=c210.c209.c208.c207.make_case("sufficient_known",0,1)
        resolved=c210.shared_resolve(c210.typed_from_record(v).base)
        self.assertTrue(resolved["resolved"])
        self.assertTrue(resolved["verified"])
        self.assertEqual(resolved["value"],1)

    def test_04_shared_resolver_keeps_critical_hidden_unresolved(self):
        v,_=c210.c209.c208.c207.make_case("answer_critical_hidden",0,0)
        resolved=c210.shared_resolve(c210.typed_from_record(v).base)
        self.assertFalse(resolved["resolved"])
        self.assertIsNone(resolved["value"])

    def test_05_internal_only_full_development_totals(self):
        s=self.internal_summary
        self.assertEqual((s["episodes"],s["correct"],s["answered"],s["unresolved"]),(144,48,48,96))
        self.assertEqual((s["acquisition_attempts"],s["provider_calls"],s["publications"],s["user_turns"]),(0,0,0,0))
        self.assertEqual(s["authority_violation"],0)

    def test_06_fixed_full_development_totals(self):
        s=self.fixed_summary
        self.assertEqual((s["episodes"],s["correct"],s["answered"],s["unresolved"]),(144,128,128,16))
        self.assertEqual((s["acquisition_attempts"],s["provider_calls"],s["publications"],s["user_turns"]),(96,90,80,16))
        self.assertEqual((s["authority_violation"],s["malformed_publication"]),(0,0))

    def test_07_fixed_answer_critical_acquires_and_answers(self):
        v,s=c210.c209.c208.c207.make_case("answer_critical_hidden",0,1)
        env=c210.build_environment(v,s)
        raw=c210.fixed_acquisition_policy(env)
        scored=c210.attach_scores([raw],[v],[s])[0]
        self.assertEqual((raw["acquisition_attempts"],raw["provider_calls"],raw["publications"]),(1,1,1))
        self.assertEqual((scored["correct"],raw["answer_value"]),(1,s["semantic_conclusion"]))

    def test_08_fixed_irrelevant_missing_does_not_acquire(self):
        v,s=c210.c209.c208.c207.make_case("conclusion_irrelevant_missing",0,1)
        raw=c210.fixed_acquisition_policy(c210.build_environment(v,s))
        self.assertEqual(raw["acquisition_attempts"],0)
        self.assertTrue(raw["answer_emitted"])

    def test_09_fixed_malformed_is_rejected_without_publication(self):
        v,s=c210.c209.c208.c207.make_case("noisy_malformed_evidence",0,1)
        raw=c210.fixed_acquisition_policy(c210.build_environment(v,s))
        self.assertEqual((raw["acquisition_attempts"],raw["provider_calls"],raw["publications"]),(1,1,0))
        self.assertEqual(raw["dispatch_reason"],"INVALID_EVIDENCE")
        self.assertFalse(raw["answer_emitted"])

    def test_10_fixed_permission_denial_never_calls_provider(self):
        v,s=c210.c209.c208.c207.make_case("unavailable_acquisition",0,1)
        self.assertEqual(s["fault"],"PERMISSION_DENIED")
        raw=c210.fixed_acquisition_policy(c210.build_environment(v,s))
        self.assertEqual((raw["acquisition_attempts"],raw["provider_calls"],raw["publications"]),(1,0,0))
        self.assertEqual(raw["transition_reason"],"PERMISSION_DENIED")

    def test_11_fixed_budget_exhaustion_never_calls_provider(self):
        v,s=c210.c209.c208.c207.make_case("unavailable_acquisition",1,1)
        self.assertEqual(s["fault"],"BUDGET_EXHAUSTED")
        raw=c210.fixed_acquisition_policy(c210.build_environment(v,s))
        self.assertEqual((raw["acquisition_attempts"],raw["provider_calls"],raw["publications"]),(1,0,0))
        self.assertEqual(raw["transition_reason"],"BUDGET_EXHAUSTED")

    def test_12_fixed_missing_delivery_calls_once_without_publication(self):
        v,s=c210.c209.c208.c207.make_case("unavailable_acquisition",2,1)
        self.assertEqual(s["fault"],"MISSING_DELIVERY")
        raw=c210.fixed_acquisition_policy(c210.build_environment(v,s))
        self.assertEqual((raw["acquisition_attempts"],raw["provider_calls"],raw["publications"]),(1,1,0))
        self.assertEqual(raw["dispatch_reason"],"MISSING_DELIVERY")

    def test_13_fixed_user_only_counts_one_user_turn(self):
        v,s=c210.c209.c208.c207.make_case("user_only_information",0,1)
        raw=c210.fixed_acquisition_policy(c210.build_environment(v,s))
        self.assertEqual((raw["channel"],raw["user_turns"],raw["publications"]),("ASK_USER",1,1))

    def test_14_candidate_policy_has_no_scorer_argument(self):
        params=tuple(inspect.signature(c210.candidate_pair_policy).parameters)
        self.assertNotIn("scorer",params)
        self.assertEqual(params,("environments","base_model","selector","base_seed","head_seed"))

    def test_15_baseline_policies_have_no_scorer_argument(self):
        self.assertNotIn("scorer",inspect.signature(c210.internal_only_policy).parameters)
        self.assertNotIn("scorer",inspect.signature(c210.fixed_acquisition_policy).parameters)

    def test_16_score_wrong_abstention_is_unanswered_only(self):
        policy=dict(
            answer_emitted=True,answer_value=0,resolver_verified=True,
            acquisition_attempts=0,target_index=None,provider_calls=0,publications=0,
        )
        scorer=dict(
            semantic_conclusion=1,answerable_with_budget=True,necessary_fact_indices=[],
            fault="NONE",
        )
        v,_=c210.c209.c208.c207.make_case("sufficient_known",0,1)
        out=c210.score_record(policy,scorer,c210.typed_from_record(v).base)
        self.assertEqual(out["wrong_answer"],1)
        self.assertEqual(out["wrong_abstention"],0)

    def test_17_guarded_unsupported_requires_unverified_emission(self):
        policy=dict(
            answer_emitted=True,answer_value=1,resolver_verified=False,
            acquisition_attempts=0,target_index=None,provider_calls=0,publications=0,
        )
        scorer=dict(
            semantic_conclusion=1,answerable_with_budget=True,necessary_fact_indices=[],
            fault="NONE",
        )
        v,_=c210.c209.c208.c207.make_case("sufficient_known",0,1)
        out=c210.score_record(policy,scorer,c210.typed_from_record(v).base)
        self.assertEqual(out["guarded_unsupported_assertion"],1)

    def test_18_measurement_complete_accepts_structural_baseline_contract(self):
        policy_summary={pid:dict(self.internal_summary) for pid in c210.POLICY_IDS}
        policy_summary[c210.POLICY_INTERNAL]=dict(self.internal_summary)
        policy_summary[c210.POLICY_FIXED]=dict(self.fixed_summary)
        for pid in c210.POLICY_IDS[2:]:
            policy_summary[pid]["guarded_unsupported_assertion"]=0
            policy_summary[pid]["authority_violation"]=0
            policy_summary[pid]["malformed_publication"]=0
        models=[
            dict(initial_rows=144,post_rows=0,inference_rows=144)
            for _ in c210.CANDIDATE_PAIRS
        ]
        self.assertTrue(c210.measurement_complete(policy_summary,models,[{}]*1584))

    def test_19_measurement_complete_rejects_fixed_baseline_drift(self):
        policy_summary={pid:dict(self.internal_summary) for pid in c210.POLICY_IDS}
        policy_summary[c210.POLICY_INTERNAL]=dict(self.internal_summary)
        policy_summary[c210.POLICY_FIXED]=dict(self.fixed_summary)
        policy_summary[c210.POLICY_FIXED]["provider_calls"]-=1
        for pid in c210.POLICY_IDS[2:]:
            policy_summary[pid]["guarded_unsupported_assertion"]=0
            policy_summary[pid]["authority_violation"]=0
            policy_summary[pid]["malformed_publication"]=0
        models=[dict(initial_rows=144,post_rows=0,inference_rows=144) for _ in c210.CANDIDATE_PAIRS]
        self.assertFalse(c210.measurement_complete(policy_summary,models,[{}]*1584))

    def test_20_precheck_pins_c209_and_scorer_identity(self):
        source=inspect.getsource(c210.precheck)
        self.assertIn('p209.get("status")=="PASS"',source)
        self.assertIn('p207.get("scorer_sha256")==SCORER_SHA',source)
        self.assertIn('"development-scorer.json"',source)
        self.assertIn('p209.get("visible_sha256")==VISIBLE_SHA',source)

    def test_21_regression_suite_semantic_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=c210.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids=[t.id() for t in c210.c205._iter_tests(loaded)]
        self.assertEqual((len(names),len(all_ids)),(95,1998))
        suite=c210.regression_suite(root)
        kept=[t.id() for t in c210.c205._iter_tests(suite)]
        self.assertEqual(len(kept),1997)
        for excluded in c210.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded),1)
            self.assertNotIn(excluded,kept)

    def test_22_python_alias_bindings_are_complete(self):
        root=Path(__file__).resolve().parents[1]
        for path in (
            root/"fold_lm"/"v05_benchmarks"/"gate_e_c210_baseline_development_measurement.py",
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

    def test_23_policy_source_does_not_read_scorer(self):
        for fn in (
            c210.internal_only_policy,c210.fixed_acquisition_policy,
            c210.candidate_pair_policy,c210._attempt,c210.shared_resolve,
        ):
            source=inspect.getsource(fn)
            self.assertNotIn("scorer_row",source)
            self.assertNotIn("semantic_conclusion",source)
            self.assertNotIn("necessary_fact_indices",source)

    def test_24_powershell_guards_are_static_and_parse_runner(self):
        root=Path(__file__).resolve().parents[1]
        launcher=(root/"tools"/"invoke_c210.ps1").read_text(encoding="utf-8")
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",launcher)
        self.assertIn("RUNNER_PARSE_ERROR",launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c210.ps1"',launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "210"',launcher)
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )
        self.assertNotIn("C210 ACTIVE / NOT YET JUDGED",launcher)


if __name__=="__main__":
    unittest.main(verbosity=2)
