"""C247: normal-exposure-matched TRAIN-fit control; not a generalization gate."""
from __future__ import annotations
import argparse
import ast
from collections import Counter
import copy
import hashlib
import inspect
import json
import math
from pathlib import Path
import time
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C247-v5b-normal-exposure-control"
STAGE = "V5-B-NORMAL-EXPOSURE-CONTROL"
BASE = "8559c95ec1716cc507f77f3d9271e19dcbd8ca28"
PARENT_EXECUTION = "c17195b7c0f80ae7dd60050e25dca6a3effc21fb"
PARENT_SHA = "9a462485dffc948674b7752012893a8175cdb5de251f179763ae03e26659623a"
PARENT_ARTIFACTS = {
    "measurements.json":"81b6aaa5ae69be11e49bb0e64dff0763d8f12437393df18ff4c7ca346d8d908b",
    "split-dataset.json":"e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346",
    "trained-models.pt":"8282b378bea2c6ff166fb18ed9345bfee71ab5ac2080204a43251229f8b6fd34",
    "training-plan.json":"761b00863243d9118cd85058f585b7e3592404c677b8d8f548be45ed2fd05db8",
    "validation-summary.json":"68ccff53230dc8ab8fcf24d542547ade89f63335c4fd508db401ff0e68b80cf3",
}
SPLIT_SHA = PARENT_ARTIFACTS["split-dataset.json"]
SEEDS, FAMILIES = (234001,234002,234003), ("full","gru_only")
SPLITS, VIEWS = ("TRAIN","HOLDOUT"), ("normal","evidence_blind","query_blind")
ROWS = {"TRAIN":64,"HOLDOUT":32}
STEPS, BATCH, LR, CLIP, TOL = 200,32,.005,1.,1e-9
OWN = ("fold_lm/v05_benchmarks/model_c247_normal_exposure_control.py",
    "tests_lm/test_v05_c247_normal_exposure_control.py","tools/run_c247.ps1","tools/invoke_c247.ps1",
    "docs/experiment-ledger-addendum-c247-preregistration.md","docs/v5b-normal-exposure-control-v0.1.md")
OUTPUTS = {"control-plan.json","split-dataset.json","trained-models.pt","measurements.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "f9558bfead121a605f8cc2dd776eed5db6db981c1c20b675d44d49d4b95a502c"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c246_training_erasure as parent
    return parent


def context():
    parent=parent_module()
    _,base,fitting,binding,factory,audit=parent.context()
    return parent,base,fitting,binding,factory,audit


def identities(): return [(s,f) for s in SEEDS for f in FAMILIES]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        split_sha256=SPLIT_SHA,identities=[list(x) for x in identities()],rows=ROWS,views=list(VIEWS),
        initialization="fresh exact C246 initial_sha256, also C244 initial identity; no trained state reuse",
        primary="all Full TRAIN cells pass original full TRAIN criteria; HOLDOUT secondary only",
        control_question="is C246 normal exposure sufficient without interleaved masked updates?",
        row_schedule="old32 then added32,100 cycles; equals C246 normal subsequence",
        parent_step_map="zero-based j maps to 4*(j//2)+2+j%2",
        steps=STEPS,batch=BATCH,per_train_row_normal=100,masked_updates=0,
        parameters=dict(full=13488,gru_only=10160),width=16,slots=48,
        optimizer="AdamW",lr=LR,clip=CLIP,betas=[.9,.999],eps=1e-8,weight_decay=0.,
        precision="CPU float64",threads=2,deterministic=True,
        train_steps=1200,answer_presentations=38400,model_forward_calls=1290,row_presentations=43008,
        evaluation_forwards=90,evaluation_rows=4608,checkpoint_writes=1,
        gate=dict(accuracy=.90,fact_pair=.80,query_pair=.80,order_pair=.80,evidence_drop=.35,query_drop=.35),
        comparator="C246 final and its unchanged C244 comparator; identical original rows",
        source_pins=328,protected_inputs=514,direct_dependencies=23,own_tests=24,
        modules=132,loaded_tests=3098,focused_tests=3097,excluded_test=EXCLUDED,
        replay_tolerance=TOL,network_calls=0,gate_f_candidate=False,
        general_language_claim=False,causal_mechanism_claim=False,core_superiority_claim=False)


def balanced_indices(count,step):
    require(type(count) is int and count==64 and type(step) is int and step>=0,"schedule inputs")
    return torch.arange(32,dtype=torch.int64)+32*(step%2)


