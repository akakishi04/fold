"""R4 authoring tests. Injected leases/Win32 ABI fixtures are NOT Windows execution."""
import ast
import contextlib
import ctypes
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('r4_tested', ROOT/'tools/c324_locked_hash_r4.py')
b = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(b)


class FixtureLease:
    """Software-only mutation simulator, never exposed by the R4 executable CLI."""
    def __init__(self, path):
        self.path, self.closed = Path(path), False
        self.size, self.signature = self.path.stat().st_size, self.stat()
    def stat(self):
        s = self.path.stat()
        return s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns
    def check(self):
        if self.closed or self.stat() != self.signature:
            raise ValueError('fixture changed')
    def digest(self, pulse):
        self.check()
        h = hashlib.sha256()
        with self.path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(b.CHUNK), b''):
                h.update(chunk); pulse(len(chunk))
        self.check()
        return h.hexdigest()
    def close(self):
        self.closed = True


class Function:
    def __init__(self, fn): self.fn = fn
    def __call__(self, *args): return self.fn(*args)


class KernelFixture:
    """ctypes argument/buffer and share-access emulator, not an OS-lock proof."""
    def __init__(self, path):
        self.path, self.handles, self.calls, self.next = str(Path(path).absolute()), {}, [], 10
        self.data = Path(path).read_bytes(); self.index = 1; self.fail_read = False
        for name in ('CreateFileW', 'GetFileInformationByHandle', 'ReadFile', 'SetFilePointerEx', 'CloseHandle'):
            setattr(self, name, Function(getattr(self, '_'+name)))
    def _CreateFileW(self, path, access, share, security, disposition, flags, template):
        self.calls.append((path, access, share, security, disposition, flags, template))
        plain = path[4:] if path.startswith('\\\\?\\') else path
        if plain.startswith('UNC\\'): plain = '\\\\' + plain[4:]
        if plain != self.path or (self.handles and access != 0x80000000): return ctypes.c_void_p(-1).value
        h = self.next; self.next += 1; self.handles[h] = 0
        return h
    def _GetFileInformationByHandle(self, handle, pointer):
        if handle not in self.handles: return 0
        x = pointer._obj; x.attributes = 0x80; x.volume = 7; x.index_low = self.index
        x.size_low = len(self.data); x.links = 1; x.write.low = 33
        return 1
    def _ReadFile(self, handle, buffer, size, count, overlapped):
        if self.fail_read: return 0
        start = self.handles[handle]; chunk = self.data[start:start+size]
        ctypes.memmove(buffer, chunk, len(chunk)); count._obj.value = len(chunk)
        self.handles[handle] += len(chunk); return 1
    def _SetFilePointerEx(self, handle, distance, unused, origin):
        self.handles[handle] = distance; return 1
    def _CloseHandle(self, handle):
        if handle not in self.handles: return 0
        del self.handles[handle]; return 1


def fake_paths(root):
    (root/'tools').mkdir(exist_ok=True)
    paths = [root/'runs'/f'c{n}-fixture'/'summary.json' for n in range(323, 273, -1)]
    for p in paths: p.parent.mkdir(parents=True); p.write_text('{}', encoding='utf-8')
    text = '\n'.join(f'(Join-Path $Root "runs\\c{n}-fixture\\summary.json")' for n in range(323, 273, -1))
    (root/'tools/invoke_c324.ps1').write_text(text, encoding='utf-8')
    return paths


def fake_r3(root):
    folder = root/'docs/experiment-run-logs/c324'; folder.mkdir(parents=True)
    report = dict(role='C324-R3-PARENT-PROFILE', diagnostic_completed=True, commit_sha=b.R3_EXECUTION,
                  scientific_training_steps=0, worker=dict(timed_out=True, parent_validation_completed=False,
                  sampling=dict(samples=179, nearest_repository_frame=[dict(file=b.AUDIT_PATH, function='sha', samples=171)])))
    path = folder/'latest.log'; path.write_text('diagnostic_report = '+json.dumps(report)+'\n', encoding='utf-8')
    h = b.reference_sha(path)
    (folder/'latest.json').write_text(json.dumps(dict(experiment_id='C324', execution_head=b.R3_EXECUTION,
                            log_sha256=h, log_bytes=path.stat().st_size)), encoding='utf-8')
    return path, h


