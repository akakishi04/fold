"""C284: maximum-training-length-matched three-only versus mixed-length transfer."""
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
from torch.nn import functional as F

EXPERIMENT_ID = "C284-v5b-max-length-matched-training"
STAGE = "V5-B-MAX-LENGTH-MATCHED-TRAINING"
BASE = "255ad0ed293b5e6b29266f761c5e6b862a9fca37"
PARENT_EXECUTION = "24c4acd44905e1d3c4d2a019214eb588d72f9a93"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c283_frozen_four_character_transfer.py"
PARENT_BLOB = "2c204bbb5e8b53db5c2c1cd5202a0fcc5d4aa4a0"
SUMMARY_SHAS = (
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
    "transfer-plan.json": ("e88244fe1acc677d629e3b0400dc4926be9b26560c05a782122ae1e5042213a4", 3279),
    "quad-dataset.json": ("86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b", 172066),
    "eval-outputs.pt": ("283d3015f09a79bbab180bde7caa3a24381239b7e384b70745152c7471bf3ead", 265676521),
    "measurements.json": ("212155b8bc11906bd80ac3dc6ba3d397c6d7c8cc4a1169bdee75c319ae33e807", 264243),
    "validation-summary.json": ("c552ae8782437365eb7cc0bfb4049be507010c67c43280c79ed29a74c57c1928", 12038),
}
SEEDS = tuple(range(284001, 284006))
ARMS = ("three_char_only", "mixed_length")
TASKS = ("two_char", "triple", "quad")
OWN = ("fold_lm/v05_benchmarks/model_c284_max_length_matched_training.py",
       "tests_lm/test_v05_c284_max_length_matched_training.py", "tools/run_c284.ps1", "tools/invoke_c284.ps1",
       "docs/experiment-ledger-addendum-c284-preregistration.md", "docs/v5b-max-length-matched-training-v0.1.md")
OUTPUTS = ("architecture-plan.json", "dataset.json", "triple-dataset.json", "quad-dataset.json",
           "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10, train_steps=8000, training_rows=384000, model_forward_calls=9620,
            row_presentations=539520, core_forward_calls=38480, checkpoint_bundle_loads=1,
            model_state_loads=10, new_checkpoint_writes=1, network_calls=0)
TOL = 1e-9
MANIFEST_SHA = "c835e2293c8a379b4173e4030cb687c0bb0bc549ef44298a0d8f8f39b2e6c080"


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
    from fold_lm.v05_benchmarks import model_c283_frozen_four_character_transfer as parent
    c282, c = parent.context()
    return parent, c282, c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION, parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
                summary_sha256=list(SUMMARY_SHAS), parent_artifacts={k: list(v) for k, v in PARENT_ARTIFACTS.items()},
                seeds=list(SEEDS), arms=list(ARMS), parameters=14256, max_tokens=48, maximum_training_length=3,
                architecture="actual C278 all-token MeanFinalDualReadout in both arms; independently copied initial states",
                changed="length exposure allocation at matched maximum training length3 and fixed logical update budget",
                data_sha256="1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
                triple_sha256="432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",
                quad_sha256=PARENT_ARTIFACTS["quad-dataset.json"][0], train_tables=[2,3,192,48],
                schedule="200 epochs x4;randperm96(seed+284000+epoch);24 complete query pairs/batch;profile=epoch%3",
                lengths="three_char_only:length1; mixed_length:epoch%2;0=two,1=three;four never optimized",
                length_profile_updates={ARMS[0]: [[0,0,0],[268,268,264]], ARMS[1]: [[136,132,132],[132,136,132]]},
                per_length_row_exposures={ARMS[0]: [0,200], ARMS[1]: [100,100]}, logical_row_exposures=200,
                optimizer="AdamW", lr=.005, betas=[.9,.999], eps=1e-8, weight_decay=0., clip=1.,
                loss="mean CE only", steps_per_model=800, fit_rng="seed+285000 reset per arm",
                primary="all five mixed_length final states pass every C283 four-character criterion; controls separate",
                comparative="paired four-character seed pass and correct/collapse deltas; absolute PASS is not superiority",
                descriptive="two/three/all-task gates reported but do not replace four-character primary",
                limitation="exposure allocation,diversity and schedule remain coupled;bounded family only;no automatic Gate F",
                gate=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
                per_model_train_eval=[881,46176,3524], per_model_replay=[81,7776,324],
                raw_logit_payload_bytes=159252480, source_pins=550, protected_inputs=976, dependency_union=60,
                own_tests=32, modules=169, loaded_tests=4014, focused_tests=4013, excluded_test=EXCLUDED,
                dtype="CPU float64", threads=2, deterministic=True, replay_tolerance=TOL,
                gate_f_candidate=False, production_adoption=False, arbitrary_length_claim=False, **WORK)


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
        require(rows[ids[0]]["target"] != rows[ids[1]]["target"], "distinct pair targets")
        pairs.append(ids)
    require(len(pairs) == 96 and sorted(sum(pairs, [])) == list(range(192)), "complete pair partition")
    pairs = torch.tensor(pairs, dtype=torch.int64)
    batches, profiles, lengths = [], [], []
    for epoch in range(200):
        order = torch.randperm(96, generator=torch.Generator().manual_seed(seed + 284000 + epoch))
        for block in range(4):
            batches.append(pairs[order[block*24:(block+1)*24]].flatten())
            profiles.append(epoch % 3)
            lengths.append(1 if arm == ARMS[0] else epoch % 2)
    x, p, l = torch.stack(batches), torch.tensor(profiles), torch.tensor(lengths)
    exposure = [torch.bincount(x[l == j].flatten(), minlength=192).tolist() for j in range(2)]
    lp = [[sum(a == j and b == k for a, b in zip(lengths, profiles, strict=True)) for k in range(3)] for j in range(2)]
    require(lp == manifest()["length_profile_updates"][arm], "length/profile exposure")
    require(exposure == [[n]*192 for n in manifest()["per_length_row_exposures"][arm]], "row exposure")
    plan = dict(logical_batch_sha256=digest(x.tolist()), rendering_schedule_sha256=digest([profiles, lengths]),
                length_profile_updates=lp, per_length_row_exposures=exposure,
                row_exposures=torch.bincount(x.flatten(), minlength=192).tolist())
    return x, p, l, plan


