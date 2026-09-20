"""C204: live frozen-model re-inference inside the accepted mixed-channel loop.

At every decision construct the current structured-v2 packet. Its exact canonical first72-feature
v1 prefix feeds the accepted frozen C181 INTERNAL_SEMANTICS necessity base and C188 target selector.
The12-bit v2 tail never enters learned inference and is used only for fact-specific channel routing.

Compare every live necessity/target prediction and logit against the accepted C199 ALLOWED artifact
for the same episode/phase, then execute live NEEDS targets through the accepted C203 mixed-channel
orchestration. No training, threshold repair, saved-decision substitution, or production runtime
change.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import hashlib
from pathlib import Path
import time

import numpy as np
import torch

from fold_lm.v05 import structured_action_channel as mapper
from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05 import structured_acquisition_lifecycle as life
from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as c185
from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
from fold_lm.v05_benchmarks import gate_e_c193_budget13_authoritative_closure as c193
from fold_lm.v05_benchmarks import gate_e_c201_selected_fact_channel_route as c201
from fold_lm.v05_benchmarks import gate_e_c202_three_channel_acquisition_dispatch as c202
from fold_lm.v05_benchmarks import gate_e_c203_mixed_channel_multistep_replay as c203

EXPERIMENT_ID = "C204-v5e-live-v2-mixed-channel-loop"
STAGE = "V5-E-LIVE-V2-MIXED-CHANNEL-LOOP"
BASE = "278b88208dbee17f96d1213ccff3d4ab385d1d0b"
PARENT_C203_EXECUTION = "293b440adfddcbda0a18fd66184768c27aff49a2"
PARENT_C203_SHA = "5fb52a6f056eea1fcf2ff719a9fa8c9efa9cc0d941ea26f50fdceed4c2db56c2"
REFERENCE_C199_EXECUTION = "48100f36f4f1acdf44d5cb1d508b907e19724c10"
REFERENCE_C199_SHA = "0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9"
C181_SUMMARY_SHA = "bfc68d603682aabd719bc52d33de907a60389a8e1f58ea22ebaf33fa21906f98"
C188_SUMMARY_SHA = "2a3ef27e9dec281159197775a15771b31b4945c9a0fa84787b4b812e9efb4153"
MANIFEST_SHA = "577f8a3e0b23e1833be89845a10445a85d8b337ebb1043d2df7dffae9913414a"
BASE_SEEDS = (181001,181002,181003)
HEAD_SEEDS = (188001,188002,188003)
ARM = "INTERNAL_SEMANTICS"
ATOL = 1e-6
BATCH = 1024
OWN = (
    "fold_lm/v05_benchmarks/gate_e_c204_live_v2_mixed_channel_loop.py",
    "tests_lm/test_v05_c204_live_v2_mixed_channel_loop.py",
    "tools/run_c204.ps1",
    "tools/invoke_c204.ps1",
    "docs/experiment-ledger-addendum-c204-preregistration.md",
    "docs/live-v2-mixed-channel-loop-v0.1.md",
)
OUTPUTS = {
    "live-v2-plan.json",
    "block-results.json",
    "prediction-replay.json",
    "provider-totals.json",
    "postconditions.json",
}
COUNTERS = (
    "failed","v2_prefix_error","necessity_prediction_error","target_prediction_error",
    "route_error","action_error","dispatch_error","provider_channel_error","receipt_error",
    "fact_update_error","authority_restore_error","resource_error","final_status_error",
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def manifest():
    return dict(
        experiment_id=EXPERIMENT_ID,
        stage=STAGE,
        acceptance_base=BASE,
        parent_c203_execution=PARENT_C203_EXECUTION,
        parent_c203_sha256=PARENT_C203_SHA,
        reference_c199_execution=REFERENCE_C199_EXECUTION,
        reference_c199_sha256=REFERENCE_C199_SHA,
        c181_summary_sha256=C181_SUMMARY_SHA,
        c188_summary_sha256=C188_SUMMARY_SHA,
        base_seeds=BASE_SEEDS,
        head_seeds=HEAD_SEEDS,
        channel_layout=c203.CHANNEL_LAYOUT,
        blocks=9,
        episodes_per_block=9536,
        decision_input="construct structured-v2 packet live; exact first72 canonical v1 features feed frozen learned models; 12-bit tail never enters learned forward",
        inference="accepted C181 INTERNAL_SEMANTICS base + accepted C188 selector; raw argmax; no threshold repair",
        reference="accepted C199 ALLOWED necessity/target predictions and logits at each active phase",
        action_path="live NEEDS target -> trusted three-channel authority window -> C201 mapper -> existing acquisition lifecycle -> restore parent authority",
        fixed_parent_totals=dict(
            episodes=85824,decisions=214948,acquisitions=129124,
            final_sufficient=85824,channel_switches=32564,
        ),
        atol=ATOL,
        training_steps=0,
        fresh_seeds=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        scope="live frozen-model re-inference over mixed-channel loop; not learned channel preference or final Gate E",
    )


def load_model_contracts(c181_summary: Path, c188_summary: Path):
    require(audit.sha(c181_summary) == C181_SUMMARY_SHA, "C181 summary changed")
    require(audit.sha(c188_summary) == C188_SUMMARY_SHA, "C188 summary changed")
    p181 = audit.read_json(c181_summary)
    p188 = audit.read_json(c188_summary)
    require(
        p181.get("experiment_id") == "C181-v5e-proper-subexpression-supervision"
        and p181.get("status") == "PASS"
        and p181.get("diagnostic_execution_valid") is True
        and p181.get("production_runtime_modified") is False,
        "Wrong accepted C181 model parent",
    )
    require(
        p188.get("experiment_id") == "C188-v5e-multimissing-target-selection"
        and p188.get("status") == "PASS"
        and p188.get("diagnostic_execution_valid") is True
        and p188.get("production_runtime_modified") is False,
        "Wrong accepted C188 selector parent",
    )
    fits = {f["seed"]:f for f in p181["fit_records"] if f["arm"] == ARM}
    selector_sha = {
        (r["base_seed"],r["head_seed"]):r["head_sha256"]
        for r in p188["selector_results"]
    }
    require(set(fits) == set(BASE_SEEDS), "C181 accepted base set drift")
    require(set(selector_sha) == {(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS},
            "C188 accepted selector set drift")

    protected = {
        str(c181_summary.resolve()):C181_SUMMARY_SHA,
        str(c188_summary.resolve()):C188_SUMMARY_SHA,
    }
    base_paths = {}
    selector_paths = {}
    c181_values = set(p181.get("input_sha256",{}).values())
    c188_values = set(p188.get("input_sha256",{}).values())

    for seed in BASE_SEEDS:
        name = f"probe-{seed}-{ARM}.pt"
        artifact = next((a for a in p181["artifacts"] if a["file"] == name), None)
        require(artifact is not None, "C181 base checkpoint missing:"+name)
        path = audit.safe_child(c181_summary.resolve().parent,name)
        require(
            path.is_file() and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C181 base checkpoint:"+name,
        )
        base_paths[seed] = path
        protected[str(path.resolve())] = artifact["sha256"]

    for b in BASE_SEEDS:
        for h in HEAD_SEEDS:
            name = f"selector-{b}-{h}.pt"
            artifact = next((a for a in p188["artifacts"] if a["file"] == name), None)
            require(artifact is not None, "C188 selector checkpoint missing:"+name)
            path = audit.safe_child(c188_summary.resolve().parent,name)
            require(
                path.is_file() and path.stat().st_size == artifact["serialized_bytes"]
                and audit.sha(path) == artifact["sha256"],
                "Changed C188 selector checkpoint:"+name,
            )
            selector_paths[b,h] = path
            protected[str(path.resolve())] = artifact["sha256"]

    return p181,p188,fits,selector_sha,base_paths,selector_paths,protected


def restore_models(c181_summary: Path, c188_summary: Path):
    p181,p188,fits,selector_sha,base_paths,selector_paths,_ = load_model_contracts(
        c181_summary,c188_summary
    )
    bases = {}
    selectors = {}
    for b in BASE_SEEDS:
        bases[b] = frozen.restore_bare(base_paths[b],b,ARM,fits[b]["final_sha256"])
        for h in HEAD_SEEDS:
            selectors[b,h] = c189.restore_selector(
                selector_paths[b,h],b,h,selector_sha[b,h]
            )
    return bases,selectors


def encode_live_v2(owners, ids):
    packets = []
    rows = []
    errors = 0
    for i in ids:
        base = owners[i].state.view
        typed = c203.mixed_view(base)
        packet = v2.encode(typed)
        parent = v1.encode(base)
        if (
            tuple(packet.features[:v1.FEATURE_WIDTH]) != parent.features
            or packet.binding != parent.binding
            or v2.decode(packet) != typed
        ):
            errors += 1
        packets.append(packet)
        rows.append(packet.features[:v1.FEATURE_WIDTH])
    raw = torch.tensor(rows,dtype=torch.int32)
    require(raw.shape == (len(ids),72), "Live v2 prefix shape drift")
    return raw,packets,errors


def replay_metrics(arrays, reference):
    npred = arrays["necessity_predictions"]
    nlog = arrays["necessity_logits"]
    tpred = arrays["target_predictions"]
    tlog = arrays["target_logits"]
    rn = reference["necessity_predictions"]
    rnlog = reference["necessity_logits"]
    rt = reference["target_predictions"]
    rtlog = reference["target_logits"]
    require(
        npred.shape == rn.shape == (9536,4)
        and nlog.shape == rnlog.shape == (9536,4,2)
        and tpred.shape == rt.shape == (9536,3)
        and tlog.shape == rtlog.shape == (9536,3,4),
        "Reference/live replay shape drift",
    )
    nerr = int((npred != rn).sum())
    terr = int((tpred != rt).sum())
    ndelta = float(np.max(np.abs(nlog.astype(np.float64)-rnlog.astype(np.float64))))
    finite = np.isfinite(rtlog)
    require(np.array_equal(np.isfinite(tlog),finite), "Target logit finite-mask drift")
    tdelta = float(np.max(np.abs(
        tlog[finite].astype(np.float64)-rtlog[finite].astype(np.float64)
    ))) if finite.any() else 0.0
    return dict(
        necessity_prediction_errors=nerr,
        target_prediction_errors=terr,
        necessity_max_abs_logit_difference=ndelta,
        target_max_abs_logit_difference=tdelta,
    )


def run_live_block(views, world_codes, base_model, selector, reference,
                   provider_map, endpoint_map, expected):
    require(len(views) == len(world_codes) == 9536, "Block alignment required")
    owners = [
        life.AcquisitionOwner(action.RuntimeState(view),endpoint_map[int(code)],max_dispatches=3)
        for view,code in zip(views,world_codes,strict=True)
    ]
    n = len(views)
    n_pred = np.full((n,4),-1,dtype=np.int8)
    n_logits = np.zeros((n,4,2),dtype=np.float32)
    t_pred = np.full((n,3),-1,dtype=np.int8)
    t_logits = np.full((n,3,4),-np.inf,dtype=np.float32)
    decisions = np.zeros(n,dtype=np.int8)
    acquisitions = np.zeros(n,dtype=np.int8)
    sequences = [[] for _ in range(n)]
    counters = {k:0 for k in COUNTERS}
    meter = dict(rows=0,forward_calls=0,cell_calls=0)
    prefix_packets = 0
    provider_before = {
        channel:sum(provider_map[c][channel].calls for c in range(16))
        for channel in v2.CHANNELS
    }
    active = list(range(n))

    for phase in range(4):
        charged = []
        for i in active:
            r = owners[i].state.view.resources
            if not (r.available == c203.PARENT_AVAILABLE and r.permitted == c203.PARENT_PERMITTED):
                counters["authority_restore_error"] += 1
                counters["failed"] += 1
                continue
            if not c185.charge_decision(owners[i]):
                counters["final_status_error"] += 1
                counters["failed"] += 1
                continue
            charged.append(i)
        active = charged
        if not active:
            break

        raw,_,prefix_errors = encode_live_v2(owners,active)
        counters["v2_prefix_error"] += prefix_errors
        counters["failed"] += prefix_errors
        prefix_packets += len(active)

        any_missing = any(
            any(f.status == "UNOBSERVED" for f in owners[i].state.view.facts)
            for i in active
        )
        if any_missing:
            require(phase < 3, "Target-bearing phase exceeded acquisition bound")
            p,t,z,tz,m = c189.combined_predict(base_model,selector,raw,batch=BATCH)
        else:
            p,z,m = c189.necessity_predict(base_model,raw,batch=BATCH)
            t = np.full(len(active),-1,dtype=np.int8)
            tz = np.full((len(active),4),-np.inf,dtype=np.float32)
        for key in meter:
            meter[key] += int(m[key])

        next_active = []
        for j,i in enumerate(active):
            decisions[i] += 1
            n_pred[i,phase] = int(p[j])
            n_logits[i,phase] = z[j]
            if int(p[j]) != int(reference["necessity_predictions"][i,phase]):
                counters["necessity_prediction_error"] += 1
                counters["failed"] += 1
            if phase < 3 and any_missing:
                t_pred[i,phase] = int(t[j])
                t_logits[i,phase] = tz[j]
                if int(t[j]) != int(reference["target_predictions"][i,phase]):
                    counters["target_prediction_error"] += 1
                    counters["failed"] += 1

            if int(p[j]) == 0:
                continue
            if phase >= 3 or not any_missing:
                counters["target_prediction_error"] += 1
                counters["failed"] += 1
                continue
            target = int(t[j])
            if not 0 <= target < 4 or owners[i].state.view.facts[target].status != "UNOBSERVED":
                counters["target_prediction_error"] += 1
                counters["failed"] += 1
                continue

            owner = owners[i]
            before_facts = owner.state.view.facts
            c203.set_authority(owner,all_channels=True)
            typed = c203.mixed_view(owner.state.view)
            proposal = mapper.propose_selected(typed,owner.state,target)
            channel = c203.CHANNEL_LAYOUT[target]
            before_calls = tuple(provider_map[int(world_codes[i])][name].calls for name in v2.CHANNELS)
            transition = owner.apply(proposal)
            dispatch = (
                owner.dispatch(transition.result.intent.intent_id)
                if transition.result.status == "PENDING" else None
            )
            after_calls = tuple(provider_map[int(world_codes[i])][name].calls for name in v2.CHANNELS)

            route_error = int(not (proposal.action == channel and proposal.fact_index == target))
            action_error = int(not (
                transition.result.status == "PENDING"
                and transition.result.reason == "ACQUISITION_RESERVED"
                and transition.result.acquisition_reserved == 1
                and transition.result.internal_charged == 1
            ))
            dispatch_error = int(not (
                dispatch is not None
                and dispatch.status == "PUBLISHED"
                and dispatch.reason == "OBSERVATION_ADMITTED"
                and dispatch.provider_calls == 1
                and dispatch.fact_publications == 1
            ))
            ci = v2.CHANNELS.index(channel)
            provider_error = int(not (
                after_calls[ci]-before_calls[ci] == 1
                and sum(after_calls[k]-before_calls[k] for k in range(3) if k != ci) == 0
            ))
            expected_value = int(c190.WORLD_BITS[int(world_codes[i])][target])
            receipt = owner.receipts[-1] if owner.receipts else None
            receipt_error = int(not (
                receipt is not None and receipt.action == channel
                and receipt.fact_id == c185.FACT_IDS[target]
                and receipt.value == expected_value
            ))
            after_facts = owner.state.view.facts
            fact_error = int(not (
                after_facts[target].status == "OBSERVED"
                and after_facts[target].value == expected_value
                and all(after_facts[k] == before_facts[k] for k in range(4) if k != target)
            ))
            for key,value in (
                ("route_error",route_error),("action_error",action_error),
                ("dispatch_error",dispatch_error),("provider_channel_error",provider_error),
                ("receipt_error",receipt_error),("fact_update_error",fact_error),
            ):
                counters[key] += value
            local_failed = any((route_error,action_error,dispatch_error,provider_error,receipt_error,fact_error))
            if local_failed:
                counters["failed"] += 1
                continue

            acquisitions[i] += 1
            sequences[i].append(channel)
            c203.set_authority(owner,all_channels=False)
            rr = owner.state.view.resources
            if not (rr.available == c203.PARENT_AVAILABLE and rr.permitted == c203.PARENT_PERMITTED):
                counters["authority_restore_error"] += 1
                counters["failed"] += 1
                continue
            next_active.append(i)
        active = next_active

    if active:
        counters["final_status_error"] += len(active)
        counters["failed"] += len(active)

    final_sufficient = 0
    switches = 0
    for i,owner in enumerate(owners):
        d = int(decisions[i]); a = int(acquisitions[i])
        expected_d = int((reference["necessity_predictions"][i] >= 0).sum())
        expected_a = sum(int(x) == 1 for x in reference["necessity_predictions"][i] if int(x) >= 0)
        if (d,a) != (expected_d,expected_a):
            counters["final_status_error"] += 1
            counters["failed"] += 1
        last = [int(x) for x in n_pred[i] if int(x) >= 0]
        if last and last[-1] == 0 and d == expected_d:
            final_sufficient += 1
        else:
            counters["final_status_error"] += 1
            counters["failed"] += 1
        r = owner.state.view.resources
        if not (
            r.internal_remaining == 13-d-3*a
            and r.acquisitions_remaining == 4-a
            and r.internal_step == 7+d+3*a
            and r.available == c203.PARENT_AVAILABLE
            and r.permitted == c203.PARENT_PERMITTED
            and r.last_outcome == "NONE"
            and owner.state.pending is None
            and owner.state.terminal is None
            and len(owner.receipts) == a
        ):
            counters["resource_error"] += 1
            counters["failed"] += 1
        switches += sum(x != y for x,y in zip(sequences[i],sequences[i][1:]))

    arrays = dict(
        necessity_predictions=n_pred,necessity_logits=n_logits,
        target_predictions=t_pred,target_logits=t_logits,
    )
    replay = replay_metrics(arrays,reference)
    counters["necessity_prediction_error"] = replay["necessity_prediction_errors"]
    counters["target_prediction_error"] = replay["target_prediction_errors"]
    if replay["necessity_prediction_errors"] or replay["target_prediction_errors"]:
        counters["failed"] += replay["necessity_prediction_errors"] + replay["target_prediction_errors"]

    provider_after = {
        channel:sum(provider_map[c][channel].calls for c in range(16))
        for channel in v2.CHANNELS
    }
    channel_counts = {
        channel:provider_after[channel]-provider_before[channel]
        for channel in v2.CHANNELS
    }
    record = dict(
        episodes=9536,
        decisions=int(decisions.sum()),
        acquisitions=int(acquisitions.sum()),
        final_sufficient=final_sufficient,
        channel_counts=channel_counts,
        channel_switches=switches,
        v2_packets=prefix_packets,
        inference_rows=meter["rows"],
        inference_forward_calls=meter["forward_calls"],
        inference_cell_calls=meter["cell_calls"],
        necessity_max_abs_logit_difference=replay["necessity_max_abs_logit_difference"],
        target_max_abs_logit_difference=replay["target_max_abs_logit_difference"],
        **counters,
    )
    projection_error = int(not (
        record["decisions"] == expected["decisions"]
        and record["acquisitions"] == expected["acquisitions"]
        and record["final_sufficient"] == expected["final_sufficient"]
        and record["channel_counts"] == expected["channel_counts"]
        and record["channel_switches"] == expected["channel_switches"]
    ))
    record["projection_error"] = projection_error
    if projection_error:
        record["failed"] += 1
    return record,replay


def collect(features,predictions,bases,selectors,c203_result):
    row_indices = predictions["row_indices"].astype(np.int64)
    world_codes = predictions["world_codes"].astype(np.int64)
    require(row_indices.shape == world_codes.shape == (9536,), "Episode identity shape drift")
    raw12 = torch.from_numpy(features[row_indices].copy())
    raw13 = c193.budget13(raw12)
    provider_map,endpoint_map = c202.providers()
    reference_projection = c203_result["expected_projection"]
    records = []
    replay_rows = []
    for bi,b in enumerate(BASE_SEEDS):
        for hi,h in enumerate(HEAD_SEEDS):
            idx = bi*3+hi
            views = c190.make_views(raw13,row_indices,world_codes,f"C204-live-b{b}-h{h}")
            reference = dict(
                necessity_predictions=predictions["necessity_predictions"][0,idx],
                necessity_logits=predictions["necessity_logits"][0,idx],
                target_predictions=predictions["target_predictions"][0,idx],
                target_logits=predictions["target_logits"][0,idx],
            )
            rec,replay = run_live_block(
                views,world_codes,bases[b],selectors[b,h],reference,
                provider_map,endpoint_map,reference_projection["blocks"][idx],
            )
            rec.update(block=idx,base_seed=b,head_seed=h)
            records.append(rec)
            replay_rows.append(dict(block=idx,base_seed=b,head_seed=h,**replay))
            print(
                f"[C204] block={idx+1}/9 base={b} head={h} "
                f"decisions={rec['decisions']} acquisitions={rec['acquisitions']} "
                f"failed={rec['failed']}",
                flush=True,
            )
    totals = dict(
        episodes=sum(r["episodes"] for r in records),
        decisions=sum(r["decisions"] for r in records),
        acquisitions=sum(r["acquisitions"] for r in records),
        final_sufficient=sum(r["final_sufficient"] for r in records),
        channel_counts={
            channel:sum(r["channel_counts"][channel] for r in records)
            for channel in v2.CHANNELS
        },
        channel_switches=sum(r["channel_switches"] for r in records),
        v2_packets=sum(r["v2_packets"] for r in records),
        inference_rows=sum(r["inference_rows"] for r in records),
        inference_forward_calls=sum(r["inference_forward_calls"] for r in records),
        inference_cell_calls=sum(r["inference_cell_calls"] for r in records),
        failures=sum(r["failed"] for r in records),
        projection_errors=sum(r["projection_error"] for r in records),
        v2_prefix_errors=sum(r["v2_prefix_error"] for r in records),
        necessity_prediction_errors=sum(r["necessity_prediction_error"] for r in records),
        target_prediction_errors=sum(r["target_prediction_error"] for r in records),
        max_necessity_logit_delta=max(r["necessity_max_abs_logit_difference"] for r in records),
        max_target_logit_delta=max(r["target_max_abs_logit_difference"] for r in records),
    )
    return records,replay_rows,totals


def gate(records,totals):
    return (
        len(records) == 9
        and [(r["base_seed"],r["head_seed"]) for r in records]
            == [(b,h) for b in BASE_SEEDS for h in HEAD_SEEDS]
        and totals.get("episodes") == 85824
        and totals.get("decisions") == 214948
        and totals.get("acquisitions") == 129124
        and totals.get("final_sufficient") == 85824
        and totals.get("channel_counts")
            == {"RETRIEVE":88918,"OBSERVE":21252,"ASK_USER":18954}
        and totals.get("channel_switches") == 32564
        and totals.get("v2_packets") == 214948
        and totals.get("failures") == 0
        and totals.get("projection_errors") == 0
        and totals.get("v2_prefix_errors") == 0
        and totals.get("necessity_prediction_errors") == 0
        and totals.get("target_prediction_errors") == 0
        and totals.get("max_necessity_logit_delta",1.0) <= ATOL
        and totals.get("max_target_logit_delta",1.0) <= ATOL
        and totals.get("inference_rows",0) > 0
        and totals.get("inference_forward_calls",0) > 0
        and all(
            r.get("failed") == 0 and r.get("projection_error") == 0
            and r.get("v2_prefix_error") == 0
            and r.get("necessity_prediction_error") == 0
            and r.get("target_prediction_error") == 0
            and r.get("necessity_max_abs_logit_difference",1.0) <= ATOL
            and r.get("target_max_abs_logit_difference",1.0) <= ATOL
            for r in records
        )
    )


def precheck(c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,
             c181_summary,c188_summary,root):
    root = Path(root)
    c202_result,c199,prediction_path,c174_result,pilot_path,pins,protected = c203.precheck(
        c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,root
    )
    require(audit.sha(c203_summary) == PARENT_C203_SHA, "C203 summary changed")
    p203 = audit.read_json(c203_summary)
    c203.validate_result(p203)
    require(
        p203.get("commit_sha") == PARENT_C203_EXECUTION
        and p203.get("status") == "PASS"
        and c203.gate(p203["expected_projection"],p203["block_records"],p203["summary"])
        and p203.get("source_blobs") == pins,
        "Wrong accepted C203 parent",
    )
    protected[str(Path(c203_summary).resolve())] = PARENT_C203_SHA
    for artifact in p203["artifacts"]:
        path = audit.safe_child(Path(c203_summary).resolve().parent,artifact["file"])
        require(
            path.is_file() and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C203 artifact:"+artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]

    p181,p188,_,_,_,_,model_protected = load_model_contracts(
        Path(c181_summary),Path(c188_summary)
    )
    protected.update(model_protected)

    # Tie all frozen checkpoints to artifacts already protected by accepted C199.
    accepted_values = set(c199.get("input_sha256",{}).values())
    for path,wanted in model_protected.items():
        if path in (str(Path(c181_summary).resolve()),str(Path(c188_summary).resolve())):
            require(wanted in accepted_values, "Model summary not tied to accepted C199")
        else:
            require(wanted in accepted_values, "Model checkpoint not tied to accepted C199")

    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    pins.update({name:allpins[name] for name in OWN})
    require(len(pins) == 37 and len(protected) == 79, "C204 source/protection count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C204 manifest drift")
    return p203,c199,prediction_path,c174_result,pilot_path,p181,p188,pins,protected


def regression_modules(root):
    names = c203.regression_modules(root)
    require(len(names) == len(set(names)) == 88, "Historical regression list drift")
    return names + ["tests_lm.test_v05_c204_live_v2_mixed_channel_loop"]


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C204",
    )
    require(
        len(payload["source_blobs"]) == 37
        and len(payload["input_sha256"]) == 79
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C204 coverage drift",
    )
    require(
        payload["training_steps"] == 0
        and payload["fresh_seed_count"] == 0
        and payload["network_calls"] == 0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False,
        "C204 scope drift",
    )
    require(payload["status"] == ("PASS" if gate(payload["block_records"],payload["summary"]) else "FAIL"),
            "C204 gate drift")


def run(*,c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,
        c181_summary,c188_summary,output_dir,expected_head):
    root = Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip() == expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()
                == "feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    p203,_,prediction_path,_,_,_,_,pins,protected = precheck(
        c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,
        c181_summary,c188_summary,root
    )
    predictions = c201.load_c199_predictions(prediction_path)
    _,_,features = c203.load_c174_features(Path(c174_summary))
    bases,selectors = restore_models(Path(c181_summary),Path(c188_summary))

    out = Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    artifacts = []
    started = time.perf_counter()

    def record(name):
        path = out/name
        artifacts.append(dict(file=name,sha256=audit.sha(path),serialized_bytes=path.stat().st_size))

    def save(name,value):
        (out/name).write_bytes(blob(value));record(name)

    save("live-v2-plan.json",dict(manifest(),source_blobs=pins))
    try:
        records,replay_rows,summary = collect(features,predictions,bases,selectors,p203)
        save("block-results.json",records)
        save("prediction-replay.json",replay_rows)
        save("provider-totals.json",summary["channel_counts"])
        save("postconditions.json",dict(
            v2_input="84 features constructed every learned decision",
            learned_input="exact v2 first72 canonical v1 features only",
            routing_input="fixed12-bit v2 tail only",
            parent_authority=list(c203.PARENT_AVAILABLE),
            fixed_channel_layout=list(c203.CHANNEL_LAYOUT),
            parent_totals=dict(decisions=214948,acquisitions=129124,final_sufficient=85824,
                               channel_switches=32564),
        ))

        guard()
        precheck(c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,
                 c181_summary,c188_summary,root)
        for path,wanted in protected.items():
            require(audit.sha(path) == wanted,"Protected input changed:"+path)
        for artifact in artifacts:
            require(audit.sha(out/artifact["file"]) == artifact["sha256"],
                    "Output changed:"+artifact["file"])

        result = dict(
            experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
            status="PASS" if gate(records,summary) else "FAIL",
            diagnostic_execution_valid=True,
            C203_summary_sha256=PARENT_C203_SHA,
            C199_reference_summary_sha256=REFERENCE_C199_SHA,
            C181_summary_sha256=C181_SUMMARY_SHA,
            C188_summary_sha256=C188_SUMMARY_SHA,
            source_blobs=pins,input_sha256=protected,artifacts=artifacts,
            block_records=records,prediction_replay=replay_rows,summary=summary,
            training_steps=0,fresh_seed_count=0,network_calls=0,
            production_runtime_modified=False,gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=[
                "frozen accepted C181/C188 models only; no retraining",
                "v2 channel tail intentionally excluded from learned forward",
                "fixed exactly-one channel layout per fact",
                "fixture providers, not real sensor/user transport",
                "not learned channel preference or final Gate E",
            ],
        )
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C204] live-v2 mixed-channel loop collected",flush=True)
        print("=== C204 RESULT ===",flush=True)
        print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/"invalid.json").write_bytes(blob(dict(
            experiment_id=EXPERIMENT_ID,status="INVALID",
            diagnostic_execution_valid=False,error=str(exc),
        )))
        raise


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in (
        "c203-summary","c202-summary","c201-summary","c200-summary","c199-summary",
        "c174-summary","c181-summary","c188-summary","output-dir",
    ):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
