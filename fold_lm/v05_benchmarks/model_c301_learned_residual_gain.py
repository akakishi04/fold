"""C301: one TRAIN-learned global residual gain, initialized to the original function."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
from types import ModuleType
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C301-v5b-learned-residual-gain"
STAGE = "V5-B-LEARNED-RESIDUAL-GAIN"
BASE = "32bbfd3e74a0031ae8c327c7426d5a2900bd5c5e"
PARENT_EXECUTION = "b1d24f9ca330711802eb450f86fc3b4c64d88666"
PARENT_SHA = "440d5dcd9b8293f3925f394fa9ea1fc08d9754dfd67fc411340c5d6d1548fed3"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c300_frozen_readout_terms.py"
PARENT_BLOB = "7299772d37af3a6b693a922ca63d2418565f2d69"
READOUT_SOURCE = "fold_lm/v05_benchmarks/model_c278_mean_final_dual_query.py"
READOUT_BLOB = "0aa8d65874f4a021e21d04948ffd0a1d5615248b"
SEEDS = tuple(range(301001,301006))
ORDERS = tuple(range(301101,301106))
ARMS = ("fixed_gain", "learned_gain")
TASKS = ("two_char", "triple", "quad")
FIT_RNG = 602000
OWN = ("fold_lm/v05_benchmarks/model_c301_learned_residual_gain.py",
       "tests_lm/test_v05_c301_learned_residual_gain.py", "tools/run_c301.ps1", "tools/invoke_c301.ps1",
       "docs/experiment-ledger-addendum-c301-preregistration.md", "docs/v5b-learned-residual-gain-v0.1.md")
OUTPUTS = ("architecture-plan.json", "dataset.json", "triple-dataset.json", "quad-dataset.json",
           "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10, train_steps=8000, training_rows=384000, model_forward_calls=9620,
            row_presentations=539520, core_forward_calls=38480, model_state_loads=10,
            checkpoint_bundle_loads=1, new_checkpoint_writes=1, network_calls=0)
MANIFEST_SHA = "c10f5dd5be005595a12502ff9ebe43802f987464ca1b85da2adb28a47f175dd9"


def require(ok, message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))
def order_for(seed):
    require(seed in SEEDS,"initial seed"); return ORDERS[SEEDS.index(seed)]


def context():
    from fold_lm.v05_benchmarks import model_c300_frozen_readout_terms as parent
    _,audit,diagnostic,evaluation,transfer,training,c = parent.context()
    return parent,audit,diagnostic,evaluation,transfer,training,c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_summary_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,
        readout_source=READOUT_SOURCE,readout_blob=READOUT_BLOB,seeds=list(SEEDS),order_seeds=list(ORDERS),arms=list(ARMS),fit_rng=FIT_RNG,
        question="does a TRAIN-learned global residual gain improve reliable unseen four-character transfer versus fixed gain1",
        gain="alpha=2*sigmoid(g);g initialized exactly0;alpha initialized exactly1;one scalar per model,not per input",
        formula="readout_norm(alpha*r+a);r and a retain autograd;original C278 sum checked before substitution",
        parameters={"fixed_gain":14256,"learned_gain":14257},max_tokens=48,
        initialization="same actual C278 initial state within each pair;first common gradients and CE exactly matched before clipping",
        schedule="200epochs*4;order+301000+epoch;24 intact pairs;length=epoch%2;profile=epoch%3;100 exposures/row/length",
        loss="ordinary mean CE only",optimizer="AdamW",lr=.005,betas=[.9,.999],eps=1e-8,weight_decay=0.,clip=1.,steps=800,
        primary="all five learned_gain models pass every original four-character criterion",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        reports="10 results,60 final partitions,30 paired accuracy changes,all800 CE/gain histories and final gain",
        limits="one extra parameter;gain changes gradients/global clipping;not causal proof,per-query routing or inference speedup",
        parents=27,source_pins=652,protected_inputs=1202,own_tests=40,modules=186,loaded_tests=4638,focused_tests=4637,
        excluded_test=EXCLUDED,dtype="CPU float64",threads=2,deterministic=True,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def tensor_hash(entries):
    h=hashlib.sha256()
    for name,value in sorted(entries):
        h.update(name.encode("utf-8"))
        if value is None: h.update(b"NONE"); continue
        x=value.detach().cpu().contiguous(); h.update(str(x.dtype).encode()); h.update(str(tuple(x.shape)).encode()); h.update(x.numpy().tobytes())
    return h.hexdigest()


def hook_snapshot(model):
    return tuple((n,tuple(m._forward_pre_hooks),tuple(m._forward_hooks)) for n,m in model.named_modules())


class ResidualGain(torch.nn.Module):
    """Wrap the actual C278 model; do not detach either summand during training."""
    def __init__(self, model, arm):
        super().__init__(); require(arm in ARMS,"arm"); self.model=model; self.arm=arm
        self.register_parameter("gain_logit",torch.nn.Parameter(torch.zeros((),dtype=torch.float64)) if arm==ARMS[1] else None)
        self.verified_calls=0

    @property
    def backbone(self): return self.model.backbone
    @property
    def read(self): return self.model.read
    def gain(self):
        return 2*self.gain_logit.sigmoid() if self.gain_logit is not None else next(self.model.parameters()).new_tensor(1.)

    def forward(self, tokens, tasks):
        before=hook_snapshot(self.model); norm=self.backbone.readout_norm; state={}; handles=[]; checks=[0]; armed=[False]
        def capture_r(module,args):
            require("r" not in state and len(args)==1,"residual order"); state["r"]=args[0]
        def capture_a(module,args,output):
            require("r" in state and "a" not in state,"reader order"); state["a"]=output
        def replace(module,args):
            require(set(state)=={"r","a"} and len(args)==1,"sum coverage"); r,a=state["r"],state["a"]
            require(r.shape==a.shape==args[0].shape==(len(tokens),16) and r.dtype==a.dtype==torch.float64
                    and r.device.type==a.device.type=="cpu" and bool(torch.isfinite(r).all()) and bool(torch.isfinite(a).all()),"summand contract")
            require(torch.equal(args[0],r+a),"actual C278 sum"); checks[0]+=1
            if self.gain_logit is None: return None
            alpha=self.gain(); require(bool(torch.isfinite(alpha)) and 0.<=float(alpha.detach())<=2.,"gain bounds")
            return (alpha*r+a,)
        def arm_late(module,args,output):
            require(not armed[0],"encoder count"); armed[0]=True
            handles.append(norm.register_forward_pre_hook(replace))
        try:
            handles.append(norm.register_forward_pre_hook(capture_r))
            handles.append(self.read.output.register_forward_hook(capture_a))
            handles.append(self.backbone.local_encoder.register_forward_hook(arm_late))
            out=self.model(tokens,tasks)
            require(checks[0]==1,"formula check count"); self.verified_calls+=1
            return out
        finally:
            for h in handles: h.remove()
            require(hook_snapshot(self.model)==before,"hook restoration")


def make_models(seed,c):
    require(seed in SEEDS,"initial seed")
    base=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    require(type(base) is c.c278.MeanFinalDualReadout and sum(p.numel() for p in base.parameters())==14256,"base architecture")
    out={a:ResidualGain(copy.deepcopy(base),a) for a in ARMS}
    for arm,m in out.items():
        require(sum(p.numel() for p in m.parameters())==manifest()["parameters"][arm]
                and all(p.dtype==torch.float64 and p.device.type=="cpu" for p in m.parameters()),"capacity/precision")
        require(c.base.fingerprint(m.model)==c.base.fingerprint(base) and float(m.gain().detach())==1.,"matched initialization")
    require(not {p.data_ptr() for p in out[ARMS[0]].parameters()} & {p.data_ptr() for p in out[ARMS[1]].parameters()},"shared storage")
    return out


def schedule(order,rows,pair_source):
    require(order in ORDERS,"order seed"); pairs=pair_source.pairs_from_rows(rows)
    require(pairs.shape==(96,2) and pairs.dtype==torch.int64,"pair table")
    events=torch.empty((800,24,4),dtype=torch.int64)
    for epoch in range(200):
        ids=torch.randperm(96,generator=torch.Generator().manual_seed(order+301000+epoch))
        for block in range(4):
            step=4*epoch+block; events[step,:,0]=epoch%2; events[step,:,1]=epoch%3
            events[step,:,2:]=pairs[ids[block*24:(block+1)*24]]
    for length in range(2):
        ids=events[events[:,:,0]==length][:,2:].flatten()
        require(torch.equal(torch.bincount(ids,minlength=192),torch.full((192,),100)),"row exposures")
    return events


def pair_source(parent): return parent.context()[0].context()[2]


@contextmanager
def counted(model):
    calls=[0,0]; cores=[0]
    def forward(m,args,out): calls[0]+=1; calls[1]+=len(args[0])
    def core(m,args,out): cores[0]+=1
    h=model.register_forward_hook(forward); k=model.backbone.core.register_forward_hook(core)
    try: yield calls,cores
    finally: h.remove(); k.remove()


def fit(model,data,tokens,targets,seed,arm,ps):
    require(arm==model.arm and tokens.shape==(2,3,192,48) and targets.shape==(192,)
            and tokens.dtype==targets.dtype==torch.int64,"fit contract")
    require(torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)),"target alignment")
    events=schedule(order_for(seed),data["TRAIN"],ps); torch.manual_seed(FIT_RNG)
    opt=torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    history=[]; gains=[]; logits=[]; first_grad=None; model.train()
    for step in range(800):
        require(len(opt.param_groups)==1 and opt.param_groups[0]["lr"]==.005,"constant LR")
        opt.zero_grad(set_to_none=True); x,y=ps.render_batch(tokens,targets,events[step]); z=model(x,torch.zeros(48,dtype=torch.int64))
        require(z.shape==(48,256) and z.dtype==torch.float64 and bool(torch.isfinite(z).all()),"logits")
        loss=F.cross_entropy(z,y); require(bool(torch.isfinite(loss)),"loss")
        history.append(float(loss.detach())); gains.append(float(model.gain().detach()))
        logits.append(0. if model.gain_logit is None else float(model.gain_logit.detach()))
        loss.backward()
        if step==0: first_grad=tensor_hash((n,p.grad) for n,p in model.model.named_parameters())
        if model.gain_logit is not None:
            require(model.gain_logit.grad is not None and bool(torch.isfinite(model.gain_logit.grad)),"gain gradient")
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True); opt.step()
        if (step+1)%200==0: print(f"[C301] seed={seed} arm={arm} step={step+1}/800 ce={history[-1]:.6f} gain={float(model.gain().detach()):.6f}",flush=True)
    model.eval()
    return dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=FIT_RNG,ce_history=history,
        gain_history=gains,gain_logit_history=logits,final_gain=float(model.gain().detach()),
        final_gain_logit=0. if model.gain_logit is None else float(model.gain_logit.detach()),
        first_common_gradient_sha256=first_grad,event_sha256=digest(events.tolist()),schedule_events=events)


def check_fit(f,seed,arm,data,ps):
    require(all(type(f[k]) is int and f[k]==v for k,v in dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=FIT_RNG).items()),"fit budget")
    e=schedule(order_for(seed),data["TRAIN"],ps)
    require(isinstance(f["schedule_events"],torch.Tensor) and f["schedule_events"].dtype==torch.int64
            and torch.equal(e,f["schedule_events"]) and f["event_sha256"]==digest(e.tolist()),"events")
    for name in ("ce_history","gain_history","gain_logit_history"):
        require(len(f[name])==800 and all(type(v) in (int,float) and math.isfinite(v) for v in f[name]),"fit histories")
    require(min(f["ce_history"])>=0 and f["gain_history"][0]==1. and f["gain_logit_history"][0]==0.,"initial function")
    require(all(type(f[k]) in (int,float) and math.isfinite(f[k]) for k in ("final_gain","final_gain_logit")),"final gain")
    gg=f["gain_history"]+[f["final_gain"]]; ll=f["gain_logit_history"]+[f["final_gain_logit"]]
    expected=(2*torch.tensor(ll,dtype=torch.float64).sigmoid()).tolist() if arm==ARMS[1] else [1.]*801
    require(all(math.isclose(a,v,rel_tol=1e-14,abs_tol=1e-14) for a,v in zip(gg,expected,strict=True))
            and all(0.<=a<=2. for a in gg),"gain reconstruction")
    if arm==ARMS[0]: require(ll==[0.]*801,"fixed gain")
    require(re.fullmatch(r"[0-9a-f]{64}",f["first_common_gradient_sha256"]) is not None,"gradient fingerprint")


def check_pair(records):
    require(len(records)==2 and [r["arm"] for r in records]==list(ARMS) and records[0]["seed"]==records[1]["seed"],"paired identities")
    a,b=records
    require(a["initial_common_sha256"]==b["initial_common_sha256"]
            and a["fit"]["event_sha256"]==b["fit"]["event_sha256"]
            and a["fit"]["ce_history"][0]==b["fit"]["ce_history"][0]
            and a["fit"]["first_common_gradient_sha256"]==b["fit"]["first_common_gradient_sha256"],"matched initial function/gradients/order")


def train_one(model,data,triple,quad,tokens,targets,seed,arm,ps,evaluation,transfer,c):
    start=c.base.fingerprint(model); common=c.base.fingerprint(model.model); n=model.verified_calls
    with counted(model) as (calls,cores):
        f=fit(model,data,tokens,targets,seed,arm,ps); final=c.base.fingerprint(model); model.requires_grad_(False)
        raw=evaluation.evaluate(model,data,triple,quad,transfer,c)
    require(calls==[881,46176] and cores[0]==3524 and model.verified_calls-n==881,"train/evaluation counts")
    require(start!=final and common!=c.base.fingerprint(model.model) and final==c.base.fingerprint(model),"weight integrity")
    return dict(seed=seed,arm=arm,initial_sha256=start,initial_common_sha256=common,final_sha256=final,
        parameters=sum(p.numel() for p in model.parameters()),fit=f,raw=raw,forward_calls=881,row_presentations=46176,
        core_forward_calls=3524,formula_checks=881),{k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def replay_one(model,state,record,data,triple,quad,evaluation,transfer,c):
    model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(False); n=model.verified_calls
    require(c.base.fingerprint(model)==record["final_sha256"] and float(model.gain().detach())==record["fit"]["final_gain"],"strict checkpoint")
    with counted(model) as (calls,cores): raw=evaluation.evaluate(model,data,triple,quad,transfer,c)
    error=evaluation.replay_error(raw,record["raw"],data,c)
    require(calls==[81,7776] and cores[0]==324 and model.verified_calls-n==81 and c.base.fingerprint(model)==record["final_sha256"],"replay integrity")
    record.update(checkpoint_roundtrip=True,reload_max_error=error,replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324)


def analyze(records,data,ps,diagnostic,transfer,c):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"complete cohort")
    metrics=[]; parts=[]; results=[]; contrasts=[]
    for r in records:
        seed,arm=r["seed"],r["arm"]; check_fit(r["fit"],seed,arm,data,ps)
        require(r["parameters"]==manifest()["parameters"][arm] and r["initial_sha256"]!=r["final_sha256"]
                and r["checkpoint_roundtrip"] is True and r["formula_checks"]==881,"record integrity")
        require(type(r["reload_max_error"]) in (int,float) and math.isfinite(r["reload_max_error"]) and 0<=r["reload_max_error"]<=1e-9,"replay error")
        keys=("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in keys) and tuple(r[k] for k in keys)==(881,46176,3524,81,7776,324),"workload")
        require(set(r["raw"])==set(TASKS),"tasks")
        scored=dict(two_char=c.p267.score(data,r["raw"]["two_char"]),triple=c.c270.score(data,r["raw"]["triple"],c.p267),quad=transfer.score_quad(data,r["raw"]["quad"],c))
        flags={t+"_pass":scored[t]["passed"] for t in TASKS}; require(all(type(v) is bool for v in flags.values()),"task flags"); direct={}
        for task in TASKS:
            normalized=diagnostic.normalize_task(scored[task],task,seed,arm)
            for split in ("TRAIN","HOLDOUT"):
                part=diagnostic.partition([x for x in normalized if x["split"]==split]); direct[(task,split)]=part["direct_pass"]
                parts.append(dict(seed=seed,arm=arm,task=task,split=split,**part))
        results.append(dict(seed=seed,arm=arm,**flags,all_tasks_pass=all(flags.values()),
            fitted_train_direct_pass=all(direct[(t,"TRAIN")] for t in TASKS[:2]),seen_holdout_direct_pass=all(direct[(t,"HOLDOUT")] for t in TASKS[:2]),
            final_gain=r["fit"]["final_gain"]))
        metrics.append(dict(seed=seed,arm=arm,**scored))
    for i in range(0,10,2): check_pair(records[i:i+2])
    for seed,task,split in itertools.product(SEEDS,TASKS,("TRAIN","HOLDOUT")):
        pair=[next(p for p in parts if (p["seed"],p["arm"],p["task"],p["split"])==(seed,a,task,split)) for a in ARMS]
        require(pair[0]["rows"]==pair[1]["rows"],"partition denominator")
        contrasts.append(dict(seed=seed,task=task,split=split,rows=pair[0]["rows"],control_correct=pair[0]["correct"],candidate_correct=pair[1]["correct"]))
    counts={t:{a:sum(r[t+"_pass"] for r in results if r["arm"]==a) for a in ARMS} for t in TASKS}
    s=dict(seed_results=results,task_pass_counts=counts,candidate_gate=counts["quad"][ARMS[1]]==5,
        final_partitions=parts,contrasts=contrasts,all_pairs_matched=True,all_replays=True,**WORK)
    require((len(parts),len(contrasts))==(60,30),"inventory"); return metrics,s


def parent_hashes(parent):
    p299=parent.context()[0]
    return (PARENT_SHA,parent.PARENT_SHA,*p299.parent_hashes(p299.context()[0]))


def load_parent(paths):
    parent,audit,*_,c=context(); paths=[Path(p).resolve() for p in paths]; hashes=parent_hashes(parent)
    require(len(paths)==len(hashes)==27 and all(c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)),"parent hashes")
    with audit.no_neural():
        payload,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); parent.validate_result(payload)
        require(payload["experiment_id"]=="C300-v5b-frozen-readout-term-ablation" and payload["commit_sha"]==PARENT_EXECUTION
                and payload["status"]=="PASS" and payload["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB
                and payload["source_blobs"].get(READOUT_SOURCE)==READOUT_BLOB,"parent identity")
        s=payload["validation_summary"]
        require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False and s["all_weights_preserved"] is True
                and s["all_hooks_restored"] is True and s["task_pass_matrices"]["full_before"]==parent.expected_matrices()
                and s["task_pass_matrices"]["full_after"]==parent.expected_matrices(),"parent outcome")
        require(len(payload["artifacts"])==4 and {a["file"] for a in payload["artifacts"]}==set(parent.OUTPUTS),"parent artifacts")
        # C300 has no dataset/checkpoint of its own; read recursively verified C299 input copies.
        data=[c.audit.read_json(paths[1].parent/n) for n in OUTPUTS[1:4]]
        require(tuple(map(digest,data))==tuple(parent.context()[0].DATA_HASHES),"data hashes")
    return payload,*data


def precheck(paths,root):
    validate_seal(); p,*_=load_parent(paths); parent,audit,*_,c=context(); root=Path(root).resolve()
    pins=dict(p["source_blobs"]); protected=dict(p["input_sha256"]); require((len(pins),len(protected))==(646,1191),"inherited counts")
    for n,h in pins.items(): require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in protected.items(): require(Path(n).is_file() and c.audit.sha(n)==h,"changed input:"+n)
    covered=set()
    for module in [parent,audit,pair_source(parent),*parent.context(),*vars(c).values()]:
        path=getattr(module,"__file__",None) if isinstance(module,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            name=Path(path).resolve().relative_to(root).as_posix(); require(name in pins,"unprotected helper:"+name); covered.add(name)
    require(PARENT_SOURCE in covered and pins.get(READOUT_SOURCE)==READOUT_BLOB,"readout coverage")
    for path,h in [(Path(paths[0]).resolve(),PARENT_SHA)]+[(c.audit.safe_child(Path(paths[0]).resolve().parent,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h,"parent input"); protected[str(path.resolve())]=h
    for n in OWN: require(n not in pins,"OWN collision"); pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins)); require((len(pins),len(protected))==(652,1202),"protection count")
    print(f"registration_check = source_pins:652; protected_inputs:1202; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def runtime_preflight(paths,root):
    precheck(paths,root); parent,*_,training,c=context(); _,data,_,_=load_parent(paths); ps=pair_source(parent)
    tokens,targets=training.training_tables(data,c)
    for order in ORDERS: schedule(order,data["TRAIN"],ps)
    models=make_models(SEEDS[0],c); events=schedule(ORDERS[0],data["TRAIN"],ps); x,y=ps.render_batch(tokens,targets,events[0])
    grads=[]; outputs=[]
    for m in (models[ARMS[0]].model,models[ARMS[0]],models[ARMS[1]]):
        m.train(); m.zero_grad(set_to_none=True); torch.manual_seed(FIT_RNG)
        z=m(x,torch.zeros(48,dtype=torch.int64)); F.cross_entropy(z,y).backward(); outputs.append(z.detach())
        common=m.model if isinstance(m,ResidualGain) else m
        grads.append(tensor_hash((n,p.grad) for n,p in common.named_parameters()))
    require(all(torch.equal(outputs[0],v) for v in outputs[1:]) and len(set(grads))==1,"real initial logits/common-gradient identity")
    require(models[ARMS[1]].gain_logit.grad is not None and bool(torch.isfinite(models[ARMS[1]].gain_logit.grad)),"real gain gradient")
    print("real_initial_forward_and_common_gradients = PASS; operational preflight only",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require(p["gate_f_candidate"] is False and p["production_adoption"] is False,"claim scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(652,1202) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(READOUT_SOURCE)==READOUT_BLOB,"result protection")
    require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"output set")
    s=p["validation_summary"]; rr=s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rr]==identities(),"result cohort")
    require(all(type(r[t+"_pass"]) is bool for r in rr for t in TASKS),"result flags")
    expected={t:{a:sum(r[t+"_pass"] for r in rr if r["arm"]==a) for a in ARMS} for t in TASKS}
    gate=expected["quad"][ARMS[1]]==5
    require(s["task_pass_counts"]==expected and s["candidate_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"fixed gate")
    require(s["all_pairs_matched"] is True and s["all_replays"] is True and len(s["final_partitions"])==60 and len(s["contrasts"])==30,"result inventory")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"result workload")


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c301-gain-models-v1"
            and v["identities"]==[list(i) for i in identities()] and len(v["states"])==10,"checkpoint schema")
    return v["states"]


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==185,"parent modules")
    return names+["tests_lm.test_v05_c301_learned_residual_gain"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==4638 and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED]; require(len(kept)==4637,"focused suite"); return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    parent,_,diag,evaluation,transfer,training,c=context(); root=Path(__file__).resolve().parents[2]; ps=pair_source(parent)
    guard(root,expected_head,c); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected=precheck(summaries,root); _,data,triple,quad=load_parent(summaries); tokens,targets=training.training_tables(data,c)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False); records=[]; states=[]
    for seed in SEEDS:
        models=make_models(seed,c)
        for arm in ARMS:
            print(f"[C301] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            r,state=train_one(models[arm],data,triple,quad,tokens,targets,seed,arm,ps,evaluation,transfer,c); records.append(r); states.append(state)
        check_pair(records[-2:])
    torch.save(dict(schema="fold-c301-gain-models-v1",identities=[list(i) for i in identities()],states=states),out/"trained-models.pt")
    loaded=load_bundle(out/"trained-models.pt")
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,c)
        for j,arm in enumerate(ARMS): replay_one(models[arm],loaded[2*i+j],records[2*i+j],data,triple,quad,evaluation,transfer,c)
    metrics,s=analyze(records,data,ps,diag,transfer,c)
    torch.save(dict(schema="fold-c301-gain-eval-v1",records=records),out/"evaluations.pt")
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],data),(OUTPUTS[2],triple),(OUTPUTS[3],quad),(OUTPUTS[6],metrics),(OUTPUTS[7],s)): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]; guard(root,expected_head,c); precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if s["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=s,gate_f_candidate=False,production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p)); receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","artifacts")}
    receipt["summary_sha256"]=c.audit.sha(out/"summary.json"); print("=== C301 COMPACT RESULT RECEIPT ===",flush=True); print(json.dumps(receipt,indent=2,sort_keys=True),flush=True); return p


def verify_artifacts(outdir,summaries,expected_head):
    parent,audit,diag,_,transfer,_,c=context(); out=Path(outdir); p=c.audit.read_json(out/"summary.json"); validate_result(p); require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items(): require(c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"]); require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with audit.no_neural():
        _,data,triple,quad=load_parent(summaries)
        for n,v in zip(OUTPUTS[1:4],(data,triple,quad),strict=True): require(c.audit.read_json(out/n)==v,"persisted data")
        v=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(v)=={"schema","records"} and v["schema"]=="fold-c301-gain-eval-v1","evaluation schema")
        metrics,s=analyze(v["records"],data,pair_source(parent),diag,transfer,c)
        for n,x in ((OUTPUTS[0],manifest()),(OUTPUTS[6],metrics),(OUTPUTS[7],s)): require(c.audit.read_json(out/n)==x,"persisted:"+n)
    require(s==p["validation_summary"],"summary reconstruction"); return p,metrics


def main():
    p=argparse.ArgumentParser(); p.add_argument("--summaries",nargs=27,type=Path,required=True); p.add_argument("--output-dir",type=Path,required=True); p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__=="__main__": main()
