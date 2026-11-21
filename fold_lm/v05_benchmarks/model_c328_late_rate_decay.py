"""C328: fixed late learning-rate attenuation on the immutable C326 batch4 curriculum."""
from __future__ import annotations
import copy
import hashlib
import importlib
import itertools
import json
import math
import re
import torch
from torch.nn import functional as F

EXPERIMENT_ID='C328-v5b-late-rate-decay'
STAGE='V5-B-LATE-RATE-DECAY'
SEEDS=tuple(range(328001,328006))
ORDERS=tuple(range(328101,328106))
ARMS=('constant','late_tenth')
PROFILES=('repeat','shared_prefix','shared_suffix')
STEPS,SWITCH,FIT_RNG=1200,800,612000
RATES=(.005,.0005)
OWN=('fold_lm/v05_benchmarks/model_c328_late_rate_decay.py','tools/c328_execution.py',
     'tests_lm/test_v05_c328_late_rate_decay.py','tools/run_c328.ps1','tools/invoke_c328.ps1',
     'docs/experiment-ledger-addendum-c328-preregistration.md')
OUTPUTS=('experiment-plan.json','dataset.json','original-prompts.json','interior-prompts.json',
         'trained-models.pt','evaluations.pt','measurements.json','validation-summary.json')
OWN_TESTS,FULL_TESTS,MODULES=64,5722,217
SOURCE_COUNT,INPUT_COUNT=826,1561
WORK=dict(models=10,train_steps=12000,training_rows=576000,model_forward_calls=15420,
          row_presentations=904320,core_forward_calls=61680,model_state_loads=10,
          checkpoint_bundle_loads=1,new_checkpoint_writes=1,network_calls=0)
MANIFEST_SHA='75f3de53837dcc64127b72f541ded650436b3a6ac46686bd9d8ff2aa8b89a226'


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def previous(): return importlib.import_module('fold_lm.v05_benchmarks.model_c326_mixing_granularity')


def base(): return previous().base()


