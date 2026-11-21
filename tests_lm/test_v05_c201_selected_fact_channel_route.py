import inspect
import unittest

import numpy as np

from fold_lm.v05 import structured_action_channel as mapper
from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05_benchmarks import gate_e_c201_selected_fact_channel_route as c201


def fake_predictions(target=0):
    arr = np.full((2,9,9536,3), -1, dtype=np.int8)
    arr[0,:,:,0] = target
    return {"target_predictions": arr}


def one_selected(channel_index, *, fact_index=0, available=True, permitted=True, observed=False):
    av = [False,False,False]
    pe = [False,False,False]
    av[channel_index] = available
    pe[channel_index] = permitted
    resources = v1.Resources(
        internal_remaining=4,
        acquisitions_remaining=1,
        available=tuple(av),
        permitted=tuple(pe),
    )
    facts = [v1.Fact(chr(65+i)) for i in range(4)]
    if observed:
        facts[fact_index] = v1.Fact(chr(65+fact_index), "OBSERVED", 1, ("ref",))
    base = v1.TaskView(
        "C201|test", "C201",
        (
            v1.Node("FACT",0),
            v1.Node("FACT",1),
            v1.Node("AND",left=0,right=1),
            v1.Node("FACT",2),
            v1.Node("FACT",3),
            v1.Node("OR",left=3,right=4),
            v1.Node("OR",left=2,right=5),
        ),
        tuple(facts),
        resources,
    )
    specs = [v2.FactChannels((False,False,False)) for _ in range(4)]
    bits = [False,False,False]
    bits[channel_index] = True
    specs[fact_index] = v2.FactChannels(tuple(bits))
    return base, v2.TaskView(base, tuple(specs))


