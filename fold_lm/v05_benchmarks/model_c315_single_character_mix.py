"""C315: compare training lengths2..4 with1..4 under one fixed update budget."""
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

EXPERIMENT_ID = "C315-v5b-single-character-mix"
STAGE = "V5-B-SINGLE-CHARACTER-MIX"
BASE = "c9443536d956944c3f04d9825d01742a7851bbee"
PARENT_EXECUTION = "41d132a50b246de5357a3878606a1ac7776c830d"
PARENT_SHA = "daa6403d0eb00399cecb73e83693db41dbbb42151b979080d904428da5484e51"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c314_six_boundary_profile.py"
PARENT_BLOB = "c84328a825b3edf1525faae6f140280953cca63c"
PINNED = {PARENT_SOURCE:PARENT_BLOB,
    "fold_lm/v05_benchmarks/model_c313_frozen_six_transfer.py":"bf514ad80f85140e81b834d00aceb3379f4bfd80",
    "fold_lm/v05_benchmarks/model_c312_value_balanced_batches.py":"a676b684d605424c35713ac08940e06ab16553f4",
    "fold_lm/v05_benchmarks/model_c308_core_learning_rate.py":"f4e41f0d37b1aa5cbba536e5da984ab556eea2c5",
    "fold_lm/v05_benchmarks/model_c304_length_breadth.py":"cacb5852a29171aa8079e634d929fdd54e7f4f58"}
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
OLD_SHA = "ecf2c9784213ac8fcebfd9ac03bea42317629edcea330771c92c72d71777583d"
SIX_SHA = "b6bdc8d667376cf8b0e3f98084b676abafc7992a0a63b90cb0b20add15947d72"
SEEDS = tuple(range(315001,315006))
ORDERS = tuple(range(315101,315106))
TRAIN_LENGTHS = {"two_to_four":(2,3,4),"one_to_four":(1,2,3,4)}
ARMS = tuple(TRAIN_LENGTHS)
PROFILES = ("repeat","shared_prefix","shared_suffix")
SPLITS = ("TRAIN","HOLDOUT")
VIEWS = ("normal","evidence_blind","query_blind")
STEPS, FIT_RNG = 1200, 612000
OWN = ("fold_lm/v05_benchmarks/model_c315_single_character_mix.py",
       "tests_lm/test_v05_c315_single_character_mix.py","tools/run_c315.ps1","tools/invoke_c315.ps1",
       "docs/experiment-ledger-addendum-c315-preregistration.md","docs/v5b-single-character-mix-v0.1.md")
OUTPUTS = ("architecture-plan.json","dataset.json","length-datasets.json","trained-models.pt",
           "evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10,train_steps=12000,training_rows=576000,model_forward_calls=14880,
            row_presentations=852480,core_forward_calls=59520,model_state_loads=10,
            checkpoint_bundle_loads=1,new_checkpoint_writes=1,network_calls=0)
MANIFEST_SHA = "eb47e7656de2e83666bb780ea6bbbed34e9c56cfd00d4611ad8cca75b5e50c6d"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))
def profiles(n):
    require(type(n) is int and 1<=n<=6,"length")
    return PROFILES[:1] if n==1 else PROFILES


