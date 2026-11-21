"""C289: fixed-budget pair-loss withdrawal with concurrent CE and always-on anchors."""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import math
import re
import unittest
from pathlib import Path
from unittest.mock import patch
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C289-v5b-early-pair-withdrawal"
STAGE = "V5-B-EARLY-PAIR-WITHDRAWAL"
BASE = "4acd3873a4f524ceb3080aab10653cd13caaa1c4"
PARENT_EXECUTION = "f43618b6bb6fcc1ad4a4a4b928992adce29f4e41"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c288_query_pair_assignment_loss.py"
PARENT_BLOB = "f7f9c73565828e23533efd188f25009e5e4b3d50"
SUMMARY_SHAS = (
    "2a15fbf6c5e697d5e226bdae5a5b2f243f43625b29255839100d2f05ce24fbc0",
    "69fb8b4f8eb4affe1ff340a7b3faf2b301389cc648afed7becf486dab6fce54d",
    "14bfe8920b80c86cc8e297864402c38c53a26c87085b8963cae363cb6fd98a9a",
    "702092926265bb893babce1e5b93dd234791527344193ea876d33210e8bfdba1",
    "83df761b835fa529d72ba1cee5fe618ddaff6936d9db56defc02957b90788c83",
    "609718db24ca6e3eda4f8916f04f56b24bff3621ddca4ebe136209617fad4949",
    "075cb7399f62d048310bdfb1c31c93ac39ab8b3dc400578d60e062ebfdacf3d1",
    "f56aca6895d5acd69b3c7e557c04fdb95b2b5e13a8b0bfe56f7c6ea4d5878ea7",
    "00410f3d879cb9571186e2ebf08a1ca9df0b31b64a639adae53f503c068bc7db",
    "a0019e06e4f4b330675daa2235cb4d0cf1952930336d2f0038f17d6ebd11b5bb",
    "557069bec9d0d6ef73c7a9d1f5196f7be70edb9ab2c37a9a0d315033678b770b",
    "ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13",
    "6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f",
    "1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb",
    "0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0",
)
PARENT_ARTIFACTS = {
    "architecture-plan.json": ("44b114f22e06b214f3567baea16cc8771da55566e128c3c2d35b47023ba313d5",3851),
    "dataset.json": ("1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",36024),
    "triple-dataset.json": ("432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",158236),
    "quad-dataset.json": ("86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b",172066),
    "trained-models.pt": ("15565c23d0fda2762e5ae954b439c36c0c0681df953fe21731cf38268f82fad8",1238007),
    "evaluations.pt": ("2a5d1da162a46a1351dfc6232ce4172120c815321f810c774a816d9f54c235a2",159706383),
    "measurements.json": ("94e1bad69c3dcdabee2604ead83b997abfefd11ecac19550225e5ebc07efe7fb",788605),
    "validation-summary.json": ("460bd624531d3982a5c62170647380f8ee1fbe5b98574720280f9cd3ff5e1958",59413),
}
SEEDS = tuple(range(289001,289006))
ARMS = ("ce_only","pair_always","pair_early")
TASKS = ("two_char","triple","quad")
PAIR_WEIGHT, PAIR_MARGIN, SWITCH, TOL = .25, 1., 400, 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c289_early_pair_withdrawal.py",
       "tests_lm/test_v05_c289_early_pair_withdrawal.py","tools/run_c289.ps1","tools/invoke_c289.ps1",
       "docs/experiment-ledger-addendum-c289-preregistration.md","docs/v5b-early-pair-withdrawal-v0.1.md")
OUTPUTS = ("architecture-plan.json","dataset.json","triple-dataset.json","quad-dataset.json",
           "trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=15,train_steps=12000,training_rows=576000,model_forward_calls=14430,
            row_presentations=809280,core_forward_calls=57720,checkpoint_bundle_loads=1,
            model_state_loads=15,new_checkpoint_writes=1,network_calls=0)
COUNT_FIELDS = (("seed_pass_counts","passed"),("two_char_pass_counts","two_char_pass"),
                ("triple_pass_counts","triple_pass"),("quad_pass_counts","quad_pass"),
                ("all_tasks_pass_counts","all_tasks_pass"),("fitted_train_pass_counts","fitted_train_direct_pass"),
                ("seen_holdout_pass_counts","seen_holdout_direct_pass"))
