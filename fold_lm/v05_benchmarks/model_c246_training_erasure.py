"""C246: training-only distractor erasure; judge original, fully observed inputs."""
from __future__ import annotations
import argparse
import ast
import copy
import hashlib
import inspect
import itertools
import json
from pathlib import Path
import time
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C246-v5b-training-only-distractor-erasure"
STAGE = "V5-B-TRAINING-ONLY-DISTRACTOR-ERASURE"
BASE = "87fe39481ae65cdf2452f2cb79ba0b8f6d912a2a"
PARENT_EXECUTION = "db838801cc139b4578c2aa002cbc001c58fa1e91"
PARENT_SHA = "ae2f2a940a7c9f903bac8f8f472680654abe305df897d011e61a355e4d9d9d88"
PARENT_ARTIFACTS = {
    "diagnostic-plan.json":"50cadf2e5b9bc0c1a1fab5f29652afd5b5c2f0eeaed3be919cdadb3ebcebf1ac",
    "diagnostics.json":"231a1d10b186a0d57be227ab4dd38829ee459d142926e7be2859dd88b6fdd048",
    "intervention-inputs.json":"91e207dde4e080a52040bcf39b6f1236af7053a703a684ba94a8c6c47dfe0c22",
    "outputs.json":"aaab0bc28bf01aed325d4bbe55cd89b00e7ea2957b8db5f0930aa350da862607",
    "validation-summary.json":"2dc4f24dd318dd37ed848994b175bb929d830f7c70549d95df492feedaa3d8a3",
}
C244_SHA = "a2c5167bd6e93c09020ca5079cc94d77e692fd18768588536379d4797fd99297"
SPLIT_SHA = "e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346"
SEEDS, FAMILIES = (234001,234002,234003), ("full","gru_only")
SPLITS, VIEWS = ("TRAIN","HOLDOUT"), ("normal","evidence_blind","query_blind")
ROWS = {"TRAIN":64,"HOLDOUT":32}
STEPS, BATCH, LR, CLIP, TOL = 400,32,.005,1.,1e-9
OWN = ("fold_lm/v05_benchmarks/model_c246_training_erasure.py",
    "tests_lm/test_v05_c246_training_erasure.py","tools/run_c246.ps1","tools/invoke_c246.ps1",
    "docs/experiment-ledger-addendum-c246-preregistration.md","docs/v5b-training-erasure-v0.1.md")
