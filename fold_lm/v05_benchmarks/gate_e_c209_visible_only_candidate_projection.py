"""C209: visible-only candidate projection feasibility over the frozen C207 development manifest.

Intervention: project each general structured-v2 visible TaskView into the legacy frozen candidate
four-fact/seven-node model-input contract without scorer data or trusted runtime mutation.

No learned forward. The deciding controls are exhaustive Boolean semantic equivalence, original
fact-index preservation, dummy-target exclusion, exact C178/C188 validator acceptance, pair
equality preservation, and source-view immutability.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import unittest

import torch

from fold_lm.v05 import candidate_input_projection as projection
from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as c178
from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as c188
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_e_c208_candidate_input_compatibility_preflight as c208

EXPERIMENT_ID = "C209-v5e-visible-only-candidate-projection"
STAGE = "V5-E-VISIBLE-ONLY-CANDIDATE-PROJECTION"
BASE = "390e7dc545dfde12869bea14a05174bc830c249e"
PARENT_C208_EXECUTION = "60d7b38bd0d44662f58b55b32cb09c4d9472f8fe"
PARENT_C208_SHA = "413e88c73c9f7af5403f8f4afa13d9b9245d3201788c41bb5713abc6d7125dc4"
VISIBLE_SHA = "c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543"
MANIFEST_SHA = "c6faab8b8b74fdf6b15dc7dbe3481def184e0dbdb04859a0b9e9ff90660b3879"
OWN = (
    "fold_lm/v05/candidate_input_projection.py",
    "fold_lm/v05_benchmarks/gate_e_c209_visible_only_candidate_projection.py",
    "tests_lm/test_v05_c209_visible_only_candidate_projection.py",
    "tools/run_c209.ps1",
    "tools/invoke_c209.ps1",
    "docs/experiment-ledger-addendum-c209-preregistration.md",
    "docs/visible-only-candidate-projection-v0.1.md",
)
OUTPUTS = {
    "projection-plan.json",
    "case-projections.json",
    "family-projections.json",
    "semantic-controls.json",
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
        parent_c208_execution=PARENT_C208_EXECUTION,
        parent_c208_sha256=PARENT_C208_SHA,
        frozen_visible_sha256=VISIBLE_SHA,
        episodes=144,
        families=9,
        projection_schema=projection.SCHEMA,
        projection_rule=(
            "preserve original fact indices; normalize non-OBSERVED to UNOBSERVED in model "
            "projection; append OBSERVED TRUE constants; wrap root with AND TRUE until four "
            "facts/seven nodes"
        ),
        semantic_control=(
            "exhaustive truth-table equivalence over every original fact completion with padding "
            "constants fixed TRUE"
        ),
        expected_original_fact_counts={"1":16,"2":112,"4":16},
        expected_dummy_facts_total=272,
        expected_status_normalizations=32,
        expected_semantic_assignments=736,
        expected_equal_visible_units=50,
        model_forward_calls=0,
        scorer_used=False,
        trusted_runtime_mutated=False,
        candidate_interface_projection_added=True,
        baseline_measurement=False,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        scope=(
            "projection feasibility/semantics only; not candidate quality, baseline measurement "
            "or final Gate E"
        ),
    )


def packet_from_record(row):
    return c208.packet_from_record(row)


def _eval(nodes, bits):
    state = []
    for node in nodes:
        if node.kind == "FACT":
            state.append(int(bits[node.fact]) ^ int(node.negate))
        elif node.kind == "AND":
            state.append(state[node.left] & state[node.right])
        else:
            state.append(state[node.left] | state[node.right])
    return int(state[-1])


def _packet_sha(packet):
    return hashlib.sha256(
        json.dumps(asdict(packet), sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


def analyze_record(row):
    require(set(row) == {"case_id","unit_id","family","condition","packet"},
            "Unexpected C207 visible record schema")
    source_packet = packet_from_record(row)
    source_view = v2.decode(source_packet)
    before = asdict(source_packet)
    projected = projection.project(source_view)
    projected_view = v1.decode(projected.packet)
    after = asdict(v2.encode(source_view))

    source_unchanged = before == after
    source_digest_match = projected.source_v2_sha256 == projection.source_digest(source_view)
    raw = torch.tensor([projected.packet.features], dtype=torch.int32)

    necessity_ok = True
    target_ok = True
    try:
        c178.prepare_pair(raw)
    except ValueError:
        necessity_ok = False
    try:
        missing = c188.missing_mask(raw)
        c188.leaf_positions(raw)
    except ValueError:
        target_ok = False
        missing = None

    n = projected.original_fact_count
    mapping_ok = (
        projected.projected_to_original[:n] == tuple(range(n))
        and all(x == -1 for x in projected.projected_to_original[n:])
        and tuple(projected.dummy_fact_indices) == tuple(range(n,4))
    )
    observed_preserved = True
    normalized_nonobserved = True
    for i, original in enumerate(source_view.base.facts):
        current = projected_view.facts[i]
        if original.status == "OBSERVED":
            observed_preserved = observed_preserved and current == original
        else:
            normalized_nonobserved = normalized_nonobserved and (
                current.fact_id == original.fact_id
                and current.status == "UNOBSERVED"
                and current.value is None
                and current.reference_ids == ()
            )

    dummy_ok = True
    dummy_missing_errors = 0
    for i in projected.dummy_fact_indices:
        fact = projected_view.facts[i]
        dummy_ok = dummy_ok and (
            fact.fact_id == f"{projection.DUMMY_PREFIX}{i}"
            and fact.status == "OBSERVED"
            and fact.value == 1
            and fact.reference_ids == (f"{projection.DUMMY_REFERENCE_PREFIX}{i}",)
        )
        if missing is not None and bool(missing[0,i].item()):
            dummy_missing_errors += 1

    semantic_checks = 0
    semantic_errors = 0
    for code in range(1 << n):
        original_bits = tuple((code >> i) & 1 for i in range(n))
        projected_bits = original_bits + (1,) * (4 - n)
        semantic_checks += 1
        if _eval(source_view.base.nodes, original_bits) != _eval(projected_view.nodes, projected_bits):
            semantic_errors += 1

    return dict(
        case_id=row["case_id"],
        unit_id=row["unit_id"],
        family=row["family"],
        condition=row["condition"],
        original_fact_count=n,
        original_node_count=len(source_view.base.nodes),
        projected_fact_count=len(projected_view.facts),
        projected_node_count=len(projected_view.nodes),
        dummy_fact_count=len(projected.dummy_fact_indices),
        normalized_status_changes=projected.normalized_status_changes,
        source_unchanged=source_unchanged,
        source_digest_match=source_digest_match,
        mapping_ok=mapping_ok,
        observed_preserved=observed_preserved,
        normalized_nonobserved=normalized_nonobserved,
        dummy_ok=dummy_ok,
        dummy_missing_errors=dummy_missing_errors,
        semantic_checks=semantic_checks,
        semantic_errors=semantic_errors,
        necessity_compatible=necessity_ok,
        target_compatible=target_ok,
        combined_compatible=bool(necessity_ok and target_ok),
        source_packet_sha256=_packet_sha(source_packet),
        projected_packet_sha256=_packet_sha(projected.packet),
    )


def collect(visible):
    require(type(visible) is list and len(visible) == 144, "Frozen C207 visible cohort required")
    records = [analyze_record(row) for row in visible]
    family = {}
    for name in c208.c207.FAMILIES:
        rows = [r for r in records if r["family"] == name]
        require(len(rows) == 16, "Family coverage drift:" + name)
        family[name] = dict(
            episodes=16,
            compatible=sum(r["combined_compatible"] for r in rows),
            semantic_errors=sum(r["semantic_errors"] for r in rows),
            dummy_facts=sum(r["dummy_fact_count"] for r in rows),
            status_normalizations=sum(r["normalized_status_changes"] for r in rows),
        )

    original_fact_counts = {}
    for n in (1,2,4):
        original_fact_counts[str(n)] = sum(r["original_fact_count"] == n for r in records)

    grouped = {}
    for row,record in zip(visible,records,strict=True):
        grouped.setdefault(row["unit_id"],[]).append((row,record))
    require(len(grouped) == 72 and all(len(rows) == 2 for rows in grouped.values()),
            "Dependence-unit grouping drift")
    equal_source_units = 0
    equal_projected_units = 0
    pair_projection_errors = 0
    for rows in grouped.values():
        (v0,r0),(v1row,r1) = rows
        source_equal = v0["packet"] == v1row["packet"]
        projected_equal = r0["projected_packet_sha256"] == r1["projected_packet_sha256"]
        if source_equal:
            equal_source_units += 1
            equal_projected_units += int(projected_equal)
            pair_projection_errors += int(not projected_equal)

    summary = dict(
        episodes=144,
        families=9,
        original_fact_counts=original_fact_counts,
        dummy_facts_total=sum(r["dummy_fact_count"] for r in records),
        normalized_status_changes=sum(r["normalized_status_changes"] for r in records),
        semantic_assignments=sum(r["semantic_checks"] for r in records),
        semantic_errors=sum(r["semantic_errors"] for r in records),
        source_unchanged=sum(r["source_unchanged"] for r in records),
        source_digest_match=sum(r["source_digest_match"] for r in records),
        mapping_ok=sum(r["mapping_ok"] for r in records),
        observed_preserved=sum(r["observed_preserved"] for r in records),
        normalized_nonobserved=sum(r["normalized_nonobserved"] for r in records),
        dummy_ok=sum(r["dummy_ok"] for r in records),
        dummy_missing_errors=sum(r["dummy_missing_errors"] for r in records),
        necessity_compatible=sum(r["necessity_compatible"] for r in records),
        target_compatible=sum(r["target_compatible"] for r in records),
        combined_compatible=sum(r["combined_compatible"] for r in records),
        equal_source_units=equal_source_units,
        equal_projected_units=equal_projected_units,
        pair_projection_errors=pair_projection_errors,
        model_forward_calls=0,
        scorer_used=False,
        trusted_runtime_mutated=False,
    )
    semantic = dict(
        exhaustive_assignments=summary["semantic_assignments"],
        semantic_errors=summary["semantic_errors"],
        original_fact_counts=original_fact_counts,
        dummy_facts_total=summary["dummy_facts_total"],
        normalized_status_changes=summary["normalized_status_changes"],
        equal_source_units=equal_source_units,
        equal_projected_units=equal_projected_units,
    )
    return records,family,semantic,summary


def gate(summary):
    return (
        summary.get("episodes") == 144
        and summary.get("families") == 9
        and summary.get("original_fact_counts") == {"1":16,"2":112,"4":16}
        and summary.get("dummy_facts_total") == 272
        and summary.get("normalized_status_changes") == 32
        and summary.get("semantic_assignments") == 736
        and summary.get("semantic_errors") == 0
        and summary.get("source_unchanged") == 144
        and summary.get("source_digest_match") == 144
        and summary.get("mapping_ok") == 144
        and summary.get("observed_preserved") == 144
        and summary.get("normalized_nonobserved") == 144
        and summary.get("dummy_ok") == 144
        and summary.get("dummy_missing_errors") == 0
        and summary.get("necessity_compatible") == 144
        and summary.get("target_compatible") == 144
        and summary.get("combined_compatible") == 144
        and summary.get("equal_source_units") == 50
        and summary.get("equal_projected_units") == 50
        and summary.get("pair_projection_errors") == 0
        and summary.get("model_forward_calls") == 0
        and summary.get("scorer_used") is False
        and summary.get("trusted_runtime_mutated") is False
    )


def precheck(
    c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,
    c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,
    c188_summary,root
):
    root = Path(root)
    p207,visible_path,pins,protected = c208.precheck(
        c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,
        c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
    )
    require(audit.sha(c208_summary) == PARENT_C208_SHA, "C208 summary changed")
    p208 = audit.read_json(c208_summary)
    c208.validate_result(p208)
    require(
        p208.get("commit_sha") == PARENT_C208_EXECUTION
        and p208.get("status") == "FAIL"
        and c208.execution_valid(
            p208["summary"],p208["records"],p208["family_compatibility"]
        )
        and not c208.candidate_gate(p208["summary"])
        and p208.get("source_blobs") == pins
        and p208.get("visible_sha256") == VISIBLE_SHA,
        "Wrong accepted-valid-negative C208 parent",
    )
    protected[str(Path(c208_summary).resolve())] = PARENT_C208_SHA
    for artifact in p208["artifacts"]:
        path = audit.safe_child(Path(c208_summary).resolve().parent,artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C208 artifact:" + artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]

    pins = dict(pins)
    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    pins.update({name:allpins[name] for name in OWN})

    require(len(pins) == 77 and len(protected) == 149,
            "C209 source/protection count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C209 manifest drift")
    return p208,visible_path,pins,protected


def regression_modules(root):
    names = c208.regression_modules(root)
    require(len(names) == len(set(names)) == 93, "Historical regression module drift")
    return names + ["tests_lm.test_v05_c209_visible_only_candidate_projection"]


def regression_suite(root):
    names = regression_modules(root)
    loaded = unittest.defaultTestLoader.loadTestsFromNames(names)
    tests = list(c205._iter_tests(loaded))
    ids = [test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded) == 1, "Historical dynamic test identity drift:" + excluded)
    kept = [test for test in tests if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS]
    require(
        len(tests) == 1974
        and len(kept) == 1973
        and not any(test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS for test in kept),
        "C209 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C209",
    )
    require(
        len(payload["source_blobs"]) == 77
        and len(payload["input_sha256"]) == 149
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C209 coverage drift",
    )
    require(
        payload["model_forward_calls"] == 0
        and payload["scorer_used"] is False
        and payload["trusted_runtime_mutated"] is False
        and payload["candidate_interface_projection_added"] is True
        and payload["baseline_measurement"] is False
        and payload["training_steps"] == 0
        and payload["fresh_seed_count"] == 0
        and payload["network_calls"] == 0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False,
        "C209 scope drift",
    )
    require(
        payload["status"] == ("PASS" if gate(payload["summary"]) else "FAIL"),
        "C209 gate drift",
    )


def run(
    *,c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,
    c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,
    c188_summary,output_dir,expected_head
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
    _,visible_path,pins,protected = precheck(
        c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,
        c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,
        c188_summary,root
    )
    visible = audit.read_json(visible_path)

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

    save("projection-plan.json",dict(manifest(),source_blobs=pins))
    try:
        records,family,semantic,summary = collect(visible)
        save("case-projections.json",records)
        save("family-projections.json",family)
        save("semantic-controls.json",semantic)
        save("validation-summary.json",summary)

        guard()
        precheck(
            c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,
            c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,
            c188_summary,root
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
            C208_summary_sha256=PARENT_C208_SHA,
            visible_sha256=VISIBLE_SHA,
            source_blobs=pins,
            input_sha256=protected,
            artifacts=artifacts,
            records=records,
            family_projections=family,
            semantic_controls=semantic,
            summary=summary,
            model_forward_calls=0,
            scorer_used=False,
            trusted_runtime_mutated=False,
            candidate_interface_projection_added=True,
            baseline_measurement=False,
            training_steps=0,
            fresh_seed_count=0,
            network_calls=0,
            production_runtime_modified=False,
            gate_e_candidate=False,
            limitations=[
                "projection feasibility only; no learned forward or quality measurement",
                "non-OBSERVED status distinctions are intentionally collapsed only in model projection",
                "trusted structured-v2 runtime/evidence state remains unchanged",
                "padding TRUE facts are architectural constants, not external observations",
                "not baseline development measurement or final Gate E",
            ],
        )
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C209] visible-only candidate projection collected",flush=True)
        print("=== C209 RESULT ===",flush=True)
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
        "c208-summary","c207-summary","c206-summary","c205-summary","c204-summary",
        "c203-summary","c202-summary","c201-summary","c200-summary","c199-summary",
        "c174-summary","c181-summary","c188-summary","output-dir",
    ):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
