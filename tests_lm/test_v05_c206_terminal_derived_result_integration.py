import inspect
import unittest
from pathlib import Path

import numpy as np

from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05_benchmarks import gate_e_c202_three_channel_acquisition_dispatch as c202
from fold_lm.v05_benchmarks import gate_e_c206_terminal_derived_result_integration as c206


def base_view():
    resources=v1.Resources(
        internal_remaining=13,acquisitions_remaining=4,
        available=c206.c203.PARENT_AVAILABLE,permitted=c206.c203.PARENT_PERMITTED,
        last_outcome="NONE",internal_step=7)
    nodes=(
        v1.Node("FACT",0),v1.Node("FACT",1),v1.Node("AND",left=0,right=1),
        v1.Node("FACT",2),v1.Node("FACT",3),v1.Node("OR",left=3,right=4),
        v1.Node("OR",left=2,right=5),
    )
    facts=tuple(v1.Fact(c206.c185.FACT_IDS[i]) for i in range(4))
    return v1.TaskView("C206|test|query","C206|test",nodes,facts,resources,1,1)


def world_with_fact2_one():
    return next(i for i,bits in enumerate(c206.c190.WORLD_BITS) if bits[2] == 1)


def terminal_view():
    view=base_view()
    facts=list(view.facts)
    facts[2]=v1.Fact(
        c206.c185.FACT_IDS[2],"OBSERVED",1,("C206-test:fact2",)
    )
    return v1.TaskView(
        view.request_id,view.scope_id,view.nodes,tuple(facts),view.resources,
        view.evidence_time,view.revision
    )


def trace_one():
    n=np.full((1,4),-1,dtype=np.int8)
    t=np.full((1,3),-1,dtype=np.int8)
    n[0,0]=1
    n[0,1]=0
    t[0,0]=2
    t[0,1]=0  # C199 writer semantics: terminal target head can be present but unused.
    return n,t


def expected_one():
    return dict(
        episodes=1,decisions=2,acquisitions=1,final_sufficient=1,
        channel_counts={"RETRIEVE":0,"OBSERVE":0,"ASK_USER":1},
        channel_switches=0,
    )


def good_record():
    return dict(
        episodes=9536,decisions=23888,acquisitions=14352,
        channel_counts={"RETRIEVE":9878,"OBSERVE":2362,"ASK_USER":2112},
        channel_switches=3600,terminal_sufficient=9536,
        verified_derived=9536,opposite_rejected=9536,verifier_calls=19072,
        support_total=9536,support_min=1,support_max=1,checked_steps=28608,
        failed=0,projection_error=0,
        decision_trace_error=0,target_error=0,route_error=0,action_error=0,
        dispatch_error=0,provider_channel_error=0,receipt_error=0,
        fact_update_error=0,authority_restore_error=0,resource_error=0,
        semantic_unresolved_error=0,world_value_error=0,verification_error=0,
        opposite_rejection_error=0,support_error=0,mutation_error=0,
        derived_schema_error=0,
    )


def good_totals():
    return dict(
        episodes=85824,decisions=214948,acquisitions=129124,
        terminal_sufficient=85824,verified_derived=85824,
        opposite_rejected=85824,verifier_calls=171648,
        channel_counts={"RETRIEVE":88918,"OBSERVE":21252,"ASK_USER":18954},
        channel_switches=32564,support_total=85824,
        support_min=1,support_max=4,checked_steps=257472,
        failures=0,projection_errors=0,
    )


