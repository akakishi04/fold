"""C304: length breadth at common maximum4,1200 updates,and a shared64-slot frame."""
from __future__ import annotations
import argparse
from collections import Counter
import copy
from dataclasses import replace
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
from types import ModuleType
import unittest
import torch
from torch import nn
from torch.nn import functional as F

EXPERIMENT_ID = "C304-v5b-length-breadth-to-five"
STAGE = "V5-B-LENGTH-BREADTH-TO-FIVE"
BASE = "c8ccecbbfbb74cffb520ed4da507c9f7b8c0623b"
PARENT_EXECUTION = "8e01ac5bb1dae57f129615731b7013eed43b5719"
PARENT_SHA = "33d3370d383d8f220cea46056cb0fefdae27498794110fb7672bca726bc45d01"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c303_residual_gradient.py"
PARENT_BLOB = "0a59fd58ad89e460976f64218460c6de17ef8228"
PINNED = {
    PARENT_SOURCE:PARENT_BLOB,
    "fold_lm/v05/language_task.py":"587162ffc35e1d854fa8d8577740a1e034537de2",
    "fold_lm/v05/modules.py":"3413c2de62e83dbf4a98af044a5ac2b242c99f87",
    "fold_lm/v05_benchmarks/model_c278_mean_final_dual_query.py":"0aa8d65874f4a021e21d04948ffd0a1d5615248b",
    "fold_lm/v05_benchmarks/model_c269_query_span_pooling.py":"eb8e441e442530e377c5aad1db0c05552288c5d7",
    "fold_lm/v05_benchmarks/model_c270_frozen_triple_identifiers.py":"88b94c92267b916b304ecd44a8d02f89ab0eb301",
    "fold_lm/v05_benchmarks/model_c267_name_coverage_training.py":"5a167f078ab5b3aa8052e7995d004a25ca25fc0f",
}
SEEDS = tuple(range(304001,304006))
ORDERS = tuple(range(304101,304106))
LENGTHS = {"four_only":(4,),"three_four":(3,4),"two_three_four":(2,3,4)}
ARMS = tuple(LENGTHS)
EVAL_LENGTHS = (2,3,4,5)
PROFILES = ("repeat","shared_prefix","shared_suffix")
LEGACY_PROFILES = {2:("doubled","shared_prefix","shared_suffix"),3:("tripled","shared_prefix2","shared_suffix2"),4:("quadrupled","shared_prefix3","shared_suffix3")}
SPLITS = ("TRAIN","HOLDOUT")
VIEWS = ("normal","evidence_blind","query_blind")
SLOTS, STEPS, FIT_RNG = 64,1200,608000
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
OWN = ("fold_lm/v05_benchmarks/model_c304_length_breadth.py","tests_lm/test_v05_c304_length_breadth.py",
       "tools/run_c304.ps1","tools/invoke_c304.ps1","docs/experiment-ledger-addendum-c304-preregistration.md","docs/v5b-length-breadth-v0.1.md")
OUTPUTS = ("architecture-plan.json","dataset.json","length-datasets.json","trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=15,train_steps=18000,training_rows=864000,model_forward_calls=21240,row_presentations=1175040,
            core_forward_calls=84960,model_state_loads=15,checkpoint_bundle_loads=1,new_checkpoint_writes=1,network_calls=0)
