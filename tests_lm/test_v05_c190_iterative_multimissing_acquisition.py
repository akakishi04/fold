import inspect
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
from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as parent
from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190

def raw_row(visible=(None,0,None,1)):
    x=np.zeros(72,dtype=np.int32);x[0]=7;x[1]=4;x[2]=1;x[3]=1
    nodes=((1,1,1,0,0,0),(1,1,2,0,0,0),(1,2,0,1,2,0),
           (1,1,3,0,0,0),(1,1,4,0,0,0),(1,3,0,4,5,0),(1,2,0,3,6,0))
    x[4:46]=np.asarray(nodes,dtype=np.int32).reshape(-1)
    for i,v in enumerate(visible):
        x[46+4*i:50+4*i]=(1,1 if v is None else 2,0 if v is None else 1,0 if v is None else v)
    x[62:72]=(12,4,1,0,0,1,0,0,0,7)
    return x

def endpoint(tmp,code):
    b=c190.world_bytes(code);p=Path(tmp)/f"w{code:02d}.json";p.write_bytes(b)
    sb=life.SourceBinding(f"C190-world-{code:02d}",__import__("hashlib").sha256(b).hexdigest())
    provider=life.FileSnapshotProvider(p,sb)
    return life.Endpoint(sb,provider),provider

def meter(n):
    return dict(rows=n,forward_calls=1,cell_calls=7,wall_clock_seconds=0.0)

def cached_initial(views,target_index=0):
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{},max_dispatches=2) for v in views]
    self_charge=[driver.charge_decision(o) for o in owners]
    if not all(self_charge):
        raise AssertionError("decision debit failed")
    raw,_=parent.encode_views([o.state.view for o in owners])
    n=len(raw)
    unknown=target.missing_mask(raw).numpy()
    tz=np.full((n,4),-np.inf,dtype=np.float32)
    tz[unknown]=0.0
    tz[np.arange(n),target_index]=1.0
    return dict(raw=raw,
        necessity_predictions=np.ones(n,dtype=np.int8),
        target_predictions=np.full(n,target_index,dtype=np.int8),
        necessity_logits=np.tile(np.asarray([[0.,1.]],dtype=np.float32),(n,1)),
        target_logits=tz)