def context():
    from fold_lm.v05_benchmarks import model_c314_six_boundary_profile as parent
    p313,guarded,wide,c = parent.context()
    p312,_,policy,_,diag,_ = p313.context()
    pairs=p312.context()[5]
    return parent,p313,p312,guarded,wide,policy,pairs,diag,c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        parent_sha256=PARENT_SHA,pinned=PINNED,seeds=list(SEEDS),orders=list(ORDERS),train_lengths={a:list(v) for a,v in TRAIN_LENGTHS.items()},
        question="at equal1200updates and trained maximum4,does adding canonical length1 improve unseen6 reliability",
        slots=64,parameters=14256,core_parameters=3328,eval_lengths=list(range(1,7)),
        primary="all5 one_to_four states pass unchanged six-character local/masked gates",
        single_character="one canonical repeat profile,192TRAIN/96HOLDOUT;never triple-count degenerate profiles",
        single_score="descriptive normal/masked counts and normal NLL only;no new capability gate",
        row_length_exposure=dict(two_to_four=[0,100,100,100],one_to_four=[75,75,75,75]),
        schedule="300epochs*4;shared randperm96(order+306000+epoch);length cycles per arm;profile=(epoch//arity+length-2)%3 except length1 profile0",
        control="exact accepted C312 random_pairs schedule at same order,with event length index translated to actual length",
        common_input="same initial full/core weights and discarded shared-input gradients/update;actual first batches intentionally differ",
        loss="ordinary mean CE",optimizer="accepted C308 core_slow",core_lr=.0005,other_lr=.005,
        fit_rng=FIT_RNG,betas=[.9,.999],eps=1e-8,weight_decay=0.,clip=1.,steps_per_model=STEPS,
        train_tables=10,eval_profile_blocks=16,eval_forwards_per_model=144,data_sha256=DATA_SHA,
        old_prompts_sha256=OLD_SHA,six_prompts_sha256=SIX_SHA,
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        limits="short-example exposure replaces some2..4 exposure;length/profile timing changes;not isolated breadth effect,capacity gain or proof of abstract rules",
        own_tests=32,modules=200,loaded_tests=5086,focused_tests=5085,excluded_test=EXCLUDED,
        parents=41,source_pins=736,protected_inputs=1379,dtype="CPU float64",threads=2,deterministic=True,
        gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def render_one(row,view="normal"):
    require(view in VIEWS and row["language"] in ("en","ja"),"single render")
    chars="abc" if row["language"]=="en" else "甲乙丙"
    values=dict(zip(row["entities"],row["values"],strict=True))
    return ";".join(chars[k]+"="+("?" if view=="evidence_blind" else str(values[k])) for k in row["permutation"])+";"+("?" if view=="query_blind" else chars[row["query"]])+"="


def prompt_dataset(data,p313):
    return {str(n):{s:{p:[dict(source_id=r["id"],target=r["target"],views={v:render_one(r,v) if n==1 else p313.render(r,n,p,v) for v in VIEWS})
                         for r in data[s]] for p in profiles(n)} for s in SPLITS} for n in range(1,7)}


def validate_prompts(data,prompts,old,six,p313,wide):
    require(digest(data)==DATA_SHA and digest(old)==OLD_SHA and digest(six)==SIX_SHA,"original data hashes")
    require(prompts==prompt_dataset(data,p313) and {n:prompts[n] for n in old}==old and prompts["6"]==six,"unchanged2..6 prompts")
    normal=[]; maximum=0
    for n in range(1,7):
        for s,p in itertools.product(SPLITS,profiles(n)):
            require(len(prompts[str(n)][s][p])==len(data[s]),"prompt rows")
            for row,item in zip(data[s],prompts[str(n)][s][p],strict=True):
                require(item["source_id"]==row["id"] and item["target"]==row["target"],"prompt identities")
                normal.append(item["views"]["normal"])
                for v,text in item["views"].items():
                    x=wide.prefix_tensor(text); raw=text.encode("utf-8"); maximum=max(maximum,len(raw))
                    require(x.shape==(64,) and x.dtype==torch.int64 and x[0]==257 and x[len(raw)+1]==258
                            and torch.equal(x[1:len(raw)+1],torch.tensor(list(raw))) and bool((x[len(raw)+2:]==256).all()),"no truncation")
                    if n==1:
                        span=wide.span_mask(x[None,:]); expected=1 if v=="query_blind" or row["language"]=="en" else 3
                        require(int(span.sum())==expected,"single query span")
    require(maximum==61 and len(normal)==len(set(normal))==4608,"deduplicated profile inventory")


def training_tables(data,prompts,wide):
    require(digest(data)==DATA_SHA,"TRAIN data")
    tables={(n,p):torch.stack([wide.prefix_tensor(r["views"]["normal"]) for r in prompts[str(n)]["TRAIN"][p]])
            for n in range(1,5) for p in profiles(n)}
    require(len(tables)==10 and all(x.shape==(192,64) for x in tables.values()),"TRAIN tables")
    return tables,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)


