"""C312: redistribute unchanged TRAIN query pairs into value-balanced minibatches."""
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

EXPERIMENT_ID = "C312-v5b-value-balanced-minibatches"
STAGE = "V5-B-VALUE-BALANCED-MINIBATCHES"
BASE = "b583d14164fed3f6f03e0385e5d8c443138171f9"
PARENT_EXECUTION = "a777fc793b2affe287d055733b012ea919504446"
PARENT_SHA = "9bfdad83b33d24a986c3f76ef0e40d0ad323698b28826f80f659ff5fa6e0cdec"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c311_saved_error_context.py"
PARENT_BLOB = "d02444686ac736bc1c4f22b98b549307014e6ad4"
PINNED = {PARENT_SOURCE: PARENT_BLOB,
    "fold_lm/v05_benchmarks/model_c309_core_lr_replication.py": "8c66d64aa7ca3558d914a9b34bc9612ef444a9c2",
    "fold_lm/v05_benchmarks/model_c308_core_learning_rate.py": "f4e41f0d37b1aa5cbba536e5da984ab556eea2c5",
    "fold_lm/v05_benchmarks/model_c304_length_breadth.py": "cacb5852a29171aa8079e634d929fdd54e7f4f58"}
SEEDS = tuple(range(312001, 312006))
ORDERS = tuple(range(312101, 312106))
ARMS = ("random_pairs", "value_balanced")
LENGTHS = (2, 3, 4, 5)
TRAIN_VALUES = tuple((a, b) for a in range(4) for b in range(4) if (b-a) % 4 in (1, 3))
STEPS, FIT_RNG, SLOTS = 1200, 612000, 64
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
PROMPTS_SHA = "ecf2c9784213ac8fcebfd9ac03bea42317629edcea330771c92c72d71777583d"
OWN = ("fold_lm/v05_benchmarks/model_c312_value_balanced_batches.py",
       "tests_lm/test_v05_c312_value_balanced_batches.py", "tools/run_c312.ps1", "tools/invoke_c312.ps1",
       "docs/experiment-ledger-addendum-c312-preregistration.md", "docs/v5b-value-balanced-minibatches-v0.1.md")
OUTPUTS = ("architecture-plan.json", "dataset.json", "length-datasets.json", "trained-models.pt",
           "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10, train_steps=12000, training_rows=576000, model_forward_calls=14160,
            row_presentations=783360, core_forward_calls=56640, model_state_loads=10,
            checkpoint_bundle_loads=1, new_checkpoint_writes=1, network_calls=0)
MANIFEST_SHA = "5c543202a3c252e69f3f099b369ef9905e39662a37947c8904756b17700fab2c"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS, ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c311_saved_error_context as parent
    p310, c = parent.context()
    p309 = p310.context()[0]
    policy, _, _, _, wide, pairs, diag, transfer, same_c = p309.context()
    require(c is not None and type(c) is type(same_c), "backend context")
    return parent, p310, p309, policy, wide, pairs, diag, transfer, c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, pinned=PINNED,
        question="at fixed core_slow policy and complete epoch exposure,does balancing TRAIN value pairs in each minibatch improve unseen-five reliability",
        seeds=list(SEEDS), orders=list(ORDERS), arms=list(ARMS), train_values=[list(v) for v in TRAIN_VALUES],
        train_lengths=[2,3,4], eval_lengths=list(LENGTHS), parameters=14256, core_parameters=3328, slots=SLOTS,
        policy="accepted C308 core_slow optimizer;all parameters train;core_lr=.0005,other_lr=.005",
        schedule="same randperm96(order+306000+epoch);random consecutive24;balanced stable rank redistribution of3 per each8 TRAIN strata",
        epoch="all96 intact pairs once;4updates,epoch%3 length index,(epoch//3+epoch%3)%3 profile",
        first_loss="not required equal because first minibatches differ;common-input initial function/gradients must match",
        loss="ordinary mean CE", steps=STEPS, fit_rng=FIT_RNG, betas=[.9,.999], eps=1e-8, weight_decay=0., clip=1.,
        per_row_length_exposure=[100]*3, profile_updates=[400]*3, data_sha256=DATA_SHA, prompts_sha256=PROMPTS_SHA,
        reports="10results,80partitions,40contrasts,paired-five,1200x8 value counts per model;original masked/full scores",
        primary="all5 value_balanced states pass every original five-character local/masked criterion",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        limits="conditional core_slow comparison;batch composition/order jointly changed;not proof of imbalance causality or universal benefit",
        parents=38, source_pins=718, protected_inputs=1343, own_tests=32, modules=197, loaded_tests=4998, focused_tests=4997,
        excluded_test=EXCLUDED, dtype="CPU float64", threads=2, deterministic=True,
        gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None and digest(manifest()) == MANIFEST_SHA, "manifest seal")


