"""C317: replace the frozen readout's final query-byte anchor by its first byte."""
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

EXPERIMENT_ID = "C317-v5b-frozen-query-endpoint"
STAGE = "V5-B-FROZEN-QUERY-ENDPOINT"
BASE = "590edfc7b00fadf894cc5ce629294259843de5de"
PARENT_EXECUTION = "233b2aeefb540fd71ca2e8ab81d57f2088a063b1"
PARENT_SHA = "875d6dedbaf6e5de8ca998f6a94dfb2f39dbcf5b92a6c5527334d906dc149814"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c316_single_mix_replication.py"
PARENT_BLOB = "3d15bda5b0c4f3f487548cd6b92d3b1281febb76"
WIDE_SOURCE = "fold_lm/v05_benchmarks/model_c304_length_breadth.py"
WIDE_BLOB = "cacb5852a29171aa8079e634d929fdd54e7f4f58"
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
PROMPTS_SHA = "2a850d72af8c99321fd3dd4243ec2d01df6fda0bb2696329e29e3995a487fffd"
SEEDS = tuple(range(316001,316006))
ARMS = ("two_to_four","one_to_four")
MODES = ("original_before","first_byte","original_after")
SCORED_MODES = MODES[:2]
SPLITS = ("TRAIN","HOLDOUT")
VIEWS = ("normal","evidence_blind","query_blind")
OWN = ("fold_lm/v05_benchmarks/model_c317_query_endpoint_probe.py",
       "tests_lm/test_v05_c317_query_endpoint_probe.py","tools/run_c317.ps1","tools/invoke_c317.ps1",
       "docs/experiment-ledger-addendum-c317-preregistration.md","docs/v5b-query-endpoint-probe-v0.1.md")
OUTPUTS = ("audit-plan.json","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10,train_steps=0,model_forward_calls=4320,row_presentations=414720,
            core_forward_calls=17280,model_state_loads=10,checkpoint_bundle_loads=1,
            new_checkpoint_writes=0,network_calls=0)
MANIFEST_SHA = "10f2e095d09f6ffeb424b2d91c0215aabf8739caace720c4f6662cb4f73a1d10"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c316_single_mix_replication as parent
    return parent,parent.context()


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        parent_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,
        wide_source=WIDE_SOURCE,wide_blob=WIDE_BLOB,seeds=list(SEEDS),arms=list(ARMS),modes=list(MODES),
        question="at fixed C316 states,how does replacing only the last query-byte anchor by the first change predictions",
        intervention="actual C304 forward;first read.query call stays span mean;second input changes last-byte local state to first-byte local state",
        scope="bytes,not Unicode characters;no target labels in forward;untrained inference intervention,not a trained replacement",
        controls="original before/after match all1..6 parent logits<=1e-9 and exact argmax;all query-blind and English length1 outputs identical across endpoints",
        parameters=14256,slots=64,profiles_at_one=1,profiles_at_other_lengths=3,
        data_sha256=DATA_SHA,prompts_sha256=PROMPTS_SHA,raw_logit_payload_bytes=849346560,
        scored_states=20,length_partitions=200,single_diagnostics=40,paired_local_groups=640,paired_normal_rows=46080,
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        interpretation="diagnostic fidelity only;endpoint change may help or harm;no proof that training can exploit it or of component necessity",
        parents=43,source_pins=748,protected_inputs=1407,own_tests=32,modules=202,loaded_tests=5150,focused_tests=5149,
        excluded_test=EXCLUDED,dtype="CPU float64",threads=2,deterministic=True,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def expected_parent_results():
    return [dict(seed=s,arm=a,length_pass={str(n):not(n==6 and ((s==316002 and a==ARMS[0]) or (s==316003 and a==ARMS[1]))) for n in range(2,7)},
        six_pass=not((s==316002 and a==ARMS[0]) or (s==316003 and a==ARMS[1])),
        all_2_to_6_pass=not((s==316002 and a==ARMS[0]) or (s==316003 and a==ARMS[1]))) for s,a in identities()]


def parent_hashes(parent,x): return (PARENT_SHA,*parent.parent_hashes(x.parent))


