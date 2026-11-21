"""C257: frozen transfer to the four fact orders withheld by C256; no training."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C257-v5b-unseen-fact-order-transfer"
STAGE = "V5-B-UNSEEN-FACT-ORDER-TRANSFER"
BASE = "ee4c282687c71bed407ecb687659edd7103c740d"
PARENT_EXECUTION = "db9f3cb90d9268066c34fc91300193058301f06c"
PARENT_SHA = "56c9c4e46800aadfb3c1a125522a66c6c2014721eceac0ab29ccd08c005bd184"
PARENT_ARTIFACTS = {
    "dataset.json": "ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b",
    "measurements.json": "f7d11d7592769e54824d3d7dccc4e481029dc5157b6c35c333831408d7b032c8",
    "task-plan.json": "43948ceb676d536301d4e3a63a7ee1407f8bec44034db59f8b4f6e4872ae53b1",
    "trained-models.pt": "72d9ada52e48395290200c1c6918d7eef091aebd44a3d2a6176dc1dd442dae3a",
    "validation-summary.json": "a25fe29ed2deb33ceab64c0f7d7e450e6a143ea5c0bc428eea20b9d45dff8bc2",
}
SEEDS = (256001, 256002, 256003, 256004, 256005)
ARMS = ("aligned_precore_read", "eos_adapter")
SPLITS, VIEWS = ("TRAIN", "HOLDOUT"), ("normal", "evidence_blind", "query_blind")
KNOWN = ((0, 1, 2), (2, 1, 0))
NOVEL = ((0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1))
ENTITIES = {"en": ("a", "b", "c"), "ja": ("甲", "乙", "丙")}
TOL = 1e-9
ORDER_SHA = "9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052"
MANIFEST_SHA = "18fdc13e9c276826473467243017f30b1fa6dcf673a9a490e14318792f8a8e36"
OWN = ("fold_lm/v05_benchmarks/model_c257_unseen_fact_order.py",
       "tests_lm/test_v05_c257_unseen_fact_order.py", "tools/run_c257.ps1", "tools/invoke_c257.ps1",
       "docs/experiment-ledger-addendum-c257-preregistration.md", "docs/v5b-unseen-fact-order-v0.1.md")
OUTPUTS = {"order-plan.json", "order-dataset.json", "eval-outputs.pt", "measurements.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def context():
    from fold_lm.v05_benchmarks import model_c256_three_entity_task_shift as parent
    _, c252, reader, factory, audit = parent.context()
    return parent, c252, reader, factory, audit


def identities():
    return list(itertools.product(SEEDS, ARMS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        order_dataset_sha256=ORDER_SHA, seeds=list(SEEDS), arms=list(ARMS),
        known_orders=[list(x) for x in KNOWN], new_orders=[list(x) for x in NOVEL],
        original_rows_per_split=144, new_rows_per_split=288, views=list(VIEWS),
        intervention="only fact permutation; original query, assignment, language, target and final weights fixed",
        primary="all five candidate seeds pass original cells, every new order cell, and all-six-order consistency",
        gate=dict(accuracy=.90, query_triplet=.80, evidence_drop=.35, query_drop=.35, six_order=.80),
        per_new_order_language_rows=36, per_new_order_query_triplets=12, six_order_groups_per_language=36,
        models=10, parameters=14256, model_forward_calls=180, row_presentations=34560,
        original_forwards=60, novel_forwards=60, restoration_forwards=60,
        new_training_steps=0, checkpoint_bundle_loads=1, model_state_loads=10, new_checkpoint_writes=0,
        source_pins=388, protected_inputs=635, direct_dependencies=33,
        own_tests=24, modules=142, loaded_tests=3338, focused_tests=3337, excluded_test=EXCLUDED,
        dtype="CPU float64", threads=2, deterministic=True, replay_tolerance=TOL,
        network_calls=0, gate_f_candidate=False, production_adoption=False, general_language_claim=False)


def render(row, view):
    require(view in VIEWS and tuple(row["permutation"]) in KNOWN + NOVEL, "view/permutation")
    names = ENTITIES[row["language"]]
    facts = ";".join(names[i] + "=" + ("?" if view == "evidence_blind" else str(row["assignment"][i]))
                     for i in row["permutation"])
    return facts + ";" + ("?" if view == "query_blind" else names[row["query"]]) + "="


def novel_dataset(parts):
    require(digest(parts) == PARENT_ARTIFACTS["dataset.json"], "original dataset identity")
    result = {s: [] for s in SPLITS}
    for split in SPLITS:
        require(len(parts[split]) == 144, "original row count")
        for old in parts[split]:
            if old["order"] != 0:
                continue
            for permutation in NOVEL:
                row = dict(source_id=old["id"], id=old["id"] + ":" + "".join(map(str, permutation)),
                    assignment=list(old["assignment"]), language=old["language"], query=old["query"],
                    target=old["target"], permutation=list(permutation))
                row["prompt"] = render(row, "normal")
                require(len(row["prompt"].encode()) <= 46, "prompt length")
                result[split].append(row)
        require(len(result[split]) == len({r["id"] for r in result[split]}) == 288, "new row count/IDs")
        require({tuple(r["assignment"]) for r in result[split]} == {tuple(r["assignment"]) for r in parts[split]}, "assignment scope")
    require(digest(result) == ORDER_SHA, "new dataset hash")
    return result


def check_logits(value, rows):
    require(isinstance(value, torch.Tensor) and value.shape == (rows, 256)
            and value.device.type == "cpu" and value.dtype == torch.float64
            and bool(torch.isfinite(value).all()), "finite CPU float64 logits")


def replay(left, right):
    check_logits(left, len(right)); check_logits(right, len(right))
    error = float((left - right).abs().max())
    require(error <= TOL and torch.equal(left.argmax(-1), right.argmax(-1)), "logit/argmax replay")
    return error


def new_metrics(rows, outputs):
    require(len(rows) == 288 and set(outputs) == set(VIEWS), "new metric coverage")
    for value in outputs.values():
        check_logits(value, 288)
    predictions = {v: t.argmax(-1).tolist() for v, t in outputs.items()}
    losses = F.cross_entropy(outputs["normal"], torch.tensor([r["target"] for r in rows]), reduction="none")
    cells = []
    for language in ("en", "ja"):
        for permutation in NOVEL:
            ids = [i for i, r in enumerate(rows) if r["language"] == language and tuple(r["permutation"]) == permutation]
            groups = defaultdict(list)
            for i in ids:
                groups[tuple(rows[i]["assignment"])].append(i)
            require(len(ids) == 36 and len(groups) == 12 and all(
                len(g) == 3 and {rows[i]["query"] for i in g} == {0, 1, 2} for g in groups.values()), "query triples")
            acc = {v: sum(predictions[v][i] == rows[i]["target"] for i in ids) / 36 for v in VIEWS}
            cells.append(dict(language=language, permutation=list(permutation), rows=36,
                correct=sum(predictions["normal"][i] == rows[i]["target"] for i in ids), accuracy=acc["normal"],
                query_triplet_accuracy=sum(all(predictions["normal"][i] == rows[i]["target"] for i in g) for g in groups.values()) / 12,
                evidence_blind_accuracy=acc["evidence_blind"], query_blind_accuracy=acc["query_blind"],
                evidence_drop=acc["normal"] - acc["evidence_blind"], query_drop=acc["normal"] - acc["query_blind"],
                answer_nll=float(losses[ids].mean())))
    return cells, predictions


def new_cell_pass(cell):
    return (cell["accuracy"] >= .90 and cell["query_triplet_accuracy"] >= .80
            and cell["evidence_drop"] >= .35 and cell["query_drop"] >= .35)


def six_order_metrics(old_rows, new_rows, old_pred, new_pred):
    require(len(old_rows) == len(old_pred) == 144 and len(new_rows) == len(new_pred) == 288, "six-order rows")
    groups = defaultdict(list)
    for old, rows, predictions in ((True, old_rows, old_pred), (False, new_rows, new_pred)):
        for row, prediction in zip(rows, predictions, strict=True):
            permutation = KNOWN[row["order"]] if old else tuple(row["permutation"])
            key = (row["language"], tuple(row["assignment"]), row["query"])
            groups[key].append((permutation, prediction == row["target"]))
    require(len(groups) == 72 and all(len(g) == 6 and {p for p, _ in g} == set(KNOWN + NOVEL) for g in groups.values()), "six-order groups")
    return {lang: dict(groups=36, all_six_correct=sum(all(ok for _, ok in g) for key, g in groups.items() if key[0] == lang),
                       accuracy=sum(all(ok for _, ok in g) for key, g in groups.items() if key[0] == lang) / 36)
            for lang in ("en", "ja")}


def evaluate_new(model, new_parts, factory):
    outputs = {}
    with torch.no_grad():
        for split in SPLITS:
            outputs[split] = {}
            for view in VIEWS:
                tokens = torch.stack([factory.prefix_tensor(render(row, view).encode()) for row in new_parts[split]])
                value = model(tokens, torch.zeros(len(tokens), dtype=torch.int64))
                check_logits(value, 288); outputs[split][view] = value.detach().clone()
    return outputs


def frozen_model(ref, state, parent, c252, reader, factory):
    model = parent.make_model(factory.new_model(ref["seed"]), ref["arm"], ref["seed"], c252, reader)
    model.load_state_dict(state, strict=True); model.eval().requires_grad_(False)
    require(sum(p.numel() for p in model.parameters()) == 14256 and parent.fingerprint(model) == ref["final_sha256"], "frozen final model")
    return model


def probe_one(model, parts, new_parts, ref, parent, factory):
    require(not any(m.training for m in model.modules()) and not any(p.requires_grad for p in model.parameters()), "frozen evaluation")
    before = parent.fingerprint(model); require(before == ref["final_sha256"], "initial final-state identity")
    counts = [0, 0]
    def counted(module, args, output):
        counts[0] += 1; counts[1] += len(args[0])
    handle = model.register_forward_hook(counted)
    try:
        old_metrics, old_pred, anchor = parent.evaluate(model, parts, factory)
        anchor_error = parent.metric_error(old_metrics, ref["final"])
        require(anchor_error <= TOL and old_pred == ref["predictions"], "original C256 metric/prediction replay")
        require(parent.fingerprint(model) == before, "anchor state mutation")
        novel = evaluate_new(model, new_parts, factory)
        _, _, restored = parent.evaluate(model, parts, factory)
        restore_error = max(replay(restored[s][v], anchor[s][v]) for s in SPLITS for v in VIEWS)
    finally:
        handle.remove()
    require(counts == [18, 3456] and parent.fingerprint(model) == before, "workload/state preservation")
    return dict(seed=ref["seed"], arm=ref["arm"], final_sha256=before, forward_calls=18,
        row_presentations=3456, weights_preserved=True, anchor_error=anchor_error, restore_error=restore_error,
        outputs=dict(anchor=anchor, novel=novel, restored=restored))


def analyze(parts, new_parts, records, refs, parent):
    require(new_parts == novel_dataset(parts), "saved new dataset identity")
    require([(r["seed"], r["arm"]) for r in records] == [(r["seed"], r["arm"]) for r in refs] == identities(), "complete model identities")
    measurements = []; outcomes = {a: Counter() for a in ARMS}; seed_results = []
    for record, ref in zip(records, refs, strict=True):
        require(record["final_sha256"] == ref["final_sha256"] and record["weights_preserved"] is True
                and (record["forward_calls"], record["row_presentations"]) == (18, 3456), "record integrity")
        for key in ("anchor_error", "restore_error"):
            require(type(record[key]) in (int, float) and math.isfinite(record[key]) and 0 <= record[key] <= TOL, "record replay error")
        outputs = record["outputs"]; require(set(outputs) == {"anchor", "novel", "restored"}, "output stages")
        for stage in outputs:
            require(set(outputs[stage]) == set(SPLITS) and all(set(outputs[stage][s]) == set(VIEWS) for s in SPLITS), "split/view coverage")
        old_metrics = {}; old_predictions = {}; fresh_metrics = {}; consistency = {}
        for split in SPLITS:
            for view in VIEWS:
                check_logits(outputs["anchor"][split][view], 144)
                replay(outputs["restored"][split][view], outputs["anchor"][split][view])
            old_metrics[split], old_predictions[split] = parent.metrics(parts[split], outputs["anchor"][split])
            fresh_metrics[split], pred = new_metrics(new_parts[split], outputs["novel"][split])
            consistency[split] = six_order_metrics(parts[split], new_parts[split], old_predictions[split]["normal"], pred["normal"])
        require(parent.metric_error(old_metrics, ref["final"]) <= TOL and old_predictions == ref["predictions"], "saved original replay")
        old_pass = all(parent.cell_pass(m) for split in old_metrics.values() for m in split.values())
        new_pass = all(new_cell_pass(c) for cells in fresh_metrics.values() for c in cells)
        order_pass = all(c["accuracy"] >= .80 for split in consistency.values() for c in split.values())
        passed = old_pass and new_pass and order_pass
        outcome = "ORIGINAL_CRITERIA_MISS" if not old_pass else "NEW_ORDER_MISS" if not new_pass else "SIX_ORDER_MISS" if not order_pass else "PASS"
        outcomes[record["arm"]][outcome] += 1
        seed_results.append(dict(seed=record["seed"], arm=record["arm"], passed=passed, outcome=outcome))
        measurements.append(dict(seed=record["seed"], arm=record["arm"], original=old_metrics,
            new_orders=fresh_metrics, six_order=consistency, passed=passed, outcome=outcome))
    summary = dict(models=10, seed_results=seed_results, outcomes={a: dict(v) for a, v in outcomes.items()},
        seed_pass_counts={a: sum(r["passed"] for r in seed_results if r["arm"] == a) for a in ARMS},
        candidate_gate=all(r["passed"] for r in seed_results if r["arm"] == ARMS[0]),
        model_forward_calls=sum(r["forward_calls"] for r in records), row_presentations=sum(r["row_presentations"] for r in records),
        new_training_steps=0, new_checkpoint_writes=0, checkpoint_bundle_loads=1, model_state_loads=10,
        all_replays=True, all_weights_preserved=True)
    return measurements, summary


def load_inputs(summary_path):
    parent, _, _, _, audit = context(); path = Path(summary_path).resolve()
    require(audit.sha(path) == PARENT_SHA, "parent summary hash")
    payload, refs = parent.verify_artifacts(path.parent, PARENT_EXECUTION)
    require(payload["status"] == "PASS" and payload["validation_summary"]["seed_pass_counts"] == {ARMS[0]: 5, ARMS[1]: 0}, "accepted parent verdict")
    parts = audit.read_json(path.parent / "dataset.json")
    require(parts == parent.dataset(), "parent generator identity")
    return parts, refs


def validate_registration(source_count, input_count):
    actual = digest(manifest())
    print(f"registration_check = source_pins:{source_count}; protected_inputs:{input_count}; manifest_sha256:{actual}", flush=True)
    require((source_count, input_count) == (388, 635), f"source/input counts: expected=(388, 635) actual=({source_count}, {input_count})")
    require(actual == MANIFEST_SHA, f"manifest hash: expected={MANIFEST_SHA} actual={actual}")


def precheck(summary_path, root):
    parent, _, _, factory, audit = context(); path = Path(summary_path).resolve(); root = Path(root)
    require(audit.sha(path) == PARENT_SHA, "parent hash"); payload = audit.read_json(path); parent.validate_result(payload)
    require(payload["commit_sha"] == PARENT_EXECUTION and payload["status"] == "PASS", "parent execution")
    pins, protected = dict(payload["source_blobs"]), dict(payload["input_sha256"])
    for name, wanted in protected.items():
        require(Path(name).is_file() and audit.sha(name) == wanted, "changed input:" + name)
    for name, wanted in pins.items():
        require(audit.git(root, "rev-parse", "HEAD:" + name).decode().strip() == wanted, "changed source:" + name)
    require(str(path) not in protected, "parent double count"); protected[str(path)] = PARENT_SHA
    require({x["file"]: x["sha256"] for x in payload["artifacts"]} == PARENT_ARTIFACTS, "parent artifact identities")
    for item in payload["artifacts"]:
        child = audit.safe_child(path.parent, item["file"])
        require(audit.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "parent artifact bytes")
        require(str(child.resolve()) not in protected, "artifact double count"); protected[str(child.resolve())] = item["sha256"]
    for name in OWN:
        require(name not in pins, "OWN collision"); pins[name] = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-6])_[^/]+)\.py"
    dependencies = set(factory.LM_SOURCES) | {name for name in payload["source_blobs"] if re.fullmatch(pattern, name)} | {OWN[0]}
    require(len(dependencies) == 33 and dependencies <= set(pins), "direct dependency coverage")
    protected.update(audit.protect_tree_files(root, pins))
    validate_registration(len(pins), len(protected))
    return pins, protected


def validate_result(payload):
    require(payload["experiment_id"] == EXPERIMENT_ID and payload["stage"] == STAGE and payload["diagnostic_execution_valid"] is True, "result identity")
    require((len(payload["source_blobs"]), len(payload["input_sha256"])) == (388, 635) and set(OWN) <= set(payload["source_blobs"]), "protection")
    require(len(payload["artifacts"]) == 5 and {x["file"] for x in payload["artifacts"]} == OUTPUTS, "artifact coverage")
    summary = payload["validation_summary"]
    for key, value in dict(models=10, model_forward_calls=180, row_presentations=34560, new_training_steps=0,
                           new_checkpoint_writes=0, checkpoint_bundle_loads=1, model_state_loads=10).items():
        require(type(summary[key]) is int and summary[key] == value, "workload:" + key)
    require([(r["seed"], r["arm"]) for r in summary["seed_results"]] == identities(), "summary seed identities")
    require(type(summary["candidate_gate"]) is bool and payload["status"] == ("PASS" if summary["candidate_gate"] else "FAIL"), "status")
    require(summary["all_replays"] is True and summary["all_weights_preserved"] is True, "replay flags")
    require(payload["gate_f_candidate"] is False and payload["production_adoption"] is False and payload["network_calls"] == 0, "scope")


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == 141, "parent modules")
    return names + ["tests_lm.test_v05_c257_unseen_fact_order"]


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]; require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1, "suite IDs")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require((len(tests), len(kept)) == (3338, 3337), "suite counts")
    return unittest.TestSuite(kept)


def run(*, c256_summary, output_dir, expected_head):
    parent, c252, reader, factory, audit = context(); root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root, "rev-parse", "HEAD").decode().strip() == expected_head, "HEAD")
        require(audit.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss", "branch")
        require(not audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "dirty tracked tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins, protected = precheck(c256_summary, root); parts, refs = load_inputs(c256_summary); new_parts = novel_dataset(parts)
    states = parent.load_bundle(Path(c256_summary).resolve().parent / "trained-models.pt")
    require(len(states) == len(refs) == 10, "ten final models")
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False); records = []
    for ref, state in zip(refs, states, strict=True):
        print(f'[C257] model={len(records)+1}/10 seed={ref["seed"]} arm={ref["arm"]}; frozen unseen-order evaluation', flush=True)
        model = frozen_model(ref, state, parent, c252, reader, factory)
        records.append(probe_one(model, parts, new_parts, ref, parent, factory))
    measurements, summary = analyze(parts, new_parts, records, refs, parent)
    torch.save(dict(schema="fold-c257-order-eval-v1", records=records), out / "eval-outputs.pt")
    for name, value in (("order-plan.json", manifest()), ("order-dataset.json", new_parts),
                        ("measurements.json", measurements), ("validation-summary.json", summary)):
        (out / name).write_bytes(blob(value))
    artifacts = [dict(file=name, sha256=audit.sha(out/name), serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard(); precheck(c256_summary, root)
    for name, wanted in protected.items():
        require(audit.sha(name) == wanted, "modified input")
    payload = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head,
        status="PASS" if summary["candidate_gate"] else "FAIL", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256=protected, artifacts=artifacts, validation_summary=summary,
        gate_f_candidate=False, production_adoption=False, network_calls=0)
    validate_result(payload); (out / "summary.json").write_bytes(blob(payload))
    print("=== C257 RESULT ===", flush=True); print(blob(payload).decode(), flush=True)
    return payload


def verify_artifacts(output_dir, c256_summary, expected_head):
    parent, _, _, _, audit = context(); out = Path(output_dir); payload = audit.read_json(out / "summary.json")
    validate_result(payload); require(payload["commit_sha"] == expected_head, "saved HEAD")
    for name, wanted in payload["input_sha256"].items():
        require(audit.sha(name) == wanted, "postcheck input")
    for item in payload["artifacts"]:
        child = audit.safe_child(out, item["file"])
        require(audit.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "output bytes")
    parts, refs = load_inputs(c256_summary); new_parts = audit.read_json(out / "order-dataset.json")
    archive = torch.load(out / "eval-outputs.pt", map_location="cpu", weights_only=True)
    require(set(archive) == {"schema", "records"} and archive["schema"] == "fold-c257-order-eval-v1", "archive schema")
    measurements, summary = analyze(parts, new_parts, archive["records"], refs, parent)
    for name, value in (("order-plan.json", manifest()), ("measurements.json", measurements), ("validation-summary.json", summary)):
        require(audit.read_json(out / name) == value, "persisted replay:" + name)
    require(payload["validation_summary"] == summary, "saved summary replay")
    return payload, measurements


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("c256-summary", "output-dir"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
