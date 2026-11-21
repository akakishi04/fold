"""C268: paired-query discrimination loss; training targets never enter model inputs."""
from __future__ import annotations
import argparse
from collections import defaultdict
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C268-v5b-paired-query-discrimination-loss"
STAGE = "V5-B-PAIRED-QUERY-DISCRIMINATION-LOSS"
BASE = "9465a4bddf1182e1da3044764dec765ae5a7cacc"
PARENT_EXECUTION = "3418e545bc261cf1bb920f2ae8f819deec69150c"
PARENT_SHA = "f5f550d362428feaee12d7eee96db4cc324cea311b9b4e91ec50e4f150ec6ef8"
PARENT_ARTIFACTS = {
    "coverage-plan.json": "4f83a11bd6b2c31d7f1bd23b617772d1eab413e5099d5aafe3c4a34eb453f2d7",
    "dataset.json": "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
    "trained-models.pt": "a300bae3930b23c78bb4cd5285f581b21a243b6529eb770d24669ad25b92bd58",
    "evaluations.pt": "e01decea02b8109fbed19cc01d03091867edac02fbaed00f2a7a78e40b4782f3",
    "measurements.json": "d1c9404f3893d3b110fdbf58e15a4f241847fce8304d58a24ac35d1604acfb23",
    "validation-summary.json": "b8ab346a36cb2167e4d6cd0cbd3f19fefdc161b35a120fe40c33e00d4a8ec3f1",
}
SEEDS = tuple(range(268001,268006))
ARMS = ("ce_only","ce_pair_margin")
SPLITS = ("TRAIN","HOLDOUT")
PROFILES = ("doubled","shared_prefix","shared_suffix")
VIEWS = ("normal","evidence_blind","query_blind")
STEPS, BATCH, MARGIN, COEFFICIENT, TOL = 800, 48, 2.0, 0.1, 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c268_paired_query_loss.py",
       "tests_lm/test_v05_c268_paired_query_loss.py","tools/run_c268.ps1","tools/invoke_c268.ps1",
       "docs/experiment-ledger-addendum-c268-preregistration.md","docs/v5b-paired-query-loss-v0.1.md")
