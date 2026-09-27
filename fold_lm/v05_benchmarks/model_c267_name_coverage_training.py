"""C267: paired name-coverage training on a new, explicitly disjoint two-fact split."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager
import copy
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

EXPERIMENT_ID = "C267-v5b-paired-name-coverage-training"
STAGE = "V5-B-PAIRED-NAME-COVERAGE-TRAINING"
BASE = "38272da75661b1f2f028719b41aa4406ee6dd26b"
PARENT_EXECUTION = "b377042dcdb903a308da131feb135b0f5362d9de"
PARENT_SHA = "5d9c79306aae5fb2fd39a82fae645a1447029cae3aedfb2bf92e953bb2435247"
PARENT_ARTIFACTS = {
    "audit-plan.json": "85be4d973b9f8ce8a59e1ffa9028faceb1de3fcc8d8b3035264c2af72ed88b3e",
    "pair-attribution.json": "038dd3a9aecc86aadcd2f99a8269103a579a3aa7787ac0bc8983e37dba082e90",
    "cells.json": "2c593908456838ff582c51632106f1a21af5082d081b1647fa6a6d6efbf85357",
    "profile-summary.json": "6a33a496099a60aeb2d7715338d7c2f5caecb9cec51c0f3cff92f696f3d581d4",
    "matched-contrasts.json": "a685b34f814b16295dae958d87dd0b23b405b8d4065e512af8262dc66d7d7bf2",
    "validation-summary.json": "17f9a7895fc2d208d1bdb2a463c3455a78aa7aeb53698ab91952c4d7d963f12f",
}
SEEDS = tuple(range(267001, 267006))
ARMS = ("doubled_only", "mixed_names")
PROFILES = ("doubled", "shared_prefix", "shared_suffix")
SPLITS = ("TRAIN", "HOLDOUT")
VIEWS = ("normal", "evidence_blind", "query_blind")
SUBSETS = ((0, 1), (0, 2), (1, 2))
HOLDOUT_VALUES = ((0, 2), (1, 3), (2, 0), (3, 1))
STEPS, BATCH, EVAL_BATCH, TOL = 800, 48, 96, 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c267_name_coverage_training.py",
       "tests_lm/test_v05_c267_name_coverage_training.py", "tools/run_c267.ps1", "tools/invoke_c267.ps1",
       "docs/experiment-ledger-addendum-c267-preregistration.md", "docs/v5b-name-coverage-training-v0.1.md")
OUTPUTS = ("coverage-plan.json", "dataset.json", "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
MANIFEST_SHA = "4f83a11bd6b2c31d7f1bd23b617772d1eab413e5099d5aafe3c4a34eb453f2d7"


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
    from fold_lm.v05_benchmarks import model_c266_query_pair_audit as parent
    names, task, audit = parent.context()
    _, _, core, base, aligned, reader, factory, _ = names.context()
    return parent, core, base, aligned, reader, factory, audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        seeds=list(SEEDS), arms=list(ARMS), profiles=list(PROFILES), dataset_sha256=DATA_SHA,
        holdout_values=[list(x) for x in HOLDOUT_VALUES], train_rows=192, holdout_rows=96,
        changed="training name coverage only within fresh matched pairs; no accepted weights reused",
        split="new two-fact value split; HOLDOUT differences=2 mod4; TRAIN other distinct pairs",
        parameters=14256, steps=800, batch=48, lr=.005, optimizer="AdamW",
        betas=[.9,.999], eps=1e-8, weight_decay=0., clip=1.,
        schedule="epoch=step//4; same randperm192 seed+267000+epoch; profile0 versus epoch%3",
        profile_updates=dict(doubled_only=[800,0,0], mixed_names=[268,268,264]),
        fit_rng="seed+268000 reset per arm", dtype="CPU float64", threads=2,
        primary="all five mixed_names seeds pass both splits and all profiles; controls separate",
        gate=dict(accuracy=.90, query_pair=.80, evidence_drop=.35, query_drop=.35, two_order=.80),
        models=10, train_steps=8000, training_rows=384000, model_forward_calls=8540,
        row_presentations=435840, core_forward_calls=34160, evaluation_forwards=540,
        checkpoint_bundle_loads=1, model_state_loads=10, new_checkpoint_writes=1,
        source_pins=448, protected_inputs=761, direct_dependencies=43, own_tests=24,
        modules=152, loaded_tests=3574, focused_tests=3573, excluded_test=EXCLUDED,
        logit_payload_bytes=53084160, replay_tolerance=TOL, network_calls=0,
        gate_f_candidate=False, production_adoption=False, unseen_name_transfer_claim=False,
        causal_parser_claim=False, naming_benefit_claim=False)


def render(row, profile, view="normal"):
    require(profile in PROFILES and view in VIEWS, "profile/view")
    chars = ("a", "b", "c") if row["language"] == "en" else ("甲", "乙", "丙")
    i, j = row["entities"]; u, v = chars[i], chars[j]
    names = {i: u+u, j: v+v if profile == "doubled" else u+v if profile == "shared_prefix" else v+u}
    values = dict(zip(row["entities"], row["values"], strict=True))
    return ";".join(names[k]+"="+("?" if view == "evidence_blind" else str(values[k])) for k in row["permutation"]) + ";" + ("?" if view == "query_blind" else names[row["query"]]) + "="


def dataset():
    result = {s: [] for s in SPLITS}
    for entities, values, lang in itertools.product(SUBSETS, itertools.permutations(range(4), 2), ("en", "ja")):
        split = "HOLDOUT" if values in HOLDOUT_VALUES else "TRAIN"
        for perm, query in itertools.product((entities, entities[::-1]), entities):
            result[split].append(dict(id=f"{lang}:{entities}:{values}:{perm}:{query}", entities=list(entities),
                values=list(values), language=lang, permutation=list(perm), query=query,
                target=48+values[entities.index(query)]))
    return result


def validate_data(data):
    require(data == dataset() and digest(data) == DATA_SHA, "dataset identity")
    require([len(data[s]) for s in SPLITS] == [192,96], "split sizes")
    require(not ({tuple(r["values"]) for r in data["TRAIN"]} & {tuple(r["values"]) for r in data["HOLDOUT"]}), "value leakage")
    for rows in data.values():
        for r in rows:
            lengths = [len(render(r,p).encode()) for p in PROFILES]
            require(len(set(lengths)) == 1 and max(lengths) <= 46, "matched lengths")


def training_tables(data, factory):
    rows = data["TRAIN"]
    require(rows == dataset()["TRAIN"], "TRAIN-only rows")
    tokens = torch.stack([torch.stack([factory.prefix_tensor(render(r,p).encode()) for r in rows]) for p in PROFILES])
    targets = torch.tensor([r["target"] for r in rows], dtype=torch.int64)
    require(tokens.shape == (3,192,48) and tokens.dtype == torch.int64, "training tokens")
    return tokens, targets


def schedule(seed, arm, steps=STEPS):
    require(seed in SEEDS and arm in ARMS and type(steps) is int and 0 < steps <= STEPS, "schedule identity")
    ids, profiles = [], []
    for step in range(steps):
        epoch, block = divmod(step,4)
        g = torch.Generator(device="cpu").manual_seed(seed+267000+epoch)
        ids.append(torch.randperm(192,generator=g)[block*48:(block+1)*48])
        profiles.append(0 if arm == "doubled_only" else epoch % 3)
    indices = torch.stack(ids)
    return indices, profiles, dict(logical_batch_sha256=digest(indices.tolist()),
        row_exposures=torch.bincount(indices.flatten(),minlength=192).tolist(),
        profile_updates=[profiles.count(i) for i in range(3)])


def fit(model, tokens, targets, seed, arm):
    require(tokens.shape == (3,192,48) and targets.shape == (192,), "fit tables")
    indices, profiles, plan = schedule(seed,arm,STEPS)
    torch.manual_seed(seed+268000)
    opt = torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    model.train()
    for step in range(STEPS):
        opt.zero_grad(set_to_none=True)
        loss = F.cross_entropy(model(tokens[profiles[step],indices[step]],torch.zeros(48,dtype=torch.int64)), targets[indices[step]])
        require(bool(torch.isfinite(loss)), "nonfinite loss")
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True); opt.step()
        if (step+1) % 200 == 0:
            print(f"[C267] seed={seed} arm={arm} step={step+1}/800 answer_nll={float(loss.detach()):.6f}",flush=True)
    model.eval()
    return dict(steps=STEPS, training_rows=STEPS*48, last_loss=float(loss.detach()), **plan)


def check_logits(x,n):
    require(isinstance(x,torch.Tensor) and x.shape == (n,256) and x.dtype == torch.float64 and x.device.type == "cpu" and bool(torch.isfinite(x).all()), "finite logits")


def evaluate(model, data, factory):
    model.eval(); raw = {}
    with torch.no_grad():
        for split in SPLITS:
            rows = data[split]
            raw[split] = {}
            for profile in PROFILES:
                raw[split][profile] = {}
                for view in VIEWS:
                    chunks = []
                    for start in range(0,len(rows),96):
                        x = torch.stack([factory.prefix_tensor(render(r,profile,view).encode()) for r in rows[start:start+96]])
                        value = model(x,torch.zeros(len(x),dtype=torch.int64)); check_logits(value,len(x)); chunks.append(value.detach().clone())
                    raw[split][profile][view] = torch.cat(chunks)
    return raw


@contextmanager
def counted(model, core):
    counts = [0,0]; core_calls, ch = core.core_counter(model)
    def hook(module,args,output):
        counts[0] += 1; counts[1] += len(args[0])
    h = model.register_forward_hook(hook)
    try:
        yield counts, core_calls
    finally:
        h.remove()
        if ch is not None: ch.remove()


def train_one(model, seed, arm, data, tokens, targets, core, base, factory):
    require(sum(p.numel() for p in model.parameters()) == 14256, "model capacity")
    initial, back, head = base.fingerprint(model), base.fingerprint(model.backbone), base.fingerprint(model.read)
    with counted(model,core) as (counts,cores):
        fitting = fit(model,tokens,targets,seed,arm)
        final = base.fingerprint(model); raw = evaluate(model,data,factory)
    require(counts == [827,40992] and cores[0] == 3308, "training/evaluation counts")
    require(base.fingerprint(model) == final and final != initial and base.fingerprint(model.backbone) != back and base.fingerprint(model.read) != head, "state change/evaluation integrity")
    record = dict(seed=seed,arm=arm,parameters=14256,initial_sha256=initial,final_sha256=final,
        fit=fitting,raw=raw,weights_changed=True,forward_calls=827,row_presentations=40992,core_forward_calls=3308)
    return record, {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def replay_one(model,state,record,data,core,base,factory):
    model.load_state_dict(state,strict=True); model.eval()
    require(base.fingerprint(model) == record["final_sha256"], "strict checkpoint fingerprint")
    with counted(model,core) as (counts,cores):
        replayed = evaluate(model,data,factory)
    error = 0.
    for split,profile,view in itertools.product(SPLITS,PROFILES,VIEWS):
        a,b = replayed[split][profile][view],record["raw"][split][profile][view]
        check_logits(b,len(data[split])); error = max(error,float((a-b).abs().max()))
        require(error <= TOL and torch.equal(a.argmax(-1),b.argmax(-1)), "raw/argmax checkpoint replay")
    require(counts == [27,2592] and cores[0] == 108 and base.fingerprint(model) == record["final_sha256"], "replay workload/state")
    record.update(checkpoint_roundtrip=True,reload_max_error=error,replay_forward_calls=27,replay_row_presentations=2592,replay_core_forward_calls=108)


def score(data, raw):
    require(set(raw) == set(SPLITS), "evaluation splits")
    cells, order_cells, totals = [], [], []
    for split in SPLITS:
        rows = data[split]
        require(set(raw[split]) == set(PROFILES), "profile coverage")
        for profile in PROFILES:
            outputs = raw[split][profile]; require(set(outputs) == set(VIEWS), "view coverage")
            for x in outputs.values(): check_logits(x,len(rows))
            pred = {v:x.argmax(-1).tolist() for v,x in outputs.items()}
            loss = F.cross_entropy(outputs["normal"],torch.tensor([r["target"] for r in rows]),reduction="none")
            for lang,entities in itertools.product(("en","ja"),SUBSETS):
                for perm in (entities,entities[::-1]):
                    ids = [i for i,r in enumerate(rows) if (r["language"],tuple(r["entities"]),tuple(r["permutation"])) == (lang,entities,perm)]
                    groups = defaultdict(list)
                    for i in ids: groups[tuple(rows[i]["values"])].append(i)
                    n = 16 if split == "TRAIN" else 8
                    require(len(ids) == n and len(groups) == n//2 and all(len(g) == 2 for g in groups.values()), "cell groups")
                    acc = {v:sum(pred[v][i] == rows[i]["target"] for i in ids)/n for v in VIEWS}
                    qp = sum(all(pred["normal"][i] == rows[i]["target"] for i in g) for g in groups.values())/(n//2)
                    collapse = sum(pred["normal"][g[0]] == pred["normal"][g[1]] for g in groups.values())
                    ed,qd = acc["normal"]-acc["evidence_blind"],acc["normal"]-acc["query_blind"]
                    cells.append(dict(split=split,profile=profile,language=lang,entities=list(entities),permutation=list(perm),rows=n,
                        correct=round(acc["normal"]*n),accuracy=acc["normal"],query_pair_accuracy=qp,collapsed_pairs=collapse,
                        pairs=n//2,evidence_drop=ed,query_drop=qd,answer_nll=float(loss[ids].mean()),
                        passed=acc["normal"] >= .90 and qp >= .80 and ed >= .35 and qd >= .35))
                groups = defaultdict(list)
                for i,r in enumerate(rows):
                    if (r["language"],tuple(r["entities"])) == (lang,entities): groups[tuple(r["values"]),r["query"]].append(i)
                require(len(groups) == n and all(len(g) == 2 for g in groups.values()), "two-order groups")
                correct = sum(all(pred["normal"][i] == rows[i]["target"] for i in g) for g in groups.values())
                order_cells.append(dict(split=split,profile=profile,language=lang,entities=list(entities),groups=n,both_correct=correct,accuracy=correct/n,passed=correct/n >= .80))
            for lang in ("en","ja"):
                cc = [c for c in cells if (c["split"],c["profile"],c["language"]) == (split,profile,lang)]
                totals.append(dict(split=split,profile=profile,language=lang,correct=sum(c["correct"] for c in cc),rows=sum(c["rows"] for c in cc),
                    collapsed_pairs=sum(c["collapsed_pairs"] for c in cc),pairs=sum(c["pairs"] for c in cc)))
    return dict(cells=cells,two_order=order_cells,totals=totals,passed=all(c["passed"] for c in cells+order_cells))


def analyze(records,data):
    validate_data(data); require([(r["seed"],r["arm"]) for r in records] == identities(), "all model identities")
    metrics, results, contrasts = [], [], []
    for r in records:
        require(r["parameters"] == 14256 and r["weights_changed"] is True and r["checkpoint_roundtrip"] is True, "record integrity")
        require((r["forward_calls"],r["row_presentations"],r["core_forward_calls"],r["replay_forward_calls"],r["replay_row_presentations"],r["replay_core_forward_calls"]) == (827,40992,3308,27,2592,108), "record workload")
        require(type(r["reload_max_error"]) in (int,float) and math.isfinite(r["reload_max_error"]) and 0 <= r["reload_max_error"] <= TOL, "replay error")
        expected = schedule(r["seed"],r["arm"])[2]
        require(r["fit"]["steps"] == 800 and r["fit"]["training_rows"] == 38400 and all(r["fit"][k] == v for k,v in expected.items()), "fit schedule")
        m = score(data,r["raw"]); metrics.append(dict(seed=r["seed"],arm=r["arm"],**m)); results.append(dict(seed=r["seed"],arm=r["arm"],passed=m["passed"]))
    for i in range(0,10,2):
        a,b = records[i:i+2]
        require(a["initial_sha256"] == b["initial_sha256"] and a["fit"]["logical_batch_sha256"] == b["fit"]["logical_batch_sha256"] and a["fit"]["row_exposures"] == b["fit"]["row_exposures"], "paired initialization/exposures")
        for ca,cb in zip(metrics[i]["totals"],metrics[i+1]["totals"],strict=True):
            if ca["split"] == "HOLDOUT":
                require((ca["profile"],ca["language"],ca["rows"],ca["pairs"]) == (cb["profile"],cb["language"],cb["rows"],cb["pairs"]), "paired cells")
                contrasts.append(dict(seed=a["seed"],profile=ca["profile"],language=ca["language"],rows=ca["rows"],pairs=ca["pairs"],
                    control_correct=ca["correct"],mixed_correct=cb["correct"],correct_delta=cb["correct"]-ca["correct"],
                    control_collapsed=ca["collapsed_pairs"],mixed_collapsed=cb["collapsed_pairs"],collapse_delta=cb["collapsed_pairs"]-ca["collapsed_pairs"]))
    summary = dict(models=10,seed_results=results,seed_pass_counts={a:sum(r["passed"] for r in results if r["arm"] == a) for a in ARMS},
        candidate_gate=all(r["passed"] for r in results if r["arm"] == "mixed_names"),contrasts=contrasts,
        train_steps=8000,training_rows=384000,model_forward_calls=8540,row_presentations=435840,core_forward_calls=34160,
        checkpoint_bundle_loads=1,model_state_loads=10,new_checkpoint_writes=1,all_replays=True,all_pairs_matched=True)
    return metrics,summary


def load_parent(path):
    parent,*_,audit = context(); path = Path(path).resolve()
    require(audit.sha(path) == PARENT_SHA, "accepted diagnostic summary hash")
    p = audit.read_json(path); parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS" and p["capability_pass_claim"] is False, "diagnostic-only parent")
    require({x["file"]:x["sha256"] for x in p["artifacts"]} == PARENT_ARTIFACTS, "parent artifact contract")
    for x in p["artifacts"]:
        child = audit.safe_child(path.parent,x["file"])
        require(audit.sha(child) == x["sha256"] and child.stat().st_size == x["serialized_bytes"], "parent artifact bytes")
    require(audit.read_json(path.parent/"audit-plan.json") == parent.manifest() and audit.read_json(path.parent/"validation-summary.json") == p["validation_summary"], "parent JSON semantics")
    return p


def precheck(path,root):
    *_,factory,audit = context(); path = Path(path).resolve(); root = Path(root)
    p = load_parent(path); pins,protected = dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items(): require(Path(name).is_file() and audit.sha(name) == wanted, "changed input:"+name)
    for name,wanted in pins.items(): require(audit.git(root,"rev-parse","HEAD:"+name).decode().strip() == wanted, "changed source:"+name)
    for child,wanted in [(path,PARENT_SHA)]+[(audit.safe_child(path.parent,x["file"]),x["sha256"]) for x in p["artifacts"]]:
        key = str(child.resolve()); require(key not in protected, "duplicate input"); protected[key] = wanted
    for name in OWN:
        require(name not in pins, "OWN collision"); pins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-6])_[^/]+)\.py"
    deps = set(factory.LM_SOURCES)|{n for n in p["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps) == 43 and deps <= set(pins), "direct dependencies")
    protected.update(audit.protect_tree_files(root,pins))
    require((len(pins),len(protected)) == (448,761) and digest(manifest()) == MANIFEST_SHA, "registration counts/hash")
    validate_data(dataset()); print("registration_check = source_pins:448; protected_inputs:761; manifest_sha256:"+MANIFEST_SHA,flush=True)
    return pins,protected


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["diagnostic_execution_valid"] is True, "result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"])) == (448,761) and set(OWN) <= set(p["source_blobs"]), "protection")
    require(len(p["artifacts"]) == 6 and {x["file"] for x in p["artifacts"]} == set(OUTPUTS), "output coverage")
    s = p["validation_summary"]; rr = s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rr] == identities() and all(type(r["passed"]) is bool for r in rr), "result coverage")
    require(s["candidate_gate"] is all(r["passed"] for r in rr if r["arm"] == "mixed_names") and s["seed_pass_counts"] == {a:sum(r["passed"] for r in rr if r["arm"] == a) for a in ARMS}, "gate accounting")
    for k in ("models","train_steps","training_rows","model_forward_calls","row_presentations","core_forward_calls","checkpoint_bundle_loads","model_state_loads","new_checkpoint_writes"):
        require(type(s[k]) is int and s[k] == manifest()[k], "workload:"+k)
    require(len(s["contrasts"]) == 30 and s["all_replays"] is True and s["all_pairs_matched"] is True and p["status"] == ("PASS" if s["candidate_gate"] else "FAIL"), "status")
    require(all(p[k] is False for k in ("gate_f_candidate","production_adoption","unseen_name_transfer_claim","causal_parser_claim","naming_benefit_claim")), "scope")


def load_bundle(path):
    v = torch.load(path,map_location="cpu",weights_only=True)
    require(set(v) == {"schema","identities","states"} and v["schema"] == "fold-c267-coverage-models-v1", "bundle schema")
    require(v["identities"] == [list(x) for x in identities()] and len(v["states"]) == 10, "bundle identities")
    return v["states"]


def flatten(suite):
    for test in suite:
        if isinstance(test,unittest.TestSuite): yield from flatten(test)
        else: yield test


def regression_modules(root):
    modules = context()[0].regression_modules(root)
    require(len(modules) == len(set(modules)) == 151, "parent modules")
    return modules+["tests_lm.test_v05_c267_name_coverage_training"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1, "suite identities")
    kept = [t for t in tests if t.id() != EXCLUDED]; require((len(tests),len(kept)) == (3574,3573), "suite counts")
    return unittest.TestSuite(kept)


def run(*,c266_summary,output_dir,expected_head):
    _,core,base,aligned,reader,factory,audit = context(); root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip() == expected_head, "HEAD")
        require(audit.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss", "branch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(), "dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected = precheck(c266_summary,root)
    data = dataset()
    tokens,targets = training_tables(data,factory)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False); records,states = [],[]
    for seed in SEEDS:
        initial = base.make_model(factory.new_model(seed),"aligned_precore_read",seed,aligned,reader); original = base.fingerprint(initial)
        for arm in ARMS:
            print(f"[C267] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            r,state = train_one(copy.deepcopy(initial),seed,arm,data,tokens,targets,core,base,factory)
            require(r["initial_sha256"] == original and base.fingerprint(initial) == original, "paired initial template")
            records.append(r); states.append(state)
    torch.save(dict(schema="fold-c267-coverage-models-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for r,state in zip(records,load_bundle(out/"trained-models.pt"),strict=True):
        model = base.make_model(factory.new_model(r["seed"]),"aligned_precore_read",r["seed"],aligned,reader)
        replay_one(model,state,r,data,core,base,factory)
    metrics,summary = analyze(records,data)
    torch.save(dict(schema="fold-c267-coverage-eval-v1",records=records),out/"evaluations.pt")
    for name,value in (("coverage-plan.json",manifest()),("dataset.json",data),("measurements.json",metrics),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(); precheck(c266_summary,root)
    for name,wanted in protected.items(): require(audit.sha(name) == wanted, "modified input")
    p = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,gate_f_candidate=False,production_adoption=False,
        unseen_name_transfer_claim=False,causal_parser_claim=False,naming_benefit_claim=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p)); print("=== C267 RESULT ===",flush=True); print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(output_dir,expected_head):
    audit = context()[-1]; out = Path(output_dir); p = audit.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"] == expected_head, "saved HEAD")
    for name,wanted in p["input_sha256"].items(): require(audit.sha(name) == wanted, "postcheck input")
    for x in p["artifacts"]:
        child = audit.safe_child(out,x["file"]); require(audit.sha(child) == x["sha256"] and child.stat().st_size == x["serialized_bytes"], "output bytes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("saved postcheck forbids model calls")):
        data = audit.read_json(out/"dataset.json"); archive = torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive) == {"schema","records"} and archive["schema"] == "fold-c267-coverage-eval-v1", "evaluation schema")
        metrics,summary = analyze(archive["records"],data)
        for name,value in (("coverage-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):
            require(audit.read_json(out/name) == value, "persisted reconstruction:"+name)
    require(p["validation_summary"] == summary, "saved summary")
    return p,metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("c266-summary","output-dir"): parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True); run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
