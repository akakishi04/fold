"""C329: paired 1200/2400 checkpoints from five uninterrupted constant-rate runs."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import math
import re
import torch
from torch.nn import functional as F

EXPERIMENT_ID = 'C329-v5b-fixed-budget-extension'
STAGE = 'V5-B-FIXED-BUDGET-EXTENSION'
SEEDS = tuple(range(329001, 329006))
ORDERS = tuple(range(329101, 329106))
ARMS = ('prefix1200', 'extended2400')
PROFILES = ('repeat', 'shared_prefix', 'shared_suffix')
PREFIX, TOTAL, FIT_RNG = 1200, 2400, 612000
RATES = (.005, .0005)
OWN = ('fold_lm/v05_benchmarks/model_c329_fixed_budget_extension.py',
       'tools/c329_execution.py', 'tests_lm/test_v05_c329_fixed_budget_extension.py',
       'tools/run_c329.ps1', 'tools/invoke_c329.ps1',
       'docs/experiment-ledger-addendum-c329-preregistration.md')
OUTPUTS = ('experiment-plan.json', 'dataset.json', 'original-prompts.json',
           'interior-prompts.json', 'trained-models.pt', 'evaluations.pt',
           'measurements.json', 'validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 48, 5770, 218
SOURCE_COUNT, INPUT_COUNT = 832, 1577
WORK = dict(models=5, checkpoint_states=10, evaluation_models=10,
            train_steps=12000, training_rows=576000, model_forward_calls=15420,
            row_presentations=904320, core_forward_calls=61680, model_state_loads=20,
            checkpoint_bundle_loads=1, new_checkpoint_writes=1, network_calls=0)
MANIFEST_SHA = '9968ab6d8d2abdd3751b6ac1d1b1116a088d1c8abbdebdae50b580005d6fb7d8'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c328_late_rate_decay')


def curriculum():
    return parent().previous()


def base():
    return parent().base()


def identities():
    return list(itertools.product(SEEDS, ARMS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE,
        acceptance_base='cc8881705867b748699dc9ce25a27a0a72d76d16',
        parent_execution='3507021e46d47f6543316d46dc4481d3ead04855',
        parent_summary_sha256='10bf430e74311a883cbcc7a7b70b589490a98d0f6db4458bcfe8be748fbccb53',
        parent_envelope_sha256='d675bf546fb9d46eecf86b9a53847c5c054f4de618f311e0426a195c49f7cc32',
        question='does one fixed extra1200-update cycle improve interior binding and retain original2..6 on the same constant-rate trajectory',
        seeds=list(SEEDS), orders=list(ORDERS), arms=list(ARMS), prefix=PREFIX, total=TOTAL,
        changed='training budget1200 versus2400; the exact first1200 schedule and batch4 masks repeat once',
        held='fresh initialization,first1200 trajectory,templates,logical split,optimizer identity/moments/rates,architecture,precision,local gates',
        snapshots='five fresh fits; deep-cloned prefix1200 and extended2400 states; evaluate only after ALL fitting; no checkpoint selection',
        continuation='same optimizer; no reseed/reset/recreation/decay; before update1201 state hashes match post1200 snapshot',
        exposure_per_row=dict(prefix1200=[100,100,50,50], extended2400=[200,200,100,100]),
        exposure_order=['original2','original3','original4','interior4'],
        batch4='unchanged C326 allocator on base1200;11..13 original pairs per length4 update;repeat identities not new shuffle',
        parameters=14256, core_parameters=3328, slots=64, rows_per_update=48, fit_rng=FIT_RNG,
        optimizer='unchanged native C308 core_slow AdamW; noncore.005/core.0005;betas.9/.999;eps1e-8;decay0;globalclip1;meanCE',
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        primary='ALL5 extended2400 pass complete interior and original2..6 gates;strict interior HOLDOUT answer AND pair gains;nonnegative pooled original2..6 gains in both counts versus prefix1200',
        boundary='unequal budget by design;paired checkpoints not independent fits;seen templates/reused split;not an optimal budget or capacity/underfitting proof',
        original_single='length1 descriptive only', dtype='CPU float64', threads=2,
        deterministic=True, replay_tolerance=1e-9, readout='native mean_last',
        source_pins=SOURCE_COUNT, protected_inputs=INPUT_COUNT, inherited_sources=826,
        inherited_inputs=1561, immediate_parent_files=10, own_tests=OWN_TESTS,
        focused_tests=FULL_TESTS, modules=MODULES,
        exclusion='sole inherited exact C204 mutable-ACTIVE test;no new exclusions/skips',
        outputs=list(OUTPUTS), raw_logit_payload_bytes=336199680,
        work_scope='five2400-step trajectories plus10state evaluations and10replays;preflight/tests/verification separate',
        native_preflight='all5 actual schedules plus one discarded6forward/2backward/12row/0update native probe',
        parent_semantics='accepted C328 valid negative; unchanged saved semantic reconstruction with complete inherited protection;no ancestor semantic reruns',
        gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C329 manifest seal')


def state_hash(value):
    """Typed fingerprint of finite tensor/state data; no model forward or pickle."""
    h = hashlib.sha256()
    def put(tag, data):
        h.update(tag); h.update(str(len(data)).encode() + b':'); h.update(data)
    def visit(v):
        if isinstance(v, torch.Tensor):
            z = v.detach().cpu().contiguous()
            require(bool(torch.isfinite(z).all()), 'nonfinite state')
            put(b'T', blob([str(z.dtype), list(z.shape)])); put(b'B', z.numpy().tobytes())
        elif isinstance(v, dict):
            require(all(type(k) in (str, int) for k in v), 'state key')
            put(b'D', str(len(v)).encode())
            for k in sorted(v, key=lambda k: (type(k).__name__, str(k))):
                visit(k); visit(v[k])
        elif isinstance(v, (tuple, list)):
            put(b'Q' if isinstance(v, tuple) else b'L', str(len(v)).encode())
            for x in v:
                visit(x)
        else:
            require(v is None or type(v) in (str, int, float, bool), 'state value')
            put(b'J', blob(v))
    visit(value)
    return h.hexdigest()


def schedule(seed, rows, x):
    require(type(seed) is int and seed in SEEDS and len(rows) == 192, 'fresh schedule identity')
    events = x.parent.plan_for_order(ORDERS[SEEDS.index(seed)], 'two_to_four', rows, x.p312, x.pairs)
    curriculum().validate_schedule(events)
    return events


def make_model(seed, x):
    require(type(seed) is int and seed in SEEDS, 'fresh model identity')
    c = x.c
    ref = c.c278.MeanFinalDualReadout(c.factory.new_model(seed), seed, c.reader, c.c269.query_span_mask)
    model = x.policy.configure(x.wide.LengthReadout(ref), 'core_slow')
    require(type(model) is x.wide.LengthReadout and model.backbone.config.max_tokens == 64
            and model.backbone.core.config.slots == 64, 'native architecture')
    require(sum(p.numel() for p in model.parameters()) == 14256
            and sum(p.numel() for p in model.backbone.core.parameters()) == 3328, 'capacity')
    require(c.base.fingerprint(model) == c.base.fingerprint(ref)
            and list(model.state_dict()) == list(ref.state_dict()), 'initial native state')
    require(all(p.requires_grad and p.dtype == torch.float64 and p.device.type == 'cpu'
                for p in model.parameters()), 'precision/gradient policy')
    x.policy.parameter_groups(model, 'core_slow')
    return model


def checkpoint(model, opt, step):
    before = dict(weights=state_hash(model.state_dict()), optimizer=state_hash(opt.state_dict()))
    state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    require(state_hash(state) == before['weights'], 'snapshot copy mismatch')
    require(before == dict(weights=state_hash(model.state_dict()), optimizer=state_hash(opt.state_dict())),
            'snapshot mutated live state')
    require(all(v.numel() == 0 or state[k].data_ptr() != v.data_ptr() for k, v in model.state_dict().items()), 'snapshot alias')
    return state, dict(step=step, core=state_hash(model.backbone.core.state_dict()), **before)


def optimize(model, tables, targets, events, mask, x):
    """Two identical event cycles, one optimizer, no intermediate evaluation or reseed."""
    require(len(events) == len(mask) == PREFIX and TOTAL == 2 * PREFIX, 'registered cycles')
    p = curriculum(); torch.manual_seed(FIT_RNG)
    opt = x.policy.optimizer_for(model, 'core_slow'); opt_id = id(opt)
    initial = state_hash(model.state_dict()); core_initial = state_hash(model.backbone.core.state_dict())
    losses, rates, counts, visited, states, receipts = [], [], [], [], [], []
    union = {}; continuation = None; model.train()
    for step in range(TOTAL):
        if step == PREFIX:
            continuation = dict(weights=state_hash(model.state_dict()), optimizer=state_hash(opt.state_dict()))
            require(all(continuation[k] == receipts[0][k] for k in ('weights', 'optimizer')), 'continuation reset')
        require(id(opt) == opt_id, 'optimizer replacement')
        x.policy.verify_optimizer(opt, model, 'core_slow')
        rate = [g['lr'] for g in opt.param_groups]
        require(rate == list(RATES), 'nonconstant learning rates'); rates.append(rate)
        index = step % PREFIX; visited.append(index)
        opt.zero_grad(set_to_none=True)
        tokens, ids = p.select_tokens(tables, events[index], mask[index])
        z = model(tokens, torch.zeros(len(ids), dtype=torch.int64)); x.c.p267.check_logits(z, len(ids))
        loss = F.cross_entropy(z, targets[ids]); require(bool(torch.isfinite(loss)), 'nonfinite loss')
        losses.append(float(loss.detach())); loss.backward()
        got = {n: q.numel() for n, q in model.named_parameters() if q.grad is not None}
        counts.append(sum(got.values())); union.update(got)
        torch.nn.utils.clip_grad_norm_(list(model.parameters()), 1., error_if_nonfinite=True)
        opt.step()
        if step + 1 in (PREFIX, TOTAL):
            state, receipt = checkpoint(model, opt, step + 1); states.append(state); receipts.append(receipt)
        if (step + 1) % 200 == 0:
            print(f'[C329] step={step+1}/{TOTAL} ce={losses[-1]:.6f} lr={rate}', flush=True)
    model.eval()
    require(continuation is not None and state_hash(states[0]) == receipts[0]['weights'], 'prefix overwritten')
    return dict(initial_sha256=initial, core_initial_sha256=core_initial, ce_history=losses,
        optimizer_group_lrs=rates, gradient_parameter_counts=counts, gradient_union=dict(sorted(union.items())),
        event_indices=visited, checkpoints=receipts, continuation=continuation,
        optimizer_creations=1, intermediate_evaluations=0), states


def train_one(seed, tables, targets, data, cx, root, pins):
    b = base(); trainer, x = cx[-2:]; p = curriculum()
    model = make_model(seed, x); b.check_dependencies(root, pins, cx, model)
    events = schedule(seed, data['TRAIN'], x); mask = p.family_mask(events, 'batch4')
    keys = set(itertools.product((2, 3, 4), PROFILES))
    require(set(tables) == {'original', 'interior4'} and targets.shape == (192,)
            and targets.dtype == torch.int64, 'TRAIN inputs')
    require(all(set(t) == keys and all(z.shape == (192, 64) and z.dtype == torch.int64
            and z.device.type == 'cpu' for z in t.values()) for t in tables.values()), 'TRAIN tables')
    hooks = trainer.hook_snapshot(model)
    print(f'[C329] seed={seed} phase=uninterrupted_training', flush=True)
    with x.c.p267.counted(model, x.c.core) as (calls, cores), trainer.trained_readout(model, x.wide, 'mean_last') as stats:
        trace, states = optimize(model, tables, targets, events, mask, x)
    require(calls == [2400, 115200] and cores[0] == 9600
            and stats == dict(calls=2400, query_calls=4800, rows=115200, grad_calls=2400), 'training work')
    require(trainer.hook_snapshot(model) == hooks, 'training hook restoration')
    trace.update(seed=seed, steps=TOTAL, training_rows=115200, schedule_events=events.clone(),
        template_pair_events=mask.clone(), family_exposure_per_cycle=p.exposure(events, mask),
        schedule_sha256=digest(events.tolist()), mask_sha256=digest(mask.tolist()), policy_receipt=dict(stats))
    print(f'[C329] seed={seed} prefix_snapshot_preserved=PASS continuation_optimizer=UNCHANGED', flush=True)
    return trace, states


def check_trace(t, seed, rows, x):
    p = curriculum(); events = schedule(seed, rows, x); mask = p.family_mask(events, 'batch4')
    for k, v in dict(seed=seed, steps=TOTAL, training_rows=115200, optimizer_creations=1, intermediate_evaluations=0).items():
        require(type(t[k]) is int and t[k] == v, 'trajectory metadata:' + k)
    require(torch.equal(t['schedule_events'], events) and torch.equal(t['template_pair_events'], mask), 'saved curriculum')
    require(t['schedule_sha256'] == digest(events.tolist()) and t['mask_sha256'] == digest(mask.tolist())
            and t['family_exposure_per_cycle'] == p.exposure(events, mask), 'saved exposure')
    require(t['event_indices'] == list(range(PREFIX)) * 2 and all(type(v) is int for v in t['event_indices']), 'two exact cycles')
    require(t['optimizer_group_lrs'] == [list(RATES)] * TOTAL and len(t['ce_history']) == TOTAL
            and all(type(v) in (int, float) and math.isfinite(v) and v >= 0 for v in t['ce_history']), 'rate/loss trace')
    u, counts = t['gradient_union'], t['gradient_parameter_counts']
    require(u and all(type(k) is str and type(v) is int and v > 0 for k, v in u.items())
            and 0 < sum(u.values()) <= 14256, 'gradient union')
    require(len(counts) == TOTAL and all(type(v) is int and 0 < v <= sum(u.values()) for v in counts), 'gradient trace')
    require(all(isinstance(t[k], str) and re.fullmatch('[0-9a-f]{64}', t[k])
                for k in ('initial_sha256', 'core_initial_sha256')), 'initial state hashes')
    require(t['policy_receipt'] == dict(calls=2400, query_calls=4800, rows=115200, grad_calls=2400), 'training receipt')
    require(len(t['checkpoints']) == 2 and [r['step'] for r in t['checkpoints']] == [PREFIX, TOTAL], 'checkpoint steps')
    for r in t['checkpoints']:
        require(set(r) == {'step', 'core', 'weights', 'optimizer'} and type(r['step']) is int
                and all(re.fullmatch('[0-9a-f]{64}', r[k]) for k in ('core', 'weights', 'optimizer')), 'checkpoint receipt')
        require(r['weights'] != t['initial_sha256'] and r['core'] != t['core_initial_sha256'], 'learned checkpoint')
    require(t['continuation'] == {k: t['checkpoints'][0][k] for k in ('weights', 'optimizer')}, 'continuation binding')


def measure(model, state, data, old, new, cx):
    b = base(); trainer, x = cx[-2:]
    require(list(state) == list(model.state_dict()) and all(state[k].shape == v.shape and state[k].dtype == v.dtype
            for k, v in model.state_dict().items()), 'checkpoint schema')
    model.load_state_dict(state, strict=True); model.eval(); model.requires_grad_(False)
    before = state_hash(model.state_dict()); hooks = trainer.hook_snapshot(model)
    require(before == state_hash(state), 'loaded checkpoint bytes')
    with x.c.p267.counted(model, x.c.core) as (calls, cores), trainer.trained_readout(model, x.wide, 'mean_last') as stats:
        raw = b.evaluate(model, data, old, new, cx)
    require(calls == [171, 16416] and cores[0] == 684
            and stats == dict(calls=171, query_calls=342, rows=16416, grad_calls=0), 'evaluation work')
    require(state_hash(model.state_dict()) == before and trainer.hook_snapshot(model) == hooks, 'evaluation preservation')
    return raw, dict(stats)


def fixed_gate(rows):
    require([r['seed'] for r in rows] == list(SEEDS), 'complete paired seeds')
    flags = []
    for r in rows:
        require(type(r['candidate_interior_pass']) is bool and type(r['candidate_retention_pass']) is bool, 'gate flags')
        require(all(type(r[k]) is int for k in ('original_answer_gain', 'original_pair_gain', 'interior_answer_gain', 'interior_pair_gain')), 'gate counts')
        flags.append(r['candidate_interior_pass'] and r['candidate_retention_pass']
            and r['interior_answer_gain'] > 0 and r['interior_pair_gain'] > 0
            and r['original_answer_gain'] >= 0 and r['original_pair_gain'] >= 0)
    return all(flags), flags


def analyze(archive, states, data, cx):
    b = base(); x = cx[-1]; traces, records = archive['trajectories'], archive['records']
    require([t['seed'] for t in traces] == list(SEEDS) and [(r['seed'], r['arm']) for r in records] == identities()
            and len(states) == 10, 'complete checkpoint cohort')
    for t in traces:
        check_trace(t, t['seed'], data['TRAIN'], x)
    metrics, results = [], []
    for i, r in enumerate(records):
        checkpoint_receipt = traces[i // 2]['checkpoints'][i % 2]
        require(r['step'] == checkpoint_receipt['step'] and type(r['step']) is int
                and r['state_sha256'] == checkpoint_receipt['weights'] == state_hash(states[i]), 'checkpoint binding')
        require(r['checkpoint_roundtrip'] is True and type(r['reload_max_error']) in (int, float)
                and math.isfinite(r['reload_max_error']) and 0 <= r['reload_max_error'] <= 1e-9, 'checkpoint replay')
        require(r['policy_receipt'] == r['replay_policy_receipt'] == dict(calls=171, query_calls=342, rows=16416, grad_calls=0), 'evaluation receipts')
        b.validate_raw(r['raw'], data, cx)
        original = {str(n): x.wide.score_length(data, r['raw']['original'][str(n)], x.c) for n in range(2, 7)}
        inside = cx[2].score_new(r['raw']['interior'], data, x)
        require(all(type(v['passed']) is bool for v in (*original.values(), inside)), 'scorer flags')
        results.append(dict(seed=r['seed'], arm=r['arm'], original_pass={n: v['passed'] for n, v in original.items()},
            retention_pass=all(v['passed'] for v in original.values()), interior_pass=inside['passed']))
        single = {split: {v: int((z.argmax(1) == torch.tensor([d['target'] for d in data[split]])).sum())
                  for v, z in r['raw']['original']['1'][split]['repeat'].items()} for split in ('TRAIN', 'HOLDOUT')}
        metrics.append(dict(seed=r['seed'], arm=r['arm'], original=original, interior=inside, single_character=single))
    pairs = []
    for i, seed in enumerate(SEEDS):
        a, c = records[2*i:2*i+2]
        inside = b.heldout_contrast(a['raw']['interior']['HOLDOUT'], c['raw']['interior']['HOLDOUT'], data['HOLDOUT'])
        old = {}
        for n in range(2, 7):
            adapted = [{ip: r['raw']['original'][str(n)]['HOLDOUT'][op]
                       for op, ip in zip(PROFILES, b.templates.INTERIOR_PROFILES, strict=True)} for r in (a, c)]
            old[str(n)] = b.heldout_contrast(*adapted, data['HOLDOUT'])
        pairs.append(dict(seed=seed, candidate_interior_pass=results[2*i+1]['interior_pass'],
            candidate_retention_pass=results[2*i+1]['retention_pass'], control_interior_pass=results[2*i]['interior_pass'],
            control_retention_pass=results[2*i]['retention_pass'], original_answer_gain=sum(v['answer_gain'] for v in old.values()),
            original_pair_gain=sum(v['query_pair_gain'] for v in old.values()), interior_answer_gain=inside['answer_gain'],
            interior_pair_gain=inside['query_pair_gain'], interior=inside, original_by_length=old, shared_prefix_preserved=True))
    gate, flags = fixed_gate(pairs)
    for row, flag in zip(pairs, flags, strict=True):
        row['paired_success'] = flag
    return metrics, dict(candidate_gate=gate, paired_success_count=sum(flags), seed_results=results,
        paired_comparisons=pairs, all_shared_prefixes=True, all_replays=True, **WORK)


def load_bundle(path):
    v = torch.load(path, map_location='cpu', weights_only=True)
    require(set(v) == {'schema', 'identities', 'readout_policy', 'states'} and v['schema'] == 'fold-c329-models-v1'
            and v['identities'] == [list(x) for x in identities()] and v['readout_policy'] == 'mean_last'
            and len(v['states']) == 10, 'model bundle')
    return v['states']


def run_science(out, data, old, new, cx, root, pins):
    b = base(); prepared = curriculum().previous().training(data, old, new, cx)
    tables = {k: v[0] for k, v in prepared.items()}; y = prepared['original'][1]
    traces, states, records = [], [], []
    for seed in SEEDS:
        trace, snapshots = train_one(seed, tables, y, data, cx, root, pins)
        traces.append(trace); states.extend(snapshots)
    torch.save(dict(schema='fold-c329-models-v1', identities=[list(v) for v in identities()],
        readout_policy='mean_last', states=states), out / 'trained-models.pt')
    saved = load_bundle(out / 'trained-models.pt')
    require([state_hash(z) for z in saved] == [state_hash(z) for z in states], 'bundle roundtrip')
    for i, (seed, arm) in enumerate(identities()):
        model = make_model(seed, cx[-1]); b.check_dependencies(root, pins, cx, model)
        raw, receipt = measure(model, saved[i], data, old, new, cx)
        again, replay_receipt = measure(model, saved[i], data, old, new, cx)
        error = b.replay_error(raw, again, data, cx)
        records.append(dict(seed=seed, arm=arm, step=(PREFIX, TOTAL)[i % 2], state_sha256=state_hash(saved[i]),
            raw=raw, checkpoint_roundtrip=True, reload_max_error=error, policy_receipt=receipt,
            replay_policy_receipt=replay_receipt))
        print(f'[C329] seed={seed} arm={arm} checkpoint_replay=PASS', flush=True)
    archive = dict(schema='fold-c329-evaluations-v1', trajectories=traces, records=records)
    metrics, summary = analyze(archive, saved, data, cx); torch.save(archive, out / 'evaluations.pt')
    values = (manifest(), data, old, new, metrics, summary)
    for name, value in zip((OUTPUTS[0], OUTPUTS[1], OUTPUTS[2], OUTPUTS[3], OUTPUTS[6], OUTPUTS[7]), values, strict=True):
        with (out / name).open('xb') as stream:
            stream.write(blob(value))
    return summary


def semantic_recheck(out, data, old, new, cx, read_json):
    archive = torch.load(out / 'evaluations.pt', map_location='cpu', weights_only=True)
    require(set(archive) == {'schema', 'trajectories', 'records'} and archive['schema'] == 'fold-c329-evaluations-v1', 'evaluation schema')
    metrics, summary = analyze(archive, load_bundle(out / 'trained-models.pt'), data, cx)
    for name, value in zip((OUTPUTS[0], OUTPUTS[1], OUTPUTS[2], OUTPUTS[3], OUTPUTS[6], OUTPUTS[7]),
                          (manifest(), data, old, new, metrics, summary), strict=True):
        require(blob(read_json(out / name)) == blob(value), 'saved semantic reconstruction:' + name)
    return metrics, summary


def runtime_preflight(data, old, new, cx, root, pins):
    p = curriculum(); prepared = p.previous().training(data, old, new, cx)
    for seed in SEEDS:
        events = schedule(seed, data['TRAIN'], cx[-1]); p.family_mask(events, 'batch4')
        print(f'[C329 allocation] seed={seed} repeated_batch4=PASS', flush=True)
    trainer, x = cx[-2:]; model = make_model(SEEDS[0], x); base().check_dependencies(root, pins, cx, model)
    with torch.no_grad():
        w = model.read.output.weight; w.copy_(torch.sin(torch.arange(w.numel(), dtype=torch.float64).reshape_as(w)) * .03)
    ids = [next(i for i, r in enumerate(data['TRAIN']) if r['language'] == language) for language in ('en', 'ja')]
    for family in ('original', 'interior4'):
        tokens = prepared[family][0][4, 'repeat'][ids]; model.eval()
        with torch.no_grad():
            expected = model(tokens, torch.zeros(2, dtype=torch.int64))
            with trainer.trained_readout(model, x.wide, 'mean_last'):
                actual = model(tokens, torch.zeros(2, dtype=torch.int64))
        require(torch.equal(expected, actual), 'native readout parity'); model.train(); model.zero_grad(set_to_none=True)
        with trainer.trained_readout(model, x.wide, 'mean_last'):
            F.cross_entropy(model(tokens, torch.zeros(2, dtype=torch.int64)), prepared[family][1][ids]).backward()
        require(model.read.query.weight.grad is not None and all(z.grad is None or bool(torch.isfinite(z.grad).all())
                for z in model.parameters()), 'native TRAIN backward')
    print('C329_native_preflight=PASS; forwards=6; backward=2; optimizer_steps=0; scientific_training_started=False', flush=True)
