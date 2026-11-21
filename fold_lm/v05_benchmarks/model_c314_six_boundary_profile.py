"""C314: localize saved five-to-six degradation without changing any prediction."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
from types import ModuleType
import unittest
import torch

EXPERIMENT_ID = "C314-v5b-saved-six-boundary-profile"
STAGE = "V5-B-SAVED-SIX-BOUNDARY-PROFILE"
BASE = "9221bfbe539d3f91fa3a74caa355e4059c9453fe"
PARENT_EXECUTION = "bc6a226b8605b6ae04e64d46a387487533c0bdc0"
PARENT_SHA = "adfeb06f6db5b77feb172b8ede1f3bf7032c8ca35b299d7ecc692baeca097c97"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c313_frozen_six_transfer.py"
PARENT_BLOB = "bf514ad80f85140e81b834d00aceb3379f4bfd80"
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
OLD_PROMPTS_SHA = "ecf2c9784213ac8fcebfd9ac03bea42317629edcea330771c92c72d71777583d"
SIX_PROMPTS_SHA = "b6bdc8d667376cf8b0e3f98084b676abafc7992a0a63b90cb0b20add15947d72"
SEEDS = tuple(range(312001,312006))
ARMS = ("random_pairs","value_balanced")
PROFILES = ("repeat","shared_prefix","shared_suffix")
OLD_PROFILES = ("tripled","shared_prefix2","shared_suffix2")
SPLITS = ("TRAIN","HOLDOUT")
LANGUAGES = ("en","ja")
OWN = ("fold_lm/v05_benchmarks/model_c314_six_boundary_profile.py",
       "tests_lm/test_v05_c314_six_boundary_profile.py","tools/run_c314.ps1","tools/invoke_c314.ps1",
       "docs/experiment-ledger-addendum-c314-preregistration.md","docs/v5b-six-boundary-profile-v0.1.md")
OUTPUTS = ("audit-plan.json","boundary-report.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
ZERO = dict(train_steps=0,model_forward_calls=0,model_state_loads=0,new_checkpoint_writes=0,
            row_presentations=0,core_forward_calls=0,network_calls=0)
TRANSITIONS = ("both_correct","new_error","recovered","both_wrong")
CLASSES = ("correct","other_fact","unmentioned_digit","other_output")
MANIFEST_SHA = "e249986e20378fd3833dfb26183f94a74b93af3702149ce38bf2c03ba07c5a91"


def require(ok,message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c313_frozen_six_transfer as parent
    chain=parent.context()
    return parent,chain[1],chain[3],chain[-1]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,
        data_sha256=DATA_SHA,old_prompts_sha256=OLD_PROMPTS_SHA,six_prompts_sha256=SIX_PROMPTS_SHA,
        question="where does saved five-to-six deterioration occur by language and name profile at fixed weights and logical rows",
        seeds=list(SEEDS),arms=list(ARMS),profiles=list(PROFILES),languages=list(LANGUAGES),splits=list(SPLITS),
        source="C313 raw.before['5'] and raw.six normal logits,not after controls or selected outputs",
        margin="target logit minus largest of ALL255 non-target logits;full256 first-index argmax;ties reported",
        errors=list(CLASSES),transitions=list(TRANSITIONS),paired_rows=8640,observations=17280,groups=120,
        original_local_totals=120,original_transition_totals=20,parents=40,source_pins=730,protected_inputs=1369,
        own_tests=24,modules=199,loaded_tests=5054,focused_tests=5053,excluded_test=EXCLUDED,
        diagnostic_gate="all saved rows aligned,old local scores and transitions reconciled,report independently reconstructed",
        limits="language,UTF8 length and EOS position covary;profile also changes content;no causal separation or probability calibration",
        numeric_threads=2,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,**ZERO)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def expected_parent_results():
    return [dict(seed=s,arm=a,five_pass=not(s==312002 and a==ARMS[1]),
                 six_pass=s==312004 or (s==312005 and a==ARMS[0])) for s,a in identities()]


def answer_class(row,prediction):
    require(type(prediction) is int and 0<=prediction<256,"prediction domain")
    if prediction==row["target"]: return "correct"
    other=48+row["values"][1-row["entities"].index(row["query"])]
    if prediction==other: return "other_fact"
    return "unmentioned_digit" if 48<=prediction<52 else "other_output"


def logit_features(z,targets):
    require(isinstance(z,torch.Tensor) and z.shape==(len(targets),256) and z.dtype==torch.float64
            and z.device.type=="cpu" and not z.requires_grad and bool(torch.isfinite(z).all()),"saved normal logits")
    require(all(type(t) is int and 0<=t<256 for t in targets),"targets")
    y=torch.tensor(targets,dtype=torch.int64); indices=torch.arange(len(targets))
    competitors=z.clone(); competitors[indices,y]=-torch.inf
    margins=z[indices,y]-competitors.max(1).values
    require(bool(torch.isfinite(margins).all()),"finite margin")
    return z.argmax(1).tolist(),margins.tolist(),((z==z.max(1,keepdim=True).values).sum(1)>1).tolist()


def numeric_summary(values):
    require(values and all(type(x) in (int,float) and math.isfinite(x) for x in values),"finite numeric group")
    mean=math.fsum(x/len(values) for x in values)
    require(math.isfinite(mean),"finite group mean")
    return dict(mean=mean,minimum=min(values),maximum=max(values))


def aggregate(rows):
    require(rows,"empty group")
    counts={k:0 for k in TRANSITIONS}; errors={str(n):dict.fromkeys(CLASSES,0) for n in (5,6)}
    for r in rows:
        a=r["class5"]=="correct"; b=r["class6"]=="correct"
        counts["both_correct" if a and b else "new_error" if a else "recovered" if b else "both_wrong"]+=1
        for n in (5,6): errors[str(n)][r[f"class{n}"]]+=1
    delta=[r["margin6"]-r["margin5"] for r in rows]
    out=dict(rows=len(rows),**counts,same_wrong=sum(r["class5"]!="correct" and r["class6"]!="correct" and r["prediction5"]==r["prediction6"] for r in rows),
        five_correct=errors["5"]["correct"],six_correct=errors["6"]["correct"],answer_classes=errors,
        ties5=sum(r["tie5"] for r in rows),ties6=sum(r["tie6"] for r in rows),
        margin5=numeric_summary([r["margin5"] for r in rows]),margin6=numeric_summary([r["margin6"] for r in rows]),
        margin_delta=numeric_summary(delta),margin_decreased=sum(x<0 for x in delta),margin_increased=sum(x>0 for x in delta),
        margin_equal=sum(x==0 for x in delta),tokens5=sorted({r["tokens5"] for r in rows}),tokens6=sorted({r["tokens6"] for r in rows}))
    require(sum(counts.values())==len(rows) and out["six_correct"]-out["five_correct"]==counts["recovered"]-counts["new_error"],"count conservation")
    return out


def analyze(records,data,metrics,parent_summary,old_prompts,six_prompts):
    require(digest(data)==DATA_SHA and digest(old_prompts)==OLD_PROMPTS_SHA and digest(six_prompts)==SIX_PROMPTS_SHA,"input identity")
    require([(r["seed"],r["arm"]) for r in records]==identities()
            and [(r["seed"],r["arm"]) for r in metrics]==identities(),"complete cohort")
    require(parent_summary["seed_results"]==expected_parent_results(),"parent outcome cohort")
    require(set(data)==set(SPLITS) and [len(data[s]) for s in SPLITS]==[192,96],"split domain")
    all_ids=[r["id"] for s in SPLITS for r in data[s]]
    require(len(set(all_ids))==288,"source IDs")
    details=[]; groups=[]; receipts=[]
    for record,metric in zip(records,metrics,strict=True):
        seed,arm=record["seed"],record["arm"]
        require(record["weights_preserved"] is True and record["hooks_restored"] is True
                and set(record["raw"])=={"before","six","after"},"parent record semantics")
        totals=metric["six_score"]["totals"]
        indexed={(r["split"],r["profile"],r["language"]):r for r in totals}
        require(len(totals)==len(indexed)==12,"original six totals")
        for split in SPLITS:
            source=data[split]; model_rows=[]
            for profile,old_profile in zip(PROFILES,OLD_PROFILES,strict=True):
                z5=record["raw"]["before"]["5"][split][profile]["normal"]
                z6=record["raw"]["six"][split][profile]["normal"]
                f5=logit_features(z5,[r["target"] for r in source]); f6=logit_features(z6,[r["target"] for r in source])
                by_language={lang:[] for lang in LANGUAGES}
                for i,row in enumerate(source):
                    require(row["target"]==48+row["values"][row["entities"].index(row["query"])],"target binding")
                    p5=old_prompts["5"][split][profile][i]; p6=six_prompts[split][profile][i]
                    require(p5["source_id"]==p6["source_id"]==row["id"] and p5["target"]==p6["target"]==row["target"],"paired source alignment")
                    tokens=[len(p["views"]["normal"].encode("utf-8"))+2 for p in (p5,p6)]
                    require(tokens==([24,27] if row["language"]=="en" else [54,63]) and max(tokens)<=64,"encoded length")
                    d=dict(seed=seed,arm=arm,split=split,profile=profile,language=row["language"],source_id=row["id"],target=row["target"],
                        prediction5=f5[0][i],prediction6=f6[0][i],margin5=f5[1][i],margin6=f6[1][i],tie5=f5[2][i],tie6=f6[2][i],
                        class5=answer_class(row,f5[0][i]),class6=answer_class(row,f6[0][i]),tokens5=tokens[0],tokens6=tokens[1])
                    by_language[row["language"]].append(d); model_rows.append(d); details.append(d)
                for lang in LANGUAGES:
                    stats=aggregate(by_language[lang]); old=indexed[split,old_profile,lang]
                    require(stats["rows"]==old["rows"] and stats["six_correct"]==old["correct"],"original local score reconciliation")
                    groups.append(dict(seed=seed,arm=arm,split=split,profile=profile,language=lang,**stats))
            stats=aggregate(model_rows)
            original=[r for r in parent_summary["five_to_six"] if (r["seed"],r["arm"],r["split"])==(seed,arm,split)]
            require(len(original)==1 and all(original[0][k]==stats[k] for k in ("rows",*TRANSITIONS,"same_wrong")),"parent transition reconciliation")
            receipts.append(dict(seed=seed,arm=arm,split=split,matched=True,**{k:stats[k] for k in ("rows",*TRANSITIONS,"same_wrong")}))
    require(len(details)==8640 and len(groups)==120 and len(receipts)==20,"inventory")
    totals=aggregate(details)
    summary=dict(diagnostic_complete=True,capability_gate_applicable=False,paired_rows=8640,observations=17280,
        groups=120,original_local_totals_verified=120,original_transitions_verified=20,
        five_correct=totals["five_correct"],six_correct=totals["six_correct"],
        **{k:totals[k] for k in (*TRANSITIONS,"same_wrong")},**ZERO)
    report=dict(parent_summary_sha256=PARENT_SHA,paired_rows=details,groups=groups,parent_transitions=receipts,summary=summary)
    return report,summary


def parent_hashes(parent): return (PARENT_SHA,*parent.parent_hashes(parent.context()[0]))


def load_parent(paths):
    parent,guarded,_,c=context(); paths=[Path(p).resolve() for p in paths]; hashes=parent_hashes(parent)
    require(len(paths)==len(hashes)==40 and all(c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)),"40 parent hashes")
    with guarded.no_neural():
        p,metrics=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); parent.validate_result(p)
        require(p["experiment_id"]=="C313-v5b-frozen-six-transfer" and p["status"]=="FAIL" and p["commit_sha"]==PARENT_EXECUTION
                and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity")
        require(len(p["artifacts"])==5 and {a["file"] for a in p["artifacts"]}==set(parent.OUTPUTS),"parent descriptors")
        s=p["validation_summary"]
        require(s["seed_results"]==expected_parent_results() and s["six_pass_counts"]==dict(random_pairs=2,value_balanced=1)
                and s["primary_arm"]=="random_pairs" and s["primary_gate"] is False and s["all_replays"] is True,"parent scope")
        data=c.audit.read_json(paths[1].parent/"dataset.json"); c.p267.validate_data(data)
        old=c.audit.read_json(paths[1].parent/"length-datasets.json"); six=c.audit.read_json(paths[0].parent/"six-dataset.json")
        require(digest(data)==DATA_SHA and digest(old)==OLD_PROMPTS_SHA and digest(six)==SIX_PROMPTS_SHA,"verified input bytes")
        archive=torch.load(paths[0].parent/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c313-six-transfer-eval-v1","archive schema")
    return p,archive["records"],data,metrics,old,six


def precheck(paths,root):
    validate_seal(); p,*_=load_parent(paths); parent,_,wide,c=context(); root=Path(root).resolve()
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    require((len(pins),len(protected))==(724,1357) and pins.get(PARENT_SOURCE)==PARENT_BLOB
            and all(pins.get(n)==h for n,h in wide.PINNED.items()),"inherited protection")
    for m in [parent,*parent.context(),*parent.context()[0].context(),*wide.context(),*vars(c).values(),c.factory.language_module()]:
        path=getattr(m,"__file__",None) if isinstance(m,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root): require(Path(path).resolve().relative_to(root).as_posix() in pins,"unprotected helper")
    for n,h in pins.items(): require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in protected.items(): require(Path(n).is_file() and c.audit.sha(n)==h,"changed input:"+n)
    folder=Path(paths[0]).resolve().parent
    for path,h in [(folder/"summary.json",PARENT_SHA)]+[(c.audit.safe_child(folder,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h,"parent input"); protected[str(path.resolve())]=h
    for n in OWN: require(n not in pins,"OWN collision"); pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins)); require((len(pins),len(protected))==(730,1369),"protection counts")
    print(f"registration_check = source_pins:730; protected_inputs:1369; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def runtime_preflight(paths,root):
    torch.set_num_threads(2); precheck(paths,root); _,guarded,_,_=context()
    with guarded.no_neural():
        p,records,data,metrics,old,six=load_parent(paths)
        _,s=analyze(records,data,metrics,p["validation_summary"],old,six)
    require(s["paired_rows"]==8640,"real alignment")
    print("real_saved_six_language_profile_alignment = PASS; no new model calls",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS" and p["diagnostic_execution_valid"] is True
            and all(p[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")),"diagnostic identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(730,1369) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"result protection")
    require(len(p["artifacts"])==3 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"]
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False,"scope")
    expected=dict(paired_rows=8640,observations=17280,groups=120,original_local_totals_verified=120,original_transitions_verified=20,**ZERO)
    require(all(type(s[k]) is int and s[k]==v for k,v in expected.items()),"inventory/work")
    require(all(type(s[k]) is int and 0<=s[k]<=8640 for k in (*TRANSITIONS,"same_wrong","five_correct","six_correct"))
            and sum(s[k] for k in TRANSITIONS)==8640 and s["same_wrong"]<=s["both_wrong"]
            and s["five_correct"]==s["both_correct"]+s["new_error"] and s["six_correct"]==s["both_correct"]+s["recovered"],"result conservation")


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==198,"parent modules")
    return names+["tests_lm.test_v05_c314_six_boundary_profile"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==5054 and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED]; require(len(kept)==5053,"focused suite"); return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    torch.set_num_threads(2); _,guarded,_,c=context(); root=Path(__file__).resolve().parents[2]; guard(root,expected_head,c)
    pins,protected=precheck(summaries,root)
    with guarded.no_neural():
        parent,records,data,metrics,old,six=load_parent(summaries)
        report,s=analyze(records,data,metrics,parent["validation_summary"],old,six)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    for n,v in zip(OUTPUTS,(manifest(),report,s),strict=True): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c); precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=s,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    print("=== C314 COMPACT DIAGNOSTIC RECEIPT ===",flush=True)
    print(json.dumps(dict(experiment_id=EXPERIMENT_ID,commit_sha=expected_head,status=p["status"],artifacts=artifacts,summary_sha256=c.audit.sha(out/"summary.json")),indent=2,sort_keys=True),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    _,guarded,_,c=context(); out=Path(outdir); p=c.audit.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items(): require(c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"]); require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with guarded.no_neural():
        parent,records,data,metrics,old,six=load_parent(summaries)
        report,s=analyze(records,data,metrics,parent["validation_summary"],old,six)
    for n,v in zip(OUTPUTS,(manifest(),report,s),strict=True): require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==s,"summary reconstruction"); return p,report


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--summaries",nargs=40,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True); parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