class C206Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c206.digest(c206.manifest()),c206.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m=c206.manifest()
        self.assertEqual((m["terminal_episodes"],m["verifier_calls"]),(85824,171648))
        self.assertEqual(m["maximum_proof_steps"],7)

    def test_03_historical_c171_file_set(self):
        self.assertEqual(len(c206.C171_FILES),6)
        self.assertIn("fold_lm/v05/structured_derived_result.py",c206.C171_FILES)
        self.assertIn("fold_lm/v05_benchmarks/gate_e_c171_derived_result.py",c206.C171_FILES)

    def test_04_world_value_matches_short_circuit_completion(self):
        view=terminal_view()
        self.assertEqual(c206.world_value(view,world_with_fact2_one()),1)

    def test_05_terminal_verifies_derived(self):
        out=c206.verify_terminal(terminal_view(),world_with_fact2_one())
        self.assertEqual(out["verified_derived"],1)
        self.assertEqual(out["verification_error"],0)

    def test_06_terminal_rejects_opposite(self):
        out=c206.verify_terminal(terminal_view(),world_with_fact2_one())
        self.assertEqual(out["opposite_rejected"],1)
        self.assertEqual(out["opposite_rejection_error"],0)

    def test_07_terminal_support_is_exact_observed_reference(self):
        out=c206.verify_terminal(terminal_view(),world_with_fact2_one())
        self.assertEqual(out["support_count"],1)
        self.assertEqual(out["support_error"],0)

    def test_08_terminal_verification_is_pure(self):
        view=terminal_view()
        before=c206.blob(__import__("dataclasses").asdict(view))
        out=c206.verify_terminal(view,world_with_fact2_one())
        self.assertEqual(out["mutation_error"],0)
        self.assertEqual(c206.blob(__import__("dataclasses").asdict(view)),before)

    def test_09_terminal_detects_world_mismatch(self):
        view=terminal_view()
        code=next(i for i,bits in enumerate(c206.c190.WORLD_BITS) if bits[2] == 0)
        out=c206.verify_terminal(view,code)
        self.assertEqual(out["world_value_error"],1)

    def _integration(self):
        n,t=trace_one()
        code=world_with_fact2_one()
        providers,endpoints=c202.providers()
        rec=c206.replay_and_verify_block(
            [base_view()],np.array([code],dtype=np.int8),n,t,
            providers,endpoints,expected_one()
        )
        return code,providers,rec

    def test_10_replay_integration_passes(self):
        _,_,rec=self._integration()
        self.assertEqual((rec["failed"],rec["projection_error"]),(0,0))

    def test_11_replay_integration_terminal_contract(self):
        _,_,rec=self._integration()
        self.assertEqual(
            (rec["terminal_sufficient"],rec["verified_derived"],rec["opposite_rejected"]),
            (1,1,1)
        )

    def test_12_replay_integration_uses_ask_user_provider(self):
        code,providers,_=self._integration()
        self.assertEqual(tuple(providers[code][name].calls for name in c206.v2.CHANNELS),(0,0,1))

    def test_13_replay_integration_resource_formula(self):
        _,_,rec=self._integration()
        self.assertEqual((rec["decisions"],rec["acquisitions"]),(2,1))
        self.assertEqual(rec["resource_error"],0)

    def test_14_gate_accepts_registered_profile(self):
        records=[good_record() for _ in range(9)]
        self.assertTrue(c206.gate(records,good_totals()))

    def test_15_gate_rejects_verification_error(self):
        records=[good_record() for _ in range(9)]
        records[0]["verification_error"]=1
        records[0]["failed"]=1
        totals=good_totals();totals["failures"]=1
        self.assertFalse(c206.gate(records,totals))

    def test_16_gate_rejects_opposite_control_shortfall(self):
        records=[good_record() for _ in range(9)]
        totals=good_totals();totals["opposite_rejected"]=85823
        self.assertFalse(c206.gate(records,totals))

    def test_17_gate_rejects_zero_support(self):
        records=[good_record() for _ in range(9)]
        records[0]["support_min"]=0
        totals=good_totals();totals["support_min"]=0
        self.assertFalse(c206.gate(records,totals))

    def test_18_gate_rejects_projection_error(self):
        records=[good_record() for _ in range(9)]
        records[0]["projection_error"]=1
        totals=good_totals();totals["projection_errors"]=1
        self.assertFalse(c206.gate(records,totals))

    def test_19_gate_rejects_channel_drift(self):
        records=[good_record() for _ in range(9)]
        totals=good_totals()
        totals["channel_counts"]={"RETRIEVE":88919,"OBSERVE":21251,"ASK_USER":18954}
        self.assertFalse(c206.gate(records,totals))

    def test_20_historical_hash_helper_matches_suffix_only(self):
        fake={"input_sha256":{
            r"M:\asobiba\fold\fold_lm\v05\structured_derived_result.py":"abc",
            r"M:\asobiba\fold\other.txt":"def",
        }}
        self.assertEqual(
            c206._historical_input_hash(fake,"fold_lm/v05/structured_derived_result.py"),
            "abc",
        )

    def test_21_source_uses_benchmark_only_proof_fixture(self):
        source=inspect.getsource(c206.verify_terminal)
        self.assertIn("c171.proof_fixture",source)
        self.assertIn("c171.completion_values",source)

    def test_22_source_uses_production_verifier(self):
        source=inspect.getsource(c206.verify_terminal)
        self.assertIn("derived.verify",source)
        self.assertIn("derived.bind_candidate",source)

    def test_23_source_never_promotes_derived_to_observed(self):
        source=inspect.getsource(c206.verify_terminal)
        self.assertIn('result.derivation_kind == "BOOLEAN_LOCAL_PROOF"',source)
        self.assertIn('result.status == "OBSERVED"',source)
        self.assertNotIn('Fact(',source)

    def test_24_precheck_pins_c171_history_and_c205_parent(self):
        source=inspect.getsource(c206.precheck)
        self.assertIn("C171_FILES",source)
        self.assertIn("_historical_input_hash",source)
        self.assertIn('p205.get("status") == "PASS"',source)
        self.assertIn("p205.get(\"source_blobs\") == pins",source)

    def test_25_regression_preserves_exact_historical_exclusion(self):
        source=inspect.getsource(c206.regression_suite)
        self.assertIn("c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS",source)
        self.assertIn("ids.count(excluded) == 1",source)
        self.assertIn("len(tests) == 1900",source)
        self.assertIn("len(kept) == 1899",source)

    def test_26_scope_has_no_learning(self):
        m=c206.manifest()
        self.assertEqual(
            (m["training_steps"],m["fresh_seed_count"],m["learned_forward_calls"],m["network_calls"]),
            (0,0,0,0)
        )

    def test_27_replay_verifies_only_after_sufficient_decision(self):
        source=inspect.getsource(c206.replay_and_verify_block)
        self.assertLess(source.index("pred = int(necessity[i,phase])"),source.index("verify_terminal"))
        self.assertIn("if pred == 0:",source)
        self.assertLess(source.index("if pred == 0:"),source.index("verify_terminal"))

    def test_28_gate_requires_exact_verifier_calls(self):
        records=[good_record() for _ in range(9)]
        totals=good_totals();totals["verifier_calls"]=171647
        self.assertFalse(c206.gate(records,totals))


    def test_29_c206_launcher_parses_runner_before_logging(self):
        root=Path(__file__).resolve().parents[1]
        source=(root/"tools"/"invoke_c206.ps1").read_text(encoding="utf-8")
        self.assertIn("[System.Management.Automation.Language.Parser]::ParseFile",source)
        self.assertIn("RUNNER_PARSE_ERROR",source)
        self.assertIn('$runnerPath = Join-Path $Root "tools\\run_c206.ps1"',source)
        self.assertLess(source.index("[System.Management.Automation.Language.Parser]::ParseFile"),source.index("$failure = $null"))

    def test_30_c206_launcher_formal_state_check_is_source_static(self):
        root=Path(__file__).resolve().parents[1]
        source=(root/"tools"/"invoke_c206.ps1").read_text(encoding="utf-8")
        self.assertIn("$formalPattern = '(?ms)^## Formal state\\s+",source)
        self.assertIn('$activeMatch.Groups["id"].Value -ne "206"',source)
        self.assertNotIn("C206 ACTIVE / NOT YET JUDGED",source)


if __name__=="__main__":
    unittest.main(verbosity=2)
