"""C302: cross frozen C301 common weights with unit and TRAIN-learned gains."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
from types import ModuleType
import unittest
import torch

EXPERIMENT_ID = "C302-v5b-frozen-gain-weight-cross"
STAGE = "V5-B-FROZEN-GAIN-WEIGHT-CROSS"
BASE = "400dd5337c6e30fe901b91d4587d16d7c12f9c0b"
PARENT_EXECUTION = "d67c900c588ff0e4c8974cd8f80721da381a8770"
PARENT_SHA = "19d5a94c3ce5d2bef94683b05983c44b1e76f452490e184f8ffde7b934d559c1"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c301_learned_residual_gain.py"
PARENT_BLOB = "a1c2baa1762b57be32eff4b4b9828bd7e5da340f"
READOUT_SOURCE = "fold_lm/v05_benchmarks/model_c278_mean_final_dual_query.py"
READOUT_BLOB = "0aa8d65874f4a021e21d04948ffd0a1d5615248b"
SEEDS = tuple(range(301001,301006))
ARMS = ("fixed_gain","learned_gain")
GAIN_LABELS = ("unit","trained")
PASSES = ("original_before","swapped","original_after")
TASKS = ("two_char","triple","quad")
SPLITS = ("TRAIN","HOLDOUT")
OWN = ("fold_lm/v05_benchmarks/model_c302_frozen_gain_cross.py",
       "tests_lm/test_v05_c302_frozen_gain_cross.py","tools/run_c302.ps1","tools/invoke_c302.ps1",
       "docs/experiment-ledger-addendum-c302-preregistration.md","docs/v5b-frozen-gain-cross-v0.1.md")
OUTPUTS = ("gain-plan.json","gain-evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10,train_steps=0,model_forward_calls=2430,row_presentations=233280,
            core_forward_calls=9720,model_state_loads=10,checkpoint_bundle_loads=1,
            new_checkpoint_writes=0,network_calls=0)
MANIFEST_SHA = "283f4ac996eda2ac866a192408fff2368782b8592d350c11af33723f874f2960"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c301_learned_residual_gain as parent
    _,audit,diagnostic,evaluation,transfer,training,c = parent.context()
    return parent,audit,diagnostic,evaluation,transfer,training,c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        parent_summary_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,
        readout_source=READOUT_SOURCE,readout_blob=READOUT_BLOB,seeds=list(SEEDS),weight_arms=list(ARMS),gain_labels=list(GAIN_LABELS),
        passes=list(PASSES),question="does exchanging the final TRAIN-learned gain at fixed weights rescue or regress the original outcomes",
        gain_source="unit1 and each seed's exact C301 learned_gain fit.final_gain;no evaluation-derived gain search",
        implementation="strict-load original wrapper;evaluate its actual C278 inner model with temporary alpha*r+a hook;never mutate parameters",
        controls="original before/after reproduce parent logits<=1e-9 and exact argmax at every task/view;full wrapper fingerprints/hooks unchanged",
        cohort="all10 learned states;5 seed-specific2x2 weight/gain crosses;not fresh replication",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        interpretation="immediate frozen-gain intervention versus whole-training-policy weight differences;not a unique training mechanism or automatic adoption",
        results=30,partitions=180,within_weight_comparisons=60,across_weight_comparisons=60,matched_normal_rows=51840,
        raw_logit_payload_bytes=477757440,parents=28,source_pins=658,protected_inputs=1217,
        own_tests=32,modules=187,loaded_tests=4670,focused_tests=4669,excluded_test=EXCLUDED,
        dtype="CPU float64",threads=2,deterministic=True,capability_gate_applicable=False,gate_f_candidate=False,
        production_adoption=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def valid_gain(value):
    require(type(value) in (int,float) and math.isfinite(value) and 0.<=value<=2.,"finite gain in [0,2]")
    return float(value)


def pass_plan(arm,trained_gain):
    require(arm in ARMS,"weight arm"); trained_gain=valid_gain(trained_gain)
    original,other=(GAIN_LABELS if arm==ARMS[0] else GAIN_LABELS[::-1])
    gains=dict(unit=1.,trained=trained_gain)
    return [(name,label,gains[label]) for name,label in zip(PASSES,(original,other,original),strict=True)]


def hook_snapshot(model):
    attrs=("_forward_pre_hooks","_forward_hooks","_forward_pre_hooks_with_kwargs","_forward_hooks_with_kwargs","_forward_hooks_always_called")
    return tuple((n,tuple(tuple(getattr(m,a)) for a in attrs)) for n,m in model.named_modules())


@contextmanager
def frozen_gain(model,alpha):
    """Instrument actual C278,not C301's outer wrapper; original learned state stays untouched."""
    alpha=valid_gain(alpha)
    require(not torch.is_grad_enabled() and not any(m.training for m in model.modules())
            and not any(p.requires_grad for p in model.parameters()),"frozen inference only")
    norm=model.backbone.readout_norm; before=hook_snapshot(model); state={}; late=[]; handles=[]
    stats=dict(calls=0,formula_checks=0)
    def begin(module,args):
        require(not state and not late,"reentrant hook"); state["batch"]=len(args[0]); stats["calls"]+=1
    def capture_r(module,args):
        require("batch" in state and "r" not in state and len(args)==1,"residual capture"); state["r"]=args[0].detach().clone()
    def capture_a(module,args,output):
        require("r" in state and "a" not in state,"reader capture"); state["a"]=output.detach().clone()
    def replace(module,args):
        require(set(state)=={"batch","r","a"} and len(args)==1,"sum coverage"); r,a=state["r"],state["a"]
        require(r.shape==a.shape==args[0].shape==(state["batch"],16) and r.dtype==a.dtype==torch.float64
                and r.device.type==a.device.type=="cpu" and bool(torch.isfinite(r).all()) and bool(torch.isfinite(a).all()),"summand contract")
        require(torch.equal(args[0],r+a),"actual C278 sum identity"); stats["formula_checks"]+=1
        return None if alpha==1. else (r.new_tensor(alpha)*r+a,)
    def arm_late(module,args,output):
        require("batch" in state and not late,"local encoder count"); late.append(norm.register_forward_pre_hook(replace))
    def finish(module,args,output):
        for h in late: h.remove()
        late.clear(); state.clear()
    try:
        handles.append(model.register_forward_pre_hook(begin))
        handles.append(norm.register_forward_pre_hook(capture_r))
        handles.append(model.read.output.register_forward_hook(capture_a))
        handles.append(model.backbone.local_encoder.register_forward_hook(arm_late))
        handles.append(model.register_forward_hook(finish,always_call=True))
        yield stats
        require(stats["calls"]>0 and stats["calls"]==stats["formula_checks"] and not state and not late,"hook call coverage")
    finally:
        for h in late+handles: h.remove()
        require(hook_snapshot(model)==before,"hook restoration")


