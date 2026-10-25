"""C339 software tests. Synthetic logits/ancestor proofs are not native FOLD results."""
from __future__ import annotations
import contextlib
import copy
import hashlib
import importlib.util
import io
import itertools
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch
import torch
from fold_lm.v05_benchmarks import model_c339_saved_support_transfer as s

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.util.spec_from_file_location('_c339_tests_executor',ROOT/'tools/c339_execution.py')
e = importlib.util.module_from_spec(loader); loader.loader.exec_module(e)
HEAD = 'a'*40


def data_fixture():
    data = {'TRAIN':[],'HOLDOUT':[]}; held = {(0,2),(1,3),(2,0),(3,1)}
    for entities,values,lang in itertools.product(((0,1),(0,2),(1,2)),itertools.permutations(range(4),2),('en','ja')):
        split = 'HOLDOUT' if values in held else 'TRAIN'
        for order,query in itertools.product((entities,entities[::-1]),entities):
            data[split].append(dict(id=f'{lang}:{entities}:{values}:{order}:{query}',entities=list(entities),values=list(values),
                language=lang,permutation=list(order),query=query,target=48+values[entities.index(query)]))
    return data


def check_contrast(z):
    keys = ('answers','query_pairs','control_correct','candidate_correct','control_both_correct','candidate_both_correct',
            'rescued','regressed','pair_rescued','pair_regressed','answer_gain','query_pair_gain')
    e.require(set(z) == set(keys) and all(type(z[k]) is int for k in keys),'contrast fields')
    e.require(z['answers'] == 288 and z['query_pairs'] == 144,'contrast denominators')
    for k in keys[2:-2]:
        maximum = 144 if k in ('control_both_correct','candidate_both_correct','pair_rescued','pair_regressed') else 288
        e.require(0 <= z[k] <= maximum,'contrast range')
    e.require(z['candidate_correct']-z['control_correct'] == z['answer_gain'] == z['rescued']-z['regressed']
              and z['candidate_both_correct']-z['control_both_correct'] == z['query_pair_gain'] == z['pair_rescued']-z['pair_regressed'],'contrast conservation')


def parent_double():
    def check(v):e.require(v['candidate_gate'] is False and v['eligible_seed_count'] == 0,'synthetic negative')
    return NS(check_summary=check,previous=lambda:NS(contrast_check=check_contrast))


def independent_counts(z,rows):
    counts = dict(answers=len(rows),correct=0,wrong_observed=0,absent_digit=0,outside_catalog=0)
    for pred,r in zip(z.argmax(1).tolist(),rows,strict=True):
        other = 48+r['values'][1-r['entities'].index(r['query'])]
        k = 'correct' if pred == r['target'] else 'wrong_observed' if pred == other else 'absent_digit' if pred in range(48,52) else 'outside_catalog'
        counts[k] += 1
    return counts


def independent_contrast(left,right,rows):
    # Canonical dataset writes each two-query pair adjacently. Independently checked below.
    target = [r['target'] for r in rows]
    a = [p == t for p,t in zip(left.argmax(1).tolist(),target,strict=True)]*3
    b = [p == t for p,t in zip(right.argmax(1).tolist(),target,strict=True)]*3
    pa = [all(a[i:i+2]) for i in range(0,len(a),2)]; pb = [all(b[i:i+2]) for i in range(0,len(b),2)]
    ca,cb = independent_counts(left,rows),independent_counts(right,rows)
    return dict(answers=288,query_pairs=144,control_correct=sum(a),candidate_correct=sum(b),
        control_both_correct=sum(pa),candidate_both_correct=sum(pb),answer_gain=sum(b)-sum(a),query_pair_gain=sum(pb)-sum(pa),
        rescued=sum(not x and y for x,y in zip(a,b)),regressed=sum(x and not y for x,y in zip(a,b)),
        pair_rescued=sum(not x and y for x,y in zip(pa,pb)),pair_regressed=sum(x and not y for x,y in zip(pa,pb)),
        outside_gain=3*(cb['absent_digit']+cb['outside_catalog']-ca['absent_digit']-ca['outside_catalog']))


