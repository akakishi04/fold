"""C328 native execution: exact C327 diagnostic parent and immutable C326 training data."""
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

BRANCH='feat/sft-target-loss'
PARENT_EXECUTION='847c924f50303d93ed4df7acec74b77209b7d261'
PARENT_FOLDER='runs/c327-gradient-1cf048a0cd9449b6af6485a4802c46ca'
PARENT_SUMMARY='c4a061e158a1bd617fb7638bb034b7aa3ef78da06b15062474ff986d1f347719'
PARENT_ENVELOPE='fb44749ce38e0b0909238c51c13bbb1eb95e1898369313fb34d95483a543e535'
E_PATH='tools/c327_execution.py'
P_PATH='fold_lm/v05_benchmarks/model_c327_gradient_alignment.py'
BOOTSTRAP={E_PATH:'d329092835a15f6d89b77640da9cb8b842050ae2',P_PATH:'889cfce9a4a8108557ec5868a7626b431719359c',
    'fold_lm/v05_benchmarks/model_c308_core_learning_rate.py':'f4e41f0d37b1aa5cbba536e5da984ab556eea2c5'}
TEST_MODULE='tests_lm.test_v05_c328_late_rate_decay'


def require(ok,message):
    if not ok: raise ValueError(message)


def spec(): return importlib.import_module('fold_lm.v05_benchmarks.model_c328_late_rate_decay')


def parent(): return importlib.import_module('fold_lm.v05_benchmarks.model_c327_gradient_alignment')


def emit(name,value): print(name+' = '+json.dumps(value,sort_keys=True,ensure_ascii=True,allow_nan=False),flush=True)


def sha(path):
    with Path(path).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()


def read(path):
    def unique(pairs):
        result={}
        for k,v in pairs:
            require(k not in result,'duplicate JSON key'); result[k]=v
        return result
    def invalid(v): raise ValueError('nonfinite JSON:'+v)
    return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=unique,parse_constant=invalid)


def save(path,value):
    with Path(path).open('xb') as f: f.write(spec().blob(value))


def canonical(path): return os.path.normcase(str(Path(path).resolve(strict=True)))


def git(root,*args): return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.STDOUT).decode('utf-8').strip()


def active(text):
    m=re.search(r'(?ms)^## Formal state\s+(.*?)(?=^## |\Z)',text)
    return bool(m and re.findall(r'C(\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)',m[1])==['328'])


def guard(root,head):
    require(isinstance(head,str) and re.fullmatch('[0-9a-f]{40}',head),'invalid HEAD')
    require(git(root,'branch','--show-current')==BRANCH and git(root,'rev-parse','HEAD')==head,'branch/HEAD mismatch')
    require(not git(root,'status','--porcelain','--untracked-files=no'),'dirty tracked tree')
    require(active((root/'docs/experiment-ledger-and-handoff.md').read_text(encoding='utf-8')),'C328 not uniquely ACTIVE')


def source_bytes(path,oid):
    raw=Path(path).read_bytes(); norm=raw.replace(b'\r\n',b'\n')
    def h(v): return hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest()
    require(h(raw)==oid or (raw==norm.replace(b'\n',b'\r\n') and h(norm)==oid),'source byte identity')
    return raw


def helpers(root):
    for name,oid in BOOTSTRAP.items():
        require(git(root,'rev-parse','HEAD:'+name)==oid,'bootstrap pin'); source_bytes(root/name,oid)
    loader=importlib.util.spec_from_file_location('_c328_parent_executor',root/E_PATH)
    require(loader is not None and loader.loader is not None,'parent executor loader')
    e=importlib.util.module_from_spec(loader); loader.loader.exec_module(e)
    e326,legacy,r4,r6=e.helpers(root)
    return e,e326,legacy,r4,r6


def check_regression(value,head,count=None):
    expected=dict(commit_sha=head,tests=spec().FULL_TESTS if count is None else count,failures=0,errors=0,skipped=0,successful=True)
    require(spec().blob(value)==spec().blob(expected),'complete regression receipt')


