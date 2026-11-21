"""C180: mask only the raw-fact shortcut to a fixed tree probe's final readout.

No Boolean solver, extra supervision, weighted loss, calibration or live actions.
The original C179 cell/forward/fit/predict execute unchanged in both new conditions.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import torch
from torch import nn
from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph

EXPERIMENT_ID = 'C180-v5e-direct-fact-readout-ablation'
STAGE = 'V5-E-DIRECT-FACT-READOUT-ABLATION'
BASE = 'ec1db352749e4931d59aa7a21f1766347cbf918e'
PARENT_SHA = 'ba7488e2002894ccf614c29e84e0d50594dfba7617abfd8d9f4b64442915767b'
SEEDS = (180001, 180002, 180003)
ARMS = ('DIRECT_FACTS', 'NO_DIRECT_FACTS')
MODEL_SCHEMA = 'c180-tree-fact-readout-ablation-v1'
REPRESENTATION = 'c178-scaled-visible-leaf-binding-v1'
FACT_START, FACT_END, HEAD_WIDTH = 68, 84, 94
OWN = ('fold_lm/v05_benchmarks/gate_e_c180_fact_bypass.py',
       'tests_lm/test_v05_c180_fact_bypass.py', 'tools/run_c180.ps1',
       'docs/experiment-ledger-addendum-c180-preregistration.md')
MANIFEST_SHA = '22168a208e57615467b3d592cf1c72b27b286dbe0e8a24850bbc143b9da0e442'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


class FactReadoutMask(nn.Module):
    """Identical dense multiplication in both arms; only 16 mask constants differ.

    Input is [root64, header4, raw-facts16, runtime10], not a C170 packet.
    No learned parameters or state buffers. Condition is checkpoint metadata, not a weight.
    """
    def __init__(self, condition):
        super().__init__()
        require(condition in ARMS, 'Explicit registered readout condition required')
        self.condition = condition
        self.calls = 0

    def forward(self, x):
        require(self.condition in ARMS, 'Readout condition drift')
        require(isinstance(x, torch.Tensor) and x.dtype == torch.float32
                and x.device.type == 'cpu' and x.ndim == 2 and x.shape[1] == HEAD_WIDTH
                and len(x) > 0 and torch.isfinite(x).all().item(),
                'Finite nonempty CPU float32 [N,94] readout input required')
        mask = x.new_ones(HEAD_WIDTH)
        if self.condition == ARMS[1]:
            mask[FACT_START:FACT_END] = 0
        self.calls += 1
        return x * mask


def make_model(condition):
    require(condition in ARMS, 'Unknown condition')
    model = graph.SharedGraphProbe(graph.ARMS[1])
    model.readout = nn.Sequential(FactReadoutMask(condition), model.readout)
    validate_model(model, condition)
    return model


def validate_model(model, condition):
    require(condition in ARMS and type(model) is graph.SharedGraphProbe
            and model.arm == graph.ARMS[1], 'Both conditions must use original TREE_LINKS')
    require(type(model.readout) is nn.Sequential and len(model.readout) == 2
            and type(model.readout[0]) is FactReadoutMask
            and model.readout[0].condition == condition
            and type(model.readout[1]) is nn.Linear
            and model.readout[1].in_features == 94 and model.readout[1].out_features == 2,
            'Explicit masked readout contract required')
    require(sum(p.numel() for p in model.parameters()) == 25726, 'Parameter count changed')


def paired_initial(seed):
    require(type(seed) is int and 0 <= seed < 2**31, 'Integer seed required')
    torch.manual_seed(seed)
    a = make_model(ARMS[0]); b = deepcopy(a); b.readout[0].condition = ARMS[1]
    validate_model(b, ARMS[1])
    require(graph.fingerprint(a) == graph.fingerprint(b), 'Initial weights differ')
    return a, b


def checkpoint_payload(model, seed, condition):
    validate_model(model, condition)
    require(type(seed) is int and seed >= 0, 'Integer checkpoint seed required')
    return dict(seed=seed, condition=condition, model_schema=MODEL_SCHEMA,
                representation=REPRESENTATION, graph_arm=graph.ARMS[1], steps=2000,
                fact_readout_slice=[FACT_START, FACT_END],
                weight_sha256=graph.fingerprint(model), state_dict=model.state_dict())


def restore(path, seed, condition):
    payload = torch.load(path, map_location='cpu', weights_only=True)
    require((payload['seed'], payload['condition'], payload['model_schema'],
             payload['representation'], payload['graph_arm'], payload['steps'],
             payload['fact_readout_slice']) ==
            (seed, condition, MODEL_SCHEMA, REPRESENTATION, graph.ARMS[1], 2000,
             [FACT_START, FACT_END]), 'Checkpoint identity/representation/mask drift')
    model = make_model(condition)
    model.load_state_dict(payload['state_dict'], strict=True)
    require(graph.fingerprint(model) == payload['weight_sha256'], 'Checkpoint weights changed')
    return model.eval()


def gate(pairs):
    if [p.get('seed') for p in pairs] != list(SEEDS):
        return False
    for p in pairs:
        if p.get('paired_initial_equal') is not True or p.get('paired_batches_equal') is not True:
            return False
        try:
            a, b = p['no_direct'], p['direct']
            v = [a['macro_missing_balanced_accuracy'], b['macro_missing_balanced_accuracy'],
                 a['metrics']['macro_group_balanced_accuracy'], b['metrics']['macro_group_balanced_accuracy'],
                 a['by_missing_count']['1']['needs_recall'], b['by_missing_count']['1']['needs_recall'],
                 a['by_missing_count']['3']['sufficient_recall'], b['by_missing_count']['3']['sufficient_recall'],
                 a['metrics']['needs_recall'], a['metrics']['sufficient_recall']]
        except (KeyError, TypeError):
            return False
        if not all(type(x) in (int, float) and np.isfinite(x) for x in v):
            return False
        if not (v[0] > v[1] and v[2] >= v[3] and v[4] > v[5] and v[6] > v[7]
                and v[8] > .5 and v[9] > .5):
            return False
    return True


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, parent_sha256=PARENT_SHA, seeds=SEEDS, arms=ARMS,
        model_schema=MODEL_SCHEMA, representation=REPRESENTATION, parameters=25726,
        changed='only raw-facts16 at readout columns68:84 masked; leaves and root path unchanged',
        graph='unchanged C179 SharedGraphProbe TREE_LINKS in BOTH conditions; seven cells',
        readout='root64+header4+facts16+runtime10; dense94-mask then unchanged Linear94x2',
        loss='ordinary unweighted CE via unchanged C179 fit in BOTH conditions',
        dense_macs_per_row=177596, elementwise_mask_multiplies_per_row=94,
        model_updates=12000, training_cell_calls=84000, training_rows_drawn=3072000,
        pilot_predictions=56376, training_predictions=254664, inference_batches=312,
        inference_cell_calls=2184, readout_mask_calls=12312,
        prepared_rows=51840, leaf_fact_reads=207360, copied_fields=414720,
        steps=2000, batch=256, optimizer='Adam', lr=.001, betas=[.9,.999], eps=1e-8,
        weight_decay=0, amsgrad=False, foreach=False, row_rng='seed+1000000',
        device='cpu', dtype='float32', threads=2, deterministic_algorithms=True,
        data_sha256='eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65',
        train_rows=42444, pilot_rows=9396, train_groups=36, pilot_groups=4,
        evaluation='all6 final checkpoints saved/reloaded before any scores; raw argmax',
        primary='equal mean BA of missing1/2/3; each no_direct improves vs paired direct',
        guards='groupmacro cannot decline;count1NEEDS/count3SUFFICIENT improve;both recalls>0.5',
        secondary='both split confusion/order/paired errors and logits;not replacement gates',
        old_checkpoint_loads=0, new_checkpoint_loads=6, actual_acquisitions=0,
        proof_calls=0, evidence_writes=0, network_calls=0,
        scope='development bypass intervention,not an adopted tree/FOLD core or independent holdout')


def precheck(c179_summary, c178_summary, c177_summary, c176_summary, c174_summary, root):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    p174, pins, protected = graph.precheck(c178_summary, c177_summary, c176_summary, c174_summary, root)
    require(audit.sha(c179_summary) == PARENT_SHA, 'C179 summary hash mismatch')
    p = audit.read_json(c179_summary)
    require(p['experiment_id'] == graph.EXPERIMENT_ID and p['commit_sha'] == BASE
            and p['status'] == 'FAIL' and p['diagnostic_execution_valid'] is True
            and not graph.gate(p['pairs']) and p['source_blobs'] == pins,
            'Wrong accepted C179 identity/negative/source chain')
    require(p['trained_models'] == 6 and p['training_steps_total'] == 12000
            and p['parameters_per_model'] == 25726 and p['dense_macs_per_row'] == 177596,
            'Parent workload drift')
    protected[str(Path(c179_summary).resolve())] = PARENT_SHA
    expected = {'shared-graph-plan.json', 'shared-input-audit.json', 'pilot-predictions.json',
                'training-predictions.npz'}
    expected |= {f'probe-{s}-{a}.pt' for s in graph.SEEDS for a in graph.ARMS}
    require(len(p['artifacts']) == 10 and {a['file'] for a in p['artifacts']} == expected,
            'C179 artifact set drift')
    for a in p['artifacts']:
        f = audit.safe_child(Path(c179_summary).resolve().parent, a['file'])
        require(f.is_file() and f.stat().st_size == a['serialized_bytes'] and audit.sha(f) == a['sha256'],
                'Changed C179 artifact: '+a['file'])
        protected[str(f.resolve())] = a['sha256']
    pins = dict(pins)
    for name in graph.OWN:
        pins[name] = audit.git(root, 'rev-parse', BASE+':'+name).decode().strip()
    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root, 'rev-parse', 'HEAD:'+name).decode().strip()
    protected.update(audit.protect_tree_files(root, allpins))
    require(len(pins) == 68 and len(protected) == 120, 'Source/input union drift')
    require(hashlib.sha256(blob(manifest())).hexdigest() == MANIFEST_SHA, 'Manifest drift')
    return p174, pins, protected


def regression_modules(root):
    names = graph.regression_modules(root)
    require(len(names) == len(set(names)) == 63, 'Historical regression list drift')
    return names+['tests_lm.test_v05_c180_fact_bypass']


def run(*, c179_summary, c178_summary, c177_summary, c176_summary, c174_summary,
        output_dir, expected_head):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as ordering
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root, 'rev-parse', 'HEAD').decode().strip() == expected_head, 'HEAD mismatch')
        require(audit.git(root, 'branch', '--show-current').decode().strip() == 'feat/sft-target-loss', 'Branch mismatch')
        require(not audit.git(root, 'status', '--porcelain', '--untracked-files=no').strip(), 'Tracked tree dirty')
    guard()
    sources = (c179_summary, c178_summary, c177_summary, c176_summary, c174_summary, root)
    p174, pins, protected = precheck(*sources)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter(); fits=[]; pairs=[]; artifacts=[]; inference=[]
    def record(name):
        f=out/name; artifacts.append(dict(file=name, sha256=audit.sha(f), serialized_bytes=f.stat().st_size))
    def save(name, value):
        (out/name).write_bytes(blob(value)); record(name)
    save('fact-bypass-plan.json', dict(manifest(), source_blobs=pins))
    try:
        print('[C180] plan fixed; raw-fact readout path only; both original TREE_LINKS', flush=True)
        torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
        data, _ = audit.load_data(Path(c174_summary).resolve().parent, p174)
        raw=torch.from_numpy(data['features']); before=graph.tensor_sha(raw)
        x=binding.prepare_pair(raw)[1]; xb=graph.tensor_sha(x); graph.tree_links(x)
        train=data['split_codes']==0; ev=data['split_codes']==1
        require((len(raw),int(train.sum()),int(ev.sum()))==(51840,42444,9396), 'Dataset coverage drift')
        save('readout-mask-audit.json', dict(prepared_rows=len(raw), raw_tensor_sha256=before,
            common_input_sha256=xb, readout_width=94, fact_slice=[68,84],
            direct_mask=[1]*94, no_direct_mask=[1]*68+[0]*16+[1]*10,
            input_to_all_cells_unchanged=True, leaf_fact_reads=207360, copied_fields=414720))
        xt=x[train]; yt=torch.from_numpy(data['labels'][train].copy()); models={}
        for seed in SEEDS:
            initials=paired_initial(seed)
            for j, condition in enumerate(ARMS):
                initial=initials[j]; ih=graph.fingerprint(initial)
                def progress(row, seed=seed, condition=condition):
                    print(f"[C180] seed={seed} arm={condition} step={row['step']}/2000 train_loss={row['training_loss']:.6f}", flush=True)
                model, log=graph.fit(initial, xt, yt, seed, progress=progress)
                validate_model(model, condition)
                require(model.readout[0].calls == 2000, 'Training mask meter mismatch')
                require(graph.fingerprint(initial)==ih, 'Initial weights mutated')
                name=f'probe-{seed}-{condition}.pt'
                torch.save(checkpoint_payload(model, seed, condition), out/name)
                restored=restore(out/name, seed, condition)
                require(graph.fingerprint(restored)==graph.fingerprint(model), 'Roundtrip drift')
                record(name); models[seed,condition]=restored
                fits.append(dict(seed=seed, arm=condition, initial_sha256=ih,
                    final_sha256=graph.fingerprint(restored), parameters=25726, **log))
        require(len(fits)==6 and all(f['steps']==2000 and f['examples_drawn']==512000 for f in fits), 'Incomplete fit')
        require(all(fits[i]['initial_sha256']==fits[i+1]['initial_sha256'] and
                    fits[i]['batch_schedule_sha256']==fits[i+1]['batch_schedule_sha256'] for i in (0,2,4)), 'Unpaired fit')
        # All six saved and restored before producing any evaluation or TRAIN score.
        ps=[]; ts=[]; zs=[]; training=[]; changes=[]
        missing=ordering.missing_counts(data['features'])
        for seed in SEEDS:
            scores=[]; allpred=[]
            for condition in ARMS:
                model=models[seed,condition]; validate_model(model,condition)
                pred,z,im=graph.predict(model,x[ev]); tp,tz,tm=graph.predict(model,xt)
                validate_model(model,condition)
                inference += [dict(seed=seed,arm=condition,split='PILOT_EVAL',**im),
                              dict(seed=seed,arm=condition,split='TRAIN_RESUBSTITUTION',**tm)]
                scores.append(binding.score(data,pred.numpy(),z.numpy(),ev,audit,ordering))
                training.append(dict(seed=seed,arm=condition,**binding.score(data,tp.numpy(),tz.numpy(),train,audit,ordering)))
                ps.append(dict(seed=seed,arm=condition,model_schema=MODEL_SCHEMA,representation=REPRESENTATION,
                    row_indices=np.flatnonzero(ev).tolist(),predictions=pred.tolist(),logits=z.tolist()))
                ts.append(tp.numpy().astype(np.int8));zs.append(tz.numpy())
                full=np.empty(len(raw),dtype=np.int8);full[train]=tp.numpy();full[ev]=pred.numpy();allpred.append(full)
            pairs.append(dict(seed=seed,direct=scores[0],no_direct=scores[1],paired_initial_equal=True,paired_batches_equal=True))
            parts={}
            for mask,part in ((train,'TRAIN_RESUBSTITUTION'),(ev,'PILOT_EVAL')):
                def exchange(m):return ordering.transitions(data['labels'][m],allpred[0][m],allpred[1][m])
                parts[part]=dict(overall=exchange(mask),by_missing_count={str(k):exchange(mask&(missing==k)) for k in range(5)})
            changes.append(dict(seed=seed,parts=parts))
            print(f"[C180] seed={seed} mixed_count_BA direct={scores[0]['macro_missing_balanced_accuracy']:.6f} no_direct={scores[1]['macro_missing_balanced_accuracy']:.6f}",flush=True)
        save('pilot-predictions.json',ps)
        np.savez_compressed(out/'training-predictions.npz',row_indices=np.flatnonzero(train).astype('<i4'),
            predictions=np.stack(ts),logits=np.stack(zs),seeds=np.array([s for s in SEEDS for _ in ARMS],dtype='<i4'),
            arm_indices=np.tile(np.arange(2,dtype=np.int8),3))
        record('training-predictions.npz')
        require(sum(f['training_forward_calls'] for f in fits)==12000 and sum(f['training_cell_calls'] for f in fits)==84000, 'Training counter drift')
        require(sum(m.readout[0].calls for m in models.values())==312, 'Inference mask meter mismatch')
        require(sum(r['forward_calls'] for r in inference)==312 and sum(r['cell_calls'] for r in inference)==2184, 'Inference counter drift')
        guard();precheck(*sources)
        require(graph.tensor_sha(raw)==before and graph.tensor_sha(x)==xb, 'Inputs mutated')
        for name,want in protected.items():require(audit.sha(name)==want,'Protected input changed: '+name)
        for a in artifacts:require(audit.sha(out/a['file'])==a['sha256'],'Output changed: '+a['file'])
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status='PASS' if gate(pairs) else 'FAIL',diagnostic_execution_valid=True,
            C179_summary_sha256=PARENT_SHA,C174_summary_sha256=audit.PARENT_SHA,data_content_sha256=audit.DATA_SHA,
            source_blobs=pins,input_sha256=protected,artifacts=artifacts,pairs=pairs,training_metrics=training,
            error_exchanges=changes,fit_records=fits,inference_records=inference,
            fresh_seeds=3,trained_models=6,parameters_per_model=25726,dense_macs_per_row=177596,
            mask_multiplies_per_row=94,readout_mask_calls=12312,
            training_steps_total=12000,training_examples_drawn=3072000,training_forward_calls=12000,
            training_cell_calls=84000,inference_forward_calls=312,inference_cell_calls=2184,
            pilot_predictions=56376,training_resubstitution_predictions=254664,
            prepared_rows=51840,leaf_fact_reads=207360,copied_numeric_fields=414720,
            historical_checkpoint_deserializations=0,new_checkpoint_deserializations=6,
            actual_acquisitions=0,proof_checker_calls=0,evidence_writes=0,network_calls=0,
            production_runtime_modified=False,gate_e_candidate=False,
            environment=dict(torch=torch.__version__,numpy=np.__version__,device='cpu',dtype='float32',threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['same reused four development groups,not independent holdout',
                'both use unadopted C179 TREE_LINKS as common experimental substrate',
                'mask removes redundant direct facts,not visible facts at syntax leaves',
                '32 final weight coordinates receive zero gradient when their inputs are masked;nominal capacity parity is not effective parity',
                'masking changes optimization and direct linear expressivity;no unique internal mechanism proven',
                'no solver,hidden values,proof repair,loss weighting,threshold fitting or live acquisition'])
        (out/'summary.json').write_bytes(blob(result))
        print('=== C180 RESULT ===',flush=True);print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/'invalid.json').write_bytes(blob(dict(experiment_id=EXPERIMENT_ID,status='INVALID',
            diagnostic_execution_valid=False,error=str(exc),completed_fits=fits,completed_pairs=pairs)))
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('c179','c178','c177','c176','c174'):p.add_argument('--'+n+'-summary',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--expected-head',required=True)
    run(**vars(p.parse_args()))


if __name__=='__main__':
    main()
