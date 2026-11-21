"""C264: frozen two-fact transfer after deleting an unqueried fact; no training."""
from __future__ import annotations
import argparse
from collections import defaultdict
from contextlib import contextmanager
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

EXPERIMENT_ID = "C264-v5b-frozen-two-fact-deletion"
STAGE = "V5-B-FROZEN-TWO-FACT-DELETION"
BASE = "5f6bd9ca1c3c318451f30b4d4c9858285b3d272b"
PARENT_EXECUTION = "abca8d7eb25146fca6f7404790071d1e6f0999d0"
PARENT_SHA = "1fcceab38de3e34a3858828285fd43503df9e455e2fdb3bd31524b5035813e21"
PARENT_ARTIFACTS = {
    "dataset.json": "3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56",
    "evaluations.pt": "1681c71811844655081ca5597b6dfbe1ab80fbdc5b5046b1f947b1bf51aefd89",
    "measurements.json": "9b8bab48074a91e1dd5f3c5d389598739b651bcadeed6ec49fbf7ec0c92631ee",
    "rate-plan.json": "ca53314f0e2ccda5bc7950f031c443ad70bb4e6c6c7181b53f8e7c0768199305",
    "trained-models.pt": "a63519b761bc876b8088fe14432018cd01024bfdecbcf1fca38a0515021dede9",
    "validation-summary.json": "e42f668ec6c2a01f573be92bbcd938f1d991e48cf02d242315d02d740d29066f",
}
SEEDS = tuple(range(263001,263006))
ARMS = ("standard_forward","standard_reverse","lower_forward","lower_reverse")
SUBSETS = ((0,1),(0,2),(1,2))
SPLITS = ("TRAIN","HOLDOUT")
VIEWS = ("normal","evidence_blind","query_blind")
KNOWN = ((0,1,2),(2,1,0))
TOL = 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c264_two_fact_deletion.py",
       "tests_lm/test_v05_c264_two_fact_deletion.py","tools/run_c264.ps1","tools/invoke_c264.ps1",
       "docs/experiment-ledger-addendum-c264-preregistration.md","docs/v5b-two-fact-deletion-v0.1.md")
OUTPUTS = {"deletion-plan.json","two-fact-dataset.json","provenance.json","eval-outputs.pt","measurements.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
DATA_SHA = "8adacd9b13b87c9f6a2bd7e1bf0f735e9a1a63b521840ef301a855586643e6c1"
MANIFEST_SHA = "a4cfef0b148d7f2130324127f51217d03c191bf788b87d07d52b1d67890095b1"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c263_learning_rate_order as parent
    _,c260,trainer,base,orders,aligned,reader,factory,audit = parent.context()
    return parent,c260,trainer,base,orders,aligned,reader,factory,audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        seeds=list(SEEDS),arms=list(ARMS),parameters=14256,dataset_sha256=DATA_SHA,
        changed="delete one unqueried fact; retain query,values,known names and frozen weights",
        rows=288,subsets=[list(x) for x in SUBSETS],provenance_edges=1728,parents_per_row=6,
        new_split="none; reduced prompts deduplicated across original TRAIN/HOLDOUT projections",
        primary="all twenty frozen states pass every two-fact cell and two-order group criterion",
        gate=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        model_forward_calls=600,row_presentations=120960,core_forward_calls=2400,
        forwards_per_model=30,rows_per_model=6048,new_forwards_per_model=6,batch=144,
        checkpoint_bundle_loads=1,model_state_loads=20,new_training_steps=0,new_checkpoint_writes=0,
        reference_archive_loads_per_pass=2,formal_analysis_passes=2,logit_payload_bytes=247726080,
        source_pins=430,protected_inputs=723,direct_dependencies=40,own_tests=24,
        modules=149,loaded_tests=3502,focused_tests=3501,excluded_test=EXCLUDED,
        dtype="CPU float64",threads=2,deterministic=True,replay_tolerance=TOL,network_calls=0,
        production_adoption=False,gate_f_candidate=False,learning_rate_benefit_claim=False,
        general_language_claim=False,arbitrary_length_claim=False)


