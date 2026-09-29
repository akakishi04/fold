"""C283: frozen four-character transfer of every C282 state; no new training."""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import math
import re
import unittest
from pathlib import Path
from unittest.mock import patch
import torch

EXPERIMENT_ID = "C283-v5b-frozen-four-character-transfer"
STAGE = "V5-B-FROZEN-FOUR-CHARACTER-TRANSFER"
BASE = "b597180933fcc464395ad62cc0e915e01c796871"
PARENT_EXECUTION = "aef5aecfc438679641e59b337d7a9eb615c619a3"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c282_mixed_length_training.py"
PARENT_BLOB = "fdf35a6c0c18e0c0da4b1f592cef73be156de481"
SUMMARY_SHAS = (
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
    "architecture-plan.json": ("291ed152bec43b222e54851c5e4699776e220d60937a733599c37f617ed400de", 3281),
    "dataset.json": ("1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1", 36024),
    "triple-dataset.json": ("432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73", 158236),
    "trained-models.pt": ("8cadcfb73017fad6f82d86ba37a365cdf40ce3adcb304a531b34533300164cce", 1238007),
    "evaluations.pt": ("b0816dc5a82a200f5e2537321df491e1802fd01177b55ffbc46cf0daf08d4267", 106287783),
    "measurements.json": ("a92b92881f0ffc7c7b6a6286c7e0237d469e35f5d532269b48a34d0ee96255fd", 524693),
    "validation-summary.json": ("27d4db76f97b24941e3c88dc95a9453fe51e1521a340447d0bbe44c609369af7", 19584),
}
SEEDS = tuple(range(282001, 282006))
ARMS = ("two_char_only", "mixed_length")
PROFILE_MAP = dict(quadrupled="tripled", shared_prefix3="shared_prefix2", shared_suffix3="shared_suffix2")
SPLITS = ("TRAIN", "HOLDOUT")
VIEWS = ("normal", "evidence_blind", "query_blind")
OWN = ("fold_lm/v05_benchmarks/model_c283_frozen_four_character_transfer.py",
       "tests_lm/test_v05_c283_frozen_four_character_transfer.py", "tools/run_c283.ps1", "tools/invoke_c283.ps1",
       "docs/experiment-ledger-addendum-c283-preregistration.md", "docs/v5b-frozen-four-character-transfer-v0.1.md")
OUTPUTS = ("transfer-plan.json", "quad-dataset.json", "eval-outputs.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10, model_forward_calls=1350, row_presentations=129600, core_forward_calls=5400,
            checkpoint_bundle_loads=1, model_state_loads=10, train_steps=0, new_checkpoint_writes=0, network_calls=0)
TOL = 1e-9
QUAD_SHA = "86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b"
MANIFEST_SHA = "e88244fe1acc677d629e3b0400dc4926be9b26560c05a782122ae1e5042213a4"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS, ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c282_mixed_length_training as parent
    return parent, parent.context()


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION, parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
                summary_sha256=list(SUMMARY_SHAS), parent_artifacts={k:list(v) for k,v in PARENT_ARTIFACTS.items()},
                seeds=list(SEEDS), arms=list(ARMS), profile_adapter=PROFILE_MAP, quad_dataset_sha256=QUAD_SHA,
                parameters=14256, max_tokens=48, max_prompt_bytes=43, novel_normal_rows_per_model=864,
                changed="frozen evaluation length only: four-character identifiers unseen by both C282 arms",
                order="original two+three anchor -> four-character probe -> original two+three restore",
                per_model=[135,12960,540], raw_logit_payload_bytes=265420800,
                primary="all five frozen mixed_length states pass every four-character fixed criterion; control separate",
                interpretation="bounded transfer only; all seeds included; does not repair C282 or isolate diversity from maximum training length",
                gate=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
                source_pins=544, protected_inputs=964, dependency_union=59, own_tests=32,
                modules=168, loaded_tests=3982, focused_tests=3981, excluded_test=EXCLUDED,
                dtype="CPU float64", threads=2, deterministic=True, replay_tolerance=TOL,
                gate_f_candidate=False, production_adoption=False, arbitrary_length_claim=False, **WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None, "manifest not sealed")
    require(digest(manifest()) == MANIFEST_SHA, "manifest digest mismatch")


def names(row, profile):
    require(profile in PROFILE_MAP and row["language"] in ("en","ja"), "profile/language")
    chars = ("a","b","c") if row["language"] == "en" else ("甲","乙","丙")
    i,j = row["entities"]; u,v = chars[i],chars[j]
    return {i:u*4, j:v*4 if profile == "quadrupled" else u*3+v if profile == "shared_prefix3" else v+u*3}


