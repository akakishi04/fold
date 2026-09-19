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
from fold_lm.v05_benchmarks import gate_e_c194_generic_bounded_loop as c194
from fold_lm.v05_benchmarks import gate_e_c195_generic_loop_budget12_exhaustion as c195

def raw_row12():
    x=np.zeros(72,dtype=np.int32);x[0]=7;x[1]=4;x[2]=1;x[3]=1
    nodes=((1,1,1,0,0,0),(1,1,2,0,0,0),(1,2,0,1,2,0),
           (1,1,3,0,0,0),(1,1,4,0,0,0),(1,3,0,4,5,0),(1,2,0,3,6,0))
    x[4:46]=np.asarray(nodes,dtype=np.int32).reshape(-1)
    vis=(None,None,None,1)
    for i,v in enumerate(vis):
        x[46+4*i:50+4*i]=(1,1 if v is None else 2,0 if v is None else 1,0 if v is None else v)
    x[62:72]=(12,4,1,0,0,1,0,0,0,7)
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
    if not all(driver.charge_decision(o) for o in owners): raise AssertionError("charge failed")
    raw,_=c189.encode_views([o.state.view for o in owners]);n=len(raw)
    unknown=target.missing_mask(raw).numpy()
    tz=np.full((n,4),-np.inf,dtype=np.float32);tz[unknown]=0.;tz[np.arange(n),target_index]=1.
    return dict(raw=raw,necessity_predictions=np.ones(n,dtype=np.int8),
        target_predictions=np.full(n,target_index,dtype=np.int8),
        necessity_logits=np.tile(np.asarray([[0.,1.]],dtype=np.float32),(n,1)),
        target_logits=tz)

def three_need_reference():
    return dict(
        necessity_predictions=np.asarray([1,1,1],dtype=np.int8),
        necessity_logits=np.zeros((3,2),dtype=np.float32),
        target_predictions=np.asarray([0,1,2],dtype=np.int8),
        target_logits=np.zeros((3,4),dtype=np.float32))

def good_records():
    rows=[]
    for b,h in c195.expected_order():
        rows.append(dict(base_seed=b,head_seed=h,episodes=9536,actual_reads=14352,
            reference_exhausted_rows=928,failed=0,reference_replay_error=0,
            reference_block_mismatch=0,acquisition_contract_error=0,status_error=0,
            resource_error=0,final_logical_error=0,fake_final_decision=0,
            first_reads=9536,second_reads=3888,third_reads=928,exhausted_rows=928,
            sufficient_rows=8608,reference_necessity_prediction_errors=0,
            reference_target_prediction_errors=0,reference_unauthorized_final_predictions=0,
            reference_necessity_max_abs_logit_difference=0.0,
            reference_target_max_abs_logit_difference=0.0))
    return rows

