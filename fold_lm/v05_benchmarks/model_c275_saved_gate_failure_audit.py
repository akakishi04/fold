"""C275: saved C274 gate-failure attribution with zero neural execution."""
from __future__ import annotations
import argparse,hashlib,json,math,re,unittest
from collections import Counter,defaultdict
from pathlib import Path
from unittest.mock import patch
import torch

EXPERIMENT_ID="C275-v5b-saved-gate-failure-audit"
STAGE="V5-B-SAVED-GATE-FAILURE-AUDIT"
BASE="ecd58ccf5f59887955048a6f23f77e340981e239"
PARENT_EXECUTION="90f76a8f017d562caded127821852654b8e3d061"
PARENT_SHA="0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0"
PARENT_ARTIFACTS={
    "architecture-plan.json":"a288c48c3b9282be070f12fdc567d8c8e09bbed8003a6321792ce517a5c255e7",
    "dataset.json":"1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
    "triple-dataset.json":"432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",
    "trained-models.pt":"3a8cf72756e1112341bf8ad88e45ad124f876a608586d3dc4955cd11a16c1231",
    "evaluations.pt":"ca1124810acd5f7d86ec614a900fbe5dbd3f37278005266616e666ce8e4ebf25",
    "measurements.json":"dcbddf4c4f614e8c8b224ecba4b656a5109e5dab0de1d4a2bde8ddae0858ecca",
    "validation-summary.json":"79d1ef4ee89f067977dd1704f4c0424453018dc5c989e3afe2d7f935cb5ef2f9",
}
PARENT_IDENTITIES=[
    [274001,"first_boundary"],[274001,"final_boundary"],
    [274002,"first_boundary"],[274002,"final_boundary"],
    [274003,"first_boundary"],[274003,"final_boundary"],
    [274004,"first_boundary"],[274004,"final_boundary"],
    [274005,"first_boundary"],[274005,"final_boundary"],
]
NEAR_SEEDS=(274001,274002,274004,274005)
BROAD_SEED=274003
THRESHOLDS={"accuracy":.90,"query_pair_accuracy":.80,"evidence_drop":.35,"query_drop":.35,"two_order_accuracy":.80}
OWN=("fold_lm/v05_benchmarks/model_c275_saved_gate_failure_audit.py",
     "tests_lm/test_v05_c275_saved_gate_failure_audit.py",
     "tools/run_c275.ps1","tools/invoke_c275.ps1",
     "docs/experiment-ledger-addendum-c275-preregistration.md",
     "docs/v5b-saved-gate-failure-audit-v0.1.md")
OUTPUTS=("audit-plan.json","failure-audit.json","validation-summary.json")
EXCLUDED="tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA="18af6d20c41fbb2e0bff672ac4e82e9e06eb324bc9c56ef53f409621ac95e102"

def req(x,m):
    if not x: raise ValueError(m)
def blob(v): return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
def digest(v): return hashlib.sha256(blob(v)).hexdigest()
def context():
    from fold_lm.v05_benchmarks import model_c274_directional_boundary_diagnostic as parent
    c273,c270,c269,p267,core,base,aligned,reader,factory,audit=parent.context()
    return parent,c270,c269,p267,core,base,aligned,reader,factory,audit

def manifest():
    return dict(
        experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        parent_identities=PARENT_IDENTITIES,near_seeds=list(NEAR_SEEDS),broad_seed=BROAD_SEED,
        thresholds=THRESHOLDS,
        question="which fixed gate components reject final_boundary triple states despite near-perfect pooled answers",
        formal_pass="saved diagnostic execution integrity only; no capability winner and no Gate F promotion",
        model_forward_calls=0,row_presentations=0,core_forward_calls=0,train_steps=0,
        new_checkpoint_writes=0,model_state_loads=0,network_calls=0,
        source_pins=496,protected_inputs=868,direct_dependencies=51,
        own_tests=24,modules=160,loaded_tests=3766,focused_tests=3765,excluded_test=EXCLUDED,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)

def signed_margin(value,threshold):
    req(type(value) in (int,float) and math.isfinite(value),"finite metric")
    return float(value-threshold)