def parent_contract(result,envelope,p,e):
    p.validate_seal(); e.check_validation(result['validation_summary'])
    require(result['schema']=='fold-c327-diagnostic-v1' and result['experiment_id']==p.EXPERIMENT_ID and result['stage']==p.STAGE and result['commit_sha']==PARENT_EXECUTION and result['status']=='PASS','parent diagnostic identity')
    require(result['diagnostic_execution_valid'] is True and result['capability_gate_applicable'] is False and result['gate_f_candidate'] is False and result['production_adoption'] is False,'parent diagnostic flags')
    require(envelope['schema']=='fold-c327-execution-envelope-v1' and envelope['commit_sha']==PARENT_EXECUTION and envelope['scientific_summary_sha256']==PARENT_SUMMARY and envelope['scientific_status']=='PASS','parent envelope identity')
    require(envelope['source_count']==len(envelope['source_blobs'])==820 and envelope['input_count']==len(envelope['input_sha256'])==1549 and result['source_blobs']==envelope['source_blobs'] and result['input_sha256']==envelope['input_sha256'],'parent complete unions')
    require(set(p.OWN)<=set(envelope['source_blobs']) and all(envelope['source_blobs'].get(k)==v for k,v in {**e.BOOTSTRAP,**BOOTSTRAP}.items()),'parent direct pins')
    require(result['manifest_sha256']==envelope['manifest_sha256']==p.MANIFEST_SHA and envelope['scientific_work']==p.WORK,'parent manifest/work')
    require(envelope['parent_summary_sha256']==e.PARENT_SUMMARY and envelope['parent_envelope_sha256']==e.PARENT_ENVELOPE and envelope['immediate_parent_semantic_reconstruction'] is True and envelope['ancestor_semantic_reruns']==0 and envelope['saved_semantic_reconstruction'] is True and envelope['final_reference_rechecks']==1549 and envelope['hash_stats']['final_reference_rechecks']==1549,'parent verification completion')
    check_regression(envelope['regression'],PARENT_EXECUTION,5658)


def snapshot(root,p,e,legacy,cache):
    s=spec(); s.validate_seal(); folder=root/PARENT_FOLDER; out=folder/'science'
    require(not folder.is_symlink() and not out.is_symlink(),'parent path link')
    require(cache.sha(out/'summary.json')==PARENT_SUMMARY and cache.sha(folder/'execution-envelope.json')==PARENT_ENVELOPE,'fixed parent hashes')
    result=read(out/'summary.json'); envelope=read(folder/'execution-envelope.json'); parent_contract(result,envelope,p,e)
    inputs=dict(envelope['input_sha256']); require(len({canonical(k) for k in inputs})==1549 and all(canonical(k)==k for k in inputs),'canonical parent inventory')
    for name,wanted in inputs.items(): require(cache.sha(name)==wanted,'inherited input changed:'+name)
    added=legacy.descriptors(out,result['artifacts'],p.OUTPUTS,cache.sha)
    added.update({canonical(out/'summary.json'):PARENT_SUMMARY,canonical(folder/'execution-envelope.json'):PARENT_ENVELOPE})
    require(len(added)==6 and not set(added)&set(inputs),'six diagnostic parent files'); inputs.update(added)
    tree=legacy.tree_blobs(root); pins=dict(envelope['source_blobs']); require(all(tree.get(k)==v for k,v in pins.items()),'inherited source changed')
    for name in s.OWN:
        require(name in tree and name not in pins,'new source ownership'); pins[name]=tree[name]
        key=canonical(root/name); require(key not in inputs,'new input overlap'); inputs[key]=cache.sha(root/name)
    require(len(pins)==s.SOURCE_COUNT and len(inputs)==s.INPUT_COUNT,'C328 protection count')
    for name,oid in pins.items(): source_bytes(root/name,oid); require(inputs.get(canonical(root/name))==cache.sha(root/name),'source input binding')
    return result,envelope,pins,inputs


