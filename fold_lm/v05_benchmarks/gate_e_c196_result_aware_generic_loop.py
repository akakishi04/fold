"""C196: result-aware generic-loop continuation under dynamic permission revocation.

Hold the frozen C181/C188 models, budget13 cohort, C172/C173 runtime and C194 generic-loop
semantics. Change exactly one orchestration rule: re-enter the loop after an acquisition
attempt only when the acquisition was actually admitted/published. Compare an ALLOWED arm
against accepted C194 and a PERMISSION_REVOKED_AFTER_DECISION arm where the trusted scheduler
revokes RETRIEVE permission after the learned decision but before the first acquisition.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, time
from dataclasses import asdict, replace
from pathlib import Path
import numpy as np
import torch

EXPERIMENT_ID="C196-v5e-result-aware-generic-loop"
STAGE="V5-E-RESULT-AWARE-GENERIC-LOOP"
BASE="988090c3d047eb1360dc06a7e3fb3956027124b3"
PARENT_EXECUTION="485d32b9dba0b0df34709d631a9d454629a1570e"
PARENT_SHA="614ffe9ee4794f102416bc5e51de1cd9510fde41ec4b43eb436377d9780a9b62"
REFERENCE_EXECUTION="32e62fe1b2e8318daa766aff1bfcc1f0fc49d95a"
REFERENCE_SHA="6cdb274da944bc87cea29f2e093d4acdec6035dae6978adaf469f1d9b4dfa084"
BASE_SEEDS=(181001,181002,181003)
HEAD_SEEDS=(188001,188002,188003)
ARM="INTERNAL_SEMANTICS"
ARMS=("ALLOWED","PERMISSION_REVOKED_AFTER_DECISION")
BATCH=1024
ATOL=1e-6
MAX_ACQUISITIONS=3
MAX_DECISIONS=4
PRIOR_NAMES=("c195","c194","c193","c192","c191","c190","c189","c188","c187","c186",
             "c185","c184","c183","c182","c181","c180","c179","c178","c177","c176","c174")
OWN=("fold_lm/v05_benchmarks/gate_e_c196_result_aware_generic_loop.py",
     "tests_lm/test_v05_c196_result_aware_generic_loop.py",
     "tools/run_c196.ps1","tools/invoke_c196.ps1",
     "docs/experiment-ledger-addendum-c196-preregistration.md")
EXPECTED_TESTS=1629
OUTPUTS={"result-aware-plan.json","allowed-replay.json","episode-results.json",
         "episode-traces.jsonl.gz","episode-predictions.npz"}

def require(ok,msg):
    if not ok: raise ValueError(msg)

def blob(v):
    return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()

def digest(v):
    return hashlib.sha256(blob(v)).hexdigest()

def load_c194_predictions(path):
    p=Path(path)
    require(p.is_file() and p.stat().st_size<10_000_000,"Unexpected C194 prediction artifact size")
    with np.load(p,allow_pickle=False) as z:
        expected={"necessity_predictions","necessity_logits","target_predictions","target_logits",
                  "row_indices","local_rows","world_codes"}
        require(set(z.files)==expected,"C194 prediction schema drift")
        out={k:z[k].copy() for k in z.files}
    require(out["necessity_predictions"].shape==(9,9536,4)
            and out["necessity_logits"].shape==(9,9536,4,2)
            and out["target_predictions"].shape==(9,9536,3)
            and out["target_logits"].shape==(9,9536,3,4)
            and out["row_indices"].shape==(9536,)
            and out["local_rows"].shape==(9536,)
            and out["world_codes"].shape==(9536,),
            "C194 prediction array drift")
    return out

def revoke_retrieve_permission(owner):
    """Trusted scheduler-only refresh after the learned decision, before action proposal."""
    view=owner.state.view
    r=view.resources
    require(r.permitted[0] is True,"RETRIEVE permission must start enabled")
    denied=replace(r,permitted=(False,*r.permitted[1:]))
    owner.refresh(replace(view,resources=denied))
    require(owner.state.view.resources.permitted[0] is False,
            "Permission revocation did not persist")

def admitted(acq):
    if not isinstance(acq,dict):
        return False
    action=acq.get("action");dispatch=acq.get("dispatch")
    return bool(isinstance(action,dict) and isinstance(dispatch,dict)
        and action.get("status")=="PENDING"
        and action.get("reason")=="ACQUISITION_RESERVED"
        and action.get("acquisition_reserved")==1
        and dispatch.get("status")=="PUBLISHED"
        and dispatch.get("reason")=="OBSERVATION_ADMITTED"
        and dispatch.get("provider_calls")==1
        and dispatch.get("fact_publications")==1)

def run_loop_result_aware(views,world_codes,endpoints,base,selector,initial,arm):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05 import structured_action_runtime as action
    from fold_lm.v05 import structured_task_input as task
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190

    require(arm in ARMS,"Unregistered C196 arm")
    require(len(views)==len(world_codes)>0,"Episode/world alignment required")
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{"RETRIEVE":endpoints[int(code)]},
                                  max_dispatches=MAX_ACQUISITIONS)
            for v,code in zip(views,world_codes,strict=True)]
    n=len(views)
    records=[dict(initial=asdict(task.encode(v)),phases=[],acquisitions=[],
                  decision_charges=0,status="UNRESOLVED",world_code=int(code),arm=arm)
             for v,code in zip(views,world_codes,strict=True)]
    n_pred=np.full((n,MAX_DECISIONS),-1,dtype=np.int8)
    n_logits=np.zeros((n,MAX_DECISIONS,2),dtype=np.float32)
    t_pred=np.full((n,MAX_ACQUISITIONS),-1,dtype=np.int8)
    t_logits=np.full((n,MAX_ACQUISITIONS,4),-np.inf,dtype=np.float32)
    meter=dict(rows=0,forward_calls=0,cell_calls=0)

    active=list(range(n));iteration=0
    while active:
        require(iteration<MAX_DECISIONS,"Result-aware loop exceeded derived decision bound")
        charged=[];exhausted=[]
        for i in active:
            if driver.charge_decision(owners[i]): charged.append(i)
            else: exhausted.append(i)
        for i in exhausted: records[i]["status"]="BUDGET_EXHAUSTED"
        active=charged
        if not active: break

        raw,packets=c189.encode_views([owners[i].state.view for i in active])
        any_missing=any(any(f.status=="UNOBSERVED" for f in owners[i].state.view.facts)
                        for i in active)
        if iteration==0:
            require(torch.equal(raw,initial["raw"]),"Initial cache mapping drift")
            p=np.asarray(initial["necessity_predictions"])
            z=np.asarray(initial["necessity_logits"])
            if any_missing:
                t=np.asarray(initial["target_predictions"])
                tz=np.asarray(initial["target_logits"])
            else:
                t=np.full(len(active),-1,dtype=np.int8)
                tz=np.full((len(active),4),-np.inf,dtype=np.float32)
        elif any_missing:
            p,t,z,tz,m=c189.combined_predict(base,selector,raw,batch=BATCH)
            for k in meter:meter[k]+=m[k]
        else:
            p,z,m=c189.necessity_predict(base,raw,batch=BATCH)
            for k in meter:meter[k]+=m[k]
            t=np.full(len(active),-1,dtype=np.int8)
            tz=np.full((len(active),4),-np.inf,dtype=np.float32)

        next_active=[]
        for j,i in enumerate(active):
            n_pred[i,iteration]=p[j];n_logits[i,iteration]=z[j]
            phase=dict(iteration=iteration,packet=asdict(packets[j]),
                       necessity_prediction=int(p[j]))
            records[i]["decision_charges"]+=1
            if any_missing:
                require(iteration<MAX_ACQUISITIONS,
                        "Target-bearing decision exceeded acquisition-derived bound")
                t_pred[i,iteration]=t[j];t_logits[i,iteration]=tz[j]
                phase["target_prediction"]=int(t[j])
            records[i]["phases"].append(phase)

            if int(p[j])==0:
                records[i]["status"]="SUFFICIENT_CLASSIFICATION"
                continue

            view=owners[i].state.view
            if not any(f.status=="UNOBSERVED" for f in view.facts):
                records[i]["status"]="UNRESOLVED_NEEDS_NO_TARGET"
                continue
            target_index=int(t[j])
            if not (0<=target_index<4) or view.facts[target_index].status!="UNOBSERVED":
                records[i]["status"]="UNRESOLVED_INVALID_TARGET"
                continue

            if arm=="PERMISSION_REVOKED_AFTER_DECISION":
                require(iteration==0,"Denied arm must terminate before a second learned decision")
                revoke_retrieve_permission(owners[i])

            acq=c190.acquire(owners[i],target_index)
            records[i]["acquisitions"].append(acq)
            if admitted(acq):
                next_active.append(i)
            else:
                reason=acq["action"]["reason"] if isinstance(acq.get("action"),dict) else "UNKNOWN"
                records[i]["status"]="UNRESOLVED_ACQUISITION_"+reason

        active=next_active
        iteration+=1

    for i,o in enumerate(owners):
        records[i]["final"]=asdict(task.encode(o.state.view))
        records[i]["receipts"]=[asdict(r) for r in o.receipts]
        records[i]["pending"]=asdict(o.state.pending) if o.state.pending else None
        records[i]["runtime_terminal"]=o.state.terminal
    return records,dict(necessity_predictions=n_pred,necessity_logits=n_logits,
                        target_predictions=t_pred,target_logits=t_logits),meter

def replay_metrics(arrays,reference):
    nerr=int((arrays["necessity_predictions"]!=reference["necessity_predictions"]).sum())
    terr=int((arrays["target_predictions"]!=reference["target_predictions"]).sum())
    nmask=reference["necessity_predictions"]>=0
    tmask=reference["target_predictions"]>=0
    nd=float(np.max(np.abs(arrays["necessity_logits"][nmask]
                           -reference["necessity_logits"][nmask]))) if nmask.any() else 0.0
    finite=np.isfinite(reference["target_logits"]) & np.repeat(tmask[:,:,None],4,axis=2)
    td=float(np.max(np.abs(arrays["target_logits"][finite]
                           -reference["target_logits"][finite]))) if finite.any() else 0.0
    return dict(necessity_prediction_errors=nerr,target_prediction_errors=terr,
                necessity_max_abs_logit_difference=nd,target_max_abs_logit_difference=td)

ALLOWED_COUNTERS=("failed","necessity_error","target_error","selected_observed","repeated_target",
                  "acquisition_error","contract_error","final_decision_error",
                  "reference_replay_error","reference_block_mismatch")
DENIED_COUNTERS=("failed","initial_prediction_error","denied_attempt_error","status_error",
                 "provider_call_error","publication_error","receipt_error","retry_error",
                 "resource_error","fact_mutation_error","fake_sufficient_error")

def score_denied(record,ref_initial_n,ref_initial_t,initial_features):
    ph=record["phases"];acq=record["acquisitions"];final=record["final"]
    initial_prediction_error=int(not (
        len(ph)==1
        and ph[0]["necessity_prediction"]==int(ref_initial_n)
        and ph[0].get("target_prediction")==int(ref_initial_t)))
    a=acq[0] if len(acq)==1 else None
    action=a["action"] if isinstance(a,dict) else None
    dispatch=a["dispatch"] if isinstance(a,dict) else None
    denied_attempt_error=int(not (
        isinstance(action,dict)
        and action["status"]=="DENIED"
        and action["reason"]=="PERMISSION_DENIED"
        and action["internal_charged"]==1
        and action["acquisition_reserved"]==0
        and dispatch is None))
    status_error=int(record["status"]!="UNRESOLVED_ACQUISITION_PERMISSION_DENIED")
    provider_call_error=int(dispatch is not None and dispatch.get("provider_calls",0)!=0)
    publication_error=int(dispatch is not None and dispatch.get("fact_publications",0)!=0)
    receipt_error=int(len(record["receipts"])!=0)
    retry_error=int(len(ph)!=1 or len(acq)!=1 or record["decision_charges"]!=1)
    f=np.asarray(final["features"],dtype=np.int64)
    resource_error=int(not (
        f[62]==11 and f[63]==4 and f[67]==0 and f[70]==2 and f[71]==9
        and record["pending"] is None and record["runtime_terminal"] is None))
    x=np.asarray(initial_features,dtype=np.int64)
    fact_mutation_error=int(any(f[46:62]!=x[46:62]))
    fake_sufficient_error=int(record["status"]=="SUFFICIENT_CLASSIFICATION")
    vals=(initial_prediction_error,denied_attempt_error,status_error,provider_call_error,
          publication_error,receipt_error,retry_error,resource_error,fact_mutation_error,
          fake_sufficient_error)
    return dict(failed=int(any(vals)),initial_prediction_error=initial_prediction_error,
        denied_attempt_error=denied_attempt_error,status_error=status_error,
        provider_call_error=provider_call_error,publication_error=publication_error,
        receipt_error=receipt_error,retry_error=retry_error,resource_error=resource_error,
        fact_mutation_error=fact_mutation_error,fake_sufficient_error=fake_sufficient_error)

def expected_order():
    return [(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS]

def gate(allowed,denied):
    if [(r.get("base_seed"),r.get("head_seed")) for r in allowed]!=expected_order():return False
    if [(r.get("base_seed"),r.get("head_seed")) for r in denied]!=expected_order():return False
    for r in allowed:
        if r.get("episodes")!=9536:return False
        if any(r.get(k)!=0 for k in ALLOWED_COUNTERS):return False
        if r.get("first_reads")!=9536 or r.get("third_reads")!=r.get("final_decision_rows"):return False
        if r.get("actual_reads")!=r["first_reads"]+r["second_reads"]+r["third_reads"]:return False
        if r.get("reference_necessity_prediction_errors")!=0 or r.get("reference_target_prediction_errors")!=0:return False
        if r.get("reference_necessity_max_abs_logit_difference",1)>ATOL:return False
        if r.get("reference_target_max_abs_logit_difference",1)>ATOL:return False
    for r in denied:
        if r.get("episodes")!=9536:return False
        if any(r.get(k)!=0 for k in DENIED_COUNTERS):return False
        if r.get("denied_attempts")!=9536 or r.get("actual_reads")!=0:return False
        if r.get("provider_calls")!=0 or r.get("publications")!=0 or r.get("receipts")!=0:return False
        if r.get("learned_decisions")!=9536 or r.get("retries")!=0:return False
        if r.get("initial_reference_prediction_errors")!=0:return False
        if r.get("initial_reference_target_errors")!=0:return False
        if r.get("initial_reference_necessity_logit_delta",1)>ATOL:return False
        if r.get("initial_reference_target_logit_delta",1)>ATOL:return False
    return True

def manifest():
    return dict(
      experiment_id=EXPERIMENT_ID,stage=STAGE,parent_sha256=PARENT_SHA,
      acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
      reference_execution=REFERENCE_EXECUTION,reference_sha256=REFERENCE_SHA,
      base_seeds=BASE_SEEDS,head_seeds=HEAD_SEEDS,arms=ARMS,arm=ARM,
      question="can one result-aware continuation rule preserve accepted C194 behavior and safely stop after a permission-denied acquisition when authority is revoked after the learned decision",
      changed="after acquisition attempt, re-enter loop only on actual OBSERVATION_ADMITTED publication; otherwise terminate unresolved",
      denial_intervention="trusted scheduler revokes RETRIEVE permission true->false after iteration0 learned decision and before acquisition proposal; model decision packet remains allowed-state packet",
      held="budget13,C174 cohort,9 frozen C181/C188 pairs,16 coherent worlds,C172/C173,teachers,max_dispatches3,raw argmax",
      allowed_arm="full9536 worlds/selector; exact C194 prediction/logit/read-depth replay required",
      denied_arm="full9536 worlds/selector; exactly one DENIED/PERMISSION_DENIED action,zero dispatch/provider/publication/receipt/retry,final resources11/4/permission0/outcomePERMISSION_DENIED/step9",
      episodes_per_arm=85824,blocks_per_arm=9,
      gate="all9 allowed blocks exact C194 replay and zero scientific errors; all9 denied blocks9536 safe denials with no retry/IO/evidence/fake-sufficient and exact resources",
      training=0,fresh_seeds=0,network_calls=0,answer_generation=0,proof_checker_calls=0,core_evidence_writes=0,
      production_runtime_modified=False,gate_e_candidate=False,outputs=sorted(OUTPUTS),
      limits="development family;only first-acquisition permission revocation tested;no provider failure/stale/attempt-limit/resource-policy/tool-choice/holdout/language/answer/proof/GateE")
MANIFEST_SHA="cbbbcdac61d729e6c73a86d6e3c70ed74189db33bb4c9c2ea557becb630a2457"

def precheck(c195_summary,*args):
    from fold_lm.v05_benchmarks import gate_e_c195_generic_loop_budget12_exhaustion as parent
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(len(args)==21,"Twenty prior summaries and repository root required")
    root=args[-1]
    p194,p191ref,p193,p192,p191,p190,p189,p188,p181,p174,pins,protected=parent.precheck(
        args[0],*args[1:])
    require(audit.sha(c195_summary)==PARENT_SHA,"C195 summary changed")
    p195=audit.read_json(c195_summary);parent.validate_result(p195)
    require(p195["commit_sha"]==PARENT_EXECUTION and p195["status"]=="PASS"
            and parent.gate(p195["records"]) and p195["source_blobs"]==pins,
            "Wrong accepted C195 source/result")
    require(audit.sha(args[0])==REFERENCE_SHA,"C194 reference summary changed")
    require(p194["commit_sha"]==REFERENCE_EXECUTION and p194["status"]=="PASS",
            "Wrong accepted C194 reference")

    protected[str(Path(c195_summary).resolve())]=PARENT_SHA
    for a in p195["artifacts"]:
        f=audit.safe_child(Path(c195_summary).resolve().parent,a["file"])
        require(f.is_file() and f.stat().st_size==a["serialized_bytes"] and audit.sha(f)==a["sha256"],
                "Changed C195 artifact:"+a["file"])
        protected[str(f.resolve())]=a["sha256"]

    pins=dict(pins)
    for name in parent.OWN:
        pins[name]=audit.git(root,"rev-parse",PARENT_EXECUTION+":"+name).decode().strip()
    allpins=dict(pins)
    for name in OWN:allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins)==141 and len(protected)==374,"Source/protected union drift")
    require(digest(manifest())==MANIFEST_SHA,"Manifest drift")
    return p195,p194,p193,p192,p191,p190,p189,p188,p181,p174,pins,protected

def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c195_generic_loop_budget12_exhaustion as parent
    names=parent.regression_modules(root)
    require(len(names)==len(set(names))==80,"Historical regression list drift")
    return names+["tests_lm.test_v05_c196_result_aware_generic_loop"]

def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE
            and p["diagnostic_execution_valid"] is True,"Wrong/incomplete C196")
    require(p["episodes_per_arm"]==85824
            and len(p["allowed_records"])==len(p["denied_records"])==9
            and len(p["source_blobs"])==141 and len(p["input_sha256"])==374
            and len(p["artifacts"])==5 and {a["file"] for a in p["artifacts"]}==OUTPUTS,
            "Workload/coverage drift")
    require(all(p[k]==0 for k in ("new_training","fresh_seeds","network_calls",
                                  "answer_generation","proof_checker_calls","core_evidence_writes"))
            and p["production_runtime_modified"] is False and p["gate_e_candidate"] is False,
            "Scope drift")
    require(p["status"]==("PASS" if gate(p["allowed_records"],p["denied_records"]) else "FAIL"),
            "Gate drift")

def run(*,output_dir,expected_head,**parents):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
    from fold_lm.v05_benchmarks import gate_e_c193_budget13_authoritative_closure as c193

    root=Path(__file__).resolve().parents[2]
    args=tuple(parents[n+"_summary"] for n in PRIOR_NAMES[1:])+(root,)
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"Dirty tracked tree")
    guard()
    p195,p194,p193,p192,p191,p190,p189,p188,p181,p174,pins,protected=precheck(
        parents["c195_summary"],*args)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    artifacts=[];allowed_records=[];denied_records=[];started=time.perf_counter()
    def record_file(name):
        f=out/name;artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,v):
        (out/name).write_bytes(blob(v));record_file(name)
    save("result-aware-plan.json",dict(manifest(),source_blobs=pins))
    try:
        print("[C196] plan fixed; result-aware continuation; ALLOWED exact C194 replay + post-decision permission revocation",flush=True)
        torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
        data,metadata=audit.load_data(Path(parents["c174_summary"]).resolve().parent,p174)
        raw_all=torch.from_numpy(data["features"].copy())
        valid=c189.target_teacher(data["features"],data["template_ids"],metadata)
        _,_,evfull,_,_=target.cohort_masks(raw_all,data["labels"],data["split_codes"],valid)
        full_ix=np.flatnonzero(evfull)
        raw12=torch.from_numpy(data["features"][evfull].copy())
        raw13=c193.budget13(raw12)
        _,source_rows,local_rows,world_codes=c190.expand_worlds(raw12,full_ix)
        expanded13=c193.budget13(c190.expand_worlds(raw12,full_ix)[0])
        tids=data["template_ids"][evfull]

        ref_dir=Path(parents["c194_summary"]).resolve().parent
        saved=load_c194_predictions(ref_dir/"episode-predictions.npz")
        require(np.array_equal(saved["row_indices"],source_rows)
                and np.array_equal(saved["local_rows"],local_rows)
                and np.array_equal(saved["world_codes"],world_codes),
                "C194 episode identity drift")

        c181_dir=Path(parents["c181_summary"]).resolve().parent
        c188_dir=Path(parents["c188_summary"]).resolve().parent
        fits={f["seed"]:f for f in p181["fit_records"] if f["arm"]==ARM}
        selector_sha={(r["base_seed"],r["head_seed"]):r["head_sha256"] for r in p188["selector_results"]}
        bases={};heads={}
        for b in BASE_SEEDS:
            bases[b]=frozen.restore_bare(c181_dir/f"probe-{b}-{ARM}.pt",b,ARM,fits[b]["final_sha256"])
            for h in HEAD_SEEDS:
                heads[b,h]=c189.restore_selector(c188_dir/f"selector-{b}-{h}.pt",b,h,selector_sha[b,h])

        source_dir=Path(parents["c191_summary"]).resolve().parent/"sources"
        providers={};endpoints={}
        for code in range(16):
            f=source_dir/f"world-{code:02d}.json"
            expected=c190.SOURCE_FILES[f"sources/world-{code:02d}.json"]
            require(f.is_file() and audit.sha(f)==expected,"Changed protected coherent world source")
            sb=life.SourceBinding(f"C190-world-{code:02d}",expected)
            provider=life.FileSnapshotProvider(f,sb)
            providers[code]=provider;endpoints[code]=life.Endpoint(sb,provider)

        dense_n=np.full((2,9,9536,4),-1,dtype=np.int8)
        dense_z=np.zeros((2,9,9536,4,2),dtype=np.float32)
        dense_t=np.full((2,9,9536,3),-1,dtype=np.int8)
        dense_tz=np.full((2,9,9536,3,4),-np.inf,dtype=np.float32)
        allowed_replay=[]
        with gzip.open(out/"episode-traces.jsonl.gz","wt",encoding="utf-8",newline="\n") as trace:
            for bi,b in enumerate(BASE_SEEDS):
                for hi,h in enumerate(HEAD_SEEDS):
                    idx=bi*3+hi
                    cache,_=c193.initial_policy_cache(raw13,full_ix,bases[b],heads[b,h])
                    lt=torch.from_numpy(local_rows.astype(np.int64))
                    initial=dict(raw=cache["raw"][lt],
                        necessity_predictions=cache["necessity_predictions"][local_rows],
                        target_predictions=cache["target_predictions"][local_rows],
                        necessity_logits=cache["necessity_logits"][local_rows],
                        target_logits=cache["target_logits"][local_rows])
                    reference={k:saved[k][idx] for k in (
                        "necessity_predictions","necessity_logits","target_predictions","target_logits")}

                    for arm_i,arm in enumerate(ARMS):
                        before_reads=sum(p.reads for p in providers.values())
                        before_bytes=sum(p.bytes_read for p in providers.values())
                        views=c190.make_views(expanded13,source_rows,world_codes,
                                             f"C196-{arm}-b{b}-h{h}")
                        observed,arrays,_=run_loop_result_aware(
                            views,world_codes,endpoints,bases[b],heads[b,h],initial,arm)
                        dense_n[arm_i,idx]=arrays["necessity_predictions"]
                        dense_z[arm_i,idx]=arrays["necessity_logits"]
                        dense_t[arm_i,idx]=arrays["target_predictions"]
                        dense_tz[arm_i,idx]=arrays["target_logits"]
                        reads=sum(p.reads for p in providers.values())-before_reads
                        bytes_read=sum(p.bytes_read for p in providers.values())-before_bytes

                        if arm=="ALLOWED":
                            replay=replay_metrics(arrays,reference)
                            allowed_replay.append(dict(base_seed=b,head_seed=h,**replay))
                            replay_error=int(replay["necessity_prediction_errors"]!=0
                                or replay["target_prediction_errors"]!=0
                                or replay["necessity_max_abs_logit_difference"]>ATOL
                                or replay["target_max_abs_logit_difference"]>ATOL)
                            scores=[]
                            for j,rec in enumerate(observed):
                                s=c193.assess(rec,int(tids[int(local_rows[j])]),metadata,
                                              c190.WORLD_BITS[int(world_codes[j])])
                                s["reference_replay_error"]=replay_error
                                s["reference_block_mismatch"]=0
                                s["failed"]=int(s["failed"] or replay_error)
                                scores.append(s)
                            totals={k:sum(s[k] for s in scores) for k in c193.COUNTERS}
                            ref_rec=p194["records"][idx]
                            block_mismatch=int(any((
                                totals["first_reads"]!=ref_rec["first_reads"],
                                totals["second_reads"]!=ref_rec["second_reads"],
                                totals["third_reads"]!=ref_rec["third_reads"],
                                totals["final_decision_rows"]!=ref_rec["final_decision_rows"],
                                reads!=ref_rec["actual_reads"])))
                            if block_mismatch:
                                for s in scores:s["reference_block_mismatch"]=1;s["failed"]=1
                            rec=dict(base_seed=b,head_seed=h,episodes=9536,actual_reads=reads,
                                bytes_read=bytes_read,
                                reference_necessity_prediction_errors=replay["necessity_prediction_errors"],
                                reference_target_prediction_errors=replay["target_prediction_errors"],
                                reference_necessity_max_abs_logit_difference=replay["necessity_max_abs_logit_difference"],
                                reference_target_max_abs_logit_difference=replay["target_max_abs_logit_difference"],
                                reference_replay_error=int(replay_error*9536),
                                reference_block_mismatch=int(block_mismatch*9536),
                                **totals)
                            allowed_records.append(rec)
                        else:
                            ref_n=reference["necessity_predictions"][:,0]
                            ref_t=reference["target_predictions"][:,0]
                            initial_nerr=int((arrays["necessity_predictions"][:,0]!=ref_n).sum())
                            initial_terr=int((arrays["target_predictions"][:,0]!=ref_t).sum())
                            nmask=ref_n>=0;tmask=ref_t>=0
                            nd=float(np.max(np.abs(arrays["necessity_logits"][nmask,0]
                                -reference["necessity_logits"][nmask,0]))) if nmask.any() else 0.0
                            finite=np.isfinite(reference["target_logits"][:,0,:]) & tmask[:,None]
                            td=float(np.max(np.abs(arrays["target_logits"][:,0,:][finite]
                                -reference["target_logits"][:,0,:][finite]))) if finite.any() else 0.0
                            scores=[score_denied(rec,ref_n[j],ref_t[j],
                                rec["initial"]["features"]) for j,rec in enumerate(observed)]
                            totals={k:sum(s[k] for s in scores) for k in DENIED_COUNTERS}
                            attempts=sum(len(rec["acquisitions"]) for rec in observed)
                            provider_calls=sum((a["dispatch"] or {}).get("provider_calls",0)
                                for rec in observed for a in rec["acquisitions"])
                            publications=sum((a["dispatch"] or {}).get("fact_publications",0)
                                for rec in observed for a in rec["acquisitions"])
                            receipts=sum(len(rec["receipts"]) for rec in observed)
                            decisions=sum(rec["decision_charges"] for rec in observed)
                            retries=sum(max(0,len(rec["phases"])-1) for rec in observed)
                            rec=dict(base_seed=b,head_seed=h,episodes=9536,actual_reads=reads,
                                bytes_read=bytes_read,denied_attempts=attempts,
                                provider_calls=provider_calls,publications=publications,
                                receipts=receipts,learned_decisions=decisions,retries=retries,
                                initial_reference_prediction_errors=initial_nerr,
                                initial_reference_target_errors=initial_terr,
                                initial_reference_necessity_logit_delta=nd,
                                initial_reference_target_logit_delta=td,**totals)
                            denied_records.append(rec)

                        for j,rec0 in enumerate(observed):
                            score=(scores[j] if arm=="PERMISSION_REVOKED_AFTER_DECISION"
                                   else scores[j])
                            trace.write(json.dumps(dict(arm=arm,base_seed=b,head_seed=h,
                                source_row=int(source_rows[j]),world_code=int(world_codes[j]),
                                score=score,trace=rec0),
                                sort_keys=True,separators=(",",":"),allow_nan=False)+"\n")

                        print(f"[C196] arm={arm} block={idx+1}/9 base={b} head={h} "
                              f"reads={reads} failed={rec['failed']} ",flush=True)

        record_file("episode-traces.jsonl.gz")
        np.savez_compressed(out/"episode-predictions.npz",
            necessity_predictions=dense_n,necessity_logits=dense_z,
            target_predictions=dense_t,target_logits=dense_tz,
            row_indices=source_rows.astype("<i4"),local_rows=local_rows.astype("<i4"),
            world_codes=world_codes.astype(np.int8))
        record_file("episode-predictions.npz")
        save("allowed-replay.json",allowed_replay)
        save("episode-results.json",dict(allowed=allowed_records,denied=denied_records))

        guard();precheck(parents["c195_summary"],*args)
        for f,hsh in protected.items():require(audit.sha(f)==hsh,"Protected input changed:"+f)
        for a in artifacts:require(audit.sha(out/a["file"])==a["sha256"],"Output changed:"+a["file"])
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status="PASS" if gate(allowed_records,denied_records) else "FAIL",
            diagnostic_execution_valid=True,C195_summary_sha256=PARENT_SHA,
            C194_reference_sha256=REFERENCE_SHA,source_blobs=pins,input_sha256=protected,
            artifacts=artifacts,allowed_records=allowed_records,denied_records=denied_records,
            allowed_replay=allowed_replay,episodes_per_arm=85824,
            new_training=0,fresh_seeds=0,network_calls=0,answer_generation=0,
            proof_checker_calls=0,core_evidence_writes=0,production_runtime_modified=False,
            gate_e_candidate=False,wall_clock_seconds=time.perf_counter()-started,
            limitations=["same repeatedly inspected development family",
                "only first-acquisition post-decision permission revocation tested",
                "no provider failure/stale/attempt-limit/resource-policy/tool-choice/holdout/language/answer/proof/GateE"])
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C196] source/output preservation checked",flush=True)
        print("=== C196 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/"invalid.json").write_bytes(blob(dict(experiment_id=EXPERIMENT_ID,status="INVALID",
            diagnostic_execution_valid=False,error=str(exc),
            completed_allowed=allowed_records,completed_denied=denied_records)))
        raise

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in PRIOR_NAMES:p.add_argument("--"+n+"-summary",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))
if __name__=="__main__":main()