def plan_for_order(order,arm,rows,p312,pairs):
    require(type(order) is int and arm in ARMS,"schedule identity")
    pp,_=p312.pair_inventory(rows,pairs); lengths=TRAIN_LENGTHS[arm]; events=torch.empty((STEPS,24,4),dtype=torch.int64)
    for epoch in range(300):
        rank=torch.randperm(96,generator=torch.Generator().manual_seed(order+306000+epoch))
        n=lengths[epoch%len(lengths)]; p=0 if n==1 else (epoch//len(lengths)+n-2)%3
        for j in range(4):
            e=events[epoch*4+j]; e[:,0]=n; e[:,1]=p; e[:,2:]=pp[rank[24*j:24*(j+1)]]
    return events


def schedule(seed,arm,data,p312,pairs):
    require(seed in SEEDS,"seed")
    return plan_for_order(ORDERS[SEEDS.index(seed)],arm,data["TRAIN"],p312,pairs)


def schedule_stats(events):
    require(events.shape==(STEPS,24,4) and events.dtype==torch.int64,"events")
    return dict(event_sha256=digest(events.tolist()),logical_pair_sha256=digest(events[:,:,2:].tolist()),
        per_length_row_exposures=[torch.bincount(events[events[:,:,0]==n][:,2:].flatten(),minlength=192).tolist() for n in range(1,5)],
        length_profile_updates=[[int(((events[:,0,0]==n)&(events[:,0,1]==p)).sum()) for p in range(3)] for n in range(1,5)])


def check_plans(seed,data,p312,pairs):
    plans={a:schedule(seed,a,data,p312,pairs) for a in ARMS}
    for arm,e in plans.items():
        expected=manifest()["row_length_exposure"][arm]
        require(schedule_stats(e)["per_length_row_exposures"]==[[count]*192 for count in expected],"equal total row exposure")
        for epoch in range(300):
            chunk=e[epoch*4:epoch*4+4]
            require(sorted(chunk[:,:,2:].flatten().tolist())==list(range(192)),"complete epoch")
            require(len(set(chunk[:,:,0].flatten().tolist()))==len(set(chunk[:,:,1].flatten().tolist()))==1,"epoch renderer")
        require(not bool(((e[:,:,0]==1)&(e[:,:,1]!=0)).any()),"canonical single profile")
    require(torch.equal(plans[ARMS[0]][:,:,2:],plans[ARMS[1]][:,:,2:]),"matched logical order")
    control=p312.plan_for_order(ORDERS[SEEDS.index(seed)],"random_pairs",data["TRAIN"],pairs).clone(); control[:,:,0]+=2
    require(torch.equal(control,plans[ARMS[0]]),"unchanged control schedule")
    return plans


def make_models(seed,wide,policy,c):
    require(seed in SEEDS,"model seed")
    reference=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    template=wide.LengthReadout(reference); models={a:policy.configure(copy.deepcopy(template),"core_slow") for a in ARMS}; pointers=set()
    for m in models.values():
        require(type(m) is wide.LengthReadout and m.backbone.config.max_tokens==64 and m.backbone.core.config.slots==64,"architecture")
        require(sum(p.numel() for p in m.parameters())==14256 and sum(p.numel() for p in m.backbone.core.parameters())==3328,"capacity")
        require(c.base.fingerprint(m)==c.base.fingerprint(reference) and list(m.state_dict())==list(reference.state_dict()),"initial state")
        require(all(p.requires_grad and p.dtype==torch.float64 and p.device.type=="cpu" for p in m.parameters()),"trainable precision")
        ptr={p.data_ptr() for p in m.parameters()}; require(not ptr&pointers,"independent storage"); pointers.update(ptr)
        policy.parameter_groups(m,"core_slow")
    return models


def fit(model,data,tables,targets,seed,arm,p312,pairs,policy):
    require(set(tables)=={(n,p) for n in range(1,5) for p in profiles(n)} and all(x.shape==(192,64) and x.dtype==torch.int64 for x in tables.values()),"fit tables")
    require(targets.dtype==torch.int64 and torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]])),"target alignment")
    e=schedule(seed,arm,data,p312,pairs); torch.manual_seed(FIT_RNG); opt=policy.optimizer_for(model,"core_slow")
    losses=[]; rates=[]; counts=[]; union={}; model.train()
    for step,event in enumerate(e):
        policy.verify_optimizer(opt,model,"core_slow"); rates.append([g["lr"] for g in opt.param_groups]); opt.zero_grad(set_to_none=True)
        n,p=map(int,event[0,:2]); ids=event[:,2:].flatten()
        z=model(tables[n,PROFILES[p]][ids],torch.zeros(48,dtype=torch.int64))
        require(z.shape==(48,256) and z.dtype==torch.float64 and bool(torch.isfinite(z).all()),"logits")
        loss=F.cross_entropy(z,targets[ids]); require(bool(torch.isfinite(loss)),"finite loss"); losses.append(float(loss.detach()))
        loss.backward(); received={n:p.numel() for n,p in model.named_parameters() if p.grad is not None}; union.update(received); counts.append(sum(received.values()))
        torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True); opt.step()
        if (step+1)%200==0: print(f"[C315] seed={seed} arm={arm} step={step+1}/1200 ce={losses[-1]:.6f}",flush=True)
    model.eval()
    return dict(steps=STEPS,training_rows=57600,fit_rng=FIT_RNG,optimizer_creations=1,trainable_parameters=14256,ce_history=losses,
        optimizer_group_lrs=rates,gradient_parameter_counts=counts,gradient_union=dict(sorted(union.items())),schedule_events=e,**schedule_stats(e))


