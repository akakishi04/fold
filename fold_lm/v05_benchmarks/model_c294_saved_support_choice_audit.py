"""C294: conditional fact ranking in sealed C293 outputs; diagnostic, never a decoder."""
from __future__ import annotations
import argparse
from collections import Counter
from contextlib import contextmanager
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
from types import ModuleType
import unittest
from unittest.mock import patch
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C294-v5b-saved-support-choice-audit"
STAGE = "V5-B-SAVED-SUPPORT-CHOICE-AUDIT"
BASE = "8bdfdeae1daeab051af6407e5101578e66c1d06f"
PARENT_EXECUTION = "318d9fd76f4253b30d68645ee34c124457be78a3"
PARENT_SHA = "61a92e5d5775381cc1b7ef0fa19a9fa393197afd05a7642b74b0486ab6d338e6"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c293_fact_support_loss.py"
PARENT_BLOB = "9514bb3db5abfac91666ee67b1e1973511a2b682"
SEEDS = tuple(range(293001,293006))
ARMS = ("ce_only","scaled_ce","support_weighted")
PROFILES = {"two_char":("doubled","shared_prefix","shared_suffix"),
            "triple":("tripled","shared_prefix2","shared_suffix2"),
            "quad":("quadrupled","shared_prefix3","shared_suffix3")}
KINDS = ("full_correct","outside_correct_choice","outside_wrong_choice","other_fact")
ROLES = ("target","other_fact","absent_known_value","non_value_byte")
OWN = ("fold_lm/v05_benchmarks/model_c294_saved_support_choice_audit.py",
       "tests_lm/test_v05_c294_saved_support_choice_audit.py","tools/run_c294.ps1","tools/invoke_c294.ps1",
       "docs/experiment-ledger-addendum-c294-preregistration.md","docs/v5b-saved-support-choice-audit-v0.1.md")
