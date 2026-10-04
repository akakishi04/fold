"""C303: forward-identical residual-gradient intervention, with a frozen-core control."""
from __future__ import annotations
import argparse
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

EXPERIMENT_ID = "C303-v5b-residual-gradient-routing"
STAGE = "V5-B-RESIDUAL-GRADIENT-ROUTING"
BASE = "d628bf0b901ee6a63fc9e6c5f338fac867e8bcfc"
PARENT_EXECUTION = "cfb1092c859f9e5512dcfdd63858973ab2194710"
PARENT_SHA = "1054849a7c416eb0a32f53e114df5501401b3f4acfeec1f6dc5aa4276d302b10"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c302_frozen_gain_cross.py"
PARENT_BLOB = "1eb77daeb4fd53141ad31a6ad3c60ceba9ce3ad2"
READOUT_SOURCE = "fold_lm/v05_benchmarks/model_c278_mean_final_dual_query.py"
READOUT_BLOB = "0aa8d65874f4a021e21d04948ffd0a1d5615248b"
SEEDS = tuple(range(303001,303006))
ORDERS = tuple(range(303101,303106))
ARMS = ("full_train","core_frozen","residual_stop")
TASKS = ("two_char","triple","quad")
FIT_RNG = 606000
OWN = ("fold_lm/v05_benchmarks/model_c303_residual_gradient.py",
       "tests_lm/test_v05_c303_residual_gradient.py","tools/run_c303.ps1","tools/invoke_c303.ps1",
       "docs/experiment-ledger-addendum-c303-preregistration.md","docs/v5b-residual-gradient-v0.1.md")
OUTPUTS = ("architecture-plan.json","dataset.json","triple-dataset.json","quad-dataset.json",
           "trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=15,train_steps=12000,training_rows=576000,model_forward_calls=14430,
            row_presentations=809280,core_forward_calls=57720,model_state_loads=15,
            checkpoint_bundle_loads=1,new_checkpoint_writes=1,network_calls=0)
MANIFEST_SHA = "265067d9ca156f5181b6275ce4274ffee919751bcf1cd395b470656bce163ad7"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c302_frozen_gain_cross as parent
    p301,audit,diagnostic,evaluation,transfer,training,c=parent.context()
    return parent,p301,audit,diagnostic,evaluation,transfer,training,c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        parent_summary_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,
        readout_source=READOUT_SOURCE,readout_blob=READOUT_BLOB,seeds=list(SEEDS),orders=list(ORDERS),arms=list(ARMS),fit_rng=FIT_RNG,
        question="does stopping residual-branch backprop improve reliable quad transfer beyond merely freezing core weights",
        forward="unchanged actual C278 norm(r+a);candidate uses norm(stop_gradient(r)+a);no gain and no inference switch",
        learning="full_train learns all;core_frozen freezes core but propagates through it to inputs;residual_stop also blocks the residual input gradient",
        stored_parameters=14256,core_parameters=3328,requires_grad_parameters=dict(full_train=14256,core_frozen=10928,residual_stop=10928),
        gradient_accounting="record parameter inventory,per-update gradient-receiving scalar counts,and union of names;None is not numeric zero",
        schedule="200epochs*4;private order+303000+epoch;24 intact pairs;length=epoch%2;profile=epoch%3;100 row exposures per length",
        loss="ordinary mean CE",optimizer="AdamW",lr=.005,betas=[.9,.999],eps=1e-8,weight_decay=0.,clip=1.,steps=800,
        initial_checks="exact initial common state,first logits/CE and reader gradients;other gradients intentionally need not agree",
        primary="all five residual_stop models pass every original quad criterion;compare separately to BOTH controls",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        scope="gradient intervention and active-learning capacity differ;no claim of equal backward compute,core removal,or isolated cause",
        parents=29,source_pins=664,protected_inputs=1228,own_tests=40,modules=188,loaded_tests=4710,focused_tests=4709,
        excluded_test=EXCLUDED,partitions=90,contrasts=60,max_tokens=48,dtype="CPU float64",threads=2,deterministic=True,
        gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def tensor_hash(entries):
    h=hashlib.sha256()
    for name,value in sorted(entries):
        h.update(name.encode("utf-8"))
        if value is None: h.update(b"NONE"); continue
        x=value.detach().cpu().contiguous();h.update(str(x.dtype).encode());h.update(str(tuple(x.shape)).encode());h.update(x.numpy().tobytes())
    return h.hexdigest()


