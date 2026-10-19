"""C334: a complete frozen training-policy by inference-policy crossover."""
from __future__ import annotations
import hashlib
import importlib
import itertools
import json
import re
import torch

EXPERIMENT_ID = 'C334-v5b-frozen-policy-crossover'
STAGE = 'V5-B-FROZEN-POLICY-CROSSOVER'
SEEDS = tuple(range(332001, 332006))
ARMS = ('native', 'first_mean')
MODES = ('own_before', 'cross', 'own_after')
DOMAINS = ('original2', 'original3', 'original4', 'original5', 'original6', 'interior4')
OWN = ('fold_lm/v05_benchmarks/model_c334_frozen_policy_crossover.py',
       'tools/c334_execution.py', 'tests_lm/test_v05_c334_frozen_policy_crossover.py',
       'tools/run_c334.ps1', 'tools/invoke_c334.ps1',
       'docs/experiment-ledger-addendum-c334-preregistration.md')
OUTPUTS = ('diagnostic-plan.json', 'evaluations.pt', 'measurements.json', 'validation-summary.json')
OWN_TESTS, FULL_TESTS, MODULES = 32, 6010, 224
SOURCE_COUNT, INPUT_COUNT = 865, 3430
RECEIPT = dict(calls=171, query_calls=342, rows=16416, grad_calls=0)
WORK = dict(models=10, scored_states=20, model_forward_calls=5130, row_presentations=492480,
            core_forward_calls=20520, query_projection_calls=10260, model_state_loads=10,
            checkpoint_bundle_loads=1, train_steps=0, gradient_calls=0, optimizer_steps=0,
            new_checkpoint_writes=0, network_calls=0)
MANIFEST_SHA = '7cfbcfdd88bcfbe55bc7e7f9e84b839984f4f7cac01510330027622e71cc69ce'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)+'\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def trained():
    return importlib.import_module('fold_lm.v05_benchmarks.model_c332_trained_first_mean_query')


def identities():
    return list(itertools.product(SEEDS, ARMS))


def policy(arm, mode):
    require(type(arm) is str and arm in ARMS and type(mode) is str and mode in MODES, 'registered crossover policy')
    return ARMS[1-ARMS.index(arm)] if mode == 'cross' else arm


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE,
        acceptance_base='0b63bcc7f7efe1045f2bfb6644e6b4426e20b19b',
        parent_execution='4545da60d8e54bb3a46f090259644c44eacdab1b',
        parent_summary='abfda3d87ecc44c66cf4509382ced20ffe8fdc8452e36298a777e6b891f1c19b',
        parent_envelope='7b3cef93cba77cba008a48bc4466e5f7c1fc3523f0a57ef6de3867550ce7d479',
        question='at all fixed C332 states, how do the two inference policies interact with the policy used to train the weights',
        identities=[list(v) for v in identities()], modes=list(MODES), domains=list(DOMAINS),
        changed='within each fixed checkpoint only inference readout switches native<->first_mean;own policy restored after',
        held='all10weights,seeds,prompts,targets,domains,original readout functions,coefficient.5,last-query branch,thresholds',
        routing=[[arm, mode, policy(arm, mode)] for arm in ARMS for mode in MODES],
        diagonal='own_before reproduces C332 evaluation and replay;all scores/flags and full paired comparison reproduce C332',
        controls='all raw leaves finite CPUfloat64;logit drift<=1e-9 AND exact argmax;own_after and same-weight query_blind/English original1',
        interaction='(first_mean inference minus native inference on first_mean-trained weights) minus the same contrast on native-trained weights',
        intervention='unchanged C331 .5*(mean+first UTF8 byte local representation),last byte branch unchanged;not a Unicode-character endpoint',
        gate='integrity only;benefit,tie,harm retained;no per-example model/policy choice or tuned threshold',
        thresholds=dict(accuracy=.90, query_pair_accuracy=.80, evidence_drop=.35, query_drop=.35, both_order=.80),
        parameters=14256, core_parameters=3328, slots=64, precision='cpu float64', threads=2,
        parent_files=455, parent_test_proof_files=449, source_count=SOURCE_COUNT, input_count=INPUT_COUNT,
        own_tests=OWN_TESTS, full_tests=FULL_TESTS, modules=MODULES, outputs=list(OUTPUTS),
        raw_logit_payload_bytes=1008599040,
        preflight='one discarded C332-factory model,4English original1/6 normal/queryblind prompts;unhooked baseline+both3-mode sequences=28forwards/28rows/0updates',
        parent_semantics='immediate C333 pure JSON replay;older scientific bodies not rerun;all older source/input/proofs protected',
        nonclaims='fixed-state inference effects and training-by-inference interaction,not mediation attribution,proof of internal mechanism,trained hybrid,independent samples,efficiency or adoption',
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(digest(manifest()) == MANIFEST_SHA, 'C334 manifest seal')


