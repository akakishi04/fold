"""C324-R4: qualify lock-backed hash reuse; no scientific training or auto-retry.

Only C175.audit.sha is temporarily replaced. No parent validator/result is cached.
Windows read handles deny write/delete sharing for the entire cache lifetime.
Each miss and the final inventory are compared to the original SHA implementation.
"""
from __future__ import annotations
import argparse
import contextlib
import ctypes
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
from unittest.mock import patch

ROLE = 'C324-R4-LOCKED-HASH-QUALIFICATION'
BRANCH = 'feat/sft-target-loss'
FAILED_EXECUTION = '47ccd303f4382b7938db639e86aeb151e1f83af1'
R3_EXECUTION = '4557a1fb9344596be5faf9750eae1c67e05d0b52'
R3_LOG_SHA = '50da0a826c7a4644bce059a93d0e7598aeef482969cc27bf7c46bf53c4be0e7d'
AUDIT = 'fold_lm.v05_benchmarks.gate_e_c175_frozen_prediction_audit'
AUDIT_PATH = 'fold_lm/v05_benchmarks/gate_e_c175_frozen_prediction_audit.py'
AUDIT_BLOB = 'efd1bb246442fb4f472e33e450c16b192acfa18a'
BENCHMARK = 'fold_lm.v05_benchmarks.model_c324_interior_coverage_training'
TIMEOUT = 300
MAX_FILES = 4096
CHUNK = 1024 * 1024


def require(ok, message):
    if not ok:
        raise ValueError(message)


def emit(name, value):
    print(name + ' = ' + json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False), flush=True)


def reference_sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, sort_keys=True, ensure_ascii=True, allow_nan=False)
        stream.write('\n')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.STDOUT).decode('utf-8').strip()


def guard(root, head):
    require(isinstance(head, str) and re.fullmatch('[0-9a-f]{40}', head), 'invalid HEAD')
    require(git(root, 'branch', '--show-current') == BRANCH, 'wrong branch')
    require(git(root, 'rev-parse', 'HEAD') == head, 'stale HEAD')
    require(not git(root, 'status', '--porcelain', '--untracked-files=no'), 'dirty tracked tree')
    require(not git(root, 'diff', '--name-only', FAILED_EXECUTION, head, '--',
                    'fold_lm', 'fold_reasoning', 'tests_lm', 'tools/run_c324.ps1'), 'scientific source changed')
    require(git(root, 'rev-parse', 'HEAD:' + AUDIT_PATH) == AUDIT_BLOB, 'reference hash implementation changed')


def prerequisite(root):
    folder = Path(root) / 'docs/experiment-run-logs/c324'
    meta = json.loads((folder / 'latest.json').read_text(encoding='utf-8'))
    log = folder / 'latest.log'
    require(meta.get('experiment_id') == 'C324' and meta.get('execution_head') == R3_EXECUTION
            and meta.get('log_sha256') == R3_LOG_SHA and reference_sha(log) == R3_LOG_SHA
            and log.stat().st_size == meta.get('log_bytes'), 'R3 evidence identity')
    reports = [json.loads(line.split(' = ', 1)[1]) for line in log.read_text(encoding='utf-8').splitlines()
               if line.startswith('diagnostic_report = ')]
    require(len(reports) == 1, 'R3 report inventory')
    report = reports[0]
    require(report.get('role') == 'C324-R3-PARENT-PROFILE' and report.get('diagnostic_completed') is True
            and report.get('commit_sha') == R3_EXECUTION and report.get('scientific_training_steps') == 0,
            'R3 report contract')
    worker = report['worker']
    require(worker.get('timed_out') is True and worker.get('parent_validation_completed') is False
            and worker['sampling']['samples'] == 179, 'R3 bounded outcome')
    rows = worker['sampling']['nearest_repository_frame']
    require(sum(row['samples'] for row in rows if row['file'] == AUDIT_PATH and row['function'] == 'sha') == 171,
            'R3 deciding observation')
    return report