MANIFEST_SHA = "48b33a7ed29cf9ded858753d5f64210006f559ef428c167e912621a71896ae21"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c288_query_pair_assignment_loss as parent
    diagnostic,evaluation,transfer,training,c = parent.context()
    return parent,diagnostic,evaluation,transfer,training,c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,
                summary_sha256=list(SUMMARY_SHAS),parent_artifacts={k:list(v) for k,v in PARENT_ARTIFACTS.items()},
                seeds=list(SEEDS),arms=list(ARMS),parameters=14256,max_tokens=48,
                architecture="actual C278 MeanFinalDualReadout;three independent identical initial states",
                question="does first-half-only pair loss retain fitting benefits without always-on transfer regressions",
                changed="auxiliary weight after update400 only between pair_always and pair_early;CE-only concurrent anchor",
                objective="CE+weight*mean softplus(1-correct_assignment+swapped_assignment)",
                weights={"ce_only":[0.,0.],"pair_always":[.25,.25],"pair_early":[.25,0.]},
                switch_after_update=SWITCH,pair_weight=PAIR_WEIGHT,pair_margin=PAIR_MARGIN,
                common_prefix="pair_always/pair_early first400 CE,pair,total losses and step400 fingerprint exactly equal",
                optimizer_continuity="one AdamW per model for800 updates;no reset at401;no intermediate checkpoint",
                schedule="200 epochs x4;randperm96(seed+289000+epoch);24 intact pairs/batch;profile=epoch%3;length=epoch%2",
                per_length_row_exposures=[100,100],length_profile_updates=[[136,132,132],[132,136,132]],
                fit_rng="seed+290000 reset per arm",steps_per_model=800,optimizer="AdamW",lr=.005,
                betas=[.9,.999],eps=1e-8,weight_decay=0.,clip=1.,
                data_sha256=PARENT_ARTIFACTS["dataset.json"][0],triple_sha256=PARENT_ARTIFACTS["triple-dataset.json"][0],
                quad_sha256=PARENT_ARTIFACTS["quad-dataset.json"][0],
                primary="all five pair_early states pass every untrained four-character fixed criterion",
                contrasts="candidate pair_early minus each of CE-only and always-on;360 paired totals;90 final partitions",
                limitation="withdrawal also reduces integrated auxiliary gradient exposure;no proven late-pressure cause",
                gate=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
                source_pins=580,protected_inputs=1041,dependency_union=65,own_tests=48,
                modules=174,loaded_tests=4206,focused_tests=4205,excluded_test=EXCLUDED,
                dtype="CPU float64",threads=2,deterministic=True,replay_tolerance=TOL,
                gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None,"manifest not sealed")
    require(digest(manifest())==MANIFEST_SHA,"manifest digest mismatch")


def weight_schedule(arm):
    require(arm in ARMS,"weight arm")
    return [PAIR_WEIGHT if arm=="pair_always" or (arm=="pair_early" and s<=SWITCH) else 0. for s in range(1,801)]


def objective(logits,targets,weight):
    require(type(weight) is float and weight in (0.,PAIR_WEIGHT),"objective weight")
    require(logits.ndim==2 and logits.shape[1]==256 and len(logits)>0 and len(logits)%2==0,"objective shape")
    require(logits.dtype==torch.float64 and targets.dtype==torch.int64 and targets.shape==(len(logits),)
            and logits.device==targets.device,"objective dtype/targets")
    require(bool(torch.isfinite(logits).all()) and bool(((targets>=0)&(targets<256)).all()),"objective finite/range")
    y=targets.reshape(-1,2);z=logits.reshape(-1,2,256)
    require(bool((y[:,0]!=y[:,1]).all()),"distinct pair targets")
    i=torch.arange(len(y),device=logits.device)
    correct=z[i,0,y[:,0]]+z[i,1,y[:,1]];swapped=z[i,0,y[:,1]]+z[i,1,y[:,0]]
    gap=correct-swapped
    pair=F.softplus(PAIR_MARGIN-gap).mean();ce=F.cross_entropy(logits,targets)
    total=ce if weight==0. else ce+weight*pair
    require(bool(torch.isfinite(total)) and bool(torch.isfinite(pair)),"objective nonfinite")
    return total,ce,pair


