"""C333 locked saved-pair diagnosis; retain C332 and all its bound regression proofs."""
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
PARENT_HEAD = '6a13f1e6a10cee4fad519853835fd256089456e8'
PARENT_FOLDER = 'runs/c332-trained-query-853335f262f5409e8d84c17da3809167'
PARENT_SUMMARY = '478ea25268291aeec1c73c4169a0b4a5f04f45950054214ec8eec0e190f3b89d'
PARENT_ENVELOPE = 'd6343c4ad4c7149b118183a928810d80215ffac37891b0c6a0282d6ae75f982f'
P_PATH = 'tools/c332_execution.py'
P_BLOB = 'b590cd71fab98cae8ba2388b23345dad5156d44d'
BASE_IDS_SHA = '3e801a1c8f0ffcd9fb9aab46a5377a823fc76e98584ac0b4fe6558ec5da66855'
TEST_MODULE = 'tests_lm.test_v05_c333_paired_gate_localization'


def spec():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c333_paired_gate_localization')


def require(ok, message):
    if not ok: raise ValueError(message)


def emit(name, value):
    print(name+' = '+json.dumps(value,sort_keys=True,ensure_ascii=True,allow_nan=False),flush=True)


def sha(path):
    with Path(path).open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()


def read(path):
    def unique(items):
        result = {}
        for k,v in items:
            require(k not in result,'duplicate JSON key'); result[k] = v
        return result
    def invalid(v): raise ValueError('nonfinite JSON:'+v)
    return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=unique,parse_constant=invalid)


def save(path, value):
    with Path(path).open('xb') as stream: stream.write(spec().blob(value))


def git(root, *args):
    return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.STDOUT).decode('utf-8').strip()


def canonical(path):
    return os.path.normcase(str(Path(path).resolve(strict=True)))


def source_bytes(path, oid):
    raw = Path(path).read_bytes(); normalized = raw.replace(b'\r\n',b'\n')
    def h(v): return hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest()
    require(h(raw)==oid or (raw==normalized.replace(b'\n',b'\r\n') and h(normalized)==oid),'source bytes:'+str(path))


def active(text):
    m = re.search(r'(?ms)^## Formal state\s+(.*?)(?=^## |\Z)',text)
    return bool(m and re.findall(r'C(\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)',m[1])==['333'])


def guard(root, head):
    require(type(head) is str and re.fullmatch('[0-9a-f]{40}',head),'execution HEAD')
    require(git(root,'branch','--show-current')==BRANCH and git(root,'rev-parse','HEAD')==head,'branch/HEAD')
    require(not git(root,'status','--porcelain','--untracked-files=no'),'dirty tracked tree')
    require(active((root/'docs/experiment-ledger-and-handoff.md').read_text(encoding='utf-8')),'C333 uniquely ACTIVE')


def helpers(root):
    require(git(root,'rev-parse','HEAD:'+P_PATH)==P_BLOB,'accepted C332 executor pin'); source_bytes(root/P_PATH,P_BLOB)
    loader = importlib.util.spec_from_file_location('_c333_parent_executor',root/P_PATH)
    require(loader is not None and loader.loader is not None,'parent executor loader')
    p = importlib.util.module_from_spec(loader); loader.loader.exec_module(p); p.spec().validate_seal()
    # ph = (C331 executor, (R1.2 executor, C330 executor, runtime, legacy, locks)).
    return p,p.helpers(root)


def receipt(head, count):
    return dict(commit_sha=head,tests=count,failures=0,errors=0,skipped=0,successful=True)


def check_regression(value, head, count):
    require(spec().blob(value)==spec().blob(receipt(head,count)),'complete regression receipt')