def parent_semantics(root,result,p,e,b,cx,inputs):
    out=root/PARENT_FOLDER/'science'; ancestor=root/e.PARENT_FOLDER/'science'
    for name in ('summary.json','dataset.json','original-prompts.json','interior-prompts.json','evaluations.pt'):
        require(canonical(ancestor/name) in inputs,'unprotected C326 semantic dependency')
    require(inputs[canonical(ancestor/'summary.json')]==e.PARENT_SUMMARY and sha(ancestor/'summary.json')==e.PARENT_SUMMARY,'C326 evidence identity')
    with cx[-1].guarded.no_neural():
        data=read(ancestor/'dataset.json'); old=read(ancestor/'original-prompts.json'); new=read(ancestor/'interior-prompts.json')
        require(b.digest(data)==b.DATA_SHA and b.digest(old)==b.PROMPTS_SHA and b.digest(new)==b.digest(cx[2].new_prompts(data)),'canonical data')
        cx[-1].c.p267.validate_data(data); cx[2].check_prompts(data,old,new,cx[3],cx[-1])
        _,summary=p.semantic_recheck(out,ancestor,data,read)
        require(p.blob(summary)==p.blob(result['validation_summary']),'C327 persisted diagnostic reconstruction')
    emit('accepted_parent_semantics',dict(diagnostic_parent=True,parent_files=6,gradient_pairs=60,model_forwards=0,ancestor_semantic_reruns=0))
    return data,old,new


def suite(root,b,e,e326,legacy,r6):
    inherited=list(r6.flatten(e.suite(root,b,e326,legacy,r6))); own=list(r6.flatten(unittest.defaultTestLoader.loadTestsFromName(TEST_MODULE)))
    require(len(inherited)==5658 and len(own)==spec().OWN_TESTS,'suite components')
    tests=inherited+own; ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==spec().FULL_TESTS and b.EXCLUDED not in ids,'full distinct suite')
    require(len(b.regression_modules(root))+len(r6.RECOVERY_MODULES)+4==spec().MODULES,'module inventory')
    return unittest.TestSuite(tests)


def subprocess_run(root,folder,head,mode):
    log=folder/(mode+'.log'); command=[sys.executable,'-B','-X','faulthandler','-u',str(Path(__file__).resolve()),'--root',str(root),'--folder',str(folder),'--expected-head',head,'--mode',mode]
    started=time.monotonic(); beat=started+10
    with log.open('xb') as out:
        proc=subprocess.Popen(command,cwd=root,stdout=out,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
        try:
            with log.open('r',encoding='utf-8',errors='backslashreplace') as live:
                while proc.poll() is None:
                    text=live.read()
                    if text: sys.stdout.write(text); sys.stdout.flush()
                    now=time.monotonic()
                    if now>=beat: emit('worker_heartbeat',dict(phase=mode,elapsed_seconds=round(now-started,3))); beat=now+10
                    time.sleep(.2)
                text=live.read()
                if text: sys.stdout.write(text); sys.stdout.flush()
        finally:
            if proc.poll() is None: proc.kill(); proc.wait(timeout=10)
    emit('process_exit',dict(phase=mode,decimal=proc.returncode,hexadecimal=f'0x{proc.returncode & 0xffffffff:08X}',log=str(log)))
    require(proc.returncode==0,'C328 '+mode+' failed; no automatic retry')


def regression_child(root,folder,head):
    guard(root,head); e,e326,legacy,_,r6=helpers(root); selected=suite(root,spec().base(),e,e326,legacy,r6)
    emit('regression_suite',dict(inherited=5658,own=spec().OWN_TESTS,selected=spec().FULL_TESTS,modules=spec().MODULES))
    emit('regression_test_ids_sha256',spec().digest([t.id() for t in r6.flatten(selected)]))
    result=unittest.TextTestRunner(verbosity=1).run(selected)
    receipt=dict(commit_sha=head,tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),successful=result.wasSuccessful())
    save(folder/'regression-result.json',receipt); emit('regression_result',receipt); check_regression(receipt,head); guard(root,head)


