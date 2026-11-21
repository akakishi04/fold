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
from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as c196

def raw_row13():
    x=np.zeros(72,dtype=np.int32);x[0]=7;x[1]=4;x[2]=1;x[3]=1
    nodes=((1,1,1,0,0,0),(1,1,2,0,0,0),(1,2,0,1,2,0),
           (1,1,3,0,0,0),(1,1,4,0,0,0),(1,3,0,4,5,0),(1,2,0,3,6,0))
    x[4:46]=np.asarray(nodes,dtype=np.int32).reshape(-1)
    vis=(None,None,None,1)
    for i,v in enumerate(vis):
        x[46+4*i:50+4*i]=(1,1 if v is None else 2,0 if v is None else 1,0 if v is None else v)
    x[62:72]=(13,4,1,0,0,1,0,0,0,7)
    return x

def endpoint(tmp,code=3):
    bb=c190.world_bytes(code);p=Path(tmp)/f"w{code:02d}.json";p.write_bytes(bb)
    sb=life.SourceBinding(f"C190-world-{code:02d}",hashlib.sha256(bb).hexdigest())
    provider=life.FileSnapshotProvider(p,sb)
    return life.Endpoint(sb,provider),provider

def meter(n):
    return dict(rows=n,forward_calls=1,cell_calls=7,wall_clock_seconds=0.0)

def initial_for(views,target_index=0):
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{},max_dispatches=3) for v in views]
    if not all(driver.charge_decision(o) for o in owners):raise AssertionError("charge failed")
    raw,_=c189.encode_views([o.state.view for o in owners]);n=len(raw)
    unknown=target.missing_mask(raw).numpy()
    tz=np.full((n,4),-np.inf,dtype=np.float32);tz[unknown]=0.;tz[np.arange(n),target_index]=1.
    return dict(raw=raw,necessity_predictions=np.ones(n,dtype=np.int8),
        target_predictions=np.full(n,target_index,dtype=np.int8),
        necessity_logits=np.tile(np.asarray([[0.,1.]],dtype=np.float32),(n,1)),
        target_logits=tz)

def good_allowed():
    out=[]
    for b,h in c196.expected_order():
        first=9536;second=3900;third=928
        out.append(dict(base_seed=b,head_seed=h,episodes=9536,actual_reads=first+second+third,
            failed=0,necessity_error=0,target_error=0,selected_observed=0,repeated_target=0,
            acquisition_error=0,contract_error=0,final_decision_error=0,
            reference_replay_error=0,reference_block_mismatch=0,
            first_reads=first,second_reads=second,third_reads=third,final_decision_rows=third,
            reference_necessity_prediction_errors=0,reference_target_prediction_errors=0,
            reference_necessity_max_abs_logit_difference=0.0,
            reference_target_max_abs_logit_difference=0.0))
    return out

def good_denied():
    out=[]
    for b,h in c196.expected_order():
        out.append(dict(base_seed=b,head_seed=h,episodes=9536,actual_reads=0,bytes_read=0,
            denied_attempts=9536,provider_calls=0,publications=0,receipts=0,
            learned_decisions=9536,retries=0,
            initial_reference_prediction_errors=0,initial_reference_target_errors=0,
            initial_reference_necessity_logit_delta=0.0,initial_reference_target_logit_delta=0.0,
            failed=0,initial_prediction_error=0,denied_attempt_error=0,status_error=0,
            provider_call_error=0,publication_error=0,receipt_error=0,retry_error=0,
            resource_error=0,fact_mutation_error=0,fake_sufficient_error=0))
    return out