def parent_contract(r, v, p):
    s = p.spec(); s.validate_seal(); s.check_summary(r['validation_summary'])
    require(r['schema']=='fold-c332-science-v1' and v['schema']=='fold-c332-execution-envelope-v1'
            and r['commit_sha']==v['commit_sha']==PARENT_HEAD and r['experiment_id']==s.EXPERIMENT_ID
            and r['stage']==s.STAGE,'parent identity')
    require(r['status']==v['scientific_status']=='FAIL' and r['validation_summary']['candidate_gate'] is False
            and r['diagnostic_execution_valid'] is True and r['capability_gate_applicable'] is True
            and r['gate_f_candidate'] is False and r['production_adoption'] is False,'accepted valid negative')
    require(r['manifest_sha256']==v['manifest_sha256']==s.MANIFEST_SHA and v['scientific_work']==s.WORK
            and v['scientific_summary_sha256']==PARENT_SUMMARY,'parent seal/work')
    require(v['source_count']==len(v['source_blobs'])==853 and v['input_count']==len(v['input_sha256'])==2508
            and r['source_blobs']==v['source_blobs'] and r['input_sha256']==v['input_sha256']
            and v['source_blobs'].get(P_PATH)==P_BLOB,'full parent protection')
    require(v['parent_summary_sha256']==p.PARENT_SUMMARY and v['parent_envelope_sha256']==p.PARENT_ENVELOPE
            and v['immediate_parent_semantic_reconstruction'] is True and v['parent_regression_reconstructed'] is True
            and v['ancestor_semantic_reruns']==0 and v['saved_semantic_reconstruction'] is True
            and v['final_reference_rechecks']==2508 and v['hash_stats']['final_reference_rechecks']==2508,'parent completion')
    check_regression(v['regression'],PARENT_HEAD,5946)


def parent_test_files(folder, envelope, hash_file):
    b = envelope['regression_isolation']; require(b['tests']==5946 and b['modules']==222,'parent regression scope')
    wanted = {'regression-plan.json':b['plan_sha256'],'regression-evidence.json':b['evidence_sha256'],
              'regression-result.json':b['result_sha256']}
    for name,h in wanted.items(): require(hash_file(folder/name)==h,'parent test record:'+name)
    modules = read(folder/'regression-evidence.json')['modules']; require(len(modules)==222,'parent module count')
    for i,row in enumerate(modules):
        require(type(row['index']) is int and row['index']==i,'parent module order')
        wanted[f'module-{i:03d}.json'] = row['receipt_sha256']; wanted[f'module-{i:03d}.log'] = row['log_sha256']
    require(len(wanted)==447,'all parent test proofs')
    for name,h in wanted.items(): require(hash_file(folder/name)==h,'parent module bytes:'+name)
    return {canonical(folder/name):h for name,h in wanted.items()}


def snapshot(root, h, hash_file):
    p,ph = h; folder = root/PARENT_FOLDER; out = folder/'science'; s = spec(); s.validate_seal()
    require(not folder.is_symlink() and not out.is_symlink(),'parent path link')
    require(hash_file(out/'summary.json')==PARENT_SUMMARY and hash_file(folder/'execution-envelope.json')==PARENT_ENVELOPE,'exact C332 bytes')
    result = read(out/'summary.json'); envelope = read(folder/'execution-envelope.json'); parent_contract(result,envelope,p)
    _,_,pins,inputs = p.snapshot(root,ph,hash_file)
    require(pins==envelope['source_blobs'] and inputs==envelope['input_sha256'],'reconstructed parent maps')
    pins,inputs = dict(pins),dict(inputs); legacy = ph[1][3]
    added = legacy.descriptors(out,result['artifacts'],p.spec().OUTPUTS,hash_file)
    added.update({canonical(out/'summary.json'):PARENT_SUMMARY,canonical(folder/'execution-envelope.json'):PARENT_ENVELOPE})
    proofs = parent_test_files(folder,envelope,hash_file)
    require(not set(added)&set(proofs),'parent output collision'); added.update(proofs)
    require(len(added)==455 and not set(added)&set(inputs),'all455parent output files'); inputs.update(added)
    plan = p.build_plan(root,PARENT_HEAD,ph); checked = p.verify_tests(folder,PARENT_HEAD,plan,ph[1][0])
    require(spec().blob(checked)==spec().blob(envelope['regression_isolation']),'parent5946test proof semantics')
    tree = legacy.tree_blobs(root)
    for name in s.OWN:
        key = canonical(root/name)
        require(name in tree and name not in pins and key not in inputs,'child source ownership')
        pins[name] = tree[name]; inputs[key] = hash_file(root/name)
    require(len(pins)==s.SOURCE_COUNT and len(inputs)==s.INPUT_COUNT,'child protection counts')
    for name,oid in pins.items():
        require(tree.get(name)==oid,'source changed:'+name); source_bytes(root/name,oid)
        require(inputs.get(canonical(root/name))==hash_file(root/name),'source input binding')
    return result,envelope,pins,inputs


