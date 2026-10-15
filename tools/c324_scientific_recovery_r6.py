"""C324 R6: registered scientific retry with a locked, verified parent snapshot.

The unchanged C324 result is accompanied by a mandatory execution envelope. The
802-source/1501-input union, all 5490 tests and saved semantic reconstruction are
required; the old 792-source scientific summary alone is not an R6 acceptance.
"""
from __future__ import annotations
import argparse
import contextlib
import copy
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

ROLE = 'C324-R6-SCIENTIFIC-RECOVERY'
BRANCH = 'feat/sft-target-loss'
R5_EXECUTION = '1beb6d60f3dd0f7c72f41c9355c96827b8da4e82'
R5_PUBLICATION = 'f7a909f2e1a0b4bd5d03c0a54bcb63519b022b19'
R5_LOG_SHA = '2f89e566132f0ade3660dc7c2aafb6a4946ffaa3d441341af0d39671cd663558'
B_PATH = 'fold_lm/v05_benchmarks/model_c324_interior_coverage_training.py'
B_BLOB = '2fc9e31c7037313a3fadb126af9b153608c0ac6e'
R4_PATH = 'tools/c324_locked_hash_r4.py'
R5_PATH = 'tools/c324_verified_session_r5.py'
R6_PATH = 'tools/c324_scientific_recovery_r6.py'
FIXED = {B_PATH: B_BLOB, R4_PATH: '6459b1f6e4051fbfc54db2894f7abe3a7521df3a',
         R5_PATH: '55ba956a974cc8cf5faca5ecbeaa1c774e40956e',
         'tests_tools/test_c324_locked_hash_r4.py': 'f6d52c5464b967e3a48eefe12f5c83ea65f9f3a8',
         'tests_tools/test_c324_verified_session_r5.py': 'e31845302ae964194be95d24e4465f21e52a39d5',
         'tools/invoke_c324_locked_hash_r4.ps1': 'de55adde3f29f271e6af1bb04137252c040c8168',
         'tools/invoke_c324_verified_session_r5.ps1': '281f9cc724c7413e8a282bf931526a6c5fd45981'}
EXTRA = (R4_PATH, R5_PATH, R6_PATH, 'tools/invoke_c324_scientific_r6.ps1',
         'tests_tools/test_c324_scientific_recovery_r6.py', 'docs/c324-scientific-recovery-r6.md',
         'tests_tools/test_c324_locked_hash_r4.py', 'tests_tools/test_c324_verified_session_r5.py',
         'tools/invoke_c324_locked_hash_r4.ps1', 'tools/invoke_c324_verified_session_r5.ps1')
RECOVERY_MODULES = ('tests_tools.test_c324_locked_hash_r4',
                    'tests_tools.test_c324_verified_session_r5',
                    'tests_tools.test_c324_scientific_recovery_r6')
RECOVERY_COUNTS = (37, 48, 48)
FULL_TESTS = 5490
SOURCE_COUNT, INPUT_COUNT = 802, 1501


def require(ok, message):
    if not ok:
        raise ValueError(message)


def emit(name, value):
    print(name + ' = ' + json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False), flush=True)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    def unique(pairs):
        result = {}
        for k, v in pairs:
            require(k not in result, 'duplicate JSON key')
            result[k] = v
        return result
    def invalid(value):
        raise ValueError('nonfinite JSON:' + value)
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=invalid)


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


def source_bytes(path, oid):
    raw = Path(path).read_bytes()
    def blob(data):
        return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    normalized = raw.replace(b'\r\n', b'\n')
    require(blob(raw) == oid or (raw == normalized.replace(b'\n', b'\r\n') and blob(normalized) == oid),
            'source bytes differ from registered Git blob:' + str(path))
    return raw


