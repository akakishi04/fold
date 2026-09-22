"""C234: controlled EN/JA context binding, with the unchanged full and GRU-only models.

Answer-only learning and paired fact/query controls, not a general language benchmark.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import time
import unittest

import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C234-v5b-contextual-binding-pilot"
STAGE = "V5-B-CONTEXTUAL-BINDING-PILOT"
BASE = "3d3f6ad6f9903085ca083fbfc77bf0d4d77a93d7"
PARENT_EXECUTION = "fedf6c3e5c163d449d1ad793a87d4fa6952deb1d"
PARENT_SHA = "5e9895008ebf02c72c3b5c00a8668f1c8078feef94dd2fc1eff192d41e8709bf"
PARENT_VALIDATION_SHA = "c839db0ed26f0369dcedb6227ae5278ca60904d8636da0d00e49da02d75998e4"
DATA_SHA = "72e2f07dc12e9f7e538e2bdd08e3a738d423cd536d1e509301363e467ef26c85"
MANIFEST_SHA = "0c3c3cedd0a15fa8b392cbe38ba5285113a948b78ef3511bf106cbc75d7b2d38"
OBJECTS = {"en": ("box", "book", "ball", "umbrella"), "ja": ("箱", "本", "玉", "傘")}
EVAL_PAIRS = ((0, 3), (1, 2))
SEEDS = (234001, 234002, 234003)
FAMILIES = ("full", "gru_only")
STEPS, BATCH, LR, CLIP, TOL = 400, 32, 0.005, 1.0, 1e-9
OWN = (
    "fold_lm/v05_benchmarks/model_c234_context_binding.py",
    "tests_lm/test_v05_c234_context_binding.py",
    "tools/run_c234.ps1", "tools/invoke_c234.ps1",
    "docs/experiment-ledger-addendum-c234-preregistration.md",
    "docs/v5b-contextual-binding-v0.1.md",
)
OUTPUTS = {"binding-plan.json", "dataset.json", "trained-models.pt", "measurements.json", "validation-summary.json"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c233_core_ablation as parent
    return parent


def factory_module():
    return parent_module().parent_module().parent_module()


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
        parent_validation_sha256=PARENT_VALIDATION_SHA, data_sha256=DATA_SHA,
        objects={k:list(v) for k,v in OBJECTS.items()}, eval_value_pairs=[list(x) for x in EVAL_PAIRS],
        rows=576, train_rows=384, eval_rows=192, train_binding_groups=48, eval_binding_groups=24,
        families=list(FAMILIES), seeds=list(SEEDS), parameters=dict(full=13488,gru_only=10160),
        initialization="fresh full model and exact common-weight GRU copy before either trains",
        sampling="TRAIN rows only; CPU generator seed+1000, shared order per paired family",
        steps_per_model=STEPS, batch_size=BATCH, lr=LR, clip_norm=CLIP,
        optimizer="AdamW", betas=[0.9,0.999], eps=1e-8, weight_decay=0.0,
        total_training_steps=2400, total_answer_presentations=76800,
        dtype="float64", device="cpu", threads=2, deterministic_algorithms=True,
        score="unconstrained argmax over256 real bytes; exactly the requested ASCII digit",
        controls=["mask both observed values", "mask queried object"],
        primary="all full-model seeds satisfy both-language binding criteria",
        min_eval_accuracy=0.90, min_fact_pair_accuracy=0.80, min_query_pair_accuracy=0.80,
        min_evidence_drop=0.35, min_query_drop=0.35, replay_tolerance=TOL,
        baseline="same criteria reported independently; no superiority gate or matched capacity claim",
        selection="step400 only; no held-out tuning, early stop or replacement seeds",
        learned_memory_used=False, general_language_claim=False, gate_f_candidate=False)


def render(row, mode="normal"):
    require(mode in ("normal","evidence_blind","query_blind"), "unknown view")
    names=OBJECTS[row["language"]]; a,b=row["objects"]; x,y=row["values"]
    facts=[(a,x),(b,y)]
    if row["order"]: facts.reverse()
    text=";".join(names[k]+"="+("?" if mode=="evidence_blind" else str(v)) for k,v in facts)
    query="?" if mode=="query_blind" else names[row["query"]]
    return text+";"+query+"="


def dataset():
    rows=[]
    for a,b in itertools.combinations(range(4),2):
        for x,y in itertools.permutations(range(4),2):
            group=f"{a}-{b}-{x}-{y}"
            split="EVAL" if tuple(sorted((x,y))) in EVAL_PAIRS else "TRAIN"
            for language in OBJECTS:
                for order,query in itertools.product((0,1),(a,b)):
                    row=dict(id=f"{language}-{group}-{order}-{query}", group=group,
                        objects=[a,b], values=[x,y], language=language, order=order,
                        query=query, split=split, target=ord(str(x if query==a else y)))
                    row["prompt"]=render(row); rows.append(row)
    return rows


def validate_dataset(rows):
    require(digest(rows)==DATA_SHA, "binding dataset changed")
    train=[r for r in rows if r["split"]=="TRAIN"]; ev=[r for r in rows if r["split"]=="EVAL"]
    require((len(rows),len(train),len(ev))==(576,384,192),"split counts")
    tg={r["group"] for r in train}; eg={r["group"] for r in ev}
    require(len(tg)==48 and len(eg)==24 and not tg&eg,"group split")
    require(len({r["id"] for r in rows})==576,"row identity")
    for part in (train,ev):
        for lang in OBJECTS:
            subset=[r for r in part if r["language"]==lang]
            require(Counter(r["target"] for r in subset)=={i:len(subset)//4 for i in range(48,52)},"target balance")
    require(all(len(r["prompt"].encode())<=46 and r["prompt"]==render(r) for r in rows),"prefix format")
    return train,ev


def tensors(rows, mode="normal"):
    require(rows,"empty rows")
    factory=factory_module()
    return (torch.stack([factory.prefix_tensor(render(r,mode).encode()) for r in rows]),
            torch.tensor([r["target"] for r in rows],dtype=torch.int64))


def paired_accuracy(rows, predictions, kind):
    require(kind in ("facts","query") and len(rows)==len(predictions),"pair inputs")
    groups=defaultdict(list)
    for row,pred in zip(rows,predictions,strict=True):
        if kind=="facts":
            key=(tuple(row["objects"]),tuple(sorted(row["values"])),row["language"],row["order"],row["query"])
        else:
            key=(row["group"],row["language"],row["order"])
        groups[key].append((row["target"],pred))
    require(groups and all(len(g)==2 and g[0][0]!=g[1][0] for g in groups.values()),"invalid matched pairs")
    return sum(all(target==pred for target,pred in group) for group in groups.values())/len(groups)


def metrics(rows, predictions, evidence, query, logits, targets):
    require(len(rows)==len(predictions)==len(evidence)==len(query),"prediction count")
    loss=F.cross_entropy(logits,targets,reduction="none")
    require(bool(torch.isfinite(loss).all()),"nonfinite evaluation loss")
    out={}
    for lang in OBJECTS:
        ids=[i for i,r in enumerate(rows) if r["language"]==lang]
        require(ids,"missing language")
        part=[rows[i] for i in ids]; pred=[predictions[i] for i in ids]
        acc=sum(predictions[i]==rows[i]["target"] for i in ids)/len(ids)
        ea=sum(evidence[i]==rows[i]["target"] for i in ids)/len(ids)
        qa=sum(query[i]==rows[i]["target"] for i in ids)/len(ids)
        out[lang]=dict(rows=len(ids),accuracy=acc,answer_nll=float(loss[ids].mean()),
            evidence_blind_accuracy=ea,query_blind_accuracy=qa,
            evidence_drop=acc-ea,query_drop=acc-qa,
            fact_pair_accuracy=paired_accuracy(part,pred,"facts"),
            query_pair_accuracy=paired_accuracy(part,pred,"query"))
    return out


def evaluate(model,rows,views):
    training=model.training; model.eval(); outputs=[]
    try:
        with torch.no_grad():
            for tokens,_ in views:
                logits=model(tokens,torch.zeros(len(tokens),dtype=torch.int64))
                require(logits.shape==(len(rows),256) and bool(torch.isfinite(logits).all()),"bad model logits")
                outputs.append(logits.detach())
    finally: model.train(training)
    preds=[x.argmax(-1).tolist() for x in outputs]
    return metrics(rows,*preds,outputs[0],views[0][1]),outputs


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
        if (step+1)%100==0:print(f"[C234] seed={seed} step={step+1}/{steps} answer_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=steps,answer_presentations=steps*BATCH,first_loss=first,last_loss=last,
                fit_seconds=time.perf_counter()-started)


def binding_pass(record):
    require(set(record["final_eval"])==set(OBJECTS), "missing language metrics")
    for values in record["final_eval"].values():
        require(values["rows"]==96, "EVAL subgroup count")
        for key in ("accuracy","answer_nll","evidence_blind_accuracy","query_blind_accuracy",
                    "evidence_drop","query_drop","fact_pair_accuracy","query_pair_accuracy"):
            value=values[key]
            require(type(value) in (int,float) and math.isfinite(value), "invalid metric")
        require(all(0<=values[k]<=1 for k in ("accuracy","evidence_blind_accuracy",
                    "query_blind_accuracy","fact_pair_accuracy","query_pair_accuracy")), "invalid rate")
    return all(v["accuracy"]>=0.90 and v["fact_pair_accuracy"]>=0.80
        and v["query_pair_accuracy"]>=0.80 and v["evidence_drop"]>=0.35
        and v["query_drop"]>=0.35 for v in record["final_eval"].values())


def summarize(records):
    require([(r["seed"],r["family"]) for r in records]==list(itertools.product(SEEDS,FAMILIES)),"record order")
    return dict(seeds=list(SEEDS),models=6,
        full_binding_gate=all(binding_pass(r) for r in records if r["family"]=="full"),
        gru_binding_gate=all(binding_pass(r) for r in records if r["family"]=="gru_only"),
        all_replays=all(r["checkpoint_roundtrip"] and r["prediction_replayed"]
                       and 0<=r["reload_max_error"]<=TOL for r in records),
        all_weights_changed=all(r["weights_changed"] for r in records),
        total_training_steps=sum(r["fit"]["steps"] for r in records),
        total_answer_presentations=sum(r["fit"]["answer_presentations"] for r in records),
        general_language_claim=False,core_superiority_claim=False)


def gate(s):
    return (s.get("full_binding_gate") is True and s.get("all_replays") is True
        and s.get("all_weights_changed") is True and s.get("total_training_steps")==2400
        and s.get("total_answer_presentations")==76800 and s.get("models")==6)


def precheck(c233_summary,root):
    parent=parent_module(); a=parent.parent_module().audit_module(); root=Path(root)
    require(a.sha(c233_summary)==PARENT_SHA,"parent summary changed")
    p=a.read_json(c233_summary);parent.validate_result(p)
    s=p["validation_summary"]
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL"
            and s["baseline_qualified"] is True and s["all_replays"] is True
            and (s["full_win_cells"],s["baseline_win_cells"],s["tied_cells"])==(3,3,0),"wrong accepted negative")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    require((len(pins),len(protected))==(244,346),"parent protection counts")
    for name,wanted in protected.items():require(Path(name).is_file() and a.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items():require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    protected[str(Path(c233_summary).resolve())]=PARENT_SHA; seen=False
    for item in p["artifacts"]:
        path=a.safe_child(Path(c233_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path)==item["sha256"] and path.stat().st_size==item["serialized_bytes"],"changed artifact")
        protected[str(path.resolve())]=item["sha256"]
        if item["file"]=="validation-summary.json":
            require(item["sha256"]==PARENT_VALIDATION_SHA,"parent validation");seen=True
    require(seen,"missing parent validation")
    for name in OWN:
        require(name not in pins,"OWN collision");pins[name]=a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    deps=set(factory_module().LM_SOURCES)|{OWN[0],
        "fold_lm/v05_benchmarks/model_c233_core_ablation.py",
        "fold_lm/v05_benchmarks/model_c232_bilingual_learning.py",
        "fold_lm/v05_benchmarks/model_c231_byte_eval_contract.py",
        "fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"}
    require(len(deps)==10 and deps<=set(pins),"missing direct dependency")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(250,358),"C234 protection counts")
    require(digest(manifest())==MANIFEST_SHA,"manifest drift")
    return p,pins,protected


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==118,"parent module count")
    return names+["tests_lm.test_v05_c234_context_binding"]


def regression_suite(root):
    p=factory_module().parent_module(); helper=p.context(p.parent_module()).backend.c205
    tests=list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests];excluded=helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
    require(all(ids.count(x)==1 for x in excluded),"historical exclusion")
    kept=[t for t in tests if t.id() not in excluded]
    require((len(tests),len(kept))==(2786,2785),"C234 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(250,358) and set(OWN)<=set(p["source_blobs"]),"result protection")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"outputs")
    s=p["validation_summary"]
    require(s["seeds"]==list(SEEDS) and s["models"]==6 and s["all_replays"] is True
            and (s["total_training_steps"],s["total_answer_presentations"])==(2400,76800),"incomplete workload or replay")
    require(p["status"]==("PASS" if gate(s) else "FAIL"),"verdict drift")
    require(p["gate_f_candidate"] is False and p["network_calls"]==0,"scope drift")


def run(*,c233_summary,output_dir,expected_head):
    parent=parent_module();factory=factory_module();a=parent.parent_module().audit_module()
    root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    _,pins,protected=precheck(c233_summary,root)
    data=dataset();train,ev=validate_dataset(data);tx,ty=tensors(train)
    views=[tensors(ev,mode) for mode in ("normal","evidence_blind","query_blind")]
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    records=[];states=[];originals=[]
    for seed in SEEDS:
        full=factory.new_model(seed);baseline=parent.new_baseline(full)
        for family,model in (("full",full),("gru_only",baseline)):
            require(sum(v.numel() for v in model.parameters())==manifest()["parameters"][family],"model size")
            before=factory.fingerprint(model);initial,_=evaluate(model,ev,views)
            print(f"[C234] family={family} seed={seed}",flush=True)
            trained=fit(model,tx,ty,seed)
            final,logits=evaluate(model,ev,views);after=factory.fingerprint(model)
            records.append(dict(seed=seed,family=family,initial_eval=initial,final_eval=final,
                initial_sha256=before,final_sha256=after,weights_changed=before!=after,fit=trained,
                predictions={mode:v.argmax(-1).tolist() for mode,v in zip(("normal","evidence_blind","query_blind"),logits,strict=True)}))
            states.append({k:v.detach().clone() for k,v in model.state_dict().items()});originals.append(logits)
    checkpoint=out/"trained-models.pt"
    torch.save(dict(schema="fold-c234-binding-v1",identities=[[r["seed"],r["family"]] for r in records],states=states),checkpoint)
    bundle=torch.load(checkpoint,map_location="cpu",weights_only=True)
    require(bundle["schema"]=="fold-c234-binding-v1" and bundle["identities"]==[list(x) for x in itertools.product(SEEDS,FAMILIES)],"checkpoint identity")
    for row,state,original in zip(records,bundle["states"],originals,strict=True):
        model=factory.new_model(row["seed"])
        if row["family"]=="gru_only":model=parent.new_baseline(model)
        model.load_state_dict(state,strict=True);model.eval();_,actual=evaluate(model,ev,views)
        row["checkpoint_roundtrip"]=factory.fingerprint(model)==row["final_sha256"]
        row["reload_max_error"]=max(float((x-y).abs().max()) for x,y in zip(actual,original,strict=True))
        row["prediction_replayed"]=all(torch.equal(x.argmax(-1),y.argmax(-1)) for x,y in zip(actual,original,strict=True))
    summary=summarize(records)
    for name,value in (("binding-plan.json",manifest()),("dataset.json",data),("measurements.json",records),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard();precheck(c233_summary,root)
    for name,wanted in protected.items():require(a.sha(name)==wanted,"modified input:"+name)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        diagnostic_execution_valid=True,status="PASS" if gate(summary) else "FAIL",source_blobs=pins,
        input_sha256=protected,artifacts=artifacts,validation_summary=summary,gate_f_candidate=False,network_calls=0,
        limitations=["small symbolic textual bindings; not general language or reasoning",
                     "full and GRU-only have unequal capacity/compute; no superiority claim",
                     "new task after observed negative; not a retrospective rescue of C233",
                     "no learned memory, joint runtime, larger model or external corpus"])
    validate_result(result);(out/"summary.json").write_bytes(blob(result))
    print("=== C234 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("c233-summary","output-dir"):p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))


if __name__=="__main__":main()