def render(row, profile, view="normal"):
    require(view in VIEWS, "view")
    ns = names(row,profile); values = dict(zip(row["entities"],row["values"],strict=True))
    return ";".join(ns[k]+"="+("?" if view == "evidence_blind" else str(values[k])) for k in row["permutation"]) + ";" + ("?" if view == "query_blind" else ns[row["query"]]) + "="


def dataset(data):
    return {s:{p:[dict(source_id=r["id"], target=r["target"], views={v:render(r,p,v) for v in VIEWS})
                   for r in data[s]] for p in PROFILE_MAP} for s in SPLITS}


def validate_dataset(quad, data, c):
    c.p267.validate_data(data)
    require(quad == dataset(data) and digest(quad) == QUAD_SHA, "quad dataset identity")
    old = [renderer(r,p,v) for renderer,profiles in ((c.p267.render,c.p267.PROFILES),(c.c270.render,c.c270.PROFILES))
           for s in SPLITS for r in data[s] for p in profiles for v in VIEWS]
    old_bytes = set().union(*(set(x.encode()) for x in old))
    normal = []
    for s,p in itertools.product(SPLITS,PROFILE_MAP):
        for r,item in zip(data[s],quad[s][p],strict=True):
            require(all(len(n)==4 for n in names(r,p).values()), "four characters")
            for text in item["views"].values():
                require(len(text.encode()) <= 43 and set(text.encode()) <= old_bytes, "context overflow/new byte")
            normal.append(item["views"]["normal"])
    require(len(normal)==len(set(normal))==864 and not set(normal)&set(old), "novel unique normal prompts")


def score_quad(data, raw, c):
    require(set(raw)==set(SPLITS) and all(set(raw[s])==set(PROFILE_MAP) for s in SPLITS), "quad raw profiles")
    adapted = {s:{old:raw[s][new] for new,old in PROFILE_MAP.items()} for s in SPLITS}
    result = copy.deepcopy(c.c270.score(data,adapted,c.p267))
    reverse = {v:k for k,v in PROFILE_MAP.items()}
    for field in ("cells","two_order","totals"):
        for r in result[field]:
            require(r["profile"] in reverse, "scorer profile")
            r["profile"] = reverse[r["profile"]]
    return result


def evaluate_quad(model, quad, data, c):
    model.eval(); raw = {}
    with torch.no_grad():
        for s in SPLITS:
            raw[s] = {}
            for p in PROFILE_MAP:
                raw[s][p] = {}
                for v in VIEWS:
                    chunks = []
                    for start in range(0,len(data[s]),96):
                        x = torch.stack([c.factory.prefix_tensor(r["views"][v].encode()) for r in quad[s][p][start:start+96]])
                        require(x.shape==(min(96,len(data[s])-start),48), "unchanged context")
                        y = model(x,torch.zeros(len(x),dtype=torch.int64))
                        c.p267.check_logits(y,len(x)); chunks.append(y.detach().clone())
                    raw[s][p][v] = torch.cat(chunks)
    return raw


def evaluate_anchor(model,data,prompts,c):
    return dict(two_char=c.p267.evaluate(model,data,c.factory),
                triple=c.c270.evaluate_new(model,prompts,data,c.factory,c.p267))


def anchor_error(anchor, ref, data, c):
    require(set(anchor)=={"two_char","triple"}, "anchor tasks")
    return max(c.c270.replay_old(anchor["two_char"],ref["raw_two"],data,c.p267),
               c.previous.replay_triple(anchor["triple"],ref["raw_triple"],data,c.p267))


def frozen_probe(model,ref,data,prompts,quad,c):
    require(not any(m.training for m in model.modules()) and not any(p.requires_grad for p in model.parameters()), "frozen model")
    before = c.base.fingerprint(model)
    require(before==ref["final_sha256"] and sum(p.numel() for p in model.parameters())==14256, "parent state")
    with c.p267.counted(model,c.core) as (calls,cores):
        anchor = evaluate_anchor(model,data,prompts,c)
        ae = anchor_error(anchor,ref,data,c)
        novel = evaluate_quad(model,quad,data,c)
        restored = evaluate_anchor(model,data,prompts,c)
        recheck = anchor_error(restored,ref,data,c)
    require(calls==[135,12960] and cores[0]==540, "probe workload")
    require(c.base.fingerprint(model)==before, "weight mutation")
    return dict(seed=ref["seed"],arm=ref["arm"],final_sha256=before,weights_preserved=True,
                model_forward_calls=135,row_presentations=12960,core_forward_calls=540,
                anchor_error=ae,restore_error=recheck,anchor=anchor,novel=novel,restored=restored)


