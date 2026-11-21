"""C208: current frozen-candidate input compatibility against the frozen C207 development manifest.

No model forward and no adapter. Apply the actual current C178/C188 input validators to every
frozen C207 visible packet. A valid incompatibility is a scientific negative, not an invalid run.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest

import torch

from fold_lm.v05 import structured_task_input as v1
from fold_lm.v05 import structured_task_input_v2 as v2
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c178_visible_leaf_binding as c178
from fold_lm.v05_benchmarks import gate_e_c188_multimissing_target_selection as c188
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_e_c207_nine_family_development_manifest as c207

EXPERIMENT_ID = "C208-v5e-candidate-input-compatibility-preflight"
STAGE = "V5-E-CANDIDATE-INPUT-COMPATIBILITY-PREFLIGHT"
BASE = "8e1a01c87f3ca94d99c6ae419a832dd95f683303"
PARENT_C207_EXECUTION = "96020d20bd73bf6e2e62d5bfb202b7b2605a2079"
PARENT_C207_SHA = "a7e69871003ac1978e786809c822d75c0dc291cfbe14aa8709f8b12ec26e4477"
VISIBLE_SHA = "c7be54e9686212e06f072e754c75239e8f4261717986e3e933e40f35b4ee0543"
C178_BLOB = "2ec87851f1f75533dd2225243d0c1baeda9c9a2a"
C188_BLOB = "0819bc70377a949fe1c17a66be559336bbda96e1"
MANIFEST_SHA = "52533ba9b2057f791b55cb6d1bafebf2cedfeae0400b5ecbf0f6a661ed77e7d6"
CONTRACT_FILES = {
    "fold_lm/v05_benchmarks/gate_e_c178_visible_leaf_binding.py": C178_BLOB,
    "fold_lm/v05_benchmarks/gate_e_c188_multimissing_target_selection.py": C188_BLOB,
}
OWN = (
    "fold_lm/v05_benchmarks/gate_e_c208_candidate_input_compatibility_preflight.py",
    "tests_lm/test_v05_c208_candidate_input_compatibility_preflight.py",
    "tools/run_c208.ps1",
    "tools/invoke_c208.ps1",
    "docs/experiment-ledger-addendum-c208-preregistration.md",
    "docs/candidate-input-compatibility-preflight-v0.1.md",
)
OUTPUTS = {
    "compatibility-plan.json",
    "case-compatibility.json",
    "family-compatibility.json",
    "constraint-summary.json",
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
        parent_c207_execution=PARENT_C207_EXECUTION,
        parent_c207_sha256=PARENT_C207_SHA,
        frozen_visible_sha256=VISIBLE_SHA,
        episodes=144,
        families=9,
        input="frozen C207 structured-v2 visible packets; learned prefix is exact first72 structured-v1 features",
        necessity_contract="C178 validate_raw/prepare_pair current frozen representation contract",
        target_contract="C188 missing_mask + leaf_positions current frozen selector contract",
        intervention="none; diagnose as-is compatibility only",
        model_forward_calls=0,
        candidate_measurement=False,
        baseline_measurement=False,
        adapter_implementation=False,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        scope="candidate input compatibility preflight only; valid incompatibility is scientific evidence, not execution invalidity",
    )


def packet_from_record(row):
    p = row["packet"]
    packet = v2.PolicyInput(
        p["schema"],
        tuple(p["features"]),
        v1.Binding(
            p["binding"]["request_id"],
            p["binding"]["scope_id"],
            tuple(p["binding"]["fact_ids"]),
            tuple(tuple(x) for x in p["binding"]["reference_ids"]),
        ),
    )
    require(v2.encode(v2.decode(packet)) == packet, "Frozen C207 visible packet roundtrip drift")
    return packet


def _reason(exc):
    text = str(exc).strip()
    require(text and len(text) <= 256, "Unexpected validator exception text")
    return text


def analyze_record(row):
    require(set(row) == {"case_id","unit_id","family","condition","packet"},
            "Unexpected C207 visible record schema")
    packet = packet_from_record(row)
    raw = torch.tensor(
        [packet.features[:v1.FEATURE_WIDTH]],
        dtype=torch.int32,
    )
    require(raw.shape == (1,72), "Candidate prefix width drift")

    header_7_4 = bool(int(raw[0,0]) == 7 and int(raw[0,1]) == 4)
    facts = raw[:,46:62].reshape(1,4,4)
    active_fact_slots = int(facts[0,:,0].sum().item())
    target_status_compatible = bool(
        all(
            int(facts[0,i,1]) in (1,2)
            for i in range(4)
            if int(facts[0,i,0]) == 1
        )
    )
    nodes = raw[:,4:46].reshape(1,7,6)
    active_nodes = nodes[0,:,0] == 1
    active_fact_leaves = int(
        ((nodes[0,:,1] == 1) & active_nodes).sum().item()
    )

    necessity_ok = False
    necessity_reason = None
    try:
        c178.prepare_pair(raw)
        necessity_ok = True
    except ValueError as exc:
        necessity_reason = _reason(exc)

    target_ok = False
    target_reason = None
    try:
        c188.missing_mask(raw)
        c188.leaf_positions(raw)
        target_ok = True
    except ValueError as exc:
        target_reason = _reason(exc)

    return dict(
        case_id=row["case_id"],
        unit_id=row["unit_id"],
        family=row["family"],
        condition=row["condition"],
        header_7_nodes_4_facts=header_7_4,
        active_fact_slots=active_fact_slots,
        active_fact_leaves=active_fact_leaves,
        target_status_compatible=target_status_compatible,
        necessity_compatible=necessity_ok,
        target_compatible=target_ok,
        combined_compatible=bool(necessity_ok and target_ok),
        necessity_rejection=necessity_reason,
        target_rejection=target_reason,
    )


def collect(visible):
    require(type(visible) is list and len(visible) == 144, "Frozen C207 visible cohort required")
    records = [analyze_record(row) for row in visible]
    family = {}
    for name in c207.FAMILIES:
        rows = [r for r in records if r["family"] == name]
        require(len(rows) == 16, "C207 family coverage drift:" + name)
        family[name] = dict(
            episodes=16,
            header_compatible=sum(r["header_7_nodes_4_facts"] for r in rows),
            target_status_compatible=sum(r["target_status_compatible"] for r in rows),
            necessity_compatible=sum(r["necessity_compatible"] for r in rows),
            target_compatible=sum(r["target_compatible"] for r in rows),
            combined_compatible=sum(r["combined_compatible"] for r in rows),
        )

    necessity_reasons = Counter(
        r["necessity_rejection"] for r in records if r["necessity_rejection"] is not None
    )
    target_reasons = Counter(
        r["target_rejection"] for r in records if r["target_rejection"] is not None
    )
    constraints = dict(
        c178=dict(
            exact_header="7 nodes / 4 facts",
            four_fact_leaves=True,
            accepted_fact_statuses=list(v1.STATUSES),
        ),
        c188=dict(
            exact_header="7 nodes / 4 facts",
            four_fact_leaves=True,
            accepted_fact_statuses=["UNOBSERVED","OBSERVED"],
        ),
        observed_source_blobs=CONTRACT_FILES,
    )
    summary = dict(
        episodes=len(records),
        families=len(family),
        header_compatible=sum(r["header_7_nodes_4_facts"] for r in records),
        target_status_compatible=sum(r["target_status_compatible"] for r in records),
        necessity_compatible=sum(r["necessity_compatible"] for r in records),
        target_compatible=sum(r["target_compatible"] for r in records),
        combined_compatible=sum(r["combined_compatible"] for r in records),
        incompatible=len(records)-sum(r["combined_compatible"] for r in records),
        family_compatibility={k:v["combined_compatible"] for k,v in family.items()},
        necessity_rejection_reasons=dict(sorted(necessity_reasons.items())),
        target_rejection_reasons=dict(sorted(target_reasons.items())),
        classified_rows=len(records),
        unexpected_errors=0,
        model_forward_calls=0,
        adapter_used=False,
        scorer_used=False,
    )
    return records,family,constraints,summary


def candidate_gate(summary):
    return (
        summary.get("episodes") == 144
        and summary.get("families") == 9
        and summary.get("classified_rows") == 144
        and summary.get("unexpected_errors") == 0
        and summary.get("combined_compatible") == 144
        and summary.get("incompatible") == 0
        and summary.get("model_forward_calls") == 0
        and summary.get("adapter_used") is False
        and summary.get("scorer_used") is False
    )


def execution_valid(summary, records, family):
    return (
        type(records) is list and len(records) == 144
        and set(family) == set(c207.FAMILIES)
        and all(v.get("episodes") == 16 for v in family.values())
        and summary.get("episodes") == 144
        and summary.get("classified_rows") == 144
        and summary.get("unexpected_errors") == 0
        and summary.get("model_forward_calls") == 0
        and summary.get("adapter_used") is False
        and summary.get("scorer_used") is False
    )


def precheck(
    c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,
    c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
):
    root = Path(root)
    p206,c199,prediction_path,c174_result,pilot_path,pins,protected = c207.precheck(
        c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,
        c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
    )
    require(audit.sha(c207_summary) == PARENT_C207_SHA, "C207 summary changed")
    p207 = audit.read_json(c207_summary)
    c207.validate_result(p207)
    require(
        p207.get("commit_sha") == PARENT_C207_EXECUTION
        and p207.get("status") == "PASS"
        and c207.gate(p207["summary"])
        and p207.get("source_blobs") == pins
        and p207.get("visible_sha256") == VISIBLE_SHA,
        "Wrong accepted C207 parent",
    )
    protected[str(Path(c207_summary).resolve())] = PARENT_C207_SHA
    visible_path = None
    for artifact in p207["artifacts"]:
        path = audit.safe_child(Path(c207_summary).resolve().parent,artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C207 artifact:" + artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]
        if artifact["file"] == "development-visible.json":
            visible_path = path
    require(visible_path is not None and audit.sha(visible_path) == VISIBLE_SHA,
            "C207 visible artifact identity drift")

    pins = dict(pins)
    for rel,wanted in CONTRACT_FILES.items():
        current = audit.git(root,"rev-parse","HEAD:"+rel).decode().strip()
        require(current == wanted, "Candidate input contract source changed:" + rel)
        pins[rel] = wanted

    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    pins.update({name:allpins[name] for name in OWN})

    require(len(pins) == 70 and len(protected) == 136,
            "C208 source/protection count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C208 manifest drift")
    return p207,visible_path,pins,protected


def regression_modules(root):
    names = c207.regression_modules(root)
    require(len(names) == len(set(names)) == 92, "Historical regression module drift")
    return names + ["tests_lm.test_v05_c208_candidate_input_compatibility_preflight"]


def regression_suite(root):
    names = regression_modules(root)
    loaded = unittest.defaultTestLoader.loadTestsFromNames(names)
    tests = list(c205._iter_tests(loaded))
    ids = [test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded) == 1, "Historical dynamic test identity drift:" + excluded)
    kept = [test for test in tests if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS]
    require(
        len(tests) == 1950
        and len(kept) == 1949
        and not any(test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS for test in kept),
        "C208 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C208",
    )
    require(
        len(payload["source_blobs"]) == 70
        and len(payload["input_sha256"]) == 136
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C208 coverage drift",
    )
    require(
        payload["model_forward_calls"] == 0
        and payload["candidate_measurement"] is False
        and payload["baseline_measurement"] is False
        and payload["adapter_implementation"] is False
        and payload["training_steps"] == 0
        and payload["fresh_seed_count"] == 0
        and payload["network_calls"] == 0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False,
        "C208 scope drift",
    )
    require(execution_valid(payload["summary"],payload["records"],payload["family_compatibility"]),
            "C208 classification completeness drift")
    require(
        payload["status"] == ("PASS" if candidate_gate(payload["summary"]) else "FAIL"),
        "C208 scientific gate drift",
    )


def run(
    *,c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,
    c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,
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
    _,visible_path,pins,protected = precheck(
        c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,
        c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
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

    save("compatibility-plan.json",dict(manifest(),source_blobs=pins))
    try:
        records,family,constraints,summary = collect(visible)
        save("case-compatibility.json",records)
        save("family-compatibility.json",family)
        save("constraint-summary.json",constraints)
        save("validation-summary.json",summary)

        guard()
        precheck(
            c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,
            c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
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
            status="PASS" if candidate_gate(summary) else "FAIL",
            diagnostic_execution_valid=True,
            C207_summary_sha256=PARENT_C207_SHA,
            visible_sha256=VISIBLE_SHA,
            source_blobs=pins,
            input_sha256=protected,
            artifacts=artifacts,
            records=records,
            family_compatibility=family,
            constraints=constraints,
            summary=summary,
            model_forward_calls=0,
            candidate_measurement=False,
            baseline_measurement=False,
            adapter_implementation=False,
            training_steps=0,
            fresh_seed_count=0,
            network_calls=0,
            production_runtime_modified=False,
            gate_e_candidate=False,
            limitations=[
                "input-contract compatibility only; no model forward",
                "no representation adapter is introduced",
                "no scorer artifact is loaded or used",
                "valid incompatibility is a scientific negative",
                "not baseline development measurement or final Gate E",
            ],
        )
        validate_result(result)
        (out/"summary.json").write_bytes(blob(result))
        print("[C208] candidate input compatibility preflight collected",flush=True)
        print("=== C208 RESULT ===",flush=True)
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
        "c207-summary","c206-summary","c205-summary","c204-summary","c203-summary",
        "c202-summary","c201-summary","c200-summary","c199-summary","c174-summary",
        "c181-summary","c188-summary","output-dir",
    ):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
