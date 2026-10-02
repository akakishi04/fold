"""C295: predeclared CE800/CE1600 snapshots of five uninterrupted trajectories."""
from __future__ import annotations
import argparse
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

EXPERIMENT_ID = "C295-v5b-ce-training-budget"
STAGE = "V5-B-CE-TRAINING-BUDGET"
BASE = "1ef1dd45252819d5925d78eaaea3d40b156aeda2"
PARENT_EXECUTION = "dead7ca153a8aadb6f30135f47a59981e4b4dfcf"
PARENT_SHA = "abdf1b71f56e3f452d3955277a659722ca38f95a47be1dc6ca5330e688e37e10"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c294_saved_support_choice_audit.py"
PARENT_BLOB = "c645e0b62eba41c6f48fa140fa26f8cc3a26e3b9"
PARENT_ARTIFACTS = {
    "audit-plan.json": ("e929d73dabbcc3c6c229c46282854f8c196802e4e52995f10eb94b977b9ba1c6",2053),
    "support-choice-report.json": ("878b04c53585d880990edc0180627e52b68efbdb7da8cc73ff88c41f75bc4491",25996203),
    "validation-summary.json": ("820d37672cd1333ce613dd9c9f5d70a7a55e8fcca128796fb06b7aa5dfaf124f",101776),
}
SEEDS = tuple(range(295001,295006))
ARMS = ("ce800","ce1600")
BUDGETS = dict(zip(ARMS,(800,1600),strict=True))
TASKS = ("two_char","triple","quad")
OWN = ("fold_lm/v05_benchmarks/model_c295_ce_budget.py","tests_lm/test_v05_c295_ce_budget.py",
       "tools/run_c295.ps1","tools/invoke_c295.ps1",
       "docs/experiment-ledger-addendum-c295-preregistration.md","docs/v5b-ce-training-budget-v0.1.md")
OUTPUTS = ("architecture-plan.json","dataset.json","triple-dataset.json","quad-dataset.json",
           "trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(trajectories=5,evaluated_states=10,train_steps=8000,training_rows=384000,
            model_forward_calls=9620,row_presentations=539520,core_forward_calls=38480,
            checkpoint_bundle_loads=1,model_state_loads=20,new_checkpoint_writes=1,network_calls=0)
COUNTS = (("quad_pass_counts","quad_pass"),("two_char_pass_counts","two_char_pass"),
          ("triple_pass_counts","triple_pass"),("all_tasks_pass_counts","all_tasks_pass"),
          ("fitted_train_pass_counts","fitted_train_direct_pass"),("seen_holdout_pass_counts","seen_holdout_direct_pass"))
