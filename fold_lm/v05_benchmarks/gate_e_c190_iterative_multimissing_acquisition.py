"""C190: iterative learned multi-missing acquisition over coherent source worlds.

Diagnostic only. Reuse frozen accepted C181 necessity bases and frozen accepted C188 target
heads. Each episode is bound to one complete 4-bit source snapshot consistent with its
initial visible facts. At most two learned targets may be acquired; no third acquisition.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import time

import numpy as np
import torch

EXPERIMENT_ID = "C190-v5e-iterative-multimissing-acquisition"
STAGE = "V5-E-ITERATIVE-MULTIMISSING-ACQUISITION"
BASE = "9bd1ccc7d176a8134466eb22a3546861f1ba9a7d"
PARENT_EXECUTION = "051165ac5b14600d36f38064e36785d767de934d"
PARENT_SHA = "a9388db7e28e25cf1b12e7f78e3068228ee5b5562da12a3a626fe054fead4b7a"
BASE_SEEDS = (181001,181002,181003)
HEAD_SEEDS = (188001,188002,188003)
ARM = "INTERNAL_SEMANTICS"
WORLD_BITS = tuple(itertools.product((0,1), repeat=4))
BATCH = 1024
ATOL = 1e-6
PRIOR_NAMES = ("c189","c188","c187","c186","c185","c184","c183","c182","c181","c180",
               "c179","c178","c177","c176","c174")
OWN = ("fold_lm/v05_benchmarks/gate_e_c190_iterative_multimissing_acquisition.py",
       "tests_lm/test_v05_c190_iterative_multimissing_acquisition.py",
       "tools/run_c190.ps1","tools/invoke_c190.ps1",
       "docs/experiment-ledger-addendum-c190-preregistration.md")
EXPECTED_TESTS = 1485

def require(ok,message):
    if not ok:
        raise ValueError(message)

def blob(value):
    return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()

def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()

def world_bytes(code):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    require(type(code) is int and 0 <= code < len(WORLD_BITS),"Registered world code required")
    bits=WORLD_BITS[code]
    return blob(dict(schema=life.SOURCE_SCHEMA,provider_id=f"C190-world-{code:02d}",
        evidence_time=1,revision=1,
        records=[dict(fact_id=driver.FACT_IDS[i],value=int(bits[i])) for i in range(4)]))

SOURCE_FILES = {
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
OUTPUTS = {"iterative-plan.json","parent-replay.json","episode-results.json",
           "episode-traces.jsonl.gz","episode-predictions.npz"} | set(SOURCE_FILES)

def consistent_worlds(row):
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
    vis=target.visible_tuple(row)
    return tuple(i for i,b in enumerate(WORLD_BITS)
                 if all(v is None or v==b[j] for j,v in enumerate(vis)))

def expand_worlds(raw,row_indices):
    require(isinstance(raw,torch.Tensor) and raw.dtype==torch.int32 and raw.ndim==2
            and raw.shape[1]==72 and len(raw)==len(row_indices)>0,"Aligned raw cohort required")
    rows=[];sources=[];locals_=[];codes=[];m2=m3=0
    for local,(r,sr) in enumerate(zip(raw,row_indices,strict=True)):
        worlds=consistent_worlds(r.numpy())
        missing=sum(v is None for v in __import__(
            "fold_lm.v05_benchmarks.gate_e_c188_multimissing_target_selection",
            fromlist=["visible_tuple"]).visible_tuple(r.numpy()))
        require((missing,len(worlds)) in ((2,4),(3,8)),"World expansion domain drift")
        if missing==2:m2+=len(worlds)
        else:m3+=len(worlds)
        for code in worlds:
            rows.append(r.clone());sources.append(int(sr));locals_.append(local);codes.append(code)
    out=torch.stack(rows)
    require(len(out)==9536 and m2==4608 and m3==4928,"Registered world count drift")
    return out,np.asarray(sources,dtype=np.int32),np.asarray(locals_,dtype=np.int32),np.asarray(codes,dtype=np.int8)

def make_views(raw,source_rows,world_codes,block_id):
    from fold_lm.v05 import structured_task_input as task
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    require(len(raw)==len(source_rows)==len(world_codes)>0,"Aligned episode views required")
    views=[]
    for ordinal,(row,sr,code) in enumerate(zip(raw.tolist(),source_rows,world_codes,strict=True)):
        scope=f"C190-{block_id}-{int(sr)}-w{int(code):02d}-{ordinal}"
        refs=tuple((f"initial:{scope}:{driver.FACT_IDS[i]}",) if row[48+4*i] else () for i in range(4))
        packet=task.PolicyInput(task.SCHEMA,tuple(row),
            task.Binding(scope+"|query",scope,driver.FACT_IDS,refs))
        views.append(task.decode(packet))
    return views

def load_parent_predictions(path):
    p=Path(path)
    require(p.is_file() and p.stat().st_size < 10_000_000,"Unexpected C189 prediction artifact size")
    with np.load(p,allow_pickle=False) as z:
        expected={"necessity_predictions","necessity_logits","target_predictions","target_logits",
                  "post_labels","row_indices","base_seeds","head_seeds"}
        require(set(z.files)==expected,"C189 prediction schema drift")
        out={k:z[k].copy() for k in z.files}
    require(out["row_indices"].shape==(1768,)
            and out["necessity_predictions"].shape==(9,2,1768,2)
            and out["necessity_logits"].shape==(9,2,1768,2,2)
            and out["target_predictions"].shape==(9,2,1768)
            and out["target_logits"].shape==(9,2,1768,4)
            and out["post_labels"].shape==(9,2,1768)
            and out["base_seeds"].tolist()==[b for b in BASE_SEEDS for _ in HEAD_SEEDS]
            and out["head_seeds"].tolist()==[h for _ in BASE_SEEDS for h in HEAD_SEEDS],
            "C189 prediction array drift")
    require(np.array_equal(out["necessity_predictions"][:,0,:,0],out["necessity_predictions"][:,1,:,0])
            and np.array_equal(out["target_predictions"][:,0],out["target_predictions"][:,1]),
            "C189 initial predictions unexpectedly depend on source bit")
    return out

def initial_policy_cache(raw,row_indices,base,selector):
    """Recompute one policy output per unique observable initial state, independent of hidden world."""
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05 import structured_action_runtime as action
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as parent
    require(isinstance(raw,torch.Tensor) and raw.dtype==torch.int32 and raw.ndim==2
            and raw.shape[1]==72 and len(raw)==len(row_indices)>0,
            "Unique initial policy cohort required")
    views=driver.make_views(raw,row_indices,driver.LAYOUTS[0],"C190-initial-policy-cache")
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{},max_dispatches=2) for v in views]
    require(all(driver.charge_decision(o) for o in owners),
            "Initial policy-cache decision budget unexpectedly exhausted")
    charged,_=parent.encode_views([o.state.view for o in owners])
    p,t,z,tz,m=parent.combined_predict(base,selector,charged,batch=BATCH)
    require(p.shape==t.shape==(len(raw),) and z.shape==(len(raw),2) and tz.shape==(len(raw),4),
            "Initial policy-cache output shape drift")
    return dict(raw=charged,necessity_predictions=p,target_predictions=t,
                necessity_logits=z,target_logits=tz),m

def acquire(owner,target_index):
    from fold_lm.v05 import structured_action_runtime as action
    require(type(target_index) is int and 0 <= target_index < 4,"Local target required")
    view=owner.state.view
    require(view.facts[target_index].status=="UNOBSERVED","Target must currently be unobserved")
    fid=view.facts[target_index].fact_id
    tr=owner.apply(action.propose(owner.state,"RETRIEVE",fact_index=target_index))
    dispatched=None
    if tr.result.status=="PENDING":
        dispatched=owner.dispatch(tr.result.intent.intent_id)
    return dict(input_index=target_index,fact_id=fid,action=asdict(tr.result),
                dispatch=asdict(dispatched) if dispatched else None)

def run_block(views,world_codes,endpoints,base,selector,initial=None):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05 import structured_action_runtime as action
    from fold_lm.v05 import structured_task_input as task
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as parent

    require(len(views)==len(world_codes)>0,"Episode/world alignment required")
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{"RETRIEVE":endpoints[int(code)]},
                                  max_dispatches=2)
            for v,code in zip(views,world_codes,strict=True)]
    n=len(views)
    records=[dict(initial=asdict(task.encode(v)),phases=[],acquisitions=[],
                  decision_charges=0,status="UNRESOLVED",world_code=int(code))
             for v,code in zip(views,world_codes,strict=True)]
    n_pred=np.full((n,3),-1,dtype=np.int8);n_logits=np.zeros((n,3,2),dtype=np.float32)
    t_pred=np.full((n,2),-1,dtype=np.int8);t_logits=np.full((n,2,4),-np.inf,dtype=np.float32)
    meter=dict(rows=0,forward_calls=0,cell_calls=0)

    active=[i for i,o in enumerate(owners) if driver.charge_decision(o)]
    require(len(active)==n,"Initial decision budget unexpectedly exhausted")
    raw0,packets0=parent.encode_views([owners[i].state.view for i in active])
    if initial is None:
        p0,t0,z0,tz0,m0=parent.combined_predict(base,selector,raw0,batch=BATCH)
        for k in meter: meter[k]+=m0[k]
    else:
        require(type(initial) is dict and set(initial)=={
            "raw","necessity_predictions","target_predictions","necessity_logits","target_logits"},
            "Exact initial policy cache required")
        require(isinstance(initial["raw"],torch.Tensor) and torch.equal(raw0,initial["raw"]),
                "Initial policy cache/input identity drift")
        p0=np.asarray(initial["necessity_predictions"])
        t0=np.asarray(initial["target_predictions"])
        z0=np.asarray(initial["necessity_logits"])
        tz0=np.asarray(initial["target_logits"])
        require(p0.shape==t0.shape==(n,) and z0.shape==(n,2) and tz0.shape==(n,4)
                and p0.dtype.kind in "iu" and t0.dtype.kind in "iu"
                and np.isfinite(z0).all(),
                "Invalid cached initial policy outputs")
        unknown=__import__("fold_lm.v05_benchmarks.gate_e_c188_multimissing_target_selection",
                           fromlist=["missing_mask"]).missing_mask(raw0).numpy()
        require(np.isfinite(tz0[unknown]).all() and np.isneginf(tz0[~unknown]).all()
                and np.array_equal(p0,z0.argmax(1)) and np.array_equal(t0,tz0.argmax(1)),
                "Cached initial raw argmax/nonfinite drift")
    first=[]
    for j,i in enumerate(active):
        n_pred[i,0]=p0[j];n_logits[i,0]=z0[j];t_pred[i,0]=t0[j];t_logits[i,0]=tz0[j]
        records[i]["decision_charges"]+=1
        records[i]["phases"].append(dict(phase=0,packet=asdict(packets0[j]),
            necessity_prediction=int(p0[j]),target_prediction=int(t0[j])))
        if p0[j]==1:
            records[i]["acquisitions"].append(acquire(owners[i],int(t0[j])))
            first.append(i)
        else:
            records[i]["status"]="SUFFICIENT_CLASSIFICATION"

    second_decision=[i for i in first if driver.charge_decision(owners[i])]
    require(len(second_decision)==len(first),"Second decision budget unexpectedly exhausted")
    second=[]
    if second_decision:
        raw1,packets1=parent.encode_views([owners[i].state.view for i in second_decision])
        p1,t1,z1,tz1,m1=parent.combined_predict(base,selector,raw1,batch=BATCH)
        for k in meter: meter[k]+=m1[k]
        for j,i in enumerate(second_decision):
            n_pred[i,1]=p1[j];n_logits[i,1]=z1[j];t_pred[i,1]=t1[j];t_logits[i,1]=tz1[j]
            records[i]["decision_charges"]+=1
            records[i]["phases"].append(dict(phase=1,packet=asdict(packets1[j]),
                necessity_prediction=int(p1[j]),target_prediction=int(t1[j])))
            if p1[j]==1:
                records[i]["acquisitions"].append(acquire(owners[i],int(t1[j])))
                second.append(i)
            else:
                records[i]["status"]="SUFFICIENT_CLASSIFICATION"

    final_decision=[i for i in second if driver.charge_decision(owners[i])]
    require(len(final_decision)==len(second),"Final decision budget unexpectedly exhausted")
    if final_decision:
        raw2,packets2=parent.encode_views([owners[i].state.view for i in final_decision])
        p2,z2,m2=parent.necessity_predict(base,raw2,batch=BATCH)
        for k in meter: meter[k]+=m2[k]
        for j,i in enumerate(final_decision):
            n_pred[i,2]=p2[j];n_logits[i,2]=z2[j]
            records[i]["decision_charges"]+=1
            records[i]["phases"].append(dict(phase=2,packet=asdict(packets2[j]),
                necessity_prediction=int(p2[j])))
            records[i]["status"]="SUFFICIENT_CLASSIFICATION" if p2[j]==0 else "UNRESOLVED"

    for i,o in enumerate(owners):
        records[i]["final"]=asdict(task.encode(o.state.view))
        records[i]["receipts"]=[asdict(r) for r in o.receipts]
        records[i]["pending"]=asdict(o.state.pending) if o.state.pending else None
        records[i]["runtime_terminal"]=o.state.terminal
    return records,dict(necessity_predictions=n_pred,necessity_logits=n_logits,
                        target_predictions=t_pred,target_logits=t_logits),meter

def logical_label(features,template_id,metadata):
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as parent
    return parent.post_label(features,template_id,metadata)

def teacher_for(features,template_id,metadata):
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as parent
    a=np.asarray(features,dtype=np.int32).reshape(1,72)
    return parent.target_teacher(a,np.asarray([template_id],dtype=np.int32),metadata)[0]

COUNTERS=("failed","initial_error","initial_replay_error","target0_error","selected_observed",
          "first_acquisition_error","post1_error","target1_error","repeated_target",
          "second_acquisition_error","post2_error","contract_error",
          "first_reservations","first_provider_calls","first_publications",
          "second_reservations","second_provider_calls","second_publications",
          "decision_charges","internal_charged","post1_expected_needs","post2_expected_needs")

def assess(record,template_id,metadata,world_bits,parent_initial_target):
    require(len(world_bits)==4 and all(type(v) is int and v in (0,1) for v in world_bits),
            "Exact scoring world required")
    initial=record["initial"];final=record["final"];ph=record["phases"];acq=record["acquisitions"]
    x=np.asarray(initial["features"],dtype=np.int64);f=np.asarray(final["features"],dtype=np.int64)
    p0=ph[0]["necessity_prediction"] if ph else -1
    t0=ph[0]["target_prediction"] if ph else -1
    valid0=teacher_for(initial["features"],template_id,metadata)
    initial_error=int(p0!=1)
    replay_error=int(t0!=int(parent_initial_target))
    target0_error=int(not (0<=t0<4 and bool(valid0[t0])))
    selected_observed=int(0<=t0<4 and x[48+4*t0]==1)

    def acq_ok(a,target_index,receipt_index):
        if a is None or not (0<=target_index<4):return False
        d=a["dispatch"];fid=initial["binding"]["fact_ids"][target_index]
        if d is None:return False
        return (a["input_index"]==target_index and a["fact_id"]==fid
            and a["action"]["status"]=="PENDING" and a["action"]["reason"]=="ACQUISITION_RESERVED"
            and a["action"]["internal_charged"]==1 and a["action"]["acquisition_reserved"]==1
            and d["status"]=="PUBLISHED" and d["reason"]=="OBSERVATION_ADMITTED"
            and d["internal_charged"]==2 and d["provider_calls"]==1 and d["fact_publications"]==1
            and receipt_index < len(record["receipts"])
            and record["receipts"][receipt_index]["fact_id"]==fid
            and record["receipts"][receipt_index]["value"]==world_bits[target_index]
            and record["receipts"][receipt_index]["action"]=="RETRIEVE")

    first=a0=acq[0] if len(acq)>0 else None
    first_ok=acq_ok(a0,t0,0)
    first_error=int(not first_ok)

    p1=ph[1]["necessity_prediction"] if len(ph)>1 else -1
    t1=ph[1]["target_prediction"] if len(ph)>1 else -1
    expected1=logical_label(ph[1]["packet"]["features"],template_id,metadata) if len(ph)>1 else None
    post1_error=int(expected1 is None or p1!=expected1)
    expected1_needs=int(expected1==1)
    valid1=teacher_for(ph[1]["packet"]["features"],template_id,metadata) if expected1==1 else np.zeros(4,dtype=bool)
    target1_error=int(expected1==1 and not (0<=t1<4 and bool(valid1[t1])))
    repeat=int(expected1==1 and t1==t0)
    selected_observed += int(expected1==1 and 0<=t1<4
                             and ph[1]["packet"]["features"][48+4*t1]==1)

    a1=acq[1] if len(acq)>1 else None
    second_should=expected1==1
    second_ok=acq_ok(a1,t1,1) if second_should else (a1 is None)
    second_error=int(not second_ok)

    p2=ph[2]["necessity_prediction"] if len(ph)>2 else -1
    expected2=logical_label(ph[2]["packet"]["features"],template_id,metadata) if len(ph)>2 else None
    post2_error=int(second_should and (expected2 is None or p2!=expected2))
    expected2_needs=int(expected2==1) if second_should else 0

    first_res=first["action"]["acquisition_reserved"] if first else 0
    first_calls=first["dispatch"]["provider_calls"] if first and first["dispatch"] else 0
    first_pubs=first["dispatch"]["fact_publications"] if first and first["dispatch"] else 0
    second_res=a1["action"]["acquisition_reserved"] if a1 else 0
    second_calls=a1["dispatch"]["provider_calls"] if a1 and a1["dispatch"] else 0
    second_pubs=a1["dispatch"]["fact_publications"] if a1 and a1["dispatch"] else 0
    internal_actions=sum(a["action"]["internal_charged"]+(a["dispatch"]["internal_charged"] if a["dispatch"] else 0)
                         for a in acq)
    total_charged=record["decision_charges"]+internal_actions

    structural=(record["pending"] is None and record["runtime_terminal"] is None
        and initial["binding"]["fact_ids"]==final["binding"]["fact_ids"]
        and initial["binding"]["request_id"]==final["binding"]["request_id"]
        and initial["binding"]["scope_id"]==final["binding"]["scope_id"]
        and np.array_equal(f[:46],x[:46]) and np.array_equal(f[64:70],x[64:70])
        and f[62]==x[62]-total_charged
        and f[63]==x[63]-first_res-second_res
        and f[71]==x[71]+total_charged
        and len(record["receipts"])==first_pubs+second_pubs)
    acquired=[t for t in (t0,t1 if second_should else -1) if 0<=t<4]
    for j in range(4):
        if j in acquired:
            structural=structural and list(f[46+4*j:50+4*j])==[1,2,1,world_bits[j]]
        else:
            structural=structural and np.array_equal(f[46+4*j:50+4*j],x[46+4*j:50+4*j])
            structural=structural and final["binding"]["reference_ids"][j]==initial["binding"]["reference_ids"][j]
    if first_pubs:
        structural=structural and list(final["binding"]["reference_ids"][t0])==[record["receipts"][0]["reference_id"]]
    if second_pubs:
        structural=structural and list(final["binding"]["reference_ids"][t1])==[record["receipts"][1]["reference_id"]]

    expected_decisions=2+(1 if second_should else 0)
    structural=structural and record["decision_charges"]==expected_decisions
    expected_status=("SUFFICIENT_CLASSIFICATION" if
        ((not second_should and p1==0) or (second_should and p2==0)) else "UNRESOLVED")
    structural=structural and record["status"]==expected_status
    contract_error=int(not structural)

    vals=(initial_error,replay_error,target0_error,selected_observed,first_error,post1_error,
          target1_error,repeat,second_error,post2_error,contract_error)
    return dict(
        failed=int(any(vals)),initial_error=initial_error,initial_replay_error=replay_error,
        target0_error=target0_error,selected_observed=int(selected_observed),
        first_acquisition_error=first_error,post1_error=post1_error,target1_error=target1_error,
        repeated_target=repeat,second_acquisition_error=second_error,post2_error=post2_error,
        contract_error=contract_error,
        first_reservations=int(first_res),first_provider_calls=int(first_calls),
        first_publications=int(first_pubs),second_reservations=int(second_res),
        second_provider_calls=int(second_calls),second_publications=int(second_pubs),
        decision_charges=int(record["decision_charges"]),internal_charged=int(total_charged),
        post1_expected_needs=expected1_needs,post2_expected_needs=expected2_needs)

def expected_order():
    return [(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS]

def gate(records):
    if [(r.get("base_seed"),r.get("head_seed")) for r in records] != expected_order():
        return False
    for r in records:
        if r.get("episodes")!=9536 or r.get("missing2_worlds")!=4608 or r.get("missing3_worlds")!=4928:
            return False
        if any(type(r.get(k)) is not int or r[k] < 0 for k in COUNTERS):
            return False
        if any(r[k]!=0 for k in ("failed","initial_error","initial_replay_error","target0_error",
            "selected_observed","first_acquisition_error","post1_error","target1_error",
            "repeated_target","second_acquisition_error","post2_error","contract_error")):
            return False
        second=r["post1_expected_needs"]
        if (r["first_reservations"],r["first_provider_calls"],r["first_publications"]) != (9536,9536,9536):
            return False
        if (r["second_reservations"],r["second_provider_calls"],r["second_publications"]) != (second,second,second):
            return False
        if r["decision_charges"] != 2*9536+second:
            return False
        if r["internal_charged"] != 5*9536+4*second:
            return False
        if r.get("final_sufficient",0)+r.get("final_needs",0)!=9536:
            return False
        for key in ("initial_necessity_max_abs_logit_difference","initial_target_max_abs_logit_difference"):
            d=r.get(key)
            if not isinstance(d,(int,float)) or not np.isfinite(d) or d>ATOL:
                return False
    return True

def manifest():
    return dict(
        experiment_id=EXPERIMENT_ID,stage=STAGE,parent_sha256=PARENT_SHA,
        acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        base_seeds=BASE_SEEDS,head_seeds=HEAD_SEEDS,arm=ARM,
        question="after first live learned acquisition remains NEEDS, same frozen components select a second new target, acquire once more, then reclassify actual state",
        changed="C189 one-acquisition stop extended to at most two sequential learned target acquisitions using one coherent world snapshot",
        layout="original C174 local fact layout only; no renaming intervention",
        cohort="all1768 PILOT NEEDS rows missing2/3 expanded over every complete 4-bit world consistent with initial visible facts",
        cohort_rows=1768,missing2_rows=1152,missing3_rows=616,
        worlds_per_selector=9536,missing2_worlds=4608,missing3_worlds=4928,
        selectors=9,blocks=9,episodes=85824,source_files=SOURCE_FILES,
        source_contract="16 complete four-fact C173 snapshots; one snapshot fixed per episode and shared by both possible acquisitions",
        initial_replay="one recomputed C189-identical policy output per unique initial TaskView; hidden world copies reuse that output; logits replay accepted C189 <=1e-6",
        max_acquisitions_per_episode=2,max_decisions_per_episode=3,
        first_decision_resources="11internal/4acquisitions/step8",
        after_first_acquisition_second_decision="7internal/3acquisitions/step12",
        after_second_acquisition_final_decision="3internal/2acquisitions/step16",
        target_teacher="scoring only: C188 influential target set at each actual visible state; never policy/provider input",
        necessity_teacher="scoring only: C174 logical necessity at each actual visible state",
        gate="all9 blocks zero initial/replay/target0/post1/target1/repeat/second-action/post2/contract errors; second reads exactly iff logical post1 NEEDS",
        base_checkpoint_loads=3,target_checkpoint_loads=9,
        logical_initial_episodes=85824,initial_unique_policy_rows=15912,
        initial_policy_forward_calls=18,initial_policy_cell_calls=126,
        live_second_rows="observed,0..85824",live_final_rows="observed,0..85824",
        training=0,fresh_seeds=0,network_calls=0,answer_generation=0,proof_checker_calls=0,core_evidence_writes=0,
        production_runtime_modified=False,gate_e_candidate=False,
        outputs=sorted(OUTPUTS),
        limits="same repeatedly inspected four development groups;exact-state initial policy memoization across hidden-world copies;max2 acquisitions;fixed RETRIEVE/provider;no third acquisition,learned tool/provider,renaming,language,answer/proof or full GateE")

MANIFEST_SHA = "ddca97a8c8de1687929b95e69f33c3073647017c3514871ae3db81d22605ef6d"

def precheck(c189_summary,*args):
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as previous
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(len(args)==15,"Fourteen prior summaries and repository root required")
    root=args[-1]
    p188,p181,p174,pins,protected=previous.precheck(args[0],*args[1:])
    require(audit.sha(c189_summary)==PARENT_SHA,"C189 summary changed")
    parent=audit.read_json(c189_summary);previous.validate_result(parent)
    require(parent["commit_sha"]==PARENT_EXECUTION and parent["status"]=="PASS"
            and previous.gate(parent["records"],parent["selector_replay"])
            and parent["source_blobs"]==pins,"Wrong accepted C189 source/result")
    protected[str(Path(c189_summary).resolve())]=PARENT_SHA
    for a in parent["artifacts"]:
        f=audit.safe_child(Path(c189_summary).resolve().parent,a["file"])
        require(f.is_file() and f.stat().st_size==a["serialized_bytes"] and audit.sha(f)==a["sha256"],
                "Changed C189 artifact:"+a["file"])
        protected[str(f.resolve())]=a["sha256"]
    pins=dict(pins)
    for name in previous.OWN:
        pins[name]=audit.git(root,"rev-parse",PARENT_EXECUTION+":"+name).decode().strip()
    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins)==111 and len(protected)==277,"Source/protected union drift")
    require(digest(manifest())==MANIFEST_SHA,"Manifest drift")
    return parent,p188,p181,p174,pins,protected

def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as previous
    names=previous.regression_modules(root)
    require(len(names)==len(set(names))==74,"Historical regression list drift")
    return names+["tests_lm.test_v05_c190_iterative_multimissing_acquisition"]

def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE
            and p["diagnostic_execution_valid"] is True,"Wrong/incomplete C190")
    require(p["episodes"]==85824 and len(p["records"])==9
            and p["base_checkpoint_loads"]==3 and p["target_checkpoint_loads"]==9
            and p["logical_initial_episodes"]==85824 and p["initial_unique_policy_rows"]==15912
            and p["initial_policy_forward_calls"]==18 and p["initial_policy_cell_calls"]==126
            and 0<=p["live_second_rows"]<=85824 and 0<=p["live_final_rows"]<=85824
            and p["total_base_rows"]==p["initial_unique_policy_rows"]+p["live_second_rows"]+p["live_final_rows"]
            and p["total_target_rows"]==p["initial_unique_policy_rows"]+p["live_second_rows"]
            and len(p["source_blobs"])==111 and len(p["input_sha256"])==277
            and len(p["artifacts"])==21 and {a["file"] for a in p["artifacts"]}==OUTPUTS,
            "Workload/coverage drift")
    require(all(p[k]==0 for k in ("new_training","fresh_seeds","network_calls",
                                  "answer_generation","proof_checker_calls","core_evidence_writes"))
            and p["production_runtime_modified"] is False and p["gate_e_candidate"] is False,
            "Scope drift")
    require(p["actual_file_reads"]==p["totals"]["first_provider_calls"]+p["totals"]["second_provider_calls"],
            "IO accounting drift")
    require(p["status"]==("PASS" if gate(p["records"]) else "FAIL"),"Gate drift")

def run(*,output_dir,expected_head,**parents):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as parent

    root=Path(__file__).resolve().parents[2]
    args=tuple(parents[n+"_summary"] for n in PRIOR_NAMES[1:])+(root,)
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"Dirty tracked tree")
    guard()
    p189,p188,p181,p174,pins,protected=precheck(parents["c189_summary"],*args)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter();artifacts=[];records=[]
    def record_file(name):
        f=out/name;artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,value):
        (out/name).write_bytes(blob(value));record_file(name)
    save("iterative-plan.json",dict(manifest(),source_blobs=pins))
    try:
        print("[C190] plan fixed; coherent worlds; at most two learned acquisitions; no third acquisition",flush=True)
        torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
        data,metadata=audit.load_data(Path(parents["c174_summary"]).resolve().parent,p174)
        raw_all=torch.from_numpy(data["features"].copy())
        valid=parent.target_teacher(data["features"],data["template_ids"],metadata)
        _,_,evfull,miss,profile=target.cohort_masks(raw_all,data["labels"],data["split_codes"],valid)
        full_ix=np.flatnonzero(evfull)
        full_missing=miss[evfull]
        require(len(full_ix)==1768
                and int((full_missing==2).sum())==1152
                and int((full_missing==3).sum())==616
                and profile["eval_discriminating"]==528
                and profile["eval_m2"]==376 and profile["eval_m3"]==152,
                "C190 cohort drift")
        raw=torch.from_numpy(data["features"][evfull].copy())
        expanded,source_rows,local_rows,world_codes=expand_worlds(raw,full_ix)
        require(len(expanded)==9536,"C190 expanded cohort drift")
        tids=data["template_ids"][evfull]
        groups=data["groups"][evfull]

        c189_dir=Path(parents["c189_summary"]).resolve().parent
        saved=load_parent_predictions(c189_dir/"episode-predictions.npz")
        require(np.array_equal(saved["row_indices"],full_ix),"C189 row identity drift")

        c181_dir=Path(parents["c181_summary"]).resolve().parent
        c188_dir=Path(parents["c188_summary"]).resolve().parent
        fits={f["seed"]:f for f in p181["fit_records"] if f["arm"]==ARM}
        selector_sha={(r["base_seed"],r["head_seed"]):r["head_sha256"] for r in p188["selector_results"]}
        require(set(fits)==set(BASE_SEEDS) and set(selector_sha)=={(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS},
                "Frozen checkpoint coverage drift")
        bases={};heads={};base_fp={};head_fp={}
        for b in BASE_SEEDS:
            bases[b]=frozen.restore_bare(c181_dir/f"probe-{b}-{ARM}.pt",b,ARM,fits[b]["final_sha256"])
            base_fp[b]=graph.fingerprint(bases[b])
            for h in HEAD_SEEDS:
                heads[b,h]=parent.restore_selector(c188_dir/f"selector-{b}-{h}.pt",b,h,selector_sha[b,h])
                head_fp[b,h]=target.head_fingerprint(heads[b,h])

        (out/"sources").mkdir()
        providers={};endpoints={}
        for code in range(16):
            name=f"sources/world-{code:02d}.json";bb=world_bytes(code)
            require(hashlib.sha256(bb).hexdigest()==SOURCE_FILES[name],"World source hash drift")
            (out/name).write_bytes(bb);record_file(name)
            sb=life.SourceBinding(f"C190-world-{code:02d}",hashlib.sha256(bb).hexdigest())
            p=life.FileSnapshotProvider(out/name,sb);providers[code]=p;endpoints[code]=life.Endpoint(sb,p)

        dense=dict(
            necessity_predictions=np.full((9,9536,3),-1,dtype=np.int8),
            necessity_logits=np.zeros((9,9536,3,2),dtype=np.float32),
            target_predictions=np.full((9,9536,2),-1,dtype=np.int8),
            target_logits=np.full((9,9536,2,4),-np.inf,dtype=np.float32))
        parent_replay=[];live_second=0;live_final=0
        live_meter=dict(rows=0,forward_calls=0,cell_calls=0)
        initial_meter=dict(rows=0,forward_calls=0,cell_calls=0)
        local_tensor=torch.from_numpy(local_rows.astype(np.int64))

        with gzip.open(out/"episode-traces.jsonl.gz","wt",encoding="utf-8",newline="\n") as trace:
            for bi,b in enumerate(BASE_SEEDS):
                for hi,h in enumerate(HEAD_SEEDS):
                    idx=bi*3+hi
                    cache,cache_meter=initial_policy_cache(raw,full_ix,bases[b],heads[b,h])
                    for k in initial_meter:initial_meter[k]+=cache_meter[k]
                    parent_np_unique=saved["necessity_predictions"][idx,0,:,0]
                    parent_nz_unique=saved["necessity_logits"][idx,0,:,0]
                    parent_tp_unique=saved["target_predictions"][idx,0]
                    parent_tz_unique=saved["target_logits"][idx,0]
                    unknown_unique=target.missing_mask(cache["raw"]).numpy()
                    nerr=int((cache["necessity_predictions"]!=parent_np_unique).sum())
                    terr=int((cache["target_predictions"]!=parent_tp_unique).sum())
                    ndelta=float(np.max(np.abs(cache["necessity_logits"]-parent_nz_unique)))
                    tdelta=float(np.max(np.abs(cache["target_logits"][unknown_unique]-parent_tz_unique[unknown_unique])))
                    require(nerr==terr==0 and ndelta<=ATOL and tdelta<=ATOL,
                            "Accepted C189 unique initial policy replay drift")
                    parent_replay.append(dict(base_seed=b,head_seed=h,
                        necessity_prediction_errors=nerr,target_prediction_errors=terr,
                        necessity_max_abs_logit_difference=ndelta,target_max_abs_logit_difference=tdelta))

                    initial=dict(
                        raw=cache["raw"][local_tensor],
                        necessity_predictions=cache["necessity_predictions"][local_rows],
                        target_predictions=cache["target_predictions"][local_rows],
                        necessity_logits=cache["necessity_logits"][local_rows],
                        target_logits=cache["target_logits"][local_rows])
                    before_reads=sum(p.reads for p in providers.values())
                    views=make_views(expanded,source_rows,world_codes,f"b{b}-h{h}")
                    observed,arrays,meter=run_block(views,world_codes,endpoints,bases[b],heads[b,h],initial=initial)
                    for k in live_meter:live_meter[k]+=meter[k]
                    dense["necessity_predictions"][idx]=arrays["necessity_predictions"]
                    dense["necessity_logits"][idx]=arrays["necessity_logits"]
                    dense["target_predictions"][idx]=arrays["target_predictions"]
                    dense["target_logits"][idx]=arrays["target_logits"]
                    live_second+=sum(len(r["phases"])>=2 for r in observed)
                    live_final+=sum(len(r["phases"])>=3 for r in observed)

                    parent_np=parent_np_unique[local_rows]
                    parent_tp=parent_tp_unique[local_rows]
                    require(np.array_equal(arrays["necessity_predictions"][:,0],parent_np)
                            and np.array_equal(arrays["target_predictions"][:,0],parent_tp),
                            "Expanded initial cache mapping drift")

                    scores=[]
                    for j,rec in enumerate(observed):
                        local=int(local_rows[j]);code=int(world_codes[j])
                        score=assess(rec,int(tids[local]),metadata,WORLD_BITS[code],int(parent_tp[j]))
                        score["initial_replay_error"] = int(score["initial_replay_error"] or
                            arrays["necessity_predictions"][j,0]!=parent_np[j])
                        score["failed"]=int(score["failed"] or score["initial_replay_error"])
                        scores.append(score)
                        trace.write(json.dumps(dict(base_seed=b,head_seed=h,
                            source_row=int(source_rows[j]),local_row=local,world_code=code,
                            score=score,trace=rec),sort_keys=True,separators=(",",":"),allow_nan=False)+"\n")

                    totals={k:sum(s[k] for s in scores) for k in COUNTERS}
                    reads=sum(p.reads for p in providers.values())-before_reads
                    require(reads==totals["first_provider_calls"]+totals["second_provider_calls"],
                            "Provider read accounting discrepancy")
                    final_sufficient=sum(
                        (s["post1_expected_needs"]==0) or
                        (s["post1_expected_needs"]==1 and s["post2_expected_needs"]==0)
                        for s in scores)
                    final_needs=9536-final_sufficient
                    rec=dict(base_seed=b,head_seed=h,episodes=9536,missing2_worlds=4608,missing3_worlds=4928,
                        initial_necessity_max_abs_logit_difference=ndelta,
                        initial_target_max_abs_logit_difference=tdelta,
                        initial_parent_necessity_prediction_errors=nerr,
                        initial_parent_target_prediction_errors=terr,
                        final_sufficient=int(final_sufficient),final_needs=int(final_needs),
                        by_group={str(g):{k:sum(scores[j][k] for j in np.flatnonzero(groups[local_rows]==g))
                            for k in COUNTERS} for g in sorted(set(groups.tolist()))},
                        **totals)
                    records.append(rec)
                    print(f"[C190] block={len(records)}/9 base={b} head={h} failed={rec['failed']} "
                          f"second_reads={rec['second_provider_calls']} final_needs={rec['final_needs']} reads={reads}",flush=True)

        record_file("episode-traces.jsonl.gz")
        np.savez_compressed(out/"episode-predictions.npz",**dense,row_indices=source_rows.astype("<i4"),
            local_rows=local_rows.astype("<i4"),world_codes=world_codes.astype(np.int8),
            base_seeds=np.repeat(np.asarray(BASE_SEEDS,dtype="<i4"),3),
            head_seeds=np.tile(np.asarray(HEAD_SEEDS,dtype="<i4"),3))
        record_file("episode-predictions.npz")
        save("parent-replay.json",parent_replay)
        save("episode-results.json",records)
        print("[C190] 2/3 all85824 coherent-world episodes collected; at most two acquisitions",flush=True)

        guard();precheck(parents["c189_summary"],*args)
        require([graph.fingerprint(bases[b]) for b in BASE_SEEDS]==[base_fp[b] for b in BASE_SEEDS],
                "Frozen C181 base changed")
        require([target.head_fingerprint(heads[b,h]) for b in BASE_SEEDS for h in HEAD_SEEDS] ==
                [head_fp[b,h] for b in BASE_SEEDS for h in HEAD_SEEDS],"Frozen C188 head changed")
        for f,hsh in protected.items():require(audit.sha(f)==hsh,"Protected input changed:"+f)
        for a in artifacts:require(audit.sha(out/a["file"])==a["sha256"],"Output changed:"+a["file"])

        totals={k:sum(r[k] for r in records) for k in COUNTERS}
        reads=sum(p.reads for p in providers.values());readbytes=sum(p.bytes_read for p in providers.values())
        result=dict(
            experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status="PASS" if gate(records) else "FAIL",diagnostic_execution_valid=True,
            C189_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,
            artifacts=artifacts,records=records,parent_replay=parent_replay,totals=totals,
            episodes=85824,logical_initial_episodes=85824,
            initial_unique_policy_rows=initial_meter["rows"],
            initial_policy_forward_calls=initial_meter["forward_calls"],
            initial_policy_cell_calls=initial_meter["cell_calls"],
            live_second_rows=live_second,live_final_rows=live_final,
            total_base_rows=initial_meter["rows"]+live_second+live_final,
            total_target_rows=initial_meter["rows"]+live_second,
            live_inference_forward_calls=live_meter["forward_calls"],
            live_inference_cell_calls=live_meter["cell_calls"],
            base_checkpoint_loads=3,target_checkpoint_loads=9,
            actual_acquisitions=totals["first_provider_calls"]+totals["second_provider_calls"],
            actual_file_reads=reads,provider_bytes_read=readbytes,
            taskview_fact_publications=totals["first_publications"]+totals["second_publications"],
            new_training=0,fresh_seeds=0,network_calls=0,answer_generation=0,
            proof_checker_calls=0,core_evidence_writes=0,
            production_runtime_modified=False,gate_e_candidate=False,
            environment=dict(torch=torch.__version__,numpy=np.__version__,device="cpu",dtype="float32",threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=[
                "same four repeatedly inspected development groups;not independent final confirmation",
                "identical initial TaskViews across hidden-world copies share one recomputed frozen policy output;world code is not a cache key or model input",
                "maximum two acquisitions;remaining NEEDS never triggers a third acquisition",
                "fixed RETRIEVE and one coherent local snapshot provider;tool/provider choice remains handwritten",
                "identity/original C174 local layout only;renaming path not retested",
                "logical teachers are scoring only;no answer/proof/language/larger expressions"])
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C190] 3/3 source/output preservation checked",flush=True)
        print("=== C190 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
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

if __name__=="__main__":
    main()