def schedule(seed,rows):
    require(seed in SEEDS and len(rows)==192,"schedule identity")
    groups={}
    for i,r in enumerate(rows):
        k=(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups.setdefault(k,[]).append(i)
    pairs=[]
    for k in sorted(groups):
        ids=sorted(groups[k],key=lambda i:rows[i]["query"])
        require(len(ids)==2 and [rows[i]["query"] for i in ids]==list(k[1]),"complete query pair")
        require(rows[ids[0]]["target"]!=rows[ids[1]]["target"],"pair target collision");pairs.append(ids)
    require(len(pairs)==96 and sorted(sum(pairs,[]))==list(range(192)),"pair partition")
    pairs=torch.tensor(pairs,dtype=torch.int64);batches=[];profiles=[];lengths=[]
    for epoch in range(200):
        order=torch.randperm(96,generator=torch.Generator().manual_seed(seed+289000+epoch))
        for block in range(4):
            batches.append(pairs[order[block*24:(block+1)*24]].flatten());profiles.append(epoch%3);lengths.append(epoch%2)
    x,p,l=torch.stack(batches),torch.tensor(profiles),torch.tensor(lengths)
    exposure=[torch.bincount(x[l==j].flatten(),minlength=192).tolist() for j in range(2)]
    lp=[[sum(a==j and b==k for a,b in zip(lengths,profiles,strict=True)) for k in range(3)] for j in range(2)]
    require(exposure==[[100]*192,[100]*192] and lp==manifest()["length_profile_updates"],"exposure")
    return x,p,l,dict(logical_batch_sha256=digest(x.tolist()),rendering_sha256=digest([profiles,lengths]),
                      per_length_row_exposures=exposure,length_profile_updates=lp)


def make_models(seed,c):
    require(seed in SEEDS,"model seed")
    first=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    models={ARMS[0]:first,ARMS[1]:copy.deepcopy(first),ARMS[2]:copy.deepcopy(first)}
    for m in models.values():
        require(type(m) is c.c278.MeanFinalDualReadout and sum(p.numel() for p in m.parameters())==14256,"capacity/architecture")
        require(all(p.dtype==torch.float64 for p in m.parameters()),"precision")
        require(list(m.state_dict())==list(first.state_dict()) and c.base.fingerprint(m)==c.base.fingerprint(first),"matched initial")
    for a,b in itertools.combinations(models.values(),2):
        require(all(x.data_ptr()!=y.data_ptr() for x,y in zip(a.parameters(),b.parameters(),strict=True)),"independent storage")
    return models


def fit(model,data,tokens,targets,seed,arm,c):
    require(arm in ARMS and tokens.shape==(2,3,192,48) and targets.shape==(192,)
            and tokens.dtype==targets.dtype==torch.int64,"fit tables")
    ids,profiles,lengths,plan=schedule(seed,data["TRAIN"])
    require(torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)),"target alignment")
    torch.manual_seed(seed+290000);weights=weight_schedule(arm)
    opt=torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    model.train();traces={k:[] for k in ("ce_history","pair_history","total_history","applied_lr","applied_weight")};midpoint=None
    for step in range(800):
        require(len(opt.param_groups)==1 and opt.param_groups[0]["lr"]==.005,"constant LR")
        opt.zero_grad(set_to_none=True);batch=ids[step]
        logits=model(tokens[lengths[step],profiles[step],batch],torch.zeros(48,dtype=torch.int64))
        total,ce,pair=objective(logits,targets[batch],weights[step])
        for k,v in (("ce_history",ce.detach()),("pair_history",pair.detach()),("total_history",total.detach()),
                    ("applied_lr",opt.param_groups[0]["lr"]),("applied_weight",weights[step])):traces[k].append(float(v))
        total.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True);opt.step()
        if step+1==SWITCH:midpoint=c.base.fingerprint(model)
        if (step+1)%200==0:print(f"[C289] seed={seed} arm={arm} step={step+1}/800 weight={weights[step]} ce={float(ce.detach()):.6f} pair={float(pair.detach()):.6f}",flush=True)
    model.eval()
    return dict(steps=800,training_rows=38400,optimizer_creations=1,step400_sha256=midpoint,
                last_ce=traces["ce_history"][-1],**traces,**plan)


