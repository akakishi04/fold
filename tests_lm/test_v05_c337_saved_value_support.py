"""C337 software tests; generated logits/proofs are not scientific measurements."""
from __future__ import annotations
from collections import Counter, defaultdict
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
from fold_lm.v05_benchmarks import model_c337_saved_value_support as s
from fold_lm.v05_benchmarks import model_c336_saved_query_order_patterns as p
from fold_lm.v05_benchmarks import model_c267_name_coverage_training as canonical_source

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.util.spec_from_file_location('_c337_test_executor', ROOT/'tools/c337_execution.py')
e = importlib.util.module_from_spec(loader); loader.loader.exec_module(e)
HEAD = 'a'*40


def canonical_data():
    data = {sp:[] for sp in s.SPLITS}; held = {(0,2),(1,3),(2,0),(3,1)}
    for entities,values,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),s.LANGUAGES):
        split = 'HOLDOUT' if values in held else 'TRAIN'
        for order,query in itertools.product((entities,entities[::-1]),entities):
            data[split].append(dict(id=f'{lang}:{entities}:{values}:{order}:{query}',entities=list(entities),values=list(values),
                language=lang,permutation=list(order),query=query,target=48+values[entities.index(query)]))
    e.require(s.digest(data) == s.DATA_SHA, 'canonical dataset fixture')
    return data


