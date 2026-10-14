"""C324 R3: bounded stack sampling of ONE real parent validation, never training."""
from __future__ import annotations
import argparse
from collections import Counter
import contextlib
import faulthandler
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import threading
import time
from unittest.mock import patch

ROLE = 'C324-R3-PARENT-PROFILE'
FAILED_EXECUTION = '47ccd303f4382b7938db639e86aeb151e1f83af1'
R2_EXECUTION = '7ca1ce4ae287e58a16d7e13da99fd03fb76ca89f'
R2_LOG_SHA = '1adbf28a1975172eceed6f2b97b57c504d5093164427f6b3dec361854ac11818'
BRANCH = 'feat/sft-target-loss'
TIMEOUT = 180
INTERVAL = 1.0
BENCHMARK = 'fold_lm.v05_benchmarks.model_c324_interior_coverage_training'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def emit(name, value):
    print(name + ' = ' + json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False), flush=True)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for data in iter(lambda: f.read(1048576), b''):
            h.update(data)
    return h.hexdigest()


def save(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, sort_keys=True, ensure_ascii=True, allow_nan=False)
        f.write('\n')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.STDOUT).decode('utf-8').strip()


def guard(root, head):
    require(re.fullmatch('[0-9a-f]{40}', head) is not None, 'invalid HEAD')
    require(git(root, 'branch', '--show-current') == BRANCH, 'wrong branch')
    require(git(root, 'rev-parse', 'HEAD') == head, 'stale HEAD')
    require(not git(root, 'status', '--porcelain', '--untracked-files=no'), 'dirty tracked tree')
    require(not git(root, 'diff', '--name-only', FAILED_EXECUTION, head, '--',
                    'fold_lm', 'fold_reasoning', 'tests_lm', 'tools/run_c324.ps1'), 'changed scientific implementation')


def r2_evidence(root):
    folder = Path(root) / 'docs/experiment-run-logs/c324'
    meta = json.loads((folder / 'latest.json').read_text(encoding='utf-8'))
    log = folder / 'latest.log'
    require(meta.get('experiment_id') == 'C324' and meta.get('execution_head') == R2_EXECUTION
            and meta.get('log_sha256') == R2_LOG_SHA and sha(log) == R2_LOG_SHA
            and log.stat().st_size == meta.get('log_bytes'), 'R2 evidence identity')
    reports = [json.loads(line.split(' = ', 1)[1]) for line in log.read_text(encoding='utf-8').splitlines()
               if line.startswith('diagnostic_report = ')]
    require(len(reports) == 1, 'R2 report inventory')
    r = reports[0]
    require(r.get('role') == 'C324-R2-NATIVE-DIAGNOSTIC' and r.get('diagnostic_completed') is True
            and r.get('scientific_training_steps') == 0 and r.get('commit_sha') == R2_EXECUTION, 'R2 report contract')
    require(set(r['workers']) == {'existing_cache', 'fresh_source_cache_path'}, 'R2 worker inventory')
    for worker in r['workers'].values():
        require(worker.get('completed') is True and worker.get('returncode') == 0
                and worker.get('timed_out') is False and worker['worker_result']['target']['source_matches_loaded'] is True,
                'R2 prerequisite failed')
    return r


def parent_paths(root):
    text = (Path(root) / 'tools/invoke_c324.ps1').read_text(encoding='utf-8')
    pattern = r'\(Join-Path \$Root "runs\\(c(\d{3})-[A-Za-z0-9-]+)\\summary.json"\)'
    matches = re.findall(pattern, text)
    require([int(number) for _, number in matches] == list(range(323, 273, -1)), '50 ordered parent paths')
    paths = [Path(root).resolve() / 'runs' / name / 'summary.json' for name, _ in matches]
    require(len(set(paths)) == 50 and all(p.is_file() for p in paths), 'missing/duplicate parent summary')
    return paths


def describe_stack(frame, root):
    """Names and line numbers only; never inspect frame locals or tensor data."""
    frames = []
    root = str(Path(root).resolve()).replace('\\', '/') + '/'
    for _ in range(160):
        if frame is None:
            break
        filename = frame.f_code.co_filename.replace('\\', '/')
        name = filename[len(root):] if filename.casefold().startswith(root.casefold()) else '<external>/' + filename.rsplit('/', 1)[-1]
        frames.append(dict(file=name, function=frame.f_code.co_name, line=frame.f_lineno))
        frame = frame.f_back
    return frames


