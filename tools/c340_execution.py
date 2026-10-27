"""C340 protected paired length-exposure training after accepted C339 diagnosis."""
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
PARENT_HEAD = 'f58c22f83fe7c41c451d5d0bcf26c249ab21908b'
PARENT_FOLDER = 'runs/c339-support-transfer-38b97ac63a92445cb0b212d1fe9a73fe'
PARENT_SUMMARY = '304dec1fcbb6532da968fd21c337f39079f4abb1cc305893722e466636ef4dbf'
PARENT_ENVELOPE = 'db81d2dba1bd8a1b2f850c3b5a7833a9b95b7a24d8cddc984fc1e3a5e1195be3'
P_PATH = 'tools/c339_execution.py'
P_BLOB = '27c83c8b5a3af364475a73ffd1563607255607ad'
S_PATH = 'fold_lm/v05_benchmarks/model_c339_saved_support_transfer.py'
S_BLOB = 'edde2009f4b8135199eea993d2a85aa987e87d4b'
BASE_IDS_SHA = 'b5d92857cbb2c72d61a1e2a9af242f57e283fd7c26e5e6e86661d6cbdb35fbf4'
TEST_MODULES = ('tests_lm.test_v05_c340_length5_training', 'tests_lm.test_v05_c340_execution')


def spec():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c340_length5_training')


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
    return bool(match and re.findall(r'C(\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)',match[1]) == ['340'])


def guard(root, head):
    require(type(head) is str and re.fullmatch('[0-9a-f]{40}',head),'execution HEAD')
    require(git(root,'branch','--show-current') == BRANCH and git(root,'rev-parse','HEAD') == head,'branch/HEAD')
    require(not git(root,'status','--porcelain','--untracked-files=no'),'dirty tracked tree')
    require(active((root/'docs/experiment-ledger-and-handoff.md').read_text(encoding='utf-8')),'C340 uniquely ACTIVE')


def helpers(root):
    for name,oid in ((P_PATH,P_BLOB),(S_PATH,S_BLOB)):
        require(git(root,'rev-parse','HEAD:'+name) == oid,'accepted C339 pin'); source_bytes(root/name,oid)
    loader = importlib.util.spec_from_file_location('_c340_parent',root/P_PATH)
    require(loader is not None and loader.loader is not None,'parent loader')
    parent = importlib.util.module_from_spec(loader); loader.loader.exec_module(parent); parent.spec().validate_seal()
    prior = parent.helpers(root)
    require(type(prior) is dict and set(prior) == {'parent','prior','recovery','c330','runtime','legacy','locks'},'C339 helper bridge')
    return dict(parent=parent,prior=prior,**{k:prior[k] for k in ('recovery','c330','runtime','legacy','locks')})


def receipt(head, count):
    return dict(commit_sha=head,tests=count,failures=0,errors=0,skipped=0,successful=True)


def check_regression(value, head, count):
    require(spec().blob(value) == spec().blob(receipt(head,count)),'complete regression receipt')


def parent_contract(r, v, parent):
    s = parent.spec(); s.validate_seal(); s.check_summary(r['validation_summary'])
    require(r['schema'] == 'fold-c339-diagnostic-v1' and v['schema'] == 'fold-c339-execution-envelope-v1'
            and r['commit_sha'] == v['commit_sha'] == PARENT_HEAD and r['experiment_id'] == s.EXPERIMENT_ID
            and r['stage'] == s.STAGE,'parent identity')
    require(r['status'] == v['scientific_status'] == 'PASS' and r['diagnostic_execution_valid'] is True
            and r['capability_gate_applicable'] is False and r['gate_f_candidate'] is False and r['production_adoption'] is False
            and r['validation_summary']['parent_candidate_gate'] is False
            and r['validation_summary']['parent_eligible_seed_count'] == 0,'diagnostic parent preserves negative C338')
    require(r['manifest_sha256'] == v['manifest_sha256'] == s.MANIFEST_SHA and v['scientific_work'] == s.WORK
            and v['scientific_summary_sha256'] == PARENT_SUMMARY,'parent manifest/work')
    require(v['source_count'] == len(v['source_blobs']) == 895 and v['input_count'] == len(v['input_sha256']) == 5769
            and r['source_blobs'] == v['source_blobs'] and r['input_sha256'] == v['input_sha256']
            and v['source_blobs'].get(P_PATH) == P_BLOB and v['source_blobs'].get(S_PATH) == S_BLOB,'parent protection')
    require(v['parent_summary_sha256'] == parent.PARENT_SUMMARY and v['parent_envelope_sha256'] == parent.PARENT_ENVELOPE
            and v['immediate_parent_semantic_reconstruction'] is True and v['parent_regression_reconstructed'] is True
            and v['ancestor_semantic_reruns'] == 0 and v['saved_semantic_reconstruction'] is True
            and v['final_reference_rechecks'] == 5769 and v['hash_stats']['final_reference_rechecks'] == 5769,'parent completion')
    check_regression(v['regression'],PARENT_HEAD,6202)


