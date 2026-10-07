"""C310: exhaustive value-renaming consistency in saved C309 predictions; no new inference."""
from __future__ import annotations
import argparse
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

EXPERIMENT_ID = "C310-v5b-saved-value-renaming"
STAGE = "V5-B-SAVED-VALUE-RENAMING"
BASE = "2cffcea33045a75582a94fadd963fa9f2b7d601d"
PARENT_EXECUTION = "a38c6ff864ab40efa74397017cfeec9f5628ca11"
PARENT_SHA = "c8a1a2bd3d6ad4e4d6f714b38af3ce8424d314d1f5771b5fca578d49df37066c"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c309_core_lr_replication.py"
PARENT_BLOB = "8c66d64aa7ca3558d914a9b34bc9612ef444a9c2"
WIDE_SOURCE = "fold_lm/v05_benchmarks/model_c304_length_breadth.py"
WIDE_BLOB = "cacb5852a29171aa8079e634d929fdd54e7f4f58"
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
SEEDS = tuple(range(309001, 309006))
ARMS = ("full_train", "core_frozen", "core_slow")
LENGTHS = (2, 3, 4, 5)
PROFILES = ("repeat", "shared_prefix", "shared_suffix")
OLD_PROFILES = ("tripled", "shared_prefix2", "shared_suffix2")
SPLITS = ("TRAIN", "HOLDOUT")
PERMUTATIONS = tuple(itertools.permutations(range(4)))
OWN = ("fold_lm/v05_benchmarks/model_c310_value_renaming_audit.py", "tests_lm/test_v05_c310_value_renaming_audit.py",
       "tools/run_c310.ps1", "tools/invoke_c310.ps1", "docs/experiment-ledger-addendum-c310-preregistration.md",
       "docs/v5b-value-renaming-v0.1.md")
OUTPUTS = ("audit-plan.json", "value-renaming-report.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
ZERO = dict(model_forward_calls=0, train_steps=0, model_state_loads=0, new_checkpoint_writes=0,
            row_presentations=0, core_forward_calls=0, network_calls=0)
COUNT_KEYS = ("comparisons", "equivariant", "violations", "both_correct", "both_wrong", "correct_to_wrong",
              "wrong_to_correct", "equivariant_wrong", "left_correct", "right_correct", "same_prediction")
MANIFEST_SHA = "0b4304400ddb57789a52aefb0bfe84690df7bb3fee9ef4c63e842fecfd595596"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS, ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c309_core_lr_replication as parent
    chain = parent.context()
    return parent, chain[4], chain[-1]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE, parent_execution=PARENT_EXECUTION,
        parent_summary_sha256=PARENT_SHA, parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
        wide_source=WIDE_SOURCE, wide_blob=WIDE_BLOB, dataset_sha256=DATA_SHA,
        question="do predictions follow bijective value relabeling with names/query/order fixed across original value splits",
        seeds=list(SEEDS), arms=list(ARMS), lengths=list(LENGTHS), permutations=[list(p) for p in PERMUTATIONS],
        class_map="permute ASCII0..3 only;other252 classes fixed;full256 argmax with first-class tie rule;report tied maxima",
        partition="22 changed-input permutations per row;identity and absent-pair swap reported separately",
        observations=51840, changed_input_comparisons=1140480, absent_swap_comparisons=51840, identity_comparisons=51840,
        changed_groups=240, absent_swap_groups=120, identity_groups=60, original_total_groups=720, prediction_blocks=60,
        diagnostic_gate="parent reconstruction,complete bijective alignment,original totals and independent saved-report reconstruction only",
        limits="consistency is not correctness;directed dependent comparisons;each changed target occurs twice;no new capability gate",
        numeric_threads=2, parents=36, source_pins=706, protected_inputs=1323, own_tests=32, modules=195, loaded_tests=4942, focused_tests=4941,
        excluded_test=EXCLUDED, capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False, **ZERO)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None and digest(manifest()) == MANIFEST_SHA, "manifest seal")


