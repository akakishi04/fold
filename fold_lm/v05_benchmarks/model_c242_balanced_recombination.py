"""C242: balanced value/order training and held-out value-pair recombination."""
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

EXPERIMENT_ID = "C242-v5b-balanced-value-recombination"
STAGE = "V5-B-BALANCED-VALUE-RECOMBINATION"
BASE = "0caa412ce1ce6452d721adac19d2d37f6e3d0128"
PARENT_EXECUTION = "b7b33718da1edd94cc1ed113baa6e56cc27dc3e4"
PARENT_SHA = "b228992dfd5d85e59d7c45d1dd899145588978a19ade0817a547d740e8c67e26"
PARENT_ARTIFACTS = {
    "assignment-plan.json":"1552239e7701744af508ba41ac4b620898d219380b377be1c5671b816dbac1f8",
    "measurements.json":"2ad0f83840e01fa2f074b0a313261b8c662ec4d40a9c8a13d0a24be0c0506111",
    "split-dataset.json":"1d373b3652bf03027a1e23c45e2fc117895015640193b49f9c38f07099a1ae7a",
    "trained-models.pt":"102102b1f7318ca1fc720afda96c9118a526ea48eb007ef8ed76bfa586dca9aa",
    "validation-summary.json":"389555ca1313aa86e3635a28397ac98613206373b9b6bbe15eaf1e69a2889917",
}
DATA_SHA = "72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85"
SPLIT_SHA = "9b5cc13cfe9dc9a139f23c44d87397f2af4f1174f1a9cf0fb4659d6ddfcad0b0"
MANIFEST_SHA = "8088155ef7ba95eb47a8a7ae3790247ff20d61804ac08c7fc1b1ed2f0c645760"
SEEDS, FAMILIES = (234001,234002,234003), ("full","gru_only")
VIEWS, SPLITS = ("normal","evidence_blind","query_blind"), ("TRAIN","HOLDOUT")
TRAIN_PAIRS = ((0,1),(1,0),(2,3),(3,2))
ROWS = {"TRAIN":32,"HOLDOUT":64}
STEPS, BATCH, LR, CLIP, TOL = 400,32,0.005,1.0,1e-9
OWN = ("fold_lm/v05_benchmarks/model_c242_balanced_recombination.py",
    "tests_lm/test_v05_c242_balanced_recombination.py","tools/run_c242.ps1","tools/invoke_c242.ps1",
    "docs/experiment-ledger-addendum-c242-preregistration.md","docs/v5b-balanced-recombination-v0.1.md")
