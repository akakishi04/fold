"""C336 software fixtures; synthetic ancestors are not the user's native results."""
from __future__ import annotations
from collections import Counter
import contextlib
import copy
import hashlib
import importlib.util
import io
import itertools
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c336_saved_query_order_patterns as s

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.util.spec_from_file_location('_c336_executor_tests',ROOT/'tools/c336_execution.py')
e = importlib.util.module_from_spec(loader); loader.loader.exec_module(e)
HEAD = 'a'*40


def data_fixture():
    result = {}
    for split,count in (('TRAIN',12),('HOLDOUT',6)):
        rows = []
        for lang,j,values in itertools.product(s.LANGUAGES,range(count),((0,1),(1,0))):
            entities = [f'{lang}{split}{j}a',f'{lang}{split}{j}b']
            for order in (entities,entities[::-1]):
                for q in range(2):
                    rows.append(dict(id=f'{split}{len(rows)}',language=lang,entities=list(entities),values=list(values),
                        permutation=list(order),query=entities[q],target=48+values[q]))
        result[split] = rows
    return result


def reference_category(pred, targets):
    # Independent definition using answer properties, not production classify().
    a,b = targets
    if all(pred[2*j+i] == targets[i] for j in range(2) for i in range(2)): return 'query_correct'
    if all(pred[2*j+i] == targets[1-i] for j in range(2) for i in range(2)): return 'query_swapped'
    if all(pred[2*j+i] == targets[j] for j in range(2) for i in range(2)): return 'first_fact'
    if all(pred[2*j+i] == targets[1-j] for j in range(2) for i in range(2)): return 'last_fact'
    if any(v not in targets for v in pred): return 'other_class'
    if len(set(pred)) == 1: return 'value_lock'
    return 'mixed'