def parent_test_files(folder, envelope, hash_file):
    bound = envelope['regression_isolation']; require(bound['tests'] == 6202 and bound['modules'] == 229,'parent test scope')
    wanted = {'regression-plan.json':bound['plan_sha256'],'regression-evidence.json':bound['evidence_sha256'],
              'regression-result.json':bound['result_sha256']}
    for name,value in wanted.items(): require(hash_file(folder/name) == value,'parent test record:'+name)
    rows = read(folder/'regression-evidence.json')['modules']; require(len(rows) == 229,'all parent modules')
    for i,row in enumerate(rows):
        require(type(row['index']) is int and row['index'] == i,'parent proof order')
        wanted[f'module-{i:03d}.json'] = row['receipt_sha256']; wanted[f'module-{i:03d}.log'] = row['log_sha256']
    require(len(wanted) == 461,'all461parent test proofs')
    for name,value in wanted.items(): require(hash_file(folder/name) == value,'parent proof bytes:'+name)
    return {canonical(folder/name):value for name,value in wanted.items()}


def snapshot(root, h, hash_file):
    parent = h['parent']; s = spec(); s.validate_seal(); folder = root/PARENT_FOLDER; out = folder/'science'
    require(not folder.is_symlink() and not out.is_symlink(),'parent path link')
    require(hash_file(out/'summary.json') == PARENT_SUMMARY and hash_file(folder/'execution-envelope.json') == PARENT_ENVELOPE,'exact parent bytes')
    r,v = read(out/'summary.json'),read(folder/'execution-envelope.json'); parent_contract(r,v,parent)
    _,_,pins,inputs = parent.snapshot(root,h['prior'],hash_file)
    require(pins == v['source_blobs'] and inputs == v['input_sha256'],'reconstructed parent maps')
    pins,inputs = dict(pins),dict(inputs)
    added = h['legacy'].descriptors(out,r['artifacts'],parent.spec().OUTPUTS,hash_file)
    added.update({canonical(out/'summary.json'):PARENT_SUMMARY,canonical(folder/'execution-envelope.json'):PARENT_ENVELOPE})
    proofs = parent_test_files(folder,v,hash_file); require(not set(added)&set(proofs),'parent collision'); added.update(proofs)
    require(len(added) == 467 and not set(added)&set(inputs),'all467parent files'); inputs.update(added)
    verified = parent.verify_tests(folder,PARENT_HEAD,parent.build_plan(root,PARENT_HEAD,h['prior']),h['recovery'])
    require(s.blob(verified) == s.blob(v['regression_isolation']),'parent6202proof semantics')
    tree = h['legacy'].tree_blobs(root)
    for name in s.OWN:
        path = canonical(root/name); require(name in tree and name not in pins and path not in inputs,'child ownership')
        pins[name] = tree[name]; inputs[path] = hash_file(root/name)
    require(len(pins) == s.SOURCE_COUNT and len(inputs) == s.INPUT_COUNT,'complete child protection')
    for name,oid in pins.items():
        require(tree.get(name) == oid,'inherited source changed'); source_bytes(root/name,oid)
        require(inputs.get(canonical(root/name)) == hash_file(root/name),'source/input binding')
    return r,v,pins,inputs


