"""C319: train the native mean+last and last-only readouts from paired initial states."""
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

EXPERIMENT_ID = "C319-v5b-trained-last-readout"
STAGE = "V5-B-TRAINED-LAST-READOUT"
BASE = "b43b820b94346be08646f8f5a0d499fb7824fb27"
PARENT_EXECUTION = "f4624509c4311b3e7b04b3d861cfcb3e9d58bfd0"
PARENT_SHA = "5b838ca1420dc36b146ba4afa548d889f16172bd1d1705e4f5df97a5664c5203"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c318_readout_branch_isolation.py"
PARENT_BLOB = "5d48dd2866b8e10a286cb5d3991e6f3ea24f952d"
WIDE_SOURCE = "fold_lm/v05_benchmarks/model_c304_length_breadth.py"
WIDE_BLOB = "cacb5852a29171aa8079e634d929fdd54e7f4f58"
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
PROMPTS_SHA = "2a850d72af8c99321fd3dd4243ec2d01df6fda0bb2696329e29e3995a487fffd"
SEEDS = tuple(range(319001, 319006))
ORDERS = tuple(range(319101, 319106))
ARMS = ("mean_last", "last_only")
PROFILES = ("repeat", "shared_prefix", "shared_suffix")
SPLITS = ("TRAIN", "HOLDOUT")
STEPS = 1200
FIT_RNG = 612000
OWN = ("fold_lm/v05_benchmarks/model_c319_trained_last_readout.py",
       "tests_lm/test_v05_c319_trained_last_readout.py", "tools/run_c319.ps1", "tools/invoke_c319.ps1",
       "docs/experiment-ledger-addendum-c319-preregistration.md", "docs/v5b-trained-last-readout-v0.1.md")
OUTPUTS = ("architecture-plan.json", "dataset.json", "length-datasets.json", "trained-models.pt",
           "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10, train_steps=12000, training_rows=576000, model_forward_calls=14880,
            row_presentations=852480, core_forward_calls=59520, model_state_loads=10,
            checkpoint_bundle_loads=1, new_checkpoint_writes=1, network_calls=0)
MANIFEST_SHA = "61d98e2b6289a9e11ac0bd915df26e7e07a932895d13b2730e2d675f3b6e0a7e"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS, ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c318_readout_branch_isolation as parent
    p317, p316, x = parent.context()
    return parent, p317, p316, x


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_source=PARENT_SOURCE,
        parent_blob=PARENT_BLOB, wide_source=WIDE_SOURCE, wide_blob=WIDE_BLOB,
        seeds=list(SEEDS), orders=list(ORDERS), arms=list(ARMS),
        question="does training last-only from initialization retain unseen-six reliability compared with native mean-plus-last",
        intervention="replace only the first native query input by the last-byte local state,with autograd intact,throughout training/evaluation/replay",
        parameters=14256, core_parameters=3328, slots=64, train_lengths=[2,3,4], row_exposures=[0,100,100,100],
        steps_per_model=STEPS, fit_rng=FIT_RNG, loss="ordinary mean CE", core_lr=.0005, other_lr=.005,
        optimizer="AdamW betas.9/.999 eps1e-8 weight_decay0;global gradient clip1 before step",
        coefficient="two identical native last attentions averaged .5;total memory coefficient1,not norm matching or compute saving",
        parent_reuse="C315 plan/evaluate/replay;C308 optimizer;actual C304 forward;no parent mutation or pretrained state reuse",
        primary="ALL5 new last_only states pass every existing six-character local/masked criterion",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        data_sha256=DATA_SHA, prompts_sha256=PROMPTS_SHA, eval_lengths=[1,2,3,4,5,6],
        limits="fresh initialization/order,not fresh tasks;one trained alternative,not universal necessity;no old gate rewrite or seed search",
        single_character="untrained single canonical profile,descriptive only in both arms",
        parents=45, source_pins=760, protected_inputs=1429, own_tests=24, modules=204,
        loaded_tests=5198, focused_tests=5197, excluded_test=EXCLUDED,
        dtype="CPU float64", threads=2, deterministic=True, gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA, "manifest seal")


def parent_counts():
    return {m:{str(n):{a:v[i] for a,v in arms.items()} for i,n in enumerate(range(2,7))} for m,arms in {
        "original_before":{"two_to_four":[5,5,5,5,4],"one_to_four":[5,5,5,5,4]},
        "mean_only":{"two_to_four":[4,0,0,0,0],"one_to_four":[2,0,0,0,0]},
        "last_only":{"two_to_four":[5,5,5,3,2],"one_to_four":[5,4,5,4,0]}}.items()}


