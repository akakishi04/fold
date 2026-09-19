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
from fold_lm.v05_benchmarks import gate_e_c197_provider_failure_generic_loop as c197

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

def fault_endpoint(code=3):
    bb=c190.world_bytes(code)
    sb=life.SourceBinding(f"C190-world-{code:02d}",hashlib.sha256(bb).hexdigest())
    fp=c197.FailingProvider()
    return life.Endpoint(sb,fp),fp

def initial_for(views,target_index=0):
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{},max_dispatches=3) for v in views]
    if not all(driver.charge_decision(o) for o in owners): raise AssertionError("charge failed")
    raw,_=c189.encode_views([o.state.view for o in owners]);n=len(raw)
    unknown=target.missing_mask(raw).numpy()
    tz=np.full((n,4),-np.inf,dtype=np.float32);tz[unknown]=0.;tz[np.arange(n),target_index]=1.
    return dict(raw=raw,necessity_predictions=np.ones(n,dtype=np.int8),
        target_predictions=np.full(n,target_index,dtype=np.int8),
        necessity_logits=np.tile(np.asarray([[0.,1.]],dtype=np.float32),(n,1)),
        target_logits=tz)

def good_allowed():
    out=[]
    for b,h in c197.expected_order():
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

def good_failure():
    out=[]
    for b,h in c197.expected_order():
        out.append(dict(base_seed=b,head_seed=h,episodes=9536,
            failure_attempts=9536,provider_calls=9536,adapter_calls=9536,
            publications=0,receipts=0,learned_decisions=9536,retries=0,
            initial_reference_prediction_errors=0,initial_reference_target_errors=0,
            initial_reference_necessity_logit_delta=0.0,initial_reference_target_logit_delta=0.0,
            failed=0,initial_prediction_error=0,provider_failure_error=0,status_error=0,
            provider_call_error=0,publication_error=0,receipt_error=0,retry_error=0,
            resource_error=0,fact_mutation_error=0,fake_sufficient_error=0))
    return out