def load_parent(paths):
    parent,x=context(); paths=[Path(p).resolve() for p in paths]; hashes=parent_hashes(parent,x)
    require(len(paths)==len(hashes)==43 and all(x.c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)),"43 parent hashes")
    with x.guarded.no_neural():
        p,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); parent.validate_result(p)
        require(p["experiment_id"]=="C316-v5b-single-mix-replication" and p["status"]=="FAIL" and p["commit_sha"]==PARENT_EXECUTION
                and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(WIDE_SOURCE)==WIDE_BLOB,"parent identity")
        require(len(p["artifacts"])==7 and {a["file"] for a in p["artifacts"]}==set(parent.OUTPUTS),"parent outputs")
        s=p["validation_summary"]
        require(s["seed_results"]==expected_parent_results() and s["candidate_gate"] is False and s["all_pairs_matched"] is True and s["all_replays"] is True,"parent outcomes")
        data=x.c.audit.read_json(paths[0].parent/"dataset.json"); prompts=x.c.audit.read_json(paths[0].parent/"length-datasets.json")
        require(digest(data)==DATA_SHA and digest(prompts)==PROMPTS_SHA,"canonical input hashes")
        x.c.p267.validate_data(data)
        x.parent.validate_prompts(data,prompts,{str(n):prompts[str(n)] for n in (2,3,4,5)},prompts["6"],x.p313,x.wide)
        archive=torch.load(paths[0].parent/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c316-single-replication-eval-v1"
                and [(r["seed"],r["arm"]) for r in archive["records"]]==identities(),"parent final-evaluation archive")
    return p,data,prompts,archive["records"]


