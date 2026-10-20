"""C335: alternate TRAIN readouts at fixed budget; evaluate both arms natively."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import math
import re
import torch
from torch.nn import functional as F

EXPERIMENT_ID = 'C335-v5b-alternating-readout-training'
STAGE = 'V5-B-ALTERNATING-READOUT-TRAINING'
SEEDS = tuple(range(335001, 335006))
ORDERS = tuple(range(335101, 335106))
ARMS = ('native', 'alternating')
READOUTS = ('native_before', 'first_mean')
CYCLE, STEPS, FIT_RNG = 1200, 2400, 612000
RATES = (.005, .0005)
OWN = ('fold_lm/v05_benchmarks/model_c335_alternating_readout_training.py',
       'tools/c335_execution.py', 'tests_lm/test_v05_c335_alternating_readout_training.py',
       'tools/run_c335.ps1', 'tools/invoke_c335.ps1',
       'docs/experiment-ledger-addendum-c335-preregistration.md')
OUTPUTS = ('experiment-plan.json', 'training-traces.json', 'trained-models.pt',
           'evaluations.pt', 'measurements.json', 'validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 48, 6058, 225
SOURCE_COUNT, INPUT_COUNT = 871, 3893
WORK = dict(training_models=10, evaluation_models=10, checkpoint_states=10,
            optimizer_creations=10, train_steps=24000, gradient_calls=24000,
            optimizer_steps=24000, training_rows=1152000, model_forward_calls=27420,
            row_presentations=1480320, core_forward_calls=109680,
            query_projection_calls=54840, model_state_loads=20,
            checkpoint_bundle_loads=1, new_checkpoint_writes=1, network_calls=0)
MANIFEST_SHA = '946639b00b62504f89faf0c5a8a0b14fba375da031f1b17b11436a61b1ec48b0'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def previous():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c332_trained_first_mean_query')


def crossed():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c334_frozen_policy_crossover')


def identities():
    return list(itertools.product(SEEDS, ARMS))


def mode_at(arm, step):
    require(type(arm) is str and arm in ARMS and type(step) is int and 0 <= step < STEPS, 'registered arm/step')
    return READOUTS[0] if arm == 'native' else READOUTS[((step % CYCLE)+(step // CYCLE)) % 2]


def policy_plan(arm):
    require(CYCLE % 2 == 0 and STEPS == 2*CYCLE, 'two even cycles')
    modes = [mode_at(arm, step) for step in range(STEPS)]
    for i in range(CYCLE):
        require(sorted((modes[i], modes[CYCLE+i])) == sorted(READOUTS if arm == 'alternating' else (READOUTS[0],)*2), 'each event policy coverage')
    return modes


def policy_receipts(arm):
    modes = policy_plan(arm)
    return {mode:dict(calls=modes.count(mode), query_calls=2*modes.count(mode),
                      rows=48*modes.count(mode), grad_calls=modes.count(mode)) for mode in READOUTS}


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE,
        acceptance_base='6033993736efa1ed65e645fd0c11d801de25b15c',
        parent_execution='c6e9ead698ed053d2e96a93ff13febffb3d1b049',
        parent_summary='12130d6d096cd287a7f415108b5f71738bcc86d8ef439c7930ba4b0a390fbf81',
        parent_envelope='1efb6d154a4c617da3547e9fce3c22fc224caf36fa32aea81d00eabec6bbea68',
        question='does equal-budget alternating TRAIN readout exposure improve original6 while retaining other domains when BOTH arms evaluate with native mean/last',
        seeds=list(SEEDS), orders=list(ORDERS), arms=list(ARMS), cycle=CYCLE, steps=STEPS, fit_rng=FIT_RNG,
        changed='TRAIN readout schedule only: native throughout versus alternating native/first_mean with reversed parity in second cycle',
        held='paired fresh initial weights,all TRAIN examples/event order,batch4 family mask,2400updates,optimizer,learning rates,architecture,loss,evaluation native only,scorers/thresholds',
        schedule_rule='mode index=((step%1200)+(step//1200))%2;READOUTS=[native_before,first_mean];every repeated event receives each once',
        policy_plan_sha256={a:digest(policy_plan(a)) for a in ARMS},
        policy_receipts={a:policy_receipts(a) for a in ARMS},
        training='C326 batch4/two_to_four schedule repeated twice;no original5/6 name-family fitting;no intermediate evaluation',
        exposure_per_row=[200,200,100,100], exposure_order=['original2','original3','original4','interior4'],
        optimizer='unchanged core_slow AdamW noncore.005/core.0005,betas.9/.999,eps1e-8,decay0;meanCE/globalclip1;one optimizer across both cycles',
        evaluation_policy='native_before for both arms and evaluation/replay;no first_mean evaluation or per-example selection',
        gate='all5 alternating models pass all original2..6/interior gates;each pair nonnegative original6 answer/pair,pooled original2..5 answer/pair,interior answer/pair;strict positive original6 aggregate answer AND pair gains',
        thresholds=dict(accuracy=.90, query_pair_accuracy=.80, evidence_drop=.35, query_drop=.35, both_order=.80),
        parameters=14256, core_parameters=3328, slots=64, precision='cpu float64', threads=2,
        controls='paired initial deep copies;exact per-event policy plan;native saved replay across114views <=1e-9 AND exactargmax;state/data preservation',
        preflight='all5schedules and both policy plans;discarded native model6forwards/12rows/4backward/0updates',
        boundary='unproven training-policy augmentation;not resuming/selecting C332weights,not universal invariance,not isolated causal mechanism;half the native-policy TRAIN exposures in candidate',
        parent_files=457, source_count=SOURCE_COUNT, input_count=INPUT_COUNT,
        own_tests=OWN_TESTS, full_tests=FULL_TESTS, modules=MODULES,
        outputs=list(OUTPUTS), raw_logit_payload_bytes=672399360,
        gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C335 manifest seal')


def make_model(seed, x):
    require(type(seed) is int and seed in SEEDS, 'fresh C335 seed')
    c = x.c
    ref = c.c278.MeanFinalDualReadout(c.factory.new_model(seed), seed, c.reader, c.c269.query_span_mask)
    model = x.policy.configure(x.wide.LengthReadout(ref), 'core_slow')
    require(type(model) is x.wide.LengthReadout and model.backbone.config.max_tokens == 64
            and model.backbone.core.config.slots == 64, 'native architecture')
    require(sum(p.numel() for p in model.parameters()) == 14256
            and sum(p.numel() for p in model.backbone.core.parameters()) == 3328, 'capacity')
    require(c.base.fingerprint(model) == c.base.fingerprint(ref) and list(model.state_dict()) == list(ref.state_dict()), 'native initialization')
    require(all(p.requires_grad and p.dtype == torch.float64 and p.device.type == 'cpu' for p in model.parameters()), 'gradient/precision')
    x.policy.parameter_groups(model, 'core_slow')
    return model


def make_pair(seed, x):
    models = {arm:make_model(seed, x) for arm in ARMS}; p = previous()
    require(p.state_hash(models[ARMS[0]].state_dict()) == p.state_hash(models[ARMS[1]].state_dict()), 'paired initial weights')
    pointers = [{v.data_ptr() for v in m.parameters() if v.numel()} for m in models.values()]
    require(not pointers[0]&pointers[1], 'independent paired storage')
    return models


def schedule(seed, train_rows, x):
    require(type(seed) is int and seed in SEEDS and len(train_rows) == 192, 'TRAIN schedule identity')
    curriculum = previous().source().curriculum()
    events = x.parent.plan_for_order(ORDERS[SEEDS.index(seed)], 'two_to_four', train_rows, x.p312, x.pairs)
    curriculum.validate_schedule(events)
    return events, curriculum.family_mask(events, 'batch4')


def optimize(model, arm, tables, y, events, mask, x):
    """TRAIN-only interface. Exactly one forward/update; no policy averaging loss."""
    p = previous(); modes = policy_plan(arm)
    require(len(events) == len(mask) == CYCLE, 'registered event cycle')
    torch.manual_seed(FIT_RNG); opt = x.policy.optimizer_for(model, 'core_slow'); opt_id = id(opt)
    initial = p.state_hash(model.state_dict()); core_initial = p.state_hash(model.backbone.core.state_dict())
    losses, rates, counts, indices, observed = [], [], [], [], []
    receipts = {mode:dict(calls=0, query_calls=0, rows=0, grad_calls=0) for mode in READOUTS}
    union = {}; boundary = None; continuation = None; model.train()
    with torch.enable_grad():
        for step, mode in enumerate(modes):
            if step == CYCLE:
                continuation = dict(weights=p.state_hash(model.state_dict()), optimizer=p.state_hash(opt.state_dict()))
                require(continuation == boundary, 'optimizer/weight reset at cycle boundary')
            require(id(opt) == opt_id, 'optimizer replaced')
            x.policy.verify_optimizer(opt, model, 'core_slow')
            rate = [g['lr'] for g in opt.param_groups]; require(rate == list(RATES), 'fixed learning rates')
            rates.append(rate); index = step % CYCLE; indices.append(index); opt.zero_grad(set_to_none=True)
            tokens, ids = p.source().curriculum().select_tokens(tables, events[index], mask[index])
            require(len(ids) == 48, 'registered TRAIN batch')
            with p.readouts().readout(model, x.wide, mode) as stats:
                logits = model(tokens, torch.zeros(len(ids), dtype=torch.int64)); x.c.p267.check_logits(logits, len(ids))
                loss = F.cross_entropy(logits, y[ids]); require(bool(torch.isfinite(loss)), 'nonfinite TRAIN loss')
                losses.append(float(loss.detach())); loss.backward()
            require(stats == dict(calls=1, query_calls=2, rows=48, grad_calls=1), 'one actual policy forward')
            for key in receipts[mode]: receipts[mode][key] += stats[key]
            observed.append(mode)
            got = {name:v.numel() for name,v in model.named_parameters() if v.grad is not None}
            require(got, 'missing gradients'); counts.append(sum(got.values())); union.update(got)
            torch.nn.utils.clip_grad_norm_(list(model.parameters()), 1., error_if_nonfinite=True); opt.step()
            if step+1 == CYCLE:
                boundary = dict(weights=p.state_hash(model.state_dict()), optimizer=p.state_hash(opt.state_dict()))
            if (step+1) % 200 == 0:
                print(f'[C335] arm={arm} step={step+1}/{STEPS} policy={mode} ce={losses[-1]:.6f}', flush=True)
    model.eval(); require(continuation == boundary and boundary is not None, 'continued optimizer')
    require(observed == modes and blob(receipts) == blob(policy_receipts(arm)), 'exact TRAIN policy exposure')
    state = {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    require(p.state_hash(state) == p.state_hash(model.state_dict()) and all(v.numel() == 0 or state[k].data_ptr() != v.data_ptr()
            for k,v in model.state_dict().items()), 'deep saved state')
    return dict(arm=arm, steps=STEPS, initial_sha256=initial, final_sha256=p.state_hash(state),
        core_initial_sha256=core_initial, core_final_sha256=p.state_hash(model.backbone.core.state_dict()),
        ce_history=losses, optimizer_group_lrs=rates, gradient_parameter_counts=counts, gradient_union=dict(sorted(union.items())),
        event_indices=indices, policy_modes=observed, policy_receipts=receipts,
        boundary=boundary, continuation=continuation, optimizer_creations=1, intermediate_evaluations=0), state


def train_one(seed, arm, model, tables, y, train_rows, cx, root, pins):
    p = previous(); x = cx[-1]; p.source().base().check_dependencies(root, pins, cx, model)
    events, mask = schedule(seed, train_rows, x); before = p.training_fingerprint(tables, y, events, mask)
    print(f'[C335] seed={seed} arm={arm} phase=training', flush=True)
    with x.c.p267.counted(model, x.c.core) as (calls, cores):
        trace, state = optimize(model, arm, tables, y, events, mask, x)
    require(calls == [2400,115200] and cores[0] == 9600, 'measured TRAIN work')
    require(p.training_fingerprint(tables, y, events, mask) == before, 'TRAIN input mutation')
    trace.update(seed=seed, training_input_sha256=before, schedule_sha256=digest(events.tolist()), mask_sha256=digest(mask.tolist()),
                 family_exposure_per_cycle=p.source().curriculum().exposure(events, mask))
    return trace, state


def check_trace(t, train_rows, x):
    require(type(t['seed']) is int and t['seed'] in SEEDS and t['arm'] in ARMS, 'trace identity')
    events, mask = schedule(t['seed'], train_rows, x)
    require(type(t['steps']) is int and t['steps'] == STEPS
            and t['event_indices'] == list(range(CYCLE))*2 and all(type(z) is int for z in t['event_indices']), 'event order/budget')
    require(t['policy_modes'] == policy_plan(t['arm']) and blob(t['policy_receipts']) == blob(policy_receipts(t['arm'])), 'saved TRAIN policies')
    require(t['schedule_sha256'] == digest(events.tolist()) and t['mask_sha256'] == digest(mask.tolist())
            and t['family_exposure_per_cycle'] == previous().source().curriculum().exposure(events, mask), 'saved exposure')
    require(t['optimizer_group_lrs'] == [list(RATES)]*STEPS and len(t['ce_history']) == STEPS
            and all(type(v) in (int,float) and math.isfinite(v) and v >= 0 for v in t['ce_history']), 'rates/loss history')
    union = t['gradient_union']; counts = t['gradient_parameter_counts']
    require(union and all(type(k) is str and type(v) is int and v > 0 for k,v in union.items())
            and 0 < sum(union.values()) <= 14256 and len(counts) == STEPS
            and all(type(v) is int and 0 < v <= sum(union.values()) for v in counts), 'gradient inventory')
    for key in ('initial_sha256','final_sha256','core_initial_sha256','core_final_sha256','training_input_sha256'):
        require(type(t[key]) is str and re.fullmatch('[0-9a-f]{64}', t[key]), 'state/input hash')
    require(t['initial_sha256'] != t['final_sha256'] and t['core_initial_sha256'] != t['core_final_sha256'], 'trained state')
    require(t['boundary'] == t['continuation'] and set(t['boundary']) == {'weights','optimizer'}
            and all(type(v) is str and re.fullmatch('[0-9a-f]{64}',v) for v in t['boundary'].values()), 'continued state')
    require(type(t['optimizer_creations']) is int and t['optimizer_creations'] == 1
            and type(t['intermediate_evaluations']) is int and t['intermediate_evaluations'] == 0, 'no restart/selection')


def fixed_gate(pairs):
    require([r['seed'] for r in pairs] == list(SEEDS) and all(type(r['seed']) is int for r in pairs), 'full paired cohort')
    eligible = []
    for r in pairs:
        keys = ('six_answer_gain','six_pair_gain','short_answer_gain','short_pair_gain','interior_answer_gain','interior_pair_gain')
        require(type(r['candidate_full_pass']) is bool and all(type(r[k]) is int for k in keys), 'gate types')
        eligible.append(r['candidate_full_pass'] and all(r[k] >= 0 for k in keys))
    return all(eligible) and sum(r['six_answer_gain'] for r in pairs) > 0 and sum(r['six_pair_gain'] for r in pairs) > 0, eligible


def check_summary(v):
    require(all(type(v[k]) is int and v[k] == n for k,n in WORK.items()) and v['paired_conditions_valid'] is True
            and v['all_replays'] is True and v['evaluation_policy'] == 'native_before', 'work/integrity/evaluation policy')
    require([(r['seed'],r['arm']) for r in v['seed_results']] == identities(), 'all final states')
    require(len(v['paired_comparisons']) == 5, 'paired comparisons')
    for i,pair in enumerate(v['paired_comparisons']):
        for offset,key in ((0,'control_full_pass'),(1,'candidate_full_pass')):
            flags = v['seed_results'][2*i+offset]
            crossed().check_flags({k:flags[k] for k in ('original_pass','interior_pass','retention_pass','failures')})
            require(pair[key] is (flags['retention_pass'] and flags['interior_pass']), 'gate binding')
        old, inside = pair['original_by_length'], pair['interior']; require(set(old) == set(map(str,range(2,7))), 'all domains')
        for z in [inside,*old.values()]: previous().contrast_check(z)
        require(pair['six_answer_gain'] == old['6']['answer_gain'] and pair['six_pair_gain'] == old['6']['query_pair_gain']
                and pair['short_answer_gain'] == sum(old[str(n)]['answer_gain'] for n in range(2,6))
                and pair['short_pair_gain'] == sum(old[str(n)]['query_pair_gain'] for n in range(2,6))
                and pair['interior_answer_gain'] == inside['answer_gain'] and pair['interior_pair_gain'] == inside['query_pair_gain'], 'gain binding')
    gate, eligibility = fixed_gate(v['paired_comparisons'])
    require(v['candidate_gate'] is gate and type(v['eligible_seed_count']) is int and v['eligible_seed_count'] == sum(eligibility), 'fixed gate')


def analyze(traces, records, states, data, cx):
    p = previous(); q = p.readouts()
    require([(t['seed'],t['arm']) for t in traces] == [(r['seed'],r['arm']) for r in records] == identities()
            and len(states) == 10, 'complete trained cohort')
    metrics, flags = [], []
    for t,r,state in zip(traces,records,states,strict=True):
        check_trace(t, data['TRAIN'], cx[-1])
        require(set(r) == {'seed','arm','state_sha256','evaluation_policy','raw','receipts'}
                and r['state_sha256'] == t['final_sha256'] == p.state_hash(state)
                and r['evaluation_policy'] == 'native_before' and set(r['raw']) == set(r['receipts']) == {'evaluation','replay'}, 'state/evaluation binding')
        for mode in ('evaluation','replay'):
            p.source().base().validate_raw(r['raw'][mode], data, cx)
            require(blob(r['receipts'][mode]) == blob(dict(calls=171,query_calls=342,rows=16416,grad_calls=0)), 'actual evaluation work')
        crossed().same_tree(r['raw']['evaluation'], r['raw']['replay'])
        score,f = q.summarize_mode(r['raw']['evaluation'], data, cx)
        metrics.append(dict(seed=t['seed'],arm=t['arm'],score=score)); flags.append(dict(seed=t['seed'],arm=t['arm'],**f))
    pairs = []
    for i,seed in enumerate(SEEDS):
        a,c = traces[2*i:2*i+2]
        require(all(a[k] == c[k] for k in ('initial_sha256','core_initial_sha256','training_input_sha256','schedule_sha256',
                    'mask_sha256','family_exposure_per_cycle','event_indices','optimizer_group_lrs')), 'paired TRAIN conditions')
        comparisons = q.compare(records[2*i]['raw']['evaluation'], records[2*i+1]['raw']['evaluation'], data, p.source().base())
        old,inside = comparisons['original_by_length'],comparisons['interior']
        pairs.append(dict(seed=seed,control_full_pass=flags[2*i]['retention_pass'] and flags[2*i]['interior_pass'],
            candidate_full_pass=flags[2*i+1]['retention_pass'] and flags[2*i+1]['interior_pass'],
            six_answer_gain=old['6']['answer_gain'],six_pair_gain=old['6']['query_pair_gain'],
            short_answer_gain=sum(old[str(n)]['answer_gain'] for n in range(2,6)),
            short_pair_gain=sum(old[str(n)]['query_pair_gain'] for n in range(2,6)),
            interior_answer_gain=inside['answer_gain'],interior_pair_gain=inside['query_pair_gain'],**comparisons))
    gate,eligible = fixed_gate(pairs)
    value = dict(candidate_gate=gate,eligible_seed_count=sum(eligible),paired_conditions_valid=True,all_replays=True,
                 evaluation_policy='native_before',seed_results=flags,paired_comparisons=pairs,**WORK)
    check_summary(value); return metrics,value


def load_states(path):
    v = torch.load(path, map_location='cpu', weights_only=True)
    require(set(v) == {'schema','identities','states'} and v['schema'] == 'fold-c335-trained-models-v1'
            and v['identities'] == [list(z) for z in identities()] and len(v['states']) == 10, 'model bundle')
    return v['states']


def run_training(out, source_out, cx, root, pins, read):
    p = previous(); data,old,new = p.load_data(source_out,read); before = digest((data,old,new))
    tables,y = p.prepared(data,old,new,cx); traces,states = [],[]
    for seed in SEEDS:
        models = make_pair(seed,cx[-1])
        for arm in ARMS:
            trace,state = train_one(seed,arm,models[arm],tables,y,data['TRAIN'],cx,root,pins)
            traces.append(trace); states.append(state)
        del models
    with (out/'trained-models.pt').open('xb') as stream:
        torch.save(dict(schema='fold-c335-trained-models-v1',identities=[list(z) for z in identities()],states=states),stream)
    saved = load_states(out/'trained-models.pt'); require([p.state_hash(v) for v in saved] == [p.state_hash(v) for v in states], 'bundle roundtrip')
    records = []
    for (seed,arm),state in zip(identities(),saved,strict=True):
        model = make_model(seed,cx[-1]); p.source().base().check_dependencies(root,pins,cx,model)
        model.eval(); model.requires_grad_(False); raw,receipts = {},{}
        for kind in ('evaluation','replay'):
            model.load_state_dict(state,strict=True); require(p.state_hash(model.state_dict()) == p.state_hash(state), 'loaded checkpoint')
            raw[kind],receipts[kind] = p.readouts().measure(model,'native_before',data,old,new,cx)
            require(p.state_hash(model.state_dict()) == p.state_hash(state), 'evaluation changed weights')
        records.append(dict(seed=seed,arm=arm,state_sha256=p.state_hash(state),evaluation_policy='native_before',raw=raw,receipts=receipts))
        print(f'[C335] seed={seed} arm={arm} native_saved_evaluation_and_replay=COMPLETE',flush=True)
    metrics,value = analyze(traces,records,saved,data,cx); require(digest((data,old,new)) == before, 'data/prompt mutation')
    with (out/'evaluations.pt').open('xb') as stream:
        torch.save(dict(schema='fold-c335-evaluations-v1',records=records),stream)
    for name,item in (('experiment-plan.json',manifest()),('training-traces.json',traces),('measurements.json',metrics),('validation-summary.json',value)):
        with (out/name).open('xb') as stream: stream.write(blob(item))
    return value


def semantic_recheck(out, source_out, cx, read):
    data,_,_ = previous().load_data(source_out,read)
    archive = torch.load(out/'evaluations.pt',map_location='cpu',weights_only=True)
    require(set(archive) == {'schema','records'} and archive['schema'] == 'fold-c335-evaluations-v1', 'evaluation writer schema')
    metrics,value = analyze(read(out/'training-traces.json'),archive['records'],load_states(out/'trained-models.pt'),data,cx)
    for name,item in (('experiment-plan.json',manifest()),('measurements.json',metrics),('validation-summary.json',value)):
        require(blob(read(out/name)) == blob(item), 'saved reconstruction:'+name)
    return value


def native_preflight(source_out, cx, root, pins, read):
    p = previous(); q = p.readouts(); x = cx[-1]; data,old,new = p.load_data(source_out,read)
    tables,y = p.prepared(data,old,new,cx)
    for seed in SEEDS: schedule(seed,data['TRAIN'],x)
    for arm in ARMS: policy_plan(arm)
    model = make_model(SEEDS[0],x); p.source().base().check_dependencies(root,pins,cx,model)
    with torch.no_grad():
        w = model.read.output.weight; w.copy_(torch.sin(torch.arange(w.numel(),dtype=torch.float64).reshape_as(w))*.03)
    initial = p.state_hash(model.state_dict())
    ids = [next(i for i,r in enumerate(data['TRAIN']) if r['language'] == lang) for lang in ('en','ja')]
    for family in ('original','interior4'):
        tokens = tables[family][4,'repeat'][ids]; tasks = torch.zeros(2,dtype=torch.int64); model.train()
        with torch.no_grad(): expected = model(tokens,tasks)
        for mode in READOUTS:
            model.zero_grad(set_to_none=True)
            with torch.enable_grad(),q.readout(model,x.wide,mode) as stats:
                logits = model(tokens,tasks)
                if mode == 'native_before': q.same(expected,logits.detach())
                F.cross_entropy(logits,y[ids]).backward()
            require(stats == dict(calls=1,query_calls=2,rows=2,grad_calls=1) and model.read.query.weight.grad is not None
                    and all(v.grad is None or bool(torch.isfinite(v.grad).all()) for v in model.parameters()), 'native backward')
    require(p.state_hash(model.state_dict()) == initial, 'preflight weights mutated')
    print('C335_native_preflight=PASS;schedules=5;policy_plans=2;forwards=6;rows=12;backward=4;updates=0',flush=True)
