"""C206: terminal mixed-channel state -> verified derived-result integration.

Replay the accepted C199 ALLOWED decision trace through the accepted C203 mixed-channel lifecycle.
At every final SUFFICIENT state, use the C171 benchmark-only proof fixture as a reference candidate
producer and the production structured_derived_result.verify() as the deciding checker.

This does not test learned proof generation. It tests the Gate-E output boundary: a logical
conclusion is emitted as DERIVED with supporting references and never promoted to OBSERVED.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import time
import unittest

import numpy as np
import torch

from fold_lm.v05 import structured_action_channel as mapper
from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05 import structured_acquisition_lifecycle as life
from fold_lm.v05 import structured_derived_result as derived
from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05_benchmarks import gate_e_c171_derived_result as c171
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as c185
from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
from fold_lm.v05_benchmarks import gate_e_c193_budget13_authoritative_closure as c193
from fold_lm.v05_benchmarks import gate_e_c201_selected_fact_channel_route as c201
from fold_lm.v05_benchmarks import gate_e_c202_three_channel_acquisition_dispatch as c202
from fold_lm.v05_benchmarks import gate_e_c203_mixed_channel_multistep_replay as c203
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205

EXPERIMENT_ID = "C206-v5e-terminal-derived-result-integration"
STAGE = "V5-E-TERMINAL-DERIVED-RESULT-INTEGRATION"
BASE = "7a3f69283f3395cbc69adf64d3cc45ab57987d0d"
PARENT_C205_EXECUTION = "c78b79e95b92552c032df05220868122398fd339"
PARENT_C205_SHA = "2f60e87aa7158bf22e1a4f6b15904a4e66096a1db81a6477e0b398be87fc3c2b"
MANIFEST_SHA = "4841fda580c84bc66fb66f2fb123d08ec0dd7feedf29ab2aecbf85954970ac51"
BLOCKS = 9
EPISODES = 9536
MAX_STEPS = derived.MAX_PROOF_STEPS
C171_FILES = (
    "fold_lm/v05/structured_derived_result.py",
    "fold_lm/v05_benchmarks/gate_e_c171_derived_result.py",
    "tests_lm/test_v05_c171_derived_result.py",
    "tools/run_c171.ps1",
    "docs/structured-derived-result-v0.1.md",
    "docs/experiment-ledger-addendum-c171-preregistration.md",
)
OWN = (
    "fold_lm/v05_benchmarks/gate_e_c206_terminal_derived_result_integration.py",
    "tests_lm/test_v05_c206_terminal_derived_result_integration.py",
    "tools/run_c206.ps1",
    "tools/invoke_c206.ps1",
    "docs/experiment-ledger-addendum-c206-preregistration.md",
    "docs/terminal-derived-result-integration-v0.1.md",
)
OUTPUTS = {
    "derived-integration-plan.json",
    "block-results.json",
    "verification-totals.json",
    "support-profile.json",
    "negative-controls.json",
}
COUNTERS = (
    "failed",
    "decision_trace_error",
    "target_error",
    "route_error",
    "action_error",
    "dispatch_error",
    "provider_channel_error",
    "receipt_error",
    "fact_update_error",
    "authority_restore_error",
    "resource_error",
    "semantic_unresolved_error",
    "world_value_error",
    "verification_error",
    "opposite_rejection_error",
    "support_error",
    "mutation_error",
    "derived_schema_error",
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
        parent_c205_execution=PARENT_C205_EXECUTION,
        parent_c205_sha256=PARENT_C205_SHA,
        behavioral_reference="accepted C199 ALLOWED saved necessity/target trace, behaviorally identical to C204 live argmax trajectory",
        terminal_episodes=85824,
        blocks=9,
        decisions=214948,
        acquisitions=129124,
        channel_counts={"RETRIEVE":88918,"OBSERVE":21252,"ASK_USER":18954},
        channel_switches=32564,
        candidate_producer="C171 benchmark-only proof_fixture; not learned reasoning and not production code",
        deciding_verifier="fold_lm.v05.structured_derived_result.verify",
        semantic_oracle="C171 completion_values independent exhaustive evaluator; evaluator-only",
        correct_verifications=85824,
        opposite_controls=85824,
        verifier_calls=171648,
        maximum_proof_steps=7,
        training_steps=0,
        fresh_seed_count=0,
        learned_forward_calls=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        scope="terminal derived-result contract integration only; not learned proof generation, language answer generation, or final Gate E",
    )


def world_value(view: v1.TaskView, world_code: int) -> int:
    bits = c190.WORLD_BITS[int(world_code)]
    stack = []
    for node in view.nodes:
        if node.kind == "FACT":
            stack.append(int(bits[node.fact]) ^ int(node.negate))
        elif node.kind == "AND":
            stack.append(stack[node.left] & stack[node.right])
        else:
            stack.append(stack[node.left] | stack[node.right])
    return int(stack[-1])


def verify_terminal(view: v1.TaskView, world_code: int):
    before = blob(asdict(view))
    completions = c171.completion_values(view)
    semantic_error = int(len(completions) != 1)
    expected = int(completions[0]) if len(completions) == 1 else 0
    world_error = int(len(completions) == 1 and expected != world_value(view, world_code))

    proof, support = c171.proof_fixture(view)
    candidate = derived.bind_candidate(view, expected, proof, support)
    result = derived.verify(view, candidate, max_steps=MAX_STEPS)

    verified = bool(
        len(completions) == 1
        and result.status == "VERIFIED_DERIVED"
        and result.reason == "VALID_LOCAL_PROOF"
        and result.schema == derived.SCHEMA
        and result.derivation_kind == "BOOLEAN_LOCAL_PROOF"
        and result.value == expected
        and result.supporting_references == support
        and result.proof == proof
        and 1 <= result.checked_steps <= MAX_STEPS
    )
    verification_error = int(not verified)

    opposite = derived.bind_candidate(view, 1 - expected, proof, support)
    opposite_result = derived.verify(view, opposite, max_steps=MAX_STEPS)
    opposite_error = int(not (
        opposite_result.status == "REJECTED"
        and opposite_result.value is None
        and opposite_result.supporting_references == ()
        and opposite_result.proof == ()
        and 1 <= opposite_result.checked_steps <= MAX_STEPS
    ))

    support_error = int(not (
        1 <= len(support) <= len(view.facts)
        and tuple(s.fact_index for s in support) == tuple(sorted(s.fact_index for s in support))
        and all(
            view.facts[s.fact_index].status == "OBSERVED"
            and view.facts[s.fact_index].reference_ids == (s.reference_id,)
            for s in support
        )
    ))
    schema_error = int(
        result.schema == v1.SCHEMA
        or result.derivation_kind != "BOOLEAN_LOCAL_PROOF"
        or result.status == "OBSERVED"
    )
    mutation_error = int(blob(asdict(view)) != before)

    return dict(
        semantic_unresolved_error=semantic_error,
        world_value_error=world_error,
        verification_error=verification_error,
        opposite_rejection_error=opposite_error,
        support_error=support_error,
        mutation_error=mutation_error,
        derived_schema_error=schema_error,
        verified_derived=int(verified),
        opposite_rejected=int(not opposite_error),
        verifier_calls=2,
        support_count=len(support),
        checked_steps=result.checked_steps,
    )


def replay_and_verify_block(
    views, world_codes, necessity, targets, provider_map, endpoint_map, expected
):
    require(len(views) == len(world_codes) > 0, "Block alignment required")
    n = len(views)
    owners = [
        life.AcquisitionOwner(
            action.RuntimeState(view),
            endpoint_map[int(code)],
            max_dispatches=3,
        )
        for view,code in zip(views,world_codes,strict=True)
    ]
    decisions = np.zeros(n,dtype=np.int8)
    acquisitions = np.zeros(n,dtype=np.int8)
    channel_sequences = [[] for _ in range(n)]
    counters = {key:0 for key in COUNTERS}
    terminal = dict(
        verified_derived=0,
        opposite_rejected=0,
        verifier_calls=0,
        support_total=0,
        support_min=5,
        support_max=0,
        checked_steps=0,
        terminal_sufficient=0,
    )
    provider_before = {
        channel:sum(provider_map[c][channel].calls for c in range(16))
        for channel in v2.CHANNELS
    }
    active = list(range(n))

    for phase in range(4):
        next_active = []
        for i in active:
            owner = owners[i]
            r0 = owner.state.view.resources
            if not (
                r0.available == c203.PARENT_AVAILABLE
                and r0.permitted == c203.PARENT_PERMITTED
            ):
                counters["authority_restore_error"] += 1
                counters["failed"] += 1
                continue
            if not c185.charge_decision(owner):
                counters["decision_trace_error"] += 1
                counters["failed"] += 1
                continue
            decisions[i] += 1
            pred = int(necessity[i,phase])
            if pred not in (0,1):
                counters["decision_trace_error"] += 1
                counters["failed"] += 1
                continue

            if pred == 0:
                check = verify_terminal(owner.state.view,int(world_codes[i]))
                terminal["terminal_sufficient"] += 1
                terminal["verified_derived"] += check["verified_derived"]
                terminal["opposite_rejected"] += check["opposite_rejected"]
                terminal["verifier_calls"] += check["verifier_calls"]
                terminal["support_total"] += check["support_count"]
                terminal["support_min"] = min(terminal["support_min"],check["support_count"])
                terminal["support_max"] = max(terminal["support_max"],check["support_count"])
                terminal["checked_steps"] += check["checked_steps"]
                local = 0
                for key in (
                    "semantic_unresolved_error","world_value_error","verification_error",
                    "opposite_rejection_error","support_error","mutation_error",
                    "derived_schema_error",
                ):
                    counters[key] += check[key]
                    local += check[key]
                if local:
                    counters["failed"] += 1
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
            c203.set_authority(owner,all_channels=True)
            typed = c203.mixed_view(owner.state.view)
            proposal = mapper.propose_selected(typed,owner.state,target)
            channel = c203.CHANNEL_LAYOUT[target]
            before_calls = tuple(
                provider_map[int(world_codes[i])][name].calls for name in v2.CHANNELS
            )
            transition = owner.apply(proposal)
            dispatch = (
                owner.dispatch(transition.result.intent.intent_id)
                if transition.result.status == "PENDING" else None
            )
            after_calls = tuple(
                provider_map[int(world_codes[i])][name].calls for name in v2.CHANNELS
            )

            route_error = int(not (
                proposal.action == channel and proposal.fact_index == target
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
            ))
            ci = v2.CHANNELS.index(channel)
            provider_error = int(not (
                after_calls[ci] - before_calls[ci] == 1
                and sum(
                    after_calls[k] - before_calls[k]
                    for k in range(3) if k != ci
                ) == 0
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
            fact_error = int(not (
                after_facts[target].status == "OBSERVED"
                and after_facts[target].value == expected_value
                and all(
                    after_facts[k] == before_facts[k]
                    for k in range(4) if k != target
                )
            ))
            for key,value in (
                ("route_error",route_error),
                ("action_error",action_error),
                ("dispatch_error",dispatch_error),
                ("provider_channel_error",provider_error),
                ("receipt_error",receipt_error),
                ("fact_update_error",fact_error),
            ):
                counters[key] += value
            if any((route_error,action_error,dispatch_error,provider_error,receipt_error,fact_error)):
                counters["failed"] += 1
                continue

            acquisitions[i] += 1
            channel_sequences[i].append(channel)
            c203.set_authority(owner,all_channels=False)
            rr = owner.state.view.resources
            if not (
                rr.available == c203.PARENT_AVAILABLE
                and rr.permitted == c203.PARENT_PERMITTED
            ):
                counters["authority_restore_error"] += 1
                counters["failed"] += 1
                continue
            next_active.append(i)
        active = next_active

    if active:
        counters["decision_trace_error"] += len(active)
        counters["failed"] += len(active)

    switches = 0
    for i,owner in enumerate(owners):
        d = int(decisions[i])
        acq = int(acquisitions[i])
        ref_d = int((necessity[i] >= 0).sum())
        ref_a = sum(int(x) == 1 for x in necessity[i] if int(x) >= 0)
        if (d,acq) != (ref_d,ref_a):
            counters["decision_trace_error"] += 1
            counters["failed"] += 1
        r = owner.state.view.resources
        if not (
            r.internal_remaining == 13 - d - 3*acq
            and r.acquisitions_remaining == 4 - acq
            and r.internal_step == 7 + d + 3*acq
            and r.available == c203.PARENT_AVAILABLE
            and r.permitted == c203.PARENT_PERMITTED
            and r.last_outcome == "NONE"
            and owner.state.pending is None
            and owner.state.terminal is None
            and len(owner.receipts) == acq
        ):
            counters["resource_error"] += 1
            counters["failed"] += 1
        switches += sum(
            left != right
            for left,right in zip(channel_sequences[i],channel_sequences[i][1:])
        )

    provider_after = {
        channel:sum(provider_map[c][channel].calls for c in range(16))
        for channel in v2.CHANNELS
    }
    channel_counts = {
        channel:provider_after[channel]-provider_before[channel]
        for channel in v2.CHANNELS
    }
    record = dict(
        episodes=n,
        decisions=int(decisions.sum()),
        acquisitions=int(acquisitions.sum()),
        channel_counts=channel_counts,
        channel_switches=switches,
        **terminal,
        **counters,
    )
    projection_error = int(not (
        record["episodes"] == expected["episodes"]
        and record["decisions"] == expected["decisions"]
        and record["acquisitions"] == expected["acquisitions"]
        and record["terminal_sufficient"] == expected["final_sufficient"]
        and record["channel_counts"] == expected["channel_counts"]
        and record["channel_switches"] == expected["channel_switches"]
    ))
    record["projection_error"] = projection_error
    if projection_error:
        record["failed"] += 1
    return record


def gate(records, totals):
    return (
        len(records) == 9
        and totals.get("episodes") == 85824
        and totals.get("decisions") == 214948
        and totals.get("acquisitions") == 129124
        and totals.get("terminal_sufficient") == 85824
        and totals.get("verified_derived") == 85824
        and totals.get("opposite_rejected") == 85824
        and totals.get("verifier_calls") == 171648
        and totals.get("channel_counts")
            == {"RETRIEVE":88918,"OBSERVE":21252,"ASK_USER":18954}
        and totals.get("channel_switches") == 32564
        and totals.get("support_min",0) >= 1
        and totals.get("support_max",5) <= 4
        and totals.get("checked_steps",0) >= 85824
        and totals.get("checked_steps",0) <= 85824 * MAX_STEPS
        and totals.get("failures") == 0
        and totals.get("projection_errors") == 0
        and all(
            r.get("failed") == 0
            and r.get("projection_error") == 0
            and r.get("terminal_sufficient") == 9536
            and r.get("verified_derived") == 9536
            and r.get("opposite_rejected") == 9536
            and r.get("verifier_calls") == 19072
            and r.get("support_min",0) >= 1
            and r.get("support_max",5) <= 4
            for r in records
        )
    )


def _historical_input_hash(c199, rel):
    suffix = rel.replace("\\","/").lower()
    matches = [
        value for key,value in c199["input_sha256"].items()
        if str(key).replace("\\","/").lower().endswith("/" + suffix)
    ]
    require(len(matches) == 1, "Historical C171 input identity drift:" + rel)
    return matches[0]


def precheck(
    c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,
    c199_summary,c174_summary,c181_summary,c188_summary,root
):
    root = Path(root)
    p204,c199,prediction_path,c174_result,pilot_path,p181,p188,pins,protected = c205.precheck(
        c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,
        c199_summary,c174_summary,c181_summary,c188_summary,root
    )
    require(audit.sha(c205_summary) == PARENT_C205_SHA, "C205 summary changed")
    p205 = audit.read_json(c205_summary)
    c205.validate_result(p205)
    require(
        p205.get("commit_sha") == PARENT_C205_EXECUTION
        and p205.get("status") == "PASS"
        and c205.gate(
            p205["canonical_unique"],p205["expanded_direct"],
            p205["c204_max_match"],p205["workload"]
        )
        and p205.get("source_blobs") == pins,
        "Wrong accepted C205 parent",
    )
    protected[str(Path(c205_summary).resolve())] = PARENT_C205_SHA
    for artifact in p205["artifacts"]:
        path = audit.safe_child(Path(c205_summary).resolve().parent,artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C205 artifact:" + artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]

    pins = dict(pins)
    for rel in C171_FILES:
        path = root / rel
        wanted = _historical_input_hash(c199,rel)
        require(path.is_file() and audit.sha(path) == wanted,
                "Changed accepted C171 input:" + rel)
        protected[str(path.resolve())] = wanted
        pins[rel] = audit.git(root,"rev-parse","HEAD:"+rel).decode().strip()

    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    pins.update({name:allpins[name] for name in OWN})

    require(len(pins) == 56 and len(protected) == 110,
            "C206 source/protection count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C206 manifest drift")
    return p205,c199,prediction_path,c174_result,pilot_path,pins,protected


def regression_modules(root):
    names = c205.regression_modules(root)
    require(len(names) == len(set(names)) == 90, "Historical regression module drift")
    return names + ["tests_lm.test_v05_c206_terminal_derived_result_integration"]


def regression_suite(root):
    names = regression_modules(root)
    loaded = unittest.defaultTestLoader.loadTestsFromNames(names)
    tests = list(c205._iter_tests(loaded))
    ids = [test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded) == 1, "Historical dynamic test identity drift:" + excluded)
    kept = [
        test for test in tests
        if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
    ]
    require(
        len(tests) == 1902
        and len(kept) == 1901
        and not any(
            test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
            for test in kept
        ),
        "C206 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C206",
    )
    require(
        len(payload["source_blobs"]) == 56
        and len(payload["input_sha256"]) == 110
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C206 coverage drift",
    )
    require(
        payload["training_steps"] == 0
        and payload["fresh_seed_count"] == 0
        and payload["learned_forward_calls"] == 0
        and payload["network_calls"] == 0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False,
        "C206 scope drift",
    )
    require(
        payload["status"] == (
            "PASS" if gate(payload["block_records"],payload["summary"]) else "FAIL"
        ),
        "C206 gate drift",
    )


def run(
    *,c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,
    c199_summary,c174_summary,c181_summary,c188_summary,output_dir,expected_head
):
    root = Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip() == expected_head,
                "HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()
                == "feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    p205,c199,prediction_path,_,_,pins,protected = precheck(
        c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,
        c199_summary,c174_summary,c181_summary,c188_summary,root
    )
    predictions = c201.load_c199_predictions(prediction_path)
    _,_,features = c203.load_c174_features(Path(c174_summary))
    source_rows = predictions["row_indices"].astype(np.int64)
    world_codes = predictions["world_codes"].astype(np.int64)
    require(source_rows.shape == world_codes.shape == (9536,),
            "Accepted episode identity drift")
    raw12 = torch.from_numpy(features[source_rows].copy())
    raw13 = c193.budget13(raw12)
    expected_projection = c203.expected_projection(predictions)
    provider_map,endpoint_map = c202.providers()

    out = Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    artifacts = []
    started = time.perf_counter()

    def record(name):
        path = out / name
        artifacts.append(dict(
            file=name,sha256=audit.sha(path),serialized_bytes=path.stat().st_size
        ))

    def save(name,value):
        (out/name).write_bytes(blob(value))
        record(name)

    save("derived-integration-plan.json",dict(manifest(),source_blobs=pins))
    try:
        records = []
        for block in range(9):
            views = c190.make_views(
                raw13,source_rows,world_codes,f"C206-derived-b{block}"
            )
            rec = replay_and_verify_block(
                views,world_codes,
                predictions["necessity_predictions"][0,block],
                predictions["target_predictions"][0,block],
                provider_map,endpoint_map,
                expected_projection["blocks"][block],
            )
            rec["block"] = block
            records.append(rec)
            print(
                f"[C206] block={block+1}/9 verified={rec['verified_derived']} "
                f"opposite_rejected={rec['opposite_rejected']} failed={rec['failed']}",
                flush=True,
            )

        totals = dict(
            episodes=sum(r["episodes"] for r in records),
            decisions=sum(r["decisions"] for r in records),
            acquisitions=sum(r["acquisitions"] for r in records),
            terminal_sufficient=sum(r["terminal_sufficient"] for r in records),
            verified_derived=sum(r["verified_derived"] for r in records),
            opposite_rejected=sum(r["opposite_rejected"] for r in records),
            verifier_calls=sum(r["verifier_calls"] for r in records),
            channel_counts={
                channel:sum(r["channel_counts"][channel] for r in records)
                for channel in v2.CHANNELS
            },
            channel_switches=sum(r["channel_switches"] for r in records),
            support_total=sum(r["support_total"] for r in records),
            support_min=min(r["support_min"] for r in records),
            support_max=max(r["support_max"] for r in records),
            checked_steps=sum(r["checked_steps"] for r in records),
            failures=sum(r["failed"] for r in records),
            projection_errors=sum(r["projection_error"] for r in records),
        )
        for key in COUNTERS[1:]:
            totals[key + ("s" if not key.endswith("s") else "")] = sum(
                r[key] for r in records
            )

        save("block-results.json",records)
        save("verification-totals.json",totals)
        save("support-profile.json",dict(
            support_min=totals["support_min"],
            support_max=totals["support_max"],
            support_total=totals["support_total"],
            checked_steps=totals["checked_steps"],
        ))
        save("negative-controls.json",dict(
            opposite_controls=85824,
            opposite_rejected=totals["opposite_rejected"],
            opposite_rejection_errors=totals["opposite_rejection_errors"],
        ))

        guard()
        precheck(
            c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,
            c199_summary,c174_summary,c181_summary,c188_summary,root
        )
        for path,wanted in protected.items():
            require(audit.sha(path) == wanted,"Protected input changed:" + path)
        for artifact in artifacts:
            require(
                audit.sha(out/artifact["file"]) == artifact["sha256"],
                "Output changed:" + artifact["file"],
            )

        result = dict(
            experiment_id=EXPERIMENT_ID,
            stage=STAGE,
            commit_sha=expected_head,
            status="PASS" if gate(records,totals) else "FAIL",
            diagnostic_execution_valid=True,
            C205_summary_sha256=PARENT_C205_SHA,
            source_blobs=pins,
            input_sha256=protected,
            artifacts=artifacts,
            block_records=records,
            summary=totals,
            training_steps=0,
            fresh_seed_count=0,
            learned_forward_calls=0,
            network_calls=0,
            production_runtime_modified=False,
            gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=[
                "C171 proof_fixture is benchmark-only reference candidate generation",
                "not learned proof generation or natural-language answer generation",
                "accepted saved learned decisions replayed; no new learned forward",
                "fixture providers, not real sensor/user transport",
                "development prerequisite, not final Gate E",
            ],
        )
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C206] terminal derived-result integration collected",flush=True)
        print("=== C206 RESULT ===",flush=True)
        print(blob(result).decode(),flush=True)
        return result
    except Exception as exc:
        (out/"invalid.json").write_bytes(blob(dict(
            experiment_id=EXPERIMENT_ID,
            status="INVALID",
            diagnostic_execution_valid=False,
            error=str(exc),
        )))
        raise


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in (
        "c205-summary","c204-summary","c203-summary","c202-summary","c201-summary",
        "c200-summary","c199-summary","c174-summary","c181-summary","c188-summary",
        "output-dir",
    ):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
