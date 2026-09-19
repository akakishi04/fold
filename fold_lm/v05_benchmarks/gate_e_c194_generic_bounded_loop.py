"""C194: generic bounded loop equivalence against accepted C193.

Diagnostic-only Gate-E development experiment. Frozen C181/C188 checkpoints, budget13,
coherent worlds, C172/C173 runtime, teachers and cohort are held. The only changed variable
is orchestration: C193's hand-unrolled phase0/1/2/3 control is replaced by one state-driven
bounded decide -> optional acquire -> reobserve loop.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, time
from dataclasses import asdict
from pathlib import Path
import numpy as np
import torch

EXPERIMENT_ID="C194-v5e-generic-bounded-loop-equivalence"
STAGE="V5-E-GENERIC-BOUNDED-LOOP-EQUIVALENCE"
BASE="d69d9bf7238d241eb27b266467fcfe41fa0d5661"
PARENT_EXECUTION="7649392a506530de2ee881d9914148a4e88b197c"
PARENT_SHA="660c4799c894ee2b3355d024fc446c5ff14ff69cad41c41b2b6b255ed4aa7416"
BASE_SEEDS=(181001,181002,181003)
HEAD_SEEDS=(188001,188002,188003)
ARM="INTERNAL_SEMANTICS"
BATCH=1024
ATOL=1e-6
MAX_ACQUISITIONS=3
MAX_DECISIONS=MAX_ACQUISITIONS+1
PRIOR_NAMES=("c193","c192","c191","c190","c189","c188","c187","c186","c185","c184",
             "c183","c182","c181","c180","c179","c178","c177","c176","c174")
OWN=("fold_lm/v05_benchmarks/gate_e_c194_generic_bounded_loop.py",
     "tests_lm/test_v05_c194_generic_bounded_loop.py",
     "tools/run_c194.ps1","tools/invoke_c194.ps1",
     "docs/experiment-ledger-addendum-c194-preregistration.md")
EXPECTED_TESTS=1581
OUTPUTS={"generic-loop-plan.json","parent-replay.json","episode-results.json",
         "episode-traces.jsonl.gz","episode-predictions.npz"}

def require(ok,msg):
    if not ok: raise ValueError(msg)

def blob(v):
    return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()

def digest(v):
    return hashlib.sha256(blob(v)).hexdigest()

def load_parent_predictions(path):
    p=Path(path)
    require(p.is_file() and p.stat().st_size < 10_000_000,"Unexpected C193 prediction artifact size")
    with np.load(p,allow_pickle=False) as z:
        expected={"necessity_predictions","necessity_logits","target_predictions","target_logits",
                  "row_indices","local_rows","world_codes"}
        require(set(z.files)==expected,"C193 prediction schema drift")
        out={k:z[k].copy() for k in z.files}
    require(out["necessity_predictions"].shape==(9,9536,4)
            and out["necessity_logits"].shape==(9,9536,4,2)
            and out["target_predictions"].shape==(9,9536,3)
            and out["target_logits"].shape==(9,9536,3,4)
            and out["row_indices"].shape==(9536,)
            and out["local_rows"].shape==(9536,)
            and out["world_codes"].shape==(9536,),
            "C193 prediction array drift")
    return out

def run_loop(views,world_codes,endpoints,base,selector,initial):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05 import structured_action_runtime as action
    from fold_lm.v05 import structured_task_input as task
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190

    require(len(views)==len(world_codes)>0,"Episode/world alignment required")
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{"RETRIEVE":endpoints[int(code)]},
                                  max_dispatches=MAX_ACQUISITIONS)
            for v,code in zip(views,world_codes,strict=True)]
    n=len(views)
    records=[dict(initial=asdict(task.encode(v)),phases=[],acquisitions=[],
                  decision_charges=0,status="UNRESOLVED",world_code=int(code))
             for v,code in zip(views,world_codes,strict=True)]
    n_pred=np.full((n,MAX_DECISIONS),-1,dtype=np.int8)
    n_logits=np.zeros((n,MAX_DECISIONS,2),dtype=np.float32)
    t_pred=np.full((n,MAX_ACQUISITIONS),-1,dtype=np.int8)
    t_logits=np.full((n,MAX_ACQUISITIONS,4),-np.inf,dtype=np.float32)
    meter=dict(rows=0,forward_calls=0,cell_calls=0)

    active=list(range(n))
    iteration=0
    while active:
        require(iteration < MAX_DECISIONS,"Generic loop exceeded derived decision bound")
        charged=[];exhausted=[]
        for i in active:
            if driver.charge_decision(owners[i]):
                charged.append(i)
            else:
                exhausted.append(i)
        for i in exhausted:
            records[i]["status"]="BUDGET_EXHAUSTED"
        active=charged
        if not active:
            break

        raw,packets=c189.encode_views([owners[i].state.view for i in active])
        any_missing=any(any(f.status=="UNOBSERVED" for f in owners[i].state.view.facts)
                        for i in active)
        if iteration==0:
            require(torch.equal(raw,initial["raw"]),"Generic loop initial cache mapping drift")
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
            for k in meter: meter[k]+=m[k]
        else:
            p,z,m=c189.necessity_predict(base,raw,batch=BATCH)
            for k in meter: meter[k]+=m[k]
            t=np.full(len(active),-1,dtype=np.int8)
            tz=np.full((len(active),4),-np.inf,dtype=np.float32)

        next_active=[]
        for j,i in enumerate(active):
            n_pred[i,iteration]=p[j];n_logits[i,iteration]=z[j]
            phase=dict(iteration=iteration,packet=asdict(packets[j]),
                       necessity_prediction=int(p[j]))
            records[i]["decision_charges"]+=1
            if any_missing:
                require(iteration < MAX_ACQUISITIONS,
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
            records[i]["acquisitions"].append(c190.acquire(owners[i],target_index))
            next_active.append(i)

        active=next_active
        iteration+=1

    for i,o in enumerate(owners):
        records[i]["final"]=asdict(task.encode(o.state.view))
        records[i]["receipts"]=[asdict(r) for r in o.receipts]
        records[i]["pending"]=asdict(o.state.pending) if o.state.pending else None
        records[i]["runtime_terminal"]=o.state.terminal
    return records,dict(necessity_predictions=n_pred,necessity_logits=n_logits,
                        target_predictions=t_pred,target_logits=t_logits),meter

COUNTERS=("failed","necessity_error","target_error","selected_observed","repeated_target",
          "acquisition_error","contract_error","first_reads","second_reads","third_reads",
          "final_decision_rows","final_decision_error","parent_replay_error",
          "parent_block_mismatch")

def parent_replay_metrics(arrays,parent_arrays):
    nerr=int((arrays["necessity_predictions"]!=parent_arrays["necessity_predictions"]).sum())
    terr=int((arrays["target_predictions"]!=parent_arrays["target_predictions"]).sum())
    nmask=parent_arrays["necessity_predictions"]>=0
    tmask=parent_arrays["target_predictions"]>=0
    ndelta=float(np.max(np.abs(
        arrays["necessity_logits"][nmask]-parent_arrays["necessity_logits"][nmask]))) if nmask.any() else 0.0
    finite=np.isfinite(parent_arrays["target_logits"]) & np.repeat(tmask[:,:,None],4,axis=2)
    tdelta=float(np.max(np.abs(
        arrays["target_logits"][finite]-parent_arrays["target_logits"][finite]))) if finite.any() else 0.0
    return dict(necessity_prediction_errors=nerr,target_prediction_errors=terr,
                necessity_max_abs_logit_difference=ndelta,target_max_abs_logit_difference=tdelta)

def expected_order():
    return [(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS]

def gate(records):
    if [(r.get("base_seed"),r.get("head_seed")) for r in records]!=expected_order():
        return False
    for r in records:
        if r.get("episodes")!=9536: return False
        if any(type(r.get(k)) is not int or r[k]<0 for k in COUNTERS): return False
        if any(r[k]!=0 for k in ("failed","necessity_error","target_error","selected_observed",
                                  "repeated_target","acquisition_error","contract_error",
                                  "final_decision_error","parent_replay_error","parent_block_mismatch")):
            return False
        if r["first_reads"]!=9536: return False
        if not (0<=r["third_reads"]==r["final_decision_rows"]<=r["second_reads"]<=r["first_reads"]):
            return False
        if r["third_reads"]<=0: return False
        if r.get("actual_reads")!=r["first_reads"]+r["second_reads"]+r["third_reads"]:
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
      question="can one generic bounded decide-acquire-reobserve loop reproduce accepted C193 exactly without phase1/phase2/phase3 orchestration branches",
      changed="hand-unrolled C193 phase orchestration replaced by one state-driven bounded loop; model,data,budget13,runtime and source worlds unchanged",
      loop_rule="while unresolved: charge one decision; if any active row has an unobserved fact evaluate combined necessity+target for the active batch, otherwise necessity-only; SUFFICIENT stops; NEEDS with a legal target acquires then re-enters",
      initial_rule="iteration0 reuses the same unique-state budget13 memoized frozen output used by C193; subsequent iterations are state-driven",
      bound="max_dispatches3 implies at most4 learned decisions; the bound is derived from acquisition capacity, not a phase-specific stopping branch",
      cohort="same1768 PILOT NEEDS missing2/3 expanded to9536 coherent worlds per selector",
      episodes=85824,blocks=9,selectors=9,
      parent_replay="C193 necessity/target predictions must match exactly; active finite logit coordinates <=1e-6; read-depth/final-decision counts must match per block",
      gate="all9 blocks zero scientific errors,parent replay errors,parent block mismatches; exact first/second/third/final rows and actual reads; all episodes terminate SUFFICIENT",
      training=0,fresh_seeds=0,network_calls=0,answer_generation=0,proof_checker_calls=0,core_evidence_writes=0,
      production_runtime_modified=False,gate_e_candidate=False,outputs=sorted(OUTPUTS),
      limits="development family;generic loop remains benchmark/runtime candidate not production adoption;no learned resource policy,tool/provider choice,renaming holdout,language,answer/proof or full GateE")

MANIFEST_SHA="046659d7103d327e8b75e13258b597db4813fb0f7c844f35e444b54b0ea21d99"

def precheck(c193_summary,*args):
    from fold_lm.v05_benchmarks import gate_e_c193_budget13_authoritative_closure as parent
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(len(args)==19,"Eighteen prior summaries and repository root required")
    root=args[-1]
    p192,p191,p190,p189,p188,p181,p174,pins,protected=parent.precheck(args[0],*args[1:])
    require(audit.sha(c193_summary)==PARENT_SHA,"C193 summary changed")
    p=audit.read_json(c193_summary);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS"
            and parent.gate(p["records"]) and p["source_blobs"]==pins,
            "Wrong accepted C193 source/result")
    protected[str(Path(c193_summary).resolve())]=PARENT_SHA
    for a in p["artifacts"]:
        f=audit.safe_child(Path(c193_summary).resolve().parent,a["file"])
        require(f.is_file() and f.stat().st_size==a["serialized_bytes"] and audit.sha(f)==a["sha256"],
                "Changed C193 artifact:"+a["file"])
        protected[str(f.resolve())]=a["sha256"]
    pins=dict(pins)
    for name in parent.OWN:
        pins[name]=audit.git(root,"rev-parse",PARENT_EXECUTION+":"+name).decode().strip()
    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins)==131 and len(protected)==352,"Source/protected union drift")
    require(digest(manifest())==MANIFEST_SHA,"Manifest drift")
    return p,p192,p191,p190,p189,p188,p181,p174,pins,protected

def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c193_budget13_authoritative_closure as parent
    names=parent.regression_modules(root)
    require(len(names)==len(set(names))==78,"Historical regression list drift")
    return names+["tests_lm.test_v05_c194_generic_bounded_loop"]

def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE
            and p["diagnostic_execution_valid"] is True,"Wrong/incomplete C194")
    require(p["episodes"]==85824 and len(p["records"])==9
            and len(p["source_blobs"])==131 and len(p["input_sha256"])==352
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
    from fold_lm.v05_benchmarks import gate_e_c193_budget13_authoritative_closure as parent

    root=Path(__file__).resolve().parents[2]
    args=tuple(parents[n+"_summary"] for n in PRIOR_NAMES[1:])+(root,)
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"Dirty tracked tree")
    guard()
    p193,p192,p191,p190,p189,p188,p181,p174,pins,protected=precheck(parents["c193_summary"],*args)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    artifacts=[];records=[];started=time.perf_counter()
    def record_file(name):
        f=out/name;artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,v):
        (out/name).write_bytes(blob(v));record_file(name)
    save("generic-loop-plan.json",dict(manifest(),source_blobs=pins))
    try:
        print("[C194] plan fixed; generic state-driven bounded loop; exact C193 replay required",flush=True)
        torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
        data,metadata=audit.load_data(Path(parents["c174_summary"]).resolve().parent,p174)
        raw_all=torch.from_numpy(data["features"].copy())
        valid=c189.target_teacher(data["features"],data["template_ids"],metadata)
        _,_,evfull,_,_=target.cohort_masks(raw_all,data["labels"],data["split_codes"],valid)
        full_ix=np.flatnonzero(evfull)
        raw12=torch.from_numpy(data["features"][evfull].copy())
        raw13=parent.budget13(raw12)
        expanded12,source_rows,local_rows,world_codes=c190.expand_worlds(raw12,full_ix)
        expanded13=parent.budget13(expanded12)
        tids=data["template_ids"][evfull]

        parent_dir=Path(parents["c193_summary"]).resolve().parent
        saved=load_parent_predictions(parent_dir/"episode-predictions.npz")
        require(np.array_equal(saved["row_indices"],source_rows)
                and np.array_equal(saved["local_rows"],local_rows)
                and np.array_equal(saved["world_codes"],world_codes),
                "C193 episode identity drift")

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
        parent_replay=[]
        with gzip.open(out/"episode-traces.jsonl.gz","wt",encoding="utf-8",newline="\n") as trace:
            for bi,b in enumerate(BASE_SEEDS):
                for hi,h in enumerate(HEAD_SEEDS):
                    idx=bi*3+hi
                    cache,_=parent.initial_policy_cache(raw13,full_ix,bases[b],heads[b,h])
                    lt=torch.from_numpy(local_rows.astype(np.int64))
                    initial=dict(raw=cache["raw"][lt],
                        necessity_predictions=cache["necessity_predictions"][local_rows],
                        target_predictions=cache["target_predictions"][local_rows],
                        necessity_logits=cache["necessity_logits"][local_rows],
                        target_logits=cache["target_logits"][local_rows])

                    before=sum(p.reads for p in providers.values())
                    views=c190.make_views(expanded13,source_rows,world_codes,f"C194-b{b}-h{h}")
                    observed,arrays,_=run_loop(views,world_codes,endpoints,bases[b],heads[b,h],initial)
                    dense["necessity_predictions"][idx]=arrays["necessity_predictions"]
                    dense["necessity_logits"][idx]=arrays["necessity_logits"]
                    dense["target_predictions"][idx]=arrays["target_predictions"]
                    dense["target_logits"][idx]=arrays["target_logits"]

                    parent_arrays={k:saved[k][idx] for k in (
                        "necessity_predictions","necessity_logits","target_predictions","target_logits")}
                    replay=parent_replay_metrics(arrays,parent_arrays)
                    parent_replay.append(dict(base_seed=b,head_seed=h,**replay))
                    replay_error=int(replay["necessity_prediction_errors"]!=0
                        or replay["target_prediction_errors"]!=0
                        or replay["necessity_max_abs_logit_difference"]>ATOL
                        or replay["target_max_abs_logit_difference"]>ATOL)

                    scores=[]
                    for j,rec in enumerate(observed):
                        score=parent.assess(rec,int(tids[int(local_rows[j])]),metadata,
                                            c190.WORLD_BITS[int(world_codes[j])])
                        score["parent_replay_error"]=replay_error
                        score["parent_block_mismatch"]=0
                        score["failed"]=int(score["failed"] or replay_error)
                        scores.append(score)
                        trace.write(json.dumps(dict(base_seed=b,head_seed=h,
                            source_row=int(source_rows[j]),world_code=int(world_codes[j]),
                            score=score,trace=rec),
                            sort_keys=True,separators=(",",":"),allow_nan=False)+"\n")

                    totals={k:sum(s[k] for s in scores) for k in parent.COUNTERS}
                    reads=sum(p.reads for p in providers.values())-before
                    parent_rec=p193["records"][idx]
                    block_mismatch=int(any((
                        totals["first_reads"]!=parent_rec["first_reads"],
                        totals["second_reads"]!=parent_rec["second_reads"],
                        totals["third_reads"]!=parent_rec["third_reads"],
                        totals["final_decision_rows"]!=parent_rec["final_decision_rows"],
                        reads!=parent_rec["actual_reads"])))
                    if block_mismatch:
                        for score in scores:
                            score["parent_block_mismatch"]=1
                            score["failed"]=1
                    rec=dict(base_seed=b,head_seed=h,episodes=9536,actual_reads=reads,
                        parent_necessity_prediction_errors=replay["necessity_prediction_errors"],
                        parent_target_prediction_errors=replay["target_prediction_errors"],
                        parent_necessity_max_abs_logit_difference=replay["necessity_max_abs_logit_difference"],
                        parent_target_max_abs_logit_difference=replay["target_max_abs_logit_difference"],
                        parent_replay_error=int(replay_error*9536),
                        parent_block_mismatch=int(block_mismatch*9536),
                        **totals)
                    rec["failed"]+=int(replay_error*9536)+int(block_mismatch*9536)
                    records.append(rec)
                    print(f"[C194] block={len(records)}/9 base={b} head={h} failed={rec['failed']} "
                          f"reads={reads} second={rec['second_reads']} third={rec['third_reads']} "
                          f"final={rec['final_decision_rows']} replay_n={replay['necessity_prediction_errors']} "
                          f"replay_t={replay['target_prediction_errors']}",flush=True)

        record_file("episode-traces.jsonl.gz")
        np.savez_compressed(out/"episode-predictions.npz",**dense,row_indices=source_rows.astype("<i4"),
                            local_rows=local_rows.astype("<i4"),world_codes=world_codes.astype(np.int8))
        record_file("episode-predictions.npz")
        save("parent-replay.json",parent_replay);save("episode-results.json",records)

        guard();precheck(parents["c193_summary"],*args)
        for f,hsh in protected.items(): require(audit.sha(f)==hsh,"Protected input changed:"+f)
        for a in artifacts: require(audit.sha(out/a["file"])==a["sha256"],"Output changed:"+a["file"])

        totals={k:sum(r[k] for r in records) for k in COUNTERS}
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status="PASS" if gate(records) else "FAIL",diagnostic_execution_valid=True,
            C193_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,
            artifacts=artifacts,records=records,parent_replay=parent_replay,totals=totals,
            episodes=85824,actual_file_reads=sum(p.reads for p in providers.values()),
            provider_bytes_read=sum(p.bytes_read for p in providers.values()),
            new_training=0,fresh_seeds=0,network_calls=0,answer_generation=0,
            proof_checker_calls=0,core_evidence_writes=0,
            production_runtime_modified=False,gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=["same repeatedly inspected development family",
                "generic loop is benchmark/runtime candidate, not production adoption",
                "no learned resource policy/tool-provider choice/independent holdout/language/answer/proof/GateE"])
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C194] source/output preservation checked",flush=True)
        print("=== C194 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
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
