"""C324-R5: bounded qualification of seven verifiers on a read-locked snapshot.

No scientific run. Each verifier body executes on its first exact request. Only
validated metadata is retained; every caller receives a fresh deep copy. R4's
native Windows leases remain held until the final uncached reference reread.
"""
from __future__ import annotations
import argparse
import contextlib
import copy
import functools
import hashlib
import importlib
import importlib.util
import inspect
import json
import math
import os
from pathlib import Path
import random
import subprocess
import sys
import threading
import time
from unittest.mock import patch

ROLE = 'C324-R5-VERIFIED-SESSION-QUALIFICATION'
R4_EXECUTION = '9b8ef0895899d12fa17b244d766cfa5f3c431dc6'
R4_PUBLICATION = 'a443d7b3b9db6202cf4edcdc98ecedab930aea72'
R4_LOG_SHA = 'e83f4878f25a4555c3fee4aef2281c4b37f8d423de761f3ff50a5b2f73eb964a'
R4_PATH = 'tools/c324_locked_hash_r4.py'
R4_BLOB = '6459b1f6e4051fbfc54db2894f7abe3a7521df3a'
TIMEOUT = 600
MAX_ENTRIES = 16
MAX_METADATA_BYTES = 64 * 1024 * 1024
TARGETS = {
    'model_c316_single_mix_replication': '3d15bda5b0c4f3f487548cd6b92d3b1281febb76',
    'model_c317_query_endpoint_probe': '7ef1736df78b5dd883a331c434f5f82f1eb8ab92',
    'model_c318_readout_branch_isolation': '5d48dd2866b8e10a286cb5d3991e6f3ea24f952d',
    'model_c319_trained_last_readout': '8222ddc165464b8acb84380f47d397504308a9df',
    'model_c320_unequal_name_lengths': '5e183c330c883d8c44d9cd66ac2b89365517f9cc',
    'model_c321_interior_name_order': '6c55bedbfb0373ce809e3bd62a73260adaf65212',
    'model_c322_saved_query_contrast': 'c93fb85922c5907c424698897de4af2888f81f77',
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def emit(name, value):
    print(name + ' = ' + json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False), flush=True)


def save(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, sort_keys=True, ensure_ascii=True, allow_nan=False)
        stream.write('\n')


def load_r4(root):
    spec = importlib.util.spec_from_file_location('_fold_c324_r4_for_r5', Path(root) / R4_PATH)
    require(spec is not None and spec.loader is not None, 'R4 helper unavailable')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prerequisite(root, r4):
    folder = Path(root) / 'docs/experiment-run-logs/c324'
    meta = json.loads((folder / 'latest.json').read_text(encoding='utf-8'))
    log = folder / 'latest.log'
    require(meta.get('experiment_id') == 'C324' and meta.get('execution_head') == R4_EXECUTION
            and meta.get('log_sha256') == R4_LOG_SHA and r4.reference_sha(log) == R4_LOG_SHA
            and log.stat().st_size == meta.get('log_bytes'), 'R4 evidence identity')
    rows = [json.loads(line.split(' = ', 1)[1]) for line in log.read_text(encoding='utf-8').splitlines()
            if line.startswith('diagnostic_report = ')]
    require(len(rows) == 1, 'R4 report count')
    report = rows[0]
    require(report.get('role') == 'C324-R4-LOCKED-HASH-QUALIFICATION'
            and report.get('commit_sha') == R4_EXECUTION and report.get('diagnostic_completed') is True
            and report.get('scientific_training_steps') == 0, 'R4 report contract')
    require(report['worker'].get('timed_out') is True
            and report['worker'].get('parent_validation_completed') is False, 'R4 incomplete qualification')
    return report


def tree_blobs(root, head):
    raw = subprocess.check_output(['git', '-C', str(root), 'ls-tree', '-r', '-z', head])
    result = {}
    for record in raw.split(b'\0'):
        if not record:
            continue
        header, name = record.split(b'\t', 1)
        mode, kind, oid = header.split(b' ')
        if kind == b'blob':
            key = name.decode('utf-8')
            require(key not in result and mode in (b'100644', b'100755'), 'unsupported source tree entry')
            result[key] = oid.decode('ascii')
    return result


def canonical(path):
    return os.path.normcase(str(Path(path).resolve(strict=True)))


