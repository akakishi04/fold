"""C324-R2 bounded import/bytecode diagnostic. Never starts the scientific run."""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import sysconfig
import time
import types

ROLE = 'C324-R2-NATIVE-DIAGNOSTIC'
FAILED_EXECUTION = '47ccd303f4382b7938db639e86aeb151e1f83af1'
FAILED_PUBLICATION = '68397de27b4c538ddbd22dc2209fddb7afbc2409'
FAILED_LOG_SHA256 = '8a5e28af87430010931afef2b2da3b61590f32930bee2967daff37c8db6a3271'
BRANCH = 'feat/sft-target-loss'
TARGET = 'fold_lm.v05_benchmarks.model_c242_balanced_recombination'
BENCHMARK = 'fold_lm.v05_benchmarks.model_c324_interior_coverage_training'
REPEATS = 4096
CONTEXT_CALLS = 3
WORKER_TIMEOUT = 120
SCIENTIFIC_TREES = ('fold_lm', 'fold_reasoning', 'tests_lm')
ENV_KEYS = ('PYTHON_GIL', 'PYTHON_JIT', 'PYTHONMALLOC', 'PYTHONPYCACHEPREFIX',
            'PYTHONDONTWRITEBYTECODE', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'KMP_DUPLICATE_LIB_OK')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def emit(name, value):
    print(name + ' = ' + json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False), flush=True)


def file_sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def dump_new(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, sort_keys=True, ensure_ascii=True, allow_nan=False)
        stream.write('\n')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.STDOUT).decode('utf-8').strip()


def guard(root, head):
    require(len(head) == 40 and all(c in '0123456789abcdef' for c in head), 'invalid expected HEAD')
    require(git(root, 'branch', '--show-current') == BRANCH, 'wrong branch')
    require(git(root, 'rev-parse', 'HEAD') == head, 'stale expected HEAD')
    require(not git(root, 'status', '--porcelain', '--untracked-files=no'), 'dirty tracked tree')
    # No scientific tree is allowed to differ from the failed, already-tested execution.
    require(not git(root, 'diff', '--name-only', FAILED_EXECUTION, head, '--', *SCIENTIFIC_TREES),
            'scientific source changed during diagnostic-only recovery')


def code_signature(code):
    """Compare executable structure without modifying or executing any code object."""
    def constant(v):
        if isinstance(v, types.CodeType):
            return ['code', code_signature(v)]
        if isinstance(v, tuple):
            return ['tuple', [constant(x) for x in v]]
        if isinstance(v, frozenset):
            return ['frozenset', sorted((constant(x) for x in v), key=repr)]
        if isinstance(v, bytes):
            return ['bytes', v.hex()]
        return [type(v).__name__, repr(v)]
    fields = ('co_argcount', 'co_posonlyargcount', 'co_kwonlyargcount', 'co_nlocals',
              'co_stacksize', 'co_flags', 'co_names', 'co_varnames', 'co_freevars',
              'co_cellvars', 'co_name', 'co_qualname', 'co_firstlineno')
    value = {name: getattr(code, name) for name in fields}
    for name in ('co_code', 'co_linetable', 'co_exceptiontable'):
        value[name] = getattr(code, name).hex()
    value['co_consts'] = [constant(v) for v in code.co_consts]
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def source_function(path, name):
    # Compiles source to inspect a function; does not exec the compiled module.
    module = compile(Path(path).read_bytes(), str(Path(path).resolve()), 'exec', dont_inherit=True,
                     optimize=sys.flags.optimize)
    functions = [v for v in module.co_consts if isinstance(v, types.CodeType) and v.co_name == name]
    require(len(functions) == 1, 'source function missing or ambiguous')
    return functions[0]


def runtime_info():
    return dict(python=sys.version, executable=sys.executable, platform=platform.platform(),
                implementation=sys.implementation.name, cache_tag=sys.implementation.cache_tag,
                gil_enabled=getattr(sys, '_is_gil_enabled', lambda: None)(),
                gil_disabled_build=sysconfig.get_config_var('Py_GIL_DISABLED'),
                debug_build=sysconfig.get_config_var('Py_DEBUG'), optimize=sys.flags.optimize,
                pycache_prefix=sys.pycache_prefix, dont_write_bytecode=sys.dont_write_bytecode,
                environment={k: os.environ[k] for k in ENV_KEYS if k in os.environ})