def parent_paths(root):
    text = (Path(root) / 'tools/invoke_c324.ps1').read_text(encoding='utf-8')
    matches = re.findall(r'\(Join-Path \$Root "runs\\(c(\d{3})-[A-Za-z0-9-]+)\\summary.json"\)', text)
    require([int(n) for _, n in matches] == list(range(323, 273, -1)), '50 ordered parent paths')
    paths = [Path(root).resolve() / 'runs' / name / 'summary.json' for name, _ in matches]
    require(len(set(paths)) == 50 and all(p.is_file() for p in paths), 'missing/duplicate parent summary')
    return paths


class FileTime(ctypes.Structure):
    _fields_ = [('low', ctypes.c_uint32), ('high', ctypes.c_uint32)]


class FileInfo(ctypes.Structure):
    _fields_ = [('attributes', ctypes.c_uint32), ('creation', FileTime), ('access', FileTime),
                ('write', FileTime), ('volume', ctypes.c_uint32), ('size_high', ctypes.c_uint32),
                ('size_low', ctypes.c_uint32), ('links', ctypes.c_uint32),
                ('index_high', ctypes.c_uint32), ('index_low', ctypes.c_uint32)]


class WinAPI:
    """Native HANDLEs, not CRT file descriptors (the cohort can exceed 512 files)."""
    def __init__(self, library=None):
        self.injected = library is not None
        if library is None:
            require(os.name == 'nt', 'R4 production locking requires Windows; no unlocked fallback')
            library = ctypes.WinDLL('kernel32', use_last_error=True)
        self.lib = library
        signatures = {
            'CreateFileW': ([ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p,
                             ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p], ctypes.c_void_p),
            'GetFileInformationByHandle': ([ctypes.c_void_p, ctypes.POINTER(FileInfo)], ctypes.c_int32),
            'ReadFile': ([ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32,
                          ctypes.POINTER(ctypes.c_uint32), ctypes.c_void_p], ctypes.c_int32),
            'SetFilePointerEx': ([ctypes.c_void_p, ctypes.c_int64, ctypes.c_void_p, ctypes.c_uint32], ctypes.c_int32),
            'CloseHandle': ([ctypes.c_void_p], ctypes.c_int32),
        }
        for name, (args, result) in signatures.items():
            fn = getattr(library, name)
            fn.argtypes, fn.restype = args, result
        require(ctypes.sizeof(FileInfo) == 52, 'Win32 FILE_INFORMATION ABI')

    def error(self):
        if not self.injected:
            return ctypes.WinError(ctypes.get_last_error())
        # This branch is reachable only with an explicitly injected software fixture.
        error = OSError(32, 'simulated Win32 API failure')
        error.winerror = 32
        return error

    def open(self, path, access=0x80000000, share=1):
        name = str(Path(path).absolute())
        if os.name == 'nt' and not name.startswith('\\\\?\\'):
            name = '\\\\?\\UNC\\' + name[2:] if name.startswith('\\\\') else '\\\\?\\' + name
        # OPEN_EXISTING; no writes, no delete-on-close, no inherited handle.
        handle = self.lib.CreateFileW(name, access, share, None, 3, 0x00200080, None)
        if handle is None or handle == ctypes.c_void_p(-1).value:
            raise self.error()
        return handle

    def info(self, handle):
        info = FileInfo()
        if not self.lib.GetFileInformationByHandle(handle, ctypes.byref(info)):
            raise self.error()
        require(not info.attributes & (0x10 | 0x400), 'directory/reparse point is not a hash input')
        return (info.volume, info.index_high, info.index_low, info.size_high, info.size_low,
                info.write.high, info.write.low, info.creation.high, info.creation.low)

    def close(self, handle):
        if not self.lib.CloseHandle(handle):
            raise self.error()

    def digest(self, handle, pulse):
        if not self.lib.SetFilePointerEx(handle, 0, None, 0):
            raise self.error()
        buffer, count, h, total = ctypes.create_string_buffer(CHUNK), ctypes.c_uint32(), hashlib.sha256(), 0
        while True:
            if not self.lib.ReadFile(handle, buffer, CHUNK, ctypes.byref(count), None):
                raise self.error()
            if count.value == 0:
                break
            h.update(buffer.raw[:count.value])
            total += count.value
            pulse(count.value)
        return h.hexdigest(), total


