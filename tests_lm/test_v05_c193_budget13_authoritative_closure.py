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
from fold_lm.v05_benchmarks import gate_e_c193_budget13_authoritative_closure as c193

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

def raw_row12():
    x=raw_row13();x[62]=12;return x

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
    for b,h in c193.expected_order():
        first=9536;second=3900;third=928
        rows.append(dict(base_seed=b,head_seed=h,episodes=9536,actual_reads=first+second+third,
            failed=0,necessity_error=0,target_error=0,selected_observed=0,repeated_target=0,
            acquisition_error=0,contract_error=0,first_reads=first,second_reads=second,
            third_reads=third,final_decision_rows=third,final_decision_error=0))
    return rows

class C193Tests(unittest.TestCase):
    def test_01_manifest_hash(self):
        self.assertEqual(c193.digest(c193.manifest()),c193.MANIFEST_SHA)

    def test_02_manifest_scope(self):
        m=c193.manifest()
        self.assertEqual((m["episodes"],m["blocks"],m["selectors"]),(85824,9,9))
        self.assertEqual(m["changed"],"TaskView internal_remaining initial coordinate 12->13 only")

    def test_03_outputs_exact(self):
        self.assertEqual(len(c193.OUTPUTS),4)

    def test_04_expected_order(self):
        self.assertEqual(len(c193.expected_order()),9)

    def test_05_budget13_only_coordinate62(self):
        raw=torch.from_numpy(np.stack([raw_row12(),raw_row12()]))
        out=c193.budget13(raw)
        diff=torch.nonzero(out!=raw,as_tuple=False)
        self.assertEqual(diff[:,1].tolist(),[62,62])
        self.assertEqual(out[:,62].tolist(),[13,13])

    def test_06_budget13_does_not_mutate_input(self):
        raw=torch.from_numpy(np.stack([raw_row12()]))
        before=raw.clone();_ = c193.budget13(raw)
        self.assertTrue(torch.equal(raw,before))

    def test_07_budget13_rejects_non12(self):
        raw=torch.from_numpy(np.stack([raw_row13()]))
        with self.assertRaises(ValueError): c193.budget13(raw)

    def test_08_initial_cache_charges_to12(self):
        raw=torch.from_numpy(np.stack([raw_row13()]))
        base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
        def combined(base,head,raw,**kw):
            n=len(raw);return np.ones(n,np.int8),np.zeros(n,np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
        with mock.patch.object(c189,"combined_predict",combined):
            cache,_=c193.initial_policy_cache(raw,np.array([0]),base,head)
        self.assertEqual((int(cache["raw"][0,62]),int(cache["raw"][0,71])),(12,8))

    def test_09_run_three_acquisitions_and_final_decision(self):
        with tempfile.TemporaryDirectory() as td:
            ep,p=endpoint(td,3)
            raw=torch.from_numpy(np.stack([raw_row13()]))
            views=c190.make_views(raw,np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector();calls=[0]
            def combined(base,head,raw,**kw):
                calls[0]+=1;n=len(raw);ti=1 if calls[0]==1 else 2
                return np.ones(n,np.int8),np.full(n,ti,np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
            final=lambda base,raw,**kw:(np.zeros(len(raw),np.int8),np.zeros((len(raw),2),np.float32),meter(len(raw)))
            with mock.patch.object(c189,"combined_predict",combined),mock.patch.object(c189,"necessity_predict",final):
                rec,_,_=c193.run_block(views,np.array([3]),{3:ep},base,head,initial_for(views,0))
            self.assertEqual((p.reads,len(rec[0]["acquisitions"]),len(rec[0]["phases"])),(3,3,4))
            self.assertEqual(rec[0]["status"],"SUFFICIENT_CLASSIFICATION")

    def test_10_final_resources_exact(self):
        with tempfile.TemporaryDirectory() as td:
            ep,_=endpoint(td,3);raw=torch.from_numpy(np.stack([raw_row13()]))
            views=c190.make_views(raw,np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector();calls=[0]
            def combined(base,head,raw,**kw):
                calls[0]+=1;n=len(raw);ti=1 if calls[0]==1 else 2
                return np.ones(n,np.int8),np.full(n,ti,np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
            final=lambda base,raw,**kw:(np.zeros(len(raw),np.int8),np.zeros((len(raw),2),np.float32),meter(len(raw)))
            with mock.patch.object(c189,"combined_predict",combined),mock.patch.object(c189,"necessity_predict",final):
                rec,_,_=c193.run_block(views,np.array([3]),{3:ep},base,head,initial_for(views,0))
            f=rec[0]["final"]["features"]
            self.assertEqual((f[62],f[63],f[71]),(0,1,20))

    def test_11_final_decision_is_charged(self):
        with tempfile.TemporaryDirectory() as td:
            ep,_=endpoint(td,3);raw=torch.from_numpy(np.stack([raw_row13()]))
            views=c190.make_views(raw,np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector();calls=[0]
            def combined(base,head,raw,**kw):
                calls[0]+=1;n=len(raw);ti=1 if calls[0]==1 else 2
                return np.ones(n,np.int8),np.full(n,ti,np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
            final=lambda base,raw,**kw:(np.zeros(len(raw),np.int8),np.zeros((len(raw),2),np.float32),meter(len(raw)))
            with mock.patch.object(c189,"combined_predict",combined),mock.patch.object(c189,"necessity_predict",final):
                rec,_,_=c193.run_block(views,np.array([3]),{3:ep},base,head,initial_for(views,0))
            self.assertEqual(rec[0]["decision_charges"],4)

    def test_12_gate_accepts(self):
        self.assertTrue(c193.gate(good_records()))

    def test_13_gate_requires_nine(self):
        self.assertFalse(c193.gate(good_records()[:-1]))

    def test_14_gate_rejects_necessity_error(self):
        r=good_records();r[0]["necessity_error"]=r[0]["failed"]=1
        self.assertFalse(c193.gate(r))

    def test_15_gate_rejects_target_error(self):
        r=good_records();r[0]["target_error"]=r[0]["failed"]=1
        self.assertFalse(c193.gate(r))

    def test_16_gate_rejects_acquisition_error(self):
        r=good_records();r[0]["acquisition_error"]=r[0]["failed"]=1
        self.assertFalse(c193.gate(r))

    def test_17_gate_rejects_final_error(self):
        r=good_records();r[0]["final_decision_error"]=r[0]["failed"]=1
        self.assertFalse(c193.gate(r))

    def test_18_gate_requires_third_coverage(self):
        r=good_records();r[0]["third_reads"]=r[0]["final_decision_rows"]=0;r[0]["actual_reads"]=r[0]["first_reads"]+r[0]["second_reads"]
        self.assertFalse(c193.gate(r))

    def test_19_gate_requires_final_equals_third(self):
        r=good_records();r[0]["final_decision_rows"]-=1
        self.assertFalse(c193.gate(r))

    def test_20_gate_read_accounting(self):
        r=good_records();r[0]["actual_reads"]+=1
        self.assertFalse(c193.gate(r))

    def test_21_resource_path_declared(self):
        self.assertIn("after3acq+4decisions0/1/20",c193.manifest()["resources"])

    def test_22_model_visibility_declared(self):
        self.assertIn("model-visible",c193.manifest()["model_visibility"])

    def test_23_no_parent_prediction_loader_dependency(self):
        source=inspect.getsource(c193.run)
        self.assertNotIn("load_parent_predictions",source)
        self.assertIn("source_dir=Path(parents[\"c191_summary\"])",source)

    def test_24_run_path_uses_budget13_for_unique_and_expanded(self):
        source=inspect.getsource(c193.run)
        self.assertIn("raw13=budget13(raw12)",source)
        self.assertIn("expanded13=budget13(expanded12)",source)

if __name__=="__main__": unittest.main(verbosity=2)