class C195Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c195.digest(c195.manifest()),c195.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m=c195.manifest()
        self.assertEqual((m["episodes"],m["blocks"],m["selectors"]),(85824,9,9))
        self.assertIn("13->12",m["changed"])

    def test_03_outputs_exact(self):
        self.assertEqual(len(c195.OUTPUTS),5)

    def test_04_expected_order(self):
        self.assertEqual(len(c195.expected_order()),9)

    def _run_three(self):
        td=tempfile.TemporaryDirectory()
        ep,p=endpoint(td.name,3)
        raw=torch.from_numpy(np.stack([raw_row12()]))
        views=c190.make_views(raw,np.array([0]),np.array([3]),"x")
        base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector();calls=[0]
        def combined(base,head,raw,**kw):
            calls[0]+=1;n=len(raw);ti=1 if calls[0]==1 else 2
            return np.ones(n,np.int8),np.full(n,ti,np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
        with mock.patch.object(c189,"combined_predict",combined):
            rec,arr,_=c194.run_loop(views,np.array([3]),{3:ep},base,head,initial_for(views,0))
        return td,p,rec,arr

    def test_05_budget12_three_acquisitions(self):
        td,p,rec,_=self._run_three()
        try:self.assertEqual((p.reads,len(rec[0]["acquisitions"])),(3,3))
        finally:td.cleanup()

    def test_06_fourth_debit_refused(self):
        td,_,rec,_=self._run_three()
        try:self.assertEqual((rec[0]["decision_charges"],len(rec[0]["phases"])),(3,3))
        finally:td.cleanup()

    def test_07_exhausted_status(self):
        td,_,rec,_=self._run_three()
        try:self.assertEqual(rec[0]["status"],"BUDGET_EXHAUSTED")
        finally:td.cleanup()

    def test_08_exhausted_resources_exact(self):
        td,_,rec,_=self._run_three()
        try:
            f=rec[0]["final"]["features"]
            self.assertEqual((f[62],f[63],f[71]),(0,1,19))
        finally:td.cleanup()

    def test_09_no_unauthorized_phase3_prediction(self):
        td,_,_,arr=self._run_three()
        try:self.assertEqual(arr["necessity_predictions"][0,3],-1)
        finally:td.cleanup()

    def test_10_earlier_sufficient_still_stops(self):
        with tempfile.TemporaryDirectory() as td:
            ep,p=endpoint(td,3)
            raw=torch.from_numpy(np.stack([raw_row12()]))
            views=c190.make_views(raw,np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
            def combined(base,head,raw,**kw):
                n=len(raw)
                return np.zeros(n,np.int8),np.ones(n,np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
            with mock.patch.object(c189,"combined_predict",combined):
                rec,_,_=c194.run_loop(views,np.array([3]),{3:ep},base,head,initial_for(views,0))
            self.assertEqual((p.reads,len(rec[0]["acquisitions"]),rec[0]["status"]),
                             (1,1,"SUFFICIENT_CLASSIFICATION"))

    def test_11_reference_replay_exact(self):
        td,_,_,arr=self._run_three()
        try:
            ref=three_need_reference()
            m=c195.reference_replay_metrics(arr,ref)
            self.assertEqual(m["necessity_prediction_errors"],0)
            self.assertEqual(m["target_prediction_errors"],0)
            self.assertEqual(m["unauthorized_final_predictions"],0)
        finally:td.cleanup()

    def test_12_replay_detects_unauthorized_final(self):
        td,_,_,arr=self._run_three()
        try:
            arr["necessity_predictions"][0,3]=0
            m=c195.reference_replay_metrics(arr,three_need_reference())
            self.assertEqual(m["unauthorized_final_predictions"],1)
        finally:td.cleanup()

    def test_13_gate_accepts(self):
        self.assertTrue(c195.gate(good_records()))

    def test_14_gate_requires_nine(self):
        self.assertFalse(c195.gate(good_records()[:-1]))

    def test_15_gate_rejects_fake_final(self):
        r=good_records();r[0]["fake_final_decision"]=r[0]["failed"]=1
        self.assertFalse(c195.gate(r))

    def test_16_gate_rejects_resource_error(self):
        r=good_records();r[0]["resource_error"]=r[0]["failed"]=1
        self.assertFalse(c195.gate(r))

    def test_17_gate_requires_928_exhausted(self):
        r=good_records();r[0]["exhausted_rows"]=927
        self.assertFalse(c195.gate(r))

    def test_18_gate_rejects_reference_prediction_error(self):
        r=good_records();r[0]["reference_target_prediction_errors"]=1
        self.assertFalse(c195.gate(r))

    def test_19_gate_rejects_logit_drift(self):
        r=good_records();r[0]["reference_necessity_max_abs_logit_difference"]=2*c195.ATOL
        self.assertFalse(c195.gate(r))

    def test_20_gate_read_accounting(self):
        r=good_records();r[0]["actual_reads"]+=1
        self.assertFalse(c195.gate(r))

    def _write_reference(self,p):
        np.savez_compressed(p,
            necessity_predictions=np.zeros((9,9536,3),dtype=np.int8),
            necessity_logits=np.zeros((9,9536,3,2),dtype=np.float32),
            target_predictions=np.zeros((9,9536,3),dtype=np.int8),
            target_logits=np.zeros((9,9536,3,4),dtype=np.float32),
            row_indices=np.zeros(9536,dtype=np.int32),
            local_rows=np.zeros(9536,dtype=np.int32),
            world_codes=np.zeros(9536,dtype=np.int8))

    def test_21_reference_loader_shapes(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz";self._write_reference(p)
            z=c195.load_reference_predictions(p)
            self.assertEqual(z["necessity_logits"].shape,(9,9536,3,2))

    def test_22_reference_loader_rejects_schema(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz";np.savez_compressed(p,x=np.zeros(1))
            with self.assertRaises(ValueError):c195.load_reference_predictions(p)

    def test_23_run_reuses_generic_loop(self):
        source=inspect.getsource(c195.run)
        self.assertIn("parent.run_loop(",source)
        self.assertNotIn("def run_loop",source)

    def test_24_run_uses_child_reference_loader(self):
        source=inspect.getsource(c195.run)
        self.assertIn('saved=load_reference_predictions(',source)
        self.assertNotIn('reference.load_parent_predictions(',source)
        self.assertLess(source.index("block_mismatch=int"),source.index("trace.write("))

if __name__=="__main__":
    unittest.main(verbosity=2)
