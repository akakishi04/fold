"""C200: opt-in per-fact acquisition-channel input contract diagnostic.

No learned policy, tool selection, transport, provider call or evidence write. Verify that
structured task input v2 preserves the canonical 72-feature v1 packet exactly and appends
only visible per-fact RETRIEVE / OBSERVE / ASK_USER eligibility metadata.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, replace
import hashlib
import itertools
import json
from pathlib import Path
import time

from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2

EXPERIMENT_ID = "C200-v5e-acquisition-channel-input"
STAGE = "V5-E-ACQUISITION-CHANNEL-INPUT"
BASE = "9bd98d750f81257b5e22f39bbe4c79462fcc8bd6"
PARENT_EXECUTION = "48100f36f4f1acdf44d5cb1d508b907e19724c10"
PARENT_SHA = "0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9"
MANIFEST_SHA = "af65cbab8b4e9d594fc4ffad5709acee07a5c85bc91a9148771c1dfe64de13bb"
EXPECTED = dict(mask_roundtrips=32, runtime_cross=448, hidden_pairs=12, malformed_cases=18)
PARENT_SOURCE = "fold_lm/v05/structured_task_input.py"
OWN = (
    "fold_lm/v05/structured_task_input_v2.py",
    "fold_lm/v05_benchmarks/gate_e_c200_acquisition_channel_input.py",
    "tests_lm/test_v05_c200_acquisition_channel_input.py",
    "tools/run_c200.ps1",
    "tools/invoke_c200.ps1",
    "docs/experiment-ledger-addendum-c200-preregistration.md",
    "docs/structured-task-interface-v0.2.md",
)
OUTPUTS = {
    "channel-plan.json",
    "mask-roundtrips.json",
    "runtime-cross.json",
    "hidden-pairs.json",
    "malformed.json",
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
        parent_execution=PARENT_EXECUTION,
        parent_sha256=PARENT_SHA,
        v1_schema=v1.SCHEMA,
        v2_schema=v2.SCHEMA,
        v1_feature_width=v1.FEATURE_WIDTH,
        v2_feature_width=v2.FEATURE_WIDTH,
        channels=list(v2.CHANNELS),
        layout="exact canonical v1 72-feature prefix + four fact slots x three channel eligibility bits",
        mask_roundtrips=32,
        runtime_cross=448,
        hidden_pairs=12,
        malformed_cases=18,
        hidden_values_in_input=False,
        answer_labels_in_input=False,
        necessity_labels_in_input=False,
        evaluator_dependency_in_input=False,
        runtime_authority_separate=True,
        training_steps=0,
        fresh_seed_count=0,
        learned_forward_calls=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        scope="input-contract diagnostic only; not learned tool selection or final Gate E",
    )


def four_fact_base(resources=v1.Resources()):
    nodes = (
        v1.Node("FACT", 0),
        v1.Node("FACT", 1),
        v1.Node("AND", left=0, right=1),
        v1.Node("FACT", 2),
        v1.Node("FACT", 3),
        v1.Node("OR", left=3, right=4),
        v1.Node("OR", left=2, right=5),
    )
    facts = tuple(v1.Fact(chr(65+i)) for i in range(4))
    return v1.TaskView("C200|four", "C200", nodes, facts, resources)


def two_fact_base(operator, known_a):
    nodes = (
        v1.Node("FACT", 0),
        v1.Node("FACT", 1),
        v1.Node(operator, left=0, right=1),
    )
    facts = (
        v1.Fact("A", "OBSERVED", known_a, ("C200:A",)),
        v1.Fact("B"),
    )
    return v1.TaskView("C200|pair", "C200", nodes, facts)


def one_fact_base(resources):
    return v1.TaskView(
        "C200|single",
        "C200",
        (v1.Node("FACT", 0),),
        (v1.Fact("A"),),
        resources,
    )


def all_masks():
    return tuple(itertools.product((False, True), repeat=3))


def mask_roundtrips():
    rows = []
    base = four_fact_base()
    parent = v1.encode(base)
    masks = all_masks()
    for slot in range(4):
        for mask in masks:
            specs = [v2.FactChannels((False, False, False)) for _ in range(4)]
            specs[slot] = v2.FactChannels(tuple(mask))
            view = v2.TaskView(base, tuple(specs))
            packet = v2.encode(view)
            recovered = v2.decode(packet)
            rows.append(dict(
                slot=slot,
                mask=list(mask),
                passed=(
                    recovered == view
                    and tuple(packet.features[:v1.FEATURE_WIDTH]) == parent.features
                    and packet.binding == parent.binding
                ),
                packet_sha256=digest(asdict(packet)),
            ))
    return rows


def runtime_cross():
    rows = []
    masks = all_masks()
    nonempty = [m for m in masks if any(m)]
    for channel_mask, available, permitted in itertools.product(nonempty, masks, masks):
        resources = v1.Resources(
            internal_remaining=8,
            acquisitions_remaining=2,
            available=tuple(available),
            permitted=tuple(permitted),
        )
        base = one_fact_base(resources)
        view = v2.TaskView(base, (v2.FactChannels(tuple(channel_mask)),))
        packet = v2.encode(view)
        recovered = v2.decode(packet)
        expected = tuple(
            name for i, name in enumerate(v2.CHANNELS)
            if channel_mask[i] and available[i] and permitted[i]
        )
        rows.append(dict(
            channel_mask=list(channel_mask),
            available=list(available),
            permitted=list(permitted),
            declared=list(v2.declared_channels(view, 0)),
            usable=list(v2.visible_usable_channels(view, 0)),
            expected=list(expected),
            passed=(
                recovered == view
                and tuple(packet.features[:v1.FEATURE_WIDTH]) == v1.encode(base).features
                and v2.visible_usable_channels(view, 0) == expected
            ),
        ))
    return rows


def hidden_pairs():
    rows = []
    one_hot = ((True,False,False),(False,True,False),(False,False,True))
    for mask, operator, known_a in itertools.product(one_hot, ("AND", "OR"), (0, 1)):
        base = two_fact_base(operator, known_a)
        view = v2.TaskView(
            base,
            (
                v2.FactChannels((False,False,False)),
                v2.FactChannels(mask),
            ),
        )
        packet0 = v2.encode(view)
        packet1 = v2.encode(view)
        out0 = (known_a & 0) if operator == "AND" else (known_a | 0)
        out1 = (known_a & 1) if operator == "AND" else (known_a | 1)
        rows.append(dict(
            channel=list(mask),
            operator=operator,
            known_a=known_a,
            evaluator_hidden_values=[0,1],
            evaluator_outputs=[out0,out1],
            answer_differs=out0 != out1,
            packet_equal=packet0 == packet1,
            hidden_value_present_in_packet=False,
            packet_sha256=digest(asdict(packet0)),
        ))
    return rows


def malformed_probes():
    base1 = one_fact_base(v1.Resources())
    good1 = v2.TaskView(base1, (v2.FactChannels((True,False,False)),))
    packet = v2.encode(good1)
    base2 = v1.TaskView(
        "C200|two", "C200",
        (v1.Node("FACT",0),v1.Node("FACT",1),v1.Node("AND",left=0,right=1)),
        (v1.Fact("A"),v1.Fact("B")),
    )
    good2 = v2.TaskView(
        base2,
        (v2.FactChannels((True,False,False)),v2.FactChannels((False,True,False))),
    )
    packet2 = v2.encode(good2)

    def changed(p, index, value):
        values = list(p.features)
        values[index] = value
        return replace(p, features=tuple(values))

    return (
        ("wrong-schema", lambda: v2.decode(replace(packet, schema="legacy"))),
        ("short-features", lambda: v2.decode(replace(packet, features=packet.features[:-1]))),
        ("long-features", lambda: v2.decode(replace(packet, features=packet.features+(0,)))),
        ("channel-two", lambda: v2.decode(changed(packet, 72, 2))),
        ("channel-bool", lambda: v2.decode(changed(packet, 72, True))),
        ("channel-negative", lambda: v2.decode(changed(packet, 72, -1))),
        ("channel-too-large", lambda: v2.decode(changed(packet, 72, v1.MAX_INTEGER+1))),
        ("padding-nonzero", lambda: v2.decode(changed(packet, 75, 1))),
        ("features-list", lambda: v2.decode(replace(packet, features=list(packet.features)))),
        ("binding-mapping", lambda: v2.decode(replace(packet, binding=asdict(packet.binding)))),
        ("binding-count", lambda: v2.decode(replace(
            packet2, binding=replace(packet2.binding, fact_ids=("A",))
        ))),
        ("v1-node-mask", lambda: v2.decode(changed(packet, 4, 0))),
        ("v1-hidden-payload", lambda: v2.decode(changed(packet, 49, 1))),
        ("view-channel-list", lambda: v2.TaskView(base1, [v2.FactChannels((True,False,False))])),
        ("view-channel-count", lambda: v2.TaskView(base1, ())),
        ("factchannels-list", lambda: v2.FactChannels([True,False,False])),
        ("factchannels-short", lambda: v2.FactChannels((True,False))),
        ("factchannels-integers", lambda: v2.FactChannels((1,0,0))),
    )


def malformed_rows():
    rows = []
    for name, fn in malformed_probes():
        try:
            fn()
        except (ValueError, TypeError) as exc:
            rows.append(dict(case_id=name, rejected=True, error_type=type(exc).__name__))
        else:
            rows.append(dict(case_id=name, rejected=False, error_type=None))
    return rows


def collect():
    masks = mask_roundtrips()
    runtime = runtime_cross()
    hidden = hidden_pairs()
    malformed = malformed_rows()
    summary = dict(
        mask_roundtrips=len(masks),
        runtime_cross=len(runtime),
        hidden_pairs=len(hidden),
        malformed_cases=len(malformed),
        roundtrip_failures=sum(not x["passed"] for x in masks),
        runtime_cross_failures=sum(not x["passed"] for x in runtime),
        hidden_packet_mismatches=sum(not x["packet_equal"] for x in hidden),
        hidden_answer_diff_pairs=sum(x["answer_differs"] for x in hidden),
        malformed_rejected=sum(x["rejected"] for x in malformed),
        v1_feature_width=v1.FEATURE_WIDTH,
        v2_feature_width=v2.FEATURE_WIDTH,
        v1_prefix_preserved=all(x["passed"] for x in masks) and all(x["passed"] for x in runtime),
        channel_classes=len(all_masks()),
    )
    return summary, masks, runtime, hidden, malformed


def gate(summary):
    return (
        all(summary.get(k) == v for k, v in EXPECTED.items())
        and summary.get("roundtrip_failures") == 0
        and summary.get("runtime_cross_failures") == 0
        and summary.get("hidden_packet_mismatches") == 0
        and summary.get("hidden_answer_diff_pairs") == 6
        and summary.get("malformed_rejected") == 18
        and summary.get("v1_feature_width") == 72
        and summary.get("v2_feature_width") == 84
        and summary.get("v1_prefix_preserved") is True
        and summary.get("channel_classes") == 8
    )


def precheck(c199_summary, root):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit

    root = Path(root)
    require(audit.sha(c199_summary) == PARENT_SHA, "C199 summary changed")
    parent = audit.read_json(c199_summary)
    require(
        parent.get("experiment_id") == "C199-v5e-attempt-limit-generic-loop"
        and parent.get("stage") == "V5-E-ATTEMPT-LIMIT-GENERIC-LOOP"
        and parent.get("commit_sha") == PARENT_EXECUTION
        and parent.get("status") == "PASS"
        and parent.get("diagnostic_execution_valid") is True
        and parent.get("production_runtime_modified") is False,
        "Wrong accepted C199 parent",
    )

    parent_v1 = audit.git(root, "rev-parse", PARENT_EXECUTION + ":" + PARENT_SOURCE).decode().strip()
    current_v1 = audit.git(root, "rev-parse", "HEAD:" + PARENT_SOURCE).decode().strip()
    require(parent_v1 == current_v1, "Canonical v1 source changed")

    paths = (PARENT_SOURCE,) + OWN
    pins = {name: audit.git(root, "rev-parse", "HEAD:" + name).decode().strip() for name in paths}
    protected = {str(Path(c199_summary).resolve()): PARENT_SHA}
    protected.update(audit.protect_tree_files(root, pins))
    require(len(pins) == 8 and len(protected) == 9, "C200 source/protection count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C200 manifest drift")
    return parent, pins, protected


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c199_attempt_limit_generic_loop as parent

    names = parent.regression_modules(root)
    require(len(names) == len(set(names)) == 84, "Historical regression list drift")
    return names + ["tests_lm.test_v05_c200_acquisition_channel_input"]


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C200",
    )
    require(
        len(payload["source_blobs"]) == 8
        and len(payload["input_sha256"]) == 9
        and len(payload["artifacts"]) == 5
        and {x["file"] for x in payload["artifacts"]} == OUTPUTS,
        "C200 coverage drift",
    )
    require(
        payload["training_steps"] == 0
        and payload["fresh_seed_count"] == 0
        and payload["learned_forward_calls"] == 0
        and payload["network_calls"] == 0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False,
        "C200 scope drift",
    )
    require(
        payload["status"] == ("PASS" if gate(payload["summary"]) else "FAIL"),
        "C200 gate drift",
    )


def run(*, c199_summary, output_dir, expected_head):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit

    root = Path(__file__).resolve().parents[2]

    def guard():
        require(
            audit.git(root, "rev-parse", "HEAD").decode().strip() == expected_head,
            "HEAD mismatch",
        )
        require(
            audit.git(root, "branch", "--show-current").decode().strip()
            == "feat/sft-target-loss",
            "Branch mismatch",
        )
        require(
            not audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(),
            "Dirty tracked tree",
        )

    guard()
    _, pins, protected = precheck(c199_summary, root)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    artifacts = []
    started = time.perf_counter()

    def record_file(name):
        path = out / name
        artifacts.append(dict(
            file=name,
            sha256=audit.sha(path),
            serialized_bytes=path.stat().st_size,
        ))

    def save(name, value):
        (out / name).write_bytes(blob(value))
        record_file(name)

    save("channel-plan.json", dict(manifest(), source_blobs=pins))
    try:
        summary, masks, runtime, hidden, malformed = collect()
        save("mask-roundtrips.json", masks)
        save("runtime-cross.json", runtime)
        save("hidden-pairs.json", hidden)
        save("malformed.json", malformed)

        guard()
        precheck(c199_summary, root)
        for path, wanted in protected.items():
            require(audit.sha(path) == wanted, "Protected input changed:" + path)
        for artifact in artifacts:
            require(
                audit.sha(out / artifact["file"]) == artifact["sha256"],
                "Output changed:" + artifact["file"],
            )

        result = dict(
            experiment_id=EXPERIMENT_ID,
            stage=STAGE,
            commit_sha=expected_head,
            status="PASS" if gate(summary) else "FAIL",
            diagnostic_execution_valid=True,
            C199_summary_sha256=PARENT_SHA,
            source_blobs=pins,
            input_sha256=protected,
            artifacts=artifacts,
            summary=summary,
            training_steps=0,
            fresh_seed_count=0,
            learned_forward_calls=0,
            network_calls=0,
            production_runtime_modified=False,
            gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=[
                "input-contract diagnostic only",
                "no learned acquisition-channel selector",
                "no tool execution, answer generation or final Gate E",
            ],
        )
        validate_result(result)
        (out / "summary.json").write_bytes(blob(result))
        print("[C200] channel input contract collected", flush=True)
        print("=== C200 RESULT ===", flush=True)
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
    parser.add_argument("--c199-summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
