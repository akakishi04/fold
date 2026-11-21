"""C184: explicit local-index canonicalization before frozen C181 inference.

This is a hand-written input adapter contract, NOT learned naming invariance.
No logical operator is evaluated; full numeric fact records and inverse maps survive.
Historical raw predictions, checkpoints and C182's negative result are never replaced.
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

EXPERIMENT_ID = 'C184-v5e-canonical-fact-index-adapter'
STAGE = 'V5-E-CANONICAL-FACT-INDEX-ADAPTER'
BASE = '53bfa13bc74e74334a610605fc4fb63a4cc84702'
PARENT_SHA = 'ec3b67c7ff865e26d633d03bd5086a9ff60bdc277bc26333085121dc20232c24'
SEEDS = (181001, 181002, 181003)
ARMS = ('FINAL_ONLY', 'INTERNAL_SEMANTICS')
PERMUTATIONS = tuple(itertools.permutations(range(4)))
SCHEMA = 'c184-first-occurrence-local-fact-indices-v1'
ATOL = 1e-6
OWN = ('fold_lm/v05_benchmarks/gate_e_c184_canonical_fact_indices.py',
       'tests_lm/test_v05_c184_canonical_fact_indices.py', 'tools/run_c184.ps1',
       'docs/experiment-ledger-addendum-c184-preregistration.md')
OUTPUTS = {'canonical-index-plan.json', 'canonicalization-audit.json', 'frozen-replay.json',
           'normalized-results.json', 'normalized-predictions.npz'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


def fields(raw):
    """Validate the bounded read-once numeric adapter domain, without solving it.

    Resource/header contents not used by renaming are transported verbatim. This
    helper does not replace the C170 PolicyInput/provenance validation boundary.
    """
    require(isinstance(raw, torch.Tensor) and raw.device.type == 'cpu'
            and raw.dtype == torch.int32 and raw.ndim == 2 and raw.shape[1] == 72
            and len(raw) > 0 and ((raw >= 0) & (raw < 2**24)).all().item(),
            'Nonempty canonical CPUint32 [N,72] required')
    require((raw[:, :2] == torch.tensor([7, 4], dtype=torch.int32)).all().item(),
            'Only seven nodes and four distinct facts are supported')
    nodes = raw[:, 4:46].reshape(-1, 7, 6)
    facts = raw[:, 46:62].reshape(-1, 4, 4)
    require((nodes[:, :, 0] == 1).all().item() and (facts[:, :, 0] == 1).all().item(),
            'Every node and fact must be active')
    kinds = nodes[:, :, 1]
    require(((kinds >= 1) & (kinds <= 3)).all().item(), 'Unknown operator kind')
    leaf = kinds == 1
    require((leaf.sum(1) == 4).all().item(), 'Four leaves required')
    ids = nodes[:, :, 2][leaf].reshape(-1, 4).long()
    require(torch.equal(ids.sort(1).values, torch.arange(1, 5).expand(len(raw), -1)),
            'Read-once fact references must form a permutation of1..4')
    require((nodes[:, :, 2][~leaf] == 0).all().item()
            and (nodes[:, :, 3:5][leaf] == 0).all().item()
            and ((nodes[:, :, 5] == 0) | (nodes[:, :, 5] == 1)).all().item()
            and (nodes[:, :, 5][~leaf] == 0).all().item(), 'Noncanonical node fields')
    parents = torch.zeros((len(raw), 7), dtype=torch.int64)
    for i in range(7):
        for col in (3, 4):
            child = nodes[:, i, col].long(); active = ~leaf[:, i]
            require(((child[active] >= 1) & (child[active] <= i)).all().item(),
                    'Forward or out-of-range child')
            parents.scatter_add_(1, (child-1).clamp(min=0).unsqueeze(1), active.long().unsqueeze(1))
    require(torch.equal(parents, torch.tensor([1]*6+[0]).expand(len(raw), -1)),
            'One connected ordered tree required')
    status, present, value = facts[:, :, 1], facts[:, :, 2], facts[:, :, 3]
    require(((status == 1) | (status == 2)).all().item()
            and torch.equal(present, (status == 2).int())
            and ((value == 0) | (value == 1)).all().item()
            and (value[present == 0] == 0).all().item(), 'Unknown/unusable/hidden fact payload')
    return nodes, facts, leaf, ids-1


def canonicalize(raw):
    """Return copied raw fields and canonical-slot -> input-slot map (zero based).

    First encountered FACT becomes local1, next local2, etc. No label, saved input,
    prediction, operator evaluation or checkpoint is available to this function.
    """
    nodes, facts, leaf, to_input = fields(raw)
    out = raw.clone()
    new_nodes = out[:, 4:46].reshape(-1, 7, 6)
    new_nodes[:, :, 2][leaf] = torch.arange(1, 5, dtype=torch.int32).expand(len(raw), -1).reshape(-1)
    out[:, 46:62] = facts.gather(1, to_input[:, :, None].expand(-1, -1, 4)).reshape(-1, 16)
    return out, to_input.clone()


def restore_input(canonical, to_input):
    """Undo a returned map for numeric records/references; never infer missing facts."""
    nodes, facts, leaf, ids = fields(canonical)
    require(torch.equal(ids, torch.arange(4).expand(len(canonical), -1)), 'Canonical input required')
    require(isinstance(to_input, torch.Tensor) and to_input.device.type == 'cpu'
            and to_input.dtype == torch.int64 and to_input.shape == (len(canonical), 4)
            and torch.equal(to_input.sort(1).values, torch.arange(4).expand(len(canonical), -1)),
            'Exact canonical-to-input bijection required')
    out = canonical.clone()
    out[:, 4:46].reshape(-1, 7, 6)[:, :, 2][leaf] = (to_input+1).int().reshape(-1)
    moved = torch.empty_like(facts)
    moved.scatter_(1, to_input[:, :, None].expand(-1, -1, 4), facts)
    out[:, 46:62] = moved.reshape(-1, 16)
    return out


def normalization_check(raw, reference):
    """Measure finite adapter contract misses; do not disguise them as a PASS."""
    require(raw.shape == reference.shape, 'Comparison shape mismatch')
    before = raw.clone()
    result, mapping = canonicalize(raw)
    twice, _ = canonicalize(result)
    restored = restore_input(result, mapping)
    check = dict(rows=len(raw), canonical_mismatches=int((result != reference).any(1).sum()),
                 roundtrip_mismatches=int((restored != raw).any(1).sum()),
                 idempotence_mismatches=int((twice != result).any(1).sum()),
                 mutated_input_rows=int((before != raw).any(1).sum()))
    return result, mapping, check


def gate(records, checks):
    if not isinstance(checks, list) or len(checks) != 24:
        return False
    for i, c in enumerate(checks):
        if c.get('permutation_index') != i or c.get('rows') != (51840 if i == 0 else 9396):
            return False
        for key in ('canonical_mismatches', 'roundtrip_mismatches', 'idempotence_mismatches', 'mutated_input_rows'):
            if type(c.get(key)) is not int or c[key] != 0:
                return False
    expected = [(s, a, j) for j in range(1, 24) for s in SEEDS for a in ARMS]
    if [(r.get('seed'), r.get('arm'), r.get('permutation_index')) for r in records] != expected:
        return False
    for r in records:
        if r.get('n') != 9396 or type(r.get('errors')) is not int or not 0 <= r['errors'] <= 9396:
            return False
        d = r.get('max_abs_logit_difference')
        if type(d) not in (float, int) or not np.isfinite(d) or not 0 <= d <= ATOL:
            return False
        if type(r.get('decision_flips')) is not int or r['decision_flips'] != 0:
            return False
        if r['arm'] == ARMS[1] and r['errors'] != 0:
            return False
    return True


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, parent_sha256=PARENT_SHA,
        source_execution_head=BASE, schema=SCHEMA, source_seeds=SEEDS, arms=ARMS,
        changed='handwritten first-occurrence LOCAL fact-index canonicalization before unchanged frozen inference',
        scope='read-once4facts/7nodes;rename numeric references and whole4fieldrecords;retain inverse map',
        operator_evaluation=False, label_input=False, hidden_values=False,
        permutations=PERMUTATIONS, original_rows=51840, renamed_inputs=216108,
        normalization_rows=267948, normalizer_row_calls_including_idempotence=535896,
        inverse_row_calls=267948, replay_rows=311040, normalized_predictions=1296648,
        candidate_normalized_predictions=648324, total_inference_rows=1607688,
        inference_batches=1692, inference_cell_calls=11844, checkpoint_loads=6,
        training=0, fresh_seeds=0, teacher_calls=0, auxiliary_calls=0,
        batch=1024, device='cpu', dtype='float32', threads=2, logit_atol=ATOL, logit_rtol=0,
        gate='all exact canonical/roundtrip/idempotence/input checks;all models preserve original decisions/logits;internal errors0',
        claim='adapter-plus-frozen-model contract;canonical equality implies behavior preservation,not new learned generalization',
        limits='reused semantic tasks;no full PolicyInput/provenance/action remapping integration or Gate E',
        outputs=sorted(OUTPUTS))


MANIFEST_SHA = 'de54874ad495253c0111c006b9f40f6c85291fc67a8ad243ceb232c1b13e24ed'


def precheck(c183_summary, c182_summary, c181_summary, c180_summary, c179_summary,
             c178_summary, c177_summary, c176_summary, c174_summary, root):
    from fold_lm.v05_benchmarks import gate_e_c183_frozen_path_attribution as previous
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    _, p181, p174, pins, protected = previous.precheck(c182_summary, c181_summary,
        c180_summary, c179_summary, c178_summary, c177_summary, c176_summary, c174_summary, root)
    require(audit.sha(c183_summary) == PARENT_SHA, 'C183 summary hash mismatch')
    parent = audit.read_json(c183_summary); previous.validate_result(parent)
    require(parent['commit_sha'] == BASE and parent['status'] == 'PASS'
            and parent['source_blobs'] == pins, 'Wrong accepted C183 source')
    protected[str(Path(c183_summary).resolve())] = PARENT_SHA
    for a in parent['artifacts']:
        f = audit.safe_child(Path(c183_summary).resolve().parent, a['file'])
        require(f.is_file() and f.stat().st_size == a['serialized_bytes'] and audit.sha(f) == a['sha256'],
                'Changed C183 artifact:'+a['file'])
        protected[str(f.resolve())] = a['sha256']
    pins = dict(pins)
    for name in previous.OWN: pins[name] = audit.git(root, 'rev-parse', BASE+':'+name).decode().strip()
    allpins = dict(pins)
    for name in OWN: allpins[name] = audit.git(root, 'rev-parse', 'HEAD:'+name).decode().strip()
    protected.update(audit.protect_tree_files(root, allpins))
    require(len(pins) == 84 and len(protected) == 172, 'Source/input union drift')
    require(hashlib.sha256(blob(manifest())).hexdigest() == MANIFEST_SHA, 'Manifest drift')
    return p181, p174, pins, protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c183_frozen_path_attribution as previous
    names = previous.regression_modules(root)
    require(len(names) == len(set(names)) == 67, 'Historical regression list drift')
    return names+['tests_lm.test_v05_c184_canonical_fact_indices']


def validate_result(p):
    expected = dict(normalization_rows=267948, normalizer_row_calls_including_idempotence=535896,
        inverse_row_calls=267948, replay_rows=311040, normalized_predictions=1296648,
        candidate_normalized_predictions=648324, total_inference_rows=1607688,
        inference_batches=1692, inference_cell_calls=11844, checkpoint_loads=6,
        new_training=0, fresh_seeds=0, teacher_calls=0, auxiliary_forward_calls=0,
        actual_acquisitions=0, proof_checker_calls=0, evidence_writes=0, network_calls=0)
    require(p['experiment_id'] == EXPERIMENT_ID and p['stage'] == STAGE
            and p['diagnostic_execution_valid'] is True and all(p[k] == v for k, v in expected.items()),
            'Identity/workload drift')
    require(len(p['source_blobs']) == 84 and len(p['input_sha256']) == 172
            and len(p['replay']) == 12 and len(p['artifacts']) == 5
            and {a['file'] for a in p['artifacts']} == OUTPUTS, 'Coverage/protection drift')
    require(p['production_runtime_modified'] is False and p['gate_e_candidate'] is False, 'Scope drift')
    require(p['status'] == ('PASS' if gate(p['records'], p['normalization_checks']) else 'FAIL'), 'Fixed gate mismatch')


def run(*, c183_summary, c182_summary, c181_summary, c180_summary, c179_summary,
        c178_summary, c177_summary, c176_summary, c174_summary, output_dir, expected_head):
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as order
    graph = frozen.graph; root = Path(__file__).resolve().parents[2]
    args = (c183_summary, c182_summary, c181_summary, c180_summary, c179_summary,
            c178_summary, c177_summary, c176_summary, c174_summary, root)
    def guard():
        require(audit.git(root, 'rev-parse', 'HEAD').decode().strip() == expected_head, 'HEAD mismatch')
        require(audit.git(root, 'branch', '--show-current').decode().strip() == 'feat/sft-target-loss', 'Branch mismatch')
        require(not audit.git(root, 'status', '--porcelain', '--untracked-files=no').strip(), 'Tracked tree dirty')
    guard(); p181, p174, pins, protected = precheck(*args)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False)
    artifacts = []; replay = []; records = []; checks = []; started = time.perf_counter()
    def record(name):
        f = out/name; artifacts.append(dict(file=name, sha256=audit.sha(f), serialized_bytes=f.stat().st_size))
    def save(name, value):
        (out/name).write_bytes(blob(value)); record(name)
    save('canonical-index-plan.json', dict(manifest(), source_blobs=pins))
    try:
        print('[C184] plan fixed; explicit local-index adapter; frozen weights; no learned-invariance claim', flush=True)
        torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
        data, _ = audit.load_data(Path(c174_summary).resolve().parent, p174)
        raw = torch.from_numpy(data['features']); raw_sha = graph.tensor_sha(raw)
        train, ev = data['split_codes'] == 0, data['split_codes'] == 1
        binding.validate_raw(raw)
        require(torch.equal(fields(raw)[3], torch.arange(4).expand(len(raw), -1)), 'Original naming convention drift')
        _, _, check = normalization_check(raw, raw); checks.append(dict(permutation_index=0, **check))
        x = binding.prepare_pair(raw)[1]; x_sha = graph.tensor_sha(x)
        parent_dir = Path(c181_summary).resolve().parent
        old = audit.read_json(parent_dir/'pilot-predictions.json')
        old_train = audit.load_npz(parent_dir/'training-predictions.npz')
        require(len(old) == 6 and np.array_equal(old_train['row_indices'], np.flatnonzero(train))
                and old_train['predictions'].shape == (6, 42444) and old_train['logits'].shape == (6, 42444, 2)
                and np.array_equal(old_train['seeds'], np.repeat(SEEDS, 2))
                and np.array_equal(old_train['arm_indices'], np.tile([0, 1], 3)), 'C181 saved schema drift')
        model_order = [(s, a) for s in SEEDS for a in ARMS]
        models = []; identities = []; fingerprints = []; batches = cells = rows = 0
        for i, (seed, arm) in enumerate(model_order):
            fit = p181['fit_records'][i]; saved = old[i]
            require((fit['seed'], fit['arm']) == (seed, arm) == (saved['seed'], saved['arm'])
                    and np.array_equal(saved['row_indices'], np.flatnonzero(ev)), 'C181 model/row drift')
            model = frozen.restore_bare(parent_dir/f'probe-{seed}-{arm}.pt', seed, arm, fit['final_sha256'])
            models.append(model); fingerprints.append(graph.fingerprint(model))
            for mask, label, sp, sz, expected in (
                (ev, 'PILOT_EVAL', saved['predictions'], saved['logits'], p181['pairs'][i//2]['final_only' if i%2 == 0 else 'internal']),
                (train, 'TRAIN_RESUBSTITUTION', old_train['predictions'][i], old_train['logits'][i], p181['training_metrics'][i])):
                p, z, meter = graph.predict(model, x[mask], batch=1024)
                replay.append(dict(seed=seed, arm=arm, split=label, **frozen.replay_check(p.numpy(), z.numpy(), sp, sz)))
                audit.same_metrics(binding.score(data, np.asarray(sp), np.asarray(sz), mask, audit, order), expected)
                batches += meter['forward_calls']; cells += meter['cell_calls']; rows += meter['rows']
                if label == 'PILOT_EVAL': identities.append((p.numpy().copy(), z.numpy().copy()))
        save('frozen-replay.json', replay)
        print('[C184] 1/3 all311040 original decisions replayed; no teacher or auxiliary head', flush=True)
        n = 9396; predictions = np.empty((6, 23, n), dtype=np.int8)
        logits = np.empty((6, 23, n, 2), dtype=np.float32); maps = []; details = []
        y = data['labels'][ev]; missing = order.missing_counts(data['features'][ev]); groups = data['groups'][ev]
        for j, perm in enumerate(PERMUTATIONS[1:], 1):
            changed = frozen.rename_raw(raw[ev], perm)
            canonical, mapping, check = normalization_check(changed, raw[ev])
            checks.append(dict(permutation_index=j, **check)); maps.append(mapping.numpy().astype(np.int8))
            xx = binding.prepare_pair(canonical)[1]
            for i, (seed, arm) in enumerate(model_order):
                p, z, meter = graph.predict(models[i], xx, batch=1024)
                predictions[i, j-1] = p.numpy(); logits[i, j-1] = z.numpy()
                score = frozen.summarize(y, p.numpy(), identities[i][0], missing, groups)
                delta = float(np.max(np.abs(z.numpy().astype(np.float64)-identities[i][1].astype(np.float64))))
                rec = dict(seed=seed, arm=arm, permutation_index=j, n=n, errors=score['errors'],
                           decision_flips=score['decision_flips'], max_abs_logit_difference=delta)
                records.append(rec); details.append(dict(**rec, old_to_new=perm, score=score))
                batches += meter['forward_calls']; cells += meter['cell_calls']; rows += meter['rows']
            print(f'[C184] permutation={j}/23 canonical_mismatches={check["canonical_mismatches"]} candidate_errors={[records[-6+i]["errors"] for i in (1,3,5)]}', flush=True)
        save('canonicalization-audit.json', dict(schema=SCHEMA, checks=checks,
            mapping='zero-based canonical slot -> original input slot;preserve outside neural features',
            provenance='numeric4fieldrecords only;full PolicyInput binding integration NOT exercised'))
        save('normalized-results.json', details)
        np.savez_compressed(out/'normalized-predictions.npz', row_indices=np.flatnonzero(ev).astype('<i4'),
            permutations=np.asarray(PERMUTATIONS[1:], dtype=np.int8), predictions=predictions, logits=logits,
            canonical_to_input=np.stack(maps), seeds=np.repeat(np.asarray(SEEDS, dtype='<i4'), 2),
            arm_indices=np.tile(np.arange(2, dtype=np.int8), 3))
        record('normalized-predictions.npz')
        print('[C184] 2/3 all1296648 normalized predictions collected; original C182 outputs untouched', flush=True)
        guard(); precheck(*args)
        require(graph.tensor_sha(raw) == raw_sha and graph.tensor_sha(x) == x_sha, 'Original input mutation')
        require([graph.fingerprint(m) for m in models] == fingerprints, 'Frozen weights changed')
        for f, h in protected.items(): require(audit.sha(f) == h, 'Protected input changed:'+f)
        for a in artifacts: require(audit.sha(out/a['file']) == a['sha256'], 'Output changed')
        result = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head,
            status='PASS' if gate(records, checks) else 'FAIL', diagnostic_execution_valid=True,
            C183_summary_sha256=PARENT_SHA, data_content_sha256=audit.DATA_SHA,
            source_blobs=pins, input_sha256=protected, artifacts=artifacts, replay=replay,
            records=records, normalization_checks=checks,
            normalization_rows=sum(c['rows'] for c in checks),
            normalizer_row_calls_including_idempotence=2*sum(c['rows'] for c in checks),
            inverse_row_calls=sum(c['rows'] for c in checks), replay_rows=sum(r['rows'] for r in replay),
            normalized_predictions=predictions.size, candidate_normalized_predictions=predictions[1::2].size,
            total_inference_rows=rows, inference_batches=batches, inference_cell_calls=cells, checkpoint_loads=len(models),
            new_training=0, fresh_seeds=0, teacher_calls=0, auxiliary_forward_calls=0,
            actual_acquisitions=0, proof_checker_calls=0, evidence_writes=0, network_calls=0,
            production_runtime_modified=False, gate_e_candidate=False,
            environment=dict(torch=torch.__version__, numpy=np.__version__, device='cpu', dtype='float32', threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['handwritten input normalization,NOT newly learned index invariance',
                'canonical equality to known inputs makes unchanged output expected by construction,not independent generalization',
                'same reused read-once4fact semantic problems;no larger/repeated-variable/language reasoning claim',
                'inverse numeric slot mapping retained;full provenance/PolicyInput/action mapping not integrated',
                'C182negative and C183diagnosis remain unchanged;no checkpoint or threshold repair'])
        validate_result(result); (out/'summary.json').write_bytes(blob(result))
        print('[C184] 3/3 source/output preservation checked', flush=True)
        print('=== C184 RESULT ===', flush=True); print(blob(result).decode(), flush=True)
        return result
    except Exception as exc:
        (out/'invalid.json').write_bytes(blob(dict(experiment_id=EXPERIMENT_ID, status='INVALID',
            diagnostic_execution_valid=False, error=str(exc), completed_replay=replay, completed_records=records)))
        raise


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for n in ('c183-summary', 'c182-summary', 'c181-summary', 'c180-summary', 'c179-summary',
              'c178-summary', 'c177-summary', 'c176-summary', 'c174-summary', 'output-dir'):
        p.add_argument('--'+n, type=Path, required=True)
    p.add_argument('--expected-head', required=True); run(**vars(p.parse_args()))


if __name__ == '__main__':
    main()