def parent_normal_step(step):
    require(type(step) is int and 0<=step<STEPS,"control step")
    return 4*(step//2)+2+step%2


def fit(model,train_tokens,train_targets,seed,*,steps=STEPS):
    require(type(steps) is int and steps>0 and len(train_tokens)==train_targets.numel()>0,"training inputs")
    sampler=torch.Generator(device="cpu").manual_seed(seed+1000)
    optimizer=torch.optim.AdamW(model.parameters(),lr=LR,betas=(0.9,0.999),eps=1e-8,weight_decay=0.0)
    model.train(); started=time.perf_counter(); first=last=None
    for step in range(steps):
        ids=balanced_indices(len(train_targets),step)
        optimizer.zero_grad(set_to_none=True)
        logits=model(train_tokens[ids],torch.zeros(BATCH,dtype=torch.int64))
        loss=F.cross_entropy(logits,train_targets[ids]); require(bool(torch.isfinite(loss)),"nonfinite training loss")
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),CLIP,error_if_nonfinite=True)
        optimizer.step(); last=float(loss.detach())
        if first is None:first=last
        if (step+1)%100==0:print(f"[C247] seed={seed} step={step+1}/{steps} answer_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=steps,answer_presentations=steps*BATCH,first_loss=first,last_loss=last,
                fit_seconds=time.perf_counter()-started)


def audit_recipe(base,parent):
    class Labels(ast.NodeTransformer):
        def visit_Constant(self,node):
            if isinstance(node.value,str):node.value=node.value.replace("[C244]","[C247]")
            return node
    expected=Labels().visit(ast.parse(inspect.getsource(base.fit)))
    require(ast.dump(expected,include_attributes=False)==ast.dump(ast.parse(inspect.getsource(fit)),include_attributes=False),"normal fit AST drift")
    require(base.STEPS==parent.STEPS==400 and STEPS==200,"registered budget difference")
    require(all(getattr(base,k)==getattr(parent,k)==globals()[k] for k in ("BATCH","LR","CLIP","TOL")),"optimizer constants")
    marker=torch.stack((torch.zeros(64,48),torch.ones(64,48)),dim=1)
    for step in range(STEPS):
        pstep=parent_normal_step(step)
        require(torch.equal(balanced_indices(64,step),parent.balanced_indices(64,pstep)),"normal row subsequence")
        require(bool((parent.select_view(marker,pstep)==0).all()),"mapped parent view is not normal")


def load_inputs(c246_summary):
    parent,base,fitting,_,_,a=context();path=Path(c246_summary).resolve()
    parts=a.read_json(path.parent/"split-dataset.json")
    require(set(parts)==set(SPLITS) and digest(parts)==SPLIT_SHA and {k:len(v) for k,v in parts.items()}==ROWS,"partition identity")
    records=a.read_json(path.parent/"measurements.json")
    require(parent.summarize(records,base,fitting)==a.read_json(path)["validation_summary"],"C246 measurement summary")
    require([(r["seed"],r["family"]) for r in records]==identities(),"parent record order")
    discrete=base.parent_module().discrete_metrics
    for r in records:
        h=r["initial_sha256"]
        require(isinstance(h,str) and len(h)==64 and all(c in "0123456789abcdef" for c in h) and h!=r["final_sha256"],"initial identity")
        require(set(r["c244_comparator"])==set(SPLITS),"C244 comparator schema")
        for split in SPLITS:
            fitting.validate_metrics(r["c244_comparator"][split],ROWS[split])
            d=discrete(parts[split],r["predictions"][split])
            require(all(abs(v-r["final"][split][lang][k])<=TOL for lang,m in d.items() for k,v in m.items()),"parent discrete replay")
    return parts,records


def train_one(model,parts,ref,*,base,fitting,binding,factory):
    before=factory.fingerprint(model);require(before==ref["initial_sha256"],"fresh initial fingerprint")
    tokens,targets=binding.tensors(parts["TRAIN"],"normal")
    counts=[0,0];updates=[0];blocks=[0,0]
    def hook(module,args,output):
        counts[0]+=1;counts[1]+=len(args[0])
        if module.training:
            step=updates[0]
            require(step<STEPS and torch.equal(args[0],tokens[base.balanced_indices(64,step)]),"actual normal optimizer batch")
            blocks[step%2]+=1;updates[0]+=1
    handle=model.register_forward_hook(hook)
    try:
        initial,_=fitting.evaluate(model,parts["TRAIN"],binding,factory.fingerprint)
        trained=fit(model,tokens,targets,ref["seed"])
        final={};raw={}
        for split in SPLITS:final[split],raw[split]=fitting.evaluate(model,parts[split],binding,factory.fingerprint)
    finally:handle.remove()
    after=factory.fingerprint(model)
    require(before!=after and counts==[209,6880] and updates[0]==200 and blocks==[100,100],"training count/update")
    record=dict(seed=ref["seed"],family=ref["family"],initial_sha256=before,final_sha256=after,
        initial_train=initial,final=final,fit=trained,block_updates=blocks,forward_calls=counts[0],row_presentations=counts[1],
        weights_changed=True,predictions={s:fitting.prediction_record(raw[s],ROWS[s]) for s in SPLITS},
        c246_comparator=copy.deepcopy(ref["final"]),c244_comparator=copy.deepcopy(ref["c244_comparator"]))
    return record,{k:v.detach().cpu().clone() for k,v in model.state_dict().items()},raw