def metadata_bytes(value):
    """Type-aware fingerprint; never retain models/tensors or deserialize pickle."""
    seen = set()
    nodes = [0]
    def visit(v, depth=0):
        nodes[0] += 1
        require(depth <= 64 and nodes[0] <= 1000000, 'metadata structure bound')
        t = type(v)
        if v is None:
            return ['none']
        if t is bool:
            return ['bool', v]
        if t is int:
            return ['int', str(v)]
        if t is float:
            require(math.isfinite(v), 'nonfinite verifier metadata')
            return ['float', v.hex()]
        if t is str:
            return ['str', v]
        if t in (tuple, list, dict):
            require(id(v) not in seen, 'cyclic verifier metadata')
            seen.add(id(v))
            try:
                if t is dict:
                    require(all(type(k) is str for k in v), 'non-string metadata key')
                    return ['dict', [[k, visit(x, depth+1)] for k, x in v.items()]]
                return [t.__name__, [visit(x, depth+1) for x in v]]
            finally:
                seen.remove(id(v))
        if t.__module__.startswith('numpy'):
            import numpy as np
            require(isinstance(v, np.generic) and v.dtype.kind in 'bifu' and bool(np.isfinite(v)),
                    'unsupported numpy metadata')
            return ['numpy_scalar', v.dtype.str, v.tobytes().hex()]
        raise ValueError('non-metadata verifier return:' + t.__module__ + '.' + t.__qualname__)
    raw = json.dumps(visit(value), ensure_ascii=True, allow_nan=False, separators=(',', ':')).encode('ascii')
    require(len(raw) <= MAX_METADATA_BYTES, 'metadata byte bound')
    return raw


class FrozenInputs:
    """All registered inputs are leased BEFORE any verifier result can be reused."""
    def __init__(self, cache):
        self.cache = cache
        self.allowed = set()
        self.frozen = False

    def freeze(self, expected):
        require(not self.frozen and expected, 'snapshot already frozen or empty')
        merged = {}
        for path, wanted in expected:
            key = canonical(path)
            require(type(wanted) is str and len(wanted) == 64, 'bad input digest')
            require(key not in merged or merged[key] == wanted, 'conflicting snapshot aliases')
            merged[key] = wanted
        for key, wanted in merged.items():
            require(self.cache.sha(key) == wanted, 'snapshot byte mismatch:' + key)
        self.allowed = set(merged)
        self.frozen = True
        self.check()
        return merged

    def check(self):
        require(self.frozen and not self.cache.closed, 'inactive input snapshot')
        for key in self.allowed:
            require(key in self.cache.entries, 'snapshot lease missing')
            self.cache.entries[key][0].check()

    def sha(self, path):
        require(self.frozen and canonical(path) in self.allowed, 'unregistered hash dependency:' + str(path))
        return self.cache.sha(path)