def same_tree(a, b):
    """Do not confuse small logit drift with equal decisions."""
    errors = []
    def walk(x, y):
        if type(x) is dict:
            require(type(y) is dict and set(x) == set(y), 'raw tree identity')
            for key in sorted(x):
                walk(x[key], y[key])
        else:
            require(isinstance(x, torch.Tensor) and isinstance(y, torch.Tensor)
                    and x.dtype == y.dtype == torch.float64 and x.device.type == y.device.type == 'cpu', 'raw tensor precision')
            errors.append(trained().readouts().same(x, y))
    walk(a, b)
    require(len(errors) == 114, 'complete114raw-view tensors')
    return max(errors)


def load_prior(folder):
    v = torch.load(folder/'evaluations.pt', map_location='cpu', weights_only=True)
    require(type(v) is dict and set(v) == {'schema', 'records'}
            and v['schema'] == 'fold-c332-evaluations-v1', 'C332 evaluation writer')
    rows = v['records']
    require(type(rows) is list and [(r['seed'], r['arm']) for r in rows] == identities(), 'all C332 states')
    for r in rows:
        require(set(r) == {'seed', 'arm', 'state_sha256', 'readout_mode', 'raw', 'receipts'}
                and type(r['seed']) is int and re.fullmatch('[0-9a-f]{64}', r['state_sha256'])
                and r['readout_mode'] == trained().policy_mode(r['arm'])
                and set(r['raw']) == set(r['receipts']) == {'evaluation', 'replay'}, 'C332 record identity/policy')
        require(all(blob(x) == blob(RECEIPT) for x in r['receipts'].values()), 'parent evaluation receipts')
    return rows


def domain_contrast(comparison, domain):
    return comparison['interior'] if domain == 'interior4' else comparison['original_by_length'][domain[-1]]


def factorial(effects, saved):
    """All four cells; the matched-policy diagonal stays bound to C332."""
    rows = []
    for i, seed in enumerate(SEEDS):
        n, f = effects[2*i:2*i+2]
        ref = saved['paired_comparisons'][i]
        for domain in DOMAINS:
            a = domain_contrast(n['comparison'], domain)
            b = domain_contrast(f['comparison'], domain)
            old = domain_contrast(ref, domain)
            values = {}
            for kind, left, right, maximum in (
                    ('answers', 'control_correct', 'candidate_correct', 288),
                    ('pairs', 'control_both_correct', 'candidate_both_correct', 144)):
                nn, nf, fn, ff = a[left], a[right], b[right], b[left]
                require((nn, ff) == (old[left], old[right]), 'C332 diagonal counts')
                require(all(type(x) is int and 0 <= x <= maximum for x in (nn, nf, fn, ff)), 'factorial count bounds')
                values[kind] = dict(native_native=nn, native_first_mean=nf, first_mean_native=fn,
                    first_mean_first_mean=ff, inference_gain_native_weights=nf-nn,
                    inference_gain_first_mean_weights=ff-fn, interaction=(ff-fn)-(nf-nn))
            rows.append(dict(seed=seed, domain=domain, **values))
    return rows


def check_flags(flags):
    require(set(flags) == {'original_pass', 'interior_pass', 'retention_pass', 'failures'}, 'scorer flags')
    require(set(flags['original_pass']) == set(map(str, range(2, 7)))
            and all(type(v) is bool for v in flags['original_pass'].values())
            and type(flags['interior_pass']) is bool and flags['retention_pass'] is all(flags['original_pass'].values()), 'domain flags')
    require(set(flags['failures']) == set(DOMAINS), 'failure domains')
    for domain, f in flags['failures'].items():
        require(set(f) == {'local', 'order'} and type(f['local']) is int and 0 <= f['local'] <= 72
                and type(f['order']) is int and 0 <= f['order'] <= 36, 'failure counts')
        flag = flags['interior_pass'] if domain == 'interior4' else flags['original_pass'][domain[-1]]
        require(flag is (f['local'] == f['order'] == 0), 'failure/flag consistency')


