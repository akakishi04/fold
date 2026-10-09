"""C316: one fresh-seed replication of the unchanged C315 short-example mixture."""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
from types import ModuleType, SimpleNamespace
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C316-v5b-single-mix-replication"
STAGE = "V5-B-SINGLE-MIX-REPLICATION"
BASE = "0d83544dfeb835a5c74f9690008598872f3e0f2d"
PARENT_EXECUTION = "5708562420e530749a8f63b1f4baf3c7e0f28029"
PARENT_SHA = "aceda00cebf61b49e5f923bf7c426e2f4522dcac68444fc2e07b27a17b63dd66"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c315_single_character_mix.py"
PARENT_BLOB = "8bf47583b3c8dd3e4e35a8612912d170a2a8b77c"
PARENT_MANIFEST = "eb47e7656de2e83666bb780ea6bbbed34e9c56cfd00d4611ad8cca75b5e50c6d"
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
PROMPTS_SHA = "2a850d72af8c99321fd3dd4243ec2d01df6fda0bb2696329e29e3995a487fffd"
SEEDS = tuple(range(316001,316006))
ORDERS = tuple(range(316101,316106))
ARMS = ("two_to_four","one_to_four")
LENGTHS = {ARMS[0]:(2,3,4),ARMS[1]:(1,2,3,4)}
EXPOSURES = {ARMS[0]:(0,100,100,100),ARMS[1]:(75,75,75,75)}
PROFILES = ("repeat","shared_prefix","shared_suffix")
SPLITS = ("TRAIN","HOLDOUT")
STEPS, FIT_RNG = 1200, 612000
OWN = ("fold_lm/v05_benchmarks/model_c316_single_mix_replication.py",
       "tests_lm/test_v05_c316_single_mix_replication.py","tools/run_c316.ps1","tools/invoke_c316.ps1",
       "docs/experiment-ledger-addendum-c316-preregistration.md","docs/v5b-single-mix-replication-v0.1.md")
OUTPUTS = ("architecture-plan.json","dataset.json","length-datasets.json","trained-models.pt",
           "evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10,train_steps=12000,training_rows=576000,model_forward_calls=14880,
            row_presentations=852480,core_forward_calls=59520,model_state_loads=10,
            checkpoint_bundle_loads=1,new_checkpoint_writes=1,network_calls=0)
MANIFEST_SHA = "e77e05efffb480bce89fb9b16071babfff15dd533d0ac6677798478fd2103718"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c315_single_character_mix as parent
    p314,p313,p312,guarded,wide,policy,pairs,diag,c=parent.context()
    return SimpleNamespace(parent=parent,p314=p314,p313=p313,p312=p312,guarded=guarded,
                           wide=wide,policy=policy,pairs=pairs,diag=diag,c=c)


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,
        parent_manifest=PARENT_MANIFEST,seeds=list(SEEDS),orders=list(ORDERS),arms=list(ARMS),
        question="does the fixed C315 single-character allocation reproduce unseen-six reliability in one new paired cohort",
        changed="only initial seeds and paired-order seeds;no additional seed search authorized",
        parameters=14256,core_parameters=3328,slots=64,steps_per_model=STEPS,fit_rng=FIT_RNG,
        train_lengths={a:list(LENGTHS[a]) for a in ARMS},row_length_exposure={a:list(EXPOSURES[a]) for a in ARMS},
        parent_reuse="actual C315 plan_for_order/training_tables/evaluate/replay,actual C308 core_slow optimizer;no parent mutation",
        primary="ALL5 NEW one_to_four states pass every original six-character local/masked gate",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        core_lr=.0005,other_lr=.005,loss="ordinary mean CE",optimizer="AdamW;betas.9/.999;eps1e-8;decay0;globalclip1",
        data_sha256=DATA_SHA,prompts_sha256=PROMPTS_SHA,eval_lengths=list(range(1,7)),
        single_character="one canonical profile;counts/NLL diagnostic only;never triple-counted",
        limits="new initialization/order,not new tasks;exposure dilution and profile timing remain;no abstract-rule or superiority claim",
        own_tests=32,modules=201,loaded_tests=5118,focused_tests=5117,excluded_test=EXCLUDED,
        parents=42,source_pins=742,protected_inputs=1393,dtype="CPU float64",threads=2,deterministic=True,
        gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def policy_check(x):
    p=x.parent; p.validate_seal()
    require(p.MANIFEST_SHA==PARENT_MANIFEST and p.STEPS==STEPS and p.FIT_RNG==FIT_RNG
            and p.ARMS==ARMS and p.TRAIN_LENGTHS==LENGTHS and p.PROFILES==PROFILES,"unchanged parent policy")
    require(x.policy.CORE_LR==.0005 and x.policy.BASE_LR==.005,"unchanged learning rates")