def parent_semantics(root, h, prior, inputs):
    out = root/PARENT_FOLDER/'science'
    source_out = root/h['parent'].PARENT_FOLDER/'science'
    data_out = root/h['c330'].PARENT_FOLDER/'science'
    p = h['parent'].spec()
    for folder,names in ((out,p.OUTPUTS),(source_out,(*p.parent().OUTPUTS,'summary.json')),
                        (data_out,('dataset.json','original-prompts.json','interior-prompts.json'))):
        require(all(canonical(folder/name) in inputs for name in names),'protected semantic inputs')
    base = p.parent().previous().source().base(); cx = base.context()
    with cx[-1].guarded.no_neural():
        source_prior = read(source_out/'summary.json')['validation_summary']
        value = p.semantic_recheck(out,source_out,data_out,source_prior,read)
        require(spec().blob(value) == spec().blob(prior['validation_summary']),'immediate C339 semantics')
        data,old,new = p.parent().previous().load_data(data_out,read)
        require(base.digest(data) == base.DATA_SHA and base.digest(old) == base.PROMPTS_SHA
                and base.digest(new) == base.digest(cx[2].new_prompts(data)),'canonical data/prompts')
        cx[-1].c.p267.validate_data(data); cx[2].check_prompts(data,old,new,cx[3],cx[-1])
    emit('accepted_parent_semantics',dict(parent_files=467,regression_tests=6202,model_forwards=0,ancestor_semantic_reruns=0))
    return data_out,cx