class Sampler:
    def __init__(self, root, path, phase, interval=INTERVAL):
        self.root, self.path, self.phase, self.interval = root, Path(path), phase, interval
        self.target = threading.get_ident()
        self.stop_event = threading.Event()
        self.error = None
        self.thread = threading.Thread(target=self.run, name='c324-r3-sampler', daemon=True)

    def run(self):
        started = time.monotonic()
        try:
            with self.path.open('x', encoding='utf-8', buffering=1) as stream:
                while not self.stop_event.is_set():
                    frame = sys._current_frames().get(self.target)
                    try:
                        stack = describe_stack(frame, self.root)
                    finally:
                        del frame
                    row = dict(elapsed_seconds=round(time.monotonic()-started, 3), phase=self.phase[0], stack=stack)
                    stream.write(json.dumps(row, ensure_ascii=True, allow_nan=False) + '\n')
                    stream.flush()
                    self.stop_event.wait(self.interval)
        except BaseException as exc:
            self.error = type(exc).__name__ + ':' + str(exc)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.stop_event.set()
        self.thread.join(timeout=5)
        require(not self.thread.is_alive() and self.error is None, 'sampler failed:' + str(self.error))


def summarize_samples(path):
    path = Path(path)
    phases, nearest, leaves = Counter(), Counter(), Counter()
    last, count, incomplete = [], 0, False
    if not path.exists():
        return dict(samples=0, incomplete_last_line=False, phases={}, nearest_repository_frame=[], leaf_frame=[], last_stack=[])
    raw = path.read_bytes()
    require(len(raw) <= 16 * 1024 * 1024, 'sample log exceeded bound')
    rows = raw.splitlines(keepends=True)
    for index, rawline in enumerate(rows):
        if not rawline.endswith(b'\n'):
            require(index == len(rows)-1, 'incomplete nonterminal sample')
            incomplete = True
            break
        row = json.loads(rawline)
        stack = row['stack']
        require(type(row['phase']) is str and type(stack) is list and len(stack) <= 160, 'sample schema')
        count += 1
        phases[row['phase']] += 1
        if stack:
            leaves[(stack[0]['file'], stack[0]['function'])] += 1
        own = [f for f in stack if f['file'].startswith(('fold_lm/', 'fold_reasoning/'))]
        if own:
            nearest[(own[0]['file'], own[0]['function'])] += 1
        last = stack
    def top(counter):
        return [dict(file=k[0], function=k[1], samples=v) for k,v in counter.most_common(12)]
    return dict(samples=count, incomplete_last_line=incomplete, phases=dict(phases),
                nearest_repository_frame=top(nearest), leaf_frame=top(leaves), last_stack=last[:24])


def worker(root, output):
    import importlib
    root, output = Path(root).resolve(), Path(output).resolve()
    sys.path.insert(0, str(root))
    phase = ['runtime_import']
    emit('worker_runtime', dict(python=sys.version, executable=sys.executable,
                               gil_enabled=getattr(sys, '_is_gil_enabled', lambda: None)(),
                               pycache_prefix=sys.pycache_prefix, dont_write_bytecode=sys.dont_write_bytecode))
    with Sampler(root, output / 'samples.jsonl', phase):
        import torch
        torch.set_num_threads(2)
        torch.use_deterministic_algorithms(True)
        phase[0] = 'benchmark_import'
        emit('phase', phase[0])
        def forbidden(*args, **kwargs):
            raise RuntimeError('R3 diagnostic forbids model forwards and optimizer construction')
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(torch.nn.Module, '_call_impl', side_effect=forbidden))
            stack.enter_context(patch.object(torch.optim.Optimizer, '__init__', side_effect=forbidden))
            b = importlib.import_module(BENCHMARK)
            for name in ('run', 'runtime_preflight', 'fit', 'make_models'):
                stack.enter_context(patch.object(b, name, side_effect=forbidden))
            phase[0] = 'parent_path_and_manifest_check'
            paths = parent_paths(root)
            b.validate_seal()
            phase[0] = 'real_parent_validation'
            emit('phase', phase[0])
            started = time.monotonic()
            # The SAME loader that failed, once. No validator memoization or result substitution.
            with b.context()[-1].guarded.no_neural():
                result, data, old, new = b.load_parent(paths)
            phase[0] = 'parent_validation_returned'
            receipt = dict(role=ROLE, worker_completed=True, parent_validation_completed=True,
                           parent_loader_calls=1, parent_seconds=time.monotonic()-started,
                           parent_experiment=result['experiment_id'], train_rows=len(data['TRAIN']),
                           holdout_rows=len(data['HOLDOUT']), model_forward_calls=0,
                           scientific_training_steps=0, scientific_status='NOT_JUDGED')
            save(output / 'worker-result.json', receipt)
            emit('worker_result', receipt)


