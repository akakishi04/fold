"""C313: prospective six-character transfer in every frozen C312 checkpoint."""
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

EXPERIMENT_ID = "C313-v5b-frozen-six-transfer"
STAGE = "V5-B-FROZEN-SIX-TRANSFER"
BASE = "0c4dfe291010f90d7b444c36fd49d3accf64158c"
PARENT_EXECUTION = "f481ae2b547bccc5cd5f43ae2654f89e8fa3140f"
PARENT_SHA = "2bb0efc9a9f128a0aeda9585dabab4ee0c672ba2e9b31f4b148cc6ba959a5ed6"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c312_value_balanced_batches.py"
PARENT_BLOB = "a676b684d605424c35713ac08940e06ab16553f4"
WIDE_SOURCE = "fold_lm/v05_benchmarks/model_c304_length_breadth.py"
WIDE_BLOB = "cacb5852a29171aa8079e634d929fdd54e7f4f58"
SEEDS = tuple(range(312001, 312006))
ARMS = ("random_pairs", "value_balanced")
PRIMARY_ARM = "random_pairs"
PROFILES = ("repeat", "shared_prefix", "shared_suffix")
SPLITS = ("TRAIN", "HOLDOUT")
VIEWS = ("normal", "evidence_blind", "query_blind")
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
PROMPTS_SHA = "ecf2c9784213ac8fcebfd9ac03bea42317629edcea330771c92c72d71777583d"
OWN = ("fold_lm/v05_benchmarks/model_c313_frozen_six_transfer.py",
       "tests_lm/test_v05_c313_frozen_six_transfer.py", "tools/run_c313.ps1", "tools/invoke_c313.ps1",
       "docs/experiment-ledger-addendum-c313-preregistration.md", "docs/v5b-frozen-six-transfer-v0.1.md")
OUTPUTS = ("evaluation-plan.json", "six-dataset.json", "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10, train_steps=0, model_forward_calls=2430, row_presentations=233280,
            core_forward_calls=9720, model_state_loads=10, checkpoint_bundle_loads=1,
            new_checkpoint_writes=0, network_calls=0)
MANIFEST_SHA = "f6e02599e4704457781f1ac49272a0a8d50d9c40524d66d4bcfb173e1cf86cca"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS, ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c312_value_balanced_batches as parent
    chain = parent.context()
    return parent, chain[1], chain[3], chain[4], chain[6], chain[-1]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
        wide_source=WIDE_SOURCE, wide_blob=WIDE_BLOB, seeds=list(SEEDS), arms=list(ARMS), primary_arm=PRIMARY_ARM,
        question="do all five retained random-batch baseline checkpoints transfer from training lengths2..4 to unseen6 without retraining",
        comparison="all five balanced checkpoints retained,including312002;not selected per row or retuned",
        slots=64, parameters=14256, old_lengths=[2,3,4,5], new_length=6, max_prompt_bytes=61, max_encoded_tokens=63,
        profiles=list(PROFILES), views=list(VIEWS), data_sha256=DATA_SHA, old_prompts_sha256=PROMPTS_SHA,
        passes="old2..5 before;new6;old2..5 after;frozen weights,original256-class argmax",
        baseline="each old view reproduces the exact C312 archive<=1e-9 and exact argmax;both arms old task flags unchanged",
        primary="ALL5 random_pairs states pass every original-style six-character local/masked gate",
        gates=dict(accuracy=.90, query_pair=.80, evidence_drop=.35, query_drop=.35, two_order=.80),
        limits="same models/value split/name templates;not fresh seeds,arbitrary-length proof,balanced rescue or Gate F",
        reports="10 states,20 six partitions,20 paired-five-to-six transitions,both arm pass counts and old replay errors",
        raw_logit_payload_bytes=477757440, parents=39, source_pins=724, protected_inputs=1357,
        own_tests=32, modules=198, loaded_tests=5030, focused_tests=5029, excluded_test=EXCLUDED,
        dtype="CPU float64", threads=2, deterministic=True, gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None and digest(manifest()) == MANIFEST_SHA, "manifest seal")


