"""C326: exact-exposure epoch mixing versus within-update query-pair mixing.

Allocation is a deterministic integral flow on schedule identities, not model
outputs. Accepted modules are called without patching their globals or functions.
"""
from __future__ import annotations
from collections import deque
import copy
import hashlib
import importlib
import itertools
import json
import math
import torch
from torch.nn import functional as F

EXPERIMENT_ID = 'C326-v5b-mixing-granularity'
STAGE = 'V5-B-MIXING-GRANULARITY'
SEEDS = tuple(range(326001,326006))
ORDERS = tuple(range(326101,326106))
ARMS = ('epoch4','batch4')
PROFILES = ('repeat','shared_prefix','shared_suffix')
STEPS, FIT_RNG = 1200, 612000
OWN = ('fold_lm/v05_benchmarks/model_c326_mixing_granularity.py',
       'tools/c326_execution.py','tests_lm/test_v05_c326_mixing_granularity.py',
       'tools/run_c326.ps1','tools/invoke_c326.ps1',
       'docs/experiment-ledger-addendum-c326-preregistration.md')
OUTPUTS = ('experiment-plan.json','dataset.json','original-prompts.json',
           'interior-prompts.json','trained-models.pt','evaluations.pt',
           'measurements.json','validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 64, 5610, 215
SOURCE_COUNT, INPUT_COUNT = 814, 1533
WORK = dict(models=10,train_steps=12000,training_rows=576000,
            model_forward_calls=15420,row_presentations=904320,
            core_forward_calls=61680,model_state_loads=10,
            checkpoint_bundle_loads=1,new_checkpoint_writes=1,network_calls=0)
MANIFEST_SHA = '2be1555cf0296e55f5adf2e11302d6112b9b49836781199fcb3fc126d384871e'


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def previous():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c325_mixed_name_coverage')


def base(): return previous().base()


def identities(): return list(itertools.product(SEEDS,ARMS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,
        acceptance_base='1a8d15e46aa0b661d5570bed662e67aa1760fc77',
        parent_execution='f95895313da81634976d0ff2761efdd793888c2b',
        parent_summary_sha256='e3e9808fea616ecc27e2644f808553f16fb6a11203284bdea5c2cf63b32006e8',
        parent_envelope_sha256='e40a7e93159cdf33b94b11e8ee8df197da66949d121dd52eb8c6036db99440b9',
        question='does within-update mixing recover interior binding without losing original retention at exactly matched per-pair/per-profile family exposure',
        arms=list(ARMS),seeds=list(SEEDS),orders=list(ORDERS),
        control='C325 mixed4 rule: complete length4 epochs alternate old/interior starting old',
        candidate='deterministic integral flow spreads old/interior query pairs within each length4 update',
        allocation='per profile: each pair retains its control old quota; update old quota is successive integer-floor difference of total_old/updates; edges chronological update then sorted pair ID; Dinic BFS/DFS insertion order',
        changed='temporal family assignment only; exact pair/profile family exposure retained',
        held='logical row order,query pair membership,targets,length/profile order,total per-row exposure,paired fresh initialization,optimizer,precision,architecture,steps',
        per_row_length_exposure=[0,100,100,100],length4_old_exposure=50,length4_interior_exposure=50,
        batch_pair_family_counts='11..13 old of24 pairs per length4 update,balanced to preserve odd profile quotas;not an exact12/12 claim',
        parameters=14256,core_parameters=3328,slots=64,readout='native mean_last',
        steps_per_model=STEPS,rows_per_step=48,fit_rng=FIT_RNG,
        optimizer='AdamW betas .9/.999 eps1e-8 weight_decay0;global gradient clip1',
        core_lr=.0005,other_lr=.005,loss='ordinary mean CE',
        primary='ALL5 batch4 full interior and original2..6 gates;strictly positive interior HOLDOUT answer and both-query gains;nonnegative pooled original2..6 HOLDOUT answer and both-query gains versus epoch4',
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        original_single='length1 descriptive only',
        boundary='a temporal-allocation intervention,not proof of gradient conflict or universal mixing benefit;seen templates,reused logical split,no seed selection',
        allocation_failure='INVALID before fitting;no outcome-dependent alternative allocator',
        source_pins=SOURCE_COUNT,protected_inputs=INPUT_COUNT,inherited_sources=808,inherited_inputs=1517,
        immediate_parent_files=10,own_tests=OWN_TESTS,focused_tests=FULL_TESTS,modules=MODULES,
        excluded_test='tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state',
        dtype='CPU float64',threads=2,deterministic=True,replay_tolerance=1e-9,
        internal_steps_per_forward=4,raw_logit_payload_bytes=336199680,
        outputs=list(OUTPUTS),parent_validation='exact C325 summary+envelope,all inherited bytes,immediate saved semantics;no recursive older semantic reruns',
        execution='native Windows read leases;separate ordinary full regression;ten model replays;saved semantic reconstruction;fresh byte verifier',
        work_scope='child fitting/evaluation/ten replays only;preflight,allocation,tests,parent/saved verification separately scoped',
        gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal(): require(digest(manifest())==MANIFEST_SHA,'C326 manifest seal')


def validate_schedule(events):
    require(isinstance(events,torch.Tensor) and events.dtype==torch.int64 and
            events.device.type=='cpu' and events.shape==(STEPS,24,4),'schedule shape/dtype')
    canonical=None
    for epoch in range(STEPS//4):
        e=events[4*epoch:4*epoch+4]
        require(bool((e[:,:,:2]==e[0,0,:2]).all()),'split epoch length/profile')
        require(int(e[0,0,0]) in (2,3,4) and int(e[0,0,1]) in (0,1,2),'schedule domain')
        require(sorted(e[:,:,2:].flatten().tolist())==list(range(192)),'incomplete epoch')
        pairs={tuple(sorted(r)) for r in e[:,:,2:].reshape(-1,2).tolist()}
        if canonical is None: canonical=pairs
        require(len(pairs)==96 and pairs==canonical,'query pair identity changed')
    for length in (2,3,4):
        ids=events[events[:,:,0]==length][:,2:].flatten()
        require(torch.equal(torch.bincount(ids,minlength=192),torch.full((192,),100,dtype=torch.int64)),'length exposure')


def schedule(seed,rows,x):
    require(type(seed) is int and seed in SEEDS and len(rows)==192,'schedule identity')
    e=x.parent.plan_for_order(ORDERS[SEEDS.index(seed)],'two_to_four',rows,x.p312,x.pairs)
    validate_schedule(e)
    return e


def block_mask(events):
    validate_schedule(events)
    mask=torch.zeros((STEPS,24),dtype=torch.int64); ordinal=0
    for epoch in range(STEPS//4):
        if int(events[epoch*4,0,0])==4:
            mask[epoch*4:epoch*4+4]=ordinal%2; ordinal+=1
    require(ordinal==100 and int(mask.sum())==4800,'block family exposure')
    return mask


def balanced_allocation(neighbors,quotas):
    """Integral bipartite flow: chosen edges use ORIGINAL, not interior, names."""
    require(neighbors and quotas and all(type(q) is int and q>=0 for q in quotas),'flow quotas')
    m,n=len(neighbors),len(quotas); total=sum(quotas)
    require(all(row and len(row)==len(set(row)) and all(type(v) is int and 0<=v<n for v in row)
                for row in neighbors),'flow neighbors')
    caps=[((i+1)*total)//m-(i*total)//m for i in range(m)]
    require(all(0<=q<=len(row) for q,row in zip(caps,neighbors,strict=True)),'infeasible update quota')
    source=m+n; sink=source+1; graph=[[] for _ in range(sink+1)]
    def edge(a,b,c):
        f=[b,len(graph[b]),c]; r=[a,len(graph[a]),0]
        graph[a].append(f); graph[b].append(r); return f
    for i,q in enumerate(caps): edge(source,i,q)
    refs={}
    for i,row in enumerate(neighbors):
        for j in sorted(row): refs[i,j]=edge(i,m+j,1)
    for j,q in enumerate(quotas): edge(m+j,sink,q)
    flow=0
    while True:
        level=[-1]*len(graph); level[source]=0; todo=deque([source])
        while todo:
            a=todo.popleft()
            for b,_,cap in graph[a]:
                if cap and level[b]<0: level[b]=level[a]+1; todo.append(b)
        if level[sink]<0: break
        offset=[0]*len(graph)
        def send(a,amount):
            if a==sink: return amount
            while offset[a]<len(graph[a]):
                item=graph[a][offset[a]]; b,reverse,cap=item
                if cap and level[b]==level[a]+1:
                    pushed=send(b,min(amount,cap))
                    if pushed:
                        item[2]-=pushed; graph[b][reverse][2]+=pushed; return pushed
                offset[a]+=1
            return 0
        while pushed:=send(source,total-flow): flow+=pushed
    require(flow==total,'infeasible exact family assignment; no fallback')
    chosen=[{j for j in row if refs[i,j][2]==0} for i,row in enumerate(neighbors)]
    require([len(x) for x in chosen]==caps and [sum(j in x for x in chosen) for j in range(n)]==quotas,'flow conservation')
    return chosen,caps


def exposure(events,mask):
    require(mask.shape==(STEPS,24) and mask.dtype==torch.int64 and mask.device.type=='cpu'
            and bool(((mask==0)|(mask==1)).all()),'family mask')
    result={}
    for e,f in zip(events.tolist(),mask.tolist(),strict=True):
        for row,family in zip(e,f,strict=True):
            n,p,a,b=row
            if n!=4: require(family==0,'short-name family changed')
            key=f'{n}:{p}:{min(a,b)}:{max(a,b)}'
            counts=result.setdefault(key,[0,0]); counts[family]+=1
    return result


def family_mask(events,arm):
    require(arm in ARMS,'unregistered arm')
    control=block_mask(events)
    if arm=='epoch4': return control
    raw=events.tolist(); result=control.clone()
    pairs=sorted({tuple(sorted(row[2:])) for e in raw[:4] for row in e})
    index={pair:i for i,pair in enumerate(pairs)}
    for profile in range(3):
        steps=[i for i,e in enumerate(raw) if e[0][:2]==[4,profile]]
        neighbors=[[index[tuple(sorted(row[2:]))] for row in raw[i]] for i in steps]
        quotas=[0]*96
        for i,row in zip(steps,neighbors,strict=True):
            for k,j in enumerate(row): quotas[j]+=int(control[i,k]==0)
        chosen,caps=balanced_allocation(neighbors,quotas)
        require(min(caps)>=11 and max(caps)<=13,'registered mixed-update bound')
        for i,row,old in zip(steps,neighbors,chosen,strict=True):
            result[i]=torch.tensor([0 if j in old else 1 for j in row],dtype=torch.int64)
    require(exposure(events,result)==exposure(events,control),'per-pair/profile exposure changed')
    require(int(result.sum())==4800 and not torch.equal(result,control),'no temporal intervention')
    return result


def make_models(seed,x):
    require(type(seed) is int and seed in SEEDS,'fresh model seed')
    c=x.c; ref=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    template=x.wide.LengthReadout(ref); models={a:x.policy.configure(copy.deepcopy(template),'core_slow') for a in ARMS}
    used=set()
    for m in models.values():
        require(type(m) is x.wide.LengthReadout and m.backbone.config.max_tokens==64 and m.backbone.core.config.slots==64,'architecture')
        require(sum(z.numel() for z in m.parameters())==14256 and sum(z.numel() for z in m.backbone.core.parameters())==3328,'capacity')
        require(c.base.fingerprint(m)==c.base.fingerprint(ref) and list(m.state_dict())==list(ref.state_dict()),'paired initialization')
        require(all(z.requires_grad and z.dtype==torch.float64 and z.device.type=='cpu' for z in m.parameters()),'precision')
        ptr={z.data_ptr() for z in m.parameters()}; require(not ptr&used,'shared storage'); used.update(ptr)
        x.policy.parameter_groups(m,'core_slow')
    return models


def select_tokens(tables,event,selected):
    require(selected.dtype==torch.int64 and selected.shape==(len(event),) and
            bool(((selected==0)|(selected==1)).all()),'batch family selection')
    n,p=map(int,event[0,:2]); ids=event[:,2:].flatten()
    a=tables['original'][n,PROFILES[p]][ids]; b=tables['interior4'][n,PROFILES[p]][ids]
    return torch.where(selected.repeat_interleave(2)[:,None].bool(),b,a),ids


def train_steps(model,tables,targets,events,mask,x):
    torch.manual_seed(FIT_RNG); opt=x.policy.optimizer_for(model,'core_slow'); model.train()
    losses=[]; rates=[]; counts=[]; union={}
    for step,(event,selected) in enumerate(zip(events,mask,strict=True)):
        x.policy.verify_optimizer(opt,model,'core_slow'); rates.append([g['lr'] for g in opt.param_groups]); opt.zero_grad(set_to_none=True)
        tokens,ids=select_tokens(tables,event,selected)
        z=model(tokens,torch.zeros(len(ids),dtype=torch.int64)); x.c.p267.check_logits(z,len(ids))
        loss=F.cross_entropy(z,targets[ids]); require(bool(torch.isfinite(loss)),'nonfinite training loss'); losses.append(float(loss.detach()))
        loss.backward(); got={n:p.numel() for n,p in model.named_parameters() if p.grad is not None}; union.update(got); counts.append(sum(got.values()))
        torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True); opt.step()
        if (step+1)%200==0: print(f'[C326] step={step+1}/{len(events)} ce={losses[-1]:.6f}',flush=True)
    model.eval()
    return dict(ce_history=losses,optimizer_group_lrs=rates,gradient_parameter_counts=counts,gradient_union=dict(sorted(union.items())))


def fit(model,tables,targets,events,arm,x):
    mask=family_mask(events,arm); keys=set(itertools.product((2,3,4),PROFILES))
    require(set(tables)=={'original','interior4'} and targets.shape==(192,) and targets.dtype==torch.int64,'TRAIN inputs')
    require(all(set(t)==keys and all(z.shape==(192,64) and z.dtype==torch.int64 and z.device.type=='cpu' for z in t.values()) for t in tables.values()),'TRAIN tables')
    trace=train_steps(model,tables,targets,events,mask,x)
    return dict(steps=STEPS,training_rows=57600,fit_rng=FIT_RNG,optimizer_creations=1,trainable_parameters=14256,
        schedule_events=events.clone(),template_pair_events=mask.clone(),family_exposure=exposure(events,mask),
        family_schedule_sha256=digest(mask.tolist()),**trace,**x.parent.schedule_stats(events))


def check_fit(trace,seed,arm,rows,x):
    events=schedule(seed,rows,x); mask=family_mask(events,arm)
    fixed=dict(steps=STEPS,training_rows=57600,fit_rng=FIT_RNG,optimizer_creations=1,trainable_parameters=14256)
    require(all(type(trace[k]) is int and trace[k]==v for k,v in fixed.items()),'fit budget')
    require(torch.equal(trace['schedule_events'],events) and torch.equal(trace['template_pair_events'],mask),'saved schedule')
    require(trace['family_exposure']==exposure(events,mask) and trace['family_schedule_sha256']==digest(mask.tolist()),'saved family exposure')
    require(all(trace[k]==v for k,v in x.parent.schedule_stats(events).items()),'saved logical exposure')
    require(trace['optimizer_group_lrs']==[[.005,.0005]]*STEPS and len(trace['ce_history'])==STEPS and
            all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in trace['ce_history']),'optimizer/loss trace')
    union=trace['gradient_union']; counts=trace['gradient_parameter_counts']
    require(union and all(type(k) is str and type(v) is int and v>0 for k,v in union.items()) and 0<sum(union.values())<=14256,'gradient union')
    require(len(counts)==STEPS and all(type(v) is int and 0<v<=sum(union.values()) for v in counts),'gradient counts')


def train_one(model,tables,targets,events,data,old,new,seed,arm,cx):
    b=base(); trainer,x=cx[-2:]; c=x.c
    initial,ci=c.base.fingerprint(model),c.base.fingerprint(model.backbone.core); hooks=trainer.hook_snapshot(model)
    print(f'[C326] seed={seed} arm={arm} phase=training',flush=True)
    with c.p267.counted(model,c.core) as (calls,cores),trainer.trained_readout(model,x.wide,'mean_last') as stats:
        trained=fit(model,tables,targets,events,arm,x); final,cf=c.base.fingerprint(model),c.base.fingerprint(model.backbone.core)
        model.requires_grad_(False); raw=b.evaluate(model,data,old,new,cx)
    require(calls==[1371,74016] and cores[0]==5484 and stats==dict(calls=1371,query_calls=2742,rows=74016,grad_calls=1200),'fit/evaluation work')
    require(initial!=final and ci!=cf and c.base.fingerprint(model)==final and trainer.hook_snapshot(model)==hooks,'learned/preserved state')
    state={n:z.detach().cpu().clone() for n,z in model.state_dict().items()}
    return dict(seed=seed,arm=arm,readout_policy='mean_last',initial_sha256=initial,core_initial_sha256=ci,final_sha256=final,
        core_final_sha256=cf,fit=trained,raw=raw,policy_receipt=dict(stats),forward_calls=1371,row_presentations=74016,
        core_forward_calls=5484,saved_state_sha256=b.state_digest(state)),state


def replay(model,state,record,data,old,new,cx):
    b=base(); trainer,x=cx[-2:]
    require(list(state)==list(model.state_dict()) and all(state[k].shape==v.shape and state[k].dtype==v.dtype for k,v in model.state_dict().items()),'checkpoint schema')
    require(b.state_digest(state)==record['saved_state_sha256'],'checkpoint digest')
    model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(False)
    fingerprint=x.c.base.fingerprint(model); hooks=trainer.hook_snapshot(model); require(fingerprint==record['final_sha256'],'checkpoint fingerprint')
    with x.c.p267.counted(model,x.c.core) as (calls,cores),trainer.trained_readout(model,x.wide,'mean_last') as stats:
        raw=b.evaluate(model,data,old,new,cx)
    require(calls==[171,16416] and cores[0]==684 and stats==dict(calls=171,query_calls=342,rows=16416,grad_calls=0),'replay work')
    require(x.c.base.fingerprint(model)==fingerprint and trainer.hook_snapshot(model)==hooks,'replay preservation')
    record.update(checkpoint_roundtrip=True,reload_max_error=b.replay_error(record['raw'],raw,data,cx),replay_policy_receipt=dict(stats),
        replay_forward_calls=171,replay_row_presentations=16416,replay_core_forward_calls=684)
    print(f'[C326] seed={record["seed"]} arm={record["arm"]} checkpoint_replay=PASS',flush=True)


def fixed_gate(rows):
    require([r['seed'] for r in rows]==list(SEEDS),'gate seed inventory'); flags=[]
    for r in rows:
        require(type(r['candidate_interior_pass']) is bool and type(r['candidate_retention_pass']) is bool,'gate flags')
        require(all(type(r[k]) is int for k in ('original_answer_gain','original_pair_gain','interior_answer_gain','interior_pair_gain')),'gate counts')
        flags.append(r['candidate_interior_pass'] and r['candidate_retention_pass'] and r['interior_answer_gain']>0 and
                     r['interior_pair_gain']>0 and r['original_answer_gain']>=0 and r['original_pair_gain']>=0)
    return all(flags),flags


def analyze(records,data,cx):
    b=base(); x=cx[-1]; require([(r['seed'],r['arm']) for r in records]==identities(),'complete paired cohort')
    metrics=[]; results=[]
    for r in records:
        check_fit(r['fit'],r['seed'],r['arm'],data['TRAIN'],x); b.validate_raw(r['raw'],data,cx)
        require(r['readout_policy']=='mean_last' and r['checkpoint_roundtrip'] is True and r['initial_sha256']!=r['final_sha256'] and
                r['core_initial_sha256']!=r['core_final_sha256'],'record state')
        require(r['policy_receipt']==dict(calls=1371,query_calls=2742,rows=74016,grad_calls=1200) and
                r['replay_policy_receipt']==dict(calls=171,query_calls=342,rows=16416,grad_calls=0),'policy receipts')
        fields=('forward_calls','row_presentations','core_forward_calls','replay_forward_calls','replay_row_presentations','replay_core_forward_calls')
        require(all(type(r[k]) is int for k in fields) and tuple(r[k] for k in fields)==(1371,74016,5484,171,16416,684),'work receipt')
        require(type(r['reload_max_error']) in (int,float) and math.isfinite(r['reload_max_error']) and 0<=r['reload_max_error']<=1e-9,'replay bound')
        original={str(n):x.wide.score_length(data,r['raw']['original'][str(n)],x.c) for n in range(2,7)}
        inside=cx[2].score_new(r['raw']['interior'],data,x)
        require(all(type(v['passed']) is bool for v in (*original.values(),inside)),'scorer flags')
        results.append(dict(seed=r['seed'],arm=r['arm'],original_pass={n:v['passed'] for n,v in original.items()},
            retention_pass=all(v['passed'] for v in original.values()),interior_pass=inside['passed']))
        single={split:{v:int((z.argmax(1)==torch.tensor([d['target'] for d in data[split]])).sum())
            for v,z in r['raw']['original']['1'][split]['repeat'].items()} for split in ('TRAIN','HOLDOUT')}
        metrics.append(dict(seed=r['seed'],arm=r['arm'],original=original,interior=inside,single_character=single))
    pairs=[]
    for i,seed in enumerate(SEEDS):
        a,c=records[2*i:2*i+2]
        require(all(a[k]==c[k] for k in ('initial_sha256','core_initial_sha256')) and torch.equal(a['fit']['schedule_events'],c['fit']['schedule_events'])
                and a['fit']['family_exposure']==c['fit']['family_exposure'],'paired state/order/exposure')
        inside=b.heldout_contrast(a['raw']['interior']['HOLDOUT'],c['raw']['interior']['HOLDOUT'],data['HOLDOUT'])
        old={}
        for n in range(2,7):
            adapted=[{ip:r['raw']['original'][str(n)]['HOLDOUT'][op] for op,ip in zip(PROFILES,b.templates.INTERIOR_PROFILES,strict=True)} for r in (a,c)]
            old[str(n)]=b.heldout_contrast(*adapted,data['HOLDOUT'])
        pairs.append(dict(seed=seed,candidate_interior_pass=results[2*i+1]['interior_pass'],candidate_retention_pass=results[2*i+1]['retention_pass'],
            control_interior_pass=results[2*i]['interior_pass'],control_retention_pass=results[2*i]['retention_pass'],
            original_answer_gain=sum(v['answer_gain'] for v in old.values()),original_pair_gain=sum(v['query_pair_gain'] for v in old.values()),
            interior_answer_gain=inside['answer_gain'],interior_pair_gain=inside['query_pair_gain'],interior=inside,original_by_length=old))
    gate,flags=fixed_gate(pairs)
    for row,flag in zip(pairs,flags,strict=True): row['paired_success']=flag
    return metrics,dict(candidate_gate=gate,paired_success_count=sum(flags),seed_results=results,paired_comparisons=pairs,
        all_pairs_matched=True,all_replays=True,all_family_exposures_matched=True,**WORK)


def load_bundle(path):
    value=torch.load(path,map_location='cpu',weights_only=True)
    require(set(value)=={'schema','identities','readout_policy','states'} and value['schema']=='fold-c326-models-v1' and
            value['identities']==[list(v) for v in identities()] and value['readout_policy']=='mean_last' and len(value['states'])==10,'C326 model bundle')
    return value['states']


def run_science(out,data,old,new,cx,root,pins):
    b=base(); prepared=previous().training(data,old,new,cx); tables={k:v[0] for k,v in prepared.items()}; targets=prepared['original'][1]
    records=[]; states=[]
    for seed in SEEDS:
        models=make_models(seed,cx[-1]); events=schedule(seed,data['TRAIN'],cx[-1])
        for arm in ARMS:
            b.check_dependencies(root,pins,cx,models[arm]); r,state=train_one(models[arm],tables,targets,events,data,old,new,seed,arm,cx)
            records.append(r); states.append(state)
    torch.save(dict(schema='fold-c326-models-v1',identities=[list(v) for v in identities()],readout_policy='mean_last',states=states),out/'trained-models.pt')
    saved=load_bundle(out/'trained-models.pt')
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,cx[-1])
        for j,arm in enumerate(ARMS): replay(models[arm],saved[2*i+j],records[2*i+j],data,old,new,cx)
    metrics,summary=analyze(records,data,cx)
    torch.save(dict(schema='fold-c326-evaluations-v1',records=records),out/'evaluations.pt')
    for name,value in zip((OUTPUTS[0],OUTPUTS[1],OUTPUTS[2],OUTPUTS[3],OUTPUTS[6],OUTPUTS[7]),(manifest(),data,old,new,metrics,summary),strict=True):
        with (out/name).open('xb') as stream: stream.write(blob(value))
    return summary


def semantic_recheck(out,data,old,new,cx,read_json):
    b=base(); archive=torch.load(out/'evaluations.pt',map_location='cpu',weights_only=True)
    require(set(archive)=={'schema','records'} and archive['schema']=='fold-c326-evaluations-v1','evaluation schema')
    states=load_bundle(out/'trained-models.pt')
    require([b.state_digest(v) for v in states]==[r['saved_state_sha256'] for r in archive['records']],'saved checkpoint tensors')
    metrics,summary=analyze(archive['records'],data,cx)
    for name,value in zip((OUTPUTS[0],OUTPUTS[1],OUTPUTS[2],OUTPUTS[3],OUTPUTS[6],OUTPUTS[7]),(manifest(),data,old,new,metrics,summary),strict=True):
        require(blob(read_json(out/name))==blob(value),'saved semantic reconstruction:'+name)
    return metrics,summary


def runtime_preflight(data,old,new,cx,root,pins):
    b=base(); prepared=previous().training(data,old,new,cx)
    for seed in SEEDS:
        events=schedule(seed,data['TRAIN'],cx[-1]); a=family_mask(events,'epoch4'); z=family_mask(events,'batch4')
        require(torch.equal(a[:,0],previous().families(events,'mixed4')),'C325 control rule parity')
        require(exposure(events,a)==exposure(events,z),'preflight exact exposure')
        print(f'[C326 allocation] seed={seed} exact_pair_profile_exposure=PASS mixed_updates=400',flush=True)
    models=make_models(SEEDS[0],cx[-1]); ids=[next(i for i,r in enumerate(data['TRAIN']) if r['language']==lang) for lang in ('en','ja')]
    for arm in ARMS:
        model=models[arm]; b.check_dependencies(root,pins,cx,model)
        with torch.no_grad():
            w=model.read.output.weight; w.copy_(torch.sin(torch.arange(w.numel(),dtype=torch.float64).reshape_as(w))*.03)
        for family in ('original','interior4'):
            tokens=prepared[family][0][4,'repeat'][ids]; model.eval()
            with torch.no_grad():
                expected=model(tokens,torch.zeros(2,dtype=torch.int64))
                with cx[-2].trained_readout(model,cx[-1].wide,'mean_last'): actual=model(tokens,torch.zeros(2,dtype=torch.int64))
            require(torch.equal(expected,actual),'native readout parity')
            model.train(); model.zero_grad(set_to_none=True)
            with cx[-2].trained_readout(model,cx[-1].wide,'mean_last'):
                F.cross_entropy(model(tokens,torch.zeros(2,dtype=torch.int64)),prepared[family][1][ids]).backward()
            require(model.read.query.weight.grad is not None and all(p.grad is None or bool(torch.isfinite(p.grad).all()) for p in model.parameters()),'native TRAIN backward')
    print('C326_native_TRAIN_and_gradient_preflight = PASS; scientific_training_started = False',flush=True)
