"""C340: replace original length-four TRAIN tokens by length-five tokens only."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import math
import re
import torch
from torch.nn import functional as F

EXPERIMENT_ID = 'C340-v5b-length5-training'
STAGE = 'V5-B-LENGTH5-TRAINING'
SEEDS = tuple(range(340001, 340006))
ORDERS = tuple(range(340101, 340106))
ARMS = ('original4', 'original5')
PROFILES = ('repeat', 'shared_prefix', 'shared_suffix')
CYCLE, STEPS, FIT_RNG = 1200, 2400, 612000
RATES = (.005, .0005)
TRAIN_TOKENS = {'original4':3110400, 'original5':3225600}
DOMAINS = tuple('original'+str(n) for n in range(2, 7))+('interior4',)
OWN = ('fold_lm/v05_benchmarks/model_c340_length5_training.py',
       'tools/c340_execution.py', 'tests_lm/test_v05_c340_length5_training.py',
       'tests_lm/test_v05_c340_execution.py', 'tools/run_c340.ps1',
       'tools/invoke_c340.ps1', 'docs/experiment-ledger-addendum-c340-preregistration.md')
OUTPUTS = ('experiment-plan.json', 'training-traces.json', 'trained-models.pt',
           'evaluations.pt', 'measurements.json', 'validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 56, 6258, 231
SOURCE_COUNT, INPUT_COUNT = 902, 6243
WORK = dict(training_models=10, evaluation_models=10, checkpoint_states=10,
    optimizer_creations=10, train_steps=24000, gradient_calls=24000, optimizer_steps=24000,
    training_rows=1152000, model_forward_calls=27420, row_presentations=1480320,
    core_forward_calls=109680, query_projection_calls=54840, model_state_loads=20,
    checkpoint_bundle_loads=1, new_checkpoint_writes=1, network_calls=0)
MANIFEST_SHA = '8016f388949a574a3609a563d1005c99b1c83455cd31148471f60a7c9b832914'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def previous():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c332_trained_first_mean_query')


def support():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c338_value_support_training')


def identities():
    return list(itertools.product(SEEDS, ARMS))


def length_for(arm):
    require(type(arm) is str and arm in ARMS, 'registered arm')
    return 4 if arm == 'original4' else 5


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE,
        acceptance_base='aea1286c205e274611e63b14ddd26e5c99884f1f',
        parent_execution='f58c22f83fe7c41c451d5d0bcf26c249ab21908b',
        parent_summary='304dec1fcbb6532da968fd21c337f39079f4abb1cc305893722e466636ef4dbf',
        parent_envelope='db81d2dba1bd8a1b2f850c3b5a7833a9b95b7a24d8cddc984fc1e3a5e1195be3',
        question='does replacing original4 TRAIN tokens by canonical original5 tokens improve never-trained original6 transfer at equal updates while retaining shorter tasks',
        seeds=list(SEEDS), orders=list(ORDERS), arms=list(ARMS), cycle=CYCLE, steps=STEPS, fit_rng=FIT_RNG,
        changed='only original-family schedule-slot4 tokens: canonical length4 versus canonical length5 normal TRAIN prompts',
        held='fresh paired weights,logical192 TRAIN rows,value split,targets,1200events repeated twice,batch4 family mask,original2/3 and interior4 tokens,ordinaryCE,native readout,optimizer,rates,capacity,scorers',
        train_lengths={'original4':[2,3,4], 'original5':[2,3,5]}, interior_train_length=4,
        actual_per_row_exposure={'original4':dict(original2=200,original3=200,original4=100,interior4=100),
                                'original5':dict(original2=200,original3=200,original5=100,interior4=100)},
        never_train='original6 and all HOLDOUT logical rows;masked prompts never enter training',
        compute_boundary='updates/rows/padded64 frames are equal;nonpadding tokens including BOS/EOS are measured per arm and differ',
        nonpadding_training_tokens_per_model=dict(TRAIN_TOKENS),
        substitution='original5 normal strings retain canonical source_id,target,profile and language;original4 schedule index remains4 so interior4 selection is unchanged',
        optimizer='core_slow AdamW noncore.005/core.0005 betas.9/.999 eps1e-8 decay0/globalclip1;one optimizer,ordinary mean CE256',
        gate='all5candidate full original2..6 and interior4 gates;each seed nonnegative original6 answer/pair gains,pooled original2..5 gains,interior4 gains;strict total original6 answer AND pair gains',
        saturation='perfect control ties remain valid negatives if strict aggregate original6 gains are absent',
        support_counts='four raw all256-argmax answer kinds descriptive only;no auxiliary support loss or supplied-value inference filter',
        thresholds=dict(accuracy=.90, query_pair=.80, evidence_drop=.35, query_drop=.35, both_order=.80),
        parameters=14256, core_parameters=3328, slots=64, precision='cpu float64', threads=2,
        evaluation_policy='native_before in both arms;full114views per state,exact argmax and1e-9 replay',
        preflight='all5 schedules/both token tables;discarded native model,2arms*2families*2languages;8forwards/16rows/4backwards/0updates',
        boundary='seen canonical templates,reused value split,one training-boundary intervention;no universal length-generalization mechanism,optimal curriculum or capacity claim',
        source_count=SOURCE_COUNT, input_count=INPUT_COUNT, parent_files=467,
        own_tests=OWN_TESTS, full_tests=FULL_TESTS, modules=MODULES, outputs=list(OUTPUTS),
        raw_logit_payload_bytes=672399360, gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C340 manifest seal')


def prepared(data, old, new, cx):
    """Build both TRAIN-only tables; original slot4 is replaced, never interior4."""
    p = previous(); base = p.source().base()
    require(digest(data) == base.DATA_SHA and digest(old) == base.PROMPTS_SHA, 'canonical TRAIN sources')
    baseline, y = p.prepared(data, old, new, cx)
    tables = {arm:{family:{key:value.clone() for key,value in rows.items()}
                   for family,rows in baseline.items()} for arm in ARMS}
    for profile in PROFILES:
        records = old['5']['TRAIN'][profile]
        require(type(records) is list and len(records) == len(data['TRAIN']) == 192, 'length5 TRAIN records')
        tokens = []
        for row,item in zip(data['TRAIN'], records, strict=True):
            require(item['source_id'] == row['id'] and type(item['source_id']) is type(row['id'])
                    and type(item['target']) is int and item['target'] == row['target'], 'length5 teacher alignment')
            text = item['views']['normal']
            require(type(text) is str and text and '\x00' not in text, 'normal TRAIN string')
            tokens.append(cx[-1].wide.prefix_tensor(text))
        tables['original5']['original'][4,profile] = torch.stack(tokens)
    validate_tables(tables, y)
    return tables, y


def validate_tables(tables, y):
    keys = set(itertools.product((2,3,4), PROFILES))
    require(set(tables) == set(ARMS) and isinstance(y,torch.Tensor) and y.shape == (192,)
            and y.dtype == torch.int64 and y.device.type == 'cpu', 'paired TRAIN tables/labels')
    for arm in ARMS:
        require(set(tables[arm]) == {'original','interior4'}, 'TRAIN family inventory')
        for table in tables[arm].values():
            require(set(table) == keys and all(isinstance(z,torch.Tensor) and z.shape == (192,64)
                    and z.dtype == torch.int64 and z.device.type == 'cpu'
                    and bool(((z >= 0)&(z <= 258)).all()) for z in table.values()), 'TRAIN tensor contract')
    for family in ('original','interior4'):
        changed = {k for k in keys if not torch.equal(tables['original4'][family][k], tables['original5'][family][k])}
        require(changed == ({(4,p) for p in PROFILES} if family == 'original' else set()), 'exact token substitution boundary')


def make_model(seed, x):
    require(type(seed) is int and seed in SEEDS, 'fresh C340 seed')
    c = x.c
    ref = c.c278.MeanFinalDualReadout(c.factory.new_model(seed), seed, c.reader, c.c269.query_span_mask)
    model = x.policy.configure(x.wide.LengthReadout(ref), 'core_slow')
    require(type(model) is x.wide.LengthReadout and model.backbone.config.max_tokens == 64
            and model.backbone.core.config.slots == 64, 'native architecture')
    require(sum(v.numel() for v in model.parameters()) == 14256
            and sum(v.numel() for v in model.backbone.core.parameters()) == 3328, 'capacity')
    require(c.base.fingerprint(model) == c.base.fingerprint(ref) and list(model.state_dict()) == list(ref.state_dict()), 'native initialization')
    require(all(v.requires_grad and v.dtype == torch.float64 and v.device.type == 'cpu' for v in model.parameters()), 'precision/gradient')
    x.policy.parameter_groups(model, 'core_slow')
    return model


def make_pair(seed, x):
    models = {arm:make_model(seed, x) for arm in ARMS}; p = previous()
    require(p.state_hash(models['original4'].state_dict()) == p.state_hash(models['original5'].state_dict()), 'paired initial weights')
    ptrs = [{v.data_ptr() for v in m.parameters() if v.numel()} for m in models.values()]
    require(not ptrs[0]&ptrs[1], 'independent paired storage')
    return models


def schedule(seed, rows, x):
    require(type(seed) is int and seed in SEEDS and len(rows) == 192, 'TRAIN schedule identity')
    curriculum = previous().source().curriculum()
    events = x.parent.plan_for_order(ORDERS[SEEDS.index(seed)], 'two_to_four', rows, x.p312, x.pairs)
    curriculum.validate_schedule(events)
    return events, curriculum.family_mask(events, 'batch4')


def actual_exposure(arm, events, mask):
    """Count actual source-domain presentations separately from unchanged schedule slots."""
    length = length_for(arm); require(len(events) == len(mask) == CYCLE, 'exposure schedule')
    result = {k:[0]*192 for k in ('original2','original3','original4','original5','original6','interior4')}
    for event, selected in zip(events.tolist(), mask.tolist(), strict=True):
        for (n,profile,a,b),family in zip(event, selected, strict=True):
            require(n in (2,3,4) and profile in (0,1,2) and family in (0,1)
                    and (n == 4 or family == 0), 'exposure domain')
            domain = 'interior4' if family else 'original'+str(length if n == 4 else n)
            result[domain][a] += 1; result[domain][b] += 1
    expected = {k:(100 if k in ('original2','original3') else 50 if k in ('original'+str(length),'interior4') else 0) for k in result}
    require(all(rows == [expected[k]]*192 for k,rows in result.items()), 'exact actual per-row exposure')
    return result


def token_presentations(tables, events, mask):
    """One-cycle nonpadding byte-token exposures, preserving actual family assignment."""
    sizes = {f:{k:(v != 256).sum(1) for k,v in rows.items()} for f,rows in tables.items()}
    total = 0
    for event, selected in zip(events,mask,strict=True):
        n,p = map(int,event[0,:2]); ids = event[:,2:].flatten(); use = selected.repeat_interleave(2).bool()
        old = sizes['original'][n,PROFILES[p]][ids]; inside = sizes['interior4'][n,PROFILES[p]][ids]
        total += int(torch.where(use,inside,old).sum())
    return total


def optimize(model, arm, tables, y, events, mask, x):
    """Only the chosen TRAIN tensors and teacher targets enter the fit loop."""
    length_for(arm); p = previous()
    require(len(events) == len(mask) == CYCLE and STEPS == 2*CYCLE, 'registered cycles')
    torch.manual_seed(FIT_RNG); opt = x.policy.optimizer_for(model, 'core_slow'); opt_id = id(opt)
    initial = p.state_hash(model.state_dict()); core_initial = p.state_hash(model.backbone.core.state_dict())
    losses,rates,counts,indices = [],[],[],[]; union = {}; boundary = None; continuation = None
    model.train(); nonpadding = 0
    with torch.enable_grad(), p.readouts().readout(model, x.wide, 'native_before') as stats:
        for step in range(STEPS):
            if step == CYCLE:
                continuation = dict(weights=p.state_hash(model.state_dict()), optimizer=p.state_hash(opt.state_dict()))
                require(continuation == boundary, 'optimizer/weight reset')
            require(id(opt) == opt_id, 'optimizer replaced'); x.policy.verify_optimizer(opt, model, 'core_slow')
            rate = [g['lr'] for g in opt.param_groups]; require(rate == list(RATES), 'fixed rates'); rates.append(rate)
            index = step%CYCLE; indices.append(index); opt.zero_grad(set_to_none=True)
            tokens,ids = p.source().curriculum().select_tokens(tables, events[index], mask[index])
            require(len(ids) == 48, 'TRAIN batch')
            nonpadding += int((tokens != 256).sum())
            logits = model(tokens, torch.zeros(len(ids), dtype=torch.int64)); x.c.p267.check_logits(logits, len(ids))
            loss = F.cross_entropy(logits, y[ids])
            require(bool(torch.isfinite(loss)) and float(loss.detach()) >= 0, 'finite CE')
            losses.append(float(loss.detach())); loss.backward()
            got = {name:v.numel() for name,v in model.named_parameters() if v.grad is not None}
            require(got, 'missing gradients'); counts.append(sum(got.values())); union.update(got)
            torch.nn.utils.clip_grad_norm_(list(model.parameters()), 1., error_if_nonfinite=True); opt.step()
            if step+1 == CYCLE: boundary = dict(weights=p.state_hash(model.state_dict()), optimizer=p.state_hash(opt.state_dict()))
            if (step+1)%200 == 0:
                print(f'[C340] arm={arm} step={step+1}/{STEPS} ce={losses[-1]:.6f}', flush=True)
    model.eval(); require(boundary is not None and boundary == continuation, 'continuous optimizer')
    require(stats == dict(calls=STEPS,query_calls=2*STEPS,rows=48*STEPS,grad_calls=STEPS), 'TRAIN receipt')
    state = {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    require(p.state_hash(state) == p.state_hash(model.state_dict()) and all(v.numel() == 0 or state[k].data_ptr() != v.data_ptr()
            for k,v in model.state_dict().items()), 'deep checkpoint')
    return dict(arm=arm, readout_mode='native_before', original_training_length=length_for(arm), steps=STEPS,
        initial_sha256=initial, final_sha256=p.state_hash(state), core_initial_sha256=core_initial,
        core_final_sha256=p.state_hash(model.backbone.core.state_dict()), ce_history=losses,
        optimizer_group_lrs=rates, gradient_parameter_counts=counts, gradient_union=dict(sorted(union.items())),
        event_indices=indices, policy_receipt=dict(stats), boundary=boundary, continuation=continuation,
        optimizer_creations=1, intermediate_evaluations=0, nonpadding_token_presentations=nonpadding), state


def train_one(seed, arm, model, tables, y, rows, cx, root, pins):
    p = previous(); x = cx[-1]; p.source().base().check_dependencies(root,pins,cx,model)
    events,mask = schedule(seed,rows,x); before = p.training_fingerprint(tables,y,events,mask)
    exposure = actual_exposure(arm,events,mask)
    print(f'[C340] seed={seed} arm={arm} phase=training',flush=True)
    with x.c.p267.counted(model,x.c.core) as (calls,cores):
        trace,state = optimize(model,arm,tables,y,events,mask,x)
    require(calls == [2400,115200] and cores[0] == 9600, 'measured TRAIN work')
    require(p.training_fingerprint(tables,y,events,mask) == before, 'TRAIN input mutation')
    require(trace['nonpadding_token_presentations'] == 2*token_presentations(tables,events,mask) == TRAIN_TOKENS[arm], 'measured TRAIN token exposure')
    trace.update(seed=seed, training_input_sha256=before, logical_training_sha256=p.state_hash(dict(targets=y,events=events,mask=mask)),
        schedule_sha256=digest(events.tolist()), mask_sha256=digest(mask.tolist()),
        family_exposure_per_cycle=p.source().curriculum().exposure(events,mask), actual_exposure_per_cycle=exposure)
    return trace,state


def check_trace(t, rows, x, tables, y):
    p = previous(); require(type(t['seed']) is int and t['seed'] in SEEDS and t['arm'] in ARMS, 'trace identity')
    events,mask = schedule(t['seed'],rows,x)
    require(t['readout_mode'] == 'native_before' and type(t['original_training_length']) is int
            and t['original_training_length'] == length_for(t['arm']), 'trace token/readout policy')
    require(type(t['steps']) is int and t['steps'] == STEPS and t['event_indices'] == list(range(CYCLE))*2
            and all(type(v) is int for v in t['event_indices']), 'event budget/order')
    require(t['schedule_sha256'] == digest(events.tolist()) and t['mask_sha256'] == digest(mask.tolist())
            and t['family_exposure_per_cycle'] == p.source().curriculum().exposure(events,mask)
            and t['actual_exposure_per_cycle'] == actual_exposure(t['arm'],events,mask), 'actual exposure reconstruction')
    require(type(t['nonpadding_token_presentations']) is int and t['nonpadding_token_presentations'] == 2*token_presentations(tables,events,mask) == TRAIN_TOKENS[t['arm']], 'reconstructed token exposure')
    require(t['training_input_sha256'] == p.training_fingerprint(tables,y,events,mask)
            and t['logical_training_sha256'] == p.state_hash(dict(targets=y,events=events,mask=mask)), 'actual TRAIN token fingerprint')
    require(t['optimizer_group_lrs'] == [list(RATES)]*STEPS and len(t['ce_history']) == STEPS
            and all(type(v) is float and math.isfinite(v) and v >= 0 for v in t['ce_history']), 'rates/CE history')
    union,counts = t['gradient_union'],t['gradient_parameter_counts']
    require(union and all(type(k) is str and type(v) is int and v > 0 for k,v in union.items()) and 0 < sum(union.values()) <= 14256
            and len(counts) == STEPS and all(type(v) is int and 0 < v <= sum(union.values()) for v in counts), 'gradient inventory')
    for k in ('initial_sha256','final_sha256','core_initial_sha256','core_final_sha256','training_input_sha256','logical_training_sha256'):
        require(type(t[k]) is str and re.fullmatch('[0-9a-f]{64}',t[k]), 'state/input fingerprint')
    require(t['initial_sha256'] != t['final_sha256'] and t['core_initial_sha256'] != t['core_final_sha256'], 'trained state')
    require(t['boundary'] == t['continuation'] and set(t['boundary']) == {'weights','optimizer'}
            and all(type(v) is str and re.fullmatch('[0-9a-f]{64}',v) for v in t['boundary'].values()), 'continued state')
    require(type(t['optimizer_creations']) is int and t['optimizer_creations'] == 1 and type(t['intermediate_evaluations']) is int
            and t['intermediate_evaluations'] == 0 and t['policy_receipt'] == dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400), 'no restart/selection')


def fixed_gate(pairs):
    require([r['seed'] for r in pairs] == list(SEEDS) and all(type(r['seed']) is int for r in pairs), 'all paired seeds')
    names = ('six_answer_gain','six_pair_gain','short_answer_gain','short_pair_gain','interior_answer_gain','interior_pair_gain')
    eligible = []
    for r in pairs:
        require(type(r['candidate_full_pass']) is bool and all(type(r[k]) is int for k in names), 'gate types')
        eligible.append(r['candidate_full_pass'] and all(r[k] >= 0 for k in names))
    strict = sum(r['six_answer_gain'] for r in pairs) > 0 and sum(r['six_pair_gain'] for r in pairs) > 0
    return all(eligible) and strict, eligible


def check_summary(v):
    p = previous()
    require(all(type(v[k]) is int and v[k] == n for k,n in WORK.items()) and v['paired_conditions_valid'] is True
            and v['all_replays'] is True and v['evaluation_policy'] == 'native_before', 'work/integrity')
    require([(r['seed'],r['arm']) for r in v['seed_results']] == identities() and len(v['paired_comparisons']) == 5, 'cohort')
    for i,pair in enumerate(v['paired_comparisons']):
        for offset,key in ((0,'control_full_pass'),(1,'candidate_full_pass')):
            f = v['seed_results'][2*i+offset]
            require(set(f['original_pass']) == set(map(str,range(2,7))) and all(type(b) is bool for b in f['original_pass'].values())
                    and type(f['interior_pass']) is bool and f['retention_pass'] is all(f['original_pass'].values())
                    and pair[key] is (f['retention_pass'] and f['interior_pass']), 'full gate binding')
            require(type(f['training_nonpadding_tokens']) is int and f['training_nonpadding_tokens'] == TRAIN_TOKENS[f['arm']], 'measured effective tokens')
            require(set(f['support']) == set(DOMAINS), 'support domains')
            for r in f['support'].values():
                kinds = support().audit().KINDS
                require(set(r) == {'answers',*kinds} and r['answers'] == 288 and type(r['answers']) is int
                        and all(type(r[k]) is int and r[k] >= 0 for k in kinds)
                        and sum(r[k] for k in kinds) == 288, 'support partition')
        old,inside = pair['original_by_length'],pair['interior']
        require(set(old) == set(map(str,range(2,7))), 'all comparison domains')
        for d,z in [('interior4',inside)]+[('original'+n,z) for n,z in old.items()]:
            p.contrast_check(z)
            require(z['control_correct'] == v['seed_results'][2*i]['support'][d]['correct']
                    and z['candidate_correct'] == v['seed_results'][2*i+1]['support'][d]['correct'], 'support/contrast binding')
        require(pair['six_answer_gain'] == old['6']['answer_gain'] and pair['six_pair_gain'] == old['6']['query_pair_gain']
                and pair['short_answer_gain'] == sum(old[str(n)]['answer_gain'] for n in range(2,6))
                and pair['short_pair_gain'] == sum(old[str(n)]['query_pair_gain'] for n in range(2,6))
                and pair['interior_answer_gain'] == inside['answer_gain'] and pair['interior_pair_gain'] == inside['query_pair_gain'], 'gate count binding')
    gate,eligible = fixed_gate(v['paired_comparisons'])
    require(v['candidate_gate'] is gate and type(v['eligible_seed_count']) is int and v['eligible_seed_count'] == sum(eligible), 'fixed gate')


def analyze(traces, records, states, data, cx, tables, y):
    p = previous(); q = p.readouts(); validate_tables(tables,y)
    require([(t['seed'],t['arm']) for t in traces] == [(r['seed'],r['arm']) for r in records] == identities()
            and len(states) == 10, 'complete trained cohort')
    metrics,flags = [],[]
    for t,r,state in zip(traces,records,states,strict=True):
        check_trace(t,data['TRAIN'],cx[-1],tables[t['arm']],y)
        require(set(r) == {'seed','arm','state_sha256','evaluation_policy','raw','receipts'}
                and r['state_sha256'] == t['final_sha256'] == p.state_hash(state) and r['evaluation_policy'] == 'native_before'
                and set(r['raw']) == set(r['receipts']) == {'evaluation','replay'}, 'state binding')
        for mode in ('evaluation','replay'):
            p.source().base().validate_raw(r['raw'][mode],data,cx)
            require(blob(r['receipts'][mode]) == blob(dict(calls=171,query_calls=342,rows=16416,grad_calls=0)), 'evaluation receipt')
        require(p.source().base().replay_error(r['raw']['evaluation'],r['raw']['replay'],data,cx) <= 1e-9, 'saved replay')
        score,f = q.summarize_mode(r['raw']['evaluation'],data,cx)
        metrics.append(dict(seed=t['seed'],arm=t['arm'],score=score))
        flags.append(dict(seed=t['seed'],arm=t['arm'],training_nonpadding_tokens=t['nonpadding_token_presentations'],support=support().support_report(r['raw']['evaluation'],data),**f))
    pairs = []
    for i,seed in enumerate(SEEDS):
        a,b = traces[2*i:2*i+2]
        require(all(a[k] == b[k] for k in ('initial_sha256','core_initial_sha256','logical_training_sha256',
            'schedule_sha256','mask_sha256','family_exposure_per_cycle','event_indices','optimizer_group_lrs'))
            and a['training_input_sha256'] != b['training_input_sha256'], 'paired conditions/token intervention')
        compare = q.compare(records[2*i]['raw']['evaluation'],records[2*i+1]['raw']['evaluation'],data,p.source().base())
        old,inside = compare['original_by_length'],compare['interior']
        pairs.append(dict(seed=seed,control_full_pass=flags[2*i]['retention_pass'] and flags[2*i]['interior_pass'],
            candidate_full_pass=flags[2*i+1]['retention_pass'] and flags[2*i+1]['interior_pass'],
            six_answer_gain=old['6']['answer_gain'],six_pair_gain=old['6']['query_pair_gain'],
            short_answer_gain=sum(old[str(n)]['answer_gain'] for n in range(2,6)),
            short_pair_gain=sum(old[str(n)]['query_pair_gain'] for n in range(2,6)),
            interior_answer_gain=inside['answer_gain'],interior_pair_gain=inside['query_pair_gain'],**compare))
    gate,eligible = fixed_gate(pairs)
    value = dict(candidate_gate=gate,eligible_seed_count=sum(eligible),paired_conditions_valid=True,all_replays=True,
        evaluation_policy='native_before',seed_results=flags,paired_comparisons=pairs,**WORK)
    check_summary(value)
    return metrics,value


def load_states(path):
    v = torch.load(path,map_location='cpu',weights_only=True)
    require(set(v) == {'schema','identities','states'} and v['schema'] == 'fold-c340-trained-models-v1'
            and v['identities'] == [list(z) for z in identities()] and len(v['states']) == 10, 'model bundle')
    return v['states']


def run_training(out, data_out, cx, root, pins, read):
    p = previous(); data,old,new = p.load_data(data_out,read); before = digest((data,old,new))
    tables,y = prepared(data,old,new,cx); traces,states = [],[]
    for seed in SEEDS:
        models = make_pair(seed,cx[-1])
        for arm in ARMS:
            trace,state = train_one(seed,arm,models[arm],tables[arm],y,data['TRAIN'],cx,root,pins)
            traces.append(trace); states.append(state)
        del models
    with (out/'trained-models.pt').open('xb') as stream:
        torch.save(dict(schema='fold-c340-trained-models-v1',identities=[list(z) for z in identities()],states=states),stream)
    saved = load_states(out/'trained-models.pt')
    require([p.state_hash(v) for v in saved] == [p.state_hash(v) for v in states], 'checkpoint roundtrip')
    records = []
    for (seed,arm),state in zip(identities(),saved,strict=True):
        model = make_model(seed,cx[-1]); p.source().base().check_dependencies(root,pins,cx,model)
        model.eval(); model.requires_grad_(False); raw,receipts = {},{}
        for kind in ('evaluation','replay'):
            model.load_state_dict(state,strict=True); require(p.state_hash(model.state_dict()) == p.state_hash(state), 'loaded state')
            raw[kind],receipts[kind] = p.readouts().measure(model,'native_before',data,old,new,cx)
            require(p.state_hash(model.state_dict()) == p.state_hash(state), 'evaluation weight mutation')
        records.append(dict(seed=seed,arm=arm,state_sha256=p.state_hash(state),evaluation_policy='native_before',raw=raw,receipts=receipts))
        print(f'[C340] seed={seed} arm={arm} native_saved_evaluation_and_replay=COMPLETE',flush=True)
    metrics,value = analyze(traces,records,saved,data,cx,tables,y)
    require(digest((data,old,new)) == before, 'data/prompt mutation')
    with (out/'evaluations.pt').open('xb') as stream:
        torch.save(dict(schema='fold-c340-evaluations-v1',records=records),stream)
    for name,item in (('experiment-plan.json',manifest()),('training-traces.json',traces),('measurements.json',metrics),('validation-summary.json',value)):
        with (out/name).open('xb') as stream: stream.write(blob(item))
    return value


def semantic_recheck(out, data_out, cx, read):
    data,old,new = previous().load_data(data_out,read); tables,y = prepared(data,old,new,cx)
    archive = torch.load(out/'evaluations.pt',map_location='cpu',weights_only=True)
    require(set(archive) == {'schema','records'} and archive['schema'] == 'fold-c340-evaluations-v1', 'evaluation schema')
    metrics,value = analyze(read(out/'training-traces.json'),archive['records'],load_states(out/'trained-models.pt'),data,cx,tables,y)
    for name,item in (('experiment-plan.json',manifest()),('measurements.json',metrics),('validation-summary.json',value)):
        require(blob(read(out/name)) == blob(item), 'saved training reconstruction:'+name)
    return value


def native_preflight(data_out, cx, root, pins, read):
    p = previous(); x = cx[-1]; data,old,new = p.load_data(data_out,read); tables,y = prepared(data,old,new,cx)
    for seed in SEEDS:
        events,mask = schedule(seed,data['TRAIN'],x)
        for arm in ARMS: actual_exposure(arm,events,mask)
    model = make_model(SEEDS[0],x); p.source().base().check_dependencies(root,pins,cx,model)
    with torch.no_grad():
        w = model.read.output.weight; w.copy_(torch.sin(torch.arange(w.numel(),dtype=torch.float64).reshape_as(w))*.03)
    initial = p.state_hash(model.state_dict())
    ids = [next(i for i,r in enumerate(data['TRAIN']) if r['language'] == lang) for lang in ('en','ja')]
    for arm,family in itertools.product(ARMS,('original','interior4')):
        tokens = tables[arm][family][4,'repeat'][ids]; tasks = torch.zeros(2,dtype=torch.int64); model.train()
        with torch.no_grad(): expected = model(tokens,tasks)
        model.zero_grad(set_to_none=True)
        with torch.enable_grad(),p.readouts().readout(model,x.wide,'native_before') as stats:
            logits = model(tokens,tasks); p.readouts().same(expected,logits.detach())
            F.cross_entropy(logits,y[ids]).backward()
        require(stats == dict(calls=1,query_calls=2,rows=2,grad_calls=1) and model.read.query.weight.grad is not None
                and all(v.grad is None or bool(torch.isfinite(v.grad).all()) for v in model.parameters()), 'native backward')
    require(p.state_hash(model.state_dict()) == initial, 'preflight changed weights')
    print('C340_native_preflight=PASS;schedules=5;forwards=8;rows=16;backward=4;updates=0',flush=True)
