"""C326: immutable immediate-parent evidence and native locked execution.

No accepted global is patched. No ancestor training or semantic recursion.
The complete primary result and execution envelope are both mandatory.
"""
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
PARENT_EXECUTION='f95895313da81634976d0ff2761efdd793888c2b'
PARENT_FOLDER='runs/c325-mixed-name-26478978a92c42d2980095d76d6e4339'
PARENT_SUMMARY='e3e9808fea616ecc27e2644f808553f16fb6a11203284bdea5c2cf63b32006e8'
PARENT_ENVELOPE='e40a7e93159cdf33b94b11e8ee8df197da66949d121dd52eb8c6036db99440b9'
E_PATH='tools/c325_execution.py'
P_PATH='fold_lm/v05_benchmarks/model_c325_mixed_name_coverage.py'
BOOTSTRAP={E_PATH:'26dc2a3dcd548fd2c135a10e88ff8bcebe1578ad',P_PATH:'86e6a4b5666d42b805c1e21b34a40acde0088709',
    'fold_lm/v05_benchmarks/model_c324_interior_coverage_training.py':'2fc9e31c7037313a3fadb126af9b153608c0ac6e',
    'tools/c324_locked_hash_r4.py':'6459b1f6e4051fbfc54db2894f7abe3a7521df3a',
    'tools/c324_scientific_recovery_r6.py':'353f54f1bd66117728839049e99b17fc3aee4bf2'}
TEST_MODULE='tests_lm.test_v05_c326_mixing_granularity'


def require(ok,message):
    if not ok: raise ValueError(message)


def spec(): return importlib.import_module('fold_lm.v05_benchmarks.model_c326_mixing_granularity')


def emit(name,value):
    print(name+' = '+json.dumps(value,sort_keys=True,ensure_ascii=True,allow_nan=False),flush=True)


def sha(path):
    with Path(path).open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()


def read(path):
    def unique(pairs):
        out={}
        for k,v in pairs:
            require(k not in out,'duplicate JSON key'); out[k]=v
        return out
    def invalid(value): raise ValueError('nonfinite JSON:'+value)
    return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=unique,parse_constant=invalid)


def save(path,value):
    with Path(path).open('xb') as stream: stream.write(spec().blob(value))


def canonical(path): return os.path.normcase(str(Path(path).resolve(strict=True)))


def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.STDOUT).decode('utf-8').strip()


def active(text):
    m=re.search(r'(?ms)^## Formal state\s+(.*?)(?=^## |\Z)',text)
    return bool(m and re.findall(r'C(\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)',m[1])==['326'])


def guard(root,head):
    require(isinstance(head,str) and re.fullmatch('[0-9a-f]{40}',head),'invalid execution HEAD')
    require(git(root,'branch','--show-current')==BRANCH,'wrong branch')
    require(git(root,'rev-parse','HEAD')==head,'stale HEAD')
    require(not git(root,'status','--porcelain','--untracked-files=no'),'dirty tracked tree')
    require(active((root/'docs/experiment-ledger-and-handoff.md').read_text(encoding='utf-8')),'C326 not ACTIVE')


def source_bytes(path,oid):
    raw=Path(path).read_bytes(); normalized=raw.replace(b'\r\n',b'\n')
    def object_hash(data): return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    require(object_hash(raw)==oid or (raw==normalized.replace(b'\n',b'\r\n') and object_hash(normalized)==oid),'source bytes:'+str(path))
    return raw


def helpers(root):
    for path,oid in BOOTSTRAP.items():
        require(git(root,'rev-parse','HEAD:'+path)==oid,'bootstrap source pin'); source_bytes(root/path,oid)
    loader=importlib.util.spec_from_file_location('_c326_parent_execution',root/E_PATH)
    require(loader is not None and loader.loader is not None,'helper import')
    e=importlib.util.module_from_spec(loader); loader.loader.exec_module(e)
    r4,r6=e.helpers(root)
    return e,r4,r6


