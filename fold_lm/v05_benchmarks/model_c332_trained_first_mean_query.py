"""C332: train and evaluate two readouts consistently at equal fixed budgets."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import math
import re
import torch
from torch.nn import functional as F

EXPERIMENT_ID = 'C332-v5b-trained-first-mean-query'
STAGE = 'V5-B-TRAINED-FIRST-MEAN-QUERY'
SEEDS = tuple(range(332001, 332006))
ORDERS = tuple(range(332101, 332106))
ARMS = ('native', 'first_mean')
CYCLE, STEPS, FIT_RNG = 1200, 2400, 612000
RATES = (.005, .0005)
OWN = ('fold_lm/v05_benchmarks/model_c332_trained_first_mean_query.py',
       'tools/c332_execution.py', 'tests_lm/test_v05_c332_trained_first_mean_query.py',
       'tools/run_c332.ps1', 'tools/invoke_c332.ps1',
       'docs/experiment-ledger-addendum-c332-preregistration.md')
OUTPUTS = ('experiment-plan.json', 'training-traces.json', 'trained-models.pt',
           'evaluations.pt', 'measurements.json', 'validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 48, 5946, 222
SOURCE_COUNT, INPUT_COUNT = 853, 2508
WORK = dict(training_models=10, evaluation_models=10, checkpoint_states=10,
            optimizer_creations=10, train_steps=24000, training_rows=1152000,
            model_forward_calls=27420, row_presentations=1480320,
            core_forward_calls=109680, query_projection_calls=54840,
            model_state_loads=20, checkpoint_bundle_loads=1,
            new_checkpoint_writes=1, network_calls=0)
MANIFEST_SHA = '2a216840891fcc13c98890d525a23054e074d88464cf546223dd693f4cb50874'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def readouts():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c331_frozen_first_mean_query')


def source():
    return readouts().source()


def state_hash(value):
    return source().state_hash(value)


def identities():
    return list(itertools.product(SEEDS, ARMS))


def policy_mode(arm):
    require(type(arm) is str and arm in ARMS, 'registered training/evaluation arm')
    return 'native_before' if arm == 'native' else 'first_mean'


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE,
        acceptance_base='bb7a025db8eb32c9de76646fc13a223e933ca155',
        parent_execution='36444b77b48ac1be5545a5346454142eb1955fb0',
        parent_summary='28f5aa242fdb26674e4f1b2bde6e752c8e4b7fea88c1fb19b6157a796acd4376',
        parent_envelope='3b3bb3a591b225d8f03d30c374c47d2307d2ca744061601aa2fd2f3356b046a0',
        question='does training with fixed first_mean/last readout improve original6 binding while retaining original2..5 and interior4 versus native mean/last at equal budget',
        seeds=list(SEEDS), orders=list(ORDERS), arms=list(ARMS), cycle=CYCLE, steps=STEPS, fit_rng=FIT_RNG,
        changed='readout used consistently for all training and evaluation: native mean/last versus .5*(mean+first-byte)/last',
        held='paired fresh initial weights,logical split,all TRAIN events/masks,2400updates,optimizer/rates,architecture,precision,scoring thresholds',
        training='C326 batch4 two_to_four schedule0..1199 repeated exactly;no original5/6 name-family exposure;no intermediate evaluation',
        exposure_per_row=[200,200,100,100], exposure_order=['original2','original3','original4','interior4'],
        optimizer='unchanged C308 core_slow factory;AdamW noncore.005/core.0005,betas.9/.999,eps1e-8,decay0;meanCE/globalclip1',
        parameters=14256, core_parameters=3328, slots=64, precision='cpu float64', threads=2,
        gate='all5 candidate full original2..6+interior gates;per-seed nonnegative original6 answer/pair gains,pooled original2..5 gains and interior gains;strictly positive original6 aggregate answer AND pair gains',
        saturation='ties allowed per seed,including perfect native controls;strict cohort gains still required;never changes C329 verdict or gate',
        thresholds=dict(accuracy=.90, query_pair=.80, evidence_drop=.35, query_drop=.35, both_order=.80),
        controls='each saved final state reload/evaluate/reload/replay with SAME training arm,1e-9+exactargmax;no cross-trained-model query-blind equality assumption',
        preflight='all5 actual schedules and both policies on original/interior English+Japanese;6forwards/12rows/4backward/0updates;discarded model',
        boundary='fresh equal-budget architecture-policy comparison,not fine-tuning accepted weights or proof of frozen-distribution-shift causality;byte not Unicode-character endpoint',
        parent_files=451, parent_file_breakdown='4science+summary+envelope+3regression records+221module receipt/log pairs',
        source_count=SOURCE_COUNT, input_count=INPUT_COUNT, own_tests=OWN_TESTS,
        full_tests=FULL_TESTS, modules=MODULES, outputs=list(OUTPUTS), raw_logit_payload_bytes=672399360,
        gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C332 manifest seal')


def make_model(seed, x):
    require(type(seed) is int and seed in SEEDS, 'fresh initialization seed')
    c = x.c
    ref = c.c278.MeanFinalDualReadout(c.factory.new_model(seed), seed, c.reader, c.c269.query_span_mask)
    model = x.policy.configure(x.wide.LengthReadout(ref), 'core_slow')
    require(type(model) is x.wide.LengthReadout and model.backbone.config.max_tokens == 64
            and model.backbone.core.config.slots == 64, 'native architecture')
    require(sum(p.numel() for p in model.parameters()) == 14256
            and sum(p.numel() for p in model.backbone.core.parameters()) == 3328, 'capacity')
    require(c.base.fingerprint(model) == c.base.fingerprint(ref)
            and list(model.state_dict()) == list(ref.state_dict()), 'fresh native state')
    require(all(p.requires_grad and p.dtype == torch.float64 and p.device.type == 'cpu'
                for p in model.parameters()), 'precision/gradient policy')
    x.policy.parameter_groups(model, 'core_slow')
    return model


def make_pair(seed, x):
    models = {arm:make_model(seed,x) for arm in ARMS}
    require(state_hash(models['native'].state_dict()) == state_hash(models['first_mean'].state_dict()), 'paired initial weights')
    pointers = [{p.data_ptr() for p in m.parameters() if p.numel()} for m in models.values()]
    require(not pointers[0] & pointers[1], 'independent paired parameter storage')
    return models


def training_fingerprint(tables, y, events, mask):
    values = [tables[family][key] for family in sorted(tables) for key in sorted(tables[family])]
    return state_hash(dict(tables=values, labels=y, events=events, mask=mask))


def schedule(seed, train_rows, x):
    require(type(seed) is int and seed in SEEDS and len(train_rows) == 192, 'fresh schedule identity')
    p = source().curriculum()
    events = x.parent.plan_for_order(ORDERS[SEEDS.index(seed)], 'two_to_four', train_rows, x.p312, x.pairs)
    p.validate_schedule(events)
    mask = p.family_mask(events, 'batch4')
    return events, mask


def prepared(data, old, new, cx):
    values = source().curriculum().previous().training(data, old, new, cx)
    tables = {key: value[0] for key, value in values.items()}
    y = values['original'][1]
    require(torch.equal(y, values['interior4'][1]), 'family targets differ')
    require(set(tables) == {'original', 'interior4'} and y.shape == (192,)
            and y.dtype == torch.int64 and y.device.type == 'cpu', 'TRAIN labels')
    keys = set(itertools.product((2,3,4), ('repeat','shared_prefix','shared_suffix')))
    require(all(set(t) == keys and all(z.shape == (192,64) and z.dtype == torch.int64
            and z.device.type == 'cpu' for z in t.values()) for t in tables.values()), 'TRAIN tables')
    return tables, y


def optimize(model, arm, tables, y, events, mask, x):
    """Only TRAIN tensors enter this function. One optimizer, two identical cycles."""
    mode = policy_mode(arm)
    require(len(events) == len(mask) == CYCLE and STEPS == 2*CYCLE, 'registered cycles')
    torch.manual_seed(FIT_RNG)
    opt = x.policy.optimizer_for(model, 'core_slow'); opt_id = id(opt)
    initial = state_hash(model.state_dict()); core_initial = state_hash(model.backbone.core.state_dict())
    losses, rates, counts, visited = [], [], [], []
    union = {}; boundary = None; continuation = None
    model.train()
    with torch.enable_grad(), readouts().readout(model, x.wide, mode) as stats:
        for step in range(STEPS):
            if step == CYCLE:
                continuation = dict(weights=state_hash(model.state_dict()), optimizer=state_hash(opt.state_dict()))
                require(continuation == boundary, 'cycle boundary reset')
            require(id(opt) == opt_id, 'optimizer replacement')
            x.policy.verify_optimizer(opt, model, 'core_slow')
            rate = [g['lr'] for g in opt.param_groups]
            require(rate == list(RATES), 'constant learning rates')
            rates.append(rate); index = step % CYCLE; visited.append(index)
            opt.zero_grad(set_to_none=True)
            tokens, ids = source().curriculum().select_tokens(tables, events[index], mask[index])
            logits = model(tokens, torch.zeros(len(ids), dtype=torch.int64)); x.c.p267.check_logits(logits, len(ids))
            loss = F.cross_entropy(logits, y[ids]); require(bool(torch.isfinite(loss)), 'nonfinite training loss')
            losses.append(float(loss.detach())); loss.backward()
            got = {name:p.numel() for name,p in model.named_parameters() if p.grad is not None}
            counts.append(sum(got.values())); union.update(got)
            torch.nn.utils.clip_grad_norm_(list(model.parameters()), 1., error_if_nonfinite=True); opt.step()
            if step+1 == CYCLE:
                boundary = dict(weights=state_hash(model.state_dict()), optimizer=state_hash(opt.state_dict()))
            if (step+1) % 200 == 0:
                print(f'[C332] arm={arm} step={step+1}/{STEPS} ce={losses[-1]:.6f}', flush=True)
    model.eval(); require(boundary is not None and continuation == boundary, 'continued optimizer')
    final_hash = state_hash(model.state_dict())
    state = {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    require(state_hash(state) == final_hash and all(v.numel() == 0 or state[k].data_ptr() != v.data_ptr()
            for k,v in model.state_dict().items()), 'deep checkpoint copy')
    return dict(arm=arm, readout_mode=mode, steps=STEPS, initial_sha256=initial, final_sha256=final_hash,
        core_initial_sha256=core_initial, core_final_sha256=state_hash(model.backbone.core.state_dict()),
        ce_history=losses, optimizer_group_lrs=rates, gradient_parameter_counts=counts, gradient_union=dict(sorted(union.items())),
        event_indices=visited, boundary=boundary, continuation=continuation,
        optimizer_creations=1, intermediate_evaluations=0, policy_receipt=dict(stats)), state


def train_one(seed, arm, model, tables, y, train_rows, cx, root, pins):
    x = cx[-1]
    source().base().check_dependencies(root, pins, cx, model)
    events, mask = schedule(seed, train_rows, x)
    input_sha = training_fingerprint(tables,y,events,mask)
    print(f'[C332] seed={seed} arm={arm} phase=training', flush=True)
    with x.c.p267.counted(model, x.c.core) as (calls, cores):
        trace, state = optimize(model, arm, tables, y, events, mask, x)
    require(calls == [2400,115200] and cores[0] == 9600
            and trace['policy_receipt'] == dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400), 'training work')
    require(training_fingerprint(tables,y,events,mask) == input_sha, 'TRAIN tensor mutation')
    trace.update(seed=seed, training_input_sha256=input_sha, schedule_sha256=digest(events.tolist()), mask_sha256=digest(mask.tolist()),
                 family_exposure_per_cycle=source().curriculum().exposure(events,mask))
    return trace, state


def check_trace(t, train_rows, x):
    events, mask = schedule(t['seed'], train_rows, x)
    require(t['readout_mode'] == policy_mode(t['arm']) and type(t['steps']) is int and t['steps'] == STEPS,
            'saved training policy')
    require(t['schedule_sha256'] == digest(events.tolist()) and t['mask_sha256'] == digest(mask.tolist())
            and t['family_exposure_per_cycle'] == source().curriculum().exposure(events,mask), 'saved exposure')
    require(t['event_indices'] == list(range(CYCLE))*2 and all(type(v) is int for v in t['event_indices']), 'repeated event order')
    require(t['optimizer_group_lrs'] == [list(RATES)]*STEPS and len(t['ce_history']) == STEPS
            and all(type(v) in (int,float) and math.isfinite(v) and v >= 0 for v in t['ce_history']), 'saved rates/losses')
    u = t['gradient_union']; counts = t['gradient_parameter_counts']
    require(u and all(type(k) is str and type(v) is int and v > 0 for k,v in u.items())
            and 0 < sum(u.values()) <= 14256 and len(counts) == STEPS
            and all(type(v) is int and 0 < v <= sum(u.values()) for v in counts), 'saved gradient inventory')
    for k in ('initial_sha256','final_sha256','core_initial_sha256','core_final_sha256','training_input_sha256'):
        require(type(t[k]) is str and re.fullmatch('[0-9a-f]{64}',t[k]), 'saved state hash')
    require(t['initial_sha256'] != t['final_sha256'] and t['core_initial_sha256'] != t['core_final_sha256'], 'trained state')
    require(t['boundary'] == t['continuation'] and set(t['boundary']) == {'weights','optimizer'}
            and all(type(v) is str and re.fullmatch('[0-9a-f]{64}',v) for v in t['boundary'].values()), 'saved continuation')
    require(type(t['optimizer_creations']) is int and t['optimizer_creations'] == 1
            and type(t['intermediate_evaluations']) is int and t['intermediate_evaluations'] == 0
            and t['policy_receipt'] == dict(calls=2400,query_calls=4800,rows=115200,grad_calls=2400), 'saved training receipts')


def contrast_check(z):
    keys = ('answers','query_pairs','control_correct','candidate_correct','control_both_correct','candidate_both_correct',
            'rescued','regressed','pair_rescued','pair_regressed','answer_gain','query_pair_gain')
    require(set(z) == set(keys) and all(type(z[k]) is int for k in keys), 'contrast fields')
    require(z['answers'] == 288 and z['query_pairs'] == 144, 'contrast denominators')
    for k in keys[2:-2]:
        maximum = 144 if k in ('control_both_correct','candidate_both_correct','pair_rescued','pair_regressed') else 288
        require(0 <= z[k] <= maximum, 'contrast range')
    require(z['candidate_correct']-z['control_correct'] == z['answer_gain'] == z['rescued']-z['regressed']
            and z['candidate_both_correct']-z['control_both_correct'] == z['query_pair_gain'] == z['pair_rescued']-z['pair_regressed'], 'contrast conservation')


def fixed_gate(pairs):
    require([r['seed'] for r in pairs] == list(SEEDS), 'full paired cohort')
    flags = []
    for r in pairs:
        require(type(r['candidate_full_pass']) is bool, 'candidate gate type')
        require(all(type(r[k]) is int for k in ('six_answer_gain','six_pair_gain','short_answer_gain','short_pair_gain','interior_answer_gain','interior_pair_gain')), 'gain types')
        flags.append(r['candidate_full_pass'] and all(r[k] >= 0 for k in
            ('six_answer_gain','six_pair_gain','short_answer_gain','short_pair_gain','interior_answer_gain','interior_pair_gain')))
    strict = sum(r['six_answer_gain'] for r in pairs) > 0 and sum(r['six_pair_gain'] for r in pairs) > 0
    return all(flags) and strict, flags


def analyze(traces, records, states, data, cx):
    require([(t['seed'],t['arm']) for t in traces] == [(r['seed'],r['arm']) for r in records] == identities()
            and len(states) == 10, 'complete trained cohort')
    metrics, flags = [], []
    for t,r,state in zip(traces,records,states,strict=True):
        check_trace(t,data['TRAIN'],cx[-1])
        require(r['state_sha256'] == t['final_sha256'] == state_hash(state)
                and r['readout_mode'] == t['readout_mode'] and set(r['raw']) == {'evaluation','replay'}, 'saved trained state/policy')
        for mode in ('evaluation','replay'):
            source().base().validate_raw(r['raw'][mode],data,cx)
            require(r['receipts'][mode] == dict(calls=171,query_calls=342,rows=16416,grad_calls=0), 'evaluation work')
        require(source().base().replay_error(r['raw']['evaluation'],r['raw']['replay'],data,cx) <= 1e-9, 'same-policy checkpoint replay')
        score,f = readouts().summarize_mode(r['raw']['evaluation'],data,cx)
        metrics.append(dict(seed=t['seed'],arm=t['arm'],score=score)); flags.append(dict(seed=t['seed'],arm=t['arm'],**f))
    pairs = []
    for i,seed in enumerate(SEEDS):
        a,c = traces[2*i:2*i+2]
        require(a['initial_sha256'] == c['initial_sha256'] and a['core_initial_sha256'] == c['core_initial_sha256']
                and all(a[k] == c[k] for k in ('training_input_sha256','schedule_sha256','mask_sha256','family_exposure_per_cycle','event_indices','optimizer_group_lrs')), 'paired training conditions')
        comparisons = readouts().compare(records[2*i]['raw']['evaluation'],records[2*i+1]['raw']['evaluation'],data,source().base())
        old,inside = comparisons['original_by_length'],comparisons['interior']
        pairs.append(dict(seed=seed,control_full_pass=flags[2*i]['retention_pass'] and flags[2*i]['interior_pass'],
            candidate_full_pass=flags[2*i+1]['retention_pass'] and flags[2*i+1]['interior_pass'],
            six_answer_gain=old['6']['answer_gain'],six_pair_gain=old['6']['query_pair_gain'],
            short_answer_gain=sum(old[str(n)]['answer_gain'] for n in range(2,6)),
            short_pair_gain=sum(old[str(n)]['query_pair_gain'] for n in range(2,6)),
            interior_answer_gain=inside['answer_gain'],interior_pair_gain=inside['query_pair_gain'],**comparisons))
    gate, eligibility = fixed_gate(pairs)
    result = dict(candidate_gate=gate,eligible_seed_count=sum(eligibility),paired_conditions_valid=True,
                  all_replays=True,seed_results=flags,paired_comparisons=pairs,**WORK)
    check_summary(result)
    return metrics,result


def check_summary(v):
    require(all(type(v[k]) is int and v[k] == n for k,n in WORK.items())
            and v['paired_conditions_valid'] is True and v['all_replays'] is True, 'work/integrity')
    require([(r['seed'],r['arm']) for r in v['seed_results']] == identities(), 'summary cohort')
    for i,pair in enumerate(v['paired_comparisons']):
        for offset,key in ((0,'control_full_pass'),(1,'candidate_full_pass')):
            f = v['seed_results'][2*i+offset]
            require(set(f['original_pass']) == set(map(str,range(2,7))) and all(type(z) is bool for z in f['original_pass'].values())
                    and type(f['interior_pass']) is bool and f['retention_pass'] is all(f['original_pass'].values())
                    and pair[key] is (f['retention_pass'] and f['interior_pass']), 'summary gates')
        old,inside = pair['original_by_length'],pair['interior']
        require(set(old) == set(map(str,range(2,7))), 'all original domains')
        for z in [inside,*old.values()]: contrast_check(z)
        require(pair['six_answer_gain'] == old['6']['answer_gain'] and pair['six_pair_gain'] == old['6']['query_pair_gain']
                and pair['short_answer_gain'] == sum(old[str(n)]['answer_gain'] for n in range(2,6))
                and pair['short_pair_gain'] == sum(old[str(n)]['query_pair_gain'] for n in range(2,6))
                and pair['interior_answer_gain'] == inside['answer_gain'] and pair['interior_pair_gain'] == inside['query_pair_gain'], 'gate count binding')
    gate,flags = fixed_gate(v['paired_comparisons'])
    require(v['candidate_gate'] is gate and type(v['eligible_seed_count']) is int and v['eligible_seed_count'] == sum(flags), 'fixed primary gate')


def load_states(path):
    v = torch.load(path,map_location='cpu',weights_only=True)
    require(set(v) == {'schema','identities','states'} and v['schema'] == 'fold-c332-trained-models-v1'
            and v['identities'] == [list(z) for z in identities()] and len(v['states']) == 10, 'model bundle')
    return v['states']


def load_data(source_out,read):
    return tuple(read(source_out/name) for name in ('dataset.json','original-prompts.json','interior-prompts.json'))


def run_training(out,source_out,cx,root,pins,read):
    data,old,new = load_data(source_out,read); data_hash = digest((data,old,new))
    tables,y = prepared(data,old,new,cx); traces,states = [],[]
    for seed in SEEDS:
        models = make_pair(seed,cx[-1])
        for arm in ARMS:
            trace,state = train_one(seed,arm,models[arm],tables,y,data['TRAIN'],cx,root,pins)
            traces.append(trace);states.append(state)
        del models
    for i in range(5):
        require(traces[2*i]['initial_sha256'] == traces[2*i+1]['initial_sha256'], 'paired initialization')
    torch.save(dict(schema='fold-c332-trained-models-v1',identities=[list(z) for z in identities()],states=states),out/'trained-models.pt')
    saved = load_states(out/'trained-models.pt')
    require([state_hash(v) for v in states] == [state_hash(v) for v in saved], 'bundle roundtrip')
    records = []
    for (seed,arm),state in zip(identities(),saved,strict=True):
        model = make_model(seed,cx[-1]);source().base().check_dependencies(root,pins,cx,model)
        model.eval();model.requires_grad_(False);raw,receipts = {},{}
        for kind in ('evaluation','replay'):
            model.load_state_dict(state,strict=True);require(state_hash(model.state_dict()) == state_hash(state), 'loaded checkpoint')
            raw[kind],receipts[kind] = readouts().measure(model,policy_mode(arm),data,old,new,cx)
            require(state_hash(model.state_dict()) == state_hash(state), 'evaluation mutated checkpoint')
        records.append(dict(seed=seed,arm=arm,state_sha256=state_hash(state),readout_mode=policy_mode(arm),raw=raw,receipts=receipts))
        print(f'[C332] seed={seed} arm={arm} saved_evaluation_and_replay=COMPLETE',flush=True)
    metrics,result = analyze(traces,records,saved,data,cx)
    require(digest((data,old,new)) == data_hash,'data/prompt mutation')
    torch.save(dict(schema='fold-c332-evaluations-v1',records=records),out/'evaluations.pt')
    for name,value in (('experiment-plan.json',manifest()),('training-traces.json',traces),('measurements.json',metrics),('validation-summary.json',result)):
        with (out/name).open('xb') as stream: stream.write(blob(value))
    return result


def semantic_recheck(out,source_out,cx,read):
    data,_,_ = load_data(source_out,read)
    v = torch.load(out/'evaluations.pt',map_location='cpu',weights_only=True)
    require(set(v) == {'schema','records'} and v['schema'] == 'fold-c332-evaluations-v1','evaluation schema')
    metrics,result = analyze(read(out/'training-traces.json'),v['records'],load_states(out/'trained-models.pt'),data,cx)
    for name,value in (('experiment-plan.json',manifest()),('measurements.json',metrics),('validation-summary.json',result)):
        require(blob(read(out/name)) == blob(value),'saved reconstruction:'+name)
    return result


def native_preflight(source_out,cx,root,pins,read):
    data,old,new = load_data(source_out,read);tables,y = prepared(data,old,new,cx)
    for seed in SEEDS: schedule(seed,data['TRAIN'],cx[-1])
    model = make_model(SEEDS[0],cx[-1]);source().base().check_dependencies(root,pins,cx,model)
    with torch.no_grad():
        w = model.read.output.weight;w.copy_(torch.sin(torch.arange(w.numel(),dtype=torch.float64).reshape_as(w))*.03)
    initial = state_hash(model.state_dict())
    ids = [next(i for i,r in enumerate(data['TRAIN']) if r['language'] == lang) for lang in ('en','ja')]
    for family in ('original','interior4'):
        tokens = tables[family][4,'repeat'][ids];tasks = torch.zeros(2,dtype=torch.int64)
        model.train()
        with torch.no_grad(): expected = model(tokens,tasks)
        for arm in ARMS:
            model.zero_grad(set_to_none=True)
            with torch.enable_grad(),readouts().readout(model,cx[-1].wide,policy_mode(arm)) as stats:
                logits = model(tokens,tasks)
                if arm == 'native':readouts().same(expected,logits.detach())
                F.cross_entropy(logits,y[ids]).backward()
            require(stats == dict(calls=1,query_calls=2,rows=2,grad_calls=1)
                    and model.read.query.weight.grad is not None and bool(torch.isfinite(model.read.query.weight.grad).all())
                    and all(p.grad is None or bool(torch.isfinite(p.grad).all()) for p in model.parameters()),'native backward')
    require(state_hash(model.state_dict()) == initial,'preflight weight mutation')
    print('C332_native_preflight=PASS;schedules=5;forwards=6;rows=12;backward=4;optimizer_steps=0',flush=True)