def answer_failure(seed,arm,task,cell):
    margins={
        "accuracy":signed_margin(cell["accuracy"],THRESHOLDS["accuracy"]),
        "query_pair_accuracy":signed_margin(cell["query_pair_accuracy"],THRESHOLDS["query_pair_accuracy"]),
        "evidence_drop":signed_margin(cell["evidence_drop"],THRESHOLDS["evidence_drop"]),
        "query_drop":signed_margin(cell["query_drop"],THRESHOLDS["query_drop"]),
    }
    failed=[k for k,v in margins.items() if v<0]
    expected_pass=not failed
    req(cell["passed"] is expected_pass,"answer-cell pass/margin mismatch")
    return dict(kind="answer_cell",seed=seed,arm=arm,task=task,
        split=cell["split"],profile=cell["profile"],language=cell["language"],
        entities=cell["entities"],permutation=cell["permutation"],rows=cell["rows"],correct=cell["correct"],
        pairs=cell["pairs"],collapsed_pairs=cell["collapsed_pairs"],
        accuracy=cell["accuracy"],query_pair_accuracy=cell["query_pair_accuracy"],
        evidence_drop=cell["evidence_drop"],query_drop=cell["query_drop"],
        margins=margins,failed_criteria=failed,passed=cell["passed"])

def two_order_failure(seed,arm,task,item):
    margin=signed_margin(item["accuracy"],THRESHOLDS["two_order_accuracy"])
    expected_pass=margin>=0
    req(item["passed"] is expected_pass,"two-order pass/margin mismatch")
    return dict(kind="two_order",seed=seed,arm=arm,task=task,
        split=item["split"],profile=item["profile"],language=item["language"],entities=item["entities"],
        groups=item["groups"],both_correct=item["both_correct"],accuracy=item["accuracy"],
        margins={"two_order_accuracy":margin},failed_criteria=[] if expected_pass else ["two_order_accuracy"],
        passed=item["passed"])

def aggregate_failures(failures):
    criterion=Counter();seed_criterion=Counter();profile_criterion=Counter();arm_task=Counter()
    neg=defaultdict(list)
    for f in failures:
        arm_task[(f["arm"],f["task"])]+=1
        for c in f["failed_criteria"]:
            criterion[c]+=1
            seed_criterion[(str(f["seed"]),c)]+=1
            profile_criterion[(f["arm"],f["task"],f["split"],f["profile"],c)]+=1
            neg[c].append(f["margins"][c])
    return dict(
        criterion_counts=dict(sorted(criterion.items())),
        seed_criterion_counts={"|".join(k):v for k,v in sorted(seed_criterion.items())},
        profile_criterion_counts={"|".join(k):v for k,v in sorted(profile_criterion.items())},
        arm_task_failure_records={"|".join(k):v for k,v in sorted(arm_task.items())},
        negative_margin_range={k:dict(min=min(v),max=max(v)) for k,v in sorted(neg.items())})

