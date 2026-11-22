"""C346 execution software checks; synthetic evidence is never a scientific result."""
from __future__ import annotations
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch
from fold_lm.v05_benchmarks import model_c346_pair_max_rate as s

ROOT = Path(__file__).resolve().parents[1]
HEAD = 'a'*40


def module_at(name, path):
    loader = importlib.util.spec_from_file_location(name, ROOT/path)
    value = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(value)
    return value


e = module_at('_c346_executor_tests', 'tools/c346_execution.py')
recovery = module_at('_c346_accepted_recovery', 'tools/c330_recovery_r1.py')
accepted = module_at('_c346_accepted_timeout', 'tools/c344_execution.py')


def plan_fixture():
    """Synthetic ancestor IDs plus the actual two new module inventories."""
    groups = []
    q, r = divmod(6578, 241)
    for i in range(241):
        name = f'tests_lm.synthetic_{i:03d}'
        groups.append(dict(module=name, test_ids=[name+f'.Cases.test_{j:03d}' for j in range(q+(i < r))]))
    base_hash = s.digest([v for g in groups for v in g['test_ids']])
    for name in e.TEST_MODULES:
        own = list(recovery.flatten(unittest.defaultTestLoader.loadTestsFromName(name)))
        e.require(own and all(type(t).__module__ == name for t in own), 'real own module loader')
        groups.append(dict(module=name, test_ids=[t.id() for t in own]))
    ids = [v for g in groups for v in g['test_ids']]
    return dict(schema='fold-c346-regression-plan-v1', commit_sha=HEAD, manifest_sha256=s.MANIFEST_SHA,
                test_ids_sha256=s.digest(ids), groups=groups), base_hash


def successful(group):
    return dict(tests=len(group['test_ids']), failures=0, errors=0, skipped=0, expected_failures=0,
                unexpected_successes=0, successful=True, started_ids=group['test_ids'], success_ids=group['test_ids'])


def proof(folder, plan, index, plan_sha):
    group = plan['groups'][index]
    pid, parent_pid = 20000+index, 10000+index
    row = dict(schema='fold-c330-r1-module-v2', commit_sha=HEAD, plan_sha256=plan_sha, index=index,
               module=group['module'], pid=pid, parent_pid=parent_pid, result=successful(group))
    e.save(folder/f'module-{index:03d}.json', row)
    marker = dict(index=index, module=group['module'], tests=len(group['test_ids']), pid=pid, parent_pid=parent_pid)
    text = 'Explicit synthetic process evidence; no tests executed by this fixture.\n'
    for name in ('regression_module_begin', 'regression_module_complete'):
        text += name+' = '+json.dumps(marker,sort_keys=True,ensure_ascii=True,allow_nan=False)+'\n'
    (folder/f'module-{index:03d}.log').write_text(text, encoding='utf-8')
    return pid if index%2 == 0 else parent_pid


def parent_fixture():
    ps = NS(validate_seal=Mock(), check_summary=Mock(), EXPERIMENT_ID='synthetic-parent', STAGE='synthetic-stage',
            MANIFEST_SHA='synthetic-manifest', WORK={})
    parent = NS(spec=lambda:ps, PARENT_SUMMARY='old-summary', PARENT_ENVELOPE='old-envelope', EXECUTION_REVISION='C345-R0')
    pins = {e.P_PATH:e.P_BLOB, e.S_PATH:e.S_BLOB, **{f'p{i}':'a' for i in range(935)}}
    inputs = {f'i{i}':'b' for i in range(8679)}
    r = dict(schema='fold-c345-diagnostic-v1', commit_sha=e.PARENT_HEAD, experiment_id=ps.EXPERIMENT_ID,
        stage=ps.STAGE, status='PASS', diagnostic_execution_valid=True, capability_gate_applicable=False,
        gate_f_candidate=False, production_adoption=False, manifest_sha256=ps.MANIFEST_SHA,
        source_blobs=pins, input_sha256=inputs, validation_summary=dict(diagnostic_complete=True,
            parent_validation_summary=dict(candidate_gate=False,eligible_seed_count=2)))
    v = dict(schema='fold-c345-execution-envelope-v1', commit_sha=e.PARENT_HEAD, scientific_status='PASS',
        scientific_summary_sha256=e.PARENT_SUMMARY, manifest_sha256=ps.MANIFEST_SHA, scientific_work={},
        source_count=937, input_count=8679, source_blobs=pins, input_sha256=inputs, parent_summary_sha256=parent.PARENT_SUMMARY,
        parent_envelope_sha256=parent.PARENT_ENVELOPE, immediate_parent_semantic_reconstruction=True,
        parent_regression_reconstructed=True, ancestor_semantic_reruns=0, saved_semantic_reconstruction=True,
        final_reference_rechecks=8679, hash_stats={'final_reference_rechecks':8679}, regression=e.receipt(e.PARENT_HEAD,6578),
        execution_revision='C345-R0',timeout_cleanup_implementation='C344-R1',
        timeout_cleanup_preflight=accepted.timeout_preflight_expected(e.PARENT_HEAD))
    return r,v,parent,accepted


