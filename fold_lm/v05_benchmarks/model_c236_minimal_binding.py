"""C236: fixed-budget fit of 16 existing TRAIN binding rows; not generalization."""
from __future__ import annotations
import argparse
import ast
import hashlib
import inspect
import itertools
import json
import math
from pathlib import Path
import time
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C236-v5b-minimal-binding-learnability"
STAGE = "V5-B-MINIMAL-BINDING-LEARNABILITY"
BASE = "4e7c83ae5948ac1ee403b61f018b334f170f32c4"
PARENT_EXECUTION = "fc3311955c3dcda87b67c2ee8dd58a59fb256d6f"
PARENT_SHA = "a9d6daa76bab38488ec3634d186ba81a2d61ae878df80202f3084057e917b1b5"
PARENT_ARTIFACTS = {
    "diagnostic-plan.json": "2e8bb701b3a6d512479c7118ac0973784617e1243639ef00c3903caed1a0f6c3",
    "diagnostics.json": "a93f73fb6cb17d9a3a8067f8a4d522cafe68acad56d02200ce95de521f5a989c",
    "model-fingerprints.json": "28c26fa0d6ecf84db469b6ee3a945bd956489802cd4795d39b3a28c15fd7d71c",
    "predictions.json": "10f477d42f1b53a250c34e77616a81f17f3e92e008f9ae1619fe572a055c44d3",
    "validation-summary.json": "30ac8dcbe92b826e9d2f69384204ade6e6fb9fb6e07b660713325c9640385023",
}
DATA_SHA = "72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85"
PROBE_SHA = "bc80e9ea2607ae1e99b2b1da3bb85d5f20ba9dc4b103e67176428f9703a9f52c"
MANIFEST_SHA = "86f534a54964a31d0139d5a3ceb3ef4b5e3c2ab46667adb002390a5b5d347957"
SEEDS, FAMILIES = (234001, 234002, 234003), ("full", "gru_only")
VIEWS = ("normal", "evidence_blind", "query_blind")
STEPS, BATCH, LR, CLIP, TOL = 400, 32, 0.005, 1.0, 1e-9
OWN = (
    "fold_lm/v05_benchmarks/model_c236_minimal_binding.py",
    "tests_lm/test_v05_c236_minimal_binding.py",
    "tools/run_c236.ps1", "tools/invoke_c236.ps1",
    "docs/experiment-ledger-addendum-c236-preregistration.md",
    "docs/v5b-minimal-binding-learnability-v0.1.md",
)
OUTPUTS = {"probe-plan.json", "probe-dataset.json", "trained-models.pt",
           "measurements.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c235_frozen_binding_diagnostic as parent
    return parent


def context():
    parent = parent_module()
    binding = parent.parent_module()
    factory = binding.factory_module()
    audit = binding.parent_module().parent_module().audit_module()
    return parent, binding, factory, audit


def identities():
    return list(itertools.product(SEEDS, FAMILIES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
        parent_artifacts=PARENT_ARTIFACTS, parent_dataset_sha256=DATA_SHA,
        probe_sha256=PROBE_SHA, selection="C234 TRAIN; objects [0,1]; sorted values [0,1]",
        train_rows=16, languages=["en", "ja"], identities=[list(x) for x in identities()],
        views=list(VIEWS), initialization="fresh identical C234 initial fingerprints; common copy before fit",
        parameters=dict(full=13488, gru_only=10160), slots=48, width=16,
        steps_per_model=STEPS, batch_size=BATCH, lr=LR, clip_norm=CLIP,
        optimizer="AdamW", betas=[0.9,0.999], eps=1e-8, weight_decay=0.0,
        sampler="CPU generator seed+1000; replacement sampling over selected16 rows",
        total_training_steps=2400, total_answer_presentations=76800,
        evaluation_forward_calls=54, model_forward_calls=2454, total_row_presentations=77664,
        checkpoint_writes=1, min_probe_accuracy=0.90, min_fact_pair_accuracy=0.80,
        min_query_pair_accuracy=0.80, min_evidence_drop=0.35, min_query_drop=0.35,
        replay_tolerance=TOL, dtype="float64", device="cpu", threads=2,
        deterministic_algorithms=True, evaluation="initial/final/reloaded on the same16 TRAIN rows only",
        selection_step=400, held_out_evaluation_rows=0, primary="all full seed/language cells pass",
        baseline="GRU-only same criteria independently; no superiority gate",
        changed="training cohort breadth only relative to C234; no budget extension",
        general_language_claim=False, held_out_generalization_claim=False, gate_f_candidate=False,
        source_pins=262, protected_inputs=382, own_tests=24, modules=121,
        loaded_tests=2834, focused_tests=2833, excluded_test=EXCLUDED, network_calls=0)


def select_probe(train):
    require(len(train) == 384 and all(r["split"] == "TRAIN" for r in train), "parent TRAIN contract")
    rows = [r for r in train if r["objects"] == [0,1] and sorted(r["values"]) == [0,1]]
    require(len(rows) == 16 and digest(rows) == PROBE_SHA, "minimal cohort identity")
    return rows


def fit(model,train_tokens,train_targets,seed,*,steps=STEPS):
    require(type(steps) is int and steps>0 and len(train_tokens)==train_targets.numel()>0,"training inputs")
    sampler=torch.Generator(device="cpu").manual_seed(seed+1000)
    optimizer=torch.optim.AdamW(model.parameters(),lr=LR,betas=(0.9,0.999),eps=1e-8,weight_decay=0.0)
    model.train(); started=time.perf_counter(); first=last=None
    for step in range(steps):
        ids=torch.randint(len(train_targets),(BATCH,),generator=sampler)
        optimizer.zero_grad(set_to_none=True)
        logits=model(train_tokens[ids],torch.zeros(BATCH,dtype=torch.int64))
        loss=F.cross_entropy(logits,train_targets[ids]); require(bool(torch.isfinite(loss)),"nonfinite training loss")
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),CLIP,error_if_nonfinite=True)
        optimizer.step(); last=float(loss.detach())
        if first is None:first=last
        if (step+1)%100==0:print(f"[C236] seed={seed} step={step+1}/{steps} answer_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=steps,answer_presentations=steps*BATCH,first_loss=first,last_loss=last,
                fit_seconds=time.perf_counter()-started)


