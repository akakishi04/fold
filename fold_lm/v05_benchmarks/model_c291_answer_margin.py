"""C291: answer-wise hardest-rival supervision with concurrent CE/pair-sum controls."""
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
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C291-v5b-answer-wise-hardest-rival-margin"
STAGE = "V5-B-ANSWER-WISE-HARDEST-RIVAL-MARGIN"
BASE = "8f3158ea7f61c87bf674794755c8c36ccb0b27fe"
PARENT_EXECUTION = "327e0a2e45270a4eb60f43daf8cca5c21242987c"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c290_saved_pair_margin_audit.py"
PARENT_BLOB = "43cbbd346f8d6f8b1b57bf9bc026a995ed52786d"
PARENT_SHA = "1f4a3c16130b4c4517ddc7b5c09d7404ed83652fd0d6ce8b9a2438195a9cb11e"
PARENT_ARTIFACTS = {
    "audit-plan.json": ("123a8805343a6c7704ff6042d83928d3069aa43fe79e213e2b5798811d35b6f3",2124),
    "pair-margin-report.json": ("28c87864bab54bd6b2402b0f52d478e35eddc7c67c8eb82ee1afa9e37f4307da",6580944),
    "validation-summary.json": ("88ad4b349cd7bacfe9ea8ca3dccd016329fc684cf828d619ae9b4db76da2b703",46427),
}
SEEDS = tuple(range(291001,291006))
ARMS = ("ce_only","pair_sum","answer_margin")
TASKS = ("two_char","triple","quad")
WEIGHT, MARGIN, TOL = .25, 1., 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c291_answer_margin.py",
       "tests_lm/test_v05_c291_answer_margin.py","tools/run_c291.ps1","tools/invoke_c291.ps1",
       "docs/experiment-ledger-addendum-c291-preregistration.md","docs/v5b-answer-margin-v0.1.md")
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
MANIFEST_SHA = "99916916817da709aead967aaae85052dfb3b049b1bc3ed7356a94abb7781d12"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c290_saved_pair_margin_audit as parent
    legacy,_ = parent.context()
    _,diagnostic,evaluation,transfer,training,c = legacy.context()
    return parent,legacy,diagnostic,evaluation,transfer,training,c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,
                parent_summary_sha256=PARENT_SHA,parent_artifacts={k:list(v) for k,v in PARENT_ARTIFACTS.items()},
                ancestors="C289 plus immutable C289.SUMMARY_SHAS;17 ordered summaries including C290",
                seeds=list(SEEDS),arms=list(ARMS),parameters=14256,max_tokens=48,
                architecture="actual C278 all-token MeanFinalDualReadout;three independent identical initial states",
                question="does answer-wise hardest-rival auxiliary improve reliable unseen four-character transfer at fixed budget",
                objectives={"ce_only":"CE","pair_sum":"CE+.25*mean_pair softplus(1-sum_pair(z_target-z_swapped))",
                            "answer_margin":"CE+.25*mean_row softplus(1+max_non_target_logit-target_logit)"},
                margin=MARGIN,auxiliary_weight=WEIGHT,negative_classes=255,
                changed="auxiliary objective only within matched seed;aggregation and negative set change together",
                supervision="TRAIN labels only in losses;no labels,negative identities or pair metadata enter forward",
                schedule="200 epochs x4;randperm96(seed+291000+epoch);24 intact pairs/batch;profile=epoch%3;length=epoch%2",
                per_length_row_exposures=[100,100],length_profile_updates=[[136,132,132],[132,136,132]],
                fit_rng="seed+292000 reset per arm",steps_per_model=800,optimizer="AdamW",lr=.005,
                betas=[.9,.999],eps=1e-8,weight_decay=0.,clip=1.,
                data_sha256="1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
                triple_sha256="432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",
                quad_sha256="86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b",
                primary="all five answer_margin states pass every untrained four-character fixed criterion",
                descriptive="two/three/all-task and trained-length TRAIN/HOLDOUT direct gates;90 partitions;360 contrasts",
                gate=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
                limitation="not gradient-scale matched;max ties use torch.max first index;no mechanism isolation or automatic superiority",
                source_pins=592,protected_inputs=1066,dependency_union=67,own_tests=40,
                modules=176,loaded_tests=4286,focused_tests=4285,excluded_test=EXCLUDED,
                dtype="CPU float64",threads=2,deterministic=True,replay_tolerance=TOL,
                gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def objective(logits,targets,arm):
    require(arm in ARMS,"objective arm")
    require(logits.ndim==2 and logits.shape[1]==256 and len(logits)>0 and len(logits)%2==0,"objective shape")
    require(logits.dtype==torch.float64 and targets.dtype==torch.int64 and targets.shape==(len(logits),)
            and logits.device==targets.device,"objective dtype/targets")
    require(bool(torch.isfinite(logits).all()) and bool(((targets>=0)&(targets<256)).all()),"objective finite/range")
    y=targets.reshape(-1,2);z=logits.reshape(-1,2,256)
    require(bool((y[:,0]!=y[:,1]).all()),"distinct pair targets")
    i=torch.arange(len(y),device=logits.device)
    correct=z[i,0,y[:,0]]+z[i,1,y[:,1]];swapped=z[i,0,y[:,1]]+z[i,1,y[:,0]]
    pair=F.softplus(MARGIN-(correct-swapped)).mean()
    mask=torch.zeros_like(logits,dtype=torch.bool).scatter_(1,targets[:,None],True)
    rival=logits.masked_fill(mask,float("-inf")).max(dim=1).values
    answer=F.softplus(MARGIN+rival-logits.gather(1,targets[:,None]).squeeze(1)).mean()
    ce=F.cross_entropy(logits,targets)
    total=ce if arm==ARMS[0] else ce+WEIGHT*(pair if arm==ARMS[1] else answer)
    require(all(bool(torch.isfinite(v)) for v in (total,ce,pair,answer)),"nonfinite loss")
    return total,ce,pair,answer