def render(r,view="normal"):
    require(view in VIEWS and r["language"] in ("en","ja"),"view/language")
    names = ("a","b","c") if r["language"]=="en" else ("甲","乙","丙")
    values = dict(zip(r["entities"],r["values"],strict=True))
    return ";".join(names[i]+"="+("?" if view=="evidence_blind" else str(values[i])) for i in r["permutation"])+";"+("?" if view=="query_blind" else names[r["query"]])+"="


def dataset():
    rows=[]
    for entities in SUBSETS:
        for values in itertools.permutations(range(4),2):
            for language in ("en","ja"):
                for permutation in (entities,entities[::-1]):
                    for query in entities:
                        rid=":".join((language,"".join(map(str,entities)),"".join(map(str,values)),"".join(map(str,permutation)),str(query)))
                        r=dict(id=rid,entities=list(entities),values=list(values),language=language,
                               permutation=list(permutation),query=query,target=48+values[entities.index(query)])
                        r["prompt"]=render(r);rows.append(r)
    return rows


def validate_dataset(rows):
    require(rows==dataset() and digest(rows)==DATA_SHA,"two-fact dataset identity")
    require(len(rows)==len({r["prompt"] for r in rows})==len({r["id"] for r in rows})==288,"unique reduced rows")
    require(all(len(r["prompt"].encode())<=46 for r in rows),"no truncation")


def provenance(data,rows):
    validate_dataset(rows);lookup={r["prompt"]:r for r in rows};edges=defaultdict(list);sources=set()
    require(set(data)=={"original","extra"},"source stages")
    for stage in ("original","extra"):
        require(set(data[stage])==set(SPLITS),"source splits")
        for split in SPLITS:
            for old in data[stage][split]:
                key=stage+"/"+split+"/"+old["id"];require(key not in sources,"duplicate source");sources.add(key)
                permutation=KNOWN[old["order"]] if stage=="original" else tuple(old["permutation"])
                require(sorted(permutation)==[0,1,2] and len(set(old["assignment"]))==3,"source assignment")
                for removed in range(3):
                    if removed==old["query"]:continue
                    entities=[i for i in range(3) if i!=removed]
                    r=dict(entities=entities,values=[old["assignment"][i] for i in entities],
                           permutation=[i for i in permutation if i!=removed],language=old["language"],query=old["query"])
                    reduced=lookup[render(r)];require(reduced["target"]==old["target"],"deletion changed answer")
                    edges[reduced["id"]].append(dict(source=key,removed_entity=removed))
    require(len(sources)==864 and len(edges)==288 and all(len(v)==6 for v in edges.values()),"projection coverage")
    return [dict(row_id=r["id"],parents=sorted(edges[r["id"]],key=lambda x:x["source"])) for r in rows]


def check_logits(x,n):
    require(isinstance(x,torch.Tensor) and x.shape==(n,256) and x.dtype==torch.float64
            and x.device.type=="cpu" and bool(torch.isfinite(x).all()),"finite CPU float64 logits")


def replay_original(left,right):
    require(set(left)==set(right)=={"original","extra"},"replay stages");error=0.
    for stage,n in (("original",144),("extra",288)):
        require(set(left[stage])==set(right[stage])==set(SPLITS),"replay splits")
        for split in SPLITS:
            require(set(left[stage][split])==set(right[stage][split])==set(VIEWS),"replay views")
            for view in VIEWS:
                a,b=left[stage][split][view],right[stage][split][view];check_logits(a,n);check_logits(b,n)
                error=max(error,float((a-b).abs().max()))
                require(error<=TOL and torch.equal(a.argmax(-1),b.argmax(-1)),"raw/argmax replay")
    return error


