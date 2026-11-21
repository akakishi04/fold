"""C333 tests: real accepted JSON adapters; synthetic scores/proofs are not model results."""
from __future__ import annotations
import ast
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
from fold_lm.v05_benchmarks import model_c333_paired_gate_localization as s
from fold_lm.v05_benchmarks import model_c332_trained_first_mean_query as p
from fold_lm.v05_benchmarks import model_c330_saved_gate_localization as q

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.util.spec_from_file_location('_c333_executor_tests',ROOT/'tools/c333_execution.py')
e = importlib.util.module_from_spec(loader); loader.loader.exec_module(e)
HEAD = 'a'*40


def score(kind='pass'):
    cells,orders = [],[]
    for split,profile,language,entities,perm in q.expected_keys():
        n = 16 if split=='TRAIN' else 8
        failed = split=='HOLDOUT' and profile==q.SCORER_PROFILES[-1] and language=='en' and entities==(0,1) and perm==(0,1)
        normal = failed and kind in ('normal','mixed')
        correct,both = (n-2,n//2-2) if normal else (n,n//2)
        cells.append(dict(split=split,profile=profile,language=language,entities=list(entities),permutation=list(perm),
            rows=n,correct=correct,accuracy=correct/n,query_pair_accuracy=both/(n//2),collapsed_pairs=0,pairs=n//2,
            evidence_drop=.25 if failed and kind in ('mask','mixed') else .5,query_drop=.5,
            answer_nll=.1,passed=not (failed and kind!='pass')))
    for split,profile,language,entities in q.expected_keys(True):
        n = 16 if split=='TRAIN' else 8
        failed = split=='HOLDOUT' and profile==q.SCORER_PROFILES[-1] and language=='en' and entities==(0,1) and kind in ('normal','mixed')
        correct = n-2 if failed else n
        orders.append(dict(split=split,profile=profile,language=language,entities=list(entities),groups=n,
                           both_correct=correct,accuracy=correct/n,passed=correct/n>=.8))
    totals = []
    for split,profile,language in itertools.product(q.SPLITS,q.SCORER_PROFILES,q.LANGUAGES):
        rows = [r for r in cells if (r['split'],r['profile'],r['language'])==(split,profile,language)]
        totals.append(dict(split=split,profile=profile,language=language,
            **{k:sum(r[k] for r in rows) for k in ('rows','correct','pairs','collapsed_pairs')}))
    return dict(cells=cells,two_order=orders,totals=totals,passed=all(r['passed'] for r in cells+orders))


def fixture():
    """Complete hand-specified score cohort, never executed historical training."""
    metrics,flags = [],[]
    for seed,arm in s.identities():
        domains = {d:score() for d in s.DOMAINS}
        if seed==332001:
            domains['original6'] = score('normal' if arm=='native' else 'pass')
            if arm=='first_mean': domains['original5'] = score('mask')
        if seed==332004 and arm=='first_mean':
            domains['original6'] = score('mixed'); domains['interior4'] = score('normal')
        metrics.append(dict(seed=seed,arm=arm,score=dict(original={str(n):domains['original'+str(n)] for n in range(2,7)},interior=domains['interior4'])))
        old = {str(n):domains['original'+str(n)]['passed'] for n in range(2,7)}
        flags.append(dict(seed=seed,arm=arm,original_pass=old,interior_pass=domains['interior4']['passed'],retention_pass=all(old.values()),
            failures={d:dict(local=sum(not r['passed'] for r in v['cells']),order=sum(not r['passed'] for r in v['two_order'])) for d,v in domains.items()}))
    pairs = []
    def count(record,domain):
        v = record['score']['interior'] if domain=='interior4' else record['score']['original'][domain[-1]]
        rows = [r for r in v['cells'] if r['split']=='HOLDOUT']
        return sum(r['correct'] for r in rows),int(sum(r['query_pair_accuracy']*r['pairs'] for r in rows))
    for i,seed in enumerate(s.SEEDS):
        comparisons = {}
        for domain in s.DOMAINS:
            a,b = [count(record,domain) for record in metrics[2*i:2*i+2]]; gain,pairgain = b[0]-a[0],b[1]-a[1]
            comparisons[domain] = dict(answers=288,query_pairs=144,control_correct=a[0],candidate_correct=b[0],
                control_both_correct=a[1],candidate_both_correct=b[1],answer_gain=gain,query_pair_gain=pairgain,
                rescued=max(gain,0),regressed=max(-gain,0),pair_rescued=max(pairgain,0),pair_regressed=max(-pairgain,0))
        old = {str(n):comparisons['original'+str(n)] for n in range(2,7)}; inside = comparisons['interior4']
        pairs.append(dict(seed=seed,control_full_pass=flags[2*i]['retention_pass'] and flags[2*i]['interior_pass'],
            candidate_full_pass=flags[2*i+1]['retention_pass'] and flags[2*i+1]['interior_pass'],
            six_answer_gain=old['6']['answer_gain'],six_pair_gain=old['6']['query_pair_gain'],
            short_answer_gain=sum(old[str(n)]['answer_gain'] for n in range(2,6)),
            short_pair_gain=sum(old[str(n)]['query_pair_gain'] for n in range(2,6)),
            interior_answer_gain=inside['answer_gain'],interior_pair_gain=inside['query_pair_gain'],original_by_length=old,interior=inside))
    gate,eligible = p.fixed_gate(pairs)
    result = dict(candidate_gate=gate,eligible_seed_count=sum(eligible),paired_conditions_valid=True,all_replays=True,
                  seed_results=flags,paired_comparisons=pairs,**p.WORK)
    p.check_summary(result)
    return metrics,result


def parent_fixture():
    _,value = fixture(); pins = {e.P_PATH:e.P_BLOB,**{f'p{i}':'b'*40 for i in range(852)}}
    inputs = {f'i{i}':'c'*64 for i in range(2508)}; parent = NS(spec=lambda:p,PARENT_SUMMARY='d'*64,PARENT_ENVELOPE='e'*64)
    r = dict(schema='fold-c332-science-v1',commit_sha=e.PARENT_HEAD,experiment_id=p.EXPERIMENT_ID,stage=p.STAGE,status='FAIL',
        diagnostic_execution_valid=True,capability_gate_applicable=True,gate_f_candidate=False,production_adoption=False,
        manifest_sha256=p.MANIFEST_SHA,source_blobs=dict(pins),input_sha256=dict(inputs),validation_summary=value)
    v = dict(schema='fold-c332-execution-envelope-v1',commit_sha=e.PARENT_HEAD,scientific_status='FAIL',scientific_summary_sha256=e.PARENT_SUMMARY,
        manifest_sha256=p.MANIFEST_SHA,scientific_work=p.WORK,source_count=853,input_count=2508,source_blobs=pins,input_sha256=inputs,
        parent_summary_sha256=parent.PARENT_SUMMARY,parent_envelope_sha256=parent.PARENT_ENVELOPE,immediate_parent_semantic_reconstruction=True,
        parent_regression_reconstructed=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,final_reference_rechecks=2508,
        hash_stats={'final_reference_rechecks':2508},regression=e.receipt(e.PARENT_HEAD,5946))
    return r,v,parent


def fake_recovery():
    """Explicit module-validator collaborator, not an accepted historical run."""
    def flatten(values):
        for v in values:
            if isinstance(v,unittest.TestSuite): yield from flatten(v)
            else: yield v
    def validate(row,g,head,i,ph,launcher,log):
        e.require(row['schema']=='fold-c330-r1-module-v2' and row['commit_sha']==head and row['index']==i
                  and row['plan_sha256']==ph and row['module']==g['module'],'module ABI')
        e.require(row['result']['success_ids']==g['test_ids'],'test success IDs')
        e.require(launcher in (row['pid'],row['parent_pid']),'PID relation')
        return 'direct' if launcher==row['pid'] else 'redirected-child'
    return NS(flatten=flatten,EXCLUDED='excluded',validate_module_evidence=Mock(side_effect=validate),
        allowed_module=lambda name:type(name) is str and (re.fullmatch(r'tests_lm\.[A-Za-z0-9_]+',name) is not None or name=='tests_tools.test_c324_locked_hash_r4'))


def fake_plan():
    groups = []; n,rem = divmod(5946,222)
    for i in range(222):
        name = 'tests_tools.test_c324_locked_hash_r4' if i==0 else f'tests_lm.fixture_{i:03d}'
        groups.append(dict(module=name,test_ids=[name+f'.Fixture.test_{j:03d}' for j in range(n+(i<rem))]))
    groups.append(dict(module=e.TEST_MODULE,test_ids=[e.TEST_MODULE+f'.C333Tests.test_{i:02d}' for i in range(32)]))
    ids = [t for g in groups for t in g['test_ids']]
    return dict(schema='fold-c333-regression-plan-v1',commit_sha=HEAD,manifest_sha256=s.MANIFEST_SHA,
                test_ids_sha256=s.digest(ids),groups=groups),s.digest(ids[:-32])


def fake_module(folder,plan,i,ph):
    g = plan['groups'][i]; pid,parent = 20000+i,10000+i
    e.save(folder/f'module-{i:03d}.json',dict(schema='fold-c330-r1-module-v2',commit_sha=HEAD,index=i,plan_sha256=ph,
        module=g['module'],pid=pid,parent_pid=parent,result=dict(tests=len(g['test_ids']),success_ids=g['test_ids'])))
    (folder/f'module-{i:03d}.log').write_text('synthetic collaborator proof',encoding='utf-8')
    return pid if i%2==0 else parent


def proof_files(folder):
    modules = []
    for i in range(222):
        (folder/f'module-{i:03d}.json').write_bytes(b'{}'); (folder/f'module-{i:03d}.log').write_bytes(b'fixture')
        modules.append(dict(index=i,receipt_sha256=e.sha(folder/f'module-{i:03d}.json'),log_sha256=e.sha(folder/f'module-{i:03d}.log')))
    e.save(folder/'regression-plan.json',{}); e.save(folder/'regression-result.json',{}); e.save(folder/'regression-evidence.json',{'modules':modules})
    return dict(tests=5946,modules=222,plan_sha256=e.sha(folder/'regression-plan.json'),
                result_sha256=e.sha(folder/'regression-result.json'),evidence_sha256=e.sha(folder/'regression-evidence.json'))


class C333Tests(unittest.TestCase):
    def test_01_seal_and_zero_neural_work(self):
        s.validate_seal(); self.assertEqual(s.WORK['model_forward_calls'],0); self.assertEqual(s.WORK['train_steps'],0)
        with patch.object(s,'ARMS',('first_mean','native')),self.assertRaises(ValueError): s.validate_seal()
    def test_02_actual_loader_and_additive_counts(self):
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(e.TEST_MODULE).countTestCases(),32)
        self.assertEqual(s.FULL_TESTS,5946+32); self.assertEqual(s.SOURCE_COUNT,853+6); self.assertEqual(s.INPUT_COUNT,2508+455+6)
    def test_03_complete_real_adapter_analysis(self):
        local,changes,value = s.analyze(*fixture())
        self.assertEqual(len(local['cells']),4320); self.assertEqual(len(local['two_order']),2160)
        self.assertEqual(len(changes['local']),2160); self.assertEqual(len(changes['two_order']),1080)
        self.assertFalse(value['parent_validation_summary']['candidate_gate']); self.assertEqual(len(value['strata']),144)
    def test_04_input_immutable_and_deterministic(self):
        inputs = fixture(); before = s.digest(inputs); a = s.analyze(*inputs); b = s.analyze(*inputs)
        self.assertEqual(s.blob(a),s.blob(b)); self.assertEqual(s.digest(inputs),before)
    def test_05_coordinate_reordering_does_not_change_result(self):
        metrics,value = fixture(); expected = s.analyze(metrics,value)
        for record in metrics:
            for score_value in [record['score']['interior'],*record['score']['original'].values()]:
                score_value['cells'].reverse(); score_value['two_order'].reverse()
        self.assertEqual(s.blob(s.analyze(metrics,value)),s.blob(expected))
    def test_06_wrong_seed_order_and_missing_cohort_rejected(self):
        for kind in ('reverse','drop'):
            metrics,v = fixture()
            if kind=='reverse': metrics.reverse()
            else: metrics.pop()
            with self.subTest(),self.assertRaises(ValueError): s.analyze(metrics,v)
    def test_07_C329_flat_wrapper_is_not_C332_score_wrapper(self):
        metrics,v = fixture(); record = metrics[0]; record.update(record.pop('score'))
        with self.assertRaisesRegex(ValueError,'measurements record'): s.analyze(metrics,v)
    def test_08_missing_domain_rejected(self):
        metrics,v = fixture(); del metrics[0]['score']['original']['6']
        with self.assertRaises(ValueError): s.analyze(metrics,v)
    def test_09_duplicate_coordinate_rejected(self):
        metrics,v = fixture(); rows = metrics[0]['score']['original']['2']['cells']; rows[1] = copy.deepcopy(rows[0])
        with self.assertRaises(ValueError): s.analyze(metrics,v)
    def test_10_false_saved_pass_and_totals_rejected(self):
        for field in ('passed','totals'):
            metrics,v = fixture(); z = metrics[0]['score']['original']['6']
            if field=='passed': z['passed'] = True
            else: z['totals'][0]['correct'] -= 1
            with self.subTest(),self.assertRaises(ValueError): s.analyze(metrics,v)
    def test_11_real_mask_and_binding_classification(self):
        for kind,pattern in (('pass','pass'),('normal','normal_binding_only'),('mask','mask_only'),('mixed','mixed')):
            cells,_,_ = q.adapted_score(score(kind),'interior4')
            selected = [r for r in cells if r['pattern']!='pass']
            self.assertEqual(len(selected),0 if kind=='pass' else 1)
            if selected:
                self.assertEqual(selected[0]['pattern'],pattern); self.assertEqual(selected[0]['input_profile'],'v_dominant')
    def test_12_matched_rescue_and_regression_not_swapped(self):
        _,changes,v = s.analyze(*fixture())
        def row(domain,criterion): return next(r for r in v['transition_summary'] if (r['domain'],r['criterion'])==(domain,criterion))
        self.assertEqual(row('original6','accuracy')['rescued'],1); self.assertEqual(row('original6','accuracy')['regressed'],1)
        self.assertEqual(row('original5','evidence_drop')['regressed'],1); self.assertEqual(row('interior4','accuracy')['regressed'],1)
        r = next(r for r in changes['local'] if r['rescued'])
        self.assertEqual(r['seed'],332001); self.assertEqual(r['input_profile'],'shared_suffix')
    def test_13_cross_coordinate_transition_rejected(self):
        a,b = q.adapted_score(score('normal'),'original6')[0][:2]
        with self.assertRaises(ValueError): q.transition(a,b)
    def test_14_parent_failure_counts_cannot_be_dropped(self):
        metrics,v = fixture(); v['seed_results'][0]['failures']['original6']['local'] += 1
        with self.assertRaisesRegex(ValueError,'parent flags'): s.analyze(metrics,v)
    def test_15_parent_HOLDOUT_counts_reconciled(self):
        metrics,v = fixture(); z = v['paired_comparisons'][0]['original_by_length']['6']
        z['control_correct'] -= 1; z['candidate_correct'] -= 1
        p.check_summary(v)
        with self.assertRaisesRegex(ValueError,'HOLDOUT counts'): s.analyze(metrics,v)
    def test_16_transition_and_stratum_semantic_tamper(self):
        _,_,value = s.analyze(*fixture())
        for field in ('transition','stratum'):
            v = copy.deepcopy(value)
            if field=='transition': v['transition_summary'][0]['rescued'] += 1
            else: v['strata'][0]['patterns']['mask_only'] += 1
            with self.subTest(),self.assertRaises(ValueError): s.check_summary(v)
    def test_17_real_production_writer_reconstruction_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); parent = root/'parent'; out = root/'out'; parent.mkdir(); out.mkdir()
            metrics,value = fixture(); e.save(parent/'measurements.json',metrics); e.save(parent/'validation-summary.json',value)
            result = s.run_diagnostic(out,parent,e.read); self.assertTrue(result['diagnostic_complete'])
            self.assertEqual(s.blob(s.semantic_recheck(out,parent,e.read)),s.blob(result))
            self.assertEqual(set(p.name for p in out.iterdir()),set(s.OUTPUTS))
            with self.assertRaises(FileExistsError): s.run_diagnostic(out,parent,e.read)
    def test_18_resealed_output_hash_does_not_bypass_semantics(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); parent = root/'parent'; out = root/'out'; parent.mkdir(); out.mkdir()
            metrics,value = fixture(); e.save(parent/'measurements.json',metrics); e.save(parent/'validation-summary.json',value)
            s.run_diagnostic(out,parent,e.read); path = out/'transitions.json'; v = e.read(path)
            v['local'][0]['regressed'] = ['accuracy']; path.write_bytes(s.blob(v)); self.assertEqual(len(e.sha(path)),64)
            with self.assertRaisesRegex(ValueError,'reconstruction'): s.semantic_recheck(out,parent,e.read)
    def test_19_parent_primary_gate_not_promoted(self):
        metrics,v = fixture(); v['candidate_gate'] = True
        with self.assertRaises(ValueError): s.analyze(metrics,v)
    def test_20_parent_contract_accepts_negative_not_old_diagnostic(self):
        e.parent_contract(*parent_fixture())
        for target,key,value in ((0,'status','PASS'),(0,'schema','fold-c331-diagnostic-v1'),(0,'capability_gate_applicable',False),
                                 (1,'source_count',847),(1,'input_count',2051),(1,'final_reference_rechecks',2507)):
            args = parent_fixture(); args[target][key] = value
            with self.subTest(key=key),self.assertRaises(ValueError): e.parent_contract(*args)
    def test_21_all447proofs_and_nested_snapshot_full_union(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); pins,inputs,tree = {},{},{}
            for i in range(853):
                name = f'ancestor/source_{i}.py'; path = root/name; path.parent.mkdir(parents=True,exist_ok=True); raw = f'# fixture{i}\n'.encode(); path.write_bytes(raw)
                pins[name] = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(); tree[name] = pins[name]; inputs[e.canonical(path)] = e.sha(path)
            inputs.update({f'synthetic-parent-input-{i}':'a'*64 for i in range(2508-853)})
            for name in s.OWN:
                path = root/name; path.parent.mkdir(parents=True,exist_ok=True); raw = name.encode(); path.write_bytes(raw)
                tree[name] = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            folder = root/e.PARENT_FOLDER; out = folder/'science'; out.mkdir(parents=True)
            for name in p.OUTPUTS: (out/name).write_bytes(b'parent fixture')
            proofs = proof_files(folder); e.save(out/'summary.json',{'artifacts':[]})
            e.save(folder/'execution-envelope.json',dict(source_blobs=pins,input_sha256=inputs,regression_isolation=proofs))
            legacy = NS(tree_blobs=lambda root:tree,descriptors=lambda out,records,names,h:{e.canonical(out/n):h(out/n) for n in names})
            recovery = object(); ph = (object(),(recovery,None,None,legacy,None))
            parent = NS(spec=lambda:p,snapshot=Mock(return_value=({}, {},pins,inputs)),build_plan=Mock(return_value={'fixture':True}),verify_tests=Mock(return_value=proofs))
            with patch.object(e,'PARENT_SUMMARY',e.sha(out/'summary.json')),patch.object(e,'PARENT_ENVELOPE',e.sha(folder/'execution-envelope.json')),patch.object(e,'parent_contract'):
                self.assertEqual(len(e.parent_test_files(folder,{'regression_isolation':proofs},e.sha)),447)
                _,_,a,b = e.snapshot(root,(parent,ph),e.sha); self.assertEqual((len(a),len(b)),(859,2969))
                parent.snapshot.assert_called_once_with(root,ph,e.sha)
                self.assertEqual(parent.verify_tests.call_args.args,(folder,e.PARENT_HEAD,{'fixture':True},recovery))
                (folder/'module-221.log').write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError,'parent module bytes'): e.snapshot(root,(parent,ph),e.sha)
    def test_22_exact_immediate_parent_semantic_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp); source = root/'c329/science'; source.mkdir(parents=True)
            for name in ('dataset.json','original-prompts.json','interior-prompts.json'): (source/name).write_bytes(b'{}')
            inputs = {e.canonical(path):e.sha(path) for path in source.iterdir()}; cx = (NS(guarded=NS(no_neural=contextlib.nullcontext)),)
            ps = NS(source=lambda:NS(base=lambda:NS(context=lambda:cx)),semantic_recheck=Mock(return_value={'negative':True}))
            parent = NS(spec=lambda:ps); ph = (object(),(None,NS(PARENT_FOLDER='c329'),None,None,None))
            self.assertEqual(e.parent_semantics(root,(parent,ph),{'validation_summary':{'negative':True}},inputs),cx)
            self.assertEqual(ps.semantic_recheck.call_args.args,(root/e.PARENT_FOLDER/'science',source,cx,e.read))
    def test_23_plan_uses_nested_parent_and_real_loader(self):
        plan,digest = fake_plan(); r = fake_recovery(); ph = (object(),(r,None,None,None,None))
        parent = NS(build_plan=Mock(return_value={'groups':plan['groups'][:-1]}))
        with patch.object(e,'BASE_IDS_SHA',digest):
            actual = e.build_plan(ROOT,HEAD,(parent,ph)); self.assertEqual(len(actual['groups']),223)
            self.assertEqual(len(actual['groups'][-1]['test_ids']),32); parent.build_plan.assert_called_once_with(ROOT,HEAD,ph)
    def test_24_test_plan_drop_duplicate_reorder_and_unknown_rejected(self):
        plan,digest = fake_plan(); r = fake_recovery()
        with patch.object(e,'BASE_IDS_SHA',digest):
            for kind in ('drop','duplicate','reverse','module'):
                v = copy.deepcopy(plan)
                if kind=='drop': v['groups'].pop()
                elif kind=='duplicate': v['groups'][0]['test_ids'][1] = v['groups'][0]['test_ids'][0]
                elif kind=='reverse': v['groups'][0]['test_ids'].reverse()
                else: v['groups'][0]['module'] = 'unsafe.module'
                with self.subTest(),self.assertRaises(ValueError): e.validate_plan(v,HEAD,r)
    def test_25_collector_and_verifier_delegate_same_PID_ABI(self):
        plan,digest = fake_plan(); r = fake_recovery()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            folder = Path(tmp); e.collect_tests(folder,HEAD,plan,r,lambda i,h:fake_module(folder,plan,i,h))
            self.assertEqual(e.verify_tests(folder,HEAD,plan,r)['tests'],5978); self.assertEqual(r.validate_module_evidence.call_count,446)
            (folder/'module-222.log').write_bytes(b'tampered')
            with self.assertRaisesRegex(ValueError,'proof bytes'): e.verify_tests(folder,HEAD,plan,r)
    def test_26_failure_stops_tests_and_diagnosis_without_retry(self):
        plan,digest = fake_plan(); r = fake_recovery(); runner = Mock(side_effect=ValueError('fixture failure')); diagnose = Mock()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),contextlib.redirect_stdout(io.StringIO()):
            folder = Path(tmp)
            with self.assertRaises(ValueError): e.collect_tests(folder,HEAD,plan,r,runner)
            self.assertEqual(runner.call_count,1); self.assertFalse((folder/'regression-result.json').exists())
            with self.assertRaises(ValueError): e.execute_stages(runner,diagnose,Mock(),Mock())
            diagnose.assert_not_called()
    def test_27_module_CLI_calls_accepted_runner_under_child_guard(self):
        plan,digest = fake_plan(); r = fake_recovery(); r.execute_module = Mock(return_value={'tests':len(plan['groups'][0]['test_ids'])}); r.check_module = Mock()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',digest),patch.object(e,'helpers',return_value=(None,(None,(r,None,None,None,None)))),patch.object(e,'guard'),contextlib.redirect_stdout(io.StringIO()):
            folder = Path(tmp); e.save(folder/'regression-plan.json',plan); e.module_child(folder,folder,HEAD,0,e.sha(folder/'regression-plan.json'))
            r.execute_module.assert_called_once_with(plan['groups'][0]['module'],plan['groups'][0]['test_ids'])
            self.assertEqual(e.read(folder/'module-000.json')['parent_pid'],e.os.getppid())
    def test_28_real_git_JSON_and_source_byte_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); subprocess.run(['git','init','-q',str(root)],check=True)
            for args in [('checkout','-qb',e.BRANCH),('config','user.name','C333 fixture'),('config','user.email','c333@example.invalid')]: subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
            (root/'docs').mkdir(); h = root/'docs/experiment-ledger-and-handoff.md'; h.write_text('## Formal state\nC333 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
            subprocess.run(['git','-C',str(root),'add','.'],check=True); subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
            head = e.git(root,'rev-parse','HEAD'); e.guard(root,head)
            with self.assertRaises(ValueError): e.guard(root,HEAD)
            h.write_bytes(b'changed')
            with self.assertRaises(ValueError): e.guard(root,head)
            file = root/'x'; e.save(file,{'名前':'甲乙'}); self.assertEqual(e.read(file),{'名前':'甲乙'})
            with self.assertRaises(FileExistsError): e.save(file,{})
            for text in ('{"a":1,"a":2}','NaN','Infinity'):
                file.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError): e.read(file)
            raw = b'a\nb\n'; oid = hashlib.sha1(b'blob 4\0'+raw).hexdigest()
            for value in (raw,raw.replace(b'\n',b'\r\n')): file.write_bytes(value); e.source_bytes(file,oid)
            file.write_bytes(b'changed')
            with self.assertRaises(ValueError): e.source_bytes(file,oid)
    def test_29_actual_nonzero_process_and_controller_no_retry(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp); log = root/'error.log'
            with self.assertRaises(ValueError): e.run_logged(root,[sys.executable,'-c','print("fixture");raise SystemExit(7)'],log,'fixture')
            self.assertIn('fixture',log.read_text(encoding='utf-8'))
            with patch.object(e,'guard'),patch.object(e,'run_logged',side_effect=ValueError('fixture')) as runner:
                with self.assertRaises(ValueError): e.run(root,root/'runs/x',HEAD)
                self.assertEqual(runner.call_count,1)
    def test_30_production_worker_real_JSON_diagnosis_with_synthetic_infrastructure(self): self.worker_fixture(False)
    def test_31_fresh_verifier_and_invalid_regression_stop(self): self.worker_fixture(True)
    def worker_fixture(self,bad):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp); folder = root/'runs/child'; folder.mkdir(parents=True); parent_out = root/e.PARENT_FOLDER/'science'; parent_out.mkdir(parents=True)
            metrics,value = fixture(); e.save(parent_out/'measurements.json',metrics); e.save(parent_out/'validation-summary.json',value)
            calls = []; pins = {f'p{i}':'a'*40 for i in range(859)}; inputs = {f'i{i}':'b'*64 for i in range(2969)}
            class Cache:
                entries={}; stats={'final_reference_rechecks':2969}; sha=staticmethod(e.sha)
                def __init__(self,*a,**k): pass
                def __enter__(self): return self
                def __exit__(self,*a): calls.append('release')
                def recheck(self): calls.append('final'); return [{'path':k,'sha256':v} for k,v in inputs.items()]
            locks = NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None)
            runtime = NS(native_runtime=lambda:(NS(__version__='synthetic'),NS(__version__='synthetic')))
            legacy = NS(descriptors=lambda out,items,names,h:e.require(items==e.artifacts(out),'fixture artifact identity'))
            ph = (None,(None,None,runtime,legacy,locks)); parent = NS(spec=lambda:NS(source=lambda:NS(base=lambda:NS(peak_rss=lambda:1))))
            cx = (NS(guarded=NS(no_neural=contextlib.nullcontext)),)
            def snapshot(*a): calls.append('snapshot'); return {'validation_summary':value},{},pins,inputs
            def semantics(*a): calls.append('parent'); return cx
            def regression(*a):
                calls.append('tests')
                if bad: raise ValueError('synthetic regression failure')
                e.save(folder/'regression-result.json',e.receipt(HEAD,5978))
            with patch.object(e,'guard'),patch.object(e,'helpers',return_value=(parent,ph)),patch.object(e,'snapshot',side_effect=snapshot),patch.object(e,'parent_semantics',side_effect=semantics),patch.object(e,'run_logged',side_effect=regression),patch.object(e,'build_plan',return_value={}),patch.object(e,'verify_tests',return_value={'tests':5978,'modules':223}):
                if bad:
                    with self.assertRaises(ValueError): e.scientific_worker(root,folder,HEAD)
                    self.assertFalse((folder/'science/summary.json').exists()); self.assertEqual(calls,['snapshot','parent','tests','release'])
                else:
                    e.scientific_worker(root,folder,HEAD); self.assertEqual(calls,['snapshot','parent','tests','final','release'])
                    primary = e.read(folder/'science/summary.json'); self.assertEqual(primary['status'],'PASS')
                    self.assertFalse(primary['capability_gate_applicable']); self.assertFalse(primary['validation_summary']['parent_validation_summary']['candidate_gate'])
                    e.verify_outputs(root,folder,HEAD)
                    primary['capability_gate_applicable'] = True; (folder/'science/summary.json').write_bytes(s.blob(primary))
                    with self.assertRaisesRegex(ValueError,'diagnostic flags'): e.verify_outputs(root,folder,HEAD)
    def test_32_launcher_CLI_and_no_neural_scientific_imports(self):
        text = (ROOT/'tools/invoke_c333.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','ParseFile'): self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C333',text); self.assertIn('c333_execution.py',(ROOT/'tools/run_c333.ps1').read_text(encoding='utf-8'))
        tree = ast.parse(Path(s.__file__).read_text(encoding='utf-8'))
        imports = [a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names]
        self.assertNotIn('torch',imports); self.assertNotIn('numpy',imports)
        run = subprocess.run([sys.executable,str(ROOT/'tools/c333_execution.py'),'--folder','unused','--expected-head',HEAD,'--mode','invalid'],capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(run.returncode,0); self.assertIn('invalid choice',run.stderr)


if __name__=='__main__': unittest.main()
