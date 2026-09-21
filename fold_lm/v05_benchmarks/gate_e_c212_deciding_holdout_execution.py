"""C212: execute the frozen C211 deciding Gate-E holdout exactly once.

The scientific question is fixed by accepted C211: does the selected frozen candidate satisfy every
registered Gate-E rule on the independent holdout relative to INTERNAL_ONLY and
FIXED_ACQUISITION?

C212 changes no candidate identity, holdout row, threshold, statistical rule, family, budget,
answer boundary, checkpoint or runtime policy. A complete valid rule failure is scientific
negative evidence, not an execution error.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest

from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_e_c210_baseline_development_measurement as c210
from fold_lm.v05_benchmarks import gate_e_c211_deciding_manifest_freeze as c211

EXPERIMENT_ID = "C212-v5e-deciding-holdout-execution"
STAGE = "V5-E-DECIDING-HOLDOUT-EXECUTION"
BASE = "5cecd8d3683b3ccdbdb285ec97ea4722c8c3ba0f"
PARENT_C211_EXECUTION = "9cedc79a02441e9cddb0efc0c8bbc7714f9112db"
PARENT_C211_SHA = "97f5c1fde9128651ae842046e706219a50e0f34238b87d17d253e89d71279263"
DECIDING_MANIFEST_SHA = "f9356e87b210bc7d836d016a9ad7a4f841a9a651b3bb9faf9428b0415df9e6d6"
DECISION_RULES_SHA = "d143f2a6b4b96c672131daf22dea5c207d42375440c7d403ee95b9782fd75bcc"
HOLDOUT_VISIBLE_SHA = "1197f59ab6bf659929ecb7a9f42df27ea28e81586c4602f8e1eb96da17be126b"
HOLDOUT_SCORER_SHA = "3975c10afc2e644f5279de4d46459d1aa250c6e7b381bb944b0b8cf6b585ff22"
HOLDOUT_UNITS_SHA = "630d9c94b4aee67f55c3f9704ad6a508679e01450da73dd18a8935b4bac8dc34"
SELECTED_POLICY = "CANDIDATE-181001-188001"
SELECTED_BASE_SEED = 181001
SELECTED_HEAD_SEED = 188001
BASE_CHECKPOINT_SHA = "3f1bad426640c58ad8479a226cb2292991e014ec88bfbc0931a538e0f81e8289"
SELECTOR_CHECKPOINT_SHA = "02547ed98ce155f6c260b5dbdf8fe5e2bb7dc4ce40248c77d511ab8089e6178d"
POLICY_IDS = (c210.POLICY_INTERNAL, c210.POLICY_FIXED, SELECTED_POLICY)
MANIFEST_SHA = "1e9c1fd0de152ccd070a267383e46fbe73ff5c55114fe984c85ecd7274347898"
C211_ARTIFACT_SHA = {
    "holdout-visible.json": HOLDOUT_VISIBLE_SHA,
    "holdout-scorer.json": HOLDOUT_SCORER_SHA,
    "holdout-units.json": HOLDOUT_UNITS_SHA,
    "decision-rules.json": DECISION_RULES_SHA,
    "deciding-manifest.json": DECIDING_MANIFEST_SHA,
}
OWN = (
    "fold_lm/v05_benchmarks/gate_e_c212_deciding_holdout_execution.py",
    "tests_lm/test_v05_c212_deciding_holdout_execution.py",
    "tools/run_c212.ps1",
    "tools/invoke_c212.ps1",
    "docs/experiment-ledger-addendum-c212-preregistration.md",
    "docs/gate-e-deciding-holdout-execution-v0.1.md",
)
OUTPUTS = {
    "execution-plan.json",
    "episode-results.json",
    "policy-summary.json",
    "family-summary.json",
    "gate-e-decision.json",
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
        parent_c211_execution=PARENT_C211_EXECUTION,
        parent_c211_sha256=PARENT_C211_SHA,
        deciding_manifest_sha256=DECIDING_MANIFEST_SHA,
        decision_rules_sha256=DECISION_RULES_SHA,
        holdout_visible_sha256=HOLDOUT_VISIBLE_SHA,
        holdout_scorer_sha256=HOLDOUT_SCORER_SHA,
        holdout_units_sha256=HOLDOUT_UNITS_SHA,
        selected_candidate=SELECTED_POLICY,
        base_checkpoint_sha256=BASE_CHECKPOINT_SHA,
        selector_checkpoint_sha256=SELECTOR_CHECKPOINT_SHA,
        baselines=[c210.POLICY_INTERNAL, c210.POLICY_FIXED],
        policy_identities=list(POLICY_IDS),
        holdout_episodes=144,
        dependence_units=72,
        policy_episode_evaluations=432,
        execution=(
            "evaluate INTERNAL_ONLY, FIXED_ACQUISITION and the frozen selected candidate exactly once "
            "on the accepted C211 independent holdout using the accepted C210 policy/runtime boundary"
        ),
        registered_decision_rules="exact accepted C211 decision-rules.json; no mutation after holdout",
        shared_answer_boundary=(
            "C171 completion_values + benchmark proof_fixture + production "
            "structured_derived_result.verify; disclosed symbolic guard"
        ),
        holdout_execution_count=1,
        no_retraining_after_holdout=True,
        no_candidate_change=True,
        no_threshold_relaxation=True,
        no_failed_family_removal=True,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_deciding_execution=True,
        scope=(
            "one-shot deciding holdout execution under frozen C211 identity/rules; "
            "valid rule failure is scientific negative, execution defects retry same C212"
        ),
    )


def _op_ok(candidate, baseline, op):
    require(op in (">=", "<="), "registered comparator required")
    return candidate >= baseline if op == ">=" else candidate <= baseline


def fixed_noninferiority(candidate_summary, fixed_summary, candidate_families, fixed_families, rules):
    registered = rules["fixed_noninferiority"]
    require(registered["margin_episodes"] == 0, "fixed noninferiority margin drift")
    overall = {}
    for metric, op in registered["overall"]:
        cv = int(candidate_summary[metric])
        bv = int(fixed_summary[metric])
        overall[metric] = dict(candidate=cv, baseline=bv, comparator=op, passed=_op_ok(cv, bv, op))

    require(set(candidate_families) == set(fixed_families) == set(c211.FAMILIES),
            "fixed family coverage drift")
    per_family = {}
    for family in c211.FAMILIES:
        checks = {}
        for metric, op in registered["per_family"]:
            cv = int(candidate_families[family][metric])
            bv = int(fixed_families[family][metric])
            checks[metric] = dict(
                candidate=cv, baseline=bv, comparator=op, passed=_op_ok(cv, bv, op)
            )
        per_family[family] = checks

    return dict(
        margin_episodes=0,
        overall=overall,
        per_family=per_family,
        all_pass=(
            all(x["passed"] for x in overall.values())
            and all(x["passed"] for checks in per_family.values() for x in checks.values())
        ),
    )


def _align_rows(candidate_rows, baseline_rows):
    require(len(candidate_rows) == len(baseline_rows) == 144, "paired144 rows required")
    for c, b in zip(candidate_rows, baseline_rows, strict=True):
        require(
            c["case_id"] == b["case_id"]
            and c["unit_id"] == b["unit_id"]
            and c["family"] == b["family"]
            and c["condition"] == b["condition"],
            "paired row identity drift",
        )


def internal_improvement(candidate_rows, internal_rows, rules):
    _align_rows(candidate_rows, internal_rows)
    registered = rules["internal_improvement"]
    require(
        registered["minimum_margin_episodes"] == 1
        and registered["claims"] == [
            "useful_correct_resolution",
            "positive_acquisition_gain",
        ]
        and registered["test"] == "one-sided exact paired McNemar"
        and registered["familywise_alpha"] == 0.05
        and registered["holm_thresholds"] == [0.025, 0.05],
        "internal improvement rule drift",
    )

    candidate_correct = [int(r["correct"] == 1) for r in candidate_rows]
    internal_correct = [int(r["correct"] == 1) for r in internal_rows]
    candidate_gain = [int(int(r["acquisition_gain"]) > 0) for r in candidate_rows]
    internal_gain = [int(int(r["acquisition_gain"]) > 0) for r in internal_rows]

    claims = {}
    for name, cv, bv in (
        ("useful_correct_resolution", candidate_correct, internal_correct),
        ("positive_acquisition_gain", candidate_gain, internal_gain),
    ):
        test = c211.one_sided_mcnemar(cv, bv)
        margin = int(sum(cv) - sum(bv))
        claims[name] = dict(
            candidate_positive=int(sum(cv)),
            baseline_positive=int(sum(bv)),
            margin_episodes=margin,
            minimum_margin_episodes=1,
            margin_pass=margin >= 1,
            mcnemar=test,
        )

    holm = c211.holm_two(
        {name: payload["mcnemar"]["p_one_sided"] for name, payload in claims.items()},
        alpha=0.05,
    )
    return dict(
        claims=claims,
        holm=holm,
        all_pass=all(x["margin_pass"] for x in claims.values()) and holm["all_pass"],
    )


def hard_zero_gate(candidate_summary, candidate_rows, rules):
    hard = {
        name: int(candidate_summary[name])
        for name in rules["hard_zero_candidate"]
    }
    runtime = dict(
        authority_violations=int(candidate_summary["authority_violation"]),
        acquisition_budget_violations=int(sum(
            max(0, int(r["acquisition_attempts"]) - 1) for r in candidate_rows
        )),
        malformed_evidence_publications=int(candidate_summary["malformed_publication"]),
        hypothesis_to_observation_promotions=0,
    )
    require(set(runtime) == set(rules["hard_runtime"]), "hard runtime key drift")
    return dict(
        candidate=hard,
        runtime=runtime,
        all_pass=(
            all(value == 0 for value in hard.values())
            and all(runtime[name] == int(want) for name, want in rules["hard_runtime"].items())
        ),
    )


def compute_ceiling_gate(model_meter, rules):
    ceiling = rules["candidate_compute_ceiling"]
    actual = dict(
        initial_inference_rows=int(model_meter["initial_rows"]),
        post_inference_rows=int(model_meter["post_rows"]),
        total_inference_rows=int(model_meter["inference_rows"]),
        forward_calls=int(model_meter["inference_forward_calls"]),
        cell_calls=int(model_meter["inference_cell_calls"]),
    )
    checks = dict(
        initial_rows=actual["initial_inference_rows"] == int(ceiling["initial_inference_rows"]),
        post_rows=actual["post_inference_rows"] <= int(ceiling["maximum_post_inference_rows"]),
        total_rows=actual["total_inference_rows"] <= int(ceiling["maximum_total_inference_rows"]),
        forward_calls=actual["forward_calls"] <= int(ceiling["maximum_forward_calls"]),
        cell_calls=actual["cell_calls"] <= int(ceiling["maximum_cell_calls"]),
        row_accounting=(
            actual["total_inference_rows"]
            == actual["initial_inference_rows"] + actual["post_inference_rows"]
        ),
    )
    return dict(actual=actual, ceiling=ceiling, checks=checks, all_pass=all(checks.values()))


def output_floor_gate(candidate_summary, candidate_rows, rules):
    floor = rules["unsupported_assertion_floor"]
    verified_emissions = all(
        (not bool(r["answer_emitted"])) or bool(r["resolver_verified"])
        for r in candidate_rows
    )
    return dict(
        candidate_guarded_unsupported=int(candidate_summary["guarded_unsupported_assertion"]),
        candidate_required=int(floor["candidate_post_guard_required"]),
        strict_reduction_claim=floor["strict_reduction_claim"],
        verified_emissions=verified_emissions,
        all_pass=(
            int(candidate_summary["guarded_unsupported_assertion"])
            == int(floor["candidate_post_guard_required"])
            and floor["strict_reduction_claim"] == "NOT_DEMONSTRATED_ZERO_FLOOR"
            and verified_emissions
        ),
    )


def build_decision(policy_summary, family_summary, rows_by_policy, model_meter, rules):
    require(set(policy_summary) == set(family_summary) == set(POLICY_IDS),
            "three-policy deciding summary required")
    fixed = fixed_noninferiority(
        policy_summary[SELECTED_POLICY],
        policy_summary[c210.POLICY_FIXED],
        family_summary[SELECTED_POLICY],
        family_summary[c210.POLICY_FIXED],
        rules,
    )
    improvement = internal_improvement(
        rows_by_policy[SELECTED_POLICY],
        rows_by_policy[c210.POLICY_INTERNAL],
        rules,
    )
    hard = hard_zero_gate(
        policy_summary[SELECTED_POLICY],
        rows_by_policy[SELECTED_POLICY],
        rules,
    )
    compute = compute_ceiling_gate(model_meter, rules)
    output = output_floor_gate(
        policy_summary[SELECTED_POLICY],
        rows_by_policy[SELECTED_POLICY],
        rules,
    )
    gate_e_passed = all((
        fixed["all_pass"],
        improvement["all_pass"],
        hard["all_pass"],
        compute["all_pass"],
        output["all_pass"],
    ))
    return dict(
        fixed_noninferiority=fixed,
        internal_improvement=improvement,
        hard_zero=hard,
        compute_ceiling=compute,
        unsupported_assertion_floor=output,
        gate_e_passed=bool(gate_e_passed),
        formal_outcome=(
            "GATE_E_PASSED"
            if gate_e_passed
            else "GATE_E_NOT_PASSED_VALID_NEGATIVE"
        ),
    )


def measurement_complete(policy_summary, family_summary, episode_rows, model_meter):
    row_counts = Counter(r.get("policy_id") for r in episode_rows)
    pair_counts = Counter((r.get("policy_id"), r.get("case_id")) for r in episode_rows)
    return (
        set(policy_summary) == set(POLICY_IDS)
        and set(family_summary) == set(POLICY_IDS)
        and set(row_counts) == set(POLICY_IDS)
        and all(row_counts[p] == 144 for p in POLICY_IDS)
        and len(episode_rows) == 432
        and all(count == 1 for count in pair_counts.values())
        and len(pair_counts) == 432
        and all(policy_summary[p]["episodes"] == 144 for p in POLICY_IDS)
        and all(set(family_summary[p]) == set(c211.FAMILIES) for p in POLICY_IDS)
        and all(
            family_summary[p][family]["episodes"] == 16
            for p in POLICY_IDS for family in c211.FAMILIES
        )
        and model_meter.get("policy_id") == SELECTED_POLICY
        and model_meter.get("initial_rows") == 144
        and model_meter.get("inference_rows")
            == model_meter.get("initial_rows") + model_meter.get("post_rows")
        and policy_summary[SELECTED_POLICY]["inference_rows"] == model_meter["inference_rows"]
        and policy_summary[SELECTED_POLICY]["inference_forward_calls"]
            == model_meter["inference_forward_calls"]
        and policy_summary[SELECTED_POLICY]["inference_cell_calls"]
            == model_meter["inference_cell_calls"]
    )


def precheck(
    c211_summary,c210_summary,c209_summary,c208_summary,c207_summary,c206_summary,
    c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,
    c199_summary,c174_summary,c181_summary,c188_summary,root
):
    root = Path(root)
    p210,_,pins,protected = c211.precheck(
        c210_summary,c209_summary,c208_summary,c207_summary,c206_summary,c205_summary,
        c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,c199_summary,
        c174_summary,c181_summary,c188_summary,root
    )
    require(audit.sha(c211_summary) == PARENT_C211_SHA, "C211 summary changed")
    p211 = audit.read_json(c211_summary)
    c211.validate_result(p211)
    require(
        p211.get("commit_sha") == PARENT_C211_EXECUTION
        and p211.get("status") == "PASS"
        and c211.gate(
            p211["validation_summary"],p211["candidate"],p211["decision_rules"]
        )
        and p211.get("source_blobs") == pins
        and p211.get("holdout_evaluated") is False
        and p211.get("model_forward_calls") == 0
        and p211.get("baseline_policy_calls") == 0
        and p211.get("candidate",{}).get("policy_id") == SELECTED_POLICY
        and p211.get("candidate",{}).get("base_checkpoint_sha256") == BASE_CHECKPOINT_SHA
        and p211.get("candidate",{}).get("selector_checkpoint_sha256") == SELECTOR_CHECKPOINT_SHA,
        "Wrong accepted C211 parent",
    )
    protected[str(Path(c211_summary).resolve())] = PARENT_C211_SHA

    artifact_paths = {}
    for artifact in p211["artifacts"]:
        name = artifact["file"]
        path = audit.safe_child(Path(c211_summary).resolve().parent,name)
        require(
            name in C211_ARTIFACT_SHA
            and C211_ARTIFACT_SHA[name] == artifact["sha256"]
            and path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C211 artifact:" + name,
        )
        artifact_paths[name] = path
        protected[str(path.resolve())] = artifact["sha256"]
    require(set(artifact_paths) == set(C211_ARTIFACT_SHA), "C211 artifact set drift")

    deciding = audit.read_json(artifact_paths["deciding-manifest.json"])
    rules = audit.read_json(artifact_paths["decision-rules.json"])
    require(
        rules == p211["decision_rules"] == c211.decision_rules()
        and deciding.get("candidate") == p211["candidate"]
        and deciding.get("decision_rules") == rules
        and deciding.get("holdout",{}).get("visible_sha256") == HOLDOUT_VISIBLE_SHA
        and deciding.get("holdout",{}).get("scorer_sha256") == HOLDOUT_SCORER_SHA
        and deciding.get("holdout",{}).get("units_sha256") == HOLDOUT_UNITS_SHA
        and p211.get("holdout_visible_sha256") == HOLDOUT_VISIBLE_SHA
        and p211.get("holdout_scorer_sha256") == HOLDOUT_SCORER_SHA
        and p211.get("holdout_units_sha256") == HOLDOUT_UNITS_SHA
        and p211.get("deciding_manifest_sha256") == DECIDING_MANIFEST_SHA,
        "Frozen C211 deciding contract drift",
    )

    pins = dict(pins)
    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    pins.update({name:allpins[name] for name in OWN})

    require(len(pins) == 99 and len(protected) == 189,
            "C212 source/protection count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C212 manifest drift")
    return p211,artifact_paths,pins,protected


def regression_modules(root):
    names = c211.regression_modules(root)
    require(len(names) == len(set(names)) == 96, "Historical regression module drift")
    return names + ["tests_lm.test_v05_c212_deciding_holdout_execution"]


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
        len(tests) == 2056
        and len(kept) == 2055
        and not any(
            test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
            for test in kept
        ),
        "C212 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True
        and payload["holdout_execution_complete"] is True,
        "Wrong/incomplete C212",
    )
    require(
        len(payload["source_blobs"]) == 99
        and len(payload["input_sha256"]) == 189
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C212 coverage drift",
    )
    require(
        payload["holdout_evaluated"] is True
        and payload["holdout_execution_count"] == 1
        and payload["policy_episode_evaluations"] == 432
        and payload["training_steps"] == 0
        and payload["fresh_seed_count"] == 0
        and payload["network_calls"] == 0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_deciding_execution"] is True,
        "C212 scope drift",
    )
    require(
        measurement_complete(
            payload["policy_summary"],
            payload["family_summary"],
            payload["episode_results"],
            payload["candidate_model_meter"],
        ),
        "C212 deciding measurement incomplete",
    )
    require(
        payload["decision"]["gate_e_passed"] is payload["gate_e_passed"]
        and payload["status"] == ("PASS" if payload["gate_e_passed"] else "FAIL")
        and payload["formal_outcome"] == payload["decision"]["formal_outcome"],
        "C212 verdict drift",
    )


def run(
    *,c211_summary,c210_summary,c209_summary,c208_summary,c207_summary,c206_summary,
    c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,
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
    p211,artifact_paths,pins,protected = precheck(
        c211_summary,c210_summary,c209_summary,c208_summary,c207_summary,c206_summary,
        c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,
        c199_summary,c174_summary,c181_summary,c188_summary,root
    )
    visible = audit.read_json(artifact_paths["holdout-visible.json"])
    scorer = audit.read_json(artifact_paths["holdout-scorer.json"])
    units = audit.read_json(artifact_paths["holdout-units.json"])
    rules = audit.read_json(artifact_paths["decision-rules.json"])
    require(
        len(visible) == len(scorer) == 144 and len(units) == 72,
        "Frozen holdout size drift",
    )
    scorer_by = {row["case_id"]:row for row in scorer}
    require(
        len(scorer_by) == 144 and all(v["case_id"] in scorer_by for v in visible),
        "Frozen holdout scorer alignment drift",
    )
    scorer_order = [scorer_by[v["case_id"]] for v in visible]

    def new_envs():
        return [c210.build_environment(v,s) for v,s in zip(visible,scorer_order,strict=True)]

    internal_rows = c210.attach_scores(
        [c210.internal_only_policy(env) for env in new_envs()],
        visible,scorer_order,
    )
    fixed_rows = c210.attach_scores(
        [c210.fixed_acquisition_policy(env) for env in new_envs()],
        visible,scorer_order,
    )

    c210.torch.set_num_threads(2)
    c210.torch.use_deterministic_algorithms(True)
    bases,selectors = c210.c204.restore_models(Path(c181_summary),Path(c188_summary))
    candidate_raw,model_meter = c210.candidate_pair_policy(
        new_envs(),
        bases[SELECTED_BASE_SEED],
        selectors[SELECTED_BASE_SEED,SELECTED_HEAD_SEED],
        SELECTED_BASE_SEED,
        SELECTED_HEAD_SEED,
    )
    candidate_rows = c210.attach_scores(candidate_raw,visible,scorer_order)

    rows_by_policy = {
        c210.POLICY_INTERNAL: internal_rows,
        c210.POLICY_FIXED: fixed_rows,
        SELECTED_POLICY: candidate_rows,
    }
    episode_rows = (
        internal_rows + fixed_rows + candidate_rows
    )
    policy_summary = {
        pid:c210.summarize_policy(rows)
        for pid,rows in rows_by_policy.items()
    }
    policy_summary[SELECTED_POLICY]["inference_forward_calls"] = int(
        model_meter["inference_forward_calls"]
    )
    policy_summary[SELECTED_POLICY]["inference_cell_calls"] = int(
        model_meter["inference_cell_calls"]
    )
    family_summary = {
        pid:c210.summarize_families(rows)
        for pid,rows in rows_by_policy.items()
    }

    require(
        measurement_complete(policy_summary,family_summary,episode_rows,model_meter),
        "C212 holdout evaluation incomplete",
    )
    decision = build_decision(
        policy_summary,family_summary,rows_by_policy,model_meter,rules
    )

    out = Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    artifacts = []

    def record(name):
        path = out/name
        artifacts.append(dict(
            file=name,sha256=audit.sha(path),serialized_bytes=path.stat().st_size
        ))

    def save(name,value):
        (out/name).write_bytes(blob(value))
        record(name)

    save("execution-plan.json",dict(
        manifest(),
        source_blobs=pins,
        parent_deciding_manifest_sha256=DECIDING_MANIFEST_SHA,
        frozen_decision_rules=rules,
    ))
    save("episode-results.json",episode_rows)
    save("policy-summary.json",policy_summary)
    save("family-summary.json",family_summary)
    save("gate-e-decision.json",decision)

    guard()
    precheck(
        c211_summary,c210_summary,c209_summary,c208_summary,c207_summary,c206_summary,
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

    gate_e_passed = bool(decision["gate_e_passed"])
    result = dict(
        experiment_id=EXPERIMENT_ID,
        stage=STAGE,
        commit_sha=expected_head,
        status="PASS" if gate_e_passed else "FAIL",
        formal_outcome=decision["formal_outcome"],
        diagnostic_execution_valid=True,
        holdout_execution_complete=True,
        C211_summary_sha256=PARENT_C211_SHA,
        deciding_manifest_sha256=DECIDING_MANIFEST_SHA,
        decision_rules_sha256=DECISION_RULES_SHA,
        holdout_visible_sha256=HOLDOUT_VISIBLE_SHA,
        holdout_scorer_sha256=HOLDOUT_SCORER_SHA,
        holdout_units_sha256=HOLDOUT_UNITS_SHA,
        source_blobs=pins,
        input_sha256=protected,
        artifacts=artifacts,
        episode_results=episode_rows,
        policy_summary=policy_summary,
        family_summary=family_summary,
        candidate_model_meter=model_meter,
        decision=decision,
        gate_e_passed=gate_e_passed,
        holdout_evaluated=True,
        holdout_execution_count=1,
        policy_episode_evaluations=len(episode_rows),
        model_forward_calls=int(model_meter["inference_forward_calls"]),
        baseline_policy_calls=288,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_deciding_execution=True,
        limitations=[
            "selected candidate and all decision rules were frozen before this holdout execution",
            "shared symbolic verifier remains part of every policy answer boundary",
            "guarded unsupported-assertion reduction versus INTERNAL_ONLY remains not demonstrated at zero floor",
            "a valid scientific failure is final negative evidence for this frozen Gate E registration",
        ],
    )
    validate_result(result)
    (out/"summary.json").write_bytes(blob(result))
    print(
        f"[C212] deciding holdout complete gate_e_passed={gate_e_passed} "
        f"candidate_correct={policy_summary[SELECTED_POLICY]['correct']} "
        f"fixed_correct={policy_summary[c210.POLICY_FIXED]['correct']} "
        f"internal_correct={policy_summary[c210.POLICY_INTERNAL]['correct']}",
        flush=True,
    )
    print("=== C212 RESULT ===",flush=True)
    print(blob(result).decode(),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in (
        "c211-summary","c210-summary","c209-summary","c208-summary","c207-summary",
        "c206-summary","c205-summary","c204-summary","c203-summary","c202-summary",
        "c201-summary","c200-summary","c199-summary","c174-summary","c181-summary",
        "c188-summary","output-dir",
    ):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
