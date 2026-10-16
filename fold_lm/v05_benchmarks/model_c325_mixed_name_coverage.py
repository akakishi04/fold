"""C325: paired interior-only versus half-original length-four TRAIN coverage.

The accepted C324 module supplies native architecture helpers and unchanged
scorers. No accepted module globals, model forward, or old verdicts are patched.
"""
from __future__ import annotations
import copy
import hashlib
import importlib
import itertools
import json
import math
from pathlib import Path
import torch
from torch.nn import functional as F

EXPERIMENT_ID = 'C325-v5b-mixed-name-coverage'
STAGE = 'V5-B-MIXED-NAME-COVERAGE'
SEEDS = tuple(range(325001, 325006))
ORDERS = tuple(range(325101, 325106))
ARMS = ('interior4', 'mixed4')
PROFILES = ('repeat', 'shared_prefix', 'shared_suffix')
STEPS = 1200
FIT_RNG = 612000
OWN = ('fold_lm/v05_benchmarks/model_c325_mixed_name_coverage.py',
       'tools/c325_execution.py', 'tests_lm/test_v05_c325_mixed_name_coverage.py',
       'tools/run_c325.ps1', 'tools/invoke_c325.ps1',
       'docs/experiment-ledger-addendum-c325-preregistration.md')
OUTPUTS = ('experiment-plan.json', 'dataset.json', 'original-prompts.json',
           'interior-prompts.json', 'trained-models.pt', 'evaluations.pt',
           'measurements.json', 'validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 56, 5546, 214
SOURCE_COUNT, INPUT_COUNT = 808, 1517
WORK = dict(models=10, train_steps=12000, training_rows=576000,
            model_forward_calls=15420, row_presentations=904320,
            core_forward_calls=61680, model_state_loads=10,
            checkpoint_bundle_loads=1, new_checkpoint_writes=1, network_calls=0)
MANIFEST_SHA = '03ed2ba1d2d2951087c70ce41ddf39756674a30ac4cef56671e158eb80fff3d0'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def base():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c324_interior_coverage_training')


def identities():
    return list(itertools.product(SEEDS, ARMS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE,
        acceptance_base='6c3198793f0f6b852fa96be125323763cbfdddde',
        parent_execution='fcef3d5833c31d51e261ce578209bd5acd73f59c',
        parent_summary_sha256='21e752a51809a9b400c798b24c4ff405105458965b54610cfa16f71a349fbbdd',
        parent_envelope_sha256='2c6013d9b4f33fb20e79e68946ad8596d756d23694d7d04508fcd0ca0e3040c3',
        question='does half-original length4 TRAIN coverage recover original retention while preserving interior binding at equal total budget',
        arms=list(ARMS), seeds=list(SEEDS), orders=list(ORDERS),
        changed='only length4 template family: all interior versus alternating complete length4 epochs old/interior starting old',
        held='paired fresh initial weights,logical rows,targets,pair order,length/profile schedule,optimizer,precision,steps,native mean_last',
        length4_epochs=100, mixed4_original_epochs=50, mixed4_interior_epochs=50,
        per_row_length_exposure=[0,100,100,100], train_lengths=[2,3,4],
        length4_family='same family for all 192 rows of each complete epoch;never split a query pair',
        parameters=14256, core_parameters=3328, slots=64, readout='native mean_last',
        steps_per_model=1200, rows_per_step=48, fit_rng=FIT_RNG,
        optimizer='AdamW betas .9/.999 eps1e-8 weight_decay0;global gradient clip1',
        core_lr=.0005, other_lr=.005, loss='ordinary mean CE',
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        primary='ALL5 mixed4 interior gates AND original2..6 gates;positive pooled original2..6 HOLDOUT answer AND pair gains;nonnegative interior HOLDOUT answer AND pair gains against paired interior4',
        comparison='report every length/profile/language/TRAIN/HOLDOUT cell and rescued/regressed counts;never select seeds',
        boundary='seen template families and reused logical split;not unseen-template generalization,statistical independence,Gate F,or production adoption',
        original_single='length1 descriptive only',
        dtype='CPU float64', threads=2, deterministic=True, replay_tolerance=1e-9,
        internal_steps_per_forward=4, raw_logit_payload_bytes=336199680,
        source_pins=SOURCE_COUNT, protected_inputs=INPUT_COUNT,
        inherited_sources=802, inherited_inputs=1501, immediate_parent_files=10,
        own_tests=OWN_TESTS, focused_tests=FULL_TESTS, modules=MODULES,
        exclusion='inherited single C204 mutable-control-state test;no new exclusions',
        parent_validation='rehash all inherited inputs and fixed summary/envelope;reconstruct immediate C324 metrics from saved logits/states;do not refit or recursively reexecute older semantic validators',
        execution='native read leases throughout worker;full regression separate unmodified process;fresh output/envelope byte verifier',
        console='streamed test dots,suite-ID digest,compact domain minima/totals;complete cell metrics remain local hashed artifacts',
        outputs=list(OUTPUTS), work_scope='child fitting/evaluation/ten model replays only;preflight,software tests,parent and saved semantic verification separate',
        gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C325 manifest seal')


def validate_schedule(events):
    require(isinstance(events,torch.Tensor) and events.dtype == torch.int64
            and events.device.type == 'cpu' and events.shape == (STEPS,24,4), 'schedule shape/dtype')
    for epoch in range(STEPS//4):
        e = events[4*epoch:4*epoch+4]
        require(bool((e[:,:,:2] == e[0,0,:2]).all()), 'epoch length/profile changes')
        require(int(e[0,0,0]) in (2,3,4) and int(e[0,0,1]) in (0,1,2), 'schedule domain')
        require(sorted(e[:,:,2:].flatten().tolist()) == list(range(192)), 'incomplete epoch')
    for length in (2,3,4):
        chosen = events[events[:,:,0] == length][:,2:].flatten()
        require(torch.equal(torch.bincount(chosen,minlength=192),torch.full((192,),100,dtype=torch.int64)), 'length exposure')


def schedule(seed, rows, x):
    require(type(seed) is int and seed in SEEDS and len(rows)==192, 'fresh schedule identity')
    events = x.parent.plan_for_order(ORDERS[SEEDS.index(seed)],'two_to_four',rows,x.p312,x.pairs)
    validate_schedule(events)
    return events


def families(events, arm):
    require(arm in ARMS, 'unregistered arm')
    validate_schedule(events)
    result = torch.zeros(STEPS,dtype=torch.int64)
    ordinal = 0
    for epoch in range(STEPS//4):
        if int(events[4*epoch,0,0]) == 4:
            result[4*epoch:4*epoch+4] = 1 if arm=='interior4' else ordinal%2
            ordinal += 1
    require(ordinal == 100 and int(result.sum()) == (400 if arm=='interior4' else 200), 'family allocation')
    return result


def family_stats(events, selected):
    require(selected.shape==(STEPS,) and selected.dtype==torch.int64
            and bool(((selected==0)|(selected==1)).all()), 'family schedule')
    rows = {}
    for length in (2,3,4):
        for family in (0,1):
            mask = (events[:,0,0]==length)&(selected==family)
            ids = events[mask,:,2:].flatten()
            rows[f'{length}:{family}'] = torch.bincount(ids,minlength=192).tolist()
    return dict(family_schedule_sha256=digest(selected.tolist()),family_row_exposures=rows)


def make_models(seed, x):
    require(type(seed) is int and seed in SEEDS, 'fresh model seed')
    c = x.c
    reference = c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    template = x.wide.LengthReadout(reference)
    models = {arm:x.policy.configure(copy.deepcopy(template),'core_slow') for arm in ARMS}
    pointers = set()
    for m in models.values():
        require(type(m) is x.wide.LengthReadout and m.backbone.config.max_tokens==64
                and m.backbone.core.config.slots==64, 'native architecture')
        require(sum(p.numel() for p in m.parameters())==14256
                and sum(p.numel() for p in m.backbone.core.parameters())==3328, 'capacity')
        require(c.base.fingerprint(m)==c.base.fingerprint(reference)
                and list(m.state_dict())==list(reference.state_dict()), 'paired initialization')
        require(all(p.requires_grad and p.dtype==torch.float64 and p.device.type=='cpu' for p in m.parameters()), 'precision')
        current={p.data_ptr() for p in m.parameters()}
        require(not current&pointers,'shared model storage'); pointers.update(current)
        x.policy.parameter_groups(m,'core_slow')
    return models


def training(data, old, new, cx):
    b=base()
    views=b.training_views(data['TRAIN'],{str(n):old[str(n)]['TRAIN'] for n in (2,3,4)},new['TRAIN'])
    result={name:b.tensor_tables(views[name],cx[-1].wide) for name in ('original','interior4')}
    require(torch.equal(result['original'][1],result['interior4'][1]),'teacher alignment')
    return result


def train_steps(model, tables, targets, events, selected, x):
    """Numeric loop; formal fit validates its complete fixed input before entry."""
    torch.manual_seed(FIT_RNG)
    opt=x.policy.optimizer_for(model,'core_slow')
    model.train(); losses=[]; rates=[]; counts=[]; union={}
    for step,e in enumerate(events):
        x.policy.verify_optimizer(opt,model,'core_slow')
        rates.append([g['lr'] for g in opt.param_groups]); opt.zero_grad(set_to_none=True)
        length,profile=map(int,e[0,:2]); ids=e[:,2:].flatten()
        source=tables['interior4' if int(selected[step]) else 'original']
        z=model(source[length,PROFILES[profile]][ids],torch.zeros(len(ids),dtype=torch.int64))
        x.c.p267.check_logits(z,len(ids)); loss=F.cross_entropy(z,targets[ids])
        require(bool(torch.isfinite(loss)),'nonfinite training loss'); losses.append(float(loss.detach()))
        loss.backward()
        received={n:p.numel() for n,p in model.named_parameters() if p.grad is not None}
        union.update(received); counts.append(sum(received.values()))
        torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True); opt.step()
        if (step+1)%200==0:
            print(f'[C325] step={step+1}/{len(events)} ce={losses[-1]:.6f}',flush=True)
    model.eval()
    return dict(ce_history=losses,optimizer_group_lrs=rates,gradient_parameter_counts=counts,gradient_union=dict(sorted(union.items())))


def fit(model, tables, targets, events, arm, x):
    selected=families(events,arm)
    require(set(tables)=={'original','interior4'} and targets.shape==(192,)
            and targets.dtype==torch.int64,'training inputs')
    keys=set(itertools.product((2,3,4),PROFILES))
    for table in tables.values():
        require(set(table)==keys and all(z.shape==(192,64) and z.dtype==torch.int64
                and z.device.type=='cpu' for z in table.values()),'training tables')
    trace=train_steps(model,tables,targets,events,selected,x)
    return dict(steps=STEPS,training_rows=57600,fit_rng=FIT_RNG,optimizer_creations=1,
        trainable_parameters=14256,schedule_events=events.clone(),template_events=selected.clone(),
        **trace,**x.parent.schedule_stats(events),**family_stats(events,selected))


def check_fit(trace, seed, arm, rows, x):
    e=schedule(seed,rows,x); f=families(e,arm)
    expected=dict(steps=STEPS,training_rows=57600,fit_rng=FIT_RNG,optimizer_creations=1,trainable_parameters=14256)
    require(all(type(trace[k]) is int and trace[k]==v for k,v in expected.items()),'fit budget')
    require(torch.equal(trace['schedule_events'],e) and torch.equal(trace['template_events'],f),'saved schedule')
    require(all(trace[k]==v for k,v in {**x.parent.schedule_stats(e),**family_stats(e,f)}.items()),'saved exposures')
    require(trace['optimizer_group_lrs']==[[.005,.0005]]*STEPS and len(trace['ce_history'])==STEPS
            and all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in trace['ce_history']),'fit numeric trace')
    union=trace['gradient_union']; counts=trace['gradient_parameter_counts']
    require(union and all(type(k) is str and type(v) is int and v>0 for k,v in union.items())
            and 0<sum(union.values())<=14256,'gradient union')
    require(len(counts)==STEPS and all(type(v) is int and 0<v<=sum(union.values()) for v in counts),'gradient counts')


def train_one(model, tables, targets, events, data, old, new, seed, arm, cx):
    b=base(); trainer,x=cx[-2:]; c=x.c
    initial,core_initial=c.base.fingerprint(model),c.base.fingerprint(model.backbone.core)
    hooks=trainer.hook_snapshot(model)
    print(f'[C325] seed={seed} arm={arm} phase=training',flush=True)
    with c.p267.counted(model,c.core) as (calls,cores),trainer.trained_readout(model,x.wide,'mean_last') as stats:
        trained=fit(model,tables,targets,events,arm,x)
        final,core_final=c.base.fingerprint(model),c.base.fingerprint(model.backbone.core)
        model.requires_grad_(False)
        raw=b.evaluate(model,data,old,new,cx)
    require(calls==[1371,74016] and cores[0]==5484 and stats==dict(calls=1371,query_calls=2742,rows=74016,grad_calls=1200),'train/eval work')
    require(initial!=final and core_initial!=core_final and c.base.fingerprint(model)==final
            and trainer.hook_snapshot(model)==hooks,'learned/preserved state')
    r=dict(seed=seed,arm=arm,readout_policy='mean_last',initial_sha256=initial,core_initial_sha256=core_initial,
        final_sha256=final,core_final_sha256=core_final,fit=trained,raw=raw,policy_receipt=dict(stats),
        forward_calls=1371,row_presentations=74016,core_forward_calls=5484)
    state={n:z.detach().cpu().clone() for n,z in model.state_dict().items()}
    r['saved_state_sha256']=b.state_digest(state)
    return r,state


def replay(model, state, record, data, old, new, cx):
    b=base(); trainer,x=cx[-2:]
    require(list(state)==list(model.state_dict()) and all(state[k].shape==v.shape and state[k].dtype==v.dtype
            for k,v in model.state_dict().items()),'checkpoint schema')
    require(b.state_digest(state)==record['saved_state_sha256'],'checkpoint digest')
    model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(False)
    fingerprint=x.c.base.fingerprint(model); hooks=trainer.hook_snapshot(model)
    require(fingerprint==record['final_sha256'],'checkpoint fingerprint')
    with x.c.p267.counted(model,x.c.core) as (calls,cores),trainer.trained_readout(model,x.wide,'mean_last') as stats:
        raw=b.evaluate(model,data,old,new,cx)
    require(calls==[171,16416] and cores[0]==684 and stats==dict(calls=171,query_calls=342,rows=16416,grad_calls=0),'replay work')
    require(x.c.base.fingerprint(model)==fingerprint and trainer.hook_snapshot(model)==hooks,'replay preservation')
    record.update(checkpoint_roundtrip=True,reload_max_error=b.replay_error(record['raw'],raw,data,cx),
        replay_policy_receipt=dict(stats),replay_forward_calls=171,replay_row_presentations=16416,replay_core_forward_calls=684)
    print(f'[C325] seed={record["seed"]} arm={record["arm"]} checkpoint_replay=PASS',flush=True)


def fixed_gate(rows):
    require([r['seed'] for r in rows]==list(SEEDS),'gate seed inventory')
    flags=[]
    for r in rows:
        require(type(r['candidate_interior_pass']) is bool and type(r['candidate_retention_pass']) is bool,'gate flags')
        fields=('original_answer_gain','original_pair_gain','interior_answer_gain','interior_pair_gain')
        require(all(type(r[k]) is int for k in fields),'gate counts')
        flags.append(r['candidate_interior_pass'] and r['candidate_retention_pass'] and
            r['original_answer_gain']>0 and r['original_pair_gain']>0 and
            r['interior_answer_gain']>=0 and r['interior_pair_gain']>=0)
    return all(flags),flags


def analyze(records, data, cx):
    b=base(); x=cx[-1]
    require([(r['seed'],r['arm']) for r in records]==identities(),'complete paired cohort')
    metrics=[]; results=[]
    for r in records:
        check_fit(r['fit'],r['seed'],r['arm'],data['TRAIN'],x); b.validate_raw(r['raw'],data,cx)
        require(r['readout_policy']=='mean_last' and r['checkpoint_roundtrip'] is True
                and r['initial_sha256']!=r['final_sha256'] and r['core_initial_sha256']!=r['core_final_sha256'],'record state')
        require(r['policy_receipt']==dict(calls=1371,query_calls=2742,rows=74016,grad_calls=1200)
                and r['replay_policy_receipt']==dict(calls=171,query_calls=342,rows=16416,grad_calls=0),'policy receipts')
        fields=('forward_calls','row_presentations','core_forward_calls','replay_forward_calls','replay_row_presentations','replay_core_forward_calls')
        require(all(type(r[k]) is int for k in fields) and tuple(r[k] for k in fields)==(1371,74016,5484,171,16416,684),'work receipt')
        require(type(r['reload_max_error']) in (int,float) and math.isfinite(r['reload_max_error'])
                and 0<=r['reload_max_error']<=1e-9,'replay bound')
        original={str(n):x.wide.score_length(data,r['raw']['original'][str(n)],x.c) for n in range(2,7)}
        interior=cx[2].score_new(r['raw']['interior'],data,x)
        require(all(type(v['passed']) is bool for v in (*original.values(),interior)),'scorer flags')
        results.append(dict(seed=r['seed'],arm=r['arm'],original_pass={n:v['passed'] for n,v in original.items()},
            retention_pass=all(v['passed'] for v in original.values()),interior_pass=interior['passed']))
        single={s:{v:int((z.argmax(1)==torch.tensor([d['target'] for d in data[s]])).sum())
                for v,z in r['raw']['original']['1'][s]['repeat'].items()} for s in ('TRAIN','HOLDOUT')}
        metrics.append(dict(seed=r['seed'],arm=r['arm'],original=original,interior=interior,single_character=single))
    pairs=[]
    for i,seed in enumerate(SEEDS):
        a,c=records[2*i:2*i+2]
        require(all(a[k]==c[k] for k in ('initial_sha256','core_initial_sha256'))
                and torch.equal(a['fit']['schedule_events'],c['fit']['schedule_events']),'paired initialization/schedule')
        inside=b.heldout_contrast(a['raw']['interior']['HOLDOUT'],c['raw']['interior']['HOLDOUT'],data['HOLDOUT'])
        old={}
        for n in range(2,7):
            adapted=[{ip:r['raw']['original'][str(n)]['HOLDOUT'][op]
                for op,ip in zip(PROFILES,b.templates.INTERIOR_PROFILES,strict=True)} for r in (a,c)]
            old[str(n)]=b.heldout_contrast(*adapted,data['HOLDOUT'])
        pairs.append(dict(seed=seed,candidate_interior_pass=results[2*i+1]['interior_pass'],
            candidate_retention_pass=results[2*i+1]['retention_pass'],
            control_interior_pass=results[2*i]['interior_pass'],control_retention_pass=results[2*i]['retention_pass'],
            original_answer_gain=sum(v['answer_gain'] for v in old.values()),
            original_pair_gain=sum(v['query_pair_gain'] for v in old.values()),
            interior_answer_gain=inside['answer_gain'],interior_pair_gain=inside['query_pair_gain'],
            interior=inside,original_by_length=old))
    gate,flags=fixed_gate(pairs)
    for row,flag in zip(pairs,flags,strict=True): row['paired_success']=flag
    return metrics,dict(candidate_gate=gate,paired_success_count=sum(flags),seed_results=results,
        paired_comparisons=pairs,all_pairs_matched=True,all_replays=True,**WORK)


def load_bundle(path):
    value=torch.load(path,map_location='cpu',weights_only=True)
    require(set(value)=={'schema','identities','readout_policy','states'} and
        value['schema']=='fold-c325-models-v1' and value['identities']==[list(v) for v in identities()]
        and value['readout_policy']=='mean_last' and len(value['states'])==10,'C325 model bundle')
    return value['states']


def run_science(out, data, old, new, cx, root, pins):
    b=base(); prepared=training(data,old,new,cx)
    tables={k:v[0] for k,v in prepared.items()}; targets=prepared['original'][1]
    records=[]; states=[]
    for seed in SEEDS:
        models=make_models(seed,cx[-1]); events=schedule(seed,data['TRAIN'],cx[-1])
        for arm in ARMS:
            b.check_dependencies(root,pins,cx,models[arm])
            record,state=train_one(models[arm],tables,targets,events,data,old,new,seed,arm,cx)
            records.append(record); states.append(state)
    torch.save(dict(schema='fold-c325-models-v1',identities=[list(v) for v in identities()],
                    readout_policy='mean_last',states=states),out/'trained-models.pt')
    saved=load_bundle(out/'trained-models.pt')
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,cx[-1])
        for j,arm in enumerate(ARMS): replay(models[arm],saved[2*i+j],records[2*i+j],data,old,new,cx)
    measurements,summary=analyze(records,data,cx)
    torch.save(dict(schema='fold-c325-evaluations-v1',records=records),out/'evaluations.pt')
    for name,value in zip((OUTPUTS[0],OUTPUTS[1],OUTPUTS[2],OUTPUTS[3],OUTPUTS[6],OUTPUTS[7]),
            (manifest(),data,old,new,measurements,summary),strict=True):
        with (out/name).open('xb') as stream: stream.write(blob(value))
    return summary


def semantic_recheck(out, data, old, new, cx, read_json):
    b=base(); archive=torch.load(out/'evaluations.pt',map_location='cpu',weights_only=True)
    require(set(archive)=={'schema','records'} and archive['schema']=='fold-c325-evaluations-v1','evaluation schema')
    states=load_bundle(out/'trained-models.pt')
    require([b.state_digest(s) for s in states]==[r['saved_state_sha256'] for r in archive['records']],'saved checkpoint tensors')
    metrics,summary=analyze(archive['records'],data,cx)
    for name,value in zip((OUTPUTS[0],OUTPUTS[1],OUTPUTS[2],OUTPUTS[3],OUTPUTS[6],OUTPUTS[7]),
            (manifest(),data,old,new,metrics,summary),strict=True):
        require(blob(read_json(out/name))==blob(value),'saved semantic reconstruction:'+name)
    return metrics,summary


def runtime_preflight(data, old, new, cx, root, pins):
    b=base(); prepared=training(data,old,new,cx)
    for seed in SEEDS:
        events=schedule(seed,data['TRAIN'],cx[-1])
        for arm in ARMS: families(events,arm)
    models=make_models(SEEDS[0],cx[-1])
    ids=[next(i for i,r in enumerate(data['TRAIN']) if r['language']==language) for language in ('en','ja')]
    for arm in ARMS:
        model=models[arm]; b.check_dependencies(root,pins,cx,model)
        with torch.no_grad():
            w=model.read.output.weight; w.copy_(torch.sin(torch.arange(w.numel(),dtype=torch.float64).reshape_as(w))*.03)
        for family in ('original','interior4'):
            tokens=prepared[family][0][4,'repeat'][ids]
            model.eval()
            with torch.no_grad():
                expected=model(tokens,torch.zeros(2,dtype=torch.int64))
                with cx[-2].trained_readout(model,cx[-1].wide,'mean_last'):
                    actual=model(tokens,torch.zeros(2,dtype=torch.int64))
            require(torch.equal(expected,actual),'native mean_last parity')
            model.train(); model.zero_grad(set_to_none=True)
            with cx[-2].trained_readout(model,cx[-1].wide,'mean_last'):
                F.cross_entropy(model(tokens,torch.zeros(2,dtype=torch.int64)),prepared[family][1][ids]).backward()
            require(model.read.query.weight.grad is not None and all(p.grad is None or bool(torch.isfinite(p.grad).all())
                    for p in model.parameters()),'native TRAIN backward')
    print('C325_native_TRAIN_and_gradient_preflight = PASS; scientific_training_started = False',flush=True)