class VerifiedSession:
    """Memoize exact verifier requests, with immutable inputs and isolated outputs."""
    def __init__(self, guard, state, progress=lambda value: None, max_entries=MAX_ENTRIES,
                 max_bytes=MAX_METADATA_BYTES):
        self.guard, self.state, self.progress = guard, state, progress
        self.max_entries, self.max_bytes = max_entries, max_bytes
        self.entries, self.active, self.counts = {}, set(), {}
        self.owner, self.closed, self.bytes = threading.get_ident(), False, 0

    def wrap(self, name, original, source_identity):
        signature, code = inspect.signature(original), original.__code__
        require(tuple(signature.parameters) == ('outdir', 'summaries', 'expected_head'), 'verifier signature drift')
        @functools.wraps(original)
        def wrapped(*args, **kwargs):
            require(not self.closed and threading.get_ident() == self.owner, 'closed/concurrent verifier session')
            require(original.__code__ is code, 'verifier code mutated')
            bound = signature.bind(*args, **kwargs)
            out = canonical(bound.arguments['outdir'])
            parents = tuple(canonical(p) for p in bound.arguments['summaries'])
            head = bound.arguments['expected_head']
            require(type(head) is str, 'invalid verifier HEAD')
            key = (name, source_identity, out, parents, head)
            self.guard()
            state = self.state()
            row = self.counts.setdefault(name, dict(requests=0, executions=0, reused=0, failures=0))
            row['requests'] += 1
            if key in self.entries:
                stored, fingerprint, context = self.entries[key]
                require(context == state, 'verifier runtime context changed')
                require(hashlib.sha256(metadata_bytes(stored)).hexdigest() == fingerprint, 'stored metadata mutated')
                value = copy.deepcopy(stored)
                require(metadata_bytes(value) == metadata_bytes(stored), 'metadata copy changed')
                row['reused'] += 1
                self.progress(dict(verifier=name, event='REUSE', **row))
                return value
            require(key not in self.active and len(self.entries) + len(self.active) < self.max_entries,
                    'recursive request or verifier entry bound')
            self.active.add(key)
            row['executions'] += 1
            self.progress(dict(verifier=name, event='EXECUTE', **row))
            try:
                # Canonical ordered values avoid consuming a generator before the original call.
                value = original(Path(out), [Path(p) for p in parents], head)
                self.guard()
                require(self.state() == state, 'verifier changed RNG/runtime context')
                require(type(value) is tuple and len(value) == 2 and type(value[0]) is dict, 'verifier return contract')
                raw = metadata_bytes(value)
                require(self.bytes + len(raw) <= self.max_bytes, 'session metadata memory bound')
                stored = copy.deepcopy(value)
                require(metadata_bytes(stored) == raw, 'metadata copy mismatch')
                self.entries[key] = stored, hashlib.sha256(raw).hexdigest(), state
                self.bytes += len(raw)
                self.progress(dict(verifier=name, event='COMPLETED', metadata_bytes=len(raw), **row))
                return value  # stored is already independent from this first caller
            except BaseException:
                row['failures'] += 1
                raise
            finally:
                self.active.remove(key)
        return wrapped

    def close(self):
        self.closed = True
        self.entries.clear()
        self.active.clear()
        self.bytes = 0


def runtime_state(torch, np):
    # No CUDA initialization, model forward, randomness consumption or thread changes.
    n = np.random.get_state()
    payload = (random.getstate(), n[0], n[1].tobytes().hex(), n[2:],
               torch.random.get_rng_state().numpy().tobytes().hex(), torch.get_num_threads(),
               torch.get_default_dtype().__repr__(), torch.is_grad_enabled(),
               torch.are_deterministic_algorithms_enabled())
    return hashlib.sha256(repr(payload).encode()).hexdigest()


def build_snapshot(root, paths, b, cache, blobs):
    require(cache.sha(paths[0]) == b.PARENT_SHA, 'accepted C323 summary hash')
    parent = b.read_json(paths[0])
    b.validate_parent(parent)
    pins = parent['source_blobs']
    require(all(blobs.get(p) == h for p, h in pins.items()), 'inherited source blob changed')
    expected = list(parent['input_sha256'].items())
    expected += list(zip(paths, b.parent_hashes(b.context()), strict=True))
    for artifact in parent['artifacts']:
        path = paths[0].parent / artifact['file']
        require(path.resolve().parent == paths[0].parent and not path.is_symlink(), 'unsafe parent output')
        expected.append((path, artifact['sha256']))
    known = {canonical(p) for p, _ in expected}
    require(all(canonical(root / p) in known for p in pins), 'source bytes absent from snapshot')
    for name, oid in TARGETS.items():
        path = 'fold_lm/v05_benchmarks/' + name + '.py'
        require(pins.get(path) == oid == blobs.get(path), 'target verifier source identity')
    snapshot = FrozenInputs(cache)
    merged = snapshot.freeze(expected)
    # The R4/R5 helpers and active child are protected operational inputs, too.
    for relative in (R4_PATH, 'tools/c324_verified_session_r5.py',
                     'fold_lm/v05_benchmarks/model_c324_interior_coverage_training.py'):
        path = root / relative
        value = cache.sha(path)
        key = canonical(path)
        snapshot.allowed.add(key)
        merged[key] = value
    snapshot.check()
    return snapshot, parent, merged


