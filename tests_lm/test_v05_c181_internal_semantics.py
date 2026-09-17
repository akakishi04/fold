"""C181 unit tests. Synthetic fixtures/two-update fits, not formal pilot scores."""
from copy import deepcopy
import hashlib
import inspect
import itertools
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import torch
from torch import nn
from fold_lm.v05_benchmarks import gate_e_c181_internal_semantics as b


def raw_case(values=(0,None,1,None),neg=0,ops=(2,3,3),comb=False):
    leaf=lambda i:[1,1,i,0,0,int(bool(neg & (1 << (i-1))))]
    if comb:
        nodes=[leaf(1),leaf(2),[1,ops[0],0,1,2,0],leaf(3),[1,ops[1],0,3,4,0],leaf(4),[1,ops[2],0,5,6,0]]
    else:
        nodes=[leaf(1),leaf(2),[1,ops[0],0,1,2,0],leaf(3),leaf(4),[1,ops[1],0,4,5,0],[1,ops[2],0,3,6,0]]
    facts=[[1,1,0,0] if v is None else [1,2,1,v] for v in values]
    return [7,4,1,1]+sum(nodes,[])+sum(facts,[])+[3,1,1,0,0,1,0,0,0,7]


def bound(raw):
    # Independent synthetic fixture conversion using the published C170/C178 layout.
    scales=(7,4,1,1)+(1,3,4,7,7,1)*7+(1,8,1,1)*4+(12,4,1,1,1,1,1,1,6,7)
    x=raw.float()/torch.tensor(scales,dtype=torch.float32)
    for r in range(len(raw)):
        for i in range(7):
            if raw[r,5+6*i] == 1:
                fact=int(raw[r,6+6*i])-1
                x[r,7+6*i]=raw[r,48+4*fact];x[r,8+6*i]=raw[r,49+4*fact]
    return x


def tiny():
    raw=torch.tensor([raw_case((0,None,1,None)),raw_case((1,None,0,None))],dtype=torch.int32)
    return raw,bound(raw),torch.tensor([0,1]),b.teacher_targets(raw)[1]


def good_pairs():
    def score(v):
        return dict(macro_missing_balanced_accuracy=v,metrics=dict(macro_group_balanced_accuracy=v,needs_recall=v,sufficient_recall=v),
                    by_missing_count={'1':{'needs_recall':v},'3':{'sufficient_recall':v}})
    return [dict(seed=s,final_only=score(.6),internal=score(.7),paired_initial_equal=True,paired_batches_equal=True) for s in b.SEEDS]


class InternalSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):torch.set_num_threads(2)

    def test_01_known_zero_short_circuit(self):
        r=torch.tensor([raw_case()],dtype=torch.int32);ix,y=b.teacher_targets(r)
        self.assertEqual(ix.tolist(),[[2,5]]);self.assertEqual(y.tolist(),[[0,1]])

    def test_02_known_one(self):
        r=torch.tensor([raw_case((1,1,0,0))],dtype=torch.int32)
        self.assertEqual(b.teacher_targets(r)[1].tolist(),[[1,0]])

    def test_03_unknown_stays_unknown(self):
        r=torch.tensor([raw_case((1,None,0,None))],dtype=torch.int32)
        self.assertEqual(b.teacher_targets(r)[1].tolist(),[[2,2]])

    def test_04_negation_affects_teacher_not_raw(self):
        r=torch.tensor([raw_case((1,None,0,None),neg=5)],dtype=torch.int32);copy=r.clone()
        self.assertEqual(b.teacher_targets(r)[1].tolist(),[[0,1]]);self.assertTrue(torch.equal(copy,r))

    def test_05_root_not_supervised(self):
        a=torch.tensor([raw_case(ops=(2,3,2))],dtype=torch.int32);c=a.clone();c[0,41]=3
        ia,ya=b.teacher_targets(a);ib,yb=b.teacher_targets(c)
        self.assertTrue(torch.equal(ia,ib));self.assertTrue(torch.equal(ya,yb));self.assertNotIn(6,ia[0].tolist())

    def test_06_repeated_variables_rejected(self):
        r=torch.tensor([raw_case()],dtype=torch.int32);r[0,6]=2
        with self.assertRaises(ValueError):b.teacher_targets(r)

    def test_07_hidden_payload_and_status_rejected(self):
        for col,val in ((53,1),(51,3),(52,1)):
            r=torch.tensor([raw_case()],dtype=torch.int32);r[0,col]=val
            with self.subTest(col=col),self.assertRaises(ValueError):b.teacher_targets(r)

    def test_08_teacher_shapes_and_types(self):
        for r in (torch.zeros((1,71),dtype=torch.int32),torch.zeros((0,72),dtype=torch.int32),torch.zeros((1,72)),torch.zeros((1,72),dtype=torch.bool)):
            with self.subTest(dtype=r.dtype),self.assertRaises(ValueError):b.teacher_targets(r)

    def test_09_independent_completion_enumeration(self):
        # Exhaustive visible assignments for two synthetic tree shapes/four sign patterns.
        for comb in (False,True):
            for neg in (0,3,5,15):
                rows=[raw_case(v,neg=neg,comb=comb) for v in itertools.product((None,0,1),repeat=4)]
                raw=torch.tensor(rows,dtype=torch.int32);ix,y=b.teacher_targets(raw)
                for j,row in enumerate(rows):
                    facts=[row[46+4*i:50+4*i] for i in range(4)]
                    observed=[None if f[2]==0 else f[3] for f in facts]
                    for k,node_id in enumerate(ix[j].tolist()):
                        outputs=set()
                        for assignment in itertools.product((0,1),repeat=4):
                            if any(v is not None and v!=assignment[i] for i,v in enumerate(observed)):continue
                            def ev(i):
                                n=row[4+6*i:10+6*i]
                                if n[1]==1:return assignment[n[2]-1]^n[5]
                                a,c=ev(n[3]-1),ev(n[4]-1)
                                return (a&c) if n[1]==2 else (a|c)
                            outputs.add(ev(node_id))
                        want=next(iter(outputs)) if len(outputs)==1 else 2
                        self.assertEqual(int(y[j,k]),want)

    def test_10_teacher_no_label_interface(self):
        self.assertEqual(list(inspect.signature(b.teacher_targets).parameters),['raw'])
        self.assertEqual(list(inspect.signature(b.SemanticProbe.forward).parameters),['self','x'])

    def test_11_row_permutation(self):
        r,_,_,_=tiny();a,c=b.teacher_targets(r);d,e=b.teacher_targets(r.flip(0))
        self.assertTrue(torch.equal(a.flip(0),d));self.assertTrue(torch.equal(c.flip(0),e))

    def test_12_neural_teacher_node_alignment(self):
        r=torch.tensor([raw_case(comb=v) for v in (False,True)],dtype=torch.int32)
        self.assertTrue(torch.equal(b.proper_indices(bound(r)),b.teacher_targets(r)[0]))

    def test_13_parameter_counts(self):
        m=b.SemanticProbe(b.ARMS[0]);self.assertEqual(sum(p.numel() for p in m.parameters()),25921)
        self.assertEqual(sum(p.numel() for p in m.base.parameters()),25726)

    def test_14_paired_initial(self):
        a,c=b.paired_initial(11);self.assertEqual(b.graph.fingerprint(a),b.graph.fingerprint(c))
        self.assertNotEqual(a.condition,c.condition)

    def test_15_main_forward_unchanged(self):
        _,x,_,_=tiny();m=b.SemanticProbe(b.ARMS[0]);a=m(x);c,az=m.training_forward(x)
        self.assertTrue(torch.equal(a,c));self.assertEqual(az.shape,(2,2,3));self.assertFalse(m.base.cell._forward_hooks)

    def test_16_aux_reads_actual_proper_states(self):
        _,x,_,_=tiny();m=b.SemanticProbe(b.ARMS[0]);states=[]
        h=m.base.cell.register_forward_hook(lambda mod,args,out:states.append(out));m(x);h.remove()
        ix=b.proper_indices(x);want=m.auxiliary(torch.stack(states,1)[torch.arange(2)[:,None],ix])
        _,actual=m.training_forward(x);self.assertTrue(torch.equal(want,actual))

    def test_17_aux_signal_reaches_shared_cell(self):
        _,x,y,t=tiny();a,c=b.paired_initial(11)
        for m in (a,c):
            z,az=m.training_forward(x);loss,_,_=b.objective(z,az,y,t,m.condition);loss.backward()
        self.assertFalse(torch.equal(a.base.cell[0].weight.grad,c.base.cell[0].weight.grad))

    def test_18_zero_coefficient_gives_zero_aux_gradient(self):
        _,x,y,t=tiny();m=b.SemanticProbe(b.ARMS[0]);z,az=m.training_forward(x)
        b.objective(z,az,y,t,m.condition)[0].backward()
        self.assertTrue(all(p.grad is not None and torch.count_nonzero(p.grad)==0 for p in m.auxiliary.parameters()))

    def test_19_unit_coefficient_trains_aux(self):
        _,x,y,t=tiny();m=b.SemanticProbe(b.ARMS[1]);z,az=m.training_forward(x)
        b.objective(z,az,y,t,m.condition)[0].backward()
        self.assertTrue(any(torch.count_nonzero(p.grad)>0 for p in m.auxiliary.parameters()))

    def test_20_loss_is_mean_not_node_sum(self):
        z=torch.tensor([[.2,.3],[.1,.4]]);az=torch.ones((2,2,3));y=torch.tensor([0,1]);t=torch.tensor([[0,2],[1,2]])
        total,main,aux=b.objective(z,az,y,t,b.ARMS[1])
        self.assertEqual(float(total),float(main+aux));self.assertAlmostEqual(float(aux),float(torch.log(torch.tensor(3.))))

    def test_21_fit_preserves_inputs(self):
        _,x,y,t=tiny();m=b.paired_initial(12)[0];before=[b.graph.fingerprint(m),x.clone(),y.clone(),t.clone()]
        b.fit(m,x,y,t,12,steps=2,batch=2)
        self.assertEqual(before[0],b.graph.fingerprint(m))
        for a,c in zip(before[1:],(x,y,t)):self.assertTrue(torch.equal(a,c))

    def test_22_two_update_determinism(self):
        _,x,y,t=tiny();m=b.paired_initial(12)[1];a,_=b.fit(m,x,y,t,12,steps=2,batch=2);c,_=b.fit(m,x,y,t,12,steps=2,batch=2)
        self.assertEqual(b.graph.fingerprint(a),b.graph.fingerprint(c))

    def test_23_paired_schedules_and_meters(self):
        _,x,y,t=tiny();a,c=b.paired_initial(13)
        a,ha=b.fit(a,x,y,t,13,steps=2,batch=2);c,hc=b.fit(c,x,y,t,13,steps=2,batch=2)
        self.assertEqual(ha['batch_schedule_sha256'],hc['batch_schedule_sha256'])
        self.assertEqual((a.base.calls,a.base.cell_calls,a.auxiliary_calls,a.auxiliary_rows),(2,14,2,8))

    def test_24_zero_aux_matches_original_fit(self):
        _,x,y,t=tiny();m=b.paired_initial(17)[0]
        a,_=b.fit(m,x,y,t,17,steps=2,batch=2);c,_=b.graph.fit(m.base,x,y,17,steps=2,batch=2)
        self.assertEqual(b.graph.fingerprint(a.base),b.graph.fingerprint(c))

    def test_25_inference_never_calls_teacher_or_head(self):
        _,x,_,_=tiny();m=b.SemanticProbe(b.ARMS[1])
        with patch.object(b,'teacher_targets',side_effect=RuntimeError('teacher')),patch.object(m.auxiliary,'forward',side_effect=RuntimeError('head')):
            p,z,meter=b.predict(m,x)
        self.assertEqual(m.auxiliary_calls,0);self.assertEqual(meter['cell_calls'],7)

    def test_26_checkpoint_roundtrip(self):
        _,x,_,_=tiny();m=b.paired_initial(31)[1]
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'m.pt';torch.save(b.checkpoint_payload(m,31),path);c=b.restore(path,31,b.ARMS[1])
            self.assertTrue(torch.equal(m(x),c(x)))

    def test_27_checkpoint_contract_tamper(self):
        m=b.paired_initial(31)[0]
        for key,val in [('alpha',1),('root_supervision',True),('model_schema','wrong')]:
            with tempfile.TemporaryDirectory() as td:
                p=b.checkpoint_payload(m,31);p[key]=val;path=Path(td)/'m.pt';torch.save(p,path)
                with self.assertRaises(ValueError):b.restore(path,31,b.ARMS[0])

    def test_28_checkpoint_weights_tamper(self):
        m=b.paired_initial(31)[0]
        with tempfile.TemporaryDirectory() as td:
            p=deepcopy(b.checkpoint_payload(m,31));next(iter(p['state_dict'].values())).add_(1)
            path=Path(td)/'m.pt';torch.save(p,path)
            with self.assertRaises(ValueError):b.restore(path,31,b.ARMS[0])

    def test_29_raw_argmax_not_repaired(self):
        _,x,_,_=tiny();m=b.SemanticProbe(b.ARMS[1])
        with torch.no_grad():
            for p in m.parameters():p.zero_()
        p,z,_=b.predict(m,x);self.assertEqual(p.tolist(),[0,0]);self.assertTrue(torch.equal(p,z.argmax(1)))

    def test_30_invalid_loss_targets_and_nonfinite(self):
        z=torch.zeros((2,2));az=torch.zeros((2,2,3));y=torch.tensor([0,1]);t=torch.tensor([[0,1],[2,0]])
        for zz,tt in ((z+float('nan'),t),(z,t+4),(z,t.float())):
            with self.assertRaises(ValueError):b.objective(zz,az,y,tt,b.ARMS[0])

    def test_31_gate_all_seeds_and_pair_integrity(self):
        p=good_pairs();self.assertTrue(b.gate(p));self.assertFalse(b.gate(p[:-1]))
        p[1]['paired_initial_equal']=False;self.assertFalse(b.gate(p))

    def test_32_gate_strict_primary_and_minority_gains(self):
        for where in ('primary','one','three'):
            p=good_pairs()
            if where=='primary':p[0]['internal']['macro_missing_balanced_accuracy']=.6
            else:p[0]['internal']['by_missing_count']['1' if where=='one' else '3']['needs_recall' if where=='one' else 'sufficient_recall']=.6
            self.assertFalse(b.gate(p))

    def test_33_gate_group_equality_and_recalls(self):
        p=good_pairs();p[0]['internal']['metrics']['macro_group_balanced_accuracy']=.6;self.assertTrue(b.gate(p))
        for v in (.5,float('nan')):
            p=good_pairs();p[2]['internal']['metrics']['needs_recall']=v;self.assertFalse(b.gate(p))

    def test_34_additive_regression_list(self):
        fake=SimpleNamespace(regression_modules=lambda root:[f'old{i}' for i in range(64)])
        import fold_lm.v05_benchmarks as package
        with patch.object(package,'gate_e_c180_fact_bypass',fake,create=True),patch.dict(sys.modules,{'fold_lm.v05_benchmarks.gate_e_c180_fact_bypass':fake}):
            names=b.regression_modules(Path('.'))
        self.assertEqual(len(names),65);self.assertEqual(len(set(names)),65)

    def test_35_frozen_manifest(self):
        m=b.manifest();self.assertEqual(hashlib.sha256(b.blob(m)).hexdigest(),b.MANIFEST_SHA)
        self.assertEqual((m['teacher_rows'],m['unique_teacher_targets'],m['pilot_teacher_targets']),(42444,84888,0))
        self.assertEqual(m['training_forward_dense_macs_per_row']-m['inference_dense_macs_per_row'],384)

    def test_36_hook_cleanup_after_exception(self):
        _,x,_,_=tiny();m=b.SemanticProbe(b.ARMS[0])
        with patch.object(m.base.cell,'forward',side_effect=RuntimeError('synthetic')):
            with self.assertRaises(RuntimeError):m.training_forward(x)
        self.assertFalse(m.base.cell._forward_hooks)


if __name__=='__main__':unittest.main()