def monitor(command, root, output, timeout=TIMEOUT):
    output = Path(output)
    started = time.monotonic()
    timed_out = False
    with (output/'stdout.log').open('xb') as out, (output/'stderr.log').open('xb') as err:
        proc = subprocess.Popen(command, cwd=root, stdout=out, stderr=err)
        try:
            while True:
                remaining = timeout - (time.monotonic()-started)
                if remaining <= 0:
                    timed_out = True
                    proc.kill()
                    proc.wait()
                    break
                try:
                    proc.wait(timeout=min(10, remaining))
                    break
                except subprocess.TimeoutExpired:
                    emit('worker_heartbeat', dict(pid=proc.pid, elapsed_seconds=round(time.monotonic()-started, 3)))
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
    result = dict(returncode=proc.returncode, returncode_hex=f'0x{proc.returncode & 0xffffffff:08X}',
                  timed_out=timed_out, elapsed_seconds=round(time.monotonic()-started, 3),
                  parent_validation_completed=False)
    for name in ('stdout', 'stderr'):
        path = output/(name+'.log')
        raw = path.read_bytes()
        result[name+'_sha256'] = sha(path)
        emit('worker_'+name, dict(bytes=len(raw), text=raw[-32768:].decode('utf-8', errors='backslashreplace'), truncated=len(raw)>32768))
    receipt = output/'worker-result.json'
    if receipt.is_file():
        value = json.loads(receipt.read_text(encoding='utf-8'))
        require(value.get('role') == ROLE and value.get('worker_completed') is True
                and value.get('parent_loader_calls') == 1 and value.get('model_forward_calls') == 0
                and value.get('scientific_training_steps') == 0, 'worker receipt contract')
        result['worker_result'] = value
        result['parent_validation_completed'] = (proc.returncode == 0 and not timed_out
                                                 and value.get('parent_validation_completed') is True)
    result['sampling'] = summarize_samples(output/'samples.jsonl')
    return result


def run(root, output, head):
    root, output = Path(root).resolve(), Path(output).resolve()
    guard(root, head)
    r2_evidence(root)
    require(output.is_relative_to(root/'runs') and output != root/'runs', 'output outside runs')
    output.mkdir(parents=True, exist_ok=False)
    emit('execution_role', ROLE)
    emit('scientific_execution_requested', False)
    command = [sys.executable, '-B', '-X', 'faulthandler', '-u', str(Path(__file__).resolve()),
               '--worker', '--root', str(root), '--output-dir', str(output)]
    emit('probe_plan', dict(workers=1, wall_time_limit_seconds=TIMEOUT, sample_interval_seconds=INTERVAL,
                            parent_loader='C324.load_parent', cache_policy='existing read-only lookup',
                            full_regression=False, training=False, profiler_hooks=False))
    result = monitor(command, root, output)
    guard(root, head)
    report = dict(role=ROLE, commit_sha=head, diagnostic_completed=True, worker=result,
                  scientific_status='NOT_JUDGED', scientific_training_steps=0,
                  next_action='STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY',
                  interpretation='Stack samples locate active frames, not exact call counts or unbiased wall-time shares. Timeout is a bounded observation, not validator failure or science PASS.')
    save(output/'diagnostic-report.json', report)
    emit('diagnostic_report', report)
    emit('diagnostic_completed', True)
    emit('scientific_training_started', False)
    emit('action', report['next_action'])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--expected-head')
    p.add_argument('--worker', action='store_true')
    a = p.parse_args()
    if a.worker:
        worker(a.root, a.output_dir)
    else:
        require(a.expected_head is not None, 'expected HEAD required')
        run(a.root, a.output_dir, a.expected_head)


if __name__ == '__main__':
    faulthandler.enable(all_threads=True)
    main()
