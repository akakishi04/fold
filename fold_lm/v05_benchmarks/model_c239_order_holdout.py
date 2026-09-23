"""C239: fresh TRAIN-order0 fitting and held-out order1 evaluation, not general language."""
from __future__ import annotations
import argparse
import ast
from collections import Counter
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

EXPERIMENT_ID = "C239-v5b-fact-order-holdout"
STAGE = "V5-B-FACT-ORDER-HOLDOUT"
BASE = "74100dd8c7b151f0cdd44e36ef846825614d7836"
PARENT_EXECUTION = "a7999c92e2f6f071c045de268feaf5ddd6f438ac"
PARENT_SHA = "06ab54549477894ea17f986364cacc6b3b7d25ff2dea70b18e98e2a957c80363"
PARENT_ARTIFACTS = {
    "measurements.json": "3d358412484f9f9d227ea0a37e8b5ca9de72fff980f8f7d0d32a95982b658fe7",
    "probe-dataset.json": "bc80e9ea2607ae1e99b2b1da3bb85d5f20ba9dc4b103e67176428f9703a9f52c",
    "sampler-plan.json": "ae9d0b7e92ee7024b57210f1779aebbfc0757fa995acbdf6f9359b2f23664232",
    "trained-models.pt": "2a09b28dd2a10c210380cbe05eb18360f69d309e44bc3e9599f0eb3e178c624d",
    "validation-summary.json": "8c7edfb3a5634bd06a7d3f4b15db909d7e09330e1cec844bda943a363f69670a",
}
SPLIT_SHA = "6f47a61c0ec4de616e77dab803ad964a9243e627b8a06f3e987d2824f8951731"
MANIFEST_SHA = "4eca2f0276b521286729f1819abd929a035659a589488b332fe976d392b4dac0"
SEEDS, FAMILIES = (234001,234002,234003), ("full","gru_only")
VIEWS = ("normal","evidence_blind","query_blind")
SPLITS = ("TRAIN","HOLDOUT")
STEPS, BATCH, LR, CLIP, TOL = 400,32,0.005,1.0,1e-9
OWN = ("fold_lm/v05_benchmarks/model_c239_order_holdout.py",
    "tests_lm/test_v05_c239_order_holdout.py", "tools/run_c239.ps1", "tools/invoke_c239.ps1",
    "docs/experiment-ledger-addendum-c239-preregistration.md", "docs/v5b-fact-order-holdout-v0.1.md")