def identities(): return list(itertools.product(SEEDS,ARMS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base='d96e7ff66f76463e6fe39ca159e687f7d26d2011',
        parent_execution='847c924f50303d93ed4df7acec74b77209b7d261',
        parent_summary_sha256='c4a061e158a1bd617fb7638bb034b7aa3ef78da06b15062474ff986d1f347719',
        parent_envelope_sha256='fb44749ce38e0b0909238c51c13bbb1eb95e1898369313fb34d95483a543e535',
        question='does a fixed final-third LR reduction improve interior binding while retaining original2..6 under batch4 mixing',
        seeds=list(SEEDS),orders=list(ORDERS),arms=list(ARMS),steps=STEPS,switch_after_completed_updates=SWITCH,
        late_factor=.1,base_rates=list(RATES),late_rates=[v*.1 for v in RATES],fit_rng=FIT_RNG,
        changed='only both optimizer group learning rates for updates801..1200;no optimizer recreation or moment reset',
        held='C326 batch4 exact pair/profile family exposure,logical order,targets,paired initialization,first800updates,capacity,budget,optimizer other settings',
        curriculum='unchanged C326 family_mask(events,batch4);old4/interior4 each50 per row;old2/old3 each100',
        parameters=14256,core_parameters=3328,slots=64,readout='native mean_last',rows_per_update=48,
        optimizer='native C308 core_slow AdamW;betas.9/.999 eps1e-8 decay0;globalclip1;ordinary mean CE',
        boundary_receipt='identical full state/optimizer hashes and first800CE between arms;moment hash unchanged across LR assignment',
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        primary='ALL5 late_tenth pass full interior and original2..6 gates;positive interior HOLDOUT answer AND pair gains;nonnegative pooled original2..6 gains in both counts',
        boundary='prospective LR policy,not a C327 causal conclusion;seen templates,reused logical split;no seed selection or threshold/ratio/budget search',
        dtype='CPU float64',threads=2,deterministic=True,replay_tolerance=1e-9,original_single='length1 descriptive only',
        source_pins=SOURCE_COUNT,protected_inputs=INPUT_COUNT,inherited_sources=820,inherited_inputs=1549,
        immediate_parent_files=6,own_tests=OWN_TESTS,focused_tests=FULL_TESTS,modules=MODULES,
        exclusion='sole inherited C204 mutable-ACTIVE test;no new exclusions',outputs=list(OUTPUTS),
        raw_logit_payload_bytes=336199680,work_scope='child fitting/evaluation/ten replays only;preflight/tests/verification separately scoped',
        parent_semantics='C327 gradient archive reconstructed against exact inherited C326 outputs;no recursive older semantic bodies',
        gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal(): require(digest(manifest())==MANIFEST_SHA,'C328 manifest seal')


def state_hash(value):
    """Typed canonical fingerprint, including tensor dtype/shape/bytes and optimizer state."""
    h=hashlib.sha256()
    def put(tag,data): h.update(tag); h.update(str(len(data)).encode()+b':'); h.update(data)
    def visit(v):
        if isinstance(v,torch.Tensor):
            z=v.detach().cpu().contiguous(); require(bool(torch.isfinite(z).all()),'nonfinite state')
            put(b'T',blob([str(z.dtype),list(z.shape)])); put(b'B',z.numpy().tobytes())
        elif isinstance(v,dict):
            require(all(type(k) in (str,int) for k in v),'state key')
            put(b'D',str(len(v)).encode())
            for k in sorted(v,key=lambda k:(type(k).__name__,str(k))): visit(k); visit(v[k])
        elif isinstance(v,(tuple,list)):
            put(b'Q' if isinstance(v,tuple) else b'L',str(len(v)).encode())
            for x in v: visit(x)
        else: require(v is None or type(v) in (str,int,float,bool),'state value'); put(b'J',blob(v))
    visit(value)
    return h.hexdigest()


def rates_for(arm,step):
    require(arm in ARMS and type(step) is int and 0<=step<STEPS,'rate identity')
    return tuple(v*(.1 if arm=='late_tenth' and step>=SWITCH else 1.) for v in RATES)


def optimizer_contract(opt,model):
    require(type(opt) is torch.optim.AdamW and len(opt.param_groups)==2,'native two-group AdamW')
    named=list(model.named_parameters()); core={id(p) for p in model.backbone.core.parameters()}
    require(core=={id(p) for n,p in named if n.startswith('backbone.core.')},'core boundary')
    wanted=[[id(p) for _,p in named if id(p) not in core],[id(p) for _,p in named if id(p) in core]]
    require(all(p.requires_grad for _,p in named) and all(wanted),'active groups')
    groups=[]
    for i,g in enumerate(opt.param_groups):
        require([id(p) for p in g['params']]==wanted[i] and g['lr']==RATES[i] and
                g['betas']==(.9,.999) and g['eps']==1e-8 and g['weight_decay']==0.,'initial optimizer contract')
        groups.append(dict(ids=wanted[i],settings=blob({k:v for k,v in g.items() if k not in ('params','lr')})))
    return dict(identity=id(opt),groups=groups,defaults=blob(opt.defaults))


def verify_optimizer(opt,contract,rates):
    require(id(opt)==contract['identity'] and len(opt.param_groups)==2 and blob(opt.defaults)==contract['defaults'],'optimizer replaced/defaults changed')
    for g,c,lr in zip(opt.param_groups,contract['groups'],rates,strict=True):
        require([id(p) for p in g['params']]==c['ids'] and
                blob({k:v for k,v in g.items() if k not in ('params','lr')})==c['settings'] and
                type(g['lr']) is float and g['lr']==lr,'optimizer policy changed')


def assign_rates(opt,contract,arm,step):
    before=state_hash(opt.state_dict()['state'])
    for group,rate in zip(opt.param_groups,rates_for(arm,step),strict=True): group['lr']=rate
    verify_optimizer(opt,contract,rates_for(arm,step))
    after=state_hash(opt.state_dict()['state']); require(before==after,'moment reset at rate switch')
    return dict(before=before,after=after,optimizer_preserved=True)


def schedule(seed,rows,x):
    require(type(seed) is int and seed in SEEDS and len(rows)==192,'fresh schedule identity')
    e=x.parent.plan_for_order(ORDERS[SEEDS.index(seed)],'two_to_four',rows,x.p312,x.pairs)
    previous().validate_schedule(e)
    return e


def make_models(seed,x):
    require(type(seed) is int and seed in SEEDS,'fresh model identity'); c=x.c
    ref=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    template=x.wide.LengthReadout(ref); models={a:x.policy.configure(copy.deepcopy(template),'core_slow') for a in ARMS}; used=set()
    for m in models.values():
        require(type(m) is x.wide.LengthReadout and m.backbone.config.max_tokens==64 and m.backbone.core.config.slots==64,'native architecture')
        require(sum(z.numel() for z in m.parameters())==14256 and sum(z.numel() for z in m.backbone.core.parameters())==3328,'capacity')
        require(c.base.fingerprint(m)==c.base.fingerprint(ref) and list(m.state_dict())==list(ref.state_dict()),'paired initialization')
        require(all(z.requires_grad and z.dtype==torch.float64 and z.device.type=='cpu' for z in m.parameters()),'precision')
        ptr={z.data_ptr() for z in m.parameters()}; require(not used&ptr,'shared storage'); used.update(ptr)
        x.policy.parameter_groups(m,'core_slow')
    return models


def optimize(model,tables,targets,events,mask,arm,x):
    """Same CE/clip/AdamW arithmetic; only explicit group lr assignment changes."""
    require(arm in ARMS and len(events)==len(mask)==STEPS,'registered workload')
    p=previous(); torch.manual_seed(FIT_RNG); opt=x.policy.optimizer_for(model,'core_slow')
    x.policy.verify_optimizer(opt,model,'core_slow'); contract=optimizer_contract(opt,model)
    model.train(); losses=[]; rates=[]; counts=[]; union={}; boundary=None; switch=None
    for step,(ev,selected) in enumerate(zip(events,mask,strict=True)):
        if step==SWITCH:
            boundary=dict(weights=state_hash(model.state_dict()),optimizer=state_hash(opt.state_dict()))
            switch=assign_rates(opt,contract,arm,step)
        verify_optimizer(opt,contract,rates_for(arm,step)); rates.append([g['lr'] for g in opt.param_groups])
        opt.zero_grad(set_to_none=True); tokens,ids=p.select_tokens(tables,ev,selected)
        z=model(tokens,torch.zeros(len(ids),dtype=torch.int64)); x.c.p267.check_logits(z,len(ids))
        loss=F.cross_entropy(z,targets[ids]); require(bool(torch.isfinite(loss)),'finite loss'); losses.append(float(loss.detach()))
        loss.backward(); got={n:q.numel() for n,q in model.named_parameters() if q.grad is not None}; union.update(got); counts.append(sum(got.values()))
        torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True); opt.step()
        if (step+1)%200==0: print(f'[C328] arm={arm} step={step+1}/{STEPS} ce={losses[-1]:.6f} lr={rates[-1]}',flush=True)
    model.eval(); require(boundary is not None and switch is not None,'switch unvisited')
    return dict(ce_history=losses,optimizer_group_lrs=rates,gradient_parameter_counts=counts,
                gradient_union=dict(sorted(union.items())),boundary=boundary,switch=switch,optimizer_creations=1)


def fit(model,tables,targets,events,arm,x):
    p=previous(); mask=p.family_mask(events,'batch4'); keys=set(itertools.product((2,3,4),PROFILES))
    require(set(tables)=={'original','interior4'} and targets.shape==(192,) and targets.dtype==torch.int64,'training inputs')
    require(all(set(t)==keys and all(v.shape==(192,64) and v.dtype==torch.int64 and v.device.type=='cpu' for v in t.values()) for t in tables.values()),'training tables')
    trace=optimize(model,tables,targets,events,mask,arm,x)
    return dict(steps=STEPS,training_rows=57600,fit_rng=FIT_RNG,trainable_parameters=14256,
        schedule_events=events.clone(),template_pair_events=mask.clone(),family_exposure=p.exposure(events,mask),
        family_schedule_sha256=digest(mask.tolist()),**trace,**x.parent.schedule_stats(events))


def check_fit(trace,seed,arm,rows,x):
    p=previous(); e=schedule(seed,rows,x); mask=p.family_mask(e,'batch4')
    for k,v in dict(steps=1200,training_rows=57600,fit_rng=FIT_RNG,trainable_parameters=14256,optimizer_creations=1).items():
        require(type(trace[k]) is int and trace[k]==v,'fit metadata:'+k)
    require(torch.equal(trace['schedule_events'],e) and torch.equal(trace['template_pair_events'],mask),'saved curriculum')
    require(trace['family_exposure']==p.exposure(e,mask) and trace['family_schedule_sha256']==digest(mask.tolist()),'saved family exposure')
    require(all(trace[k]==v for k,v in x.parent.schedule_stats(e).items()),'saved logical exposure')
    require(trace['optimizer_group_lrs']==[list(rates_for(arm,i)) for i in range(STEPS)],'saved exact rate trace')
    require(len(trace['ce_history'])==STEPS and all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in trace['ce_history']),'CE trace')
    u=trace['gradient_union']; counts=trace['gradient_parameter_counts']
    require(u and all(type(k) is str and type(v) is int and v>0 for k,v in u.items()) and 0<sum(u.values())<=14256,'gradient union')
    require(len(counts)==STEPS and all(type(v) is int and 0<v<=sum(u.values()) for v in counts),'gradient trace')
    require(set(trace['boundary'])=={'weights','optimizer'} and all(re.fullmatch('[0-9a-f]{64}',v) for v in trace['boundary'].values()),'boundary hashes')
    switch=trace['switch']; require(switch['before']==switch['after'] and re.fullmatch('[0-9a-f]{64}',switch['before']) and switch['optimizer_preserved'] is True,'switch moment preservation')


