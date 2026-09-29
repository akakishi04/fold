"""C279: saved C278 mean/final dual-query failure-profile attribution with zero neural execution."""
from __future__ import annotations
import argparse,hashlib,json,math,re,unittest
from collections import Counter,defaultdict
from pathlib import Path
from unittest.mock import patch
import torch

EXPERIMENT_ID="C279-v5b-saved-dual-failure-profile-audit"
STAGE="V5-B-SAVED-DUAL-FAILURE-PROFILE-AUDIT"
BASE="b3745f7d90565297cd4d19024d7da4fd62954251"
PARENT_EXECUTION="ca6e45cc90b3b48e3d56c10acde72e35574878fd"
PARENT_SHA="557069bec9d0d6ef73c7a9d1f5196f7be70edb9ab2c37a9a0d315033678b770b"
PARENT_ARTIFACTS={
    "architecture-plan.json":"791f287f21bcadd6c708496cd6922a2ef82a2ab94d2cf12ab5c3d669e1917dec",
    "dataset.json":"1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
    "triple-dataset.json":"432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",
    "trained-models.pt":"a86f34ed93dd8b3d0f2e46e960f134571223f2146b31763202b4f11b778f52d5",
    "evaluations.pt":"1ee106c701ee4ca6048c6bc9200bee343f57a7cfe88d2c201aa920ada8c2bfdc",
    "measurements.json":"ae12d78b16787622efc62206775a7ec7e9e021a8085b7c42a8bea8efbb90e24f",
    "validation-summary.json":"01a2dd82e73cfcc06feffa14b0edb5c5f2df7af0f0366f5b0cc3142e3862678c",
}
C277_SHA="ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13"
C276_SHA="6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f"
C275_SHA="1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb"
C274_SHA="0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0"
PARENT_IDENTITIES=[
    [278001,"mean_span"],[278001,"mean_final_dual"],
    [278002,"mean_span"],[278002,"mean_final_dual"],
    [278003,"mean_span"],[278003,"mean_final_dual"],
    [278004,"mean_span"],[278004,"mean_final_dual"],
    [278005,"mean_span"],[278005,"mean_final_dual"],
]
THRESHOLDS={"accuracy":.90,"query_pair_accuracy":.80,"evidence_drop":.35,"query_drop":.35,"two_order_accuracy":.80}
ARMS=("mean_span","mean_final_dual")
OWN=("fold_lm/v05_benchmarks/model_c279_saved_dual_failure_profile_audit.py",
     "tests_lm/test_v05_c279_saved_dual_failure_profile_audit.py",
     "tools/run_c279.ps1","tools/invoke_c279.ps1",
     "docs/experiment-ledger-addendum-c279-preregistration.md",
     "docs/v5b-saved-dual-failure-profile-audit-v0.1.md")
OUTPUTS=("audit-plan.json","failure-profile.json","validation-summary.json")
EXCLUDED="tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA="daeea4cfcf5083ec9a5237ea092f0c11ac7ab3cf38b76e9cdf62f60c4fea1af7"

def req(x,m):
    if not x: raise ValueError(m)
def blob(v): return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
def digest(v): return hashlib.sha256(blob(v)).hexdigest()
def context():
    from fold_lm.v05_benchmarks import model_c278_mean_final_dual_query as parent
    c277,c270,c269,p267,core,base,aligned,reader,factory,audit=parent.context()
    return parent,c277,c270,c269,p267,core,base,aligned,reader,factory,audit

def manifest():
    return dict(
        experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        c277_summary_sha256=C277_SHA,c276_summary_sha256=C276_SHA,
        c275_summary_sha256=C275_SHA,c274_summary_sha256=C274_SHA,
        parent_identities=PARENT_IDENTITIES,thresholds=THRESHOLDS,arms=list(ARMS),
        question="which fixed criteria remain responsible for mean_final_dual triple failures, especially shared_suffix2",
        formal_pass="saved diagnostic execution integrity only; no capability winner and no Gate F promotion",
        model_forward_calls=0,row_presentations=0,core_forward_calls=0,train_steps=0,
        new_checkpoint_writes=0,model_state_loads=0,network_calls=0,
        source_pins=520,protected_inputs=916,direct_dependencies=55,
        own_tests=24,modules=164,loaded_tests=3862,focused_tests=3861,excluded_test=EXCLUDED,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)

def signed_margin(value,threshold):
    req(type(value) in (int,float) and math.isfinite(value),"finite metric")
    return float(value-threshold)