def helper(root, relative, oid, name):
    source_bytes(Path(root) / relative, oid)
    require(git(root, 'rev-parse', 'HEAD:' + relative) == oid, 'helper source pin')
    spec = importlib.util.spec_from_file_location(name, Path(root) / relative)
    require(spec is not None and spec.loader is not None, 'helper import spec')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prerequisite(root):
    folder = Path(root) / 'docs/experiment-run-logs/c324'
    meta, log = read(folder / 'latest.json'), folder / 'latest.log'
    require(meta.get('experiment_id') == 'C324' and meta.get('execution_head') == R5_EXECUTION
            and meta.get('log_sha256') == R5_LOG_SHA and sha(log) == R5_LOG_SHA
            and meta.get('log_bytes') == log.stat().st_size, 'R5 evidence identity')
    reports = [json.loads(s.split(' = ', 1)[1]) for s in log.read_text(encoding='utf-8').splitlines()
               if s.startswith('diagnostic_report = ')]
    require(len(reports) == 1, 'R5 report inventory')
    report = reports[0]
    worker = report['worker']; receipt = worker['worker_result']
    require(report['commit_sha'] == R5_EXECUTION and report['role'] == 'C324-R5-VERIFIED-SESSION-QUALIFICATION'
            and report['diagnostic_completed'] is True and report['scientific_training_steps'] == 0,
            'R5 diagnostic contract')
    require(worker['returncode'] == 0 and worker['timed_out'] is False
            and worker['parent_validation_completed'] is True and receipt['reference_recheck_completed'] is True
            and receipt['snapshot_files'] == receipt['hash_stats']['final_reference_rechecks'] == 1486,
            'R5 did not finish verification')
    rows = receipt['verifier_stats']
    require(len(rows) == 7 and all(v['executions'] == 1 and v['failures'] == 0 for v in rows.values())
            and sum(v['reused'] for v in rows.values()) == 9, 'R5 verifier completion')
    return report


class GitBatch:
    """Exact immutable Git blob replies; all nonmatching commands still use Git."""
    def __init__(self, root, pins):
        self.root, self.pins = Path(root).resolve(), dict(pins)
        ids = sorted(set(pins.values()))
        require(all(re.fullmatch('[0-9a-f]{40}', x) for x in ids), 'bad source OID')
        data = subprocess.check_output(['git', '-C', str(root), 'cat-file', '--batch'],
                                       input=('\n'.join(ids) + '\n').encode('ascii'))
        require(len(data) <= 128 * 1024 * 1024, 'source payload bound')
        self.blobs = self.parse(data, ids)
        self.hits = 0

    @staticmethod
    def parse(data, ids):
        result, offset = {}, 0
        for wanted in ids:
            end = data.index(b'\n', offset)
            oid, kind, size = data[offset:end].split()
            require(oid.decode() == wanted and kind == b'blob', 'batch blob identity')
            size = int(size); offset = end + 1
            raw = data[offset:offset+size]; offset += size
            require(len(raw) == size and data[offset:offset+1] == b'\n', 'batch blob framing')
            require(hashlib.sha1(b'blob ' + str(size).encode() + b'\0' + raw).hexdigest() == wanted,
                    'batch blob content')
            result[wanted] = raw; offset += 1
        require(offset == len(data), 'extra batch output')
        return result

    def wrap(self, original, binary):
        def wrapped(root, *args):
            reply = None
            if Path(root).resolve() == self.root:
                if len(args) == 2 and args[0] == 'rev-parse' and args[1].startswith('HEAD:'):
                    name = args[1][5:]
                    if name in self.pins:
                        reply = (self.pins[name] + '\n').encode('ascii')
                elif len(args) == 3 and args[:2] == ('cat-file', 'blob'):
                    reply = self.blobs.get(args[2])
            if reply is None:
                return original(root, *args)
            self.hits += 1
            return reply if binary else reply.decode('utf-8').strip()
        return wrapped


