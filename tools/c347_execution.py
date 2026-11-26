"""C347 protected saved loss/correctness-transition audit after accepted negative C346."""
from __future__ import annotations
import argparse
import contextlib
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
PARENT_HEAD = '622e623faa0c3c698a18033eb8b4bca554088918'
PARENT_FOLDER = 'runs/c346-pair-max-rate-68993e9eaa4e410886dbe0d24a3def3c'
PARENT_SUMMARY = 'd06fa2a06287696424ac58e3d56e7262282caca81b028f61709f609ab728e816'
PARENT_ENVELOPE = 'b8b57583363d61aca10d947c891de0d8b3d8b2319e659652cacf101a334e3c3d'
P_PATH = 'tools/c346_execution.py'
P_BLOB = '7950248a3d9acd9e8eb8c7da48b1b707ea478d85'
S_PATH = 'fold_lm/v05_benchmarks/model_c346_pair_max_rate.py'
S_BLOB = '684970a7a1d073f22422cb46f7f1514802af832e'
BASE_IDS_SHA = '39ced3110d4a2d9288390401f53000fc322e4541a17ea47384553e7767425394'
TEST_MODULES = ('tests_lm.test_v05_c347_saved_loss_transition', 'tests_lm.test_v05_c347_execution')
EXECUTION_REVISION = 'C347-R0'
TIMEOUT_CLEANUP_IMPLEMENTATION = 'C344-R1'


def spec():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c347_saved_loss_transition')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def emit(name, value):
    print(name+' = '+json.dumps(value,sort_keys=True,ensure_ascii=True,allow_nan=False),flush=True)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def read(path):
    def unique(items):
        result = {}
        for k,v in items:
            require(k not in result,'duplicate JSON key'); result[k] = v
        return result
    def invalid(value):
        raise ValueError('nonfinite JSON:'+value)
    return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=unique,parse_constant=invalid)


def save(path, value):
    with Path(path).open('xb') as stream: stream.write(spec().blob(value))


def git(root, *args):
    return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.STDOUT).decode('utf-8').strip()


def canonical(path):
    return os.path.normcase(str(Path(path).resolve(strict=True)))


def source_bytes(path, oid):
    raw = Path(path).read_bytes(); lf = raw.replace(b'\r\n',b'\n')
    def h(value): return hashlib.sha1(b'blob '+str(len(value)).encode()+b'\0'+value).hexdigest()
    require(h(raw) == oid or (raw == lf.replace(b'\n',b'\r\n') and h(lf) == oid),'source bytes:'+str(path))


def active(text):
    match = re.search(r'(?ms)^## Formal state\s+(.*?)(?=^## |\Z)',text)
    return bool(match and re.findall(r'C(\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)',match[1]) == ['347'])


def guard(root, head):
    require(type(head) is str and re.fullmatch('[0-9a-f]{40}',head),'execution HEAD')
    require(git(root,'branch','--show-current') == BRANCH and git(root,'rev-parse','HEAD') == head,'branch/HEAD')
    require(not git(root,'status','--porcelain','--untracked-files=no'),'dirty tracked tree')
    require(active((root/'docs/experiment-ledger-and-handoff.md').read_text(encoding='utf-8')),'C347 uniquely ACTIVE')


def helpers(root):
    for name,oid in ((P_PATH,P_BLOB),(S_PATH,S_BLOB)):
        require(git(root,'rev-parse','HEAD:'+name) == oid,'accepted C346 pin'); source_bytes(root/name,oid)
    loader = importlib.util.spec_from_file_location('_c347_parent',root/P_PATH)
    require(loader is not None and loader.loader is not None,'parent loader')
    parent = importlib.util.module_from_spec(loader); loader.loader.exec_module(parent); parent.spec().validate_seal()
    prior = parent.helpers(root)
    require(type(prior) is dict and set(prior) == {'parent','prior','cleanup','recovery','c330','runtime','legacy','locks'},'C346 helper bridge')
    cleanup = prior['cleanup']
    require(cleanup.EXECUTION_REVISION == TIMEOUT_CLEANUP_IMPLEMENTATION,'C344-R1 cleanup bridge')
    return dict(parent=parent,prior=prior,cleanup=cleanup,**{k:prior[k] for k in ('recovery','c330','runtime','legacy','locks')})


def check_timeout_preflight(value, head, cleanup):
    require(cleanup.EXECUTION_REVISION == TIMEOUT_CLEANUP_IMPLEMENTATION,'accepted cleanup implementation')
    cleanup.check_timeout_preflight(value,head)


def timeout_cleanup_preflight(root, head, h):
    """Execute the accepted C344-R1 checks and retain their implementation receipt."""
    cleanup = h['cleanup']
    require(cleanup.EXECUTION_REVISION == TIMEOUT_CLEANUP_IMPLEMENTATION,'accepted cleanup implementation')
    value = cleanup.timeout_cleanup_preflight(root,head,h['recovery'])
    check_timeout_preflight(value,head,cleanup)
    return value


def receipt(head, count):
    return dict(commit_sha=head,tests=count,failures=0,errors=0,skipped=0,successful=True)


def check_regression(value, head, count):
    require(spec().blob(value) == spec().blob(receipt(head,count)),'complete regression receipt')


def protected_counts():
    manifest = spec().manifest()
    values = manifest['source_count'],manifest['input_count']
    require(all(type(v) is int and v > 0 for v in values),'manifest protection counts')
    return values


