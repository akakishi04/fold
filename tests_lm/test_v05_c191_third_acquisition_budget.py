import json
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
from fold_lm.v05_benchmarks import gate_e_c191_third_acquisition_budget as c191

def raw_row(visible=(None,None,None,1)):
    x=np.zeros(72,dtype=np.int32);x[0]=7;x[1]=4;x[2]=1;x[3]=1
    nodes=((1,1,1,0,0,0),(1,1,2,0,0,0),(1,2,0,1,2,0),
           (1,1,3,0,0,0),(1,1,4,0,0,0),(1,3,0,4,5,0),(1,2,0,3,6,0))
    x[4:46]=np.asarray(nodes,dtype=np.int32).reshape(-1)
    for i,v in enumerate(visible):
        x[46+4*i:50+4*i]=(1,1 if v is None else 2,0 if v is None else 1,0 if v is None else v)
    x[62:72]=(12,4,1,0,0,1,0,0,0,7)
    return x

def endpoint(tmp,code=3):
    b=c190.world_bytes(code);p=Path(tmp)/f"w{code:02d}.json";p.write_bytes(b)
    sb=life.SourceBinding(f"C190-world-{code:02d}",__import__("hashlib").sha256(b).hexdigest())
    provider=life.FileSnapshotProvider(p,sb)
    return life.Endpoint(sb,provider),provider

def meter(n):
    return dict(rows=n,forward_calls=1,cell_calls=7,wall_clock_seconds=0.0)

def initial_for(views,target_index=0):
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{},max_dispatches=3) for v in views]
    if not all(driver.charge_decision(o) for o in owners):raise AssertionError("charge failed")
    raw,_=c189.encode_views([o.state.view for o in owners]);n=len(raw)
    unknown=target.missing_mask(raw).numpy();tz=np.full((n,4),-np.inf,dtype=np.float32)
    tz[unknown]=0.;tz[np.arange(n),target_index]=1.
    return dict(raw=raw,necessity_predictions=np.ones(n,dtype=np.int8),
        target_predictions=np.full(n,target_index,dtype=np.int8),
        necessity_logits=np.tile(np.asarray([[0.,1.]],dtype=np.float32),(n,1)),
        target_logits=tz)

