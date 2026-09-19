"""C193: authoritative post-third final decision with only internal budget 12 -> 13.

Diagnostic-only Gate-E development experiment. The only experimental intervention is the
initial TaskView internal_remaining coordinate: 12 becomes 13. Frozen C181/C188 checkpoints,
cohort, coherent source worlds, C172/C173 runtime, teachers and all other resources are held.
The full learned path is rerun because internal_remaining is model-visible.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, time
from dataclasses import asdict
from pathlib import Path
import numpy as np
import torch

EXPERIMENT_ID="C193-v5e-budget13-authoritative-closure"
STAGE="V5-E-BUDGET13-AUTHORITATIVE-CLOSURE"
BASE="c7a577bb0b82ffaf78c81b1a973ab1c3a9409bc8"
PARENT_EXECUTION="583e7be99b3837690948634d9c8fc89967a5f573"
PARENT_SHA="05d1b0b7783ca8c3e0313a32172f8f7068ec0c9542042e7cfe2246bb81446ee1"
BASE_SEEDS=(181001,181002,181003)
HEAD_SEEDS=(188001,188002,188003)
ARM="INTERNAL_SEMANTICS"
BATCH=1024
PRIOR_NAMES=("c192","c191","c190","c189","c188","c187","c186","c185","c184","c183",
             "c182","c181","c180","c179","c178","c177","c176","c174")
OWN=("fold_lm/v05_benchmarks/gate_e_c193_budget13_authoritative_closure.py",
     "tests_lm/test_v05_c193_budget13_authoritative_closure.py",
     "tools/run_c193.ps1","tools/invoke_c193.ps1",
     "docs/experiment-ledger-addendum-c193-preregistration.md")
EXPECTED_TESTS=1557
OUTPUTS={"budget13-plan.json","episode-results.json","episode-traces.jsonl.gz",
         "episode-predictions.npz"}

def require(ok,msg):
    if not ok: raise ValueError(msg)

def blob(v):
    return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()

def digest(v):
    return hashlib.sha256(blob(v)).hexdigest()

def budget13(raw):
    require(isinstance(raw,torch.Tensor) and raw.dtype==torch.int32 and raw.ndim==2
            and raw.shape[1]==72 and len(raw)>0,"Aligned int32 raw rows required")
    out=raw.clone()
    require(bool(torch.all(out[:,62]==12)) and bool(torch.all(out[:,63]==4))
            and bool(torch.all(out[:,71]==7)),"Expected original C174 resource coordinates")
    out[:,62]=13
    changed=torch.nonzero(out!=raw,as_tuple=False)
    require(len(changed)==len(raw) and bool(torch.all(changed[:,1]==62)),
            "Budget intervention changed more than internal_remaining")
    return out

def initial_policy_cache(raw13,row_indices,base,selector):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05 import structured_action_runtime as action
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
    require(len(raw13)==len(row_indices)>0,"Unique initial budget13 cohort required")
    views=driver.make_views(raw13,row_indices,driver.LAYOUTS[0],"C193-initial-budget13")
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{},max_dispatches=3) for v in views]
    require(all(driver.charge_decision(o) for o in owners),"Initial budget13 decision debit failed")
    charged,_=c189.encode_views([o.state.view for o in owners])
    require(bool(torch.all(charged[:,62]==12)) and bool(torch.all(charged[:,71]==8)),
            "Budget13 initial debit coordinates drift")
    p,t,z,tz,m=c189.combined_predict(base,selector,charged,batch=BATCH)
    require(p.shape==t.shape==(len(raw13),) and z.shape==(len(raw13),2)
            and tz.shape==(len(raw13),4),"Initial budget13 output shape drift")
    return dict(raw=charged,necessity_predictions=p,target_predictions=t,
                necessity_logits=z,target_logits=tz),m

def run_block(views,world_codes,endpoints,base,selector,initial):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05 import structured_action_runtime as action
    from fold_lm.v05 import structured_task_input as task
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190

    require(len(views)==len(world_codes)>0,"Episode/world alignment required")
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{"RETRIEVE":endpoints[int(code)]},
                                  max_dispatches=3)
            for v,code in zip(views,world_codes,strict=True)]
    n=len(views)
    records=[dict(initial=asdict(task.encode(v)),phases=[],acquisitions=[],
                  decision_charges=0,status="UNRESOLVED",world_code=int(code))
             for v,code in zip(views,world_codes,strict=True)]
    n_pred=np.full((n,4),-1,dtype=np.int8)
    n_logits=np.zeros((n,4,2),dtype=np.float32)
    t_pred=np.full((n,3),-1,dtype=np.int8)
    t_logits=np.full((n,3,4),-np.inf,dtype=np.float32)
    meter=dict(rows=0,forward_calls=0,cell_calls=0)

    active=[i for i,o in enumerate(owners) if driver.charge_decision(o)]
    require(len(active)==n,"Initial decision budget unexpectedly exhausted")
    raw0,packets0=c189.encode_views([owners[i].state.view for i in active])
    require(torch.equal(raw0,initial["raw"]),"Budget13 initial cache mapping drift")
    p0=np.asarray(initial["necessity_predictions"]);t0=np.asarray(initial["target_predictions"])
    z0=np.asarray(initial["necessity_logits"]);tz0=np.asarray(initial["target_logits"])
    first=[]
    for j,i in enumerate(active):
        n_pred[i,0]=p0[j];n_logits[i,0]=z0[j];t_pred[i,0]=t0[j];t_logits[i,0]=tz0[j]
        records[i]["decision_charges"]+=1
        records[i]["phases"].append(dict(phase=0,packet=asdict(packets0[j]),
            necessity_prediction=int(p0[j]),target_prediction=int(t0[j])))
        if p0[j]==1:
            records[i]["acquisitions"].append(c190.acquire(owners[i],int(t0[j])));first.append(i)
        else: records[i]["status"]="SUFFICIENT_CLASSIFICATION"

    phase1=[i for i in first if driver.charge_decision(owners[i])]
    require(len(phase1)==len(first),"Phase1 budget unexpectedly exhausted")
    second=[]
    if phase1:
        raw1,packets1=c189.encode_views([owners[i].state.view for i in phase1])
        p1,t1,z1,tz1,m1=c189.combined_predict(base,selector,raw1,batch=BATCH)
        for k in meter: meter[k]+=m1[k]
        for j,i in enumerate(phase1):
            n_pred[i,1]=p1[j];n_logits[i,1]=z1[j];t_pred[i,1]=t1[j];t_logits[i,1]=tz1[j]
            records[i]["decision_charges"]+=1
            records[i]["phases"].append(dict(phase=1,packet=asdict(packets1[j]),
                necessity_prediction=int(p1[j]),target_prediction=int(t1[j])))
            if p1[j]==1:
                records[i]["acquisitions"].append(c190.acquire(owners[i],int(t1[j])));second.append(i)
            else: records[i]["status"]="SUFFICIENT_CLASSIFICATION"

    phase2=[i for i in second if driver.charge_decision(owners[i])]
    require(len(phase2)==len(second),"Phase2 budget unexpectedly exhausted")
    third=[]
    if phase2:
        raw2,packets2=c189.encode_views([owners[i].state.view for i in phase2])
        p2,t2,z2,tz2,m2=c189.combined_predict(base,selector,raw2,batch=BATCH)
        for k in meter: meter[k]+=m2[k]
        for j,i in enumerate(phase2):
            n_pred[i,2]=p2[j];n_logits[i,2]=z2[j];t_pred[i,2]=t2[j];t_logits[i,2]=tz2[j]
            records[i]["decision_charges"]+=1
            records[i]["phases"].append(dict(phase=2,packet=asdict(packets2[j]),
                necessity_prediction=int(p2[j]),target_prediction=int(t2[j])))
            if p2[j]==1:
                records[i]["acquisitions"].append(c190.acquire(owners[i],int(t2[j])));third.append(i)
            else: records[i]["status"]="SUFFICIENT_CLASSIFICATION"

    phase3=[i for i in third if driver.charge_decision(owners[i])]
    require(len(phase3)==len(third),"Final authoritative decision budget unexpectedly exhausted")
    if phase3:
        raw3,packets3=c189.encode_views([owners[i].state.view for i in phase3])
        p3,z3,m3=c189.necessity_predict(base,raw3,batch=BATCH)
        for k in meter: meter[k]+=m3[k]
        for j,i in enumerate(phase3):
            n_pred[i,3]=p3[j];n_logits[i,3]=z3[j]
            records[i]["decision_charges"]+=1
            records[i]["phases"].append(dict(phase=3,packet=asdict(packets3[j]),
                necessity_prediction=int(p3[j])))
            records[i]["status"]="SUFFICIENT_CLASSIFICATION" if p3[j]==0 else "UNRESOLVED"

    for i,o in enumerate(owners):
        records[i]["final"]=asdict(task.encode(o.state.view))
        records[i]["receipts"]=[asdict(r) for r in o.receipts]
        records[i]["pending"]=asdict(o.state.pending) if o.state.pending else None
        records[i]["runtime_terminal"]=o.state.terminal
    return records,dict(necessity_predictions=n_pred,necessity_logits=n_logits,
                        target_predictions=t_pred,target_logits=t_logits),meter

COUNTERS=("failed","necessity_error","target_error","selected_observed","repeated_target",
          "acquisition_error","contract_error","first_reads","second_reads","third_reads",
          "final_decision_rows","final_decision_error")

def assess(record,template_id,metadata,world_bits):
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
    ph=record["phases"];acq=record["acquisitions"];initial=record["initial"];final=record["final"]
    necessity_error=target_error=selected_observed=repeated=acq_error=final_error=0
    prior_targets=[]
    expected_need=[]
    for q in range(min(3,len(ph))):
        packet=ph[q]["packet"];pred=ph[q]["necessity_prediction"]
        expected=c190.logical_label(packet["features"],template_id,metadata)
        expected_need.append(expected)
        necessity_error+=int(pred!=expected)
        if expected==1:
            t=ph[q].get("target_prediction",-1)
            valid=c190.teacher_for(packet["features"],template_id,metadata)
            target_error+=int(not (0<=t<4 and bool(valid[t])))
            selected_observed+=int(0<=t<4 and packet["features"][48+4*t]==1)
            repeated+=int(t in prior_targets)
            prior_targets.append(t)

    should_acq=sum(int(x==1) for x in expected_need)
    def acq_ok(a,index):
        if a is None or not (0<=index<4): return False
        d=a["dispatch"]
        return (d is not None and a["input_index"]==index and a["action"]["status"]=="PENDING"
            and a["action"]["reason"]=="ACQUISITION_RESERVED" and d["status"]=="PUBLISHED"
            and d["reason"]=="OBSERVATION_ADMITTED" and d["provider_calls"]==1
            and d["fact_publications"]==1 and d["internal_charged"]==2)
    for q in range(should_acq):
        t=prior_targets[q] if q<len(prior_targets) else -1
        a=acq[q] if q<len(acq) else None
        ok=acq_ok(a,t)
        if ok:
            ok=record["receipts"][q]["fact_id"]==a["fact_id"] and record["receipts"][q]["value"]==world_bits[t]
        acq_error+=int(not ok)
    acq_error+=abs(len(acq)-should_acq)

    third=should_acq==3
    if third:
        if len(ph)<4:
            final_error+=1
        else:
            expected3=c190.logical_label(ph[3]["packet"]["features"],template_id,metadata)
            final_error+=int(expected3!=0 or ph[3]["necessity_prediction"]!=0)
    final_features=np.asarray(final["features"],dtype=np.int64)
    expected_decisions=1+should_acq
    # initial decision plus one re-decision after each acquisition
    expected_internal=13-expected_decisions-3*should_acq
    expected_step=7+expected_decisions+3*should_acq
    expected_acq_remaining=4-should_acq
    structural=(record["pending"] is None and record["runtime_terminal"] is None
        and record["decision_charges"]==expected_decisions
        and final_features[62]==expected_internal
        and final_features[63]==expected_acq_remaining
        and final_features[71]==expected_step
        and len(record["receipts"])==should_acq
        and record["status"]=="SUFFICIENT_CLASSIFICATION")
    if third:
        structural=structural and expected_internal==0 and expected_step==20
        structural=structural and all(final_features[48+4*j]==1 for j in range(4))
    contract=int(not structural)
    vals=(necessity_error,target_error,selected_observed,repeated,acq_error,final_error,contract)
    return dict(failed=int(any(vals)),necessity_error=int(necessity_error),
        target_error=int(target_error),selected_observed=int(selected_observed),
        repeated_target=int(repeated),acquisition_error=int(acq_error),
        contract_error=contract,first_reads=int(should_acq>=1),
        second_reads=int(should_acq>=2),third_reads=int(should_acq>=3),
        final_decision_rows=int(third),final_decision_error=int(final_error))

def expected_order():
    return [(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS]

def gate(records):
    if [(r.get("base_seed"),r.get("head_seed")) for r in records]!=expected_order(): return False
    for r in records:
        if r.get("episodes")!=9536: return False
        if any(type(r.get(k)) is not int or r[k]<0 for k in COUNTERS): return False
        if any(r[k]!=0 for k in ("failed","necessity_error","target_error","selected_observed",
                                  "repeated_target","acquisition_error","contract_error",
                                  "final_decision_error")): return False
        if r["first_reads"]!=9536: return False
        if not (0<=r["third_reads"]==r["final_decision_rows"]<=r["second_reads"]<=r["first_reads"]):
            return False
        if r["third_reads"]<=0: return False
        if r.get("actual_reads")!=r["first_reads"]+r["second_reads"]+r["third_reads"]: return False
    return True

def manifest():
    return dict(
      experiment_id=EXPERIMENT_ID,stage=STAGE,parent_sha256=PARENT_SHA,
      acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
      base_seeds=BASE_SEEDS,head_seeds=HEAD_SEEDS,arm=ARM,
      question="with only initial internal budget changed12->13, does the full frozen learned runtime remain correct and execute authoritative post3 SUFFICIENT closure",
      changed="TaskView internal_remaining initial coordinate 12->13 only",
      held="same C174 cohort,9 frozen C181/C188 selector pairs,16 coherent worlds,C172/C173,all other resources,teachers and runtime semantics",
      cohort="same1768 PILOT NEEDS missing2/3 expanded to9536 coherent worlds per selector",
      episodes=85824,blocks=9,selectors=9,
      intervention_guard="budget13() must change only feature coordinate62 from12 to13",
      model_visibility="internal_remaining is model-visible; intermediate actions are rescored for correctness rather than forced to replay budget12 decisions",
      resources="start13/4/step7; after 1acq+2decisions8/3/12; after2acq+3decisions4/2/16; after3acq+4decisions0/1/20",
      final_authority="after third real acquisition, charge_decision must succeed then frozen C181 necessity-only prediction must be SUFFICIENT",
      gate="all9 blocks zero necessity/target/observed/repeat/acquisition/final/contract errors; first reads9536; third/final rows equal and >0; exact resource accounting",
      training=0,fresh_seeds=0,network_calls=0,answer_generation=0,proof_checker_calls=0,core_evidence_writes=0,
      production_runtime_modified=False,gate_e_candidate=False,outputs=sorted(OUTPUTS),
      limits="development family;budget13 is diagnostic intervention not adopted runtime default;no learned resource policy,tool/provider choice,renaming holdout,language,answer/proof or full GateE")

MANIFEST_SHA="c038222b91af95f557a39171c18ed75e791e32455d74556c771875b9c68a95b5"

def precheck(c192_summary,*args):
    from fold_lm.v05_benchmarks import gate_e_c192_post3_shadow_necessity as parent
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(len(args)==18,"Seventeen prior summaries and repository root required")
    root=args[-1]
    p191,p190,p189,p188,p181,p174,pins,protected=parent.precheck(args[0],*args[1:])
    require(audit.sha(c192_summary)==PARENT_SHA,"C192 summary changed")
    p=audit.read_json(c192_summary);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS"
            and parent.gate(p["records"]) and p["source_blobs"]==pins,
            "Wrong accepted C192 source/result")
    protected[str(Path(c192_summary).resolve())]=PARENT_SHA
    for a in p["artifacts"]:
        f=audit.safe_child(Path(c192_summary).resolve().parent,a["file"])
        require(f.is_file() and f.stat().st_size==a["serialized_bytes"] and audit.sha(f)==a["sha256"],
                "Changed C192 artifact:"+a["file"])
        protected[str(f.resolve())]=a["sha256"]
    pins=dict(pins)
    for name in parent.OWN:
        pins[name]=audit.git(root,"rev-parse",PARENT_EXECUTION+":"+name).decode().strip()
    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins)==126 and len(protected)==342,"Source/protected union drift")
    require(digest(manifest())==MANIFEST_SHA,"Manifest drift")
    return p,p191,p190,p189,p188,p181,p174,pins,protected

def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c192_post3_shadow_necessity as parent
    names=parent.regression_modules(root)
    require(len(names)==len(set(names))==77,"Historical regression list drift")
    return names+["tests_lm.test_v05_c193_budget13_authoritative_closure"]

def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE
            and p["diagnostic_execution_valid"] is True,"Wrong/incomplete C193")
    require(p["episodes"]==85824 and len(p["records"])==9
            and len(p["source_blobs"])==126 and len(p["input_sha256"])==342
            and len(p["artifacts"])==4 and {a["file"] for a in p["artifacts"]}==OUTPUTS,
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

    root=Path(__file__).resolve().parents[2]
    args=tuple(parents[n+"_summary"] for n in PRIOR_NAMES[1:])+(root,)
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"Dirty tracked tree")
    guard()
    p192,p191,p190,p189,p188,p181,p174,pins,protected=precheck(parents["c192_summary"],*args)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    artifacts=[];records=[];started=time.perf_counter()
    def record_file(name):
        f=out/name;artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,v):
        (out/name).write_bytes(blob(v));record_file(name)
    save("budget13-plan.json",dict(manifest(),source_blobs=pins))
    try:
        print("[C193] plan fixed; only internal budget12->13; full authoritative learned path rescored",flush=True)
        torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
        data,metadata=audit.load_data(Path(parents["c174_summary"]).resolve().parent,p174)
        raw_all=torch.from_numpy(data["features"].copy())
        valid=c189.target_teacher(data["features"],data["template_ids"],metadata)
        _,_,evfull,_,_=target.cohort_masks(raw_all,data["labels"],data["split_codes"],valid)
        full_ix=np.flatnonzero(evfull)
        raw12=torch.from_numpy(data["features"][evfull].copy())
        raw13=budget13(raw12)
        expanded12,source_rows,local_rows,world_codes=c190.expand_worlds(raw12,full_ix)
        expanded13=budget13(expanded12)
        tids=data["template_ids"][evfull]

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
        with gzip.open(out/"episode-traces.jsonl.gz","wt",encoding="utf-8",newline="\n") as trace:
            for bi,b in enumerate(BASE_SEEDS):
                for hi,h in enumerate(HEAD_SEEDS):
                    idx=bi*3+hi
                    cache,_=initial_policy_cache(raw13,full_ix,bases[b],heads[b,h])
                    lt=torch.from_numpy(local_rows.astype(np.int64))
                    initial=dict(raw=cache["raw"][lt],
                        necessity_predictions=cache["necessity_predictions"][local_rows],
                        target_predictions=cache["target_predictions"][local_rows],
                        necessity_logits=cache["necessity_logits"][local_rows],
                        target_logits=cache["target_logits"][local_rows])
                    before=sum(p.reads for p in providers.values())
                    views=c190.make_views(expanded13,source_rows,world_codes,f"C193-b{b}-h{h}")
                    observed,arrays,_=run_block(views,world_codes,endpoints,bases[b],heads[b,h],initial)
                    dense["necessity_predictions"][idx]=arrays["necessity_predictions"]
                    dense["necessity_logits"][idx]=arrays["necessity_logits"]
                    dense["target_predictions"][idx]=arrays["target_predictions"]
                    dense["target_logits"][idx]=arrays["target_logits"]
                    scores=[]
                    for j,rec in enumerate(observed):
                        score=assess(rec,int(tids[int(local_rows[j])]),metadata,
                                     c190.WORLD_BITS[int(world_codes[j])])
                        scores.append(score)
                        trace.write(json.dumps(dict(base_seed=b,head_seed=h,source_row=int(source_rows[j]),
                            world_code=int(world_codes[j]),score=score,trace=rec),
                            sort_keys=True,separators=(",",":"),allow_nan=False)+"\n")
                    totals={k:sum(s[k] for s in scores) for k in COUNTERS}
                    reads=sum(p.reads for p in providers.values())-before
                    rec=dict(base_seed=b,head_seed=h,episodes=9536,actual_reads=reads,**totals)
                    records.append(rec)
                    print(f"[C193] block={len(records)}/9 base={b} head={h} failed={rec['failed']} "
                          f"reads={reads} second={rec['second_reads']} third={rec['third_reads']} "
                          f"final={rec['final_decision_rows']} final_err={rec['final_decision_error']}",flush=True)
        record_file("episode-traces.jsonl.gz")
        np.savez_compressed(out/"episode-predictions.npz",**dense,row_indices=source_rows.astype("<i4"),
                            local_rows=local_rows.astype("<i4"),world_codes=world_codes.astype(np.int8))
        record_file("episode-predictions.npz")
        save("episode-results.json",records)
        guard();precheck(parents["c192_summary"],*args)
        for f,hsh in protected.items(): require(audit.sha(f)==hsh,"Protected input changed:"+f)
        for a in artifacts: require(audit.sha(out/a["file"])==a["sha256"],"Output changed:"+a["file"])
        totals={k:sum(r[k] for r in records) for k in COUNTERS}
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status="PASS" if gate(records) else "FAIL",diagnostic_execution_valid=True,
            C192_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,
            artifacts=artifacts,records=records,totals=totals,episodes=85824,
            actual_file_reads=sum(p.reads for p in providers.values()),
            provider_bytes_read=sum(p.bytes_read for p in providers.values()),
            new_training=0,fresh_seeds=0,network_calls=0,answer_generation=0,
            proof_checker_calls=0,core_evidence_writes=0,
            production_runtime_modified=False,gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=["budget13 is a diagnostic intervention, not adopted production default",
                "same repeatedly inspected development groups",
                "no learned resource policy/tool-provider choice/independent holdout/language/answer/proof/GateE"])
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C193] source/output preservation checked",flush=True)
        print("=== C193 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
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