def train_one(model,data,triple,quad,tokens,targets,seed,arm,evaluation,transfer,c):
    initial=c.base.fingerprint(model);back=c.base.fingerprint(model.backbone);head=c.base.fingerprint(model.read)
    with c.p267.counted(model,c.core) as (calls,cores):
        fitted=fit(model,data,tokens,targets,seed,arm,c)
        final=c.base.fingerprint(model);model.requires_grad_(False)
        raw=evaluation.evaluate(model,data,triple,quad,transfer,c)
    require(calls==[881,46176] and cores[0]==3524,"train/evaluation workload")
    require(initial!=final and back!=c.base.fingerprint(model.backbone) and head!=c.base.fingerprint(model.read)
            and final==c.base.fingerprint(model),"weight integrity")
    return dict(seed=seed,arm=arm,parameters=14256,initial_sha256=initial,final_sha256=final,weights_changed=True,
                fit=fitted,raw=raw,forward_calls=881,row_presentations=46176,core_forward_calls=3524),{k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def check_fit(f,seed,arm,data):
    require(type(f["steps"]) is int and f["steps"]==800 and type(f["training_rows"]) is int and f["training_rows"]==38400,"fit budget")
    plan=schedule(seed,data["TRAIN"])[3]
    require(all(f[k]==v for k,v in plan.items()) and f["applied_lr"]==[.005]*800
            and f["applied_weight"]==weight_schedule(arm),"fit schedule/LR/weight")
    require(type(f["optimizer_creations"]) is int and f["optimizer_creations"]==1,"optimizer continuity")
    require(re.fullmatch(r"[0-9a-f]{64}",f["step400_sha256"]) is not None,"midpoint fingerprint")
    for key in ("ce_history","pair_history","total_history"):
        require(len(f[key])==800 and all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in f[key]),"loss trace")
    require(all(math.isclose(t,ce+w*q,rel_tol=1e-12,abs_tol=1e-12)
                for t,ce,q,w in zip(f["total_history"],f["ce_history"],f["pair_history"],f["applied_weight"],strict=True)),"objective reconstruction")
    require(f["last_ce"]==f["ce_history"][-1],"last loss")


def check_matched_group(records):
    require(len(records)==3 and [r["arm"] for r in records]==list(ARMS) and len({r["seed"] for r in records})==1,"matched group identities")
    for b in records[1:]:
        a=records[0]
        require(a["initial_sha256"]==b["initial_sha256"] and all(a["fit"][k]==b["fit"][k]
                for k in ("logical_batch_sha256","rendering_sha256","applied_lr")),"matched initial/data/LR")
    a,b=records[1:]
    require(a["fit"]["step400_sha256"]==b["fit"]["step400_sha256"] and all(a["fit"][k][:SWITCH]==b["fit"][k][:SWITCH]
            for k in ("ce_history","pair_history","total_history")),"common auxiliary first400 prefix")


def analyze(records,data,diagnostic,transfer,c):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"record identities")
    metrics=[];results=[];partitions=[];contrasts=[]
    for r in records:
        require(r["parameters"]==14256 and r["weights_changed"] is True and r["checkpoint_roundtrip"] is True,"record integrity")
        error=r["reload_max_error"]
        require(type(error) in (int,float) and math.isfinite(error) and 0<=error<=TOL,"replay bound")
        keys=("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in keys) and tuple(r[k] for k in keys)==(881,46176,3524,81,7776,324),"record workload")
        check_fit(r["fit"],r["seed"],r["arm"],data);require(set(r["raw"])==set(TASKS),"raw tasks")
        scored=dict(two_char=c.p267.score(data,r["raw"]["two_char"]),triple=c.c270.score(data,r["raw"]["triple"],c.p267),
                    quad=transfer.score_quad(data,r["raw"]["quad"],c))
        flags={t+"_pass":scored[t]["passed"] for t in TASKS};direct={}
        for task in TASKS:
            normalized=diagnostic.normalize_task(scored[task],task,r["seed"],r["arm"])
            for split in ("TRAIN","HOLDOUT"):
                part=diagnostic.partition([x for x in normalized if x["split"]==split]);direct[(task,split)]=part["direct_pass"]
                partitions.append(dict(seed=r["seed"],arm=r["arm"],task=task,split=split,**part))
        results.append(dict(seed=r["seed"],arm=r["arm"],passed=flags["quad_pass"],all_tasks_pass=all(flags.values()),
                            fitted_train_direct_pass=all(direct[(t,"TRAIN")] for t in TASKS[:2]),
                            seen_holdout_direct_pass=all(direct[(t,"HOLDOUT")] for t in TASKS[:2]),**flags))
        metrics.append(dict(seed=r["seed"],arm=r["arm"],**scored))
    for i in range(0,15,3):
        check_matched_group(records[i:i+3])
        for j in (0,1):
            for task in TASKS:
                for x,y in zip(metrics[i+j][task]["totals"],metrics[i+2][task]["totals"],strict=True):
                    keys=("split","profile","language","rows","pairs")
                    require(all(x[k]==y[k] for k in keys),"contrast identity")
                    contrasts.append(dict(task=task,seed=records[i]["seed"],comparator=ARMS[j],candidate=ARMS[2],
                                          **{k:x[k] for k in keys},control_correct=x["correct"],candidate_correct=y["correct"],
                                          control_collapsed=x["collapsed_pairs"],candidate_collapsed=y["collapsed_pairs"]))
    summary=dict(seed_results=results,contrasts=contrasts,final_partitions=partitions,all_replays=True,
                 all_groups_matched=True,all_auxiliary_prefixes_matched=True,
                 candidate_gate=all(r["quad_pass"] for r in results if r["arm"]==ARMS[2]),**WORK)
    for name,field in COUNT_FIELDS:summary[name]={a:sum(r[field] for r in results if r["arm"]==a) for a in ARMS}
    require(len(contrasts)==360 and len(partitions)==90,"summary inventory")
    return metrics,summary


def expected_parent_results():
    out=[]
    for s,a in itertools.product(range(288001,288006),("ce_only","ce_pair_assignment")):
        seen=s not in (288002,288003);quad=seen if a=="ce_only" else s==288005
        out.append(dict(seed=s,arm=a,passed=quad,quad_pass=quad,two_char_pass=seen,triple_pass=seen,all_tasks_pass=seen and quad,
                        fitted_train_direct_pass=seen or a=="ce_pair_assignment",seen_holdout_direct_pass=seen))
    return out


def validate_parent(p):
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL" and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity/source")
    actual={a["file"]:(a["sha256"],a["serialized_bytes"]) for a in p["artifacts"]}
    require(len(p["artifacts"])==8 and actual==PARENT_ARTIFACTS,"parent artifacts")
    s=p["validation_summary"]
    require(s["seed_results"]==expected_parent_results() and s["candidate_gate"] is False
            and s["all_replays"] is True and s["all_pairs_matched"] is True,"parent results")
    require(s["quad_pass_counts"]=={"ce_only":3,"ce_pair_assignment":1}
            and s["fitted_train_pass_counts"]=={"ce_only":3,"ce_pair_assignment":5},"parent deciding metrics")