def logits_for(rows, arm, seed):
    predictions = []
    for start in range(0,len(rows),4):
        a,b = rows[start]['target'],rows[start+1]['target']
        patterns = [(a,b,a,b),(b,a,b,a),(a,a,b,b),(b,b,a,a),(a,a,a,a),(55,b,a,b),(a,b,b,b)]
        shift = int(arm == 'alternating')
        predictions.extend(patterns[(start//4+shift+seed%3)%len(patterns)])
    logits = torch.zeros((len(rows),256),dtype=torch.float64)
    logits[torch.arange(len(rows)),torch.tensor(predictions)] = 1.
    return logits,predictions


def raw_tree(data, arm, seed):
    tensors = {sp:logits_for(data[sp],arm,seed)[0] for sp in s.SPLITS}
    def split_tree(profiles):
        return {sp:{pr:{view:tensors[sp] for view in ('normal','evidence_blind','query_blind')} for pr in profiles} for sp in s.SPLITS}
    return dict(original={str(n):split_tree(('repeat',) if n == 1 else ('repeat','shared_prefix','shared_suffix')) for n in range(1,7)},
                interior=split_tree(('u_dominant','balanced','v_dominant')))


def raw_check(raw, data, cx):
    require = e.require
    require(set(raw) == {'original','interior'} and set(raw['original']) == set(map(str,range(1,7))), 'raw shape')
    count = 0
    for tree in [*raw['original'].values(),raw['interior']]:
        for split,profiles in tree.items():
            for views in profiles.values():
                for z in views.values():
                    require(z.shape == (len(data[split]),256) and z.dtype == torch.float64 and bool(torch.isfinite(z).all()),'raw tensor')
                    count += 1
    require(count == 114,'all114views')


def same_tree(a,b):
    if isinstance(a,dict):
        e.require(set(a) == set(b),'tree keys')
        for k in a: same_tree(a[k],b[k])
    else:
        e.require(torch.equal(a,b),'replay mismatch')


def independent_contrast(data, seed):
    rows = data['HOLDOUT']; a = logits_for(rows,'native',seed)[1]; b = logits_for(rows,'alternating',seed)[1]
    correct = [[v == r['target'] for v,r in zip(pred,rows)] for pred in (a,b)]
    pairs = [[all(c[i:i+2]) for i in range(0,len(rows),2)] for c in correct]
    old,new = correct; op,np = pairs
    # Each raw profile repeats this synthetic set; all three profiles are counted.
    return dict(answers=3*len(rows),query_pairs=3*len(pairs[0]),control_correct=3*sum(old),candidate_correct=3*sum(new),
        control_both_correct=3*sum(op),candidate_both_correct=3*sum(np),rescued=3*sum(not x and y for x,y in zip(old,new)),
        regressed=3*sum(x and not y for x,y in zip(old,new)),pair_rescued=3*sum(not x and y for x,y in zip(op,np)),
        pair_regressed=3*sum(x and not y for x,y in zip(op,np)),answer_gain=3*(sum(new)-sum(old)),query_pair_gain=3*(sum(np)-sum(op)))


def fixture():
    data = data_fixture(); records = []
    for seed,arm in s.identities():
        raw = raw_tree(data,arm,seed)
        records.append(dict(seed=seed,arm=arm,state_sha256='a'*64,evaluation_policy='native_before',raw={'evaluation':raw,'replay':raw},
            receipts={m:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for m in ('evaluation','replay')}))
    pairs = [dict(seed=seed,original_by_length={str(n):independent_contrast(data,seed) for n in range(2,7)},interior=independent_contrast(data,seed)) for seed in s.SEEDS]
    parent = dict(candidate_gate=False,eligible_seed_count=0,evaluation_policy='native_before',paired_comparisons=pairs)
    base = NS(validate_raw=raw_check,peak_rss=lambda:1)
    p = NS(check_summary=lambda value:e.require(value['candidate_gate'] is False,'synthetic negative'),
        previous=lambda:NS(source=lambda:NS(base=lambda:base)),crossed=lambda:NS(same_tree=same_tree))
    return NS(data=data,archive=dict(schema='fold-c335-evaluations-v1',records=records),parent=parent,p=p)


def synthetic_recovery():
    def flatten(suite):
        for t in suite:
            if isinstance(t,unittest.TestSuite): yield from flatten(t)
            else: yield t
    def validate(row,g,head,i,ph,launcher,log):
        e.require(row['schema'] == 'fold-c330-r1-module-v2' and row['commit_sha'] == head and row['index'] == i
            and row['module'] == g['module'] and row['plan_sha256'] == ph,'generic ABI')
        e.require(row['result']['success_ids'] == g['test_ids'] and row['result']['tests'] == len(g['test_ids']),'successful IDs')
        e.require(launcher in (row['pid'],row['parent_pid']),'PID topology')
        return 'direct' if launcher == row['pid'] else 'redirected-child'
    return NS(flatten=flatten,EXCLUDED='excluded',allowed_module=lambda n:bool(re.fullmatch(r'tests_lm\.[A-Za-z0-9_]+',n)),
              validate_module_evidence=Mock(side_effect=validate))


def test_plan():
    groups = []; q,rem = divmod(6058,225)
    for i in range(225):
        name = f'tests_lm.fixture_{i:03d}'; groups.append(dict(module=name,test_ids=[name+f'.Fixture.test_{j:03d}' for j in range(q+(i<rem))]))
    groups.append(dict(module=e.TEST_MODULE,test_ids=[e.TEST_MODULE+f'.C336Tests.test_{j:02d}' for j in range(32)]))
    ids = [v for g in groups for v in g['test_ids']]
    return dict(schema='fold-c336-regression-plan-v1',commit_sha=HEAD,manifest_sha256=s.MANIFEST_SHA,test_ids_sha256=s.digest(ids),groups=groups),s.digest(ids[:-32])


def module_proof(folder,plan,i,ph):
    g = plan['groups'][i]; pid,parent = 20000+i,10000+i
    e.save(folder/f'module-{i:03d}.json',dict(schema='fold-c330-r1-module-v2',commit_sha=HEAD,index=i,module=g['module'],plan_sha256=ph,
        pid=pid,parent_pid=parent,result=dict(tests=len(g['test_ids']),success_ids=g['test_ids'])))
    (folder/f'module-{i:03d}.log').write_bytes(b'explicit synthetic collaborator proof')
    return pid if i%2 == 0 else parent


def parent_fixture():
    ps = NS(validate_seal=lambda:None,check_summary=lambda value:None,EXPERIMENT_ID='parent',STAGE='stage',MANIFEST_SHA='m',WORK={})
    p = NS(spec=lambda:ps,PARENT_SUMMARY='s',PARENT_ENVELOPE='e')
    pins = {e.P_PATH:e.P_BLOB,**{f'p{i}':'a' for i in range(870)}}; inputs = {f'i{i}':'b' for i in range(3893)}
    r = dict(schema='fold-c335-trained-v1',commit_sha=e.PARENT_HEAD,experiment_id='parent',stage='stage',status='FAIL',scientific_execution_valid=True,
        capability_gate_applicable=True,gate_f_candidate=False,production_adoption=False,validation_summary={'candidate_gate':False},
        source_blobs=pins,input_sha256=inputs,manifest_sha256='m')
    v = dict(schema='fold-c335-execution-envelope-v1',commit_sha=e.PARENT_HEAD,scientific_status='FAIL',scientific_summary_sha256=e.PARENT_SUMMARY,
        manifest_sha256='m',scientific_work={},source_count=871,input_count=3893,source_blobs=pins,input_sha256=inputs,parent_summary_sha256='s',
        parent_envelope_sha256='e',immediate_parent_semantic_reconstruction=True,parent_regression_reconstructed=True,ancestor_semantic_reruns=0,
        saved_semantic_reconstruction=True,final_reference_rechecks=3893,hash_stats={'final_reference_rechecks':3893},regression=e.receipt(e.PARENT_HEAD,6058))
    return r,v,p


class C336Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old_threads = torch.get_num_threads(); torch.set_num_threads(2); cls.f = fixture()
        with patch.object(s,'previous',return_value=cls.f.p):
            cls.details,cls.changes,cls.summary = s.analyze(cls.f.data,cls.f.archive,cls.f.parent,())
    @classmethod
    def tearDownClass(cls): torch.set_num_threads(cls.old_threads)
    def context(self): return patch.object(s,'previous',return_value=self.f.p)
    def test_01_manifest_seal_and_tamper(self):
        s.validate_seal()
        with patch.object(s,'CATEGORIES',('changed',)),self.assertRaises(ValueError): s.validate_seal()
    def test_02_actual_loader_and_work_contract(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),32)
        self.assertEqual((s.FULL_TESTS,s.MODULES,s.SOURCE_COUNT,s.INPUT_COUNT),(6058+32,225+1,871+6,3893+461+6))
        self.assertEqual(s.WORK['normal_answers'],10*18*(192+96)); self.assertEqual(s.WORK['model_forward_calls'],0)
    def test_03_logical_groups_exact_four_slots(self):
        g = s.logical_groups(self.f.data); self.assertEqual([len(g[k]) for k in s.SPLITS],[48,24])
        for split,rows in g.items(): self.assertEqual(sorted(i for r in rows for i in r['indices']),list(range(len(self.f.data[split]))))
    def test_04_duplicate_row_ID_rejected(self):
        d = copy.deepcopy(self.f.data); d['TRAIN'][1]['id'] = d['TRAIN'][0]['id']
        with self.assertRaises(ValueError): s.logical_groups(d)
    def test_05_missing_or_duplicate_query_order_rejected(self):
        d = copy.deepcopy(self.f.data); d['TRAIN'][1]['query'] = d['TRAIN'][0]['query']; d['TRAIN'][1]['target'] = d['TRAIN'][0]['target']
        with self.assertRaises(ValueError): s.logical_groups(d)
        with self.assertRaises(ValueError): s.logical_groups({'TRAIN':[],'HOLDOUT':[]})
    def test_06_source_target_language_and_value_types(self):
        for key,val in (('target',True),('language','de'),('values',[True,0]),('permutation',['bad','order'])):
            d = copy.deepcopy(self.f.data); d['TRAIN'][0][key] = val
            with self.subTest(),self.assertRaises(ValueError): s.logical_groups(d)
    def test_07_exhaustive_binary_classification_independent(self):
        categories = Counter()
        for pred in itertools.product((48,49),repeat=4):
            for targets in ((48,49),(49,48)):
                got = s.classify(pred,targets); self.assertEqual(got['category'],reference_category(pred,targets))
                if targets == (48,49): categories[got['category']] += 1
        self.assertEqual(categories,Counter(query_correct=1,query_swapped=1,first_fact=1,last_fact=1,value_lock=2,mixed=10))
    def test_08_order_orientation_not_target_selected(self):
        self.assertEqual(s.classify([49,49,48,48],[49,48])['category'],'first_fact')
        self.assertEqual(s.classify([48,48,49,49],[49,48])['category'],'last_fact')
        self.assertEqual(s.classify([49,48,49,48],[48,49])['category'],'query_swapped')
    def test_09_other_class_not_binary_or_valid_value_lock(self):
        self.assertEqual(s.classify([55]*4,[48,49])['category'],'other_class')
        self.assertEqual(s.classify([55]*4,[48,49])['other_answers'],4)
    def test_10_bad_predictions_and_boolean_targets(self):
        for pred in ([True,49,48,49],[256]*4,[float('nan')]*4,[48]*3):
            with self.assertRaises(ValueError): s.classify(pred,[48,49])
        with self.assertRaises(ValueError): s.classify([48]*4,[48,48])
    def test_11_equal_totals_do_not_hide_exchanged_errors(self):
        a=dict(predictions=[48]*4,targets=[48,49],category='value_lock');b=dict(predictions=[49]*4,targets=[48,49],category='value_lock')
        v=s.transition(a,b);self.assertEqual((v['answer_gain'],v['rescued'],v['regressed']),(0,2,2))
    def test_12_pairs_require_both_answers_correct(self):
        a=dict(predictions=[48,49,48,49],targets=[48,49],category='query_correct')
        b=dict(predictions=[48,48,49,49],targets=[48,49],category='first_fact')
        v=s.transition(a,b);self.assertEqual((v['control_both_correct'],v['candidate_both_correct'],v['pair_regressed']),(2,0,2))
    def test_13_argmax_uses_all256_classes(self):
        raw=raw_tree(self.f.data,'native',335001);z=raw['original']['2']['TRAIN']['repeat']['normal'].clone();z[:,3]=99.
        raw['original']['2']['TRAIN']['repeat']['normal']=z
        self.assertEqual(s.normal_predictions(raw,'original2','TRAIN','repeat',192),[3]*192)
    def test_14_invalid_logits_fail_closed(self):
        for kind in ('nan','dtype','shape'):
            raw=raw_tree(self.f.data,'native',335001);z=raw['interior']['TRAIN']['balanced']['normal'].clone()
            if kind=='nan':z[0,0]=float('nan')
            elif kind=='dtype':z=z.float()
            else:z=z[:1]
            raw['interior']['TRAIN']['balanced']['normal']=z
            with self.assertRaises(ValueError):s.normal_predictions(raw,'interior4','TRAIN','balanced',192)
    def test_15_complete_production_analysis_and_reference_counts(self):
        self.assertEqual((len(self.details),len(self.changes),len(self.summary['strata'])),(12960,6480,720))
        for r in self.details:self.assertEqual(r['category'],reference_category(r['predictions'],r['targets']))
        self.assertEqual(sum(r['answers'] for r in self.summary['strata']),51840)
        self.assertFalse(self.summary['parent_validation_summary']['candidate_gate'])
    def test_16_parent_rescue_counts_reconciled_not_just_total_gain(self):
        parent=copy.deepcopy(self.f.parent);parent['paired_comparisons'][0]['original_by_length']['6']['rescued']+=1
        with self.context(),self.assertRaisesRegex(ValueError,'reconciliation'):s.analyze(self.f.data,self.f.archive,parent,())
    def test_17_complete_cohort_schema_and_policy(self):
        for kind in ('drop','schema','policy'):
            a=dict(self.f.archive);a['records']=[dict(r) for r in a['records']]
            if kind=='drop':a['records'].pop()
            elif kind=='schema':a['schema']='wrong'
            else:a['records'][0]['evaluation_policy']='first_mean'
            with self.context(),self.assertRaises(ValueError):s.analyze(self.f.data,a,self.f.parent,())
    def test_18_saved_replay_mismatch_rejected(self):
        a=copy.deepcopy(self.f.archive);r=a['records'][0];r['raw']['replay']=copy.deepcopy(r['raw']['replay'])
        r['raw']['replay']['interior']['TRAIN']['balanced']['normal'][0,0]+=2.
        with self.context(),self.assertRaisesRegex(ValueError,'replay'):s.analyze(self.f.data,a,self.f.parent,())
    def test_19_summary_partition_and_missing_language_rejected(self):
        with self.context():
            for kind in ('drop','count','parent'):
                v=copy.deepcopy(self.summary)
                if kind=='drop':v['strata'].pop()
                elif kind=='count':v['strata'][0]['categories']['query_correct']+=1
                else:v['parent_validation_summary']['candidate_gate']=True
                with self.assertRaises(ValueError):s.check_summary(v)
    def test_20_real_archive_writer_reconstruction_and_tamper(self):
        with tempfile.TemporaryDirectory() as tmp,self.context():
            root=Path(tmp);source=root/'source';data=root/'data';out=root/'out'
            for p in (source,data,out):p.mkdir()
            e.save(data/'dataset.json',self.f.data);torch.save(self.f.archive,source/'evaluations.pt')
            value=s.run_diagnostic(out,source,data,self.f.parent,(),e.read)
            restored=s.semantic_recheck(out,source,data,self.f.parent,(),e.read)
            self.assertEqual(s.blob(value),s.blob(restored));self.assertEqual(set(p.name for p in out.iterdir()),set(s.OUTPUTS))
            (out/'transitions.json').write_bytes(b'[]')
            with self.assertRaisesRegex(ValueError,'reconstruction'):s.semantic_recheck(out,source,data,self.f.parent,(),e.read)
    def test_21_parent_negative_contract_and_exact_protection(self):
        r,v,p=parent_fixture();e.parent_contract(r,v,p)
        for key,value in (('scientific_status','PASS'),('input_count',3430),('source_count',865),('final_reference_rechecks',3892)):
            bad=copy.deepcopy(v);bad[key]=value
            with self.assertRaises(ValueError):e.parent_contract(r,bad,p)
    def test_22_all453_parent_proofs_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);items=[]
            for i in range(225):
                (folder/f'module-{i:03d}.json').write_bytes(b'{}');(folder/f'module-{i:03d}.log').write_bytes(b'fixture')
                items.append(dict(index=i,receipt_sha256=e.sha(folder/f'module-{i:03d}.json'),log_sha256=e.sha(folder/f'module-{i:03d}.log')))
            e.save(folder/'regression-plan.json',{});e.save(folder/'regression-result.json',{});e.save(folder/'regression-evidence.json',dict(modules=items))
            env=dict(regression_isolation=dict(tests=6058,modules=225,plan_sha256=e.sha(folder/'regression-plan.json'),
                result_sha256=e.sha(folder/'regression-result.json'),evidence_sha256=e.sha(folder/'regression-evidence.json')))
            self.assertEqual(len(e.parent_test_files(folder,env,e.sha)),453)
            # Exercise the real successor snapshot union with explicit fake ancestor maps.
            root=folder/'repo';root.mkdir();out=root/e.PARENT_FOLDER/'science';out.mkdir(parents=True)
            pins={};inputs={};tree={}
            for i in range(871):
                name=f'ancestor/{i}.py';path=root/name;path.parent.mkdir(exist_ok=True);raw=f'# fixture{i}\n'.encode();path.write_bytes(raw)
                oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();pins[name]=oid;tree[name]=oid;inputs[e.canonical(path)]=e.sha(path)
            # Materialize the entire inherited union, not only its source entries.
            for i in range(3893-871):
                path=root/f'input-{i}.bin';path.write_bytes(str(i).encode('ascii'))
                inputs[e.canonical(path)]=e.sha(path)
            for name in s.OWN:
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);raw=name.encode();path.write_bytes(raw)
                tree[name]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            names=('experiment-plan.json','training-traces.json','trained-models.pt','evaluations.pt','measurements.json','validation-summary.json')
            for name in names:(out/name).write_bytes(b'fixture')
            for path in folder.iterdir():
                if path.is_file():(out.parent/path.name).write_bytes(path.read_bytes())
            e.save(out/'summary.json',{'artifacts':[]});e.save(out.parent/'execution-envelope.json',dict(source_blobs=pins,input_sha256=inputs,**env))
            def inherited_snapshot(root, prior, hash_file):
                for name,wanted in inputs.items():
                    self.assertEqual(hash_file(name),wanted)
                return {},{},pins,inputs
            proof=env['regression_isolation'];parent=NS(spec=lambda:NS(OUTPUTS=names),snapshot=inherited_snapshot,build_plan=Mock(return_value={}),verify_tests=Mock(return_value=proof))
            h=dict(parent=parent,prior=('explicit','fixture'),recovery=object(),legacy=NS(tree_blobs=lambda root:tree,
                descriptors=lambda out,items,names,h:{e.canonical(out/n):h(out/n) for n in names}))
            with patch.object(e,'PARENT_SUMMARY',e.sha(out/'summary.json')),patch.object(e,'PARENT_ENVELOPE',e.sha(out.parent/'execution-envelope.json')),patch.object(e,'parent_contract'):
                _,_,got_pins,got_inputs=e.snapshot(root,h,e.sha)
                self.assertEqual((len(got_pins),len(got_inputs)),(877,4360))
                self.assertEqual(len(pins),871);self.assertEqual(len(inputs),3893)
                self.locked_snapshot_boundary(root,h,got_inputs)
            (folder/'module-224.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.parent_test_files(folder,env,e.sha)
    def locked_snapshot_boundary(self,root,h,expected):
        # Real accepted cache + real files; only the OS lease is a software fixture.
        # No Windows sharing/protection or actual ancestor outcome is claimed here.
        loader=importlib.util.spec_from_file_location('_c336_r4_boundary',ROOT/'tools/c324_locked_hash_r4.py')
        locks=importlib.util.module_from_spec(loader);loader.loader.exec_module(locks)
        leases=[];reference=Mock(wraps=e.sha)
        class Lease:
            def __init__(self,path):
                self.path=Path(path);self.size=self.path.stat().st_size;self.closed=False
                leases.append(self)
            def check(self):
                e.require(not self.closed and self.path.stat().st_size == self.size,'fixture lease identity')
            def digest(self,pulse):
                self.check();raw=self.path.read_bytes();pulse(len(raw))
                return hashlib.sha256(raw).hexdigest()
            def close(self):self.closed=True
        # Reproduce the original failure in the real snapshot/parent-proof path.
        with locks.LockedHashes(reference,Lease) as cache:
            with self.assertRaisesRegex(ValueError,'locked-file bound exceeded'):
                e.snapshot(root,h,cache.sha)
            self.assertEqual(len(cache.entries),cache.max_files)
            self.assertLess(cache.max_files,len(expected))
            self.assertTrue(all(not lease.closed for lease in leases))
        self.assertTrue(all(lease.closed for lease in leases));self.assertFalse(cache.entries)
        leases.clear();reference.reset_mock()
        extra=root/'not-registered.bin';extra.write_bytes(b'extra')
        with locks.LockedHashes(reference,Lease,max_files=s.INPUT_COUNT) as cache:
            _,_,pins,inputs=e.snapshot(root,h,cache.sha)
            self.assertEqual(inputs,expected);self.assertEqual(len(pins),s.SOURCE_COUNT)
            self.assertEqual(len(cache.entries),s.INPUT_COUNT)
            self.assertEqual(reference.call_count,s.INPUT_COUNT)
            first=next(iter(inputs));self.assertEqual(cache.sha(first),inputs[first])
            self.assertEqual(reference.call_count,s.INPUT_COUNT)  # reuse still checks the lease
            with self.assertRaisesRegex(ValueError,'locked-file bound exceeded'):
                cache.sha(extra)
            self.assertEqual(len(leases),s.INPUT_COUNT)  # rejection precedes lease acquisition
            self.assertTrue(all(not lease.closed for lease in leases))
            inventory=cache.recheck()
            self.assertEqual({v['path']:v['sha256'] for v in inventory},expected)
            self.assertEqual(cache.stats['final_reference_rechecks'],s.INPUT_COUNT)
            self.assertEqual(reference.call_count,2*s.INPUT_COUNT)
            self.assertEqual(Counter(e.canonical(c.args[0]) for c in reference.call_args_list),
                             Counter({name:2 for name in expected}))
            self.assertTrue(all(not lease.closed for lease in leases))
        self.assertTrue(all(lease.closed for lease in leases));self.assertFalse(cache.entries)
        # Final uncached reread must detect changed bytes even with equal size.
        leases.clear();path=Path(first);original=path.read_bytes()
        try:
            with locks.LockedHashes(e.sha,Lease,max_files=s.INPUT_COUNT) as cache:
                cache.sha(path);path.write_bytes(bytes([original[0]^1])+original[1:])
                with self.assertRaisesRegex(ValueError,'final/reference digest mismatch'):cache.recheck()
                self.assertTrue(all(not lease.closed for lease in leases))
        finally:path.write_bytes(original)
        self.assertTrue(all(lease.closed for lease in leases));self.assertFalse(cache.entries)
    def test_23_immediate_parent_loader_signature(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);source=root/e.PARENT_FOLDER/'science';data=root/'c329/science';source.mkdir(parents=True);data.mkdir(parents=True)
            names=('experiment-plan.json','training-traces.json','trained-models.pt','evaluations.pt','measurements.json','validation-summary.json')
            for folder,files in ((source,names),(data,('dataset.json','original-prompts.json','interior-prompts.json'))):
                for name in files:(folder/name).write_bytes(b'{}')
            inputs={e.canonical(p):e.sha(p) for f in (source,data) for p in f.iterdir()};saved=self.f.parent
            ps=NS(OUTPUTS=names,semantic_recheck=Mock(return_value=saved));h=dict(parent=NS(spec=lambda:ps),c330=NS(PARENT_FOLDER='c329'))
            x=NS(guarded=NS(no_neural=contextlib.nullcontext),c=NS(p267=NS(validate_data=lambda data:None)))
            cx=(None,None,NS(new_prompts=lambda data:{},check_prompts=lambda *a:None),None,None,x)
            base=NS(context=lambda:cx,digest=s.digest,DATA_SHA=s.digest({}),PROMPTS_SHA=s.digest({}))
            old=NS(load_data=lambda *a:({}, {},{}),source=lambda:NS(base=lambda:base));p=NS(previous=lambda:old)
            with patch.object(s,'previous',return_value=p):
                e.parent_semantics(root,h,{'validation_summary':saved},inputs)
                ps.semantic_recheck.assert_called_once_with(source,data,cx,e.read)
                del inputs[e.canonical(source/'evaluations.pt')]
                with self.assertRaises(ValueError):e.parent_semantics(root,h,{'validation_summary':saved},inputs)
    def test_24_actual_own_loader_is_appended(self):
        plan,digest=test_plan();r=synthetic_recovery();parent=NS(build_plan=Mock(return_value={'groups':plan['groups'][:-1]}))
        with patch.object(e,'BASE_IDS_SHA',digest):
            got=e.build_plan(ROOT,HEAD,dict(parent=parent,prior=('explicit','fixture'),recovery=r))
            self.assertEqual(len(got['groups']),226);self.assertEqual(len(got['groups'][-1]['test_ids']),32)
    def test_25_plan_drop_duplicate_reorder_rejected(self):
        plan,digest=test_plan();r=synthetic_recovery()
        with patch.object(e,'BASE_IDS_SHA',digest):
            e.validate_plan(plan,HEAD,r)
            for kind in ('drop','duplicate','reorder'):
                v=copy.deepcopy(plan)
                if kind=='drop':v['groups'].pop()
                elif kind=='duplicate':v['groups'][0]['test_ids'][1]=v['groups'][0]['test_ids'][0]
                else:v['groups'][0]['test_ids'].reverse()
                with self.assertRaises(ValueError):e.validate_plan(v,HEAD,r)
    def test_26_module_mode_delegates_exact_module_only(self):
        plan,digest=test_plan();r=synthetic_recovery();g=plan['groups'][0];r.execute_module=Mock(return_value={'tests':len(g['test_ids'])});r.check_module=Mock()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),patch.object(e,'guard'),patch.object(e,'helpers',return_value={'recovery':r}),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.save(folder/'regression-plan.json',plan);e.module_child(folder,folder,HEAD,0,e.sha(folder/'regression-plan.json'))
            r.execute_module.assert_called_once_with(g['module'],g['test_ids']);self.assertEqual(e.read(folder/'module-000.json')['parent_pid'],e.os.getppid())
    def test_27_collect_fresh_verify_and_log_tamper(self):
        plan,digest=test_plan();r=synthetic_recovery()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.collect_tests(folder,HEAD,plan,r,lambda i,h:module_proof(folder,plan,i,h))
            self.assertEqual(e.verify_tests(folder,HEAD,plan,r)['tests'],6090);self.assertEqual(r.validate_module_evidence.call_count,452)
            (folder/'module-225.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.verify_tests(folder,HEAD,plan,r)
    def test_28_failed_regression_stops_before_diagnosis(self):
        diagnosis=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
            e.execute_stages(Mock(side_effect=ValueError('fixture')),diagnosis,Mock(),Mock())
        diagnosis.assert_not_called()
    def test_29_actual_worker_and_fresh_verifier_collaborators(self):
        with tempfile.TemporaryDirectory() as tmp,self.context(),contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);folder=root/'runs/x';folder.mkdir(parents=True);pins={f'p{i}':'a' for i in range(877)};inputs={f'i{i}':'b' for i in range(4360)};calls=[]
            class Cache:
                entries={};stats={'final_reference_rechecks':4360};sha=staticmethod(e.sha)
                def __init__(self, original, lease_factory, *, progress, max_files):
                    e.require(type(max_files) is int and max_files == s.INPUT_COUNT == len(inputs),
                              'worker must pass exact registered lock capacity')
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release')
                def recheck(self):calls.append('final');return [{'path':k,'sha256':v} for k,v in inputs.items()]
            h=dict(runtime=NS(native_runtime=lambda:(NS(__version__='fixture'),NS(__version__='fixture'))),
                locks=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None),
                legacy=NS(descriptors=lambda out,items,*a:e.require(items==e.artifacts(out),'artifacts')),recovery=None)
            cx=(NS(guarded=NS(no_neural=contextlib.nullcontext)),)
            def regression(*a):calls.append('tests');e.save(folder/'regression-result.json',e.receipt(HEAD,6090))
            def diagnostic(out,*a):
                calls.append('diagnose')
                for name in s.OUTPUTS:(out/name).write_bytes(b'fixture')
                return self.summary
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=h),patch.object(e,'snapshot',return_value=({'validation_summary':self.f.parent},{},pins,inputs)),patch.object(e,'parent_semantics',return_value=(root,root,cx)),patch.object(e,'run_logged',side_effect=regression),patch.object(e,'build_plan',return_value={}),patch.object(e,'verify_tests',return_value=dict(tests=6090,modules=226)),patch.object(s,'run_diagnostic',side_effect=diagnostic),patch.object(s,'semantic_recheck',return_value=self.summary):
                e.scientific_worker(root,folder,HEAD);e.verify_outputs(root,folder,HEAD)
                self.assertEqual(calls,['tests','diagnose','final','release'])
                p=folder/'science/summary.json';v=e.read(p);self.assertFalse(v['capability_gate_applicable']);v['capability_gate_applicable']=True;p.write_bytes(s.blob(v))
                with self.assertRaises(ValueError):e.verify_outputs(root,folder,HEAD)
    def test_30_Git_guard_JSON_and_LF_CRLF(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);subprocess.run(['git','init','-q',str(root)],check=True)
            for args in [('checkout','-qb',e.BRANCH),('config','user.name','C336 fixture'),('config','user.email','c336@example.invalid')]:subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
            (root/'docs').mkdir();p=root/'docs/experiment-ledger-and-handoff.md';p.write_text('## Formal state\nC336 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
            subprocess.run(['git','-C',str(root),'add','.'],check=True);subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
            e.guard(root,e.git(root,'rev-parse','HEAD'))
            with self.assertRaises(ValueError):e.guard(root,HEAD)
            path=root/'json';e.save(path,{'名前':'甲乙'});self.assertEqual(e.read(path),{'名前':'甲乙'})
            with self.assertRaises(FileExistsError):e.save(path,{})
            for text in ('{"a":1,"a":2}','NaN'):
                path.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):e.read(path)
            raw=b'a\nb\n';oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
            for b in (raw,raw.replace(b'\n',b'\r\n')):path.write_bytes(b);e.source_bytes(path,oid)
            path.write_bytes(b'changed')
            with self.assertRaises(ValueError):e.source_bytes(path,oid)
    def test_31_real_subprocess_and_launcher_route(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);log=root/'x.log'
            with self.assertRaises(ValueError):e.run_logged(root,[sys.executable,'-c','print("fixture");raise SystemExit(7)'],log,'fixture')
            self.assertIn('fixture',log.read_text(encoding='utf-8'))
        p=subprocess.run([sys.executable,str(ROOT/'tools/c336_execution.py'),'--folder','unused','--expected-head',HEAD,'--mode','bad'],capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(p.returncode,0);self.assertIn('invalid choice',p.stderr)
        text=(ROOT/'tools/invoke_c336.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'):self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C336',text)
    def test_32_no_retry_and_bound_output_bytes(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'guard'),patch.object(e,'run_logged',side_effect=ValueError('fixture')) as call,contextlib.redirect_stdout(io.StringIO()) as log:
            root=Path(tmp)
            with self.assertRaises(ValueError):e.run(root,root/'runs/x',HEAD)
            self.assertEqual(call.call_count,1);self.assertIn('run_execution_valid = false',log.getvalue())
            out=root/'out';out.mkdir()
            for name in s.OUTPUTS:(out/name).write_bytes(b'fixture')
            def mutate():(out/s.OUTPUTS[0]).write_bytes(b'changed')
            with self.assertRaises(ValueError):e.bound_semantics(out,mutate)


if __name__ == '__main__': unittest.main()