def pair_inventory(rows, pairs):
    require(len(rows) == 192, "TRAIN row count")
    pp = pairs.pairs_from_rows(rows)
    require(pp.shape == (96,2) and pp.dtype == torch.int64 and sorted(pp.flatten().tolist()) == list(range(192)), "pair partition")
    strata = []
    for a,b in pp.tolist():
        ra,rb = rows[a],rows[b]
        require(all(ra[k] == rb[k] for k in ("entities","values","permutation","language"))
                and {ra["query"],rb["query"]} == set(ra["entities"]) and ra["target"] != rb["target"], "intact question pair")
        for r in (ra,rb):
            require(r["target"] == 48+r["values"][r["entities"].index(r["query"])], "target binding")
        value = tuple(ra["values"])
        require(value in TRAIN_VALUES, "HOLDOUT or invalid pair in TRAIN")
        strata.append(TRAIN_VALUES.index(value))
    require([strata.count(i) for i in range(8)] == [12]*8, "eight TRAIN strata")
    return pp, strata


def plan_for_order(order, arm, rows, pairs):
    require(type(order) is int and arm in ARMS, "plan identity")
    pp, strata = pair_inventory(rows, pairs)
    events = torch.empty((STEPS,24,4), dtype=torch.int64)
    for epoch in range(300):
        rank = torch.randperm(96, generator=torch.Generator().manual_seed(order+306000+epoch)).tolist()
        groups = [[i for i in rank if strata[i] == v] for v in range(8)]
        for j in range(4):
            if arm == ARMS[0]:
                selected = rank[24*j:24*(j+1)]
            else:
                chosen = {i for g in groups for i in g[3*j:3*(j+1)]}
                selected = [i for i in rank if i in chosen]
            require(len(selected) == len(set(selected)) == 24, "batch pairs")
            events[4*epoch+j,:,0] = epoch % 3
            events[4*epoch+j,:,1] = (epoch//3+epoch%3) % 3
            events[4*epoch+j,:,2:] = pp[selected]
    return events


def schedule(seed, arm, data, pairs):
    require(seed in SEEDS, "seed")
    return plan_for_order(ORDERS[SEEDS.index(seed)], arm, data["TRAIN"], pairs)


def batch_value_counts(events, rows):
    require(events.shape == (STEPS,24,4) and events.dtype == torch.int64, "event shape")
    counts = []
    for e in events.tolist():
        c = [0]*8
        for _,_,i,j in e:
            require(0 <= i < 192 and 0 <= j < 192 and rows[i]["values"] == rows[j]["values"], "event TRAIN pair")
            v = tuple(rows[i]["values"]); require(v in TRAIN_VALUES, "event value stratum")
            c[TRAIN_VALUES.index(v)] += 1
        counts.append(c)
    return counts


def check_plan_pair(seed, data, pairs, wide):
    plans = {a:schedule(seed,a,data,pairs) for a in ARMS}
    for arm,events in plans.items():
        stats = wide.schedule_stats(events)
        require(stats["per_length_row_exposures"] == [[100]*192 for _ in range(3)]
                and [sum(r[p] for r in stats["length_profile_updates"]) for p in range(3)] == [400]*3, "equal total exposure")
        for epoch in range(300):
            e = events[4*epoch:4*(epoch+1)]
            require(sorted(e[:,:,2:].flatten().tolist()) == list(range(192)), "complete epoch")
        if arm == ARMS[1]: require(batch_value_counts(events,data["TRAIN"]) == [[3]*8 for _ in range(STEPS)], "balanced batches")
    require(torch.equal(plans[ARMS[0]][:,:,:2],plans[ARMS[1]][:,:,:2])
            and not torch.equal(plans[ARMS[0]],plans[ARMS[1]]), "only batch assignments differ")
    return plans


def make_models(seed, policy, wide, c):
    require(seed in SEEDS, "model seed")
    reference = c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    template = wide.LengthReadout(reference)
    models = {a:policy.configure(copy.deepcopy(template),"core_slow") for a in ARMS}; used = set()
    for model in models.values():
        require(type(model) is wide.LengthReadout and model.backbone.config.max_tokens == SLOTS
                and model.backbone.core.config.slots == SLOTS, "architecture")
        require(sum(p.numel() for p in model.parameters()) == 14256
                and sum(p.numel() for p in model.backbone.core.parameters()) == 3328, "capacity")
        require(list(model.state_dict()) == list(reference.state_dict()) and c.base.fingerprint(model) == c.base.fingerprint(reference), "initial state")
        require(all(p.requires_grad and p.dtype == torch.float64 and p.device.type == "cpu" for p in model.parameters()), "training precision")
        ptrs = {p.data_ptr() for p in model.parameters()}; require(not ptrs & used, "independent storage"); used.update(ptrs)
        policy.parameter_groups(model,"core_slow")
    return models


def fit(model, data, tokens, targets, seed, arm, pairs, wide, policy):
    require(tokens.shape == (3,3,192,SLOTS) and targets.shape == (192,) and tokens.dtype == targets.dtype == torch.int64, "training tables")
    require(torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)), "target alignment")
    events = schedule(seed,arm,data,pairs); stats = wide.schedule_stats(events)
    torch.manual_seed(FIT_RNG); opt = policy.optimizer_for(model,"core_slow")
    losses,counts,rates,union = [],[],[],{}; model.train()
    active = [p for p in model.parameters() if p.requires_grad]
    for step,e in enumerate(events):
        policy.verify_optimizer(opt,model,"core_slow"); rates.append([g["lr"] for g in opt.param_groups])
        opt.zero_grad(set_to_none=True); ids=e[:,2:].flatten()
        z=model(tokens[e[:,0].repeat_interleave(2),e[:,1].repeat_interleave(2),ids],torch.zeros(48,dtype=torch.int64))
        require(z.shape == (48,256) and z.dtype == torch.float64 and bool(torch.isfinite(z).all()), "logits")
        loss=F.cross_entropy(z,targets[ids]); require(bool(torch.isfinite(loss)), "finite loss")
        losses.append(float(loss.detach())); loss.backward()
        received={n:p.numel() for n,p in model.named_parameters() if p.grad is not None}; union.update(received); counts.append(sum(received.values()))
        torch.nn.utils.clip_grad_norm_(active,1.,error_if_nonfinite=True); opt.step()
        if (step+1)%200 == 0: print(f"[C312] seed={seed} arm={arm} step={step+1}/1200 ce={losses[-1]:.6f}",flush=True)
    model.eval()
    return dict(steps=STEPS,training_rows=57600,optimizer_creations=1,fit_rng=FIT_RNG,
        trainable_parameters=sum(p.numel() for p in active),ce_history=losses,optimizer_group_lrs=rates,
        gradient_parameter_counts=counts,gradient_union=dict(sorted(union.items())),schedule_events=events,
        value_pair_counts=batch_value_counts(events,data["TRAIN"]),**stats)


