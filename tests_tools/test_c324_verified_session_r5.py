"""R5 software-only tests. These fixtures do not qualify Windows parent archives."""
import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('r5_tested', ROOT / 'tools/c324_verified_session_r5.py')
b = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b)


class FixtureCache:
    """Explicit software mutation detector, NOT the production Windows lock."""
    def __init__(self):
        self.entries, self.closed = {}, False
    def sha(self, path):
        key = b.canonical(path)
        raw = Path(path).read_bytes()
        value = hashlib.sha256(raw).hexdigest()
        if key not in self.entries:
            def check():
                if Path(path).read_bytes() != raw:
                    raise ValueError('fixture bytes changed')
            self.entries[key] = NS(check=check), value
        self.entries[key][0].check()
        return self.entries[key][1]


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.parents = []
        for n in range(3):
            p = self.root / ('p' + str(n)); p.write_text('{}', encoding='utf-8'); self.parents.append(p)
        self.guard = Mock()
        self.state = Mock(return_value='constant-runtime')
        self.s = b.VerifiedSession(self.guard, self.state)
        self.calls = []
        def verify(outdir, summaries, expected_head):
            self.calls.append((outdir, list(summaries), expected_head))
            return {'head': expected_head, 'parent_order': [str(p) for p in summaries]}, [{'value': 0.5}]
        self.original = verify
        self.fn = self.s.wrap('fixture', verify, 'source-id')
    def tearDown(self):
        self.s.close(); self.temp.cleanup()
    def call(self, fn=None, parents=None, head='a'):
        return (self.fn if fn is None else fn)(self.root, self.parents if parents is None else parents, head)

    def test_01_same_key_runs_body_once(self):
        a=self.call(); z=self.call(); self.assertEqual(a,z); self.assertEqual(len(self.calls),1)
        self.assertEqual(self.s.counts['fixture']['reused'],1)
    def test_02_first_caller_cannot_mutate_cache(self):
        a=self.call(); a[1][0]['value']=77; self.assertEqual(self.call()[1][0]['value'],.5)
    def test_03_hit_caller_cannot_mutate_cache(self):
        self.call(); a=self.call(); a[0]['parent_order'].clear(); self.assertEqual(len(self.call()[0]['parent_order']),3)
    def test_04_parent_order_is_part_of_key(self):
        self.call(); self.call(parents=list(reversed(self.parents))); self.assertEqual(len(self.calls),2)
    def test_05_expected_head_is_part_of_key(self):
        self.call(); self.call(head='b'); self.assertEqual(len(self.calls),2)
    def test_06_output_directory_is_part_of_key(self):
        self.call(); other=self.root/'other'; other.mkdir(); self.fn(other,self.parents,'a'); self.assertEqual(len(self.calls),2)
    def test_07_source_identity_is_part_of_key(self):
        self.call(); other=self.s.wrap('fixture',self.original,'different-source'); self.call(other); self.assertEqual(len(self.calls),2)
    def test_08_name_is_part_of_key(self):
        self.call(); other=self.s.wrap('other',self.original,'source-id'); self.call(other); self.assertEqual(len(self.calls),2)
    def test_09_keyword_and_positional_equivalence(self):
        self.call(); self.fn(expected_head='a',summaries=self.parents,outdir=self.root); self.assertEqual(len(self.calls),1)
    def test_10_generator_order_not_consumed(self):
        self.call(parents=iter(self.parents)); self.assertEqual(len(self.calls[0][1]),3)
    def test_11_failure_never_cached(self):
        count=[]
        def broken(outdir,summaries,expected_head):
            count.append(1); raise ValueError('original rejection')
        fn=self.s.wrap('bad',broken,'source')
        for _ in range(2):
            with self.assertRaisesRegex(ValueError,'original rejection'):self.call(fn)
        self.assertEqual(len(count),2); self.assertFalse(self.s.entries); self.assertFalse(self.s.active)
    def test_12_missing_input_is_not_a_cache_hit(self):
        self.call(); self.parents[0].unlink()
        with self.assertRaises(FileNotFoundError):self.call()
    def test_13_guard_runs_before_reuse(self):
        self.call(); self.guard.side_effect=ValueError('input changed')
        with self.assertRaisesRegex(ValueError,'input changed'):self.call()
        self.assertEqual(self.s.counts['fixture']['reused'],0)
    def test_14_changed_runtime_does_not_reuse(self):
        self.call(); self.state.return_value='changed'
        with self.assertRaisesRegex(ValueError,'runtime context changed'):self.call()
    def test_15_runtime_mutation_on_miss_rejected(self):
        self.state.side_effect=['before','after']
        with self.assertRaisesRegex(ValueError,'changed RNG'):self.call()
        self.assertFalse(self.s.entries)
    def test_16_stored_metadata_corruption_rejected(self):
        self.call(); next(iter(self.s.entries.values()))[0][1][0]['value']=123
        with self.assertRaisesRegex(ValueError,'stored metadata'):self.call()
    def test_17_code_mutation_rejected(self):
        def changed(outdir,summaries,expected_head):
            self.calls.append('changed');return {},[]
        self.original.__code__=changed.__code__
        with self.assertRaisesRegex(ValueError,'code mutated'):self.call()
    def test_18_entry_limit_fail_closed(self):
        self.s.max_entries=1; self.call()
        with self.assertRaisesRegex(ValueError,'entry bound'):self.call(head='different')
    def test_19_metadata_memory_bound(self):
        self.s.max_bytes=1
        with self.assertRaisesRegex(ValueError,'memory bound'):self.call()
        self.assertFalse(self.s.entries)
    def test_20_concurrent_use_rejected(self):
        errors=[]
        def other():
            try:self.call()
            except ValueError as exc:errors.append(str(exc))
        t=threading.Thread(target=other);t.start();t.join();self.assertEqual(len(errors),1);self.assertFalse(self.calls)
    def test_21_closed_session_cannot_reuse(self):
        self.call();self.s.close()
        with self.assertRaisesRegex(ValueError,'closed'):self.call()
    def test_22_new_session_does_not_reuse_old_pass(self):
        self.call(); other=b.VerifiedSession(self.guard,self.state)
        self.call(other.wrap('fixture',self.original,'source-id'));other.close();self.assertEqual(len(self.calls),2)
    def test_23_recursive_same_request_rejected(self):
        def recursive(outdir,summaries,expected_head):return fn(outdir,summaries,expected_head)
        fn=self.s.wrap('recursive',recursive,'source')
        with self.assertRaisesRegex(ValueError,'recursive request'):self.call(fn)
        self.assertFalse(self.s.active)
    def test_24_manifest_result_types_are_preserved(self):
        x=self.call();z=self.call();self.assertEqual(type(x),type(z));self.assertIsInstance(z,tuple)
        self.assertIsInstance(z[1],list);self.assertEqual(b.metadata_bytes(x),b.metadata_bytes(z))
    def test_25_unexpected_signature_rejected(self):
        with self.assertRaisesRegex(ValueError,'signature'):self.s.wrap('x',lambda path:None,'x')
    def test_26_nonmetadata_result_not_cached(self):
        def bad(outdir,summaries,expected_head):return {},[object()]
        with self.assertRaisesRegex(ValueError,'non-metadata'):self.call(self.s.wrap('bad',bad,'x'))
        self.assertFalse(self.s.entries)