def fixture():
    data = data_fixture(); records = []; flags = []; comparisons = []; tensors = {}
    for seed,arm in s.identities():
        views = {}
        for split,rows in data.items():
            z = torch.full((len(rows),256),-8.,dtype=torch.float64)
            for i,r in enumerate(rows):
                t = r['target']; other = 48+r['values'][1-r['entities'].index(r['query'])]
                absent = min(set(range(48,52))-{t,other}); z[i,t] = 3.; z[i,other] = 1.
                mod = (i+seed)%6
                if mod == 0 and arm == 'native':z[i,absent] = 4.
                elif mod == 1:z[i,other] = 5. if arm == 'native' else 0.
                elif mod == 2:z[i,100 if arm == 'native' else other] = 6.
                elif mod == 3:z[i,other] = 3.
                elif mod == 4 and arm == 'support_loss':z[i,absent] = 4.
            views[split] = z
        tensors[seed,arm] = views
        # Shared immutable synthetic views keep this software fixture small.
        raw = dict(original={str(n):{sp:{p:{'normal':views[sp]} for p in s.profiles('original'+str(n))} for sp in s.SPLITS} for n in range(2,7)},
                   interior={sp:{p:{'normal':views[sp]} for p in s.profiles('interior4')} for sp in s.SPLITS})
        records.append(dict(seed=seed,arm=arm,state_sha256='b'*64,evaluation_policy='native_before',
            raw={m:copy.deepcopy(raw) for m in ('evaluation','replay')},
            receipts={m:dict(calls=171,query_calls=342,rows=16416,grad_calls=0) for m in ('evaluation','replay')}))
        counts = independent_counts(views['HOLDOUT'],data['HOLDOUT']); counts = {k:3*v for k,v in counts.items()}
        flags.append(dict(seed=seed,arm=arm,support={d:dict(counts) for d in s.DOMAINS}))
    for seed in s.SEEDS:
        c = independent_contrast(tensors[seed,'native']['HOLDOUT'],tensors[seed,'support_loss']['HOLDOUT'],data['HOLDOUT'])
        comparisons.append(dict(seed=seed,domains={d:dict(c) for d in s.DOMAINS}))
    prior = dict(candidate_gate=False,eligible_seed_count=0,seed_results=flags,paired_comparisons=comparisons)
    return data,dict(schema='fold-c338-evaluations-v1',records=records),prior


def fake_recovery():
    def flatten(suite):
        for x in suite:
            if isinstance(x,unittest.TestSuite):yield from flatten(x)
            else:yield x
    def validate(row,g,head,i,ph,launcher,log):
        e.require(row['schema']=='fold-c330-r1-module-v2' and row['commit_sha']==head and row['index']==i
                  and row['module']==g['module'] and row['plan_sha256']==ph,'module ABI')
        e.require(row['result']['success_ids']==g['test_ids'] and row['result']['tests']==len(g['test_ids']),'complete IDs')
        e.require(launcher in (row['pid'],row['parent_pid']),'PID relation')
        return 'direct' if launcher==row['pid'] else 'redirected-child'
    return NS(flatten=flatten,EXCLUDED='excluded',allowed_module=lambda n:bool(re.fullmatch(r'tests_lm\.[A-Za-z0-9_]+',n)),
              validate_module_evidence=Mock(side_effect=validate))


def plan_fixture():
    groups = []; q,r = divmod(6170,228)
    for i in range(228):
        m = f'tests_lm.fixture_{i:03d}'; groups.append(dict(module=m,test_ids=[m+f'.C.test_{j:03d}' for j in range(q+(i<r))]))
    groups.append(dict(module=e.TEST_MODULE,test_ids=[e.TEST_MODULE+f'.C339Tests.test_{i:02d}' for i in range(32)]))
    ids = [v for g in groups for v in g['test_ids']]
    return dict(schema='fold-c339-regression-plan-v1',commit_sha=HEAD,manifest_sha256=s.MANIFEST_SHA,test_ids_sha256=s.digest(ids),groups=groups),s.digest(ids[:-32])


def proof(folder,plan,i,ph):
    g = plan['groups'][i]; pid,parent = 20000+i,10000+i
    e.save(folder/f'module-{i:03d}.json',dict(schema='fold-c330-r1-module-v2',commit_sha=HEAD,index=i,module=g['module'],plan_sha256=ph,
        pid=pid,parent_pid=parent,result=dict(tests=len(g['test_ids']),success_ids=g['test_ids'])))
    (folder/f'module-{i:03d}.log').write_bytes(b'explicit synthetic proof'); return pid if i%2==0 else parent