class ParentData:
    """Parsed canonical JSON only, tied to one live read-locked snapshot.

Unlike a model result cache this data is independent of training RNG/grad state.
The real loader must preserve RNG/context on construction; each read is a copy.
"""
    def __init__(self, paths, value, check, encode):
        self.paths = tuple(str(Path(p).resolve()) for p in paths)
        require(type(value) is tuple and len(value) == 4 and all(type(x) is dict for x in value), 'parent data contract')
        self.encode, self.check = encode, check
        self.value = copy.deepcopy(value)
        self.fingerprint = hashlib.sha256(encode(self.value)).hexdigest()
        self.calls, self.closed = 0, False

    def load(self, paths):
        require(not self.closed, 'closed parent data')
        require(tuple(str(Path(p).resolve()) for p in paths) == self.paths, 'different ordered parent request')
        self.check()
        require(hashlib.sha256(self.encode(self.value)).hexdigest() == self.fingerprint, 'stored parent data changed')
        value = copy.deepcopy(self.value)
        require(self.encode(value) == self.encode(self.value), 'parent copy changed')
        self.calls += 1
        emit('verified_parent_data', dict(read=self.calls, real_parent_loader_calls=1))
        return value

    def close(self):
        self.closed = True
        self.value = None


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from flatten(test)
        else:
            yield test


def combined_suite(b, root):
    base = list(flatten(b.regression_suite(root)))
    require(len(base) == 5357 and len(b.regression_modules(root)) == 210, 'base regression inventory')
    extra = []
    for name, expected in zip(RECOVERY_MODULES, RECOVERY_COUNTS, strict=True):
        tests = list(flatten(unittest.defaultTestLoader.loadTestsFromName(name)))
        require(len(tests) == expected, 'recovery test inventory:' + name)
        extra.extend(tests)
    tests = base + extra; ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) == FULL_TESTS and b.EXCLUDED not in ids, 'combined regression inventory')
    return unittest.TestSuite(tests)


def regression_child(root, folder, head):
    guard(root, head)
    b = importlib.import_module('fold_lm.v05_benchmarks.model_c324_interior_coverage_training')
    suite = combined_suite(b, root)
    emit('regression_suite', dict(base=5357, recovery=sum(RECOVERY_COUNTS), selected=FULL_TESTS, modules=213))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    receipt = dict(tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                   skipped=len(result.skipped), successful=result.wasSuccessful(), commit_sha=head)
    save(folder / 'regression-result.json', receipt)
    emit('regression_result', receipt)
    require(result.wasSuccessful() and result.testsRun == FULL_TESTS and not result.skipped, 'full regression failed')
    guard(root, head)


def subprocess_run(root, folder, head, mode):
    """Stream child logs while retaining native failure evidence. Never auto-retry."""
    log = folder / (mode + '.log')
    command = [sys.executable, '-B', '-X', 'faulthandler', '-u', str(Path(__file__).resolve()),
               '--root', str(root), '--folder', str(folder), '--expected-head', head, '--mode', mode]
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    started = time.monotonic(); next_heartbeat = started + 10
    with log.open('xb') as out:
        proc = subprocess.Popen(command, cwd=root, stdout=out, stderr=subprocess.STDOUT, env=env)
        try:
            with log.open('r', encoding='utf-8', errors='backslashreplace') as live:
                while proc.poll() is None:
                    text = live.read()
                    if text:
                        sys.stdout.write(text); sys.stdout.flush()
                    now = time.monotonic()
                    if now >= next_heartbeat:
                        emit('worker_heartbeat', dict(phase=mode, elapsed_seconds=round(now-started, 3)))
                        next_heartbeat = now + 10
                    time.sleep(.2)
                text = live.read()
                if text:
                    sys.stdout.write(text); sys.stdout.flush()
        finally:
            if proc.poll() is None:
                proc.kill(); proc.wait(timeout=10)
    emit('process_exit', dict(phase=mode, decimal=proc.returncode,
                             hexadecimal=f'0x{proc.returncode & 0xffffffff:08X}', log=str(log)))
    require(proc.returncode == 0, 'C324 R6 ' + mode + ' process failed; preserve log; no automatic retry')


def validate_regression(receipt, head):
    require(receipt == dict(tests=FULL_TESTS, failures=0, errors=0, skipped=0, successful=True, commit_sha=head),
            'complete regression receipt required')