MANIFEST_SHA = "b35abbf4b55aa4b4722678ea26a558ce9ef3117c839257b6185fd4312c601a7f"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(v):
    return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(v): return hashlib.sha256(blob(v)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c294_saved_support_choice_audit as parent
    p293,c=parent.context()
    _,_,diagnostic,evaluation,transfer,training,c=p293.context()
    return parent,p293,diagnostic,evaluation,transfer,training,c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        parent_summary_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,
        parent_artifacts={k:list(v) for k,v in PARENT_ARTIFACTS.items()},
        question="does a fixed CE extension from800 to1600 updates improve reliable four-character transfer",
        seeds=list(SEEDS),arms=list(ARMS),budgets=BUDGETS,parameters=14256,max_tokens=48,
        architecture="actual C278 all-token MeanFinalDualReadout;no output filtering or auxiliary loss",
        design="five uninterrupted trajectories;clone snapshots after updates800 and1600;evaluate only after all training",
        schedule="400 epochs*4;randperm96(seed+295000+epoch);24 intact pairs;profile=epoch%3;length=epoch%2",
        fit_rng="seed+296000 once per trajectory",per_length_exposure={"ce800":100,"ce1600":200},
        optimizer="one AdamW per trajectory;no reset at800",lr=.005,betas=[.9,.999],eps=1e-8,weight_decay=0.,clip=1.,
        objective="mean CE only",primary="all five ce1600 snapshots pass every original quad criterion",
        limits="double per-state training cost;paired timepoints not independent models;no equal-compute superiority or causal proof",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        data_sha256="1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
        triple_sha256="432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",
        quad_sha256="86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b",
        parents=21,source_pins=616,protected_inputs=1116,own_tests=32,modules=180,loaded_tests=4422,
        focused_tests=4421,excluded_test=EXCLUDED,replay_tolerance=1e-9,dtype="CPU float64",threads=2,
        deterministic=True,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def schedule(seed,rows,steps=1600):
    require(seed in SEEDS and type(steps) is int and steps in (800,1600) and len(rows)==192,"schedule identity")
    groups={}
    for i,r in enumerate(rows):
        key=(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups.setdefault(key,[]).append(i)
    pairs=[]
    for key in sorted(groups):
        ids=sorted(groups[key],key=lambda i:rows[i]["query"])
        require(len(ids)==2 and [rows[i]["query"] for i in ids]==list(key[1]),"paired queries")
        require(len(set(key[2]))==2 and all(rows[i]["target"]==48+key[2][key[1].index(rows[i]["query"])] for i in ids),"paired targets")
        pairs.append(ids)
    require(len(pairs)==96 and sorted(sum(pairs,[]))==list(range(192)),"complete row partition")
    pairs=torch.tensor(pairs,dtype=torch.int64);batches=[];profiles=[];lengths=[]
    for epoch in range(steps//4):
        order=torch.randperm(96,generator=torch.Generator().manual_seed(seed+295000+epoch))
        for block in range(4):
            batches.append(pairs[order[block*24:(block+1)*24]].flatten());profiles.append(epoch%3);lengths.append(epoch%2)
    x,p,l=torch.stack(batches),torch.tensor(profiles),torch.tensor(lengths)
    exposure=[torch.bincount(x[l==j].flatten(),minlength=192).tolist() for j in range(2)]
    require(exposure==[[steps//8]*192]*2,"length exposure")
    return x,p,l,dict(batch_sha256=digest(x.tolist()),rendering_sha256=digest([profiles,lengths]),per_length_exposures=exposure)


def new_model(seed,c):
    require(seed in SEEDS,"model seed")
    model=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    require(sum(p.numel() for p in model.parameters())==14256 and all(p.dtype==torch.float64 and p.device.type=="cpu" for p in model.parameters()),"model capacity/precision")
    return model


def fit_trajectory(model,data,tokens,targets,seed,fingerprint,steps=1600):
    # steps=800 exists for prefix-equivalence authoring tests; scientific run always requests1600.
    require(tokens.shape==(2,3,192,48) and targets.shape==(192,) and tokens.dtype==targets.dtype==torch.int64,"fit tensors")
    require(torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)),"target alignment")
    ids,profiles,lengths,plan=schedule(seed,data["TRAIN"],steps)
    torch.manual_seed(seed+296000);initial=fingerprint(model)
    opt=torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    losses=[];snapshots={};hashes={};model.train()
    for step in range(steps):
        require(len(opt.param_groups)==1 and opt.param_groups[0]["lr"]==.005,"constant LR")
        opt.zero_grad(set_to_none=True);batch=ids[step]
        z=model(tokens[lengths[step],profiles[step],batch],torch.zeros(48,dtype=torch.int64))
        require(z.shape==(48,256) and z.dtype==torch.float64 and bool(torch.isfinite(z).all()),"training logits")
        loss=F.cross_entropy(z,targets[batch]);require(bool(torch.isfinite(loss)),"finite CE")
        losses.append(float(loss.detach()));loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True);opt.step()
        if step+1 in (800,1600):
            arm="ce"+str(step+1);hashes[arm]=fingerprint(model)
            snapshots[arm]={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
        if (step+1)%200==0:print(f"[C295] seed={seed} step={step+1}/{steps} ce={losses[-1]:.6f}",flush=True)
    model.eval()
    return dict(seed=seed,steps=steps,training_rows=48*steps,optimizer_creations=1,initial_sha256=initial,
                snapshot_sha256=hashes,ce_history=losses,prefix_loss_sha256=digest(losses[:800]),**plan),snapshots


def check_trajectory(t,data):
    require(t["seed"] in SEEDS and type(t["steps"]) is int and t["steps"]==1600 and t["training_rows"]==76800
            and type(t["optimizer_creations"]) is int and t["optimizer_creations"]==1,"trajectory budget")
    require(set(t["snapshot_sha256"])==set(ARMS) and all(re.fullmatch(r"[0-9a-f]{64}",h) for h in [t["initial_sha256"],*t["snapshot_sha256"].values()]),"snapshot hashes")
    require(all(h!=t["initial_sha256"] for h in t["snapshot_sha256"].values()),"weights changed")
    losses=t["ce_history"]
    require(len(losses)==1600 and all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in losses),"loss trace")
    require(t["prefix_loss_sha256"]==digest(losses[:800]) and all(t[k]==v for k,v in schedule(t["seed"],data["TRAIN"])[3].items()),"trace/schedule")


def score_snapshot(model,state,seed,arm,t,data,triple,quad,evaluation,transfer,c):
    model.load_state_dict(state,strict=True);model.eval();model.requires_grad_(False)
    require(c.base.fingerprint(model)==t["snapshot_sha256"][arm],"initial snapshot load")
    with c.p267.counted(model,c.core) as (calls,cores):raw=evaluation.evaluate(model,data,triple,quad,transfer,c)
    require(calls==[81,7776] and cores[0]==324 and c.base.fingerprint(model)==t["snapshot_sha256"][arm],"frozen evaluation")
    return dict(seed=seed,arm=arm,steps_at_snapshot=BUDGETS[arm],parameters=14256,final_sha256=t["snapshot_sha256"][arm],
                raw=raw,evaluation_forward_calls=81,evaluation_rows=7776,evaluation_core_calls=324)


def analyze(records,trajectories,data,parent,diagnostic,transfer,c):
    require([(r["seed"],r["arm"]) for r in records]==identities() and [t["seed"] for t in trajectories]==list(SEEDS),"cohort")
    for t in trajectories:check_trajectory(t,data)
    lookup={t["seed"]:t for t in trajectories};metrics=[];results=[];partitions=[];contrasts=[]
    for r in records:
        require(r["parameters"]==14256 and r["steps_at_snapshot"]==BUDGETS[r["arm"]]
                and r["final_sha256"]==lookup[r["seed"]]["snapshot_sha256"][r["arm"]],"snapshot identity")
        require(r["checkpoint_roundtrip"] is True and type(r["reload_max_error"]) in (int,float)
                and math.isfinite(r["reload_max_error"]) and 0<=r["reload_max_error"]<=1e-9,"replay integrity")
        keys=("evaluation_forward_calls","evaluation_rows","evaluation_core_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in keys) and tuple(r[k] for k in keys)==(81,7776,324,81,7776,324),"scoring workload")
        require(set(r["raw"])==set(TASKS),"task inventory")
        scored=dict(two_char=c.p267.score(data,r["raw"]["two_char"]),triple=c.c270.score(data,r["raw"]["triple"],c.p267),quad=transfer.score_quad(data,r["raw"]["quad"],c))
        flags={task+"_pass":scored[task]["passed"] for task in TASKS};require(all(type(v) is bool for v in flags.values()),"flags")
        direct={}
        for task in TASKS:
            normalized=diagnostic.normalize_task(scored[task],task,r["seed"],r["arm"])
            for split in ("TRAIN","HOLDOUT"):
                part=diagnostic.partition([x for x in normalized if x["split"]==split]);direct[(task,split)]=part["direct_pass"]
                observations=[]
                for views in r["raw"][task][split].values():observations.extend(parent.measure(views["normal"],data[split]))
                aux=parent.aggregate(observations)
                require(aux["rows"]==part["rows"] and aux["correct"]==part["correct"],"auxiliary reconciliation")
                partitions.append(dict(seed=r["seed"],arm=r["arm"],task=task,split=split,**part,
                    output_role_counts=aux["output_role_counts"],oracle_conditional_correct=aux["conditional_correct"]))
        results.append(dict(seed=r["seed"],arm=r["arm"],passed=flags["quad_pass"],all_tasks_pass=all(flags.values()),
            fitted_train_direct_pass=all(direct[(t,"TRAIN")] for t in TASKS[:2]),seen_holdout_direct_pass=all(direct[(t,"HOLDOUT")] for t in TASKS[:2]),**flags))
        metrics.append(dict(seed=r["seed"],arm=r["arm"],**scored))
    for i in range(0,10,2):
        for task in TASKS:
            for a,b in zip(metrics[i][task]["totals"],metrics[i+1][task]["totals"],strict=True):
                keys=("split","profile","language","rows","pairs");require(all(a[k]==b[k] for k in keys),"contrast identity")
                contrasts.append(dict(seed=records[i]["seed"],task=task,**{k:a[k] for k in keys},
                    control_correct=a["correct"],candidate_correct=b["correct"],control_collapsed=a["collapsed_pairs"],candidate_collapsed=b["collapsed_pairs"]))
    s=dict(seed_results=results,final_partitions=partitions,contrasts=contrasts,all_replays=True,common_trajectory=True,
           candidate_gate=all(r["quad_pass"] for r in results if r["arm"]=="ce1600"),**WORK)
    for name,field in COUNTS:s[name]={arm:sum(r[field] for r in results if r["arm"]==arm) for arm in ARMS}
    require(len(partitions)==60 and len(contrasts)==180,"summary inventory")
    return metrics,s


def load_parent(paths):
    parent,p293,*_,c=context();paths=[Path(p).resolve() for p in paths]
    p292,p291,*_=p293.context();old=p291.context()
    wanted=(PARENT_SHA,parent.PARENT_SHA,p293.PARENT_SHA,p292.PARENT_SHA,p291.PARENT_SHA,old[0].PARENT_SHA,*old[1].SUMMARY_SHAS)
    require(len(paths)==len(wanted)==21 and all(c.audit.sha(p)==h for p,h in zip(paths,wanted,strict=True)),"parent hashes")
    with parent.no_neural():
        p,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION);parent.validate_result(p)
        require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS" and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity")
        require(len(p["artifacts"])==3 and {a["file"]:(a["sha256"],a["serialized_bytes"]) for a in p["artifacts"]}==PARENT_ARTIFACTS,"parent descriptors")
        require(p["validation_summary"]["diagnostic_complete"] is True and p["validation_summary"]["capability_gate_applicable"] is False,"parent scope")
        data,triple,quad=[c.audit.read_json(paths[1].parent/n) for n in ("dataset.json","triple-dataset.json","quad-dataset.json")]
        require(all(digest(v)==manifest()[k] for v,k in zip((data,triple,quad),("data_sha256","triple_sha256","quad_sha256"),strict=True)),"data identities")
    return p,data,triple,quad


def precheck(paths,root):
    validate_seal();p,_,_,_=load_parent(paths);parent,p293,*_,c=context();root=Path(root).resolve()
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"]);require((len(pins),len(protected))==(610,1106),"inherited counts")
    for n,h in pins.items():require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in protected.items():require(Path(n).is_file() and c.audit.sha(n)==h,"changed input:"+n)
    modules=[parent,p293]+[m for m in p293.context() if isinstance(m,ModuleType)]+[m for m in vars(c).values() if isinstance(m,ModuleType)]
    covered=set()
    for m in modules:
        path=getattr(m,"__file__",None)
        if path and Path(path).resolve().is_relative_to(root):
            name=Path(path).resolve().relative_to(root).as_posix();require(name in pins,"unprotected helper:"+name);covered.add(name)
    require(PARENT_SOURCE in covered and pins[PARENT_SOURCE]==PARENT_BLOB,"parent coverage")
    for path,h in [(Path(paths[0]).resolve(),PARENT_SHA)]+[(c.audit.safe_child(Path(paths[0]).resolve().parent,n),v[0]) for n,v in PARENT_ARTIFACTS.items()]:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h,"parent input");protected[str(path.resolve())]=h
    for n in OWN:require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins));require((len(pins),len(protected))==(616,1116),"protection counts")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def runtime_preflight(paths,root):
    precheck(paths,root);*_,training,c=context();_,data,_,_=load_parent(paths)
    tokens,targets=training.training_tables(data,c)
    require(tokens.shape==(2,3,192,48) and targets.shape==(192,),"real training tables")
    for seed in SEEDS:
        a=schedule(seed,data["TRAIN"],800);b=schedule(seed,data["TRAIN"],1600)
        require(all(torch.equal(x,y[:800]) for x,y in zip(a[:3],b[:3],strict=True)),"exact schedule prefix")
    new_model(SEEDS[0],c)
    print("real_tables_schedule_prefix_and_initial_model = PASS; science not started",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require(p["gate_f_candidate"] is False and p["production_adoption"] is False,"claim scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(616,1116) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"result protection")
    require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"outputs")
    s=p["validation_summary"];rr=s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rr]==identities() and all(type(r[f]) is bool for r in rr for _,f in COUNTS),"result cohort/flags")
    for name,field in COUNTS:require(s[name]=={a:sum(r[field] for r in rr if r["arm"]==a) for a in ARMS},"pass counts")
    require(all(r["passed"] is r["quad_pass"] and r["all_tasks_pass"] is all(r[t+"_pass"] for t in TASKS) for r in rr),"gate alignment")
    gate=all(r["quad_pass"] for r in rr if r["arm"]=="ce1600")
    require(s["candidate_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"candidate gate")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()) and s["all_replays"] is True and s["common_trajectory"] is True,"workload/integrity")
    require(len(s["final_partitions"])==60 and len(s["contrasts"])==180,"result inventory")


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c295-budget-states-v1" and v["identities"]==[list(x) for x in identities()] and len(v["states"])==10,"bundle schema")
    return v["states"]


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite):yield from flatten(t)
        else:yield t


def regression_modules(root):
    names=context()[0].regression_modules(root);require(len(names)==len(set(names))==179,"parent modules")
    return names+["tests_lm.test_v05_c295_ce_budget"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==manifest()["loaded_tests"] and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED];require(len(kept)==manifest()["focused_tests"],"focused suite")
    return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss" and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    parent,_,diagnostic,evaluation,transfer,training,c=context();root=Path(__file__).resolve().parents[2]
    guard(root,expected_head,c);torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(summaries,root);_,data,triple,quad=load_parent(summaries);tokens,targets=training.training_tables(data,c)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);trajectories=[];states=[];records=[]
    for seed in SEEDS:
        model=new_model(seed,c);print(f"[C295] trajectory={len(trajectories)+1}/5 seed={seed}",flush=True)
        with c.p267.counted(model,c.core) as (calls,cores):t,snapshots=fit_trajectory(model,data,tokens,targets,seed,c.base.fingerprint,1600)
        require(calls==[1600,76800] and cores[0]==6400,"actual training workload")
        check_trajectory(t,data);trajectories.append(t);states.extend(snapshots[a] for a in ARMS)
    # Evaluation cannot influence any training trajectory: it starts after all five have finished.
    torch.save(dict(schema="fold-c295-budget-states-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    loaded=load_bundle(out/"trained-models.pt")
    for index,(seed,arm) in enumerate(identities()):
        print(f"[C295] frozen_state={index+1}/10 seed={seed} arm={arm}",flush=True)
        r=score_snapshot(new_model(seed,c),states[index],seed,arm,trajectories[index//2],data,triple,quad,evaluation,transfer,c)
        evaluation.replay_one(new_model(seed,c),loaded[index],r,data,triple,quad,transfer,c);records.append(r)
    metrics,summary=analyze(records,trajectories,data,parent,diagnostic,transfer,c)
    torch.save(dict(schema="fold-c295-budget-eval-v1",records=records,trajectories=trajectories),out/"evaluations.pt")
    for n,v in (("architecture-plan.json",manifest()),("dataset.json",data),("triple-dataset.json",triple),("quad-dataset.json",quad),("measurements.json",metrics),("validation-summary.json",summary)):(out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c);precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
           source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,gate_f_candidate=False,production_adoption=False)
    validate_result(p);(out/"summary.json").write_bytes(blob(p))
    receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","diagnostic_execution_valid","artifacts")}
    receipt.update(source_pins=len(pins),protected_inputs=len(protected),summary_sha256=c.audit.sha(out/"summary.json"))
    print("=== C295 COMPACT RESULT RECEIPT ===",flush=True);print(json.dumps(receipt,sort_keys=True,indent=2),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    parent,_,diagnostic,_,transfer,_,c=context();out=Path(outdir);p=c.audit.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items():require(c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"]);require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with parent.no_neural():
        _,data,triple,quad=load_parent(summaries)
        for n,v in (("dataset.json",data),("triple-dataset.json",triple),("quad-dataset.json",quad)):require(c.audit.read_json(out/n)==v,"persisted data")
        v=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(v)=={"schema","records","trajectories"} and v["schema"]=="fold-c295-budget-eval-v1","evaluation schema")
        metrics,summary=analyze(v["records"],v["trajectories"],data,parent,diagnostic,transfer,c)
        for n,val in (("architecture-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):require(c.audit.read_json(out/n)==val,"persisted:"+n)
    require(summary==p["validation_summary"],"summary reconstruction");return p,metrics


def main():
    p=argparse.ArgumentParser();p.add_argument("--summaries",nargs=21,type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True);p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__=="__main__":main()