MANIFEST_SHA = "af8f2ffc7b04e27bdd3597ede0d5b2cd55b6b6b526238dabf11a1b17f3edd9a0"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c303_residual_gradient as parent
    _,p301,audit,diagnostic,_,transfer,_,c = parent.context()
    return parent,p301,audit,diagnostic,transfer,c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        parent_summary_sha256=PARENT_SHA,pinned=PINNED,seeds=list(SEEDS),orders=list(ORDERS),arms={a:list(ls) for a,ls in LENGTHS.items()},
        question="does broader length coverage improve unseen five-character reliability at a common trained maximum4 and1200updates",
        parameters=14256,core_parameters=3328,slots=SLOTS,old_slots=48,max_prompt_bytes=52,max_encoded_tokens=54,
        context_policy="all arms64;clone48 backbone/reader weights;replace only backbone.max_tokens/core.slots configs;no truncation/new vocabulary",
        readout="child slot-generalized C278 mean/final dual query;all-valid pre-core memory;post-core residual;full backward",
        compatibility="TRAIN-only48-vs64 logits and gradients<=1e-9,exact argmax;nonzero-reader software control;old2/3/4 renderers byte-exact",
        training="ordinary full CE;one AdamW;lr.005;betas.9/.999;eps1e-8;weight_decay0;clip1",fit_rng=FIT_RNG,steps=STEPS,
        schedule="300 epochs*4;shared private randperm96(order+304000+epoch);length=arm[epoch%len(arm)];profile=(epoch//3+epoch%3)%3",
        per_row_length_exposure={ARMS[0]:[0,0,300],ARMS[1]:[0,150,150],ARMS[2]:[100,100,100]},
        profile_updates=[400,400,400],maximum_training_length=4,eval_lengths=list(EVAL_LENGTHS),data_sha256=DATA_SHA,
        primary="all five two_three_four models pass every original-style five-character local/masked criterion",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        interpretation="length coverage/allocation and ordering differ;max length,total updates,profile exposure held;not arbitrary-length-rule proof",
        old_gate_status="C303 negative and GateF remain unchanged;four-character task is now trained in every arm",
        parents=30,source_pins=670,protected_inputs=1243,own_tests=40,modules=189,loaded_tests=4750,focused_tests=4749,excluded_test=EXCLUDED,
        partitions=120,contrasts=80,dtype="CPU float64",threads=2,deterministic=True,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def prefix_tensor(text,slots=SLOTS):
    require(isinstance(text,str) and bool(text) and type(slots) is int and slots in (48,SLOTS),"prefix contract")
    raw=text.encode("utf-8"); require(len(raw)+2<=slots,"context overflow: never truncate")
    return torch.tensor([257,*raw,258,*([256]*(slots-len(raw)-2))],dtype=torch.int64)


def name_map(row,length,profile):
    require(type(length) is int and length in EVAL_LENGTHS and profile in PROFILES and row["language"] in ("en","ja"),"render policy")
    chars=("a","b","c") if row["language"]=="en" else ("甲","乙","丙")
    i,j=row["entities"];u,v=chars[i],chars[j]
    return {i:u*length,j:v*length if profile==PROFILES[0] else u*(length-1)+v if profile==PROFILES[1] else v+u*(length-1)}


def render(row,length,profile,view="normal"):
    require(view in VIEWS,"view")
    ns=name_map(row,length,profile);values=dict(zip(row["entities"],row["values"],strict=True))
    return ";".join(ns[k]+"="+("?" if view=="evidence_blind" else str(values[k])) for k in row["permutation"])+";"+("?" if view=="query_blind" else ns[row["query"]])+"="


def prompt_dataset(data):
    return {str(n):{s:{p:[dict(source_id=r["id"],target=r["target"],views={v:render(r,n,p,v) for v in VIEWS})
                for r in data[s]] for p in PROFILES} for s in SPLITS} for n in EVAL_LENGTHS}


def validate_prompts(prompts,data,c,transfer):
    c.p267.validate_data(data);require(digest(data)==DATA_SHA and prompts==prompt_dataset(data),"prompt identity")
    all_normal=[];old_bytes=set();new_bytes=set();longest=0
    renderers={2:c.p267.render,3:c.c270.render,4:transfer.render}
    for n,s,p in itertools.product(EVAL_LENGTHS,SPLITS,PROFILES):
        for r,item in zip(data[s],prompts[str(n)][s][p],strict=True):
            require(all(len(name)==n for name in name_map(r,n,p).values()),"identifier length")
            for v,text in item["views"].items():
                x=prefix_tensor(text);raw=text.encode("utf-8");longest=max(longest,len(raw))
                require(x.shape==(SLOTS,) and x[len(raw)+1]==258,"boundary")
                if n<=4:
                    require(text==renderers[n](r,LEGACY_PROFILES[n][PROFILES.index(p)],v),"old renderer drift")
                    old_bytes.update(raw)
                else:new_bytes.update(raw)
            all_normal.append(item["views"]["normal"])
    require(longest==52 and new_bytes<=old_bytes and len(all_normal)==len(set(all_normal))==3456,"bounded novel coverage")


def training_tables(data):
    require(digest(data)==DATA_SHA,"registered data")
    x=torch.stack([torch.stack([torch.stack([prefix_tensor(render(r,n,p)) for r in data["TRAIN"]]) for p in PROFILES]) for n in (2,3,4)])
    y=torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)
    require(x.shape==(3,3,192,SLOTS) and y.shape==(192,),"TRAIN tables")
    return x,y


