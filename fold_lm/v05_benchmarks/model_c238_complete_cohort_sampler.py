"""C238: change only C236 batch selection; fit the same16 seen TRAIN rows."""
from __future__ import annotations
import argparse
import ast
import copy
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

EXPERIMENT_ID = "C238-v5b-complete-cohort-sampler"
STAGE = "V5-B-COMPLETE-COHORT-SAMPLER"
BASE = "6c3d4150f42cd43592b5c5a1ef1c18dab9396270"
PARENT_EXECUTION = "2dec1314181d62fbdf0a7d4c52007a9360921fd2"
PARENT_SHA = "056fcbe4ebd2f888c0d5d5aa2761a18cd4229ed4af428e8e298d7af3abf55b32"
PARENT_ARTIFACTS = {
    "contrasts.json": "3449be022b490fb8c67bf47f688e68d9d7b277e235399e671acc2f61aebcb85f",
    "diagnostic-plan.json": "1e5ab23f80a3cf2b510ce82bdd9f343b53716a6dc9641eb9b09ae6dd165c06ce",
    "diagnostics.json": "87c37f0b645b0740cd2202c6d85a56a4d1164c5580c6eaa04036501f83627b70",
    "traces.json": "eee07984fb62d83d1114ffa9476ab410257646dcb61a9c8096c21eb15a0063e0",
    "validation-summary.json": "066206986d83833a759d1e36d8d1efd5aab4b95c0693b32c3935b1d9baf06d9f",
}
COMPARATOR_EXECUTION = "0bc91722ca27803f065d2458505b502a2d01e50f"
COMPARATOR_SHA = "0e8628e048cc34e5b43104c0228c65fe18baee216c295223b0caa14c827327ec"
PROBE_SHA = "bc80e9ea2607ae1e99b2b1da3bb85d5f20ba9dc4b103e67176428f9703a9f52c"
SEEDS, FAMILIES = (234001,234002,234003), ("full","gru_only")
VIEWS = ("normal","evidence_blind","query_blind")
STEPS, BATCH, LR, CLIP, TOL = 400,32,0.005,1.0,1e-9
OWN = (
    "fold_lm/v05_benchmarks/model_c238_complete_cohort_sampler.py",
    "tests_lm/test_v05_c238_complete_cohort_sampler.py",
    "tools/run_c238.ps1", "tools/invoke_c238.ps1",
    "docs/experiment-ledger-addendum-c238-preregistration.md",
    "docs/v5b-complete-cohort-sampler-v0.1.md",
)
OUTPUTS = {"sampler-plan.json","probe-dataset.json","trained-models.pt","measurements.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "ae9d0b7e92ee7024b57210f1779aebbfc0757fa995acbdf6f9359b2f23664232"


def require(condition,message):
    if not condition: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c237_frozen_signal_audit as parent
    return parent


def context():
    parent=parent_module()
    fitting,binding,factory,audit=parent.context()
    return parent,fitting,binding,factory,audit


def identities():
    return list(itertools.product(SEEDS,FAMILIES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        comparator_execution=COMPARATOR_EXECUTION,comparator_sha256=COMPARATOR_SHA,
        comparator="accepted C236 recorded measurements; no comparator retraining",
        cohort_sha256=PROBE_SHA,train_rows=16,languages=["en","ja"],views=list(VIEWS),
        identities=[list(x) for x in identities()],parameters=dict(full=13488,gru_only=10160),
        initialization="fresh; initial_sha256 and initial_probe must match C236; common copy before fit",
        changed="one batch-index assignment: replacement sampling to complete cohort twice",
        batch_indices=list(range(16))*2,row_presentations_per_model=[800]*16,
        steps_per_model=STEPS,batch_size=BATCH,optimizer="AdamW",lr=LR,clip_norm=CLIP,
        betas=[0.9,0.999],eps=1e-8,weight_decay=0.0,
        total_training_steps=2400,total_answer_presentations=76800,
        evaluation_forward_calls=54,model_forward_calls=2454,total_row_presentations=77664,
        checkpoint_writes=1,held_out_evaluation_rows=0,network_calls=0,
        dtype="float64",device="cpu",threads=2,deterministic_algorithms=True,
        final_step=400,accuracy_threshold=.90,fact_pair_threshold=.80,query_pair_threshold=.80,
        evidence_drop_threshold=.35,query_drop_threshold=.35,replay_tolerance=TOL,
        primary="all Full seed/language cells pass C236 probe gate",baseline="GRU-only gate separately",
        source_pins=274,protected_inputs=406,direct_dependencies=14,own_tests=24,
        modules=123,loaded_tests=2882,focused_tests=2881,excluded_test=EXCLUDED,
        general_language_claim=False,held_out_generalization_claim=False,gate_f_candidate=False)


def balanced_indices(count):
    require(type(count) is int and count==16,"complete-cohort sampler requires16 rows")
    return torch.arange(count,dtype=torch.int64).repeat(2)


# The unused generator initialization is retained to make the sole executable change
# against accepted C236.fit the ids assignment. No random sample is drawn from it.
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
        if (step+1)%100==0:print(f"[C238] seed={seed} step={step+1}/{steps} answer_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=steps,answer_presentations=steps*BATCH,first_loss=first,last_loss=last,
                fit_seconds=time.perf_counter()-started)


def audit_fit_contract(fitting):
    """Mechanically allow only the specified ids expression and progress tag."""
    reference=ast.parse(inspect.getsource(fitting.fit))
    candidate=ast.parse(inspect.getsource(fit))
    assignments=[n for n in ast.walk(reference) if isinstance(n,ast.Assign) and len(n.targets)==1
        and isinstance(n.targets[0],ast.Name) and n.targets[0].id=="ids"]
    require(len(assignments)==1,"parent batch-index assignment count")
    original=ast.parse("torch.randint(len(train_targets),(BATCH,),generator=sampler)",mode="eval").body
    require(ast.dump(assignments[0].value)==ast.dump(original),"parent sampler is not registered comparator")
    assignments[0].value=ast.parse("balanced_indices(len(train_targets))",mode="eval").body
    class Labels(ast.NodeTransformer):
        def visit_Constant(self,node):
            if isinstance(node.value,str): node.value=node.value.replace("[C236]","[C238]")
            return node
    require(ast.dump(Labels().visit(reference),include_attributes=False)==ast.dump(candidate,include_attributes=False),
        "training differs beyond registered sampler/progress tag")
    require(all(getattr(fitting,k)==globals()[k] for k in ("STEPS","BATCH","LR","CLIP","TOL")),"training constants")


def metric_error(actual,expected):
    require(set(actual)==set(expected)=={"en","ja"},"metric languages")
    errors=[]
    for lang in ("en","ja"):
        require(set(actual[lang])==set(expected[lang]),"metric keys")
        for key,value in actual[lang].items():
            other=expected[lang][key]
            require(type(value) in (int,float) and type(other) in (int,float)
                and math.isfinite(value) and math.isfinite(other),"metric finite values")
            errors.append(abs(value-other))
    return max(errors)


def validate_comparator(records,summary,*,parent,fitting):
    parent.validate_parent_records(records,fitting)
    require(fitting.summarize(records)==summary,"C236 measurement/summary identity")
    for rec in records:
        fingerprint=rec["initial_sha256"]
        require(isinstance(fingerprint,str) and len(fingerprint)==64
            and all(c in "0123456789abcdef" for c in fingerprint),"initial fingerprint schema")
        fitting.validate_metrics(rec["initial_probe"])
        for m in rec["final_probe"].values():
            require(m["accuracy"]==.5 and m["fact_pair_accuracy"]==m["query_pair_accuracy"]==0
                and m["evidence_drop"]==m["query_drop"]==0,"accepted C236 deciding metrics")
    return records


def train_one(model,*,rows,views,reference,fitting,binding,factory):
    before=factory.fingerprint(model)
    require(before==reference["initial_sha256"],"fresh initialization mismatch")
    calls=[0,0]
    def hook(module,args,output): calls[0]+=1; calls[1]+=len(args[0])
    handle=model.register_forward_hook(hook)
    try:
        initial,_=binding.evaluate(model,rows,views)
        fitting.validate_metrics(initial)
        initial_error=metric_error(initial,reference["initial_probe"])
        require(initial_error<=TOL and factory.fingerprint(model)==before,"initial replay or evaluation mutation")
        trained=fit(model,*views[0],reference["seed"])
        final_hash=factory.fingerprint(model)
        final,logits=binding.evaluate(model,rows,views)
        fitting.validate_metrics(final)
        require(final_hash!=before and factory.fingerprint(model)==final_hash,"no update or final evaluation mutation")
    finally: handle.remove()
    require(calls==[406,12896],"training/evaluation workload")
    state={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    record=dict(seed=reference["seed"],family=reference["family"],initial_sha256=before,final_sha256=final_hash,
        initial_probe=initial,initial_replay_error=initial_error,final_probe=final,fit=trained,
        predictions=fitting.prediction_record(logits),weights_changed=True,
        forward_calls=calls[0],row_presentations=calls[1],comparator_final=copy.deepcopy(reference["final_probe"]))
    return record,state,logits


def load_bundle(path):
    value=torch.load(path,map_location="cpu",weights_only=True)
    require(value["schema"]=="fold-c238-complete-cohort-v1"
        and value["identities"]==[list(x) for x in identities()] and len(value["states"])==6,"checkpoint schema/order")
    return value["states"]


def summarize(records,*,fitting):
    result=fitting.summarize(records)
    result["all_initial_replays"]=all(0<=r["initial_replay_error"]<=TOL for r in records)
    result["comparator_reused"]=True
    result["per_row_presentations_per_model"]=800
    return result


def validate_result(result):
    require(result["experiment_id"]==EXPERIMENT_ID and result["stage"]==STAGE
        and result["diagnostic_execution_valid"] is True,"result identity")
    require((len(result["source_blobs"]),len(result["input_sha256"]))==(274,406)
        and set(OWN)<=set(result["source_blobs"]),"protection coverage")
    require(len(result["artifacts"])==5 and {x["file"] for x in result["artifacts"]}==OUTPUTS,"artifact coverage")
    s=result["validation_summary"]
    require((s["models"],s["total_training_steps"],s["total_answer_presentations"],s["model_forward_calls"],
        s["total_row_presentations"],s["per_row_presentations_per_model"])==(6,2400,76800,2454,77664,800),"fixed workload")
    require(s["all_replays"] is True and s["all_weights_changed"] is True and s["all_initial_replays"] is True
        and s["comparator_reused"] is True,"replay/update integrity")
    require(type(s["full_probe_gate"]) is bool and type(s["gru_probe_gate"]) is bool
        and result["status"]==("PASS" if s["full_probe_gate"] else "FAIL"),"scientific status")
    require(s["general_language_claim"] is False and s["held_out_generalization_claim"] is False
        and result["gate_f_candidate"] is False and result["network_calls"]==0,"scope")


def precheck(c237_summary,c236_summary,root):
    parent,fitting,_,factory,a=context(); root=Path(root); c237_summary=Path(c237_summary).resolve()
    require(a.sha(c237_summary)==PARENT_SHA,"C237 summary identity")
    p=a.read_json(c237_summary); parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION,"C237 execution identity")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for path,wanted in protected.items(): require(Path(path).is_file() and a.sha(path)==wanted,"changed input:"+path)
    for path,wanted in pins.items(): require(a.git(root,"rev-parse","HEAD:"+path).decode().strip()==wanted,"changed source:"+path)
    require(str(c237_summary) not in protected,"parent summary duplicate")
    protected[str(c237_summary)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"C237 artifact identities")
    for item in p["artifacts"]:
        path=a.safe_child(c237_summary.parent,item["file"])
        require(a.sha(path)==item["sha256"] and path.stat().st_size==item["serialized_bytes"],"C237 artifact bytes")
        require(str(path.resolve()) not in protected,"parent artifact duplicate")
        protected[str(path.resolve())]=item["sha256"]
    require(protected.get(str(Path(c236_summary).resolve()))==COMPARATOR_SHA
        and a.sha(c236_summary)==COMPARATOR_SHA,"C236 comparator protection")
    comparison=a.read_json(c236_summary); fitting.validate_result(comparison)
    require(comparison["commit_sha"]==COMPARATOR_EXECUTION and comparison["status"]=="FAIL","accepted comparator")
    for path in OWN:
        require(path not in pins,"OWN collision")
        pins[path]=a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    deps=set(factory.LM_SOURCES)|{OWN[0],
        "fold_lm/v05_benchmarks/model_c237_frozen_signal_audit.py",
        "fold_lm/v05_benchmarks/model_c236_minimal_binding.py",
        "fold_lm/v05_benchmarks/model_c235_frozen_binding_diagnostic.py",
        "fold_lm/v05_benchmarks/model_c234_context_binding.py",
        "fold_lm/v05_benchmarks/model_c233_core_ablation.py",
        "fold_lm/v05_benchmarks/model_c232_bilingual_learning.py",
        "fold_lm/v05_benchmarks/model_c231_byte_eval_contract.py",
        "fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py"}
    require(len(deps)==14 and deps<=set(pins),"direct dependency coverage")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(274,406),"protection count")
    require(digest(manifest())==MANIFEST_SHA,"manifest drift")
    audit_fit_contract(fitting)
    return pins,protected


def load_inputs(c236_summary):
    parent,fitting,_,_,a=context(); directory=Path(c236_summary).resolve().parent
    rows=a.read_json(directory/"probe-dataset.json")
    require(len(rows)==16 and digest(rows)==PROBE_SHA,"unchanged cohort")
    records=validate_comparator(a.read_json(directory/"measurements.json"),
        a.read_json(c236_summary)["validation_summary"],parent=parent,fitting=fitting)
    return rows,records


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==122,"parent regression modules")
    return names+["tests_lm.test_v05_c238_complete_cohort_sampler"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite): yield from flatten(item)
        else: yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"historical test identity/exclusion")
    kept=[t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(2882,2881),"regression counts")
    return unittest.TestSuite(kept)