OUTPUTS = ("audit-plan.json","support-choice-report.json","validation-summary.json")
PARENT_OUTPUTS = ("architecture-plan.json","dataset.json","triple-dataset.json","quad-dataset.json",
                  "trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
ZERO_KEYS = ("model_forward_calls","train_steps","model_state_loads","new_checkpoint_writes",
             "row_presentations","core_forward_calls","network_calls")
MANIFEST_SHA = "e929d73dabbcc3c6c229c46282854f8c196802e4e52995f10eb94b977b9ba1c6"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(v):
    return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(v): return hashlib.sha256(blob(v)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c293_fact_support_loss as parent
    return parent,parent.context()[-1]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION,parent_summary_sha256=PARENT_SHA,
                parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,parent_outputs=list(PARENT_OUTPUTS),
                parents="20 ordered summaries:C293,C292,C291,C290,C289,C288..C274;hashes before dispatch",
                seeds=list(SEEDS),arms=list(ARMS),kinds=list(KINDS),roles=list(ROLES),
                question="when the full winner is outside the stated values,is the within-fact target ranking correct",
                support="unordered two values from verified logical input facts,not chosen from target or predictions",
                tie_break="lowest numeric class index for both full and support argmax;exact ties reported separately",
                decomposition="stable log-softmax CE=Lsupport+Lchoice;rtol=atol=1e-10",
                scope="oracle-support numerical diagnostic on normal logits only;no decoder or capability promotion",
                observations=38880,partitions=90,profile_language_groups=540,comparisons=60,comparison_rows=25920,
                source_pins=610,protected_inputs=1106,own_tests=32,modules=179,loaded_tests=4390,focused_tests=4389,
                excluded_test=EXCLUDED,capability_gate_applicable=False,gate_f_candidate=False,
                production_adoption=False,**dict.fromkeys(ZERO_KEYS,0))


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def expected_results():
    out=[]
    for seed,arm in identities():
        seen=seed!=293004
        quad=seed in ({293002,293005} if arm==ARMS[0] else {293003} if arm==ARMS[1] else {293002,293003})
        out.append(dict(seed=seed,arm=arm,passed=quad,quad_pass=quad,two_char_pass=seen,triple_pass=seen,
                        all_tasks_pass=quad,fitted_train_direct_pass=seen,seen_holdout_direct_pass=seen))
    return out


def fact_support(row):
    e,v,q=row["entities"],row["values"],row["query"]
    require(len(e)==len(v)==2 and len(set(e))==len(set(v))==2,"two distinct facts")
    require(all(type(x) is int and 0<=x<3 for x in e) and all(type(x) is int and 0<=x<4 for x in v),"fact domain")
    require(type(q) is int and q in e and sorted(row["permutation"])==sorted(e),"query/order")
    require(type(row["target"]) is int and row["target"]==48+v[e.index(q)],"target binding")
    return sorted(48+x for x in v)


def measure(logits,rows):
    require(isinstance(logits,torch.Tensor) and logits.shape==(len(rows),256) and len(rows)>0,"logit shape")
    require(logits.dtype==torch.float64 and logits.device.type=="cpu" and not logits.requires_grad
            and bool(torch.isfinite(logits).all()),"saved tensor contract")
    support=torch.tensor([fact_support(r) for r in rows],dtype=torch.int64)
    y=torch.tensor([r["target"] for r in rows],dtype=torch.int64)
    local=logits.gather(1,support)
    full=logits.argmax(1);conditional=support.gather(1,local.argmax(1,keepdim=True)).squeeze(1)
    mask=torch.zeros_like(logits,dtype=torch.bool).scatter_(1,support,True)
    outside_max=logits.masked_fill(mask,float("-inf")).max(1).values
    within_max=local.max(1).values
    logp=F.log_softmax(logits,dim=1)
    logmass=torch.logsumexp(logp.gather(1,support),dim=1)
    support_nll=-logmass;ce=-logp.gather(1,y[:,None]).squeeze(1)
    choice_nll=logmass-logp.gather(1,y[:,None]).squeeze(1)
    other=support.sum(1)-y
    choice_gap=logits.gather(1,y[:,None]).squeeze(1)-logits.gather(1,other[:,None]).squeeze(1)
    require(all(bool(torch.isfinite(t).all()) for t in (ce,support_nll,choice_nll,choice_gap,within_max-outside_max)),"derived finite")
    require(torch.allclose(ce,support_nll+choice_nll,rtol=1e-10,atol=1e-10),"CE decomposition")
    require(bool((support_nll>=-1e-10).all()) and bool((choice_nll>=-1e-10).all()),"nonnegative losses")
    result=[]
    for i,r in enumerate(rows):
        f,k,t,o=int(full[i]),int(conditional[i]),int(y[i]),int(other[i])
        inside=f in (t,o);correct=f==t;choice_correct=k==t
        require(not correct or choice_correct,"full-correct monotonicity")
        require(not inside or f==k,"support-ranking consistency")
        kind=KINDS[0] if correct else KINDS[3] if inside else KINDS[1] if choice_correct else KINDS[2]
        role="target" if correct else "other_fact" if inside else "absent_known_value" if 48<=f<=51 else "non_value_byte"
        result.append(dict(source_id=r["id"],language=r["language"],entities=r["entities"],values=r["values"],
                           permutation=r["permutation"],query=r["query"],support=support[i].tolist(),target=t,other_value=o,
                           full_prediction=f,conditional_prediction=k,full_correct=correct,conditional_correct=choice_correct,
                           kind=kind,output_role=role,choice_tie=bool(local[i,0]==local[i,1]),
                           support_outside_tie=bool(within_max[i]==outside_max[i]),choice_gap=float(choice_gap[i]),
                           support_outside_gap=float(within_max[i]-outside_max[i]),support_mass=float(logmass[i].exp()),
                           answer_nll=float(ce[i]),support_nll=float(support_nll[i]),choice_nll=float(choice_nll[i])))
    return result


def aggregate(rows):
    require(bool(rows),"empty aggregate")
    counts=Counter(r["kind"] for r in rows);roles=Counter(r["output_role"] for r in rows)
    require(set(counts)<=set(KINDS) and set(roles)<=set(ROLES),"classification inventory")
    n=len(rows);correct=sum(r["full_correct"] for r in rows);cc=sum(r["conditional_correct"] for r in rows)
    require(correct==counts[KINDS[0]]==roles["target"] and cc-correct==counts[KINDS[1]],"classification reconstruction")
    result=dict(rows=n,correct=correct,conditional_correct=cc,conditional_errors=n-cc,
                kind_counts={k:counts[k] for k in KINDS},output_role_counts={k:roles[k] for k in ROLES},
                choice_ties=sum(r["choice_tie"] for r in rows),support_outside_ties=sum(r["support_outside_tie"] for r in rows))
    for k in ("answer_nll","support_nll","choice_nll","support_mass"):
        result["mean_"+k]=math.fsum(r[k] for r in rows)/n
    require(math.isclose(result["mean_answer_nll"],result["mean_support_nll"]+result["mean_choice_nll"],rel_tol=1e-10,abs_tol=1e-10),"aggregate decomposition")
    return result


def collapse(rows):
    groups={}
    for r in rows:
        key=(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))
        groups.setdefault(key,[]).append(r)
    require(all(len(v)==2 and {r["query"] for r in v}==set(k[1]) for k,v in groups.items()),"query pair coverage")
    return sum(v[0]["full_prediction"]==v[1]["full_prediction"] for v in groups.values())