def span_mask(tokens):
    require(tokens.dtype==torch.int64 and tokens.ndim==2 and tokens.shape[1] in (48,SLOTS),"span tokens")
    valid=tokens!=256;eos=valid.sum(1)-1;rows=torch.arange(len(tokens),device=tokens.device)
    require(bool((eos>=4).all()) and bool((tokens[rows,eos]==258).all()),"span EOS")
    eq=eos-1;require(bool((tokens[rows,eq]==61).all()),"last equals")
    pos=torch.arange(tokens.shape[1],device=tokens.device).expand(len(tokens),-1)
    semi=(tokens==59)&valid&(pos<eq[:,None]);last=torch.where(semi,pos,torch.full_like(pos,-1)).max(1).values
    require(bool((last>=1).all()),"last separator")
    mask=(pos>last[:,None])&(pos<eq[:,None])&valid
    require(bool(mask.any(1).all()) and not bool((((tokens==59)|(tokens==61))&mask).any()),"visible query")
    return mask


class LengthReadout(nn.Module):
    """C278 numerical path with a configurable frame; preserves parameter names and ordering."""
    def __init__(self,reference,slots=SLOTS):
        super().__init__();require(slots in (48,SLOTS),"supported frame")
        self.backbone=copy.deepcopy(reference.backbone);self.read=copy.deepcopy(reference.read);self.family="full"
        self.backbone.config=replace(self.backbone.config,max_tokens=slots)
        self.backbone.core.config=replace(self.backbone.core.config,slots=slots)
        require(sum(p.numel() for p in self.parameters())==14256 and self.backbone.config.width==16,"capacity")
    def forward(self,tokens,tasks):
        slots=self.backbone.config.max_tokens
        require(tokens.dtype==tasks.dtype==torch.int64 and tokens.ndim==2 and tokens.shape[1]==slots and tasks.shape==(len(tokens),) and bool((tasks==0).all()),"forward contract")
        valid=tokens!=256;eos=valid.sum(1)-1;rows=torch.arange(len(tokens),device=tokens.device)
        require(bool((tokens[rows,eos]==258).all()),"EOS")
        span=span_mask(tokens);pos=torch.arange(slots,device=tokens.device).expand(len(tokens),-1)
        final=torch.where(span,pos,torch.full_like(pos,-1)).max(1).values
        require(bool(span[rows,final].all()),"last query byte")
        local=[];nxt=[];routes=Counter();norm=[0];handles=[]
        def lh(m,a,o):local.append(o[0]*valid.unsqueeze(-1).to(o[0].dtype))
        def ch(m,a,k,o):
            route=k.get("route_index");require(len(local)==1 and len(a)==2 and torch.equal(a[1],local[0]),"pre-core context")
            routes[route]+=1
            if route==self.backbone.config.next_route:nxt.append(o)
        def nh(m,a):
            norm[0]+=1;cfg=self.backbone.config;post=a[0]
            require(routes=={cfg.next_route:cfg.internal_steps,cfg.instruction_route:cfg.internal_steps},"core routes")
            require(len(nxt)==cfg.internal_steps and torch.equal(nxt[-1][rows,eos],post),"residual provenance")
            mean=(local[0]*span[:,:,None]).sum(1)/span.sum(1,keepdim=True).to(local[0].dtype)
            keys=self.read.key(local[0]);qm=self.read.query(mean);qf=self.read.query(local[0][rows,final])
            sm=(keys*qm[:,None,:]).sum(-1)/4.0;sf=(keys*qf[:,None,:]).sum(-1)/4.0
            am=sm.masked_fill(~valid,float("-inf")).softmax(-1);af=sf.masked_fill(~valid,float("-inf")).softmax(-1)
            memory=((am[:,:,None]*local[0]).sum(1)+(af[:,:,None]*local[0]).sum(1))*.5
            return (post+self.read.output(memory),)
        try:
            handles.append(self.backbone.local_encoder.register_forward_hook(lh))
            handles.append(self.backbone.core.register_forward_hook(ch,with_kwargs=True))
            handles.append(self.backbone.readout_norm.register_forward_pre_hook(nh));out=self.backbone(tokens,tasks)
        finally:
            for h in handles:h.remove()
        require(norm[0]==1 and out.shape==(len(tokens),256) and bool(torch.isfinite(out).all()),"output")
        return out


