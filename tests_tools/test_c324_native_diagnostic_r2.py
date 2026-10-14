"""C324 R2 controller tests; fixtures are explicitly not a scientific FOLD run."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('c324_native_r2_tested', ROOT/'tools/c324_native_diagnostic_r2.py')
b = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b)


class NativeDiagnosticTests(unittest.TestCase):
    def test_01_signature_is_stable(self):
        a=compile('def f():\n return 1\n','a','exec').co_consts[0]
        z=compile('def f():\n return 1\n','different_path','exec').co_consts[0]
        self.assertEqual(b.code_signature(a),b.code_signature(z))

    def test_02_signature_detects_changed_code(self):
        a=compile('def f():\n return 1\n','a','exec').co_consts[0]
        z=compile('def f():\n return 2\n','a','exec').co_consts[0]
        self.assertNotEqual(b.code_signature(a),b.code_signature(z))

    def test_03_compile_does_not_execute_module(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source.py';p.write_text('def f():\n return 3\nraise RuntimeError("must not execute")\n')
            self.assertEqual(b.source_function(p,'f').co_name,'f')

    def test_04_missing_function_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source.py';p.write_text('a=1\n')
            with self.assertRaises(ValueError):b.source_function(p,'f')

    def test_05_cache_copy_preserves_original(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'source.pyc';p.write_bytes(b'not-executed-bytecode')
            out=root/'out';out.mkdir();r=b.cache_record(p,out)
            self.assertEqual(p.read_bytes(),b'not-executed-bytecode')
            self.assertEqual((out/r['preserved_file']).read_bytes(),p.read_bytes())
            self.assertEqual(r['sha256'],b.file_sha(p))

    def test_06_missing_cache_is_reported(self):
        with tempfile.TemporaryDirectory() as d:self.assertFalse(b.cache_record(Path(d)/'missing',d)['exists'])

    def test_07_no_overwrite_receipts(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'receipt.json';b.dump_new(p,{'a':1})
            with self.assertRaises(FileExistsError):b.dump_new(p,{'a':2})

    def test_08_nan_rejected(self):
        with tempfile.TemporaryDirectory() as d,self.assertRaises(ValueError):b.dump_new(Path(d)/'receipt',{'x':float('nan')})

    def test_09_baseline_is_readonly_without_cache_override(self):
        with tempfile.TemporaryDirectory() as d:
            cmd=b.worker_command('python','script',d,d,False)
            self.assertIn('-B',cmd);self.assertFalse(any('pycache_prefix=' in x for x in cmd))
            self.assertNotIn('-O',cmd);self.assertNotIn('-I',cmd)

    def test_10_fresh_prefix_empty_and_separate(self):
        with tempfile.TemporaryDirectory() as d:
            cmd=b.worker_command('python','script',d,d,True)
            self.assertIn('pycache_prefix='+str(Path(d)/'empty-pycache-prefix'),cmd)
            self.assertEqual(list((Path(d)/'empty-pycache-prefix').iterdir()),[])
            with self.assertRaises(FileExistsError):b.worker_command('python','script',d,d,True)

    def test_11_runtime_info_does_not_dump_secrets(self):
        with patch.dict('os.environ',{'SECRET_TOKEN':'not-for-report','OMP_NUM_THREADS':'2'}):
            r=b.runtime_info();self.assertNotIn('SECRET_TOKEN',r['environment']);self.assertEqual(r['environment']['OMP_NUM_THREADS'],'2')

    def test_12_guard_rejects_wrong_branch(self):
        with patch.object(b,'git',return_value='other'),self.assertRaisesRegex(ValueError,'branch'):b.guard(ROOT,'a'*40)

    def test_13_guard_rejects_stale_head(self):
        with patch.object(b,'git',side_effect=[b.BRANCH,'b'*40]),self.assertRaisesRegex(ValueError,'HEAD'):b.guard(ROOT,'a'*40)

    def test_14_guard_rejects_dirty(self):
        with patch.object(b,'git',side_effect=[b.BRANCH,'a'*40,' M changed']),self.assertRaisesRegex(ValueError,'dirty'):b.guard(ROOT,'a'*40)

    def test_15_guard_rejects_scientific_changes(self):
        with patch.object(b,'git',side_effect=[b.BRANCH,'a'*40,'','fold_lm/changed.py']),self.assertRaisesRegex(ValueError,'source changed'):b.guard(ROOT,'a'*40)

    def test_16_guard_accepts_unchanged_science(self):
        with patch.object(b,'git',side_effect=[b.BRANCH,'a'*40,'','']) as run:b.guard(ROOT,'a'*40)
        self.assertEqual(run.call_args.args[1:4],('diff','--name-only',b.FAILED_EXECUTION))

    def test_17_process_failure_is_preserved(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            r=b.run_worker([sys.executable,'-c','import sys;print("native diagnosis");sys.exit(7)'],d,d)
            self.assertEqual(r['returncode'],7);self.assertFalse(r['completed']);self.assertFalse(r['timed_out'])

    def test_18_worker_success_needs_receipt(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            r=b.run_worker([sys.executable,'-c','pass'],d,d);self.assertFalse(r['completed'])

    def test_19_timeout_kills_only_probe(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            r=b.run_worker([sys.executable,'-c','import time;time.sleep(30)'],d,d,timeout=.05)
            self.assertTrue(r['timed_out']);self.assertFalse(r['completed'])

    def test_20_success_receipt_readback(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            b.dump_new(Path(d)/'worker-result.json',{'role':b.ROLE,'scientific_training_steps':0})
            r=b.run_worker([sys.executable,'-c','pass'],d,d);self.assertTrue(r['completed'])

    def test_21_two_outcomes_collected_no_auto_science(self):
        with tempfile.TemporaryDirectory() as d,patch.object(b,'guard') as guard,patch.object(b,'run_worker',return_value={'completed':False}) as worker,contextlib.redirect_stdout(io.StringIO()):
            out=Path(d)/'runs'/'r2';b.run(d,out,'a'*40)
            self.assertEqual(worker.call_count,2);self.assertEqual(guard.call_count,2)
            r=json.loads((out/'diagnostic-report.json').read_text());self.assertEqual(r['scientific_status'],'NOT_JUDGED')
            self.assertFalse(r['scientific_execution_requested']);self.assertEqual(r['scientific_training_steps'],0)

    def test_22_unsafe_output_rejected(self):
        with tempfile.TemporaryDirectory() as d,patch.object(b,'guard'),self.assertRaisesRegex(ValueError,'inside runs'):b.run(d,Path(d)/'other','a'*40)

    def test_23_launcher_publication_and_preflight_order(self):
        text=(ROOT/'tools/invoke_c324_native_diagnostic_r2.ps1').read_text()
        self.assertLess(text.index('STALE_EXPECTED_HEAD'),text.index('$log ='))
        self.assertLess(text.index('STALE_RECOVERY'),text.index('$log ='))
        self.assertIn('publish_experiment_log.ps1',text);self.assertIn('scientific_execution_requested = False',text)
        self.assertNotIn('run_c324.ps1',text)

    def test_24_source_worker_guard_inventory(self):
        import inspect
        text=inspect.getsource(b.worker)
        for name in ("'_call_impl'","'__init__'","'load'","'load_parent'","'precheck'","'run'","'runtime_preflight'"):self.assertIn(name,text)
        self.assertNotIn('verify_artifacts(',text);self.assertNotIn('optimizer.step(',text)

    def test_25_real_subprocess_healthy_import_fixture(self):
        self._integration(False)

    def test_26_real_subprocess_stale_cache_fixture(self):
        self._integration(True)

    def _integration(self, stale):
        # Real interpreter/PyTorch, synthetic repository modules; no real ancestor archives.
        import os
        import py_compile
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d);package=root/'fold_lm'/'v05_benchmarks';package.mkdir(parents=True)
            (root/'fold_lm'/'__init__.py').write_text('')
            (package/'__init__.py').write_text('')
            (package/'model_c241_assignment_holdout.py').write_text('MARKER = 1\n')
            target=package/'model_c242_balanced_recombination.py'
            source='def parent_module():\n    "old"\n    from fold_lm.v05_benchmarks import model_c241_assignment_holdout as parent\n    return parent\n'
            target.write_text(source);stat=target.stat()
            py_compile.compile(str(target),doraise=True)
            if stale:
                target.write_text(source.replace('"old"','"new"'))
                os.utime(target,ns=(stat.st_atime_ns,stat.st_mtime_ns))
            (package/'model_c324_interior_coverage_training.py').write_text(
                'def context(): return (None,)*6\ndef load_parent(): pass\ndef precheck(): pass\ndef run(): pass\ndef runtime_preflight(): pass\n')
            before=b.file_sha(target);outcomes=[]
            for label,fresh in (('existing',False),('fresh',True)):
                out=root/label;out.mkdir()
                cmd=b.worker_command(sys.executable,ROOT/'tools/c324_native_diagnostic_r2.py',root,out,fresh)
                outcomes.append(b.run_worker(cmd,root,out))
            self.assertEqual(b.file_sha(target),before)
            self.assertEqual([r['completed'] for r in outcomes],[not stale,True],outcomes)
            for r in outcomes:
                if r['completed']:
                    self.assertEqual(r['worker_result']['model_forward_calls'],0)
                    self.assertEqual(r['worker_result']['parent_artifact_verifications'],0)
            if stale:
                self.assertIn('differs from current source',(root/'existing'/'stderr.log').read_text())


if __name__=='__main__':unittest.main()