OUTPUTS = ("loss-plan.json","dataset.json","trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "cf16b504aa03e1e5f61c000c161b44c3a551fe7c103096c9119274947fb4e07b"


def require(ok,message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c267_name_coverage_training as parent
    _,core,base,aligned,reader,factory,audit = parent.context()
    return parent,core,base,aligned,reader,factory,audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        seeds=list(SEEDS),arms=list(ARMS),parameters=14256,
        dataset_sha256="1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
        changed="CE versus CE+0.1*mean(relu(2-query_logit_contrast)); identical paired batches in both arms",
        contrast="(z0[t0]-z0[t1])-(z1[t0]-z1[t1]); targets only in training loss",
        margin=MARGIN,coefficient=COEFFICIENT,steps=STEPS,batch=BATCH,lr=.005,
        optimizer="AdamW",betas=[.9,.999],eps=1e-8,weight_decay=0.,clip=1.,
        schedule="96 TRAIN query pairs; randperm96 seed+268000+epoch;24 pairs/batch;profile=epoch%3",
        epochs=200,row_exposures=200,profile_updates=[268,268,264],fit_rng="seed+269000 reset per arm",
        primary="all five ce_pair_margin states pass C267 criteria on both splits/all profiles; control separate",
        gate=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        models=10,train_steps=8000,training_rows=384000,model_forward_calls=8540,
        row_presentations=435840,core_forward_calls=34160,evaluation_forwards=540,
        checkpoint_bundle_loads=1,model_state_loads=10,new_checkpoint_writes=1,
        source_pins=454,protected_inputs=774,direct_dependencies=44,own_tests=24,
        modules=153,loaded_tests=3598,focused_tests=3597,excluded_test=EXCLUDED,
        dtype="CPU float64",threads=2,deterministic=True,replay_tolerance=TOL,network_calls=0,
        gate_f_candidate=False,production_adoption=False,unseen_name_transfer_claim=False,causal_parser_claim=False)


def query_pairs(rows):
    require(len(rows)==192 and len({r["id"] for r in rows})==192,"TRAIN row identity")
    groups = defaultdict(list)
    for i,r in enumerate(rows):
        key = (r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups[key].append(i)
    pairs = []
    for key in sorted(groups):
        ids = sorted(groups[key],key=lambda i:rows[i]["query"])
        require(len(ids)==2 and [rows[i]["query"] for i in ids]==list(key[1]),"both queries required")
        require(rows[ids[0]]["target"]!=rows[ids[1]]["target"],"distinct targets")
        pairs.append(ids)
    require(len(pairs)==96 and sorted(sum(pairs,[]))==list(range(192)),"complete pair partition")
    return torch.tensor(pairs,dtype=torch.int64)


def schedule(seed,rows,steps=800):
    require(seed in SEEDS and type(steps) is int and 0<steps<=800,"schedule identity")
    pairs = query_pairs(rows); batches = []; profiles = []
    for epoch in range((steps+3)//4):
        g = torch.Generator(device="cpu").manual_seed(seed+268000+epoch)
        order = torch.randperm(96,generator=g)
        for block in range(4):
            if len(batches)==steps:
                break
            batches.append(pairs[order[block*24:(block+1)*24]].flatten())
            profiles.append(epoch%3)
    indices = torch.stack(batches)
    return indices,profiles,dict(batch_sha256=digest(indices.tolist()),
        row_exposures=torch.bincount(indices.flatten(),minlength=192).tolist(),
        profile_updates=[profiles.count(i) for i in range(3)])


def objective(logits,targets,arm):
    require(arm in ARMS and logits.shape==(48,256) and targets.shape==(48,),"loss dimensions/arm")
    require(targets.dtype==torch.int64 and bool(torch.isfinite(logits).all()),"loss inputs")
    paired = targets.reshape(24,2)
    require(bool((paired[:,0]!=paired[:,1]).all()) and bool(((targets>=0)&(targets<256)).all()),"training targets")
    z = logits.reshape(24,2,256); i = torch.arange(24,device=logits.device)
    contrast = (z[i,0,paired[:,0]]-z[i,0,paired[:,1]])-(z[i,1,paired[:,0]]-z[i,1,paired[:,1]])
    ce = F.cross_entropy(logits,targets)
    penalty = F.relu(MARGIN-contrast).mean()
    total = ce if arm=="ce_only" else ce+COEFFICIENT*penalty
    return total,ce,penalty


def fit(model,data,tokens,targets,seed,arm):
    require(tokens.shape==(3,192,48) and targets.shape==(192,),"training tables")
    ids,profiles,plan = schedule(seed,data["TRAIN"],STEPS)
    torch.manual_seed(seed+269000)
    opt = torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    model.train()
    for step in range(STEPS):
        opt.zero_grad(set_to_none=True)
        # Pair/target metadata goes to the loss only, never into model.forward.
        logits = model(tokens[profiles[step],ids[step]],torch.zeros(48,dtype=torch.int64))
        loss,ce,penalty = objective(logits,targets[ids[step]],arm)
        require(bool(torch.isfinite(loss)),"nonfinite loss")
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True); opt.step()
        if (step+1)%200==0:
            print(f"[C268] seed={seed} arm={arm} step={step+1}/800 ce={float(ce.detach()):.6f} pair_penalty={float(penalty.detach()):.6f}",flush=True)
    model.eval()
    return dict(steps=STEPS,training_rows=STEPS*48,last_ce=float(ce.detach()),
        last_penalty=float(penalty.detach()),last_total=float(loss.detach()),**plan)


def train_one(model,seed,arm,data,tokens,targets,parent,core,base,factory):
    require(sum(p.numel() for p in model.parameters())==14256,"capacity")
    initial = base.fingerprint(model); back = base.fingerprint(model.backbone); head = base.fingerprint(model.read)
    with parent.counted(model,core) as (counts,cores):
        fitted = fit(model,data,tokens,targets,seed,arm)
        final = base.fingerprint(model)
        raw = parent.evaluate(model,data,factory)
    require(counts==[827,40992] and cores[0]==3308,"training/final workload")
    require(base.fingerprint(model)==final and final!=initial and base.fingerprint(model.backbone)!=back
        and base.fingerprint(model.read)!=head,"weight change/evaluation integrity")
    record = dict(seed=seed,arm=arm,parameters=14256,initial_sha256=initial,final_sha256=final,fit=fitted,raw=raw,
        weights_changed=True,forward_calls=827,row_presentations=40992,core_forward_calls=3308)
    return record,{k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def analyze(records,data,parent):
    parent.validate_data(data)
    require([(r["seed"],r["arm"]) for r in records]==identities(),"complete identities")
    metrics = []; results = []; contrasts = []
    for r in records:
        require(r["parameters"]==14256 and r["weights_changed"] is True and r["checkpoint_roundtrip"] is True,"record integrity")
        require(tuple(r[k] for k in ("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls"))==(827,40992,3308,27,2592,108),"record workload")
        require(type(r["reload_max_error"]) in (int,float) and math.isfinite(r["reload_max_error"]) and 0<=r["reload_max_error"]<=TOL,"replay error")
        expected = schedule(r["seed"],data["TRAIN"])[2]
        require(r["fit"]["steps"]==800 and r["fit"]["training_rows"]==38400 and all(r["fit"][k]==v for k,v in expected.items()),"actual schedule")
        for k in ("last_ce","last_penalty","last_total"):
            require(type(r["fit"][k]) in (int,float) and math.isfinite(r["fit"][k]) and r["fit"][k]>=0,"loss record")
        want = r["fit"]["last_ce"]+(COEFFICIENT*r["fit"]["last_penalty"] if r["arm"]==ARMS[1] else 0.)
        require(abs(want-r["fit"]["last_total"])<=TOL,"loss arithmetic")
        scored = parent.score(data,r["raw"])
        metrics.append(dict(seed=r["seed"],arm=r["arm"],**scored))
        results.append(dict(seed=r["seed"],arm=r["arm"],passed=scored["passed"]))
    for i in range(0,10,2):
        a,b = records[i:i+2]
        require(a["initial_sha256"]==b["initial_sha256"] and a["fit"]["batch_sha256"]==b["fit"]["batch_sha256"],"paired state/batches")
        for x,y in zip(metrics[i]["totals"],metrics[i+1]["totals"],strict=True):
            require(tuple(x[k] for k in ("split","profile","language","rows","pairs"))==tuple(y[k] for k in ("split","profile","language","rows","pairs")),"contrast identities")
            if x["split"]=="HOLDOUT":
                contrasts.append(dict(seed=a["seed"],profile=x["profile"],language=x["language"],rows=x["rows"],pairs=x["pairs"],
                    control_correct=x["correct"],candidate_correct=y["correct"],correct_delta=y["correct"]-x["correct"],
                    control_collapsed=x["collapsed_pairs"],candidate_collapsed=y["collapsed_pairs"],collapse_delta=y["collapsed_pairs"]-x["collapsed_pairs"]))
    summary = dict(models=10,seed_results=results,seed_pass_counts={a:sum(r["passed"] for r in results if r["arm"]==a) for a in ARMS},
        candidate_gate=all(r["passed"] for r in results if r["arm"]==ARMS[1]),contrasts=contrasts,
        train_steps=8000,training_rows=384000,model_forward_calls=8540,row_presentations=435840,core_forward_calls=34160,
        checkpoint_bundle_loads=1,model_state_loads=10,new_checkpoint_writes=1,all_replays=True,all_pairs_matched=True)
    return metrics,summary


def load_parent(path):
    parent,*_,audit = context(); path = Path(path).resolve()
    require(audit.sha(path)==PARENT_SHA,"accepted parent hash")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("parent verification forbids model calls")):
        payload,metrics = parent.verify_artifacts(path.parent,PARENT_EXECUTION)
    parent.validate_result(payload)
    require(payload["status"]=="FAIL" and payload["commit_sha"]==PARENT_EXECUTION
        and payload["validation_summary"]["seed_pass_counts"]=={"doubled_only":0,"mixed_names":1},"C267 valid negative")
    require({x["file"]:x["sha256"] for x in payload["artifacts"]}==PARENT_ARTIFACTS and len(metrics)==10,"accepted artifacts")
    return payload


def precheck(path,root):
    _,*_,factory,audit = context(); root = Path(root); path = Path(path).resolve(); payload = load_parent(path)
    pins,protected = dict(payload["source_blobs"]),dict(payload["input_sha256"])
    for name,wanted in protected.items():
        require(Path(name).is_file() and audit.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items():
        require(audit.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    for child,wanted in [(path,PARENT_SHA)]+[(audit.safe_child(path.parent,x["file"]),x["sha256"]) for x in payload["artifacts"]]:
        key = str(child.resolve()); require(key not in protected,"duplicate parent input"); protected[key] = wanted
    for name in OWN:
        require(name not in pins,"OWN collision"); pins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-7])_[^/]+)\.py"
    deps = set(factory.LM_SOURCES)|{n for n in payload["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps)==44 and deps<=set(pins),"direct dependencies")
    protected.update(audit.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(454,774) and digest(manifest())==MANIFEST_SHA,"registration counts/hash")
    print("registration_check = source_pins:454; protected_inputs:774; manifest_sha256:"+MANIFEST_SHA,flush=True)
    return pins,protected


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(454,774) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==6 and {x["file"] for x in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s = p["validation_summary"]; rr = s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rr]==identities() and all(type(r["passed"]) is bool for r in rr),"result identities")
    require(s["candidate_gate"] is all(r["passed"] for r in rr if r["arm"]==ARMS[1]) and s["seed_pass_counts"]=={a:sum(r["passed"] for r in rr if r["arm"]==a) for a in ARMS},"gate accounting")
    for k in ("models","train_steps","training_rows","model_forward_calls","row_presentations","core_forward_calls","checkpoint_bundle_loads","model_state_loads","new_checkpoint_writes"):
        require(type(s[k]) is int and s[k]==manifest()[k],"workload:"+k)
    require(len(s["contrasts"])==30 and s["all_replays"] is True and s["all_pairs_matched"] is True
        and p["status"]==("PASS" if s["candidate_gate"] else "FAIL"),"status")
    require(all(p[k] is False for k in ("gate_f_candidate","production_adoption","unseen_name_transfer_claim","causal_parser_claim")),"scope")


def load_bundle(path):
    v = torch.load(path,map_location="cpu",weights_only=True)
    require(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c268-query-loss-models-v1","bundle schema")
    require(v["identities"]==[list(x) for x in identities()] and len(v["states"])==10,"bundle identities")
    return v["states"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names)==len(set(names))==152,"parent modules")
    return names+["tests_lm.test_v05_c268_paired_query_loss"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids = [t.id() for t in tests]
    require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"suite identities")
    kept = [t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(3598,3597),"suite counts")
    return unittest.TestSuite(kept)


def run(*,c267_summary,output_dir,expected_head):
    parent,core,base,aligned,reader,factory,audit = context(); root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected = precheck(c267_summary,root)
    data = parent.dataset(); parent.validate_data(data)
    tokens,targets = parent.training_tables(data,factory)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False); records = []; states = []
    for seed in SEEDS:
        initial = base.make_model(factory.new_model(seed),"aligned_precore_read",seed,aligned,reader)
        initial_sha = base.fingerprint(initial)
        for arm in ARMS:
            print(f"[C268] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            r,state = train_one(copy.deepcopy(initial),seed,arm,data,tokens,targets,parent,core,base,factory)
            require(r["initial_sha256"]==initial_sha and base.fingerprint(initial)==initial_sha,"paired template")
            records.append(r); states.append(state)
    torch.save(dict(schema="fold-c268-query-loss-models-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for r,state in zip(records,load_bundle(out/"trained-models.pt"),strict=True):
        model = base.make_model(factory.new_model(r["seed"]),"aligned_precore_read",r["seed"],aligned,reader)
        parent.replay_one(model,state,r,data,core,base,factory)
    metrics,summary = analyze(records,data,parent)
    torch.save(dict(schema="fold-c268-query-loss-eval-v1",records=records),out/"evaluations.pt")
    for name,value in (("loss-plan.json",manifest()),("dataset.json",data),("measurements.json",metrics),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(); precheck(c267_summary,root)
    for name,wanted in protected.items():
        require(audit.sha(name)==wanted,"modified input")
    payload = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,production_adoption=False,unseen_name_transfer_claim=False,causal_parser_claim=False)
    validate_result(payload); (out/"summary.json").write_bytes(blob(payload))
    print("=== C268 RESULT ===",flush=True); print(blob(payload).decode(),flush=True)
    return payload


def verify_artifacts(output_dir,expected_head):
    parent,*_,audit = context(); out = Path(output_dir); p = audit.read_json(out/"summary.json")
    validate_result(p); require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():
        require(audit.sha(name)==wanted,"postcheck input")
    for x in p["artifacts"]:
        child = audit.safe_child(out,x["file"])
        require(audit.sha(child)==x["sha256"] and child.stat().st_size==x["serialized_bytes"],"output bytes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("saved postcheck forbids model calls")):
        data = audit.read_json(out/"dataset.json"); v = torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(v)=={"schema","records"} and v["schema"]=="fold-c268-query-loss-eval-v1","eval schema")
        metrics,summary = analyze(v["records"],data,parent)
        for name,value in (("loss-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):
            require(audit.read_json(out/name)==value,"persisted reconstruction:"+name)
    require(p["validation_summary"]==summary,"saved summary")
    return p,metrics


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("c267-summary","output-dir"):
        p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--expected-head",required=True); run(**vars(p.parse_args()))


if __name__=="__main__":
    main()
