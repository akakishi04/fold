"""C241: train both fact positions on assignment[0,1], hold out swapped assignment."""
from __future__ import annotations
import argparse
import ast
from collections import Counter, defaultdict
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

EXPERIMENT_ID = "C241-v5b-assignment-holdout-balanced-order"
STAGE = "V5-B-ASSIGNMENT-HOLDOUT-BALANCED-ORDER"
BASE = "e74ec1f66b1b475f3d91b54183818c8168c2ab3b"
PARENT_EXECUTION = "7bf66561cfb151a6ba2562791a1645b760ad6f1f"
PARENT_SHA = "3551a5da3346381fdeb81b80a7cd297822ee51f64e80f9d966158ecf4c36b8b0"
PARENT_ARTIFACTS = {
    "audit-plan.json": "31d2b0579d65b354979ef1d98e3012a57a95820e2f12cd729c931c8d8525bc25",
    "diagnostics.json": "3db440f1348746bbdee122abd404fa7894cca9a9cc5a7abd8d688735c575be8e",
    "paired-orders.json": "4e9bb61c419a9f710374261f8b5c95fd5414ce254fb2a7d5b1963ca88bc9fc6f",
    "row-audit.json": "bffbba05c1625ff8375867a7642c9087ba6edcc901fa31214e2b396a87bf2d4e",
    "validation-summary.json": "ba79501874430b2967db3e2c57cf9bd8abe8cae0258e6827ff1b92e7b716a66e",
}
C239_EXECUTION = "c847609c8d045c9c5db4ec882bf336a9671180ff"
C239_SHA = "500af8c078c5a6114d1cb115b0dad9ee5ae7f622c41fce765f144668e2e041af"
SPLIT_SHA = "1d373b3652bf03027a1e23c45e2fc117895015640193b49f9c38f07099a1ae7a"
MANIFEST_SHA = "1552239e7701744af508ba41ac4b620898d219380b377be1c5671b816dbac1f8"
SEEDS, FAMILIES = (234001, 234002, 234003), ("full", "gru_only")
VIEWS, SPLITS = ("normal", "evidence_blind", "query_blind"), ("TRAIN", "HOLDOUT")
STEPS, BATCH, LR, CLIP, TOL = 400, 32, 0.005, 1.0, 1e-9
OWN = (
    "fold_lm/v05_benchmarks/model_c241_assignment_holdout.py",
    "tests_lm/test_v05_c241_assignment_holdout.py",
    "tools/run_c241.ps1", "tools/invoke_c241.ps1",
    "docs/experiment-ledger-addendum-c241-preregistration.md",
    "docs/v5b-assignment-holdout-v0.1.md",
)
OUTPUTS = {"assignment-plan.json", "split-dataset.json", "trained-models.pt",
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
    from fold_lm.v05_benchmarks import model_c240_saved_position_audit as parent
    return parent


def context():
    parent = parent_module()
    fitting = parent.parent_module()
    _, _, binding, factory, audit = fitting.context()
    return parent, fitting, binding, factory, audit


def identities():
    return list(itertools.product(SEEDS, FAMILIES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        c239_summary_sha256=C239_SHA, assignment_split_sha256=SPLIT_SHA,
        partition="values[0,1] TRAIN8; values[1,0] HOLDOUT8; both orders/queries/languages",
        identities=[list(x) for x in identities()], views=list(VIEWS), splits=list(SPLITS),
        initialization="fresh; exact C239 initial_sha256; no trained parent state",
        parameters=dict(full=13488, gru_only=10160), width=16, slots=48,
        train_rows=8, holdout_rows=8, rows_per_language_per_split=4,
        query_pairs_per_language_per_split=2, order_pairs_per_language_per_split=2,
        batch_indices=list(range(8))*4, steps_per_model=STEPS, batch_size=BATCH, lr=LR, clip_norm=CLIP,
        optimizer="AdamW", betas=[.9,.999], eps=1e-8, weight_decay=0.0,
        total_training_steps=2400, total_answer_presentations=76800, train_row_presentations_per_model=1600,
        evaluation_forwards=90, model_forward_calls=2490, total_row_presentations=77520,
        evaluation_order="initial TRAIN3; fit400; final TRAIN3/HOLDOUT3; reload TRAIN3/HOLDOUT3",
        checkpoint_writes=1, final_step=400, accuracy_threshold=.90, query_pair_threshold=.80,
        order_pair_threshold=.80, evidence_drop_threshold=.35, query_drop_threshold=.35,
        primary="all Full TRAIN and HOLDOUT seed/language cells pass; GRU-only independently",
        replay_tolerance=TOL, device="cpu", dtype="float64", threads=2, deterministic_algorithms=True,
        source_pins=292, protected_inputs=442, direct_dependencies=17, own_tests=24,
        modules=126, loaded_tests=2954, focused_tests=2953, excluded_test=EXCLUDED,
        position_shortcut_train_accuracy=.50, entity_constant_holdout_accuracy=0.0,
        general_language_claim=False, unseen_entity_claim=False, unseen_value_claim=False,
        gate_f_candidate=False, network_calls=0)


def split_assignments(source_parts):
    parent = parent_module()
    source_parts = parent.validate_parts(source_parts)
    parts = {
        "TRAIN": [r for split in SPLITS for r in source_parts[split] if r["values"] == [0,1]],
        "HOLDOUT": [r for split in SPLITS for r in source_parts[split] if r["values"] == [1,0]],
    }
    require(digest(parts) == SPLIT_SHA, "assignment split identity")
    for split, values in (("TRAIN", [0,1]), ("HOLDOUT", [1,0])):
        rows = parts[split]
        require(len(rows) == 8 and len({r["id"] for r in rows}) == 8, "partition count/identity")
        require(all(r["values"] == values and r["split"] == "TRAIN" for r in rows), "assignment/provenance")
        for lang in ("en","ja"):
            sub = [r for r in rows if r["language"] == lang]
            require(len(sub) == 4 and Counter(r["order"] for r in sub) == {0:2,1:2}
                and Counter(r["query"] for r in sub) == {0:2,1:2}
                and Counter(r["target"] for r in sub) == {48:2,49:2}, "factor balance")
    for key in ("id","prompt"):
        require(not {r[key] for r in parts["TRAIN"]} & {r[key] for r in parts["HOLDOUT"]}, "partition leakage")
    return parts


def balanced_indices(count):
    require(type(count) is int and count == 8, "C241 requires exactly8 TRAIN rows")
    return torch.arange(count, dtype=torch.int64).repeat(4)


def fit(model, train_tokens, train_targets, seed, *, steps=STEPS):
    require(type(steps) is int and steps>0 and len(train_tokens)==train_targets.numel()>0,"training inputs")
    sampler=torch.Generator(device="cpu").manual_seed(seed+1000)
    optimizer=torch.optim.AdamW(model.parameters(),lr=LR,betas=(0.9,0.999),eps=1e-8,weight_decay=0.0)
    model.train(); started=time.perf_counter(); first=last=None
    for step in range(steps):
        ids=balanced_indices(len(train_targets))
        optimizer.zero_grad(set_to_none=True)
        logits=model(train_tokens[ids],torch.zeros(BATCH,dtype=torch.int64))
        loss=F.cross_entropy(logits,train_targets[ids]); require(bool(torch.isfinite(loss)),"nonfinite training loss")
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),CLIP,error_if_nonfinite=True)
        optimizer.step(); last=float(loss.detach())
        if first is None:first=last
        if (step+1)%100==0:print(f"[C241] seed={seed} step={step+1}/{steps} answer_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=steps,answer_presentations=steps*BATCH,first_loss=first,last_loss=last,
                fit_seconds=time.perf_counter()-started)