def precheck(paths,root):
    validate_seal(); parent,x=context(); p,_,_,_=load_parent(paths); root=Path(root).resolve()
    pins,inputs=dict(p["source_blobs"]),dict(p["input_sha256"])
    require((len(pins),len(inputs))==(742,1393) and pins.get(PARENT_SOURCE)==PARENT_BLOB and pins.get(WIDE_SOURCE)==WIDE_BLOB
            and all(pins.get(n)==h for n,h in x.parent.PINNED.items()) and all(pins.get(n)==h for n,h in x.wide.PINNED.items()),"inherited protection")
    for m in [parent,x.parent,*x.parent.context(),*x.p312.context(),*x.wide.context(),*vars(x.c).values(),x.c.factory.language_module()]:
        path=getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root): require(Path(path).resolve().relative_to(root).as_posix() in pins,"unprotected helper")
    for n,h in pins.items(): require(x.c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in inputs.items(): require(Path(n).is_file() and x.c.audit.sha(n)==h,"changed input:"+n)
    folder=Path(paths[0]).resolve().parent
    for path,h in [(folder/"summary.json",PARENT_SHA)]+[(x.c.audit.safe_child(folder,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in inputs and x.c.audit.sha(path)==h,"parent input"); inputs[str(path.resolve())]=h
    for n in OWN: require(n not in pins,"OWN collision"); pins[n]=x.c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    inputs.update(x.c.audit.protect_tree_files(root,pins)); require((len(pins),len(inputs))==(748,1407),"protection counts")
    print(f"registration_check = source_pins:748; protected_inputs:1407; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,inputs


def hook_snapshot(model):
    attrs=("_forward_pre_hooks","_forward_hooks","_forward_pre_hooks_with_kwargs","_forward_hooks_with_kwargs","_forward_hooks_always_called")
    return [(n,tuple(tuple(getattr(m,a)) for a in attrs)) for n,m in model.named_modules()]


@contextmanager
def endpoint_probe(model,wide,first_byte):
    """Observe native call provenance; replace only the second shared query projection input."""
    require(type(first_byte) is bool and not torch.is_grad_enabled() and not any(m.training for m in model.modules())
            and not any(p.requires_grad for p in model.parameters()),"frozen inference only")
    before=hook_snapshot(model); handles=[]; state={}
    stats=dict(calls=0,query_calls=0,rows=0,different_positions=0)
    def begin(module,args):
        require(not state and len(args)==2,"non-reentrant model call")
        tokens=args[0]; span=wide.span_mask(tokens); valid=tokens!=256
        require(tokens.shape[1]==64 and span.dtype==torch.bool and span.shape==tokens.shape and bool(span.any(1).all()),"query span")
        pos=torch.arange(64,device=tokens.device).expand_as(tokens)
        state.update(valid=valid,span=span,first=torch.where(span,pos,64).min(1).values,last=torch.where(span,pos,-1).max(1).values,q=0)
        stats["calls"]+=1; stats["rows"]+=len(tokens)
        stats["different_positions"]+=int((state["first"]!=state["last"]).sum())
    def capture(module,args,out):
        require(state and "local" not in state and isinstance(out,(tuple,list)) and len(out)>0,"single local encoder")
        local=out[0]*state["valid"].unsqueeze(-1).to(out[0].dtype)
        require(local.shape==(*state["valid"].shape,16) and local.dtype==torch.float64 and local.device.type=="cpu"
                and bool(torch.isfinite(local).all()),"local representation")
        state["local"]=local.detach().clone()
    def query(module,args):
        require("local" in state and len(args)==1 and state["q"] in (0,1),"two query calls")
        local=state["local"]; rows=torch.arange(len(local)); span=state["span"]
        wanted=(local*span[:,:,None]).sum(1)/span.sum(1,keepdim=True).to(local.dtype) if state["q"]==0 else local[rows,state["last"]]
        require(torch.equal(args[0],wanted),"native query-input provenance")
        index=state["q"]; state["q"]+=1; stats["query_calls"]+=1
        if index==1 and first_byte: return (local[rows,state["first"]],)
        return None
    def finish(module,args,out):
        try:
            if out is not None: require("local" in state and state["q"]==2,"completed query coverage")
        finally: state.clear()
    try:
        handles.append(model.register_forward_pre_hook(begin))
        handles.append(model.backbone.local_encoder.register_forward_hook(capture))
        handles.append(model.read.query.register_forward_pre_hook(query))
        handles.append(model.register_forward_hook(finish,always_call=True))
        yield stats
        require(stats["calls"]>0 and stats["query_calls"]==2*stats["calls"] and not state,"probe coverage")
    finally:
        for h in handles: h.remove()
        state.clear(); require(hook_snapshot(model)==before,"hook restoration")


def degenerate_controls(before,changed,data):
    for n in before:
        for s,p in itertools.product(SPLITS,before[n]["TRAIN"]):
            require(torch.equal(before[n][s][p]["query_blind"],changed[n][s][p]["query_blind"]),"query-blind endpoint identity")
    for s in SPLITS:
        ids=[i for i,r in enumerate(data[s]) if r["language"]=="en"]
        for v in VIEWS: require(torch.equal(before["1"][s]["repeat"][v][ids],changed["1"][s]["repeat"][v][ids]),"English one-byte identity")


def infer_one(model,state,anchor,data,prompts,x):
    model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(False)
    fp=x.c.base.fingerprint(model); hooks=hook_snapshot(model)
    require(fp==anchor["final_sha256"],"strict checkpoint")
    raw={}; attestations={}
    for mode in MODES:
        print(f"[C317] seed={anchor['seed']} arm={anchor['arm']} mode={mode}",flush=True)
        with torch.no_grad(),x.c.p267.counted(model,x.c.core) as (calls,cores),endpoint_probe(model,x.wide,mode=="first_byte") as stats:
            raw[mode]=x.parent.evaluate(model,prompts,data,x.wide,x.c)
        require(calls==[144,13824] and cores[0]==576 and stats==dict(calls=144,query_calls=288,rows=13824,different_positions=8928),"mode accounting")
        require(x.c.base.fingerprint(model)==fp and hook_snapshot(model)==hooks,"frozen state/hooks")
        attestations[mode]=dict(stats)
    errors=[x.parent.replay_error(raw[n],anchor["raw"],data,x.c) for n in (MODES[0],MODES[2])]
    degenerate_controls(raw[MODES[0]],raw[MODES[1]],data)
    return dict(seed=anchor["seed"],arm=anchor["arm"],final_sha256=fp,raw=raw,attestations=attestations,
                replay_errors=errors,weights_preserved=True,hooks_restored=True)


def paired_counts(left,right,rows,ids):
    y=torch.tensor([r["target"] for r in rows],dtype=torch.int64)[ids]
    a=left[ids].argmax(1); z=right[ids].argmax(1); ac=a==y; zc=z==y
    d=dict(rows=len(ids),left_correct=int(ac.sum()),right_correct=int(zc.sum()),rescued=int((~ac&zc).sum()),
           regressed=int((ac&~zc).sum()),both_wrong=int((~ac&~zc).sum()),argmax_flips=int((a!=z).sum()))
    require(d["right_correct"]-d["left_correct"]==d["rescued"]-d["regressed"],"paired conservation")
    return d


def analyze(records,anchors,data,x):
    require([(r["seed"],r["arm"]) for r in records]==identities() and [(r["seed"],r["arm"]) for r in anchors]==identities(),"complete cohort")
    metrics=[]; results=[]; parts=[]; single=[]; paired=[]; controls=[]
    for r,old,flag in zip(records,anchors,expected_parent_results(),strict=True):
        key=dict(seed=r["seed"],arm=r["arm"])
        require(r["final_sha256"]==old["final_sha256"] and r["weights_preserved"] is True and r["hooks_restored"] is True
                and set(r["raw"])==set(MODES),"record provenance")
        expected={n:dict(calls=144,query_calls=288,rows=13824,different_positions=8928) for n in MODES}
        require(r["attestations"]==expected,"hook receipts")
        for raw in r["raw"].values(): x.parent.validate_raw(raw,data,x.c)
        errors=[x.parent.replay_error(r["raw"][n],old["raw"],data,x.c) for n in (MODES[0],MODES[2])]
        require(errors==r["replay_errors"] and all(type(e) in (int,float) and math.isfinite(e) and 0<=e<=1e-9 for e in errors),"original reproduction")
        degenerate_controls(r["raw"][MODES[0]],r["raw"][MODES[1]],data)
        restored={str(n):x.wide.score_length(data,r["raw"][MODES[2]][str(n)],x.c)["passed"] for n in range(2,7)}
        require(restored==flag["length_pass"],"restored gates")
        controls.append(dict(**key,replay_errors=errors,degenerate_controls=True))
        for mode in SCORED_MODES:
            raw=r["raw"][mode]; scored={str(n):x.wide.score_length(data,raw[str(n)],x.c) for n in range(2,7)}
            flags={n:z["passed"] for n,z in scored.items()}; require(all(type(v) is bool for v in flags.values()),"length flags")
            if mode==MODES[0]: require(flags==flag["length_pass"],"original gates")
            results.append(dict(**key,mode=mode,length_pass=flags,six_pass=flags["6"]))
            metrics.append(dict(**key,mode=mode,length_scores=scored))
            for n in range(2,7):
                normal=x.diag.normalize_task(scored[str(n)],"triple",r["seed"],r["arm"])
                for s in SPLITS: parts.append(dict(**key,mode=mode,identifier_length=n,split=s,**x.diag.partition([p for p in normal if p["split"]==s])))
            for s in SPLITS:
                views=raw["1"][s]["repeat"]; y=torch.tensor([z["target"] for z in data[s]],dtype=torch.int64)
                single.append(dict(**key,mode=mode,split=s,rows=len(y),normal_nll=float(F.cross_entropy(views["normal"],y)),
                    correct_by_view={v:int((z.argmax(1)==y).sum()) for v,z in views.items()},capability_gate_applicable=False))
        for n in range(1,7):
            for s,p,language in itertools.product(SPLITS,x.parent.profiles(n),("en","ja")):
                ids=[i for i,row in enumerate(data[s]) if row["language"]==language]
                d=paired_counts(r["raw"][MODES[0]][str(n)][s][p]["normal"],r["raw"][MODES[1]][str(n)][s][p]["normal"],data[s],ids)
                paired.append(dict(**key,identifier_length=n,split=s,profile=p,language=language,**d))
    require((len(results),len(parts),len(single),len(paired))==(20,200,40,640) and sum(p["rows"] for p in paired)==46080,"report inventory")
    counts={m:{str(n):{a:sum(r["length_pass"][str(n)] for r in results if r["mode"]==m and r["arm"]==a) for a in ARMS} for n in range(2,7)} for m in SCORED_MODES}
    return metrics,dict(cell_results=results,final_partitions=parts,single_character_diagnostics=single,paired_local_groups=paired,reproductions=controls,
        length_pass_counts=counts,diagnostic_complete=True,capability_gate_applicable=False,**WORK)


def runtime_preflight(paths,root):
    torch.set_num_threads(2); precheck(paths,root); parent,x=context(); _,data,prompts,anchors=load_parent(paths)
    states=parent.load_bundle(Path(paths[0]).resolve().parent/"trained-models.pt"); models=parent.make_models(SEEDS[0],x)
    ids=[next(i for i,r in enumerate(data["TRAIN"]) if r["language"]==lang) for lang in ("en","ja")]
    tokens=torch.stack([x.wide.prefix_tensor(prompts[str(n)]["TRAIN"][p][i]["views"][v]) for n,p in ((1,"repeat"),(6,"shared_suffix")) for i in ids for v in VIEWS])
    for j,arm in enumerate(ARMS):
        model=models[arm]; model.load_state_dict(states[j],strict=True); model.eval(); model.requires_grad_(False); fp=x.c.base.fingerprint(model)
        require(fp==anchors[j]["final_sha256"],"smoke checkpoint")
        with torch.no_grad():
            original=model(tokens,torch.zeros(len(tokens),dtype=torch.int64))
            with endpoint_probe(model,x.wide,False): observed=model(tokens,torch.zeros(len(tokens),dtype=torch.int64))
            with endpoint_probe(model,x.wide,True): altered=model(tokens,torch.zeros(len(tokens),dtype=torch.int64))
            restored=model(tokens,torch.zeros(len(tokens),dtype=torch.int64))
        x.c.p267.check_logits(altered,len(tokens)); require(torch.equal(original,observed) and torch.equal(original,restored) and fp==x.c.base.fingerprint(model),"smoke provenance/restoration")
    print("real_frozen_query_endpoint_probe = PASS; operational smoke only",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS" and p["diagnostic_execution_valid"] is True
            and all(p[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")),"diagnostic scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(748,1407) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(WIDE_SOURCE)==WIDE_BLOB,"result protection")
    require(len(p["artifacts"])==4 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"]; rr=s["cell_results"]
    require([(r["seed"],r["arm"],r["mode"]) for r in rr]==[(a,b,m) for a,b in identities() for m in SCORED_MODES],"result cohort")
    require(all(set(r["length_pass"])==set(map(str,range(2,7))) and all(type(v) is bool for v in r["length_pass"].values()) and r["six_pass"] is r["length_pass"]["6"] for r in rr),"result flags")
    require([r["length_pass"] for r in rr if r["mode"]==MODES[0]]==[f["length_pass"] for f in expected_parent_results()],"parent gate receipts")
    expected={m:{str(n):{a:sum(r["length_pass"][str(n)] for r in rr if r["mode"]==m and r["arm"]==a) for a in ARMS} for n in range(2,7)} for m in SCORED_MODES}
    require(s["length_pass_counts"]==expected and s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False,"counts/scope")
    require((len(s["final_partitions"]),len(s["single_character_diagnostics"]),len(s["paired_local_groups"]),len(s["reproductions"]))==(200,40,640,10),"result inventory")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"workload")


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==201,"parent modules")
    return names+["tests_lm.test_v05_c317_query_endpoint_probe"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==5150 and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED]; require(len(kept)==5149,"focused suite"); return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    torch.set_num_threads(2); torch.use_deterministic_algorithms(True); parent,x=context(); root=Path(__file__).resolve().parents[2]
    guard(root,expected_head,x.c); pins,inputs=precheck(summaries,root); _,data,prompts,anchors=load_parent(summaries)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    states=parent.load_bundle(Path(summaries[0]).resolve().parent/"trained-models.pt"); records=[]
    for i,seed in enumerate(SEEDS):
        models=parent.make_models(seed,x)
        for j,arm in enumerate(ARMS): records.append(infer_one(models[arm],states[2*i+j],anchors[2*i+j],data,prompts,x))
    metrics,s=analyze(records,anchors,data,x)
    torch.save(dict(schema="fold-c317-endpoint-eval-v1",records=records),out/"evaluations.pt")
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[2],metrics),(OUTPUTS[3],s)): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=x.c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,x.c); precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=inputs,artifacts=artifacts,validation_summary=s,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p)); receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","artifacts")}
    receipt["summary_sha256"]=x.c.audit.sha(out/"summary.json"); print("=== C317 COMPACT DIAGNOSTIC RECEIPT ===",flush=True); print(json.dumps(receipt,sort_keys=True,indent=2),flush=True); return p


def verify_artifacts(outdir,summaries,expected_head):
    _,x=context(); out=Path(outdir); p=x.c.audit.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items(): require(x.c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=x.c.audit.safe_child(out,a["file"]); require(x.c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with x.guarded.no_neural():
        _,data,_,anchors=load_parent(summaries); archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c317-endpoint-eval-v1","evaluation schema")
        metrics,s=analyze(archive["records"],anchors,data,x)
        for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[2],metrics),(OUTPUTS[3],s)): require(x.c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==s,"summary reconstruction"); return p,metrics


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--summaries",nargs=43,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True); parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
