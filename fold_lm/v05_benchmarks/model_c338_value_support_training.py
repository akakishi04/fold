"""C338: paired native training with a fixed supplied-value mass penalty."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import math
import re
import torch
from torch.nn import functional as F

EXPERIMENT_ID = 'C338-v5b-value-support-training'
STAGE = 'V5-B-VALUE-SUPPORT-TRAINING'
SEEDS = tuple(range(338001, 338006))
ORDERS = tuple(range(338101, 338106))
ARMS = ('native', 'support_loss')
CYCLE, STEPS, FIT_RNG = 1200, 2400, 612000
RATES = (.005, .0005)
DOMAINS = tuple('original'+str(n) for n in range(2,7))+('interior4',)
OWN = ('fold_lm/v05_benchmarks/model_c338_value_support_training.py',
       'tools/c338_execution.py', 'tests_lm/test_v05_c338_value_support_training.py',
       'tools/run_c338.ps1', 'tools/invoke_c338.ps1',
       'docs/experiment-ledger-addendum-c338-preregistration.md')
OUTPUTS = ('experiment-plan.json','training-traces.json','trained-models.pt',
           'evaluations.pt','measurements.json','validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 48, 6170, 228
SOURCE_COUNT, INPUT_COUNT = 889, 5296
WORK = dict(training_models=10,evaluation_models=10,checkpoint_states=10,
    optimizer_creations=10,train_steps=24000,gradient_calls=24000,optimizer_steps=24000,
    training_rows=1152000,model_forward_calls=27420,row_presentations=1480320,
    core_forward_calls=109680,query_projection_calls=54840,model_state_loads=20,
    checkpoint_bundle_loads=1,new_checkpoint_writes=1,network_calls=0)
MANIFEST_SHA = 'd2c6bcbadfa3f04c35cad137fece59c9499f8b5de37589425479b05376b9fe73'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def previous():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c332_trained_first_mean_query')


def audit():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c337_saved_value_support')


def identities():
    return list(itertools.product(SEEDS,ARMS))


def coefficient(arm):
    require(type(arm) is str and arm in ARMS,'registered arm')
    return 0. if arm == 'native' else 1.


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,
        acceptance_base='8b7cdc54a7a735320617e1650cd349efb5850288',
        parent_execution='aae0a83742d56df9dcfe059f3b6ad81e26798505',
        parent_summary='415784b8d7d468a6d3f102775e29ae887fcb01ebc5718abef35dc9439fd6a0b8',
        parent_envelope='12df1d44c5973f9bb5ac7bd2ce766b4bf1fb5204bb3d064c44d6a9f09c7b237e',
        question='does extra TRAIN supplied-value mass supervision reduce outside-pair errors without sacrificing within-pair binding or existing gates',
        seeds=list(SEEDS),orders=list(ORDERS),arms=list(ARMS),cycle=CYCLE,steps=STEPS,fit_rng=FIT_RNG,rates=list(RATES),
        coefficients={a:coefficient(a) for a in ARMS},
        objective='mean CE256(target)+alpha*mean(logsumexp(all256)-logsumexp(two TRAIN supplied values));alpha0 returns exact CE',
        decomposition='CE256=support_NLL+within_pair_CE;alpha1 doubles support_NLL,does not add an independent information source',
        held='paired fresh weights,TRAIN rows/events/family masks,2400updates,core_slow AdamW,native readout in train/evaluation,architecture/scorers/thresholds',
        support='sorted two distinct0..3 byte classes from TRAIN row values;query/order invariant;never a forward argument or inference filter',
        schedule='C326 batch4/two_to_four,1200events repeated twice;no original5/6 TRAIN names;one optimizer/no intermediate evaluation',
        optimizer='noncore.005/core.0005;AdamW betas.9/.999 eps1e-8 decay0/globalclip1;no learning-rate compensation for larger objective',
        gate='all5candidate full gates;each seed/domain nonnegative HOLDOUT correct/pair gains and nonincreasing outside errors;strict total correct AND pair gains AND fewer outside errors',
        saturation='no strict gain exception for perfect controls;ties may yield valid negative',
        thresholds=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,both_order=.80),
        parameters=14256,core_parameters=3328,slots=64,precision='cpu float64',threads=2,
        evaluation_policy='native_before;all256 raw argmax;no support labels in model input or readout',
        preflight='discarded native model,original/interior en+ja,6forwards/12rows/4backward/0updates;all5schedules',
        boundary='hypothesis only;loss reweighting can alter clipping and updates;within-pair errors need not improve;no C335bad-seed removal or old-weight reuse',
        source_count=SOURCE_COUNT,input_count=INPUT_COUNT,parent_files=463,own_tests=OWN_TESTS,
        full_tests=FULL_TESTS,modules=MODULES,outputs=list(OUTPUTS),raw_logit_payload_bytes=672399360,
        gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA,'C338 manifest seal')


def support_labels(train_rows, y):
    require(type(train_rows) is list and len(train_rows) == 192 and isinstance(y,torch.Tensor)
            and y.shape == (192,) and y.dtype == torch.int64 and y.device.type == 'cpu','TRAIN support shape')
    pairs = []
    for r,target in zip(train_rows,y.tolist(),strict=True):
        values = r['values']
        require(type(values) is list and len(values) == 2 and all(type(v) is int and 0 <= v < 4 for v in values)
                and values[0] != values[1] and target == r['target'] == 48+values[r['entities'].index(r['query'])], 'TRAIN value semantics')
        pairs.append(sorted(48+v for v in values))
    return torch.tensor(pairs,dtype=torch.int64)


def objective(logits, targets, supplied, alpha):
    require(type(alpha) is float and alpha in (0.,1.),'fixed support coefficient')
    require(isinstance(logits,torch.Tensor) and logits.ndim == 2 and logits.shape[1] == 256
            and len(logits) > 0 and logits.dtype == torch.float64 and logits.device.type == 'cpu'
            and bool(torch.isfinite(logits).all()),'finite TRAIN logits')
    n = len(logits)
    require(isinstance(targets,torch.Tensor) and targets.shape == (n,) and targets.dtype == torch.int64
            and targets.device.type == 'cpu' and isinstance(supplied,torch.Tensor) and supplied.shape == (n,2)
            and supplied.dtype == torch.int64 and supplied.device.type == 'cpu','support label types')
    require(bool(((supplied >= 48)&(supplied <= 51)).all()) and bool((supplied[:,0] < supplied[:,1]).all())
            and bool((supplied == targets[:,None]).any(1).all()),'two sorted supplied values/target containment')
    ce = F.cross_entropy(logits,targets)
    support = (torch.logsumexp(logits,1)-torch.logsumexp(logits.gather(1,supplied),1)).mean()
    total = ce if alpha == 0. else ce+support
    require(all(bool(torch.isfinite(v)) and float(v.detach()) >= 0 for v in (ce,support,total)),'finite nonnegative loss')
    return total,ce,support


def make_model(seed, x):
    require(type(seed) is int and seed in SEEDS,'fresh C338 seed')
    c = x.c
    ref = c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    model = x.policy.configure(x.wide.LengthReadout(ref),'core_slow')
    require(type(model) is x.wide.LengthReadout and model.backbone.config.max_tokens == 64
            and model.backbone.core.config.slots == 64,'native architecture')
    require(sum(v.numel() for v in model.parameters()) == 14256
            and sum(v.numel() for v in model.backbone.core.parameters()) == 3328,'capacity')
    require(c.base.fingerprint(model) == c.base.fingerprint(ref) and list(model.state_dict()) == list(ref.state_dict()),'native initialization')
    require(all(v.requires_grad and v.dtype == torch.float64 and v.device.type == 'cpu' for v in model.parameters()),'precision/gradient')
    x.policy.parameter_groups(model,'core_slow'); return model


def make_pair(seed, x):
    models = {arm:make_model(seed,x) for arm in ARMS}; p = previous()
    require(p.state_hash(models['native'].state_dict()) == p.state_hash(models['support_loss'].state_dict()),'paired initial weights')
    ptrs = [{v.data_ptr() for v in m.parameters() if v.numel()} for m in models.values()]
    require(not ptrs[0]&ptrs[1],'independent paired storage'); return models


def schedule(seed, rows, x):
    require(type(seed) is int and seed in SEEDS and len(rows) == 192,'TRAIN schedule identity')
    curriculum = previous().source().curriculum()
    events = x.parent.plan_for_order(ORDERS[SEEDS.index(seed)],'two_to_four',rows,x.p312,x.pairs)
    curriculum.validate_schedule(events); return events,curriculum.family_mask(events,'batch4')


def training_hash(tables,y,supplied,events,mask):
    return previous().state_hash(dict(base=previous().training_fingerprint(tables,y,events,mask),supplied=supplied))


def optimize(model, arm, tables, y, supplied, events, mask, x):
    p = previous(); alpha = coefficient(arm)
    require(len(events) == len(mask) == CYCLE and STEPS == 2*CYCLE,'registered cycles')
    torch.manual_seed(FIT_RNG); opt = x.policy.optimizer_for(model,'core_slow'); opt_id = id(opt)
    initial = p.state_hash(model.state_dict()); core_initial = p.state_hash(model.backbone.core.state_dict())
    losses,rates,counts,indices = [],[],[],[]; union = {}; boundary = None; continuation = None
    receipt = dict(calls=0,query_calls=0,rows=0,grad_calls=0); model.train()
    with torch.enable_grad():
        for step in range(STEPS):
            if step == CYCLE:
                continuation = dict(weights=p.state_hash(model.state_dict()),optimizer=p.state_hash(opt.state_dict()))
                require(continuation == boundary,'optimizer/weight reset')
            require(id(opt) == opt_id,'optimizer replaced'); x.policy.verify_optimizer(opt,model,'core_slow')
            rate = [g['lr'] for g in opt.param_groups]; require(rate == list(RATES),'fixed rates'); rates.append(rate)
            index = step%CYCLE; indices.append(index); opt.zero_grad(set_to_none=True)
            tokens,ids = p.source().curriculum().select_tokens(tables,events[index],mask[index]); require(len(ids) == 48,'TRAIN batch')
            with p.readouts().readout(model,x.wide,'native_before') as stats:
                logits = model(tokens,torch.zeros(len(ids),dtype=torch.int64)); x.c.p267.check_logits(logits,len(ids))
                total,ce,support = objective(logits,y[ids],supplied[ids],alpha)
                losses.append(dict(total=float(total.detach()),ce=float(ce.detach()),support=float(support.detach())))
                total.backward()
            require(stats == dict(calls=1,query_calls=2,rows=48,grad_calls=1),'one native TRAIN forward')
            for k in receipt: receipt[k] += stats[k]
            got = {name:v.numel() for name,v in model.named_parameters() if v.grad is not None}
            require(got,'missing gradients'); counts.append(sum(got.values())); union.update(got)
            torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True); opt.step()
            if step+1 == CYCLE: boundary = dict(weights=p.state_hash(model.state_dict()),optimizer=p.state_hash(opt.state_dict()))
            if (step+1)%200 == 0:
                print(f'[C338] arm={arm} step={step+1}/{STEPS} ce={losses[-1]["ce"]:.6f} support={losses[-1]["support"]:.6f}',flush=True)
    model.eval(); require(boundary is not None and boundary == continuation,'continuous optimizer')
    require(receipt == dict(calls=STEPS,query_calls=2*STEPS,rows=48*STEPS,grad_calls=STEPS),'TRAIN receipt')
    state = {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    require(p.state_hash(state) == p.state_hash(model.state_dict()) and all(v.numel() == 0 or state[k].data_ptr() != v.data_ptr()
            for k,v in model.state_dict().items()),'deep checkpoint')
    return dict(arm=arm,coefficient=alpha,steps=STEPS,initial_sha256=initial,final_sha256=p.state_hash(state),
        core_initial_sha256=core_initial,core_final_sha256=p.state_hash(model.backbone.core.state_dict()),
        loss_history=losses,optimizer_group_lrs=rates,gradient_parameter_counts=counts,gradient_union=dict(sorted(union.items())),
        event_indices=indices,policy_receipt=receipt,boundary=boundary,continuation=continuation,
        optimizer_creations=1,intermediate_evaluations=0),state


def train_one(seed, arm, model, tables, y, supplied, rows, cx, root, pins):
    p = previous(); x = cx[-1]; p.source().base().check_dependencies(root,pins,cx,model)
    events,mask = schedule(seed,rows,x); before = training_hash(tables,y,supplied,events,mask)
    print(f'[C338] seed={seed} arm={arm} phase=training',flush=True)
    with x.c.p267.counted(model,x.c.core) as (calls,cores):
        trace,state = optimize(model,arm,tables,y,supplied,events,mask,x)
    require(calls == [2400,115200] and cores[0] == 9600,'measured TRAIN work')
    require(training_hash(tables,y,supplied,events,mask) == before,'TRAIN input mutation')
    trace.update(seed=seed,training_input_sha256=before,support_sha256=digest(supplied.tolist()),
        schedule_sha256=digest(events.tolist()),mask_sha256=digest(mask.tolist()),
        family_exposure_per_cycle=p.source().curriculum().exposure(events,mask))
    return trace,state


def check_trace(t, rows, x):
    require(type(t['seed']) is int and t['seed'] in SEEDS and t['arm'] in ARMS,'trace identity')
    alpha = coefficient(t['arm']); events,mask = schedule(t['seed'],rows,x)
    y = torch.tensor([r['target'] for r in rows],dtype=torch.int64)
    require(type(t['coefficient']) is float and t['coefficient'] == alpha and t['support_sha256'] == digest(support_labels(rows,y).tolist()),'support provenance')
    require(type(t['steps']) is int and t['steps'] == STEPS and t['event_indices'] == list(range(CYCLE))*2
            and all(type(v) is int for v in t['event_indices']),'event budget/order')
    require(t['schedule_sha256'] == digest(events.tolist()) and t['mask_sha256'] == digest(mask.tolist())
            and t['family_exposure_per_cycle'] == previous().source().curriculum().exposure(events,mask),'exposure')
    require(t['optimizer_group_lrs'] == [list(RATES)]*STEPS and len(t['loss_history']) == STEPS,'rates/loss history')
    for r in t['loss_history']:
        require(set(r) == {'total','ce','support'} and all(type(v) is float and math.isfinite(v) and v >= 0 for v in r.values())
                and r['total'] == (r['ce'] if alpha == 0. else r['ce']+r['support']),'loss arithmetic')
    union,counts = t['gradient_union'],t['gradient_parameter_counts']
    require(union and all(type(k) is str and type(v) is int and v > 0 for k,v in union.items()) and 0 < sum(union.values()) <= 14256
            and len(counts) == STEPS and all(type(v) is int and 0 < v <= sum(union.values()) for v in counts),'gradient inventory')
    for k in ('initial_sha256','final_sha256','core_initial_sha256','core_final_sha256','training_input_sha256'):
        require(type(t[k]) is str and re.fullmatch('[0-9a-f]{64}',t[k]),'state/input fingerprint')
    require(t['initial_sha256'] != t['final_sha256'] and t['core_initial_sha256'] != t['core_final_sha256'],'trained state')
    require(t['boundary'] == t['continuation'] and set(t['boundary']) == {'weights','optimizer'}
            and all(type(v) is str and re.fullmatch('[0-9a-f]{64}',v) for v in t['boundary'].values()),'continued state')
    require(type(t['optimizer_creations']) is int and t['optimizer_creations'] == 1 and type(t['intermediate_evaluations']) is int
            and t['intermediate_evaluations'] == 0 and t['policy_receipt'] == dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400),'no restart/selection')


def support_report(raw, data):
    reports = {}
    for domain in DOMAINS:
        rows = data['HOLDOUT']; target = [r['target'] for r in rows]
        other = [48+r['values'][1-r['entities'].index(r['query'])] for r in rows]; items = []
        tree = raw['interior'] if domain == 'interior4' else raw['original'][domain[-1]]
        for profile in audit().parent().profiles(domain):
            items.extend(audit().audit_logits(tree['HOLDOUT'][profile]['normal'],target,other))
        counts = {k:sum(r['kind'] == k for r in items) for k in audit().KINDS}
        require(len(items) == 288,'support report denominator')
        reports[domain] = dict(answers=288,**counts)
    return reports


def fixed_gate(pairs):
    require([r['seed'] for r in pairs] == list(SEEDS) and all(type(r['seed']) is int for r in pairs),'all paired seeds')
    eligible = []
    for r in pairs:
        require(type(r['candidate_full_pass']) is bool and set(r['domains']) == set(DOMAINS)
                and all(all(type(z[k]) is int for k in ('answer_gain','query_pair_gain','outside_gain')) for z in r['domains'].values()),'gate domains/types')
        eligible.append(r['candidate_full_pass'] and all(z['answer_gain'] >= 0 and z['query_pair_gain'] >= 0
            and z['outside_gain'] <= 0 for z in r['domains'].values()))
    strict = (sum(z['answer_gain'] for r in pairs for z in r['domains'].values()) > 0
              and sum(z['query_pair_gain'] for r in pairs for z in r['domains'].values()) > 0
              and sum(z['outside_gain'] for r in pairs for z in r['domains'].values()) < 0)
    return all(eligible) and strict,eligible


def check_summary(v):
    require(all(type(v[k]) is int and v[k] == n for k,n in WORK.items()) and v['paired_conditions_valid'] is True
            and v['all_replays'] is True and v['evaluation_policy'] == 'native_before','work/integrity')
    require([(r['seed'],r['arm']) for r in v['seed_results']] == identities() and len(v['paired_comparisons']) == 5,'cohort')
    for i,pair in enumerate(v['paired_comparisons']):
        require(set(pair['domains']) == set(DOMAINS),'all domain comparisons')
        for offset,key in ((0,'control_full_pass'),(1,'candidate_full_pass')):
            f = v['seed_results'][2*i+offset]
            require(set(f['original_pass']) == set(map(str,range(2,7))) and all(type(b) is bool for b in f['original_pass'].values())
                    and type(f['interior_pass']) is bool and f['retention_pass'] is all(f['original_pass'].values())
                    and pair[key] is (f['retention_pass'] and f['interior_pass']),'full gate binding')
            require(set(f['support']) == set(DOMAINS),'support domains')
            for d,r in f['support'].items():
                require(set(r) == {'answers',*audit().KINDS} and r['answers'] == 288 and type(r['answers']) is int
                        and all(type(r[k]) is int and r[k] >= 0 for k in audit().KINDS)
                        and sum(r[k] for k in audit().KINDS) == 288,'support partition')
        for d,z in pair['domains'].items():
            previous().contrast_check({k:w for k,w in z.items() if k != 'outside_gain'})
            require(type(z['outside_gain']) is int,'outside count type')
            a,b = [v['seed_results'][2*i+j]['support'][d] for j in (0,1)]
            require(z['control_correct'] == a['correct'] and z['candidate_correct'] == b['correct']
                    and z['outside_gain'] == b['absent_digit']+b['outside_catalog']-a['absent_digit']-a['outside_catalog'],'support/contrast binding')
    gate,eligible = fixed_gate(v['paired_comparisons'])
    require(v['candidate_gate'] is gate and type(v['eligible_seed_count']) is int and v['eligible_seed_count'] == sum(eligible),'fixed gate')


def analyze(traces, records, states, data, cx):
    p = previous(); q = p.readouts()
    require([(t['seed'],t['arm']) for t in traces] == [(r['seed'],r['arm']) for r in records] == identities()
            and len(states) == 10,'complete trained cohort')
    metrics,flags = [],[]
    for t,r,state in zip(traces,records,states,strict=True):
        check_trace(t,data['TRAIN'],cx[-1])
        require(set(r) == {'seed','arm','state_sha256','evaluation_policy','raw','receipts'}
                and r['state_sha256'] == t['final_sha256'] == p.state_hash(state) and r['evaluation_policy'] == 'native_before'
                and set(r['raw']) == set(r['receipts']) == {'evaluation','replay'},'state binding')
        for mode in ('evaluation','replay'):
            p.source().base().validate_raw(r['raw'][mode],data,cx)
            require(blob(r['receipts'][mode]) == blob(dict(calls=171,query_calls=342,rows=16416,grad_calls=0)),'evaluation receipt')
        require(p.source().base().replay_error(r['raw']['evaluation'],r['raw']['replay'],data,cx) <= 1e-9,'saved replay')
        score,f = q.summarize_mode(r['raw']['evaluation'],data,cx)
        metrics.append(dict(seed=t['seed'],arm=t['arm'],score=score))
        flags.append(dict(seed=t['seed'],arm=t['arm'],support=support_report(r['raw']['evaluation'],data),**f))
    pairs = []
    for i,seed in enumerate(SEEDS):
        a,b = traces[2*i:2*i+2]
        require(all(a[k] == b[k] for k in ('initial_sha256','core_initial_sha256','training_input_sha256','support_sha256',
            'schedule_sha256','mask_sha256','family_exposure_per_cycle','event_indices','optimizer_group_lrs')),'paired conditions')
        compare = q.compare(records[2*i]['raw']['evaluation'],records[2*i+1]['raw']['evaluation'],data,p.source().base())
        domains = {}
        for d in DOMAINS:
            z = compare['interior'] if d == 'interior4' else compare['original_by_length'][d[-1]]
            old,new = [flags[2*i+j]['support'][d] for j in (0,1)]
            domains[d] = dict(**z,outside_gain=new['absent_digit']+new['outside_catalog']-old['absent_digit']-old['outside_catalog'])
        pairs.append(dict(seed=seed,control_full_pass=flags[2*i]['retention_pass'] and flags[2*i]['interior_pass'],
            candidate_full_pass=flags[2*i+1]['retention_pass'] and flags[2*i+1]['interior_pass'],domains=domains))
    gate,eligible = fixed_gate(pairs)
    value = dict(candidate_gate=gate,eligible_seed_count=sum(eligible),paired_conditions_valid=True,all_replays=True,
        evaluation_policy='native_before',seed_results=flags,paired_comparisons=pairs,**WORK)
    check_summary(value); return metrics,value


def load_states(path):
    v = torch.load(path,map_location='cpu',weights_only=True)
    require(set(v) == {'schema','identities','states'} and v['schema'] == 'fold-c338-trained-models-v1'
            and v['identities'] == [list(z) for z in identities()] and len(v['states']) == 10,'model bundle')
    return v['states']


def run_training(out, data_out, cx, root, pins, read):
    p = previous(); data,old,new = p.load_data(data_out,read); before = digest((data,old,new))
    tables,y = p.prepared(data,old,new,cx); supplied = support_labels(data['TRAIN'],y); traces,states = [],[]
    for seed in SEEDS:
        models = make_pair(seed,cx[-1])
        for arm in ARMS:
            trace,state = train_one(seed,arm,models[arm],tables,y,supplied,data['TRAIN'],cx,root,pins)
            traces.append(trace); states.append(state)
        del models
    with (out/'trained-models.pt').open('xb') as stream:
        torch.save(dict(schema='fold-c338-trained-models-v1',identities=[list(z) for z in identities()],states=states),stream)
    saved = load_states(out/'trained-models.pt'); require([p.state_hash(v) for v in saved] == [p.state_hash(v) for v in states],'checkpoint roundtrip')
    records = []
    for (seed,arm),state in zip(identities(),saved,strict=True):
        model = make_model(seed,cx[-1]); p.source().base().check_dependencies(root,pins,cx,model)
        model.eval(); model.requires_grad_(False); raw,receipts = {},{}
        for kind in ('evaluation','replay'):
            model.load_state_dict(state,strict=True); require(p.state_hash(model.state_dict()) == p.state_hash(state),'loaded state')
            raw[kind],receipts[kind] = p.readouts().measure(model,'native_before',data,old,new,cx)
            require(p.state_hash(model.state_dict()) == p.state_hash(state),'evaluation weight mutation')
        records.append(dict(seed=seed,arm=arm,state_sha256=p.state_hash(state),evaluation_policy='native_before',raw=raw,receipts=receipts))
        print(f'[C338] seed={seed} arm={arm} native_saved_evaluation_and_replay=COMPLETE',flush=True)
    metrics,value = analyze(traces,records,saved,data,cx); require(digest((data,old,new)) == before,'data/prompt mutation')
    with (out/'evaluations.pt').open('xb') as stream: torch.save(dict(schema='fold-c338-evaluations-v1',records=records),stream)
    for name,item in (('experiment-plan.json',manifest()),('training-traces.json',traces),('measurements.json',metrics),('validation-summary.json',value)):
        with (out/name).open('xb') as stream: stream.write(blob(item))
    return value


def semantic_recheck(out, data_out, cx, read):
    data,_,_ = previous().load_data(data_out,read)
    archive = torch.load(out/'evaluations.pt',map_location='cpu',weights_only=True)
    require(set(archive) == {'schema','records'} and archive['schema'] == 'fold-c338-evaluations-v1','evaluation schema')
    metrics,value = analyze(read(out/'training-traces.json'),archive['records'],load_states(out/'trained-models.pt'),data,cx)
    for name,item in (('experiment-plan.json',manifest()),('measurements.json',metrics),('validation-summary.json',value)):
        require(blob(read(out/name)) == blob(item),'saved training reconstruction:'+name)
    return value


def native_preflight(data_out, cx, root, pins, read):
    p = previous(); x = cx[-1]; data,old,new = p.load_data(data_out,read)
    tables,y = p.prepared(data,old,new,cx); supplied = support_labels(data['TRAIN'],y)
    for seed in SEEDS: schedule(seed,data['TRAIN'],x)
    model = make_model(SEEDS[0],x); p.source().base().check_dependencies(root,pins,cx,model)
    with torch.no_grad():
        w = model.read.output.weight; w.copy_(torch.sin(torch.arange(w.numel(),dtype=torch.float64).reshape_as(w))*.03)
    initial = p.state_hash(model.state_dict()); ids = [next(i for i,r in enumerate(data['TRAIN']) if r['language'] == lang) for lang in ('en','ja')]
    for family in ('original','interior4'):
        tokens = tables[family][4,'repeat'][ids]; tasks = torch.zeros(2,dtype=torch.int64); model.train()
        with torch.no_grad(): expected = model(tokens,tasks)
        for arm in ARMS:
            model.zero_grad(set_to_none=True)
            with torch.enable_grad(),p.readouts().readout(model,x.wide,'native_before') as stats:
                logits = model(tokens,tasks); p.readouts().same(expected,logits.detach())
                objective(logits,y[ids],supplied[ids],coefficient(arm))[0].backward()
            require(stats == dict(calls=1,query_calls=2,rows=2,grad_calls=1) and model.read.query.weight.grad is not None
                    and all(v.grad is None or bool(torch.isfinite(v.grad).all()) for v in model.parameters()),'native backward')
    require(p.state_hash(model.state_dict()) == initial,'preflight changed weights')
    print('C338_native_preflight=PASS;schedules=5;forwards=6;rows=12;backward=4;updates=0',flush=True)
