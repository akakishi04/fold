"""C287: saved final-fit versus generalization partition; no neural execution."""
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

EXPERIMENT_ID = "C287-v5b-saved-fit-partition-audit"
STAGE = "V5-B-SAVED-FIT-PARTITION-AUDIT"
BASE = "6ce09f66e8ea61a9fbfffd1e2de38a9ba8cdef61"
PARENT_EXECUTION = "7fe7c72ff88e252b3087c9715674510dbba96651"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c286_cosine_tail_stability.py"
PARENT_BLOB = "332452219fe1a0b5472abb4a64be2827e6751b9f"
SUMMARY_SHAS = (
    "14bfe8920b80c86cc8e297864402c38c53a26c87085b8963cae363cb6fd98a9a",
    "702092926265bb893babce1e5b93dd234791527344193ea876d33210e8bfdba1",
    "83df761b835fa529d72ba1cee5fe618ddaff6936d9db56defc02957b90788c83",
    "609718db24ca6e3eda4f8916f04f56b24bff3621ddca4ebe136209617fad4949",
    "075cb7399f62d048310bdfb1c31c93ac39ab8b3dc400578d60e062ebfdacf3d1",
    "f56aca6895d5acd69b3c7e557c04fdb95b2b5e13a8b0bfe56f7c6ea4d5878ea7",
    "00410f3d879cb9571186e2ebf08a1ca9df0b31b64a639adae53f503c068bc7db",
    "a0019e06e4f4b330675daa2235cb4d0cf1952930336d2f0038f17d6ebd11b5bb",
    "557069bec9d0d6ef73c7a9d1f5196f7be70edb9ab2c37a9a0d315033678b770b",
    "ee4290a1fccd923b9308b1bcd344c3016c7ea90533b72836365139672d66ed13",
    "6b8263b45837ffef19767caab569c5511ea54c634ff2a3e38e8773c13a8a8e9f",
    "1c255b542a742c0fa02fb36ffdcdfd762eddfb284f2347112feb816f40183beb",
    "0c30db2011e8b6cbc5cdcc67dee85792abd0d058f9f54a86cc65b103d2cc24a0",
)
PARENT_ARTIFACTS = {
    "architecture-plan.json": ("3d0ecd3f4785967a88e8b84597d9615be79eb7e609c348bf2ca1cdead8cbe94e",3676),
    "dataset.json": ("1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",36024),
    "triple-dataset.json": ("432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",158236),
    "quad-dataset.json": ("86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b",172066),
    "trained-models.pt": ("f55a6fed1abb6a0c93053504a3f8a42c4110ded8328cde5e1a2c5d0e37b0d2ce",1238007),
    "evaluations.pt": ("408551ec07aa4ac5d5bd6978cd042657b96634a33cb34e3f3239bdc53cff9279",159563727),
    "measurements.json": ("40bfb616890304229ce1b581cc58d64d22b5bf8456a15d7d773db3672f5a1186",790540),
    "validation-summary.json": ("9ac20a5fe67a69bf3e6ebcadd3b948561d00cc98857c5f0bfb2cb68003b7d803",38210),
}
SEEDS = tuple(range(286001,286006))
ARMS = ("constant_lr","cosine_tail")
PROFILES = {"two_char":("doubled","shared_prefix","shared_suffix"),
            "triple":("tripled","shared_prefix2","shared_suffix2"),
            "quad":("quadrupled","shared_prefix3","shared_suffix3")}
THRESHOLDS = dict(accuracy=.90,query_pair_accuracy=.80,evidence_drop=.35,query_drop=.35,two_order_accuracy=.80)
WINDOWS = ((1,400),(401,600),(601,800))
OWN = ("fold_lm/v05_benchmarks/model_c287_saved_fit_partition_audit.py",
       "tests_lm/test_v05_c287_saved_fit_partition_audit.py","tools/run_c287.ps1","tools/invoke_c287.ps1",
       "docs/experiment-ledger-addendum-c287-preregistration.md","docs/v5b-saved-fit-partition-audit-v0.1.md")