def audit_fit_contract(binding):
    """Training executable AST must equal accepted C234, except its progress label."""
    class Labels(ast.NodeTransformer):
        def visit_Constant(self, node):
            if isinstance(node.value, str):
                node.value = node.value.replace("[C234]", "[C236]")
            return node
    def normalized(fn):
        return ast.dump(Labels().visit(ast.parse(inspect.getsource(fn))), include_attributes=False)
    require(normalized(fit) == normalized(binding.fit), "training algorithm differs from C234")
    require(all(getattr(binding,k) == globals()[k] for k in ("STEPS","BATCH","LR","CLIP","TOL")),
            "training constants differ")


def validate_metrics(metrics):
    require(set(metrics) == {"en","ja"}, "probe languages")
    rates = ("accuracy", "evidence_blind_accuracy", "query_blind_accuracy", "fact_pair_accuracy", "query_pair_accuracy")
    for m in metrics.values():
        require(m["rows"] == 8, "probe subgroup count")
        for k in (*rates, "answer_nll", "evidence_drop", "query_drop"):
            require(type(m[k]) in (int,float) and math.isfinite(m[k]), "nonfinite metric")
        require(all(0 <= m[k] <= 1 for k in rates) and m["answer_nll"] >= 0, "metric range")
        require(abs(m["evidence_drop"]-(m["accuracy"]-m["evidence_blind_accuracy"])) <= TOL
                and abs(m["query_drop"]-(m["accuracy"]-m["query_blind_accuracy"])) <= TOL,
                "mask drop semantics")


def probe_pass(metrics):
    validate_metrics(metrics)
    return all(m["accuracy"] >= .90 and m["fact_pair_accuracy"] >= .80
        and m["query_pair_accuracy"] >= .80 and m["evidence_drop"] >= .35
        and m["query_drop"] >= .35 for m in metrics.values())


def prediction_record(logits):
    require(len(logits) == 3 and all(x.shape == (16,256) and bool(torch.isfinite(x).all()) for x in logits),
            "probe logits")
    return {mode:x.argmax(-1).tolist() for mode,x in zip(VIEWS,logits,strict=True)}