def cache_record(path, folder):
    """Preserve targeted preexisting .pyc bytes; never delete or unmarshal them."""
    path = Path(path)
    if not path.is_file():
        return dict(path=str(path), exists=False)
    size = path.stat().st_size
    require(size <= 16 * 1024 * 1024, 'target cache too large to preserve')
    raw = path.read_bytes()
    name = 'observed-' + hashlib.sha256(str(path).encode()).hexdigest()[:16] + '.pyc'
    with (Path(folder) / name).open('xb') as stream:
        stream.write(raw)
    return dict(path=str(path), exists=True, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                magic=raw[:4].hex(), expected_magic=importlib.util.MAGIC_NUMBER.hex(),
                preserved_file=name)


def worker(root, output):
    """Import-only probe: runtime libraries, one source check, bounded import calls."""
    sys.path.insert(0, str(root))
    emit('runtime_before_import', runtime_info())
    import torch
    import numpy
    from unittest.mock import patch
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    emit('runtime_libraries', dict(torch=str(torch.__version__), numpy=numpy.__version__,
                                  torch_origin=torch.__file__, numpy_origin=numpy.__file__,
                                  gil_enabled=getattr(sys, '_is_gil_enabled', lambda: None)()))
    def forbidden(*args, **kwargs):
        raise RuntimeError('R2 diagnostic forbids models, optimizers and tensor archives')
    with contextlib.ExitStack() as stack:
        stack.enter_context(patch.object(torch.nn.Module, '_call_impl', side_effect=forbidden))
        stack.enter_context(patch.object(torch.optim.Optimizer, '__init__', side_effect=forbidden))
        stack.enter_context(patch.object(torch, 'load', side_effect=forbidden))
        emit('target_import', 'BEGIN')
        module = importlib.import_module(TARGET)
        origin = Path(module.__file__).resolve()
        require(origin.is_relative_to(root), 'target resolved outside repository')
        cached = cache_record(module.__cached__, output) if module.__cached__ else dict(exists=False)
        loaded = code_signature(module.parent_module.__code__)
        compiled = code_signature(source_function(origin, 'parent_module'))
        evidence = dict(source_file=str(origin), source_sha256=file_sha(origin), cache=cached,
                        loaded_code_sha256=loaded, compiled_code_sha256=compiled,
                        source_matches_loaded=(loaded == compiled))
        emit('target_code_evidence', evidence)
        require(loaded == compiled, 'loaded parent_module bytecode differs from current source')
        target_parent = importlib.import_module('fold_lm.v05_benchmarks.model_c241_assignment_holdout')
        emit('parent_module_probe', dict(phase='BEGIN', calls=REPEATS))
        for _ in range(REPEATS):
            require(module.parent_module() is target_parent, 'wrong parent module identity')
        require(code_signature(module.parent_module.__code__) == loaded, 'code changed during probe')
        emit('parent_module_probe', dict(phase='END', calls=REPEATS))
        b = importlib.import_module(BENCHMARK)
        stack.enter_context(patch.object(b, 'load_parent', side_effect=forbidden))
        stack.enter_context(patch.object(b, 'precheck', side_effect=forbidden))
        stack.enter_context(patch.object(b, 'run', side_effect=forbidden))
        stack.enter_context(patch.object(b, 'runtime_preflight', side_effect=forbidden))
        emit('context_import_probe', dict(phase='BEGIN', calls=CONTEXT_CALLS))
        for _ in range(CONTEXT_CALLS):
            require(len(b.context()) == 6, 'C324 context contract')
        emit('context_import_probe', dict(phase='END', calls=CONTEXT_CALLS))
    result = dict(role=ROLE, diagnostic_worker_completed=True, target=evidence,
                  parent_module_calls=REPEATS, context_calls=CONTEXT_CALLS,
                  scientific_training_steps=0, model_forward_calls=0, parent_artifact_verifications=0)
    dump_new(output / 'worker-result.json', result)
    emit('diagnostic_worker_result', result)


