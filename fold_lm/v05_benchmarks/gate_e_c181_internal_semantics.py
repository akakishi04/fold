"""C181: TRAIN-only proper-subexpression supervision with unchanged inference.

Both arms run the original C179 tree forward including its direct fact readout.
Only the coefficient of a three-class auxiliary TRAIN loss differs: zero or one.
The teacher never supplies values to the neural forward or scores pilot subtrees.
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

EXPERIMENT_ID = 'C181-v5e-proper-subexpression-supervision'
STAGE = 'V5-E-PROPER-SUBEXPRESSION-SUPERVISION'
BASE = '074419e41b38ad756b2c29a50ea070d5ca60f2d3'
PARENT_SHA = '9ad6eb52054388abda89d2eb8254b2ce278bfc983ae2a6375ab7d8327f91adf2'
SEEDS = (181001, 181002, 181003)
ARMS = ('FINAL_ONLY', 'INTERNAL_SEMANTICS')
CLASSES = ('KNOWN_ZERO', 'KNOWN_ONE', 'UNRESOLVED')
MODEL_SCHEMA = 'c181-proper-internal-semantics-v1'
REPRESENTATION = 'c178-scaled-visible-leaf-binding-v1'
PARAMETERS, INFERENCE_PARAMETERS = 25921, 25726
STEPS, BATCH = 2000, 256
OWN = ('fold_lm/v05_benchmarks/gate_e_c181_internal_semantics.py',
       'tests_lm/test_v05_c181_internal_semantics.py', 'tools/run_c181.ps1',
       'docs/experiment-ledger-addendum-c181-preregistration.md')
MANIFEST_SHA = '1f1baf3f40018ab84eb69d1812cf0c04d9fae624ee50e705d3bc780e35d6d3f4'
require = graph.require
blob = graph.blob


def teacher_targets(raw: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Exact teacher for the read-once TRAIN family; no root or hidden-bit targets.

    Accept canonical raw observed/unobserved facts only. Evaluate the six nonroot
    nodes, retain the two proper binary nodes, and never evaluate the root.
    This programmed logic is exclusively a training-label generator, not inference.
    """
    require(isinstance(raw, torch.Tensor) and raw.device.type == 'cpu'
            and raw.dtype == torch.int32 and raw.ndim == 2 and raw.shape[1] == 72
            and len(raw) > 0 and ((raw >= 0) & (raw < 2**24)).all().item(),
            'Canonical nonempty CPU int32 TRAIN fields required')
    indices, labels = [], []
    for row in raw.tolist():
        require(row[:2] == [7, 4], 'Read-once seven-node/four-fact teacher only')
        nodes = [row[4+6*i:10+6*i] for i in range(7)]
        facts = [row[46+4*i:50+4*i] for i in range(4)]
        require(all(f[0] == 1 and f[1] in (1, 2) and f[2] == int(f[1] == 2)
                    and f[3] in (0, 1) and (f[2] == 1 or f[3] == 0) for f in facts),
                'Teacher cannot read hidden/stale/conflicting payloads')
        parents = [0]*7; fact_ids = []; proper = []
        for i, (active, kind, fact, left, right, neg) in enumerate(nodes):
            require(active == 1 and kind in (1, 2, 3) and neg in (0, 1), 'Invalid node')
            if kind == 1:
                require(1 <= fact <= 4 and left == right == 0, 'Invalid leaf')
                fact_ids.append(fact)
            else:
                require(fact == neg == 0 and 1 <= left <= i and 1 <= right <= i,
                        'Invalid internal link')
                parents[left-1] += 1; parents[right-1] += 1
                if i < 6: proper.append(i)
        require(sorted(fact_ids) == [1, 2, 3, 4] and parents == [1]*6+[0]
                and len(proper) == 2, 'Teacher requires connected read-once tree')
        state = []
        for active, kind, fact, left, right, neg in nodes[:6]:
            if kind == 1:
                f = facts[fact-1]; v = (f[3] ^ neg) if f[2] else 2
            else:
                a, b = state[left-1], state[right-1]
                if kind == 2: v = 0 if 0 in (a, b) else (1 if a == b == 1 else 2)
                else: v = 1 if 1 in (a, b) else (0 if a == b == 0 else 2)
            state.append(v)
        indices.append(proper); labels.append([state[i] for i in proper])
    return torch.tensor(indices, dtype=torch.int64), torch.tensor(labels, dtype=torch.int64)


