"""C327: fixed C326 checkpoint gradient geometry, with no optimizer or weight update."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import math
import statistics
from pathlib import Path
import torch
from torch.nn import functional as F

EXPERIMENT_ID = 'C327-v5b-frozen-gradient-alignment'
STAGE = 'V5-B-FROZEN-GRADIENT-ALIGNMENT'
SEEDS = tuple(range(326001,326006))
ARMS = ('epoch4','batch4')
PROFILES = ('repeat','shared_prefix','shared_suffix')
LANGUAGES = ('en','ja')
GROUPS = ('all','core','reader','other')
OWN = ('fold_lm/v05_benchmarks/model_c327_gradient_alignment.py','tools/c327_execution.py',
       'tests_lm/test_v05_c327_gradient_alignment.py','tools/run_c327.ps1','tools/invoke_c327.ps1',
       'docs/experiment-ledger-addendum-c327-preregistration.md')
OUTPUTS = ('diagnostic-plan.json','gradients.pt','measurements.json','validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 48,5658,216
SOURCE_COUNT, INPUT_COUNT = 820,1549
WORK = dict(models=10,gradient_pairs=60,gradient_evaluations=240,model_forward_calls=240,
            row_presentations=23040,core_forward_calls=960,model_state_loads=10,
            checkpoint_bundle_loads=1,evaluation_bundle_loads=1,train_steps=0,
            optimizer_steps=0,new_checkpoint_writes=0,network_calls=0)
MANIFEST_SHA = '36fca7e0b0baea3b51adcaad167caa551033e0f802ab3f883d4f4f846cbc22ee'


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def parent(): return importlib.import_module('fold_lm.v05_benchmarks.model_c326_mixing_granularity')


def identities(): return list(itertools.product(SEEDS,ARMS,PROFILES,LANGUAGES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,
        acceptance_base='c3aff2fe3a6067860d19e76903b8f50677984467',
        parent_execution='dbef3dbc1566ff2c8c30405e9c8d207f5e79f460',
        parent_summary_sha256='0dd7af1c69774f5d00b1ee654284c38731f4233b2b858aedcf1bf0aaa77656aa',
        parent_envelope_sha256='d379e907d3d9668f47b9690cb097398005b6c0c6c349ac30082ac3590d7dc62a',
        question='are matched original4/interior4 TRAIN gradients opposed at fixed C326 final checkpoints',
        seeds=list(SEEDS),arms=list(ARMS),profiles=list(PROFILES),languages=list(LANGUAGES),
        rows_per_objective=96,split='TRAIN only',readout='native mean_last',
        objectives='ordinary mean CE,matched logical rows,original4 versus corresponding interior4 profile',
        gradient='autograd.grad on all named parameters;unused tensors explicitly zero with connectivity retained',
        groups=list(GROUPS),partition='core=backbone.core.;reader=read.;other=remaining;all=disjoint union',
        repeat='original then interior,then interior then original at identical state;maxabs1e-9 and identical connectivity',
        saved_logit_check='each forward matches the corresponding protected C326 TRAIN logits,absolute1e-9 and identical argmax',
        statistics='raw dot,cosine,norms;directional derivatives for Euclidean -mean gradient;zero norm cosine=null',
        fixed_gate='diagnostic integrity only;no required conflict sign,frequency or capability improvement',
        boundary='terminal local geometry,not full trajectory,causal gradient-conflict proof or actual AdamW direction;no weight update',
        parameters=14256,core_parameters=3328,slots=64,dtype='CPU float64',threads=2,deterministic=True,
        gradient_payload_bytes=13685760,source_pins=SOURCE_COUNT,protected_inputs=INPUT_COUNT,
        inherited_sources=814,inherited_inputs=1533,parent_files=10,
        own_tests=OWN_TESTS,focused_tests=FULL_TESTS,modules=MODULES,
        excluded_test='tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state',
        parent_validation='both C326 records,all inherited bytes,immediate saved semantics;no recursive older semantic reruns',
        outputs=list(OUTPUTS),capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,
        work_scope='child gradient measurements and reverse repeats;parent/saved verification,preflight and software tests separate',**WORK)


def validate_seal(): require(digest(manifest())==MANIFEST_SHA,'C327 manifest seal')


def group_of(name):
    return 'core' if name.startswith('backbone.core.') else 'reader' if name.startswith('read.') else 'other'


def layout_of(model):
    return [dict(name=n,shape=list(p.shape),numel=p.numel(),group=group_of(n)) for n,p in model.named_parameters()]


def validate_layout(layout):
    require(type(layout) is list and layout,'empty parameter layout'); names=[]; total=0; counts=dict.fromkeys(GROUPS[1:],0)
    for r in layout:
        require(set(r)=={'name','shape','numel','group'} and type(r['name']) is str and r['name'],'layout fields')
        require(type(r['shape']) is list and all(type(n) is int and n>0 for n in r['shape']) and
                type(r['numel']) is int and r['numel']==math.prod(r['shape']) and r['group']==group_of(r['name']),'layout shape/group')
        names.append(r['name']); total+=r['numel']; counts[r['group']]+=r['numel']
    require(len(names)==len(set(names)) and total==14256 and counts['core']==3328 and counts['reader']>0 and counts['other']>0,'native parameter inventory')
    return counts


def row_indices(data,language):
    require(language in LANGUAGES and set(data)=={'TRAIN','HOLDOUT'},'logical split/language')
    ids=[i for i,r in enumerate(data['TRAIN']) if r['language']==language]
    require(len(data['TRAIN'])==192 and len(ids)==96,'complete language TRAIN rows')
    return ids


def objective(model,tokens,targets,expected):
    params=tuple(model.parameters()); require(params and all(p.requires_grad for p in params),'enabled differentiation')
    require(all(p.grad is None for p in params),'preexisting accumulated gradient')
    require(tokens.dtype==targets.dtype==torch.int64 and tokens.ndim==2 and len(tokens)==len(targets),'objective inputs')
    z=model(tokens,torch.zeros(len(tokens),dtype=torch.int64))
    require(z.dtype==torch.float64 and z.device.type=='cpu' and z.shape==expected.shape and
            expected.dtype==torch.float64 and bool(torch.isfinite(z).all()) and bool(torch.isfinite(expected).all()),'finite logits')
    error=float((z.detach()-expected).abs().max())
    require(error<=1e-9 and torch.equal(z.detach().argmax(1),expected.argmax(1)),'protected parent logit replay')
    loss=F.cross_entropy(z,targets); require(bool(torch.isfinite(loss)),'finite loss')
    gs=torch.autograd.grad(loss,params,allow_unused=True)
    connected=[g is not None for g in gs]
    vector=torch.cat([(torch.zeros_like(p) if g is None else g).detach().reshape(-1) for p,g in zip(params,gs,strict=True)])
    require(bool(torch.isfinite(vector).all()) and all(p.grad is None for p in params),'finite nonaccumulating gradient')
    return dict(gradient=vector,connected=connected,loss=float(loss.detach()),logit_error=error)


def repeated_pair(measure):
    a,b=measure(0),measure(1)
    rb,ra=measure(1),measure(0)
    errors=[]
    for first,again in ((a,ra),(b,rb)):
        error=float((first['gradient']-again['gradient']).abs().max())
        require(error<=1e-9 and first['connected']==again['connected'] and abs(first['loss']-again['loss'])<=1e-9,'reverse-order gradient replay')
        errors.append(error)
    return a,b,errors


def geometry(a,b):
    require(isinstance(a,torch.Tensor) and isinstance(b,torch.Tensor) and a.shape==b.shape and a.ndim==1 and
            a.dtype==b.dtype==torch.float64 and a.device.type==b.device.type=='cpu' and
            not a.requires_grad and not b.requires_grad and bool(torch.isfinite(a).all()) and bool(torch.isfinite(b).all()),'gradient vector')
    aa=float(torch.dot(a,a)); bb=float(torch.dot(b,b)); ab=float(torch.dot(a,b))
    require(all(math.isfinite(v) for v in (aa,bb,ab)),'finite gradient moments')
    na,nb=math.sqrt(aa),math.sqrt(bb)
    cosine=None if na==0 or nb==0 else ab/(na*nb)
    require(cosine is None or math.isfinite(cosine) and abs(cosine)<=1+1e-12,'cosine range')
    da,db=-.5*(aa+ab),-.5*(bb+ab)
    return dict(old_norm=na,interior_norm=nb,dot=ab,cosine=cosine,old_squared_norm=aa,interior_squared_norm=bb,
        negative_dot=ab<0,zero_old=na==0,zero_interior=nb==0,old_derivative_along_negative_mean=da,
        interior_derivative_along_negative_mean=db,mean_is_joint_strict_descent=da<0 and db<0)


def partition_metrics(a,b,layout):
    parts={k:[] for k in GROUPS[1:]}; offset=0
    for r in layout:
        parts[r['group']].extend(range(offset,offset+r['numel'])); offset+=r['numel']
    require(offset==a.numel()==b.numel(),'layout/vector alignment')
    result={'all':geometry(a,b)}
    result.update({k:geometry(a[ids],b[ids]) for k,ids in parts.items()})
    for key in ('dot','old_squared_norm','interior_squared_norm'):
        total=sum(result[k][key] for k in GROUPS[1:]); value=result['all'][key]
        require(abs(total-value)<=1e-10*max(1.,abs(total),abs(value)),'gradient partition conservation')
    return result


def saved_expected(parent_record,profile,language,data,b):
    ids=row_indices(data,language); ip=b.templates.INTERIOR_PROFILES[PROFILES.index(profile)]
    raw=parent_record['raw']
    return ids,(raw['original']['4']['TRAIN'][profile]['normal'][ids],raw['interior']['TRAIN'][ip]['normal'][ids])


def analyze(archive,parents,data,b):
    require(set(archive)=={'schema','layout','records','model_receipts'} and archive['schema']=='fold-c327-gradients-v1','gradient archive')
    layout=archive['layout']; validate_layout(layout)
    expected_models=list(itertools.product(SEEDS,ARMS))
    require([(r['seed'],r['arm']) for r in parents]==expected_models,'parent complete cohort')
    require([(r['seed'],r['arm'],r['profile'],r['language']) for r in archive['records']]==identities(),'complete gradient cohort')
    require([(r['seed'],r['arm']) for r in archive['model_receipts']]==expected_models,'model receipt cohort')
    for r,p in zip(archive['model_receipts'],parents,strict=True):
        require(r['before']==r['after']==p['final_sha256'] and r['hooks_restored'] is True and r['no_accumulated_gradients'] is True,'checkpoint preservation')
        require(r['calls']==[24,2304] and r['core_calls']==96 and
                r['policy']==dict(calls=24,query_calls=48,rows=2304,grad_calls=24),'measured forward accounting')
    bymodel={(r['seed'],r['arm']):r for r in parents}; rows=[]
    for r in archive['records']:
        ids,zs=saved_expected(bymodel[r['seed'],r['arm']],r['profile'],r['language'],data,b)
        require(r['row_ids_sha256']==digest([data['TRAIN'][i]['id'] for i in ids]) and r['rows']==96,'row identity')
        y=torch.tensor([data['TRAIN'][i]['target'] for i in ids],dtype=torch.int64)
        vectors=[]
        for j,name in enumerate(('old','interior')):
            v=r[name]; g=v['gradient']; connected=v['connected']
            require(g.shape==(14256,) and g.dtype==torch.float64 and not g.requires_grad and g.device.type=='cpu' and bool(torch.isfinite(g).all()),'saved gradient')
            require(type(connected) is list and len(connected)==len(layout) and all(type(z) is bool for z in connected),'saved connectivity')
            offset=0
            for field,used in zip(layout,connected,strict=True):
                if not used: require(bool((g[offset:offset+field['numel']]==0).all()),'unused gradient not zero')
                offset+=field['numel']
            require(type(v['loss']) in (int,float) and math.isfinite(v['loss']) and
                    abs(v['loss']-float(F.cross_entropy(zs[j],y)))<=1e-9,'saved parent loss replay')
            require(type(v['logit_error']) in (int,float) and 0<=v['logit_error']<=1e-9,'saved logit replay receipt')
            vectors.append(g)
        require(type(r['repeat_errors']) is list and len(r['repeat_errors'])==2 and
                all(type(z) in (int,float) and 0<=z<=1e-9 for z in r['repeat_errors']),'saved gradient replay receipt')
        groups=partition_metrics(*vectors,layout)
        rows.append(dict(seed=r['seed'],arm=r['arm'],profile=r['profile'],language=r['language'],rows=96,
            old_loss=r['old']['loss'],interior_loss=r['interior']['loss'],groups=groups,
            old_unused_parameters=sum(f['numel'] for f,u in zip(layout,r['old']['connected']) if not u),
            interior_unused_parameters=sum(f['numel'] for f,u in zip(layout,r['interior']['connected']) if not u)))
    aggregates=[]
    for seed,arm,group in itertools.product(SEEDS,ARMS,GROUPS):
        gs=[r['groups'][group] for r in rows if (r['seed'],r['arm'])==(seed,arm)]
        require(len(gs)==6,'six profile/language objectives'); cs=[r['cosine'] for r in gs if r['cosine'] is not None]
        aggregates.append(dict(seed=seed,arm=arm,group=group,pairs=6,defined_cosines=len(cs),negative_dot=sum(r['negative_dot'] for r in gs),
            mean_joint_descent=sum(r['mean_is_joint_strict_descent'] for r in gs),
            cosine_min=min(cs) if cs else None,cosine_median=statistics.median(cs) if cs else None,
            cosine_max=max(cs) if cs else None))
    summary=dict(diagnostic_complete=True,capability_gate_applicable=False,sign_gate_applicable=False,
                 all_weights_preserved=True,all_reverse_replays=True,aggregates=aggregates,**WORK)
    return rows,summary


def run_diagnostic(out,parent_out,data,old,new,cx,root,pins):
    p=parent(); b=p.base(); trainer,x=cx[-2:]
    states=p.load_bundle(parent_out/'trained-models.pt')
    saved=torch.load(parent_out/'evaluations.pt',map_location='cpu',weights_only=True)
    require(set(saved)=={'schema','records'} and saved['schema']=='fold-c326-evaluations-v1','parent evaluations')
    parents=saved['records']; prepared=p.previous().training(data,old,new,cx)
    tables={k:v[0] for k,v in prepared.items()}; targets=prepared['original'][1]
    archive=dict(schema='fold-c327-gradients-v1',layout=[],records=[],model_receipts=[])
    for si,seed in enumerate(SEEDS):
        models=p.make_models(seed,x)
        for ai,arm in enumerate(ARMS):
            model=models[arm]; ref=parents[2*si+ai]; state=states[2*si+ai]
            require((ref['seed'],ref['arm'])==(seed,arm) and b.state_digest(state)==ref['saved_state_sha256'],'checkpoint identity')
            model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(True)
            b.check_dependencies(root,pins,cx,model); layout=layout_of(model); validate_layout(layout)
            if not archive['layout']: archive['layout']=layout
            require(archive['layout']==layout,'identical parameter layout'); before=x.c.base.fingerprint(model)
            require(before==ref['final_sha256'],'loaded checkpoint fingerprint'); hooks=trainer.hook_snapshot(model)
            with x.c.p267.counted(model,x.c.core) as (calls,cores),trainer.trained_readout(model,x.wide,'mean_last') as policy:
                for profile,language in itertools.product(PROFILES,LANGUAGES):
                    ids,expected=saved_expected(ref,profile,language,data,b)
                    inputs=(tables['original'][4,profile][ids],tables['interior4'][4,profile][ids])
                    with torch.enable_grad():
                        a,c,errors=repeated_pair(lambda j:objective(model,inputs[j],targets[ids],expected[j]))
                    require(x.c.base.fingerprint(model)==before,'weight mutation during measurement')
                    archive['records'].append(dict(seed=seed,arm=arm,profile=profile,language=language,rows=96,
                        row_ids_sha256=digest([data['TRAIN'][i]['id'] for i in ids]),old=a,interior=c,repeat_errors=errors))
            after=x.c.base.fingerprint(model)
            require(after==before and trainer.hook_snapshot(model)==hooks and all(z.grad is None for z in model.parameters()),'model preservation')
            archive['model_receipts'].append(dict(seed=seed,arm=arm,before=before,after=after,hooks_restored=True,
                no_accumulated_gradients=True,calls=list(calls),core_calls=cores[0],policy=dict(policy)))
            model.requires_grad_(False)
            print(f'[C327] seed={seed} arm={arm} gradient_pairs=6 reverse_replay=PASS weights=UNCHANGED',flush=True)
    metrics,summary=analyze(archive,parents,data,b)
    torch.save(archive,out/'gradients.pt')
    for name,value in (('diagnostic-plan.json',manifest()),('measurements.json',metrics),('validation-summary.json',summary)):
        with (out/name).open('xb') as stream: stream.write(blob(value))
    return summary


def semantic_recheck(out,parent_out,data,read_json):
    b=parent().base(); archive=torch.load(out/'gradients.pt',map_location='cpu',weights_only=True)
    saved=torch.load(parent_out/'evaluations.pt',map_location='cpu',weights_only=True)
    require(saved['schema']=='fold-c326-evaluations-v1','parent evaluation schema')
    metrics,summary=analyze(archive,saved['records'],data,b)
    for name,value in (('diagnostic-plan.json',manifest()),('measurements.json',metrics),('validation-summary.json',summary)):
        require(blob(read_json(out/name))==blob(value),'saved diagnostic reconstruction:'+name)
    return metrics,summary


def runtime_preflight(parent_out,data,old,new,cx,root,pins):
    """One fixed TRAIN gradient/reverse-repeat probe, separately scoped from the cohort."""
    p=parent(); b=p.base(); trainer,x=cx[-2:]
    states=p.load_bundle(parent_out/'trained-models.pt')
    saved=torch.load(parent_out/'evaluations.pt',map_location='cpu',weights_only=True)
    ref=saved['records'][0]
    require((ref['seed'],ref['arm'])==(SEEDS[0],ARMS[0]),'preflight identity')
    model=p.make_models(SEEDS[0],x)[ARMS[0]]; model.load_state_dict(states[0],strict=True); model.eval(); model.requires_grad_(True)
    validate_layout(layout_of(model)); b.check_dependencies(root,pins,cx,model)
    before=x.c.base.fingerprint(model); require(before==ref['final_sha256'],'preflight state'); hooks=trainer.hook_snapshot(model)
    prepared=p.previous().training(data,old,new,cx); ids,expected=saved_expected(ref,PROFILES[0],LANGUAGES[0],data,b)
    tokens=tuple(prepared[k][0][4,PROFILES[0]][ids] for k in ('original','interior4')); y=prepared['original'][1][ids]
    with x.c.p267.counted(model,x.c.core) as (calls,cores),trainer.trained_readout(model,x.wide,'mean_last') as policy,torch.enable_grad():
        repeated_pair(lambda j:objective(model,tokens[j],y,expected[j]))
    require(calls==[4,384] and cores[0]==16 and policy==dict(calls=4,query_calls=8,rows=384,grad_calls=4),'preflight work')
    require(x.c.base.fingerprint(model)==before and trainer.hook_snapshot(model)==hooks and all(z.grad is None for z in model.parameters()),'preflight preservation')
    model.requires_grad_(False)
    print('C327_native_gradient_preflight = PASS; forwards=4; optimizer_steps=0; cohort_started=False',flush=True)