def audit_metrics(metrics):
    req(len(metrics)==10 and [[x["seed"],x["arm"]] for x in metrics]==PARENT_IDENTITIES,"parent metric identities")
    all_records=[];failures=[];parent_passes=[]
    for m in metrics:
        seed,arm=m["seed"],m["arm"]
        parent_passes.append(dict(seed=seed,arm=arm,two_char=m["two_char"]["passed"],triple=m["triple"]["passed"]))
        for task in ("two_char","triple"):
            tm=m[task]
            req(set(("cells","two_order","totals","passed"))<=set(tm),"task metric schema")
            rebuilt=[]
            for cell in tm["cells"]:
                r=answer_failure(seed,arm,task,cell);all_records.append(r)
                if not r["passed"]:failures.append(r)
                rebuilt.append(r["passed"])
            for item in tm["two_order"]:
                r=two_order_failure(seed,arm,task,item);all_records.append(r)
                if not r["passed"]:failures.append(r)
                rebuilt.append(r["passed"])
            req(tm["passed"] is all(rebuilt),"task pass not equal to all fixed records")
    primary=[f for f in failures if f["arm"]=="final_boundary" and f["task"]=="triple"]
    coverage={seed:any(f["seed"]==seed for f in primary) for seed in (274001,274002,274003,274004,274005)}
    req(all(coverage.values()),"primary audit must cover every failing final triple seed")
    near=[f for f in primary if f["seed"] in NEAR_SEEDS]
    broad=[f for f in primary if f["seed"]==BROAD_SEED]
    req(near and broad,"near/broad cohorts both represented")
    audit=dict(
        thresholds=THRESHOLDS,
        parent_passes=parent_passes,
        total_fixed_records=len(all_records),
        total_failure_records=len(failures),
        failures=failures,
        aggregates=aggregate_failures(failures),
        primary_final_boundary_triple=dict(
            seed_failure_coverage={str(k):v for k,v in coverage.items()},
            failure_records=primary,
            near_seed_failure_records=near,
            broad_seed_failure_records=broad,
            near_seed_count=len(near),broad_seed_count=len(broad),
            aggregates=aggregate_failures(primary)))
    summary=dict(
        parent_records=10,fixed_records=len(all_records),failure_records=len(failures),
        primary_final_triple_failures=len(primary),
        primary_seed_coverage={str(k):v for k,v in coverage.items()},
        parent_task_pass_counts={
            arm:{
                "two_char":sum(x["two_char"] for x in parent_passes if x["arm"]==arm),
                "triple":sum(x["triple"] for x in parent_passes if x["arm"]==arm)
            } for arm in ("first_boundary","final_boundary")},
        diagnostic_complete=True,capability_gate_applicable=False,
        model_forward_calls=0,row_presentations=0,core_forward_calls=0,train_steps=0,
        new_checkpoint_writes=0,model_state_loads=0)
    return audit,summary

def load_parent(path):
    parent,*rest=context();audit=rest[-1];p=Path(path).resolve()
    req(audit.sha(p)==PARENT_SHA,"parent summary hash")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C275 parent verification forbids model calls")):
        payload,metrics=parent.verify_artifacts(p.parent,PARENT_EXECUTION)
    parent.validate_result(payload)
    req(payload["status"]=="PASS" and payload["validation_summary"]["diagnostic_complete"] is True
        and payload["validation_summary"]["capability_gate_applicable"] is False,"C274 diagnostic verdict")
    req(payload["validation_summary"]["task_pass_counts"]==
        {"final_boundary":{"triple":0,"two_char":4},"first_boundary":{"triple":0,"two_char":0}},"C274 pass counts")
    req({x["file"]:x["sha256"] for x in payload["artifacts"]}==PARENT_ARTIFACTS and len(metrics)==10,"parent artifacts")
    req(audit.read_json(p.parent/"measurements.json")==metrics,"parent measurements exact")
    return payload,metrics

