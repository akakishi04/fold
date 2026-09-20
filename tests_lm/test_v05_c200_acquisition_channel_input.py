import inspect
import unittest
from dataclasses import replace

from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05_benchmarks import gate_e_c200_acquisition_channel_input as c200


class C200Tests(unittest.TestCase):
    def test_01_schema_identity(self):
        self.assertEqual(v2.SCHEMA, "fold-structured-task-input-v2")

    def test_02_feature_width_is_additive(self):
        self.assertEqual(v2.FEATURE_WIDTH, 84)

    def test_03_channels_match_registered_tools(self):
        self.assertEqual(v2.CHANNELS, v1.TOOLS)

    def test_04_manifest_hash(self):
        self.assertEqual(c200.digest(c200.manifest()), c200.MANIFEST_SHA)

    def test_05_manifest_scope_counts(self):
        m = c200.manifest()
        self.assertEqual((m["mask_roundtrips"], m["runtime_cross"], m["hidden_pairs"], m["malformed_cases"]),
                         (32,448,12,18))

    def test_06_four_fact_prefix_exact(self):
        base = c200.four_fact_base()
        view = v2.TaskView(base, tuple(v2.FactChannels((True,False,False)) for _ in range(4)))
        packet = v2.encode(view)
        self.assertEqual(packet.features[:72], v1.encode(base).features)

    def test_07_four_fact_binding_exact(self):
        base = c200.four_fact_base()
        view = v2.TaskView(base, tuple(v2.FactChannels((False,True,False)) for _ in range(4)))
        self.assertEqual(v2.encode(view).binding, v1.encode(base).binding)

    def test_08_roundtrip_exact(self):
        base = c200.four_fact_base()
        view = v2.TaskView(base, tuple(v2.FactChannels((True,True,False)) for _ in range(4)))
        self.assertEqual(v2.decode(v2.encode(view)), view)

    def test_09_all_channel_masks_roundtrip(self):
        rows = c200.mask_roundtrips()
        self.assertEqual((len(rows), sum(not r["passed"] for r in rows)), (32,0))

    def test_10_all_eight_channel_classes_present(self):
        rows = c200.mask_roundtrips()
        masks = {tuple(r["mask"]) for r in rows}
        self.assertEqual(len(masks), 8)

    def test_11_runtime_cross_count(self):
        rows = c200.runtime_cross()
        self.assertEqual(len(rows), 448)

    def test_12_runtime_cross_all_pass(self):
        rows = c200.runtime_cross()
        self.assertFalse(any(not r["passed"] for r in rows))

    def test_13_declared_channels_do_not_apply_authority(self):
        base = c200.one_fact_base(v1.Resources(
            internal_remaining=3, acquisitions_remaining=1,
            available=(False,False,False), permitted=(False,False,False)))
        view = v2.TaskView(base, (v2.FactChannels((True,True,True)),))
        self.assertEqual(v2.declared_channels(view,0), v1.TOOLS)
        self.assertEqual(v2.visible_usable_channels(view,0), ())

    def test_14_visible_usable_intersects_masks(self):
        base = c200.one_fact_base(v1.Resources(
            internal_remaining=3, acquisitions_remaining=1,
            available=(True,True,False), permitted=(True,False,True)))
        view = v2.TaskView(base, (v2.FactChannels((True,True,True)),))
        self.assertEqual(v2.visible_usable_channels(view,0), ("RETRIEVE",))

    def test_15_zero_channel_fact_is_representable(self):
        base = c200.one_fact_base(v1.Resources())
        view = v2.TaskView(base, (v2.FactChannels((False,False,False)),))
        self.assertEqual(v2.declared_channels(view,0), ())

    def test_16_hidden_pair_count(self):
        self.assertEqual(len(c200.hidden_pairs()), 12)

    def test_17_hidden_pair_packets_identical(self):
        self.assertFalse(any(not r["packet_equal"] for r in c200.hidden_pairs()))

    def test_18_hidden_pairs_include_answer_changing_cases(self):
        self.assertEqual(sum(r["answer_differs"] for r in c200.hidden_pairs()), 6)

    def test_19_hidden_values_not_in_packet_contract(self):
        self.assertTrue(all(not r["hidden_value_present_in_packet"] for r in c200.hidden_pairs()))

    def test_20_malformed_count(self):
        self.assertEqual(len(c200.malformed_rows()), 18)

    def test_21_all_malformed_rejected(self):
        self.assertTrue(all(r["rejected"] for r in c200.malformed_rows()))

    def test_22_padding_must_be_zero(self):
        base = c200.one_fact_base(v1.Resources())
        packet = v2.encode(v2.TaskView(base,(v2.FactChannels((True,False,False)),)))
        values = list(packet.features); values[75] = 1
        with self.assertRaises(ValueError):
            v2.decode(replace(packet,features=tuple(values)))

    def test_23_channel_flag_bool_is_rejected(self):
        base = c200.one_fact_base(v1.Resources())
        packet = v2.encode(v2.TaskView(base,(v2.FactChannels((True,False,False)),)))
        values = list(packet.features); values[72] = True
        with self.assertRaises(ValueError):
            v2.decode(replace(packet,features=tuple(values)))

    def test_24_v1_consumer_cannot_implicitly_accept_v2(self):
        def consumer(packet):
            return packet
        consumer.input_schema = v1.SCHEMA
        base = c200.one_fact_base(v1.Resources())
        view = v2.TaskView(base,(v2.FactChannels((True,False,False)),))
        with self.assertRaises(TypeError):
            v2.deliver(view,consumer)

    def test_25_v2_consumer_explicit_accept(self):
        def consumer(packet):
            return packet
        consumer.input_schema = v2.SCHEMA
        base = c200.one_fact_base(v1.Resources())
        view = v2.TaskView(base,(v2.FactChannels((False,False,True)),))
        self.assertEqual(v2.deliver(view,consumer), v2.encode(view))

    def test_26_gate_accepts_collected_summary(self):
        summary,*_ = c200.collect()
        self.assertTrue(c200.gate(summary))

    def test_27_gate_rejects_prefix_failure(self):
        summary,*_ = c200.collect()
        summary["v1_prefix_preserved"] = False
        self.assertFalse(c200.gate(summary))

    def test_28_gate_rejects_hidden_packet_mismatch(self):
        summary,*_ = c200.collect()
        summary["hidden_packet_mismatches"] = 1
        self.assertFalse(c200.gate(summary))

    def test_29_source_has_no_action_execution_import(self):
        source = inspect.getsource(v2)
        self.assertNotIn("structured_action_runtime", source)
        self.assertNotIn("structured_acquisition_lifecycle", source)

    def test_30_source_layout_is_v1_prefix_plus_tail(self):
        source = inspect.getsource(v2.encode)
        self.assertIn("features = list(parent.features)", source)
        self.assertIn("features.extend", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
