"""C253: frozen residual-path intervention on all five accepted C252 models."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import unittest
import torch
from torch import nn
from torch.nn import functional as F

EXPERIMENT_ID = "C253-v5b-frozen-postcore-residual"
STAGE = "V5-B-FROZEN-POSTCORE-RESIDUAL"
BASE = "c647917f2ff052f0c7fe403d1355c16ba6b5da65"
PARENT_EXECUTION = "2e3102b6f1d7061afcfd0bcf996ad660fcf36a36"
PARENT_SHA = "18c176213aa0c047ddf9fe53f188e933e341f5e8556571c0a8999e7a36164f9e"
PARENT_ARTIFACTS = {
    "alignment-plan.json": "f662c4d9c5588bbc0662ae9f578dd59068354a76951bf7192f18f8e53166fd9b",
    "measurements.json": "dc88a83ab9d8add4022ba898af9a030b787cd46e088c94b1d26e205c83c29b91",
    "split-dataset.json": "e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346",
    "trained-models.pt": "024e8081fae8bc45ce449b3bdf53745499911ca631387620a6575e2312c5b6c3",
    "validation-summary.json": "8442f683dfe0ed9122f476b723083d017a6cd5ef6e1087bca67dfd20fc167fbf",
}
SEEDS = (250001, 250002, 250003, 250004, 250005)
SPLITS = ("TRAIN", "HOLDOUT")
VIEWS = ("normal", "evidence_blind", "query_blind")
MODES = ("intact", "pre_residual", "reader_only", "restored")
ROWS = {"TRAIN": 64, "HOLDOUT": 32}
TOL = 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c253_frozen_residual_path.py",
       "tests_lm/test_v05_c253_frozen_residual_path.py", "tools/run_c253.ps1", "tools/invoke_c253.ps1",
       "docs/experiment-ledger-addendum-c253-preregistration.md", "docs/v5b-frozen-residual-path-v0.1.md")
OUTPUTS = {"residual-plan.json", "outputs.pt", "diagnostics.json", "contrasts.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "c48689b9cebedc757261ded1912dbb597884f19ac007d971bcd7bfbfbfd8307d"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c252_precore_query_alignment as parent
    return parent


def context():
    parent = parent_module()
    _, base, fitting, binding, factory, audit = parent.context()
    return parent, base, fitting, binding, factory, audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        seeds=list(SEEDS), modes=list(MODES), views=list(VIEWS), rows=ROWS,
        formulas=dict(intact="LN(post+read)", pre_residual="LN(pre+read)",
                      reader_only="LN(read)", restored="LN(post+read)"),
        invariant="pre-core query, K/V, reader contribution, weights, inputs and computed core states unchanged",
        insertion="replace LayerNorm output using the same parameters/epsilon and the specified input vector",
        primary="diagnostic integrity only; no accuracy-drop requirement",
        new_training_steps=0, model_forward_calls=120, row_presentations=5760,
        parent_bundle_loads=1, model_state_loads=5, new_checkpoint_writes=0,
        normalization_recomputations=60, diagnostic_cells=80, contrast_cells=40,
        source_pins=364, protected_inputs=587, direct_dependencies=29, own_tests=24,
        modules=138, loaded_tests=3242, focused_tests=3241, excluded_test=EXCLUDED,
        dtype="CPU float64", threads=2, deterministic=True, replay_tolerance=TOL,
        network_calls=0, nll_recomputed=True, capability_pass_claim=False, causal_mechanism_claim=False,
        training_core_necessity_claim=False, production_adoption=False, gate_f_candidate=False)


def metric_error(left, right):
    require(set(left) == set(right) == {"en", "ja"}, "metric languages")
    errors = []
    for lang in left:
        require(set(left[lang]) == set(right[lang]), "metric keys")
        for key, value in left[lang].items():
            other = right[lang][key]
            require(type(value) in (int, float) and type(other) in (int, float)
                    and math.isfinite(value) and math.isfinite(other), "finite metrics")
            errors.append(abs(value - other))
    return max(errors)


def metrics(rows, outputs):
    n = len(rows)
    require(set(outputs) == set(VIEWS) and n in (32, 64), "view/row schema")
    for value in outputs.values():
        require(isinstance(value, torch.Tensor) and value.shape == (n, 256)
                and value.dtype == torch.float64 and value.device.type == "cpu"
                and bool(torch.isfinite(value).all()), "finite output tensor")
    predictions = {v: outputs[v].argmax(-1).tolist() for v in VIEWS}
    targets = torch.tensor([r["target"] for r in rows], dtype=torch.int64)
    loss = F.cross_entropy(outputs["normal"], targets, reduction="none")
    result = {}
    for lang in ("en", "ja"):
        ids = [i for i, r in enumerate(rows) if r["language"] == lang]
        require(len(ids) == n // 2, "language balance")
        accuracy = {v: sum(predictions[v][i] == rows[i]["target"] for i in ids) / len(ids) for v in VIEWS}
        value = dict(rows=len(ids), accuracy=accuracy["normal"], answer_nll=float(loss[ids].mean()),
            evidence_blind_accuracy=accuracy["evidence_blind"], query_blind_accuracy=accuracy["query_blind"],
            evidence_drop=accuracy["normal"] - accuracy["evidence_blind"],
            query_drop=accuracy["normal"] - accuracy["query_blind"])
        for kind in ("fact", "query", "order"):
            groups = defaultdict(list)
            for i in ids:
                row = rows[i]
                key = (tuple(row["objects"]), tuple(sorted(row["values"])), row["order"], row["query"]) if kind == "fact" else (
                    row["group"], row["order"] if kind == "query" else row["query"])
                groups[key].append(i)
            require(len(groups) == n // 4 and all(len(g) == 2 for g in groups.values()), "pair completeness")
            require(all((rows[i]["target"] == rows[j]["target"]) == (kind == "order") for i, j in groups.values()), "pair semantics")
            value[kind + "_pair_accuracy"] = sum(all(predictions["normal"][i] == rows[i]["target"] for i in g)
                                                  for g in groups.values()) / len(groups)
        result[lang] = value
    return result, predictions


def parent_match(parts, outputs, ref):
    error = 0.0
    for split in SPLITS:
        measured, predictions = metrics(parts[split], outputs[split])
        require(predictions == ref["predictions"][split], "parent prediction replay")
        error = max(error, metric_error(measured, ref["final"][split]))
    require(error <= TOL, "parent metric replay")
    return error


def probe_forward(model, tokens, tasks, mode):
    require(mode in MODES and not any(m.training for m in model.modules()), "mode/frozen eval")
    require(not any(p.requires_grad for p in model.parameters()), "parameters must be frozen")
    norm = model.backbone.readout_norm
    require(isinstance(norm, nn.LayerNorm) and tuple(norm.normalized_shape) == (16,), "normalization contract")
    valid = tokens != 256
    eos = valid.sum(1) - 1
    require(tokens.dtype == tasks.dtype == torch.int64 and tokens.ndim == 2 and tokens.shape[1] == 48
            and tasks.shape == (len(tokens),) and bool((tasks == 0).all())
            and bool((eos >= 1).all()) and bool((tokens[torch.arange(len(tokens)), eos] == 258).all()), "input contract")
    capture = {}; counts = Counter(); routes = Counter(); handles = []
    def local_hook(module, args, output):
        counts["local"] += 1
        capture["pre"] = output[0][torch.arange(len(tokens)), eos]
    def core_hook(module, args, kwargs, output):
        route = kwargs.get("route_index"); routes[route] += 1
        if route == model.backbone.config.next_route:
            capture["core_post"] = output[torch.arange(len(tokens)), eos]
    def query_hook(module, args):
        counts["query"] += 1
        require(torch.equal(args[0], capture["pre"]), "pre-core query invariant")
    def reader_hook(module, args, output):
        counts["reader"] += 1; capture["read"] = output
    def before_norm(module, args):
        counts["pre_norm"] += 1; capture["post"] = args[0]
        require(torch.equal(capture["post"], capture["core_post"]), "untouched post-core residual")
    def after_norm(module, args, output):
        counts["post_norm"] += 1
        require(torch.equal(args[0], capture["post"] + capture["read"]), "parent residual addition")
        if mode in ("intact", "restored"):
            return None
        changed = capture["pre"] + capture["read"] if mode == "pre_residual" else capture["read"]
        return F.layer_norm(changed, norm.normalized_shape, norm.weight, norm.bias, norm.eps)
    try:
        handles.append(model.backbone.local_encoder.register_forward_hook(local_hook))
        handles.append(model.backbone.core.register_forward_hook(core_hook, with_kwargs=True))
        handles.append(model.read.query.register_forward_pre_hook(query_hook))
        handles.append(model.read.output.register_forward_hook(reader_hook))
        # Registered before C252 installs its own injection: this sees the untouched post-core state.
        handles.append(norm.register_forward_pre_hook(before_norm))
        handles.append(norm.register_forward_hook(after_norm))
        with torch.no_grad():
            logits = model(tokens, tasks)
    finally:
        for handle in handles:
            handle.remove()
    require(counts == {k: 1 for k in ("local", "query", "reader", "pre_norm", "post_norm")}, "hook call counts")
    cfg = model.backbone.config
    require(routes == {cfg.next_route: cfg.internal_steps, cfg.instruction_route: cfg.internal_steps}, "core route counts")
    require(logits.shape == (len(tokens), 256) and bool(torch.isfinite(logits).all()), "finite logits")
    components = {k: capture[k].detach().clone() for k in ("pre", "post", "read")}
    return logits.detach().clone(), components


def frozen_model(ref, state, parent, factory):
    model = parent.AlignedPrecoreReadout(factory.new_model(ref["seed"]), ref["seed"])
    model.load_state_dict(state, strict=True)
    model.eval(); model.requires_grad_(False)
    require(sum(p.numel() for p in model.parameters()) == 14256
            and factory.fingerprint(model) == ref["final_sha256"], "accepted checkpoint identity")
    return model


def diagnose_one(model, parts, ref, binding, fingerprint):
    before = fingerprint(model)
    require(before == ref["final_sha256"], "frozen model identity")
    inputs = {s: {v: binding.tensors(parts[s], v)[0] for v in VIEWS} for s in SPLITS}
    outputs = {}; components = {}; counts = [0, 0]
    def count(module, args, output):
        counts[0] += 1; counts[1] += len(args[0])
    handle = model.register_forward_hook(count)
    try:
        for mode in MODES:
            outputs[mode] = {}; components[mode] = {}
            for split in SPLITS:
                outputs[mode][split] = {}; components[mode][split] = {}
                for view in VIEWS:
                    tokens = inputs[split][view]
                    result, signals = probe_forward(model, tokens, torch.zeros(len(tokens), dtype=torch.int64), mode)
                    outputs[mode][split][view] = result; components[mode][split][view] = signals
                    require(fingerprint(model) == before, "weight mutation")
                    if mode != "intact":
                        require(all(torch.equal(signals[k], components["intact"][split][view][k]) for k in signals), "component drift")
            if mode == "intact":
                parent_match(parts, outputs[mode], ref)
    finally:
        handle.remove()
    require(counts == [24, 1152], "measured diagnostic workload")
    require(fingerprint(model) == before and not any(m.training for m in model.modules()), "final frozen state")
    return dict(seed=ref["seed"], outputs=outputs, components=components, forward_calls=counts[0], row_presentations=counts[1],
                final_sha256=before, weights_preserved=True)


def analyze(parts, entries, refs):
    require([e["seed"] for e in entries] == [r["seed"] for r in refs] == list(SEEDS), "all five identities")
    diagnostics = []; contrasts = []
    for entry, ref in zip(entries, refs, strict=True):
        require(entry["final_sha256"] == ref["final_sha256"] and entry["weights_preserved"] is True
                and (entry["forward_calls"], entry["row_presentations"]) == (24, 1152), "entry integrity")
        outputs, signals = entry["outputs"], entry["components"]
        require(set(outputs) == set(signals) == set(MODES), "mode coverage")
        error = parent_match(parts, outputs["intact"], ref); measured = {}; prediction = {}
        for mode in MODES:
            require(set(outputs[mode]) == set(signals[mode]) == set(SPLITS), "split coverage")
            measured[mode] = {}; prediction[mode] = {}
            for split in SPLITS:
                require(set(signals[mode][split]) == set(VIEWS), "component views")
                measured[mode][split], prediction[mode][split] = metrics(parts[split], outputs[mode][split])
                for view in VIEWS:
                    c = signals[mode][split][view]
                    require(set(c) == {"pre", "post", "read"}, "component schema")
                    for key, value in c.items():
                        require(isinstance(value, torch.Tensor) and value.shape == (ROWS[split], 16)
                                and value.dtype == torch.float64 and value.device.type == "cpu"
                                and bool(torch.isfinite(value).all()), "component tensor")
                        require(torch.equal(value, signals["intact"][split][view][key]), "persisted component invariance")
                    if mode == "restored":
                        drift = float((outputs[mode][split][view] - outputs["intact"][split][view]).abs().max())
                        require(drift <= TOL and prediction[mode][split][view] == prediction["intact"][split][view], "restored output replay")
        diagnostics.append(dict(seed=entry["seed"], parent_metric_error=error, metrics=measured))
        for mode in ("pre_residual", "reader_only"):
            for split in SPLITS:
                rows = parts[split]
                old = prediction["intact"][split]["normal"]; new = prediction[mode][split]["normal"]
                for lang in ("en", "ja"):
                    ids = [i for i, r in enumerate(rows) if r["language"] == lang]
                    a = measured["intact"][split][lang]; c = measured[mode][split][lang]
                    contrasts.append(dict(seed=entry["seed"], mode=mode, split=split, language=lang, rows=len(ids),
                        original_correct=sum(old[i] == rows[i]["target"] for i in ids),
                        changed_correct=sum(new[i] == rows[i]["target"] for i in ids),
                        wrong_to_correct=sum(old[i] != rows[i]["target"] and new[i] == rows[i]["target"] for i in ids),
                        correct_to_wrong=sum(old[i] == rows[i]["target"] and new[i] != rows[i]["target"] for i in ids),
                        answer_flips=sum(old[i] != new[i] for i in ids), accuracy_delta=c["accuracy"]-a["accuracy"],
                        nll_delta=c["answer_nll"]-a["answer_nll"],
                        logit_max_abs=float((outputs[mode][split]["normal"][ids]-outputs["intact"][split]["normal"][ids]).abs().max()),
                        component_mean_norm={k: float(signals["intact"][split]["normal"][k][ids].norm(dim=-1).mean()) for k in ("pre", "post", "read")}))
    summary = dict(models=5, diagnostic_cells=80, contrast_cells=len(contrasts), model_forward_calls=120,
        row_presentations=5760, new_training_steps=0, parent_bundle_loads=1, model_state_loads=5,
        new_checkpoint_writes=0, parent_predictions_replayed=True, parent_metrics_replayed=True,
        components_unchanged=True, restored_outputs_replayed=True, weights_preserved=True,
        nll_recomputed=True, capability_pass_claim=False, causal_mechanism_claim=False)
    require(len(contrasts) == 40, "contrast count")
    return diagnostics, contrasts, summary


def load_inputs(c252_summary):
    parent, _, fitting, _, _, a = context(); path = Path(c252_summary).resolve()
    require(a.sha(path) == PARENT_SHA, "parent summary hash")
    p = a.read_json(path); parent.validate_result(p)
    parts = a.read_json(path.parent / "split-dataset.json")
    require(set(parts) == set(SPLITS) and {s: len(parts[s]) for s in SPLITS} == ROWS
            and digest(parts) == PARENT_ARTIFACTS["split-dataset.json"], "exact partition")
    refs = a.read_json(path.parent / "measurements.json")
    require(parent.summarize(refs, fitting) == p["validation_summary"]
            and [(r["seed"], r["family"], r["arm"]) for r in refs] == [(s, "full", "aligned_precore_read") for s in SEEDS], "parent final records")
    return parts, refs


def precheck(c252_summary, root):
    parent, _, _, _, factory, a = context(); path = Path(c252_summary).resolve(); root = Path(root)
    require(a.sha(path) == PARENT_SHA, "parent summary identity")
    p = a.read_json(path); parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "FAIL"
            and p["validation_summary"]["seed_pass_count"] == 4
            and p["validation_summary"]["cell_outcomes"] == {"BOTH_PASS": 8, "RECOMBINATION_MISS": 2}, "accepted parent")
    pins, protected = dict(p["source_blobs"]), dict(p["input_sha256"])
    for name, wanted in protected.items():
        require(Path(name).is_file() and a.sha(name) == wanted, "changed input:" + name)
    for name, wanted in pins.items():
        require(a.git(root, "rev-parse", "HEAD:"+name).decode().strip() == wanted, "changed source:"+name)
    require(str(path) not in protected, "parent double count"); protected[str(path)] = PARENT_SHA
    require({x["file"]: x["sha256"] for x in p["artifacts"]} == PARENT_ARTIFACTS, "parent artifacts")
    for item in p["artifacts"]:
        child = a.safe_child(path.parent, item["file"])
        require(a.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "parent artifact bytes")
        require(str(child.resolve()) not in protected, "artifact double count")
        protected[str(child.resolve())] = item["sha256"]
    for name in OWN:
        require(name not in pins, "OWN collision"); pins[name] = a.git(root, "rev-parse", "HEAD:"+name).decode().strip()
    helpers = (
        "gate_f_c230_prepared_capsule.py",
        "model_c231_byte_eval_contract.py",
        "model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py",
        "model_c234_context_binding.py",
        "model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py",
        "model_c237_frozen_signal_audit.py",
        "model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py",
        "model_c240_saved_position_audit.py",
        "model_c241_assignment_holdout.py",
        "model_c242_balanced_recombination.py",
        "model_c243_saved_recombination_audit.py",
        "model_c244_two_partner_recombination.py",
        "model_c245_selective_evidence.py",
        "model_c246_training_erasure.py",
        "model_c247_normal_exposure_control.py",
        "model_c248_residual_token_read.py",
        "model_c249_frozen_read_ablation.py",
        "model_c250_fresh_seed_replication.py",
        "model_c251_precore_read.py",
        "model_c252_precore_query_alignment.py",
    )
    required = set(factory.LM_SOURCES) | {"fold_lm/v05_benchmarks/"+h for h in helpers} | {OWN[0]}
    require(len(required) == 29 and required <= set(pins), "deciding dependency coverage")
    protected.update(a.protect_tree_files(root, pins))
    require((len(pins), len(protected)) == (364, 587) and digest(manifest()) == MANIFEST_SHA, "protection/manifest counts")
    return pins, protected


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["status"] == "PASS"
            and p["diagnostic_execution_valid"] is True, "diagnostic status")
    require((len(p["source_blobs"]), len(p["input_sha256"])) == (364, 587)
            and set(OWN) <= set(p["source_blobs"]), "result protection")
    require(len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS, "artifact coverage")
    s = p["validation_summary"]; m = manifest()
    for key in ("model_forward_calls", "row_presentations", "new_training_steps", "parent_bundle_loads", "model_state_loads",
                "new_checkpoint_writes", "diagnostic_cells", "contrast_cells"):
        require(type(s[key]) is int and s[key] == m[key], "result count:"+key)
    require(s["models"] == 5 and all(s[k] is True for k in ("parent_predictions_replayed", "parent_metrics_replayed",
            "components_unchanged", "restored_outputs_replayed", "weights_preserved", "nll_recomputed")), "replay flags")
    require(s["capability_pass_claim"] is False and s["causal_mechanism_claim"] is False
            and p["gate_f_candidate"] is False and p["production_adoption"] is False and p["network_calls"] == 0, "claim boundary")


def regression_modules(root):
    names = parent_module().regression_modules(root)
    require(len(names) == len(set(names)) == 137, "parent modules")
    return names + ["tests_lm.test_v05_c253_frozen_residual_path"]


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1, "test identities")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require((len(tests), len(kept)) == (3242, 3241), "suite counts")
    return unittest.TestSuite(kept)


def run(*, c252_summary, output_dir, expected_head):
    parent, _, _, binding, factory, a = context(); root = Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root, "rev-parse", "HEAD").decode().strip() == expected_head, "HEAD")
        require(a.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss", "branch")
        require(not a.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "dirty tracked tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins, protected = precheck(c252_summary, root); parts, refs = load_inputs(c252_summary)
    states = parent.load_bundle(Path(c252_summary).resolve().parent / "trained-models.pt")
    require(len(states) == len(refs) == 5, "checkpoint count")
    entries = []
    for ref, state in zip(refs, states, strict=True):
        print(f'[C253] model={len(entries)+1}/5 seed={ref["seed"]}; frozen residual diagnostic', flush=True)
        model = frozen_model(ref, state, parent, factory)
        entries.append(diagnose_one(model, parts, ref, binding, factory.fingerprint))
    diagnostics, contrasts, summary = analyze(parts, entries, refs)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False)
    torch.save(dict(schema="fold-c253-frozen-outputs-v1", entries=entries), out / "outputs.pt")
    for name, value in (("residual-plan.json", manifest()), ("diagnostics.json", diagnostics),
                        ("contrasts.json", contrasts), ("validation-summary.json", summary)):
        (out / name).write_bytes(blob(value))
    artifacts = [dict(file=n, sha256=a.sha(out/n), serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard(); precheck(c252_summary, root)
    for name, wanted in protected.items():
        require(a.sha(name) == wanted, "modified input")
    p = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head, status="PASS", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256=protected, artifacts=artifacts, validation_summary=summary,
        gate_f_candidate=False, production_adoption=False, network_calls=0)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    print("=== C253 RESULT ===", flush=True); print(blob(p).decode(), flush=True)
    return p


def verify_artifacts(output_dir, c252_summary, expected_head):
    _, _, _, _, _, a = context(); out = Path(output_dir); p = a.read_json(out/"summary.json")
    validate_result(p); require(p["commit_sha"] == expected_head, "saved HEAD")
    for name, wanted in p["input_sha256"].items():
        require(a.sha(name) == wanted, "postcheck input")
    for item in p["artifacts"]:
        child = a.safe_child(out, item["file"])
        require(a.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "saved artifact")
    data = torch.load(out/"outputs.pt", map_location="cpu", weights_only=True)
    require(set(data) == {"schema", "entries"} and data["schema"] == "fold-c253-frozen-outputs-v1", "output archive schema")
    parts, refs = load_inputs(c252_summary)
    diagnostics, contrasts, summary = analyze(parts, data["entries"], refs)
    for name, value in (("residual-plan.json", manifest()), ("diagnostics.json", diagnostics),
                        ("contrasts.json", contrasts), ("validation-summary.json", summary)):
        require(a.read_json(out/name) == value, "persisted recomputation:"+name)
    require(summary == p["validation_summary"], "saved summary replay")
    return p, diagnostics, contrasts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("c252-summary", "output-dir"):
        parser.add_argument("--"+name, type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
