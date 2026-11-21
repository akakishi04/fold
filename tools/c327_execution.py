"""C327 locked diagnostic orchestration; accepted code is reused, never patched."""
from __future__ import annotations
import argparse
import hashlib
import importlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import unittest

BRANCH='feat/sft-target-loss'
PARENT_EXECUTION='dbef3dbc1566ff2c8c30405e9c8d207f5e79f460'
PARENT_FOLDER='runs/c326-mixing-bbd9cd8f43db45f18b2370f2c3337dfa'
PARENT_SUMMARY='0dd7af1c69774f5d00b1ee654284c38731f4233b2b858aedcf1bf0aaa77656aa'
PARENT_ENVELOPE='d379e907d3d9668f47b9690cb097398005b6c0c6c349ac30082ac3590d7dc62a'
E_PATH='tools/c326_execution.py'
P_PATH='fold_lm/v05_benchmarks/model_c326_mixing_granularity.py'
BOOTSTRAP={E_PATH:'e4808721464a20e87f08e16b4f47a7c88ca40ad0',P_PATH:'1090c13372720abf9ec2a14941bbce34f436df98'}
TEST_MODULE='tests_lm.test_v05_c327_gradient_alignment'


def require(ok,message):
    if not ok: raise ValueError(message)


def spec(): return importlib.import_module('fold_lm.v05_benchmarks.model_c327_gradient_alignment')


def emit(name,value): print(name+' = '+json.dumps(value,sort_keys=True,ensure_ascii=True,allow_nan=False),flush=True)


def sha(path):
    with Path(path).open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()


def read(path):
    def unique(pairs):
        out={}
        for k,v in pairs:
            require(k not in out,'duplicate JSON key'); out[k]=v
        return out
    def invalid(v): raise ValueError('nonfinite JSON:'+v)
    return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=unique,parse_constant=invalid)


def save(path,value):
    with Path(path).open('xb') as stream: stream.write(spec().blob(value))


def canonical(path): return os.path.normcase(str(Path(path).resolve(strict=True)))


def git(root,*args): return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.STDOUT).decode('utf-8').strip()


def active(text):
    m=re.search(r'(?ms)^## Formal state\s+(.*?)(?=^## |\Z)',text)
    return bool(m and re.findall(r'C(\d{3}) ACTIVE / (?:NOT YET JUDGED|INVALID ATTEMPT RECOVERY)',m[1])==['327'])


def guard(root,head):
    require(isinstance(head,str) and re.fullmatch('[0-9a-f]{40}',head),'invalid HEAD')
    require(git(root,'branch','--show-current')==BRANCH and git(root,'rev-parse','HEAD')==head,'branch/HEAD mismatch')
    require(not git(root,'status','--porcelain','--untracked-files=no'),'dirty tracked tree')
    require(active((root/'docs/experiment-ledger-and-handoff.md').read_text(encoding='utf-8')),'C327 not uniquely ACTIVE')


def source_bytes(path,oid):
    raw=Path(path).read_bytes(); normalized=raw.replace(b'\r\n',b'\n')
    def h(v): return hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest()
    require(h(raw)==oid or (raw==normalized.replace(b'\n',b'\r\n') and h(normalized)==oid),'source byte identity')
    return raw


def helpers(root):
    for name,oid in BOOTSTRAP.items():
        require(git(root,'rev-parse','HEAD:'+name)==oid,'bootstrap pin'); source_bytes(root/name,oid)
    loader=importlib.util.spec_from_file_location('_c327_parent_executor',root/E_PATH)
    require(loader is not None and loader.loader is not None,'helper loader')
    e=importlib.util.module_from_spec(loader); loader.loader.exec_module(e)
    e325,r4,r6=e.helpers(root)
    return e,e325,r4,r6


def check_regression(value,head,count=None):
    wanted=dict(commit_sha=head,tests=spec().FULL_TESTS if count is None else count,failures=0,errors=0,skipped=0,successful=True)
    require(spec().blob(value)==spec().blob(wanted),'complete regression receipt')


