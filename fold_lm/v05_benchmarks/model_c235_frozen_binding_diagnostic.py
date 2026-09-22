"""C235: frozen TRAIN/EVAL binding diagnostic; no training or C234 verdict change."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import unittest
import torch

EXPERIMENT_ID = "C235-v5b-frozen-binding-diagnostic"
STAGE = "V5-B-FROZEN-BINDING-DIAGNOSTIC"
BASE = "8a58594d7fb4523ab2f5ef172d16cf7cafb7f4d1"
PARENT_EXECUTION = "c225c2d82636085e2d639878738e1b9a7aa37b42"
PARENT_SHA = "a38b583d986cdf313bcf135307bb290160fea791848d9bf4c16b5453fd79f523"
PARENT_ARTIFACTS = {
    "binding-plan.json": "0c3c3cedd0a15fa8b392cbe38ba5285113a948b78ef3511bf106cbc75d7b2d38",
    "dataset.json": "72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85",
    "measurements.json": "23f822d0a05faac176efc767b5702a21763946b295a76c503f01abc965c776c3",
    "trained-models.pt": "711dd636597d5ec575136bd780ac303eb21ed6198d411f977bb20c67fd20bd26",
    "validation-summary.json": "655dc04bd3509246c432eb8817699b5685ca300df612515d55358d78e634b629",
}
SEEDS, FAMILIES = (234001, 234002, 234003), ("full", "gru_only")
VIEWS = ("normal", "evidence_blind", "query_blind")
TOL = 1e-9
MANIFEST_SHA = "2e8bb701b3a6d512479c7118ac0973784617e1243639ef00c3903caed1a0f6c3"
OWN = (
    "fold_lm/v05_benchmarks/model_c235_frozen_binding_diagnostic.py",
    "tests_lm/test_v05_c235_frozen_binding_diagnostic.py",
    "tools/run_c235.ps1", "tools/invoke_c235.ps1",
    "docs/experiment-ledger-addendum-c235-preregistration.md",
    "docs/v5b-frozen-binding-diagnostic-v0.1.md",
)
OUTPUTS = {"diagnostic-plan.json", "diagnostics.json", "predictions.json",
           "model-fingerprints.json", "validation-summary.json"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c234_context_binding as parent
    return parent


def identities():
    return list(itertools.product(SEEDS, FAMILIES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
        parent_artifacts=PARENT_ARTIFACTS, identities=[list(x) for x in identities()],
        views=list(VIEWS), train_rows=384, eval_rows=192, models=6,
        model_forward_calls=36, evaluated_rows_including_masks=10368,
        exact_eval_predictions=3456, new_training_steps=0,
        diagnosis="accuracy-only descriptive split at existing 0.90 criterion; not a new ability gate",
        measurements=["TRAIN/EVAL parent metrics", "supplied-value rate", "mean supplied-value probability mass",
                      "query-pair unchanged answer", "query-pair both correct", "first/last fact agreement"],
        replay_metric_tolerance=TOL, dtype="float64", device="cpu", threads=2,
        deterministic_algorithms=True, checkpoint_writes=0,
        gate_scope="diagnostic integrity only, independent of accuracy or attribution outcome",
        changes="evaluate saved step400 models on complete TRAIN as well as EVAL",
        general_language_claim=False, gate_f_candidate=False)


def validate_parent_records(rows):
    require(isinstance(rows, list) and [(r["seed"], r["family"]) for r in rows] == identities(),
            "parent record order")
    for r in rows:
        require(r["checkpoint_roundtrip"] is True and r["prediction_replayed"] is True
                and r["weights_changed"] is True and 0 <= r["reload_max_error"] <= TOL,
                "parent execution checks")
        require((r["fit"]["steps"], r["fit"]["answer_presentations"]) == (400, 12800),
                "parent workload")
        require(isinstance(r["final_sha256"], str) and len(r["final_sha256"]) == 64
                and all(c in "0123456789abcdef" for c in r["final_sha256"]), "fingerprint")
        require(set(r["predictions"]) == set(VIEWS), "parent prediction views")
        for values in r["predictions"].values():
            require(len(values) == 192 and all(type(v) is int and 0 <= v < 256 for v in values),
                    "parent byte predictions")
        validate_metrics(r["final_eval"], 96)
    return rows


def validate_metrics(metrics, count):
    require(set(metrics) == {"en", "ja"}, "language groups")
    rates = ("accuracy", "evidence_blind_accuracy", "query_blind_accuracy",
             "fact_pair_accuracy", "query_pair_accuracy")
    for m in metrics.values():
        require(m["rows"] == count, "language row count")
        for key in (*rates, "answer_nll", "evidence_drop", "query_drop"):
            require(type(m[key]) in (int, float) and math.isfinite(m[key]), "nonfinite metric")
        require(all(0 <= m[k] <= 1 for k in rates) and m["answer_nll"] >= 0, "metric range")
        require(abs(m["evidence_drop"] - (m["accuracy"]-m["evidence_blind_accuracy"])) <= TOL
                and abs(m["query_drop"] - (m["accuracy"]-m["query_blind_accuracy"])) <= TOL,
                "control drop semantics")


def load_bundle(path):
    bundle = torch.load(path, map_location="cpu", weights_only=True)
    require(bundle["schema"] == "fold-c234-binding-v1"
            and bundle["identities"] == [list(x) for x in identities()]
            and len(bundle["states"]) == 6, "C234 checkpoint schema/order")
    return bundle["states"]


def replay_error(metrics, predictions, saved):
    validate_metrics(metrics, 96)
    require(set(predictions) == set(VIEWS) and predictions == saved["predictions"],
            "parent EVAL argmax replay mismatch")
    error = max(abs(metrics[lang][key]-saved["final_eval"][lang][key])
                for lang in ("en", "ja") for key in saved["final_eval"][lang])
    require(error <= TOL, "parent EVAL metric replay mismatch")
    return error


def analyze(rows, predictions, logits):
    """Post-inference scorer only; query/target metadata never enters the model here."""
    require(len(rows) == len(predictions) > 0 and logits.shape == (len(rows), 256)
            and bool(torch.isfinite(logits).all()), "diagnostic inputs")
    require(all(type(v) is int and 0 <= v < 256 for v in predictions), "predicted byte IDs")
    require(logits.argmax(-1).tolist() == predictions, "logits/predictions mismatch")
    probs = logits.softmax(-1); result = {}
    for lang in ("en", "ja"):
        ids = [i for i,r in enumerate(rows) if r["language"] == lang]
        require(ids, "missing diagnostic language")
        groups = defaultdict(list); correct = offered = first = last = 0; mass = 0.0
        for i in ids:
            r, pred = rows[i], predictions[i]
            values = [48+v for v in r["values"]]
            require(len(values) == 2 and values[0] != values[1], "two distinct values required")
            require(r["target"] in values and r["query"] in r["objects"], "target/query schema")
            correct += pred == r["target"]; offered += pred in values
            first += pred == values[r["order"]]; last += pred == values[1-r["order"]]
            mass += float(probs[i, values].sum())
            groups[(r["group"], r["order"])].append((r["query"], r["target"], pred))
        require(all(len(g)==2 and g[0][0]!=g[1][0] and g[0][1]!=g[1][1]
                    for g in groups.values()), "query-pair structure")
        same = sum(g[0][2] == g[1][2] for g in groups.values())
        both = sum(all(t == p for _,t,p in g) for g in groups.values())
        require(first+last == offered and correct <= offered and both+same <= len(groups),
                "diagnostic accounting")
        result[lang] = dict(rows=len(ids), correct=correct, supplied_value_answers=offered,
            supplied_value_rate=offered/len(ids), mean_supplied_value_mass=mass/len(ids),
            first_fact_agreement=first/len(ids), last_fact_agreement=last/len(ids),
            query_pairs=len(groups), query_same_answer_pairs=same,
            query_same_answer_rate=same/len(groups), query_both_correct_pairs=both)
    return result


def classify(train_accuracy, eval_accuracy):
    require(all(type(v) in (int,float) and math.isfinite(v) and 0 <= v <= 1
                for v in (train_accuracy, eval_accuracy)), "classification rates")
    if train_accuracy < 0.90:
        return "TRAIN_ACCURACY_BELOW_90"
    return "TRAIN_AT_LEAST_90_EVAL_BELOW_90" if eval_accuracy < 0.90 else "BOTH_ACCURACIES_AT_LEAST_90"


def summarize(records):
    require([(r["seed"],r["family"]) for r in records] == identities(), "diagnostic record order")
    counts = Counter(v for r in records for v in r["diagnosis"].values())
    return dict(models=len(records), all_parent_replays=all(r["parent_replay_error"] <= TOL for r in records),
        all_fingerprints_unchanged=all(r["before_sha256"] == r["after_sha256"] for r in records),
        model_forward_calls=sum(r["forward_calls"] for r in records),
        evaluated_rows_including_masks=sum(r["evaluated_rows"] for r in records),
        diagnosis_counts=dict(counts), diagnosis_cells=sum(counts.values()),
        new_training_steps=0, capability_pass_claim=False)


def gate(s):
    return (s.get("models") == 6 and s.get("all_parent_replays") is True
        and s.get("all_fingerprints_unchanged") is True and s.get("model_forward_calls") == 36
        and s.get("evaluated_rows_including_masks") == 10368 and s.get("diagnosis_cells") == 12
        and s.get("new_training_steps") == 0 and s.get("capability_pass_claim") is False)


def precheck(c234_summary, root):
    pmod=parent_module(); a=pmod.parent_module().parent_module().audit_module(); root=Path(root)
    require(a.sha(c234_summary)==PARENT_SHA, "C234 summary identity")
    p=a.read_json(c234_summary); pmod.validate_result(p); s=p["validation_summary"]
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL"
            and s["full_binding_gate"] is False and s["gru_binding_gate"] is False
            and s["all_replays"] is True, "wrong accepted C234 negative")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    require((len(pins),len(protected))==(250,358), "parent protection")
    for path,sha in protected.items(): require(Path(path).is_file() and a.sha(path)==sha,"changed input:"+path)
    for path,sha in pins.items(): require(a.git(root,"rev-parse","HEAD:"+path).decode().strip()==sha,"changed source:"+path)
    protected[str(Path(c234_summary).resolve())]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS, "parent artifact identities")
    for item in p["artifacts"]:
        path=a.safe_child(Path(c234_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path)==item["sha256"] and path.stat().st_size==item["serialized_bytes"],"parent artifact bytes")
        protected[str(path.resolve())]=item["sha256"]
    for path in OWN:
        require(path not in pins,"OWN collision"); pins[path]=a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    deps=set(pmod.factory_module().LM_SOURCES)|{OWN[0],
        "fold_lm/v05_benchmarks/model_c234_context_binding.py",
        "fold_lm/v05_benchmarks/model_c233_core_ablation.py",
        "fold_lm/v05_benchmarks/model_c232_bilingual_learning.py",
        "fold_lm/v05_benchmarks/model_c231_byte_eval_contract.py",
        "fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"}
    require(len(deps)==11 and deps<=set(pins),"direct dependency protection")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(256,370),"C235 protection counts")
    require(digest(manifest())==MANIFEST_SHA,"manifest drift")
    return p,pins,protected


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==119,"parent modules")
    return names+["tests_lm.test_v05_c235_frozen_binding_diagnostic"]


def regression_suite(root):
    p=parent_module().factory_module().parent_module(); helper=p.context(p.parent_module()).backend.c205
    tests=list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests]; excluded=helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
    require(all(ids.count(x)==1 for x in excluded),"historical exclusion")
    kept=[t for t in tests if t.id() not in excluded]
    require((len(tests),len(kept))==(2810,2809),"C235 regression counts")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(256,370) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"output coverage")
    require(gate(p["validation_summary"]) and p["status"]=="PASS", "incomplete diagnostic integrity")
    require(p["gate_f_candidate"] is False and p["network_calls"]==0,"scope")


def run(*, c234_summary, output_dir, expected_head):
    pmod=parent_module(); factory=pmod.factory_module(); a=pmod.parent_module().parent_module().audit_module()
    root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    parent,pins,protected=precheck(c234_summary,root); directory=Path(c234_summary).resolve().parent
    saved=validate_parent_records(a.read_json(directory/"measurements.json"))
    require(pmod.summarize(saved)==parent["validation_summary"],"parent summary/records mismatch")
    states=load_bundle(directory/"trained-models.pt")
    train,ev=pmod.validate_dataset(a.read_json(directory/"dataset.json"))
    parts={"TRAIN":train,"EVAL":ev}
    views={key:[pmod.tensors(rows,mode) for mode in VIEWS] for key,rows in parts.items()}
    reports=[]; prediction_records=[]; fingerprints=[]
    for saved_row,state in zip(saved,states,strict=True):
        seed,family=saved_row["seed"],saved_row["family"]
        model=factory.new_model(seed)
        if family=="gru_only": model=pmod.parent_module().new_baseline(model)
        model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(False)
        before=factory.fingerprint(model)
        require(before==saved_row["final_sha256"],"saved model fingerprint mismatch")
        calls=[0,0]
        def hook(module,args,output): calls[0]+=1; calls[1]+=len(args[0])
        handle=model.register_forward_hook(hook); scores={}; extra={}; preds={}
        try:
            for key,rows in parts.items():
                scores[key],logits=pmod.evaluate(model,rows,views[key])
                validate_metrics(scores[key],len(rows)//2)
                preds[key]={mode:value.argmax(-1).tolist() for mode,value in zip(VIEWS,logits,strict=True)}
                extra[key]=analyze(rows,preds[key]["normal"],logits[0])
        finally: handle.remove()
        error=replay_error(scores["EVAL"],preds["EVAL"],saved_row)
        after=factory.fingerprint(model); require(before==after,"evaluation changed weights")
        diagnosis={lang:classify(scores["TRAIN"][lang]["accuracy"],scores["EVAL"][lang]["accuracy"]) for lang in ("en","ja")}
        reports.append(dict(seed=seed,family=family,metrics=scores,behavior=extra,diagnosis=diagnosis,
            parent_replay_error=error,before_sha256=before,after_sha256=after,
            forward_calls=calls[0],evaluated_rows=calls[1]))
        prediction_records.append(dict(seed=seed,family=family,predictions=preds))
        fingerprints.append(dict(seed=seed,family=family,before=before,after=after))
        print(f"[C235] seed={seed} family={family} diagnosis={diagnosis}",flush=True)
    summary=summarize(reports); require(gate(summary),"diagnostic integrity gate")
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    for name,value in (("diagnostic-plan.json",manifest()),("diagnostics.json",reports),
        ("predictions.json",prediction_records),("model-fingerprints.json",fingerprints),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard(); precheck(c234_summary,root)
    for path,sha in protected.items(): require(a.sha(path)==sha,"modified input:"+path)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
        validation_summary=summary,gate_f_candidate=False,network_calls=0,
        limitations=["frozen diagnostic, not successful binding or a rescue of C234",
            "TRAIN scoring is not held-out generalization; no causal proof of optimizer/architecture cause",
            "reused small synthetic contexts, unequal model capacity, no speed or general-language claim"])
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C235 RESULT ===",flush=True); print(blob(result).decode(),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("c234-summary","output-dir"): parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True); run(**vars(parser.parse_args()))


if __name__=="__main__": main()