def load_parent(paths):
    parent,_,_,_,_,c=context();paths=[Path(p).resolve() for p in paths]
    require(len(paths)==15 and all(c.audit.sha(p)==w for p,w in zip(paths,SUMMARY_SHAS,strict=True)),"parent summary hashes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C289 parent forbids neural calls")), \
         patch.object(torch.nn.Module,"load_state_dict",side_effect=RuntimeError("C289 parent forbids state loading")), \
         patch.object(torch,"save",side_effect=RuntimeError("C289 parent forbids writes")):
        p,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION)
    parent.validate_result(p);validate_parent(p);return p


def precheck(paths,root):
    validate_seal();p=load_parent(paths);_,_,_,_,_,c=context();root=Path(root);directory=Path(paths[0]).resolve().parent
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for n,w in pins.items():require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==w,"changed source:"+n)
    for n,w in protected.items():require(Path(n).is_file() and c.audit.sha(n)==w,"changed input:"+n)
    for child,w in [(Path(paths[0]).resolve(),SUMMARY_SHAS[0])]+[(c.audit.safe_child(directory,n),v[0]) for n,v in PARENT_ARTIFACTS.items()]:
        require(str(child.resolve()) not in protected and c.audit.sha(child)==w,"parent input")
        protected[str(child.resolve())]=w
    for n in OWN:
        require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9]|27[0-9]|28[0-8])_[^/]+)\.py"
    deps=set(c.factory.LM_SOURCES)|{n for n in p["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps)==manifest()["dependency_union"] and deps<=set(pins) and pins.get(PARENT_SOURCE)==PARENT_BLOB,"dependency coverage")
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(manifest()["source_pins"],manifest()["protected_inputs"]),"protection cardinality")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require(all(p[k] is False for k in ("gate_f_candidate","production_adoption","arbitrary_length_claim")),"result scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(580,1041) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"result protection")
    require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifact set")
    s=p["validation_summary"];rr=s["seed_results"]
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"workload")
    require([(r["seed"],r["arm"]) for r in rr]==identities(),"result identities")
    require(all(type(r[field]) is bool for r in rr for _,field in COUNT_FIELDS),"boolean flags")
    require(all(r["passed"] is r["quad_pass"] and r["all_tasks_pass"] is all(r[t+"_pass"] for t in TASKS) for r in rr),"primary/descriptive gates")
    for name,field in COUNT_FIELDS:require(s[name]=={a:sum(r[field] for r in rr if r["arm"]==a) for a in ARMS},"pass counts")
    gate=all(r["quad_pass"] for r in rr if r["arm"]==ARMS[2])
    require(s["candidate_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"candidate gate")
    require(all(s[k] is True for k in ("all_replays","all_groups_matched","all_auxiliary_prefixes_matched")),"matching/replay")
    require(len(s["contrasts"])==360 and len(s["final_partitions"])==90,"result inventory")
    require({r["comparator"] for r in s["contrasts"]}==set(ARMS[:2])
            and all(r["candidate"]==ARMS[2] for r in s["contrasts"]),"comparator roles")


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c289-early-pair-models-v1"
            and v["identities"]==[list(i) for i in identities()] and len(v["states"])==15,"checkpoint schema")
    return v["states"]


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite):yield from flatten(t)
        else:yield t


def regression_modules(root):
    names=context()[0].regression_modules(root)
    require(len(names)==len(set(names))==manifest()["modules"]-1,"parent modules")
    return names+["tests_lm.test_v05_c289_early_pair_withdrawal"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==manifest()["loaded_tests"] and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED];require(len(kept)==manifest()["focused_tests"],"focused suite")
    return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head
            and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    _,diagnostic,evaluation,transfer,training,c=context();root=Path(__file__).resolve().parents[2]
    guard(root,expected_head,c);torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(summaries,root)
    data=c.p267.dataset();c.p267.validate_data(data)
    triple=c.c270.prompt_dataset(data,c.p267);c.c270.validate_dataset(triple,data,c.p267)
    quad=transfer.dataset(data);transfer.validate_dataset(quad,data,c)
    tokens,targets=training.training_tables(data,c)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);records=[];states=[]
    for seed in SEEDS:
        models=make_models(seed,c)
        for arm in ARMS:
            print(f"[C289] model={len(records)+1}/15 seed={seed} arm={arm}",flush=True)
            rec,state=train_one(models[arm],data,triple,quad,tokens,targets,seed,arm,evaluation,transfer,c)
            records.append(rec);states.append(state)
        check_matched_group(records[-3:])
    torch.save(dict(schema="fold-c289-early-pair-models-v1",identities=[list(i) for i in identities()],states=states),out/"trained-models.pt")
    states=load_bundle(out/"trained-models.pt")
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,c)
        for j,arm in enumerate(ARMS):
            k=3*i+j;evaluation.replay_one(models[arm],states[k],records[k],data,triple,quad,transfer,c)
    metrics,summary=analyze(records,data,diagnostic,transfer,c)
    torch.save(dict(schema="fold-c289-early-pair-eval-v1",records=records),out/"evaluations.pt")
    for n,v in (("architecture-plan.json",manifest()),("dataset.json",data),("triple-dataset.json",triple),("quad-dataset.json",quad),
                ("measurements.json",metrics),("validation-summary.json",summary)):(out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c);precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
           diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
           gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False)
    validate_result(p);(out/"summary.json").write_bytes(blob(p))
    print("=== C289 RESULT ===",flush=True);print(blob(p).decode(),flush=True);return p


