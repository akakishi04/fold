"""C255: fixed-query value-assignment swaps; frozen saved-feature diagnostic only."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest
import torch
from torch import nn

EXPERIMENT_ID = "C255-v5b-value-residual-swap"
STAGE = "V5-B-VALUE-RESIDUAL-SWAP"
BASE = "5764f3e18a09452739029c3accd7740686d8d7fe"
PARENT_EXECUTION = "4e6e5abf5a6a3c97e784868b9fc5e016fc1cf77c"
PARENT_SHA = "96f0a3eaafbf0b9fc62e7e9f789344eac45497b2679662525ea54993803535f5"
C253_SHA = "2d65feaed637c71728cd8ed1cc60f54306a7fb733b43c6b695e86f0313f27e47"
C252_SHA = "18c176213aa0c047ddf9fe53f188e933e341f5e8556571c0a8999e7a36164f9e"
PARENT_ARTIFACTS = {
    "contrasts.json": "562e6fae59bd1cb79dcefd1191445277d53735c2bec1ee1cbfc08726cd5b80b2",
    "diagnostics.json": "2c98ffc583768f43aa3311d7164828163888da19f18594d36ce49840b75990e2",
    "head-outputs.pt": "ad4bfefa0380323fb5c408c1f9de4778d2e04c09637bae44049efb7df5f2d5a1",
    "swap-plan.json": "cfbf05fc55fe6c87a0b738bfab7f4c676bb75ed503883cb399898f7936641276",
    "validation-summary.json": "f204facbb500f7bc43db578e39231c8c2bc39dd07c7c399dcbef1de3ca3b9d95",
}
SPLIT_SHA = "e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346"
SEEDS = (250001, 250002, 250003, 250004, 250005)
SPLITS, VIEWS = ("TRAIN", "HOLDOUT"), ("normal", "evidence_blind", "query_blind")
MODES = ("self", "value_swap", "coherent_swap", "restored")
SCORED_MODES = ("self", "value_swap", "restored")
ROWS, TOL = {"TRAIN": 64, "HOLDOUT": 32}, 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c255_value_residual_swap.py",
       "tests_lm/test_v05_c255_value_residual_swap.py", "tools/run_c255.ps1", "tools/invoke_c255.ps1",
       "docs/experiment-ledger-addendum-c255-preregistration.md", "docs/v5b-value-residual-swap-v0.1.md")
OUTPUTS = {"value-plan.json", "head-outputs.pt", "diagnostics.json", "contrasts.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "e5a6589105d534218c9056768c2af3e60da136a2dfb9f9fa8393bba9198a548a"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def context():
    from fold_lm.v05_benchmarks import model_c254_paired_residual_swap as parent
    diagnostic, c252, factory, audit = parent.context()
    return parent, diagnostic, c252, factory, audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        c253_sha256=C253_SHA, c252_sha256=C252_SHA, split_sha256=SPLIT_SHA,
        seeds=list(SEEDS), modes=list(MODES), scored_modes=list(SCORED_MODES), rows=ROWS, views=list(VIEWS),
        donor="same language/query/order/object pair; values reversed; same split and seed",
        formula="decoder(LN(post[donor]+read[recipient])); coherent control swaps both",
        controls="self/restored original replay; coherent donor replay; evidence-blind value swap identity",
        comparators="immutable C254 order/query swap metrics; no comparator head rerun",
        primary="diagnostic integrity only; coherent_swap is replay control, not recipient accuracy",
        full_model_forward_calls=0, encoder_core_reader_forward_calls=0,
        head_forward_calls=120, head_row_presentations=5760, new_training_steps=0,
        checkpoint_bundle_loads=1, model_state_loads=5, new_checkpoint_writes=0,
        diagnostic_cells=60, contrast_cells=20, source_pins=376, protected_inputs=611,
        direct_dependencies=31, own_tests=24, modules=140, loaded_tests=3290, focused_tests=3289,
        excluded_test=EXCLUDED, dtype="CPU float64", threads=2, deterministic=True, replay_tolerance=TOL,
        network_calls=0, capability_pass_claim=False, causal_mechanism_claim=False,
        production_adoption=False, gate_f_candidate=False)


def donors(rows):
    require(len(rows) in (32, 64), "donor row count")
    def key(r):
        return r["language"], tuple(r["objects"]), tuple(r["values"]), r["order"], r["query"]
    lookup = {key(r): i for i, r in enumerate(rows)}
    require(len(lookup) == len(rows) == len({r["id"] for r in rows}), "unique row keys")
    indices = []
    for r in rows:
        require(r["objects"] == [0, 1] and r["query"] in (0, 1) and r["order"] in (0, 1)
                and len(r["values"]) == 2 and r["values"][0] != r["values"][1], "row contract")
        language, objects, values, order, query = key(r)
        k = language, objects, values[::-1], order, query
        require(k in lookup, "missing reversed-assignment donor")
        j = lookup[k]
        require(rows[j]["target"] != r["target"], "donor target validation")
        indices.append(j)
    require(sorted(indices) == list(range(len(rows))) and
            all(j != i and indices[j] == i for i, j in enumerate(indices)), "fixed-point-free involution")
    return indices


def tensor_check(value, shape):
    require(isinstance(value, torch.Tensor) and tuple(value.shape) == tuple(shape)
            and value.device.type == "cpu" and value.dtype == torch.float64
            and bool(torch.isfinite(value).all()), "finite float64 tensor")


def replay(left, right):
    require(left.shape == right.shape, "replay shape")
    tensor_check(left, left.shape); tensor_check(right, left.shape)
    error = float((left-right).abs().max())
    require(error <= TOL and torch.equal(left.argmax(-1), right.argmax(-1)), "logit/argmax replay")
    return error


def score_one(model, parts, entry, fingerprint):
    require(not any(m.training for m in model.modules()) and not any(p.requires_grad for p in model.parameters()), "frozen model")
    before = fingerprint(model)
    require(before == entry["final_sha256"], "accepted final identity")
    norm, decoder = model.backbone.readout_norm, model.backbone.decoder
    require(isinstance(norm, nn.LayerNorm) and tuple(norm.normalized_shape) == (16,)
            and isinstance(decoder, nn.Linear) and (decoder.in_features, decoder.out_features) == (16, 256), "head contract")
    counts = Counter(); head_rows = [0]; handles = []; outputs = {}; error = 0.0
    maps = {s: donors(parts[s]) for s in SPLITS}
    def forbidden(module, args):
        raise ValueError("full/encoder/core/reader forward forbidden")
    def counted_norm(module, args, output):
        counts["norm"] += 1
    def counted_decoder(module, args, output):
        counts["decoder"] += 1; head_rows[0] += len(args[0])
    try:
        for module in (model, model.backbone, model.backbone.local_encoder, model.backbone.core, model.read):
            handles.append(module.register_forward_pre_hook(forbidden))
        handles.append(norm.register_forward_hook(counted_norm))
        handles.append(decoder.register_forward_hook(counted_decoder))
        with torch.no_grad():
            for mode in MODES:
                outputs[mode] = {}
                for split in SPLITS:
                    d = maps[split]; outputs[mode][split] = {}
                    for view in VIEWS:
                        signals = entry["components"]["intact"][split][view]
                        post, read = signals["post"], signals["read"]
                        tensor_check(post, (ROWS[split], 16)); tensor_check(read, (ROWS[split], 16))
                        if view == "evidence_blind":
                            require(float((post[d]-post).abs().max()) <= TOL and float((read[d]-read).abs().max()) <= TOL, "masked fact-pair identity")
                        p = post[d] if mode in ("value_swap", "coherent_swap") else post
                        r = read[d] if mode == "coherent_swap" else read
                        output = decoder(norm(p+r)).detach().clone()
                        tensor_check(output, (ROWS[split], 256)); outputs[mode][split][view] = output
                        original = entry["outputs"]["intact"][split][view]
                        if mode == "self": error = max(error, replay(output, original))
                        if mode == "coherent_swap": error = max(error, replay(output, original[d]))
                        if mode == "restored" or (mode == "value_swap" and view == "evidence_blind"):
                            error = max(error, replay(output, outputs["self"][split][view]))
                        require(fingerprint(model) == before, "parameter mutation")
    finally:
        for handle in handles: handle.remove()
    require(counts == {"norm": 24, "decoder": 24} and head_rows[0] == 1152, "head workload")
    return dict(seed=entry["seed"], final_sha256=before, outputs=outputs, replay_max_error=error,
                head_forward_calls=24, head_row_presentations=1152, weights_preserved=True)


def analyze(parts, records, original, prior, metric_fn):
    require(set(parts) == set(SPLITS) and digest(parts) == SPLIT_SHA, "partition identity")
    require([r["seed"] for r in records] == [e["seed"] for e in original] == [r["seed"] for r in prior] == list(SEEDS), "all five identities")
    diagnostics, contrasts = [], []
    for record, entry, old in zip(records, original, prior, strict=True):
        require(record["final_sha256"] == entry["final_sha256"] == old["final_sha256"]
                and record["weights_preserved"] is True and
                (record["head_forward_calls"], record["head_row_presentations"]) == (24, 1152), "record integrity")
        require(type(record["replay_max_error"]) in (int, float) and 0 <= record["replay_max_error"] <= TOL, "replay bound")
        outputs = record["outputs"]; require(set(outputs) == set(MODES), "mode keys")
        measured = {m: {} for m in SCORED_MODES}; predictions = {m: {} for m in SCORED_MODES}
        for mode in MODES:
            require(set(outputs[mode]) == set(SPLITS), "split keys")
            for split in SPLITS:
                require(set(outputs[mode][split]) == set(VIEWS), "view keys")
                d = donors(parts[split])
                for view in VIEWS:
                    value = outputs[mode][split][view]; tensor_check(value, (ROWS[split], 256))
                    original_logits = entry["outputs"]["intact"][split][view]
                    if mode == "self":
                        replay(value, original_logits); replay(value, old["outputs"]["self"][split][view])
                    if mode == "coherent_swap": replay(value, original_logits[d])
                    if mode == "restored" or (mode == "value_swap" and view == "evidence_blind"):
                        replay(value, outputs["self"][split][view])
                if mode in SCORED_MODES:
                    measured[mode][split], predictions[mode][split] = metric_fn(parts[split], outputs[mode][split])
        diagnostics.append(dict(seed=record["seed"], metrics=measured, coherent_donor_replay=True))
        for split in SPLITS:
            rows = parts[split]; d = donors(rows)
            before, after = predictions["self"][split]["normal"], predictions["value_swap"][split]["normal"]
            comparisons = {mode: metric_fn(rows, old["outputs"][mode][split])[0] for mode in ("order_swap", "query_swap")}
            for lang in ("en", "ja"):
                ids = [i for i, r in enumerate(rows) if r["language"] == lang]
                a, c = measured["self"][split][lang], measured["value_swap"][split][lang]
                contrasts.append(dict(seed=record["seed"], split=split, language=lang, rows=len(ids),
                    original_correct=sum(before[i] == rows[i]["target"] for i in ids),
                    changed_correct=sum(after[i] == rows[i]["target"] for i in ids),
                    correct_to_wrong=sum(before[i] == rows[i]["target"] and after[i] != rows[i]["target"] for i in ids),
                    wrong_to_correct=sum(before[i] != rows[i]["target"] and after[i] == rows[i]["target"] for i in ids),
                    answer_flips=sum(before[i] != after[i] for i in ids),
                    donor_target_matches=sum(after[i] == rows[d[i]]["target"] for i in ids),
                    accuracy_delta=c["accuracy"]-a["accuracy"], nll_delta=c["answer_nll"]-a["answer_nll"],
                    c254_order_metrics=comparisons["order_swap"][lang], c254_query_metrics=comparisons["query_swap"][lang]))
    require(len(diagnostics) == 5 and len(contrasts) == 20, "analysis counts")
    summary = dict(models=5, diagnostic_cells=60, contrast_cells=20, full_model_forward_calls=0,
        encoder_core_reader_forward_calls=0, head_forward_calls=sum(r["head_forward_calls"] for r in records),
        head_row_presentations=sum(r["head_row_presentations"] for r in records), new_training_steps=0,
        checkpoint_bundle_loads=1, model_state_loads=5, new_checkpoint_writes=0, weights_preserved=True,
        intact_replayed=True, coherent_donor_replayed=True, restored_replayed=True, evidence_blind_control_replayed=True,
        capability_pass_claim=False, causal_mechanism_claim=False)
    return diagnostics, contrasts, summary


def load_inputs(c254_summary, c253_summary, c252_summary):
    parent, diagnostic, _, _, a = context(); path = Path(c254_summary).resolve()
    require(a.sha(path) == PARENT_SHA and a.sha(c253_summary) == C253_SHA and a.sha(c252_summary) == C252_SHA, "parent hashes")
    p = a.read_json(path); parent.validate_result(p)
    parts, refs, original = parent.load_inputs(c253_summary, c252_summary)
    archive = torch.load(path.parent/"head-outputs.pt", map_location="cpu", weights_only=True)
    require(set(archive) == {"schema", "records"} and archive["schema"] == "fold-c254-head-outputs-v1", "parent archive schema")
    prior = archive["records"]
    d, c, s = parent.analyze(parts, prior, original, diagnostic.metrics)
    for name, value in (("swap-plan.json", parent.manifest()), ("diagnostics.json", d), ("contrasts.json", c), ("validation-summary.json", s)):
        require(a.read_json(path.parent/name) == value, "parent archive replay")
    require(s == p["validation_summary"], "parent summary replay")
    for split in SPLITS: donors(parts[split])
    return parts, refs, original, prior


def precheck(c254_summary, c253_summary, c252_summary, root):
    parent, _, _, factory, a = context(); path, root = Path(c254_summary).resolve(), Path(root)
    require(a.sha(path) == PARENT_SHA, "parent hash"); p = a.read_json(path); parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS", "accepted diagnostic")
    pins, protected = dict(p["source_blobs"]), dict(p["input_sha256"])
    for name, wanted in protected.items(): require(Path(name).is_file() and a.sha(name) == wanted, "changed input:"+name)
    for name, wanted in pins.items(): require(a.git(root, "rev-parse", "HEAD:"+name).decode().strip() == wanted, "changed source:"+name)
    for earlier, wanted in ((c253_summary, C253_SHA), (c252_summary, C252_SHA)):
        require(protected.get(str(Path(earlier).resolve())) == wanted, "inherited parent identity")
    require(str(path) not in protected, "parent duplicate"); protected[str(path)] = PARENT_SHA
    require({x["file"]: x["sha256"] for x in p["artifacts"]} == PARENT_ARTIFACTS, "parent artifact identities")
    for item in p["artifacts"]:
        child = a.safe_child(path.parent, item["file"])
        require(a.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "parent artifact bytes")
        require(str(child.resolve()) not in protected, "artifact duplicate"); protected[str(child.resolve())] = item["sha256"]
    for name in OWN:
        require(name not in pins, "OWN collision"); pins[name] = a.git(root, "rev-parse", "HEAD:"+name).decode().strip()
    helpers = ("gate_f_c230_prepared_capsule.py", "model_c231_byte_eval_contract.py", "model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py", "model_c234_context_binding.py", "model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py", "model_c237_frozen_signal_audit.py", "model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py", "model_c240_saved_position_audit.py", "model_c241_assignment_holdout.py",
        "model_c242_balanced_recombination.py", "model_c243_saved_recombination_audit.py", "model_c244_two_partner_recombination.py",
        "model_c245_selective_evidence.py", "model_c246_training_erasure.py", "model_c247_normal_exposure_control.py",
        "model_c248_residual_token_read.py", "model_c249_frozen_read_ablation.py", "model_c250_fresh_seed_replication.py",
        "model_c251_precore_read.py", "model_c252_precore_query_alignment.py", "model_c253_frozen_residual_path.py",
        "model_c254_paired_residual_swap.py")
    required = set(factory.LM_SOURCES) | {"fold_lm/v05_benchmarks/"+n for n in helpers} | {OWN[0]}
    require(len(required) == 31 and required <= set(pins), "deciding dependency coverage")
    protected.update(a.protect_tree_files(root, pins))
    require((len(pins), len(protected)) == (376, 611) and digest(manifest()) == MANIFEST_SHA, "protection/manifest")
    return pins, protected


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["status"] == "PASS"
            and p["diagnostic_execution_valid"] is True, "diagnostic status")
    require((len(p["source_blobs"]), len(p["input_sha256"])) == (376, 611) and set(OWN) <= set(p["source_blobs"]), "result protection")
    require(len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS, "output coverage")
    s, m = p["validation_summary"], manifest()
    for k in ("diagnostic_cells", "contrast_cells", "full_model_forward_calls", "encoder_core_reader_forward_calls", "head_forward_calls",
              "head_row_presentations", "new_training_steps", "checkpoint_bundle_loads", "model_state_loads", "new_checkpoint_writes"):
        require(type(s[k]) is int and s[k] == m[k], "count:"+k)
    require(s["models"] == 5 and all(s[k] is True for k in ("weights_preserved", "intact_replayed", "coherent_donor_replayed",
            "restored_replayed", "evidence_blind_control_replayed")), "replay flags")
    require(s["capability_pass_claim"] is False and s["causal_mechanism_claim"] is False
            and p["production_adoption"] is False and p["gate_f_candidate"] is False and p["network_calls"] == 0, "scope")


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == 139, "parent modules")
    return names+["tests_lm.test_v05_c255_value_residual_swap"]


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite): yield from flatten(item)
        else: yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]; require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1, "test identities")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require((len(tests), len(kept)) == (3290, 3289), "suite counts")
    return unittest.TestSuite(kept)


def run(*, c254_summary, c253_summary, c252_summary, output_dir, expected_head):
    _, diagnostic, c252, factory, a = context(); root = Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root, "rev-parse", "HEAD").decode().strip() == expected_head, "HEAD")
        require(a.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss", "branch")
        require(not a.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins, protected = precheck(c254_summary, c253_summary, c252_summary, root)
    parts, refs, original, prior = load_inputs(c254_summary, c253_summary, c252_summary)
    states = c252.load_bundle(Path(c252_summary).resolve().parent/"trained-models.pt")
    require(len(states) == len(refs) == len(original) == 5, "state coverage")
    records = []
    for ref, state, entry in zip(refs, states, original, strict=True):
        print(f'[C255] model={len(records)+1}/5 seed={ref["seed"]}; fixed-query value swap, head only', flush=True)
        model = diagnostic.frozen_model(ref, state, c252, factory)
        records.append(score_one(model, parts, entry, factory.fingerprint))
    d, c, s = analyze(parts, records, original, prior, diagnostic.metrics)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False)
    torch.save(dict(schema="fold-c255-value-head-outputs-v1", records=records), out/"head-outputs.pt")
    for name, value in (("value-plan.json", manifest()), ("diagnostics.json", d), ("contrasts.json", c), ("validation-summary.json", s)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n, sha256=a.sha(out/n), serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard(); precheck(c254_summary, c253_summary, c252_summary, root)
    for name, wanted in protected.items(): require(a.sha(name) == wanted, "modified input")
    p = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head, status="PASS", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256=protected, artifacts=artifacts, validation_summary=s, production_adoption=False, gate_f_candidate=False, network_calls=0)
    validate_result(p); (out/"summary.json").write_bytes(blob(p)); print("=== C255 RESULT ===", flush=True); print(blob(p).decode(), flush=True)
    return p


def verify_artifacts(output_dir, c254_summary, c253_summary, c252_summary, expected_head):
    _, diagnostic, _, _, a = context(); out = Path(output_dir); p = a.read_json(out/"summary.json")
    validate_result(p); require(p["commit_sha"] == expected_head, "saved HEAD")
    for name, wanted in p["input_sha256"].items(): require(a.sha(name) == wanted, "postcheck input")
    for item in p["artifacts"]:
        child = a.safe_child(out, item["file"])
        require(a.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "saved artifact")
    archive = torch.load(out/"head-outputs.pt", map_location="cpu", weights_only=True)
    require(set(archive) == {"schema", "records"} and archive["schema"] == "fold-c255-value-head-outputs-v1", "output schema")
    parts, _, original, prior = load_inputs(c254_summary, c253_summary, c252_summary)
    d, c, s = analyze(parts, archive["records"], original, prior, diagnostic.metrics)
    for name, value in (("value-plan.json", manifest()), ("diagnostics.json", d), ("contrasts.json", c), ("validation-summary.json", s)):
        require(a.read_json(out/name) == value, "persisted recomputation:"+name)
    require(s == p["validation_summary"], "summary replay")
    return p, d, c


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for n in ("c254-summary", "c253-summary", "c252-summary", "output-dir"): p.add_argument("--"+n, type=Path, required=True)
    p.add_argument("--expected-head", required=True); run(**vars(p.parse_args()))


if __name__ == "__main__": main()