def expected_parent_flags():
    out = []
    for seed, arm in identities():
        flags = {str(n): not (seed == 309005 and arm == "full_train")
                 and not (seed == 309002 and (arm != "full_train" or n >= 4)) for n in LENGTHS}
        out.append(dict(seed=seed, arm=arm, length_pass=flags, quint_pass=flags["5"], all_lengths_pass=all(flags.values()),
            fitted_train_direct_pass=True, trained_length_holdout_direct_pass=all(flags[str(n)] for n in (2, 3, 4))))
    return out


def row_key(row, values=None):
    return (row["language"], tuple(row["entities"]), tuple(row["values"] if values is None else values),
            tuple(row["permutation"]), row["query"])


def align_values(data):
    require(set(data) == set(SPLITS) and [len(data[s]) for s in SPLITS] == [192, 96], "data domain")
    rows = data["TRAIN"]+data["HOLDOUT"]
    require(all(type(r["id"]) is str for r in rows) and len({r["id"] for r in rows}) == 288, "unique source IDs")
    for split in SPLITS:
        for r in data[split]:
            e, v, order, q = r["entities"], r["values"], r["permutation"], r["query"]
            require(r["language"] in ("en", "ja") and len(e) == len(v) == len(order) == 2
                    and len(set(e)) == len(set(v)) == 2, "fact shape")
            require(all(type(x) is int and 0 <= x < 3 for x in e+order)
                    and all(type(x) is int and 0 <= x < 4 for x in v)
                    and sorted(order) == sorted(e) and type(q) is int and q in e, "fact values")
            require(type(r["target"]) is int and r["target"] == 48+v[e.index(q)], "target binding")
            require((split == "HOLDOUT") == ((v[1]-v[0]) % 4 == 2), "original split")
    index = {row_key(r): i for i, r in enumerate(rows)}
    require(len(index) == 288, "duplicate logical row")
    maps, labels = [], []
    for perm in PERMUTATIONS:
        keys = [row_key(r, [perm[v] for v in r["values"]]) for r in rows]
        require(all(k in index for k in keys), "missing relabeled counterpart")
        ids = [index[k] for k in keys]
        require(sorted(ids) == list(range(288)), "bijection")
        label = list(range(256)); label[48:52] = [48+v for v in perm]
        require(all(rows[j]["target"] == label[r["target"]] for r, j in zip(rows, ids, strict=True)), "renamed target")
        maps.append(ids); labels.append(label)
    mapping = torch.tensor(maps, dtype=torch.int64); label_map = torch.tensor(labels, dtype=torch.int64)
    same = mapping == torch.arange(288)
    require(bool(same[0].all()) and bool((same.sum(0) == 2).all())
            and bool((~same).sum(0).eq(22).all()), "stabilizer inventory")
    return rows, mapping, label_map


def validate_counts(r):
    require(all(type(r[k]) is int and 0 <= r[k] <= r["comparisons"] for k in COUNT_KEYS)
            and r["comparisons"] > 0, "count type/range")
    require(r["comparisons"] == r["equivariant"]+r["violations"]
            and r["comparisons"] == sum(r[k] for k in ("both_correct", "both_wrong", "correct_to_wrong", "wrong_to_correct"))
            and r["left_correct"] == r["both_correct"]+r["correct_to_wrong"]
            and r["right_correct"] == r["both_correct"]+r["wrong_to_correct"]
            and r["equivariant"] == r["both_correct"]+r["equivariant_wrong"]
            and r["equivariant_wrong"] <= r["both_wrong"], "count conservation")


