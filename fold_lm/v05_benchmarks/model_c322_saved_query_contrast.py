"""C322: saved-logit paired-query contrast; no new neural computation."""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
from types import ModuleType
import unittest
import torch

EXPERIMENT_ID = 'C322-v5b-saved-query-contrast'
STAGE = 'V5-B-SAVED-QUERY-CONTRAST'
BASE = '9025d339a67ae4b4b22435b8bda068c204d49d5e'
PARENT_EXECUTION = 'a31d5c5389f41cdb137b0bf375b7c7a99d8fb882'
PARENT_SHA = '0e95c700cbac90025beb7baf1d65413cb1694de72b659540c2eb901f77f52fd9'
PARENT_SOURCE = 'fold_lm/v05_benchmarks/model_c321_interior_name_order.py'
PARENT_BLOB = '6c55bedbfb0373ce809e3bd62a73260adaf65212'
SEEDS = tuple(range(319001,319006))
ARMS = ('mean_last','last_only')
CONDITIONS = ('old4','interior')
SPLITS = ('TRAIN','HOLDOUT')
PROFILES = ('u_dominant','balanced','v_dominant')
OLD_PROFILES = ('repeat','shared_prefix','shared_suffix')
LANGUAGES = ('en','ja')
TOLERANCE = 1e-9
OWN = ('fold_lm/v05_benchmarks/model_c322_saved_query_contrast.py',
       'tests_lm/test_v05_c322_saved_query_contrast.py','tools/run_c322.ps1','tools/invoke_c322.ps1',
       'docs/experiment-ledger-addendum-c322-preregistration.md','docs/v5b-saved-query-contrast-v0.1.md')
OUTPUTS = ('audit-plan.json','query-pairs.json','measurements.json','validation-summary.json')
EXCLUDED = 'tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state'
WORK = dict(models=10,saved_answers=17280,paired_contexts=8640,groups=240,
            train_steps=0,model_forward_calls=0,model_state_loads=0,new_checkpoint_writes=0,network_calls=0)
MANIFEST_SHA = '719cd169028e0c0ead99f4620035b532cefed65145c4bcb4f8af3c781fda01e8'


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c321_interior_name_order as p
    parent,owner,x = p.context()
    return p,parent,owner,x


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        parent_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,
        conditions=list(CONDITIONS),seeds=list(SEEDS),arms=list(ARMS),profiles=list(PROFILES),
        old_profiles=list(OLD_PROFILES),old_profile_pairing='matched row families,not identical old/new strings',
        question='does query-dependent output discrimination collapse or merely fail to change the top answer',
        pair_orientation='canonical entities[0] query A then entities[1] query B,never logit or target ranking',
        shift_distance='max_abs((zA-zB)-(zA[0]-zB[0]));constant logit shifts removed',
        preference='mA=zA[tA]-zA[tB];mB=zB[tA]-zB[tB];D=mA-mB',
        contrast_signs='strict positive/zero/negative;not a capability or accuracy gate',
        near_shift_invariant_tolerance=TOLERANCE,normal_argmax='all256 classes unchanged',
        exact_two_value_direction='mA>0 and mB<0;descriptive only,no restricted decoder',
        parents=48,source_pins=778,protected_inputs=1467,own_tests=24,modules=207,
        loaded_tests=5270,focused_tests=5269,excluded_test=EXCLUDED,
        dtype='saved CPU float64',capability_gate_applicable=False,gate_f_candidate=False,
        production_adoption=False,limits='output diagnostic only;no hidden-state or causal claim',**WORK)


def validate_seal(): require(digest(manifest())==MANIFEST_SHA,'manifest seal')


def pair_rows(rows):
    """Group identical facts/order; retain canonical entity order,not adjacency assumptions."""
    groups = {}; seen=set()
    for i,r in enumerate(rows):
        require(r['id'] not in seen,'duplicate row ID'); seen.add(r['id'])
        e=tuple(r['entities']); v=tuple(r['values']); order=tuple(r['permutation'])
        require(len(e)==len(v)==2 and len(set(e))==2 and len(set(v))==2 and set(order)==set(e)
                and r['query'] in e and r['language'] in LANGUAGES,'logical row')
        require(type(r['target']) is int and r['target']==48+v[e.index(r['query'])],'target binding')
        key=(r['language'],e,v,order); g=groups.setdefault(key,{})
        require(r['query'] not in g,'duplicate query'); g[r['query']]=i
    out=[]
    for (_,e,_,_),g in groups.items():
        require(set(g)==set(e),'incomplete question pair'); out.append((g[e[0]],g[e[1]]))
    require(len(out)*2==len(rows),'pair coverage'); return out


