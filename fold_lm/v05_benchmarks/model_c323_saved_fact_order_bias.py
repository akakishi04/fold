"""C323: saved four-response order counterfactuals; no model execution."""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import itertools
import json
from pathlib import Path
from types import ModuleType
import unittest

EXPERIMENT_ID = "C323-v5b-saved-fact-order-bias"
STAGE = "V5-B-SAVED-FACT-ORDER-BIAS"
BASE = "a0e2221eb8f12b5a2cc8f325876a8752ed1b9eb1"
PARENT_EXECUTION = "b7943ab4435d68d2716e6137b596042b777f2efb"
PARENT_SHA = "fdcf1f2ac893a46c900e50db93740004926c70765ca269ba0cfe7474bf4c5796"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c322_saved_query_contrast.py"
PARENT_BLOB = "c93fb85922c5907c424698897de4af2888f81f77"
SEEDS = tuple(range(319001, 319006))
ARMS = ("mean_last", "last_only")
CONDITIONS = ("old4", "interior")
SPLITS = ("TRAIN", "HOLDOUT")
PROFILES = ("u_dominant", "balanced", "v_dominant")
LANGUAGES = ("en", "ja")
OWN = ("fold_lm/v05_benchmarks/model_c323_saved_fact_order_bias.py",
       "tests_lm/test_v05_c323_saved_fact_order_bias.py",
       "tools/run_c323.ps1", "tools/invoke_c323.ps1",
       "docs/experiment-ledger-addendum-c323-preregistration.md",
       "docs/v5b-saved-fact-order-bias-v0.1.md")
OUTPUTS = ("audit-plan.json", "order-counterfactuals.json", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10, parent_query_pairs=8640, order_counterfactuals=4320, normal_answers=17280,
            reporting_groups=240, score_reconciliations=4, train_steps=0, model_forward_calls=0,
            model_state_loads=0, new_checkpoint_writes=0, network_calls=0)
MANIFEST_SHA = "8c4e9152cb11d1492cd7d88cf7caafef40a901de6c68aa44e404c1c46ff7c5de"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def context():
    from fold_lm.v05_benchmarks import model_c322_saved_query_contrast as p
    parent, model, owner, x = p.context()
    return p, parent, model, owner, x


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
                parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
                question="do frozen C321 answers follow first/last fact position when the fact order swaps",
                conditions=list(CONDITIONS), arms=list(ARMS), seeds=list(SEEDS),
                splits=list(SPLITS), profiles=list(PROFILES), languages=list(LANGUAGES),
                unit="four normal argmax results per fixed logical facts/values/two question names/two fact orders",
                first_last="position in the rendered facts;never selected by target or output rank",
                classifications="first-fact in both orders,last-fact in both orders,one-value lock,query-consistent,other",
                controls="compare every old4 group with its matched interior family;do not modify saved logits or gate flags",
                fixed_gate="diagnostic integrity,not model capability;old C321 negative remains",
                parents=49, source_pins=784, protected_inputs=1478, own_tests=24,
                modules=208, loaded_tests=5294, focused_tests=5293, excluded_test=EXCLUDED,
                capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False,
                **WORK)


def validate_seal():
    require(len(MANIFEST_SHA) == 64 and digest(manifest()) == MANIFEST_SHA, "manifest seal")


def logical_index(data):
    require(set(data) == set(SPLITS), "logical split inventory")
    byid = {}
    for split in SPLITS:
        index = {}
        for row in data[split]:
            require(row["id"] not in index, "duplicate source row ID")
            entities = tuple(row["entities"])
            values = tuple(row["values"])
            perm = tuple(row["permutation"])
            require(len(entities) == len(values) == 2 and len(set(entities)) == len(set(values)) == 2
                    and (perm == entities or perm == entities[::-1])
                    and row["query"] in entities and row["language"] in LANGUAGES, "bad source row")
            require(type(row["target"]) is int and row["target"] == 48 + values[entities.index(row["query"])], "source target")
            index[row["id"]] = row
        require(len(index) in (192, 96), "source row count")
        byid[split] = index
    return byid


def parent_ordered_hashes(p, parent, model, owner):
    return (PARENT_SHA, p.PARENT_SHA, parent.PARENT_SHA, *model.parent_hashes(owner))