def worker_command(executable, script, root, output, fresh):
    args = [str(executable), '-B', '-X', 'faulthandler', '-u']
    if fresh:
        # New empty prefix + -B: no old cache reads from source directories, no cache writes.
        prefix = Path(output) / 'empty-pycache-prefix'
        prefix.mkdir(exist_ok=False)
        args += ['-X', 'pycache_prefix=' + str(prefix)]
    return args + [str(script), '--worker', '--root', str(root), '--output-dir', str(output)]


def run_worker(command, root, output, timeout=WORKER_TIMEOUT):
    start = time.monotonic()
    out, err = Path(output) / 'stdout.log', Path(output) / 'stderr.log'
    timed_out = False
    with out.open('xb') as stdout, err.open('xb') as stderr:
        proc = subprocess.Popen(command, cwd=root, stdout=stdout, stderr=stderr)
        try:
            while True:
                try:
                    proc.wait(timeout=min(10, max(.01, timeout - (time.monotonic() - start))))
                    break
                except subprocess.TimeoutExpired:
                    elapsed = time.monotonic() - start
                    emit('worker_heartbeat', dict(pid=proc.pid, elapsed_seconds=round(elapsed, 3)))
                    if elapsed >= timeout:
                        timed_out = True
                        proc.kill()
                        proc.wait()
                        break
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
    result = dict(returncode=proc.returncode, returncode_hex=f'0x{proc.returncode & 0xffffffff:08X}',
                  timed_out=timed_out, elapsed_seconds=round(time.monotonic()-start, 3),
                  stdout_sha256=file_sha(out), stderr_sha256=file_sha(err))
    for label, path in (('stdout', out), ('stderr', err)):
        raw = path.read_bytes()
        emit('worker_' + label, dict(bytes=len(raw), truncated=len(raw) > 98304,
                                     text=raw[:98304].decode('utf-8', errors='backslashreplace')))
    saved = Path(output) / 'worker-result.json'
    if saved.is_file():
        payload = json.loads(saved.read_text(encoding='utf-8'))
        require(payload.get('role') == ROLE and payload.get('scientific_training_steps') == 0,
                'invalid worker diagnostic receipt')
        result['worker_result'] = payload
    result['completed'] = (proc.returncode == 0 and not timed_out and 'worker_result' in result)
    return result


def run(root, output, expected_head):
    root, output = Path(root).resolve(), Path(output).resolve()
    guard(root, expected_head)
    require(output.is_relative_to(root / 'runs') and output != root / 'runs', 'diagnostic output must be inside runs')
    output.mkdir(parents=True, exist_ok=False)
    emit('execution_role', ROLE)
    emit('scientific_execution_requested', False)
    emit('failed_scientific_execution_head', FAILED_EXECUTION)
    emit('failed_publication_commit', FAILED_PUBLICATION)
    emit('diagnostic_parent_runtime', runtime_info())
    results = {}
    # Exactly two probe processes, not a retry-until-success loop. Continue to collect both outcomes.
    for label, fresh in (('existing_cache', False), ('fresh_source_cache_path', True)):
        folder = output / label
        folder.mkdir()
        command = worker_command(sys.executable, Path(__file__).resolve(), root, folder, fresh)
        emit('worker_begin', dict(label=label, cache_policy='fresh empty prefix' if fresh else 'existing lookup policy',
                                  timeout_seconds=WORKER_TIMEOUT))
        results[label] = run_worker(command, root, folder)
        emit('worker_end', dict(label=label, **results[label]))
    guard(root, expected_head)
    report = dict(role=ROLE, commit_sha=expected_head, failed_execution_head=FAILED_EXECUTION,
                  failed_log_sha256=FAILED_LOG_SHA256, diagnostic_completed=True, workers=results,
                  scientific_execution_requested=False, scientific_training_steps=0,
                  scientific_status='NOT_JUDGED', next_action='STOP_FOR_REVIEW_NO_SCIENTIFIC_AUTORETRY',
                  interpretation='Short import probes do not reproduce the complete 50-parent validator; success is not a crash fix.')
    dump_new(output / 'diagnostic-report.json', report)
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
        worker(args.root.resolve(), args.output_dir.resolve())
    else:
        require(args.expected_head is not None, 'expected HEAD required')
        run(args.root, args.output_dir, args.expected_head)


if __name__ == '__main__':
    main()
