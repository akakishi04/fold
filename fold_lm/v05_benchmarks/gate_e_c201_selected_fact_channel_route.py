"""C201: route accepted learned fact targets through structured-v2 channel metadata.

No new training and no provider execution. Use the accepted C199 saved phase-0 fact targets as
the target source. For each target, exercise all three exactly-one semantic channel variants and
verify that the opt-in mapper produces the same fact index and correct typed ActionProposal.
Separately cross semantic routing with real structured_action_runtime authority outcomes.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, replace
import json
import hashlib
from pathlib import Path
import time

import numpy as np

from fold_lm.v05 import structured_action_channel as mapper
from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2

EXPERIMENT_ID = "C201-v5e-selected-fact-channel-route"
STAGE = "V5-E-SELECTED-FACT-CHANNEL-ROUTE"
BASE = "fc8ac139a4a88a703349047c1993e8203258ba3b"
PARENT_C200_EXECUTION = "11181a355f13e7be2fda3957b9cdd45ad8868316"
PARENT_C200_SHA = "624889546c9b484003e3f2bc79c1d746de28ea168def13da1a2dc87fde73520e"
TARGET_C199_EXECUTION = "48100f36f4f1acdf44d5cb1d508b907e19724c10"
TARGET_C199_SHA = "0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9"
MANIFEST_SHA = "615e3aa8374650ae95c889c6e6d9de4b6a5a076327e06838ccae1b74eb71df25"
ROUTE_CASES = 257472
AUTHORITY_CROSS = 12
OBSERVED_CONTROLS = 3
INVALID_CASES = 7
OWN = (
    "fold_lm/v05/structured_action_channel.py",
    "fold_lm/v05_benchmarks/gate_e_c201_selected_fact_channel_route.py",
    "tests_lm/test_v05_c201_selected_fact_channel_route.py",
    "tools/run_c201.ps1",
    "tools/invoke_c201.ps1",
    "docs/experiment-ledger-addendum-c201-preregistration.md",
    "docs/structured-action-channel-v0.1.md",
)
OUTPUTS = {
    "channel-route-plan.json",
    "learned-target-routes.json",
    "authority-cross.json",
    "observed-controls.json",
    "invalid-mapper.json",
}


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
        parent_c200_execution=PARENT_C200_EXECUTION,
        parent_c200_sha256=PARENT_C200_SHA,
        target_source_c199_execution=TARGET_C199_EXECUTION,
        target_source_c199_sha256=TARGET_C199_SHA,
        input_schema=v2.SCHEMA,
        action_schema=action.SCHEMA,
        target_artifact_arm="ALLOWED",
        target_phase=0,
        blocks=9,
        episodes_per_block=9536,
        channel_variants=list(v2.CHANNELS),
        route_cases=ROUTE_CASES,
        authority_cross=AUTHORITY_CROSS,
        observed_controls=OBSERVED_CONTROLS,
        invalid_mapper_cases=INVALID_CASES,
        mapper="exactly one declared channel on selected fact -> typed ActionProposal with unchanged fact_index",
        authority_rule="mapper does not intersect runtime authority; structured_action_runtime.step reauthorizes proposal",
        target_rule="accepted C199 saved phase0 target only; no new target inference or relabeling",
        training_steps=0,
        fresh_seed_count=0,
        learned_forward_calls=0,
        provider_calls=0,
        network_calls=0,
        evidence_writes=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        scope="reference integration diagnostic; not learned channel preference or final Gate E",
    )


def load_c199_predictions(path):
    p = Path(path)
    require(p.is_file() and p.stat().st_size < 20_000_000,
            "Unexpected C199 prediction artifact size")
    with np.load(p, allow_pickle=False) as z:
        expected = {
            "necessity_predictions", "necessity_logits", "target_predictions", "target_logits",
            "row_indices", "local_rows", "world_codes",
        }
        require(set(z.files) == expected, "C199 prediction schema drift")
        out = {k: z[k].copy() for k in z.files}
    require(
        out["necessity_predictions"].shape == (2,9,9536,4)
        and out["necessity_logits"].shape == (2,9,9536,4,2)
        and out["target_predictions"].shape == (2,9,9536,3)
        and out["target_logits"].shape == (2,9,9536,3,4)
        and out["row_indices"].shape == (9536,)
        and out["local_rows"].shape == (9536,)
        and out["world_codes"].shape == (9536,),
        "C199 prediction array drift",
    )
    phase0_n = out["necessity_predictions"][0,:,:,0]
    phase0_t = out["target_predictions"][0,:,:,0]
    require(np.all(phase0_n == 1), "C199 initial cohort is not all NEEDS")
    require(np.all((0 <= phase0_t) & (phase0_t < 4)), "C199 initial target out of range")
    return out


def four_fact_base(resources=None):
    if resources is None:
        resources = v1.Resources(
            internal_remaining=8,
            acquisitions_remaining=2,
            available=(True,True,True),
            permitted=(True,True,True),
        )
    nodes = (
        v1.Node("FACT",0),
        v1.Node("FACT",1),
        v1.Node("AND",left=0,right=1),
        v1.Node("FACT",2),
        v1.Node("FACT",3),
        v1.Node("OR",left=3,right=4),
        v1.Node("OR",left=2,right=5),
    )
    facts = tuple(v1.Fact(chr(65+i)) for i in range(4))
    return v1.TaskView("C201|route", "C201", nodes, facts, resources)


def v2_for_selected(base, fact_index, channel_index):
    require(type(fact_index) is int and 0 <= fact_index < 4, "Registered fact index required")
    require(type(channel_index) is int and 0 <= channel_index < 3, "Registered channel index required")
    specs = [v2.FactChannels((False,False,False)) for _ in range(4)]
    bits = [False,False,False]
    bits[channel_index] = True
    specs[fact_index] = v2.FactChannels(tuple(bits))
    return v2.TaskView(base, tuple(specs))


def prototype_routes():
    base = four_fact_base()
    state = action.RuntimeState(base)
    rows = []
    for fact_index in range(4):
        for channel_index, channel in enumerate(v2.CHANNELS):
            view = v2_for_selected(base, fact_index, channel_index)
            proposal = mapper.propose_selected(view, state, fact_index)
            rows.append(dict(
                fact_index=fact_index,
                channel=channel,
                proposal=asdict(proposal),
                passed=(
                    proposal.action == channel
                    and proposal.fact_index == fact_index
                    and proposal.request_id == base.request_id
                    and proposal.scope_id == base.scope_id
                    and proposal.expected_state_sha256 == action.state_digest(state)
                ),
            ))
    return rows


def learned_target_routes(predictions):
    prototypes = {(r["fact_index"], r["channel"]): r for r in prototype_routes()}
    targets = predictions["target_predictions"][0,:,:,0]
    rows = []
    mismatches = 0
    total = 0
    for block in range(9):
        block_targets = targets[block]
        for channel in v2.CHANNELS:
            for fact_index in range(4):
                count = int((block_targets == fact_index).sum())
                proto = prototypes[(fact_index, channel)]
                mismatch = 0 if proto["passed"] else count
                rows.append(dict(
                    block=block,
                    channel=channel,
                    fact_index=fact_index,
                    cases=count,
                    route_mismatches=mismatch,
                ))
                total += count
                mismatches += mismatch
    return rows, total, mismatches


def one_fact_base(channel_index, available, permitted, *, observed=False):
    av = [False,False,False]
    pe = [False,False,False]
    av[channel_index] = available
    pe[channel_index] = permitted
    resources = v1.Resources(
        internal_remaining=4,
        acquisitions_remaining=1,
        available=tuple(av),
        permitted=tuple(pe),
    )
    fact = (
        v1.Fact("A", "OBSERVED", 1, ("C201:observed",))
        if observed else v1.Fact("A")
    )
    return v1.TaskView(
        "C201|single", "C201",
        (v1.Node("FACT",0),),
        (fact,),
        resources,
    )


def one_fact_v2(base, channel_index):
    bits = [False,False,False]
    bits[channel_index] = True
    return v2.TaskView(base, (v2.FactChannels(tuple(bits)),))


def authority_rows():
    rows = []
    for channel_index, channel in enumerate(v2.CHANNELS):
        for available in (False, True):
            for permitted in (False, True):
                base = one_fact_base(channel_index, available, permitted)
                view = one_fact_v2(base, channel_index)
                state = action.RuntimeState(base)
                proposal = mapper.propose_selected(view, state, 0)
                transition = action.step(state, proposal)
                if not permitted:
                    expected = ("DENIED", "PERMISSION_DENIED")
                elif not available:
                    expected = ("DENIED", "PROVIDER_UNAVAILABLE")
                else:
                    expected = ("PENDING", "ACQUISITION_RESERVED")
                rows.append(dict(
                    channel=channel,
                    available=available,
                    permitted=permitted,
                    proposal_action=proposal.action,
                    result_status=transition.result.status,
                    result_reason=transition.result.reason,
                    passed=(
                        proposal.action == channel
                        and proposal.fact_index == 0
                        and (transition.result.status, transition.result.reason) == expected
                    ),
                ))
    return rows


def observed_rows():
    rows = []
    for channel_index, channel in enumerate(v2.CHANNELS):
        base = one_fact_base(channel_index, True, True, observed=True)
        view = one_fact_v2(base, channel_index)
        state = action.RuntimeState(base)
        proposal = mapper.propose_selected(view, state, 0)
        transition = action.step(state, proposal)
        rows.append(dict(
            channel=channel,
            proposal_action=proposal.action,
            result_status=transition.result.status,
            result_reason=transition.result.reason,
            passed=(
                proposal.action == channel
                and transition.result.status == "DENIED"
                and transition.result.reason == "ALREADY_OBSERVED"
            ),
        ))
    return rows


def invalid_rows():
    base = four_fact_base()
    state = action.RuntimeState(base)

    def view_with(bits):
        specs = [v2.FactChannels((False,False,False)) for _ in range(4)]
        specs[0] = v2.FactChannels(bits)
        return v2.TaskView(base, tuple(specs))

    other = replace(base, revision=base.revision+1)
    probes = (
        ("zero-channel", lambda: mapper.propose_selected(view_with((False,False,False)), state, 0)),
        ("multi-channel", lambda: mapper.propose_selected(view_with((True,True,False)), state, 0)),
        ("negative-index", lambda: mapper.propose_selected(view_with((True,False,False)), state, -1)),
        ("high-index", lambda: mapper.propose_selected(view_with((True,False,False)), state, 4)),
        ("state-view-mismatch", lambda: mapper.propose_selected(
            v2.TaskView(other, view_with((True,False,False)).channels), state, 0)),
        ("wrong-view-type", lambda: mapper.propose_selected(base, state, 0)),
        ("wrong-state-type", lambda: mapper.propose_selected(
            view_with((True,False,False)), base, 0)),
    )
    rows = []
    for case_id, fn in probes:
        try:
            fn()
        except (TypeError, ValueError) as exc:
            rows.append(dict(case_id=case_id, rejected=True, error_type=type(exc).__name__))
        else:
            rows.append(dict(case_id=case_id, rejected=False, error_type=None))
    return rows


def collect(predictions):
    route_rows, route_cases, route_mismatches = learned_target_routes(predictions)
    authority = authority_rows()
    observed = observed_rows()
    invalid = invalid_rows()
    summary = dict(
        route_cases=route_cases,
        route_records=len(route_rows),
        route_mismatches=route_mismatches,
        channel_case_totals={
            channel: sum(r["cases"] for r in route_rows if r["channel"] == channel)
            for channel in v2.CHANNELS
        },
        authority_cross=len(authority),
        authority_failures=sum(not r["passed"] for r in authority),
        authority_pending=sum(r["result_status"] == "PENDING" for r in authority),
        authority_permission_denied=sum(r["result_reason"] == "PERMISSION_DENIED" for r in authority),
        authority_unavailable=sum(r["result_reason"] == "PROVIDER_UNAVAILABLE" for r in authority),
        observed_controls=len(observed),
        observed_failures=sum(not r["passed"] for r in observed),
        invalid_mapper_cases=len(invalid),
        invalid_mapper_rejected=sum(r["rejected"] for r in invalid),
    )
    return summary, route_rows, authority, observed, invalid


def gate(summary):
    return (
        summary.get("route_cases") == ROUTE_CASES
        and summary.get("route_records") == 108
        and summary.get("route_mismatches") == 0
        and summary.get("channel_case_totals") == {
            "RETRIEVE": 85824, "OBSERVE": 85824, "ASK_USER": 85824
        }
        and summary.get("authority_cross") == AUTHORITY_CROSS
        and summary.get("authority_failures") == 0
        and summary.get("authority_pending") == 3
        and summary.get("authority_permission_denied") == 6
        and summary.get("authority_unavailable") == 3
        and summary.get("observed_controls") == OBSERVED_CONTROLS
        and summary.get("observed_failures") == 0
        and summary.get("invalid_mapper_cases") == INVALID_CASES
        and summary.get("invalid_mapper_rejected") == INVALID_CASES
    )


def precheck(c200_summary, c199_summary, root):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c200_acquisition_channel_input as parent

    root = Path(root)
    parent_c199, pins, protected = parent.precheck(c199_summary, root)
    require(audit.sha(c200_summary) == PARENT_C200_SHA, "C200 summary changed")
    c200 = audit.read_json(c200_summary)
    parent.validate_result(c200)
    require(
        c200.get("commit_sha") == PARENT_C200_EXECUTION
        and c200.get("status") == "PASS"
        and parent.gate(c200["summary"]),
        "Wrong accepted C200 parent",
    )

    for name in parent.OWN:
        accepted = audit.git(root, "rev-parse", PARENT_C200_EXECUTION + ":" + name).decode().strip()
        current = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
        require(current == accepted, "Accepted C200 source changed:" + name)

    protected[str(Path(c200_summary).resolve())] = PARENT_C200_SHA
    for artifact in c200["artifacts"]:
        path = audit.safe_child(Path(c200_summary).resolve().parent, artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C200 artifact:" + artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]

    require(audit.sha(c199_summary) == TARGET_C199_SHA, "C199 target summary changed")
    c199 = audit.read_json(c199_summary)
    require(
        c199.get("experiment_id") == "C199-v5e-attempt-limit-generic-loop"
        and c199.get("commit_sha") == TARGET_C199_EXECUTION
        and c199.get("status") == "PASS"
        and c199.get("diagnostic_execution_valid") is True,
        "Wrong accepted C199 target source",
    )
    prediction = next(
        (a for a in c199["artifacts"] if a["file"] == "episode-predictions.npz"), None
    )
    require(prediction is not None, "C199 prediction artifact missing")
    prediction_path = audit.safe_child(Path(c199_summary).resolve().parent, prediction["file"])
    require(
        prediction_path.is_file()
        and prediction_path.stat().st_size == prediction["serialized_bytes"]
        and audit.sha(prediction_path) == prediction["sha256"],
        "Changed C199 prediction artifact",
    )
    protected[str(prediction_path.resolve())] = prediction["sha256"]

    pins = dict(pins)
    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
    protected.update(audit.protect_tree_files(root, allpins))
    pins.update({name: allpins[name] for name in OWN})
    require(len(pins) == 15 and len(protected) == 23, "C201 source/protection count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C201 manifest drift")
    return c200, c199, prediction_path, pins, protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c200_acquisition_channel_input as parent
    names = parent.regression_modules(root)
    require(len(names) == len(set(names)) == 85, "Historical regression list drift")
    return names + ["tests_lm.test_v05_c201_selected_fact_channel_route"]


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C201",
    )
    require(
        len(payload["source_blobs"]) == 15
        and len(payload["input_sha256"]) == 23
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C201 coverage drift",
    )
    require(
        payload["training_steps"] == 0
        and payload["fresh_seed_count"] == 0
        and payload["learned_forward_calls"] == 0
        and payload["provider_calls"] == 0
        and payload["network_calls"] == 0
        and payload["evidence_writes"] == 0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False,
        "C201 scope drift",
    )
    require(
        payload["status"] == ("PASS" if gate(payload["summary"]) else "FAIL"),
        "C201 gate drift",
    )


def run(*, c200_summary, c199_summary, output_dir, expected_head):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    root = Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root, "rev-parse", "HEAD").decode().strip() == expected_head,
                "HEAD mismatch")
        require(audit.git(root, "branch", "--show-current").decode().strip()
                == "feat/sft-target-loss", "Branch mismatch")
        require(not audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    _, _, prediction_path, pins, protected = precheck(c200_summary, c199_summary, root)
    predictions = load_c199_predictions(prediction_path)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    artifacts = []
    started = time.perf_counter()

    def record(name):
        path = out / name
        artifacts.append(dict(file=name, sha256=audit.sha(path),
                              serialized_bytes=path.stat().st_size))

    def save(name, value):
        (out / name).write_bytes(blob(value))
        record(name)

    save("channel-route-plan.json", dict(manifest(), source_blobs=pins))
    try:
        summary, routes, authority, observed, invalid = collect(predictions)
        save("learned-target-routes.json", routes)
        save("authority-cross.json", authority)
        save("observed-controls.json", observed)
        save("invalid-mapper.json", invalid)

        guard()
        precheck(c200_summary, c199_summary, root)
        for path, wanted in protected.items():
            require(audit.sha(path) == wanted, "Protected input changed:" + path)
        for artifact in artifacts:
            require(audit.sha(out / artifact["file"]) == artifact["sha256"],
                    "Output changed:" + artifact["file"])

        result = dict(
            experiment_id=EXPERIMENT_ID,
            stage=STAGE,
            commit_sha=expected_head,
            status="PASS" if gate(summary) else "FAIL",
            diagnostic_execution_valid=True,
            C200_summary_sha256=PARENT_C200_SHA,
            C199_target_summary_sha256=TARGET_C199_SHA,
            source_blobs=pins,
            input_sha256=protected,
            artifacts=artifacts,
            summary=summary,
            training_steps=0,
            fresh_seed_count=0,
            learned_forward_calls=0,
            provider_calls=0,
            network_calls=0,
            evidence_writes=0,
            production_runtime_modified=False,
            gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=[
                "accepted saved target indices; no new target inference",
                "exactly-one declared channel only",
                "reference mapper, not learned channel preference",
                "no provider execution or final Gate E",
            ],
        )
        validate_result(result)
        (out / "summary.json").write_bytes(blob(result))
        print("[C201] selected-fact channel routing collected", flush=True)
        print("=== C201 RESULT ===", flush=True)
        print(blob(result).decode(), flush=True)
        return result
    except Exception as exc:
        (out / "invalid.json").write_bytes(blob(dict(
            experiment_id=EXPERIMENT_ID,
            status="INVALID",
            diagnostic_execution_valid=False,
            error=str(exc),
        )))
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c200-summary", type=Path, required=True)
    parser.add_argument("--c199-summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