OUTPUTS = {"training-plan.json","split-dataset.json","trained-models.pt","measurements.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "761b00863243d9118cd85058f585b7e3592404c677b8d8f548be45ed2fd05db8"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c245_selective_evidence as parent
    return parent


def context():
    parent=parent_module()
    base,fitting,binding,factory,audit=parent.context()
    return parent,base,fitting,binding,factory,audit


def identities(): return list(itertools.product(SEEDS,FAMILIES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        c244_sha256=C244_SHA,split_sha256=SPLIT_SHA,identities=[list(x) for x in identities()],rows=ROWS,
        eval_views=list(VIEWS),train_views=["normal","other_value_blind"],
        cycle=["old:other_value_blind","added:other_value_blind","old:normal","added:normal"],
        block_view_updates=[[100,100],[100,100]],per_train_row_normal=100,per_train_row_masked=100,
        initialization="fresh exact C244 initial_sha256; never trained checkpoints",
        parameters=dict(full=13488,gru_only=10160),width=16,slots=48,steps=STEPS,batch=BATCH,
        optimizer="AdamW",lr=LR,clip=CLIP,betas=[.9,.999],eps=1e-8,weight_decay=0.,
        dtype="float64",device="cpu",threads=2,deterministic=True,
        train_steps=2400,answer_presentations=76800,normal_presentations=38400,masked_presentations=38400,
        model_forward_calls=2490,row_presentations=81408,checkpoint_writes=1,
        gate=dict(accuracy=.90,fact_pair=.80,query_pair=.80,order_pair=.80,evidence_drop=.35,query_drop=.35),
        endpoint="original normal TRAIN64/HOLDOUT32 plus inherited masks; no selective-mask success score",
        comparator="same-row C244 final metrics; existing evidence, no parent model inference",
        training_cue="visible query selects erased nonqueried field; remaining value is a copying cue",
        source_pins=322,protected_inputs=502,direct_dependencies=22,own_tests=24,
        modules=131,loaded_tests=3074,focused_tests=3073,excluded_test=EXCLUDED,
        replay_tolerance=TOL,network_calls=0,gate_f_candidate=False,general_language_claim=False,
        core_superiority_claim=False,causal_mechanism_claim=False)


def balanced_indices(count,step):
    require(type(count) is int and count==64 and type(step) is int and step>=0,"schedule inputs")
    return torch.arange(32,dtype=torch.int64)+32*(step%2)


def select_view(batch,step):
    require(type(step) is int and step>=0 and batch.ndim==3 and batch.shape[1:]==(2,48),"view inputs")
    return batch[:,1 if step%4<2 else 0,:]


def training_tokens(parts,parent,binding,factory):
    require(digest(parts)==SPLIT_SHA and {s:len(r) for s,r in parts.items()}==ROWS,"fixed partition")
    rows=parts["TRAIN"]
    texts=[parent.masked_prompt(r,"other_value_blind",binding) for r in rows]
    normal,targets=binding.tensors(rows,"normal")
    masked,again=parent.tensors(rows,texts,"other_value_blind",binding,factory)
    require(torch.equal(targets,again) and normal.shape==masked.shape==(64,48)
        and normal.dtype==masked.dtype==torch.int64,"training token parity")
    require(not (set(texts)|{r["prompt"] for r in rows}) & {r["prompt"] for r in parts["HOLDOUT"]},"normal holdout leakage")
    return torch.stack((normal,masked),dim=1),targets


def fit(model,train_tokens,train_targets,seed,*,steps=STEPS):
    require(type(steps) is int and steps>0 and len(train_tokens)==train_targets.numel()>0,"training inputs")
    sampler=torch.Generator(device="cpu").manual_seed(seed+1000)
    optimizer=torch.optim.AdamW(model.parameters(),lr=LR,betas=(0.9,0.999),eps=1e-8,weight_decay=0.0)
    model.train(); started=time.perf_counter(); first=last=None
    for step in range(steps):
        ids=balanced_indices(len(train_targets),step)
        optimizer.zero_grad(set_to_none=True)
        logits=model(select_view(train_tokens[ids],step),torch.zeros(BATCH,dtype=torch.int64))
        loss=F.cross_entropy(logits,train_targets[ids]); require(bool(torch.isfinite(loss)),"nonfinite training loss")
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),CLIP,error_if_nonfinite=True)
        optimizer.step(); last=float(loss.detach())
        if first is None:first=last
        if (step+1)%100==0:print(f"[C246] seed={seed} step={step+1}/{steps} answer_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=steps,answer_presentations=steps*BATCH,first_loss=first,last_loss=last,
                fit_seconds=time.perf_counter()-started)


def audit_fit_contract(base):
    class Change(ast.NodeTransformer):
        changed=0
        def visit_Constant(self,node):
            if isinstance(node.value,str):node.value=node.value.replace("[C244]","[C246]")
            return node
        def visit_Assign(self,node):
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id=="logits":
                before=ast.parse("logits=model(train_tokens[ids],torch.zeros(BATCH,dtype=torch.int64))").body[0]
                require(ast.dump(node,include_attributes=False)==ast.dump(before,include_attributes=False),"parent input expression")
                self.changed+=1
                return ast.parse("logits=model(select_view(train_tokens[ids],step),torch.zeros(BATCH,dtype=torch.int64))").body[0]
            return self.generic_visit(node)
    change=Change();expected=change.visit(ast.parse(inspect.getsource(base.fit)))
    require(change.changed==1 and ast.dump(expected,include_attributes=False)==ast.dump(ast.parse(inspect.getsource(fit)),include_attributes=False),"fit drift beyond input view/tag")
    require(all(getattr(base,k)==globals()[k] for k in ("STEPS","BATCH","LR","CLIP","TOL")),"fit constants")
    require(all(torch.equal(balanced_indices(64,s),base.balanced_indices(64,s)) for s in range(STEPS)),"row schedule parity")