def proper_indices(x: torch.Tensor) -> torch.Tensor:
    nodes, _ = graph.tree_links(x)
    keep = (nodes[:, :, 1] > .5) & (torch.arange(7)[None, :] < 6)
    require((keep.sum(1) == 2).all().item(), 'Exactly two proper binary nodes required')
    return keep.nonzero(as_tuple=False)[:, 1].reshape(len(x), 2)


class SemanticProbe(nn.Module):
    """Auxiliary head reads learned states; its outputs never feed the main path."""
    def __init__(self, condition: str):
        super().__init__(); require(condition in ARMS, 'Explicit condition required')
        self.condition = condition
        self.base = graph.SharedGraphProbe(graph.ARMS[1])
        self.auxiliary = nn.Linear(64, 3, dtype=torch.float32)
        self.auxiliary_calls = self.auxiliary_rows = 0

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.base(x)  # Identical original inference; no teacher/head/hook.

    def training_forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        ix = proper_indices(x); states = []
        handle = self.base.cell.register_forward_hook(lambda module, args, output: states.append(output))
        try:
            logits = self.base(x)
        finally:
            handle.remove()
        require(len(states) == 7, 'Capture must observe exactly seven original cell calls')
        selected = torch.stack(states, dim=1)[torch.arange(len(x))[:, None], ix]
        aux = self.auxiliary(selected)
        self.auxiliary_calls += 1; self.auxiliary_rows += 2*len(x)
        return logits, aux


def validate_model(model, condition):
    require(type(model) is SemanticProbe and condition in ARMS and model.condition == condition,
            'Registered model/condition required')
    require(type(model.base) is graph.SharedGraphProbe and model.base.arm == graph.ARMS[1]
            and type(model.base.readout) is nn.Linear and model.base.readout.in_features == 94
            and model.base.readout.out_features == 2, 'Original direct-fact tree inference required')
    require(sum(p.numel() for p in model.parameters()) == PARAMETERS
            and sum(p.numel() for p in model.base.parameters()) == INFERENCE_PARAMETERS,
            'Model capacity drift')


def paired_initial(seed):
    require(type(seed) is int and 0 <= seed < 2**31, 'Integer seed required')
    torch.manual_seed(seed); a = SemanticProbe(ARMS[0]); b = deepcopy(a); b.condition = ARMS[1]
    validate_model(a, ARMS[0]); validate_model(b, ARMS[1])
    require(graph.fingerprint(a) == graph.fingerprint(b), 'Unpaired initialization')
    return a, b


def objective(logits, aux_logits, labels, targets, condition):
    require(condition in ARMS and logits.ndim == 2 and logits.shape[1] == 2
            and aux_logits.shape == (len(logits), 2, 3) and labels.shape == (len(logits),)
            and targets.shape == (len(logits), 2) and len(logits) > 0,
            'Main and two proper-node predictions required')
    require(labels.dtype == targets.dtype == torch.int64
            and ((labels >= 0) & (labels <= 1)).all().item()
            and ((targets >= 0) & (targets <= 2)).all().item()
            and torch.isfinite(logits).all().item() and torch.isfinite(aux_logits).all().item(),
            'Finite logits and typed labels required')
    main = nn.functional.cross_entropy(logits, labels)
    aux = nn.functional.cross_entropy(aux_logits.reshape(-1, 3), targets.reshape(-1))
    # Mean across the two nodes, not sum: fixed unit task-level coefficient.
    alpha = float(condition == ARMS[1])
    return main + alpha*aux, main, aux