def parent_contract(result,envelope,p,e):
    p.validate_seal(); e.check_validation(result['validation_summary'])
    require(result['schema']=='fold-c326-science-v1' and result['experiment_id']==p.EXPERIMENT_ID and result['stage']==p.STAGE
            and result['commit_sha']==PARENT_EXECUTION and result['status']=='FAIL' and result['validation_summary']['candidate_gate'] is False
            and result['diagnostic_execution_valid'] is True and result['gate_f_candidate'] is False and result['production_adoption'] is False,'parent science identity')
    require(envelope['schema']=='fold-c326-execution-envelope-v1' and envelope['commit_sha']==PARENT_EXECUTION and
            envelope['scientific_summary_sha256']==PARENT_SUMMARY and envelope['scientific_status']=='FAIL','parent envelope identity')
    require(envelope['source_count']==len(envelope['source_blobs'])==814 and envelope['input_count']==len(envelope['input_sha256'])==1533
            and result['source_blobs']==envelope['source_blobs'] and result['input_sha256']==envelope['input_sha256'],'parent complete union')
    require(set(p.OWN)<=set(envelope['source_blobs']) and all(envelope['source_blobs'].get(k)==v for k,v in {**e.BOOTSTRAP,**BOOTSTRAP}.items()),'parent direct pins')
    require(envelope['manifest_sha256']==result['manifest_sha256']==p.MANIFEST_SHA and envelope['scientific_work']==p.WORK,'parent manifest/work')
    require(envelope['parent_summary_sha256']==e.PARENT_SUMMARY and envelope['parent_envelope_sha256']==e.PARENT_ENVELOPE and
            envelope['immediate_parent_semantic_reconstruction'] is True and envelope['ancestor_semantic_reruns']==0 and
            envelope['saved_semantic_reconstruction'] is True and envelope['final_reference_rechecks']==1533 and
            envelope['hash_stats']['final_reference_rechecks']==1533,'parent completion')
    check_regression(envelope['regression'],PARENT_EXECUTION,5610)


def snapshot(root,p,e,legacy,cache):
    s=spec(); s.validate_seal(); folder=root/PARENT_FOLDER; out=folder/'science'
    require(not folder.is_symlink() and not out.is_symlink(),'parent directory link')
    require(cache.sha(out/'summary.json')==PARENT_SUMMARY and cache.sha(folder/'execution-envelope.json')==PARENT_ENVELOPE,'parent hashes')
    result=read(out/'summary.json'); envelope=read(folder/'execution-envelope.json'); parent_contract(result,envelope,p,e)
    inputs=dict(envelope['input_sha256'])
    require(len({canonical(k) for k in inputs})==1533 and all(canonical(k)==k for k in inputs),'canonical inherited inputs')
    for name,wanted in inputs.items(): require(cache.sha(name)==wanted,'changed parent input:'+name)
    added=legacy.descriptors(out,result['artifacts'],p.OUTPUTS,cache.sha)
    added.update({canonical(out/'summary.json'):PARENT_SUMMARY,canonical(folder/'execution-envelope.json'):PARENT_ENVELOPE})
    require(len(added)==10 and not set(added)&set(inputs),'parent output overlap'); inputs.update(added)
    tree=legacy.tree_blobs(root); pins=dict(envelope['source_blobs'])
    require(all(tree.get(k)==v for k,v in pins.items()),'parent source changed')
    for name in s.OWN:
        require(name in tree and name not in pins,'new source ownership'); pins[name]=tree[name]
        key=canonical(root/name); require(key not in inputs,'new input overlap'); inputs[key]=cache.sha(root/name)
    require(len(pins)==s.SOURCE_COUNT and len(inputs)==s.INPUT_COUNT,'new complete inventory')
    for name,oid in pins.items():
        source_bytes(root/name,oid); require(inputs.get(canonical(root/name))==cache.sha(root/name),'source/input binding')
    return result,envelope,pins,inputs


def parent_semantics(root,result,p,b,cx):
    out=root/PARENT_FOLDER/'science'
    with cx[-1].guarded.no_neural():
        data=read(out/'dataset.json'); old=read(out/'original-prompts.json'); new=read(out/'interior-prompts.json')
        require(b.digest(data)==b.DATA_SHA and b.digest(old)==b.PROMPTS_SHA and b.digest(new)==b.digest(cx[2].new_prompts(data)),'canonical parent data')
        cx[-1].c.p267.validate_data(data); cx[2].check_prompts(data,old,new,cx[3],cx[-1])
        _,summary=p.semantic_recheck(out,data,old,new,cx,read)
        require(p.blob(summary)==p.blob(result['validation_summary']),'parent semantic summary')
    emit('accepted_parent_semantics',dict(primary=True,envelope=True,checkpoints=10,model_forwards=0,ancestor_semantic_reruns=0))
    return data,old,new


