"""C285: saved matched-cell length-transfer attribution; no neural execution."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import re
import unittest
from pathlib import Path
from unittest.mock import patch
import torch

EXPERIMENT_ID = "C285-v5b-saved-length-transfer-audit"
STAGE = "V5-B-SAVED-LENGTH-TRANSFER-AUDIT"
BASE = "8b16da05d3669e86ee6b9d323c6cb9eeec4766bf"
PARENT_EXECUTION = "3d34f6ba19017fd7d0422f070624ea7b1b494555"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c284_max_length_matched_training.py"
PARENT_BLOB = "cc560842a4f2b4e9b0ba6ae9481c42e2f3bb1df1"
SUMMARY_SHAS = (
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
    "architecture-plan.json": ("c835e2293c8a379b4173e4030cb687c0bb0bc549ef44298a0d8f8f39b2e6c080",4082),
    "dataset.json": ("1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",36024),
    "triple-dataset.json": ("432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",158236),
    "quad-dataset.json": ("86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b",172066),
    "trained-models.pt": ("4f4e23be2c803b1b15a3d5ead607fa16de30650031c49bf96e15857b0610c117",1238007),
    "evaluations.pt": ("d5469f156adbe1f03e5f255ce424062bbad3a021130f89b02abcd22c990a0e3f",159421903),
    "measurements.json": ("c7cc3f82a98d352ecef22b788c928c19704d8ca47335b8e3e7ed18011679636d",788207),
    "validation-summary.json": ("0e3e0914ba8bdd9d710a57fe7d99e7fdb2456df14e88d1752dd8fda5be220e28",38125),
}
SEEDS = tuple(range(284001,284006))
ARMS = ("three_char_only","mixed_length")
PROFILES = {"two_char":("doubled","shared_prefix","shared_suffix"),
            "triple":("tripled","shared_prefix2","shared_suffix2"),
            "quad":("quadrupled","shared_prefix3","shared_suffix3")}
THRESHOLDS = dict(accuracy=.90,query_pair_accuracy=.80,evidence_drop=.35,query_drop=.35,two_order_accuracy=.80)
OWN = ("fold_lm/v05_benchmarks/model_c285_saved_length_transfer_audit.py",
       "tests_lm/test_v05_c285_saved_length_transfer_audit.py","tools/run_c285.ps1","tools/invoke_c285.ps1",
       "docs/experiment-ledger-addendum-c285-preregistration.md","docs/v5b-saved-length-transfer-audit-v0.1.md")
OUTPUTS = ("audit-plan.json","cell-attribution.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
ZERO_KEYS = ("model_forward_calls","row_presentations","core_forward_calls","train_steps",
             "model_state_loads","new_checkpoint_writes","network_calls")
MANIFEST_SHA = "cef543afe98b94e09f62183c1175f4dca8727838aad6a40a341e1beef641286c"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def context():
    from fold_lm.v05_benchmarks import model_c284_max_length_matched_training as parent
    return parent,parent.context()[2]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
                parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,summary_sha256=list(SUMMARY_SHAS),
                parent_artifacts={k:list(v) for k,v in PARENT_ARTIFACTS.items()},seeds=list(SEEDS),arms=list(ARMS),
                profiles={k:list(v) for k,v in PROFILES.items()},thresholds=THRESHOLDS,
                question="which C284 quad criterion failures are new versus already failing matched triple cells, and how do arms differ",
                primary="all states; quad arm pairs and within-state triple-to-quad criterion transitions; no capability winner",
                limitation="matched-cell co-failure is not identical-row failure or causal inheritance; criteria overlap; no seed filtering",
                fixed_records=3240,quad_arm_pairs=540,longitudinal_pairs_per_arm=540,
                source_pins=556,protected_inputs=991,dependency_union=61,own_tests=32,
                modules=170,loaded_tests=4046,focused_tests=4045,excluded_test=EXCLUDED,
                capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,
                **dict.fromkeys(ZERO_KEYS,0))


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None,"manifest not sealed")
    require(digest(manifest())==MANIFEST_SHA,"manifest digest mismatch")


def identities(): return list(itertools.product(SEEDS,ARMS))


def expected_results():
    flags = ((1,1,1),(1,1,0),(0,0,0),(0,0,0),(0,1,1),(1,1,1),(1,1,0),(1,1,1),(1,1,0),(1,1,1))
    return [dict(seed=s,arm=a,two_char_pass=bool(f[0]),triple_pass=bool(f[1]),quad_pass=bool(f[2]),
                 passed=bool(f[2]),all_tasks_pass=all(f)) for (s,a),f in zip(identities(),flags,strict=True)]


def finite(value):
    require(type(value) in (int,float) and math.isfinite(value),"finite numeric metric")
    return float(value)


def integer(value,n):
    require(type(value) is int and 0<=value<=n,"integer count")
    return value


def ratio(value,n):
    value=finite(value); k=round(value*n)
    require(0<=k<=n and abs(value-k/n)<=1e-12,"discrete ratio")
    return k


def cell_key(r):
    return (r["kind"],r["split"],r["profile_index"],r["language"],tuple(r["entities"]),tuple(r.get("permutation",[])))


def expected_keys():
    out=set()
    for s,p,l,e in itertools.product(("TRAIN","HOLDOUT"),range(3),("en","ja"),((0,1),(0,2),(1,2))):
        out.add(("two_order",s,p,l,e,()))
        for perm in (e,e[::-1]): out.add(("answer_cell",s,p,l,e,perm))
    return out


def normalize(cell,kind,task,seed,arm):
    require(cell["profile"] in PROFILES[task],"unknown profile")
    r=dict(cell,kind=kind,task=task,seed=seed,arm=arm,profile_index=PROFILES[task].index(cell["profile"]))
    require(cell_key(r) in expected_keys(),"unknown cell key")
    n=16 if r["split"]=="TRAIN" else 8
    acc=finite(r["accuracy"])
    if kind=="answer_cell":
        require(type(r["rows"]) is int and r["rows"]==n and type(r["pairs"]) is int and r["pairs"]==n//2,"cell denominators")
        correct=integer(r["correct"],n); qp=ratio(r["query_pair_accuracy"],n//2)
        collapse=integer(r["collapsed_pairs"],n//2)
        require(abs(acc-correct/n)<=1e-12 and 2*qp<=correct and qp+collapse<=n//2,"cell counts")
        for view,drop in (("evidence_blind","evidence_drop"),("query_blind","query_drop")):
            r[view+"_correct"]=ratio(acc-finite(r[drop]),n)
        margins={k:finite(r[k])-v for k,v in THRESHOLDS.items() if k!="two_order_accuracy"}
    else:
        require(type(r["groups"]) is int and r["groups"]==n,"order denominator")
        require(abs(acc-integer(r["both_correct"],n)/n)<=1e-12,"order counts")
        margins={"two_order_accuracy":acc-THRESHOLDS["two_order_accuracy"]}
    failed=[k for k,v in margins.items() if v<0]
    require(type(r["passed"]) is bool and r["passed"] is (not failed),"cell pass flag")
    r.update(margins=margins,failed_criteria=failed)
    r["failure_class"]=("pass" if not failed else "two_order" if kind=="two_order" else
                        "answer_involving" if {"accuracy","query_pair_accuracy"}&set(failed) else "mask_only")
    return r


def transitions(pairs):
    criteria={}
    for criterion in THRESHOLDS:
        counts=dict.fromkeys(("both_pass","left_fail_right_pass","left_pass_right_fail","both_fail"),0)
        for left,right in pairs:
            require(cell_key(left)==cell_key(right),"paired cell mismatch")
            require(set(left["margins"])==set(right["margins"]),"paired criteria")
            if criterion not in left["margins"]: continue
            a=criterion in left["failed_criteria"];b=criterion in right["failed_criteria"]
            label="both_fail" if a and b else "left_fail_right_pass" if a else "left_pass_right_fail" if b else "both_pass"
            counts[label]+=1
        criteria[criterion]=dict(evaluable=sum(counts.values()),left_fail=counts["both_fail"]+counts["left_fail_right_pass"],
                                 right_fail=counts["both_fail"]+counts["left_pass_right_fail"],
                                 right_minus_left=counts["left_pass_right_fail"]-counts["left_fail_right_pass"],**counts)
    totals={}
    for i,name in enumerate(("left","right")):
        rows=[p[i] for p in pairs if p[i]["kind"]=="answer_cell"]
        totals[name]={k:sum(r[k] for r in rows) for k in ("rows","correct","pairs","collapsed_pairs","evidence_blind_correct","query_blind_correct")}
        totals[name]["mask_only_cells"]=sum(r["failure_class"]=="mask_only" for r in rows)
    return dict(paired_records=len(pairs),criteria=criteria,totals=totals)


def analyze(metrics):
    require([(m["seed"],m["arm"]) for m in metrics]==identities(),"model identities")
    records=[];results=[];index={}
    for m in metrics:
        flags={}
        for task in PROFILES:
            tm=m[task]
            rr=[normalize(r,kind,task,m["seed"],m["arm"]) for field,kind in (("cells","answer_cell"),("two_order","two_order")) for r in tm[field]]
            keys=[cell_key(r) for r in rr]
            require(len(keys)==len(set(keys)) and set(keys)==expected_keys(),"complete unique grid")
            good=all(r["passed"] for r in rr)
            require(type(tm["passed"]) is bool and tm["passed"] is good,"task pass flag")
            flags[task+"_pass"]=good
            for r in sorted(rr,key=cell_key):
                records.append(r);index[(m["seed"],m["arm"],task,cell_key(r))]=r
        results.append(dict(seed=m["seed"],arm=m["arm"],passed=flags["quad_pass"],all_tasks_pass=all(flags.values()),**flags))
    quad_pairs=[(r,index[(r["seed"],ARMS[1],"quad",cell_key(r))]) for r in records if r["task"]=="quad" and r["arm"]==ARMS[0]]
    longitudinal={a:[(r,index[(r["seed"],a,"quad",cell_key(r))]) for r in records if r["task"]=="triple" and r["arm"]==a] for a in ARMS}
    primary=dict(quad_between_arms=transitions(quad_pairs),triple_to_quad={a:transitions(p) for a,p in longitudinal.items()})
    per_seed={str(s):dict(quad_between_arms=transitions([p for p in quad_pairs if p[0]["seed"]==s]),
                         triple_to_quad={a:transitions([p for p in pp if p[0]["seed"]==s]) for a,pp in longitudinal.items()}) for s in SEEDS}
    profiles={f"{split}:{profile}":transitions([p for p in quad_pairs if p[0]["split"]==split and p[0]["profile_index"]==i])
              for split,i,profile in ((s,i,p) for s in ("TRAIN","HOLDOUT") for i,p in enumerate(PROFILES["quad"]))}
    summary=dict(parent_results=results,fixed_records=len(records),primary=primary,per_seed=per_seed,quad_profiles=profiles,
                 diagnostic_complete=True,capability_gate_applicable=False,**dict.fromkeys(ZERO_KEYS,0))
    report=dict(records=records,summary=summary,orientation="arm pairs:left=three_char_only,right=mixed_length; length pairs:left=triple,right=quad",
                warning="matched-cell transitions only; not rowwise or causal attribution; no seed exclusions")
    return report,summary


def validate_parent(payload):
    require(payload["commit_sha"]==PARENT_EXECUTION and payload["status"]=="FAIL","parent identity")
    require(payload["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent source pin")
    actual={a["file"]:(a["sha256"],a["serialized_bytes"]) for a in payload["artifacts"]}
    require(len(payload["artifacts"])==8 and actual==PARENT_ARTIFACTS,"parent artifacts")
    s=payload["validation_summary"]
    require(s["candidate_gate"] is False and s["all_replays"] is True and s["all_pairs_matched"] is True,"parent validity")
    require(s["seed_results"]==expected_results(),"parent seed gates")


def load_parent(paths):
    parent,c=context();paths=[Path(p).resolve() for p in paths]
    require(len(paths)==11 and all(c.audit.sha(p)==s for p,s in zip(paths,SUMMARY_SHAS,strict=True)),"parent summary hashes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C285 forbids neural calls")), \
         patch.object(torch.nn.Module,"load_state_dict",side_effect=RuntimeError("C285 forbids state loading")), \
         patch.object(torch,"save",side_effect=RuntimeError("C285 forbids checkpoint writes")):
        payload,metrics=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION)
    parent.validate_result(payload);validate_parent(payload)
    return payload,metrics


def precheck(paths,root):
    validate_seal();payload,_=load_parent(paths);_,c=context()
    root,p=Path(root),Path(paths[0]).resolve()
    pins,protected=dict(payload["source_blobs"]),dict(payload["input_sha256"])
    for n,w in pins.items(): require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==w,"changed source:"+n)
    for n,w in protected.items(): require(Path(n).is_file() and c.audit.sha(n)==w,"changed input:"+n)
    for child,w in [(p,SUMMARY_SHAS[0])]+[(c.audit.safe_child(p.parent,n),v[0]) for n,v in PARENT_ARTIFACTS.items()]:
        require(str(child.resolve()) not in protected and c.audit.sha(child)==w,"parent input")
        protected[str(child.resolve())]=w
    for n in OWN:
        require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9]|27[0-9]|28[0-4])_[^/]+)\.py"
    deps=set(c.factory.LM_SOURCES)|{n for n in payload["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps)==manifest()["dependency_union"] and deps<=set(pins),"dependency coverage")
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(manifest()["source_pins"],manifest()["protected_inputs"]),"registration counts")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS","result identity")
    require(p["diagnostic_execution_valid"] is True and all(p[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")),"scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(556,991) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"protection")
    require(len(p["artifacts"])==3 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"output set")
    s=p["validation_summary"]
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False,"diagnostic scope")
    require(s["fixed_records"]==3240 and s["parent_results"]==expected_results(),"accepted grids/results")
    require(s["primary"]["quad_between_arms"]["paired_records"]==540
            and all(s["primary"]["triple_to_quad"][a]["paired_records"]==540 for a in ARMS),"paired coverage")
    for k in ZERO_KEYS: require(type(s[k]) is int and s[k]==0,"zero workload:"+k)


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root)
    require(len(names)==len(set(names))==manifest()["modules"]-1,"parent modules")
    return names+["tests_lm.test_v05_c285_saved_length_transfer_audit"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==manifest()["loaded_tests"] and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED]
    require(len(kept)==manifest()["focused_tests"],"focused suite")
    return unittest.TestSuite(kept)


def guard(root,head):
    _,c=context()
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head
            and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    root=Path(__file__).resolve().parents[2];_,c=context();guard(root,expected_head)
    pins,protected=precheck(summaries,root);payload,metrics=load_parent(summaries)
    report,summary=analyze(metrics)
    require(summary["parent_results"]==payload["validation_summary"]["seed_results"],"parent reconstruction")
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for n,v in zip(OUTPUTS,(manifest(),report,summary),strict=True): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head);precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
           source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
           capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(p);(out/"summary.json").write_bytes(blob(p))
    print("=== C285 RESULT ===",flush=True);print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    _,c=context();out=Path(outdir);p=c.audit.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,w in p["input_sha256"].items(): require(c.audit.sha(n)==w,"protected input")
    for a in p["artifacts"]:
        child=c.audit.safe_child(out,a["file"])
        require(c.audit.sha(child)==a["sha256"] and child.stat().st_size==a["serialized_bytes"],"output bytes")
    _,metrics=load_parent(summaries);report,summary=analyze(metrics)
    for n,v in zip(OUTPUTS,(manifest(),report,summary),strict=True): require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==summary,"summary reconstruction")
    return p,report


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--summaries",nargs=11,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True);parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
