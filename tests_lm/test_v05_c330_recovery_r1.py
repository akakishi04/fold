"""C330 R1 execution-isolation tests; synthetic inventories are not full regression."""
from __future__ import annotations
import contextlib
import copy
import hashlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

ROOT=Path(__file__).resolve().parents[1]
loader=importlib.util.spec_from_file_location('_c330_r1_tests',ROOT/'tools/c330_recovery_r1.py')
r=importlib.util.module_from_spec(loader); loader.loader.exec_module(r)
HEAD='a'*40


def synthetic_plan(first=None):
    groups=[]
    if first is not None: groups.append(copy.deepcopy(first))
    remaining=r.BASE_TESTS-sum(len(g['test_ids']) for g in groups)
    count=r.MODULES-1-len(groups)
    quotient,remainder=divmod(remaining,count)
    for index in range(count):
        module=f'tests_lm._r1_fixture_{index:03d}'
        ids=[f'{module}.Fixture.test_{i:03d}' for i in range(quotient+(index<remainder))]
        groups.append(dict(module=module,test_ids=ids))
    groups.append(dict(module=r.TEST_MODULE,test_ids=[r.TEST_MODULE+f'.Fixture.test_{i:03d}' for i in range(r.OWN_TESTS)]))
    value=dict(schema='fold-c330-r1-regression-plan-v1',commit_sha=HEAD,recovery_sha256=r.RECOVERY_SHA,
        policy=r.POLICY,test_ids_sha256=r.digest([tid for g in groups for tid in g['test_ids']]),groups=groups)
    r.validate_plan(value,HEAD)
    return value


def passed(ids):
    return dict(tests=len(ids),failures=0,errors=0,skipped=0,expected_failures=0,unexpected_successes=0,
                successful=True,started_ids=list(ids),success_ids=list(ids))


def write_module_evidence(folder,plan,index,plan_sha):
    group=plan['groups'][index]; pid=20000+index
    r.save(folder/f'module-{index:03d}.json',dict(schema='fold-c330-r1-module-v1',commit_sha=HEAD,
        plan_sha256=plan_sha,index=index,module=group['module'],pid=pid,result=passed(group['test_ids'])))
    (folder/f'module-{index:03d}.log').write_text('synthetic module receipt; no tests executed\n',encoding='utf-8')
    return pid


@contextlib.contextmanager
def temporary_module(source):
    import tests_lm
    name='tests_lm._c330_r1_temporary'
    module=types.ModuleType(name); module.__dict__['unittest']=unittest
    exec(compile(source,'<explicit test fixture>','exec'),module.__dict__)
    with patch.dict(sys.modules,{name:module}),patch.object(tests_lm,'_c330_r1_temporary',module,create=True):
        yield name


def git_fixture(root):
    subprocess.run(['git','init','-q',str(root)],check=True)
    for args in [('checkout','-qb','feat/sft-target-loss'),('config','user.name','C330 R1 fixture'),('config','user.email','r1@example.invalid')]:
        subprocess.run(['git','-C',str(root),*args],check=True,capture_output=True)
    (root/'docs').mkdir(); (root/'docs/experiment-ledger-and-handoff.md').write_text('## Formal state\nC330 ACTIVE / INVALID ATTEMPT RECOVERY\n',encoding='utf-8')
    subprocess.run(['git','-C',str(root),'add','.'],check=True)
    subprocess.run(['git','-C',str(root),'commit','-qm','synthetic fixture'],check=True)
    return r.git(root,'rev-parse','HEAD')