def answer_record(seed,arm,task,cell):
    margins={
        "accuracy":signed_margin(cell["accuracy"],THRESHOLDS["accuracy"]),
        "query_pair_accuracy":signed_margin(cell["query_pair_accuracy"],THRESHOLDS["query_pair_accuracy"]),
        "evidence_drop":signed_margin(cell["evidence_drop"],THRESHOLDS["evidence_drop"]),
        "query_drop":signed_margin(cell["query_drop"],THRESHOLDS["query_drop"]),
    }
    failed=[k for k,v in margins.items() if v<0]
    req(cell["passed"] is (not failed),"answer-cell pass/margin mismatch")
    return dict(kind="answer_cell",seed=seed,arm=arm,task=task,split=cell["split"],profile=cell["profile"],
        language=cell["language"],entities=cell["entities"],permutation=cell["permutation"],
        rows=cell["rows"],correct=cell["correct"],pairs=cell["pairs"],collapsed_pairs=cell["collapsed_pairs"],
        accuracy=cell["accuracy"],query_pair_accuracy=cell["query_pair_accuracy"],
        evidence_drop=cell["evidence_drop"],query_drop=cell["query_drop"],
        margins=margins,failed_criteria=failed,passed=cell["passed"])

def two_order_record(seed,arm,task,item):
    margin=signed_margin(item["accuracy"],THRESHOLDS["two_order_accuracy"])
    passed=margin>=0
    req(item["passed"] is passed,"two-order pass/margin mismatch")
    return dict(kind="two_order",seed=seed,arm=arm,task=task,split=item["split"],profile=item["profile"],
        language=item["language"],entities=item["entities"],groups=item["groups"],both_correct=item["both_correct"],
        accuracy=item["accuracy"],margins={"two_order_accuracy":margin},
        failed_criteria=[] if passed else ["two_order_accuracy"],passed=item["passed"])

def aggregate(records):
    criterion=Counter();seed=Counter();profile=Counter();task=Counter();neg=defaultdict(list)
    for r in records:
        if not r["failed_criteria"]: continue
        task[(r["arm"],r["task"])]+=1
        for c in r["failed_criteria"]:
            criterion[(r["arm"],c)]+=1
            seed[(r["arm"],str(r["seed"]),c)]+=1
            profile[(r["arm"],r["task"],r["split"],r["profile"],c)]+=1
            neg[(r["arm"],c)].append(r["margins"][c])
    def flat(counter): return {"|".join(k):v for k,v in sorted(counter.items())}
    return dict(
        criterion_counts=flat(criterion),seed_criterion_counts=flat(seed),
        profile_criterion_counts=flat(profile),arm_task_failure_records=flat(task),
        negative_margin_range={"|".join(k):dict(min=min(v),max=max(v)) for k,v in sorted(neg.items())})

def deltas(records,selector):
    chosen=[r for r in records if selector(r)]
    counts={a:Counter() for a in ARMS}
    for r in chosen:
        for c in r["failed_criteria"]: counts[r["arm"]][c]+=1
    criteria=sorted(set(counts[ARMS[0]])|set(counts[ARMS[1]]))
    return dict(
        control=dict(sorted(counts[ARMS[0]].items())),
        candidate=dict(sorted(counts[ARMS[1]].items())),
        candidate_minus_control={c:counts[ARMS[1]][c]-counts[ARMS[0]][c] for c in criteria})