def expected_parent_results():
    return [dict(seed=s,arm=a,length_pass={str(n):not(n==6 and (s==315002 or (s==315004 and a==ARMS[0]))) for n in range(2,7)},
        six_pass=not(s==315002 or (s==315004 and a==ARMS[0])),all_2_to_6_pass=not(s==315002 or (s==315004 and a==ARMS[0])))
        for s,a in itertools.product(range(315001,315006),ARMS)]


def parent_hashes(p): return (PARENT_SHA,*p.parent_hashes(p.context()[0]))


def load_parent(paths):
    x=context(); paths=[Path(p).resolve() for p in paths]; hashes=parent_hashes(x.parent)
    require(len(paths)==len(hashes)==42 and all(x.c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)),"42 parent hashes")
    with x.guarded.no_neural():
        p,_=x.parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); x.parent.validate_result(p)
        require(p["experiment_id"]=="C315-v5b-single-character-mix" and p["commit_sha"]==PARENT_EXECUTION
                and p["status"]=="FAIL" and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity")
        require(len(p["artifacts"])==7 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"parent outputs")
        s=p["validation_summary"]
        require(s["seed_results"]==expected_parent_results() and s["candidate_gate"] is False
                and s["all_pairs_matched"] is True and s["all_replays"] is True,"parent outcome contract")
        data=x.c.audit.read_json(paths[0].parent/"dataset.json"); prompts=x.c.audit.read_json(paths[0].parent/"length-datasets.json")
        require(digest(data)==DATA_SHA and digest(prompts)==PROMPTS_SHA,"canonical inputs")
        x.c.p267.validate_data(data)
        x.parent.validate_prompts(data,prompts,{str(n):prompts[str(n)] for n in (2,3,4,5)},prompts["6"],x.p313,x.wide)
    return p,data,prompts


def precheck(paths,root):
    validate_seal(); x=context(); policy_check(x); p,_,_=load_parent(paths); root=Path(root).resolve()
    pins,inputs=dict(p["source_blobs"]),dict(p["input_sha256"])
    require((len(pins),len(inputs))==(736,1379) and pins.get(PARENT_SOURCE)==PARENT_BLOB
            and all(pins.get(n)==h for n,h in x.parent.PINNED.items())
            and all(pins.get(n)==h for n,h in x.wide.PINNED.items()),"inherited protection")
    for m in [x.parent,*x.parent.context(),*x.p312.context(),*x.wide.context(),*vars(x.c).values(),x.c.factory.language_module()]:
        path=getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            require(Path(path).resolve().relative_to(root).as_posix() in pins,"unprotected helper")
    for n,h in pins.items(): require(x.c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in inputs.items(): require(Path(n).is_file() and x.c.audit.sha(n)==h,"changed input:"+n)
    directory=Path(paths[0]).resolve().parent
    for path,h in [(directory/"summary.json",PARENT_SHA)]+[(x.c.audit.safe_child(directory,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in inputs and x.c.audit.sha(path)==h,"parent input"); inputs[str(path.resolve())]=h
    for n in OWN: require(n not in pins,"OWN collision"); pins[n]=x.c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    inputs.update(x.c.audit.protect_tree_files(root,pins)); require((len(pins),len(inputs))==(742,1393),"protection counts")
    print(f"registration_check = source_pins:742; protected_inputs:1393; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,inputs


def schedule(seed,arm,data,x):
    require(seed in SEEDS and arm in ARMS,"new cohort")
    return x.parent.plan_for_order(ORDERS[SEEDS.index(seed)],arm,data["TRAIN"],x.p312,x.pairs)


def check_plans(seed,data,x):
    plans={a:schedule(seed,a,data,x) for a in ARMS}
    for arm,e in plans.items():
        st=x.parent.schedule_stats(e)
        require(st["per_length_row_exposures"]==[[n]*192 for n in EXPOSURES[arm]],"length exposures")
        require(all(sorted(e[4*i:4*i+4,:,2:].flatten().tolist())==list(range(192)) for i in range(300)),"epoch coverage")
        require(not bool(((e[:,:,0]==1)&(e[:,:,1]!=0)).any()),"single profile")
    require(torch.equal(plans[ARMS[0]][:,:,2:],plans[ARMS[1]][:,:,2:]),"paired logical order")
    old=x.p312.plan_for_order(ORDERS[SEEDS.index(seed)],"random_pairs",data["TRAIN"],x.pairs).clone(); old[:,:,0]+=2
    require(torch.equal(old,plans[ARMS[0]]),"original control schedule")
    return plans


def make_models(seed,x):
    require(seed in SEEDS,"new initial seed")
    c=x.c; ref=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    template=x.wide.LengthReadout(ref); models={a:x.policy.configure(copy.deepcopy(template),"core_slow") for a in ARMS}; used=set()
    for m in models.values():
        require(type(m) is x.wide.LengthReadout and m.backbone.config.max_tokens==64 and m.backbone.core.config.slots==64,"model/frame")
        require(sum(p.numel() for p in m.parameters())==14256 and sum(p.numel() for p in m.backbone.core.parameters())==3328,"capacity")
        require(c.base.fingerprint(m)==c.base.fingerprint(ref) and list(m.state_dict())==list(ref.state_dict()),"initial identity")
        require(all(p.requires_grad and p.dtype==torch.float64 and p.device.type=="cpu" for p in m.parameters()),"precision/learning")
        ptr={p.data_ptr() for p in m.parameters()}; require(not ptr&used,"shared storage"); used.update(ptr)
        x.policy.parameter_groups(m,"core_slow")
    return models


def optimize(model,tables,targets,events,x,label="fixture"):
    """C315 numerical loop,with an explicit immutable schedule;no parent global changes."""
    require(events.shape==(STEPS,24,4) and events.dtype==torch.int64,"optimization schedule")
    torch.manual_seed(FIT_RNG); opt=x.policy.optimizer_for(model,"core_slow")
    losses=[]; rates=[]; counts=[]; union={}; model.train()
    for step,event in enumerate(events):
        x.policy.verify_optimizer(opt,model,"core_slow"); rates.append([g["lr"] for g in opt.param_groups]); opt.zero_grad(set_to_none=True)
        n,p=map(int,event[0,:2]); ids=event[:,2:].flatten()
        z=model(tables[n,PROFILES[p]][ids],torch.zeros(48,dtype=torch.int64))
        require(z.shape==(48,256) and z.dtype==torch.float64 and bool(torch.isfinite(z).all()),"training logits")
        loss=F.cross_entropy(z,targets[ids]); require(bool(torch.isfinite(loss)),"finite loss"); losses.append(float(loss.detach()))
        loss.backward(); received={n:p.numel() for n,p in model.named_parameters() if p.grad is not None}; union.update(received); counts.append(sum(received.values()))
        torch.nn.utils.clip_grad_norm_(list(model.parameters()),1.,error_if_nonfinite=True); opt.step()
        if (step+1)%200==0: print(f"[C316] {label} step={step+1}/1200 ce={losses[-1]:.6f}",flush=True)
    model.eval()
    return dict(steps=STEPS,training_rows=57600,fit_rng=FIT_RNG,optimizer_creations=1,trainable_parameters=14256,ce_history=losses,
        optimizer_group_lrs=rates,gradient_parameter_counts=counts,gradient_union=dict(sorted(union.items())),schedule_events=events,**x.parent.schedule_stats(events))


def check_fit(f,seed,arm,data,x):
    require(all(type(f[k]) is int and f[k]==v for k,v in dict(steps=1200,training_rows=57600,fit_rng=FIT_RNG,optimizer_creations=1,trainable_parameters=14256).items()),"fit metadata")
    e=schedule(seed,arm,data,x)
    require(torch.equal(f["schedule_events"],e) and all(f[k]==v for k,v in x.parent.schedule_stats(e).items()),"fit schedule")
    require(f["optimizer_group_lrs"]==[[.005,.0005]]*STEPS and len(f["ce_history"])==STEPS
            and all(type(z) in (int,float) and math.isfinite(z) and z>=0 for z in f["ce_history"]),"fit numeric policy")
    u=f["gradient_union"]; require(u and all(type(n) is str and type(v) is int and v>0 for n,v in u.items()) and sum(u.values())<=14256,"gradient union")
    require(len(f["gradient_parameter_counts"])==STEPS and all(type(v) is int and 0<v<=sum(u.values()) for v in f["gradient_parameter_counts"]),"gradient trace")


def train_one(model,data,prompts,tables,targets,seed,arm,x):
    require(set(tables)=={(n,p) for n in range(1,5) for p in x.parent.profiles(n)}
            and all(t.shape==(192,64) and t.dtype==torch.int64 for t in tables.values())
            and targets.dtype==torch.int64 and torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]])),"TRAIN only tables/labels")
    c=x.c; initial=c.base.fingerprint(model); core_initial=c.base.fingerprint(model.backbone.core)
    with c.p267.counted(model,c.core) as (calls,cores):
        f=optimize(model,tables,targets,schedule(seed,arm,data,x),x,f"seed={seed} arm={arm}")
        final=c.base.fingerprint(model); core_final=c.base.fingerprint(model.backbone.core)
        model.requires_grad_(False); raw=x.parent.evaluate(model,prompts,data,x.wide,c)
    require(calls==[1344,71424] and cores[0]==5376 and initial!=final and core_initial!=core_final
            and c.base.fingerprint(model)==final,"train/evaluate accounting")
    return dict(seed=seed,arm=arm,initial_sha256=initial,core_initial_sha256=core_initial,final_sha256=final,core_final_sha256=core_final,fit=f,raw=raw,
                forward_calls=1344,row_presentations=71424,core_forward_calls=5376),{n:z.detach().cpu().clone() for n,z in model.state_dict().items()}


def analyze(records,data,x):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"complete new cohort")
    metrics=[]; results=[]; parts=[]; single=[]
    for r in records:
        check_fit(r["fit"],r["seed"],r["arm"],data,x); x.parent.validate_raw(r["raw"],data,x.c)
        require(r["initial_sha256"]!=r["final_sha256"] and r["core_initial_sha256"]!=r["core_final_sha256"] and r["checkpoint_roundtrip"] is True,"model state")
        error=r["reload_max_error"]; require(type(error) in (float,int) and math.isfinite(error) and 0<=error<=1e-9,"replay error")
        keys=("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in keys) and tuple(r[k] for k in keys)==(1344,71424,5376,144,13824,576),"record work")
        scored={str(n):x.wide.score_length(data,r["raw"][str(n)],x.c) for n in range(2,7)}; flags={n:z["passed"] for n,z in scored.items()}
        require(all(type(v) is bool for v in flags.values()),"score flags")
        for n in range(2,7):
            normal=x.diag.normalize_task(scored[str(n)],"triple",r["seed"],r["arm"])
            for s in SPLITS: parts.append(dict(seed=r["seed"],arm=r["arm"],identifier_length=n,split=s,length_trained=n in LENGTHS[r["arm"]],**x.diag.partition([v for v in normal if v["split"]==s])))
        for s in SPLITS:
            views=r["raw"]["1"][s]["repeat"]; y=torch.tensor([z["target"] for z in data[s]],dtype=torch.int64)
            single.append(dict(seed=r["seed"],arm=r["arm"],split=s,length_trained=r["arm"]==ARMS[1],rows=len(y),
                correct_by_view={v:int((z.argmax(1)==y).sum()) for v,z in views.items()},normal_nll=float(F.cross_entropy(views["normal"],y)),capability_gate_applicable=False))
        results.append(dict(seed=r["seed"],arm=r["arm"],length_pass=flags,six_pass=flags["6"],all_2_to_6_pass=all(flags.values())))
        metrics.append(dict(seed=r["seed"],arm=r["arm"],length_scores=scored))
    for i,seed in enumerate(SEEDS):
        check_plans(seed,data,x); a,b=records[2*i:2*i+2]
        require(all(a[k]==b[k] for k in ("initial_sha256","core_initial_sha256")) and a["fit"]["logical_pair_sha256"]==b["fit"]["logical_pair_sha256"],"paired state/order")
    counts={str(n):{a:sum(r["length_pass"][str(n)] for r in results if r["arm"]==a) for a in ARMS} for n in range(2,7)}
    paired=dict(both_pass=0,control_only=0,candidate_only=0,both_fail=0)
    for i in range(5):
        a,b=[r["six_pass"] for r in results[2*i:2*i+2]]; paired["both_pass" if a and b else "control_only" if a else "candidate_only" if b else "both_fail"]+=1
    return metrics,dict(seed_results=results,final_partitions=parts,single_character_diagnostics=single,length_pass_counts=counts,
        paired_six=paired,candidate_gate=counts["6"][ARMS[1]]==5,all_pairs_matched=True,all_replays=True,**WORK)


def runtime_preflight(paths,root):
    torch.set_num_threads(2); precheck(paths,root); x=context(); _,data,prompts=load_parent(paths)
    for seed in SEEDS: check_plans(seed,data,x)
    tables,y=x.parent.training_tables(data,prompts,x.wide); models=make_models(SEEDS[0],x)
    ids=[next(i for i,r in enumerate(data["TRAIN"]) if r["language"]==lang) for lang in ("en","ja")]
    inp=torch.cat([tables[n,"repeat"][ids] for n in (1,2)]); target=y[ids].repeat(2); signatures=[]
    for model in models.values():
        m=copy.deepcopy(model); m.train(); opt=x.policy.optimizer_for(m,"core_slow"); x.policy.verify_optimizer(opt,m,"core_slow"); opt.zero_grad(set_to_none=True)
        z=m(inp,torch.zeros(len(inp),dtype=torch.int64)); x.c.p267.check_logits(z,len(inp)); F.cross_entropy(z,target).backward()
        grads={n:None if p.grad is None else p.grad.detach().clone() for n,p in m.named_parameters()}
        torch.nn.utils.clip_grad_norm_(list(m.parameters()),1.,error_if_nonfinite=True); opt.step(); signatures.append((z.detach(),grads,x.c.base.fingerprint(m)))
    a,b=signatures; require(torch.equal(a[0],b[0]) and a[2]==b[2] and a[1].keys()==b[1].keys(),"common-input output/update")
    require(all((g is None and b[1][n] is None) or (g is not None and b[1][n] is not None and torch.equal(g,b[1][n])) for n,g in a[1].items()),"common-input gradient")
    print("real_single_mix_replication_probe = PASS; discarded copies only",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True
            and p["gate_f_candidate"] is False and p["production_adoption"] is False,"result scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(742,1393) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"result protection")
    require(len(p["artifacts"])==7 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"result artifacts")
    s=p["validation_summary"]; rr=s["seed_results"]; require([(r["seed"],r["arm"]) for r in rr]==identities(),"result cohort")
    require(all(set(r["length_pass"])==set(map(str,range(2,7))) and all(type(v) is bool for v in r["length_pass"].values())
                and r["six_pass"] is r["length_pass"]["6"] and r["all_2_to_6_pass"] is all(r["length_pass"].values()) for r in rr),"result flags")
    counts={str(n):{a:sum(r["length_pass"][str(n)] for r in rr if r["arm"]==a) for a in ARMS} for n in range(2,7)}; gate=counts["6"][ARMS[1]]==5
    require(s["length_pass_counts"]==counts and s["candidate_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"new-only primary gate")
    require(len(s["final_partitions"])==100 and len(s["single_character_diagnostics"])==20 and s["all_pairs_matched"] is True and s["all_replays"] is True,"result coverage")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"workload")


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context().parent.regression_modules(root); require(len(names)==len(set(names))==200,"parent modules")
    return names+["tests_lm.test_v05_c316_single_mix_replication"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==5118 and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED]; require(len(kept)==5117,"focused suite"); return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def load_bundle(path):
    obj=torch.load(path,map_location="cpu",weights_only=True)
    require(set(obj)=={"schema","identities","states"} and obj["schema"]=="fold-c316-single-replication-models-v1"
            and obj["identities"]==[list(v) for v in identities()] and len(obj["states"])==10,"checkpoint schema/order")
    return obj["states"]


def run(*,summaries,output_dir,expected_head):
    torch.set_num_threads(2); torch.use_deterministic_algorithms(True); x=context(); root=Path(__file__).resolve().parents[2]
    guard(root,expected_head,x.c); pins,inputs=precheck(summaries,root); _,data,prompts=load_parent(summaries)
    tables,y=x.parent.training_tables(data,prompts,x.wide); out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    records=[]; states=[]
    for seed in SEEDS:
        check_plans(seed,data,x); models=make_models(seed,x)
        for arm in ARMS:
            r,state=train_one(models[arm],data,prompts,tables,y,seed,arm,x); records.append(r); states.append(state)
    torch.save(dict(schema="fold-c316-single-replication-models-v1",identities=[list(v) for v in identities()],states=states),out/"trained-models.pt")
    loaded=load_bundle(out/"trained-models.pt")
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,x)
        for j,arm in enumerate(ARMS): x.parent.replay(models[arm],loaded[2*i+j],records[2*i+j],data,prompts,x.wide,x.c)
    metrics,s=analyze(records,data,x); torch.save(dict(schema="fold-c316-single-replication-eval-v1",records=records),out/"evaluations.pt")
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],data),(OUTPUTS[2],prompts),(OUTPUTS[5],metrics),(OUTPUTS[6],s)): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=x.c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,x.c); precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if s["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
           source_blobs=pins,input_sha256=inputs,artifacts=artifacts,validation_summary=s,gate_f_candidate=False,production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","artifacts")}; receipt["summary_sha256"]=x.c.audit.sha(out/"summary.json")
    print("=== C316 COMPACT EXPERIMENT RECEIPT ===",flush=True); print(json.dumps(receipt,sort_keys=True,indent=2),flush=True); return p


def verify_artifacts(outdir,summaries,expected_head):
    x=context(); out=Path(outdir); p=x.c.audit.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items(): require(x.c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=x.c.audit.safe_child(out,a["file"]); require(x.c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with x.guarded.no_neural():
        _,data,prompts=load_parent(summaries); archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c316-single-replication-eval-v1","evaluation schema")
        metrics,s=analyze(archive["records"],data,x)
        for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],data),(OUTPUTS[2],prompts),(OUTPUTS[5],metrics),(OUTPUTS[6],s)): require(x.c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==s,"summary reconstruction"); return p,metrics


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--summaries",nargs=42,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True); parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