def check_fit(f,seed,arm,data,p312,pairs):
    require(all(type(f[k]) is int and f[k]==v for k,v in dict(steps=1200,training_rows=57600,fit_rng=FIT_RNG,optimizer_creations=1,trainable_parameters=14256).items()),"fit metadata")
    e=schedule(seed,arm,data,p312,pairs)
    require(torch.equal(f["schedule_events"],e) and all(f[k]==v for k,v in schedule_stats(e).items()),"saved schedule")
    require(f["optimizer_group_lrs"]==[[.005,.0005]]*STEPS and len(f["ce_history"])==STEPS
            and all(type(x) in (int,float) and math.isfinite(x) and x>=0 for x in f["ce_history"]),"optimizer/loss trace")
    u=f["gradient_union"]; require(u and all(type(k) is str and type(v) is int and v>0 for k,v in u.items()) and sum(u.values())<=14256,"gradient union")
    require(len(f["gradient_parameter_counts"])==STEPS and all(type(v) is int and 0<v<=sum(u.values()) for v in f["gradient_parameter_counts"]),"gradient trace")


def evaluate(model,prompts,data,wide,c):
    require(not any(m.training for m in model.modules()) and not any(p.requires_grad for p in model.parameters()),"frozen evaluator")
    out={}
    with torch.no_grad():
        for n in range(1,7):
            out[str(n)]={}
            for s in SPLITS:
                out[str(n)][s]={}
                for p in profiles(n):
                    out[str(n)][s][p]={}
                    for v in VIEWS:
                        chunks=[]
                        for start in range(0,len(data[s]),96):
                            x=torch.stack([wide.prefix_tensor(r["views"][v]) for r in prompts[str(n)][s][p][start:start+96]])
                            z=model(x,torch.zeros(len(x),dtype=torch.int64)); c.p267.check_logits(z,len(x)); chunks.append(z.detach().clone())
                        out[str(n)][s][p][v]=torch.cat(chunks)
    return out


def validate_raw(raw,data,c):
    require(set(raw)==set(map(str,range(1,7))),"raw lengths")
    for n in range(1,7):
        require(set(raw[str(n)])==set(SPLITS),"raw splits")
        for s in SPLITS:
            require(set(raw[str(n)][s])==set(profiles(n)),"raw profile multiplicity")
            for p in profiles(n):
                require(set(raw[str(n)][s][p])==set(VIEWS),"raw views")
                for z in raw[str(n)][s][p].values(): c.p267.check_logits(z,len(data[s])); require(not z.requires_grad,"saved detached logits")


def replay_error(left,right,data,c):
    validate_raw(left,data,c); validate_raw(right,data,c); error=0.
    for n in range(1,7):
        for s,p,v in itertools.product(SPLITS,profiles(n),VIEWS):
            x,z=left[str(n)][s][p][v],right[str(n)][s][p][v]
            error=max(error,float((x-z).abs().max())); require(error<=1e-9 and torch.equal(x.argmax(1),z.argmax(1)),"strict replay logits")
    return error


