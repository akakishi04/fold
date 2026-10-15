"""R6 authoring tests; synthetic workers are not native scientific executions."""
import ast
import contextlib
import hashlib
import importlib.util
import inspect
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('r6_tested', ROOT/'tools/c324_scientific_recovery_r6.py')
b = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(b)
HEAD = 'a'*40

def oid(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

def encoding(v):
    return repr(v).encode('utf-8')

def fake_evidence(root):
    folder = root/'docs/experiment-run-logs/c324'; folder.mkdir(parents=True)
    receipt = dict(reference_recheck_completed=True, snapshot_files=1486,
                   hash_stats=dict(final_reference_rechecks=1486),
                   verifier_stats={str(i):dict(executions=1, failures=0, reused=9 if i==0 else 0) for i in range(7)})
    report = dict(commit_sha=b.R5_EXECUTION, role='C324-R5-VERIFIED-SESSION-QUALIFICATION',
                  diagnostic_completed=True, scientific_training_steps=0,
                  worker=dict(returncode=0,timed_out=False,parent_validation_completed=True,worker_result=receipt))
    def write():
        log=folder/'latest.log';log.write_text('diagnostic_report = '+json.dumps(report)+'\n',encoding='utf-8')
        h=b.sha(log)
        (folder/'latest.json').write_text(json.dumps(dict(experiment_id='C324',execution_head=b.R5_EXECUTION,
                              log_sha256=h,log_bytes=log.stat().st_size)),encoding='utf-8')
        return h
    return report,write

class Dummy:
    def __init__(self,name):self.name=name
    def id(self):return self.name
    def __call__(self,result):pass
    def countTestCases(self):return 1

class R6Tests(unittest.TestCase):
    def test_01_source_lf(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_bytes(b'a\nb\n');self.assertEqual(b.source_bytes(p,oid(p.read_bytes())),p.read_bytes())
    def test_02_source_crlf(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_bytes(b'a\r\nb\r\n');self.assertEqual(b.source_bytes(p,oid(b'a\nb\n')),p.read_bytes())
    def test_03_mixed_line_endings_not_silent(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_bytes(b'a\r\nb\n')
            with self.assertRaises(ValueError):b.source_bytes(p,oid(b'a\nb\n'))
    def test_04_source_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_bytes(b'changed')
            with self.assertRaises(ValueError):b.source_bytes(p,oid(b'original'))
    def test_05_duplicate_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_text('{"x":1,"x":2}',encoding='utf-8')
            with self.assertRaises(ValueError):b.read(p)
    def test_06_nonfinite_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_text('{"x":NaN}',encoding='utf-8')
            with self.assertRaises(ValueError):b.read(p)
    def test_07_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';b.save(p,{})
            with self.assertRaises(FileExistsError):b.save(p,{})
    def test_08_unicode_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';v={'日本語':True};b.save(p,v);self.assertEqual(b.read(p),v)
    def test_09_batch_parser_binary_and_newline(self):
        raw=b'a\0b\nc';h=oid(raw);data=h.encode()+b' blob 5\n'+raw+b'\n'
        self.assertEqual(b.GitBatch.parse(data,[h]),{h:raw})
    def test_10_batch_wrong_oid(self):
        with self.assertRaises(ValueError):b.GitBatch.parse(b'b'*40+b' blob 1\na\n',['a'*40])
    def test_11_batch_bad_framing(self):
        h=oid(b'a')
        with self.assertRaises(ValueError):b.GitBatch.parse(h.encode()+b' blob 1\naX',[h])
    def test_12_batch_trailing_payload(self):
        h=oid(b'a')
        with self.assertRaises(ValueError):b.GitBatch.parse(h.encode()+b' blob 1\na\nextra',[h])
    def test_13_batch_digest_mismatch(self):
        h=oid(b'a')
        with self.assertRaises(ValueError):b.GitBatch.parse(h.encode()+b' blob 1\nz\n',[h])
    def test_14_real_git_batch(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);subprocess.run(['git','init','-q',d],check=True)
            p=root/'a b.py';p.write_bytes(b'hello\n');subprocess.run(['git','-C',d,'add','.'],check=True)
            subprocess.run(['git','-C',d,'-c','user.name=fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture'],check=True)
            h=b.git(root,'rev-parse','HEAD:a b.py');batch=b.GitBatch(root,{'a b.py':h})
            self.assertEqual(batch.blobs[h],p.read_bytes())
    def batch(self):
        x=object.__new__(b.GitBatch);x.root=ROOT.resolve();x.pins={'x':'a'*40};x.blobs={'a'*40:b'bytes\n'};x.hits=0;return x
    def test_15_text_git_reply(self):
        x=self.batch();original=Mock();self.assertEqual(x.wrap(original,False)(ROOT,'rev-parse','HEAD:x'),'a'*40);original.assert_not_called()
    def test_16_binary_git_reply(self):
        x=self.batch();self.assertEqual(x.wrap(Mock(),True)(ROOT,'rev-parse','HEAD:x'),b'a'*40+b'\n')
    def test_17_cat_file_preserves_bytes(self):
        x=self.batch();self.assertEqual(x.wrap(Mock(),True)(ROOT,'cat-file','blob','a'*40),b'bytes\n')
    def test_18_unknown_git_command_delegates(self):
        x=self.batch();original=Mock(return_value='native');self.assertEqual(x.wrap(original,False)(ROOT,'status'),'native');original.assert_called_once()
    def test_19_other_repository_delegates(self):
        x=self.batch();original=Mock(return_value='native');self.assertEqual(x.wrap(original,False)(ROOT.parent,'rev-parse','HEAD:x'),'native')
    def parent(self):
        return b.ParentData([ROOT],({'p':1},{'TRAIN':[]},{'old':[]},{'new':[]}),Mock(),encoding)
    def test_20_parent_first_copy_isolated(self):
        x=self.parent();v=x.load([ROOT]);v[1]['TRAIN'].append(1);self.assertEqual(x.load([ROOT])[1]['TRAIN'],[])
    def test_21_parent_hit_copy_isolated(self):
        x=self.parent();x.load([ROOT]);v=x.load([ROOT]);v[2]['old'].append(1);self.assertEqual(x.load([ROOT])[2]['old'],[])
    def test_22_different_parent_request_rejected(self):
        x=self.parent()
        with self.assertRaises(ValueError):x.load([ROOT.parent])
    def test_23_closed_data_rejected(self):
        x=self.parent();x.close()
        with self.assertRaises(ValueError):x.load([ROOT])
    def test_24_lease_guard_always_runs(self):
        x=self.parent();x.load([ROOT]);x.check.side_effect=ValueError('changed')
        with self.assertRaises(ValueError):x.load([ROOT])
        self.assertEqual(x.calls,1)
    def test_25_stored_parent_mutation_rejected(self):
        x=self.parent();x.value[0]['p']=99
        with self.assertRaises(ValueError):x.load([ROOT])
    def test_26_parent_non_json_contract_rejected(self):
        with self.assertRaises(ValueError):b.ParentData([ROOT],({},[],{},{}),Mock(),encoding)
    def test_27_parent_generator_supported(self):
        x=self.parent();self.assertEqual(x.load(iter([ROOT]))[0],{'p':1})
    def test_28_count_read_not_reconstruction(self):
        x=self.parent();[x.load([ROOT]) for _ in range(3)];self.assertEqual(x.calls,3)
    def test_29_parent_read_does_not_consume_rng(self):
        import random
        x=self.parent();before=random.getstate();x.load([ROOT]);self.assertEqual(random.getstate(),before)
    def test_30_repository_guard(self):
        with patch.object(b,'git',side_effect=[b.BRANCH,HEAD,'']):b.guard(ROOT,HEAD)
    def test_31_repository_drift_rejected(self):
        for values in (['wrong'],[b.BRANCH,'b'*40],[b.BRANCH,HEAD,'dirty']):
            with patch.object(b,'git',side_effect=values),self.assertRaises(ValueError):b.guard(ROOT,HEAD)
    def test_32_successful_r5_required(self):
        with tempfile.TemporaryDirectory() as d:
            r,w=fake_evidence(Path(d));h=w()
            with patch.object(b,'R5_LOG_SHA',h):self.assertEqual(b.prerequisite(Path(d)),r)
    def test_33_r5_tamper_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);r,w=fake_evidence(root);h=w();(root/'docs/experiment-run-logs/c324/latest.log').write_bytes(b'bad')
            with patch.object(b,'R5_LOG_SHA',h),self.assertRaises(ValueError):b.prerequisite(root)
    def test_34_incomplete_r5_not_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);r,w=fake_evidence(root);r['worker']['worker_result']['reference_recheck_completed']=False;h=w()
            with patch.object(b,'R5_LOG_SHA',h),self.assertRaises(ValueError):b.prerequisite(root)
    def test_35_missing_verifier_not_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);r,w=fake_evidence(root);r['worker']['worker_result']['verifier_stats'].pop('0');h=w()
            with patch.object(b,'R5_LOG_SHA',h),self.assertRaises(ValueError):b.prerequisite(root)
    def receipt(self):return dict(tests=5490,failures=0,errors=0,skipped=0,successful=True,commit_sha=HEAD)
    def test_36_regression_receipt(self):b.validate_regression(self.receipt(),HEAD)
    def test_37_regression_failures_rejected(self):
        for name,value in (('failures',1),('errors',1),('skipped',1),('successful',False),('commit_sha','wrong')):
            r=self.receipt();r[name]=value
            with self.assertRaises(ValueError):b.validate_regression(r,HEAD)
    def test_38_old_test_count_not_full_r6(self):
        r=self.receipt();r['tests']=5357
        with self.assertRaises(ValueError):b.validate_regression(r,HEAD)
    def suite_fixture(self,duplicate=False,excluded=False):
        base=[Dummy('base.'+str(i)) for i in range(5357)]
        if excluded:base[0]=Dummy('excluded')
        c=NS(regression_suite=lambda root:unittest.TestSuite(base),regression_modules=lambda root:list(range(210)),EXCLUDED='excluded')
        extras=[unittest.TestSuite(Dummy(('base.0' if duplicate and i==0 and j==0 else f'extra.{i}.{j}')) for j in range(n)) for i,n in enumerate(b.RECOVERY_COUNTS)]
        return c,extras
    def test_39_full_suite_counts_semantically(self):
        c,extras=self.suite_fixture()
        with patch.object(unittest.defaultTestLoader,'loadTestsFromName',side_effect=extras):
            self.assertEqual(b.combined_suite(c,ROOT).countTestCases(),5490)
    def test_40_duplicate_test_rejected(self):
        c,extras=self.suite_fixture(duplicate=True)
        with patch.object(unittest.defaultTestLoader,'loadTestsFromName',side_effect=extras),self.assertRaises(ValueError):b.combined_suite(c,ROOT)
    def test_41_old_exclusion_preserved(self):
        c,extras=self.suite_fixture(excluded=True)
        with patch.object(unittest.defaultTestLoader,'loadTestsFromName',side_effect=extras),self.assertRaises(ValueError):b.combined_suite(c,ROOT)
    def test_42_controller_orders_science_and_independent_verify(self):
        with tempfile.TemporaryDirectory() as d,patch.object(b,'guard'),patch.object(b,'prerequisite'),patch.object(b,'subprocess_run') as run,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d);b.run(root,root/'runs/x',HEAD)
            self.assertEqual([c.args[-1] for c in run.call_args_list],['science','verify'])
    def test_43_failed_science_never_autoretries(self):
        with tempfile.TemporaryDirectory() as d,patch.object(b,'guard'),patch.object(b,'prerequisite'),patch.object(b,'subprocess_run',side_effect=ValueError('native')) as run,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d)
            with self.assertRaises(ValueError):b.run(root,root/'runs/x',HEAD)
            self.assertEqual(run.call_count,1)
        original=subprocess.Popen
        def failing(command,**kwargs):return original([sys.executable,'-u','-c','print("native failure fixture"); raise SystemExit(7)'],**kwargs)
        with tempfile.TemporaryDirectory() as d,patch.object(b.subprocess,'Popen',side_effect=failing),contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(ValueError):b.subprocess_run(Path(d),Path(d),HEAD,'fixture')
            self.assertIn('native failure fixture',(Path(d)/'fixture.log').read_text(encoding='utf-8'))
    def test_44_output_must_be_fresh_and_local(self):
        with tempfile.TemporaryDirectory() as d,patch.object(b,'guard'),patch.object(b,'prerequisite'),self.assertRaises(ValueError):
            root=Path(d);b.run(root,root/'elsewhere',HEAD)
    def test_45_no_scientific_condition_mutations(self):
        tree=ast.parse(inspect.getsource(b.scientific_worker))
        attrs=[n.attr for n in ast.walk(tree) if isinstance(n,ast.Attribute) and isinstance(n.ctx,ast.Store)]
        for name in ('SEEDS','STEPS','MANIFEST_SHA','WORK','OWN'):self.assertNotIn(name,attrs)
        text=inspect.getsource(b.scientific_worker)
        self.assertLess(text.index('b.runtime_preflight('),text.index("subprocess_run(root, folder, head, 'regression')"))
        self.assertLess(text.index('validate_regression('),text.index('b.run('))
        self.assertLess(text.index('b.verify_artifacts('),text.index('cache.recheck()'))
    def test_46_launcher_before_publish_guards(self):
        text=(ROOT/'tools/invoke_c324_scientific_r6.ps1').read_text(encoding='utf-8')
        self.assertLess(text.index('STALE_EXPECTED_HEAD'),text.index('$log ='))
        self.assertLess(text.index('STALE_RECOVERY'),text.index('$log ='))
        self.assertIn('publish_experiment_log.ps1',text);self.assertIn('SCIENTIFIC_R6',text)
    def test_47_real_worker_path_synthetic_science(self):self.worker_fixture(False)
    def test_48_worker_never_trains_after_bad_regression(self):self.worker_fixture(True)

    def worker_fixture(self,bad):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d);folder=root/'runs/r6';folder.mkdir(parents=True);events=[]
            primary={f'source-{i}':'a'*40 for i in range(792)};pins={**primary,**dict.fromkeys(b.EXTRA,'b'*40)}
            inputs={str(root/f'input-{i}'):'f'*64 for i in range(1501)}
            result=dict(source_blobs=primary,input_sha256=dict(list(inputs.items())[:1491]),status='FAIL',
                        validation_summary=dict(candidate_gate=False,seed_results=[],paired_comparisons=[]))
            class Data:
                calls=0
                def load(self,paths):self.calls+=1;return {},{},{},{}
                def close(self):events.append('close')
            data=Data()
            class Cache:
                stats={}
                def __enter__(self):return self
                def __exit__(self,*a):pass
                def recheck(self):events.append('recheck');return [dict(path=k,sha256=v) for k,v in inputs.items()]
            c=NS(OWN=(),MANIFEST_SHA='seal',WORK={'train_steps':12000},git=Mock(),load_parent=Mock(),validate_seal=Mock())
            def preflight(paths,root):events.append('preflight');c.load_parent(paths)
            def run(**kwargs):
                events.append('train');c.load_parent(kwargs['summaries']);out=kwargs['output_dir'];out.mkdir();b.save(out/'summary.json',result);return result
            def verify(out,paths,head):events.append('verify');c.load_parent(paths);return result,[]
            c.runtime_preflight=preflight;c.run=run;c.verify_artifacts=verify
            audit=NS(sha=Mock(),git=Mock());r4=NS(WinAPI=Mock(),lock_probe=Mock(return_value={}),AUDIT='fixture.audit',
                       parent_paths=Mock(return_value=[root]),LockedHashes=lambda *a,**k:Cache(),ReadLease=Mock())
            r5=NS(tree_blobs=Mock(return_value=b.FIXED),canonical=lambda p:str(p));snapshot=NS(check=Mock())
            batch=NS(wrap=lambda fn,binary:fn,hits=0)
            def child(root,folder,head,mode):
                events.append('regression');receipt=self.receipt()
                if bad:receipt['failures']=1
                b.save(folder/'regression-result.json',receipt)
            torch=NS(__version__='2.10.0+cu130',set_num_threads=Mock(),use_deterministic_algorithms=Mock())
            numpy=NS(__version__='2.3.5')
            target='fold_lm.v05_benchmarks.model_c324_interior_coverage_training'
            def importer(name):return c if name==target else audit
            # os.name affects pathlib globally; make it native only for the initial predicate.
            class Platform:
                name='nt'
            with patch.object(b,'os',Platform),patch.object(b,'guard'),patch.object(b,'source_bytes'),patch.object(b,'helper',side_effect=[r4,r5]),\
                 patch.object(b.sys,'version_info',(3,13,15)),patch.dict(sys.modules,{'torch':torch,'numpy':numpy}),\
                 patch.object(b.importlib,'import_module',side_effect=importer),\
                 patch.object(b,'prepare_parent',return_value=(snapshot,pins,inputs,batch,data,{})),\
                 patch.object(b,'subprocess_run',side_effect=child):
                if bad:
                    with self.assertRaises(ValueError):b.scientific_worker(root,folder,HEAD)
                    self.assertNotIn('train',events);self.assertNotIn('recheck',events)
                else:
                    b.scientific_worker(root,folder,HEAD)
                    self.assertEqual(events,['preflight','regression','train','verify','close','recheck'])
                    envelope=b.read(folder/'execution-envelope.json')
                    self.assertEqual(envelope['scientific_status'],'FAIL')
                    self.assertEqual(envelope['parsed_parent_reads'],3)
                    self.assertEqual(envelope['source_count'],802);self.assertEqual(envelope['input_count'],1501)

if __name__=='__main__':unittest.main()
