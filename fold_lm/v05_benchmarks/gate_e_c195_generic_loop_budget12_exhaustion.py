"""C195: generic-loop budget-exhaustion safety at original internal budget12.

Hold the accepted C194 generic state-driven bounded loop fixed and change only the initial
TaskView internal_remaining coordinate from13 back to12. The reference behavior is accepted
C191, which exercised the same frozen components/cohort at budget12 with hand-unrolled
orchestration. C195 asks whether the generic loop reproduces that path and stops safely when
the fourth scheduler debit is unavailable after a third acquisition.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, time
from pathlib import Path
import numpy as np
import torch

EXPERIMENT_ID="C195-v5e-generic-loop-budget12-exhaustion"
STAGE="V5-E-GENERIC-LOOP-BUDGET12-EXHAUSTION"
BASE="53b9d957763a76003321b63af2ed4255b5a6b835"
PARENT_EXECUTION="32e62fe1b2e8318daa766aff1bfcc1f0fc49d95a"
PARENT_SHA="6cdb274da944bc87cea29f2e093d4acdec6035dae6978adaf469f1d9b4dfa084"
REFERENCE_EXECUTION="f83ed1d60758dc1ff895b2b9c42c69d6a68c0931"
REFERENCE_SHA="b05cd702e9572c61a3ae981e5279c7fb096fe1078c7d65f6401f180f307c84f4"
BASE_SEEDS=(181001,181002,181003)
HEAD_SEEDS=(188001,188002,188003)
ARM="INTERNAL_SEMANTICS"
BATCH=1024
ATOL=1e-6
PRIOR_NAMES=("c194","c193","c192","c191","c190","c189","c188","c187","c186","c185",
             "c184","c183","c182","c181","c180","c179","c178","c177","c176","c174")
OWN=("fold_lm/v05_benchmarks/gate_e_c195_generic_loop_budget12_exhaustion.py",
     "tests_lm/test_v05_c195_generic_loop_budget12_exhaustion.py",
     "tools/run_c195.ps1","tools/invoke_c195.ps1",
     "docs/experiment-ledger-addendum-c195-preregistration.md")
EXPECTED_TESTS=1605
OUTPUTS={"budget12-loop-plan.json","reference-replay.json","episode-results.json",
         "episode-traces.jsonl.gz","episode-predictions.npz"}

def require(ok,msg):
    if not ok: raise ValueError(msg)

def blob(v):
    return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()

def digest(v):
    return hashlib.sha256(blob(v)).hexdigest()

def load_reference_predictions(path):
    p=Path(path)
    require(p.is_file() and p.stat().st_size < 10_000_000,
            "Unexpected C191 prediction artifact size")
    with np.load(p,allow_pickle=False) as z:
        expected={"necessity_predictions","necessity_logits","target_predictions","target_logits",
                  "row_indices","local_rows","world_codes"}
        require(set(z.files)==expected,"C191 prediction schema drift")
        out={k:z[k].copy() for k in z.files}
    require(out["necessity_predictions"].shape==(9,9536,3)
            and out["necessity_logits"].shape==(9,9536,3,2)
            and out["target_predictions"].shape==(9,9536,3)
            and out["target_logits"].shape==(9,9536,3,4)
            and out["row_indices"].shape==(9536,)
            and out["local_rows"].shape==(9536,)
            and out["world_codes"].shape==(9536,),
            "C191 prediction array drift")
    return out

def reference_replay_metrics(arrays,reference):
    ncur=arrays["necessity_predictions"][:,:3]
    zcur=arrays["necessity_logits"][:,:3]
    tcur=arrays["target_predictions"]
    tzcur=arrays["target_logits"]
    nref=reference["necessity_predictions"]
    zref=reference["necessity_logits"]
    tref=reference["target_predictions"]
    tzref=reference["target_logits"]
    nerr=int((ncur!=nref).sum())
    terr=int((tcur!=tref).sum())
    nmask=nref>=0
    tmask=tref>=0
    ndelta=float(np.max(np.abs(zcur[nmask]-zref[nmask]))) if nmask.any() else 0.0
    finite=np.isfinite(tzref) & np.repeat(tmask[:,:,None],4,axis=2)
    tdelta=float(np.max(np.abs(tzcur[finite]-tzref[finite]))) if finite.any() else 0.0
    unauthorized=int((arrays["necessity_predictions"][:,3]>=0).sum())
    return dict(necessity_prediction_errors=nerr,target_prediction_errors=terr,
                necessity_max_abs_logit_difference=ndelta,
                target_max_abs_logit_difference=tdelta,
                unauthorized_final_predictions=unauthorized)

COUNTERS=("failed","reference_replay_error","reference_block_mismatch",
          "acquisition_contract_error","status_error","resource_error",
          "final_logical_error","fake_final_decision","first_reads","second_reads",
          "third_reads","exhausted_rows","sufficient_rows")

def assess(record,reference_n,reference_t,template_id,metadata,world_bits):
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
    ph=record["phases"];acq=record["acquisitions"];final=record["final"]
    ref_active=reference_n>=0
    expected_phases=int(ref_active.sum())
    expected_acq=int((reference_n==1).sum())
    ref_targets=[int(reference_t[q]) for q in range(3)
                 if reference_n[q]==1 and int(reference_t[q])>=0]

    acquisition_error=0
    if len(acq)!=expected_acq or len(record["receipts"])!=expected_acq:
        acquisition_error+=1
    for q in range(min(expected_acq,len(acq),len(ref_targets),len(record["receipts"]))):
        a=acq[q];d=a["dispatch"];t=ref_targets[q]
        ok=(a["input_index"]==t and d is not None
            and a["action"]["status"]=="PENDING"
            and a["action"]["reason"]=="ACQUISITION_RESERVED"
            and a["action"]["acquisition_reserved"]==1
            and d["status"]=="PUBLISHED"
            and d["reason"]=="OBSERVATION_ADMITTED"
            and d["provider_calls"]==1 and d["fact_publications"]==1
            and record["receipts"][q]["fact_id"]==a["fact_id"]
            and record["receipts"][q]["value"]==world_bits[t])
        acquisition_error+=int(not ok)

    exhausted=int(expected_acq==3)
    expected_status="BUDGET_EXHAUSTED" if exhausted else "SUFFICIENT_CLASSIFICATION"
    status_error=int(record["status"]!=expected_status or len(ph)!=expected_phases)

    expected_decisions=3 if exhausted else expected_acq+1
    expected_internal=12-expected_decisions-3*expected_acq
    expected_acq_remaining=4-expected_acq
    expected_step=7+expected_decisions+3*expected_acq
    f=np.asarray(final["features"],dtype=np.int64)
    resource_error=int(not (
        record["decision_charges"]==expected_decisions
        and f[62]==expected_internal
        and f[63]==expected_acq_remaining
        and f[71]==expected_step
        and record["pending"] is None
        and record["runtime_terminal"] is None))

    final_logical_error=0
    fake_final=0
    if exhausted:
        final_logical_error=int(c190.logical_label(final["features"],template_id,metadata)!=0)
        fake_final=int(len(ph)>3 or record["decision_charges"]>3
                       or record["status"]=="SUFFICIENT_CLASSIFICATION")
        resource_error=int(resource_error or expected_internal!=0
                           or expected_acq_remaining!=1 or expected_step!=19
                           or not all(f[48+4*j]==1 for j in range(4)))

    vals=(acquisition_error,status_error,resource_error,final_logical_error,fake_final)
    return dict(failed=int(any(vals)),reference_replay_error=0,
        reference_block_mismatch=0,acquisition_contract_error=int(acquisition_error),
        status_error=status_error,resource_error=resource_error,
        final_logical_error=final_logical_error,fake_final_decision=fake_final,
        first_reads=int(expected_acq>=1),second_reads=int(expected_acq>=2),
        third_reads=int(expected_acq>=3),exhausted_rows=exhausted,
        sufficient_rows=int(not exhausted))

def expected_order():
    return [(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS]

def reference_block_expectations(ref_rec):
    """Normalize the accepted C191 per-block record through its actual schema."""
    required={"episodes","parent_second_reads","third_provider_calls","actual_reads",
              "parent_final_needs","final_logical_needs","fourth_decision_accepted"}
    require(isinstance(ref_rec,dict) and required.issubset(ref_rec),
            "C191 reference record schema drift")
    for key in required-{"episodes"}:
        require(type(ref_rec[key]) is int and ref_rec[key]>=0,
                "C191 reference record counter drift:"+key)
    require(ref_rec["episodes"]==9536,"C191 reference episode count drift")
    require(ref_rec["parent_final_needs"]==ref_rec["third_provider_calls"]==928,
            "C191 reference exhausted/third-read count drift")
    require(ref_rec["final_logical_needs"]==0
            and ref_rec["fourth_decision_accepted"]==0,
            "C191 reference final boundary drift")
    return dict(second_reads=ref_rec["parent_second_reads"],
                third_reads=ref_rec["third_provider_calls"],
                exhausted_rows=ref_rec["third_provider_calls"],
                actual_reads=ref_rec["actual_reads"])

def gate(records):
    if [(r.get("base_seed"),r.get("head_seed")) for r in records]!=expected_order():
        return False
    for r in records:
        if r.get("episodes")!=9536 or r.get("reference_exhausted_rows")!=928:
            return False
        if any(type(r.get(k)) is not int or r[k]<0 for k in COUNTERS):
            return False
        if any(r[k]!=0 for k in ("failed","reference_replay_error",
                                  "reference_block_mismatch","acquisition_contract_error",
                                  "status_error","resource_error","final_logical_error",
                                  "fake_final_decision")):
            return False
        if r["first_reads"]!=9536 or r["exhausted_rows"]!=928:
            return False
        if r["third_reads"]!=r["exhausted_rows"]:
            return False
        if r["sufficient_rows"]+r["exhausted_rows"]!=9536:
            return False
        if r.get("actual_reads")!=r["first_reads"]+r["second_reads"]+r["third_reads"]:
            return False
        if r.get("reference_necessity_prediction_errors")!=0:
            return False
        if r.get("reference_target_prediction_errors")!=0:
            return False
        if r.get("reference_unauthorized_final_predictions")!=0:
            return False
        if r.get("reference_necessity_max_abs_logit_difference",1)>ATOL:
            return False
        if r.get("reference_target_max_abs_logit_difference",1)>ATOL:
            return False
    return True

def manifest():
    return dict(
      experiment_id=EXPERIMENT_ID,stage=STAGE,parent_sha256=PARENT_SHA,
      acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
      reference_execution=REFERENCE_EXECUTION,reference_sha256=REFERENCE_SHA,
      base_seeds=BASE_SEEDS,head_seeds=HEAD_SEEDS,arm=ARM,
      question="with the accepted generic loop held fixed and only initial internal budget13->12, does it reproduce accepted C191 budget-exhaustion behavior without fake sufficiency or extra work",
      changed="TaskView internal_remaining initial coordinate13->12 only; generic C194 loop implementation is reused unchanged",
      held="same C174 cohort,9 frozen C181/C188 pairs,16 coherent worlds,C172/C173,teachers,max_dispatches3 and loop semantics",
      reference="accepted C191 budget12 predictions/read depths/final exhaustion boundary",
      cohort="same1768 PILOT NEEDS missing2/3 expanded to9536 coherent worlds per selector",
      episodes=85824,blocks=9,selectors=9,
      exhaustion_contract="three-acquisition rows end with BUDGET_EXHAUSTED,decision_charges3,resources0/1/19,all facts observed,logical final SUFFICIENT,but no fourth learned prediction",
      replay="first3 necessity and all3 target predictions exact to C191; active finite logits <=1e-6; per-block second/third/read totals exact",
      gate="all9 blocks zero runtime/replay/block/status/resource/fake-final errors;928 exhausted rows each;no unauthorized phase3 prediction;exact reads",
      training=0,fresh_seeds=0,network_calls=0,answer_generation=0,proof_checker_calls=0,core_evidence_writes=0,
      production_runtime_modified=False,gate_e_candidate=False,outputs=sorted(OUTPUTS),
      limits="development family;budget12 safety test only;does not learn resource policy or prove arbitrary loop/tool-provider/holdout/language/answer/proof/GateE")
MANIFEST_SHA="ebfa3e2f916368b4e2b07efa072c9f9c2b4ec62cb0c77ac69e3cb1f527b90128"

def precheck(c194_summary,*args):
    from fold_lm.v05_benchmarks import gate_e_c194_generic_bounded_loop as parent
    from fold_lm.v05_benchmarks import gate_e_c191_third_acquisition_budget as reference
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(len(args)==20,"Nineteen prior summaries and repository root required")
    root=args[-1]
    p193,p192,p191,p190,p189,p188,p181,p174,pins,protected=parent.precheck(args[0],*args[1:])
    require(audit.sha(c194_summary)==PARENT_SHA,"C194 summary changed")
    p194=audit.read_json(c194_summary);parent.validate_result(p194)
    require(p194["commit_sha"]==PARENT_EXECUTION and p194["status"]=="PASS"
            and parent.gate(p194["records"]) and p194["source_blobs"]==pins,
            "Wrong accepted C194 source/result")

    c191_summary=Path(args[2])
    require(audit.sha(c191_summary)==REFERENCE_SHA,"C191 reference summary changed")
    p191ref=audit.read_json(c191_summary);reference.validate_result(p191ref)
    require(p191ref["commit_sha"]==REFERENCE_EXECUTION and p191ref["status"]=="PASS"
            and reference.gate(p191ref["records"]),
            "Wrong accepted C191 reference")

    protected[str(Path(c194_summary).resolve())]=PARENT_SHA
    for a in p194["artifacts"]:
        f=audit.safe_child(Path(c194_summary).resolve().parent,a["file"])
        require(f.is_file() and f.stat().st_size==a["serialized_bytes"] and audit.sha(f)==a["sha256"],
                "Changed C194 artifact:"+a["file"])
        protected[str(f.resolve())]=a["sha256"]

    pins=dict(pins)
    for name in parent.OWN:
        pins[name]=audit.git(root,"rev-parse",PARENT_EXECUTION+":"+name).decode().strip()
    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins)==136 and len(protected)==363,"Source/protected union drift")
    require(digest(manifest())==MANIFEST_SHA,"Manifest drift")
    return p194,p191ref,p193,p192,p191,p190,p189,p188,p181,p174,pins,protected

def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c194_generic_bounded_loop as parent
    names=parent.regression_modules(root)
    require(len(names)==len(set(names))==79,"Historical regression list drift")
    return names+["tests_lm.test_v05_c195_generic_loop_budget12_exhaustion"]

def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE
            and p["diagnostic_execution_valid"] is True,"Wrong/incomplete C195")
    require(p["episodes"]==85824 and len(p["records"])==9
            and len(p["source_blobs"])==136 and len(p["input_sha256"])==363
            and len(p["artifacts"])==5 and {a["file"] for a in p["artifacts"]}==OUTPUTS,
            "Workload/coverage drift")
    require(all(p[k]==0 for k in ("new_training","fresh_seeds","network_calls",
                                  "answer_generation","proof_checker_calls","core_evidence_writes"))
            and p["production_runtime_modified"] is False and p["gate_e_candidate"] is False,
            "Scope drift")
    require(p["status"]==("PASS" if gate(p["records"]) else "FAIL"),"Gate drift")

def run(*,output_dir,expected_head,**parents):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
    from fold_lm.v05_benchmarks import gate_e_c194_generic_bounded_loop as parent

    root=Path(__file__).resolve().parents[2]
    args=tuple(parents[n+"_summary"] for n in PRIOR_NAMES[1:])+(root,)
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"Dirty tracked tree")
    guard()
    p194,p191ref,p193,p192,p191,p190,p189,p188,p181,p174,pins,protected=precheck(
        parents["c194_summary"],*args)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    artifacts=[];records=[];started=time.perf_counter()
    def record_file(name):
        f=out/name;artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,v):
        (out/name).write_bytes(blob(v));record_file(name)
    save("budget12-loop-plan.json",dict(manifest(),source_blobs=pins))
    try:
        print("[C195] plan fixed; C194 generic loop held; only budget13->12; C191 exact reference",flush=True)
        torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
        data,metadata=audit.load_data(Path(parents["c174_summary"]).resolve().parent,p174)
        raw_all=torch.from_numpy(data["features"].copy())
        valid=c189.target_teacher(data["features"],data["template_ids"],metadata)
        _,_,evfull,_,_=target.cohort_masks(raw_all,data["labels"],data["split_codes"],valid)
        full_ix=np.flatnonzero(evfull)
        raw12=torch.from_numpy(data["features"][evfull].copy())
        expanded12,source_rows,local_rows,world_codes=c190.expand_worlds(raw12,full_ix)
        tids=data["template_ids"][evfull]

        ref_dir=Path(parents["c191_summary"]).resolve().parent
        saved=load_reference_predictions(ref_dir/"episode-predictions.npz")
        require(np.array_equal(saved["row_indices"],source_rows)
                and np.array_equal(saved["local_rows"],local_rows)
                and np.array_equal(saved["world_codes"],world_codes),
                "C191 reference episode identity drift")

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

        dense=dict(necessity_predictions=np.full((9,9536,4),-1,dtype=np.int8),
                   necessity_logits=np.zeros((9,9536,4,2),dtype=np.float32),
                   target_predictions=np.full((9,9536,3),-1,dtype=np.int8),
                   target_logits=np.full((9,9536,3,4),-np.inf,dtype=np.float32))
        reference_replay=[]
        with gzip.open(out/"episode-traces.jsonl.gz","wt",encoding="utf-8",newline="\n") as trace:
            for bi,b in enumerate(BASE_SEEDS):
                for hi,h in enumerate(HEAD_SEEDS):
                    idx=bi*3+hi
                    cache,_=c190.initial_policy_cache(raw12,full_ix,bases[b],heads[b,h])
                    lt=torch.from_numpy(local_rows.astype(np.int64))
                    initial=dict(raw=cache["raw"][lt],
                        necessity_predictions=cache["necessity_predictions"][local_rows],
                        target_predictions=cache["target_predictions"][local_rows],
                        necessity_logits=cache["necessity_logits"][local_rows],
                        target_logits=cache["target_logits"][local_rows])

                    before=sum(p.reads for p in providers.values())
                    views=c190.make_views(expanded12,source_rows,world_codes,f"C195-b{b}-h{h}")
                    observed,arrays,_=parent.run_loop(
                        views,world_codes,endpoints,bases[b],heads[b,h],initial)
                    dense["necessity_predictions"][idx]=arrays["necessity_predictions"]
                    dense["necessity_logits"][idx]=arrays["necessity_logits"]
                    dense["target_predictions"][idx]=arrays["target_predictions"]
                    dense["target_logits"][idx]=arrays["target_logits"]

                    reference={k:saved[k][idx] for k in (
                        "necessity_predictions","necessity_logits","target_predictions","target_logits")}
                    replay=reference_replay_metrics(arrays,reference)
                    reference_replay.append(dict(base_seed=b,head_seed=h,**replay))
                    replay_error=int(replay["necessity_prediction_errors"]!=0
                        or replay["target_prediction_errors"]!=0
                        or replay["unauthorized_final_predictions"]!=0
                        or replay["necessity_max_abs_logit_difference"]>ATOL
                        or replay["target_max_abs_logit_difference"]>ATOL)

                    scores=[]
                    for j,rec in enumerate(observed):
                        score=assess(rec,reference["necessity_predictions"][j],
                            reference["target_predictions"][j],
                            int(tids[int(local_rows[j])]),metadata,
                            c190.WORLD_BITS[int(world_codes[j])])
                        score["reference_replay_error"]=replay_error
                        score["failed"]=int(score["failed"] or replay_error)
                        scores.append(score)

                    base_totals={k:sum(s[k] for s in scores) for k in COUNTERS}
                    reads=sum(p.reads for p in providers.values())-before
                    ref_rec=p191ref["records"][idx]
                    ref_expected=reference_block_expectations(ref_rec)
                    block_mismatch=int(any((
                        base_totals["second_reads"]!=ref_expected["second_reads"],
                        base_totals["third_reads"]!=ref_expected["third_reads"],
                        base_totals["exhausted_rows"]!=ref_expected["exhausted_rows"],
                        reads!=ref_expected["actual_reads"])))
                    if block_mismatch:
                        for score in scores:
                            score["reference_block_mismatch"]=1
                            score["failed"]=1

                    for j,(score,rec) in enumerate(zip(scores,observed,strict=True)):
                        trace.write(json.dumps(dict(base_seed=b,head_seed=h,
                            source_row=int(source_rows[j]),world_code=int(world_codes[j]),
                            score=score,trace=rec),
                            sort_keys=True,separators=(",",":"),allow_nan=False)+"\n")

                    totals={k:sum(s[k] for s in scores) for k in COUNTERS}
                    rec=dict(base_seed=b,head_seed=h,episodes=9536,actual_reads=reads,
                        reference_exhausted_rows=ref_expected["exhausted_rows"],
                        reference_necessity_prediction_errors=replay["necessity_prediction_errors"],
                        reference_target_prediction_errors=replay["target_prediction_errors"],
                        reference_unauthorized_final_predictions=replay["unauthorized_final_predictions"],
                        reference_necessity_max_abs_logit_difference=replay["necessity_max_abs_logit_difference"],
                        reference_target_max_abs_logit_difference=replay["target_max_abs_logit_difference"],
                        **totals)
                    records.append(rec)
                    print(f"[C195] block={len(records)}/9 base={b} head={h} failed={rec['failed']} "
                          f"reads={reads} second={rec['second_reads']} third={rec['third_reads']} "
                          f"exhausted={rec['exhausted_rows']} fake_final={rec['fake_final_decision']} "
                          f"replay_n={replay['necessity_prediction_errors']} "
                          f"replay_t={replay['target_prediction_errors']}",flush=True)

        record_file("episode-traces.jsonl.gz")
        np.savez_compressed(out/"episode-predictions.npz",**dense,row_indices=source_rows.astype("<i4"),
                            local_rows=local_rows.astype("<i4"),world_codes=world_codes.astype(np.int8))
        record_file("episode-predictions.npz")
        save("reference-replay.json",reference_replay);save("episode-results.json",records)

        guard();precheck(parents["c194_summary"],*args)
        for f,hsh in protected.items(): require(audit.sha(f)==hsh,"Protected input changed:"+f)
        for a in artifacts: require(audit.sha(out/a["file"])==a["sha256"],"Output changed:"+a["file"])

        totals={k:sum(r[k] for r in records) for k in COUNTERS}
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status="PASS" if gate(records) else "FAIL",diagnostic_execution_valid=True,
            C194_summary_sha256=PARENT_SHA,C191_reference_sha256=REFERENCE_SHA,
            source_blobs=pins,input_sha256=protected,artifacts=artifacts,
            records=records,reference_replay=reference_replay,totals=totals,
            episodes=85824,actual_file_reads=sum(p.reads for p in providers.values()),
            provider_bytes_read=sum(p.bytes_read for p in providers.values()),
            new_training=0,fresh_seeds=0,network_calls=0,answer_generation=0,
            proof_checker_calls=0,core_evidence_writes=0,
            production_runtime_modified=False,gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=["same repeatedly inspected development family",
                "budget12 exhaustion safety only;not a learned resource policy",
                "no arbitrary loop/tool-provider/independent holdout/language/answer/proof/GateE"])
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C195] source/output preservation checked",flush=True)
        print("=== C195 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/"invalid.json").write_bytes(blob(dict(experiment_id=EXPERIMENT_ID,status="INVALID",
            diagnostic_execution_valid=False,error=str(exc),completed_records=records)))
        raise

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in PRIOR_NAMES:p.add_argument("--"+n+"-summary",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))
if __name__=="__main__": main()