def parent_fixture():
    ps = NS(validate_seal=lambda:None,check_summary=lambda v:None,EXPERIMENT_ID='parent',STAGE='stage',MANIFEST_SHA='manifest',WORK={})
    parent = NS(spec=lambda:ps,PARENT_SUMMARY='old-summary',PARENT_ENVELOPE='old-envelope')
    pins = {e.P_PATH:e.P_BLOB,e.S_PATH:e.S_BLOB,**{f'p{i}':'a' for i in range(887)}}; inputs = {f'i{i}':'b' for i in range(5296)}
    r = dict(schema='fold-c338-trained-v1',commit_sha=e.PARENT_HEAD,experiment_id='parent',stage='stage',status='FAIL',
        scientific_execution_valid=True,capability_gate_applicable=True,gate_f_candidate=False,production_adoption=False,
        manifest_sha256='manifest',source_blobs=pins,input_sha256=inputs,validation_summary=dict(candidate_gate=False,eligible_seed_count=0))
    v = dict(schema='fold-c338-execution-envelope-v1',commit_sha=e.PARENT_HEAD,scientific_status='FAIL',scientific_summary_sha256=e.PARENT_SUMMARY,
        manifest_sha256='manifest',scientific_work={},source_count=889,input_count=5296,source_blobs=pins,input_sha256=inputs,
        parent_summary_sha256=parent.PARENT_SUMMARY,parent_envelope_sha256=parent.PARENT_ENVELOPE,immediate_parent_semantic_reconstruction=True,
        parent_regression_reconstructed=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,final_reference_rechecks=5296,
        hash_stats={'final_reference_rechecks':5296},regression=e.receipt(e.PARENT_HEAD,6170))
    return r,v,parent


