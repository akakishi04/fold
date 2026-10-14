"""C324: equal-budget paired TRAIN-template intervention, native mean+last in both arms."""
from __future__ import annotations
import argparse
import copy
import hashlib
import inspect
import itertools
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import time
from types import ModuleType
import unittest
import torch
from torch.nn import functional as F
from fold_lm.v05_benchmarks import c324_training_templates as templates

EXPERIMENT_ID = 'C324-v5b-interior-coverage-training'
STAGE = 'V5-B-INTERIOR-COVERAGE-TRAINING'
BASE = '88e6b1d5e9fd97aa0c5cb7f3b61a133faa539dcf'
PARENT_EXECUTION = '1090f54bfbb4c1c7ea40d6f7be12124930bd4fd4'
PARENT_SHA = 'fcc87597395300e45eacabaa94b87b6910093669532279f9ed6c67ec3f84af1f'
PARENT_SOURCE = 'fold_lm/v05_benchmarks/model_c323_saved_fact_order_bias.py'
PARENT_BLOB = '9d9dc794ce95d14755e0916b21ebebe2ae2ac176'
DATA_SHA = '1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1'
PROMPTS_SHA = '2a850d72af8c99321fd3dd4243ec2d01df6fda0bb2696329e29e3995a487fffd'
SEEDS = tuple(range(324001, 324006))
ORDERS = tuple(range(324101, 324106))
ARMS = templates.ARMS
PROFILES = templates.OLD_PROFILES
SPLITS = ('TRAIN', 'HOLDOUT')
VIEWS = ('normal', 'evidence_blind', 'query_blind')
STEPS, FIT_RNG = 1200, 612000
OWN = ('fold_lm/v05_benchmarks/model_c324_interior_coverage_training.py',
       'fold_lm/v05_benchmarks/c324_training_templates.py',
       'tests_lm/test_v05_c324_interior_coverage_training.py',
       'tests_lm/test_v05_c324_training_templates.py',
       'tools/run_c324.ps1', 'tools/invoke_c324.ps1',
       'docs/experiment-ledger-addendum-c324-preregistration.md',
       'docs/v5b-interior-coverage-training-v0.1.md')
OUTPUTS = ('experiment-plan.json', 'dataset.json', 'original-prompts.json',
           'interior-prompts.json', 'trained-models.pt', 'evaluations.pt',
           'measurements.json', 'validation-summary.json')
EXCLUDED = 'tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state'
OWN_MODULES = ('tests_lm.test_v05_c324_training_templates', 'tests_lm.test_v05_c324_interior_coverage_training')
WORK = dict(models=10, train_steps=12000, training_rows=576000,
            model_forward_calls=15420, row_presentations=904320, core_forward_calls=61680,
            model_state_loads=10, checkpoint_bundle_loads=1, new_checkpoint_writes=1,
            network_calls=0)
MANIFEST_SHA = 'b726bde41e2b456cca615dde2a8fa36ef3192a73b7526a4a97f03f5f5b33851f'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def constant(value):
        raise ValueError('nonfinite JSON:' + value)
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs, parse_constant=constant)


def child(folder, name):
    require(type(name) is str and name in OUTPUTS, 'unregistered artifact path')
    folder = Path(folder).resolve()
    path = folder / name
    require(path.resolve().parent == folder and not path.is_symlink(), 'unsafe artifact path')
    return path


