"""C300: frozen inference interventions on the actual pre-normalization readout sum."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
from types import ModuleType
import unittest
import torch

EXPERIMENT_ID = "C300-v5b-frozen-readout-term-ablation"
STAGE = "V5-B-FROZEN-READOUT-TERM-ABLATION"
BASE = "c726cc8d1c587328943229276d6588fb59386a06"
PARENT_EXECUTION = "1ef1436febee7b2a70b2b91cb7a5dcb2a9e04d0c"
PARENT_SHA = "d0b2c055e190a313e5abc399716e2ec0cddfb104cc447a6216f2fab0ed312851"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c299_core_initialization.py"
PARENT_BLOB = "b97749c29217b0ad9c57a4bf61d668684e391880"
READOUT_SOURCE = "fold_lm/v05_benchmarks/model_c278_mean_final_dual_query.py"
READOUT_BLOB = "0aa8d65874f4a021e21d04948ffd0a1d5615248b"
LEVELS = (297001, 297002, 297003)
MODES = ("full_before", "residual_only", "reader_only", "full_after")
TASKS = ("two_char", "triple", "quad")
SPLITS = ("TRAIN", "HOLDOUT")
OWN = ("fold_lm/v05_benchmarks/model_c300_frozen_readout_terms.py",
       "tests_lm/test_v05_c300_frozen_readout_terms.py", "tools/run_c300.ps1", "tools/invoke_c300.ps1",
       "docs/experiment-ledger-addendum-c300-preregistration.md", "docs/v5b-frozen-readout-terms-v0.1.md")
OUTPUTS = ("intervention-plan.json", "intervention-evaluations.pt", "measurements.json", "validation-summary.json")
PARENT_OUTPUTS = ("architecture-plan.json", "dataset.json", "triple-dataset.json", "quad-dataset.json",
                  "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=9, train_steps=0, model_forward_calls=2916, row_presentations=279936,
            core_forward_calls=11664, model_state_loads=9, checkpoint_bundle_loads=1,
            new_checkpoint_writes=0, network_calls=0)
MANIFEST_SHA = "31d1418e00e6a26cd5f541f47353bf3d947e4feebf0c807a87e8b7e069ef2e30"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(LEVELS, LEVELS))


def context():
    from fold_lm.v05_benchmarks import model_c299_core_initialization as parent
    _, _, _, audit, diagnostic, evaluation, transfer, training, c = parent.context()
    return parent, audit, diagnostic, evaluation, transfer, training, c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_summary_sha256=PARENT_SHA,
        parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
        readout_source=READOUT_SOURCE, readout_blob=READOUT_BLOB,
        question="which frozen predictions are rescued or lost when either pre-normalization readout summand is suppressed",
        cohort="all9 C299 learned remaining/core combinations,not selected successes or fresh training",
        levels=list(LEVELS), modes=list(MODES), parameters=14256, max_tokens=48,
        intervention="normalizer input r+a;residual_only=r;reader_only=a;all earlier computation still executes",
        provenance="capture r before C278 hook and a at read.output;late hook requires exact r+a identity before replacement",
        restoration="full before/after reproduce all original task/view logits<=1e-9 and exact argmax;weights and hook registries unchanged",
        gates=dict(accuracy=.90, query_pair=.80, evidence_drop=.35, query_drop=.35, two_order=.80),
        interpretation="inference-time interventions on jointly trained terms,not additive logit attribution,training-cause proof or deployment policy",
        partitions=216, comparisons=108, matched_normal_rows=46656, raw_logit_payload_bytes=573308928,
        parents=26, source_pins=646, protected_inputs=1191, own_tests=40,
        modules=185, loaded_tests=4598, focused_tests=4597, excluded_test=EXCLUDED,
        dtype="CPU float64", threads=2, deterministic=True, capability_gate_applicable=False,
        gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None and digest(manifest()) == MANIFEST_SHA, "manifest seal")


def expected_matrices():
    seen = [[True, False, False], [True, True, True], [True, True, True]]
    return dict(two_char=seen, triple=seen, quad=[[True, False, False], [False, False, False], [True, False, True]])


def hook_snapshot(model):
    return tuple((name, tuple(m._forward_pre_hooks), tuple(m._forward_hooks)) for name, m in model.named_modules())


@contextmanager
def intervene(model, mode):
    """Keep C278's forward intact; intercept only its verified r+a normalizer input."""
    require(mode in MODES, "intervention mode")
    require(not torch.is_grad_enabled() and not any(m.training for m in model.modules())
            and not any(p.requires_grad for p in model.parameters()), "frozen intervention only")
    norm = model.backbone.readout_norm
    before = hook_snapshot(model)
    state, late, handles = {}, [], []
    stats = dict(calls=0, formula_checks=0)

    def begin(module, args):
        require(not state and not late, "reentrant intervention")
        state["batch"] = len(args[0]); stats["calls"] += 1

    def capture_residual(module, args):
        require("batch" in state and "residual" not in state and len(args) == 1, "residual capture order")
        state["residual"] = args[0].detach().clone()

    def capture_reader(module, args, output):
        require("residual" in state and "reader" not in state, "reader capture order")
        state["reader"] = output.detach().clone()

    def replace(module, args):
        require(set(state) == {"batch", "residual", "reader"} and len(args) == 1, "sum capture coverage")
        r, a = state["residual"], state["reader"]
        require(r.shape == a.shape == args[0].shape == (state["batch"], 16)
                and r.dtype == a.dtype == args[0].dtype == torch.float64
                and r.device.type == a.device.type == "cpu"
                and bool(torch.isfinite(r).all()) and bool(torch.isfinite(a).all()), "summand contract")
        require(torch.equal(args[0], r+a), "actual C278 sum identity")
        stats["formula_checks"] += 1
        if mode == "residual_only": return (r,)
        if mode == "reader_only": return (a,)
        return None

    def arm_late_hook(module, args, output):
        # C278 has registered its own norm hook before calling the local encoder.
        require("batch" in state and not late, "local encoder call count")
        late.append(norm.register_forward_pre_hook(replace))

    def finish(module, args, output):
        for handle in late: handle.remove()
        late.clear(); state.clear()

    try:
        handles.append(model.register_forward_pre_hook(begin))
        handles.append(norm.register_forward_pre_hook(capture_residual))
        handles.append(model.read.output.register_forward_hook(capture_reader))
        handles.append(model.backbone.local_encoder.register_forward_hook(arm_late_hook))
        handles.append(model.register_forward_hook(finish, always_call=True))
        yield stats
        require(stats["calls"] > 0 and stats["calls"] == stats["formula_checks"] and not state and not late, "intervention call coverage")
    finally:
        for handle in late+handles: handle.remove()
        require(hook_snapshot(model) == before, "hook restoration")


