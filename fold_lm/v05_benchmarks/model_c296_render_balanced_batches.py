"""C296: same rendered examples, blocked versus balanced minibatches; fresh paired CE."""
from __future__ import annotations
import argparse
from collections import Counter
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

EXPERIMENT_ID = "C296-v5b-render-balanced-minibatches"
STAGE = "V5-B-RENDER-BALANCED-MINIBATCHES"
BASE = "ae3705004c346edd7c29d1ee5708233d5b77b61d"
PARENT_EXECUTION = "c5ba373c0ed7e4699adc06cd2aac44624b4330e8"
PARENT_SHA = "ea6e10cc0d0371b3dbf11316f37a794b97a7dbd1889053ce771644e9e96f10a5"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c295_ce_budget.py"
PARENT_BLOB = "ae88e50e3aa77fb81b8dc800aee98cdb89276dab"
SEEDS = tuple(range(296001,296006))
ARMS = ("blocked", "balanced")
TASKS = ("two_char", "triple", "quad")
STEPS, MIXED_STEPS, BLOCK = 800, 792, 24
OWN = ("fold_lm/v05_benchmarks/model_c296_render_balanced_batches.py",
       "tests_lm/test_v05_c296_render_balanced_batches.py", "tools/run_c296.ps1", "tools/invoke_c296.ps1",
       "docs/experiment-ledger-addendum-c296-preregistration.md", "docs/v5b-render-balanced-minibatches-v0.1.md")
OUTPUTS = ("architecture-plan.json", "dataset.json", "triple-dataset.json", "quad-dataset.json",
           "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10,train_steps=8000,training_rows=384000,model_forward_calls=9620,
            row_presentations=539520,core_forward_calls=38480,checkpoint_bundle_loads=1,
            model_state_loads=10,new_checkpoint_writes=1,network_calls=0)
COUNTS = (("quad_pass_counts","quad_pass"),("two_char_pass_counts","two_char_pass"),
          ("triple_pass_counts","triple_pass"),("all_tasks_pass_counts","all_tasks_pass"),
          ("fitted_train_pass_counts","fitted_train_direct_pass"),("seen_holdout_pass_counts","seen_holdout_direct_pass"))
MANIFEST_SHA = "b7cdb58ec0caf6389babfe67c4c8ce5d5fb6afef08589d91b6588bc72753ddb9"


