"""C286: constant versus late cosine LR; identical mixed-length data and update budget."""
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

EXPERIMENT_ID = "C286-v5b-cosine-tail-stability"
STAGE = "V5-B-COSINE-TAIL-STABILITY"
BASE = "100ac28eca9015269fd69104edf36645c4f1bf9a"
PARENT_EXECUTION = "f2bd32785895c30defa16be7d1eca6279ba4ed23"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c285_saved_length_transfer_audit.py"
PARENT_BLOB = "383b4156351c601a26b1f58c2ccdea59206f8538"
SUMMARY_SHAS = (
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
    "audit-plan.json": ("cef543afe98b94e09f62183c1175f4dca8727838aad6a40a341e1beef641286c", 3246),
    "cell-attribution.json": ("2d733c0d92bf57678ff610153aab95d48ab2b1c17ec67d8bc447cedd2c2f8b15", 1687080),
    "validation-summary.json": ("a814abd30a8a5432722ed35ae0ee19d87706aa4db5a876a58887e4de4e6ebf3b", 29907),
}
SEEDS = tuple(range(286001, 286006))
ARMS = ("constant_lr", "cosine_tail")
TASKS = ("two_char", "triple", "quad")
OWN = ("fold_lm/v05_benchmarks/model_c286_cosine_tail_stability.py",
       "tests_lm/test_v05_c286_cosine_tail_stability.py", "tools/run_c286.ps1", "tools/invoke_c286.ps1",
       "docs/experiment-ledger-addendum-c286-preregistration.md", "docs/v5b-cosine-tail-stability-v0.1.md")
OUTPUTS = ("architecture-plan.json", "dataset.json", "triple-dataset.json", "quad-dataset.json",
           "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10, train_steps=8000, training_rows=384000, model_forward_calls=9620,
            row_presentations=539520, core_forward_calls=38480, checkpoint_bundle_loads=1,
            model_state_loads=10, new_checkpoint_writes=1, network_calls=0)
TOL = 1e-9
MANIFEST_SHA = "3d0ecd3f4785967a88e8b84597d9615be79eb7e609c348bf2ca1cdead8cbe94e"


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
    from fold_lm.v05_benchmarks import model_c285_saved_length_transfer_audit as parent
    previous, c = parent.context()
    transfer, training, _ = previous.context()
    return parent, previous, transfer, training, c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION, parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
                summary_sha256=list(SUMMARY_SHAS), parent_artifacts={k:list(v) for k,v in PARENT_ARTIFACTS.items()},
                seeds=list(SEEDS), arms=list(ARMS), parameters=14256, max_tokens=48,
                architecture="actual C278 all-token MeanFinalDualReadout in both arms",
                changed="LR applied before updates401..800 only; identical mixed2/3 examples and800 updates",
                lr_rule="1-based s:constant=.005;candidate s<=400:.005;else .0005+.0045*(1+cos(pi*(s-400)/400))/2",
                common_prefix="paired initial and step400 fingerprints plus first400 losses must match exactly",
                schedule="200 epochs x4;randperm96(seed+286000+epoch);24 query pairs/batch;profile=epoch%3;length=epoch%2",
                length_profile_updates=[[136,132,132],[132,136,132]], per_length_row_exposures=[100,100],
                logical_row_exposures=200, train_tables=[2,3,192,48], fit_rng="seed+287000 reset per arm",
                data_sha256="1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
                triple_sha256="432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",
                quad_sha256="86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b",
                optimizer="AdamW", betas=[.9,.999], eps=1e-8, weight_decay=0., clip=1., loss="mean CE only",
                primary="all five cosine_tail states pass every four-character fixed criterion; control separate",
                descriptive="two/three/all-task gates and180 paired contrasts; no automatic superiority",
                limitation="C285 does not establish an optimizer cause;no new length/data/architecture;no automatic Gate F",
                gate=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
                source_pins=562, protected_inputs=1001, dependency_union=62, own_tests=40,
                modules=171, loaded_tests=4086, focused_tests=4085, excluded_test=EXCLUDED,
                dtype="CPU float64", threads=2, deterministic=True, replay_tolerance=TOL,
                gate_f_candidate=False, production_adoption=False, arbitrary_length_claim=False, **WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None, "manifest not sealed")
    require(digest(manifest()) == MANIFEST_SHA, "manifest digest mismatch")


def learning_rates(arm):
    require(arm in ARMS, "LR arm")
    return [.005 if arm == ARMS[0] or s <= 400 else .0005 + .0045*(1+math.cos(math.pi*(s-400)/400))/2
            for s in range(1,801)]


