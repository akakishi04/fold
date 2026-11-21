"""Synthetic helper checks; no registered pilot data or full training run."""
import inspect
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import torch
from torch import nn

try:
    from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as b
except ModuleNotFoundError:
    import gate_e_c179_shared_graph as b


def inputs():
    # Explicit C178 scaled-bound format, two small synthetic examples.
    raw=torch.tensor([
        [1,1,1,0,0,0],[1,1,2,0,0,0],[1,2,0,1,2,0],
        [1,1,3,0,0,1],[1,1,4,0,0,0],[1,3,0,4,5,0],[1,2,0,3,6,0]],dtype=torch.float32)
    x=torch.zeros(2,72,dtype=torch.float32);x[:,:4]=1
    scale=torch.tensor([1,3,4,7,7,1],dtype=torch.float32)
    x[:,4:46]=(raw/scale).reshape(1,42)
    for i,k in [(0,0),(1,1),(3,2),(4,3)]:
        present=1 if k<2 else 0
        x[:,46+4*k:50+4*k]=torch.tensor([1,2/8 if present else 1/8,present,0.0])
        x[:,4+6*i+3]=present
    x[1,4+6*0+4]=1;x[1,49]=1
    x[:,62:]=torch.tensor([.25,.25,1,0,0,1,0,0,0,1])
    return x


def pairs():
    def score(n=.6,g=.7,r=.6):
        return dict(macro_missing_balanced_accuracy=n,metrics=dict(macro_group_balanced_accuracy=g,needs_recall=.7,sufficient_recall=.7),
            by_missing_count={'1':{'needs_recall':r},'3':{'sufficient_recall':r}})
    return [dict(seed=s,sequence=score(),tree=score(.7,.72,.65),paired_initial_equal=True,paired_batches_equal=True) for s in b.SEEDS]