def fingerprint(model): return tensor_hash(model.state_dict().items())


def hook_snapshot(model):
    attrs=("_forward_pre_hooks","_forward_hooks","_forward_pre_hooks_with_kwargs","_forward_hooks_with_kwargs","_forward_hooks_always_called")
    return tuple((n,tuple(tuple(getattr(m,a)) for a in attrs)) for n,m in model.named_modules())


class GradientRoute(torch.nn.Module):
    def __init__(self,model,arm):
        super().__init__();require(arm in ARMS,"arm");self.model=model;self.arm=arm;self.verified_calls=0
        if arm!=ARMS[0]: self.backbone.core.requires_grad_(False)
    @property
    def backbone(self): return self.model.backbone
    @property
    def read(self): return self.model.read
    def forward(self,tokens,tasks):
        before=hook_snapshot(self.model);state={};handles=[];armed=[False];checks=[0];norm=self.backbone.readout_norm
        def capture_r(module,args):
            require("r" not in state and len(args)==1,"residual capture");state["r"]=args[0]
        def capture_a(module,args,out):
            require("r" in state and "a" not in state,"reader capture");state["a"]=out
        def replace(module,args):
            require(set(state)=={"r","a"} and len(args)==1,"sum coverage");r,a=state["r"],state["a"]
            require(r.shape==a.shape==args[0].shape==(len(tokens),16) and r.dtype==a.dtype==torch.float64
                    and r.device.type==a.device.type=="cpu" and bool(torch.isfinite(r).all()) and bool(torch.isfinite(a).all()),"summands")
            require(torch.equal(args[0],r+a),"actual C278 sum");checks[0]+=1
            if self.arm!=ARMS[2]: return None
            value=r.detach()+a
            require(torch.equal(value,args[0]),"forward identity")
            return (value,)
        def arm_late(module,args,out):
            require(not armed[0],"encoder count");armed[0]=True;handles.append(norm.register_forward_pre_hook(replace))
        try:
            handles.append(norm.register_forward_pre_hook(capture_r))
            handles.append(self.read.output.register_forward_hook(capture_a))
            handles.append(self.backbone.local_encoder.register_forward_hook(arm_late))
            out=self.model(tokens,tasks);require(checks[0]==1,"formula check count");self.verified_calls+=1;return out
        finally:
            for h in handles:h.remove()
            require(hook_snapshot(self.model)==before,"hook restoration")


def make_models(seed,c):
    require(seed in SEEDS,"seed")
    base=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    require(type(base) is c.c278.MeanFinalDualReadout and sum(p.numel() for p in base.parameters())==14256
            and sum(p.numel() for p in base.backbone.core.parameters())==3328,"actual architecture")
    models={a:GradientRoute(copy.deepcopy(base),a) for a in ARMS};seen=set()
    for arm,m in models.items():
        require(sum(p.numel() for p in m.parameters())==14256 and sum(p.numel() for p in m.parameters() if p.requires_grad)==manifest()["requires_grad_parameters"][arm],"parameter inventory")
        require(all(p.dtype==torch.float64 and p.device.type=="cpu" for p in m.parameters()) and fingerprint(m.model)==fingerprint(base),"initial state")
        ptrs={p.data_ptr() for p in m.parameters()};require(not seen&ptrs,"shared storage");seen.update(ptrs)
    return models