def fit(initial, x, y, targets, seed, *, steps=STEPS, batch=BATCH, progress=None):
    validate_model(initial, initial.condition)
    require(type(seed) is int and 0 <= seed < 2**31 and type(steps) is int and steps > 0
            and type(batch) is int and batch > 0, 'Fixed positive workload and seed required')
    graph.tree_links(x)
    require(y.dtype == targets.dtype == torch.int64 and y.device.type == targets.device.type == 'cpu'
            and y.shape == (len(x),) and targets.shape == (len(x), 2)
            and set(y.tolist()) == {0, 1} and ((targets >= 0) & (targets <= 2)).all().item(),
            'Typed TRAIN targets required')
    model = deepcopy(initial).train()
    model.base.calls = model.base.cell_calls = model.base.rows = 0
    model.auxiliary_calls = model.auxiliary_rows = 0
    before = [graph.fingerprint(initial), graph.tensor_sha(x), graph.tensor_sha(y), graph.tensor_sha(targets)]
    opt = torch.optim.Adam(model.parameters(), lr=.001, betas=(.9, .999), eps=1e-8,
                           weight_decay=0, amsgrad=False, foreach=False)
    rng = torch.Generator(device='cpu').manual_seed(seed+1000000)
    schedule = hashlib.sha256(); history = []; started = time.perf_counter()
    for step in range(steps):
        ids = torch.randint(len(x), (batch,), generator=rng); schedule.update(ids.numpy().tobytes())
        opt.zero_grad(set_to_none=True)
        z, az = model.training_forward(x[ids])
        loss, main, aux = objective(z, az, y[ids], targets[ids], model.condition)
        require(torch.isfinite(loss).item(), 'Nonfinite loss')
        loss.backward()
        require(all(p.grad is not None and torch.isfinite(p.grad).all().item() for p in model.parameters()),
                'Invalid gradient')
        opt.step()
        if (step+1) % 500 == 0 or step+1 == steps:
            r = dict(step=step+1, training_loss=float(loss.detach()),
                     main_loss=float(main.detach()), auxiliary_loss=float(aux.detach()))
            history.append(r)
            if progress is not None: progress(r)
    require(all(torch.isfinite(p).all().item() for p in model.parameters()), 'Invalid final weights')
    require(before == [graph.fingerprint(initial), graph.tensor_sha(x), graph.tensor_sha(y), graph.tensor_sha(targets)],
            'Immutable training inputs changed')
    require((model.base.calls, model.base.cell_calls, model.base.rows, model.auxiliary_calls,
             model.auxiliary_rows) == (steps, 7*steps, steps*batch, steps, 2*steps*batch), 'Fit meter mismatch')
    return model.eval(), dict(steps=steps, examples_drawn=steps*batch,
        batch_schedule_sha256=schedule.hexdigest(), training_log=history,
        training_forward_calls=steps, training_cell_calls=7*steps, auxiliary_forward_calls=steps,
        auxiliary_target_uses=2*steps*batch, fit_wall_clock_seconds=time.perf_counter()-started)


def predict(model, x):
    """Only the original inference path; no auxiliary state read or teacher call."""
    validate_model(model, model.condition); before = graph.fingerprint(model)
    aux_before = (model.auxiliary_calls, model.auxiliary_rows)
    p, z, meter = graph.predict(model.base, x)
    require(graph.fingerprint(model) == before and aux_before == (model.auxiliary_calls, model.auxiliary_rows),
            'Inference must preserve weights and bypass auxiliary computation')
    return p, z, meter


def checkpoint_payload(model, seed):
    validate_model(model, model.condition)
    return dict(seed=seed, condition=model.condition, model_schema=MODEL_SCHEMA,
        representation=REPRESENTATION, classes=CLASSES, proper_nodes_only=True, root_supervision=False,
        steps=STEPS, alpha=int(model.condition == ARMS[1]), weight_sha256=graph.fingerprint(model),
        state_dict=model.state_dict())


def restore(path, seed, condition):
    p = torch.load(path, map_location='cpu', weights_only=True)
    require((p['seed'], p['condition'], p['model_schema'], p['representation'], tuple(p['classes']),
             p['proper_nodes_only'], p['root_supervision'], p['steps'], p['alpha']) ==
            (seed, condition, MODEL_SCHEMA, REPRESENTATION, CLASSES, True, False, STEPS, int(condition == ARMS[1])),
            'Checkpoint identity or supervision contract drift')
    model = SemanticProbe(condition); model.load_state_dict(p['state_dict'], strict=True)
    require(graph.fingerprint(model) == p['weight_sha256'], 'Checkpoint weights changed')
    validate_model(model, condition)
    return model.eval()