def summarize(records,fitting):
    require([(r["seed"],r["family"]) for r in records]==identities(),"record identity order")
    train_gate={f:True for f in FAMILIES};joint_gate=dict(train_gate);cells=[]
    for r in records:
        require(r["block_updates"]==[100,100] and set(r["final"])==set(SPLITS),"record schedule/split")
        for split in SPLITS:
            for field in ("final","c246_comparator","c244_comparator"):fitting.validate_metrics(r[field][split],ROWS[split])
        for lang in ("en","ja"):
            train=fitting.cell_pass(r["final"]["TRAIN"][lang]);held=fitting.cell_pass(r["final"]["HOLDOUT"][lang])
            prior=fitting.cell_pass(r["c246_comparator"]["TRAIN"][lang])
            label="BOTH_TRAIN_PASS" if train and prior else "CONTROL_TRAIN_PASS_ONLY" if train else "C246_TRAIN_PASS_ONLY" if prior else "NEITHER_TRAIN_PASS"
            cells.append(dict(seed=r["seed"],family=r["family"],language=lang,train_pass=train,holdout_pass=held,c246_train_pass=prior,comparison=label))
            train_gate[r["family"]]&=train;joint_gate[r["family"]]&=train and held
    return dict(models=6,full_train_control_gate=train_gate["full"],gru_train_control_gate=train_gate["gru_only"],
        secondary_full_joint_gate=joint_gate["full"],secondary_gru_joint_gate=joint_gate["gru_only"],cells=cells,
        comparison_counts=dict(Counter(c["comparison"] for c in cells)),
        all_replays=all(r["checkpoint_roundtrip"] is True and r["prediction_replayed"] is True and 0<=r["reload_max_error"]<=TOL for r in records),
        all_weights_changed=all(r["weights_changed"] is True for r in records),
        train_steps=sum(r["fit"]["steps"] for r in records),answer_presentations=sum(r["fit"]["answer_presentations"] for r in records),
        model_forward_calls=sum(r["forward_calls"] for r in records),row_presentations=sum(r["row_presentations"] for r in records),
        general_language_claim=False,causal_mechanism_claim=False,core_superiority_claim=False)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(328,514) and set(OWN)<=set(p["source_blobs"]),"protection counts")
    require(len(p["artifacts"])==5 and {a["file"] for a in p["artifacts"]}==OUTPUTS,"output coverage")
    s=p["validation_summary"]
    require((s["models"],s["train_steps"],s["answer_presentations"],s["model_forward_calls"],s["row_presentations"])==(6,1200,38400,1290,43008),"workload")
    require(s["all_replays"] is True and s["all_weights_changed"] is True and len(s["cells"])==12 and sum(s["comparison_counts"].values())==12,"integrity")
    for k in ("full_train_control_gate","gru_train_control_gate","secondary_full_joint_gate","secondary_gru_joint_gate"):require(type(s[k]) is bool,"gate type")
    require(p["status"]==("PASS" if s["full_train_control_gate"] else "FAIL"),"TRAIN-only primary status")
    require(p["gate_f_candidate"] is False and p["network_calls"]==0 and all(s[k] is False for k in ("general_language_claim","causal_mechanism_claim","core_superiority_claim")),"scope")


def precheck(c246_summary,root):
    parent,base,_,_,factory,a=context();root=Path(root);path=Path(c246_summary).resolve()
    require(a.sha(path)==PARENT_SHA,"parent summary hash");p=a.read_json(path);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL" and p["validation_summary"]["cell_outcomes"]=={"TRAIN_CRITERIA_MISS":10,"RECOMBINATION_MISS":2},"accepted parent")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items():require(Path(name).is_file() and a.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items():require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    require(str(path) not in protected,"parent double count");protected[str(path)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifact identities")
    for item in p["artifacts"]:
        child=a.safe_child(path.parent,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"parent artifact bytes")
        require(str(child.resolve()) not in protected,"artifact double count");protected[str(child.resolve())]=item["sha256"]
    for name in OWN:
        require(name not in pins,"OWN collision");pins[name]=a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    helpers=("gate_f_c230_prepared_capsule.py","model_c231_byte_eval_contract.py","model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py","model_c234_context_binding.py","model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py","model_c237_frozen_signal_audit.py","model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py","model_c240_saved_position_audit.py","model_c241_assignment_holdout.py",
        "model_c242_balanced_recombination.py","model_c243_saved_recombination_audit.py","model_c244_two_partner_recombination.py",
        "model_c245_selective_evidence.py","model_c246_training_erasure.py")
    deps=set(factory.LM_SOURCES)|{OWN[0]}|{"fold_lm/v05_benchmarks/"+h for h in helpers}
    require(len(deps)==23 and deps<=set(pins),"direct dependency coverage")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(328,514) and digest(manifest())==MANIFEST_SHA,"count/manifest")
    audit_recipe(base,parent)
    return pins,protected