def check_fit(f,seed,arm,data,pairs,wide):
    for k,v in dict(steps=STEPS,training_rows=57600,optimizer_creations=1,fit_rng=FIT_RNG,trainable_parameters=14256).items():
        require(type(f[k]) is int and f[k] == v,"fit metadata:"+k)
    e=schedule(seed,arm,data,pairs); stats=wide.schedule_stats(e)
    require(torch.equal(f["schedule_events"],e) and all(f[k] == v for k,v in stats.items()),"schedule reconstruction")
    require(f["value_pair_counts"] == batch_value_counts(e,data["TRAIN"]) and f["optimizer_group_lrs"] == [[.005,.0005]]*STEPS,"batch/LR history")
    require(len(f["ce_history"]) == STEPS and all(type(x) in (int,float) and math.isfinite(x) and x>=0 for x in f["ce_history"]),"loss trace")
    u=f["gradient_union"]; require(u and all(type(n) is str and type(v) is int and v>0 for n,v in u.items()),"gradient union")
    require(sum(u.values())<=14256 and len(f["gradient_parameter_counts"])==STEPS
        and all(type(v) is int and 0<v<=sum(u.values()) for v in f["gradient_parameter_counts"]),"gradient counts")


def train_one(model,data,prompts,tokens,targets,seed,arm,pairs,wide,c,policy):
    initial=c.base.fingerprint(model); core_initial=c.base.fingerprint(model.backbone.core)
    with c.p267.counted(model,c.core) as (calls,cores):
        fitted=fit(model,data,tokens,targets,seed,arm,pairs,wide,policy)
        final=c.base.fingerprint(model); core_final=c.base.fingerprint(model.backbone.core)
        model.requires_grad_(False); raw=wide.evaluate(model,prompts,data,c)
    require(calls==[1308,67968] and cores[0]==5232,"train/evaluation count")
    require(initial!=final and core_initial!=core_final and c.base.fingerprint(model)==final,"learned state")
    return dict(seed=seed,arm=arm,parameters=14256,slots=SLOTS,initial_sha256=initial,final_sha256=final,
        core_initial_sha256=core_initial,core_final_sha256=core_final,fit=fitted,raw=raw,
        forward_calls=1308,row_presentations=67968,core_forward_calls=5232), {n:t.detach().cpu().clone() for n,t in model.state_dict().items()}