def expected_parent_counts():
    return {t:dict(fixed_gain=2,learned_gain=1 if t=="quad" else 3) for t in TASKS}


def adapt_anchors(payload,records):
    summary=payload["validation_summary"]; results=summary["seed_results"]
    require([(r["seed"],r["arm"]) for r in records]==identities()
            and [(r["seed"],r["arm"]) for r in results]==identities(),"parent cohort")
    require(summary["task_pass_counts"]==expected_parent_counts() and summary["candidate_gate"] is False
            and summary["all_pairs_matched"] is True and summary["all_replays"] is True,"parent results")
    gains={}; flags={}
    for r,s in zip(records,results,strict=True):
        arm=r["arm"]; gain=valid_gain(r["fit"]["final_gain"])
        require(gain==s["final_gain"] and r["parameters"]==(14256 if arm==ARMS[0] else 14257)
                and r["checkpoint_roundtrip"] is True and re.fullmatch(r"[0-9a-f]{64}",r["final_sha256"]) is not None,"parent state metadata")
        f={t:s[t+"_pass"] for t in TASKS}; require(all(type(v) is bool for v in f.values()),"parent flags")
        flags[(r["seed"],arm)]=f
        if arm==ARMS[0]: require(gain==1.,"parent fixed gain")
        else: gains[r["seed"]]=gain
    require(set(gains)==set(SEEDS),"five TRAIN gains")
    return gains,flags


