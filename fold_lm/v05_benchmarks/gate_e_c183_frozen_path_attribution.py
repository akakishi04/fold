"""C183: frozen activation-interchange localization of C182 naming failures.

Diagnostic counterfactual readouts are NOT legal complete problem inputs and are
never deployed, repaired, ensembled or substituted for C182 decisions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import torch
from torch import nn

EXPERIMENT_ID = 'C183-v5e-frozen-renaming-path-attribution'
STAGE = 'V5-E-FROZEN-RENAMING-PATH-ATTRIBUTION'
BASE = '8ee4942d7b4ec73ac65de8d6f17f59c297c6ee99'
PARENT_SHA = '06c00df5ee0bbafd8b908d038b68be00667e42597f8959ba3d3a431d87e03f73'
SEEDS = (181001, 181002, 181003)
ARMS = ('FINAL_ONLY', 'INTERNAL_SEMANTICS')
MODES = ('ORIGINAL', 'RENAMED', 'TREE_ONLY', 'DIRECT_ONLY')
PERMUTATION_INDEX = 17
PERMUTATION = (2, 3, 1, 0)
BATCH = 1024
REPLAY_ATOL = 1e-6
OWN = ('fold_lm/v05_benchmarks/gate_e_c183_frozen_path_attribution.py',
       'tests_lm/test_v05_c183_frozen_path_attribution.py', 'tools/run_c183.ps1',
       'docs/experiment-ledger-addendum-c183-preregistration.md')
OUTPUTS = {'path-attribution-plan.json', 'source-audit.json', 'replay.json',
           'path-results.json', 'counterexamples.json', 'path-predictions.npz'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


def check_readouts(original, renamed):
    require(isinstance(original, torch.Tensor) and isinstance(renamed, torch.Tensor)
            and original.device.type == renamed.device.type == 'cpu'
            and original.dtype == renamed.dtype == torch.float32
            and original.ndim == 2 and original.shape[1] == 94
            and original.shape == renamed.shape and len(original) > 0
            and torch.isfinite(original).all().item() and torch.isfinite(renamed).all().item(),
            'Finite paired CPUfloat32 readout inputs [N,94] required')
    # Only root64 and the direct fact table16 may differ after coherent renaming.
    require(torch.equal(original[:,64:68], renamed[:,64:68])
            and torch.equal(original[:,84:], renamed[:,84:]), 'Header/resource context changed')


def hybrid_inputs(original, renamed):
    """Interchange two actual activations; no labels, solver or learned changes."""
    check_readouts(original, renamed)
    tree = original.clone(); tree[:,:64] = renamed[:,:64]
    direct = original.clone(); direct[:,68:84] = renamed[:,68:84]
    return tree, direct


def capture_predict(model, x, predictor):
    """Observe original readout arguments, without editing main forward outputs."""
    require(type(model.readout) is nn.Linear and model.readout.in_features == 94
            and model.readout.out_features == 2 and not model.readout._forward_pre_hooks,
            'Unmodified original Linear94->2 readout required')
    inputs = []
    handle = model.readout.register_forward_pre_hook(
        lambda module, args: inputs.append(args[0].detach().clone()))
    try:
        pred, logits, meter = predictor(model, x, batch=BATCH)
    finally:
        handle.remove()
    require(len(inputs) == (len(x)+BATCH-1)//BATCH, 'Readout capture count drift')
    h = torch.cat(inputs)
    check_readouts(h, h)
    require(len(h) == len(x), 'Readout capture row drift')
    return pred, logits, h, meter


def head_predict(head, h):
    check_readouts(h, h)
    require(type(head) is nn.Linear and head.weight.shape == (2,94)
            and head.weight.dtype == torch.float32 and head.weight.device.type == 'cpu',
            'Original CPUfloat32 output head required')
    out = []
    with torch.inference_mode():
        for lo in range(0,len(h),BATCH):
            out.append(head(h[lo:lo+BATCH]))
    z = torch.cat(out)
    require(torch.isfinite(z).all().item(), 'Nonfinite counterfactual logits')
    return z.argmax(1), z, (len(h)+BATCH-1)//BATCH


def failure_mode(label, original, renamed, tree, direct):
    require(all(type(v) is int and v in (0,1) for v in (label,original,renamed,tree,direct)),
            'Integer binary decisions required')
    require(original == label and renamed != label, 'An actual coherent renaming failure is required')
    a, b = tree != label, direct != label
    return ('EITHER_ALONE' if a and b else 'TREE_ONLY_SUFFICIENT' if a
            else 'DIRECT_ONLY_SUFFICIENT' if b else 'JOINT_REQUIRED')


def gate(cases):
    # Complete accepted failure set only. Never trust a stored classification label.
    if not isinstance(cases, list) or len(cases) != 1:
        return False
    c = cases[0]
    if c.get('seed') != 181003 or c.get('permutation_index') != PERMUTATION_INDEX:
        return False
    try:
        mode = failure_mode(c['label'], *(c['decisions'][k] for k in MODES))
    except (KeyError, TypeError, ValueError):
        return False
    return c.get('mode') == mode and mode in ('TREE_ONLY_SUFFICIENT','DIRECT_ONLY_SUFFICIENT')


def describe_row(row):
    """Render supplied syntax and visible facts; do not evaluate any operator."""
    r = np.asarray(row)
    require(r.shape == (72,) and r.dtype.kind in 'iu' and r[:2].tolist() == [7,4], 'Raw row required')
    terms = []
    for active, kind, fact, left, right, neg in r[4:46].reshape(7,6).tolist():
        require(active == 1 and kind in (1,2,3), 'Invalid syntax')
        if kind == 1:
            require(1 <= fact <= 4 and left == right == 0 and neg in (0,1), 'Invalid leaf')
            terms.append(('NOT ' if neg else '')+f'F{fact}')
        else:
            require(1 <= left <= len(terms) and 1 <= right <= len(terms), 'Invalid child')
            terms.append(f'({terms[left-1]} {"AND" if kind == 2 else "OR"} {terms[right-1]})')
    facts = []
    for i,(active,status,present,value) in enumerate(r[46:62].reshape(4,4).tolist(),1):
        require(active == 1 and status in (1,2) and present == int(status == 2)
                and value in (0,1) and (present or value == 0), 'Invalid visible fact')
        facts.append(dict(fact=i, observed=bool(present), value=value if present else None))
    return dict(expression=terms[-1], facts=facts)


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,parent_sha256=PARENT_SHA,
        source_execution_head=BASE,source_seeds=SEEDS,arms=ARMS,modes=MODES,
        permutation_index=PERMUTATION_INDEX,old_to_new=PERMUTATION,
        question='Does exactly one isolated route reproduce each observed C182 candidate flip?',
        intervention='interchange actual root64 or direct facts16 at frozen final Linear94->2',
        input_scope='all9396source pilot rows at identity and sole failed permutation17;all6models',
        selection='outcome-conditioned complete candidate failure permutation set;not independent evaluation',
        saved_predictions_audited=1296648,main_forward_rows=112752,
        main_forward_batches=120,main_cell_calls=840,counterfactual_readout_rows=112752,
        counterfactual_readout_batches=120,total_output_decisions=225504,
        checkpoint_loads=6,training=0,fresh_seeds=0,teacher_calls=0,auxiliary_calls=0,
        replay_atol=REPLAY_ATOL,replay_rtol=0,batch=BATCH,threads=2,device='cpu',dtype='float32',
        gate='all actual candidate failures have exactly one sufficient isolated route;joint/either => VALID NEGATIVE',
        limits='local frozen activation diagnostic;hybrids not valid full inputs;no C182 rescue or adoption',
        outputs=sorted(OUTPUTS))


MANIFEST_SHA = 'e4152fd486ccbe0c03c48c6bcf3dcc154ca41b03b079c24dee14d78f070a49f3'


def precheck(c182_summary,c181_summary,c180_summary,c179_summary,c178_summary,
             c177_summary,c176_summary,c174_summary,root):
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as prev
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    p181,p174,pins,protected=prev.precheck(c181_summary,c180_summary,c179_summary,c178_summary,
                                         c177_summary,c176_summary,c174_summary,root)
    require(audit.sha(c182_summary)==PARENT_SHA,'C182 summary hash mismatch')
    p182=audit.read_json(c182_summary);prev.validate_result(p182)
    require(p182['commit_sha']==BASE and p182['status']=='FAIL' and p182['source_blobs']==pins,
            'Wrong accepted C182 negative')
    failures=[r for r in p182['records'] if r['arm']==ARMS[1] and r['errors']]
    require(failures==[dict(seed=181003,arm=ARMS[1],permutation_index=17,n=9396,errors=1,decision_flips=1)],
            'Accepted candidate failure set changed')
    protected[str(Path(c182_summary).resolve())]=PARENT_SHA
    for a in p182['artifacts']:
        f=audit.safe_child(Path(c182_summary).resolve().parent,a['file'])
        require(f.is_file() and f.stat().st_size==a['serialized_bytes'] and audit.sha(f)==a['sha256'],
                'C182 artifact changed:'+a['file'])
        protected[str(f.resolve())]=a['sha256']
    pins=dict(pins)
    for name in prev.OWN:pins[name]=audit.git(root,'rev-parse',BASE+':'+name).decode().strip()
    allpins=dict(pins)
    for name in OWN:allpins[name]=audit.git(root,'rev-parse','HEAD:'+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins)==80 and len(protected)==161,'Source/input union drift')
    require(hashlib.sha256(blob(manifest())).hexdigest()==MANIFEST_SHA,'Manifest drift')
    return p182,p181,p174,pins,protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as prev
    names=prev.regression_modules(root)
    require(len(names)==len(set(names))==66,'Historical regression list drift')
    return names+['tests_lm.test_v05_c183_frozen_path_attribution']


def validate_result(p):
    require(p['experiment_id']==EXPERIMENT_ID and p['stage']==STAGE
            and p['diagnostic_execution_valid'] is True,'Wrong/incomplete result')
    wanted=dict(saved_predictions_audited=1296648,main_forward_rows=112752,
        main_forward_batches=120,main_cell_calls=840,counterfactual_readout_rows=112752,
        counterfactual_readout_batches=120,total_output_decisions=225504,checkpoint_loads=6,
        new_training=0,fresh_seeds=0,teacher_calls=0,auxiliary_forward_calls=0,
        actual_acquisitions=0,proof_checker_calls=0,evidence_writes=0,network_calls=0)
    require(all(p[k]==v for k,v in wanted.items()),'Workload drift')
    require(len(p['source_blobs'])==80 and len(p['input_sha256'])==161
            and len(p['artifacts'])==6 and {a['file'] for a in p['artifacts']}==OUTPUTS,'Protection/output drift')
    require(len(p['replay'])==12 and len(p['model_records'])==6
            and p['production_runtime_modified'] is False and p['gate_e_candidate'] is False,'Scope drift')
    require(p['status']==('PASS' if gate(p['failure_cases']) else 'FAIL'),'Fixed gate mismatch')


def run(*,c182_summary,c181_summary,c180_summary,c179_summary,c178_summary,c177_summary,
        c176_summary,c174_summary,output_dir,expected_head):
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as prev
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c177_frozen_score_order as order
    graph=prev.graph;root=Path(__file__).resolve().parents[2]
    args=(c182_summary,c181_summary,c180_summary,c179_summary,c178_summary,c177_summary,c176_summary,c174_summary,root)
    def guard():
        require(audit.git(root,'rev-parse','HEAD').decode().strip()==expected_head,'HEAD mismatch')
        require(audit.git(root,'branch','--show-current').decode().strip()=='feat/sft-target-loss','Branch mismatch')
        require(not audit.git(root,'status','--porcelain','--untracked-files=no').strip(),'Tracked tree dirty')
    guard();p182,p181,p174,pins,protected=precheck(*args)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    artifacts=[];replay=[];cases=[];records=[];started=time.perf_counter()
    def save(name,v):
        (out/name).write_bytes(blob(v));record(name)
    def record(name):
        f=out/name;artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    save('path-attribution-plan.json',dict(manifest(),source_blobs=pins))
    try:
        print('[C183] plan fixed; frozen two-route activation interchange; no training or rescue',flush=True)
        torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
        data,metadata=audit.load_data(Path(c174_summary).resolve().parent,p174)
        ev=data['split_codes']==1;indices=np.flatnonzero(ev);y=data['labels'][ev]
        raw=torch.from_numpy(data['features'][ev].copy());rh=graph.tensor_sha(raw)
        changed=prev.rename_raw(raw,PERMUTATION)
        x0=binding.prepare_pair(raw)[1];x1=binding.prepare_pair(changed)[1]
        hashes=[graph.tensor_sha(z) for z in (x0,x1,changed)]
        old=audit.read_json(Path(c181_summary).resolve().parent/'pilot-predictions.json')
        saved=audit.load_npz(Path(c182_summary).resolve().parent/'renamed-predictions.npz')
        require(set(saved)=={'row_indices','permutations','predictions','logits','seeds','arm_indices'}
            and np.array_equal(saved['row_indices'],indices)
            and np.array_equal(saved['permutations'],np.asarray(prev.PERMUTATIONS[1:]))
            and np.array_equal(saved['seeds'],np.repeat(SEEDS,2))
            and np.array_equal(saved['arm_indices'],np.tile([0,1],3)),'Saved row/model mapping drift')
        sp,sz=saved['predictions'],saved['logits']
        require(sp.shape==(6,23,9396) and sz.shape==(6,23,9396,2)
            and sp.dtype==np.int8 and sz.dtype==np.float32 and np.isfinite(sz).all()
            and np.array_equal(sp,sz.argmax(-1)),'Saved prediction schema drift')
        require(len(old)==6,'C181 model coverage drift')
        missing=order.missing_counts(data['features'][ev]);groups=data['groups'][ev]
        details=audit.read_json(Path(c182_summary).resolve().parent/'renaming-results.json')
        require(len(details)==138,'Detailed source coverage drift')
        model_order=[(s,a) for s in SEEDS for a in ARMS]
        for j in range(23):
            for i,(seed,arm) in enumerate(model_order):
                rec=p182['records'][j*6+i];detail=details[j*6+i]
                require((old[i]['seed'],old[i]['arm'])==(seed,arm)
                    and np.array_equal(old[i]['row_indices'],indices),'C181 row/model drift')
                score=prev.summarize(y,sp[i,j],old[i]['predictions'],missing,groups)
                require(rec=={k:detail[k] for k in rec}
                    and detail['old_to_new']==list(prev.PERMUTATIONS[j+1]),'Source detail identity drift')
                audit.same_metrics(score,detail['score'])
                require(score['errors']==rec['errors'] and score['decision_flips']==rec['decision_flips'],'Source count drift')
        failure_positions=np.argwhere(sp[1::2]!=y[None,None,:])
        require(failure_positions.shape==(1,3) and failure_positions[0,:2].tolist()==[2,16],
                'Complete source candidate failure set mismatch')
        fi=int(failure_positions[0,2])
        source_case=dict(source_row=int(indices[fi]),pilot_row=fi,template_index=int(data['template_ids'][ev][fi]),
            semantic_group=int(groups[fi]),missing_count=int(missing[fi]),label=int(y[fi]),
            original=describe_row(raw[fi].numpy()),renamed=describe_row(changed[fi].numpy()))
        require(source_case['semantic_group']==3 and source_case['missing_count']==1 and source_case['label']==1,
                'Counterexample stratum drift')
        save('source-audit.json',dict(saved_predictions_audited=int(sp.size),source_case=source_case,
            source_failure_positions=failure_positions.tolist(),selected_permutations=[17],
            numerical_novelty=False,selection='all C182 candidate failures;outcome-conditioned'))
        print('[C183] 1/3 all1296648 saved decisions audited; one counterexample identified',flush=True)
        zall=[];head_batches=head_rows=base_batches=base_cells=base_rows=0
        for i,(seed,arm) in enumerate(model_order):
            fit=p181['fit_records'][i]
            model=prev.restore_bare(Path(c181_summary).resolve().parent/f'probe-{seed}-{arm}.pt',seed,arm,fit['final_sha256'])
            fp=graph.fingerprint(model)
            p0,z0,h0,m0=capture_predict(model,x0,graph.predict)
            p1,z1,h1,m1=capture_predict(model,x1,graph.predict)
            for tag,p,z,pp,zz,m in (('ORIGINAL',p0,z0,old[i]['predictions'],old[i]['logits'],m0),
                                    ('RENAMED',p1,z1,sp[i,16],sz[i,16],m1)):
                check=prev.replay_check(p.numpy(),z.numpy(),pp,zz)
                replay.append(dict(seed=seed,arm=arm,condition=tag,**check))
                base_batches+=m['forward_calls'];base_cells+=m['cell_calls'];base_rows+=m['rows']
            ht,hd=hybrid_inputs(h0,h1)
            pt,zt,mt=head_predict(model.readout,ht);pd,zd,md=head_predict(model.readout,hd)
            head_batches+=mt+md;head_rows+=len(pt)+len(pd)
            zz=torch.stack((z0,z1,zt,zd));pp=zz.argmax(-1).numpy();zall.append(zz.numpy())
            scores={tag:audit.metrics(y,pp[k],groups) for k,tag in enumerate(MODES)}
            row=dict(seed=seed,arm=arm,metrics=scores,
                counterexample_logits=zz[:,fi].tolist(),counterexample_predictions=pp[:,fi].tolist())
            records.append(row)
            if arm==ARMS[1] and (sp[i,16]!=y).any():
                for ix in np.flatnonzero(sp[i,16]!=y):
                    decisions=[int(v) for v in pp[:,ix]]
                    mode=failure_mode(int(y[ix]),*decisions)
                    margins=[float(zz[k,ix,1].double()-zz[k,ix,0].double()) for k in range(4)]
                    case=dict(seed=seed,arm=arm,permutation_index=17,old_to_new=PERMUTATION,
                        source_row=int(indices[ix]),pilot_row=int(ix),label=int(y[ix]),mode=mode,
                        decisions=dict(zip(MODES,decisions)),logits=dict(zip(MODES,zz[:,ix].tolist())),
                        needs_margins=dict(zip(MODES,margins)),
                        additive_margin_residual=margins[1]-margins[2]-margins[3]+margins[0],
                        input=source_case)
                    cases.append(case)
                    print(f'[C183] seed={seed} row={indices[ix]} path_mode={mode} margins={margins}',flush=True)
            require(graph.fingerprint(model)==fp and all(not p.requires_grad for p in model.parameters()),'Frozen model changed')
            require(not model.readout._forward_pre_hooks,'Capture hook leaked')
            print(f'[C183] model={i+1}/6 identity/renamed replay and two isolated readouts complete',flush=True)
        save('replay.json',replay);save('path-results.json',records);save('counterexamples.json',cases)
        zall=np.stack(zall).astype(np.float32)
        np.savez_compressed(out/'path-predictions.npz',row_indices=indices.astype('<i4'),logits=zall,
            predictions=zall.argmax(-1).astype(np.int8),seeds=np.repeat(np.asarray(SEEDS,dtype='<i4'),2),
            arm_indices=np.tile(np.asarray([0,1],dtype=np.int8),3),mode_indices=np.arange(4,dtype=np.int8))
        record('path-predictions.npz')
        require(graph.tensor_sha(raw)==rh and [graph.tensor_sha(z) for z in (x0,x1,changed)]==hashes,'Input mutation')
        guard();precheck(*args)
        for f,h in protected.items():require(audit.sha(f)==h,'Protected input changed:'+f)
        for a in artifacts:require(audit.sha(out/a['file'])==a['sha256'],'Output changed')
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status='PASS' if gate(cases) else 'FAIL',diagnostic_execution_valid=True,
            C182_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
            failure_cases=cases,model_records=records,replay=replay,saved_predictions_audited=int(sp.size),
            main_forward_rows=base_rows,main_forward_batches=base_batches,main_cell_calls=base_cells,
            counterfactual_readout_rows=head_rows,counterfactual_readout_batches=head_batches,
            total_output_decisions=int(zall.shape[0]*zall.shape[1]*zall.shape[2]),checkpoint_loads=6,
            new_training=0,fresh_seeds=0,teacher_calls=0,auxiliary_forward_calls=0,
            actual_acquisitions=0,proof_checker_calls=0,evidence_writes=0,network_calls=0,
            production_runtime_modified=False,gate_e_candidate=False,
            environment=dict(torch=torch.__version__,numpy=np.__version__,device='cpu',dtype='float32',threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=['outcome-conditioned frozen localization,not generalization',
                'hybrid readout states are deliberate internal counterfactuals,not valid complete task inputs',
                'unique isolated-route sufficiency is local to frozen states,not a universal causal mechanism',
                'C182 remains VALID NEGATIVE;no corrected policy or checkpoint is produced'])
        validate_result(result);(out/'summary.json').write_bytes(blob(result))
        print('[C183] 3/3 frozen inputs/outputs preserved; C182 decision is not repaired',flush=True)
        print('=== C183 RESULT ===',flush=True);print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/'invalid.json').write_bytes(blob(dict(experiment_id=EXPERIMENT_ID,status='INVALID',
            diagnostic_execution_valid=False,error=str(exc),completed_replay=replay,completed_cases=cases)))
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('c182-summary','c181-summary','c180-summary','c179-summary','c178-summary',
              'c177-summary','c176-summary','c174-summary','output-dir'):
        p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--expected-head',required=True);run(**vars(p.parse_args()))


if __name__=='__main__':
    main()
