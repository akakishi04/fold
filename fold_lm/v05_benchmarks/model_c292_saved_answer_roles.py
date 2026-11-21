"""C292: observable answer roles in sealed C291 logits; no new neural execution."""
from __future__ import annotations
import argparse
from collections import Counter
from contextlib import contextmanager
import hashlib
import itertools
import json
from pathlib import Path
import re
from types import ModuleType
import unittest
from unittest.mock import patch
import torch

EXPERIMENT_ID = "C292-v5b-saved-answer-role-audit"
STAGE = "V5-B-SAVED-ANSWER-ROLE-AUDIT"
BASE = "842e32a59bb5e3ef3f475554fb238c693139377e"
PARENT_EXECUTION = "8d33edabbc7a91654a3da6056091cec2d84d9a24"
PARENT_SHA = "271cc816f49fd7d53714508fee284bbf9f93783b3e74ac2728fc2a5286d740fa"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c291_answer_margin.py"
PARENT_BLOB = "4257586769ffd9e810fd41d5bc0debea86dd087f"
SEEDS = tuple(range(291001,291006))
ARMS = ("ce_only","pair_sum","answer_margin")
PROFILES = {"two_char":("doubled","shared_prefix","shared_suffix"),
            "triple":("tripled","shared_prefix2","shared_suffix2"),
            "quad":("quadrupled","shared_prefix3","shared_suffix3")}
ROLES = ("target","other_fact","absent_known_value","non_value_byte")
OWN = ("fold_lm/v05_benchmarks/model_c292_saved_answer_roles.py",
       "tests_lm/test_v05_c292_saved_answer_roles.py","tools/run_c292.ps1","tools/invoke_c292.ps1",
       "docs/experiment-ledger-addendum-c292-preregistration.md","docs/v5b-saved-answer-roles-v0.1.md")
OUTPUTS = ("audit-plan.json","answer-role-report.json","validation-summary.json")
PARENT_OUTPUTS = ("architecture-plan.json","dataset.json","triple-dataset.json","quad-dataset.json",
                  "trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
ZERO_KEYS = ("model_forward_calls","train_steps","model_state_loads","new_checkpoint_writes",
             "row_presentations","core_forward_calls","network_calls")
MANIFEST_SHA = "f45b635e637d043d7b5dfeb2c65abed847a0b7d47ae3dd0cb4f0ce6c7f4f2869"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c291_answer_margin as parent
    return parent,parent.context()[-1]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION,parent_summary_sha256=PARENT_SHA,
                parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,parent_outputs=list(PARENT_OUTPUTS),
                parents="18 ordered summaries:C291,C290,C289,C288..C274;all hashes before dispatch",
                question="which residual errors select the other fact,an absent known value,or a non-value byte",
                seeds=list(SEEDS),arms=list(ARMS),roles=list(ROLES),value_bytes=[48,49,50,51],
                observations=38880,partitions=90,profile_language_groups=540,value_pair_groups=540,
                comparisons=60,comparison_rows=25920,
                coverage="all normal final logits;parent reconstructs every original masked/full gate",
                protection="entire592 inherited sources plus6 OWN;explicit parent-context module coverage",
                source_pins=598,protected_inputs=1081,own_tests=32,modules=177,loaded_tests=4318,focused_tests=4317,
                excluded_test=EXCLUDED,capability_gate_applicable=False,gate_f_candidate=False,
                interpretation="observable output categories only;no causal attribution or prediction filtering",
                **dict.fromkeys(ZERO_KEYS,0))


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def expected_results():
    out=[]
    for seed,arm in identities():
        seen=arm=="pair_sum" or seed!=291003
        quad=seed in (291002,291005) if arm=="pair_sum" else seed!=291003
        out.append(dict(seed=seed,arm=arm,passed=quad,quad_pass=quad,two_char_pass=seen,triple_pass=seen,
                        all_tasks_pass=quad,fitted_train_direct_pass=True,seen_holdout_direct_pass=seen))
    return out