def check_regression(row,head,count=None):
    expected=dict(commit_sha=head,tests=spec().FULL_TESTS if count is None else count,failures=0,errors=0,skipped=0,successful=True)
    require(spec().blob(row)==spec().blob(expected),'complete regression receipt required')


def parent_contract(result,envelope,p,e):
    p.validate_seal(); e.check_validation(result['validation_summary'])
    require(result['schema']=='fold-c325-science-v1' and result['experiment_id']==p.EXPERIMENT_ID and result['stage']==p.STAGE
            and result['commit_sha']==PARENT_EXECUTION and result['status']=='FAIL' and result['validation_summary']['candidate_gate'] is False
            and result['diagnostic_execution_valid'] is True and result['gate_f_candidate'] is False and result['production_adoption'] is False,'parent science identity')
    require(envelope['schema']=='fold-c325-execution-envelope-v1' and envelope['commit_sha']==PARENT_EXECUTION
            and envelope['scientific_summary_sha256']==PARENT_SUMMARY and envelope['scientific_status']=='FAIL','parent envelope identity')
    require(envelope['source_count']==len(envelope['source_blobs'])==808 and envelope['input_count']==len(envelope['input_sha256'])==1517
            and result['source_blobs']==envelope['source_blobs'] and result['input_sha256']==envelope['input_sha256'],'parent complete unions')
    require(set(p.OWN)<=set(envelope['source_blobs']) and all(envelope['source_blobs'].get(k)==v for k,v in BOOTSTRAP.items()),'parent direct source pins')
    require(envelope['manifest_sha256']==result['manifest_sha256']==p.MANIFEST_SHA and envelope['scientific_work']==p.WORK,'parent manifest/work')
    require(envelope['parent_summary_sha256']==e.PARENT_SUMMARY and envelope['parent_envelope_sha256']==e.PARENT_ENVELOPE
            and envelope['immediate_parent_semantic_reconstruction'] is True and envelope['ancestor_semantic_reruns']==0
            and envelope['saved_semantic_reconstruction'] is True and envelope['final_reference_rechecks']==1517
            and envelope['hash_stats']['final_reference_rechecks']==1517,'parent completed verification')
    check_regression(envelope['regression'],PARENT_EXECUTION,5546)


def snapshot(root,p,e,cache):
    s=spec(); s.validate_seal(); folder=root/PARENT_FOLDER; out=folder/'science'
    require(not folder.is_symlink() and not out.is_symlink(),'parent directory link')
    require(cache.sha(out/'summary.json')==PARENT_SUMMARY and cache.sha(folder/'execution-envelope.json')==PARENT_ENVELOPE,'accepted parent hashes')
    result=read(out/'summary.json'); envelope=read(folder/'execution-envelope.json'); parent_contract(result,envelope,p,e)
    inputs=dict(envelope['input_sha256'])
    require(len({canonical(k) for k in inputs})==1517 and all(canonical(k)==k for k in inputs),'parent canonical inventory')
    for path,wanted in inputs.items(): require(cache.sha(path)==wanted,'inherited input changed:'+path)
    added=e.descriptors(out,result['artifacts'],p.OUTPUTS,cache.sha)
    added.update({canonical(out/'summary.json'):PARENT_SUMMARY,canonical(folder/'execution-envelope.json'):PARENT_ENVELOPE})
    require(len(added)==10 and not set(added)&set(inputs),'parent output overlap'); inputs.update(added)
    tree=e.tree_blobs(root); pins=dict(envelope['source_blobs'])
    require(all(tree.get(k)==v for k,v in pins.items()),'inherited source changed')
    for name in s.OWN:
        require(name in tree and name not in pins,'new source ownership'); pins[name]=tree[name]
        key=canonical(root/name); require(key not in inputs,'new input overlap'); inputs[key]=cache.sha(root/name)
    require(len(pins)==s.SOURCE_COUNT and len(inputs)==s.INPUT_COUNT,'C326 protection inventory')
    for name,oid in pins.items():
        source_bytes(root/name,oid); require(inputs.get(canonical(root/name))==cache.sha(root/name),'unprotected source input')
    return result,envelope,pins,inputs


