"""C331 native frozen probe; preserve accepted C330 R1.2 and all test evidence."""
from __future__ import annotations
import argparse
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

BRANCH = 'feat/sft-target-loss'
PARENT_HEAD = 'a92b0096949c4176f793dc2b57e910149222efb0'
PARENT_FOLDER = 'runs/c330-localization-688c9a321f204989b6a694820eaab9bd'
PARENT_SUMMARY = 'f7c1a6567f2ab9929528722bfc699b8228275e8cb185c31f1de87e5260278691'
PARENT_ENVELOPE = 'ad30fc8f64775ebe93f9c2650bc74dc809583c877397a94889745b3e388381ad'
RECOVERY_SHA = 'cb09791f16e446ad2e1116981700c5be26997865d2da2eef89e76acdad1df8b9'
BASE_IDS_SHA = 'f7c7f355197393a53f0d9d8f3f4c8a044e4b365719a4894090017e206e709dc6'
R_PATH = 'tools/c330_recovery_r1.py'
R_BLOB = '30a986f3e6437fae7fc62bb08f67e1654f28e4d7'
TEST_MODULE = 'tests_lm.test_v05_c331_frozen_first_mean_query'


def spec():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c331_frozen_first_mean_query')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def emit(name, value):
    print(name+' = '+json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False), flush=True)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    def unique(items):
        result = {}
        for k, v in items:
            require(k not in result, 'duplicate JSON key'); result[k] = v
        return result
    def invalid(v):
        raise ValueError('nonfinite JSON:'+v)
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=invalid)


def save(path, value):
    with Path(path).open('xb') as stream:
        stream.write(spec().blob(value))


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.STDOUT).decode('utf-8').strip()


def canonical(path):
    return os.path.normcase(str(Path(path).resolve(strict=True)))


def source_bytes(path, oid):
    raw = Path(path).read_bytes(); normalized = raw.replace(b'\r\n', b'\n')
    def h(v):
        return hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest()
    require(h(raw) == oid or (raw == normalized.replace(b'\n', b'\r\n') and h(normalized) == oid), 'source bytes:'+str(path))


def active(text):
    m = re.search(r'(?ms)^## Formal state\s+(.*?)(?=^## |\Z)', text)
    return bool(m and re.findall(r'C(\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)', m[1]) == ['331'])


def guard(root, head):
    require(type(head) is str and re.fullmatch('[0-9a-f]{40}', head), 'execution HEAD')
    require(git(root, 'branch', '--show-current') == BRANCH and git(root, 'rev-parse', 'HEAD') == head, 'branch/HEAD')
    require(not git(root, 'status', '--porcelain', '--untracked-files=no'), 'dirty tracked tree')
    require(active((root/'docs/experiment-ledger-and-handoff.md').read_text(encoding='utf-8')), 'C331 uniquely ACTIVE')


def helpers(root):
    require(git(root, 'rev-parse', 'HEAD:'+R_PATH) == R_BLOB, 'accepted recovery pin')
    source_bytes(root/R_PATH, R_BLOB)
    loader = importlib.util.spec_from_file_location('_c331_recovery', root/R_PATH)
    require(loader is not None and loader.loader is not None, 'recovery loader')
    r = importlib.util.module_from_spec(loader); loader.loader.exec_module(r); r.seal()
    require(r.RECOVERY_SHA == RECOVERY_SHA and r.REVISION == 'C330-R1.2', 'accepted recovery revision')
    base = r.load_base(root)
    _, _, _, runtime, legacy, locks, _ = base.helpers(root)
    return r, base, runtime, legacy, locks


def receipt(head, count):
    return dict(commit_sha=head, tests=count, failures=0, errors=0, skipped=0, successful=True)


def check_regression(value, head, count):
    require(spec().blob(value) == spec().blob(receipt(head, count)), 'full regression receipt')