def answer_role(row,prediction):
    e,v,perm,q=row["entities"],row["values"],row["permutation"],row["query"]
    require(len(e)==len(v)==len(perm)==2 and len(set(e))==len(set(v))==2,"two distinct facts")
    require(all(type(x) is int and 0<=x<3 for x in e) and all(type(x) is int and 0<=x<4 for x in v),"entity/value domain")
    require(sorted(perm)==sorted(e) and q in e and type(q) is int,"fact permutation/query")
    target=48+v[e.index(q)];other=48+v[1-e.index(q)]
    require(type(row["target"]) is int and row["target"]==target,"target/value binding")
    require(type(prediction) is int and 0<=prediction<256,"prediction byte")
    role="target" if prediction==target else "other_fact" if prediction==other else "absent_known_value" if 48<=prediction<=51 else "non_value_byte"
    return dict(target=target,other_value=other,prediction=prediction,role=role)


def tally(rows):
    require(bool(rows),"empty group")
    counts=Counter(r["role"] for r in rows);require(set(counts)<=set(ROLES),"unknown role")
    confusion=Counter((r["target"],r["prediction"]) for r in rows)
    return dict(rows=len(rows),correct=counts["target"],errors=len(rows)-counts["target"],
                role_counts={r:counts[r] for r in ROLES},
                confusion=[[y,p,n] for (y,p),n in sorted(confusion.items())])


def collapse(rows):
    groups={}
    for r in rows:
        key=(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups.setdefault(key,[]).append(r)
    require(all(len(rs)==2 and {r["query"] for r in rs}==set(k[1]) for k,rs in groups.items()),"query pair coverage")
    return sum(rs[0]["prediction"]==rs[1]["prediction"] for rs in groups.values())


def compare(control,candidate):
    require(len(control)==len(candidate)>0,"comparison size")
    transitions=Counter();flips=rescued=regressed=0
    for a,b in zip(control,candidate,strict=True):
        require(all(a[k]==b[k] for k in ("task","split","profile","source_id","target","other_value")),"aligned row identity")
        transitions[(a["role"],b["role"])]+=1;flips+=a["prediction"]!=b["prediction"]
        rescued+=a["role"]!="target" and b["role"]=="target"
        regressed+=a["role"]=="target" and b["role"]!="target"
    return dict(rows=len(control),argmax_flips=flips,rescued=rescued,regressed=regressed,
                transitions={a+"->"+b:transitions[(a,b)] for a,b in itertools.product(ROLES,repeat=2)})


def analyze(records,data,metrics):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"record identities")
    require([(m["seed"],m["arm"]) for m in metrics]==identities(),"metric identities")
    require(set(data)=={"TRAIN","HOLDOUT"},"data splits")
    for split,n in (("TRAIN",192),("HOLDOUT",96)):
        require(len(data[split])==n and len({r["id"] for r in data[split]})==n,"unique source rows")
        require(len({tuple(r["values"]) for r in data[split]})==(8 if split=="TRAIN" else 4),"value split inventory")
    observations=[];partitions=[];details=[];value_pairs=[];lookup={}
    for raw,metric in zip(records,metrics,strict=True):
        require(set(raw["raw"])==set(PROFILES),"raw tasks")
        for task,profiles in PROFILES.items():
            require(set(raw["raw"][task])=={"TRAIN","HOLDOUT"},"raw splits")
            for split in ("TRAIN","HOLDOUT"):
                rows=data[split];part=[]
                require(set(raw["raw"][task][split])==set(profiles),"profiles")
                for profile in profiles:
                    views=raw["raw"][task][split][profile]
                    require(set(views)=={"normal","evidence_blind","query_blind"},"view schema")
                    z=views["normal"]
                    require(isinstance(z,torch.Tensor) and z.shape==(len(rows),256) and z.dtype==torch.float64
                            and z.device.type=="cpu" and not z.requires_grad and bool(torch.isfinite(z).all()),"saved logits")
                    predictions=z.argmax(1).tolist();selected=[]
                    for row,prediction in zip(rows,predictions,strict=True):
                        selected.append(dict(seed=raw["seed"],arm=raw["arm"],task=task,split=split,profile=profile,
                                             source_id=row["id"],**{k:row[k] for k in ("language","entities","values","permutation","query")},
                                             **answer_role(row,prediction)))
                    for language in ("en","ja"):
                        language_rows=[r for r in selected if r["language"]==language];counts=tally(language_rows)
                        old=[r for r in metric[task]["totals"] if (r["split"],r["profile"],r["language"])==(split,profile,language)]
                        require(len(old)==1 and all(counts[k]==old[0][k] for k in ("rows","correct"))
                                and old[0]["pairs"]==len(language_rows)//2
                                and old[0]["collapsed_pairs"]==collapse(language_rows),"parent normal totals")
                        details.append(dict(seed=raw["seed"],arm=raw["arm"],task=task,split=split,profile=profile,language=language,**counts))
                    part.extend(selected)
                key=dict(seed=raw["seed"],arm=raw["arm"],task=task,split=split)
                partitions.append(dict(**key,**tally(part)))
                for values in sorted({tuple(r["values"]) for r in part}):
                    value_pairs.append(dict(**key,values=list(values),**tally([r for r in part if tuple(r["values"])==values])))
                lookup[(raw["seed"],raw["arm"],task,split)]=part;observations.extend(part)
    comparisons=[]
    for seed,task,split,arm in itertools.product(SEEDS,PROFILES,("TRAIN","HOLDOUT"),ARMS[:2]):
        comparisons.append(dict(seed=seed,task=task,split=split,comparator=arm,candidate=ARMS[2],
                                 **compare(lookup[(seed,arm,task,split)],lookup[(seed,ARMS[2],task,split)])))
    require((len(observations),len(partitions),len(details),len(value_pairs),len(comparisons))==(38880,90,540,540,60),"audit inventory")
    require(sum(x["rows"] for x in comparisons)==25920,"comparison rows")
    summary=dict(parent_results=expected_results(),observations=len(observations),partitions=partitions,
                 value_pairs=value_pairs,comparisons=comparisons,diagnostic_complete=True,
                 capability_gate_applicable=False,**dict.fromkeys(ZERO_KEYS,0))
    return dict(observations=observations,profile_language=details,summary=summary),summary