def check_pair(a,c):
    require(all(a[k]==c[k] for k in ('initial_sha256','core_initial_sha256')),'paired initialization')
    x,y=a['fit'],c['fit']
    require(torch.equal(x['schedule_events'],y['schedule_events']) and torch.equal(x['template_pair_events'],y['template_pair_events']) and x['family_exposure']==y['family_exposure'],'paired curriculum')
    require(x['boundary']==y['boundary'] and x['ce_history'][:SWITCH]==y['ce_history'][:SWITCH] and x['switch']['before']==y['switch']['before'],'first800 paired state/optimizer mismatch')


def train_one(model,tables,y,events,data,old,new,seed,arm,cx):
    b=base(); trainer,x=cx[-2:]; c=x.c
    initial,ci=c.base.fingerprint(model),c.base.fingerprint(model.backbone.core); hooks=trainer.hook_snapshot(model)
    print(f'[C328] seed={seed} arm={arm} phase=training',flush=True)
    with c.p267.counted(model,c.core) as (calls,cores),trainer.trained_readout(model,x.wide,'mean_last') as stats:
        trace=fit(model,tables,y,events,arm,x); final,cf=c.base.fingerprint(model),c.base.fingerprint(model.backbone.core)
        model.requires_grad_(False); raw=b.evaluate(model,data,old,new,cx)
    require(calls==[1371,74016] and cores[0]==5484 and stats==dict(calls=1371,query_calls=2742,rows=74016,grad_calls=1200),'fit/eval work')
    require(initial!=final and ci!=cf and c.base.fingerprint(model)==final and trainer.hook_snapshot(model)==hooks,'learned/preserved state')
    state={n:v.detach().cpu().clone() for n,v in model.state_dict().items()}
    return dict(seed=seed,arm=arm,readout_policy='mean_last',initial_sha256=initial,core_initial_sha256=ci,final_sha256=final,
        core_final_sha256=cf,fit=trace,raw=raw,policy_receipt=dict(stats),forward_calls=1371,row_presentations=74016,
        core_forward_calls=5484,saved_state_sha256=b.state_digest(state)),state