def schedule(seed,rows):
    require(seed in SEEDS and len(rows)==192,"schedule identity")
    groups={}
    for i,r in enumerate(rows):
        key=(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups.setdefault(key,[]).append(i)
    pairs=[]
    for key in sorted(groups):
        ids=sorted(groups[key],key=lambda i:rows[i]["query"])
        require(len(ids)==2 and [rows[i]["query"] for i in ids]==list(key[1]),"complete query pair")
        require(rows[ids[0]]["target"]!=rows[ids[1]]["target"],"pair target collision");pairs.append(ids)
    require(len(pairs)==96 and sorted(sum(pairs,[]))==list(range(192)),"pair partition")
    pairs=torch.tensor(pairs,dtype=torch.int64);batches=[];profiles=[];lengths=[]
    for epoch in range(200):
        order=torch.randperm(96,generator=torch.Generator().manual_seed(seed+291000+epoch))
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
    models=dict(zip(ARMS,(first,copy.deepcopy(first),copy.deepcopy(first)),strict=True))
    for m in models.values():
        require(type(m) is c.c278.MeanFinalDualReadout and sum(p.numel() for p in m.parameters())==14256,"capacity/architecture")
        require(all(p.dtype==torch.float64 and p.device.type=="cpu" for p in m.parameters()),"precision/device")
        require(list(m.state_dict())==list(first.state_dict()) and c.base.fingerprint(m)==c.base.fingerprint(first),"matched initial")
    for a,b in itertools.combinations(models.values(),2):
        require(all(x.data_ptr()!=y.data_ptr() for x,y in zip(a.parameters(),b.parameters(),strict=True)),"independent storage")
    return models


def fit(model,data,tokens,targets,seed,arm):
    require(arm in ARMS and tokens.shape==(2,3,192,48) and targets.shape==(192,)
            and tokens.dtype==targets.dtype==torch.int64,"fit tables")
    ids,profiles,lengths,plan=schedule(seed,data["TRAIN"])
    require(torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)),"target alignment")
    torch.manual_seed(seed+292000)
    opt=torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    traces={k:[] for k in ("ce_history","pair_history","answer_history","total_history","applied_lr","applied_weight")}
    model.train()
    for step in range(800):
        require(len(opt.param_groups)==1 and opt.param_groups[0]["lr"]==.005,"constant LR")
        opt.zero_grad(set_to_none=True);batch=ids[step]
        logits=model(tokens[lengths[step],profiles[step],batch],torch.zeros(48,dtype=torch.int64))
        total,ce,pair,answer=objective(logits,targets[batch],arm)
        for k,v in (("ce_history",ce.detach()),("pair_history",pair.detach()),("answer_history",answer.detach()),
                    ("total_history",total.detach()),("applied_lr",opt.param_groups[0]["lr"]),("applied_weight",0. if arm==ARMS[0] else WEIGHT)):
            traces[k].append(float(v))
        total.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True);opt.step()
        if (step+1)%200==0:print(f"[C291] seed={seed} arm={arm} step={step+1}/800 ce={float(ce.detach()):.6f} pair={float(pair.detach()):.6f} answer={float(answer.detach()):.6f}",flush=True)
    model.eval()
    return dict(steps=800,training_rows=38400,optimizer_creations=1,last_ce=traces["ce_history"][-1],**traces,**plan)


