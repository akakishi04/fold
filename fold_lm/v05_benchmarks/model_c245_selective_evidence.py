"""C245: frozen selective factual-value erasure; diagnostic integrity, not ability."""
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
from torch.nn import functional as F

EXPERIMENT_ID = "C245-v5b-frozen-selective-evidence"
STAGE = "V5-B-FROZEN-SELECTIVE-EVIDENCE"
BASE = "2d7fc4fabee22a7a5f718748756b952deb979f25"
PARENT_EXECUTION = "d89007bc5a04c4f6b99bff966093b0e14174e04b"
PARENT_SHA = "a2c5167bd6e93c09020ca5079cc94d77e692fd18768588536379d4797fd99297"
PARENT_ARTIFACTS = {
    "measurements.json": "cd0fba1897aea554a74b984622f97fa93399baadda4fff5a757e1bfdbd24239d",
    "split-dataset.json": "e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346",
    "trained-models.pt": "90c367dc4026e757ed561af75a25d529d37dd9fea404d4d6370f1bac5211b519",
    "two-partner-plan.json": "e89a41c15ef3d702c7009a9b4fc22f4e28809dea3892c5d63cf02120a1e10b0b",
    "validation-summary.json": "b80fea969f5329fc401c0be3470233ae50dd55319b3a83c0e0047a5fe4c0808f",
}
SEEDS, FAMILIES = (234001, 234002, 234003), ("full", "gru_only")
ROWS = {"TRAIN": 64, "HOLDOUT": 32}
ORIGINAL = ("normal", "evidence_blind", "query_blind")
SELECTIVE = ("queried_value_blind", "other_value_blind")
VIEWS = ORIGINAL + SELECTIVE
TOL = 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c245_selective_evidence.py",
       "tests_lm/test_v05_c245_selective_evidence.py", "tools/run_c245.ps1", "tools/invoke_c245.ps1",
       "docs/experiment-ledger-addendum-c245-preregistration.md", "docs/v5b-selective-evidence-v0.1.md")
