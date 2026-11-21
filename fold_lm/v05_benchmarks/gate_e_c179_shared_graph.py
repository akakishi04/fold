"""C179: equal-budget shared neural updates, sequence links versus supplied tree links.

No hand-coded Boolean evaluation, intermediate truth labels, threshold fitting or live policy.
Both arms use C178's visible-field preparation and the same new shared cell seven times.
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

EXPERIMENT_ID = 'C179-v5e-shared-update-graph'
STAGE = 'V5-E-SHARED-UPDATE-GRAPH'
BASE = 'e9ee578a80b63e72a33414b62ba17a0111329ddb'
PARENT_SHA = '19bee9fbb4068d43bcd05378b18e0e87f4b4e50fc73b635b5e69f7d2d30190d8'
SEEDS = (179001, 179002, 179003)
ARMS = ('SEQUENCE_LINKS', 'TREE_LINKS')
MODEL_SCHEMA = 'c179-shared-graph-64-v1'
REPRESENTATION = 'c178-scaled-visible-leaf-binding-v1'
STATE, HIDDEN, STEPS, BATCH = 64, 128, 2000, 256
PARAMETERS, MACS_PER_ROW = 25726, 177596
OWN = ('fold_lm/v05_benchmarks/gate_e_c179_shared_graph.py',
       'tests_lm/test_v05_c179_shared_graph.py', 'tools/run_c179.ps1',
       'docs/experiment-ledger-addendum-c179-preregistration.md')
MANIFEST_SHA = '8e4fce52612b7e01fbd4f9f58ccb3dd8eee1bfbea16dd9d50ef5f39aca712456'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


def fingerprint(model):
    h = hashlib.sha256()
    for name, t in sorted(model.state_dict().items()):
        h.update(name.encode()); h.update(str(tuple(t.shape)).encode())
        h.update(t.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def tensor_sha(x):
    a = x.detach().cpu().contiguous().numpy()
    return hashlib.sha256(str(a.dtype).encode()+str(a.shape).encode()+a.tobytes()).hexdigest()


def tree_links(x):
    """Decode supplied indices only. Never evaluate operators or necessity."""
    require(isinstance(x, torch.Tensor) and x.dtype == torch.float32 and x.device.type == 'cpu'
        and x.ndim == 2 and x.shape[1] == 72 and len(x) > 0 and torch.isfinite(x).all().item(),
        'Finite nonempty CPU float32 bound features required')
    n = x[:, 4:46].reshape(-1, 7, 6)
    require((x[:, :2] == 1).all().item() and (n[:, :, 0] == 1).all().item(), 'Fixed seven-node/four-fact input')
    kinds = (n[:, :, 1]*3).round().to(torch.int64)
    require(((kinds >= 1) & (kinds <= 3)).all().item()
        and torch.equal(n[:, :, 1], kinds.to(torch.float32)/3), 'Noncanonical node kinds')
    leaf = kinds == 1
    require((leaf.sum(1) == 4).all().item(), 'Four leaves required')
    pointers = (n[:, :, 3:5]*7).round().to(torch.int64)
    require(torch.equal(n[:, :, 3:5][~leaf], (pointers.to(torch.float32)/7)[~leaf]), 'Noninteger internal pointers')
    links = torch.where(leaf.unsqueeze(2), torch.zeros_like(pointers), pointers)
    parents = torch.zeros((len(x), 7), dtype=torch.int64)
    for i in range(7):
        for side in range(2):
            ix = links[:, i, side]
            require(((ix >= 0) & (ix <= i)).all().item()
                and (ix[~leaf[:, i]] >= 1).all().item(), 'Forward/out-of-range child link')
            parents.scatter_add_(1, (ix-1).clamp(min=0).unsqueeze(1), (~leaf[:, i]).long().unsqueeze(1))
    require(torch.equal(parents, torch.tensor([1,1,1,1,1,1,0]).expand(len(x),-1)), 'Connected ordered tree required')
    return n, links


class SharedGraphProbe(nn.Module):
    """Common cell and readout; ONLY hidden-state link selection differs by arm.

    The sequential control still sees every node's original numerical syntax fields.
    Cells have unconstrained learned weights; hidden states are not Boolean truth values.
    Counters are diagnostic meters, not model inputs or serialized learned state.
    """
    def __init__(self, arm):
        super().__init__(); require(arm in ARMS, 'Explicit registered arm required')
        self.arm = arm
        self.cell = nn.Sequential(nn.Linear(6+2*STATE, HIDDEN, dtype=torch.float32), nn.ReLU(),
                                  nn.Linear(HIDDEN, STATE, dtype=torch.float32), nn.ReLU())
        self.readout = nn.Linear(STATE+30, 2, dtype=torch.float32)
        self.calls = self.cell_calls = self.rows = 0

    def forward(self, x):
        require(self.arm in ARMS, 'Unregistered routing mode')
        nodes, links = tree_links(x)
        zero = x.new_zeros((len(x), STATE)); states = []; row = torch.arange(len(x))
        self.calls += 1; self.rows += len(x)
        for i in range(7):
            bank = torch.stack([zero]+states, dim=1)
            if self.arm == ARMS[0]:
                left = torch.full((len(x),), i, dtype=torch.int64)
                right = torch.full((len(x),), max(0, i-1), dtype=torch.int64)
            else:
                left, right = links[:, i, 0], links[:, i, 1]
            h = self.cell(torch.cat((nodes[:, i], bank[row, left], bank[row, right]), dim=1))
            states.append(h); self.cell_calls += 1
        context = torch.cat((x[:, :4], x[:, 46:]), dim=1)
        return self.readout(torch.cat((states[-1], context), dim=1))


def paired_initial(seed):
    require(type(seed) is int and 0 <= seed < 2**31, 'Integer initialization seed required')
    torch.manual_seed(seed); a = SharedGraphProbe(ARMS[0]); b = deepcopy(a); b.arm = ARMS[1]
    require(fingerprint(a) == fingerprint(b), 'Unpaired initialization')
    return a, b


def fit(initial, x, y, seed, *, steps=STEPS, batch=BATCH, progress=None):
    require(type(initial) is SharedGraphProbe and type(seed) is int and 0 <= seed < 2**31,
            'Registered model and seed required')
    tree_links(x)
    require(y.shape == (len(x),) and y.dtype == torch.int64 and y.device.type == 'cpu'
        and set(y.tolist()) == {0,1} and type(steps) is int and steps > 0
        and type(batch) is int and batch > 0, 'Typed TRAIN labels and fixed positive workload required')
    model = deepcopy(initial).train(); model.calls = model.cell_calls = model.rows = 0
    before, xb, yb = fingerprint(initial), tensor_sha(x), tensor_sha(y)
    opt = torch.optim.Adam(model.parameters(), lr=.001, betas=(.9,.999), eps=1e-8,
                           weight_decay=0, amsgrad=False, foreach=False)
    rng = torch.Generator(device='cpu').manual_seed(seed+1000000)
    schedule = hashlib.sha256(); history = []; started = time.perf_counter()
    for i in range(steps):
        ids = torch.randint(len(x), (batch,), generator=rng); schedule.update(ids.numpy().tobytes())
        opt.zero_grad(set_to_none=True); loss = nn.functional.cross_entropy(model(x[ids]), y[ids])
        require(torch.isfinite(loss).item(), 'Nonfinite training loss')
        loss.backward()
        require(all(p.grad is not None and torch.isfinite(p.grad).all().item() for p in model.parameters()), 'Invalid gradient')
        opt.step()
        if (i+1)%500 == 0 or i+1 == steps:
            record = dict(step=i+1, training_loss=float(loss.detach())); history.append(record)
            if progress is not None: progress(record)
    require(all(torch.isfinite(p).all().item() for p in model.parameters()), 'Invalid final weight')
    require(fingerprint(initial) == before and tensor_sha(x) == xb and tensor_sha(y) == yb, 'Immutable fit input changed')
    require((model.calls,model.cell_calls,model.rows) == (steps,7*steps,steps*batch), 'Training meter mismatch')
    return model.eval(), dict(steps=steps,examples_drawn=steps*batch,batch_schedule_sha256=schedule.hexdigest(),
        training_log=history,training_forward_calls=model.calls,training_cell_calls=model.cell_calls,
        fit_wall_clock_seconds=time.perf_counter()-started)


def predict(model, x, *, batch=1024):
    require(type(model) is SharedGraphProbe and type(batch) is int and batch > 0, 'Registered model and positive batch required')
    tree_links(x); model.eval(); before = fingerprint(model); old = (model.calls,model.cell_calls,model.rows)
    started = time.perf_counter(); out = []
    with torch.inference_mode():
        for lo in range(0,len(x),batch): out.append(model(x[lo:lo+batch]).cpu())
    z = torch.cat(out); require(torch.isfinite(z).all().item() and fingerprint(model) == before, 'Invalid/mutating inference')
    calls = (len(x)+batch-1)//batch
    require((model.calls-old[0],model.cell_calls-old[1],model.rows-old[2]) == (calls,7*calls,len(x)), 'Inference meter mismatch')
    return z.argmax(1), z, dict(forward_calls=calls,cell_calls=7*calls,rows=len(x),wall_clock_seconds=time.perf_counter()-started)


def restore(path, seed, arm):
    p = torch.load(path, map_location='cpu', weights_only=True)
    require((p['seed'],p['arm'],p['model_schema'],p['representation'],p['steps']) ==
        (seed,arm,MODEL_SCHEMA,REPRESENTATION,STEPS), 'Checkpoint identity/schema mismatch')
    model = SharedGraphProbe(arm); model.load_state_dict(p['state_dict'],strict=True)
    require(fingerprint(model) == p['weight_sha256'], 'Checkpoint fingerprint mismatch')
    return model.eval()


def gate(pairs):
    if [p.get('seed') for p in pairs] != list(SEEDS): return False
    for p in pairs:
        if p.get('paired_initial_equal') is not True or p.get('paired_batches_equal') is not True: return False
        try:
            a,b = p['tree'],p['sequence']
            v = [a['macro_missing_balanced_accuracy'],b['macro_missing_balanced_accuracy'],
                 a['metrics']['macro_group_balanced_accuracy'],b['metrics']['macro_group_balanced_accuracy'],
                 a['by_missing_count']['1']['needs_recall'],b['by_missing_count']['1']['needs_recall'],
                 a['by_missing_count']['3']['sufficient_recall'],b['by_missing_count']['3']['sufficient_recall'],
                 a['metrics']['needs_recall'],a['metrics']['sufficient_recall']]
        except (KeyError,TypeError): return False
        if not all(type(z) in (int,float) and np.isfinite(z) for z in v): return False
        if not (v[0]>v[1] and v[2]>=v[3] and v[4]>v[5] and v[6]>v[7] and v[8]>.5 and v[9]>.5): return False
    return True


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,parent_sha256=PARENT_SHA,seeds=SEEDS,arms=ARMS,
        model_schema=MODEL_SCHEMA,representation=REPRESENTATION,parameters=PARAMETERS,
        shared_cell='134->128ReLU->64ReLU;7 applications per row',readout='root64+context30->2',
        changed='hidden-state links ONLY:previous-two-node states versus supplied AST children/zero leaves',
        input='same C178 bound representation in BOTH arms;all original fields retained;no Boolean evaluation',
        dense_macs_per_row=MACS_PER_ROW,steps=STEPS,batch=BATCH,lr=.001,optimizer='Adam',
        betas=[.9,.999],eps=1e-8,weight_decay=0,amsgrad=False,foreach=False,
        loss='ordinary unweighted cross entropy;only final necessity labels',
        train_rows=42444,pilot_rows=9396,train_groups=36,pilot_groups=4,
        data_sha256='eaae9aef5f64a204fe4d249bccbd437cd42f90172cd6f0eeb91be834b9450c65',
        device='cpu',dtype='float32',threads=2,deterministic_algorithms=True,
        updates=12000,sampled_rows=3072000,training_cell_calls=84000,
        pilot_predictions=56376,training_predictions=254664,inference_batches=312,inference_cell_calls=2184,
        prepared_rows=51840,leaf_fact_reads=207360,copied_fields=414720,
        evaluation='all six final checkpoints saved/reloaded before ANY score;raw argmax',
        gate='EACH seed tree improves mixed-count BA and count1needs/count3sufficient;groupmacro no decline;both aggregate recalls>0.5',
        secondary='both split logits/group/count/AUC/error exchange;not alternative acceptance',
        limits='new shared diagnostic backbone,not FOLD core;equal dense budget within C179,not equal to old flat MLP',
        actual_acquisitions=0,proof_checker_calls=0,evidence_writes=0,network_calls=0)


def precheck(c178_summary,c177_summary,c176_summary,c174_summary,root):
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as old
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    _,p174,pins,protected = old.precheck(c177_summary,c176_summary,c174_summary,root)
    require(audit.sha(c178_summary) == PARENT_SHA,'C178 summary hash mismatch'); p = audit.read_json(c178_summary)
    require(p['experiment_id'] == old.EXPERIMENT_ID and p['commit_sha'] == BASE and p['status'] == 'FAIL'
        and p['diagnostic_execution_valid'] is True and not old.gate(p['pairs']) and p['source_blobs'] == pins,
        'Wrong accepted C178 negative')
    expected = {'leaf-binding-plan.json','input-binding-audit.json','pilot-predictions.json','training-predictions.npz'}
    expected |= {f'probe-{seed}-{arm}.pt' for seed in old.SEEDS for arm in old.ARMS}
    require(len(p['artifacts']) == 10 and {a['file'] for a in p['artifacts']} == expected,'C178 artifact set drift')
    protected[str(Path(c178_summary).resolve())] = PARENT_SHA
    for a in p['artifacts']:
        f = audit.safe_child(Path(c178_summary).resolve().parent,a['file'])
        require(f.is_file() and f.stat().st_size == a['serialized_bytes'] and audit.sha(f) == a['sha256'],'Changed C178 artifact')
        protected[str(f.resolve())] = a['sha256']
    pins = dict(pins)
    for name in old.OWN: pins[name] = audit.git(root,'rev-parse',BASE+':'+name).decode().strip()
    ownpins = dict(pins)
    for name in OWN: ownpins[name] = audit.git(root,'rev-parse','HEAD:'+name).decode().strip()
    protected.update(audit.protect_tree_files(root,ownpins))
    require(len(pins)==64 and len(protected)==105,'Source/input union drift')
    require(hashlib.sha256(blob(manifest())).hexdigest() == MANIFEST_SHA,'Manifest drift')
    return p174,pins,protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as old
    names = old.regression_modules(root)
    require(len(names)==len(set(names))==62,'Historical regression list drift')
    return names+['tests_lm.test_v05_c179_shared_graph']


def run(*,c178_summary,c177_summary,c176_summary,c174_summary,output_dir,expected_head):
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as old
    from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as order
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,'rev-parse','HEAD').decode().strip()==expected_head,'HEAD mismatch')
        require(audit.git(root,'branch','--show-current').decode().strip()=='feat/sft-target-loss','Branch mismatch')
        require(not audit.git(root,'status','--porcelain','--untracked-files=no').strip(),'Tracked tree dirty')
    args=(c178_summary,c177_summary,c176_summary,c174_summary,root)
    guard();p174,pins,protected=precheck(*args)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter();artifacts=[];fits=[];pairs=[]
    def record(name):
        f=out/name;artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,value): (out/name).write_bytes(blob(value));record(name)
    save('shared-graph-plan.json',dict(manifest(),source_blobs=pins))
    try:
        print('[C179] plan fixed; same shared cell and seven updates; only hidden-state links differ',flush=True)
        torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
        data,_=audit.load_data(Path(c174_summary).resolve().parent,p174)
        train,ev=data['split_codes']==0,data['split_codes']==1
        raw=torch.from_numpy(data['features']);rawhash=tensor_sha(raw)
        _,x=old.prepare_pair(raw);tree_links(x);xhash=tensor_sha(x)
        save('shared-input-audit.json',dict(raw_sha256=rawhash,shared_bound_sha256=xhash,
            rows=len(raw),leaf_fact_reads=len(raw)*4,copied_fields=len(raw)*8))
        xt=x[train];y=torch.from_numpy(data['labels'][train].copy());models={}
        for seed in SEEDS:
            initials=paired_initial(seed)
            for arm,initial in zip(ARMS,initials,strict=True):
                require(sum(p.numel() for p in initial.parameters())==PARAMETERS,'Capacity drift')
                def progress(r,seed=seed,arm=arm):
                    print(f"[C179] seed={seed} arm={arm} step={r['step']}/2000 train_loss={r['training_loss']:.6f}",flush=True)
                model,history=fit(initial,xt,y,seed,progress=progress)
                name=f'probe-{seed}-{arm}.pt'
                torch.save(dict(seed=seed,arm=arm,model_schema=MODEL_SCHEMA,representation=REPRESENTATION,
                    steps=STEPS,weight_sha256=fingerprint(model),state_dict=model.state_dict()),out/name)
                restored=restore(out/name,seed,arm);record(name);models[seed,arm]=restored
                fits.append(dict(seed=seed,arm=arm,initial_sha256=fingerprint(initial),
                    final_sha256=fingerprint(restored),parameters=PARAMETERS,**history))
        require(len(fits)==6 and all(f['steps']==STEPS and f['examples_drawn']==512000 for f in fits),'Incomplete fits')
        require(all(fits[i]['initial_sha256']==fits[i+1]['initial_sha256'] and
            fits[i]['batch_schedule_sha256']==fits[i+1]['batch_schedule_sha256'] for i in (0,2,4)),'Unpaired fits')
        # Only now score the six fixed final models. No score-based selection.
        pilot=[];tpred=[];tlogit=[];training=[];exchanges=[];inference=[]
        missing=order.missing_counts(data['features'])
        for seed in SEEDS:
            scores=[];full=[]
            for arm in ARMS:
                p,z,meter=predict(models[seed,arm],x[ev]);tp,tz,tm=predict(models[seed,arm],xt)
                inference.extend([dict(seed=seed,arm=arm,split='PILOT_EVAL',**meter),
                                  dict(seed=seed,arm=arm,split='TRAIN_RESUBSTITUTION',**tm)])
                scores.append(old.score(data,p.numpy(),z.numpy(),ev,audit,order))
                training.append(dict(seed=seed,arm=arm,**old.score(data,tp.numpy(),tz.numpy(),train,audit,order)))
                pilot.append(dict(seed=seed,arm=arm,representation=REPRESENTATION,model_schema=MODEL_SCHEMA,
                    row_indices=np.flatnonzero(ev).tolist(),predictions=p.tolist(),logits=z.tolist()))
                tpred.append(tp.numpy().astype(np.int8));tlogit.append(tz.numpy())
                q=np.empty(51840,dtype=np.int8);q[ev]=p.numpy();q[train]=tp.numpy();full.append(q)
            pairs.append(dict(seed=seed,sequence=scores[0],tree=scores[1],paired_initial_equal=True,paired_batches_equal=True))
            parts={}
            for mask,name in ((train,'TRAIN_RESUBSTITUTION'),(ev,'PILOT_EVAL')):
                parts[name]=dict(overall=order.transitions(data['labels'][mask],full[0][mask],full[1][mask]),
                    by_missing_count={str(k):order.transitions(data['labels'][mask&(missing==k)],full[0][mask&(missing==k)],full[1][mask&(missing==k)]) for k in range(5)})
            exchanges.append(dict(seed=seed,parts=parts))
            print(f"[C179] seed={seed} mixed_count_BA sequence={scores[0]['macro_missing_balanced_accuracy']:.6f} tree={scores[1]['macro_missing_balanced_accuracy']:.6f}",flush=True)
        save('pilot-predictions.json',pilot)
        np.savez_compressed(out/'training-predictions.npz',row_indices=np.flatnonzero(train).astype('<i4'),
            predictions=np.stack(tpred),logits=np.stack(tlogit),
            seeds=np.array([s for s in SEEDS for _ in ARMS],dtype='<i4'),arm_indices=np.tile(np.arange(2,dtype=np.int8),3))
        record('training-predictions.npz')
        require(sum(r['forward_calls'] for r in inference)==312 and sum(r['cell_calls'] for r in inference)==2184,'Inference count mismatch')
        guard();precheck(*args);require(tensor_sha(raw)==rawhash and tensor_sha(x)==xhash,'Shared input mutated')
        for name,h in protected.items():require(audit.sha(name)==h,'Protected input changed:'+name)
        for a in artifacts:require(audit.sha(out/a['file'])==a['sha256'],'Output changed')
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status='PASS' if gate(pairs) else 'FAIL',
            diagnostic_execution_valid=True,C178_summary_sha256=PARENT_SHA,C174_summary_sha256=audit.PARENT_SHA,
            source_blobs=pins,input_sha256=protected,artifacts=artifacts,pairs=pairs,fit_records=fits,
            training_metrics=training,error_exchanges=exchanges,inference_records=inference,
            data_content_sha256=audit.DATA_SHA,trained_models=6,fresh_seeds=3,parameters_per_model=PARAMETERS,
            dense_macs_per_row=MACS_PER_ROW,training_steps_total=12000,training_examples_drawn=3072000,
            training_forward_calls=sum(f['training_forward_calls'] for f in fits),
            training_cell_calls=sum(f['training_cell_calls'] for f in fits),inference_forward_calls=312,inference_cell_calls=2184,
            pilot_predictions=56376,training_resubstitution_predictions=254664,prepared_rows=51840,
            leaf_fact_reads=207360,copied_numeric_fields=414720,new_checkpoint_deserializations=6,historical_checkpoint_deserializations=0,
            actual_acquisitions=0,proof_checker_calls=0,evidence_writes=0,network_calls=0,production_runtime_modified=False,gate_e_candidate=False,
            environment=dict(torch=torch.__version__,numpy=np.__version__,device='cpu',dtype='float32',threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['new diagnostic shared backbone,not deployed FOLD core or live policy',
                'C178 binding used in BOTH arms as a fixed control,not promoted as a proven improvement',
                'handwritten AST routing and visible-fact gathering;learned cell does not execute programmed Boolean rules',
                'same four reused development groups,not independent confirmation',
                'equal parameters/dense cell counts within C179,not an equal-compute comparison to old flat MLP',
                'dense MACs omit validation/gather/activation/backward/optimizer and cannot establish speed'])
        (out/'summary.json').write_bytes(blob(result));print('=== C179 RESULT ===',flush=True);print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/'invalid.json').write_bytes(blob(dict(experiment_id=EXPERIMENT_ID,status='INVALID',diagnostic_execution_valid=False,
            error=str(exc),completed_fits=fits,completed_pairs=pairs)))
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('c178-summary','c177-summary','c176-summary','c174-summary','output-dir'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--expected-head',required=True);run(**vars(p.parse_args()))


if __name__ == '__main__':
    main()