def report_protected_counts(pins, inputs):
    sources,protected = protected_counts()
    emit('registration_counts',dict(source_pins=len(pins),protected_inputs=len(inputs),
         expected_source_pins=sources,expected_protected_inputs=protected,manifest_sha256=spec().MANIFEST_SHA,
         actual_manifest_sha256=spec().digest(spec().manifest())))
    require(len(pins) == sources,'complete child source protection')
    require(len(inputs) == protected,'complete child input protection')


def own_compile_inventory():
    s = spec()
    return dict(python_sources=[p for p in s.OWN if p.endswith('.py')],
                test_modules=list(TEST_MODULES),own_tests=s.manifest()['own_tests'])


def compile_import_own(root):
    value = own_compile_inventory()
    for name in value['python_sources']:
        compile((root/name).read_text(encoding='utf-8'),str(root/name),'exec')
    spec().validate_seal()
    tests = []
    for module in TEST_MODULES:
        imported = importlib.import_module(module)
        require(imported.__name__ == module,'own module import')
        loaded = list(helpers_recovery_flatten(unittest.defaultTestLoader.loadTestsFromModule(imported)))
        require(loaded and all(type(t).__module__ == module for t in loaded),'own test import inventory')
        tests.extend(loaded)
    require(len(tests) == value['own_tests'],'compiled/imported own test count')
    return value


def helpers_recovery_flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite): yield from helpers_recovery_flatten(item)
        else: yield item


def runtime_identity(torch, np):
    return dict(python=sys.version.split()[0],torch=str(torch.__version__),numpy=np.__version__,
                device='cpu',precision='float64',threads=2)


def check_inventory(inventory, expected, message):
    require(len(inventory) == len(expected) and {r['path']:r['sha256'] for r in inventory} == expected,message)


def parent_contract(r, v, parent, cleanup):
    s = parent.spec(); s.validate_seal(); s.check_summary(r['validation_summary'])
    require(r['schema'] == 'fold-c346-trained-v1' and v['schema'] == 'fold-c346-execution-envelope-v1'
            and r['commit_sha'] == v['commit_sha'] == PARENT_HEAD and r['experiment_id'] == s.EXPERIMENT_ID
            and r['stage'] == s.STAGE,'parent identity')
    require(r['status'] == v['scientific_status'] == 'FAIL' and r['scientific_execution_valid'] is True
            and r['capability_gate_applicable'] is True and r['gate_f_candidate'] is False and r['production_adoption'] is False
            and r['validation_summary']['candidate_gate'] is False
            and type(r['validation_summary']['eligible_seed_count']) is int
            and r['validation_summary']['eligible_seed_count'] == 0,'accepted negative parent')
    expected_components = dict(all_candidates_full_pass=False,candidate_full_pass_count=0,
        nonnegative_counts=dict(mean_ce=dict(passed=64,total=120),pair_max=dict(passed=68,total=120)),
        nonnegative_vs_mean_ce=False,nonnegative_vs_pair_max=False,strict_interior_vs_pair_max=False)
    require(spec().blob(r['validation_summary']['gate_components']) == spec().blob(expected_components),'accepted C346 subgates')
    require(r['manifest_sha256'] == v['manifest_sha256'] == s.MANIFEST_SHA and v['scientific_work'] == s.WORK
            and v['scientific_summary_sha256'] == PARENT_SUMMARY,'parent manifest/work')
    require(v['source_count'] == len(v['source_blobs']) == 944 and v['input_count'] == len(v['input_sha256']) == 9177
            and r['source_blobs'] == v['source_blobs'] and r['input_sha256'] == v['input_sha256']
            and v['source_blobs'].get(P_PATH) == P_BLOB and v['source_blobs'].get(S_PATH) == S_BLOB,'parent protection')
    require(v['parent_summary_sha256'] == parent.PARENT_SUMMARY and v['parent_envelope_sha256'] == parent.PARENT_ENVELOPE
            and v['immediate_parent_semantic_reconstruction'] is True and v['parent_regression_reconstructed'] is True
            and v['ancestor_semantic_reruns'] == 0 and v['saved_semantic_reconstruction'] is True
            and v['final_reference_rechecks'] == 9177 and v['hash_stats']['final_reference_rechecks'] == 9177,'parent completion')
    require(parent.EXECUTION_REVISION == v['execution_revision'] == 'C346-R0'
            and v['timeout_cleanup_implementation'] == TIMEOUT_CLEANUP_IMPLEMENTATION,'parent execution/cleanup revision')
    check_timeout_preflight(v['timeout_cleanup_preflight'],PARENT_HEAD,cleanup)
    check_regression(v['regression'],PARENT_HEAD,6652)


def parent_test_files(folder, envelope, hash_file):
    bound = envelope['regression_isolation']; require(bound['tests'] == 6652 and bound['modules'] == 243,'parent test scope')
    wanted = {'regression-plan.json':bound['plan_sha256'],'regression-evidence.json':bound['evidence_sha256'],
              'regression-result.json':bound['result_sha256']}
    for name,value in wanted.items(): require(hash_file(folder/name) == value,'parent test record:'+name)
    rows = read(folder/'regression-evidence.json')['modules']; require(len(rows) == 243,'all parent modules')
    for i,row in enumerate(rows):
        require(type(row['index']) is int and row['index'] == i,'parent proof order')
        wanted[f'module-{i:03d}.json'] = row['receipt_sha256']; wanted[f'module-{i:03d}.log'] = row['log_sha256']
    require(len(wanted) == 489,'all489parent test proofs')
    for name,value in wanted.items(): require(hash_file(folder/name) == value,'parent proof bytes:'+name)
    return {canonical(folder/name):value for name,value in wanted.items()}


