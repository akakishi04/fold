"""C175 helpers use toy predictions; no registered reference/evaluation is run."""
from __future__ import annotations
import hashlib
import inspect
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import numpy as np
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as b


class C175Tests(unittest.TestCase):
    def toy(self):
        x=np.zeros((4,72),dtype=np.int32);x[:,46]=[0,0,1,1]
        return x,np.asarray([0,1,1,1],dtype=np.int64)

    def test_01_only_syntax_fields_excluded(self):
        x=np.zeros((2,72),dtype=np.int32);x[1,4:46]=17
        self.assertEqual(*b.blind_keys(x))

    def test_02_facts_and_resources_are_retained(self):
        for i in list(range(4))+list(range(46,72)):
            x=np.zeros((2,72),dtype=np.int32);x[1,i]=1
            self.assertNotEqual(*b.blind_keys(x))

    def test_03_majority_and_tie_zero(self):
        x,y=self.toy();table,counts=b.build_reference(x,y)
        self.assertEqual(b.reference_predictions(table,x).tolist(),[0,0,1,1])
        self.assertEqual(sorted(counts.values()),[[1,1],[0,2]][::-1])

    def test_04_reference_interface_has_only_train_inputs(self):
        self.assertEqual(set(inspect.signature(b.build_reference).parameters),{'x_train','y_train'})
        self.assertEqual(set(inspect.signature(b.reference_predictions).parameters),{'table','features'})

    def test_05_unseen_key_has_no_fallback(self):
        x,y=self.toy();table,_=b.build_reference(x,y);x[0,47]=3
        with self.assertRaises(b.InvalidExecution):b.reference_predictions(table,x)

    def test_06_reference_preserves_inputs(self):
        x,y=self.toy();xx=x.copy();yy=y.copy();b.build_reference(x,y)
        self.assertTrue(np.array_equal(x,xx));self.assertTrue(np.array_equal(y,yy))

    def test_07_single_class_strata_have_null_ba(self):
        r=b.basic_metrics(np.array([0,0]),np.array([0,1]))
        self.assertIsNone(r['balanced_accuracy']);self.assertIsNone(r['needs_recall'])
        self.assertEqual(r['sufficient_recall'],.5)

    def test_08_group_mean_not_row_weighted(self):
        r=b.metrics([0,1,0,0,1,1],[0,1,1,1,0,0],[1,1,2,2,2,2])
        self.assertEqual(r['macro_group_balanced_accuracy'],.5)
        self.assertAlmostEqual(r['accuracy'],1/3)

    def test_09_metric_replay_checks_confusion(self):
        r=b.metrics([0,1],[0,1],[0,0]);b.same_metrics(r,{'accuracy':1.0,'confusion':[[1,0],[0,1]]})
        with self.assertRaises(b.InvalidExecution):b.same_metrics(r,{'confusion':[[0,1],[0,1]]})

    def test_10_invalid_metric_input_rejected(self):
        for y,p in [([0,1],[0]),([True,False],[0,1]),([0,2],[0,1])]:
            with self.assertRaises(b.InvalidExecution):b.basic_metrics(y,p)

    def test_11_constant_blind_prediction_cannot_solve_both(self):
        r=b.matched_pairs([(1,)]*4,[0,0,1,1],[0]*4)
        self.assertEqual(r['cross_label_pairs'],4);self.assertEqual(r['both_correct_pairs'],0)

    def test_12_counterfactual_counts_preserve_correlations(self):
        r=b.matched_pairs([(1,)]*4,[0,0,1,1],[0,0,1,1])
        self.assertEqual(r['both_correct_rate'],1)
        self.assertEqual(r['mixed_blind_keys'],1)

    def test_13_gate_requires_each_seed_and_strict_gain(self):
        rows=[dict(seed=s,full=dict(macro_group_balanced_accuracy=.8,sufficient_recall=.8,needs_recall=.7)) for s in b.SEEDS]
        base=dict(macro_group_balanced_accuracy=.7)
        self.assertTrue(b.gate(rows,base));self.assertFalse(b.gate(rows[:-1],base))
        rows[1]['full']['macro_group_balanced_accuracy']=.7;self.assertFalse(b.gate(rows,base))
        rows[1]['full']['macro_group_balanced_accuracy']=.8;rows[2]['full']['needs_recall']=.5
        self.assertFalse(b.gate(rows,base))

    def test_14_manifest_fixed_and_zero_model_work(self):
        self.assertEqual(hashlib.sha256(b.blob(b.manifest())).hexdigest(),b.MANIFEST_SHA)
        for k in ('new_training','new_model_forwards','new_seeds','checkpoint_loads','actual_acquisitions'):
            self.assertEqual(b.manifest()[k],0)
        self.assertEqual(b.manifest()['stored_model_predictions'],311040)

    def test_15_safe_relative_paths(self):
        with tempfile.TemporaryDirectory() as d:
            for name in ('../x','/tmp/x','C:/x','a\\b','a/../x','.','a//b',''):
                with self.assertRaises(b.InvalidExecution):b.safe_child(d,name)
            self.assertEqual(b.safe_child(d,'docs/a.md'),Path(d)/'docs/a.md')

    def test_16_duplicate_nonfinite_json_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.json'
            for raw in ('{"a":1,"a":2}','{"a":NaN}'):
                p.write_text(raw)
                with self.assertRaises(b.InvalidExecution):b.read_json(p)

    def test_17_npz_never_unpickles(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.npz';np.savez_compressed(p,x=np.array([{'x':1}],dtype=object))
            with self.assertRaises(ValueError):b.load_npz(p)
            np.savez_compressed(p,x=np.arange(4));self.assertEqual(b.load_npz(p)['x'].tolist(),[0,1,2,3])

    def test_18_real_standalone_git_paths_and_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'fold_lm').mkdir();path=root/'fold_lm'/'p.py';path.write_bytes(b'one\ntwo\n')
            subprocess.run(['git','init','-q',d],check=True)
            subprocess.run(['git','-C',d,'-c','core.autocrlf=false','add','fold_lm/p.py'],check=True)
            subprocess.run(['git','-C',d,'-c','user.name=Test','-c','user.email=test@example.invalid','commit','-qm','fixture'],check=True)
            identity=b.git(root,'rev-parse','HEAD:fold_lm/p.py').decode().strip()
            pins={'fold_lm/p.py':identity};self.assertEqual(len(b.protect_tree_files(root,pins)),1)
            path.write_bytes(b'one\r\ntwo\r\n');b.protect_tree_files(root,pins)
            path.write_bytes(b'changed\n')
            with self.assertRaises(b.InvalidExecution):b.protect_tree_files(root,pins)

    def test_19_parent_hash_checked_before_parse(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.json';p.write_text('not json')
            with self.assertRaisesRegex(b.InvalidExecution,'hash mismatch'):b.load_parent(p)

    def test_20_artifact_hashes_and_exact_set(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);parent=root/'summary.json';parent.write_text('{}');items=[]
            for name in sorted(b.ARTIFACTS):
                (root/name).write_bytes(b'toy')
                items.append(dict(file=name,sha256=b.sha(root/name),serialized_bytes=3))
            p={'artifacts':items};self.assertEqual(len(b.protect_artifacts(parent,p)),12)
            (root/'pilot-predictions.json').write_bytes(b'bad')
            with self.assertRaises(b.InvalidExecution):b.protect_artifacts(parent,p)
            with self.assertRaises(b.InvalidExecution):b.protect_artifacts(parent,{'artifacts':items[:-1]})


if __name__=='__main__':unittest.main()