OUTPUTS = {"diagnostic-plan.json", "intervention-inputs.json", "outputs.json", "diagnostics.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "50cadf2e5b9bc0c1a1fab5f29652afd5b5c2f0eeaed3be919cdadb3ebcebf1ac"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c244_two_partner_recombination as parent
    return parent


def context():
    parent = parent_module()
    _, fitting, binding, factory, audit = parent.context()
    return parent, fitting, binding, factory, audit


def identities():
    return list(itertools.product(SEEDS, FAMILIES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        identities=[list(x) for x in identities()], rows=ROWS, views=list(VIEWS),
        intervention="replace exactly one factual digit by ?; keep names/query/order/byte length",
        checkpoint="all six accepted C244 final states; no checkpoint selection",
        model_forward_calls=60, row_presentations=2880, diagnostic_cells=24, checkpoint_bundle_loads=1,
        new_training_steps=0, checkpoint_writes=0, network_calls=0,
        dtype="float64", device="cpu", threads=2, deterministic=True, replay_tolerance=TOL,
        gate="integrity and original-view replay only; no selective-accuracy cutoff",
        selective_input_ceilings=dict(TRAIN=dict(queried_value_blind=.5, other_value_blind=1.),
                                     HOLDOUT=dict(queried_value_blind=1., other_value_blind=1.)),
        source_pins=316, protected_inputs=490, direct_dependencies=21, own_tests=24,
        modules=130, loaded_tests=3050, focused_tests=3049, excluded_test=EXCLUDED,
        gate_f_candidate=False, capability_pass_claim=False, causal_mechanism_claim=False)


def masked_prompt(row, mode, binding):
    require(mode in SELECTIVE, "selective mode")
    normal = binding.render(row)
    fields = normal.split(";")
    require(len(fields)==3 and row["objects"]==[0, 1] and row["query"] in (0, 1), "fact layout")
    index = row["objects"].index(row["query"])
    if row["order"]:
        index = 1-index
    if mode=="other_value_blind":
        index = 1-index
    require(fields[index][-1] in "0123" and fields[index][-2]=="=", "single factual digit")
    fields[index] = fields[index][:-1]+"?"
    changed = ";".join(fields)
    a, c = normal.encode(), changed.encode()
    require(len(a)==len(c) and sum(x!=y for x, y in zip(a, c))==1, "one-byte erasure")
    return changed


def input_records(parts, binding):
    require(set(parts)==set(ROWS) and digest(parts)==PARENT_ARTIFACTS["split-dataset.json"], "fixed C244 partition")
    result = {}
    for split, rows in parts.items():
        require(len(rows)==ROWS[split], "partition size")
        result[split] = {v: [binding.render(r, v) if v in ORIGINAL else masked_prompt(r, v, binding) for r in rows] for v in VIEWS}
        for mode in SELECTIVE:
            groups = defaultdict(Counter)
            for row, text in zip(rows, result[split][mode], strict=True):
                groups[text][row["target"]] += 1
            ceiling = sum(max(x.values()) for x in groups.values())/len(rows)
            require(ceiling==manifest()["selective_input_ceilings"][split][mode], "masked ambiguity ceiling")
    return result


def tensors(rows, texts, mode, binding, factory):
    tokens = torch.stack([factory.prefix_tensor(s.encode()) for s in texts])
    targets = torch.tensor([r["target"] for r in rows], dtype=torch.int64)
    require(tokens.dtype==torch.int64 and tokens.shape==(len(rows), 48), "token shape/dtype")
    if mode in ORIGINAL:
        old_tokens, old_targets = binding.tensors(rows, mode)
        require(torch.equal(tokens, old_tokens) and torch.equal(targets, old_targets), "parent tokenizer parity")
    else:
        normal, _ = binding.tensors(rows, "normal")
        changed = tokens!=normal
        require(bool((changed.sum(1)==1).all()) and bool((tokens[changed]==63).all()), "selective token erasure")
    return tokens, targets


def checked_logits(value, n):
    require(isinstance(value, torch.Tensor) and value.shape==(n, 256) and value.dtype==torch.float64
            and value.device.type=="cpu" and bool(torch.isfinite(value).all()), "logit contract")
    return value


def original_metrics(rows, outputs, binding):
    logits = [outputs[v] for v in ORIGINAL]
    predictions = [x.argmax(-1).tolist() for x in logits]
    targets = torch.tensor([r["target"] for r in rows], dtype=torch.int64)
    result = binding.metrics(rows, *predictions, logits[0], targets)
    for lang in ("en", "ja"):
        groups = defaultdict(list)
        for i, row in enumerate(rows):
            if row["language"]==lang:
                groups[(row["group"], row["query"])].append(i)
        require(len(groups)==len(rows)//4 and all(len(g)==2 and rows[g[0]]["target"]==rows[g[1]]["target"] for g in groups.values()), "order pairs")
        result[lang]["order_pair_accuracy"] = sum(all(predictions[0][i]==rows[i]["target"] for i in g) for g in groups.values())/len(groups)
    return result


def compare_parent(parts, outputs, reference, binding):
    error = 0.
    require(set(reference["predictions"])==set(reference["final"])==set(ROWS), "parent fields")
    for split, rows in parts.items():
        calculated = original_metrics(rows, outputs[split], binding)
        require(set(reference["final"][split])==set(calculated), "parent languages")
        for lang, metrics in calculated.items():
            saved = reference["final"][split][lang]
            require(set(saved)==set(metrics), "parent metric keys")
            for key, value in metrics.items():
                require(type(saved[key]) in (int, float) and math.isfinite(saved[key]) and math.isfinite(value), "parent metric finite")
                error = max(error, abs(value-saved[key]))
        require(set(reference["predictions"][split])==set(ORIGINAL), "parent prediction views")
        for view in ORIGINAL:
            require(outputs[split][view].argmax(-1).tolist()==reference["predictions"][split][view], "parent answer replay")
    require(error<=TOL, "parent metric replay")
    return error


def score_model(parts, inputs, model, reference, binding, factory):
    require(not model.training and all(not p.requires_grad and p.grad is None for p in model.parameters()), "model not frozen")
    before = factory.fingerprint(model)
    require(before==reference["final_sha256"], "accepted final fingerprint")
    counts, outputs = [0, 0], {}
    def hook(module, args, output):
        counts[0] += 1
        counts[1] += len(args[0])
    handle = model.register_forward_hook(hook)
    try:
        with torch.no_grad():
            for split, rows in parts.items():
                outputs[split] = {}
                for mode in VIEWS:
                    tokens, _ = tensors(rows, inputs[split][mode], mode, binding, factory)
                    logits = model(tokens, torch.zeros(len(rows), dtype=torch.int64))
                    outputs[split][mode] = checked_logits(logits, len(rows)).detach().clone()
    finally:
        handle.remove()
    after = factory.fingerprint(model)
    require(after==before and counts==[10, 480] and not model.training
            and all(not p.requires_grad and p.grad is None for p in model.parameters()), "mutation/workload")
    error = compare_parent(parts, outputs, reference, binding)
    return dict(seed=reference["seed"], family=reference["family"], before_sha256=before, after_sha256=after,
        forward_calls=counts[0], row_presentations=counts[1], parent_metric_error=error,
        logits={s: {v: x.tolist() for v, x in values.items()} for s, values in outputs.items()})


def decode_outputs(record):
    require(set(record["logits"])==set(ROWS), "output partitions")
    result = {}
    for split, n in ROWS.items():
        require(set(record["logits"][split])==set(VIEWS), "output views")
        result[split] = {v: checked_logits(torch.tensor(x, dtype=torch.float64), n) for v, x in record["logits"][split].items()}
    return result


def diagnose(parts, records):
    require([(r["seed"], r["family"]) for r in records]==identities(), "record identity order")
    cells = []
    for record in records:
        outputs = decode_outputs(record)
        for split, rows in parts.items():
            target = torch.tensor([r["target"] for r in rows])
            normal = outputs[split]["normal"]
            normal_pred = normal.argmax(-1)
            normal_loss = F.cross_entropy(normal, target, reduction="none")
            for lang in ("en", "ja"):
                ids = torch.tensor([i for i, r in enumerate(rows) if r["language"]==lang])
                cell = dict(seed=record["seed"], family=record["family"], split=split, language=lang, rows=len(ids), views={})
                base_ok = normal_pred[ids]==target[ids]
                for mode in VIEWS:
                    logits = outputs[split][mode]
                    pred = logits.argmax(-1)
                    loss = F.cross_entropy(logits, target, reduction="none")
                    ok = pred[ids]==target[ids]
                    cell["views"][mode] = dict(correct=int(ok.sum()), accuracy=float(ok.double().mean()),
                        answer_nll=float(loss[ids].mean()), accuracy_drop=float(base_ok.double().mean()-ok.double().mean()),
                        answer_flips=int((pred[ids]!=normal_pred[ids]).sum()),
                        correct_to_wrong=int((base_ok & ~ok).sum()), wrong_to_correct=int((~base_ok & ok).sum()),
                        nll_increase=float((loss[ids]-normal_loss[ids]).mean()),
                        logit_linf=float((logits[ids]-normal[ids]).abs().max()))
                cells.append(cell)
    return cells


def summarize(records):
    require([(r["seed"], r["family"]) for r in records]==identities(), "summary order")
    for r in records:
        require(r["before_sha256"]==r["after_sha256"] and len(r["before_sha256"])==64
                and 0<=r["parent_metric_error"]<=TOL and (r["forward_calls"], r["row_presentations"])==(10,480), "frozen replay/count")
    return dict(models=6, diagnostic_cells=24, model_forward_calls=sum(r["forward_calls"] for r in records),
        row_presentations=sum(r["row_presentations"] for r in records), all_parent_replays=True,
        all_fingerprints_unchanged=True, new_training_steps=0, checkpoint_writes=0,
        capability_pass_claim=False, causal_mechanism_claim=False)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS"
            and p["diagnostic_execution_valid"] is True, "diagnostic identity")
    require((len(p["source_blobs"]), len(p["input_sha256"]))==(316,490) and set(OWN)<=set(p["source_blobs"]), "protection counts")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS, "output coverage")
    expected = dict(models=6, diagnostic_cells=24, model_forward_calls=60, row_presentations=2880,
        all_parent_replays=True, all_fingerprints_unchanged=True, new_training_steps=0,
        checkpoint_writes=0, capability_pass_claim=False, causal_mechanism_claim=False)
    require(p["validation_summary"]==expected and p["gate_f_candidate"] is False and p["network_calls"]==0, "integrity/scope")


def precheck(c244_summary, root):
    parent, _, _, factory, a = context()
    root, path = Path(root), Path(c244_summary).resolve()
    require(a.sha(path)==PARENT_SHA, "parent summary hash")
    p = a.read_json(path)
    parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL"
            and p["validation_summary"]["cell_outcomes"]=={"RECOMBINATION_MISS":12}, "accepted C244")
    pins, protected = dict(p["source_blobs"]), dict(p["input_sha256"])
    for name, wanted in protected.items():
        require(Path(name).is_file() and a.sha(name)==wanted, "changed input: "+name)
    for name, wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted, "changed source: "+name)
    require(str(path) not in protected, "parent duplicate")
    protected[str(path)] = PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS, "parent artifacts")
    for item in p["artifacts"]:
        child = a.safe_child(path.parent, item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"], "parent bytes")
        require(str(child.resolve()) not in protected, "artifact duplicate")
        protected[str(child.resolve())] = item["sha256"]
    for name in OWN:
        require(name not in pins, "OWN collision")
        pins[name] = a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    helpers = ("gate_f_c230_prepared_capsule.py", "model_c231_byte_eval_contract.py", "model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py", "model_c234_context_binding.py", "model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py", "model_c237_frozen_signal_audit.py", "model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py", "model_c240_saved_position_audit.py", "model_c241_assignment_holdout.py",
        "model_c242_balanced_recombination.py", "model_c243_saved_recombination_audit.py", "model_c244_two_partner_recombination.py")
    deps = set(factory.LM_SOURCES)|{OWN[0]}|{"fold_lm/v05_benchmarks/"+h for h in helpers}
    require(len(deps)==21 and deps<=set(pins), "direct dependency coverage")
    protected.update(a.protect_tree_files(root, pins))
    require((len(pins),len(protected))==(316,490) and digest(manifest())==MANIFEST_SHA, "counts/manifest")
    return pins, protected


def load_inputs(c244_summary):
    parent, fitting, binding, _, a = context()
    path = Path(c244_summary).resolve()
    parts = a.read_json(path.parent/"split-dataset.json")
    input_records(parts, binding)
    refs = a.read_json(path.parent/"measurements.json")
    require(parent.summarize(refs, fitting)==a.read_json(path)["validation_summary"], "parent measurement replay")
    require([(r["seed"],r["family"]) for r in refs]==identities(), "parent identity order")
    for r in refs:
        h = r["final_sha256"]
        require(isinstance(h,str) and len(h)==64 and all(c in "0123456789abcdef" for c in h), "final fingerprint schema")
    return parts, refs


def regression_modules(root):
    names = parent_module().regression_modules(root)
    require(len(names)==len(set(names))==129, "parent modules")
    return names+["tests_lm.test_v05_c245_selective_evidence"]


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1, "suite identities")
    kept = [t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(3050,3049), "suite counts")
    return unittest.TestSuite(kept)