def analyze(records,refs,data,c):
    require([(r["seed"],r["arm"]) for r in records]==[(r["seed"],r["arm"]) for r in refs]==identities(), "model identities")
    metrics,results,contrasts = [],[],[]
    for r,ref in zip(records,refs,strict=True):
        require(r["weights_preserved"] is True and r["final_sha256"]==ref["final_sha256"], "saved state")
        require(tuple(r[k] for k in ("model_forward_calls","row_presentations","core_forward_calls"))==(135,12960,540), "saved workload")
        for k in ("anchor_error","restore_error"):
            require(type(r[k]) in (int,float) and math.isfinite(r[k]) and 0<=r[k]<=TOL, "replay bound")
        anchor_error(r["anchor"],ref,data,c); anchor_error(r["restored"],ref,data,c)
        scored = score_quad(data,r["novel"],c)
        require(type(scored["passed"]) is bool, "quad gate type")
        metrics.append(dict(seed=r["seed"],arm=r["arm"],**scored))
        results.append(dict(seed=r["seed"],arm=r["arm"],passed=scored["passed"]))
    for i in range(0,10,2):
        for a,b in zip(metrics[i]["totals"],metrics[i+1]["totals"],strict=True):
            require(all(a[k]==b[k] for k in ("split","profile","language","rows","pairs")), "contrast identity")
            contrasts.append(dict(seed=metrics[i]["seed"],**{k:a[k] for k in ("split","profile","language","rows","pairs")},
                                  control_correct=a["correct"],candidate_correct=b["correct"],
                                  control_collapsed=a["collapsed_pairs"],candidate_collapsed=b["collapsed_pairs"]))
    require(len(contrasts)==60, "contrasts")
    summary = dict(seed_results=results,seed_pass_counts={a:sum(r["passed"] for r in results if r["arm"]==a) for a in ARMS},
                   candidate_gate=all(r["passed"] for r in results if r["arm"]==ARMS[1]),contrasts=contrasts,
                   all_replays=True,all_weights_preserved=True,**WORK)
    return metrics,summary