def schedule(seed, rows):
    require(seed in SEEDS and len(rows) == 192, "schedule identity")
    groups = {}
    for i,r in enumerate(rows):
        k = (r["language"], tuple(r["entities"]), tuple(r["values"]), tuple(r["permutation"]))
        groups.setdefault(k, []).append(i)
    pairs = []
    for k in sorted(groups):
        ids = sorted(groups[k], key=lambda i:rows[i]["query"])
        require(len(ids) == 2 and [rows[i]["query"] for i in ids] == list(k[1]), "complete query pair")
        require(rows[ids[0]]["target"] != rows[ids[1]]["target"], "distinct targets")
        pairs.append(ids)
    require(len(pairs) == 96 and sorted(sum(pairs, [])) == list(range(192)), "pair partition")
    pairs = torch.tensor(pairs, dtype=torch.int64)
    batches, profiles, lengths = [], [], []
    for epoch in range(200):
        order = torch.randperm(96, generator=torch.Generator().manual_seed(seed+286000+epoch))
        for block in range(4):
            batches.append(pairs[order[block*24:(block+1)*24]].flatten())
            profiles.append(epoch%3); lengths.append(epoch%2)
    x,p,l = torch.stack(batches),torch.tensor(profiles),torch.tensor(lengths)
    exposure = [torch.bincount(x[l==j].flatten(), minlength=192).tolist() for j in range(2)]
    lp = [[sum(a==j and b==k for a,b in zip(lengths,profiles,strict=True)) for k in range(3)] for j in range(2)]
    require(exposure == [[100]*192,[100]*192] and lp == manifest()["length_profile_updates"], "exposure")
    return x,p,l,dict(logical_batch_sha256=digest(x.tolist()), rendering_sha256=digest([profiles,lengths]),
                      per_length_row_exposures=exposure, length_profile_updates=lp)


def make_models(seed, c):
    require(seed in SEEDS, "model seed")
    control = c.c278.MeanFinalDualReadout(c.factory.new_model(seed), seed, c.reader, c.c269.query_span_mask)
    candidate = copy.deepcopy(control)
    require(type(control) is type(candidate) is c.c278.MeanFinalDualReadout, "architecture")
    require(all(sum(p.numel() for p in m.parameters()) == 14256 for m in (control,candidate)), "capacity")
    require(all(p.dtype == torch.float64 for m in (control,candidate) for p in m.parameters()), "precision")
    require(list(control.state_dict()) == list(candidate.state_dict())
            and c.base.fingerprint(control) == c.base.fingerprint(candidate), "matched initial state")
    require(all(a.data_ptr() != b.data_ptr() for a,b in zip(control.parameters(),candidate.parameters(),strict=True)), "storage")
    return dict(zip(ARMS,(control,candidate),strict=True))


def fit(model, data, tokens, targets, seed, arm, c):
    require(tokens.shape == (2,3,192,48) and targets.shape == (192,)
            and tokens.dtype == targets.dtype == torch.int64, "fit tables")
    ids,profiles,lengths,plan = schedule(seed,data["TRAIN"])
    rates = learning_rates(arm); observed,losses = [],[]
    torch.manual_seed(seed+287000)
    optimizer = torch.optim.AdamW(model.parameters(), lr=.005, betas=(.9,.999), eps=1e-8, weight_decay=0.)
    model.train(); midpoint = None
    for step in range(800):
        for group in optimizer.param_groups:
            group["lr"] = rates[step]
        require(len(optimizer.param_groups) == 1, "optimizer group count")
        observed.append(float(optimizer.param_groups[0]["lr"]))
        optimizer.zero_grad(set_to_none=True)
        logits = model(tokens[lengths[step],profiles[step],ids[step]], torch.zeros(48,dtype=torch.int64))
        loss = F.cross_entropy(logits,targets[ids[step]])
        require(bool(torch.isfinite(loss)), "nonfinite loss")
        losses.append(float(loss.detach()))
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True)
        optimizer.step()
        if step == 399:
            midpoint = c.base.fingerprint(model)
        if (step+1)%200 == 0:
            print(f"[C286] seed={seed} arm={arm} step={step+1}/800 lr={observed[-1]:.9g} ce={losses[-1]:.6f}",flush=True)
    model.eval()
    require(observed == rates and isinstance(midpoint,str), "applied LR history")
    return dict(steps=800,training_rows=38400,step400_sha256=midpoint,applied_lr=observed,
                lr_sha256=digest(observed),loss_history=losses,last_ce=losses[-1],**plan)