def make_models(seed,c):
    require(seed in SEEDS,"seed")
    ref=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    template=LengthReadout(ref);models={a:copy.deepcopy(template) for a in ARMS};used=set()
    for m in models.values():
        require(list(m.state_dict())==list(ref.state_dict()) and c.base.fingerprint(m)==c.base.fingerprint(ref),"initial state")
        require(all(p.dtype==torch.float64 and p.device.type=="cpu" and p.requires_grad for p in m.parameters()),"full learning")
        ptrs={p.data_ptr() for p in m.parameters()};require(not ptrs&used,"independent storage");used.update(ptrs)
    return models


def compatibility_probe(reference,data):
    """Operational TRAIN-only probe; deliberately nonzero reader prevents a vacuous zero-head test."""
    ref=copy.deepcopy(reference);wide=LengthReadout(ref)
    with torch.no_grad():
        values=torch.arange(ref.read.output.weight.numel(),dtype=torch.float64).reshape_as(ref.read.output.weight)
        ref.read.output.weight.copy_(torch.sin(values)*.03);wide.read.output.weight.copy_(ref.read.output.weight)
    texts=[render(data["TRAIN"][i],n,p,v) for i in (0,4) for n in (2,3,4) for p in PROFILES for v in VIEWS]
    x48=torch.stack([prefix_tensor(t,48) for t in texts]);x64=torch.stack([prefix_tensor(t) for t in texts])
    y=torch.tensor([48+(i%4) for i in range(len(texts))]);zs=[];gs=[]
    for m,x in ((ref,x48),(wide,x64)):
        m.train();m.zero_grad(set_to_none=True);z=m(x,torch.zeros(len(x),dtype=torch.int64));F.cross_entropy(z,y).backward()
        zs.append(z.detach());gs.append({n:None if p.grad is None else p.grad.detach().clone() for n,p in m.named_parameters()})
    require(torch.equal(zs[0].argmax(1),zs[1].argmax(1)) and torch.allclose(zs[0],zs[1],atol=1e-9,rtol=0),"48/64 outputs")
    require(gs[0].keys()==gs[1].keys(),"gradient keys")
    max_grad=0.
    for n,g in gs[0].items():
        h=gs[1][n];require((g is None)==(h is None),"gradient connectivity")
        if g is not None:
            require(torch.allclose(g,h,atol=1e-9,rtol=0),"48/64 gradients:"+n);max_grad=max(max_grad,float((g-h).abs().max()))
    return dict(rows=len(texts),max_logit_error=float((zs[0]-zs[1]).abs().max()),max_gradient_error=max_grad)


def schedule(seed,arm,rows,ps):
    require(seed in SEEDS and arm in ARMS and len(rows)==192,"schedule identity")
    pp=ps.pairs_from_rows(rows);require(pp.shape==(96,2) and pp.dtype==torch.int64,"pair shape")
    require(sorted(pp.flatten().tolist())==list(range(192)),"complete pairs")
    for a,b in pp.tolist():
        require(rows[a]["target"]!=rows[b]["target"] and all(rows[a][k]==rows[b][k] for k in ("entities","values","permutation","language")),"intact pair")
    events=torch.empty((STEPS,24,4),dtype=torch.int64);allowed=LENGTHS[arm];order_seed=ORDERS[SEEDS.index(seed)]
    for epoch in range(300):
        permutation=torch.randperm(96,generator=torch.Generator().manual_seed(order_seed+304000+epoch))
        length=allowed[epoch%len(allowed)];profile=(epoch//3+epoch%3)%3
        for j in range(4):
            step=4*epoch+j;events[step,:,0]=length-2;events[step,:,1]=profile;events[step,:,2:]=pp[permutation[24*j:24*(j+1)]]
    return events


def schedule_stats(events):
    counts=[];profiles=[]
    for k in range(3):
        selected=events[events[:,:,0]==k];counts.append(torch.bincount(selected[:,2:].flatten(),minlength=192).tolist())
        profiles.append([int(((events[:,0,0]==k)&(events[:,0,1]==p)).sum()) for p in range(3)])
    return dict(per_length_row_exposures=counts,length_profile_updates=profiles,event_sha256=digest(events.tolist()),
        logical_pair_sha256=digest(events[:,:,2:].tolist()),profile_sha256=digest(events[:,:,1].tolist()))


def fit(model,data,tokens,targets,seed,arm,ps):
    require(tokens.shape==(3,3,192,SLOTS) and tokens.dtype==targets.dtype==torch.int64,"fit tokens")
    require(torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)),"target alignment")
    events=schedule(seed,arm,data["TRAIN"],ps);stats=schedule_stats(events);torch.manual_seed(FIT_RNG)
    opt=torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    model.train();losses=[]
    for step,e in enumerate(events):
        require(opt.param_groups[0]["lr"]==.005,"constant LR");opt.zero_grad(set_to_none=True)
        ids=e[:,2:].flatten();z=model(tokens[e[:,0].repeat_interleave(2),e[:,1].repeat_interleave(2),ids],torch.zeros(48,dtype=torch.int64))
        loss=F.cross_entropy(z,targets[ids]);require(bool(torch.isfinite(loss)),"finite loss");losses.append(float(loss.detach()))
        loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True);opt.step()
        if (step+1)%200==0:print(f"[C304] seed={seed} arm={arm} step={step+1}/1200 ce={losses[-1]:.6f}",flush=True)
    model.eval()
    return dict(steps=STEPS,training_rows=57600,optimizer_creations=1,fit_rng=FIT_RNG,ce_history=losses,schedule_events=events,**stats)