def require(ok, message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c295_ce_budget as parent
    audit_parent,_,diagnostic,evaluation,transfer,training,c = parent.context()
    return parent,audit_parent,diagnostic,evaluation,transfer,training,c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_summary_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,
        question="does balancing existing renderings within minibatches improve reliable quad transfer at identical800-update budget",
        seeds=list(SEEDS),arms=list(ARMS),parameters=14256,max_tokens=48,
        architecture="actual C278 all-token MeanFinalDualReadout;ordinary CE;no restricted decoder",
        base_schedule="200epochs*4;randperm96(seed+296000+epoch);24 intact pairs;profile=epoch%3;length=epoch%2",
        event_schema="int64[800,24,4]:length_index,profile_index,first_query_row,second_query_row",
        balanced_schedule="in each complete24-update block,take four consecutive pairs from each of six sorted rendering queues per update",
        balanced_steps=MIXED_STEPS,shared_tail_steps=8,blocks=33,
        invariants="exact rendered-pair multiset per24-update block;identical last8 updates;each source row100 exposures at each length",
        fit_rng="seed+297000 independently reset per arm",optimizer="AdamW",lr=.005,betas=[.9,.999],eps=1e-8,weight_decay=0.,clip=1.,
        per_model_steps=STEPS,batch_rows=48,
        primary="all five balanced final states pass every original four-character fixed criterion",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        limitation="order and within-batch composition change jointly;no claim of isolated gradient conflict or forgetting;not continued C295 weights",
        data_sha256="1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
        triple_sha256="432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",
        quad_sha256="86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b",
        parents=22,source_pins=622,protected_inputs=1131,own_tests=40,modules=181,loaded_tests=4462,focused_tests=4461,
        excluded_test=EXCLUDED,dtype="CPU float64",threads=2,deterministic=True,replay_tolerance=1e-9,
        gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def pairs_from_rows(rows):
    require(len(rows)==192,"TRAIN row count")
    groups={}
    for i,r in enumerate(rows):
        key=(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups.setdefault(key,[]).append(i)
    pairs=[]
    for key in sorted(groups):
        ids=sorted(groups[key],key=lambda i:rows[i]["query"])
        require(len(key[1])==len(key[2])==2 and len(set(key[1]))==len(set(key[2]))==2,"distinct facts")
        require(sorted(key[3])==sorted(key[1]) and len(ids)==2 and [rows[i]["query"] for i in ids]==list(key[1]),"intact query pair")
        require(all(type(v) is int and 0<=v<4 for v in key[2]),"value domain")
        require(all(rows[i]["target"]==48+key[2][key[1].index(rows[i]["query"])] for i in ids),"paired targets")
        pairs.append(ids)
    require(len(pairs)==96 and sorted(sum(pairs,[]))==list(range(192)),"pair partition")
    return torch.tensor(pairs,dtype=torch.int64)


def event_counter(events): return Counter(map(tuple,events.reshape(-1,4).tolist()))


def verify_plan_pair(blocked,balanced):
    for x in (blocked,balanced):
        require(x.dtype==torch.int64 and x.device.type=="cpu" and x.shape==(STEPS,24,4),"event tensor")
        require(bool(((x[:,:,0]>=0)&(x[:,:,0]<2)).all()) and bool(((x[:,:,1]>=0)&(x[:,:,1]<3)).all()),"render indices")
        require(bool(((x[:,:,2:]>=0)&(x[:,:,2:]<192)).all()),"row indices")
    hashes=[]
    for start in range(0,MIXED_STEPS,BLOCK):
        a,b=blocked[start:start+BLOCK],balanced[start:start+BLOCK]
        require(event_counter(a)==event_counter(b),"block multiset")
        hashes.append(digest(sorted(a.reshape(-1,4).tolist())))
        for batch in b:
            require(Counter(map(tuple,batch[:,:2].tolist()))==dict.fromkeys(itertools.product(range(2),range(3)),4),"balanced batch")
    require(torch.equal(blocked[MIXED_STEPS:],balanced[MIXED_STEPS:]),"shared tail")
    require(event_counter(blocked)==event_counter(balanced),"global multiset")
    exposures=torch.zeros((2,192),dtype=torch.int64)
    for length in range(2):
        ids=blocked[blocked[:,:,0]==length][:,2:].flatten()
        exposures[length]=torch.bincount(ids,minlength=192)
    require(bool((exposures==100).all()),"equal length exposures")
    return dict(block_multiset_sha256=hashes,shared_tail_sha256=digest(blocked[MIXED_STEPS:].tolist()),
                global_multiset_sha256=digest(sorted(blocked.reshape(-1,4).tolist())),per_length_row_exposures=exposures.tolist())


def schedules(seed,rows):
    require(seed in SEEDS,"schedule seed")
    pairs=pairs_from_rows(rows);blocked=torch.empty((STEPS,24,4),dtype=torch.int64)
    for epoch in range(200):
        order=torch.randperm(96,generator=torch.Generator().manual_seed(seed+296000+epoch))
        for block in range(4):
            idx=epoch*4+block;blocked[idx,:,0]=epoch%2;blocked[idx,:,1]=epoch%3
            blocked[idx,:,2:]=pairs[order[block*24:(block+1)*24]]
    balanced=blocked.clone()
    for start in range(0,MIXED_STEPS,BLOCK):
        flat=blocked[start:start+BLOCK].reshape(-1,4)
        queues=[flat[(flat[:,0]==l)&(flat[:,1]==p)] for l,p in itertools.product(range(2),range(3))]
        require(all(q.shape==(96,4) for q in queues),"render queue coverage")
        for step in range(BLOCK):
            balanced[start+step]=torch.cat([q[step*4:(step+1)*4] for q in queues],dim=0)
    shared=verify_plan_pair(blocked,balanced)
    return dict(zip(ARMS,(blocked,balanced),strict=True)),shared


def render_batch(tokens,targets,events):
    require(tokens.shape==(2,3,192,48) and targets.shape==(192,) and tokens.dtype==targets.dtype==torch.int64,"training tables")
    require(events.shape==(24,4) and events.dtype==torch.int64,"batch events")
    rows=events[:,2:].reshape(-1);lengths=events[:,0].repeat_interleave(2);profiles=events[:,1].repeat_interleave(2)
    require(bool(((rows>=0)&(rows<192)).all()) and bool(((lengths>=0)&(lengths<2)).all()) and bool(((profiles>=0)&(profiles<3)).all()),"batch bounds")
    return tokens[lengths,profiles,rows],targets[rows]


def make_models(seed,c):
    require(seed in SEEDS,"model seed")
    first=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    models=dict(zip(ARMS,(first,copy.deepcopy(first)),strict=True))
    for m in models.values():
        require(type(m) is c.c278.MeanFinalDualReadout and sum(p.numel() for p in m.parameters())==14256,"capacity")
        require(all(p.dtype==torch.float64 and p.device.type=="cpu" for p in m.parameters()),"precision")
        require(c.base.fingerprint(m)==c.base.fingerprint(first) and list(m.state_dict())==list(first.state_dict()),"matched initial")
    require(all(a.data_ptr()!=b.data_ptr() for a,b in zip(models[ARMS[0]].parameters(),models[ARMS[1]].parameters(),strict=True)),"independent states")
    return models


def fit(model,data,tokens,targets,seed,arm):
    require(arm in ARMS,"fit arm")
    require(torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)),"target alignment")
    plans,shared=schedules(seed,data["TRAIN"]);events=plans[arm]
    torch.manual_seed(seed+297000);opt=torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    model.train();losses=[]
    for step in range(STEPS):
        require(len(opt.param_groups)==1 and opt.param_groups[0]["lr"]==.005,"constant LR")
        opt.zero_grad(set_to_none=True);x,y=render_batch(tokens,targets,events[step]);z=model(x,torch.zeros(48,dtype=torch.int64))
        require(z.shape==(48,256) and z.dtype==torch.float64 and bool(torch.isfinite(z).all()),"logits")
        loss=F.cross_entropy(z,y);require(bool(torch.isfinite(loss)),"loss")
        losses.append(float(loss.detach()));loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True);opt.step()
        if (step+1)%200==0:print(f"[C296] seed={seed} arm={arm} step={step+1}/800 ce={losses[-1]:.6f}",flush=True)
    model.eval()
    return dict(steps=800,training_rows=38400,optimizer_creations=1,ce_history=losses,last_ce=losses[-1],
                schedule_events=events.clone(),event_sha256=digest(events.tolist()),**shared)


