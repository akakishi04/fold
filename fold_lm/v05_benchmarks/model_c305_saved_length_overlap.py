"""C305: align saved answers across identifier lengths; no new model execution."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
import hashlib
import itertools
import json
from pathlib import Path
import re
from types import ModuleType
import unittest
from unittest.mock import patch
import torch

EXPERIMENT_ID = "C305-v5b-saved-length-error-overlap"
STAGE = "V5-B-SAVED-LENGTH-ERROR-OVERLAP"
BASE = "75b6545c1dc1d570286e76bb0b53473673247d33"
PARENT_EXECUTION = "f309fde3e2aa8df33156ce55c703c9c37c6e106b"
PARENT_SHA = "c4b0babc2f7b9ea544c96385ed386a721630ce81bfb26fcb5e1e028450670717"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c304_length_breadth.py"
PARENT_BLOB = "cacb5852a29171aa8079e634d929fdd54e7f4f58"
SEEDS = tuple(range(304001, 304006))
ARMS = ("four_only", "three_four", "two_three_four")
LENGTHS = (2, 3, 4, 5)
PROFILES = ("repeat", "shared_prefix", "shared_suffix")
SCORE_PROFILES = ("tripled", "shared_prefix2", "shared_suffix2")
SPLITS = ("TRAIN", "HOLDOUT")
OWN = ("fold_lm/v05_benchmarks/model_c305_saved_length_overlap.py",
       "tests_lm/test_v05_c305_saved_length_overlap.py", "tools/run_c305.ps1", "tools/invoke_c305.ps1",
       "docs/experiment-ledger-addendum-c305-preregistration.md", "docs/v5b-saved-length-overlap-v0.1.md")
OUTPUTS = ("audit-plan.json", "aligned-answers.json", "validation-summary.json")
ZERO_KEYS = ("train_steps", "model_forward_calls", "row_presentations", "core_forward_calls",
             "model_state_loads", "new_checkpoint_writes", "network_calls")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "844119479e6a43fc9fa5d3510ce05d8300ed2108dd819c6058b24b3b449632bd"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS, ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c304_length_breadth as parent
    return parent, parent.context()[-1]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_source=PARENT_SOURCE,
        parent_blob=PARENT_BLOB, seeds=list(SEEDS), arms=list(ARMS), lengths=list(LENGTHS),
        question="which five-character errors persist from the same logical question at four, versus newly appear or disappear",
        primary_reference_length=4, descriptive_reference_lengths=[2, 3],
        alignment="same seed,arm,split,profile,source_id,query,target;all normal full256-class argmax outputs",
        invariants="exact parent verifier retains all original masked/full gates;no filtering,correction or model calls",
        logical_rows=12960, saved_predictions=51840, transition_groups=90, detail_groups=540,
        signature_groups=30, reconciled_totals=720, reconciled_partitions=120,
        ratios="null for zero denominator;conditional error rates descriptive,not a new capability gate",
        interpretation="known cohort,dependent paired observations;overlap does not identify a hidden causal mechanism",
        parents=31, source_pins=676, protected_inputs=1257, own_tests=32,
        modules=190, loaded_tests=4782, focused_tests=4781, excluded_test=EXCLUDED,
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False,
        **dict.fromkeys(ZERO_KEYS, 0))


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None and digest(manifest()) == MANIFEST_SHA, "manifest seal")


@contextmanager
def no_neural():
    with torch.no_grad(), patch.object(torch.nn.Module, "_call_impl", side_effect=RuntimeError("C305 forbids model calls")), \
         patch.object(torch.nn.Module, "load_state_dict", side_effect=RuntimeError("C305 forbids model-state loads")), \
         patch.object(torch, "save", side_effect=RuntimeError("C305 forbids tensor/checkpoint writes")):
        yield


def expected_flags():
    result = []
    for seed, arm in identities():
        good = ()
        if arm == ARMS[0]:
            good = (3, 4, 5) if seed in (304002, 304003) else (4, 5) if seed == 304005 else ()
        elif arm == ARMS[1]:
            good = LENGTHS if seed == 304003 else (3, 4, 5) if seed == 304005 else ()
        elif seed in (304003, 304005):
            good = LENGTHS
        result.append(dict(seed=seed, arm=arm, length_pass={str(n): n in good for n in LENGTHS}))
    return result


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def transition(rows, reference):
    require(reference in (2, 3, 4) and rows, "transition domain")
    counts = Counter()
    for row in rows:
        predictions, target = row["predictions"], row["target"]
        require(len(predictions) == 4 and type(target) is int and 0 <= target < 256
                and all(type(v) is int and 0 <= v < 256 for v in predictions), "prediction bytes")
        left, right = predictions[reference - 2], predictions[3]
        a, b = left == target, right == target
        counts["both_correct" if a and b else "reference_only" if a else "five_only" if b else "both_wrong"] += 1
        counts["argmax_flips"] += left != right
        if not a and not b:
            counts["both_wrong_same_answer" if left == right else "both_wrong_changed_answer"] += 1
    out = {k: counts[k] for k in ("both_correct", "reference_only", "five_only", "both_wrong",
                                  "argmax_flips", "both_wrong_same_answer", "both_wrong_changed_answer")}
    out.update(rows=len(rows), reference_correct=counts["both_correct"] + counts["reference_only"],
               five_correct=counts["both_correct"] + counts["five_only"])
    out["five_errors"] = counts["reference_only"] + counts["both_wrong"]
    out["persistent_fraction_of_five_errors"] = ratio(counts["both_wrong"], out["five_errors"])
    out["five_error_rate_given_reference_correct"] = ratio(counts["reference_only"], out["reference_correct"])
    require(out["five_correct"] - out["reference_correct"] == out["five_only"] - out["reference_only"], "transition conservation")
    return out


def collapse(rows, predictions):
    groups = defaultdict(list)
    for row, prediction in zip(rows, predictions, strict=True):
        key = (row["language"], tuple(row["entities"]), tuple(row["values"]), tuple(row["permutation"]))
        groups[key].append((row["query"], prediction))
    require(all(len(v) == 2 and {q for q, _ in v} == set(k[1]) for k, v in groups.items()), "complete query pairs")
    return sum(v[0][1] == v[1][1] for v in groups.values())


def analyze(records, data, prompts, metrics, partitions):
    require([(r["seed"], r["arm"]) for r in records] == identities()
            and [(r["seed"], r["arm"]) for r in metrics] == identities(), "complete ordered cohort")
    require(set(data) == set(SPLITS) and set(prompts) == set(map(str, LENGTHS)), "data domain")
    for split, n in (("TRAIN", 192), ("HOLDOUT", 96)):
        require(len(data[split]) == n and len({r["id"] for r in data[split]}) == n, "unique logical rows")
    pmap = {(p["seed"], p["arm"], p["identifier_length"], p["split"]): p for p in partitions}
    require(len(pmap) == len(partitions) == 120, "parent partition inventory")
    aligned, transitions, details, signatures = [], [], [], []
    reconciled = 0
    for record, metric in zip(records, metrics, strict=True):
        key = dict(seed=record["seed"], arm=record["arm"])
        require(set(record["raw"]) == set(metric["length_scores"]) == set(map(str, LENGTHS)), "length coverage")
        for split in SPLITS:
            rows, selected = data[split], []
            for profile, old_profile in zip(PROFILES, SCORE_PROFILES, strict=True):
                predictions = []
                for length in LENGTHS:
                    n = str(length)
                    require(set(record["raw"][n]) == set(SPLITS) and set(record["raw"][n][split]) == set(PROFILES), "raw split/profile")
                    items = prompts[n][split][profile]
                    require(len(items) == len(rows) and all((i["source_id"], i["target"]) == (r["id"], r["target"])
                            for r, i in zip(rows, items, strict=True)), "aligned prompt identity")
                    views = record["raw"][n][split][profile]
                    require(set(views) == {"normal", "evidence_blind", "query_blind"}, "view coverage")
                    z = views["normal"]
                    require(isinstance(z, torch.Tensor) and z.shape == (len(rows), 256) and z.dtype == torch.float64
                            and z.device.type == "cpu" and not z.requires_grad and bool(torch.isfinite(z).all()), "saved logits")
                    pred = z.argmax(1).tolist()
                    predictions.append(pred)
                    for language in ("en", "ja"):
                        ids = [i for i, r in enumerate(rows) if r["language"] == language]
                        totals = [t for t in metric["length_scores"][n]["totals"]
                                  if (t["split"], t["profile"], t["language"]) == (split, old_profile, language)]
                        require(len(totals) == 1 and totals[0]["rows"] == len(ids)
                                and totals[0]["correct"] == sum(pred[i] == rows[i]["target"] for i in ids)
                                and totals[0]["pairs"] == len(ids) // 2
                                and totals[0]["collapsed_pairs"] == collapse([rows[i] for i in ids], [pred[i] for i in ids]), "parent normal totals")
                        reconciled += 1
                for i, row in enumerate(rows):
                    pred = [p[i] for p in predictions]
                    signature = "".join("1" if v == row["target"] else "0" for v in pred)
                    selected.append(dict(**key, split=split, profile=profile, source_id=row["id"],
                        target=row["target"], language=row["language"], query=row["query"],
                        predictions=pred, correctness_signature=signature))
            for length in LENGTHS:
                p = pmap[(record["seed"], record["arm"], length, split)]
                require(p["rows"] == len(selected) and p["correct"] == sum(r["predictions"][length - 2] == r["target"] for r in selected), "parent partition totals")
            bins = Counter(r["correctness_signature"] for r in selected)
            signatures.append(dict(**key, split=split, rows=len(selected), counts={f"{i:04b}": bins[f"{i:04b}"] for i in range(16)}))
            for reference in (2, 3, 4):
                transitions.append(dict(**key, split=split, reference_length=reference, **transition(selected, reference)))
                for profile, language in itertools.product(PROFILES, ("en", "ja")):
                    group = [r for r in selected if (r["profile"], r["language"]) == (profile, language)]
                    details.append(dict(**key, split=split, reference_length=reference, profile=profile, language=language, **transition(group, reference)))
            aligned.extend(selected)
    require((len(aligned), len(transitions), len(details), len(signatures), reconciled) == (12960, 90, 540, 30, 720), "audit inventory")
    summary = dict(parent_flags=expected_flags(), logical_rows=len(aligned), saved_predictions=4 * len(aligned),
        transition_groups=transitions, detail_groups=details, signature_groups=signatures, reconciled_totals=reconciled,
        reconciled_partitions=len(pmap), diagnostic_complete=True, capability_gate_applicable=False, **dict.fromkeys(ZERO_KEYS, 0))
    return aligned, summary


def load_parent(paths):
    parent, c = context()
    paths = [Path(p).resolve() for p in paths]
    hashes = (PARENT_SHA, *parent.parent_hashes(parent.context()[0]))
    require(len(paths) == len(hashes) == 31 and all(c.audit.sha(p) == h for p, h in zip(paths, hashes, strict=True)), "parent hashes")
    with no_neural():
        payload, metrics = parent.verify_artifacts(paths[0].parent, paths[1:], PARENT_EXECUTION)
        parent.validate_result(payload)
        require(payload["experiment_id"] == "C304-v5b-length-breadth-to-five" and payload["commit_sha"] == PARENT_EXECUTION
                and payload["status"] == "FAIL" and payload["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "parent identity")
        s = payload["validation_summary"]
        flags = [{k: r[k] for k in ("seed", "arm", "length_pass")} for r in s["seed_results"]]
        require(flags == expected_flags() and s["candidate_gate"] is False and s["all_groups_matched"] is True and s["all_replays"] is True, "parent flags")
        require(len(payload["artifacts"]) == 7 and {a["file"] for a in payload["artifacts"]} == set(parent.OUTPUTS), "parent artifacts")
        data = c.audit.read_json(paths[0].parent / "dataset.json")
        prompts = c.audit.read_json(paths[0].parent / "length-datasets.json")
        archive = torch.load(paths[0].parent / "evaluations.pt", map_location="cpu", weights_only=True)
        require(set(archive) == {"schema", "records"} and archive["schema"] == "fold-c304-length-eval-v1", "parent archive")
    return payload, archive["records"], data, prompts, metrics, s["final_partitions"]


def precheck(paths, root):
    validate_seal()
    payload, *_ = load_parent(paths)
    parent, c = context()
    root = Path(root).resolve()
    pins, protected = dict(payload["source_blobs"]), dict(payload["input_sha256"])
    require((len(pins), len(protected)) == (670, 1243), "inherited protection")
    for n, h in pins.items():
        require(c.audit.git(root, "rev-parse", "HEAD:" + n).decode().strip() == h, "changed source:" + n)
    for n, h in protected.items():
        require(Path(n).is_file() and c.audit.sha(n) == h, "changed input:" + n)
    for module in [parent, *parent.context(), *vars(c).values()]:
        path = getattr(module, "__file__", None) if isinstance(module, ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            require(Path(path).resolve().relative_to(root).as_posix() in pins, "unprotected direct helper")
    require(pins.get(PARENT_SOURCE) == PARENT_BLOB, "parent source pin")
    directory = Path(paths[0]).resolve().parent
    for path, h in [(directory / "summary.json", PARENT_SHA)] + [(c.audit.safe_child(directory, a["file"]), a["sha256"]) for a in payload["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path) == h, "parent input")
        protected[str(path.resolve())] = h
    for n in OWN:
        require(n not in pins, "OWN collision")
        pins[n] = c.audit.git(root, "rev-parse", "HEAD:" + n).decode().strip()
    protected.update(c.audit.protect_tree_files(root, pins))
    require((len(pins), len(protected)) == (676, 1257), "protection cardinality")
    print(f"registration_check = source_pins:676; protected_inputs:1257; manifest_sha256:{MANIFEST_SHA}", flush=True)
    return pins, protected


def reconstruct(paths):
    with no_neural():
        _, records, data, prompts, metrics, partitions = load_parent(paths)
        return analyze(records, data, prompts, metrics, partitions)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["status"] == "PASS" and p["diagnostic_execution_valid"] is True, "result identity")
    require(all(p[k] is False for k in ("capability_gate_applicable", "gate_f_candidate", "production_adoption")), "result scope")
    require((len(p["source_blobs"]), len(p["input_sha256"])) == (676, 1257) and set(OWN) <= set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "result protection")
    require(len(p["artifacts"]) == 3 and {a["file"] for a in p["artifacts"]} == set(OUTPUTS), "result artifacts")
    s = p["validation_summary"]
    require(s["parent_flags"] == expected_flags() and s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False, "diagnostic boundary")
    require((s["logical_rows"], s["saved_predictions"], s["reconciled_totals"], s["reconciled_partitions"]) == (12960, 51840, 720, 120), "result counts")
    require(tuple(len(s[k]) for k in ("transition_groups", "detail_groups", "signature_groups")) == (90, 540, 30), "result groups")
    require(all(type(s[k]) is int and s[k] == 0 for k in ZERO_KEYS), "zero neural workload")


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from flatten(test)
        else:
            yield test


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == 189, "parent modules")
    return names + ["tests_lm.test_v05_c305_saved_length_overlap"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) == 4782 and ids.count(EXCLUDED) == 1, "loaded suite")
    return unittest.TestSuite(t for t in tests if t.id() != EXCLUDED)


def guard(root, head, c):
    require(c.audit.git(root, "rev-parse", "HEAD").decode().strip() == head
            and c.audit.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss"
            and not c.audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "repository guard")


def run(*, summaries, output_dir, expected_head):
    _, c = context()
    root = Path(__file__).resolve().parents[2]
    guard(root, expected_head, c)
    pins, protected = precheck(summaries, root)
    aligned, summary = reconstruct(summaries)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    for n, value in zip(OUTPUTS, (manifest(), aligned, summary), strict=True):
        (out / n).write_bytes(blob(value))
    artifacts = [dict(file=n, sha256=c.audit.sha(out / n), serialized_bytes=(out / n).stat().st_size) for n in OUTPUTS]
    guard(root, expected_head, c)
    precheck(summaries, root)
    p = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head, status="PASS", diagnostic_execution_valid=True,
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False,
        source_blobs=pins, input_sha256=protected, artifacts=artifacts, validation_summary=summary)
    validate_result(p)
    (out / "summary.json").write_bytes(blob(p))
    receipt = dict(experiment_id=EXPERIMENT_ID, status="PASS", commit_sha=expected_head, artifacts=artifacts, summary_sha256=c.audit.sha(out / "summary.json"))
    print("=== C305 COMPACT DIAGNOSTIC RECEIPT ===", flush=True)
    print(json.dumps(receipt, indent=2, sort_keys=True), flush=True)
    return p


def verify_artifacts(outdir, summaries, expected_head):
    _, c = context()
    out = Path(outdir)
    p = c.audit.read_json(out / "summary.json")
    validate_result(p)
    require(p["commit_sha"] == expected_head, "execution HEAD")
    for n, h in p["input_sha256"].items():
        require(c.audit.sha(n) == h, "protected input")
    for a in p["artifacts"]:
        path = c.audit.safe_child(out, a["file"])
        require(c.audit.sha(path) == a["sha256"] and path.stat().st_size == a["serialized_bytes"], "output bytes")
    aligned, summary = reconstruct(summaries)
    for n, value in zip(OUTPUTS, (manifest(), aligned, summary), strict=True):
        require(c.audit.read_json(out / n) == value, "persisted:" + n)
    require(p["validation_summary"] == summary, "summary reconstruction")
    return p


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summaries", nargs=31, type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