def load_parent(paths):
    parent,audit,*_,c=context(); paths=[Path(p).resolve() for p in paths]
    hashes=(PARENT_SHA,*parent.parent_hashes(parent.context()[0]))
    require(len(paths)==len(hashes)==28 and all(c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)),"parent hashes")
    with audit.no_neural():
        payload,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); parent.validate_result(payload)
        require(payload["experiment_id"]=="C301-v5b-learned-residual-gain" and payload["commit_sha"]==PARENT_EXECUTION
                and payload["status"]=="FAIL" and payload["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB
                and payload["source_blobs"].get(READOUT_SOURCE)==READOUT_BLOB,"parent identity")
        require(len(payload["artifacts"])==8 and {a["file"] for a in payload["artifacts"]}==set(parent.OUTPUTS),"parent artifacts")
        data=[c.audit.read_json(paths[0].parent/n) for n in ("dataset.json","triple-dataset.json","quad-dataset.json")]
        archive=torch.load(paths[0].parent/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c301-gain-eval-v1","parent archive")
        gains,flags=adapt_anchors(payload,archive["records"])
    return payload,*data,archive["records"],gains,flags


def precheck(paths,root):
    validate_seal(); payload,*_=load_parent(paths); parent,audit,*_,c=context(); root=Path(root).resolve()
    pins=dict(payload["source_blobs"]); protected=dict(payload["input_sha256"])
    require((len(pins),len(protected))==(652,1202),"inherited counts"); covered=set()
    for n,h in pins.items(): require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in protected.items(): require(Path(n).is_file() and c.audit.sha(n)==h,"changed input:"+n)
    for module in [parent,audit,*parent.context(),*vars(c).values()]:
        path=getattr(module,"__file__",None) if isinstance(module,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            n=Path(path).resolve().relative_to(root).as_posix(); require(n in pins,"unprotected helper:"+n); covered.add(n)
    require(PARENT_SOURCE in covered and pins[READOUT_SOURCE]==READOUT_BLOB,"direct source coverage")
    directory=Path(paths[0]).resolve().parent
    for path,h in [(directory/"summary.json",PARENT_SHA)]+[(c.audit.safe_child(directory,a["file"]),a["sha256"]) for a in payload["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h,"parent input"); protected[str(path.resolve())]=h
    for n in OWN:
        require(n not in pins,"OWN collision"); pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins)); require((len(pins),len(protected))==(658,1217),"protection counts")
    print(f"registration_check = source_pins:658; protected_inputs:1217; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def infer_state(wrapper,state,anchor,trained_gain,data,triple,quad,evaluation,transfer,c):
    wrapper.load_state_dict(state,strict=True); wrapper.eval(); wrapper.requires_grad_(False)
    start=c.base.fingerprint(wrapper); original=valid_gain(anchor["fit"]["final_gain"])
    require(start==anchor["final_sha256"] and float(wrapper.gain().detach())==original,"strict original state/gain")
    before=hook_snapshot(wrapper); outputs={}; attestations={}; alphas={}; labels={}
    for name,label,alpha in pass_plan(anchor["arm"],trained_gain):
        print(f"[C302] seed={anchor['seed']} weights={anchor['arm']} pass={name} gain={alpha:.9f}",flush=True)
        with torch.no_grad(),c.p267.counted(wrapper.model,c.core) as (calls,cores),frozen_gain(wrapper.model,alpha) as stats:
            raw=evaluation.evaluate(wrapper.model,data,triple,quad,transfer,c)
        require(calls==[81,7776] and cores[0]==324 and stats==dict(calls=81,formula_checks=81),"mode counts")
        require(c.base.fingerprint(wrapper)==start and float(wrapper.gain().detach())==original and hook_snapshot(wrapper)==before,"frozen state/hooks")
        outputs[name]=raw; attestations[name]=dict(stats); alphas[name]=alpha; labels[name]=label
    errors=[evaluation.replay_error(outputs[n],anchor["raw"],data,c) for n in (PASSES[0],PASSES[2])]
    errors.append(evaluation.replay_error(outputs[PASSES[0]],outputs[PASSES[2]],data,c))
    return dict(seed=anchor["seed"],arm=anchor["arm"],final_sha256=start,original_gain=original,trained_gain=trained_gain,
        pass_gains=alphas,pass_labels=labels,raw=outputs,attestations=attestations,reproduction_errors=errors,weights_preserved=True,hooks_restored=True)


def compare_normal(left,right,rows):
    require(set(left)==set(right),"comparison profiles"); totals=dict(rows=0,argmax_flips=0,rescued=0,regressed=0,left_correct=0,right_correct=0)
    y=torch.tensor([r["target"] for r in rows],dtype=torch.int64)
    for profile in left:
        a,b=left[profile]["normal"],right[profile]["normal"]
        require(a.shape==b.shape==(len(rows),256),"comparison shape")
        x,z=a.argmax(1),b.argmax(1); ca,cb=x==y,z==y
        for k,v in dict(rows=len(rows),argmax_flips=int((x!=z).sum()),rescued=int((~ca&cb).sum()),regressed=int((ca&~cb).sum()),
                        left_correct=int(ca.sum()),right_correct=int(cb.sum())).items(): totals[k]+=v
    require(totals["right_correct"]-totals["left_correct"]==totals["rescued"]-totals["regressed"],"paired counts")
    return totals


def analyze(records,anchors,gains,flags,data,diagnostic,evaluation,transfer,c):
    require([(r["seed"],r["arm"]) for r in records]==identities()
            and [(r["seed"],r["arm"]) for r in anchors]==identities(),"complete cohort")
    metrics=[]; parts=[]; results=[]; reproductions=[]; lookup={}; within=[]; across=[]
    for r,old in zip(records,anchors,strict=True):
        key=dict(seed=r["seed"],arm=r["arm"]); plan=pass_plan(r["arm"],gains[r["seed"]])
        require(r["final_sha256"]==old["final_sha256"] and r["original_gain"]==old["fit"]["final_gain"]
                and r["trained_gain"]==gains[r["seed"]] and r["weights_preserved"] is True and r["hooks_restored"] is True,"record provenance")
        require(set(r["raw"])==set(PASSES) and r["pass_gains"]=={n:a for n,_,a in plan}
                and r["pass_labels"]=={n:l for n,l,_ in plan}
                and r["attestations"]=={n:dict(calls=81,formula_checks=81) for n in PASSES},"pass contract")
        errors=[evaluation.replay_error(r["raw"][n],old["raw"],data,c) for n in (PASSES[0],PASSES[2])]
        errors.append(evaluation.replay_error(r["raw"][PASSES[0]],r["raw"][PASSES[2]],data,c))
        require(errors==r["reproduction_errors"] and all(type(e) in (int,float) and math.isfinite(e) and 0<=e<=1e-9 for e in errors),"original reproduction")
        reproductions.append(dict(**key,errors=errors,matched=True))
        for name,label,alpha in plan:
            raw=r["raw"][name]; require(set(raw)==set(TASKS),"tasks")
            scored=dict(two_char=c.p267.score(data,raw["two_char"]),triple=c.c270.score(data,raw["triple"],c.p267),quad=transfer.score_quad(data,raw["quad"],c))
            ff={t:scored[t]["passed"] for t in TASKS}; require(all(type(v) is bool for v in ff.values()),"flags")
            if name!=PASSES[1]: require(ff==flags[(r["seed"],r["arm"])],"original task gates")
            result=dict(**key,pass_name=name,gain_label=label,gain=alpha,all_tasks_pass=all(ff.values()),**{t+"_pass":v for t,v in ff.items()})
            results.append(result); metrics.append(dict(**key,pass_name=name,**scored))
            if name!=PASSES[2]: lookup[(r["seed"],r["arm"],label)]=raw
            for task in TASKS:
                normalized=diagnostic.normalize_task(scored[task],task,r["seed"],r["arm"]+":"+name)
                for split in SPLITS:
                    part=diagnostic.partition([p for p in normalized if p["split"]==split])
                    parts.append(dict(**key,pass_name=name,gain_label=label,task=task,split=split,**part))
    for seed,arm,task,split in itertools.product(SEEDS,ARMS,TASKS,SPLITS):
        within.append(dict(seed=seed,arm=arm,task=task,split=split,left_gain="unit",right_gain="trained",
            **compare_normal(lookup[(seed,arm,"unit")][task][split],lookup[(seed,arm,"trained")][task][split],data[split])))
    for seed,label,task,split in itertools.product(SEEDS,GAIN_LABELS,TASKS,SPLITS):
        across.append(dict(seed=seed,gain_label=label,task=task,split=split,left_weights=ARMS[0],right_weights=ARMS[1],
            **compare_normal(lookup[(seed,ARMS[0],label)][task][split],lookup[(seed,ARMS[1],label)][task][split],data[split])))
    counts={arm:{label:{task:sum(r[task+"_pass"] for r in results if r["arm"]==arm and r["gain_label"]==label and r["pass_name"]!=PASSES[2]) for task in TASKS} for label in GAIN_LABELS} for arm in ARMS}
    require((len(results),len(parts),len(within),len(across))==(30,180,60,60) and sum(r["rows"] for r in within+across)==51840,"inventory")
    s=dict(cell_results=results,final_partitions=parts,within_weight=within,across_weight=across,reproductions=reproductions,
        task_pass_counts=counts,trained_gains=[dict(seed=s,gain=gains[s]) for s in SEEDS],diagnostic_complete=True,
        capability_gate_applicable=False,all_weights_preserved=True,all_hooks_restored=True,**WORK)
    return metrics,s


def runtime_preflight(paths,root):
    precheck(paths,root); parent,*_,training,c=context(); _,data,_,_,anchors,gains,_=load_parent(paths)
    states=parent.load_bundle(Path(paths[0]).resolve().parent/"trained-models.pt"); models=parent.make_models(SEEDS[0],c)
    x=training.training_tables(data,c)[0][0,0,:48]; tasks=torch.zeros(48,dtype=torch.int64)
    for i,arm in enumerate(ARMS):
        m=models[arm]; m.load_state_dict(states[i],strict=True); m.eval(); m.requires_grad_(False)
        start=c.base.fingerprint(m); require(start==anchors[i]["final_sha256"],"real checkpoint")
        with torch.no_grad():
            plain=m(x,tasks)
            for name,_,alpha in pass_plan(arm,gains[SEEDS[0]]):
                with frozen_gain(m.model,alpha): z=m.model(x,tasks)
                c.p267.check_logits(z,48)
                if name!=PASSES[1]: require(torch.equal(plain,z),"real wrapper/inner identity")
        require(c.base.fingerprint(m)==start,"smoke state")
    print("real_fixed_and_learned_wrapper_gain_cross = PASS; operational smoke only",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS" and p["diagnostic_execution_valid"] is True,"result identity")
    require(all(p[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")),"scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(658,1217) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(READOUT_SOURCE)==READOUT_BLOB,"result protection")
    require(len(p["artifacts"])==4 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"]; rr=s["cell_results"]
    require([(r["seed"],r["arm"],r["pass_name"]) for r in rr]==[(seed,arm,n) for seed,arm in identities() for n in PASSES],"result ordering")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"workload")
    require((len(s["final_partitions"]),len(s["within_weight"]),len(s["across_weight"]),len(s["reproductions"]))==(180,60,60,10),"result inventory")
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False and s["all_weights_preserved"] is True and s["all_hooks_restored"] is True,"result flags")
    require([r["seed"] for r in s["trained_gains"]]==list(SEEDS),"gain cohort")
    gains={r["seed"]:valid_gain(r["gain"]) for r in s["trained_gains"]}
    for seed,arm in identities():
        records=[r for r in rr if (r["seed"],r["arm"])==(seed,arm)]
        require([(r["pass_name"],r["gain_label"],r["gain"]) for r in records]==pass_plan(arm,gains[seed]),"result gain mapping")
        require(all(type(r[t+"_pass"]) is bool for r in records for t in TASKS)
                and all(records[0][t+"_pass"]==records[2][t+"_pass"] for t in TASKS),"restored gates")
    expected={a:{l:{t:sum(r[t+"_pass"] for r in rr if r["arm"]==a and r["gain_label"]==l and r["pass_name"]!=PASSES[2]) for t in TASKS} for l in GAIN_LABELS} for a in ARMS}
    require(s["task_pass_counts"]==expected,"count reconstruction")
    for t in TASKS:
        require(expected[ARMS[0]]["unit"][t]==expected_parent_counts()[t][ARMS[0]] and expected[ARMS[1]]["trained"][t]==expected_parent_counts()[t][ARMS[1]],"original aggregate gates")
    require([(r["seed"],r["arm"]) for r in s["reproductions"]]==identities(),"reproduction cohort")
    for r in s["reproductions"]:
        require(r["matched"] is True and len(r["errors"])==3 and all(type(e) in (int,float) and math.isfinite(e) and 0<=e<=1e-9 for e in r["errors"]),"reproduction bounds")


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==186,"parent modules")
    return names+["tests_lm.test_v05_c302_frozen_gain_cross"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==4670 and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED]; require(len(kept)==4669,"focused suite"); return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    parent,_,diag,evaluation,transfer,_,c=context(); root=Path(__file__).resolve().parents[2]
    guard(root,expected_head,c); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected=precheck(summaries,root); _,data,triple,quad,anchors,gains,flags=load_parent(summaries)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    states=parent.load_bundle(Path(summaries[0]).resolve().parent/"trained-models.pt"); records=[]
    for i,seed in enumerate(SEEDS):
        models=parent.make_models(seed,c)
        for j,arm in enumerate(ARMS):
            k=2*i+j; records.append(infer_state(models[arm],states[k],anchors[k],gains[seed],data,triple,quad,evaluation,transfer,c))
    metrics,s=analyze(records,anchors,gains,flags,data,diag,evaluation,transfer,c)
    torch.save(dict(schema="fold-c302-gain-cross-eval-v1",records=records),out/OUTPUTS[1])
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[2],metrics),(OUTPUTS[3],s)): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c); precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=s,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p)); receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","artifacts")}
    receipt["summary_sha256"]=c.audit.sha(out/"summary.json"); print("=== C302 COMPACT DIAGNOSTIC RECEIPT ===",flush=True); print(json.dumps(receipt,indent=2,sort_keys=True),flush=True); return p


def verify_artifacts(outdir,summaries,expected_head):
    _,audit,diag,evaluation,transfer,_,c=context(); out=Path(outdir); p=c.audit.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items(): require(c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"]); require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with audit.no_neural():
        _,data,_,_,anchors,gains,flags=load_parent(summaries)
        archive=torch.load(out/OUTPUTS[1],map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c302-gain-cross-eval-v1","evaluation schema")
        metrics,s=analyze(archive["records"],anchors,gains,flags,data,diag,evaluation,transfer,c)
        for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[2],metrics),(OUTPUTS[3],s)): require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==s,"summary reconstruction"); return p,metrics


def main():
    p=argparse.ArgumentParser(); p.add_argument("--summaries",nargs=28,type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True); p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__=="__main__": main()