def audit_fit_contract(fitting):
    class Labels(ast.NodeTransformer):
        def visit_Constant(self,node):
            if isinstance(node.value,str):
                node.value=node.value.replace("[C239]","[C241]")
            return node
    expected = Labels().visit(ast.parse(inspect.getsource(fitting.fit)))
    actual = ast.parse(inspect.getsource(fit))
    require(ast.dump(expected,include_attributes=False) == ast.dump(actual,include_attributes=False),
        "fit differs from accepted C239 beyond progress tag")
    require(all(getattr(fitting,k) == globals()[k] for k in ("STEPS","BATCH","LR","CLIP","TOL")),
        "training constants differ")


def pair_accuracy(rows, predictions, kind):
    require(kind in ("query","order") and len(rows)==len(predictions), "pair inputs")
    groups=defaultdict(list)
    for i,(row,pred) in enumerate(zip(rows,predictions,strict=True)):
        key=(row["group"],row["order"]) if kind=="query" else (row["group"],row["query"])
        groups[key].append((row["target"],pred))
    require(len(groups)==2 and all(len(g)==2 for g in groups.values()), "pair coverage")
    if kind=="query":
        require(all(g[0][0] != g[1][0] for g in groups.values()), "query targets must differ")
    else:
        require(all(g[0][0] == g[1][0] for g in groups.values()), "order targets must match")
    return sum(all(t==p for t,p in group) for group in groups.values())/2