def check_fit(f,seed,arm,data):
    require(type(f["steps"]) is int and f["steps"]==800 and f["training_rows"]==38400
            and type(f["optimizer_creations"]) is int and f["optimizer_creations"]==1,"fit workload")
    plans,shared=schedules(seed,data["TRAIN"]);events=f["schedule_events"]
    require(isinstance(events,torch.Tensor) and events.dtype==torch.int64 and torch.equal(events,plans[arm]),"persisted schedule")
    require(f["event_sha256"]==digest(events.tolist()) and all(f[k]==v for k,v in shared.items()),"schedule attestations")
    require(len(f["ce_history"])==800 and all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in f["ce_history"])
            and f["last_ce"]==f["ce_history"][-1],"loss history")


def train_one(model,data,triple,quad,tokens,targets,seed,arm,evaluation,transfer,c):
    initial=c.base.fingerprint(model);back=c.base.fingerprint(model.backbone);head=c.base.fingerprint(model.read)
    with c.p267.counted(model,c.core) as (calls,cores):
        f=fit(model,data,tokens,targets,seed,arm);final=c.base.fingerprint(model);model.requires_grad_(False)
        raw=evaluation.evaluate(model,data,triple,quad,transfer,c)
    require(calls==[881,46176] and cores[0]==3524,"train/evaluation workload")
    require(initial!=final and back!=c.base.fingerprint(model.backbone) and head!=c.base.fingerprint(model.read)
            and final==c.base.fingerprint(model),"weight integrity")
    return dict(seed=seed,arm=arm,parameters=14256,initial_sha256=initial,final_sha256=final,weights_changed=True,
                fit=f,raw=raw,forward_calls=881,row_presentations=46176,core_forward_calls=3524),{k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def analyze(records,data,audit_parent,diagnostic,transfer,c):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"cohort")
    metrics=[];results=[];parts=[];contrasts=[]
    for r in records:
        require(r["parameters"]==14256 and r["weights_changed"] is True and r["checkpoint_roundtrip"] is True,"state integrity")
        error=r["reload_max_error"];require(type(error) in (int,float) and math.isfinite(error) and 0<=error<=1e-9,"replay drift")
        keys=("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in keys) and tuple(r[k] for k in keys)==(881,46176,3524,81,7776,324),"record workload")
        check_fit(r["fit"],r["seed"],r["arm"],data);require(set(r["raw"])==set(TASKS),"raw tasks")
        scored=dict(two_char=c.p267.score(data,r["raw"]["two_char"]),triple=c.c270.score(data,r["raw"]["triple"],c.p267),quad=transfer.score_quad(data,r["raw"]["quad"],c))
        flags={t+"_pass":scored[t]["passed"] for t in TASKS};require(all(type(v) is bool for v in flags.values()),"task flags");direct={}
        for task in TASKS:
            normalized=diagnostic.normalize_task(scored[task],task,r["seed"],r["arm"])
            for split in ("TRAIN","HOLDOUT"):
                p=diagnostic.partition([x for x in normalized if x["split"]==split]);direct[(task,split)]=p["direct_pass"]
                obs=[]
                for views in r["raw"][task][split].values():obs.extend(audit_parent.measure(views["normal"],data[split]))
                aux=audit_parent.aggregate(obs);require(aux["rows"]==p["rows"] and aux["correct"]==p["correct"],"roles match scores")
                parts.append(dict(seed=r["seed"],arm=r["arm"],task=task,split=split,**p,output_role_counts=aux["output_role_counts"],oracle_conditional_correct=aux["conditional_correct"]))
        results.append(dict(seed=r["seed"],arm=r["arm"],passed=flags["quad_pass"],all_tasks_pass=all(flags.values()),
            fitted_train_direct_pass=all(direct[(t,"TRAIN")] for t in TASKS[:2]),seen_holdout_direct_pass=all(direct[(t,"HOLDOUT")] for t in TASKS[:2]),**flags))
        metrics.append(dict(seed=r["seed"],arm=r["arm"],**scored))
    for i in range(0,10,2):
        a,b=records[i:i+2];require(a["initial_sha256"]==b["initial_sha256"],"paired initialization")
        verify_plan_pair(a["fit"]["schedule_events"],b["fit"]["schedule_events"])
        for task in TASKS:
            for x,y in zip(metrics[i][task]["totals"],metrics[i+1][task]["totals"],strict=True):
                keys=("split","profile","language","rows","pairs");require(all(x[k]==y[k] for k in keys),"contrast identity")
                contrasts.append(dict(seed=a["seed"],task=task,**{k:x[k] for k in keys},control_correct=x["correct"],candidate_correct=y["correct"],control_collapsed=x["collapsed_pairs"],candidate_collapsed=y["collapsed_pairs"]))
    s=dict(seed_results=results,final_partitions=parts,contrasts=contrasts,all_replays=True,all_pairs_matched=True,
           candidate_gate=all(r["quad_pass"] for r in results if r["arm"]==ARMS[1]),**WORK)
    for name,field in COUNTS:s[name]={a:sum(r[field] for r in results if r["arm"]==a) for a in ARMS}
    require((len(parts),len(contrasts))==(60,180),"inventory");return metrics,s


def expected_parent_results():
    rr=[]
    for seed,arm in itertools.product(range(295001,295006),("ce800","ce1600")):
        seen=seed not in (295002,295003);quad=seed==295001 or (seed==295004 and arm=="ce1600")
        rr.append(dict(seed=seed,arm=arm,passed=quad,quad_pass=quad,two_char_pass=seen,triple_pass=seen,all_tasks_pass=quad,
                       fitted_train_direct_pass=seen,seen_holdout_direct_pass=seen))
    return rr


def load_parent(paths):
    parent,audit_parent,*_,c=context();paths=[Path(p).resolve() for p in paths]
    p293=parent.context()[1];p292,p291,*_=p293.context();old=p291.context()
    wanted=(PARENT_SHA,parent.PARENT_SHA,audit_parent.PARENT_SHA,p293.PARENT_SHA,p292.PARENT_SHA,p291.PARENT_SHA,old[0].PARENT_SHA,*old[1].SUMMARY_SHAS)
    require(len(paths)==len(wanted)==22 and all(c.audit.sha(p)==h for p,h in zip(paths,wanted,strict=True)),"parent hashes")
    with audit_parent.no_neural():
        p,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION);parent.validate_result(p)
        require(p["experiment_id"]=="C295-v5b-ce-training-budget" and p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL"
                and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity")
        require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"parent outputs")
        s=p["validation_summary"];require(s["seed_results"]==expected_parent_results() and s["common_trajectory"] is True
                and s["all_replays"] is True and s["candidate_gate"] is False,"parent result")
        data,triple,quad=[c.audit.read_json(paths[0].parent/n) for n in ("dataset.json","triple-dataset.json","quad-dataset.json")]
        require(all(digest(v)==manifest()[k] for v,k in zip((data,triple,quad),("data_sha256","triple_sha256","quad_sha256"),strict=True)),"dataset identities")
    return p,data,triple,quad