def evaluate(model,prompts,data,c):
    require(not any(m.training for m in model.modules()) and not any(p.requires_grad for p in model.parameters()),"frozen final model")
    raw={}
    with torch.no_grad():
        for n in EVAL_LENGTHS:
            raw[str(n)]={}
            for s in SPLITS:
                raw[str(n)][s]={}
                for p in PROFILES:
                    raw[str(n)][s][p]={}
                    for v in VIEWS:
                        chunks=[]
                        for start in range(0,len(data[s]),96):
                            x=torch.stack([prefix_tensor(r["views"][v]) for r in prompts[str(n)][s][p][start:start+96]])
                            z=model(x,torch.zeros(len(x),dtype=torch.int64));c.p267.check_logits(z,len(x));chunks.append(z.detach().clone())
                        raw[str(n)][s][p][v]=torch.cat(chunks)
    return raw


def replay_error(left,right,data,c):
    require(set(left)==set(right)==set(map(str,EVAL_LENGTHS)),"replay lengths");error=0.
    for n,s,p,v in itertools.product(map(str,EVAL_LENGTHS),SPLITS,PROFILES,VIEWS):
        a,z=left[n][s][p][v],right[n][s][p][v];c.p267.check_logits(a,len(data[s]));c.p267.check_logits(z,len(data[s]))
        error=max(error,float((a-z).abs().max()));require(error<=1e-9 and torch.equal(a.argmax(1),z.argmax(1)),"raw/argmax replay")
    return error


def score_length(data,raw,c):
    require(set(raw)==set(SPLITS) and all(set(raw[s])==set(PROFILES) for s in SPLITS),"scoring profile domain")
    adapted={s:{old:raw[s][new] for new,old in zip(PROFILES,LEGACY_PROFILES[3],strict=True)} for s in SPLITS}
    # The inherited scorer groups logical facts,queries,orders and views;identifier length is not an input.
    return c.c270.score(data,adapted,c.p267)


def check_fit(f,seed,arm,data,ps):
    require(all(type(f[k]) is int and f[k]==v for k,v in dict(steps=STEPS,training_rows=57600,optimizer_creations=1,fit_rng=FIT_RNG).items()),"fit budget")
    expected=schedule(seed,arm,data["TRAIN"],ps);require(torch.equal(f["schedule_events"],expected),"fixed schedule")
    stats=schedule_stats(expected);require(all(f[k]==v for k,v in stats.items()),"schedule reconstruction")
    target=manifest()["per_row_length_exposure"][arm]
    require(f["per_length_row_exposures"]==[[n]*192 for n in target],"exposure allocation")
    require([sum(r[p] for r in f["length_profile_updates"]) for p in range(3)]==[400]*3,"profile exposure")
    require(len(f["ce_history"])==STEPS and all(type(x) in (int,float) and math.isfinite(x) and x>=0 for x in f["ce_history"]),"loss trace")