def train_one(model,data,prompts,tables,targets,seed,arm,p312,pairs,policy,wide,c):
    initial=c.base.fingerprint(model); core_initial=c.base.fingerprint(model.backbone.core)
    with c.p267.counted(model,c.core) as (calls,cores):
        f=fit(model,data,tables,targets,seed,arm,p312,pairs,policy); final=c.base.fingerprint(model); core_final=c.base.fingerprint(model.backbone.core)
        model.requires_grad_(False); raw=evaluate(model,prompts,data,wide,c)
    require(calls==[1344,71424] and cores[0]==5376 and initial!=final and core_initial!=core_final and c.base.fingerprint(model)==final,"training accounting/state")
    return dict(seed=seed,arm=arm,initial_sha256=initial,core_initial_sha256=core_initial,final_sha256=final,core_final_sha256=core_final,fit=f,raw=raw,
        forward_calls=1344,row_presentations=71424,core_forward_calls=5376),{n:z.detach().cpu().clone() for n,z in model.state_dict().items()}


def replay(model,state,record,data,prompts,wide,c):
    model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(False)
    require(c.base.fingerprint(model)==record["final_sha256"],"strict checkpoint")
    with c.p267.counted(model,c.core) as (calls,cores): raw=evaluate(model,prompts,data,wide,c)
    require(calls==[144,13824] and cores[0]==576 and c.base.fingerprint(model)==record["final_sha256"],"replay accounting/state")
    record.update(checkpoint_roundtrip=True,reload_max_error=replay_error(record["raw"],raw,data,c),replay_forward_calls=144,replay_row_presentations=13824,replay_core_forward_calls=576)