def train_one(model,parts,ref,*,parent,base,fitting,binding,factory):
    before=factory.fingerprint(model);require(before==ref["initial_sha256"],"fresh initial identity")
    tokens,targets=training_tokens(parts,parent,binding,factory)
    counts=[0,0];updates=[0];matrix=[[0,0],[0,0]]
    def hook(module,args,output):
        counts[0]+=1;counts[1]+=len(args[0])
        if module.training:
            step=updates[0];block=step%2;view=1-((step//2)%2)
            require(torch.equal(args[0],tokens[base.balanced_indices(64,step),view,:]),"actual scheduled input mismatch")
            matrix[block][view]+=1;updates[0]+=1
    handle=model.register_forward_hook(hook)
    try:
        initial,_=fitting.evaluate(model,parts["TRAIN"],binding,factory.fingerprint)
        trained=fit(model,tokens,targets,ref["seed"])
        final={};raw={}
        for s in SPLITS:final[s],raw[s]=fitting.evaluate(model,parts[s],binding,factory.fingerprint)
    finally:handle.remove()
    after=factory.fingerprint(model)
    require(before!=after and counts==[409,13280] and updates[0]==400 and matrix==[[100,100],[100,100]],"training integrity")
    record=dict(seed=ref["seed"],family=ref["family"],initial_sha256=before,final_sha256=after,
        initial_train=initial,final=final,fit=trained,block_updates=[200,200],block_view_updates=matrix,
        forward_calls=counts[0],row_presentations=counts[1],weights_changed=True,
        predictions={s:fitting.prediction_record(raw[s],ROWS[s]) for s in SPLITS},
        c244_comparator=copy.deepcopy(ref["final"]))
    return record,{k:v.detach().cpu().clone() for k,v in model.state_dict().items()},raw


def summarize(records,base,fitting):
    result=base.summarize(records,fitting)
    require(all(r["block_view_updates"]==[[100,100],[100,100]] for r in records),"view schedule counts")
    result["full_augmentation_gate"]=result.pop("full_two_partner_gate")
    result["gru_augmentation_gate"]=result.pop("gru_two_partner_gate")
    result.update(normal_presentations=38400,masked_presentations=38400)
    return result


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(322,502) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"artifacts")
    s=p["validation_summary"]
    require((s["models"],s["train_steps"],s["answer_presentations"],s["model_forward_calls"],s["row_presentations"],s["normal_presentations"],s["masked_presentations"])
        ==(6,2400,76800,2490,81408,38400,38400),"workload")
    require(s["all_replays"] is True and s["all_weights_changed"] is True and sum(s["cell_outcomes"].values())==12,"integrity")
    require(type(s["full_augmentation_gate"]) is bool and type(s["gru_augmentation_gate"]) is bool
        and p["status"]==("PASS" if s["full_augmentation_gate"] else "FAIL"),"scientific status")
    require(p["gate_f_candidate"] is False and p["network_calls"]==0 and all(s[k] is False for k in
        ("general_language_claim","core_superiority_claim","causal_mechanism_claim")),"scope")


def precheck(c245_summary,c244_summary,root):
    parent,_,_,_,factory,a=context();root=Path(root);path=Path(c245_summary).resolve();old=Path(c244_summary).resolve()
    require(a.sha(path)==PARENT_SHA,"C245 summary identity");p=a.read_json(path);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS","accepted parent")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items():require(Path(name).is_file() and a.sha(name)==wanted,"changed input: "+name)
    for name,wanted in pins.items():require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source: "+name)
    require(protected.get(str(old))==C244_SHA and a.sha(old)==C244_SHA,"C244 inherited identity")
    require(str(path) not in protected,"parent duplicate");protected[str(path)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifacts")
    for item in p["artifacts"]:
        child=a.safe_child(path.parent,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"parent bytes")
        require(str(child.resolve()) not in protected,"artifact duplicate");protected[str(child.resolve())]=item["sha256"]
    for name in OWN:
        require(name not in pins,"OWN collision");pins[name]=a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    helpers=("gate_f_c230_prepared_capsule.py","model_c231_byte_eval_contract.py","model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py","model_c234_context_binding.py","model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py","model_c237_frozen_signal_audit.py","model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py","model_c240_saved_position_audit.py","model_c241_assignment_holdout.py",
        "model_c242_balanced_recombination.py","model_c243_saved_recombination_audit.py","model_c244_two_partner_recombination.py",
        "model_c245_selective_evidence.py")
    deps=set(factory.LM_SOURCES)|{OWN[0]}|{"fold_lm/v05_benchmarks/"+h for h in helpers}
    require(len(deps)==22 and deps<=set(pins),"direct dependency coverage")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(322,502) and digest(manifest())==MANIFEST_SHA,"counts/manifest")
    audit_fit_contract(context()[1])
    return pins,protected


def load_inputs(c244_summary):
    parent,_,_,binding,factory,_=context()
    parts,refs=parent.load_inputs(c244_summary)
    require([(r["seed"],r["family"]) for r in refs]==identities(),"parent identities")
    for r in refs:
        h=r["initial_sha256"]
        require(isinstance(h,str) and len(h)==64 and all(c in "0123456789abcdef" for c in h) and h!=r["final_sha256"],"initial/final semantics")
    training_tokens(parts,parent,binding,factory)
    return parts,refs


def load_bundle(path):
    value=torch.load(path,map_location="cpu",weights_only=True)
    require(value["schema"]=="fold-c246-training-erasure-v1" and value["identities"]==[list(x) for x in identities()] and len(value["states"])==6,"checkpoint schema/order")
    return value["states"]


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==130,"parent modules")
    return names+["tests_lm.test_v05_c246_training_erasure"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests];require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"suite identity")
    kept=[t for t in tests if t.id()!=EXCLUDED];require((len(tests),len(kept))==(3074,3073),"suite counts")
    return unittest.TestSuite(kept)