def make_models(seed, c):
    require(seed in SEEDS, "model seed")
    control = c.c278.MeanFinalDualReadout(c.factory.new_model(seed), seed, c.reader, c.c269.query_span_mask)
    candidate = copy.deepcopy(control)
    require(type(control) is type(candidate) is c.c278.MeanFinalDualReadout, "architecture")
    require(sum(p.numel() for p in control.parameters()) == sum(p.numel() for p in candidate.parameters()) == 14256, "capacity")
    require(list(control.state_dict()) == list(candidate.state_dict())
            and c.base.fingerprint(control) == c.base.fingerprint(candidate), "matched state")
    require(all(a.data_ptr() != b.data_ptr() for a,b in zip(control.parameters(), candidate.parameters(), strict=True)), "independent storage")
    return dict(zip(ARMS, (control, candidate), strict=True))


def fit(model, data, tokens, targets, seed, arm):
    require(tokens.shape == (2,3,192,48) and targets.shape == (192,)
            and tokens.dtype == targets.dtype == torch.int64, "fit tables")
    indices, profiles, lengths, plan = schedule(seed, arm, data["TRAIN"])
    torch.manual_seed(seed + 285000)
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
        if (step+1) % 200 == 0:
            print(f"[C284] seed={seed} arm={arm} step={step+1}/800 ce={float(loss.detach()):.6f}", flush=True)
    model.eval()
    return dict(steps=800, training_rows=38400, last_ce=float(loss.detach()), **plan)


def evaluate(model, data, triple, quad, parent, c):
    require(not any(m.training for m in model.modules())
            and not any(p.requires_grad for p in model.parameters()), "frozen final evaluation")
    return dict(two_char=c.p267.evaluate(model, data, c.factory),
                triple=c.c270.evaluate_new(model, triple, data, c.factory, c.p267),
                quad=parent.evaluate_quad(model, quad, data, c))