class OtherTests(unittest.TestCase):
    def test_27_typed_fingerprints(self):
        for a,z in ((True,1),(1,1.0),([1],(1,)),(0.0,-0.0)):
            self.assertNotEqual(b.metadata_bytes(a),b.metadata_bytes(z))
    def test_28_nonfinite_and_cycles_rejected(self):
        cyclic=[];cyclic.append(cyclic)
        for v in (float('nan'),float('inf'),cyclic):
            with self.assertRaises(ValueError):b.metadata_bytes(v)
    def test_29_numpy_scalar_is_preserved(self):
        import numpy as np
        import copy
        v={'x':np.float64(.5),'z':np.int64(2)}
        self.assertEqual(b.metadata_bytes(v),b.metadata_bytes(copy.deepcopy(v)))
        with self.assertRaises(ValueError):b.metadata_bytes(np.zeros(2))
    def test_30_snapshot_checks_complete_inputs_and_aliases(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'abcd');cache=FixtureCache();snapshot=b.FrozenInputs(cache)
            digest=hashlib.sha256(b'abcd').hexdigest();snapshot.freeze([(p,digest),(p,digest)])
            self.assertEqual(len(snapshot.allowed),1);self.assertEqual(snapshot.sha(p),digest)
            p.write_bytes(b'wxyz')
            with self.assertRaisesRegex(ValueError,'fixture bytes changed'):snapshot.check()
    def test_31_snapshot_rejects_initial_corruption(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'abcd')
            with self.assertRaisesRegex(ValueError,'byte mismatch'):b.FrozenInputs(FixtureCache()).freeze([(p,'a'*64)])
    def test_32_snapshot_missing_new_or_conflicting_paths(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'a');s=b.FrozenInputs(FixtureCache());h=hashlib.sha256(b'a').hexdigest()
            with self.assertRaisesRegex(ValueError,'conflicting'):s.freeze([(p,h),(p,'b'*64)])
            s.freeze([(p,h)]);q=Path(d)/'q';q.write_bytes(b'a')
            with self.assertRaisesRegex(ValueError,'unregistered'):s.sha(q)
            with self.assertRaises(ValueError):s.freeze([(p,h)])
    def test_33_missing_or_released_lease_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'a');c=FixtureCache();s=b.FrozenInputs(c);s.freeze([(p,hashlib.sha256(b'a').hexdigest())])
            c.closed=True
            with self.assertRaises(ValueError):s.check()
            c.closed=False;c.entries.clear()
            with self.assertRaises(ValueError):s.check()
    def test_34_real_git_tree_inventory(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);subprocess.run(['git','init','-q',d],check=True)
            (root/'file with space.txt').write_bytes(b'a\0b');subprocess.run(['git','-C',d,'add','.'],check=True)
            subprocess.run(['git','-C',d,'-c','user.name=fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture'],check=True)
            got=b.tree_blobs(root,'HEAD');wanted=subprocess.check_output(['git','-C',d,'rev-parse','HEAD:file with space.txt']).decode().strip()
            self.assertEqual(got,{'file with space.txt':wanted})
    def test_35_runtime_probe_consumes_no_rng(self):
        import torch
        import numpy as np
        a=b.runtime_state(torch,np);z=b.runtime_state(torch,np);self.assertEqual(a,z)
    def test_36_reference_and_deduplicated_graph_same_value(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'p';p.write_text('{}',encoding='utf-8')
            def graph(cached):
                session=b.VerifiedSession(lambda:None,lambda:'state');counts=[0]*7;funcs=[]
                for index in range(7):
                    def make(i):
                        def verifier(outdir,summaries,expected_head):
                            counts[i]+=1
                            if i:
                                a=funcs[i-1](outdir,summaries,expected_head)
                                z=funcs[i-1](outdir,summaries,expected_head)
                                if a!=z:raise ValueError('fixture mismatch')
                                value=a[0]['value']+1
                            else:value=1
                            return {'value':value},[{'level':i}]
                        return verifier
                    original=make(index);funcs.append(session.wrap(str(index),original,'source') if cached else original)
                result=funcs[-1](root,[p],'head');session.close();return result,counts
            ref,old=graph(False);actual,new=graph(True)
            self.assertEqual(ref,actual);self.assertEqual(sum(old),127);self.assertEqual(new,[1]*7)
    def test_37_real_process_error_is_not_qualification(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            r=b.monitor([sys.executable,'-c','raise SystemExit(7)'],d,d)
        self.assertEqual(r['returncode'],7);self.assertFalse(r['parent_validation_completed'])
    def test_38_timeout_not_native_failure_or_pass(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            r=b.monitor([sys.executable,'-c','import time;time.sleep(20)'],d,d,timeout=.05)
        self.assertTrue(r['timed_out']);self.assertFalse(r['parent_validation_completed'])
    def test_39_zero_exit_needs_valid_receipt(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            r=b.monitor([sys.executable,'-c','pass'],d,d)
        self.assertFalse(r['parent_validation_completed'])
    def test_40_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'out';b.save(p,{})
            with self.assertRaises(FileExistsError):b.save(p,{})
    def test_41_launcher_guard_before_log(self):
        text=(ROOT/'tools/invoke_c324_verified_session_r5.ps1').read_text(encoding='utf-8')
        self.assertLess(text.index('STALE_RECOVERY'),text.index('$log ='))
        self.assertLess(text.index('STALE_EXPECTED_HEAD'),text.index('$log ='))
        self.assertIn('publish_experiment_log.ps1',text);self.assertNotIn('run_c324.ps1',text)
    def test_42_worker_one_loader_and_final_reference(self):
        tree=ast.parse(inspect_source(b.worker));calls=[x.func.attr for x in ast.walk(tree) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute)]
        self.assertEqual(calls.count('load_parent'),1);self.assertIn('recheck',calls)
        self.assertNotIn('fit',calls);self.assertNotIn('run',calls)
        self.assertLess(inspect_source(b.worker).index('build_snapshot('),inspect_source(b.worker).index('b.load_parent('))
    def test_43_old_negative_is_not_relabelled(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            def negative(outdir,summaries,expected_head):return {'status':'FAIL'},[{'correct':1,'errors':5}]
            session=b.VerifiedSession(lambda:None,lambda:'state');fn=session.wrap('negative',negative,'source')
            self.assertEqual(fn(root,[],'x'),fn(root,[],'x'));self.assertEqual(fn(root,[],'x')[0]['status'],'FAIL');session.close()
    def test_44_corrupt_reference_graph_not_hidden(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'data';p.write_bytes(b'bad');cache=FixtureCache();s=b.FrozenInputs(cache)
            with self.assertRaises(ValueError):s.freeze([(p,hashlib.sha256(b'good').hexdigest())])
            self.assertFalse(s.frozen)

    def test_45_r4_prerequisite_whole_log_hash(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);folder=root/'docs/experiment-run-logs/c324';folder.mkdir(parents=True)
            report=dict(role='C324-R4-LOCKED-HASH-QUALIFICATION',commit_sha=b.R4_EXECUTION,
                        diagnostic_completed=True,scientific_training_steps=0,
                        worker=dict(timed_out=True,parent_validation_completed=False))
            log=folder/'latest.log';log.write_text('diagnostic_report = '+json.dumps(report)+'\n',encoding='utf-8')
            sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();h=sha(log)
            meta=dict(experiment_id='C324',execution_head=b.R4_EXECUTION,log_sha256=h,log_bytes=log.stat().st_size)
            (folder/'latest.json').write_text(json.dumps(meta),encoding='utf-8')
            with patch.object(b,'R4_LOG_SHA',h):
                self.assertEqual(b.prerequisite(root,NS(reference_sha=sha)),report)
                log.write_text('tampered',encoding='utf-8')
                with self.assertRaisesRegex(ValueError,'identity'):b.prerequisite(root,NS(reference_sha=sha))
    def test_46_controller_one_worker_and_stop(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d);fake=NS(guard=Mock())
            with patch.object(b,'load_r4',return_value=fake),patch.object(b,'tree_blobs',return_value={b.R4_PATH:b.R4_BLOB}),\
                 patch.object(b,'prerequisite'),patch.object(b,'monitor',return_value={'timed_out':True}) as m:
                b.run(root,root/'runs/r5','a'*40)
            self.assertEqual(m.call_count,1);self.assertEqual(fake.guard.call_count,2)
            report=json.loads((root/'runs/r5/diagnostic-report.json').read_text(encoding='utf-8'))
            self.assertEqual(report['scientific_status'],'NOT_JUDGED')
            self.assertEqual(report['next_action'],'STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY')
    def test_47_build_snapshot_uses_pinned_parent_and_all_sources(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);paths=[];pins={};inputs={};blobs={}
            sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
            for name,oid in b.TARGETS.items():
                rel='fold_lm/v05_benchmarks/'+name+'.py';p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'fixture')
                pins[rel]=blobs[rel]=oid;inputs[str(p)]=sha(p)
            parent=dict(source_blobs=pins,input_sha256=inputs,artifacts=[dict(file='artifact.json',sha256=hashlib.sha256(b'{}').hexdigest())])
            for i in range(50):
                p=root/'runs'/str(i)/'summary.json';p.parent.mkdir(parents=True);p.write_text(json.dumps(parent) if i==0 else '{}',encoding='utf-8');paths.append(p)
            (paths[0].parent/'artifact.json').write_bytes(b'{}')
            for rel in (b.R4_PATH,'tools/c324_verified_session_r5.py','fold_lm/v05_benchmarks/model_c324_interior_coverage_training.py'):
                p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'fixture-helper')
            c=NS(PARENT_SHA=sha(paths[0]),read_json=lambda p:json.loads(Path(p).read_text(encoding='utf-8')),
                 validate_parent=Mock(),parent_hashes=lambda cx:[sha(p) for p in paths],context=lambda:())
            snapshot,got,expected=b.build_snapshot(root,paths,c,FixtureCache(),blobs)
            self.assertEqual(got,parent);self.assertTrue(snapshot.frozen);self.assertEqual(set(expected),snapshot.allowed)
            self.assertEqual(len(snapshot.allowed),61)
            next(iter(inputs));p=Path(next(iter(inputs)));p.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'changed'):snapshot.check()
    def test_48_worker_route_cannot_reach_training(self):
        text=inspect_source(b.worker)
        for name in ("'_call_impl'","'__init__'","'run'","'runtime_preflight'","'fit'","'make_models'"):self.assertIn(name,text)
        self.assertLess(text.index('lock_probe('),text.index('build_snapshot('))
        self.assertLess(text.index('cache.recheck()'),text.index("save(output / 'worker-result.json'"))


def inspect_source(fn):
    import inspect
    return inspect.getsource(fn)

if __name__=='__main__':unittest.main()