def schedule(seed,rows,ps):
    require(seed in SEEDS,"schedule seed");order=ORDERS[SEEDS.index(seed)];pairs=ps.pairs_from_rows(rows)
    require(pairs.dtype==torch.int64 and pairs.shape==(96,2),"pairs");events=torch.empty((800,24,4),dtype=torch.int64)
    for epoch in range(200):
        ids=torch.randperm(96,generator=torch.Generator().manual_seed(order+303000+epoch))
        for j in range(4):
            n=4*epoch+j;events[n,:,0]=epoch%2;events[n,:,1]=epoch%3;events[n,:,2:]=pairs[ids[24*j:24*(j+1)]]
    for length in range(2):
        require(torch.equal(torch.bincount(events[events[:,:,0]==length][:,2:].flatten(),minlength=192),torch.full((192,),100)),"exposures")
    return events


def parameter_inventory(model):
    return {n:dict(numel=p.numel(),trainable=p.requires_grad,core=n.startswith("model.backbone.core.")) for n,p in model.named_parameters()}


def fit(model,data,tokens,targets,seed,ps):
    require(tokens.shape==(2,3,192,48) and targets.shape==(192,) and tokens.dtype==targets.dtype==torch.int64,"tables")
    require(torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)),"target alignment")
    events=schedule(seed,data["TRAIN"],ps);inventory=parameter_inventory(model);torch.manual_seed(FIT_RNG)
    opt=torch.optim.AdamW((p for p in model.parameters() if p.requires_grad),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    model.train();losses=[];counts=[];core_counts=[];union=set();first={}
    for step in range(800):
        require(len(opt.param_groups)==1 and opt.param_groups[0]["lr"]==.005,"LR")
        opt.zero_grad(set_to_none=True);x,y=ps.render_batch(tokens,targets,events[step]);z=model(x,torch.zeros(48,dtype=torch.int64))
        require(z.shape==(48,256) and z.dtype==torch.float64 and bool(torch.isfinite(z).all()),"logits")
        loss=F.cross_entropy(z,y);require(bool(torch.isfinite(loss)),"loss");losses.append(float(loss.detach()));loss.backward()
        active={n for n,p in model.named_parameters() if p.grad is not None};union.update(active)
        require(all(bool(torch.isfinite(p.grad).all()) for p in model.parameters() if p.grad is not None),"nonfinite gradients")
        count=sum(inventory[n]["numel"] for n in active);cc=sum(inventory[n]["numel"] for n in active if inventory[n]["core"])
        counts.append(count);core_counts.append(cc)
        if model.arm!=ARMS[0]:require(cc==0,"frozen core gradient")
        if step==0:
            first=dict(logits_sha256=tensor_hash([("logits",z)]),reader_gradient_sha256=tensor_hash((n,p.grad) for n,p in model.read.named_parameters()))
        torch.nn.utils.clip_grad_norm_((p for p in model.parameters() if p.requires_grad),1.,error_if_nonfinite=True);opt.step()
        if (step+1)%200==0:print(f"[C303] seed={seed} arm={model.arm} step={step+1}/800 ce={losses[-1]:.6f} gradient_scalars={count}",flush=True)
    model.eval()
    return dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=FIT_RNG,ce_history=losses,
        parameter_inventory=inventory,gradient_scalars=counts,core_gradient_scalars=core_counts,gradient_parameter_union=sorted(union),
        event_sha256=digest(events.tolist()),schedule_events=events,**first)


