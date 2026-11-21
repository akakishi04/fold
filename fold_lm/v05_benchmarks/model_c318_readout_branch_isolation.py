"""C318: frozen, scale-preserving isolation of the native mean/last query branches."""
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
from torch.nn import functional as F

EXPERIMENT_ID = "C318-v5b-frozen-readout-branches"
STAGE = "V5-B-FROZEN-READOUT-BRANCHES"
BASE = "300dcb6ed45411cec6e646f732cb95ed664cf683"
PARENT_EXECUTION = "3ecd3a638726f86b294f0fe94d53a2fc5d082e01"
PARENT_SHA = "09632cda7689c9b23229ec993d19c108ac23a7bb142285cd58b11bcc713d8cb5"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c317_query_endpoint_probe.py"
PARENT_BLOB = "7ef1736df78b5dd883a331c434f5f82f1eb8ab92"
WIDE_SOURCE = "fold_lm/v05_benchmarks/model_c304_length_breadth.py"
WIDE_BLOB = "cacb5852a29171aa8079e634d929fdd54e7f4f58"
SEEDS = tuple(range(316001,316006))
ARMS = ("two_to_four","one_to_four")
MODES = ("original_before","mean_only","last_only","original_after")
SPLITS = ("TRAIN","HOLDOUT")
OWN = ("fold_lm/v05_benchmarks/model_c318_readout_branch_isolation.py",
       "tests_lm/test_v05_c318_readout_branch_isolation.py","tools/run_c318.ps1","tools/invoke_c318.ps1",
       "docs/experiment-ledger-addendum-c318-preregistration.md","docs/v5b-readout-branch-isolation-v0.1.md")
OUTPUTS = ("audit-plan.json","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10,train_steps=0,model_forward_calls=5760,row_presentations=552960,
            core_forward_calls=23040,model_state_loads=10,checkpoint_bundle_loads=1,new_checkpoint_writes=0,network_calls=0)
MANIFEST_SHA = "757879ae36418ab5b3973a18ea80902aef081c3e41b4a463f03cc841c2c3e4ad"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c317_query_endpoint_probe as parent
    p316,x=parent.context()
    return parent,p316,x


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        parent_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,wide_source=WIDE_SOURCE,wide_blob=WIDE_BLOB,
        seeds=list(SEEDS),arms=list(ARMS),modes=list(MODES),parameters=14256,slots=64,
        question="at fixed C316 weights,how do the two existing query-attention branches compare when used individually",
        intervention="duplicate native mean input or native last-byte input in both shared query projections;retain the .5 memory average",
        controls="original before/after match C316 all1..6 logits<=1e-9 and exact argmax;query-blind and English length1 unchanged",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        limits="frozen intervention,not trained alternatives or universal necessity;total coefficient unchanged,activation norm not matched",
        scored_states=30,length_partitions=300,single_diagnostics=60,paired_groups=1280,paired_normal_rows=92160,
        raw_logit_payload_bytes=1132462080,parents=44,source_pins=754,protected_inputs=1418,
        own_tests=24,modules=203,loaded_tests=5174,focused_tests=5173,excluded_test=EXCLUDED,
        dtype="CPU float64",threads=2,deterministic=True,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def parent_hashes(p,p316,x): return (PARENT_SHA,*p.parent_hashes(p316,x))


def load_parent(paths):
    p,p316,x=context(); paths=[Path(v).resolve() for v in paths]; hashes=parent_hashes(p,p316,x)
    require(len(paths)==len(hashes)==44 and all(x.c.audit.sha(v)==h for v,h in zip(paths,hashes,strict=True)),"44 parent hashes")
    with x.guarded.no_neural():
        evidence,_=p.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); p.validate_result(evidence)
        require(evidence["commit_sha"]==PARENT_EXECUTION and evidence["experiment_id"]=="C317-v5b-frozen-query-endpoint"
                and evidence["status"]=="PASS" and evidence["capability_gate_applicable"] is False,"parent semantics")
        require(len(evidence["artifacts"])==4 and {a["file"] for a in evidence["artifacts"]}==set(p.OUTPUTS),"parent artifacts")
        expected={m:{str(n):dict.fromkeys(ARMS,0 if m=="first_byte" else 4 if n==6 else 5) for n in range(2,7)} for m in ("original_before","first_byte")}
        require(evidence["validation_summary"]["length_pass_counts"]==expected,"C317 outcomes")
        _,data,prompts,anchors=p.load_parent(paths[1:])
    return evidence,data,prompts,anchors