def suite(root,b,e,legacy,r6):
    inherited=list(r6.flatten(e.suite(root,b,legacy,r6)))
    own=list(r6.flatten(unittest.defaultTestLoader.loadTestsFromName(TEST_MODULE)))
    require(len(inherited)==5610 and len(own)==spec().OWN_TESTS,'suite components')
    tests=inherited+own; ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==spec().FULL_TESTS and b.EXCLUDED not in ids,'suite identities')
    require(len(b.regression_modules(root))+len(r6.RECOVERY_MODULES)+3==spec().MODULES,'suite module count')
    return unittest.TestSuite(tests)


def subprocess_run(root,folder,head,mode):
    log=folder/(mode+'.log'); command=[sys.executable,'-B','-X','faulthandler','-u',str(Path(__file__).resolve()),
        '--root',str(root),'--folder',str(folder),'--expected-head',head,'--mode',mode]
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
    require(proc.returncode==0,'C327 '+mode+' failed; no automatic retry')


def regression_child(root,folder,head):
    guard(root,head); e,legacy,_,r6=helpers(root); selected=suite(root,spec().parent().base(),e,legacy,r6)
    emit('regression_suite',dict(inherited=5610,own=spec().OWN_TESTS,selected=spec().FULL_TESTS,modules=spec().MODULES))
    emit('regression_test_ids_sha256',spec().digest([t.id() for t in r6.flatten(selected)]))
    result=unittest.TextTestRunner(verbosity=1).run(selected)
    receipt=dict(commit_sha=head,tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),successful=result.wasSuccessful())
    save(folder/'regression-result.json',receipt); emit('regression_result',receipt); check_regression(receipt,head); guard(root,head)


def check_validation(value):
    s=spec()
    require(all(type(value[k]) is int and value[k]==v for k,v in s.WORK.items()),'diagnostic work')
    for key in ('diagnostic_complete','all_weights_preserved','all_reverse_replays'): require(value[key] is True,'diagnostic completion')
    require(value['capability_gate_applicable'] is False and value['sign_gate_applicable'] is False,'no sign/capability gate')
    expected=list(itertools.product(s.SEEDS,s.ARMS,s.GROUPS))
    require([(r['seed'],r['arm'],r['group']) for r in value['aggregates']]==expected,'all aggregate groups')
    for r in value['aggregates']:
        require(r['pairs']==6 and all(type(r[k]) is int and 0<=r[k]<=6 for k in ('defined_cosines','negative_dot','mean_joint_descent')),'aggregate counts')
        require(r['negative_dot']<=r['defined_cosines'],'zero gradients cannot oppose')
        cs=[r[k] for k in ('cosine_min','cosine_median','cosine_max')]
        require(all(v is None for v in cs) if r['defined_cosines']==0 else
                all(type(v) in (int,float) and -1-1e-12<=v<=1+1e-12 for v in cs) and cs==sorted(cs),'cosine summary')