def check_fit(f,seed,arm,data,ps):
    require(all(type(f[k]) is int and f[k]==v for k,v in dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=FIT_RNG).items()),"fit budget")
    e=schedule(seed,data["TRAIN"],ps);require(torch.equal(f["schedule_events"],e) and f["event_sha256"]==digest(e.tolist()),"schedule")
    inv=f["parameter_inventory"]
    require(bool(inv) and all(type(v["numel"]) is int and v["numel"]>0 and type(v["trainable"]) is type(v["core"]) is bool for v in inv.values()),"inventory types")
    require(sum(v["numel"] for v in inv.values())==14256 and sum(v["numel"] for v in inv.values() if v["core"])==3328
            and sum(v["numel"] for v in inv.values() if v["trainable"])==manifest()["requires_grad_parameters"][arm],"inventory counts")
    require(all(v["core"]==n.startswith("model.backbone.core.") and v["trainable"]==(arm==ARMS[0] or not v["core"]) for n,v in inv.items()),"inventory policy")
    union=f["gradient_parameter_union"];require(union==sorted(set(union)) and set(union)<=set(inv) and all(inv[n]["trainable"] for n in union),"gradient union")
    cap=sum(inv[n]["numel"] for n in union)
    require(len(f["ce_history"])==800 and all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in f["ce_history"]),"loss history")
    require(len(f["gradient_scalars"])==len(f["core_gradient_scalars"])==800 and all(type(n) is int and 0<n<=cap for n in f["gradient_scalars"]),"gradient counts")
    require(all(type(n) is int and 0<=n<=3328 for n in f["core_gradient_scalars"]),"core counts")
    if arm!=ARMS[0]:require(f["core_gradient_scalars"]==[0]*800 and not any(inv[n]["core"] for n in union),"frozen core history")
    for n in ("logits_sha256","reader_gradient_sha256"):require(re.fullmatch(r"[0-9a-f]{64}",f[n]) is not None,"first-step fingerprint")


def check_group(rows):
    require(len(rows)==3 and [r["arm"] for r in rows]==list(ARMS) and len({r["seed"] for r in rows})==1,"group identities")
    require(len({r["initial_sha256"] for r in rows})==len({r["core_initial_sha256"] for r in rows})==1,"initial equality")
    for k in ("event_sha256","logits_sha256","reader_gradient_sha256"):
        require(len({r["fit"][k] for r in rows})==1,"matched "+k)
    require(len({r["fit"]["ce_history"][0] for r in rows})==1,"initial CE")