def analyze(records,data,p312,pairs,wide,diag,c):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"complete cohort")
    metrics=[]; results=[]; parts=[]; single=[]
    for r in records:
        check_fit(r["fit"],r["seed"],r["arm"],data,p312,pairs); validate_raw(r["raw"],data,c)
        require(r["initial_sha256"]!=r["final_sha256"] and r["core_initial_sha256"]!=r["core_final_sha256"] and r["checkpoint_roundtrip"] is True,"record state")
        e=r["reload_max_error"]; require(type(e) in (int,float) and math.isfinite(e) and 0<=e<=1e-9,"reload bound")
        keys=("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in keys) and tuple(r[k] for k in keys)==(1344,71424,5376,144,13824,576),"record work")
        scores={str(n):wide.score_length(data,r["raw"][str(n)],c) for n in range(2,7)}; flags={n:z["passed"] for n,z in scores.items()}
        require(all(type(v) is bool for v in flags.values()),"length gates")
        for n in range(2,7):
            normalized=diag.normalize_task(scores[str(n)],"triple",r["seed"],r["arm"])
            for s in SPLITS: parts.append(dict(seed=r["seed"],arm=r["arm"],identifier_length=n,split=s,length_trained=n in TRAIN_LENGTHS[r["arm"]],**diag.partition([p for p in normalized if p["split"]==s])))
        for s in SPLITS:
            views=r["raw"]["1"][s]["repeat"]; y=torch.tensor([z["target"] for z in data[s]],dtype=torch.int64)
            single.append(dict(seed=r["seed"],arm=r["arm"],split=s,length_trained=r["arm"]==ARMS[1],rows=len(y),
                correct_by_view={v:int((views[v].argmax(1)==y).sum()) for v in VIEWS},normal_nll=float(F.cross_entropy(views["normal"],y)),capability_gate_applicable=False))
        results.append(dict(seed=r["seed"],arm=r["arm"],length_pass=flags,six_pass=flags["6"],all_2_to_6_pass=all(flags.values())))
        metrics.append(dict(seed=r["seed"],arm=r["arm"],length_scores=scores))
    for i,seed in enumerate(SEEDS):
        check_plans(seed,data,p312,pairs); a,b=records[2*i:2*i+2]
        require(all(a[k]==b[k] for k in ("initial_sha256","core_initial_sha256")) and a["fit"]["logical_pair_sha256"]==b["fit"]["logical_pair_sha256"],"paired initial/order")
    counts={str(n):{a:sum(r["length_pass"][str(n)] for r in results if r["arm"]==a) for a in ARMS} for n in range(2,7)}
    pairs6=dict(both_pass=0,control_only=0,candidate_only=0,both_fail=0)
    for seed in SEEDS:
        a,b=[r["six_pass"] for r in results if r["seed"]==seed]; pairs6["both_pass" if a and b else "control_only" if a else "candidate_only" if b else "both_fail"]+=1
    return metrics,dict(seed_results=results,final_partitions=parts,single_character_diagnostics=single,length_pass_counts=counts,paired_six=pairs6,
        candidate_gate=counts["6"][ARMS[1]]==5,all_pairs_matched=True,all_replays=True,**WORK)


def parent_hashes(parent): return (PARENT_SHA,*parent.parent_hashes(parent.context()[0]))


def load_parent(paths):
    parent,p313,_,guarded,wide,_,_,_,c=context(); paths=[Path(p).resolve() for p in paths]; hashes=parent_hashes(parent)
    require(len(paths)==len(hashes)==41 and all(c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)),"41 parent hashes")
    with guarded.no_neural():
        p,report=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); parent.validate_result(p)
        require(p["experiment_id"]=="C314-v5b-saved-six-boundary-profile" and p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS"
                and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity")
        require(len(p["artifacts"])==3 and {a["file"] for a in p["artifacts"]}==set(parent.OUTPUTS),"parent descriptors")
        s=p["validation_summary"]; require(s["paired_rows"]==8640 and s["observations"]==17280 and s["new_error"]==89 and s["both_wrong"]==3
                and s["six_correct"]==8548 and s["capability_gate_applicable"] is False,"parent diagnostic contract")
        data=c.audit.read_json(paths[2].parent/"dataset.json"); c.p267.validate_data(data)
        old=c.audit.read_json(paths[2].parent/"length-datasets.json"); six=c.audit.read_json(paths[1].parent/"six-dataset.json")
        prompts=prompt_dataset(data,p313); validate_prompts(data,prompts,old,six,p313,wide)
    return p,data,prompts


def precheck(paths,root):
    validate_seal(); p,_,_=load_parent(paths); parent,p313,p312,_,wide,policy,_,_,c=context(); root=Path(root).resolve()
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    require((len(pins),len(protected))==(730,1369) and all(pins.get(n)==h for n,h in PINNED.items()) and all(pins.get(n)==h for n,h in wide.PINNED.items()),"inherited protection")
    for m in [parent,*parent.context(),*p313.context(),*p312.context(),*wide.context(),*vars(c).values(),c.factory.language_module()]:
        path=getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root): require(Path(path).resolve().relative_to(root).as_posix() in pins,"unprotected helper")
    for n,h in pins.items(): require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in protected.items(): require(Path(n).is_file() and c.audit.sha(n)==h,"changed input:"+n)
    folder=Path(paths[0]).resolve().parent
    for path,h in [(folder/"summary.json",PARENT_SHA)]+[(c.audit.safe_child(folder,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h,"parent input"); protected[str(path.resolve())]=h
    for n in OWN: require(n not in pins,"OWN collision"); pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins)); require((len(pins),len(protected))==(736,1379),"protection counts")
    require(policy.CORE_LR==.0005 and policy.BASE_LR==.005 and p312.FIT_RNG==FIT_RNG,"unchanged optimization")
    print(f"registration_check = source_pins:736; protected_inputs:1379; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def runtime_preflight(paths,root):
    torch.set_num_threads(2); precheck(paths,root)
    _,_,p312,_,wide,policy,pairs,_,c=context(); _,data,prompts=load_parent(paths)
    for seed in SEEDS: check_plans(seed,data,p312,pairs)
    tables,targets=training_tables(data,prompts,wide); models=make_models(SEEDS[0],wide,policy,c); signatures=[]
    ids=[next(i for i,r in enumerate(data["TRAIN"]) if r["language"]==lang) for lang in ("en","ja")]
    x=torch.cat([tables[n,"repeat"][ids] for n in (1,2)]); y=targets[ids].repeat(2)
    for model in models.values():
        m=copy.deepcopy(model); m.train(); o=policy.optimizer_for(m,"core_slow"); policy.verify_optimizer(o,m,"core_slow"); o.zero_grad(set_to_none=True)
        z=m(x,torch.zeros(len(x),dtype=torch.int64)); c.p267.check_logits(z,len(x)); F.cross_entropy(z,y).backward()
        g={n:None if p.grad is None else p.grad.detach().clone() for n,p in m.named_parameters()}
        torch.nn.utils.clip_grad_norm_(list(m.parameters()),1.,error_if_nonfinite=True); o.step(); signatures.append((z.detach(),g,c.base.fingerprint(m)))
    a,b=signatures; require(torch.equal(a[0],b[0]) and a[2]==b[2] and a[1].keys()==b[1].keys(),"common-input output/update")
    require(all((g is None and b[1][n] is None) or (g is not None and b[1][n] is not None and torch.equal(g,b[1][n])) for n,g in a[1].items()),"common-input gradients")
    print("real_single_character_span_and_equal_budget_probe = PASS; discarded copies only",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True
            and p["gate_f_candidate"] is False and p["production_adoption"] is False,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(736,1379) and set(OWN)<=set(p["source_blobs"])
            and all(p["source_blobs"].get(n)==h for n,h in PINNED.items()),"result protection")
    require(len(p["artifacts"])==7 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"]; rr=s["seed_results"]; require([(r["seed"],r["arm"]) for r in rr]==identities(),"result cohort")
    require(all(set(r["length_pass"])==set(map(str,range(2,7))) and all(type(v) is bool for v in r["length_pass"].values())
                and r["six_pass"] is r["length_pass"]["6"] and r["all_2_to_6_pass"] is all(r["length_pass"].values()) for r in rr),"result flags")
    counts={str(n):{a:sum(r["length_pass"][str(n)] for r in rr if r["arm"]==a) for a in ARMS} for n in range(2,7)}; gate=counts["6"][ARMS[1]]==5
    require(s["length_pass_counts"]==counts and s["candidate_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"primary gate")
    require(len(s["final_partitions"])==100 and len(s["single_character_diagnostics"])==20 and s["all_pairs_matched"] is True and s["all_replays"] is True,"report coverage")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"workload")


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==199,"parent modules")
    return names+["tests_lm.test_v05_c315_single_character_mix"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==5086 and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED]; require(len(kept)==5085,"focused suite"); return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c315-single-mix-models-v1"
            and v["identities"]==[list(x) for x in identities()] and len(v["states"])==10,"model archive")
    return v["states"]


def run(*,summaries,output_dir,expected_head):
    torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    _,_,p312,_,wide,policy,pairs,diag,c=context(); root=Path(__file__).resolve().parents[2]; guard(root,expected_head,c)
    pins,protected=precheck(summaries,root); _,data,prompts=load_parent(summaries); tables,targets=training_tables(data,prompts,wide)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False); records=[]; states=[]
    for seed in SEEDS:
        check_plans(seed,data,p312,pairs); models=make_models(seed,wide,policy,c)
        for arm in ARMS:
            r,state=train_one(models[arm],data,prompts,tables,targets,seed,arm,p312,pairs,policy,wide,c); records.append(r); states.append(state)
    torch.save(dict(schema="fold-c315-single-mix-models-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    loaded=load_bundle(out/"trained-models.pt")
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,wide,policy,c)
        for j,arm in enumerate(ARMS): replay(models[arm],loaded[2*i+j],records[2*i+j],data,prompts,wide,c)
    metrics,s=analyze(records,data,p312,pairs,wide,diag,c)
    torch.save(dict(schema="fold-c315-single-mix-eval-v1",records=records),out/"evaluations.pt")
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],data),(OUTPUTS[2],prompts),(OUTPUTS[5],metrics),(OUTPUTS[6],s)): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c); precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if s["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=s,gate_f_candidate=False,production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","artifacts")}; receipt["summary_sha256"]=c.audit.sha(out/"summary.json")
    print("=== C315 COMPACT EXPERIMENT RECEIPT ===",flush=True); print(json.dumps(receipt,sort_keys=True,indent=2),flush=True); return p


def verify_artifacts(outdir,summaries,expected_head):
    _,_,p312,guarded,wide,_,pairs,diag,c=context(); out=Path(outdir); p=c.audit.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items(): require(c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"]); require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with guarded.no_neural():
        _,data,prompts=load_parent(summaries); archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c315-single-mix-eval-v1","evaluation archive")
        metrics,s=analyze(archive["records"],data,p312,pairs,wide,diag,c)
        for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],data),(OUTPUTS[2],prompts),(OUTPUTS[5],metrics),(OUTPUTS[6],s)): require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==s,"summary reconstruction"); return p,metrics


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--summaries",nargs=41,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True); parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
