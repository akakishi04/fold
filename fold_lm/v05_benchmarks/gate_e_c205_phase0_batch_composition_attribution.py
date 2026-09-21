"""C205: attribute C204 logit replay miss to phase-0 batch composition.

No runtime actions and no threshold change. For each accepted C181/C188 pair, evaluate the same
phase-0 observable states two ways:

A) canonical unique: 1768 unique PILOT states -> structured-v2 -> exact72 prefix -> frozen inference,
   then expand outputs to9536 worlds using the accepted C199 local_rows map.
B) expanded direct: 9536 world-expanded duplicate states -> structured-v2 -> exact72 prefix ->
   frozen inference directly.

Compare both against the accepted C199 ALLOWED phase-0 reference and compare the expanded-direct
max deltas against the full-loop maxima observed in accepted-valid-negative C204.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import torch

from fold_lm.v05 import structured_action_runtime as action
from fold_lm.v05 import structured_acquisition_lifecycle as life
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c185_single_missing_acquisition as c185
from fold_lm.v05_benchmarks import gate_e_c189_live_multimissing_target as c189
from fold_lm.v05_benchmarks import gate_e_c190_iterative_multimissing_acquisition as c190
from fold_lm.v05_benchmarks import gate_e_c193_budget13_authoritative_closure as c193
from fold_lm.v05_benchmarks import gate_e_c201_selected_fact_channel_route as c201
from fold_lm.v05_benchmarks import gate_e_c203_mixed_channel_multistep_replay as c203
from fold_lm.v05_benchmarks import gate_e_c204_live_v2_mixed_channel_loop as c204

EXPERIMENT_ID = "C205-v5e-phase0-batch-composition-attribution"
STAGE = "V5-E-PHASE0-BATCH-COMPOSITION-ATTRIBUTION"
BASE = "278b88208dbee17f96d1213ccff3d4ab385d1d0b"
PARENT_C204_EXECUTION = "0ef49a4f97b516a00066df4986c062f98fda676d"
PARENT_C204_SHA = "9c02e4dbd497fbc91ae25c02f4cc5a3baad0af8cf9cc296f2bac0f6f8ffe72e9"
REFERENCE_C199_EXECUTION = "48100f36f4f1acdf44d5cb1d508b907e19724c10"
REFERENCE_C199_SHA = "0ee89c9720022146c9625bbe7cd4d02a615c411ff2f3f068d5dac91d5ab906f9"
MANIFEST_SHA = "316f8ec5e4654a321aff67ddf48e067feb29cf786e330697230ad3187e6f8c0c"
BASE_SEEDS = c204.BASE_SEEDS
HEAD_SEEDS = c204.HEAD_SEEDS
ATOL = c204.ATOL
BATCH = c204.BATCH
UNIQUE_ROWS = 1768
EXPANDED_ROWS = 9536
OWN = (
    "fold_lm/v05_benchmarks/gate_e_c205_phase0_batch_composition_attribution.py",
    "tests_lm/test_v05_c205_phase0_batch_composition_attribution.py",
    "tools/run_c205.ps1",
    "tools/invoke_c205.ps1",
    "docs/experiment-ledger-addendum-c205-preregistration.md",
    "docs/phase0-batch-composition-attribution-v0.1.md",
)
OUTPUTS = {
    "attribution-plan.json",
    "canonical-unique.json",
    "expanded-direct.json",
    "c204-max-match.json",
    "workload.json",
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
        parent_c204_execution=PARENT_C204_EXECUTION,
        parent_c204_sha256=PARENT_C204_SHA,
        reference_c199_execution=REFERENCE_C199_EXECUTION,
        reference_c199_sha256=REFERENCE_C199_SHA,
        question="are C204 gate-breaking logit maxima fully attributable to phase0 duplicate-expanded batch composition rather than structured-v2 prefix/state semantics",
        changed="phase0 inference cohort presentation only: canonical1768 unique states versus direct9536 world-expanded duplicate states",
        held="same frozen C181/C188 checkpoints,same current phase0 canonical72 features,same v2 layout,same raw argmax,same BATCH1024,CPU float32,threads2,deterministic algorithms,C199 reference",
        canonical_unique_rows=1768,
        expanded_rows=9536,
        blocks=9,
        canonical_total_rows=15912,
        expanded_total_rows=85824,
        canonical_forward_calls=18,
        expanded_forward_calls=90,
        canonical_cell_calls=126,
        expanded_cell_calls=630,
        atol=ATOL,
        training_steps=0,
        fresh_seed_count=0,
        acquisitions=0,
        network_calls=0,
        production_runtime_modified=False,
        gate_e_candidate=False,
        scope="numeric batch-composition attribution only; no threshold relaxation or runtime action claim",
    )


def reconstruct_phase0_cohort(features, predictions):
    source_rows = predictions["row_indices"].astype(np.int64)
    local_rows = predictions["local_rows"].astype(np.int64)
    world_codes = predictions["world_codes"].astype(np.int64)
    require(
        source_rows.shape == local_rows.shape == world_codes.shape == (EXPANDED_ROWS,),
        "Accepted expanded identity shape drift",
    )
    require(
        int(local_rows.min()) == 0
        and int(local_rows.max()) == UNIQUE_ROWS - 1
        and set(local_rows.tolist()) == set(range(UNIQUE_ROWS)),
        "Accepted local-row domain drift",
    )

    full_ix = np.full(UNIQUE_ROWS, -1, dtype=np.int64)
    for pos, local in enumerate(local_rows):
        if full_ix[local] < 0:
            full_ix[local] = source_rows[pos]
        else:
            require(full_ix[local] == source_rows[pos], "Local/source identity drift")
    require((full_ix >= 0).all(), "Incomplete unique source rows")

    raw12 = torch.from_numpy(features[full_ix].copy())
    raw13 = c193.budget13(raw12)
    expanded12, source2, local2, world2 = c190.expand_worlds(raw12, full_ix)
    require(
        np.array_equal(source2, source_rows)
        and np.array_equal(local2, local_rows)
        and np.array_equal(world2, world_codes),
        "Reconstructed world expansion does not match accepted C199 identity",
    )
    expanded13 = c193.budget13(expanded12)
    return dict(
        full_ix=full_ix,
        raw13=raw13,
        expanded13=expanded13,
        source_rows=source_rows,
        local_rows=local_rows,
        world_codes=world_codes,
    )


def infer_v2_unique(raw13, full_ix, local_rows, base, selector, block_id):
    views = c185.make_views(raw13, full_ix, c185.LAYOUTS[0], block_id)
    owners = [
        life.AcquisitionOwner(action.RuntimeState(view), {}, max_dispatches=3)
        for view in views
    ]
    require(all(c185.charge_decision(owner) for owner in owners),
            "Canonical unique phase0 decision charge failed")
    raw, _, prefix_errors = c204.encode_live_v2(owners, list(range(len(owners))))
    require(len(raw) == UNIQUE_ROWS, "Canonical unique row count drift")
    p, t, z, tz, meter = c189.combined_predict(base, selector, raw, batch=BATCH)
    return dict(
        raw=raw,
        necessity_predictions=p[local_rows].copy(),
        target_predictions=t[local_rows].copy(),
        necessity_logits=z[local_rows].copy(),
        target_logits=tz[local_rows].copy(),
        prefix_errors=prefix_errors,
        meter=meter,
    )


def infer_v2_expanded(expanded13, source_rows, world_codes, base, selector, block_id):
    views = c190.make_views(expanded13, source_rows, world_codes, block_id)
    owners = [
        life.AcquisitionOwner(action.RuntimeState(view), {}, max_dispatches=3)
        for view in views
    ]
    require(all(c185.charge_decision(owner) for owner in owners),
            "Expanded direct phase0 decision charge failed")
    raw, _, prefix_errors = c204.encode_live_v2(owners, list(range(len(owners))))
    require(len(raw) == EXPANDED_ROWS, "Expanded direct row count drift")
    p, t, z, tz, meter = c189.combined_predict(base, selector, raw, batch=BATCH)
    return dict(
        raw=raw,
        necessity_predictions=p.copy(),
        target_predictions=t.copy(),
        necessity_logits=z.copy(),
        target_logits=tz.copy(),
        prefix_errors=prefix_errors,
        meter=meter,
    )


def phase0_reference(predictions, block):
    return dict(
        necessity_predictions=predictions["necessity_predictions"][0, block, :, 0].copy(),
        necessity_logits=predictions["necessity_logits"][0, block, :, 0].copy(),
        target_predictions=predictions["target_predictions"][0, block, :, 0].copy(),
        target_logits=predictions["target_logits"][0, block, :, 0].copy(),
    )


def compare(arrays, reference):
    p = arrays["necessity_predictions"]
    t = arrays["target_predictions"]
    z = arrays["necessity_logits"]
    tz = arrays["target_logits"]
    rp = reference["necessity_predictions"]
    rt = reference["target_predictions"]
    rz = reference["necessity_logits"]
    rtz = reference["target_logits"]
    require(
        p.shape == rp.shape == (EXPANDED_ROWS,)
        and t.shape == rt.shape == (EXPANDED_ROWS,)
        and z.shape == rz.shape == (EXPANDED_ROWS, 2)
        and tz.shape == rtz.shape == (EXPANDED_ROWS, 4),
        "Phase0 comparison shape drift",
    )
    finite = np.isfinite(rtz)
    require(np.array_equal(np.isfinite(tz), finite), "Target finite-mask drift")
    return dict(
        necessity_prediction_errors=int((p != rp).sum()),
        target_prediction_errors=int((t != rt).sum()),
        necessity_max_abs_logit_difference=float(
            np.max(np.abs(z.astype(np.float64) - rz.astype(np.float64)))
        ),
        target_max_abs_logit_difference=float(
            np.max(np.abs(tz[finite].astype(np.float64) - rtz[finite].astype(np.float64)))
        ) if finite.any() else 0.0,
    )


def c204_replay_map(p204):
    rows = p204.get("prediction_replay")
    require(isinstance(rows, list) and len(rows) == 9, "C204 replay record coverage drift")
    out = {}
    for row in rows:
        require(
            set(("block", "base_seed", "head_seed", "necessity_prediction_errors",
                 "target_prediction_errors", "necessity_max_abs_logit_difference",
                 "target_max_abs_logit_difference")).issubset(row),
            "C204 replay record schema drift",
        )
        key = (int(row["base_seed"]), int(row["head_seed"]))
        require(key not in out, "Duplicate C204 replay record")
        out[key] = row
    require(set(out) == {(b, h) for b in BASE_SEEDS for h in HEAD_SEEDS},
            "C204 replay pair set drift")
    return out


def gate(canonical, expanded, matches, workload):
    expected_pairs = [(b, h) for b in BASE_SEEDS for h in HEAD_SEEDS]
    return (
        [(r["base_seed"], r["head_seed"]) for r in canonical] == expected_pairs
        and [(r["base_seed"], r["head_seed"]) for r in expanded] == expected_pairs
        and [(r["base_seed"], r["head_seed"]) for r in matches] == expected_pairs
        and all(
            r["prefix_errors"] == 0
            and r["expanded_prefix_mismatches"] == 0
            and r["necessity_prediction_errors"] == 0
            and r["target_prediction_errors"] == 0
            and r["necessity_max_abs_logit_difference"] <= ATOL
            and r["target_max_abs_logit_difference"] <= ATOL
            for r in canonical
        )
        and all(
            r["prefix_errors"] == 0
            and r["necessity_prediction_errors"] == 0
            and r["target_prediction_errors"] == 0
            and r["necessity_max_abs_logit_difference"] > ATOL
            and r["target_max_abs_logit_difference"] > ATOL
            for r in expanded
        )
        and all(
            r["necessity_parent_max_delta_difference"] <= 1e-12
            and r["target_parent_max_delta_difference"] <= 1e-12
            for r in matches
        )
        and workload == dict(
            canonical_rows=15912,
            expanded_rows=85824,
            canonical_forward_calls=18,
            expanded_forward_calls=90,
            canonical_cell_calls=126,
            expanded_cell_calls=630,
        )
    )


def precheck(c204_summary, c203_summary, c202_summary, c201_summary, c200_summary,
             c199_summary, c174_summary, c181_summary, c188_summary, root):
    root = Path(root)
    p203, c199, prediction_path, c174_result, pilot_path, p181, p188, pins, protected = c204.precheck(
        c203_summary, c202_summary, c201_summary, c200_summary, c199_summary, c174_summary,
        c181_summary, c188_summary, root
    )
    require(audit.sha(c204_summary) == PARENT_C204_SHA, "C204 summary changed")
    p204 = audit.read_json(c204_summary)
    c204.validate_result(p204)
    require(
        p204.get("commit_sha") == PARENT_C204_EXECUTION
        and p204.get("status") == "FAIL"
        and p204.get("diagnostic_execution_valid") is True
        and p204.get("source_blobs") == pins
        and p204["summary"].get("necessity_prediction_errors") == 0
        and p204["summary"].get("target_prediction_errors") == 0
        and p204["summary"].get("v2_prefix_errors") == 0
        and p204["summary"].get("failures") == 0
        and p204["summary"].get("max_necessity_logit_delta", 0) > ATOL
        and p204["summary"].get("max_target_logit_delta", 0) > ATOL
        and not c204.gate(p204["block_records"], p204["summary"]),
        "Wrong accepted-valid-negative C204 parent",
    )

    protected[str(Path(c204_summary).resolve())] = PARENT_C204_SHA
    for artifact in p204["artifacts"]:
        path = audit.safe_child(Path(c204_summary).resolve().parent, artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C204 artifact:" + artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]

    pins = dict(pins)
    for name in c204.OWN:
        wanted = audit.git(root, "rev-parse", PARENT_C204_EXECUTION + ":" + name).decode().strip()
        current = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
        require(current == wanted, "Accepted C204 source changed:" + name)
        pins[name] = wanted

    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
    protected.update(audit.protect_tree_files(root, allpins))
    pins.update({name: allpins[name] for name in OWN})
    require(len(pins) == 44 and len(protected) == 92, "C205 source/protection count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C205 manifest drift")
    return p204, c199, prediction_path, c174_result, pilot_path, p181, p188, pins, protected


def regression_modules(root):
    names = c204.regression_modules(root)
    require(len(names) == len(set(names)) == 89, "Historical regression list drift")
    return names + ["tests_lm.test_v05_c205_phase0_batch_composition_attribution"]


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C205",
    )
    require(
        len(payload["source_blobs"]) == 44
        and len(payload["input_sha256"]) == 92
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C205 coverage drift",
    )
    require(
        payload["training_steps"] == 0
        and payload["fresh_seed_count"] == 0
        and payload["acquisitions"] == 0
        and payload["network_calls"] == 0
        and payload["production_runtime_modified"] is False
        and payload["gate_e_candidate"] is False,
        "C205 scope drift",
    )
    require(
        payload["status"] == (
            "PASS" if gate(
                payload["canonical_unique"], payload["expanded_direct"],
                payload["c204_max_match"], payload["workload"]
            ) else "FAIL"
        ),
        "C205 gate drift",
    )


def run(*, c204_summary, c203_summary, c202_summary, c201_summary, c200_summary,
        c199_summary, c174_summary, c181_summary, c188_summary, output_dir, expected_head):
    root = Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root, "rev-parse", "HEAD").decode().strip() == expected_head,
                "HEAD mismatch")
        require(audit.git(root, "branch", "--show-current").decode().strip()
                == "feat/sft-target-loss", "Branch mismatch")
        require(not audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    p204, _, prediction_path, _, _, _, _, pins, protected = precheck(
        c204_summary, c203_summary, c202_summary, c201_summary, c200_summary,
        c199_summary, c174_summary, c181_summary, c188_summary, root
    )
    predictions = c201.load_c199_predictions(prediction_path)
    _, _, features = c203.load_c174_features(Path(c174_summary))
    bases, selectors = c204.restore_models(Path(c181_summary), Path(c188_summary))
    cohort = reconstruct_phase0_cohort(features, predictions)
    parent_map = c204_replay_map(p204)

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

    save("attribution-plan.json", dict(manifest(), source_blobs=pins))
    try:
        canonical = []
        expanded = []
        matches = []
        canonical_meter = dict(rows=0, forward_calls=0, cell_calls=0)
        expanded_meter = dict(rows=0, forward_calls=0, cell_calls=0)

        for bi, b in enumerate(BASE_SEEDS):
            for hi, h in enumerate(HEAD_SEEDS):
                idx = bi * 3 + hi
                unique = infer_v2_unique(
                    cohort["raw13"], cohort["full_ix"], cohort["local_rows"],
                    bases[b], selectors[b, h], f"C205-unique-b{b}-h{h}",
                )
                direct = infer_v2_expanded(
                    cohort["expanded13"], cohort["source_rows"], cohort["world_codes"],
                    bases[b], selectors[b, h], f"C205-expanded-b{b}-h{h}",
                )
                reference = phase0_reference(predictions, idx)
                um = compare(unique, reference)
                em = compare(direct, reference)
                mismatch_rows = int(
                    (unique["raw"][cohort["local_rows"]] != direct["raw"]).any(dim=1).sum().item()
                )
                parent = parent_map[b, h]

                canonical.append(dict(
                    block=idx, base_seed=b, head_seed=h,
                    prefix_errors=unique["prefix_errors"],
                    expanded_prefix_mismatches=mismatch_rows,
                    **um,
                ))
                expanded.append(dict(
                    block=idx, base_seed=b, head_seed=h,
                    prefix_errors=direct["prefix_errors"],
                    **em,
                ))
                matches.append(dict(
                    block=idx, base_seed=b, head_seed=h,
                    necessity_parent_max=float(parent["necessity_max_abs_logit_difference"]),
                    target_parent_max=float(parent["target_max_abs_logit_difference"]),
                    necessity_expanded_max=em["necessity_max_abs_logit_difference"],
                    target_expanded_max=em["target_max_abs_logit_difference"],
                    necessity_parent_max_delta_difference=abs(
                        em["necessity_max_abs_logit_difference"]
                        - float(parent["necessity_max_abs_logit_difference"])
                    ),
                    target_parent_max_delta_difference=abs(
                        em["target_max_abs_logit_difference"]
                        - float(parent["target_max_abs_logit_difference"])
                    ),
                ))

                for key in canonical_meter:
                    canonical_meter[key] += int(unique["meter"][key])
                    expanded_meter[key] += int(direct["meter"][key])

                print(
                    f"[C205] block={idx+1}/9 base={b} head={h} "
                    f"unique_n={um['necessity_max_abs_logit_difference']:.9g} "
                    f"expanded_n={em['necessity_max_abs_logit_difference']:.9g}",
                    flush=True,
                )

        workload = dict(
            canonical_rows=canonical_meter["rows"],
            expanded_rows=expanded_meter["rows"],
            canonical_forward_calls=canonical_meter["forward_calls"],
            expanded_forward_calls=expanded_meter["forward_calls"],
            canonical_cell_calls=canonical_meter["cell_calls"],
            expanded_cell_calls=expanded_meter["cell_calls"],
        )

        save("canonical-unique.json", canonical)
        save("expanded-direct.json", expanded)
        save("c204-max-match.json", matches)
        save("workload.json", workload)

        guard()
        precheck(
            c204_summary, c203_summary, c202_summary, c201_summary, c200_summary,
            c199_summary, c174_summary, c181_summary, c188_summary, root
        )
        for path, wanted in protected.items():
            require(audit.sha(path) == wanted, "Protected input changed:" + path)
        for artifact in artifacts:
            require(audit.sha(out / artifact["file"]) == artifact["sha256"],
                    "Output changed:" + artifact["file"])

        result = dict(
            experiment_id=EXPERIMENT_ID,
            stage=STAGE,
            commit_sha=expected_head,
            status="PASS" if gate(canonical, expanded, matches, workload) else "FAIL",
            diagnostic_execution_valid=True,
            C204_summary_sha256=PARENT_C204_SHA,
            C199_reference_summary_sha256=REFERENCE_C199_SHA,
            source_blobs=pins,
            input_sha256=protected,
            artifacts=artifacts,
            canonical_unique=canonical,
            expanded_direct=expanded,
            c204_max_match=matches,
            workload=workload,
            training_steps=0,
            fresh_seed_count=0,
            acquisitions=0,
            network_calls=0,
            production_runtime_modified=False,
            gate_e_candidate=False,
            wall_clock_seconds=time.perf_counter()-started,
            limitations=[
                "phase0 numeric attribution only",
                "no runtime acquisitions or action replay",
                "same1e-6 tolerance; no post-hoc relaxation",
                "development cohort, not independent holdout",
                "does not retroactively convert C204 to PASS",
            ],
        )
        validate_result(result)
        (out / "summary.json").write_bytes(blob(result))
        print("[C205] phase0 batch-composition attribution collected", flush=True)
        print("=== C205 RESULT ===", flush=True)
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
    for name in (
        "c204-summary", "c203-summary", "c202-summary", "c201-summary", "c200-summary",
        "c199-summary", "c174-summary", "c181-summary", "c188-summary", "output-dir",
    ):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