def replay(model,state,r,data,old,new,cx):
    b=base(); trainer,x=cx[-2:]
    require(list(state)==list(model.state_dict()) and all(state[k].shape==v.shape and state[k].dtype==v.dtype for k,v in model.state_dict().items()),'checkpoint schema')
    require(b.state_digest(state)==r['saved_state_sha256'],'checkpoint digest'); model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(False)
    fp=x.c.base.fingerprint(model); hooks=trainer.hook_snapshot(model); require(fp==r['final_sha256'],'checkpoint fingerprint')
    with x.c.p267.counted(model,x.c.core) as (calls,cores),trainer.trained_readout(model,x.wide,'mean_last') as stats: raw=b.evaluate(model,data,old,new,cx)
    require(calls==[171,16416] and cores[0]==684 and stats==dict(calls=171,query_calls=342,rows=16416,grad_calls=0),'replay work')
    require(x.c.base.fingerprint(model)==fp and trainer.hook_snapshot(model)==hooks,'replay preservation')
    r.update(checkpoint_roundtrip=True,reload_max_error=b.replay_error(r['raw'],raw,data,cx),replay_policy_receipt=dict(stats),
        replay_forward_calls=171,replay_row_presentations=16416,replay_core_forward_calls=684)
    print(f'[C328] seed={r["seed"]} arm={r["arm"]} checkpoint_replay=PASS',flush=True)