def score(rows,raw):
    validate_dataset(rows);require(set(raw)==set(VIEWS),"new views")
    for x in raw.values():check_logits(x,288)
    preds={v:x.argmax(-1).tolist() for v,x in raw.items()}
    ok={v:[p==r["target"] for p,r in zip(preds[v],rows,strict=True)] for v in VIEWS}
    loss=F.cross_entropy(raw["normal"],torch.tensor([r["target"] for r in rows]),reduction="none")
    cells=[];consistency=[]
    for language in ("en","ja"):
        for entities in SUBSETS:
            for permutation in (entities,entities[::-1]):
                ids=[i for i,r in enumerate(rows) if (r["language"],tuple(r["entities"]),tuple(r["permutation"]))==(language,entities,permutation)]
                groups=defaultdict(list)
                for i in ids:groups[tuple(rows[i]["values"])].append(i)
                require(len(ids)==24 and len(groups)==12 and all(len(g)==2 for g in groups.values()),"cell counts")
                acc={v:sum(ok[v][i] for i in ids)/24 for v in VIEWS}
                qp=sum(all(ok["normal"][i] for i in g) for g in groups.values())/12
                ed,qd=acc["normal"]-acc["evidence_blind"],acc["normal"]-acc["query_blind"]
                cells.append(dict(language=language,entities=list(entities),permutation=list(permutation),rows=24,
                    correct=sum(ok["normal"][i] for i in ids),accuracy=acc["normal"],query_pair_accuracy=qp,
                    evidence_drop=ed,query_drop=qd,answer_nll=float(loss[ids].mean()),
                    passed=acc["normal"]>=.90 and qp>=.80 and ed>=.35 and qd>=.35))
            groups=defaultdict(list)
            for i,r in enumerate(rows):
                if (r["language"],tuple(r["entities"]))==(language,entities):groups[tuple(r["values"]),r["query"]].append(i)
            require(len(groups)==24 and all(len(g)==2 for g in groups.values()),"order group counts")
            count=sum(all(ok["normal"][i] for i in g) for g in groups.values())
            consistency.append(dict(language=language,entities=list(entities),groups=24,both_correct=count,accuracy=count/24,passed=count/24>=.80))
    return dict(cells=cells,two_order=consistency,correct=sum(ok["normal"]),rows=288,passed=all(c["passed"] for c in cells+consistency))


def evaluate_new(model,rows,factory):
    result={}
    with torch.no_grad():
        for view in VIEWS:
            outputs=[]
            for start in range(0,288,144):
                x=torch.stack([factory.prefix_tensor(render(r,view).encode()) for r in rows[start:start+144]])
                logits=model(x,torch.zeros(len(x),dtype=torch.int64));check_logits(logits,144);outputs.append(logits.detach().clone())
            result[view]=torch.cat(outputs)
    return result


def probe(model,ref,data,rows,c260,trainer,base,orders,factory):
    require(not any(m.training for m in model.modules()) and not any(p.requires_grad for p in model.parameters()),"frozen model")
    before=base.fingerprint(model);require(before==ref["final_sha256"] and sum(p.numel() for p in model.parameters())==14256,"final identity/capacity")
    counts=[0,0];cores,ch=c260.core_counter(model)
    def counted(module,args,output):counts[0]+=1;counts[1]+=len(args[0])
    hook=model.register_forward_hook(counted)
    try:
        anchor=trainer.evaluate(model,data["original"],data["extra"],base,orders,factory)
        ae=replay_original(anchor,ref["raw"]);require(base.fingerprint(model)==before,"anchor mutation")
        reduced=evaluate_new(model,rows,factory)
        restored=trainer.evaluate(model,data["original"],data["extra"],base,orders,factory)
        re=max(replay_original(restored,anchor),replay_original(restored,ref["raw"]))
    finally:
        hook.remove()
        if ch is not None:ch.remove()
    require(counts==[30,6048] and cores[0]==120,"probe workload")
    require(base.fingerprint(model)==before,"weight mutation")
    return dict(seed=ref["seed"],arm=ref["arm"],final_sha256=before,weights_preserved=True,
        model_forward_calls=30,row_presentations=6048,core_forward_calls=120,anchor_error=ae,restore_error=re,
        anchor=anchor,reduced=reduced,restored=restored)