def train_one(model, data, triple, quad, tokens, targets, seed, arm, parent, c):
    initial = c.base.fingerprint(model)
    back, head = c.base.fingerprint(model.backbone), c.base.fingerprint(model.read)
    with c.p267.counted(model, c.core) as (calls, cores):
        fitted = fit(model, data, tokens, targets, seed, arm)
        final = c.base.fingerprint(model)
        model.requires_grad_(False)
        raw = evaluate(model, data, triple, quad, parent, c)
    require(calls == [881,46176] and cores[0] == 3524, "train/evaluation workload")
    require(initial != final and back != c.base.fingerprint(model.backbone)
            and head != c.base.fingerprint(model.read) and c.base.fingerprint(model) == final, "weight/evaluation integrity")
    record = dict(seed=seed, arm=arm, parameters=14256, initial_sha256=initial, final_sha256=final,
                  weights_changed=True, fit=fitted, raw=raw, forward_calls=881, row_presentations=46176, core_forward_calls=3524)
    return record, {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def replay_error(left, right, data, c):
    require(set(left) == set(right) == set(TASKS), "replay tasks")
    error = 0.
    for task in TASKS:
        require(set(left[task]) == set(right[task]) == {"TRAIN","HOLDOUT"}, "replay splits")
        for split in ("TRAIN","HOLDOUT"):
            require(set(left[task][split]) == set(right[task][split]), "replay profiles")
            for profile, views in left[task][split].items():
                require(set(views) == set(right[task][split][profile]) == {"normal","evidence_blind","query_blind"}, "replay views")
                for view, a in views.items():
                    b = right[task][split][profile][view]
                    c.p267.check_logits(a, len(data[split])); c.p267.check_logits(b, len(data[split]))
                    error = max(error, float((a-b).abs().max()))
                    require(error <= TOL and torch.equal(a.argmax(-1), b.argmax(-1)), "raw/argmax replay")
    return error


def replay_one(model, state, record, data, triple, quad, parent, c):
    model.load_state_dict(state, strict=True)
    model.eval(); model.requires_grad_(False)
    require(c.base.fingerprint(model) == record["final_sha256"], "strict state fingerprint")
    with c.p267.counted(model, c.core) as (calls, cores):
        raw = evaluate(model, data, triple, quad, parent, c)
    error = replay_error(raw, record["raw"], data, c)
    require(calls == [81,7776] and cores[0] == 324 and c.base.fingerprint(model) == record["final_sha256"], "replay workload/state")
    record.update(checkpoint_roundtrip=True, reload_max_error=error, replay_forward_calls=81,
                  replay_row_presentations=7776, replay_core_forward_calls=324)


def analyze(records, data, parent, c):
    require([(r["seed"],r["arm"]) for r in records] == identities(), "record identities")
    metrics, results, contrasts = [], [], []
    for r in records:
        require(r["parameters"] == 14256 and r["weights_changed"] is True and r["checkpoint_roundtrip"] is True, "record integrity")
        err = r["reload_max_error"]
        require(type(err) in (int,float) and math.isfinite(err) and 0 <= err <= TOL, "replay bound")
        keys = ("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(tuple(r[k] for k in keys) == (881,46176,3524,81,7776,324), "record workload")
        plan = schedule(r["seed"],r["arm"],data["TRAIN"])[3]
        fitted = r["fit"]
        require(fitted["steps"] == 800 and fitted["training_rows"] == 38400
                and math.isfinite(fitted["last_ce"]) and all(fitted[k] == v for k,v in plan.items()), "fit plan")
        require(set(r["raw"]) == set(TASKS), "scored tasks")
        scored = dict(two_char=c.p267.score(data,r["raw"]["two_char"]),
                      triple=c.c270.score(data,r["raw"]["triple"],c.p267),
                      quad=parent.score_quad(data,r["raw"]["quad"],c))
        require(all(type(m["passed"]) is bool for m in scored.values()), "task flags")
        flags = {t+"_pass":scored[t]["passed"] for t in TASKS}
        results.append(dict(seed=r["seed"],arm=r["arm"],passed=flags["quad_pass"],all_tasks_pass=all(flags.values()),**flags))
        metrics.append(dict(seed=r["seed"],arm=r["arm"],**scored))
    for i in range(0,10,2):
        a,b = records[i:i+2]
        require(a["initial_sha256"] == b["initial_sha256"]
                and a["fit"]["logical_batch_sha256"] == b["fit"]["logical_batch_sha256"], "matched states/batches")
        for task in TASKS:
            for x,y in zip(metrics[i][task]["totals"],metrics[i+1][task]["totals"],strict=True):
                require(all(x[k] == y[k] for k in ("split","profile","language","rows","pairs")), "contrast identity")
                contrasts.append(dict(task=task,seed=a["seed"],**{k:x[k] for k in ("split","profile","language","rows","pairs")},
                                      control_correct=x["correct"],candidate_correct=y["correct"],
                                      control_collapsed=x["collapsed_pairs"],candidate_collapsed=y["collapsed_pairs"]))
    require(len(contrasts) == 180, "contrast count")
    summary = dict(seed_results=results,contrasts=contrasts,all_pairs_matched=True,all_replays=True,
                   candidate_gate=all(r["quad_pass"] for r in results if r["arm"] == ARMS[1]),**WORK)
    for out,field in (("seed_pass_counts","passed"),("two_char_pass_counts","two_char_pass"),
                      ("triple_pass_counts","triple_pass"),("quad_pass_counts","quad_pass"),("all_tasks_pass_counts","all_tasks_pass")):
        summary[out] = {a:sum(r[field] for r in results if r["arm"] == a) for a in ARMS}
    return metrics,summary


def load_parent(paths):
    parent,_,c = context()
    paths = [Path(p).resolve() for p in paths]
    require(len(paths) == 10 and all(c.audit.sha(p) == s for p,s in zip(paths,SUMMARY_SHAS,strict=True)), "parent summary hashes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C284 parent forbids neural calls")), \
         patch.object(torch.nn.Module,"load_state_dict",side_effect=RuntimeError("C284 parent forbids state loading")), \
         patch.object(torch,"save",side_effect=RuntimeError("C284 parent forbids writes")):
        payload,_ = parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION)
    parent.validate_result(payload)
    require(payload["commit_sha"] == PARENT_EXECUTION and payload["status"] == "FAIL"
            and payload["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "parent identity/source")
    artifacts = {a["file"]:(a["sha256"],a["serialized_bytes"]) for a in payload["artifacts"]}
    require(len(payload["artifacts"]) == 5 and artifacts == PARENT_ARTIFACTS, "parent artifacts")
    s = payload["validation_summary"]
    require(s["candidate_gate"] is False and s["seed_pass_counts"] == {"two_char_only":0,"mixed_length":3}
            and s["all_replays"] is True and s["all_weights_preserved"] is True, "parent verdict")
    return payload


def precheck(paths,root):
    validate_seal(); payload = load_parent(paths)
    _,_,c = context(); root,p = Path(root),Path(paths[0]).resolve()
    pins,protected = dict(payload["source_blobs"]),dict(payload["input_sha256"])
    for n,w in pins.items():
        require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip() == w, "changed source:"+n)
    for n,w in protected.items():
        require(Path(n).is_file() and c.audit.sha(n) == w, "changed input:"+n)
    for child,w in [(p,SUMMARY_SHAS[0])] + [(c.audit.safe_child(p.parent,n),v[0]) for n,v in PARENT_ARTIFACTS.items()]:
        require(str(child.resolve()) not in protected and c.audit.sha(child) == w, "parent input")
        protected[str(child.resolve())] = w
    for n in OWN:
        require(n not in pins, "OWN collision"); pins[n] = c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9]|27[0-9]|28[0-3])_[^/]+)\.py"
    deps = set(c.factory.LM_SOURCES) | {n for n in payload["source_blobs"] if re.fullmatch(pattern,n)} | {OWN[0]}
    require(len(deps) == manifest()["dependency_union"] and deps <= set(pins), "dependency coverage")
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected)) == (550,976), "registration counts")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["diagnostic_execution_valid"] is True, "identity")
    require(all(p[k] is False for k in ("gate_f_candidate","production_adoption","arbitrary_length_claim")), "scope")
    require((len(p["source_blobs"]),len(p["input_sha256"])) == (550,976) and set(OWN) <= set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "protection")
    require(len(p["artifacts"]) == len(OUTPUTS) and {a["file"] for a in p["artifacts"]} == set(OUTPUTS), "artifacts")
    s = p["validation_summary"]; rr = s["seed_results"]
    require(all(type(s[k]) is int and s[k] == v for k,v in WORK.items()), "workload")
    require([(r["seed"],r["arm"]) for r in rr] == identities(), "results")
    require(all(type(r[k]) is bool for r in rr for k in ("passed","two_char_pass","triple_pass","quad_pass","all_tasks_pass")), "result flags")
    require(all(r["passed"] is r["quad_pass"] and r["all_tasks_pass"] is all(r[t+"_pass"] for t in TASKS) for r in rr), "primary versus descriptive gates")
    for out,field in (("seed_pass_counts","passed"),("two_char_pass_counts","two_char_pass"),
                      ("triple_pass_counts","triple_pass"),("quad_pass_counts","quad_pass"),("all_tasks_pass_counts","all_tasks_pass")):
        require(s[out] == {a:sum(r[field] for r in rr if r["arm"] == a) for a in ARMS}, "pass counts")
    gate = all(r["quad_pass"] for r in rr if r["arm"] == ARMS[1])
    require(s["candidate_gate"] is gate and p["status"] == ("PASS" if gate else "FAIL"), "candidate gate")
    require(s["all_pairs_matched"] is True and s["all_replays"] is True and len(s["contrasts"]) == 180, "replay/contrasts")


