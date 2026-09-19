import inspect
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock

import numpy as np
import torch

from fold_lm.v05 import structured_acquisition_lifecycle as life
from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05 import structured_task_input as task
from fold_lm.v05_benchmarks import gate_e_c174_learned_necessity as c174
from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189


def raw_row(visible=(None,0,None,1)):
    x=np.zeros(72,dtype=np.int32);x[0]=7;x[1]=4;x[2]=1;x[3]=1
    nodes=(
        (1,1,1,0,0,0),
        (1,1,2,0,0,0),
        (1,2,0,1,2,0),
        (1,1,3,0,0,0),
        (1,1,4,0,0,0),
        (1,3,0,4,5,0),
        (1,2,0,3,6,0),
    )
    x[4:46]=np.asarray(nodes,dtype=np.int32).reshape(-1)
    for i,v in enumerate(visible):
        x[46+4*i:50+4*i]=(1,1 if v is None else 2,0 if v is None else 1,0 if v is None else v)
    x[62:72]=(12,4,1,0,0,1,0,0,0,7)
    return x


def endpoint(tmp,bit,fact_index=0):
    b=c189.source_bytes(fact_index,bit);p=Path(tmp)/f"s{fact_index}-{bit}.json";p.write_bytes(b)
    sb=life.SourceBinding(f"C185-fixture-{fact_index}-{bit}",__import__("hashlib").sha256(b).hexdigest())
    provider=life.FileSnapshotProvider(p,sb)
    return life.Endpoint(sb,provider),provider

def endpoint_map(tmp,bit):
    eps={};providers={}
    for i,fid in enumerate(driver.FACT_IDS):
        ep,p=endpoint(tmp,bit,i);eps[fid]=ep;providers[i]=p
    return eps,providers


