"""C189: frozen learned multi-missing target -> one real acquisition -> live reclassification.

Diagnostic only. Reuse all nine accepted C188 selector heads and their three frozen
C181 INTERNAL_SEMANTICS bases. The initial necessity decision and learned target
selection share one base forward. Exactly one RETRIEVE may execute; post state is
reclassified once and never triggers a second acquisition.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import gzip
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import torch
from torch import nn

EXPERIMENT_ID = "C189-v5e-live-multimissing-target-acquisition"
STAGE = "V5-E-LIVE-MULTIMISSING-TARGET-ACQUISITION"
BASE = "2edadff6f8fab1c3c26da46adee630d12e433be8"
PARENT_EXECUTION = "683d795b12d4f0aada4850dcac2a010e699882ad"
PARENT_SHA = "2a3ef27e9dec281159197775a15771b31b4945c9a0fa84787b4b812e9efb4153"
BASE_SEEDS = (181001, 181002, 181003)
HEAD_SEEDS = (188001, 188002, 188003)
ARM = "INTERNAL_SEMANTICS"
BITS = (0, 1)
BATCH = 1024
PRIOR_NAMES = ("c188","c187","c186","c185","c184","c183","c182","c181","c180",
               "c179","c178","c177","c176","c174")
OWN = ("fold_lm/v05_benchmarks/gate_e_c189_live_multimissing_target.py",
       "tests_lm/test_v05_c189_live_multimissing_target.py",
       "tools/run_c189.ps1",
       "docs/experiment-ledger-addendum-c189-preregistration.md")
SOURCES = {
    "sources/fact-0-completion-0.json": "d3d693b1ce3d22b31f3826feace8eb511eb3e8f5b427ba1ac2fb607af8419dc2",
    "sources/fact-1-completion-0.json": "1b6b28bab6436fb62dac757d629d4eda6da45c098f70f5f3414a6b1afc9fd292",
    "sources/fact-2-completion-0.json": "ff89d9d08d5cf91452059f835997a2001c2c27e39a341e35294a28c564beca5b",
    "sources/fact-3-completion-0.json": "6182708e781d9f0f73cd3df20c1257a9611d8d3ed02f4499992e700545b249c2",
    "sources/fact-0-completion-1.json": "aa684e21cc075142892e05a65d260a3967abde5da7b3996d58b924df7df8f7d6",
    "sources/fact-1-completion-1.json": "43984ace8084b91f3bb8ec74c1da6f97b3ff95a988fe62373f7a07647ceb3e56",
    "sources/fact-2-completion-1.json": "d6fb4451badea2e3d8fe8bceb80464c891efae5f7323c1509599c9eca5e2b70c",
    "sources/fact-3-completion-1.json": "09c4b6c269cbfbf1ab3c9cf9ce22cdcd5ded0abbf2fd601d8a1e50be2a6e9ea9",
}
OUTPUTS = {"live-target-plan.json","selector-replay.json","episode-results.json",
           "episode-traces.jsonl.gz","episode-predictions.npz"} | set(SOURCES)
ATOL = 1e-6
EXPECTED_TESTS = 1449


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def source_bytes(fact_index, bit):
    require(type(fact_index) is int and 0 <= fact_index < 4 and
            type(bit) is int and bit in BITS, "Registered source identity required")
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    data = driver.fixture_bytes(fact_index, bit)
    name = f"sources/fact-{fact_index}-completion-{bit}.json"
    require(hashlib.sha256(data).hexdigest() == SOURCES[name],
            "Registered source bytes drift")
    return data


def encode_views(views):
    """Direct original C174 layout; C189 intentionally adds no rename intervention."""
    from fold_lm.v05 import structured_task_input as task
    require(type(views) is list and views, "Nonempty view batch required")
    packets = [task.encode(v) for v in views]
    require(all(task.decode(p) == v for p, v in zip(packets, views, strict=True)),
            "TaskView roundtrip drift")
    raw = torch.tensor([p.features for p in packets], dtype=torch.int32)
    require(raw.shape == (len(views),72), "Policy packet width drift")
    return raw, packets


def restore_selector(path, base_seed, head_seed, expected_sha):
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as parent
    require((base_seed,head_seed) in {(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS},
            "Unregistered selector identity")
    payload = torch.load(path, map_location="cpu", weights_only=True)
    require((payload["base_seed"],payload["head_seed"],payload["schema"],
             payload["feature_width"],payload["steps"]) ==
            (base_seed,head_seed,"c188-target-selector-v1",parent.FEATURES,parent.STEPS),
            "Selector checkpoint metadata drift")
    model = parent.TargetSelector()
    model.load_state_dict(payload["state_dict"], strict=True)
    model.eval()
    require(parent.head_fingerprint(model) == payload["head_sha256"] == expected_sha,
            "Selector checkpoint fingerprint drift")
    return model


def load_parent_predictions(path):
    p = Path(path)
    require(p.is_file() and p.stat().st_size < 2_000_000,
            "Unexpected C188 prediction artifact size")
    with np.load(p, allow_pickle=False) as z:
        require(set(z.files) == {"row_indices","predictions","logits","base_seeds","head_seeds"},
                "C188 prediction schema drift")
        out = {k:z[k].copy() for k in z.files}
    require(out["row_indices"].shape == (1768,) and out["row_indices"].dtype.kind in "iu"
            and out["predictions"].shape == (9,1768)
            and out["logits"].shape == (9,1768,4) and out["logits"].dtype == np.float32
            and out["base_seeds"].tolist() == [b for b in BASE_SEEDS for _ in HEAD_SEEDS]
            and out["head_seeds"].tolist() == [h for _ in BASE_SEEDS for h in HEAD_SEEDS],
            "C188 prediction array drift")
    require(set(np.unique(out["predictions"]).tolist()) <= {0,1,2,3},
            "Invalid saved target prediction")
    return out


def combined_predict(base, selector, raw, *, batch=BATCH):
    """One frozen base forward emits necessity plus hidden states for the target head."""
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target

    require(type(base) is graph.SharedGraphProbe and base.arm == graph.ARMS[1],
            "Frozen TREE_LINKS base required")
    require(type(selector) is target.TargetSelector and type(batch) is int and batch > 0,
            "Frozen target head required")
    target.missing_mask(raw)
    positions = target.leaf_positions(raw)
    scaled = binding.prepare_pair(raw)[1]
    unknown = target.missing_mask(raw)
    base_fp = graph.fingerprint(base)
    head_fp = target.head_fingerprint(selector)
    old = (base.calls,base.cell_calls,base.rows)
    n_logits=[]; t_logits=[]
    started=time.perf_counter()
    with torch.inference_mode():
        for lo in range(0,len(raw),batch):
            hi=min(len(raw),lo+batch)
            states=[]
            handle=base.cell.register_forward_hook(
                lambda module,args,output: states.append(output.detach()))
            try:
                nz=base(scaled[lo:hi])
            finally:
                handle.remove()
            require(len(states)==7 and nz.shape==(hi-lo,2)
                    and torch.isfinite(nz).all().item(), "Combined base forward drift")
            bank=torch.stack(states,dim=1)
            flat=bank.reshape(hi-lo,-1)[:,None,:].expand(-1,4,-1)
            one=nn.functional.one_hot(positions[lo:hi],num_classes=7).to(torch.float32)
            features=torch.cat((flat,one),dim=2)
            tz=selector(features)
            tz=tz.masked_fill(~unknown[lo:hi],float("-inf"))
            require(torch.isfinite(tz[unknown[lo:hi]]).all().item()
                    and torch.isneginf(tz[~unknown[lo:hi]]).all().item(),
                    "Target score mask/nonfinite drift")
            n_logits.append(nz.cpu()); t_logits.append(tz.cpu())
    nz=torch.cat(n_logits); tz=torch.cat(t_logits)
    calls=(len(raw)+batch-1)//batch
    require(graph.fingerprint(base)==base_fp
            and target.head_fingerprint(selector)==head_fp
            and (base.calls-old[0],base.cell_calls-old[1],base.rows-old[2]) ==
                (calls,7*calls,len(raw)),
            "Frozen combined inference mutated weights/meters")
    return (nz.argmax(1).numpy().astype(np.int8),
            tz.argmax(1).numpy().astype(np.int8),
            nz.numpy(),tz.numpy(),
            dict(rows=len(raw),forward_calls=calls,cell_calls=7*calls,
                 wall_clock_seconds=time.perf_counter()-started))


def necessity_predict(base, raw, *, batch=BATCH):
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
    p,z,m = graph.predict(base,binding.prepare_pair(raw)[1],batch=batch)
    return p.numpy().astype(np.int8),z.numpy(),m


def target_teacher(features, template_ids, metadata):
    """Scoring/training-label logic only; never passed to policy or transport."""
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as parent
    return parent.influence_masks(features,template_ids,metadata)


def post_label(row, template_id, metadata):
    from fold_lm.v05_benchmarks import gate_e_c174_learned_necessity as c174
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as parent
    visible=parent.visible_tuple(row)
    table=tuple(int(v) for v in metadata[int(template_id)]["truth_table"])
    return int(c174.label_for(table,visible))


def bind_selected_endpoint(owner, endpoints, target_index):
    """Trusted runtime wiring after learned selection; preserve exact RuntimeState."""
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    require(type(target_index) is int and 0 <= target_index < 4,
            "Local target index required")
    view=owner.state.view
    require(view.facts[target_index].status=="UNOBSERVED",
            "Selected endpoint target must be unknown")
    fid=view.facts[target_index].fact_id
    require(fid in endpoints and type(endpoints[fid]) is life.Endpoint,
            "Selected target endpoint unavailable")
    state=owner.state
    rebound=life.AcquisitionOwner(state,{"RETRIEVE":endpoints[fid]},max_dispatches=1)
    require(rebound.state == state, "Endpoint binding changed RuntimeState")
    return rebound


def acquire_selected(owner, target_index):
    """C172/C173 execute the raw learned local target; no target repair."""
    from fold_lm.v05 import structured_action_runtime as action
    require(type(target_index) is int and 0 <= target_index < 4,
            "Local target index required")
    view=owner.state.view
    require(view.facts[target_index].status=="UNOBSERVED",
            "Learned target must currently be unknown")
    fid=view.facts[target_index].fact_id
    transition=owner.apply(action.propose(owner.state,"RETRIEVE",fact_index=target_index))
    dispatched=None
    if transition.result.status=="PENDING":
        dispatched=owner.dispatch(transition.result.intent.intent_id)
    return dict(input_index=target_index,fact_id=fid,action=asdict(transition.result),
                dispatch=asdict(dispatched) if dispatched else None)


def run_block(views, endpoints, base, selector):
    """Independent episodes; one shared initial forward, max one acquisition, one post decision."""
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05 import structured_action_runtime as action
    from fold_lm.v05 import structured_task_input as task
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver

    require(views and all(sum(f.status=="UNOBSERVED" for f in v.facts) in (2,3)
                          for v in views), "C189 requires initial missing2/3 rows")
    owners=[life.AcquisitionOwner(action.RuntimeState(v),{},max_dispatches=1) for v in views]
    n=len(views)
    records=[dict(initial=asdict(task.encode(v)),phases=[],acquisition=None,
                  decision_charges=0,status="UNRESOLVED") for v in views]
    necessity=np.full((n,2),-1,dtype=np.int8)
    nlogits=np.zeros((n,2,2),dtype=np.float32)
    target_pred=np.full(n,-1,dtype=np.int8)
    target_logits=np.full((n,4),-np.inf,dtype=np.float32)
    meter=dict(rows=0,forward_calls=0,cell_calls=0)

    active=[i for i,o in enumerate(owners) if driver.charge_decision(o)]
    require(len(active)==n, "Initial decision budget unexpectedly exhausted")
    raw,packets=encode_views([owners[i].state.view for i in active])
    p,t,z,tz,m=combined_predict(base,selector,raw)
    for k in meter: meter[k]+=m[k]
    post=[]
    for j,i in enumerate(active):
        necessity[i,0]=p[j]; nlogits[i,0]=z[j]
        target_pred[i]=t[j]; target_logits[i]=tz[j]
        records[i]["decision_charges"]+=1
        records[i]["phases"].append(dict(
            phase=0,packet=asdict(packets[j]),
            necessity_prediction=int(p[j]),target_prediction=int(t[j])))
        if p[j]==1:
            owners[i]=bind_selected_endpoint(owners[i],endpoints,int(t[j]))
            records[i]["acquisition"]=acquire_selected(owners[i],int(t[j]))
            post.append(i)
        else:
            records[i]["status"]="SUFFICIENT_CLASSIFICATION"

    post_active=[i for i in post if driver.charge_decision(owners[i])]
    require(len(post_active)==len(post), "Post decision budget unexpectedly exhausted")
    if post_active:
        raw2,packets2=encode_views([owners[i].state.view for i in post_active])
        p2,z2,m2=necessity_predict(base,raw2)
        for k in meter: meter[k]+=m2[k]
        for j,i in enumerate(post_active):
            necessity[i,1]=p2[j]; nlogits[i,1]=z2[j]
            records[i]["decision_charges"]+=1
            records[i]["phases"].append(dict(
                phase=1,packet=asdict(packets2[j]),
                necessity_prediction=int(p2[j])))
            records[i]["status"]="SUFFICIENT_CLASSIFICATION" if p2[j]==0 else "UNRESOLVED"

    for i,o in enumerate(owners):
        records[i]["final"]=asdict(task.encode(o.state.view))
        records[i]["receipts"]=[asdict(r) for r in o.receipts]
        records[i]["pending"]=asdict(o.state.pending) if o.state.pending else None
        records[i]["runtime_terminal"]=o.state.terminal
    return records,dict(necessity_predictions=necessity,necessity_logits=nlogits,
                        target_predictions=target_pred,target_logits=target_logits),meter


def assess(record, valid_targets, source_row, template_id, metadata, bit, parent_target):
    """Post-hoc scoring only. Never changes target/action/evidence/prediction."""
    require(type(bit) is int and bit in BITS and
            type(parent_target) in (int,np.int8,np.int16,np.int32,np.int64),
            "Registered scoring inputs required")
    initial,final=record["initial"],record["final"]
    x=np.asarray(initial["features"],dtype=np.int64)
    f=np.asarray(final["features"],dtype=np.int64)
    phases=record["phases"]
    p0=phases[0]["necessity_prediction"] if phases else -1
    selected=phases[0]["target_prediction"] if phases else -1
    post=phases[1]["necessity_prediction"] if len(phases)>1 else -1
    valid=np.asarray(valid_targets,dtype=bool)
    require(valid.shape==(4,), "Target teacher row width drift")
    target_ok=0 <= selected < 4 and bool(valid[selected])
    target_replay_ok=selected == int(parent_target)
    selected_observed=int(0 <= selected < 4 and x[48+4*selected]==1)

    acq=record["acquisition"]; dispatch=acq["dispatch"] if acq else None
    reserved=acq["action"]["acquisition_reserved"] if acq else 0
    calls=dispatch["provider_calls"] if dispatch else 0
    pubs=dispatch["fact_publications"] if dispatch else 0
    receipts=record["receipts"]
    structural=True
    if not (0 <= selected < 4):
        structural=False
    else:
        selected_fid=initial["binding"]["fact_ids"][selected]
        structural = structural and x[48+4*selected]==0
        structural = structural and acq is not None and acq["input_index"]==selected and acq["fact_id"]==selected_fid
        structural = structural and acq["action"]["status"]=="PENDING" and acq["action"]["reason"]=="ACQUISITION_RESERVED"
        structural = structural and acq["action"]["internal_charged"]==1 and reserved==1
        structural = structural and dispatch is not None and dispatch["status"]=="PUBLISHED"
        structural = structural and dispatch["reason"]=="OBSERVATION_ADMITTED"
        structural = structural and dispatch["internal_charged"]==2 and calls==pubs==1
        structural = structural and len(receipts)==1 and receipts[0]["fact_id"]==selected_fid
        structural = structural and receipts[0]["value"]==bit and receipts[0]["action"]=="RETRIEVE"
        structural = structural and receipts[0]["request_id"]==initial["binding"]["request_id"]
        structural = structural and receipts[0]["scope_id"]==initial["binding"]["scope_id"]
        structural = structural and dispatch["evidence"]==receipts[0]
        structural = structural and list(f[46+4*selected:50+4*selected])==[1,2,1,bit]
        structural = structural and list(final["binding"]["reference_ids"][selected])==[receipts[0]["reference_id"]]
        for j in range(4):
            if j != selected:
                structural = structural and np.array_equal(f[46+4*j:50+4*j],x[46+4*j:50+4*j])
                structural = structural and final["binding"]["reference_ids"][j]==initial["binding"]["reference_ids"][j]
    charges=record["decision_charges"]+(acq["action"]["internal_charged"] if acq else 0)+(dispatch["internal_charged"] if dispatch else 0)
    structural = structural and f[62]==x[62]-charges and f[63]==x[63]-reserved and f[71]==x[71]+charges
    structural = structural and np.array_equal(f[64:70],x[64:70]) and np.array_equal(f[:46],x[:46])
    structural = structural and initial["binding"]["fact_ids"]==final["binding"]["fact_ids"]
    structural = structural and initial["binding"]["request_id"]==final["binding"]["request_id"]
    structural = structural and initial["binding"]["scope_id"]==final["binding"]["scope_id"]
    structural = structural and record["pending"] is None and record["runtime_terminal"] is None
    expected_post=post_label(final["features"],template_id,metadata) if pubs==1 else None
    post_error=int(expected_post is None or post != expected_post)
    status_ok=(record["status"]==("SUFFICIENT_CLASSIFICATION" if post==0 else "UNRESOLVED")) if acq else True
    structural=structural and status_ok and record["decision_charges"]==(2 if acq else 1)
    initial_error=int(p0 != 1)
    target_error=int(not target_ok)
    replay_error=int(not target_replay_ok)
    missed=int(acq is None or calls!=1 or pubs!=1)
    contract=int(not structural)
    return dict(
        failed=int(bool(initial_error or target_error or replay_error or missed or post_error or contract)),
        initial_error=initial_error,target_error=target_error,target_replay_error=replay_error,
        selected_observed=selected_observed,missed_acquisition=missed,
        post_error=post_error,contract_error=contract,
        post_expected=-1 if expected_post is None else int(expected_post),
        post_prediction=int(post),reservations=int(reserved),provider_calls=int(calls),
        publications=int(pubs),decision_charges=int(record["decision_charges"]),
        internal_charged=int(charges))


COUNTERS=("failed","initial_error","target_error","target_replay_error","selected_observed",
          "missed_acquisition","post_error","contract_error","reservations","provider_calls",
          "publications","decision_charges","internal_charged")


def expected_order():
    return [(b,h,bit) for b in BASE_SEEDS for h in HEAD_SEEDS for bit in BITS]


def gate(records, replay):
    if [(r.get("base_seed"),r.get("head_seed"),r.get("completion")) for r in records] != expected_order():
        return False
    if not isinstance(replay,list) or [(r.get("base_seed"),r.get("head_seed")) for r in replay] != [
            (b,h) for b in BASE_SEEDS for h in HEAD_SEEDS]:
        return False
    if any(r.get("predictions_equal") is not True or
           not isinstance(r.get("max_abs_logit_difference"),(int,float)) or
           not np.isfinite(r["max_abs_logit_difference"]) or
           r["max_abs_logit_difference"] > ATOL for r in replay):
        return False
    for r in records:
        if r.get("episodes")!=1768 or r.get("discriminating_rows")!=528:
            return False
        if any(type(r.get(k)) is not int or r[k] < 0 for k in COUNTERS):
            return False
        if any(r[k] != 0 for k in ("failed","initial_error","target_error","target_replay_error",
                                     "selected_observed","missed_acquisition","post_error","contract_error")):
            return False
        if (r["reservations"],r["provider_calls"],r["publications"]) != (1768,1768,1768):
            return False
        if r["decision_charges"]!=3536 or r["internal_charged"]!=8840:
            return False
        if r.get("discriminating_target_errors") != 0:
            return False
        delta=r.get("initial_target_max_abs_logit_difference")
        if not isinstance(delta,(int,float)) or not np.isfinite(delta) or delta > ATOL:
            return False
        if r.get("post_sufficient",0)+r.get("post_needs",0) != 1768:
            return False
    return True


def manifest():
    return dict(
        experiment_id=EXPERIMENT_ID,stage=STAGE,parent_sha256=PARENT_SHA,
        acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        base_seeds=BASE_SEEDS,head_seeds=HEAD_SEEDS,arm=ARM,bits=BITS,
        question="frozen learned necessity+target drives one real selected-fact RETRIEVE then reclassifies actual multi-missing state",
        changed="offline C188 target selection connected to actual C172/C173 acquisition; no learned weights change",
        initial_policy="one shared frozen C181 base forward emits necessity and hidden states; frozen C188 head selects target",
        post_policy="one frozen C181 necessity-only decision after actual admission; no second acquisition",
        layout="original C174 local fact layout only; no C184 renaming intervention in C189",
        cohort="all1768 PILOT NEEDS rows with missing2/3; discriminating target subset528 retained",
        blocks=18,episodes=31824,episodes_per_block=1768,discriminating_rows_per_block=528,
        completion_bits=2,selectors=9,source_files=SOURCES,
        source_contract="eight C185-format single-fact files; learned target chooses which exact endpoint is bound; only selected fact may publish",
        target_replay_rows=15912,static_base_feature_rows=5304,static_base_feature_forwards=6,
        live_initial_base_rows=31824,live_post_base_rows="measured,0..31824",
        live_target_rows=31824,total_base_rows_max=68952,
        base_checkpoint_loads=3,target_checkpoint_loads=9,
        training=0,fresh_seeds=0,max_acquisitions_per_episode=1,max_post_decisions=1,
        ideal_reads=31824,ideal_publications=31824,
        initial_resources="original12internal/4acquisitions/step7; one combined learned decision charged before input",
        expected_live_first="11internal/4acquisitions/step8",
        expected_live_post="after action1+dispatch2+postdecision1 =>7internal/3acquisitions/step12",
        target_teacher="scoring only: C188 influential-target set; never policy/provider input",
        post_teacher="scoring only: C174 logical necessity on actual final visible facts",
        gate="all9x2 blocks zero initial/target/replay/post/contract errors; exact one read/publication each; target logits replay C188 <=1e-6",
        actual_network_calls=0,answer_generation=0,proof_checker_calls=0,core_evidence_writes=0,
        production_runtime_modified=False,gate_e_candidate=False,
        outputs=sorted(OUTPUTS),
        limits="same four repeatedly inspected development groups;one acquisition only;fixed RETRIEVE/provider;no iterative planning,renaming,language,answer/proof or full GateE")


MANIFEST_SHA = "6acccb0b116a57a34e4f91733d0a15ac345d144ba9b6cb0db8a1e7af4ecf0e47"


def precheck(c188_summary, *args):
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as previous
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    require(len(args)==14, "Thirteen prior summaries and repository root required")
    root=args[-1]
    p181,p174,pins,protected=previous.precheck(args[0],*args[1:])
    require(audit.sha(c188_summary)==PARENT_SHA, "C188 summary changed")
    parent=audit.read_json(c188_summary); previous.validate_result(parent)
    require(parent["commit_sha"]==PARENT_EXECUTION and parent["status"]=="PASS"
            and previous.selector_gate(parent["selector_results"],parent["frequency_reference"])
            and parent["source_blobs"]==pins, "Wrong accepted C188 source/result")
    protected[str(Path(c188_summary).resolve())]=PARENT_SHA
    for a in parent["artifacts"]:
        f=audit.safe_child(Path(c188_summary).resolve().parent,a["file"])
        require(f.is_file() and f.stat().st_size==a["serialized_bytes"] and audit.sha(f)==a["sha256"],
                "Changed C188 artifact:"+a["file"])
        protected[str(f.resolve())]=a["sha256"]
    pins=dict(pins)
    for name in previous.OWN:
        pins[name]=audit.git(root,"rev-parse",PARENT_EXECUTION+":"+name).decode().strip()
    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    require(len(pins)==107 and len(protected)==258, "Source/protected union drift")
    require(digest(manifest())==MANIFEST_SHA, "Manifest drift")
    return parent,p181,p174,pins,protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as previous
    names=previous.regression_modules(root)
    require(len(names)==len(set(names))==73, "Historical regression list drift")
    return names+["tests_lm.test_v05_c189_live_multimissing_target"]


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE
            and p["diagnostic_execution_valid"] is True, "Wrong/incomplete C189")
    require(p["episodes"]==31824 and len(p["records"])==18 and len(p["selector_replay"])==9
            and p["base_checkpoint_loads"]==3 and p["target_checkpoint_loads"]==9
            and p["target_replay_rows"]==15912 and p["live_initial_rows"]==31824
            and 0 <= p["live_post_rows"] <= 31824
            and p["total_base_rows"]==5304+31824+p["live_post_rows"]
            and p["total_target_rows"]==15912+31824
            and len(p["source_blobs"])==107 and len(p["input_sha256"])==258
            and len(p["artifacts"])==13 and {a["file"] for a in p["artifacts"]}==OUTPUTS,
            "Workload/coverage drift")
    require(all(p[k]==0 for k in ("new_training","fresh_seeds","network_calls",
                                  "answer_generation","proof_checker_calls","core_evidence_writes"))
            and p["production_runtime_modified"] is False and p["gate_e_candidate"] is False,
            "Scope drift")
    require(p["actual_file_reads"]==p["totals"]["provider_calls"]==p["totals"]["publications"],
            "IO accounting drift")
    require(p["status"]==("PASS" if gate(p["records"],p["selector_replay"]) else "FAIL"),
            "Gate drift")


def run(*, output_dir, expected_head, **parents):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05_benchmarks import gate_e_c174_learned_necessity as c174
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as binding
    from fold_lm.v05_benchmarks import gate_e_c179_shared_graph as graph
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target

    root=Path(__file__).resolve().parents[2]
    args=tuple(parents[n+"_summary"] for n in PRIOR_NAMES[1:])+(root,)
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"Dirty tracked tree")
    guard()
    p188,p181,p174,pins,protected=precheck(parents["c188_summary"],*args)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter(); artifacts=[]; records=[]; replay=[]
    def record_file(name):
        f=out/name; artifacts.append(dict(file=name,sha256=audit.sha(f),serialized_bytes=f.stat().st_size))
    def save(name,value):
        (out/name).write_bytes(blob(value)); record_file(name)
    save("live-target-plan.json",dict(manifest(),source_blobs=pins))
    try:
        print("[C189] plan fixed; frozen learned target drives exactly one real RETRIEVE; no second acquisition",flush=True)
        torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
        data,metadata=audit.load_data(Path(parents["c174_summary"]).resolve().parent,p174)
        raw_all=torch.from_numpy(data["features"].copy())
        valid=target_teacher(data["features"],data["template_ids"],metadata)
        _,_,evfull,miss,profile=target.cohort_masks(raw_all,data["labels"],data["split_codes"],valid)
        full_ix=np.flatnonzero(evfull)
        require(len(full_ix)==1768 and profile["eval_discriminating"]==528
                and (data["labels"][evfull]==1).all(), "C189 cohort drift")
        raw=torch.from_numpy(data["features"][evfull].copy())
        valid_full=valid[evfull]; groups=data["groups"][evfull]; tids=data["template_ids"][evfull]
        vc=valid_full.sum(1); m=miss[evfull]
        discriminating=(vc<m)
        require(int(discriminating.sum())==528, "C189 discriminating subset drift")

        parent_dir=Path(parents["c188_summary"]).resolve().parent
        saved=load_parent_predictions(parent_dir/"pilot-predictions.npz")
        require(np.array_equal(saved["row_indices"],full_ix), "C188 row identity drift")
        c181_dir=Path(parents["c181_summary"]).resolve().parent
        fits={f["seed"]:f for f in p181["fit_records"] if f["arm"]==ARM}
        selector_sha={(r["base_seed"],r["head_seed"]):r["head_sha256"] for r in p188["selector_results"]}
        require(set(fits)==set(BASE_SEEDS) and set(selector_sha)=={(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS},
                "Frozen checkpoint coverage drift")
        bases={}; heads={}; base_fp={}; head_fp={}
        for b in BASE_SEEDS:
            bases[b]=frozen.restore_bare(c181_dir/f"probe-{b}-{ARM}.pt",b,ARM,fits[b]["final_sha256"])
            base_fp[b]=graph.fingerprint(bases[b])
            for h in HEAD_SEEDS:
                heads[b,h]=restore_selector(parent_dir/f"selector-{b}-{h}.pt",b,h,selector_sha[b,h])
                head_fp[b,h]=target.head_fingerprint(heads[b,h])

        static_rows=static_forwards=static_cells=0
        for bi,b in enumerate(BASE_SEEDS):
            features,meter=target.capture_fact_features(
                bases[b],binding.prepare_pair(raw)[1],raw,batch=BATCH)
            static_rows+=meter["rows"];static_forwards+=meter["forward_calls"];static_cells+=meter["cell_calls"]
            unknown=target.missing_mask(raw)
            for hi,h in enumerate(HEAD_SEEDS):
                idx=bi*3+hi
                pred,z,_=target.predict_selector(heads[b,h],features,unknown,batch=BATCH)
                znp=z.numpy(); finite=unknown.numpy()
                delta=float(np.max(np.abs(znp[finite]-saved["logits"][idx][finite])))
                eq=bool(np.array_equal(pred.numpy(),saved["predictions"][idx]))
                require(eq and delta<=ATOL, "Accepted C188 selector replay drift")
                replay.append(dict(base_seed=b,head_seed=h,predictions_equal=eq,
                                   max_abs_logit_difference=delta))
        require((static_rows,static_forwards,static_cells)==(5304,6,42),
                "Static replay workload drift")
        save("selector-replay.json",replay)
        print("[C189] 1/3 all15912 C188 target predictions replayed exactly; 1768 live source rows fixed",flush=True)

        (out/"sources").mkdir()
        providers={}; endpoints={bit:{} for bit in BITS}
        for bit in BITS:
            for i,fid in enumerate(driver.FACT_IDS):
                name=f"sources/fact-{i}-completion-{bit}.json"; data_bytes=source_bytes(i,bit)
                (out/name).write_bytes(data_bytes); record_file(name)
                sb=life.SourceBinding(f"C185-fixture-{i}-{bit}",hashlib.sha256(data_bytes).hexdigest())
                provider=life.FileSnapshotProvider(out/name,sb)
                providers[i,bit]=provider
                endpoints[bit][fid]=life.Endpoint(sb,provider)

        dense=dict(
            necessity_predictions=np.full((9,2,1768,2),-1,dtype=np.int8),
            necessity_logits=np.zeros((9,2,1768,2,2),dtype=np.float32),
            target_predictions=np.full((9,2,1768),-1,dtype=np.int8),
            target_logits=np.full((9,2,1768,4),-np.inf,dtype=np.float32),
            post_labels=np.full((9,2,1768),-1,dtype=np.int8))
        live_meter=dict(rows=0,forward_calls=0,cell_calls=0);live_post_rows=0

        with gzip.open(out/"episode-traces.jsonl.gz","wt",encoding="utf-8",newline="\n") as trace:
            for bi,b in enumerate(BASE_SEEDS):
                for hi,h in enumerate(HEAD_SEEDS):
                    idx=bi*3+hi
                    for bit in BITS:
                        views=driver.make_views(raw,full_ix,driver.LAYOUTS[0],f"C189-b{b}-h{h}-v{bit}")
                        before_reads=sum(providers[i,bit].reads for i in range(4))
                        observed,arrays,meter=run_block(views,endpoints[bit],bases[b],heads[b,h])
                        for k in live_meter: live_meter[k]+=meter[k]
                        live_post_rows+=sum(1 for r in observed if len(r["phases"])==2)
                        dense["necessity_predictions"][idx,bit]=arrays["necessity_predictions"]
                        dense["necessity_logits"][idx,bit]=arrays["necessity_logits"]
                        dense["target_predictions"][idx,bit]=arrays["target_predictions"]
                        dense["target_logits"][idx,bit]=arrays["target_logits"]

                        unknown=target.missing_mask(raw).numpy()
                        delta=float(np.max(np.abs(arrays["target_logits"][unknown]-saved["logits"][idx][unknown])))
                        scores=[]
                        for j,(rec,vm,tid) in enumerate(zip(observed,valid_full,tids,strict=True)):
                            score=assess(rec,vm,int(full_ix[j]),int(tid),metadata,bit,
                                         int(saved["predictions"][idx,j]))
                            scores.append(score);dense["post_labels"][idx,bit,j]=score["post_expected"]
                            trace.write(json.dumps(dict(base_seed=b,head_seed=h,completion=bit,
                                source_row=int(full_ix[j]),score=score,trace=rec),
                                sort_keys=True,separators=(",",":"),allow_nan=False)+"\n")
                        totals={k:sum(s[k] for s in scores) for k in COUNTERS}
                        actual_reads=sum(providers[i,bit].reads for i in range(4))-before_reads
                        require(actual_reads==totals["provider_calls"], "Provider read accounting discrepancy")
                        rec=dict(base_seed=b,head_seed=h,completion=bit,episodes=1768,
                            discriminating_rows=528,
                            discriminating_target_errors=sum(scores[j]["target_error"]
                                for j in np.flatnonzero(discriminating)),
                            initial_target_max_abs_logit_difference=delta,
                            post_sufficient=sum(s["post_expected"]==0 for s in scores),
                            post_needs=sum(s["post_expected"]==1 for s in scores),
                            by_group={str(g):{k:sum(scores[j][k] for j in np.flatnonzero(groups==g))
                                for k in COUNTERS} for g in sorted(set(groups.tolist()))},
                            **totals)
                        records.append(rec)
                        print(f"[C189] block={len(records)}/18 base={b} head={h} bit={bit} "
                              f"failed={rec['failed']} post_needs={rec['post_needs']} reads={actual_reads}",flush=True)
        record_file("episode-traces.jsonl.gz")
        np.savez_compressed(out/"episode-predictions.npz",**dense,
            row_indices=full_ix.astype("<i4"),
            base_seeds=np.repeat(np.asarray(BASE_SEEDS,dtype="<i4"),3),
            head_seeds=np.tile(np.asarray(HEAD_SEEDS,dtype="<i4"),3))
        record_file("episode-predictions.npz")
        save("episode-results.json",records)
        print("[C189] 2/3 all31824 live episodes collected; selected fact only; no second acquisition",flush=True)

        guard();precheck(parents["c188_summary"],*args)
        require([graph.fingerprint(bases[b]) for b in BASE_SEEDS]==[base_fp[b] for b in BASE_SEEDS],
                "Frozen C181 base changed")
        require([target.head_fingerprint(heads[b,h]) for b in BASE_SEEDS for h in HEAD_SEEDS] ==
                [head_fp[b,h] for b in BASE_SEEDS for h in HEAD_SEEDS],
                "Frozen C188 head changed")
        for f,hsh in protected.items(): require(audit.sha(f)==hsh,"Protected input changed:"+f)
        for a in artifacts: require(audit.sha(out/a["file"])==a["sha256"],"Output changed:"+a["file"])

        totals={k:sum(r[k] for r in records) for k in COUNTERS}
        reads=sum(p.reads for p in providers.values());readbytes=sum(p.bytes_read for p in providers.values())
        result=dict(
            experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status="PASS" if gate(records,replay) else "FAIL",
            diagnostic_execution_valid=True,C188_summary_sha256=PARENT_SHA,
            source_blobs=pins,input_sha256=protected,artifacts=artifacts,
            selector_replay=replay,records=records,totals=totals,episodes=31824,
            target_replay_rows=15912,live_initial_rows=31824,live_post_rows=live_post_rows,
            total_base_rows=5304+live_meter["rows"],total_target_rows=15912+31824,
            static_base_feature_rows=5304,static_base_feature_forward_calls=6,
            static_base_feature_cell_calls=42,
            live_inference_forward_calls=live_meter["forward_calls"],
            live_inference_cell_calls=live_meter["cell_calls"],
            base_checkpoint_loads=3,target_checkpoint_loads=9,
            actual_acquisitions=totals["provider_calls"],actual_file_reads=reads,
            provider_bytes_read=readbytes,taskview_fact_publications=totals["publications"],
            new_training=0,fresh_seeds=0,network_calls=0,answer_generation=0,
            proof_checker_calls=0,core_evidence_writes=0,
            production_runtime_modified=False,gate_e_candidate=False,
            environment=dict(torch=torch.__version__,numpy=np.__version__,device="cpu",dtype="float32",threads=2),
            wall_clock_seconds=time.perf_counter()-started,
            limitations=[
                "same four repeatedly inspected development groups;not independent final confirmation",
                "one acquisition maximum;post NEEDS never triggers a second target/action",
                "fixed RETRIEVE and local file provider;tool/provider choice remains handwritten",
                "identity/original C174 local layout only;C184/C185 renaming path not retested",
                "target and post logical teachers are scoring only;no answer/proof/language/larger expressions"])
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C189] 3/3 source/output preservation checked",flush=True)
        print("=== C189 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/"invalid.json").write_bytes(blob(dict(
            experiment_id=EXPERIMENT_ID,status="INVALID",diagnostic_execution_valid=False,
            error=str(exc),completed_records=records,completed_replay=replay)))
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in PRIOR_NAMES:
        p.add_argument("--"+n+"-summary",type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True)
    p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__=="__main__":
    main()
