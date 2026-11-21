"""R3 software tests, including a real subprocess with synthetic parent modules."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/'tools/c324_parent_profile_r3.py'
SPEC = importlib.util.spec_from_file_location('r3_tested', SCRIPT)
b = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b)


def fake_paths(root):
    (root/'tools').mkdir(exist_ok=True)
    paths = [root/'runs'/f'c{n}-fixture'/'summary.json' for n in range(323,273,-1)]
    for p in paths:
        p.parent.mkdir(parents=True); p.write_text('{}',encoding='utf-8')
    text = '\n'.join(f'(Join-Path $Root "runs\\c{n}-fixture\\summary.json")' for n in range(323,273,-1))
    (root/'tools/invoke_c324.ps1').write_text(text,encoding='utf-8')
    return paths


def fake_r2(root):
    folder=root/'docs/experiment-run-logs/c324';folder.mkdir(parents=True)
    worker=dict(completed=True,returncode=0,timed_out=False,worker_result=dict(target=dict(source_matches_loaded=True)))
    r=dict(role='C324-R2-NATIVE-DIAGNOSTIC',diagnostic_completed=True,scientific_training_steps=0,
           commit_sha=b.R2_EXECUTION,workers={k:worker for k in ('existing_cache','fresh_source_cache_path')})
    log=folder/'latest.log';log.write_text('diagnostic_report = '+json.dumps(r)+'\n',encoding='utf-8')
    h=b.sha(log)
    (folder/'latest.json').write_text(json.dumps(dict(experiment_id='C324',execution_head=b.R2_EXECUTION,
                                                     log_sha256=h,log_bytes=log.stat().st_size)),encoding='utf-8')
    return log,h


class R3Tests(unittest.TestCase):
    def test_01_guard_preserves_science(self):
        with patch.object(b,'git',side_effect=[b.BRANCH,'a'*40,'','']) as g:b.guard(ROOT,'a'*40)
        self.assertIn('tools/run_c324.ps1',g.call_args.args)

    def test_02_wrong_branch(self):
        with patch.object(b,'git',return_value='wrong'),self.assertRaises(ValueError):b.guard(ROOT,'a'*40)

    def test_03_wrong_head(self):
        with patch.object(b,'git',side_effect=[b.BRANCH,'b'*40]),self.assertRaises(ValueError):b.guard(ROOT,'a'*40)

    def test_04_dirty_or_science_change(self):
        for tail in (['changed'],['','fold_lm/x.py']):
            with patch.object(b,'git',side_effect=[b.BRANCH,'a'*40,*tail]),self.assertRaises(ValueError):b.guard(ROOT,'a'*40)

    def test_05_all_fifty_ordered_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);expected=fake_paths(root);self.assertEqual(b.parent_paths(root),expected)

    def test_06_missing_path(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);fake_paths(root)[10].unlink()
            with self.assertRaises(ValueError):b.parent_paths(root)

    def test_07_reordered_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);fake_paths(root);p=root/'tools/invoke_c324.ps1'
            p.write_text('\n'.join(reversed(p.read_text().splitlines())),encoding='utf-8')
            with self.assertRaises(ValueError):b.parent_paths(root)

    def test_08_r2_validated_not_inferred(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);_,h=fake_r2(root)
            with patch.object(b,'R2_LOG_SHA',h):self.assertTrue(b.r2_evidence(root)['diagnostic_completed'])

    def test_09_r2_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,h=fake_r2(root);p.write_text('tampered',encoding='utf-8')
            with patch.object(b,'R2_LOG_SHA',h),self.assertRaises(ValueError):b.r2_evidence(root)

    def test_10_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'out';b.save(p,{})
            with self.assertRaises(FileExistsError):b.save(p,{})

    def test_11_stack_never_reads_locals(self):
        frame=NS(f_code=NS(co_filename=str(ROOT/'fold_lm/x.py'),co_name='x'),f_lineno=7,f_back=None)
        self.assertEqual(b.describe_stack(frame,ROOT),[dict(file='fold_lm/x.py',function='x',line=7)])

    def test_12_stack_bounds_and_external_redaction(self):
        frame=NS(f_code=NS(co_filename='/private/secret/module.py',co_name='x'),f_lineno=1)
        frame.f_back=frame
        frames=b.describe_stack(frame,ROOT)
        self.assertEqual(len(frames),160);self.assertEqual(frames[0]['file'],'<external>/module.py')

    def test_13_sampler_writes_and_stops(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'samples';phase=['fixture']
            with b.Sampler(ROOT,p,phase,interval=.005) as sampler:time.sleep(.03)
            self.assertFalse(sampler.thread.is_alive());self.assertGreater(b.summarize_samples(p)['samples'],0)

    def test_14_missing_samples_not_fake_success(self):
        with tempfile.TemporaryDirectory() as d:self.assertEqual(b.summarize_samples(Path(d)/'missing')['samples'],0)

    def test_15_partial_final_sample_retained_safely(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'samples';p.write_bytes(b'{"phase":"x","stack":[]}\n{"phase":')
            r=b.summarize_samples(p);self.assertEqual(r['samples'],1);self.assertTrue(r['incomplete_last_line'])

    def test_16_malformed_complete_sample_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'samples';p.write_bytes(b'not-json\n')
            with self.assertRaises(ValueError):b.summarize_samples(p)

    def test_17_nearest_frame_not_inclusive_sum(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'samples';row=dict(phase='parent',stack=[dict(file='<external>/x.py',function='read',line=1),
                dict(file='fold_lm/a.py',function='load',line=2),dict(file='fold_lm/b.py',function='verify',line=3)])
            p.write_text(json.dumps(row)+'\n',encoding='utf-8');r=b.summarize_samples(p)
            self.assertEqual(r['nearest_repository_frame'],[dict(file='fold_lm/a.py',function='load',samples=1)])

    def test_18_failure_keeps_exit(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            r=b.monitor([sys.executable,'-c','raise SystemExit(7)'],d,d)
        self.assertEqual(r['returncode'],7);self.assertFalse(r['parent_validation_completed'])

    def test_19_zero_exit_without_receipt_not_pass(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            r=b.monitor([sys.executable,'-c','pass'],d,d)
        self.assertFalse(r['parent_validation_completed'])

    def test_20_timeout_retains_samples(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            p=Path(d)/'samples.jsonl';p.write_text('{"phase":"fixture","stack":[]}\n',encoding='utf-8')
            r=b.monitor([sys.executable,'-c','import time;time.sleep(30)'],d,d,timeout=.05)
        self.assertTrue(r['timed_out']);self.assertEqual(r['sampling']['samples'],1)

    def test_21_controller_one_probe_and_no_autoretry(self):
        with tempfile.TemporaryDirectory() as d,patch.object(b,'guard'),patch.object(b,'r2_evidence'),\
             patch.object(b,'monitor',return_value={'timed_out':True}) as m,contextlib.redirect_stdout(io.StringIO()):
            out=Path(d)/'runs'/'r3';b.run(d,out,'a'*40)
            self.assertEqual(m.call_count,1)
            r=json.loads((out/'diagnostic-report.json').read_text())
            self.assertEqual(r['scientific_status'],'NOT_JUDGED');self.assertEqual(r['scientific_training_steps'],0)

    def test_22_bad_output_before_probe(self):
        with tempfile.TemporaryDirectory() as d,patch.object(b,'guard'),patch.object(b,'r2_evidence'),self.assertRaises(ValueError):
            b.run(d,Path(d)/'elsewhere','a'*40)

    def test_23_launcher_recovery_before_log(self):
        text=(ROOT/'tools/invoke_c324_parent_profile_r3.ps1').read_text(encoding='utf-8')
        self.assertLess(text.index('STALE_RECOVERY'),text.index('$log ='))
        self.assertLess(text.index('STALE_EXPECTED_HEAD'),text.index('$log ='))
        self.assertNotIn('run_c324.ps1',text);self.assertIn('publish_experiment_log.ps1',text)

    def test_24_worker_does_not_trace_or_start_science(self):
        import ast
        tree=ast.parse(SCRIPT.read_text(encoding='utf-8'))
        names=[n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)]
        self.assertNotIn('settrace',names);self.assertNotIn('setprofile',names)
        self.assertEqual(names.count('load_parent'),1)
        self.assertNotIn('runtime_preflight',names);self.assertNotIn('fit',names)

    def test_25_real_worker_synthetic_parent(self):self.integration(False)
    def test_26_real_worker_forbids_model_forward(self):self.integration(True)

    def integration(self, neural):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d);fake_paths(root);pkg=root/'fold_lm/v05_benchmarks';pkg.mkdir(parents=True)
            (pkg.parent/'__init__.py').write_text('',encoding='utf-8');(pkg/'__init__.py').write_text('',encoding='utf-8')
            code='from types import SimpleNamespace as NS\nfrom contextlib import nullcontext\n'
            code+='def validate_seal(): pass\ndef context(): return (NS(guarded=NS(no_neural=nullcontext)),)\n'
            code+='def run(): raise RuntimeError("must not run")\ndef runtime_preflight(): pass\ndef fit(): pass\ndef make_models(): pass\n'
            code+='def load_parent(paths):\n assert len(paths)==50\n'
            if neural:code+=' import torch\n torch.nn.Linear(1,1)(torch.zeros(1,1))\n'
            code+=" return {'experiment_id':'SOFTWARE-FIXTURE'}, {'TRAIN':[0],'HOLDOUT':[0]}, {}, {}\n"
            (pkg/'model_c324_interior_coverage_training.py').write_text(code,encoding='utf-8')
            out=root/'out';out.mkdir()
            r=b.monitor([sys.executable,'-B',str(SCRIPT),'--worker','--root',str(root),'--output-dir',str(out)],root,out,timeout=45)
            self.assertEqual(r['parent_validation_completed'],not neural,r)
            if not neural:self.assertEqual(r['worker_result']['scientific_training_steps'],0)
            else:self.assertIn('forbids model forwards',(out/'stderr.log').read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main()