def train_one(model, *, binding, factory, rows, views, seed, family, expected_initial):
    before = factory.fingerprint(model)
    require(before == expected_initial, "not the accepted C234 fresh initialization")
    calls = [0,0]
    def hook(module, args, output): calls[0] += 1; calls[1] += len(args[0])
    handle = model.register_forward_hook(hook)
    try:
        initial, _ = binding.evaluate(model, rows, views)
        validate_metrics(initial)
        require(factory.fingerprint(model) == before, "initial evaluation mutated model")
        trained = fit(model, *views[0], seed)
        final_hash = factory.fingerprint(model)
        final, logits = binding.evaluate(model, rows, views)
        validate_metrics(final)
        require(factory.fingerprint(model) == final_hash and before != final_hash,
                "final evaluation mutation or no learning update")
    finally:
        handle.remove()
    require(calls == [406,12896], "training/evaluation workload")
    state = {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    rec = dict(seed=seed, family=family, initial_sha256=before, final_sha256=final_hash,
        initial_probe=initial, final_probe=final, fit=trained, predictions=prediction_record(logits),
        weights_changed=True, forward_calls=calls[0], row_presentations=calls[1])
    return rec, state, logits


def replay_one(model, state, record, reference, *, binding, factory, rows, views):
    model.load_state_dict(state, strict=True); model.eval()
    require(factory.fingerprint(model) == record["final_sha256"], "checkpoint fingerprint")
    calls = [0,0]
    def hook(module, args, output): calls[0] += 1; calls[1] += len(args[0])
    handle = model.register_forward_hook(hook)
    try: metrics, logits = binding.evaluate(model, rows, views)
    finally: handle.remove()
    validate_metrics(metrics)
    error = max(float((x-y).abs().max()) for x,y in zip(logits,reference,strict=True))
    metric_error = max(abs(metrics[l][k]-record["final_probe"][l][k])
                       for l in ("en","ja") for k in record["final_probe"][l])
    require(error <= TOL and metric_error <= TOL and prediction_record(logits) == record["predictions"],
            "checkpoint replay mismatch")
    require(calls == [3,48] and factory.fingerprint(model) == record["final_sha256"],
            "replay workload or weight mutation")
    record.update(checkpoint_roundtrip=True, prediction_replayed=True,
        reload_max_error=error, replay_metric_error=metric_error,
        forward_calls=record["forward_calls"]+calls[0], row_presentations=record["row_presentations"]+calls[1])


def load_bundle(path):
    value = torch.load(path, map_location="cpu", weights_only=True)
    require(value["schema"] == "fold-c236-minimal-binding-v1"
        and value["identities"] == [list(x) for x in identities()] and len(value["states"]) == 6,
        "C236 checkpoint schema/order")
    return value["states"]


def summarize(records):
    require([(r["seed"],r["family"]) for r in records] == identities(), "record order")
    return dict(models=6, full_probe_gate=all(probe_pass(r["final_probe"]) for r in records if r["family"]=="full"),
        gru_probe_gate=all(probe_pass(r["final_probe"]) for r in records if r["family"]=="gru_only"),
        all_replays=all(r["checkpoint_roundtrip"] is True and r["prediction_replayed"] is True
            and 0 <= r["reload_max_error"] <= TOL and 0 <= r["replay_metric_error"] <= TOL for r in records),
        all_weights_changed=all(r["weights_changed"] is True for r in records),
        total_training_steps=sum(r["fit"]["steps"] for r in records),
        total_answer_presentations=sum(r["fit"]["answer_presentations"] for r in records),
        model_forward_calls=sum(r["forward_calls"] for r in records),
        total_row_presentations=sum(r["row_presentations"] for r in records),
        general_language_claim=False, held_out_generalization_claim=False)


def validate_result(result):
    require(result["experiment_id"] == EXPERIMENT_ID and result["stage"] == STAGE
            and result["diagnostic_execution_valid"] is True, "result identity")
    require((len(result["source_blobs"]),len(result["input_sha256"])) == (262,382)
        and set(OWN) <= set(result["source_blobs"]), "result protection")
    require(len(result["artifacts"]) == 5 and {x["file"] for x in result["artifacts"]} == OUTPUTS,
            "artifact coverage")
    s = result["validation_summary"]
    require(s["models"] == 6 and s["all_replays"] is True and s["all_weights_changed"] is True
        and (s["total_training_steps"],s["total_answer_presentations"],s["model_forward_calls"],s["total_row_presentations"])
        == (2400,76800,2454,77664), "execution integrity")
    require(type(s["full_probe_gate"]) is bool and type(s["gru_probe_gate"]) is bool
        and result["status"] == ("PASS" if s["full_probe_gate"] else "FAIL"), "scientific status")
    require(result["gate_f_candidate"] is False and result["network_calls"] == 0
        and s["general_language_claim"] is False and s["held_out_generalization_claim"] is False, "scope")


def precheck(c235_summary, c234_summary, root):
    parent,binding,factory,a = context(); root=Path(root)
    require(a.sha(c235_summary) == PARENT_SHA, "C235 summary identity")
    p = a.read_json(c235_summary); parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS"
        and p["validation_summary"]["diagnosis_counts"] == {"TRAIN_ACCURACY_BELOW_90":12}, "accepted C235 diagnostic")
    pins,protected = dict(p["source_blobs"]),dict(p["input_sha256"])
    for path,wanted in protected.items(): require(Path(path).is_file() and a.sha(path)==wanted, "changed input:"+path)
    for path,wanted in pins.items(): require(a.git(root,"rev-parse","HEAD:"+path).decode().strip()==wanted, "changed source:"+path)
    require(a.sha(c234_summary) == parent.PARENT_SHA
        and protected.get(str(Path(c234_summary).resolve())) == parent.PARENT_SHA, "C234 source summary not protected")
    protected[str(Path(c235_summary).resolve())] = PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]} == PARENT_ARTIFACTS, "C235 artifact identities")
    for item in p["artifacts"]:
        path=a.safe_child(Path(c235_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path)==item["sha256"] and path.stat().st_size==item["serialized_bytes"], "parent artifact bytes")
        protected[str(path.resolve())]=item["sha256"]
    for path in OWN:
        require(path not in pins, "OWN collision")
        pins[path]=a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    deps=set(factory.LM_SOURCES) | {OWN[0],
        "fold_lm/v05_benchmarks/model_c235_frozen_binding_diagnostic.py",
        "fold_lm/v05_benchmarks/model_c234_context_binding.py",
        "fold_lm/v05_benchmarks/model_c233_core_ablation.py",
        "fold_lm/v05_benchmarks/model_c232_bilingual_learning.py",
        "fold_lm/v05_benchmarks/model_c231_byte_eval_contract.py",
        "fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"}
    require(len(deps)==12 and deps<=set(pins), "direct dependency protection")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected)) == (262,382), "protection counts")
    require(digest(manifest())==MANIFEST_SHA, "manifest drift"); audit_fit_contract(binding)
    return pins,protected


