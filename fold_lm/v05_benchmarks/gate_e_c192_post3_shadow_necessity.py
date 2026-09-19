"""C192: read-only post-third semantic shadow probe under exhausted runtime budget.

Replay accepted C191 exactly through the third real acquisition. On the resulting actual
fully observed states with internal_remaining=0, invoke the frozen C181 necessity model
diagnostically without scheduler debit or runtime mutation. This does not create an
authoritative fourth decision.
"""
from __future__ import annotations
import argparse, gzip, json, time
from dataclasses import asdict
from pathlib import Path
import numpy as np
import torch

EXPERIMENT_ID="C192-v5e-post3-shadow-necessity"
STAGE="V5-E-POST3-SHADOW-NECESSITY"
BASE="37e2f2c818ec32f6c1281ed8ba8f58c3d07590b4"
PARENT_EXECUTION="f83ed1d60758dc1ff895b2b9c42c69d6a68c0931"
PARENT_SHA="b05cd702e9572c61a3ae981e5279c7fb096fe1078c7d65f6401f180f307c84f4"
BASE_SEEDS=(181001,181002,181003)
HEAD_SEEDS=(188001,188002,188003)
ARM="INTERNAL_SEMANTICS"
BATCH=1024
ATOL=1e-6
PRIOR_NAMES=("c191","c190","c189","c188","c187","c186","c185","c184","c183","c182",
             "c181","c180","c179","c178","c177","c176","c174")
OWN=("fold_lm/v05_benchmarks/gate_e_c192_post3_shadow_necessity.py",
     "tests_lm/test_v05_c192_post3_shadow_necessity.py",
     "tools/run_c192.ps1","tools/invoke_c192.ps1",
     "docs/experiment-ledger-addendum-c192-preregistration.md")
EXPECTED_TESTS=1533
OUTPUTS={"shadow-plan.json","parent-replay.json","episode-results.json",
         "shadow-traces.jsonl.gz","shadow-predictions.npz"}

def require(ok,msg):
    if not ok: raise ValueError(msg)

def blob(v):
    return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()

def digest(v):
    import hashlib
    return hashlib.sha256(blob(v)).hexdigest()

def packet_from_dict(d):
    from fold_lm.v05 import structured_task_input as task
    b=d["binding"]
    return task.PolicyInput(d["schema"],tuple(d["features"]),
        task.Binding(b["request_id"],b["scope_id"],tuple(b["fact_ids"]),
                     tuple(tuple(x) for x in b["reference_ids"])))

def load_parent_predictions(path):
    p=Path(path)
    require(p.is_file() and p.stat().st_size < 10_000_000,"Unexpected C191 prediction artifact size")
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

def parent_replay_metrics(observed,arrays,saved,idx):
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
    nerr=int((arrays["necessity_predictions"]!=saved["necessity_predictions"][idx]).sum())
    terr=0;nd=0.0;td=0.0
    for phase in range(3):
        active=arrays["necessity_predictions"][:,phase]>=0
        if active.any():
            nd=max(nd,float(np.max(np.abs(arrays["necessity_logits"][active,phase]
                                         -saved["necessity_logits"][idx,active,phase]))))
        tactive=arrays["target_predictions"][:,phase]>=0
        if tactive.any():
            terr+=int((arrays["target_predictions"][tactive,phase]
                       !=saved["target_predictions"][idx,tactive,phase]).sum())
            raw=torch.from_numpy(np.asarray(
                [observed[j]["phases"][phase]["packet"]["features"] for j in np.flatnonzero(tactive)],
                dtype=np.int32))
            unknown=target.missing_mask(raw).numpy()
            cur=arrays["target_logits"][tactive,phase]
            old=saved["target_logits"][idx,tactive,phase]
            td=max(td,float(np.max(np.abs(cur[unknown]-old[unknown]))))
    return dict(necessity_prediction_errors=nerr,target_prediction_errors=terr,
                necessity_max_abs_logit_difference=nd,target_max_abs_logit_difference=td)

COUNTERS=("failed","parent_replay_error","shadow_error","shadow_nonfinite",
          "logical_teacher_error","runtime_mutation","shadow_rows","runtime_reads_after_shadow")