def parent_semantics(root,result,p,b,cx):
    out=root/PARENT_FOLDER/'science'
    with cx[-1].guarded.no_neural():
        data=read(out/'dataset.json'); old=read(out/'original-prompts.json'); new=read(out/'interior-prompts.json')
        require(b.digest(data)==b.DATA_SHA and b.digest(old)==b.PROMPTS_SHA and b.digest(new)==b.digest(cx[2].new_prompts(data)),'canonical parent prompts')
        cx[-1].c.p267.validate_data(data); cx[2].check_prompts(data,old,new,cx[3],cx[-1])
        _,summary=p.semantic_recheck(out,data,old,new,cx,read)
        require(p.blob(summary)==p.blob(result['validation_summary']),'parent summary reconstruction')
    emit('accepted_parent_semantics',dict(primary=True,envelope=True,checkpoints=10,model_forwards=0,ancestor_semantic_reruns=0))
    return data,old,new


def suite(root,b,e,r6):
    s=spec(); inherited=list(r6.flatten(e.suite(root,b,r6))); own=list(r6.flatten(unittest.defaultTestLoader.loadTestsFromName(TEST_MODULE)))
    require(len(inherited)==5546 and len(own)==s.OWN_TESTS,'suite component counts')
    tests=inherited+own; ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==s.FULL_TESTS and b.EXCLUDED not in ids,'full suite identities')
    require(len(b.regression_modules(root))+len(r6.RECOVERY_MODULES)+2==s.MODULES,'module inventory')
    return unittest.TestSuite(tests)


def subprocess_run(root,folder,head,mode):
    log=folder/(mode+'.log'); command=[sys.executable,'-B','-X','faulthandler','-u',str(Path(__file__).resolve()),
        '--root',str(root),'--folder',str(folder),'--expected-head',head,'--mode',mode]
    env=dict(os.environ,PYTHONIOENCODING='utf-8'); started=time.monotonic(); beat=started+10
    with log.open('xb') as out:
        proc=subprocess.Popen(command,cwd=root,stdout=out,stderr=subprocess.STDOUT,env=env)
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
    require(proc.returncode==0,'C326 '+mode+' failed; preserve attempt; no automatic retry')


def regression_child(root,folder,head):
    guard(root,head); e,_,r6=helpers(root); b=spec().base(); selected=suite(root,b,e,r6)
    emit('regression_suite',dict(inherited=5546,own=spec().OWN_TESTS,selected=spec().FULL_TESTS,modules=spec().MODULES))
    emit('regression_test_ids_sha256',spec().digest([t.id() for t in r6.flatten(selected)]))
    result=unittest.TextTestRunner(verbosity=1).run(selected)
    receipt=dict(commit_sha=head,tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),successful=result.wasSuccessful())
    save(folder/'regression-result.json',receipt); emit('regression_result',receipt); check_regression(receipt,head); guard(root,head)


def execute_stages(head,preflight,regression,fitting,verification,finalize):
    emit('phase','native_TRAIN_and_gradient_preflight'); preflight()
    emit('phase','full_regression_unmodified_separate_process'); receipt=regression(); check_regression(receipt,head)
    emit('phase','scientific_training_10_models'); summary=fitting()
    emit('phase','saved_checkpoint_and_measurement_verification'); metrics,verified=verification()
    require(spec().blob(summary)==spec().blob(verified),'child saved summary differs')
    emit('phase','final_uncached_input_recheck'); inventory=finalize()
    return summary,metrics,receipt,inventory