def parent_semantics(root, h, parent_result, inputs):
    p,ph = h; source_out = root/ph[1][1].PARENT_FOLDER/'science'
    for name in ('dataset.json','original-prompts.json','interior-prompts.json'):
        require(canonical(source_out/name) in inputs,'protected C329 data/prompts')
    b = p.spec().source().base(); cx = b.context()
    with cx[-1].guarded.no_neural():
        value = p.spec().semantic_recheck(root/PARENT_FOLDER/'science',source_out,cx,read)
        require(spec().blob(value)==spec().blob(parent_result['validation_summary']),'immediate C332 saved semantics')
    emit('accepted_parent_semantics',dict(scientific_status='FAIL',execution_valid=True,parent_files=455,
         regression_tests=5946,model_forwards=0,ancestor_semantic_reruns=0))
    return cx


def validate_plan(plan, head, r):
    s = spec()
    require(set(plan)=={'schema','commit_sha','manifest_sha256','test_ids_sha256','groups'}
            and plan['schema']=='fold-c333-regression-plan-v1' and plan['commit_sha']==head
            and plan['manifest_sha256']==s.MANIFEST_SHA,'test plan identity')
    groups = plan['groups']; require(type(groups) is list and len(groups)==s.MODULES,'module count')
    ids,modules = [],[]
    for g in groups:
        require(set(g)=={'module','test_ids'} and r.allowed_module(g['module']) and type(g['test_ids']) is list
                and g['test_ids'] and all(type(t) is str and t.startswith(g['module']+'.') for t in g['test_ids']),'test ID provenance')
        ids.extend(g['test_ids']); modules.append(g['module'])
    require(len(ids)==len(set(ids))==s.FULL_TESTS and len(modules)==len(set(modules)) and r.EXCLUDED not in ids
            and groups[-1]['module']==TEST_MODULE and len(groups[-1]['test_ids'])==s.OWN_TESTS,'complete test inventory')
    require(s.digest(ids[:-s.OWN_TESTS])==BASE_IDS_SHA and s.digest(ids)==plan['test_ids_sha256'],'unchanged5946test IDs')


def build_plan(root, head, h):
    p,ph = h; r = ph[1][0]; prior = p.build_plan(root,head,ph)
    own = list(r.flatten(unittest.defaultTestLoader.loadTestsFromName(TEST_MODULE)))
    require(len(own)==spec().OWN_TESTS and all(type(t).__module__==TEST_MODULE for t in own),'actual own loader')
    groups = prior['groups']+[dict(module=TEST_MODULE,test_ids=[t.id() for t in own])]
    plan = dict(schema='fold-c333-regression-plan-v1',commit_sha=head,manifest_sha256=spec().MANIFEST_SHA,
                test_ids_sha256=spec().digest([t for g in groups for t in g['test_ids']]),groups=groups)
    validate_plan(plan,head,r); return plan


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
                    if now>=beat: emit('worker_heartbeat',dict(phase=phase,elapsed_seconds=round(now-start,3))); beat=now+10
                    time.sleep(.2)
                text = live.read()
                if text: sys.stdout.write(text); sys.stdout.flush()
        finally:
            if process.poll() is None: process.kill(); process.wait(timeout=10)
    emit('process_exit',dict(phase=phase,pid=process.pid,decimal=process.returncode,hexadecimal=f'0x{process.returncode & 0xffffffff:08X}'))
    require(process.returncode==0,'C333 '+phase+' failed;no automatic retry'); return process.pid


def module_child(root, folder, head, index, plan_sha):
    guard(root,head); spec().validate_seal(); r = helpers(root)[1][1][0]
    require(sha(folder/'regression-plan.json')==plan_sha,'module plan bytes')
    plan = read(folder/'regression-plan.json'); validate_plan(plan,head,r)
    require(type(index) is int and 0<=index<spec().MODULES,'module index')
    g = plan['groups'][index]; process = dict(pid=os.getpid(),parent_pid=os.getppid())
    marker = dict(index=index,module=g['module'],tests=len(g['test_ids']),**process)
    emit('regression_module_begin',marker); value = r.execute_module(g['module'],g['test_ids'])
    save(folder/f'module-{index:03d}.json',dict(schema='fold-c330-r1-module-v2',commit_sha=head,plan_sha256=plan_sha,
         index=index,module=g['module'],result=value,**process))
    r.check_module(value,g); guard(root,head)
    require(process==dict(pid=os.getpid(),parent_pid=os.getppid()),'module process identity changed')
    emit('regression_module_complete',marker)


