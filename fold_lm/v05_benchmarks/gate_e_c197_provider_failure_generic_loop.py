"""C197: provider-failure containment in the accepted result-aware generic loop.

Hold C196 loop semantics, budget13, frozen C181/C188 models, cohort and coherent source
bindings. Change only the first acquisition endpoint outcome: after successful authority
and reservation, the endpoint is invoked once and raises ProviderFailure. The accepted
result-aware loop must terminate unresolved without publication, receipt, retry or fake
SUFFICIENT.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, time
from pathlib import Path
import numpy as np
import torch

EXPERIMENT_ID="C197-v5e-provider-failure-reason-propagation"
STAGE="V5-E-PROVIDER-FAILURE-REASON-PROPAGATION"
BASE="561cc91eaaa219a0c627a79b249aa07d76ad759b"
PARENT_EXECUTION="c1a4e68c785fab6441dd08892588add81f9486d6"
PARENT_SHA="b0de25067be3fb9ab24486e2936a62b26f6cf0446f3b85f7e97f7cb932d7e6fb"
REFERENCE_EXECUTION="32e62fe1b2e8318daa766aff1bfcc1f0fc49d95a"
REFERENCE_SHA="6cdb274da944bc87cea29f2e093d4acdec6035dae6978adaf469f1d9b4dfa084"
BASE_SEEDS=(181001,181002,181003)
HEAD_SEEDS=(188001,188002,188003)
ARM="INTERNAL_SEMANTICS"
ARMS=("ALLOWED","PROVIDER_FAILURE_AFTER_RESERVATION")
BATCH=1024
ATOL=1e-6
PRIOR_NAMES=("c196","c195","c194","c193","c192","c191","c190","c189","c188","c187","c186",
             "c185","c184","c183","c182","c181","c180","c179","c178","c177","c176","c174")
OWN=("fold_lm/v05_benchmarks/gate_e_c197_provider_failure_generic_loop.py",
     "tests_lm/test_v05_c197_provider_failure_generic_loop.py",
     "tools/run_c197.ps1","tools/invoke_c197.ps1",
     "docs/experiment-ledger-addendum-c197-preregistration.md")
EXPECTED_TESTS=1653
OUTPUTS={"provider-failure-plan.json","allowed-replay.json","episode-results.json",
         "episode-traces.jsonl.gz","episode-predictions.npz"}

def require(ok,msg):
    if not ok: raise ValueError(msg)

def blob(v):
    return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()

def digest(v):
    return hashlib.sha256(blob(v)).hexdigest()

class FailingProvider:
    def __init__(self):
        self.calls=0
    def __call__(self,request):
        from fold_lm.v05 import structured_acquisition_lifecycle as life
        self.calls+=1
        raise life.ProviderFailure("C197_FORCED_PROVIDER_FAILURE")

def run_loop_reason_aware(views,world_codes,endpoints,base,selector,initial):
    """C196 result-aware continuation plus one terminal-reason propagation rule."""
    from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as c196
    records,arrays,meter=c196.run_loop_result_aware(
        views,world_codes,endpoints,base,selector,initial,"ALLOWED")
    for rec in records:
        if not rec["acquisitions"]:
            continue
        acq=rec["acquisitions"][-1]
        if c196.admitted(acq):
            continue
        action=acq.get("action") if isinstance(acq,dict) else None
        dispatch=acq.get("dispatch") if isinstance(acq,dict) else None
        reason=(dispatch.get("reason") if isinstance(dispatch,dict)
                else action.get("reason") if isinstance(action,dict) else "UNKNOWN")
        rec["status"]="UNRESOLVED_ACQUISITION_"+str(reason)
    return records,arrays,meter

FAIL_COUNTERS=("failed","initial_prediction_error","provider_failure_error","status_error",
               "provider_call_error","publication_error","receipt_error","retry_error",
               "resource_error","fact_mutation_error","fake_sufficient_error")

def score_failure(record,ref_initial_n,ref_initial_t,initial_features):
    ph=record["phases"];acq=record["acquisitions"];final=record["final"]
    initial_prediction_error=int(not (
        len(ph)==1
        and ph[0]["necessity_prediction"]==int(ref_initial_n)
        and ph[0].get("target_prediction")==int(ref_initial_t)))
    a=acq[0] if len(acq)==1 else None
    action=a["action"] if isinstance(a,dict) else None
    dispatch=a["dispatch"] if isinstance(a,dict) else None
    provider_failure_error=int(not (
        isinstance(action,dict) and isinstance(dispatch,dict)
        and action["status"]=="PENDING"
        and action["reason"]=="ACQUISITION_RESERVED"
        and action["internal_charged"]==1
        and action["acquisition_reserved"]==1
        and dispatch["status"]=="UNRESOLVED"
        and dispatch["reason"]=="PROVIDER_FAILURE"
        and dispatch["internal_charged"]==2
        and dispatch["provider_calls"]==1
        and dispatch["fact_publications"]==0
        and dispatch["evidence"] is None))
    status_error=int(record["status"]!="UNRESOLVED_ACQUISITION_PROVIDER_FAILURE")
    provider_call_error=int(not isinstance(dispatch,dict) or dispatch.get("provider_calls")!=1)
    publication_error=int(isinstance(dispatch,dict) and dispatch.get("fact_publications",0)!=0)
    receipt_error=int(len(record["receipts"])!=0)
    retry_error=int(len(ph)!=1 or len(acq)!=1 or record["decision_charges"]!=1)
    f=np.asarray(final["features"],dtype=np.int64)
    resource_error=int(not (
        f[62]==9 and f[63]==3 and f[64]==1 and f[67]==1
        and f[70]==0 and f[71]==11
        and record["pending"] is None and record["runtime_terminal"] is None))
    x=np.asarray(initial_features,dtype=np.int64)
    fact_mutation_error=int(any(f[46:62]!=x[46:62]))
    fake_sufficient_error=int(record["status"]=="SUFFICIENT_CLASSIFICATION")
    vals=(initial_prediction_error,provider_failure_error,status_error,provider_call_error,
          publication_error,receipt_error,retry_error,resource_error,fact_mutation_error,
          fake_sufficient_error)
    return dict(failed=int(any(vals)),initial_prediction_error=initial_prediction_error,
        provider_failure_error=provider_failure_error,status_error=status_error,
        provider_call_error=provider_call_error,publication_error=publication_error,
        receipt_error=receipt_error,retry_error=retry_error,resource_error=resource_error,
        fact_mutation_error=fact_mutation_error,fake_sufficient_error=fake_sufficient_error)

def expected_order():
    return [(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS]

def gate(allowed,failure):
    from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as parent
    if [(r.get("base_seed"),r.get("head_seed")) for r in allowed]!=expected_order(): return False
    if [(r.get("base_seed"),r.get("head_seed")) for r in failure]!=expected_order(): return False
    for r in allowed:
        if r.get("episodes")!=9536: return False
        if any(r.get(k)!=0 for k in parent.ALLOWED_COUNTERS): return False
        if r.get("first_reads")!=9536 or r.get("third_reads")!=r.get("final_decision_rows"): return False
        if r.get("actual_reads")!=r["first_reads"]+r["second_reads"]+r["third_reads"]: return False
        if r.get("reference_necessity_prediction_errors")!=0 or r.get("reference_target_prediction_errors")!=0: return False
        if r.get("reference_necessity_max_abs_logit_difference",1)>ATOL: return False
        if r.get("reference_target_max_abs_logit_difference",1)>ATOL: return False
    for r in failure:
        if r.get("episodes")!=9536: return False
        if any(type(r.get(k)) is not int or r[k]<0 for k in FAIL_COUNTERS): return False
        if any(r[k]!=0 for k in FAIL_COUNTERS): return False
        if r.get("failure_attempts")!=9536 or r.get("provider_calls")!=9536: return False
        if r.get("adapter_calls")!=9536 or r.get("publications")!=0 or r.get("receipts")!=0: return False
        if r.get("learned_decisions")!=9536 or r.get("retries")!=0: return False
        if r.get("initial_reference_prediction_errors")!=0 or r.get("initial_reference_target_errors")!=0: return False
        if r.get("initial_reference_necessity_logit_delta",1)>ATOL: return False
        if r.get("initial_reference_target_logit_delta",1)>ATOL: return False
    return True

def manifest():
    return dict(
      experiment_id=EXPERIMENT_ID,stage=STAGE,parent_sha256=PARENT_SHA,
      acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
      reference_execution=REFERENCE_EXECUTION,reference_sha256=REFERENCE_SHA,
      base_seeds=BASE_SEEDS,head_seeds=HEAD_SEEDS,arms=ARMS,arm=ARM,
      question="can one failure-reason propagation rule preserve accepted C196 allowed behavior and safely expose a post-reservation ProviderFailure as the generic-loop terminal unresolved cause",
      changed="when a non-admitted acquisition has a dispatch result, generic-loop terminal unresolved status uses dispatch.reason; otherwise it keeps action.reason",
      held="budget13,C174 cohort,9 frozen C181/C188 pairs,16 coherent source bindings,C172/C173,C196 result-aware continuation rule,teachers,max_dispatches3,raw argmax",
      allowed_arm="full9536 worlds/selector; exact accepted C196/C194 allowed replay required",
      failure_arm="full9536 worlds/selector; one PENDING/ACQUISITION_RESERVED action then one UNRESOLVED/PROVIDER_FAILURE dispatch/provider call; terminal status must preserve PROVIDER_FAILURE; zero publication/receipt/retry/fake-sufficient",
      failure_resources="after decision+reservation+failed provider dispatch: internal9,acquisitions3,RETRIEVE available1/permitted1,last_outcome NONE,step11,pending none",
      episodes_per_arm=85824,blocks_per_arm=9,
      gate="all9 allowed blocks exact reference replay and zero scientific errors; all9 failure blocks9536 provider failures,9536 provider calls,terminal reason PROVIDER_FAILURE,zero publication/receipt/retry/fact mutation/fake sufficient,exact resources",
      training=0,fresh_seeds=0,network_calls=0,answer_generation=0,proof_checker_calls=0,core_evidence_writes=0,
      production_runtime_modified=False,gate_e_candidate=False,outputs=sorted(OUTPUTS),
      limits="development family;only first-acquisition provider failure and status propagation tested;no stale/attempt-limit/resource-policy/tool-choice/holdout/language/answer/proof/GateE")

MANIFEST_SHA="7f7121c336e68dc58578e35f75b7c459986f5adbd2329344fc08514e468d58d2"

def precheck(c196_summary,*args):
    from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as parent
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(len(args)==22,"Twenty-one prior summaries and repository root required")
    root=args[-1]
    p195,p194,p193,p192,p191,p190,p189,p188,p181,p174,pins,protected=parent.precheck(
        args[0],*args[1:])
    require(audit.sha(c196_summary)==PARENT_SHA,"C196 summary changed")
    p196=audit.read_json(c196_summary);parent.validate_result(p196)
    require(p196["commit_sha"]==PARENT_EXECUTION and p196["status"]=="PASS"
            and parent.gate(p196["allowed_records"],p196["denied_records"])
            and p196["source_blobs"]==pins,
            "Wrong accepted C196 source/result")
    protected[str(Path(c196_summary).resolve())]=PARENT_SHA
    for a in p196["artifacts"]:
        f=audit.safe_child(Path(c196_summary).resolve().parent,a["file"])
        require(f.is_file() and f.stat().st_size==a["serialized_bytes"] and audit.sha(f)==a["sha256"],
                "Changed C196 artifact:"+a["file"])
        protected[str(f.resolve())]=a["sha256"]
    pins=dict(pins)
    for name in parent.OWN:
        pins[name]=audit.git(root,"rev-parse",PARENT_EXECUTION+":"+name).decode().strip()
    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins)==146 and len(protected)==385,"Source/protected union drift")
    require(digest(manifest())==MANIFEST_SHA,"Manifest drift")
    return p196,p195,p194,p193,p192,p191,p190,p189,p188,p181,p174,pins,protected

def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as parent
    names=parent.regression_modules(root)
    require(len(names)==len(set(names))==81,"Historical regression list drift")
    return names+["tests_lm.test_v05_c197_provider_failure_generic_loop"]

def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE
            and p["diagnostic_execution_valid"] is True,"Wrong/incomplete C197")
    require(p["episodes_per_arm"]==85824
            and len(p["allowed_records"])==len(p["failure_records"])==9
            and len(p["source_blobs"])==146 and len(p["input_sha256"])==385
            and len(p["artifacts"])==5 and {a["file"] for a in p["artifacts"]}==OUTPUTS,
            "Workload/coverage drift")
    require(all(p[k]==0 for k in ("new_training","fresh_seeds","network_calls",
                                  "answer_generation","proof_checker_calls","core_evidence_writes"))
            and p["production_runtime_modified"] is False and p["gate_e_candidate"] is False,
            "Scope drift")
    require(p["status"]==("PASS" if gate(p["allowed_records"],p["failure_records"]) else "FAIL"),
            "Gate drift")

def run(*,output_dir,expected_head,**parents):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
    from fold_lm.v05_benchmarks import gate_e_c193_budget13_authoritative_closure as c193
    from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as c196

    root=Path(__file__).resolve().parents[2]
    args=tuple(parents[n+"_summary"] for n in PRIOR_NAMES[1:])+(root,)
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"Dirty tracked tree")
    guard()
    p196,p195,p194,p193,p192,p191,p190,p189,p188,p181,p174,pins,protected=precheck(
        parents["c196_summary"],*args)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    artifacts=[];allowed_records=[];failure_records=[];started=time.perf_counter()
    def record_file(name):
        f=out/name;artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,v):
        (out/name).write_bytes(blob(v));record_file(name)
    save("provider-failure-plan.json",dict(manifest(),source_blobs=pins))
    try:
        print("[C197] plan fixed; accepted C196 loop; ALLOWED replay + post-reservation ProviderFailure",flush=True)
        torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
        data,metadata=audit.load_data(Path(parents["c174_summary"]).resolve().parent,p174)
        raw_all=torch.from_numpy(data["features"].copy())
        valid=c189.target_teacher(data["features"],data["template_ids"],metadata)
        _,_,evfull,_,_=target.cohort_masks(raw_all,data["labels"],data["split_codes"],valid)
        full_ix=np.flatnonzero(evfull)
        raw12=torch.from_numpy(data["features"][evfull].copy())
        raw13=c193.budget13(raw12)
        expanded12,source_rows,local_rows,world_codes=c190.expand_worlds(raw12,full_ix)
        expanded13=c193.budget13(expanded12)
        tids=data["template_ids"][evfull]

        c194_dir=Path(parents["c194_summary"]).resolve().parent
        saved=c196.load_c194_predictions(c194_dir/"episode-predictions.npz")
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
        real_providers={};real_endpoints={};fault_adapters={};fault_endpoints={}
        for code in range(16):
            f=source_dir/f"world-{code:02d}.json"
            expected=c190.SOURCE_FILES[f"sources/world-{code:02d}.json"]
            require(f.is_file() and audit.sha(f)==expected,"Changed protected coherent world source")
            sb=life.SourceBinding(f"C190-world-{code:02d}",expected)
            rp=life.FileSnapshotProvider(f,sb);real_providers[code]=rp;real_endpoints[code]=life.Endpoint(sb,rp)
            fp=FailingProvider();fault_adapters[code]=fp;fault_endpoints[code]=life.Endpoint(sb,fp)

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
                        views=c190.make_views(expanded13,source_rows,world_codes,
                                             f"C197-{arm}-b{b}-h{h}")
                        if arm=="ALLOWED":
                            before_reads=sum(p.reads for p in real_providers.values())
                            before_bytes=sum(p.bytes_read for p in real_providers.values())
                            observed,arrays,_=run_loop_reason_aware(
                                views,world_codes,real_endpoints,bases[b],heads[b,h],initial)
                            reads=sum(p.reads for p in real_providers.values())-before_reads
                            bytes_read=sum(p.bytes_read for p in real_providers.values())-before_bytes
                        else:
                            before_calls=sum(p.calls for p in fault_adapters.values())
                            observed,arrays,_=run_loop_reason_aware(
                                views,world_codes,fault_endpoints,bases[b],heads[b,h],initial)
                            reads=0;bytes_read=0
                            adapter_calls=sum(p.calls for p in fault_adapters.values())-before_calls
                            for rec in observed: rec["arm"]=arm

                        dense_n[arm_i,idx]=arrays["necessity_predictions"]
                        dense_z[arm_i,idx]=arrays["necessity_logits"]
                        dense_t[arm_i,idx]=arrays["target_predictions"]
                        dense_tz[arm_i,idx]=arrays["target_logits"]

                        if arm=="ALLOWED":
                            replay=c196.replay_metrics(arrays,reference)
                            allowed_replay.append(dict(base_seed=b,head_seed=h,**replay))
                            replay_error=int(replay["necessity_prediction_errors"]!=0
                                or replay["target_prediction_errors"]!=0
                                or replay["necessity_max_abs_logit_difference"]>ATOL
                                or replay["target_max_abs_logit_difference"]>ATOL)
                            scores=[]
                            for j,rec in enumerate(observed):
                                q=c193.assess(rec,int(tids[int(local_rows[j])]),metadata,
                                              c190.WORLD_BITS[int(world_codes[j])])
                                q["reference_replay_error"]=replay_error
                                q["reference_block_mismatch"]=0
                                q["failed"]=int(q["failed"] or replay_error)
                                scores.append(q)
                            totals={k:sum(x[k] for x in scores) for k in c193.COUNTERS}
                            ref_rec=p196["allowed_records"][idx]
                            block_mismatch=int(any((
                                totals["first_reads"]!=ref_rec["first_reads"],
                                totals["second_reads"]!=ref_rec["second_reads"],
                                totals["third_reads"]!=ref_rec["third_reads"],
                                totals["final_decision_rows"]!=ref_rec["final_decision_rows"],
                                reads!=ref_rec["actual_reads"])))
                            if block_mismatch:
                                for q in scores:q["reference_block_mismatch"]=1;q["failed"]=1
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
                            trace_scores=scores
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
                            scores=[score_failure(rec,ref_n[j],ref_t[j],rec["initial"]["features"])
                                    for j,rec in enumerate(observed)]
                            totals={k:sum(x[k] for x in scores) for k in FAIL_COUNTERS}
                            attempts=sum(len(rec["acquisitions"]) for rec in observed)
                            provider_calls=sum((a["dispatch"] or {}).get("provider_calls",0)
                                for rec in observed for a in rec["acquisitions"])
                            publications=sum((a["dispatch"] or {}).get("fact_publications",0)
                                for rec in observed for a in rec["acquisitions"])
                            receipts=sum(len(rec["receipts"]) for rec in observed)
                            decisions=sum(rec["decision_charges"] for rec in observed)
                            retries=sum(max(0,len(rec["phases"])-1) for rec in observed)
                            rec=dict(base_seed=b,head_seed=h,episodes=9536,
                                failure_attempts=attempts,provider_calls=provider_calls,
                                adapter_calls=adapter_calls,publications=publications,receipts=receipts,
                                learned_decisions=decisions,retries=retries,
                                initial_reference_prediction_errors=initial_nerr,
                                initial_reference_target_errors=initial_terr,
                                initial_reference_necessity_logit_delta=nd,
                                initial_reference_target_logit_delta=td,**totals)
                            failure_records.append(rec)
                            trace_scores=scores

                        for j,rec0 in enumerate(observed):
                            trace.write(json.dumps(dict(arm=arm,base_seed=b,head_seed=h,
                                source_row=int(source_rows[j]),world_code=int(world_codes[j]),
                                score=trace_scores[j],trace=rec0),
                                sort_keys=True,separators=(",",":"),allow_nan=False)+"\n")
                        print(f"[C197] arm={arm} block={idx+1}/9 base={b} head={h} "
                              f"failed={rec['failed']} ",flush=True)

        record_file("episode-traces.jsonl.gz")
        np.savez_compressed(out/"episode-predictions.npz",
            necessity_predictions=dense_n,necessity_logits=dense_z,
            target_predictions=dense_t,target_logits=dense_tz,
            row_indices=source_rows.astype("<i4"),local_rows=local_rows.astype("<i4"),
            world_codes=world_codes.astype(np.int8))
        record_file("episode-predictions.npz")
        save("allowed-replay.json",allowed_replay)
        save("episode-results.json",dict(allowed=allowed_records,failure=failure_records))

        guard();precheck(parents["c196_summary"],*args)
        for f,hsh in protected.items():require(audit.sha(f)==hsh,"Protected input changed:"+f)
        for a in artifacts:require(audit.sha(out/a["file"])==a["sha256"],"Output changed:"+a["file"])
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status="PASS" if gate(allowed_records,failure_records) else "FAIL",
            diagnostic_execution_valid=True,C196_summary_sha256=PARENT_SHA,
            C194_reference_sha256=REFERENCE_SHA,source_blobs=pins,input_sha256=protected,
            artifacts=artifacts,allowed_records=allowed_records,failure_records=failure_records,
            allowed_replay=allowed_replay,episodes_per_arm=85824,
            new_training=0,fresh_seeds=0,network_calls=0,answer_generation=0,
            proof_checker_calls=0,core_evidence_writes=0,production_runtime_modified=False,
            gate_e_candidate=False,wall_clock_seconds=time.perf_counter()-started,
            limitations=["same repeatedly inspected development family",
                "only first-acquisition ProviderFailure tested",
                "no stale/attempt-limit/resource-policy/tool-choice/holdout/language/answer/proof/GateE"])
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C197] source/output preservation checked",flush=True)
        print("=== C197 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/"invalid.json").write_bytes(blob(dict(experiment_id=EXPERIMENT_ID,status="INVALID",
            diagnostic_execution_valid=False,error=str(exc),
            completed_allowed=allowed_records,completed_failure=failure_records)))
        raise

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in PRIOR_NAMES:p.add_argument("--"+n+"-summary",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))
if __name__=="__main__": main()