def metrics(rows, prediction, evidence, query, logits, targets):
    require(len(rows)==len(prediction)==len(evidence)==len(query)==8 and logits.shape==(8,256)
        and targets.shape==(8,), "metric input shapes")
    loss=F.cross_entropy(logits,targets,reduction="none")
    require(bool(torch.isfinite(loss).all()), "nonfinite evaluation loss")
    out={}
    for lang in ("en","ja"):
        ids=[i for i,r in enumerate(rows) if r["language"]==lang]
        require(len(ids)==4, "language rows")
        sub=[rows[i] for i in ids]; pred=[prediction[i] for i in ids]
        acc=sum(prediction[i]==rows[i]["target"] for i in ids)/4
        ea=sum(evidence[i]==rows[i]["target"] for i in ids)/4
        qa=sum(query[i]==rows[i]["target"] for i in ids)/4
        out[lang]=dict(rows=4,accuracy=acc,answer_nll=float(loss[ids].mean()),
            evidence_blind_accuracy=ea,query_blind_accuracy=qa,evidence_drop=acc-ea,query_drop=acc-qa,
            query_pair_accuracy=pair_accuracy(sub,pred,"query"),order_pair_accuracy=pair_accuracy(sub,pred,"order"))
    return out


def validate_metrics(value):
    require(set(value)=={"en","ja"}, "metric languages")
    rates=("accuracy","evidence_blind_accuracy","query_blind_accuracy","query_pair_accuracy","order_pair_accuracy")
    keys=set(rates)|{"rows","answer_nll","evidence_drop","query_drop"}
    for m in value.values():
        require(set(m)==keys and m["rows"]==4, "metric schema/count")
        require(all(type(v) in (int,float) and math.isfinite(v) for v in m.values()), "nonfinite metric")
        require(all(0<=m[k]<=1 for k in rates) and m["answer_nll"]>=0, "metric range")
        require(abs(m["evidence_drop"]-m["accuracy"]+m["evidence_blind_accuracy"])<=TOL
            and abs(m["query_drop"]-m["accuracy"]+m["query_blind_accuracy"])<=TOL, "mask semantics")


def cell_pass(m):
    return (m["accuracy"]>=.90 and m["query_pair_accuracy"]>=.80 and m["order_pair_accuracy"]>=.80
        and m["evidence_drop"]>=.35 and m["query_drop"]>=.35)


def predictions(logits):
    require(len(logits)==3 and all(x.shape==(8,256) and bool(torch.isfinite(x).all()) for x in logits),
        "prediction logits")
    return {mode:x.argmax(-1).tolist() for mode,x in zip(VIEWS,logits,strict=True)}


