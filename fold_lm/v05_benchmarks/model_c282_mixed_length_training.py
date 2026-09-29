"""C282: fixed-budget length coverage, not a claim of unseen-length generalization."""
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
from types import SimpleNamespace
from unittest.mock import patch

import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C282-v5b-mixed-length-training"
STAGE = "V5-B-MIXED-LENGTH-TRAINING"
BASE = "d54a8d5a775949ccb54dae6ebc9e934c7579c8f5"
PARENT_EXECUTION = "96d02062bf98cf32cfc5173c36db28bb00960f0d"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c281_saved_support_transition_audit.py"
PARENT_BLOB = "2e06703af5e187febc12dbf65f33e3a6a773e612"
SUMMARY_SHAS = (
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
    "audit-plan.json": ("ff14c1b8c6ed2a2c36f72b716732e8ae624d3ab9e2f96675a7f0763a17a10ea2", 2603),
    "failure-profile.json": ("dd80ffb33f3f98aa4b129cef5f5cec56562010b509f5933af41cf76e26d41420", 1178793),
    "validation-summary.json": ("1fc1e6e768b4ebfd1211974fae99dcb35603f2cf06b3e7d54fa7f8479426da2f", 15880),
}
SEEDS = tuple(range(282001, 282006))
ARMS = ("two_char_only", "mixed_length")
OWN = ("fold_lm/v05_benchmarks/model_c282_mixed_length_training.py",
       "tests_lm/test_v05_c282_mixed_length_training.py", "tools/run_c282.ps1", "tools/invoke_c282.ps1",
       "docs/experiment-ledger-addendum-c282-preregistration.md", "docs/v5b-mixed-length-training-v0.1.md")
OUTPUTS = ("architecture-plan.json", "dataset.json", "triple-dataset.json", "trained-models.pt",
           "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10, train_steps=8000, training_rows=384000, model_forward_calls=9080,
            row_presentations=487680, core_forward_calls=36320, checkpoint_bundle_loads=1,
            model_state_loads=10, new_checkpoint_writes=1)
TOL = 1e-9
MANIFEST_SHA = "291ed152bec43b222e54851c5e4699776e220d60937a733599c37f617ed400de"


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
    from fold_lm.v05_benchmarks import model_c281_saved_support_transition_audit as parent
    previous = parent.context()[0]
    _, c278, c270, c269, p267, core, base, _, reader, factory, audit = previous.context()
    return SimpleNamespace(parent=parent, previous=previous, c278=c278, c270=c270, c269=c269,
                           p267=p267, core=core, base=base, reader=reader, factory=factory, audit=audit)


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION, summary_sha256=list(SUMMARY_SHAS),
                parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
                parent_artifacts={k: list(v) for k, v in PARENT_ARTIFACTS.items()},
                seeds=list(SEEDS), arms=list(ARMS), architecture="actual C278 MeanFinalDualReadout; all-token support in both arms",
                parameters=14256, changed="TRAIN rendering length coverage only; no new attention path",
                data_sha256="1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
                triple_data_sha256="432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",
                schedule="200 epochs x4 batches; randperm96 seed+282000+epoch;24 complete query pairs/batch;profile=epoch%3",
                lengths="two_char_only:length0; mixed_length:length=epoch%2;0=two-char,1=three-char",
                length_profile_updates={ARMS[0]: [[268,268,264],[0,0,0]], ARMS[1]: [[136,132,132],[132,136,132]]},
                logical_row_exposures=200, per_length_row_exposures={ARMS[0]: [200,0], ARMS[1]: [100,100]},
                train_tables=[2,3,192,48], optimizer="AdamW", lr=.005, betas=[.9,.999], eps=1e-8,
                weight_decay=0., clip=1., loss="mean CE only", steps_per_model=800, fit_rng="seed+283000 reset per arm",
                gate=dict(accuracy=.90, query_pair=.80, evidence_drop=.35, query_drop=.35, two_order=.80),
                primary="all five mixed_length final states pass both complete C267/C270 tasks; control separate",
                interpretation="candidate sees three-character TRAIN names; success is seen-length held-out-value-combination learning, NOT unseen-length transfer",
                unseen_length_success_claim=False, gate_f_candidate=False, production_adoption=False,
                source_pins=538, protected_inputs=950, dependency_union=58, own_tests=32,
                modules=167, loaded_tests=3950, focused_tests=3949, excluded_test=EXCLUDED,
                dtype="CPU float64", threads=2, deterministic=True, replay_tolerance=TOL, network_calls=0, **WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None, "manifest not sealed")
    require(digest(manifest()) == MANIFEST_SHA, "manifest digest mismatch")