def parent_hashes(parent, p317, p316, x):
    return (PARENT_SHA, *parent.parent_hashes(p317, p316, x))


def load_parent(paths):
    parent,p317,p316,x=context(); paths=[Path(p).resolve() for p in paths]
    hashes=parent_hashes(parent,p317,p316,x)
    require(len(paths)==len(hashes)==45 and all(x.c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)), "45 parent hashes")
    with x.guarded.no_neural():
        evidence,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); parent.validate_result(evidence)
        require(evidence["experiment_id"]=="C318-v5b-frozen-readout-branches" and evidence["commit_sha"]==PARENT_EXECUTION
                and evidence["status"]=="PASS" and evidence["capability_gate_applicable"] is False, "diagnostic parent semantics")
        require(len(evidence["artifacts"])==4 and {a["file"] for a in evidence["artifacts"]}==set(parent.OUTPUTS)
                and evidence["validation_summary"]["length_pass_counts"]==parent_counts(), "parent artifacts/outcomes")
        _,data,prompts,_=parent.load_parent(paths[1:])
        require(digest(data)==DATA_SHA and digest(prompts)==PROMPTS_SHA, "canonical inputs")
    return evidence,data,prompts


def precheck(paths,root):
    validate_seal(); parent,p317,p316,x=context(); evidence,_,_=load_parent(paths); root=Path(root).resolve()
    pins,inputs=dict(evidence["source_blobs"]),dict(evidence["input_sha256"])
    require((len(pins),len(inputs))==(754,1418) and pins.get(PARENT_SOURCE)==PARENT_BLOB
            and pins.get(WIDE_SOURCE)==WIDE_BLOB, "inherited protection")
    for m in [parent,p317,p316,x.parent,*x.parent.context(),*x.p312.context(),*x.wide.context(),*vars(x.c).values(),x.c.factory.language_module()]:
        name=getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if name and Path(name).resolve().is_relative_to(root):
            require(Path(name).resolve().relative_to(root).as_posix() in pins, "unprotected helper")
    for n,h in pins.items(): require(x.c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h, "changed source:"+n)
    for n,h in inputs.items(): require(Path(n).is_file() and x.c.audit.sha(n)==h, "changed input:"+n)
    folder=Path(paths[0]).resolve().parent
    for path,h in [(folder/"summary.json",PARENT_SHA)]+[(x.c.audit.safe_child(folder,a["file"]),a["sha256"]) for a in evidence["artifacts"]]:
        require(str(path.resolve()) not in inputs and x.c.audit.sha(path)==h, "parent input"); inputs[str(path.resolve())]=h
    for n in OWN:
        require(n not in pins,"OWN collision"); pins[n]=x.c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    inputs.update(x.c.audit.protect_tree_files(root,pins))
    require((len(pins),len(inputs))==(760,1429), "protection counts")
    require(x.policy.CORE_LR==.0005 and x.policy.BASE_LR==.005 and x.parent.STEPS==1200 and x.parent.FIT_RNG==FIT_RNG, "optimizer policy")
    print(f"registration_check = source_pins:760; protected_inputs:1429; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,inputs


def hook_snapshot(model):
    attrs=("_forward_pre_hooks","_forward_hooks","_forward_pre_hooks_with_kwargs","_forward_hooks_with_kwargs","_forward_hooks_always_called")
    return [(n,tuple(tuple(getattr(m,a)) for a in attrs)) for n,m in model.named_modules()]


@contextmanager
def trained_readout(model,wide,arm):
    """Use the selected policy consistently;unlike C318,never detach the selected representation."""
    require(arm in ARMS, "readout policy")
    original=hook_snapshot(model); handles=[]; state={}
    stats=dict(calls=0,query_calls=0,rows=0,grad_calls=0)
    def begin(module,args):
        require(not state and len(args)==2,"nonreentrant forward")
        tokens=args[0]; span=wide.span_mask(tokens); valid=tokens!=256
        require(tokens.shape[1]==64 and span.shape==tokens.shape and span.dtype==torch.bool and bool(span.any(1).all()),"visible span")
        pos=torch.arange(64,device=tokens.device).expand_as(tokens)
        state.update(valid=valid,span=span,last=torch.where(span,pos,-1).max(1).values,q=0,grad=torch.is_grad_enabled())
        stats["calls"]+=1; stats["rows"]+=len(tokens); stats["grad_calls"]+=int(state["grad"])
    def capture(module,args,out):
        require(state and "local" not in state and isinstance(out,(tuple,list)),"one encoder capture")
        local=out[0]*state["valid"].unsqueeze(-1).to(out[0].dtype)
        require(local.shape==(*state["valid"].shape,16) and local.dtype==torch.float64 and local.device.type=="cpu"
                and bool(torch.isfinite(local).all()),"local representation")
        if state["grad"]: require(local.requires_grad,"selected representation was detached")
        state["local"]=local
        state["mean"]=(local*state["span"][:,:,None]).sum(1)/state["span"].sum(1,keepdim=True).to(local.dtype)
        state["last_state"]=local[torch.arange(len(local)),state["last"]]
    def query(module,args):
        require("local" in state and len(args)==1 and state["q"] in (0,1),"two native queries")
        index=state["q"]; expected=state["mean"] if index==0 else state["last_state"]
        require(torch.equal(args[0],expected),"native query provenance")
        state["q"]+=1; stats["query_calls"]+=1
        if arm=="last_only" and index==0:
            if state["grad"]: require(state["last_state"].requires_grad,"last input gradient")
            return (state["last_state"],)
        return None
    def finish(module,args,out):
        try:
            if out is not None: require(state.get("q")==2,"query coverage")
        finally: state.clear()
    try:
        handles.append(model.register_forward_pre_hook(begin)); handles.append(model.backbone.local_encoder.register_forward_hook(capture))
        handles.append(model.read.query.register_forward_pre_hook(query)); handles.append(model.register_forward_hook(finish,always_call=True))
        yield stats
        require(stats["calls"]>0 and stats["query_calls"]==2*stats["calls"] and not state,"policy coverage")
    finally:
        for h in handles: h.remove()
        state.clear(); require(hook_snapshot(model)==original,"hook restoration")


def schedule(seed,data,x):
    require(seed in SEEDS,"fresh seed")
    e=x.parent.plan_for_order(ORDERS[SEEDS.index(seed)],"two_to_four",data["TRAIN"],x.p312,x.pairs)
    st=x.parent.schedule_stats(e)
    require(st["per_length_row_exposures"]==[[k]*192 for k in (0,100,100,100)]
            and all(sorted(e[4*i:4*i+4,:,2:].flatten().tolist())==list(range(192)) for i in range(300)),"fixed TRAIN allocation")
    return e


def make_models(seed,x):
    require(seed in SEEDS,"fresh model seed")
    c=x.c; reference=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    template=x.wide.LengthReadout(reference)
    models={arm:x.policy.configure(copy.deepcopy(template),"core_slow") for arm in ARMS}; used=set()
    for model in models.values():
        require(type(model) is x.wide.LengthReadout and model.backbone.config.max_tokens==64 and model.backbone.core.config.slots==64,"model/frame")
        require(sum(p.numel() for p in model.parameters())==14256 and sum(p.numel() for p in model.backbone.core.parameters())==3328,"capacity")
        require(list(model.state_dict())==list(reference.state_dict()) and c.base.fingerprint(model)==c.base.fingerprint(reference),"initial state")
        require(all(p.requires_grad and p.dtype==torch.float64 and p.device.type=="cpu" for p in model.parameters()),"trainable precision")
        pointers={p.data_ptr() for p in model.parameters()}; require(not used&pointers,"independent storage"); used.update(pointers)
        x.policy.parameter_groups(model,"core_slow")
    return models


def optimize(model,tables,targets,events,x,label):
    require(events.shape==(1200,24,4) and events.dtype==torch.int64 and set(tables)=={(n,p) for n in (2,3,4) for p in PROFILES},"training tables/schedule")
    require(all(t.shape==(192,64) and t.dtype==torch.int64 for t in tables.values()) and targets.shape==(192,) and targets.dtype==torch.int64,"training shapes")
    torch.manual_seed(FIT_RNG); opt=x.policy.optimizer_for(model,"core_slow"); model.train()
    losses=[]; rates=[]; counts=[]; union={}
    for step,event in enumerate(events):
        x.policy.verify_optimizer(opt,model,"core_slow"); rates.append([g["lr"] for g in opt.param_groups]); opt.zero_grad(set_to_none=True)
        n,p=map(int,event[0,:2]); ids=event[:,2:].flatten()
        z=model(tables[n,PROFILES[p]][ids],torch.zeros(48,dtype=torch.int64))
        require(z.shape==(48,256) and z.dtype==torch.float64 and z.device.type=="cpu" and bool(torch.isfinite(z).all()),"training logits")
        loss=F.cross_entropy(z,targets[ids]); require(bool(torch.isfinite(loss)),"finite loss"); losses.append(float(loss.detach()))
        loss.backward(); got={name:p.numel() for name,p in model.named_parameters() if p.grad is not None}; union.update(got); counts.append(sum(got.values()))
        torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True); opt.step()
        if (step+1)%200==0: print(f"[C319] {label} step={step+1}/1200 ce={losses[-1]:.6f}",flush=True)
    model.eval()
    return dict(steps=1200,training_rows=57600,fit_rng=FIT_RNG,optimizer_creations=1,trainable_parameters=14256,
        ce_history=losses,optimizer_group_lrs=rates,gradient_parameter_counts=counts,gradient_union=dict(sorted(union.items())),
        schedule_events=events,**x.parent.schedule_stats(events))