class C201Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c201.digest(c201.manifest()), c201.MANIFEST_SHA)

    def test_02_manifest_scope_counts(self):
        m = c201.manifest()
        self.assertEqual(
            (m["route_cases"],m["authority_cross"],m["observed_controls"],m["invalid_mapper_cases"]),
            (257472,12,3,7),
        )

    def test_03_mapper_retrieve(self):
        base, view = one_selected(0)
        p = mapper.propose_selected(view, action.RuntimeState(base), 0)
        self.assertEqual((p.action,p.fact_index),("RETRIEVE",0))

    def test_04_mapper_observe(self):
        base, view = one_selected(1)
        p = mapper.propose_selected(view, action.RuntimeState(base), 0)
        self.assertEqual((p.action,p.fact_index),("OBSERVE",0))

    def test_05_mapper_ask_user(self):
        base, view = one_selected(2)
        p = mapper.propose_selected(view, action.RuntimeState(base), 0)
        self.assertEqual((p.action,p.fact_index),("ASK_USER",0))

    def test_06_mapper_preserves_nonzero_fact_index(self):
        base, view = one_selected(2,fact_index=3)
        p = mapper.propose_selected(view, action.RuntimeState(base), 3)
        self.assertEqual((p.action,p.fact_index),("ASK_USER",3))

    def test_07_mapper_uses_current_state_digest(self):
        base, view = one_selected(0)
        state = action.RuntimeState(base)
        p = mapper.propose_selected(view,state,0)
        self.assertEqual(p.expected_state_sha256,action.state_digest(state))

    def test_08_mapper_rejects_zero_channel(self):
        base, _ = one_selected(0)
        view = v2.TaskView(base,tuple(v2.FactChannels((False,False,False)) for _ in range(4)))
        with self.assertRaises(ValueError):
            mapper.propose_selected(view,action.RuntimeState(base),0)

    def test_09_mapper_rejects_multi_channel(self):
        base, view = one_selected(0)
        specs=list(view.channels);specs[0]=v2.FactChannels((True,True,False))
        with self.assertRaises(ValueError):
            mapper.propose_selected(v2.TaskView(base,tuple(specs)),action.RuntimeState(base),0)

    def test_10_mapper_rejects_state_view_mismatch(self):
        base, view = one_selected(0)
        other=v1.TaskView(base.request_id,base.scope_id,base.nodes,base.facts,base.resources,base.evidence_time,base.revision+1)
        with self.assertRaises(ValueError):
            mapper.propose_selected(view,action.RuntimeState(other),0)

    def test_11_mapper_rejects_wrong_view_type(self):
        base, _ = one_selected(0)
        with self.assertRaises(TypeError):
            mapper.propose_selected(base,action.RuntimeState(base),0)

    def test_12_mapper_rejects_wrong_state_type(self):
        base, view = one_selected(0)
        with self.assertRaises(TypeError):
            mapper.propose_selected(view,base,0)

    def test_13_mapper_rejects_negative_target(self):
        base, view = one_selected(0)
        with self.assertRaises(ValueError):
            mapper.propose_selected(view,action.RuntimeState(base),-1)

    def test_14_mapper_rejects_high_target(self):
        base, view = one_selected(0)
        with self.assertRaises(ValueError):
            mapper.propose_selected(view,action.RuntimeState(base),4)

    def test_15_prototype_routes_cover_twelve(self):
        rows=c201.prototype_routes()
        self.assertEqual((len(rows),sum(not r["passed"] for r in rows)),(12,0))

    def test_16_learned_routes_count(self):
        rows,total,mismatch=c201.learned_target_routes(fake_predictions(0))
        self.assertEqual((len(rows),total,mismatch),(108,257472,0))

    def test_17_learned_routes_balance_channels(self):
        rows,_,_=c201.learned_target_routes(fake_predictions(2))
        totals={c:sum(r["cases"] for r in rows if r["channel"]==c) for c in v2.CHANNELS}
        self.assertEqual(totals,{"RETRIEVE":85824,"OBSERVE":85824,"ASK_USER":85824})

    def test_18_authority_cross_count_and_pass(self):
        rows=c201.authority_rows()
        self.assertEqual((len(rows),sum(not r["passed"] for r in rows)),(12,0))

    def test_19_authority_outcome_counts(self):
        rows=c201.authority_rows()
        self.assertEqual(
            (
                sum(r["result_status"]=="PENDING" for r in rows),
                sum(r["result_reason"]=="PERMISSION_DENIED" for r in rows),
                sum(r["result_reason"]=="PROVIDER_UNAVAILABLE" for r in rows),
            ),
            (3,6,3),
        )

    def test_20_mapper_does_not_prefilter_permission(self):
        rows=c201.authority_rows()
        denied=[r for r in rows if not r["permitted"]]
        self.assertTrue(all(r["proposal_action"]==r["channel"] for r in denied))

    def test_21_observed_controls(self):
        rows=c201.observed_rows()
        self.assertEqual((len(rows),sum(not r["passed"] for r in rows)),(3,0))
        self.assertTrue(all(r["result_reason"]=="ALREADY_OBSERVED" for r in rows))

    def test_22_invalid_mapper_cases(self):
        rows=c201.invalid_rows()
        self.assertEqual((len(rows),sum(r["rejected"] for r in rows)),(7,7))

    def test_23_gate_accepts_collected_summary(self):
        summary,*_=c201.collect(fake_predictions(1))
        self.assertTrue(c201.gate(summary))

    def test_24_gate_rejects_route_mismatch(self):
        summary,*_=c201.collect(fake_predictions(1))
        summary["route_mismatches"]=1
        self.assertFalse(c201.gate(summary))

    def test_25_gate_rejects_authority_failure(self):
        summary,*_=c201.collect(fake_predictions(1))
        summary["authority_failures"]=1
        self.assertFalse(c201.gate(summary))

    def test_26_gate_rejects_invalid_mapper_shortfall(self):
        summary,*_=c201.collect(fake_predictions(1))
        summary["invalid_mapper_rejected"]=6
        self.assertFalse(c201.gate(summary))

    def test_27_helper_does_not_import_acquisition_lifecycle(self):
        source=inspect.getsource(mapper)
        self.assertNotIn("structured_acquisition_lifecycle",source)

    def test_28_helper_does_not_use_visible_usable_channels(self):
        source=inspect.getsource(mapper.propose_selected)
        self.assertNotIn("visible_usable_channels",source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