def gate(pairs):
    if [p.get('seed') for p in pairs] != list(SEEDS): return False
    for p in pairs:
        if p.get('paired_initial_equal') is not True or p.get('paired_batches_equal') is not True: return False
        try:
            a, b = p['internal'], p['final_only']
            v = [a['macro_missing_balanced_accuracy'], b['macro_missing_balanced_accuracy'],
                 a['metrics']['macro_group_balanced_accuracy'], b['metrics']['macro_group_balanced_accuracy'],
                 a['by_missing_count']['1']['needs_recall'], b['by_missing_count']['1']['needs_recall'],
                 a['by_missing_count']['3']['sufficient_recall'], b['by_missing_count']['3']['sufficient_recall'],
                 a['metrics']['needs_recall'], a['metrics']['sufficient_recall']]
        except (KeyError, TypeError): return False
        if not all(type(x) in (float, int) and np.isfinite(x) for x in v): return False
        if not (v[0] > v[1] and v[2] >= v[3] and v[4] > v[5] and v[6] > v[7] and v[8] > .5 and v[9] > .5): return False
    return True


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, parent_sha256=PARENT_SHA, seeds=SEEDS, arms=ARMS,
        model_schema=MODEL_SCHEMA, representation=REPRESENTATION,
        changed='coefficient of TRAIN proper-internal 3-class CE only:0 versus1',
        inference='unchanged original C179 TREE_LINKS with DIRECT fact readout;no auxiliary head or teacher',
        target_classes=CLASSES, target_nodes='two proper binary nodes;exclude root and leaves',
        teacher='read-once partial Boolean semantics from TRAIN visible facts;no hidden assignment',
        parameters=PARAMETERS, inference_parameters=INFERENCE_PARAMETERS, auxiliary_parameters=195,
        inference_dense_macs_per_row=177596, training_forward_dense_macs_per_row=177980,
        steps=STEPS, batch=BATCH, lr=.001, optimizer='Adam', betas=[.9,.999], eps=1e-8,
        weight_decay=0, amsgrad=False, foreach=False, row_rng='seed+1000000',
        loss='mean main CE + alpha*mean CE over two proper nodes;unweighted classes;alpha0 or1',
        device='cpu', dtype='float32', threads=2, deterministic_algorithms=True,
        data_sha256='eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65',
        train_rows=42444, pilot_rows=9396, train_groups=36, pilot_groups=4,
        teacher_rows=42444, unique_teacher_targets=84888, teacher_nonroot_node_evaluations=254664,
        pilot_teacher_targets=0, root_teacher_targets=0, leaf_teacher_targets=0,
        updates=12000, sampled_rows=3072000, training_cell_calls=84000, auxiliary_forward_calls=12000,
        auxiliary_target_uses_both_arms=6144000, active_auxiliary_target_uses=3072000,
        pilot_predictions=56376, training_predictions=254664, inference_batches=312,
        inference_cell_calls=2184, inference_auxiliary_calls=0,
        evaluation='all six FINAL checkpoints saved/restored before scores;raw main argmax',
        gate='each seed internal improves mixed-countBA,count1NEEDS,count3SUFFICIENT;groupmacro nondecline;both aggregate recalls>0.5',
        secondary='both split main logits/confusion/order/exchanges;not replacement gates',
        old_checkpoint_loads=0, new_checkpoint_loads=6, actual_acquisitions=0,
        proof_checker_calls=0, evidence_writes=0, network_calls=0,
        scope='fixed development supervision intervention,not proof of a unique credit-assignment cause or Gate E')


def precheck(c180_summary, c179_summary, c178_summary, c177_summary, c176_summary, c174_summary, root):
    from fold_lm.v05_benchmarks import gate_e_c180_fact_bypass as previous
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    p174, pins, protected = previous.precheck(c179_summary, c178_summary, c177_summary, c176_summary, c174_summary, root)
    require(audit.sha(c180_summary) == PARENT_SHA, 'C180 summary hash mismatch')
    p = audit.read_json(c180_summary)
    require(p['experiment_id'] == previous.EXPERIMENT_ID and p['commit_sha'] == BASE
            and p['diagnostic_execution_valid'] is True and p['status'] == 'FAIL'
            and not previous.gate(p['pairs']) and p['source_blobs'] == pins, 'Wrong accepted C180 negative')
    expected = {'fact-bypass-plan.json', 'readout-mask-audit.json', 'pilot-predictions.json', 'training-predictions.npz'}
    expected |= {f'probe-{s}-{a}.pt' for s in previous.SEEDS for a in previous.ARMS}
    require(len(p['artifacts']) == 10 and {a['file'] for a in p['artifacts']} == expected, 'C180 artifact set drift')
    protected[str(Path(c180_summary).resolve())] = PARENT_SHA
    for a in p['artifacts']:
        f = audit.safe_child(Path(c180_summary).resolve().parent, a['file'])
        require(f.is_file() and f.stat().st_size == a['serialized_bytes'] and audit.sha(f) == a['sha256'],
                'Changed C180 artifact:'+a['file'])
        protected[str(f.resolve())] = a['sha256']
    pins = dict(pins)
    for name in previous.OWN: pins[name] = audit.git(root, 'rev-parse', BASE+':'+name).decode().strip()
    allpins = dict(pins)
    for name in OWN: allpins[name] = audit.git(root, 'rev-parse', 'HEAD:'+name).decode().strip()
    protected.update(audit.protect_tree_files(root, allpins))
    require(len(pins) == 72 and len(protected) == 135, 'Source/input union drift')
    require(hashlib.sha256(blob(manifest())).hexdigest() == MANIFEST_SHA, 'Manifest drift')
    return p174, pins, protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c180_fact_bypass as previous
    names = previous.regression_modules(root)
    require(len(names) == len(set(names)) == 64, 'Historical regression list drift')
    return names+['tests_lm.test_v05_c181_internal_semantics']