def precheck(paths,root):
    validate_seal();p,_,_,_=load_parent(paths);parent,audit_parent,*_,c=context();root=Path(root).resolve()
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"]);require((len(pins),len(protected))==(616,1116),"inherited protection")
    for n,h in pins.items():require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in protected.items():require(Path(n).is_file() and c.audit.sha(n)==h,"changed input:"+n)
    modules=[parent,audit_parent]+[m for m in parent.context() if isinstance(m,ModuleType)]+[m for m in vars(c).values() if isinstance(m,ModuleType)]
    covered=set()
    for m in modules:
        path=getattr(m,"__file__",None)
        if path and Path(path).resolve().is_relative_to(root):
            name=Path(path).resolve().relative_to(root).as_posix();require(name in pins,"unprotected helper:"+name);covered.add(name)
    require(PARENT_SOURCE in covered and pins[PARENT_SOURCE]==PARENT_BLOB,"parent coverage")
    for child,h in [(Path(paths[0]).resolve(),PARENT_SHA)]+[(c.audit.safe_child(Path(paths[0]).resolve().parent,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(child.resolve()) not in protected and c.audit.sha(child)==h,"parent input");protected[str(child.resolve())]=h
    for n in OWN:require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins));require((len(pins),len(protected))==(622,1131),"protection counts")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def runtime_preflight(paths,root):
    precheck(paths,root);*_,training,c=context();_,data,_,_=load_parent(paths);tokens,targets=training.training_tables(data,c)
    for seed in SEEDS:
        plans,_=schedules(seed,data["TRAIN"])
        for events in plans.values():
            x,y=render_batch(tokens,targets,events[0]);require(x.shape==(48,48) and y.shape==(48,),"real batch")
    make_models(SEEDS[0],c);print("real_render_batches_multisets_and_initial_models = PASS; science not started",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require(p["gate_f_candidate"] is False and p["production_adoption"] is False,"claim scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(622,1131) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"result protection")
    require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"outputs")
    s=p["validation_summary"];rr=s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rr]==identities() and all(type(r[f]) is bool for r in rr for _,f in COUNTS),"results")
    for name,field in COUNTS:require(s[name]=={a:sum(r[field] for r in rr if r["arm"]==a) for a in ARMS},"pass counts")
    require(all(r["passed"] is r["quad_pass"] and r["all_tasks_pass"] is all(r[t+"_pass"] for t in TASKS) for r in rr),"gate alignment")
    gate=all(r["quad_pass"] for r in rr if r["arm"]==ARMS[1])
    require(s["candidate_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"candidate gate")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()) and s["all_replays"] is True and s["all_pairs_matched"] is True,"workload")
    require((len(s["final_partitions"]),len(s["contrasts"]))==(60,180),"result inventory")


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c296-render-models-v1"
            and v["identities"]==[list(i) for i in identities()] and len(v["states"])==10,"bundle schema")
    return v["states"]


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite):yield from flatten(t)
        else:yield t