def collect_tests(folder, head, plan, r, run_module):
    validate_plan(plan,head,r); save(folder/'regression-plan.json',plan); ph = sha(folder/'regression-plan.json')
    items = []; total = 0; start = time.monotonic()
    for i,g in enumerate(plan['groups']):
        emit('regression_progress',dict(completed=total,total=spec().FULL_TESTS,index=i,module=g['module']))
        launcher = run_module(i,ph); path = folder/f'module-{i:03d}.json'; log = folder/f'module-{i:03d}.log'; row = read(path)
        relation = r.validate_module_evidence(row,g,head,i,ph,launcher,log)
        items.append(dict(index=i,launcher_pid=launcher,pid=row['pid'],parent_pid=row['parent_pid'],relation=relation,
                          exit_code=0,receipt_sha256=sha(path),log_sha256=sha(log)))
        total += row['result']['tests']
    require(total==spec().FULL_TESTS,'all tests executed')
    save(folder/'regression-evidence.json',dict(schema='fold-c333-regression-v1',commit_sha=head,plan_sha256=ph,
         test_ids_sha256=plan['test_ids_sha256'],modules=items))
    save(folder/'regression-result.json',receipt(head,total))
    emit('regression_result',dict(**receipt(head,total),modules=spec().MODULES,seconds=round(time.monotonic()-start,3)))


def verify_tests(folder, head, plan, r):
    validate_plan(plan,head,r); require(spec().blob(read(folder/'regression-plan.json'))==spec().blob(plan),'planned inventory')
    v = read(folder/'regression-evidence.json'); ph = sha(folder/'regression-plan.json')
    require(set(v)=={'schema','commit_sha','plan_sha256','test_ids_sha256','modules'} and v['schema']=='fold-c333-regression-v1'
            and v['commit_sha']==head and v['plan_sha256']==ph and v['test_ids_sha256']==plan['test_ids_sha256']
            and len(v['modules'])==spec().MODULES,'test proof identity')
    ids = []
    for i,(item,g) in enumerate(zip(v['modules'],plan['groups'],strict=True)):
        require(set(item)=={'index','launcher_pid','pid','parent_pid','relation','exit_code','receipt_sha256','log_sha256'}
                and type(item['index']) is int and item['index']==i and type(item['exit_code']) is int and item['exit_code']==0,'completed module')
        path = folder/f'module-{i:03d}.json'; log = folder/f'module-{i:03d}.log'
        require(sha(path)==item['receipt_sha256'] and sha(log)==item['log_sha256'],'module proof bytes')
        row = read(path); relation = r.validate_module_evidence(row,g,head,i,ph,item['launcher_pid'],log)
        require(type(item['pid']) is int and type(item['parent_pid']) is int and row['pid']==item['pid']
                and row['parent_pid']==item['parent_pid'] and relation==item['relation'],'module topology')
        ids.extend(row['result']['success_ids'])
    require(len(ids)==spec().FULL_TESTS and spec().digest(ids)==plan['test_ids_sha256'],'all successful test IDs')
    check_regression(read(folder/'regression-result.json'),head,spec().FULL_TESTS)
    return dict(tests=spec().FULL_TESTS,modules=spec().MODULES,plan_sha256=ph,
                evidence_sha256=sha(folder/'regression-evidence.json'),result_sha256=sha(folder/'regression-result.json'))


def regression_child(root, folder, head):
    guard(root,head); h = helpers(root); plan = build_plan(root,head,h)
    emit('regression_test_ids_sha256',plan['test_ids_sha256'])
    def run_module(i,ph):
        args = command(root,folder,head,'module')+['--module-index',str(i),'--plan-sha256',ph]
        return run_logged(root,args,folder/f'module-{i:03d}.log',plan['groups'][i]['module'])
    collect_tests(folder,head,plan,h[1][1][0],run_module); guard(root,head)