def analyze(records,data,ps,diag,c):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"record cohort");metrics=[];parts=[];results=[]
    for r in records:
        check_fit(r["fit"],r["seed"],r["arm"],data,ps)
        require(r["parameters"]==14256 and r["slots"]==SLOTS and r["initial_sha256"]!=r["final_sha256"] and r["core_changed"] is True and r["checkpoint_roundtrip"] is True,"model integrity")
        e=r["reload_max_error"];require(type(e) in (int,float) and math.isfinite(e) and 0<=e<=1e-9,"replay bound")
        fields=("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in fields) and tuple(r[k] for k in fields)==(1308,67968,5232,108,10368,432),"record work")
        require(set(r["raw"])==set(map(str,EVAL_LENGTHS)),"all four task lengths")
        scored={str(n):score_length(data,r["raw"][str(n)],c) for n in EVAL_LENGTHS};flags={n:v["passed"] for n,v in scored.items()}
        require(all(type(v) is bool for v in flags.values()),"gate flags");direct={}
        for n in EVAL_LENGTHS:
            normalized=diag.normalize_task(scored[str(n)],"triple",r["seed"],r["arm"])
            for s in SPLITS:
                part=diag.partition([x for x in normalized if x["split"]==s]);direct[(n,s)]=part["direct_pass"]
                parts.append(dict(seed=r["seed"],arm=r["arm"],identifier_length=n,split=s,length_trained=n in LENGTHS[r["arm"]],**part))
        results.append(dict(seed=r["seed"],arm=r["arm"],length_pass=flags,quint_pass=flags["5"],all_lengths_pass=all(flags.values()),
            fitted_train_direct_pass=all(direct[n,"TRAIN"] for n in LENGTHS[r["arm"]]),trained_length_holdout_direct_pass=all(direct[n,"HOLDOUT"] for n in LENGTHS[r["arm"]])))
        metrics.append(dict(seed=r["seed"],arm=r["arm"],length_scores=scored))
    for i in range(0,15,3):
        group=records[i:i+3];require(len({r["initial_sha256"] for r in group})==1,"matched initial")
        for k in ("logical_pair_sha256","profile_sha256"):require(len({r["fit"][k] for r in group})==1,"matched logical examples/profiles")
    contrasts=[]
    for seed,n,s,control in itertools.product(SEEDS,EVAL_LENGTHS,SPLITS,ARMS[:2]):
        x,y=[next(p for p in parts if (p["seed"],p["identifier_length"],p["split"],p["arm"])==(seed,n,s,a)) for a in (control,ARMS[2])]
        contrasts.append(dict(seed=seed,identifier_length=n,split=s,control=control,candidate=ARMS[2],rows=x["rows"],control_correct=x["correct"],candidate_correct=y["correct"]))
    counts={str(n):{a:sum(r["length_pass"][str(n)] for r in results if r["arm"]==a) for a in ARMS} for n in EVAL_LENGTHS}
    return metrics,dict(seed_results=results,final_partitions=parts,contrasts=contrasts,length_pass_counts=counts,
        candidate_gate=counts["5"][ARMS[2]]==5,all_groups_matched=True,all_replays=True,**WORK)


def parent_hashes(parent):
    p302,p301,*_=parent.context()
    return (PARENT_SHA,parent.PARENT_SHA,p302.PARENT_SHA,*p301.parent_hashes(p301.context()[0]))


def load_parent(paths):
    parent,_,audit,_,_,c=context();paths=[Path(p).resolve() for p in paths];hashes=parent_hashes(parent)
    require(len(paths)==len(hashes)==30 and all(c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)),"parent hashes")
    with audit.no_neural():
        p,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION);parent.validate_result(p);s=p["validation_summary"]
        expected=dict(two_char=dict(full_train=4,core_frozen=5,residual_stop=4),triple=dict(full_train=4,core_frozen=5,residual_stop=4),quad=dict(full_train=3,core_frozen=4,residual_stop=0))
        require(p["experiment_id"]=="C303-v5b-residual-gradient-routing" and p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL"
            and s["task_pass_counts"]==expected and s["candidate_gate"] is False and s["all_groups_matched"] is True and s["all_replays"] is True,"accepted parent")
        require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(parent.OUTPUTS),"parent artifacts")
        data=c.audit.read_json(paths[0].parent/"dataset.json");c.p267.validate_data(data)
    return p,data