def train_one(model,data,triple,quad,tokens,targets,seed,arm,evaluation,transfer,c):
    initial=c.base.fingerprint(model);back=c.base.fingerprint(model.backbone);head=c.base.fingerprint(model.read)
    with c.p267.counted(model,c.core) as (calls,cores):
        fitted=fit(model,data,tokens,targets,seed,arm);final=c.base.fingerprint(model);model.requires_grad_(False)
        raw=evaluation.evaluate(model,data,triple,quad,transfer,c)
    require(calls==[881,46176] and cores[0]==3524,"train/evaluation workload")
    require(initial!=final and back!=c.base.fingerprint(model.backbone) and head!=c.base.fingerprint(model.read)
            and final==c.base.fingerprint(model),"weight integrity")
    return dict(seed=seed,arm=arm,parameters=14256,initial_sha256=initial,final_sha256=final,weights_changed=True,
                fit=fitted,raw=raw,forward_calls=881,row_presentations=46176,core_forward_calls=3524),{k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def check_fit(f,seed,arm,data):
    require(type(f["steps"]) is int and f["steps"]==800 and type(f["training_rows"]) is int and f["training_rows"]==38400,"fit budget")
    plan=schedule(seed,data["TRAIN"])[3];weight=0. if arm==ARMS[0] else WEIGHT
    require(all(f[k]==v for k,v in plan.items()) and f["applied_lr"]==[.005]*800 and f["applied_weight"]==[weight]*800,"fit schedule")
    require(type(f["optimizer_creations"]) is int and f["optimizer_creations"]==1,"optimizer continuity")
    for key in ("ce_history","pair_history","answer_history","total_history"):
        require(len(f[key])==800 and all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in f[key]),"loss trace")
    aux=f["pair_history"] if arm==ARMS[1] else f["answer_history"]
    require(all(math.isclose(t,ce+weight*q,rel_tol=1e-12,abs_tol=1e-12)
                for t,ce,q in zip(f["total_history"],f["ce_history"],aux,strict=True)),"objective reconstruction")
    require(f["last_ce"]==f["ce_history"][-1],"last loss")


def check_matched_group(records):
    require(len(records)==3 and [r["arm"] for r in records]==list(ARMS) and len({r["seed"] for r in records})==1,"matched identities")
    a=records[0]
    for b in records[1:]:
        require(a["initial_sha256"]==b["initial_sha256"] and all(a["fit"][k]==b["fit"][k]
                for k in ("logical_batch_sha256","rendering_sha256","applied_lr")),"matched initial/data/LR")
        require(all(a["fit"][k][0]==b["fit"][k][0] for k in ("ce_history","pair_history","answer_history")),"matched first input losses")


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
        scored=dict(two_char=c.p267.score(data,r["raw"]["two_char"]),triple=c.c270.score(data,r["raw"]["triple"],c.p267),quad=transfer.score_quad(data,r["raw"]["quad"],c))
        require(all(type(scored[t]["passed"]) is bool for t in TASKS),"task flags")
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
    summary=dict(seed_results=results,contrasts=contrasts,final_partitions=partitions,all_replays=True,all_groups_matched=True,
                 candidate_gate=all(r["quad_pass"] for r in results if r["arm"]==ARMS[2]),**WORK)
    for name,field in COUNT_FIELDS:summary[name]={a:sum(r[field] for r in results if r["arm"]==a) for a in ARMS}
    require(len(contrasts)==360 and len(partitions)==90,"summary inventory")
    return metrics,summary