def train_one(model,data,triple,quad,tokens,targets,seed,ps,p301,evaluation,transfer,c):
    start=c.base.fingerprint(model);core_start=c.base.fingerprint(model.backbone.core);n=model.verified_calls
    with p301.counted(model) as (calls,cores):
        f=fit(model,data,tokens,targets,seed,ps);final=c.base.fingerprint(model);model.requires_grad_(False)
        raw=evaluation.evaluate(model,data,triple,quad,transfer,c)
    require(calls==[881,46176] and cores[0]==3524 and model.verified_calls-n==881,"train/eval counts")
    core_final=c.base.fingerprint(model.backbone.core)
    require(start!=final and final==c.base.fingerprint(model) and ((core_final==core_start)==(model.arm!=ARMS[0])),"weight policy")
    return dict(seed=seed,arm=model.arm,initial_sha256=start,final_sha256=final,core_initial_sha256=core_start,core_final_sha256=core_final,
        fit=f,raw=raw,formula_checks=881,forward_calls=881,row_presentations=46176,core_forward_calls=3524),{k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def replay_one(model,state,r,data,triple,quad,p301,evaluation,transfer,c):
    model.load_state_dict(state,strict=True);model.eval();model.requires_grad_(False);n=model.verified_calls
    require(c.base.fingerprint(model)==r["final_sha256"],"strict state")
    with p301.counted(model) as (calls,cores):raw=evaluation.evaluate(model,data,triple,quad,transfer,c)
    error=evaluation.replay_error(raw,r["raw"],data,c)
    require(calls==[81,7776] and cores[0]==324 and model.verified_calls-n==81 and c.base.fingerprint(model)==r["final_sha256"],"replay counts/state")
    r.update(checkpoint_roundtrip=True,reload_max_error=error,replay_forward_calls=81,replay_row_presentations=7776,replay_core_forward_calls=324)


def analyze(records,data,ps,diag,transfer,c):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"cohort");metrics=[];parts=[];results=[];contrasts=[]
    for r in records:
        seed,arm=r["seed"],r["arm"];check_fit(r["fit"],seed,arm,data,ps)
        require(r["initial_sha256"]!=r["final_sha256"] and ((r["core_initial_sha256"]==r["core_final_sha256"])==(arm!=ARMS[0])) and r["checkpoint_roundtrip"] is True,"state metadata")
        require(type(r["reload_max_error"]) in (int,float) and math.isfinite(r["reload_max_error"]) and 0<=r["reload_max_error"]<=1e-9,"replay bound")
        names=("formula_checks","forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[n]) is int for n in names) and tuple(r[n] for n in names)==(881,881,46176,3524,81,7776,324),"work")
        require(set(r["raw"])==set(TASKS),"tasks")
        scored=dict(two_char=c.p267.score(data,r["raw"]["two_char"]),triple=c.c270.score(data,r["raw"]["triple"],c.p267),quad=transfer.score_quad(data,r["raw"]["quad"],c))
        flags={t+"_pass":scored[t]["passed"] for t in TASKS};require(all(type(v) is bool for v in flags.values()),"flags");direct={}
        for task in TASKS:
            rr=diag.normalize_task(scored[task],task,seed,arm)
            for split in ("TRAIN","HOLDOUT"):
                p=diag.partition([x for x in rr if x["split"]==split]);direct[(task,split)]=p["direct_pass"];parts.append(dict(seed=seed,arm=arm,task=task,split=split,**p))
        inv=r["fit"]["parameter_inventory"]
        results.append(dict(seed=seed,arm=arm,**flags,all_tasks_pass=all(flags.values()),fitted_train_direct_pass=all(direct[t,"TRAIN"] for t in TASKS[:2]),seen_holdout_direct_pass=all(direct[t,"HOLDOUT"] for t in TASKS[:2]),
            gradient_receiving_numel=sum(inv[n]["numel"] for n in r["fit"]["gradient_parameter_union"]),core_changed=r["core_initial_sha256"]!=r["core_final_sha256"]))
        metrics.append(dict(seed=seed,arm=arm,**scored))
    for i in range(0,15,3):check_group(records[i:i+3])
    for seed,task,split,control in itertools.product(SEEDS,TASKS,("TRAIN","HOLDOUT"),ARMS[:2]):
        x,y=[next(p for p in parts if (p["seed"],p["task"],p["split"],p["arm"])==(seed,task,split,a)) for a in (control,ARMS[2])]
        require(x["rows"]==y["rows"],"denominator");contrasts.append(dict(seed=seed,task=task,split=split,control=control,candidate=ARMS[2],rows=x["rows"],control_correct=x["correct"],candidate_correct=y["correct"]))
    counts={t:{a:sum(r[t+"_pass"] for r in results if r["arm"]==a) for a in ARMS} for t in TASKS}
    return metrics,dict(seed_results=results,final_partitions=parts,contrasts=contrasts,task_pass_counts=counts,candidate_gate=counts["quad"][ARMS[2]]==5,all_groups_matched=True,all_replays=True,**WORK)


def expected_parent_counts():
    return dict(fixed_gain=dict(unit=dict(two_char=2,triple=2,quad=2),trained=dict(two_char=2,triple=2,quad=2)),
                learned_gain=dict(unit=dict(two_char=3,triple=2,quad=1),trained=dict(two_char=3,triple=3,quad=1)))


def load_parent(paths):
    parent,p301,audit,*_,c=context();paths=[Path(p).resolve() for p in paths]
    hashes=(PARENT_SHA,parent.PARENT_SHA,*p301.parent_hashes(p301.context()[0]))
    require(len(paths)==len(hashes)==29 and all(c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)),"parent hashes")
    with audit.no_neural():
        p,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION);parent.validate_result(p);s=p["validation_summary"]
        require(p["experiment_id"]=="C302-v5b-frozen-gain-weight-cross" and p["status"]=="PASS" and p["commit_sha"]==PARENT_EXECUTION
                and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(READOUT_SOURCE)==READOUT_BLOB,"parent identity")
        require(len(p["artifacts"])==4 and {a["file"] for a in p["artifacts"]}==set(parent.OUTPUTS) and s["task_pass_counts"]==expected_parent_counts()
                and s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False and s["all_weights_preserved"] is True and s["all_hooks_restored"] is True,"parent result")
        data=[c.audit.read_json(paths[1].parent/n) for n in OUTPUTS[1:4]]
        expected=p301.context()[0].context()[0].DATA_HASHES
        require(tuple(map(digest,data))==tuple(expected),"verified C301 data")
    return p,*data