def precheck(c274_summary,root):
    parent,*rest=context();factory,audit=rest[-2],rest[-1];root=Path(root);p=Path(c274_summary).resolve()
    payload,_=load_parent(p);pins,protected=dict(payload["source_blobs"]),dict(payload["input_sha256"])
    for n,w in protected.items():req(Path(n).is_file() and audit.sha(n)==w,"changed input:"+n)
    for n,w in pins.items():req(audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==w,"changed source:"+n)
    for child,w in [(p,PARENT_SHA)]+[(audit.safe_child(p.parent,x["file"]),x["sha256"]) for x in payload["artifacts"]]:
        key=str(child.resolve());req(key not in protected and audit.sha(child)==w,"parent input identity");protected[key]=w
    for x in payload["artifacts"]:req(audit.safe_child(p.parent,x["file"]).stat().st_size==x["serialized_bytes"],"parent artifact size")
    for n in OWN:
        req(n not in pins,"OWN collision");pins[n]=audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9]|27[0-4])_[^/]+)\.py"
    deps=set(factory.LM_SOURCES)|{n for n in payload["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    req(len(deps)==51 and deps<=set(pins),"deps")
    protected.update(audit.protect_tree_files(root,pins))
    registration=manifest();expected=(registration["source_pins"],registration["protected_inputs"])
    actual=(len(pins),len(protected));actual_manifest=digest(registration)
    print(f"registration_check = source_pins:{actual[0]}; protected_inputs:{actual[1]}; manifest_sha256:{actual_manifest}",flush=True)
    req(actual==expected,f"registration counts expected={expected} actual={actual}")
    req(MANIFEST_SHA!="PENDING_FINAL_SEAL","manifest not sealed")
    req(actual_manifest==MANIFEST_SHA,f"registration manifest expected={MANIFEST_SHA} actual={actual_manifest}")
    return pins,protected

def validate_result(p):
    req(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"identity")
    registration=manifest();expected=(registration["source_pins"],registration["protected_inputs"])
    req((len(p["source_blobs"]),len(p["input_sha256"]))==expected and set(OWN)<=set(p["source_blobs"]),"protection")
    req(len(p["artifacts"])==3 and {x["file"] for x in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"]
    req(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False,"diagnostic")
    req(s["parent_records"]==10 and all(s["primary_seed_coverage"].values()),"coverage")
    for k in ("model_forward_calls","row_presentations","core_forward_calls","train_steps","new_checkpoint_writes","model_state_loads"):
        req(s[k]==0,"zero workload:"+k)
    req(p["status"]=="PASS" and p["gate_f_candidate"] is False and p["production_adoption"] is False
        and p["capability_gate_applicable"] is False,"scope")

def flatten(s):
    for x in s:
        if isinstance(x,unittest.TestSuite):yield from flatten(x)
        else:yield x
def regression_modules(root):
    names=context()[0].regression_modules(root);req(len(names)==159,"modules")
    return names+["tests_lm.test_v05_c275_saved_gate_failure_audit"]
def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    req(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"exclude")
    kept=[t for t in tests if t.id()!=EXCLUDED];req((len(tests),len(kept))==(3766,3765),"suite")
    return unittest.TestSuite(kept)

def run(*,c274_summary,output_dir,expected_head):
    *_,audit=context();root=Path(__file__).resolve().parents[2]
    def guard():
        req(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head
            and audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repo")
    guard()
    pins,protected=precheck(c274_summary,root)
    _,metrics=load_parent(c274_summary)
    audit_result,summary=audit_metrics(metrics)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for n,v in (("audit-plan.json",manifest()),("failure-audit.json",audit_result),("validation-summary.json",summary)):
        (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard();precheck(c274_summary,root)
    for n,w in protected.items():req(audit.sha(n)==w,"modified input")
    payload=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
        validation_summary=summary,gate_f_candidate=False,production_adoption=False,
        capability_gate_applicable=False)
    validate_result(payload)
    (out/"summary.json").write_bytes(blob(payload))
    print("=== C275 RESULT ===",flush=True);print(blob(payload).decode(),flush=True)
    return payload

def verify_artifacts(outdir,c274_summary,expected_head):
    *_,audit=context();out=Path(outdir)
    p=audit.read_json(out/"summary.json");validate_result(p);req(p["commit_sha"]==expected_head,"HEAD")
    for n,w in p["input_sha256"].items():req(audit.sha(n)==w,"postcheck input")
    for x in p["artifacts"]:
        child=audit.safe_child(out,x["file"]);req(audit.sha(child)==x["sha256"] and child.stat().st_size==x["serialized_bytes"],"output bytes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C275 postcheck forbids model calls")):
        _,metrics=load_parent(c274_summary)
        audit_result,summary=audit_metrics(metrics)
        req(audit.read_json(out/"audit-plan.json")==manifest(),"persisted plan")
        req(audit.read_json(out/"failure-audit.json")==audit_result,"persisted failure audit")
        req(audit.read_json(out/"validation-summary.json")==summary,"persisted validation summary")
    req(p["validation_summary"]==summary,"summary")
    return p,audit_result

def main():
    p=argparse.ArgumentParser()
    for n in ("c274-summary","output-dir"):p.add_argument("--"+n,type=Path,required=True)
    p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))
if __name__=="__main__":main()