def parent_contract(result, envelope, r, base):
    s = base.spec(); s.validate_seal(); s.check_summary(result['validation_summary'])
    require(result['schema'] == 'fold-c330-diagnostic-v1' and envelope['schema'] == 'fold-c330-execution-envelope-v1'
            and result['experiment_id'] == s.EXPERIMENT_ID and result['stage'] == s.STAGE
            and result['commit_sha'] == envelope['commit_sha'] == PARENT_HEAD, 'parent identity')
    require(result['status'] == envelope['scientific_status'] == 'PASS' and result['diagnostic_execution_valid'] is True
            and result['capability_gate_applicable'] is False and result['gate_f_candidate'] is False
            and result['production_adoption'] is False, 'parent diagnostic semantics')
    require(result['execution_revision'] == envelope['execution_revision'] == 'C330-R1.2'
            and result['recovery_manifest_sha256'] == envelope['recovery_manifest_sha256'] == RECOVERY_SHA
            and spec().blob(result['recovery_manifest']) == spec().blob(envelope['recovery_manifest']) == spec().blob(r.contract()), 'parent recovery semantics')
    require(result['manifest_sha256'] == envelope['manifest_sha256'] == s.MANIFEST_SHA
            and envelope['scientific_work'] == s.WORK and envelope['scientific_summary_sha256'] == PARENT_SUMMARY, 'parent science seal')
    require(envelope['source_count'] == len(envelope['source_blobs']) == 841
            and envelope['input_count'] == len(envelope['input_sha256']) == 1596
            and result['source_blobs'] == envelope['source_blobs'] and result['input_sha256'] == envelope['input_sha256'], 'complete accepted unions')
    require(envelope['source_blobs'].get(R_PATH) == R_BLOB
            and envelope['parent_summary_sha256'] == base.PARENT_SUMMARY and envelope['parent_envelope_sha256'] == base.PARENT_ENVELOPE
            and envelope['immediate_parent_semantic_reconstruction'] is True and envelope['ancestor_semantic_reruns'] == 0
            and envelope['saved_semantic_reconstruction'] is True and envelope['final_reference_rechecks'] == 1596
            and envelope['hash_stats']['final_reference_rechecks'] == 1596, 'parent completed verification')
    check_regression(envelope['regression'], PARENT_HEAD, 5850)
    require(result['validation_summary']['parent_candidate_gate'] is False
            and result['validation_summary']['parent_paired_success_count'] == 1, 'preserved C329 negative')


def parent_test_files(folder, envelope, hash_file):
    """The443 supplementary outputs are required, not an optional small receipt."""
    bound = envelope['regression_isolation']
    expected = {'regression-plan-r1.json': bound['plan_sha256'],
                'regression-isolation-r1.json': bound['evidence_sha256'],
                'regression-result.json': bound['result_sha256']}
    require(bound['tests'] == 5850 and bound['modules'] == 220, 'parent regression scope')
    for name, wanted in expected.items():
        require(hash_file(folder/name) == wanted, 'parent test evidence:'+name)
    isolation = read(folder/'regression-isolation-r1.json')
    require(len(isolation['modules']) == 220, 'parent module inventory')
    for i, row in enumerate(isolation['modules']):
        require(type(row['index']) is int and row['index'] == i, 'parent module ordering')
        expected[f'module-{i:03d}.json'] = row['receipt_sha256']
        expected[f'module-{i:03d}.log'] = row['log_sha256']
    require(len(expected) == 443, 'complete parent supplementary inventory')
    for name, wanted in expected.items():
        require(hash_file(folder/name) == wanted, 'parent module bytes:'+name)
    return {canonical(folder/name): wanted for name, wanted in expected.items()}


