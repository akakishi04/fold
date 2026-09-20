import inspect
import unittest

import numpy as np

from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05 import structured_acquisition_lifecycle as life
from fold_lm.v05_benchmarks import gate_e_c203_mixed_channel_multistep_replay as c203


def fake_predictions():
    n=np.full((2,9,9536,4),-1,dtype=np.int8)
    t=np.full((2,9,9536,3),-1,dtype=np.int8)
    # Every row: NEEDS target0 -> SUFFICIENT.
    n[0,:,:,0]=1;n[0,:,:,1]=0
    t[0,:,:,0]=0
    return {
        "necessity_predictions":n,
        "target_predictions":t,
    }


def tiny_base():
    resources=v1.Resources(
        internal_remaining=13,acquisitions_remaining=4,
        available=c203.PARENT_AVAILABLE,permitted=c203.PARENT_PERMITTED,
        last_outcome="NONE",internal_step=7)
    nodes=(
        v1.Node("FACT",0),v1.Node("FACT",1),v1.Node("AND",left=0,right=1),
        v1.Node("FACT",2),v1.Node("FACT",3),v1.Node("OR",left=3,right=4),
        v1.Node("OR",left=2,right=5),
    )
    facts=tuple(v1.Fact(c203.c185.FACT_IDS[i]) for i in range(4))
    return v1.TaskView("C203|tiny","C203",nodes,facts,resources)


