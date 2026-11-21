"""C177: frozen score ordering after C176's accepted negative.

No torch, training, model forward, calibration, threshold selection or prediction repair.
AUC comparisons reuse the existing development pilot; they cannot reverse C176's verdict.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import time

import numpy as np

EXPERIMENT_ID = 'C177-v5e-frozen-score-order-audit'
STAGE = 'V5-E-FROZEN-SCORE-ORDER-AUDIT'
BASE = '6155242c6564858293d355c51ae2a3dbc7f25bdb'
PARENT_SHA = 'b5f48626e266a65326da41c965a48cc0824926ce636f9f6571e3962b0a0e6a5b'
SEEDS = (176001, 176002, 176003)
ARMS = ('UNIFORM_CE', 'CONDITIONAL_CE')
PARENT_OWN = ('fold_lm/v05_benchmarks/gate_e_c176_conditional_loss.py',
    'tests_lm/test_v05_c176_conditional_loss.py', 'tools/run_c176.ps1',
    'docs/experiment-ledger-addendum-c176-preregistration.md')
OWN = ('fold_lm/v05_benchmarks/gate_e_c177_frozen_score_order.py',
    'tests_lm/test_v05_c177_frozen_score_order.py', 'tools/run_c177.ps1',
    'docs/experiment-ledger-addendum-c177-preregistration.md')
MANIFEST_SHA = '942735a9f843485eaf7b2b3b5f15cab774e749f7e52d37adcb64dcd8dcb5572e'


class InvalidExecution(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise InvalidExecution(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def binary_labels(y):
    y = np.asarray(y)
    require(y.ndim == 1 and y.dtype.kind in 'iu' and set(np.unique(y)) <= {0, 1},
            'One-dimensional integer binary labels required')
    return y


def rank_pairs(labels, scores):
    """NEEDS=1 must rank above SUFFICIENT=0. Ties get exactly half credit.

    Count all opposite-label pairs without constructing the Cartesian product.
    Labels are evaluation data only. This function neither fits nor changes predictions.
    """
    y = binary_labels(labels); s = np.asarray(scores)
    require(s.shape == y.shape and s.dtype.kind in 'fiu' and np.isfinite(s).all(),
            'Aligned finite numeric scores required')
    n0, n1 = int((y == 0).sum()), int((y == 1).sum())
    if not n0 or not n1:
        return dict(n=len(y), n0=n0, n1=n1, pairs=0, wins=0, ties=0, losses=0, auc=None)
    _, ids = np.unique(s, return_inverse=True)
    z = np.bincount(ids[y == 0], minlength=int(ids.max()) + 1).astype(np.int64)
    o = np.bincount(ids[y == 1], minlength=len(z)).astype(np.int64)
    wins = int(np.sum(o * (np.cumsum(z) - z))); ties = int(np.sum(o * z))
    total = n0 * n1
    return dict(n=len(y), n0=n0, n1=n1, pairs=total, wins=wins, ties=ties,
                losses=total - wins - ties, auc=(2 * wins + ties) / (2 * total))


def grouped_rank_pairs(keys, labels, scores):
    y = binary_labels(labels); s = np.asarray(scores)
    require(len(keys) == len(y) and s.shape == y.shape, 'Misaligned grouped scores')
    rank_pairs(y, s)  # Validate even a pure-label collection.
    buckets = {}
    for i, key in enumerate(keys):
        buckets.setdefault(key, []).append(i)
    rows = [rank_pairs(y[ids], s[ids]) for ids in buckets.values()]
    out = {k: sum(r[k] for r in rows) for k in ('n', 'n0', 'n1', 'pairs', 'wins', 'ties', 'losses')}
    out['auc'] = (2 * out['wins'] + out['ties']) / (2 * out['pairs']) if out['pairs'] else None
    out['keys'] = len(buckets); out['mixed_keys'] = sum(r['pairs'] > 0 for r in rows)
    return out


def primary(strata):
    """Exact mean over preregistered missing-count strata1,2,3; no silent omission."""
    terms = []
    for k in ('1', '2', '3'):
        r = strata[k]
        require(r['pairs'] > 0, 'Primary stratum lacks both labels')
        terms.append(Fraction(2 * r['wins'] + r['ties'], 2 * r['pairs']))
    q = sum(terms, Fraction()) / 3
    return dict(numerator=q.numerator, denominator=q.denominator, auc=float(q))


def gate(pairs):
    if [p.get('seed') for p in pairs] != list(SEEDS):
        return False
    for p in pairs:
        try:
            u, c = p['uniform']['primary'], p['conditional']['primary']
            a, b = Fraction(c['numerator'], c['denominator']), Fraction(u['numerator'], u['denominator'])
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            return False
        if not (0 <= b < a <= 1):
            return False
    return True


def raw_margins(logits, predictions):
    z = np.asarray(logits); p = binary_labels(predictions)
    require(z.shape == (len(p), 2) and z.dtype.kind in 'fiu' and np.isfinite(z).all(),
            'Finite two-column logits required')
    require(np.array_equal(p, z.argmax(axis=1)), 'Stored prediction is not raw argmax')
    # Float64 subtraction of stored float32 values, with no rescaling or threshold fitting.
    z = z.astype(np.float64)
    return z[:, 1] - z[:, 0]


def transitions(labels, uniform, conditional):
    y, u, c = (binary_labels(a) for a in (labels, uniform, conditional))
    require(y.shape == u.shape == c.shape, 'Misaligned paired predictions')
    uc, cc = u == y, c == y
    return dict(n=len(y), both_correct=int((uc & cc).sum()),
        both_wrong=int((~uc & ~cc).sum()), rescued=int((~uc & cc).sum()),
        regressed=int((uc & ~cc).sum()), to_needs=int(((u == 0) & (c == 1)).sum()),
        to_sufficient=int(((u == 1) & (c == 0)).sum()))


def missing_counts(raw):
    x = np.asarray(raw)
    require(x.ndim == 2 and x.shape[1] == 72 and x.dtype.kind in 'iu', 'Integer72 fields required')
    present = x[:, 48:62:4]
    require(set(np.unique(present)) <= {0, 1}, 'Presence must be binary')
    return (present == 0).sum(axis=1)


def score_replay(data, p, mask, audit):
    y, g = data['labels'][mask], data['groups'][mask]
    m = missing_counts(data['features'][mask])
    strata = {str(k): audit.basic_metrics(y[m == k], p[m == k]) for k in range(5)}
    return dict(metrics=audit.metrics(y, p, g), by_missing_count=strata,
        macro_missing_balanced_accuracy=sum(strata[str(k)]['balanced_accuracy'] for k in (1, 2, 3)) / 3)


def c176_gate(pairs):
    """Recheck the original, unchanged C176 gate; a negative parent is required."""
    require([p['seed'] for p in pairs] == list(SEEDS), 'Parent pair identities changed')
    for p in pairs:
        require(p['paired_initial_equal'] is True and p['paired_batches_equal'] is True,
                'Parent training was not paired')
    return all(p['conditional']['macro_missing_balanced_accuracy'] > p['uniform']['macro_missing_balanced_accuracy']
        and p['conditional']['metrics']['macro_group_balanced_accuracy'] >= p['uniform']['metrics']['macro_group_balanced_accuracy']
        and p['conditional']['by_missing_count']['1']['needs_recall'] > p['uniform']['by_missing_count']['1']['needs_recall']
        and p['conditional']['by_missing_count']['3']['sufficient_recall'] > p['uniform']['by_missing_count']['3']['sufficient_recall']
        and p['conditional']['metrics']['needs_recall'] > .5
        and p['conditional']['metrics']['sufficient_recall'] > .5 for p in pairs)


def precheck(c176_summary, c174_summary, root):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(audit.sha(c176_summary) == PARENT_SHA, 'C176 summary hash mismatch')
    p = audit.read_json(c176_summary)
    require(p['experiment_id'] == 'C176-v5e-missing-count-conditional-loss'
        and p['commit_sha'] == BASE and p['status'] == 'FAIL'
        and p['diagnostic_execution_valid'] is True and not c176_gate(p['pairs']), 'Wrong C176 negative')
    require(p['trained_models'] == 6 and p['training_steps_total'] == 12000
        and p['pilot_predictions'] == 56376 and p['training_resubstitution_predictions'] == 254664
        and len(p['source_blobs']) == 52, 'Incomplete parent')
    p174 = audit.load_parent(c174_summary)
    require(p['C174_summary_sha256'] == audit.PARENT_SHA and p['data_content_sha256'] == audit.DATA_SHA,
            'Data/lineage drift')
    protected = audit.protect_artifacts(c174_summary, p174)
    protected[str(Path(c176_summary).resolve())] = PARENT_SHA
    expected = {'conditional-plan.json', 'train-weight-table.json', 'pilot-predictions.json', 'training-predictions.npz'}
    expected |= {f'probe-{s}-{a}.pt' for s in SEEDS for a in ARMS}
    require(len(p['artifacts']) == 10 and {a['file'] for a in p['artifacts']} == expected, 'Parent artifact set')
    for a in p['artifacts']:
        f = audit.safe_child(Path(c176_summary).resolve().parent, a['file'])
        require(f.is_file() and f.stat().st_size == a['serialized_bytes'] and audit.sha(f) == a['sha256'],
                'Parent artifact changed: ' + a['file'])
        protected[str(f.resolve())] = a['sha256']
    pins = dict(p['source_blobs'])
    for n in PARENT_OWN:
        pins[n] = audit.git(root, 'rev-parse', BASE + ':' + n).decode().strip()
    require(len(pins) == 56, 'Historical union drift')
    all_pins = dict(pins)
    for n in OWN:
        all_pins[n] = audit.git(root, 'rev-parse', 'HEAD:' + n).decode().strip()
    protected.update(audit.protect_tree_files(root, all_pins))
    require(len(protected) == 83, 'Protected input count drift')
    require(hashlib.sha256(blob(manifest())).hexdigest() == MANIFEST_SHA, 'Manifest drift')
    return p, p174, pins, protected


def load_predictions(root, parent, data, audit):
    train = np.flatnonzero(data['split_codes'] == 0); pilot = np.flatnonzero(data['split_codes'] == 1)
    t = audit.load_npz(root / 'training-predictions.npz')
    require(set(t) == {'row_indices', 'predictions'} and np.array_equal(t['row_indices'], train)
        and t['predictions'].shape == (6, 42444), 'TRAIN saved row profile')
    saved = audit.read_json(root / 'pilot-predictions.json')
    require(len(saved) == 6, 'Missing pilot model')
    allp = np.empty((6, 51840), dtype=np.int8); margins = []
    order = [(s, a) for s in SEEDS for a in ARMS]
    require([(r['seed'], r['arm']) for r in parent['training_metrics']] == order, 'TRAIN score order')
    for i, (r, identity) in enumerate(zip(saved, order, strict=True)):
        require((r['seed'], r['arm']) == identity and np.array_equal(r['row_indices'], pilot), 'PILOT row/model order')
        p, tp = binary_labels(r['predictions']), binary_labels(t['predictions'][i])
        require(p.shape == (9396,) and tp.shape == (42444,), 'Prediction coverage')
        margins.append(raw_margins(r['logits'], p))
        allp[i, train] = tp; allp[i, pilot] = p
        audit.same_metrics(score_replay(data, p, data['split_codes'] == 1, audit),
                           parent['pairs'][i // 2]['uniform' if i % 2 == 0 else 'conditional'])
        audit.same_metrics(score_replay(data, tp, data['split_codes'] == 0, audit), parent['training_metrics'][i])
    return allp, np.stack(margins)


def ordering(labels, scores, groups, missing, keys):
    y = binary_labels(labels); g, m = np.asarray(groups), np.asarray(missing)
    require(g.shape == m.shape == y.shape, 'Ordering arrays misaligned')
    strata = {str(k): rank_pairs(y[m == k], scores[m == k]) for k in range(5)}
    return dict(primary=primary(strata), by_missing_count=strata,
        per_group={str(k): rank_pairs(y[g == k], scores[g == k]) for k in sorted(set(g.tolist()))},
        overall=rank_pairs(y, scores), matched_visible=grouped_rank_pairs(keys, y, scores))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, parent_sha256=PARENT_SHA,
        data_sha256='eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65',
        seeds=SEEDS, arms=ARMS, stored_predictions=311040, pilot_score_rows=56376,
        aligned_prediction_pairs=155520, train_rows=42444, pilot_rows=9396,
        score='float64(saved logit1)-float64(saved logit0);no modification',
        primary='equal mean ROC pair-order AUC within missing counts1,2,3;tie half;exact fractions',
        gate='each seed conditional primary strictly exceeds paired uniform;ties fail',
        secondary=['AUC by all four pilot groups', 'overall AUC', 'same-blind-key pair ordering',
                   'TRAIN and PILOT rescue/regression counts by group and missing count'],
        new_training=0, model_forwards=0, checkpoint_loads=0, fresh_seeds=0,
        threshold_searches=0, inference_corrections=0, actual_acquisitions=0,
        training_auc='unavailable because TRAIN logits were not saved;no new forward',
        scope='post-C176 reused development data;narrow ranking diagnostic;C176 remains negative')


def regression_modules(root):
    text = (Path(root) / 'tools/run_c167.ps1').read_text(encoding='utf-8')
    names = re.findall(r'^\s*"(tests_lm\.[a-zA-Z0-9_]+)"\s*$', text, re.M)
    require(len(names) == len(set(names)) == 51, 'Historical regression list drift')
    return names + ['tests_lm.' + n for n in ('test_v05_c168_necessity_observability',
        'test_v05_c169_interface_batch', 'test_v05_c170_structured_task_input', 'test_v05_c171_derived_result',
        'test_v05_c172_action_runtime', 'test_v05_c173_acquisition_lifecycle', 'test_v05_c174_learned_necessity',
        'test_v05_c175_frozen_prediction_audit', 'test_v05_c176_conditional_loss', 'test_v05_c177_frozen_score_order')]


def run(*, c176_summary, c174_summary, output_dir, expected_head):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root, 'rev-parse', 'HEAD').decode().strip() == expected_head, 'HEAD mismatch')
        require(audit.git(root, 'branch', '--show-current').decode().strip() == 'feat/sft-target-loss', 'Branch mismatch')
        require(not audit.git(root, 'status', '--porcelain', '--untracked-files=no').strip(), 'Tracked tree dirty')
    guard(); parent, p174, pins, protected = precheck(c176_summary, c174_summary, root)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False); started = time.perf_counter()
    (out / 'score-order-plan.json').write_bytes(blob(dict(manifest(), source_blobs=pins)))
    try:
        print('[C177] plan fixed; frozen logits; no training or threshold adjustment', flush=True)
        data, _ = audit.load_data(Path(c174_summary).resolve().parent, p174)
        prediction, margins = load_predictions(Path(c176_summary).resolve().parent, parent, data, audit)
        print('[C177] 1/3 all 311040 decisions and C176 score tables verified', flush=True)
        y, g, split = data['labels'], data['groups'], data['split_codes']
        m = missing_counts(data['features']); ev = split == 1
        keys = audit.blind_keys(data['features'][ev]); pairs = []; changes = []
        for i, seed in enumerate(SEEDS):
            rows = [ordering(y[ev], margins[2*i+j], g[ev], m[ev], keys) for j in (0, 1)]
            pairs.append(dict(seed=seed, uniform=rows[0], conditional=rows[1],
                delta=rows[1]['primary']['auc'] - rows[0]['primary']['auc']))
            u, c = prediction[2*i], prediction[2*i+1]; parts = {}
            for code, name in ((0, 'TRAIN_RESUBSTITUTION'), (1, 'PILOT_EVAL')):
                mask = split == code
                parts[name] = dict(overall=transitions(y[mask], u[mask], c[mask]),
                    by_missing_count={str(k): transitions(y[mask & (m == k)], u[mask & (m == k)], c[mask & (m == k)]) for k in range(5)},
                    per_group={str(k): transitions(y[mask & (g == k)], u[mask & (g == k)], c[mask & (g == k)]) for k in sorted(set(g[mask].tolist()))})
            changes.append(dict(seed=seed, parts=parts))
            print(f"[C177] seed={seed} mixed_count_AUC uniform={rows[0]['primary']['auc']:.6f} conditional={rows[1]['primary']['auc']:.6f}", flush=True)
        print('[C177] 2/3 ordering and error exchanges collected; no candidate changed', flush=True)
        (out / 'score-order-details.json').write_bytes(blob(dict(pairs=pairs, error_exchanges=changes)))
        guard(); precheck(c176_summary, c174_summary, root)
        for name, wanted in protected.items():
            require(audit.sha(name) == wanted, 'Protected input changed: ' + name)
        artifacts = [dict(file=n, sha256=audit.sha(out/n), serialized_bytes=(out/n).stat().st_size)
                     for n in ('score-order-plan.json', 'score-order-details.json')]
        result = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head,
            status='PASS' if gate(pairs) else 'FAIL', diagnostic_execution_valid=True,
            C176_summary_sha256=PARENT_SHA, C174_summary_sha256=audit.PARENT_SHA,
            source_blobs=pins, input_sha256=protected, artifacts=artifacts,
            replayed_model_predictions=311040, pilot_score_rows=56376, aligned_prediction_pairs=155520,
            pairs=pairs, error_exchange_summary=[dict(seed=r['seed'], parts={n: {k:v for k,v in p.items() if k != 'per_group'} for n,p in r['parts'].items()}) for r in changes],
            new_training_steps=0, model_forwards=0, checkpoint_deserializations=0, fresh_seeds=0,
            threshold_searches=0, inference_corrections=0, actual_acquisitions=0, evidence_writes=0,
            network_calls=0, production_runtime_modified=False, gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['C176 remains ACCEPTED VALID NEGATIVE even if this diagnostic passes',
                'same four reused development groups;not independent confirmation',
                'AUC is ordering,not calibration or usable accuracy;no threshold is selected',
                'TRAIN AUC unavailable because logits were not saved;no new model forward',
                'cross-label pairs share data and are not independent experimental samples',
                'positive ranking result rules out only a pure per-stratum constant-offset account of these scores,not all alternative mechanisms'])
        (out/'summary.json').write_bytes(blob(result))
        print('[C177] 3/3 source/output preservation checked', flush=True)
        print('=== C177 RESULT ===', flush=True); print(blob(result).decode(), flush=True)
        return result
    except Exception as exc:
        (out/'invalid.json').write_bytes(blob(dict(experiment_id=EXPERIMENT_ID, status='INVALID', diagnostic_execution_valid=False, error=str(exc))))
        raise


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--c176-summary', type=Path, required=True); p.add_argument('--c174-summary', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True); p.add_argument('--expected-head', required=True)
    run(**vars(p.parse_args()))


if __name__ == '__main__':
    main()