def precheck(paths,root):
    validate_seal(); p,p316,x=context(); evidence,*_=load_parent(paths); root=Path(root).resolve()
    pins,inputs=dict(evidence["source_blobs"]),dict(evidence["input_sha256"])
    require((len(pins),len(inputs))==(748,1407) and pins.get(PARENT_SOURCE)==PARENT_BLOB and pins.get(WIDE_SOURCE)==WIDE_BLOB,"parent protection")
    for m in [p,p316,x.parent,*x.parent.context(),*x.p312.context(),*x.wide.context(),*vars(x.c).values(),x.c.factory.language_module()]:
        path=getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root): require(Path(path).resolve().relative_to(root).as_posix() in pins,"unprotected helper")
    for n,h in pins.items(): require(x.c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in inputs.items(): require(Path(n).is_file() and x.c.audit.sha(n)==h,"changed input:"+n)
    folder=Path(paths[0]).resolve().parent
    for path,h in [(folder/"summary.json",PARENT_SHA)]+[(x.c.audit.safe_child(folder,a["file"]),a["sha256"]) for a in evidence["artifacts"]]:
        require(str(path.resolve()) not in inputs and x.c.audit.sha(path)==h,"parent input"); inputs[str(path.resolve())]=h
    for n in OWN: require(n not in pins,"OWN collision"); pins[n]=x.c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    inputs.update(x.c.audit.protect_tree_files(root,pins)); require((len(pins),len(inputs))==(754,1418),"protection counts")
    print(f"registration_check = source_pins:754; protected_inputs:1418; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,inputs


def hooks(model):
    attrs=("_forward_pre_hooks","_forward_hooks","_forward_pre_hooks_with_kwargs","_forward_hooks_with_kwargs","_forward_hooks_always_called")
    return [(n,tuple(tuple(getattr(m,a)) for a in attrs)) for n,m in model.named_modules()]


@contextmanager
def branch_probe(model,wide,mode):
    require(mode in MODES and not torch.is_grad_enabled() and not any(m.training for m in model.modules())
            and not any(v.requires_grad for v in model.parameters()),"frozen mode")
    previous=hooks(model); handles=[]; state={}; stats=dict(calls=0,query_calls=0,rows=0,one_byte_rows=0)
    def begin(module,args):
        require(not state and len(args)==2,"nonreentrant call")
        tokens=args[0]; span=wide.span_mask(tokens); valid=tokens!=256
        require(tokens.shape[1]==64 and span.shape==tokens.shape and span.dtype==torch.bool and bool(span.any(1).all()),"span contract")
        pos=torch.arange(64,device=tokens.device).expand_as(tokens)
        state.update(valid=valid,span=span,last=torch.where(span,pos,-1).max(1).values,q=0)
        stats["calls"]+=1; stats["rows"]+=len(tokens); stats["one_byte_rows"]+=int((span.sum(1)==1).sum())
    def capture(module,args,out):
        require(state and "local" not in state and isinstance(out,(tuple,list)),"single encoder")
        local=out[0]*state["valid"].unsqueeze(-1).to(out[0].dtype)
        require(local.shape==(*state["valid"].shape,16) and local.dtype==torch.float64 and local.device.type=="cpu" and bool(torch.isfinite(local).all()),"local contract")
        state["local"]=local.detach().clone()
        state["mean"]=(local*state["span"][:,:,None]).sum(1)/state["span"].sum(1,keepdim=True).to(local.dtype)
        state["end"]=local[torch.arange(len(local)),state["last"]]
    def query(module,args):
        require("local" in state and len(args)==1 and state["q"] in (0,1),"two query calls")
        index=state["q"]; native=state["mean"] if index==0 else state["end"]
        require(torch.equal(args[0],native),"native query provenance")
        state["q"]+=1; stats["query_calls"]+=1
        if mode=="mean_only" and index==1: return (state["mean"],)
        if mode=="last_only" and index==0: return (state["end"],)
        return None
    def finish(module,args,out):
        try:
            if out is not None: require("local" in state and state["q"]==2,"query coverage")
        finally: state.clear()
    try:
        handles.append(model.register_forward_pre_hook(begin)); handles.append(model.backbone.local_encoder.register_forward_hook(capture))
        handles.append(model.read.query.register_forward_pre_hook(query)); handles.append(model.register_forward_hook(finish,always_call=True))
        yield stats
        require(stats["calls"]>0 and stats["query_calls"]==2*stats["calls"] and not state,"probe coverage")
    finally:
        for h in handles: h.remove()
        state.clear(); require(hooks(model)==previous,"hook restoration")


def infer_one(model,weights,anchor,data,prompts,p,x):
    model.load_state_dict(weights,strict=True); model.eval(); model.requires_grad_(False)
    fp=x.c.base.fingerprint(model); original_hooks=hooks(model); require(fp==anchor["final_sha256"],"strict checkpoint")
    raw={}; receipts={}
    for mode in MODES:
        print(f"[C318] seed={anchor['seed']} arm={anchor['arm']} mode={mode}",flush=True)
        with torch.no_grad(),x.c.p267.counted(model,x.c.core) as (calls,cores),branch_probe(model,x.wide,mode) as stats:
            raw[mode]=x.parent.evaluate(model,prompts,data,x.wide,x.c)
        require(calls==[144,13824] and cores[0]==576 and stats==dict(calls=144,query_calls=288,rows=13824,one_byte_rows=4896),"mode accounting")
        require(x.c.base.fingerprint(model)==fp and hooks(model)==original_hooks,"weights/hooks preserved"); receipts[mode]=dict(stats)
    errors=[x.parent.replay_error(raw[m],anchor["raw"],data,x.c) for m in (MODES[0],MODES[-1])]
    for m in MODES[1:3]: p.degenerate_controls(raw[MODES[0]],raw[m],data)
    return dict(seed=anchor["seed"],arm=anchor["arm"],final_sha256=fp,raw=raw,receipts=receipts,replay_errors=errors,weights_preserved=True,hooks_restored=True)


def analyze(records,anchors,data,p,x):
    require([(r["seed"],r["arm"]) for r in records]==identities() and [(r["seed"],r["arm"]) for r in anchors]==identities(),"complete cohort")
    metrics=[]; results=[]; parts=[]; single=[]; paired=[]; controls=[]
    for r,old,flag in zip(records,anchors,p.expected_parent_results(),strict=True):
        key=dict(seed=r["seed"],arm=r["arm"])
        require(r["final_sha256"]==old["final_sha256"] and r["weights_preserved"] is True and r["hooks_restored"] is True and set(r["raw"])==set(MODES),"record provenance")
        require(r["receipts"]=={m:dict(calls=144,query_calls=288,rows=13824,one_byte_rows=4896) for m in MODES},"probe receipts")
        for z in r["raw"].values(): x.parent.validate_raw(z,data,x.c)
        errors=[x.parent.replay_error(r["raw"][m],old["raw"],data,x.c) for m in (MODES[0],MODES[-1])]
        require(errors==r["replay_errors"] and all(type(e) in (int,float) and math.isfinite(e) and 0<=e<=1e-9 for e in errors),"original reproduction")
        for m in MODES[1:3]: p.degenerate_controls(r["raw"][MODES[0]],r["raw"][m],data)
        require({str(n):x.wide.score_length(data,r["raw"][MODES[-1]][str(n)],x.c)["passed"] for n in range(2,7)}==flag["length_pass"],"restored gates")
        controls.append(dict(**key,replay_errors=errors,degenerate_controls=True))
        for mode in MODES[:3]:
            raw=r["raw"][mode]; scored={str(n):x.wide.score_length(data,raw[str(n)],x.c) for n in range(2,7)}
            flags={n:z["passed"] for n,z in scored.items()}; require(all(type(v) is bool for v in flags.values()),"boolean gates")
            if mode==MODES[0]: require(flags==flag["length_pass"],"baseline gates")
            results.append(dict(**key,mode=mode,length_pass=flags,six_pass=flags["6"])); metrics.append(dict(**key,mode=mode,length_scores=scored))
            for n in range(2,7):
                local=x.diag.normalize_task(scored[str(n)],"triple",r["seed"],r["arm"])
                for split in SPLITS: parts.append(dict(**key,mode=mode,identifier_length=n,split=split,**x.diag.partition([z for z in local if z["split"]==split])))
            for split in SPLITS:
                y=torch.tensor([z["target"] for z in data[split]]); views=raw["1"][split]["repeat"]
                single.append(dict(**key,mode=mode,split=split,rows=len(y),normal_nll=float(F.cross_entropy(views["normal"],y)),correct_by_view={v:int((z.argmax(1)==y).sum()) for v,z in views.items()},capability_gate_applicable=False))
        for mode,n in itertools.product(MODES[1:3],range(1,7)):
            for split,profile,lang in itertools.product(SPLITS,x.parent.profiles(n),("en","ja")):
                ids=[i for i,z in enumerate(data[split]) if z["language"]==lang]
                counts=p.paired_counts(r["raw"][MODES[0]][str(n)][split][profile]["normal"],r["raw"][mode][str(n)][split][profile]["normal"],data[split],ids)
                paired.append(dict(**key,mode=mode,identifier_length=n,split=split,profile=profile,language=lang,**counts))
    require((len(results),len(parts),len(single),len(paired))==(30,300,60,1280) and sum(z["rows"] for z in paired)==92160,"report inventory")
    counts={m:{str(n):{a:sum(r["length_pass"][str(n)] for r in results if r["mode"]==m and r["arm"]==a) for a in ARMS} for n in range(2,7)} for m in MODES[:3]}
    return metrics,dict(cell_results=results,final_partitions=parts,single_character_diagnostics=single,paired_local_groups=paired,reproductions=controls,length_pass_counts=counts,diagnostic_complete=True,capability_gate_applicable=False,**WORK)


def runtime_preflight(paths,root):
    torch.set_num_threads(2); precheck(paths,root); p,p316,x=context(); _,data,prompts,anchors=load_parent(paths)
    states=p316.load_bundle(Path(paths[1]).resolve().parent/"trained-models.pt"); models=p316.make_models(SEEDS[0],x)
    ids=[next(i for i,r in enumerate(data["TRAIN"]) if r["language"]==lang) for lang in ("en","ja")]
    tokens=torch.stack([x.wide.prefix_tensor(prompts[str(n)]["TRAIN"][profile][i]["views"][view]) for n,profile in ((1,"repeat"),(6,"shared_prefix")) for i in ids for view in ("normal","evidence_blind","query_blind")])
    for j,arm in enumerate(ARMS):
        model=models[arm]; model.load_state_dict(states[j],strict=True); model.eval(); model.requires_grad_(False); fp=x.c.base.fingerprint(model)
        require(fp==anchors[j]["final_sha256"],"smoke checkpoint")
        with torch.no_grad():
            native=model(tokens,torch.zeros(len(tokens),dtype=torch.int64))
            for mode in MODES:
                with branch_probe(model,x.wide,mode): z=model(tokens,torch.zeros(len(tokens),dtype=torch.int64))
                x.c.p267.check_logits(z,len(tokens))
                if mode in (MODES[0],MODES[-1]): require(torch.equal(native,z),"smoke identity")
        require(fp==x.c.base.fingerprint(model),"smoke state")
    print("real_frozen_branch_isolation_probe = PASS; discarded probes only",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS" and p["diagnostic_execution_valid"] is True and all(p[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")),"diagnostic scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(754,1418) and set(OWN)<=set(p["source_blobs"]) and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(WIDE_SOURCE)==WIDE_BLOB,"result protection")
    require(len(p["artifacts"])==4 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"]; rows=s["cell_results"]
    require([(r["seed"],r["arm"],r["mode"]) for r in rows]==[(seed,arm,m) for seed,arm in identities() for m in MODES[:3]],"result cohort")
    require(all(set(r["length_pass"])==set(map(str,range(2,7))) and all(type(v) is bool for v in r["length_pass"].values()) and r["six_pass"] is r["length_pass"]["6"] for r in rows),"gate types")
    expected={m:{str(n):{a:sum(r["length_pass"][str(n)] for r in rows if r["mode"]==m and r["arm"]==a) for a in ARMS} for n in range(2,7)} for m in MODES[:3]}
    require(s["length_pass_counts"]==expected and s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False,"counts/scope")
    require(tuple(len(s[k]) for k in ("final_partitions","single_character_diagnostics","paired_local_groups","reproductions"))==(300,60,1280,10) and all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"coverage/work")


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==202,"parent modules")
    return names+["tests_lm.test_v05_c318_readout_branch_isolation"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==5174 and ids.count(EXCLUDED)==1,"loaded suite")
    return unittest.TestSuite(t for t in tests if t.id()!=EXCLUDED)


def run(*,summaries,output_dir,expected_head):
    torch.set_num_threads(2); torch.use_deterministic_algorithms(True); p,p316,x=context(); root=Path(__file__).resolve().parents[2]
    p.guard(root,expected_head,x.c); pins,inputs=precheck(summaries,root); _,data,prompts,anchors=load_parent(summaries)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    states=p316.load_bundle(Path(summaries[1]).resolve().parent/"trained-models.pt"); records=[]
    for i,seed in enumerate(SEEDS):
        models=p316.make_models(seed,x)
        for j,arm in enumerate(ARMS): records.append(infer_one(models[arm],states[2*i+j],anchors[2*i+j],data,prompts,p,x))
    metrics,s=analyze(records,anchors,data,p,x); torch.save(dict(schema="fold-c318-branches-eval-v1",records=records),out/"evaluations.pt")
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[2],metrics),(OUTPUTS[3],s)): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=x.c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    p.guard(root,expected_head,x.c); precheck(summaries,root)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,source_blobs=pins,input_sha256=inputs,artifacts=artifacts,validation_summary=s,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C318 COMPACT DIAGNOSTIC RECEIPT ===",flush=True); print(json.dumps(dict(experiment_id=EXPERIMENT_ID,commit_sha=expected_head,status="PASS",summary_sha256=x.c.audit.sha(out/"summary.json"),artifacts=artifacts),indent=2),flush=True)
    return result


def verify_artifacts(outdir,summaries,expected_head):
    p,_,x=context(); out=Path(outdir); result=x.c.audit.read_json(out/"summary.json"); validate_result(result)
    require(result["commit_sha"]==expected_head,"execution HEAD")
    for n,h in result["input_sha256"].items(): require(x.c.audit.sha(n)==h,"protected input")
    for a in result["artifacts"]:
        path=x.c.audit.safe_child(out,a["file"]); require(x.c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with x.guarded.no_neural():
        _,data,_,anchors=load_parent(summaries); archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c318-branches-eval-v1","archive schema")
        metrics,s=analyze(archive["records"],anchors,data,p,x)
        for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[2],metrics),(OUTPUTS[3],s)): require(x.c.audit.read_json(out/n)==v,"persisted:"+n)
    require(result["validation_summary"]==s,"summary reconstruction"); return result,metrics


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--summaries",nargs=44,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True); parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
