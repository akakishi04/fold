import hashlib
import inspect
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
import torch

from fold_lm.v05 import structured_acquisition_lifecycle as life
from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
from fold_lm.v05_benchmarks import gate_e_c199_attempt_limit_generic_loop as c199


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


def second_need():
    return (
        np.asarray([1], dtype=np.int8),
        np.asarray([1], dtype=np.int8),
        np.asarray([[0.0,1.0]], dtype=np.float32),
        np.asarray([[0.0,1.0,0.0,-np.inf]], dtype=np.float32),
        dict(rows=1, forward_calls=1, cell_calls=7, wall_clock_seconds=0.0),
    )


def good_allowed():
    out = []
    second = (3888,3896,3936,3816,3856,3888,3920,3888,3860)
    for idx, (b, h) in enumerate(c199.expected_order()):
        first, third = 9536, 928
        out.append(dict(
            base_seed=b, head_seed=h, episodes=9536,
            actual_reads=first+second[idx]+third,
            failed=0, necessity_error=0, target_error=0, selected_observed=0,
            repeated_target=0, acquisition_error=0, contract_error=0,
            final_decision_error=0, reference_replay_error=0,
            reference_block_mismatch=0, first_reads=first, second_reads=second[idx],
            third_reads=third, final_decision_rows=third,
            reference_necessity_prediction_errors=0,
            reference_target_prediction_errors=0,
            reference_necessity_max_abs_logit_difference=0.0,
            reference_target_max_abs_logit_difference=0.0,
        ))
    return out


def good_limit():
    second = (3888,3896,3936,3816,3856,3888,3920,3888,3860)
    out = []
    for idx, (b, h) in enumerate(c199.expected_order()):
        rec = dict(
            base_seed=b, head_seed=h, episodes=9536,
            first_reads=9536, provider_calls=9536, publications=9536, receipts=9536,
            learned_decisions=19072, attempt_limit_rows=second[idx],
            sufficient_after_first=9536-second[idx], reference_second_reads=second[idx],
            second_provider_calls=0, second_publications=0,
            prefix_necessity_prediction_errors=0, prefix_target_prediction_errors=0,
            prefix_necessity_logit_delta=0.0, prefix_target_logit_delta=0.0,
            unauthorized_third_prediction=0,
        )
        rec.update({k: 0 for k in c199.LIMIT_COUNTERS})
        out.append(rec)
    return out