def prepare_parent(b, r4, r5, root, head, paths, folder, cache, blobs):
    snapshot, parent, expected = r5.build_snapshot(root, paths, b, cache, blobs)
    pins = dict(parent['source_blobs'])
    for relative in (*b.OWN, *EXTRA):
        require(relative not in parent['source_blobs'], 'source ownership overlap')
        require(relative in blobs, 'untracked required source:' + relative)
        pins[relative] = blobs[relative]
        raw = source_bytes(root / relative, blobs[relative])
        wanted = hashlib.sha256(raw).hexdigest()
        require(cache.sha(root / relative) == wanted, 'source changed while locking')
        key = r5.canonical(root / relative)
        snapshot.allowed.add(key); expected[key] = wanted
    require(len(pins) == SOURCE_COUNT and len(expected) == INPUT_COUNT, 'R6 complete protection inventory')
    batch = GitBatch(root, pins)
    for relative, oid in pins.items():
        raw = (root / relative).read_bytes(); canonical = batch.blobs[oid]
        require(raw == canonical or raw == canonical.replace(b'\n', b'\r\n'), 'source snapshot bytes')
    snapshot.check()
    audit = importlib.import_module(r4.AUDIT)
    modules = {name: importlib.import_module('fold_lm.v05_benchmarks.' + name) for name in r5.TARGETS}
    originals = {name: m.verify_artifacts for name, m in modules.items()}
    wrappers = {}
    def check():
        snapshot.check()
        for name, module in modules.items():
            require(module.verify_artifacts is wrappers[name], 'verifier binding changed')
            module.validate_seal()
    torch = importlib.import_module('torch'); np = importlib.import_module('numpy')
    session = r5.VerifiedSession(check, lambda: r5.runtime_state(torch, np), progress=lambda row: emit('verifier_progress', row))
    for name in modules:
        wrappers[name] = session.wrap(name, originals[name], head + ':' + r5.TARGETS[name])
    state = r5.runtime_state(torch, np)
    def forbidden(*args, **kwargs):
        raise ValueError('model execution forbidden during parent reconstruction')
    try:
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(audit, 'sha', snapshot.sha))
            stack.enter_context(patch.object(torch.nn.Module, '_call_impl', side_effect=forbidden))
            stack.enter_context(patch.object(torch.optim.Optimizer, '__init__', side_effect=forbidden))
            for name, module in modules.items():
                stack.enter_context(patch.object(module, 'verify_artifacts', wrappers[name]))
            with b.context()[-1].guarded.no_neural():
                value = b.load_parent(paths)
        require(r5.runtime_state(torch, np) == state, 'parent loader changes RNG/runtime')
        require(set(session.counts) == set(r5.TARGETS) and all(v['executions'] == 1 and v['failures'] == 0
                for v in session.counts.values()), 'seven verified bodies required')
        require(sum(v['reused'] for v in session.counts.values()) > 0, 'verified reuse not exercised')
        require(value[0] == parent, 'accepted parent differs')
        stats = copy.deepcopy(session.counts)
    finally:
        session.close()
    data = ParentData(paths, value, snapshot.check, r5.metadata_bytes)
    save(folder / 'snapshot-inputs.json', expected)
    return snapshot, pins, expected, batch, data, stats