def render(row, length, profile, view="normal"):
    require(type(length) is int and length in (2,3,4,5,6) and profile in PROFILES and view in VIEWS, "render policy")
    require(row["language"] in ("en","ja"), "language")
    chars = ("a","b","c") if row["language"] == "en" else ("甲","乙","丙")
    i,j = row["entities"]; u,v = chars[i],chars[j]
    names = {i:u*length, j:v*length if profile == PROFILES[0] else u*(length-1)+v if profile == PROFILES[1] else v+u*(length-1)}
    values = dict(zip(row["entities"],row["values"],strict=True))
    return ";".join(names[k]+"="+("?" if view == "evidence_blind" else str(values[k])) for k in row["permutation"])+";"+("?" if view == "query_blind" else names[row["query"]])+"="


def six_prompts(data):
    return {s:{p:[dict(source_id=r["id"], target=r["target"], views={v:render(r,6,p,v) for v in VIEWS})
                   for r in data[s]] for p in PROFILES} for s in SPLITS}


def check_prompts(data, old, six, wide):
    require(digest(data) == DATA_SHA and digest(old) == PROMPTS_SHA and six == six_prompts(data), "data/prompt identity")
    old_normal=set(); old_bytes=set(); new_bytes=set(); new_normal=[]; maximum=0
    for n,s,p in itertools.product((2,3,4,5),SPLITS,PROFILES):
        require(len(old[str(n)][s][p]) == len(data[s]), "old row count")
        for r,item in zip(data[s],old[str(n)][s][p],strict=True):
            require(item["source_id"] == r["id"] and item["target"] == r["target"] and set(item["views"]) == set(VIEWS), "old identities")
            for v in VIEWS:
                text=render(r,n,p,v)
                require(text == item["views"][v] == wide.render(r,n,p,v), "old renderer compatibility")
                old_bytes.update(text.encode("utf-8"))
            old_normal.add(item["views"]["normal"])
    for s,p in itertools.product(SPLITS,PROFILES):
        for item in six[s][p]:
            new_normal.append(item["views"]["normal"])
            for text in item["views"].values():
                raw=text.encode("utf-8"); maximum=max(maximum,len(raw)); new_bytes.update(raw)
                x=wide.prefix_tensor(text)
                require(x.shape == (64,) and x.dtype == torch.int64 and x[0] == 257 and x[len(raw)+1] == 258
                        and torch.equal(x[1:len(raw)+1],torch.tensor(list(raw))) and bool((x[len(raw)+2:] == 256).all()), "untruncated bytes")
    require(maximum == 61 and len(new_normal) == len(set(new_normal)) == 864
            and not set(new_normal)&old_normal and new_bytes <= old_bytes, "novel length,not vocabulary")


def expected_parent_flags():
    return [dict(seed=seed, arm=arm, length_pass={str(n):not(seed==312002 and arm==ARMS[1] and n==5) for n in (2,3,4,5)},
        quint_pass=not(seed==312002 and arm==ARMS[1]), all_lengths_pass=not(seed==312002 and arm==ARMS[1]),
        fitted_train_direct_pass=True, trained_length_holdout_direct_pass=True) for seed,arm in identities()]


def parent_hashes(parent): return (PARENT_SHA,*parent.parent_hashes(parent.context()[0]))


