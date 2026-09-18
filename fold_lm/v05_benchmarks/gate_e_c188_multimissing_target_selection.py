"""C188: learned target selection among multiple missing facts.

Offline diagnostic only. Freeze the three accepted C181 INTERNAL_SEMANTICS bases.
Train only a small shared scorer on TRAIN-only influential-target supervision.
No acquisition/runtime/answer/proof execution in this C number.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import itertools
import json
from pathlib import Path
import time

import numpy as np
import torch
from torch import nn

EXPERIMENT_ID = "C188-v5e-multimissing-target-selection"
STAGE = "V5-E-MULTIMISSING-TARGET-SELECTION"
BASE = "bdbc71ca17a7a6138f54d1188c17ce7dd33dcece"
PARENT_EXECUTION = "bbb79df40f3428f358bec7381cd872efa7845e63"
PARENT_SHA = "910a8a51c70a7ddfd996d99d21bcd9bc362ba568919ed04fb7305071d9142ccd"
BASE_SEEDS = (181001, 181002, 181003)
HEAD_SEEDS = (188001, 188002, 188003)
ARM = "INTERNAL_SEMANTICS"
STEPS, BATCH = 2000, 256
STATE, FACTS, NODES = 64, 4, 7
FEATURES = NODES * STATE + NODES
HIDDEN = 64
HEAD_PARAMETERS = FEATURES * HIDDEN + HIDDEN + HIDDEN + 1
PARENTS = ("c187","c186","c185","c184","c183","c182","c181","c180","c179",
           "c178","c177","c176","c174")
OWN = ("fold_lm/v05_benchmarks/gate_e_c188_multimissing_target_selection.py",
       "tests_lm/test_v05_c188_multimissing_target_selection.py",
       "tools/run_c188.ps1",
       "docs/experiment-ledger-addendum-c188-preregistration.md")
OUTPUTS = {"target-selection-plan.json","target-teacher.npz","frequency-reference.json",
           "selector-results.json","pilot-predictions.npz"} | {
               f"selector-{b}-{h}.pt" for b in BASE_SEEDS for h in HEAD_SEEDS}
BITS = tuple(itertools.product((0,1), repeat=4))
ATOL = 1e-6
EXPECTED_TESTS = 1413

EXPECTED = {
    "train_discriminating": 3824,
    "train_m2": 2696,
    "train_m3": 1128,
    "train_m3_valid1": 440,
    "train_m3_valid2": 688,
    "eval_discriminating": 528,
    "eval_m2": 376,
    "eval_m3": 152,
    "eval_m3_valid1": 72,
    "eval_m3_valid2": 80,
    "eval_full_multimissing": 1768,
    "frequency_m2_hits": 268,
    "frequency_m3_hits": 128,
    "first_m2_hits": 188,
    "first_m3_hits": 84,
    "frequency_keys": 32,
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()

def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()

def tensor_sha(x):
    require(isinstance(x, torch.Tensor) and x.device.type == "cpu", "CPU tensor required")
    a = x.detach().contiguous().numpy()
    return hashlib.sha256(str(a.dtype).encode()+str(a.shape).encode()+a.tobytes()).hexdigest()

def missing_mask(raw):
    require(isinstance(raw, torch.Tensor) and raw.dtype == torch.int32 and raw.device.type == "cpu"
            and raw.ndim == 2 and raw.shape[1] == 72 and len(raw) > 0,
            "Canonical int32 [N,72] raw input required")
    f = raw[:,46:62].reshape(-1,4,4)
    require((f[:,:,0] == 1).all().item(), "All four fact slots required")
    status,present,value = f[:,:,1],f[:,:,2],f[:,:,3]
    require(((status == 1)|(status == 2)).all().item()
            and torch.equal(present == 1, status == 2)
            and ((value == 0)|(value == 1)).all().item()
            and (value[present == 0] == 0).all().item(),
            "C174 observed/unobserved fact schema required")
    return present == 0

def leaf_positions(raw):
    missing_mask(raw)
    n = raw[:,4:46].reshape(-1,7,6)
    kinds, ids = n[:,:,1], n[:,:,2]
    leaf = kinds == 1
    require((leaf.sum(1) == 4).all().item(), "Four FACT leaves required")
    out = torch.full((len(raw),4), -1, dtype=torch.int64)
    for node in range(7):
        rows = torch.nonzero(leaf[:,node], as_tuple=True)[0]
        if len(rows):
            fact = ids[rows,node].to(torch.int64)-1
            require(((fact >= 0)&(fact < 4)).all().item(), "Bad FACT index")
            out[rows,fact] = node
    require((out >= 0).all().item(), "Incomplete fact-node map")
    for i in range(len(raw)):
        require(len(set(out[i].tolist())) == 4, "Repeated fact occurrence outside C188 scope")
    return out

def visible_tuple(row):
    r = np.asarray(row)
    require(r.shape == (72,), "One raw row required")
    result=[]
    for i in range(4):
        active,status,present,value = map(int, r[46+4*i:50+4*i])
        require(active == 1 and status in (1,2) and present == int(status == 2)
                and value in (0,1) and (present or value == 0), "Bad visible fact row")
        result.append(value if present else None)
    return tuple(result)

def influence_masks(features, template_ids, metadata):
    """TRAIN/evaluation label generator only; never called by selector inference."""
    x=np.asarray(features); ids=np.asarray(template_ids)
    require(x.ndim==2 and x.shape[1]==72 and ids.shape==(len(x),) and len(x)>0, "Bad teacher input")
    out=np.zeros((len(x),4), dtype=bool)
    for ri,(row,tid) in enumerate(zip(x,ids,strict=True)):
        ti=int(tid)
        require(0 <= ti < len(metadata), "Bad template index")
        table=tuple(int(v) for v in metadata[ti]["truth_table"])
        require(len(table)==16 and set(table)<={0,1}, "Bad truth table")
        vis=visible_tuple(row)
        for f in range(4):
            if vis[f] is not None:
                continue
            for bi,b in enumerate(BITS):
                if not all(v is None or v==b[j] for j,v in enumerate(vis)):
                    continue
                b2=list(b); b2[f]^=1; b2=tuple(b2)
                if all(v is None or v==b2[j] for j,v in enumerate(vis)):
                    bj=BITS.index(b2)
                    if table[bi] != table[bj]:
                        out[ri,f]=True
                        break
    return out

def cohort_masks(raw, labels, splits, valid):
    x = raw.detach().cpu().numpy() if isinstance(raw,torch.Tensor) else np.asarray(raw)
    y=np.asarray(labels); s=np.asarray(splits); v=np.asarray(valid)
    require(x.shape[1:]==(72,) and y.shape==s.shape==(len(x),) and v.shape==(len(x),4),
            "Cohort shape mismatch")
    miss=np.asarray([sum(z is None for z in visible_tuple(row)) for row in x],dtype=np.int8)
    vc=v.sum(1)
    require(np.all((y==0)==(vc==0)), "Necessity/target teacher disagreement")
    full_train=(s==0)&(y==1)&np.isin(miss,[2,3])
    full_eval=(s==1)&(y==1)&np.isin(miss,[2,3])
    train=full_train&(vc<miss)
    eval_=full_eval&(vc<miss)
    profile = {
        "train_discriminating": int(train.sum()),
        "train_m2": int((train&(miss==2)).sum()),
        "train_m3": int((train&(miss==3)).sum()),
        "train_m3_valid1": int((train&(miss==3)&(vc==1)).sum()),
        "train_m3_valid2": int((train&(miss==3)&(vc==2)).sum()),
        "eval_discriminating": int(eval_.sum()),
        "eval_m2": int((eval_&(miss==2)).sum()),
        "eval_m3": int((eval_&(miss==3)).sum()),
        "eval_m3_valid1": int((eval_&(miss==3)&(vc==1)).sum()),
        "eval_m3_valid2": int((eval_&(miss==3)&(vc==2)).sum()),
        "eval_full_multimissing": int(full_eval.sum()),
    }
    require(all(profile[k]==EXPECTED[k] for k in profile), "Registered cohort drift")
    return train, eval_, full_eval, miss, profile

def blind_key(row):
    r=np.asarray(row)
    require(r.shape==(72,), "One raw row required")
    return tuple(map(int,r[46:62]))

def build_frequency_reference(train_raw, train_valid):
    x=np.asarray(train_raw); v=np.asarray(train_valid)
    require(x.ndim==2 and x.shape[1]==72 and v.shape==(len(x),4) and len(x)>0, "Bad reference TRAIN data")
    counts={}
    for row,vm in zip(x,v,strict=True):
        key=blind_key(row); c=counts.setdefault(key,[0,0,0,0])
        for i in range(4):
            if vm[i]: c[i]+=1
    return counts

def apply_frequency_reference(counts, eval_raw):
    x=np.asarray(eval_raw); pred=[]
    for row in x:
        key=blind_key(row)
        require(key in counts, "Unseen syntax-blind visible key; no fallback")
        vis=visible_tuple(row); unknown=[i for i,v in enumerate(vis) if v is None]
        require(unknown, "Reference requires missing facts")
        c=counts[key]
        pred.append(max(unknown,key=lambda i:(c[i],-i)))
    return np.asarray(pred,dtype=np.int8)

def first_unknown(eval_raw):
    return np.asarray([next(i for i,v in enumerate(visible_tuple(row)) if v is None)
                       for row in np.asarray(eval_raw)],dtype=np.int8)

def target_metrics(valid, raw, prediction, groups=None):
    v=np.asarray(valid); x=np.asarray(raw); p=np.asarray(prediction)
    require(v.shape==(len(x),4) and p.shape==(len(x),) and len(x)>0, "Metric shape mismatch")
    miss=np.asarray([sum(z is None for z in visible_tuple(row)) for row in x],dtype=np.int8)
    unknown=np.asarray([[z is None for z in visible_tuple(row)] for row in x],dtype=bool)
    require(np.all((p>=0)&(p<4)), "Target index out of range")
    selected_unknown=unknown[np.arange(len(x)),p]
    hits=v[np.arange(len(x)),p]
    by={}
    for m in (2,3):
        q=miss==m; require(q.any(), f"Missing-count {m} absent")
        by[str(m)]={"rows":int(q.sum()),"hits":int(hits[q].sum()),"hit_rate":float(hits[q].mean())}
    result={"rows":len(x),"hits":int(hits.sum()),"hit_rate":float(hits.mean()),
            "selected_observed":int((~selected_unknown).sum()),
            "by_missing_count":by,
            "macro_m2_m3":(by["2"]["hit_rate"]+by["3"]["hit_rate"])/2}
    if groups is not None:
        g=np.asarray(groups); require(g.shape==(len(x),), "Group shape mismatch")
        result["by_group"]={str(k):{"rows":int((g==k).sum()),"hits":int(hits[g==k].sum()),
                                      "hit_rate":float(hits[g==k].mean())}
                            for k in sorted(set(g.tolist()))}
    return result

def validate_registered_references(train_raw,train_valid,eval_raw,eval_valid,eval_groups):
    counts=build_frequency_reference(train_raw,train_valid)
    require(len(counts)==EXPECTED["frequency_keys"], "Reference key count drift")
    fp=apply_frequency_reference(counts,eval_raw)
    first=first_unknown(eval_raw)
    fm=target_metrics(eval_valid,eval_raw,fp,eval_groups)
    im=target_metrics(eval_valid,eval_raw,first,eval_groups)
    require((fm["by_missing_count"]["2"]["hits"],fm["by_missing_count"]["3"]["hits"]) ==
            (EXPECTED["frequency_m2_hits"],EXPECTED["frequency_m3_hits"]), "Frequency reference drift")
    require((im["by_missing_count"]["2"]["hits"],im["by_missing_count"]["3"]["hits"]) ==
            (EXPECTED["first_m2_hits"],EXPECTED["first_m3_hits"]), "First-unknown reference drift")
    return counts, fm, im

class TargetSelector(nn.Module):
    def __init__(self):
        super().__init__()
        self.scorer=nn.Sequential(nn.Linear(FEATURES,HIDDEN,dtype=torch.float32),nn.ReLU(),
                                  nn.Linear(HIDDEN,1,dtype=torch.float32))
    def forward(self, fact_features):
        require(isinstance(fact_features,torch.Tensor) and fact_features.device.type=="cpu"
                and fact_features.dtype==torch.float32 and fact_features.ndim==3
                and fact_features.shape[1:]==(4,FEATURES) and len(fact_features)>0
                and torch.isfinite(fact_features).all().item(), "Finite [N,4,455] features required")
        return self.scorer(fact_features).squeeze(-1)

def head_fingerprint(model):
    require(type(model) is TargetSelector, "TargetSelector required")
    h=hashlib.sha256()
    for name,t in sorted(model.state_dict().items()):
        h.update(name.encode()); h.update(str(tuple(t.shape)).encode())
        h.update(t.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()

def selection_loss(logits, unknown, valid):
    require(logits.ndim==2 and logits.shape[1]==4 and unknown.shape==valid.shape==logits.shape
            and unknown.dtype==valid.dtype==torch.bool and len(logits)>0
            and torch.isfinite(logits).all().item(), "Typed selector batch required")
    require((valid & ~unknown).sum().item()==0 and (valid.sum(1)>=1).all().item()
            and (valid.sum(1)<unknown.sum(1)).all().item(), "Discriminating valid target sets required")
    denom=torch.logsumexp(logits.masked_fill(~unknown,float("-inf")),dim=1)
    numer=torch.logsumexp(logits.masked_fill(~valid,float("-inf")),dim=1)
    loss=(denom-numer).mean()
    require(torch.isfinite(loss).item(), "Nonfinite selector loss")
    return loss

def paired_head_initial(seed):
    require(type(seed) is int and 0<=seed<2**31, "Integer head seed required")
    torch.manual_seed(seed); m=TargetSelector()
    require(sum(p.numel() for p in m.parameters())==HEAD_PARAMETERS, "Selector capacity drift")
    return m

def fit_selector(initial, features, unknown, valid, seed, *, steps=STEPS, batch=BATCH, progress=None):
    require(type(initial) is TargetSelector and type(seed) is int and 0<=seed<2**31
            and type(steps) is int and steps>0 and type(batch) is int and batch>0, "Fixed selector fit required")
    require(features.shape[:2]==unknown.shape==valid.shape and features.shape[2]==FEATURES
            and len(features)>0, "Fit tensor shape mismatch")
    model=deepcopy(initial).train(); before=(head_fingerprint(initial),tensor_sha(features))
    rng=torch.Generator(device="cpu").manual_seed(seed+1000000)
    opt=torch.optim.Adam(model.parameters(),lr=.001,betas=(.9,.999),eps=1e-8,
                         weight_decay=0,amsgrad=False,foreach=False)
    schedule=hashlib.sha256(); history=[]; started=time.perf_counter()
    for step in range(steps):
        ids=torch.randint(len(features),(batch,),generator=rng); schedule.update(ids.numpy().tobytes())
        opt.zero_grad(set_to_none=True)
        loss=selection_loss(model(features[ids]),unknown[ids],valid[ids])
        loss.backward()
        require(all(p.grad is not None and torch.isfinite(p.grad).all().item() for p in model.parameters()),
                "Invalid selector gradient")
        opt.step()
        if (step+1)%500==0 or step+1==steps:
            row={"step":step+1,"training_loss":float(loss.detach())}; history.append(row)
            if progress is not None: progress(row)
    require(all(torch.isfinite(p).all().item() for p in model.parameters())
            and before==(head_fingerprint(initial),tensor_sha(features)), "Fit mutated input/initial")
    return model.eval(), {"steps":steps,"examples_drawn":steps*batch,
        "batch_schedule_sha256":schedule.hexdigest(),"training_log":history,
        "fit_wall_clock_seconds":time.perf_counter()-started}

def predict_selector(model, features, unknown, *, batch=1024):
    require(type(model) is TargetSelector and features.shape[:2]==unknown.shape
            and features.shape[2]==FEATURES and unknown.dtype==torch.bool, "Prediction input mismatch")
    before=head_fingerprint(model); out=[]; started=time.perf_counter()
    with torch.inference_mode():
        for lo in range(0,len(features),batch):
            z=model(features[lo:lo+batch])
            z=z.masked_fill(~unknown[lo:lo+batch],float("-inf"))
            out.append(z)
    z=torch.cat(out)
    require(head_fingerprint(model)==before and torch.isfinite(z[unknown]).all().item()
            and torch.isneginf(z[~unknown]).all().item(), "Selector inference drift")
    return z.argmax(1), z, {"rows":len(features),"forward_calls":(len(features)+batch-1)//batch,
                            "wall_clock_seconds":time.perf_counter()-started}

def capture_fact_features(base, scaled, raw, *, batch=1024):
    from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
    require(type(base) is graph.SharedGraphProbe and base.arm==graph.ARMS[1], "Frozen TREE_LINKS base required")
    pos=leaf_positions(raw); require(scaled.shape==(len(raw),72), "Scaled/raw row mismatch")
    before=graph.fingerprint(base); old=(base.calls,base.cell_calls,base.rows); chunks=[]
    with torch.inference_mode():
        for lo in range(0,len(raw),batch):
            hi=min(len(raw),lo+batch); states=[]
            handle=base.cell.register_forward_hook(lambda module,args,output: states.append(output.detach()))
            try:
                z=base(scaled[lo:hi])
            finally:
                handle.remove()
            require(len(states)==7 and z.shape==(hi-lo,2) and torch.isfinite(z).all().item(),
                    "Hidden-state capture mismatch")
            bank=torch.stack(states,dim=1)
            flat=bank.reshape(hi-lo,-1)[:,None,:].expand(-1,4,-1)
            one=nn.functional.one_hot(pos[lo:hi],num_classes=7).to(torch.float32)
            chunks.append(torch.cat((flat,one),dim=2).cpu())
    out=torch.cat(chunks)
    calls=(len(raw)+batch-1)//batch
    require(out.shape==(len(raw),4,FEATURES) and torch.isfinite(out).all().item()
            and graph.fingerprint(base)==before
            and (base.calls-old[0],base.cell_calls-old[1],base.rows-old[2])==(calls,7*calls,len(raw)),
            "Frozen feature extraction drift")
    return out, {"rows":len(raw),"forward_calls":calls,"cell_calls":7*calls}

def selector_gate(results, frequency):
    expected=[(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS]
    if [(r.get("base_seed"),r.get("head_seed")) for r in results] != expected:
        return False
    try:
        b2=frequency["by_missing_count"]["2"]["hit_rate"]
        b3=frequency["by_missing_count"]["3"]["hit_rate"]
        bm=frequency["macro_m2_m3"]
    except (KeyError,TypeError):
        return False
    for r in results:
        try:
            m=r["discriminating"]
            vals=(m["by_missing_count"]["2"]["hit_rate"],m["by_missing_count"]["3"]["hit_rate"],
                  m["macro_m2_m3"])
        except (KeyError,TypeError):
            return False
        if not all(type(x) in (int,float) and np.isfinite(x) for x in vals):
            return False
        if not (m.get("selected_observed")==0 and vals[0]>b2 and vals[1]>b3 and vals[2]>bm):
            return False
    return True

def manifest():
    return {
      "experiment_id":EXPERIMENT_ID,"stage":STAGE,"parent_sha256":PARENT_SHA,
      "acceptance_base":BASE,"parent_execution":PARENT_EXECUTION,
      "base_seeds":BASE_SEEDS,"head_seeds":HEAD_SEEDS,"base_arm":ARM,
      "question":"learn WHICH currently influential missing fact on multi-missing NEEDS rows",
      "changed":"new shared target-selection head only; accepted C181 base frozen",
      "teacher":"TRAIN-only influential target sets from visible observations plus registered truth tables",
      "teacher_definition":"unknown fact is valid iff two visible-consistent completions differing only in that fact yield different final outputs",
      "cohort":EXPECTED,
      "train_rows":3824,"pilot_primary_rows":528,"pilot_secondary_rows":1768,
      "target_model":"shared Linear455->64ReLU->1 per fact","target_parameters":HEAD_PARAMETERS,
      "base_parameters":25726,"trained_target_heads":9,"base_checkpoint_loads":3,
      "steps":STEPS,"batch":BATCH,"optimizer":"Adam","lr":.001,"betas":[.9,.999],
      "eps":1e-8,"weight_decay":0,"amsgrad":False,"foreach":False,
      "sampling":"with replacement; head_seed+1000000; same schedule across base seeds",
      "loss":"mean logsumexp(all unknown logits)-logsumexp(TRAIN valid influential logits)",
      "features":"all seven frozen64d C181 hidden states flattened + fact leaf-position onehot7",
      "inference_mask":"observable unknown facts only; target teacher absent",
      "frequency_reference":"TRAIN-only exact counts by visible fact-table key; choose max count among unknown; low slot tie",
      "frequency_expected":{"m2":"268/376","m3":"128/152","macro":0.7774356103023516},
      "first_unknown_expected":{"m2":"188/376","m3":"84/152","macro":0.5263157894736843},
      "primary":"equal mean target-hit rate on discriminating PILOT missing2 and missing3",
      "gate":"each of all9 selectors strictly beats TRAIN-frequency reference on m2,m3,and macro;zero observed selections;finite raw logits",
      "secondary":"full1768 PILOT multi-missing target hit,per-group,first-unknown reference;not alternate gate",
      "device":"cpu","dtype":"float32","threads":2,"deterministic_algorithms":True,
      "base_feature_rows":3*(3824+1768),"base_feature_forward_calls":18,"base_feature_cell_calls":126,
      "target_updates":9*STEPS,"target_examples_drawn":9*STEPS*BATCH,
      "pilot_selector_predictions":9*1768,
      "training":"selector heads only; no C181 base updates",
      "actual_acquisitions":0,"network_calls":0,"evidence_writes":0,"answer_generation":0,"proof_checker_calls":0,
      "production_runtime_modified":False,"gate_e_candidate":False,
      "limits":"same repeatedly-inspected four development semantic groups;offline target choice only;no live acquisition/tool/retry/language/general GateE claim",
      "outputs":sorted(OUTPUTS)
    }

MANIFEST_SHA = "0f8d22b00839e5a7506d5dabc06c64a7add86eb8a00e41840414842b7a773682"

def precheck(c187_summary, *args):
    from fold_lm.v05_benchmarks import gate_e_c187_restricted_acquisition as previous
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(len(args)==13, "Twelve prior summaries and repository root required")
    root=args[-1]
    p181,p174,pins,protected=previous.precheck(*args)
    require(audit.sha(c187_summary)==PARENT_SHA, "C187 summary changed")
    parent=audit.read_json(c187_summary); previous.validate_result(parent)
    require(parent["commit_sha"]==PARENT_EXECUTION and parent["status"]=="PASS"
            and previous.gate(parent["records"]) and parent["source_blobs"]==pins,
            "Wrong accepted C187 source/result")
    protected[str(Path(c187_summary).resolve())]=PARENT_SHA
    for a in parent["artifacts"]:
        f=audit.safe_child(Path(c187_summary).resolve().parent,a["file"])
        require(f.is_file() and f.stat().st_size==a["serialized_bytes"] and audit.sha(f)==a["sha256"],
                "Changed C187 artifact:"+a["file"])
        protected[str(f.resolve())]=a["sha256"]
    pins=dict(pins)
    for name in previous.OWN:
        pins[name]=audit.git(root,"rev-parse",PARENT_EXECUTION+":"+name).decode().strip()
    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins)==103 and len(protected)==239, "Source/protected union drift")
    require(digest(manifest())==MANIFEST_SHA, "Manifest drift")
    return p181,p174,pins,protected

def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c187_restricted_acquisition as previous
    names=previous.regression_modules(root)
    require(len(names)==len(set(names))==72, "Historical regression list drift")
    return names+["tests_lm.test_v05_c188_multimissing_target_selection"]

def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE
            and p["diagnostic_execution_valid"] is True, "Wrong/incomplete C188")
    require(p["trained_target_heads"]==9 and p["base_checkpoint_loads"]==3
            and p["new_training_steps"]==18000 and p["target_examples_drawn"]==4608000
            and p["base_feature_rows"]==16776 and p["base_feature_forward_calls"]==18
            and p["base_feature_cell_calls"]==126 and p["pilot_selector_predictions"]==15912
            and len(p["selector_results"])==9 and len(p["fit_records"])==9
            and len(p["source_blobs"])==103 and len(p["input_sha256"])==239
            and len(p["artifacts"])==14 and {a["file"] for a in p["artifacts"]}==OUTPUTS,
            "Workload/coverage drift")
    require(p["production_runtime_modified"] is False and p["gate_e_candidate"] is False
            and all(p[k]==0 for k in ("actual_acquisitions","network_calls","evidence_writes",
                                      "answer_generation","proof_checker_calls")),
            "Scope drift")
    require(p["status"]==("PASS" if selector_gate(p["selector_results"],p["frequency_reference"]) else "FAIL"),
            "Gate drift")

def run(*, output_dir, expected_head, **parents):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    root=Path(__file__).resolve().parents[2]
    args=tuple(parents[n+"_summary"] for n in PARENTS[1:])+(root,)
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"Dirty tracked tree")
    guard()
    p181,p174,pins,protected=precheck(parents["c187_summary"],*args)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter(); artifacts=[]; fit_records=[]; result_rows=[]
    def record(name):
        f=out/name; artifacts.append({"file":name,"sha256":audit.sha(f),"serialized_bytes":f.stat().st_size})
    def save(name,value):
        (out/name).write_bytes(blob(value)); record(name)
    save("target-selection-plan.json",dict(manifest(),source_blobs=pins))
    try:
        print("[C188] plan fixed; frozen C181 bases; TRAIN-only influential-target selector; no acquisition",flush=True)
        torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
        data,metadata=audit.load_data(Path(parents["c174_summary"]).resolve().parent,p174)
        raw=torch.from_numpy(data["features"].copy())
        valid=influence_masks(data["features"],data["template_ids"],metadata)
        train,evdisc,evfull,miss,profile=cohort_masks(raw,data["labels"],data["split_codes"],valid)
        train_ix=np.flatnonzero(train); eval_ix=np.flatnonzero(evdisc); full_ix=np.flatnonzero(evfull)
        np.savez_compressed(out/"target-teacher.npz",
            train_indices=train_ix.astype("<i4"),train_valid=valid[train].astype(np.uint8),
            eval_discriminating_indices=eval_ix.astype("<i4"),eval_discriminating_valid=valid[evdisc].astype(np.uint8),
            eval_full_indices=full_ix.astype("<i4"),eval_full_valid=valid[evfull].astype(np.uint8))
        record("target-teacher.npz")
        counts,freq_metrics,first_metrics=validate_registered_references(
            data["features"][train],valid[train],data["features"][evdisc],valid[evdisc],data["groups"][evdisc])
        save("frequency-reference.json",{
            "training_keys":len(counts),
            "counts":[{"key":list(k),"target_counts":v} for k,v in sorted(counts.items())],
            "frequency":freq_metrics,"first_unknown":first_metrics})
        print("[C188] 1/3 target teacher and TRAIN-only frequency reference fixed; PILOT discriminating rows=528",flush=True)
        parent=Path(parents["c181_summary"]).resolve().parent
        internal_fits={f["seed"]:f for f in p181["fit_records"] if f["arm"]==ARM}
        require(set(internal_fits)==set(BASE_SEEDS),"Accepted C181 candidate fits missing")
        bound_all=binding.prepare_pair(raw)[1]
        base_feature_meter={"rows":0,"forward_calls":0,"cell_calls":0}
        predictions=[]; logits_store=[]; base_fps={}
        for bseed in BASE_SEEDS:
            fit=internal_fits[bseed]
            base=frozen.restore_bare(parent/f"probe-{bseed}-{ARM}.pt",bseed,ARM,fit["final_sha256"])
            base_fp=graph.fingerprint(base); base_fps[bseed]=base_fp
            train_features,m1=capture_fact_features(base,bound_all[train],raw[train])
            eval_features,m2=capture_fact_features(base,bound_all[evfull],raw[evfull])
            for m in (m1,m2):
                for k in base_feature_meter: base_feature_meter[k]+=m[k]
            require(graph.fingerprint(base)==base_fp,"Frozen base changed during feature extraction")
            train_unknown=missing_mask(raw[train]); train_valid=torch.from_numpy(valid[train])
            eval_unknown=missing_mask(raw[evfull])
            disc_in_full=np.isin(full_ix,eval_ix)
            require(int(disc_in_full.sum())==528,"PILOT subset mapping drift")
            for hseed in HEAD_SEEDS:
                initial=paired_head_initial(hseed); ih=head_fingerprint(initial)
                def progress(row,bseed=bseed,hseed=hseed):
                    print(f"[C188] base={bseed} head={hseed} step={row['step']}/2000 loss={row['training_loss']:.6f}",flush=True)
                model,hist=fit_selector(initial,train_features,train_unknown,train_valid,hseed,progress=progress)
                name=f"selector-{bseed}-{hseed}.pt"
                torch.save({"base_seed":bseed,"head_seed":hseed,"schema":"c188-target-selector-v1",
                            "feature_width":FEATURES,"steps":STEPS,
                            "head_sha256":head_fingerprint(model),"state_dict":model.state_dict()},out/name)
                payload=torch.load(out/name,map_location="cpu",weights_only=True)
                require((payload["base_seed"],payload["head_seed"],payload["schema"],payload["feature_width"],payload["steps"])==
                        (bseed,hseed,"c188-target-selector-v1",FEATURES,STEPS),"Selector checkpoint metadata drift")
                restored=TargetSelector(); restored.load_state_dict(payload["state_dict"],strict=True); restored.eval()
                require(head_fingerprint(restored)==payload["head_sha256"],"Selector checkpoint changed")
                record(name)
                pred,z,meter=predict_selector(restored,eval_features,eval_unknown)
                pred_np=pred.numpy(); z_np=z.numpy()
                disc_pred=pred_np[disc_in_full]
                dm=target_metrics(valid[evdisc],data["features"][evdisc],disc_pred,data["groups"][evdisc])
                fm=target_metrics(valid[evfull],data["features"][evfull],pred_np,data["groups"][evfull])
                result_rows.append({"base_seed":bseed,"head_seed":hseed,"discriminating":dm,
                                    "full_multimissing":fm,"head_sha256":head_fingerprint(restored)})
                fit_records.append({"base_seed":bseed,"head_seed":hseed,"initial_sha256":ih,
                                    "final_sha256":head_fingerprint(restored),**hist})
                predictions.append(pred_np.astype(np.int8)); logits_store.append(z_np.astype(np.float32))
                print(f"[C188] base={bseed} head={hseed} m2={dm['by_missing_count']['2']['hit_rate']:.6f} "
                      f"m3={dm['by_missing_count']['3']['hit_rate']:.6f} macro={dm['macro_m2_m3']:.6f}",flush=True)
        require(base_feature_meter=={"rows":16776,"forward_calls":18,"cell_calls":126},"Base feature workload drift")
        for hseed in HEAD_SEEDS:
            rows=[f for f in fit_records if f["head_seed"]==hseed]
            require(len({f["initial_sha256"] for f in rows})==1 and len({f["batch_schedule_sha256"] for f in rows})==1,
                    "Unpaired selector initialization/schedule across frozen bases")
        np.savez_compressed(out/"pilot-predictions.npz",
            row_indices=full_ix.astype("<i4"),predictions=np.stack(predictions),
            logits=np.stack(logits_store),base_seeds=np.repeat(np.asarray(BASE_SEEDS,dtype="<i4"),3),
            head_seeds=np.tile(np.asarray(HEAD_SEEDS,dtype="<i4"),3))
        record("pilot-predictions.npz")
        save("selector-results.json",{"selector_results":result_rows,"fit_records":fit_records,
                                      "frequency_reference":freq_metrics,"first_unknown_reference":first_metrics,
                                      "cohort_profile":profile,"base_fingerprints":base_fps})
        print("[C188] 2/3 all nine selector heads saved/reloaded and scored; no best-head rescue",flush=True)
        guard(); precheck(parents["c187_summary"],*args)
        require([graph.fingerprint(frozen.restore_bare(parent/f"probe-{s}-{ARM}.pt",s,ARM,internal_fits[s]["final_sha256"]))
                 for s in BASE_SEEDS]==[base_fps[s] for s in BASE_SEEDS],"Accepted base checkpoint changed")
        for f,h in protected.items(): require(audit.sha(f)==h,"Protected input changed:"+f)
        for a in artifacts: require(audit.sha(out/a["file"])==a["sha256"],"Output changed:"+a["file"])
        result={"experiment_id":EXPERIMENT_ID,"stage":STAGE,"commit_sha":expected_head,
            "status":"PASS" if selector_gate(result_rows,freq_metrics) else "FAIL",
            "diagnostic_execution_valid":True,"C187_summary_sha256":PARENT_SHA,
            "source_blobs":pins,"input_sha256":protected,"artifacts":artifacts,
            "cohort_profile":profile,"frequency_reference":freq_metrics,"first_unknown_reference":first_metrics,
            "selector_results":result_rows,"fit_records":fit_records,
            "trained_target_heads":9,"base_checkpoint_loads":3,"fresh_head_seeds":3,
            "new_training_steps":sum(f["steps"] for f in fit_records),
            "target_examples_drawn":sum(f["examples_drawn"] for f in fit_records),
            "base_feature_rows":base_feature_meter["rows"],"base_feature_forward_calls":base_feature_meter["forward_calls"],
            "base_feature_cell_calls":base_feature_meter["cell_calls"],
            "pilot_selector_predictions":len(result_rows)*len(full_ix),
            "actual_acquisitions":0,"network_calls":0,"evidence_writes":0,"answer_generation":0,"proof_checker_calls":0,
            "production_runtime_modified":False,"gate_e_candidate":False,
            "environment":{"torch":torch.__version__,"numpy":np.__version__,"device":"cpu","dtype":"float32","threads":2},
            "wall_clock_seconds":time.perf_counter()-started,
            "limitations":["same four repeatedly inspected development semantic groups;not independent final confirmation",
                "target teacher is programmed TRAIN supervision;PILOT target sets are scoring labels only",
                "frozen C181 hidden states and hand-coded AST/leaf position features;not learned tool choice",
                "offline which-fact selection only;no C172/C173 acquisition,retry,answer or proof",
                "only C174 read-once four-fact family;no repeated variables/language/larger expressions"]}
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C188] 3/3 source/output preservation checked",flush=True)
        print("=== C188 RESULT ===",flush=True); print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/"invalid.json").write_bytes(blob({"experiment_id":EXPERIMENT_ID,"status":"INVALID",
            "diagnostic_execution_valid":False,"error":str(exc),"completed_fits":fit_records,
            "completed_results":result_rows}))
        raise

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in PARENTS:
        p.add_argument("--"+n+"-summary",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))

if __name__=="__main__":
    main()
