"""C270: frozen transfer from trained two-character names to unseen three-character familiar-byte names."""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import torch
from torch.nn import functional as F

EXPERIMENT_ID="C270-v5b-frozen-triple-identifiers"
STAGE="V5-B-FROZEN-TRIPLE-IDENTIFIERS"
BASE="f0f10ee158a0f4740fea390f4d96d93ed0e1851b"
PARENT_EXECUTION="7c44987b4a70f6ed821657f518b81f78bf0a376d"
PARENT_SHA="a97663b83c536d2ce8df4fb41d42493cbbfc35fe757b9b72fca1b63382f255b8"
PARENT_ARTIFACTS={
    "query-plan.json":"cec2e2bfe254605c5c4a68c3f71bbaf7135de10a4a39af37a9d4b4aef469e2aa",
    "dataset.json":"1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
    "trained-models.pt":"65f3b34e163b7753ecfda2eadedeb7cd8f282a0437b6b94ec2034d2efeadea9c",
    "evaluations.pt":"a9212d3da65849ebc08f4f7ed1e669f73b34f897d1f4ab05b077582c1d220c29",
    "measurements.json":"3d64033da08d8a83b8bebe53e6acd4b85340acffb9d849ebcb7b921f480a7811",
    "validation-summary.json":"44de8eb095ceca1f3827ec4e2ba521a750fd80e49b38235db027754dbb540e6a",
}
SEEDS=tuple(range(269001,269006))
ARMS=("eos_query","span_query")
SPLITS=("TRAIN","HOLDOUT")
PROFILES=("tripled","shared_prefix2","shared_suffix2")
VIEWS=("normal","evidence_blind","query_blind")
TOL=1e-9
OWN=("fold_lm/v05_benchmarks/model_c270_frozen_triple_identifiers.py",
     "tests_lm/test_v05_c270_frozen_triple_identifiers.py","tools/run_c270.ps1","tools/invoke_c270.ps1",
     "docs/experiment-ledger-addendum-c270-preregistration.md","docs/v5b-frozen-triple-identifiers-v0.1.md")
OUTPUTS=("transfer-plan.json","triple-dataset.json","eval-outputs.pt","measurements.json","validation-summary.json")
EXCLUDED="tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
DATA_SHA="432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73"
MANIFEST_SHA="3fa2e3267b08c6ea528bfdb52bc7ad0e932e3215945e5231bdf38a48e453f016"

def require(ok,message):
    if not ok: raise ValueError(message)
def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))
def context():
    from fold_lm.v05_benchmarks import model_c269_query_span_pooling as parent
    p268,p267,core,base,aligned,reader,factory,audit=parent.context()
    return parent,p267,core,base,aligned,reader,factory,audit
def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        seeds=list(SEEDS),arms=list(ARMS),profiles=list(PROFILES),dataset_sha256=DATA_SHA,
        changed="frozen transfer from trained two-character identifiers to unseen three-character familiar-byte identifiers",
        primary="all five frozen span_query states pass unchanged C267 thresholds on both value splits/all three new profiles; control separate",
        gate=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        rows_per_profile={"TRAIN":192,"HOLDOUT":96},new_normal_rows_per_model=864,
        model_forward_calls=810,row_presentations=77760,core_forward_calls=3240,
        forwards_per_model=81,rows_per_model=7776,checkpoint_bundle_loads=1,model_state_loads=10,
        new_training_steps=0,new_checkpoint_writes=0,raw_logit_payload_bytes=159252480,
        source_pins=466,protected_inputs=800,direct_dependencies=46,own_tests=24,
        modules=155,loaded_tests=3646,focused_tests=3645,excluded_test=EXCLUDED,
        dtype="CPU float64",threads=2,deterministic=True,replay_tolerance=TOL,network_calls=0,
        gate_f_candidate=False,production_adoption=False,arbitrary_name_claim=False,
        causal_parser_claim=False,general_language_claim=False)

def name_map(row,profile):
    require(profile in PROFILES and row["language"] in ("en","ja"),"profile/language")
    chars=("a","b","c") if row["language"]=="en" else ("甲","乙","丙")
    i,j=row["entities"];u,v=chars[i],chars[j]
    second=v*3 if profile=="tripled" else u+u+v if profile=="shared_prefix2" else v+u+u
    return {i:u*3,j:second}