class ReadLease:
    def __init__(self, path, api):
        self.path, self.api, self.handle = Path(path), api, None
        self.handle = api.open(self.path)
        try:
            self.identity = api.info(self.handle)
            self.size = (self.identity[3] << 32) | self.identity[4]
        except BaseException:
            self.close()
            raise

    def check(self):
        require(self.handle is not None and self.api.info(self.handle) == self.identity, 'held file changed')
        other = self.api.open(self.path)
        try:
            require(self.api.info(other) == self.identity, 'input path retargeted')
        finally:
            self.api.close(other)

    def digest(self, pulse):
        self.check()
        value, count = self.api.digest(self.handle, pulse)
        require(count == self.size, 'short/expanded read under lock')
        self.check()
        return value

    def close(self):
        if self.handle is not None:
            handle, self.handle = self.handle, None
            self.api.close(handle)


class LockedHashes:
    """Single-thread, single-session cache with mandatory leases and reference checks."""
    def __init__(self, original, lease_factory, progress=lambda value: None, max_files=MAX_FILES):
        self.original, self.lease_factory, self.progress = original, lease_factory, progress
        self.max_files, self.entries, self.closed = max_files, {}, False
        self.owner, self.started, self.last_progress = threading.get_ident(), time.monotonic(), 0.0
        self.stats = dict(hash_calls=0, cache_hits=0, unique_files=0, stream_bytes=0, reference_bytes=0,
                          logical_reference_bytes=0, final_reference_rechecks=0, phase='parent_validation')

    def pulse(self, stream_bytes=0, force=False):
        self.stats['stream_bytes'] += stream_bytes
        now = time.monotonic()
        if force or now - self.last_progress >= 10:
            self.last_progress = now
            self.progress(dict(self.stats, elapsed_seconds=round(now-self.started, 3)))

    def sha(self, path):
        require(not self.closed and threading.get_ident() == self.owner, 'closed/concurrent hash session')
        path = Path(path).resolve(strict=True)
        key = os.path.normcase(str(path))
        self.stats['hash_calls'] += 1
        if key in self.entries:
            lease, value = self.entries[key]
            lease.check()
            self.stats['cache_hits'] += 1
            self.stats['logical_reference_bytes'] += lease.size
            self.pulse()
            return value
        require(len(self.entries) < self.max_files, 'locked-file bound exceeded; no eviction fallback')
        lease = self.lease_factory(path)
        try:
            value = lease.digest(self.pulse)
            self.stats['reference_bytes'] += lease.size
            require(value == self.original(path), 'miss/reference digest mismatch')
            lease.check()
            self.entries[key] = (lease, value)
        except BaseException:
            lease.close()
            raise
        self.stats['unique_files'] = len(self.entries)
        self.stats['logical_reference_bytes'] += lease.size
        self.pulse()
        return value

    def recheck(self):
        require(not self.closed and threading.get_ident() == self.owner, 'closed/concurrent recheck')
        self.stats['phase'] = 'final_uncached_reference_recheck'
        self.pulse(force=True)
        inventory = []
        for key, (lease, value) in self.entries.items():
            lease.check()
            self.stats['reference_bytes'] += lease.size
            require(self.original(lease.path) == value, 'final/reference digest mismatch')
            lease.check()
            self.stats['final_reference_rechecks'] += 1
            inventory.append(dict(path=key, size=lease.size, sha256=value))
            self.pulse()
        require(len(inventory) == self.stats['unique_files'], 'reference recheck inventory')
        self.pulse(force=True)
        return inventory

    def close(self):
        self.closed = True
        errors = []
        for lease, _ in self.entries.values():
            try:
                lease.close()
            except OSError as exc:
                errors.append(str(exc))
        self.entries.clear()
        require(not errors, 'lease cleanup failed:' + ';'.join(errors))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def lock_probe(api, output):
    path = Path(output) / 'lock-probe.bin'
    with path.open('xb') as stream:
        stream.write(b'FOLD-C324-R4-read-only-lock-probe\n')
    lease = ReadLease(path, api)
    try:
        require(lease.digest(lambda n: None) == reference_sha(path), 'native read/reference parity')
        for access in (0x40000000, 0x00010000):  # Request WRITE and DELETE rights; never mutate data.
            try:
                handle = api.open(path, access=access, share=7)
            except OSError as exc:
                require(getattr(exc, 'winerror', None) == 32, 'probe failed for a reason other than sharing')
            else:
                api.close(handle)
                raise ValueError('write/delete access not blocked by held lease')
    finally:
        lease.close()
    handle = api.open(path, access=0x40000000, share=7)
    api.close(handle)
    return dict(native_lock_probe='PASS', write_access_denied=True, delete_access_denied=True,
                read_compatible=True, released_after_close=True)