def load_inputs(c234_summary):
    parent,binding,_,a=context(); directory=Path(c234_summary).resolve().parent
    data=a.read_json(directory/"dataset.json")
    train,_=binding.validate_dataset(data)
    rows=select_probe(train)
    saved=parent.validate_parent_records(a.read_json(directory/"measurements.json"))
    initial={(r["seed"],r["family"]):r["initial_sha256"] for r in saved}
    require(list(initial)==identities(), "parent initial identity order")
    return rows,initial


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==120, "parent modules")
    return names+["tests_lm.test_v05_c236_minimal_binding"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite): yield from flatten(item)
        else: yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1, "test identity/exclusion")
    kept=[t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(2834,2833), "regression counts")
    return unittest.TestSuite(kept)


def run(*, c235_summary, c234_summary, output_dir, expected_head):
    parent,binding,factory,a=context(); root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head, "HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss", "branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(), "dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c235_summary,c234_summary,root)
    rows,initial=load_inputs(c234_summary)
    views=[binding.tensors(rows,mode) for mode in VIEWS]
    records=[]; states=[]; references=[]
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    for seed in SEEDS:
        full=factory.new_model(seed)
        baseline=binding.parent_module().new_baseline(full)
        require((sum(p.numel() for p in full.parameters()),sum(p.numel() for p in baseline.parameters()))
                == (13488,10160), "model size")
        for family,model in (("full",full),("gru_only",baseline)):
            print(f"[C236] family={family} seed={seed}; minimal TRAIN16",flush=True)
            record,state,reference=train_one(model,binding=binding,factory=factory,rows=rows,views=views,
                seed=seed,family=family,expected_initial=initial[(seed,family)])
            records.append(record); states.append(state); references.append(reference)
    torch.save(dict(schema="fold-c236-minimal-binding-v1", identities=[list(x) for x in identities()], states=states),out/"trained-models.pt")
    reloaded=load_bundle(out/"trained-models.pt")
    for record,state,reference in zip(records,reloaded,references,strict=True):
        model=factory.new_model(record["seed"])
        if record["family"]=="gru_only": model=binding.parent_module().new_baseline(model)
        replay_one(model,state,record,reference,binding=binding,factory=factory,rows=rows,views=views)
    summary=summarize(records)
    for name,value in (("probe-plan.json",manifest()),("probe-dataset.json",rows),
                       ("measurements.json",records),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard(); precheck(c235_summary,c234_summary,root)
    for path,wanted in protected.items(): require(a.sha(path)==wanted, "modified input:"+path)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if summary["full_probe_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,network_calls=0,limitations=[
            "16 seen TRAIN rows only; success may be memorization and is not C234 rescue",
            "cohort reduction also increases repeat exposure and reduces vocabulary breadth",
            "negative is fixed-recipe failure, not architecture-wide impossibility or a cause diagnosis"])
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C236 RESULT ===",flush=True); print(blob(result).decode(),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("c235-summary","c234-summary","output-dir"): parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