def snapshot(root, h, hash_file):
    parent = h['parent']; s = spec(); s.validate_seal(); folder = root/PARENT_FOLDER; out = folder/'science'
    require(not folder.is_symlink() and not out.is_symlink(),'parent path link')
    require(hash_file(out/'summary.json') == PARENT_SUMMARY and hash_file(folder/'execution-envelope.json') == PARENT_ENVELOPE,'exact parent bytes')
    r,v = read(out/'summary.json'),read(folder/'execution-envelope.json'); parent_contract(r,v,parent,h['cleanup'])
    _,_,pins,inputs = parent.snapshot(root,h['prior'],hash_file)
    require(pins == v['source_blobs'] and inputs == v['input_sha256'],'reconstructed parent maps')
    pins,inputs = dict(pins),dict(inputs)
    added = h['legacy'].descriptors(out,r['artifacts'],parent.spec().OUTPUTS,hash_file)
    added.update({canonical(out/'summary.json'):PARENT_SUMMARY,canonical(folder/'execution-envelope.json'):PARENT_ENVELOPE})
    proofs = parent_test_files(folder,v,hash_file); require(not set(added)&set(proofs),'parent collision'); added.update(proofs)
    require(len(added) == 497 and not set(added)&set(inputs),'all497parent files'); inputs.update(added)
    verified = parent.verify_tests(folder,PARENT_HEAD,parent.build_plan(root,PARENT_HEAD,h['prior']),h['recovery'])
    require(s.blob(verified) == s.blob(v['regression_isolation']),'parent6652proof semantics')
    tree = h['legacy'].tree_blobs(root)
    for name in s.OWN:
        path = canonical(root/name); require(name in tree and name not in pins and path not in inputs,'child ownership')
        pins[name] = tree[name]; inputs[path] = hash_file(root/name)
    report_protected_counts(pins,inputs)
    for name,oid in pins.items():
        require(tree.get(name) == oid,'inherited source changed'); source_bytes(root/name,oid)
        require(inputs.get(canonical(root/name)) == hash_file(root/name),'source/input binding')
    return r,v,pins,inputs


def parent_semantics(root, h, prior, inputs):
    source_out = root/PARENT_FOLDER/'science'; data_out = root/h['c330'].PARENT_FOLDER/'science'
    p = h['parent'].spec()
    for folder,names in ((source_out,p.OUTPUTS),
                        (data_out,('dataset.json','original-prompts.json','interior-prompts.json'))):
        require(all(canonical(folder/name) in inputs for name in names),'protected semantic inputs')
    base = p.previous().source().base(); cx = base.context()
    with cx[-1].guarded.no_neural():
        value = p.semantic_recheck(source_out,data_out,cx,read)
        require(spec().blob(value) == spec().blob(prior['validation_summary']),'immediate C346 semantics')
        data,old,new = p.previous().load_data(data_out,read)
        require(base.digest(data) == base.DATA_SHA and base.digest(old) == base.PROMPTS_SHA
                and base.digest(new) == base.digest(cx[2].new_prompts(data)),'canonical data/prompts')
        cx[-1].c.p267.validate_data(data); cx[2].check_prompts(data,old,new,cx[3],cx[-1])
    emit('accepted_parent_semantics',dict(parent_files=497,regression_tests=6652,model_forwards=0,ancestor_semantic_reruns=0))
    return source_out,data_out,cx


def validate_plan(plan, head, recovery):
    s = spec()
    require(set(plan) == {'schema','commit_sha','manifest_sha256','test_ids_sha256','groups'}
            and plan['schema'] == 'fold-c347-regression-plan-v1' and plan['commit_sha'] == head
            and plan['manifest_sha256'] == s.MANIFEST_SHA,'test plan identity')
    groups = plan['groups']; require(type(groups) is list and len(groups) == s.MODULES,'module count')
    ids,modules = [],[]
    for g in groups:
        require(set(g) == {'module','test_ids'} and recovery.allowed_module(g['module']) and type(g['test_ids']) is list
                and g['test_ids'] and all(type(t) is str and t.startswith(g['module']+'.') for t in g['test_ids']),'test ID provenance')
        ids.extend(g['test_ids']); modules.append(g['module'])
    own = groups[-len(TEST_MODULES):]
    require(len(ids) == len(set(ids)) == s.FULL_TESTS and len(modules) == len(set(modules)) and recovery.EXCLUDED not in ids
            and tuple(g['module'] for g in own) == TEST_MODULES
            and sum(len(g['test_ids']) for g in own) == s.OWN_TESTS,'complete test inventory')
    require(s.digest(ids[:-s.OWN_TESTS]) == BASE_IDS_SHA and s.digest(ids) == plan['test_ids_sha256'],'unchanged6652test IDs')


def build_plan(root, head, h):
    prior = h['parent'].build_plan(root,head,h['prior']); recovery = h['recovery']; groups = list(prior['groups'])
    count = 0
    for module in TEST_MODULES:
        own = list(recovery.flatten(unittest.defaultTestLoader.loadTestsFromName(module)))
        require(own and all(type(t).__module__ == module for t in own),'actual own loader')
        count += len(own); groups.append(dict(module=module,test_ids=[t.id() for t in own]))
    require(count == spec().OWN_TESTS,'actual own total')
    plan = dict(schema='fold-c347-regression-plan-v1',commit_sha=head,manifest_sha256=spec().MANIFEST_SHA,
                test_ids_sha256=spec().digest([t for g in groups for t in g['test_ids']]),groups=groups)
    validate_plan(plan,head,recovery); return plan