OUTPUTS = ("audit-plan.json","fit-partition-report.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
ZERO_KEYS = ("model_forward_calls","row_presentations","core_forward_calls","train_steps","model_state_loads","new_checkpoint_writes","network_calls")
MANIFEST_SHA = "98e5768640301fd36d00706305809bd5b4707eb10458bee5abfaef478b1bf430"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c286_cosine_tail_stability as parent
    return parent,parent.context()[4]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
                parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,summary_sha256=list(SUMMARY_SHAS),
                parent_artifacts={k:list(v) for k,v in PARENT_ARTIFACTS.items()},seeds=list(SEEDS),arms=list(ARMS),
                profiles={k:list(v) for k,v in PROFILES.items()},thresholds=THRESHOLDS,windows=[list(w) for w in WINDOWS],
                question="where residual C286 error appears:optimized normal TRAIN,seen-length HOLDOUT,or untrained quad",
                loss_semantics="pre-update minibatch CE;stratify length/profile/windows;not final-dataset loss or checkpoint selection",
                final_semantics="row-weighted saved final answer_nll;direct gates separate from mask/full gates",
                fixed_records=3240,split_partitions=60,loss_bins=180,paired_loss_bins=90,
                source_pins=568,protected_inputs=1016,dependency_union=63,own_tests=32,
                modules=172,loaded_tests=4118,focused_tests=4117,excluded_test=EXCLUDED,
                capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,**dict.fromkeys(ZERO_KEYS,0))


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None,"manifest not sealed")
    require(digest(manifest())==MANIFEST_SHA,"manifest digest mismatch")


def expected_results():
    out=[]
    for s,a in identities():
        seen=s not in (286002,286003);quad=seen and not (s==286005 and a==ARMS[0])
        out.append(dict(seed=s,arm=a,two_char_pass=seen,triple_pass=seen,quad_pass=quad,passed=quad,all_tasks_pass=seen and quad))
    return out


def finite(x):
    require(type(x) in (int,float) and math.isfinite(x),"finite numeric metric")
    return float(x)


def grid(task,kind):
    out=set()
    for s,p,l,e in itertools.product(("TRAIN","HOLDOUT"),PROFILES[task],("en","ja"),((0,1),(0,2),(1,2))):
        for order in ((e,e[::-1]) if kind=="answer" else ((),)):
            out.add((s,p,l,e,order))
    return out


def key(r,kind):
    return (r["split"],r["profile"],r["language"],tuple(r["entities"]),tuple(r["permutation"]) if kind=="answer" else ())