def check_contrast(row):
    fields=('answers','query_pairs','control_correct','candidate_correct','control_both_correct','candidate_both_correct','rescued','regressed','pair_rescued','pair_regressed','answer_gain','query_pair_gain')
    require(set(row)==set(fields) and all(type(row[k]) is int for k in fields),'contrast fields')
    require(row['answers']==288 and row['query_pairs']==144 and all(row[k]>=0 for k in fields[:-2]),'contrast bounds')
    require(all(row[k]<=288 for k in ('control_correct','candidate_correct','rescued','regressed')) and all(row[k]<=144 for k in ('control_both_correct','candidate_both_correct','pair_rescued','pair_regressed')),'contrast denominators')
    require(row['candidate_correct']-row['control_correct']==row['answer_gain']==row['rescued']-row['regressed'] and row['candidate_both_correct']-row['control_both_correct']==row['query_pair_gain']==row['pair_rescued']-row['pair_regressed'],'contrast conservation')


def check_validation(v):
    s=spec(); require([(r['seed'],r['arm']) for r in v['seed_results']]==s.identities(),'saved cohort')
    require(all(type(v[k]) is int and v[k]==value for k,value in s.WORK.items()) and all(v[k] is True for k in ('all_pairs_matched','all_replays','all_first800_matched')),'saved integrity/work')
    require([r['seed'] for r in v['paired_comparisons']]==list(s.SEEDS),'paired inventory')
    for i,pair in enumerate(v['paired_comparisons']):
        require(pair['first800_matched'] is True,'paired common prefix')
        for offset,prefix in ((0,'control'),(1,'candidate')):
            r=v['seed_results'][2*i+offset]
            require(set(r['original_pass'])==set(map(str,range(2,7))) and all(type(z) is bool for z in r['original_pass'].values()) and type(r['interior_pass']) is bool and r['retention_pass'] is all(r['original_pass'].values()) and pair[prefix+'_retention_pass'] is r['retention_pass'] and pair[prefix+'_interior_pass'] is r['interior_pass'],'gate binding')
        old=pair['original_by_length']; inside=pair['interior']; require(set(old)==set(map(str,range(2,7))),'contrast domains')
        for row in [inside,*old.values()]: check_contrast(row)
        require(pair['original_answer_gain']==sum(r['answer_gain'] for r in old.values()) and pair['original_pair_gain']==sum(r['query_pair_gain'] for r in old.values()) and pair['interior_answer_gain']==inside['answer_gain'] and pair['interior_pair_gain']==inside['query_pair_gain'],'gain binding')
    gate,flags=s.fixed_gate(v['paired_comparisons']); require(v['candidate_gate'] is gate and type(v['paired_success_count']) is int and v['paired_success_count']==sum(flags) and [r['paired_success'] for r in v['paired_comparisons']]==flags,'fixed gate')


