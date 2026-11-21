"""C321: frozen name binding with equal endpoints and equal character multisets."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path
from types import ModuleType
import unittest
import torch

EXPERIMENT_ID = "C321-v5b-frozen-interior-name-order"
STAGE = "V5-B-FROZEN-INTERIOR-NAME-ORDER"
BASE = "8785a88b70a14a4b8d632ff520a03977eb73f129"
PARENT_EXECUTION = "0e4687acfa72355cbddc47c3ceb98700354fe34d"
PARENT_SHA = "9e41e82228f26cf525ee54e4097abd493a339641d6b3d3f5b2a6d10ba8868431"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c320_unequal_name_lengths.py"
PARENT_BLOB = "5e183c330c883d8c44d9cd66ac2b89365517f9cc"
MODEL_SOURCE = "fold_lm/v05_benchmarks/model_c319_trained_last_readout.py"
MODEL_BLOB = "8222ddc165464b8acb84380f47d397504308a9df"
SEEDS = tuple(range(319001,319006))
ARMS = ("mean_last","last_only")
PROFILES = ("u_dominant","balanced","v_dominant")
SCORER_PROFILES = ("repeat","shared_prefix","shared_suffix")
PATTERNS = (("uuvu","uvuu"),("uuvv","uvuv"),("vuvv","vvuv"))
SPLITS = ("TRAIN","HOLDOUT")
VIEWS = ("normal","evidence_blind","query_blind")
MODES = ("before","interior","after")
OWN = ("fold_lm/v05_benchmarks/model_c321_interior_name_order.py",
       "tests_lm/test_v05_c321_interior_name_order.py","tools/run_c321.ps1","tools/invoke_c321.ps1",
       "docs/experiment-ledger-addendum-c321-preregistration.md","docs/v5b-interior-name-order-v0.1.md")
OUTPUTS = ("evaluation-plan.json","interior-prompts.json","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10,train_steps=0,model_forward_calls=3150,row_presentations=302400,
            core_forward_calls=12600,model_state_loads=10,checkpoint_bundle_loads=1,new_checkpoint_writes=0,network_calls=0)
MANIFEST_SHA = "813f7283535086c9b7ebd416da1fb1d50b5240ece9d58e364173b4cb4d433fea"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c320_unequal_name_lengths as parent
    model,x = parent.context()
    return parent,model,x


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        parent_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,model_source=MODEL_SOURCE,model_blob=MODEL_BLOB,
        seeds=list(SEEDS),arms=list(ARMS),profiles={k:list(v) for k,v in zip(PROFILES,PATTERNS,strict=True)},
        scorer_adapter=dict(zip(PROFILES,SCORER_PROFILES,strict=True)),
        question="can frozen models bind names when endpoints,length and character counts match but interior order differs",
        primary="all5 mean_last states pass all three profiles under every original local/masked criterion",
        controls="C319 original1..6 before/after <=1e-9 and exact argmax;own trained policy and weights preserved",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        parameters=14256,slots=64,name_length=4,max_prompt_bytes=43,max_encoded_tokens=45,normal_inputs=864,
        new_training=False,new_vocabulary=False,model_selection=False,primary_arm="mean_last",
        limits="same checkpoints and synthetic value split;new name-order distribution,not universal identity matching or fresh-seed replication",
        parents=47,source_pins=772,protected_inputs=1455,own_tests=24,modules=206,loaded_tests=5246,focused_tests=5245,
        excluded_test=EXCLUDED,raw_logit_payload_bytes=619315200,dtype="CPU float64",threads=2,deterministic=True,
        gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal(): require(len(MANIFEST_SHA)==64 and digest(manifest())==MANIFEST_SHA,"manifest seal")


def name_pair(row,profile):
    require(profile in PROFILES and row["language"] in ("en","ja"),"name policy")
    i,j=row["entities"]; chars="abc" if row["language"]=="en" else "甲乙丙"; table={"u":chars[i],"v":chars[j]}
    a,b=("".join(table[c] for c in pattern) for pattern in PATTERNS[PROFILES.index(profile)])
    require(a!=b and len(a)==len(b)==4 and a[0]==b[0] and a[-1]==b[-1] and Counter(a)==Counter(b),"matched names")
    return {i:a,j:b}


def render(row,profile,view="normal"):
    require(view in VIEWS,"view"); names=name_pair(row,profile); values=dict(zip(row["entities"],row["values"],strict=True))
    return ";".join(names[k]+"="+("?" if view=="evidence_blind" else str(values[k])) for k in row["permutation"])+";"+("?" if view=="query_blind" else names[row["query"]])+"="


def new_prompts(data):
    return {s:{p:[dict(source_id=r["id"],target=r["target"],views={v:render(r,p,v) for v in VIEWS}) for r in data[s]] for p in PROFILES} for s in SPLITS}


def check_prompts(data,old,new,parent,x):
    require(digest(data)==parent.DATA_SHA and digest(old)==parent.PROMPTS_SHA and new==new_prompts(data),"canonical inputs")
    old_normal={r["views"]["normal"] for length in old.values() for split in length.values() for rows in split.values() for r in rows}
    vocabulary=set("".join(old_normal).encode("utf-8")) | {ord("?")}; seen=[]; maximum=0
    for s,p in itertools.product(SPLITS,PROFILES):
        for row,item in zip(data[s],new[s][p],strict=True):
            seen.append(item["views"]["normal"])
            for view,text in item["views"].items():
                raw=text.encode("utf-8"); maximum=max(maximum,len(raw)); tokens=x.wide.prefix_tensor(text)
                require(set(raw)<=vocabulary and tokens.shape==(64,) and tokens.dtype==torch.int64 and int(tokens[0])==257
                        and int(tokens[len(raw)+1])==258 and tokens[1:len(raw)+1].tolist()==list(raw) and bool((tokens[len(raw)+2:]==256).all()),"exact input bytes")
                q="?" if view=="query_blind" else name_pair(row,p)[row["query"]]
                require(tokens[x.wide.span_mask(tokens[None,:])[0]].tolist()==list(q.encode("utf-8")),"actual query span")
    require(maximum==43 and len(seen)==len(set(seen))==864 and not set(seen)&old_normal,"novel input coverage")


def load_parent(paths):
    parent,model,x=context(); paths=[Path(p).resolve() for p in paths]; hashes=(PARENT_SHA,*parent.parent_hashes(model))
    require(len(paths)==len(hashes)==47 and all(x.c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)),"47 parent hashes")
    with x.guarded.no_neural():
        evidence,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); parent.validate_result(evidence)
        require(evidence["experiment_id"]=="C320-v5b-frozen-unequal-name-lengths" and evidence["commit_sha"]==PARENT_EXECUTION
                and evidence["status"]=="PASS" and evidence["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity")
        require(len(evidence["artifacts"])==5 and {a["file"] for a in evidence["artifacts"]}==set(parent.OUTPUTS),"parent writer")
        expected=[dict(seed=s,arm=a,layout_pass={k:not(s==319002 and a=="last_only" and k=="short_long") for k in ("short_long","long_short")},all_layouts_pass=not(s==319002 and a=="last_only")) for s,a in identities()]
        require(evidence["validation_summary"]["seed_results"]==expected and evidence["validation_summary"]["primary_gate"] is True,"parent outcomes")
        _,data,old,anchors=parent.load_parent(paths[1:])
        check_prompts(data,old,new_prompts(data),parent,x)
    return evidence,data,old,anchors


def precheck(paths,root):
    validate_seal(); parent,model,x=context(); evidence,*_=load_parent(paths); root=Path(root).resolve()
    pins,inputs=dict(evidence["source_blobs"]),dict(evidence["input_sha256"])
    require((len(pins),len(inputs))==(766,1443) and pins.get(PARENT_SOURCE)==PARENT_BLOB and pins.get(MODEL_SOURCE)==MODEL_BLOB,"inherited protection")
    for m in [parent,model,*model.context(),x.parent,*x.parent.context(),*x.p312.context(),*x.wide.context(),*vars(x.c).values(),x.c.factory.language_module()]:
        path=getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root): require(Path(path).resolve().relative_to(root).as_posix() in pins,"unprotected helper")
    for n,h in pins.items(): require(x.c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"source changed:"+n)
    for n,h in inputs.items(): require(Path(n).is_file() and x.c.audit.sha(n)==h,"input changed:"+n)
    folder=Path(paths[0]).resolve().parent
    for path,h in [(folder/"summary.json",PARENT_SHA)]+[(x.c.audit.safe_child(folder,a["file"]),a["sha256"]) for a in evidence["artifacts"]]:
        require(str(path.resolve()) not in inputs and x.c.audit.sha(path)==h,"parent input"); inputs[str(path.resolve())]=h
    for n in OWN: require(n not in pins,"OWN collision"); pins[n]=x.c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    inputs.update(x.c.audit.protect_tree_files(root,pins)); require((len(pins),len(inputs))==(772,1455),"protection inventory")
    print(f"registration_check = source_pins:772; protected_inputs:1455; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,inputs


def evaluate_new(model,prompts,data,x):
    require(not torch.is_grad_enabled() and not any(m.training for m in model.modules()) and not any(v.requires_grad for v in model.parameters()),"frozen evaluation")
    raw={s:{p:{} for p in PROFILES} for s in SPLITS}
    for s,p,v in itertools.product(SPLITS,PROFILES,VIEWS):
        chunks=[]
        for start in range(0,len(data[s]),96):
            tokens=torch.stack([x.wide.prefix_tensor(r["views"][v]) for r in prompts[s][p][start:start+96]])
            z=model(tokens,torch.zeros(len(tokens),dtype=torch.int64)); x.c.p267.check_logits(z,len(tokens)); chunks.append(z.detach().clone())
        raw[s][p][v]=torch.cat(chunks)
    return raw


def score_new(raw,data,x):
    require(set(raw)==set(SPLITS) and all(set(raw[s])==set(PROFILES) for s in SPLITS),"new domain")
    for s,p in itertools.product(SPLITS,PROFILES):
        require(set(raw[s][p])==set(VIEWS),"views")
        for z in raw[s][p].values(): x.c.p267.check_logits(z,len(data[s])); require(not z.requires_grad,"detached logits")
    # Scorer labels are opaque profile slots; this adapter never changes model inputs or rows.
    adapted={s:{old:raw[s][new] for new,old in zip(PROFILES,SCORER_PROFILES,strict=True)} for s in SPLITS}
    return x.wide.score_length(data,adapted,x.c)


def infer_one(model,state,anchor,data,old,new,owner,x):
    require(anchor["readout_policy"]==anchor["arm"] and anchor["arm"] in ARMS,"trained policy")
    model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(False)
    fp=x.c.base.fingerprint(model); hooks=owner.hook_snapshot(model); require(fp==anchor["final_sha256"],"strict checkpoint")
    raw={}; receipts={}
    for mode in MODES:
        print(f"[C321] seed={anchor['seed']} arm={anchor['arm']} mode={mode}",flush=True)
        with torch.no_grad(),x.c.p267.counted(model,x.c.core) as (calls,cores),owner.trained_readout(model,x.wide,anchor["arm"]) as stats:
            raw[mode]=evaluate_new(model,new,data,x) if mode=="interior" else x.parent.evaluate(model,old,data,x.wide,x.c)
        n=27 if mode=="interior" else 144
        require(calls==[n,96*n] and cores[0]==4*n and stats==dict(calls=n,query_calls=2*n,rows=96*n,grad_calls=0),"work/policy")
        require(fp==x.c.base.fingerprint(model) and hooks==owner.hook_snapshot(model),"state/hooks changed"); receipts[mode]=dict(stats)
    errors=[x.parent.replay_error(raw[m],anchor["raw"],data,x.c) for m in ("before","after")]
    return dict(seed=anchor["seed"],arm=anchor["arm"],readout_policy=anchor["arm"],final_sha256=fp,raw=raw,
                receipts=receipts,replay_errors=errors,weights_preserved=True,hooks_restored=True)


def analyze(records,anchors,data,parent,x):
    require([(r["seed"],r["arm"]) for r in records]==identities() and [(r["seed"],r["arm"]) for r in anchors]==identities(),"complete cohort")
    results=[]; parts=[]; metrics=[]; controls=[]
    for r,a,flag in zip(records,anchors,parent.expected_parent_results(),strict=True):
        require(r["readout_policy"]==a["readout_policy"]==r["arm"] and r["final_sha256"]==a["final_sha256"]
                and r["weights_preserved"] is True and r["hooks_restored"] is True and set(r["raw"])==set(MODES),"provenance")
        require(r["receipts"]=={m:dict(calls=n,query_calls=2*n,rows=96*n,grad_calls=0) for m,n in zip(MODES,(144,27,144),strict=True)},"receipts")
        errors=[x.parent.replay_error(r["raw"][m],a["raw"],data,x.c) for m in ("before","after")]
        require(errors==r["replay_errors"] and all(type(e) in (int,float) and math.isfinite(e) and 0<=e<=1e-9 for e in errors),"reproduction")
        for m in ("before","after"):
            require({str(n):x.wide.score_length(data,r["raw"][m][str(n)],x.c)["passed"] for n in range(2,7)}==flag["length_pass"],"old gates")
        score=score_new(r["raw"]["interior"],data,x); require(type(score["passed"]) is bool,"gate type")
        key=dict(seed=r["seed"],arm=r["arm"]); local=x.diag.normalize_task(score,"triple",r["seed"],r["arm"])
        for s in SPLITS: parts.append(dict(**key,split=s,**x.diag.partition([v for v in local if v["split"]==s])))
        metrics.append(dict(**key,scorer_profile_map=dict(zip(PROFILES,SCORER_PROFILES,strict=True)),score=score))
        results.append(dict(**key,interior_pass=score["passed"])); controls.append(dict(**key,replay_errors=errors,matched=True))
    counts={a:sum(r["interior_pass"] for r in results if r["arm"]==a) for a in ARMS}
    return metrics,dict(seed_results=results,final_partitions=parts,reproductions=controls,pass_counts=counts,
        primary_arm="mean_last",primary_gate=counts["mean_last"]==5,all_replays=True,**WORK)


def runtime_preflight(paths,root):
    torch.set_num_threads(2); precheck(paths,root); _,owner,x=context(); _,data,old,anchors=load_parent(paths); new=new_prompts(data)
    states=owner.load_bundle(Path(paths[1]).resolve().parent/"trained-models.pt"); models=owner.make_models(SEEDS[0],x)
    ids=[next(i for i,r in enumerate(data["TRAIN"]) if r["language"]==lang) for lang in ("en","ja")]
    oldx=torch.stack([x.wide.prefix_tensor(old["4"]["TRAIN"]["repeat"][i]["views"]["normal"]) for i in ids])
    newx=torch.stack([x.wide.prefix_tensor(new["TRAIN"][p][i]["views"][v]) for p,i,v in itertools.product(PROFILES,ids,VIEWS)])
    for j,arm in enumerate(ARMS):
        model=models[arm]; model.load_state_dict(states[j],strict=True); model.eval(); model.requires_grad_(False); fp=x.c.base.fingerprint(model)
        require(fp==anchors[j]["final_sha256"],"smoke checkpoint"); hooks=owner.hook_snapshot(model)
        with torch.no_grad(),owner.trained_readout(model,x.wide,arm):
            a=model(oldx,torch.zeros(2,dtype=torch.int64)); z=model(newx,torch.zeros(len(newx),dtype=torch.int64)); after=model(oldx,torch.zeros(2,dtype=torch.int64))
        x.c.p267.check_logits(z,len(newx)); require(torch.equal(a,after) and fp==x.c.base.fingerprint(model) and hooks==owner.hook_snapshot(model),"smoke restoration")
    print("real_interior_order_policy_probe = PASS; discarded probes only",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True and p["gate_f_candidate"] is False and p["production_adoption"] is False,"result scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(772,1455) and set(OWN)<=set(p["source_blobs"]) and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(MODEL_SOURCE)==MODEL_BLOB,"protection")
    require(len(p["artifacts"])==5 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"]; rows=s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rows]==identities() and all(type(r["interior_pass"]) is bool for r in rows),"result cohort")
    counts={a:sum(r["interior_pass"] for r in rows if r["arm"]==a) for a in ARMS}; gate=counts["mean_last"]==5
    require(s["pass_counts"]==counts and s["primary_arm"]=="mean_last" and s["primary_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"primary")
    require(len(s["final_partitions"])==20 and len(s["reproductions"])==10 and s["all_replays"] is True and all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"work/coverage")


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==205,"parent modules")
    return names+["tests_lm.test_v05_c321_interior_name_order"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==5246 and ids.count(EXCLUDED)==1,"loaded suite")
    return unittest.TestSuite(t for t in tests if t.id()!=EXCLUDED)


def run(*,summaries,output_dir,expected_head):
    torch.set_num_threads(2); torch.use_deterministic_algorithms(True); parent,owner,x=context(); root=Path(__file__).resolve().parents[2]
    owner.context()[1].guard(root,expected_head,x.c); pins,inputs=precheck(summaries,root); _,data,old,anchors=load_parent(summaries); new=new_prompts(data)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False); states=owner.load_bundle(Path(summaries[1]).resolve().parent/"trained-models.pt"); records=[]
    for i,seed in enumerate(SEEDS):
        models=owner.make_models(seed,x)
        for j,arm in enumerate(ARMS): records.append(infer_one(models[arm],states[2*i+j],anchors[2*i+j],data,old,new,owner,x))
    metrics,s=analyze(records,anchors,data,parent,x); torch.save(dict(schema="fold-c321-interior-eval-v1",records=records),out/"evaluations.pt")
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],new),(OUTPUTS[3],metrics),(OUTPUTS[4],s)): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=x.c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    owner.context()[1].guard(root,expected_head,x.c); precheck(summaries,root)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if s["primary_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=inputs,artifacts=artifacts,validation_summary=s,gate_f_candidate=False,production_adoption=False)
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C321 COMPACT EXPERIMENT RECEIPT ===",flush=True)
    print(json.dumps(dict(experiment_id=EXPERIMENT_ID,commit_sha=expected_head,status=result["status"],summary_sha256=x.c.audit.sha(out/"summary.json"),artifacts=artifacts),indent=2),flush=True)
    return result


def verify_artifacts(outdir,summaries,expected_head):
    parent,_,x=context(); out=Path(outdir); result=x.c.audit.read_json(out/"summary.json"); validate_result(result); require(result["commit_sha"]==expected_head,"execution HEAD")
    for n,h in result["input_sha256"].items(): require(x.c.audit.sha(n)==h,"protected input")
    for a in result["artifacts"]:
        path=x.c.audit.safe_child(out,a["file"]); require(x.c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with x.guarded.no_neural():
        _,data,_,anchors=load_parent(summaries); archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c321-interior-eval-v1","archive schema")
        metrics,s=analyze(archive["records"],anchors,data,parent,x)
        for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],new_prompts(data)),(OUTPUTS[3],metrics),(OUTPUTS[4],s)): require(x.c.audit.read_json(out/n)==v,"persisted:"+n)
    require(result["validation_summary"]==s,"summary reconstruction"); return result,metrics


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--summaries",nargs=47,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True); parser.add_argument("--expected-head",required=True); run(**vars(parser.parse_args()))


if __name__=="__main__": main()
