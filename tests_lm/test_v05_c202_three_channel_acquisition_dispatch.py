import inspect
import unittest

import numpy as np

from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05 import structured_acquisition_lifecycle as life
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
from fold_lm.v05_benchmarks import gate_e_c202_three_channel_acquisition_dispatch as c202


def fake_predictions(target=0, world=3):
    tp=np.full((2,9,9536,3),-1,dtype=np.int8)
    tp[0,:,:,0]=target
    return {"target_predictions":tp,"world_codes":np.full((9536,),world,dtype=np.int8)}


def good_records():
    rows=[]
    for block in range(9):
        for channel in v2.CHANNELS:
            rows.append(dict(
                block=block,channel=channel,cases=9536,provider_calls=9536,
                publications=9536,receipts=9536,target_counts=[9536,0,0,0],
                failed=0,route_error=0,action_error=0,dispatch_error=0,
                provider_channel_error=0,receipt_error=0,selected_value_error=0,
                nonselected_mutation_error=0,resource_error=0,
            ))
    return rows


def good_summary():
    return dict(
        dispatch_cases=257472,block_records=27,failures=0,route_errors=0,
        action_errors=0,dispatch_errors=0,provider_channel_errors=0,receipt_errors=0,
        selected_value_errors=0,nonselected_mutation_errors=0,resource_errors=0,
        provider_calls=257472,publications=257472,receipts=257472,
        channel_provider_calls={"RETRIEVE":85824,"OBSERVE":85824,"ASK_USER":85824},
    )


class C202Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c202.digest(c202.manifest()),c202.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m=c202.manifest()
        self.assertEqual((m["blocks"],m["episodes_per_block"],m["dispatch_cases"]),(9,9536,257472))

    def test_03_output_contract(self):
        self.assertEqual(len(c202.OUTPUTS),5)

    def test_04_base_view_postdecision_resources(self):
        v=c202.base_view("x")
        r=v.resources
        self.assertEqual((r.internal_remaining,r.acquisitions_remaining,r.internal_step),(12,4,8))
        self.assertEqual((r.available,r.permitted),((True,True,True),(True,True,True)))

    def test_05_channel_view_retrieve(self):
        b=c202.base_view("x")
        v=c202.channel_view(b,2,0)
        self.assertEqual(v2.declared_channels(v,2),("RETRIEVE",))

    def test_06_channel_view_observe(self):
        b=c202.base_view("x")
        v=c202.channel_view(b,1,1)
        self.assertEqual(v2.declared_channels(v,1),("OBSERVE",))

    def test_07_channel_view_ask_user(self):
        b=c202.base_view("x")
        v=c202.channel_view(b,3,2)
        self.assertEqual(v2.declared_channels(v,3),("ASK_USER",))

    def test_08_memory_provider_valid_delivery(self):
        raw=c190.world_bytes(3)
        source=life.SourceBinding("C190-world-03",__import__("hashlib").sha256(raw).hexdigest())
        p=c202.MemoryWorldProvider(raw,source)
        req=life.FetchRequest("i","s|q","s","RETRIEVE",c202.c185.FACT_IDS[0],source)
        d=p(req)
        self.assertEqual((p.calls,d.status,d.action),(1,"FOUND","RETRIEVE"))

    def _one(self,channel_index,target=0,world=3):
        pm,em=c202.providers()
        score=c202.execute_one(
            block=0,row=0,world_code=world,target=target,channel_index=channel_index,
            provider_map=pm,endpoint_map=em)
        return pm,score

    def test_09_retrieve_case_passes(self):
        _,s=self._one(0)
        self.assertEqual(s["failed"],0)

    def test_10_observe_case_passes(self):
        _,s=self._one(1)
        self.assertEqual(s["failed"],0)

    def test_11_ask_user_case_passes(self):
        _,s=self._one(2)
        self.assertEqual(s["failed"],0)

    def test_12_only_retrieve_provider_called(self):
        pm,_=self._one(0,2,5)
        self.assertEqual(tuple(pm[5][c].calls for c in v2.CHANNELS),(1,0,0))

    def test_13_only_observe_provider_called(self):
        pm,_=self._one(1,2,5)
        self.assertEqual(tuple(pm[5][c].calls for c in v2.CHANNELS),(0,1,0))

    def test_14_only_ask_user_provider_called(self):
        pm,_=self._one(2,2,5)
        self.assertEqual(tuple(pm[5][c].calls for c in v2.CHANNELS),(0,0,1))

    def test_15_selected_world_value_checked(self):
        _,s=self._one(1,3,9)
        self.assertEqual(s["selected_value_error"],0)

    def test_16_nonselected_facts_untouched(self):
        _,s=self._one(2,1,6)
        self.assertEqual(s["nonselected_mutation_error"],0)

    def test_17_resource_contract_exact(self):
        _,s=self._one(0,1,6)
        self.assertEqual(s["resource_error"],0)

    def test_18_action_and_dispatch_contract_exact(self):
        _,s=self._one(0,1,6)
        self.assertEqual((s["action_error"],s["dispatch_error"]),(0,0))

    def test_19_gate_accepts_registered_shape(self):
        self.assertTrue(c202.gate(good_summary(),good_records()))

    def test_20_gate_rejects_route_error(self):
        s=good_summary();r=good_records();s["route_errors"]=1
        self.assertFalse(c202.gate(s,r))

    def test_21_gate_rejects_wrong_channel_total(self):
        s=good_summary();r=good_records();s["channel_provider_calls"]["ASK_USER"]-=1
        self.assertFalse(c202.gate(s,r))

    def test_22_gate_rejects_block_provider_shortfall(self):
        s=good_summary();r=good_records();r[0]["provider_calls"]-=1
        self.assertFalse(c202.gate(s,r))

    def test_23_gate_rejects_publication_shortfall(self):
        s=good_summary();r=good_records();s["publications"]-=1
        self.assertFalse(c202.gate(s,r))

    def test_24_manifest_uses_no_training(self):
        m=c202.manifest()
        self.assertEqual((m["training_steps"],m["fresh_seed_count"],m["learned_forward_calls"]),(0,0,0))

    def test_25_execute_path_uses_mapper_and_owner_dispatch(self):
        source=inspect.getsource(c202.execute_one)
        self.assertIn("mapper.propose_selected",source)
        self.assertIn("owner.apply",source)
        self.assertIn("owner.dispatch",source)

    def test_26_fixture_is_in_memory_not_file_provider(self):
        source=inspect.getsource(c202.MemoryWorldProvider)
        self.assertNotIn("Path(",source)
        self.assertNotIn("FileSnapshotProvider",source)


if __name__=="__main__":
    unittest.main(verbosity=2)