def fixed_gate(rows):
    require([r['seed'] for r in rows]==list(SEEDS),'complete paired seeds'); flags=[]
    for r in rows:
        require(type(r['candidate_interior_pass']) is bool and type(r['candidate_retention_pass']) is bool,'gate flags')
        require(all(type(r[k]) is int for k in ('original_answer_gain','original_pair_gain','interior_answer_gain','interior_pair_gain')),'gate counts')
        flags.append(r['candidate_interior_pass'] and r['candidate_retention_pass'] and r['interior_answer_gain']>0 and r['interior_pair_gain']>0 and r['original_answer_gain']>=0 and r['original_pair_gain']>=0)
    return all(flags),flags


def analyze(records,data,cx):
    b=base(); x=cx[-1]; require([(r['seed'],r['arm']) for r in records]==identities(),'complete record cohort'); metrics=[]; results=[]
    for r in records:
        check_fit(r['fit'],r['seed'],r['arm'],data['TRAIN'],x); b.validate_raw(r['raw'],data,cx)
        require(r['readout_policy']=='mean_last' and r['checkpoint_roundtrip'] is True and r['initial_sha256']!=r['final_sha256'] and r['core_initial_sha256']!=r['core_final_sha256'],'record state')
        require(r['policy_receipt']==dict(calls=1371,query_calls=2742,rows=74016,grad_calls=1200) and r['replay_policy_receipt']==dict(calls=171,query_calls=342,rows=16416,grad_calls=0),'policy receipts')
        fields=('forward_calls','row_presentations','core_forward_calls','replay_forward_calls','replay_row_presentations','replay_core_forward_calls')
        require(all(type(r[k]) is int for k in fields) and tuple(r[k] for k in fields)==(1371,74016,5484,171,16416,684),'work receipt')
        require(type(r['reload_max_error']) in (int,float) and math.isfinite(r['reload_max_error']) and 0<=r['reload_max_error']<=1e-9,'replay bound')
        original={str(n):x.wide.score_length(data,r['raw']['original'][str(n)],x.c) for n in range(2,7)}; inside=cx[2].score_new(r['raw']['interior'],data,x)
        require(all(type(v['passed']) is bool for v in (*original.values(),inside)),'scorer flags')
        results.append(dict(seed=r['seed'],arm=r['arm'],original_pass={n:v['passed'] for n,v in original.items()},retention_pass=all(v['passed'] for v in original.values()),interior_pass=inside['passed']))
        single={split:{v:int((z.argmax(1)==torch.tensor([d['target'] for d in data[split]])).sum()) for v,z in r['raw']['original']['1'][split]['repeat'].items()} for split in ('TRAIN','HOLDOUT')}
        metrics.append(dict(seed=r['seed'],arm=r['arm'],original=original,interior=inside,single_character=single))
    pairs=[]
    for i,seed in enumerate(SEEDS):
        a,c=records[2*i:2*i+2]; check_pair(a,c); inside=b.heldout_contrast(a['raw']['interior']['HOLDOUT'],c['raw']['interior']['HOLDOUT'],data['HOLDOUT']); old={}
        for n in range(2,7):
            adapted=[{ip:r['raw']['original'][str(n)]['HOLDOUT'][op] for op,ip in zip(PROFILES,b.templates.INTERIOR_PROFILES,strict=True)} for r in (a,c)]
            old[str(n)]=b.heldout_contrast(*adapted,data['HOLDOUT'])
        pairs.append(dict(seed=seed,candidate_interior_pass=results[2*i+1]['interior_pass'],candidate_retention_pass=results[2*i+1]['retention_pass'],control_interior_pass=results[2*i]['interior_pass'],control_retention_pass=results[2*i]['retention_pass'],original_answer_gain=sum(v['answer_gain'] for v in old.values()),original_pair_gain=sum(v['query_pair_gain'] for v in old.values()),interior_answer_gain=inside['answer_gain'],interior_pair_gain=inside['query_pair_gain'],interior=inside,original_by_length=old,first800_matched=True))
    gate,flags=fixed_gate(pairs)
    for row,flag in zip(pairs,flags,strict=True): row['paired_success']=flag
    return metrics,dict(candidate_gate=gate,paired_success_count=sum(flags),seed_results=results,paired_comparisons=pairs,all_pairs_matched=True,all_replays=True,all_first800_matched=True,**WORK)