def load_parent(paths):
    p, parent, model, owner, x = context()
    paths = [Path(z).resolve() for z in paths]
    hashes = parent_ordered_hashes(p, parent, model, owner)
    require(len(paths) == len(hashes) == 49 and all(x.c.audit.sha(z) == sha for z, sha in zip(paths, hashes, strict=True)), "49 parent hashes")
    with x.guarded.no_neural():
        evidence, _ = p.verify_artifacts(paths[0].parent, paths[1:], PARENT_EXECUTION)
        p.validate_result(evidence)
        require(evidence["commit_sha"] == PARENT_EXECUTION and evidence["experiment_id"] == "C322-v5b-saved-query-contrast"
                and evidence["status"] == "PASS" and evidence["capability_gate_applicable"] is False
                and evidence["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "parent identity")
        require(len(evidence["artifacts"]) == 4 and {a["file"] for a in evidence["artifacts"]} == set(p.OUTPUTS), "parent artifact inventory")
        require(evidence["validation_summary"]["diagnostic_complete"] is True
                and len(evidence["validation_summary"]["overall"]) == 4, "parent diagnostic completeness")
        _, data, _ = p.load_parent(paths[1:])
        pairs = x.c.audit.read_json(paths[0].parent / "query-pairs.json")
    require(len(pairs) == 8640, "parent saved-pair inventory")
    logical_index(data)
    return evidence, data, pairs


def classify_pair(entry, source_ids):
    """Use the source record's fact permutation, never a post-hoc answer choice."""
    split = entry["split"]
    require(split in SPLITS and entry["language"] in LANGUAGES, "pair split/language")
    a = source_ids[split].get(entry["row_A"])
    b = source_ids[split].get(entry["row_B"])
    require(a is not None and b is not None, "pair source rows")
    entities = tuple(a["entities"])
    values = tuple(a["values"])
    perm = tuple(a["permutation"])
    require(a["query"] == entities[0] and b["query"] == entities[1]
            and all(a[k] == b[k] for k in ("language", "entities", "values", "permutation"))
            and a["language"] == entry["language"] and a["target"] == entry["target_A"]
            and b["target"] == entry["target_B"], "paired source binding")
    first = 48 + values[entities.index(perm[0])]
    last = 48 + values[entities.index(perm[1])]
    pa, pb = entry["prediction_A"], entry["prediction_B"]
    require(all(type(z) is int and 0 <= z < 256 for z in (pa, pb)) and first != last, "prediction domain")
    require(entry["same_prediction"] is (pa == pb)
            and entry["correct_count"] == int(pa == a["target"]) + int(pb == b["target"]), "parent row outcomes")
    profile = entry["profile"]
    require(profile in PROFILES and entry["source_profile"] == ("repeat", "shared_prefix", "shared_suffix")[PROFILES.index(profile)]
            if entry["condition"] == "old4" else profile in PROFILES and entry["source_profile"] == profile, "profile mapping")
    return (entry["seed"], entry["arm"], entry["condition"], split, profile, entry["language"], entities, values, perm,
            dict(prediction_A=pa, prediction_B=pb, target_A=a["target"], target_B=b["target"],
                 first_value=first, last_value=last, collapsed=pa == pb,
                 both_first=pa == first and pb == first,
                 both_last=pa == last and pb == last,
                 both_correct=pa == a["target"] and pb == b["target"],
                 correct=entry["correct_count"],
                 first_answers=int(pa == first) + int(pb == first),
                 last_answers=int(pa == last) + int(pb == last),
                 other_answers=int(pa not in (first, last)) + int(pb not in (first, last))))


def order_quad(pair1, pair2, key):
    """Pair two fact permutations with both query directions held constant."""
    x, y = pair1, pair2
    require((x["first_value"], x["last_value"]) == (y["last_value"], y["first_value"]), "fact order swap")
    preds = (x["prediction_A"], x["prediction_B"], y["prediction_A"], y["prediction_B"])
    first = x["both_first"] and y["both_first"]
    last = x["both_last"] and y["both_last"]
    stable = int(preds[0] == preds[2]) + int(preds[1] == preds[3])
    return dict(seed=key[0], arm=key[1], condition=key[2], split=key[3], profile=key[4], language=key[5],
                entities=list(key[6]), values=list(key[7]),
                correct=x["correct"] + y["correct"],
                four_correct=x["both_correct"] and y["both_correct"],
                collapsed_orders=int(x["collapsed"]) + int(y["collapsed"]),
                first_fact_both_orders=first, last_fact_both_orders=last,
                same_value_all_four=len(set(preds)) == 1,
                same_query_across_orders=stable,
                changed_query_across_orders=2 - stable,
                first_fact_answers=x["first_answers"] + y["first_answers"],
                last_fact_answers=x["last_answers"] + y["last_answers"],
                other_class_answers=x["other_answers"] + y["other_answers"])


def aggregate(rows):
    require(rows, "empty group")
    totals = dict(counterfactuals=len(rows), answers=4 * len(rows), query_pairs=2 * len(rows))
    fields = ("correct", "four_correct", "collapsed_orders", "first_fact_both_orders", "last_fact_both_orders",
              "same_value_all_four", "same_query_across_orders", "changed_query_across_orders",
              "first_fact_answers", "last_fact_answers", "other_class_answers")
    for key in fields:
        totals[key] = sum(z[key] for z in rows)
    require(totals["answers"] == totals["first_fact_answers"] + totals["last_fact_answers"] + totals["other_class_answers"]
            and totals["same_query_across_orders"] + totals["changed_query_across_orders"] == 2 * len(rows), "classification conservation")
    return totals


def analyze(data, pairs, parent_summary):
    ids = logical_index(data)
    groups = defaultdict(dict)
    require(len(pairs) == 8640, "query-pair count")
    for entry in pairs:
        seed, arm, condition, split, profile, language, entities, values, perm, row = classify_pair(entry, ids)
        require(seed in SEEDS and arm in ARMS and condition in CONDITIONS, "cohort membership")
        key = (seed, arm, condition, split, profile, language, entities, values)
        require(perm not in groups[key], "duplicate fact permutation")
        groups[key][perm] = row
    require(len(groups) == 4320, "counterfactual inventory")
    details = []
    for key in sorted(groups):
        permutations = groups[key]
        entities = key[6]
        require(set(permutations) == {entities, entities[::-1]}, "missing fact permutation")
        details.append(order_quad(permutations[entities], permutations[entities[::-1]], key))
    reporting = defaultdict(list)
    for row in details:
        k = tuple(row[n] for n in ("seed", "arm", "condition", "split", "profile", "language"))
        reporting[k].append(row)
    report_keys = ("seed", "arm", "condition", "split", "profile", "language")
    measured = [dict(zip(report_keys, key, strict=True), **aggregate(rows)) for key, rows in sorted(reporting.items())]
    overall = [dict(arm=arm, condition=condition,
                    **aggregate([z for z in details if z["arm"] == arm and z["condition"] == condition]))
               for arm, condition in itertools.product(ARMS, CONDITIONS)]
    expected = {(r["arm"], r["condition"]): r for r in parent_summary["overall"]}
    require(len(expected) == len(overall) == 4, "parent group coverage")
    reconciliations = []
    for r in overall:
        old = expected[r["arm"], r["condition"]]
        require((r["answers"], r["correct"], r["query_pairs"], r["collapsed_orders"]) ==
                tuple(old[n] for n in ("answers", "correct", "pairs", "same_prediction")), "C322 aggregate reconciliation")
        reconciliations.append(dict(arm=r["arm"], condition=r["condition"], matched=True))
    require(len(details) == 4320 and len(measured) == 240 and sum(r["counterfactuals"] for r in measured) == 4320, "result inventory")
    summary = dict(diagnostic_complete=True, capability_gate_applicable=False, overall=overall,
                   reconciliations=reconciliations, **WORK)
    return details, measured, summary


def precheck(paths, root):
    validate_seal()
    p, parent, model, owner, x = context()
    evidence, data, pairs = load_parent(paths)
    root = Path(root).resolve()
    pins, inputs = dict(evidence["source_blobs"]), dict(evidence["input_sha256"])
    require((len(pins), len(inputs)) == (778, 1467) and pins.get(PARENT_SOURCE) == PARENT_BLOB, "parent source protection")
    for m in [p, parent, model, owner, *owner.context(), x.parent, *x.parent.context(), *x.p312.context(), *x.wide.context(),
              *vars(x.c).values(), x.c.factory.language_module()]:
        path = getattr(m, "__file__", None) if isinstance(m, ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            require(Path(path).resolve().relative_to(root).as_posix() in pins, "unprotected helper")
    for name, sha in pins.items():
        require(x.c.audit.git(root, "rev-parse", "HEAD:" + name).decode().strip() == sha, "source changed:" + name)
    for name, sha in inputs.items():
        require(Path(name).is_file() and x.c.audit.sha(name) == sha, "protected input changed:" + name)
    folder = Path(paths[0]).resolve().parent
    for path, sha in [(folder / "summary.json", PARENT_SHA)] + [(x.c.audit.safe_child(folder, a["file"]), a["sha256"]) for a in evidence["artifacts"]]:
        require(str(path.resolve()) not in inputs and x.c.audit.sha(path) == sha, "parent output integrity")
        inputs[str(path.resolve())] = sha
    for name in OWN:
        require(name not in pins, "OWN collision")
        pins[name] = x.c.audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
    inputs.update(x.c.audit.protect_tree_files(root, pins))
    require((len(pins), len(inputs)) == (784, 1478), "registration inventory")
    print(f"registration_check = source_pins:784; protected_inputs:1478; manifest_sha256:{MANIFEST_SHA}", flush=True)
    return pins, inputs, (evidence, data, pairs)


def validate_result(result):
    require(result["experiment_id"] == EXPERIMENT_ID and result["stage"] == STAGE
            and result["status"] == "PASS" and result["diagnostic_execution_valid"] is True
            and all(result[k] is False for k in ("capability_gate_applicable", "gate_f_candidate", "production_adoption")), "diagnostic identity")
    require((len(result["source_blobs"]), len(result["input_sha256"])) == (784, 1478)
            and set(OWN) <= set(result["source_blobs"]) and result["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "result protection")
    require(len(result["artifacts"]) == 4 and {a["file"] for a in result["artifacts"]} == set(OUTPUTS), "result outputs")
    s = result["validation_summary"]
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False
            and len(s["overall"]) == 4 and len(s["reconciliations"]) == 4
            and all(x["matched"] is True for x in s["reconciliations"])
            and all(type(s[k]) is int and s[k] == v for k, v in WORK.items()), "result summary")


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_modules(root):
    p = context()[0]
    names = p.regression_modules(root)
    require(len(names) == len(set(names)) == 207, "parent regression modules")
    return names + ["tests_lm.test_v05_c323_saved_fact_order_bias"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) == 5294 and ids.count(EXCLUDED) == 1, "loaded suite")
    return unittest.TestSuite(t for t in tests if t.id() != EXCLUDED)


def guard(root, head, owner, x):
    owner.context()[1].guard(root, head, x.c)


def runtime_preflight(paths, root):
    import torch
    torch.set_num_threads(2)
    _, _, loaded = precheck(paths, root)
    with context()[4].guarded.no_neural():
        analyze(loaded[1], loaded[2], loaded[0]["validation_summary"])
    print("saved_fact_order_reconciliation = PASS; new_model_forwards = 0", flush=True)


def run(*, summaries, output_dir, expected_head):
    import torch
    torch.set_num_threads(2)
    p, parent, model, owner, x = context()
    root = Path(__file__).resolve().parents[2]
    guard(root, expected_head, owner, x)
    pins, inputs, loaded = precheck(summaries, root)
    with x.guarded.no_neural():
        details, groups, summary = analyze(loaded[1], loaded[2], loaded[0]["validation_summary"])
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    for name, value in zip(OUTPUTS, (manifest(), details, groups, summary), strict=True):
        (out / name).write_bytes(blob(value))
    artifacts = [dict(file=name, sha256=x.c.audit.sha(out / name), serialized_bytes=(out / name).stat().st_size) for name in OUTPUTS]
    for name, sha in inputs.items():
        require(x.c.audit.sha(name) == sha, "input changed during diagnosis")
    guard(root, expected_head, owner, x)
    result = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head, status="PASS",
                  diagnostic_execution_valid=True, source_blobs=pins, input_sha256=inputs,
                  artifacts=artifacts, validation_summary=summary, capability_gate_applicable=False,
                  gate_f_candidate=False, production_adoption=False)
    validate_result(result)
    (out / "summary.json").write_bytes(blob(result))
    print("C323 saved fact-order bias diagnostic complete", flush=True)
    return result


def verify_artifacts(outdir, summaries, expected_head):
    import torch
    p, parent, model, owner, x = context()
    out = Path(outdir)
    result = x.c.audit.read_json(out / "summary.json")
    validate_result(result)
    require(result["commit_sha"] == expected_head, "execution HEAD")
    for name, sha in result["input_sha256"].items():
        require(x.c.audit.sha(name) == sha, "protected input")
    for descriptor in result["artifacts"]:
        path = x.c.audit.safe_child(out, descriptor["file"])
        require(x.c.audit.sha(path) == descriptor["sha256"] and path.stat().st_size == descriptor["serialized_bytes"], "output bytes")
    with x.guarded.no_neural():
        evidence, data, pairs = load_parent(summaries)
        details, groups, summary = analyze(data, pairs, evidence["validation_summary"])
        for name, value in zip(OUTPUTS, (manifest(), details, groups, summary), strict=True):
            require(x.c.audit.read_json(out / name) == value, "persisted:" + name)
    require(result["validation_summary"] == summary, "summary reconstruction")
    return result, groups


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summaries", nargs=49, type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