def check_summary(v):
    require(set(v) == {'diagnostic_complete', 'parent_validation_summary', 'effects', 'factorial', *WORK}, 'summary fields')
    require(v['diagnostic_complete'] is True and all(type(v[k]) is int and v[k] == n for k, n in WORK.items()), 'work/integrity')
    saved = v['parent_validation_summary']; trained().check_summary(saved)
    require(saved['candidate_gate'] is False and [(r['seed'], r['arm']) for r in v['effects']] == identities(), 'cohort/negative parent')
    for row, old in zip(v['effects'], saved['seed_results'], strict=True):
        require(set(row) == {'seed', 'arm', 'own', 'cross', 'comparison', 'max_control_drift'}, 'effect fields')
        require(type(row['seed']) is int, 'seed type')
        check_flags(row['own']); check_flags(row['cross'])
        require(dict(seed=row['seed'], arm=row['arm'], **row['own']) == old, 'all parent flags/failures')
        require(type(row['max_control_drift']) in (int, float) and 0 <= row['max_control_drift'] <= 1e-9, 'control tolerance')
        require(set(row['comparison']) == {'original_by_length', 'interior'}
                and set(row['comparison']['original_by_length']) == set(map(str, range(2, 7))), 'all paired domains')
        for domain in DOMAINS:
            trained().contrast_check(domain_contrast(row['comparison'], domain))
    require(blob(v['factorial']) == blob(factorial(v['effects'], saved)), 'complete factorial reconstruction')


def analyze(archive, prior, data, cx, saved):
    p = trained(); q = p.readouts(); base = p.source().base(); p.check_summary(saved)
    require(type(archive) is dict and set(archive) == {'schema', 'records'}
            and archive['schema'] == 'fold-c334-crossover-v1', 'crossover archive')
    records = archive['records']
    require([(r['seed'], r['arm']) for r in records] == [(r['seed'], r['arm']) for r in prior] == identities(), 'full crossover cohort')
    metrics, effects = [], []
    for row, old in zip(records, prior, strict=True):
        require(set(row) == {'seed', 'arm', 'state_sha256', 'policies', 'raw', 'receipts'}
                and row['state_sha256'] == old['state_sha256']
                and row['policies'] == {mode:policy(row['arm'], mode) for mode in MODES}
                and set(row['raw']) == set(row['receipts']) == set(MODES), 'checkpoint/policy binding')
        for mode in MODES:
            base.validate_raw(row['raw'][mode], data, cx)
            require(blob(row['receipts'][mode]) == blob(RECEIPT), 'actual evaluation workload')
        for raw in old['raw'].values():
            base.validate_raw(raw, data, cx)
        before, cross, after = [row['raw'][mode] for mode in MODES]
        drift = max(same_tree(old['raw']['evaluation'], before), same_tree(old['raw']['replay'], before), same_tree(before, after))
        q.invariant_views(before, cross, data)
        own_score, own_flags = q.summarize_mode(before, data, cx)
        cross_score, cross_flags = q.summarize_mode(cross, data, cx)
        metrics.append(dict(seed=row['seed'], arm=row['arm'], own=own_score, cross=cross_score))
        effects.append(dict(seed=row['seed'], arm=row['arm'], own=own_flags, cross=cross_flags,
            max_control_drift=drift, comparison=q.compare(before, cross, data, base)))
    # Exact raw-verified original paired contrasts, including individual rescues.
    for i, ref in enumerate(saved['paired_comparisons']):
        diagonal = q.compare(records[2*i]['raw']['own_before'], records[2*i+1]['raw']['own_before'], data, base)
        require(blob(diagonal) == blob({k:ref[k] for k in ('original_by_length', 'interior')}), 'complete C332 paired diagonal')
    result = dict(diagnostic_complete=True, parent_validation_summary=saved, effects=effects,
                  factorial=factorial(effects, saved), **WORK)
    check_summary(result)
    return metrics, result