def precheck(paths,root):
    validate_seal();p,*_=load_parent(paths);parent,p301,audit,*_,c=context();ps=p301.pair_source(p301.context()[0]);root=Path(root).resolve()
    pins=dict(p["source_blobs"]);protected=dict(p["input_sha256"]);require((len(pins),len(protected))==(658,1217),"inherited counts");covered=set()
    for n,h in pins.items():require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in protected.items():require(Path(n).is_file() and c.audit.sha(n)==h,"changed input:"+n)
    for m in [parent,p301,audit,ps,*parent.context(),*vars(c).values()]:
        path=getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            n=Path(path).resolve().relative_to(root).as_posix();require(n in pins,"unprotected helper:"+n);covered.add(n)
    require(PARENT_SOURCE in covered and pins[READOUT_SOURCE]==READOUT_BLOB,"direct coverage")
    directory=Path(paths[0]).resolve().parent
    for path,h in [(directory/"summary.json",PARENT_SHA)]+[(c.audit.safe_child(directory,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h,"parent input");protected[str(path.resolve())]=h
    for n in OWN:require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins));require((len(pins),len(protected))==(664,1228),"protection counts")
    print(f"registration_check = source_pins:664; protected_inputs:1228; manifest_sha256:{MANIFEST_SHA}",flush=True);return pins,protected


def initial_probe(models,x,y):
    outputs=[];reader_grads=[]
    for m in [models[ARMS[0]].model,*models.values()]:
        m.train();m.zero_grad(set_to_none=True);torch.manual_seed(FIT_RNG);z=m(x,torch.zeros(len(x),dtype=torch.int64));F.cross_entropy(z,y).backward()
        outputs.append(z.detach());base=m.model if isinstance(m,GradientRoute) else m
        reader_grads.append(tensor_hash((n,p.grad) for n,p in base.read.named_parameters()))
    require(all(torch.equal(outputs[0],z) for z in outputs[1:]) and len(set(reader_grads))==1,"initial forward/reader-gradient identity")
    require(any(p.grad is not None and bool((p.grad!=0).any()) for p in models[ARMS[0]].backbone.core.parameters()),"full core gradient")
    for a in ARMS[1:]:require(all(p.grad is None for p in models[a].backbone.core.parameters()),"frozen core gradient")