def reference_quad(pred, targets):
    a,b = targets; correct = [x == targets[i%2] for i,x in enumerate(pred)]
    if all(correct): category = 'query_correct'
    elif all(x == targets[1-i%2] for i,x in enumerate(pred)): category = 'query_swapped'
    elif all(x == targets[i//2] for i,x in enumerate(pred)): category = 'first_fact'
    elif all(x == targets[1-i//2] for i,x in enumerate(pred)): category = 'last_fact'
    elif any(x not in targets for x in pred): category = 'other_class'
    elif len(set(pred)) == 1: category = 'value_lock'
    else: category = 'mixed'
    return dict(category=category,correct=sum(correct),both_correct=int(all(correct[:2]))+int(all(correct[2:])),
        four_correct=int(all(correct)),collapsed_orders=int(pred[0] == pred[1])+int(pred[2] == pred[3]),
        order_stable_queries=int(pred[0] == pred[2])+int(pred[1] == pred[3]),other_answers=sum(x not in targets for x in pred))


def fixture():
    data = canonical_data(); records = []; quads = []; strata = defaultdict(list)
    for seed,arm in itertools.product(s.SEEDS,s.ARMS):
        tensors = {}
        for split,rows in data.items():
            z = torch.full((len(rows),256),-5.,dtype=torch.float64)
            for i,row in enumerate(rows):
                t = row['target']; o = 48+row['values'][1-row['entities'].index(row['query'])]
                absent = min(set(range(48,52))-{t,o}); case = (i+seed+int(arm == 'alternating'))%8
                z[i,t] = 2.; z[i,o] = 1.
                if case == 1: z[i,o] = 3.
                elif case == 2: z[i,absent] = 4.
                elif case == 3: z[i,o] = 3.; z[i,absent] = 4.
                elif case == 4: z[i,7] = 4.
                elif case == 5: z[i,t] = 1.; z[i,7] = 4.
                elif case == 6: z[i,t] = 1.
                elif case == 7: z[i,0] = 2.
            tensors[split] = z
        def tree(profiles):
            return {sp:{pr:{v:tensors[sp] for v in ('normal','evidence_blind','query_blind')} for pr in profiles} for sp in s.SPLITS}
        raw = dict(original={str(n):tree(('repeat',) if n == 1 else ('repeat','shared_prefix','shared_suffix')) for n in range(1,7)},
                   interior=tree(('u_dominant','balanced','v_dominant')))
        records.append(dict(seed=seed,arm=arm,state_sha256='a'*64,evaluation_policy='native_before',raw={'evaluation':raw,'replay':raw},
            receipts={m:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for m in ('evaluation','replay')}))
        for domain,split in itertools.product(s.DOMAINS,s.SPLITS):
            rows = data[split]
            for profile in p.profiles(domain):
                for start in range(0,len(rows),4):
                    block = rows[start:start+4]; row = block[0]; targets = [48+v for v in row['values']]
                    pred = tensors[split][start:start+4].argmax(-1).tolist()
                    key = (seed,arm,domain,split,profile,row['language'])
                    q = dict(zip(s.KEYS,key,strict=True),entities=row['entities'],values=row['values'],row_ids=[r['id'] for r in block],
                             predictions=pred,targets=targets,**reference_quad(pred,targets))
                    quads.append(q); strata[key].append(q)
    reports = []
    for key,rows in sorted(strata.items()):
        counts = dict(quads=len(rows),answers=4*len(rows),query_pairs=2*len(rows),
                      categories={c:sum(r['category'] == c for r in rows) for c in p.CATEGORIES})
        for name in ('correct','both_correct','four_correct','collapsed_orders','order_stable_queries','other_answers'):
            counts[name] = sum(r[name] for r in rows)
        reports.append(dict(zip(s.KEYS,key,strict=True),**counts))
    prior = dict(diagnostic_complete=True,parent_validation_summary={'candidate_gate':False,'eligible_seed_count':1},
                 strata=reports,holdout_reconciliation=[{'synthetic':i} for i in range(30)],**p.WORK)
    return NS(data=data,archive=dict(schema='fold-c335-evaluations-v1',records=records),quads=quads,prior=prior)


def fake_recovery():
    def flatten(suite):
        for x in suite:
            if isinstance(x,unittest.TestSuite): yield from flatten(x)
            else: yield x
    def validate(row,g,head,i,ph,launcher,log):
        e.require(row['schema'] == 'fold-c330-r1-module-v2' and row['commit_sha'] == head and row['index'] == i
                  and row['module'] == g['module'] and row['plan_sha256'] == ph,'module ABI')
        e.require(row['result']['success_ids'] == g['test_ids'] and row['result']['tests'] == len(g['test_ids']),'IDs')
        e.require(launcher in (row['pid'],row['parent_pid']),'process topology')
        return 'direct' if launcher == row['pid'] else 'redirected-child'
    return NS(flatten=flatten,EXCLUDED='excluded',allowed_module=lambda n:bool(re.fullmatch(r'tests_lm\.[A-Za-z0-9_]+',n)),
              validate_module_evidence=Mock(side_effect=validate))


def plan_fixture():
    groups=[]; q,r=divmod(6090,226)
    for i in range(226):
        m=f'tests_lm.fixture_{i:03d}';groups.append(dict(module=m,test_ids=[m+f'.C.test_{j:03d}' for j in range(q+(i<r))]))
    groups.append(dict(module=e.TEST_MODULE,test_ids=[e.TEST_MODULE+f'.C337Tests.test_{i:02d}' for i in range(32)]))
    ids=[v for g in groups for v in g['test_ids']]
    return dict(schema='fold-c337-regression-plan-v1',commit_sha=HEAD,manifest_sha256=s.MANIFEST_SHA,
                test_ids_sha256=s.digest(ids),groups=groups),s.digest(ids[:-32])


def proof(folder,plan,i,ph):
    g=plan['groups'][i];pid,parent=20000+i,10000+i
    e.save(folder/f'module-{i:03d}.json',dict(schema='fold-c330-r1-module-v2',commit_sha=HEAD,index=i,module=g['module'],plan_sha256=ph,
        pid=pid,parent_pid=parent,result=dict(tests=len(g['test_ids']),success_ids=g['test_ids'])))
    (folder/f'module-{i:03d}.log').write_bytes(b'explicit synthetic proof')
    return pid if i%2 == 0 else parent


def parent_contract_fixture():
    spec=NS(validate_seal=lambda:None,check_summary=lambda v:None,EXPERIMENT_ID='parent',STAGE='stage',MANIFEST_SHA='manifest',WORK={})
    parent=NS(spec=lambda:spec,PARENT_SUMMARY='source-summary',PARENT_ENVELOPE='source-envelope')
    pins={e.P_PATH:e.P_BLOB,e.S_PATH:e.S_BLOB,**{f'p{i}':'a' for i in range(875)}}
    inputs={f'i{i}':'b' for i in range(4360)}
    r=dict(schema='fold-c336-diagnostic-v1',commit_sha=e.PARENT_HEAD,experiment_id='parent',stage='stage',status='PASS',
        diagnostic_execution_valid=True,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,
        manifest_sha256='manifest',source_blobs=pins,input_sha256=inputs,validation_summary={'parent_validation_summary':{'candidate_gate':False}})
    v=dict(schema='fold-c336-execution-envelope-v1',commit_sha=e.PARENT_HEAD,scientific_status='PASS',scientific_summary_sha256=e.PARENT_SUMMARY,
        manifest_sha256='manifest',scientific_work={},source_count=877,input_count=4360,source_blobs=pins,input_sha256=inputs,
        parent_summary_sha256=parent.PARENT_SUMMARY,parent_envelope_sha256=parent.PARENT_ENVELOPE,
        immediate_parent_semantic_reconstruction=True,parent_regression_reconstructed=True,ancestor_semantic_reruns=0,
        saved_semantic_reconstruction=True,final_reference_rechecks=4360,hash_stats={'final_reference_rechecks':4360},regression=e.receipt(e.PARENT_HEAD,6090))
    return r,v,parent


class C337Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old_threads=torch.get_num_threads();torch.set_num_threads(2);cls.f=fixture()
        with patch.object(p,'previous',return_value=NS(check_summary=lambda v:None)):
            cls.details,cls.reconciled,cls.summary=s.analyze(cls.f.data,cls.f.archive,cls.f.quads,cls.f.prior)
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.old_threads)
    def context(self):return patch.object(p,'previous',return_value=NS(check_summary=lambda v:None))
    def test_01_manifest_and_actual_test_loader(self):
        s.validate_seal();self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),32)
        with patch.object(s,'KINDS',('wrong',)),self.assertRaises(ValueError):s.validate_seal()
        self.assertEqual((s.FULL_TESTS,s.MODULES,s.SOURCE_COUNT,s.INPUT_COUNT),(6090+32,226+1,877+6,4360+461+6))
    def test_02_real_canonical_dataset_and_value_inventory(self):
        self.assertEqual(self.f.data,canonical_source.dataset());self.assertEqual(s.digest(self.f.data),s.DATA_SHA)
        self.assertEqual({tuple(r['values']) for r in self.f.data['HOLDOUT']},{(0,2),(1,3),(2,0),(3,1)})
        self.assertEqual([len(self.f.data[sp]) for sp in s.SPLITS],[192,96])
    def test_03_all12_pairs_all_four_error_kinds(self):
        for t,o in itertools.permutations(range(48,52),2):
            absent=min(set(range(48,52))-{t,o});z=torch.full((4,256),-5.,dtype=torch.float64)
            z[:,t]=2.;z[:,o]=1.
            for i,winner in enumerate((t,o,absent,7)):z[i,winner]=4.
            result=s.audit_logits(z,[t]*4,[o]*4)
            self.assertEqual([r['kind'] for r in result],list(s.KINDS))
    def test_04_outside_winner_can_have_either_within_pair_rank(self):
        z=torch.zeros((3,256),dtype=torch.float64);z[:,7]=5.;z[:,48]=torch.tensor([2.,1.,1.]);z[:,50]=torch.tensor([1.,1.,2.])
        got=s.audit_logits(z,[48]*3,[50]*3)
        self.assertEqual([r['within_pair_order'] for r in got],list(s.ORDERS));self.assertEqual([r['prediction'] for r in got],[7]*3)
    def test_05_all256_argmax_not_restricted(self):
        z=torch.zeros((256,256),dtype=torch.float64);z[torch.arange(256),torch.arange(256)]=1.
        got=s.audit_logits(z,[48]*256,[50]*256);self.assertEqual([r['prediction'] for r in got],list(range(256)))
        self.assertEqual(Counter(r['kind'] for r in got),Counter(correct=1,wrong_observed=1,absent_digit=2,outside_catalog=252))
    def test_06_exact_ties_and_first_index(self):
        z=torch.zeros((2,256),dtype=torch.float64);z[0,48]=z[0,50]=3.;z[1,0]=z[1,48]=3.;z[1,50]=2.
        got=s.audit_logits(z,[50,48],[48,50])
        self.assertEqual((got[0]['prediction'],got[0]['within_pair_order'],got[0]['kind']),(48,'tie','wrong_observed'))
        self.assertEqual((got[1]['prediction'],got[1]['support_margin'],got[1]['kind']),(0,0.,'outside_catalog'))
    def test_07_input_tensors_and_labels_unchanged(self):
        z=torch.randn((5,256),dtype=torch.float64);before=z.clone();t=[48]*5;o=[51]*5;s.audit_logits(z,t,o)
        self.assertTrue(torch.equal(z,before));self.assertEqual(t,[48]*5);self.assertEqual(o,[51]*5)
    def test_08_nonfinite_shape_dtype_gradient_and_overflow_rejected(self):
        cases=[torch.zeros((1,255),dtype=torch.float64),torch.zeros((1,256),dtype=torch.float32),torch.full((1,256),float('nan'),dtype=torch.float64),
               torch.zeros((1,256),dtype=torch.float64,requires_grad=True),torch.empty((0,256),dtype=torch.float64)]
        z=torch.zeros((1,256),dtype=torch.float64);z[0,48]=1e308;z[0,50]=-1e308;cases.append(z)
        for z in cases:
            with self.subTest(),self.assertRaises(ValueError):s.audit_logits(z,[48],[50])
    def test_09_bad_observed_values_and_mismatched_lengths(self):
        z=torch.zeros((1,256),dtype=torch.float64)
        for t,o in (([True],[50]),([48.],[50]),([48],[48]),([48],[52]),([47],[50]),([],[50])):
            with self.subTest(),self.assertRaises(ValueError):s.audit_logits(z,t,o)
    def test_10_margins_match_independent_scalar_reference(self):
        gen=torch.Generator().manual_seed(337001);z=torch.randn((36,256),generator=gen,dtype=torch.float64)
        pairs=list(itertools.permutations(range(48,52),2))*3;t=[a for a,b in pairs];o=[b for a,b in pairs]
        for row,got,(a,b) in zip(z.tolist(),s.audit_logits(z,t,o),pairs,strict=True):
            self.assertEqual(got['prediction'],max(range(256),key=lambda i:row[i]))
            self.assertEqual(got['pair_margin'],row[a]-row[b])
            self.assertEqual(got['support_margin'],max(row[a],row[b])-max(v for i,v in enumerate(row) if i not in (a,b)))
    def test_11_full_analysis_and_parent_counts(self):
        self.assertEqual((len(self.details),len(self.reconciled),len(self.summary['strata'])),(51840,720,720))
        self.assertEqual(s.blob(self.reconciled),s.blob(self.f.prior['strata']))
        self.assertEqual(sum(r['answers'] for r in self.summary['strata']),51840)
        self.assertFalse(self.summary['parent_candidate_gate'])
        for r in self.details:
            expected='correct' if r['prediction']==r['target'] else 'wrong_observed' if r['prediction']==r['other'] else 'absent_digit' if r['prediction'] in range(48,52) else 'outside_catalog'
            self.assertEqual(r['kind'],expected)
    def test_12_changed_parent_prediction_rejected(self):
        q=copy.deepcopy(self.f.quads);q[0]['predictions'][0]=(q[0]['predictions'][0]+1)%256
        with self.context(),self.assertRaisesRegex(ValueError,'quad reconstruction'):s.analyze(self.f.data,self.f.archive,q,self.f.prior)
    def test_13_parent_row_binding_and_categories_rejected(self):
        for k in ('row_ids','category'):
            q=copy.deepcopy(self.f.quads)
            if k=='row_ids':q[0][k][0]='changed'
            else:q[0][k]='changed'
            with self.context(),self.assertRaisesRegex(ValueError,'quad reconstruction'):s.analyze(self.f.data,self.f.archive,q,self.f.prior)
    def test_14_missing_duplicate_quad_and_stratum(self):
        for q in (self.f.quads[:-1],self.f.quads[:-1]+[self.f.quads[0]]):
            with self.context(),self.assertRaises(ValueError):s.analyze(self.f.data,self.f.archive,q,self.f.prior)
        prior=copy.deepcopy(self.f.prior);prior['strata'].pop()
        with self.context(),self.assertRaises(ValueError):s.analyze(self.f.data,self.f.archive,self.f.quads,prior)
    def test_15_source_cohort_and_schema_identity(self):
        for kind in ('drop','policy','schema','receipt'):
            a={'schema':self.f.archive['schema'],'records':[dict(r) for r in self.f.archive['records']]}
            if kind=='drop':a['records'].pop()
            elif kind=='policy':a['records'][0]['evaluation_policy']='first_mean'
            elif kind=='schema':a['schema']='wrong'
            else:a['records'][0]['receipts']={m:dict(calls=1) for m in ('evaluation','replay')}
            with self.context(),self.assertRaises(ValueError):s.analyze(self.f.data,a,self.f.quads,self.f.prior)
    def test_16_canonical_data_and_target_binding_not_binary_fixture(self):
        d=copy.deepcopy(self.f.data);d['TRAIN'][0]['target']=49
        with self.context(),self.assertRaisesRegex(ValueError,'canonical'):s.analyze(d,self.f.archive,self.f.quads,self.f.prior)
    def test_17_summary_partition_invalid_boolean_and_rank(self):
        for kind in ('count','joint','rank','nan','gate'):
            v=copy.deepcopy(self.summary);r=v['strata'][0]
            if kind=='count':r['answers']=True
            elif kind=='joint':r['within_pair']['correct']['tie']+=1
            elif kind=='rank':r['support_rank']['tie']+=1
            elif kind=='nan':r['mean_pair_margin']=float('nan')
            else:v['parent_candidate_gate']=True
            with self.assertRaises(ValueError):s.check_summary(v)
    def test_18_real_loader_writer_saved_reconstruction(self):
        with tempfile.TemporaryDirectory() as tmp,self.context():
            root=Path(tmp);out=root/'out';par=root/'parent';src=root/'source';data=root/'data'
            for f in (out,par,src,data):f.mkdir()
            e.save(data/'dataset.json',self.f.data);e.save(par/'query-order-quads.json',self.f.quads);torch.save(self.f.archive,src/'evaluations.pt')
            v=s.run_diagnostic(out,par,src,data,self.f.prior,e.read);checked=s.semantic_recheck(out,par,src,data,self.f.prior,e.read)
            self.assertEqual(s.blob(v),s.blob(checked));self.assertEqual(set(f.name for f in out.iterdir()),set(s.OUTPUTS))
            (out/'source-reconciliation.json').write_bytes(b'[]')
            with self.assertRaisesRegex(ValueError,'reconstruction'):s.semantic_recheck(out,par,src,data,self.f.prior,e.read)
    def test_19_reconciliation_rejects_changed_parent_aggregate(self):
        prior=copy.deepcopy(self.f.prior);next(r for r in prior['strata'] if r['correct'] > 0)['correct']-=1
        with self.context(),self.assertRaisesRegex(ValueError,'stratum reconstruction'):s.analyze(self.f.data,self.f.archive,self.f.quads,prior)
    def test_20_diagnostic_parent_contract_preserves_negative_grandparent(self):
        e.parent_contract(*parent_contract_fixture())
        for target,k,val in ((0,'status','FAIL'),(0,'capability_gate_applicable',True),(1,'input_count',3893),(1,'source_count',871),(1,'final_reference_rechecks',4359)):
            args=parent_contract_fixture();args[target][k]=val
            with self.subTest(),self.assertRaises(ValueError):e.parent_contract(*args)
    def test_21_all_parent_proofs_and_complete4827_union(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);out=root/e.PARENT_FOLDER/'science';out.mkdir(parents=True);folder=out.parent;items=[]
            for i in range(226):
                a=folder/f'module-{i:03d}.json';b=folder/f'module-{i:03d}.log';a.write_bytes(b'{}');b.write_bytes(b'fixture')
                items.append(dict(index=i,receipt_sha256=e.sha(a),log_sha256=e.sha(b)))
            for name,value in (('regression-plan.json',{}),('regression-result.json',{}),('regression-evidence.json',{'modules':items})):e.save(folder/name,value)
            proofmap=dict(tests=6090,modules=226,plan_sha256=e.sha(folder/'regression-plan.json'),evidence_sha256=e.sha(folder/'regression-evidence.json'),result_sha256=e.sha(folder/'regression-result.json'))
            self.assertEqual(len(e.parent_test_files(folder,{'regression_isolation':proofmap},e.sha)),455)
            pins={};inputs={};tree={}
            for i in range(4360):
                name=f'old/{i}.py' if i<877 else f'data/{i}.bin';path=root/name;path.parent.mkdir(exist_ok=True);raw=str(i).encode();path.write_bytes(raw)
                inputs[e.canonical(path)]=e.sha(path)
                if i<877:pins[name]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();tree[name]=pins[name]
            for name in s.OWN:
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);raw=name.encode();path.write_bytes(raw);tree[name]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            outputs=('audit-plan.json','query-order-quads.json','transitions.json','validation-summary.json')
            for n in outputs:(out/n).write_bytes(b'fixture')
            e.save(out/'summary.json',{'artifacts':[]});e.save(folder/'execution-envelope.json',dict(source_blobs=pins,input_sha256=inputs,regression_isolation=proofmap))
            def ancestor(root,prior,h):
                for name,wanted in inputs.items():self.assertEqual(h(name),wanted)
                return {},{},pins,inputs
            parent=NS(spec=lambda:NS(OUTPUTS=outputs),snapshot=ancestor,build_plan=Mock(return_value={}),verify_tests=Mock(return_value=proofmap))
            h=dict(parent=parent,prior={},recovery=None,legacy=NS(tree_blobs=lambda root:tree,descriptors=lambda out,items,names,h:{e.canonical(out/n):h(out/n) for n in names}))
            with patch.object(e,'PARENT_SUMMARY',e.sha(out/'summary.json')),patch.object(e,'PARENT_ENVELOPE',e.sha(folder/'execution-envelope.json')),patch.object(e,'parent_contract'):
                _,_,sp,ip=e.snapshot(root,h,e.sha);self.assertEqual((len(sp),len(ip)),(883,4827));self.assertEqual(len(inputs),4360)
            (folder/'module-225.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.parent_test_files(folder,{'regression_isolation':proofmap},e.sha)
    def test_22_exact_parent_semantic_loader_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);par=root/e.PARENT_FOLDER/'science';src=root/'c335/science';data=root/'c329/science'
            for f in (par,src,data):f.mkdir(parents=True)
            for f,names in ((par,('audit-plan.json','query-order-quads.json','transitions.json','validation-summary.json')),(src,('evaluations.pt',)),(data,('dataset.json','original-prompts.json','interior-prompts.json'))):
                for n in names:(f/n).write_bytes(b'{}')
            inputs={e.canonical(f):e.sha(f) for folder in (par,src,data) for f in folder.iterdir()}
            saved=self.f.prior;ps=NS(OUTPUTS=tuple(f.name for f in par.iterdir()),semantic_recheck=Mock(return_value=saved))
            h=dict(parent=NS(spec=lambda:ps,PARENT_FOLDER='c335'),c330=NS(PARENT_FOLDER='c329'))
            x=NS(guarded=NS(no_neural=contextlib.nullcontext),c=NS(p267=NS(validate_data=lambda v:None)))
            cx=(None,None,NS(new_prompts=lambda v:{},check_prompts=lambda *a:None),None,None,x)
            base=NS(context=lambda:cx,digest=s.digest,DATA_SHA=s.digest({}),PROMPTS_SHA=s.digest({}))
            old=NS(source=lambda:NS(base=lambda:base),load_data=lambda *a:({}, {}, {}))
            bridge=NS(previous=lambda:NS(previous=lambda:old))
            with patch.object(s,'parent',return_value=bridge):
                self.assertEqual(e.parent_semantics(root,h,{'validation_summary':saved},inputs),(par,src,data,cx))
                ps.semantic_recheck.assert_called_once_with(par,src,data,saved['parent_validation_summary'],cx,e.read)
                del inputs[e.canonical(src/'evaluations.pt')]
                with self.assertRaises(ValueError):e.parent_semantics(root,h,{'validation_summary':saved},inputs)
    def test_23_helper_bridge_pins_both_parent_files_before_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in (e.P_PATH,e.S_PATH):path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b'fixture')
            prior={k:object() for k in ('parent','prior','recovery','c330','runtime','legacy','locks')}
            parent=NS(spec=lambda:NS(validate_seal=Mock()),helpers=Mock(return_value=prior))
            with patch.object(e,'git',side_effect=[e.P_BLOB,e.S_BLOB]),patch.object(e,'source_bytes') as check,patch.object(e.importlib.util,'spec_from_file_location',return_value=NS(loader=NS(exec_module=lambda mod:None))),patch.object(e.importlib.util,'module_from_spec',return_value=parent):
                h=e.helpers(root);self.assertIs(h['prior'],prior);self.assertIs(h['recovery'],prior['recovery']);self.assertEqual(check.call_count,2)
    def test_24_actual_own_loader_appended(self):
        plan,digest=plan_fixture();r=fake_recovery();h=dict(parent=NS(build_plan=Mock(return_value={'groups':plan['groups'][:-1]})),prior={},recovery=r)
        with patch.object(e,'BASE_IDS_SHA',digest):
            got=e.build_plan(ROOT,HEAD,h);self.assertEqual(len(got['groups']),227);self.assertEqual(len(got['groups'][-1]['test_ids']),32)
    def test_25_missing_duplicate_and_reordered_test_plan(self):
        plan,digest=plan_fixture();r=fake_recovery()
        with patch.object(e,'BASE_IDS_SHA',digest):
            e.validate_plan(plan,HEAD,r)
            for kind in ('drop','duplicate','order'):
                v=copy.deepcopy(plan)
                if kind=='drop':v['groups'].pop()
                elif kind=='duplicate':v['groups'][0]['test_ids'][1]=v['groups'][0]['test_ids'][0]
                else:v['groups'][0]['test_ids'].reverse()
                with self.assertRaises(ValueError):e.validate_plan(v,HEAD,r)
    def test_26_collector_and_fresh_verifier_delegate_same_ABI(self):
        plan,digest=plan_fixture();r=fake_recovery()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.collect_tests(folder,HEAD,plan,r,lambda i,h:proof(folder,plan,i,h));v=e.verify_tests(folder,HEAD,plan,r)
            self.assertEqual(v['tests'],6122);self.assertEqual(r.validate_module_evidence.call_count,454)
            (folder/'module-226.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.verify_tests(folder,HEAD,plan,r)
    def test_27_module_child_delegates_only_registered_module(self):
        plan,digest=plan_fixture();r=fake_recovery();g=plan['groups'][0];r.execute_module=Mock(return_value={'tests':len(g['test_ids'])});r.check_module=Mock()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),patch.object(e,'guard'),patch.object(e,'helpers',return_value={'recovery':r}),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.save(folder/'regression-plan.json',plan);e.module_child(folder,folder,HEAD,0,e.sha(folder/'regression-plan.json'))
            r.execute_module.assert_called_once_with(g['module'],g['test_ids']);self.assertEqual(e.read(folder/'module-000.json')['parent_pid'],e.os.getppid())
    def test_28_failed_regression_blocks_science(self):
        probe=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):e.execute_stages(Mock(side_effect=ValueError('fixture')),probe,Mock(),Mock())
        probe.assert_not_called()
    def test_29_worker_capacity_and_fresh_verifier(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);folder=root/'runs/x';folder.mkdir(parents=True);pins={f'p{i}':'a' for i in range(883)};inputs={f'i{i}':'b' for i in range(4827)};calls=[]
            class Cache:
                entries={};stats={'final_reference_rechecks':4827};sha=staticmethod(e.sha)
                def __init__(self,reference,lease_factory,*,progress,max_files):
                    e.require(type(max_files) is int and max_files == s.INPUT_COUNT == len(inputs),'exact lock capacity')
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release')
                def recheck(self):calls.append('final');return [{'path':k,'sha256':v} for k,v in inputs.items()]
            h=dict(runtime=NS(native_runtime=lambda:(NS(__version__='fixture'),NS(__version__='fixture'))),
                locks=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None),
                legacy=NS(descriptors=lambda out,items,*a:e.require(items==e.artifacts(out),'artifacts')),recovery=None)
            cx=(NS(guarded=NS(no_neural=contextlib.nullcontext)),)
            bridge=NS(previous=lambda:NS(previous=lambda:NS(source=lambda:NS(base=lambda:NS(peak_rss=lambda:1)))),profiles=p.profiles)
            def tests(*a):calls.append('tests');e.save(folder/'regression-result.json',e.receipt(HEAD,6122))
            def diagnose(out,*a):
                calls.append('diagnose')
                for n in s.OUTPUTS:(out/n).write_bytes(b'fixture')
                return self.summary
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=h),patch.object(e,'snapshot',return_value=({'validation_summary':self.f.prior},{},pins,inputs)),patch.object(e,'parent_semantics',return_value=(root,root,root,cx)),patch.object(e,'run_logged',side_effect=tests),patch.object(e,'build_plan',return_value={}),patch.object(e,'verify_tests',return_value=dict(tests=6122,modules=227)),patch.object(s,'run_diagnostic',side_effect=diagnose),patch.object(s,'semantic_recheck',return_value=self.summary),patch.object(s,'parent',return_value=bridge):
                e.scientific_worker(root,folder,HEAD);e.verify_outputs(root,folder,HEAD);self.assertEqual(calls,['tests','diagnose','final','release'])
                path=folder/'science/summary.json';v=e.read(path);v['capability_gate_applicable']=True;path.write_bytes(s.blob(v))
                with self.assertRaises(ValueError):e.verify_outputs(root,folder,HEAD)
    def test_30_real_git_strict_JSON_and_source_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);subprocess.run(['git','init','-q',str(root)],check=True)
            for args in [('checkout','-qb',e.BRANCH),('config','user.name','C337 fixture'),('config','user.email','c337@example.invalid')]:subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
            (root/'docs').mkdir();(root/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC337 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
            subprocess.run(['git','-C',str(root),'add','.'],check=True);subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
            e.guard(root,e.git(root,'rev-parse','HEAD'))
            with self.assertRaises(ValueError):e.guard(root,HEAD)
            path=root/'j';e.save(path,{'名前':'甲乙'});self.assertEqual(e.read(path),{'名前':'甲乙'})
            with self.assertRaises(FileExistsError):e.save(path,{})
            for value in ('{"a":1,"a":2}','NaN'):
                path.write_text(value,encoding='utf-8')
                with self.assertRaises(ValueError):e.read(path)
            raw=b'a\nb\n';oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
            for b in (raw,raw.replace(b'\n',b'\r\n')):path.write_bytes(b);e.source_bytes(path,oid)
            path.write_bytes(b'changed')
            with self.assertRaises(ValueError):e.source_bytes(path,oid)
    def test_31_real_process_CLI_and_launcher_preflight(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);log=root/'x.log'
            with self.assertRaises(ValueError):e.run_logged(root,[sys.executable,'-c','print("fixture");raise SystemExit(7)'],log,'fixture')
            self.assertIn('fixture',log.read_text(encoding='utf-8'))
        proc=subprocess.run([sys.executable,str(ROOT/'tools/c337_execution.py'),'--folder','unused','--expected-head',HEAD,'--mode','bad'],capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(proc.returncode,0);self.assertIn('invalid choice',proc.stderr)
        text=(ROOT/'tools/invoke_c337.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'):self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C337',text);self.assertIn('c337_execution.py',(ROOT/'tools/run_c337.ps1').read_text(encoding='utf-8'))
    def test_32_no_retry_and_output_mutation_guard(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'guard'),patch.object(e,'run_logged',side_effect=ValueError('fixture')) as call,contextlib.redirect_stdout(io.StringIO()) as stream:
            root=Path(tmp)
            with self.assertRaises(ValueError):e.run(root,root/'runs/x',HEAD)
            self.assertEqual(call.call_count,1);self.assertIn('run_execution_valid = false',stream.getvalue())
            out=root/'out';out.mkdir()
            for n in s.OUTPUTS:(out/n).write_bytes(b'fixture')
            def change():(out/s.OUTPUTS[0]).write_bytes(b'changed')
            with self.assertRaises(ValueError):e.bound_semantics(out,change)


if __name__ == '__main__':unittest.main()