def evaluate(model, rows, binding, fingerprint):
    before=fingerprint(model); training=model.training; model.eval()
    views=[binding.tensors(rows,mode) for mode in VIEWS]; outputs=[]
    try:
        with torch.no_grad():
            for tokens,_ in views:
                logits=model(tokens,torch.zeros(len(tokens),dtype=torch.int64))
                require(logits.shape==(8,256) and bool(torch.isfinite(logits).all()), "bad logits")
                outputs.append(logits.detach())
    finally:
        model.train(training)
    pred=[x.argmax(-1).tolist() for x in outputs]
    result=metrics(rows,*pred,outputs[0],views[0][1]); validate_metrics(result)
    require(fingerprint(model)==before, "evaluation mutated weights")
    return result,outputs


def train_one(model, parts, reference, *, binding, factory):
    before=factory.fingerprint(model)
    require(before==reference["initial_sha256"], "fresh initial fingerprint mismatch")
    counts=[0,0]
    def hook(module,args,output): counts[0]+=1; counts[1]+=len(args[0])
    handle=model.register_forward_hook(hook)
    try:
        initial,_=evaluate(model,parts["TRAIN"],binding,factory.fingerprint)
        tokens,targets=binding.tensors(parts["TRAIN"],"normal")
        trained=fit(model,tokens,targets,reference["seed"])
        final={}; raw={}
        for split in SPLITS:
            final[split],raw[split]=evaluate(model,parts[split],binding,factory.fingerprint)
    finally:
        handle.remove()
    after=factory.fingerprint(model)
    require(before!=after and counts==[409,12872], "training update/workload")
    record=dict(seed=reference["seed"],family=reference["family"],initial_sha256=before,final_sha256=after,
        initial_train=initial,final=final,fit=trained,forward_calls=counts[0],row_presentations=counts[1],
        predictions={s:predictions(raw[s]) for s in SPLITS},weights_changed=True)
    state={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    return record,state,raw


def replay_one(model,state,record,raw,parts,*,binding,factory):
    model.load_state_dict(state,strict=True); model.eval()
    require(factory.fingerprint(model)==record["final_sha256"], "checkpoint fingerprint")
    counts=[0,0]
    def hook(module,args,output): counts[0]+=1; counts[1]+=len(args[0])
    handle=model.register_forward_hook(hook); error=0.0
    try:
        for split in SPLITS:
            measured,logits=evaluate(model,parts[split],binding,factory.fingerprint)
            error=max(error,*(float((a-c).abs().max()) for a,c in zip(logits,raw[split],strict=True)),
                *(abs(measured[l][k]-record["final"][split][l][k]) for l in measured for k in measured[l]))
            require(predictions(logits)==record["predictions"][split], "prediction replay")
    finally:
        handle.remove()
    require(error<=TOL and counts==[6,48], "replay/workload")
    record.update(checkpoint_roundtrip=True,prediction_replayed=True,reload_max_error=error,
        forward_calls=record["forward_calls"]+6,row_presentations=record["row_presentations"]+48)


def load_bundle(path):
    value=torch.load(path,map_location="cpu",weights_only=True)
    require(value["schema"]=="fold-c241-assignment-holdout-v1"
        and value["identities"]==[list(x) for x in identities()] and len(value["states"])==6,
        "checkpoint schema/order")
    return value["states"]


def summarize(records):
    require([(r["seed"],r["family"]) for r in records]==identities(), "record order")
    labels=Counter(); gates={f:True for f in FAMILIES}
    for r in records:
        require(set(r["final"])==set(SPLITS), "split metrics")
        for split in SPLITS: validate_metrics(r["final"][split])
        for lang in ("en","ja"):
            train=cell_pass(r["final"]["TRAIN"][lang]); held=cell_pass(r["final"]["HOLDOUT"][lang])
            labels["TRAIN_FIT_MISS" if not train else "ASSIGNMENT_HOLDOUT_MISS" if not held else "BOTH_PASS"]+=1
            gates[r["family"]] &= train and held
    return dict(models=6,full_assignment_gate=gates["full"],gru_assignment_gate=gates["gru_only"],
        cell_outcomes=dict(labels),
        all_replays=all(r["checkpoint_roundtrip"] is True and r["prediction_replayed"] is True
            and 0<=r["reload_max_error"]<=TOL for r in records),
        all_weights_changed=all(r["weights_changed"] is True for r in records),
        total_training_steps=sum(r["fit"]["steps"] for r in records),
        total_answer_presentations=sum(r["fit"]["answer_presentations"] for r in records),
        model_forward_calls=sum(r["forward_calls"] for r in records),
        total_row_presentations=sum(r["row_presentations"] for r in records),
        general_language_claim=False,unseen_entity_claim=False,unseen_value_claim=False)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,
        "result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(292,442) and set(OWN)<=set(p["source_blobs"]),
        "protection coverage")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS, "artifact coverage")
    s=p["validation_summary"]
    require((s["models"],s["total_training_steps"],s["total_answer_presentations"],s["model_forward_calls"],
        s["total_row_presentations"])==(6,2400,76800,2490,77520), "fixed workload")
    require(s["all_replays"] is True and s["all_weights_changed"] is True and sum(s["cell_outcomes"].values())==12,
        "result integrity")
    require(type(s["full_assignment_gate"]) is bool and type(s["gru_assignment_gate"]) is bool
        and p["status"]==("PASS" if s["full_assignment_gate"] else "FAIL"), "scientific status")
    require(p["gate_f_candidate"] is False and p["network_calls"]==0 and s["general_language_claim"] is False
        and s["unseen_entity_claim"] is False and s["unseen_value_claim"] is False, "scope")