def pair_measure(zA,zB,tA,tB):
    require(zA.shape==zB.shape==(256,) and zA.dtype==zB.dtype==torch.float64 and zA.device.type==zB.device.type=='cpu'
            and not zA.requires_grad and not zB.requires_grad and bool(torch.isfinite(zA).all()) and bool(torch.isfinite(zB).all()),'logit contract')
    require(type(tA) is int and type(tB) is int and 48<=tA<=51 and 48<=tB<=51 and tA!=tB,'pair targets')
    delta=zA-zB; centered=delta-delta[0]
    mA=float(zA[tA]-zA[tB]); mB=float(zB[tA]-zB[tB]); contrast=mA-mB
    raw=float(delta.abs().max()); dist=float(centered.abs().max())
    require(all(math.isfinite(v) for v in (mA,mB,contrast,raw,dist)),'nonfinite contrast')
    a,b=int(zA.argmax()),int(zB.argmax())
    return dict(prediction_A=a,prediction_B=b,target_A=tA,target_B=tB,correct_count=int(a==tA)+int(b==tB),
        same_prediction=a==b,raw_linf=raw,shift_invariant_linf=dist,near_shift_invariant=dist<=TOLERANCE,
        margin_A=mA,margin_B=mB,contrast=contrast,contrast_sign=1 if contrast>0 else -1 if contrast<0 else 0,
        both_target_directions=mA>0 and mB<0)


def aggregate(rows):
    require(bool(rows),'empty aggregation')
    out=dict(pairs=len(rows),answers=2*len(rows),correct=sum(r['correct_count'] for r in rows),
        same_prediction=sum(r['same_prediction'] for r in rows),both_correct=sum(r['correct_count']==2 for r in rows),
        one_correct=sum(r['correct_count']==1 for r in rows),both_wrong=sum(r['correct_count']==0 for r in rows),
        near_shift_invariant=sum(r['near_shift_invariant'] for r in rows),both_target_directions=sum(r['both_target_directions'] for r in rows),
        contrast_positive=sum(r['contrast_sign']==1 for r in rows),contrast_zero=sum(r['contrast_sign']==0 for r in rows),
        contrast_negative=sum(r['contrast_sign']==-1 for r in rows))
    for k in ('raw_linf','shift_invariant_linf','margin_A','margin_B','contrast'):
        values=[r[k] for r in rows]; out[k]=dict(mean=math.fsum(values)/len(values),minimum=min(values),maximum=max(values))
    require(out['correct']==2*out['both_correct']+out['one_correct'],'correctness conservation')
    return out


