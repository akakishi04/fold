"""C176 helper tests only: synthetic counts/toy fits, never deciding pilot training."""
from copy import deepcopy
import hashlib
from pathlib import Path
import tempfile
import unittest

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from fold_lm.v05_benchmarks import gate_e_c176_conditional_loss as b


class C176Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads=torch.get_num_threads();torch.set_num_threads(2)

    @classmethod
    def tearDownClass(cls):
        torch.set_num_threads(cls.threads)

    def toy(self):
        torch.manual_seed(17)
        return nn.Linear(72,2),torch.arange(8*72,dtype=torch.float32).reshape(8,72)/1000,torch.tensor([0,1]*4)

    def pairs(self):
        def score(primary,group,n1,s3):
            return dict(macro_missing_balanced_accuracy=primary,
                metrics=dict(macro_group_balanced_accuracy=group,needs_recall=.7,sufficient_recall=.8),
                by_missing_count={'1':dict(needs_recall=n1),'3':dict(sufficient_recall=s3)})
        return [dict(seed=s,paired_initial_equal=True,paired_batches_equal=True,
                     uniform=score(.6,.7,.2,.1),conditional=score(.7,.72,.4,.3)) for s in b.SEEDS]

    def test_01_missing_count_uses_only_presence(self):
        x=np.zeros((5,72),dtype=np.int32)
        for m in range(5): x[m,48:62:4][:4-m]=1
        self.assertEqual(b.missing_counts(x).tolist(),list(range(5)))

    def test_02_bad_presence_schema(self):
        for x in (np.zeros((3,71),dtype=np.int32),np.zeros((3,72)),np.zeros((3,72),dtype=bool)):
            with self.assertRaises(ValueError):b.missing_counts(x)
        x=np.zeros((1,72),dtype=np.int32);x[0,48]=2
        with self.assertRaises(ValueError):b.missing_counts(x)

    def test_03_zero_payload_is_not_missing(self):
        x=np.zeros((1,72),dtype=np.int32);x[:,48:62:4]=1
        self.assertEqual(b.missing_counts(x).tolist(),[0])
        x[:,49:63:4]=1
        self.assertEqual(b.missing_counts(x).tolist(),[0])

    def test_04_exact_conditional_formula(self):
        w,t=b.conditional_weights([0,0,0,1],[1,1,1,1])
        np.testing.assert_allclose(w,[2/3,2/3,2/3,2])
        self.assertEqual(t[1]['counts'],[3,1])

    def test_05_each_stratum_mass_preserved(self):
        y=np.array([0,0,1,0,1,1,1]);m=np.array([1,1,1,3,3,3,3])
        w,_=b.conditional_weights(y,m)
        for k in (1,3):self.assertAlmostEqual(float(w[m==k].sum()),float((m==k).sum()))

    def test_06_mixed_classes_have_equal_total_weight(self):
        y=np.array([0]*7+[1]*3);w,_=b.conditional_weights(y,np.ones(10,dtype=int))
        self.assertAlmostEqual(w[y==0].sum(),w[y==1].sum())

    def test_07_pure_strata_keep_unit_weight(self):
        w,_=b.conditional_weights([0,0,1],[0,0,4]);np.testing.assert_array_equal(w,[1,1,1])

    def test_08_absent_strata_do_not_invent_rows(self):
        w,t=b.conditional_weights([0,1],[2,2]);self.assertEqual(len(w),2)
        self.assertEqual(t[1],dict(missing=1,counts=[0,0],weights=[1.,1.]))

    def test_09_row_permutation_equivariance(self):
        y=np.array([0,0,1,1,1]);m=np.array([1,1,1,3,3]);order=np.array([4,1,0,3,2])
        w,t=b.conditional_weights(y,m);v,u=b.conditional_weights(y[order],m[order])
        np.testing.assert_array_equal(v,w[order]);self.assertEqual(t,u)

    def test_10_bad_labels_or_counts(self):
        for y,m in [([2],[1]),([0],[5]),([0],[-1]),([0.0],[1]),([0],[float('nan')])]:
            with self.assertRaises(ValueError):b.conditional_weights(y,m)

    def test_11_bad_shapes_and_empty(self):
        for y,m in [([],[]),([0,1],[1]),([[0,1]],[1]),([True],[1])]:
            with self.assertRaises(ValueError):b.conditional_weights(y,m)

    def test_12_training_arrays_immutable(self):
        y=np.array([0,0,1]);m=np.array([1,1,1]);a=y.copy();c=m.copy()
        b.conditional_weights(y,m);np.testing.assert_array_equal(y,a);np.testing.assert_array_equal(m,c)

    def test_13_registered_counts_mass(self):
        y=[];m=[]
        for k,counts in enumerate(b.COUNTS):
            for label,n in enumerate(counts):y.extend([label]*n);m.extend([k]*n)
        w,t=b.conditional_weights(y,m)
        self.assertEqual(len(w),42444);self.assertAlmostEqual(w.sum(),42444)
        self.assertEqual(tuple(tuple(r['counts']) for r in t),b.COUNTS)
        self.assertLess(w.max(),2.2)

    def test_14_unit_loss_matches_ordinary_ce(self):
        z=torch.tensor([[.2,.5],[1.,-.2]],dtype=torch.float32);y=torch.tensor([0,1])
        loss,ordinary=b.weighted_loss(z,y,torch.ones(2))
        self.assertTrue(torch.equal(loss,ordinary));self.assertTrue(torch.allclose(loss,F.cross_entropy(z,y)))

    def test_15_divisor_is_batch_length_not_weight_sum(self):
        z=torch.zeros(2,2);y=torch.tensor([0,1]);w=torch.tensor([2.,4.])
        loss,_=b.weighted_loss(z,y,w)
        self.assertAlmostEqual(loss.item(),3*np.log(2),places=6)

    def test_16_weighted_gradient_matches_formula(self):
        z=torch.tensor([[.2,.5],[1.,-.2]],requires_grad=True);y=torch.tensor([0,1]);w=torch.tensor([.5,2.])
        loss,_=b.weighted_loss(z,y,w);loss.backward()
        expected=(z.detach().softmax(1)-F.one_hot(y,2))*w[:,None]/2
        self.assertTrue(torch.allclose(z.grad,expected,atol=1e-7))

    def test_17_nonpositive_and_nonfinite_weights_rejected(self):
        for v in (0.,-1.,float('nan'),float('inf')):
            with self.assertRaises(ValueError):b.weighted_loss(torch.zeros(2,2),torch.tensor([0,1]),torch.tensor([1.,v]))

    def test_18_bad_loss_labels_and_types(self):
        for y in (torch.tensor([0,2]),torch.tensor([False,True]),torch.tensor([0.,1.])):
            with self.assertRaises(ValueError):b.weighted_loss(torch.zeros(2,2),y,torch.ones(2))
        with self.assertRaises(ValueError):b.weighted_loss(torch.zeros(2,3),torch.tensor([0,1]),torch.ones(2))

    def test_19_toy_fit_deterministic(self):
        model,x,y=self.toy();w=torch.ones(8)
        a,la=b.fit(model,x,y,w,11,steps=2,batch_size=4)
        c,lc=b.fit(model,x,y,w,11,steps=2,batch_size=4)
        self.assertEqual(b.fingerprint(a),b.fingerprint(c));self.assertEqual(la,lc)

    def test_20_fit_preserves_initial_and_inputs(self):
        model,x,y=self.toy();w=torch.ones(8);h=b.fingerprint(model);xc=x.clone();yc=y.clone();wc=w.clone()
        _,log=b.fit(model,x,y,w,12,steps=2,batch_size=4)
        self.assertEqual(h,b.fingerprint(model));self.assertTrue(torch.equal(x,xc))
        self.assertTrue(torch.equal(y,yc));self.assertTrue(torch.equal(w,wc));self.assertEqual(log['examples_drawn'],8)

    def test_21_pair_has_same_batches_with_different_weights(self):
        model,x,y=self.toy()
        _,a=b.fit(model,x,y,torch.ones(8),13,steps=2,batch_size=4)
        _,c=b.fit(model,x,y,torch.tensor([.5,2.]*4),13,steps=2,batch_size=4)
        self.assertEqual(a['batch_schedule_sha256'],c['batch_schedule_sha256'])

    def test_22_weights_change_updates_not_capacity(self):
        model,x,y=self.toy()
        a,_=b.fit(model,x,y,torch.ones(8),14,steps=2,batch_size=4)
        c,_=b.fit(model,x,y,torch.tensor([.5,2.]*4),14,steps=2,batch_size=4)
        self.assertNotEqual(b.fingerprint(a),b.fingerprint(c))
        self.assertEqual(sum(p.numel() for p in a.parameters()),sum(p.numel() for p in c.parameters()))

    def test_23_fit_rejects_invalid_setup(self):
        model,x,y=self.toy()
        for kw in (dict(steps=0),dict(batch_size=0),dict(steps=True)):
            with self.assertRaises(ValueError):b.fit(model,x,y,torch.ones(8),11,**kw)
        with self.assertRaises(ValueError):b.fit(model,x,y,torch.zeros(8),11,steps=1)
        with self.assertRaises(ValueError):b.fit(model,x,torch.zeros_like(y),torch.ones(8),11,steps=1)

    def test_24_gate_each_seed_and_pair_integrity(self):
        p=self.pairs();self.assertTrue(b.gate(p));self.assertFalse(b.gate(p[:-1]))
        p[1]['paired_batches_equal']=False;self.assertFalse(b.gate(p))
        p=self.pairs();p[1]['paired_initial_equal']=False;self.assertFalse(b.gate(p))

    def test_25_gate_strict_target_improvement(self):
        for path in [('macro_missing_balanced_accuracy',),('by_missing_count','1','needs_recall'),
                     ('by_missing_count','3','sufficient_recall')]:
            p=self.pairs();a=p[0]['conditional'];c=p[0]['uniform']
            for key in path[:-1]:a=a[key];c=c[key]
            a[path[-1]]=c[path[-1]];self.assertFalse(b.gate(p))

    def test_26_gate_original_score_no_drop_and_no_class_collapse(self):
        p=self.pairs();p[0]['conditional']['metrics']['macro_group_balanced_accuracy']=.7
        self.assertTrue(b.gate(p))
        for k,value in [('macro_group_balanced_accuracy',.69),('needs_recall',.5),
                        ('sufficient_recall',.5),('needs_recall',float('nan'))]:
            q=self.pairs();q[0]['conditional']['metrics'][k]=value;self.assertFalse(b.gate(q))

    def test_27_regression_list_is_additive(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'tools').mkdir()
            (root/'tools/run_c167.ps1').write_text('\n'.join(f'"tests_lm.fixture_{i}"' for i in range(51)))
            names=b.regression_modules(root)
            self.assertEqual(len(names),60);self.assertEqual(len(set(names)),60)
            self.assertEqual(names[-1],'tests_lm.test_v05_c176_conditional_loss')

    def test_28_manifest_and_workload_frozen(self):
        self.assertEqual(hashlib.sha256(b.blob(b.manifest())).hexdigest(),b.MANIFEST_SHA)
        self.assertEqual(b.SEEDS,(176001,176002,176003));self.assertEqual((b.STEPS,b.BATCH),(2000,256))
        self.assertEqual(b.manifest()['parameters'],26114)
        self.assertEqual(b.manifest()['training_updates'],12000)


if __name__=='__main__':unittest.main()