class C346ExecutionTests(unittest.TestCase):
    def test_01_parent_diagnostic_contract_preserves_negative_capability(self):
        r,v,parent,cleanup = parent_fixture(); e.parent_contract(r,v,parent,cleanup)
        parent.spec().check_summary.assert_called_once_with(r['validation_summary'])
        for target,key,value in ((0,'status','FAIL'),(0,'capability_gate_applicable',True),
                                 (0,'diagnostic_execution_valid',False),(1,'source_count',936),
                                 (1,'input_count',8678),(1,'final_reference_rechecks',8678),
                                 (1,'ancestor_semantic_reruns',1),(1,'scientific_work',{'steps':1}),
                                 (1,'execution_revision','C344-R1'),(1,'timeout_cleanup_implementation','C345-R0')):
            with self.subTest(key=key):
                args=parent_fixture();args[target][key]=value
                with self.assertRaises(ValueError):e.parent_contract(*args)
        for key,value in (('candidate_gate',True),('eligible_seed_count',0)):
            args=parent_fixture();args[0]['validation_summary']['parent_validation_summary'][key]=value
            with self.assertRaises(ValueError):e.parent_contract(*args)
        args=parent_fixture();args[0]['validation_summary']['diagnostic_complete']=False
        with self.assertRaises(ValueError):e.parent_contract(*args)
        for key,value in (('cleanup_barriers',5),('commit_sha',HEAD)):
            args=parent_fixture();args[1]['timeout_cleanup_preflight'][key]=value
            with self.assertRaises(ValueError):e.parent_contract(*args)

    def test_02_all_parent_regression_proofs_are_retained(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);items=[]
            for i in range(241):
                a=folder/f'module-{i:03d}.json';b=folder/f'module-{i:03d}.log'
                a.write_bytes(b'{}');b.write_bytes(b'explicit synthetic receipt')
                items.append(dict(index=i,receipt_sha256=e.sha(a),log_sha256=e.sha(b)))
            for name,value in (('regression-plan.json',{}),('regression-result.json',{}),('regression-evidence.json',{'modules':items})):
                e.save(folder/name,value)
            bound=dict(tests=6578,modules=241,plan_sha256=e.sha(folder/'regression-plan.json'),
                       evidence_sha256=e.sha(folder/'regression-evidence.json'),result_sha256=e.sha(folder/'regression-result.json'))
            self.assertEqual(len(e.parent_test_files(folder,{'regression_isolation':bound},e.sha)),485)
            (folder/'module-240.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.parent_test_files(folder,{'regression_isolation':bound},e.sha)

    def test_03_snapshot_rebuilds_exact_source_and_input_union(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);out=root/e.PARENT_FOLDER/'science';out.mkdir(parents=True);pins={};inputs={};tree={}
            for i in range(8679):
                name=f'old/{i}.py' if i<937 else f'data/{i}.bin';path=root/name;path.parent.mkdir(exist_ok=True)
                raw=str(i).encode();path.write_bytes(raw);inputs[e.canonical(path)]=e.sha(path)
                if i<937:pins[name]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();tree[name]=pins[name]
            for name in s.OWN:
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);raw=name.encode();path.write_bytes(raw)
                tree[name]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            names=('audit-plan.json','terminal-objectives.json','training-trajectory.json','validation-summary.json')
            for name in names:(out/name).write_bytes(b'fixture')
            proofs={}
            for i in range(485):
                path=out.parent/f'proof-{i}';path.write_bytes(b'fixture');proofs[e.canonical(path)]=e.sha(path)
            e.save(out/'summary.json',{'artifacts':[]})
            e.save(out.parent/'execution-envelope.json',dict(source_blobs=pins,input_sha256=inputs,regression_isolation={}))
            def ancestor(root,prior,hash_file):
                for name,wanted in inputs.items():self.assertEqual(hash_file(name),wanted)
                return {},{},pins,inputs
            h=dict(parent=NS(spec=lambda:NS(OUTPUTS=names),snapshot=ancestor,build_plan=lambda *a:{},verify_tests=lambda *a:{}),
                   prior={},cleanup=accepted,recovery=None,legacy=NS(tree_blobs=lambda root:tree,
                   descriptors=lambda out,items,names,hash_file:{e.canonical(out/n):hash_file(out/n) for n in names}))
            with patch.object(e,'PARENT_SUMMARY',e.sha(out/'summary.json')),patch.object(e,'PARENT_ENVELOPE',e.sha(out.parent/'execution-envelope.json')), \
                 patch.object(e,'parent_contract'),patch.object(e,'parent_test_files',return_value=proofs):
                _,_,p,v=e.snapshot(root,h,e.sha)
                self.assertEqual((len(p),len(v)),(944,9177));self.assertEqual(len(inputs),8679)
                tree['old/0.py']='bad'
                with self.assertRaises(ValueError):e.snapshot(root,h,e.sha)

    def test_04_parent_dispatch_uses_exact_five_argument_diagnostic_contract(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);source=root/e.PARENT_FOLDER/'science';trained_out=root/'c344/science';data=root/'c329/science'
            names=('audit-plan.json','terminal-objectives.json','training-trajectory.json','validation-summary.json')
            trained_names=('experiment-plan.json','training-traces.json','trained-models.pt','evaluations.pt','measurements.json','validation-summary.json')
            for folder,ns in ((source,names),(trained_out,trained_names),(data,('dataset.json','original-prompts.json','interior-prompts.json'))):
                folder.mkdir(parents=True)
                for name in ns:(folder/name).write_bytes(b'{}')
            inputs={e.canonical(p):e.sha(p) for folder in (source,trained_out,data) for p in folder.iterdir()}
            saved={'synthetic':'diagnostic-parent'};inside=[];calls=[]
            @contextlib.contextmanager
            def no_neural():
                inside.append(True)
                try:yield
                finally:inside.pop()
            x=NS(guarded=NS(no_neural=no_neural),c=NS(p267=NS(validate_data=Mock())))
            cx=(None,None,NS(new_prompts=lambda v:{},check_prompts=Mock()),None,None,x)
            def diagnostic_recheck(actual_source,actual_trained,actual_data,actual_context,reader):
                self.assertTrue(inside)
                self.assertEqual((actual_source,actual_trained,actual_data,actual_context,reader),(source,trained_out,data,cx,e.read))
                calls.append('C345');return saved
            base=NS(context=lambda:cx,digest=s.digest,DATA_SHA=s.digest({}),PROMPTS_SHA=s.digest({}))
            previous=NS(source=lambda:NS(base=lambda:base),load_data=lambda *a:({}, {}, {}),semantic_recheck=Mock())
            trained=NS(OUTPUTS=trained_names,previous=lambda:previous,semantic_recheck=Mock())
            ps=NS(OUTPUTS=names,parent=lambda:trained,semantic_recheck=diagnostic_recheck)
            h=dict(parent=NS(spec=lambda:ps,PARENT_FOLDER='c344'),c330=NS(PARENT_FOLDER='c329'))
            self.assertEqual(e.parent_semantics(root,h,{'validation_summary':saved},inputs),(data,cx))
            self.assertEqual(calls,['C345']);self.assertFalse(inside)
            trained.semantic_recheck.assert_not_called();previous.semantic_recheck.assert_not_called()
            for path in (source/'terminal-objectives.json',source/'training-trajectory.json',trained_out/'trained-models.pt',
                         trained_out/'evaluations.pt',data/'dataset.json'):
                incomplete=dict(inputs);del incomplete[e.canonical(path)]
                with self.assertRaises(ValueError):e.parent_semantics(root,h,{'validation_summary':saved},incomplete)

    def test_05_pinned_parent_bytes_are_checked_before_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in (e.P_PATH,e.S_PATH):p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'fixture')
            prior={k:object() for k in ('parent','prior','recovery','c330','runtime','legacy','locks')};prior['parent']=accepted
            parent=NS(spec=lambda:NS(validate_seal=Mock()),helpers=Mock(return_value=prior))
            with patch.object(e,'git',side_effect=[e.P_BLOB,e.S_BLOB]),patch.object(e,'source_bytes') as check, \
                 patch.object(e.importlib.util,'spec_from_file_location',return_value=NS(loader=NS(exec_module=lambda m:None))), \
                 patch.object(e.importlib.util,'module_from_spec',return_value=parent):
                self.assertIs(e.helpers(root)['prior'],prior);self.assertEqual(check.call_count,2)
            with patch.object(e,'git',return_value='changed'),patch.object(e.importlib.util,'spec_from_file_location') as load:
                with self.assertRaises(ValueError):e.helpers(root)
                load.assert_not_called()

    def test_06_real_own_loaders_and_ordered_plan(self):
        plan,base_hash=plan_fixture()
        h=dict(parent=NS(build_plan=lambda *a:{'groups':plan['groups'][:-2]}),prior={},recovery=recovery)
        with patch.object(e,'BASE_IDS_SHA',base_hash):
            got=e.build_plan(ROOT,HEAD,h);self.assertEqual(got,plan)
            self.assertEqual(len(got['groups']),s.MODULES)
            self.assertEqual(sum(len(g['test_ids']) for g in got['groups'][-2:]),s.OWN_TESTS)
            self.assertEqual(sum(len(g['test_ids']) for g in got['groups']),s.FULL_TESTS)
            for kind in ('missing','duplicate','historical-order','own-order'):
                changed=copy.deepcopy(plan)
                if kind=='missing':changed['groups'].pop()
                elif kind=='duplicate':changed['groups'][0]['test_ids'][1]=changed['groups'][0]['test_ids'][0]
                elif kind=='historical-order':changed['groups'][0]['test_ids'].reverse()
                else:changed['groups'][-2:]=changed['groups'][-2:][::-1]
                with self.assertRaises(ValueError):e.validate_plan(changed,HEAD,recovery)

    def test_07_collector_and_fresh_proof_verifier_use_accepted_pid_markers(self):
        plan,base_hash=plan_fixture()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',base_hash),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp)
            with patch.object(recovery,'validate_module_evidence',wraps=recovery.validate_module_evidence) as check:
                e.collect_tests(folder,HEAD,plan,recovery,lambda i,h:proof(folder,plan,i,h))
                value=e.verify_tests(folder,HEAD,plan,recovery)
                self.assertEqual(check.call_count,2*s.MODULES)
            self.assertEqual((value['tests'],value['modules']),(s.FULL_TESTS,s.MODULES))
            items=e.read(folder/'regression-evidence.json')['modules']
            self.assertEqual({v['relation'] for v in items},{'direct','redirected-child'})
            (folder/'module-242.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.verify_tests(folder,HEAD,plan,recovery)

    def test_08_module_process_dispatch_uses_inherited_timeout_boundary(self):
        plan,base_hash=plan_fixture();group=plan['groups'][0]
        boundary=Mock(wraps=accepted.timeout_monitor_boundary)
        h={'recovery':recovery,'cleanup':NS(timeout_monitor_boundary=boundary),'parent':NS()}
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',base_hash),patch.object(e,'guard'), \
             patch.object(e,'helpers',return_value=h), \
             patch.object(recovery,'execute_module',return_value=successful(group)) as execute,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.save(folder/'regression-plan.json',plan)
            e.module_child(folder,folder,HEAD,0,e.sha(folder/'regression-plan.json'))
            execute.assert_called_once_with(group['module'],group['test_ids'])
            boundary.assert_called_once_with(folder,group['module'])
            row=e.read(folder/'module-000.json');self.assertEqual(row['parent_pid'],e.os.getppid())
            for index in (-1,s.MODULES,True):
                with self.assertRaises(ValueError):e.module_child(folder,folder,HEAD,index,e.sha(folder/'regression-plan.json'))
        # Call ordering is observed through the real module process entry point.
        calls=[]
        @contextlib.contextmanager
        def observed(root,module):
            calls.append(('enter',module))
            try:yield
            finally:calls.append(('exit',module))
        def run(module,ids):
            self.assertEqual(calls,[('enter',module)]);calls.append(('execute',module));return successful(group)
        h['cleanup'].timeout_monitor_boundary=observed
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',base_hash),patch.object(e,'guard'), \
             patch.object(e,'helpers',return_value=h),patch.object(recovery,'execute_module',side_effect=run),contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);e.save(folder/'regression-plan.json',plan)
            e.module_child(folder,folder,HEAD,0,e.sha(folder/'regression-plan.json'))
        self.assertEqual(calls,[('enter',group['module']),('execute',group['module']),('exit',group['module'])])

    def test_09_accepted_receipt_validator_rejects_unrelated_or_fake_completion(self):
        plan,_=plan_fixture();group=plan['groups'][0]
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);launcher=proof(folder,plan,0,'f'*64);row=e.read(folder/'module-000.json');log=folder/'module-000.log'
            recovery.validate_module_evidence(row,group,HEAD,0,'f'*64,launcher,log)
            with self.assertRaises(ValueError):recovery.validate_module_evidence(row,group,HEAD,0,'f'*64,3,log)
            row['result']['success_ids']=row['result']['success_ids'][:-1]
            with self.assertRaises(ValueError):recovery.validate_module_evidence(row,group,HEAD,0,'f'*64,launcher,log)

    def test_10_real_worker_and_fresh_verifier_keep_training_and_saved_checks_separate(self):
        for candidate in (False,True):
            with self.subTest(candidate=candidate),tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
                root=Path(tmp);folder=root/'runs/x';folder.mkdir(parents=True);data=root/'canonical-data'
                pins={f'p{i}':'a' for i in range(s.SOURCE_COUNT)};inputs={f'i{i}':'b' for i in range(s.INPUT_COUNT)};calls=[]
                value=dict(candidate_gate=candidate,eligible_seed_count=5 if candidate else 2)
                prior=dict(parent_validation_summary=dict(candidate_gate=False,eligible_seed_count=2),diagnostic_complete=True)
                class Cache:
                    entries={};stats={'final_reference_rechecks':s.INPUT_COUNT};sha=staticmethod(e.sha)
                    def __init__(self,reference,lease_factory,*,progress,max_files):
                        e.require(type(max_files) is int and max_files==s.INPUT_COUNT==len(inputs),'exact finite capacity')
                        e.require('timeout_cleanup' in calls,'cleanup preflight precedes native locks')
                    def __enter__(self):return self
                    def __exit__(self,*a):calls.append('release')
                    def recheck(self):calls.append('final');return [{'path':k,'sha256':v} for k,v in inputs.items()]
                inside=[]
                @contextlib.contextmanager
                def no_neural():
                    inside.append(True)
                    try:yield
                    finally:inside.pop()
                cx=(NS(guarded=NS(no_neural=no_neural)),)
                previous=NS(source=lambda:NS(base=lambda:NS(check_dependencies=lambda *a:None,peak_rss=lambda:1)))
                parent=NS(spec=lambda:NS(parent=lambda:NS(previous=lambda:previous)),EXECUTION_REVISION='C345-R0')
                def native_runtime():calls.append('runtime');return NS(__version__='fixture'),NS(__version__='fixture')
                h=dict(parent=parent,cleanup=accepted,runtime=NS(native_runtime=native_runtime),
                    locks=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None),
                    legacy=NS(descriptors=lambda out,items,*a:e.require(items==e.artifacts(out),'artifact descriptors')),recovery=None)
                def cleanup(repo,expected_head,actual_helpers):
                    self.assertEqual((repo,expected_head,actual_helpers),(root,HEAD,h))
                    calls.append('timeout_cleanup');return accepted.timeout_preflight_expected(HEAD)
                def snapshot(*args):
                    self.assertIn('timeout_cleanup',calls);calls.append('snapshot')
                    return {'validation_summary':prior},{},pins,inputs
                def preflight(data_out,context,repo,protected,reader):
                    self.assertFalse(inside)
                    self.assertEqual((data_out,context,repo,protected,reader),(data,cx,root,pins,e.read))
                    calls.append('preflight')
                def tests(*a):calls.append('tests');e.save(folder/'regression-result.json',e.receipt(HEAD,s.FULL_TESTS))
                def train(out,data_out,context,repo,protected,reader):
                    self.assertFalse(inside)
                    self.assertEqual((out,data_out,context,repo,protected,reader),(folder/'science',data,cx,root,pins,e.read))
                    calls.append('train')
                    for name in s.OUTPUTS:(out/name).write_bytes(b'explicit synthetic artifact')
                    return value
                def recheck(out,data_out,context,reader):
                    self.assertTrue(inside)
                    self.assertEqual((out,data_out,context,reader),(folder/'science',data,cx,e.read))
                    calls.append('verify');return value
                def report(actual,emitter):
                    self.assertTrue(inside);self.assertEqual((actual,emitter),(value,e.emit));calls.append('report')
                with patch.object(e,'guard'),patch.object(e,'helpers',return_value=h),patch.object(e,'snapshot',side_effect=snapshot), \
                     patch.object(e,'timeout_cleanup_preflight',side_effect=cleanup), \
                     patch.object(e,'parent_semantics',return_value=(data,cx)),patch.object(e,'run_logged',side_effect=tests),patch.object(e,'build_plan',return_value={}), \
                     patch.object(e,'verify_tests',return_value=dict(tests=s.FULL_TESTS,modules=s.MODULES)),patch.object(s,'native_preflight',side_effect=preflight), \
                     patch.object(s,'run_training',side_effect=train),patch.object(s,'semantic_recheck',side_effect=recheck), \
                     patch.object(s,'report_results',side_effect=report),patch.object(s,'check_summary'):
                    e.scientific_worker(root,folder,HEAD);e.verify_outputs(root,folder,HEAD)
                    self.assertEqual(calls,['runtime','timeout_cleanup','snapshot','preflight','tests','train','verify','final','release','report','snapshot','verify'])
                    self.assertFalse(inside)
                    actual=e.read(folder/'science/summary.json')
                    self.assertEqual(actual['status'],'PASS' if candidate else 'FAIL');self.assertTrue(actual['scientific_execution_valid'])
                    self.assertTrue(actual['capability_gate_applicable']);self.assertFalse(actual['gate_f_candidate']);self.assertFalse(actual['production_adoption'])
                    path=folder/'execution-envelope.json';envelope=e.read(path)
                    self.assertEqual(envelope['execution_revision'],'C346-R0')
                    self.assertEqual(envelope['timeout_cleanup_implementation'],'C344-R1')
                    self.assertEqual(envelope['timeout_cleanup_preflight'],accepted.timeout_preflight_expected(HEAD))
                    for key,bad in (('tests',5),('cleanup_barriers',5),('cleanup_ready',False),('platform','other'),
                                    ('commit_sha','b'*40),('source_blobs',{}),('execution_revision','C346-R0')):
                        changed=copy.deepcopy(envelope);changed['timeout_cleanup_preflight'][key]=bad;path.write_bytes(s.blob(changed))
                        with self.assertRaises(ValueError):e.verify_outputs(root,folder,HEAD)
                    for key in ('execution_revision','timeout_cleanup_implementation'):
                        changed=copy.deepcopy(envelope);changed[key]='unreviewed';path.write_bytes(s.blob(changed))
                        with self.assertRaises(ValueError):e.verify_outputs(root,folder,HEAD)
                    for key in ('started_ids','success_ids'):
                        changed=copy.deepcopy(envelope);changed['timeout_cleanup_preflight'][key].pop();path.write_bytes(s.blob(changed))
                        with self.assertRaises(ValueError):e.verify_outputs(root,folder,HEAD)
                    path.write_bytes(s.blob(envelope))
                    actual['capability_gate_applicable']=False;(folder/'science/summary.json').write_bytes(s.blob(actual))
                    with self.assertRaises(ValueError):e.verify_outputs(root,folder,HEAD)

    def test_11_regression_failure_never_enters_training(self):
        train=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
            e.execute_stages(Mock(),Mock(side_effect=ValueError('synthetic regression failure')),train,Mock(),Mock())
        train.assert_not_called()

    def test_12_incomplete_regression_scope_blocks_training(self):
        train=Mock()
        for value in (dict(tests=s.FULL_TESTS-1,modules=s.MODULES),dict(tests=s.FULL_TESTS,modules=s.MODULES-1)):
            with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
                e.execute_stages(Mock(),lambda:value,train,Mock(),Mock())
        train.assert_not_called()
        h=dict(runtime=NS(native_runtime=Mock(return_value=(None,None))),locks=Mock(),recovery=None)
        with patch.object(e,'guard'),patch.object(e,'helpers',return_value=h), \
             patch.object(e,'timeout_cleanup_preflight',side_effect=ValueError('native cleanup failure')), \
             patch.object(e,'snapshot') as snapshot,patch.object(s,'run_training') as train:
            with self.assertRaisesRegex(ValueError,'native cleanup failure'):e.scientific_worker(ROOT,ROOT,HEAD)
            snapshot.assert_not_called();h['locks'].WinAPI.assert_not_called();train.assert_not_called()

    def test_13_saved_reconstruction_mismatch_blocks_finalization(self):
        finish=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
            e.execute_stages(Mock(),lambda:dict(tests=s.FULL_TESTS,modules=s.MODULES),lambda:{'gate':False},lambda:{'gate':True},finish)
        finish.assert_not_called()

    def test_14_run_does_not_retry_scientific_process_failure(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'guard'),patch.object(e,'run_logged',side_effect=ValueError('synthetic failure')) as run, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            root=Path(tmp)
            with self.assertRaises(ValueError):e.run(root,root/'runs/x',HEAD)
            self.assertEqual(run.call_count,1);self.assertIn('run_execution_valid = false',output.getvalue())

    def test_15_run_requires_successful_fresh_verifier(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'guard'),patch.object(e,'run_logged',side_effect=[1,ValueError('synthetic verifier failure')]) as run, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            root=Path(tmp)
            with self.assertRaises(ValueError):e.run(root,root/'runs/x',HEAD)
            self.assertEqual(run.call_count,2);self.assertIn('run_execution_valid = false',output.getvalue())

    def test_16_real_git_guard_requires_clean_correct_active_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);subprocess.run(['git','init','-q',str(root)],check=True)
            for args in [('checkout','-qb',e.BRANCH),('config','user.name','C346 fixture'),('config','user.email','c346@example.invalid')]:
                subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
            (root/'docs').mkdir();path=root/'docs/experiment-ledger-and-handoff.md'
            path.write_text('## Formal state\nC346 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
            subprocess.run(['git','-C',str(root),'add','.'],check=True);subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
            head=e.git(root,'rev-parse','HEAD');e.guard(root,head)
            with self.assertRaises(ValueError):e.guard(root,HEAD)
            path.write_text('dirty\n',encoding='utf-8')
            with self.assertRaises(ValueError):e.guard(root,head)
        self.assertFalse(e.active('## Formal state\nC344 ACTIVE / NOT YET JUDGED\n'))
        self.assertFalse(e.active('## Formal state\nC345 ACTIVE / NOT YET JUDGED\n'))
        self.assertFalse(e.active('## Formal state\nC346 ACTIVE / NOT YET JUDGED\nC344 ACTIVE / NOT YET JUDGED\n'))
        self.assertFalse(e.active('## History\nC346 ACTIVE / NOT YET JUDGED\n'))
        self.assertTrue(e.active('## Formal state\r\n**C346 ACTIVE / NOT YET JUDGED**\r\n## History\r\nC344 ACTIVE / NOT YET JUDGED'))

    def test_17_utf8_json_exclusive_writer_rejects_duplicate_and_nonfinite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'j';e.save(path,{'名前':'甲乙'});self.assertEqual(e.read(path),{'名前':'甲乙'})
            with self.assertRaises(FileExistsError):e.save(path,{})
            for value in ('{"a":1,"a":2}','NaN','{"v":Infinity}'):
                path.write_text(value,encoding='utf-8')
                with self.assertRaises(ValueError):e.read(path)

    def test_18_source_blob_accepts_only_exact_lf_or_crlf(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'source';raw=b'a\nb\n';oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
            for value in (raw,raw.replace(b'\n',b'\r\n')):path.write_bytes(value);e.source_bytes(path,oid)
            path.write_bytes(b'a\r\nb\n')
            with self.assertRaises(ValueError):e.source_bytes(path,oid)

    def test_19_real_nonzero_subprocess_preserves_output(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);log=root/'failure.log'
            with self.assertRaises(ValueError):
                e.run_logged(root,[sys.executable,'-c','print("synthetic failure");raise SystemExit(7)'],log,'fixture')
            self.assertIn('synthetic failure',log.read_text(encoding='utf-8'))
        value=accepted.timeout_preflight_expected(HEAD)
        parent=NS(EXECUTION_REVISION=accepted.EXECUTION_REVISION,
                  timeout_cleanup_preflight=Mock(return_value=value),check_timeout_preflight=accepted.check_timeout_preflight)
        h=dict(cleanup=parent,parent=NS(EXECUTION_REVISION='C345-R0'),recovery=recovery)
        self.assertIs(e.timeout_cleanup_preflight(ROOT,HEAD,h),value)
        parent.timeout_cleanup_preflight.assert_called_once_with(ROOT,HEAD,recovery)
        parent.timeout_cleanup_preflight.reset_mock()
        parent.EXECUTION_REVISION='unreviewed'
        with self.assertRaises(ValueError):e.timeout_cleanup_preflight(ROOT,HEAD,h)
        parent.timeout_cleanup_preflight.assert_not_called()
        parent.EXECUTION_REVISION=accepted.EXECUTION_REVISION
        parent.timeout_cleanup_preflight.return_value={**value,'cleanup_barriers':5}
        with self.assertRaises(ValueError):e.timeout_cleanup_preflight(ROOT,HEAD,h)
        sentinel=RuntimeError('native fixture failure');parent.timeout_cleanup_preflight.side_effect=sentinel
        with self.assertRaises(RuntimeError) as caught:e.timeout_cleanup_preflight(ROOT,HEAD,h)
        self.assertIs(caught.exception,sentinel)

    def test_20_cli_rejects_unknown_mode_and_command_contract(self):
        proc=subprocess.run([sys.executable,str(ROOT/'tools/c346_execution.py'),'--folder','unused','--expected-head',HEAD,'--mode','bad'],
                            capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(proc.returncode,0);self.assertIn('invalid choice',proc.stderr)
        for mode in ('science','regression','module','verify'):
            args=e.command(ROOT,ROOT/'runs/x',HEAD,mode)
            self.assertEqual(args[-2:],['--mode',mode]);self.assertEqual(args[args.index('--expected-head')+1],HEAD)
            self.assertEqual(Path(args[5]),ROOT/'tools/c346_execution.py')

    def test_21_hash_bound_semantics_rejects_artifact_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            for name in s.OUTPUTS:(out/name).write_bytes(b'fixture')
            def change():(out/s.OUTPUTS[0]).write_bytes(b'changed')
            with self.assertRaises(ValueError):e.bound_semantics(out,change)

    def test_22_launcher_preflight_precedes_logging_and_uses_current_routes(self):
        text=(ROOT/'tools/invoke_c346.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','WRONG_BRANCH','DIRTY_TRACKED_TREE','ParseFile'):
            self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C346',text);self.assertIn('scientific_training_requested = True',text)
        self.assertIn('runs\\c346-pair-max-rate-',text)
        self.assertIn('c346_execution.py',(ROOT/'tools/run_c346.ps1').read_text(encoding='utf-8'))
        self.assertIn("-ne '346'",text)

    def test_23_manifest_counts_match_real_loaders_and_protected_inventory(self):
        s.validate_seal()
        own=[unittest.defaultTestLoader.loadTestsFromName(name).countTestCases() for name in e.TEST_MODULES]
        self.assertEqual(sum(own),s.OWN_TESTS);self.assertEqual(6578+sum(own),s.FULL_TESTS)
        self.assertEqual(241+len(own),s.MODULES)
        self.assertEqual(len(s.OWN),7);self.assertEqual(len(set(s.OWN)),7)
        self.assertEqual(937+len(s.OWN),s.SOURCE_COUNT);self.assertEqual(8679+491+len(s.OWN),s.INPUT_COUNT)
        self.assertEqual(set(name.replace('.','/')+'.py' for name in e.TEST_MODULES),{p for p in s.OWN if p.startswith('tests_lm/')})

    def test_24_complete_regression_receipt_rejects_partial_or_skipped_success(self):
        receipt=e.receipt(HEAD,s.FULL_TESTS);e.check_regression(receipt,HEAD,s.FULL_TESTS)
        for key,value in (('tests',s.FULL_TESTS-1),('skipped',1),('successful',False),('errors',1),('failures',1),('commit_sha','b'*40)):
            changed=dict(receipt);changed[key]=value
            with self.assertRaises(ValueError):e.check_regression(changed,HEAD,s.FULL_TESTS)

    def test_25_real_helper_bridge_keeps_diagnostic_and_cleanup_parents_distinct(self):
        h=e.helpers(ROOT)
        self.assertEqual(set(h),{'parent','prior','cleanup','recovery','c330','runtime','legacy','locks'})
        self.assertIs(h['cleanup'],h['prior']['parent'])
        self.assertEqual(h['parent'].EXECUTION_REVISION,'C345-R0')
        self.assertEqual(h['cleanup'].EXECUTION_REVISION,'C344-R1')
        self.assertFalse(hasattr(h['parent'],'timeout_monitor_boundary'))
        self.assertTrue(callable(h['cleanup'].timeout_monitor_boundary))
        for head in (e.PARENT_HEAD,HEAD):
            receipt=h['cleanup'].timeout_preflight_expected(head)
            e.check_timeout_preflight(receipt,head,h['cleanup'])
            with self.assertRaises(ValueError):e.check_timeout_preflight(receipt,'b'*40,h['cleanup'])
        with self.assertRaises(ValueError):e.check_timeout_preflight(receipt,HEAD,h['parent'])

    def test_26_failed_native_objective_preflight_blocks_regression_and_training(self):
        preflight=Mock(side_effect=ValueError('synthetic objective preflight failure'))
        regression,train,verify,finalize=Mock(),Mock(),Mock(),Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaisesRegex(ValueError,'objective preflight'):
            e.execute_stages(preflight,regression,train,verify,finalize)
        preflight.assert_called_once_with()
        for call in (regression,train,verify,finalize):call.assert_not_called()


if __name__=='__main__':unittest.main()
