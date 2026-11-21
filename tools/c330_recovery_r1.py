"""C330 R1.2: distinguish a subprocess launcher from its runtime child.

The C330 diagnostic/scorers and every accepted source/test are unchanged. Each
registered module gets a new ordinary interpreter. Preserve complete per-test
success receipts, including failures in class/module setup and native crashes.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import unittest

BASE_PATH = 'tools/c330_execution.py'
BASE_BLOB = '1fb5fb47e1e9998cd8ec3a38b25afeb7ec44b31a'
MODEL_PATH = 'fold_lm/v05_benchmarks/model_c330_saved_gate_localization.py'
MODEL_BLOB = '73c30cba137b4d11a9ac39c8f3702bdd0b2e6baf'
BASE_TEST_IDS_SHA = '0e90ec4c1cf292528d7aec95bac8388f12e53fb1ca9dad08ebba58c9174d5183'
BASE_MANIFEST = 'f6a114dd91c086e8a60b374271533bee70d6e1dbb71b187e0aac434b38ff58c7'
EXCLUDED = 'tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state'
OWN = ('tools/c330_recovery_r1.py', 'tests_lm/test_v05_c330_recovery_r1.py', 'docs/c330-recovery-r1.md')
TEST_MODULE = 'tests_lm.test_v05_c330_recovery_r1'
OWN_TESTS, BASE_TESTS, FULL_TESTS, MODULES = 32, 5818, 5850, 220
SOURCE_COUNT, INPUT_COUNT = 841, 1596
POLICY = 'ordered-fresh-process-per-test-module-no-retry-v1'
REVISION = 'C330-R1.2'
# Exact already-registered C324 tooling modules, not a wildcard import permission.
TOOL_MODULES = ('tests_tools.test_c324_locked_hash_r4',
                'tests_tools.test_c324_verified_session_r5',
                'tests_tools.test_c324_scientific_recovery_r6')
INVALID_EXECUTION = '848117fe8326ff146c350343b69d00858a6b0743'
INVALID_PUBLICATION = '63195b8948375de6917e55e692c7bc7b8f01d4ce'
RECOVERY_SHA = 'cb09791f16e446ad2e1116981700c5be26997865d2da2eef89e76acdad1df8b9'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    def unique(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key'); result[key] = value
        return result
    def invalid(value):
        raise ValueError('nonfinite JSON: '+value)
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=invalid)


def save(path, value):
    with Path(path).open('xb') as stream:
        stream.write(blob(value))


def emit(name, value):
    print(name+' = '+json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False), flush=True)


def contract():
    return dict(revision=REVISION, policy=POLICY, invalid_execution=INVALID_EXECUTION,
        invalid_publication=INVALID_PUBLICATION, diagnostic_manifest_sha256=BASE_MANIFEST,
        base_executor_blob=BASE_BLOB, diagnostic_blob=MODEL_BLOB, base_test_ids_sha256=BASE_TEST_IDS_SHA,
        own=list(OWN), own_tests=OWN_TESTS, base_tests=BASE_TESTS, full_tests=FULL_TESTS,
        modules=MODULES, sources=SOURCE_COUNT, inputs=INPUT_COUNT, tool_modules=list(TOOL_MODULES),
        excluded_test=EXCLUDED, module_retries=0, parallel_modules=1,
        scientific_changes=False, new_scientific_model_calls=0,
        process_identity='launcher PID equals worker PID OR worker parent PID;exactly zero or one redirector hop;all IDs positive integers;receipt and begin/complete log identity agree',
        module_schema='fold-c330-r1-module-v2', regression_schema='fold-c330-r1-regression-v2',
        scope='full test-ID inventory unchanged then32 additive tests;new interpreter per module;not a cross-module shared-process regression claim',
        cause_boundary='R1.1 first ten tests passed but launcher PID45276 differed from worker PID1304;the previous receipt had no parent PID;support the documented venv redirector without accepting unrelated processes;C311 native fault unresolved')


def seal():
    require(digest(contract()) == RECOVERY_SHA, 'C330 R1.2 contract seal')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.STDOUT).decode('utf-8').strip()


def source_bytes(path, oid):
    raw = Path(path).read_bytes(); normalized = raw.replace(b'\r\n', b'\n')
    def hashed(value):
        return hashlib.sha1(b'blob '+str(len(value)).encode()+b'\0'+value).hexdigest()
    require(hashed(raw) == oid or (raw == normalized.replace(b'\n', b'\r\n') and hashed(normalized) == oid), 'source bytes: '+str(path))


def guard(root, head):
    require(isinstance(head, str) and re.fullmatch('[0-9a-f]{40}', head), 'execution HEAD')
    require(git(root, 'branch', '--show-current') == 'feat/sft-target-loss' and git(root, 'rev-parse', 'HEAD') == head, 'branch/HEAD mismatch')
    require(not git(root, 'status', '--porcelain', '--untracked-files=no'), 'dirty tracked tree')
    text = (root/'docs/experiment-ledger-and-handoff.md').read_text(encoding='utf-8')
    match = re.search(r'(?ms)^## Formal state\s+(.*?)(?=^## |\Z)', text)
    require(match and re.findall(r'C(\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)', match[1]) == ['330'], 'C330 uniquely ACTIVE')


def load_base(root):
    for name, oid in ((BASE_PATH, BASE_BLOB), (MODEL_PATH, MODEL_BLOB)):
        require(git(root, 'rev-parse', 'HEAD:'+name) == oid, 'unchanged C330 implementation'); source_bytes(root/name, oid)
    spec = importlib.util.spec_from_file_location('_c330_r1_base', root/BASE_PATH)
    require(spec is not None and spec.loader is not None, 'C330 base loader')
    base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
    base.spec().validate_seal(); require(base.spec().MANIFEST_SHA == BASE_MANIFEST, 'unchanged science contract')
    return base


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from flatten(test)
        else:
            yield test


def allowed_module(name):
    return type(name) is str and (re.fullmatch(r'tests_lm\.[A-Za-z0-9_]+', name) is not None
                                 or name in TOOL_MODULES)


def partition(tests):
    groups, seen, seen_modules = [], set(), set()
    for test in tests:
        module, tid = type(test).__module__, test.id()
        require(allowed_module(module) and type(tid) is str and tid.startswith(module+'.'),
                f'test module/ID: module={module!r}; id={tid!r}')
        require(tid not in seen and tid != EXCLUDED, 'duplicate/excluded test ID'); seen.add(tid)
        if not groups or groups[-1]['module'] != module:
            require(module not in seen_modules, 'noncontiguous module order'); seen_modules.add(module)
            groups.append(dict(module=module, test_ids=[]))
        groups[-1]['test_ids'].append(tid)
    require(groups, 'empty test inventory')
    return groups


def validate_plan(plan, head):
    require(set(plan) == {'schema','commit_sha','recovery_sha256','policy','test_ids_sha256','groups'}, 'regression plan fields')
    require(plan['schema'] == 'fold-c330-r1-regression-plan-v1' and plan['commit_sha'] == head
        and plan['recovery_sha256'] == RECOVERY_SHA and plan['policy'] == POLICY, 'regression plan identity')
    groups = plan['groups']; require(type(groups) is list and len(groups) == MODULES, 'regression module count')
    ids, modules = [], []
    for group in groups:
        require(set(group) == {'module','test_ids'} and allowed_module(group['module']),
                'module plan: '+repr(group.get('module')))
        require(type(group['test_ids']) is list and group['test_ids'] and all(type(v) is str and v.startswith(group['module']+'.') for v in group['test_ids']), 'module test IDs')
        modules.append(group['module']); ids.extend(group['test_ids'])
    require(len(modules) == len(set(modules)) == MODULES and len(ids) == len(set(ids)) == FULL_TESTS and EXCLUDED not in ids, 'complete distinct inventory')
    require(modules[-1] == TEST_MODULE and len(groups[-1]['test_ids']) == OWN_TESTS and plan['test_ids_sha256'] == digest(ids), 'inventory seal')


def build_plan(root, head, base):
    e329,e328,e327,e326,legacy,_,r6 = base.helpers(root)
    require(tuple(r6.RECOVERY_MODULES) == TOOL_MODULES, 'inherited tooling module registry changed')
    inherited = list(flatten(base.suite(root, base.spec().parent().base(), e329,e328,e327,e326,legacy,r6)))
    own = list(flatten(unittest.defaultTestLoader.loadTestsFromName(TEST_MODULE)))
    require(len(inherited) == BASE_TESTS and len(own) == OWN_TESTS, 'base and recovery suite counts')
    require(digest([test.id() for test in inherited]) == BASE_TEST_IDS_SHA, 'original C330 full test-ID sequence changed')
    tests = inherited+own
    plan = dict(schema='fold-c330-r1-regression-plan-v1', commit_sha=head, recovery_sha256=RECOVERY_SHA,
        policy=POLICY, test_ids_sha256=digest([t.id() for t in tests]), groups=partition(tests))
    validate_plan(plan,head)
    return plan


class TrackingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); self.started_ids=[]; self.success_ids=[]
    def startTest(self, test):
        self.started_ids.append(test.id()); super().startTest(test)
    def addSuccess(self, test):
        self.success_ids.append(test.id()); super().addSuccess(test)


def execute_module(module, expected):
    loaded = list(flatten(unittest.defaultTestLoader.loadTestsFromName(module)))
    selected = [test for test in loaded if test.id() != EXCLUDED]
    require([test.id() for test in selected] == expected, 'module loader differs from full-suite inventory')
    result = unittest.TextTestRunner(verbosity=1, resultclass=TrackingResult).run(unittest.TestSuite(selected))
    record = dict(tests=result.testsRun, failures=len(result.failures), errors=len(result.errors), skipped=len(result.skipped),
        expected_failures=len(result.expectedFailures), unexpected_successes=len(result.unexpectedSuccesses),
        successful=result.wasSuccessful(), started_ids=result.started_ids, success_ids=result.success_ids)
    return record


def check_module(record, group):
    require(set(record) == {'tests','failures','errors','skipped','expected_failures','unexpected_successes','successful','started_ids','success_ids'}, 'module receipt fields')
    for key in ('tests','failures','errors','skipped','expected_failures','unexpected_successes'):
        require(type(record[key]) is int, 'integer test count')
    require(record['tests'] == len(group['test_ids']) and record['successful'] is True
        and all(record[k] == 0 for k in ('failures','errors','skipped','expected_failures','unexpected_successes'))
        and record['started_ids'] == record['success_ids'] == group['test_ids'], 'all module tests must execute and pass')


def process_relation(launcher_pid, worker_pid, parent_pid):
    """Popen may hold a venv redirector that waits for the actual interpreter."""
    require(all(type(v) is int and v > 0 for v in (launcher_pid, worker_pid, parent_pid))
        and worker_pid != parent_pid, 'module process identity: invalid PID values')
    if launcher_pid == worker_pid:
        return 'direct'
    require(launcher_pid == parent_pid,
        f'module process identity: unrelated launch={launcher_pid}, worker={worker_pid}, parent={parent_pid}')
    return 'redirected-child'


def validate_module_evidence(row, group, head, index, plan_sha, launcher_pid, log):
    require(set(row)=={'schema','commit_sha','plan_sha256','index','module','pid','parent_pid','result'}
        and row['schema']=='fold-c330-r1-module-v2' and row['commit_sha']==head
        and row['plan_sha256']==plan_sha and type(row['index']) is int and row['index']==index
        and row['module']==group['module'], 'module process identity: receipt binding')
    relation=process_relation(launcher_pid,row['pid'],row['parent_pid'])
    check_module(row['result'],group)
    expected=dict(index=index,module=group['module'],tests=len(group['test_ids']),
        pid=row['pid'],parent_pid=row['parent_pid'])
    markers={name:[] for name in ('regression_module_begin','regression_module_complete')}
    for line in log.read_text(encoding='utf-8').splitlines():
        for name, rows in markers.items():
            prefix=name+' = '
            if line.startswith(prefix):
                rows.append(line[len(prefix):])
    for name, rows in markers.items():
        require(len(rows)==1, 'module process identity: missing/duplicate '+name)
        # Emit uses canonical JSON; compare text to reject duplicate keys and bool/int aliases.
        require(rows[0]==json.dumps(expected,sort_keys=True,ensure_ascii=True,allow_nan=False),
            'module process identity: log/receipt disagreement '+name)
    return relation


def run_logged(root, command, logfile, phase):
    started=time.monotonic(); beat=started+10
    with logfile.open('xb') as target:
        process=subprocess.Popen(command,cwd=root,stdout=target,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
        try:
            with logfile.open('r',encoding='utf-8',errors='backslashreplace') as live:
                while process.poll() is None:
                    text=live.read()
                    if text: sys.stdout.write(text); sys.stdout.flush()
                    now=time.monotonic()
                    if now>=beat: emit('worker_heartbeat',dict(phase=phase,elapsed_seconds=round(now-started,3))); beat=now+10
                    time.sleep(.2)
                text=live.read()
                if text: sys.stdout.write(text); sys.stdout.flush()
        finally:
            if process.poll() is None: process.kill(); process.wait(timeout=10)
    emit('process_exit',dict(phase=phase,pid=process.pid,decimal=process.returncode,hexadecimal=f'0x{process.returncode & 0xffffffff:08X}',log=str(logfile)))
    require(process.returncode == 0, 'C330 R1.2 '+phase+' failed; preserve attempt; no retry')
    return process.pid


def command(root, folder, head, mode):
    return [sys.executable,'-B','-X','faulthandler','-u',str(Path(__file__).resolve()),'--root',str(root),'--folder',str(folder),'--expected-head',head,'--mode',mode]


def module_child(root, folder, head, index, plan_sha):
    guard(root,head); seal()
    plan_path=folder/'regression-plan-r1.json'
    require(sha(plan_path)==plan_sha, 'module plan bytes'); plan=read(plan_path); validate_plan(plan,head)
    require(type(index) is int and 0<=index<len(plan['groups']), 'module index')
    group=plan['groups'][index]
    process=dict(pid=os.getpid(),parent_pid=os.getppid())
    marker=dict(index=index,module=group['module'],tests=len(group['test_ids']),**process)
    emit('regression_module_begin',marker)
    record=execute_module(group['module'],group['test_ids'])
    # Write failing Python receipts as well. A native crash has no success receipt.
    value=dict(schema='fold-c330-r1-module-v2',commit_sha=head,plan_sha256=plan_sha,index=index,
        module=group['module'],result=record,**process)
    save(folder/f'module-{index:03d}.json',value)
    check_module(record,group); guard(root,head)
    require(process==dict(pid=os.getpid(),parent_pid=os.getppid()),'module process identity changed during tests')
    emit('regression_module_complete',marker)


def collect_regression(root, folder, head, plan, run_module):
    validate_plan(plan,head); save(folder/'regression-plan-r1.json',plan); plan_sha=sha(folder/'regression-plan-r1.json')
    evidence=[]; completed=0; started=time.monotonic()
    for index, group in enumerate(plan['groups']):
        emit('regression_progress',dict(completed=completed,total=FULL_TESTS,index=index,module=group['module']))
        pid=run_module(index,plan_sha)
        path=folder/f'module-{index:03d}.json'; log=folder/f'module-{index:03d}.log'; value=read(path)
        relation=validate_module_evidence(value,group,head,index,plan_sha,pid,log)
        evidence.append(dict(index=index,launcher_pid=pid,pid=value['pid'],parent_pid=value['parent_pid'],
            relation=relation,exit_code=0,receipt_sha256=sha(path),log_sha256=sha(log)))
        emit('regression_process_identity',dict(index=index,module=group['module'],launcher_pid=pid,
            worker_pid=value['pid'],parent_pid=value['parent_pid'],relation=relation))
        completed+=value['result']['tests']
    require(completed==FULL_TESTS,'regression total')
    envelope=dict(schema='fold-c330-r1-regression-v2',commit_sha=head,recovery_sha256=RECOVERY_SHA,
        policy=POLICY,plan_sha256=plan_sha,test_ids_sha256=plan['test_ids_sha256'],modules=evidence)
    save(folder/'regression-isolation-r1.json',envelope)
    receipt=dict(commit_sha=head,tests=FULL_TESTS,failures=0,errors=0,skipped=0,successful=True)
    save(folder/'regression-result.json',receipt)
    emit('regression_result',dict(**receipt,modules=MODULES,policy=POLICY,seconds=round(time.monotonic()-started,3)))
    return receipt


def regression_child(root, folder, head):
    guard(root,head); seal(); base=load_base(root); plan=build_plan(root,head,base)
    emit('regression_test_ids_sha256',plan['test_ids_sha256'])
    def child(index,plan_sha):
        args=command(root,folder,head,'module')+['--module-index',str(index),'--plan-sha256',plan_sha]
        return run_logged(root,args,folder/f'module-{index:03d}.log',plan['groups'][index]['module'])
    collect_regression(root,folder,head,plan,child); guard(root,head)


def verify_regression(folder, head, plan):
    validate_plan(plan,head)
    require(blob(read(folder/'regression-plan-r1.json'))==blob(plan),'regression inventory changed')
    value=read(folder/'regression-isolation-r1.json'); plan_sha=sha(folder/'regression-plan-r1.json')
    require(set(value)=={'schema','commit_sha','recovery_sha256','policy','plan_sha256','test_ids_sha256','modules'}
        and value['schema']=='fold-c330-r1-regression-v2' and value['commit_sha']==head
        and value['recovery_sha256']==RECOVERY_SHA and value['policy']==POLICY and value['plan_sha256']==plan_sha
        and value['test_ids_sha256']==plan['test_ids_sha256'] and len(value['modules'])==MODULES,'regression evidence identity')
    all_ids=[]
    for index,(item,group) in enumerate(zip(value['modules'],plan['groups'],strict=True)):
        require(set(item)=={'index','launcher_pid','pid','parent_pid','relation','exit_code','receipt_sha256','log_sha256'}
            and type(item['index']) is int and item['index']==index and type(item['exit_code']) is int
            and item['exit_code']==0,'module completion evidence')
        require(process_relation(item['launcher_pid'],item['pid'],item['parent_pid'])==item['relation'],
            'module process identity: aggregate topology')
        path=folder/f'module-{index:03d}.json'; log=folder/f'module-{index:03d}.log'
        require(sha(path)==item['receipt_sha256'] and sha(log)==item['log_sha256'],'module receipt/log bytes')
        row=read(path)
        relation=validate_module_evidence(row,group,head,index,plan_sha,item['launcher_pid'],log)
        require(row['pid']==item['pid'] and row['parent_pid']==item['parent_pid'] and relation==item['relation'],
            'module receipt identity')
        all_ids.extend(row['result']['success_ids'])
    require(len(all_ids)==FULL_TESTS and digest(all_ids)==plan['test_ids_sha256'],'complete successful test-ID sequence')
    expected=dict(commit_sha=head,tests=FULL_TESTS,failures=0,errors=0,skipped=0,successful=True)
    require(blob(read(folder/'regression-result.json'))==blob(expected),'regression aggregate receipt')
    return dict(policy=POLICY,modules=MODULES,tests=FULL_TESTS,plan_sha256=plan_sha,
        evidence_sha256=sha(folder/'regression-isolation-r1.json'),result_sha256=sha(folder/'regression-result.json'))


def extend_protection(root, pins, inputs, legacy, hash_file, canonical):
    require(len(pins)==838 and len(inputs)==1593,'base C330 protection')
    tree=legacy.tree_blobs(root); pins=dict(pins); inputs=dict(inputs)
    for name in OWN:
        require(name in tree and name not in pins and canonical(root/name) not in inputs,'R1 ownership')
        pins[name]=tree[name]; source_bytes(root/name,tree[name]); inputs[canonical(root/name)]=hash_file(root/name)
    require(len(pins)==SOURCE_COUNT and len(inputs)==INPUT_COUNT,'R1 full protection')
    return pins,inputs


def scientific_worker(root, folder, head):
    guard(root,head); seal(); base=load_base(root); s=base.spec()
    e329,_,_,e326,legacy,r4,_=base.helpers(root); torch,np=e326.native_runtime()
    api=r4.WinAPI(); emit('native_lock_probe',r4.lock_probe(api,folder)); p=s.parent(); b=p.base()
    started=time.monotonic()
    with r4.LockedHashes(sha,lambda path:r4.ReadLease(path,api),progress=lambda r:emit('hash_progress',r)) as cache:
        parent_result,_,pins,inputs=base.snapshot(root,p,e329,legacy,cache)
        pins,inputs=extend_protection(root,pins,inputs,legacy,cache.sha,base.canonical)
        cx=b.context(); b.check_dependencies(root,pins,cx); base.parent_semantics(root,parent_result,p,b,cx,inputs)
        emit('registration_check',dict(revision=REVISION,source_pins=len(pins),protected_inputs=len(inputs),full_tests=FULL_TESTS,recovery_sha256=RECOVERY_SHA))
        emit('phase','full_regression_fresh_process_per_module')
        run_logged(root,command(root,folder,head,'regression'),folder/'regression.log','regression')
        for lease,_ in cache.entries.values(): lease.check()
        guard(root,head)
        # Reconstruct the exact selected IDs; no test method or setUpClass runs here.
        regression_evidence=verify_regression(folder,head,build_plan(root,head,base))
        out=folder/'science'; out.mkdir(exist_ok=False); parent_out=root/base.PARENT_FOLDER/'science'
        emit('phase','saved_gate_failure_localization')
        with cx[-1].guarded.no_neural():
            summary=s.run_diagnostic(out,parent_out,read)
            checked,files=base.bound_semantics(out,lambda:s.semantic_recheck(out,parent_out,read))
        require(blob(summary)==blob(checked),'saved diagnostic reconstruction')
        emit('phase','final_uncached_input_recheck'); inventory=cache.recheck()
        require(len(inventory)==INPUT_COUNT and {r['path']:r['sha256'] for r in inventory}==inputs,'all final input rereads')
        hash_stats=dict(cache.stats)
    guard(root,head); s.check_summary(summary); require(base.artifacts(out)==files,'post-verification output bytes')
    require(summary['parent_candidate_gate'] is parent_result['validation_summary']['candidate_gate']
        and summary['parent_paired_success_count']==parent_result['validation_summary']['paired_success_count'],'preserve C329 verdict')
    result=dict(schema='fold-c330-diagnostic-v1',experiment_id=s.EXPERIMENT_ID,stage=s.STAGE,commit_sha=head,status='PASS',
        diagnostic_execution_valid=True,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,
        source_blobs=pins,input_sha256=inputs,artifacts=files,validation_summary=summary,manifest_sha256=s.MANIFEST_SHA,
        execution_revision=REVISION,recovery_manifest_sha256=RECOVERY_SHA,recovery_manifest=contract(),
        runtime=dict(python=sys.version.split()[0],torch=str(torch.__version__),numpy=np.__version__,worker_seconds=time.monotonic()-started,
            process_peak_rss_bytes=b.peak_rss(),device='cpu',precision='float64',threads=2))
    save(out/'summary.json',result)
    envelope=dict(schema='fold-c330-execution-envelope-v1',commit_sha=head,source_blobs=pins,input_sha256=inputs,
        source_count=SOURCE_COUNT,input_count=INPUT_COUNT,scientific_summary_sha256=sha(out/'summary.json'),scientific_status='PASS',
        regression=read(folder/'regression-result.json'),regression_isolation=regression_evidence,
        parent_summary_sha256=base.PARENT_SUMMARY,parent_envelope_sha256=base.PARENT_ENVELOPE,
        immediate_parent_semantic_reconstruction=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,
        final_reference_rechecks=INPUT_COUNT,hash_stats=hash_stats,manifest_sha256=s.MANIFEST_SHA,scientific_work=s.WORK,
        execution_revision=REVISION,recovery_manifest_sha256=RECOVERY_SHA,recovery_manifest=contract())
    save(folder/'execution-envelope.json',envelope)
    emit('summary',str(out/'summary.json')); emit('summary_sha256',envelope['scientific_summary_sha256'])
    for row in summary['seed_results']: emit('C330 preserved_seed',row)
    for row in summary['strata']:
        if row['arm']=='extended2400': emit('C330 residual_stratum',row)
    for row in summary['transition_summary']: emit('C330 gate_transition',row)
    emit('execution_envelope',dict(path=str(folder/'execution-envelope.json'),sha256=sha(folder/'execution-envelope.json')))
    emit('diagnostic_status','PASS'); emit('capability_gate_applicable',False)
    emit('persisted_gate_localization','PASS;local_cells=4320;order_cells=2160;model_forwards=0')


def verify_outputs(root, folder, head):
    guard(root,head); seal(); base=load_base(root); s=base.spec(); out=folder/'science'
    r=read(out/'summary.json'); v=read(folder/'execution-envelope.json')
    require(r['schema']=='fold-c330-diagnostic-v1' and v['schema']=='fold-c330-execution-envelope-v1'
        and r['commit_sha']==v['commit_sha']==head and r['experiment_id']==s.EXPERIMENT_ID and r['stage']==s.STAGE,'child identity')
    require(r['status']==v['scientific_status']=='PASS' and r['diagnostic_execution_valid'] is True and r['capability_gate_applicable'] is False
        and r['gate_f_candidate'] is False and r['production_adoption'] is False,'diagnostic flags')
    require(r['execution_revision']==v['execution_revision']==REVISION and r['recovery_manifest_sha256']==v['recovery_manifest_sha256']==RECOVERY_SHA
        and r['manifest_sha256']==v['manifest_sha256']==BASE_MANIFEST and v['scientific_work']==s.WORK
        and blob(r['recovery_manifest'])==blob(v['recovery_manifest'])==blob(contract()),'science/recovery identities')
    require(sha(out/'summary.json')==v['scientific_summary_sha256'],'summary bytes')
    require(v['source_count']==len(v['source_blobs'])==SOURCE_COUNT and v['input_count']==len(v['input_sha256'])==INPUT_COUNT
        and r['source_blobs']==v['source_blobs'] and r['input_sha256']==v['input_sha256'],'complete source/input unions')
    require(v['parent_summary_sha256']==base.PARENT_SUMMARY and v['parent_envelope_sha256']==base.PARENT_ENVELOPE
        and v['immediate_parent_semantic_reconstruction'] is True and v['ancestor_semantic_reruns']==0
        and v['saved_semantic_reconstruction'] is True and v['final_reference_rechecks']==INPUT_COUNT
        and v['hash_stats']['final_reference_rechecks']==INPUT_COUNT,'completed preservation')
    e329,_,_,_,legacy,_,_=base.helpers(root); p=s.parent(); po=root/base.PARENT_FOLDER/'science'
    require(sha(po/'summary.json')==base.PARENT_SUMMARY and sha(po.parent/'execution-envelope.json')==base.PARENT_ENVELOPE,'parent fixed bytes')
    pr=read(po/'summary.json'); pe=read(po.parent/'execution-envelope.json'); base.parent_contract(pr,pe,p,e329)
    tree=legacy.tree_blobs(root); own=tuple(s.OWN)+OWN
    require(len(set(own))==9 and not set(own)&set(pe['source_blobs']) and v['source_blobs']=={**pe['source_blobs'],**{k:tree[k] for k in own}},'exact source union')
    wanted=dict(pe['input_sha256']); wanted.update(legacy.descriptors(po,pr['artifacts'],p.OUTPUTS,sha))
    wanted.update({base.canonical(po/'summary.json'):base.PARENT_SUMMARY,base.canonical(po.parent/'execution-envelope.json'):base.PARENT_ENVELOPE})
    wanted.update({base.canonical(root/k):sha(root/k) for k in own}); require(wanted==v['input_sha256'],'exact input union')
    for name,oid in v['source_blobs'].items(): require(tree.get(name)==oid,'source changed'); source_bytes(root/name,oid)
    for name,expected in wanted.items(): require(sha(name)==expected,'input changed: '+name)
    legacy.descriptors(out,r['artifacts'],s.OUTPUTS,sha)
    evidence=verify_regression(folder,head,build_plan(root,head,base))
    require(blob(evidence)==blob(v['regression_isolation']) and blob(v['regression'])==blob(read(folder/'regression-result.json')),'all regression evidence bound')
    s.check_summary(r['validation_summary'])
    checked,_=base.bound_semantics(out,lambda:s.semantic_recheck(out,po,read))
    require(blob(checked)==blob(r['validation_summary']) and checked['parent_candidate_gate'] is pr['validation_summary']['candidate_gate']
        and checked['parent_paired_success_count']==pr['validation_summary']['paired_success_count'],'fresh diagnostic/parent reconstruction')
    guard(root,head); emit('execution_envelope_verified',dict(revision=REVISION,source_pins=SOURCE_COUNT,protected_inputs=INPUT_COUNT,full_tests=FULL_TESTS,modules=MODULES))


def run(root, folder, head):
    guard(root,head); seal(); require(folder.is_relative_to(root/'runs') and folder!=root/'runs','output outside runs')
    folder.mkdir(parents=True,exist_ok=False); valid=False
    emit('execution_role',REVISION+'-MODULE-ISOLATED-RECOVERY'); emit('scientific_execution_head',head)
    try:
        run_logged(root,command(root,folder,head,'science'),folder/'science.log','science')
        run_logged(root,command(root,folder,head,'verify'),folder/'verify.log','verify'); valid=True
    finally:
        guard(root,head); emit('run_execution_valid',valid)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); parser.add_argument('--folder',type=Path,required=True)
    parser.add_argument('--expected-head',required=True); parser.add_argument('--mode',choices=('run','science','regression','module','verify'),default='run')
    parser.add_argument('--module-index',type=int); parser.add_argument('--plan-sha256')
    args=parser.parse_args(); root=args.root.resolve(); folder=args.folder.resolve()
    require(folder.is_relative_to(root/'runs') and folder!=root/'runs','output outside runs')
    if args.mode=='module': module_child(root,folder,args.expected_head,args.module_index,args.plan_sha256)
    else:
        require(args.module_index is None and args.plan_sha256 is None,'module-only arguments')
        {'run':run,'science':scientific_worker,'regression':regression_child,'verify':verify_outputs}[args.mode](root,folder,args.expected_head)


if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).resolve().parents[1])); main()
