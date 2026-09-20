"""C203: replay accepted multi-step learned decisions through mixed fact-specific channels.

No training and no learned forward calls. Reconstruct the accepted C199 coherent-world episodes
from protected C174 pilot features and replay the immutable accepted C199 ALLOWED necessity/target
trace. Each fact has a fixed semantic acquisition channel:
fact0 RETRIEVE, fact1 OBSERVE, fact2 ASK_USER, fact3 RETRIEVE.

Before every replayed learned decision, the v1 runtime authority masks are the accepted parent
RETRIEVE-only masks. After NEEDS+target, a trusted scheduler temporarily enables all three channels,
the selected fact is wrapped in structured-v2 metadata and routed by the accepted C201 mapper through
the existing acquisition lifecycle. Parent masks are restored before the next replayed decision.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, replace
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
from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as c185
from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
from fold_lm.v05_benchmarks import gate_e_c193_budget13_authoritative_closure as c193
from fold_lm.v05_benchmarks import gate_e_c201_selected_fact_channel_route as c201
from fold_lm.v05_benchmarks import gate_e_c202_three_channel_acquisition_dispatch as c202

EXPERIMENT_ID = "C203-v5e-mixed-channel-multistep-replay"
STAGE = "V5-E-MIXED-CHANNEL-MULTISTEP-REPLAY"
BASE = "e44a5e93ed0048e282e4c2389c0ca68c6c69adda"
PARENT_C202_EXECUTION = "a140f33b02aa4056b7c1fcff9041b09f9b7342c4"
PARENT_C202_SHA = "b568d8b652802c16fb75b85416c6d4ed956abcf767164d688ee39be1178e8c82"
TARGET_C199_EXECUTION = "48100f36f4f1acdf44d5cb1d508b907e19724c10"
TARGET_C199_SHA = "0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9"
C174_SHA = "3e69b7d8cff9e1cfdab7d06c58d45f83d1f596ac793c85c4c34ff620f8637d36"
MANIFEST_SHA = "2b9723733441019df8d73fa40fcf1421023c4765cbe6fdc91a31b2765b447ae6"
CHANNEL_LAYOUT = ("RETRIEVE", "OBSERVE", "ASK_USER", "RETRIEVE")
PARENT_AVAILABLE = (True, False, False)
PARENT_PERMITTED = (True, False, False)
ALL_TRUE = (True, True, True)
BLOCKS = 9
EPISODES = 9536
OWN = (
    "fold_lm/v05_benchmarks/gate_e_c203_mixed_channel_multistep_replay.py",
    "tests_lm/test_v05_c203_mixed_channel_multistep_replay.py",
    "tools/run_c203.ps1",
    "tools/invoke_c203.ps1",
    "docs/experiment-ledger-addendum-c203-preregistration.md",
    "docs/mixed-channel-multistep-replay-v0.1.md",
)
OUTPUTS = {
    "mixed-loop-plan.json",
    "expected-projection.json",
    "block-results.json",
    "provider-totals.json",
    "postconditions.json",
}
COUNTERS = (
    "failed", "decision_trace_error", "target_error", "route_error", "action_error",
    "dispatch_error", "provider_channel_error", "receipt_error", "fact_update_error",
    "authority_restore_error", "resource_error", "final_status_error",
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
        parent_c202_execution=PARENT_C202_EXECUTION,
        parent_c202_sha256=PARENT_C202_SHA,
        target_source_c199_execution=TARGET_C199_EXECUTION,
        target_source_c199_sha256=TARGET_C199_SHA,
        c174_summary_sha256=C174_SHA,
        channel_layout=list(CHANNEL_LAYOUT),
        blocks=BLOCKS,
        episodes_per_block=EPISODES,
        decision_source="accepted C199 ALLOWED saved necessity/target predictions; no new learned forward",
        model_visible_authority="before every replayed decision restore accepted RETRIEVE-only available/permitted masks",
        action_authority="after NEEDS+target trusted scheduler temporarily enables all three channels, dispatches selected fact through fixed one-hot channel, then restores parent masks",
        expected_decisions_total=214948,
        expected_acquisitions_total=129124,
        expected_final_sufficient=85824,
        expected_channel_counts="deterministic projection of accepted target indices through fixed channel_layout",
        expected_switches="deterministic within-episode transitions between consecutive projected acquisition channels",
        training_steps=0,
        fresh_seed_count=0,
        learned_forward_calls=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        scope="mixed-channel multi-step orchestration replay; not learned channel preference or final Gate E",
    )


def load_c174_features(c174_summary: Path):
    require(audit.sha(c174_summary) == C174_SHA, "C174 summary changed")
    summary = audit.read_json(c174_summary)
    require(
        summary.get("experiment_id") == "C174-v5e-learned-necessity-syntax-ablation"
        and summary.get("status") == "PASS"
        and summary.get("diagnostic_execution_valid") is True,
        "Wrong accepted C174 data parent",
    )
    artifact = next((a for a in summary["artifacts"] if a["file"] == "pilot-data.npz"), None)
    require(artifact is not None, "C174 pilot-data artifact missing")
    path = audit.safe_child(c174_summary.resolve().parent, artifact["file"])
    require(
        path.is_file()
        and path.stat().st_size == artifact["serialized_bytes"]
        and audit.sha(path) == artifact["sha256"],
        "Changed C174 pilot-data artifact",
    )
    with np.load(path, allow_pickle=False) as z:
        require(
            set(z.files) == {"features","labels","template_ids","split_codes","groups"},
            "C174 pilot-data schema drift",
        )
        features = z["features"].copy()
    require(features.shape == (51840,72) and features.dtype == np.dtype("<i4"),
            "C174 feature array drift")
    return summary, path, features


def mixed_view(base: v1.TaskView) -> v2.TaskView:
    specs = []
    for channel in CHANNEL_LAYOUT:
        bits = tuple(name == channel for name in v2.CHANNELS)
        specs.append(v2.FactChannels(bits))
    return v2.TaskView(base, tuple(specs))


def set_authority(owner: life.AcquisitionOwner, *, all_channels: bool):
    view = owner.state.view
    r = view.resources
    available = ALL_TRUE if all_channels else PARENT_AVAILABLE
    permitted = ALL_TRUE if all_channels else PARENT_PERMITTED
    owner.refresh(replace(
        view,
        resources=replace(r, available=available, permitted=permitted),
    ))


def expected_projection(predictions):
    n = predictions["necessity_predictions"][0]
    t = predictions["target_predictions"][0]
    require(n.shape == (9,9536,4) and t.shape == (9,9536,3),
            "C199 replay shape drift")
    blocks = []
    totals = {name:0 for name in v2.CHANNELS}
    all_switches = 0
    all_acquisitions = 0
    all_decisions = 0
    for block in range(9):
        channel_counts = {name:0 for name in v2.CHANNELS}
        acquisitions = decisions = switches = final_sufficient = 0
        for row in range(9536):
            decisions_row = [int(x) for x in n[block,row] if int(x) >= 0]
            targets_row = [int(x) for x in t[block,row] if int(x) >= 0]
            require(decisions_row and decisions_row[-1] == 0,
                    "Accepted trace must terminate SUFFICIENT")
            require(all(x == 1 for x in decisions_row[:-1]),
                    "Accepted trace has nonterminal non-NEEDS decision")
            require(len(targets_row) == len(decisions_row)-1,
                    "Accepted target/decision depth mismatch")
            require(all(0 <= x < 4 for x in targets_row), "Accepted target out of range")
            channels = [CHANNEL_LAYOUT[x] for x in targets_row]
            for channel in channels:
                channel_counts[channel] += 1
            switches += sum(a != b for a,b in zip(channels,channels[1:]))
            acquisitions += len(targets_row)
            decisions += len(decisions_row)
            final_sufficient += 1
        for channel in v2.CHANNELS:
            totals[channel] += channel_counts[channel]
        all_switches += switches
        all_acquisitions += acquisitions
        all_decisions += decisions
        blocks.append(dict(
            block=block,
            episodes=9536,
            decisions=decisions,
            acquisitions=acquisitions,
            final_sufficient=final_sufficient,
            channel_counts=channel_counts,
            channel_switches=switches,
        ))
    return dict(
        blocks=blocks,
        totals=dict(
            episodes=85824,
            decisions=all_decisions,
            acquisitions=all_acquisitions,
            final_sufficient=85824,
            channel_counts=totals,
            channel_switches=all_switches,
        ),
    )


def replay_block(views, world_codes, necessity, targets, provider_map, endpoint_map, expected):
    require(len(views) == len(world_codes) == 9536, "Block alignment required")
    owners = [
        life.AcquisitionOwner(
            action.RuntimeState(view),
            endpoint_map[int(code)],
            max_dispatches=3,
        )
        for view,code in zip(views,world_codes,strict=True)
    ]
    episode_decisions = np.zeros(len(views), dtype=np.int8)
    episode_acquisitions = np.zeros(len(views), dtype=np.int8)
    channel_sequences = [[] for _ in views]
    counters = {k:0 for k in COUNTERS}
    provider_before = {
        channel: sum(provider_map[c][channel].calls for c in range(16))
        for channel in v2.CHANNELS
    }
    active = list(range(len(views)))

    for phase in range(4):
        next_active = []
        for i in active:
            owner = owners[i]
            r0 = owner.state.view.resources
            if not (r0.available == PARENT_AVAILABLE and r0.permitted == PARENT_PERMITTED):
                counters["authority_restore_error"] += 1
            if not c185.charge_decision(owner):
                counters["decision_trace_error"] += 1
                counters["failed"] += 1
                continue
            episode_decisions[i] += 1
            pred = int(necessity[i,phase])
            if pred not in (0,1):
                counters["decision_trace_error"] += 1
                counters["failed"] += 1
                continue
            if pred == 0:
                continue
            if phase >= 3:
                counters["decision_trace_error"] += 1
                counters["failed"] += 1
                continue
            target = int(targets[i,phase])
            if not 0 <= target < 4 or owner.state.view.facts[target].status != "UNOBSERVED":
                counters["target_error"] += 1
                counters["failed"] += 1
                continue

            before_facts = owner.state.view.facts
            set_authority(owner, all_channels=True)
            typed = mixed_view(owner.state.view)
            proposal = mapper.propose_selected(typed, owner.state, target)
            channel = CHANNEL_LAYOUT[target]
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
            channel_index = v2.CHANNELS.index(channel)
            provider_channel_error = int(not (
                after_calls[channel_index]-before_calls[channel_index] == 1
                and sum(after_calls[j]-before_calls[j] for j in range(3) if j != channel_index) == 0
            ))
            expected_value = int(c190.WORLD_BITS[int(world_codes[i])][target])
            receipt = owner.receipts[-1] if owner.receipts else None
            receipt_error = int(not (
                receipt is not None
                and receipt.action == channel
                and receipt.fact_id == c185.FACT_IDS[target]
                and receipt.value == expected_value
            ))
            after_facts = owner.state.view.facts
            fact_update_error = int(not (
                after_facts[target].status == "OBSERVED"
                and after_facts[target].value == expected_value
                and all(after_facts[j] == before_facts[j] for j in range(4) if j != target)
            ))
            for key,value in (
                ("route_error",route_error),("action_error",action_error),
                ("dispatch_error",dispatch_error),("provider_channel_error",provider_channel_error),
                ("receipt_error",receipt_error),("fact_update_error",fact_update_error),
            ):
                counters[key] += value
            local_failed = any((route_error,action_error,dispatch_error,provider_channel_error,
                                receipt_error,fact_update_error))
            if local_failed:
                counters["failed"] += 1
                continue

            episode_acquisitions[i] += 1
            channel_sequences[i].append(channel)
            set_authority(owner, all_channels=False)
            rr = owner.state.view.resources
            if not (rr.available == PARENT_AVAILABLE and rr.permitted == PARENT_PERMITTED):
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
        decisions = int(episode_decisions[i])
        acquisitions = int(episode_acquisitions[i])
        ref_decisions = int((necessity[i] >= 0).sum())
        ref_acquisitions = int((targets[i] >= 0).sum())
        if (decisions,acquisitions) != (ref_decisions,ref_acquisitions):
            counters["decision_trace_error"] += 1
            counters["failed"] += 1
        last = [int(x) for x in necessity[i] if int(x) >= 0]
        if last and last[-1] == 0 and decisions == ref_decisions:
            final_sufficient += 1
        else:
            counters["final_status_error"] += 1
            counters["failed"] += 1
        r = owner.state.view.resources
        expected_internal = 13 - decisions - 3*acquisitions
        expected_acq = 4 - acquisitions
        expected_step = 7 + decisions + 3*acquisitions
        if not (
            r.internal_remaining == expected_internal
            and r.acquisitions_remaining == expected_acq
            and r.available == PARENT_AVAILABLE
            and r.permitted == PARENT_PERMITTED
            and r.last_outcome == "NONE"
            and r.internal_step == expected_step
            and owner.state.pending is None
            and owner.state.terminal is None
            and len(owner.receipts) == acquisitions
        ):
            counters["resource_error"] += 1
            counters["failed"] += 1
        switches += sum(a != b for a,b in zip(channel_sequences[i],channel_sequences[i][1:]))

    provider_after = {
        channel: sum(provider_map[c][channel].calls for c in range(16))
        for channel in v2.CHANNELS
    }
    channel_counts = {
        channel: provider_after[channel]-provider_before[channel]
        for channel in v2.CHANNELS
    }
    record = dict(
        episodes=9536,
        decisions=int(episode_decisions.sum()),
        acquisitions=int(episode_acquisitions.sum()),
        final_sufficient=final_sufficient,
        channel_counts=channel_counts,
        channel_switches=switches,
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
    return record


def collect(features, predictions):
    row_indices = predictions["row_indices"].astype(np.int64)
    world_codes = predictions["world_codes"].astype(np.int64)
    require(
        row_indices.shape == world_codes.shape == (9536,)
        and int(row_indices.min()) >= 0
        and int(row_indices.max()) < len(features)
        and int(world_codes.min()) >= 0
        and int(world_codes.max()) < 16,
        "Accepted episode identity drift",
    )
    raw12 = torch.from_numpy(features[row_indices].copy())
    raw13 = c193.budget13(raw12)
    projection = expected_projection(predictions)
    provider_map, endpoint_map = c202.providers()
    records = []
    for block in range(9):
        views = c190.make_views(
            raw13,row_indices,world_codes,
            f"C203-mixed-b{block}",
        )
        rec = replay_block(
            views,world_codes,
            predictions["necessity_predictions"][0,block],
            predictions["target_predictions"][0,block],
            provider_map,endpoint_map,
            projection["blocks"][block],
        )
        rec["block"] = block
        records.append(rec)
        print(
            f"[C203] block={block+1}/9 acquisitions={rec['acquisitions']} "
            f"switches={rec['channel_switches']} failed={rec['failed']}",
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
        failures=sum(r["failed"] for r in records),
        projection_errors=sum(r["projection_error"] for r in records),
    )
    for key in COUNTERS[1:]:
        totals[key+"s" if not key.endswith("s") else key] = sum(r[key] for r in records)
    return projection, records, totals


def gate(projection, records, totals):
    expected = projection["totals"]
    return (
        len(records) == 9
        and totals.get("episodes") == 85824
        and expected["decisions"] == 214948
        and expected["acquisitions"] == 129124
        and expected["final_sufficient"] == 85824
        and totals.get("decisions") == 214948
        and totals.get("acquisitions") == 129124
        and totals.get("final_sufficient") == 85824
        and totals.get("channel_counts") == expected["channel_counts"]
        and totals.get("channel_switches") == expected["channel_switches"]
        and expected["channel_switches"] > 0
        and totals.get("failures") == 0
        and totals.get("projection_errors") == 0
        and all(r.get("failed") == 0 and r.get("projection_error") == 0 for r in records)
    )


def precheck(c202_summary, c201_summary, c200_summary, c199_summary, c174_summary, root):
    from fold_lm.v05_benchmarks import gate_e_c202_three_channel_acquisition_dispatch as parent

    root = Path(root)
    c201_parent, c199, prediction_path, pins, protected = parent.precheck(
        c201_summary,c200_summary,c199_summary,root
    )
    require(audit.sha(c202_summary) == PARENT_C202_SHA, "C202 summary changed")
    c202_result = audit.read_json(c202_summary)
    parent.validate_result(c202_result)
    require(
        c202_result.get("commit_sha") == PARENT_C202_EXECUTION
        and c202_result.get("status") == "PASS"
        and parent.gate(c202_result["summary"],c202_result["block_records"])
        and c202_result.get("source_blobs") == pins,
        "Wrong accepted C202 parent",
    )
    protected[str(Path(c202_summary).resolve())] = PARENT_C202_SHA
    for artifact in c202_result["artifacts"]:
        path = audit.safe_child(Path(c202_summary).resolve().parent,artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C202 artifact:"+artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]

    c174_result,pilot_path,_ = load_c174_features(Path(c174_summary))
    protected[str(Path(c174_summary).resolve())] = C174_SHA
    protected[str(pilot_path.resolve())] = audit.sha(pilot_path)

    require(audit.sha(c199_summary) == TARGET_C199_SHA, "C199 target summary changed")
    require(c199.get("commit_sha") == TARGET_C199_EXECUTION, "Wrong C199 target execution")

    for name in parent.OWN:
        wanted = audit.git(root,"rev-parse",PARENT_C202_EXECUTION+":"+name).decode().strip()
        current = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
        require(current == wanted, "Accepted C202 source changed:"+name)
        pins[name] = wanted

    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    pins.update({name:allpins[name] for name in OWN})

    require(len(pins) == 31 and len(protected) == 53, "C203 source/protection count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C203 manifest drift")
    return c202_result,c199,prediction_path,c174_result,pilot_path,pins,protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c202_three_channel_acquisition_dispatch as parent
    names = parent.regression_modules(root)
    require(len(names) == len(set(names)) == 87, "Historical regression list drift")
    return names + ["tests_lm.test_v05_c203_mixed_channel_multistep_replay"]


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C203",
    )
    require(
        len(payload["source_blobs"]) == 31
        and len(payload["input_sha256"]) == 53
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C203 coverage drift",
    )
    require(
        payload["training_steps"] == 0
        and payload["fresh_seed_count"] == 0
        and payload["learned_forward_calls"] == 0
        and payload["network_calls"] == 0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False,
        "C203 scope drift",
    )
    require(
        payload["status"] == (
            "PASS" if gate(payload["expected_projection"],payload["block_records"],payload["summary"])
            else "FAIL"
        ),
        "C203 gate drift",
    )


def run(*, c202_summary, c201_summary, c200_summary, c199_summary, c174_summary,
        output_dir, expected_head):
    root = Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip() == expected_head,
                "HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()
                == "feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    _,_,prediction_path,_,_,pins,protected = precheck(
        c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,root
    )
    predictions = c201.load_c199_predictions(prediction_path)
    _,_,features = load_c174_features(Path(c174_summary))

    out = Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    artifacts = []
    started = time.perf_counter()

    def record(name):
        path = out/name
        artifacts.append(dict(file=name,sha256=audit.sha(path),
                              serialized_bytes=path.stat().st_size))

    def save(name,value):
        (out/name).write_bytes(blob(value));record(name)

    save("mixed-loop-plan.json",dict(manifest(),source_blobs=pins))
    try:
        projection,records,summary = collect(features,predictions)
        save("expected-projection.json",projection)
        save("block-results.json",records)
        save("provider-totals.json",summary["channel_counts"])
        save("postconditions.json",dict(
            parent_decision_masks=dict(available=list(PARENT_AVAILABLE),permitted=list(PARENT_PERMITTED)),
            action_window_masks=dict(available=list(ALL_TRUE),permitted=list(ALL_TRUE)),
            channel_layout=list(CHANNEL_LAYOUT),
            final_status="all episodes terminate at final accepted SUFFICIENT decision",
            resource_formula="internal=13-decisions-3*acquisitions; acquisitions=4-acquisitions; step=7+decisions+3*acquisitions",
        ))

        guard()
        precheck(c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,root)
        for path,wanted in protected.items():
            require(audit.sha(path) == wanted,"Protected input changed:"+path)
        for artifact in artifacts:
            require(audit.sha(out/artifact["file"]) == artifact["sha256"],
                    "Output changed:"+artifact["file"])

        result = dict(
            experiment_id=EXPERIMENT_ID,
            stage=STAGE,
            commit_sha=expected_head,
            status="PASS" if gate(projection,records,summary) else "FAIL",
            diagnostic_execution_valid=True,
            C202_summary_sha256=PARENT_C202_SHA,
            C199_target_summary_sha256=TARGET_C199_SHA,
            C174_summary_sha256=C174_SHA,
            source_blobs=pins,
            input_sha256=protected,
            artifacts=artifacts,
            expected_projection=projection,
            block_records=records,
            summary=summary,
            training_steps=0,
            fresh_seed_count=0,
            learned_forward_calls=0,
            network_calls=0,
            production_runtime_modified=False,
            gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=[
                "accepted saved learned decisions; no new learned forward",
                "fixed one-hot channel layout per fact",
                "trusted authority window enabled only after replayed decision",
                "fixture providers, not real sensor/user transport",
                "not learned channel preference or final Gate E",
            ],
        )
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C203] mixed-channel multi-step replay collected",flush=True)
        print("=== C203 RESULT ===",flush=True)
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
    parser.add_argument("--c202-summary",type=Path,required=True)
    parser.add_argument("--c201-summary",type=Path,required=True)
    parser.add_argument("--c200-summary",type=Path,required=True)
    parser.add_argument("--c199-summary",type=Path,required=True)
    parser.add_argument("--c174-summary",type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