def analyze(records,refs,rows):
    require([(r["seed"],r["arm"]) for r in records]==[(r["seed"],r["arm"]) for r in refs]==identities(),"record identities")
    measured=[];results=[]
    for r,ref in zip(records,refs,strict=True):
        require(r["weights_preserved"] is True and r["final_sha256"]==ref["final_sha256"],"saved state")
        require((r["model_forward_calls"],r["row_presentations"],r["core_forward_calls"])==(30,6048,120),"saved workload")
        for k in ("anchor_error","restore_error"):
            require(type(r[k]) in (int,float) and math.isfinite(r[k]) and 0<=r[k]<=TOL,"saved replay error")
        replay_original(r["anchor"],ref["raw"]);replay_original(r["restored"],r["anchor"]);replay_original(r["restored"],ref["raw"])
        m=score(rows,r["reduced"]);measured.append(dict(seed=r["seed"],arm=r["arm"],**m))
        results.append(dict(seed=r["seed"],arm=r["arm"],passed=m["passed"]))
    summary=dict(models=20,seed_results=results,seed_pass_counts={a:sum(r["passed"] for r in results if r["arm"]==a) for a in ARMS},
        joint_gate=all(r["passed"] for r in results),model_forward_calls=600,row_presentations=120960,core_forward_calls=2400,
        new_training_steps=0,new_checkpoint_writes=0,checkpoint_bundle_loads=1,model_state_loads=20,all_replays=True,all_weights_preserved=True)
    return measured,summary


@contextmanager
def no_model_calls():
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C264 saved verification forbids model calls")):
        yield


def check_parent(p,parent):
    parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS","accepted parent identity")
    require(p["validation_summary"]["seed_pass_counts"]=={a:5 for a in ARMS}
            and p["validation_summary"]["rate_joint_pass"]=={"standard":True,"lower":True},"accepted parent counts")
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifacts")


def load_reference(path):
    parent,*_,audit=context();path=Path(path).resolve();require(audit.sha(path)==PARENT_SHA,"parent summary hash")
    with no_model_calls():
        p,metrics=parent.verify_artifacts(path.parent,PARENT_EXECUTION)
    check_parent(p,parent);require(len(metrics)==20,"parent metric count")
    data=audit.read_json(path.parent/"dataset.json")
    v=torch.load(path.parent/"evaluations.pt",map_location="cpu",weights_only=True)
    require(set(v)=={"schema","records"} and v["schema"]=="fold-c263-rate-eval-v1","reference schema")
    require([(r["seed"],r["arm"]) for r in v["records"]]==identities(),"reference identities")
    return data,v["records"]


def validate_registration(source_count,input_count):
    actual=digest(manifest());print(f"registration_check = source_pins:{source_count}; protected_inputs:{input_count}; manifest_sha256:{actual}",flush=True)
    require((source_count,input_count)==(430,723),f"counts expected=(430,723) actual=({source_count},{input_count})")
    require(actual==MANIFEST_SHA,f"manifest expected={MANIFEST_SHA} actual={actual}");validate_dataset(dataset())