def load_parent(paths):
    parent, no_models, _, wide, _, c=context(); paths=[Path(p).resolve() for p in paths]
    hashes=parent_hashes(parent)
    require(len(paths)==len(hashes)==39 and all(c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)), "39 parent hashes")
    with no_models.no_neural():
        payload,metrics=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); parent.validate_result(payload)
        require(payload["experiment_id"]=="C312-v5b-value-balanced-minibatches" and payload["status"]=="FAIL"
                and payload["commit_sha"]==PARENT_EXECUTION and payload["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB
                and payload["source_blobs"].get(WIDE_SOURCE)==WIDE_BLOB, "parent identity")
        require(len(payload["artifacts"])==7 and {a["file"] for a in payload["artifacts"]}==set(parent.OUTPUTS), "parent artifacts")
        s=payload["validation_summary"]
        require(s["seed_results"]==expected_parent_flags() and s["candidate_gate"] is False and s["all_pairs_matched"] is True
                and s["all_replays"] is True, "parent outcomes")
        data=c.audit.read_json(paths[0].parent/"dataset.json"); c.p267.validate_data(data)
        old=c.audit.read_json(paths[0].parent/"length-datasets.json"); check_prompts(data,old,six_prompts(data),wide)
        archive=torch.load(paths[0].parent/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c312-value-batches-eval-v1"
                and [(r["seed"],r["arm"]) for r in archive["records"]]==identities(), "parent evaluation archive")
    return payload,data,old,archive["records"]


def precheck(paths,root):
    validate_seal(); payload,_,_,_=load_parent(paths); parent,_,_,wide,_,c=context(); root=Path(root).resolve()
    pins,protected=dict(payload["source_blobs"]),dict(payload["input_sha256"])
    require((len(pins),len(protected))==(718,1343) and all(pins.get(n)==h for n,h in parent.PINNED.items())
            and all(pins.get(n)==h for n,h in wide.PINNED.items()), "inherited protection")
    for m in [parent,*parent.context(),*wide.context(),*vars(c).values(),c.factory.language_module()]:
        path=getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root): require(Path(path).resolve().relative_to(root).as_posix() in pins,"unprotected helper")
    for n,h in pins.items(): require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in protected.items(): require(Path(n).is_file() and c.audit.sha(n)==h,"changed input:"+n)
    folder=Path(paths[0]).resolve().parent
    for path,h in [(folder/"summary.json",PARENT_SHA)]+[(c.audit.safe_child(folder,a["file"]),a["sha256"]) for a in payload["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h,"parent input"); protected[str(path.resolve())]=h
    for n in OWN: require(n not in pins,"OWN collision"); pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins)); require((len(pins),len(protected))==(724,1357),"protection counts")
    print(f"registration_check = source_pins:724; protected_inputs:1357; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def hook_snapshot(model):
    attrs=("_forward_pre_hooks","_forward_hooks","_forward_pre_hooks_with_kwargs","_forward_hooks_with_kwargs","_forward_hooks_always_called")
    return [(n,tuple(tuple(getattr(m,a)) for a in attrs)) for n,m in model.named_modules()]


def evaluate_six(model,prompts,data,wide,c):
    require(not any(m.training for m in model.modules()) and not any(p.requires_grad for p in model.parameters()),"frozen evaluation")
    raw={}
    with torch.no_grad():
        for s in SPLITS:
            raw[s]={}
            for p in PROFILES:
                raw[s][p]={}
                for v in VIEWS:
                    chunks=[]
                    for start in range(0,len(data[s]),96):
                        x=torch.stack([wide.prefix_tensor(r["views"][v]) for r in prompts[s][p][start:start+96]])
                        z=model(x,torch.zeros(len(x),dtype=torch.int64)); c.p267.check_logits(z,len(x)); chunks.append(z.detach().clone())
                    raw[s][p][v]=torch.cat(chunks)
    return raw


def infer_one(model,state,anchor,data,old,six,wide,c):
    model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(False)
    fingerprint=c.base.fingerprint(model); hooks=hook_snapshot(model)
    require(fingerprint==anchor["final_sha256"],"strict checkpoint")
    outputs={}
    for name in ("before","six","after"):
        print(f"[C313] seed={anchor['seed']} arm={anchor['arm']} pass={name}",flush=True)
        with torch.no_grad(),c.p267.counted(model,c.core) as (calls,cores):
            outputs[name]=evaluate_six(model,six,data,wide,c) if name=="six" else wide.evaluate(model,old,data,c)
        expected=(27,2592,108) if name=="six" else (108,10368,432)
        require((*calls,cores[0])==expected and c.base.fingerprint(model)==fingerprint and hook_snapshot(model)==hooks,"pass accounting/preservation")
    errors=[wide.replay_error(outputs[n],anchor["raw"],data,c) for n in ("before","after")]
    return dict(seed=anchor["seed"],arm=anchor["arm"],final_sha256=fingerprint,raw=outputs,replay_errors=errors,
                weights_preserved=True,hooks_restored=True,forward_calls=243,row_presentations=23328,core_forward_calls=972)


def transition(five,six,rows):
    y=torch.tensor([r["target"] for r in rows]); counts=dict(rows=0,both_correct=0,new_error=0,recovered=0,both_wrong=0,same_wrong=0)
    for p in PROFILES:
        a=five[p]["normal"].argmax(1); b=six[p]["normal"].argmax(1); ac=a==y; bc=b==y
        for k,v in dict(rows=len(rows),both_correct=int((ac&bc).sum()),new_error=int((ac&~bc).sum()),
                       recovered=int((~ac&bc).sum()),both_wrong=int((~ac&~bc).sum()),same_wrong=int((~ac&~bc&(a==b)).sum())).items(): counts[k]+=v
    require(counts["rows"]==sum(counts[k] for k in ("both_correct","new_error","recovered","both_wrong")),"transition conservation")
    return counts


def analyze(records,anchors,data,wide,diag,c):
    require([(r["seed"],r["arm"]) for r in records]==identities() and [(r["seed"],r["arm"]) for r in anchors]==identities(),"complete cohort")
    metrics,results,parts,transitions,controls=[],[],[],[],[]
    for r,old,flag in zip(records,anchors,expected_parent_flags(),strict=True):
        key=dict(seed=r["seed"],arm=r["arm"])
        require(r["final_sha256"]==old["final_sha256"] and r["weights_preserved"] is True and r["hooks_restored"] is True
                and set(r["raw"])=={"before","six","after"},"state provenance")
        require(all(type(r[k]) is int for k in ("forward_calls","row_presentations","core_forward_calls"))
                and tuple(r[k] for k in ("forward_calls","row_presentations","core_forward_calls"))==(243,23328,972),"record workload")
        errors=[wide.replay_error(r["raw"][n],old["raw"],data,c) for n in ("before","after")]
        require(errors==r["replay_errors"] and all(type(e) in (int,float) and math.isfinite(e) and 0<=e<=1e-9 for e in errors),"baseline reproduction")
        for mode in ("before","after"):
            require({n:wide.score_length(data,z,c)["passed"] for n,z in r["raw"][mode].items()}==flag["length_pass"],"original gates")
        six=r["raw"]["six"]
        require(set(six)==set(SPLITS) and all(set(six[s])==set(PROFILES) for s in SPLITS),"six domain")
        for s,p in itertools.product(SPLITS,PROFILES):
            require(set(six[s][p])==set(VIEWS),"six views")
            for z in six[s][p].values(): c.p267.check_logits(z,len(data[s])); require(not z.requires_grad,"detached logits")
        scored=wide.score_length(data,six,c); require(type(scored["passed"]) is bool,"six flag")
        norm=diag.normalize_task(scored,"triple",r["seed"],r["arm"])
        for s in SPLITS:
            part=diag.partition([p for p in norm if p["split"]==s]); parts.append(dict(**key,identifier_length=6,split=s,length_trained=False,**part))
            t=transition(old["raw"]["5"][s],six[s],data[s]); require(t["both_correct"]+t["recovered"]==part["correct"],"six count reconciliation")
            transitions.append(dict(**key,split=s,**t))
        controls.append(dict(**key,replay_errors=errors,matched=True))
        results.append(dict(**key,five_pass=flag["quint_pass"],six_pass=scored["passed"]))
        metrics.append(dict(**key,six_score=scored))
    counts={a:sum(r["six_pass"] for r in results if r["arm"]==a) for a in ARMS}
    return metrics,dict(seed_results=results,final_partitions=parts,five_to_six=transitions,reproductions=controls,
        six_pass_counts=counts,primary_arm=PRIMARY_ARM,primary_gate=counts[PRIMARY_ARM]==5,all_replays=True,**WORK)


def runtime_preflight(paths,root):
    torch.set_num_threads(2); precheck(paths,root)
    parent,_,policy,wide,_,c=context(); _,data,old,anchors=load_parent(paths); six=six_prompts(data)
    states=parent.load_bundle(Path(paths[0]).resolve().parent/"trained-models.pt"); models=parent.make_models(SEEDS[0],policy,wide,c)
    for i,arm in enumerate(ARMS):
        model=models[arm]; model.load_state_dict(states[i],strict=True); model.eval(); model.requires_grad_(False)
        fp=c.base.fingerprint(model); require(fp==anchors[i]["final_sha256"],"probe checkpoint")
        ids=[next(i for i,r in enumerate(data["TRAIN"]) if r["language"]==lang) for lang in ("en","ja")]
        oldx=torch.stack([wide.prefix_tensor(old["5"]["TRAIN"][PROFILES[0]][j]["views"]["normal"]) for j in ids])
        newx=torch.stack([wide.prefix_tensor(six["TRAIN"][PROFILES[0]][j]["views"]["normal"]) for j in ids])
        with torch.no_grad():
            z=model(oldx,torch.zeros(2,dtype=torch.int64)); new=model(newx,torch.zeros(2,dtype=torch.int64)); again=model(oldx,torch.zeros(2,dtype=torch.int64))
        c.p267.check_logits(new,2); require(torch.equal(z,again) and fp==c.base.fingerprint(model),"probe restoration")
    print("real_six_render_and_frozen_checkpoint_smoke = PASS; no retraining",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True
            and p["gate_f_candidate"] is False and p["production_adoption"] is False,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(724,1357) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(WIDE_SOURCE)==WIDE_BLOB,"result protection")
    require(len(p["artifacts"])==5 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"]; rr=s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rr]==identities() and all(type(r["six_pass"]) is bool for r in rr),"result cohort")
    require([r["five_pass"] for r in rr]==[r["quint_pass"] for r in expected_parent_flags()],"parent flags")
    counts={a:sum(r["six_pass"] for r in rr if r["arm"]==a) for a in ARMS}; gate=counts[PRIMARY_ARM]==5
    require(s["six_pass_counts"]==counts and s["primary_arm"]==PRIMARY_ARM and s["primary_gate"] is gate
            and p["status"]==("PASS" if gate else "FAIL"),"prospective six gate")
    require(s["all_replays"] is True and len(s["final_partitions"])==len(s["five_to_six"])==20 and len(s["reproductions"])==10,"coverage")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"work")


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==197,"parent modules")
    return names+["tests_lm.test_v05_c313_frozen_six_transfer"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==5030 and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED]; require(len(kept)==5029,"focused suite"); return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    parent,_,policy,wide,diag,c=context(); root=Path(__file__).resolve().parents[2]; guard(root,expected_head,c)
    pins,protected=precheck(summaries,root); _,data,old,anchors=load_parent(summaries); six=six_prompts(data)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    states=parent.load_bundle(Path(summaries[0]).resolve().parent/"trained-models.pt"); records=[]
    for i,seed in enumerate(SEEDS):
        models=parent.make_models(seed,policy,wide,c)
        for j,arm in enumerate(ARMS): records.append(infer_one(models[arm],states[2*i+j],anchors[2*i+j],data,old,six,wide,c))
    metrics,s=analyze(records,anchors,data,wide,diag,c)
    torch.save(dict(schema="fold-c313-six-transfer-eval-v1",records=records),out/"evaluations.pt")
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],six),(OUTPUTS[3],metrics),(OUTPUTS[4],s)): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c); precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if s["primary_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=s,gate_f_candidate=False,production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","artifacts")}; receipt["summary_sha256"]=c.audit.sha(out/"summary.json")
    print("=== C313 COMPACT EXPERIMENT RECEIPT ===",flush=True); print(json.dumps(receipt,sort_keys=True,indent=2),flush=True); return p


def verify_artifacts(outdir,summaries,expected_head):
    _,no_models,_,wide,diag,c=context(); out=Path(outdir); p=c.audit.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items(): require(c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"]); require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with no_models.no_neural():
        _,data,_,anchors=load_parent(summaries); archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c313-six-transfer-eval-v1","archive")
        metrics,s=analyze(archive["records"],anchors,data,wide,diag,c)
        for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],six_prompts(data)),(OUTPUTS[3],metrics),(OUTPUTS[4],s)):
            require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==s,"summary reconstruction"); return p,metrics


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--summaries",nargs=39,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True); parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
