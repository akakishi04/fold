import hashlib
import inspect
import unittest

import numpy as np
import torch

from fold_lm.v05 import structured_acquisition_lifecycle as life
from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
from fold_lm.v05_benchmarks import gate_e_c198_stale_reservation_generic_loop as c198


def raw_row13():
    x = np.zeros(72, dtype=np.int32)
    x[0] = 7
    x[1] = 4
    x[2] = 1
    x[3] = 1
    nodes = (
        (1,1,1,0,0,0),(1,1,2,0,0,0),(1,2,0,1,2,0),
        (1,1,3,0,0,0),(1,1,4,0,0,0),(1,3,0,4,5,0),(1,2,0,3,6,0),
    )
    x[4:46] = np.asarray(nodes, dtype=np.int32).reshape(-1)
    visible = (None, None, None, 1)
    for i, value in enumerate(visible):
        x[46+4*i:50+4*i] = (
            1,
            1 if value is None else 2,
            0 if value is None else 1,
            0 if value is None else value,
        )
    x[62:72] = (13,4,1,0,0,1,0,0,0,7)
    return x


class ShouldNotRun:
    def __init__(self):
        self.calls = 0

    def __call__(self, request):
        self.calls += 1
        raise AssertionError("stale reservation reached provider")


def endpoint(code=3):
    raw = c190.world_bytes(code)
    binding = life.SourceBinding(
        f"C190-world-{code:02d}",
        hashlib.sha256(raw).hexdigest(),
    )
    provider = ShouldNotRun()
    return life.Endpoint(binding, provider), provider


def initial_for(views, target_index=0):
    owners = [life.AcquisitionOwner(action.RuntimeState(v), {}, max_dispatches=3)
              for v in views]
    if not all(driver.charge_decision(o) for o in owners):
        raise AssertionError("charge failed")
    raw, _ = c189.encode_views([o.state.view for o in owners])
    n = len(raw)
    unknown = target.missing_mask(raw).numpy()
    target_logits = np.full((n,4), -np.inf, dtype=np.float32)
    target_logits[unknown] = 0.0
    target_logits[np.arange(n), target_index] = 1.0
    return dict(
        raw=raw,
        necessity_predictions=np.ones(n, dtype=np.int8),
        target_predictions=np.full(n, target_index, dtype=np.int8),
        necessity_logits=np.tile(np.asarray([[0.0,1.0]], dtype=np.float32), (n,1)),
        target_logits=target_logits,
    )


def good_allowed():
    out = []
    for b, h in c198.expected_order():
        first, second, third = 9536, 3900, 928
        out.append(dict(
            base_seed=b, head_seed=h, episodes=9536,
            actual_reads=first+second+third,
            failed=0, necessity_error=0, target_error=0, selected_observed=0,
            repeated_target=0, acquisition_error=0, contract_error=0,
            final_decision_error=0, reference_replay_error=0,
            reference_block_mismatch=0, first_reads=first, second_reads=second,
            third_reads=third, final_decision_rows=third,
            reference_necessity_prediction_errors=0,
            reference_target_prediction_errors=0,
            reference_necessity_max_abs_logit_difference=0.0,
            reference_target_max_abs_logit_difference=0.0,
        ))
    return out


def good_stale():
    out = []
    for b, h in c198.expected_order():
        rec = dict(
            base_seed=b, head_seed=h, episodes=9536,
            stale_attempts=9536, provider_calls=0, actual_provider_reads=0,
            publications=0, receipts=0, learned_decisions=9536, retries=0,
            initial_reference_prediction_errors=0,
            initial_reference_target_errors=0,
            initial_reference_necessity_logit_delta=0.0,
            initial_reference_target_logit_delta=0.0,
        )
        rec.update({k: 0 for k in c198.STALE_COUNTERS})
        out.append(rec)
    return out