def regression_modules(root):
    names=context()[0].regression_modules(root);require(len(names)==len(set(names))==manifest()["modules"]-1,"parent modules")
    return names+["tests_lm.test_v05_c296_render_balanced_batches"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==manifest()["loaded_tests"] and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED];require(len(kept)==manifest()["focused_tests"],"focused suite")
    return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    _,audit_parent,diagnostic,evaluation,transfer,training,c=context();root=Path(__file__).resolve().parents[2]
    guard(root,expected_head,c);torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(summaries,root);_,data,triple,quad=load_parent(summaries);tokens,targets=training.training_tables(data,c)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);records=[];states=[]
    for seed in SEEDS:
        models=make_models(seed,c)
        for arm in ARMS:
            print(f"[C296] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            r,state=train_one(models[arm],data,triple,quad,tokens,targets,seed,arm,evaluation,transfer,c);records.append(r);states.append(state)
    torch.save(dict(schema="fold-c296-render-models-v1",identities=[list(i) for i in identities()],states=states),out/"trained-models.pt")
    loaded=load_bundle(out/"trained-models.pt")
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,c)
        for j,arm in enumerate(ARMS):
            idx=2*i+j;evaluation.replay_one(models[arm],loaded[idx],records[idx],data,triple,quad,transfer,c)
    metrics,summary=analyze(records,data,audit_parent,diagnostic,transfer,c)
    torch.save(dict(schema="fold-c296-render-eval-v1",records=records),out/"evaluations.pt")
    for n,v in (("architecture-plan.json",manifest()),("dataset.json",data),("triple-dataset.json",triple),("quad-dataset.json",quad),("measurements.json",metrics),("validation-summary.json",summary)):(out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c);precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
           source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,gate_f_candidate=False,production_adoption=False)
    validate_result(p);(out/"summary.json").write_bytes(blob(p))
    receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","diagnostic_execution_valid","artifacts")}
    receipt.update(source_pins=len(pins),protected_inputs=len(protected),summary_sha256=c.audit.sha(out/"summary.json"))
    print("=== C296 COMPACT RESULT RECEIPT ===",flush=True);print(json.dumps(receipt,indent=2,sort_keys=True),flush=True);return p


def verify_artifacts(outdir,summaries,expected_head):
    _,audit_parent,diagnostic,_,transfer,_,c=context();out=Path(outdir);p=c.audit.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items():require(c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"]);require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with audit_parent.no_neural():
        _,data,triple,quad=load_parent(summaries)
        for n,v in (("dataset.json",data),("triple-dataset.json",triple),("quad-dataset.json",quad)):require(c.audit.read_json(out/n)==v,"persisted data")
        archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c296-render-eval-v1","evaluation schema")
        metrics,summary=analyze(archive["records"],data,audit_parent,diagnostic,transfer,c)
        for n,v in (("architecture-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(summary==p["validation_summary"],"summary reconstruction");return p,metrics


def main():
    p=argparse.ArgumentParser();p.add_argument("--summaries",nargs=22,type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True);p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))


if __name__=="__main__":main()
