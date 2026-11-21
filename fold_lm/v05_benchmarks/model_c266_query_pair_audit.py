"""C266: one saved-output query-pair diagnostic, not a capability experiment."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import torch

EXPERIMENT_ID = "C266-v5b-saved-query-pair-audit"
STAGE = "V5-B-SAVED-QUERY-PAIR-AUDIT"
BASE = "92da414cec60028f813b8196f61b5a432f7c6b90"
PARENT_EXECUTION = "e0809d90c552471dee8723ce1b10528488f23be0"
PARENT_SHA = "f8c00bbcb311eeaf686ee43ef36d0597180e57c2bd70598d0fc23357c4da7998"
C264_SHA = "1c7e3d517bcf764f2b4eb89e432cb8ce303861359957f1fbfd77de9f19eb1503"
C263_SHA = "1fcceab38de3e34a3858828285fd43503df9e455e2fdb3bd31524b5035813e21"
ROW_SHA = "8adacd9b13b87c9f6a2bd7e1bf0f735e9a1a63b521840ef301a855586643e6c1"
PARENT_ARTIFACTS = {
    "eval-outputs.pt": "546f5eb5dd62aa205c046fc5f2c7065837dc9ce578c79725c72ac451f87ae782",
    "identifier-dataset.json": "4bcc707da1814d765c4218f73203e175d092bea096becc593b789fbbcdb729bb",
    "identifier-plan.json": "1a6316f251e15e29e67d22eb2d6be02407a6fa4ea6a610759b332f5bd9de53a3",
    "measurements.json": "208943819e92e4f5cdd4f299668c86b14cba338180e1686ddd40d776b8315656",
    "validation-summary.json": "fd2e2028c442b651b740b7e0e82ea9e326750c0052b22a9d7b072486a2988bbd",
}
SEEDS = tuple(range(263001, 263006))
ARMS = ("standard_forward", "standard_reverse", "lower_forward", "lower_reverse")
PROFILES = ("doubled", "shared_prefix", "shared_suffix")
VIEWS = ("normal", "evidence_blind", "query_blind")
CATEGORIES = ("both_correct", "swapped", "collapse_entity0", "collapse_entity1", "collapse_outside", "other_different")
ANSWER_CLASSES = ("correct", "other_entity", "absent_digit", "other_byte")
OWN = ("fold_lm/v05_benchmarks/model_c266_query_pair_audit.py",
       "tests_lm/test_v05_c266_query_pair_audit.py", "tools/run_c266.ps1", "tools/invoke_c266.ps1",
       "docs/experiment-ledger-addendum-c266-preregistration.md", "docs/v5b-query-pair-audit-v0.1.md")
OUTPUTS = ("audit-plan.json", "pair-attribution.json", "cells.json", "profile-summary.json", "matched-contrasts.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "85be4d973b9f8ce8a59e1ffa9028faceb1de3fcc8d8b3035264c2af72ed88b3e"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS, ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c265_compound_identifiers as parent
    parts = parent.context()
    return parent, parts[0], parts[-1]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, c264_sha256=C264_SHA, c263_sha256=C263_SHA,
        parent_artifacts=PARENT_ARTIFACTS, row_sha256=ROW_SHA, seeds=list(SEEDS), arms=list(ARMS), profiles=list(PROFILES),
        question="When only the query name changes, do saved answers collapse, swap, or fail otherwise?",
        changed="offline grouping only; no input, state, inference or training intervention",
        categories=list(CATEGORIES), answer_classes=list(ANSWER_CLASSES), models=20,
        normal_answers=17280, query_pairs=8640, cells=720, profile_summaries=120, matched_contrasts=80,
        model_forward_calls=0, model_state_loads=0, checkpoint_bundle_loads=0, new_training_steps=0,
        new_checkpoint_writes=0, eval_archive_reads_per_pass=6, analysis_passes=2,
        source_pins=442, protected_inputs=748, direct_dependencies=42, own_tests=24,
        modules=151, loaded_tests=3550, focused_tests=3549, excluded_test=EXCLUDED,
        diagnostic_only=True, capability_pass_claim=False, causal_parser_claim=False,
        gate_f_candidate=False, production_adoption=False, network_calls=0)


def tensor_check(x):
    require(isinstance(x, torch.Tensor) and x.shape == (288, 256) and x.dtype == torch.float64
            and x.device.type == "cpu" and bool(torch.isfinite(x).all()), "finite saved CPU float64 logits")


def pair_class(predicted, targets):
    a, b = predicted; x, y = targets
    require(x != y and all(type(v) is int and 0 <= v < 256 for v in (a, b, x, y)), "pair values")
    if (a, b) == (x, y): return "both_correct"
    if (a, b) == (y, x): return "swapped"
    if a == b: return "collapse_entity0" if a == x else "collapse_entity1" if a == y else "collapse_outside"
    return "other_different"


def answer_class(prediction, target, other):
    return "correct" if prediction == target else "other_entity" if prediction == other else "absent_digit" if 48 <= prediction <= 51 else "other_byte"


def query_groups(rows):
    require(digest(rows) == ROW_SHA and len(rows) == 288, "source-row identity")
    groups = defaultdict(list)
    for i, row in enumerate(rows):
        groups[(row["language"], tuple(row["entities"]), tuple(row["values"]), tuple(row["permutation"]))].append(i)
    require(len(groups) == 144, "query group count")
    result = []
    for key, ids in sorted(groups.items()):
        ids.sort(key=lambda i: rows[i]["query"])
        require(len(ids) == 2 and [rows[i]["query"] for i in ids] == list(key[1]), "both distinct queries")
        require([rows[i]["target"] for i in ids] == [48 + v for v in key[2]], "query targets")
        result.append((key, ids))
    return result


def aggregate(pairs, keys):
    groups = defaultdict(list)
    for p in pairs:
        groups[tuple(tuple(p[k]) if isinstance(p[k], list) else p[k] for k in keys)].append(p)
    output = []
    for key, values in sorted(groups.items()):
        counts = {c: sum(p["category"] == c for p in values) for c in CATEGORIES}
        answers = {c: sum(p["answer_classes"].count(c) for p in values) for c in ANSWER_CLASSES}
        collapsed = sum(counts[c] for c in CATEGORIES if c.startswith("collapse_"))
        n = len(values)
        require(sum(counts.values()) == n and sum(answers.values()) == 2*n, "integer partition")
        output.append(dict(zip(keys, [list(v) if isinstance(v, tuple) else v for v in key], strict=True)) | dict(
            pairs=n, answers=2*n, categories=counts, answer_classes=answers, collapsed_pairs=collapsed,
            collapse_rate=collapsed/n, paired_accuracy=counts["both_correct"]/n,
            correct_answers=answers["correct"], same_logit_pairs=sum(p["same_logits"] for p in values),
            selected_first_fact=sum(p["selected_position"] == 0 for p in values),
            selected_last_fact=sum(p["selected_position"] == 1 for p in values)))
    return output


def analyze(records, rows, parent_metrics):
    require([(r["seed"], r["arm"]) for r in records] == identities(), "all source states")
    require([(r["seed"], r["arm"]) for r in parent_metrics] == identities(), "parent metrics identities")
    groups = query_groups(rows); pairs = []
    for r in records:
        require(r["weights_preserved"] is True and set(r["renamed"]) == set(PROFILES), "source record semantics")
        for profile in PROFILES:
            raw = r["renamed"][profile]
            require(set(raw) == set(VIEWS), "all saved views")
            for x in raw.values(): tensor_check(x)
            predictions = raw["normal"].argmax(-1).tolist()
            for (language, entities, values, permutation), ids in groups:
                pred = [predictions[i] for i in ids]; targets = [rows[i]["target"] for i in ids]
                category = pair_class(pred, targets)
                chosen = entities[0] if category == "collapse_entity0" else entities[1] if category == "collapse_entity1" else None
                gap = float((raw["normal"][ids[0]] - raw["normal"][ids[1]]).abs().max())
                require(math.isfinite(gap), "nonfinite query-logit difference")
                pairs.append(dict(seed=r["seed"], arm=r["arm"], profile=profile, language=language,
                    entities=list(entities), values=list(values), permutation=list(permutation),
                    row_ids=[rows[i]["id"] for i in ids], predictions=pred, targets=targets, category=category,
                    answer_classes=[answer_class(pred[i], targets[i], targets[1-i]) for i in (0, 1)],
                    selected_entity=chosen, selected_position=permutation.index(chosen) if chosen is not None else None,
                    query_logit_max_abs_difference=gap, same_logits=gap == 0.0))
    cells = aggregate(pairs, ("seed", "arm", "profile", "language", "entities", "permutation"))
    profiles = aggregate(pairs, ("seed", "arm", "profile", "language"))
    require(len(pairs) == 8640 and len(cells) == 720 and all(c["pairs"] == 12 for c in cells), "cell coverage")
    require(len(profiles) == 120 and all(c["pairs"] == 72 for c in profiles), "profile coverage")
    index = {(c["seed"], c["arm"], c["profile"], c["language"], tuple(c["entities"]), tuple(c["permutation"])): c for c in cells}
    for source in parent_metrics:
        for profile in PROFILES:
            old = source["profiles"][profile]
            subset = [c for c in cells if (c["seed"], c["arm"], c["profile"]) == (source["seed"], source["arm"], profile)]
            require(sum(c["correct_answers"] for c in subset) == old["correct"] and old["rows"] == 288, "parent total reconciliation")
            require(len(old["cells"]) == 12, "parent cell coverage")
            for cell in old["cells"]:
                c = index[source["seed"], source["arm"], profile, cell["language"], tuple(cell["entities"]), tuple(cell["permutation"])]
                require(c["correct_answers"] == cell["correct"] and c["paired_accuracy"] == cell["query_pair_accuracy"], "parent cell reconciliation")
    lookup = {(p["seed"], p["arm"], p["profile"], p["language"], tuple(p["entities"]), tuple(p["values"]), tuple(p["permutation"])): p for p in pairs}
    contrasts = []
    for seed, arm, language, profile in itertools.product(SEEDS, ARMS, ("en", "ja"), PROFILES[1:]):
        baseline = [p for p in pairs if (p["seed"], p["arm"], p["profile"], p["language"]) == (seed, arm, "doubled", language)]
        counts = dict(retained=0, collapsed=0, swapped=0, other=0); eligible = 0
        for p in baseline:
            q = lookup[seed, arm, profile, language, tuple(p["entities"]), tuple(p["values"]), tuple(p["permutation"])]
            if p["category"] != "both_correct": continue
            eligible += 1; category = q["category"]
            counts["retained" if category == "both_correct" else "collapsed" if category.startswith("collapse_") else "swapped" if category == "swapped" else "other"] += 1
        require(len(baseline) == 72 and sum(counts.values()) == eligible, "matched contrast accounting")
        contrasts.append(dict(seed=seed, arm=arm, language=language, profile=profile, all_pairs=72,
            baseline_both_correct=eligible, transitions=counts, collapse_fraction=counts["collapsed"]/eligible if eligible else None))
    require(len(contrasts) == 80, "contrast coverage")
    summary = dict(models=20, normal_answers=17280, query_pairs=len(pairs), cells=len(cells), profile_summaries=len(profiles),
        matched_contrasts=len(contrasts), profile_categories={p:{c:sum(x["category"] == c for x in pairs if x["profile"] == p) for c in CATEGORIES} for p in PROFILES},
        model_forward_calls=0, model_state_loads=0, checkpoint_bundle_loads=0, new_training_steps=0, new_checkpoint_writes=0,
        capability_pass_claim=False, causal_parser_claim=False, parent_scores_reconciled=True)
    return pairs, cells, profiles, contrasts, summary


@contextmanager
def saved_only():
    original = torch.load; loads = []
    def checked(path, *args, **kwargs):
        require(Path(path).name in ("eval-outputs.pt", "evaluations.pt"), "learned or unknown archive load forbidden")
        require(kwargs.get("weights_only") is True and kwargs.get("map_location") == "cpu", "safe archive load")
        loads.append(str(path)); return original(path, *args, **kwargs)
    with patch.object(torch, "load", side_effect=checked), patch.object(torch.nn.Module, "_call_impl", side_effect=RuntimeError("C266 forbids model calls")):
        yield loads


def check_parent(payload, parent):
    parent.validate_result(payload)
    require(payload["commit_sha"] == PARENT_EXECUTION and payload["status"] == "FAIL", "accepted C265 negative")
    s = payload["validation_summary"]
    require(s["seed_pass_counts"] == {a:0 for a in ARMS}, "parent joint misses")
    expected = dict(doubled=dict(zip(ARMS, (5,5,3,3))), shared_prefix=dict(zip(ARMS, (3,2,0,1))), shared_suffix={a:0 for a in ARMS})
    require(s["profile_pass_counts"] == expected, "accepted profile outcomes")
    require({x["file"]:x["sha256"] for x in payload["artifacts"]} == PARENT_ARTIFACTS, "parent artifact identities")


def load_reference(p265, p264, p263):
    parent, task, audit = context(); paths = [Path(p).resolve() for p in (p265, p264, p263)]
    require([audit.sha(p) for p in paths] == [PARENT_SHA, C264_SHA, C263_SHA], "parent summary identities")
    payload, metrics = parent.verify_artifacts(paths[0].parent, paths[1], paths[2], PARENT_EXECUTION)
    check_parent(payload, parent)
    archive = torch.load(paths[0].parent/"eval-outputs.pt", map_location="cpu", weights_only=True)
    require(set(archive) == {"schema", "records"} and archive["schema"] == "fold-c265-identifiers-eval-v1", "C265 saved logits schema")
    return archive["records"], task.dataset(), metrics


def compute(p265, p264, p263):
    with saved_only() as loads:
        records, rows, metrics = load_reference(p265, p264, p263)
        outputs = analyze(records, rows, metrics)
    require(Counter(Path(p).name for p in loads) == {"eval-outputs.pt":4, "evaluations.pt":2}, "reference archive workload")
    outputs[-1]["eval_archive_reads_per_pass"] = len(loads)
    return outputs


def precheck(p265, p264, p263, root):
    parent, _, audit = context(); path = Path(p265).resolve(); root = Path(root)
    require(audit.sha(path) == PARENT_SHA, "parent hash")
    payload = audit.read_json(path); check_parent(payload, parent)
    pins, protected = dict(payload["source_blobs"]), dict(payload["input_sha256"])
    for p, sha in ((p264, C264_SHA), (p263, C263_SHA)):
        require(protected.get(str(Path(p).resolve())) == sha, "inherited source protection")
    for name, wanted in protected.items(): require(Path(name).is_file() and audit.sha(name) == wanted, "changed input:"+name)
    for name, wanted in pins.items(): require(audit.git(root, "rev-parse", "HEAD:"+name).decode().strip() == wanted, "changed source:"+name)
    for child, wanted in [(path, PARENT_SHA)]+[(audit.safe_child(path.parent, x["file"]), x["sha256"]) for x in payload["artifacts"]]:
        key = str(child.resolve()); require(key not in protected and audit.sha(child) == wanted, "parent bytes/duplicate"); protected[key] = wanted
    for x in payload["artifacts"]: require(audit.safe_child(path.parent, x["file"]).stat().st_size == x["serialized_bytes"], "parent size")
    for name in OWN:
        require(name not in pins, "OWN collision"); pins[name] = audit.git(root, "rev-parse", "HEAD:"+name).decode().strip()
    factory = parent.context()[-2]
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-5])_[^/]+)\.py"
    deps = set(factory.LM_SOURCES)|{n for n in payload["source_blobs"] if re.fullmatch(pattern, n)}|{OWN[0]}
    require(len(deps) == 42 and deps <= set(pins), "direct scientific dependencies")
    protected.update(audit.protect_tree_files(root, pins))
    require((len(pins), len(protected)) == (442,748) and digest(manifest()) == MANIFEST_SHA, "registration counts/hash")
    print("registration_check = source_pins:442; protected_inputs:748; manifest_sha256:"+MANIFEST_SHA, flush=True)
    return pins, protected


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["status"] == "PASS" and p["diagnostic_execution_valid"] is True, "diagnostic identity")
    require((len(p["source_blobs"]), len(p["input_sha256"])) == (442,748) and set(OWN) <= set(p["source_blobs"]), "protection")
    require(len(p["artifacts"]) == 6 and {a["file"] for a in p["artifacts"]} == set(OUTPUTS), "artifact coverage")
    s = p["validation_summary"]
    for key, value in dict(models=20, normal_answers=17280, query_pairs=8640, cells=720, profile_summaries=120, matched_contrasts=80,
                           model_forward_calls=0, model_state_loads=0, checkpoint_bundle_loads=0, new_training_steps=0, new_checkpoint_writes=0, eval_archive_reads_per_pass=6).items():
        require(type(s[key]) is int and s[key] == value, "workload:"+key)
    require(set(s["profile_categories"]) == set(PROFILES), "profile coverage")
    for counts in s["profile_categories"].values():
        require(set(counts) == set(CATEGORIES) and all(type(v) is int and v >= 0 for v in counts.values()) and sum(counts.values()) == 2880, "partition counts")
    require(s["parent_scores_reconciled"] is True and s["capability_pass_claim"] is False and s["causal_parser_claim"] is False, "diagnostic nonclaims")
    require(all(p[k] is False for k in ("capability_pass_claim", "causal_parser_claim", "gate_f_candidate", "production_adoption")), "scope")


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite): yield from flatten(test)
        else: yield test


def regression_modules(root):
    modules = context()[0].regression_modules(root)
    require(len(modules) == len(set(modules)) == 150, "parent modules")
    return modules+["tests_lm.test_v05_c266_query_pair_audit"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]; require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1, "test IDs")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require((len(tests), len(kept)) == (3550,3549), "suite counts")
    return unittest.TestSuite(kept)


def run(*, c265_summary, c264_summary, c263_summary, output_dir, expected_head):
    audit = context()[-1]; root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root, "rev-parse", "HEAD").decode().strip() == expected_head, "HEAD")
        require(audit.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss", "branch")
        require(not audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "dirty tracked tree")
    guard(); torch.set_num_threads(2)
    parents = (c265_summary, c264_summary, c263_summary)
    pins, protected = precheck(*parents, root)
    print("[C266] saved-query attribution; model calls=0; training=0", flush=True)
    outputs = compute(*parents)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False)
    for name, value in zip(OUTPUTS, (manifest(), *outputs), strict=True): (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n, sha256=audit.sha(out/n), serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(); precheck(*parents, root)
    for name, wanted in protected.items(): require(audit.sha(name) == wanted, "modified input")
    p = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head, status="PASS", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256=protected, artifacts=artifacts, validation_summary=outputs[-1],
        capability_pass_claim=False, causal_parser_claim=False, gate_f_candidate=False, production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    print("=== C266 RESULT ===", flush=True); print(blob(p).decode(), flush=True)
    return p


def verify_artifacts(output_dir, c265_summary, c264_summary, c263_summary, expected_head):
    audit = context()[-1]; out = Path(output_dir); p = audit.read_json(out/"summary.json")
    validate_result(p); require(p["commit_sha"] == expected_head, "saved HEAD")
    for name, wanted in p["input_sha256"].items(): require(audit.sha(name) == wanted, "postcheck input")
    for x in p["artifacts"]:
        child = audit.safe_child(out, x["file"])
        require(audit.sha(child) == x["sha256"] and child.stat().st_size == x["serialized_bytes"], "output bytes")
    outputs = compute(c265_summary, c264_summary, c263_summary)
    for name, value in zip(OUTPUTS, (manifest(), *outputs), strict=True): require(audit.read_json(out/name) == value, "persisted reattribution:"+name)
    require(p["validation_summary"] == outputs[-1], "saved summary replay")
    return p, outputs[2], outputs[3]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("c265-summary", "c264-summary", "c263-summary", "output-dir"): p.add_argument("--"+name, type=Path, required=True)
    p.add_argument("--expected-head", required=True); run(**vars(p.parse_args()))


if __name__ == "__main__":
    main()