class C199Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c199.digest(c199.manifest()), c199.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m = c199.manifest()
        self.assertEqual((m["episodes_per_arm"], m["blocks_per_arm"]), (85824, 9))
        self.assertEqual(tuple(m["arms"]), c199.ARMS)

    def test_03_outputs_exact(self):
        self.assertEqual(len(c199.OUTPUTS), 5)

    def test_04_expected_order(self):
        self.assertEqual(len(c199.expected_order()), 9)

    def _run_limit(self):
        raw = torch.from_numpy(np.stack([raw_row13()]))
        views = c190.make_views(raw, np.array([0]), np.array([3]), "x")
        data = c190.world_bytes(3)
        binding = life.SourceBinding("C190-world-03", hashlib.sha256(data).hexdigest())
        td = tempfile.TemporaryDirectory()
        path = Path(td.name) / "world-03.json"
        path.write_bytes(data)
        provider = life.FileSnapshotProvider(path, binding)
        endpoint = life.Endpoint(binding, provider)
        base = graph.SharedGraphProbe(graph.ARMS[1])
        head = target.TargetSelector()
        with mock.patch.object(c189, "combined_predict", return_value=second_need()):
            rec, arrays, _ = c199.run_loop_limit(
                views, np.array([3]), {3: endpoint}, base, head,
                initial_for(views, 0), "DISPATCH_LIMIT_ONE",
            )
        return td, provider, rec, arrays

    def test_05_first_provider_call_occurs_once(self):
        td, provider, rec, _ = self._run_limit()
        try:
            self.assertEqual((provider.reads, len(rec[0]["acquisitions"])), (1, 2))
        finally:
            td.cleanup()

    def test_06_first_acquisition_is_admitted(self):
        td, _, rec, _ = self._run_limit()
        try:
            a = rec[0]["acquisitions"][0]
            self.assertEqual((a["dispatch"]["status"], a["dispatch"]["reason"]),
                             ("PUBLISHED", "OBSERVATION_ADMITTED"))
        finally:
            td.cleanup()

    def test_07_second_reservation_is_created(self):
        td, _, rec, _ = self._run_limit()
        try:
            a = rec[0]["acquisitions"][1]["action"]
            self.assertEqual((a["status"], a["reason"], a["acquisition_reserved"]),
                             ("PENDING", "ACQUISITION_RESERVED", 1))
        finally:
            td.cleanup()

    def test_08_second_dispatch_hits_attempt_limit(self):
        td, _, rec, _ = self._run_limit()
        try:
            d = rec[0]["acquisitions"][1]["dispatch"]
            self.assertEqual((d["status"], d["reason"], d["provider_calls"]),
                             ("DENIED", "ATTEMPT_LIMIT", 0))
        finally:
            td.cleanup()

    def test_09_reason_propagates_to_loop_status(self):
        td, _, rec, _ = self._run_limit()
        try:
            self.assertEqual(rec[0]["status"],
                             "UNRESOLVED_ACQUISITION_ATTEMPT_LIMIT")
        finally:
            td.cleanup()

    def test_10_limit_has_no_third_decision(self):
        td, _, rec, arrays = self._run_limit()
        try:
            self.assertEqual((rec[0]["decision_charges"], len(rec[0]["phases"])), (2, 2))
            self.assertTrue(np.all(arrays["necessity_predictions"][0,2:] == -1))
            self.assertTrue(np.all(arrays["target_predictions"][0,2:] == -1))
        finally:
            td.cleanup()

    def test_11_limit_resources_exact(self):
        td, _, rec, _ = self._run_limit()
        try:
            f = rec[0]["final"]["features"]
            self.assertEqual((f[62],f[63],f[64],f[67],f[70],f[71]),
                             (6,2,1,1,5,14))
        finally:
            td.cleanup()

    def test_12_one_receipt_and_one_new_observation(self):
        td, _, rec, _ = self._run_limit()
        try:
            initial = rec[0]["initial"]["features"]
            final = rec[0]["final"]["features"]
            self.assertEqual(len(rec[0]["receipts"]), 1)
            before = sum(initial[48+4*i] == 1 for i in range(4))
            after = sum(final[48+4*i] == 1 for i in range(4))
            self.assertEqual(after, before+1)
        finally:
            td.cleanup()

    def test_13_score_limit_accepts_integration_record(self):
        td, _, rec, _ = self._run_limit()
        try:
            s = c199.score_limit(rec[0], 1, 0, 1, 1, rec[0]["initial"]["features"])
            self.assertEqual(s["failed"], 0)
        finally:
            td.cleanup()

    def test_14_score_rejects_wrong_status(self):
        td, _, rec, _ = self._run_limit()
        try:
            rec[0]["status"] = "UNRESOLVED_ACQUISITION_PROVIDER_FAILURE"
            s = c199.score_limit(rec[0], 1, 0, 1, 1, rec[0]["initial"]["features"])
            self.assertEqual((s["status_error"], s["failed"]), (1, 1))
        finally:
            td.cleanup()

    def test_15_gate_accepts(self):
        self.assertTrue(c199.gate(good_allowed(), good_limit()))

    def test_16_gate_requires_nine(self):
        self.assertFalse(c199.gate(good_allowed()[:-1], good_limit()))

    def test_17_gate_rejects_allowed_replay_error(self):
        a, l = good_allowed(), good_limit()
        a[0]["reference_replay_error"] = 1
        self.assertFalse(c199.gate(a, l))

    def test_18_gate_rejects_limit_error(self):
        a, l = good_allowed(), good_limit()
        l[0]["attempt_limit_contract_error"] = l[0]["failed"] = 1
        self.assertFalse(c199.gate(a, l))

    def test_19_gate_rejects_second_provider_call(self):
        a, l = good_allowed(), good_limit()
        l[0]["second_provider_calls"] = 1
        self.assertFalse(c199.gate(a, l))

    def test_20_gate_rejects_third_prediction(self):
        a, l = good_allowed(), good_limit()
        l[0]["unauthorized_third_prediction"] = 1
        self.assertFalse(c199.gate(a, l))

    def test_21_gate_requires_reference_second_count(self):
        a, l = good_allowed(), good_limit()
        l[0]["attempt_limit_rows"] -= 1
        self.assertFalse(c199.gate(a, l))

    def test_22_parent_loader_contract_is_explicit(self):
        source = inspect.getsource(c199.load_c198_predictions)
        self.assertIn("(2, 9, 9536, 4)", source)
        self.assertIn("C198 prediction schema drift", source)

    def test_23_owner_limit_is_single_changed_runtime_config(self):
        source = inspect.getsource(c199.run_loop_limit)
        self.assertIn('dispatch_limit = MAX_ACQUISITIONS if arm == "ALLOWED" else 1', source)
        self.assertIn("max_dispatches=dispatch_limit", source)

    def test_24_reason_rule_prefers_dispatch(self):
        source = inspect.getsource(c199.run_loop_limit)
        self.assertIn('dispatch.get("reason")', source)
        self.assertIn('"UNRESOLVED_ACQUISITION_" + str(reason)', source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