def validate_result(p):
    require(p['experiment_id'] == EXPERIMENT_ID and p['stage'] == STAGE
            and p['diagnostic_execution_valid'] is True, 'Wrong/incomplete result')
    expected = dict(trained_models=6, fresh_seeds=3, parameters_per_model=25921, inference_parameters=25726,
        training_steps_total=12000, training_examples_drawn=3072000, training_forward_calls=12000,
        training_cell_calls=84000, auxiliary_forward_calls=12000, auxiliary_target_uses=6144000,
        active_auxiliary_target_uses=3072000, teacher_rows=42444, teacher_targets=84888,
        teacher_nonroot_node_evaluations=254664, pilot_teacher_targets=0, inference_auxiliary_calls=0,
        pilot_predictions=56376, training_resubstitution_predictions=254664,
        inference_forward_calls=312, inference_cell_calls=2184,
        historical_checkpoint_deserializations=0, new_checkpoint_deserializations=6,
        actual_acquisitions=0, proof_checker_calls=0, evidence_writes=0, network_calls=0)
    require(all(p[k] == v for k,v in expected.items()), 'Workload drift')
    require(p['production_runtime_modified'] is False and p['gate_e_candidate'] is False, 'Scope drift')
    fits = p['fit_records']
    require([(f['seed'],f['arm']) for f in fits] == [(s,a) for s in SEEDS for a in ARMS], 'Missing/reordered fits')
    require(all(f['steps'] == 2000 and f['examples_drawn'] == 512000 and f['parameters'] == PARAMETERS for f in fits), 'Fit drift')
    for i in (0,2,4):
        require(fits[i]['initial_sha256'] == fits[i+1]['initial_sha256'] and
                fits[i]['batch_schedule_sha256'] == fits[i+1]['batch_schedule_sha256'], 'Unpaired fits')
    require(len(p['source_blobs']) == 72 and len(p['input_sha256']) == 135, 'Source coverage drift')
    require(('PASS' if gate(p['pairs']) else 'FAIL') == p['status'], 'Result disagrees with fixed gate')