class C198Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c198.digest(c198.manifest()), c198.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m = c198.manifest()
        self.assertEqual((m["episodes_per_arm"], m["blocks_per_arm"]), (85824, 9))
        self.assertEqual(tuple(m["arms"]), c198.ARMS)

    def test_03_outputs_exact(self):
        self.assertEqual(len(c198.OUTPUTS), 5)

    def test_04_expected_order(self):
        self.assertEqual(len(c198.expected_order()), 9)

    def _run_stale(self):
        ep, provider = endpoint(3)
        raw = torch.from_numpy(np.stack([raw_row13()]))
        views = c190.make_views(raw, np.array([0]), np.array([3]), "x")
        base = graph.SharedGraphProbe(graph.ARMS[1])
        head = target.TargetSelector()
        rec, arrays, _ = c198.run_loop_stale_aware(
            views,
            np.array([3]),
            {3: ep},
            base,
            head,
            initial_for(views, 0),
            "STALE_RESERVATION_AFTER_RESERVATION",
        )
        return provider, rec, arrays

    def test_05_integration_provider_not_called(self):
        provider, rec, _ = self._run_stale()
        self.assertEqual((provider.calls, len(rec[0]["acquisitions"])), (0, 1))

    def test_06_action_reserves_before_refresh(self):
        _, rec, _ = self._run_stale()
        a = rec[0]["acquisitions"][0]["action"]
        self.assertEqual((a["status"], a["reason"], a["acquisition_reserved"]),
                         ("PENDING", "ACQUISITION_RESERVED", 1))

    def test_07_dispatch_rejects_stale_reservation(self):
        _, rec, _ = self._run_stale()
        d = rec[0]["acquisitions"][0]["dispatch"]
        self.assertEqual((d["status"], d["reason"], d["provider_calls"]),
                         ("REJECTED", "STALE_RESERVATION", 0))

    def test_08_reason_propagates_to_loop_status(self):
        _, rec, _ = self._run_stale()
        self.assertEqual(
            rec[0]["status"],
            "UNRESOLVED_ACQUISITION_STALE_RESERVATION",
        )

    def test_09_stale_no_retry(self):
        _, rec, arrays = self._run_stale()
        self.assertEqual((rec[0]["decision_charges"], len(rec[0]["phases"])), (1, 1))
        self.assertTrue(np.all(arrays["necessity_predictions"][0,1:] == -1))

    def test_10_stale_resources_exact(self):
        _, rec, _ = self._run_stale()
        f = rec[0]["final"]["features"]
        self.assertEqual((f[62],f[63],f[64],f[67],f[70],f[71]),
                         (10,3,1,1,0,10))

    def test_11_refresh_advances_identity_exactly_once(self):
        _, rec, _ = self._run_stale()
        initial = rec[0]["initial"]["features"]
        final = rec[0]["final"]["features"]
        self.assertEqual((final[2], final[3]), (initial[2]+1, initial[3]+1))

    def test_12_stale_no_receipt_or_fact_mutation(self):
        _, rec, _ = self._run_stale()
        self.assertEqual(rec[0]["receipts"], [])
        self.assertEqual(
            rec[0]["initial"]["features"][46:62],
            rec[0]["final"]["features"][46:62],
        )

    def test_13_score_stale_accepts_integration_record(self):
        _, rec, _ = self._run_stale()
        s = c198.score_stale(
            rec[0], 1, 0, rec[0]["initial"]["features"]
        )
        self.assertEqual(s["failed"], 0)

    def test_14_score_rejects_wrong_status(self):
        _, rec, _ = self._run_stale()
        rec[0]["status"] = "UNRESOLVED_ACQUISITION_PROVIDER_FAILURE"
        s = c198.score_stale(rec[0], 1, 0, rec[0]["initial"]["features"])
        self.assertEqual((s["status_error"], s["failed"]), (1, 1))

    def test_15_gate_accepts(self):
        self.assertTrue(c198.gate(good_allowed(), good_stale()))

    def test_16_gate_requires_nine(self):
        self.assertFalse(c198.gate(good_allowed()[:-1], good_stale()))

    def test_17_gate_rejects_allowed_replay_error(self):
        a, s = good_allowed(), good_stale()
        a[0]["reference_replay_error"] = 1
        self.assertFalse(c198.gate(a, s))

    def test_18_gate_rejects_stale_error(self):
        a, s = good_allowed(), good_stale()
        s[0]["stale_reservation_error"] = s[0]["failed"] = 1
        self.assertFalse(c198.gate(a, s))

    def test_19_gate_rejects_provider_call(self):
        a, s = good_allowed(), good_stale()
        s[0]["provider_calls"] = 1
        self.assertFalse(c198.gate(a, s))

    def test_20_gate_rejects_provider_read(self):
        a, s = good_allowed(), good_stale()
        s[0]["actual_provider_reads"] = 1
        self.assertFalse(c198.gate(a, s))

    def test_21_gate_rejects_retry(self):
        a, s = good_allowed(), good_stale()
        s[0]["retries"] = 1
        self.assertFalse(c198.gate(a, s))

    def test_22_parent_loader_contract_is_explicit(self):
        source = inspect.getsource(c198.load_c197_predictions)
        self.assertIn("(2, 9, 9536, 4)", source)
        self.assertIn("C197 prediction schema drift", source)

    def test_23_refresh_occurs_between_reservation_and_dispatch(self):
        source = inspect.getsource(c198.acquire)
        self.assertLess(source.index("owner.apply("), source.index("invalidate_reservation(owner)"))
        self.assertLess(source.index("invalidate_reservation(owner)"), source.index("owner.dispatch("))

    def test_24_reason_rule_prefers_dispatch(self):
        source = inspect.getsource(c198.run_loop_stale_aware)
        self.assertIn('dispatch.get("reason")', source)
        self.assertIn('"UNRESOLVED_ACQUISITION_" + str(reason)', source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