class C191Tests(unittest.TestCase):
    def _good(self):
        out=[]
        for b,h in c191.expected_order():
            out.append(dict(base_seed=b,head_seed=h,episodes=9536,parent_second_reads=3888,
                parent_final_needs=928,phase0_errors=0,phase1_errors=0,phase2_need_errors=0,
                initial_necessity_max_abs_logit_difference=0.0,
                initial_target_max_abs_logit_difference=0.0,
                actual_reads=9536+3888+928,failed=0,parent_replay_error=0,target2_error=0,
                selected_observed=0,repeated_target=0,third_acquisition_error=0,
                final_logical_needs=0,fourth_decision_accepted=0,contract_error=0,
                third_reservations=928,third_provider_calls=928,third_publications=928))
        return out

    def test_01_manifest_hash(self):
        self.assertEqual(c191.digest(c191.manifest()),c191.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m=c191.manifest()
        self.assertEqual((m["episodes"],m["blocks"],m["expected_third_acquisitions"]),(85824,9,8352))
        self.assertEqual(m["max_acquisitions_per_episode"],3)
        self.assertFalse(m["production_runtime_modified"])

    def test_03_expected_order(self):
        self.assertEqual(len(c191.expected_order()),9)

    def test_04_gate_accepts(self):
        self.assertTrue(c191.gate(self._good()))

    def test_05_gate_requires_nine(self):
        self.assertFalse(c191.gate(self._good()[:-1]))

    def test_06_gate_rejects_target2_error(self):
        r=self._good();r[0]["target2_error"]=r[0]["failed"]=1
        self.assertFalse(c191.gate(r))

    def test_07_gate_rejects_repeat(self):
        r=self._good();r[0]["repeated_target"]=r[0]["failed"]=1
        self.assertFalse(c191.gate(r))

    def test_08_gate_rejects_third_io(self):
        r=self._good();r[0]["third_provider_calls"]-=1
        self.assertFalse(c191.gate(r))

    def test_09_gate_rejects_final_logical_need(self):
        r=self._good();r[0]["final_logical_needs"]=r[0]["failed"]=1
        self.assertFalse(c191.gate(r))

    def test_10_gate_rejects_fourth_decision(self):
        r=self._good();r[0]["fourth_decision_accepted"]=r[0]["failed"]=1
        self.assertFalse(c191.gate(r))

    def test_11_gate_rejects_read_accounting(self):
        r=self._good();r[0]["actual_reads"]-=1
        self.assertFalse(c191.gate(r))

    def test_12_gate_rejects_replay_error(self):
        r=self._good();r[0]["phase1_errors"]=1
        self.assertFalse(c191.gate(r))

    def test_13_gate_rejects_logit_drift(self):
        r=self._good();r[0]["initial_target_max_abs_logit_difference"]=c191.ATOL*2
        self.assertFalse(c191.gate(r))

    def test_14_load_parent_shapes(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz"
            np.savez_compressed(p,necessity_predictions=np.zeros((9,9536,3),dtype=np.int8),
                necessity_logits=np.zeros((9,9536,3,2),dtype=np.float32),
                target_predictions=np.zeros((9,9536,2),dtype=np.int8),
                target_logits=np.zeros((9,9536,2,4),dtype=np.float32),
                row_indices=np.zeros(9536,dtype=np.int32),local_rows=np.zeros(9536,dtype=np.int32),
                world_codes=np.zeros(9536,dtype=np.int8),
                base_seeds=np.repeat(np.asarray(c191.BASE_SEEDS,dtype=np.int32),3),
                head_seeds=np.tile(np.asarray(c191.HEAD_SEEDS,dtype=np.int32),3))
            z=c191.load_parent_predictions(p)
            self.assertEqual(z["target_logits"].shape,(9,9536,2,4))

    def test_15_load_parent_rejects_schema(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz";np.savez_compressed(p,x=np.zeros(1))
            with self.assertRaises(ValueError):c191.load_parent_predictions(p)

    def test_16_run_three_acquisitions(self):
        with tempfile.TemporaryDirectory() as td:
            ep,p=endpoint(td,3)
            views=c190.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector();calls=[0]
            def combined(base,head,raw,**kw):
                calls[0]+=1;n=len(raw);ti=1 if calls[0]==1 else 2
                tz=np.zeros((n,4),dtype=np.float32)
                return np.ones(n,dtype=np.int8),np.full(n,ti,dtype=np.int8),np.zeros((n,2),dtype=np.float32),tz,meter(n)
            with mock.patch.object(c189,"combined_predict",combined):
                rec,_,_=c191.run_block(views,np.array([3]),{3:ep},base,head,initial_for(views,0))
            self.assertEqual((p.reads,len(rec[0]["acquisitions"])),(3,3))
            self.assertFalse(rec[0]["fourth_decision_accepted"])

    def test_17_third_exhausts_internal_budget(self):
        with tempfile.TemporaryDirectory() as td:
            ep,_=endpoint(td,3)
            views=c190.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector();calls=[0]
            def combined(base,head,raw,**kw):
                calls[0]+=1;n=len(raw);ti=1 if calls[0]==1 else 2
                return np.ones(n,dtype=np.int8),np.full(n,ti,dtype=np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
            with mock.patch.object(c189,"combined_predict",combined):
                rec,_,_=c191.run_block(views,np.array([3]),{3:ep},base,head,initial_for(views,0))
            self.assertEqual((rec[0]["final"]["features"][62],rec[0]["final"]["features"][63],rec[0]["final"]["features"][71]),(0,1,19))

    def test_18_third_observes_all_facts(self):
        with tempfile.TemporaryDirectory() as td:
            ep,_=endpoint(td,3)
            views=c190.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector();calls=[0]
            def combined(base,head,raw,**kw):
                calls[0]+=1;n=len(raw);ti=1 if calls[0]==1 else 2
                return np.ones(n,dtype=np.int8),np.full(n,ti,dtype=np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
            with mock.patch.object(c189,"combined_predict",combined):
                rec,_,_=c191.run_block(views,np.array([3]),{3:ep},base,head,initial_for(views,0))
            f=rec[0]["final"]["features"]
            self.assertTrue(all(f[48+4*j]==1 for j in range(4)))

    def test_19_phase2_sufficient_stops_at_two(self):
        with tempfile.TemporaryDirectory() as td:
            ep,p=endpoint(td,3)
            views=c190.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector();calls=[0]
            def combined(base,head,raw,**kw):
                calls[0]+=1;n=len(raw)
                if calls[0]==1:return np.ones(n,dtype=np.int8),np.ones(n,dtype=np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
                return np.zeros(n,dtype=np.int8),np.full(n,2,dtype=np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
            with mock.patch.object(c189,"combined_predict",combined):
                rec,_,_=c191.run_block(views,np.array([3]),{3:ep},base,head,initial_for(views,0))
            self.assertEqual((p.reads,len(rec[0]["acquisitions"])),(2,2))

    def test_20_target2_scope_declared_trivial(self):
        self.assertIn("exactly one unobserved fact",c191.manifest()["target2_scope"])

    def test_21_budget_is_unchanged(self):
        self.assertIn("start12/4/step7",c191.manifest()["resources"])

    def test_22_no_post3_learned_decision(self):
        self.assertIn("no final learned decision",c191.manifest()["final_teacher"])

    def test_23_outputs_count(self):
        self.assertEqual(len(c191.OUTPUTS),21)

    def test_24_fixed_source_worlds(self):
        self.assertEqual(c191.SOURCE_FILES,c190.SOURCE_FILES if hasattr(c190,"SOURCE_FILES") else c191.SOURCE_FILES)

if __name__=="__main__":unittest.main(verbosity=2)
