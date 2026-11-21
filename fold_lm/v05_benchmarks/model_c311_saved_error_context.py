"""C311: classify saved C310 errors by ordered value pair and length-persistent identity."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
from types import ModuleType
import unittest

EXPERIMENT_ID = "C311-v5b-saved-error-context"
STAGE = "V5-B-SAVED-ERROR-CONTEXT"
BASE = "0738f8e1c0be9aeecacea450abab806c9f5403a2"
PARENT_EXECUTION = "bdbf7c4c410ceb9d621ae5d3ecf86e764061550b"
PARENT_SHA = "eec24c37d318d0634623185193b50a4a7e4fb82abd6abe350a4712f807d59961"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c310_value_renaming_audit.py"
PARENT_BLOB = "2f581ca13bdcc5dc0cd7a87f15eea6782af367a9"
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
SEEDS = tuple(range(309001, 309006))
ARMS = ("full_train", "core_frozen", "core_slow")
LENGTHS = (2, 3, 4, 5)
PROFILES = ("repeat", "shared_prefix", "shared_suffix")
SPLITS = ("TRAIN", "HOLDOUT")
PAIRS = tuple((a, b) for a in range(4) for b in range(4) if a != b)
ERRORS = ("other_fact", "unmentioned_digit", "non_digit")
OWN = ("fold_lm/v05_benchmarks/model_c311_saved_error_context.py",
       "tests_lm/test_v05_c311_saved_error_context.py", "tools/run_c311.ps1", "tools/invoke_c311.ps1",
       "docs/experiment-ledger-addendum-c311-preregistration.md", "docs/v5b-saved-error-context-v0.1.md")
OUTPUTS = ("audit-plan.json", "error-context-report.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
ZERO = dict(model_forward_calls=0, train_steps=0, model_state_loads=0,
            new_checkpoint_writes=0, row_presentations=0, core_forward_calls=0, network_calls=0)
MANIFEST_SHA = "b9e5f42cf681031892d77f2f134bc307d56233f22e039cac13009b3cd90b34fd"


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
    from fold_lm.v05_benchmarks import model_c310_value_renaming_audit as parent
    return parent, parent.context()[-1]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_source=PARENT_SOURCE,
        parent_blob=PARENT_BLOB, dataset_sha256=DATA_SHA,
        question="are C309 HOLDOUT failures concentrated on specific ordered value pairs and persistent from trained lengths into unseen five",
        seeds=list(SEEDS), arms=list(ARMS), lengths=list(LENGTHS), profiles=list(PROFILES),
        original_splits=list(SPLITS), ordered_value_pairs=[list(x) for x in PAIRS],
        error_classes=list(ERRORS), primary_focus="309002 HOLDOUT; all15 original arms/seeds retained as controls",
        source="strictly verified C310 saved full-256 argmax predictions, original C309 logical data; no new outputs",
        score="separate correct, other-fact, unmentioned digit, non-digit; no repairs or restricted decoding",
        length_identity="same seed,arm,profile,source row across 2/3/4/5; signature bits and 4-to-5 transitions",
        interpretation="descriptive within fixed original splits, not new seeds/trials or causal mechanisms",
        observations=51840, pair_groups=2160, language_groups=720, signature_groups=90,
        persisted_prediction_blocks=60, parent_original_totals=720,
        diagnostic_gate="exact parent C310 reconstruction + every row categorized + per-pair and persistence conservation",
        parents=37, source_pins=712, protected_inputs=1333, own_tests=24,
        modules=196, loaded_tests=4966, focused_tests=4965, excluded_test=EXCLUDED,
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False, **ZERO)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None and digest(manifest()) == MANIFEST_SHA, "manifest seal")


def describe_answer(row, prediction):
    """Correctness is independent of relabeling equivariance and model-side gate flags."""
    require(type(prediction) is int and 0 <= prediction < 256, "prediction domain")
    target = row["target"]
    require(type(target) is int and target in range(48, 52), "target domain")
    entities, values, query = row["entities"], row["values"], row["query"]
    require(len(entities) == len(values) == 2 and sorted(entities) == sorted(set(entities))
            and len(set(values)) == 2 and query in entities, "logical row")
    other = 48+values[1-entities.index(query)]
    if prediction == target:
        return "correct"
    if prediction == other:
        return "other_fact"
    if 48 <= prediction <= 51:
        return "unmentioned_digit"
    return "non_digit"


def count_group(labels):
    counts = dict(rows=0, correct=0, other_fact=0, unmentioned_digit=0, non_digit=0)
    for value in labels:
        require(value in counts and value != "rows", "answer class")
        counts[value] += 1
        counts["rows"] += 1
    require(sum(counts[k] for k in ("correct", *ERRORS)) == counts["rows"], "error partition")
    return counts


def analyze(parent_payload, source_data):
    require(type(parent_payload) is dict and set(parent_payload) ==
            {"row_ids", "permutations", "destination_indices", "predictions", "original_totals", "summary"}, "parent report schema")
    require(set(source_data) == set(SPLITS) and [len(source_data[s]) for s in SPLITS] == [192, 96], "split domain")
    rows = source_data["TRAIN"]+source_data["HOLDOUT"]
    require(parent_payload["row_ids"] == [r["id"] for r in rows] and len(set(parent_payload["row_ids"])) == 288, "original row order")
    require(len(parent_payload["permutations"]) == 24 and len(parent_payload["destination_indices"]) == 24, "parent bijection inventory")
    require(len(parent_payload["original_totals"]) == 720 and parent_payload["summary"]["diagnostic_complete"] is True
            and parent_payload["summary"]["observations"] == 51840, "original parent diagnostic")
    pred_blocks = parent_payload["predictions"]
    expected = [(seed, arm, n) for seed, arm in identities() for n in LENGTHS]
    require([(b["seed"], b["arm"], b["identifier_length"]) for b in pred_blocks] == expected, "all60 model-length blocks")
    pair_groups, language_groups, signature_groups = [], [], []
    fixed = {(r["split"], r["profile"], r["language"], r["seed"], r["arm"], r["identifier_length"]): r
             for r in parent_payload["original_totals"]}
    require(len(fixed) == 720, "unique originals")
    labels_by_model = {}
    for block in pred_blocks:
        seed, arm, n = block["seed"], block["arm"], block["identifier_length"]
        require(set(block["predictions"]) == set(PROFILES) and set(block["tied_max_indices"]) == set(PROFILES), "profile domain")
        for profile in PROFILES:
            predictions = block["predictions"][profile]
            require(type(predictions) is list and len(predictions) == 288, "prediction count")
            ties = block["tied_max_indices"][profile]
            require(type(ties) is list and ties == sorted(set(ties)) and all(type(i) is int and 0 <= i < 288 for i in ties), "tie indices")
            classifications = [describe_answer(row, prediction) for row, prediction in zip(rows, predictions, strict=True)]
            labels_by_model[seed, arm, n, profile] = classifications
            for pair in PAIRS:
                indices = [i for i, row in enumerate(rows) if tuple(row["values"]) == pair]
                require(len(indices) == 24 and len({rows[i]["id"] for i in indices}) == 24, "value pair cardinality")
                split = "HOLDOUT" if (pair[1]-pair[0])%4 == 2 else "TRAIN"
                require(all((i >= 192) == (split == "HOLDOUT") for i in indices), "original split of pair")
                c = count_group(classifications[i] for i in indices)
                pair_groups.append(dict(seed=seed, arm=arm, identifier_length=n, profile=profile,
                                        values=list(pair), split=split, **c))
            for split in SPLITS:
                selected = range(192) if split == "TRAIN" else range(192, 288)
                for lang in ("en", "ja"):
                    indices = [i for i in selected if rows[i]["language"] == lang]
                    c = count_group(classifications[i] for i in indices)
                    previous = fixed[split, profile, lang, seed, arm, n]
                    require(c["rows"] == previous["rows"] and c["correct"] == previous["correct"], "original totals score")
                    language_groups.append(dict(seed=seed, arm=arm, identifier_length=n, profile=profile,
                                                split=split, language=lang, **c))
    for seed, arm in identities():
        for profile, split in itertools.product(PROFILES, SPLITS):
            indices = range(192) if split == "TRAIN" else range(192, 288)
            patterns = {format(i,"04b"): 0 for i in range(16)}
            transition = dict(both_correct=0, four_only_correct=0, five_only_correct=0, both_wrong=0)
            for i in indices:
                checks = [labels_by_model[seed,arm,n,profile][i] == "correct" for n in LENGTHS]
                bits = "".join("1" if k else "0" for k in checks)
                patterns[bits] += 1
                if checks[2] and checks[3]: transition["both_correct"] += 1
                elif checks[2]: transition["four_only_correct"] += 1
                elif checks[3]: transition["five_only_correct"] += 1
                else: transition["both_wrong"] += 1
            require(sum(patterns.values()) == len(indices) == sum(transition.values()), "signature conservation")
            signature_groups.append(dict(seed=seed, arm=arm, profile=profile, split=split,
                                         rows=len(indices), patterns=patterns, four_to_five=transition))
    require((len(pair_groups), len(language_groups), len(signature_groups)) == (2160, 720, 90), "group inventory")
    require(sum(x["rows"] for x in pair_groups) == 51840 and sum(x["rows"] for x in language_groups) == 51840, "row conservation")
    require(all(sum(x[k] for k in ("correct", *ERRORS)) == x["rows"] for x in pair_groups+language_groups), "value conservation")
    report = dict(parent_summary_sha256=PARENT_SHA, pairs=pair_groups, language_splits=language_groups,
                  length_signatures=signature_groups, focus_seed=309002,
                  original_report_digest=digest(parent_payload), source_row_count=288)
    summary = dict(diagnostic_complete=True, observations=51840, pair_groups=2160, language_groups=720,
                   signature_groups=90, parent_original_totals=720,
                   paired_value_questions=24, parent_report_digest=report["original_report_digest"],
                   capability_gate_applicable=False, **ZERO)
    return report, summary


def parent_hashes(parent):
    p309 = parent.context()[0]
    return (PARENT_SHA, parent.PARENT_SHA, *p309.parent_hashes(p309.context()[0]))


def load_parent(paths):
    parent, c = context(); paths = [Path(p).resolve() for p in paths]
    hashes = parent_hashes(parent)
    require(len(paths) == len(hashes) == 37 and all(c.audit.sha(p) == h for p,h in zip(paths, hashes, strict=True)), "37 parent hashes")
    with parent.no_neural():
        p, report = parent.verify_artifacts(paths[0].parent, paths[1:], PARENT_EXECUTION)
        parent.validate_result(p)
        require(p["experiment_id"] == "C310-v5b-saved-value-renaming" and p["status"] == "PASS"
                and p["commit_sha"] == PARENT_EXECUTION and p["diagnostic_execution_valid"] is True
                and p["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "parent identity")
        require(len(p["artifacts"]) == 3 and {a["file"] for a in p["artifacts"]} == set(parent.OUTPUTS)
                and p["validation_summary"]["capability_gate_applicable"] is False, "parent diagnostic scope")
        path = paths[1].parent/"dataset.json"
        data = c.audit.read_json(path)
        c.p267.validate_data(data)
        require(parent.digest(data) == DATA_SHA, "data hash")
    return p, report, data


def precheck(paths, root):
    validate_seal()
    p, _, _ = load_parent(paths)
    parent, c = context(); root = Path(root).resolve()
    pins, protected = dict(p["source_blobs"]), dict(p["input_sha256"])
    require((len(pins),len(protected)) == (706,1323) and pins.get(PARENT_SOURCE) == PARENT_BLOB, "inherited protection")
    for m in [parent, *parent.context(), *parent.context()[0].context(), *vars(c).values(), c.factory.language_module()]:
        path = getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            require(Path(path).resolve().relative_to(root).as_posix() in pins,"unprotected helper")
    for n,h in pins.items():
        require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip() == h,"changed source:"+n)
    for n,h in protected.items():
        require(Path(n).is_file() and c.audit.sha(n) == h,"changed input:"+n)
    folder = paths[0].resolve().parent
    for path,h in [(folder/"summary.json",PARENT_SHA)]+[(c.audit.safe_child(folder,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path) == h,"parent input")
        protected[str(path.resolve())] = h
    for n in OWN:
        require(n not in pins,"OWN collision")
        pins[n] = c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected)) == (712,1333),"protection counts")
    print(f"registration_check = source_pins:712; protected_inputs:1333; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def runtime_preflight(paths, root):
    precheck(paths, root)
    parent, _ = context()
    with parent.no_neural():
        _, old, data = load_parent(paths)
        _, summary = analyze(old, data)
    require(summary["observations"] == 51840, "real saved diagnostic")
    print("real_saved_error_pair_and_length_audit = PASS; no new inference",flush=True)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["status"] == "PASS"
            and p["diagnostic_execution_valid"] is True and all(p[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")), "result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"])) == (712,1333)
            and set(OWN) <= set(p["source_blobs"]) and p["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB,"source pins")
    require(len(p["artifacts"]) == 3 and {a["file"] for a in p["artifacts"]} == set(OUTPUTS), "result outputs")
    s = p["validation_summary"]
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False
            and all(type(s[k]) is int and s[k] == v for k,v in ZERO.items()), "zero work")
    require(all(s[k] == n for k,n in (("observations",51840),("pair_groups",2160),("language_groups",720),("signature_groups",90),("parent_original_totals",720)))
            and re.fullmatch(r"[0-9a-f]{64}",s["parent_report_digest"]) is not None,"summary inventory")


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == 195,"parent module inventory")
    return names+["tests_lm.test_v05_c311_saved_error_context"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) == 4966 and ids.count(EXCLUDED) == 1,"loaded suite")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require(len(kept) == 4965,"focused suite")
    return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip() == head
            and c.audit.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    parent,c = context()
    root = Path(__file__).resolve().parents[2]
    guard(root,expected_head,c)
    pins,protected = precheck(summaries,root)
    with parent.no_neural():
        _,old,data = load_parent(summaries)
        report,summary = analyze(old,data)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    for n,v in zip(OUTPUTS,(manifest(),report,summary),strict=True): (out/n).write_bytes(blob(v))
    artifacts = [dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c); precheck(summaries,root)
    p = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
             source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
             capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    receipt = {k:p[k] for k in ("experiment_id","stage","commit_sha","status","artifacts")}
    receipt["summary_sha256"] = c.audit.sha(out/"summary.json")
    print("=== C311 COMPACT DIAGNOSTIC RECEIPT ===",flush=True)
    print(json.dumps(receipt,indent=2,sort_keys=True),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    parent,c = context(); out = Path(outdir); p = c.audit.read_json(out/"summary.json")
    validate_result(p); require(p["commit_sha"] == expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items(): require(c.audit.sha(n) == h,"protected input")
    for a in p["artifacts"]:
        path = c.audit.safe_child(out,a["file"])
        require(c.audit.sha(path) == a["sha256"] and path.stat().st_size == a["serialized_bytes"],"output bytes")
    with parent.no_neural():
        _,old,data = load_parent(summaries)
        report,summary = analyze(old,data)
    for n,v in zip(OUTPUTS,(manifest(),report,summary),strict=True): require(c.audit.read_json(out/n) == v,"persisted:"+n)
    require(p["validation_summary"] == summary,"summary reconstruction")
    return p,report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summaries",nargs=37,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__": main()
