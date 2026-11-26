"""C347 execution software checks; synthetic evidence is never a scientific result."""
from __future__ import annotations
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch
from fold_lm.v05_benchmarks import model_c347_saved_loss_transition as s

ROOT = Path(__file__).resolve().parents[1]
HEAD = 'a'*40


def module_at(name, path):
    loader = importlib.util.spec_from_file_location(name, ROOT/path)
    value = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(value)
    return value


e = module_at('_c347_executor_tests', 'tools/c347_execution.py')
recovery = module_at('_c347_accepted_recovery', 'tools/c330_recovery_r1.py')
accepted = module_at('_c347_accepted_timeout', 'tools/c344_execution.py')


def plan_fixture():
    """Synthetic ancestor IDs plus the actual two new module inventories."""
    groups = []
    q, r = divmod(6652, 243)
    for i in range(243):
        name = f'tests_lm.synthetic_{i:03d}'
        groups.append(dict(module=name, test_ids=[name+f'.Cases.test_{j:03d}' for j in range(q+(i < r))]))
    base_hash = s.digest([v for g in groups for v in g['test_ids']])
    for name in e.TEST_MODULES:
        own = list(recovery.flatten(unittest.defaultTestLoader.loadTestsFromName(name)))
        e.require(own and all(type(t).__module__ == name for t in own), 'real own module loader')
        groups.append(dict(module=name, test_ids=[t.id() for t in own]))
    ids = [v for g in groups for v in g['test_ids']]
    return dict(schema='fold-c347-regression-plan-v1', commit_sha=HEAD, manifest_sha256=s.MANIFEST_SHA,
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


def parent_gate_components():
    return dict(all_candidates_full_pass=False,candidate_full_pass_count=0,
        nonnegative_counts=dict(mean_ce=dict(passed=64,total=120),pair_max=dict(passed=68,total=120)),
        nonnegative_vs_mean_ce=False,nonnegative_vs_pair_max=False,strict_interior_vs_pair_max=False)


def parent_fixture():
    ps = NS(validate_seal=Mock(), check_summary=Mock(), EXPERIMENT_ID='synthetic-parent', STAGE='synthetic-stage',
            MANIFEST_SHA='synthetic-manifest', WORK={})
    parent = NS(spec=lambda:ps, PARENT_SUMMARY='old-summary', PARENT_ENVELOPE='old-envelope',
        EXECUTION_REVISION='C346-R0')
    pins = {e.P_PATH:e.P_BLOB, e.S_PATH:e.S_BLOB, **{f'p{i}':'a' for i in range(942)}}
    inputs = {f'i{i}':'b' for i in range(9177)}
    r = dict(schema='fold-c346-trained-v1', commit_sha=e.PARENT_HEAD, experiment_id=ps.EXPERIMENT_ID,
        stage=ps.STAGE, status='FAIL', scientific_execution_valid=True, capability_gate_applicable=True,
        gate_f_candidate=False, production_adoption=False, manifest_sha256=ps.MANIFEST_SHA,
        source_blobs=pins, input_sha256=inputs, validation_summary=dict(candidate_gate=False,eligible_seed_count=0,gate_components=parent_gate_components()))
    v = dict(schema='fold-c346-execution-envelope-v1', commit_sha=e.PARENT_HEAD, scientific_status='FAIL',
        scientific_summary_sha256=e.PARENT_SUMMARY, manifest_sha256=ps.MANIFEST_SHA, scientific_work={},
        source_count=944, input_count=9177, source_blobs=pins, input_sha256=inputs, parent_summary_sha256=parent.PARENT_SUMMARY,
        parent_envelope_sha256=parent.PARENT_ENVELOPE, immediate_parent_semantic_reconstruction=True,
        parent_regression_reconstructed=True, ancestor_semantic_reruns=0, saved_semantic_reconstruction=True,
        final_reference_rechecks=9177, hash_stats={'final_reference_rechecks':9177}, regression=e.receipt(e.PARENT_HEAD,6652),
        execution_revision='C346-R0',timeout_cleanup_implementation='C344-R1',
        timeout_cleanup_preflight=accepted.timeout_preflight_expected(e.PARENT_HEAD))
    return r,v,parent


def validation_fixture(folder, pins=None, inputs=None, tests=None):
    sources,protected=e.protected_counts()
    pins={f'p{i}':'a' for i in range(sources)} if pins is None else pins
    inputs={f'i{i}':'b' for i in range(protected)} if inputs is None else inputs
    tests=tests or dict(tests=s.FULL_TESTS,modules=s.MODULES,plan_sha256='1'*64,evidence_sha256='2'*64,result_sha256='3'*64)
    runtime=e.runtime_identity(NS(__version__='fixture'),NS(__version__='fixture'))
    return dict(schema='fold-c347-runtime-validation-v1',experiment_id=s.EXPERIMENT_ID,stage=s.STAGE,commit_sha=HEAD,
        run_folder=e.canonical(folder),manifest_sha256=s.MANIFEST_SHA,status='PASS',source_blobs=pins,input_sha256=inputs,
        source_count=sources,input_count=protected,compile_imports=e.own_compile_inventory(),regression=e.receipt(HEAD,s.FULL_TESTS),
        regression_isolation=tests,parent_summary_sha256=e.PARENT_SUMMARY,parent_envelope_sha256=e.PARENT_ENVELOPE,
        immediate_parent_semantic_reconstruction=True,parent_regression_reconstructed=True,ancestor_semantic_reruns=0,
        final_reference_rechecks=protected,hash_stats={'final_reference_rechecks':protected},execution_revision=e.EXECUTION_REVISION,
        timeout_cleanup_implementation=e.TIMEOUT_CLEANUP_IMPLEMENTATION,timeout_cleanup_preflight=accepted.timeout_preflight_expected(HEAD),
        native_runtime=runtime,validation_log=dict(file='validation.log',sha256='4'*64,serialized_bytes=1))


class C347ExecutionTests(unittest.TestCase):
    def test_01_parent_trained_contract_preserves_negative_capability(self):
        r,v,parent = parent_fixture(); e.parent_contract(r,v,parent,accepted)
        parent.spec().check_summary.assert_called_once_with(r['validation_summary'])
        for target,key,value in ((0,'status','PASS'),(0,'capability_gate_applicable',False),
                                 (0,'scientific_execution_valid',False),(1,'source_count',943),
                                 (1,'input_count',9176),(1,'final_reference_rechecks',9176),
                                 (1,'ancestor_semantic_reruns',1),(1,'scientific_work',{'steps':1}),(1,'execution_revision','C344-R1')):
            with self.subTest(key=key):
                args=parent_fixture();args[target][key]=value
                with self.assertRaises(ValueError):e.parent_contract(*args,accepted)
        for key,value in (('candidate_gate',True),('eligible_seed_count',2)):
            args=parent_fixture();args[0]['validation_summary'][key]=value
            with self.assertRaises(ValueError):e.parent_contract(*args,accepted)
        args=parent_fixture();args[1]['timeout_cleanup_preflight']['cleanup_barriers']=5
        with self.assertRaises(ValueError):e.parent_contract(*args,accepted)

    def test_02_all_parent_regression_proofs_are_retained(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);items=[]
            for i in range(243):
                a=folder/f'module-{i:03d}.json';b=folder/f'module-{i:03d}.log'
                a.write_bytes(b'{}');b.write_bytes(b'explicit synthetic receipt')
                items.append(dict(index=i,receipt_sha256=e.sha(a),log_sha256=e.sha(b)))
            for name,value in (('regression-plan.json',{}),('regression-result.json',{}),('regression-evidence.json',{'modules':items})):
                e.save(folder/name,value)
            bound=dict(tests=6652,modules=243,plan_sha256=e.sha(folder/'regression-plan.json'),
                       evidence_sha256=e.sha(folder/'regression-evidence.json'),result_sha256=e.sha(folder/'regression-result.json'))
            self.assertEqual(len(e.parent_test_files(folder,{'regression_isolation':bound},e.sha)),489)
            (folder/'module-242.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.parent_test_files(folder,{'regression_isolation':bound},e.sha)

    def test_03_snapshot_rebuilds_exact_source_and_input_union(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);out=root/e.PARENT_FOLDER/'science';out.mkdir(parents=True);pins={};inputs={};tree={}
            for i in range(9177):
                name=f'old/{i}.py' if i<944 else f'data/{i}.bin';path=root/name;path.parent.mkdir(exist_ok=True)
                raw=str(i).encode();path.write_bytes(raw);inputs[e.canonical(path)]=e.sha(path)
                if i<944:pins[name]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();tree[name]=pins[name]
            for name in s.OWN:
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);raw=name.encode();path.write_bytes(raw)
                tree[name]=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            names=('experiment-plan.json','training-traces.json','trained-models.pt','evaluations.pt','measurements.json','validation-summary.json')
            for name in names:(out/name).write_bytes(b'fixture')
            proofs={}
            for i in range(489):
                path=out.parent/f'proof-{i}';path.write_bytes(b'fixture');proofs[e.canonical(path)]=e.sha(path)
            e.save(out/'summary.json',{'artifacts':[]})
            e.save(out.parent/'execution-envelope.json',dict(source_blobs=pins,input_sha256=inputs,regression_isolation={}))
            def ancestor(root,prior,hash_file):
                for name,wanted in inputs.items():self.assertEqual(hash_file(name),wanted)
                return {},{},pins,inputs
            h=dict(parent=NS(spec=lambda:NS(OUTPUTS=names),snapshot=ancestor,build_plan=lambda *a:{},verify_tests=lambda *a:{}),
                   prior={},cleanup=accepted,recovery=None,legacy=NS(tree_blobs=lambda root:tree,
                   descriptors=lambda out,items,names,hash_file:{e.canonical(out/n):hash_file(out/n) for n in names}))
            seen=[]
            def tracked_hash(path):
                seen.append(Path(path));return e.sha(path)
            def wrong_envelope_hash(path):
                return 'f'*64 if Path(path)==out.parent/'execution-envelope.json' else e.sha(path)
            with patch.object(e,'PARENT_SUMMARY',e.sha(out/'summary.json')),patch.object(e,'PARENT_ENVELOPE',e.sha(out.parent/'execution-envelope.json')), \
                 patch.object(e,'parent_contract'),patch.object(e,'parent_test_files',return_value=proofs):
                _,_,p,v=e.snapshot(root,h,tracked_hash)
                self.assertEqual((len(p),len(v)),(s.SOURCE_COUNT,s.INPUT_COUNT));self.assertEqual(len(inputs),9177)
                self.assertIn(out/'summary.json',seen);self.assertIn(out.parent/'execution-envelope.json',seen)
                with self.assertRaisesRegex(ValueError,'exact parent bytes'):e.snapshot(root,h,wrong_envelope_hash)
                tree['old/0.py']='bad'
                with self.assertRaises(ValueError):e.snapshot(root,h,e.sha)

    def test_04_parent_dispatch_uses_exact_four_argument_trained_contract(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);source=root/e.PARENT_FOLDER/'science';data=root/'c329/science'
            names=('experiment-plan.json','training-traces.json','trained-models.pt','evaluations.pt','measurements.json','validation-summary.json')
            for folder,ns in ((source,names),(data,('dataset.json','original-prompts.json','interior-prompts.json'))):
                folder.mkdir(parents=True)
                for name in ns:(folder/name).write_bytes(b'{}')
            inputs={e.canonical(p):e.sha(p) for folder in (source,data) for p in folder.iterdir()};saved={'synthetic':'trained-parent'}
            inside=[];calls=[]
            @contextlib.contextmanager
            def no_neural():
                inside.append(True)
                try:yield
                finally:inside.pop()
            x=NS(guarded=NS(no_neural=no_neural),c=NS(p267=NS(validate_data=Mock())))
            cx=(None,None,NS(new_prompts=lambda v:{},check_prompts=Mock()),None,None,x)
            def trained_recheck(actual_source,actual_data,actual_context,reader):
                self.assertTrue(inside);self.assertEqual((actual_source,actual_data,actual_context,reader),(source,data,cx,e.read))
                calls.append('C346');return saved
            base=NS(context=lambda:cx,digest=s.digest,DATA_SHA=s.digest({}),PROMPTS_SHA=s.digest({}))
            previous=NS(source=lambda:NS(base=lambda:base),load_data=lambda *a:({}, {}, {}),semantic_recheck=Mock())
            ps=NS(OUTPUTS=names,previous=lambda:previous,semantic_recheck=trained_recheck)
            h=dict(parent=NS(spec=lambda:ps),c330=NS(PARENT_FOLDER='c329'))
            self.assertEqual(e.parent_semantics(root,h,{'validation_summary':saved},inputs),(source,data,cx))
            self.assertEqual(calls,['C346']);self.assertFalse(inside)
            previous.semantic_recheck.assert_not_called()
            for path in (*(source/name for name in names),*(data/name for name in ('dataset.json','original-prompts.json','interior-prompts.json'))):
                incomplete=dict(inputs);del incomplete[e.canonical(path)]
                with self.assertRaises(ValueError):e.parent_semantics(root,h,{'validation_summary':saved},incomplete)

    def test_05_pinned_parent_bytes_are_checked_before_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in (e.P_PATH,e.S_PATH):p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'fixture')
            prior={k:object() for k in ('parent','prior','recovery','c330','runtime','legacy','locks')}
            prior['cleanup']=accepted
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
            (folder/'module-244.log').write_bytes(b'changed')
            with self.assertRaises(ValueError):e.verify_tests(folder,HEAD,plan,recovery)

    def test_08_module_process_dispatch_uses_inherited_timeout_boundary(self):
        plan,base_hash=plan_fixture();group=plan['groups'][0]
        boundary=Mock(wraps=accepted.timeout_monitor_boundary)
        h={'recovery':recovery,'cleanup':NS(timeout_monitor_boundary=boundary)}
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

    def test_10_real_worker_and_fresh_verifier_reuse_validated_proofs_and_preserve_parent_negative(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()) as output:
            root=Path(tmp);folder=root/'runs/x';folder.mkdir(parents=True)
            source=root/'saved-parent';data=root/'canonical-data'
            pins={f'p{i}':'a' for i in range(s.SOURCE_COUNT)};inputs={f'i{i}':'b' for i in range(s.INPUT_COUNT)};calls=[]
            closure={f'v{i}':'c' for i in range(s.manifest()['validation_retained_files'])}
            binding=dict(receipt_sha256='1'*64,log_sha256='2'*64,retained_files=len(closure),closure_sha256='3'*64)
            validated=validation_fixture(folder,pins,inputs)
            e.save(folder/'regression-result.json',e.receipt(HEAD,s.FULL_TESTS))
            value=dict(parent_validation_summary=dict(candidate_gate=False,eligible_seed_count=0),diagnostic_complete=True)
            class Cache:
                sha=staticmethod(e.sha)
                def __init__(self,reference,lease_factory,*,progress,max_files):
                    self.kind='input' if max_files==len(inputs) else 'validation'
                    self.expected=inputs if self.kind=='input' else closure
                    e.require(type(max_files) is int and max_files==len(self.expected),'exact separate finite capacity')
                    self.entries={};self.stats={'final_reference_rechecks':max_files}
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release-'+self.kind)
                def recheck(self):
                    calls.append(self.kind+'-final');return [{'path':k,'sha256':v} for k,v in self.expected.items()]
            inside=[]
            @contextlib.contextmanager
            def no_neural():
                inside.append(True)
                try:yield
                finally:inside.pop()
            cx=(NS(guarded=NS(no_neural=no_neural)),)
            previous=NS(source=lambda:NS(base=lambda:NS(check_dependencies=lambda *a:None,peak_rss=lambda:1)))
            parent=NS(spec=lambda:NS(previous=lambda:previous),EXECUTION_REVISION='C346-R0')
            def native_runtime():calls.append('runtime');return NS(__version__='fixture'),NS(__version__='fixture')
            h=dict(parent=parent,cleanup=accepted,runtime=NS(native_runtime=native_runtime),
                locks=NS(WinAPI=lambda:None,LockedHashes=Cache,ReadLease=None),
                legacy=NS(descriptors=lambda out,items,*a:e.require(items==e.artifacts(out),'artifact descriptors')),recovery=None)
            def snapshot(*args):calls.append('snapshot');return {'validation_summary':{}},{},pins,inputs
            def reuse(repo,actual_folder,head,actual_h,actual_pins,actual_inputs,runtime,hash_file):
                self.assertEqual((repo,actual_folder,head,actual_h,actual_pins,actual_inputs),(root,folder,HEAD,h,pins,inputs))
                self.assertEqual(runtime,validated['native_runtime']);calls.append('validated-tests')
                return validated,binding,closure
            def diagnose(out,parent_out,data_out,context,reader):
                self.assertTrue(inside)
                self.assertEqual((out,parent_out,data_out,context,reader),(folder/'science',source,data,cx,e.read))
                self.assertEqual(calls[-1],'validated-tests');calls.append('diagnose')
                for name in s.OUTPUTS:(out/name).write_bytes(b'explicit synthetic artifact')
                return value
            def recheck(out,parent_out,data_out,context,reader):
                self.assertTrue(inside)
                self.assertEqual((out,parent_out,data_out,context,reader),(folder/'science',source,data,cx,e.read))
                calls.append('verify');return value
            def report(actual,emitter):
                self.assertTrue(inside);self.assertEqual((actual,emitter),(value,e.emit));calls.append('report')
            with patch.object(e,'guard'),patch.object(e,'ready_for_execution'),patch.object(e,'helpers',return_value=h), \
                 patch.object(e,'snapshot',side_effect=snapshot),patch.object(e,'parent_semantics',return_value=(source,data,cx)), \
                 patch.object(e,'verify_validation',side_effect=reuse),patch.object(e,'run_logged') as process, \
                 patch.object(s,'run_diagnostic',side_effect=diagnose),patch.object(s,'semantic_recheck',side_effect=recheck), \
                 patch.object(s,'report_results',side_effect=report),patch.object(s,'check_summary'):
                e.scientific_worker(root,folder,HEAD);e.verify_outputs(root,folder,HEAD)
                self.assertEqual(calls,['runtime','snapshot','validated-tests','diagnose','verify','input-final','validation-final',
                    'release-validation','release-input','report','runtime','snapshot','validated-tests','verify',
                    'input-final','validation-final','release-validation','release-input'])
                process.assert_not_called();self.assertFalse(inside)
                line=next(line for line in output.getvalue().splitlines() if line.startswith('validated_regression_reused = '))
                published=json.loads(line.split(' = ',1)[1]);self.assertEqual({k:published[k] for k in binding},binding)
                actual=e.read(folder/'science/summary.json')
                self.assertEqual(actual['status'],'PASS');self.assertTrue(actual['diagnostic_execution_valid'])
                self.assertFalse(actual['capability_gate_applicable']);self.assertFalse(actual['gate_f_candidate']);self.assertFalse(actual['production_adoption'])
                self.assertEqual(actual['validation_summary']['parent_validation_summary'],dict(candidate_gate=False,eligible_seed_count=0))
                path=folder/'execution-envelope.json';envelope=e.read(path)
                self.assertEqual(envelope['execution_revision'],'C347-R0')
                self.assertEqual(envelope['timeout_cleanup_implementation'],'C344-R1')
                self.assertEqual(envelope['timeout_cleanup_preflight'],accepted.timeout_preflight_expected(HEAD))
                self.assertEqual(envelope['validation_binding'],binding)
                self.assertEqual(envelope['regression_executions_in_execute'],0)
                for key,bad in (('tests',5),('cleanup_barriers',5),('cleanup_ready',False),('platform','other'),
                                ('commit_sha','b'*40),('source_blobs',{}),('execution_revision','C347-R0')):
                    changed=copy.deepcopy(envelope);changed['timeout_cleanup_preflight'][key]=bad;path.write_bytes(s.blob(changed))
                    with self.assertRaises(ValueError):e.verify_outputs(root,folder,HEAD)
                for key,bad in (('execution_revision','unreviewed'),('timeout_cleanup_implementation','unreviewed'),
                                ('validation_binding',{}),('validation_reference_rechecks',494),
                                ('regression_executions_in_validate',0),('regression_executions_in_execute',1),('retained_output_files',499)):
                    changed=copy.deepcopy(envelope);changed[key]=bad;path.write_bytes(s.blob(changed))
                    with self.assertRaises(ValueError):e.verify_outputs(root,folder,HEAD)
                for key in ('started_ids','success_ids'):
                    changed=copy.deepcopy(envelope);changed['timeout_cleanup_preflight'][key].pop();path.write_bytes(s.blob(changed))
                    with self.assertRaises(ValueError):e.verify_outputs(root,folder,HEAD)
                path.write_bytes(s.blob(envelope))
                actual['capability_gate_applicable']=True;(folder/'science/summary.json').write_bytes(s.blob(actual))
                with self.assertRaises(ValueError):e.verify_outputs(root,folder,HEAD)

    def test_11_regression_failure_never_enters_diagnosis(self):
        diagnose=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
            e.execute_stages(Mock(side_effect=ValueError('synthetic regression failure')),diagnose,Mock(),Mock())
        diagnose.assert_not_called()

    def test_12_incomplete_regression_scope_blocks_diagnosis(self):
        diagnose=Mock()
        for value in (dict(tests=s.FULL_TESTS-1,modules=s.MODULES),dict(tests=s.FULL_TESTS,modules=s.MODULES-1)):
            with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
                e.execute_stages(lambda:value,diagnose,Mock(),Mock())
        diagnose.assert_not_called()
        h=dict(runtime=NS(native_runtime=Mock(return_value=(NS(__version__='fixture'),NS(__version__='fixture')))),locks=Mock(),recovery=None)
        with patch.object(e,'guard'),patch.object(e,'helpers',return_value=h), \
             patch.object(e,'compile_import_own',return_value=e.own_compile_inventory()), \
             patch.object(e,'timeout_cleanup_preflight',side_effect=ValueError('native cleanup failure')), \
             patch.object(e,'snapshot') as snapshot,patch.object(s,'run_diagnostic') as diagnose:
            with self.assertRaisesRegex(ValueError,'native cleanup failure'):e.runtime_validation(ROOT,ROOT,HEAD)
            snapshot.assert_not_called();h['locks'].WinAPI.assert_not_called();diagnose.assert_not_called()

    def test_13_saved_reconstruction_mismatch_blocks_finalization(self):
        finish=Mock()
        with contextlib.redirect_stdout(io.StringIO()),self.assertRaises(ValueError):
            e.execute_stages(lambda:dict(tests=s.FULL_TESTS,modules=s.MODULES),lambda:{'gate':False},lambda:{'gate':True},finish)
        finish.assert_not_called()

    def test_14_run_does_not_retry_scientific_process_failure(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'guard'),patch.object(e,'ready_for_execution'),patch.object(e,'run_logged',side_effect=ValueError('synthetic failure')) as run, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            root=Path(tmp)
            with self.assertRaises(ValueError):e.run(root,root/'runs/x',HEAD)
            self.assertEqual(run.call_count,1);self.assertIn('run_execution_valid = false',output.getvalue())

    def test_15_run_requires_successful_fresh_verifier(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'guard'),patch.object(e,'ready_for_execution'),patch.object(e,'run_logged',side_effect=[1,ValueError('synthetic verifier failure')]) as run, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            root=Path(tmp)
            with self.assertRaises(ValueError):e.run(root,root/'runs/x',HEAD)
            self.assertEqual(run.call_count,2);self.assertIn('run_execution_valid = false',output.getvalue())

    def test_16_real_git_guard_requires_clean_correct_active_branch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);subprocess.run(['git','init','-q',str(root)],check=True)
            for args in [('checkout','-qb',e.BRANCH),('config','user.name','C347 fixture'),('config','user.email','c347@example.invalid')]:
                subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
            (root/'docs').mkdir();path=root/'docs/experiment-ledger-and-handoff.md'
            path.write_text('## Formal state\nC347 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
            subprocess.run(['git','-C',str(root),'add','.'],check=True);subprocess.run(['git','-C',str(root),'commit','-qm','fixture'],check=True)
            head=e.git(root,'rev-parse','HEAD');e.guard(root,head)
            with self.assertRaises(ValueError):e.guard(root,HEAD)
            path.write_text('dirty\n',encoding='utf-8')
            with self.assertRaises(ValueError):e.guard(root,head)
        self.assertFalse(e.active('## Formal state\nC344 ACTIVE / NOT YET JUDGED\n'))
        self.assertFalse(e.active('## Formal state\nC343 ACTIVE / NOT YET JUDGED\n'))
        self.assertFalse(e.active('## Formal state\nC347 ACTIVE / NOT YET JUDGED\nC344 ACTIVE / NOT YET JUDGED\n'))
        self.assertFalse(e.active('## History\nC347 ACTIVE / NOT YET JUDGED\n'))
        self.assertTrue(e.active('## Formal state\r\n**C347 ACTIVE / NOT YET JUDGED**\r\n## History\r\nC344 ACTIVE / NOT YET JUDGED'))

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
        h=dict(parent=NS(EXECUTION_REVISION='C346-R0'),cleanup=parent,recovery=recovery)
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
        proc=subprocess.run([sys.executable,str(ROOT/'tools/c347_execution.py'),'--folder','unused','--expected-head',HEAD,'--mode','bad'],
                            capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(proc.returncode,0);self.assertIn('invalid choice',proc.stderr)
        for mode in ('validate','science','regression','module','verify'):
            args=e.command(ROOT,ROOT/'runs/x',HEAD,mode)
            self.assertEqual(args[-2:],['--mode',mode]);self.assertEqual(args[args.index('--expected-head')+1],HEAD)
            self.assertEqual(Path(args[5]),ROOT/'tools/c347_execution.py')

    def test_21_hash_bound_semantics_rejects_artifact_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            for name in s.OUTPUTS:(out/name).write_bytes(b'fixture')
            def change():(out/s.OUTPUTS[0]).write_bytes(b'changed')
            with self.assertRaises(ValueError):e.bound_semantics(out,change)

    def test_22_launcher_preflight_precedes_logging_and_uses_current_routes(self):
        text=(ROOT/'tools/invoke_c347.ps1').read_text(encoding='utf-8')
        for token in ('STALE_EXPECTED_HEAD','STALE_EXPERIMENT','WRONG_BRANCH','DIRTY_TRACKED_TREE','ParseFile'):
            self.assertLess(text.index(token),text.index('$log ='))
        self.assertIn('-ExperimentId C347',text);self.assertIn('scientific_training_requested = False',text)
        self.assertIn('runs\\c347-saved-loss-transition-',text)
        self.assertIn('c347_execution.py',(ROOT/'tools/run_c347.ps1').read_text(encoding='utf-8'))
        self.assertIn("-ne '347'",text)
        self.assertLess(text.index('--mode validate'),text.index('$log ='))
        self.assertLess(text.index("Skip-Invocation 'AUTHORING_RUNTIME_PREFLIGHT_FAILED'"),text.index('$log ='))
        self.assertGreater(text.rindex('STALE_EXPECTED_HEAD'),text.index('--mode validate'))
        self.assertEqual(text.count('Get-Content -LiteralPath $validationLog -Encoding UTF8'),1)

    def test_23_manifest_counts_match_real_loaders_and_protected_inventory(self):
        s.validate_seal()
        own=[unittest.defaultTestLoader.loadTestsFromName(name).countTestCases() for name in e.TEST_MODULES]
        self.assertEqual(sum(own),s.OWN_TESTS);self.assertEqual(6652+sum(own),s.FULL_TESTS)
        self.assertEqual(243+len(own),s.MODULES)
        self.assertEqual(len(s.OWN),7);self.assertEqual(len(set(s.OWN)),7)
        self.assertEqual(944+len(s.OWN),s.SOURCE_COUNT);self.assertEqual(9177+497+len(s.OWN),s.INPUT_COUNT)
        self.assertEqual(set(name.replace('.','/')+'.py' for name in e.TEST_MODULES),{p for p in s.OWN if p.startswith('tests_lm/')})
        manifest=s.manifest()
        self.assertEqual(manifest['regression_proof_files'],3+2*s.MODULES)
        self.assertEqual(manifest['validation_outputs'],['validation-receipt.json','validation.log'])
        self.assertEqual(manifest['validation_retained_files'],manifest['regression_proof_files']+len(manifest['validation_outputs']))
        self.assertEqual(manifest['retained_output_files'],len(s.OUTPUTS)+2+manifest['validation_retained_files'])

    def test_24_complete_regression_receipt_rejects_partial_or_skipped_success(self):
        receipt=e.receipt(HEAD,s.FULL_TESTS);e.check_regression(receipt,HEAD,s.FULL_TESTS)
        for key,value in (('tests',s.FULL_TESTS-1),('skipped',1),('successful',False),('errors',1),('failures',1),('commit_sha','b'*40)):
            changed=dict(receipt);changed[key]=value
            with self.assertRaises(ValueError):e.check_regression(changed,HEAD,s.FULL_TESTS)

    def test_25_c346_helper_bridge_selects_c344_cleanup_not_diagnostic_parent(self):
        self.assertEqual(accepted.EXECUTION_REVISION,'C344-R1')
        wrong_parent=NS(EXECUTION_REVISION='C345-R0')
        prior={k:object() for k in ('prior','recovery','c330','runtime','legacy','locks')}
        prior.update(parent=wrong_parent,cleanup=accepted)
        parent=NS(EXECUTION_REVISION='C346-R0',spec=lambda:NS(validate_seal=Mock()),helpers=Mock(return_value=prior))
        with patch.object(e,'git',side_effect=lambda *a:e.P_BLOB if a[-1]=='HEAD:'+e.P_PATH else e.S_BLOB), \
             patch.object(e,'source_bytes'), \
             patch.object(e.importlib.util,'spec_from_file_location',return_value=NS(loader=NS(exec_module=lambda m:None))), \
             patch.object(e.importlib.util,'module_from_spec',return_value=parent):
            h=e.helpers(ROOT)
            self.assertIs(h['parent'],parent);self.assertIs(h['prior'],prior);self.assertIs(h['cleanup'],accepted)
            self.assertIsNot(h['cleanup'],h['parent']);self.assertIsNot(h['cleanup'],prior['parent'])
            parent.helpers.assert_called_once_with(ROOT)
            for changed in ({k:v for k,v in prior.items() if k!='cleanup'}, {**prior,'cleanup':wrong_parent}, {**prior,'unexpected':None}):
                parent.helpers.return_value=changed
                with self.assertRaises(ValueError):e.helpers(ROOT)
        r,v,parent=parent_fixture()
        for key,bad in (('nonnegative_vs_pair_max',True),('candidate_full_pass_count',1)):
            changed=copy.deepcopy(r);changed['validation_summary']['gate_components'][key]=bad
            with self.assertRaises(ValueError):e.parent_contract(changed,v,parent,accepted)
        changed=copy.deepcopy(r)
        changed['validation_summary']['gate_components']['nonnegative_counts']['mean_ce']['passed']=65
        with self.assertRaises(ValueError):e.parent_contract(changed,v,parent,accepted)
        bad_envelope=copy.deepcopy(v);bad_envelope['timeout_cleanup_implementation']='C346-R0'
        with self.assertRaises(ValueError):e.parent_contract(r,bad_envelope,parent,accepted)

    def test_26_permanent_c272_provenance_seal_remains_outside_formal_state(self):
        # This value is a defined append-only historical invariant, not the current ACTIVE C.
        from fold_lm.v05_benchmarks import model_c272_query_boundaries as historical
        seal='89fd059a478b2190ecd03f8277aae2bafc7fcb12517897f56b4bd6cc89258604'
        self.assertEqual(historical.MANIFEST_SHA,seal)
        for path in ('docs/experiment-ledger-addendum-c272-preregistration.md',
                     'docs/experiment-ledger-addendum-c272-c273.md',
                     'docs/experiment-ledger-addendum-c273-preflight-recovery.md',
                     'docs/experiment-authoring-runtime-gate.md'):
            self.assertIn(seal,(ROOT/path).read_text(encoding='utf-8'))
        handoff=(ROOT/'docs/experiment-ledger-and-handoff.md').read_text(encoding='utf-8')
        formal=e.re.search(r'(?ms)^## Formal state\s+(.*?)(?=^## |\Z)',handoff)
        self.assertIsNotNone(formal)
        # Any future ACTIVE state may change. The immutable historical seal must survive it.
        self.assertIn(seal,handoff[:formal.start()]+handoff[formal.end():])


    def test_27_native_validate_executes_regression_once_then_closes_log_before_receipt(self):
        self.assertEqual(e.compile_import_own(ROOT),e.own_compile_inventory())
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()) as output:
            root=Path(tmp);folder=root/'runs/native-validate';calls=[];streams=[]
            pins={f'p{i}':'a' for i in range(s.SOURCE_COUNT)};inputs={f'i{i}':'b' for i in range(s.INPUT_COUNT)}
            class Cache:
                entries={};stats={'final_reference_rechecks':len(inputs)};sha=staticmethod(e.sha)
                def __init__(self,reference,lease_factory,*,progress,max_files):
                    self.assertion=max_files==len(inputs) and calls[-1]=='cleanup'
                    e.require(self.assertion,'cleanup before exact input lease capacity')
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release')
                def recheck(self):calls.append('reread');return [dict(path=k,sha256=v) for k,v in inputs.items()]
            base=NS(check_dependencies=lambda *a:calls.append('dependencies'))
            parent=NS(spec=lambda:NS(previous=lambda:NS(source=lambda:NS(base=lambda:base))))
            def runtime():calls.append('runtime');return NS(__version__='fixture'),NS(__version__='fixture')
            h=dict(parent=parent,cleanup=accepted,recovery=recovery,runtime=NS(native_runtime=runtime),
                locks=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None))
            def compile_own(repo):self.assertEqual(repo,root);calls.append('compile');return e.own_compile_inventory()
            def cleanup(*args):calls.append('cleanup');return accepted.timeout_preflight_expected(HEAD)
            def snapshot(*args):calls.append('snapshot');return {'validation_summary':{}},{},pins,inputs
            def semantics(*args):calls.append('parent');return None,None,()
            def regression(repo,args,path,phase):
                self.assertEqual((repo,path,phase),(root,folder/'regression.log','regression'))
                self.assertEqual(args[-2:],['--mode','regression']);calls.append('regression')
                e.save(folder/'regression-result.json',e.receipt(HEAD,s.FULL_TESTS));return 123
            def verified(*args):
                calls.append('proofs');return dict(tests=s.FULL_TESTS,modules=s.MODULES,plan_sha256='1'*64,evidence_sha256='2'*64,result_sha256='3'*64)
            real_text=e.ValidationText;real_sha=e.sha
            def transcript(live,retained):streams.append(retained);return real_text(live,retained)
            def observed_sha(path):
                if Path(path)==folder/'validation.log':self.assertTrue(streams and all(stream.closed for stream in streams))
                return real_sha(path)
            with patch.object(e,'guard'),patch.object(e,'compile_import_own',side_effect=compile_own), \
                 patch.object(e,'helpers',return_value=h),patch.object(e,'timeout_cleanup_preflight',side_effect=cleanup), \
                 patch.object(e,'snapshot',side_effect=snapshot),patch.object(e,'parent_semantics',side_effect=semantics), \
                 patch.object(e,'run_logged',side_effect=regression) as process,patch.object(e,'build_plan',return_value={}), \
                 patch.object(e,'verify_tests',side_effect=verified),patch.object(e,'ValidationText',side_effect=transcript), \
                 patch.object(e,'sha',side_effect=observed_sha),patch.object(s,'run_diagnostic') as diagnose:
                e.validate(root,folder,HEAD)
                self.assertEqual(calls,['compile','runtime','cleanup','snapshot','parent','dependencies','regression','proofs','reread','release'])
                self.assertEqual(process.call_count,1);diagnose.assert_not_called()
            saved=e.read(folder/'validation-receipt.json')
            e.validation_contract(saved,folder,HEAD,pins,inputs,accepted,saved['native_runtime']);e.ready_for_execution(folder,HEAD)
            log=(folder/'validation.log').read_text(encoding='utf-8')
            self.assertIn('authoring_runtime_preflight_complete = true',log)
            self.assertNotIn('authoring_runtime_preflight_receipt',log)
            self.assertIn('authoring_runtime_preflight_receipt',output.getvalue())
            self.assertEqual(saved['validation_log']['sha256'],e.sha(folder/'validation.log'))
            self.assertEqual(saved['validation_log']['serialized_bytes'],(folder/'validation.log').stat().st_size)

    def test_28_validation_contract_rejects_stale_incomplete_or_altered_attestation(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp);value=validation_fixture(folder);pins=value['source_blobs'];inputs=value['input_sha256']
            runtime=value['native_runtime'];e.validation_contract(value,folder,HEAD,pins,inputs,accepted,runtime)
            mutations=((('commit_sha',),'b'*40),(('run_folder',),str(folder/'other')),(('manifest_sha256',),'0'*64),
                (('status',),'FAIL'),(('source_blobs',),{}),(('input_sha256',),{}),(('source_count',),1),(('input_count',),1),
                (('compile_imports','own_tests'),1),(('regression','tests'),s.FULL_TESTS-1),(('regression','skipped'),1),
                (('regression_isolation','modules'),s.MODULES-1),(('final_reference_rechecks',),s.INPUT_COUNT-1),
                (('hash_stats','final_reference_rechecks'),s.INPUT_COUNT-1),(('parent_summary_sha256',),'0'*64),
                (('ancestor_semantic_reruns',),1),(('execution_revision',),'unreviewed'),
                (('timeout_cleanup_preflight','cleanup_ready'),False),(('native_runtime','python'),'different'),
                (('validation_log','file'),'regression.log'),(('validation_log','serialized_bytes'),0))
            for keys,bad in mutations:
                with self.subTest(keys=keys):
                    changed=copy.deepcopy(value);target=changed
                    for key in keys[:-1]:target=target[key]
                    target[keys[-1]]=bad
                    with self.assertRaises(ValueError):e.validation_contract(changed,folder,HEAD,pins,inputs,accepted,runtime)
            missing=copy.deepcopy(value);missing.pop('regression')
            for changed in (missing,{**value,'unexpected':True}):
                with self.assertRaises(ValueError):e.validation_contract(changed,folder,HEAD,pins,inputs,accepted,runtime)

    def test_29_validation_binds_all_proofs_and_log_and_rejects_other_run_folder(self):
        plan,base_hash=plan_fixture()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'BASE_IDS_SHA',base_hash),contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp);folder=root/'runs/one';folder.mkdir(parents=True)
            e.collect_tests(folder,HEAD,plan,recovery,lambda i,h:proof(folder,plan,i,h))
            tests=e.verify_tests(folder,HEAD,plan,recovery)
            log=folder/'validation.log';log.write_text('Explicit synthetic validation transcript.\n',encoding='utf-8')
            value=validation_fixture(folder,tests=tests)
            value['validation_log']=dict(file=log.name,sha256=e.sha(log),serialized_bytes=log.stat().st_size)
            e.save(folder/'validation-receipt.json',value)
            for name in ('regression.log','science.log','verify.log'):(folder/name).write_bytes(b'auxiliary fixture')
            h=dict(parent=NS(build_plan=lambda *a:{'groups':plan['groups'][:-2]}),prior={},recovery=recovery,cleanup=accepted)
            args=(root,folder,HEAD,h,value['source_blobs'],value['input_sha256'],value['native_runtime'],e.sha)
            saved,binding,closure=e.verify_validation(*args)
            self.assertEqual(saved,value);self.assertEqual(len(closure),s.manifest()['validation_retained_files'])
            self.assertEqual(binding['receipt_sha256'],e.sha(folder/'validation-receipt.json'))
            self.assertEqual(binding['log_sha256'],e.sha(log))
            self.assertEqual({Path(k).name for k in closure}&{'regression.log','science.log','verify.log'},set())
            e.ready_for_execution(folder,HEAD)
            for name in ('validation.log','regression-plan.json','module-244.log','module-000.json'):
                path=folder/name;original=path.read_bytes();path.write_bytes(original+b'changed')
                with self.assertRaises(ValueError):e.verify_validation(*args)
                path.write_bytes(original)
            other=root/'runs/two';shutil.copytree(folder,other)
            with self.assertRaises(ValueError):e.verify_validation(root,other,HEAD,h,value['source_blobs'],value['input_sha256'],value['native_runtime'],e.sha)
            with patch.object(e,'guard'),patch.object(e,'run_logged') as execute:
                with self.assertRaises(ValueError):e.run(root,other,HEAD)
                execute.assert_not_called()
            (folder/'validation-receipt.json').unlink()
            with patch.object(e,'guard'),patch.object(e,'run_logged') as execute:
                with self.assertRaises(FileNotFoundError):e.run(root,folder,HEAD)
                execute.assert_not_called()

    def test_30_validation_failure_preserves_local_log_without_receipt_or_execution(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp)
            for index,message in enumerate(('compile/import failure','regression proof failure','final input reread failure')):
                folder=root/f'runs/failure-{index}'
                with patch.object(e,'guard'),patch.object(e,'runtime_validation',side_effect=ValueError(message)), \
                     patch.object(s,'run_diagnostic') as diagnose:
                    with self.assertRaisesRegex(ValueError,message):e.validate(root,folder,HEAD)
                    diagnose.assert_not_called()
                self.assertFalse((folder/'validation-receipt.json').exists());self.assertFalse((folder/'science').exists())
                log=(folder/'validation.log').read_text(encoding='utf-8')
                self.assertIn('authoring_runtime_preflight_failure',log);self.assertIn(message,log)
                self.assertNotIn('authoring_runtime_preflight_complete',log)
                with patch.object(e,'guard'),patch.object(e,'runtime_validation') as work:
                    with self.assertRaises(FileExistsError):e.validate(root,folder,HEAD)
                    work.assert_not_called()
                with patch.object(e,'guard'),patch.object(e,'run_logged') as execute:
                    with self.assertRaises(FileNotFoundError):e.run(root,folder,HEAD)
                    execute.assert_not_called()

    def test_31_child_protection_counts_come_from_manifest_and_report_before_mismatch(self):
        manifest={**s.manifest(),'source_count':3,'input_count':5}
        with patch.object(s,'manifest',return_value=manifest),patch.object(s,'SOURCE_COUNT',99),patch.object(s,'INPUT_COUNT',98):
            self.assertEqual(e.protected_counts(),(3,5))
            for pins,inputs,message in (({'a':1,'b':2},{'i':1},'source protection'),
                                       ({'a':1,'b':2,'c':3},{'i':1},'input protection')):
                with contextlib.redirect_stdout(io.StringIO()) as output,self.assertRaisesRegex(ValueError,message):
                    e.report_protected_counts(pins,inputs)
                value=json.loads(output.getvalue().split(' = ',1)[1])
                self.assertEqual((value['source_pins'],value['protected_inputs']),(len(pins),len(inputs)))
                self.assertEqual((value['expected_source_pins'],value['expected_protected_inputs']),(3,5))
                self.assertEqual(value['actual_manifest_sha256'],s.digest(manifest))
            with contextlib.redirect_stdout(io.StringIO()):e.report_protected_counts(dict.fromkeys('abc'),dict.fromkeys('ijklm'))
        for bad in (0,True,'951'):
            with patch.object(s,'manifest',return_value={**manifest,'source_count':bad}):
                with self.assertRaises(ValueError):e.protected_counts()
        with tempfile.TemporaryDirectory() as tmp,patch.object(e,'guard'),patch.object(s,'MANIFEST_SHA','0'*64), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            root=Path(tmp);folder=root/'runs/unsealed'
            with self.assertRaisesRegex(ValueError,'C347 manifest seal'):e.validate(root,folder,HEAD)
            value=json.loads(output.getvalue().split(' = ',1)[1])
            self.assertEqual(value,dict(actual_manifest_sha256=s.digest(s.manifest()),expected_manifest_sha256='0'*64))
            self.assertFalse(folder.exists())

    def test_32_real_powershell_native_validation_failure_cannot_publish_or_run_science(self):
        pwsh=shutil.which('pwsh')
        self.assertIsNotNone(pwsh,'PowerShell is required for the native launcher fixture; put installed pwsh on PATH')
        source=(ROOT/'tools/invoke_c347.ps1').read_text(encoding='utf-8')
        dependency="$Python = Join-Path $Root '.venv-py31315\\Scripts\\python.exe'"
        self.assertEqual(source.count(dependency),1)
        fixture=source.replace(dependency,"$Python = Join-Path $Root 'fixture-native.ps1'")
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'tools').mkdir();(root/'docs').mkdir()
            (root/'tools/invoke_c347.ps1').write_text(fixture,encoding='utf-8')
            (root/'tools/c347_execution.py').write_text('# fixture dependency only\n',encoding='utf-8')
            for name,marker in (('run_c347.ps1','runner-called'),('publish_experiment_log.ps1','publisher-called')):
                (root/'tools'/name).write_text("Set-Content -LiteralPath (Join-Path (Split-Path -Parent $PSScriptRoot) '"+marker+"') -Value 'unexpected'\n",encoding='utf-8')
            (root/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC347 ACTIVE / NOT YET JUDGED\n',encoding='utf-8')
            (root/'fixture-native.ps1').write_text("""$payload = ConvertTo-Json -InputObject @($args) -Compress
Set-Content -LiteralPath (Join-Path $PSScriptRoot 'native-args.json') -Value $payload -Encoding UTF8
Write-Output 'NATIVE_VALIDATE_STUB_ENTERED'
$global:LASTEXITCODE = 7
""",encoding='utf-8')
            (root/'harness.ps1').write_text("""$ErrorActionPreference = 'Stop'
function global:git {
    $global:LASTEXITCODE = 0
    switch (($args -join ' ')) {
        'branch --show-current' { 'feat/sft-target-loss'; return }
        'rev-parse HEAD' { 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'; return }
        'status --porcelain --untracked-files=no' { return }
        default { throw ('unexpected fixture git command: ' + ($args -join ' ')) }
    }
}
& (Join-Path $PSScriptRoot 'tools/invoke_c347.ps1') -ExpectedHead 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
""",encoding='utf-8')
            result=subprocess.run([pwsh,'-NoLogo','-NoProfile','-NonInteractive','-File',str(root/'harness.ps1')],
                cwd=root,capture_output=True,text=True,encoding='utf-8',timeout=60)
            self.assertEqual(result.returncode,0,(result.stdout,result.stderr))
            for marker in ('NATIVE_VALIDATE_STUB_ENTERED','invocation_skipped = AUTHORING_RUNTIME_PREFLIGHT_FAILED',
                           'experiment_executed = False','execution_log_publish_attempted = False'):
                self.assertIn(marker,result.stdout)
            actual=json.loads((root/'native-args.json').read_text(encoding='utf-8-sig'))
            self.assertEqual(actual[actual.index('--mode')+1],'validate')
            self.assertEqual(actual[actual.index('--expected-head')+1],HEAD)
            self.assertEqual(actual[actual.index('--root')+1],str(root))
            self.assertFalse((root/'runner-called').exists());self.assertFalse((root/'publisher-called').exists())
            self.assertEqual(list((root/'runs').glob('*.log')),[])


if __name__=='__main__':unittest.main()