def normalize_task(tm,task,seed,arm):
    records=[]
    for field,kind in (("cells","answer"),("two_order","order")):
        keys=[key(r,kind) for r in tm[field]]
        require(len(keys)==len(set(keys)) and set(keys)==grid(task,kind),"complete unique grid")
        for r in sorted(tm[field],key=lambda r:key(r,kind)):
            n=16 if r["split"]=="TRAIN" else 8
            acc=finite(r["accuracy"]);denom="rows" if kind=="answer" else "groups"
            count="correct" if kind=="answer" else "both_correct"
            require(type(r[denom]) is int and r[denom]==n and type(r[count]) is int
                    and 0<=r[count]<=n and abs(acc-r[count]/n)<=1e-12,"cell counts")
            values={k:finite(r[k]) for k in THRESHOLDS if k!="two_order_accuracy"} if kind=="answer" else {"two_order_accuracy":acc}
            if kind=="answer":
                require(type(r["pairs"]) is int and r["pairs"]==n//2 and finite(r["answer_nll"])>=0,"answer fields")
                qp=values["query_pair_accuracy"]*(n//2)
                require(0<=qp<=n//2 and abs(qp-round(qp))<=1e-12 and 2*qp<=r[count],"query pair ratio")
                require(type(r["collapsed_pairs"]) is int and 0<=r["collapsed_pairs"]<=n//2-round(qp),"collapse counts")
                for k in ("evidence_drop","query_drop"):
                    v=(acc-values[k])*n
                    require(0<=v<=n and abs(v-round(v))<=1e-12,"ablated count")
            failed=[k for k,v in values.items() if v<THRESHOLDS[k]]
            require(type(r["passed"]) is bool and r["passed"] is (not failed),"cell pass flag")
            direct=not bool(set(failed)&{"accuracy","query_pair_accuracy","two_order_accuracy"})
            records.append(dict(r,seed=seed,arm=arm,task=task,kind=kind,failed_criteria=failed,
                                direct_pass=direct,mask_only=kind=="answer" and direct and bool(failed)))
    require(type(tm["passed"]) is bool and tm["passed"] is all(r["passed"] for r in records),"task pass flag")
    return records


def partition(rows):
    answers=[r for r in rows if r["kind"]=="answer"];orders=[r for r in rows if r["kind"]=="order"]
    require(len(answers)==36 and len(orders)==18,"split coverage")
    n=sum(r["rows"] for r in answers)
    return dict(rows=n,correct=sum(r["correct"] for r in answers),pairs=sum(r["pairs"] for r in answers),
                collapsed_pairs=sum(r["collapsed_pairs"] for r in answers),
                final_normal_nll=math.fsum(r["rows"]*r["answer_nll"] for r in answers)/n,
                criterion_failures={k:sum(k in r["failed_criteria"] for r in rows) for k in THRESHOLDS},
                direct_pass=all(r["direct_pass"] for r in rows),full_pass=all(r["passed"] for r in rows),
                mask_only_cells=sum(r["mask_only"] for r in answers))


def loss_bins(fit_records):
    require([(r["seed"],r["arm"]) for r in fit_records]==identities(),"fit identities")
    bins=[];lookup={};traces={}
    for rec in fit_records:
        f=rec["fit"];losses=f["loss_history"]
        require(type(f["steps"]) is int and f["steps"]==800 and len(losses)==800,"loss length")
        require(all(finite(v)>=0 for v in losses) and f["last_ce"]==losses[-1],"loss values")
        require(re.fullmatch(r"[0-9a-f]{64}",f["step400_sha256"]) is not None,"midpoint fingerprint")
        traces[(rec["seed"],rec["arm"])]=f
        for lo,hi in WINDOWS:
            for length,profile in itertools.product(range(2),range(3)):
                ids=[s-1 for s in range(lo,hi+1) if ((s-1)//4)%2==length and ((s-1)//4)%3==profile]
                require(bool(ids),"empty loss stratum")
                vals=[float(losses[i]) for i in ids]
                row=dict(seed=rec["seed"],arm=rec["arm"],first_update=lo,last_update=hi,length=length+2,
                         profile_index=profile,updates=len(ids),mean_ce=math.fsum(vals)/len(vals),max_ce=max(vals),min_ce=min(vals))
                bins.append(row);lookup[(rec["seed"],rec["arm"],lo,length,profile)]=row
    paired=[]
    for seed in SEEDS:
        a,b=(traces[(seed,arm)] for arm in ARMS)
        require(a["step400_sha256"]==b["step400_sha256"] and a["loss_history"][:400]==b["loss_history"][:400],"common first400 prefix")
        for lo,hi in WINDOWS:
            for length,profile in itertools.product(range(2),range(3)):
                x,y=(lookup[(seed,arm,lo,length,profile)] for arm in ARMS)
                paired.append(dict(seed=seed,first_update=lo,last_update=hi,length=length+2,profile_index=profile,
                                   updates=x["updates"],candidate_minus_control_mean_ce=y["mean_ce"]-x["mean_ce"]))
    require(len(bins)==180 and len(paired)==90,"loss-bin inventory")
    return bins,paired


def analyze(metrics,fits):
    require([(m["seed"],m["arm"]) for m in metrics]==identities(),"metric identities")
    records=[];parts=[];models=[];results=[]
    for m in metrics:
        idx={};flags={}
        for task in PROFILES:
            rr=normalize_task(m[task],task,m["seed"],m["arm"]);records.extend(rr)
            flags[task+"_pass"]=m[task]["passed"]
            for split in ("TRAIN","HOLDOUT"):
                p=partition([r for r in rr if r["split"]==split]);idx[(task,split)]=p
                parts.append(dict(seed=m["seed"],arm=m["arm"],task=task,split=split,**p))
        fitted=all(idx[(t,"TRAIN")]["direct_pass"] for t in ("two_char","triple"))
        heldout=all(idx[(t,"HOLDOUT")]["direct_pass"] for t in ("two_char","triple"))
        novel=all(idx[("quad",s)]["direct_pass"] for s in ("TRAIN","HOLDOUT"))
        first="fitted_train" if not fitted else "seen_length_holdout" if not heldout else "quad" if not novel else "none"
        models.append(dict(seed=m["seed"],arm=m["arm"],fitted_train_direct_pass=fitted,
                           seen_length_holdout_direct_pass=heldout,quad_direct_pass=novel,first_direct_failure_partition=first))
        results.append(dict(seed=m["seed"],arm=m["arm"],passed=flags["quad_pass"],all_tasks_pass=all(flags.values()),**flags))
    bins,paired=loss_bins(fits)
    summary=dict(parent_results=results,fixed_records=len(records),split_partitions=parts,model_partitions=models,
                 loss_bins=bins,paired_loss_bins=paired,diagnostic_complete=True,capability_gate_applicable=False,**dict.fromkeys(ZERO_KEYS,0))
    report=dict(records=records,summary=summary,warning="partition labels are descriptive,not causal;pre-update minibatch losses are not final-dataset evaluation")
    return report,summary


@contextmanager
def no_neural():
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C287 forbids neural calls")), \
         patch.object(torch.nn.Module,"load_state_dict",side_effect=RuntimeError("C287 forbids state loading")), \
         patch.object(torch,"save",side_effect=RuntimeError("C287 forbids checkpoint writes")):
        yield


def validate_parent(p):
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL" and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity/source")
    actual={a["file"]:(a["sha256"],a["serialized_bytes"]) for a in p["artifacts"]}
    require(len(p["artifacts"])==8 and actual==PARENT_ARTIFACTS,"parent artifacts")
    s=p["validation_summary"]
    require(s["seed_results"]==expected_results() and s["candidate_gate"] is False
            and all(s[k] is True for k in ("all_replays","all_pairs_matched","all_prefixes_matched")),"parent gates/prefix")


def load_parent(paths):
    parent,c=context();paths=[Path(p).resolve() for p in paths]
    require(len(paths)==13 and all(c.audit.sha(p)==s for p,s in zip(paths,SUMMARY_SHAS,strict=True)),"parent hashes")
    with no_neural():
        payload,metrics=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION)
        parent.validate_result(payload);validate_parent(payload)
        archive=torch.load(paths[0].parent/"evaluations.pt",map_location="cpu",weights_only=True)
    require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c286-cosine-tail-eval-v1","fit archive schema")
    fits=[dict(seed=r["seed"],arm=r["arm"],fit=r["fit"]) for r in archive["records"]]
    require([(r["seed"],r["arm"]) for r in fits]==identities(),"all fit records")
    return payload,metrics,fits


def precheck(paths,root):
    validate_seal();payload,_,_=load_parent(paths);_,c=context();root=Path(root);p=Path(paths[0]).resolve()
    pins,protected=dict(payload["source_blobs"]),dict(payload["input_sha256"])
    for n,w in pins.items(): require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==w,"changed source:"+n)
    for n,w in protected.items(): require(Path(n).is_file() and c.audit.sha(n)==w,"changed input:"+n)
    for child,w in [(p,SUMMARY_SHAS[0])]+[(c.audit.safe_child(p.parent,n),v[0]) for n,v in PARENT_ARTIFACTS.items()]:
        require(str(child.resolve()) not in protected and c.audit.sha(child)==w,"parent input")
        protected[str(child.resolve())]=w
    for n in OWN:
        require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9]|27[0-9]|28[0-6])_[^/]+)\.py"
    deps=set(c.factory.LM_SOURCES)|{n for n in payload["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps)==manifest()["dependency_union"] and deps<=set(pins),"dependency coverage")
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(568,1016),"registration counts")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS" and p["diagnostic_execution_valid"] is True,"result identity")
    require(all(p[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")),"result scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(568,1016) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"result protection")
    require(len(p["artifacts"])==3 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"output set")
    s=p["validation_summary"]
    require(s["parent_results"]==expected_results() and s["fixed_records"]==3240,"parent reconstruction")
    require((len(s["split_partitions"]),len(s["model_partitions"]),len(s["loss_bins"]),len(s["paired_loss_bins"]))==(60,10,180,90),"report inventory")
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False,"diagnostic scope")
    for k in ZERO_KEYS: require(type(s[k]) is int and s[k]==0,"zero workload:"+k)


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names=context()[0].regression_modules(root)
    require(len(names)==len(set(names))==manifest()["modules"]-1,"parent modules")
    return names+["tests_lm.test_v05_c287_saved_fit_partition_audit"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==manifest()["loaded_tests"] and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED];require(len(kept)==manifest()["focused_tests"],"focused suite")
    return unittest.TestSuite(kept)


def guard(root,head):
    _,c=context()
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    root=Path(__file__).resolve().parents[2];_,c=context();guard(root,expected_head)
    pins,protected=precheck(summaries,root)
    with no_neural():
        payload,metrics,fits=load_parent(summaries);report,summary=analyze(metrics,fits)
    require(summary["parent_results"]==payload["validation_summary"]["seed_results"],"parent reconstructed flags")
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for n,v in zip(OUTPUTS,(manifest(),report,summary),strict=True): (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head);precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
           source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
           capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(p);(out/"summary.json").write_bytes(blob(p))
    print("=== C287 RESULT ===",flush=True);print(blob(p).decode(),flush=True);return p


def verify_artifacts(outdir,summaries,expected_head):
    _,c=context();out=Path(outdir);p=c.audit.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,w in p["input_sha256"].items(): require(c.audit.sha(n)==w,"protected input")
    for a in p["artifacts"]:
        child=c.audit.safe_child(out,a["file"])
        require(c.audit.sha(child)==a["sha256"] and child.stat().st_size==a["serialized_bytes"],"output bytes")
    with no_neural():
        _,metrics,fits=load_parent(summaries);report,summary=analyze(metrics,fits)
    for n,v in zip(OUTPUTS,(manifest(),report,summary),strict=True): require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==summary,"summary reconstruction");return p,report


def main():
    p=argparse.ArgumentParser();p.add_argument("--summaries",nargs=13,type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True);p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__=="__main__": main()