def render(row,profile,view="normal"):
    require(view in VIEWS,"view")
    names=name_map(row,profile);values=dict(zip(row["entities"],row["values"],strict=True))
    return ";".join(names[k]+"="+("?" if view=="evidence_blind" else str(values[k])) for k in row["permutation"])+        ";"+("?" if view=="query_blind" else names[row["query"]])+"="

def prompt_dataset(data,p267):
    p267.validate_data(data)
    result={split:{} for split in SPLITS}
    for split in SPLITS:
        rows=data[split]
        for profile in PROFILES:
            result[split][profile]=[dict(source_id=r["id"],target=r["target"],
                views={view:render(r,profile,view) for view in VIEWS}) for r in rows]
    return result

def validate_dataset(prompts,data,p267):
    require(prompts==prompt_dataset(data,p267) and digest(prompts)==DATA_SHA,"triple dataset identity")
    old_bytes=set().union(*(set(p267.render(r,p,v).encode()) for split in SPLITS for r in data[split] for p in p267.PROFILES for v in VIEWS))
    normal_prompts=[]
    for split in SPLITS:
        require(set(prompts[split])==set(PROFILES),"profile coverage")
        for profile in PROFILES:
            rows=prompts[split][profile]
            require(len(rows)==len(data[split]) and len({r["views"]["normal"] for r in rows})==len(rows),"unique prompt rows")
            for base,item in zip(data[split],rows,strict=True):
                require(item["source_id"]==base["id"] and item["target"]==base["target"],"prompt metadata")
                normal_prompts.append(item["views"]["normal"])
                for text in item["views"].values():
                    require(len(text.encode())<=46 and set(text.encode())<=old_bytes,"prompt length/new byte")
                names=name_map(base,profile)
                require(all(len(x)==3 for x in names.values()),"three-character identifiers")
    require(len(normal_prompts)==len(set(normal_prompts))==864,"global unique normal prompts")

def replay_old(left,right,data,p267):
    require(set(left)==set(right)==set(SPLITS),"replay splits");error=0.
    for split in SPLITS:
        require(set(left[split])==set(right[split])==set(p267.PROFILES),"replay profiles")
        for profile in p267.PROFILES:
            require(set(left[split][profile])==set(right[split][profile])==set(VIEWS),"replay views")
            for view in VIEWS:
                a,b=left[split][profile][view],right[split][profile][view]
                p267.check_logits(a,len(data[split]));p267.check_logits(b,len(data[split]))
                error=max(error,float((a-b).abs().max()))
                require(error<=TOL and torch.equal(a.argmax(-1),b.argmax(-1)),"raw/argmax replay")
    return error

def evaluate_new(model,prompts,data,factory,p267):
    raw={}
    model.eval()
    with torch.no_grad():
        for split in SPLITS:
            raw[split]={}
            for profile in PROFILES:
                raw[split][profile]={}
                for view in VIEWS:
                    chunks=[]
                    items=prompts[split][profile]
                    for start in range(0,len(items),96):
                        x=torch.stack([factory.prefix_tensor(item["views"][view].encode()) for item in items[start:start+96]])
                        value=model(x,torch.zeros(len(x),dtype=torch.int64));p267.check_logits(value,len(x));chunks.append(value.detach().clone())
                    raw[split][profile][view]=torch.cat(chunks)
    return raw