def precheck(paths,root):
    validate_seal();p,_=load_parent(paths);parent,p301,audit,diag,transfer,c=context();root=Path(root).resolve()
    pins=dict(p["source_blobs"]);protected=dict(p["input_sha256"]);require((len(pins),len(protected))==(664,1228),"inherited counts")
    require(all(pins.get(n)==h for n,h in PINNED.items()),"exact deciding-source pins")
    ps=p301.pair_source(p301.context()[0]);language=c.factory.language_module()
    for m in [parent,p301,audit,diag,transfer,ps,language,*parent.context(),*vars(c).values()]:
        path=getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):require(Path(path).resolve().relative_to(root).as_posix() in pins,"unprotected direct helper")
    for n,h in pins.items():require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in protected.items():require(Path(n).is_file() and c.audit.sha(n)==h,"changed input:"+n)
    directory=Path(paths[0]).resolve().parent
    for path,h in [(directory/"summary.json",PARENT_SHA)]+[(c.audit.safe_child(directory,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h,"parent input");protected[str(path.resolve())]=h
    for n in OWN:require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins));require((len(pins),len(protected))==(670,1243),"protection cardinality")
    print(f"registration_check = source_pins:670; protected_inputs:1243; manifest_sha256:{MANIFEST_SHA}",flush=True);return pins,protected