def compare(a,b):
    require(len(a)==len(b)>0,"comparison size")
    transitions=Counter();full_flips=conditional_flips=rescued=regressed=0
    for x,y in zip(a,b,strict=True):
        require(all(x[k]==y[k] for k in ("task","split","profile","source_id","support","target")),"comparison identity")
        transitions[(x["kind"],y["kind"])]+=1
        full_flips+=x["full_prediction"]!=y["full_prediction"]
        conditional_flips+=x["conditional_prediction"]!=y["conditional_prediction"]
        rescued+=not x["full_correct"] and y["full_correct"];regressed+=x["full_correct"] and not y["full_correct"]
    return dict(rows=len(a),full_argmax_flips=full_flips,conditional_argmax_flips=conditional_flips,
                rescued=rescued,regressed=regressed,transitions={x+"->"+y:transitions[(x,y)] for x,y in itertools.product(KINDS,repeat=2)})


def analyze(records,data,metrics,old_partitions):
    require([(r["seed"],r["arm"]) for r in records]==identities() and [(r["seed"],r["arm"]) for r in metrics]==identities(),"model identities")
    require(set(data)=={"TRAIN","HOLDOUT"},"data splits")
    for split,n in (("TRAIN",192),("HOLDOUT",96)):
        require(len(data[split])==n and len({r["id"] for r in data[split]})==n,"data inventory")
    old={(r["seed"],r["arm"],r["task"],r["split"]):r for r in old_partitions}
    expected=set(itertools.product(SEEDS,ARMS,PROFILES,("TRAIN","HOLDOUT")))
    require(len(old_partitions)==len(old)==90 and set(old)==expected,"parent partition coverage")
    observations=[];partitions=[];details=[];lookup={}
    for raw,m in zip(records,metrics,strict=True):
        require(set(raw["raw"])==set(PROFILES),"task coverage")
        for task,profiles in PROFILES.items():
            require(set(raw["raw"][task])=={"TRAIN","HOLDOUT"},"split coverage")
            for split in ("TRAIN","HOLDOUT"):
                require(set(raw["raw"][task][split])==set(profiles),"profile coverage")
                part=[]
                for profile in profiles:
                    views=raw["raw"][task][split][profile]
                    require(set(views)=={"normal","evidence_blind","query_blind"},"view coverage")
                    selected=[dict(seed=raw["seed"],arm=raw["arm"],task=task,split=split,profile=profile,**v)
                              for v in measure(views["normal"],data[split])]
                    for language in ("en","ja"):
                        rr=[r for r in selected if r["language"]==language];agg=aggregate(rr)
                        prior=[v for v in m[task]["totals"] if (v["split"],v["profile"],v["language"])==(split,profile,language)]
                        require(len(prior)==1 and all(agg[k]==prior[0][k] for k in ("rows","correct"))
                                and prior[0]["pairs"]==len(rr)//2 and prior[0]["collapsed_pairs"]==collapse(rr),"parent normal totals")
                        details.append(dict(seed=raw["seed"],arm=raw["arm"],task=task,split=split,profile=profile,language=language,**agg))
                    part.extend(selected)
                key=(raw["seed"],raw["arm"],task,split);agg=aggregate(part);prior=old[key]
                require(all(agg[k]==prior[k] for k in ("rows","correct","output_role_counts"))
                        and math.isclose(agg["mean_answer_nll"],prior["final_normal_nll"],rel_tol=1e-10,abs_tol=1e-10),"parent final partition")
                partitions.append(dict(seed=key[0],arm=key[1],task=task,split=split,**agg));lookup[key]=part;observations.extend(part)
    comparisons=[dict(seed=s,task=t,split=p,comparator=a,candidate=ARMS[2],
                      **compare(lookup[(s,a,t,p)],lookup[(s,ARMS[2],t,p)]))
                 for s,t,p,a in itertools.product(SEEDS,PROFILES,("TRAIN","HOLDOUT"),ARMS[:2])]
    require((len(observations),len(partitions),len(details),len(comparisons))==(38880,90,540,60)
            and sum(r["rows"] for r in comparisons)==25920,"audit inventory")
    summary=dict(parent_results=expected_results(),observations=len(observations),partitions=partitions,comparisons=comparisons,
                 diagnostic_complete=True,capability_gate_applicable=False,**dict.fromkeys(ZERO_KEYS,0))
    return dict(observations=observations,profile_language=details,summary=summary),summary


@contextmanager
def no_neural():
    with torch.no_grad(),patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C294 forbids neural calls")), \
         patch.object(torch.nn.Module,"load_state_dict",side_effect=RuntimeError("C294 forbids model state loads")), \
         patch.object(torch,"save",side_effect=RuntimeError("C294 forbids checkpoint writes")):
        yield


def load_parent(paths):
    parent,c=context();paths=[Path(p).resolve() for p in paths];p292,p291,*_=parent.context();old=p291.context()
    wanted=(PARENT_SHA,parent.PARENT_SHA,p292.PARENT_SHA,p291.PARENT_SHA,old[0].PARENT_SHA,*old[1].SUMMARY_SHAS)
    require(len(paths)==len(wanted)==20 and all(c.audit.sha(p)==w for p,w in zip(paths,wanted,strict=True)),"parent hashes")
    with no_neural():
        p,metrics=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION);parent.validate_result(p)
        require(p["experiment_id"]=="C293-v5b-fact-support-loss" and p["commit_sha"]==PARENT_EXECUTION
                and p["status"]=="FAIL" and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity")
        require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(PARENT_OUTPUTS),"parent artifacts")
        s=p["validation_summary"]
        require(s["seed_results"]==expected_results() and s["candidate_gate"] is False
                and s["all_groups_matched"] is True and s["all_replays"] is True,"parent result")
        data=c.audit.read_json(paths[0].parent/"dataset.json");c.p267.validate_data(data)
        archive=torch.load(paths[0].parent/"evaluations.pt",map_location="cpu",weights_only=True)
    require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c293-support-eval-v1","archive schema")
    return p,archive["records"],data,metrics


