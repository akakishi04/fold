"""C202: dispatch accepted learned targets through all three structured acquisition channels.

No new training or target inference. Reuse accepted C199 ALLOWED phase-0 target indices, C200
structured-v2 channel metadata, C201 selected-fact mapper, and the existing structured acquisition
lifecycle. Every accepted target is executed independently under RETRIEVE, OBSERVE and ASK_USER
using in-memory coherent C190 world fixtures. The real lifecycle still validates source identity,
delivery binding, source document contents and observation publication.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from fold_lm.v05 import structured_action_channel as mapper
from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05 import structured_acquisition_lifecycle as life
from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as c185
from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190

EXPERIMENT_ID = "C202-v5e-three-channel-acquisition-dispatch"
STAGE = "V5-E-THREE-CHANNEL-ACQUISITION-DISPATCH"
BASE = "68156aec54130f4eef26644b8882cd9b99a7cb6d"
PARENT_C201_EXECUTION = "1ce0334e0d5ee76c7e5fac40082c19bd43576415"
PARENT_C201_SHA = "c27ff79f20811ce373d175617b2a556c3c847d631f096fb401cb0251ad4fca4c"
TARGET_C199_EXECUTION = "48100f36f4f1acdf44d5cb1d508b907e19724c10"
TARGET_C199_SHA = "0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9"
MANIFEST_SHA = "24bd6b04647342e8114a6e8245af046cfdae242a06d65c0a46286f577267406e"
BLOCKS = 9
EPISODES = 9536
DISPATCH_CASES = 257472
HISTORICAL = (
    "fold_lm/v05/structured_action_runtime.py",
    "fold_lm/v05/structured_acquisition_lifecycle.py",
    "fold_lm/v05_benchmarks/gate_e_c185_single_missing_acquisition.py",
    "fold_lm/v05_benchmarks/gate_e_c190_iterative_multimissing_acquisition.py",
)
OWN = (
    "fold_lm/v05_benchmarks/gate_e_c202_three_channel_acquisition_dispatch.py",
    "tests_lm/test_v05_c202_three_channel_acquisition_dispatch.py",
    "tools/run_c202.ps1",
    "tools/invoke_c202.ps1",
    "docs/experiment-ledger-addendum-c202-preregistration.md",
    "docs/three-channel-acquisition-dispatch-v0.1.md",
)
OUTPUTS = {
    "dispatch-plan.json",
    "block-results.json",
    "provider-totals.json",
    "target-distribution.json",
    "postconditions.json",
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
        acceptance_base=BASE,
        parent_c201_execution=PARENT_C201_EXECUTION,
        parent_c201_sha256=PARENT_C201_SHA,
        target_source_c199_execution=TARGET_C199_EXECUTION,
        target_source_c199_sha256=TARGET_C199_SHA,
        input_schema=v2.SCHEMA,
        action_schema=action.SCHEMA,
        acquisition_schema=life.SCHEMA,
        blocks=BLOCKS,
        episodes_per_block=EPISODES,
        channels=list(v2.CHANNELS),
        dispatch_cases=DISPATCH_CASES,
        provider_fixture="in-memory coherent C190 world source; actual lifecycle validates source/delivery/publication",
        initial_resources="internal12/acquisitions4/all channels available+permitted/last_outcome NONE/step8",
        final_resources="internal9/acquisitions3/all channels available+permitted/last_outcome NONE/step11/pending none",
        target_rule="accepted C199 ALLOWED phase0 target; no new target inference or relabeling",
        route_rule="C201 exactly-one channel mapper; selected fact index unchanged",
        training_steps=0,
        fresh_seed_count=0,
        learned_forward_calls=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        scope="three-channel acquisition lifecycle integration; not learned channel preference or final Gate E",
    )


class MemoryWorldProvider:
    """Trusted bounded fixture provider; dispatch still revalidates its source document."""
    def __init__(self, raw: bytes, source: life.SourceBinding):
        if type(raw) is not bytes or type(source) is not life.SourceBinding:
            raise TypeError("Raw coherent source and SourceBinding required")
        self.raw = raw
        self.source = source
        self.records = life.parse_source(raw, source)
        self.calls = 0

    def __call__(self, request: life.FetchRequest) -> life.Delivery:
        if type(request) is not life.FetchRequest or request.source != self.source:
            raise life.ProviderFailure("REQUEST_SOURCE_MISMATCH")
        self.calls += 1
        value = self.records.get(request.fact_id)
        return life.Delivery(
            life.SCHEMA,
            request.intent_id,
            request.request_id,
            request.scope_id,
            request.action,
            request.fact_id,
            self.source,
            "FOUND" if value is not None else "MISSING",
            value,
            life.reference_id(self.source, request.fact_id) if value is not None else None,
            self.raw.decode("utf-8"),
        )


def base_view(scope: str) -> v1.TaskView:
    resources = v1.Resources(
        internal_remaining=12,
        acquisitions_remaining=4,
        available=(True,True,True),
        permitted=(True,True,True),
        last_outcome="NONE",
        internal_step=8,
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
    facts = tuple(v1.Fact(fid) for fid in c185.FACT_IDS)
    return v1.TaskView(scope+"|query", scope, nodes, facts, resources, 1, 1)


def channel_view(base: v1.TaskView, fact_index: int, channel_index: int) -> v2.TaskView:
    require(type(fact_index) is int and 0 <= fact_index < 4, "Registered fact index required")
    require(type(channel_index) is int and 0 <= channel_index < 3, "Registered channel required")
    specs = [v2.FactChannels((False,False,False)) for _ in range(4)]
    bits = [False,False,False]
    bits[channel_index] = True
    specs[fact_index] = v2.FactChannels(tuple(bits))
    return v2.TaskView(base, tuple(specs))


def providers():
    provider_map = {}
    endpoint_map = {}
    for code in range(16):
        raw = c190.world_bytes(code)
        source = life.SourceBinding(
            f"C190-world-{code:02d}",
            hashlib.sha256(raw).hexdigest(),
        )
        provider_map[code] = {}
        endpoint_map[code] = {}
        for channel in v2.CHANNELS:
            provider = MemoryWorldProvider(raw, source)
            provider_map[code][channel] = provider
            endpoint_map[code][channel] = life.Endpoint(source, provider)
    return provider_map, endpoint_map


def execute_one(*, block: int, row: int, world_code: int, target: int,
                channel_index: int, provider_map, endpoint_map):
    channel = v2.CHANNELS[channel_index]
    base = base_view(f"C202-b{block}-r{row}-c{channel_index}")
    view = channel_view(base, target, channel_index)
    owner = life.AcquisitionOwner(
        action.RuntimeState(base),
        endpoint_map[world_code],
        max_dispatches=1,
    )

    before = tuple(provider_map[world_code][name].calls for name in v2.CHANNELS)
    proposal = mapper.propose_selected(view, owner.state, target)
    transition = owner.apply(proposal)
    dispatch = (
        owner.dispatch(transition.result.intent.intent_id)
        if transition.result.status == "PENDING" else None
    )
    after = tuple(provider_map[world_code][name].calls for name in v2.CHANNELS)

    expected_value = int(c190.WORLD_BITS[world_code][target])
    final = owner.state.view
    receipt = owner.receipts[0] if len(owner.receipts) == 1 else None

    route_error = int(not (
        proposal.action == channel
        and proposal.fact_index == target
        and proposal.expected_state_sha256 == action.state_digest(action.RuntimeState(base))
    ))
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
        and dispatch.evidence is not None
    ))
    provider_channel_error = int(not (
        after[channel_index] - before[channel_index] == 1
        and sum(after[i] - before[i] for i in range(3) if i != channel_index) == 0
    ))
    receipt_error = int(not (
        receipt is not None
        and receipt.action == channel
        and receipt.fact_id == c185.FACT_IDS[target]
        and receipt.value == expected_value
    ))
    selected_value_error = int(not (
        final.facts[target].status == "OBSERVED"
        and final.facts[target].value == expected_value
        and len(final.facts[target].reference_ids) == 1
    ))
    nonselected_mutation_error = int(any(
        final.facts[i].status != "UNOBSERVED"
        or final.facts[i].value is not None
        or final.facts[i].reference_ids
        for i in range(4) if i != target
    ))
    r = final.resources
    resource_error = int(not (
        r.internal_remaining == 9
        and r.acquisitions_remaining == 3
        and r.available == (True,True,True)
        and r.permitted == (True,True,True)
        and r.last_outcome == "NONE"
        and r.internal_step == 11
        and owner.state.pending is None
        and owner.state.terminal is None
    ))
    values = (
        route_error, action_error, dispatch_error, provider_channel_error,
        receipt_error, selected_value_error, nonselected_mutation_error, resource_error,
    )
    return dict(
        failed=int(any(values)),
        route_error=route_error,
        action_error=action_error,
        dispatch_error=dispatch_error,
        provider_channel_error=provider_channel_error,
        receipt_error=receipt_error,
        selected_value_error=selected_value_error,
        nonselected_mutation_error=nonselected_mutation_error,
        resource_error=resource_error,
    )


COUNTERS = (
    "failed","route_error","action_error","dispatch_error","provider_channel_error",
    "receipt_error","selected_value_error","nonselected_mutation_error","resource_error",
)


def collect(predictions):
    targets = predictions["target_predictions"][0,:,:,0]
    world_codes = predictions["world_codes"]
    require(targets.shape == (9,9536) and world_codes.shape == (9536,),
            "Accepted target/world alignment drift")

    provider_map, endpoint_map = providers()
    block_records = []
    target_distribution = []
    started_calls = {
        channel: sum(provider_map[c][channel].calls for c in range(16))
        for channel in v2.CHANNELS
    }

    for block in range(9):
        for channel_index, channel in enumerate(v2.CHANNELS):
            totals = {k:0 for k in COUNTERS}
            target_counts = [0,0,0,0]
            before_calls = sum(provider_map[c][channel].calls for c in range(16))
            for row in range(9536):
                target = int(targets[block,row])
                code = int(world_codes[row])
                target_counts[target] += 1
                score = execute_one(
                    block=block,
                    row=row,
                    world_code=code,
                    target=target,
                    channel_index=channel_index,
                    provider_map=provider_map,
                    endpoint_map=endpoint_map,
                )
                for key in COUNTERS:
                    totals[key] += score[key]
            after_calls = sum(provider_map[c][channel].calls for c in range(16))
            provider_calls = after_calls - before_calls
            block_records.append(dict(
                block=block,
                channel=channel,
                cases=9536,
                provider_calls=provider_calls,
                publications=9536 - totals["dispatch_error"],
                receipts=9536 - totals["receipt_error"],
                target_counts=target_counts,
                **totals,
            ))
            target_distribution.append(dict(
                block=block,
                channel=channel,
                target_counts=target_counts,
            ))
            print(
                f"[C202] block={block+1}/9 channel={channel} "
                f"cases=9536 failed={totals['failed']}",
                flush=True,
            )

    provider_totals = {
        channel: sum(provider_map[c][channel].calls for c in range(16)) - started_calls[channel]
        for channel in v2.CHANNELS
    }
    summary = dict(
        dispatch_cases=sum(r["cases"] for r in block_records),
        block_records=len(block_records),
        failures=sum(r["failed"] for r in block_records),
        route_errors=sum(r["route_error"] for r in block_records),
        action_errors=sum(r["action_error"] for r in block_records),
        dispatch_errors=sum(r["dispatch_error"] for r in block_records),
        provider_channel_errors=sum(r["provider_channel_error"] for r in block_records),
        receipt_errors=sum(r["receipt_error"] for r in block_records),
        selected_value_errors=sum(r["selected_value_error"] for r in block_records),
        nonselected_mutation_errors=sum(r["nonselected_mutation_error"] for r in block_records),
        resource_errors=sum(r["resource_error"] for r in block_records),
        provider_calls=sum(provider_totals.values()),
        publications=sum(r["publications"] for r in block_records),
        receipts=sum(r["receipts"] for r in block_records),
        channel_provider_calls=provider_totals,
    )
    postconditions = dict(
        expected_initial_resources=dict(
            internal_remaining=12, acquisitions_remaining=4,
            available=[True,True,True], permitted=[True,True,True],
            last_outcome="NONE", internal_step=8,
        ),
        expected_final_resources=dict(
            internal_remaining=9, acquisitions_remaining=3,
            available=[True,True,True], permitted=[True,True,True],
            last_outcome="NONE", internal_step=11,
        ),
        selected_fact="OBSERVED with registered coherent-world bit and one reference",
        nonselected_facts="UNOBSERVED with no value/reference",
        receipt_count=1,
    )
    return summary, block_records, provider_totals, target_distribution, postconditions


def gate(summary, records):
    return (
        summary.get("dispatch_cases") == DISPATCH_CASES
        and summary.get("block_records") == 27
        and all(summary.get(k) == 0 for k in (
            "failures","route_errors","action_errors","dispatch_errors",
            "provider_channel_errors","receipt_errors","selected_value_errors",
            "nonselected_mutation_errors","resource_errors",
        ))
        and summary.get("provider_calls") == DISPATCH_CASES
        and summary.get("publications") == DISPATCH_CASES
        and summary.get("receipts") == DISPATCH_CASES
        and summary.get("channel_provider_calls") == {
            "RETRIEVE":85824,"OBSERVE":85824,"ASK_USER":85824
        }
        and len(records) == 27
        and all(
            r.get("cases") == 9536
            and r.get("provider_calls") == 9536
            and r.get("publications") == 9536
            and r.get("receipts") == 9536
            and r.get("failed") == 0
            for r in records
        )
    )


def precheck(c201_summary, c200_summary, c199_summary, root):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c201_selected_fact_channel_route as parent

    root = Path(root)
    _, c199, prediction_path, pins, protected = parent.precheck(
        c200_summary, c199_summary, root
    )
    require(audit.sha(c201_summary) == PARENT_C201_SHA, "C201 summary changed")
    c201 = audit.read_json(c201_summary)
    parent.validate_result(c201)
    require(
        c201.get("commit_sha") == PARENT_C201_EXECUTION
        and c201.get("status") == "PASS"
        and parent.gate(c201["summary"])
        and c201.get("source_blobs") == pins,
        "Wrong accepted C201 parent",
    )

    protected[str(Path(c201_summary).resolve())] = PARENT_C201_SHA
    for artifact in c201["artifacts"]:
        path = audit.safe_child(Path(c201_summary).resolve().parent, artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C201 artifact:" + artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]

    require(audit.sha(c199_summary) == TARGET_C199_SHA, "C199 target summary changed")
    require(c199.get("commit_sha") == TARGET_C199_EXECUTION, "Wrong C199 target execution")
    for name in HISTORICAL:
        require(name in c199["source_blobs"], "Historical source missing from C199:" + name)
        wanted = c199["source_blobs"][name]
        current = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
        require(current == wanted, "Historical source changed:" + name)
        pins[name] = wanted

    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
    protected.update(audit.protect_tree_files(root, allpins))
    pins.update({name: allpins[name] for name in OWN})

    require(len(pins) == 25 and len(protected) == 39, "C202 source/protection count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C202 manifest drift")
    return c201, c199, prediction_path, pins, protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c201_selected_fact_channel_route as parent
    names = parent.regression_modules(root)
    require(len(names) == len(set(names)) == 86, "Historical regression list drift")
    return names + ["tests_lm.test_v05_c202_three_channel_acquisition_dispatch"]


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C202",
    )
    require(
        len(payload["source_blobs"]) == 25
        and len(payload["input_sha256"]) == 39
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C202 coverage drift",
    )
    require(
        payload["training_steps"] == 0
        and payload["fresh_seed_count"] == 0
        and payload["learned_forward_calls"] == 0
        and payload["network_calls"] == 0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False,
        "C202 scope drift",
    )
    require(
        payload["status"] == (
            "PASS" if gate(payload["summary"], payload["block_records"]) else "FAIL"
        ),
        "C202 gate drift",
    )


def run(*, c201_summary, c200_summary, c199_summary, output_dir, expected_head):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c201_selected_fact_channel_route as parent

    root = Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root, "rev-parse", "HEAD").decode().strip() == expected_head,
                "HEAD mismatch")
        require(audit.git(root, "branch", "--show-current").decode().strip()
                == "feat/sft-target-loss", "Branch mismatch")
        require(not audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    _, _, prediction_path, pins, protected = precheck(
        c201_summary, c200_summary, c199_summary, root
    )
    predictions = parent.load_c199_predictions(prediction_path)

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

    save("dispatch-plan.json", dict(manifest(), source_blobs=pins))
    try:
        summary, records, provider_totals, target_distribution, postconditions = collect(predictions)
        save("block-results.json", records)
        save("provider-totals.json", provider_totals)
        save("target-distribution.json", target_distribution)
        save("postconditions.json", postconditions)

        guard()
        precheck(c201_summary, c200_summary, c199_summary, root)
        for path, wanted in protected.items():
            require(audit.sha(path) == wanted, "Protected input changed:" + path)
        for artifact in artifacts:
            require(audit.sha(out / artifact["file"]) == artifact["sha256"],
                    "Output changed:" + artifact["file"])

        result = dict(
            experiment_id=EXPERIMENT_ID,
            stage=STAGE,
            commit_sha=expected_head,
            status="PASS" if gate(summary, records) else "FAIL",
            diagnostic_execution_valid=True,
            C201_summary_sha256=PARENT_C201_SHA,
            C199_target_summary_sha256=TARGET_C199_SHA,
            source_blobs=pins,
            input_sha256=protected,
            artifacts=artifacts,
            summary=summary,
            block_records=records,
            training_steps=0,
            fresh_seed_count=0,
            learned_forward_calls=0,
            network_calls=0,
            production_runtime_modified=False,
            gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=[
                "accepted saved target indices; no new target inference",
                "exactly-one channel metadata supplied by fixture",
                "in-memory provider fixtures, not real sensor/user transport",
                "not learned channel preference or final Gate E",
            ],
        )
        validate_result(result)
        (out / "summary.json").write_bytes(blob(result))
        print("[C202] three-channel acquisition dispatch collected", flush=True)
        print("=== C202 RESULT ===", flush=True)
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
    parser.add_argument("--c201-summary", type=Path, required=True)
    parser.add_argument("--c200-summary", type=Path, required=True)
    parser.add_argument("--c199-summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