def verify_artifacts(outdir,summaries,expected_head):
    _,diagnostic,_,transfer,_,c=context();out=Path(outdir);p=c.audit.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,w in p["input_sha256"].items():require(c.audit.sha(n)==w,"protected input")
    for a in p["artifacts"]:
        child=c.audit.safe_child(out,a["file"])
        require(c.audit.sha(child)==a["sha256"] and child.stat().st_size==a["serialized_bytes"],"output bytes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C289 postcheck forbids neural calls")):
        load_parent(summaries)
        data=c.audit.read_json(out/"dataset.json");c.p267.validate_data(data)
        c.c270.validate_dataset(c.audit.read_json(out/"triple-dataset.json"),data,c.p267)
        transfer.validate_dataset(c.audit.read_json(out/"quad-dataset.json"),data,c)
        v=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(v)=={"schema","records"} and v["schema"]=="fold-c289-early-pair-eval-v1","evaluation schema")
        metrics,summary=analyze(v["records"],data,diagnostic,transfer,c)
        for n,value in (("architecture-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):
            require(c.audit.read_json(out/n)==value,"persisted:"+n)
    require(p["validation_summary"]==summary,"summary reconstruction");return p,metrics


def main():
    p=argparse.ArgumentParser();p.add_argument("--summaries",nargs=15,type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True);p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__=="__main__":main()