class C203Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c203.digest(c203.manifest()),c203.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m=c203.manifest()
        self.assertEqual((m["blocks"],m["episodes_per_block"]),(9,9536))
        self.assertEqual(m["channel_layout"],list(c203.CHANNEL_LAYOUT))

    def test_03_channel_layout_fixed(self):
        self.assertEqual(c203.CHANNEL_LAYOUT,("RETRIEVE","OBSERVE","ASK_USER","RETRIEVE"))

    def test_04_parent_masks_fixed(self):
        self.assertEqual(c203.PARENT_AVAILABLE,(True,False,False))
        self.assertEqual(c203.PARENT_PERMITTED,(True,False,False))

    def test_05_mixed_view_fact0_retrieve(self):
        view=c203.mixed_view(tiny_base())
        self.assertEqual(v2.declared_channels(view,0),("RETRIEVE",))

    def test_06_mixed_view_fact1_observe(self):
        view=c203.mixed_view(tiny_base())
        self.assertEqual(v2.declared_channels(view,1),("OBSERVE",))

    def test_07_mixed_view_fact2_ask_user(self):
        view=c203.mixed_view(tiny_base())
        self.assertEqual(v2.declared_channels(view,2),("ASK_USER",))

    def test_08_mixed_view_fact3_retrieve(self):
        view=c203.mixed_view(tiny_base())
        self.assertEqual(v2.declared_channels(view,3),("RETRIEVE",))

    def test_09_set_authority_all_true(self):
        owner=life.AcquisitionOwner(action.RuntimeState(tiny_base()),{},max_dispatches=3)
        c203.set_authority(owner,all_channels=True)
        self.assertEqual(owner.state.view.resources.available,(True,True,True))
        self.assertEqual(owner.state.view.resources.permitted,(True,True,True))

    def test_10_set_authority_restore_parent(self):
        owner=life.AcquisitionOwner(action.RuntimeState(tiny_base()),{},max_dispatches=3)
        c203.set_authority(owner,all_channels=True)
        c203.set_authority(owner,all_channels=False)
        self.assertEqual(owner.state.view.resources.available,c203.PARENT_AVAILABLE)
        self.assertEqual(owner.state.view.resources.permitted,c203.PARENT_PERMITTED)

    def test_11_authority_refresh_does_not_change_budget(self):
        owner=life.AcquisitionOwner(action.RuntimeState(tiny_base()),{},max_dispatches=3)
        before=owner.state.view.resources
        c203.set_authority(owner,all_channels=True)
        after=owner.state.view.resources
        self.assertEqual(
            (after.internal_remaining,after.acquisitions_remaining,after.internal_step),
            (before.internal_remaining,before.acquisitions_remaining,before.internal_step))

    def test_12_expected_projection_shape(self):
        p=c203.expected_projection(fake_predictions())
        self.assertEqual(len(p["blocks"]),9)
        self.assertEqual(p["totals"]["episodes"],85824)

    def test_13_expected_projection_acquisitions(self):
        p=c203.expected_projection(fake_predictions())
        self.assertEqual(p["totals"]["acquisitions"],85824)
        self.assertEqual(p["totals"]["decisions"],171648)

    def test_14_expected_projection_channel_mapping(self):
        p=c203.expected_projection(fake_predictions())
        self.assertEqual(
            p["totals"]["channel_counts"],
            {"RETRIEVE":85824,"OBSERVE":0,"ASK_USER":0})

    def test_15_expected_projection_no_switch_for_one_acquisition(self):
        p=c203.expected_projection(fake_predictions())
        self.assertEqual(p["totals"]["channel_switches"],0)

    def test_16_projection_rejects_nonterminal_needs(self):
        p=fake_predictions()
        p["necessity_predictions"][0,:,:,1]=1
        with self.assertRaises(ValueError):
            c203.expected_projection(p)

    def test_17_projection_rejects_target_depth_mismatch(self):
        p=fake_predictions()
        p["target_predictions"][0,:,:,0]=-1
        with self.assertRaises(ValueError):
            c203.expected_projection(p)

    def test_18_gate_accepts_registered_projection(self):
        projection={"totals":{
            "episodes":85824,"decisions":214948,"acquisitions":129124,
            "final_sufficient":85824,
            "channel_counts":{"RETRIEVE":100000,"OBSERVE":15000,"ASK_USER":14124},
            "channel_switches":1000}}
        records=[dict(failed=0,projection_error=0) for _ in range(9)]
        totals=dict(
            episodes=85824,decisions=214948,acquisitions=129124,final_sufficient=85824,
            channel_counts={"RETRIEVE":100000,"OBSERVE":15000,"ASK_USER":14124},
            channel_switches=1000,failures=0,projection_errors=0)
        self.assertTrue(c203.gate(projection,records,totals))

    def test_19_gate_rejects_zero_switches(self):
        projection={"totals":{
            "episodes":85824,"decisions":2,"acquisitions":1,"final_sufficient":85824,
            "channel_counts":{"RETRIEVE":1,"OBSERVE":0,"ASK_USER":0},
            "channel_switches":0}}
        records=[dict(failed=0,projection_error=0) for _ in range(9)]
        totals=dict(
            episodes=85824,decisions=2,acquisitions=1,final_sufficient=85824,
            channel_counts={"RETRIEVE":1,"OBSERVE":0,"ASK_USER":0},
            channel_switches=0,failures=0,projection_errors=0)
        self.assertFalse(c203.gate(projection,records,totals))

    def test_20_gate_rejects_provider_projection_mismatch(self):
        projection={"totals":{
            "episodes":85824,"decisions":10,"acquisitions":9,"final_sufficient":85824,
            "channel_counts":{"RETRIEVE":3,"OBSERVE":3,"ASK_USER":3},
            "channel_switches":2}}
        records=[dict(failed=0,projection_error=0) for _ in range(9)]
        totals=dict(
            episodes=85824,decisions=10,acquisitions=9,final_sufficient=85824,
            channel_counts={"RETRIEVE":4,"OBSERVE":2,"ASK_USER":3},
            channel_switches=2,failures=0,projection_errors=0)
        self.assertFalse(c203.gate(projection,records,totals))

    def test_21_gate_rejects_record_failure(self):
        projection={"totals":{
            "episodes":85824,"decisions":10,"acquisitions":9,"final_sufficient":85824,
            "channel_counts":{"RETRIEVE":3,"OBSERVE":3,"ASK_USER":3},
            "channel_switches":2}}
        records=[dict(failed=0,projection_error=0) for _ in range(9)]
        records[0]["failed"]=1
        totals=dict(
            episodes=85824,decisions=10,acquisitions=9,final_sufficient=85824,
            channel_counts={"RETRIEVE":3,"OBSERVE":3,"ASK_USER":3},
            channel_switches=2,failures=1,projection_errors=0)
        self.assertFalse(c203.gate(projection,records,totals))

    def test_22_source_replay_uses_saved_predictions(self):
        collect_source=inspect.getsource(c203.collect)
        replay_source=inspect.getsource(c203.replay_block)
        self.assertIn('predictions["necessity_predictions"]',collect_source)
        self.assertIn('predictions["target_predictions"]',collect_source)
        self.assertIn("necessity[i,phase]",replay_source)
        self.assertIn("targets[i,phase]",replay_source)
        self.assertNotIn("combined_predict(",collect_source+replay_source)
        self.assertNotIn("necessity_predict(",collect_source+replay_source)

    def test_23_replay_charges_decision_before_action_window(self):
        source=inspect.getsource(c203.replay_block)
        self.assertLess(source.index("c185.charge_decision"),source.index("set_authority(owner, all_channels=True)"))

    def test_24_replay_restores_authority_after_dispatch(self):
        source=inspect.getsource(c203.replay_block)
        self.assertLess(source.index("owner.dispatch"),source.index("set_authority(owner, all_channels=False)"))

    def test_25_replay_uses_mapper(self):
        source=inspect.getsource(c203.replay_block)
        self.assertIn("mapper.propose_selected",source)

    def test_26_replay_uses_real_dispatch(self):
        source=inspect.getsource(c203.replay_block)
        self.assertIn("owner.apply",source)
        self.assertIn("owner.dispatch",source)

    def test_27_loader_requires_c174_hash(self):
        source=inspect.getsource(c203.load_c174_features)
        self.assertIn("C174_SHA",source)
        self.assertIn('"pilot-data.npz"',source)

    def test_28_scope_has_no_training_or_forward(self):
        m=c203.manifest()
        self.assertEqual(
            (m["training_steps"],m["fresh_seed_count"],m["learned_forward_calls"],m["network_calls"]),
            (0,0,0,0))


if __name__=="__main__":
    unittest.main(verbosity=2)