class C197Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c197.digest(c197.manifest()),c197.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m=c197.manifest()
        self.assertEqual((m["episodes_per_arm"],m["blocks_per_arm"]),(85824,9))
        self.assertEqual(tuple(m["arms"]),c197.ARMS)

    def test_03_outputs_exact(self):
        self.assertEqual(len(c197.OUTPUTS),5)

    def test_04_expected_order(self):
        self.assertEqual(len(c197.expected_order()),9)

    def test_05_failing_provider_counts_and_raises(self):
        _,fp=fault_endpoint()
        with self.assertRaises(life.ProviderFailure):
            fp(None)
        self.assertEqual(fp.calls,1)

    def _run_failure(self):
        ep,fp=fault_endpoint(3)
        raw=torch.from_numpy(np.stack([raw_row13()]))
        views=c190.make_views(raw,np.array([0]),np.array([3]),"x")
        base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
        rec,arr,_=c197.run_loop_reason_aware(
            views,np.array([3]),{3:ep},base,head,initial_for(views,0))
        return fp,rec,arr

    def test_06_integration_one_provider_call(self):
        fp,rec,_=self._run_failure()
        self.assertEqual((fp.calls,len(rec[0]["acquisitions"])),(1,1))

    def test_07_integration_reserved_then_provider_failure(self):
        _,rec,_=self._run_failure()
        a=rec[0]["acquisitions"][0]
        self.assertEqual((a["action"]["status"],a["action"]["reason"]),
                         ("PENDING","ACQUISITION_RESERVED"))
        self.assertEqual((a["dispatch"]["status"],a["dispatch"]["reason"]),
                         ("UNRESOLVED","PROVIDER_FAILURE"))

    def test_08_reason_propagates_to_loop_status(self):
        _,rec,_=self._run_failure()
        self.assertEqual(rec[0]["status"],"UNRESOLVED_ACQUISITION_PROVIDER_FAILURE")

    def test_09_failure_no_retry(self):
        _,rec,arr=self._run_failure()
        self.assertEqual((rec[0]["decision_charges"],len(rec[0]["phases"])),(1,1))
        self.assertTrue(np.all(arr["necessity_predictions"][0,1:]==-1))

    def test_10_failure_resources_exact(self):
        _,rec,_=self._run_failure()
        f=rec[0]["final"]["features"]
        self.assertEqual((f[62],f[63],f[64],f[67],f[70],f[71]),(9,3,1,1,0,11))

    def test_11_failure_no_receipt_or_fact_mutation(self):
        _,rec,_=self._run_failure()
        self.assertEqual(rec[0]["receipts"],[])
        self.assertEqual(rec[0]["initial"]["features"][46:62],rec[0]["final"]["features"][46:62])

    def test_12_score_failure_accepts_integration_record(self):
        _,rec,_=self._run_failure()
        s=c197.score_failure(rec[0],1,0,rec[0]["initial"]["features"])
        self.assertEqual(s["failed"],0)

    def test_13_score_rejects_wrong_status(self):
        _,rec,_=self._run_failure()
        rec[0]["status"]="UNRESOLVED_ACQUISITION_ACQUISITION_RESERVED"
        s=c197.score_failure(rec[0],1,0,rec[0]["initial"]["features"])
        self.assertEqual((s["status_error"],s["failed"]),(1,1))

    def test_14_score_rejects_wrong_provider_count(self):
        _,rec,_=self._run_failure()
        rec[0]["acquisitions"][0]["dispatch"]["provider_calls"]=0
        s=c197.score_failure(rec[0],1,0,rec[0]["initial"]["features"])
        self.assertEqual((s["provider_call_error"],s["failed"]),(1,1))

    def test_15_score_rejects_publication(self):
        _,rec,_=self._run_failure()
        rec[0]["acquisitions"][0]["dispatch"]["fact_publications"]=1
        s=c197.score_failure(rec[0],1,0,rec[0]["initial"]["features"])
        self.assertEqual((s["publication_error"],s["failed"]),(1,1))

    def test_16_gate_accepts(self):
        self.assertTrue(c197.gate(good_allowed(),good_failure()))

    def test_17_gate_requires_nine(self):
        self.assertFalse(c197.gate(good_allowed()[:-1],good_failure()))

    def test_18_gate_rejects_allowed_replay_error(self):
        a=good_allowed();f=good_failure();a[0]["reference_replay_error"]=1
        self.assertFalse(c197.gate(a,f))

    def test_19_gate_rejects_failure_error(self):
        a=good_allowed();f=good_failure()
        f[0]["provider_failure_error"]=f[0]["failed"]=1
        self.assertFalse(c197.gate(a,f))

    def test_20_gate_requires_provider_calls(self):
        a=good_allowed();f=good_failure();f[0]["provider_calls"]-=1
        self.assertFalse(c197.gate(a,f))

    def test_21_gate_requires_adapter_calls(self):
        a=good_allowed();f=good_failure();f[0]["adapter_calls"]-=1
        self.assertFalse(c197.gate(a,f))

    def test_22_gate_rejects_retry(self):
        a=good_allowed();f=good_failure();f[0]["retries"]=1
        self.assertFalse(c197.gate(a,f))

    def test_23_wrapper_reuses_c196_loop(self):
        source=inspect.getsource(c197.run_loop_reason_aware)
        self.assertIn("c196.run_loop_result_aware(",source)
        self.assertIn('initial,"ALLOWED"',source)

    def test_24_only_reason_rule_is_added(self):
        source=inspect.getsource(c197.run_loop_reason_aware)
        self.assertIn('dispatch.get("reason")',source)
        self.assertIn('else action.get("reason")',source)
        self.assertIn('rec["status"]="UNRESOLVED_ACQUISITION_"+str(reason)',source)

if __name__=="__main__":
    unittest.main(verbosity=2)