def command(root, folder, head, mode):
    return [sys.executable,'-B','-X','faulthandler','-u',str(Path(__file__).resolve()),'--root',str(root),
            '--folder',str(folder),'--expected-head',head,'--mode',mode]


def run_logged(root, args, path, phase):
    start = time.monotonic(); beat = start+10
    with path.open('xb') as out:
        process = subprocess.Popen(args,cwd=root,stdout=out,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
        try:
            with path.open('r',encoding='utf-8',errors='backslashreplace') as live:
                while process.poll() is None:
                    text = live.read()
                    if text: sys.stdout.write(text); sys.stdout.flush()
                    now = time.monotonic()
                    if now >= beat:
                        emit('worker_heartbeat',dict(phase=phase,elapsed_seconds=round(now-start,3))); beat = now+10
                    time.sleep(.2)
                text = live.read()
                if text: sys.stdout.write(text); sys.stdout.flush()
        finally:
            if process.poll() is None: process.kill(); process.wait(timeout=10)
    emit('process_exit',dict(phase=phase,pid=process.pid,decimal=process.returncode,hexadecimal=f'0x{process.returncode & 0xffffffff:08X}'))
    require(process.returncode == 0,'C347 '+phase+' failed;no automatic retry'); return process.pid


def module_child(root, folder, head, index, plan_sha):
    guard(root,head); spec().validate_seal(); h = helpers(root); recovery = h['recovery']
    require(sha(folder/'regression-plan.json') == plan_sha,'module plan bytes')
    plan = read(folder/'regression-plan.json'); validate_plan(plan,head,recovery)
    require(type(index) is int and 0 <= index < spec().MODULES,'module index')
    group = plan['groups'][index]; process = dict(pid=os.getpid(),parent_pid=os.getppid())
    marker = dict(index=index,module=group['module'],tests=len(group['test_ids']),**process)
    emit('regression_module_begin',marker)
    with h['cleanup'].timeout_monitor_boundary(root,group['module']):
        value = recovery.execute_module(group['module'],group['test_ids'])
    save(folder/f'module-{index:03d}.json',dict(schema='fold-c330-r1-module-v2',commit_sha=head,plan_sha256=plan_sha,
         index=index,module=group['module'],result=value,**process))
    recovery.check_module(value,group); guard(root,head)
    require(process == dict(pid=os.getpid(),parent_pid=os.getppid()),'module identity changed'); emit('regression_module_complete',marker)


def collect_tests(folder, head, plan, recovery, run_module):
    validate_plan(plan,head,recovery); save(folder/'regression-plan.json',plan); ph = sha(folder/'regression-plan.json')
    items = []; total = 0; start = time.monotonic()
    for i,group in enumerate(plan['groups']):
        emit('regression_progress',dict(completed=total,total=spec().FULL_TESTS,index=i,module=group['module']))
        launcher = run_module(i,ph); path = folder/f'module-{i:03d}.json'; log = folder/f'module-{i:03d}.log'; row = read(path)
        relation = recovery.validate_module_evidence(row,group,head,i,ph,launcher,log)
        items.append(dict(index=i,launcher_pid=launcher,pid=row['pid'],parent_pid=row['parent_pid'],relation=relation,
                          exit_code=0,receipt_sha256=sha(path),log_sha256=sha(log)))
        total += row['result']['tests']
    require(total == spec().FULL_TESTS,'all tests executed')
    save(folder/'regression-evidence.json',dict(schema='fold-c347-regression-v1',commit_sha=head,plan_sha256=ph,
         test_ids_sha256=plan['test_ids_sha256'],modules=items))
    save(folder/'regression-result.json',receipt(head,total))
    emit('regression_result',dict(**receipt(head,total),modules=spec().MODULES,seconds=round(time.monotonic()-start,3)))


def verify_tests(folder, head, plan, recovery):
    validate_plan(plan,head,recovery); require(spec().blob(read(folder/'regression-plan.json')) == spec().blob(plan),'planned inventory')
    value = read(folder/'regression-evidence.json'); ph = sha(folder/'regression-plan.json')
    require(set(value) == {'schema','commit_sha','plan_sha256','test_ids_sha256','modules'} and value['schema'] == 'fold-c347-regression-v1'
            and value['commit_sha'] == head and value['plan_sha256'] == ph and value['test_ids_sha256'] == plan['test_ids_sha256']
            and len(value['modules']) == spec().MODULES,'test proof identity')
    ids = []
    for i,(item,group) in enumerate(zip(value['modules'],plan['groups'],strict=True)):
        require(set(item) == {'index','launcher_pid','pid','parent_pid','relation','exit_code','receipt_sha256','log_sha256'}
                and type(item['index']) is int and item['index'] == i and type(item['exit_code']) is int and item['exit_code'] == 0,'completed module')
        path = folder/f'module-{i:03d}.json'; log = folder/f'module-{i:03d}.log'
        require(sha(path) == item['receipt_sha256'] and sha(log) == item['log_sha256'],'module proof bytes')
        row = read(path); relation = recovery.validate_module_evidence(row,group,head,i,ph,item['launcher_pid'],log)
        require(type(item['pid']) is int and type(item['parent_pid']) is int and row['pid'] == item['pid']
                and row['parent_pid'] == item['parent_pid'] and relation == item['relation'],'module topology')
        ids.extend(row['result']['success_ids'])
    require(len(ids) == spec().FULL_TESTS and spec().digest(ids) == plan['test_ids_sha256'],'all successful test IDs')
    check_regression(read(folder/'regression-result.json'),head,spec().FULL_TESTS)
    return dict(tests=spec().FULL_TESTS,modules=spec().MODULES,plan_sha256=ph,
                evidence_sha256=sha(folder/'regression-evidence.json'),result_sha256=sha(folder/'regression-result.json'))


def regression_child(root, folder, head):
    guard(root,head); h = helpers(root); plan = build_plan(root,head,h); emit('regression_test_ids_sha256',plan['test_ids_sha256'])
    def run_module(i,ph):
        return run_logged(root,command(root,folder,head,'module')+['--module-index',str(i),'--plan-sha256',ph],
                          folder/f'module-{i:03d}.log',plan['groups'][i]['module'])
    collect_tests(folder,head,plan,h['recovery'],run_module); guard(root,head)


def artifacts(out):
    return [dict(file=n,sha256=sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in spec().OUTPUTS]


def bound_semantics(out, call):
    before = artifacts(out); value = call(); require(artifacts(out) == before,'output mutation'); return value,before


class ValidationText:
    def __init__(self, live, retained):
        self.live,self.retained = live,retained

    def write(self, text):
        self.live.write(text); self.retained.write(text); return len(text)

    def flush(self):
        self.live.flush(); self.retained.flush()


def validation_contract(value, folder, head, pins, inputs, cleanup, runtime):
    s = spec(); sources,protected = protected_counts()
    expected_keys = {'schema','experiment_id','stage','commit_sha','run_folder','manifest_sha256','status',
        'source_blobs','input_sha256','source_count','input_count','compile_imports','regression','regression_isolation',
        'parent_summary_sha256','parent_envelope_sha256','immediate_parent_semantic_reconstruction',
        'parent_regression_reconstructed','ancestor_semantic_reruns','final_reference_rechecks','hash_stats',
        'execution_revision','timeout_cleanup_implementation','timeout_cleanup_preflight','native_runtime','validation_log'}
    require(type(value) is dict and set(value) == expected_keys,'validation receipt fields')
    require(value['schema'] == 'fold-c347-runtime-validation-v1' and value['experiment_id'] == s.EXPERIMENT_ID
            and value['stage'] == s.STAGE and value['commit_sha'] == head and value['run_folder'] == canonical(folder)
            and value['manifest_sha256'] == s.MANIFEST_SHA and value['status'] == 'PASS','validation identity/folder/seal')
    report_protected_counts(pins,inputs)
    require(value['source_blobs'] == pins and value['input_sha256'] == inputs
            and type(value['source_count']) is int and value['source_count'] == sources
            and type(value['input_count']) is int and value['input_count'] == protected,'validation protection maps')
    require(s.blob(value['compile_imports']) == s.blob(own_compile_inventory()),'validation compile/import inventory')
    require(value['parent_summary_sha256'] == PARENT_SUMMARY and value['parent_envelope_sha256'] == PARENT_ENVELOPE
            and value['immediate_parent_semantic_reconstruction'] is True and value['parent_regression_reconstructed'] is True
            and type(value['ancestor_semantic_reruns']) is int and value['ancestor_semantic_reruns'] == 0
            and value['final_reference_rechecks'] == protected
            and value['hash_stats']['final_reference_rechecks'] == protected,'validation parent/input completion')
    require(value['execution_revision'] == EXECUTION_REVISION
            and value['timeout_cleanup_implementation'] == TIMEOUT_CLEANUP_IMPLEMENTATION,'validation implementation')
    check_timeout_preflight(value['timeout_cleanup_preflight'],head,cleanup)
    require(s.blob(value['native_runtime']) == s.blob(runtime),'validation native runtime identity')
    check_regression(value['regression'],head,s.FULL_TESTS)
    require(value['regression_isolation']['tests'] == s.FULL_TESTS
            and value['regression_isolation']['modules'] == s.MODULES,'validation full regression scope')
    log = value['validation_log']
    require(type(log) is dict and set(log) == {'file','sha256','serialized_bytes'} and log['file'] == 'validation.log'
            and type(log['serialized_bytes']) is int and log['serialized_bytes'] > 0
            and type(log['sha256']) is str and re.fullmatch('[0-9a-f]{64}',log['sha256']),'validation log descriptor')


def verify_validation(root, folder, head, h, pins, inputs, runtime, hash_file):
    s = spec(); manifest = s.manifest(); closure = {}
    def bind(name, expected=None):
        path = folder/name
        require(not path.is_symlink(),'validation output symlink')
        actual = hash_file(path)
        require(expected is None or actual == expected,'validation output bytes:'+name)
        key = canonical(path); require(key not in closure,'validation output collision'); closure[key] = actual
        return actual
    receipt_hash = bind('validation-receipt.json'); value = read(folder/'validation-receipt.json')
    validation_contract(value,folder,head,pins,inputs,h['cleanup'],runtime)
    log = value['validation_log']; log_hash = bind('validation.log',log['sha256'])
    require((folder/'validation.log').stat().st_size == log['serialized_bytes'],'validation log size')
    tests = value['regression_isolation']
    for name,key in (('regression-plan.json','plan_sha256'),('regression-evidence.json','evidence_sha256'),('regression-result.json','result_sha256')):
        bind(name,tests[key])
    rows = read(folder/'regression-evidence.json')['modules']
    require(type(rows) is list and len(rows) == s.MODULES,'validation proof module count')
    for i,row in enumerate(rows):
        require(type(row['index']) is int and row['index'] == i,'validation proof order')
        bind(f'module-{i:03d}.json',row['receipt_sha256']); bind(f'module-{i:03d}.log',row['log_sha256'])
    require(len(closure)-2 == manifest['regression_proof_files'] and len(closure) == manifest['validation_retained_files'],
            'complete validation output closure')
    verified = verify_tests(folder,head,build_plan(root,head,h),h['recovery'])
    require(s.blob(verified) == s.blob(tests),'validation regression proof binding')
    binding = dict(receipt_sha256=receipt_hash,log_sha256=log_hash,retained_files=len(closure),
                   closure_sha256=s.digest({Path(k).name:v for k,v in closure.items()}))
    return value,binding,closure


def runtime_validation(root, folder, head):
    guard(root,head); s = spec(); s.validate_seal(); imported = compile_import_own(root); h = helpers(root)
    torch,np = h['runtime'].native_runtime(); runtime = runtime_identity(torch,np)
    cleanup = timeout_cleanup_preflight(root,head,h); check_timeout_preflight(cleanup,head,h['cleanup'])
    guard(root,head); sources,protected = protected_counts(); locks = h['locks']; api = locks.WinAPI()
    emit('native_lock_probe',locks.lock_probe(api,folder))
    emit('locked_input_capacity',dict(max_files=protected,protected_inputs=protected))
    with locks.LockedHashes(sha,lambda path:locks.ReadLease(path,api),progress=lambda v:emit('hash_progress',v),max_files=protected) as cache:
        prior,_,pins,inputs = snapshot(root,h,cache.sha); _,_,cx = parent_semantics(root,h,prior,inputs)
        h['parent'].spec().previous().source().base().check_dependencies(root,pins,cx)
        emit('phase','native_validate_full_regression_fresh_process_per_module')
        run_logged(root,command(root,folder,head,'regression'),folder/'regression.log','regression'); guard(root,head)
        for lease,_ in cache.entries.values(): lease.check()
        tests = verify_tests(folder,head,build_plan(root,head,h),h['recovery'])
        require(tests['tests'] == s.FULL_TESTS and tests['modules'] == s.MODULES,'native validation full regression')
        inventory = cache.recheck(); check_inventory(inventory,inputs,'validation final input rereads'); stats = dict(cache.stats)
    guard(root,head)
    return dict(schema='fold-c347-runtime-validation-v1',experiment_id=s.EXPERIMENT_ID,stage=s.STAGE,commit_sha=head,
        run_folder=canonical(folder),manifest_sha256=s.MANIFEST_SHA,status='PASS',source_blobs=pins,input_sha256=inputs,
        source_count=sources,input_count=protected,compile_imports=imported,regression=read(folder/'regression-result.json'),
        regression_isolation=tests,parent_summary_sha256=PARENT_SUMMARY,parent_envelope_sha256=PARENT_ENVELOPE,
        immediate_parent_semantic_reconstruction=True,parent_regression_reconstructed=True,ancestor_semantic_reruns=0,
        final_reference_rechecks=protected,hash_stats=stats,execution_revision=EXECUTION_REVISION,
        timeout_cleanup_implementation=TIMEOUT_CLEANUP_IMPLEMENTATION,timeout_cleanup_preflight=cleanup,native_runtime=runtime)


def validate(root, folder, head):
    guard(root,head); s = spec()
    emit('registration_manifest',dict(actual_manifest_sha256=s.digest(s.manifest()),expected_manifest_sha256=s.MANIFEST_SHA))
    s.validate_seal()
    require(folder.is_relative_to(root/'runs') and folder != root/'runs','output outside runs')
    folder.mkdir(parents=True,exist_ok=False); path = folder/'validation.log'
    with path.open('x',encoding='utf-8',newline='') as retained:
        with contextlib.redirect_stdout(ValidationText(sys.stdout,retained)),contextlib.redirect_stderr(ValidationText(sys.stderr,retained)):
            emit('authoring_runtime_preflight_begin',dict(commit_sha=head,run_folder=canonical(folder)))
            try:
                value = runtime_validation(root,folder,head)
            except BaseException as exc:
                emit('authoring_runtime_preflight_failure',dict(type=type(exc).__name__,message=str(exc))); raise
            emit('authoring_runtime_preflight_complete',True)
    # The transcript is closed before its final hash enters the exclusively written receipt.
    guard(root,head)
    value['validation_log'] = dict(file='validation.log',sha256=sha(path),serialized_bytes=path.stat().st_size)
    save(folder/'validation-receipt.json',value)
    emit('authoring_runtime_preflight_receipt',dict(path=str(folder/'validation-receipt.json'),sha256=sha(folder/'validation-receipt.json')))


def ready_for_execution(folder, head):
    require(folder.is_dir() and not folder.is_symlink(),'existing validation folder required')
    require(not (folder/'science').exists() and not (folder/'execution-envelope.json').exists(),'no automatic retry of execution')
    value = read(folder/'validation-receipt.json')
    require(value['schema'] == 'fold-c347-runtime-validation-v1' and value['status'] == 'PASS'
            and value['commit_sha'] == head and value['run_folder'] == canonical(folder)
            and value['manifest_sha256'] == spec().MANIFEST_SHA,'validated run identity')
    require(value['validation_log']['file'] == 'validation.log'
            and sha(folder/'validation.log') == value['validation_log']['sha256']
            and (folder/'validation.log').stat().st_size == value['validation_log']['serialized_bytes'],'sealed validation transcript')
    check_regression(value['regression'],head,spec().FULL_TESTS)


def execute_stages(regression, audit, verify, finalize):
    emit('phase','validated_regression_reuse'); tests = regression()
    require(tests['tests'] == spec().FULL_TESTS and tests['modules'] == spec().MODULES,'verified regression scope')
    emit('phase','saved_loss_correctness_transition_audit'); value = audit()
    emit('phase','saved_diagnostic_reconstruction'); checked = verify()
    require(spec().blob(value) == spec().blob(checked),'saved result mismatch')
    emit('phase','final_uncached_input_recheck'); inventory = finalize(); return value,tests,inventory


def scientific_worker(root, folder, head):
    guard(root,head); s = spec(); s.validate_seal(); ready_for_execution(folder,head); h = helpers(root)
    torch,np = h['runtime'].native_runtime(); runtime = runtime_identity(torch,np); start = time.monotonic()
    sources,protected = protected_counts(); validation_count = s.manifest()['validation_retained_files']
    locks = h['locks']; api = locks.WinAPI()
    emit('locked_input_capacity',dict(max_files=protected,protected_inputs=protected,validation_outputs=validation_count))
    with locks.LockedHashes(sha,lambda path:locks.ReadLease(path,api),progress=lambda v:emit('hash_progress',v),max_files=protected) as cache, \
         locks.LockedHashes(sha,lambda path:locks.ReadLease(path,api),progress=lambda v:emit('validation_hash_progress',v),max_files=validation_count) as validation_cache:
        prior,_,pins,inputs = snapshot(root,h,cache.sha); source_out,data_out,cx = parent_semantics(root,h,prior,inputs)
        h['parent'].spec().previous().source().base().check_dependencies(root,pins,cx)
        out = folder/'science'; files = []; validated = {}
        def regression():
            value,binding,closure = verify_validation(root,folder,head,h,pins,inputs,runtime,validation_cache.sha)
            validated.update(value=value,binding=binding,closure=closure)
            guard(root,head); emit('validated_regression_reused',dict(tests=s.FULL_TESTS,modules=s.MODULES,**binding))
            return value['regression_isolation']
        def audit():
            out.mkdir(exist_ok=False)
            with cx[-1].guarded.no_neural(): return s.run_diagnostic(out,source_out,data_out,cx,read)
        def verification():
            with cx[-1].guarded.no_neural():
                value,bound = bound_semantics(out,lambda:s.semantic_recheck(out,source_out,data_out,cx,read))
            files.extend(bound); return value
        value,tests,inventory = execute_stages(regression,audit,verification,cache.recheck)
        check_inventory(inventory,inputs,'all final input rereads')
        validation_inventory = validation_cache.recheck()
        check_inventory(validation_inventory,validated['closure'],'all final validation output rereads')
        stats,validation_stats = dict(cache.stats),dict(validation_cache.stats)
    guard(root,head); s.check_summary(value); require(artifacts(out) == files,'final output binding')
    primary = dict(schema='fold-c347-diagnostic-v1',experiment_id=s.EXPERIMENT_ID,stage=s.STAGE,commit_sha=head,status='PASS',
        diagnostic_execution_valid=True,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,
        manifest_sha256=s.MANIFEST_SHA,source_blobs=pins,input_sha256=inputs,artifacts=files,validation_summary=value,
        runtime=dict(**runtime,worker_seconds=time.monotonic()-start,
            process_peak_rss_bytes=h['parent'].spec().previous().source().base().peak_rss(),peak_vram_bytes=None))
    save(out/'summary.json',primary)
    envelope = dict(schema='fold-c347-execution-envelope-v1',commit_sha=head,scientific_status='PASS',scientific_summary_sha256=sha(out/'summary.json'),
        source_blobs=pins,input_sha256=inputs,source_count=sources,input_count=protected,
        regression=read(folder/'regression-result.json'),regression_isolation=tests,parent_summary_sha256=PARENT_SUMMARY,
        parent_envelope_sha256=PARENT_ENVELOPE,immediate_parent_semantic_reconstruction=True,parent_regression_reconstructed=True,
        ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,final_reference_rechecks=protected,hash_stats=stats,
        manifest_sha256=s.MANIFEST_SHA,scientific_work=s.WORK,execution_revision=EXECUTION_REVISION,
        timeout_cleanup_implementation=TIMEOUT_CLEANUP_IMPLEMENTATION,
        timeout_cleanup_preflight=validated['value']['timeout_cleanup_preflight'],validation_binding=validated['binding'],
        validation_reference_rechecks=validation_count,validation_hash_stats=validation_stats,
        regression_executions_in_validate=1,regression_executions_in_execute=0,
        retained_output_files=s.manifest()['retained_output_files'])
    save(folder/'execution-envelope.json',envelope)
    emit('summary',str(out/'summary.json')); emit('summary_sha256',envelope['scientific_summary_sha256'])
    emit('preserved_parent_gate',dict(candidate_gate=value['parent_validation_summary']['candidate_gate'],eligible_seed_count=value['parent_validation_summary']['eligible_seed_count']))
    with cx[-1].guarded.no_neural(): s.report_results(value,emit)
    require(artifacts(out) == files,'result report changed outputs')
    emit('execution_envelope',dict(path=str(folder/'execution-envelope.json'),sha256=sha(folder/'execution-envelope.json')))
    emit('persisted_saved_loss_transition',dict(status='PASS',**s.WORK))


def verify_outputs(root, folder, head):
    guard(root,head); s = spec(); s.validate_seal(); h = helpers(root); out = folder/'science'
    torch,np = h['runtime'].native_runtime(); runtime = runtime_identity(torch,np)
    sources,protected = protected_counts(); validation_count = s.manifest()['validation_retained_files']
    locks = h['locks']; api = locks.WinAPI()
    with locks.LockedHashes(sha,lambda path:locks.ReadLease(path,api),progress=lambda v:emit('verify_hash_progress',v),max_files=protected) as cache, \
         locks.LockedHashes(sha,lambda path:locks.ReadLease(path,api),progress=lambda v:emit('verify_validation_hash_progress',v),max_files=validation_count) as validation_cache:
        prior,_,pins,inputs = snapshot(root,h,cache.sha); r,v = read(out/'summary.json'),read(folder/'execution-envelope.json')
        validated,binding,closure = verify_validation(root,folder,head,h,pins,inputs,runtime,validation_cache.sha)
        require(v['execution_revision'] == EXECUTION_REVISION
                and v['timeout_cleanup_implementation'] == TIMEOUT_CLEANUP_IMPLEMENTATION,'execution/cleanup implementation revision')
        check_timeout_preflight(v['timeout_cleanup_preflight'],head,h['cleanup'])
        require(s.blob(v['timeout_cleanup_preflight']) == s.blob(validated['timeout_cleanup_preflight'])
                and s.blob(v['validation_binding']) == s.blob(binding),'native validation envelope binding')
        require(type(v['regression_executions_in_validate']) is int and v['regression_executions_in_validate'] == 1
                and type(v['regression_executions_in_execute']) is int and v['regression_executions_in_execute'] == 0
                and v['validation_reference_rechecks'] == validation_count
                and v['validation_hash_stats']['final_reference_rechecks'] == validation_count
                and v['retained_output_files'] == s.manifest()['retained_output_files'],'validation reuse/retention')
        require(r['schema'] == 'fold-c347-diagnostic-v1' and v['schema'] == 'fold-c347-execution-envelope-v1' and r['commit_sha'] == v['commit_sha'] == head
                and r['experiment_id'] == s.EXPERIMENT_ID and r['stage'] == s.STAGE,'child identity')
        s.check_summary(r['validation_summary'])
        require(r['status'] == v['scientific_status'] == 'PASS' and r['diagnostic_execution_valid'] is True
                and r['capability_gate_applicable'] is False and r['gate_f_candidate'] is False and r['production_adoption'] is False,'diagnostic flags')
        require(r['source_blobs'] == v['source_blobs'] == pins and r['input_sha256'] == v['input_sha256'] == inputs
                and v['source_count'] == sources and v['input_count'] == protected,'complete child maps')
        require(v['parent_summary_sha256'] == PARENT_SUMMARY and v['parent_envelope_sha256'] == PARENT_ENVELOPE
                and v['immediate_parent_semantic_reconstruction'] is True and v['parent_regression_reconstructed'] is True
                and v['ancestor_semantic_reruns'] == 0 and v['saved_semantic_reconstruction'] is True
                and v['final_reference_rechecks'] == protected and v['hash_stats']['final_reference_rechecks'] == protected,'completion')
        require(sha(out/'summary.json') == v['scientific_summary_sha256'] and r['manifest_sha256'] == v['manifest_sha256'] == s.MANIFEST_SHA
                and v['scientific_work'] == s.WORK and {k:r['runtime'][k] for k in runtime} == runtime,'work/seal/summary/runtime')
        check_regression(v['regression'],head,s.FULL_TESTS)
        require(s.blob(validated['regression_isolation']) == s.blob(v['regression_isolation']),'test evidence binding')
        h['legacy'].descriptors(out,r['artifacts'],s.OUTPUTS,sha); source_out,data_out,cx = parent_semantics(root,h,prior,inputs)
        with cx[-1].guarded.no_neural(): checked,_ = bound_semantics(out,lambda:s.semantic_recheck(out,source_out,data_out,cx,read))
        require(s.blob(checked) == s.blob(r['validation_summary']),'fresh reconstruction')
        check_inventory(cache.recheck(),inputs,'fresh input rereads')
        check_inventory(validation_cache.recheck(),closure,'fresh validation output rereads')
    guard(root,head)
    emit('execution_envelope_verified',dict(source_pins=sources,protected_inputs=protected,full_tests=s.FULL_TESTS,
         modules=s.MODULES,validation_outputs=validation_count,retained_outputs=s.manifest()['retained_output_files']))


def run(root, folder, head):
    guard(root,head); spec().validate_seal(); require(folder.is_relative_to(root/'runs') and folder != root/'runs','output outside runs')
    ready_for_execution(folder,head); valid = False
    emit('execution_role','C347-SAVED-LOSS-TRANSITION'); emit('scientific_execution_head',head)
    emit('execution_revision',EXECUTION_REVISION)
    try:
        run_logged(root,command(root,folder,head,'science'),folder/'science.log','science')
        run_logged(root,command(root,folder,head,'verify'),folder/'verify.log','verify'); valid = True
    finally:
        guard(root,head); emit('run_execution_valid',valid)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); parser.add_argument('--folder',type=Path,required=True)
    parser.add_argument('--expected-head',required=True); parser.add_argument('--mode',choices=('validate','run','science','regression','module','verify'),default='run')
    parser.add_argument('--module-index',type=int); parser.add_argument('--plan-sha256')
    a = parser.parse_args(); root,folder = a.root.resolve(),a.folder.resolve()
    require(folder.is_relative_to(root/'runs') and folder != root/'runs','output outside runs')
    if a.mode == 'module': module_child(root,folder,a.expected_head,a.module_index,a.plan_sha256)
    else:
        require(a.module_index is None and a.plan_sha256 is None,'module-only arguments')
        {'validate':validate,'run':run,'science':scientific_worker,'regression':regression_child,'verify':verify_outputs}[a.mode](root,folder,a.expected_head)


if __name__ == '__main__':
    sys.path.insert(0,str(Path(__file__).resolve().parents[1])); main()