def schedule(seed, arm, rows):
    require(seed in SEEDS and arm in ARMS and len(rows) == 192, "schedule identity")
    groups = {}
    for i, r in enumerate(rows):
        k = (r["language"], tuple(r["entities"]), tuple(r["values"]), tuple(r["permutation"]))
        groups.setdefault(k, []).append(i)
    pairs = []
    for k in sorted(groups):
        ids = sorted(groups[k], key=lambda i: rows[i]["query"])
        require(len(ids) == 2 and [rows[i]["query"] for i in ids] == list(k[1]), "complete query pair")
        require(rows[ids[0]]["target"] != rows[ids[1]]["target"], "distinct targets")
        pairs.append(ids)
    require(len(pairs) == 96 and sorted(sum(pairs, [])) == list(range(192)), "complete pair partition")
    pairs = torch.tensor(pairs, dtype=torch.int64)
    indices, profiles, lengths = [], [], []
    for epoch in range(200):
        order = torch.randperm(96, generator=torch.Generator().manual_seed(seed + 282000 + epoch))
        for block in range(4):
            indices.append(pairs[order[block*24:(block+1)*24]].flatten())
            profiles.append(epoch % 3)
            lengths.append(0 if arm == ARMS[0] else epoch % 2)
    x, p, l = torch.stack(indices), torch.tensor(profiles), torch.tensor(lengths)
    exposure = [torch.bincount(x[l == j].flatten(), minlength=192).tolist() for j in range(2)]
    lp = [[sum(a == j and b == k for a, b in zip(lengths, profiles, strict=True)) for k in range(3)] for j in range(2)]
    require(lp == manifest()["length_profile_updates"][arm], "length/profile exposure")
    require(exposure == [[n]*192 for n in manifest()["per_length_row_exposures"][arm]], "row exposure")
    plan = dict(logical_batch_sha256=digest(x.tolist()), rendering_schedule_sha256=digest([profiles, lengths]),
                length_profile_updates=lp, per_length_row_exposures=exposure,
                row_exposures=torch.bincount(x.flatten(), minlength=192).tolist())
    return x, p, l, plan


def training_tables(data, c):
    c.p267.validate_data(data)
    rows = data["TRAIN"]
    tables = []
    for renderer, profiles in ((c.p267.render, c.p267.PROFILES), (c.c270.render, c.c270.PROFILES)):
        tables.append(torch.stack([torch.stack([c.factory.prefix_tensor(renderer(r, p, "normal").encode())
                                               for r in rows]) for p in profiles]))
    tokens = torch.stack(tables)
    targets = torch.tensor([r["target"] for r in rows], dtype=torch.int64)
    require(tokens.shape == (2,3,192,48) and tokens.dtype == torch.int64 and targets.shape == (192,), "training tables")
    return tokens, targets


def table_hash(tokens, targets):
    return digest(dict(tokens=tokens.tolist(), targets=targets.tolist()))


def make_models(seed, c):
    require(seed in SEEDS, "model seed")
    control = c.c278.MeanFinalDualReadout(c.factory.new_model(seed), seed, c.reader, c.c269.query_span_mask)
    candidate = copy.deepcopy(control)
    require(type(control) is type(candidate) is c.c278.MeanFinalDualReadout, "unchanged architecture")
    require(sum(p.numel() for p in control.parameters()) == sum(p.numel() for p in candidate.parameters()) == 14256, "capacity")
    require(list(control.state_dict()) == list(candidate.state_dict()) and c.base.fingerprint(control) == c.base.fingerprint(candidate), "matched initial state")
    require(all(a.data_ptr() != b.data_ptr() for a, b in zip(control.parameters(), candidate.parameters(), strict=True)), "independent storage")
    return dict(zip(ARMS, (control, candidate), strict=True))


