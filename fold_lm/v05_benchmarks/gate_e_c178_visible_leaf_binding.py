"""C178: paired visible-fact binding, not a Boolean solver or production policy.

Only the learned model's input representation changes. Copy already-visible
presence/value beside referencing FACT leaves; keep syntax, labels and model fixed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import torch

from fold_lm.v05 import structured_necessity_probe as api

EXPERIMENT_ID = 'C178-v5e-visible-leaf-binding'
STAGE = 'V5-E-VISIBLE-LEAF-BINDING'
BASE = '691b6df851525469889fe3640e638411ea284b58'
PARENT_SHA = '99f6e98311b50c97081ea0fdad5052c8052d2c36a1b32f0e9f2acfea30df3db4'
SEEDS = (178001, 178002, 178003)
ARMS = ('INDIRECT_FACTS', 'BOUND_VISIBLE_FACTS')
REPRESENTATIONS = ('c174-scaled-indirect-v1', 'c178-scaled-visible-leaf-binding-v1')
OWN = ('fold_lm/v05_benchmarks/gate_e_c178_visible_leaf_binding.py',
       'tests_lm/test_v05_c178_visible_leaf_binding.py', 'tools/run_c178.ps1',
       'docs/experiment-ledger-addendum-c178-preregistration.md')
MANIFEST_SHA = '4393da528c6193cd2d8762cfea081e102e02537148299578806b0f3dcb9facc0'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def tensor_sha(x):
    require(isinstance(x, torch.Tensor) and x.device.type == 'cpu', 'CPU tensor required')
    a = x.detach().contiguous().numpy()
    return hashlib.sha256(str(a.dtype).encode() + str(a.shape).encode() + a.tobytes()).hexdigest()


def validate_raw(raw):
    """Bounded numeric C174 family only; no labels, formula evaluation or inferred facts."""
    require(isinstance(raw, torch.Tensor) and raw.dtype == torch.int32
        and raw.device.type == 'cpu' and raw.ndim == 2 and raw.shape[1] == 72 and len(raw) > 0,
        'Nonempty CPU int32 [N,72] required')
    require(((raw >= 0) & (raw <= 2**24 - 1)).all().item(), 'Noncanonical integer range')
    require((raw[:, 0] == 7).all().item() and (raw[:, 1] == 4).all().item(),
            'This diagnostic accepts exactly seven nodes and four facts')
    nodes, facts = raw[:, 4:46].reshape(-1, 7, 6), raw[:, 46:62].reshape(-1, 4, 4)
    require((nodes[:, :, 0] == 1).all().item() and (facts[:, :, 0] == 1).all().item(), 'Bad active masks')
    require(((nodes[:, :, 1] >= 1) & (nodes[:, :, 1] <= 3)).all().item(), 'Unknown node kind')
    require(((nodes[:, :, 5] == 0) | (nodes[:, :, 5] == 1)).all().item(), 'Bad negation bit')
    leaf = nodes[:, :, 1] == 1
    require((leaf.sum(1) == 4).all().item(), 'Four FACT leaves required')
    ids = nodes[:, :, 2]
    require(((ids[leaf] >= 1) & (ids[leaf] <= 4)).all().item()
        and (ids[~leaf] == 0).all().item(), 'Bad fact reference')
    require(torch.equal(ids.sort(1).values[:, -4:], torch.arange(1, 5, dtype=torch.int32).expand(len(raw), -1)),
            'Original C174 read-once family required')
    require((nodes[:, :, 3:5][leaf] == 0).all().item() and (nodes[:, :, 5][~leaf] == 0).all().item(),
            'Leaf children or internal negation is noncanonical')
    parents = torch.zeros((len(raw), 7), dtype=torch.int32)
    for i in range(7):
        active = ~leaf[:, i]
        for col in (3, 4):
            child = nodes[:, i, col]
            require(((child[active] >= 1) & (child[active] <= i)).all().item(), 'Forward or invalid child')
            parents.scatter_add_(1, (child.to(torch.int64) - 1).clamp(min=0).unsqueeze(1),
                                 active.to(torch.int32).unsqueeze(1))
    want = torch.tensor([1, 1, 1, 1, 1, 1, 0], dtype=torch.int32).expand(len(raw), -1)
    require(torch.equal(parents, want), 'One connected ordered tree required')
    status, present, value = facts[:, :, 1], facts[:, :, 2], facts[:, :, 3]
    require(((status >= 1) & (status <= 8)).all().item(), 'Bad fact status')
    require(((present == 0) | (present == 1)).all().item()
        and torch.equal(present == 1, status == 2), 'Presence/status mismatch')
    require(((value == 0) | (value == 1)).all().item() and (value[present == 0] == 0).all().item(),
            'Unobserved or unusable payload must be zero placeholder')
    require(((raw[:, 64:70] == 0) | (raw[:, 64:70] == 1)).all().item()
        and (raw[:, 70] <= 6).all().item(), 'Bad runtime fields')
    return nodes, facts, leaf


def prepare_pair(raw):
    """Return two [N,72] float32 representations; never produce a C170 PolicyInput.

    On FACT leaves only, the two otherwise-zero child-pointer coordinates become
    [observed_presence, observed_raw_bit], each 0/1 AFTER original feature scaling.
    Internal-node child indices, leaf fact IDs/negation, full fact table and resources
    are unchanged. No NOT/AND/OR is executed; no unknown truth is supplied.
    """
    nodes, facts, leaf = validate_raw(raw)
    indirect = api.prepare(raw, api.ARMS[0])
    bound = indirect.clone()
    for i in range(7):
        rows = torch.nonzero(leaf[:, i], as_tuple=True)[0]
        ids = nodes[rows, i, 2].to(torch.int64) - 1
        bound[rows, 4 + 6*i + 3] = facts[rows, ids, 2].to(torch.float32)
        bound[rows, 4 + 6*i + 4] = facts[rows, ids, 3].to(torch.float32)
    # Lossless relative to original scaled input: only leaf placeholders were replaced.
    restored = bound.clone()
    for i in range(7):
        restored[leaf[:, i], 4 + 6*i + 3] = 0
        restored[leaf[:, i], 4 + 6*i + 4] = 0
    require(torch.equal(restored, indirect), 'Binding unexpectedly changed other features')
    return indirect, bound


def gate(pairs):
    if [p.get('seed') for p in pairs] != list(SEEDS):
        return False
    for p in pairs:
        if not (p.get('paired_initial_equal') is True and p.get('paired_batches_equal') is True):
            return False
        try:
            a, b = p['bound'], p['indirect']
            v = [a['macro_missing_balanced_accuracy'], b['macro_missing_balanced_accuracy'],
                a['metrics']['macro_group_balanced_accuracy'], b['metrics']['macro_group_balanced_accuracy'],
                a['by_missing_count']['1']['needs_recall'], b['by_missing_count']['1']['needs_recall'],
                a['by_missing_count']['3']['sufficient_recall'], b['by_missing_count']['3']['sufficient_recall'],
                a['metrics']['needs_recall'], a['metrics']['sufficient_recall']]
        except (KeyError, TypeError):
            return False
        if not all(type(x) in (int, float) and np.isfinite(x) for x in v):
            return False
        if not (v[0] > v[1] and v[2] >= v[3] and v[4] > v[5] and v[6] > v[7] and v[8] > .5 and v[9] > .5):
            return False
    return True


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, parent_sha256=PARENT_SHA, seeds=SEEDS, arms=ARMS,
        representations=REPRESENTATIONS, changed='visible presence/raw bit copied to leaf placeholder coordinates; no Boolean evaluation',
        data_sha256='eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65',
        train_rows=42444, pilot_rows=9396, train_groups=36, pilot_groups=4,
        model='unchanged C174 NecessityProbe72-128-ReLU-128-ReLU-2', parameters=26114,
        loss='ordinary unweighted CrossEntropyLoss in BOTH arms; unchanged C174 fit',
        steps=2000, batch_size=256, optimizer='Adam', lr=.001, betas=[.9,.999], eps=1e-8,
        weight_decay=0, amsgrad=False, foreach=False, sampling='same private uniform row RNG seed+1000000',
        device='cpu', dtype='float32', threads=2, deterministic_algorithms=True,
        training_updates=12000, examples_drawn=3072000, pilot_predictions=56376,
        training_predictions=254664, inference_batches=312, prepared_rows=51840,
        leaf_fact_reads=207360, copied_numeric_fields=414720,
        evaluation='all six final checkpoints saved/reloaded before scores; raw argmax; save TRAIN logits too',
        primary='equal mean BA within missing counts1,2,3 on reused PILOT_EVAL',
        gate='each seed primary strictly improves; original groupmacro cannot drop; count1 needs/count3 sufficient strictly improve; both aggregate recalls>0.5',
        secondary='both splits: by-count/group metrics, within-count and matched-visible AUC; paired error exchange',
        actual_acquisitions=0, evidence_writes=0, proof_checker_calls=0, historical_checkpoint_loads=0,
        scope='post-C177 development input intervention, not FOLD core, an independent holdout or live control')


def precheck(c177_summary, c176_summary, c174_summary, root):
    from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as previous
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    p176, p174, pins, protected = previous.precheck(c176_summary, c174_summary, root)
    require(audit.sha(c177_summary) == PARENT_SHA, 'C177 summary hash mismatch')
    p = audit.read_json(c177_summary)
    require(p['experiment_id'] == previous.EXPERIMENT_ID and p['commit_sha'] == BASE
        and p['status'] == 'PASS' and p['diagnostic_execution_valid'] is True
        and previous.gate(p['pairs']) and p['source_blobs'] == pins
        and p['C176_summary_sha256'] == previous.PARENT_SHA
        and p['C174_summary_sha256'] == audit.PARENT_SHA, 'Wrong C177 identity/lineage')
    protected[str(Path(c177_summary).resolve())] = PARENT_SHA
    require(len(p['artifacts']) == 2 and {a['file'] for a in p['artifacts']} ==
            {'score-order-plan.json', 'score-order-details.json'}, 'C177 artifact set drift')
    for a in p['artifacts']:
        f = audit.safe_child(Path(c177_summary).resolve().parent, a['file'])
        require(f.is_file() and f.stat().st_size == a['serialized_bytes'] and audit.sha(f) == a['sha256'],
                'C177 artifact changed: ' + a['file'])
        protected[str(f.resolve())] = a['sha256']
    pins = dict(pins)
    for name in previous.OWN:
        pins[name] = audit.git(root, 'rev-parse', BASE + ':' + name).decode().strip()
    require(len(pins) == 60, 'Historical source union drift')
    all_pins = dict(pins)
    for name in OWN:
        all_pins[name] = audit.git(root, 'rev-parse', 'HEAD:' + name).decode().strip()
    protected.update(audit.protect_tree_files(root, all_pins))
    require(len(protected) == 90, 'Protected input count drift')
    require(hashlib.sha256(blob(manifest())).hexdigest() == MANIFEST_SHA, 'Manifest drift')
    return p, p174, pins, protected


def score(data, pred, logits, mask, audit, previous):
    y, g = data['labels'][mask], data['groups'][mask]
    missing = previous.missing_counts(data['features'][mask])
    strata = {str(k): audit.basic_metrics(y[missing == k], pred[missing == k]) for k in range(5)}
    margin = previous.raw_margins(logits, pred)
    ranks = {str(k): previous.rank_pairs(y[missing == k], margin[missing == k]) for k in range(5)}
    return dict(metrics=audit.metrics(y, pred, g), by_missing_count=strata,
        macro_missing_balanced_accuracy=sum(strata[str(k)]['balanced_accuracy'] for k in (1, 2, 3))/3,
        ordering=dict(by_missing_count=ranks, primary=previous.primary(ranks),
            matched_visible=previous.grouped_rank_pairs(audit.blind_keys(data['features'][mask]), y, margin)))


def regression_modules(root):
    import re
    text = (Path(root)/'tools/run_c167.ps1').read_text(encoding='utf-8')
    names = re.findall(r'^\s*"(tests_lm\.[a-zA-Z0-9_]+)"\s*$', text, re.M)
    require(len(names) == len(set(names)) == 51, 'Historical regression list drift')
    return names + ['tests_lm.' + n for n in (
        'test_v05_c168_necessity_observability', 'test_v05_c169_interface_batch',
        'test_v05_c170_structured_task_input', 'test_v05_c171_derived_result',
        'test_v05_c172_action_runtime', 'test_v05_c173_acquisition_lifecycle',
        'test_v05_c174_learned_necessity', 'test_v05_c175_frozen_prediction_audit',
        'test_v05_c176_conditional_loss', 'test_v05_c177_frozen_score_order',
        'test_v05_c178_visible_leaf_binding')]


def run(*, c177_summary, c176_summary, c174_summary, output_dir, expected_head):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as previous
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root, 'rev-parse', 'HEAD').decode().strip() == expected_head, 'HEAD mismatch')
        require(audit.git(root, 'branch', '--show-current').decode().strip() == 'feat/sft-target-loss', 'Branch mismatch')
        require(not audit.git(root, 'status', '--porcelain', '--untracked-files=no').strip(), 'Tracked tree dirty')
    guard(); parent, p174, pins, protected = precheck(c177_summary, c176_summary, c174_summary, root)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter(); fits = []; pairs = []; artifacts = []
    def record(name):
        f = out/name; artifacts.append(dict(file=name, sha256=audit.sha(f), serialized_bytes=f.stat().st_size))
    def save(name, value):
        (out/name).write_bytes(blob(value)); record(name)
    save('leaf-binding-plan.json', dict(manifest(), source_blobs=pins))
    try:
        print('[C178] plan fixed; visible-leaf binding only; same model, unweighted loss and updates', flush=True)
        torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
        data, _ = audit.load_data(Path(c174_summary).resolve().parent, p174)
        train, ev = data['split_codes'] == 0, data['split_codes'] == 1
        raw = torch.from_numpy(data['features']); before = tensor_sha(raw)
        xs = prepare_pair(raw)
        require(tensor_sha(raw) == before and len(raw) == 51840, 'Raw input changed or incomplete')
        save('input-binding-audit.json', dict(raw_tensor_sha256=before,
            indirect_tensor_sha256=tensor_sha(xs[0]), bound_tensor_sha256=tensor_sha(xs[1]),
            prepared_rows=len(raw), leaf_fact_reads=len(raw)*4, copied_numeric_fields=len(raw)*8,
            original_scaled_input_recoverable=True, representation_names=REPRESENTATIONS))
        xtrain = [x[train] for x in xs]; ytrain = torch.from_numpy(data['labels'][train].copy())
        models = {}
        for seed in SEEDS:
            torch.manual_seed(seed); initial = api.NecessityProbe().cpu(); ih = api.fingerprint(initial)
            require(sum(p.numel() for p in initial.parameters()) == 26114, 'Capacity drift')
            for j, arm in enumerate(ARMS):
                def progress(row, seed=seed, arm=arm):
                    print(f"[C178] seed={seed} arm={arm} step={row['step']}/2000 train_loss={row['training_loss']:.6f}", flush=True)
                model, log = api.fit(initial, xtrain[j], ytrain, seed, progress=progress)
                require(api.fingerprint(initial) == ih, 'Initial weights mutated')
                name = f'probe-{seed}-{arm}.pt'
                torch.save(dict(seed=seed, arm=arm, representation=REPRESENTATIONS[j], steps=2000,
                    state_dict=model.state_dict()), out/name)
                payload = torch.load(out/name, map_location='cpu', weights_only=True)
                require((payload['seed'], payload['arm'], payload['representation'], payload['steps']) ==
                        (seed, arm, REPRESENTATIONS[j], 2000), 'Checkpoint metadata drift')
                restored = api.NecessityProbe().cpu(); restored.load_state_dict(payload['state_dict'], strict=True)
                require(api.fingerprint(restored) == api.fingerprint(model), 'Checkpoint roundtrip drift')
                record(name); models[seed, arm] = restored.eval()
                fits.append(dict(seed=seed, arm=arm, representation=REPRESENTATIONS[j], initial_sha256=ih,
                                 final_sha256=api.fingerprint(restored), **log))
        require(len(fits) == 6 and all(f['steps'] == 2000 and f['examples_drawn'] == 512000 for f in fits), 'Incomplete fits')
        require(all(fits[i]['initial_sha256'] == fits[i+1]['initial_sha256'] and
            fits[i]['batch_schedule_sha256'] == fits[i+1]['batch_schedule_sha256'] for i in (0, 2, 4)), 'Unpaired fits')
        pilot_saved = []; train_saved = []; train_logits = []; training = []; changes = []
        for seed in SEEDS:
            eval_scores = []; train_scores = []; preds = []
            for j, arm in enumerate(ARMS):
                p, z = api.predict(models[seed, arm], xs[j][ev])
                tp, tz = api.predict(models[seed, arm], xtrain[j])
                eval_scores.append(score(data, p.numpy(), z.numpy(), ev, audit, previous))
                train_scores.append(score(data, tp.numpy(), tz.numpy(), train, audit, previous))
                pilot_saved.append(dict(seed=seed, arm=arm, representation=REPRESENTATIONS[j],
                    row_indices=np.flatnonzero(ev).tolist(), predictions=p.tolist(), logits=z.tolist()))
                train_saved.append(tp.numpy().astype(np.int8)); train_logits.append(tz.numpy())
                training.append(dict(seed=seed, arm=arm, **train_scores[-1]))
                full = np.empty(51840, dtype=np.int8); full[ev] = p.numpy(); full[train] = tp.numpy(); preds.append(full)
            pairs.append(dict(seed=seed, indirect=eval_scores[0], bound=eval_scores[1],
                              paired_initial_equal=True, paired_batches_equal=True))
            parts = {}
            missing = previous.missing_counts(data['features'])
            for mask, part in ((train, 'TRAIN_RESUBSTITUTION'), (ev, 'PILOT_EVAL')):
                parts[part] = dict(overall=previous.transitions(data['labels'][mask], preds[0][mask], preds[1][mask]),
                    by_missing_count={str(k): previous.transitions(data['labels'][mask & (missing == k)],
                        preds[0][mask & (missing == k)], preds[1][mask & (missing == k)]) for k in range(5)})
            changes.append(dict(seed=seed, parts=parts))
            print(f"[C178] seed={seed} mixed_count_BA indirect={eval_scores[0]['macro_missing_balanced_accuracy']:.6f} bound={eval_scores[1]['macro_missing_balanced_accuracy']:.6f}", flush=True)
        save('pilot-predictions.json', pilot_saved)
        np.savez_compressed(out/'training-predictions.npz', row_indices=np.flatnonzero(train).astype('<i4'),
            predictions=np.stack(train_saved), logits=np.stack(train_logits),
            seeds=np.array([s for s in SEEDS for _ in ARMS], dtype='<i4'), arm_indices=np.tile(np.arange(2, dtype=np.int8), 3))
        record('training-predictions.npz')
        guard(); precheck(c177_summary, c176_summary, c174_summary, root)
        require(tensor_sha(raw) == before, 'Raw inputs mutated')
        for name, want in protected.items():
            require(audit.sha(name) == want, 'Protected input changed: ' + name)
        for a in artifacts:
            require(audit.sha(out/a['file']) == a['sha256'], 'Output changed: ' + a['file'])
        result = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head,
            status='PASS' if gate(pairs) else 'FAIL', diagnostic_execution_valid=True,
            C177_summary_sha256=PARENT_SHA, C176_summary_sha256=previous.PARENT_SHA,
            C174_summary_sha256=audit.PARENT_SHA, data_content_sha256=audit.DATA_SHA,
            source_blobs=pins, input_sha256=protected, artifacts=artifacts, pairs=pairs,
            training_metrics=training, error_exchanges=changes, fit_records=fits,
            fresh_seeds=3, trained_models=6, training_steps_total=12000, training_examples_drawn=3072000,
            training_forward_calls=12000, inference_forward_calls=312, pilot_predictions=56376,
            training_resubstitution_predictions=254664, prepared_rows=51840,
            leaf_fact_reads=207360, copied_numeric_fields=414720,
            historical_checkpoint_deserializations=0, new_checkpoint_deserializations=6,
            actual_acquisitions=0, proof_checker_calls=0, evidence_writes=0, network_calls=0,
            production_runtime_modified=False, gate_e_candidate=False,
            environment=dict(torch=torch.__version__, numpy=np.__version__, device='cpu', dtype='float32', threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['handwritten visible-field binding, not learned binding or logical evaluation',
                'same four reused pilot groups; not independent confirmation',
                'same diagnostic MLP, not FOLD shared core or safe live policy',
                'new input semantics are explicitly checkpoint-bound, not a changed C170 packet or historical model',
                'C176 remains negative; no threshold repair, weighted loss or model/step increase'])
        (out/'summary.json').write_bytes(blob(result))
        print('=== C178 RESULT ===', flush=True); print(blob(result).decode(), flush=True)
        return result
    except Exception as exc:
        (out/'invalid.json').write_bytes(blob(dict(experiment_id=EXPERIMENT_ID, status='INVALID',
            diagnostic_execution_valid=False, error=str(exc), completed_fits=fits, completed_pairs=pairs)))
        raise


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--c177-summary', type=Path, required=True); p.add_argument('--c176-summary', type=Path, required=True)
    p.add_argument('--c174-summary', type=Path, required=True); p.add_argument('--output-dir', type=Path, required=True)
    p.add_argument('--expected-head', required=True)
    run(**vars(p.parse_args()))


if __name__ == '__main__':
    main()
