"""C191: third learned acquisition under unchanged C190 internal budget.

Diagnostic only. Replays accepted C190 through phase2, then on post2 NEEDS exposes the
same frozen C188 target head, performs exactly one third real acquisition from the same
coherent world, exhausts the remaining three internal units, and verifies a fourth
decision cannot be charged. No post-third learned decision is permitted.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, time
from dataclasses import asdict
from pathlib import Path
import numpy as np
import torch

EXPERIMENT_ID="C191-v5e-third-acquisition-budget-boundary"
STAGE="V5-E-THIRD-ACQUISITION-BUDGET-BOUNDARY"
BASE="53b114aeeabbee2e5ea54ebf6f1396054b74132a"
PARENT_EXECUTION="b3d04dae6ed621deba987162b3d63c8f815bbe72"
PARENT_SHA="6902f97fd1fbcb1eb878884594a333ae41a0d35c83b872d287439386f7fabd59"
BASE_SEEDS=(181001,181002,181003)
HEAD_SEEDS=(188001,188002,188003)
ARM="INTERNAL_SEMANTICS"
BATCH=1024
ATOL=1e-6
PRIOR_NAMES=("c190","c189","c188","c187","c186","c185","c184","c183","c182","c181",
             "c180","c179","c178","c177","c176","c174")
OWN=("fold_lm/v05_benchmarks/gate_e_c191_third_acquisition_budget.py",
     "tests_lm/test_v05_c191_third_acquisition_budget.py",
     "tools/run_c191.ps1","tools/invoke_c191.ps1",
     "docs/experiment-ledger-addendum-c191-preregistration.md")
EXPECTED_TESTS=1509

def require(ok,msg):
    if not ok: raise ValueError(msg)

def blob(v):
    return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()

def digest(v):
    return hashlib.sha256(blob(v)).hexdigest()

def load_parent_predictions(path):
    p=Path(path)
    require(p.is_file() and p.stat().st_size < 5_000_000,"Unexpected C190 prediction artifact size")
    with np.load(p,allow_pickle=False) as z:
        expected={"necessity_predictions","necessity_logits","target_predictions","target_logits",
                  "row_indices","local_rows","world_codes","base_seeds","head_seeds"}
        require(set(z.files)==expected,"C190 prediction schema drift")
        out={k:z[k].copy() for k in z.files}
    require(out["necessity_predictions"].shape==(9,9536,3)
            and out["necessity_logits"].shape==(9,9536,3,2)
            and out["target_predictions"].shape==(9,9536,2)
            and out["target_logits"].shape==(9,9536,2,4)
            and out["row_indices"].shape==(9536,)
            and out["local_rows"].shape==(9536,)
            and out["world_codes"].shape==(9536,)
            and out["base_seeds"].tolist()==[b for b in BASE_SEEDS for _ in HEAD_SEEDS]
            and out["head_seeds"].tolist()==[h for _ in BASE_SEEDS for h in HEAD_SEEDS],
            "C190 prediction array drift")
    return out

def run_block(views,world_codes,endpoints,base,selector,initial):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05 import structured_action_runtime as action
    from fold_lm.v05 import structured_task_input as task
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190

    require(len(views)==len(world_codes)>0,"Episode/world alignment required")
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{"RETRIEVE":endpoints[int(code)]},
                                  max_dispatches=3)
            for v,code in zip(views,world_codes,strict=True)]
    n=len(views)
    records=[dict(initial=asdict(task.encode(v)),phases=[],acquisitions=[],
                  decision_charges=0,fourth_decision_accepted=False,
                  status="UNRESOLVED",world_code=int(code))
             for v,code in zip(views,world_codes,strict=True)]
    n_pred=np.full((n,3),-1,dtype=np.int8)
    n_logits=np.zeros((n,3,2),dtype=np.float32)
    t_pred=np.full((n,3),-1,dtype=np.int8)
    t_logits=np.full((n,3,4),-np.inf,dtype=np.float32)
    meter=dict(rows=0,forward_calls=0,cell_calls=0)

    active=[i for i,o in enumerate(owners) if driver.charge_decision(o)]
    require(len(active)==n,"Initial decision budget unexpectedly exhausted")
    raw0,packets0=c189.encode_views([owners[i].state.view for i in active])
    require(torch.equal(raw0,initial["raw"]),"Initial cache mapping drift")
    p0=np.asarray(initial["necessity_predictions"]);t0=np.asarray(initial["target_predictions"])
    z0=np.asarray(initial["necessity_logits"]);tz0=np.asarray(initial["target_logits"])
    first=[]
    for j,i in enumerate(active):
        n_pred[i,0]=p0[j];n_logits[i,0]=z0[j];t_pred[i,0]=t0[j];t_logits[i,0]=tz0[j]
        records[i]["decision_charges"]+=1
        records[i]["phases"].append(dict(phase=0,packet=asdict(packets0[j]),
            necessity_prediction=int(p0[j]),target_prediction=int(t0[j])))
        if p0[j]==1:
            records[i]["acquisitions"].append(c190.acquire(owners[i],int(t0[j])))
            first.append(i)
        else:
            records[i]["status"]="SUFFICIENT_CLASSIFICATION"

    phase1=[i for i in first if driver.charge_decision(owners[i])]
    require(len(phase1)==len(first),"Phase1 decision budget unexpectedly exhausted")
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
                records[i]["acquisitions"].append(c190.acquire(owners[i],int(t1[j])))
                second.append(i)
            else:
                records[i]["status"]="SUFFICIENT_CLASSIFICATION"

    phase2=[i for i in second if driver.charge_decision(owners[i])]
    require(len(phase2)==len(second),"Phase2 decision budget unexpectedly exhausted")
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
                records[i]["acquisitions"].append(c190.acquire(owners[i],int(t2[j])))
                third.append(i)
                before=owners[i].state
                accepted=driver.charge_decision(owners[i])
                records[i]["fourth_decision_accepted"]=bool(accepted)
                require(owners[i].state==before,"Rejected fourth decision mutated state")
                records[i]["status"]="BUDGET_EXHAUSTED_AFTER_THIRD"
            else:
                records[i]["status"]="SUFFICIENT_CLASSIFICATION"

    for i,o in enumerate(owners):
        records[i]["final"]=asdict(task.encode(o.state.view))
        records[i]["receipts"]=[asdict(r) for r in o.receipts]
        records[i]["pending"]=asdict(o.state.pending) if o.state.pending else None
        records[i]["runtime_terminal"]=o.state.terminal
    return records,dict(necessity_predictions=n_pred,necessity_logits=n_logits,
                        target_predictions=t_pred,target_logits=t_logits),meter

COUNTERS=("failed","parent_replay_error","target2_error","selected_observed",
          "repeated_target","third_acquisition_error","final_logical_needs",
          "fourth_decision_accepted","contract_error","third_reservations",
          "third_provider_calls","third_publications")

def assess(record,template_id,metadata,world_bits,parent_phase2_need,parent_targets):
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
    initial=record["initial"];final=record["final"];ph=record["phases"];acq=record["acquisitions"]
    should=int(parent_phase2_need==1)
    target2=ph[2]["target_prediction"] if len(ph)>2 else -1
    packet2=ph[2]["packet"] if len(ph)>2 else None
    unknown=[]
    if packet2 is not None:
        x=np.asarray(packet2["features"],dtype=np.int64)
        unknown=[j for j in range(4) if x[48+4*j]==0]
    target2_error=int(should and not (len(unknown)==1 and target2==unknown[0]))
    selected_observed=int(should and target2 not in unknown)
    repeat=int(should and target2 in set(int(x) for x in parent_targets))
    a2=acq[2] if len(acq)>2 else None
    if should:
        ok=(a2 is not None and a2["input_index"]==target2
            and a2["action"]["status"]=="PENDING"
            and a2["action"]["reason"]=="ACQUISITION_RESERVED"
            and a2["action"]["acquisition_reserved"]==1
            and a2["dispatch"] is not None
            and a2["dispatch"]["status"]=="PUBLISHED"
            and a2["dispatch"]["reason"]=="OBSERVATION_ADMITTED"
            and a2["dispatch"]["provider_calls"]==1
            and a2["dispatch"]["fact_publications"]==1
            and len(record["receipts"])==3
            and record["receipts"][2]["fact_id"]==a2["fact_id"]
            and record["receipts"][2]["value"]==world_bits[target2])
    else:
        ok=(a2 is None)
    third_error=int(not ok)

    final_label=c190.logical_label(final["features"],template_id,metadata) if should else 0
    final_need=int(should and final_label!=0)
    fourth=int(record["fourth_decision_accepted"])
    f=np.asarray(final["features"],dtype=np.int64)
    structural=(record["pending"] is None and record["runtime_terminal"] is None)
    if should:
        structural=structural and (f[62],f[63],f[71])==(0,1,19)
        structural=structural and all(f[48+4*j]==1 for j in range(4))
        structural=structural and record["decision_charges"]==3
        structural=structural and record["status"]=="BUDGET_EXHAUSTED_AFTER_THIRD"
    contract=int(not structural)
    vals=(target2_error,selected_observed,repeat,third_error,final_need,fourth,contract)
    return dict(failed=int(any(vals)),parent_replay_error=0,target2_error=target2_error,
        selected_observed=selected_observed,repeated_target=repeat,
        third_acquisition_error=third_error,final_logical_needs=final_need,
        fourth_decision_accepted=fourth,contract_error=contract,
        third_reservations=int(a2["action"]["acquisition_reserved"]) if a2 else 0,
        third_provider_calls=int(a2["dispatch"]["provider_calls"]) if a2 and a2["dispatch"] else 0,
        third_publications=int(a2["dispatch"]["fact_publications"]) if a2 and a2["dispatch"] else 0)

def expected_order():
    return [(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS]

def gate(records):
    if [(r.get("base_seed"),r.get("head_seed")) for r in records]!=expected_order():
        return False
    for r in records:
        if r.get("episodes")!=9536 or r.get("parent_final_needs")!=928:
            return False
        if any(type(r.get(k)) is not int or r[k]<0 for k in COUNTERS):
            return False
        if any(r[k]!=0 for k in ("failed","parent_replay_error","target2_error",
            "selected_observed","repeated_target","third_acquisition_error",
            "final_logical_needs","fourth_decision_accepted","contract_error")):
            return False
        if (r["third_reservations"],r["third_provider_calls"],r["third_publications"])!=(928,928,928):
            return False
        if r.get("phase0_errors")!=0 or r.get("phase1_errors")!=0 or r.get("phase2_need_errors")!=0:
            return False
        if r.get("actual_reads") != 9536 + r.get("parent_second_reads", -1) + 928:
            return False
        if r.get("initial_necessity_max_abs_logit_difference",1)>ATOL or r.get("initial_target_max_abs_logit_difference",1)>ATOL:
            return False
    return True

SOURCE_FILES={
    "sources/world-00.json":"60db548156b43455a76347bb0515e54059762604c680915e3f80e09eb1124040",
    "sources/world-01.json":"a9d0f3d29470459c91e5682308cd4037a8381541340b28368f6f16b572a6f073",
    "sources/world-02.json":"7edc1a04ca1325cdc5c6206726b53ff15ee559dee618fac6a7535afcf3bb4502",
    "sources/world-03.json":"1cca00c5520898b045f5b8676ddbe63570de3b192a967b420c7993ba5ccfd5cd",
    "sources/world-04.json":"e031661bc1a8fe4bb3035ca034bb9584bfe211298a43a2870828ebab06b5a61f",
    "sources/world-05.json":"04e97110c77e4676b18a0927bd56df9354ddda77d0b3290b5165f9b1410058f9",
    "sources/world-06.json":"a1a07b00ec5d71e38d8a476ad2f2a1377a204e6b35c04ea74e9028c1b87ce925",
    "sources/world-07.json":"300dc8e390343c3121842b2f72ae3655d11ddcc035b8ccf677d9023ae03deb58",
    "sources/world-08.json":"2bbf3d15cb6301b91fe53b145442c75fbe37cfbcdb19ef53d905f1a9e6998340",
    "sources/world-09.json":"4bfc759ea45316250416bd5ce6059868b0c750a6e31e0dfeca4ad27f9a43cf47",
    "sources/world-10.json":"a97d2218530ed8ea3a9e40a1572062c0f78710fe809e6cb1f41f80cab1ac7c37",
    "sources/world-11.json":"38d4a7c43c857b9858e1719983dbec383195e60fb36d5bde1c8442955524fb5d",
    "sources/world-12.json":"1a79c8d24809b0fcdc4f462439e12eb20db1f894e80b031e9203e40a2ee221b3",
    "sources/world-13.json":"445619ad0bb33940756ce2c5713e4181c2d444ad5ec3bf9347f02e32b0cf783c",
    "sources/world-14.json":"267c4e437380a233232a90a5c2bf3b451404aef21a2839eb2c33e12f93227257",
    "sources/world-15.json":"3b603abc2a5279c5f2315160ff79ac0d74d9740abeb5ac42b32b84f6f1839743",
}
OUTPUTS={"third-step-plan.json","parent-replay.json","episode-results.json",
         "episode-traces.jsonl.gz","episode-predictions.npz"}|set(SOURCE_FILES)

def manifest():
    return dict(
      experiment_id=EXPERIMENT_ID,stage=STAGE,parent_sha256=PARENT_SHA,
      acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
      base_seeds=BASE_SEEDS,head_seeds=HEAD_SEEDS,arm=ARM,
      question="under unchanged internal budget12, can C190 post2 NEEDS states execute exactly one third learned target/acquisition, publish the last missing fact, exhaust budget exactly, and refuse a fourth decision",
      changed="C190 acquisition horizon extends from max2 to max3; resource budget and all learned components remain unchanged",
      cohort="same 85824 coherent-world episodes; third acquisition only on accepted C190 post2 NEEDS states",
      worlds_per_selector=9536,blocks=9,episodes=85824,expected_third_acquisitions=8352,
      source_files=SOURCE_FILES,
      source_contract="same 16 complete four-fact snapshots as C190; one world fixed per episode across all acquisitions",
      initial_policy="same exact-state memoized frozen C181+C188 output as accepted C190",
      phase1_policy="same frozen C181+C188 combined decision as C190",
      phase2_policy="same C181 necessity decision boundary, now also exposes frozen C188 target2 before optional third acquisition",
      target2_scope="post2 NEEDS has exactly one unobserved fact; target mask leaves one legal fact, so this is runtime closure evidence not alternative-target ranking evidence",
      resources="start12/4/step7; after decision0 11/4/8; after acq1+decision1 7/3/12; after acq2+decision2 3/2/16; after acq3 0/1/19; fourth decision must be refused",
      max_acquisitions_per_episode=3,max_learned_decisions_per_episode=3,
      final_teacher="scoring only: logical necessity after third admission must be SUFFICIENT; no final learned decision is allowed",
      parent_replay="phase0,phase1,and phase2 necessity plus first two targets replay accepted C190; initial logits exact-state replay <=1e-6",
      gate="all9 blocks zero replay/target/action/contract errors; third reads exactly C190 post2 NEEDS; final logical NEEDS0; fourth decision accepted0; final resources exact",
      initial_unique_policy_rows=15912,
      training=0,fresh_seeds=0,network_calls=0,answer_generation=0,proof_checker_calls=0,core_evidence_writes=0,
      production_runtime_modified=False,gate_e_candidate=False,outputs=sorted(OUTPUTS),
      limits="same four repeatedly inspected development groups;third target is sole remaining unknown;no final learned post3 decision because unchanged budget exhausts;no tool/provider learning,renaming,language,answer/proof or full GateE")

MANIFEST_SHA="8cf89274974a4204156c2cb2eb1f87d101f8ab09b320dd7e649a4380ddb852f1"

def precheck(c190_summary,*args):
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as parent
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(len(args)==16,"Fifteen prior summaries and repository root required")
    root=args[-1]
    p189,p188,p181,p174,pins,protected=parent.precheck(args[0],*args[1:])
    require(audit.sha(c190_summary)==PARENT_SHA,"C190 summary changed")
    p=audit.read_json(c190_summary);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS"
            and parent.gate(p["records"]) and p["source_blobs"]==pins,
            "Wrong accepted C190 source/result")
    protected[str(Path(c190_summary).resolve())]=PARENT_SHA
    for a in p["artifacts"]:
        f=audit.safe_child(Path(c190_summary).resolve().parent,a["file"])
        require(f.is_file() and f.stat().st_size==a["serialized_bytes"] and audit.sha(f)==a["sha256"],
                "Changed C190 artifact:"+a["file"])
        protected[str(f.resolve())]=a["sha256"]
    pins=dict(pins)
    for name in parent.OWN:
        pins[name]=audit.git(root,"rev-parse",PARENT_EXECUTION+":"+name).decode().strip()
    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins)==116 and len(protected)==304,"Source/protected union drift")
    require(digest(manifest())==MANIFEST_SHA,"Manifest drift")
    return p,p189,p188,p181,p174,pins,protected

def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as parent
    names=parent.regression_modules(root)
    require(len(names)==len(set(names))==75,"Historical regression list drift")
    return names+["tests_lm.test_v05_c191_third_acquisition_budget"]

def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE
            and p["diagnostic_execution_valid"] is True,"Wrong/incomplete C191")
    require(p["episodes"]==85824 and len(p["records"])==9
            and p["third_acquisitions"]==8352
            and len(p["source_blobs"])==116 and len(p["input_sha256"])==304
            and len(p["artifacts"])==21 and {a["file"] for a in p["artifacts"]}==OUTPUTS,
            "Workload/coverage drift")
    require(all(p[k]==0 for k in ("new_training","fresh_seeds","network_calls",
                                  "answer_generation","proof_checker_calls","core_evidence_writes"))
            and p["production_runtime_modified"] is False and p["gate_e_candidate"] is False,
            "Scope drift")
    require(p["status"]==("PASS" if gate(p["records"]) else "FAIL"),"Gate drift")

def run(*,output_dir,expected_head,**parents):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
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
    p190,p189,p188,p181,p174,pins,protected=precheck(parents["c190_summary"],*args)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    artifacts=[];records=[];started=time.perf_counter()
    def record_file(name):
        f=out/name;artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,v):
        (out/name).write_bytes(blob(v));record_file(name)
    save("third-step-plan.json",dict(manifest(),source_blobs=pins))
    try:
        print("[C191] plan fixed; unchanged budget12; third acquisition only on C190 post2 NEEDS; no post3 learned decision",flush=True)
        torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
        data,metadata=audit.load_data(Path(parents["c174_summary"]).resolve().parent,p174)
        raw_all=torch.from_numpy(data["features"].copy())
        valid=c189.target_teacher(data["features"],data["template_ids"],metadata)
        _,_,evfull,_,_=target.cohort_masks(raw_all,data["labels"],data["split_codes"],valid)
        full_ix=np.flatnonzero(evfull);raw=torch.from_numpy(data["features"][evfull].copy())
        expanded,source_rows,local_rows,world_codes=c190.expand_worlds(raw,full_ix)
        tids=data["template_ids"][evfull]
        parent_dir=Path(parents["c190_summary"]).resolve().parent
        saved=load_parent_predictions(parent_dir/"episode-predictions.npz")
        require(np.array_equal(saved["row_indices"],source_rows)
                and np.array_equal(saved["local_rows"],local_rows)
                and np.array_equal(saved["world_codes"],world_codes),"C190 episode identity drift")

        c181_dir=Path(parents["c181_summary"]).resolve().parent
        c188_dir=Path(parents["c188_summary"]).resolve().parent
        fits={f["seed"]:f for f in p181["fit_records"] if f["arm"]==ARM}
        selector_sha={(r["base_seed"],r["head_seed"]):r["head_sha256"] for r in p188["selector_results"]}
        bases={};heads={}
        for b in BASE_SEEDS:
            bases[b]=frozen.restore_bare(c181_dir/f"probe-{b}-{ARM}.pt",b,ARM,fits[b]["final_sha256"])
            for h in HEAD_SEEDS:
                heads[b,h]=c189.restore_selector(c188_dir/f"selector-{b}-{h}.pt",b,h,selector_sha[b,h])

        (out/"sources").mkdir()
        providers={};endpoints={}
        for code in range(16):
            name=f"sources/world-{code:02d}.json";bb=c190.world_bytes(code)
            require(hashlib.sha256(bb).hexdigest()==SOURCE_FILES[name],"World source hash drift")
            (out/name).write_bytes(bb);record_file(name)
            sb=life.SourceBinding(f"C190-world-{code:02d}",hashlib.sha256(bb).hexdigest())
            p=life.FileSnapshotProvider(out/name,sb);providers[code]=p;endpoints[code]=life.Endpoint(sb,p)

        dense=dict(
            necessity_predictions=np.full((9,9536,3),-1,dtype=np.int8),
            necessity_logits=np.zeros((9,9536,3,2),dtype=np.float32),
            target_predictions=np.full((9,9536,3),-1,dtype=np.int8),
            target_logits=np.full((9,9536,3,4),-np.inf,dtype=np.float32))
        parent_replay=[]
        with gzip.open(out/"episode-traces.jsonl.gz","wt",encoding="utf-8",newline="\n") as trace:
            for bi,b in enumerate(BASE_SEEDS):
                for hi,h in enumerate(HEAD_SEEDS):
                    idx=bi*3+hi
                    cache,m0=c190.initial_policy_cache(raw,full_ix,bases[b],heads[b,h])
                    pn0=saved["necessity_predictions"][idx,:,0];pt0=saved["target_predictions"][idx,:,0]
                    pn1=saved["necessity_predictions"][idx,:,1];pt1=saved["target_predictions"][idx,:,1]
                    pn2=saved["necessity_predictions"][idx,:,2]
                    local_tensor=torch.from_numpy(local_rows.astype(np.int64))
                    initial=dict(raw=cache["raw"][local_tensor],
                        necessity_predictions=cache["necessity_predictions"][local_rows],
                        target_predictions=cache["target_predictions"][local_rows],
                        necessity_logits=cache["necessity_logits"][local_rows],
                        target_logits=cache["target_logits"][local_rows])
                    nd=float(np.max(np.abs(cache["necessity_logits"]-p190["parent_replay"][idx]["necessity_max_abs_logit_difference"]*0
                        - np.asarray(cache["necessity_logits"])))) if False else 0.0
                    before=sum(p.reads for p in providers.values())
                    views=c190.make_views(expanded,source_rows,world_codes,f"C191-b{b}-h{h}")
                    observed,arrays,_=run_block(views,world_codes,endpoints,bases[b],heads[b,h],initial)
                    dense["necessity_predictions"][idx]=arrays["necessity_predictions"]
                    dense["necessity_logits"][idx]=arrays["necessity_logits"]
                    dense["target_predictions"][idx]=arrays["target_predictions"]
                    dense["target_logits"][idx]=arrays["target_logits"]

                    unknown0=target.missing_mask(initial["raw"]).numpy()
                    ndelta=float(np.max(np.abs(arrays["necessity_logits"][:,0]-saved["necessity_logits"][idx,:,0])))
                    tdelta=float(np.max(np.abs(arrays["target_logits"][:,0][unknown0]-saved["target_logits"][idx,:,0][unknown0])))
                    phase0=int((arrays["necessity_predictions"][:,0]!=pn0).sum()
                        +(arrays["target_predictions"][:,0]!=pt0).sum())
                    mask1=pn0==1
                    phase1=int((arrays["necessity_predictions"][mask1,1]!=pn1[mask1]).sum()
                        +(arrays["target_predictions"][mask1,1]!=pt1[mask1]).sum())
                    mask2=pn1==1
                    phase2=int((arrays["necessity_predictions"][mask2,2]!=pn2[mask2]).sum())
                    parent_replay.append(dict(base_seed=b,head_seed=h,phase0_errors=phase0,
                        phase1_errors=phase1,phase2_need_errors=phase2,
                        initial_necessity_max_abs_logit_difference=ndelta,
                        initial_target_max_abs_logit_difference=tdelta))
                    scores=[]
                    for j,rec in enumerate(observed):
                        score=assess(rec,int(tids[int(local_rows[j])]),metadata,
                            c190.WORLD_BITS[int(world_codes[j])],int(pn2[j]),
                            (int(pt0[j]),int(pt1[j]) if pt1[j]>=0 else -1))
                        score["parent_replay_error"]=int(bool(phase0 or phase1 or phase2))
                        score["failed"]=int(score["failed"] or score["parent_replay_error"])
                        scores.append(score)
                        trace.write(json.dumps(dict(base_seed=b,head_seed=h,source_row=int(source_rows[j]),
                            world_code=int(world_codes[j]),score=score,trace=rec),
                            sort_keys=True,separators=(",",":"),allow_nan=False)+"\n")
                    totals={k:sum(s[k] for s in scores) for k in COUNTERS}
                    reads=sum(p.reads for p in providers.values())-before
                    parent_rec=p190["records"][idx]
                    rec=dict(base_seed=b,head_seed=h,episodes=9536,
                        parent_second_reads=parent_rec["second_provider_calls"],
                        parent_final_needs=parent_rec["final_needs"],
                        phase0_errors=phase0,phase1_errors=phase1,phase2_need_errors=phase2,
                        initial_necessity_max_abs_logit_difference=ndelta,
                        initial_target_max_abs_logit_difference=tdelta,actual_reads=reads,**totals)
                    records.append(rec)
                    print(f"[C191] block={len(records)}/9 base={b} head={h} failed={rec['failed']} "
                          f"third_reads={rec['third_provider_calls']} fourth_accept={rec['fourth_decision_accepted']}",flush=True)
        record_file("episode-traces.jsonl.gz")
        np.savez_compressed(out/"episode-predictions.npz",**dense,row_indices=source_rows.astype("<i4"),
            local_rows=local_rows.astype("<i4"),world_codes=world_codes.astype(np.int8))
        record_file("episode-predictions.npz")
        save("parent-replay.json",parent_replay);save("episode-results.json",records)
        guard();precheck(parents["c190_summary"],*args)
        for f,hsh in protected.items():require(audit.sha(f)==hsh,"Protected input changed:"+f)
        for a in artifacts:require(audit.sha(out/a["file"])==a["sha256"],"Output changed:"+a["file"])
        totals={k:sum(r[k] for r in records) for k in COUNTERS}
        result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status="PASS" if gate(records) else "FAIL",diagnostic_execution_valid=True,
            C190_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,
            artifacts=artifacts,records=records,parent_replay=parent_replay,totals=totals,
            episodes=85824,third_acquisitions=totals["third_provider_calls"],
            actual_file_reads=sum(p.reads for p in providers.values()),
            provider_bytes_read=sum(p.bytes_read for p in providers.values()),
            new_training=0,fresh_seeds=0,network_calls=0,answer_generation=0,
            proof_checker_calls=0,core_evidence_writes=0,
            production_runtime_modified=False,gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=["same four repeatedly inspected development groups",
                "target2 is the sole remaining unknown, so target2 correctness is not alternative-ranking evidence",
                "unchanged internal budget is exhausted by third acquisition; no learned post3 decision",
                "fixed RETRIEVE/local provider; no language/answer/proof/GateE"])
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C191] source/output preservation checked",flush=True)
        print("=== C191 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
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
