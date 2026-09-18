import importlib.util
import inspect
import itertools
import hashlib
import unittest
from pathlib import Path

import numpy as np
import torch

try:
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as c188
except ModuleNotFoundError:
    MOD_PATH=Path(__file__).with_name("gate_e_c188_multimissing_target_selection.py")
    spec=importlib.util.spec_from_file_location("c188",MOD_PATH)
    c188=importlib.util.module_from_spec(spec); spec.loader.exec_module(c188)

SHAPES=((((0,1),2),3),((0,(1,2)),3),((0,1),(2,3)),(0,((1,2),3)),(0,(1,(2,3))))
BITS=tuple(itertools.product((0,1),repeat=4))
PARTIAL=tuple(itertools.product((None,0,1),repeat=4))
PERMS=tuple(itertools.permutations(range(4)))

def eval_shape(shape,ops,neg,vals):
    it=iter(ops)
    def rec(s):
        if isinstance(s,int): return vals[s]^neg[s]
        op=next(it); a=rec(s[0]); b=rec(s[1])
        return a&b if op=="AND" else a|b
    return rec(shape)

def sem_group(table):
    tabs=[]
    for p in PERMS:
        renamed=tuple(table[BITS.index(tuple(b[p[i]] for i in range(4)))] for b in BITS)
        tabs += [renamed,tuple(1-v for v in renamed)]
    return min(tabs)

def known_groups():
    specs=((SHAPES[2],("OR","AND","AND")),(SHAPES[4],("OR","AND","OR")))
    return {sem_group(tuple(eval_shape(s,ops,(0,0,0,0),b) for b in BITS)) for s,ops in specs}
KG=known_groups()

def split_for(g):
    if g in KG: return 0
    d=hashlib.sha256(("C174:function-permutation-split:v1|"+''.join(map(str,g))).encode()).digest()
    return int(int.from_bytes(d[:8],"big")%5==0)

def raw_row(vis):
    x=np.zeros(72,dtype=np.int32); x[0]=7; x[1]=4
    for i,v in enumerate(vis):
        x[46+4*i]=1
        x[47+4*i]=1 if v is None else 2
        x[48+4*i]=0 if v is None else 1
        x[49+4*i]=0 if v is None else v
    return x

def leaf_raw(vis=(None,0,1,0), ids=(1,2,3,4)):
    x=raw_row(vis)
    for i,fid in enumerate(ids):
        x[4+6*i:10+6*i]=[1,1,fid,0,0,0]
    x[28:34]=[1,2,0,1,2,0]
    x[34:40]=[1,3,0,3,4,0]
    x[40:46]=[1,2,0,5,6,0]
    return x