@contextmanager
def no_neural():
    with torch.no_grad(),patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C292 forbids neural calls")), \
         patch.object(torch.nn.Module,"load_state_dict",side_effect=RuntimeError("C292 forbids model-state loads")), \
         patch.object(torch,"save",side_effect=RuntimeError("C292 forbids checkpoint writes")):
        yield


def load_parent(paths):
    parent,c=context();paths=[Path(p).resolve() for p in paths];old=parent.context()
    wanted=(PARENT_SHA,parent.PARENT_SHA,old[0].PARENT_SHA,*old[1].SUMMARY_SHAS)
    require(len(paths)==len(wanted)==18 and all(c.audit.sha(p)==w for p,w in zip(paths,wanted,strict=True)),"parent hashes")
    with no_neural():
        payload,metrics=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION);parent.validate_result(payload)
        require(payload["experiment_id"]=="C291-v5b-answer-wise-hardest-rival-margin" and payload["commit_sha"]==PARENT_EXECUTION
                and payload["status"]=="FAIL" and payload["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity")
        require(len(payload["artifacts"])==8 and {a["file"] for a in payload["artifacts"]}==set(PARENT_OUTPUTS),"parent artifacts")
        s=payload["validation_summary"]
        require(s["seed_results"]==expected_results() and s["candidate_gate"] is False
                and s["all_groups_matched"] is True and s["all_replays"] is True,"parent result")
        data=c.audit.read_json(paths[0].parent/"dataset.json");c.p267.validate_data(data)
        archive=torch.load(paths[0].parent/"evaluations.pt",map_location="cpu",weights_only=True)
    require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c291-answer-margin-eval-v1","archive schema")
    return payload,archive["records"],data,metrics


def precheck(paths,root):
    validate_seal();payload,_,_,_=load_parent(paths);parent,c=context();root=Path(root).resolve()
    pins,protected=dict(payload["source_blobs"]),dict(payload["input_sha256"])
    require((len(pins),len(protected))==(592,1066),"inherited protection count")
    for n,w in pins.items():require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==w,"changed source:"+n)
    for n,w in protected.items():require(Path(n).is_file() and c.audit.sha(n)==w,"changed input:"+n)
    modules=[parent]+[m for m in parent.context() if isinstance(m,ModuleType)]+[m for m in vars(c).values() if isinstance(m,ModuleType)]
    covered=set()
    for m in modules:
        path=getattr(m,"__file__",None)
        if path and Path(path).resolve().is_relative_to(root):
            name=Path(path).resolve().relative_to(root).as_posix();require(name in pins,"unprotected helper:"+name);covered.add(name)
    require(PARENT_SOURCE in covered and pins[PARENT_SOURCE]==PARENT_BLOB,"direct parent coverage")
    directory=Path(paths[0]).resolve().parent
    for child,w in [(Path(paths[0]).resolve(),PARENT_SHA)]+[(c.audit.safe_child(directory,a["file"]),a["sha256"]) for a in payload["artifacts"]]:
        require(str(child.resolve()) not in protected and c.audit.sha(child)==w,"parent input")
        protected[str(child.resolve())]=w
    for n in OWN:
        require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(598,1081),"protection count")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS"
            and p["diagnostic_execution_valid"] is True,"result identity")
    require(all(p[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")),"result scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(598,1081) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"result protection")
    require(len(p["artifacts"])==3 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"result artifacts")
    s=p["validation_summary"]
    require(s["parent_results"]==expected_results() and s["observations"]==38880
            and (len(s["partitions"]),len(s["value_pairs"]),len(s["comparisons"]))==(90,540,60),"result inventory")
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False,"diagnostic scope")
    for k in ZERO_KEYS:require(type(s[k]) is int and s[k]==0,"zero workload:"+k)


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite):yield from flatten(t)
        else:yield t


