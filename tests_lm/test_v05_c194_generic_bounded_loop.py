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
    if not all(driver.charge_decision(o) for o in owners): raise AssertionError("charge failed")
    raw,_=c189.encode_views([o.state.view for o in owners]);n=len(raw)
    unknown=target.missing_mask(raw).numpy()
    tz=np.full((n,4),-np.inf,dtype=np.float32);tz[unknown]=0.;tz[np.arange(n),target_index]=1.
    return dict(raw=raw,necessity_predictions=np.ones(n,dtype=np.int8),
        target_predictions=np.full(n,target_index,dtype=np.int8),
        necessity_logits=np.tile(np.asarray([[0.,1.]],dtype=np.float32),(n,1)),
        target_logits=tz)

def good_records():
    rows=[]
    for b,h in c194.expected_order():
        first=9536;second=3900;third=928
        rows.append(dict(base_seed=b,head_seed=h,episodes=9536,actual_reads=first+second+third,
            failed=0,necessity_error=0,target_error=0,selected_observed=0,repeated_target=0,
            acquisition_error=0,contract_error=0,first_reads=first,second_reads=second,
            third_reads=third,final_decision_rows=third,final_decision_error=0,
            parent_replay_error=0,parent_block_mismatch=0,
            parent_necessity_prediction_errors=0,parent_target_prediction_errors=0,
            parent_necessity_max_abs_logit_difference=0.0,
            parent_target_max_abs_logit_difference=0.0))
    return rows