def artifacts(out):
    return [dict(file=n,sha256=sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in spec().OUTPUTS]


def bound_semantics(out, call):
    before = artifacts(out); value = call(); require(artifacts(out)==before,'output changed during reconstruction')
    return value,before


def execute_stages(regression, diagnostic, verify, finalize):
    emit('phase','full_regression_fresh_process_per_module'); tests = regression()
    require(tests['tests']==spec().FULL_TESTS and tests['modules']==spec().MODULES,'verified regression scope')
    emit('phase','saved_paired_gate_localization'); result = diagnostic()
    emit('phase','saved_diagnostic_reconstruction'); checked = verify()
    require(spec().blob(result)==spec().blob(checked),'saved result mismatch')
    emit('phase','final_uncached_input_recheck'); inventory = finalize()
    return result,tests,inventory


def scientific_worker(root, folder, head):
    guard(root,head); s = spec(); s.validate_seal(); h = helpers(root); p,ph = h
    runtime,locks = ph[1][2],ph[1][4]; torch,np = runtime.native_runtime(); api = locks.WinAPI(); start = time.monotonic()
    emit('native_lock_probe',locks.lock_probe(api,folder))
    with locks.LockedHashes(sha,lambda path:locks.ReadLease(path,api),progress=lambda v:emit('hash_progress',v)) as cache:
        parent_result,_,pins,inputs = snapshot(root,h,cache.sha); cx = parent_semantics(root,h,parent_result,inputs)
        out = folder/'science'; out.mkdir(exist_ok=False); files = []; parent_out = root/PARENT_FOLDER/'science'
        emit('registration_check',dict(source_pins=len(pins),protected_inputs=len(inputs),full_tests=s.FULL_TESTS,manifest_sha256=s.MANIFEST_SHA))
        def regression():
            run_logged(root,command(root,folder,head,'regression'),folder/'regression.log','regression'); guard(root,head)
            for lease,_ in cache.entries.values(): lease.check()
            return verify_tests(folder,head,build_plan(root,head,h),ph[1][0])
        def diagnose():
            with cx[-1].guarded.no_neural(): return s.run_diagnostic(out,parent_out,read)
        def verification():
            with cx[-1].guarded.no_neural(): value,bound = bound_semantics(out,lambda:s.semantic_recheck(out,parent_out,read))
            files.extend(bound); return value
        result,tests,inventory = execute_stages(regression,diagnose,verification,cache.recheck)
        require(len(inventory)==s.INPUT_COUNT and {v['path']:v['sha256'] for v in inventory}==inputs,'all final input rereads')
        stats = dict(cache.stats)
    guard(root,head); s.check_summary(result); require(artifacts(out)==files,'final output binding')
    primary = dict(schema='fold-c333-diagnostic-v1',experiment_id=s.EXPERIMENT_ID,stage=s.STAGE,commit_sha=head,status='PASS',
        diagnostic_execution_valid=True,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,
        manifest_sha256=s.MANIFEST_SHA,source_blobs=pins,input_sha256=inputs,artifacts=files,validation_summary=result,
        runtime=dict(python=sys.version.split()[0],torch=str(torch.__version__),numpy=np.__version__,device='cpu',precision='float64',
                     threads=2,worker_seconds=time.monotonic()-start,process_peak_rss_bytes=p.spec().source().base().peak_rss(),peak_vram_bytes=None))
    save(out/'summary.json',primary)
    envelope = dict(schema='fold-c333-execution-envelope-v1',commit_sha=head,scientific_status='PASS',scientific_summary_sha256=sha(out/'summary.json'),
        source_blobs=pins,input_sha256=inputs,source_count=s.SOURCE_COUNT,input_count=s.INPUT_COUNT,
        regression=read(folder/'regression-result.json'),regression_isolation=tests,parent_summary_sha256=PARENT_SUMMARY,
        parent_envelope_sha256=PARENT_ENVELOPE,immediate_parent_semantic_reconstruction=True,parent_regression_reconstructed=True,
        ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,final_reference_rechecks=s.INPUT_COUNT,
        hash_stats=stats,manifest_sha256=s.MANIFEST_SHA,scientific_work=s.WORK)
    save(folder/'execution-envelope.json',envelope)
    emit('summary',str(out/'summary.json')); emit('summary_sha256',envelope['scientific_summary_sha256'])
    emit('preserved_parent_gate',dict(candidate_gate=result['parent_validation_summary']['candidate_gate'],
         eligible_seed_count=result['parent_validation_summary']['eligible_seed_count']))
    for row in result['strata']: emit('C333 stratum',row)
    for row in result['transition_summary']: emit('C333 transition',row)
    emit('execution_envelope',dict(path=str(folder/'execution-envelope.json'),sha256=sha(folder/'execution-envelope.json')))
    emit('persisted_paired_localization','PASS;local_cells=4320;order_cells=2160;new_model_forwards=0')


def verify_outputs(root, folder, head):
    guard(root,head); s = spec(); s.validate_seal(); h = helpers(root); out = folder/'science'
    parent_result,_,pins,inputs = snapshot(root,h,sha); r = read(out/'summary.json'); v = read(folder/'execution-envelope.json')
    require(r['schema']=='fold-c333-diagnostic-v1' and v['schema']=='fold-c333-execution-envelope-v1'
            and r['commit_sha']==v['commit_sha']==head and r['experiment_id']==s.EXPERIMENT_ID and r['stage']==s.STAGE,'child identity')
    s.check_summary(r['validation_summary'])
    require(r['status']==v['scientific_status']=='PASS' and r['diagnostic_execution_valid'] is True
            and r['capability_gate_applicable'] is False and r['gate_f_candidate'] is False and r['production_adoption'] is False,'diagnostic flags')
    require(r['source_blobs']==v['source_blobs']==pins and r['input_sha256']==v['input_sha256']==inputs
            and v['source_count']==s.SOURCE_COUNT and v['input_count']==s.INPUT_COUNT,'complete child maps')
    require(v['parent_summary_sha256']==PARENT_SUMMARY and v['parent_envelope_sha256']==PARENT_ENVELOPE
            and v['immediate_parent_semantic_reconstruction'] is True and v['parent_regression_reconstructed'] is True
            and v['ancestor_semantic_reruns']==0 and v['saved_semantic_reconstruction'] is True
            and v['final_reference_rechecks']==s.INPUT_COUNT and v['hash_stats']['final_reference_rechecks']==s.INPUT_COUNT,'verification completion')
    require(sha(out/'summary.json')==v['scientific_summary_sha256'] and r['manifest_sha256']==v['manifest_sha256']==s.MANIFEST_SHA
            and v['scientific_work']==s.WORK,'work/seal/summary bytes')
    check_regression(v['regression'],head,s.FULL_TESTS)
    require(s.blob(verify_tests(folder,head,build_plan(root,head,h),h[1][1][0]))==s.blob(v['regression_isolation']),'test proof binding')
    h[1][1][3].descriptors(out,r['artifacts'],s.OUTPUTS,sha); cx = parent_semantics(root,h,parent_result,inputs)
    with cx[-1].guarded.no_neural(): checked,_ = bound_semantics(out,lambda:s.semantic_recheck(out,root/PARENT_FOLDER/'science',read))
    require(s.blob(checked)==s.blob(r['validation_summary']),'fresh saved reconstruction')
    guard(root,head); emit('execution_envelope_verified',dict(source_pins=s.SOURCE_COUNT,protected_inputs=s.INPUT_COUNT,full_tests=s.FULL_TESTS,modules=s.MODULES))


def run(root, folder, head):
    guard(root,head); spec().validate_seal(); require(folder.is_relative_to(root/'runs') and folder!=root/'runs','output outside runs')
    folder.mkdir(parents=True,exist_ok=False); valid = False
    emit('execution_role','C333-PAIRED-GATE-LOCALIZATION'); emit('scientific_execution_head',head)
    try:
        run_logged(root,command(root,folder,head,'science'),folder/'science.log','science')
        run_logged(root,command(root,folder,head,'verify'),folder/'verify.log','verify'); valid = True
    finally: guard(root,head); emit('run_execution_valid',valid)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); parser.add_argument('--folder',type=Path,required=True)
    parser.add_argument('--expected-head',required=True); parser.add_argument('--mode',choices=('run','science','regression','module','verify'),default='run')
    parser.add_argument('--module-index',type=int); parser.add_argument('--plan-sha256')
    a = parser.parse_args(); root = a.root.resolve(); folder = a.folder.resolve()
    require(folder.is_relative_to(root/'runs') and folder!=root/'runs','output outside runs')
    if a.mode=='module': module_child(root,folder,a.expected_head,a.module_index,a.plan_sha256)
    else:
        require(a.module_index is None and a.plan_sha256 is None,'module-only arguments')
        {'run':run,'science':scientific_worker,'regression':regression_child,'verify':verify_outputs}[a.mode](root,folder,a.expected_head)


if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).resolve().parents[1])); main()