def run(*, c244_summary, output_dir, expected_head):
    parent, _, binding, factory, a = context()
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head, "HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss", "branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(), "dirty tree")
    guard()
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    pins, protected = precheck(c244_summary, root)
    parts, refs = load_inputs(c244_summary)
    inputs = input_records(parts, binding)
    states = parent.load_bundle(Path(c244_summary).resolve().parent/"trained-models.pt")
    records = []
    for ref, state in zip(refs, states, strict=True):
        model = factory.new_model(ref["seed"])
        if ref["family"]=="gru_only":
            model = binding.parent_module().new_baseline(model)
        model.load_state_dict(state, strict=True)
        model.eval().requires_grad_(False)
        print(f'[C245] model={len(records)+1}/6 seed={ref["seed"]} family={ref["family"]}; frozen evidence erasure', flush=True)
        records.append(score_model(parts, inputs, model, ref, binding, factory))
    cells, summary = diagnose(parts, records), summarize(records)
    require(len(cells)==24, "diagnostic cell coverage")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    for name, value in (("diagnostic-plan.json",manifest()),("intervention-inputs.json",inputs),
        ("outputs.json",records),("diagnostics.json",cells),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n,sha256=a.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard()
    precheck(c244_summary, root)
    for name, wanted in protected.items():
        require(a.sha(name)==wanted, "modified input")
    p = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,network_calls=0,limitations=[
            "Selective masks are out-of-training-distribution; accuracy is not a capability gate.",
            "Hiding queried value leaves redundant information, particularly on the HOLDOUT matching.",
            "Input-erasure sensitivity is not a unique internal-mechanism attribution or improvement."])
    validate_result(p)
    (out/"summary.json").write_bytes(blob(p))
    print("=== C245 RESULT ===", flush=True)
    print(blob(p).decode(), flush=True)
    return p