class C190Tests(unittest.TestCase):
    def test_01_world_count(self):
        self.assertEqual(len(c190.WORLD_BITS),16)

    def test_02_world_zero_records_all_facts(self):
        p=json.loads(c190.world_bytes(0))
        self.assertEqual(len(p["records"]),4)
        self.assertEqual([r["fact_id"] for r in p["records"]],list(driver.FACT_IDS))
        self.assertEqual([r["value"] for r in p["records"]],[0,0,0,0])

    def test_03_world_fifteen_records_ones(self):
        p=json.loads(c190.world_bytes(15))
        self.assertEqual([r["value"] for r in p["records"]],[1,1,1,1])

    def test_04_world_code_rejects_bool(self):
        with self.assertRaises(ValueError): c190.world_bytes(True)

    def test_05_world_code_rejects_range(self):
        for code in (-1,16):
            with self.assertRaises(ValueError): c190.world_bytes(code)

    def test_06_consistent_worlds_missing2(self):
        self.assertEqual(len(c190.consistent_worlds(raw_row())),4)

    def test_07_consistent_worlds_missing3(self):
        self.assertEqual(len(c190.consistent_worlds(raw_row((None,None,None,1)))),8)

    def test_08_consistent_worlds_preserve_visible(self):
        for code in c190.consistent_worlds(raw_row((None,0,None,1))):
            self.assertEqual(c190.WORLD_BITS[code][1],0)
            self.assertEqual(c190.WORLD_BITS[code][3],1)

    def test_09_expand_registered_counts(self):
        rows=np.stack([raw_row() for _ in range(1152)]+
                      [raw_row((None,None,None,1)) for _ in range(616)])
        out,s,l,c=c190.expand_worlds(torch.from_numpy(rows),np.arange(1768))
        self.assertEqual((len(out),int((c>=0).sum())),(9536,9536))
        self.assertEqual(len(np.unique(l)),1768)

    def test_10_make_views_preserves_epoch_and_world_hidden(self):
        raw=torch.from_numpy(np.stack([raw_row()]))
        v=c190.make_views(raw,np.array([7]),np.array([3],dtype=np.int8),"x")[0]
        self.assertEqual((v.evidence_time,v.revision),(1,1))
        self.assertEqual(sum(f.status=="UNOBSERVED" for f in v.facts),2)

    def _parent_npz(self,path,bit_equal=True):
        n=np.ones((9,2,1768,2),dtype=np.int8)
        if not bit_equal:n[:,1,:,0]=0
        np.savez_compressed(path,
            necessity_predictions=n,necessity_logits=np.zeros((9,2,1768,2,2),dtype=np.float32),
            target_predictions=np.zeros((9,2,1768),dtype=np.int8),
            target_logits=np.zeros((9,2,1768,4),dtype=np.float32),
            post_labels=np.zeros((9,2,1768),dtype=np.int8),
            row_indices=np.arange(1768,dtype=np.int32),
            base_seeds=np.repeat(np.asarray(c190.BASE_SEEDS,dtype=np.int32),3),
            head_seeds=np.tile(np.asarray(c190.HEAD_SEEDS,dtype=np.int32),3))

    def test_11_parent_loader_shape(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz";self._parent_npz(p)
            z=c190.load_parent_predictions(p)
            self.assertEqual(z["target_logits"].shape,(9,2,1768,4))

    def test_12_parent_loader_rejects_bit_dependent_initial(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz";self._parent_npz(p,False)
            with self.assertRaises(ValueError):c190.load_parent_predictions(p)

    def test_13_initial_policy_cache_unique_rows(self):
        raw=torch.from_numpy(np.stack([raw_row(),raw_row((None,None,None,1))]))
        base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
        cache,m=c190.initial_policy_cache(raw,np.array([7,8]),base,head)
        self.assertEqual(cache["raw"].shape,(2,72))
        self.assertEqual(cache["raw"][:,62].tolist(),[11,11])
        self.assertEqual(cache["raw"][:,71].tolist(),[8,8])
        self.assertEqual(m["rows"],2)

    def test_14_first_acquisition_real_io(self):
        with tempfile.TemporaryDirectory() as td:
            ep,p=endpoint(td,3)
            v=c190.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),np.array([3]),"x")[0]
            o=life.AcquisitionOwner(action.RuntimeState(v),{"RETRIEVE":ep},max_dispatches=2)
            self.assertTrue(driver.charge_decision(o))
            a=c190.acquire(o,0)
            self.assertEqual((a["dispatch"]["status"],p.reads,o.state.view.facts[0].value),("PUBLISHED",1,0))

    def test_15_second_acquisition_same_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            ep,p=endpoint(td,3)
            v=c190.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),np.array([3]),"x")[0]
            o=life.AcquisitionOwner(action.RuntimeState(v),{"RETRIEVE":ep},max_dispatches=2)
            driver.charge_decision(o);c190.acquire(o,0);driver.charge_decision(o);c190.acquire(o,2)
            self.assertEqual(p.reads,2)
            self.assertEqual((o.state.view.facts[0].value,o.state.view.facts[2].value),(0,1))

    def test_16_run_block_stops_after_first_when_sufficient(self):
        with tempfile.TemporaryDirectory() as td:
            ep,p=endpoint(td,3);views=c190.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector();calls=[0]
            def combined(base,head,raw,**kw):
                calls[0]+=1;n=len(raw);need=1 if calls[0]==1 else 0
                return (np.full(n,need,dtype=np.int8),np.zeros(n,dtype=np.int8),
                    np.tile(np.array([[1.,2.]],dtype=np.float32),(n,1)),
                    np.zeros((n,4),dtype=np.float32),meter(n))
            initial=cached_initial(views,0)
            with mock.patch.object(parent,"combined_predict",combined):
                rec,_,_=c190.run_block(views,np.array([3]),{3:ep},base,head,initial=initial)
            self.assertEqual((p.reads,len(rec[0]["acquisitions"]),len(rec[0]["phases"])),(1,1,2))

    def test_17_run_block_two_acquisitions(self):
        with tempfile.TemporaryDirectory() as td:
            ep,p=endpoint(td,3);views=c190.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
            def combined(base,head,raw,**kw):
                n=len(raw)
                return (np.ones(n,dtype=np.int8),np.full(n,2,dtype=np.int8),
                    np.tile(np.array([[0.,1.]],dtype=np.float32),(n,1)),
                    np.zeros((n,4),dtype=np.float32),meter(n))
            final=lambda base,raw,**kw:(np.zeros(len(raw),dtype=np.int8),np.zeros((len(raw),2),dtype=np.float32),meter(len(raw)))
            initial=cached_initial(views,0)
            with mock.patch.object(parent,"combined_predict",combined),mock.patch.object(parent,"necessity_predict",final):
                rec,_,_=c190.run_block(views,np.array([3]),{3:ep},base,head,initial=initial)
            self.assertEqual((p.reads,len(rec[0]["acquisitions"]),len(rec[0]["phases"])),(2,2,3))

    def test_18_run_block_never_third_acquisition(self):
        with tempfile.TemporaryDirectory() as td:
            ep,p=endpoint(td,3);views=c190.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
            def combined(base,head,raw,**kw):
                n=len(raw)
                return (np.ones(n,dtype=np.int8),np.full(n,2,dtype=np.int8),
                    np.zeros((n,2),dtype=np.float32),np.zeros((n,4),dtype=np.float32),meter(n))
            final=lambda base,raw,**kw:(np.ones(len(raw),dtype=np.int8),np.zeros((len(raw),2),dtype=np.float32),meter(len(raw)))
            initial=cached_initial(views,0)
            with mock.patch.object(parent,"combined_predict",combined),mock.patch.object(parent,"necessity_predict",final):
                rec,_,_=c190.run_block(views,np.array([3]),{3:ep},base,head,initial=initial)
            self.assertEqual(p.reads,2)
            self.assertEqual(rec[0]["status"],"UNRESOLVED")

    def test_19_resource_state_after_one_acquisition(self):
        with tempfile.TemporaryDirectory() as td:
            ep,_=endpoint(td,3);views=c190.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector();calls=[0]
            def combined(base,head,raw,**kw):
                calls[0]+=1;n=len(raw);need=1 if calls[0]==1 else 0
                return np.full(n,need,dtype=np.int8),np.zeros(n,dtype=np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
            initial=cached_initial(views,0)
            with mock.patch.object(parent,"combined_predict",combined):
                rec,_,_=c190.run_block(views,np.array([3]),{3:ep},base,head,initial=initial)
            self.assertEqual((rec[0]["final"]["features"][62],rec[0]["final"]["features"][63],rec[0]["final"]["features"][71]),(7,3,12))

    def test_20_resource_state_after_two_acquisitions(self):
        with tempfile.TemporaryDirectory() as td:
            ep,_=endpoint(td,3);views=c190.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),np.array([3]),"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
            def combined(base,head,raw,**kw):
                n=len(raw)
                return np.ones(n,dtype=np.int8),np.full(n,2,dtype=np.int8),np.zeros((n,2),np.float32),np.zeros((n,4),np.float32),meter(n)
            final=lambda base,raw,**kw:(np.zeros(len(raw),dtype=np.int8),np.zeros((len(raw),2),np.float32),meter(len(raw)))
            initial=cached_initial(views,0)
            with mock.patch.object(parent,"combined_predict",combined),mock.patch.object(parent,"necessity_predict",final):
                rec,_,_=c190.run_block(views,np.array([3]),{3:ep},base,head,initial=initial)
            self.assertEqual((rec[0]["final"]["features"][62],rec[0]["final"]["features"][63],rec[0]["final"]["features"][71]),(3,2,16))

    def _good_records(self,second=4000):
        out=[]
        for b,h in c190.expected_order():
            out.append(dict(base_seed=b,head_seed=h,episodes=9536,missing2_worlds=4608,missing3_worlds=4928,
                failed=0,initial_error=0,initial_replay_error=0,target0_error=0,selected_observed=0,
                first_acquisition_error=0,post1_error=0,target1_error=0,repeated_target=0,
                second_acquisition_error=0,post2_error=0,contract_error=0,
                first_reservations=9536,first_provider_calls=9536,first_publications=9536,
                second_reservations=second,second_provider_calls=second,second_publications=second,
                decision_charges=2*9536+second,internal_charged=5*9536+4*second,
                post1_expected_needs=second,post2_expected_needs=1000,
                final_sufficient=8536,final_needs=1000,
                initial_necessity_max_abs_logit_difference=0.0,initial_target_max_abs_logit_difference=0.0))
        return out

    def test_21_gate_accepts_dynamic_second_count(self):
        self.assertTrue(c190.gate(self._good_records()))

    def test_22_gate_requires_nine_blocks(self):
        self.assertFalse(c190.gate(self._good_records()[:-1]))

    def test_23_gate_rejects_first_target_error(self):
        r=self._good_records();r[0]["target0_error"]=r[0]["failed"]=1
        self.assertFalse(c190.gate(r))

    def test_24_gate_rejects_second_target_error(self):
        r=self._good_records();r[0]["target1_error"]=r[0]["failed"]=1
        self.assertFalse(c190.gate(r))

    def test_25_gate_rejects_repeat(self):
        r=self._good_records();r[0]["repeated_target"]=r[0]["failed"]=1
        self.assertFalse(c190.gate(r))

    def test_26_gate_rejects_post2_error(self):
        r=self._good_records();r[0]["post2_error"]=r[0]["failed"]=1
        self.assertFalse(c190.gate(r))

    def test_27_gate_rejects_second_io_mismatch(self):
        r=self._good_records();r[0]["second_provider_calls"]-=1
        self.assertFalse(c190.gate(r))

    def test_28_gate_rejects_decision_accounting(self):
        r=self._good_records();r[0]["decision_charges"]-=1
        self.assertFalse(c190.gate(r))

    def test_29_gate_rejects_internal_accounting(self):
        r=self._good_records();r[0]["internal_charged"]-=1
        self.assertFalse(c190.gate(r))

    def test_30_gate_rejects_initial_logit_drift(self):
        r=self._good_records();r[0]["initial_target_max_abs_logit_difference"]=c190.ATOL*2
        self.assertFalse(c190.gate(r))

    def test_31_manifest_hash_fixed(self):
        self.assertEqual(c190.digest(c190.manifest()),c190.MANIFEST_SHA)

    def test_32_manifest_world_workload(self):
        m=c190.manifest()
        self.assertEqual((m["worlds_per_selector"],m["blocks"],m["episodes"]),(9536,9,85824))
        self.assertEqual((m["logical_initial_episodes"],m["initial_unique_policy_rows"]),(85824,15912))

    def test_33_manifest_scope(self):
        m=c190.manifest()
        self.assertEqual((m["training"],m["fresh_seeds"],m["max_acquisitions_per_episode"]),(0,0,2))
        self.assertFalse(m["production_runtime_modified"])
        self.assertFalse(m["gate_e_candidate"])

    def test_34_source_hashes_fixed(self):
        for code in range(16):
            name=f"sources/world-{code:02d}.json"
            self.assertEqual(__import__("hashlib").sha256(c190.world_bytes(code)).hexdigest(),c190.SOURCE_FILES[name])

    def test_35_outputs_exact_count(self):
        self.assertEqual(len(c190.OUTPUTS),21)

    def test_36_policy_interfaces_have_no_teacher_or_answer(self):
        for fn in (c190.run_block,c190.acquire):
            names=set(inspect.signature(fn).parameters)
            self.assertFalse({"label","teacher","answer","expected_value","world_bits"} & names)

if __name__=="__main__":
    unittest.main(verbosity=2)