def scientific_worker(root, folder, head):
    worker_started = time.monotonic()
    guard(root, head)
    require(os.name == 'nt', 'native Windows read leases required')
    r4 = helper(root, R4_PATH, FIXED[R4_PATH], '_c324_r4_for_r6')
    r5 = helper(root, R5_PATH, FIXED[R5_PATH], '_c324_r5_for_r6')
    blobs = r5.tree_blobs(root, head)
    require(all(blobs.get(k) == v for k, v in FIXED.items()), 'registered reference source changed')
    for relative, wanted in FIXED.items():
        source_bytes(root / relative, wanted)
    api = r4.WinAPI(); emit('native_lock_probe', r4.lock_probe(api, folder))
    import torch
    import numpy as np
    require(sys.version_info[:3] == (3, 13, 15) and str(torch.__version__) == '2.10.0+cu130'
            and np.__version__ == '2.3.5', 'authoritative runtime mismatch')
    torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    b = importlib.import_module('fold_lm.v05_benchmarks.model_c324_interior_coverage_training')
    b.validate_seal(); paths = r4.parent_paths(root)
    audit = importlib.import_module(r4.AUDIT)
    out = folder / 'science'
    with r4.LockedHashes(audit.sha, lambda p: r4.ReadLease(p, api),
                         progress=lambda row: emit('hash_progress', row)) as cache:
        emit('phase', 'locked_parent_reconstruction')
        parent_started = time.monotonic()
        snapshot, pins, expected, batch, data, verifier_stats = prepare_parent(b, r4, r5, root, head, paths, folder, cache, blobs)
        parent_elapsed = time.monotonic() - parent_started
        emit('parent_snapshot_ready', dict(seconds=parent_elapsed, protected_inputs=INPUT_COUNT))
        try:
            with patch.object(b, 'load_parent', data.load), patch.object(b, 'git', batch.wrap(b.git, False)), \
                 patch.object(audit, 'git', batch.wrap(audit.git, True)):
                emit('phase', 'native_TRAIN_and_gradient_preflight')
                b.runtime_preflight(paths, root)
                emit('phase', 'full_regression_unmodified_separate_process')
                subprocess_run(root, folder, head, 'regression')
                regression = read(folder / 'regression-result.json'); validate_regression(regression, head)
                guard(root, head); snapshot.check()
                emit('phase', 'scientific_training_10_models')
                result = b.run(summaries=paths, output_dir=out, expected_head=head)
                emit('phase', 'saved_checkpoint_and_measurement_verification')
                verified, metrics = b.verify_artifacts(out, paths, head)
                require(verified == result, 'saved scientific result differs')
                primary = {k: v for k, v in pins.items() if k not in EXTRA}
                require(result['source_blobs'] == primary and len(primary) == 792, 'primary/extended source union')
                require(all(expected.get(r5.canonical(k)) == v for k, v in result['input_sha256'].items())
                        and len(result['input_sha256']) == 1491, 'primary/extended input union')
                parent_reads = data.calls
        finally:
            data.close()
        emit('phase', 'final_uncached_input_recheck')
        snapshot.check(); inventory = cache.recheck()
        require(len(inventory) == INPUT_COUNT and {r['path']: r['sha256'] for r in inventory} == expected,
                'final reference inventory incomplete')
        hash_stats = dict(cache.stats)
    guard(root, head)
    envelope = dict(schema='fold-c324-r6-execution-envelope-v1', role=ROLE, commit_sha=head,
        scientific_summary_sha256=sha(out / 'summary.json'), scientific_status=result['status'],
        source_blobs=pins, input_sha256=expected, source_count=SOURCE_COUNT, input_count=INPUT_COUNT,
        base_scientific_manifest_sha256=b.MANIFEST_SHA, regression=regression,
        verifier_stats=verifier_stats, real_parent_loader_calls=1, parsed_parent_reads=parent_reads,
        final_reference_rechecks=INPUT_COUNT, saved_semantic_reconstruction=True,
        hash_stats=hash_stats, git_batch_hits=batch.hits, scientific_work=b.WORK,
        r5_diagnostic_execution=R5_EXECUTION, r5_log_sha256=R5_LOG_SHA,
        timing=dict(parent_snapshot_seconds=parent_elapsed, worker_seconds=time.monotonic()-worker_started))
    save(folder / 'execution-envelope.json', envelope)
    emit('summary', str(out / 'summary.json')); emit('summary_sha256', envelope['scientific_summary_sha256'])
    emit('scientific_status', result['status']); emit('candidate_gate', result['validation_summary']['candidate_gate'])
    for row in result['validation_summary']['seed_results']: emit('C324 seed', row)
    for row in result['validation_summary']['paired_comparisons']: emit('C324 pair', row)
    for row in metrics: emit('C324 metrics', row)
    emit('execution_envelope', dict(path=str(folder / 'execution-envelope.json'), sha256=sha(folder / 'execution-envelope.json'),
                                  source_count=SOURCE_COUNT, input_count=INPUT_COUNT, regression_tests=FULL_TESTS))
    emit('persisted_training_evaluation', 'PASS; checkpoint_replays = 10')


