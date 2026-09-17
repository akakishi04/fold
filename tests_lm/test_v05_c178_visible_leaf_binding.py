"""C178 mechanics tests on synthetic inputs; not the registered learning experiment."""
from copy import deepcopy
from dataclasses import replace
import hashlib
import inspect
from pathlib import Path
import tempfile
import unittest

import torch

from fold_lm.v05 import structured_task_input as task
from fold_lm.v05 import structured_necessity_probe as api
from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as b


def view(values=(1, None, 0, None)):
    nodes = (task.Node('FACT', fact=0), task.Node('FACT', fact=1), task.Node('AND', left=0, right=1),
             task.Node('FACT', fact=2), task.Node('FACT', fact=3), task.Node('OR', left=3, right=4),
             task.Node('AND', left=2, right=5))
    facts = tuple(task.Fact(f'f{i}', 'UNOBSERVED' if x is None else 'OBSERVED', x,
                           () if x is None else (f'r{i}',)) for i, x in enumerate(values))
    return task.TaskView('scope|test', 'scope', nodes, facts)


def raw(v=None):
    return torch.tensor([task.encode(view() if v is None else v).features], dtype=torch.int32)


def valid_pairs():
    def score(x):
        return dict(macro_missing_balanced_accuracy=x,
            metrics=dict(macro_group_balanced_accuracy=x, needs_recall=x, sufficient_recall=x),
            by_missing_count={'1': dict(needs_recall=x), '3': dict(sufficient_recall=x)})
    return [dict(seed=s, indirect=score(.6), bound=score(.7),
                 paired_initial_equal=True, paired_batches_equal=True) for s in b.SEEDS]