def train_one(model,data,triple,quad,tokens,targets,seed,arm,previous,transfer,c):
    initial = c.base.fingerprint(model)
    back,head = c.base.fingerprint(model.backbone),c.base.fingerprint(model.read)
    with c.p267.counted(model,c.core) as (calls,cores):
        fitted = fit(model,data,tokens,targets,seed,arm,c)
        final = c.base.fingerprint(model); model.requires_grad_(False)
        raw = previous.evaluate(model,data,triple,quad,transfer,c)
    require(calls == [881,46176] and cores[0] == 3524, "train/eval workload")
    require(initial != final and back != c.base.fingerprint(model.backbone)
            and head != c.base.fingerprint(model.read) and c.base.fingerprint(model) == final, "weights")
    record = dict(seed=seed,arm=arm,parameters=14256,initial_sha256=initial,final_sha256=final,weights_changed=True,
                  fit=fitted,raw=raw,forward_calls=881,row_presentations=46176,core_forward_calls=3524)
    return record,{k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def analyze(records,data,transfer,c):
    require([(r["seed"],r["arm"]) for r in records] == identities(), "record identities")
    metrics,results,contrasts = [],[],[]
    for r in records:
        require(r["parameters"] == 14256 and r["weights_changed"] is True and r["checkpoint_roundtrip"] is True, "record integrity")
        error = r["reload_max_error"]
        require(type(error) in (int,float) and math.isfinite(error) and 0 <= error <= TOL, "replay error")
        keys = ("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in keys) and tuple(r[k] for k in keys) == (881,46176,3524,81,7776,324), "record workload")
        fitted = r["fit"]; plan = schedule(r["seed"],data["TRAIN"])[3]; rates = learning_rates(r["arm"])
        require(fitted["steps"] == 800 and fitted["training_rows"] == 38400 and all(fitted[k] == v for k,v in plan.items()), "fit plan")
        require(fitted["applied_lr"] == rates and fitted["lr_sha256"] == digest(rates), "LR history")
        require(len(fitted["loss_history"]) == 800 and all(type(v) in (int,float) and math.isfinite(v) and v >= 0 for v in fitted["loss_history"]), "loss history")
        require(fitted["last_ce"] == fitted["loss_history"][-1] and re.fullmatch(r"[0-9a-f]{64}",fitted["step400_sha256"]) is not None, "fit summary")
        require(set(r["raw"]) == set(TASKS), "raw tasks")
        scored = dict(two_char=c.p267.score(data,r["raw"]["two_char"]),triple=c.c270.score(data,r["raw"]["triple"],c.p267),
                      quad=transfer.score_quad(data,r["raw"]["quad"],c))
        require(all(type(v["passed"]) is bool for v in scored.values()), "task flags")
        flags = {t+"_pass":scored[t]["passed"] for t in TASKS}
        results.append(dict(seed=r["seed"],arm=r["arm"],passed=flags["quad_pass"],all_tasks_pass=all(flags.values()),**flags))
        metrics.append(dict(seed=r["seed"],arm=r["arm"],**scored))
    for i in range(0,10,2):
        a,b = records[i:i+2]
        require(a["initial_sha256"] == b["initial_sha256"] and a["fit"]["logical_batch_sha256"] == b["fit"]["logical_batch_sha256"], "matched initial/batches")
        require(a["fit"]["step400_sha256"] == b["fit"]["step400_sha256"]
                and a["fit"]["loss_history"][:400] == b["fit"]["loss_history"][:400], "common first400 prefix")
        for task in TASKS:
            for x,y in zip(metrics[i][task]["totals"],metrics[i+1][task]["totals"],strict=True):
                require(all(x[k] == y[k] for k in ("split","profile","language","rows","pairs")), "contrast identity")
                contrasts.append(dict(task=task,seed=a["seed"],**{k:x[k] for k in ("split","profile","language","rows","pairs")},
                                      control_correct=x["correct"],candidate_correct=y["correct"],
                                      control_collapsed=x["collapsed_pairs"],candidate_collapsed=y["collapsed_pairs"]))
    require(len(contrasts) == 180, "contrast count")
    summary = dict(seed_results=results,contrasts=contrasts,all_replays=True,all_pairs_matched=True,all_prefixes_matched=True,
                   candidate_gate=all(r["quad_pass"] for r in results if r["arm"] == ARMS[1]),**WORK)
    for out,field in (("seed_pass_counts","passed"),("two_char_pass_counts","two_char_pass"),("triple_pass_counts","triple_pass"),
                      ("quad_pass_counts","quad_pass"),("all_tasks_pass_counts","all_tasks_pass")):
        summary[out] = {a:sum(r[field] for r in results if r["arm"] == a) for a in ARMS}
    return metrics,summary


def load_parent(paths):
    parent,_,_,_,c = context(); paths = [Path(p).resolve() for p in paths]
    require(len(paths) == 12 and all(c.audit.sha(p) == s for p,s in zip(paths,SUMMARY_SHAS,strict=True)), "parent hashes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C286 parent forbids neural calls")), \
         patch.object(torch.nn.Module,"load_state_dict",side_effect=RuntimeError("C286 parent forbids state loading")), \
         patch.object(torch,"save",side_effect=RuntimeError("C286 parent forbids writes")):
        payload,_ = parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION)
    parent.validate_result(payload)
    require(payload["commit_sha"] == PARENT_EXECUTION and payload["status"] == "PASS"
            and payload["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "parent identity/source")
    actual = {a["file"]:(a["sha256"],a["serialized_bytes"]) for a in payload["artifacts"]}
    require(len(payload["artifacts"]) == 3 and actual == PARENT_ARTIFACTS, "parent artifacts")
    s = payload["validation_summary"]
    require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False and s["model_forward_calls"] == 0, "parent scope")
    q = s["primary"]["triple_to_quad"]["mixed_length"]["criteria"]["accuracy"]
    require((q["both_fail"],q["left_pass_right_fail"],q["right_fail"]) == (37,6,43), "parent deciding metric")
    return payload


def precheck(paths,root):
    validate_seal(); payload = load_parent(paths); _,_,_,_,c = context()
    root,p = Path(root),Path(paths[0]).resolve()
    pins,protected = dict(payload["source_blobs"]),dict(payload["input_sha256"])
    for n,w in pins.items(): require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip() == w, "changed source:"+n)
    for n,w in protected.items(): require(Path(n).is_file() and c.audit.sha(n) == w, "changed input:"+n)
    for child,w in [(p,SUMMARY_SHAS[0])] + [(c.audit.safe_child(p.parent,n),v[0]) for n,v in PARENT_ARTIFACTS.items()]:
        require(str(child.resolve()) not in protected and c.audit.sha(child) == w, "parent input")
        protected[str(child.resolve())] = w
    for n in OWN:
        require(n not in pins, "OWN collision"); pins[n] = c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9]|27[0-9]|28[0-5])_[^/]+)\.py"
    deps = set(c.factory.LM_SOURCES) | {n for n in payload["source_blobs"] if re.fullmatch(pattern,n)} | {OWN[0]}
    require(len(deps) == manifest()["dependency_union"] and deps <= set(pins), "dependency coverage")
    require(pins.get(PARENT_SOURCE) == PARENT_BLOB, "direct parent pin")
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected)) == (562,1001), "protection cardinality")
    print(f"registration_check = source_pins:{len(pins)}; protected_inputs:{len(protected)}; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["diagnostic_execution_valid"] is True, "identity")
    require(all(p[k] is False for k in ("gate_f_candidate","production_adoption","arbitrary_length_claim")), "scope")
    require((len(p["source_blobs"]),len(p["input_sha256"])) == (562,1001) and set(OWN) <= set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "protection")
    require(len(p["artifacts"]) == 8 and {a["file"] for a in p["artifacts"]} == set(OUTPUTS), "artifacts")
    s = p["validation_summary"]; rr = s["seed_results"]
    require(all(type(s[k]) is int and s[k] == v for k,v in WORK.items()), "workload")
    require([(r["seed"],r["arm"]) for r in rr] == identities(), "results")
    require(all(type(r[k]) is bool for r in rr for k in ("passed","two_char_pass","triple_pass","quad_pass","all_tasks_pass")), "flags")
    require(all(r["passed"] is r["quad_pass"] and r["all_tasks_pass"] is all(r[t+"_pass"] for t in TASKS) for r in rr), "primary/descriptive")
    for out,field in (("seed_pass_counts","passed"),("two_char_pass_counts","two_char_pass"),("triple_pass_counts","triple_pass"),
                      ("quad_pass_counts","quad_pass"),("all_tasks_pass_counts","all_tasks_pass")):
        require(s[out] == {a:sum(r[field] for r in rr if r["arm"] == a) for a in ARMS}, "pass counts")
    gate = all(r["quad_pass"] for r in rr if r["arm"] == ARMS[1])
    require(s["candidate_gate"] is gate and p["status"] == ("PASS" if gate else "FAIL"), "candidate gate")
    require(s["all_replays"] is True and s["all_pairs_matched"] is True and s["all_prefixes_matched"] is True
            and len(s["contrasts"]) == 180, "replay/prefix/contrasts")


def load_bundle(path):
    v = torch.load(path,map_location="cpu",weights_only=True)
    require(set(v) == {"schema","identities","states"} and v["schema"] == "fold-c286-cosine-tail-models-v1"
            and v["identities"] == [list(i) for i in identities()] and len(v["states"]) == 10, "bundle")
    return v["states"]


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == manifest()["modules"]-1, "parent modules")
    return names + ["tests_lm.test_v05_c286_cosine_tail_stability"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) == manifest()["loaded_tests"] and ids.count(EXCLUDED) == 1, "loaded suite")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require(len(kept) == manifest()["focused_tests"], "focused suite")
    return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip() == head
            and c.audit.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(), "repository guard")