def runtime_preflight(paths,root):
    precheck(paths,root);_,p301,*_,training,c=context();_,data,_,_=load_parent(paths);ps=p301.pair_source(p301.context()[0]);tokens,targets=training.training_tables(data,c)
    for s in SEEDS:schedule(s,data["TRAIN"],ps)
    models=make_models(SEEDS[0],c);x,y=ps.render_batch(tokens,targets,schedule(SEEDS[0],data["TRAIN"],ps)[0]);initial_probe(models,x,y)
    print("real_original_forward_and_gradient_route_preflight = PASS; science not started",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True and p["gate_f_candidate"] is False and p["production_adoption"] is False,"result identity/scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(664,1228) and set(OWN)<=set(p["source_blobs"]) and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(READOUT_SOURCE)==READOUT_BLOB,"result protection")
    require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"];rr=s["seed_results"];require([(r["seed"],r["arm"]) for r in rr]==identities(),"result cohort")
    require(all(type(r[t+"_pass"]) is bool for r in rr for t in TASKS),"result booleans")
    counts={t:{a:sum(r[t+"_pass"] for r in rr if r["arm"]==a) for a in ARMS} for t in TASKS};gate=counts["quad"][ARMS[2]]==5
    require(s["task_pass_counts"]==counts and s["candidate_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"candidate gate")
    require(s["all_groups_matched"] is True and s["all_replays"] is True and len(s["final_partitions"])==90 and len(s["contrasts"])==60,"result inventory")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"result work")


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c303-gradient-models-v1" and v["identities"]==[list(i) for i in identities()] and len(v["states"])==15,"bundle");return v["states"]


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite):yield from flatten(t)
        else:yield t


def regression_modules(root):
    names=context()[0].regression_modules(root);require(len(names)==len(set(names))==187,"parent modules");return names+["tests_lm.test_v05_c303_residual_gradient"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==4710 and ids.count(EXCLUDED)==1,"loaded suite");kept=[t for t in tests if t.id()!=EXCLUDED]
    require(len(kept)==4709,"focused suite");return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss" and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    _,p301,_,diag,evaluation,transfer,training,c=context();root=Path(__file__).resolve().parents[2];ps=p301.pair_source(p301.context()[0])
    guard(root,expected_head,c);torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(summaries,root);_,data,triple,quad=load_parent(summaries);tokens,targets=training.training_tables(data,c)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);records=[];states=[]
    for seed in SEEDS:
        models=make_models(seed,c)
        for arm in ARMS:
            print(f"[C303] model={len(records)+1}/15 seed={seed} arm={arm}",flush=True)
            r,s=train_one(models[arm],data,triple,quad,tokens,targets,seed,ps,p301,evaluation,transfer,c);records.append(r);states.append(s)
        check_group(records[-3:])
    torch.save(dict(schema="fold-c303-gradient-models-v1",identities=[list(i) for i in identities()],states=states),out/OUTPUTS[4]);states=load_bundle(out/OUTPUTS[4])
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,c)
        for j,arm in enumerate(ARMS):replay_one(models[arm],states[3*i+j],records[3*i+j],data,triple,quad,p301,evaluation,transfer,c)
    metrics,s=analyze(records,data,ps,diag,transfer,c);torch.save(dict(schema="fold-c303-gradient-eval-v1",records=records),out/OUTPUTS[5])
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],data),(OUTPUTS[2],triple),(OUTPUTS[3],quad),(OUTPUTS[6],metrics),(OUTPUTS[7],s)):(out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS];guard(root,expected_head,c);precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if s["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=s,gate_f_candidate=False,production_adoption=False)
    validate_result(p);(out/"summary.json").write_bytes(blob(p));receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","artifacts")};receipt["summary_sha256"]=c.audit.sha(out/"summary.json")
    print("=== C303 COMPACT RESULT RECEIPT ===",flush=True);print(json.dumps(receipt,indent=2,sort_keys=True),flush=True);return p


def verify_artifacts(outdir,summaries,expected_head):
    _,p301,audit,diag,_,transfer,_,c=context();out=Path(outdir);p=c.audit.read_json(out/"summary.json");validate_result(p);require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items():require(c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"]);require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with audit.no_neural():
        _,data,triple,quad=load_parent(summaries)
        for n,v in zip(OUTPUTS[1:4],(data,triple,quad),strict=True):require(c.audit.read_json(out/n)==v,"persisted data")
        v=torch.load(out/OUTPUTS[5],map_location="cpu",weights_only=True);require(set(v)=={"schema","records"} and v["schema"]=="fold-c303-gradient-eval-v1","eval schema")
        metrics,s=analyze(v["records"],data,p301.pair_source(p301.context()[0]),diag,transfer,c)
        for n,x in ((OUTPUTS[0],manifest()),(OUTPUTS[6],metrics),(OUTPUTS[7],s)):require(c.audit.read_json(out/n)==x,"persisted:"+n)
    require(s==p["validation_summary"],"summary reconstruction");return p,metrics


def main():
    p=argparse.ArgumentParser();p.add_argument("--summaries",nargs=29,type=Path,required=True);p.add_argument("--output-dir",type=Path,required=True);p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))


if __name__=="__main__":main()