class C189Tests(unittest.TestCase):
    def test_01_source_zero_exact_selected_fact(self):
        p=json.loads(c189.source_bytes(2,0))
        self.assertEqual(p["schema"],life.SOURCE_SCHEMA)
        self.assertEqual(p["records"],[{"fact_id":driver.FACT_IDS[2],"value":0}])

    def test_02_source_one_exact_selected_fact(self):
        p=json.loads(c189.source_bytes(3,1))
        self.assertEqual(p["records"],[{"fact_id":driver.FACT_IDS[3],"value":1}])

    def test_03_source_identity_rejects_bool_and_unregistered(self):
        for i,v in ((True,0),(0,True),(-1,0),(4,0),(0,-1),(0,2)):
            with self.assertRaises(ValueError): c189.source_bytes(i,v)

    def test_04_encode_views_direct_layout(self):
        r=torch.from_numpy(np.stack([raw_row()]))
        v=driver.make_views(r,np.array([7]),driver.LAYOUTS[0],"x")
        got,_=c189.encode_views(v)
        self.assertTrue(torch.equal(got,r))
        self.assertEqual(got[0,2:4].tolist(),[1,1])

    def test_05_encode_views_no_canonicalization(self):
        r=raw_row();r[6],r[12]=2,1
        v=driver.make_views(torch.from_numpy(np.stack([r])),np.array([7]),driver.LAYOUTS[0],"x")
        got,_=c189.encode_views(v)
        self.assertTrue(torch.equal(got,torch.from_numpy(np.stack([r]))))

    def test_06_restore_selector_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            m=target.TargetSelector();sha=target.head_fingerprint(m)
            p=Path(td)/"s.pt"
            torch.save(dict(base_seed=181001,head_seed=188001,schema="c188-target-selector-v1",
                feature_width=target.FEATURES,steps=target.STEPS,head_sha256=sha,state_dict=m.state_dict()),p)
            got=c189.restore_selector(p,181001,188001,sha)
            self.assertEqual(target.head_fingerprint(got),sha)

    def test_07_restore_selector_rejects_metadata(self):
        with tempfile.TemporaryDirectory() as td:
            m=target.TargetSelector();sha=target.head_fingerprint(m);p=Path(td)/"s.pt"
            torch.save(dict(base_seed=181001,head_seed=188001,schema="bad",
                feature_width=target.FEATURES,steps=target.STEPS,head_sha256=sha,state_dict=m.state_dict()),p)
            with self.assertRaises(ValueError): c189.restore_selector(p,181001,188001,sha)

    def test_08_restore_selector_rejects_fingerprint(self):
        with tempfile.TemporaryDirectory() as td:
            m=target.TargetSelector();sha=target.head_fingerprint(m);p=Path(td)/"s.pt"
            torch.save(dict(base_seed=181001,head_seed=188001,schema="c188-target-selector-v1",
                feature_width=target.FEATURES,steps=target.STEPS,head_sha256=sha,state_dict=m.state_dict()),p)
            with self.assertRaises(ValueError): c189.restore_selector(p,181001,188001,"0"*64)

    def _parent_npz(self,path):
        np.savez_compressed(path,row_indices=np.arange(1768,dtype=np.int32),
            predictions=np.zeros((9,1768),dtype=np.int8),
            logits=np.zeros((9,1768,4),dtype=np.float32),
            base_seeds=np.repeat(np.asarray(c189.BASE_SEEDS,dtype=np.int32),3),
            head_seeds=np.tile(np.asarray(c189.HEAD_SEEDS,dtype=np.int32),3))

    def test_09_parent_prediction_loader(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz";self._parent_npz(p)
            z=c189.load_parent_predictions(p)
            self.assertEqual(z["predictions"].shape,(9,1768))

    def test_10_parent_prediction_loader_missing_member(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"p.npz"
            np.savez_compressed(p,row_indices=np.arange(1768,dtype=np.int32))
            with self.assertRaises(ValueError): c189.load_parent_predictions(p)

    def test_11_combined_predict_shapes_and_mask(self):
        raw=torch.from_numpy(np.stack([raw_row(),raw_row((None,None,1,0))]))
        base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
        p,t,z,tz,m=c189.combined_predict(base,head,raw,batch=1)
        self.assertEqual((p.shape,t.shape,z.shape,tz.shape),((2,),(2,),(2,2),(2,4)))
        unknown=target.missing_mask(raw).numpy()
        self.assertTrue(np.isneginf(tz[~unknown]).all())
        self.assertEqual(m["cell_calls"],14)

    def test_12_target_hidden_path_resource_invariant(self):
        a=raw_row();b=a.copy();b[62]=11;b[71]=8
        raw=torch.from_numpy(np.stack([a,b]))
        base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
        _,t,_,tz,_=c189.combined_predict(base,head,raw)
        u=target.missing_mask(raw).numpy()
        self.assertEqual(int(t[0]),int(t[1]))
        self.assertTrue(np.array_equal(tz[0][u[0]],tz[1][u[1]]))

    def test_13_combined_predict_preserves_weights(self):
        raw=torch.from_numpy(np.stack([raw_row()]))
        base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
        a,b=graph.fingerprint(base),target.head_fingerprint(head)
        c189.combined_predict(base,head,raw)
        self.assertEqual((a,b),(graph.fingerprint(base),target.head_fingerprint(head)))

    def test_14_necessity_predict_raw_argmax(self):
        raw=torch.from_numpy(np.stack([raw_row()]))
        base=graph.SharedGraphProbe(graph.ARMS[1])
        p,z,_=c189.necessity_predict(base,raw)
        self.assertTrue(np.array_equal(p,z.argmax(1)))

    def test_15_target_teacher_is_scoring_only_signature(self):
        self.assertEqual(set(inspect.signature(c189.target_teacher).parameters),{"features","template_ids","metadata"})
        self.assertNotIn("valid_targets",inspect.signature(c189.run_block).parameters)

    def test_16_post_label_simple_and(self):
        table=[b[0]&b[1] for b in c174.BITS]
        row=raw_row((1,1,None,None))
        self.assertEqual(c189.post_label(row,0,[{"truth_table":table}]),0)

    def test_17_acquire_selected_dynamic_fact(self):
        with tempfile.TemporaryDirectory() as td:
            eps,providers=endpoint_map(td,1)
            v=driver.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),driver.LAYOUTS[0],"x")[0]
            o=life.AcquisitionOwner(action.RuntimeState(v),{},max_dispatches=1)
            self.assertTrue(driver.charge_decision(o))
            o=c189.bind_selected_endpoint(o,eps,2)
            rec=c189.acquire_selected(o,2)
            self.assertEqual(rec["fact_id"],driver.FACT_IDS[2])
            self.assertEqual(providers[2].reads,1)
            self.assertEqual(o.state.view.facts[2].value,1)
            self.assertEqual(o.state.view.facts[0].status,"UNOBSERVED")

    def test_18_acquire_selected_rejects_observed(self):
        with tempfile.TemporaryDirectory() as td:
            eps,_=endpoint_map(td,0)
            v=driver.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),driver.LAYOUTS[0],"x")[0]
            o=life.AcquisitionOwner(action.RuntimeState(v),{},max_dispatches=1)
            with self.assertRaises(ValueError): c189.bind_selected_endpoint(o,eps,1)

    def test_19_acquire_selected_no_second_dispatch(self):
        with tempfile.TemporaryDirectory() as td:
            eps,providers=endpoint_map(td,0)
            v=driver.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),driver.LAYOUTS[0],"x")[0]
            o=life.AcquisitionOwner(action.RuntimeState(v),{},max_dispatches=1)
            o=c189.bind_selected_endpoint(o,eps,0)
            c189.acquire_selected(o,0)
            self.assertEqual(providers[0].reads,1)
            with self.assertRaises(ValueError): c189.acquire_selected(o,0)

    def test_20_run_block_learned_target_drives_real_io(self):
        with tempfile.TemporaryDirectory() as td:
            eps,providers=endpoint_map(td,1)
            rows=torch.from_numpy(np.stack([raw_row(),raw_row((None,None,1,0))]))
            views=driver.make_views(rows,np.array([0,1]),driver.LAYOUTS[0],"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
            def fake_combined(base,head,raw,**kw):
                n=len(raw);return (np.ones(n,dtype=np.int8),np.array([0,1],dtype=np.int8),
                    np.tile(np.array([[0.,1.]],dtype=np.float32),(n,1)),
                    np.zeros((n,4),dtype=np.float32),dict(rows=n,forward_calls=1,cell_calls=7,wall_clock_seconds=0.))
            def fake_post(base,raw,**kw):
                n=len(raw);return np.array([0,1],dtype=np.int8),np.zeros((n,2),dtype=np.float32),dict(rows=n,forward_calls=1,cell_calls=7,wall_clock_seconds=0.)
            with mock.patch.object(c189,"combined_predict",fake_combined),mock.patch.object(c189,"necessity_predict",fake_post):
                rec,arr,_=c189.run_block(views,eps,base,head)
            self.assertEqual(sum(p.reads for p in providers.values()),2)
            self.assertEqual(rec[0]["receipts"][0]["fact_id"],driver.FACT_IDS[0])
            self.assertEqual(rec[1]["receipts"][0]["fact_id"],driver.FACT_IDS[1])
            self.assertEqual(arr["necessity_predictions"][:,1].tolist(),[0,1])

    def test_21_run_block_has_one_acquisition_each(self):
        with tempfile.TemporaryDirectory() as td:
            eps,providers=endpoint_map(td,0)
            views=driver.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),driver.LAYOUTS[0],"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
            fake=lambda base,head,raw,**kw:(np.ones(len(raw),dtype=np.int8),np.zeros(len(raw),dtype=np.int8),
                np.zeros((len(raw),2),dtype=np.float32),np.zeros((len(raw),4),dtype=np.float32),
                dict(rows=len(raw),forward_calls=1,cell_calls=7,wall_clock_seconds=0.))
            post=lambda base,raw,**kw:(np.ones(len(raw),dtype=np.int8),np.zeros((len(raw),2),dtype=np.float32),
                dict(rows=len(raw),forward_calls=1,cell_calls=7,wall_clock_seconds=0.))
            with mock.patch.object(c189,"combined_predict",fake),mock.patch.object(c189,"necessity_predict",post):
                rec,_,_=c189.run_block(views,eps,base,head)
            self.assertEqual(sum(p.reads for p in providers.values()),1)
            self.assertEqual(len(rec[0]["receipts"]),1)
            self.assertEqual(len(rec[0]["phases"]),2)

    def test_22_run_block_post_need_does_not_reacquire(self):
        self.test_21_run_block_has_one_acquisition_each()

    def test_23_run_block_charges_two_decisions(self):
        with tempfile.TemporaryDirectory() as td:
            eps,_=endpoint_map(td,0)
            views=driver.make_views(torch.from_numpy(np.stack([raw_row()])),np.array([0]),driver.LAYOUTS[0],"x")
            base=graph.SharedGraphProbe(graph.ARMS[1]);head=target.TargetSelector()
            fake=lambda base,head,raw,**kw:(np.ones(len(raw),dtype=np.int8),np.zeros(len(raw),dtype=np.int8),
                np.zeros((len(raw),2),dtype=np.float32),np.zeros((len(raw),4),dtype=np.float32),
                dict(rows=len(raw),forward_calls=1,cell_calls=7,wall_clock_seconds=0.))
            post=lambda base,raw,**kw:(np.zeros(len(raw),dtype=np.int8),np.zeros((len(raw),2),dtype=np.float32),
                dict(rows=len(raw),forward_calls=1,cell_calls=7,wall_clock_seconds=0.))
            with mock.patch.object(c189,"combined_predict",fake),mock.patch.object(c189,"necessity_predict",post):
                rec,_,_=c189.run_block(views,eps,base,head)
            self.assertEqual(rec[0]["decision_charges"],2)
            self.assertEqual(rec[0]["final"]["features"][62],7)
            self.assertEqual(rec[0]["final"]["features"][63],3)
            self.assertEqual(rec[0]["final"]["features"][71],12)

    def _good_replay(self):
        return [dict(base_seed=b,head_seed=h,predictions_equal=True,max_abs_logit_difference=0.0)
                for b in c189.BASE_SEEDS for h in c189.HEAD_SEEDS]

    def _good_records(self):
        out=[]
        for b,h,bit in c189.expected_order():
            out.append(dict(base_seed=b,head_seed=h,completion=bit,episodes=1768,discriminating_rows=528,
                failed=0,initial_error=0,target_error=0,target_replay_error=0,selected_observed=0,
                missed_acquisition=0,post_error=0,contract_error=0,reservations=1768,
                provider_calls=1768,publications=1768,decision_charges=3536,internal_charged=8840,
                discriminating_target_errors=0,initial_target_max_abs_logit_difference=0.0,
                post_sufficient=700,post_needs=1068))
        return out

    def test_24_gate_accepts_exact_profile(self):
        self.assertTrue(c189.gate(self._good_records(),self._good_replay()))

    def test_25_gate_requires_all_eighteen_blocks(self):
        self.assertFalse(c189.gate(self._good_records()[:-1],self._good_replay()))

    def test_26_gate_rejects_target_error(self):
        r=self._good_records();r[0]["target_error"]=r[0]["failed"]=1
        self.assertFalse(c189.gate(r,self._good_replay()))

    def test_27_gate_rejects_discriminating_target_error(self):
        r=self._good_records();r[0]["discriminating_target_errors"]=1
        self.assertFalse(c189.gate(r,self._good_replay()))

    def test_28_gate_rejects_initial_need_error(self):
        r=self._good_records();r[0]["initial_error"]=r[0]["failed"]=1
        self.assertFalse(c189.gate(r,self._good_replay()))

    def test_29_gate_rejects_post_error(self):
        r=self._good_records();r[0]["post_error"]=r[0]["failed"]=1
        self.assertFalse(c189.gate(r,self._good_replay()))

    def test_30_gate_rejects_contract_error(self):
        r=self._good_records();r[0]["contract_error"]=r[0]["failed"]=1
        self.assertFalse(c189.gate(r,self._good_replay()))

    def test_31_gate_rejects_io_count(self):
        r=self._good_records();r[0]["provider_calls"]-=1
        self.assertFalse(c189.gate(r,self._good_replay()))

    def test_32_gate_rejects_decision_accounting(self):
        r=self._good_records();r[0]["decision_charges"]-=1
        self.assertFalse(c189.gate(r,self._good_replay()))

    def test_33_gate_rejects_parent_replay(self):
        q=self._good_replay();q[0]["predictions_equal"]=False
        self.assertFalse(c189.gate(self._good_records(),q))

    def test_34_gate_rejects_target_logit_drift(self):
        r=self._good_records();r[0]["initial_target_max_abs_logit_difference"]=c189.ATOL*2
        self.assertFalse(c189.gate(r,self._good_replay()))

    def test_35_manifest_hash_and_scope(self):
        self.assertEqual(c189.digest(c189.manifest()),c189.MANIFEST_SHA)
        m=c189.manifest()
        self.assertEqual((m["blocks"],m["episodes"],m["training"]),(18,31824,0))
        self.assertFalse(m["production_runtime_modified"])
        self.assertFalse(m["gate_e_candidate"])

    def test_36_policy_interfaces_have_no_teacher_or_answer(self):
        for fn in (c189.combined_predict,c189.necessity_predict,c189.run_block,c189.acquire_selected):
            names=set(inspect.signature(fn).parameters)
            self.assertFalse({"label","teacher","answer","expected_value"} & names)

if __name__=="__main__":
    unittest.main(verbosity=2)