def replay(model,state,record,data,prompts,wide,c):
    model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(False)
    require(c.base.fingerprint(model)==record["final_sha256"],"strict state replay")
    with c.p267.counted(model,c.core) as (calls,cores): raw=wide.evaluate(model,prompts,data,c)
    require(calls==[108,10368] and cores[0]==432 and c.base.fingerprint(model)==record["final_sha256"],"replay counts/state")
    record.update(checkpoint_roundtrip=True,reload_max_error=wide.replay_error(record["raw"],raw,data,c),
        replay_forward_calls=108,replay_row_presentations=10368,replay_core_forward_calls=432)


def analyze(records,data,pairs,wide,diag,c):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"complete cohort")
    metrics,parts,results=[],[],[]
    for r in records:
        check_fit(r["fit"],r["seed"],r["arm"],data,pairs,wide)
        require(r["parameters"]==14256 and r["slots"]==64 and r["initial_sha256"]!=r["final_sha256"]
            and r["core_initial_sha256"]!=r["core_final_sha256"] and r["checkpoint_roundtrip"] is True,"record state")
        e=r["reload_max_error"]; require(type(e) in (int,float) and math.isfinite(e) and 0<=e<=1e-9,"replay tolerance")
        keys=("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in keys) and tuple(r[k] for k in keys)==(1308,67968,5232,108,10368,432),"record work")
        require(set(r["raw"])==set(map(str,LENGTHS)),"raw lengths")
        scored={str(n):wide.score_length(data,r["raw"][str(n)],c) for n in LENGTHS}; flags={n:v["passed"] for n,v in scored.items()}; direct={}
        require(all(type(v) is bool for v in flags.values()),"task flags")
        for n in LENGTHS:
            norm=diag.normalize_task(scored[str(n)],"triple",r["seed"],r["arm"])
            for split in ("TRAIN","HOLDOUT"):
                part=diag.partition([p for p in norm if p["split"]==split]); direct[n,split]=part["direct_pass"]
                parts.append(dict(seed=r["seed"],arm=r["arm"],identifier_length=n,split=split,length_trained=n<5,**part))
        results.append(dict(seed=r["seed"],arm=r["arm"],length_pass=flags,quint_pass=flags["5"],all_lengths_pass=all(flags.values()),
            fitted_train_direct_pass=all(direct[n,"TRAIN"] for n in (2,3,4)),trained_length_holdout_direct_pass=all(direct[n,"HOLDOUT"] for n in (2,3,4))))
        metrics.append(dict(seed=r["seed"],arm=r["arm"],length_scores=scored))
    for i,seed in enumerate(SEEDS):
        group=records[2*i:2*i+2]; check_plan_pair(seed,data,pairs,wide)
        require(all(len({r[k] for r in group})==1 for k in ("initial_sha256","core_initial_sha256")),"matched initial weights")
        require(group[0]["fit"]["profile_sha256"]==group[1]["fit"]["profile_sha256"],"matched render schedule")
    counts={str(n):{a:sum(r["length_pass"][str(n)] for r in results if r["arm"]==a) for a in ARMS} for n in LENGTHS}
    paired=dict(both_pass=0,control_only=0,candidate_only=0,both_fail=0); contrasts=[]
    for seed in SEEDS:
        a,b=[r["quint_pass"] for r in results if r["seed"]==seed]
        paired["both_pass" if a and b else "control_only" if a else "candidate_only" if b else "both_fail"]+=1
        for n,split in itertools.product(LENGTHS,("TRAIN","HOLDOUT")):
            x,y=[p for p in parts if (p["seed"],p["identifier_length"],p["split"])==(seed,n,split)]
            contrasts.append(dict(seed=seed,identifier_length=n,split=split,rows=x["rows"],random_correct=x["correct"],balanced_correct=y["correct"]))
    return metrics,dict(seed_results=results,final_partitions=parts,contrasts=contrasts,length_pass_counts=counts,paired_five=paired,
        candidate_gate=counts["5"][ARMS[1]]==5,all_pairs_matched=True,all_replays=True,**WORK)


def parent_hashes(parent):
    return (PARENT_SHA,*parent.parent_hashes(parent.context()[0]))


def load_parent(paths):
    parent,p310,_,_,wide,_,_,transfer,c=context(); paths=[Path(p).resolve() for p in paths]; hashes=parent_hashes(parent)
    require(len(paths)==len(hashes)==38 and all(c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)),"38 parent hashes")
    with p310.no_neural():
        p,report=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); parent.validate_result(p)
        require(p["experiment_id"]=="C311-v5b-saved-error-context" and p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS"
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity")
        require(len(p["artifacts"])==3 and {a["file"] for a in p["artifacts"]}==set(parent.OUTPUTS)
            and p["validation_summary"]["observations"]==51840 and p["validation_summary"]["capability_gate_applicable"] is False,"parent contract")
        data=c.audit.read_json(paths[2].parent/"dataset.json"); prompts=c.audit.read_json(paths[2].parent/"length-datasets.json")
        c.p267.validate_data(data)
        require(digest(data)==DATA_SHA and digest(prompts)==PROMPTS_SHA and prompts==wide.prompt_dataset(data),"original data/prompts")
        wide.validate_prompts(prompts,data,c,transfer)
    return p,data,prompts


def precheck(paths,root):
    validate_seal(); p,_,_=load_parent(paths); parent,p310,p309,policy,wide,pairs,diag,transfer,c=context(); root=Path(root).resolve()
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    require((len(pins),len(protected))==(712,1333) and all(pins.get(n)==h for n,h in PINNED.items())
        and all(pins.get(n)==h for n,h in wide.PINNED.items()),"inherited pins")
    for m in [parent,p310,p309,policy,wide,pairs,diag,transfer,*p309.context(),*wide.context(),*vars(c).values(),c.factory.language_module()]:
        path=getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root): require(Path(path).resolve().relative_to(root).as_posix() in pins,"unprotected helper")
    for n,h in pins.items(): require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in protected.items(): require(Path(n).is_file() and c.audit.sha(n)==h,"changed input:"+n)
    folder=Path(paths[0]).resolve().parent
    for path,h in [(folder/"summary.json",PARENT_SHA)]+[(c.audit.safe_child(folder,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h,"parent input"); protected[str(path.resolve())]=h
    for n in OWN: require(n not in pins,"OWN collision"); pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins)); require((len(pins),len(protected))==(718,1343),"protection counts")
    require(policy.CORE_LR==.0005 and policy.BASE_LR==.005 and p309.FIT_RNG==FIT_RNG,"fixed core_slow policy")
    print(f"registration_check = source_pins:718; protected_inputs:1343; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def runtime_preflight(paths,root):
    torch.set_num_threads(2); precheck(paths,root)
    _,_,p309,policy,wide,pairs,_,_,c=context(); _,data,_=load_parent(paths)
    for seed in SEEDS: check_plan_pair(seed,data,pairs,wide)
    for seed,order in zip(p309.SEEDS,p309.ORDERS,strict=True):
        require(torch.equal(plan_for_order(order,ARMS[0],data["TRAIN"],pairs),p309.schedule(seed,data["TRAIN"],pairs)),"original schedule compatibility")
    tokens,targets=wide.training_tables(data); models=make_models(SEEDS[0],policy,wide,c); e=schedule(SEEDS[0],ARMS[0],data,pairs)[0]; ids=e[:,2:].flatten()
    signatures=[]
    for model in models.values():
        m=copy.deepcopy(model); opt=policy.optimizer_for(m,"core_slow"); policy.verify_optimizer(opt,m,"core_slow")
        m.train(); opt.zero_grad(set_to_none=True)
        z=m(tokens[e[:,0].repeat_interleave(2),e[:,1].repeat_interleave(2),ids],torch.zeros(48,dtype=torch.int64)); F.cross_entropy(z,targets[ids]).backward()
        grad={n:None if p.grad is None else p.grad.detach().clone() for n,p in m.named_parameters()}
        torch.nn.utils.clip_grad_norm_(list(m.parameters()),1.,error_if_nonfinite=True); opt.step()
        signatures.append((z.detach(),grad,c.base.fingerprint(m)))
    x,y=signatures; require(torch.equal(x[0],y[0]) and x[2]==y[2] and x[1].keys()==y[1].keys(),"common-input identity")
    require(all((g is None and y[1][n] is None) or (g is not None and y[1][n] is not None and torch.equal(g,y[1][n])) for n,g in x[1].items()),"common-input gradients")
    print("real_value_balance_epoch_budget_and_common_input_probe = PASS; discarded copies only",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True
        and p["gate_f_candidate"] is False and p["production_adoption"] is False,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(718,1343) and set(OWN)<=set(p["source_blobs"])
        and all(p["source_blobs"].get(n)==h for n,h in PINNED.items()),"result pins")
    require(len(p["artifacts"])==7 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"result artifacts")
    s=p["validation_summary"]; rr=s["seed_results"]; require([(r["seed"],r["arm"]) for r in rr]==identities(),"result cohort")
    for r in rr:
        require(set(r["length_pass"])==set(map(str,LENGTHS)) and all(type(v) is bool for v in r["length_pass"].values())
            and r["quint_pass"] is r["length_pass"]["5"] and r["all_lengths_pass"] is all(r["length_pass"].values()),"result flags")
    counts={str(n):{a:sum(r["length_pass"][str(n)] for r in rr if r["arm"]==a) for a in ARMS} for n in LENGTHS}; gate=counts["5"][ARMS[1]]==5
    require(s["length_pass_counts"]==counts and s["candidate_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"primary gate")
    require(s["all_pairs_matched"] is True and s["all_replays"] is True and len(s["final_partitions"])==80 and len(s["contrasts"])==40,"result coverage")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"result work")


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==196,"parent modules")
    return names+["tests_lm.test_v05_c312_value_balanced_batches"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==4998 and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED]; require(len(kept)==4997,"focused suite"); return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
        and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c312-value-batches-models-v1"
        and v["identities"]==[list(x) for x in identities()] and len(v["states"])==10,"model archive")
    return v["states"]


