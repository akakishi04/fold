import ast
import inspect
import re
import unittest
from pathlib import Path

from fold_lm.v05_benchmarks import gate_e_c212_deciding_holdout_execution as c212


class C212Tests(unittest.TestCase):
    @staticmethod
    def _rows(policy, correct_count=80, gain_count=80, attempts=1):
        rows=[]
        for i in range(144):
            family=c212.c211.FAMILIES[i//16]
            rows.append(dict(
                policy_id=policy,
                case_id=f"H-{family}-case-{i:03d}",
                unit_id=f"H-{family}-u{i//2:03d}",
                family=family,
                condition=i%2,
                correct=int(i < correct_count),
                acquisition_gain=int(i < gain_count),
                acquisition_attempts=int(attempts if i < gain_count else 0),
                answer_emitted=bool(i < correct_count),
                resolver_verified=bool(i < correct_count),
            ))
        return rows

    @staticmethod
    def _summary(correct=80, answered=80, wrong_abstention=48, attempts=80,
                 provider_calls=80, user_turns=8):
        return dict(
            episodes=144,
            correct=correct,
            answered=answered,
            wrong_abstention=wrong_abstention,
            unnecessary_acquisition=0,
            acquisition_attempts=attempts,
            provider_calls=provider_calls,
            user_turns=user_turns,
            wrong_answer=0,
            guarded_unsupported_assertion=0,
            authority_violation=0,
            malformed_publication=0,
            invalid_target=0,
            inference_rows=224,
            inference_forward_calls=2,
            inference_cell_calls=14,
        )

    @staticmethod
    def _families(correct=8, answered=8, wrong_abstention=5, user_turns=1):
        return {
            family:dict(
                episodes=16,
                correct=correct,
                answered=answered,
                wrong_abstention=wrong_abstention,
                unnecessary_acquisition=0,
                user_turns=user_turns,
            )
            for family in c212.c211.FAMILIES
        }

    @classmethod
    def _passing_fixture(cls):
        candidate=cls._summary()
        fixed=cls._summary()
        internal=cls._summary(
            correct=48,answered=48,wrong_abstention=80,
            attempts=0,provider_calls=0,user_turns=0,
        )
        policy={
            c212.c210.POLICY_INTERNAL:internal,
            c212.c210.POLICY_FIXED:fixed,
            c212.SELECTED_POLICY:candidate,
        }
        family={
            c212.c210.POLICY_INTERNAL:cls._families(correct=5,answered=5,wrong_abstention=9,user_turns=0),
            c212.c210.POLICY_FIXED:cls._families(),
            c212.SELECTED_POLICY:cls._families(),
        }
        rows={
            c212.c210.POLICY_INTERNAL:cls._rows(c212.c210.POLICY_INTERNAL,48,0,0),
            c212.c210.POLICY_FIXED:cls._rows(c212.c210.POLICY_FIXED,80,80,1),
            c212.SELECTED_POLICY:cls._rows(c212.SELECTED_POLICY,80,80,1),
        }
        meter=dict(
            policy_id=c212.SELECTED_POLICY,
            initial_rows=144,post_rows=80,inference_rows=224,
            inference_forward_calls=2,inference_cell_calls=14,
        )
        return policy,family,rows,meter

    def test_01_manifest_hash(self):
        self.assertEqual(c212.digest(c212.manifest()),c212.MANIFEST_SHA)

    def test_02_parent_c211_identity_is_exact(self):
        self.assertEqual(
            (c212.PARENT_C211_EXECUTION,c212.PARENT_C211_SHA),
            (
                "9cedc79a02441e9cddb0efc0c8bbc7714f9112db",
                "97f5c1fde9128651ae842046e706219a50e0f34238b87d17d253e89d71279263",
            ),
        )

    def test_03_frozen_holdout_artifact_hashes_are_exact(self):
        self.assertEqual(
            c212.C211_ARTIFACT_SHA,
            {
                "holdout-visible.json":"1197f59ab6bf659929ecb7a9f42df27ea28e81586c4602f8e1eb96da17be126b",
                "holdout-scorer.json":"3975c10afc2e644f5279de4d46459d1aa250c6e7b381bb944b0b8cf6b585ff22",
                "holdout-units.json":"630d9c94b4aee67f55c3f9704ad6a508679e01450da73dd18a8935b4bac8dc34",
                "decision-rules.json":"d143f2a6b4b96c672131daf22dea5c207d42375440c7d403ee95b9782fd75bcc",
                "deciding-manifest.json":"f9356e87b210bc7d836d016a9ad7a4f841a9a651b3bb9faf9428b0415df9e6d6",
            },
        )

    def test_04_selected_candidate_identity_is_frozen(self):
        self.assertEqual(c212.SELECTED_POLICY,"CANDIDATE-181001-188001")
        self.assertEqual((c212.SELECTED_BASE_SEED,c212.SELECTED_HEAD_SEED),(181001,188001))
        self.assertEqual(
            c212.BASE_CHECKPOINT_SHA,
            "3f1bad426640c58ad8479a226cb2292991e014ec88bfbc0931a538e0f81e8289",
        )
        self.assertEqual(
            c212.SELECTOR_CHECKPOINT_SHA,
            "02547ed98ce155f6c260b5dbdf8fe5e2bb7dc4ce40248c77d511ab8089e6178d",
        )

    def test_05_manifest_forbids_post_holdout_adaptation(self):
        m=c212.manifest()
        self.assertTrue(m["holdout_execution_count"]==1)
        self.assertTrue(m["no_retraining_after_holdout"])
        self.assertTrue(m["no_candidate_change"])
        self.assertTrue(m["no_threshold_relaxation"])
        self.assertTrue(m["no_failed_family_removal"])

    def test_06_registered_policy_scope_is_three_policies(self):
        self.assertEqual(
            c212.POLICY_IDS,
            (
                c212.c210.POLICY_INTERNAL,
                c212.c210.POLICY_FIXED,
                c212.SELECTED_POLICY,
            ),
        )
        self.assertEqual(c212.manifest()["policy_episode_evaluations"],432)

    def test_07_fixed_noninferiority_passes_exact_tie(self):
        policy,family,_,_=self._passing_fixture()
        out=c212.fixed_noninferiority(
            policy[c212.SELECTED_POLICY],policy[c212.c210.POLICY_FIXED],
            family[c212.SELECTED_POLICY],family[c212.c210.POLICY_FIXED],
            c212.c211.decision_rules(),
        )
        self.assertTrue(out["all_pass"])

    def test_08_fixed_noninferiority_rejects_correct_loss(self):
        policy,family,_,_=self._passing_fixture()
        policy[c212.SELECTED_POLICY]["correct"]-=1
        out=c212.fixed_noninferiority(
            policy[c212.SELECTED_POLICY],policy[c212.c210.POLICY_FIXED],
            family[c212.SELECTED_POLICY],family[c212.c210.POLICY_FIXED],
            c212.c211.decision_rules(),
        )
        self.assertFalse(out["overall"]["correct"]["passed"])

    def test_09_fixed_noninferiority_rejects_more_user_turns(self):
        policy,family,_,_=self._passing_fixture()
        policy[c212.SELECTED_POLICY]["user_turns"]+=1
        out=c212.fixed_noninferiority(
            policy[c212.SELECTED_POLICY],policy[c212.c210.POLICY_FIXED],
            family[c212.SELECTED_POLICY],family[c212.c210.POLICY_FIXED],
            c212.c211.decision_rules(),
        )
        self.assertFalse(out["overall"]["user_turns"]["passed"])

    def test_10_fixed_per_family_failure_is_not_hidden(self):
        policy,family,_,_=self._passing_fixture()
        family[c212.SELECTED_POLICY][c212.c211.FAMILIES[0]]["wrong_abstention"]+=1
        out=c212.fixed_noninferiority(
            policy[c212.SELECTED_POLICY],policy[c212.c210.POLICY_FIXED],
            family[c212.SELECTED_POLICY],family[c212.c210.POLICY_FIXED],
            c212.c211.decision_rules(),
        )
        self.assertFalse(out["per_family"][c212.c211.FAMILIES[0]]["wrong_abstention"]["passed"])
        self.assertFalse(out["all_pass"])

    def test_11_internal_improvement_passes_strict_effects(self):
        _,_,rows,_=self._passing_fixture()
        out=c212.internal_improvement(
            rows[c212.SELECTED_POLICY],rows[c212.c210.POLICY_INTERNAL],
            c212.c211.decision_rules(),
        )
        self.assertTrue(out["all_pass"])
        self.assertGreaterEqual(
            out["claims"]["useful_correct_resolution"]["margin_episodes"],1
        )
        self.assertGreaterEqual(
            out["claims"]["positive_acquisition_gain"]["margin_episodes"],1
        )

    def test_12_internal_improvement_rejects_zero_margin(self):
        internal=self._rows(c212.c210.POLICY_INTERNAL,80,80,1)
        candidate=self._rows(c212.SELECTED_POLICY,80,80,1)
        out=c212.internal_improvement(candidate,internal,c212.c211.decision_rules())
        self.assertFalse(out["all_pass"])

    def test_13_internal_improvement_uses_exact_registered_holm(self):
        _,_,rows,_=self._passing_fixture()
        out=c212.internal_improvement(
            rows[c212.SELECTED_POLICY],rows[c212.c210.POLICY_INTERNAL],
            c212.c211.decision_rules(),
        )
        self.assertEqual(out["holm"]["thresholds"],[0.025,0.05])
        self.assertEqual(set(out["holm"]["decisions"]),{
            "useful_correct_resolution","positive_acquisition_gain",
        })

    def test_14_hard_zero_gate_accepts_zero_fixture(self):
        policy,_,rows,_=self._passing_fixture()
        out=c212.hard_zero_gate(
            policy[c212.SELECTED_POLICY],rows[c212.SELECTED_POLICY],
            c212.c211.decision_rules(),
        )
        self.assertTrue(out["all_pass"])

    def test_15_hard_zero_gate_rejects_wrong_answer(self):
        policy,_,rows,_=self._passing_fixture()
        policy[c212.SELECTED_POLICY]["wrong_answer"]=1
        out=c212.hard_zero_gate(
            policy[c212.SELECTED_POLICY],rows[c212.SELECTED_POLICY],
            c212.c211.decision_rules(),
        )
        self.assertFalse(out["all_pass"])

    def test_16_hard_runtime_rejects_acquisition_budget_violation(self):
        policy,_,rows,_=self._passing_fixture()
        rows[c212.SELECTED_POLICY][0]["acquisition_attempts"]=2
        out=c212.hard_zero_gate(
            policy[c212.SELECTED_POLICY],rows[c212.SELECTED_POLICY],
            c212.c211.decision_rules(),
        )
        self.assertEqual(out["runtime"]["acquisition_budget_violations"],1)
        self.assertFalse(out["all_pass"])

    def test_17_compute_ceiling_accepts_registered_development_shape(self):
        _,_,_,meter=self._passing_fixture()
        self.assertTrue(
            c212.compute_ceiling_gate(meter,c212.c211.decision_rules())["all_pass"]
        )

    def test_18_compute_ceiling_rejects_total_row_overrun(self):
        _,_,_,meter=self._passing_fixture()
        meter["post_rows"]=145
        meter["inference_rows"]=289
        out=c212.compute_ceiling_gate(meter,c212.c211.decision_rules())
        self.assertFalse(out["all_pass"])

    def test_19_output_floor_accepts_verified_emissions(self):
        policy,_,rows,_=self._passing_fixture()
        out=c212.output_floor_gate(
            policy[c212.SELECTED_POLICY],rows[c212.SELECTED_POLICY],
            c212.c211.decision_rules(),
        )
        self.assertTrue(out["all_pass"])
        self.assertEqual(out["strict_reduction_claim"],"NOT_DEMONSTRATED_ZERO_FLOOR")

    def test_20_output_floor_rejects_unverified_emission(self):
        policy,_,rows,_=self._passing_fixture()
        rows[c212.SELECTED_POLICY][0]["answer_emitted"]=True
        rows[c212.SELECTED_POLICY][0]["resolver_verified"]=False
        out=c212.output_floor_gate(
            policy[c212.SELECTED_POLICY],rows[c212.SELECTED_POLICY],
            c212.c211.decision_rules(),
        )
        self.assertFalse(out["all_pass"])

    def test_21_build_decision_passes_complete_fixture(self):
        policy,family,rows,meter=self._passing_fixture()
        out=c212.build_decision(policy,family,rows,meter,c212.c211.decision_rules())
        self.assertTrue(out["gate_e_passed"])
        self.assertEqual(out["formal_outcome"],"GATE_E_PASSED")

    def test_22_build_decision_returns_valid_negative_on_rule_failure(self):
        policy,family,rows,meter=self._passing_fixture()
        policy[c212.SELECTED_POLICY]["correct"]-=1
        out=c212.build_decision(policy,family,rows,meter,c212.c211.decision_rules())
        self.assertFalse(out["gate_e_passed"])
        self.assertEqual(out["formal_outcome"],"GATE_E_NOT_PASSED_VALID_NEGATIVE")

    def test_23_measurement_complete_accepts_three_by_144(self):
        policy,family,rows,meter=self._passing_fixture()
        all_rows=[]
        for pid in c212.POLICY_IDS:
            all_rows.extend(rows[pid])
        self.assertTrue(c212.measurement_complete(policy,family,all_rows,meter))

    def test_24_measurement_complete_rejects_missing_row(self):
        policy,family,rows,meter=self._passing_fixture()
        all_rows=[]
        for pid in c212.POLICY_IDS:
            all_rows.extend(rows[pid])
        self.assertFalse(c212.measurement_complete(policy,family,all_rows[:-1],meter))

    def test_25_precheck_source_requires_exact_c211_artifacts(self):
        source=inspect.getsource(c212.precheck)
        self.assertIn("C211_ARTIFACT_SHA",source)
        self.assertIn("DECIDING_MANIFEST_SHA",source)
        self.assertIn("p211.get(\"source_blobs\") == pins",source)
        self.assertIn("rules == p211[\"decision_rules\"] == c211.decision_rules()",source)

    def test_26_run_uses_frozen_holdout_and_no_training(self):
        source=inspect.getsource(c212.run)
        self.assertIn('artifact_paths["holdout-visible.json"]',source)
        self.assertIn('artifact_paths["holdout-scorer.json"]',source)
        self.assertIn("candidate_pair_policy",source)
        self.assertNotIn("optimizer",source.lower())
        self.assertNotIn("backward(",source)

    def test_27_regression_suite_semantic_counts(self):
        root=Path(__file__).resolve().parents[1]
        names=c212.regression_modules(root)
        loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
        all_ids=[t.id() for t in c212.c205._iter_tests(loaded)]
        self.assertEqual((len(names),len(all_ids)),(97,2056))
        suite=c212.regression_suite(root)
        kept=[t.id() for t in c212.c205._iter_tests(suite)]
        self.assertEqual(len(kept),2055)
        for excluded in c212.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
            self.assertEqual(all_ids.count(excluded),1)
            self.assertNotIn(excluded,kept)

    def test_28_python_alias_bindings_are_complete(self):
        root=Path(__file__).resolve().parents[1]
        for path in (
            root/"fold_lm"/"v05_benchmarks"/"gate_e_c212_deciding_holdout_execution.py",
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

    def test_29_powershell_runner_and_launcher_guards(self):
        root=Path(__file__).resolve().parents[1]
        runner=(root/"tools"/"run_c212.ps1").read_text(encoding="utf-8")
        launcher=(root/"tools"/"invoke_c212.ps1").read_text(encoding="utf-8")
        self.assertIn("expected_focused_tests = 2055",runner)
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",launcher)
        self.assertIn("RUNNER_PARSE_ERROR",launcher)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c212.ps1"',launcher)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "212"',launcher)
        self.assertLess(
            launcher.index("[System.Management.Automation.Language.Parser]::ParseFile"),
            launcher.index("$failure = $null"),
        )

    def test_30_launcher_pins_accepted_c211_summary_path(self):
        root=Path(__file__).resolve().parents[1]
        launcher=(root/"tools"/"invoke_c212.ps1").read_text(encoding="utf-8")
        self.assertIn(
            "runs\\c211-v5e-deciding-manifest-3d7891a0bb5b425db029bbf316728def\\summary.json",
            launcher,
        )
        self.assertNotIn("c211-v5e-deciding-manifest-674ab427c3504f7780ec3abc5d98645c",launcher)


if __name__=="__main__":
    unittest.main(verbosity=2)