def validate_plan(plan, head, recovery):
    s = spec()
    require(set(plan) == {'schema','commit_sha','manifest_sha256','test_ids_sha256','groups'}
            and plan['schema'] == 'fold-c340-regression-plan-v1' and plan['commit_sha'] == head
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
    require(s.digest(ids[:-s.OWN_TESTS]) == BASE_IDS_SHA and s.digest(ids) == plan['test_ids_sha256'],'unchanged6202test IDs')


def build_plan(root, head, h):
    prior = h['parent'].build_plan(root,head,h['prior']); recovery = h['recovery']; groups = list(prior['groups'])
    count = 0
    for module in TEST_MODULES:
        own = list(recovery.flatten(unittest.defaultTestLoader.loadTestsFromName(module)))
        require(own and all(type(t).__module__ == module for t in own),'actual own loader')
        count += len(own); groups.append(dict(module=module,test_ids=[t.id() for t in own]))
    require(count == spec().OWN_TESTS,'actual own total')
    plan = dict(schema='fold-c340-regression-plan-v1',commit_sha=head,manifest_sha256=spec().MANIFEST_SHA,
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
    require(process.returncode == 0,'C340 '+phase+' failed;no automatic retry'); return process.pid


def module_child(root, folder, head, index, plan_sha):
    guard(root,head); spec().validate_seal(); recovery = helpers(root)['recovery']
    require(sha(folder/'regression-plan.json') == plan_sha,'module plan bytes')
    plan = read(folder/'regression-plan.json'); validate_plan(plan,head,recovery)
    require(type(index) is int and 0 <= index < spec().MODULES,'module index')
    group = plan['groups'][index]; process = dict(pid=os.getpid(),parent_pid=os.getppid())
    marker = dict(index=index,module=group['module'],tests=len(group['test_ids']),**process)
    emit('regression_module_begin',marker); value = recovery.execute_module(group['module'],group['test_ids'])
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
    save(folder/'regression-evidence.json',dict(schema='fold-c340-regression-v1',commit_sha=head,plan_sha256=ph,
         test_ids_sha256=plan['test_ids_sha256'],modules=items))
    save(folder/'regression-result.json',receipt(head,total))
    emit('regression_result',dict(**receipt(head,total),modules=spec().MODULES,seconds=round(time.monotonic()-start,3)))


def verify_tests(folder, head, plan, recovery):
    validate_plan(plan,head,recovery); require(spec().blob(read(folder/'regression-plan.json')) == spec().blob(plan),'planned inventory')
    value = read(folder/'regression-evidence.json'); ph = sha(folder/'regression-plan.json')
    require(set(value) == {'schema','commit_sha','plan_sha256','test_ids_sha256','modules'} and value['schema'] == 'fold-c340-regression-v1'
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


def execute_stages(preflight, regression, train, verify, finalize):
    emit('phase','native_length5_preflight'); preflight()
    emit('phase','full_regression_fresh_process_per_module'); tests = regression()
    require(tests['tests'] == spec().FULL_TESTS and tests['modules'] == spec().MODULES,'verified regression scope')
    emit('phase','paired_length5_training'); value = train()
    emit('phase','saved_training_reconstruction'); checked = verify()
    require(spec().blob(value) == spec().blob(checked),'saved result mismatch')
    emit('phase','final_uncached_input_recheck'); inventory = finalize(); return value,tests,inventory


def scientific_worker(root, folder, head):
    guard(root,head); s = spec(); s.validate_seal(); h = helpers(root)
    torch,np = h['runtime'].native_runtime(); locks = h['locks']; api = locks.WinAPI(); start = time.monotonic()
    emit('native_lock_probe',locks.lock_probe(api,folder)); emit('locked_input_capacity',dict(max_files=s.INPUT_COUNT,protected_inputs=s.INPUT_COUNT))
    with locks.LockedHashes(sha,lambda path:locks.ReadLease(path,api),progress=lambda v:emit('hash_progress',v),max_files=s.INPUT_COUNT) as cache:
        parent,_,pins,inputs = snapshot(root,h,cache.sha); data_out,cx = parent_semantics(root,h,parent,inputs)
        s.previous().source().base().check_dependencies(root,pins,cx)
        out = folder/'science'; out.mkdir(exist_ok=False); files = []
        emit('registration_check',dict(source_pins=len(pins),protected_inputs=len(inputs),full_tests=s.FULL_TESTS,manifest_sha256=s.MANIFEST_SHA))
        def regression():
            run_logged(root,command(root,folder,head,'regression'),folder/'regression.log','regression'); guard(root,head)
            for lease,_ in cache.entries.values(): lease.check()
            return verify_tests(folder,head,build_plan(root,head,h),h['recovery'])
        def verification():
            with cx[-1].guarded.no_neural():
                value,bound = bound_semantics(out,lambda:s.semantic_recheck(out,data_out,cx,read))
            files.extend(bound); return value
        value,tests,inventory = execute_stages(lambda:s.native_preflight(data_out,cx,root,pins,read),regression,
            lambda:s.run_training(out,data_out,cx,root,pins,read),verification,cache.recheck)
        require(len(inventory) == s.INPUT_COUNT and {r['path']:r['sha256'] for r in inventory} == inputs,'all final input rereads')
        stats = dict(cache.stats)
    guard(root,head); s.check_summary(value); require(artifacts(out) == files,'final output binding')
    status = 'PASS' if value['candidate_gate'] else 'FAIL'
    primary = dict(schema='fold-c340-trained-v1',experiment_id=s.EXPERIMENT_ID,stage=s.STAGE,commit_sha=head,status=status,
        scientific_execution_valid=True,capability_gate_applicable=True,gate_f_candidate=False,production_adoption=False,
        manifest_sha256=s.MANIFEST_SHA,source_blobs=pins,input_sha256=inputs,artifacts=files,validation_summary=value,
        runtime=dict(python=sys.version.split()[0],torch=str(torch.__version__),numpy=np.__version__,device='cpu',precision='float64',
            threads=2,worker_seconds=time.monotonic()-start,process_peak_rss_bytes=s.previous().source().base().peak_rss(),peak_vram_bytes=None))
    save(out/'summary.json',primary)
    envelope = dict(schema='fold-c340-execution-envelope-v1',commit_sha=head,scientific_status=status,scientific_summary_sha256=sha(out/'summary.json'),
        source_blobs=pins,input_sha256=inputs,source_count=s.SOURCE_COUNT,input_count=s.INPUT_COUNT,
        regression=read(folder/'regression-result.json'),regression_isolation=tests,parent_summary_sha256=PARENT_SUMMARY,
        parent_envelope_sha256=PARENT_ENVELOPE,immediate_parent_semantic_reconstruction=True,parent_regression_reconstructed=True,
        ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,final_reference_rechecks=s.INPUT_COUNT,hash_stats=stats,
        manifest_sha256=s.MANIFEST_SHA,scientific_work=s.WORK)
    save(folder/'execution-envelope.json',envelope)
    emit('summary',str(out/'summary.json')); emit('summary_sha256',envelope['scientific_summary_sha256'])
    for row in value['paired_comparisons']: emit('C340 paired comparison',row)
    for row in value['seed_results']: emit('C340 seed result',row)
    emit('candidate_gate',dict(passed=value['candidate_gate'],eligible_seed_count=value['eligible_seed_count']))
    emit('scientific_status',status); emit('execution_envelope',dict(path=str(folder/'execution-envelope.json'),sha256=sha(folder/'execution-envelope.json')))
    emit('persisted_length5_training','PASS;states=10;steps=24000;forwards=27420;raw_argmax=256classes')


def verify_outputs(root, folder, head):
    guard(root,head); s = spec(); s.validate_seal(); h = helpers(root); out = folder/'science'
    parent,_,pins,inputs = snapshot(root,h,sha); r,v = read(out/'summary.json'),read(folder/'execution-envelope.json')
    require(r['schema'] == 'fold-c340-trained-v1' and v['schema'] == 'fold-c340-execution-envelope-v1' and r['commit_sha'] == v['commit_sha'] == head
            and r['experiment_id'] == s.EXPERIMENT_ID and r['stage'] == s.STAGE,'child identity')
    s.check_summary(r['validation_summary']); status = 'PASS' if r['validation_summary']['candidate_gate'] else 'FAIL'
    require(r['status'] == v['scientific_status'] == status and r['scientific_execution_valid'] is True
            and r['capability_gate_applicable'] is True and r['gate_f_candidate'] is False and r['production_adoption'] is False,'scientific flags')
    require(r['source_blobs'] == v['source_blobs'] == pins and r['input_sha256'] == v['input_sha256'] == inputs
            and v['source_count'] == s.SOURCE_COUNT and v['input_count'] == s.INPUT_COUNT,'complete child maps')
    require(v['parent_summary_sha256'] == PARENT_SUMMARY and v['parent_envelope_sha256'] == PARENT_ENVELOPE
            and v['immediate_parent_semantic_reconstruction'] is True and v['parent_regression_reconstructed'] is True
            and v['ancestor_semantic_reruns'] == 0 and v['saved_semantic_reconstruction'] is True
            and v['final_reference_rechecks'] == s.INPUT_COUNT and v['hash_stats']['final_reference_rechecks'] == s.INPUT_COUNT,'completion')
    require(sha(out/'summary.json') == v['scientific_summary_sha256'] and r['manifest_sha256'] == v['manifest_sha256'] == s.MANIFEST_SHA
            and v['scientific_work'] == s.WORK,'work/seal/summary')
    check_regression(v['regression'],head,s.FULL_TESTS)
    require(s.blob(verify_tests(folder,head,build_plan(root,head,h),h['recovery'])) == s.blob(v['regression_isolation']),'test evidence binding')
    h['legacy'].descriptors(out,r['artifacts'],s.OUTPUTS,sha); data_out,cx = parent_semantics(root,h,parent,inputs)
    with cx[-1].guarded.no_neural(): checked,_ = bound_semantics(out,lambda:s.semantic_recheck(out,data_out,cx,read))
    require(s.blob(checked) == s.blob(r['validation_summary']),'fresh reconstruction'); guard(root,head)
    emit('execution_envelope_verified',dict(source_pins=s.SOURCE_COUNT,protected_inputs=s.INPUT_COUNT,full_tests=s.FULL_TESTS,modules=s.MODULES))


def run(root, folder, head):
    guard(root,head); spec().validate_seal(); require(folder.is_relative_to(root/'runs') and folder != root/'runs','output outside runs')
    folder.mkdir(parents=True,exist_ok=False); valid = False
    emit('execution_role','C340-LENGTH5-TRAINING'); emit('scientific_execution_head',head)
    try:
        run_logged(root,command(root,folder,head,'science'),folder/'science.log','science')
        run_logged(root,command(root,folder,head,'verify'),folder/'verify.log','verify'); valid = True
    finally:
        guard(root,head); emit('run_execution_valid',valid)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); parser.add_argument('--folder',type=Path,required=True)
    parser.add_argument('--expected-head',required=True); parser.add_argument('--mode',choices=('run','science','regression','module','verify'),default='run')
    parser.add_argument('--module-index',type=int); parser.add_argument('--plan-sha256')
    a = parser.parse_args(); root,folder = a.root.resolve(),a.folder.resolve()
    require(folder.is_relative_to(root/'runs') and folder != root/'runs','output outside runs')
    if a.mode == 'module': module_child(root,folder,a.expected_head,a.module_index,a.plan_sha256)
    else:
        require(a.module_index is None and a.plan_sha256 is None,'module-only arguments')
        {'run':run,'science':scientific_worker,'regression':regression_child,'verify':verify_outputs}[a.mode](root,folder,a.expected_head)


if __name__ == '__main__':
    sys.path.insert(0,str(Path(__file__).resolve().parents[1])); main()