class C196Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c196.digest(c196.manifest()),c196.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m=c196.manifest()
        self.assertEqual((m["episodes_per_arm"],m["blocks_per_arm"]),(85824,9))
        self.assertEqual(tuple(m["arms"]),c196.ARMS)

    def test_03_outputs_exact(self):
        self.assertEqual(len(c196.OUTPUTS),5)

    def test_04_expected_order(self):
        self.assertEqual(len(c196.expected_order()),9)

    def test_05_admitted_true_only_for_published_observation(self):
        a=dict(action=dict(status="PENDING",reason="ACQUISITION_RESERVED",acquisition_reserved=1),
               dispatch=dict(status="PUBLISHED",reason="OBSERVATION_ADMITTED",
                             provider_calls=1,fact_publications=1))
        self.assertTrue(c196.admitted(a))
        a["dispatch"]["status"]="DENIED"
        self.assertFalse(c196.admitted(a))

    def test_06_permission_refresh_only_revokes_retrieve(self):
        raw=torch.from_numpy(np.stack([raw_row13()]))
        view=c190.make_views(raw,np.array([0]),np.array([3]),"x")[0]
        owner=life.AcquisitionOwner(action.RuntimeState(view),{},max_dispatches=3)
        before=owner.state.view
        c196.revoke_retrieve_permission(owner)
        after=owner.state.view
        self.assertTrue(before.resources.permitted[0])
        self.assertFalse(after.resources.permitted[0])
        self.assertEqual(before.resources.internal_remaining,after.resources.internal_remaining)
        self.assertEqual(before.resources.internal_step,after.resources.internal_step)

    def _run(self,arm):
        td=tempfile.TemporaryDirectory()
        ep,p=endpoint(td.name,3)
        raw=torch.from_numpy(np.stack([raw_row13()]))
        views=c190.make_views(raw,np.array([0]),np.array([3]),"x")
        base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector();calls=[0]
        def combined(base,head,raw,**kw):
            calls[0]+=1;n=len(raw);ti=1 if calls[0]==1 else 2
            return np.ones(n,np.int8),np.full(n,ti,np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
        final=lambda base,raw,**kw:(np.zeros(len(raw),np.int8),np.zeros((len(raw),2),np.float32),meter(len(raw)))
        with mock.patch.object(c189,"combined_predict",combined),mock.patch.object(c189,"necessity_predict",final):
            rec,arr,_=c196.run_loop_result_aware(
                views,np.array([3]),{3:ep},base,head,initial_for(views,0),arm)
        return td,p,rec,arr

    def test_07_allowed_three_acquisitions(self):
        td,p,rec,_=self._run("ALLOWED")
        try:self.assertEqual((p.reads,len(rec[0]["acquisitions"])),(3,3))
        finally:td.cleanup()

    def test_08_allowed_final_sufficient(self):
        td,_,rec,_=self._run("ALLOWED")
        try:self.assertEqual((rec[0]["status"],rec[0]["decision_charges"]),
                             ("SUFFICIENT_CLASSIFICATION",4))
        finally:td.cleanup()

    def test_09_allowed_resources_exact(self):
        td,_,rec,_=self._run("ALLOWED")
        try:
            f=rec[0]["final"]["features"]
            self.assertEqual((f[62],f[63],f[71]),(0,1,20))
        finally:td.cleanup()

    def test_10_denied_one_attempt_no_provider_read(self):
        td,p,rec,_=self._run("PERMISSION_REVOKED_AFTER_DECISION")
        try:self.assertEqual((p.reads,len(rec[0]["acquisitions"])),(0,1))
        finally:td.cleanup()

    def test_11_denied_status_and_reason(self):
        td,_,rec,_=self._run("PERMISSION_REVOKED_AFTER_DECISION")
        try:
            a=rec[0]["acquisitions"][0]
            self.assertEqual(rec[0]["status"],"UNRESOLVED_ACQUISITION_PERMISSION_DENIED")
            self.assertEqual((a["action"]["status"],a["action"]["reason"],a["dispatch"]),
                             ("DENIED","PERMISSION_DENIED",None))
        finally:td.cleanup()

    def test_12_denied_no_retry(self):
        td,_,rec,arr=self._run("PERMISSION_REVOKED_AFTER_DECISION")
        try:
            self.assertEqual((rec[0]["decision_charges"],len(rec[0]["phases"])),(1,1))
            self.assertTrue(np.all(arr["necessity_predictions"][0,1:]==-1))
        finally:td.cleanup()

    def test_13_denied_resources_exact(self):
        td,_,rec,_=self._run("PERMISSION_REVOKED_AFTER_DECISION")
        try:
            f=rec[0]["final"]["features"]
            self.assertEqual((f[62],f[63],f[67],f[70],f[71]),(11,4,0,2,9))
        finally:td.cleanup()

    def test_14_denied_no_receipt_or_fact_mutation(self):
        td,_,rec,_=self._run("PERMISSION_REVOKED_AFTER_DECISION")
        try:
            self.assertEqual(rec[0]["receipts"],[])
            self.assertEqual(rec[0]["initial"]["features"][46:62],rec[0]["final"]["features"][46:62])
        finally:td.cleanup()

    def test_15_result_aware_source_continues_only_if_admitted(self):
        source=inspect.getsource(c196.run_loop_result_aware)
        self.assertIn("if admitted(acq):",source)
        self.assertIn("next_active.append(i)",source)
        self.assertIn("UNRESOLVED_ACQUISITION_",source)

    def test_16_gate_accepts(self):
        self.assertTrue(c196.gate(good_allowed(),good_denied()))

    def test_17_gate_rejects_allowed_replay_error(self):
        a=good_allowed();d=good_denied()
        a[0]["reference_replay_error"]=1
        self.assertFalse(c196.gate(a,d))

    def test_18_gate_rejects_allowed_block_mismatch(self):
        a=good_allowed();d=good_denied()
        a[0]["reference_block_mismatch"]=1
        self.assertFalse(c196.gate(a,d))

    def test_19_gate_rejects_denial_retry(self):
        a=good_allowed();d=good_denied()
        d[0]["retries"]=1
        self.assertFalse(c196.gate(a,d))

    def test_20_gate_rejects_denial_provider_call(self):
        a=good_allowed();d=good_denied()
        d[0]["provider_calls"]=1
        self.assertFalse(c196.gate(a,d))

    def test_21_gate_rejects_denial_resource_error(self):
        a=good_allowed();d=good_denied()
        d[0]["resource_error"]=d[0]["failed"]=1
        self.assertFalse(c196.gate(a,d))

    def _write_parent(self,p):
        np.savez_compressed(p,
            necessity_predictions=np.zeros((9,9536,4),dtype=np.int8),
            necessity_logits=np.zeros((9,9536,4,2),dtype=np.float32),
            target_predictions=np.zeros((9,9536,3),dtype=np.int8),
            target_logits=np.zeros((9,9536,3,4),dtype=np.float32),
            row_indices=np.zeros(9536,dtype=np.int32),
            local_rows=np.zeros(9536,dtype=np.int32),
            world_codes=np.zeros(9536,dtype=np.int8))

    def test_22_c194_loader_shapes(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz";self._write_parent(p)
            z=c196.load_c194_predictions(p)
            self.assertEqual(z["necessity_logits"].shape,(9,9536,4,2))

    def test_23_c194_loader_rejects_schema(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz";np.savez_compressed(p,x=np.zeros(1))
            with self.assertRaises(ValueError):c196.load_c194_predictions(p)

    def test_24_run_uses_child_loader_and_post_decision_revocation(self):
        source=inspect.getsource(c196.run)
        loop=inspect.getsource(c196.run_loop_result_aware)
        self.assertIn('saved=load_c194_predictions(',source)
        self.assertNotIn('load_parent_predictions(',source)
        self.assertLess(loop.index('phase["target_prediction"]'),loop.index("revoke_retrieve_permission"))
        self.assertLess(loop.index("revoke_retrieve_permission"),loop.index("c190.acquire("))

if __name__=="__main__":
    unittest.main(verbosity=2)