def check_contrast(row):
    fields=('answers','query_pairs','control_correct','candidate_correct','control_both_correct','candidate_both_correct',
            'rescued','regressed','pair_rescued','pair_regressed','answer_gain','query_pair_gain')
    require(set(row)==set(fields) and all(type(row[k]) is int for k in fields),'contrast fields')
    require(row['answers']==288 and row['query_pairs']==144 and all(row[k]>=0 for k in fields[:-2]),'contrast bounds')
    require(all(row[k]<=288 for k in ('control_correct','candidate_correct','rescued','regressed')) and
            all(row[k]<=144 for k in ('control_both_correct','candidate_both_correct','pair_rescued','pair_regressed')),'contrast denominator')
    require(row['candidate_correct']-row['control_correct']==row['answer_gain']==row['rescued']-row['regressed'] and
            row['candidate_both_correct']-row['control_both_correct']==row['query_pair_gain']==row['pair_rescued']-row['pair_regressed'],'contrast conservation')


def check_validation(value):
    s=spec(); require([(r['seed'],r['arm']) for r in value['seed_results']]==s.identities(),'saved seed inventory')
    require(all(type(value[k]) is int and value[k]==v for k,v in s.WORK.items()) and value['all_pairs_matched'] is True
            and value['all_replays'] is True and value['all_family_exposures_matched'] is True,'saved work/integrity')
    require([r['seed'] for r in value['paired_comparisons']]==list(s.SEEDS),'paired seed inventory')
    for i,pair in enumerate(value['paired_comparisons']):
        for offset,prefix in ((0,'control'),(1,'candidate')):
            r=value['seed_results'][2*i+offset]
            require(set(r['original_pass'])==set(map(str,range(2,7))) and all(type(v) is bool for v in r['original_pass'].values())
                    and type(r['interior_pass']) is bool and r['retention_pass'] is all(r['original_pass'].values())
                    and pair[prefix+'_retention_pass'] is r['retention_pass'] and pair[prefix+'_interior_pass'] is r['interior_pass'],'saved gate binding')
        old=pair['original_by_length']; inside=pair['interior']; require(set(old)==set(map(str,range(2,7))),'contrast domains')
        for row in [inside,*old.values()]: check_contrast(row)
        require(pair['original_answer_gain']==sum(r['answer_gain'] for r in old.values()) and
                pair['original_pair_gain']==sum(r['query_pair_gain'] for r in old.values()) and
                pair['interior_answer_gain']==inside['answer_gain'] and pair['interior_pair_gain']==inside['query_pair_gain'],'gain binding')
    gate,flags=s.fixed_gate(value['paired_comparisons'])
    require(value['candidate_gate'] is gate and type(value['paired_success_count']) is int and value['paired_success_count']==sum(flags)
            and [r['paired_success'] for r in value['paired_comparisons']]==flags,'composite gate')