class C178Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        torch.use_deterministic_algorithms(True)

    def test_01_control_is_exact_original_preparation(self):
        x = raw(); u, c = b.prepare_pair(x)
        self.assertTrue(torch.equal(u, api.prepare(x, api.ARMS[0])))
        self.assertEqual(c.shape, (1, 72)); self.assertEqual(c.dtype, torch.float32)

    def test_02_known_one_copied_to_correct_leaf(self):
        _, c = b.prepare_pair(raw()); self.assertEqual(c[0, 7:9].tolist(), [1, 1])

    def test_03_zero_remains_known_not_missing(self):
        _, c = b.prepare_pair(raw()); self.assertEqual(c[0, 25:27].tolist(), [1, 0])
        self.assertEqual(c[0, 13:15].tolist(), [0, 0])

    def test_04_only_leaf_child_placeholders_change(self):
        u, c = b.prepare_pair(raw()); mask = torch.zeros_like(u, dtype=torch.bool)
        for i in (0, 1, 3, 4): mask[:, 7+6*i:9+6*i] = True
        self.assertTrue(torch.equal(u[~mask], c[~mask]))

    def test_05_internal_topology_stays_exact(self):
        u, c = b.prepare_pair(raw())
        for i in (2, 5, 6): self.assertTrue(torch.equal(u[:,4+6*i:10+6*i], c[:,4+6*i:10+6*i]))

    def test_06_fact_indices_are_not_erased(self):
        u, c = b.prepare_pair(raw()); self.assertTrue(torch.equal(u[:,6:46:6], c[:,6:46:6]))

    def test_07_negation_is_not_computed_by_adapter(self):
        v = view(); ns = list(v.nodes); ns[0] = replace(ns[0], negate=True)
        _, c = b.prepare_pair(raw(replace(v, nodes=tuple(ns))))
        self.assertEqual(c[0,7:10].tolist(), [1, 1, 1])

    def test_08_operator_change_does_not_change_copied_bit(self):
        v=view(); ns=list(v.nodes); ns[2]=replace(ns[2],kind='OR')
        _, a=b.prepare_pair(raw(v)); _, c=b.prepare_pair(raw(replace(v,nodes=tuple(ns))))
        self.assertEqual(torch.nonzero(a!=c,as_tuple=False).tolist(), [[0,17]])

    def test_09_binding_follows_fact_id_not_leaf_position(self):
        v=view(); ns=list(v.nodes); ns[0]=replace(ns[0],fact=2); ns[3]=replace(ns[3],fact=0)
        _, c=b.prepare_pair(raw(replace(v,nodes=tuple(ns))))
        self.assertEqual(c[0,7:9].tolist(),[1,0]); self.assertEqual(c[0,25:27].tolist(),[1,1])

    def test_10_unknowns_do_not_get_guessed(self):
        u,c=b.prepare_pair(raw(view((None,None,None,None))))
        self.assertTrue(torch.equal(u,c))

    def test_11_unusable_status_no_payload(self):
        v=view(); fs=list(v.facts); fs[0]=task.Fact('f0','STALE',None,('old',))
        _,c=b.prepare_pair(raw(replace(v,facts=tuple(fs))))
        self.assertEqual(c[0,7:9].tolist(),[0,0])

    def test_12_raw_input_not_mutated(self):
        x=raw(); h=b.tensor_sha(x); b.prepare_pair(x); self.assertEqual(h,b.tensor_sha(x))

    def test_13_fact_table_and_resources_unchanged(self):
        u,c=b.prepare_pair(raw()); self.assertTrue(torch.equal(u[:,46:],c[:,46:]))

    def test_14_batch_permutation_equivariance(self):
        x=torch.cat([raw(),raw(view((0,1,None,1)))])
        u,c=b.prepare_pair(x); ru,rc=b.prepare_pair(x.flip(0))
        self.assertTrue(torch.equal(u.flip(0),ru)); self.assertTrue(torch.equal(c.flip(0),rc))

    def test_15_shape_and_dtype_rejected(self):
        for x in (raw().float(),raw().long(),torch.zeros((0,72),dtype=torch.int32),raw()[:,:71]):
            with self.assertRaises(ValueError): b.prepare_pair(x)

    def test_16_range_and_noncanonical_width_rejected(self):
        for idx,val in ((0,6),(1,3),(2,-1),(2,2**24)):
            x=raw();x[0,idx]=val
            with self.assertRaises(ValueError): b.prepare_pair(x)

    def test_17_masks_and_kinds_rejected(self):
        for idx,val in ((4,0),(46,0),(5,4),(9,2)):
            x=raw();x[0,idx]=val
            with self.assertRaises(ValueError): b.prepare_pair(x)

    def test_18_bad_fact_binding_rejected(self):
        for val in (0,2,5):
            x=raw();x[0,6]=val
            with self.assertRaises(ValueError): b.prepare_pair(x)

    def test_19_nonzero_leaf_children_and_forward_links_rejected(self):
        for idx,val in ((7,1),(19,7),(20,1),(21,1)):
            x=raw();x[0,idx]=val
            with self.assertRaises(ValueError): b.prepare_pair(x)

    def test_20_hidden_or_mistyped_payload_rejected(self):
        for idx,val in ((53,1),(48,0),(49,2),(52,2),(51,9)):
            x=raw();x[0,idx]=val
            with self.assertRaises(ValueError): b.prepare_pair(x)

    def test_21_runtime_fields_rejected(self):
        for idx,val in ((64,2),(70,7)):
            x=raw();x[0,idx]=val
            with self.assertRaises(ValueError): b.prepare_pair(x)

    def test_22_no_teacher_argument_or_new_packet(self):
        self.assertEqual(list(inspect.signature(b.prepare_pair).parameters),['raw'])
        self.assertIsInstance(b.prepare_pair(raw())[1],torch.Tensor)
        self.assertNotEqual(b.REPRESENTATIONS[1],task.SCHEMA)

    def test_23_capacity_and_forward_shape_unchanged(self):
        model=api.NecessityProbe(); self.assertEqual(sum(p.numel() for p in model.parameters()),26114)
        self.assertEqual(model(b.prepare_pair(raw())[1]).shape,(1,2))

    def test_24_toy_training_preserves_pair_initial_and_batches(self):
        x=torch.cat([raw(),raw(view((0,1,1,None)))])*1
        u,c=b.prepare_pair(x); y=torch.tensor([0,1],dtype=torch.int64)
        torch.manual_seed(10); initial=api.NecessityProbe(); h=api.fingerprint(initial)
        a,la=api.fit(initial,u,y,10,steps=2,batch_size=4)
        d,ld=api.fit(initial,c,y,10,steps=2,batch_size=4)
        self.assertEqual(api.fingerprint(initial),h)
        self.assertEqual(la['batch_schedule_sha256'],ld['batch_schedule_sha256'])
        self.assertNotEqual(api.fingerprint(a),api.fingerprint(d))

    def test_25_checkpoint_representation_metadata_and_roundtrip(self):
        torch.manual_seed(1); model=api.NecessityProbe()
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'test.pt'; torch.save(dict(representation=b.REPRESENTATIONS[1],state_dict=model.state_dict()),p)
            d=torch.load(p,weights_only=True,map_location='cpu'); self.assertEqual(d['representation'],b.REPRESENTATIONS[1])
            restored=api.NecessityProbe();restored.load_state_dict(d['state_dict'])
            self.assertEqual(api.fingerprint(model),api.fingerprint(restored))

    def test_26_gate_all_seeds_and_pair_integrity(self):
        p=valid_pairs();self.assertTrue(b.gate(p));self.assertFalse(b.gate(p[:-1]));self.assertFalse(b.gate(p[::-1]))
        p[1]['paired_batches_equal']=False;self.assertFalse(b.gate(p))

    def test_27_gate_strict_primary_and_minority_improvements(self):
        for path in [('macro_missing_balanced_accuracy',),('by_missing_count','1','needs_recall'),('by_missing_count','3','sufficient_recall')]:
            p=valid_pairs();d=p[1]['bound']
            for k in path[:-1]: d=d[k]
            d[path[-1]]=.6;self.assertFalse(b.gate(p))

    def test_28_gate_original_score_and_recalls(self):
        p=valid_pairs();p[0]['bound']['metrics']['macro_group_balanced_accuracy']=.6;self.assertTrue(b.gate(p))
        p[0]['bound']['metrics']['macro_group_balanced_accuracy']=.59;self.assertFalse(b.gate(p))
        for key in ('needs_recall','sufficient_recall'):
            p=valid_pairs();p[0]['bound']['metrics'][key]=.5;self.assertFalse(b.gate(p))

    def test_29_nonfinite_gate_and_json_rejected(self):
        p=valid_pairs();p[0]['bound']['macro_missing_balanced_accuracy']=float('nan');self.assertFalse(b.gate(p))
        with self.assertRaises(ValueError):b.blob(p)

    def test_30_registered_manifest_and_no_extra_training(self):
        m=b.manifest();self.assertEqual(hashlib.sha256(b.blob(m)).hexdigest(),b.MANIFEST_SHA)
        self.assertEqual(m['parameters'],26114);self.assertEqual(m['training_updates'],12000)
        self.assertEqual(m['leaf_fact_reads'],207360);self.assertEqual(m['copied_numeric_fields'],414720)
        self.assertEqual(m['steps'],2000);self.assertEqual(m['batch_size'],256)

    def test_31_regression_list_additive_and_unique(self):
        with tempfile.TemporaryDirectory() as td:
            tools=Path(td)/'tools';tools.mkdir()
            (tools/'run_c167.ps1').write_text('\n'.join(f'  "tests_lm.old_{i}"' for i in range(51)))
            names=b.regression_modules(td)
            self.assertEqual(len(names),62);self.assertEqual(len(set(names)),62)
            self.assertEqual(names[-1],'tests_lm.test_v05_c178_visible_leaf_binding')

    def test_32_missing_historical_regression_list_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            tools=Path(td)/'tools';tools.mkdir();(tools/'run_c167.ps1').write_text('"tests_lm.only"')
            with self.assertRaises(ValueError):b.regression_modules(td)


if __name__ == '__main__':
    unittest.main()