def run(*,c237_summary,c236_summary,output_dir,expected_head):
    _,fitting,binding,factory,a=context(); root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch mismatch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tracked tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c237_summary,c236_summary,root)
    rows,comparators=load_inputs(c236_summary)
    views=[binding.tensors(rows,mode) for mode in VIEWS]
    records=[]; states=[]; references=[]
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    for seed in SEEDS:
        full=factory.new_model(seed)
        baseline=binding.parent_module().new_baseline(full)
        require((sum(p.numel() for p in full.parameters()),sum(p.numel() for p in baseline.parameters()))
            ==(13488,10160),"model sizes")
        for family,model in (("full",full),("gru_only",baseline)):
            reference=comparators[len(records)]
            require((reference["seed"],reference["family"])==(seed,family),"paired comparator identity")
            print(f"[C238] model={len(records)+1}/6 seed={seed} family={family}; every TRAIN row twice per batch",flush=True)
            record,state,logits=train_one(model,rows=rows,views=views,reference=reference,
                fitting=fitting,binding=binding,factory=factory)
            records.append(record); states.append(state); references.append(logits)
    torch.save(dict(schema="fold-c238-complete-cohort-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    reloaded=load_bundle(out/"trained-models.pt")
    for record,state,reference in zip(records,reloaded,references,strict=True):
        model=factory.new_model(record["seed"])
        if record["family"]=="gru_only": model=binding.parent_module().new_baseline(model)
        fitting.replay_one(model,state,record,reference,binding=binding,factory=factory,rows=rows,views=views)
    summary=summarize(records,fitting=fitting)
    for name,value in (("sampler-plan.json",manifest()),("probe-dataset.json",rows),
        ("measurements.json",records),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard(); precheck(c237_summary,c236_summary,root)
    for path,wanted in protected.items(): require(a.sha(path)==wanted,"modified input:"+path)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if summary["full_probe_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,network_calls=0,limitations=[
            "Only16 seen TRAIN prompts; possible memorization, no held-out binding claim.",
            "Sampler changes joint coverage, label balance and stochastic-gradient variability together.",
            "C236 comparator is reused, not rerun; C237 sensitivity is not proof of a sampler cause."])
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C238 RESULT ===",flush=True); print(blob(result).decode(),flush=True)
    return result


def verify_artifacts(output_dir,c236_summary,expected_head):
    _,fitting,_,_,a=context(); out=Path(output_dir)
    result=a.read_json(out/"summary.json"); validate_result(result)
    require(result["commit_sha"]==expected_head,"summary execution identity")
    for path,wanted in result["input_sha256"].items(): require(a.sha(path)==wanted,"postcheck input")
    for item in result["artifacts"]:
        path=a.safe_child(out,item["file"])
        require(a.sha(path)==item["sha256"] and path.stat().st_size==item["serialized_bytes"],"postcheck artifact")
    records=a.read_json(out/"measurements.json")
    require(summarize(records,fitting=fitting)==result["validation_summary"],"measurement summary")
    require(a.read_json(out/"validation-summary.json")==result["validation_summary"],"saved validation")
    require(a.read_json(out/"sampler-plan.json")==manifest(),"saved plan")
    require(digest(a.read_json(out/"probe-dataset.json"))==PROBE_SHA,"saved cohort")
    _,comparators=load_inputs(c236_summary)
    for rec,old in zip(records,comparators,strict=True):
        require((rec["seed"],rec["family"])==(old["seed"],old["family"])
            and rec["comparator_final"]==old["final_probe"] and rec["initial_sha256"]==old["initial_sha256"],"comparator replay")
        require(metric_error(rec["initial_probe"],old["initial_probe"])<=TOL,"saved initial metrics")
    return result,records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("c237-summary","c236-summary","output-dir"): parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