def count_comparisons(pred, targets, mapping, labels, mask):
    require(pred.shape == targets.shape == (288,) and pred.dtype == targets.dtype == torch.int64
            and mapping.shape == (24, 288) and labels.shape == (24, 256)
            and mapping.dtype == labels.dtype == torch.int64
            and mask.shape == (24, 288) and mask.dtype == torch.bool, "comparison tensors")
    require(bool(((pred >= 0) & (pred < 256)).all()), "prediction domain")
    left = pred.expand(24, -1); right = pred[mapping]
    eq = right == labels[:, pred]; lc = (pred == targets).expand(24, -1); rc = right == targets[mapping]
    def n(condition):
        return int((mask & condition).sum())
    out = dict(comparisons=int(mask.sum()), equivariant=n(eq), violations=n(~eq), both_correct=n(lc & rc), both_wrong=n(~lc & ~rc),
        correct_to_wrong=n(lc & ~rc), wrong_to_correct=n(~lc & rc), equivariant_wrong=n(eq & ~lc & ~rc),
        left_correct=n(lc), right_correct=n(rc), same_prediction=n(left == right))
    require(n(lc & rc & ~eq) == 0, "correct answers must transform")
    validate_counts(out)
    return out


def original_total(rows, predictions, language):
    ids = [i for i, r in enumerate(rows) if r["language"] == language]; pairs = {}
    for i in ids:
        r = rows[i]; pairs.setdefault(row_key(r)[:-1], []).append(i)
    require(all(len(g) == 2 and {rows[i]["query"] for i in g} == set(rows[g[0]]["entities"]) for g in pairs.values()), "query pairs")
    return dict(rows=len(ids), correct=sum(predictions[i] == rows[i]["target"] for i in ids), pairs=len(pairs),
        collapsed_pairs=sum(predictions[g[0]] == predictions[g[1]] for g in pairs.values()))