def run_probe(out, state_out, data_out, cx, root, pins, saved, read):
    p = trained(); data, old, new = p.load_data(data_out, read); before_data = digest((data, old, new))
    prior = load_prior(state_out); states = p.load_states(state_out/'trained-models.pt'); records = []
    require(len(states) == len(prior) == 10, 'state inventory')
    for state, ref in zip(states, prior, strict=True):
        require(p.state_hash(state) == ref['state_sha256'], 'source state hash')
        model = p.make_model(ref['seed'], cx[-1]); p.source().base().check_dependencies(root, pins, cx, model)
        model.load_state_dict(state, strict=True); model.eval(); model.requires_grad_(False)
        initial = p.state_hash(model.state_dict()); require(initial == ref['state_sha256'], 'loaded state hash')
        raw, receipts = {}, {}; policies = {mode:policy(ref['arm'], mode) for mode in MODES}
        for mode in MODES:
            raw[mode], receipts[mode] = p.readouts().measure(model, p.policy_mode(policies[mode]), data, old, new, cx)
            require(p.state_hash(model.state_dict()) == initial, 'frozen model mutated')
        records.append(dict(seed=ref['seed'], arm=ref['arm'], state_sha256=initial, policies=policies, raw=raw, receipts=receipts))
        print(f"[C334] seed={ref['seed']} trained={ref['arm']} own_cross_own=COMPLETE weights=UNCHANGED", flush=True)
    archive = dict(schema='fold-c334-crossover-v1', records=records)
    metrics, result = analyze(archive, prior, data, cx, saved)
    require(digest((data, old, new)) == before_data, 'data/prompt mutation')
    with (out/'evaluations.pt').open('xb') as stream:
        torch.save(archive, stream)
    for name, value in (('diagnostic-plan.json', manifest()), ('measurements.json', metrics), ('validation-summary.json', result)):
        with (out/name).open('xb') as stream:
            stream.write(blob(value))
    return result


def semantic_recheck(out, state_out, data_out, cx, saved, read):
    data, _, _ = trained().load_data(data_out, read)
    archive = torch.load(out/'evaluations.pt', map_location='cpu', weights_only=True)
    metrics, result = analyze(archive, load_prior(state_out), data, cx, saved)
    for name, value in (('diagnostic-plan.json', manifest()), ('measurements.json', metrics), ('validation-summary.json', result)):
        require(blob(read(out/name)) == blob(value), 'saved crossover reconstruction:'+name)
    return result


def native_preflight(data_out, cx, root, pins, read):
    p = trained(); q = p.readouts(); x = cx[-1]; data, old, _ = p.load_data(data_out, read)
    model = p.make_model(SEEDS[0], x); p.source().base().check_dependencies(root, pins, cx, model)
    with torch.no_grad():
        w = model.read.output.weight
        w.copy_(torch.sin(torch.arange(w.numel(), dtype=torch.float64).reshape_as(w))*.03)
    model.eval(); model.requires_grad_(False); initial = p.state_hash(model.state_dict())
    i = next(i for i, row in enumerate(data['TRAIN']) if row['language'] == 'en')
    for n, view in ((1, 'normal'), (1, 'query_blind'), (6, 'normal'), (6, 'query_blind')):
        text = old[str(n)]['TRAIN']['repeat'][i]['views'][view]
        tokens = x.wide.prefix_tensor(text)[None, :]; tasks = torch.zeros(1, dtype=torch.int64)
        with torch.no_grad():
            unhooked = model(tokens, tasks)
            for arm in ARMS:
                logits = []
                for mode in MODES:
                    selected = policy(arm, mode)
                    with q.readout(model, x.wide, p.policy_mode(selected)) as receipt:
                        value = model(tokens, tasks)
                    require(receipt == dict(calls=1, query_calls=2, rows=1, grad_calls=0), 'preflight readout work')
                    x.c.p267.check_logits(value, 1)
                    if selected == 'native' or n == 1 or view == 'query_blind':
                        q.same(unhooked, value)
                    logits.append(value)
                q.same(logits[0], logits[2])
    require(p.state_hash(model.state_dict()) == initial, 'preflight weight mutation')
    print('C334_native_preflight=PASS;forwards=28;rows=28;updates=0;cohort_started=False', flush=True)