def run(*,summaries,output_dir,expected_head):
    torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    _,_,_,policy,wide,pairs,diag,_,c=context(); root=Path(__file__).resolve().parents[2]; guard(root,expected_head,c)
    pins,protected=precheck(summaries,root); _,data,prompts=load_parent(summaries); tokens,targets=wide.training_tables(data)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False); records=[]; states=[]
    for seed in SEEDS:
        check_plan_pair(seed,data,pairs,wide); models=make_models(seed,policy,wide,c)
        for arm in ARMS:
            print(f"[C312] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            r,state=train_one(models[arm],data,prompts,tokens,targets,seed,arm,pairs,wide,c,policy); records.append(r); states.append(state)
    torch.save(dict(schema="fold-c312-value-batches-models-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    loaded=load_bundle(out/"trained-models.pt")
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,policy,wide,c)
        for j,arm in enumerate(ARMS): replay(models[arm],loaded[2*i+j],records[2*i+j],data,prompts,wide,c)
    metrics,s=analyze(records,data,pairs,wide,diag,c)
    torch.save(dict(schema="fold-c312-value-batches-eval-v1",records=records),out/"evaluations.pt")
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],data),(OUTPUTS[2],prompts),(OUTPUTS[5],metrics),(OUTPUTS[6],s)): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c); precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if s["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=s,gate_f_candidate=False,production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","artifacts")}; receipt["summary_sha256"]=c.audit.sha(out/"summary.json")
    print("=== C312 COMPACT EXPERIMENT RECEIPT ===",flush=True); print(json.dumps(receipt,sort_keys=True,indent=2),flush=True); return p


def verify_artifacts(outdir,summaries,expected_head):
    _,p310,_,_,wide,pairs,diag,_,c=context(); out=Path(outdir); p=c.audit.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items(): require(c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"]); require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with p310.no_neural():
        _,data,prompts=load_parent(summaries); archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c312-value-batches-eval-v1","evaluation archive")
        metrics,s=analyze(archive["records"],data,pairs,wide,diag,c)
        for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],data),(OUTPUTS[2],prompts),(OUTPUTS[5],metrics),(OUTPUTS[6],s)):
            require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==s,"summary reconstruction"); return p,metrics


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--summaries",nargs=38,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True); parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