def run(*,c245_summary,c244_summary,output_dir,expected_head):
    parent,base,fitting,binding,factory,a=context();root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c245_summary,c244_summary,root);parts,refs=load_inputs(c244_summary)
    records=[];states=[];raw=[];out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for seed in SEEDS:
        full=factory.new_model(seed);baseline=binding.parent_module().new_baseline(full)
        require((sum(p.numel() for p in full.parameters()),sum(p.numel() for p in baseline.parameters()))==(13488,10160),"model sizes")
        for family,model in (("full",full),("gru_only",baseline)):
            ref=refs[len(records)];require((ref["seed"],ref["family"])==(seed,family),"paired identity")
            print(f"[C246] model={len(records)+1}/6 seed={seed} family={family}; training-only erasure",flush=True)
            r,state,outputs=train_one(model,parts,ref,parent=parent,base=base,fitting=fitting,binding=binding,factory=factory)
            records.append(r);states.append(state);raw.append(outputs)
    torch.save(dict(schema="fold-c246-training-erasure-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for r,state,outputs in zip(records,load_bundle(out/"trained-models.pt"),raw,strict=True):
        model=factory.new_model(r["seed"])
        if r["family"]=="gru_only":model=binding.parent_module().new_baseline(model)
        base.replay_one(model,state,r,outputs,parts,fitting=fitting,binding=binding,factory=factory)
    summary=summarize(records,base,fitting)
    for name,value in (("training-plan.json",manifest()),("split-dataset.json",parts),("measurements.json",records),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=n,sha256=a.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard();precheck(c245_summary,c244_summary,root)
    for name,wanted in protected.items():require(a.sha(name)==wanted,"modified input")
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["full_augmentation_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,network_calls=0,limitations=["Training mask supplies a relevance/copying cue; normal inference is unchanged.",
        "Normal exposures halve at fixed total presentations; no isolated internal-cause claim.","Adaptive internal fixture, not general language or core superiority."])
    validate_result(p);(out/"summary.json").write_bytes(blob(p));print("=== C246 RESULT ===",flush=True);print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(output_dir,c244_summary,expected_head):
    _,base,fitting,_,_,a=context();out=Path(output_dir);p=a.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():require(a.sha(name)==wanted,"postcheck input")
    for item in p["artifacts"]:
        child=a.safe_child(out,item["file"]);require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"artifact bytes")
    records=a.read_json(out/"measurements.json");parts,refs=load_inputs(c244_summary)
    require(a.read_json(out/"training-plan.json")==manifest() and a.read_json(out/"split-dataset.json")==parts,"plan/partition")
    require(summarize(records,base,fitting)==p["validation_summary"]==a.read_json(out/"validation-summary.json"),"summary replay")
    discrete=base.parent_module().discrete_metrics
    for r,ref in zip(records,refs,strict=True):
        require(r["initial_sha256"]==ref["initial_sha256"] and r["c244_comparator"]==ref["final"],"initial/comparator identity")
        for s in SPLITS:
            metrics=discrete(parts[s],r["predictions"][s])
            for lang,m in metrics.items():
                require(all(abs(v-r["final"][s][lang][k])<=TOL for k,v in m.items()),"saved discrete metrics")
    return p,records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for n in ("c245-summary","c244-summary","output-dir"):parser.add_argument("--"+n,type=Path,required=True)
    parser.add_argument("--expected-head",required=True);run(**vars(parser.parse_args()))


if __name__=="__main__":main()
