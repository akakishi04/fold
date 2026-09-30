"""C290: assignment-margin correctness and aligned prediction changes from saved logits only."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import re
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C290-v5b-saved-pair-margin-audit"
STAGE = "V5-B-SAVED-PAIR-MARGIN-AUDIT"
BASE = "4ffae6420500e0233c1b19df07f6f0cfac73c16d"
PARENT_EXECUTION = "b5026f48e0c8b39bbfb9069f34271d7b6ba9d50f"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c289_early_pair_withdrawal.py"
PARENT_BLOB = "d5e2231d1d1a1e39b5628129f3ca2ef9838c9951"
PARENT_SHA = "151117fcd43177b8e393eeee6935222e54f01caecf8a17b4656149aec5058897"
SEEDS = tuple(range(289001,289006))
ARMS = ("ce_only","pair_always","pair_early")
PROFILES = {"two_char":("doubled","shared_prefix","shared_suffix"),
            "triple":("tripled","shared_prefix2","shared_suffix2"),
            "quad":("quadrupled","shared_prefix3","shared_suffix3")}
PARENT_OUTPUTS = ("architecture-plan.json","dataset.json","triple-dataset.json","quad-dataset.json",
                  "trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")
OWN = ("fold_lm/v05_benchmarks/model_c290_saved_pair_margin_audit.py",
       "tests_lm/test_v05_c290_saved_pair_margin_audit.py","tools/run_c290.ps1","tools/invoke_c290.ps1",
       "docs/experiment-ledger-addendum-c290-preregistration.md","docs/v5b-saved-pair-margin-audit-v0.1.md")
OUTPUTS = ("audit-plan.json","pair-margin-report.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
ZERO_KEYS = ("model_forward_calls","row_presentations","core_forward_calls","train_steps",
             "model_state_loads","new_checkpoint_writes","network_calls")
MANIFEST_SHA = "123a8805343a6c7704ff6042d83928d3069aa43fe79e213e2b5798811d35b6f3"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c289_early_pair_withdrawal as parent
    return parent,parent.context()[5]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
                parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,parent_summary_sha256=PARENT_SHA,
                parent_artifacts="all eight names/hash/size triples committed by exact parent summary SHA; verify before loading",
                parent_outputs=list(PARENT_OUTPUTS),ancestor_hashes="15 ordered immutable C289.SUMMARY_SHAS plus exact C289 summary",
                seeds=list(SEEDS),arms=list(ARMS),profiles={k:list(v) for k,v in PROFILES.items()},
                question="does a satisfied assignment margin coexist with wrong individual answers,and which aligned answers change after withdrawal",
                margin=1.,margin_scope="descriptive existing auxiliary margin only;never a replacement capability gate",
                views="normal saved logits only;parent independently verifies all original masked/full gates",
                pair_records=19440,partitions=90,comparisons=60,comparison_pairs=12960,
                source_pins=586,protected_inputs=1056,dependency_union=66,own_tests=40,
                modules=175,loaded_tests=4246,focused_tests=4245,excluded_test=EXCLUDED,
                capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,
                console="compact validated receipt and partitions;full protected maps and per-pair report stay local",**dict.fromkeys(ZERO_KEYS,0))


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None,"manifest not sealed")
    require(digest(manifest())==MANIFEST_SHA,"manifest digest mismatch")


def expected_results():
    out=[]
    for seed,arm in identities():
        seen=seed>=289003 if arm=="ce_only" else seed>=289002
        fit=seed!=289002 if arm=="ce_only" else (arm=="pair_always" or seed!=289001)
        quad=arm=="ce_only" and seed>=289003
        out.append(dict(seed=seed,arm=arm,passed=quad,quad_pass=quad,two_char_pass=seen,triple_pass=seen,
                        all_tasks_pass=quad,fitted_train_direct_pass=fit,seen_holdout_direct_pass=seen))
    return out


def pair_indices(rows):
    groups={}
    for i,r in enumerate(rows):
        key=(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups.setdefault(key,[]).append(i)
    out=[]
    for key in sorted(groups):
        ids=sorted(groups[key],key=lambda i:rows[i]["query"])
        require(len(ids)==2 and [rows[i]["query"] for i in ids]==list(key[1]),"complete pair queries")
        labels=[rows[i]["target"] for i in ids]
        require(all(type(y) is int and 0<=y<256 for y in labels) and labels[0]!=labels[1],"pair targets")
        out.append((key,ids))
    require(sorted(i for _,ids in out for i in ids)==list(range(len(rows))),"pair coverage")
    return out


def pair_values(logits,targets):
    require(isinstance(logits,torch.Tensor) and logits.ndim==2 and logits.shape[1]==256
            and len(logits)>0 and len(logits)%2==0,"logit shape")
    require(logits.dtype==torch.float64 and logits.device.type=="cpu" and not logits.requires_grad
            and targets.dtype==torch.int64 and targets.shape==(len(logits),) and targets.device==logits.device,"tensor contract")
    require(bool(torch.isfinite(logits).all()) and bool(((targets>=0)&(targets<256)).all()),"finite/range")
    z=logits.reshape(-1,2,256);y=targets.reshape(-1,2);i=torch.arange(len(y))
    require(bool((y[:,0]!=y[:,1]).all()),"distinct targets")
    correct_score=z[i,0,y[:,0]]+z[i,1,y[:,1]];swapped_score=z[i,0,y[:,1]]+z[i,1,y[:,0]]
    gap=correct_score-swapped_score
    penalty=F.softplus(1.-gap);pred=z.argmax(-1);correct=(pred==y).sum(-1)
    ce=F.cross_entropy(logits,targets,reduction="none").reshape(-1,2).mean(1)
    require(bool(torch.isfinite(gap).all()) and bool(torch.isfinite(penalty).all()) and bool(torch.isfinite(ce).all()),"finite derived")
    return [dict(targets=y[j].tolist(),predictions=pred[j].tolist(),correct_answers=int(correct[j]),
                 collapsed=bool(pred[j,0]==pred[j,1]),assignment_gap=float(gap[j]),
                 margin_met=bool(gap[j]>=1.),pair_penalty=float(penalty[j]),mean_answer_nll=float(ce[j])) for j in range(len(y))]


def aggregate(records):
    require(bool(records),"empty aggregate")
    n=len(records);both=sum(r["correct_answers"]==2 for r in records);met=sum(r["margin_met"] for r in records)
    wrong_met=sum(r["margin_met"] and r["correct_answers"]<2 for r in records)
    return dict(pairs=n,rows=2*n,correct=sum(r["correct_answers"] for r in records),
                both_correct=both,one_correct=sum(r["correct_answers"]==1 for r in records),
                neither_correct=sum(r["correct_answers"]==0 for r in records),
                collapsed_pairs=sum(r["collapsed"] for r in records),margin_met=met,
                margin_met_with_error=wrong_met,margin_not_met_with_both_correct=sum(not r["margin_met"] and r["correct_answers"]==2 for r in records),
                mean_pair_penalty=math.fsum(r["pair_penalty"] for r in records)/n,
                mean_answer_nll=math.fsum(r["mean_answer_nll"] for r in records)/n)


def compare_pairs(control,candidate):
    require(len(control)==len(candidate)>0,"comparison count")
    changed=rescued=regressed=flips=0
    for a,b in zip(control,candidate,strict=True):
        require(all(a[k]==b[k] for k in ("task","split","profile","pair_key","targets")),"comparison identity")
        f=sum(x!=y for x,y in zip(a["predictions"],b["predictions"],strict=True))
        changed+=f>0;flips+=f
        rescued+=a["correct_answers"]<2 and b["correct_answers"]==2
        regressed+=a["correct_answers"]==2 and b["correct_answers"]<2
    return dict(pairs=len(control),changed_prediction_pairs=changed,argmax_flips=flips,
                rescued_both_correct=rescued,regressed_both_correct=regressed)


def analyze(records,data,metrics):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"record identities")
    require([(r["seed"],r["arm"]) for r in metrics]==identities(),"metric identities")
    pairs=[];partitions=[];lookup={}
    for raw,metric in zip(records,metrics,strict=True):
        require(set(raw["raw"])==set(PROFILES),"raw tasks")
        for task,profiles in PROFILES.items():
            require(set(raw["raw"][task])=={"TRAIN","HOLDOUT"},"raw splits")
            for split in ("TRAIN","HOLDOUT"):
                rows=data[split];require(len(rows)==(192 if split=="TRAIN" else 96),"row count")
                groups=pair_indices(rows);ordered=[i for _,ids in groups for i in ids];part=[]
                targets=torch.tensor([rows[i]["target"] for i in ordered],dtype=torch.int64)
                require(set(raw["raw"][task][split])==set(profiles),"profile coverage")
                for profile in profiles:
                    views=raw["raw"][task][split][profile]
                    require(set(views)=={"normal","evidence_blind","query_blind"},"view schema")
                    z=views["normal"];require(tuple(z.shape)==(len(rows),256),"normal shape")
                    values=pair_values(z[ordered],targets);profile_rows=[]
                    for (key,_),v in zip(groups,values,strict=True):
                        row=dict(seed=raw["seed"],arm=raw["arm"],task=task,split=split,profile=profile,
                                 pair_key=[key[0],list(key[1]),list(key[2]),list(key[3])],**v)
                        profile_rows.append(row)
                    for language in ("en","ja"):
                        selected=[r for r in profile_rows if r["pair_key"][0]==language]
                        got=aggregate(selected)
                        old=[r for r in metric[task]["totals"] if (r["split"],r["profile"],r["language"])==(split,profile,language)]
                        require(len(old)==1 and all(got[k]==old[0][k] for k in ("rows","pairs","correct","collapsed_pairs")),"parent normal totals")
                    part.extend(profile_rows)
                require(len(part)==(288 if split=="TRAIN" else 144),"partition pair count")
                partitions.append(dict(seed=raw["seed"],arm=raw["arm"],task=task,split=split,**aggregate(part)))
                lookup[(raw["seed"],raw["arm"],task,split)]=part;pairs.extend(part)
    comparisons=[]
    for seed,task,split,arm in itertools.product(SEEDS,PROFILES,("TRAIN","HOLDOUT"),ARMS[:2]):
        comparisons.append(dict(seed=seed,task=task,split=split,comparator=arm,candidate="pair_early",
                                 **compare_pairs(lookup[(seed,arm,task,split)],lookup[(seed,"pair_early",task,split)])))
    require((len(pairs),len(partitions),len(comparisons))==(19440,90,60)
            and sum(r["pairs"] for r in comparisons)==12960,"audit inventory")
    summary=dict(parent_results=expected_results(),pair_records=len(pairs),partitions=partitions,
                 comparisons=comparisons,diagnostic_complete=True,capability_gate_applicable=False,**dict.fromkeys(ZERO_KEYS,0))
    return dict(pairs=pairs,summary=summary),summary


@contextmanager
def no_neural():
    with torch.no_grad(),patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C290 forbids neural calls")), \
         patch.object(torch.nn.Module,"load_state_dict",side_effect=RuntimeError("C290 forbids state loading")), \
         patch.object(torch,"save",side_effect=RuntimeError("C290 forbids checkpoint writes")):
        yield


def validate_parent(p):
    require(p["commit_sha"]==PARENT_EXECUTION and p["experiment_id"]=="C289-v5b-early-pair-withdrawal"
            and p["status"]=="FAIL" and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity/source")
    require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(PARENT_OUTPUTS),"parent artifact inventory")
    for a in p["artifacts"]:
        require(re.fullmatch(r"[0-9a-f]{64}",a["sha256"]) is not None and type(a["serialized_bytes"]) is int
                and a["serialized_bytes"]>0,"parent artifact descriptor")
    s=p["validation_summary"]
    require(s["seed_results"]==expected_results() and s["candidate_gate"] is False
            and all(s[k] is True for k in ("all_replays","all_groups_matched","all_auxiliary_prefixes_matched")),"parent results")


def load_parent(paths):
    parent,c=context();paths=[Path(p).resolve() for p in paths]
    wanted=(PARENT_SHA,*parent.SUMMARY_SHAS)
    require(len(paths)==len(wanted)==16 and all(c.audit.sha(p)==w for p,w in zip(paths,wanted,strict=True)),"parent hashes")
    with no_neural():
        p,metrics=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION)
        parent.validate_result(p);validate_parent(p)
        data=c.audit.read_json(paths[0].parent/"dataset.json");c.p267.validate_data(data)
        v=torch.load(paths[0].parent/"evaluations.pt",map_location="cpu",weights_only=True)
    require(set(v)=={"schema","records"} and v["schema"]=="fold-c289-early-pair-eval-v1","parent archive schema")
    return p,v["records"],data,metrics


def precheck(paths,root):
    validate_seal();p,_,_,_=load_parent(paths);_,c=context();root=Path(root);directory=Path(paths[0]).resolve().parent
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for n,w in pins.items():require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==w,"changed source:"+n)
    for n,w in protected.items():require(Path(n).is_file() and c.audit.sha(n)==w,"changed input:"+n)
    for child,w in [(Path(paths[0]).resolve(),PARENT_SHA)]+[(c.audit.safe_child(directory,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(child.resolve()) not in protected and c.audit.sha(child)==w,"parent input")
        protected[str(child.resolve())]=w
    for n in OWN:
        require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9]|27[0-9]|28[0-9])_[^/]+)\.py"
    deps=set(c.factory.LM_SOURCES)|{n for n in p["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps)==manifest()["dependency_union"] and deps<=set(pins) and pins.get(PARENT_SOURCE)==PARENT_BLOB,"dependency coverage")
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(586,1056),"protection cardinality")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS"
            and p["diagnostic_execution_valid"] is True,"result identity")
    require(all(p[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")),"result scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(586,1056) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"result protection")
    require(len(p["artifacts"])==3 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"output set")
    s=p["validation_summary"]
    require(s["parent_results"]==expected_results() and s["pair_records"]==19440
            and (len(s["partitions"]),len(s["comparisons"]))==(90,60),"result inventory")
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False,"diagnostic scope")
    for k in ZERO_KEYS:require(type(s[k]) is int and s[k]==0,"zero workload:"+k)


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite):yield from flatten(t)
        else:yield t


def regression_modules(root):
    names=context()[0].regression_modules(root)
    require(len(names)==len(set(names))==manifest()["modules"]-1,"parent modules")
    return names+["tests_lm.test_v05_c290_saved_pair_margin_audit"]


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
        parent,records,data,metrics=load_parent(summaries);report,summary=analyze(records,data,metrics)
    require(summary["parent_results"]==parent["validation_summary"]["seed_results"],"parent flags")
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for n,v in zip(OUTPUTS,(manifest(),report,summary),strict=True):(out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c);precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
           source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
           capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(p);(out/"summary.json").write_bytes(blob(p))
    receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","diagnostic_execution_valid","artifacts","capability_gate_applicable")}
    receipt.update(source_pins=len(pins),protected_inputs=len(protected),summary_sha256=c.audit.sha(out/"summary.json"))
    print("=== C290 COMPACT RESULT RECEIPT ===",flush=True)
    print(json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False),flush=True)
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
    p=argparse.ArgumentParser();p.add_argument("--summaries",nargs=16,type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True);p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__=="__main__":main()
