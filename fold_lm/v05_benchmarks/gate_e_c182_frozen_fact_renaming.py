"""C182: frozen C181 base inference under consistent fact-index renaming.

No training, teacher generation, auxiliary-head construction, or output repair.
New numeric syntax is a semantic relabeling of reused development cases, not a
new independent semantic holdout. All six source models are retained and scored.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time

import numpy as np
import torch
from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph

EXPERIMENT_ID = 'C182-v5e-frozen-fact-renaming'
STAGE = 'V5-E-FROZEN-FACT-RENAMING'
BASE = '3ec4cd8f2afc664799f1e6bfecfce457dd255ad4'
PARENT_SHA = 'bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98'
SEEDS = (181001, 181002, 181003)
ARMS = ('FINAL_ONLY', 'INTERNAL_SEMANTICS')
SCHEMA = 'c181-proper-internal-semantics-v1'
REPRESENTATION = 'c178-scaled-visible-leaf-binding-v1'
CLASSES = ('KNOWN_ZERO', 'KNOWN_ONE', 'UNRESOLVED')
PERMUTATIONS = tuple(itertools.permutations(range(4)))
IDENTITY = (0, 1, 2, 3)
REPLAY_ATOL = 1e-6
OWN = ('fold_lm/v05_benchmarks/gate_e_c182_frozen_fact_renaming.py',
       'tests_lm/test_v05_c182_frozen_fact_renaming.py', 'tools/run_c182.ps1',
       'docs/experiment-ledger-addendum-c182-preregistration.md')
OUTPUTS = {'renaming-plan.json', 'transform-audit.json', 'frozen-replay.json',
           'renaming-results.json', 'renamed-predictions.npz'}
MANIFEST_SHA = '4aa37d094447417e466048f92d2b4949296078ab77d00f5d7d4b24ec46ff55d5'
require, blob = graph.require, graph.blob


def permutation(value):
    require(isinstance(value, (tuple, list)) and len(value) == 4
            and all(type(i) is int for i in value) and sorted(value) == list(range(4)),
            'An exact old-index to new-index permutation is required')
    return tuple(value)


def rename_raw(raw, old_to_new):
    """Relabel references AND move complete fact records; never read a label."""
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    p = permutation(old_to_new)
    nodes, facts, leaf = binding.validate_raw(raw)
    out = raw.clone()
    new_nodes, new_facts = out[:, 4:46].reshape(-1, 7, 6), out[:, 46:62].reshape(-1, 4, 4)
    mapping = torch.tensor((0,) + tuple(i+1 for i in p), dtype=torch.int64)
    new_nodes[:, :, 2] = mapping[nodes[:, :, 2].long()].to(torch.int32)
    new_facts[:, list(p), :] = facts
    binding.validate_raw(out)
    # A reference must reach the identical complete record after renaming.
    r, n = leaf.nonzero(as_tuple=True)
    require(torch.equal(facts[r, nodes[r, n, 2].long()-1],
                        new_facts[r, new_nodes[r, n, 2].long()-1]), 'Reference meaning changed')
    keep = torch.ones(72, dtype=torch.bool)
    keep[46:62] = False
    keep[6:46:6] = False
    require(torch.equal(raw[:, keep], out[:, keep]), 'Nonreference syntax/runtime changed')
    return out


def state_fingerprint(state):
    require(isinstance(state, dict) and state and all(isinstance(k, str) for k in state),
            'Named tensor state required')
    h = hashlib.sha256()
    for name, t in sorted(state.items()):
        require(isinstance(t, torch.Tensor) and t.device.type == 'cpu'
                and t.dtype == torch.float32 and torch.isfinite(t).all().item(), 'Invalid stored tensor')
        h.update(name.encode()); h.update(str(tuple(t.shape)).encode())
        h.update(t.detach().contiguous().numpy().tobytes())
    return h.hexdigest()


def bare_from_payload(payload, seed, arm, expected_weight_sha):
    """Validate the whole C181 state, but construct ONLY its original base model."""
    require(type(seed) is int and seed in SEEDS and arm in ARMS, 'Unknown source model')
    want = dict(seed=seed, condition=arm, model_schema=SCHEMA, representation=REPRESENTATION,
                proper_nodes_only=True, root_supervision=False, steps=2000,
                alpha=int(arm == ARMS[1]))
    require(isinstance(payload, dict) and all(payload.get(k) == v for k, v in want.items())
            and tuple(payload.get('classes', ())) == CLASSES, 'Source checkpoint contract drift')
    state = payload['state_dict']
    require(state_fingerprint(state) == payload.get('weight_sha256') == expected_weight_sha,
            'Source checkpoint weight fingerprint mismatch')
    # Restoring a frozen model must not select or consume a new initialization seed.
    with torch.random.fork_rng(devices=[]):
        model = graph.SharedGraphProbe(graph.ARMS[1])
    expected_keys = {'base.'+k for k in model.state_dict()} | {'auxiliary.weight', 'auxiliary.bias'}
    require(set(state) == expected_keys and state['auxiliary.weight'].shape == (3, 64)
            and state['auxiliary.bias'].shape == (3,), 'Source state tensor schema drift')
    base_state = {k: state['base.'+k] for k in model.state_dict()}
    require(all(base_state[k].shape == t.shape for k, t in model.state_dict().items()), 'Base tensor shape drift')
    model.load_state_dict(base_state, strict=True)
    model.eval().requires_grad_(False)
    require(graph.fingerprint(model) == state_fingerprint(base_state)
            and sum(t.numel() for t in model.parameters()) == 25726
            and not hasattr(model, 'auxiliary'), 'Bare restore failed')
    require(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.modules()),
            'Unexpected inference hooks')
    return model


def restore_bare(path, seed, arm, expected_weight_sha):
    return bare_from_payload(torch.load(path, map_location='cpu', weights_only=True),
                             seed, arm, expected_weight_sha)


def replay_check(predictions, logits, saved_predictions, saved_logits):
    p, z, sp, sz = map(np.asarray, (predictions, logits, saved_predictions, saved_logits))
    require(p.ndim == sp.ndim == 1 and z.shape == sz.shape == (len(p), 2)
            and sp.shape == p.shape and p.dtype.kind in 'iu' and sp.dtype.kind in 'iu'
            and set(np.unique(sp)) <= {0, 1} and np.isfinite(z).all() and np.isfinite(sz).all(),
            'Malformed/nonfinite replay')
    require(np.array_equal(p, z.argmax(1)) and np.array_equal(sp, sz.argmax(1)), 'Nonraw argmax')
    require(np.array_equal(p, sp), 'Frozen identity decisions do not reproduce C181')
    delta = float(np.max(np.abs(z.astype(np.float64)-sz.astype(np.float64))))
    require(delta <= REPLAY_ATOL, 'Frozen identity logits exceed preregistered tolerance')
    return dict(rows=len(p), decisions_equal=True, max_abs_logit_difference=delta)


def summarize(y, pred, identity_pred, missing, groups):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as order
    y, pred, identity_pred, missing, groups = map(np.asarray, (y, pred, identity_pred, missing, groups))
    require(all(a.shape == y.shape for a in (pred, identity_pred, missing, groups)), 'Summary shape mismatch')
    return dict(metrics=audit.metrics(y, pred, groups),
        by_missing_count={str(k): audit.basic_metrics(y[missing == k], pred[missing == k]) for k in range(5)},
        errors=int((pred != y).sum()), decision_flips=int((pred != identity_pred).sum()),
        exchange=order.transitions(y, identity_pred, pred))


def gate(records):
    if [(r.get('seed'), r.get('arm'), r.get('permutation_index')) for r in records] != [
            (s, a, j) for j in range(1, 24) for s in SEEDS for a in ARMS]:
        return False
    for r in records:
        if r.get('n') != 9396 or type(r.get('errors')) is not int or type(r.get('decision_flips')) is not int:
            return False
        if not 0 <= r['errors'] <= 9396 or not 0 <= r['decision_flips'] <= 9396:
            return False
        if r['arm'] == ARMS[1] and (r['errors'] != 0 or r['decision_flips'] != 0):
            return False
    return True


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, parent_sha256=PARENT_SHA,
        source_execution_head=BASE, source_seeds=SEEDS, arms=ARMS,
        permutations=PERMUTATIONS, mapping='old zero-based fact index -> new index;move whole fact record',
        changed='numeric fact naming/index convention only;all AST links,operators,negations,leaf-visible contents retained',
        data='C174 reused PILOT9396 rows/116templates/4groups;no new semantic group',
        identity_replay_rows=311040, transformed_inputs=216108, transformed_predictions=1296648,
        candidate_transformed_predictions=648324, total_inference_rows=1607688,
        inference_batches=1692, inference_cell_calls=11844, batch=1024,
        replay_atol=REPLAY_ATOL, replay_rtol=0, replay_decisions='exact',
        checkpoint_loads=6, constructed_model='original C179 SharedGraphProbe TREE_LINKS;only base state loaded',
        source_stored_parameters=25921, inference_parameters=25726,
        new_training=0, fresh_seeds=0, teacher_calls=0, auxiliary_forward_calls=0,
        gate='all three INTERNAL_SEMANTICS models correct on every row of every23nonidentitypermutation;no decision flips',
        control='all three FINAL_ONLY checkpoints scored without a perfection requirement',
        finite_failure='VALID NEGATIVE;C181unchanged', invalid='source/schema/replay/nonfinite/incomplete/protection error',
        outputs=sorted(OUTPUTS), device='cpu', dtype='float32', threads=2,
        limits='metamorphic naming robustness on reused tasks;not independent semantic generalization or Gate E')


def precheck(c181_summary, c180_summary, c179_summary, c178_summary, c177_summary, c176_summary, c174_summary, root):
    from fold_lm.v05_benchmarks import gate_e_c181_internal_semantics as previous
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    p174, pins, protected = previous.precheck(c180_summary, c179_summary, c178_summary,
                                             c177_summary, c176_summary, c174_summary, root)
    require(audit.sha(c181_summary) == PARENT_SHA, 'C181 summary hash mismatch')
    parent = audit.read_json(c181_summary); previous.validate_result(parent)
    require(parent['commit_sha'] == BASE and parent['status'] == 'PASS'
            and parent['source_blobs'] == pins, 'Wrong accepted C181 source')
    expected = {'internal-semantics-plan.json', 'teacher-targets.npz', 'teacher-audit.json',
                'pilot-predictions.json', 'training-predictions.npz'}
    expected |= {f'probe-{s}-{a}.pt' for s in SEEDS for a in ARMS}
    require(len(parent['artifacts']) == 11 and {a['file'] for a in parent['artifacts']} == expected,
            'C181 artifact set drift')
    protected[str(Path(c181_summary).resolve())] = PARENT_SHA
    for a in parent['artifacts']:
        f = audit.safe_child(Path(c181_summary).resolve().parent, a['file'])
        require(f.is_file() and f.stat().st_size == a['serialized_bytes'] and audit.sha(f) == a['sha256'],
                'C181 artifact changed: '+a['file'])
        protected[str(f.resolve())] = a['sha256']
    pins = dict(pins)
    for name in previous.OWN: pins[name] = audit.git(root, 'rev-parse', BASE+':'+name).decode().strip()
    allpins = dict(pins)
    for name in OWN: allpins[name] = audit.git(root, 'rev-parse', 'HEAD:'+name).decode().strip()
    protected.update(audit.protect_tree_files(root, allpins))
    require(len(pins) == 76 and len(protected) == 151, 'Source/input union drift')
    require(hashlib.sha256(blob(manifest())).hexdigest() == MANIFEST_SHA, 'C182 manifest drift')
    return parent, p174, pins, protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c181_internal_semantics as previous
    names = previous.regression_modules(root)
    require(len(names) == len(set(names)) == 65, 'Historical regression list drift')
    return names+['tests_lm.test_v05_c182_frozen_fact_renaming']


def validate_result(p):
    expected = dict(identity_replay_rows=311040, transformed_inputs=216108,
        transformed_predictions=1296648, candidate_transformed_predictions=648324,
        total_inference_rows=1607688, inference_batches=1692, inference_cell_calls=11844,
        checkpoint_loads=6, new_training=0, fresh_seeds=0, teacher_calls=0,
        auxiliary_forward_calls=0, actual_acquisitions=0, proof_checker_calls=0,
        evidence_writes=0, network_calls=0)
    require(p['experiment_id'] == EXPERIMENT_ID and p['stage'] == STAGE
            and p['diagnostic_execution_valid'] is True
            and all(p[k] == v for k, v in expected.items()), 'C182 identity/workload drift')
    require(p['production_runtime_modified'] is False and p['gate_e_candidate'] is False
            and len(p['source_blobs']) == 76 and len(p['input_sha256']) == 151, 'C182 scope/protection drift')
    require(len(p['records']) == 138 and len(p['replay']) == 12
            and len(p['artifacts']) == 5 and {a['file'] for a in p['artifacts']} == OUTPUTS, 'C182 output coverage drift')
    require(p['status'] == ('PASS' if gate(p['records']) else 'FAIL'), 'C182 fixed gate disagreement')


def run(*, c181_summary, c180_summary, c179_summary, c178_summary, c177_summary,
        c176_summary, c174_summary, output_dir, expected_head):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as order
    root = Path(__file__).resolve().parents[2]
    args = (c181_summary, c180_summary, c179_summary, c178_summary, c177_summary, c176_summary, c174_summary, root)
    def guard():
        require(audit.git(root, 'rev-parse', 'HEAD').decode().strip() == expected_head, 'HEAD mismatch')
        require(audit.git(root, 'branch', '--show-current').decode().strip() == 'feat/sft-target-loss', 'Branch mismatch')
        require(not audit.git(root, 'status', '--porcelain', '--untracked-files=no').strip(), 'Tracked tree dirty')
    guard(); parent, p174, pins, protected = precheck(*args)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter(); artifacts = []; replay = []; records = []; details = []
    def record(name):
        f = out/name; artifacts.append(dict(file=name, sha256=audit.sha(f), serialized_bytes=f.stat().st_size))
    def save(name, value):
        (out/name).write_bytes(blob(value)); record(name)
    save('renaming-plan.json', dict(manifest(), source_blobs=pins))
    try:
        print('[C182] plan fixed; frozen bare checkpoints; consistent fact renaming; no training', flush=True)
        torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
        data, _ = audit.load_data(Path(c174_summary).resolve().parent, p174)
        train, ev = data['split_codes'] == 0, data['split_codes'] == 1
        raw = torch.from_numpy(data['features']); raw_hash = graph.tensor_sha(raw)
        nodes, _, leaves = binding.validate_raw(raw)
        require(torch.equal(nodes[:, :, 2][leaves].reshape(-1, 4),
                            torch.arange(1, 5, dtype=torch.int32).expand(len(raw), -1)),
                'Original canonical leaf naming changed; novelty proof invalid')
        raw_ev = raw[ev]
        require(len(np.unique(raw_ev.numpy(), axis=0)) == 9396, 'Duplicate source PILOT inputs')
        x = binding.prepare_pair(raw)[1]; x_hash = graph.tensor_sha(x)
        parent_dir = Path(c181_summary).resolve().parent
        saved_train = audit.load_npz(parent_dir/'training-predictions.npz')
        saved_pilot = audit.read_json(parent_dir/'pilot-predictions.json')
        require(set(saved_train) == {'row_indices', 'predictions', 'logits', 'seeds', 'arm_indices'}
                and np.array_equal(saved_train['row_indices'], np.flatnonzero(train))
                and saved_train['predictions'].shape == (6, 42444)
                and saved_train['logits'].shape == (6, 42444, 2)
                and saved_train['logits'].dtype == np.float32
                and np.array_equal(saved_train['seeds'], np.repeat(SEEDS, 2))
                and np.array_equal(saved_train['arm_indices'], np.tile([0, 1], 3))
                and len(saved_pilot) == 6, 'Saved C181 prediction schema drift')
        model_order = [(s, a) for s in SEEDS for a in ARMS]
        models, identity, fingerprints = [], [], []; batches = cells = rows = 0
        for i, (seed, arm) in enumerate(model_order):
            fit = parent['fit_records'][i]
            require((fit['seed'], fit['arm']) == (seed, arm), 'Parent model order drift')
            model = restore_bare(parent_dir/f'probe-{seed}-{arm}.pt', seed, arm, fit['final_sha256'])
            models.append(model); fingerprints.append(graph.fingerprint(model))
            s = saved_pilot[i]
            require((s['seed'], s['arm'], s['model_schema'], s['representation']) ==
                    (seed, arm, SCHEMA, REPRESENTATION)
                    and np.array_equal(s['row_indices'], np.flatnonzero(ev)), 'Pilot row/model identity drift')
            for mask, label, sp, sz, expected in (
                (ev, 'PILOT_EVAL', s['predictions'], s['logits'], parent['pairs'][i//2]['final_only' if i%2 == 0 else 'internal']),
                (train, 'TRAIN_RESUBSTITUTION', saved_train['predictions'][i], saved_train['logits'][i], parent['training_metrics'][i])):
                p, z, meter = graph.predict(model, x[mask])
                check = replay_check(p.numpy(), z.numpy(), sp, sz)
                # Reaggregate SAVED scores exactly; frozen forward separately has a fixed tolerance.
                actual = binding.score(data, np.asarray(sp), np.asarray(sz), mask, audit, order)
                audit.same_metrics(actual, expected)
                replay.append(dict(seed=seed, arm=arm, split=label, **check))
                batches += meter['forward_calls']; cells += meter['cell_calls']; rows += meter['rows']
                if label == 'PILOT_EVAL': identity.append(p.numpy().copy())
        save('frozen-replay.json', replay)
        print('[C182] 1/3 all 311040 identity decisions replayed; auxiliary head absent', flush=True)
        n = 9396; preds = np.empty((6, 23, n), dtype=np.int8); logits = np.empty((6, 23, n, 2), dtype=np.float32)
        hashes = []; y = data['labels'][ev]; missing = order.missing_counts(data['features'][ev]); groups = data['groups'][ev]
        for j, perm in enumerate(PERMUTATIONS[1:], start=1):
            changed = rename_raw(raw_ev, perm); xx = binding.prepare_pair(changed)[1]
            before = graph.tensor_sha(xx); hashes.append(dict(permutation_index=j, old_to_new=perm, raw_sha256=graph.tensor_sha(changed)))
            # The only prepared syntax change is fact IDs; bound visible values remain identical.
            original_nodes = x[ev, 4:46].reshape(-1, 7, 6); new_nodes = xx[:, 4:46].reshape(-1, 7, 6)
            require(torch.equal(original_nodes[:, :, [0, 1, 3, 4, 5]], new_nodes[:, :, [0, 1, 3, 4, 5]]),
                    'Renaming changed operators/links/negation/bound visible values')
            for i, (seed, arm) in enumerate(model_order):
                p, z, meter = graph.predict(models[i], xx)
                preds[i, j-1] = p.numpy(); logits[i, j-1] = z.numpy()
                score = summarize(y, p.numpy(), identity[i], missing, groups)
                rec = dict(seed=seed, arm=arm, permutation_index=j, n=n,
                           errors=score['errors'], decision_flips=score['decision_flips'])
                records.append(rec); details.append(dict(**rec, old_to_new=perm, score=score))
                batches += meter['forward_calls']; cells += meter['cell_calls']; rows += meter['rows']
            require(graph.tensor_sha(xx) == before, 'Transformed input changed during inference')
            errors = [records[-6+i]['errors'] for i in (1, 3, 5)]
            print(f'[C182] permutation={j}/23 old_to_new={perm} candidate_errors={errors}', flush=True)
        require(graph.tensor_sha(raw) == raw_hash and graph.tensor_sha(x) == x_hash, 'Original inputs changed')
        save('transform-audit.json', dict(source_rows=9396, unique_source_rows=9396,
            canonical_source_leaf_order=[1, 2, 3, 4], nonidentity_permutations=23,
            transformed_inputs=216108, overlap_with_original_numeric_inputs=0,
            novelty_basis='bijective transforms;23distinctnoncanonicalleaforders;all51840originalleaforderscanonical',
            labels='inherited;no solver or teacher generation', transforms=hashes))
        save('renaming-results.json', details)
        np.savez_compressed(out/'renamed-predictions.npz', row_indices=np.flatnonzero(ev).astype('<i4'),
            permutations=np.asarray(PERMUTATIONS[1:], dtype=np.int8), predictions=preds, logits=logits,
            seeds=np.repeat(np.asarray(SEEDS, dtype='<i4'), 2), arm_indices=np.tile(np.arange(2, dtype=np.int8), 3))
        record('renamed-predictions.npz')
        print('[C182] 2/3 all 1296648 renamed predictions collected; no cases discarded', flush=True)
        guard(); precheck(*args)
        require([graph.fingerprint(m) for m in models] == fingerprints, 'Frozen weights changed')
        for name, h in protected.items(): require(audit.sha(name) == h, 'Protected input changed: '+name)
        for a in artifacts: require(audit.sha(out/a['file']) == a['sha256'], 'Output changed')
        aggregates = []
        for i, (seed, arm) in enumerate(model_order):
            aggregate = summarize(np.tile(y, 23), preds[i].reshape(-1), np.tile(identity[i], 23),
                                  np.tile(missing, 23), np.tile(groups, 23))
            aggregates.append(dict(seed=seed, arm=arm, **aggregate))
        result = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head,
            status='PASS' if gate(records) else 'FAIL', diagnostic_execution_valid=True,
            C181_summary_sha256=PARENT_SHA, data_content_sha256=audit.DATA_SHA,
            source_blobs=pins, input_sha256=protected, artifacts=artifacts, replay=replay,
            records=records, aggregates=aggregates, identity_replay_rows=311040,
            transformed_inputs=216108, transformed_predictions=preds.size,
            candidate_transformed_predictions=preds[1::2].size, total_inference_rows=rows,
            inference_batches=batches, inference_cell_calls=cells, checkpoint_loads=len(models),
            new_training=0, fresh_seeds=0, teacher_calls=0, auxiliary_forward_calls=0,
            actual_acquisitions=0, proof_checker_calls=0, evidence_writes=0, network_calls=0,
            production_runtime_modified=False, gate_e_candidate=False,
            environment=dict(torch=torch.__version__, numpy=np.__version__, device='cpu', dtype='float32', threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['same development semantic tasks;only fact naming/index layout is new',
                         'three candidate checkpoints reused;no fresh-seed or independent-holdout confirmation',
                         'no new training,hidden answers,teacher,auxiliary inference or prediction repair',
                         'all FINAL_ONLY controls scored;their errors do not invalidate candidate robustness'])
        validate_result(result); (out/'summary.json').write_bytes(blob(result))
        print('[C182] 3/3 source/output preservation checked', flush=True)
        print('=== C182 RESULT ===', flush=True); print(blob(result).decode(), flush=True)
        return result
    except Exception as exc:
        (out/'invalid.json').write_bytes(blob(dict(experiment_id=EXPERIMENT_ID, status='INVALID',
            diagnostic_execution_valid=False, error=str(exc), completed_replay=replay, completed_records=records)))
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('c181-summary', 'c180-summary', 'c179-summary', 'c178-summary', 'c177-summary', 'c176-summary', 'c174-summary', 'output-dir'):
        parser.add_argument('--'+name, type=Path, required=True)
    parser.add_argument('--expected-head', required=True)
    run(**vars(parser.parse_args()))


if __name__ == '__main__':
    main()