def load_bundle(path):
    value=torch.load(path,map_location="cpu",weights_only=True)
    require(value["schema"]=="fold-c247-normal-exposure-v1" and value["identities"]==[list(x) for x in identities()] and len(value["states"])==6,"bundle schema/order")
    return value["states"]


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==131,"parent modules")
    return names+["tests_lm.test_v05_c247_normal_exposure_control"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests];require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"suite identities")
    kept=[t for t in tests if t.id()!=EXCLUDED];require((len(tests),len(kept))==(3098,3097),"suite counts")
    return unittest.TestSuite(kept)


def run(*,c246_summary,output_dir,expected_head):
    _,base,fitting,binding,factory,a=context();root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"execution HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c246_summary,root);parts,refs=load_inputs(c246_summary)
    records=[];states=[];raw=[];out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for seed in SEEDS:
        full=factory.new_model(seed);baseline=binding.parent_module().new_baseline(full)
        require((sum(p.numel() for p in full.parameters()),sum(p.numel() for p in baseline.parameters()))==(13488,10160),"parameter counts")
        for family,model in (("full",full),("gru_only",baseline)):
            ref=refs[len(records)];require((ref["seed"],ref["family"])==(seed,family),"paired identity")
            print(f"[C247] model={len(records)+1}/6 seed={seed} family={family};200 normal-only updates",flush=True)
            record,state,outputs=train_one(model,parts,ref,base=base,fitting=fitting,binding=binding,factory=factory)
            records.append(record);states.append(state);raw.append(outputs)
    torch.save(dict(schema="fold-c247-normal-exposure-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for record,state,outputs in zip(records,load_bundle(out/"trained-models.pt"),raw,strict=True):
        model=factory.new_model(record["seed"])
        if record["family"]=="gru_only":model=binding.parent_module().new_baseline(model)
        base.replay_one(model,state,record,outputs,parts,fitting=fitting,binding=binding,factory=factory)
    summary=summarize(records,fitting)
    for name,value in (("control-plan.json",manifest()),("split-dataset.json",parts),("measurements.json",records),("validation-summary.json",summary)):(out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard();precheck(c246_summary,root)
    for name,wanted in protected.items():require(a.sha(name)==wanted,"modified input")
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["full_train_control_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,gate_f_candidate=False,network_calls=0,
        limitations=["Primary is normal-exposure TRAIN sufficiency, not HOLDOUT success.","Removing masked updates changes optimizer step count/state; not a unique mechanism test.","Comparators are reused accepted records, not independent baseline reruns."])
    validate_result(p);(out/"summary.json").write_bytes(blob(p));print("=== C247 RESULT ===",flush=True);print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(output_dir,c246_summary,expected_head):
    _,base,fitting,_,_,a=context();out=Path(output_dir);p=a.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():require(a.sha(name)==wanted,"postcheck input")
    for item in p["artifacts"]:
        child=a.safe_child(out,item["file"]);require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"artifact bytes")
    records=a.read_json(out/"measurements.json");parts,refs=load_inputs(c246_summary)
    require(a.read_json(out/"control-plan.json")==manifest() and a.read_json(out/"split-dataset.json")==parts,"plan/partition")
    require(summarize(records,fitting)==p["validation_summary"]==a.read_json(out/"validation-summary.json"),"summary replay")
    for record,ref in zip(records,refs,strict=True):
        require(record["initial_sha256"]==ref["initial_sha256"] and record["c246_comparator"]==ref["final"] and record["c244_comparator"]==ref["c244_comparator"],"initial/comparator identity")
        for split in SPLITS:
            m=base.parent_module().discrete_metrics(parts[split],record["predictions"][split])
            require(all(abs(v-record["final"][split][lang][k])<=TOL for lang,d in m.items() for k,v in d.items()),"saved discrete replay")
    return p,records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for n in ("c246-summary","output-dir"):parser.add_argument("--"+n,type=Path,required=True)
    parser.add_argument("--expected-head",required=True);run(**vars(parser.parse_args()))


if __name__=="__main__":main()
