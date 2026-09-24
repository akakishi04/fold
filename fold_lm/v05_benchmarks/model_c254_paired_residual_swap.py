"""C254: paired swaps of saved post-core residuals; frozen head-only recomputation."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest
import torch
from torch import nn

EXPERIMENT_ID = "C254-v5b-paired-residual-swap"
STAGE = "V5-B-PAIRED-RESIDUAL-SWAP"
BASE = "bd1b88a27ab4aaa5712d06bc178158e6f410a7ff"
PARENT_EXECUTION = "13523ebefc482f3b230101d9a89938bda79c69e5"
PARENT_SHA = "2d65feaed637c71728cd8ed1cc60f54306a7fb733b43c6b695e86f0313f27e47"
C252_SHA = "18c176213aa0c047ddf9fe53f188e933e341f5e8556571c0a8999e7a36164f9e"
PARENT_ARTIFACTS = {
    "contrasts.json": "e364a74cb9338d7be8c57e85bcbac63e77d169847e83c358175b4e7caaa416d7",
    "diagnostics.json": "5647cbff9a4d214e3c83e77f689e9fde18955c5aef1dba71647c3db9cdd3c6bb",
    "outputs.pt": "3e8ba69a46323ed4c47c143f7cacd23ddd42c64cc7a5dbd3973cfd9bff32147c",
    "residual-plan.json": "c48689b9cebedc757261ded1912dbb597884f19ac007d971bcd7bfbfbfd8307d",
    "validation-summary.json": "b9cefa29b067961cb9dd181e5ab8be63352b795ee7e91540a63cc2b13d971685",
}
SPLIT_SHA = "e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346"
SEEDS = (250001, 250002, 250003, 250004, 250005)
SPLITS, VIEWS = ("TRAIN", "HOLDOUT"), ("normal", "evidence_blind", "query_blind")
MODES = ("self", "order_swap", "query_swap", "restored")
ROWS, TOL = {"TRAIN": 64, "HOLDOUT": 32}, 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c254_paired_residual_swap.py",
       "tests_lm/test_v05_c254_paired_residual_swap.py", "tools/run_c254.ps1", "tools/invoke_c254.ps1",
       "docs/experiment-ledger-addendum-c254-preregistration.md", "docs/v5b-paired-residual-swap-v0.1.md")
OUTPUTS = {"swap-plan.json", "head-outputs.pt", "diagnostics.json", "contrasts.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "cfbf05fc55fe6c87a0b738bfab7f4c676bb75ed503883cb399898f7936641276"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def context():
    from fold_lm.v05_benchmarks import model_c253_frozen_residual_path as parent
    c252, _, _, _, factory, audit = parent.context()
    return parent, c252, factory, audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        c252_summary_sha256=C252_SHA, split_sha256=SPLIT_SHA, seeds=list(SEEDS), modes=list(MODES),
        rows=ROWS, views=list(VIEWS), formula="decoder(LN(saved_post[donor] + recipient_saved_read))",
        donor_rules=dict(self="same row", order_swap="same facts/query, opposite fact order",
                         query_swap="same facts/order, opposite query", restored="same row again"),
        donor_scope="same seed/split/language/view; fixed involutions; no correctness-based donor selection",
        primary="diagnostic integrity only; no score-change threshold",
        full_model_forward_calls=0, encoder_core_reader_forward_calls=0,
        head_forward_calls=120, head_row_presentations=5760, new_training_steps=0,
        checkpoint_bundle_loads=1, model_state_loads=5, new_checkpoint_writes=0,
        diagnostic_cells=80, contrast_cells=40, source_pins=370, protected_inputs=599,
        direct_dependencies=30, own_tests=24, modules=139, loaded_tests=3266, focused_tests=3265,
        excluded_test=EXCLUDED, dtype="CPU float64", threads=2, deterministic=True, replay_tolerance=TOL,
        network_calls=0, capability_pass_claim=False, causal_mechanism_claim=False,
        production_adoption=False, gate_f_candidate=False)


def donor_indices(rows, mode):
    require(mode in MODES and len(rows) in (32, 64), "donor mode/count")
    keys = [(r["language"], r["group"], r["order"], r["query"]) for r in rows]
    require(len(set(keys)) == len(rows) and len({r["id"] for r in rows}) == len(rows), "unique donor keys")
    lookup = {key: i for i, key in enumerate(keys)}
    result = []
    for i, row in enumerate(rows):
        require(row["objects"] == [0, 1] and row["query"] in (0, 1) and row["order"] in (0, 1), "row contract")
        language, group, order, query = keys[i]
        key = (language, group, 1-order if mode == "order_swap" else order,
               1-query if mode == "query_swap" else query)
        require(key in lookup, "missing paired donor")
        j = lookup[key]; donor = rows[j]
        require(donor["values"] == row["values"] and donor["objects"] == row["objects"], "same facts")
        # Targets validate the declared pair, but never select its index.
        require((donor["target"] == row["target"]) == (mode != "query_swap"), "paired target relation")
        result.append(j)
    require(sorted(result) == list(range(len(rows))) and all(result[result[i]] == i for i in range(len(rows))), "permutation/involution")
    if mode in ("order_swap", "query_swap"):
        require(all(i != j for i, j in enumerate(result)), "no self donor in changed mode")
    return result


def tensor_check(value, shape):
    require(isinstance(value, torch.Tensor) and tuple(value.shape) == tuple(shape)
            and value.device.type == "cpu" and value.dtype == torch.float64
            and bool(torch.isfinite(value).all()), "finite float64 tensor")


def max_error(left, right):
    require(left.shape == right.shape, "replay shape")
    tensor_check(left, left.shape); tensor_check(right, left.shape)
    error = float((left-right).abs().max())
    require(error <= TOL and torch.equal(left.argmax(-1), right.argmax(-1)), "raw-logit/argmax replay")
    return error


def score_one(model, parts, entry, fingerprint):
    require(not any(m.training for m in model.modules()) and not any(p.requires_grad for p in model.parameters()), "frozen head")
    require(fingerprint(model) == entry["final_sha256"], "checkpoint identity")
    norm, decoder = model.backbone.readout_norm, model.backbone.decoder
    require(isinstance(norm, nn.LayerNorm) and tuple(norm.normalized_shape) == (16,)
            and isinstance(decoder, nn.Linear) and (decoder.in_features, decoder.out_features) == (16, 256), "head contract")
    before = fingerprint(model); counts = Counter(); rows_seen = [0]; handles = []
    def forbid(module, args):
        raise ValueError("encoder/core/reader/full-model forward forbidden")
    def counted_norm(module, args, output):
        counts["norm"] += 1
    def counted_decoder(module, args, output):
        counts["decoder"] += 1; rows_seen[0] += len(args[0])
    results = {}; error = 0.0
    try:
        for module in (model, model.backbone, model.backbone.local_encoder, model.backbone.core, model.read):
            handles.append(module.register_forward_pre_hook(forbid))
        handles.append(norm.register_forward_hook(counted_norm))
        handles.append(decoder.register_forward_hook(counted_decoder))
        with torch.no_grad():
            for mode in MODES:
                results[mode] = {}
                for split in SPLITS:
                    indices = donor_indices(parts[split], mode)
                    results[mode][split] = {}
                    for view in VIEWS:
                        signals = entry["components"]["intact"][split][view]
                        post, read = signals["post"], signals["read"]
                        tensor_check(post, (ROWS[split], 16)); tensor_check(read, (ROWS[split], 16))
                        selected = post[indices]
                        if mode == "query_swap" and view == "query_blind":
                            require(torch.equal(selected, post), "query-blind paired residual identity")
                        # Addition creates a new tensor: saved source activations remain unmodified.
                        output = decoder(norm(selected + read)).detach().clone()
                        tensor_check(output, (ROWS[split], 256))
                        results[mode][split][view] = output
                        if mode == "self":
                            error = max(error, max_error(output, entry["outputs"]["intact"][split][view]))
                        if mode == "restored" or (mode == "query_swap" and view == "query_blind"):
                            error = max(error, max_error(output, results["self"][split][view]))
                        require(fingerprint(model) == before, "head/parameter mutation")
    finally:
        for handle in handles:
            handle.remove()
    require(counts == {"norm": 24, "decoder": 24} and rows_seen[0] == 1152, "head-only workload")
    return dict(seed=entry["seed"], final_sha256=before, outputs=results,
                head_forward_calls=24, head_row_presentations=1152, weights_preserved=True, replay_max_error=error)


def analyze(parts, records, original, metric_fn):
    require(digest(parts) == SPLIT_SHA and {s: len(parts[s]) for s in SPLITS} == ROWS, "partition identity")
    require([r["seed"] for r in records] == [e["seed"] for e in original] == list(SEEDS), "all five identities")
    diagnostics, contrasts = [], []
    for record, entry in zip(records, original, strict=True):
        require(record["final_sha256"] == entry["final_sha256"] and record["weights_preserved"] is True
                and (record["head_forward_calls"], record["head_row_presentations"]) == (24, 1152), "record integrity")
        require(type(record["replay_max_error"]) in (int, float) and 0 <= record["replay_max_error"] <= TOL, "record replay flag")
        outputs = record["outputs"]; require(set(outputs) == set(MODES), "mode coverage")
        measured, predictions = {}, {}
        for mode in MODES:
            require(set(outputs[mode]) == set(SPLITS), "split coverage")
            measured[mode], predictions[mode] = {}, {}
            for split in SPLITS:
                require(set(outputs[mode][split]) == set(VIEWS), "view coverage")
                for view in VIEWS:
                    value = outputs[mode][split][view]; tensor_check(value, (ROWS[split], 256))
                    if mode == "self": max_error(value, entry["outputs"]["intact"][split][view])
                    if mode == "restored" or (mode == "query_swap" and view == "query_blind"):
                        max_error(value, outputs["self"][split][view])
                measured[mode][split], predictions[mode][split] = metric_fn(parts[split], outputs[mode][split])
        diagnostics.append(dict(seed=record["seed"], metrics=measured))
        for mode in ("order_swap", "query_swap"):
            for split in SPLITS:
                rows = parts[split]; donor = donor_indices(rows, mode)
                old = predictions["self"][split]["normal"]; new = predictions[mode][split]["normal"]
                for lang in ("en", "ja"):
                    ids = [i for i, row in enumerate(rows) if row["language"] == lang]
                    m, n = measured["self"][split][lang], measured[mode][split][lang]
                    contrasts.append(dict(seed=record["seed"], mode=mode, split=split, language=lang, rows=len(ids),
                        original_correct=sum(old[i] == rows[i]["target"] for i in ids),
                        changed_correct=sum(new[i] == rows[i]["target"] for i in ids),
                        correct_to_wrong=sum(old[i] == rows[i]["target"] and new[i] != rows[i]["target"] for i in ids),
                        wrong_to_correct=sum(old[i] != rows[i]["target"] and new[i] == rows[i]["target"] for i in ids),
                        answer_flips=sum(old[i] != new[i] for i in ids),
                        donor_target_matches=sum(new[i] == rows[donor[i]]["target"] for i in ids),
                        accuracy_delta=n["accuracy"]-m["accuracy"], nll_delta=n["answer_nll"]-m["answer_nll"]))
    require(len(contrasts) == 40, "contrast count")
    summary = dict(models=5, diagnostic_cells=80, contrast_cells=40, full_model_forward_calls=0,
        encoder_core_reader_forward_calls=0, head_forward_calls=sum(r["head_forward_calls"] for r in records),
        head_row_presentations=sum(r["head_row_presentations"] for r in records), new_training_steps=0,
        new_checkpoint_writes=0, checkpoint_bundle_loads=1, model_state_loads=5, weights_preserved=True,
        intact_logits_replayed=True, restored_logits_replayed=True, query_blind_control_replayed=True,
        capability_pass_claim=False, causal_mechanism_claim=False)
    return diagnostics, contrasts, summary


def load_inputs(c253_summary, c252_summary):
    parent, _, _, a = context(); path = Path(c253_summary).resolve()
    require(a.sha(path) == PARENT_SHA and a.sha(c252_summary) == C252_SHA, "parent identities")
    p = a.read_json(path); parent.validate_result(p)
    parts, refs = parent.load_inputs(c252_summary)  # C253's loader intentionally reads C252.
    saved = torch.load(path.parent/"outputs.pt", map_location="cpu", weights_only=True)
    require(set(saved) == {"schema", "entries"} and saved["schema"] == "fold-c253-frozen-outputs-v1", "C253 archive schema")
    entries = saved["entries"]
    diagnostics, contrasts, summary = parent.analyze(parts, entries, refs)
    for name, value in (("residual-plan.json", parent.manifest()), ("diagnostics.json", diagnostics),
                        ("contrasts.json", contrasts), ("validation-summary.json", summary)):
        require(a.read_json(path.parent/name) == value, "parent archive replay:"+name)
    require(summary == p["validation_summary"], "parent summary replay")
    for split in SPLITS:
        for mode in MODES: donor_indices(parts[split], mode)
    return parts, refs, entries


def precheck(c253_summary, c252_summary, root):
    parent, _, factory, a = context(); path, earlier, root = Path(c253_summary).resolve(), Path(c252_summary).resolve(), Path(root)
    require(a.sha(path) == PARENT_SHA, "parent summary hash")
    p = a.read_json(path); parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS", "accepted diagnostic parent")
    pins, protected = dict(p["source_blobs"]), dict(p["input_sha256"])
    for name, wanted in protected.items(): require(Path(name).is_file() and a.sha(name) == wanted, "changed input:"+name)
    for name, wanted in pins.items(): require(a.git(root, "rev-parse", "HEAD:"+name).decode().strip() == wanted, "changed source:"+name)
    require(protected.get(str(earlier)) == C252_SHA and a.sha(earlier) == C252_SHA, "inherited C252 identity")
    require(str(path) not in protected, "parent double count"); protected[str(path)] = PARENT_SHA
    require({x["file"]: x["sha256"] for x in p["artifacts"]} == PARENT_ARTIFACTS, "parent artifacts")
    for item in p["artifacts"]:
        child = a.safe_child(path.parent, item["file"])
        require(a.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "parent bytes")
        require(str(child.resolve()) not in protected, "artifact double count"); protected[str(child.resolve())] = item["sha256"]
    for name in OWN:
        require(name not in pins, "OWN collision"); pins[name] = a.git(root, "rev-parse", "HEAD:"+name).decode().strip()
    helpers = ("gate_f_c230_prepared_capsule.py", "model_c231_byte_eval_contract.py", "model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py", "model_c234_context_binding.py", "model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py", "model_c237_frozen_signal_audit.py", "model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py", "model_c240_saved_position_audit.py", "model_c241_assignment_holdout.py",
        "model_c242_balanced_recombination.py", "model_c243_saved_recombination_audit.py", "model_c244_two_partner_recombination.py",
        "model_c245_selective_evidence.py", "model_c246_training_erasure.py", "model_c247_normal_exposure_control.py",
        "model_c248_residual_token_read.py", "model_c249_frozen_read_ablation.py", "model_c250_fresh_seed_replication.py",
        "model_c251_precore_read.py", "model_c252_precore_query_alignment.py", "model_c253_frozen_residual_path.py")
    required = set(factory.LM_SOURCES) | {"fold_lm/v05_benchmarks/"+h for h in helpers} | {OWN[0]}
    require(len(required) == 30 and required <= set(pins), "direct dependencies")
    protected.update(a.protect_tree_files(root, pins))
    require((len(pins), len(protected)) == (370, 599) and digest(manifest()) == MANIFEST_SHA, "protection/manifest")
    return pins, protected


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["status"] == "PASS"
            and p["diagnostic_execution_valid"] is True, "diagnostic identity")
    require((len(p["source_blobs"]), len(p["input_sha256"])) == (370, 599) and set(OWN) <= set(p["source_blobs"]), "protection")
    require(len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS, "outputs")
    s, m = p["validation_summary"], manifest()
    for key in ("diagnostic_cells", "contrast_cells", "full_model_forward_calls", "encoder_core_reader_forward_calls",
                "head_forward_calls", "head_row_presentations", "new_training_steps", "new_checkpoint_writes",
                "checkpoint_bundle_loads", "model_state_loads"):
        require(type(s[key]) is int and s[key] == m[key], "result count:"+key)
    require(s["models"] == 5 and all(s[k] is True for k in ("weights_preserved", "intact_logits_replayed",
            "restored_logits_replayed", "query_blind_control_replayed")), "replay flags")
    require(s["capability_pass_claim"] is False and s["causal_mechanism_claim"] is False
            and p["production_adoption"] is False and p["gate_f_candidate"] is False and p["network_calls"] == 0, "scope")


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == 138, "parent modules")
    return names + ["tests_lm.test_v05_c254_paired_residual_swap"]


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite): yield from flatten(item)
        else: yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]; require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1, "suite IDs")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require((len(tests), len(kept)) == (3266, 3265), "suite counts")
    return unittest.TestSuite(kept)


def run(*, c253_summary, c252_summary, output_dir, expected_head):
    parent, c252, factory, a = context(); root = Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root, "rev-parse", "HEAD").decode().strip() == expected_head, "HEAD")
        require(a.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss", "branch")
        require(not a.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "dirty tracked tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins, protected = precheck(c253_summary, c252_summary, root)
    parts, refs, original = load_inputs(c253_summary, c252_summary)
    states = c252.load_bundle(Path(c252_summary).resolve().parent/"trained-models.pt")
    require(len(states) == len(refs) == len(original) == 5, "model coverage")
    records = []
    for ref, state, entry in zip(refs, states, original, strict=True):
        print(f'[C254] model={len(records)+1}/5 seed={ref["seed"]}; frozen head-only paired swaps', flush=True)
        model = parent.frozen_model(ref, state, c252, factory)
        records.append(score_one(model, parts, entry, factory.fingerprint))
    diagnostics, contrasts, summary = analyze(parts, records, original, parent.metrics)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False)
    torch.save(dict(schema="fold-c254-head-outputs-v1", records=records), out/"head-outputs.pt")
    for name, value in (("swap-plan.json", manifest()), ("diagnostics.json", diagnostics),
                        ("contrasts.json", contrasts), ("validation-summary.json", summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n, sha256=a.sha(out/n), serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard(); precheck(c253_summary, c252_summary, root)
    for name, wanted in protected.items(): require(a.sha(name) == wanted, "modified input")
    p = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head, status="PASS", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256=protected, artifacts=artifacts, validation_summary=summary,
        production_adoption=False, gate_f_candidate=False, network_calls=0)
    validate_result(p); (out/"summary.json").write_bytes(blob(p)); print("=== C254 RESULT ===", flush=True); print(blob(p).decode(), flush=True)
    return p


def verify_artifacts(output_dir, c253_summary, c252_summary, expected_head):
    parent, _, _, a = context(); out = Path(output_dir); p = a.read_json(out/"summary.json")
    validate_result(p); require(p["commit_sha"] == expected_head, "saved HEAD")
    for name, wanted in p["input_sha256"].items(): require(a.sha(name) == wanted, "postcheck input")
    for item in p["artifacts"]:
        child = a.safe_child(out, item["file"])
        require(a.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "saved artifact")
    data = torch.load(out/"head-outputs.pt", map_location="cpu", weights_only=True)
    require(set(data) == {"schema", "records"} and data["schema"] == "fold-c254-head-outputs-v1", "output archive")
    parts, _, original = load_inputs(c253_summary, c252_summary)
    diagnostics, contrasts, summary = analyze(parts, data["records"], original, parent.metrics)
    for name, value in (("swap-plan.json", manifest()), ("diagnostics.json", diagnostics),
                        ("contrasts.json", contrasts), ("validation-summary.json", summary)):
        require(a.read_json(out/name) == value, "persisted replay:"+name)
    require(summary == p["validation_summary"], "summary replay")
    return p, diagnostics, contrasts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("c253-summary", "c252-summary", "output-dir"):
        parser.add_argument("--"+name, type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__": main()