def load_parent(paths):
    parent, audit, *_, c = context(); paths = [Path(p).resolve() for p in paths]
    hashes = (PARENT_SHA, *parent.parent_hashes(parent.context()[0]))
    require(len(paths) == len(hashes) == 26 and all(c.audit.sha(p) == h for p, h in zip(paths, hashes, strict=True)), "parent hashes")
    with audit.no_neural():
        payload, _ = parent.verify_artifacts(paths[0].parent, paths[1:], PARENT_EXECUTION); parent.validate_result(payload)
        require(payload["experiment_id"] == "C299-v5b-core-initialization-grid" and payload["commit_sha"] == PARENT_EXECUTION
                and payload["status"] == "PASS" and payload["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB
                and payload["source_blobs"].get(READOUT_SOURCE) == READOUT_BLOB, "parent identity")
        s = payload["validation_summary"]
        require(s["task_pass_matrices"] == expected_matrices() and s["diagnostic_complete"] is True
                and s["capability_gate_applicable"] is False and s["components_matched"] is True and s["all_replays"] is True, "parent outcome")
        require(len(payload["artifacts"]) == 8 and {a["file"] for a in payload["artifacts"]} == set(PARENT_OUTPUTS), "parent outputs")
        data = [c.audit.read_json(paths[0].parent/n) for n in PARENT_OUTPUTS[1:4]]
        require(tuple(map(digest, data)) == tuple(parent.DATA_HASHES), "data hashes")
        archive = torch.load(paths[0].parent/"evaluations.pt", map_location="cpu", weights_only=True)
        require(set(archive) == {"schema", "records"} and archive["schema"] == "fold-c299-core-eval-v1", "parent archive")
        parent.check_grid(archive["records"])
    return payload, *data, archive["records"]


def precheck(paths, root):
    validate_seal(); payload, *_ = load_parent(paths); parent, audit, *_, c = context(); root = Path(root).resolve()
    pins, protected = dict(payload["source_blobs"]), dict(payload["input_sha256"])
    require((len(pins), len(protected)) == (640, 1176), "inherited counts")
    for n, h in pins.items(): require(c.audit.git(root, "rev-parse", "HEAD:"+n).decode().strip() == h, "changed source:"+n)
    for n, h in protected.items(): require(Path(n).is_file() and c.audit.sha(n) == h, "changed input:"+n)
    covered = set()
    for module in [parent, audit, *parent.context(), *vars(c).values()]:
        path = getattr(module, "__file__", None) if isinstance(module, ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            n = Path(path).resolve().relative_to(root).as_posix(); require(n in pins, "unprotected helper:"+n); covered.add(n)
    require(PARENT_SOURCE in covered and pins.get(READOUT_SOURCE) == READOUT_BLOB, "readout source coverage")
    entries = [(Path(paths[0]).resolve(), PARENT_SHA)] + [(c.audit.safe_child(Path(paths[0]).resolve().parent, a["file"]), a["sha256"]) for a in payload["artifacts"]]
    for path, h in entries:
        require(str(path.resolve()) not in protected and c.audit.sha(path) == h, "parent input"); protected[str(path.resolve())] = h
    for n in OWN:
        require(n not in pins, "OWN collision"); pins[n] = c.audit.git(root, "rev-parse", "HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root, pins))
    require((len(pins), len(protected)) == (646, 1191), "protection counts")
    print(f"registration_check = source_pins:646; protected_inputs:1191; manifest_sha256:{MANIFEST_SHA}", flush=True)
    return pins, protected


def runtime_preflight(paths, root):
    precheck(paths, root); parent, _, _, _, _, training, c = context(); _, data, _, _, anchors = load_parent(paths)
    states = parent.load_bundle(Path(paths[0]).resolve().parent/"trained-models.pt")
    model = parent.make_grid(c)[identities()[0]]; model.load_state_dict(states[0], strict=True); model.eval(); model.requires_grad_(False)
    require(c.base.fingerprint(model) == anchors[0]["final_sha256"], "real checkpoint")
    tokens, _ = training.training_tables(data, c); x = tokens[0, 0, :48]; tasks = torch.zeros(48, dtype=torch.int64)
    start = c.base.fingerprint(model)
    with torch.no_grad():
        plain = model(x, tasks)
        for mode in MODES:
            with intervene(model, mode): value = model(x, tasks)
            c.p267.check_logits(value, 48)
            if mode.startswith("full"): require(torch.equal(value, plain), "instrumented identity smoke")
    require(c.base.fingerprint(model) == start, "smoke state preserved")
    print("real_frozen_checkpoint_and_readout_hook_smoke = PASS; operational preflight only", flush=True)


def infer_cell(model, state, anchor, data, triple, quad, evaluation, transfer, c):
    model.load_state_dict(state, strict=True); model.eval(); model.requires_grad_(False)
    start = c.base.fingerprint(model); require(start == anchor["final_sha256"], "strict state fingerprint")
    snapshots = hook_snapshot(model); outputs, attestations = {}, {}
    for mode in MODES:
        print(f"[C300] remaining={anchor['remaining_seed']} core={anchor['core_seed']} mode={mode}", flush=True)
        with torch.no_grad(), c.p267.counted(model, c.core) as (calls, cores):
            with intervene(model, mode) as stats: raw = evaluation.evaluate(model, data, triple, quad, transfer, c)
        require(calls == [81, 7776] and cores[0] == 324 and stats == dict(calls=81, formula_checks=81), "mode workload")
        require(c.base.fingerprint(model) == start and hook_snapshot(model) == snapshots, "frozen state/hooks")
        outputs[mode] = raw; attestations[mode] = dict(stats)
    errors = [evaluation.replay_error(outputs[m], anchor["raw"], data, c) for m in (MODES[0], MODES[-1])]
    restoration = evaluation.replay_error(outputs[MODES[0]], outputs[MODES[-1]], data, c)
    return dict(remaining_seed=anchor["remaining_seed"], core_seed=anchor["core_seed"], final_sha256=start,
                raw=outputs, mode_attestations=attestations, before_error=errors[0], after_error=errors[1],
                restoration_error=restoration, weights_preserved=True, hooks_restored=True)


def compare_normal(left, right, data):
    rows = flips = rescued = regressed = control_correct = changed_correct = 0
    for profile in left:
        require(profile in right, "profile matching")
        a, b = left[profile]["normal"], right[profile]["normal"]
        require(a.shape == b.shape == (len(data), 256), "comparison shape")
        targets = torch.tensor([r["target"] for r in data], dtype=torch.int64)
        x, y = a.argmax(1), b.argmax(1); ca, cb = x == targets, y == targets
        rows += len(data); flips += int((x != y).sum()); rescued += int((~ca & cb).sum()); regressed += int((ca & ~cb).sum())
        control_correct += int(ca.sum()); changed_correct += int(cb.sum())
    require(changed_correct-control_correct == rescued-regressed, "paired count identity")
    return dict(rows=rows, argmax_flips=flips, rescued=rescued, regressed=regressed,
                control_correct=control_correct, ablated_correct=changed_correct)


def analyze(records, anchors, data, diagnostic, evaluation, transfer, c):
    require([(r["remaining_seed"], r["core_seed"]) for r in records] == identities()
            and [(r["remaining_seed"], r["core_seed"]) for r in anchors] == identities(), "complete cohort")
    metrics, results, parts, comparisons, reproductions = [], [], [], [], []
    for r, old in zip(records, anchors, strict=True):
        key = dict(remaining_seed=r["remaining_seed"], core_seed=r["core_seed"])
        require(r["final_sha256"] == old["final_sha256"] and r["weights_preserved"] is True and r["hooks_restored"] is True, "record integrity")
        require(set(r["raw"]) == set(MODES) and r["mode_attestations"] == {m:dict(calls=81, formula_checks=81) for m in MODES}, "mode inventory")
        errors = [evaluation.replay_error(r["raw"][m], old["raw"], data, c) for m in (MODES[0], MODES[-1])]
        errors.append(evaluation.replay_error(r["raw"][MODES[0]], r["raw"][MODES[-1]], data, c))
        for name, error in zip(("before_error", "after_error", "restoration_error"), errors, strict=True):
            require(type(error) in (int, float) and math.isfinite(error) and 0 <= error <= 1e-9 and r[name] == error, "reproduction")
        reproductions.append(dict(**key, before_error=errors[0], after_error=errors[1], restoration_error=errors[2], matched=True))
        for mode in MODES:
            raw = r["raw"][mode]; require(set(raw) == set(TASKS), "task inventory")
            scored = dict(two_char=c.p267.score(data, raw["two_char"]), triple=c.c270.score(data, raw["triple"], c.p267), quad=transfer.score_quad(data, raw["quad"], c))
            flags = {t+"_pass":scored[t]["passed"] for t in TASKS}; require(all(type(v) is bool for v in flags.values()), "task flags")
            results.append(dict(**key, mode=mode, all_tasks_pass=all(flags.values()), **flags)); metrics.append(dict(**key, mode=mode, **scored))
            for task in TASKS:
                normalized = diagnostic.normalize_task(scored[task], task, r["remaining_seed"], str(r["core_seed"])+":"+mode)
                for split in SPLITS:
                    part = diagnostic.partition([x for x in normalized if x["split"] == split]); parts.append(dict(**key, mode=mode, task=task, split=split, **part))
        for mode, task, split in itertools.product(MODES[1:3], TASKS, SPLITS):
            comparisons.append(dict(**key, mode=mode, task=task, split=split,
                **compare_normal(r["raw"][MODES[0]][task][split], r["raw"][mode][task][split], data[split])))
    matrices = {}
    for mode in MODES:
        rr = [r for r in results if r["mode"] == mode]
        matrices[mode] = {t:[[rr[3*i+j][t+"_pass"] for j in range(3)] for i in range(3)] for t in TASKS}
    require(all(matrices[m] == expected_matrices() for m in (MODES[0], MODES[-1])), "original capability matrix reproduction")
    require((len(results), len(parts), len(comparisons)) == (36, 216, 108)
            and sum(r["rows"] for r in comparisons) == 46656, "audit inventory")
    summary = dict(cell_results=results, final_partitions=parts, comparisons=comparisons, reproductions=reproductions,
        task_pass_matrices=matrices, diagnostic_complete=True, capability_gate_applicable=False,
        all_weights_preserved=True, all_hooks_restored=True, **WORK)
    return metrics, summary


def validate_result(payload):
    require(payload["experiment_id"] == EXPERIMENT_ID and payload["stage"] == STAGE and payload["status"] == "PASS"
            and payload["diagnostic_execution_valid"] is True, "diagnostic identity")
    require(all(payload[k] is False for k in ("capability_gate_applicable", "gate_f_candidate", "production_adoption")), "scope")
    require((len(payload["source_blobs"]), len(payload["input_sha256"])) == (646, 1191) and set(OWN) <= set(payload["source_blobs"])
            and payload["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB and payload["source_blobs"].get(READOUT_SOURCE) == READOUT_BLOB, "protection")
    require(len(payload["artifacts"]) == 4 and {a["file"] for a in payload["artifacts"]} == set(OUTPUTS), "artifacts")
    s = payload["validation_summary"]
    require(all(type(s[k]) is int and s[k] == v for k, v in WORK.items()), "workload")
    require((len(s["cell_results"]), len(s["final_partitions"]), len(s["comparisons"]), len(s["reproductions"])) == (36,216,108,9), "inventory")
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False
            and s["all_weights_preserved"] is True and s["all_hooks_restored"] is True, "integrity flags")
    require(all(s["task_pass_matrices"][m] == expected_matrices() for m in (MODES[0], MODES[-1])), "original gates")
    require([(r["remaining_seed"],r["core_seed"],r["mode"]) for r in s["cell_results"]]
            == [(i,j,m) for i,j in identities() for m in MODES], "result order")
    for r in s["reproductions"]:
        require(r["matched"] is True and all(type(r[k]) in (int,float) and math.isfinite(r[k]) and 0<=r[k]<=1e-9
                for k in ("before_error", "after_error", "restoration_error")), "reproduction bounds")


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite): yield from flatten(test)
        else: yield test


def regression_modules(root):
    names = context()[0].regression_modules(root); require(len(names) == len(set(names)) == 184, "parent modules")
    return names+["tests_lm.test_v05_c300_frozen_readout_terms"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) == manifest()["loaded_tests"] and ids.count(EXCLUDED) == 1, "loaded suite")
    kept = [t for t in tests if t.id() != EXCLUDED]; require(len(kept) == manifest()["focused_tests"], "focused suite")
    return unittest.TestSuite(kept)


def guard(root, head, c):
    require(c.audit.git(root, "rev-parse", "HEAD").decode().strip() == head
            and c.audit.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss"
            and not c.audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "repository guard")


def run(*, summaries, output_dir, expected_head):
    parent, _, diagnostic, evaluation, transfer, _, c = context(); root = Path(__file__).resolve().parents[2]
    guard(root, expected_head, c); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins, protected = precheck(summaries, root); _, data, triple, quad, anchors = load_parent(summaries)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False)
    states = parent.load_bundle(Path(summaries[0]).resolve().parent/"trained-models.pt"); models = parent.make_grid(c)
    records = [infer_cell(models[key], states[i], anchors[i], data, triple, quad, evaluation, transfer, c) for i, key in enumerate(identities())]
    metrics, summary = analyze(records, anchors, data, diagnostic, evaluation, transfer, c)
    torch.save(dict(schema="fold-c300-readout-terms-eval-v1", records=records), out/OUTPUTS[1])
    for n, v in ((OUTPUTS[0], manifest()), (OUTPUTS[2], metrics), (OUTPUTS[3], summary)): (out/n).write_bytes(blob(v))
    artifacts = [dict(file=n, sha256=c.audit.sha(out/n), serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root, expected_head, c); precheck(summaries, root)
    payload = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head, status="PASS", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256=protected, artifacts=artifacts, validation_summary=summary,
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False)
    validate_result(payload); (out/"summary.json").write_bytes(blob(payload))
    receipt = {k:payload[k] for k in ("experiment_id", "stage", "commit_sha", "status", "artifacts")}
    receipt["summary_sha256"] = c.audit.sha(out/"summary.json")
    print("=== C300 COMPACT DIAGNOSTIC RECEIPT ===", flush=True); print(json.dumps(receipt, sort_keys=True, indent=2), flush=True)
    return payload


def verify_artifacts(outdir, summaries, expected_head):
    _, audit, diagnostic, evaluation, transfer, _, c = context(); out = Path(outdir)
    payload = c.audit.read_json(out/"summary.json"); validate_result(payload); require(payload["commit_sha"] == expected_head, "execution HEAD")
    for n, h in payload["input_sha256"].items(): require(c.audit.sha(n) == h, "protected input")
    for a in payload["artifacts"]:
        path = c.audit.safe_child(out, a["file"]); require(c.audit.sha(path) == a["sha256"] and path.stat().st_size == a["serialized_bytes"], "output bytes")
    with audit.no_neural():
        _, data, _, _, anchors = load_parent(summaries)
        archive = torch.load(out/OUTPUTS[1], map_location="cpu", weights_only=True)
        require(set(archive) == {"schema", "records"} and archive["schema"] == "fold-c300-readout-terms-eval-v1", "evaluation schema")
        metrics, summary = analyze(archive["records"], anchors, data, diagnostic, evaluation, transfer, c)
        for n, v in ((OUTPUTS[0], manifest()), (OUTPUTS[2], metrics), (OUTPUTS[3], summary)): require(c.audit.read_json(out/n) == v, "persisted:"+n)
    require(summary == payload["validation_summary"], "summary reconstruction")
    return payload, metrics


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--summaries", nargs=26, type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True); parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__": main()