class C330R1Tests(unittest.TestCase):
    def test_01_contract_seal_and_tamper(self):
        r.seal()
        with patch.object(r,'POLICY','changed'),self.assertRaises(ValueError):r.seal()
    def test_02_additive_counts_and_actual_loader(self):
        self.assertEqual(r.FULL_TESTS,r.BASE_TESTS+r.OWN_TESTS)
        self.assertEqual(r.SOURCE_COUNT,838+len(r.OWN)); self.assertEqual(r.INPUT_COUNT,1593+len(r.OWN))
        self.assertEqual(unittest.defaultTestLoader.loadTestsFromName(r.TEST_MODULE).countTestCases(),32)
        self.assertEqual(r.contract()['module_retries'],0)
    def test_03_partition_preserves_exact_order(self):
        def case(module,tid):
            cls=type('Fixture',(unittest.TestCase,),{'__module__':module,'id':lambda self:tid})
            return cls()
        tests=[case('tests_lm.a','tests_lm.a.C.x'),case('tests_lm.a','tests_lm.a.C.y'),case('tests_lm.b','tests_lm.b.D.z')]
        groups=r.partition(tests)
        self.assertEqual([g['module'] for g in groups],['tests_lm.a','tests_lm.b'])
        self.assertEqual([tid for g in groups for tid in g['test_ids']],[t.id() for t in tests])
    def test_04_partition_rejects_duplicate_and_noncontiguous(self):
        def case(module,tid):
            return type('Fixture',(unittest.TestCase,),{'__module__':module,'id':lambda self:module+'.C.'+tid})()
        for tests in ([case('tests_lm.a','x')]*2,[case('tests_lm.a','x'),case('tests_lm.b','x'),case('tests_lm.a','y')]):
            with self.subTest(),self.assertRaises(ValueError):r.partition(tests)
    def test_05_plan_complete_counts_and_tamper(self):
        value=synthetic_plan()
        for kind in ('missing','duplicate','hash','policy','own'):
            v=copy.deepcopy(value)
            if kind=='missing':v['groups'].pop(0)
            elif kind=='duplicate':v['groups'][0]['test_ids'][1]=v['groups'][0]['test_ids'][0]
            elif kind=='hash':v['test_ids_sha256']='0'*64
            elif kind=='policy':v['policy']='retry-until-pass'
            else:v['groups'][-1]['module']='tests_lm._different'
            with self.subTest(kind=kind),self.assertRaises(ValueError):r.validate_plan(v,HEAD)
    def test_06_real_unittest_execution_success_ids(self):
        with temporary_module('class C(unittest.TestCase):\n def test_a(self): self.assertTrue(True)\n def test_b(self): self.assertEqual(2,2)\n') as module,contextlib.redirect_stderr(io.StringIO()):
            ids=[module+'.C.test_a',module+'.C.test_b']; value=r.execute_module(module,ids)
            r.check_module(value,{'test_ids':ids}); self.assertEqual(value['tests'],2)
    def test_07_real_failure_is_never_success(self):
        with temporary_module('class C(unittest.TestCase):\n def test_a(self): self.fail("intentional fixture")\n') as module,contextlib.redirect_stderr(io.StringIO()):
            ids=[module+'.C.test_a']; value=r.execute_module(module,ids)
            self.assertEqual(value['failures'],1)
            with self.assertRaises(ValueError):r.check_module(value,{'test_ids':ids})
    def test_08_setupclass_error_zero_started_not_complete(self):
        source='class C(unittest.TestCase):\n @classmethod\n def setUpClass(cls): raise RuntimeError("fixture setup failure")\n def test_a(self): pass\n'
        with temporary_module(source) as module,contextlib.redirect_stderr(io.StringIO()):
            ids=[module+'.C.test_a']; value=r.execute_module(module,ids)
            self.assertEqual(value['started_ids'],[]); self.assertGreater(value['errors'],0)
            with self.assertRaises(ValueError):r.check_module(value,{'test_ids':ids})
    def test_09_skipped_tests_are_not_successful_completion(self):
        source='class C(unittest.TestCase):\n @unittest.skip("fixture")\n def test_a(self): pass\n'
        with temporary_module(source) as module,contextlib.redirect_stderr(io.StringIO()):
            ids=[module+'.C.test_a']; value=r.execute_module(module,ids)
            self.assertEqual(value['skipped'],1)
            with self.assertRaises(ValueError):r.check_module(value,{'test_ids':ids})
    def test_10_unexpected_loader_ids_block_execution(self):
        with temporary_module('class C(unittest.TestCase):\n def test_a(self): raise AssertionError("must not execute")\n') as module:
            with self.assertRaisesRegex(ValueError,'loader differs'):r.execute_module(module,[module+'.C.wrong'])
    def test_11_boolean_counts_and_forged_success_rejected(self):
        ids=['tests_lm.a.C.test_a']; value=passed(ids)
        for key,bad in [('tests',True),('started_ids',[]),('success_ids',[]),('expected_failures',1),('successful',1)]:
            row=copy.deepcopy(value); row[key]=bad
            with self.subTest(key=key),self.assertRaises(ValueError):r.check_module(row,{'test_ids':ids})
    def test_12_expected_failure_not_silently_converted_to_pass(self):
        source='class C(unittest.TestCase):\n @unittest.expectedFailure\n def test_a(self): self.fail("expected fixture failure")\n'
        with temporary_module(source) as module,contextlib.redirect_stderr(io.StringIO()):
            ids=[module+'.C.test_a']; value=r.execute_module(module,ids)
            self.assertEqual(value['expected_failures'],1)
            with self.assertRaises(ValueError):r.check_module(value,{'test_ids':ids})
    def test_13_collector_and_fresh_evidence_reconstruction(self):
        plan=synthetic_plan()
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp); calls=[]
            def execute(index,plan_sha):calls.append(index); return write_module_evidence(folder,plan,index,plan_sha)
            value=r.collect_regression(folder,folder,HEAD,plan,execute)
            self.assertEqual(calls,list(range(r.MODULES))); self.assertEqual(value['tests'],r.FULL_TESTS)
            evidence=r.verify_regression(folder,HEAD,plan)
            self.assertEqual(evidence['modules'],r.MODULES); self.assertEqual(evidence['tests'],r.FULL_TESTS)
    def test_14_native_style_nonzero_stops_at_first_attempt(self):
        plan=synthetic_plan(); calls=[]
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp)
            def execute(index,plan_sha):
                calls.append(index)
                if index==1:raise ValueError('0xC0000005 fixture, no retry')
                return write_module_evidence(folder,plan,index,plan_sha)
            with self.assertRaises(ValueError):r.collect_regression(folder,folder,HEAD,plan,execute)
            self.assertEqual(calls,[0,1]); self.assertFalse((folder/'regression-result.json').exists())
    def test_15_tampered_module_log_breaks_fresh_verification(self):
        plan=synthetic_plan()
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp); r.collect_regression(folder,folder,HEAD,plan,lambda i,h:write_module_evidence(folder,plan,i,h))
            (folder/'module-000.log').write_text('changed',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'receipt/log bytes'):r.verify_regression(folder,HEAD,plan)
    def test_16_plan_content_cannot_drop_tests_after_execution(self):
        plan=synthetic_plan()
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp); r.collect_regression(folder,folder,HEAD,plan,lambda i,h:write_module_evidence(folder,plan,i,h))
            (folder/'regression-plan-r1.json').write_text('{}',encoding='utf-8')
            with self.assertRaises(ValueError):r.verify_regression(folder,HEAD,plan)
    def test_17_mismatched_pid_or_incomplete_success_aborts(self):
        plan=synthetic_plan()
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp)
            def execute(index,h):return write_module_evidence(folder,plan,index,h)+1
            with self.assertRaisesRegex(ValueError,'process identity'):r.collect_regression(folder,folder,HEAD,plan,execute)
            self.assertFalse((folder/'regression-isolation-r1.json').exists())
    def test_18_real_process_error_preserved_and_not_retried(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp); log=root/'native-fixture.log'
            with self.assertRaises(ValueError):r.run_logged(root,[sys.executable,'-c','import sys; print("fixture failure",flush=True); sys.exit(7)'],log,'fixture')
            self.assertIn('fixture failure',log.read_text(encoding='utf-8'))
    def test_19_new_process_does_not_inherit_previous_interpreter_globals(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp)
            first='import builtins; builtins._c330_r1_fixture=True; print("mutated only this process")'
            second='import builtins; assert not hasattr(builtins,"_c330_r1_fixture"); print("fresh")'
            p1=r.run_logged(root,[sys.executable,'-c',first],root/'a.log','first')
            p2=r.run_logged(root,[sys.executable,'-c',second],root/'b.log','second')
            self.assertGreater(p1,0); self.assertGreater(p2,0); self.assertIn('fresh',(root/'b.log').read_text(encoding='utf-8'))
    def test_20_strict_json_and_exclusive_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'data'; r.save(path,{'名前':'甲乙'}); self.assertEqual(r.read(path),{'名前':'甲乙'})
            with self.assertRaises(FileExistsError):r.save(path,{})
            for value in ('{"a":1,"a":2}','NaN','Infinity'):
                path.write_text(value,encoding='utf-8')
                with self.subTest(),self.assertRaises(ValueError):r.read(path)
    def test_21_real_git_active_recovery_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); head=git_fixture(root); r.guard(root,head)
            with self.assertRaises(ValueError):r.guard(root,HEAD)
            (root/'docs/experiment-ledger-and-handoff.md').write_text('changed',encoding='utf-8')
            with self.assertRaises(ValueError):r.guard(root,head)
    def test_22_source_lf_crlf_and_tampering(self):
        raw=b'a\nb\n'; oid=hashlib.sha1(b'blob 4\0'+raw).hexdigest()
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'x'
            for value in (raw,raw.replace(b'\n',b'\r\n')):path.write_bytes(value); r.source_bytes(path,oid)
            path.write_bytes(b'bad')
            with self.assertRaises(ValueError):r.source_bytes(path,oid)
    def test_23_all_three_new_sources_and_inputs_extend_old_unions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); tree={}; pins={f'old{i}':'a'*40 for i in range(838)}; inputs={f'oldinput{i}':'b'*64 for i in range(1593)}
            for name in r.OWN:
                path=root/name; path.parent.mkdir(parents=True,exist_ok=True); data=('fixture '+name).encode(); path.write_bytes(data)
                tree[name]=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            canonical=lambda path:str(path.resolve())
            a,b=r.extend_protection(root,pins,inputs,NS(tree_blobs=lambda root:tree),r.sha,canonical)
            self.assertEqual(len(a),841); self.assertEqual(len(b),1596); self.assertEqual(len(pins),838)
            self.assertTrue(all(a[k]==v for k,v in pins.items())); self.assertTrue(all(b[k]==v for k,v in inputs.items()))
    def test_24_child_module_mode_uses_one_actual_module_not_whole_suite(self):
        source='class C(unittest.TestCase):\n def test_a(self): self.assertEqual(3,3)\n'
        with temporary_module(source) as module,tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            folder=Path(tmp); group=dict(module=module,test_ids=[module+'.C.test_a']); plan=synthetic_plan(group)
            r.save(folder/'regression-plan-r1.json',plan)
            with patch.object(r,'guard'),patch.object(r,'build_plan',side_effect=AssertionError('module must not load all modules')):
                r.module_child(folder,folder,HEAD,0,r.sha(folder/'regression-plan-r1.json'))
            value=r.read(folder/'module-000.json'); self.assertEqual(value['result']['success_ids'],group['test_ids'])
    def test_25_real_cli_mode_and_output_path_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            p=subprocess.run([sys.executable,str(ROOT/'tools/c330_recovery_r1.py'),'--folder',str(root),'--expected-head',HEAD,'--mode','invalid'],capture_output=True,text=True,encoding='utf-8')
            self.assertNotEqual(p.returncode,0); self.assertIn('invalid choice',p.stderr)
    def test_26_run_controller_order_and_no_retry(self):
        for bad in (False,True):
            with tempfile.TemporaryDirectory() as tmp,patch.object(r,'guard'),patch.object(r,'run_logged',side_effect=ValueError('fixture') if bad else None,return_value=1) as runner,contextlib.redirect_stdout(io.StringIO()) as output:
                root=Path(tmp)
                if bad:
                    with self.assertRaises(ValueError):r.run(root,root/'runs/x',HEAD)
                    self.assertEqual(runner.call_count,1); self.assertIn('run_execution_valid = false',output.getvalue())
                else:
                    r.run(root,root/'runs/x',HEAD); self.assertEqual([call.args[-1] for call in runner.call_args_list],['science','verify'])
    def test_27_production_worker_keeps_diagnostic_not_capability(self):
        self.worker_fixture(False)
    def test_28_production_worker_stops_before_diagnosis_on_regression_failure(self):
        self.worker_fixture(True)
    def worker_fixture(self,bad):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            root=Path(tmp); folder=root/'runs/x'; folder.mkdir(parents=True); calls=[]
            pins={f'p{i}':'a'*40 for i in range(r.SOURCE_COUNT)}; inputs={str(root/f'i{i}'):'b'*64 for i in range(r.INPUT_COUNT)}
            class Cache:
                entries={}; stats={'final_reference_rechecks':r.INPUT_COUNT}
                sha=staticmethod(r.sha)
                def __init__(self,*a,**kw):pass
                def __enter__(self):return self
                def __exit__(self,*a):calls.append('release')
                def recheck(self):calls.append('final'); return [{'path':k,'sha256':v} for k,v in inputs.items()]
            r4=NS(WinAPI=lambda:None,lock_probe=lambda *a:{'synthetic':True},LockedHashes=Cache,ReadLease=None)
            cx=(NS(guarded=NS(no_neural=contextlib.nullcontext)),); b=NS(context=lambda:cx,check_dependencies=lambda *a:None,peak_rss=lambda:1)
            summary=dict(parent_candidate_gate=False,parent_paired_success_count=1,seed_results=[],strata=[],transition_summary=[])
            outputs=('a.json','b.json','c.json','d.json')
            def artifacts(out):return [dict(file=name,sha256=r.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in outputs]
            def diagnose(out,*args):
                calls.append('diagnose')
                for name in outputs:r.save(out/name,{'synthetic':True})
                return summary
            def reconstruct(*args):calls.append('saved'); return summary
            def bound(out,call):return call(),artifacts(out)
            s=NS(parent=lambda:NS(base=lambda:b),run_diagnostic=diagnose,semantic_recheck=reconstruct,check_summary=lambda value:None,
                EXPERIMENT_ID='synthetic',STAGE='synthetic',MANIFEST_SHA=r.BASE_MANIFEST,WORK={'model_forward_calls':0})
            runtime=NS(__version__='synthetic')
            def snapshot(*args):calls.append('snapshot'); return {'validation_summary':{'candidate_gate':False,'paired_success_count':1}},{},pins,inputs
            base=NS(spec=lambda:s,helpers=lambda root:(NS(),NS(),NS(),NS(native_runtime=lambda:(runtime,runtime)),NS(),r4,NS()),snapshot=snapshot,
                canonical=lambda p:str(p.resolve()),parent_semantics=lambda *args:calls.append('parent'),PARENT_FOLDER='synthetic-parent',
                PARENT_SUMMARY='c'*64,PARENT_ENVELOPE='d'*64,bound_semantics=bound,artifacts=artifacts)
            def regression(*args):
                calls.append('tests')
                if bad:raise ValueError('fixture native crash')
                r.save(folder/'regression-result.json',dict(commit_sha=HEAD,tests=r.FULL_TESTS,failures=0,errors=0,skipped=0,successful=True))
            with patch.object(r,'guard'),patch.object(r,'load_base',return_value=base),patch.object(r,'extend_protection',return_value=(pins,inputs)),patch.object(r,'run_logged',side_effect=regression),patch.object(r,'build_plan',return_value={}),patch.object(r,'verify_regression',return_value={'synthetic':True}):
                if bad:
                    with self.assertRaises(ValueError):r.scientific_worker(root,folder,HEAD)
                    self.assertNotIn('diagnose',calls)
                else:
                    r.scientific_worker(root,folder,HEAD)
                    self.assertEqual(calls,['snapshot','parent','tests','diagnose','saved','final','release'])
                    value=r.read(folder/'science/summary.json'); self.assertEqual(value['status'],'PASS'); self.assertFalse(value['capability_gate_applicable'])
                    self.assertEqual(value['execution_revision'],'C330-R1')
    def test_29_runner_route_and_unchanged_science_pins(self):
        text=(ROOT/'tools/run_c330.ps1').read_text(encoding='utf-8')
        self.assertIn('c330_recovery_r1.py',text); self.assertIn('--expected-head $ExpectedHead',text)
        self.assertEqual(r.MODEL_BLOB,'73c30cba137b4d11a9ac39c8f3702bdd0b2e6baf')
        self.assertEqual(r.BASE_BLOB,'1fb5fb47e1e9998cd8ec3a38b25afeb7ec44b31a')
    def test_30_module_plan_hash_tamper_prevents_test_execution(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(r,'guard'),patch.object(r,'execute_module') as execute:
            folder=Path(tmp); r.save(folder/'regression-plan-r1.json',synthetic_plan())
            with self.assertRaises(ValueError):r.module_child(folder,folder,HEAD,0,'0'*64)
            execute.assert_not_called()
    def test_31_module_setup_and_teardown_stay_inside_one_process(self):
        source='events=[]\ndef setUpModule(): events.append("module-up")\ndef tearDownModule(): events.append("module-down")\nclass C(unittest.TestCase):\n @classmethod\n def setUpClass(cls): events.append("class-up")\n @classmethod\n def tearDownClass(cls): events.append("class-down")\n def test_a(self): events.append("a")\n def test_b(self): events.append("b")\n'
        with temporary_module(source) as module,contextlib.redirect_stderr(io.StringIO()):
            ids=[module+'.C.test_a',module+'.C.test_b']; result=r.execute_module(module,ids); r.check_module(result,{'test_ids':ids})
            self.assertEqual(sys.modules[module].events,['module-up','class-up','a','b','class-down','module-down'])
    def test_32_resealed_forged_module_receipt_still_rejected(self):
        plan=synthetic_plan()
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            folder=Path(tmp); r.collect_regression(folder,folder,HEAD,plan,lambda i,h:write_module_evidence(folder,plan,i,h))
            path=folder/'module-000.json'; record=r.read(path); record['result']['success_ids'].pop(); path.write_bytes(r.blob(record))
            ep=folder/'regression-isolation-r1.json'; evidence=r.read(ep); evidence['modules'][0]['receipt_sha256']=r.sha(path); ep.write_bytes(r.blob(evidence))
            with self.assertRaisesRegex(ValueError,'execute and pass'):r.verify_regression(folder,HEAD,plan)


if __name__=='__main__':unittest.main()