def load_bundle(path):
    v=torch.load(path,map_location='cpu',weights_only=True)
    require(set(v)=={'schema','identities','readout_policy','states'} and v['schema']=='fold-c328-models-v1' and v['identities']==[list(x) for x in identities()] and v['readout_policy']=='mean_last' and len(v['states'])==10,'model bundle')
    return v['states']


def run_science(out,data,old,new,cx,root,pins):
    b=base(); prepared=previous().previous().training(data,old,new,cx); tables={k:v[0] for k,v in prepared.items()}; y=prepared['original'][1]; records=[]; states=[]
    for seed in SEEDS:
        models=make_models(seed,cx[-1]); events=schedule(seed,data['TRAIN'],cx[-1])
        for arm in ARMS:
            b.check_dependencies(root,pins,cx,models[arm]); r,state=train_one(models[arm],tables,y,events,data,old,new,seed,arm,cx); records.append(r); states.append(state)
        check_pair(*records[-2:]); print(f'[C328] seed={seed} first800_weights_optimizer=IDENTICAL',flush=True)
    torch.save(dict(schema='fold-c328-models-v1',identities=[list(v) for v in identities()],readout_policy='mean_last',states=states),out/'trained-models.pt'); saved=load_bundle(out/'trained-models.pt')
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,cx[-1])
        for j,arm in enumerate(ARMS): replay(models[arm],saved[2*i+j],records[2*i+j],data,old,new,cx)
    metrics,summary=analyze(records,data,cx); torch.save(dict(schema='fold-c328-evaluations-v1',records=records),out/'evaluations.pt')
    for name,v in zip((OUTPUTS[0],OUTPUTS[1],OUTPUTS[2],OUTPUTS[3],OUTPUTS[6],OUTPUTS[7]),(manifest(),data,old,new,metrics,summary),strict=True):
        with (out/name).open('xb') as stream: stream.write(blob(v))
    return summary


def semantic_recheck(out,data,old,new,cx,read_json):
    b=base(); a=torch.load(out/'evaluations.pt',map_location='cpu',weights_only=True)
    require(set(a)=={'schema','records'} and a['schema']=='fold-c328-evaluations-v1','evaluation schema'); states=load_bundle(out/'trained-models.pt')
    require([b.state_digest(v) for v in states]==[r['saved_state_sha256'] for r in a['records']],'saved state digests')
    metrics,summary=analyze(a['records'],data,cx)
    for name,v in zip((OUTPUTS[0],OUTPUTS[1],OUTPUTS[2],OUTPUTS[3],OUTPUTS[6],OUTPUTS[7]),(manifest(),data,old,new,metrics,summary),strict=True): require(blob(read_json(out/name))==blob(v),'saved semantic reconstruction:'+name)
    return metrics,summary


def runtime_preflight(data,old,new,cx,root,pins):
    p=previous(); b=base(); prepared=p.previous().training(data,old,new,cx)
    for seed in SEEDS:
        ev=schedule(seed,data['TRAIN'],cx[-1]); p.family_mask(ev,'batch4')
        print(f'[C328 allocation] seed={seed} batch4=PASS',flush=True)
    trainer,x=cx[-2:]; m=make_models(SEEDS[0],x)['constant']; b.check_dependencies(root,pins,cx,m)
    with torch.no_grad():
        w=m.read.output.weight; w.copy_(torch.sin(torch.arange(w.numel(),dtype=torch.float64).reshape_as(w))*.03)
    ids=[next(i for i,r in enumerate(data['TRAIN']) if r['language']==language) for language in ('en','ja')]
    for family in ('original','interior4'):
        tokens=prepared[family][0][4,'repeat'][ids]; m.eval()
        with torch.no_grad():
            expected=m(tokens,torch.zeros(2,dtype=torch.int64))
            with trainer.trained_readout(m,x.wide,'mean_last'): actual=m(tokens,torch.zeros(2,dtype=torch.int64))
        require(torch.equal(expected,actual),'native readout parity'); m.train(); m.zero_grad(set_to_none=True)
        with trainer.trained_readout(m,x.wide,'mean_last'): F.cross_entropy(m(tokens,torch.zeros(2,dtype=torch.int64)),prepared[family][1][ids]).backward()
        require(m.read.query.weight.grad is not None and all(q.grad is None or bool(torch.isfinite(q.grad).all()) for q in m.parameters()),'native TRAIN backward')
    print('C328_native_preflight=PASS; forwards=6; backward=2; optimizer_steps=0; scientific_training_started=False',flush=True)