def run(*, c180_summary, c179_summary, c178_summary, c177_summary, c176_summary, c174_summary,
        output_dir, expected_head):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as order
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,'rev-parse','HEAD').decode().strip() == expected_head, 'HEAD mismatch')
        require(audit.git(root,'branch','--show-current').decode().strip() == 'feat/sft-target-loss', 'Branch mismatch')
        require(not audit.git(root,'status','--porcelain','--untracked-files=no').strip(), 'Tracked tree dirty')
    args = (c180_summary,c179_summary,c178_summary,c177_summary,c176_summary,c174_summary,root)
    guard(); p174,pins,protected = precheck(*args)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter(); artifacts=[]; fits=[]; pairs=[]; inference=[]
    def record(name):
        f=out/name; artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,value): (out/name).write_bytes(blob(value)); record(name)
    save('internal-semantics-plan.json',dict(manifest(),source_blobs=pins))
    try:
        print('[C181] plan fixed; TRAIN proper-node teacher only; unchanged main inference',flush=True)
        torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
        data,_=audit.load_data(Path(c174_summary).resolve().parent,p174)
        train,ev=data['split_codes']==0,data['split_codes']==1
        require((int(train.sum()),int(ev.sum()),len(train)) == (42444,9396,51840), 'Split drift')
        raw=torch.from_numpy(data['features']); rawhash=graph.tensor_sha(raw)
        x=binding.prepare_pair(raw)[1]; xhash=graph.tensor_sha(x); xt=x[train]
        # Never call this generator on PILOT data. No root evaluation or root target.
        ix,targets=teacher_targets(raw[train])
        require(torch.equal(ix,proper_indices(xt)), 'Teacher/neural node alignment mismatch')
        th=graph.tensor_sha(targets)
        np.savez_compressed(out/'teacher-targets.npz',row_indices=np.flatnonzero(train).astype('<i4'),
            node_indices=ix.numpy().astype(np.int8),targets=targets.numpy().astype(np.int8))
        record('teacher-targets.npz')
        save('teacher-audit.json',dict(rows=42444,targets=84888,nonroot_nodes_evaluated=254664,
            raw_tensor_sha256=rawhash,common_input_sha256=xhash,target_sha256=th,
            target_classes=CLASSES,class_counts=np.bincount(targets.numpy().reshape(-1),minlength=3).tolist(),
            root_targets=0,leaf_targets=0,pilot_targets=0,hidden_value_reads=0))
        y=torch.from_numpy(data['labels'][train].copy()); models={}
        for seed in SEEDS:
            for arm,initial in zip(ARMS,paired_initial(seed),strict=True):
                def progress(r,seed=seed,arm=arm):
                    print(f"[C181] seed={seed} arm={arm} step={r['step']}/2000 main_loss={r['main_loss']:.6f} aux_loss={r['auxiliary_loss']:.6f}",flush=True)
                model,history=fit(initial,xt,y,targets,seed,progress=progress)
                name=f'probe-{seed}-{arm}.pt'; torch.save(checkpoint_payload(model,seed),out/name)
                restored=restore(out/name,seed,arm); record(name)
                require(graph.fingerprint(restored)==graph.fingerprint(model),'Checkpoint roundtrip drift')
                fits.append(dict(seed=seed,arm=arm,initial_sha256=graph.fingerprint(initial),
                    final_sha256=graph.fingerprint(restored),parameters=PARAMETERS,**history))
                models[seed,arm]=restored
        require(len(fits)==6,'Incomplete fits')
        # All final models saved/restored before any main TRAIN or PILOT scores.
        pilot=[];tpred=[];tlogit=[];training=[];exchanges=[];missing=order.missing_counts(data['features'])
        for seed in SEEDS:
            scores=[]; full=[]
            for arm in ARMS:
                p,z,meter=predict(models[seed,arm],x[ev]);tp,tz,tm=predict(models[seed,arm],xt)
                inference.extend([dict(seed=seed,arm=arm,split='PILOT_EVAL',**meter),dict(seed=seed,arm=arm,split='TRAIN_RESUBSTITUTION',**tm)])
                scores.append(binding.score(data,p.numpy(),z.numpy(),ev,audit,order))
                training.append(dict(seed=seed,arm=arm,**binding.score(data,tp.numpy(),tz.numpy(),train,audit,order)))
                pilot.append(dict(seed=seed,arm=arm,representation=REPRESENTATION,model_schema=MODEL_SCHEMA,
                    row_indices=np.flatnonzero(ev).tolist(),predictions=p.tolist(),logits=z.tolist()))
                tpred.append(tp.numpy().astype(np.int8));tlogit.append(tz.numpy())
                q=np.empty(51840,dtype=np.int8);q[ev]=p.numpy();q[train]=tp.numpy();full.append(q)
            pair=dict(seed=seed,final_only=scores[0],internal=scores[1],
                paired_initial_equal=fits[2*(seed-SEEDS[0])]['initial_sha256']==fits[2*(seed-SEEDS[0])+1]['initial_sha256'],
                paired_batches_equal=fits[2*(seed-SEEDS[0])]['batch_schedule_sha256']==fits[2*(seed-SEEDS[0])+1]['batch_schedule_sha256'])
            pairs.append(pair); parts={}
            for mask,name in ((train,'TRAIN_RESUBSTITUTION'),(ev,'PILOT_EVAL')):
                parts[name]=dict(overall=order.transitions(data['labels'][mask],full[0][mask],full[1][mask]),
                    by_missing_count={str(k):order.transitions(data['labels'][mask&(missing==k)],full[0][mask&(missing==k)],full[1][mask&(missing==k)]) for k in range(5)})
            exchanges.append(dict(seed=seed,parts=parts))
            print(f"[C181] seed={seed} mixed_count_BA final_only={scores[0]['macro_missing_balanced_accuracy']:.6f} internal={scores[1]['macro_missing_balanced_accuracy']:.6f}",flush=True)
        save('pilot-predictions.json',pilot)
        np.savez_compressed(out/'training-predictions.npz',row_indices=np.flatnonzero(train).astype('<i4'),
            predictions=np.stack(tpred),logits=np.stack(tlogit),seeds=np.repeat(np.array(SEEDS,dtype='<i4'),2),
            arm_indices=np.tile(np.arange(2,dtype=np.int8),3));record('training-predictions.npz')
        guard();precheck(*args)
        require(graph.tensor_sha(raw)==rawhash and graph.tensor_sha(x)==xhash and graph.tensor_sha(targets)==th,'Input/teacher changed')
        for name,h in protected.items():require(audit.sha(name)==h,'Protected input changed:'+name)
        for a in artifacts:require(audit.sha(out/a['file'])==a['sha256'],'Output changed')
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status='PASS' if gate(pairs) else 'FAIL',
            diagnostic_execution_valid=True,C180_summary_sha256=PARENT_SHA,C174_summary_sha256=audit.PARENT_SHA,
            data_content_sha256=audit.DATA_SHA,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
            pairs=pairs,fit_records=fits,training_metrics=training,error_exchanges=exchanges,inference_records=inference,
            trained_models=6,fresh_seeds=3,parameters_per_model=PARAMETERS,inference_parameters=INFERENCE_PARAMETERS,
            training_steps_total=sum(f['steps'] for f in fits),training_examples_drawn=sum(f['examples_drawn'] for f in fits),
            training_forward_calls=sum(f['training_forward_calls'] for f in fits),training_cell_calls=sum(f['training_cell_calls'] for f in fits),
            auxiliary_forward_calls=sum(f['auxiliary_forward_calls'] for f in fits),auxiliary_target_uses=sum(f['auxiliary_target_uses'] for f in fits),
            active_auxiliary_target_uses=sum(f['auxiliary_target_uses'] for f in fits if f['arm']==ARMS[1]),
            teacher_rows=len(targets),teacher_targets=targets.numel(),teacher_nonroot_node_evaluations=6*len(targets),
            pilot_teacher_targets=0,inference_auxiliary_calls=sum(m.auxiliary_calls for m in models.values()),
            inference_forward_calls=sum(r['forward_calls'] for r in inference),inference_cell_calls=sum(r['cell_calls'] for r in inference),
            pilot_predictions=56376,training_resubstitution_predictions=254664,
            inference_dense_macs_per_row=177596,training_forward_dense_macs_per_row=177980,
            prepared_rows=51840,leaf_fact_reads=207360,copied_numeric_fields=414720,
            historical_checkpoint_deserializations=0,new_checkpoint_deserializations=6,
            actual_acquisitions=0,proof_checker_calls=0,evidence_writes=0,network_calls=0,
            production_runtime_modified=False,gate_e_candidate=False,
            environment=dict(torch=torch.__version__,numpy=np.__version__,device='cpu',dtype='float32',threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['TRAIN teacher is hand-coded partial Boolean semantics,not a learned solver',
                'no hidden values/root targets/teacher-forced states;auxiliary head absent from inference',
                'extra TRAIN supervision changes optimization/regularization;not a unique credit-assignment proof',
                'both arms use unadopted C179tree/C178binding as common substrate;C180mask not adopted',
                'same four reused development groups;not independent generalization or Gate E',
                'equal nominal head count/forward work;zero-weight control has inactive auxiliary gradients'])
        validate_result(result)
        (out/'summary.json').write_bytes(blob(result));print('=== C181 RESULT ===',flush=True);print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/'invalid.json').write_bytes(blob(dict(experiment_id=EXPERIMENT_ID,status='INVALID',
            diagnostic_execution_valid=False,error=str(exc),completed_fits=fits,completed_pairs=pairs)))
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('c180-summary','c179-summary','c178-summary','c177-summary','c176-summary','c174-summary','output-dir'):
        p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--expected-head',required=True);run(**vars(p.parse_args()))


if __name__ == '__main__':
    main()