def verify_envelope(root, folder, head):
    """Fresh process checks the complete saved envelope and every input byte."""
    guard(root, head)
    envelope = read(folder / 'execution-envelope.json')
    require(envelope['schema'] == 'fold-c324-r6-execution-envelope-v1' and envelope['role'] == ROLE
            and envelope['commit_sha'] == head, 'execution envelope identity')
    require(envelope['source_count'] == len(envelope['source_blobs']) == SOURCE_COUNT
            and envelope['input_count'] == len(envelope['input_sha256']) == INPUT_COUNT
            and set(EXTRA) <= set(envelope['source_blobs']), 'execution envelope protection inventory')
    validate_regression(envelope['regression'], head)
    require(envelope['real_parent_loader_calls'] == 1 and envelope['parsed_parent_reads'] >= 3
            and envelope['final_reference_rechecks'] == INPUT_COUNT and envelope['saved_semantic_reconstruction'] is True,
            'incomplete scientific execution envelope')
    require(all(envelope['source_blobs'].get(k) == v for k, v in FIXED.items()), 'envelope reference pins')
    rows = envelope['verifier_stats']
    require(len(rows) == 7 and all(v['executions'] == 1 and v['failures'] == 0 for v in rows.values())
            and sum(v['reused'] for v in rows.values()) > 0, 'envelope verifier completeness')
    require(envelope['hash_stats']['final_reference_rechecks'] == INPUT_COUNT, 'envelope final hash checks')
    for relative, oid in envelope['source_blobs'].items():
        source_bytes(root / relative, oid)
    r5 = helper(root, R5_PATH, FIXED[R5_PATH], '_c324_verify_r5')
    blobs = r5.tree_blobs(root, head)
    require(all(blobs.get(k) == v for k, v in envelope['source_blobs'].items()), 'envelope source pins changed')
    for name, wanted in envelope['input_sha256'].items():
        require(sha(name) == wanted, 'envelope input changed:' + name)
    out = folder / 'science'
    require(sha(out / 'summary.json') == envelope['scientific_summary_sha256'], 'scientific summary bytes changed')
    b = importlib.import_module('fold_lm.v05_benchmarks.model_c324_interior_coverage_training')
    result = read(out / 'summary.json'); b.validate_result(result)
    require(result['commit_sha'] == head and result['status'] == envelope['scientific_status']
            and b.MANIFEST_SHA == envelope['base_scientific_manifest_sha256'] and b.WORK == envelope['scientific_work'],
            'scientific contract or identity changed')
    require(result['source_blobs'] == {k:v for k,v in envelope['source_blobs'].items() if k not in EXTRA},
            'saved primary/source envelope mismatch')
    require(len(result['input_sha256']) == 1491 and all(envelope['input_sha256'].get(r5.canonical(k)) == v
            for k,v in result['input_sha256'].items()), 'saved primary/input envelope mismatch')
    for artifact in result['artifacts']:
        path = b.child(out, artifact['file'])
        require(sha(path) == artifact['sha256'] and path.stat().st_size == artifact['serialized_bytes'], 'saved artifact changed')
    guard(root, head)
    emit('execution_envelope_verified', dict(source_pins=SOURCE_COUNT, protected_inputs=INPUT_COUNT, full_tests=FULL_TESTS))


def run(root, folder, head):
    guard(root, head); prerequisite(root)
    require(folder.is_relative_to(root / 'runs') and folder != root / 'runs', 'output outside runs')
    folder.mkdir(parents=True, exist_ok=False)
    emit('execution_role', ROLE); emit('scientific_execution_requested', True)
    complete = False
    try:
        subprocess_run(root, folder, head, 'science')
        subprocess_run(root, folder, head, 'verify')
        complete = True
    finally:
        guard(root, head)
        emit('run_execution_valid', complete)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--expected-head', required=True)
    parser.add_argument('--mode', choices=('run', 'science', 'regression', 'verify'), default='run')
    args = parser.parse_args(); root, folder = args.root.resolve(), args.folder.resolve()
    sys.path.insert(0, str(root))
    actions = dict(run=run, science=scientific_worker, regression=regression_child, verify=verify_envelope)
    actions[args.mode](root, folder, args.expected_head)


if __name__ == '__main__':
    main()