class C339Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threads = torch.get_num_threads(); torch.set_num_threads(2)
        cls.data,cls.archive,cls.prior = fixture()
        with patch.object(s,'parent',return_value=parent_double()):cls.details,cls.paired,cls.value = s.analyze(cls.data,cls.archive,cls.prior)
    @classmethod
    def tearDownClass(cls):torch.set_num_threads(cls.threads)
    def parent_context(self):return patch.object(s,'parent',return_value=parent_double())
    def test_01_manifest_actual_loader_and_work(self):
        s.validate_seal();self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),32)
        self.assertEqual((s.SOURCE_COUNT,s.INPUT_COUNT,s.FULL_TESTS,s.MODULES),(889+6,5296+467+6,6170+32,228+1))
        with patch.object(s,'SEEDS',(1,)),self.assertRaises(ValueError):s.validate_seal()
    def test_02_actual_canonical_dataset_and_nonbinary_values(self):
        from fold_lm.v05_benchmarks import model_c267_name_coverage_training as p
        self.assertEqual(self.data,p.dataset());self.assertEqual(s.digest(self.data),s.DATA_SHA)
        self.assertEqual(len({tuple(r['values']) for rows in self.data.values() for r in rows}),12)
        self.assertEqual([len(self.data[k]) for k in s.SPLITS],[192,96])
    def test_03_raw256_argmax_not_pair_filter(self):
        z = torch.full((3,256),-5.,dtype=torch.float64);z[:,48]=2.;z[:,50]=1.;z[0,49]=4.;z[1,88]=5.;z[2,50]=3.
        got = s.components(z,[48]*3,[50]*3)
        self.assertEqual([r['prediction'] for r in got],[49,88,50]);self.assertEqual([r['kind'] for r in got],list(s.KINDS[2:])+['wrong_observed'])
        self.assertEqual(got[0]['within_pair_order'],'target_higher')
    def test_04_exact_ties_preserved(self):
        z = torch.zeros((1,256),dtype=torch.float64);r=s.components(z,[48],[50])[0]
        self.assertEqual((r['prediction'],r['pair_margin'],r['support_margin']),(0,0.,0.));self.assertEqual(r['within_pair_order'],'tie')
        self.assertAlmostEqual(r['support_nll'],math.log(128),places=13);self.assertAlmostEqual(r['within_nll'],math.log(2),places=13)
    def test_05_NLL_decomposition_against_independent_logsoftmax(self):
        z=torch.randn((12,256),generator=torch.Generator().manual_seed(339),dtype=torch.float64)*3
        t=[48,49,50,51]*3;o=[50,51,48,49]*3;got=s.components(z,t,o);logp=z.log_softmax(1)
        for i,r in enumerate(got):
            support=-torch.logsumexp(logp[i,[t[i],o[i]]],0).item()
            within=torch.nn.functional.cross_entropy(z[i,[t[i],o[i]]][None,:],torch.tensor([0])).item()
            self.assertAlmostEqual(r['support_nll'],support,places=12);self.assertAlmostEqual(r['within_nll'],within,places=12)
            self.assertAlmostEqual(r['support_nll']+r['within_nll'],-logp[i,t[i]].item(),places=12)
        z=torch.full((1,256),-100.,dtype=torch.float64);z[0,48]=0.;z[0,50]=21.
        self.assertGreater(s.components(z,[48],[50])[0]['within_nll'],21.)
    def test_06_input_immutable_shift_invariant(self):
        z=torch.randn((4,256),dtype=torch.float64);before=z.clone();t=[48]*4;o=[51]*4
        a=s.components(z,t,o);b=s.components(z+17,t,o);self.assertTrue(torch.equal(z,before))
        for x,y in zip(a,b):
            self.assertEqual(x['prediction'],y['prediction'])
            for f in ('support_nll','within_nll','pair_margin','support_margin'):self.assertAlmostEqual(x[f],y[f],places=12)
    def test_07_nonfinite_overflow_rejected(self):
        for bad in (float('nan'),float('inf')):
            z=torch.zeros((1,256),dtype=torch.float64);z[0,4]=bad
            with self.assertRaises(ValueError):s.components(z,[48],[49])
        z=torch.full((1,256),1e308,dtype=torch.float64);z[0,48:50]=-1e308
        with self.assertRaises(ValueError):s.components(z,[48],[49])
    def test_08_input_shapes_types_and_support_identities(self):
        z=torch.zeros((1,256),dtype=torch.float64)
        for a,b in (([48],[48]),([True],[49]),([48.],[49]),([48],[52])):
            with self.assertRaises(ValueError):s.components(z,a,b)
        for value in (z.float(),z[:,:255],z.requires_grad_()):
            with self.assertRaises(ValueError):s.components(value,[48],[49])
    def test_09_transition_directions_and_rescue_conservation(self):
        rows=self.data['HOLDOUT'][:4];t=[r['target'] for r in rows];o=[48+r['values'][1-r['entities'].index(r['query'])] for r in rows]
        a=torch.full((4,256),-4.,dtype=torch.float64);b=a.clone()
        for i in range(4):a[i,t[i]]=3.;b[i,t[i]]=3.
        a[0,88]=5.;b[1,99]=5.;a[2,o[2]]=5.;b[2,88]=6.
        left=s.components(a,t,o);right=s.components(b,t,o)
        for i,(x,y) in enumerate(zip(left,right)):x['row_id']=y['row_id']=str(i)
        r=s.transitions(left,right)
        self.assertEqual((r['rescued'],r['regressed']),(1,1))
        self.assertEqual(r['kind_matrix']['outside_catalog']['correct'],1);self.assertEqual(r['kind_matrix']['wrong_observed']['outside_catalog'],1)
        self.assertEqual(sum(sum(v.values()) for v in r['kind_matrix'].values()),4)
    def test_10_pair_identity_and_delta_overflow_rejected(self):
        a=copy.deepcopy(self.details[:2]);b=copy.deepcopy(a);b[0]['row_id']='bad'
        with self.assertRaises(ValueError):s.transitions(a,b)
        b=copy.deepcopy(a);b[0]['support_margin']=1e308;a[0]['support_margin']=-1e308
        with self.assertRaises(ValueError):s.transitions(a,b)
    def test_11_query_pairs_are_canonical_and_duplicates_rejected(self):
        for rows in self.data.values():self.assertEqual(s.query_pairs(rows),[(i,i+1) for i in range(0,len(rows),2)])
        rows=copy.deepcopy(self.data['HOLDOUT']);rows[1]=copy.deepcopy(rows[0])
        with self.assertRaises(ValueError):s.query_pairs(rows)
    def test_12_aggregation_uses_exact_answer_weights(self):
        a=self.details[:17];r=s.aggregate(a)
        self.assertEqual(sum(r['kinds'].values()),17)
        self.assertAlmostEqual(r['mean_support_nll'],sum(v['support_nll'] for v in a)/17,places=12)
        self.assertAlmostEqual(r['mean_within_nll'],sum(v['within_nll'] for v in a)/17,places=12)
    def test_13_actual_analysis_full_inventory_and_parent_reconciliation(self):
        self.assertEqual((len(self.details),len(self.paired),len(self.value['strata'])),(51840,360,720))
        self.assertEqual(sum(r['answers'] for r in self.paired),25920)
        self.assertEqual(len(self.value['reconciled_contrasts']),30)
        with self.parent_context():s.check_summary(self.value)
        self.assertEqual({r['kind'] for r in self.details},set(s.KINDS))
    def test_14_missing_reordered_wrong_schema_and_dataset(self):
        for kind in ('missing','reordered','schema','data'):
            data=copy.deepcopy(self.data);archive=dict(self.archive,records=list(self.archive['records']))
            if kind=='missing':archive['records'].pop()
            elif kind=='reordered':archive['records'].reverse()
            elif kind=='schema':archive['schema']='fold-c335-evaluations-v1'
            else:data['TRAIN'][0]['target']=0
            with self.parent_context(),self.assertRaises(ValueError):s.analyze(data,archive,self.prior)
    def test_15_source_record_receipt_and_replay_tamper(self):
        for kind in ('receipt','hash','replay'):
            archive=copy.deepcopy(self.archive)
            if kind=='receipt':archive['records'][0]['receipts']['evaluation']['calls']=0
            elif kind=='hash':archive['records'][0]['state_sha256']='bad'
            else:archive['records'][0]['raw']['replay']['original']['2']['TRAIN']['repeat']['normal'][0,0]+=1
            with self.parent_context(),self.assertRaises(ValueError):s.analyze(self.data,archive,self.prior)
    def test_16_parent_counts_and_rescue_counts_must_match(self):
        for kind in ('support','contrast'):
            prior=copy.deepcopy(self.prior)
            if kind=='support':prior['seed_results'][0]['support']['original2']['correct']+=1
            else:prior['paired_comparisons'][0]['domains']['original2']['rescued']+=1
            with self.parent_context(),self.assertRaises(ValueError):s.analyze(self.data,self.archive,prior)
    def test_17_summary_marginal_tamper(self):
        for kind in ('work','matrix','strata','nll','parent','contrast','sign'):
            v=copy.deepcopy(self.value)
            if kind=='work':v['saved_states']=True
            elif kind=='matrix':v['paired_strata'][0]['kind_matrix']['correct']['correct']+=1
            elif kind=='strata':v['strata'][0]['kinds']['correct']+=1
            elif kind=='nll':v['strata'][0]['mean_support_nll']=-1.
            elif kind=='parent':v['parent_candidate_gate']=True
            elif kind=='sign':
                m=v['paired_strata'][0]['sign_matrices']['support_margin']
                a,b=next((a,b) for a in m for b in m[a] if m[a][b]);m[a][b]-=1
                m['zero']['zero']+=1
            else:v['reconciled_contrasts'][0]['rescued']+=1
            with self.parent_context(),self.assertRaises(ValueError):s.check_summary(v)
    def test_18_real_loader_writer_semantic_roundtrip_and_tamper(self):
        with tempfile.TemporaryDirectory() as tmp,self.parent_context():
            root=Path(tmp);out=root/'out';out.mkdir();src=root/'source';src.mkdir();data=root/'data';data.mkdir()
            e.save(data/'dataset.json',self.data);torch.save(self.archive,src/'evaluations.pt')
            actual=s.run_audit(out,src,data,self.prior,e.read);self.assertEqual(actual,self.value)
            self.assertEqual(set(p.name for p in out.iterdir()),set(s.OUTPUTS))
            self.assertEqual(s.semantic_recheck(out,src,data,self.prior,e.read),actual)
            (out/'paired-transitions.json').write_bytes(b'[]')
            with self.assertRaises(ValueError):s.semantic_recheck(out,src,data,self.prior,e.read)
    def test_19_parent_negative_contract_not_diagnostic_PASS(self):
        e.parent_contract(*parent_fixture())
        for target,k,v in ((0,'status','PASS'),(0,'capability_gate_applicable',False),(1,'input_count',4827),(1,'final_reference_rechecks',5295)):
            args=parent_fixture();args[target][k]=v
            with self.assertRaises(ValueError):e.parent_contract(*args)
    def test_20_all459parent_proof_files_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);items=[]
            for i in range(228):
                a=folder/f'module-{i:03d}.json';b=folder/f'module-{i:03d}.log';a.write_bytes(b'{}');b.write_bytes(b'fixture')
                items.append(dict(index=i,receipt_sha256=e.sha(a),log_sha256=e.sha(b)))
            for name,value in (('regression-plan.json',{}),('regression-result.json',{}),('regression-evidence.json',{'modules':items})):e.save(folder/name,value)
            bound=dict(tests=6170,modules=228,plan_sha256=e.sha(folder/'regression-plan.json'),evidence_sha256=e.sha(folder/'regression-evidence.json'),result_sha256=e.sha(folder/'regression-result.json'))
            self.assertEqual(len(e.parent_test_files(folder,{'regression_isolation':bound},e.sha)),459)
            (folder/'module-227.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.parent_test_files(folder,{'regression_isolation':bound},e.sha)
    def test_21_actual_snapshot_complete5769_union(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);out=root/e.PARENT_FOLDER/'science';out.mkdir(parents=True);pins={};inputs={};tree={}
            for i in range(5296):
                name=f'old/{i}.py' if i<889 else f'data/{i}.bin';path=root/name;path.parent.mkdir(exist_ok=True);raw=str(i).encode();path.write_bytes(raw)
                inputs[e.canonical(path)]=e.sha(path)
                if i<889:pins[name]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();tree[name]=pins[name]
            for name in s.OWN:
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);raw=name.encode();path.write_bytes(raw);tree[name]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            names=('experiment-plan.json','training-traces.json','trained-models.pt','evaluations.pt','measurements.json','validation-summary.json')
            for n in names:(out/n).write_bytes(b'fixture')
            proofs={}
            for i in range(459):path=out.parent/f'proof-{i}';path.write_bytes(b'fixture');proofs[e.canonical(path)]=e.sha(path)
            e.save(out/'summary.json',{'artifacts':[]});e.save(out.parent/'execution-envelope.json',dict(source_blobs=pins,input_sha256=inputs,regression_isolation={}))
            def ancestor(root,prior,h):
                for name,wanted in inputs.items():self.assertEqual(h(name),wanted)
                return {},{},pins,inputs
            h=dict(parent=NS(spec=lambda:NS(OUTPUTS=names),snapshot=ancestor,build_plan=lambda *a:{},verify_tests=lambda *a:{}),prior={},recovery=None,
                legacy=NS(tree_blobs=lambda root:tree,descriptors=lambda out,items,names,h:{e.canonical(out/n):h(out/n) for n in names}))
            with patch.object(e,'PARENT_SUMMARY',e.sha(out/'summary.json')),patch.object(e,'PARENT_ENVELOPE',e.sha(out.parent/'execution-envelope.json')), \
                 patch.object(e,'parent_contract'),patch.object(e,'parent_test_files',return_value=proofs):
                _,_,p,v=e.snapshot(root,h,e.sha);self.assertEqual((len(p),len(v)),(895,5769));self.assertEqual(len(inputs),5296)
    def test_22_exact_four_argument_parent_semantics(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);source=root/e.PARENT_FOLDER/'science';data=root/'c329/science';source.mkdir(parents=True);data.mkdir(parents=True)
            names=('experiment-plan.json','training-traces.json','trained-models.pt','evaluations.pt','measurements.json','validation-summary.json')
            for folder,ns in ((source,names),(data,('dataset.json','original-prompts.json','interior-prompts.json'))):
                for n in ns:(folder/n).write_bytes(b'{}')
            inputs={e.canonical(f):e.sha(f) for folder in (source,data) for f in folder.iterdir()};saved={'synthetic':'parent'}
            x=NS(guarded=NS(no_neural=contextlib.nullcontext),c=NS(p267=NS(validate_data=lambda v:None)))
            cx=(None,None,NS(new_prompts=lambda v:{},check_prompts=lambda *a:None),None,None,x)
            base=NS(context=lambda:cx,digest=s.digest,DATA_SHA=s.digest({}),PROMPTS_SHA=s.digest({}))
            previous=NS(source=lambda:NS(base=lambda:base),load_data=lambda *a:({}, {}, {}))
            ps=NS(OUTPUTS=names,previous=lambda:previous,semantic_recheck=Mock(return_value=saved))
            h=dict(parent=NS(spec=lambda:ps),c330=NS(PARENT_FOLDER='c329'))
            self.assertEqual(e.parent_semantics(root,h,{'validation_summary':saved},inputs),(source,data,cx))
            ps.semantic_recheck.assert_called_once_with(source,data,cx,e.read)
            del inputs[e.canonical(source/'trained-models.pt')]
            with self.assertRaises(ValueError):e.parent_semantics(root,h,{'validation_summary':saved},inputs)
    def test_23_helper_pins_precede_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in (e.P_PATH,e.S_PATH):p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'fixture')
            prior={k:object() for k in ('parent','prior','recovery','c330','runtime','legacy','locks')}
            parent=NS(spec=lambda:NS(validate_seal=Mock()),helpers=Mock(return_value=prior))
            with patch.object(e,'git',side_effect=[e.P_BLOB,e.S_BLOB]),patch.object(e,'source_bytes') as check, \
                 patch.object(e.importlib.util,'spec_from_file_location',return_value=NS(loader=NS(exec_module=lambda m:None))), \
                 patch.object(e.importlib.util,'module_from_spec',return_value=parent):
                self.assertIs(e.helpers(root)['prior'],prior);self.assertEqual(check.call_count,2)
    def test_24_actual_own_loader_plan_and_changed_inventory(self):
        plan,digest=plan_fixture();r=fake_recovery();h=dict(parent=NS(build_plan=lambda *a:{'groups':plan['groups'][:-1]}),prior={},recovery=r)
        with patch.object(e,'BASE_IDS_SHA',digest):
            got=e.build_plan(ROOT,HEAD,h);self.assertEqual((len(got['groups']),len(got['groups'][-1]['test_ids'])),(229,32))
            for kind in ('drop','duplicate','order'):
                v=copy.deepcopy(plan)
                if kind=='drop':v['groups'].pop()
                elif kind=='duplicate':v['groups'][0]['test_ids'][1]=v['groups'][0]['test_ids'][0]
                else:v['groups'][0]['test_ids'].reverse()
                with self.assertRaises(ValueError):e.validate_plan(v,HEAD,r)
    def test_25_collector_and_verifier_same_PID_ABI(self):
        plan,digest=plan_fixture();r=fake_recovery()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.collect_tests(folder,HEAD,plan,r,lambda i,h:proof(folder,plan,i,h));v=e.verify_tests(folder,HEAD,plan,r)
            self.assertEqual(v['tests'],6202);self.assertEqual(r.validate_module_evidence.call_count,458)
            (folder/'module-228.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.verify_tests(folder,HEAD,plan,r)
    def test_26_module_dispatch_exact_registered_IDs(self):
        plan,digest=plan_fixture();r=fake_recovery();g=plan['groups'][0];r.execute_module=Mock(return_value={'tests':len(g['test_ids'])});r.check_module=Mock()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),patch.object(e,'guard'),patch.object(e,'helpers',return_value={'recovery':r}),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.save(folder/'regression-plan.json',plan);e.module_child(folder,folder,HEAD,0,e.sha(folder/'regression-plan.json'))
            r.execute_module.assert_called_once_with(g['module'],g['test_ids'])
            self.assertEqual(e.read(folder/'module-000.json')['parent_pid'],e.os.getppid())
    def test_27_worker_capacity_fresh_verification_and_mutation(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);folder=root/'runs/x';folder.mkdir(parents=True);pins={f'p{i}':'a' for i in range(895)};inputs={f'i{i}':'b' for i in range(5769)};calls=[]
            value=self.value
            class Cache:
                entries={};stats={'final_reference_rechecks':5769};sha=staticmethod(e.sha)
                def __init__(self,reference,lease_factory,*,progress,max_files):e.require(type(max_files) is int and max_files==s.INPUT_COUNT==len(inputs),'exact finite capacity')
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release')
                def recheck(self):calls.append('final');return [{'path':k,'sha256':v} for k,v in inputs.items()]
            h=dict(runtime=NS(native_runtime=lambda:(NS(__version__='fixture'),NS(__version__='fixture'))),
                locks=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None),
                legacy=NS(descriptors=lambda out,items,*a:e.require(items==e.artifacts(out),'artifacts')),recovery=None)
            cx=(NS(guarded=NS(no_neural=contextlib.nullcontext)),)
            p=parent_double();p.previous=lambda:NS(contrast_check=check_contrast,source=lambda:NS(base=lambda:NS(check_dependencies=lambda *a:None,peak_rss=lambda:1)))
            def tests(*a):calls.append('tests');e.save(folder/'regression-result.json',e.receipt(HEAD,6202))
            def audit(out,*a):
                calls.append('audit')
                for n in s.OUTPUTS:(out/n).write_bytes(b'fixture')
                return value
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=h),patch.object(e,'snapshot',return_value=({'validation_summary':{}},{},pins,inputs)), \
                 patch.object(e,'parent_semantics',return_value=(root,root,cx)),patch.object(e,'run_logged',side_effect=tests),patch.object(e,'build_plan',return_value={}), \
                 patch.object(e,'verify_tests',return_value=dict(tests=6202,modules=229)),patch.object(s,'run_audit',side_effect=audit), \
                 patch.object(s,'semantic_recheck',return_value=value),patch.object(s,'parent',return_value=p):
                e.scientific_worker(root,folder,HEAD);e.verify_outputs(root,folder,HEAD)
                self.assertEqual(calls,['tests','audit','final','release'])
                path=folder/'science/summary.json';v=e.read(path);self.assertFalse(v['capability_gate_applicable']);v['capability_gate_applicable']=True;path.write_bytes(s.blob(v))
                with self.assertRaises(ValueError):e.verify_outputs(root,folder,HEAD)
    def test_28_failed_regression_blocks_audit_and_no_retry(self):
        audit=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):e.execute_stages(Mock(side_effect=ValueError('fixture')),audit,Mock(),Mock())
        audit.assert_not_called()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'guard'),patch.object(e,'run_logged',side_effect=ValueError('fixture')) as run,contextlib.redirect_stdout(io.StringIO()) as output:
            root=Path(tmp)
            with self.assertRaises(ValueError):e.run(root,root/'runs/x',HEAD)
            self.assertEqual(run.call_count,1);self.assertIn('run_execution_valid = false',output.getvalue())
    def test_29_real_Git_guard_JSON_and_CRLF(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);subprocess.run(['git','init','-q',str(root)],check=True)
            for args in [('checkout','-qb',e.BRANCH),('config','user.name','C339 fixture'),('config','user.email','c339@example.invalid')]:subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
            (root/'docs').mkdir();(root/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC339 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
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
        self.assertFalse(e.active('## Formal state\nC338 ACTIVE / NOT YET JUDGED\n'))
    def test_30_real_subprocess_and_CLI_bad_mode(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);log=root/'x.log'
            with self.assertRaises(ValueError):e.run_logged(root,[sys.executable,'-c','print("fixture");raise SystemExit(7)'],log,'fixture')
            self.assertIn('fixture',log.read_text(encoding='utf-8'))
        proc=subprocess.run([sys.executable,str(ROOT/'tools/c339_execution.py'),'--folder','unused','--expected-head',HEAD,'--mode','bad'],capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(proc.returncode,0);self.assertIn('invalid choice',proc.stderr)
    def test_31_saved_outputs_hashbound_and_exclusive(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            for n in s.OUTPUTS:(out/n).write_bytes(b'fixture')
            def change():(out/s.OUTPUTS[0]).write_bytes(b'changed')
            with self.assertRaises(ValueError):e.bound_semantics(out,change)
    def test_32_launcher_preflight_and_current_routes(self):
        text=(ROOT/'tools/invoke_c339.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'):self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C339',text);self.assertIn('c339_execution.py',(ROOT/'tools/run_c339.ps1').read_text(encoding='utf-8'))
        for mode in ('science','regression','verify'):
            args=e.command(ROOT,ROOT/'runs/x',HEAD,mode);self.assertEqual(args[-2:],['--mode',mode])


if __name__=='__main__':unittest.main()
