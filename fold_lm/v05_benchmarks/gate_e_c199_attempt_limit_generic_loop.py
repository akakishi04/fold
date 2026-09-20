"""C199: ATTEMPT_LIMIT containment in the accepted generic learned acquisition loop.

Hold C198/C197/C196 orchestration, budget13, frozen C181/C188 models, cohort and coherent
sources fixed. Change only trusted AcquisitionOwner max_dispatches from3 to1 in the
intervention arm. The first acquisition must publish normally. If the accepted learned policy
still needs a second observation, the second reservation may be created but dispatch must
terminate DENIED/ATTEMPT_LIMIT without a second provider call or publication.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np
import torch

EXPERIMENT_ID = "C199-v5e-attempt-limit-generic-loop"
STAGE = "V5-E-ATTEMPT-LIMIT-GENERIC-LOOP"
BASE = "073bc6b549b6b34c6b585e4759e822bbd8ed0400"
PARENT_EXECUTION = "e5a09864497fa38a9eac8d400b5162e33e99ec0d"
PARENT_SHA = "9cbb99e6ad200c5a9b88438abf140c58dd293661d8765f3460e3d2a7c70a8e75"
REFERENCE_EXECUTION = PARENT_EXECUTION
REFERENCE_SHA = PARENT_SHA
BASE_SEEDS = (181001, 181002, 181003)
HEAD_SEEDS = (188001, 188002, 188003)
ARM = "INTERNAL_SEMANTICS"
ARMS = ("ALLOWED", "DISPATCH_LIMIT_ONE")
BATCH = 1024
ATOL = 1e-6
MAX_ACQUISITIONS = 3
MAX_DECISIONS = 4
PRIOR_NAMES = (
    "c198", "c197", "c196", "c195", "c194", "c193", "c192", "c191", "c190",
    "c189", "c188", "c187", "c186", "c185", "c184", "c183", "c182", "c181",
    "c180", "c179", "c178", "c177", "c176", "c174",
)
OWN = (
    "fold_lm/v05_benchmarks/gate_e_c199_attempt_limit_generic_loop.py",
    "tests_lm/test_v05_c199_attempt_limit_generic_loop.py",
    "tools/run_c199.ps1",
    "tools/invoke_c199.ps1",
    "docs/experiment-ledger-addendum-c199-preregistration.md",
)
EXPECTED_TESTS = 1701
OUTPUTS = {
    "attempt-limit-plan.json",
    "allowed-replay.json",
    "episode-results.json",
    "episode-traces.jsonl.gz",
    "episode-predictions.npz",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def load_c198_predictions(path):
    p = Path(path)
    require(p.is_file() and p.stat().st_size < 20_000_000,
            "Unexpected C198 prediction artifact size")
    with np.load(p, allow_pickle=False) as z:
        expected = {
            "necessity_predictions", "necessity_logits", "target_predictions", "target_logits",
            "row_indices", "local_rows", "world_codes",
        }
        require(set(z.files) == expected, "C198 prediction schema drift")
        out = {k: z[k].copy() for k in z.files}
    require(
        out["necessity_predictions"].shape == (2, 9, 9536, 4)
        and out["necessity_logits"].shape == (2, 9, 9536, 4, 2)
        and out["target_predictions"].shape == (2, 9, 9536, 3)
        and out["target_logits"].shape == (2, 9, 9536, 3, 4)
        and out["row_indices"].shape == (9536,)
        and out["local_rows"].shape == (9536,)
        and out["world_codes"].shape == (9536,),
        "C198 prediction array drift",
    )
    return out


def admitted(acq):
    from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as c196
    return c196.admitted(acq)


def acquire(owner, target_index):
    from fold_lm.v05 import structured_action_runtime as action

    require(type(target_index) is int and 0 <= target_index < 4, "Local target required")
    view = owner.state.view
    require(view.facts[target_index].status == "UNOBSERVED",
            "Target must currently be unobserved")
    fid = view.facts[target_index].fact_id
    transition = owner.apply(action.propose(owner.state, "RETRIEVE", fact_index=target_index))
    dispatched = None
    if transition.result.status == "PENDING":
        dispatched = owner.dispatch(transition.result.intent.intent_id)
    return dict(
        input_index=target_index,
        fact_id=fid,
        action=asdict(transition.result),
        dispatch=asdict(dispatched) if dispatched else None,
    )


def run_loop_limit(views, world_codes, endpoints, base, selector, initial, arm):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05 import structured_action_runtime as action
    from fold_lm.v05 import structured_task_input as task
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189

    require(arm in ARMS, "Unregistered C199 arm")
    require(len(views) == len(world_codes) > 0, "Episode/world alignment required")
    dispatch_limit = MAX_ACQUISITIONS if arm == "ALLOWED" else 1
    owners = [
        life.AcquisitionOwner(
            action.RuntimeState(v),
            {"RETRIEVE": endpoints[int(code)]},
            max_dispatches=dispatch_limit,
        )
        for v, code in zip(views, world_codes, strict=True)
    ]
    n = len(views)
    records = [
        dict(
            initial=asdict(task.encode(v)),
            phases=[],
            acquisitions=[],
            decision_charges=0,
            status="UNRESOLVED",
            world_code=int(code),
            arm=arm,
        )
        for v, code in zip(views, world_codes, strict=True)
    ]
    n_pred = np.full((n, MAX_DECISIONS), -1, dtype=np.int8)
    n_logits = np.zeros((n, MAX_DECISIONS, 2), dtype=np.float32)
    t_pred = np.full((n, MAX_ACQUISITIONS), -1, dtype=np.int8)
    t_logits = np.full((n, MAX_ACQUISITIONS, 4), -np.inf, dtype=np.float32)
    meter = dict(rows=0, forward_calls=0, cell_calls=0)

    active = list(range(n))
    iteration = 0
    while active:
        require(iteration < MAX_DECISIONS, "Attempt-limit loop exceeded decision bound")
        charged, exhausted = [], []
        for i in active:
            if driver.charge_decision(owners[i]):
                charged.append(i)
            else:
                exhausted.append(i)
        for i in exhausted:
            records[i]["status"] = "BUDGET_EXHAUSTED"
        active = charged
        if not active:
            break

        raw, packets = c189.encode_views([owners[i].state.view for i in active])
        any_missing = any(
            any(f.status == "UNOBSERVED" for f in owners[i].state.view.facts)
            for i in active
        )
        if iteration == 0:
            require(torch.equal(raw, initial["raw"]), "Initial cache mapping drift")
            p = np.asarray(initial["necessity_predictions"])
            z = np.asarray(initial["necessity_logits"])
            if any_missing:
                t = np.asarray(initial["target_predictions"])
                tz = np.asarray(initial["target_logits"])
            else:
                t = np.full(len(active), -1, dtype=np.int8)
                tz = np.full((len(active), 4), -np.inf, dtype=np.float32)
        elif any_missing:
            p, t, z, tz, m = c189.combined_predict(base, selector, raw, batch=BATCH)
            for k in meter:
                meter[k] += m[k]
        else:
            p, z, m = c189.necessity_predict(base, raw, batch=BATCH)
            for k in meter:
                meter[k] += m[k]
            t = np.full(len(active), -1, dtype=np.int8)
            tz = np.full((len(active), 4), -np.inf, dtype=np.float32)

        next_active = []
        for j, i in enumerate(active):
            n_pred[i, iteration] = p[j]
            n_logits[i, iteration] = z[j]
            phase = dict(
                iteration=iteration,
                packet=asdict(packets[j]),
                necessity_prediction=int(p[j]),
            )
            records[i]["decision_charges"] += 1
            if any_missing:
                require(iteration < MAX_ACQUISITIONS,
                        "Target-bearing decision exceeded acquisition-derived bound")
                t_pred[i, iteration] = t[j]
                t_logits[i, iteration] = tz[j]
                phase["target_prediction"] = int(t[j])
            records[i]["phases"].append(phase)

            if int(p[j]) == 0:
                records[i]["status"] = "SUFFICIENT_CLASSIFICATION"
                continue

            view = owners[i].state.view
            if not any(f.status == "UNOBSERVED" for f in view.facts):
                records[i]["status"] = "UNRESOLVED_NEEDS_NO_TARGET"
                continue
            target_index = int(t[j])
            if not (0 <= target_index < 4) or view.facts[target_index].status != "UNOBSERVED":
                records[i]["status"] = "UNRESOLVED_INVALID_TARGET"
                continue

            acq = acquire(owners[i], target_index)
            records[i]["acquisitions"].append(acq)
            if admitted(acq):
                next_active.append(i)
            else:
                action_result = acq.get("action") if isinstance(acq, dict) else None
                dispatch = acq.get("dispatch") if isinstance(acq, dict) else None
                reason = (
                    dispatch.get("reason") if isinstance(dispatch, dict)
                    else action_result.get("reason") if isinstance(action_result, dict)
                    else "UNKNOWN"
                )
                records[i]["status"] = "UNRESOLVED_ACQUISITION_" + str(reason)

        active = next_active
        iteration += 1

    for i, owner in enumerate(owners):
        records[i]["final"] = asdict(task.encode(owner.state.view))
        records[i]["receipts"] = [asdict(r) for r in owner.receipts]
        records[i]["pending"] = asdict(owner.state.pending) if owner.state.pending else None
        records[i]["runtime_terminal"] = owner.state.terminal
    return records, dict(
        necessity_predictions=n_pred,
        necessity_logits=n_logits,
        target_predictions=t_pred,
        target_logits=t_logits,
    ), meter


LIMIT_COUNTERS = (
    "failed",
    "prefix_prediction_error",
    "attempt_limit_contract_error",
    "status_error",
    "provider_work_error",
    "publication_error",
    "receipt_error",
    "third_decision_error",
    "resource_error",
    "fact_state_error",
    "fake_sufficient_error",
)


def score_limit(record, ref_n0, ref_t0, ref_n1, ref_t1, initial_features):
    phases = record["phases"]
    acquisitions = record["acquisitions"]
    final = np.asarray(record["final"]["features"], dtype=np.int64)
    initial = np.asarray(initial_features, dtype=np.int64)
    expected_limit = int(ref_n1) == 1

    prefix_prediction_error = int(not (
        len(phases) == 2
        and phases[0]["necessity_prediction"] == int(ref_n0)
        and phases[0].get("target_prediction") == int(ref_t0)
        and phases[1]["necessity_prediction"] == int(ref_n1)
        and phases[1].get("target_prediction") == int(ref_t1)
    ))

    first = acquisitions[0] if len(acquisitions) >= 1 else None
    first_action = first["action"] if isinstance(first, dict) else None
    first_dispatch = first["dispatch"] if isinstance(first, dict) else None
    first_ok = bool(
        isinstance(first_action, dict)
        and isinstance(first_dispatch, dict)
        and first_action["status"] == "PENDING"
        and first_action["reason"] == "ACQUISITION_RESERVED"
        and first_dispatch["status"] == "PUBLISHED"
        and first_dispatch["reason"] == "OBSERVATION_ADMITTED"
        and first_dispatch["provider_calls"] == 1
        and first_dispatch["fact_publications"] == 1
    )

    if expected_limit:
        second = acquisitions[1] if len(acquisitions) == 2 else None
        second_action = second["action"] if isinstance(second, dict) else None
        second_dispatch = second["dispatch"] if isinstance(second, dict) else None
        second_ok = bool(
            isinstance(second_action, dict)
            and isinstance(second_dispatch, dict)
            and second_action["status"] == "PENDING"
            and second_action["reason"] == "ACQUISITION_RESERVED"
            and second_action["acquisition_reserved"] == 1
            and second_dispatch["status"] == "DENIED"
            and second_dispatch["reason"] == "ATTEMPT_LIMIT"
            and second_dispatch["provider_calls"] == 0
            and second_dispatch["fact_publications"] == 0
            and second_dispatch["evidence"] is None
        )
        attempt_limit_contract_error = int(not (first_ok and second_ok))
        status_error = int(
            record["status"] != "UNRESOLVED_ACQUISITION_ATTEMPT_LIMIT"
        )
        provider_work_error = int(
            not first_dispatch
            or first_dispatch.get("provider_calls") != 1
            or not second_dispatch
            or second_dispatch.get("provider_calls") != 0
        )
        publication_error = int(
            first_dispatch.get("fact_publications") != 1
            or second_dispatch.get("fact_publications") != 0
        ) if first_dispatch and second_dispatch else 1
        receipt_error = int(len(record["receipts"]) != 1)
        resource_error = int(not (
            final[62] == 6
            and final[63] == 2
            and final[64] == 1
            and final[67] == 1
            and final[70] == 5
            and final[71] == 14
            and record["pending"] is None
            and record["runtime_terminal"] is None
        ))
    else:
        attempt_limit_contract_error = int(not (first_ok and len(acquisitions) == 1))
        status_error = int(record["status"] != "SUFFICIENT_CLASSIFICATION")
        provider_work_error = int(
            not first_dispatch or first_dispatch.get("provider_calls") != 1
        )
        publication_error = int(
            not first_dispatch or first_dispatch.get("fact_publications") != 1
        )
        receipt_error = int(len(record["receipts"]) != 1)
        resource_error = int(not (
            final[62] == 8
            and final[63] == 3
            and final[64] == 1
            and final[67] == 1
            and final[70] == 0
            and final[71] == 12
            and record["pending"] is None
            and record["runtime_terminal"] is None
        ))

    third_decision_error = int(
        len(phases) != 2 or record["decision_charges"] != 2
    )

    initial_observed = int(sum(
        initial[48 + 4 * i] == 1 for i in range(4)
    ))
    final_observed = int(sum(
        final[48 + 4 * i] == 1 for i in range(4)
    ))
    fact_state_error = int(final_observed != initial_observed + 1)

    fake_sufficient_error = int(
        expected_limit and record["status"] == "SUFFICIENT_CLASSIFICATION"
    )

    values = (
        prefix_prediction_error,
        attempt_limit_contract_error,
        status_error,
        provider_work_error,
        publication_error,
        receipt_error,
        third_decision_error,
        resource_error,
        fact_state_error,
        fake_sufficient_error,
    )
    return dict(
        failed=int(any(values)),
        expected_limit=int(expected_limit),
        prefix_prediction_error=prefix_prediction_error,
        attempt_limit_contract_error=attempt_limit_contract_error,
        status_error=status_error,
        provider_work_error=provider_work_error,
        publication_error=publication_error,
        receipt_error=receipt_error,
        third_decision_error=third_decision_error,
        resource_error=resource_error,
        fact_state_error=fact_state_error,
        fake_sufficient_error=fake_sufficient_error,
    )


def expected_order():
    return [(b, h) for b in BASE_SEEDS for h in HEAD_SEEDS]


def prefix_replay(arrays, reference):
    nerr = int((arrays["necessity_predictions"][:, :2]
                != reference["necessity_predictions"][:, :2]).sum())
    terr = int((arrays["target_predictions"][:, :2]
                != reference["target_predictions"][:, :2]).sum())
    nref = reference["necessity_logits"][:, :2]
    nd = float(np.max(np.abs(arrays["necessity_logits"][:, :2] - nref)))
    tref = reference["target_logits"][:, :2]
    finite = np.isfinite(tref)
    td = float(np.max(np.abs(
        arrays["target_logits"][:, :2][finite] - tref[finite]
    ))) if finite.any() else 0.0
    no_third = int(
        np.any(arrays["necessity_predictions"][:, 2:] != -1)
        or np.any(arrays["target_predictions"][:, 2:] != -1)
    )
    return dict(
        necessity_prediction_errors=nerr,
        target_prediction_errors=terr,
        necessity_max_abs_logit_difference=nd,
        target_max_abs_logit_difference=td,
        unauthorized_third_prediction=int(no_third),
    )


def gate(allowed, limit):
    from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as c196

    if [(r.get("base_seed"), r.get("head_seed")) for r in allowed] != expected_order():
        return False
    if [(r.get("base_seed"), r.get("head_seed")) for r in limit] != expected_order():
        return False
    for r in allowed:
        if r.get("episodes") != 9536:
            return False
        if any(r.get(k) != 0 for k in c196.ALLOWED_COUNTERS):
            return False
        if r.get("first_reads") != 9536 or r.get("third_reads") != r.get("final_decision_rows"):
            return False
        if r.get("actual_reads") != r["first_reads"] + r["second_reads"] + r["third_reads"]:
            return False
        if r.get("reference_necessity_prediction_errors") != 0:
            return False
        if r.get("reference_target_prediction_errors") != 0:
            return False
        if r.get("reference_necessity_max_abs_logit_difference", 1) > ATOL:
            return False
        if r.get("reference_target_max_abs_logit_difference", 1) > ATOL:
            return False
    for r in limit:
        if r.get("episodes") != 9536:
            return False
        if any(type(r.get(k)) is not int or r[k] < 0 for k in LIMIT_COUNTERS):
            return False
        if any(r[k] != 0 for k in LIMIT_COUNTERS):
            return False
        if r.get("first_reads") != 9536 or r.get("provider_calls") != 9536:
            return False
        if r.get("publications") != 9536 or r.get("receipts") != 9536:
            return False
        if r.get("learned_decisions") != 19072:
            return False
        if r.get("attempt_limit_rows") != r.get("reference_second_reads"):
            return False
        if r.get("sufficient_after_first") + r.get("attempt_limit_rows") != 9536:
            return False
        if r.get("second_provider_calls") != 0 or r.get("second_publications") != 0:
            return False
        if r.get("unauthorized_third_prediction") != 0:
            return False
        if r.get("prefix_necessity_prediction_errors") != 0:
            return False
        if r.get("prefix_target_prediction_errors") != 0:
            return False
        if r.get("prefix_necessity_logit_delta", 1) > ATOL:
            return False
        if r.get("prefix_target_logit_delta", 1) > ATOL:
            return False
    return True


def manifest():
    return dict(
        experiment_id=EXPERIMENT_ID,
        stage=STAGE,
        parent_sha256=PARENT_SHA,
        acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,
        reference_execution=REFERENCE_EXECUTION,
        reference_sha256=REFERENCE_SHA,
        base_seeds=BASE_SEEDS,
        head_seeds=HEAD_SEEDS,
        arms=ARMS,
        arm=ARM,
        question="with accepted learned models and generic loop semantics held fixed, does changing only AcquisitionOwner max_dispatches from3 to1 safely stop a required second acquisition as ATTEMPT_LIMIT after one admitted observation",
        changed="intervention arm constructs the trusted AcquisitionOwner with max_dispatches1 instead of3; model inputs, budget13, source bindings, provider implementation and orchestration rules are otherwise fixed",
        held="budget13,C174 cohort,9 frozen C181/C188 pairs,16 coherent source bindings,C172/C173,C197 reason propagation,C196 result-aware continuation,teachers,raw argmax",
        allowed_arm="full9536 worlds/selector; exact accepted C198/C197 allowed replay required",
        limit_arm="first acquisition admitted normally for every episode; every accepted-reference second acquisition request reserves locally then dispatches DENIED/ATTEMPT_LIMIT with zero second provider call/publication; rows sufficient after first observation stop normally",
        limit_resources="ATTEMPT_LIMIT rows end internal6,acquisitions2,available1,permitted1,last_outcome ATTEMPT_LIMIT,step14,pending none; one admitted fact/receipt only",
        episodes_per_arm=85824,
        blocks_per_arm=9,
        gate="all9 allowed blocks exact reference replay and zero scientific errors; all9 limit blocks exact accepted second-request counts,9536 first provider reads/publications/receipts,zero second provider work,no third learned decision,and exact per-row terminal/resource contract",
        training=0,
        fresh_seeds=0,
        network_calls=0,
        answer_generation=0,
        proof_checker_calls=0,
        core_evidence_writes=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        outputs=sorted(OUTPUTS),
        limits="development family;dispatch limit intervention is trusted runtime configuration;no retry/resource-policy/tool-choice/holdout/language/answer/proof/GateE",
    )


MANIFEST_SHA = "3bda32133c97539c4e327899e08859e57df9361caa50657e22000374e65bacec"


def precheck(c198_summary, *args):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c198_stale_reservation_generic_loop as parent

    require(len(args) == 24, "Twenty-three prior summaries and repository root required")
    root = args[-1]
    (
        p197, p196, p195, p194, p193, p192, p191, p190, p189, p188, p181, p174,
        pins, protected,
    ) = parent.precheck(args[0], *args[1:])
    require(audit.sha(c198_summary) == PARENT_SHA, "C198 summary changed")
    p198 = audit.read_json(c198_summary)
    parent.validate_result(p198)
    require(
        p198["commit_sha"] == PARENT_EXECUTION
        and p198["status"] == "PASS"
        and parent.gate(p198["allowed_records"], p198["stale_records"])
        and p198["source_blobs"] == pins,
        "Wrong accepted C198 source/result",
    )

    protected[str(Path(c198_summary).resolve())] = PARENT_SHA
    for artifact in p198["artifacts"]:
        f = audit.safe_child(Path(c198_summary).resolve().parent, artifact["file"])
        require(
            f.is_file()
            and f.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(f) == artifact["sha256"],
            "Changed C198 artifact:" + artifact["file"],
        )
        protected[str(f.resolve())] = artifact["sha256"]

    pins = dict(pins)
    for name in parent.OWN:
        pins[name] = audit.git(
            root, "rev-parse", PARENT_EXECUTION + ":" + name
        ).decode().strip()
    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
    protected.update(audit.protect_tree_files(root, allpins))
    require(len(pins) == 156 and len(protected) == 407,
            "Source/protected union drift")
    require(digest(manifest()) == MANIFEST_SHA, "Manifest drift")
    return (
        p198, p197, p196, p195, p194, p193, p192, p191, p190, p189, p188,
        p181, p174, pins, protected,
    )


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c198_stale_reservation_generic_loop as parent

    names = parent.regression_modules(root)
    require(len(names) == len(set(names)) == 83, "Historical regression list drift")
    return names + ["tests_lm.test_v05_c199_attempt_limit_generic_loop"]


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C199",
    )
    require(
        payload["episodes_per_arm"] == 85824
        and len(payload["allowed_records"]) == len(payload["limit_records"]) == 9
        and len(payload["source_blobs"]) == 156
        and len(payload["input_sha256"]) == 407
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "Workload/coverage drift",
    )
    require(
        all(payload[k] == 0 for k in (
            "new_training", "fresh_seeds", "network_calls", "answer_generation",
            "proof_checker_calls", "core_evidence_writes",
        ))
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False,
        "Scope drift",
    )
    require(
        payload["status"] == (
            "PASS" if gate(payload["allowed_records"], payload["limit_records"]) else "FAIL"
        ),
        "Gate drift",
    )


def run(*, output_dir, expected_head, **parents):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c182_frozen_fact_renaming as frozen
    from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as target
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
    from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
    from fold_lm.v05_benchmarks import gate_e_c193_budget13_authoritative_closure as c193
    from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as c196

    root = Path(__file__).resolve().parents[2]
    args = tuple(parents[n + "_summary"] for n in PRIOR_NAMES[1:]) + (root,)

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
    (
        p198, p197, p196, p195, p194, p193, p192, p191, p190, p189, p188,
        p181, p174, pins, protected,
    ) = precheck(parents["c198_summary"], *args)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    artifacts = []
    allowed_records = []
    limit_records = []
    started = time.perf_counter()

    def record_file(name):
        f = out / name
        artifacts.append(
            dict(file=name, sha256=audit.sha(f), serialized_bytes=f.stat().st_size)
        )

    def save(name, value):
        (out / name).write_bytes(blob(value))
        record_file(name)

    save("attempt-limit-plan.json", dict(manifest(), source_blobs=pins))

    try:
        print(
            "[C199] plan fixed; accepted C198/C197 loop; ALLOWED replay + dispatch limit one",
            flush=True,
        )
        torch.set_num_threads(2)
        torch.use_deterministic_algorithms(True)

        data, metadata = audit.load_data(Path(parents["c174_summary"]).resolve().parent, p174)
        raw_all = torch.from_numpy(data["features"].copy())
        valid = c189.target_teacher(data["features"], data["template_ids"], metadata)
        _, _, evfull, _, _ = target.cohort_masks(
            raw_all, data["labels"], data["split_codes"], valid
        )
        full_ix = np.flatnonzero(evfull)
        raw12 = torch.from_numpy(data["features"][evfull].copy())
        raw13 = c193.budget13(raw12)
        expanded12, source_rows, local_rows, world_codes = c190.expand_worlds(raw12, full_ix)
        expanded13 = c193.budget13(expanded12)
        tids = data["template_ids"][evfull]

        c198_dir = Path(parents["c198_summary"]).resolve().parent
        saved = load_c198_predictions(c198_dir / "episode-predictions.npz")
        require(
            np.array_equal(saved["row_indices"], source_rows)
            and np.array_equal(saved["local_rows"], local_rows)
            and np.array_equal(saved["world_codes"], world_codes),
            "C198 episode identity drift",
        )

        c181_dir = Path(parents["c181_summary"]).resolve().parent
        c188_dir = Path(parents["c188_summary"]).resolve().parent
        fits = {f["seed"]: f for f in p181["fit_records"] if f["arm"] == ARM}
        selector_sha = {
            (r["base_seed"], r["head_seed"]): r["head_sha256"]
            for r in p188["selector_results"]
        }
        bases = {}
        heads = {}
        for b in BASE_SEEDS:
            bases[b] = frozen.restore_bare(
                c181_dir / f"probe-{b}-{ARM}.pt",
                b, ARM, fits[b]["final_sha256"],
            )
            for h in HEAD_SEEDS:
                heads[b, h] = c189.restore_selector(
                    c188_dir / f"selector-{b}-{h}.pt",
                    b, h, selector_sha[b, h],
                )

        source_dir = Path(parents["c191_summary"]).resolve().parent / "sources"
        real_providers = {}
        real_endpoints = {}
        for code in range(16):
            f = source_dir / f"world-{code:02d}.json"
            expected = c190.SOURCE_FILES[f"sources/world-{code:02d}.json"]
            require(
                f.is_file() and audit.sha(f) == expected,
                "Changed protected coherent world source",
            )
            binding = life.SourceBinding(f"C190-world-{code:02d}", expected)
            provider = life.FileSnapshotProvider(f, binding)
            real_providers[code] = provider
            real_endpoints[code] = life.Endpoint(binding, provider)

        dense_n = np.full((2, 9, 9536, 4), -1, dtype=np.int8)
        dense_z = np.zeros((2, 9, 9536, 4, 2), dtype=np.float32)
        dense_t = np.full((2, 9, 9536, 3), -1, dtype=np.int8)
        dense_tz = np.full((2, 9, 9536, 3, 4), -np.inf, dtype=np.float32)
        allowed_replay = []

        with gzip.open(
            out / "episode-traces.jsonl.gz",
            "wt", encoding="utf-8", newline="\n",
        ) as trace:
            for bi, b in enumerate(BASE_SEEDS):
                for hi, h in enumerate(HEAD_SEEDS):
                    idx = bi * 3 + hi
                    cache, _ = c193.initial_policy_cache(
                        raw13, full_ix, bases[b], heads[b, h]
                    )
                    lt = torch.from_numpy(local_rows.astype(np.int64))
                    initial = dict(
                        raw=cache["raw"][lt],
                        necessity_predictions=cache["necessity_predictions"][local_rows],
                        target_predictions=cache["target_predictions"][local_rows],
                        necessity_logits=cache["necessity_logits"][local_rows],
                        target_logits=cache["target_logits"][local_rows],
                    )
                    reference = dict(
                        necessity_predictions=saved["necessity_predictions"][0, idx],
                        necessity_logits=saved["necessity_logits"][0, idx],
                        target_predictions=saved["target_predictions"][0, idx],
                        target_logits=saved["target_logits"][0, idx],
                    )

                    for arm_i, arm in enumerate(ARMS):
                        views = c190.make_views(
                            expanded13, source_rows, world_codes,
                            f"C199-{arm}-b{b}-h{h}",
                        )
                        before_reads = sum(p.reads for p in real_providers.values())
                        before_bytes = sum(p.bytes_read for p in real_providers.values())
                        observed, arrays, _ = run_loop_limit(
                            views, world_codes, real_endpoints,
                            bases[b], heads[b, h], initial, arm,
                        )
                        reads = sum(p.reads for p in real_providers.values()) - before_reads
                        bytes_read = (
                            sum(p.bytes_read for p in real_providers.values()) - before_bytes
                        )

                        dense_n[arm_i, idx] = arrays["necessity_predictions"]
                        dense_z[arm_i, idx] = arrays["necessity_logits"]
                        dense_t[arm_i, idx] = arrays["target_predictions"]
                        dense_tz[arm_i, idx] = arrays["target_logits"]

                        if arm == "ALLOWED":
                            replay = c196.replay_metrics(arrays, reference)
                            allowed_replay.append(dict(base_seed=b, head_seed=h, **replay))
                            replay_error = int(
                                replay["necessity_prediction_errors"] != 0
                                or replay["target_prediction_errors"] != 0
                                or replay["necessity_max_abs_logit_difference"] > ATOL
                                or replay["target_max_abs_logit_difference"] > ATOL
                            )
                            scores = []
                            for j, rec in enumerate(observed):
                                q = c193.assess(
                                    rec,
                                    int(tids[int(local_rows[j])]),
                                    metadata,
                                    c190.WORLD_BITS[int(world_codes[j])],
                                )
                                q["reference_replay_error"] = replay_error
                                q["reference_block_mismatch"] = 0
                                q["failed"] = int(q["failed"] or replay_error)
                                scores.append(q)
                            totals = {k: sum(x[k] for x in scores) for k in c193.COUNTERS}
                            ref_rec = p198["allowed_records"][idx]
                            block_mismatch = int(any((
                                totals["first_reads"] != ref_rec["first_reads"],
                                totals["second_reads"] != ref_rec["second_reads"],
                                totals["third_reads"] != ref_rec["third_reads"],
                                totals["final_decision_rows"] != ref_rec["final_decision_rows"],
                                reads != ref_rec["actual_reads"],
                            )))
                            if block_mismatch:
                                for q in scores:
                                    q["reference_block_mismatch"] = 1
                                    q["failed"] = 1
                            block = dict(
                                base_seed=b, head_seed=h, episodes=9536,
                                actual_reads=reads, bytes_read=bytes_read,
                                reference_necessity_prediction_errors=replay[
                                    "necessity_prediction_errors"
                                ],
                                reference_target_prediction_errors=replay[
                                    "target_prediction_errors"
                                ],
                                reference_necessity_max_abs_logit_difference=replay[
                                    "necessity_max_abs_logit_difference"
                                ],
                                reference_target_max_abs_logit_difference=replay[
                                    "target_max_abs_logit_difference"
                                ],
                                reference_replay_error=int(replay_error * 9536),
                                reference_block_mismatch=int(block_mismatch * 9536),
                                **totals,
                            )
                            allowed_records.append(block)
                            trace_scores = scores
                        else:
                            prefix = prefix_replay(arrays, reference)
                            ref_n0 = reference["necessity_predictions"][:, 0]
                            ref_t0 = reference["target_predictions"][:, 0]
                            ref_n1 = reference["necessity_predictions"][:, 1]
                            ref_t1 = reference["target_predictions"][:, 1]
                            scores = [
                                score_limit(
                                    rec, ref_n0[j], ref_t0[j], ref_n1[j], ref_t1[j],
                                    rec["initial"]["features"],
                                )
                                for j, rec in enumerate(observed)
                            ]
                            totals = {k: sum(x[k] for x in scores) for k in LIMIT_COUNTERS}
                            attempt_limit_rows = sum(x["expected_limit"] for x in scores)
                            sufficient_after_first = 9536 - attempt_limit_rows
                            provider_calls = sum(
                                (a["dispatch"] or {}).get("provider_calls", 0)
                                for rec in observed for a in rec["acquisitions"]
                            )
                            publications = sum(
                                (a["dispatch"] or {}).get("fact_publications", 0)
                                for rec in observed for a in rec["acquisitions"]
                            )
                            receipts = sum(len(rec["receipts"]) for rec in observed)
                            learned_decisions = sum(rec["decision_charges"] for rec in observed)
                            second_provider_calls = sum(
                                (rec["acquisitions"][1]["dispatch"] or {}).get("provider_calls", 0)
                                for rec in observed if len(rec["acquisitions"]) == 2
                            )
                            second_publications = sum(
                                (rec["acquisitions"][1]["dispatch"] or {}).get("fact_publications", 0)
                                for rec in observed if len(rec["acquisitions"]) == 2
                            )
                            block = dict(
                                base_seed=b, head_seed=h, episodes=9536,
                                first_reads=reads, bytes_read=bytes_read,
                                provider_calls=provider_calls,
                                publications=publications,
                                receipts=receipts,
                                learned_decisions=learned_decisions,
                                attempt_limit_rows=attempt_limit_rows,
                                sufficient_after_first=sufficient_after_first,
                                reference_second_reads=p198["allowed_records"][idx]["second_reads"],
                                second_provider_calls=second_provider_calls,
                                second_publications=second_publications,
                                prefix_necessity_prediction_errors=prefix[
                                    "necessity_prediction_errors"
                                ],
                                prefix_target_prediction_errors=prefix[
                                    "target_prediction_errors"
                                ],
                                prefix_necessity_logit_delta=prefix[
                                    "necessity_max_abs_logit_difference"
                                ],
                                prefix_target_logit_delta=prefix[
                                    "target_max_abs_logit_difference"
                                ],
                                unauthorized_third_prediction=prefix[
                                    "unauthorized_third_prediction"
                                ],
                                **totals,
                            )
                            limit_records.append(block)
                            trace_scores = scores

                        for j, rec0 in enumerate(observed):
                            trace.write(json.dumps(
                                dict(
                                    arm=arm,
                                    base_seed=b,
                                    head_seed=h,
                                    source_row=int(source_rows[j]),
                                    world_code=int(world_codes[j]),
                                    score=trace_scores[j],
                                    trace=rec0,
                                ),
                                sort_keys=True,
                                separators=(",", ":"),
                                allow_nan=False,
                            ) + "\n")
                        print(
                            f"[C199] arm={arm} block={idx+1}/9 base={b} head={h} "
                            f"failed={block['failed']}",
                            flush=True,
                        )

        record_file("episode-traces.jsonl.gz")
        np.savez_compressed(
            out / "episode-predictions.npz",
            necessity_predictions=dense_n,
            necessity_logits=dense_z,
            target_predictions=dense_t,
            target_logits=dense_tz,
            row_indices=source_rows.astype("<i4"),
            local_rows=local_rows.astype("<i4"),
            world_codes=world_codes.astype(np.int8),
        )
        record_file("episode-predictions.npz")
        save("allowed-replay.json", allowed_replay)
        save("episode-results.json", dict(allowed=allowed_records, limit=limit_records))

        guard()
        precheck(parents["c198_summary"], *args)
        for f, hsh in protected.items():
            require(audit.sha(f) == hsh, "Protected input changed:" + f)
        for artifact in artifacts:
            require(
                audit.sha(out / artifact["file"]) == artifact["sha256"],
                "Output changed:" + artifact["file"],
            )

        result = dict(
            experiment_id=EXPERIMENT_ID,
            stage=STAGE,
            commit_sha=expected_head,
            status="PASS" if gate(allowed_records, limit_records) else "FAIL",
            diagnostic_execution_valid=True,
            C198_summary_sha256=PARENT_SHA,
            source_blobs=pins,
            input_sha256=protected,
            artifacts=artifacts,
            allowed_records=allowed_records,
            limit_records=limit_records,
            allowed_replay=allowed_replay,
            episodes_per_arm=85824,
            new_training=0,
            fresh_seeds=0,
            network_calls=0,
            answer_generation=0,
            proof_checker_calls=0,
            core_evidence_writes=0,
            production_runtime_modified=False,
            gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter() - started,
            limitations=[
                "same repeatedly inspected development family",
                "dispatch-limit intervention is trusted runtime configuration",
                "no retry/resource-policy/tool-choice/holdout/language/answer/proof/GateE",
            ],
        )
        validate_result(result)
        (out / "summary.json").write_bytes(blob(result))
        print("[C199] source/output preservation checked", flush=True)
        print("=== C199 RESULT ===", flush=True)
        print(blob(result).decode(), flush=True)
        return result
    except Exception as exc:
        (out / "invalid.json").write_bytes(blob(dict(
            experiment_id=EXPERIMENT_ID,
            status="INVALID",
            diagnostic_execution_valid=False,
            error=str(exc),
            completed_allowed=allowed_records,
            completed_limit=limit_records,
        )))
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in PRIOR_NAMES:
        parser.add_argument("--" + name + "-summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
