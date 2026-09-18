"""Synthetic unit tests, not C183 checkpoint inference or deciding measurements."""
import copy
import hashlib
import inspect
import unittest
import numpy as np
import torch
from torch import nn
from fold_lm.v05_benchmarks import gate_e_c183_frozen_path_attribution as b


def inputs(n=3):
    a=torch.arange(n*94,dtype=torch.float32).reshape(n,94)/1000
    r=a.clone();r[:,:64]+=.1;r[:,68:84]-=.2
    return a,r


class Toy(nn.Module):
    def __init__(self):
        super().__init__();self.readout=nn.Linear(94,2)
    def forward(self,x):return self.readout(x)


def predictor(m,x,*,batch):
    with torch.inference_mode():
        z=torch.cat([m(x[i:i+batch]) for i in range(0,len(x),batch)])
    return z.argmax(1),z,dict(rows=len(x),forward_calls=(len(x)+batch-1)//batch)


def raw_row():
    a=np.zeros(72,dtype=np.int32);a[:2]=[7,4]
    a[4:46]=np.asarray([[1,1,1,0,0,0],[1,1,2,0,0,1],[1,2,0,1,2,0],
        [1,1,3,0,0,0],[1,1,4,0,0,0],[1,3,0,4,5,0],[1,3,0,3,6,0]]).ravel()
    a[46:62]=np.asarray([[1,2,1,0],[1,1,0,0],[1,2,1,1],[1,1,0,0]]).ravel()
    return a


def case(tree=0,direct=1):
    d=dict(zip(b.MODES,[1,0,tree,direct]))
    return dict(seed=181003,permutation_index=17,label=1,decisions=d,
                mode=b.failure_mode(1,1,0,tree,direct))


class FrozenPathTests(unittest.TestCase):
    def test_01_only_root_patched(self):
        a,r=inputs();t,d=b.hybrid_inputs(a,r)
        self.assertTrue(torch.equal(t[:,:64],r[:,:64]));self.assertTrue(torch.equal(t[:,64:],a[:,64:]))
    def test_02_only_facts_patched(self):
        a,r=inputs();t,d=b.hybrid_inputs(a,r)
        self.assertTrue(torch.equal(d[:,68:84],r[:,68:84]));self.assertTrue(torch.equal(d[:,:68],a[:,:68]))
        self.assertTrue(torch.equal(d[:,84:],a[:,84:]))
    def test_03_original_not_mutated(self):
        a,r=inputs();aa=a.clone();rr=r.clone();b.hybrid_inputs(a,r)
        self.assertTrue(torch.equal(a,aa) and torch.equal(r,rr))
    def test_04_identity(self):
        a,_=inputs();t,d=b.hybrid_inputs(a,a)
        self.assertTrue(torch.equal(a,t) and torch.equal(a,d))
    def test_05_header_change_rejected(self):
        a,r=inputs();r[0,64]+=1
        with self.assertRaises(ValueError):b.hybrid_inputs(a,r)
    def test_06_runtime_change_rejected(self):
        a,r=inputs();r[0,90]+=1
        with self.assertRaises(ValueError):b.hybrid_inputs(a,r)
    def test_07_shape(self):
        a,r=inputs()
        with self.assertRaises(ValueError):b.hybrid_inputs(a[:,:93],r[:,:93])
    def test_08_dtype(self):
        a,r=inputs()
        with self.assertRaises(ValueError):b.hybrid_inputs(a.double(),r.double())
    def test_09_nonfinite(self):
        a,r=inputs();r[0,0]=float('nan')
        with self.assertRaises(ValueError):b.hybrid_inputs(a,r)
    def test_10_empty(self):
        a,r=inputs()
        with self.assertRaises(ValueError):b.hybrid_inputs(a[:0],r[:0])
    def test_11_capture_numerical_parity(self):
        m=Toy().eval().requires_grad_(False);x,_=inputs();p,z,h,_=b.capture_predict(m,x,predictor)
        pp,zz,_=predictor(m,x,batch=b.BATCH)
        self.assertTrue(torch.equal(p,pp) and torch.equal(z,zz) and torch.equal(h,x))
    def test_12_hook_cleanup(self):
        m=Toy();x,_=inputs();b.capture_predict(m,x,predictor)
        self.assertFalse(m.readout._forward_pre_hooks)
    def test_13_hook_cleanup_on_exception(self):
        m=Toy();x,_=inputs()
        def bad(*args,**kwargs):raise RuntimeError('fixture failure')
        with self.assertRaises(RuntimeError):b.capture_predict(m,x,bad)
        self.assertFalse(m.readout._forward_pre_hooks)
    def test_14_existing_hook_rejected(self):
        m=Toy();x,_=inputs();h=m.readout.register_forward_pre_hook(lambda *args:None)
        try:
            with self.assertRaises(ValueError):b.capture_predict(m,x,predictor)
        finally:h.remove()
    def test_15_capture_multiple_batches(self):
        m=Toy();x,_=inputs(1027);_,_,h,meter=b.capture_predict(m,x,predictor)
        self.assertEqual(meter['forward_calls'],2);self.assertTrue(torch.equal(h,x))
    def test_16_head_raw_argmax(self):
        m=Toy();a,_=inputs();p,z,n=b.head_predict(m.readout,a)
        self.assertTrue(torch.equal(p,z.argmax(1)));self.assertEqual(n,1)
    def test_17_head_preserves_weights(self):
        m=Toy();old=copy.deepcopy(m.state_dict());a,_=inputs();b.head_predict(m.readout,a)
        self.assertTrue(all(torch.equal(v,old[k]) for k,v in m.state_dict().items()))
    def test_18_linear_decomposition(self):
        m=Toy();a,r=inputs();t,d=b.hybrid_inputs(a,r)
        z=[b.head_predict(m.readout,x)[1] for x in (a,r,t,d)]
        self.assertTrue(torch.allclose(z[1].double()-z[0].double(),z[2].double()+z[3].double()-2*z[0].double(),atol=1e-6,rtol=0))
    def test_19_tree_only_case(self):self.assertEqual(b.failure_mode(1,1,0,0,1),'TREE_ONLY_SUFFICIENT')
    def test_20_direct_only_case(self):self.assertEqual(b.failure_mode(1,1,0,1,0),'DIRECT_ONLY_SUFFICIENT')
    def test_21_joint_case(self):self.assertEqual(b.failure_mode(1,1,0,1,1),'JOINT_REQUIRED')
    def test_22_either_case(self):self.assertEqual(b.failure_mode(1,1,0,0,0),'EITHER_ALONE')
    def test_23_not_source_failure(self):
        with self.assertRaises(ValueError):b.failure_mode(1,1,1,0,1)
    def test_24_bool_rejected(self):
        with self.assertRaises(ValueError):b.failure_mode(True,1,0,1,0)
    def test_25_gate_unique_not_joint(self):
        self.assertTrue(b.gate([case()]));self.assertTrue(b.gate([case(1,0)]))
        self.assertFalse(b.gate([case(1,1)]));self.assertFalse(b.gate([case(0,0)]))
    def test_26_gate_coverage_and_identity(self):
        self.assertFalse(b.gate([]));self.assertFalse(b.gate([case(),case()]))
        c=case();c['seed']=181002;self.assertFalse(b.gate([c]))
    def test_27_gate_recomputes_classification(self):
        c=case(1,1);c['mode']='TREE_ONLY_SUFFICIENT';self.assertFalse(b.gate([c]))
    def test_28_syntax_render_no_evaluation(self):
        r=raw_row();d=b.describe_row(r)
        self.assertEqual(d['expression'],'((F1 AND NOT F2) OR (F3 OR F4))')
        self.assertEqual(d['facts'][0]['value'],0);self.assertIsNone(d['facts'][1]['value'])
    def test_29_renderer_hidden_value_rejected(self):
        r=raw_row();r[53]=1
        with self.assertRaises(ValueError):b.describe_row(r)
    def test_30_no_labels_in_intervention(self):
        self.assertEqual(list(inspect.signature(b.hybrid_inputs).parameters),['original','renamed'])
        self.assertNotIn('label',inspect.signature(b.capture_predict).parameters)
    def test_31_manifest_fixed(self):
        self.assertEqual(hashlib.sha256(b.blob(b.manifest())).hexdigest(),b.MANIFEST_SHA)
        self.assertEqual(b.manifest()['main_forward_rows'],6*2*9396)
        self.assertEqual(b.manifest()['main_cell_calls'],120*7)
    def test_32_nonfinite_json_rejected(self):
        with self.assertRaises(ValueError):b.blob(dict(x=float('nan')))


if __name__=='__main__':unittest.main()