def load_parent(paths):
    parent,c = context(); paths = [Path(p).resolve() for p in paths]
    require(len(paths)==9 and all(c.audit.sha(p)==s for p,s in zip(paths,SUMMARY_SHAS,strict=True)), "parent summary hashes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C283 parent forbids neural calls")), \
         patch.object(torch.nn.Module,"load_state_dict",side_effect=RuntimeError("C283 parent forbids state loading")), \
         patch.object(torch,"save",side_effect=RuntimeError("C283 parent forbids writes")):
        payload,_ = parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION)
    parent.validate_result(payload)
    require(payload["commit_sha"]==PARENT_EXECUTION and payload["status"]=="FAIL" and payload["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB, "parent identity/source")
    actual = {a["file"]:(a["sha256"],a["serialized_bytes"]) for a in payload["artifacts"]}
    require(len(payload["artifacts"])==7 and actual==PARENT_ARTIFACTS, "parent artifacts")
    s = payload["validation_summary"]
    require(s["candidate_gate"] is False and s["all_pairs_matched"] is True and s["all_replays"] is True, "parent validity")
    require(s["seed_pass_counts"]=={ARMS[0]:0,ARMS[1]:4} and s["two_char_pass_counts"]==dict.fromkeys(ARMS,4)
            and s["triple_pass_counts"]=={ARMS[0]:0,ARMS[1]:4}, "parent gates")
    archive = torch.load(paths[0].parent/"evaluations.pt",map_location="cpu",weights_only=True)
    require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c282-mixed-length-eval-v1", "parent eval schema")
    refs = [{k:r[k] for k in ("seed","arm","final_sha256","raw_two","raw_triple")} for r in archive["records"]]
    require([(r["seed"],r["arm"]) for r in refs]==identities(), "all parent states")
    data = c.audit.read_json(paths[0].parent/"dataset.json")
    prompts = c.audit.read_json(paths[0].parent/"triple-dataset.json")
    c.p267.validate_data(data); c.c270.validate_dataset(prompts,data,c.p267)
    return payload,refs,data,prompts


def precheck(paths,root):
    validate_seal(); payload,_,data,_ = load_parent(paths)
    _,c = context(); root,p = Path(root),Path(paths[0]).resolve()
    pins,protected = dict(payload["source_blobs"]),dict(payload["input_sha256"])
    for n,w in pins.items():
        require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==w,"changed source:"+n)
    for n,w in protected.items():
        require(Path(n).is_file() and c.audit.sha(n)==w,"changed input:"+n)
    for child,w in [(p,SUMMARY_SHAS[0])]+[(c.audit.safe_child(p.parent,n),v[0]) for n,v in PARENT_ARTIFACTS.items()]:
        require(str(child.resolve()) not in protected and c.audit.sha(child)==w,"parent input")
        protected[str(child.resolve())]=w
    for n in OWN:
        require(n not in pins,"OWN collision"); pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9]|27[0-9]|28[0-2])_[^/]+)\.py"
    deps=set(c.factory.LM_SOURCES)|{n for n in payload["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps)==manifest()["dependency_union"] and deps<=set(pins),"dependency coverage")
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(544,964),"protection cardinality")
    validate_dataset(dataset(data),data,c)
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"identity")
    require(all(p[k] is False for k in ("gate_f_candidate","production_adoption","arbitrary_length_claim")),"scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(544,964) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"result protection")
    require(len(p["artifacts"])==5 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"]; rr=s["seed_results"]
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"workload")
    require([(r["seed"],r["arm"]) for r in rr]==identities() and all(type(r["passed"]) is bool for r in rr),"results")
    require(s["seed_pass_counts"]=={a:sum(r["passed"] for r in rr if r["arm"]==a) for a in ARMS},"pass counts")
    gate=all(r["passed"] for r in rr if r["arm"]==ARMS[1])
    require(s["candidate_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"quad candidate gate")
    require(s["all_replays"] is True and s["all_weights_preserved"] is True and len(s["contrasts"])==60,"replay")


def flatten(suite):
    for x in suite:
        if isinstance(x,unittest.TestSuite): yield from flatten(x)
        else: yield x


def regression_modules(root):
    names=context()[0].regression_modules(root)
    require(len(names)==len(set(names))==manifest()["modules"]-1,"parent modules")
    return names+["tests_lm.test_v05_c283_frozen_four_character_transfer"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==manifest()["loaded_tests"] and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED]
    require(len(kept)==manifest()["focused_tests"],"focused suite")
    return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head
            and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    parent,c=context(); root=Path(__file__).resolve().parents[2]
    guard(root,expected_head,c); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected=precheck(summaries,root)
    _,refs,data,prompts=load_parent(summaries); quad=dataset(data); validate_dataset(quad,data,c)
    states=parent.load_bundle(Path(summaries[0]).resolve().parent/"trained-models.pt")
    require(len(states)==10,"all checkpoint states")
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False); records=[]
    for i,seed in enumerate(SEEDS):
        models=parent.make_models(seed,c)
        for j,arm in enumerate(ARMS):
            k=2*i+j; model=models[arm]; model.load_state_dict(states[k],strict=True); model.eval(); model.requires_grad_(False)
            print(f"[C283] frozen model={k+1}/10 seed={seed} arm={arm}",flush=True)
            records.append(frozen_probe(model,refs[k],data,prompts,quad,c))
    metrics,summary=analyze(records,refs,data,c)
    torch.save(dict(schema="fold-c283-four-character-eval-v1",records=records),out/"eval-outputs.pt")
    for n,v in (("transfer-plan.json",manifest()),("quad-dataset.json",quad),("measurements.json",metrics),("validation-summary.json",summary)):
        (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c); precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
           diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
           validation_summary=summary,gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    print("=== C283 RESULT ===",flush=True); print(blob(p).decode(),flush=True); return p


def verify_artifacts(outdir,summaries,expected_head):
    _,c=context(); out=Path(outdir); p=c.audit.read_json(out/"summary.json")
    validate_result(p); require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,w in p["input_sha256"].items(): require(c.audit.sha(n)==w,"protected input")
    for a in p["artifacts"]:
        child=c.audit.safe_child(out,a["file"])
        require(c.audit.sha(child)==a["sha256"] and child.stat().st_size==a["serialized_bytes"],"output bytes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C283 postcheck forbids neural calls")):
        _,refs,data,_=load_parent(summaries)
        quad=c.audit.read_json(out/"quad-dataset.json"); validate_dataset(quad,data,c)
        archive=torch.load(out/"eval-outputs.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c283-four-character-eval-v1","eval schema")
        metrics,summary=analyze(archive["records"],refs,data,c)
        for n,v in (("transfer-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):
            require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==summary,"summary reconstruction"); return p,metrics


def main():
    p=argparse.ArgumentParser(); p.add_argument("--summaries",nargs=9,type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True); p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__=="__main__": main()