def analyze(records, data, metrics):
    require([(r["seed"], r["arm"]) for r in records] == identities()
            and [(r["seed"], r["arm"]) for r in metrics] == identities(), "complete parent cohort")
    rows, mapping, labels = align_values(data); target = torch.tensor([r["target"] for r in rows])
    splits = torch.tensor([0]*192+[1]*96); changed = mapping != torch.arange(288)
    nonidentity = torch.arange(24)[:, None] != 0
    masks = {(a, z): changed & (splits == a)[None, :] & (splits[mapping] == z) for a, z in itertools.product(range(2), repeat=2)}
    stable_masks = {a: ~changed & nonidentity & (splits == a)[None, :] for a in range(2)}
    identity_mask = ~nonidentity.expand(24, 288)
    changes, stabilizers, controls, originals, blocks = [], [], [], [], []
    for record, metric in zip(records, metrics, strict=True):
        require(set(record["raw"]) == set(map(str, LENGTHS))
                and set(metric["length_scores"]) == set(map(str, LENGTHS)), "length inventory")
        for length in LENGTHS:
            key = dict(seed=record["seed"], arm=record["arm"], identifier_length=length)
            acc = {k: dict.fromkeys(COUNT_KEYS, 0) for k in masks}
            stab = {k: dict.fromkeys(COUNT_KEYS, 0) for k in stable_masks}; ident = dict.fromkeys(COUNT_KEYS, 0)
            predictions = {}; tied_indices = {}
            raw = record["raw"][str(length)]; require(set(raw) == set(SPLITS), "raw splits")
            for profile, old_profile in zip(PROFILES, OLD_PROFILES, strict=True):
                pp, ties = [], []
                for split in SPLITS:
                    require(set(raw[split]) == set(PROFILES)
                            and set(raw[split][profile]) == {"normal", "evidence_blind", "query_blind"}, "raw views")
                    z = raw[split][profile]["normal"]
                    require(isinstance(z, torch.Tensor) and z.shape == (len(data[split]), 256) and z.dtype == torch.float64
                            and z.device.type == "cpu" and not z.requires_grad and bool(torch.isfinite(z).all()), "saved logits")
                    pred = z.argmax(1).tolist(); offset = len(pp); pp.extend(pred)
                    tied = (z == z.max(1, keepdim=True).values).sum(1) > 1
                    ties.extend(offset+i for i in tied.nonzero().flatten().tolist())
                    for language in ("en", "ja"):
                        totals = original_total(data[split], pred, language)
                        old = [r for r in metric["length_scores"][str(length)]["totals"]
                               if (r["split"], r["profile"], r["language"]) == (split, old_profile, language)]
                        require(len(old) == 1 and all(old[0][k] == v for k, v in totals.items()), "original normal totals")
                        tie_count = sum(bool(tied[i]) for i, r in enumerate(data[split]) if r["language"] == language)
                        originals.append(dict(**key, split=split, profile=profile, language=language,
                                              tied_max_rows=tie_count, **totals))
                predictions[profile] = pp; tied_indices[profile] = ties; p = torch.tensor(pp, dtype=torch.int64)
                for destination, mask in masks.items():
                    for k, v in count_comparisons(p, target, mapping, labels, mask).items(): acc[destination][k] += v
                for split, mask in stable_masks.items():
                    for k, v in count_comparisons(p, target, mapping, labels, mask).items(): stab[split][k] += v
                for k, v in count_comparisons(p, target, mapping, labels, identity_mask).items(): ident[k] += v
            for (a, z), values in acc.items():
                changes.append(dict(**key, source_split=SPLITS[a], destination_split=SPLITS[z], **values))
            for a, values in stab.items(): stabilizers.append(dict(**key, source_split=SPLITS[a], **values))
            require(ident["violations"] == 0, "identity control")
            controls.append(dict(**key, **ident))
            blocks.append(dict(**key, predictions=predictions, tied_max_indices=tied_indices))
    require((len(changes), len(stabilizers), len(controls), len(originals), len(blocks)) == (240, 120, 60, 720, 60), "inventory")
    summary = dict(parent_results=expected_parent_flags(), changed_input=changes, absent_swap=stabilizers, identity_controls=controls,
        observations=51840, changed_input_comparisons=sum(r["comparisons"] for r in changes),
        absent_swap_comparisons=sum(r["comparisons"] for r in stabilizers), identity_comparisons=sum(r["comparisons"] for r in controls),
        original_totals_verified=720, tied_max_rows=sum(r["tied_max_rows"] for r in originals),
        diagnostic_complete=True, capability_gate_applicable=False, **ZERO)
    require((summary["changed_input_comparisons"], summary["absent_swap_comparisons"], summary["identity_comparisons"])
            == (1140480, 51840, 51840), "comparison counts")
    return dict(row_ids=[r["id"] for r in rows], permutations=[list(p) for p in PERMUTATIONS], destination_indices=mapping.tolist(),
                predictions=blocks, original_totals=originals, summary=summary), summary


@contextmanager
def no_neural():
    with torch.no_grad(), patch.object(torch.nn.Module, "_call_impl", side_effect=RuntimeError("C310 forbids model calls")), \
         patch.object(torch.nn.Module, "load_state_dict", side_effect=RuntimeError("C310 forbids state loading")), \
         patch.object(torch, "save", side_effect=RuntimeError("C310 forbids tensor/checkpoint writes")):
        yield


