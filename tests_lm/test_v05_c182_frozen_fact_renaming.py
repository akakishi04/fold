"""C182 helper tests use synthetic inputs, never the deciding checkpoints or cases."""
from copy import deepcopy
import hashlib
import inspect
import itertools
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import numpy as np
import torch
from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as b
from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph


def raw_row(values=(1, None, 0, 1), shape=((0, 1), (2, 3)), neg=(0, 1, 0, 0)):
    nodes=[]; ops=iter((3, 2, 3))
    def emit(s):
        if type(s) is int: nodes.append([1, 1, s+1, 0, 0, neg[s]])
        else:
            op=next(ops); left=emit(s[0]); right=emit(s[1]); nodes.append([1, op, 0, left, right, 0])
        return len(nodes)
    emit(shape)
    facts=[[1, 1, 0, 0] if v is None else [1, 2, 1, v] for v in values]
    return torch.tensor([[7, 4, 0, 0]+sum(nodes, [])+sum(facts, [])+[12, 4, 1, 1, 1, 1, 1, 1, 0, 0]],dtype=torch.int32)


def completions(raw):
    row=raw[0].tolist(); facts=[row[46+4*i:50+4*i] for i in range(4)]
    missing=[i for i,f in enumerate(facts) if not f[2]]; out=set()
    for bits in itertools.product((0,1),repeat=len(missing)):
        values=[f[3] for f in facts]
        for i,v in zip(missing,bits):values[i]=v
        state=[]
        for i in range(7):
            _,kind,f,left,right,neg=row[4+6*i:10+6*i]
            if kind==1: v=values[f-1]^neg
            elif kind==2: v=state[left-1]&state[right-1]
            else:v=state[left-1]|state[right-1]
            state.append(v)
        out.add(state[-1])
    return out


def payload():
    model=graph.SharedGraphProbe(graph.ARMS[1]);aux=torch.nn.Linear(64,3)
    state={'base.'+k:v.clone() for k,v in model.state_dict().items()}
    state.update({'auxiliary.'+k:v.clone() for k,v in aux.state_dict().items()})
    p=dict(seed=b.SEEDS[0],condition=b.ARMS[1],model_schema=b.SCHEMA,representation=b.REPRESENTATION,
           proper_nodes_only=True,root_supervision=False,steps=2000,alpha=1,classes=b.CLASSES,
           state_dict=state,weight_sha256=b.state_fingerprint(state))
    return p,model


def records():
    return [dict(seed=s,arm=a,permutation_index=j,n=9396,errors=0,decision_flips=0)
            for j in range(1,24) for s in b.SEEDS for a in b.ARMS]


class FrozenRenamingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):torch.set_num_threads(2)
    def test_01_permutation_set(self):
        self.assertEqual(len(set(b.PERMUTATIONS)),24);self.assertEqual(b.PERMUTATIONS[0],b.IDENTITY)
    def test_02_bad_permutations(self):
        for p in ((0,0,2,3),(0,1,2),(0,1,2,4),(False,1,2,3),(0.,1,2,3),'0123'):
            with self.assertRaises(ValueError):b.permutation(p)
    def test_03_identity_copy(self):
        x=raw_row();y=b.rename_raw(x,b.IDENTITY);self.assertTrue(torch.equal(x,y));self.assertNotEqual(x.data_ptr(),y.data_ptr())
    def test_04_whole_fact_records(self):
        x=raw_row();p=(2,0,3,1);y=b.rename_raw(x,p)
        self.assertTrue(torch.equal(y[:,46:62].reshape(-1,4,4)[:,list(p)],x[:,46:62].reshape(-1,4,4)))
    def test_05_references_follow_mapping(self):
        p=(2,0,3,1);nodes=b.rename_raw(raw_row(),p)[:,4:46].reshape(-1,7,6)
        self.assertEqual(nodes[:,:,2][nodes[:,:,1]==1].tolist(),[3,1,4,2])
    def test_06_inverse(self):
        x=raw_row()
        for p in b.PERMUTATIONS:
            inverse=tuple(p.index(i) for i in range(4))
            self.assertTrue(torch.equal(b.rename_raw(b.rename_raw(x,p),inverse),x))
    def test_07_composition(self):
        x=raw_row();p=(2,0,3,1);q=(1,3,0,2)
        self.assertTrue(torch.equal(b.rename_raw(b.rename_raw(x,p),q),b.rename_raw(x,tuple(q[p[i]] for i in range(4)))))
    def test_08_other_fields_preserved(self):
        x=raw_row();y=b.rename_raw(x,(3,2,1,0));keep=torch.ones(72,dtype=torch.bool);keep[46:62]=False;keep[6:46:6]=False
        self.assertTrue(torch.equal(x[:,keep],y[:,keep]))
    def test_09_no_mutation(self):
        x=raw_row();old=x.clone();b.rename_raw(x,(3,2,1,0));self.assertTrue(torch.equal(x,old))
    def test_10_bound_leaf_information_preserved(self):
        x=raw_row();a=binding.prepare_pair(x)[1][:,4:46].reshape(-1,7,6)
        for p in b.PERMUTATIONS:
            c=binding.prepare_pair(b.rename_raw(x,p))[1][:,4:46].reshape(-1,7,6)
            self.assertTrue(torch.equal(a[:,:,[0,1,3,4,5]],c[:,:,[0,1,3,4,5]]))
    def test_11_independent_semantics_enumeration(self):
        shapes=((((0,1),2),3),((0,(1,2)),3),((0,1),(2,3)),(0,((1,2),3)),(0,(1,(2,3))))
        for shape in shapes:
            for values in itertools.product((None,0,1),repeat=4):
                x=raw_row(values,shape);want=completions(x)
                for p in b.PERMUTATIONS:self.assertEqual(completions(b.rename_raw(x,p)),want)
    def test_12_hidden_payload_rejected(self):
        x=raw_row();x[0,53]=1
        with self.assertRaises(ValueError):b.rename_raw(x,b.IDENTITY)
    def test_13_invalid_raw(self):
        for x in (raw_row().float(),raw_row()[:,:71],torch.zeros((0,72),dtype=torch.int32)):
            with self.assertRaises(ValueError):b.rename_raw(x,b.IDENTITY)
    def test_14_new_leaf_orders_unique(self):
        values=[]
        for p in b.PERMUTATIONS[1:]:
            n=b.rename_raw(raw_row(),p)[:,4:46].reshape(-1,7,6);v=tuple(n[:,:,2][n[:,:,1]==1].tolist());self.assertNotEqual(v,(1,2,3,4));values.append(v)
        self.assertEqual(len(set(values)),23)
    def test_15_batch_equivariance(self):
        x=torch.cat([raw_row(),raw_row((None,0,1,None))]);p=(3,0,1,2)
        self.assertTrue(torch.equal(b.rename_raw(x.flip(0),p),b.rename_raw(x,p).flip(0)))
    def test_16_no_labels_in_transform_or_inference(self):
        self.assertEqual(list(inspect.signature(b.rename_raw).parameters),['raw','old_to_new'])
        self.assertEqual(list(inspect.signature(graph.SharedGraphProbe.forward).parameters),['self','x'])
    def test_17_bare_restore_capacity(self):
        p,_=payload();m=b.bare_from_payload(p,b.SEEDS[0],b.ARMS[1],p['weight_sha256'])
        self.assertEqual(type(m),graph.SharedGraphProbe);self.assertFalse(hasattr(m,'auxiliary'));self.assertEqual(sum(t.numel() for t in m.parameters()),25726)
    def test_18_full_fingerprint_covers_auxiliary(self):
        p,_=payload();p['state_dict']['auxiliary.bias'][0]+=1
        with self.assertRaises(ValueError):b.bare_from_payload(p,b.SEEDS[0],b.ARMS[1],p['weight_sha256'])
    def test_19_contract_tamper(self):
        for k,v in [('seed',123),('condition',b.ARMS[0]),('root_supervision',True),('steps',2001),('alpha',0),('classes',('A','B','C'))]:
            p,_=payload();p[k]=v
            with self.assertRaises(ValueError):b.bare_from_payload(p,b.SEEDS[0],b.ARMS[1],p['weight_sha256'])
    def test_20_tensor_schema_and_nonfinite(self):
        for value in (torch.zeros(1),torch.tensor([float('nan'),0,0])):
            p,_=payload();p['state_dict']['auxiliary.bias']=value
            with self.assertRaises(ValueError):
                p['weight_sha256']=b.state_fingerprint(p['state_dict']);b.bare_from_payload(p,b.SEEDS[0],b.ARMS[1],p['weight_sha256'])
    def test_21_bare_numerical_parity(self):
        p,old=payload();m=b.bare_from_payload(p,b.SEEDS[0],b.ARMS[1],p['weight_sha256']);x=binding.prepare_pair(raw_row())[1]
        self.assertTrue(torch.equal(graph.predict(m,x)[1],graph.predict(old,x)[1]))
    def test_22_rng_preserved(self):
        p,_=payload();state=torch.random.get_rng_state().clone();b.bare_from_payload(p,b.SEEDS[0],b.ARMS[1],p['weight_sha256']);self.assertTrue(torch.equal(state,torch.random.get_rng_state()))
    def test_23_frozen_weights_and_meters(self):
        p,_=payload();m=b.bare_from_payload(p,b.SEEDS[0],b.ARMS[1],p['weight_sha256']);h=graph.fingerprint(m)
        self.assertTrue(all(not t.requires_grad for t in m.parameters()));_,_,r=graph.predict(m,binding.prepare_pair(raw_row())[1]);self.assertEqual((r['rows'],r['cell_calls']),(1,7));self.assertEqual(h,graph.fingerprint(m))
    def test_24_file_restore_weights_only(self):
        p,_=payload()
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'toy.pt';torch.save(p,f);m=b.restore_bare(f,b.SEEDS[0],b.ARMS[1],p['weight_sha256']);self.assertEqual(type(m),graph.SharedGraphProbe)
    def test_25_replay_exact(self):
        p=np.array([0,1]);z=np.array([[2.,0.],[0.,2.]],dtype=np.float32);r=b.replay_check(p,z,p,z);self.assertEqual(r['max_abs_logit_difference'],0)
    def test_26_replay_fixed_tolerance(self):
        p=np.array([0]);z=np.array([[1.,0.]]);b.replay_check(p,z,p,z+5e-7)
        with self.assertRaises(ValueError):b.replay_check(p,z,p,z+2e-6)
    def test_27_repaired_or_nonfinite_predictions_rejected(self):
        for p,z,sp,sz in [(np.array([1]),np.array([[1.,0.]]),np.array([0]),np.array([[1.,0.]])),(np.array([0]),np.array([[float('nan'),0.]]),np.array([0]),np.array([[1.,0.]]))]:
            with self.assertRaises(ValueError):b.replay_check(p,z,sp,sz)
    def test_28_gate_coverage(self):
        r=records();self.assertTrue(b.gate(r));self.assertFalse(b.gate(r[:-1]));self.assertFalse(b.gate(r[::-1]))
    def test_29_every_candidate_and_permutation_required(self):
        for s in b.SEEDS:
            r=records();next(x for x in r if x['seed']==s and x['arm']==b.ARMS[1] and x['permutation_index']==23)['errors']=1;self.assertFalse(b.gate(r))
        r=records();r[1]['decision_flips']=1;self.assertFalse(b.gate(r))
    def test_30_controls_not_required_perfect(self):
        r=records()
        for x in r:
            if x['arm']==b.ARMS[0]:x['errors']=9000;x['decision_flips']=8000
        self.assertTrue(b.gate(r))
    def test_31_frozen_manifest(self):
        self.assertEqual(hashlib.sha256(b.blob(b.manifest())).hexdigest(),b.MANIFEST_SHA)
        m=b.manifest();self.assertEqual(m['new_training'],0);self.assertEqual(m['total_inference_rows'],6*(42444+24*9396));self.assertEqual(m['inference_batches'],6*(42+24*10))
    def test_32_additive_regression_list(self):
        names=['tests_lm.historical_'+str(i) for i in range(65)]
        with mock.patch('fold_lm.v05_benchmarks.gate_e_c181_internal_semantics.regression_modules',return_value=names):
            actual=b.regression_modules(Path('.'));self.assertEqual(actual[:-1],names);self.assertEqual(len(actual),66)


if __name__=='__main__':unittest.main()