def precheck(path,root):
    parent,*_,factory,audit=context();path=Path(path).resolve();root=Path(root)
    require(audit.sha(path)==PARENT_SHA,"parent summary hash");p=audit.read_json(path);check_parent(p,parent)
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items():require(Path(name).is_file() and audit.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items():require(audit.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    for child,wanted in [(path,PARENT_SHA)]+[(audit.safe_child(path.parent,x["file"]),x["sha256"]) for x in p["artifacts"]]:
        key=str(child.resolve());require(key not in protected,"duplicate parent input");require(audit.sha(child)==wanted,"parent bytes");protected[key]=wanted
    for x in p["artifacts"]:require(audit.safe_child(path.parent,x["file"]).stat().st_size==x["serialized_bytes"],"parent size")
    for name in OWN:
        require(name not in pins,"OWN collision");pins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-3])_[^/]+)\.py"
    deps=set(factory.LM_SOURCES)|{n for n in p["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps)==40 and deps<=set(pins),"direct dependencies")
    protected.update(audit.protect_tree_files(root,pins));validate_registration(len(pins),len(protected));return pins,protected


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(430,723) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==6 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"output coverage")
    s=p["validation_summary"];results=s["seed_results"]
    require([(r["seed"],r["arm"]) for r in results]==identities() and all(type(r["passed"]) is bool for r in results),"result coverage")
    require(s["joint_gate"] is all(r["passed"] for r in results) and s["seed_pass_counts"]=={a:sum(r["passed"] for r in results if r["arm"]==a) for a in ARMS},"gate accounting")
    for k,v in dict(models=20,model_forward_calls=600,row_presentations=120960,core_forward_calls=2400,new_training_steps=0,new_checkpoint_writes=0,checkpoint_bundle_loads=1,model_state_loads=20).items():
        require(type(s[k]) is int and s[k]==v,"workload:"+k)
    require(s["all_replays"] is True and s["all_weights_preserved"] is True and p["status"]==("PASS" if s["joint_gate"] else "FAIL"),"status/integrity")
    require(all(p[k] is False for k in ("production_adoption","gate_f_candidate","learning_rate_benefit_claim","general_language_claim","arbitrary_length_claim")) and p["network_calls"]==0,"scope")


def regression_modules(root):
    names=context()[0].regression_modules(root);require(len(names)==len(set(names))==148,"parent modules")
    return names+["tests_lm.test_v05_c264_two_fact_deletion"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"test identities")
    kept=[t for t in tests if t.id()!=EXCLUDED];require((len(tests),len(kept))==(3502,3501),"suite counts")
    return unittest.TestSuite(kept)


def run(*,c263_summary,output_dir,expected_head):
    parent,c260,trainer,base,orders,aligned,reader,factory,audit=context();root=Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c263_summary,root);data,refs=load_reference(c263_summary);rows=dataset();links=provenance(data,rows)
    states=parent.load_bundle(Path(c263_summary).resolve().parent/"trained-models.pt");require(len(states)==20,"state count")
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);records=[]
    for ref,state in zip(refs,states,strict=True):
        model=base.make_model(factory.new_model(ref["seed"]),"aligned_precore_read",ref["seed"],aligned,reader)
        model.load_state_dict(state,strict=True);model.eval().requires_grad_(False)
        print(f'[C264] model={len(records)+1}/20 seed={ref["seed"]} arm={ref["arm"]}; frozen two-fact evaluation',flush=True)
        records.append(probe(model,ref,data,rows,c260,trainer,base,orders,factory))
    measurements,summary=analyze(records,refs,rows)
    torch.save(dict(schema="fold-c264-deletion-eval-v1",records=records),out/"eval-outputs.pt")
    for name,value in (("deletion-plan.json",manifest()),("two-fact-dataset.json",rows),("provenance.json",links),("measurements.json",measurements),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard();precheck(c263_summary,root)
    for name,wanted in protected.items():require(audit.sha(name)==wanted,"modified input")
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["joint_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,production_adoption=False,gate_f_candidate=False,
        learning_rate_benefit_claim=False,general_language_claim=False,arbitrary_length_claim=False,network_calls=0)
    validate_result(p);(out/"summary.json").write_bytes(blob(p));print("=== C264 RESULT ===",flush=True);print(blob(p).decode(),flush=True);return p


def verify_artifacts(output_dir,c263_summary,expected_head):
    audit=context()[-1];out=Path(output_dir);p=audit.read_json(out/"summary.json");validate_result(p);require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():require(audit.sha(name)==wanted,"postcheck input")
    for x in p["artifacts"]:
        child=audit.safe_child(out,x["file"]);require(audit.sha(child)==x["sha256"] and child.stat().st_size==x["serialized_bytes"],"output bytes")
    with no_model_calls():
        data,refs=load_reference(c263_summary);rows=audit.read_json(out/"two-fact-dataset.json")
        v=torch.load(out/"eval-outputs.pt",map_location="cpu",weights_only=True)
        require(set(v)=={"schema","records"} and v["schema"]=="fold-c264-deletion-eval-v1","evaluation schema")
        measurements,summary=analyze(v["records"],refs,rows)
        for name,value in (("deletion-plan.json",manifest()),("provenance.json",provenance(data,rows)),("measurements.json",measurements),("validation-summary.json",summary)):
            require(audit.read_json(out/name)==value,"persisted replay:"+name)
    require(p["validation_summary"]==summary,"saved summary");return p,measurements


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("c263-summary","output-dir"):p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))


if __name__=="__main__":
    main()