def load_bundle(path):
    v = torch.load(path,map_location="cpu",weights_only=True)
    require(set(v) == {"schema","identities","states"} and v["schema"] == "fold-c284-max-length-models-v1"
            and v["identities"] == [list(i) for i in identities()] and len(v["states"]) == 10, "bundle identity")
    return v["states"]


def flatten(suite):
    for x in suite:
        if isinstance(x,unittest.TestSuite): yield from flatten(x)
        else: yield x


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == manifest()["modules"]-1, "parent modules")
    return names + ["tests_lm.test_v05_c284_max_length_matched_training"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) == manifest()["loaded_tests"] and ids.count(EXCLUDED) == 1, "loaded suite")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require(len(kept) == manifest()["focused_tests"], "focused suite")
    return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip() == head
            and c.audit.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(), "repository guard")


def run(*,summaries,output_dir,expected_head):
    parent,c282,c = context(); root = Path(__file__).resolve().parents[2]
    guard(root,expected_head,c); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected = precheck(summaries,root)
    data = c.p267.dataset(); c.p267.validate_data(data)
    triple = c.c270.prompt_dataset(data,c.p267); c.c270.validate_dataset(triple,data,c.p267)
    quad = parent.dataset(data); parent.validate_dataset(quad,data,c)
    tokens,targets = c282.training_tables(data,c)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    records,states = [],[]
    for seed in SEEDS:
        models = make_models(seed,c)
        for arm in ARMS:
            print(f"[C284] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            r,state = train_one(models[arm],data,triple,quad,tokens,targets,seed,arm,parent,c)
            records.append(r); states.append(state)
    torch.save(dict(schema="fold-c284-max-length-models-v1",identities=[list(i) for i in identities()],states=states),out/"trained-models.pt")
    states = load_bundle(out/"trained-models.pt")
    for i,seed in enumerate(SEEDS):
        models = make_models(seed,c)
        for j,arm in enumerate(ARMS):
            k = 2*i+j
            replay_one(models[arm],states[k],records[k],data,triple,quad,parent,c)
    metrics,summary = analyze(records,data,parent,c)
    torch.save(dict(schema="fold-c284-max-length-eval-v1",records=records),out/"evaluations.pt")
    for n,v in (("architecture-plan.json",manifest()),("dataset.json",data),("triple-dataset.json",triple),
                ("quad-dataset.json",quad),("measurements.json",metrics),("validation-summary.json",summary)):
        (out/n).write_bytes(blob(v))
    artifacts = [dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c); precheck(summaries,root)
    p = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
             diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
             validation_summary=summary,gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    print("=== C284 RESULT ===",flush=True); print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    parent,_,c = context(); out = Path(outdir)
    p = c.audit.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"] == expected_head, "execution HEAD")
    for n,w in p["input_sha256"].items(): require(c.audit.sha(n) == w, "protected input")
    for a in p["artifacts"]:
        child = c.audit.safe_child(out,a["file"])
        require(c.audit.sha(child) == a["sha256"] and child.stat().st_size == a["serialized_bytes"], "output bytes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C284 postcheck forbids neural calls")):
        load_parent(summaries)
        data = c.audit.read_json(out/"dataset.json"); c.p267.validate_data(data)
        c.c270.validate_dataset(c.audit.read_json(out/"triple-dataset.json"),data,c.p267)
        parent.validate_dataset(c.audit.read_json(out/"quad-dataset.json"),data,c)
        v = torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(v) == {"schema","records"} and v["schema"] == "fold-c284-max-length-eval-v1", "eval schema")
        metrics,summary = analyze(v["records"],data,parent,c)
        for n,value in (("architecture-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):
            require(c.audit.read_json(out/n) == value, "persisted:"+n)
    require(p["validation_summary"] == summary, "summary reconstruction")
    return p,metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summaries",nargs=10,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__": main()