def precheck(paths,root):
    validate_seal();p,_,_,_=load_parent(paths);parent,c=context();root=Path(root).resolve()
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    require((len(pins),len(protected))==(604,1091),"inherited counts")
    for n,w in pins.items():require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==w,"changed source:"+n)
    for n,w in protected.items():require(Path(n).is_file() and c.audit.sha(n)==w,"changed input:"+n)
    modules=[parent]+[m for m in parent.context() if isinstance(m,ModuleType)]+[m for m in vars(c).values() if isinstance(m,ModuleType)]
    covered=set()
    for m in modules:
        path=getattr(m,"__file__",None)
        if path and Path(path).resolve().is_relative_to(root):
            name=Path(path).resolve().relative_to(root).as_posix();require(name in pins,"unprotected helper:"+name);covered.add(name)
    require(PARENT_SOURCE in covered and pins[PARENT_SOURCE]==PARENT_BLOB,"parent coverage")
    directory=Path(paths[0]).resolve().parent
    for child,w in [(Path(paths[0]).resolve(),PARENT_SHA)]+[(c.audit.safe_child(directory,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(child.resolve()) not in protected and c.audit.sha(child)==w,"parent input");protected[str(child.resolve())]=w
    for n in OWN:
        require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(610,1106),"protection counts")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS" and p["diagnostic_execution_valid"] is True,"result identity")
    require(all(p[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")),"result scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(610,1106) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"result protection")
    require(len(p["artifacts"])==3 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"result artifacts")
    s=p["validation_summary"]
    require(s["parent_results"]==expected_results() and s["observations"]==38880 and (len(s["partitions"]),len(s["comparisons"]))==(90,60),"result inventory")
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False,"diagnostic scope")
    for k in ZERO_KEYS:require(type(s[k]) is int and s[k]==0,"zero workload:"+k)


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite):yield from flatten(t)
        else:yield t


def regression_modules(root):
    names=context()[0].regression_modules(root)
    require(len(names)==len(set(names))==manifest()["modules"]-1,"parent modules")
    return names+["tests_lm.test_v05_c294_saved_support_choice_audit"]


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
    _,c=context();root=Path(__file__).resolve().parents[2];guard(root,expected_head,c);pins,protected=precheck(summaries,root)
    with no_neural():
        parent,records,data,metrics=load_parent(summaries)
        report,summary=analyze(records,data,metrics,parent["validation_summary"]["final_partitions"])
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
    print("=== C294 COMPACT RESULT RECEIPT ===",flush=True);print(json.dumps(receipt,indent=2,sort_keys=True),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    _,c=context();out=Path(outdir);p=c.audit.read_json(out/"summary.json");validate_result(p);require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,w in p["input_sha256"].items():require(c.audit.sha(n)==w,"protected input")
    for a in p["artifacts"]:
        child=c.audit.safe_child(out,a["file"]);require(c.audit.sha(child)==a["sha256"] and child.stat().st_size==a["serialized_bytes"],"output bytes")
    with no_neural():
        parent,records,data,metrics=load_parent(summaries)
        report,summary=analyze(records,data,metrics,parent["validation_summary"]["final_partitions"])
    for n,v in zip(OUTPUTS,(manifest(),report,summary),strict=True):require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==summary,"summary reconstruction");return p,report


def main():
    p=argparse.ArgumentParser();p.add_argument("--summaries",nargs=20,type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True);p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__=="__main__":main()