def analyze(records,data,p,x,parent_summary):
    require([(r['seed'],r['arm']) for r in records]==identities(),'cohort order')
    indices={s:pair_rows(data[s]) for s in SPLITS}; pairs=[]; reconciliations=[]
    expected={(r['seed'],r['arm'],r['split']):r for r in parent_summary['final_partitions']}
    require(len(expected)==20,'parent partitions')
    for record in records:
        require(record['readout_policy']==record['arm'] and record['weights_preserved'] is True and record['hooks_restored'] is True,'parent provenance')
        for condition in CONDITIONS:
            raw=record['raw']['before']['4'] if condition=='old4' else record['raw']['interior']
            score=x.wide.score_length(data,raw,x.c) if condition=='old4' else p.score_new(raw,data,x)
            local=x.diag.normalize_task(score,'triple',record['seed'],record['arm'])
            for split in SPLITS:
                partition=x.diag.partition([v for v in local if v['split']==split]); subset=[]
                for slot,profile in enumerate(PROFILES):
                    key=OLD_PROFILES[slot] if condition=='old4' else profile
                    z=raw[split][key]['normal']; x.c.p267.check_logits(z,len(data[split]))
                    for ia,ib in indices[split]:
                        a,b=data[split][ia],data[split][ib]
                        r=dict(seed=record['seed'],arm=record['arm'],condition=condition,split=split,profile=profile,
                            source_profile=key,language=a['language'],row_A=a['id'],row_B=b['id'],
                            **pair_measure(z[ia],z[ib],a['target'],b['target']))
                        pairs.append(r); subset.append(r)
                totals=aggregate(subset)
                require((totals['answers'],totals['correct'],totals['pairs'],totals['same_prediction'])==
                        tuple(partition[k] for k in ('rows','correct','pairs','collapsed_pairs')),'original-score reconciliation')
                if condition=='interior':
                    old=expected[(record['seed'],record['arm'],split)]
                    require(all(partition[k]==old[k] for k in ('rows','correct','pairs','collapsed_pairs','full_pass')),'parent aggregate reconciliation')
                reconciliations.append(dict(seed=record['seed'],arm=record['arm'],condition=condition,split=split,matched=True,
                    rows=totals['answers'],correct=totals['correct'],same_prediction=totals['same_prediction']))
    grouped=defaultdict(list)
    for r in pairs: grouped[tuple(r[k] for k in ('seed','arm','condition','split','profile','language'))].append(r)
    keys=('seed','arm','condition','split','profile','language')
    groups=[dict(zip(keys,key,strict=True),**aggregate(value)) for key,value in sorted(grouped.items())]
    overall=[dict(arm=a,condition=c,**aggregate([r for r in pairs if r['arm']==a and r['condition']==c])) for a,c in itertools.product(ARMS,CONDITIONS)]
    require(len(pairs)==8640 and len(groups)==240 and len(reconciliations)==40,'diagnostic inventory')
    return pairs,groups,dict(diagnostic_complete=True,capability_gate_applicable=False,reconciliations=reconciliations,overall=overall,**WORK)


def load_parent(paths):
    p,parent,owner,x=context(); paths=[Path(v).resolve() for v in paths]
    hashes=(PARENT_SHA,p.PARENT_SHA,*parent.parent_hashes(owner))
    require(len(paths)==len(hashes)==48 and all(x.c.audit.sha(v)==h for v,h in zip(paths,hashes,strict=True)),'48 parent hashes')
    with x.guarded.no_neural():
        evidence,_=p.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); p.validate_result(evidence)
        require(evidence['experiment_id']=='C321-v5b-frozen-interior-name-order' and evidence['commit_sha']==PARENT_EXECUTION
                and evidence['status']=='FAIL' and evidence['source_blobs'].get(PARENT_SOURCE)==PARENT_BLOB,'parent identity')
        require(evidence['validation_summary']['pass_counts']==dict.fromkeys(ARMS,0) and evidence['validation_summary']['primary_gate'] is False,'parent verdict')
        require(len(evidence['artifacts'])==5 and {a['file'] for a in evidence['artifacts']}==set(p.OUTPUTS),'parent artifacts')
        _,data,_,_=p.load_parent(paths[1:])
        archive=torch.load(paths[0].parent/'evaluations.pt',map_location='cpu',weights_only=True)
        require(set(archive)=={'schema','records'} and archive['schema']=='fold-c321-interior-eval-v1','archive schema')
    return evidence,data,archive['records']


def precheck(paths,root):
    validate_seal(); p,parent,owner,x=context(); loaded=load_parent(paths); evidence=loaded[0]; root=Path(root).resolve()
    pins,inputs=dict(evidence['source_blobs']),dict(evidence['input_sha256'])
    require((len(pins),len(inputs))==(772,1455) and pins.get(PARENT_SOURCE)==PARENT_BLOB,'parent protection')
    for m in [p,parent,owner,*owner.context(),x.parent,*x.parent.context(),*x.p312.context(),*x.wide.context(),*vars(x.c).values(),x.c.factory.language_module()]:
        path=getattr(m,'__file__',None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root): require(Path(path).resolve().relative_to(root).as_posix() in pins,'unprotected helper')
    for n,h in pins.items(): require(x.c.audit.git(root,'rev-parse','HEAD:'+n).decode().strip()==h,'changed source:'+n)
    for n,h in inputs.items(): require(Path(n).is_file() and x.c.audit.sha(n)==h,'changed input:'+n)
    folder=Path(paths[0]).resolve().parent
    for path,h in [(folder/'summary.json',PARENT_SHA)]+[(x.c.audit.safe_child(folder,a['file']),a['sha256']) for a in evidence['artifacts']]:
        require(str(path.resolve()) not in inputs and x.c.audit.sha(path)==h,'parent input'); inputs[str(path.resolve())]=h
    for n in OWN: require(n not in pins,'OWN collision'); pins[n]=x.c.audit.git(root,'rev-parse','HEAD:'+n).decode().strip()
    inputs.update(x.c.audit.protect_tree_files(root,pins)); require((len(pins),len(inputs))==(778,1467),'protection counts')
    print(f'registration_check = source_pins:778; protected_inputs:1467; manifest_sha256:{MANIFEST_SHA}',flush=True)
    return pins,inputs,loaded