def run(*,summaries,output_dir,expected_head):
    _,previous,transfer,training,c = context(); root = Path(__file__).resolve().parents[2]
    guard(root,expected_head,c); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected = precheck(summaries,root)
    data = c.p267.dataset(); c.p267.validate_data(data)
    triple = c.c270.prompt_dataset(data,c.p267); c.c270.validate_dataset(triple,data,c.p267)
    quad = transfer.dataset(data); transfer.validate_dataset(quad,data,c)
    tokens,targets = training.training_tables(data,c)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False); records,states = [],[]
    for seed in SEEDS:
        models = make_models(seed,c)
        for arm in ARMS:
            print(f"[C286] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            r,state = train_one(models[arm],data,triple,quad,tokens,targets,seed,arm,previous,transfer,c)
            records.append(r); states.append(state)
    torch.save(dict(schema="fold-c286-cosine-tail-models-v1",identities=[list(i) for i in identities()],states=states),out/"trained-models.pt")
    states = load_bundle(out/"trained-models.pt")
    for i,seed in enumerate(SEEDS):
        models = make_models(seed,c)
        for j,arm in enumerate(ARMS):
            k = 2*i+j
            previous.replay_one(models[arm],states[k],records[k],data,triple,quad,transfer,c)
    metrics,summary = analyze(records,data,transfer,c)
    torch.save(dict(schema="fold-c286-cosine-tail-eval-v1",records=records),out/"evaluations.pt")
    for n,v in (("architecture-plan.json",manifest()),("dataset.json",data),("triple-dataset.json",triple),("quad-dataset.json",quad),
                ("measurements.json",metrics),("validation-summary.json",summary)):
        (out/n).write_bytes(blob(v))
    artifacts = [dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c); precheck(summaries,root)
    p = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
             diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
             gate_f_candidate=False,production_adoption=False,arbitrary_length_claim=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    print("=== C286 RESULT ===",flush=True); print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    _,_,transfer,_,c = context(); out = Path(outdir)
    p = c.audit.read_json(out/"summary.json"); validate_result(p); require(p["commit_sha"] == expected_head, "execution HEAD")
    for n,w in p["input_sha256"].items(): require(c.audit.sha(n) == w, "protected input")
    for a in p["artifacts"]:
        child = c.audit.safe_child(out,a["file"])
        require(c.audit.sha(child) == a["sha256"] and child.stat().st_size == a["serialized_bytes"], "output bytes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("C286 postcheck forbids neural calls")):
        load_parent(summaries)
        data = c.audit.read_json(out/"dataset.json"); c.p267.validate_data(data)
        c.c270.validate_dataset(c.audit.read_json(out/"triple-dataset.json"),data,c.p267)
        transfer.validate_dataset(c.audit.read_json(out/"quad-dataset.json"),data,c)
        v = torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(v) == {"schema","records"} and v["schema"] == "fold-c286-cosine-tail-eval-v1", "eval schema")
        metrics,summary = analyze(v["records"],data,transfer,c)
        for n,value in (("architecture-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):
            require(c.audit.read_json(out/n) == value, "persisted:"+n)
    require(p["validation_summary"] == summary, "summary reconstruction")
    return p,metrics


def main():
    p = argparse.ArgumentParser(); p.add_argument("--summaries",nargs=12,type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True); p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__ == "__main__": main()
