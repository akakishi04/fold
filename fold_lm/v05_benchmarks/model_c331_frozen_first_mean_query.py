"""C331: one frozen first/mean-query blend, retaining the native last query."""
from __future__ import annotations
from contextlib import contextmanager
import hashlib
import importlib
import itertools
import json
import math
import torch

EXPERIMENT_ID = 'C331-v5b-frozen-first-mean-query'
STAGE = 'V5-B-FROZEN-FIRST-MEAN-QUERY'
SEEDS = tuple(range(329001, 329006))
ARMS = ('prefix1200', 'extended2400')
MODES = ('native_before', 'first_mean', 'native_after')
OWN = ('fold_lm/v05_benchmarks/model_c331_frozen_first_mean_query.py',
       'tools/c331_execution.py', 'tests_lm/test_v05_c331_frozen_first_mean_query.py',
       'tools/run_c331.ps1', 'tools/invoke_c331.ps1',
       'docs/experiment-ledger-addendum-c331-preregistration.md')
OUTPUTS = ('diagnostic-plan.json', 'evaluations.pt', 'measurements.json', 'validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 48, 5898, 221
SOURCE_COUNT, INPUT_COUNT = 847, 2051
WORK = dict(models=10, scored_states=20, train_steps=0, gradient_calls=0,
            model_forward_calls=5130, row_presentations=492480, core_forward_calls=20520,
            query_projection_calls=10260, model_state_loads=10, checkpoint_bundle_loads=1,
            new_checkpoint_writes=0, network_calls=0)
MANIFEST_SHA = '8644f03a61e1dbdbb44a31514a392fd18cdb7ce71c190ee1a1fd2a8c759c30f8'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def source():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c329_fixed_budget_extension')


def localizer():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c330_saved_gate_localization')


def identities():
    return list(itertools.product(SEEDS, ARMS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE,
        acceptance_base='b195a3962dd868ffa430500ca3bf6ae87dc44b1d',
        parent_execution='a92b0096949c4176f793dc2b57e910149222efb0',
        parent_summary='f7c1a6567f2ab9929528722bfc699b8228275e8cb185c31f1de87e5260278691',
        parent_envelope='ad30fc8f64775ebe93f9c2650bc74dc809583c877397a94889745b3e388381ad',
        question='at frozen C329 states, does adding first-byte local information to the mean query change long shared-suffix binding while preserving other tasks',
        identities=[list(x) for x in identities()], modes=list(MODES),
        changed='first native read.query input is .5*(span_mean+first_query_byte_local_state);second remains last_query_byte_local_state',
        held='saved weights,all checkpoints,inputs,targets,span parser,two attention calls,attention output averaging,core and residual path',
        granularity='UTF8 byte,not first complete Unicode character;no target-dependent endpoint or profile selection',
        controls='native before/after match accepted C329 raw outputs within1e-9;query-blind and English original1 unchanged within1e-9;exact argmax for all controls',
        gate='diagnostic integrity only;all effects including harm retained;no selected coefficient or posthoc capability gate',
        thresholds=dict(accuracy=.90, query_pair=.80, evidence_drop=.35, query_drop=.35, both_order=.80),
        parameters=14256, core_parameters=3328, slots=64, dtype='cpu float64', threads=2,
        raw_logit_payload_bytes=1008599040, outputs=list(OUTPUTS),
        own_tests=OWN_TESTS, full_tests=FULL_TESTS, modules=MODULES,
        source_count=SOURCE_COUNT, input_count=INPUT_COUNT, parent_output_files=449,
        parent_output_breakdown='4 diagnostic outputs+summary+envelope+3 regression records+220 module receipt/log pairs',
        preflight='discarded native model;12 forwards/12 rows/0updates;nonzero reader probe;separate from cohort',
        nonclaims='untrained inference intervention,not trained capacity or proof of pooling causality;C317 replaced last by first whereas this keeps last',
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C331 manifest seal')


def hooks(model):
    names = ('_forward_pre_hooks', '_forward_hooks', '_forward_pre_hooks_with_kwargs',
             '_forward_hooks_with_kwargs', '_forward_hooks_always_called')
    return [(n, tuple(tuple(getattr(m, a)) for a in names)) for n, m in model.named_modules()]


def pooled(local, valid, span):
    require(local.ndim == 3 and local.shape == (*valid.shape, 16) and span.shape == valid.shape
            and valid.dtype == span.dtype == torch.bool and bool(span.any(1).all())
            and bool((~span | valid).all()), 'visible native query span')
    require(local.dtype == torch.float64 and local.device.type == 'cpu' and bool(torch.isfinite(local).all()), 'local precision')
    z = local*valid.unsqueeze(-1).to(local.dtype)
    pos = torch.arange(valid.shape[1]).expand_as(valid)
    first = torch.where(span, pos, valid.shape[1]).min(1).values
    last = torch.where(span, pos, -1).max(1).values
    batch = torch.arange(len(z))
    mean = (z*span.unsqueeze(-1)).sum(1)/span.sum(1, keepdim=True).to(z.dtype)
    return mean, z[batch, first], z[batch, last]


@contextmanager
def readout(model, wide, mode):
    require(mode in MODES, 'registered readout mode')
    old = hooks(model); handles = []; state = {}
    stats = dict(calls=0, query_calls=0, rows=0, grad_calls=0)
    def begin(module, args):
        require(not state and len(args) == 2, 'nonreentrant native forward')
        tokens = args[0]
        require(tokens.ndim == 2 and tokens.shape[1] == 64, '64-byte frame')
        state.update(valid=tokens != 256, span=wide.span_mask(tokens), q=0)
        stats['calls'] += 1; stats['rows'] += len(tokens); stats['grad_calls'] += int(torch.is_grad_enabled())
    def capture(module, args, out):
        require(state and 'mean' not in state and isinstance(out, (tuple, list)), 'one encoder output')
        mean, first, last = pooled(out[0], state['valid'], state['span'])
        state.update(mean=mean, first=first, last=last)
    def query(module, args):
        require('mean' in state and len(args) == 1 and state['q'] in (0, 1), 'two native queries')
        q = state['q']; expected = state['mean'] if q == 0 else state['last']
        require(torch.equal(args[0], expected), 'native query provenance')
        state['q'] += 1; stats['query_calls'] += 1
        if mode == 'first_mean' and q == 0:
            return (.5*(state['mean']+state['first']),)
        return None
    def finish(module, args, out):
        try:
            if out is not None:
                require(state.get('q') == 2, 'native query coverage')
        finally:
            state.clear()
    try:
        handles.append(model.register_forward_pre_hook(begin))
        handles.append(model.backbone.local_encoder.register_forward_hook(capture))
        handles.append(model.read.query.register_forward_pre_hook(query))
        handles.append(model.register_forward_hook(finish, always_call=True))
        yield stats
        require(stats['calls'] > 0 and stats['query_calls'] == 2*stats['calls'] and not state, 'readout coverage')
    finally:
        for handle in handles:
            handle.remove()
        state.clear(); require(hooks(model) == old, 'restored hooks')


def same(a, b):
    require(a.shape == b.shape and a.dtype == b.dtype and bool(torch.isfinite(a).all())
            and bool(torch.isfinite(b).all()), 'finite compatible logits')
    error = float((a-b).abs().max()) if a.numel() else 0.
    require(error <= 1e-9 and torch.equal(a.argmax(-1), b.argmax(-1)), 'control logits/argmax')
    return error


def invariant_views(a, b, data):
    count = 0
    def walk(x, y):
        nonlocal count
        require(type(x) is dict and type(y) is dict and set(x) == set(y), 'view tree')
        for k in x:
            if isinstance(x[k], dict):
                walk(x[k], y[k])
            elif k == 'query_blind':
                same(x[k], y[k]); count += 1
    walk(a, b)
    for split in ('TRAIN', 'HOLDOUT'):
        ids = [i for i, r in enumerate(data[split]) if r['language'] == 'en']
        require(ids, 'English single-byte controls')
        for view in ('normal', 'evidence_blind', 'query_blind'):
            same(a['original']['1'][split]['repeat'][view][ids], b['original']['1'][split]['repeat'][view][ids])
    require(count == 38, 'complete query-blind controls')


def summarize_mode(raw, data, cx):
    x = cx[-1]
    scores = {str(n): x.wide.score_length(data, raw['original'][str(n)], x.c) for n in range(2, 7)}
    inside = cx[2].score_new(raw['interior'], data, x)
    flags = dict(original_pass={k: v['passed'] for k, v in scores.items()}, interior_pass=inside['passed'],
                 retention_pass=all(v['passed'] for v in scores.values()))
    failures = {}
    for domain, score in [('original'+n, v) for n, v in scores.items()]+[('interior4', inside)]:
        cells, orders, _ = localizer().adapted_score(score, domain)
        failures[domain] = dict(local=sum(not r['passed'] for r in cells), order=sum(not r['passed'] for r in orders))
    return dict(original=scores, interior=inside), dict(**flags, failures=failures)


def compare(a, b, data, base):
    old = {}
    for n in range(2, 7):
        aligned = [{ip: r['original'][str(n)]['HOLDOUT'][op] for op, ip in
                    zip(('repeat', 'shared_prefix', 'shared_suffix'), base.templates.INTERIOR_PROFILES, strict=True)} for r in (a, b)]
        old[str(n)] = base.heldout_contrast(*aligned, data['HOLDOUT'])
    inside = base.heldout_contrast(a['interior']['HOLDOUT'], b['interior']['HOLDOUT'], data['HOLDOUT'])
    return dict(original_by_length=old, interior=inside)


def analyze(archive, prior, data, cx, parent_flags):
    require(set(archive) == {'schema', 'records'} and archive['schema'] == 'fold-c331-query-probe-v1', 'archive schema')
    rows = archive['records']; base = source().base()
    require([(r['seed'], r['arm']) for r in rows] == identities()
            and [(r['seed'], r['arm']) for r in prior] == identities()
            and [(r['seed'], r['arm']) for r in parent_flags] == identities(), 'all saved checkpoints')
    metrics, effects = [], []
    for r, old, flag in zip(rows, prior, parent_flags, strict=True):
        require(set(r) == {'seed', 'arm', 'state_sha256', 'raw', 'receipts'}
                and r['state_sha256'] == old['state_sha256'] and set(r['raw']) == set(MODES)
                and set(r['receipts']) == set(MODES), 'checkpoint record binding')
        for mode in MODES:
            base.validate_raw(r['raw'][mode], data, cx)
            require(r['receipts'][mode] == dict(calls=171, query_calls=342, rows=16416, grad_calls=0), 'forward receipt')
        before, candidate, after = [r['raw'][mode] for mode in MODES]
        require(base.replay_error(old['raw'], before, data, cx) <= 1e-9
                and base.replay_error(before, after, data, cx) <= 1e-9, 'native accepted replay')
        invariant_views(before, candidate, data)
        a, af = summarize_mode(before, data, cx); c, cf = summarize_mode(candidate, data, cx)
        require({k: af[k] for k in ('original_pass', 'interior_pass', 'retention_pass')} ==
                {k: flag[k] for k in ('original_pass', 'interior_pass', 'retention_pass')}, 'preserve parent gates')
        metrics.append(dict(seed=r['seed'], arm=r['arm'], native=a, first_mean=c))
        effects.append(dict(seed=r['seed'], arm=r['arm'], native=af, first_mean=cf, **compare(before, candidate, data, base)))
    summary = dict(diagnostic_complete=True, all_native_replays=True, all_invariant_views=True,
                   all_weights_preserved=True, effects=effects, **WORK)
    check_summary(summary)
    return metrics, summary


def check_summary(v):
    require(all(type(v[k]) is int and v[k] == n for k, n in WORK.items()), 'workload')
    require(all(v[k] is True for k in ('diagnostic_complete', 'all_native_replays', 'all_invariant_views', 'all_weights_preserved')), 'diagnostic integrity')
    require([(r['seed'], r['arm']) for r in v['effects']] == identities(), 'effect cohort')
    for row in v['effects']:
        require(set(row['original_by_length']) == set(map(str, range(2, 7))), 'contrast lengths')
        for mode in ('native', 'first_mean'):
            f = row[mode]
            require(set(f['original_pass']) == set(map(str, range(2, 7)))
                    and all(type(x) is bool for x in f['original_pass'].values())
                    and type(f['interior_pass']) is bool and f['retention_pass'] is all(f['original_pass'].values()), 'effect gates')
            require(set(f['failures']) == {'original'+str(n) for n in range(2, 7)} | {'interior4'}, 'failure domains')
            for domain, z in f['failures'].items():
                require(set(z) == {'local', 'order'} and type(z['local']) is int and 0 <= z['local'] <= 72
                        and type(z['order']) is int and 0 <= z['order'] <= 36, 'failure counts')
                passed = f['interior_pass'] if domain == 'interior4' else f['original_pass'][domain[-1]]
                require(passed is (z['local'] == z['order'] == 0), 'failure/gate binding')
        for z in [row['interior'], *row['original_by_length'].values()]:
            fields = ('answers', 'query_pairs', 'control_correct', 'candidate_correct', 'control_both_correct',
                      'candidate_both_correct', 'rescued', 'regressed', 'pair_rescued', 'pair_regressed', 'answer_gain', 'query_pair_gain')
            require(set(z) == set(fields) and all(type(z[k]) is int for k in fields), 'contrast fields')
            require(z['answers'] == 288 and z['query_pairs'] == 144
                    and all(0 <= z[k] <= (144 if k in ('control_both_correct', 'candidate_both_correct', 'pair_rescued', 'pair_regressed') else 288) for k in fields[2:-2]), 'contrast bounds')
            require(z['candidate_correct']-z['control_correct'] == z['answer_gain'] == z['rescued']-z['regressed']
                    and z['candidate_both_correct']-z['control_both_correct'] == z['query_pair_gain'] == z['pair_rescued']-z['pair_regressed'], 'contrast conservation')


def measure(model, mode, data, old, new, cx):
    x = cx[-1]
    with torch.no_grad(), x.c.p267.counted(model, x.c.core) as (calls, cores), readout(model, x.wide, mode) as stats:
        raw = source().base().evaluate(model, data, old, new, cx)
    require(calls == [171, 16416] and cores[0] == 684 and stats == dict(calls=171, query_calls=342, rows=16416, grad_calls=0), 'measured native work')
    return raw, dict(stats)


def load_evidence(folder, read):
    data = read(folder/'dataset.json'); old = read(folder/'original-prompts.json'); new = read(folder/'interior-prompts.json')
    prior = torch.load(folder/'evaluations.pt', map_location='cpu', weights_only=True)
    require(set(prior) == {'schema', 'trajectories', 'records'} and prior['schema'] == 'fold-c329-evaluations-v1'
            and [(r['seed'], r['arm']) for r in prior['records']] == identities(), 'C329 writer schema')
    return data, old, new, prior['records']


def run_probe(out, source_out, cx, root, pins, parent_flags, read):
    data, old, new, prior = load_evidence(source_out, read)
    input_hash = digest((data, old, new))
    p = source(); states = p.load_bundle(source_out/'trained-models.pt'); records = []
    for state, saved in zip(states, prior, strict=True):
        require(p.state_hash(state) == saved['state_sha256'], 'accepted checkpoint hash')
        model = p.make_model(saved['seed'], cx[-1]); p.base().check_dependencies(root, pins, cx, model)
        model.load_state_dict(state, strict=True); model.eval(); model.requires_grad_(False)
        initial = p.state_hash(model.state_dict()); raw = {}; receipts = {}
        require(initial == saved['state_sha256'], 'loaded state identity')
        for mode in MODES:
            raw[mode], receipts[mode] = measure(model, mode, data, old, new, cx)
            require(p.state_hash(model.state_dict()) == initial, 'frozen checkpoint mutated')
        records.append(dict(seed=saved['seed'], arm=saved['arm'], state_sha256=initial, raw=raw, receipts=receipts))
        print(f"[C331] seed={saved['seed']} arm={saved['arm']} three_modes=COMPLETE weights=UNCHANGED", flush=True)
    archive = dict(schema='fold-c331-query-probe-v1', records=records)
    metrics, summary = analyze(archive, prior, data, cx, parent_flags)
    require(digest((data, old, new)) == input_hash, 'source data mutated in memory')
    torch.save(archive, out/'evaluations.pt')
    for name, value in (('diagnostic-plan.json', manifest()), ('measurements.json', metrics), ('validation-summary.json', summary)):
        with (out/name).open('xb') as stream:
            stream.write(blob(value))
    return summary


def semantic_recheck(out, source_out, cx, parent_flags, read):
    data, _, _, prior = load_evidence(source_out, read)
    archive = torch.load(out/'evaluations.pt', map_location='cpu', weights_only=True)
    metrics, summary = analyze(archive, prior, data, cx, parent_flags)
    for name, value in (('diagnostic-plan.json', manifest()), ('measurements.json', metrics), ('validation-summary.json', summary)):
        require(blob(read(out/name)) == blob(value), 'saved probe reconstruction:'+name)
    return summary


def native_preflight(source_out, cx, root, pins, read):
    # This discarded model never supplies a scientific state or a selected coefficient.
    data = read(source_out/'dataset.json'); old = read(source_out/'original-prompts.json')
    p = source(); x = cx[-1]; model = p.make_model(SEEDS[0], x); p.base().check_dependencies(root, pins, cx, model)
    with torch.no_grad():
        w = model.read.output.weight
        w.copy_(torch.sin(torch.arange(w.numel(), dtype=torch.float64).reshape_as(w))*.03)
    model.eval(); model.requires_grad_(False); before = p.state_hash(model.state_dict())
    i = next(i for i, r in enumerate(data['TRAIN']) if r['language'] == 'en')
    for n, view in ((1, 'normal'), (1, 'query_blind'), (6, 'normal'), (6, 'query_blind')):
        text = old[str(n)]['TRAIN']['repeat'][i]['views'][view]
        tokens = x.wide.prefix_tensor(text)[None, :]; tasks = torch.zeros(1, dtype=torch.int64)
        with torch.no_grad():
            native = model(tokens, tasks)
            with readout(model, x.wide, 'native_before'):
                checked = model(tokens, tasks)
            with readout(model, x.wide, 'first_mean'):
                candidate = model(tokens, tasks)
        same(native, checked)
        x.c.p267.check_logits(candidate, 1)
        if n == 1 or view == 'query_blind':
            same(native, candidate)
    require(p.state_hash(model.state_dict()) == before, 'probe model mutation')
    print('C331_native_preflight=PASS;forwards=12;rows=12;optimizer_steps=0;cohort_started=False', flush=True)