class C194Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c194.digest(c194.manifest()),c194.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m=c194.manifest()
        self.assertEqual((m["episodes"],m["blocks"],m["selectors"]),(85824,9,9))
        self.assertIn("state-driven bounded loop",m["changed"])

    def test_03_derived_bound(self):
        self.assertEqual((c194.MAX_ACQUISITIONS,c194.MAX_DECISIONS),(3,4))

    def test_04_outputs_exact(self):
        self.assertEqual(len(c194.OUTPUTS),5)

    def test_05_expected_order(self):
        self.assertEqual(len(c194.expected_order()),9)

    def _run_three(self):
        td=tempfile.TemporaryDirectory()
        ep,p=endpoint(td.name,3)
        raw=torch.from_numpy(np.stack([raw_row13()]))
        views=c190.make_views(raw,np.array([0]),np.array([3]),"x")
        base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector();calls=[0]
        def combined(base,head,raw,**kw):
            calls[0]+=1;n=len(raw);ti=1 if calls[0]==1 else 2
            return np.ones(n,np.int8),np.full(n,ti,np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
        final=lambda base,raw,**kw:(np.zeros(len(raw),np.int8),np.zeros((len(raw),2),np.float32),meter(len(raw)))
        patches=(mock.patch.object(c189,"combined_predict",combined),mock.patch.object(c189,"necessity_predict",final))
        patches[0].start();patches[1].start()
        try:
            rec,arr,_=c194.run_loop(views,np.array([3]),{3:ep},base,head,initial_for(views,0))
        finally:
            patches[1].stop();patches[0].stop()
        return td,p,rec,arr

    def test_06_generic_loop_three_acquisitions(self):
        td,p,rec,_=self._run_three()
        try:self.assertEqual((p.reads,len(rec[0]["acquisitions"])),(3,3))
        finally:td.cleanup()

    def test_07_generic_loop_four_decisions(self):
        td,_,rec,_=self._run_three()
        try:self.assertEqual((rec[0]["decision_charges"],len(rec[0]["phases"])),(4,4))
        finally:td.cleanup()

    def test_08_generic_loop_final_sufficient(self):
        td,_,rec,_=self._run_three()
        try:self.assertEqual(rec[0]["status"],"SUFFICIENT_CLASSIFICATION")
        finally:td.cleanup()

    def test_09_generic_loop_final_resources(self):
        td,_,rec,_=self._run_three()
        try:
            f=rec[0]["final"]["features"]
            self.assertEqual((f[62],f[63],f[71]),(0,1,20))
        finally:td.cleanup()

    def test_10_arrays_match_parent_shapes(self):
        td,_,_,arr=self._run_three()
        try:
            self.assertEqual(arr["necessity_predictions"].shape,(1,4))
            self.assertEqual(arr["target_predictions"].shape,(1,3))
        finally:td.cleanup()

    def test_11_loop_source_has_no_phase1_branch(self):
        source=inspect.getsource(c194.run_loop)
        self.assertNotIn("phase1",source)
        self.assertNotIn("phase2",source)
        self.assertNotIn("phase3",source)

    def test_12_loop_target_mode_is_state_driven(self):
        source=inspect.getsource(c194.run_loop)
        self.assertIn("any_missing=any(",source)
        self.assertIn("elif any_missing:",source)

    def test_13_gate_accepts(self):
        self.assertTrue(c194.gate(good_records()))

    def test_14_gate_requires_nine(self):
        self.assertFalse(c194.gate(good_records()[:-1]))

    def test_15_gate_rejects_parent_replay(self):
        r=good_records();r[0]["parent_replay_error"]=r[0]["failed"]=1
        self.assertFalse(c194.gate(r))

    def test_16_gate_rejects_parent_block_mismatch(self):
        r=good_records();r[0]["parent_block_mismatch"]=r[0]["failed"]=1
        self.assertFalse(c194.gate(r))

    def test_17_gate_rejects_prediction_error(self):
        r=good_records();r[0]["parent_necessity_prediction_errors"]=1
        self.assertFalse(c194.gate(r))

    def test_18_gate_rejects_logit_drift(self):
        r=good_records();r[0]["parent_target_max_abs_logit_difference"]=2*c194.ATOL
        self.assertFalse(c194.gate(r))

    def test_19_gate_rejects_scientific_error(self):
        r=good_records();r[0]["necessity_error"]=r[0]["failed"]=1
        self.assertFalse(c194.gate(r))

    def test_20_gate_read_accounting(self):
        r=good_records();r[0]["actual_reads"]+=1
        self.assertFalse(c194.gate(r))

    def test_21_parent_replay_metrics_exact(self):
        arr=dict(necessity_predictions=np.zeros((2,4),np.int8),
                 necessity_logits=np.zeros((2,4,2),np.float32),
                 target_predictions=np.zeros((2,3),np.int8),
                 target_logits=np.zeros((2,3,4),np.float32))
        m=c194.parent_replay_metrics(arr,arr)
        self.assertEqual(m,dict(necessity_prediction_errors=0,target_prediction_errors=0,
            necessity_max_abs_logit_difference=0.0,target_max_abs_logit_difference=0.0))

    def _write_parent(self,p):
        np.savez_compressed(p,
            necessity_predictions=np.zeros((9,9536,4),dtype=np.int8),
            necessity_logits=np.zeros((9,9536,4,2),dtype=np.float32),
            target_predictions=np.zeros((9,9536,3),dtype=np.int8),
            target_logits=np.zeros((9,9536,3,4),dtype=np.float32),
            row_indices=np.zeros(9536,dtype=np.int32),
            local_rows=np.zeros(9536,dtype=np.int32),
            world_codes=np.zeros(9536,dtype=np.int8))

    def test_22_parent_loader_shapes(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz";self._write_parent(p)
            z=c194.load_parent_predictions(p)
            self.assertEqual(z["necessity_logits"].shape,(9,9536,4,2))

    def test_23_parent_loader_rejects_schema(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz";np.savez_compressed(p,x=np.zeros(1))
            with self.assertRaises(ValueError):c194.load_parent_predictions(p)

    def test_24_run_uses_child_parent_loader(self):
        source=inspect.getsource(c194.run)
        self.assertIn('saved=load_parent_predictions(',source)
        self.assertNotIn('saved=parent.load_parent_predictions(',source)
        self.assertLess(source.index("block_mismatch=int"),source.index("trace.write("))

if __name__=="__main__":
    unittest.main(verbosity=2)