def worker(root, output, head):
    root, output = Path(root).resolve(), Path(output).resolve()
    require(os.name == 'nt', 'R5 requires native Windows leases; no unlocked fallback')
    sys.path.insert(0, str(root))
    r4 = load_r4(root)
    r4.guard(root, head)
    blobs = tree_blobs(root, head)
    require(blobs.get(R4_PATH) == R4_BLOB, 'R4 locking helper changed')
    api = r4.WinAPI()
    emit('native_lock_probe', r4.lock_probe(api, output))
    import torch
    import numpy as np
    require(sys.version_info[:3] == (3, 13, 15) and str(torch.__version__) == '2.10.0+cu130'
            and np.__version__ == '2.3.5', 'authoritative runtime mismatch')
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    b, audit = importlib.import_module(r4.BENCHMARK), importlib.import_module(r4.AUDIT)
    b.validate_seal()
    paths = r4.parent_paths(root)
    modules = {name: importlib.import_module('fold_lm.v05_benchmarks.' + name) for name in TARGETS}
    original_hash = audit.sha
    originals = {name: module.verify_artifacts for name, module in modules.items()}
    def forbidden(*args, **kwargs):
        raise RuntimeError('R5 qualification forbids model forwards, optimization and science entry')
    with contextlib.ExitStack() as guards:
        guards.enter_context(patch.object(torch.nn.Module, '_call_impl', side_effect=forbidden))
        guards.enter_context(patch.object(torch.optim.Optimizer, '__init__', side_effect=forbidden))
        for name in ('run', 'runtime_preflight', 'fit', 'make_models'):
            guards.enter_context(patch.object(b, name, side_effect=forbidden))
        with r4.LockedHashes(original_hash, lambda p: r4.ReadLease(p, api),
                             progress=lambda row: emit('hash_progress', row)) as cache:
            emit('phase', 'freeze_complete_input_snapshot')
            snapshot, parent, expected = build_snapshot(root, paths, b, cache, blobs)
            save(output / 'snapshot-inputs.json', expected)
            wrappers = {}
            def call_guard():
                snapshot.check()
                for name, module in modules.items():
                    require(module.verify_artifacts is wrappers[name], 'verifier binding changed')
                    module.validate_seal()
            session = VerifiedSession(call_guard, lambda: runtime_state(torch, np),
                                      progress=lambda row: emit('verifier_progress', row))
            for name in modules:
                wrappers[name] = session.wrap(name, originals[name], head + ':' + TARGETS[name])
            started = time.monotonic()
            try:
                with contextlib.ExitStack() as substitutions:
                    substitutions.enter_context(patch.object(audit, 'sha', snapshot.sha))
                    for name, module in modules.items():
                        substitutions.enter_context(patch.object(module, 'verify_artifacts', wrappers[name]))
                    with b.context()[-1].guarded.no_neural():
                        emit('phase', 'one_real_parent_loader_with_verified_reuse')
                        result, data, old, new = b.load_parent(paths)
                require(audit.sha is original_hash and all(modules[n].verify_artifacts is f for n, f in originals.items()),
                        'reference bindings not restored')
                b.validate_parent(result)
                require(result == parent and len(data['TRAIN']) == 192 and len(data['HOLDOUT']) == 96,
                        'parent result/data contract')
                require(set(session.counts) == set(TARGETS) and all(v['executions'] == 1 and v['failures'] == 0
                        for v in session.counts.values()), 'all seven verifier bodies must complete exactly once')
                require(sum(v['reused'] for v in session.counts.values()) > 0, 'no verifier reuse exercised')
                snapshot.check()
                inventory = cache.recheck()
                require(len(inventory) == len(snapshot.allowed), 'final reference inventory incomplete')
                save(output / 'hash-inventory.json', inventory)
                receipt = dict(role=ROLE, worker_completed=True, parent_validation_completed=True,
                    reference_recheck_completed=True, parent_loader_calls=1, scientific_training_steps=0,
                    model_forward_calls=0, scientific_status='NOT_JUDGED', verifier_stats=session.counts,
                    retained_metadata_bytes=session.bytes, hash_stats=dict(cache.stats),
                    snapshot_files=len(snapshot.allowed), snapshot_sha256=r4.reference_sha(output / 'snapshot-inputs.json'),
                    hash_inventory_sha256=r4.reference_sha(output / 'hash-inventory.json'),
                    parent_seconds_including_final_recheck=time.monotonic()-started,
                    parent_experiment=result['experiment_id'], parent_commit=result['commit_sha'],
                    canonical_data_sha256=b.digest(data), original_prompts_sha256=b.digest(old),
                    interior_prompts_sha256=b.digest(new))
            finally:
                session.close()
    r4.guard(root, head)
    save(output / 'worker-result.json', receipt)
    emit('worker_result', receipt)


