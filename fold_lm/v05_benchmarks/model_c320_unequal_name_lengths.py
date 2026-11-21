"""C320: frozen transfer to unequal name lengths within the trained length range."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
from types import ModuleType
import unittest
import torch

EXPERIMENT_ID = "C320-v5b-frozen-unequal-name-lengths"
STAGE = "V5-B-FROZEN-UNEQUAL-NAME-LENGTHS"
BASE = "1c60afa5997ca9f61a6f5b44e73a31e2b15cd609"
PARENT_EXECUTION = "529c54ef63b1015b25632b8123a9a552eebcd263"
PARENT_SHA = "48815ca382d0da078da12ec2d54f2c42261e94498b682f679d8f46d746ec0580"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c319_trained_last_readout.py"
PARENT_BLOB = "8222ddc165464b8acb84380f47d397504308a9df"
WIDE_SOURCE = "fold_lm/v05_benchmarks/model_c304_length_breadth.py"
WIDE_BLOB = "cacb5852a29171aa8079e634d929fdd54e7f4f58"
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
PROMPTS_SHA = "2a850d72af8c99321fd3dd4243ec2d01df6fda0bb2696329e29e3995a487fffd"
SEEDS = tuple(range(319001,319006))
ARMS = ("mean_last","last_only")
PRIMARY_ARM = "mean_last"
LAYOUTS = {"short_long":(2,4),"long_short":(4,2)}
PROFILES = ("repeat","shared_prefix","shared_suffix")
SPLITS = ("TRAIN","HOLDOUT")
VIEWS = ("normal","evidence_blind","query_blind")
OWN = ("fold_lm/v05_benchmarks/model_c320_unequal_name_lengths.py",
       "tests_lm/test_v05_c320_unequal_name_lengths.py","tools/run_c320.ps1","tools/invoke_c320.ps1",
       "docs/experiment-ledger-addendum-c320-preregistration.md","docs/v5b-unequal-name-lengths-v0.1.md")
OUTPUTS = ("evaluation-plan.json","unequal-prompts.json","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10,train_steps=0,model_forward_calls=3420,row_presentations=328320,
            core_forward_calls=13680,model_state_loads=10,checkpoint_bundle_loads=1,new_checkpoint_writes=0,network_calls=0)
MANIFEST_SHA = "34ac7cbac03191c2e64ae05887f7d04cbc90c3cf0a73e18427708c1bbeed307d"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c319_trained_last_readout as parent
    return parent,parent.context()[-1]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        parent_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,wide_blob=WIDE_BLOB,
        seeds=list(SEEDS),arms=list(ARMS),layouts={k:list(v) for k,v in LAYOUTS.items()},primary_arm=PRIMARY_ARM,
        question="can frozen equal-name-length-trained models handle two and four character names within one question",
        policy="retain each C319 trained readout in every old/new evaluation;no intervention or training",
        controls="original1..6 before/after match saved C319 logits<=1e-9 and exact argmax;old per-state gates unchanged",
        primary="all5 retained mean_last states pass both unequal layouts under every original local/masked criterion",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        parameters=14256,slots=64,max_new_prompt_bytes=37,max_new_encoded_tokens=39,new_normal_inputs=1728,
        data_sha256=DATA_SHA,old_prompts_sha256=PROMPTS_SHA,old_lengths=[1,2,3,4,5,6],
        parent_models="all10,including last_only319005;no model or per-query selection",
        limits="new within-question length composition;not longer names,new vocabulary,fresh seeds or proof of arbitrary reasoning",
        scored_conditions=20,partitions=40,reproductions=10,raw_logit_payload_bytes=672399360,
        parents=46,source_pins=766,protected_inputs=1443,own_tests=24,modules=205,loaded_tests=5222,focused_tests=5221,
        excluded_test=EXCLUDED,dtype="CPU float64",threads=2,deterministic=True,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal(): require(len(MANIFEST_SHA)==64 and digest(manifest())==MANIFEST_SHA,"manifest seal")


def render(row,lengths,profile,view="normal"):
    require(len(lengths)==2 and all(type(n) is int and 1<=n<=6 for n in lengths) and profile in PROFILES and view in VIEWS,"render policy")
    require(row["language"] in ("en","ja"),"language")
    i,j=row["entities"]; n,m=lengths; chars="abc" if row["language"]=="en" else "甲乙丙"; u,v=chars[i],chars[j]
    names={i:u*n,j:v*m if profile=="repeat" else u*(m-1)+v if profile=="shared_prefix" else v+u*(m-1)}
    require(names[i]!=names[j],"distinct names")
    values=dict(zip(row["entities"],row["values"],strict=True))
    return ";".join(names[k]+"="+("?" if view=="evidence_blind" else str(values[k])) for k in row["permutation"])+";"+("?" if view=="query_blind" else names[row["query"]])+"="


def new_prompts(data):
    return {k:{s:{p:[dict(source_id=r["id"],target=r["target"],views={v:render(r,ll,p,v) for v in VIEWS}) for r in data[s]]
                   for p in PROFILES} for s in SPLITS} for k,ll in LAYOUTS.items()}


def check_prompts(data,old,new,x):
    require(digest(data)==DATA_SHA and digest(old)==PROMPTS_SHA and new==new_prompts(data),"canonical prompts")
    seen=set(); vocabulary=set()
    for n in range(1,7):
        for s,p in itertools.product(SPLITS,x.parent.profiles(n)):
            for row,item in zip(data[s],old[str(n)][s][p],strict=True):
                require(item["source_id"]==row["id"] and item["target"]==row["target"] and set(item["views"])==set(VIEWS),"old identity")
                for v,text in item["views"].items():
                    require(text==render(row,(n,n),p,v),"equal-length renderer compatibility")
                    vocabulary.update(text.encode("utf-8"))
                seen.add(item["views"]["normal"])
    normal=[]; maximum=0
    for k,s,p in itertools.product(LAYOUTS,SPLITS,PROFILES):
        for row,item in zip(data[s],new[k][s][p],strict=True):
            normal.append(item["views"]["normal"])
            for v,text in item["views"].items():
                raw=text.encode("utf-8"); maximum=max(maximum,len(raw)); tokens=x.wide.prefix_tensor(text)
                require(set(raw)<=vocabulary and tokens.shape==(64,) and tokens.dtype==torch.int64 and int(tokens[0])==257
                        and int(tokens[len(raw)+1])==258 and torch.equal(tokens[1:len(raw)+1],torch.tensor(list(raw),dtype=torch.int64))
                        and bool((tokens[len(raw)+2:]==256).all()),"bytes/BOS/EOS/padding")
                query="?" if v=="query_blind" else text.rsplit(";",1)[1][:-1]
                span=x.wide.span_mask(tokens[None,:])[0]
                require(tokens[span].tolist()==list(query.encode("utf-8")),"actual query span")
    require(maximum==37 and len(normal)==len(set(normal))==1728 and not set(normal)&seen,"new layout coverage")


def expected_parent_results():
    return [dict(seed=s,arm=a,length_pass={str(n):not(s==319005 and a=="last_only" and n==6) for n in range(2,7)},
        six_pass=not(s==319005 and a=="last_only"),all_2_to_6_pass=not(s==319005 and a=="last_only")) for s,a in identities()]


def parent_hashes(p): return (PARENT_SHA,*p.parent_hashes(*p.context()))


def load_parent(paths):
    p,x=context(); paths=[Path(v).resolve() for v in paths]; hashes=parent_hashes(p)
    require(len(paths)==len(hashes)==46 and all(x.c.audit.sha(v)==h for v,h in zip(paths,hashes,strict=True)),"46 parent hashes")
    with x.guarded.no_neural():
        evidence,_=p.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); p.validate_result(evidence)
        require(evidence["experiment_id"]=="C319-v5b-trained-last-readout" and evidence["commit_sha"]==PARENT_EXECUTION
                and evidence["status"]=="FAIL" and evidence["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity")
        require(len(evidence["artifacts"])==7 and {a["file"] for a in evidence["artifacts"]}==set(p.OUTPUTS),"parent writer contract")
        s=evidence["validation_summary"]
        require(s["seed_results"]==expected_parent_results() and s["candidate_gate"] is False and s["all_pairs_matched"] is True and s["all_replays"] is True,"parent outcomes")
        folder=paths[0].parent; data=x.c.audit.read_json(folder/"dataset.json"); old=x.c.audit.read_json(folder/"length-datasets.json")
        x.c.p267.validate_data(data); check_prompts(data,old,new_prompts(data),x)
        archive=torch.load(folder/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c319-trained-readout-eval-v1"
                and [(r["seed"],r["arm"]) for r in archive["records"]]==identities(),"parent evaluation schema")
        require(all(r["readout_policy"]==r["arm"] for r in archive["records"]),"trained policies")
    return evidence,data,old,archive["records"]


def precheck(paths,root):
    validate_seal(); p,x=context(); evidence,*_=load_parent(paths); root=Path(root).resolve()
    pins,inputs=dict(evidence["source_blobs"]),dict(evidence["input_sha256"])
    require((len(pins),len(inputs))==(760,1429) and pins.get(PARENT_SOURCE)==PARENT_BLOB and pins.get(WIDE_SOURCE)==WIDE_BLOB,"inherited protection")
    for m in [p,*p.context(),x.parent,*x.parent.context(),*x.p312.context(),*x.wide.context(),*vars(x.c).values(),x.c.factory.language_module()]:
        path=getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root): require(Path(path).resolve().relative_to(root).as_posix() in pins,"unprotected helper")
    for n,h in pins.items(): require(x.c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in inputs.items(): require(Path(n).is_file() and x.c.audit.sha(n)==h,"changed input:"+n)
    folder=Path(paths[0]).resolve().parent
    for path,h in [(folder/"summary.json",PARENT_SHA)]+[(x.c.audit.safe_child(folder,a["file"]),a["sha256"]) for a in evidence["artifacts"]]:
        require(str(path.resolve()) not in inputs and x.c.audit.sha(path)==h,"parent input"); inputs[str(path.resolve())]=h
    for n in OWN: require(n not in pins,"OWN collision"); pins[n]=x.c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    inputs.update(x.c.audit.protect_tree_files(root,pins)); require((len(pins),len(inputs))==(766,1443),"protection counts")
    print(f"registration_check = source_pins:766; protected_inputs:1443; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,inputs


def evaluate_new(model,prompts,data,x):
    require(not torch.is_grad_enabled() and not any(m.training for m in model.modules()) and not any(v.requires_grad for v in model.parameters()),"frozen evaluator")
    raw={}
    for k in LAYOUTS:
        raw[k]={}
        for s in SPLITS:
            raw[k][s]={}
            for profile in PROFILES:
                raw[k][s][profile]={}
                for view in VIEWS:
                    chunks=[]
                    for start in range(0,len(data[s]),96):
                        tokens=torch.stack([x.wide.prefix_tensor(item["views"][view]) for item in prompts[k][s][profile][start:start+96]])
                        z=model(tokens,torch.zeros(len(tokens),dtype=torch.int64)); x.c.p267.check_logits(z,len(tokens)); chunks.append(z.detach().clone())
                    raw[k][s][profile][view]=torch.cat(chunks)
    return raw


def validate_new(raw,data,x):
    require(set(raw)==set(LAYOUTS),"new layouts")
    for k,s in itertools.product(LAYOUTS,SPLITS):
        require(set(raw[k])==set(SPLITS) and set(raw[k][s])==set(PROFILES),"new splits/profiles")
        for profile in PROFILES:
            require(set(raw[k][s][profile])==set(VIEWS),"new views")
            for z in raw[k][s][profile].values(): x.c.p267.check_logits(z,len(data[s])); require(not z.requires_grad,"detached logits")


def infer_one(model,state,anchor,data,old,new,p,x):
    require(anchor["readout_policy"]==anchor["arm"] and anchor["arm"] in ARMS,"trained-policy identity")
    model.load_state_dict(state,strict=True); model.eval(); model.requires_grad_(False)
    fp=x.c.base.fingerprint(model); hooks=p.hook_snapshot(model); require(fp==anchor["final_sha256"],"strict checkpoint")
    raw={}; receipts={}
    for mode in ("before","unequal","after"):
        print(f"[C320] seed={anchor['seed']} arm={anchor['arm']} mode={mode}",flush=True)
        with torch.no_grad(),x.c.p267.counted(model,x.c.core) as (calls,cores),p.trained_readout(model,x.wide,anchor["arm"]) as stats:
            raw[mode]=evaluate_new(model,new,data,x) if mode=="unequal" else x.parent.evaluate(model,old,data,x.wide,x.c)
        expected=(54,5184,216) if mode=="unequal" else (144,13824,576)
        require((*calls,cores[0])==expected and stats==dict(calls=expected[0],query_calls=2*expected[0],rows=expected[1],grad_calls=0),"phase work/policy")
        require(fp==x.c.base.fingerprint(model) and hooks==p.hook_snapshot(model),"weight/hook preservation"); receipts[mode]=dict(stats)
    errors=[x.parent.replay_error(raw[m],anchor["raw"],data,x.c) for m in ("before","after")]
    return dict(seed=anchor["seed"],arm=anchor["arm"],readout_policy=anchor["arm"],final_sha256=fp,
        raw=raw,receipts=receipts,replay_errors=errors,weights_preserved=True,hooks_restored=True)


def analyze(records,anchors,data,x):
    require([(r["seed"],r["arm"]) for r in records]==identities() and [(r["seed"],r["arm"]) for r in anchors]==identities(),"complete cohort")
    results=[]; parts=[]; metrics=[]; controls=[]
    for r,a,flag in zip(records,anchors,expected_parent_results(),strict=True):
        require(r["readout_policy"]==a["readout_policy"]==r["arm"] and r["final_sha256"]==a["final_sha256"]
                and r["weights_preserved"] is True and r["hooks_restored"] is True and set(r["raw"])=={"before","unequal","after"},"record provenance")
        require(r["receipts"]=={m:dict(calls=c,query_calls=2*c,rows=96*c,grad_calls=0) for m,c in (("before",144),("unequal",54),("after",144))},"policy receipts")
        errors=[x.parent.replay_error(r["raw"][m],a["raw"],data,x.c) for m in ("before","after")]
        require(errors==r["replay_errors"] and all(type(e) in (int,float) and 0<=e<=1e-9 for e in errors),"reproduction")
        for m in ("before","after"):
            require({str(n):x.wide.score_length(data,r["raw"][m][str(n)],x.c)["passed"] for n in range(2,7)}==flag["length_pass"],"old gates")
        validate_new(r["raw"]["unequal"],data,x); key=dict(seed=r["seed"],arm=r["arm"]); flags={}
        for layout,z in r["raw"]["unequal"].items():
            score=x.wide.score_length(data,z,x.c); require(type(score["passed"]) is bool,"gate type"); flags[layout]=score["passed"]
            local=x.diag.normalize_task(score,"triple",r["seed"],r["arm"])
            for s in SPLITS: parts.append(dict(**key,layout=layout,name_lengths=list(LAYOUTS[layout]),split=s,**x.diag.partition([v for v in local if v["split"]==s])))
            metrics.append(dict(**key,layout=layout,score=score))
        results.append(dict(**key,layout_pass=flags,all_layouts_pass=all(flags.values())))
        controls.append(dict(**key,replay_errors=errors,matched=True))
    counts={k:{a:sum(r["layout_pass"][k] for r in results if r["arm"]==a) for a in ARMS} for k in LAYOUTS}
    all_counts={a:sum(r["all_layouts_pass"] for r in results if r["arm"]==a) for a in ARMS}
    return metrics,dict(seed_results=results,final_partitions=parts,reproductions=controls,layout_pass_counts=counts,
        all_layouts_counts=all_counts,primary_arm=PRIMARY_ARM,primary_gate=all_counts[PRIMARY_ARM]==5,all_replays=True,**WORK)


def runtime_preflight(paths,root):
    torch.set_num_threads(2); precheck(paths,root); p,x=context(); _,data,old,anchors=load_parent(paths)
    new=new_prompts(data); states=p.load_bundle(Path(paths[0]).resolve().parent/"trained-models.pt"); models=p.make_models(SEEDS[0],x)
    ids=[next(i for i,r in enumerate(data["TRAIN"]) if r["language"]==lang) for lang in ("en","ja")]
    texts=[old["4"]["TRAIN"]["shared_suffix"][i]["views"]["normal"] for i in ids]
    texts += [new[k]["TRAIN"]["shared_suffix"][i]["views"]["normal"] for k in LAYOUTS for i in ids]
    tokens=torch.stack([x.wide.prefix_tensor(v) for v in texts]); tasks=torch.zeros(len(tokens),dtype=torch.int64)
    for j,arm in enumerate(ARMS):
        model=models[arm]; model.load_state_dict(states[j],strict=True); model.eval(); model.requires_grad_(False); fp=x.c.base.fingerprint(model)
        require(fp==anchors[j]["final_sha256"],"smoke checkpoint")
        with torch.no_grad(),p.trained_readout(model,x.wide,arm):
            a=model(tokens[:2],tasks[:2]); z=model(tokens[2:],tasks[2:]); again=model(tokens[:2],tasks[:2])
        x.c.p267.check_logits(z,4); require(torch.equal(a,again) and fp==x.c.base.fingerprint(model),"smoke restoration")
    print("real_unequal_layout_policy_probe = PASS; discarded probes only",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True
            and p["gate_f_candidate"] is False and p["production_adoption"] is False,"result scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(766,1443) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(WIDE_SOURCE)==WIDE_BLOB,"result protection")
    require(len(p["artifacts"])==5 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"]; rr=s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rr]==identities() and all(set(r["layout_pass"])==set(LAYOUTS)
            and all(type(v) is bool for v in r["layout_pass"].values()) and r["all_layouts_pass"] is all(r["layout_pass"].values()) for r in rr),"result cohort/flags")
    counts={k:{a:sum(r["layout_pass"][k] for r in rr if r["arm"]==a) for a in ARMS} for k in LAYOUTS}
    combined={a:sum(r["all_layouts_pass"] for r in rr if r["arm"]==a) for a in ARMS}; gate=combined[PRIMARY_ARM]==5
    require(s["layout_pass_counts"]==counts and s["all_layouts_counts"]==combined and s["primary_arm"]==PRIMARY_ARM
            and s["primary_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"prospective primary")
    require(len(s["final_partitions"])==40 and len(s["reproductions"])==10 and s["all_replays"] is True
            and all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"work/coverage")


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==204,"parent modules")
    return names+["tests_lm.test_v05_c320_unequal_name_lengths"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==5222 and ids.count(EXCLUDED)==1,"loaded suite")
    return unittest.TestSuite(t for t in tests if t.id()!=EXCLUDED)


def run(*,summaries,output_dir,expected_head):
    torch.set_num_threads(2); torch.use_deterministic_algorithms(True); p,x=context(); root=Path(__file__).resolve().parents[2]
    p.context()[1].guard(root,expected_head,x.c); pins,inputs=precheck(summaries,root); _,data,old,anchors=load_parent(summaries); new=new_prompts(data)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    states=p.load_bundle(Path(summaries[0]).resolve().parent/"trained-models.pt"); records=[]
    for i,seed in enumerate(SEEDS):
        models=p.make_models(seed,x)
        for j,arm in enumerate(ARMS): records.append(infer_one(models[arm],states[2*i+j],anchors[2*i+j],data,old,new,p,x))
    metrics,s=analyze(records,anchors,data,x); torch.save(dict(schema="fold-c320-unequal-eval-v1",records=records),out/"evaluations.pt")
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],new),(OUTPUTS[3],metrics),(OUTPUTS[4],s)): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=x.c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    p.context()[1].guard(root,expected_head,x.c); precheck(summaries,root)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if s["primary_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=inputs,artifacts=artifacts,validation_summary=s,gate_f_candidate=False,production_adoption=False)
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C320 COMPACT EXPERIMENT RECEIPT ===",flush=True)
    print(json.dumps(dict(experiment_id=EXPERIMENT_ID,commit_sha=expected_head,status=result["status"],summary_sha256=x.c.audit.sha(out/"summary.json"),artifacts=artifacts),indent=2),flush=True)
    return result


def verify_artifacts(outdir,summaries,expected_head):
    _,x=context(); out=Path(outdir); result=x.c.audit.read_json(out/"summary.json"); validate_result(result)
    require(result["commit_sha"]==expected_head,"execution HEAD")
    for n,h in result["input_sha256"].items(): require(x.c.audit.sha(n)==h,"protected input")
    for a in result["artifacts"]:
        path=x.c.audit.safe_child(out,a["file"]); require(x.c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with x.guarded.no_neural():
        _,data,_,anchors=load_parent(summaries); archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c320-unequal-eval-v1","evaluation schema")
        metrics,s=analyze(archive["records"],anchors,data,x)
        for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],new_prompts(data)),(OUTPUTS[3],metrics),(OUTPUTS[4],s)):
            require(x.c.audit.read_json(out/n)==v,"persisted:"+n)
    require(result["validation_summary"]==s,"summary reconstruction"); return result,metrics


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--summaries",nargs=46,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True); parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