def evaluate_parent(b, audit, paths, cache, output):
    original = audit.sha
    require(cache.original is original, 'wrong reference function')
    # Only this low-level primitive is substituted; parent calls and semantic checks stay intact.
    with patch.object(audit, 'sha', cache.sha), b.context()[-1].guarded.no_neural():
        result, data, old, new = b.load_parent(paths)
    require(audit.sha is original, 'reference function not restored')
    b.validate_parent(result)
    require(len(data['TRAIN']) == 192 and len(data['HOLDOUT']) == 96, 'canonical data counts')
    inventory = cache.recheck()
    save(Path(output)/'hash-inventory.json', inventory)
    return dict(parent_experiment=result['experiment_id'], parent_commit=result['commit_sha'],
                train_rows=len(data['TRAIN']), holdout_rows=len(data['HOLDOUT']),
                hash_inventory_sha256=reference_sha(Path(output)/'hash-inventory.json'),
                hash_inventory_count=len(inventory), canonical_data_sha256=b.digest(data),
                original_prompts_sha256=b.digest(old), interior_prompts_sha256=b.digest(new))


def worker(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    require(os.name == 'nt', 'R4 worker requires native Windows locking')
    sys.path.insert(0, str(root))
    emit('worker_runtime', dict(python=sys.version, executable=sys.executable, dont_write_bytecode=sys.dont_write_bytecode))
    api = WinAPI()
    emit('native_lock_probe', lock_probe(api, output))
    import torch
    import numpy
    require(sys.version_info[:3] == (3, 13, 15) and str(torch.__version__) == '2.10.0+cu130'
            and numpy.__version__ == '2.3.5', 'authoritative runtime mismatch; do not reinstall automatically')
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    emit('runtime_libraries', dict(torch=str(torch.__version__), numpy=numpy.__version__))
    b, audit = importlib.import_module(BENCHMARK), importlib.import_module(AUDIT)
    require(Path(audit.__file__).resolve() == root / AUDIT_PATH, 'unexpected audit module origin')
    b.validate_seal()
    paths = parent_paths(root)
    def forbidden(*args, **kwargs):
        raise RuntimeError('R4 qualification forbids model forwards, optimization and scientific entry')
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.object(torch.nn.Module, '_call_impl', side_effect=forbidden))
        stack.enter_context(patch.object(torch.optim.Optimizer, '__init__', side_effect=forbidden))
        for name in ('run', 'runtime_preflight', 'fit', 'make_models'):
            stack.enter_context(patch.object(b, name, side_effect=forbidden))
        cache = LockedHashes(audit.sha, lambda path: ReadLease(path, api),
                             progress=lambda value: emit('hash_progress', value))
        with cache:
            emit('parent_validation', 'BEGIN; candidate locked hashes; one loader call')
            receipt = evaluate_parent(b, audit, paths, cache, output)
            stats = dict(cache.stats)
    receipt.update(role=ROLE, worker_completed=True, parent_validation_completed=True,
                   reference_recheck_completed=True, parent_loader_calls=1, hash_stats=stats,
                   scientific_training_steps=0, model_forward_calls=0, scientific_status='NOT_JUDGED')
    save(output/'worker-result.json', receipt)
    emit('worker_result', receipt)