def monitor(command, root, output, timeout=TIMEOUT):
    output = Path(output)
    started, next_heartbeat, timed_out = time.monotonic(), 10.0, False
    with (output / 'stdout.log').open('xb') as out, (output / 'stderr.log').open('xb') as err:
        proc = subprocess.Popen(command, cwd=root, stdout=out, stderr=err)
        try:
            while proc.poll() is None:
                elapsed = time.monotonic() - started
                remaining = timeout - elapsed
                if remaining <= 0:
                    timed_out = True
                    proc.kill()
                    proc.wait(timeout=10)
                    break
                try:
                    proc.wait(timeout=min(10, remaining))
                except subprocess.TimeoutExpired:
                    elapsed = time.monotonic() - started
                    if elapsed >= next_heartbeat:
                        emit('worker_heartbeat', dict(pid=proc.pid, elapsed_seconds=round(elapsed, 3)))
                        next_heartbeat = elapsed + 10
                    if timeout-elapsed < .02:
                        time.sleep(max(0, timeout-elapsed))
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=10)
    result = dict(returncode=proc.returncode, returncode_hex=f'0x{proc.returncode & 0xffffffff:08X}',
                  timed_out=timed_out, elapsed_seconds=round(time.monotonic()-started, 3),
                  parent_validation_completed=False)
    for name in ('stdout', 'stderr'):
        raw = (output / (name+'.log')).read_bytes()
        result[name+'_sha256'] = hashlib.sha256(raw).hexdigest()
        emit('worker_'+name, dict(bytes=len(raw), text=raw[-131072:].decode('utf-8', errors='backslashreplace'),
                                 truncated=len(raw) > 131072))
    file = output / 'worker-result.json'
    if file.is_file():
        receipt = json.loads(file.read_text(encoding='utf-8'))
        require(receipt.get('role') == ROLE and receipt.get('worker_completed') is True
                and receipt.get('parent_loader_calls') == 1 and receipt.get('scientific_training_steps') == 0
                and receipt.get('model_forward_calls') == 0 and receipt.get('reference_recheck_completed') is True,
                'worker receipt contract')
        result['worker_result'] = receipt
        result['parent_validation_completed'] = (proc.returncode == 0 and not timed_out
                                                 and receipt.get('parent_validation_completed') is True)
    return result


def run(root, output, head):
    root, output = Path(root).resolve(), Path(output).resolve()
    r4 = load_r4(root)
    r4.guard(root, head)
    require(tree_blobs(root, head).get(R4_PATH) == R4_BLOB, 'R4 helper identity')
    prerequisite(root, r4)
    require(output.is_relative_to(root / 'runs') and output != root / 'runs', 'output outside runs')
    output.mkdir(parents=True, exist_ok=False)
    emit('execution_role', ROLE)
    emit('scientific_execution_requested', False)
    emit('qualification_plan', dict(workers=1, wall_time_limit_seconds=TIMEOUT, verifiers=list(TARGETS),
         locked_snapshot=True, persistent_result_cache=False, full_regression=False, training=False))
    command = [sys.executable, '-B', '-X', 'faulthandler', '-u', str(Path(__file__).resolve()),
               '--worker', '--root', str(root), '--output-dir', str(output), '--expected-head', head]
    outcome = monitor(command, root, output)
    r4.guard(root, head)
    report = dict(role=ROLE, commit_sha=head, diagnostic_completed=True, worker=outcome,
                  scientific_status='NOT_JUDGED', scientific_training_steps=0,
                  next_action='STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY',
                  interpretation='Single-session verifier reuse qualification, not a scientific result, proven crash repair or controlled wall-time speedup.')
    save(output / 'diagnostic-report.json', report)
    emit('diagnostic_report', report)
    emit('diagnostic_completed', True)
    emit('scientific_training_started', False)
    emit('action', report['next_action'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--expected-head', required=True)
    parser.add_argument('--worker', action='store_true')
    args = parser.parse_args()
    if args.worker:
        worker(args.root, args.output_dir, args.expected_head)
    else:
        run(args.root, args.output_dir, args.expected_head)


if __name__ == '__main__':
    main()