def precheck(c240_summary,c239_summary,root):
    parent,fitting,_,factory,a=context(); root=Path(root); c240=Path(c240_summary).resolve(); c239=Path(c239_summary).resolve()
    require(a.sha(c240)==PARENT_SHA, "C240 summary hash")
    p=a.read_json(c240); parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS"
        and p["validation_summary"]["all_discrete_replays"] is True, "accepted C240 parent")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items(): require(Path(name).is_file() and a.sha(name)==wanted, "changed input:"+name)
    for name,wanted in pins.items(): require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted, "changed source:"+name)
    require(str(c240) not in protected, "parent summary duplicate"); protected[str(c240)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS, "C240 artifact identities")
    for item in p["artifacts"]:
        child=a.safe_child(c240.parent,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"], "C240 artifact bytes")
        require(str(child.resolve()) not in protected, "parent artifact duplicate"); protected[str(child.resolve())]=item["sha256"]
    require(protected.get(str(c239))==C239_SHA and a.sha(c239)==C239_SHA, "C239 summary protection")
    q=a.read_json(c239); fitting.validate_result(q)
    require(q["commit_sha"]==C239_EXECUTION and q["status"]=="FAIL"
        and q["validation_summary"]["cell_outcomes"]=={"ORDER_HOLDOUT_MISS":12}, "accepted C239 source parent")
    for name in OWN:
        require(name not in pins, "OWN collision"); pins[name]=a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    deps=set(factory.LM_SOURCES)|{OWN[0]}|{"fold_lm/v05_benchmarks/"+x for x in (
        "gate_f_c230_prepared_capsule.py","model_c231_byte_eval_contract.py","model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py","model_c234_context_binding.py","model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py","model_c237_frozen_signal_audit.py","model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py","model_c240_saved_position_audit.py")}
    require(len(deps)==17 and deps<=set(pins), "direct dependency coverage")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(292,442) and digest(manifest())==MANIFEST_SHA, "counts/manifest")
    audit_fit_contract(fitting)
    return pins,protected


