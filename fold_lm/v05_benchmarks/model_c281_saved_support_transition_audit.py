"""C281: paired fixed-criterion transitions in saved C280 outputs; no neural execution."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
import unittest
from pathlib import Path
from unittest.mock import patch

import torch

EXPERIMENT_ID = "C281-v5b-saved-support-transition-audit"
STAGE = "V5-B-SAVED-SUPPORT-TRANSITION-AUDIT"
BASE = "3b06f8d34f2b4ce0bc7a234c3e29c2b5234df95d"
PARENT_EXECUTION = "2c2eb8a86a03910ba9c63ff277c137d1e842a32f"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c280_evidence_only_dual_memory.py"
PARENT_BLOB = "b0fbd492675ff8d147af13573b26c09c3d4afcab"
SUMMARY_SHAS = (
    "00410f3d879cb9571186e2ebf08a1ca9df0b31b64a639adae53f503c068bc7db",
    "a0019e06e4f4b330675daa2235cb4d0cf1952930336d2f0038f17d6ebd11b5bb",
    "557069bec9d0d6ef73c7a9d1f5196f7be70edb9ab2c37a9a0d315033678b770b",
    "ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13",
    "6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f",
    "1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb",
    "0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0",
)
PARENT_ARTIFACTS = {
    "architecture-plan.json": ("c02aa9b88d7eeb9a7671674b982b5d7dad420c88cae10b4e40b4c6130219e1ac", 3371),
    "dataset.json": ("1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1", 36024),
    "triple-dataset.json": ("432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73", 158236),
    "trained-models.pt": ("cf628e8505d371ce298778e697bbb72f8df48708b80306a2ab17c1f4d30c4d6f", 1238071),
    "evaluations.pt": ("7d3db012ef8288a336b9327a57876beb023f31d0c716e2650e08ed36ab2193de", 106277991),
    "measurements.json": ("a5d55cf9914f2a4168b7ffc12c56e4d291ceb8c94736f958a8a8f69893477ecc", 525082),
    "validation-summary.json": ("bf13ebb24d23c90b8b317b6df7294b5eaef5f3df5c854e10f77aacf57d263f19", 23004),
}
SEEDS = tuple(range(280001, 280006))
ARMS = ("all_token_dual", "evidence_only_dual")
PROFILES = {"two_char": ("doubled", "shared_prefix", "shared_suffix"),
            "triple": ("tripled", "shared_prefix2", "shared_suffix2")}
THRESHOLDS = {"accuracy": .90, "query_pair_accuracy": .80,
              "evidence_drop": .35, "query_drop": .35, "two_order_accuracy": .80}
OWN = ("fold_lm/v05_benchmarks/model_c281_saved_support_transition_audit.py",
       "tests_lm/test_v05_c281_saved_support_transition_audit.py",
       "tools/run_c281.ps1", "tools/invoke_c281.ps1",
       "docs/experiment-ledger-addendum-c281-preregistration.md",
       "docs/v5b-saved-support-transition-audit-v0.1.md")
OUTPUTS = ("audit-plan.json", "failure-profile.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
ZERO_KEYS = ("model_forward_calls", "row_presentations", "core_forward_calls", "train_steps",
             "model_state_loads", "new_checkpoint_writes", "network_calls")
MANIFEST_SHA = "ff14c1b8c6ed2a2c36f72b716732e8ae624d3ab9e2f96675a7f0763a17a10ea2"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def context():
    from fold_lm.v05_benchmarks import model_c280_evidence_only_dual_memory as parent
    return parent, *parent.context()[-2:]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION, summary_sha256=list(SUMMARY_SHAS),
                parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
                parent_artifacts={k: list(v) for k, v in PARENT_ARTIFACTS.items()},
                seeds=list(SEEDS), arms=list(ARMS), thresholds=THRESHOLDS,
                question="which C280 fixed-criterion failures evidence-only support rescues or introduces, especially shared_suffix2",
                primary="all five seeds; paired rescue/new-failure counts, not a capability winner",
                stratum="seed280004 versus other four is explanatory only; no seed exclusion",
                fixed_records=2160, paired_records=1080, source_pins=532, protected_inputs=940,
                direct_dependencies=57, own_tests=32, modules=166, loaded_tests=3918, focused_tests=3917,
                excluded_test=EXCLUDED, capability_gate_applicable=False, gate_f_candidate=False,
                production_adoption=False, **dict.fromkeys(ZERO_KEYS, 0))


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None, "manifest not sealed")
    require(digest(manifest()) == MANIFEST_SHA, "manifest digest mismatch")


def scalar(value, name):
    require(type(value) in (int, float) and math.isfinite(value), "finite scalar:" + name)
    return float(value)


def count(value, bound, name):
    require(type(value) is int and 0 <= value <= bound, "integer count:" + name)
    return value


def integer_ratio(value, denominator, name):
    value = scalar(value, name)
    numerator = round(value * denominator)
    require(0 <= numerator <= denominator and abs(value - numerator / denominator) <= 1e-12,
            "discrete ratio:" + name)
    return numerator


def key(record):
    return (record["kind"], record["task"], record["split"], record["profile"],
            record["language"], tuple(record["entities"]), tuple(record.get("permutation", [])))


def expected_keys(task):
    keys = set()
    for split, profile, language, entities in itertools.product(
            ("TRAIN", "HOLDOUT"), PROFILES[task], ("en", "ja"), ((0, 1), (0, 2), (1, 2))):
        for perm in (entities, entities[::-1]):
            keys.add(("answer_cell", task, split, profile, language, entities, perm))
        keys.add(("two_order", task, split, profile, language, entities, ()))
    return keys


def normalized(seed, arm, task, cell, kind):
    r = dict(cell, seed=seed, arm=arm, task=task, kind=kind)
    require(key(r) in expected_keys(task), "unknown fixed record")
    n = 16 if cell["split"] == "TRAIN" else 8
    accuracy = scalar(cell["accuracy"], "accuracy")
    if kind == "answer_cell":
        require(type(cell["rows"]) is int and cell["rows"] == n, "answer rows")
        require(type(cell["pairs"]) is int and cell["pairs"] == n // 2, "pair rows")
        correct = count(cell["correct"], n, "correct")
        require(abs(accuracy - correct / n) <= 1e-12, "correct/accuracy")
        pair_correct = integer_ratio(cell["query_pair_accuracy"], n // 2, "query_pair_accuracy")
        collapsed = count(cell["collapsed_pairs"], n // 2, "collapse")
        require(2 * pair_correct <= correct and pair_correct + collapsed <= n // 2, "pair consistency")
        margins = {c: scalar(cell[c], c) - THRESHOLDS[c] for c in THRESHOLDS if c != "two_order_accuracy"}
        for view, drop in (("evidence_blind", "evidence_drop"), ("query_blind", "query_drop")):
            r[view + "_correct"] = integer_ratio(accuracy - scalar(cell[drop], drop), n, view)
            r[view + "_accuracy"] = r[view + "_correct"] / n
    else:
        require(type(cell["groups"]) is int and cell["groups"] == n, "order groups")
        correct = count(cell["both_correct"], n, "both_correct")
        require(abs(accuracy - correct / n) <= 1e-12, "order accuracy")
        margins = {"two_order_accuracy": accuracy - THRESHOLDS["two_order_accuracy"]}
    failed = [c for c, margin in margins.items() if margin < 0]
    require(type(cell["passed"]) is bool and cell["passed"] is (not failed), "pass/margin mismatch")
    r.update(margins=margins, failed_criteria=failed)
    r["failure_class"] = ("pass" if not failed else "two_order" if kind == "two_order" else
                          "answer_involving" if {"accuracy", "query_pair_accuracy"} & set(failed) else "mask_only")
    return r


def view(pairs):
    criteria = {}
    for criterion in THRESHOLDS:
        selected = [(a, b) for a, b in pairs if criterion in a["margins"]]
        counts = dict.fromkeys(("both_pass", "rescued", "introduced", "both_fail"), 0)
        for a, b in selected:
            left, right = criterion in a["failed_criteria"], criterion in b["failed_criteria"]
            label = "both_fail" if left and right else "rescued" if left else "introduced" if right else "both_pass"
            counts[label] += 1
        criteria[criterion] = dict(evaluable=len(selected), control_fail=counts["rescued"] + counts["both_fail"],
                                   candidate_fail=counts["introduced"] + counts["both_fail"],
                                   candidate_minus_control=counts["introduced"] - counts["rescued"], **counts)
    totals = {}
    for index, arm in enumerate(ARMS):
        rows = [p[index] for p in pairs if p[index]["kind"] == "answer_cell"]
        totals[arm] = {k: sum(r[k] for r in rows) for k in
                       ("rows", "correct", "pairs", "collapsed_pairs", "evidence_blind_correct", "query_blind_correct")}
        totals[arm]["mask_only_cells"] = sum(r["failure_class"] == "mask_only" for r in rows)
        totals[arm]["answer_involving_cells"] = sum(r["failure_class"] == "answer_involving" for r in rows)
    return dict(paired_records=len(pairs), criteria=criteria, totals=totals)


def analyze(metrics):
    require([(m["seed"], m["arm"]) for m in metrics] == list(itertools.product(SEEDS, ARMS)), "model identities")
    records, parent_results = [], []
    for m in metrics:
        flags = {}
        for task in PROFILES:
            tm = m[task]
            rr = [normalized(m["seed"], m["arm"], task, c, kind)
                  for field, kind in (("cells", "answer_cell"), ("two_order", "two_order")) for c in tm[field]]
            keys = [key(r) for r in rr]
            require(len(keys) == len(set(keys)) and set(keys) == expected_keys(task), "complete unique grid")
            flags[task + "_pass"] = all(r["passed"] for r in rr)
            require(type(tm["passed"]) is bool and tm["passed"] is flags[task + "_pass"], "task pass")
            records.extend(sorted(rr, key=key))
        passed = flags["two_char_pass"] and flags["triple_pass"]
        require(type(m["passed"]) is bool and m["passed"] is passed, "whole pass")
        parent_results.append(dict(seed=m["seed"], arm=m["arm"], passed=passed, **flags))
    indexed = {(r["seed"], r["arm"], key(r)): r for r in records}
    pairs = [(r, indexed[(r["seed"], ARMS[1], key(r))]) for r in records if r["arm"] == ARMS[0]]
    triple = [(a, b) for a, b in pairs if a["task"] == "triple"]
    primary = dict(two_char_all=view([(a, b) for a, b in pairs if a["task"] == "two_char"]),
                   triple_all=view(triple))
    for profile, split in (("shared_prefix2", "HOLDOUT"), ("shared_suffix2", "TRAIN"), ("shared_suffix2", "HOLDOUT")):
        primary[profile + "_" + split.lower()] = view([(a, b) for a, b in triple if (a["profile"], a["split"]) == (profile, split)])
    primary["triple_seed280004"] = view([(a, b) for a, b in triple if a["seed"] == 280004])
    primary["triple_other_seeds"] = view([(a, b) for a, b in triple if a["seed"] != 280004])
    per_seed = {str(seed): view([(a, b) for a, b in triple if a["seed"] == seed]) for seed in SEEDS}
    summary = dict(parent_records=10, fixed_records=len(records), paired_records=len(pairs),
                   failure_records=sum(not r["passed"] for r in records), parent_results=parent_results,
                   primary=primary, per_seed_triple=per_seed, diagnostic_complete=True,
                   capability_gate_applicable=False, **dict.fromkeys(ZERO_KEYS, 0))
    report = dict(thresholds=THRESHOLDS, records=records, primary=primary, per_seed_triple=per_seed,
                  note="criterion counts overlap; all seeds primary; 280004/rest is explanatory only")
    return report, summary


def validate_parent(payload):
    s = payload["validation_summary"]
    require(payload["commit_sha"] == PARENT_EXECUTION and payload["status"] == "FAIL", "parent identity")
    require(payload["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "parent direct source pin")
    require(s["candidate_gate"] is False and s["all_replays"] is True and s["all_pairs_matched"] is True, "parent validity")
    for field, number in (("seed_pass_counts", 0), ("two_char_pass_counts", 4), ("triple_pass_counts", 0)):
        require(s[field] == dict.fromkeys(ARMS, number), "parent " + field)
    actual = {a["file"]: (a["sha256"], a["serialized_bytes"]) for a in payload["artifacts"]}
    require(len(payload["artifacts"]) == 7 and actual == PARENT_ARTIFACTS, "parent artifacts")


def load_parent(paths):
    parent, _, audit = context()
    paths = [Path(p).resolve() for p in paths]
    require(len(paths) == len(SUMMARY_SHAS) and all(audit.sha(p) == s for p, s in zip(paths, SUMMARY_SHAS, strict=True)), "parent summary hashes")
    with patch.object(torch.nn.Module, "_call_impl", side_effect=RuntimeError("C281 forbids neural calls")), \
         patch.object(torch.nn.Module, "load_state_dict", side_effect=RuntimeError("C281 forbids state loading")), \
         patch.object(torch, "save", side_effect=RuntimeError("C281 forbids checkpoint writes")):
        payload, metrics = parent.verify_artifacts(paths[0].parent, *paths[1:], PARENT_EXECUTION)
    parent.validate_result(payload)
    validate_parent(payload)
    return payload, metrics


def precheck(paths, root):
    validate_seal()
    payload, _ = load_parent(paths)
    _, factory, audit = context()
    root, p = Path(root), Path(paths[0]).resolve()
    pins, protected = dict(payload["source_blobs"]), dict(payload["input_sha256"])
    for name, wanted in pins.items():
        require(audit.git(root, "rev-parse", "HEAD:" + name).decode().strip() == wanted, "changed source:" + name)
    for name, wanted in protected.items():
        require(Path(name).is_file() and audit.sha(name) == wanted, "changed input:" + name)
    for child, wanted in [(p, SUMMARY_SHAS[0])] + [(audit.safe_child(p.parent, n), v[0]) for n, v in PARENT_ARTIFACTS.items()]:
        require(str(child.resolve()) not in protected and audit.sha(child) == wanted, "parent input")
        protected[str(child.resolve())] = wanted
    for name in OWN:
        require(name not in pins, "OWN collision")
        pins[name] = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9]|27[0-9]|280)_[^/]+)\.py"
    deps = set(factory.LM_SOURCES) | {n for n in payload["source_blobs"] if re.fullmatch(pattern, n)} | {OWN[0]}
    require(len(deps) == manifest()["direct_dependencies"] and deps <= set(pins), "direct source coverage")
    require(pins[PARENT_SOURCE] == PARENT_BLOB, "direct parent changed")
    protected.update(audit.protect_tree_files(root, pins))
    require((len(pins), len(protected)) == (manifest()["source_pins"], manifest()["protected_inputs"]), "protection cardinality")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}", flush=True)
    return pins, protected


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["status"] == "PASS", "result identity")
    require(p["diagnostic_execution_valid"] is True and p["capability_gate_applicable"] is False
            and p["gate_f_candidate"] is False and p["production_adoption"] is False, "scope")
    require((len(p["source_blobs"]), len(p["input_sha256"])) == (manifest()["source_pins"], manifest()["protected_inputs"])
            and set(OWN) <= set(p["source_blobs"]) and p["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "result protection")
    require(len(p["artifacts"]) == 3 and {a["file"] for a in p["artifacts"]} == set(OUTPUTS), "output set")
    s = p["validation_summary"]
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False, "diagnostic scope")
    require((s["parent_records"], s["fixed_records"], s["paired_records"]) == (10, 2160, 1080), "coverage")
    for k in ZERO_KEYS:
        require(type(s[k]) is int and s[k] == 0, "zero workload:" + k)
    rr = s["parent_results"]
    require([(r["seed"], r["arm"]) for r in rr] == list(itertools.product(SEEDS, ARMS)), "result models")
    require(all(r["passed"] is False and r["triple_pass"] is False and r["two_char_pass"] is (r["seed"] != 280004) for r in rr), "accepted parent subgates")


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == manifest()["modules"] - 1, "parent modules")
    return names + ["tests_lm.test_v05_c281_saved_support_transition_audit"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) == manifest()["loaded_tests"] and ids.count(EXCLUDED) == 1, "loaded suite")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require(len(kept) == manifest()["focused_tests"], "focused suite")
    return unittest.TestSuite(kept)


def guard(root, expected_head):
    audit = context()[-1]
    require(audit.git(root, "rev-parse", "HEAD").decode().strip() == expected_head
            and audit.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss"
            and not audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "repository guard")


def run(*, summaries, output_dir, expected_head):
    root, audit = Path(__file__).resolve().parents[2], context()[-1]
    guard(root, expected_head)
    pins, protected = precheck(summaries, root)
    parent, metrics = load_parent(summaries)
    report, summary = analyze(metrics)
    require(summary["parent_results"] == parent["validation_summary"]["seed_results"], "parent result reconstruction")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    for name, value in zip(OUTPUTS, (manifest(), report, summary), strict=True):
        (out / name).write_bytes(blob(value))
    artifacts = [dict(file=n, sha256=audit.sha(out / n), serialized_bytes=(out / n).stat().st_size) for n in OUTPUTS]
    guard(root, expected_head)
    precheck(summaries, root)
    p = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head, status="PASS",
             diagnostic_execution_valid=True, source_blobs=pins, input_sha256=protected,
             artifacts=artifacts, validation_summary=summary, capability_gate_applicable=False,
             gate_f_candidate=False, production_adoption=False)
    validate_result(p)
    (out / "summary.json").write_bytes(blob(p))
    print("=== C281 RESULT ===", flush=True)
    print(blob(p).decode(), flush=True)
    return p


def verify_artifacts(outdir, summaries, expected_head):
    audit, out = context()[-1], Path(outdir)
    p = audit.read_json(out / "summary.json")
    validate_result(p)
    require(p["commit_sha"] == expected_head, "execution HEAD")
    for name, wanted in p["input_sha256"].items():
        require(audit.sha(name) == wanted, "protected input")
    for a in p["artifacts"]:
        child = audit.safe_child(out, a["file"])
        require(audit.sha(child) == a["sha256"] and child.stat().st_size == a["serialized_bytes"], "output bytes")
    _, metrics = load_parent(summaries)
    report, summary = analyze(metrics)
    for name, value in zip(OUTPUTS, (manifest(), report, summary), strict=True):
        require(audit.read_json(out / name) == value, "persisted reconstruction:" + name)
    require(p["validation_summary"] == summary, "summary reconstruction")
    return p, report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summaries", nargs=7, type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