def audit_metrics(metrics):
    req(len(metrics)==10 and [[x["seed"],x["arm"]] for x in metrics]==PARENT_IDENTITIES,"parent metric identities")
    records=[];parent_passes=[]
    for m in metrics:
        seed,arm=m["seed"],m["arm"]
        parent_passes.append(dict(seed=seed,arm=arm,two_char=m["two_char"]["passed"],triple=m["triple"]["passed"],passed=m["passed"]))
        for task in ("two_char","triple"):
            tm=m[task];rebuilt=[]
            for cell in tm["cells"]:
                r=answer_record(seed,arm,task,cell);records.append(r);rebuilt.append(r["passed"])
            for item in tm["two_order"]:
                r=two_order_record(seed,arm,task,item);records.append(r);rebuilt.append(r["passed"])
            req(tm["passed"] is all(rebuilt),"task pass not equal to fixed records")
        req(m["passed"] is (m["two_char"]["passed"] and m["triple"]["passed"]),"whole pass mismatch")
    all_fail=[r for r in records if r["failed_criteria"]]
    triple=deltas(records,lambda r:r["task"]=="triple")
    prefix_hold=deltas(records,lambda r:r["task"]=="triple" and r["profile"]=="shared_prefix2" and r["split"]=="HOLDOUT")
    suffix_train=deltas(records,lambda r:r["task"]=="triple" and r["profile"]=="shared_suffix2" and r["split"]=="TRAIN")
    suffix_hold=deltas(records,lambda r:r["task"]=="triple" and r["profile"]=="shared_suffix2" and r["split"]=="HOLDOUT")
    per_seed={str(seed):deltas(records,lambda r,seed=seed:r["seed"]==seed and r["task"]=="triple")
              for seed in range(278001,278006)}
    audit=dict(
        thresholds=THRESHOLDS,parent_passes=parent_passes,total_fixed_records=len(records),
        total_failure_records=len(all_fail),failures=all_fail,aggregates=aggregate(records),
        primary=dict(triple_all=triple,shared_prefix2_holdout=prefix_hold,
            shared_suffix2_train=suffix_train,shared_suffix2_holdout=suffix_hold,
            per_seed_triple=per_seed))
    summary=dict(
        parent_records=10,fixed_records=len(records),failure_records=len(all_fail),
        parent_seed_pass_counts={a:sum(x["passed"] for x in parent_passes if x["arm"]==a) for a in ARMS},
        parent_two_char_pass_counts={a:sum(x["two_char"] for x in parent_passes if x["arm"]==a) for a in ARMS},
        parent_triple_pass_counts={a:sum(x["triple"] for x in parent_passes if x["arm"]==a) for a in ARMS},
        triple_criterion_delta=triple["candidate_minus_control"],
        shared_prefix2_holdout_delta=prefix_hold["candidate_minus_control"],
        shared_suffix2_train_delta=suffix_train["candidate_minus_control"],
        shared_suffix2_holdout_delta=suffix_hold["candidate_minus_control"],
        diagnostic_complete=True,capability_gate_applicable=False,
        model_forward_calls=0,row_presentations=0,core_forward_calls=0,train_steps=0,
        new_checkpoint_writes=0,model_state_loads=0)
    return audit,summary

def load_parent(c278_summary,c277_summary,c276_summary,c275_summary,c274_summary):
    parent,*rest=context();audit=rest[-1]
    p=Path(c278_summary).resolve();q=Path(c277_summary).resolve();r=Path(c276_summary).resolve()
    s=Path(c275_summary).resolve();t=Path(c274_summary).resolve()
    req(audit.sha(p)==PARENT_SHA and audit.sha(q)==C277_SHA and audit.sha(r)==C276_SHA
        and audit.sha(s)==C275_SHA and audit.sha(t)==C274_SHA,"parent hash")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C279 parent verification forbids model calls")):
        payload,metrics=parent.verify_artifacts(p.parent,q,r,s,t,PARENT_EXECUTION)
    parent.validate_result(payload)
    vs=payload["validation_summary"]
    req(payload["status"]=="FAIL" and vs["candidate_gate"] is False
        and vs["seed_pass_counts"]=={"mean_final_dual":0,"mean_span":0}
        and vs["two_char_pass_counts"]=={"mean_final_dual":5,"mean_span":5}
        and vs["triple_pass_counts"]=={"mean_final_dual":0,"mean_span":0},"C278 verdict")
    req({x["file"]:x["sha256"] for x in payload["artifacts"]}==PARENT_ARTIFACTS and len(metrics)==10,"parent artifacts")
    return payload,metrics