def artifacts(out): return [dict(file=n,sha256=sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in spec().OUTPUTS]


def bound_semantics(out,call):
    before=artifacts(out); value=call(); require(artifacts(out)==before,'output changed during semantic read'); return value,before


def execute_stages(head,preflight,regression,fit,verify,finalize):
    emit('phase','native_TRAIN_and_schedule_preflight'); preflight()
    emit('phase','full_regression_unmodified_separate_process'); receipt=regression(); check_regression(receipt,head)
    emit('phase','scientific_training_10_models'); value=fit()
    emit('phase','saved_training_reconstruction'); metrics,verified=verify(); require(spec().blob(value)==spec().blob(verified),'saved result mismatch')
    emit('phase','final_uncached_input_recheck'); inventory=finalize()
    return value,metrics,receipt,inventory


def scientific_worker(root,folder,head):
    started=time.monotonic(); guard(root,head); s=spec(); s.validate_seal(); e,e326,legacy,r4,_=helpers(root)
    torch,np=e326.native_runtime(); api=r4.WinAPI(); emit('native_lock_probe',r4.lock_probe(api,folder)); p=parent(); b=s.base()
    with r4.LockedHashes(sha,lambda path:r4.ReadLease(path,api),progress=lambda r:emit('hash_progress',r)) as cache:
        emit('phase','accepted_C327_composite_snapshot'); result,old_envelope,pins,inputs=snapshot(root,p,e,legacy,cache)
        cx=b.context(); b.check_dependencies(root,pins,cx); data,old,new=parent_semantics(root,result,p,e,b,cx,inputs)
        fp=s.digest((data,old,new)); out=folder/'science'; out.mkdir(exist_ok=False); verified_artifacts=[]
        emit('registration_check',dict(source_pins=len(pins),protected_inputs=len(inputs),manifest_sha256=s.MANIFEST_SHA))
        def regression():
            subprocess_run(root,folder,head,'regression'); guard(root,head)
            for lease,_ in cache.entries.values(): lease.check()
            return read(folder/'regression-result.json')
        def verification():
            with cx[-1].guarded.no_neural(): value,receipt=bound_semantics(out,lambda:s.semantic_recheck(out,data,old,new,cx,read))
            verified_artifacts.extend(receipt); return value
        value,metrics,receipt,inventory=execute_stages(head,lambda:s.runtime_preflight(data,old,new,cx,root,pins),regression,lambda:s.run_science(out,data,old,new,cx,root,pins),verification,cache.recheck)
        require(s.digest((data,old,new))==fp,'parent data mutated')
        require(len(inventory)==s.INPUT_COUNT and {r['path']:r['sha256'] for r in inventory}==inputs,'full final inventory'); stats=dict(cache.stats)
    guard(root,head); check_validation(value); require(artifacts(out)==verified_artifacts,'post-verification output change')
    result=dict(schema='fold-c328-science-v1',experiment_id=s.EXPERIMENT_ID,stage=s.STAGE,commit_sha=head,status='PASS' if value['candidate_gate'] else 'FAIL',diagnostic_execution_valid=True,gate_f_candidate=False,production_adoption=False,source_blobs=pins,input_sha256=inputs,artifacts=verified_artifacts,validation_summary=value,manifest_sha256=s.MANIFEST_SHA,
        runtime=dict(python=sys.version.split()[0],torch=str(torch.__version__),numpy=np.__version__,device='cpu',precision='float64',threads=2,worker_seconds=time.monotonic()-started,process_peak_rss_bytes=b.peak_rss(),peak_vram_bytes=None,serialized_artifact_bytes=sum(r['serialized_bytes'] for r in verified_artifacts)))
    save(out/'summary.json',result)
    envelope=dict(schema='fold-c328-execution-envelope-v1',commit_sha=head,source_blobs=pins,input_sha256=inputs,source_count=s.SOURCE_COUNT,input_count=s.INPUT_COUNT,scientific_summary_sha256=sha(out/'summary.json'),scientific_status=result['status'],regression=receipt,parent_summary_sha256=PARENT_SUMMARY,parent_envelope_sha256=PARENT_ENVELOPE,immediate_parent_semantic_reconstruction=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,final_reference_rechecks=len(inventory),hash_stats=stats,manifest_sha256=s.MANIFEST_SHA,scientific_work=s.WORK)
    save(folder/'execution-envelope.json',envelope); emit('summary',str(out/'summary.json')); emit('summary_sha256',envelope['scientific_summary_sha256']); emit('scientific_status',result['status'])
    for row in value['seed_results']: emit('C328 seed',row)
    for row in value['paired_comparisons']: emit('C328 pair',row)
    for row in metrics: emit('C328 metrics',legacy.console_metrics(row))
    emit('execution_envelope',dict(path=str(folder/'execution-envelope.json'),sha256=sha(folder/'execution-envelope.json'),source_pins=s.SOURCE_COUNT,protected_inputs=s.INPUT_COUNT,regression_tests=s.FULL_TESTS))
    emit('persisted_training_evaluation','PASS; checkpoint_replays=10; first800_matched_pairs=5')


def verify_outputs(root,folder,head):
    guard(root,head); s=spec(); s.validate_seal(); out=folder/'science'; r=read(out/'summary.json'); v=read(folder/'execution-envelope.json')
    require(r['schema']=='fold-c328-science-v1' and v['schema']=='fold-c328-execution-envelope-v1' and r['commit_sha']==v['commit_sha']==head and r['experiment_id']==s.EXPERIMENT_ID and r['stage']==s.STAGE,'child identity')
    require(r['diagnostic_execution_valid'] is True and r['gate_f_candidate'] is False and r['production_adoption'] is False,'child flags')
    require(r['manifest_sha256']==v['manifest_sha256']==s.MANIFEST_SHA and v['scientific_work']==s.WORK and sha(out/'summary.json')==v['scientific_summary_sha256'],'manifest/work/bytes')
    check_validation(r['validation_summary']); check_regression(v['regression'],head)
    require(r['status']==v['scientific_status']==('PASS' if r['validation_summary']['candidate_gate'] else 'FAIL'),'scientific status')
    require(v['source_count']==len(v['source_blobs'])==s.SOURCE_COUNT and v['input_count']==len(v['input_sha256'])==s.INPUT_COUNT and r['source_blobs']==v['source_blobs'] and r['input_sha256']==v['input_sha256'],'child complete union')
    require(v['parent_summary_sha256']==PARENT_SUMMARY and v['parent_envelope_sha256']==PARENT_ENVELOPE and v['immediate_parent_semantic_reconstruction'] is True and v['ancestor_semantic_reruns']==0 and v['saved_semantic_reconstruction'] is True and v['final_reference_rechecks']==s.INPUT_COUNT and v['hash_stats']['final_reference_rechecks']==s.INPUT_COUNT,'complete verification')
    e,_,legacy,_,_=helpers(root); p=parent(); po=root/PARENT_FOLDER/'science'
    require(sha(po/'summary.json')==PARENT_SUMMARY and sha(po.parent/'execution-envelope.json')==PARENT_ENVELOPE,'parent fixed bytes')
    pr=read(po/'summary.json'); pe=read(po.parent/'execution-envelope.json'); parent_contract(pr,pe,p,e); tree=legacy.tree_blobs(root); pins=v['source_blobs']
    require(pins=={**pe['source_blobs'],**{k:tree[k] for k in s.OWN}} and not set(s.OWN)&set(pe['source_blobs']),'source union')
    wanted=dict(pe['input_sha256']); wanted.update(legacy.descriptors(po,pr['artifacts'],p.OUTPUTS,sha)); wanted.update({canonical(po/'summary.json'):PARENT_SUMMARY,canonical(po.parent/'execution-envelope.json'):PARENT_ENVELOPE}); wanted.update({canonical(root/k):sha(root/k) for k in s.OWN})
    require(wanted==v['input_sha256'],'input union')
    for name,oid in pins.items(): require(tree.get(name)==oid,'source changed'); source_bytes(root/name,oid)
    for name,h in wanted.items(): require(sha(name)==h,'input changed:'+name)
    legacy.descriptors(out,r['artifacts'],s.OUTPUTS,sha); guard(root,head); emit('execution_envelope_verified',dict(source_pins=s.SOURCE_COUNT,protected_inputs=s.INPUT_COUNT,full_tests=s.FULL_TESTS))


def run(root,folder,head):
    guard(root,head); require(folder.is_relative_to(root/'runs') and folder!=root/'runs','output outside runs'); folder.mkdir(parents=True,exist_ok=False); complete=False
    emit('execution_role','C328-LATE-RATE-DECAY'); emit('scientific_execution_head',head)
    try: subprocess_run(root,folder,head,'science'); subprocess_run(root,folder,head,'verify'); complete=True
    finally: guard(root,head); emit('run_execution_valid',complete)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); parser.add_argument('--folder',type=Path,required=True); parser.add_argument('--expected-head',required=True); parser.add_argument('--mode',choices=('run','science','regression','verify'),default='run')
    a=parser.parse_args(); root=a.root.resolve(); folder=a.folder.resolve(); require(folder.is_relative_to(root/'runs') and folder!=root/'runs','output outside runs')
    {'run':run,'science':scientific_worker,'regression':regression_child,'verify':verify_outputs}[a.mode](root,folder,a.expected_head)


if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).resolve().parents[1])); main()