def snapshot(root, h, hash_file):
    r, base, _, legacy, _ = h; s = spec(); s.validate_seal()
    folder = root/PARENT_FOLDER; out = folder/'science'
    require(not folder.is_symlink() and not out.is_symlink(), 'parent path link')
    require(hash_file(out/'summary.json') == PARENT_SUMMARY and hash_file(folder/'execution-envelope.json') == PARENT_ENVELOPE, 'exact parent bytes')
    result = read(out/'summary.json'); envelope = read(folder/'execution-envelope.json'); parent_contract(result, envelope, r, base)
    inputs = dict(envelope['input_sha256'])
    require(all(canonical(k) == k for k in inputs) and len({canonical(k) for k in inputs}) == 1596, 'parent canonical paths')
    for path, wanted in inputs.items():
        require(hash_file(path) == wanted, 'inherited input changed:'+path)
    added = legacy.descriptors(out, result['artifacts'], base.spec().OUTPUTS, hash_file)
    added.update({canonical(out/'summary.json'): PARENT_SUMMARY, canonical(folder/'execution-envelope.json'): PARENT_ENVELOPE})
    extra = parent_test_files(folder, envelope, hash_file)
    require(not set(added) & set(extra), 'parent output collision'); added.update(extra)
    require(len(added) == 449 and not set(added) & set(inputs), 'complete449parent outputs'); inputs.update(added)
    expected_plan = r.build_plan(root, PARENT_HEAD, base)
    verified = r.verify_regression(folder, PARENT_HEAD, expected_plan)
    require(spec().blob(verified) == spec().blob(envelope['regression_isolation']), 'parent full regression reconstruction')
    tree = legacy.tree_blobs(root); pins = dict(envelope['source_blobs'])
    require(all(tree.get(k) == v for k, v in pins.items()), 'inherited source changed')
    for name in s.OWN:
        require(name in tree and name not in pins and canonical(root/name) not in inputs, 'child source overlap')
        pins[name] = tree[name]; inputs[canonical(root/name)] = hash_file(root/name)
    require(len(pins) == s.SOURCE_COUNT and len(inputs) == s.INPUT_COUNT, 'child protection counts')
    for name, oid in pins.items():
        source_bytes(root/name, oid)
        require(inputs.get(canonical(root/name)) == hash_file(root/name), 'source input binding')
    return result, envelope, pins, inputs


def parent_semantics(root, h, parent, inputs):
    _, base, _, _, _ = h; p = base.spec(); source_out = root/base.PARENT_FOLDER/'science'
    for name in ('dataset.json', 'original-prompts.json', 'interior-prompts.json', 'evaluations.pt', 'trained-models.pt'):
        require(canonical(source_out/name) in inputs, 'unprotected source checkpoint/data')
    b = spec().source().base(); cx = b.context()
    with cx[-1].guarded.no_neural():
        value = p.semantic_recheck(root/PARENT_FOLDER/'science', source_out, read)
        require(spec().blob(value) == spec().blob(parent['validation_summary']), 'immediate C330 semantics')
        data = read(source_out/'dataset.json'); old = read(source_out/'original-prompts.json'); new = read(source_out/'interior-prompts.json')
        require(b.digest(data) == b.DATA_SHA and b.digest(old) == b.PROMPTS_SHA
                and b.digest(new) == b.digest(cx[2].new_prompts(data)), 'canonical inherited prompts')
        cx[-1].c.p267.validate_data(data); cx[2].check_prompts(data, old, new, cx[3], cx[-1])
    emit('accepted_parent_semantics', dict(diagnostic=True, parent_files=449, inherited_regression=5850, model_forwards=0, ancestor_semantic_reruns=0))
    return source_out, cx


def validate_plan(plan, head, r):
    require(set(plan) == {'schema', 'commit_sha', 'manifest_sha256', 'test_ids_sha256', 'groups'}
            and plan['schema'] == 'fold-c331-regression-plan-v1' and plan['commit_sha'] == head
            and plan['manifest_sha256'] == spec().MANIFEST_SHA, 'C331 test plan identity')
    groups = plan['groups']; require(type(groups) is list and len(groups) == spec().MODULES, 'module count')
    ids = []; modules = []
    for g in groups:
        require(set(g) == {'module', 'test_ids'} and r.allowed_module(g['module'])
                and type(g['test_ids']) is list and g['test_ids']
                and all(type(v) is str and v.startswith(g['module']+'.') for v in g['test_ids']), 'module ID provenance')
        modules.append(g['module']); ids.extend(g['test_ids'])
    require(len(ids) == len(set(ids)) == spec().FULL_TESTS and len(modules) == len(set(modules))
            and r.EXCLUDED not in ids and groups[-1]['module'] == TEST_MODULE
            and len(groups[-1]['test_ids']) == spec().OWN_TESTS, 'complete test inventory')
    require(spec().digest(ids[:-spec().OWN_TESTS]) == BASE_IDS_SHA
            and spec().digest(ids) == plan['test_ids_sha256'], 'unchanged5850test IDs')