def assess_shadow(record,shadow_pred,shadow_logits,template_id,metadata):
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
    final=record["final"];f=np.asarray(final["features"],dtype=np.int64)
    eligible=(record["status"]=="BUDGET_EXHAUSTED_AFTER_THIRD")
    if not eligible:
        return dict(failed=0,parent_replay_error=0,shadow_error=0,shadow_nonfinite=0,
                    logical_teacher_error=0,runtime_mutation=0,shadow_rows=0,runtime_reads_after_shadow=0)
    logical=c190.logical_label(final["features"],template_id,metadata)
    logical_error=int(logical!=0)
    finite=int(np.isfinite(shadow_logits).all())
    shadow_error=int(shadow_pred!=0)
    contract=(f[62],f[63],f[71])==(0,1,19) and all(f[48+4*j]==1 for j in range(4))
    runtime_mutation=int(not contract)
    vals=(logical_error,1-finite,shadow_error,runtime_mutation)
    return dict(failed=int(any(vals)),parent_replay_error=0,shadow_error=shadow_error,
                shadow_nonfinite=int(not finite),logical_teacher_error=logical_error,
                runtime_mutation=runtime_mutation,shadow_rows=1,runtime_reads_after_shadow=0)

def expected_order():
    return [(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS]

def gate(records):
    if [(r.get("base_seed"),r.get("head_seed")) for r in records]!=expected_order():
        return False
    for r in records:
        if r.get("episodes")!=9536 or r.get("parent_third_acquisitions")!=928:
            return False
        if any(type(r.get(k)) is not int or r[k]<0 for k in COUNTERS):
            return False
        if any(r[k]!=0 for k in ("failed","parent_replay_error","shadow_error","shadow_nonfinite",
                                  "logical_teacher_error","runtime_mutation","runtime_reads_after_shadow")):
            return False
        if r["shadow_rows"]!=928:
            return False
        if r.get("actual_reads") != r.get("parent_actual_reads"):
            return False
        if r.get("parent_necessity_prediction_errors")!=0 or r.get("parent_target_prediction_errors")!=0:
            return False
        if r.get("parent_necessity_max_abs_logit_difference",1)>ATOL:
            return False
        if r.get("parent_target_max_abs_logit_difference",1)>ATOL:
            return False
    return True

def manifest():
    return dict(
      experiment_id=EXPERIMENT_ID,stage=STAGE,parent_sha256=PARENT_SHA,
      acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
      base_seeds=BASE_SEEDS,head_seeds=HEAD_SEEDS,arm=ARM,
      question="after accepted C191 exhausts runtime internal budget at post3 fully observed state, does frozen C181 diagnostically classify that actual state as SUFFICIENT without scheduler debit or runtime mutation",
      changed="add one read-only shadow necessity inference after third acquisition; authoritative runtime path and budget remain unchanged",
      cohort="same 85824 coherent-world episodes; shadow probe only on 8352 accepted C191 third-acquisition states",
      selectors=9,blocks=9,episodes=85824,shadow_rows=8352,
      parent_replay="all C191 phase0/1/2 necessity and target predictions replay; finite logits <=1e-6 on active coordinates",
      shadow_input="actual final TaskView after third admission: all facts observed, internal_remaining0, acquisitions_remaining1, internal_step19",
      shadow_policy="frozen C181 necessity-only inference directly over encoded immutable TaskView; no charge_decision, no action proposal, no state refresh",
      teacher="scoring only: C190 logical necessity must be SUFFICIENT on fully observed final state",
      gate="all9 blocks: parent replay exact,928 shadow rows,zero shadow/nonfinite/logical/mutation errors,no new provider read",
      training=0,fresh_seeds=0,network_calls=0,answer_generation=0,proof_checker_calls=0,core_evidence_writes=0,
      production_runtime_modified=False,gate_e_candidate=False,outputs=sorted(OUTPUTS),
      limits="shadow inference is diagnostic and non-authoritative;does not prove runtime can execute a fourth decision;same repeatedly inspected development groups;no budget redesign,tool/provider learning,language,answer/proof or full GateE")

MANIFEST_SHA="1d103bf279bd123f7e8ada5a5094242424715da5ed3bc01adff9a1ec881d0b12"

def precheck(c191_summary,*args):
    from fold_lm.v05_benchmarks import gate_e_c191_third_acquisition_budget as parent
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(len(args)==17,"Sixteen prior summaries and repository root required")
    root=args[-1]
    p190,p189,p188,p181,p174,pins,protected=parent.precheck(args[0],*args[1:])
    require(audit.sha(c191_summary)==PARENT_SHA,"C191 summary changed")
    p=audit.read_json(c191_summary);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS"
            and parent.gate(p["records"]) and p["source_blobs"]==pins,
            "Wrong accepted C191 source/result")
    protected[str(Path(c191_summary).resolve())]=PARENT_SHA
    for a in p["artifacts"]:
        f=audit.safe_child(Path(c191_summary).resolve().parent,a["file"])
        require(f.is_file() and f.stat().st_size==a["serialized_bytes"] and audit.sha(f)==a["sha256"],
                "Changed C191 artifact:"+a["file"])
        protected[str(f.resolve())]=a["sha256"]
    pins=dict(pins)
    for name in parent.OWN:
        pins[name]=audit.git(root,"rev-parse",PARENT_EXECUTION+":"+name).decode().strip()
    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins)==121 and len(protected)==331,"Source/protected union drift")
    require(digest(manifest())==MANIFEST_SHA,"Manifest drift")
    return p,p190,p189,p188,p181,p174,pins,protected