def regression_modules(root):
    names=context()[0].regression_modules(root)
    require(len(names)==len(set(names))==manifest()["modules"]-1,"parent modules")
    return names+["tests_lm.test_v05_c292_saved_answer_roles"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==manifest()["loaded_tests"] and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED];require(len(kept)==manifest()["focused_tests"],"focused suite")
    return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head
            and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    _,c=context();root=Path(__file__).resolve().parents[2];guard(root,expected_head,c)
    pins,protected=precheck(summaries,root)
    with no_neural():
        _,records,data,metrics=load_parent(summaries);report,summary=analyze(records,data,metrics)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for n,v in zip(OUTPUTS,(manifest(),report,summary),strict=True):(out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c);precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
           source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
           capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(p);(out/"summary.json").write_bytes(blob(p))
    receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","diagnostic_execution_valid","artifacts")}
    receipt.update(source_pins=len(pins),protected_inputs=len(protected),summary_sha256=c.audit.sha(out/"summary.json"))
    print("=== C292 COMPACT RESULT RECEIPT ===",flush=True);print(json.dumps(receipt,indent=2,sort_keys=True),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    _,c=context();out=Path(outdir);p=c.audit.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,w in p["input_sha256"].items():require(c.audit.sha(n)==w,"protected input")
    for a in p["artifacts"]:
        child=c.audit.safe_child(out,a["file"])
        require(c.audit.sha(child)==a["sha256"] and child.stat().st_size==a["serialized_bytes"],"output bytes")
    with no_neural():
        _,records,data,metrics=load_parent(summaries);report,summary=analyze(records,data,metrics)
    for n,v in zip(OUTPUTS,(manifest(),report,summary),strict=True):require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==summary,"summary reconstruction");return p,report


def main():
    p=argparse.ArgumentParser();p.add_argument("--summaries",nargs=18,type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True);p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__=="__main__":main()