def identities():
    return list(itertools.product(SEEDS, ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c323_saved_fact_order_bias as p
    q, interior, lengths, trainer, x = p.context()
    return p, q, interior, lengths, trainer, x


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
        parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
        question='does explicit interior-order TRAIN coverage improve held-out binding while retaining original tasks',
        seeds=list(SEEDS), orders=list(ORDERS), arms=list(ARMS), readout='native mean_last in BOTH arms',
        changed='replace only length4 TRAIN templates; original profiles map by slot to C321 interior profiles',
        held='paired initial weights,logical rows,targets,order,length allocation,optimizer,steps,architecture',
        parameters=14256, core_parameters=3328, slots=64, train_lengths=[2, 3, 4],
        steps_per_model=STEPS, rows_per_step=48, fit_rng=FIT_RNG, loss='ordinary mean CE',
        row_length_exposure=[0, 100, 100, 100], core_lr=.0005, other_lr=.005,
        optimizer='AdamW betas .9/.999 eps1e-8 weight_decay0;global gradient clip1',
        data_sha256=DATA_SHA, original_prompts_sha256=PROMPTS_SHA,
        original_eval_lengths=[1, 2, 3, 4, 5, 6], original_gate_lengths=[2, 3, 4, 5, 6],
        interior_profiles=list(templates.INTERIOR_PROFILES), splits=list(SPLITS), views=list(VIEWS),
        primary='ALL5 candidate interior gates AND original2..6 retention AND strictly positive paired HOLDOUT correct-answer and both-query-correct counts',
        gates=dict(accuracy=.90, query_pair=.80, evidence_drop=.35, query_drop=.35, two_order=.80),
        comparison='HOLDOUT gains aggregate all three profiles and both languages within each paired seed; report rescues and regressions',
        boundary='seen interior templates,held-out logical value combinations;not unseen-pattern generalization or structural impossibility',
        original_single='length1 is descriptive only', parents=50, source_pins=792,
        protected_inputs=1491, own_tests=64, modules=210, loaded_tests=5358, focused_tests=5357,
        excluded_test=EXCLUDED, outputs=list(OUTPUTS), raw_logit_payload_bytes=336199680,
        dtype='CPU float64', threads=2, deterministic=True, replay_tolerance=1e-9,
        internal_steps_per_forward=4, peak_memory_scope='process high-water RSS includes ancestor verification',
        work_scope='child scientific fitting/evaluation/replay only;artifact verification and software tests are separate',
        gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(re.fullmatch('[0-9a-f]{64}', MANIFEST_SHA) is not None and digest(manifest()) == MANIFEST_SHA, 'manifest seal')


def parent_hashes(cx):
    p, q, interior, lengths, trainer, _ = cx
    return (PARENT_SHA, *p.parent_ordered_hashes(q, interior, lengths, trainer))


def validate_parent(result):
    require(result['experiment_id'] == 'C323-v5b-saved-fact-order-bias'
            and result['commit_sha'] == PARENT_EXECUTION and result['status'] == 'PASS'
            and result['diagnostic_execution_valid'] is True and result['capability_gate_applicable'] is False,
            'parent identity')
    require(len(result['source_blobs']) == 784 and len(result['input_sha256']) == 1478
            and result['source_blobs'].get(PARENT_SOURCE) == PARENT_BLOB, 'parent protection')
    require(len(result['artifacts']) == 4 and {a['file'] for a in result['artifacts']} ==
            {'audit-plan.json', 'order-counterfactuals.json', 'measurements.json', 'validation-summary.json'}, 'parent artifacts')
    expected = {('mean_last', 'old4'): (4320, 0), ('last_only', 'old4'): (4320, 0),
                ('mean_last', 'interior'): (2211, 814), ('last_only', 'interior'): (2292, 809)}
    rows = result['validation_summary']['overall']
    require(result['validation_summary']['diagnostic_complete'] is True and len(rows) == 4
            and {(r['arm'], r['condition']): (r['correct'], r['same_value_all_four']) for r in rows} == expected,
            'accepted parent outcomes')


def load_parent(paths):
    cx = context()
    p, _, interior, lengths, trainer, x = cx
    paths = [Path(z).resolve() for z in paths]
    hashes = parent_hashes(cx)
    require(len(paths) == len(hashes) == 50 and len(set(paths)) == 50, '50 ordered parents')
    require(all(sha(z) == h for z, h in zip(paths, hashes, strict=True)), '50 parent hashes')
    with x.guarded.no_neural():
        result, _ = p.verify_artifacts(paths[0].parent, paths[1:], PARENT_EXECUTION)
        p.validate_result(result)
        validate_parent(result)
        # These two C319 JSON artifacts are covered by the recursive parent verification.
        data = read_json(paths[4].parent / 'dataset.json')
        old = read_json(paths[4].parent / 'length-datasets.json')
        require(digest(data) == DATA_SHA == trainer.DATA_SHA and digest(old) == PROMPTS_SHA == trainer.PROMPTS_SHA,
                'canonical C319 JSON')
        x.c.p267.validate_data(data)
        new = interior.new_prompts(data)
        interior.check_prompts(data, old, new, lengths, x)
    return result, data, old, new


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.STDOUT).decode('utf-8').strip()


def guard(root, head):
    p, _, _, _, trainer, x = context()
    p.guard(root, head, trainer, x)


def check_dependencies(root, pins, cx, model=None):
    p, q, interior, lengths, trainer, x = cx
    modules = [p, q, interior, lengths, trainer, templates, x.parent, x.wide, x.policy, x.p312, x.pairs,
               x.diag, *vars(x.c).values(), x.c.factory.language_module()]
    for mod in modules:
        filename = getattr(mod, '__file__', None) if isinstance(mod, ModuleType) else None
        if filename and Path(filename).resolve().is_relative_to(root):
            require(Path(filename).resolve().relative_to(root).as_posix() in pins, 'unprotected direct dependency:' + filename)
    if model is not None:
        for module in model.modules():
            filename = inspect.getfile(type(module))
            if Path(filename).resolve().is_relative_to(root):
                require(Path(filename).resolve().relative_to(root).as_posix() in pins, 'unprotected model class:' + filename)


def verify_inputs(inputs):
    for name, expected in inputs.items():
        require(sha(name) == expected, 'protected input changed:' + name)


def precheck(paths, root):
    validate_seal()
    cx = context()
    result, data, old, new = load_parent(paths)
    root = Path(root).resolve()
    pins, inputs = dict(result['source_blobs']), dict(result['input_sha256'])
    for name, expected in pins.items():
        require(git(root, 'rev-parse', 'HEAD:' + name) == expected, 'source changed:' + name)
    verify_inputs(inputs)
    folder = Path(paths[0]).resolve().parent
    descriptors = [('summary.json', PARENT_SHA)] + [(a['file'], a['sha256']) for a in result['artifacts']]
    for name, expected in descriptors:
        path = folder / name
        require(path.resolve().parent == folder and not path.is_symlink(), 'parent artifact path')
        require(str(path) not in inputs and sha(path) == expected, 'parent output integrity')
        inputs[str(path)] = expected
    for name in OWN:
        require(name not in pins, 'OWN collision')
        pins[name] = git(root, 'rev-parse', 'HEAD:' + name)
    inputs.update(cx[-1].c.audit.protect_tree_files(root, pins))
    require((len(pins), len(inputs)) == (792, 1491), 'protection inventory')
    check_dependencies(root, pins, cx)
    require(cx[-1].policy.CORE_LR == .0005 and cx[-1].policy.BASE_LR == .005, 'optimizer constants')
    print(f'registration_check = source_pins:792; protected_inputs:1491; manifest_sha256:{MANIFEST_SHA}', flush=True)
    return pins, inputs, (data, old, new)


def training_views(train_rows, original_train, interior_train):
    result = {arm: templates.build_training_views(train_rows, original_train, interior_train if arm == 'interior4' else None, arm=arm)
              for arm in ARMS}
    a, b = (result[arm] for arm in ARMS)
    require(a.source_ids == b.source_ids and a.targets == b.targets, 'paired teacher alignment')
    require({k for k in a.tables if a.tables[k] != b.tables[k]} == {(4, p) for p in PROFILES}, 'only length4 changes')
    return result


def tensor_tables(view, wide):
    require(len(view.targets) == 192 and set(view.tables) == set(itertools.product((2, 3, 4), PROFILES)), 'TRAIN inventory')
    tables = {key: torch.stack([wide.prefix_tensor(text) for text in texts]) for key, texts in view.tables.items()}
    require(all(z.shape == (192, 64) and z.dtype == torch.int64 and z.device.type == 'cpu' for z in tables.values()), 'TRAIN tensors')
    return tables, torch.tensor(view.targets, dtype=torch.int64)


def schedule(seed, train_rows, x):
    require(type(seed) is int and seed in SEEDS and len(train_rows) == 192, 'schedule identity')
    events = x.parent.plan_for_order(ORDERS[SEEDS.index(seed)], 'two_to_four', train_rows, x.p312, x.pairs)
    stats = x.parent.schedule_stats(events)
    require(stats['per_length_row_exposures'] == [[n] * 192 for n in (0, 100, 100, 100)], 'row exposures')
    require(all(sorted(events[4*i:4*i+4, :, 2:].flatten().tolist()) == list(range(192)) for i in range(300)), 'complete epochs')
    return events


def make_models(seed, x):
    require(type(seed) is int and seed in SEEDS, 'fresh model seed')
    c = x.c
    reference = c.c278.MeanFinalDualReadout(c.factory.new_model(seed), seed, c.reader, c.c269.query_span_mask)
    template = x.wide.LengthReadout(reference)
    models = {arm: x.policy.configure(copy.deepcopy(template), 'core_slow') for arm in ARMS}
    pointers = set()
    for model in models.values():
        require(type(model) is x.wide.LengthReadout and model.backbone.config.max_tokens == 64
                and model.backbone.core.config.slots == 64, 'native architecture')
        require(sum(z.numel() for z in model.parameters()) == 14256
                and sum(z.numel() for z in model.backbone.core.parameters()) == 3328, 'capacity')
        require(c.base.fingerprint(model) == c.base.fingerprint(reference)
                and list(model.state_dict()) == list(reference.state_dict()), 'paired initialization')
        require(all(z.requires_grad and z.dtype == torch.float64 and z.device.type == 'cpu' for z in model.parameters()), 'precision')
        current = {z.data_ptr() for z in model.parameters()}
        require(not current & pointers, 'shared model storage')
        pointers.update(current)
        x.policy.parameter_groups(model, 'core_slow')
    return models


def fit(model, tables, targets, events, x, label):
    require(events.shape == (STEPS, 24, 4) and events.dtype == torch.int64, 'fit schedule')
    require(set(tables) == set(itertools.product((2, 3, 4), PROFILES))
            and all(z.shape == (192, 64) and z.dtype == torch.int64 for z in tables.values())
            and targets.shape == (192,) and targets.dtype == torch.int64, 'fit TRAIN inputs')
    torch.manual_seed(FIT_RNG)
    optimizer = x.policy.optimizer_for(model, 'core_slow')
    model.train()
    losses, rates, counts, union = [], [], [], {}
    for step, event in enumerate(events):
        x.policy.verify_optimizer(optimizer, model, 'core_slow')
        rates.append([g['lr'] for g in optimizer.param_groups])
        optimizer.zero_grad(set_to_none=True)
        length, profile = map(int, event[0, :2])
        ids = event[:, 2:].flatten()
        z = model(tables[length, PROFILES[profile]][ids], torch.zeros(48, dtype=torch.int64))
        x.c.p267.check_logits(z, 48)
        loss = F.cross_entropy(z, targets[ids])
        require(bool(torch.isfinite(loss)), 'nonfinite training loss')
        losses.append(float(loss.detach()))
        loss.backward()
        received = {name: param.numel() for name, param in model.named_parameters() if param.grad is not None}
        union.update(received)
        counts.append(sum(received.values()))
        torch.nn.utils.clip_grad_norm_(list(model.parameters()), 1., error_if_nonfinite=True)
        optimizer.step()
        if (step + 1) % 200 == 0:
            print(f'[C324] {label} step={step+1}/{STEPS} ce={losses[-1]:.6f}', flush=True)
    model.eval()
    return dict(steps=STEPS, training_rows=57600, fit_rng=FIT_RNG, optimizer_creations=1,
                trainable_parameters=14256, ce_history=losses, optimizer_group_lrs=rates,
                gradient_parameter_counts=counts, gradient_union=dict(sorted(union.items())),
                schedule_events=events.clone(), **x.parent.schedule_stats(events))


def check_fit(result, seed, train_rows, x):
    for key, value in dict(steps=1200, training_rows=57600, fit_rng=FIT_RNG, optimizer_creations=1, trainable_parameters=14256).items():
        require(type(result[key]) is int and result[key] == value, 'fit metadata:' + key)
    events = schedule(seed, train_rows, x)
    require(torch.equal(result['schedule_events'], events) and all(result[k] == v for k, v in x.parent.schedule_stats(events).items()), 'saved schedule')
    require(result['optimizer_group_lrs'] == [[.005, .0005]] * STEPS and len(result['ce_history']) == STEPS
            and all(type(z) in (int, float) and math.isfinite(z) and z >= 0 for z in result['ce_history']), 'fit numeric trace')
    union = result['gradient_union']
    require(union and all(type(k) is str and type(v) is int and v > 0 for k, v in union.items())
            and sum(union.values()) <= 14256, 'gradient union')
    require(len(result['gradient_parameter_counts']) == STEPS
            and all(type(v) is int and 0 < v <= sum(union.values()) for v in result['gradient_parameter_counts']), 'gradient counts')


def evaluate(model, data, old, new, cx):
    _, _, interior, _, _, x = cx
    with torch.no_grad():
        return dict(original=x.parent.evaluate(model, old, data, x.wide, x.c),
                    interior=interior.evaluate_new(model, new, data, x))


def validate_raw(raw, data, cx):
    require(set(raw) == {'original', 'interior'}, 'raw domain inventory')
    cx[-1].parent.validate_raw(raw['original'], data, cx[-1].c)
    interior = raw['interior']
    require(set(interior) == set(SPLITS), 'interior split inventory')
    for split in SPLITS:
        require(set(interior[split]) == set(templates.INTERIOR_PROFILES), 'interior profile inventory')
        for views in interior[split].values():
            require(set(views) == set(VIEWS), 'interior view inventory')
            for z in views.values():
                cx[-1].c.p267.check_logits(z, len(data[split]))
                require(not z.requires_grad, 'detached saved logits')


def replay_error(a, b, data, cx):
    validate_raw(a, data, cx)
    validate_raw(b, data, cx)
    error = cx[-1].parent.replay_error(a['original'], b['original'], data, cx[-1].c)
    for split, profile, view in itertools.product(SPLITS, templates.INTERIOR_PROFILES, VIEWS):
        left, right = a['interior'][split][profile][view], b['interior'][split][profile][view]
        error = max(error, float((left - right).abs().max()))
        require(error <= 1e-9 and torch.equal(left.argmax(1), right.argmax(1)), 'interior strict replay')
    return error


def train_one(model, tables, targets, events, data, old, new, seed, arm, cx):
    trainer, x = cx[-2:]
    c = x.c
    initial, core_initial = c.base.fingerprint(model), c.base.fingerprint(model.backbone.core)
    hooks = trainer.hook_snapshot(model)
    print(f'[C324] seed={seed} arm={arm} phase=training', flush=True)
    with c.p267.counted(model, c.core) as (calls, cores), trainer.trained_readout(model, x.wide, 'mean_last') as stats:
        trained = fit(model, tables, targets, events, x, f'seed={seed} arm={arm}')
        final, core_final = c.base.fingerprint(model), c.base.fingerprint(model.backbone.core)
        model.requires_grad_(False)
        print(f'[C324] seed={seed} arm={arm} phase=original-and-interior-evaluation', flush=True)
        raw = evaluate(model, data, old, new, cx)
    require(calls == [1371, 74016] and cores[0] == 5484
            and stats == dict(calls=1371, query_calls=2742, rows=74016, grad_calls=1200), 'train/eval work')
    require(initial != final and core_initial != core_final and c.base.fingerprint(model) == final
            and trainer.hook_snapshot(model) == hooks, 'learned/preserved state')
    record = dict(seed=seed, arm=arm, readout_policy='mean_last', initial_sha256=initial,
                  core_initial_sha256=core_initial, final_sha256=final, core_final_sha256=core_final,
                  fit=trained, raw=raw, policy_receipt=dict(stats), forward_calls=1371,
                  row_presentations=74016, core_forward_calls=5484)
    return record, {name: z.detach().cpu().clone() for name, z in model.state_dict().items()}


def replay(model, state, record, data, old, new, cx):
    trainer, x = cx[-2:]
    require(list(state) == list(model.state_dict()) and all(state[k].shape == v.shape and state[k].dtype == v.dtype for k,v in model.state_dict().items()), 'checkpoint tensor schema')
    require(state_digest(state) == record['saved_state_sha256'], 'checkpoint tensor digest')
    model.load_state_dict(state, strict=True)
    model.eval()
    model.requires_grad_(False)
    fingerprint = x.c.base.fingerprint(model)
    require(fingerprint == record['final_sha256'], 'checkpoint fingerprint')
    hooks = trainer.hook_snapshot(model)
    with x.c.p267.counted(model, x.c.core) as (calls, cores), trainer.trained_readout(model, x.wide, 'mean_last') as stats:
        raw = evaluate(model, data, old, new, cx)
    require(calls == [171, 16416] and cores[0] == 684
            and stats == dict(calls=171, query_calls=342, rows=16416, grad_calls=0), 'replay work')
    require(x.c.base.fingerprint(model) == fingerprint and trainer.hook_snapshot(model) == hooks, 'replay state preservation')
    record.update(checkpoint_roundtrip=True, reload_max_error=replay_error(record['raw'], raw, data, cx),
                  replay_policy_receipt=dict(stats), replay_forward_calls=171,
                  replay_row_presentations=16416, replay_core_forward_calls=684)
    print(f"[C324] seed={record['seed']} arm={record['arm']} phase=checkpoint-replay PASS", flush=True)


def query_pairs(rows):
    require(bool(rows), 'empty query rows')
    groups = {}
    for index, row in enumerate(rows):
        key = (row['language'], tuple(row['entities']), tuple(row['values']), tuple(row['permutation']))
        group = groups.setdefault(key, {})
        require(row['query'] not in group, 'duplicate query')
        group[row['query']] = index
    result = []
    for (_, entities, _, _), group in groups.items():
        require(set(group) == set(entities), 'incomplete query pair')
        result.append(tuple(group[e] for e in entities))
    require(2 * len(result) == len(rows), 'query pair inventory')
    return result


def heldout_contrast(control, candidate, rows):
    require(set(control) == set(candidate) == set(templates.INTERIOR_PROFILES), 'contrast profiles')
    pairs = query_pairs(rows)
    y = torch.tensor([r['target'] for r in rows], dtype=torch.int64)
    correct = [0, 0]
    both = [0, 0]
    rescued = regressed = pair_rescued = pair_regressed = 0
    for profile in templates.INTERIOR_PROFILES:
        logits = [raw[profile]['normal'] for raw in (control, candidate)]
        for z in logits:
            require(z.shape == (len(rows), 256) and z.dtype == torch.float64 and z.device.type == 'cpu'
                    and bool(torch.isfinite(z).all()), 'contrast logits')
        a, b = [z.argmax(1) == y for z in logits]
        pa, pb = [torch.tensor([bool(mask[i] and mask[j]) for i, j in pairs]) for mask in (a, b)]
        correct[0] += int(a.sum()); correct[1] += int(b.sum())
        both[0] += int(pa.sum()); both[1] += int(pb.sum())
        rescued += int((~a & b).sum()); regressed += int((a & ~b).sum())
        pair_rescued += int((~pa & pb).sum()); pair_regressed += int((pa & ~pb).sum())
    require(correct[1] - correct[0] == rescued - regressed and both[1] - both[0] == pair_rescued - pair_regressed, 'paired accounting')
    return dict(answers=len(rows)*3, query_pairs=len(pairs)*3, control_correct=correct[0], candidate_correct=correct[1],
                control_both_correct=both[0], candidate_both_correct=both[1], answer_gain=correct[1]-correct[0],
                query_pair_gain=both[1]-both[0], rescued=rescued, regressed=regressed,
                pair_rescued=pair_rescued, pair_regressed=pair_regressed)


def fixed_gate(rows):
    require([r['seed'] for r in rows] == list(SEEDS), 'gate seed inventory')
    flags = []
    for r in rows:
        require(type(r['candidate_interior_pass']) is bool and type(r['candidate_retention_pass']) is bool
                and type(r['answer_gain']) is int and type(r['query_pair_gain']) is int, 'gate types')
        flags.append(r['candidate_interior_pass'] and r['candidate_retention_pass'] and r['answer_gain'] > 0 and r['query_pair_gain'] > 0)
    return all(flags), flags


def analyze(records, data, cx):
    require([(r['seed'], r['arm']) for r in records] == identities(), 'complete paired cohort')
    interior, x = cx[2], cx[-1]
    metrics, results = [], []
    for r in records:
        check_fit(r['fit'], r['seed'], data['TRAIN'], x)
        validate_raw(r['raw'], data, cx)
        require(r['readout_policy'] == 'mean_last' and r['initial_sha256'] != r['final_sha256']
                and r['core_initial_sha256'] != r['core_final_sha256'] and r['checkpoint_roundtrip'] is True, 'record state')
        require(r['policy_receipt'] == dict(calls=1371, query_calls=2742, rows=74016, grad_calls=1200)
                and r['replay_policy_receipt'] == dict(calls=171, query_calls=342, rows=16416, grad_calls=0), 'policy receipts')
        fields = ('forward_calls','row_presentations','core_forward_calls','replay_forward_calls','replay_row_presentations','replay_core_forward_calls')
        require(all(type(r[k]) is int for k in fields) and tuple(r[k] for k in fields) == (1371,74016,5484,171,16416,684), 'record work')
        require(type(r['reload_max_error']) in (int,float) and math.isfinite(r['reload_max_error']) and 0 <= r['reload_max_error'] <= 1e-9, 'replay tolerance')
        original = {str(n): x.wide.score_length(data, r['raw']['original'][str(n)], x.c) for n in range(2,7)}
        new_score = interior.score_new(r['raw']['interior'], data, x)
        require(all(type(v['passed']) is bool for v in (*original.values(),new_score)), 'scorer gate types')
        results.append(dict(seed=r['seed'], arm=r['arm'], original_pass={n:v['passed'] for n,v in original.items()},
                            retention_pass=all(v['passed'] for v in original.values()), interior_pass=new_score['passed']))
        single = {s: {v: int((z.argmax(1) == torch.tensor([d['target'] for d in data[s]])).sum())
                      for v,z in r['raw']['original']['1'][s]['repeat'].items()} for s in SPLITS}
        metrics.append(dict(seed=r['seed'], arm=r['arm'], original=original, interior=new_score, single_character=single))
    comparisons = []
    for i, seed in enumerate(SEEDS):
        a, b = records[2*i:2*i+2]
        require(all(a[k] == b[k] for k in ('initial_sha256','core_initial_sha256'))
                and torch.equal(a['fit']['schedule_events'], b['fit']['schedule_events']), 'paired initial/schedule')
        gain = heldout_contrast(a['raw']['interior']['HOLDOUT'], b['raw']['interior']['HOLDOUT'], data['HOLDOUT'])
        comparisons.append(dict(seed=seed, candidate_interior_pass=results[2*i+1]['interior_pass'],
                                candidate_retention_pass=results[2*i+1]['retention_pass'],
                                control_interior_pass=results[2*i]['interior_pass'],
                                control_retention_pass=results[2*i]['retention_pass'], **gain))
    gate, flags = fixed_gate(comparisons)
    for row, flag in zip(comparisons, flags, strict=True):
        row['paired_success'] = flag
    summary = dict(candidate_gate=gate, paired_success_count=sum(flags), seed_results=results,
                   paired_comparisons=comparisons, all_pairs_matched=True, all_replays=True, **WORK)
    return metrics, summary


def state_digest(state):
    require(isinstance(state, dict) and bool(state), 'empty checkpoint state')
    h = hashlib.sha256()
    for name in sorted(state):
        z = state[name]
        require(type(name) is str and isinstance(z, torch.Tensor) and z.device.type == 'cpu'
                and not z.requires_grad and bool(torch.isfinite(z).all()), 'checkpoint tensor')
        h.update(blob([name, str(z.dtype), list(z.shape)]))
        h.update(z.contiguous().numpy().tobytes())
    return h.hexdigest()


def load_bundle(path):
    archive = torch.load(path, map_location='cpu', weights_only=True)
    require(set(archive) == {'schema','identities','readout_policy','states'}
            and archive['schema'] == 'fold-c324-interior-coverage-models-v1'
            and archive['identities'] == [list(v) for v in identities()]
            and archive['readout_policy'] == 'mean_last' and len(archive['states']) == 10, 'checkpoint schema')
    return archive['states']


def validate_result(result):
    require(result['experiment_id'] == EXPERIMENT_ID and result['stage'] == STAGE
            and result['diagnostic_execution_valid'] is True and result['gate_f_candidate'] is False
            and result['production_adoption'] is False, 'result identity')
    require((len(result['source_blobs']),len(result['input_sha256'])) == (792,1491)
            and set(OWN) <= result['source_blobs'].keys() and result['source_blobs'].get(PARENT_SOURCE) == PARENT_BLOB, 'result protection')
    require(len(result['artifacts']) == len(OUTPUTS) and {a['file'] for a in result['artifacts']} == set(OUTPUTS), 'artifact inventory')
    s = result['validation_summary']
    require([(r['seed'],r['arm']) for r in s['seed_results']] == identities()
            and all(type(s[k]) is int and s[k] == v for k,v in WORK.items())
            and s['all_pairs_matched'] is True and s['all_replays'] is True, 'result cohort/work')
    for i,row in enumerate(s['paired_comparisons']):
        candidate = s['seed_results'][2*i+1]
        require(set(candidate['original_pass']) == set(map(str,range(2,7)))
                and all(type(v) is bool for v in candidate['original_pass'].values())
                and candidate['retention_pass'] is all(candidate['original_pass'].values())
                and row['candidate_interior_pass'] is candidate['interior_pass']
                and row['candidate_retention_pass'] is candidate['retention_pass'], 'result paired gate binding')
    gate, flags = fixed_gate(s['paired_comparisons'])
    require(s['candidate_gate'] is gate and s['paired_success_count'] == sum(flags)
            and [r['paired_success'] for r in s['paired_comparisons']] == flags
            and result['status'] == ('PASS' if gate else 'FAIL'), 'result gate')


def peak_rss():
    if sys.platform == 'win32':
        import ctypes
        from ctypes import wintypes
        class Counters(ctypes.Structure):
            _fields_ = [('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)] + [(name,ctypes.c_size_t) for name in
                ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage',
                 'QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
        kernel = ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        api = ctypes.WinDLL('psapi',use_last_error=True).GetProcessMemoryInfo
        api.argtypes = (wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD)
        api.restype = wintypes.BOOL
        counters = Counters();counters.cb = ctypes.sizeof(counters)
        require(bool(api(kernel.GetCurrentProcess(),ctypes.byref(counters),counters.cb)), 'process memory measurement')
        return int(counters.PeakWorkingSetSize)
    import resource
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value if sys.platform == 'darwin' else value*1024)


def run(*, summaries, output_dir, expected_head):
    started = time.perf_counter()
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    root = Path(__file__).resolve().parents[2]
    cx = context()
    guard(root, expected_head)
    pins, inputs, (data, old, new) = precheck(summaries, root)
    views = training_views(data['TRAIN'], {str(n):old[str(n)]['TRAIN'] for n in (2,3,4)}, new['TRAIN'])
    training = {arm:tensor_tables(views[arm],cx[-1].wide) for arm in ARMS}
    out = Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    records, states = [], []
    for seed in SEEDS:
        models = make_models(seed,cx[-1])
        events = schedule(seed,data['TRAIN'],cx[-1])
        for arm in ARMS:
            check_dependencies(root,pins,cx,models[arm])
            r,state = train_one(models[arm],*training[arm],events,data,old,new,seed,arm,cx)
            r['saved_state_sha256'] = state_digest(state)
            records.append(r); states.append(state)
    torch.save(dict(schema='fold-c324-interior-coverage-models-v1',identities=[list(v) for v in identities()],
                    readout_policy='mean_last',states=states),out/'trained-models.pt')
    saved = load_bundle(out/'trained-models.pt')
    for i,seed in enumerate(SEEDS):
        models = make_models(seed,cx[-1])
        for j,arm in enumerate(ARMS):
            replay(models[arm],saved[2*i+j],records[2*i+j],data,old,new,cx)
    metrics, summary = analyze(records,data,cx)
    torch.save(dict(schema='fold-c324-interior-coverage-evaluations-v1',records=records),out/'evaluations.pt')
    values = (manifest(),data,old,new,metrics,summary)
    for name,value in zip((OUTPUTS[0],OUTPUTS[1],OUTPUTS[2],OUTPUTS[3],OUTPUTS[6],OUTPUTS[7]),values,strict=True):
        (out/name).write_bytes(blob(value))
    descriptors = [dict(file=name,sha256=sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in OUTPUTS]
    verify_inputs(inputs)
    guard(root,expected_head)
    result = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status='PASS' if summary['candidate_gate'] else 'FAIL',
                  diagnostic_execution_valid=True,source_blobs=pins,input_sha256=inputs,artifacts=descriptors,
                  validation_summary=summary,gate_f_candidate=False,production_adoption=False,
                  runtime=dict(python=sys.version.split()[0],torch=str(torch.__version__),device='cpu',
                               elapsed_seconds=time.perf_counter()-started,process_peak_rss_bytes=peak_rss(),
                               peak_vram_bytes=None,serialized_artifact_bytes=sum(a['serialized_bytes'] for a in descriptors)))
    validate_result(result)
    (out/'summary.json').write_bytes(blob(result))
    print('C324 paired training, evaluation and checkpoint replay complete',flush=True)
    return result


def verify_artifacts(outdir,summaries,expected_head):
    cx = context()
    out = Path(outdir)
    result = read_json(out/'summary.json')
    validate_result(result)
    require(result['commit_sha'] == expected_head,'execution HEAD')
    verify_inputs(result['input_sha256'])
    for descriptor in result['artifacts']:
        path = child(out,descriptor['file'])
        require(sha(path) == descriptor['sha256'] and path.stat().st_size == descriptor['serialized_bytes'],'artifact bytes')
    with cx[-1].guarded.no_neural():
        _,data,old,new = load_parent(summaries)
        archive = torch.load(out/'evaluations.pt',map_location='cpu',weights_only=True)
        require(set(archive) == {'schema','records'} and archive['schema'] == 'fold-c324-interior-coverage-evaluations-v1','evaluation schema')
        saved = load_bundle(out/'trained-models.pt')
        require([state_digest(state) for state in saved] == [r['saved_state_sha256'] for r in archive['records']], 'persisted checkpoint tensors')
        metrics,summary = analyze(archive['records'],data,cx)
        for name,value in zip((OUTPUTS[0],OUTPUTS[1],OUTPUTS[2],OUTPUTS[3],OUTPUTS[6],OUTPUTS[7]),
                              (manifest(),data,old,new,metrics,summary),strict=True):
            require(read_json(out/name) == value,'persisted:'+name)
    require(result['validation_summary'] == summary,'summary reconstruction')
    return result,metrics


def flatten(suite):
    for test in suite:
        if isinstance(test,unittest.TestSuite):
            yield from flatten(test)
        else:
            yield test


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == 208 and not set(names)&set(OWN_MODULES),'parent regression modules')
    return names + list(OWN_MODULES)


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [test.id() for test in tests]
    require(len(ids) == len(set(ids)) == manifest()['loaded_tests'] and ids.count(EXCLUDED) == 1,'loaded regression suite')
    return unittest.TestSuite(test for test in tests if test.id() != EXCLUDED)


def runtime_preflight(paths,root):
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    pins,_,(data,old,new) = precheck(paths,root)
    cx = context()
    views = training_views(data['TRAIN'],{str(n):old[str(n)]['TRAIN'] for n in (2,3,4)},new['TRAIN'])
    tables = {arm:tensor_tables(views[arm],cx[-1].wide) for arm in ARMS}
    for seed in SEEDS:
        schedule(seed,data['TRAIN'],cx[-1])
    models = make_models(SEEDS[0],cx[-1])
    ids = [next(i for i,r in enumerate(data['TRAIN']) if r['language'] == language) for language in ('en','ja')]
    # Discarded nonzero output head prevents a zero-initialized equality/gradient probe being vacuous.
    for arm in ARMS:
        model = models[arm]
        check_dependencies(Path(root).resolve(),pins,cx,model)
        with torch.no_grad():
            weight = model.read.output.weight
            weight.copy_(torch.sin(torch.arange(weight.numel(),dtype=torch.float64).reshape_as(weight))*.03)
        tokens = tables[arm][0][4,'repeat'][ids]
        model.eval()
        with torch.no_grad():
            expected = model(tokens,torch.zeros(2,dtype=torch.int64))
            with cx[-2].trained_readout(model,cx[-1].wide,'mean_last'):
                actual = model(tokens,torch.zeros(2,dtype=torch.int64))
        require(torch.equal(expected,actual),'native mean_last parity')
        model.train(); model.zero_grad(set_to_none=True)
        with cx[-2].trained_readout(model,cx[-1].wide,'mean_last'):
            loss = F.cross_entropy(model(tokens,torch.zeros(2,dtype=torch.int64)),tables[arm][1][ids])
            loss.backward()
        require(model.read.query.weight.grad is not None
                and all(z.grad is None or bool(torch.isfinite(z.grad).all()) for z in model.parameters()),'TRAIN backward probe')
    print('paired_template_and_native_gradient_preflight = PASS; scientific_training_started = False',flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--summaries',nargs=50,type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--expected-head',required=True)
    run(**vars(parser.parse_args()))


if __name__ == '__main__':
    main()