def fit(model, data, tokens, targets, seed, arm):
    require(tokens.shape == (2,3,192,48) and tokens.dtype == targets.dtype == torch.int64 and targets.shape == (192,), "fit tables")
    indices, profiles, lengths, plan = schedule(seed, arm, data["TRAIN"])
    torch.manual_seed(seed + 283000)
    optimizer = torch.optim.AdamW(model.parameters(), lr=.005, betas=(.9,.999), eps=1e-8, weight_decay=0.)
    model.train()
    for step in range(800):
        ids = indices[step]
        optimizer.zero_grad(set_to_none=True)
        logits = model(tokens[lengths[step], profiles[step], ids], torch.zeros(48, dtype=torch.int64))
        loss = F.cross_entropy(logits, targets[ids])
        require(bool(torch.isfinite(loss)), "nonfinite loss")
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1., error_if_nonfinite=True)
        optimizer.step()
        if (step + 1) % 200 == 0:
            print(f"[C282] seed={seed} arm={arm} step={step+1}/800 ce={float(loss.detach()):.6f}", flush=True)
    model.eval()
    return dict(steps=800, training_rows=38400, last_ce=float(loss.detach()), table_sha256=table_hash(tokens, targets), **plan)


def train_one(model, data, prompts, tokens, targets, seed, arm, c):
    initial = c.base.fingerprint(model)
    back, head = c.base.fingerprint(model.backbone), c.base.fingerprint(model.read)
    with c.p267.counted(model, c.core) as (counts, cores):
        fitted = fit(model, data, tokens, targets, seed, arm)
        final = c.base.fingerprint(model)
        two = c.p267.evaluate(model, data, c.factory)
        triple = c.c270.evaluate_new(model, prompts, data, c.factory, c.p267)
    require(counts == [854,43584] and cores[0] == 3416, "train/evaluation workload")
    require(c.base.fingerprint(model) == final and initial != final and back != c.base.fingerprint(model.backbone)
            and head != c.base.fingerprint(model.read), "weight/evaluation integrity")
    r = dict(seed=seed, arm=arm, parameters=14256, initial_sha256=initial, final_sha256=final, fit=fitted,
             raw_two=two, raw_triple=triple, weights_changed=True, forward_calls=854, row_presentations=43584, core_forward_calls=3416)
    return r, {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def analyze(records, data, c):
    require([(r["seed"], r["arm"]) for r in records] == identities(), "record identities")
    tokens, targets = training_tables(data, c)
    thash = table_hash(tokens, targets)
    metrics, results, contrasts = [], [], []
    for r in records:
        require(r["parameters"] == 14256 and r["weights_changed"] is True and r["checkpoint_roundtrip"] is True, "record integrity")
        err = r["reload_max_error"]
        require(type(err) in (int,float) and math.isfinite(err) and 0 <= err <= TOL, "replay error")
        names = ("forward_calls", "row_presentations", "core_forward_calls", "replay_forward_calls", "replay_row_presentations", "replay_core_forward_calls")
        require(tuple(r[n] for n in names) == (854,43584,3416,54,5184,216), "record workload")
        plan = schedule(r["seed"], r["arm"], data["TRAIN"])[3]
        fitted = r["fit"]
        require(fitted["steps"] == 800 and fitted["training_rows"] == 38400 and fitted["table_sha256"] == thash
                and all(fitted[k] == v for k,v in plan.items()) and math.isfinite(fitted["last_ce"]), "fit plan")
        two, tri = c.p267.score(data, r["raw_two"]), c.c270.score(data, r["raw_triple"], c.p267)
        require(type(two["passed"]) is bool and type(tri["passed"]) is bool, "task flags")
        passed = two["passed"] and tri["passed"]
        metrics.append(dict(seed=r["seed"], arm=r["arm"], two_char=two, triple=tri, passed=passed))
        results.append(dict(seed=r["seed"], arm=r["arm"], two_char_pass=two["passed"], triple_pass=tri["passed"], passed=passed))
    for i in range(0,10,2):
        a, b = records[i:i+2]
        require(a["initial_sha256"] == b["initial_sha256"] and a["fit"]["logical_batch_sha256"] == b["fit"]["logical_batch_sha256"], "matched states/batches")
        for task in ("two_char", "triple"):
            left, right = metrics[i][task]["totals"], metrics[i+1][task]["totals"]
            for x, y in zip(left, right, strict=True):
                require(all(x[k] == y[k] for k in ("split","profile","language","rows","pairs")), "contrast identity")
                if task == "two_char" and x["split"] != "HOLDOUT":
                    continue
                contrasts.append(dict(task=task, seed=a["seed"], **{k:x[k] for k in ("split","profile","language","rows","pairs")},
                                      control_correct=x["correct"], candidate_correct=y["correct"],
                                      control_collapsed=x["collapsed_pairs"], candidate_collapsed=y["collapsed_pairs"]))
    require(len(contrasts) == 90, "contrast count")
    summary = dict(seed_results=results, contrasts=contrasts, all_pairs_matched=True, all_replays=True,
                   candidate_gate=all(r["passed"] for r in results if r["arm"] == ARMS[1]),
                   unseen_length_success_claim=False, **WORK)
    for out, field in (("seed_pass_counts","passed"), ("two_char_pass_counts","two_char_pass"), ("triple_pass_counts","triple_pass")):
        summary[out] = {a:sum(r[field] for r in results if r["arm"] == a) for a in ARMS}
    return metrics, summary


def load_parent(paths, c):
    paths = [Path(p).resolve() for p in paths]
    require(len(paths) == 8 and all(c.audit.sha(p) == s for p,s in zip(paths, SUMMARY_SHAS, strict=True)), "parent summary hashes")
    with patch.object(torch.nn.Module, "_call_impl", side_effect=RuntimeError("C282 parent forbids neural calls")):
        payload, report = c.parent.verify_artifacts(paths[0].parent, paths[1:], PARENT_EXECUTION)
    c.parent.validate_result(payload)
    require(payload["commit_sha"] == PARENT_EXECUTION and payload["status"] == "PASS"
            and payload["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "parent identity/source")
    actual = {a["file"]:(a["sha256"],a["serialized_bytes"]) for a in payload["artifacts"]}
    require(len(payload["artifacts"]) == 3 and actual == PARENT_ARTIFACTS, "parent artifacts")
    s = payload["validation_summary"]
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False and s["model_forward_calls"] == 0, "parent scope")
    for task in ("two_char_all", "triple_all"):
        require(all(t["mask_only_cells"] == 0 for t in s["primary"][task]["totals"].values()), "parent mask-only result")
    require(s["primary"]["triple_all"]["criteria"]["accuracy"]["candidate_fail"] == 85, "parent deciding metric")
    return payload


def precheck(paths, root):
    validate_seal()
    c = context()
    payload = load_parent(paths, c)
    root, p = Path(root), Path(paths[0]).resolve()
    pins, protected = dict(payload["source_blobs"]), dict(payload["input_sha256"])
    for name, value in pins.items():
        require(c.audit.git(root, "rev-parse", "HEAD:"+name).decode().strip() == value, "changed source:"+name)
    for name, value in protected.items():
        require(Path(name).is_file() and c.audit.sha(name) == value, "changed input:"+name)
    for child, value in [(p,SUMMARY_SHAS[0])] + [(c.audit.safe_child(p.parent,n),v[0]) for n,v in PARENT_ARTIFACTS.items()]:
        require(str(child.resolve()) not in protected and c.audit.sha(child) == value, "parent input")
        protected[str(child.resolve())] = value
    for name in OWN:
        require(name not in pins, "OWN collision")
        pins[name] = c.audit.git(root, "rev-parse", "HEAD:"+name).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9]|27[0-9]|28[01])_[^/]+)\.py"
    deps = set(c.factory.LM_SOURCES) | {n for n in payload["source_blobs"] if re.fullmatch(pattern,n)} | {OWN[0]}
    require(len(deps) == manifest()["dependency_union"] and deps <= set(pins), "dependency coverage")
    require(pins[PARENT_SOURCE] == PARENT_BLOB, "direct parent pin")
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected)) == (manifest()["source_pins"],manifest()["protected_inputs"]), "registration counts")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}", flush=True)
    return pins, protected


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["diagnostic_execution_valid"] is True, "identity")
    require(all(p[k] is False for k in ("gate_f_candidate","production_adoption","unseen_length_success_claim")), "scope")
    require((len(p["source_blobs"]),len(p["input_sha256"])) == (538,950) and set(OWN) <= set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "protection")
    require(len(p["artifacts"]) == len(OUTPUTS) and {a["file"] for a in p["artifacts"]} == set(OUTPUTS), "artifacts")
    s = p["validation_summary"]
    require(all(type(s[k]) is int and s[k] == v for k,v in WORK.items()), "workload")
    rr = s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rr] == identities(), "models")
    require(all(type(r[k]) is bool for r in rr for k in ("passed","two_char_pass","triple_pass")), "result flags")
    require(all(r["passed"] is (r["two_char_pass"] and r["triple_pass"]) for r in rr), "whole gate")
    for out, field in (("seed_pass_counts","passed"),("two_char_pass_counts","two_char_pass"),("triple_pass_counts","triple_pass")):
        require(s[out] == {a:sum(r[field] for r in rr if r["arm"] == a) for a in ARMS}, "subgate counts")
    gate = all(r["passed"] for r in rr if r["arm"] == ARMS[1])
    require(s["candidate_gate"] is gate and p["status"] == ("PASS" if gate else "FAIL"), "candidate gate")
    require(s["all_pairs_matched"] is True and s["all_replays"] is True and len(s["contrasts"]) == 90
            and s["unseen_length_success_claim"] is False, "replay/scope")