def artifacts(out): return [dict(file=n,sha256=sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in spec().OUTPUTS]


def bound_semantics(out,call):
    before=artifacts(out); result=call(); require(artifacts(out)==before,'output changed during semantic read'); return result,before


def execute_stages(head,preflight,regression,measure,verify,finalize):
    emit('phase','native_gradient_preflight'); preflight()
    emit('phase','full_regression_unmodified_separate_process'); receipt=regression(); check_regression(receipt,head)
    emit('phase','frozen_checkpoint_gradients'); value=measure()
    emit('phase','saved_gradient_geometry_reconstruction'); metrics,verified=verify()
    require(spec().blob(value)==spec().blob(verified),'saved diagnostic mismatch')
    emit('phase','final_uncached_input_recheck'); inventory=finalize()
    return value,metrics,receipt,inventory


def diagnostic_worker(root,folder,head):
    started=time.monotonic(); guard(root,head); s=spec(); s.validate_seal(); e,legacy,r4,_=helpers(root)
    torch,np=e.native_runtime(); api=r4.WinAPI(); emit('native_lock_probe',r4.lock_probe(api,folder))
    p=s.parent(); b=p.base()
    with r4.LockedHashes(sha,lambda path:r4.ReadLease(path,api),progress=lambda r:emit('hash_progress',r)) as cache:
        emit('phase','accepted_C326_composite_snapshot'); result,old_envelope,pins,inputs=snapshot(root,p,e,legacy,cache)
        cx=b.context(); b.check_dependencies(root,pins,cx); data,old,new=parent_semantics(root,result,p,b,cx)
        fingerprint=s.digest((data,old,new)); out=folder/'science'; out.mkdir(exist_ok=False); verified_artifacts=[]
        emit('registration_check',dict(source_pins=len(pins),protected_inputs=len(inputs),manifest_sha256=s.MANIFEST_SHA))
        def regression():
            subprocess_run(root,folder,head,'regression'); guard(root,head)
            for lease,_ in cache.entries.values(): lease.check()
            return read(folder/'regression-result.json')
        def verification():
            with cx[-1].guarded.no_neural():
                value,receipt=bound_semantics(out,lambda:s.semantic_recheck(out,root/PARENT_FOLDER/'science',data,read))
            verified_artifacts.extend(receipt); return value
        value,metrics,receipt,inventory=execute_stages(head,
            lambda:s.runtime_preflight(root/PARENT_FOLDER/'science',data,old,new,cx,root,pins),regression,
            lambda:s.run_diagnostic(out,root/PARENT_FOLDER/'science',data,old,new,cx,root,pins),verification,cache.recheck)
        require(s.digest((data,old,new))==fingerprint,'canonical parent data mutated')
        require(len(inventory)==s.INPUT_COUNT and {r['path']:r['sha256'] for r in inventory}==inputs,'final full inventory')
        hash_stats=dict(cache.stats)
    guard(root,head); check_validation(value); require(artifacts(out)==verified_artifacts,'post-verification output changed')
    result=dict(schema='fold-c327-diagnostic-v1',experiment_id=s.EXPERIMENT_ID,stage=s.STAGE,commit_sha=head,status='PASS',
        diagnostic_execution_valid=True,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,
        source_blobs=pins,input_sha256=inputs,artifacts=verified_artifacts,validation_summary=value,manifest_sha256=s.MANIFEST_SHA,
        runtime=dict(python=sys.version.split()[0],torch=str(torch.__version__),numpy=np.__version__,device='cpu',precision='float64',threads=2,
            worker_seconds=time.monotonic()-started,process_peak_rss_bytes=b.peak_rss(),peak_vram_bytes=None,
            serialized_artifact_bytes=sum(r['serialized_bytes'] for r in verified_artifacts)))
    save(out/'summary.json',result)
    envelope=dict(schema='fold-c327-execution-envelope-v1',commit_sha=head,source_blobs=pins,input_sha256=inputs,
        source_count=s.SOURCE_COUNT,input_count=s.INPUT_COUNT,scientific_summary_sha256=sha(out/'summary.json'),scientific_status='PASS',
        regression=receipt,parent_summary_sha256=PARENT_SUMMARY,parent_envelope_sha256=PARENT_ENVELOPE,
        immediate_parent_semantic_reconstruction=True,ancestor_semantic_reruns=0,saved_semantic_reconstruction=True,
        final_reference_rechecks=len(inventory),hash_stats=hash_stats,manifest_sha256=s.MANIFEST_SHA,scientific_work=s.WORK)
    save(folder/'execution-envelope.json',envelope)
    emit('summary',str(out/'summary.json')); emit('summary_sha256',envelope['scientific_summary_sha256'])
    for row in value['aggregates']: emit('C327 alignment',row)
    emit('diagnostic_status','PASS'); emit('capability_gate_applicable',False)
    emit('execution_envelope',dict(path=str(folder/'execution-envelope.json'),sha256=sha(folder/'execution-envelope.json'),
        source_pins=s.SOURCE_COUNT,protected_inputs=s.INPUT_COUNT,regression_tests=s.FULL_TESTS))
    emit('persisted_gradient_diagnostic','PASS; reverse_replayed_pairs=60; optimizer_steps=0')


def verify_outputs(root,folder,head):
    guard(root,head); s=spec(); s.validate_seal(); out=folder/'science'; result=read(out/'summary.json'); envelope=read(folder/'execution-envelope.json')
    require(result['schema']=='fold-c327-diagnostic-v1' and envelope['schema']=='fold-c327-execution-envelope-v1' and
            result['commit_sha']==envelope['commit_sha']==head and result['experiment_id']==s.EXPERIMENT_ID and result['stage']==s.STAGE,'child identity')
    require(result['status']==envelope['scientific_status']=='PASS' and result['diagnostic_execution_valid'] is True and
            result['capability_gate_applicable'] is False and result['gate_f_candidate'] is False and result['production_adoption'] is False,'diagnostic flags')
    require(result['manifest_sha256']==envelope['manifest_sha256']==s.MANIFEST_SHA and envelope['scientific_work']==s.WORK,'manifest/work')
    require(sha(out/'summary.json')==envelope['scientific_summary_sha256'],'summary hash'); check_validation(result['validation_summary']); check_regression(envelope['regression'],head)
    require(envelope['source_count']==len(envelope['source_blobs'])==s.SOURCE_COUNT and envelope['input_count']==len(envelope['input_sha256'])==s.INPUT_COUNT
            and result['source_blobs']==envelope['source_blobs'] and result['input_sha256']==envelope['input_sha256'],'complete child union')
    require(envelope['parent_summary_sha256']==PARENT_SUMMARY and envelope['parent_envelope_sha256']==PARENT_ENVELOPE and
            envelope['immediate_parent_semantic_reconstruction'] is True and envelope['ancestor_semantic_reruns']==0 and
            envelope['saved_semantic_reconstruction'] is True and envelope['final_reference_rechecks']==s.INPUT_COUNT and
            envelope['hash_stats']['final_reference_rechecks']==s.INPUT_COUNT,'complete child verification')
    e,legacy,_,_=helpers(root); p=s.parent(); parent_out=root/PARENT_FOLDER/'science'
    require(sha(parent_out/'summary.json')==PARENT_SUMMARY and sha(parent_out.parent/'execution-envelope.json')==PARENT_ENVELOPE,'fixed parent hashes')
    pr=read(parent_out/'summary.json'); pe=read(parent_out.parent/'execution-envelope.json'); parent_contract(pr,pe,p,e)
    tree=legacy.tree_blobs(root); pins=envelope['source_blobs']
    require(pins=={**pe['source_blobs'],**{k:tree[k] for k in s.OWN}} and not set(s.OWN)&set(pe['source_blobs']),'exact source union')
    wanted=dict(pe['input_sha256']); wanted.update(legacy.descriptors(parent_out,pr['artifacts'],p.OUTPUTS,sha))
    wanted.update({canonical(parent_out/'summary.json'):PARENT_SUMMARY,canonical(parent_out.parent/'execution-envelope.json'):PARENT_ENVELOPE})
    wanted.update({canonical(root/k):sha(root/k) for k in s.OWN}); require(wanted==envelope['input_sha256'],'exact input union')
    for name,oid in pins.items(): require(tree.get(name)==oid,'source changed'); source_bytes(root/name,oid)
    for name,wanted_hash in wanted.items(): require(sha(name)==wanted_hash,'input changed:'+name)
    legacy.descriptors(out,result['artifacts'],s.OUTPUTS,sha); guard(root,head)
    emit('execution_envelope_verified',dict(source_pins=s.SOURCE_COUNT,protected_inputs=s.INPUT_COUNT,full_tests=s.FULL_TESTS))


def run(root,folder,head):
    guard(root,head); require(folder.is_relative_to(root/'runs') and folder!=root/'runs','output outside runs')
    folder.mkdir(parents=True,exist_ok=False); complete=False
    emit('execution_role','C327-FROZEN-GRADIENT-ALIGNMENT'); emit('scientific_execution_head',head)
    try:
        subprocess_run(root,folder,head,'science'); subprocess_run(root,folder,head,'verify'); complete=True
    finally: guard(root,head); emit('run_execution_valid',complete)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); parser.add_argument('--folder',type=Path,required=True)
    parser.add_argument('--expected-head',required=True); parser.add_argument('--mode',choices=('run','science','regression','verify'),default='run')
    a=parser.parse_args(); root=a.root.resolve(); folder=a.folder.resolve()
    require(folder.is_relative_to(root/'runs') and folder!=root/'runs','output outside runs')
    {'run':run,'science':diagnostic_worker,'regression':regression_child,'verify':verify_outputs}[a.mode](root,folder,a.expected_head)


if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).resolve().parents[1])); main()