def monitor(command, root, output, timeout=TIMEOUT):
    output = Path(output)
    start, next_heartbeat, timed_out = time.monotonic(), 10.0, False
    with (output/'stdout.log').open('xb') as out, (output/'stderr.log').open('xb') as err:
        proc = subprocess.Popen(command, cwd=root, stdout=out, stderr=err)
        try:
            while proc.poll() is None:
                elapsed = time.monotonic()-start
                remaining = timeout-elapsed
                if remaining <= 0:
                    timed_out = True
                    proc.kill()
                    proc.wait(timeout=10)
                    break
                try:
                    proc.wait(timeout=min(10, remaining))
                except subprocess.TimeoutExpired:
                    elapsed = time.monotonic()-start
                    if elapsed >= next_heartbeat:
                        emit('worker_heartbeat', dict(elapsed_seconds=round(elapsed, 3), pid=proc.pid))
                        next_heartbeat = elapsed + 10
                    if timeout-elapsed < .02:
                        time.sleep(max(0, timeout-elapsed))
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=10)
    result = dict(returncode=proc.returncode, returncode_hex=f'0x{proc.returncode & 0xffffffff:08X}',
                  timed_out=timed_out, elapsed_seconds=round(time.monotonic()-start, 3),
                  parent_validation_completed=False)
    for name in ('stdout', 'stderr'):
        path = output/(name+'.log')
        raw = path.read_bytes()
        emit('worker_'+name, dict(bytes=len(raw), text=raw[-65536:].decode('utf-8', errors='backslashreplace'), truncated=len(raw)>65536))
        result[name+'_sha256'] = reference_sha(path)
    path = output/'worker-result.json'
    if path.is_file():
        receipt = json.loads(path.read_text(encoding='utf-8'))
        require(receipt.get('role') == ROLE and receipt.get('worker_completed') is True
                and receipt.get('parent_loader_calls') == 1 and receipt.get('scientific_training_steps') == 0
                and receipt.get('model_forward_calls') == 0 and receipt.get('reference_recheck_completed') is True,
                'worker receipt contract')
        result['worker_result'] = receipt
        result['parent_validation_completed'] = proc.returncode == 0 and not timed_out and receipt.get('parent_validation_completed') is True
    return result


def run(root, output, head):
    root, output = Path(root).resolve(), Path(output).resolve()
    guard(root, head)
    prerequisite(root)
    require(output.is_relative_to(root/'runs') and output != root/'runs', 'output outside runs')
    output.mkdir(parents=True, exist_ok=False)
    emit('execution_role', ROLE)
    emit('scientific_execution_requested', False)
    emit('qualification_plan', dict(workers=1, wall_time_limit_seconds=TIMEOUT, max_locked_files=MAX_FILES,
                                   reused='hash digest only', parent_validator_result_cache=False,
                                   full_regression=False, scientific_training=False))
    command = [sys.executable, '-B', '-X', 'faulthandler', '-u', str(Path(__file__).resolve()),
               '--worker', '--root', str(root), '--output-dir', str(output)]
    result = monitor(command, root, output)
    guard(root, head)
    report = dict(role=ROLE, commit_sha=head, diagnostic_completed=True, worker=result,
                  scientific_status='NOT_JUDGED', scientific_training_steps=0,
                  next_action='STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY',
                  interpretation='Lock-backed hash qualification, not proof of native-crash repair or scientific success. Byte counts are logical payload reads, not disk I/O. No measured full-reference wall-time ratio.')
    save(output/'diagnostic-report.json', report)
    emit('diagnostic_report', report)
    emit('diagnostic_completed', True)
    emit('scientific_training_started', False)
    emit('action', report['next_action'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--expected-head')
    parser.add_argument('--worker', action='store_true')
    args = parser.parse_args()
    if args.worker:
        worker(args.root, args.output_dir)
    else:
        require(args.expected_head is not None, 'expected HEAD required')
        run(args.root, args.output_dir, args.expected_head)


if __name__ == '__main__':
    main()