def precheck(c278_summary,c277_summary,c276_summary,c275_summary,c274_summary,root):
    parent,*rest=context();factory,audit=rest[-2],rest[-1];root=Path(root)
    p=Path(c278_summary).resolve()
    payload,_=load_parent(c278_summary,c277_summary,c276_summary,c275_summary,c274_summary)
    pins,protected=dict(payload["source_blobs"]),dict(payload["input_sha256"])
    for n,w in protected.items(): req(Path(n).is_file() and audit.sha(n)==w,"changed input:"+n)
    for n,w in pins.items(): req(audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==w,"changed source:"+n)
    for child,w in [(p,PARENT_SHA)]+[(audit.safe_child(p.parent,x["file"]),x["sha256"]) for x in payload["artifacts"]]:
        key=str(child.resolve());req(key not in protected and audit.sha(child)==w,"parent input identity");protected[key]=w
    for x in payload["artifacts"]: req(audit.safe_child(p.parent,x["file"]).stat().st_size==x["serialized_bytes"],"parent artifact size")
    for n in OWN:
        req(n not in pins,"OWN collision");pins[n]=audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9]|27[0-8])_[^/]+)\.py"
    deps=set(factory.LM_SOURCES)|{n for n in payload["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    req(len(deps)==55 and deps<=set(pins),"deps")
    protected.update(audit.protect_tree_files(root,pins))
    registration=manifest();expected=(registration["source_pins"],registration["protected_inputs"])
    actual=(len(pins),len(protected));actual_manifest=digest(registration)
    print(f"registration_check = source_pins:{actual[0]}; protected_inputs:{actual[1]}; manifest_sha256:{actual_manifest}",flush=True)
    req(actual==expected,f"registration counts expected={expected} actual={actual}")
    req(actual_manifest==MANIFEST_SHA,f"registration manifest expected={MANIFEST_SHA} actual={actual_manifest}")
    return pins,protected

def validate_result(p):
    req(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"identity")
    registration=manifest();expected=(registration["source_pins"],registration["protected_inputs"])
    req((len(p["source_blobs"]),len(p["input_sha256"]))==expected and set(OWN)<=set(p["source_blobs"]),"protection")
    req(len(p["artifacts"])==3 and {x["file"] for x in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"]
    req(s["parent_seed_pass_counts"]=={"mean_span":0,"mean_final_dual":0}
        and s["parent_two_char_pass_counts"]=={"mean_span":5,"mean_final_dual":5}
        and s["parent_triple_pass_counts"]=={"mean_span":0,"mean_final_dual":0},"parent pass counts")
    req(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False,"diagnostic")
    for k in ("model_forward_calls","row_presentations","core_forward_calls","train_steps","new_checkpoint_writes","model_state_loads"):
        req(s[k]==0,"zero workload:"+k)
    req(p["status"]=="PASS" and p["gate_f_candidate"] is False and p["production_adoption"] is False
        and p["capability_gate_applicable"] is False,"scope")

def flatten(s):
    for x in s:
        if isinstance(x,unittest.TestSuite): yield from flatten(x)
        else: yield x

def regression_modules(root):
    names=context()[0].regression_modules(root);req(len(names)==163,"modules")
    return names+["tests_lm.test_v05_c279_saved_dual_failure_profile_audit"]

def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    req(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"exclude")
    kept=[t for t in tests if t.id()!=EXCLUDED];req((len(tests),len(kept))==(3862,3861),"suite")
    return unittest.TestSuite(kept)

def run(*,c278_summary,c277_summary,c276_summary,c275_summary,c274_summary,output_dir,expected_head):
    root=Path(__file__).resolve().parents[2];audit=context()[-1]
    def guard():
        req(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head
            and audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repo")
    guard();pins,protected=precheck(c278_summary,c277_summary,c276_summary,c275_summary,c274_summary,root)
    _,metrics=load_parent(c278_summary,c277_summary,c276_summary,c275_summary,c274_summary)
    profile,summary=audit_metrics(metrics)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for n,v in (("audit-plan.json",manifest()),("failure-profile.json",profile),("validation-summary.json",summary)):
        (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard();precheck(c278_summary,c277_summary,c276_summary,c275_summary,c274_summary,root)
    payload=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
        validation_summary=summary,gate_f_candidate=False,production_adoption=False,
        capability_gate_applicable=False)
    validate_result(payload);(out/"summary.json").write_bytes(blob(payload))
    print("=== C279 RESULT ===",flush=True);print(blob(payload).decode(),flush=True);return payload

def verify_artifacts(outdir,c278_summary,c277_summary,c276_summary,c275_summary,c274_summary,expected_head):
    audit=context()[-1];out=Path(outdir)
    p=audit.read_json(out/"summary.json");validate_result(p);req(p["commit_sha"]==expected_head,"HEAD")
    for n,w in p["input_sha256"].items(): req(audit.sha(n)==w,"postcheck input")
    for x in p["artifacts"]:
        child=audit.safe_child(out,x["file"]);req(audit.sha(child)==x["sha256"] and child.stat().st_size==x["serialized_bytes"],"output bytes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C279 postcheck forbids model calls")):
        _,metrics=load_parent(c278_summary,c277_summary,c276_summary,c275_summary,c274_summary)
        profile,summary=audit_metrics(metrics)
        req(audit.read_json(out/"audit-plan.json")==manifest(),"persisted plan")
        req(audit.read_json(out/"failure-profile.json")==profile,"persisted failure profile")
        req(audit.read_json(out/"validation-summary.json")==summary,"persisted validation summary")
    req(p["validation_summary"]==summary,"summary")
    return p,profile

def main():
    p=argparse.ArgumentParser()
    for n in ("c278-summary","c277-summary","c276-summary","c275-summary","c274-summary","output-dir"):
        p.add_argument("--"+n,type=Path,required=True)
    p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))
if __name__=="__main__": main()