def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c191_third_acquisition_budget as parent
    names=parent.regression_modules(root)
    require(len(names)==len(set(names))==76,"Historical regression list drift")
    return names+["tests_lm.test_v05_c192_post3_shadow_necessity"]

def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE
            and p["diagnostic_execution_valid"] is True,"Wrong/incomplete C192")
    require(p["episodes"]==85824 and len(p["records"])==9
            and p["shadow_rows"]==8352
            and len(p["source_blobs"])==121 and len(p["input_sha256"])==331
            and len(p["artifacts"])==5 and {a["file"] for a in p["artifacts"]}==OUTPUTS,
            "Workload/coverage drift")
    require(all(p[k]==0 for k in ("new_training","fresh_seeds","network_calls",
                                  "answer_generation","proof_checker_calls","core_evidence_writes"))
            and p["production_runtime_modified"] is False and p["gate_e_candidate"] is False,
            "Scope drift")
    require(p["status"]==("PASS" if gate(p["records"]) else "FAIL"),"Gate drift")

def run(*,output_dir,expected_head,**parents):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05 import structured_task_input as task
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
    from fold_lm.v05_benchmarks import gate_e_c191_third_acquisition_budget as c191

    root=Path(__file__).resolve().parents[2]
    args=tuple(parents[n+"_summary"] for n in PRIOR_NAMES[1:])+(root,)
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"Dirty tracked tree")
    guard()
    p191,p190,p189,p188,p181,p174,pins,protected=precheck(parents["c191_summary"],*args)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    artifacts=[];records=[];started=time.perf_counter()
    def record_file(name):
        f=out/name;artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,v):
        (out/name).write_bytes(blob(v));record_file(name)
    save("shadow-plan.json",dict(manifest(),source_blobs=pins))
    try:
        print("[C192] plan fixed; replay C191; read-only post3 necessity shadow; no scheduler debit/state mutation",flush=True)
        torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
        data,metadata=audit.load_data(Path(parents["c174_summary"]).resolve().parent,p174)
        raw_all=torch.from_numpy(data["features"].copy())
        valid=c189.target_teacher(data["features"],data["template_ids"],metadata)
        _,_,evfull,_,_=target.cohort_masks(raw_all,data["labels"],data["split_codes"],valid)
        full_ix=np.flatnonzero(evfull);raw=torch.from_numpy(data["features"][evfull].copy())
        expanded,source_rows,local_rows,world_codes=c190.expand_worlds(raw,full_ix)
        tids=data["template_ids"][evfull]

        pdir=Path(parents["c191_summary"]).resolve().parent
        saved=c191.load_parent_predictions(pdir/"episode-predictions.npz")
        require(np.array_equal(saved["row_indices"],source_rows)
                and np.array_equal(saved["local_rows"],local_rows)
                and np.array_equal(saved["world_codes"],world_codes),"C191 episode identity drift")

        c181_dir=Path(parents["c181_summary"]).resolve().parent
        c188_dir=Path(parents["c188_summary"]).resolve().parent
        fits={f["seed"]:f for f in p181["fit_records"] if f["arm"]==ARM}
        selector_sha={(r["base_seed"],r["head_seed"]):r["head_sha256"] for r in p188["selector_results"]}
        bases={};heads={}
        for b in BASE_SEEDS:
            bases[b]=frozen.restore_bare(c181_dir/f"probe-{b}-{ARM}.pt",b,ARM,fits[b]["final_sha256"])
            for h in HEAD_SEEDS:
                heads[b,h]=c189.restore_selector(c188_dir/f"selector-{b}-{h}.pt",b,h,selector_sha[b,h])

        c191_sources=pdir/"sources"
        providers={};endpoints={}
        for code in range(16):
            f=c191_sources/f"world-{code:02d}.json"
            expected=c190.SOURCE_FILES[f"sources/world-{code:02d}.json"]
            require(f.is_file() and audit.sha(f)==expected,"Changed protected C191 world source")
            sb=life.SourceBinding(f"C190-world-{code:02d}",expected)
            p=life.FileSnapshotProvider(f,sb);providers[code]=p;endpoints[code]=life.Endpoint(sb,p)

        shadow_pred=np.full((9,9536),-1,dtype=np.int8)
        shadow_logits=np.zeros((9,9536,2),dtype=np.float32)
        parent_replay=[]
        with gzip.open(out/"shadow-traces.jsonl.gz","wt",encoding="utf-8",newline="\n") as trace:
            for bi,b in enumerate(BASE_SEEDS):
                for hi,h in enumerate(HEAD_SEEDS):
                    idx=bi*3+hi
                    cache,_=c190.initial_policy_cache(raw,full_ix,bases[b],heads[b,h])
                    lt=torch.from_numpy(local_rows.astype(np.int64))
                    initial=dict(raw=cache["raw"][lt],
                        necessity_predictions=cache["necessity_predictions"][local_rows],
                        target_predictions=cache["target_predictions"][local_rows],
                        necessity_logits=cache["necessity_logits"][local_rows],
                        target_logits=cache["target_logits"][local_rows])
                    before_reads=sum(p.reads for p in providers.values())
                    views=c190.make_views(expanded,source_rows,world_codes,f"C192-b{b}-h{h}")
                    observed,arrays,_=c191.run_block(views,world_codes,endpoints,bases[b],heads[b,h],initial)
                    replay=parent_replay_metrics(observed,arrays,saved,idx)
                    require(replay["necessity_prediction_errors"]==0
                            and replay["target_prediction_errors"]==0
                            and replay["necessity_max_abs_logit_difference"]<=ATOL
                            and replay["target_max_abs_logit_difference"]<=ATOL,
                            "Accepted C191 parent replay drift")
                    parent_replay.append(dict(base_seed=b,head_seed=h,**replay))

                    eligible=np.asarray([r["status"]=="BUDGET_EXHAUSTED_AFTER_THIRD" for r in observed])
                    require(int(eligible.sum())==928,"C191 post3 cohort drift")
                    final_packets=[packet_from_dict(observed[j]["final"]) for j in np.flatnonzero(eligible)]
                    final_views=[task.decode(p) for p in final_packets]
                    raw3,roundtrip=c189.encode_views(final_views)
                    require(all(asdict(roundtrip[k])==observed[j]["final"]
                                for k,j in enumerate(np.flatnonzero(eligible))),
                            "Shadow encode mutated/rebound final state")
                    before_packets=[asdict(task.encode(v)) for v in final_views]
                    sp,sz,m=c189.necessity_predict(bases[b],raw3,batch=BATCH)
                    after_packets=[asdict(task.encode(v)) for v in final_views]
                    require(before_packets==after_packets,"Shadow inference mutated TaskView")
                    shadow_pred[idx,eligible]=sp;shadow_logits[idx,eligible]=sz

                    scores=[];ei=0
                    for j,rec in enumerate(observed):
                        if eligible[j]:
                            score=assess_shadow(rec,int(sp[ei]),sz[ei],int(tids[int(local_rows[j])]),metadata);ei+=1
                        else:
                            score=assess_shadow(rec,-1,np.asarray([0.,0.]),int(tids[int(local_rows[j])]),metadata)
                        score["parent_replay_error"]=int(any(replay[k] for k in (
                            "necessity_prediction_errors","target_prediction_errors"))
                            or replay["necessity_max_abs_logit_difference"]>ATOL
                            or replay["target_max_abs_logit_difference"]>ATOL)
                        score["failed"]=int(score["failed"] or score["parent_replay_error"])
                        scores.append(score)
                        if eligible[j]:
                            trace.write(json.dumps(dict(base_seed=b,head_seed=h,
                                source_row=int(source_rows[j]),world_code=int(world_codes[j]),
                                score=score,final=rec["final"],shadow_prediction=int(shadow_pred[idx,j]),
                                shadow_logits=shadow_logits[idx,j].tolist()),
                                sort_keys=True,separators=(",",":"),allow_nan=False)+"\n")
                    after_reads=sum(p.reads for p in providers.values())
                    totals={k:sum(s[k] for s in scores) for k in COUNTERS}
                    parent_rec=p191["records"][idx]
                    rec=dict(base_seed=b,head_seed=h,episodes=9536,
                        parent_third_acquisitions=parent_rec["third_provider_calls"],
                        parent_actual_reads=parent_rec["actual_reads"],
                        actual_reads=after_reads-before_reads,
                        parent_necessity_prediction_errors=replay["necessity_prediction_errors"],
                        parent_target_prediction_errors=replay["target_prediction_errors"],
                        parent_necessity_max_abs_logit_difference=replay["necessity_max_abs_logit_difference"],
                        parent_target_max_abs_logit_difference=replay["target_max_abs_logit_difference"],
                        **totals)
                    records.append(rec)
                    print(f"[C192] block={len(records)}/9 base={b} head={h} failed={rec['failed']} "
                          f"shadow={rec['shadow_rows']} shadow_err={rec['shadow_error']} reads={rec['actual_reads']}",flush=True)

        record_file("shadow-traces.jsonl.gz")
        np.savez_compressed(out/"shadow-predictions.npz",predictions=shadow_pred,logits=shadow_logits,
            row_indices=source_rows.astype("<i4"),local_rows=local_rows.astype("<i4"),
            world_codes=world_codes.astype(np.int8))
        record_file("shadow-predictions.npz")
        save("parent-replay.json",parent_replay);save("episode-results.json",records)
        guard();precheck(parents["c191_summary"],*args)
        for f,hsh in protected.items():require(audit.sha(f)==hsh,"Protected input changed:"+f)
        for a in artifacts:require(audit.sha(out/a["file"])==a["sha256"],"Output changed:"+a["file"])
        totals={k:sum(r[k] for r in records) for k in COUNTERS}
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status="PASS" if gate(records) else "FAIL",diagnostic_execution_valid=True,
            C191_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,
            artifacts=artifacts,records=records,parent_replay=parent_replay,totals=totals,
            episodes=85824,shadow_rows=totals["shadow_rows"],
            actual_file_reads=sum(p.reads for p in providers.values()),
            provider_bytes_read=sum(p.bytes_read for p in providers.values()),
            new_training=0,fresh_seeds=0,network_calls=0,answer_generation=0,
            proof_checker_calls=0,core_evidence_writes=0,
            production_runtime_modified=False,gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=["shadow inference is read-only and not an authoritative scheduler decision",
                "same repeatedly inspected development groups",
                "fixed RETRIEVE/local provider;no budget redesign/language/answer/proof/GateE"])
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C192] source/output preservation checked",flush=True)
        print("=== C192 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
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
