"""C243: offline error analysis of fixed C242 final answers; no model execution."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import unittest

EXPERIMENT_ID = "C243-v5b-saved-recombination-error-audit"
STAGE = "V5-B-SAVED-RECOMBINATION-ERROR-AUDIT"
BASE = "17d5cd5d82c584faaee0b02d52a22776c9ef47a3"
PARENT_EXECUTION = "372c2c37429acece3f06a9b4521313da4b3d5f8e"
PARENT_SHA = "d10aad6f47eb2cabc35d8b6519b22c05ab634922cbc81a9bea6147ea7794cfcb"
PARENT_ARTIFACTS = {
    "measurements.json": "dcc69fcc29f3de2baf8a53082afd83dfa259d98a631689d2b916879b4b1a46f4",
    "recombination-plan.json": "8088155ef7ba95eb47a8a7ae3790247ff20d61804ac08c7fc1b1ed2f0c645760",
    "split-dataset.json": "9b5cc13cfe9dc9a139f23c44d87397f2af4f1174f1a9cf0fb4659d6ddfcad0b0",
    "trained-models.pt": "a71531049d76a89b29a9e9f38dfda47cda79c50c071aab32beb8bbfda481f387",
    "validation-summary.json": "5ac81c55f5d56e3984be7b769ae8a040a8965f16584c19c67423405f962cd3da",
}
SEEDS, FAMILIES = (234001, 234002, 234003), ("full", "gru_only")
SPLITS, VIEWS = ("TRAIN", "HOLDOUT"), ("normal", "evidence_blind", "query_blind")
ROWS = {"TRAIN": 32, "HOLDOUT": 64}
PARTNER = {0: 1, 1: 0, 2: 3, 3: 2}
RULES = ("entity", "other_entity", "partner_of_other", "query_fixed_position", "first", "last",
         "constant_0", "constant_1", "constant_2", "constant_3")
CATEGORIES = ("correct", "other_supplied", "absent_partner_of_other", "absent_partner_of_queried", "other_byte")
KINDS, TOL = ("fact", "query", "order"), 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c243_saved_recombination_audit.py",
       "tests_lm/test_v05_c243_saved_recombination_audit.py", "tools/run_c243.ps1", "tools/invoke_c243.ps1",
       "docs/experiment-ledger-addendum-c243-preregistration.md", "docs/v5b-saved-recombination-audit-v0.1.md")
OUTPUTS = {"audit-plan.json", "row-errors.json", "pair-audit.json", "diagnostics.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "02f2420c59bfa7a232686ea42cf2ed47ee6c17ebe2714e81a2fbc169a8e70379"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS, FAMILIES))


def parent_module():
    from fold_lm.v05_benchmarks import model_c242_balanced_recombination as parent
    return parent


def context():
    parent = parent_module()
    _, _, factory, audit = parent.context()
    return parent, factory, audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        identities=[list(x) for x in identities()], rows=ROWS, views=list(VIEWS), rules=list(RULES),
        categories=list(CATEGORIES), pair_kinds=list(KINDS), partner_map={str(k): v for k, v in PARTNER.items()},
        saved_predictions=1728, normal_rows=576, rule_comparisons=5760, pair_records=864, diagnostic_cells=24,
        model_forward_calls=0, new_training_steps=0, checkpoint_loads=0, checkpoint_writes=0, network_calls=0,
        source_pins=304, protected_inputs=466, direct_dependencies=19, own_tests=24,
        modules=128, loaded_tests=3002, focused_tests=3001, excluded_test=EXCLUDED, tolerance=TOL,
        gate="diagnostic integrity only; no agreement threshold", nll_recomputed=False,
        sample_scope="same accepted answers, no independent replication", causal_claim=False, capability_pass_claim=False,
        identifiability="TRAIN entity=partner_of_other; HOLDOUT four digits exhaust four named value categories",
        gate_f_candidate=False)


def validate_parts(parts):
    require(set(parts) == set(SPLITS) and digest(parts) == PARENT_ARTIFACTS["split-dataset.json"], "split identity")
    observed = defaultdict(set)
    for r in parts["TRAIN"]:
        x, y = r["values"]
        observed[x].add(y)
        observed[y].add(x)
    require(dict(observed) == {k: {v} for k, v in PARTNER.items()}, "TRAIN partner relation")
    for split, rows in parts.items():
        require(len(rows) == ROWS[split] and len({r["id"] for r in rows}) == len(rows), "row coverage")
        for r in rows:
            x, y = r["values"]
            require(r["objects"] == [0, 1] and x in PARTNER and y in PARTNER and x != y
                    and r["query"] in (0, 1) and r["order"] in (0, 1), "row semantics")
            require(r["target"] == 48 + r["values"][r["query"]], "target relation")
            require((PARTNER[x] == y) == (split == "TRAIN"), "split pair relation")
    for key in ("id", "prompt", "group"):
        require(not {r[key] for r in parts["TRAIN"]} & {r[key] for r in parts["HOLDOUT"]}, "split overlap")
    return parts


def rule_answers(row):
    values, q = row["values"], row["query"]
    rendered = values if row["order"] == 0 else values[::-1]
    return dict(entity=48 + values[q], other_entity=48 + values[1-q],
        partner_of_other=48 + PARTNER[values[1-q]], query_fixed_position=48 + rendered[q],
        first=48 + rendered[0], last=48 + rendered[1], **{f"constant_{d}": 48+d for d in range(4)})


def category(row, answer):
    rules = rule_answers(row)
    if answer == rules["entity"]:
        return "correct"
    if answer == rules["other_entity"]:
        return "other_supplied"
    if answer == rules["partner_of_other"]:
        return "absent_partner_of_other"
    if answer == 48 + PARTNER[row["values"][row["query"]]]:
        return "absent_partner_of_queried"
    return "other_byte"


def pairs(rows, lang, kind):
    require(kind in KINDS and lang in ("en", "ja"), "pair kind/language")
    groups = defaultdict(list)
    for i, r in enumerate(rows):
        if r["language"] != lang:
            continue
        if kind == "fact":
            key = (tuple(r["objects"]), tuple(sorted(r["values"])), r["order"], r["query"])
        else:
            key = (r["group"], r["order"] if kind == "query" else r["query"])
        groups[key].append(i)
    require(len(groups) == len(rows)//4 and all(len(g) == 2 for g in groups.values()), "pair count")
    for i, j in groups.values():
        require((rows[i]["target"] == rows[j]["target"]) == (kind == "order"), "pair target relation")
    return list(groups.values())


def discrete_metrics(rows, pred):
    n = len(rows)
    require(set(pred) == set(VIEWS), "view keys")
    require(all(isinstance(v, list) and len(v) == n and all(type(x) is int and 0 <= x < 256 for x in v)
                for v in pred.values()), "prediction byte schema")
    out = {}
    for lang in ("en", "ja"):
        ids = [i for i, r in enumerate(rows) if r["language"] == lang]
        require(len(ids) == n//2, "language count")
        acc = {v: sum(pred[v][i] == rows[i]["target"] for i in ids)/len(ids) for v in VIEWS}
        m = dict(rows=len(ids), accuracy=acc["normal"], evidence_blind_accuracy=acc["evidence_blind"],
                 query_blind_accuracy=acc["query_blind"], evidence_drop=acc["normal"]-acc["evidence_blind"],
                 query_drop=acc["normal"]-acc["query_blind"])
        for kind in KINDS:
            groups = pairs(rows, lang, kind)
            m[kind + "_pair_accuracy"] = sum(all(pred["normal"][i] == rows[i]["target"] for i in g) for g in groups)/len(groups)
        out[lang] = m
    return out


def validate_record(parts, record):
    require(set(record["final"]) == set(record["predictions"]) == set(SPLITS), "final split schema")
    require(record["checkpoint_roundtrip"] is True and record["prediction_replayed"] is True
            and record["weights_changed"] is True and type(record["reload_max_error"]) in (int, float)
            and 0 <= record["reload_max_error"] <= TOL, "parent replay flags")
    for split in SPLITS:
        measured = discrete_metrics(parts[split], record["predictions"][split])
        require(set(record["final"][split]) == {"en", "ja"}, "final languages")
        for lang, m in measured.items():
            saved = record["final"][split][lang]
            require(set(saved) == set(m) | {"answer_nll"}, "final metric keys")
            require(all(type(v) in (int, float) and math.isfinite(v) for v in saved.values())
                    and saved["answer_nll"] >= 0, "nonfinite parent metrics")
            require(all(abs(saved[k]-v) <= TOL for k, v in m.items()), "discrete metric replay")


def analyze(parts, records):
    validate_parts(parts)
    require([(r["seed"], r["family"]) for r in records] == identities(), "model identities")
    details, paired, cells = [], [], []
    for record in records:
        validate_record(parts, record)
        ident = dict(seed=record["seed"], family=record["family"])
        for split in SPLITS:
            rows, pred = parts[split], record["predictions"][split]
            for lang in ("en", "ja"):
                current = []
                for i, row in enumerate(rows):
                    if row["language"] != lang:
                        continue
                    item = dict(**ident, split=split, language=lang, id=row["id"], target=row["target"],
                        values=row["values"], query=row["query"], order=row["order"],
                        predictions={v: pred[v][i] for v in VIEWS}, rules=rule_answers(row), category=category(row, pred["normal"][i]))
                    current.append(item)
                details.extend(current)
                cells.append(dict(**ident, split=split, language=lang, rows=len(current),
                    categories={c: sum(r["category"] == c for r in current) for c in CATEGORIES},
                    rule_matches={rule: sum(r["predictions"]["normal"] == r["rules"][rule] for r in current) for rule in RULES}))
                for kind in KINDS:
                    for i, j in pairs(rows, lang, kind):
                        a, b = pred["normal"][i], pred["normal"][j]
                        paired.append(dict(**ident, split=split, language=lang, kind=kind,
                            ids=[rows[i]["id"], rows[j]["id"]], predictions=[a, b],
                            same_answer=a == b, both_correct=a == rows[i]["target"] and b == rows[j]["target"]))
    summary = dict(models=len(records), diagnostic_cells=len(cells), normal_rows=len(details),
        saved_predictions=sum(len(r["predictions"]) for r in details), rule_comparisons=sum(len(r["rules"]) for r in details),
        pair_records=len(paired), all_discrete_replays=True, model_forward_calls=0, new_training_steps=0,
        checkpoint_loads=0, checkpoint_writes=0, nll_recomputed=False, capability_pass_claim=False, causal_claim=False)
    return {"audit-plan.json": manifest(), "row-errors.json": details, "pair-audit.json": paired,
            "diagnostics.json": cells, "validation-summary.json": summary}


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["status"] == "PASS"
            and p["diagnostic_execution_valid"] is True, "diagnostic identity")
    require((len(p["source_blobs"]), len(p["input_sha256"])) == (304, 466) and set(OWN) <= set(p["source_blobs"]), "protection counts")
    require(len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS, "artifact coverage")
    s, m = p["validation_summary"], manifest()
    for k in ("diagnostic_cells", "normal_rows", "saved_predictions", "rule_comparisons", "pair_records",
              "model_forward_calls", "new_training_steps", "checkpoint_loads", "checkpoint_writes"):
        require(type(s[k]) is int and s[k] == m[k], "summary count: " + k)
    require(s["models"] == 6 and s["all_discrete_replays"] is True and s["nll_recomputed"] is False
            and s["capability_pass_claim"] is False and s["causal_claim"] is False
            and p["network_calls"] == 0 and p["gate_f_candidate"] is False, "scope/replay")


def precheck(c242_summary, root):
    parent, factory, a = context()
    root, path = Path(root), Path(c242_summary).resolve()
    require(a.sha(path) == PARENT_SHA, "parent summary hash")
    p = a.read_json(path)
    parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "FAIL"
            and p["validation_summary"]["cell_outcomes"] == {"RECOMBINATION_MISS": 12}, "accepted C242 state")
    pins, protected = dict(p["source_blobs"]), dict(p["input_sha256"])
    for name, wanted in protected.items():
        require(Path(name).is_file() and a.sha(name) == wanted, "changed input: " + name)
    for name, wanted in pins.items():
        require(a.git(root, "rev-parse", "HEAD:" + name).decode().strip() == wanted, "changed source: " + name)
    require(str(path) not in protected, "summary duplicate")
    protected[str(path)] = PARENT_SHA
    require({x["file"]: x["sha256"] for x in p["artifacts"]} == PARENT_ARTIFACTS, "parent artifact identities")
    for item in p["artifacts"]:
        child = a.safe_child(path.parent, item["file"])
        require(a.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "parent bytes")
        require(str(child.resolve()) not in protected, "artifact duplicate")
        protected[str(child.resolve())] = item["sha256"]
    for name in OWN:
        require(name not in pins, "OWN collision")
        pins[name] = a.git(root, "rev-parse", "HEAD:" + name).decode().strip()
    helpers = ("gate_f_c230_prepared_capsule.py", "model_c231_byte_eval_contract.py", "model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py", "model_c234_context_binding.py", "model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py", "model_c237_frozen_signal_audit.py", "model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py", "model_c240_saved_position_audit.py", "model_c241_assignment_holdout.py",
        "model_c242_balanced_recombination.py")
    deps = set(factory.LM_SOURCES) | {OWN[0]} | {"fold_lm/v05_benchmarks/" + h for h in helpers}
    require(len(deps) == 19 and deps <= set(pins), "dependency coverage")
    protected.update(a.protect_tree_files(root, pins))
    require((len(pins), len(protected)) == (304, 466) and digest(manifest()) == MANIFEST_SHA, "counts/manifest")
    return pins, protected


def load_inputs(c242_summary):
    parent, _, a = context()
    path = Path(c242_summary).resolve()
    parts = validate_parts(a.read_json(path.parent / "split-dataset.json"))
    records = a.read_json(path.parent / "measurements.json")
    require(parent.summarize(records) == a.read_json(path)["validation_summary"], "parent summary replay")
    require([(r["seed"], r["family"]) for r in records] == identities(), "parent order")
    for r in records:
        validate_record(parts, r)
    return parts, records


def regression_modules(root):
    names = parent_module().regression_modules(root)
    require(len(names) == len(set(names)) == 127, "parent modules")
    return names + ["tests_lm.test_v05_c243_saved_recombination_audit"]


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1, "suite identities")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require((len(tests), len(kept)) == (3002, 3001), "suite counts")
    return unittest.TestSuite(kept)


def run(*, c242_summary, output_dir, expected_head):
    _, _, a = context()
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root, "rev-parse", "HEAD").decode().strip() == expected_head, "execution HEAD")
        require(a.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss", "branch")
        require(not a.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "dirty tree")
    guard()
    pins, protected = precheck(c242_summary, root)
    parts, records = load_inputs(c242_summary)
    outputs = analyze(parts, records)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    for name, value in outputs.items():
        (out / name).write_bytes(blob(value))
    artifacts = [dict(file=name, sha256=a.sha(out/name), serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard()
    precheck(c242_summary, root)
    for name, wanted in protected.items():
        require(a.sha(name) == wanted, "modified input")
    p = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head, status="PASS",
        diagnostic_execution_valid=True, source_blobs=pins, input_sha256=protected, artifacts=artifacts,
        validation_summary=outputs["validation-summary.json"], gate_f_candidate=False, network_calls=0,
        limitations=["Saved answers are reused evidence, not new model samples.",
                     "Rule agreement cannot identify a causal/internal algorithm.",
                     "NLL is hash-protected but not reconstructed from answer bytes."])
    validate_result(p)
    (out / "summary.json").write_bytes(blob(p))
    print("=== C243 RESULT; SAVED C242 ANSWERS ONLY ===", flush=True)
    print(blob(p).decode(), flush=True)
    return p


def verify_artifacts(output_dir, c242_summary, expected_head):
    _, _, a = context()
    out = Path(output_dir)
    p = a.read_json(out / "summary.json")
    validate_result(p)
    require(p["commit_sha"] == expected_head, "saved execution identity")
    for name, wanted in p["input_sha256"].items():
        require(a.sha(name) == wanted, "postcheck input")
    for item in p["artifacts"]:
        child = a.safe_child(out, item["file"])
        require(a.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "postcheck bytes")
    outputs = analyze(*load_inputs(c242_summary))
    for name, value in outputs.items():
        require(a.read_json(out / name) == value, "persisted replay: " + name)
    require(outputs["validation-summary.json"] == p["validation_summary"], "saved summary replay")
    return p, outputs["diagnostics.json"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("c242-summary", "output-dir"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