class C188Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        features=[]; labels=[]; tids=[]; splits=[]; metadata=[]; groups=[]
        group_names=set(); templates=[]
        ti=0
        for shape in SHAPES:
            for ops in itertools.product(("AND","OR"),repeat=3):
                for neg in itertools.product((0,1),repeat=4):
                    table=tuple(eval_shape(shape,ops,neg,b) for b in BITS)
                    g=sem_group(table); sp=split_for(g)
                    metadata.append({"truth_table":list(table)})
                    templates.append((g,sp))
                    group_names.add(g)
                    for vis in PARTIAL:
                        outs={v for b,v in zip(BITS,table) if all(a is None or a==bb for a,bb in zip(vis,b))}
                        features.append(raw_row(vis)); labels.append(int(len(outs)==2)); tids.append(ti); splits.append(sp)
                    ti+=1
        ordered=sorted(group_names)
        for tid in tids: groups.append(ordered.index(templates[tid][0]))
        cls.features=np.stack(features)
        cls.labels=np.asarray(labels,dtype=np.int64)
        cls.tids=np.asarray(tids,dtype=np.int32)
        cls.splits=np.asarray(splits,dtype=np.uint8)
        cls.groups=np.asarray(groups,dtype=np.int32)
        cls.metadata=metadata
        cls.valid=c188.influence_masks(cls.features,cls.tids,cls.metadata)
        cls.train,cls.evdisc,cls.evfull,cls.miss,cls.profile=c188.cohort_masks(
            cls.features,cls.labels,cls.splits,cls.valid)

    def test_01_parameter_count(self):
        self.assertEqual(c188.HEAD_PARAMETERS,29249)
        self.assertEqual(sum(p.numel() for p in c188.TargetSelector().parameters()),29249)

    def test_02_visible_zero_is_observed(self):
        self.assertEqual(c188.visible_tuple(raw_row((0,None,1,None))),(0,None,1,None))

    def test_03_missing_mask_uses_presence(self):
        m=c188.missing_mask(torch.from_numpy(np.stack([raw_row((0,None,1,None))])))
        self.assertEqual(m.tolist(),[[False,True,False,True]])

    def test_04_leaf_positions(self):
        p=c188.leaf_positions(torch.from_numpy(np.stack([leaf_raw()])))
        self.assertEqual(p.tolist(),[[0,1,2,3]])

    def test_05_repeated_fact_rejected(self):
        with self.assertRaises(ValueError):
            c188.leaf_positions(torch.from_numpy(np.stack([leaf_raw(ids=(1,1,3,4))])))

    def test_06_influence_and(self):
        table=[b[0]&b[1] for b in BITS]
        v=c188.influence_masks(np.stack([raw_row((1,None,0,0))]),np.array([0]),[{"truth_table":table}])
        self.assertEqual(v.tolist(),[[False,True,False,False]])

    def test_07_influence_or_short_circuit(self):
        table=[b[0]|b[1] for b in BITS]
        v=c188.influence_masks(np.stack([raw_row((1,None,0,0))]),np.array([0]),[{"truth_table":table}])
        self.assertEqual(v.tolist(),[[False,False,False,False]])

    def test_08_influence_multiple_valid(self):
        table=[b[0]^b[1] for b in BITS]
        v=c188.influence_masks(np.stack([raw_row((None,None,0,0))]),np.array([0]),[{"truth_table":table}])
        self.assertEqual(v.tolist(),[[True,True,False,False]])

    def test_09_teacher_interface_has_no_labels(self):
        self.assertNotIn("labels",inspect.signature(c188.influence_masks).parameters)

    def test_10_registered_cohort_counts(self):
        self.assertEqual(self.profile["train_discriminating"],3824)
        self.assertEqual(self.profile["eval_discriminating"],528)
        self.assertEqual(self.profile["eval_full_multimissing"],1768)

    def test_11_registered_target_size_counts(self):
        self.assertEqual(self.profile["train_m3_valid1"],440)
        self.assertEqual(self.profile["train_m3_valid2"],688)
        self.assertEqual(self.profile["eval_m3_valid1"],72)
        self.assertEqual(self.profile["eval_m3_valid2"],80)

    def test_12_frequency_reference_keys(self):
        counts=c188.build_frequency_reference(self.features[self.train],self.valid[self.train])
        self.assertEqual(len(counts),32)

    def test_13_first_unknown_reference_exact(self):
        p=c188.first_unknown(self.features[self.evdisc])
        m=c188.target_metrics(self.valid[self.evdisc],self.features[self.evdisc],p,self.groups[self.evdisc])
        self.assertEqual((m["by_missing_count"]["2"]["hits"],m["by_missing_count"]["3"]["hits"]),(188,84))

    def test_14_frequency_reference_exact(self):
        counts=c188.build_frequency_reference(self.features[self.train],self.valid[self.train])
        p=c188.apply_frequency_reference(counts,self.features[self.evdisc])
        m=c188.target_metrics(self.valid[self.evdisc],self.features[self.evdisc],p,self.groups[self.evdisc])
        self.assertEqual((m["by_missing_count"]["2"]["hits"],m["by_missing_count"]["3"]["hits"]),(268,128))

    def test_15_frequency_reference_no_unseen_key(self):
        counts=c188.build_frequency_reference(self.features[self.train],self.valid[self.train])
        for row in self.features[self.evdisc]:
            self.assertIn(c188.blind_key(row),counts)

    def test_16_frequency_tie_uses_low_slot(self):
        row=raw_row((None,None,0,0)); counts={c188.blind_key(row):[2,2,0,0]}
        self.assertEqual(int(c188.apply_frequency_reference(counts,np.stack([row]))[0]),0)

    def test_17_unseen_reference_has_no_fallback(self):
        row=raw_row((None,None,0,0))
        with self.assertRaises(ValueError):
            c188.apply_frequency_reference({},np.stack([row]))

    def test_18_target_metrics_counts_observed_selection(self):
        rows=np.stack([raw_row((None,None,0,0)),raw_row((None,None,None,0))])
        valid=np.array([[1,0,0,0],[0,1,0,0]],dtype=bool)
        p=np.array([2,1],dtype=np.int8)
        m=c188.target_metrics(valid,rows,p)
        self.assertEqual(m["selected_observed"],1)

    def test_19_selector_forward_shape(self):
        m=c188.TargetSelector()
        z=m(torch.zeros((5,4,c188.FEATURES),dtype=torch.float32))
        self.assertEqual(tuple(z.shape),(5,4))

    def test_20_selection_loss_single_valid(self):
        z=torch.tensor([[0.,1.,2.,3.]])
        u=torch.tensor([[1,1,0,0]],dtype=torch.bool)
        v=torch.tensor([[0,1,0,0]],dtype=torch.bool)
        got=c188.selection_loss(z,u,v)
        want=torch.logsumexp(torch.tensor([0.,1.]),0)-torch.tensor(1.)
        self.assertAlmostEqual(float(got),float(want),places=7)

    def test_21_selection_loss_set_mass(self):
        z=torch.tensor([[0.,1.,2.,-1.]])
        u=torch.tensor([[1,1,1,0]],dtype=torch.bool)
        v=torch.tensor([[0,1,1,0]],dtype=torch.bool)
        got=c188.selection_loss(z,u,v)
        self.assertGreaterEqual(float(got),0.0)

    def test_22_loss_rejects_observed_valid(self):
        z=torch.zeros((1,4)); u=torch.tensor([[1,0,1,0]],dtype=torch.bool)
        v=torch.tensor([[0,1,0,0]],dtype=torch.bool)
        with self.assertRaises(ValueError): c188.selection_loss(z,u,v)

    def test_23_loss_rejects_nondiscriminating(self):
        z=torch.zeros((1,4)); u=torch.tensor([[1,1,0,0]],dtype=torch.bool)
        v=u.clone()
        with self.assertRaises(ValueError): c188.selection_loss(z,u,v)

    def test_24_head_initial_deterministic(self):
        a=c188.paired_head_initial(188001); b=c188.paired_head_initial(188001)
        self.assertEqual(c188.head_fingerprint(a),c188.head_fingerprint(b))

    def test_25_head_seed_changes_initial(self):
        a=c188.paired_head_initial(188001); b=c188.paired_head_initial(188002)
        self.assertNotEqual(c188.head_fingerprint(a),c188.head_fingerprint(b))

    def test_26_toy_fit_deterministic(self):
        f=torch.randn((8,4,c188.FEATURES),generator=torch.Generator().manual_seed(1))
        u=torch.tensor([[1,1,0,0]]*8,dtype=torch.bool)
        v=torch.tensor([[1,0,0,0],[0,1,0,0]]*4,dtype=torch.bool)
        init=c188.paired_head_initial(188001)
        a,ha=c188.fit_selector(init,f,u,v,188001,steps=2,batch=4)
        b,hb=c188.fit_selector(init,f,u,v,188001,steps=2,batch=4)
        self.assertEqual(c188.head_fingerprint(a),c188.head_fingerprint(b))
        self.assertEqual(ha["batch_schedule_sha256"],hb["batch_schedule_sha256"])

    def test_27_toy_fit_preserves_initial_and_features(self):
        f=torch.randn((8,4,c188.FEATURES),generator=torch.Generator().manual_seed(2))
        u=torch.tensor([[1,1,0,0]]*8,dtype=torch.bool)
        v=torch.tensor([[1,0,0,0],[0,1,0,0]]*4,dtype=torch.bool)
        init=c188.paired_head_initial(188001); ih=c188.head_fingerprint(init); fh=c188.tensor_sha(f)
        c188.fit_selector(init,f,u,v,188001,steps=2,batch=4)
        self.assertEqual((ih,fh),(c188.head_fingerprint(init),c188.tensor_sha(f)))

    def test_28_same_head_seed_same_schedule(self):
        f=torch.zeros((8,4,c188.FEATURES)); u=torch.tensor([[1,1,0,0]]*8,dtype=torch.bool)
        v=torch.tensor([[1,0,0,0],[0,1,0,0]]*4,dtype=torch.bool)
        _,a=c188.fit_selector(c188.paired_head_initial(188003),f,u,v,188003,steps=2,batch=4)
        _,b=c188.fit_selector(c188.paired_head_initial(188003),f+1,u,v,188003,steps=2,batch=4)
        self.assertEqual(a["batch_schedule_sha256"],b["batch_schedule_sha256"])

    def test_29_predict_masks_observed(self):
        f=torch.zeros((2,4,c188.FEATURES)); u=torch.tensor([[1,0,1,0],[0,1,0,1]],dtype=torch.bool)
        p,z,_=c188.predict_selector(c188.TargetSelector().eval(),f,u,batch=1)
        self.assertTrue(torch.isneginf(z[~u]).all())
        self.assertTrue(all(u[i,p[i]].item() for i in range(2)))

    def _good_results(self):
        m={"selected_observed":0,"by_missing_count":{"2":{"hit_rate":.9},"3":{"hit_rate":.95}},
           "macro_m2_m3":.925}
        return [{"base_seed":b,"head_seed":h,"discriminating":dict(m)} for b in c188.BASE_SEEDS for h in c188.HEAD_SEEDS]

    def _base_ref(self):
        return {"by_missing_count":{"2":{"hit_rate":268/376},"3":{"hit_rate":128/152}},
                "macro_m2_m3":((268/376)+(128/152))/2}

    def test_30_gate_all_nine(self):
        self.assertTrue(c188.selector_gate(self._good_results(),self._base_ref()))

    def test_31_gate_one_failure(self):
        r=self._good_results(); r[0]["discriminating"]["by_missing_count"]["2"]["hit_rate"]=.7
        self.assertFalse(c188.selector_gate(r,self._base_ref()))

    def test_32_gate_tie_fails(self):
        r=self._good_results(); r[0]["discriminating"]["by_missing_count"]["3"]["hit_rate"]=128/152
        self.assertFalse(c188.selector_gate(r,self._base_ref()))

    def test_33_gate_observed_selection_fails(self):
        r=self._good_results(); r[0]["discriminating"]["selected_observed"]=1
        self.assertFalse(c188.selector_gate(r,self._base_ref()))

    def test_34_manifest_hash_fixed(self):
        self.assertEqual(c188.digest(c188.manifest()),c188.MANIFEST_SHA)

    def test_35_manifest_workload(self):
        m=c188.manifest()
        self.assertEqual((m["trained_target_heads"],m["target_updates"],m["target_examples_drawn"]),(9,18000,4608000))
        self.assertEqual((m["base_feature_rows"],m["base_feature_forward_calls"],m["base_feature_cell_calls"]),(16776,18,126))

    def test_36_scope_has_no_live_acquisition(self):
        m=c188.manifest()
        self.assertEqual((m["actual_acquisitions"],m["network_calls"],m["evidence_writes"],m["answer_generation"],m["proof_checker_calls"]),(0,0,0,0,0))
        self.assertFalse(m["production_runtime_modified"])
        self.assertFalse(m["gate_e_candidate"])

if __name__=="__main__":
    unittest.main(verbosity=2)