def score(data,raw,p267):
    p267.validate_data(data);require(set(raw)==set(SPLITS),"evaluation splits")
    cells=[];order_cells=[];totals=[]
    for split in SPLITS:
        rows=data[split];n=16 if split=="TRAIN" else 8
        require(set(raw[split])==set(PROFILES),"evaluation profiles")
        for profile in PROFILES:
            outputs=raw[split][profile];require(set(outputs)==set(VIEWS),"views")
            for x in outputs.values():p267.check_logits(x,len(rows))
            pred={v:x.argmax(-1).tolist() for v,x in outputs.items()}
            loss=F.cross_entropy(outputs["normal"],torch.tensor([r["target"] for r in rows]),reduction="none")
            for lang,entities in itertools.product(("en","ja"),p267.SUBSETS):
                for perm in (entities,entities[::-1]):
                    ids=[i for i,r in enumerate(rows) if (r["language"],tuple(r["entities"]),tuple(r["permutation"]))==(lang,entities,perm)]
                    groups=defaultdict(list)
                    for i in ids:groups[tuple(rows[i]["values"])].append(i)
                    require(len(ids)==n and len(groups)==n//2 and all(len(g)==2 for g in groups.values()),"cell groups")
                    acc={v:sum(pred[v][i]==rows[i]["target"] for i in ids)/n for v in VIEWS}
                    qp=sum(all(pred["normal"][i]==rows[i]["target"] for i in g) for g in groups.values())/(n//2)
                    collapse=sum(pred["normal"][g[0]]==pred["normal"][g[1]] for g in groups.values())
                    ed,qd=acc["normal"]-acc["evidence_blind"],acc["normal"]-acc["query_blind"]
                    cells.append(dict(split=split,profile=profile,language=lang,entities=list(entities),permutation=list(perm),
                        rows=n,correct=round(acc["normal"]*n),accuracy=acc["normal"],query_pair_accuracy=qp,
                        collapsed_pairs=collapse,pairs=n//2,evidence_drop=ed,query_drop=qd,answer_nll=float(loss[ids].mean()),
                        passed=acc["normal"]>=.90 and qp>=.80 and ed>=.35 and qd>=.35))
                groups=defaultdict(list)
                for i,r in enumerate(rows):
                    if (r["language"],tuple(r["entities"]))==(lang,entities):
                        groups[tuple(r["values"]),r["query"]].append(i)
                require(len(groups)==n and all(len(g)==2 for g in groups.values()),"two-order groups")
                correct=sum(all(pred["normal"][i]==rows[i]["target"] for i in g) for g in groups.values())
                order_cells.append(dict(split=split,profile=profile,language=lang,entities=list(entities),groups=n,
                    both_correct=correct,accuracy=correct/n,passed=correct/n>=.80))
            for lang in ("en","ja"):
                cc=[c for c in cells if (c["split"],c["profile"],c["language"])==(split,profile,lang)]
                totals.append(dict(split=split,profile=profile,language=lang,rows=sum(c["rows"] for c in cc),
                    correct=sum(c["correct"] for c in cc),pairs=sum(c["pairs"] for c in cc),
                    collapsed_pairs=sum(c["collapsed_pairs"] for c in cc)))
    return dict(cells=cells,two_order=order_cells,totals=totals,passed=all(c["passed"] for c in cells+order_cells))

def probe(model,ref,data,prompts,p267,core,base,factory):
    require(not any(m.training for m in model.modules()) and not any(p.requires_grad for p in model.parameters()),"frozen model")
    before=base.fingerprint(model);require(before==ref["final_sha256"] and sum(p.numel() for p in model.parameters())==14256,"final identity/capacity")
    with p267.counted(model,core) as (counts,cores):
        anchor=p267.evaluate(model,data,factory);ae=replay_old(anchor,ref["raw"],data,p267)
        require(base.fingerprint(model)==before,"anchor mutation")
        novel=evaluate_new(model,prompts,data,factory,p267)
        restored=p267.evaluate(model,data,factory);recheck=max(replay_old(restored,anchor,data,p267),replay_old(restored,ref["raw"],data,p267))
    require(counts==[81,7776] and cores[0]==324,"probe workload")
    require(base.fingerprint(model)==before,"weight mutation")
    return dict(seed=ref["seed"],arm=ref["arm"],final_sha256=before,weights_preserved=True,
        model_forward_calls=81,row_presentations=7776,core_forward_calls=324,anchor_error=ae,restore_error=recheck,
        anchor=anchor,novel=novel,restored=restored)

def analyze(records,refs,data,p267):
    require([(r["seed"],r["arm"]) for r in records]==[(r["seed"],r["arm"]) for r in refs]==identities(),"record identities")
    metrics=[];results=[];contrasts=[]
    for r,ref in zip(records,refs,strict=True):
        require(r["weights_preserved"] is True and r["final_sha256"]==ref["final_sha256"],"saved state")
        require((r["model_forward_calls"],r["row_presentations"],r["core_forward_calls"])==(81,7776,324),"saved workload")
        for k in ("anchor_error","restore_error"):
            require(type(r[k]) in (int,float) and math.isfinite(r[k]) and 0<=r[k]<=TOL,"saved replay error")
        replay_old(r["anchor"],ref["raw"],data,p267);replay_old(r["restored"],r["anchor"],data,p267);replay_old(r["restored"],ref["raw"],data,p267)
        m=score(data,r["novel"],p267);metrics.append(dict(seed=r["seed"],arm=r["arm"],**m));results.append(dict(seed=r["seed"],arm=r["arm"],passed=m["passed"]))
    for i in range(0,10,2):
        a,b=metrics[i:i+2]
        require((a["seed"],a["arm"],b["seed"],b["arm"])==(b["seed"],"eos_query",b["seed"],"span_query"),"paired identities")
        for x,y in zip(a["totals"],b["totals"],strict=True):
            require(tuple(x[k] for k in ("split","profile","language","rows","pairs"))==tuple(y[k] for k in ("split","profile","language","rows","pairs")),"contrast identities")
            contrasts.append(dict(seed=a["seed"],split=x["split"],profile=x["profile"],language=x["language"],rows=x["rows"],pairs=x["pairs"],
                control_correct=x["correct"],candidate_correct=y["correct"],correct_delta=y["correct"]-x["correct"],
                control_collapsed=x["collapsed_pairs"],candidate_collapsed=y["collapsed_pairs"],collapse_delta=y["collapsed_pairs"]-x["collapsed_pairs"]))
    summary=dict(models=10,seed_results=results,seed_pass_counts={a:sum(r["passed"] for r in results if r["arm"]==a) for a in ARMS},
        candidate_gate=all(r["passed"] for r in results if r["arm"]=="span_query"),contrasts=contrasts,
        model_forward_calls=810,row_presentations=77760,core_forward_calls=3240,checkpoint_bundle_loads=1,
        model_state_loads=10,new_training_steps=0,new_checkpoint_writes=0,all_replays=True,all_weights_preserved=True)
    return metrics,summary

def check_parent(payload,parent):
    parent.validate_result(payload)
    require(payload["commit_sha"]==PARENT_EXECUTION and payload["status"]=="PASS","accepted C269 identity")
    require(payload["validation_summary"]["seed_pass_counts"]=={"eos_query":4,"span_query":5}
        and payload["validation_summary"]["candidate_gate"] is True,"accepted C269 gate")
    require({x["file"]:x["sha256"] for x in payload["artifacts"]}==PARENT_ARTIFACTS,"parent artifacts")

def load_reference(path):
    parent,p267,*_,audit=context();path=Path(path).resolve();require(audit.sha(path)==PARENT_SHA,"parent summary hash")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("parent verification forbids model calls")):
        payload,parent_metrics=parent.verify_artifacts(path.parent,PARENT_EXECUTION)
        check_parent(payload,parent)
        data=audit.read_json(path.parent/"dataset.json");p267.validate_data(data)
        archive=torch.load(path.parent/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c269-query-span-eval-v1","parent eval schema")
        got,summary=parent.analyze(archive["records"],data,p267)
        require(got==parent_metrics and summary==payload["validation_summary"],"parent saved semantics")
        refs=[{k:r[k] for k in ("seed","arm","final_sha256","raw")} for r in archive["records"]]
    require([(r["seed"],r["arm"]) for r in refs]==identities(),"parent identities")
    return data,refs

def validate_registration(source_count,input_count):
    actual=digest(manifest())
    print(f"registration_check = source_pins:{source_count}; protected_inputs:{input_count}; manifest_sha256:{actual}",flush=True)
    require((source_count,input_count)==(466,800),"source/input counts")
    require(actual==MANIFEST_SHA,f"manifest expected={MANIFEST_SHA} actual={actual}")

def precheck(path,root):
    parent,_,_,_,_,_,factory,audit=context();path=Path(path).resolve();root=Path(root)
    require(audit.sha(path)==PARENT_SHA,"parent summary hash");payload=audit.read_json(path);check_parent(payload,parent)
    pins,protected=dict(payload["source_blobs"]),dict(payload["input_sha256"])
    for name,wanted in protected.items():require(Path(name).is_file() and audit.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items():require(audit.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    for child,wanted in [(path,PARENT_SHA)]+[(audit.safe_child(path.parent,x["file"]),x["sha256"]) for x in payload["artifacts"]]:
        key=str(child.resolve());require(key not in protected and audit.sha(child)==wanted,"parent input identity");protected[key]=wanted
    for x in payload["artifacts"]:require(audit.safe_child(path.parent,x["file"]).stat().st_size==x["serialized_bytes"],"parent artifact size")
    for name in OWN:
        require(name not in pins,"OWN collision");pins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9])_[^/]+)\.py"
    deps=set(factory.LM_SOURCES)|{n for n in payload["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps)==46 and deps<=set(pins),"direct dependencies")
    protected.update(audit.protect_tree_files(root,pins));validate_registration(len(pins),len(protected))
    return pins,protected

def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(466,800) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==set(OUTPUTS),"artifact coverage")
    s=p["validation_summary"];rr=s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rr]==identities() and all(type(r["passed"]) is bool for r in rr),"result identities")
    require(s["candidate_gate"] is all(r["passed"] for r in rr if r["arm"]=="span_query")
        and s["seed_pass_counts"]=={a:sum(r["passed"] for r in rr if r["arm"]==a) for a in ARMS},"gate accounting")
    for k,v in dict(models=10,model_forward_calls=810,row_presentations=77760,core_forward_calls=3240,
                    checkpoint_bundle_loads=1,model_state_loads=10,new_training_steps=0,new_checkpoint_writes=0).items():
        require(type(s[k]) is int and s[k]==v,"workload:"+k)
    require(len(s["contrasts"])==60 and s["all_replays"] is True and s["all_weights_preserved"] is True
        and p["status"]==("PASS" if s["candidate_gate"] else "FAIL"),"status/integrity")
    require(all(p[k] is False for k in ("gate_f_candidate","production_adoption","arbitrary_name_claim","causal_parser_claim","general_language_claim"))
        and p["network_calls"]==0,"scope")

