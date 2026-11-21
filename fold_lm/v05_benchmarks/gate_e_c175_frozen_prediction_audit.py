"""C175: frozen C174 predictions versus a TRAIN-only syntax-blind frequency reference.

Offline development analysis, not independent holdout confirmation. No torch import,
checkpoint deserialization, model forward, optimizer, acquisition or prediction repair.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import subprocess
import time
import zipfile

import numpy as np

EXPERIMENT_ID = 'C175-v5e-frozen-prediction-frequency-reference'
STAGE = 'V5-E-FROZEN-PREDICTION-FREQUENCY-REFERENCE'
BASE = 'd011b13952abc10093d8d8d2b418ecc3d39f5fc3'
PARENT_SHA = '3e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36'
DATA_SHA = 'eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65'
SEEDS = (174001, 174002, 174003)
ARMS = ('TASK_VISIBLE', 'SYNTAX_ABLATED')
MODEL_ORDER = tuple((s, a) for s in SEEDS for a in ARMS)
ARRAYS = ('features', 'labels', 'template_ids', 'split_codes', 'groups')
PARENT_OWN = ('fold_lm/v05/structured_necessity_probe.py',
    'fold_lm/v05_benchmarks/gate_e_c174_learned_necessity.py',
    'tests_lm/test_v05_c174_learned_necessity.py', 'tools/run_c174.ps1',
    'docs/learned-necessity-probe-v0.1.md', 'docs/experiment-ledger-addendum-c174-preregistration.md')
OWN = ('fold_lm/v05_benchmarks/gate_e_c175_frozen_prediction_audit.py',
       'tests_lm/test_v05_c175_frozen_prediction_audit.py', 'tools/run_c175.ps1',
       'docs/experiment-ledger-addendum-c175-preregistration.md')
ARTIFACTS = {'necessity-plan.json', 'templates-and-splits.json', 'pilot-data.npz',
             'pilot-predictions.json', 'training-predictions.npz'} | {
                 f'probe-{s}-{a}.pt' for s, a in MODEL_ORDER}
MANIFEST_SHA = '51c7b72eb8496118185ec9ab370f068902f312b332855abc479be00a5ffc9478'


class InvalidExecution(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise InvalidExecution(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read_json(path):
    def unique(items):
        out = {}
        for key, value in items:
            require(key not in out, 'Duplicate JSON key: ' + key)
            out[key] = value
        return out
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(InvalidExecution('Nonfinite JSON')))


def safe_child(root, name):
    require(isinstance(name, str) and name and '\\' not in name and ':' not in name,
            'Unsafe relative path')
    p = PurePosixPath(name)
    require(bool(p.parts) and not p.is_absolute() and all(x not in ('.', '..') for x in p.parts)
            and str(p) == name, 'Noncanonical relative path')
    root = Path(root).resolve(); child = root.joinpath(*p.parts)
    require(child.resolve().is_relative_to(root) and not child.is_symlink(), 'Escaping path')
    return child


def git(root, *args):
    try:
        return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:
        raise InvalidExecution('Git failed: ' + ' '.join(args)) from exc


def protect_tree_files(root, pins):
    hashes = {}
    for name, wanted in pins.items():
        path = safe_child(root, name)
        require(bool(re.fullmatch('[0-9a-f]{40}', wanted)), 'Bad blob identity')
        require(git(root, 'rev-parse', 'HEAD:' + name).decode().strip() == wanted,
                'Historical source changed: ' + name)
        canonical = git(root, 'cat-file', 'blob', wanted); raw = path.read_bytes()
        require(raw == canonical or raw == canonical.replace(b'\n', b'\r\n'),
                'Uncommitted source: ' + name)
        hashes[str(path.resolve())] = hashlib.sha256(raw).hexdigest()
    return hashes


def protect_sources(root, parent):
    pins = dict(parent['source_blobs'])
    require(len(pins) == 42, 'C174 source count drift')
    for name in PARENT_OWN:
        safe_child(root, name)
        pins[name] = git(root, 'rev-parse', BASE + ':' + name).decode().strip()
    require(len(pins) == 48, 'Historical union drift')
    historical = dict(pins)
    for name in OWN:
        pins[name] = git(root, 'rev-parse', 'HEAD:' + name).decode().strip()
    return historical, protect_tree_files(root, pins)


def load_parent(path):
    require(sha(path) == PARENT_SHA, 'C174 summary hash mismatch')
    p = read_json(path)
    require(p['experiment_id'] == 'C174-v5e-learned-necessity-syntax-ablation'
            and p['commit_sha'] == BASE and p['status'] == 'PASS'
            and p['diagnostic_execution_valid'] is True, 'Wrong C174 identity')
    require(p['trained_models'] == 6 and p['pilot_predictions'] == 56376
            and p['training_resubstitution_predictions'] == 254664, 'Incomplete C174')
    return p


def protect_artifacts(parent_path, parent):
    root = Path(parent_path).resolve().parent
    items = parent['artifacts']; names = [a['file'] for a in items]
    require(len(names) == len(set(names)) == 11 and set(names) == ARTIFACTS,
            'Artifact set drift')
    hashes = {str(Path(parent_path).resolve()): PARENT_SHA}
    for item in items:
        path = safe_child(root, item['file'])
        require(path.is_file() and path.stat().st_size == item['serialized_bytes']
                and sha(path) == item['sha256'], 'Artifact hash/size mismatch: ' + item['file'])
        hashes[str(path.resolve())] = item['sha256']
    return hashes


def load_npz(path):
    with zipfile.ZipFile(path) as archive:
        require(sum(i.file_size for i in archive.infolist()) <= 32 * 1024 * 1024,
                'Oversized expanded NPZ')
        require(len(archive.namelist()) == len(set(archive.namelist())), 'Duplicate NPZ member')
    with np.load(path, allow_pickle=False) as arrays:
        return {k: arrays[k].copy() for k in arrays.files}


def load_data(root, parent):
    d = load_npz(root / 'pilot-data.npz'); metadata = read_json(root / 'templates-and-splits.json')
    require(set(d) == set(ARRAYS) and len(metadata) == 640, 'Data fields drift')
    for name, shape, dtype in [('features', (51840,72), '<i4'), ('labels', (51840,), '<i8'),
                               ('template_ids', (51840,), '<i4'), ('split_codes', (51840,), '|u1'),
                               ('groups', (51840,), '<i4')]:
        require(d[name].shape == shape and d[name].dtype.str == dtype, 'Array schema: ' + name)
    h = hashlib.sha256(blob(metadata))
    for name in ARRAYS:
        h.update(d[name].tobytes())
    require(h.hexdigest() == DATA_SHA == parent['data_content_sha256'], 'Canonical data drift')
    x, y, ids, split, groups = (d[k] for k in ARRAYS)
    require(set(y.tolist()) == {0,1} and set(split.tolist()) == {0,1}, 'Bad labels/splits')
    require(np.array_equal(ids, np.repeat(np.arange(640),81)), 'Row ordering drift')
    group_names = sorted({m['group'] for m in metadata})
    require(len(group_names) == 40, 'Group metadata drift')
    require(np.array_equal(groups, [group_names.index(metadata[i]['group']) for i in ids]),
            'Group array mismatch')
    require(np.array_equal(split, [int(metadata[i]['split'] == 'PILOT_EVAL') for i in ids]),
            'Split array mismatch')
    for code, n, n0, ng, nt in [(0,42444,27816,36,524),(1,9396,6744,4,116)]:
        mask = split == code
        require(int(mask.sum()) == n and int((y[mask] == 0).sum()) == n0
                and len(set(groups[mask])) == ng and len(set(ids[mask])) == nt, 'Data profile drift')
    require(not set(groups[split == 0]) & set(groups[split == 1]), 'Group leakage')
    return d, metadata


def basic_metrics(y, p):
    y, p = np.asarray(y), np.asarray(p)
    require(y.ndim == p.ndim == 1 and len(y) == len(p)
            and y.dtype.kind in 'iu' and p.dtype.kind in 'iu'
            and set(y.tolist()) <= {0,1} and set(p.tolist()) <= {0,1}, 'Bad metric inputs')
    c = [[int(((y == a) & (p == b)).sum()) for b in (0,1)] for a in (0,1)]
    recalls = [c[i][i]/sum(c[i]) if sum(c[i]) else None for i in (0,1)]
    return dict(n=len(y), confusion=c, sufficient_recall=recalls[0], needs_recall=recalls[1],
                balanced_accuracy=None if None in recalls else sum(recalls)/2,
                accuracy=float((y == p).mean()) if len(y) else None)


def metrics(y, p, groups):
    y, p, groups = (np.asarray(a) for a in (y,p,groups))
    require(groups.shape == y.shape, 'Bad group shape')
    out = basic_metrics(y,p)
    per = {str(g):basic_metrics(y[groups == g],p[groups == g]) for g in sorted(set(groups.tolist()))}
    require(per and all(v['balanced_accuracy'] is not None for v in per.values()),
            'Primary groups need both classes')
    out.update(per_group=per, macro_group_balanced_accuracy=float(np.mean(
        [v['balanced_accuracy'] for v in per.values()])))
    return out


def same_metrics(actual, recorded):
    for k,v in recorded.items():
        if k in ('seed','arm'):
            continue
        require(k in actual, 'Missing replay metric: ' + k)
        if isinstance(v, dict):
            same_metrics(actual[k], v)
        elif isinstance(v, float):
            require(math.isfinite(v) and math.isclose(actual[k],v,rel_tol=0,abs_tol=1e-12),
                    'Metric replay drift: ' + k)
        else:
            require(actual[k] == v, 'Metric replay drift: ' + k)


def load_predictions(root, parent, d):
    train = np.flatnonzero(d['split_codes'] == 0); test = np.flatnonzero(d['split_codes'] == 1)
    saved = load_npz(root / 'training-predictions.npz')
    require(set(saved) == {'row_indices','predictions'} and np.array_equal(saved['row_indices'],train),
            'Training row identities drift')
    tp = saved['predictions']
    require(tp.shape == (6,42444) and tp.dtype.kind in 'iu' and set(np.unique(tp)) <= {0,1},
            'Training prediction schema')
    pilot = read_json(root / 'pilot-predictions.json'); require(len(pilot) == 6, 'Pilot model count')
    allp = np.full((6,51840), -1, dtype=np.int8)
    allp[:,train] = tp
    for i,(row,(seed,arm)) in enumerate(zip(pilot,MODEL_ORDER,strict=True)):
        require((row['seed'],row['arm']) == (seed,arm) and np.array_equal(row['row_indices'],test),
                'Pilot row/model identities drift')
        pred = np.asarray(row['predictions']); logits = np.asarray(row['logits'])
        require(pred.shape == (9396,) and pred.dtype.kind in 'iu' and set(pred.tolist()) <= {0,1}
                and logits.shape == (9396,2) and np.isfinite(logits).all()
                and np.array_equal(pred,logits.argmax(1)), 'Raw prediction/logit mismatch')
        allp[i,test] = pred
        same_metrics(metrics(d['labels'][test],pred,d['groups'][test]),
                     parent['pairs'][i//2]['full' if i%2 == 0 else 'ablated'])
        recorded = parent['training_metrics'][i]
        require((recorded['seed'], recorded['arm']) == (seed,arm), 'Train metric identity')
        same_metrics(metrics(d['labels'][train],allp[i,train],d['groups'][train]),recorded)
    y,g = d['labels'][test],d['groups'][test]
    baseline = (d['features'][test,48:62:4] == 0).any(axis=1).astype(np.int64)
    for name,p in [('missing_fact_rule',baseline),('always_sufficient',np.zeros_like(y)),
                   ('always_needs_observation',np.ones_like(y))]:
        same_metrics(metrics(y,p,g),parent['baselines'][name])
    require(np.all(allp >= 0), 'Missing stored predictions')
    return allp


def blind_keys(features):
    x = np.asarray(features)
    require(x.ndim == 2 and x.shape[1] == 72 and x.dtype.kind in 'iu', 'Bad feature schema')
    # Same information left by C174 ablation, before its fixed positive scaling.
    z = np.concatenate((x[:,:4], x[:,46:]),axis=1)
    return [tuple(int(v) for v in row) for row in z]


def build_reference(x_train, y_train):
    keys = blind_keys(x_train); y = np.asarray(y_train)
    require(y.ndim == 1 and len(y) == len(keys) and y.dtype.kind in 'iu'
            and set(y.tolist()) <= {0,1} and len(y), 'Bad TRAIN reference input')
    counts = {}
    for k,v in zip(keys,y,strict=True):
        c = counts.setdefault(k,[0,0]); c[int(v)] += 1
    # TRAIN row-unweighted majority, ties class0. No eval labels/groups or fitted threshold.
    table = {k:int(c[1] > c[0]) for k,c in counts.items()}
    return table, counts


def reference_predictions(table, features):
    keys = blind_keys(features)
    require(all(k in table for k in keys), 'Unseen blind key; no fallback')
    return np.asarray([table[k] for k in keys],dtype=np.int8)


def matched_pairs(keys, labels, prediction):
    counts = {}
    for k,y,p in zip(keys,labels,prediction,strict=True):
        row = counts.setdefault(k,[0,0,0,0]); row[int(y)] += 1
        if y == p:
            row[2+int(y)] += 1
    pairs = sum(c[0]*c[1] for c in counts.values())
    both = sum(c[2]*c[3] for c in counts.values())
    return dict(cross_label_pairs=pairs, both_correct_pairs=both,
                both_correct_rate=both/pairs if pairs else None,
                mixed_blind_keys=sum(c[0]>0 and c[1]>0 for c in counts.values()),
                interpretation='pairs share visible facts/resources; not independent samples or one-edit interventions')


def gate(rows, reference):
    if [r.get('seed') for r in rows] != list(SEEDS):
        return False
    return all(r['full']['macro_group_balanced_accuracy'] > reference['macro_group_balanced_accuracy']
               and r['full']['sufficient_recall'] > 0.5 and r['full']['needs_recall'] > 0.5
               for r in rows)


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,parent_sha256=PARENT_SHA,data_sha256=DATA_SHA,
                question='Does each frozen syntax-visible model exceed a TRAIN-only conditional-majority reference?',
                changed_variable='comparator; candidate predictions and data fixed',
                reference='group by raw fields0..3 and46..71; TRAIN rows only; unweighted majority; tie0; unseen invalid',
                main_metric='macro-group balanced accuracy over all4 existing PILOT_EVAL groups',
                decision='each seed full strictly exceeds reference and both aggregate class recalls>0.5',
                seeds=SEEDS,arms=ARMS,train_rows=42444,pilot_rows=9396,blind_keys=81,
                stored_model_predictions=311040,reference_predictions=51840,
                secondary=['group confusion','missing-count0..4 confusion','matched-visible cross-label pair discrimination'],
                new_training=0,new_model_forwards=0,new_seeds=0,checkpoint_loads=0,actual_acquisitions=0,
                scope='post-C174 development analysis on reused splits, not independent confirmation or Gate E')


def run(*, c174_summary, output_dir, expected_head):
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(git(root,'rev-parse','HEAD').decode().strip() == expected_head, 'HEAD mismatch')
        require(git(root,'branch','--show-current').decode().strip() == 'feat/sft-target-loss', 'Branch mismatch')
        require(not git(root,'status','--porcelain','--untracked-files=no').strip(), 'Tracked tree dirty')
    guard(); parent = load_parent(c174_summary)
    pins, protected = protect_sources(root,parent)
    protected.update(protect_artifacts(c174_summary,parent))
    require(hashlib.sha256(blob(manifest())).hexdigest() == MANIFEST_SHA,'Manifest drift')
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False); started = time.perf_counter()
    (out/'audit-plan.json').write_bytes(blob(dict(manifest(),source_blobs=pins)))
    try:
        print('[C175] plan fixed; frozen predictions; no training/model forward',flush=True)
        source = Path(c174_summary).resolve().parent
        data, _ = load_data(source,parent)
        prediction = load_predictions(source,parent,data)
        print('[C175] 1/3 all 311040 saved predictions and C174 metrics verified',flush=True)
        x,y,split,g = (data[k] for k in ('features','labels','split_codes','groups'))
        tr = split == 0; ev = ~tr
        table,counts = build_reference(x[tr],y[tr])
        require(len(table) == 81 and all(sum(c) == 524 for c in counts.values()), 'TRAIN key coverage drift')
        ref = reference_predictions(table,x)
        refscore = metrics(y[ev],ref[ev],g[ev]); rows = []; detail = []
        keys = blind_keys(x); missing = (x[:,48:62:4] == 0).sum(axis=1)
        for i,(seed,arm) in enumerate(MODEL_ORDER):
            p = prediction[i]
            record = dict(seed=seed,arm=arm,parts={})
            for name,mask in [('TRAIN_RESUBSTITUTION',tr),('PILOT_EVAL',ev)]:
                ids = np.flatnonzero(mask)
                record['parts'][name] = dict(metrics=metrics(y[mask],p[mask],g[mask]),
                    by_missing_count={str(n):basic_metrics(y[mask & (missing==n)],p[mask & (missing==n)]) for n in range(5)},
                    matched_visible=matched_pairs([keys[j] for j in ids],y[mask],p[mask]))
            detail.append(record)
        for j,seed in enumerate(SEEDS):
            full = detail[2*j]['parts']['PILOT_EVAL']['metrics']
            blind = detail[2*j+1]['parts']['PILOT_EVAL']['metrics']
            rows.append(dict(seed=seed,full=full,ablated=blind,
                full_minus_reference=full['macro_group_balanced_accuracy']-refscore['macro_group_balanced_accuracy']))
        print('[C175] 2/3 TRAIN-only frequency reference and error strata collected',flush=True)
        reference_detail = dict(pilot=refscore,training=metrics(y[tr],ref[tr],g[tr]),
            table=[dict(key=list(k),counts=counts[k],prediction=table[k]) for k in sorted(table)],
            objective='TRAIN empirical ordinary accuracy; not claimed optimal for held-out group-macro BA')
        (out/'audit-details.json').write_bytes(blob(dict(models=detail,reference=reference_detail)))
        guard(); protect_sources(root,parent)
        for path,wanted in protected.items():
            require(sha(path) == wanted, 'Protected input changed: ' + path)
        artifacts = [dict(file=n,sha256=sha(out/n),serialized_bytes=(out/n).stat().st_size)
                     for n in ('audit-plan.json','audit-details.json')]
        result = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status='PASS' if gate(rows,refscore) else 'FAIL',diagnostic_execution_valid=True,
            C174_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
            replayed_model_predictions=int(prediction.size),reference_predictions=len(ref),blind_keys=len(table),
            reference=refscore,pairs=rows,
            reference_training={k:v for k,v in reference_detail['training'].items() if k != 'per_group'},
            secondary=[dict(seed=r['seed'],arm=r['arm'],parts={n:{k:v for k,v in part.items()
                if k != 'metrics'} for n,part in r['parts'].items()}) for r in detail],
            new_training_steps=0,new_model_forwards=0,fresh_seeds=0,
            checkpoint_deserializations=0,actual_acquisitions=0,evidence_writes=0,network_calls=0,
            production_runtime_modified=False,gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['development reference added after seeing C174 summary; no independent holdout',
                'same4 pilot groups and same frozen weights/predictions; no claim of improved model',
                'reference uses TRAIN labels only and optimizes row-weighted TRAIN majority, not pilot macro BA',
                'matched-visible pairs are correlated secondary observations, not one-edit causal interventions'])
        (out/'summary.json').write_bytes(blob(result))
        print('[C175] 3/3 source/output preservation checked',flush=True)
        print('=== C175 RESULT ===',flush=True); print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/'invalid.json').write_bytes(blob(dict(experiment_id=EXPERIMENT_ID,status='INVALID',
            diagnostic_execution_valid=False,error=str(exc))))
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--c174-summary',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--expected-head',required=True)
    run(**vars(parser.parse_args()))


if __name__ == '__main__':
    main()