OUTPUTS = {"holdout-plan.json","split-dataset.json","trained-models.pt","measurements.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c238_complete_cohort_sampler as parent
    return parent


def context():
    parent=parent_module()
    _,fitting,binding,factory,audit=parent.context()
    return parent,fitting,binding,factory,audit


def identities():
    return list(itertools.product(SEEDS,FAMILIES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        split_sha256=SPLIT_SHA,partition="order0 TRAIN8; order1 HOLDOUT8; preserve parent row bytes",
        identities=[list(x) for x in identities()],views=list(VIEWS),splits=list(SPLITS),
        initialization="fresh, exact accepted C238 initial_sha256; no trained parent state",
        parameters=dict(full=13488,gru_only=10160),width=16,slots=48,
        train_rows=8,holdout_rows=8,rows_per_language_per_split=4,pairs_per_kind_per_language_per_split=2,
        batch_indices=list(range(8))*4,steps_per_model=STEPS,batch_size=BATCH,lr=LR,clip_norm=CLIP,
        optimizer="AdamW",betas=[.9,.999],eps=1e-8,weight_decay=0.0,
        total_training_steps=2400,total_answer_presentations=76800,train_row_presentations_per_model=1600,
        evaluation_forwards=90,model_forward_calls=2490,total_row_presentations=77520,
        evaluation_order="initial TRAIN3; fit400; final TRAIN3/HOLDOUT3; reload TRAIN3/HOLDOUT3",
        checkpoint_writes=1,final_step=400,accuracy_threshold=.90,pair_threshold=.80,mask_drop_threshold=.35,
        primary="all Full TRAIN and HOLDOUT seed/language cells pass; GRU-only independently",
        replay_tolerance=TOL,device="cpu",dtype="float64",threads=2,deterministic_algorithms=True,
        source_pins=280,protected_inputs=418,direct_dependencies=15,own_tests=24,
        modules=124,loaded_tests=2906,focused_tests=2905,excluded_test=EXCLUDED,
        group_overlap="intentional matched facts/questions; prompt/row-ID disjoint, not fact-disjoint",
        general_language_claim=False,unseen_entity_value_claim=False,gate_f_candidate=False,network_calls=0)


def split_pool(rows):
    require(len(rows)==16 and digest(rows)==PARENT_ARTIFACTS["probe-dataset.json"],"parent cohort identity")
    parts={key:[r for r in rows if r["order"]==order] for key,order in zip(SPLITS,(0,1),strict=True)}
    require(digest(parts)==SPLIT_SHA,"split identity")
    for part in parts.values():
        require(len(part)==8 and len({r["id"] for r in part})==8,"split count")
        require(all(r["split"]=="TRAIN" for r in part),"parent membership metadata must remain unchanged")
        for lang in ("en","ja"):
            require(Counter(r["target"] for r in part if r["language"]==lang)=={48:2,49:2},"split balance")
    for key in ("id","prompt"):
        require(not {r[key] for r in parts["TRAIN"]}&{r[key] for r in parts["HOLDOUT"]},"split leakage")
    return parts


def balanced_indices(count):
    require(type(count) is int and count==8,"C239 requires exactly8 TRAIN rows")
    return torch.arange(count,dtype=torch.int64).repeat(4)


def fit(model,train_tokens,train_targets,seed,*,steps=STEPS):
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
        if (step+1)%100==0:print(f"[C239] seed={seed} step={step+1}/{steps} answer_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=steps,answer_presentations=steps*BATCH,first_loss=first,last_loss=last,
                fit_seconds=time.perf_counter()-started)


def audit_fit_contract(parent):
    class Labels(ast.NodeTransformer):
        def visit_Constant(self,node):
            if isinstance(node.value,str): node.value=node.value.replace("[C238]","[C239]")
            return node
    source=Labels().visit(ast.parse(inspect.getsource(parent.fit)))
    require(ast.dump(source,include_attributes=False)==ast.dump(ast.parse(inspect.getsource(fit)),include_attributes=False),
        "fit differs beyond progress label; cohort repetition is confined to balanced_indices")
    require(all(getattr(parent,key)==globals()[key] for key in ("STEPS","BATCH","LR","CLIP","TOL")),"training constants")


def validate_metrics(metrics):
    require(set(metrics)=={"en","ja"},"metric languages")
    rates=("accuracy","evidence_blind_accuracy","query_blind_accuracy","fact_pair_accuracy","query_pair_accuracy")
    keys=set(rates)|{"rows","answer_nll","evidence_drop","query_drop"}
    for m in metrics.values():
        require(set(m)==keys and m["rows"]==4,"C239 metric schema/count")
        require(all(type(v) in (int,float) and math.isfinite(v) for v in m.values()),"nonfinite metric")
        require(all(0<=m[k]<=1 for k in rates) and m["answer_nll"]>=0,"metric range")
        require(abs(m["evidence_drop"]-m["accuracy"]+m["evidence_blind_accuracy"])<=TOL
            and abs(m["query_drop"]-m["accuracy"]+m["query_blind_accuracy"])<=TOL,"mask semantics")


def cell_pass(m):
    return (m["accuracy"]>=.90 and m["fact_pair_accuracy"]>=.80 and m["query_pair_accuracy"]>=.80
        and m["evidence_drop"]>=.35 and m["query_drop"]>=.35)


def predictions(logits):
    require(len(logits)==3 and all(x.shape==(8,256) and bool(torch.isfinite(x).all()) for x in logits),"logit shape/finite")
    return {key:x.argmax(-1).tolist() for key,x in zip(VIEWS,logits,strict=True)}


def evaluate(model,rows,binding,fingerprint):
    before=fingerprint(model)
    views=[binding.tensors(rows,mode) for mode in VIEWS]
    metrics,logits=binding.evaluate(model,rows,views)
    validate_metrics(metrics); predictions(logits)
    require(fingerprint(model)==before,"evaluation mutated weights")
    return metrics,logits


def train_one(model,parts,reference,*,binding,factory):
    before=factory.fingerprint(model)
    require(before==reference["initial_sha256"],"fresh initial fingerprint mismatch")
    counts=[0,0]
    def hook(module,args,output): counts[0]+=1; counts[1]+=len(args[0])
    handle=model.register_forward_hook(hook)
    try:
        initial,_=evaluate(model,parts["TRAIN"],binding,factory.fingerprint)
        tokens,targets=binding.tensors(parts["TRAIN"],"normal")
        trained=fit(model,tokens,targets,reference["seed"])
        final={}; raw={}
        for key in SPLITS: final[key],raw[key]=evaluate(model,parts[key],binding,factory.fingerprint)
    finally: handle.remove()
    after=factory.fingerprint(model)
    require(before!=after and counts==[409,12872],"training update/workload")
    record=dict(seed=reference["seed"],family=reference["family"],initial_sha256=before,final_sha256=after,
        initial_train=initial,final=final,fit=trained,forward_calls=counts[0],row_presentations=counts[1],
        predictions={k:predictions(v) for k,v in raw.items()},weights_changed=True)
    state={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    return record,state,raw


def replay_one(model,state,record,raw,parts,*,binding,factory):
    model.load_state_dict(state,strict=True); model.eval()
    require(factory.fingerprint(model)==record["final_sha256"],"checkpoint identity")
    counts=[0,0]
    def hook(module,args,output): counts[0]+=1; counts[1]+=len(args[0])
    handle=model.register_forward_hook(hook); error=0.0
    try:
        for key in SPLITS:
            metrics,logits=evaluate(model,parts[key],binding,factory.fingerprint)
            error=max(error,*(float((a-c).abs().max()) for a,c in zip(logits,raw[key],strict=True)),
                *(abs(metrics[l][k]-record["final"][key][l][k]) for l in metrics for k in metrics[l]))
            require(predictions(logits)==record["predictions"][key],"prediction replay")
    finally: handle.remove()
    require(error<=TOL and counts==[6,48],"replay error/workload")
    record.update(checkpoint_roundtrip=True,prediction_replayed=True,reload_max_error=error,
        forward_calls=record["forward_calls"]+6,row_presentations=record["row_presentations"]+48)


def load_bundle(path):
    value=torch.load(path,map_location="cpu",weights_only=True)
    require(value["schema"]=="fold-c239-order-holdout-v1" and value["identities"]==[list(x) for x in identities()]
        and len(value["states"])==6,"checkpoint schema/order")
    return value["states"]


def summarize(records):
    require([(r["seed"],r["family"]) for r in records]==identities(),"measurement order")
    labels=Counter(); gates={f:True for f in FAMILIES}
    for r in records:
        require(set(r["final"])==set(SPLITS),"split metrics")
        for metrics in r["final"].values(): validate_metrics(metrics)
        for lang in ("en","ja"):
            train=cell_pass(r["final"]["TRAIN"][lang]); held=cell_pass(r["final"]["HOLDOUT"][lang])
            labels["TRAIN_FIT_MISS" if not train else "ORDER_HOLDOUT_MISS" if not held else "BOTH_PASS"]+=1
            gates[r["family"]]&=train and held
    return dict(models=6,full_order_gate=gates["full"],gru_order_gate=gates["gru_only"],cell_outcomes=dict(labels),
        all_replays=all(r["checkpoint_roundtrip"] is True and r["prediction_replayed"] is True and 0<=r["reload_max_error"]<=TOL for r in records),
        all_weights_changed=all(r["weights_changed"] is True for r in records),
        total_training_steps=sum(r["fit"]["steps"] for r in records),total_answer_presentations=sum(r["fit"]["answer_presentations"] for r in records),
        model_forward_calls=sum(r["forward_calls"] for r in records),total_row_presentations=sum(r["row_presentations"] for r in records),
        general_language_claim=False,unseen_entity_value_claim=False)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(280,418) and set(OWN)<=set(p["source_blobs"]),"protection coverage")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"output coverage")
    s=p["validation_summary"]
    require((s["models"],s["total_training_steps"],s["total_answer_presentations"],s["model_forward_calls"],s["total_row_presentations"])
        ==(6,2400,76800,2490,77520),"fixed workload")
    require(s["all_replays"] is True and s["all_weights_changed"] is True and sum(s["cell_outcomes"].values())==12,"result integrity")
    require(type(s["full_order_gate"]) is bool and type(s["gru_order_gate"]) is bool
        and p["status"]==("PASS" if s["full_order_gate"] else "FAIL"),"ability status")
    require(p["gate_f_candidate"] is False and p["network_calls"]==0
        and s["general_language_claim"] is False and s["unseen_entity_value_claim"] is False,"scope")


def precheck(c238_summary,root):
    parent,_,_,factory,a=context(); root=Path(root); path=Path(c238_summary).resolve()
    require(a.sha(path)==PARENT_SHA,"parent summary hash")
    p=a.read_json(path); parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS"
        and p["validation_summary"]["full_probe_gate"] is True and p["validation_summary"]["gru_probe_gate"] is True,"accepted parent")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items(): require(Path(name).is_file() and a.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items(): require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    require(str(path) not in protected,"parent double count"); protected[str(path)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifact identities")
    for item in p["artifacts"]:
        child=a.safe_child(path.parent,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"parent artifact bytes")
        require(str(child.resolve()) not in protected,"artifact double count"); protected[str(child.resolve())]=item["sha256"]
    for name in OWN:
        require(name not in pins,"OWN collision"); pins[name]=a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    deps=set(factory.LM_SOURCES)|{OWN[0]}|{"fold_lm/v05_benchmarks/"+x for x in (
        "gate_f_c230_prepared_capsule.py","model_c231_byte_eval_contract.py","model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py","model_c234_context_binding.py","model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py","model_c237_frozen_signal_audit.py","model_c238_complete_cohort_sampler.py")}
    require(len(deps)==15 and deps<=set(pins),"direct dependency protection")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(280,418) and digest(manifest())==MANIFEST_SHA,"counts/manifest")
    audit_fit_contract(parent)
    return pins,protected


def load_inputs(c238_summary):
    parent,fitting,_,_,a=context(); directory=Path(c238_summary).resolve().parent
    parts=split_pool(a.read_json(directory/"probe-dataset.json"))
    records=a.read_json(directory/"measurements.json")
    require(parent.summarize(records,fitting=fitting)==a.read_json(c238_summary)["validation_summary"],"parent measurement summary")
    require([(r["seed"],r["family"]) for r in records]==identities(),"parent identities")
    for r in records:
        initial=r["initial_sha256"]
        require(isinstance(initial,str) and len(initial)==64 and all(c in "0123456789abcdef" for c in initial),"initial fingerprint contract")
        fitting.validate_metrics(r["initial_probe"]); fitting.validate_metrics(r["final_probe"])
        require(r["initial_sha256"]!=r["final_sha256"],"parent before/after identity")
    return parts,records


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==123,"parent modules")
    return names+["tests_lm.test_v05_c239_order_holdout"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite): yield from flatten(item)
        else: yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests]; require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"test identities")
    kept=[t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(2906,2905),"regression count")
    return unittest.TestSuite(kept)