def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item
def regression_modules(root):
    names=context()[0].regression_modules(root);require(len(names)==len(set(names))==154,"parent modules")
    return names+["tests_lm.test_v05_c270_frozen_triple_identifiers"]
def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"suite IDs");kept=[t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(3646,3645),"suite counts");return unittest.TestSuite(kept)

def run(*,c269_summary,output_dir,expected_head):
    parent,p267,core,base,aligned,reader,factory,audit=context();root=Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c269_summary,root);data,refs=load_reference(c269_summary)
    prompts=prompt_dataset(data,p267);validate_dataset(prompts,data,p267)
    states=parent.load_bundle(Path(c269_summary).resolve().parent/"trained-models.pt");require(len(states)==10,"state count")
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);records=[]
    for ref,state in zip(refs,states,strict=True):
        model=parent.make_arm_model(ref["seed"],ref["arm"],base,aligned,reader,factory)
        model.load_state_dict(state,strict=True);model.eval().requires_grad_(False)
        print(f'[C270] model={len(records)+1}/10 seed={ref["seed"]} arm={ref["arm"]}; frozen triple-identifier transfer',flush=True)
        records.append(probe(model,ref,data,prompts,p267,core,base,factory))
    metrics,summary=analyze(records,refs,data,p267)
    torch.save(dict(schema="fold-c270-triple-eval-v1",records=records),out/"eval-outputs.pt")
    for name,value in (("transfer-plan.json",manifest()),("triple-dataset.json",prompts),("measurements.json",metrics),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard();precheck(c269_summary,root)
    for name,wanted in protected.items():require(audit.sha(name)==wanted,"modified input")
    payload=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,production_adoption=False,arbitrary_name_claim=False,causal_parser_claim=False,general_language_claim=False,network_calls=0)
    validate_result(payload);(out/"summary.json").write_bytes(blob(payload));print("=== C270 RESULT ===",flush=True);print(blob(payload).decode(),flush=True);return payload

def verify_artifacts(output_dir,c269_summary,expected_head):
    _,p267,*rest=context();audit=rest[-1];out=Path(output_dir);p=audit.read_json(out/"summary.json")
    validate_result(p);require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():require(audit.sha(name)==wanted,"postcheck input")
    for x in p["artifacts"]:
        child=audit.safe_child(out,x["file"]);require(audit.sha(child)==x["sha256"] and child.stat().st_size==x["serialized_bytes"],"output bytes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("saved postcheck forbids model calls")):
        data,refs=load_reference(c269_summary);prompts=audit.read_json(out/"triple-dataset.json");validate_dataset(prompts,data,p267)
        archive=torch.load(out/"eval-outputs.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c270-triple-eval-v1","eval schema")
        metrics,summary=analyze(archive["records"],refs,data,p267)
        for name,value in (("transfer-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):
            require(audit.read_json(out/name)==value,"persisted reconstruction:"+name)
    require(p["validation_summary"]==summary,"saved summary");return p,metrics

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("c269-summary","output-dir"):p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))
if __name__=="__main__":main()