def runtime_preflight(paths,root):
    precheck(paths,root);_,p301,_,_,transfer,c=context();_,data=load_parent(paths);prompts=prompt_dataset(data);validate_prompts(prompts,data,c,transfer)
    x,y=training_tables(data);ps=p301.pair_source(p301.context()[0])
    for seed in SEEDS:
        for arm in ARMS:
            stats=schedule_stats(schedule(seed,arm,data["TRAIN"],ps))
            require(stats["per_length_row_exposures"]==[[n]*192 for n in manifest()["per_row_length_exposure"][arm]],"real exposure")
    models=make_models(SEEDS[0],c);ref=c.c278.MeanFinalDualReadout(c.factory.new_model(SEEDS[0]),SEEDS[0],c.reader,c.c269.query_span_mask)
    print("frame_compatibility =",json.dumps(compatibility_probe(ref,data),sort_keys=True),flush=True)
    with torch.no_grad():
        texts=[render(data["TRAIN"][i],5,p) for i in (0,4) for p in PROFILES];tokens=torch.stack([prefix_tensor(t) for t in texts])
        z=models[ARMS[0]](tokens,torch.zeros(len(tokens),dtype=torch.int64));c.p267.check_logits(z,len(tokens))
    print("real_2_to_5_inputs_no_truncation_and_common64_frame = PASS; scientific training not started",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True and p["gate_f_candidate"] is False and p["production_adoption"] is False,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(670,1243) and set(OWN)<=set(p["source_blobs"]) and all(p["source_blobs"].get(n)==h for n,h in PINNED.items()),"result protection")
    require(len(p["artifacts"])==7 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifact set")
    s=p["validation_summary"];rr=s["seed_results"];require([(r["seed"],r["arm"]) for r in rr]==identities(),"result cohort")
    require(all(set(r["length_pass"])==set(map(str,EVAL_LENGTHS)) and all(type(v) is bool for v in r["length_pass"].values()) for r in rr),"task flags")
    require(all(r["quint_pass"] is r["length_pass"]["5"] and r["all_lengths_pass"] is all(r["length_pass"].values()) for r in rr),"result flags")
    counts={str(n):{a:sum(r["length_pass"][str(n)] for r in rr if r["arm"]==a) for a in ARMS} for n in EVAL_LENGTHS};gate=counts["5"][ARMS[2]]==5
    require(s["length_pass_counts"]==counts and s["candidate_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"primary gate")
    require(s["all_groups_matched"] is True and s["all_replays"] is True and len(s["final_partitions"])==120 and len(s["contrasts"])==80,"result completeness")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"workload")


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(set(v)=={"schema","slots","identities","states"} and v["schema"]=="fold-c304-length-models-v1" and v["slots"]==SLOTS and v["identities"]==[list(i) for i in identities()] and len(v["states"])==15,"model bundle")
    return v["states"]


def train_one(model,data,prompts,tokens,targets,seed,arm,ps,c):
    initial=c.base.fingerprint(model);core0=c.base.fingerprint(model.backbone.core)
    with c.p267.counted(model,c.core) as (calls,cores):
        f=fit(model,data,tokens,targets,seed,arm,ps);final=c.base.fingerprint(model);model.requires_grad_(False);raw=evaluate(model,prompts,data,c)
    require(calls==[1308,67968] and cores[0]==5232,"train/evaluation counts")
    require(initial!=final and core0!=c.base.fingerprint(model.backbone.core) and c.base.fingerprint(model)==final,"weights")
    return dict(seed=seed,arm=arm,parameters=14256,slots=SLOTS,initial_sha256=initial,final_sha256=final,core_changed=True,fit=f,raw=raw,
        forward_calls=1308,row_presentations=67968,core_forward_calls=5232),{k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def replay_one(model,state,record,prompts,data,c):
    model.load_state_dict(state,strict=True);model.eval();model.requires_grad_(False);require(c.base.fingerprint(model)==record["final_sha256"],"strict final state")
    with c.p267.counted(model,c.core) as (calls,cores):raw=evaluate(model,prompts,data,c)
    error=replay_error(raw,record["raw"],data,c)
    require(calls==[108,10368] and cores[0]==432 and c.base.fingerprint(model)==record["final_sha256"],"replay counts/state")
    record.update(checkpoint_roundtrip=True,reload_max_error=error,replay_forward_calls=108,replay_row_presentations=10368,replay_core_forward_calls=432)


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite):yield from flatten(t)
        else:yield t


def regression_modules(root):
    names=context()[0].regression_modules(root);require(len(names)==len(set(names))==188,"parent modules");return names+["tests_lm.test_v05_c304_length_breadth"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==manifest()["loaded_tests"] and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED];require(len(kept)==manifest()["focused_tests"],"focused suite");return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss" and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    _,p301,_,diag,transfer,c=context();root=Path(__file__).resolve().parents[2];ps=p301.pair_source(p301.context()[0])
    guard(root,expected_head,c);torch.set_num_threads(2);torch.use_deterministic_algorithms(True);pins,protected=precheck(summaries,root)
    _,data=load_parent(summaries);prompts=prompt_dataset(data);validate_prompts(prompts,data,c,transfer);tokens,targets=training_tables(data)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);records=[];states=[]
    for seed in SEEDS:
        models=make_models(seed,c)
        for arm in ARMS:
            print(f"[C304] model={len(records)+1}/15 seed={seed} arm={arm}",flush=True)
            r,state=train_one(models[arm],data,prompts,tokens,targets,seed,arm,ps,c);records.append(r);states.append(state)
    torch.save(dict(schema="fold-c304-length-models-v1",slots=SLOTS,identities=[list(i) for i in identities()],states=states),out/OUTPUTS[3]);states=load_bundle(out/OUTPUTS[3])
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,c)
        for j,arm in enumerate(ARMS):replay_one(models[arm],states[3*i+j],records[3*i+j],prompts,data,c)
    metrics,s=analyze(records,data,ps,diag,c);torch.save(dict(schema="fold-c304-length-eval-v1",records=records),out/OUTPUTS[4])
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],data),(OUTPUTS[2],prompts),(OUTPUTS[5],metrics),(OUTPUTS[6],s)):(out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS];guard(root,expected_head,c);precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if s["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=s,gate_f_candidate=False,production_adoption=False)
    validate_result(p);(out/"summary.json").write_bytes(blob(p));receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","artifacts")}
    receipt["summary_sha256"]=c.audit.sha(out/"summary.json");print("=== C304 COMPACT RESULT RECEIPT ===",flush=True);print(json.dumps(receipt,indent=2,sort_keys=True),flush=True);return p


def verify_artifacts(outdir,summaries,expected_head):
    _,p301,audit,diag,transfer,c=context();out=Path(outdir);p=c.audit.read_json(out/"summary.json");validate_result(p);require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items():require(c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"]);require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with audit.no_neural():
        _,data=load_parent(summaries);prompts=prompt_dataset(data);validate_prompts(prompts,data,c,transfer)
        require(c.audit.read_json(out/OUTPUTS[1])==data and c.audit.read_json(out/OUTPUTS[2])==prompts,"persisted data")
        v=torch.load(out/OUTPUTS[4],map_location="cpu",weights_only=True);require(set(v)=={"schema","records"} and v["schema"]=="fold-c304-length-eval-v1","eval schema")
        metrics,s=analyze(v["records"],data,p301.pair_source(p301.context()[0]),diag,c)
        for n,x in ((OUTPUTS[0],manifest()),(OUTPUTS[5],metrics),(OUTPUTS[6],s)):require(c.audit.read_json(out/n)==x,"persisted:"+n)
    require(p["validation_summary"]==s,"summary reconstruction");return p,metrics


def main():
    p=argparse.ArgumentParser();p.add_argument("--summaries",nargs=30,type=Path,required=True);p.add_argument("--output-dir",type=Path,required=True);p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))


if __name__=="__main__":main()