def check_fit(f,seed,data,x):
    require(all(type(f[k]) is int and f[k]==v for k,v in dict(steps=1200,training_rows=57600,fit_rng=FIT_RNG,optimizer_creations=1,trainable_parameters=14256).items()),"fit metadata")
    e=schedule(seed,data,x)
    require(torch.equal(f["schedule_events"],e) and all(f[k]==v for k,v in x.parent.schedule_stats(e).items()),"fit schedule")
    require(f["optimizer_group_lrs"]==[[.005,.0005]]*1200 and len(f["ce_history"])==1200
            and all(type(v) in (float,int) and math.isfinite(v) and v>=0 for v in f["ce_history"]),"fit numeric policy")
    u=f["gradient_union"]; require(u and all(type(n) is str and type(v) is int and v>0 for n,v in u.items()) and sum(u.values())<=14256,"gradient union")
    require(len(f["gradient_parameter_counts"])==1200 and all(type(v) is int and 0<v<=sum(u.values()) for v in f["gradient_parameter_counts"]),"gradient trace")


def train_one(model,data,prompts,tables,y,seed,arm,x):
    require(seed in SEEDS and arm in ARMS and torch.equal(y,torch.tensor([r["target"] for r in data["TRAIN"]])),"training identity/labels")
    c=x.c; initial=c.base.fingerprint(model); core_initial=c.base.fingerprint(model.backbone.core); old_hooks=hook_snapshot(model)
    with c.p267.counted(model,c.core) as (calls,cores),trained_readout(model,x.wide,arm) as stats:
        f=optimize(model,tables,y,schedule(seed,data,x),x,f"seed={seed} arm={arm}")
        final=c.base.fingerprint(model); core_final=c.base.fingerprint(model.backbone.core)
        model.requires_grad_(False); raw=x.parent.evaluate(model,prompts,data,x.wide,c)
    require(calls==[1344,71424] and cores[0]==5376 and stats==dict(calls=1344,query_calls=2688,rows=71424,grad_calls=1200),"train/eval policy work")
    require(initial!=final and core_initial!=core_final and c.base.fingerprint(model)==final and hook_snapshot(model)==old_hooks,"learned/preserved state")
    return dict(seed=seed,arm=arm,readout_policy=arm,initial_sha256=initial,core_initial_sha256=core_initial,
        final_sha256=final,core_final_sha256=core_final,fit=f,raw=raw,policy_receipt=dict(stats),
        forward_calls=1344,row_presentations=71424,core_forward_calls=5376),{n:z.detach().cpu().clone() for n,z in model.state_dict().items()}