def validate_parent(p,parent):
    require(p["experiment_id"]=="C290-v5b-saved-pair-margin-audit" and p["commit_sha"]==PARENT_EXECUTION
            and p["status"]=="PASS" and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity/source")
    require(len(p["artifacts"])==3 and {a["file"]:(a["sha256"],a["serialized_bytes"]) for a in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifacts")
    s=p["validation_summary"]
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False
            and s["parent_results"]==parent.expected_results() and s["pair_records"]==19440,"parent diagnostic scope")


def load_parent(paths):
    parent,legacy,_,_,_,_,c=context();paths=[Path(p).resolve() for p in paths]
    wanted=(PARENT_SHA,parent.PARENT_SHA,*legacy.SUMMARY_SHAS)
    require(len(paths)==len(wanted)==17 and all(c.audit.sha(p)==w for p,w in zip(paths,wanted,strict=True)),"parent summary hashes")
    with parent.no_neural():
        p,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION);parent.validate_result(p);validate_parent(p,parent)
        directory=paths[1].parent
        data,triple,quad=[c.audit.read_json(directory/n) for n in ("dataset.json","triple-dataset.json","quad-dataset.json")]
        require(all(digest(v)==manifest()[k] for v,k in zip((data,triple,quad),("data_sha256","triple_sha256","quad_sha256"),strict=True)),"data identity")
    return p,data,triple,quad


def precheck(paths,root):
    validate_seal();p,_,_,_=load_parent(paths);*_,c=context();root=Path(root);directory=Path(paths[0]).resolve().parent
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for n,w in pins.items():require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==w,"changed source:"+n)
    for n,w in protected.items():require(Path(n).is_file() and c.audit.sha(n)==w,"changed input:"+n)
    for child,w in [(Path(paths[0]).resolve(),PARENT_SHA)]+[(c.audit.safe_child(directory,n),v[0]) for n,v in PARENT_ARTIFACTS.items()]:
        require(str(child.resolve()) not in protected and c.audit.sha(child)==w,"parent input")
        protected[str(child.resolve())]=w
    for n in OWN:
        require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|2[4-8][0-9]|290)_[^/]+)\.py"
    deps=set(c.factory.LM_SOURCES)|{n for n in p["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps)==manifest()["dependency_union"] and deps<=set(pins) and pins.get(PARENT_SOURCE)==PARENT_BLOB,"dependency coverage")
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(592,1066),"protection cardinality")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def runtime_preflight(paths,root):
    precheck(paths,root);_,legacy,_,_,_,training,c=context();_,data,_,_=load_parent(paths)
    tokens,targets=training.training_tables(data,c)
    require(tokens.shape==(2,3,192,48) and targets.shape==(192,),"real tables")
    for seed in SEEDS:schedule(seed,data["TRAIN"])
    make_models(SEEDS[0],c)
    z=torch.randn((48,256),generator=torch.Generator().manual_seed(291000),dtype=torch.float64)
    ids=schedule(SEEDS[0],data["TRAIN"])[0][0];y=targets[ids]
    for arm,weight in ((ARMS[0],0.),(ARMS[1],WEIGHT)):
        a=z.clone().requires_grad_();b=z.clone().requires_grad_()
        left=objective(a,y,arm);right=legacy.objective(b,y,weight)
        require(all(torch.equal(x,v) for x,v in zip(left[:3],right,strict=True)),"legacy objective equality")
        require(torch.equal(torch.autograd.grad(left[0],a)[0],torch.autograd.grad(right[0],b)[0]),"legacy gradient equality")
    print("real_tables_pairs_models_and_anchor_objectives = PASS; science not started",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require(all(p[k] is False for k in ("gate_f_candidate","production_adoption","arbitrary_length_claim")),"result scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(592,1066) and set(OWN)<=set(p["source_blobs"])
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
    require(s["all_replays"] is True and s["all_groups_matched"] is True,"matching/replay")
    require(len(s["contrasts"])==360 and len(s["final_partitions"])==90,"result inventory")
    require({r["comparator"] for r in s["contrasts"]}==set(ARMS[:2]) and all(r["candidate"]==ARMS[2] for r in s["contrasts"]),"comparator roles")


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c291-answer-margin-models-v1"
            and v["identities"]==[list(i) for i in identities()] and len(v["states"])==15,"checkpoint schema")
    return v["states"]


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite):yield from flatten(t)
        else:yield t


def regression_modules(root):
    names=context()[0].regression_modules(root)
    require(len(names)==len(set(names))==manifest()["modules"]-1,"parent modules")
    return names+["tests_lm.test_v05_c291_answer_margin"]


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
    _,_,diagnostic,evaluation,transfer,training,c=context();root=Path(__file__).resolve().parents[2]
    guard(root,expected_head,c);torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(summaries,root);_,data,triple,quad=load_parent(summaries)
    tokens,targets=training.training_tables(data,c)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);records=[];states=[]
    for seed in SEEDS:
        models=make_models(seed,c)
        for arm in ARMS:
            print(f"[C291] model={len(records)+1}/15 seed={seed} arm={arm}",flush=True)
            rec,state=train_one(models[arm],data,triple,quad,tokens,targets,seed,arm,evaluation,transfer,c)
            records.append(rec);states.append(state)
        check_matched_group(records[-3:])
    torch.save(dict(schema="fold-c291-answer-margin-models-v1",identities=[list(i) for i in identities()],states=states),out/"trained-models.pt")
    states=load_bundle(out/"trained-models.pt")
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,c)
        for j,arm in enumerate(ARMS):
            k=3*i+j;evaluation.replay_one(models[arm],states[k],records[k],data,triple,quad,transfer,c)
    metrics,summary=analyze(records,data,diagnostic,transfer,c)
    torch.save(dict(schema="fold-c291-answer-margin-eval-v1",records=records),out/"evaluations.pt")
    for n,v in (("architecture-plan.json",manifest()),("dataset.json",data),("triple-dataset.json",triple),("quad-dataset.json",quad),
                ("measurements.json",metrics),("validation-summary.json",summary)):(out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c);precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
           diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
           gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False)
    validate_result(p);(out/"summary.json").write_bytes(blob(p))
    receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","diagnostic_execution_valid","artifacts")}
    receipt.update(source_pins=len(pins),protected_inputs=len(protected),summary_sha256=c.audit.sha(out/"summary.json"))
    print("=== C291 COMPACT RESULT RECEIPT ===",flush=True);print(json.dumps(receipt,sort_keys=True,indent=2),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    parent,_,diagnostic,_,transfer,_,c=context();out=Path(outdir);p=c.audit.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,w in p["input_sha256"].items():require(c.audit.sha(n)==w,"protected input")
    for a in p["artifacts"]:
        child=c.audit.safe_child(out,a["file"])
        require(c.audit.sha(child)==a["sha256"] and child.stat().st_size==a["serialized_bytes"],"output bytes")
    with parent.no_neural():
        _,data,triple,quad=load_parent(summaries)
        for n,v in (("dataset.json",data),("triple-dataset.json",triple),("quad-dataset.json",quad)):
            require(c.audit.read_json(out/n)==v,"persisted data:"+n)
        v=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(v)=={"schema","records"} and v["schema"]=="fold-c291-answer-margin-eval-v1","evaluation schema")
        metrics,summary=analyze(v["records"],data,diagnostic,transfer,c)
        for n,value in (("architecture-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):
            require(c.audit.read_json(out/n)==value,"persisted:"+n)
    require(p["validation_summary"]==summary,"summary reconstruction");return p,metrics


def main():
    p=argparse.ArgumentParser();p.add_argument("--summaries",nargs=17,type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True);p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__=="__main__":main()