class C179Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): torch.set_num_threads(2)

    def test_01_parameter_count(self):
        for arm in b.ARMS:self.assertEqual(sum(p.numel() for p in b.SharedGraphProbe(arm).parameters()),25726)

    def test_02_dense_mac_count(self):
        m=b.SharedGraphProbe(b.ARMS[0])
        cell=sum(x.in_features*x.out_features for x in m.cell if isinstance(x,nn.Linear))
        self.assertEqual(7*cell+m.readout.in_features*m.readout.out_features,b.MACS_PER_ROW)

    def test_03_pair_initial_weights(self):
        a,c=b.paired_initial(19);self.assertEqual(b.fingerprint(a),b.fingerprint(c));self.assertNotEqual(a.arm,c.arm)
        with torch.no_grad():next(c.parameters()).add_(1)
        self.assertNotEqual(b.fingerprint(a),b.fingerprint(c))

    def test_04_seed_validation(self):
        for seed in (True,-1,2**31,.5):
            with self.assertRaises(ValueError):b.paired_initial(seed)

    def test_05_routing_mode_is_explicit(self):
        with self.assertRaises(ValueError):b.SharedGraphProbe('UNKNOWN')

    def test_06_shape_dtype_nonfinite(self):
        for x in (inputs()[:,:71],inputs().double(),inputs()[:0],torch.full((2,72),float('nan'))):
            with self.assertRaises(ValueError):b.tree_links(x)

    def test_07_bad_header_and_mask(self):
        for col in (0,1,4):
            x=inputs();x[0,col]=0
            with self.assertRaises(ValueError):b.tree_links(x)

    def test_08_noncanonical_kind(self):
        x=inputs();x[0,5]=.5
        with self.assertRaises(ValueError):b.tree_links(x)

    def test_09_leaf_links_are_zero_not_visible_bits(self):
        _,l=b.tree_links(inputs());self.assertEqual(l[:,[0,1,3,4]].count_nonzero().item(),0)
        self.assertTrue(torch.equal(l[0,6],torch.tensor([3,6])))

    def test_10_forward_pointer_rejected(self):
        x=inputs();x[0,4+6*2+3]=6/7
        with self.assertRaises(ValueError):b.tree_links(x)

    def test_11_noninteger_pointer_rejected(self):
        x=inputs();x[0,4+6*2+3]=.11
        with self.assertRaises(ValueError):b.tree_links(x)

    def test_12_disconnected_tree_rejected(self):
        x=inputs();x[0,4+6*6+3]=1/7
        with self.assertRaises(ValueError):b.tree_links(x)

    def test_13_both_arms_have_seven_cell_calls(self):
        for arm in b.ARMS:
            m=b.SharedGraphProbe(arm);y=m(inputs());self.assertEqual(tuple(y.shape),(2,2))
            self.assertEqual((m.calls,m.cell_calls,m.rows),(1,7,2))

    def test_14_same_local_inputs_different_links(self):
        histories=[]
        for arm in b.ARMS:
            m=b.SharedGraphProbe(arm);r=[]
            h=m.cell.register_forward_pre_hook(lambda mod,args:r.append(args[0].detach().clone()))
            m(inputs());h.remove();histories.append(r)
        for i in range(7):self.assertTrue(torch.equal(histories[0][i][:,:6],histories[1][i][:,:6]))
        self.assertTrue(torch.equal(histories[1][1][:,6:],torch.zeros(2,128)))
        self.assertGreater(histories[0][1][:,6:70].abs().sum().item(),0)
        self.assertGreater(histories[0][2][:,70:].abs().sum().item(),0)

    def test_15_child_values_match_selected_states(self):
        m=b.SharedGraphProbe(b.ARMS[1]);ins=[];outs=[]
        h=m.cell.register_forward_pre_hook(lambda mod,args:ins.append(args[0].detach().clone()))
        j=m.cell.register_forward_hook(lambda mod,args,out:outs.append(out.detach().clone()))
        m(inputs());h.remove();j.remove()
        self.assertTrue(torch.equal(ins[6][:,6:70],outs[2]));self.assertTrue(torch.equal(ins[6][:,70:],outs[5]))

    def test_16_sequence_uses_previous_two(self):
        m=b.SharedGraphProbe(b.ARMS[0]);ins=[];outs=[]
        h=m.cell.register_forward_pre_hook(lambda mod,args:ins.append(args[0].detach().clone()))
        j=m.cell.register_forward_hook(lambda mod,args,out:outs.append(out.detach().clone()))
        m(inputs());h.remove();j.remove()
        self.assertTrue(torch.equal(ins[6][:,6:70],outs[5]));self.assertTrue(torch.equal(ins[6][:,70:],outs[4]))

    def test_17_gradient_through_graph(self):
        for arm in b.ARMS:
            m=b.SharedGraphProbe(arm);m(inputs()).square().sum().backward()
            self.assertTrue(all(p.grad is not None and torch.isfinite(p.grad).all() for p in m.parameters()))

    def test_18_no_input_or_parameter_mutation_during_forward(self):
        x=inputs();before=x.clone();m=b.SharedGraphProbe(b.ARMS[1]);h=b.fingerprint(m);m(x)
        self.assertTrue(torch.equal(x,before));self.assertEqual(h,b.fingerprint(m))

    def test_19_batch_permutation(self):
        m=b.SharedGraphProbe(b.ARMS[1]);x=inputs()
        torch.testing.assert_close(m(x)[[1,0]],m(x[[1,0]]),rtol=1e-5,atol=1e-7)

    def test_20_no_label_or_solver_forward_argument(self):
        self.assertEqual(list(inspect.signature(b.SharedGraphProbe.forward).parameters),['self','x'])
        self.assertNotIn('evaluate',inspect.getsource(b.SharedGraphProbe.forward))

    def test_21_toy_fit_pair_and_immutability(self):
        x=inputs();y=torch.tensor([0,1]);a,c=b.paired_initial(8);h=b.fingerprint(a)
        am,al=b.fit(a,x,y,8,steps=2,batch=2);cm,cl=b.fit(c,x,y,8,steps=2,batch=2)
        self.assertEqual(al['batch_schedule_sha256'],cl['batch_schedule_sha256']);self.assertEqual(h,b.fingerprint(a))
        self.assertEqual(al['training_cell_calls'],14);self.assertEqual(al['examples_drawn'],4)
        self.assertEqual(al['training_forward_calls'],2)

    def test_22_fit_rejects_bad_labels_and_workload(self):
        m=b.SharedGraphProbe(b.ARMS[0])
        for y,steps in [(torch.tensor([0,0]),2),(torch.tensor([0,1]),0)]:
            with self.assertRaises(ValueError):b.fit(m,inputs(),y,8,steps=steps,batch=2)

    def test_23_predict_meter_raw_argmax(self):
        m=b.SharedGraphProbe(b.ARMS[0]);h=b.fingerprint(m)
        p,z,r=b.predict(m,inputs(),batch=1)
        self.assertTrue(torch.equal(p,z.argmax(1)));self.assertEqual(r['forward_calls'],2)
        self.assertEqual(r['cell_calls'],14);self.assertEqual(h,b.fingerprint(m))

    def test_24_checkpoint_roundtrip_and_arm_binding(self):
        m=b.SharedGraphProbe(b.ARMS[1])
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'toy.pt';torch.save(dict(seed=8,arm=m.arm,steps=b.STEPS,representation=b.REPRESENTATION,
                model_schema=b.MODEL_SCHEMA,weight_sha256=b.fingerprint(m),state_dict=m.state_dict()),f)
            r=b.restore(f,8,m.arm);self.assertEqual(b.fingerprint(m),b.fingerprint(r))
            self.assertTrue(torch.equal(m(inputs()),r(inputs())))
            with self.assertRaises(ValueError):b.restore(f,8,b.ARMS[0])

    def test_25_gate_requires_all_seeds_and_integrity(self):
        p=pairs();self.assertTrue(b.gate(p));self.assertFalse(b.gate(p[:2]))
        p[0]['paired_initial_equal']=False;self.assertFalse(b.gate(p))

    def test_26_gate_strict_and_nondegradation(self):
        p=pairs();p[0]['tree']['macro_missing_balanced_accuracy']=.6;self.assertFalse(b.gate(p))
        p=pairs();p[1]['tree']['metrics']['macro_group_balanced_accuracy']=.699;self.assertFalse(b.gate(p))

    def test_27_gate_both_target_recalls_and_aggregate(self):
        for key in ('1','3'):
            p=pairs();field='needs_recall' if key=='1' else 'sufficient_recall'
            p[0]['tree']['by_missing_count'][key][field]=.6;self.assertFalse(b.gate(p))
        p=pairs();p[2]['tree']['metrics']['needs_recall']=.5;self.assertFalse(b.gate(p))

    def test_28_gate_nonfinite_and_serialization(self):
        p=pairs();p[0]['tree']['macro_missing_balanced_accuracy']=float('nan');self.assertFalse(b.gate(p))
        with self.assertRaises(ValueError):b.blob(p)

    def test_29_manifest_budget_and_no_old_mlp_claim(self):
        m=b.manifest();self.assertEqual(m['parameters'],25726);self.assertEqual(m['training_cell_calls'],7*m['updates'])
        self.assertEqual(m['inference_cell_calls'],7*m['inference_batches']);self.assertEqual(m['dense_macs_per_row'],177596)

    def test_30_zero_weights_do_not_solve_logic(self):
        for arm in b.ARMS:
            m=b.SharedGraphProbe(arm)
            with torch.no_grad():
                for p in m.parameters():p.zero_()
            self.assertTrue(torch.equal(m(inputs()),torch.zeros(2,2)))

    def test_31_checkpoint_metadata_and_tensor_hash(self):
        x=inputs();h=b.tensor_sha(x);x[0,49]=1;self.assertNotEqual(h,b.tensor_sha(x))
        self.assertNotIn('calls',b.SharedGraphProbe(b.ARMS[0]).state_dict())

    def test_32_link_decoder_is_deterministic_and_immutable(self):
        x=inputs();before=x.clone();a,l=b.tree_links(x);c,r=b.tree_links(x)
        self.assertTrue(torch.equal(x,before));self.assertTrue(torch.equal(l,r));self.assertTrue(torch.equal(a,c))


if __name__ == '__main__':unittest.main()