def replay(model,state,r,data,prompts,x):
    require(r["readout_policy"]==r["arm"] and r["arm"] in ARMS,"replay readout identity")
    with trained_readout(model,x.wide,r["arm"]) as stats:
        x.parent.replay(model,state,r,data,prompts,x.wide,x.c)
    require(stats==dict(calls=144,query_calls=288,rows=13824,grad_calls=0),"replay policy work")
    r["replay_policy_receipt"]=dict(stats)


def analyze(records,data,x):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"complete fresh cohort")
    metrics=[]; results=[]; parts=[]; single=[]
    for r in records:
        check_fit(r["fit"],r["seed"],data,x); x.parent.validate_raw(r["raw"],data,x.c)
        require(r["readout_policy"]==r["arm"] and r["policy_receipt"]==dict(calls=1344,query_calls=2688,rows=71424,grad_calls=1200)
                and r["replay_policy_receipt"]==dict(calls=144,query_calls=288,rows=13824,grad_calls=0),"consistent learning/inference policy")
        require(r["initial_sha256"]!=r["final_sha256"] and r["core_initial_sha256"]!=r["core_final_sha256"] and r["checkpoint_roundtrip"] is True,"learned model")
        error=r["reload_max_error"]; require(type(error) in (int,float) and math.isfinite(error) and 0<=error<=1e-9,"strict replay")
        keys=("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in keys) and tuple(r[k] for k in keys)==(1344,71424,5376,144,13824,576),"work record")
        scores={str(n):x.wide.score_length(data,r["raw"][str(n)],x.c) for n in range(2,7)}; flags={n:z["passed"] for n,z in scores.items()}
        require(all(type(v) is bool for v in flags.values()),"gate types")
        key=dict(seed=r["seed"],arm=r["arm"])
        for n in range(2,7):
            norm=x.diag.normalize_task(scores[str(n)],"triple",r["seed"],r["arm"])
            for s in SPLITS: parts.append(dict(**key,identifier_length=n,split=s,length_trained=n in (2,3,4),**x.diag.partition([v for v in norm if v["split"]==s])))
        for s in SPLITS:
            views=r["raw"]["1"][s]["repeat"]; y=torch.tensor([v["target"] for v in data[s]])
            single.append(dict(**key,split=s,rows=len(y),length_trained=False,capability_gate_applicable=False,
                correct_by_view={v:int((z.argmax(1)==y).sum()) for v,z in views.items()},normal_nll=float(F.cross_entropy(views["normal"],y))))
        results.append(dict(**key,length_pass=flags,six_pass=flags["6"],all_2_to_6_pass=all(flags.values()))); metrics.append(dict(**key,length_scores=scores))
    for i in range(5):
        a,z=records[2*i:2*i+2]
        require(all(a[k]==z[k] for k in ("initial_sha256","core_initial_sha256")) and a["fit"]["event_sha256"]==z["fit"]["event_sha256"],"paired initial state/rendered order")
    counts={str(n):{a:sum(r["length_pass"][str(n)] for r in results if r["arm"]==a) for a in ARMS} for n in range(2,7)}
    paired=dict(both_pass=0,control_only=0,candidate_only=0,both_fail=0)
    for i in range(5):
        a,z=[r["six_pass"] for r in results[2*i:2*i+2]]; paired["both_pass" if a and z else "control_only" if a else "candidate_only" if z else "both_fail"]+=1
    return metrics,dict(seed_results=results,final_partitions=parts,single_character_diagnostics=single,length_pass_counts=counts,
        paired_six=paired,candidate_gate=counts["6"]["last_only"]==5,all_pairs_matched=True,all_replays=True,**WORK)


def runtime_preflight(paths,root):
    torch.set_num_threads(2); precheck(paths,root); parent,_,_,x=context(); _,data,prompts=load_parent(paths)
    for seed in SEEDS: schedule(seed,data,x)
    all_tables,y=x.parent.training_tables(data,prompts,x.wide); models=make_models(SEEDS[0],x)
    ids=[next(i for i,r in enumerate(data["TRAIN"]) if r["language"]==lang) for lang in ("en","ja")]
    tokens=torch.cat([all_tables[n,"repeat"][ids] for n in (2,4)]); tasks=torch.zeros(len(tokens),dtype=torch.int64)
    # Make only discarded probes nonzero so a zero-initialized readout cannot make the check vacuous.
    probe=copy.deepcopy(models["mean_last"])
    with torch.no_grad():
        v=torch.arange(probe.read.output.weight.numel(),dtype=torch.float64).reshape_as(probe.read.output.weight)
        probe.read.output.weight.copy_(torch.sin(v)*.03)
    probe.eval(); probe.requires_grad_(False)
    with torch.no_grad():
        for arm in ARMS:
            with parent.branch_probe(probe,x.wide,"original_before" if arm=="mean_last" else "last_only"): expected=probe(tokens,tasks)
            with trained_readout(probe,x.wide,arm): actual=probe(tokens,tasks)
            require(torch.equal(expected,actual),"accepted C318 forward equivalence")
    for arm in ARMS:
        m=copy.deepcopy(probe).requires_grad_(True).train(); m.zero_grad(set_to_none=True)
        with trained_readout(m,x.wide,arm): z=m(tokens,tasks)
        F.cross_entropy(z,y[ids].repeat(2)).backward()
        require(m.read.query.weight.grad is not None and all(p.grad is None or bool(torch.isfinite(p.grad).all()) for p in m.parameters()),"differentiable readout")
    print("real_trained_branch_probe = PASS; no scientific training started",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True
            and p["gate_f_candidate"] is False and p["production_adoption"] is False,"result scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(760,1429) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(WIDE_SOURCE)==WIDE_BLOB,"result protection")
    require(len(p["artifacts"])==7 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"]; rr=s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rr]==identities() and all(set(r["length_pass"])==set(map(str,range(2,7)))
            and all(type(v) is bool for v in r["length_pass"].values()) and r["six_pass"] is r["length_pass"]["6"]
            and r["all_2_to_6_pass"] is all(r["length_pass"].values()) for r in rr),"result gates/cohort")
    counts={str(n):{a:sum(r["length_pass"][str(n)] for r in rr if r["arm"]==a) for a in ARMS} for n in range(2,7)}; gate=counts["6"]["last_only"]==5
    require(s["length_pass_counts"]==counts and s["candidate_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"candidate six gate")
    require(len(s["final_partitions"])==100 and len(s["single_character_diagnostics"])==20 and s["all_pairs_matched"] is True and s["all_replays"] is True,"coverage")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"work")


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==203,"parent modules")
    return names+["tests_lm.test_v05_c319_trained_last_readout"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==5198 and ids.count(EXCLUDED)==1,"loaded suite")
    return unittest.TestSuite(t for t in tests if t.id()!=EXCLUDED)


def load_bundle(path):
    p=torch.load(path,map_location="cpu",weights_only=True)
    require(set(p)=={"schema","identities","states"} and p["schema"]=="fold-c319-trained-readout-models-v1"
            and p["identities"]==[list(v) for v in identities()] and len(p["states"])==10,"checkpoint policy/identity")
    return p["states"]


def run(*,summaries,output_dir,expected_head):
    torch.set_num_threads(2); torch.use_deterministic_algorithms(True); parent,p317,_,x=context(); root=Path(__file__).resolve().parents[2]
    p317.guard(root,expected_head,x.c); pins,inputs=precheck(summaries,root); _,data,prompts=load_parent(summaries)
    full,y=x.parent.training_tables(data,prompts,x.wide); tables={k:v for k,v in full.items() if k[0] in (2,3,4)}
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False); records=[]; states=[]
    for seed in SEEDS:
        models=make_models(seed,x)
        for arm in ARMS:
            r,state=train_one(models[arm],data,prompts,tables,y,seed,arm,x); records.append(r); states.append(state)
    torch.save(dict(schema="fold-c319-trained-readout-models-v1",identities=[list(v) for v in identities()],states=states),out/"trained-models.pt")
    saved=load_bundle(out/"trained-models.pt")
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,x)
        for j,arm in enumerate(ARMS): replay(models[arm],saved[2*i+j],records[2*i+j],data,prompts,x)
    metrics,s=analyze(records,data,x); torch.save(dict(schema="fold-c319-trained-readout-eval-v1",records=records),out/"evaluations.pt")
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],data),(OUTPUTS[2],prompts),(OUTPUTS[5],metrics),(OUTPUTS[6],s)): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=x.c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    p317.guard(root,expected_head,x.c); precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if s["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=inputs,artifacts=artifacts,validation_summary=s,gate_f_candidate=False,production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    print("=== C319 COMPACT EXPERIMENT RECEIPT ===",flush=True)
    print(json.dumps(dict(experiment_id=EXPERIMENT_ID,commit_sha=expected_head,status=p["status"],summary_sha256=x.c.audit.sha(out/"summary.json"),artifacts=artifacts),indent=2),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    _,_,_,x=context(); out=Path(outdir); p=x.c.audit.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items(): require(x.c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=x.c.audit.safe_child(out,a["file"]); require(x.c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with x.guarded.no_neural():
        _,data,prompts=load_parent(summaries); archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c319-trained-readout-eval-v1","evaluation schema")
        metrics,s=analyze(archive["records"],data,x)
        for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],data),(OUTPUTS[2],prompts),(OUTPUTS[5],metrics),(OUTPUTS[6],s)):
            require(x.c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==s,"summary reconstruction"); return p,metrics


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--summaries",nargs=45,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True); parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