def run(*,c238_summary,output_dir,expected_head):
    _,_,binding,factory,a=context(); root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"execution HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tracked tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c238_summary,root); parts,parents=load_inputs(c238_summary)
    records=[]; states=[]; raw=[]; out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    for seed in SEEDS:
        full=factory.new_model(seed); baseline=binding.parent_module().new_baseline(full)
        require((sum(p.numel() for p in full.parameters()),sum(p.numel() for p in baseline.parameters()))==(13488,10160),"model size")
        for family,model in (("full",full),("gru_only",baseline)):
            reference=parents[len(records)]
            require((reference["seed"],reference["family"])==(seed,family),"paired identity")
            print(f"[C239] model={len(records)+1}/6 seed={seed} family={family}; TRAIN order0 only",flush=True)
            record,state,outputs=train_one(model,parts,reference,binding=binding,factory=factory)
            records.append(record); states.append(state); raw.append(outputs)
    torch.save(dict(schema="fold-c239-order-holdout-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for r,state,outputs in zip(records,load_bundle(out/"trained-models.pt"),raw,strict=True):
        model=factory.new_model(r["seed"])
        if r["family"]=="gru_only": model=binding.parent_module().new_baseline(model)
        replay_one(model,state,r,outputs,parts,binding=binding,factory=factory)
    summary=summarize(records)
    for name,value in (("holdout-plan.json",manifest()),("split-dataset.json",parts),("measurements.json",records),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard(); precheck(c238_summary,root)
    for name,wanted in protected.items(): require(a.sha(name)==wanted,"modified input")
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["full_order_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,network_calls=0,limitations=["Order transfer only; same entities, values and facts.",
        "Parent source split labels remain TRAIN; experiment partitions define optimizer membership.",
        "Training coverage/repetition differs from C238; not a matched all16 accuracy comparison."])
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C239 RESULT ===",flush=True); print(blob(result).decode(),flush=True)
    return result


def verify_artifacts(output_dir,c238_summary,expected_head):
    _,_,_,_,a=context(); out=Path(output_dir); p=a.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"]==expected_head,"saved execution identity")
    for name,wanted in p["input_sha256"].items(): require(a.sha(name)==wanted,"postcheck input")
    for item in p["artifacts"]:
        path=a.safe_child(out,item["file"])
        require(a.sha(path)==item["sha256"] and path.stat().st_size==item["serialized_bytes"],"postcheck artifact")
    records=a.read_json(out/"measurements.json")
    require(summarize(records)==p["validation_summary"]==a.read_json(out/"validation-summary.json"),"saved summary")
    require(a.read_json(out/"holdout-plan.json")==manifest(),"saved plan")
    parts,parents=load_inputs(c238_summary)
    require(a.read_json(out/"split-dataset.json")==parts and digest(parts)==SPLIT_SHA,"saved partition")
    for r,reference in zip(records,parents,strict=True): require(r["initial_sha256"]==reference["initial_sha256"],"saved initial identity")
    return p,records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("c238-summary","output-dir"): parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
