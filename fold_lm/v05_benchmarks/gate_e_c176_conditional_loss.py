"""C176 development intervention: paired TRAIN missing-count-conditional loss.

Same diagnostic MLP and row schedule in both arms. No inference-time weights,
rule repair, tool actions or claim of independent pilot holdout confirmation.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import time

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

EXPERIMENT_ID = 'C176-v5e-missing-count-conditional-loss'
STAGE = 'V5-E-MISSING-COUNT-CONDITIONAL-LOSS'
BASE = 'd54a4921a4e90ea58d72cd66988f946e67c1031d'
PARENT_SHA = 'd4bcdd76fd99dc3f5730132b8526819de486f11181f732310710b8065d43a722'
SEEDS = (176001, 176002, 176003)
ARMS = ('UNIFORM_CE', 'CONDITIONAL_CE')
STEPS, BATCH, LR = 2000, 256, 0.001
COUNTS = ((8384, 0), (12416, 4352), (6048, 6528), (968, 3224), (0, 524))
OWN = ('fold_lm/v05_benchmarks/gate_e_c176_conditional_loss.py',
       'tests_lm/test_v05_c176_conditional_loss.py', 'tools/run_c176.ps1',
       'docs/experiment-ledger-addendum-c176-preregistration.md')
MANIFEST_SHA = '09ce8d00f2f6d09fda96f93e51aed6c34fd5b4e74eba77d51848c8e1f8dbafa8'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


def fingerprint(model):
    h = hashlib.sha256()
    for name, tensor in sorted(model.state_dict().items()):
        h.update(name.encode()); h.update(str(tuple(tensor.shape)).encode())
        h.update(tensor.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def missing_counts(raw):
    x = np.asarray(raw)
    require(x.ndim == 2 and x.shape[1] == 72 and x.dtype.kind in 'iu', 'Integer72 feature matrix required')
    present = x[:,48:62:4]
    require(set(np.unique(present).tolist()) <= {0,1}, 'Nonbinary presence mask')
    return (present == 0).sum(axis=1).astype(np.int64)


def conditional_weights(y_train, missing_train):
    """Only TRAIN labels determine weights; retain the mass of each missing stratum."""
    y, m = np.asarray(y_train), np.asarray(missing_train)
    require(y.ndim == m.ndim == 1 and len(y) == len(m) and len(y) > 0,
            'Aligned nonempty training labels/counts required')
    require(y.dtype.kind in 'iu' and m.dtype.kind in 'iu' and set(y.tolist()) <= {0,1}
            and set(m.tolist()) <= set(range(5)), 'Bad training labels/counts')
    out = np.ones(len(y), dtype=np.float64); rows = []
    for k in range(5):
        counts = [int(((m == k) & (y == c)).sum()) for c in (0,1)]
        factors = [sum(counts)/(2*n) for n in counts] if min(counts) > 0 else [1.0,1.0]
        for c in (0,1):
            out[(m == k) & (y == c)] = factors[c]
        rows.append(dict(missing=k, counts=counts, weights=factors))
        require(np.isclose(out[m == k].sum(), sum(counts), rtol=0, atol=1e-8), 'Stratum mass changed')
    return out, rows


def weighted_loss(logits, labels, weights):
    require(logits.ndim == 2 and logits.shape[1] == 2 and logits.dtype == torch.float32,
            'Two float32 logits required')
    require(labels.shape == weights.shape == (len(logits),) and len(logits) > 0
            and labels.dtype == torch.int64 and weights.dtype == torch.float32,
            'Aligned typed labels/weights required')
    require(torch.isfinite(logits).all().item() and torch.isfinite(weights).all().item()
            and (weights > 0).all().item() and ((labels == 0) | (labels == 1)).all().item(),
            'Finite positive weights and binary labels required')
    per_row = F.cross_entropy(logits, labels, reduction='none')
    # Divide by batch LENGTH, not sampled weight sum. Population stratum mass is preserved.
    return (per_row * weights).mean(), per_row.mean()


def fit(initial, x_train, y_train, row_weights, seed, *, steps=STEPS, batch_size=BATCH, progress=None):
    """Both arms use this same loop; only the fixed TRAIN row_weights differ."""
    require(isinstance(initial, nn.Module) and type(seed) is int and 0 <= seed < 2**31,
            'Module and nonnegative integer seed required')
    require(type(steps) is int and steps > 0 and type(batch_size) is int and batch_size > 0,
            'Positive fixed workload required')
    require(x_train.ndim == 2 and len(x_train) > 1 and x_train.dtype == torch.float32
            and x_train.device.type == 'cpu' and torch.isfinite(x_train).all().item(), 'Bad TRAIN features')
    require(y_train.shape == row_weights.shape == (len(x_train),) and y_train.dtype == torch.int64
            and row_weights.dtype == torch.float32 and y_train.device.type == row_weights.device.type == 'cpu'
            and set(y_train.tolist()) == {0,1} and torch.isfinite(row_weights).all().item()
            and (row_weights > 0).all().item(), 'Bad TRAIN labels/weights')
    model = deepcopy(initial).cpu().train()
    optim = torch.optim.Adam(model.parameters(), lr=LR, betas=(.9,.999), eps=1e-8,
                             weight_decay=0, amsgrad=False, foreach=False)
    rng = torch.Generator(device='cpu').manual_seed(seed+1000000)
    schedule = hashlib.sha256(); history = []
    for step in range(steps):
        ids = torch.randint(len(x_train), (batch_size,), generator=rng)
        schedule.update(ids.numpy().tobytes()); optim.zero_grad(set_to_none=True)
        loss, ordinary = weighted_loss(model(x_train[ids]), y_train[ids], row_weights[ids])
        loss.backward()
        require(all(p.grad is not None and torch.isfinite(p.grad).all().item() for p in model.parameters()),
                'Nonfinite or absent gradient; no retuning')
        optim.step()
        if (step+1) % 500 == 0 or step+1 == steps:
            row = dict(step=step+1, objective_loss=float(loss.detach()),
                       unweighted_batch_ce=float(ordinary.detach()))
            history.append(row)
            if progress is not None:
                progress(row)
    require(all(torch.isfinite(p).all().item() for p in model.parameters()), 'Nonfinite final weights')
    return model.eval(), dict(steps=steps, examples_drawn=steps*batch_size,
        batch_schedule_sha256=schedule.hexdigest(), training_log=history)


def gate(pairs):
    if [p.get('seed') for p in pairs] != list(SEEDS):
        return False
    for p in pairs:
        if not (p.get('paired_initial_equal') is True and p.get('paired_batches_equal') is True):
            return False
        a, c = p['conditional'], p['uniform']
        values = [a['macro_missing_balanced_accuracy'], c['macro_missing_balanced_accuracy'],
                  a['metrics']['macro_group_balanced_accuracy'], c['metrics']['macro_group_balanced_accuracy'],
                  a['by_missing_count']['1']['needs_recall'], c['by_missing_count']['1']['needs_recall'],
                  a['by_missing_count']['3']['sufficient_recall'], c['by_missing_count']['3']['sufficient_recall'],
                  a['metrics']['needs_recall'], a['metrics']['sufficient_recall']]
        if not all(isinstance(v, (int,float)) and not isinstance(v,bool) and np.isfinite(v) for v in values):
            return False
        if not (values[0] > values[1] and values[2] >= values[3] and values[4] > values[5]
                and values[6] > values[7] and values[8] > .5 and values[9] > .5):
            return False
    return True


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,parent_sha256=PARENT_SHA,
        data_sha256='eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65',
        seeds=SEEDS,arms=ARMS,model='unchanged C174 MLP72-128-ReLU-128-ReLU-2',parameters=26114,
        weights='TRAIN N_m/(2*N_m_y) for mixed-label stratum;1 for pure stratum;no clipping',
        reduction='mean(row_weight*unreduced_CE);not division by batch weight sum',
        train_counts=COUNTS,train_rows=42444,eval_rows=9396,train_groups=36,eval_groups=4,
        features='unchanged72 scaled C170 fields;syntax visible in BOTH arms',
        steps=STEPS,batch_size=BATCH,optimizer='Adam',lr=LR,betas=[.9,.999],eps=1e-8,
        weight_decay=0,amsgrad=False,foreach=False,sampling='paired uniform rows with replacement;seed+1000000',
        device='cpu',dtype='float32',threads=2,deterministic_algorithms=True,
        training_updates=12000,training_rows_drawn=3072000,pilot_predictions=56376,
        training_resubstitution_predictions=254664,inference_batches=312,
        evaluation='all6 final checkpoints saved/reloaded BEFORE any scores;raw argmax',
        primary='equal mean BA of missing-count strata1,2,3 on reused PILOT_EVAL',
        gate='each seed primary strictly improves;original groupmacro does not drop;count1 needs and count3 sufficient recalls strictly improve;both aggregate recalls>0.5',
        scope='post-C175 development intervention;not independent holdout,final Gate E or FOLD core')


def load_sources(c175_summary, c174_summary):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(audit.sha(c175_summary) == PARENT_SHA, 'C175 summary hash mismatch')
    p = audit.read_json(c175_summary)
    require(p['experiment_id'] == audit.EXPERIMENT_ID and p['commit_sha'] == BASE
            and p['status'] == 'PASS' and p['diagnostic_execution_valid'] is True
            and p['replayed_model_predictions'] == 311040 and p['blind_keys'] == 81
            and len(p['source_blobs']) == 48, 'Wrong C175 identity/profile')
    require(audit.gate(p['pairs'],p['reference']), 'C175 verdict disagreement')
    p174 = audit.load_parent(c174_summary)
    require(p['C174_summary_sha256'] == audit.PARENT_SHA, 'Parent lineage mismatch')
    protected = audit.protect_artifacts(c174_summary,p174)
    protected[str(Path(c175_summary).resolve())] = PARENT_SHA
    items = p['artifacts']; require(len(items) == 2 and {a['file'] for a in items} ==
        {'audit-plan.json','audit-details.json'}, 'C175 artifact set drift')
    for item in items:
        f = audit.safe_child(Path(c175_summary).resolve().parent,item['file'])
        require(f.stat().st_size == item['serialized_bytes'] and audit.sha(f) == item['sha256'],
                'C175 artifact drift: '+item['file'])
        protected[str(f.resolve())] = item['sha256']
    return p, p174, protected


def protect_sources(root, parent):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    pins = dict(parent['source_blobs'])
    for n in audit.OWN:
        pins[n] = audit.git(root,'rev-parse',BASE+':'+n).decode().strip()
    require(len(pins) == 52, 'Historical source union drift')
    all_pins = dict(pins)
    for n in OWN:
        all_pins[n] = audit.git(root,'rev-parse','HEAD:'+n).decode().strip()
    return pins, audit.protect_tree_files(root,all_pins)


def precheck(c175_summary,c174_summary,root):
    p, p174, protected = load_sources(c175_summary,c174_summary)
    pins, source_hashes = protect_sources(root,p); protected.update(source_hashes)
    require(hashlib.sha256(blob(manifest())).hexdigest() == MANIFEST_SHA, 'Manifest drift')
    return p, p174, pins, protected


def score(data, pred, mask, audit):
    y, g = data['labels'][mask], data['groups'][mask]
    m = missing_counts(data['features'][mask])
    strata = {str(k):audit.basic_metrics(y[m==k],pred[m==k]) for k in range(5)}
    require(all(strata[str(k)]['balanced_accuracy'] is not None for k in (1,2,3)), 'Mixed stratum absent')
    return dict(metrics=audit.metrics(y,pred,g),by_missing_count=strata,
        macro_missing_balanced_accuracy=sum(strata[str(k)]['balanced_accuracy'] for k in (1,2,3))/3)


def regression_modules(root):
    text = (Path(root)/'tools/run_c167.ps1').read_text(encoding='utf-8')
    names = re.findall(r'^\s*"(tests_lm\.[a-zA-Z0-9_]+)"\s*$',text,re.M)
    require(len(names) == len(set(names)) == 51, 'Historical regression list drift')
    return names + ['tests_lm.'+n for n in ('test_v05_c168_necessity_observability',
        'test_v05_c169_interface_batch','test_v05_c170_structured_task_input','test_v05_c171_derived_result',
        'test_v05_c172_action_runtime','test_v05_c173_acquisition_lifecycle','test_v05_c174_learned_necessity',
        'test_v05_c175_frozen_prediction_audit','test_v05_c176_conditional_loss')]


def run(*,c175_summary,c174_summary,output_dir,expected_head):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05 import structured_necessity_probe as api
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,'rev-parse','HEAD').decode().strip() == expected_head,'HEAD mismatch')
        require(audit.git(root,'branch','--show-current').decode().strip() == 'feat/sft-target-loss','Branch mismatch')
        require(not audit.git(root,'status','--porcelain','--untracked-files=no').strip(),'Tracked tree dirty')
    guard(); parent,p174,pins,protected = precheck(c175_summary,c174_summary,root)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    started = time.perf_counter(); artifacts=[]; fits=[]; pairs=[]
    def record(name):
        f=out/name;artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,value):
        (out/name).write_bytes(blob(value));record(name)
    save('conditional-plan.json',dict(manifest(),source_blobs=pins))
    try:
        print('[C176] plan fixed; paired TRAIN-loss-only intervention; no larger model or extra steps',flush=True)
        data,_ = audit.load_data(Path(c174_summary).resolve().parent,p174)
        train=data['split_codes']==0; ev=~train
        w,table=conditional_weights(data['labels'][train],missing_counts(data['features'][train]))
        require(tuple(tuple(r['counts']) for r in table)==COUNTS,'TRAIN conditional counts drift')
        save('train-weight-table.json',table)
        torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
        raw=torch.from_numpy(data['features']);x=api.prepare(raw[train],api.ARMS[0])
        y=torch.from_numpy(data['labels'][train].copy());weights=torch.from_numpy(w.astype(np.float32))
        models={}
        for seed in SEEDS:
            torch.manual_seed(seed);initial=api.NecessityProbe().cpu();ih=fingerprint(initial)
            require(sum(p.numel() for p in initial.parameters())==26114,'Model capacity drift')
            for arm in ARMS:
                rw=torch.ones_like(weights) if arm==ARMS[0] else weights
                def progress(row,seed=seed,arm=arm):
                    print(f"[C176] seed={seed} arm={arm} step={row['step']}/2000 objective={row['objective_loss']:.6f} ordinary_ce={row['unweighted_batch_ce']:.6f}",flush=True)
                model,log=fit(initial,x,y,rw,seed,progress=progress)
                require(fingerprint(initial)==ih,'Initial model mutated')
                f=out/f'probe-{seed}-{arm}.pt'
                torch.save(dict(seed=seed,arm=arm,steps=STEPS,state_dict=model.state_dict()),f)
                checkpoint=torch.load(f,map_location='cpu',weights_only=True)
                require((checkpoint['seed'],checkpoint['arm'],checkpoint['steps'])==(seed,arm,STEPS),'Checkpoint identity drift')
                restored=api.NecessityProbe().cpu();restored.load_state_dict(checkpoint['state_dict'],strict=True)
                require(fingerprint(restored)==fingerprint(model),'Checkpoint roundtrip drift')
                record(f.name);models[seed,arm]=restored.eval()
                fits.append(dict(seed=seed,arm=arm,initial_sha256=ih,final_sha256=fingerprint(restored),**log))
        require(len(fits)==6 and all(f['steps']==2000 and f['examples_drawn']==512000 for f in fits),'Incomplete fits')
        for i in range(0,6,2):
            require(fits[i]['initial_sha256']==fits[i+1]['initial_sha256'] and
                fits[i]['batch_schedule_sha256']==fits[i+1]['batch_schedule_sha256'],'Unpaired training')
        # No scores, inference, early stopping or model selection before all six saved fits.
        evaluation=[];training=[];pilot_records=[];train_predictions=[]
        for i,(seed,arm) in enumerate((s,a) for s in SEEDS for a in ARMS):
            pred,logits=api.predict(models[seed,arm],api.prepare(raw[ev],api.ARMS[0]))
            evaluation.append(score(data,pred.numpy(),ev,audit))
            pilot_records.append(dict(seed=seed,arm=arm,row_indices=np.flatnonzero(ev).tolist(),
                predictions=pred.tolist(),logits=logits.tolist()))
            tp,_=api.predict(models[seed,arm],x)
            training.append(dict(seed=seed,arm=arm,**score(data,tp.numpy(),train,audit)))
            train_predictions.append(tp.numpy().astype(np.int8))
        for i,seed in enumerate(SEEDS):
            p=dict(seed=seed,uniform=evaluation[2*i],conditional=evaluation[2*i+1],
                paired_initial_equal=True,paired_batches_equal=True)
            pairs.append(p)
            print(f"[C176] seed={seed} mixed_count_BA uniform={p['uniform']['macro_missing_balanced_accuracy']:.6f} conditional={p['conditional']['macro_missing_balanced_accuracy']:.6f}",flush=True)
        save('pilot-predictions.json',pilot_records)
        np.savez_compressed(out/'training-predictions.npz',row_indices=np.flatnonzero(train).astype('<i4'),
                            predictions=np.stack(train_predictions));record('training-predictions.npz')
        guard();protect_sources(root,parent)
        for name,want in protected.items():require(audit.sha(name)==want,'Protected input changed: '+name)
        for a in artifacts:require(audit.sha(out/a['file'])==a['sha256'],'Output changed: '+a['file'])
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status='PASS' if gate(pairs) else 'FAIL',diagnostic_execution_valid=True,
            production_runtime_modified=False,gate_e_candidate=False,C175_summary_sha256=PARENT_SHA,
            C174_summary_sha256=audit.PARENT_SHA,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
            pairs=pairs,training_metrics=training,fit_records=fits,train_weight_table=table,
            data_content_sha256=audit.DATA_SHA,fresh_seeds=3,trained_models=6,training_steps_total=12000,
            training_examples_drawn=3072000,training_forward_calls=12000,inference_forward_calls=312,
            pilot_predictions=sum(len(r['predictions']) for r in pilot_records),
            training_resubstitution_predictions=sum(len(r) for r in train_predictions),
            historical_checkpoint_deserializations=0,new_checkpoint_deserializations=6,
            actual_acquisitions=0,proof_checker_calls=0,evidence_writes=0,network_calls=0,
            environment=dict(torch=torch.__version__,numpy=np.__version__,device='cpu',dtype='float32',threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['post-C175 development intervention on reused four pilot groups,not independent confirmation',
                'same diagnostic MLP,not FOLD shared core or a live policy',
                'loss changes training incentives;success would not prove a unique internal causal mechanism',
                'raw argmax,no inference teacher,proof repair,capacity increase or checkpoint selection'])
        (out/'summary.json').write_bytes(blob(result))
        print('=== C176 RESULT ===',flush=True);print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/'invalid.json').write_bytes(blob(dict(experiment_id=EXPERIMENT_ID,status='INVALID',
            diagnostic_execution_valid=False,error=str(exc),completed_fits=fits,completed_pairs=pairs)))
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--c175-summary',type=Path,required=True);p.add_argument('--c174-summary',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--expected-head',required=True)
    run(**vars(p.parse_args()))


if __name__ == '__main__':
    main()