def verify_artifacts(output_dir, c244_summary, expected_head):
    _, _, binding, _, a = context()
    torch.set_num_threads(2)
    out = Path(output_dir)
    p = a.read_json(out/"summary.json")
    validate_result(p)
    require(p["commit_sha"]==expected_head, "saved HEAD")
    for name, wanted in p["input_sha256"].items():
        require(a.sha(name)==wanted, "postcheck input")
    for item in p["artifacts"]:
        child = a.safe_child(out,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"], "artifact bytes")
    parts, refs = load_inputs(c244_summary)
    require(a.read_json(out/"diagnostic-plan.json")==manifest(), "saved plan")
    require(a.read_json(out/"intervention-inputs.json")==input_records(parts,binding), "saved intervention inputs")
    records = a.read_json(out/"outputs.json")
    require(summarize(records)==p["validation_summary"]==a.read_json(out/"validation-summary.json"), "saved summary")
    for record, ref in zip(records,refs,strict=True):
        require(record["before_sha256"]==ref["final_sha256"], "saved final identity")
        require(abs(compare_parent(parts,decode_outputs(record),ref,binding)-record["parent_metric_error"])<=TOL, "saved parent replay")
    cells = diagnose(parts,records)
    require(cells==a.read_json(out/"diagnostics.json") and len(cells)==24, "persisted logit diagnostic replay")
    return p,cells


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("c244-summary","output-dir"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
