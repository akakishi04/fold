"""C207: freeze a leakage-free nine-family Gate-E development fixture manifest.

No candidate or baseline is executed. This experiment validates only that all nine Gate-E v0.1
families can be represented with existing structured-v1/v2 schemas and runtime metadata while
hidden source values, semantic conclusions, necessity/action labels and fault outcomes remain
strictly scorer-only.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import unittest

from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_e_c206_terminal_derived_result_integration as c206

EXPERIMENT_ID = "C207-v5e-nine-family-development-manifest"
STAGE = "V5-E-NINE-FAMILY-DEVELOPMENT-MANIFEST"
BASE = "4230eb6fa9bf780e34915975dd9989b756a4a098"
PARENT_C206_EXECUTION = "814dd2b51a1ff03011aeb609eae1cd75041f1428"
PARENT_C206_SHA = "1fd274cc8d8686b7779838df2f62670da52ddeb87f01a026b4d96cbf62db7553"
MANIFEST_SHA = "d9d3ea599b19f1c7fa91af9e1d0a96287391ae8d4ea88b91449cb5ad4ff61f72"

FAMILIES = (
    "sufficient_known",
    "answer_critical_hidden",
    "conclusion_irrelevant_missing",
    "conflicting_evidence",
    "stale_evidence",
    "noisy_malformed_evidence",
    "unavailable_acquisition",
    "sufficient_reasoning_hard",
    "user_only_information",
)
UNITS_PER_FAMILY = 8
CONDITIONS = (0, 1)
PAIR_VISIBLE_EQUAL = {
    "answer_critical_hidden",
    "conclusion_irrelevant_missing",
    "conflicting_evidence",
    "stale_evidence",
    "noisy_malformed_evidence",
    "user_only_information",
}
FAULTS = (
    "NONE",
    "MALFORMED_PAYLOAD",
    "MISSING_DELIVERY",
    "PERMISSION_DENIED",
    "BUDGET_EXHAUSTED",
)
OWN = (
    "fold_lm/v05_benchmarks/gate_e_c207_nine_family_development_manifest.py",
    "tests_lm/test_v05_c207_nine_family_development_manifest.py",
    "tools/run_c207.ps1",
    "tools/invoke_c207.ps1",
    "docs/experiment-ledger-addendum-c207-preregistration.md",
    "docs/nine-family-development-manifest-v0.1.md",
)
OUTPUTS = {
    "development-manifest.json",
    "development-visible.json",
    "development-scorer.json",
    "dependence-units.json",
    "validation-summary.json",
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
        parent_c206_execution=PARENT_C206_EXECUTION,
        parent_c206_sha256=PARENT_C206_SHA,
        split="development",
        independent_holdout_created=False,
        families=list(FAMILIES),
        units_per_family=8,
        conditions_per_unit=2,
        dependence_units=72,
        episodes=144,
        episodes_per_family=16,
        visible_schema=v2.SCHEMA,
        scorer_separation=(
            "hidden source values, semantic conclusions, necessity/action labels and fault "
            "outcomes are scorer-only and never serialized into visible packets"
        ),
        expression_inventory=[
            "FACT(A)",
            "A_OR_B",
            "A_AND_B",
            "(A_AND_B)_OR_(C_AND_D)",
            "A_OR_(B_AND_(C_OR_D))",
        ],
        registered_faults=list(FAULTS),
        registered_channels=list(v2.CHANNELS),
        candidate_measurement=False,
        baseline_measurement=False,
        numerical_margin_registration=False,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        scope=(
            "development fixture/split manifest only; not a baseline result, holdout, "
            "or Gate E verdict"
        ),
    )


def _resources(channel=None, *, permitted=True, acquisitions=1):
    available = [False, False, False]
    permissions = [False, False, False]
    if channel is not None:
        idx = v2.CHANNELS.index(channel)
        available[idx] = True
        permissions[idx] = bool(permitted)
    return v1.Resources(
        internal_remaining=13,
        acquisitions_remaining=acquisitions,
        available=tuple(available),
        permitted=tuple(permissions),
        last_outcome="NONE",
        internal_step=7,
    )


def _channels(count, fact_index=None, channel=None):
    rows = []
    for i in range(count):
        flags = [False, False, False]
        if i == fact_index and channel is not None:
            flags[v2.CHANNELS.index(channel)] = True
        rows.append(v2.FactChannels(tuple(flags)))
    return tuple(rows)


def _simple_nodes(kind):
    require(kind in ("AND", "OR"), "Simple binary kind required")
    return (
        v1.Node("FACT", 0),
        v1.Node("FACT", 1),
        v1.Node(kind, left=0, right=1),
    )


def _hard_nodes(unit):
    if unit % 2 == 0:
        return (
            v1.Node("FACT", 0),
            v1.Node("FACT", 1),
            v1.Node("AND", left=0, right=1),
            v1.Node("FACT", 2),
            v1.Node("FACT", 3),
            v1.Node("AND", left=3, right=4),
            v1.Node("OR", left=2, right=5),
        )
    return (
        v1.Node("FACT", 0),
        v1.Node("FACT", 1),
        v1.Node("FACT", 2),
        v1.Node("FACT", 3),
        v1.Node("OR", left=2, right=3),
        v1.Node("AND", left=1, right=4),
        v1.Node("OR", left=0, right=5),
    )


def evaluate(nodes, bits):
    stack = []
    for node in nodes:
        if node.kind == "FACT":
            stack.append(int(bits[node.fact]) ^ int(node.negate))
        elif node.kind == "AND":
            stack.append(stack[node.left] & stack[node.right])
        else:
            stack.append(stack[node.left] | stack[node.right])
    return int(stack[-1])


def _fact(fid, status="UNOBSERVED", value=None, refs=()):
    return v1.Fact(fid, status, value, tuple(refs))


def _base_view(case_id, nodes, facts, resources):
    unit_id = case_id.rsplit("-c", 1)[0]
    scope = "C207|" + unit_id
    return v1.TaskView(
        scope + "|query",
        scope,
        tuple(nodes),
        tuple(facts),
        resources,
        evidence_time=1,
        revision=1,
    )


def _binary_hidden_case(family, unit, condition, *, relevance, status, channel):
    kind = "OR" if unit % 2 == 0 else "AND"
    control = (
        0 if (kind == "OR" and relevance == "critical") else
        1 if (kind == "AND" and relevance == "critical") else
        1 if kind == "OR" else
        0
    )
    case_id = f"{family}-u{unit:02d}-c{condition}"
    unit_id = f"{family}-u{unit:02d}"
    refs = ()
    if status == "STALE":
        refs = (f"stale:{unit_id}:B",)
    elif status == "CONFLICT":
        refs = (f"conflict:{unit_id}:B:0", f"conflict:{unit_id}:B:1")
    facts = (
        _fact("A", "OBSERVED", control, (f"initial:{unit_id}:A",)),
        _fact("B", status, None, refs),
    )
    view = _base_view(case_id, _simple_nodes(kind), facts, _resources(channel))
    typed = v2.TaskView(view, _channels(2, 1, channel))
    source_value = int(condition)
    conclusion = evaluate(view.nodes, (control, source_value))
    return typed, dict(
        source_value=source_value,
        semantic_conclusion=conclusion,
        answerable_with_budget=True,
        necessary_fact_indices=[1] if relevance == "critical" else [],
        unnecessary_fact_indices=[] if relevance == "critical" else [1],
        expected_proposal=channel if relevance == "critical" else "ANSWER",
        expected_terminal="ANSWER",
        fault="NONE",
    )


def make_case(family, unit, condition):
    require(family in FAMILIES, "Unknown family")
    require(type(unit) is int and 0 <= unit < UNITS_PER_FAMILY, "Unit out of range")
    require(condition in CONDITIONS, "Condition out of range")
    case_id = f"{family}-u{unit:02d}-c{condition}"

    if family == "sufficient_known":
        bit = int(condition)
        view = _base_view(
            case_id,
            (v1.Node("FACT", 0),),
            (_fact("A", "OBSERVED", bit, (f"initial:{family}-u{unit:02d}:A",)),),
            _resources(),
        )
        typed = v2.TaskView(view, _channels(1))
        oracle = dict(
            source_value=None,
            semantic_conclusion=bit,
            answerable_with_budget=True,
            necessary_fact_indices=[],
            unnecessary_fact_indices=[],
            expected_proposal="ANSWER",
            expected_terminal="ANSWER",
            fault="NONE",
        )

    elif family == "answer_critical_hidden":
        typed, oracle = _binary_hidden_case(
            family, unit, condition,
            relevance="critical", status="UNOBSERVED", channel="RETRIEVE",
        )

    elif family == "conclusion_irrelevant_missing":
        typed, oracle = _binary_hidden_case(
            family, unit, condition,
            relevance="irrelevant", status="UNOBSERVED", channel="RETRIEVE",
        )

    elif family == "conflicting_evidence":
        typed, oracle = _binary_hidden_case(
            family, unit, condition,
            relevance="critical", status="CONFLICT", channel="OBSERVE",
        )

    elif family == "stale_evidence":
        typed, oracle = _binary_hidden_case(
            family, unit, condition,
            relevance="critical", status="STALE", channel="OBSERVE",
        )

    elif family == "noisy_malformed_evidence":
        kind = "OR" if unit % 2 == 0 else "AND"
        control = 0 if kind == "OR" else 1
        source_value = unit % 2
        facts = (
            _fact("A", "OBSERVED", control, (f"initial:{family}-u{unit:02d}:A",)),
            _fact("B"),
        )
        view = _base_view(case_id, _simple_nodes(kind), facts, _resources("RETRIEVE"))
        typed = v2.TaskView(view, _channels(2, 1, "RETRIEVE"))
        fault = "NONE" if condition == 0 else "MALFORMED_PAYLOAD"
        oracle = dict(
            source_value=source_value,
            semantic_conclusion=(
                evaluate(view.nodes, (control, source_value))
                if fault == "NONE" else None
            ),
            answerable_with_budget=(fault == "NONE"),
            necessary_fact_indices=[1],
            unnecessary_fact_indices=[],
            expected_proposal="RETRIEVE",
            expected_terminal="ANSWER" if fault == "NONE" else "UNRESOLVED",
            fault=fault,
        )

    elif family == "unavailable_acquisition":
        kind = "OR" if unit % 2 == 0 else "AND"
        control = 0 if kind == "OR" else 1
        source_value = unit % 2
        fault = "NONE"
        permitted = True
        acquisitions = 1
        if condition == 1:
            fault = ("PERMISSION_DENIED", "BUDGET_EXHAUSTED", "MISSING_DELIVERY")[unit % 3]
            permitted = fault != "PERMISSION_DENIED"
            acquisitions = 0 if fault == "BUDGET_EXHAUSTED" else 1
        facts = (
            _fact("A", "OBSERVED", control, (f"initial:{family}-u{unit:02d}:A",)),
            _fact("B"),
        )
        view = _base_view(
            case_id,
            _simple_nodes(kind),
            facts,
            _resources("RETRIEVE", permitted=permitted, acquisitions=acquisitions),
        )
        typed = v2.TaskView(view, _channels(2, 1, "RETRIEVE"))
        oracle = dict(
            source_value=source_value,
            semantic_conclusion=(
                evaluate(view.nodes, (control, source_value))
                if fault == "NONE" else None
            ),
            answerable_with_budget=(fault == "NONE"),
            necessary_fact_indices=[1],
            unnecessary_fact_indices=[],
            expected_proposal="RETRIEVE",
            expected_terminal="ANSWER" if fault == "NONE" else "UNRESOLVED",
            fault=fault,
        )

    elif family == "sufficient_reasoning_hard":
        nodes = _hard_nodes(unit)
        bits = (
            (1, 1, 0, 0) if condition == 0 and unit % 2 == 0 else
            (0, 1, 0, 1) if condition == 1 and unit % 2 == 0 else
            (0, 1, 1, 0) if condition == 0 else
            (0, 0, 1, 1)
        )
        facts = tuple(
            _fact(chr(65+i), "OBSERVED", bit, (f"initial:{family}-u{unit:02d}:{chr(65+i)}",))
            for i,bit in enumerate(bits)
        )
        view = _base_view(case_id, nodes, facts, _resources())
        typed = v2.TaskView(view, _channels(4))
        oracle = dict(
            source_value=None,
            semantic_conclusion=evaluate(nodes, bits),
            answerable_with_budget=True,
            necessary_fact_indices=[],
            unnecessary_fact_indices=[],
            expected_proposal="ANSWER",
            expected_terminal="ANSWER",
            fault="NONE",
        )

    elif family == "user_only_information":
        typed, oracle = _binary_hidden_case(
            family, unit, condition,
            relevance="critical", status="UNOBSERVED", channel="ASK_USER",
        )

    else:
        raise AssertionError("unreachable")

    packet = v2.encode(typed)
    require(v2.decode(packet) == typed, "Structured-v2 roundtrip drift")
    visible = dict(
        case_id=case_id,
        unit_id=f"{family}-u{unit:02d}",
        family=family,
        condition=condition,
        packet=asdict(packet),
    )
    scorer = dict(
        case_id=case_id,
        unit_id=visible["unit_id"],
        family=family,
        condition=condition,
        **oracle,
    )
    return visible, scorer


def collect():
    visible = []
    scorer = []
    units = []
    roundtrips = 0
    for family in FAMILIES:
        for unit in range(UNITS_PER_FAMILY):
            case_ids = []
            for condition in CONDITIONS:
                v,s = make_case(family,unit,condition)
                visible.append(v)
                scorer.append(s)
                case_ids.append(v["case_id"])
                packet = v2.PolicyInput(
                    v["packet"]["schema"],
                    tuple(v["packet"]["features"]),
                    v1.Binding(
                        v["packet"]["binding"]["request_id"],
                        v["packet"]["binding"]["scope_id"],
                        tuple(v["packet"]["binding"]["fact_ids"]),
                        tuple(tuple(x) for x in v["packet"]["binding"]["reference_ids"]),
                    ),
                )
                require(v2.encode(v2.decode(packet)) == packet, "Serialized visible roundtrip drift")
                roundtrips += 1
            units.append(dict(
                unit_id=f"{family}-u{unit:02d}",
                family=family,
                cases=case_ids,
            ))
    return visible, scorer, units, roundtrips


def validate_fixture(visible, scorer, units, roundtrips):
    errors = dict(
        duplicate_case_ids=0,
        family_count_errors=0,
        unit_errors=0,
        visible_schema_errors=0,
        scorer_leakage_errors=0,
        pair_errors=0,
        scorer_contract_errors=0,
        hidden_payload_errors=0,
    )
    ids = [row["case_id"] for row in visible]
    if len(ids) != len(set(ids)):
        errors["duplicate_case_ids"] += 1

    family_counts = {family:0 for family in FAMILIES}
    for row in visible:
        family_counts[row["family"]] += 1
        if row["packet"]["schema"] != v2.SCHEMA:
            errors["visible_schema_errors"] += 1
        if set(row) != {"case_id","unit_id","family","condition","packet"}:
            errors["scorer_leakage_errors"] += 1
        text = json.dumps(row, sort_keys=True)
        if any(token in text for token in (
            "source_value","semantic_conclusion","answerable_with_budget",
            "necessary_fact_indices","unnecessary_fact_indices",
            "expected_proposal","expected_terminal","fault",
        )):
            errors["scorer_leakage_errors"] += 1
    errors["family_count_errors"] = sum(
        count != 16 for count in family_counts.values()
    )

    scorer_by = {row["case_id"]:row for row in scorer}
    visible_by = {row["case_id"]:row for row in visible}
    fault_counts = {name:0 for name in FAULTS}
    action_counts = {"ANSWER":0,"RETRIEVE":0,"OBSERVE":0,"ASK_USER":0}
    answerable = 0
    channel_episode_counts = {name:0 for name in v2.CHANNELS}

    for row in scorer:
        if set(row) != {
            "case_id","unit_id","family","condition","source_value",
            "semantic_conclusion","answerable_with_budget","necessary_fact_indices",
            "unnecessary_fact_indices","expected_proposal","expected_terminal","fault",
        }:
            errors["scorer_contract_errors"] += 1
        if row["fault"] not in FAULTS or row["expected_proposal"] not in action_counts:
            errors["scorer_contract_errors"] += 1
            continue
        fault_counts[row["fault"]] += 1
        action_counts[row["expected_proposal"]] += 1
        answerable += int(row["answerable_with_budget"])

        packet = visible_by[row["case_id"]]["packet"]
        features = packet["features"]
        nf = features[1]
        for i in range(nf):
            status_index = features[47 + 4*i]
            present = features[48 + 4*i]
            if status_index != v1.STATUSES.index("OBSERVED")+1 and present != 0:
                errors["hidden_payload_errors"] += 1
        tail = features[v1.FEATURE_WIDTH:]
        for ci,name in enumerate(v2.CHANNELS):
            if any(tail[i*3+ci] for i in range(v1.MAX_FACTS)):
                channel_episode_counts[name] += 1

    if len(units) != 72 or any(len(row["cases"]) != 2 for row in units):
        errors["unit_errors"] += 1

    for unit_row in units:
        c0,c1 = unit_row["cases"]
        v0,v1row = visible_by[c0],visible_by[c1]
        s0,s1 = scorer_by[c0],scorer_by[c1]
        family = unit_row["family"]
        equal_visible = v0["packet"] == v1row["packet"]

        if family in PAIR_VISIBLE_EQUAL and not equal_visible:
            errors["pair_errors"] += 1
        if family == "unavailable_acquisition":
            expected_equal = (s1["fault"] == "MISSING_DELIVERY")
            if equal_visible != expected_equal:
                errors["pair_errors"] += 1
        if family in ("sufficient_known","sufficient_reasoning_hard") and equal_visible:
            errors["pair_errors"] += 1

        if family in (
            "answer_critical_hidden","conclusion_irrelevant_missing",
            "conflicting_evidence","stale_evidence","user_only_information",
        ):
            if (s0["source_value"],s1["source_value"]) != (0,1):
                errors["pair_errors"] += 1
        if family == "answer_critical_hidden" and s0["semantic_conclusion"] == s1["semantic_conclusion"]:
            errors["pair_errors"] += 1
        if family == "conclusion_irrelevant_missing" and s0["semantic_conclusion"] != s1["semantic_conclusion"]:
            errors["pair_errors"] += 1

    summary = dict(
        episodes=len(visible),
        dependence_units=len(units),
        roundtrips=roundtrips,
        family_counts=family_counts,
        fault_counts=fault_counts,
        action_counts=action_counts,
        answerable_with_budget=answerable,
        channel_episode_counts=channel_episode_counts,
        errors=errors,
        failed_checks=sum(errors.values()),
        independent_holdout_created=False,
    )
    return summary


def gate(summary):
    return (
        summary.get("episodes") == 144
        and summary.get("dependence_units") == 72
        and summary.get("roundtrips") == 144
        and summary.get("family_counts") == {family:16 for family in FAMILIES}
        and summary.get("fault_counts") == {
            "NONE":128,
            "MALFORMED_PAYLOAD":8,
            "MISSING_DELIVERY":2,
            "PERMISSION_DENIED":3,
            "BUDGET_EXHAUSTED":3,
        }
        and summary.get("action_counts") == {
            "ANSWER":48,
            "RETRIEVE":48,
            "OBSERVE":32,
            "ASK_USER":16,
        }
        and summary.get("answerable_with_budget") == 128
        and summary.get("channel_episode_counts") == {
            "RETRIEVE":64,
            "OBSERVE":32,
            "ASK_USER":16,
        }
        and summary.get("failed_checks") == 0
        and summary.get("independent_holdout_created") is False
    )


def precheck(
    c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,
    c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
):
    root = Path(root)
    p205,c199,prediction_path,c174_result,pilot_path,pins,protected = c206.precheck(
        c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,
        c199_summary,c174_summary,c181_summary,c188_summary,root
    )
    require(audit.sha(c206_summary) == PARENT_C206_SHA, "C206 summary changed")
    p206 = audit.read_json(c206_summary)
    c206.validate_result(p206)
    require(
        p206.get("commit_sha") == PARENT_C206_EXECUTION
        and p206.get("status") == "PASS"
        and c206.gate(p206["block_records"],p206["summary"])
        and p206.get("source_blobs") == pins,
        "Wrong accepted C206 parent",
    )
    protected[str(Path(c206_summary).resolve())] = PARENT_C206_SHA
    for artifact in p206["artifacts"]:
        path = audit.safe_child(Path(c206_summary).resolve().parent,artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C206 artifact:" + artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]

    pins = dict(pins)
    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    pins.update({name:allpins[name] for name in OWN})

    require(len(pins) == 62 and len(protected) == 122,
            "C207 source/protection count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C207 manifest drift")
    return p206,c199,prediction_path,c174_result,pilot_path,pins,protected


def regression_modules(root):
    names = c206.regression_modules(root)
    require(len(names) == len(set(names)) == 91, "Historical regression module drift")
    return names + ["tests_lm.test_v05_c207_nine_family_development_manifest"]


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
        len(tests) == 1930
        and len(kept) == 1929
        and not any(
            test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
            for test in kept
        ),
        "C207 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C207",
    )
    require(
        len(payload["source_blobs"]) == 62
        and len(payload["input_sha256"]) == 122
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C207 coverage drift",
    )
    require(
        payload["training_steps"] == 0
        and payload["fresh_seed_count"] == 0
        and payload["network_calls"] == 0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False
        and payload["candidate_measurement"] is False
        and payload["baseline_measurement"] is False,
        "C207 scope drift",
    )
    require(
        payload["status"] == ("PASS" if gate(payload["summary"]) else "FAIL"),
        "C207 gate drift",
    )


def run(
    *,c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,
    c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,
    output_dir,expected_head
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
    _,_,_,_,_,pins,protected = precheck(
        c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,
        c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
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

    save("development-manifest.json",dict(manifest(),source_blobs=pins))
    try:
        visible,scorer,units,roundtrips = collect()
        summary = validate_fixture(visible,scorer,units,roundtrips)

        save("development-visible.json",visible)
        save("development-scorer.json",scorer)
        save("dependence-units.json",units)
        save("validation-summary.json",summary)

        guard()
        precheck(
            c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,
            c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
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
            status="PASS" if gate(summary) else "FAIL",
            diagnostic_execution_valid=True,
            C206_summary_sha256=PARENT_C206_SHA,
            source_blobs=pins,
            input_sha256=protected,
            artifacts=artifacts,
            summary=summary,
            visible_sha256=audit.sha(out/"development-visible.json"),
            scorer_sha256=audit.sha(out/"development-scorer.json"),
            units_sha256=audit.sha(out/"dependence-units.json"),
            training_steps=0,
            fresh_seed_count=0,
            network_calls=0,
            production_runtime_modified=False,
            gate_e_candidate=False,
            candidate_measurement=False,
            baseline_measurement=False,
            limitations=[
                "development fixtures only; no independent holdout created",
                "scorer labels/fault outcomes are evaluator-only",
                "no candidate or baseline performance measured",
                "no numerical Gate E margins registered",
                "does not establish final Gate E readiness by itself",
            ],
        )
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C207] nine-family development manifest collected",flush=True)
        print("=== C207 RESULT ===",flush=True)
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
        "c206-summary","c205-summary","c204-summary","c203-summary","c202-summary",
        "c201-summary","c200-summary","c199-summary","c174-summary","c181-summary",
        "c188-summary","output-dir",
    ):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