def load_parent(paths):
    parent, wide, c = context(); paths = [Path(p).resolve() for p in paths]
    hashes = (PARENT_SHA, *parent.parent_hashes(parent.context()[0]))
    require(len(paths) == len(hashes) == 36 and all(c.audit.sha(p) == h for p, h in zip(paths, hashes, strict=True)), "parent hashes")
    with no_neural():
        p, metrics = parent.verify_artifacts(paths[0].parent, paths[1:], PARENT_EXECUTION); parent.validate_result(p)
        require(p["experiment_id"] == "C309-v5b-core-lr-replication" and p["status"] == "FAIL" and p["commit_sha"] == PARENT_EXECUTION
                and p["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB and p["source_blobs"].get(WIDE_SOURCE) == WIDE_BLOB, "parent identity")
        require(len(p["artifacts"]) == 7 and {a["file"] for a in p["artifacts"]} == set(parent.OUTPUTS), "parent descriptors")
        s = p["validation_summary"]
        require(s["seed_results"] == expected_parent_flags() and s["candidate_gate"] is False
                and s["all_replays"] is True and s["all_groups_matched"] is True, "parent outcomes")
        data = c.audit.read_json(paths[0].parent/"dataset.json"); c.p267.validate_data(data)
        require(digest(data) == DATA_SHA, "data hash")
        archive = torch.load(paths[0].parent/"evaluations.pt", map_location="cpu", weights_only=True)
        require(set(archive) == {"schema", "records"} and archive["schema"] == "fold-c309-core-lr-replication-eval-v1", "parent archive")
    return p, archive["records"], data, metrics


def precheck(paths, root):
    torch.set_num_threads(2)
    validate_seal(); p, _, _, _ = load_parent(paths); parent, wide, c = context(); root = Path(root).resolve()
    pins, inputs = dict(p["source_blobs"]), dict(p["input_sha256"])
    require((len(pins), len(inputs)) == (700, 1309) and all(pins.get(n) == h for n, h in wide.PINNED.items()), "inherited protection")
    for m in [parent, *parent.context(), *wide.context(), *vars(c).values(), c.factory.language_module()]:
        path = getattr(m, "__file__", None) if isinstance(m, ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            require(Path(path).resolve().relative_to(root).as_posix() in pins, "unprotected helper")
    for n, h in pins.items(): require(c.audit.git(root, "rev-parse", "HEAD:"+n).decode().strip() == h, "changed source:"+n)
    for n, h in inputs.items(): require(Path(n).is_file() and c.audit.sha(n) == h, "changed input:"+n)
    folder = Path(paths[0]).resolve().parent
    for path, h in [(folder/"summary.json", PARENT_SHA)]+[(c.audit.safe_child(folder, a["file"]), a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in inputs and c.audit.sha(path) == h, "parent input"); inputs[str(path.resolve())] = h
    for n in OWN:
        require(n not in pins, "OWN collision"); pins[n] = c.audit.git(root, "rev-parse", "HEAD:"+n).decode().strip()
    inputs.update(c.audit.protect_tree_files(root, pins)); require((len(pins), len(inputs)) == (706, 1323), "protection counts")
    print(f"registration_check = source_pins:706; protected_inputs:1323; manifest_sha256:{MANIFEST_SHA}", flush=True)
    return pins, inputs


def runtime_preflight(paths, root):
    torch.set_num_threads(2)
    precheck(paths, root)
    with no_neural():
        _, records, data, metrics = load_parent(paths)
        _, summary = analyze(records, data, metrics)
    require(summary["observations"] == 51840, "real audit coverage")
    print("real_saved_value_alignment_and_totals = PASS; no new model execution", flush=True)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["status"] == "PASS"
            and p["diagnostic_execution_valid"] is True, "result identity")
    require(all(p[k] is False for k in ("capability_gate_applicable", "gate_f_candidate", "production_adoption")), "result scope")
    require((len(p["source_blobs"]), len(p["input_sha256"])) == (706, 1323) and set(OWN) <= set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB and p["source_blobs"].get(WIDE_SOURCE) == WIDE_BLOB, "result pins")
    require(len(p["artifacts"]) == 3 and {a["file"] for a in p["artifacts"]} == set(OUTPUTS), "result artifacts")
    s = p["validation_summary"]
    require(s["parent_results"] == expected_parent_flags() and s["diagnostic_complete"] is True
            and s["capability_gate_applicable"] is False, "diagnostic scope")
    require(all(type(s[k]) is int and s[k] == v for k, v in ZERO.items()), "zero workload")
    expected_keys = {
        "changed_input": [(seed, arm, n, a, z) for seed, arm in identities() for n in LENGTHS for a, z in itertools.product(SPLITS, repeat=2)],
        "absent_swap": [(seed, arm, n, a) for seed, arm in identities() for n in LENGTHS for a in SPLITS],
        "identity_controls": [(seed, arm, n) for seed, arm in identities() for n in LENGTHS],
    }
    for key, count in (("changed_input", 1140480), ("absent_swap", 51840), ("identity_controls", 51840)):
        rr = s[key]
        fields = ("seed", "arm", "identifier_length") + (("source_split", "destination_split") if key == "changed_input" else ("source_split",) if key == "absent_swap" else ())
        require([tuple(r[f] for f in fields) for r in rr] == expected_keys[key]
                and sum(r["comparisons"] for r in rr) == count, "result counts/keys")
        require(s[{"changed_input": "changed_input_comparisons", "absent_swap": "absent_swap_comparisons", "identity_controls": "identity_comparisons"}[key]] == count, "declared count")
        for r in rr:
            validate_counts(r)
    require(all(r["violations"] == 0 for r in s["identity_controls"]) and s["observations"] == 51840
            and s["original_totals_verified"] == 720 and type(s["tied_max_rows"]) is int
            and 0 <= s["tied_max_rows"] <= 51840, "result controls")


def flatten(suite):
    for t in suite:
        if isinstance(t, unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names = context()[0].regression_modules(root); require(len(names) == len(set(names)) == 194, "parent modules")
    return names+["tests_lm.test_v05_c310_value_renaming_audit"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) == 4942 and ids.count(EXCLUDED) == 1, "loaded suite")
    kept = [t for t in tests if t.id() != EXCLUDED]; require(len(kept) == 4941, "focused suite")
    return unittest.TestSuite(kept)


def guard(root, head, c):
    require(c.audit.git(root, "rev-parse", "HEAD").decode().strip() == head
            and c.audit.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss"
            and not c.audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "repository guard")


def run(*, summaries, output_dir, expected_head):
    torch.set_num_threads(2)
    _, _, c = context(); root = Path(__file__).resolve().parents[2]; guard(root, expected_head, c)
    pins, inputs = precheck(summaries, root)
    with no_neural():
        _, records, data, metrics = load_parent(summaries); report, s = analyze(records, data, metrics)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False)
    for n, v in zip(OUTPUTS, (manifest(), report, s), strict=True): (out/n).write_bytes(blob(v))
    artifacts = [dict(file=n, sha256=c.audit.sha(out/n), serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root, expected_head, c); precheck(summaries, root)
    p = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head, status="PASS", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256=inputs, artifacts=artifacts, validation_summary=s,
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    receipt = {k: p[k] for k in ("experiment_id", "stage", "commit_sha", "status", "artifacts")}
    receipt["summary_sha256"] = c.audit.sha(out/"summary.json")
    print("=== C310 COMPACT DIAGNOSTIC RECEIPT ===", flush=True)
    print(json.dumps(receipt, indent=2, sort_keys=True), flush=True)
    return p


def verify_artifacts(outdir, summaries, expected_head):
    torch.set_num_threads(2)
    _, _, c = context(); out = Path(outdir); p = c.audit.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"] == expected_head, "execution HEAD")
    for n, h in p["input_sha256"].items(): require(c.audit.sha(n) == h, "protected input")
    for a in p["artifacts"]:
        path = c.audit.safe_child(out, a["file"])
        require(c.audit.sha(path) == a["sha256"] and path.stat().st_size == a["serialized_bytes"], "output bytes")
    with no_neural():
        _, records, data, metrics = load_parent(summaries); report, s = analyze(records, data, metrics)
    for n, v in zip(OUTPUTS, (manifest(), report, s), strict=True): require(c.audit.read_json(out/n) == v, "persisted:"+n)
    require(p["validation_summary"] == s, "summary reconstruction")
    return p, report


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--summaries", nargs=36, type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True); parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