OUTPUTS = {"recombination-plan.json","split-dataset.json","trained-models.pt","measurements.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c241_assignment_holdout as parent
    return parent


def context():
    parent=parent_module()
    _,_,binding,factory,audit=parent.context()
    return parent,binding,factory,audit


def identities(): return list(itertools.product(SEEDS,FAMILIES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        source_dataset_sha256=DATA_SHA,split_sha256=SPLIT_SHA,train_pairs=[list(p) for p in TRAIN_PAIRS],
        selection="C234 objects[0,1]; TRAIN four ordered pairs; HOLDOUT other eight distinct ordered pairs",
        identities=[list(x) for x in identities()],rows=ROWS,views=list(VIEWS),
        initial_state="fresh; exact C241 initial_sha256; never load trained parent state",
        parameters=dict(full=13488,gru_only=10160),width=16,slots=48,
        steps=STEPS,batch=BATCH,batch_indices=list(range(32)),lr=LR,clip=CLIP,optimizer="AdamW",
        betas=[.9,.999],eps=1e-8,weight_decay=0.0,precision="CPU float64",threads=2,deterministic=True,
        train_steps=2400,answer_presentations=76800,evaluation_forwards=90,
        model_forward_calls=2490,row_presentations=80832,checkpoint_writes=1,
        evaluation="initial TRAIN; final TRAIN/HOLDOUT at step400; reload both; three views each",
        metric_gate=dict(accuracy=.90,fact_pair=.80,query_pair=.80,order_pair=.80,evidence_drop=.35,query_drop=.35),
        primary="all Full split/seed/language cells; GRU-only separately",
        masked_input_ceilings=dict(evidence_blind=.25,query_blind=.50),
        query_only_ceiling=.25,fixed_position_accuracy=.50,
        source_pins=298,protected_inputs=454,direct_dependencies=18,own_tests=24,
        modules=127,loaded_tests=2978,focused_tests=2977,excluded_test=EXCLUDED,
        replay_tolerance=TOL,network_calls=0,gate_f_candidate=False,
        general_language_claim=False,unseen_vocabulary_claim=False,core_superiority_claim=False)


def input_ceiling(rows,key):
    groups=defaultdict(Counter)
    for r in rows: groups[key(r)][r["target"]]+=1
    return sum(max(c.values()) for c in groups.values())/len(rows)


def split_data(data,binding):
    binding.validate_dataset(data)
    require(digest(data)==DATA_SHA,"source dataset identity")
    pool=[r for r in data if r["objects"]==[0,1]]
    parts={"TRAIN":[r for r in pool if tuple(r["values"]) in TRAIN_PAIRS],
           "HOLDOUT":[r for r in pool if tuple(r["values"]) not in TRAIN_PAIRS]}
    require(digest(parts)==SPLIT_SHA,"split identity")
    for split,rows in parts.items():
        require(len(rows)==ROWS[split] and len({r["id"] for r in rows})==len(rows),"split size/IDs")
        count=len(rows)//32
        require(Counter((r["language"],r["query"],r["order"],r["target"]) for r in rows)==
            {k:count for k in itertools.product(("en","ja"),(0,1),(0,1),range(48,52))},"joint factor balance")
        require(all(r["prompt"]==binding.render(r) for r in rows),"unchanged renderer")
        require(input_ceiling(rows,lambda r:(r["language"],r["query"]))==.25,"query-only ceiling")
        for mode,wanted in (("evidence_blind",.25),("query_blind",.5)):
            require(input_ceiling(rows,lambda r:binding.render(r,mode))==wanted,"masked input ceiling")
        fixed=sum(48+(r["values"] if r["order"]==0 else r["values"][::-1])[r["query"]]==r["target"] for r in rows)
        require(fixed/len(rows)==.5,"fixed-position control")
    for key in ("id","prompt","group"):
        require(not {r[key] for r in parts["TRAIN"]}&{r[key] for r in parts["HOLDOUT"]},"split overlap")
    return parts


def balanced_indices(count):
    require(type(count) is int and count==32,"C242 requires32 TRAIN rows")
    return torch.arange(count,dtype=torch.int64)


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
        if (step+1)%100==0:print(f"[C242] seed={seed} step={step+1}/{steps} answer_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=steps,answer_presentations=steps*BATCH,first_loss=first,last_loss=last,
                fit_seconds=time.perf_counter()-started)


def audit_fit_contract(parent):
    class Labels(ast.NodeTransformer):
        def visit_Constant(self,node):
            if isinstance(node.value,str): node.value=node.value.replace("[C241]","[C242]")
            return node
    require(ast.dump(Labels().visit(ast.parse(inspect.getsource(parent.fit))),include_attributes=False)==
            ast.dump(ast.parse(inspect.getsource(fit)),include_attributes=False),"fit AST drift")
    require(all(getattr(parent,k)==globals()[k] for k in ("STEPS","BATCH","LR","CLIP","TOL")),"fit constants")


def prediction_record(logits,n):
    require(len(logits)==3 and all(x.shape==(n,256) and bool(torch.isfinite(x).all()) for x in logits),"logit schema")
    return {v:x.argmax(-1).tolist() for v,x in zip(VIEWS,logits,strict=True)}


def validate_metrics(value,n):
    rates=("accuracy","evidence_blind_accuracy","query_blind_accuracy","fact_pair_accuracy","query_pair_accuracy","order_pair_accuracy")
    require(set(value)=={"en","ja"},"metric languages")
    for m in value.values():
        require(set(m)==set(rates)|{"rows","answer_nll","evidence_drop","query_drop"} and m["rows"]==n//2,"metric schema/count")
        require(all(type(v) in (int,float) and math.isfinite(v) for v in m.values()),"nonfinite metric")
        require(all(0<=m[k]<=1 for k in rates) and m["answer_nll"]>=0,"metric range")
        for k in ("evidence","query"):
            require(abs(m[k+"_drop"]-m["accuracy"]+m[k+"_blind_accuracy"])<=TOL,"mask drop")


def evaluate(model,rows,binding,fingerprint):
    before=fingerprint(model); views=[binding.tensors(rows,v) for v in VIEWS]
    metrics,logits=binding.evaluate(model,rows,views)
    pred=prediction_record(logits,len(rows))["normal"]
    for lang in ("en","ja"):
        groups=defaultdict(list)
        for i,r in enumerate(rows):
            if r["language"]==lang: groups[(r["group"],r["query"])].append(i)
        require(len(groups)==len(rows)//4 and all(len(g)==2 and rows[g[0]]["target"]==rows[g[1]]["target"] for g in groups.values()),"order pair contract")
        metrics[lang]["order_pair_accuracy"]=sum(all(pred[i]==rows[i]["target"] for i in g) for g in groups.values())/len(groups)
    validate_metrics(metrics,len(rows)); require(fingerprint(model)==before,"evaluation mutation")
    return metrics,logits


def cell_pass(m):
    return (m["accuracy"]>=.90 and all(m[k+"_pair_accuracy"]>=.80 for k in ("fact","query","order"))
        and m["evidence_drop"]>=.35 and m["query_drop"]>=.35)


def train_one(model,parts,reference,*,binding,factory):
    before=factory.fingerprint(model); require(before==reference["initial_sha256"],"fresh initial identity")
    counts=[0,0]
    def hook(module,args,output): counts[0]+=1; counts[1]+=len(args[0])
    handle=model.register_forward_hook(hook)
    try:
        initial,_=evaluate(model,parts["TRAIN"],binding,factory.fingerprint)
        trained=fit(model,*binding.tensors(parts["TRAIN"],"normal"),reference["seed"])
        final={};raw={}
        for split in SPLITS: final[split],raw[split]=evaluate(model,parts[split],binding,factory.fingerprint)
    finally: handle.remove()
    after=factory.fingerprint(model);require(before!=after and counts==[409,13184],"training update/count")
    record=dict(seed=reference["seed"],family=reference["family"],initial_sha256=before,final_sha256=after,
        initial_train=initial,final=final,fit=trained,forward_calls=counts[0],row_presentations=counts[1],weights_changed=True,
        predictions={s:prediction_record(raw[s],ROWS[s]) for s in SPLITS})
    return record,{k:v.detach().cpu().clone() for k,v in model.state_dict().items()},raw


def replay_one(model,state,record,raw,parts,*,binding,factory):
    model.load_state_dict(state,strict=True);model.eval()
    require(factory.fingerprint(model)==record["final_sha256"],"reload fingerprint")
    counts=[0,0];error=0.0
    def hook(module,args,output): counts[0]+=1;counts[1]+=len(args[0])
    handle=model.register_forward_hook(hook)
    try:
        for split in SPLITS:
            metrics,logits=evaluate(model,parts[split],binding,factory.fingerprint)
            error=max(error,*(float((x-y).abs().max()) for x,y in zip(logits,raw[split],strict=True)),
                *(abs(metrics[l][k]-record["final"][split][l][k]) for l in metrics for k in metrics[l]))
            require(prediction_record(logits,ROWS[split])==record["predictions"][split],"prediction replay")
    finally: handle.remove()
    require(error<=TOL and counts==[6,288],"reload error/count")
    record.update(checkpoint_roundtrip=True,prediction_replayed=True,reload_max_error=error,
        forward_calls=record["forward_calls"]+6,row_presentations=record["row_presentations"]+288)


def load_bundle(path):
    data=torch.load(path,map_location="cpu",weights_only=True)
    require(data["schema"]=="fold-c242-recombination-v1" and data["identities"]==[list(x) for x in identities()] and len(data["states"])==6,"bundle schema")
    return data["states"]


def summarize(records):
    require([(r["seed"],r["family"]) for r in records]==identities(),"record order")
    gates={f:True for f in FAMILIES}; labels=Counter()
    for r in records:
        require(set(r["final"])==set(SPLITS),"split metrics")
        for s in SPLITS: validate_metrics(r["final"][s],ROWS[s])
        for l in ("en","ja"):
            train=cell_pass(r["final"]["TRAIN"][l]);held=cell_pass(r["final"]["HOLDOUT"][l])
            labels["TRAIN_CRITERIA_MISS" if not train else "RECOMBINATION_MISS" if not held else "BOTH_PASS"]+=1
            gates[r["family"]]&=train and held
    return dict(models=6,full_recombination_gate=gates["full"],gru_recombination_gate=gates["gru_only"],cell_outcomes=dict(labels),
        all_replays=all(r["checkpoint_roundtrip"] is True and r["prediction_replayed"] is True and 0<=r["reload_max_error"]<=TOL for r in records),
        all_weights_changed=all(r["weights_changed"] is True for r in records),
        train_steps=sum(r["fit"]["steps"] for r in records),answer_presentations=sum(r["fit"]["answer_presentations"] for r in records),
        model_forward_calls=sum(r["forward_calls"] for r in records),row_presentations=sum(r["row_presentations"] for r in records),
        general_language_claim=False,unseen_vocabulary_claim=False,core_superiority_claim=False)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(298,454) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"artifacts")
    s=p["validation_summary"]
    require((s["models"],s["train_steps"],s["answer_presentations"],s["model_forward_calls"],s["row_presentations"])==(6,2400,76800,2490,80832),"workload")
    require(s["all_replays"] is True and s["all_weights_changed"] is True and sum(s["cell_outcomes"].values())==12,"integrity")
    require(type(s["full_recombination_gate"]) is bool and type(s["gru_recombination_gate"]) is bool
        and p["status"]==("PASS" if s["full_recombination_gate"] else "FAIL"),"scientific status")
    require(p["gate_f_candidate"] is False and p["network_calls"]==0
        and all(s[k] is False for k in ("general_language_claim","unseen_vocabulary_claim","core_superiority_claim")),"claim scope")


def precheck(c241_summary,c234_dataset,root):
    parent,_,factory,a=context();root=Path(root);path=Path(c241_summary).resolve();data=Path(c234_dataset).resolve()
    require(a.sha(path)==PARENT_SHA,"parent summary hash");p=a.read_json(path);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL" and p["validation_summary"]["cell_outcomes"]=={"TRAIN_FIT_MISS":12},"accepted parent")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items():require(Path(name).is_file() and a.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items():require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    require(protected.get(str(data))==DATA_SHA and a.sha(data)==DATA_SHA,"C234 dataset protection")
    require(str(path) not in protected,"parent duplicate");protected[str(path)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifact identities")
    for item in p["artifacts"]:
        child=a.safe_child(path.parent,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"parent bytes")
        require(str(child.resolve()) not in protected,"artifact duplicate");protected[str(child.resolve())]=item["sha256"]
    for name in OWN:
        require(name not in pins,"OWN collision");pins[name]=a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    # All earlier deciding-path helpers must remain inherited, not reconstructed after execution.
    deps=set(factory.LM_SOURCES)|{OWN[0]}|{"fold_lm/v05_benchmarks/"+name for name in (
        "gate_f_c230_prepared_capsule.py","model_c231_byte_eval_contract.py","model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py","model_c234_context_binding.py","model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py","model_c237_frozen_signal_audit.py","model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py","model_c240_saved_position_audit.py","model_c241_assignment_holdout.py")}
    require(len(deps)==18 and deps<=set(pins),"direct dependencies")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(298,454) and digest(manifest())==MANIFEST_SHA,"counts/manifest")
    audit_fit_contract(parent)
    return pins,protected


def load_inputs(c241_summary,c234_dataset):
    parent,binding,_,a=context();path=Path(c241_summary).resolve()
    parts=split_data(a.read_json(c234_dataset),binding);records=a.read_json(path.parent/"measurements.json")
    require(parent.summarize(records)==a.read_json(path)["validation_summary"],"parent measurement summary")
    require([(r["seed"],r["family"]) for r in records]==identities(),"parent identities")
    for r in records:
        h=r["initial_sha256"]
        require(isinstance(h,str) and len(h)==64 and all(c in "0123456789abcdef" for c in h) and h!=r["final_sha256"],"initial field semantics")
    return parts,records


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==126,"parent modules")
    return names+["tests_lm.test_v05_c242_balanced_recombination"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests];require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"test identities")
    kept=[t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(2978,2977),"suite counts")
    return unittest.TestSuite(kept)


def run(*,c241_summary,c234_dataset,output_dir,expected_head):
    _,binding,factory,a=context();root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"execution HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c241_summary,c234_dataset,root);parts,parents=load_inputs(c241_summary,c234_dataset)
    records=[];states=[];raw=[];out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for seed in SEEDS:
        full=factory.new_model(seed);baseline=binding.parent_module().new_baseline(full)
        require((sum(p.numel() for p in full.parameters()),sum(p.numel() for p in baseline.parameters()))==(13488,10160),"model sizes")
        for family,model in (("full",full),("gru_only",baseline)):
            ref=parents[len(records)];require((ref["seed"],ref["family"])==(seed,family),"paired initial identity")
            print(f"[C242] model={len(records)+1}/6 seed={seed} family={family}; balanced TRAIN32",flush=True)
            record,state,outputs=train_one(model,parts,ref,binding=binding,factory=factory)
            records.append(record);states.append(state);raw.append(outputs)
    torch.save(dict(schema="fold-c242-recombination-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for r,state,outputs in zip(records,load_bundle(out/"trained-models.pt"),raw,strict=True):
        model=factory.new_model(r["seed"])
        if r["family"]=="gru_only":model=binding.parent_module().new_baseline(model)
        replay_one(model,state,r,outputs,parts,binding=binding,factory=factory)
    summary=summarize(records)
    for name,value in (("recombination-plan.json",manifest()),("split-dataset.json",parts),("measurements.json",records),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard();precheck(c241_summary,c234_dataset,root)
    for name,wanted in protected.items():require(a.sha(name)==wanted,"modified input")
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["full_recombination_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,gate_f_candidate=False,network_calls=0,
        limitations=["Fixed two-entity four-value task, not general language or core superiority.",
            "New split/coverage/repetitions; not a single-variable causal comparison to C241.",
            "Fresh models; source labels are provenance, not current optimizer membership."])
    validate_result(result);(out/"summary.json").write_bytes(blob(result));print("=== C242 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
    return result


def verify_artifacts(output_dir,c241_summary,c234_dataset,expected_head):
    _,_,_,a=context();out=Path(output_dir);p=a.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():require(a.sha(name)==wanted,"postcheck input")
    for item in p["artifacts"]:
        path=a.safe_child(out,item["file"]);require(a.sha(path)==item["sha256"] and path.stat().st_size==item["serialized_bytes"],"postcheck artifact")
    records=a.read_json(out/"measurements.json")
    require(summarize(records)==p["validation_summary"]==a.read_json(out/"validation-summary.json"),"saved summary")
    require(a.read_json(out/"recombination-plan.json")==manifest(),"saved plan")
    parts,parents=load_inputs(c241_summary,c234_dataset)
    require(a.read_json(out/"split-dataset.json")==parts,"saved split")
    for r,ref in zip(records,parents,strict=True):require(r["initial_sha256"]==ref["initial_sha256"],"saved initial ID")
    return p,records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("c241-summary","c234-dataset","output-dir"):parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True);run(**vars(parser.parse_args()))


if __name__=="__main__":main()