def validate_result(p):
    require(p['experiment_id']==EXPERIMENT_ID and p['stage']==STAGE and p['status']=='PASS' and p['diagnostic_execution_valid'] is True
            and all(p[k] is False for k in ('capability_gate_applicable','gate_f_candidate','production_adoption')),'diagnostic scope')
    require((len(p['source_blobs']),len(p['input_sha256']))==(778,1467) and set(OWN)<=set(p['source_blobs'])
            and p['source_blobs'].get(PARENT_SOURCE)==PARENT_BLOB,'result protection')
    require(len(p['artifacts'])==4 and {a['file'] for a in p['artifacts']}==set(OUTPUTS),'artifacts')
    s=p['validation_summary']; require(s['diagnostic_complete'] is True and s['capability_gate_applicable'] is False
        and len(s['overall'])==4 and len(s['reconciliations'])==40 and all(r['matched'] is True for r in s['reconciliations'])
        and all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),'summary contract')


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==206,'parent modules')
    return names+['tests_lm.test_v05_c322_saved_query_contrast']


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==5270 and ids.count(EXCLUDED)==1,'loaded suite')
    return unittest.TestSuite(t for t in tests if t.id()!=EXCLUDED)


def guard(root,head,owner,x): owner.context()[1].guard(root,head,x.c)


def runtime_preflight(paths,root):
    torch.set_num_threads(2); _,_,loaded=precheck(paths,root); p,_,_,x=context()
    with x.guarded.no_neural(): analyze(loaded[2],loaded[1],p,x,loaded[0]['validation_summary'])
    print('saved_query_pair_reconciliation = PASS; new_model_forwards = 0',flush=True)


def run(*,summaries,output_dir,expected_head):
    torch.set_num_threads(2); p,_,owner,x=context(); root=Path(__file__).resolve().parents[2]; guard(root,expected_head,owner,x)
    pins,inputs,loaded=precheck(summaries,root)
    with x.guarded.no_neural(): pairs,groups,s=analyze(loaded[2],loaded[1],p,x,loaded[0]['validation_summary'])
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    for n,v in zip(OUTPUTS,(manifest(),pairs,groups,s),strict=True): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=x.c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    for n,h in inputs.items(): require(x.c.audit.sha(n)==h,'input changed during diagnostic')
    guard(root,expected_head,owner,x)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status='PASS',diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=inputs,artifacts=artifacts,validation_summary=s,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(result); (out/'summary.json').write_bytes(blob(result)); print('C322 saved query contrast complete',flush=True); return result


def verify_artifacts(outdir,summaries,expected_head):
    p,_,_,x=context(); out=Path(outdir); result=x.c.audit.read_json(out/'summary.json'); validate_result(result)
    require(result['commit_sha']==expected_head,'execution HEAD')
    for n,h in result['input_sha256'].items(): require(x.c.audit.sha(n)==h,'protected input')
    for a in result['artifacts']:
        path=x.c.audit.safe_child(out,a['file']); require(x.c.audit.sha(path)==a['sha256'] and path.stat().st_size==a['serialized_bytes'],'output bytes')
    with x.guarded.no_neural():
        evidence,data,records=load_parent(summaries); pairs,groups,s=analyze(records,data,p,x,evidence['validation_summary'])
        for n,v in zip(OUTPUTS,(manifest(),pairs,groups,s),strict=True): require(x.c.audit.read_json(out/n)==v,'persisted:'+n)
    require(result['validation_summary']==s,'summary reconstruction'); return result,groups


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--summaries',nargs=48,type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True); parser.add_argument('--expected-head',required=True); run(**vars(parser.parse_args()))

if __name__=='__main__': main()