def artifact_receipt(out):
    return [dict(file=n,sha256=sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in spec().OUTPUTS]


def bound_semantics(out,call):
    before=artifact_receipt(out); value=call(); require(artifact_receipt(out)==before,'output changed during semantic read')
    return value,before


def native_runtime():
    require(os.name=='nt','native Windows read leases required; no unlocked fallback')
    import torch
    import numpy as np
    require(sys.version_info[:3]==(3,13,15) and str(torch.__version__)=='2.10.0+cu130' and np.__version__=='2.3.5','authoritative runtime mismatch')
    torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    return torch,np


def scientific_worker(root,folder,head):
    started=time.monotonic(); guard(root,head); s=spec(); s.validate_seal()
    e,r4,r6=helpers(root); torch,np=native_runtime()
    api=r4.WinAPI(); emit('native_lock_probe',r4.lock_probe(api,folder)); p=s.previous(); b=s.base()
    with r4.LockedHashes(sha,lambda path:r4.ReadLease(path,api),progress=lambda row:emit('hash_progress',row)) as cache:
        emit('phase','accepted_C325_composite_snapshot'); parent,old_envelope,pins,inputs=snapshot(root,p,e,cache)
        cx=b.context(); b.check_dependencies(root,pins,cx); data,old,new=parent_semantics(root,parent,p,b,cx)
        canonical_data=s.digest((data,old,new)); out=folder/'science'; out.mkdir(exist_ok=False)
        parent_elapsed=time.monotonic()-started; verified_artifacts=[]
        emit('registration_check',dict(source_pins=len(pins),protected_inputs=len(inputs),manifest_sha256=s.MANIFEST_SHA))
        def regression():
            subprocess_run(root,folder,head,'regression'); guard(root,head)
            for lease,_ in cache.entries.values(): lease.check()
            return read(folder/'regression-result.json')
        def verification():
            with cx[-1].guarded.no_neural():
                value,receipt=bound_semantics(out,lambda:s.semantic_recheck(out,data,old,new,cx,read))
            verified_artifacts.extend(receipt); return value
        summary,metrics,receipt,inventory=execute_stages(head,
            lambda:s.runtime_preflight(data,old,new,cx,root,pins),regression,
            lambda:s.run_science(out,data,old,new,cx,root,pins),verification,cache.recheck)
        require(len(inventory)==s.INPUT_COUNT and {r['path']:r['sha256'] for r in inventory}==inputs,'final input inventory')
        require(s.digest((data,old,new))==canonical_data,'canonical data mutated'); hash_stats=dict(cache.stats)
    guard(root,head); check_validation(summary)
    require(artifact_receipt(out)==verified_artifacts,'output changed after semantic verification'); artifacts=verified_artifacts
    result=dict(schema='fold-c326-science-v1',experiment_id=s.EXPERIMENT_ID,stage=s.STAGE,commit_sha=head,
        status='PASS' if summary['candidate_gate'] else 'FAIL',diagnostic_execution_valid=True,source_blobs=pins,input_sha256=inputs,
        artifacts=artifacts,validation_summary=summary,manifest_sha256=s.MANIFEST_SHA,gate_f_candidate=False,production_adoption=False,
        runtime=dict(python=sys.version.split()[0],torch=str(torch.__version__),numpy=np.__version__,device='cpu',precision='float64',threads=2,
            parent_seconds=parent_elapsed,worker_seconds=time.monotonic()-started,process_peak_rss_bytes=b.peak_rss(),peak_vram_bytes=None,
            serialized_artifact_bytes=sum(r['serialized_bytes'] for r in artifacts)))
    save(out/'summary.json',result)
    envelope=dict(schema='fold-c326-execution-envelope-v1',commit_sha=head,source_blobs=pins,input_sha256=inputs,
        scientific_summary_sha256=sha(out/'summary.json'),scientific_status=result['status'],source_count=s.SOURCE_COUNT,input_count=s.INPUT_COUNT,
        regression=receipt,parent_summary_sha256=PARENT_SUMMARY,parent_envelope_sha256=PARENT_ENVELOPE,
        immediate_parent_semantic_reconstruction=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,
        final_reference_rechecks=len(inventory),hash_stats=hash_stats,manifest_sha256=s.MANIFEST_SHA,scientific_work=s.WORK)
    save(folder/'execution-envelope.json',envelope)
    emit('summary',str(out/'summary.json')); emit('summary_sha256',envelope['scientific_summary_sha256'])
    emit('scientific_status',result['status']); emit('candidate_gate',summary['candidate_gate'])
    for row in summary['seed_results']: emit('C326 seed',row)
    for row in summary['paired_comparisons']: emit('C326 pair',row)
    for row in metrics: emit('C326 metrics',e.console_metrics(row))
    emit('execution_envelope',dict(path=str(folder/'execution-envelope.json'),sha256=sha(folder/'execution-envelope.json'),
                                  source_count=s.SOURCE_COUNT,input_count=s.INPUT_COUNT,regression_tests=s.FULL_TESTS))
    emit('persisted_training_evaluation','PASS; checkpoint_replays = 10')


def verify_outputs(root,folder,head):
    guard(root,head); s=spec(); s.validate_seal(); envelope=read(folder/'execution-envelope.json'); out=folder/'science'; result=read(out/'summary.json')
    require(envelope['schema']=='fold-c326-execution-envelope-v1' and result['schema']=='fold-c326-science-v1' and envelope['commit_sha']==result['commit_sha']==head,'child identity')
    require(result['experiment_id']==s.EXPERIMENT_ID and result['stage']==s.STAGE and result['diagnostic_execution_valid'] is True
            and result['gate_f_candidate'] is False and result['production_adoption'] is False,'child flags')
    require(envelope['manifest_sha256']==result['manifest_sha256']==s.MANIFEST_SHA and envelope['scientific_work']==s.WORK,'child manifest/work')
    require(envelope['scientific_summary_sha256']==sha(out/'summary.json'),'saved summary bytes'); check_validation(result['validation_summary']); check_regression(envelope['regression'],head)
    require(result['status']==envelope['scientific_status']==('PASS' if result['validation_summary']['candidate_gate'] else 'FAIL'),'saved status')
    require(envelope['source_count']==len(envelope['source_blobs'])==s.SOURCE_COUNT and envelope['input_count']==len(envelope['input_sha256'])==s.INPUT_COUNT
            and result['source_blobs']==envelope['source_blobs'] and result['input_sha256']==envelope['input_sha256'],'child complete protection')
    require(envelope['parent_summary_sha256']==PARENT_SUMMARY and envelope['parent_envelope_sha256']==PARENT_ENVELOPE and
            envelope['immediate_parent_semantic_reconstruction'] is True and envelope['ancestor_semantic_reruns']==0 and
            envelope['saved_semantic_reconstruction'] is True and envelope['final_reference_rechecks']==s.INPUT_COUNT and
            envelope['hash_stats']['final_reference_rechecks']==s.INPUT_COUNT,'child completion')
    e,_,_=helpers(root); p=s.previous(); parent_out=root/PARENT_FOLDER/'science'
    require(sha(parent_out/'summary.json')==PARENT_SUMMARY and sha(parent_out.parent/'execution-envelope.json')==PARENT_ENVELOPE,'parent evidence changed')
    parent=read(parent_out/'summary.json'); old=read(parent_out.parent/'execution-envelope.json'); parent_contract(parent,old,p,e)
    pins=envelope['source_blobs']; tree=e.tree_blobs(root)
    require(pins=={**old['source_blobs'],**{k:tree[k] for k in s.OWN}} and not set(s.OWN)&set(old['source_blobs']),'source union')
    wanted=dict(old['input_sha256']); wanted.update(e.descriptors(parent_out,parent['artifacts'],p.OUTPUTS,sha))
    wanted.update({canonical(parent_out/'summary.json'):PARENT_SUMMARY,canonical(parent_out.parent/'execution-envelope.json'):PARENT_ENVELOPE})
    wanted.update({canonical(root/k):sha(root/k) for k in s.OWN}); require(wanted==envelope['input_sha256'],'input union')
    for name,oid in pins.items(): require(tree.get(name)==oid,'source tree changed'); source_bytes(root/name,oid)
    for name,value in wanted.items(): require(sha(name)==value,'input changed:'+name)
    e.descriptors(out,result['artifacts'],s.OUTPUTS,sha); guard(root,head)
    emit('execution_envelope_verified',dict(source_pins=s.SOURCE_COUNT,protected_inputs=s.INPUT_COUNT,full_tests=s.FULL_TESTS))


def run(root,folder,head):
    guard(root,head); require(folder.is_relative_to(root/'runs') and folder!=root/'runs','output outside runs')
    folder.mkdir(parents=True,exist_ok=False); complete=False; emit('execution_role','C326-MIXING-GRANULARITY'); emit('scientific_execution_head',head)
    try:
        subprocess_run(root,folder,head,'science'); subprocess_run(root,folder,head,'verify'); complete=True
    finally:
        guard(root,head); emit('run_execution_valid',complete)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); parser.add_argument('--folder',type=Path,required=True)
    parser.add_argument('--expected-head',required=True); parser.add_argument('--mode',choices=('run','science','regression','verify'),default='run')
    args=parser.parse_args(); root=args.root.resolve(); folder=args.folder.resolve()
    require(folder.is_relative_to(root/'runs') and folder!=root/'runs','output outside runs')
    {'run':run,'science':scientific_worker,'regression':regression_child,'verify':verify_outputs}[args.mode](root,folder,args.expected_head)


if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).resolve().parents[1])); main()