def load_bundle(path):
    v = torch.load(path, map_location="cpu", weights_only=True)
    require(set(v) == {"schema","identities","states"} and v["schema"] == "fold-c282-mixed-length-models-v1"
            and v["identities"] == [list(i) for i in identities()] and len(v["states"]) == 10, "bundle identity")
    return v["states"]


def flatten(suite):
    for x in suite:
        if isinstance(x, unittest.TestSuite):
            yield from flatten(x)
        else:
            yield x


def regression_modules(root):
    names = context().parent.regression_modules(root)
    require(len(names) == len(set(names)) == manifest()["modules"]-1, "parent modules")
    return names + ["tests_lm.test_v05_c282_mixed_length_training"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) == manifest()["loaded_tests"] and ids.count(EXCLUDED) == 1, "loaded suite")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require(len(kept) == manifest()["focused_tests"], "focused suite")
    return unittest.TestSuite(kept)


def guard(root, head, c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip() == head
            and c.audit.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(), "repository guard")


def run(*, summaries, output_dir, expected_head):
    c, root = context(), Path(__file__).resolve().parents[2]
    guard(root,expected_head,c)
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    pins, protected = precheck(summaries,root)
    data = c.p267.dataset()
    c.p267.validate_data(data)
    prompts = c.c270.prompt_dataset(data,c.p267)
    c.c270.validate_dataset(prompts,data,c.p267)
    tokens, targets = training_tables(data,c)
    out = Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    records, states = [], []
    for seed in SEEDS:
        models = make_models(seed,c)
        for arm in ARMS:
            print(f"[C282] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            r, state = train_one(models[arm],data,prompts,tokens,targets,seed,arm,c)
            records.append(r)
            states.append(state)
    torch.save(dict(schema="fold-c282-mixed-length-models-v1",identities=[list(i) for i in identities()],states=states),out/"trained-models.pt")
    states = load_bundle(out/"trained-models.pt")
    for i,seed in enumerate(SEEDS):
        models = make_models(seed,c)
        for j,arm in enumerate(ARMS):
            k = 2*i+j
            c.previous.replay_one(models[arm],states[k],records[k],data,prompts,c.p267,c.c270,c.core,c.base,c.factory)
    metrics, summary = analyze(records,data,c)
    torch.save(dict(schema="fold-c282-mixed-length-eval-v1",records=records),out/"evaluations.pt")
    for name,value in (("architecture-plan.json",manifest()),("dataset.json",data),("triple-dataset.json",prompts),
                       ("measurements.json",metrics),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c)
    precheck(summaries,root)
    p = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
             diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
             validation_summary=summary,gate_f_candidate=False,production_adoption=False,unseen_length_success_claim=False)
    validate_result(p)
    (out/"summary.json").write_bytes(blob(p))
    print("=== C282 RESULT ===",flush=True)
    print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    c, out = context(), Path(outdir)
    p = c.audit.read_json(out/"summary.json")
    validate_result(p)
    require(p["commit_sha"] == expected_head,"execution HEAD")
    for name,value in p["input_sha256"].items():
        require(c.audit.sha(name) == value,"protected input")
    for a in p["artifacts"]:
        child = c.audit.safe_child(out,a["file"])
        require(c.audit.sha(child) == a["sha256"] and child.stat().st_size == a["serialized_bytes"],"output bytes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C282 postcheck forbids neural calls")):
        load_parent(summaries,c)
        data = c.audit.read_json(out/"dataset.json")
        c.p267.validate_data(data)
        prompts = c.audit.read_json(out/"triple-dataset.json")
        c.c270.validate_dataset(prompts,data,c.p267)
        v = torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(v) == {"schema","records"} and v["schema"] == "fold-c282-mixed-length-eval-v1","eval schema")
        metrics,summary = analyze(v["records"],data,c)
        for name,value in (("architecture-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):
            require(c.audit.read_json(out/name) == value,"persisted:"+name)
    require(summary == p["validation_summary"],"summary reconstruction")
    return p,metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summaries",nargs=8,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