def load_inputs(c239_summary):
    parent,fitting,_,_,a=context(); directory=Path(c239_summary).resolve().parent
    source=parent.validate_parts(a.read_json(directory/"split-dataset.json"))
    parts=split_assignments(source)
    records=a.read_json(directory/"measurements.json")
    summary=a.read_json(c239_summary)["validation_summary"]
    require(fitting.summarize(records)==summary, "C239 measurement summary")
    require([(r["seed"],r["family"]) for r in records]==identities(), "C239 identity order")
    for r in records:
        parent.validate_record(source,r)
        initial=r["initial_sha256"]
        require(isinstance(initial,str) and len(initial)==64 and all(c in "0123456789abcdef" for c in initial)
            and initial!=r["final_sha256"], "initial/final fingerprint semantics")
    return parts,records


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==125, "parent module count")
    return names+["tests_lm.test_v05_c241_assignment_holdout"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite): yield from flatten(item)
        else: yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests]; require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1, "suite identity")
    kept=[t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(2954,2953), "suite counts")
    return unittest.TestSuite(kept)


def run(*,c240_summary,c239_summary,output_dir,expected_head):
    _,_,binding,factory,a=context(); root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head, "execution HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss", "branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(), "dirty tracked tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c240_summary,c239_summary,root); parts,parents=load_inputs(c239_summary)
    records=[]; states=[]; raw=[]; out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    for seed in SEEDS:
        full=factory.new_model(seed); baseline=binding.parent_module().new_baseline(full)
        require((sum(p.numel() for p in full.parameters()),sum(p.numel() for p in baseline.parameters()))==(13488,10160),
            "model size")
        for family,model in (("full",full),("gru_only",baseline)):
            reference=parents[len(records)]
            require((reference["seed"],reference["family"])==(seed,family), "paired identity")
            print(f"[C241] model={len(records)+1}/6 seed={seed} family={family}; TRAIN assignment[0,1] both orders",flush=True)
            record,state,outputs=train_one(model,parts,reference,binding=binding,factory=factory)
            records.append(record); states.append(state); raw.append(outputs)
    torch.save(dict(schema="fold-c241-assignment-holdout-v1",identities=[list(x) for x in identities()],states=states),
        out/"trained-models.pt")
    for r,state,outputs in zip(records,load_bundle(out/"trained-models.pt"),raw,strict=True):
        model=factory.new_model(r["seed"])
        if r["family"]=="gru_only": model=binding.parent_module().new_baseline(model)
        replay_one(model,state,r,outputs,parts,binding=binding,factory=factory)
    summary=summarize(records)
    for name,value in (("assignment-plan.json",manifest()),("split-dataset.json",parts),
        ("measurements.json",records),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard(); precheck(c240_summary,c239_summary,root)
    for name,wanted in protected.items(): require(a.sha(name)==wanted, "modified input")
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if summary["full_assignment_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,network_calls=0,limitations=[
            "Assignment transfer uses only two entities and binary values; not general language.",
            "A pass rules out the preregistered fixed-position and fixed-entity-value shortcuts on this fixture, not all shortcuts.",
            "TRAIN/HOLDOUT differ by value assignment; this is not unseen vocabulary or entity transfer."])
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C241 RESULT ===",flush=True); print(blob(result).decode(),flush=True)
    return result


def verify_artifacts(output_dir,c239_summary,expected_head):
    _,_,_,_,a=context(); out=Path(output_dir); p=a.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"]==expected_head, "saved execution identity")
    for name,wanted in p["input_sha256"].items(): require(a.sha(name)==wanted, "postcheck input")
    for item in p["artifacts"]:
        child=a.safe_child(out,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"], "postcheck artifact")
    records=a.read_json(out/"measurements.json")
    require(summarize(records)==p["validation_summary"]==a.read_json(out/"validation-summary.json"), "saved summary")
    require(a.read_json(out/"assignment-plan.json")==manifest(), "saved plan")
    parts,parents=load_inputs(c239_summary)
    require(a.read_json(out/"split-dataset.json")==parts and digest(parts)==SPLIT_SHA, "saved split")
    for r,reference in zip(records,parents,strict=True):
        require(r["initial_sha256"]==reference["initial_sha256"], "saved initial identity")
    return p,records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("c240-summary","c239-summary","output-dir"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
