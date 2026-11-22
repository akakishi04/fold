"""C346: half-rate pair-max training at fixed mixed45 budget with two reference arms."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import math
import re
import torch

EXPERIMENT_ID = 'C346-v5b-pair-max-rate'
STAGE = 'V5-B-PAIR-MAX-RATE'
SEEDS = tuple(range(346001,346006))
ORDERS = tuple(range(346101,346106))
ARMS = ('mean_ce','pair_max','pair_max_half_rate')
CONTROLS = ('pair_max','mean_ce')
CANDIDATE = 'pair_max_half_rate'
PROFILES = ('repeat','shared_prefix','shared_suffix')
CYCLE, STEPS, FIT_RNG = 1200, 2400, 612000
RATES = {'mean_ce':(.005,.0005),'pair_max':(.005,.0005),'pair_max_half_rate':(.0025,.00025)}
TRAIN_TOKENS = {arm:3168000 for arm in ARMS}
SPLITS = ('TRAIN','HOLDOUT')
LOSS_TOL = 1e-12
DOMAINS = tuple('original'+str(n) for n in range(2,7))+('interior4',)
OWN = ('fold_lm/v05_benchmarks/model_c346_pair_max_rate.py',
       'tools/c346_execution.py','tests_lm/test_v05_c346_pair_max_rate.py',
       'tests_lm/test_v05_c346_execution.py','tools/run_c346.ps1',
       'tools/invoke_c346.ps1','docs/experiment-ledger-addendum-c346-preregistration.md')
OUTPUTS = ('experiment-plan.json','training-traces.json','trained-models.pt',
           'evaluations.pt','measurements.json','validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 74, 6652, 243
SOURCE_COUNT, INPUT_COUNT = 944, 9177
WORK = dict(training_models=15,evaluation_models=15,checkpoint_states=15,
    optimizer_creations=15,train_steps=36000,gradient_calls=36000,optimizer_steps=36000,
    training_rows=1728000,model_forward_calls=41130,row_presentations=2220480,
    core_forward_calls=164520,query_projection_calls=82260,model_state_loads=30,
    checkpoint_bundle_loads=1,new_checkpoint_writes=1,network_calls=0)
ACCEPTANCE_BASE = 'f5fc8e89b5bb3d2749df91aa3b503596a6be1fc2'
MANIFEST_SHA = '8dad5562249bf21517bb8487c5c6970ac75b55405252dbbf5c3512d797d46d64'



def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c345_saved_objective_audit')


def prior():
    return parent().parent()


def previous():
    return prior().previous()


def reference():
    return prior().reference()


def support():
    return prior().support()


def identities():
    return list(itertools.product(SEEDS,ARMS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=ACCEPTANCE_BASE,
        parent_execution='c81ffe102c3a9280f28a68e572403549ce77fa1d',
        parent_summary='cfc3fe5b8f4ec927d875e2a016a940b5d34aac9ef14d93644eeb26567c0e1f30',
        parent_envelope='e883c26d1df24d940cd51b551f06e46e7ac69da216ea6024dc299ee24d2cceab',
        question='does halving both constant AdamW group rates from initialization improve pair-max interior binding and preserve every domain against default pair-max and ordinary mean CE',
        seeds=list(SEEDS),orders=list(ORDERS),arms=list(ARMS),controls=list(CONTROLS),candidate=CANDIDATE,
        cycle=CYCLE,steps=STEPS,fit_rng=FIT_RNG,rates={k:list(v) for k,v in RATES.items()},
        changed='within pair-max only constant learning-rate scale:both noncore/core rates multiplied by .5 from initialization;meanCE default-rate reference retained',
        objective='immutable C344 full256 meanCE or mean24 maximum(CEqueryA,CEqueryB);candidate uses exactly pairmax without coefficient,loss scaling or rate compensation',
        pair_semantics='canonical TRAIN metadata before optimizer creation and before every forward;two distinct counterpart queries and targets',
        held='three independent equal fresh states per seed;identical mixed45 tokens/targets,192TRAIN rows,1200events repeated twice,family/length masks,48rows24pairs,architecture,clip1,AdamW betas/eps/decay,scorers',
        input_policy='immutable C342 mixed45 banks/selectors and balanced length mask on fresh C346 order seeds;no parent global mutation or fallback',
        actual_per_row_exposure=dict(original2=200,original3=200,original4=50,original5=50,original6=0,interior4=100),
        per_cycle_exposure=dict(original2=100,original3=100,original4=25,original5=25,original6=0,interior4=50),
        exposure_unit='per canonical logical TRAIN row across profiles;HOLDOUT/masked views never fitted;original6 TRAIN names/prompts never fitted',
        nonpadding_training_tokens_per_model=dict(TRAIN_TOKENS),
        compute_boundary='same2400updates/115200rows/3168000nonpaddingtokens per model;both reductions computed in every arm;no additional neural work for terminal arithmetic',
        input_proof='equal canonical-bank/event/family/length/token-and-target-stream/pair-metadata fingerprints and first preupdate common losses in all3arms',
        optimizer='one continuous AdamW per model;noncore/core ordered groups;betas.9/.999 eps1e-8 decay0 globalclip1;default.005/.0005 candidate.0025/.00025',
        histories='all2400preupdate ordinaryCE,pairmax,selectedloss,preclipnorm and both group rates per state;no final-checkpoint or exact-clipping interpretation of preupdate traces',
        gate='all5candidate full original2..6+interior4;EACHseed EACH6domain EACHsplit nonnegative normal answer AND pair gains vs EACH default pairmax and meanCE;strict pooled interior TRAIN/HOLDOUT answer AND pair gains vs default pairmax',
        contrasts=120,nonnegative_inequalities_per_control=120,
        strict_endpoints=['interior_TRAIN_answers','interior_TRAIN_query_pairs','interior_HOLDOUT_answers','interior_HOLDOUT_query_pairs'],
        saturation='report four primary headroom counts;any strict tie or zero-headroom endpoint remains valid negative;no reseeding,subgroup selection or threshold relaxation',
        terminal='all180state/domain/split normal full256 float64 CE/pairmax summaries plus120candidate-minus-control loss contrasts;canonical metadata pairs/all3profiles/bothlanguages;equal answer/pair weighting within domain/split,not exposure weighting',
        terminal_gate='descriptive only;no required loss sign,optimization-improvement gate,loss-based model selection or additional forwards',
        support_counts='all180normal support/collapse/pair summaries and120rescue/regression contrasts across TRAIN/HOLDOUT;no supplied-value inference filter',
        limits='C345 motivates a bounded rate intervention but does not prove rate causality;no half-rate meanCE arm so no factorial interaction or optimal-LR claim;new seeds prevent same-cohort confirmation;no convergence or clipping mechanism proof',
        thresholds=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,both_order=.80),
        parameters=14256,core_parameters=3328,slots=64,precision='cpu float64',threads=2,
        evaluation_policy='native_before;all15fits before full114views/state evaluation and replay;30state reloads;exactargmax plus1e-9 replay;all256classes',
        preflight='all5schedules/pairs/allocations/streams first;discarded native model,3zero-step optimizer configurations;3arms*2cycles*2families*English+Japanese pairs;24forwards96rows12backwards0updates',
        source_count=SOURCE_COUNT,input_count=INPUT_COUNT,parent_files=491,parent_test_proof_files=485,
        own_tests=OWN_TESTS,full_tests=FULL_TESTS,modules=MODULES,outputs=list(OUTPUTS),
        raw_logit_payload_bytes=1008599040,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA,'C346 manifest seal')


def prepared(data,old,new,cx):
    return prior().prepared(data,old,new,cx)


def make_model(seed, x):
    require(type(seed) is int and seed in SEEDS,'fresh C346 seed')
    c = x.c
    ref = c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    model = x.policy.configure(x.wide.LengthReadout(ref),'core_slow')
    require(type(model) is x.wide.LengthReadout and model.backbone.config.max_tokens == 64
            and model.backbone.core.config.slots == 64,'native architecture')
    require(sum(v.numel() for v in model.parameters()) == 14256
            and sum(v.numel() for v in model.backbone.core.parameters()) == 3328,'capacity')
    require(c.base.fingerprint(model) == c.base.fingerprint(ref) and list(model.state_dict()) == list(ref.state_dict()),'native initialization')
    require(all(v.requires_grad and v.dtype == torch.float64 and v.device.type == 'cpu' for v in model.parameters()),'precision/gradient')
    x.policy.parameter_groups(model,'core_slow')
    return model


def make_models(seed, x):
    models = {arm:make_model(seed,x) for arm in ARMS}; p = previous()
    require(len({p.state_hash(model.state_dict()) for model in models.values()}) == 1,'three equal initial states')
    pointers = [{v.data_ptr() for v in model.parameters() if v.numel()} for model in models.values()]
    require(all(not a&b for a,b in itertools.combinations(pointers,2)),'three independent state storages')
    return models


def schedule(seed, rows, x):
    require(type(seed) is int and seed in SEEDS and len(rows) == 192,'TRAIN schedule identity')
    q = previous().source().curriculum()
    events = x.parent.plan_for_order(ORDERS[SEEDS.index(seed)],'two_to_four',rows,x.p312,x.pairs)
    q.validate_schedule(events)
    return events,q.family_mask(events,'batch4')


def length_mask(events,family):
    return prior().length_mask(events,family)


def actual_exposure(events,family,selected):
    return prior().actual_exposure(events,family,selected)


def select_tokens(tables,event,family,selected):
    return prior().select_tokens(tables,event,family,selected)


def training_fingerprint(tables,y,events,family,selected):
    return prior().training_fingerprint(tables,y,events,family,selected)


def stream_update(value,tokens,y,ids):
    return prior().stream_update(value,tokens,y,ids)


def input_accounting(tables, y, events, family, selected):
    value = hashlib.sha256(b'C346 TRAIN int64le tokens then targets per update\n'); count = 0
    for step in range(STEPS):
        tokens,ids = select_tokens(tables,events[step%CYCLE],family[step%CYCLE],selected[step])
        count += int((tokens != 256).sum()); stream_update(value,tokens,y,ids)
    return count,value.hexdigest()


def validate_batch_pairs(rows,targets,ids):
    return prior().validate_batch_pairs(rows,targets,ids)


def validate_training_pairs(rows,targets,events,x):
    return prior().validate_training_pairs(rows,targets,events,x)


def objective_name(arm):
    require(type(arm) is str and arm in ARMS,'registered objective arm')
    return 'mean_ce' if arm == 'mean_ce' else 'pair_max'


def objective(logits, targets, arm):
    return prior().objective(logits,targets,objective_name(arm))


def parameter_groups(model, arm, x):
    require(type(arm) is str and arm in ARMS,'registered rate arm')
    groups = x.policy.parameter_groups(model,'core_slow')
    require(len(groups) == 2 and [g['lr'] for g in groups] == [.005,.0005],'accepted group layout/default rates')
    return [dict(params=list(group['params']),lr=rate) for group,rate in zip(groups,RATES[arm],strict=True)]


def optimizer_for(model, arm, x):
    optimizer = torch.optim.AdamW(parameter_groups(model,arm,x),lr=RATES[arm][0],betas=(.9,.999),eps=1e-8,weight_decay=0.)
    verify_optimizer(optimizer,model,arm,x)
    return optimizer


def verify_optimizer(optimizer, model, arm, x):
    expected = parameter_groups(model,arm,x)
    require(type(optimizer) is torch.optim.AdamW and len(optimizer.param_groups) == 2,'unchanged AdamW/two groups')
    for actual,wanted in zip(optimizer.param_groups,expected,strict=True):
        require([id(p) for p in actual['params']] == [id(p) for p in wanted['params']]
                and type(actual['lr']) is float and actual['lr'] == wanted['lr']
                and actual['betas'] == (.9,.999) and actual['eps'] == 1e-8 and actual['weight_decay'] == 0.
                and actual['amsgrad'] is False and actual['maximize'] is False
                and actual['capturable'] is False and actual['differentiable'] is False
                and actual['foreach'] is None and actual['fused'] is None,'constant arm-specific optimizer policy')


def optimize(model, arm, tables, y, events, family, selected, rows, x):
    require(arm in ARMS and len(events) == len(family) == CYCLE and len(selected) == STEPS == 2*CYCLE, 'registered cycles')
    # This entire metadata check precedes optimizer creation, not merely the first update.
    validate_training_pairs(rows,y,events,x)
    p = previous(); torch.manual_seed(FIT_RNG)
    opt = optimizer_for(model,arm,x); opt_id = id(opt); optimizer_steps = 0
    initial = p.state_hash(model.state_dict()); core_initial = p.state_hash(model.backbone.core.state_dict())
    losses,rates,counts,indices,norms = [],[],[],[],[]; union = {}; boundary = None; continuation = None
    stream = hashlib.sha256(b'C346 TRAIN int64le tokens then targets per update\n'); nonpadding = 0; checked_pairs = 0
    model.train()
    with torch.enable_grad(),p.readouts().readout(model,x.wide,'native_before') as stats:
        for step in range(STEPS):
            if step == CYCLE:
                continuation = dict(weights=p.state_hash(model.state_dict()),optimizer=p.state_hash(opt.state_dict()))
                require(continuation == boundary, 'optimizer/weight reset')
            require(id(opt) == opt_id, 'optimizer replaced'); verify_optimizer(opt,model,arm,x)
            rate = [g['lr'] for g in opt.param_groups]; require(rate == list(RATES[arm]), 'fixed rates'); rates.append(rate)
            index = step%CYCLE; indices.append(index); opt.zero_grad(set_to_none=True)
            tokens,ids = select_tokens(tables,events[index],family[index],selected[step])
            require(len(ids) == 48 and torch.equal(ids,events[index,:,2:].reshape(-1)), 'actual paired TRAIN row order')
            validate_batch_pairs(rows,y,ids); checked_pairs += len(ids)//2
            nonpadding += int((tokens != 256).sum()); stream_update(stream,tokens,y,ids)
            logits = model(tokens,torch.zeros(len(ids),dtype=torch.int64)); x.c.p267.check_logits(logits,len(ids))
            loss,ce,pair_max = objective(logits,y[ids],arm)
            losses.append(dict(mean_ce=float(ce.detach()),pair_max=float(pair_max.detach()),selected=float(loss.detach())))
            loss.backward()
            got = {name:v.numel() for name,v in model.named_parameters() if v.grad is not None}
            require(got, 'missing gradients'); counts.append(sum(got.values())); union.update(got)
            norm = torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True)
            norms.append(float(norm)); opt.step(); optimizer_steps += 1
            if step+1 == CYCLE: boundary = dict(weights=p.state_hash(model.state_dict()),optimizer=p.state_hash(opt.state_dict()))
            if (step+1)%200 == 0:
                print(f'[C346] arm={arm} step={step+1}/{STEPS} ce={losses[-1]["mean_ce"]:.6f} pairmax={losses[-1]["pair_max"]:.6f} selected={losses[-1]["selected"]:.6f}',flush=True)
    model.eval(); require(boundary is not None and boundary == continuation, 'continuous optimizer')
    require(stats == dict(calls=STEPS,query_calls=2*STEPS,rows=48*STEPS,grad_calls=STEPS)
            and checked_pairs == 24*STEPS, 'TRAIN pair/forward receipt')
    state = {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    require(p.state_hash(state) == p.state_hash(model.state_dict()) and all(v.numel() == 0 or state[k].data_ptr() != v.data_ptr()
            for k,v in model.state_dict().items()), 'deep checkpoint')
    return dict(arm=arm,readout_mode='native_before',length_policy='mixed45',steps=STEPS,
        initial_sha256=initial,final_sha256=p.state_hash(state),core_initial_sha256=core_initial,
        core_final_sha256=p.state_hash(model.backbone.core.state_dict()),loss_history=losses,preclip_norm_history=norms,
        optimizer_group_lrs=rates,gradient_parameter_counts=counts,gradient_union=dict(sorted(union.items())),
        event_indices=indices,policy_receipt=dict(stats),boundary=boundary,continuation=continuation,
        optimizer_creations=1,optimizer_steps=optimizer_steps,intermediate_evaluations=0,checked_training_pairs=checked_pairs,
        pair_metadata_sha256=digest(rows),nonpadding_token_presentations=nonpadding,
        actual_training_stream_sha256=stream.hexdigest()),state


def train_one(seed, arm, model, tables, y, rows, cx, root, pins):
    p = previous(); x = cx[-1]; p.source().base().check_dependencies(root,pins,cx,model)
    events,family = schedule(seed,rows,x); selected = length_mask(events,family)
    before = training_fingerprint(tables,y,events,family,selected); exposure = actual_exposure(events,family,selected)
    print(f'[C346] seed={seed} arm={arm} phase=training',flush=True)
    with x.c.p267.counted(model,x.c.core) as (calls,cores):
        trace,state = optimize(model,arm,tables,y,events,family,selected,rows,x)
    require(calls == [2400,115200] and cores[0] == 9600, 'measured TRAIN work')
    require(training_fingerprint(tables,y,events,family,selected) == before, 'TRAIN input mutation')
    count,stream = input_accounting(tables,y,events,family,selected)
    require(trace['nonpadding_token_presentations'] == count == TRAIN_TOKENS[arm]
            and trace['actual_training_stream_sha256'] == stream, 'measured TRAIN token stream')
    trace.update(seed=seed,measured_training_work=dict(calls=calls[0],rows=calls[1],core_calls=cores[0]),training_input_sha256=before,
        logical_training_sha256=p.state_hash(dict(targets=y,events=events,mask=family)),
        schedule_sha256=digest(events.tolist()),mask_sha256=digest(family.tolist()),length_mask_sha256=digest(selected.tolist()),
        family_exposure_per_cycle=p.source().curriculum().exposure(events,family),actual_exposure_per_cycle=exposure)
    return trace,state


def check_trace(t, rows, x, tables, y):
    p = previous(); require(type(t['seed']) is int and t['seed'] in SEEDS and t['arm'] in ARMS, 'trace identity')
    events,family = schedule(t['seed'],rows,x); selected = length_mask(events,family)
    validate_training_pairs(rows,y,events,x)
    require(t['readout_mode'] == 'native_before' and t['length_policy'] == 'mixed45', 'trace token/readout policy')
    require(type(t['steps']) is int and t['steps'] == STEPS and t['event_indices'] == list(range(CYCLE))*2
            and all(type(v) is int for v in t['event_indices']), 'event budget/order')
    require(t['schedule_sha256'] == digest(events.tolist()) and t['mask_sha256'] == digest(family.tolist())
            and t['length_mask_sha256'] == digest(selected.tolist())
            and t['family_exposure_per_cycle'] == p.source().curriculum().exposure(events,family)
            and t['actual_exposure_per_cycle'] == actual_exposure(events,family,selected), 'actual exposure reconstruction')
    count,stream = input_accounting(tables,y,events,family,selected)
    require(type(t['nonpadding_token_presentations']) is int and t['nonpadding_token_presentations'] == count == TRAIN_TOKENS[t['arm']]
            and t['actual_training_stream_sha256'] == stream, 'reconstructed token stream')
    require(t['training_input_sha256'] == training_fingerprint(tables,y,events,family,selected)
            and t['logical_training_sha256'] == p.state_hash(dict(targets=y,events=events,mask=family))
            and t['pair_metadata_sha256'] == digest(rows) and type(t['checked_training_pairs']) is int
            and t['checked_training_pairs'] == 24*STEPS, 'TRAIN recipe/pair fingerprint')
    require(t['optimizer_group_lrs'] == [list(RATES[t['arm']])]*STEPS and len(t['loss_history']) == len(t['preclip_norm_history']) == STEPS, 'rates/loss history length')
    for row in t['loss_history']:
        require(set(row) == {'mean_ce','pair_max','selected'} and all(type(v) is float and math.isfinite(v) and v >= 0 for v in row.values()), 'finite saved losses')
        tol = LOSS_TOL*max(1.,row['mean_ce'])
        require(row['mean_ce']-tol <= row['pair_max'] <= 2*row['mean_ce']+tol and row['selected'] == row[objective_name(t['arm'])], 'registered reduction arithmetic')
    require(all(type(v) is float and math.isfinite(v) and v >= 0 for v in t['preclip_norm_history']), 'preclip gradient norms')
    union,counts = t['gradient_union'],t['gradient_parameter_counts']
    require(union and all(type(k) is str and type(v) is int and v > 0 for k,v in union.items()) and 0 < sum(union.values()) <= 14256
            and len(counts) == STEPS and all(type(v) is int and 0 < v <= sum(union.values()) for v in counts), 'gradient inventory')
    for key in ('initial_sha256','final_sha256','core_initial_sha256','core_final_sha256','training_input_sha256',
                'logical_training_sha256','actual_training_stream_sha256','length_mask_sha256','pair_metadata_sha256'):
        require(type(t[key]) is str and re.fullmatch('[0-9a-f]{64}',t[key]), 'state/input fingerprint')
    require(t['initial_sha256'] != t['final_sha256'] and t['core_initial_sha256'] != t['core_final_sha256'], 'trained state')
    require(t['boundary'] == t['continuation'] and set(t['boundary']) == {'weights','optimizer'}
            and all(type(v) is str and re.fullmatch('[0-9a-f]{64}',v) for v in t['boundary'].values()), 'continued state')
    require(t['measured_training_work'] == dict(calls=2400,rows=115200,core_calls=9600)
            and all(type(v) is int for v in t['measured_training_work'].values())
            and type(t['optimizer_steps']) is int and t['optimizer_steps'] == STEPS,'measured training/optimizer work')
    require(type(t['optimizer_creations']) is int and t['optimizer_creations'] == 1 and type(t['intermediate_evaluations']) is int
            and t['intermediate_evaluations'] == 0 and t['policy_receipt'] == dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400), 'no restart/selection')


def normal_report(raw,data):
    return prior().normal_report(raw,data)


def compare_normal(control,candidate,data):
    return prior().compare_normal(control,candidate,data)


def contrast_check(row,split):
    return prior().contrast_check(row,split)


def fixed_gate(pairs):
    require(type(pairs) is list and [(r['seed'],r['control_arm']) for r in pairs] == list(itertools.product(SEEDS,CONTROLS))
            and all(type(r['seed']) is int and r['candidate_arm'] == CANDIDATE for r in pairs),'all two-control paired coordinates')
    nonnegative = {arm:[] for arm in CONTROLS}; per_seed = {seed:[] for seed in SEEDS}; full = {}
    for row in pairs:
        seed,control = row['seed'],row['control_arm']
        require(type(row['candidate_full_pass']) is bool and set(row['normal_by_domain']) == set(DOMAINS),'candidate full/domain gate')
        if seed in full: require(full[seed] is row['candidate_full_pass'],'same candidate full gate in both contrasts')
        full[seed] = row['candidate_full_pass']
        for domain in DOMAINS:
            require(set(row['normal_by_domain'][domain]) == set(SPLITS),'both comparison splits')
            for split in SPLITS:
                z = row['normal_by_domain'][domain][split]; contrast_check(z,split)
                conditions = [z[k] >= 0 for k in ('answer_gain','query_pair_gain')]
                nonnegative[control].extend(conditions); per_seed[seed].extend(conditions)
    primary = [row for row in pairs if row['control_arm'] == 'pair_max']
    strict = {split:{key:sum(r['normal_by_domain']['interior4'][split][key] for r in primary)
                     for key in ('answer_gain','query_pair_gain')} for split in SPLITS}
    headroom = {split:dict(answer_headroom=sum(r['normal_by_domain']['interior4'][split]['answers']-
        r['normal_by_domain']['interior4'][split]['control_correct'] for r in primary),
        query_pair_headroom=sum(r['normal_by_domain']['interior4'][split]['query_pairs']-
        r['normal_by_domain']['interior4'][split]['control_both_correct'] for r in primary)) for split in SPLITS}
    components = dict(all_candidates_full_pass=all(full.values()),nonnegative_vs_pair_max=all(nonnegative['pair_max']),
        nonnegative_vs_mean_ce=all(nonnegative['mean_ce']),strict_interior_vs_pair_max=all(g > 0 for z in strict.values() for g in z.values()),
        candidate_full_pass_count=sum(full.values()),nonnegative_counts={arm:dict(passed=sum(checks),total=len(checks))
            for arm,checks in nonnegative.items()})
    require(all(row['total'] == 120 for row in components['nonnegative_counts'].values()),'all240nonnegative inequalities')
    eligible = [full[seed] and all(per_seed[seed]) for seed in SEEDS]
    gate = all(eligible) and components['strict_interior_vs_pair_max']
    return gate,eligible,strict,components,headroom


def terminal_report(raw, data, normal, seed, arm):
    result = []; diagnostic = parent()
    for domain,split in itertools.product(DOMAINS,SPLITS):
        tree = raw['interior'] if domain == 'interior4' else raw['original'][domain[-1]]
        pairs = [pair for profile in diagnostic.profiles(domain)
                 for pair in diagnostic.terminal_view(tree[split][profile]['normal'],data[split])]
        counts = normal[domain][split]
        require(len(pairs) == counts['query_pairs'] and sum(p['correct_answers'] for p in pairs) == counts['correct']
                and sum(p['both_correct'] for p in pairs) == counts['both_query_correct'],'terminal/normal exact counts')
        result.append(dict(seed=seed,arm=arm,domain=domain,split=split,normal=counts,
            mean_ce=diagnostic.statistics([p['mean_ce'] for p in pairs]),pair_max=diagnostic.statistics([p['pair_max'] for p in pairs])))
    return result


def terminal_comparisons(terminal, pairs):
    lookup = {(row['seed'],row['arm'],row['domain'],row['split']):row for row in terminal}; result = []
    for pair in pairs:
        for domain,split in itertools.product(DOMAINS,SPLITS):
            a,b = [lookup[pair['seed'],arm,domain,split] for arm in (pair['control_arm'],CANDIDATE)]
            result.append(dict(seed=pair['seed'],control_arm=pair['control_arm'],candidate_arm=CANDIDATE,domain=domain,split=split,
                mean_ce_delta=b['mean_ce']['mean']-a['mean_ce']['mean'],pair_max_delta=b['pair_max']['mean']-a['pair_max']['mean'],
                normal_contrast=pair['normal_by_domain'][domain][split]))
    return result


def observed_work(traces, records, states):
    training = [trace['policy_receipt'] for trace in traces]
    evaluation = [row for record in records for row in record['receipts'].values()]
    require(all(trace['measured_training_work'] == dict(calls=receipt['calls'],rows=receipt['rows'],core_calls=4*receipt['calls'])
                for trace,receipt in zip(traces,training,strict=True)),'measured training/core receipt binding')
    train_calls = sum(r['calls'] for r in training); eval_calls = sum(r['calls'] for r in evaluation)
    return dict(training_models=len(traces),evaluation_models=len(records),checkpoint_states=len(states),
        optimizer_creations=sum(t['optimizer_creations'] for t in traces),train_steps=sum(t['steps'] for t in traces),
        gradient_calls=sum(r['grad_calls'] for r in training+evaluation),optimizer_steps=sum(t['optimizer_steps'] for t in traces),
        training_rows=sum(r['rows'] for r in training),model_forward_calls=train_calls+eval_calls,
        row_presentations=sum(r['rows'] for r in training+evaluation),
        core_forward_calls=sum(t['measured_training_work']['core_calls'] for t in traces)+4*eval_calls,
        query_projection_calls=sum(r['query_calls'] for r in training+evaluation),model_state_loads=len(evaluation),
        checkpoint_bundle_loads=1,new_checkpoint_writes=1,network_calls=0)


def check_normal_report(value,domain,split):
    return prior().check_normal_report(value,domain,split)


def check_summary(value):
    require(type(value) is dict and set(value) == {*WORK,'candidate_gate','eligible_seed_count','strict_interior_gains','gate_components',
        'strict_interior_headroom','strict_interior_ceiling','paired_conditions_valid','all_replays','evaluation_policy',
        'seed_results','paired_comparisons','terminal','terminal_contrasts'},'summary writer schema')
    require(all(type(value[k]) is int and value[k] == n for k,n in WORK.items()) and value['paired_conditions_valid'] is True
            and value['all_replays'] is True and value['evaluation_policy'] == 'native_before','work/integrity')
    require([(r['seed'],r['arm']) for r in value['seed_results']] == identities(),'complete three-arm cohort')
    state_lookup = {}; state_keys = {'seed','arm','original_pass','interior_pass','retention_pass','failures','support','normal_by_domain','training_nonpadding_tokens'}
    for state in value['seed_results']:
        require(set(state) == state_keys and type(state['seed']) is int and set(state['original_pass']) == set(map(str,range(2,7)))
                and all(type(flag) is bool for flag in state['original_pass'].values()) and type(state['interior_pass']) is bool
                and state['retention_pass'] is all(state['original_pass'].values()),'state gate fields')
        require(type(state['training_nonpadding_tokens']) is int and state['training_nonpadding_tokens'] == TRAIN_TOKENS[state['arm']]
                and set(state['normal_by_domain']) == set(state['support']) == set(state['failures']) == set(DOMAINS),'state accounting domains')
        for domain in DOMAINS:
            require(set(state['normal_by_domain'][domain]) == set(SPLITS),'state split coverage')
            for split in SPLITS: check_normal_report(state['normal_by_domain'][domain][split],domain,split)
            require(state['support'][domain] == {k:state['normal_by_domain'][domain]['HOLDOUT'][k] for k in ('answers',*support().audit().KINDS)},'legacy HOLDOUT support binding')
            failures = state['failures'][domain]
            require(set(failures) == {'local','order'} and all(type(failures[k]) is int and 0 <= failures[k] <= limit
                    for k,limit in (('local',72),('order',36))),'state failure counts')
            passed = state['interior_pass'] if domain == 'interior4' else state['original_pass'][domain[-1]]
            require(passed is (failures == dict(local=0,order=0)),'state failure/pass binding')
        state_lookup[state['seed'],state['arm']] = state
    pairs = value['paired_comparisons']; gain_keys = ('interior_train_answer_gain','interior_train_pair_gain','interior_holdout_answer_gain','interior_holdout_pair_gain')
    require([(r['seed'],r['control_arm']) for r in pairs] == list(itertools.product(SEEDS,CONTROLS)),'complete two-control contrasts')
    for row in pairs:
        require(set(row) == {'seed','control_arm','candidate_arm','control_full_pass','candidate_full_pass','normal_by_domain',*gain_keys}
                and row['candidate_arm'] == CANDIDATE,'paired writer schema')
        left,right = [state_lookup[row['seed'],arm] for arm in (row['control_arm'],CANDIDATE)]
        for state,name in ((left,'control_full_pass'),(right,'candidate_full_pass')):
            require(type(row[name]) is bool and row[name] is (state['retention_pass'] and state['interior_pass']),'paired full flags')
        require(set(row['normal_by_domain']) == set(DOMAINS),'paired domain coverage')
        for domain in DOMAINS:
            require(set(row['normal_by_domain'][domain]) == set(SPLITS),'paired split coverage')
            for split in SPLITS:
                contrast = row['normal_by_domain'][domain][split]; contrast_check(contrast,split)
                a,b = [state['normal_by_domain'][domain][split] for state in (left,right)]
                require([contrast[k] for k in ('control_correct','candidate_correct','control_both_correct','candidate_both_correct')] ==
                        [a['correct'],b['correct'],a['both_query_correct'],b['both_query_correct']],'normal/paired count binding')
        expected = [row['normal_by_domain']['interior4'][split][key] for split in SPLITS for key in ('answer_gain','query_pair_gain')]
        require(all(type(row[k]) is int for k in gain_keys) and [row[k] for k in gain_keys] == expected,'four interior endpoints')
    gate,eligible,strict,components,headroom = fixed_gate(pairs)
    require(value['candidate_gate'] is gate and type(value['eligible_seed_count']) is int and value['eligible_seed_count'] == sum(eligible)
            and blob(value['strict_interior_gains']) == blob(strict) and blob(value['gate_components']) == blob(components)
            and blob(value['strict_interior_headroom']) == blob(headroom)
            and value['strict_interior_ceiling'] is any(n == 0 for row in headroom.values() for n in row.values()),'fixed gate/subgates/headroom')
    terminal = value['terminal']; fields = ('seed','arm','domain','split'); diagnostic = parent()
    require([tuple(row[k] for k in fields) for row in terminal] == list(itertools.product(SEEDS,ARMS,DOMAINS,SPLITS)),'all180terminal coordinates')
    for row in terminal:
        require(set(row) == {*fields,'normal','mean_ce','pair_max'},'terminal summary schema')
        normal = state_lookup[row['seed'],row['arm']]['normal_by_domain'][row['domain']][row['split']]
        require(blob(row['normal']) == blob(normal),'terminal normal binding')
        for key in ('mean_ce','pair_max'): diagnostic.check_statistics(row[key],normal['query_pairs'],True)
        tol = LOSS_TOL*max(1.,row['mean_ce']['mean'])
        require(row['mean_ce']['mean']-tol <= row['pair_max']['mean'] <= 2*row['mean_ce']['mean']+tol,'terminal reduction bounds')
    contrasts = value['terminal_contrasts']
    require(blob(contrasts) == blob(terminal_comparisons(terminal,pairs)),'all120terminal comparison arithmetic/binding')
    for row in contrasts:
        diagnostic.finite(row['mean_ce_delta']); diagnostic.finite(row['pair_max_delta'])


def analyze(traces, records, states, data, cx, tables, y):
    p = previous(); q = p.readouts(); reference().reference().validate_tables(tables,y)
    require(type(traces) is list and type(records) is list and type(states) is list
            and [(t['seed'],t['arm']) for t in traces] == [(r['seed'],r['arm']) for r in records] == identities()
            and len(states) == len(identities()),'complete trained cohort')
    metrics,flags,terminal = [],[],[]
    for trace,record,state in zip(traces,records,states,strict=True):
        check_trace(trace,data['TRAIN'],cx[-1],tables,y)
        require(set(record) == {'seed','arm','state_sha256','evaluation_policy','raw','receipts'}
                and record['state_sha256'] == trace['final_sha256'] == p.state_hash(state) and record['evaluation_policy'] == 'native_before'
                and set(record['raw']) == set(record['receipts']) == {'evaluation','replay'},'state binding')
        for mode in ('evaluation','replay'):
            p.source().base().validate_raw(record['raw'][mode],data,cx)
            require(blob(record['receipts'][mode]) == blob(dict(calls=171,query_calls=342,rows=16416,grad_calls=0)),'evaluation receipt')
        require(p.source().base().replay_error(record['raw']['evaluation'],record['raw']['replay'],data,cx) <= 1e-9,'saved replay')
        score,f = q.summarize_mode(record['raw']['evaluation'],data,cx); normal = normal_report(record['raw']['evaluation'],data)
        metrics.append(dict(seed=trace['seed'],arm=trace['arm'],score=score))
        terminal.extend(terminal_report(record['raw']['evaluation'],data,normal,trace['seed'],trace['arm']))
        legacy = {domain:{k:normal[domain]['HOLDOUT'][k] for k in ('answers',*support().audit().KINDS)} for domain in DOMAINS}
        flags.append(dict(seed=trace['seed'],arm=trace['arm'],training_nonpadding_tokens=trace['nonpadding_token_presentations'],
            support=legacy,normal_by_domain=normal,**f))
    trace_lookup = {(r['seed'],r['arm']):r for r in traces}; raw_lookup = {(r['seed'],r['arm']):r['raw']['evaluation'] for r in records}
    flag_lookup = {(r['seed'],r['arm']):r for r in flags}; pairs = []
    equal_keys = ('initial_sha256','core_initial_sha256','logical_training_sha256','schedule_sha256','mask_sha256',
        'family_exposure_per_cycle','actual_exposure_per_cycle','event_indices','training_input_sha256',
        'actual_training_stream_sha256','length_mask_sha256','pair_metadata_sha256','nonpadding_token_presentations')
    for seed in SEEDS:
        a = trace_lookup[seed,ARMS[0]]
        for arm in ARMS[1:]:
            b = trace_lookup[seed,arm]
            require(all(a[k] == b[k] for k in equal_keys),'three-arm identical conditions/input stream')
            require(all(a['loss_history'][0][k] == b['loss_history'][0][k] for k in ('mean_ce','pair_max')),'equal first preupdate common objectives')
        for control in CONTROLS:
            a,b = [flag_lookup[seed,arm] for arm in (control,CANDIDATE)]
            normal = compare_normal(raw_lookup[seed,control],raw_lookup[seed,CANDIDATE],data); inside = normal['interior4']
            pairs.append(dict(seed=seed,control_arm=control,candidate_arm=CANDIDATE,
                control_full_pass=a['retention_pass'] and a['interior_pass'],candidate_full_pass=b['retention_pass'] and b['interior_pass'],
                normal_by_domain=normal,interior_train_answer_gain=inside['TRAIN']['answer_gain'],interior_train_pair_gain=inside['TRAIN']['query_pair_gain'],
                interior_holdout_answer_gain=inside['HOLDOUT']['answer_gain'],interior_holdout_pair_gain=inside['HOLDOUT']['query_pair_gain']))
    gate,eligible,strict,components,headroom = fixed_gate(pairs)
    terminal_contrasts = terminal_comparisons(terminal,pairs); work = observed_work(traces,records,states)
    require(work == WORK,'measured complete scientific work')
    value = dict(candidate_gate=gate,eligible_seed_count=sum(eligible),strict_interior_gains=strict,gate_components=components,
        strict_interior_headroom=headroom,strict_interior_ceiling=any(n == 0 for row in headroom.values() for n in row.values()),
        paired_conditions_valid=True,all_replays=True,evaluation_policy='native_before',seed_results=flags,paired_comparisons=pairs,
        terminal=terminal,terminal_contrasts=terminal_contrasts,**work)
    check_summary(value)
    return dict(scores=metrics,terminal=terminal,terminal_contrasts=terminal_contrasts),value


def report_results(value, emit):
    check_summary(value)
    for row in value['seed_results']:
        emit('C346 seed result',{k:v for k,v in row.items() if k != 'normal_by_domain'})
        for domain,split in itertools.product(DOMAINS,SPLITS):
            emit('C346 normal result',dict(seed=row['seed'],arm=row['arm'],domain=domain,split=split,**row['normal_by_domain'][domain][split]))
    for row in value['paired_comparisons']:
        emit('C346 paired comparison',{k:v for k,v in row.items() if k != 'normal_by_domain'})
        for domain,split in itertools.product(DOMAINS,SPLITS):
            emit('C346 normal contrast',dict(seed=row['seed'],control_arm=row['control_arm'],candidate_arm=CANDIDATE,
                domain=domain,split=split,**row['normal_by_domain'][domain][split]))
    for row in value['terminal']: emit('C346 terminal objective',row)
    for row in value['terminal_contrasts']: emit('C346 terminal contrast',row)
    emit('C346 strict interior gains',value['strict_interior_gains'])
    emit('C346 gate components',value['gate_components'])
    emit('C346 primary headroom',dict(by_split=value['strict_interior_headroom'],ceiling=value['strict_interior_ceiling']))
    emit('C346 measured work',{k:value[k] for k in WORK})




def load_states(path):
    value = torch.load(path,map_location='cpu',weights_only=True)
    require(set(value) == {'schema','identities','states'} and value['schema'] == 'fold-c346-trained-models-v1'
            and value['identities'] == [list(z) for z in identities()] and len(value['states']) == len(identities()),'model bundle')
    return value['states']


def run_training(out, data_out, cx, root, pins, read):
    p = previous(); data,old,new = p.load_data(data_out,read); before = digest((data,old,new))
    tables,y = prepared(data,old,new,cx); traces,states = [],[]
    for seed in SEEDS:
        models = make_models(seed,cx[-1])
        for arm in ARMS:
            trace,state = train_one(seed,arm,models[arm],tables,y,data['TRAIN'],cx,root,pins)
            traces.append(trace); states.append(state)
        del models
    with (out/'trained-models.pt').open('xb') as stream:
        torch.save(dict(schema='fold-c346-trained-models-v1',identities=[list(z) for z in identities()],states=states),stream)
    saved = load_states(out/'trained-models.pt')
    require([p.state_hash(v) for v in saved] == [p.state_hash(v) for v in states],'checkpoint roundtrip')
    records = []
    for (seed,arm),state in zip(identities(),saved,strict=True):
        model = make_model(seed,cx[-1]); p.source().base().check_dependencies(root,pins,cx,model)
        model.eval(); model.requires_grad_(False); raw,receipts = {},{}
        for kind in ('evaluation','replay'):
            model.load_state_dict(state,strict=True); require(p.state_hash(model.state_dict()) == p.state_hash(state),'loaded state')
            raw[kind],receipts[kind] = p.readouts().measure(model,'native_before',data,old,new,cx)
            require(p.state_hash(model.state_dict()) == p.state_hash(state),'evaluation weight mutation')
        records.append(dict(seed=seed,arm=arm,state_sha256=p.state_hash(state),evaluation_policy='native_before',raw=raw,receipts=receipts))
        print(f'[C346] seed={seed} arm={arm} native_saved_evaluation_and_replay=COMPLETE',flush=True)
    metrics,value = analyze(traces,records,saved,data,cx,tables,y)
    require(digest((data,old,new)) == before,'data/prompt mutation')
    with (out/'evaluations.pt').open('xb') as stream:
        torch.save(dict(schema='fold-c346-evaluations-v1',records=records),stream)
    for name,item in (('experiment-plan.json',manifest()),('training-traces.json',traces),('measurements.json',metrics),('validation-summary.json',value)):
        with (out/name).open('xb') as stream: stream.write(blob(item))
    return value


def semantic_recheck(out, data_out, cx, read):
    data,old,new = previous().load_data(data_out,read); tables,y = prepared(data,old,new,cx)
    archive = torch.load(out/'evaluations.pt',map_location='cpu',weights_only=True)
    require(set(archive) == {'schema','records'} and archive['schema'] == 'fold-c346-evaluations-v1','evaluation schema')
    metrics,value = analyze(read(out/'training-traces.json'),archive['records'],load_states(out/'trained-models.pt'),data,cx,tables,y)
    for name,item in (('experiment-plan.json',manifest()),('measurements.json',metrics),('validation-summary.json',value)):
        require(blob(read(out/name)) == blob(item),'saved training reconstruction:'+name)
    return value


def native_preflight(data_out, cx, root, pins, read):
    p = previous(); x = cx[-1]; data,old,new = p.load_data(data_out,read); tables,y = prepared(data,old,new,cx)
    for seed in SEEDS:
        events,family = schedule(seed,data['TRAIN'],x); validate_training_pairs(data['TRAIN'],y,events,x)
        chosen = length_mask(events,family); actual_exposure(events,family,chosen)
        require(input_accounting(tables,y,events,family,chosen)[0] == 3168000, 'preflight identical mixed45 tokens')
    events,family = schedule(SEEDS[0],data['TRAIN'],x); selected = length_mask(events,family)
    model = make_model(SEEDS[0],x); p.source().base().check_dependencies(root,pins,cx,model)
    with torch.no_grad():
        w = model.read.output.weight; w.copy_(torch.sin(torch.arange(w.numel(),dtype=torch.float64).reshape_as(w))*.03)
    initial = p.state_hash(model.state_dict())
    for arm in ARMS:
        optimizer = optimizer_for(model,arm,x); verify_optimizer(optimizer,model,arm,x)
        require(not optimizer.state,'zero-step preflight optimizer')
    for arm,cycle,kind in itertools.product(ARMS,range(2),('original','interior4')):
        chosen_tokens = []; chosen_ids = []
        for language in ('en','ja'):
            found = None
            for i,event in enumerate(events):
                if int(event[0,0]) != 4: continue
                tokens,ids = select_tokens(tables,event,family[i],selected[cycle*CYCLE+i])
                for j in range(24):
                    a,b = ids[2*j:2*j+2].tolist()
                    if data['TRAIN'][a]['language'] == language and bool(family[i,j]) == (kind == 'interior4'):
                        found = tokens[2*j:2*j+2],(a,b); break
                if found is not None: break
            require(found is not None, 'native preflight language/family pair coverage')
            chosen_tokens.append(found[0]); chosen_ids.extend(found[1])
        tokens = torch.cat(chosen_tokens); ids = torch.tensor(chosen_ids,dtype=torch.int64)
        validate_batch_pairs(data['TRAIN'],y,ids); target = y[ids]
        require(tokens.shape == (4,64), 'native complete-pair frame'); tasks = torch.zeros(4,dtype=torch.int64); model.train()
        with torch.no_grad(): expected = model(tokens,tasks)
        model.zero_grad(set_to_none=True)
        with torch.enable_grad(),p.readouts().readout(model,x.wide,'native_before') as stats:
            logits = model(tokens,tasks); p.readouts().same(expected,logits.detach())
            loss,ce,pair_max = objective(logits,target,arm)
            require(float(ce.detach()) > 0 and float(pair_max.detach()) > 0, 'nontrivial native objectives'); loss.backward()
        require(stats == dict(calls=1,query_calls=2,rows=4,grad_calls=1) and model.read.query.weight.grad is not None
                and bool((model.read.query.weight.grad != 0).any())
                and all(v.grad is None or bool(torch.isfinite(v.grad).all()) for v in model.parameters()), 'native pair-max/mean backward')
    require(p.state_hash(model.state_dict()) == initial, 'preflight changed weights')
    print('C346_native_preflight=PASS;schedules=5;forwards=24;rows=96;backward=12;updates=0;optimizer_configurations=3',flush=True)
    return identities()