class R4Tests(unittest.TestCase):
    def test_01_win32_layout_and_call_signature(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'abc');lib=KernelFixture(p);api=b.WinAPI(lib);lease=b.ReadLease(p,api)
            self.assertEqual(ctypes.sizeof(b.FileInfo),52)
            self.assertEqual(lib.calls[0][1:],(0x80000000,1,None,3,0x00200080,None))
            self.assertEqual(lib.CreateFileW.restype,ctypes.c_void_p);lease.close()
            self.assertFalse(lib.handles)

    def test_02_native_adapter_chunked_digest_reference(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'日本語';p.write_bytes(b'0123'*(b.CHUNK//2+7));lib=KernelFixture(p);api=b.WinAPI(lib)
            lease=b.ReadLease(p,api);parts=[]
            self.assertEqual(lease.digest(parts.append),b.reference_sha(p));self.assertEqual(sum(parts),p.stat().st_size)
            lease.close();self.assertFalse(lib.handles)

    def test_03_empty_file_supported(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'');api=b.WinAPI(KernelFixture(p));lease=b.ReadLease(p,api)
            self.assertEqual(lease.digest(lambda n:None),hashlib.sha256(b'').hexdigest());lease.close()

    def test_04_handle_identity_drift_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'abc');lib=KernelFixture(p);lease=b.ReadLease(p,b.WinAPI(lib));lib.index+=1
            with self.assertRaisesRegex(ValueError,'held file'):lease.check()
            lease.close();self.assertFalse(lib.handles)

    def test_05_read_error_propagates_and_cleanup(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'abc');lib=KernelFixture(p);lease=b.ReadLease(p,b.WinAPI(lib));lib.fail_read=True
            with self.assertRaises(OSError):lease.digest(lambda n:None)
            lease.close();self.assertFalse(lib.handles)

    def test_06_runtime_share_probe_exercises_write_delete_release(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'lock-probe.bin'
            # The production function creates this exact payload before opening its lease.
            stub=Path(d)/'seed';stub.write_bytes(b'FOLD-C324-R4-read-only-lock-probe\n')
            lib=KernelFixture(stub);lib.path=str(p.absolute());r=b.lock_probe(b.WinAPI(lib),d)
            self.assertEqual(r['native_lock_probe'],'PASS');self.assertFalse(lib.handles)
            requests=[c[1] for c in lib.calls];self.assertIn(0x40000000,requests);self.assertIn(0x10000,requests)
            self.assertEqual(requests[-1],0x40000000)

    def test_07_no_unlocked_production_fallback(self):
        with patch.object(b.os,'name','posix'),self.assertRaisesRegex(ValueError,'Windows'):b.WinAPI()

    def test_08_first_miss_and_reuse_are_reference_equal(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'abcd');ref=Mock(wraps=b.reference_sha);leases=[]
            def factory(path):leases.append(FixtureLease(path));return leases[-1]
            with b.LockedHashes(ref,factory) as cache:
                values=[cache.sha(p) for _ in range(100)]
                self.assertEqual(set(values),{b.reference_sha(p)})
                self.assertEqual(ref.call_count,1);self.assertEqual(cache.stats['cache_hits'],99)
                self.assertEqual(cache.stats['stream_bytes'],4);self.assertEqual(cache.stats['logical_reference_bytes'],400)
                rows=cache.recheck();self.assertEqual(ref.call_count,2);self.assertEqual(len(rows),1)
                self.assertEqual(cache.stats['reference_bytes'],8)
            self.assertTrue(all(x.closed for x in leases));self.assertFalse(cache.entries)

    def test_09_mutation_at_same_size_not_silently_reused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'abcd')
            with b.LockedHashes(b.reference_sha,FixtureLease) as cache:
                cache.sha(p);p.write_bytes(b'wxyz');os.utime(p,ns=(1,1))
                with self.assertRaises(ValueError):cache.sha(p)

    def test_10_final_reference_not_metadata_alone(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'abcd')
            with b.LockedHashes(b.reference_sha,FixtureLease) as cache:
                cache.sha(p);s=p.stat();p.write_bytes(b'wxyz');os.utime(p,ns=(s.st_atime_ns,s.st_mtime_ns))
                with self.assertRaisesRegex(ValueError,'final/reference'):cache.recheck()

    def test_11_failed_miss_not_cached(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'a');lease=FixtureLease(p)
            with b.LockedHashes(lambda path:'wrong',lambda path:lease) as cache:
                with self.assertRaisesRegex(ValueError,'miss/reference'):cache.sha(p)
                self.assertFalse(cache.entries);self.assertTrue(lease.closed)

    def test_12_missing_file_raises(self):
        with tempfile.TemporaryDirectory() as d,b.LockedHashes(b.reference_sha,FixtureLease) as cache:
            with self.assertRaises(FileNotFoundError):cache.sha(Path(d)/'missing')

    def test_13_lock_failure_has_no_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'a');ref=Mock()
            with b.LockedHashes(ref,Mock(side_effect=PermissionError('sharing'))) as cache:
                with self.assertRaises(PermissionError):cache.sha(p)
                ref.assert_not_called();self.assertFalse(cache.entries)

    def test_14_max_handles_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as d,b.LockedHashes(b.reference_sha,FixtureLease,max_files=1) as cache:
            a=Path(d)/'a';z=Path(d)/'z';a.write_bytes(b'a');z.write_bytes(b'z');cache.sha(a)
            with self.assertRaisesRegex(ValueError,'bound'):cache.sha(z)
            self.assertEqual(cache.sha(a),b.reference_sha(a))

    def test_15_sessions_do_not_reuse_previous_success(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'a')
            with b.LockedHashes(b.reference_sha,FixtureLease) as a:x=a.sha(p)
            p.write_bytes(b'z')
            with b.LockedHashes(b.reference_sha,FixtureLease) as z:self.assertNotEqual(x,z.sha(p))
            with self.assertRaisesRegex(ValueError,'closed'):a.sha(p)

    def test_16_concurrent_use_rejected(self):
        with tempfile.TemporaryDirectory() as d,b.LockedHashes(b.reference_sha,FixtureLease) as cache:
            p=Path(d)/'a';p.write_bytes(b'a');errors=[]
            def child():
                try:cache.sha(p)
                except ValueError as exc:errors.append(str(exc))
            t=threading.Thread(target=child);t.start();t.join();self.assertEqual(len(errors),1)

    def test_17_equivalent_paths_share_same_locked_entry(self):
        with tempfile.TemporaryDirectory() as d,b.LockedHashes(b.reference_sha,FixtureLease) as cache:
            root=Path(d);(root/'sub').mkdir();p=root/'a';p.write_bytes(b'a')
            self.assertEqual(cache.sha(p),cache.sha(root/'sub/../a'));self.assertEqual(cache.stats['unique_files'],1)

    def test_18_context_cleanup_on_semantic_rejection(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a';p.write_bytes(b'wrong');leases=[]
            def factory(path):leases.append(FixtureLease(path));return leases[-1]
            with self.assertRaisesRegex(ValueError,'semantic'):
                with b.LockedHashes(b.reference_sha,factory) as cache:
                    cache.sha(p);raise ValueError('semantic failure unchanged')
            self.assertTrue(leases[0].closed)

    def test_19_real_parent_call_adapter_restores_hash_primitive(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'a';p.write_bytes(b'abcd');audit=NS(sha=b.reference_sha)
            def load(paths):
                for _ in range(50):self.assertEqual(audit.sha(p),b.reference_sha(p))
                return dict(experiment_id='fixture',commit_sha='x'),dict(TRAIN=[0]*192,HOLDOUT=[0]*96),{},{}
            c=NS(context=lambda:(NS(guarded=NS(no_neural=contextlib.nullcontext)),),load_parent=Mock(side_effect=load),
                 validate_parent=Mock(),digest=lambda v:hashlib.sha256(json.dumps(v).encode()).hexdigest())
            with b.LockedHashes(audit.sha,FixtureLease) as cache:
                r=b.evaluate_parent(c,audit,[p],cache,root);self.assertEqual(r['hash_inventory_count'],1)
                c.load_parent.assert_called_once_with([p]);c.validate_parent.assert_called_once()
            self.assertIs(audit.sha,b.reference_sha)

    def test_20_loader_exception_not_replaced_by_cached_pass(self):
        audit=NS(sha=b.reference_sha);c=NS(context=lambda:(NS(guarded=NS(no_neural=contextlib.nullcontext)),),
                                         load_parent=Mock(side_effect=ValueError('parent corruption')))
        with tempfile.TemporaryDirectory() as d,b.LockedHashes(audit.sha,FixtureLease) as cache:
            with self.assertRaisesRegex(ValueError,'parent corruption'):b.evaluate_parent(c,audit,[],cache,d)
            self.assertIs(audit.sha,b.reference_sha)

    def test_21_wrong_reference_rejected_before_loader(self):
        audit=NS(sha=b.reference_sha);c=Mock()
        with b.LockedHashes(lambda p:'x',FixtureLease) as cache,self.assertRaises(ValueError):b.evaluate_parent(c,audit,[],cache,'.')
        c.load_parent.assert_not_called()

    def test_22_guard_unchanged_science_and_audit_pin(self):
        with patch.object(b,'git',side_effect=[b.BRANCH,'a'*40,'','',b.AUDIT_BLOB]) as g:b.guard(ROOT,'a'*40)
        self.assertIn('tools/run_c324.ps1',g.call_args_list[-2].args)

    def test_23_guard_rejects_every_state_drift(self):
        for replies in (['wrong'],[b.BRANCH,'b'*40],[b.BRANCH,'a'*40,'dirty'],
                        [b.BRANCH,'a'*40,'','changed'],[b.BRANCH,'a'*40,'','','wrong']):
            with patch.object(b,'git',side_effect=replies),self.assertRaises(ValueError):b.guard(ROOT,'a'*40)

    def test_24_fifty_parent_order_and_existence(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);paths=fake_paths(root);self.assertEqual(paths,b.parent_paths(root));paths[2].unlink()
            with self.assertRaises(ValueError):b.parent_paths(root)

    def test_25_reordered_parent_paths_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);fake_paths(root);p=root/'tools/invoke_c324.ps1';p.write_text('\n'.join(reversed(p.read_text().splitlines())))
            with self.assertRaises(ValueError):b.parent_paths(root)

    def test_26_entire_r3_evidence_hash_checked(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p,h=fake_r3(root)
            with patch.object(b,'R3_LOG_SHA',h):self.assertTrue(b.prerequisite(root)['diagnostic_completed'])
            p.write_text('tampered')
            with patch.object(b,'R3_LOG_SHA',h),self.assertRaises(ValueError):b.prerequisite(root)

    def test_27_no_overwrite_and_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'out';b.save(p,{})
            with self.assertRaises(FileExistsError):b.save(p,{})
            with self.assertRaises(ValueError):b.save(Path(d)/'nan',dict(x=float('nan')))

    def test_28_real_process_failure_preserved(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            r=b.monitor([sys.executable,'-c','raise SystemExit(7)'],d,d)
        self.assertEqual(r['returncode'],7);self.assertFalse(r['parent_validation_completed'])

    def test_29_real_timeout_does_not_become_crash_or_success(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            r=b.monitor([sys.executable,'-c','import time;time.sleep(30)'],d,d,timeout=.05)
        self.assertTrue(r['timed_out']);self.assertFalse(r['parent_validation_completed'])

    def test_30_zero_exit_requires_complete_receipt(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            r=b.monitor([sys.executable,'-c','pass'],d,d)
        self.assertFalse(r['parent_validation_completed'])

    def test_31_receipt_exact_role_work_and_rechecks(self):
        with tempfile.TemporaryDirectory() as d,contextlib.redirect_stdout(io.StringIO()):
            b.save(Path(d)/'worker-result.json',dict(role=b.ROLE,worker_completed=True,parent_loader_calls=1,
                  scientific_training_steps=0,model_forward_calls=0,reference_recheck_completed=True,parent_validation_completed=True))
            r=b.monitor([sys.executable,'-c','pass'],d,d)
        self.assertTrue(r['parent_validation_completed'])

    def test_32_controller_one_candidate_and_no_auto_science(self):
        with tempfile.TemporaryDirectory() as d,patch.object(b,'guard'),patch.object(b,'prerequisite'),\
             patch.object(b,'monitor',return_value=dict(timed_out=True)) as m,contextlib.redirect_stdout(io.StringIO()):
            root=Path(d);out=root/'runs/r4';b.run(root,out,'a'*40);self.assertEqual(m.call_count,1)
            self.assertEqual(json.loads((out/'diagnostic-report.json').read_text())['scientific_status'],'NOT_JUDGED')

    def test_33_output_outside_runs_rejected(self):
        with tempfile.TemporaryDirectory() as d,patch.object(b,'guard'),patch.object(b,'prerequisite'),self.assertRaises(ValueError):
            b.run(Path(d),Path(d)/'elsewhere','a'*40)

    def test_34_source_has_no_training_or_validator_cache(self):
        import inspect
        src=inspect.getsource(b.worker)
        for name in ("'_call_impl'","'__init__'","'run'","'runtime_preflight'","'fit'","'make_models'"):self.assertIn(name,src)
        tree=ast.parse(inspect.getsource(b.evaluate_parent));calls=[n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)]
        self.assertEqual(calls.count('load_parent'),1);self.assertIn('recheck',calls)
        self.assertNotIn('fit',calls);self.assertNotIn('runtime_preflight',calls)

    def test_35_progress_records_bytes_not_walltime_ratio(self):
        values=[]
        with tempfile.TemporaryDirectory() as d,b.LockedHashes(b.reference_sha,FixtureLease,values.append) as cache:
            p=Path(d)/'a';p.write_bytes(b'abc');cache.sha(p);cache.pulse(force=True);cache.recheck()
        self.assertGreater(len(values),0);self.assertIn('stream_bytes',values[-1]);self.assertNotIn('speedup',values[-1])

    def test_36_launcher_guard_precedes_log_and_never_full_run(self):
        text=(ROOT/'tools/invoke_c324_locked_hash_r4.ps1').read_text(encoding='utf-8')
        self.assertLess(text.index('STALE_EXPECTED_HEAD'),text.index('$log ='))
        self.assertLess(text.index('STALE_RECOVERY'),text.index('$log ='))
        self.assertIn('publish_experiment_log.ps1',text);self.assertNotIn('run_c324.ps1',text)
        self.assertIn('-X faulthandler',text)

    def test_37_recovery_dispatch_keeps_all_parent_paths(self):
        import re
        text=(ROOT/'tools/invoke_c324.ps1').read_text(encoding='utf-8')
        self.assertIn("LOCKED_HASH_R4 = 'tools\\invoke_c324_locked_hash_r4.ps1'",text)
        self.assertIn('RECOVERY_PARSE_ERROR',text)
        nums=[int(n) for n in re.findall(r'Join-Path \$Root "runs\\c(\d{3})-',text)]
        self.assertEqual(nums,list(range(323,273,-1)))
        self.assertLess(text.index('LOCKED_HASH_R4'),text.index('$preflightLog ='))


if __name__=='__main__':unittest.main()
