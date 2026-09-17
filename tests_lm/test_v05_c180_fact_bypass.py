"""Helper checks; tiny synthetic data, never the registered C180 training run."""
from copy import deepcopy
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import torch
from torch import nn
from fold_lm.v05_benchmarks import gate_e_c180_fact_bypass as b


def inputs():
    # Two seven-node trees; synthetic visible input, not a pilot row or teacher output.
    x=torch.zeros((2,72),dtype=torch.float32);x[:,:2]=1;x[:,2:4]=1
    n=x[:,4:46].reshape(2,7,6);n[:,:,0]=1
    for i,f in ((0,0),(1,1),(3,2),(4,3)):
        n[:,i,1]=1/3;n[:,i,2]=(f+1)/4
        n[:,i,3]=1;n[:,i,4]=torch.tensor([0.,1.])
    for i,left,right,kind in ((2,1,2,2),(5,4,5,2),(6,3,6,3)):
        n[:,i,1]=kind/3;n[:,i,3]=left/7;n[:,i,4]=right/7
    f=x[:,46:62].reshape(2,4,4);f[:,:,0]=1;f[:,:,1]=2/8;f[:,:,2]=1
    f[1,:,3]=1;x[:,62:]=.25
    return x


def score(v):
    return dict(macro_missing_balanced_accuracy=v,
        metrics=dict(macro_group_balanced_accuracy=v,needs_recall=v,sufficient_recall=v),
        by_missing_count={'1':dict(needs_recall=v),'3':dict(sufficient_recall=v)})


def passing_pairs():
    return [dict(seed=s,direct=score(.6),no_direct=score(.8),
                 paired_initial_equal=True,paired_batches_equal=True) for s in b.SEEDS]


class FactBypassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):torch.set_num_threads(2)

    def test_01_explicit_condition(self):
        with self.assertRaises(ValueError):b.FactReadoutMask('automatic')

    def test_02_direct_identity(self):
        x=torch.randn(3,94);self.assertTrue(torch.equal(b.FactReadoutMask(b.ARMS[0])(x),x))

    def test_03_only_fact_columns_masked(self):
        x=torch.arange(94,dtype=torch.float32).repeat(2,1);y=b.FactReadoutMask(b.ARMS[1])(x)
        self.assertTrue(torch.equal(y[:,:68],x[:,:68]));self.assertEqual(int(torch.count_nonzero(y[:,68:84])),0)
        self.assertTrue(torch.equal(y[:,84:],x[:,84:]))

    def test_04_root_retained(self):
        x=torch.randn(2,94);self.assertTrue(torch.equal(b.FactReadoutMask(b.ARMS[1])(x)[:,:64],x[:,:64]))

    def test_05_header_runtime_retained(self):
        x=torch.randn(2,94);y=b.FactReadoutMask(b.ARMS[1])(x)
        self.assertTrue(torch.equal(y[:,64:68],x[:,64:68]));self.assertTrue(torch.equal(y[:,84:],x[:,84:]))

    def test_06_no_input_mutation(self):
        x=torch.randn(2,94);before=x.clone();b.FactReadoutMask(b.ARMS[1])(x)
        self.assertTrue(torch.equal(x,before))

    def test_07_shape_rejection(self):
        for x in (torch.zeros(94),torch.zeros(2,72),torch.zeros(0,94)):
            with self.subTest(shape=x.shape),self.assertRaises(ValueError):b.FactReadoutMask(b.ARMS[0])(x)

    def test_08_dtype_rejection(self):
        for dtype in (torch.int32,torch.float64):
            with self.subTest(dtype=dtype),self.assertRaises(ValueError):b.FactReadoutMask(b.ARMS[0])(torch.zeros(1,94,dtype=dtype))

    def test_09_nonfinite_rejection(self):
        for val in (float('inf'),float('nan')):
            x=torch.zeros(1,94);x[0,68]=val
            with self.subTest(val=val),self.assertRaises(ValueError):b.FactReadoutMask(b.ARMS[1])(x)

    def test_10_mask_has_no_weights_and_is_metered(self):
        m=b.FactReadoutMask(b.ARMS[1]);self.assertEqual(len(m.state_dict()),0)
        m(torch.zeros(1,94));m(torch.zeros(2,94));self.assertEqual(m.calls,2)

    def test_11_gradient_mask(self):
        x=torch.ones(2,94,requires_grad=True);b.FactReadoutMask(b.ARMS[1])(x).sum().backward()
        self.assertTrue(torch.equal(x.grad[:,:68],torch.ones(2,68)))
        self.assertEqual(int(torch.count_nonzero(x.grad[:,68:84])),0)
        self.assertTrue(torch.equal(x.grad[:,84:],torch.ones(2,10)))

    def test_12_capacity_and_dense_head(self):
        for arm in b.ARMS:
            m=b.make_model(arm);self.assertEqual(sum(p.numel() for p in m.parameters()),25726)
            self.assertEqual(m.readout[1].weight.shape,(2,94))

    def test_13_tree_in_both_conditions(self):
        for m in b.paired_initial(123):self.assertEqual(m.arm,b.graph.ARMS[1])

    def test_14_paired_weights(self):
        a,c=b.paired_initial(123);self.assertEqual(b.graph.fingerprint(a),b.graph.fingerprint(c))
        self.assertNotEqual(a.readout[0].condition,c.readout[0].condition)

    def test_15_same_root_and_seven_cells(self):
        a,c=b.paired_initial(123);captured=[]
        handles=[m.readout[0].register_forward_pre_hook(lambda module,args:captured.append(args[0].detach().clone())) for m in (a,c)]
        try:a(inputs());c(inputs())
        finally:
            for h in handles:h.remove()
        self.assertTrue(torch.equal(captured[0],captured[1]))
        for m in (a,c):self.assertEqual((m.calls,m.cell_calls,m.readout[0].calls),(1,7,1))

    def test_16_actual_linear_receives_mask(self):
        a,c=b.paired_initial(123);captured=[]
        handles=[m.readout[1].register_forward_pre_hook(lambda module,args:captured.append(args[0].detach().clone())) for m in (a,c)]
        try:a(inputs());c(inputs())
        finally:
            for h in handles:h.remove()
        self.assertEqual(int(torch.count_nonzero(captured[1][:,68:84])),0)
        self.assertGreater(int(torch.count_nonzero(captured[0][:,68:84])),0)
        self.assertTrue(torch.equal(captured[0][:,:68],captured[1][:,:68]))

    def test_17_leaf_information_retained(self):
        m=b.make_model(b.ARMS[1]);seen=[];x=inputs();old=x.clone()
        h=m.cell.register_forward_pre_hook(lambda module,args:seen.append(args[0][:,:6].detach().clone()))
        try:m(x)
        finally:h.remove()
        self.assertTrue(torch.equal(torch.stack(seen,1),x[:,4:46].reshape(2,7,6)))
        self.assertTrue(torch.equal(x,old))

    def test_18_original_control_numerical_parity(self):
        m=b.make_model(b.ARMS[0]);plain=b.graph.SharedGraphProbe(b.graph.ARMS[1])
        plain.cell.load_state_dict(m.cell.state_dict());plain.readout.load_state_dict(m.readout[1].state_dict())
        self.assertTrue(torch.equal(m(inputs()),plain(inputs())))

    def test_19_two_update_toy_fit_is_paired(self):
        a,c=b.paired_initial(234);x=inputs();y=torch.tensor([0,1]);old=x.clone();ih=b.graph.fingerprint(a)
        fa,la=b.graph.fit(a,x,y,234,steps=2,batch=2)
        fc,lc=b.graph.fit(c,x,y,234,steps=2,batch=2)
        self.assertEqual(la['batch_schedule_sha256'],lc['batch_schedule_sha256'])
        self.assertEqual(b.graph.fingerprint(a),ih);self.assertTrue(torch.equal(x,old))
        for m in (fa,fc):self.assertEqual((m.calls,m.cell_calls,m.readout[0].calls),(2,14,2))

    def test_20_predict_raw_argmax_and_weights(self):
        m=b.make_model(b.ARMS[1]);ih=b.graph.fingerprint(m)
        p,z,log=b.graph.predict(m,inputs(),batch=1)
        self.assertTrue(torch.equal(p,z.argmax(1)));self.assertEqual(b.graph.fingerprint(m),ih)
        self.assertEqual((log['forward_calls'],log['cell_calls'],m.readout[0].calls),(2,14,2))

    def test_21_checkpoint_roundtrips(self):
        with tempfile.TemporaryDirectory() as d:
            for condition in b.ARMS:
                m=b.make_model(condition);f=Path(d)/'toy.pt';torch.save(b.checkpoint_payload(m,3,condition),f)
                r=b.restore(f,3,condition);self.assertEqual(b.graph.fingerprint(m),b.graph.fingerprint(r))
                self.assertTrue(torch.equal(m(inputs()),r(inputs())))

    def test_22_checkpoint_metadata_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            for k,v in [('condition',b.ARMS[1]),('model_schema','old'),('steps',1999),('fact_readout_slice',[64,80]),('graph_arm','SEQUENCE_LINKS')]:
                p=b.checkpoint_payload(b.make_model(b.ARMS[0]),3,b.ARMS[0]);p[k]=v;f=Path(d)/'bad.pt';torch.save(p,f)
                with self.subTest(k=k),self.assertRaises(ValueError):b.restore(f,3,b.ARMS[0])

    def test_23_gate_pass_and_group_equality(self):
        p=passing_pairs();self.assertTrue(b.gate(p))
        for a in p:a['no_direct']['metrics']['macro_group_balanced_accuracy']=.6
        self.assertTrue(b.gate(p))

    def test_24_each_gate_condition_and_seed_required(self):
        paths=[('macro_missing_balanced_accuracy',),('metrics','macro_group_balanced_accuracy'),
               ('by_missing_count','1','needs_recall'),('by_missing_count','3','sufficient_recall'),
               ('metrics','needs_recall'),('metrics','sufficient_recall')]
        for index in range(3):
            for path in paths:
                p=passing_pairs();obj=p[index]['no_direct']
                for k in path[:-1]:obj=obj[k]
                obj[path[-1]]=.5
                with self.subTest(seed=index,path=path):self.assertFalse(b.gate(p))
        p=passing_pairs();p[0]['no_direct']['macro_missing_balanced_accuracy']=.6;self.assertFalse(b.gate(p))

    def test_25_gate_invalid_metrics_pairing_identity(self):
        for val in (float('nan'),float('inf'),True):
            p=passing_pairs();p[0]['no_direct']['macro_missing_balanced_accuracy']=val;self.assertFalse(b.gate(p))
        p=passing_pairs();p[0]['paired_batches_equal']=False;self.assertFalse(b.gate(p))
        p=passing_pairs();p[0]['seed']=0;self.assertFalse(b.gate(p));self.assertFalse(b.gate([]))

    def test_26_condition_and_tree_drift_rejected(self):
        m=b.make_model(b.ARMS[0]);m.arm=b.graph.ARMS[0]
        with self.assertRaises(ValueError):b.validate_model(m,b.ARMS[0])
        m=b.make_model(b.ARMS[0]);m.readout[0].condition='wrong'
        with self.assertRaises(ValueError):m(inputs())

    def test_27_zero_weights_do_not_solve(self):
        m=b.make_model(b.ARMS[1])
        with torch.no_grad():
            for p in m.parameters():p.zero_()
        self.assertTrue(torch.equal(m(inputs()),torch.zeros(2,2)))

    def test_28_manifest_and_regression_count(self):
        self.assertEqual(hashlib.sha256(b.blob(b.manifest())).hexdigest(),b.MANIFEST_SHA)
        names=['tests_lm.old_'+str(i) for i in range(63)]
        with patch.object(b.graph,'regression_modules',return_value=names,create=True):
            self.assertEqual(len(b.regression_modules('.')),64)
            self.assertEqual(b.regression_modules('.')[-1],'tests_lm.test_v05_c180_fact_bypass')


if __name__=='__main__':unittest.main()