def build_plan(root, head, h):
    r, base, _, _, _ = h
    prior = r.build_plan(root, head, base)
    own = list(r.flatten(unittest.defaultTestLoader.loadTestsFromName(TEST_MODULE)))
    require(len(own) == spec().OWN_TESTS and all(type(t).__module__ == TEST_MODULE for t in own), 'own test loader')
    groups = prior['groups']+[dict(module=TEST_MODULE, test_ids=[t.id() for t in own])]
    value = dict(schema='fold-c331-regression-plan-v1', commit_sha=head, manifest_sha256=spec().MANIFEST_SHA,
                 test_ids_sha256=spec().digest([v for g in groups for v in g['test_ids']]), groups=groups)
    validate_plan(value, head, r)
    return value


def command(root, folder, head, mode):
    return [sys.executable, '-B', '-X', 'faulthandler', '-u', str(Path(__file__).resolve()),
            '--root', str(root), '--folder', str(folder), '--expected-head', head, '--mode', mode]


def run_logged(root, args, logfile, phase):
    start = time.monotonic(); beat = start+10
    with logfile.open('xb') as target:
        process = subprocess.Popen(args, cwd=root, stdout=target, stderr=subprocess.STDOUT, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        try:
            with logfile.open('r', encoding='utf-8', errors='backslashreplace') as live:
                while process.poll() is None:
                    text = live.read()
                    if text:
                        sys.stdout.write(text); sys.stdout.flush()
                    now = time.monotonic()
                    if now >= beat:
                        emit('worker_heartbeat', dict(phase=phase, elapsed_seconds=round(now-start, 3))); beat = now+10
                    time.sleep(.2)
                text = live.read()
                if text:
                    sys.stdout.write(text); sys.stdout.flush()
        finally:
            if process.poll() is None:
                process.kill(); process.wait(timeout=10)
    emit('process_exit', dict(phase=phase, pid=process.pid, decimal=process.returncode, hexadecimal=f'0x{process.returncode & 0xffffffff:08X}'))
    require(process.returncode == 0, 'C331 '+phase+' failed; no automatic retry')
    return process.pid


def module_child(root, folder, head, index, plan_sha):
    guard(root, head); spec().validate_seal(); r = helpers(root)[0]
    require(sha(folder/'regression-plan.json') == plan_sha, 'module plan bytes')
    plan = read(folder/'regression-plan.json'); validate_plan(plan, head, r)
    require(type(index) is int and 0 <= index < spec().MODULES, 'module index')
    g = plan['groups'][index]; process = dict(pid=os.getpid(), parent_pid=os.getppid())
    marker = dict(index=index, module=g['module'], tests=len(g['test_ids']), **process)
    emit('regression_module_begin', marker); result = r.execute_module(g['module'], g['test_ids'])
    # Reuse the accepted generic module-evidence ABI, bound to the NEW HEAD/plan.
    save(folder/f'module-{index:03d}.json', dict(schema='fold-c330-r1-module-v2', commit_sha=head,
         plan_sha256=plan_sha, index=index, module=g['module'], result=result, **process))
    r.check_module(result, g); guard(root, head)
    require(process == dict(pid=os.getpid(), parent_pid=os.getppid()), 'module process identity changed')
    emit('regression_module_complete', marker)


def collect_tests(folder, head, plan, r, run_module):
    validate_plan(plan, head, r); save(folder/'regression-plan.json', plan); ph = sha(folder/'regression-plan.json')
    evidence = []; total = 0; started = time.monotonic()
    for i, g in enumerate(plan['groups']):
        emit('regression_progress', dict(completed=total, total=spec().FULL_TESTS, index=i, module=g['module']))
        launcher = run_module(i, ph); path = folder/f'module-{i:03d}.json'; log = folder/f'module-{i:03d}.log'; row = read(path)
        relation = r.validate_module_evidence(row, g, head, i, ph, launcher, log)
        evidence.append(dict(index=i, launcher_pid=launcher, pid=row['pid'], parent_pid=row['parent_pid'], relation=relation,
                             exit_code=0, receipt_sha256=sha(path), log_sha256=sha(log)))
        total += row['result']['tests']
    require(total == spec().FULL_TESTS, 'all tests completed')
    save(folder/'regression-evidence.json', dict(schema='fold-c331-regression-v1', commit_sha=head, plan_sha256=ph,
         test_ids_sha256=plan['test_ids_sha256'], modules=evidence))
    save(folder/'regression-result.json', receipt(head, total))
    emit('regression_result', dict(**receipt(head, total), modules=spec().MODULES, seconds=round(time.monotonic()-started, 3)))


def verify_tests(folder, head, plan, r):
    validate_plan(plan, head, r)
    require(spec().blob(read(folder/'regression-plan.json')) == spec().blob(plan), 'planned inventory')
    v = read(folder/'regression-evidence.json'); ph = sha(folder/'regression-plan.json')
    require(set(v) == {'schema', 'commit_sha', 'plan_sha256', 'test_ids_sha256', 'modules'}
            and v['schema'] == 'fold-c331-regression-v1' and v['commit_sha'] == head and v['plan_sha256'] == ph
            and v['test_ids_sha256'] == plan['test_ids_sha256'] and len(v['modules']) == spec().MODULES, 'test evidence identity')
    successful = []
    for i, (item, group) in enumerate(zip(v['modules'], plan['groups'], strict=True)):
        require(set(item) == {'index', 'launcher_pid', 'pid', 'parent_pid', 'relation', 'exit_code', 'receipt_sha256', 'log_sha256'}
                and type(item['index']) is int and item['index'] == i and type(item['exit_code']) is int and item['exit_code'] == 0, 'module completion')
        path = folder/f'module-{i:03d}.json'; log = folder/f'module-{i:03d}.log'
        require(sha(path) == item['receipt_sha256'] and sha(log) == item['log_sha256'], 'module evidence bytes')
        row = read(path); relation = r.validate_module_evidence(row, group, head, i, ph, item['launcher_pid'], log)
        require(type(item['pid']) is int and type(item['parent_pid']) is int and row['pid'] == item['pid']
                and row['parent_pid'] == item['parent_pid'] and relation == item['relation'], 'module topology')
        successful.extend(row['result']['success_ids'])
    require(len(successful) == spec().FULL_TESTS and spec().digest(successful) == plan['test_ids_sha256'], 'every successful test ID')
    check_regression(read(folder/'regression-result.json'), head, spec().FULL_TESTS)
    return dict(tests=spec().FULL_TESTS, modules=spec().MODULES, plan_sha256=ph,
                evidence_sha256=sha(folder/'regression-evidence.json'), result_sha256=sha(folder/'regression-result.json'))


def regression_child(root, folder, head):
    guard(root, head); h = helpers(root); plan = build_plan(root, head, h)
    emit('regression_test_ids_sha256', plan['test_ids_sha256'])
    def run_module(i, ph):
        args = command(root, folder, head, 'module')+['--module-index', str(i), '--plan-sha256', ph]
        return run_logged(root, args, folder/f'module-{i:03d}.log', plan['groups'][i]['module'])
    collect_tests(folder, head, plan, h[0], run_module); guard(root, head)


def artifacts(out):
    return [dict(file=n, sha256=sha(out/n), serialized_bytes=(out/n).stat().st_size) for n in spec().OUTPUTS]


def bound_semantics(out, call):
    before = artifacts(out); value = call(); require(artifacts(out) == before, 'output changed during verification')
    return value, before


def execute_stages(preflight, regression, probe, verify, finalize):
    emit('phase', 'native_readout_preflight'); preflight()
    emit('phase', 'full_regression_fresh_process_per_module'); tests = regression()
    emit('phase', 'frozen_first_mean_probe'); value = probe()
    emit('phase', 'saved_probe_reconstruction'); checked = verify()
    require(spec().blob(value) == spec().blob(checked), 'saved probe mismatch')
    emit('phase', 'final_uncached_input_recheck'); inventory = finalize()
    return value, tests, inventory


def scientific_worker(root, folder, head):
    guard(root, head); s = spec(); s.validate_seal(); h = helpers(root)
    r, base, runtime, _, locks = h; torch, np = runtime.native_runtime(); api = locks.WinAPI(); start = time.monotonic()
    emit('native_lock_probe', locks.lock_probe(api, folder))
    with locks.LockedHashes(sha, lambda path: locks.ReadLease(path, api), progress=lambda v: emit('hash_progress', v)) as cache:
        parent, _, pins, inputs = snapshot(root, h, cache.sha); source_out, cx = parent_semantics(root, h, parent, inputs)
        s.source().base().check_dependencies(root, pins, cx); out = folder/'science'; out.mkdir(exist_ok=False); files = []
        flags = parent['validation_summary']['seed_results']
        emit('registration_check', dict(source_pins=len(pins), protected_inputs=len(inputs), full_tests=s.FULL_TESTS, manifest_sha256=s.MANIFEST_SHA))
        def regression():
            run_logged(root, command(root, folder, head, 'regression'), folder/'regression.log', 'regression'); guard(root, head)
            for lease, _ in cache.entries.values():
                lease.check()
            return verify_tests(folder, head, build_plan(root, head, h), r)
        def verification():
            with cx[-1].guarded.no_neural():
                value, bound = bound_semantics(out, lambda: s.semantic_recheck(out, source_out, cx, flags, read))
            files.extend(bound); return value
        summary, tests, inventory = execute_stages(
            lambda: s.native_preflight(source_out, cx, root, pins, read), regression,
            lambda: s.run_probe(out, source_out, cx, root, pins, flags, read), verification, cache.recheck)
        require(len(inventory) == s.INPUT_COUNT and {v['path']: v['sha256'] for v in inventory} == inputs, 'all final input rereads')
        stats = dict(cache.stats)
    guard(root, head); s.check_summary(summary); require(artifacts(out) == files, 'final output binding')
    result = dict(schema='fold-c331-diagnostic-v1', experiment_id=s.EXPERIMENT_ID, stage=s.STAGE, commit_sha=head, status='PASS',
        diagnostic_execution_valid=True, capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False,
        manifest_sha256=s.MANIFEST_SHA, source_blobs=pins, input_sha256=inputs, artifacts=files, validation_summary=summary,
        runtime=dict(python=sys.version.split()[0], torch=str(torch.__version__), numpy=np.__version__, device='cpu', precision='float64',
                     threads=2, worker_seconds=time.monotonic()-start, process_peak_rss_bytes=s.source().base().peak_rss(), peak_vram_bytes=None))
    save(out/'summary.json', result)
    envelope = dict(schema='fold-c331-execution-envelope-v1', commit_sha=head, scientific_status='PASS',
        scientific_summary_sha256=sha(out/'summary.json'), source_blobs=pins, input_sha256=inputs,
        source_count=s.SOURCE_COUNT, input_count=s.INPUT_COUNT, regression=read(folder/'regression-result.json'), regression_isolation=tests,
        parent_summary_sha256=PARENT_SUMMARY, parent_envelope_sha256=PARENT_ENVELOPE,
        immediate_parent_semantic_reconstruction=True, parent_regression_reconstructed=True, ancestor_semantic_reruns=0,
        saved_semantic_reconstruction=True, final_reference_rechecks=s.INPUT_COUNT, hash_stats=stats,
        manifest_sha256=s.MANIFEST_SHA, scientific_work=s.WORK)
    save(folder/'execution-envelope.json', envelope)
    emit('summary', str(out/'summary.json')); emit('summary_sha256', envelope['scientific_summary_sha256'])
    for effect in summary['effects']:
        emit('C331 effect', effect)
    emit('execution_envelope', dict(path=str(folder/'execution-envelope.json'), sha256=sha(folder/'execution-envelope.json')))
    emit('diagnostic_status', 'PASS'); emit('capability_gate_applicable', False)
    emit('persisted_query_probe', 'PASS;states=10;native_before_after=10;forwards=5130;optimizer_steps=0')


def verify_outputs(root, folder, head):
    guard(root, head); s = spec(); s.validate_seal(); h = helpers(root); out = folder/'science'
    parent, _, pins, inputs = snapshot(root, h, sha)
    r = read(out/'summary.json'); v = read(folder/'execution-envelope.json')
    require(r['schema'] == 'fold-c331-diagnostic-v1' and v['schema'] == 'fold-c331-execution-envelope-v1'
            and r['commit_sha'] == v['commit_sha'] == head and r['experiment_id'] == s.EXPERIMENT_ID and r['stage'] == s.STAGE, 'child identity')
    require(r['status'] == v['scientific_status'] == 'PASS' and r['diagnostic_execution_valid'] is True
            and r['capability_gate_applicable'] is False and r['gate_f_candidate'] is False and r['production_adoption'] is False, 'child diagnostic flags')
    require(r['source_blobs'] == v['source_blobs'] == pins and r['input_sha256'] == v['input_sha256'] == inputs
            and v['source_count'] == s.SOURCE_COUNT and v['input_count'] == s.INPUT_COUNT, 'exact protection unions')
    require(v['parent_summary_sha256'] == PARENT_SUMMARY and v['parent_envelope_sha256'] == PARENT_ENVELOPE
            and v['immediate_parent_semantic_reconstruction'] is True and v['parent_regression_reconstructed'] is True
            and v['ancestor_semantic_reruns'] == 0 and v['saved_semantic_reconstruction'] is True
            and v['final_reference_rechecks'] == s.INPUT_COUNT and v['hash_stats']['final_reference_rechecks'] == s.INPUT_COUNT, 'verification completion')
    require(sha(out/'summary.json') == v['scientific_summary_sha256'] and r['manifest_sha256'] == v['manifest_sha256'] == s.MANIFEST_SHA
            and v['scientific_work'] == s.WORK, 'work/manifest/summary bytes')
    check_regression(v['regression'], head, s.FULL_TESTS)
    require(spec().blob(verify_tests(folder, head, build_plan(root, head, h), h[0])) == spec().blob(v['regression_isolation']), 'full test evidence binding')
    h[3].descriptors(out, r['artifacts'], s.OUTPUTS, sha)
    source_out, cx = parent_semantics(root, h, parent, inputs)
    with cx[-1].guarded.no_neural():
        checked, _ = bound_semantics(out, lambda: s.semantic_recheck(out, source_out, cx, parent['validation_summary']['seed_results'], read))
    require(spec().blob(checked) == spec().blob(r['validation_summary']), 'fresh probe reconstruction')
    guard(root, head); emit('execution_envelope_verified', dict(source_pins=s.SOURCE_COUNT, protected_inputs=s.INPUT_COUNT, full_tests=s.FULL_TESTS, modules=s.MODULES))


def run(root, folder, head):
    guard(root, head); spec().validate_seal()
    require(folder.is_relative_to(root/'runs') and folder != root/'runs', 'output outside runs')
    folder.mkdir(parents=True, exist_ok=False); valid = False
    emit('execution_role', 'C331-FROZEN-FIRST-MEAN-QUERY'); emit('scientific_execution_head', head)
    try:
        run_logged(root, command(root, folder, head, 'science'), folder/'science.log', 'science')
        run_logged(root, command(root, folder, head, 'verify'), folder/'verify.log', 'verify'); valid = True
    finally:
        guard(root, head); emit('run_execution_valid', valid)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1]); parser.add_argument('--folder', type=Path, required=True)
    parser.add_argument('--expected-head', required=True); parser.add_argument('--mode', choices=('run', 'science', 'regression', 'module', 'verify'), default='run')
    parser.add_argument('--module-index', type=int); parser.add_argument('--plan-sha256')
    a = parser.parse_args(); root = a.root.resolve(); folder = a.folder.resolve()
    require(folder.is_relative_to(root/'runs') and folder != root/'runs', 'output outside runs')
    if a.mode == 'module':
        module_child(root, folder, a.expected_head, a.module_index, a.plan_sha256)
    else:
        require(a.module_index is None and a.plan_sha256 is None, 'module-only arguments')
        {'run': run, 'science': scientific_worker, 'regression': regression_child, 'verify': verify_outputs}[a.mode](root, folder, a.expected_head)


if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parents[1])); main()
