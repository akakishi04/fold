"""C198: stale-reservation containment in the accepted reason-aware generic loop.

Hold C197/C196 loop semantics, budget13, frozen C181/C188 models, cohort and coherent
source bindings. Change only one in-flight condition: after the first successful RETRIEVE
reservation, the trusted scheduler advances evidence_time and revision by one before
dispatch. The old reservation must be rejected as STALE_RESERVATION without provider
execution, publication, receipt, retry or fake SUFFICIENT.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import time
from dataclasses import asdict, replace
from pathlib import Path

import numpy as np
import torch

EXPERIMENT_ID = "C198-v5e-stale-reservation-generic-loop"
STAGE = "V5-E-STALE-RESERVATION-GENERIC-LOOP"
BASE = "5d1fe42b3811ddf8c756d6582c6e73a78c9cea46"
PARENT_EXECUTION = "7d9a09bba9ac2286806f40bc20c6ce45a21cb279"
PARENT_SHA = "632e8af4a215d12adc83aa015da855c63605205c87832aa6a511dabfc4fd1ca5"
REFERENCE_EXECUTION = PARENT_EXECUTION
REFERENCE_SHA = PARENT_SHA
BASE_SEEDS = (181001, 181002, 181003)
HEAD_SEEDS = (188001, 188002, 188003)
ARM = "INTERNAL_SEMANTICS"
ARMS = ("ALLOWED", "STALE_RESERVATION_AFTER_RESERVATION")
BATCH = 1024
ATOL = 1e-6
MAX_ACQUISITIONS = 3
MAX_DECISIONS = 4
PRIOR_NAMES = (
    "c197", "c196", "c195", "c194", "c193", "c192", "c191", "c190", "c189",
    "c188", "c187", "c186", "c185", "c184", "c183", "c182", "c181", "c180",
    "c179", "c178", "c177", "c176", "c174",
)
OWN = (
    "fold_lm/v05_benchmarks/gate_e_c198_stale_reservation_generic_loop.py",
    "tests_lm/test_v05_c198_stale_reservation_generic_loop.py",
    "tools/run_c198.ps1",
    "tools/invoke_c198.ps1",
    "docs/experiment-ledger-addendum-c198-preregistration.md",
)
EXPECTED_TESTS = 1677
OUTPUTS = {
    "stale-reservation-plan.json",
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


def load_c197_predictions(path):
    p = Path(path)
    require(p.is_file() and p.stat().st_size < 20_000_000,
            "Unexpected C197 prediction artifact size")
    with np.load(p, allow_pickle=False) as z:
        expected = {
            "necessity_predictions", "necessity_logits", "target_predictions", "target_logits",
            "row_indices", "local_rows", "world_codes",
        }
        require(set(z.files) == expected, "C197 prediction schema drift")
        out = {k: z[k].copy() for k in z.files}
    require(
        out["necessity_predictions"].shape == (2, 9, 9536, 4)
        and out["necessity_logits"].shape == (2, 9, 9536, 4, 2)
        and out["target_predictions"].shape == (2, 9, 9536, 3)
        and out["target_logits"].shape == (2, 9, 9536, 3, 4)
        and out["row_indices"].shape == (9536,)
        and out["local_rows"].shape == (9536,)
        and out["world_codes"].shape == (9536,),
        "C197 prediction array drift",
    )
    return out


def invalidate_reservation(owner):
    """Trusted scheduler refresh after reservation, before dispatch."""
    from fold_lm.v05 import structured_task_input as task

    view = owner.state.view
    require(view.evidence_time < task.MAX_INTEGER and view.revision < task.MAX_INTEGER,
            "Cannot advance registered evidence identity")
    before_resources = view.resources
    before_facts = view.facts
    owner.refresh(replace(
        view,
        evidence_time=view.evidence_time + 1,
        revision=view.revision + 1,
    ))
    after = owner.state.view
    require(after.resources == before_resources and after.facts == before_facts,
            "Stale refresh changed facts/resources")
    require((after.evidence_time, after.revision) ==
            (view.evidence_time + 1, view.revision + 1),
            "Stale refresh did not advance evidence identity exactly once")


def acquire(owner, target_index, *, stale):
    from fold_lm.v05 import structured_action_runtime as action

    require(type(target_index) is int and 0 <= target_index < 4, "Local target required")
    view = owner.state.view
    require(view.facts[target_index].status == "UNOBSERVED",
            "Target must currently be unobserved")
    fact_id = view.facts[target_index].fact_id
    transition = owner.apply(action.propose(owner.state, "RETRIEVE", fact_index=target_index))
    dispatched = None
    if transition.result.status == "PENDING":
        if stale:
            invalidate_reservation(owner)
        dispatched = owner.dispatch(transition.result.intent.intent_id)
    return dict(
        input_index=target_index,
        fact_id=fact_id,
        action=asdict(transition.result),
        dispatch=asdict(dispatched) if dispatched else None,
    )


def admitted(acq):
    from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as c196
    return c196.admitted(acq)


def run_loop_stale_aware(views, world_codes, endpoints, base, selector, initial, arm):
    from fold_lm.v05 import structured_acquisition_lifecycle as life
    from fold_lm.v05 import structured_action_runtime as action
    from fold_lm.v05 import structured_task_input as task
    from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as driver
    from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189

    require(arm in ARMS, "Unregistered C198 arm")
    require(len(views) == len(world_codes) > 0, "Episode/world alignment required")
    owners = [
        life.AcquisitionOwner(
            action.RuntimeState(v),
            {"RETRIEVE": endpoints[int(code)]},
            max_dispatches=MAX_ACQUISITIONS,
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
        require(iteration < MAX_DECISIONS, "Stale-aware loop exceeded derived decision bound")
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

            stale = arm == "STALE_RESERVATION_AFTER_RESERVATION"
            if stale:
                require(iteration == 0,
                        "Stale arm must terminate before a second learned decision")
            acq = acquire(owners[i], target_index, stale=stale)
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


STALE_COUNTERS = (
    "failed",
    "initial_prediction_error",
    "stale_reservation_error",
    "status_error",
    "provider_call_error",
    "publication_error",
    "receipt_error",
    "retry_error",
    "resource_error",
    "identity_refresh_error",
    "fact_mutation_error",
    "fake_sufficient_error",
)


def score_stale(record, ref_initial_n, ref_initial_t, initial_features):
    phases = record["phases"]
    acquisitions = record["acquisitions"]
    final = record["final"]
    initial_prediction_error = int(not (
        len(phases) == 1
        and phases[0]["necessity_prediction"] == int(ref_initial_n)
        and phases[0].get("target_prediction") == int(ref_initial_t)
    ))
    a = acquisitions[0] if len(acquisitions) == 1 else None
    action_result = a["action"] if isinstance(a, dict) else None
    dispatch = a["dispatch"] if isinstance(a, dict) else None
    stale_reservation_error = int(not (
        isinstance(action_result, dict)
        and isinstance(dispatch, dict)
        and action_result["status"] == "PENDING"
        and action_result["reason"] == "ACQUISITION_RESERVED"
        and action_result["internal_charged"] == 1
        and action_result["acquisition_reserved"] == 1
        and dispatch["status"] == "REJECTED"
        and dispatch["reason"] == "STALE_RESERVATION"
        and dispatch["internal_charged"] == 1
        and dispatch["provider_calls"] == 0
        and dispatch["fact_publications"] == 0
        and dispatch["evidence"] is None
    ))
    status_error = int(
        record["status"] != "UNRESOLVED_ACQUISITION_STALE_RESERVATION"
    )
    provider_call_error = int(
        not isinstance(dispatch, dict) or dispatch.get("provider_calls") != 0
    )
    publication_error = int(
        isinstance(dispatch, dict) and dispatch.get("fact_publications", 0) != 0
    )
    receipt_error = int(len(record["receipts"]) != 0)
    retry_error = int(
        len(phases) != 1
        or len(acquisitions) != 1
        or record["decision_charges"] != 1
    )
    f = np.asarray(final["features"], dtype=np.int64)
    x = np.asarray(initial_features, dtype=np.int64)
    resource_error = int(not (
        f[62] == 10
        and f[63] == 3
        and f[64] == 1
        and f[67] == 1
        and f[70] == 0
        and f[71] == 10
        and record["pending"] is None
        and record["runtime_terminal"] is None
    ))
    identity_refresh_error = int(not (f[2] == x[2] + 1 and f[3] == x[3] + 1))
    fact_mutation_error = int(any(f[46:62] != x[46:62]))
    fake_sufficient_error = int(record["status"] == "SUFFICIENT_CLASSIFICATION")
    values = (
        initial_prediction_error,
        stale_reservation_error,
        status_error,
        provider_call_error,
        publication_error,
        receipt_error,
        retry_error,
        resource_error,
        identity_refresh_error,
        fact_mutation_error,
        fake_sufficient_error,
    )
    return dict(
        failed=int(any(values)),
        initial_prediction_error=initial_prediction_error,
        stale_reservation_error=stale_reservation_error,
        status_error=status_error,
        provider_call_error=provider_call_error,
        publication_error=publication_error,
        receipt_error=receipt_error,
        retry_error=retry_error,
        resource_error=resource_error,
        identity_refresh_error=identity_refresh_error,
        fact_mutation_error=fact_mutation_error,
        fake_sufficient_error=fake_sufficient_error,
    )


def expected_order():
    return [(b, h) for b in BASE_SEEDS for h in HEAD_SEEDS]


def gate(allowed, stale):
    from fold_lm.v05_benchmarks import gate_e_c196_result_aware_generic_loop as c196

    if [(r.get("base_seed"), r.get("head_seed")) for r in allowed] != expected_order():
        return False
    if [(r.get("base_seed"), r.get("head_seed")) for r in stale] != expected_order():
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
    for r in stale:
        if r.get("episodes") != 9536:
            return False
        if any(type(r.get(k)) is not int or r[k] < 0 for k in STALE_COUNTERS):
            return False
        if any(r[k] != 0 for k in STALE_COUNTERS):
            return False
        if r.get("stale_attempts") != 9536:
            return False
        if r.get("provider_calls") != 0 or r.get("actual_provider_reads") != 0:
            return False
        if r.get("publications") != 0 or r.get("receipts") != 0:
            return False
        if r.get("learned_decisions") != 9536 or r.get("retries") != 0:
            return False
        if r.get("initial_reference_prediction_errors") != 0:
            return False
        if r.get("initial_reference_target_errors") != 0:
            return False
        if r.get("initial_reference_necessity_logit_delta", 1) > ATOL:
            return False
        if r.get("initial_reference_target_logit_delta", 1) > ATOL:
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
        question="can the accepted reason-aware result-aware generic loop preserve allowed behavior and safely expose a reservation made stale by a trusted evidence-identity refresh before dispatch",
        changed="after a successful first RETRIEVE reservation, the trusted scheduler increments evidence_time and revision by one before dispatch; all facts/resources/authority/source binding stay otherwise fixed",
        held="budget13,C174 cohort,9 frozen C181/C188 pairs,16 coherent source bindings,C172/C173,C197 reason propagation,C196 result-aware continuation,teachers,max_dispatches3,raw argmax",
        allowed_arm="full9536 worlds/selector; exact accepted C197/C196/C194 allowed replay required",
        stale_arm="full9536 worlds/selector; one PENDING/ACQUISITION_RESERVED action, trusted +1 evidence_time/+1 revision refresh, then REJECTED/STALE_RESERVATION dispatch; zero provider call/publication/receipt/retry/fact mutation/fake sufficient",
        stale_resources="after decision+reservation+refresh+stale dispatch: internal10,acquisitions3,RETRIEVE available1/permitted1,last_outcome NONE,step10,evidence_time2,revision2,pending none",
        episodes_per_arm=85824,
        blocks_per_arm=9,
        gate="all9 allowed blocks exact reference replay and zero scientific errors; all9 stale blocks9536 stale rejections,zero provider calls/publication/receipt/retry/fact mutation/fake sufficient,exact resources and +1 evidence identity",
        training=0,
        fresh_seeds=0,
        network_calls=0,
        answer_generation=0,
        proof_checker_calls=0,
        core_evidence_writes=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        outputs=sorted(OUTPUTS),
        limits="development family;only first-acquisition stale reservation tested;no attempt-limit/retry/resource-policy/tool-choice/holdout/language/answer/proof/GateE",
    )


MANIFEST_SHA = "e108bcaefdb882f05420c078a4866272afe375d48e62e50ac726241fed2a44e9"


def precheck(c197_summary, *args):
    from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
    from fold_lm.v05_benchmarks import gate_e_c197_provider_failure_generic_loop as parent

    require(len(args) == 23, "Twenty-two prior summaries and repository root required")
    root = args[-1]
    (
        p196, p195, p194, p193, p192, p191, p190, p189, p188, p181, p174,
        pins, protected,
    ) = parent.precheck(args[0], *args[1:])
    require(audit.sha(c197_summary) == PARENT_SHA, "C197 summary changed")
    p197 = audit.read_json(c197_summary)
    parent.validate_result(p197)
    require(
        p197["commit_sha"] == PARENT_EXECUTION
        and p197["status"] == "PASS"
        and parent.gate(p197["allowed_records"], p197["failure_records"])
        and p197["source_blobs"] == pins,
        "Wrong accepted C197 source/result",
    )
    protected[str(Path(c197_summary).resolve())] = PARENT_SHA
    for artifact in p197["artifacts"]:
        f = audit.safe_child(Path(c197_summary).resolve().parent, artifact["file"])
        require(
            f.is_file()
            and f.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(f) == artifact["sha256"],
            "Changed C197 artifact:" + artifact["file"],
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
    require(len(pins) == 151 and len(protected) == 396,
            "Source/protected union drift")
    require(digest(manifest()) == MANIFEST_SHA, "Manifest drift")
    return (
        p197, p196, p195, p194, p193, p192, p191, p190, p189, p188, p181, p174,
        pins, protected,
    )


def regression_modules(root):
    from fold_lm.v05_benchmarks import gate_e_c197_provider_failure_generic_loop as parent

    names = parent.regression_modules(root)
    require(len(names) == len(set(names)) == 82, "Historical regression list drift")
    return names + ["tests_lm.test_v05_c198_stale_reservation_generic_loop"]


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C198",
    )
    require(
        payload["episodes_per_arm"] == 85824
        and len(payload["allowed_records"]) == len(payload["stale_records"]) == 9
        and len(payload["source_blobs"]) == 151
        and len(payload["input_sha256"]) == 396
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
            "PASS" if gate(payload["allowed_records"], payload["stale_records"]) else "FAIL"
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
        p197, p196, p195, p194, p193, p192, p191, p190, p189, p188, p181, p174,
        pins, protected,
    ) = precheck(parents["c197_summary"], *args)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    artifacts = []
    allowed_records = []
    stale_records = []
    started = time.perf_counter()

    def record_file(name):
        f = out / name
        artifacts.append(
            dict(file=name, sha256=audit.sha(f), serialized_bytes=f.stat().st_size)
        )

    def save(name, value):
        (out / name).write_bytes(blob(value))
        record_file(name)

    save("stale-reservation-plan.json", dict(manifest(), source_blobs=pins))

    try:
        print(
            "[C198] plan fixed; accepted C197/C196 loop; ALLOWED replay + "
            "post-reservation stale refresh",
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

        c197_dir = Path(parents["c197_summary"]).resolve().parent
        saved = load_c197_predictions(c197_dir / "episode-predictions.npz")
        require(
            np.array_equal(saved["row_indices"], source_rows)
            and np.array_equal(saved["local_rows"], local_rows)
            and np.array_equal(saved["world_codes"], world_codes),
            "C197 episode identity drift",
        )

        c181_dir = Path(parents["c181_summary"]).resolve().parent
        c188_dir = Path(parents["c188_summary"]).resolve().parent
        fits = {
            f["seed"]: f for f in p181["fit_records"] if f["arm"] == ARM
        }
        selector_sha = {
            (r["base_seed"], r["head_seed"]): r["head_sha256"]
            for r in p188["selector_results"]
        }
        bases = {}
        heads = {}
        for b in BASE_SEEDS:
            bases[b] = frozen.restore_bare(
                c181_dir / f"probe-{b}-{ARM}.pt",
                b,
                ARM,
                fits[b]["final_sha256"],
            )
            for h in HEAD_SEEDS:
                heads[b, h] = c189.restore_selector(
                    c188_dir / f"selector-{b}-{h}.pt",
                    b,
                    h,
                    selector_sha[b, h],
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
            "wt",
            encoding="utf-8",
            newline="\n",
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
                            expanded13,
                            source_rows,
                            world_codes,
                            f"C198-{arm}-b{b}-h{h}",
                        )
                        before_reads = sum(p.reads for p in real_providers.values())
                        before_bytes = sum(p.bytes_read for p in real_providers.values())
                        observed, arrays, _ = run_loop_stale_aware(
                            views,
                            world_codes,
                            real_endpoints,
                            bases[b],
                            heads[b, h],
                            initial,
                            arm,
                        )
                        reads = (
                            sum(p.reads for p in real_providers.values()) - before_reads
                        )
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
                            totals = {
                                k: sum(x[k] for x in scores) for k in c193.COUNTERS
                            }
                            ref_rec = p197["allowed_records"][idx]
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
                                base_seed=b,
                                head_seed=h,
                                episodes=9536,
                                actual_reads=reads,
                                bytes_read=bytes_read,
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
                            ref_n = reference["necessity_predictions"][:, 0]
                            ref_t = reference["target_predictions"][:, 0]
                            initial_nerr = int(
                                (arrays["necessity_predictions"][:, 0] != ref_n).sum()
                            )
                            initial_terr = int(
                                (arrays["target_predictions"][:, 0] != ref_t).sum()
                            )
                            nmask = ref_n >= 0
                            tmask = ref_t >= 0
                            nd = float(np.max(np.abs(
                                arrays["necessity_logits"][nmask, 0]
                                - reference["necessity_logits"][nmask, 0]
                            ))) if nmask.any() else 0.0
                            finite = (
                                np.isfinite(reference["target_logits"][:, 0, :])
                                & tmask[:, None]
                            )
                            td = float(np.max(np.abs(
                                arrays["target_logits"][:, 0, :][finite]
                                - reference["target_logits"][:, 0, :][finite]
                            ))) if finite.any() else 0.0

                            scores = [
                                score_stale(
                                    rec,
                                    ref_n[j],
                                    ref_t[j],
                                    rec["initial"]["features"],
                                )
                                for j, rec in enumerate(observed)
                            ]
                            totals = {
                                k: sum(x[k] for x in scores) for k in STALE_COUNTERS
                            }
                            attempts = sum(
                                len(rec["acquisitions"]) for rec in observed
                            )
                            provider_calls = sum(
                                (a["dispatch"] or {}).get("provider_calls", 0)
                                for rec in observed
                                for a in rec["acquisitions"]
                            )
                            publications = sum(
                                (a["dispatch"] or {}).get("fact_publications", 0)
                                for rec in observed
                                for a in rec["acquisitions"]
                            )
                            receipts = sum(len(rec["receipts"]) for rec in observed)
                            decisions = sum(rec["decision_charges"] for rec in observed)
                            retries = sum(
                                max(0, len(rec["phases"]) - 1) for rec in observed
                            )
                            block = dict(
                                base_seed=b,
                                head_seed=h,
                                episodes=9536,
                                stale_attempts=attempts,
                                provider_calls=provider_calls,
                                actual_provider_reads=reads,
                                bytes_read=bytes_read,
                                publications=publications,
                                receipts=receipts,
                                learned_decisions=decisions,
                                retries=retries,
                                initial_reference_prediction_errors=initial_nerr,
                                initial_reference_target_errors=initial_terr,
                                initial_reference_necessity_logit_delta=nd,
                                initial_reference_target_logit_delta=td,
                                **totals,
                            )
                            stale_records.append(block)
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
                            f"[C198] arm={arm} block={idx+1}/9 base={b} head={h} "
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
        save(
            "episode-results.json",
            dict(allowed=allowed_records, stale=stale_records),
        )

        guard()
        precheck(parents["c197_summary"], *args)
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
            status="PASS" if gate(allowed_records, stale_records) else "FAIL",
            diagnostic_execution_valid=True,
            C197_summary_sha256=PARENT_SHA,
            source_blobs=pins,
            input_sha256=protected,
            artifacts=artifacts,
            allowed_records=allowed_records,
            stale_records=stale_records,
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
                "only first-acquisition stale reservation tested",
                "no attempt-limit/retry/resource-policy/tool-choice/holdout/language/answer/proof/GateE",
            ],
        )
        validate_result(result)
        (out / "summary.json").write_bytes(blob(result))
        print("[C198] source/output preservation checked", flush=True)
        print("=== C198 RESULT ===", flush=True)
        print(blob(result).decode(), flush=True)
        return result
    except Exception as exc:
        (out / "invalid.json").write_bytes(blob(dict(
            experiment_id=EXPERIMENT_ID,
            status="INVALID",
            diagnostic_execution_valid=False,
            error=str(exc),
            completed_allowed=allowed_records,
            completed_stale=stale_records,
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
