"""C258: exploratory attribution of saved C257 answers; no model calls or training."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
import hashlib
import itertools
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import torch

EXPERIMENT_ID = "C258-v5b-saved-middle-slot-audit"
STAGE = "V5-B-SAVED-MIDDLE-SLOT-AUDIT"
BASE = "ff34341a10e12b00091649e29c05b088e29a09db"
PARENT_EXECUTION = "016785f35605a3eef5f94d42f0b86cb2fc4d9dfe"
PARENT_SHA = "596df75ccc89c5a12c964c2e6be1fc689e5773f4c0a857f90fdcedd4df9b8816"
PARENT_ARTIFACTS = {
    "eval-outputs.pt": "6911df9af7a10790cee9b18ff15a6b3479ca7e20046d5f6a16f95d69d068b92a",
    "measurements.json": "c37f98bbc13526f408b9b00adac16e90e23dc764d59ef4af1ef5e990b235eb22",
    "order-dataset.json": "9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052",
    "order-plan.json": "18fdc13e9c276826473467243017f30b1fa6dcf673a9a490e14318792f8a8e36",
    "validation-summary.json": "1d0d66a7550d47e34d01b5242c8ad0ef527ed7c36df66a440e31005609975d99",
}
SEEDS = (256001, 256002, 256003, 256004, 256005)
ARMS = ("aligned_precore_read", "eos_adapter")
SPLITS = ("TRAIN", "HOLDOUT")
KNOWN = ((0, 1, 2), (2, 1, 0))
NOVEL = ((0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1))
KINDS = ("correct", "other_entity", "absent_value", "other_byte")
OWN = ("fold_lm/v05_benchmarks/model_c258_saved_middle_slot_audit.py",
       "tests_lm/test_v05_c258_saved_middle_slot_audit.py", "tools/run_c258.ps1", "tools/invoke_c258.ps1",
       "docs/experiment-ledger-addendum-c258-preregistration.md", "docs/v5b-saved-middle-slot-audit-v0.1.md")
OUTPUTS = {"audit-plan.json", "row-attribution.json", "query-position-cells.json", "signature-summary.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "a4f2cad192bd56dd73d867caf8453084cdd85e8e0f10f9d2496bfaa4a6c08aef"


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
    from fold_lm.v05_benchmarks import model_c257_unseen_fact_order as parent
    previous, _, _, factory, audit = parent.context()
    return parent, previous, factory, audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        question="Does the saved novel-order error pattern concentrate on query b and the middle-slot distractor?",
        analysis="exploratory descriptive attribution after aggregate C257 scores; not independent or causal evidence",
        seeds=list(SEEDS), arms=list(ARMS), splits=list(SPLITS), known_orders=[list(x) for x in KNOWN],
        novel_orders=[list(x) for x in NOVEL], views_scored=["normal"], all_parent_views_replayed=True,
        records=10, known_rows=2880, novel_rows=5760, attributed_rows=8640,
        order_query_cells=720, query_cells=120, signature_cells=40, assignments_per_cell=12,
        model_forward_calls=0, model_state_loads=0, checkpoint_bundle_loads=0, new_training_steps=0,
        new_checkpoint_writes=0, eval_archive_loads_per_pass=1, formal_analysis_passes=2,
        primary="diagnostic integrity only; every valid signature direction is reportable; no capability gate",
        zero_denominator="JSON null, never zero or success", error_kinds=list(KINDS),
        source_pins=394, protected_inputs=647, direct_dependencies=34, own_tests=20,
        modules=143, loaded_tests=3358, focused_tests=3357, excluded_test=EXCLUDED,
        dtype="saved CPU float64 logits; integer attribution", threads=2,
        capability_pass_claim=False, causal_mechanism_claim=False, gate_f_candidate=False,
        production_adoption=False, network_calls=0)


@contextmanager
def no_model_calls():
    # Also guards accidentally introduced calls in reused parent helpers.
    with patch.object(torch.nn.Module, "_call_impl", side_effect=RuntimeError("C258 forbids model forward calls")):
        yield


def classify(assignment, query, permutation, prediction):
    require(len(assignment) == len(set(assignment)) == 3 and all(type(x) is int and 0 <= x <= 3 for x in assignment), "assignment")
    require(type(query) is int and query in (0, 1, 2) and tuple(permutation) in KNOWN + NOVEL, "query/permutation")
    require(type(prediction) is int and 0 <= prediction < 256, "prediction byte")
    value = prediction - 48
    entity = assignment.index(value) if value in assignment else None
    position = permutation.index(entity) if entity is not None else None
    kind = "correct" if entity == query else "other_entity" if entity is not None else "absent_value" if 0 <= value <= 3 else "other_byte"
    return dict(kind=kind, predicted_entity=entity, predicted_position=position,
                query_position=permutation.index(query), middle_wrong=(kind == "other_entity" and position == 1))


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def counts(rows):
    c = Counter(r["kind"] for r in rows)
    return dict(rows=len(rows), **{k: c[k] for k in KINDS},
                middle_wrong=sum(r["middle_wrong"] for r in rows))


def attribution(parts, novel, records, parent):
    require([(r["seed"], r["arm"]) for r in records] == identities(), "record identities")
    require(novel == parent.novel_dataset(parts), "dataset identity/order")
    rows = []
    for record in records:
        for split in SPLITS:
            known_lookup = defaultdict(list)
            for phase, source, stage in (("known", parts[split], "anchor"), ("novel", novel[split], "novel")):
                logits = record["outputs"][stage][split]["normal"]
                parent.check_logits(logits, len(source))
                predictions = logits.argmax(-1).tolist()
                for item, prediction in zip(source, predictions, strict=True):
                    permutation = KNOWN[item["order"]] if phase == "known" else tuple(item["permutation"])
                    assignment, query = list(item["assignment"]), item["query"]
                    require(item["target"] == 48 + assignment[query], "target semantics")
                    result = classify(assignment, query, permutation, prediction)
                    key = (item["language"], tuple(assignment), query)
                    if phase == "known":
                        known_lookup[key].append(result["kind"] == "correct")
                        baseline = None
                    else:
                        require(len(known_lookup[key]) == 2, "known pair missing")
                        baseline = all(known_lookup[key])
                    rows.append(dict(seed=record["seed"], arm=record["arm"], split=split, phase=phase,
                        language=item["language"], row_id=item["id"], assignment=assignment,
                        permutation=list(permutation), query=query, target=item["target"], prediction=prediction,
                        known_both_correct=baseline, **result))
    require(len(rows) == 8640 and Counter(r["phase"] for r in rows) == {"known": 2880, "novel": 5760}, "attribution coverage")
    order_groups, query_groups = defaultdict(list), defaultdict(list)
    for r in rows:
        key = (r["seed"], r["arm"], r["split"], r["language"])
        order_groups[key + (tuple(r["permutation"]), r["query"])].append(r)
        query_groups[key + (r["query"],)].append(r)
    require(len(order_groups) == 720 and all(len(v) == 12 for v in order_groups.values()), "order/query cells")
    cells = []
    for key, group in sorted(order_groups.items()):
        require(len({tuple(r["assignment"]) for r in group}) == 12, "duplicate assignment in cell")
        cells.append(dict(seed=key[0], arm=key[1], split=key[2], language=key[3], permutation=list(key[4]), query=key[5], **counts(group)))
    queries = []
    require(len(query_groups) == 120, "query cells")
    for key, group in sorted(query_groups.items()):
        old, new = ([r for r in group if r["phase"] == p] for p in ("known", "novel"))
        require((len(old), len(new)) == (24, 48), "query denominators")
        queries.append(dict(seed=key[0], arm=key[1], split=key[2], language=key[3], query=key[4],
            known=counts(old), novel=counts(new),
            known_both_correct_to_wrong=sum(r["known_both_correct"] and r["kind"] != "correct" for r in new),
            known_not_both_to_correct=sum(not r["known_both_correct"] and r["kind"] == "correct" for r in new)))
    by_query = {(r["seed"], r["arm"], r["split"], r["language"], r["query"]): r for r in queries}
    signatures = []
    for seed, arm in identities():
        for split in SPLITS:
            for language in ("en", "ja"):
                q = [by_query[(seed, arm, split, language, i)] for i in range(3)]
                b = q[1]["novel"]; b_errors = 48 - b["correct"]
                ac_errors = 96 - q[0]["novel"]["correct"] - q[2]["novel"]["correct"]
                middle, other = b["middle_wrong"], b["other_entity"] - b["middle_wrong"]
                signatures.append(dict(seed=seed, arm=arm, split=split, language=language,
                    b_known_correct=q[1]["known"]["correct"], b_known_rows=24, b_novel_correct=b["correct"], b_novel_rows=48,
                    b_error_rate=b_errors/48, ac_error_rate=ac_errors/96, b_minus_ac_error_rate=b_errors/48-ac_errors/96,
                    b_errors=b_errors, middle_distractor_errors=middle, other_distractor_errors=other,
                    absent_value_errors=b["absent_value"], other_byte_errors=b["other_byte"],
                    middle_share_of_b_errors=ratio(middle,b_errors), middle_share_of_in_assignment_b_errors=ratio(middle,middle+other),
                    middle_minus_other=middle-other, known_both_correct_to_wrong=q[1]["known_both_correct_to_wrong"]))
    require(len(signatures) == 40, "signature coverage")
    summary = dict(attributed_rows=len(rows), known_rows=2880, novel_rows=5760, order_query_cells=len(cells),
        query_cells=len(queries), signature_cells=len(signatures), models=10,
        model_forward_calls=0, model_state_loads=0, checkpoint_bundle_loads=0, new_training_steps=0,
        new_checkpoint_writes=0, eval_archive_loads_per_pass=1, capability_pass_claim=False, causal_mechanism_claim=False,
        totals=[dict(arm=a, split=s, phase=p, **counts([r for r in rows if (r["arm"],r["split"],r["phase"])==(a,s,p)]))
                for a in ARMS for s in SPLITS for p in ("known","novel")])
    return {"audit-plan.json":manifest(), "row-attribution.json":rows,
            "query-position-cells.json":dict(order_query=cells, query=queries),
            "signature-summary.json":signatures, "validation-summary.json":summary}


def validate_parent(payload, parent):
    parent.validate_result(payload)
    require(payload["commit_sha"] == PARENT_EXECUTION and payload["status"] == "FAIL", "accepted C257 identity/status")
    require(payload["validation_summary"]["seed_pass_counts"] == {ARMS[0]:2, ARMS[1]:0}, "accepted C257 counts")
    require({a["file"]:a["sha256"] for a in payload["artifacts"]} == PARENT_ARTIFACTS, "parent artifact contract")


def load_saved(c257_summary, c256_summary):
    parent, previous, _, audit = context(); path = Path(c257_summary).resolve()
    require(audit.sha(path) == PARENT_SHA, "parent summary hash")
    payload = audit.read_json(path); validate_parent(payload, parent)
    for item in payload["artifacts"]:
        child = audit.safe_child(path.parent, item["file"])
        require(audit.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "parent artifact bytes")
    parts, refs = parent.load_inputs(Path(c256_summary))
    novel = audit.read_json(path.parent / "order-dataset.json")
    archive = torch.load(path.parent / "eval-outputs.pt", map_location="cpu", weights_only=True)
    require(set(archive) == {"schema","records"} and archive["schema"] == "fold-c257-order-eval-v1", "archive schema")
    measurements, summary = parent.analyze(parts, novel, archive["records"], refs, previous)
    require(summary == payload["validation_summary"] == audit.read_json(path.parent / "validation-summary.json"), "parent summary replay")
    require(measurements == audit.read_json(path.parent / "measurements.json") and parent.manifest() == audit.read_json(path.parent / "order-plan.json"), "parent persisted replay")
    return parts, novel, archive["records"]


def validate_registration(source_count, input_count):
    actual = digest(manifest())
    print(f"registration_check = source_pins:{source_count}; protected_inputs:{input_count}; manifest_sha256:{actual}", flush=True)
    require((source_count,input_count) == (394,647), f"source/input counts: expected=(394, 647) actual=({source_count}, {input_count})")
    require(actual == MANIFEST_SHA, f"manifest hash: expected={MANIFEST_SHA} actual={actual}")


def precheck(c257_summary, root):
    parent, _, factory, audit = context(); path = Path(c257_summary).resolve(); root = Path(root)
    require(audit.sha(path) == PARENT_SHA, "parent summary hash")
    payload = audit.read_json(path); validate_parent(payload,parent)
    pins, protected = dict(payload["source_blobs"]), dict(payload["input_sha256"])
    for name,wanted in protected.items():
        require(Path(name).is_file() and audit.sha(name) == wanted, "changed input:"+name)
    for name,wanted in pins.items():
        require(audit.git(root,"rev-parse","HEAD:"+name).decode().strip() == wanted, "changed source:"+name)
    require(str(path) not in protected, "parent duplicate"); protected[str(path)] = PARENT_SHA
    for item in payload["artifacts"]:
        child = audit.safe_child(path.parent,item["file"])
        require(audit.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "artifact bytes")
        require(str(child.resolve()) not in protected, "artifact duplicate"); protected[str(child.resolve())] = item["sha256"]
    for name in OWN:
        require(name not in pins, "OWN collision"); pins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-7])_[^/]+)\.py"
    deps = set(factory.LM_SOURCES) | {n for n in payload["source_blobs"] if re.fullmatch(pattern,n)} | {OWN[0]}
    require(len(deps) == 34 and deps <= set(pins), "direct dependency coverage")
    protected.update(audit.protect_tree_files(root,pins)); validate_registration(len(pins),len(protected))
    return pins, protected


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == 142, "parent modules")
    return names + ["tests_lm.test_v05_c258_saved_middle_slot_audit"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]; require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1, "test IDs")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require((len(tests),len(kept)) == (3358,3357), "suite counts")
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(payload["experiment_id"] == EXPERIMENT_ID and payload["stage"] == STAGE and payload["status"] == "PASS"
            and payload["diagnostic_execution_valid"] is True, "diagnostic identity")
    require((len(payload["source_blobs"]),len(payload["input_sha256"])) == (394,647) and set(OWN) <= set(payload["source_blobs"]), "protection")
    require(len(payload["artifacts"]) == 5 and {a["file"] for a in payload["artifacts"]} == OUTPUTS, "outputs")
    expected = dict(attributed_rows=8640,known_rows=2880,novel_rows=5760,order_query_cells=720,query_cells=120,signature_cells=40,models=10,
        model_forward_calls=0,model_state_loads=0,checkpoint_bundle_loads=0,new_training_steps=0,new_checkpoint_writes=0,eval_archive_loads_per_pass=1)
    for key,value in expected.items():
        require(type(payload["validation_summary"][key]) is int and payload["validation_summary"][key] == value,"workload:"+key)
    for key in ("capability_pass_claim","causal_mechanism_claim","gate_f_candidate","production_adoption"):
        require(payload[key] is False,"non-claim:"+key)
    require(payload["network_calls"] == 0,"network")


def run(*,c257_summary,c256_summary,output_dir,expected_head):
    parent, _, _, audit = context(); root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip() == expected_head,"HEAD")
        require(audit.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss","branch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard(); torch.set_num_threads(2)
    pins,protected = precheck(c257_summary,root)
    with no_model_calls():
        parts,novel,records = load_saved(c257_summary,c256_summary)
        values = attribution(parts,novel,records,parent)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    for name,value in values.items():
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard(); precheck(c257_summary,root)
    for name,wanted in protected.items():
        require(audit.sha(name) == wanted,"modified input")
    payload = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=values["validation-summary.json"],
        capability_pass_claim=False,causal_mechanism_claim=False,gate_f_candidate=False,production_adoption=False,network_calls=0)
    validate_result(payload); (out/"summary.json").write_bytes(blob(payload))
    print("=== C258 RESULT; DIAGNOSTIC INTEGRITY ONLY ===",flush=True); print(blob(payload).decode(),flush=True)
    return payload


def verify_artifacts(output_dir,c257_summary,c256_summary,expected_head):
    parent, _, _, audit = context(); out = Path(output_dir); payload = audit.read_json(out/"summary.json")
    validate_result(payload); require(payload["commit_sha"] == expected_head,"saved HEAD")
    for name,wanted in payload["input_sha256"].items():
        require(audit.sha(name) == wanted,"postcheck input")
    for item in payload["artifacts"]:
        child = audit.safe_child(out,item["file"])
        require(audit.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"],"output bytes")
    with no_model_calls():
        parts,novel,records = load_saved(c257_summary,c256_summary)
        values = attribution(parts,novel,records,parent)
    for name,value in values.items():
        require((out/name).read_bytes() == blob(value),"persisted attribution:"+name)
    require(payload["validation_summary"] == values["validation-summary.json"],"saved summary replay")
    return payload,values["signature-summary.json"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("c257-summary","c256-summary","output-dir"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
