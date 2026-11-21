"""C308: core-only learning-rate attenuation with concurrent full/frozen controls."""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
from types import ModuleType
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C308-v5b-core-learning-rate"
STAGE = "V5-B-CORE-LEARNING-RATE"
BASE = "49bf2b96faa9afcee97bbce3840e1164b498fcd8"
PARENT_EXECUTION = "4371ad8de650261f6cdacacfd9972efcdbe970a8"
PARENT_SHA = "5cb0683de649361966f2ab549aeab94d20643d64fe68d1d8bbe3497e6d637e42"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c307_core_freeze_replication.py"
PARENT_BLOB = "02cb0d743391ef1424b537159c824c5e2bc5209b"
WIDE_SOURCE = "fold_lm/v05_benchmarks/model_c304_length_breadth.py"
WIDE_BLOB = "cacb5852a29171aa8079e634d929fdd54e7f4f58"
SEEDS = tuple(range(308001, 308006))
ORDERS = tuple(range(308101, 308106))
ARMS = ("full_train", "core_frozen", "core_slow")
LENGTHS = (2, 3, 4, 5)
STEPS, SLOTS, FIT_RNG = 1200, 64, 612000
BASE_LR, CORE_LR = .005, .0005
OWN = ("fold_lm/v05_benchmarks/model_c308_core_learning_rate.py",
       "tests_lm/test_v05_c308_core_learning_rate.py", "tools/run_c308.ps1", "tools/invoke_c308.ps1",
       "docs/experiment-ledger-addendum-c308-preregistration.md", "docs/v5b-core-learning-rate-v0.1.md")
OUTPUTS = ("architecture-plan.json", "dataset.json", "length-datasets.json", "trained-models.pt",
           "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=15, train_steps=18000, training_rows=864000, model_forward_calls=21240,
            row_presentations=1175040, core_forward_calls=84960, model_state_loads=15,
            checkpoint_bundle_loads=1, new_checkpoint_writes=1, network_calls=0)
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
PROMPTS_SHA = "ecf2c9784213ac8fcebfd9ac03bea42317629edcea330771c92c72d71777583d"
MANIFEST_SHA = "c13d8d4ed974f977840e7cc1d84d5d60e3bfc78bdbc9384ff1f5d4906f65210f"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS, ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c307_core_freeze_replication as parent
    return (parent, *parent.context())


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
        wide_source=WIDE_SOURCE, wide_blob=WIDE_BLOB, seeds=list(SEEDS), orders=list(ORDERS), arms=list(ARMS),
        question="does nominal core LR one tenth of noncore LR improve unseen-five reliability versus both full training and freezing",
        train_lengths=[2, 3, 4], eval_lengths=list(LENGTHS), slots=SLOTS, parameters=14256, core_parameters=3328,
        trainable_parameters=dict(full_train=14256, core_frozen=10928, core_slow=14256),
        noncore_lr=BASE_LR, core_lr=dict(full_train=BASE_LR, core_frozen=None, core_slow=CORE_LR),
        frozen_policy="exclude core from optimizer and requires_grad;retain core forward and input backward",
        slow_policy="all weights train;two disjoint AdamW groups;scale optimizer step NOT gradient before clipping",
        clip_order="all trainable parameters in original named-parameter order;global norm1 before AdamW",
        optimizer="AdamW", betas=[.9, .999], eps=1e-8, weight_decay=0., steps=STEPS, loss="ordinary mean CE",
        schedule="300epochs*4;randperm96(order+306000+epoch);length=2+epoch%3;profile=(epoch//3+epoch%3)%3",
        fit_rng=FIT_RNG, per_row_length_exposure=[100, 100, 100], profile_updates=[400]*3,
        dataset_sha256=DATA_SHA, prompts_sha256=PROMPTS_SHA,
        primary="all5 NEW core_slow models pass every original five-character local/masked criterion",
        gates=dict(accuracy=.90, query_pair=.80, evidence_drop=.35, query_drop=.35, two_order=.80),
        limits="prospective fixed ratio,not optimal ratio or mechanism proof;new seeds not new tasks;frozen capacity/backward differs",
        reports="15 seed results,120 partitions,80 candidate-versus-controls count contrasts,15 gradient summaries,2 paired-five contingencies",
        parents=34, source_pins=694, protected_inputs=1295, own_tests=32, modules=193, loaded_tests=4878, focused_tests=4877,
        excluded_test=EXCLUDED, dtype="CPU float64", threads=2, deterministic=True,
        gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None and digest(manifest()) == MANIFEST_SHA, "manifest seal")


def configure(model, arm):
    require(arm in ARMS, "arm")
    model.requires_grad_(True)
    if arm == "core_frozen":
        model.backbone.core.requires_grad_(False)
    return model


def make_models(seed, wide, c):
    require(seed in SEEDS, "seed")
    reference = c.c278.MeanFinalDualReadout(c.factory.new_model(seed), seed, c.reader, c.c269.query_span_mask)
    template = wide.LengthReadout(reference)
    models = {arm: configure(copy.deepcopy(template), arm) for arm in ARMS}
    used = set()
    for arm, model in models.items():
        require(type(model) is wide.LengthReadout and model.backbone.config.max_tokens == SLOTS
                and model.backbone.core.config.slots == SLOTS, "architecture/frame")
        require(sum(p.numel() for p in model.parameters()) == 14256
                and sum(p.numel() for p in model.backbone.core.parameters()) == 3328, "capacity")
        require(c.base.fingerprint(model) == c.base.fingerprint(reference) and list(model.state_dict()) == list(reference.state_dict()), "initial state")
        require(all(p.dtype == torch.float64 and p.device.type == "cpu" for p in model.parameters()), "precision")
        ptrs = {p.data_ptr() for p in model.parameters()}
        require(not ptrs & used, "shared storage")
        used.update(ptrs)
        parameter_groups(model, arm)
    return models


def parameter_groups(model, arm):
    require(arm in ARMS, "arm")
    named = list(model.named_parameters())
    core_ids = {id(p) for p in model.backbone.core.parameters()}
    require(core_ids == {id(p) for n, p in named if n.startswith("backbone.core.")}, "core boundary")
    require(all(p.requires_grad == (arm != "core_frozen" or id(p) not in core_ids) for _, p in named), "gradient policy")
    active = [p for _, p in named if p.requires_grad]
    require(sum(p.numel() for p in active) == manifest()["trainable_parameters"][arm], "trainable count")
    if arm != "core_slow":
        return [dict(params=active, lr=BASE_LR)]
    return [dict(params=[p for _, p in named if id(p) not in core_ids], lr=BASE_LR),
            dict(params=[p for _, p in named if id(p) in core_ids], lr=CORE_LR)]


def optimizer_for(model, arm):
    return torch.optim.AdamW(parameter_groups(model, arm), lr=BASE_LR, betas=(.9, .999), eps=1e-8, weight_decay=0.)


def verify_optimizer(optimizer, model, arm):
    expected = parameter_groups(model, arm)
    require(len(optimizer.param_groups) == len(expected), "optimizer groups")
    for group, wanted in zip(optimizer.param_groups, expected, strict=True):
        require([id(p) for p in group["params"]] == [id(p) for p in wanted["params"]]
                and group["lr"] == wanted["lr"] and group["betas"] == (.9, .999)
                and group["eps"] == 1e-8 and group["weight_decay"] == 0., "optimizer policy")


def schedule(seed, rows, pairs):
    require(seed in SEEDS and len(rows) == 192, "schedule identity")
    pp = pairs.pairs_from_rows(rows)
    require(pp.dtype == torch.int64 and pp.shape == (96, 2) and sorted(pp.flatten().tolist()) == list(range(192)), "pair partition")
    for a, b in pp.tolist():
        require(rows[a]["target"] != rows[b]["target"] and {rows[a]["query"], rows[b]["query"]} == set(rows[a]["entities"])
                and all(rows[a][k] == rows[b][k] for k in ("entities", "values", "permutation", "language")), "intact pair")
    events = torch.empty((STEPS, 24, 4), dtype=torch.int64)
    order = ORDERS[SEEDS.index(seed)]
    for epoch in range(300):
        perm = torch.randperm(96, generator=torch.Generator().manual_seed(order+306000+epoch))
        for j in range(4):
            events[4*epoch+j, :, 0] = epoch % 3
            events[4*epoch+j, :, 1] = (epoch//3+epoch%3) % 3
            events[4*epoch+j, :, 2:] = pp[perm[24*j:24*(j+1)]]
    return events


def first_batch_probe(models, tokens, targets, events, p306):
    freeze = p306.first_batch_probe({a: models[a] for a in ARMS[:2]}, tokens, targets, events)
    e = events[0]; ids = e[:, 2:].flatten()
    x = tokens[e[:, 0].repeat_interleave(2), e[:, 1].repeat_interleave(2), ids]
    results = []
    for arm in ("full_train", "core_slow"):
        model = copy.deepcopy(models[arm]); model.train(); model.zero_grad(set_to_none=True)
        optimizer = optimizer_for(model, arm); verify_optimizer(optimizer, model, arm)
        before = {n: p.detach().clone() for n, p in model.named_parameters()}
        z = model(x, torch.zeros(48, dtype=torch.int64)); F.cross_entropy(z, targets[ids]).backward()
        grads = {n: None if p.grad is None else p.grad.detach().clone() for n, p in model.named_parameters()}
        torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1., error_if_nonfinite=True)
        optimizer.step()
        delta = {n: p.detach()-before[n] for n, p in model.named_parameters()}
        results.append((z.detach(), grads, delta))
    (za, ga, da), (zb, gb, db) = results
    require(torch.equal(za, zb) and ga.keys() == gb.keys(), "initial full/slow output")
    max_step_error = 0.
    for name, gradient in ga.items():
        require((gradient is None) == (gb[name] is None), "gradient connectivity")
        if gradient is not None:
            require(torch.equal(gradient, gb[name]), "initial full/slow gradient:"+name)
        factor = CORE_LR/BASE_LR if name.startswith("backbone.core.") else 1.
        error = float((db[name]-factor*da[name]).abs().max())
        require(error <= 1e-12, "first-step LR application:"+name)
        max_step_error = max(max_step_error, error)
    return dict(freeze_probe=freeze, full_slow_initial_logits_equal=True, full_slow_preclip_gradients_equal=True,
                first_step_scaled_core_delta_max_error=max_step_error, discarded_probe_updates=2)


def fit(model, data, tokens, targets, seed, arm, pairs, wide):
    require(tokens.shape == (3, 3, 192, SLOTS) and tokens.dtype == targets.dtype == torch.int64, "training tables")
    require(torch.equal(targets, torch.tensor([r["target"] for r in data["TRAIN"]], dtype=torch.int64)), "target alignment")
    events = schedule(seed, data["TRAIN"], pairs); stats = wide.schedule_stats(events)
    torch.manual_seed(FIT_RNG); optimizer = optimizer_for(model, arm)
    active = [p for p in model.parameters() if p.requires_grad]
    losses, counts, union, rates = [], [], {}, []
    model.train()
    for step, e in enumerate(events):
        verify_optimizer(optimizer, model, arm)
        rates.append([g["lr"] for g in optimizer.param_groups])
        optimizer.zero_grad(set_to_none=True); ids = e[:, 2:].flatten()
        z = model(tokens[e[:, 0].repeat_interleave(2), e[:, 1].repeat_interleave(2), ids], torch.zeros(48, dtype=torch.int64))
        require(z.shape == (48, 256) and z.dtype == torch.float64 and bool(torch.isfinite(z).all()), "logits")
        loss = F.cross_entropy(z, targets[ids]); require(bool(torch.isfinite(loss)), "finite loss")
        losses.append(float(loss.detach())); loss.backward()
        received = {n: p.numel() for n, p in model.named_parameters() if p.grad is not None}
        require(arm != "core_frozen" or not any(n.startswith("backbone.core.") for n in received), "frozen core gradient")
        union.update(received); counts.append(sum(received.values()))
        torch.nn.utils.clip_grad_norm_(active, 1., error_if_nonfinite=True); optimizer.step()
        if (step+1) % 200 == 0:
            print(f"[C308] seed={seed} arm={arm} step={step+1}/1200 ce={losses[-1]:.6f} lr={rates[-1]}", flush=True)
    model.eval()
    return dict(steps=STEPS, training_rows=57600, optimizer_creations=1, fit_rng=FIT_RNG,
        trainable_parameters=sum(p.numel() for p in active), optimizer_group_lrs=rates, ce_history=losses,
        gradient_parameter_counts=counts, gradient_union=dict(sorted(union.items())), schedule_events=events, **stats)


def check_fit(f, seed, arm, data, pairs, wide):
    expected = dict(steps=STEPS, training_rows=57600, optimizer_creations=1, fit_rng=FIT_RNG,
                    trainable_parameters=manifest()["trainable_parameters"][arm])
    require(all(type(f[k]) is int and f[k] == v for k, v in expected.items()), "fit metadata")
    events = schedule(seed, data["TRAIN"], pairs); stats = wide.schedule_stats(events)
    require(torch.equal(events, f["schedule_events"]) and all(f[k] == v for k, v in stats.items()), "schedule reconstruction")
    require(f["per_length_row_exposures"] == [[100]*192 for _ in range(3)]
            and [sum(r[i] for r in f["length_profile_updates"]) for i in range(3)] == [400]*3, "exposure")
    wanted = [BASE_LR, CORE_LR] if arm == "core_slow" else [BASE_LR]
    require(f["optimizer_group_lrs"] == [wanted]*STEPS, "fixed LR history")
    require(len(f["ce_history"]) == STEPS and all(type(v) in (int, float) and math.isfinite(v) and v >= 0 for v in f["ce_history"]), "loss trace")
    union = f["gradient_union"]
    require(union and all(type(n) is str and type(v) is int and v > 0 for n, v in union.items()), "gradient union")
    require(sum(union.values()) <= expected["trainable_parameters"] and len(f["gradient_parameter_counts"]) == STEPS
            and all(type(v) is int and 0 < v <= sum(union.values()) for v in f["gradient_parameter_counts"]), "gradient counts")
    if arm == "core_frozen":
        require(not any(n.startswith("backbone.core.") for n in union), "frozen gradient union")


def train_one(model, data, prompts, tokens, targets, seed, arm, pairs, wide, c):
    initial = c.base.fingerprint(model); core_initial = c.base.fingerprint(model.backbone.core)
    with c.p267.counted(model, c.core) as (calls, cores):
        fitted = fit(model, data, tokens, targets, seed, arm, pairs, wide)
        final = c.base.fingerprint(model); core_final = c.base.fingerprint(model.backbone.core)
        model.requires_grad_(False); raw = wide.evaluate(model, prompts, data, c)
    require(calls == [1308, 67968] and cores[0] == 5232, "train/evaluation counts")
    require(initial != final and c.base.fingerprint(model) == final and ((core_initial == core_final) == (arm == "core_frozen")), "core/final state")
    return dict(seed=seed, arm=arm, parameters=14256, slots=SLOTS, initial_sha256=initial, final_sha256=final,
        core_initial_sha256=core_initial, core_final_sha256=core_final, fit=fitted, raw=raw,
        forward_calls=1308, row_presentations=67968, core_forward_calls=5232), {n: p.detach().cpu().clone() for n, p in model.state_dict().items()}


def paired_outcomes(results, control):
    require(control in ARMS[:2] and [(r["seed"], r["arm"]) for r in results] == identities(), "paired cohort")
    counts = dict(both_pass=0, control_only=0, candidate_only=0, both_fail=0)
    for seed in SEEDS:
        a, b = [next(r["quint_pass"] for r in results if (r["seed"], r["arm"]) == (seed, arm)) for arm in (control, "core_slow")]
        require(type(a) is bool and type(b) is bool, "paired flags")
        counts["both_pass" if a and b else "control_only" if a else "candidate_only" if b else "both_fail"] += 1
    return counts


def analyze(records, data, pairs, wide, diag, c):
    require([(r["seed"], r["arm"]) for r in records] == identities(), "record cohort")
    metrics, parts, results = [], [], []
    for r in records:
        arm = r["arm"]; check_fit(r["fit"], r["seed"], arm, data, pairs, wide)
        require(r["parameters"] == 14256 and r["slots"] == SLOTS and r["initial_sha256"] != r["final_sha256"]
                and ((r["core_initial_sha256"] == r["core_final_sha256"]) == (arm == "core_frozen"))
                and r["checkpoint_roundtrip"] is True, "record state")
        e = r["reload_max_error"]; require(type(e) in (int, float) and math.isfinite(e) and 0 <= e <= 1e-9, "replay")
        fields = ("forward_calls", "row_presentations", "core_forward_calls", "replay_forward_calls", "replay_row_presentations", "replay_core_forward_calls")
        require(all(type(r[k]) is int for k in fields) and tuple(r[k] for k in fields) == (1308, 67968, 5232, 108, 10368, 432), "record work")
        require(set(r["raw"]) == set(map(str, LENGTHS)), "lengths")
        scored = {str(n): wide.score_length(data, r["raw"][str(n)], c) for n in LENGTHS}
        flags = {n: v["passed"] for n, v in scored.items()}; require(all(type(v) is bool for v in flags.values()), "flags")
        direct = {}
        for n in LENGTHS:
            normalized = diag.normalize_task(scored[str(n)], "triple", r["seed"], arm)
            for split in ("TRAIN", "HOLDOUT"):
                part = diag.partition([p for p in normalized if p["split"] == split]); direct[n, split] = part["direct_pass"]
                parts.append(dict(seed=r["seed"], arm=arm, identifier_length=n, split=split, length_trained=n<5, **part))
        results.append(dict(seed=r["seed"], arm=arm, length_pass=flags, quint_pass=flags["5"], all_lengths_pass=all(flags.values()),
            fitted_train_direct_pass=all(direct[n, "TRAIN"] for n in (2, 3, 4)), trained_length_holdout_direct_pass=all(direct[n, "HOLDOUT"] for n in (2, 3, 4))))
        metrics.append(dict(seed=r["seed"], arm=arm, length_scores=scored))
    for i in range(0, 15, 3):
        group = records[i:i+3]
        for key in ("initial_sha256", "core_initial_sha256"):
            require(len({r[key] for r in group}) == 1, "matched initial states")
        require(len({r["fit"]["event_sha256"] for r in group}) == 1 and len({r["fit"]["ce_history"][0] for r in group}) == 1, "matched training inputs")
    counts = {str(n): {a: sum(r["length_pass"][str(n)] for r in results if r["arm"] == a) for a in ARMS} for n in LENGTHS}
    contrasts = []
    for seed, n, split, control in itertools.product(SEEDS, LENGTHS, ("TRAIN", "HOLDOUT"), ARMS[:2]):
        a, b = [next(p for p in parts if (p["seed"], p["identifier_length"], p["split"], p["arm"]) == (seed, n, split, arm)) for arm in (control, "core_slow")]
        require(a["rows"] == b["rows"], "contrast rows")
        contrasts.append(dict(seed=seed, identifier_length=n, split=split, control=control, rows=a["rows"], control_correct=a["correct"], core_slow_correct=b["correct"]))
    return metrics, dict(seed_results=results, final_partitions=parts, contrasts=contrasts, length_pass_counts=counts,
        gradient_receivers=[dict(seed=r["seed"], arm=r["arm"], trainable=r["fit"]["trainable_parameters"], received_union=sum(r["fit"]["gradient_union"].values())) for r in records],
        paired_five={a: paired_outcomes(results, a) for a in ARMS[:2]}, candidate_gate=counts["5"]["core_slow"] == 5,
        all_groups_matched=True, all_replays=True, **WORK)


def expected_parent_flags():
    results = []
    for seed, arm in itertools.product(range(307001, 307006), ARMS[:2]):
        flags = {str(n): not ((arm == "full_train" and seed in (307002, 307005))
                             or (arm == "core_frozen" and (seed == 307005 or (seed == 307001 and n == 5)))) for n in LENGTHS}
        results.append(dict(seed=seed, arm=arm, length_pass=flags, quint_pass=flags["5"], all_lengths_pass=all(flags.values()),
            fitted_train_direct_pass=seed != 307005, trained_length_holdout_direct_pass=not (seed == 307005 or (seed == 307002 and arm == "full_train"))))
    return results


def parent_hashes():
    parent, p306, audit, wide, *_ = context()
    return (PARENT_SHA, parent.PARENT_SHA, p306.PARENT_SHA, audit.PARENT_SHA, *wide.parent_hashes(wide.context()[0]))


def load_parent(paths):
    parent, _, audit, wide, _, _, transfer, c = context(); paths = [Path(p).resolve() for p in paths]
    hashes = parent_hashes()
    require(len(paths) == len(hashes) == 34 and all(c.audit.sha(p) == h for p, h in zip(paths, hashes, strict=True)), "parent hashes")
    with audit.no_neural():
        p, _ = parent.verify_artifacts(paths[0].parent, paths[1:], PARENT_EXECUTION); parent.validate_result(p)
        require(p["experiment_id"] == "C307-v5b-core-freeze-replication" and p["commit_sha"] == PARENT_EXECUTION and p["status"] == "FAIL"
                and p["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB and p["source_blobs"].get(WIDE_SOURCE) == WIDE_BLOB, "parent identity")
        require(len(p["artifacts"]) == 7 and {a["file"] for a in p["artifacts"]} == set(OUTPUTS), "parent outputs")
        s = p["validation_summary"]
        require(s["seed_results"] == expected_parent_flags() and s["candidate_gate"] is False and s["all_pairs_matched"] is True
                and s["all_replays"] is True and s["paired_five"] == dict(both_pass=2, full_only=1, frozen_only=1, both_fail=1), "parent outcomes")
        data = c.audit.read_json(paths[0].parent/"dataset.json"); prompts = c.audit.read_json(paths[0].parent/"length-datasets.json")
        require(digest(data) == DATA_SHA and digest(prompts) == PROMPTS_SHA and prompts == wide.prompt_dataset(data), "data hashes/prompts")
        wide.validate_prompts(prompts, data, c, transfer)
    return p, data, prompts


def precheck(paths, root):
    validate_seal(); p, _, _ = load_parent(paths)
    parent, p306, audit, wide, pairs, diag, transfer, c = context(); root = Path(root).resolve()
    pins, protected = dict(p["source_blobs"]), dict(p["input_sha256"])
    require((len(pins), len(protected)) == (688, 1281) and pins.get(PARENT_SOURCE) == PARENT_BLOB and pins.get(WIDE_SOURCE) == WIDE_BLOB, "inherited protection")
    require(all(pins.get(n) == h for n, h in wide.PINNED.items()), "backend/scorer pins")
    for module in [parent, p306, audit, wide, pairs, diag, transfer, *parent.context(), *wide.context(), *vars(c).values(), c.factory.language_module()]:
        path = getattr(module, "__file__", None) if isinstance(module, ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            require(Path(path).resolve().relative_to(root).as_posix() in pins, "unprotected helper")
    for n, h in pins.items(): require(c.audit.git(root, "rev-parse", "HEAD:"+n).decode().strip() == h, "changed source:"+n)
    for n, h in protected.items(): require(Path(n).is_file() and c.audit.sha(n) == h, "changed input:"+n)
    directory = Path(paths[0]).resolve().parent
    for path, h in [(directory/"summary.json", PARENT_SHA)]+[(c.audit.safe_child(directory, a["file"]), a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path) == h, "parent input"); protected[str(path.resolve())] = h
    for n in OWN:
        require(n not in pins, "OWN collision"); pins[n] = c.audit.git(root, "rev-parse", "HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root, pins))
    require((len(pins), len(protected)) == (694, 1295), "protection counts")
    print(f"registration_check = source_pins:694; protected_inputs:1295; manifest_sha256:{MANIFEST_SHA}", flush=True)
    return pins, protected


def runtime_preflight(paths, root):
    precheck(paths, root); _, p306, _, wide, pairs, _, _, c = context(); _, data, _ = load_parent(paths)
    tokens, targets = wide.training_tables(data)
    for seed in SEEDS:
        require(wide.schedule_stats(schedule(seed, data["TRAIN"], pairs))["per_length_row_exposures"] == [[100]*192 for _ in range(3)], "real exposure")
    report = first_batch_probe(make_models(SEEDS[0], wide, c), tokens, targets, schedule(SEEDS[0], data["TRAIN"], pairs), p306)
    print("initial_gradient_and_optimizer_probe =", json.dumps(report, sort_keys=True), flush=True)
    print("real_core_learning_rate_preflight = PASS; discarded operational probe only", flush=True)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["diagnostic_execution_valid"] is True
            and p["gate_f_candidate"] is False and p["production_adoption"] is False, "result identity")
    require((len(p["source_blobs"]), len(p["input_sha256"])) == (694, 1295) and set(OWN) <= set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB and p["source_blobs"].get(WIDE_SOURCE) == WIDE_BLOB, "result protection")
    require(len(p["artifacts"]) == 7 and {a["file"] for a in p["artifacts"]} == set(OUTPUTS), "outputs")
    s = p["validation_summary"]; results = s["seed_results"]
    require([(r["seed"], r["arm"]) for r in results] == identities(), "result cohort")
    for r in results:
        require(set(r["length_pass"]) == set(map(str, LENGTHS)) and all(type(v) is bool for v in r["length_pass"].values()), "length flags")
        require(r["quint_pass"] is r["length_pass"]["5"] and r["all_lengths_pass"] is all(r["length_pass"].values()), "derived flags")
        require(type(r["fitted_train_direct_pass"]) is bool and type(r["trained_length_holdout_direct_pass"]) is bool, "direct flags")
    counts = {str(n): {a: sum(r["length_pass"][str(n)] for r in results if r["arm"] == a) for a in ARMS} for n in LENGTHS}
    gate = counts["5"]["core_slow"] == 5
    require(s["length_pass_counts"] == counts and s["candidate_gate"] is gate and p["status"] == ("PASS" if gate else "FAIL"), "fixed gate")
    require(s["paired_five"] == {a: paired_outcomes(results, a) for a in ARMS[:2]} and s["all_groups_matched"] is True and s["all_replays"] is True, "matching")
    require((len(s["final_partitions"]), len(s["contrasts"]), len(s["gradient_receivers"])) == (120, 80, 15), "inventory")
    require(all(type(s[k]) is int and s[k] == v for k, v in WORK.items()), "workload")


def load_bundle(path):
    p = torch.load(path, map_location="cpu", weights_only=True)
    require(set(p) == {"schema", "identities", "states"} and p["schema"] == "fold-c308-core-lr-models-v1"
            and p["identities"] == [list(i) for i in identities()] and len(p["states"]) == 15, "bundle schema")
    return p["states"]


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite): yield from flatten(test)
        else: yield test


def regression_modules(root):
    names = context()[0].regression_modules(root); require(len(names) == len(set(names)) == 192, "parent modules")
    return names+["tests_lm.test_v05_c308_core_learning_rate"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) == 4878 and ids.count(EXCLUDED) == 1, "loaded suite")
    kept = [t for t in tests if t.id() != EXCLUDED]; require(len(kept) == 4877, "focused suite")
    return unittest.TestSuite(kept)


def guard(root, head, c):
    require(c.audit.git(root, "rev-parse", "HEAD").decode().strip() == head
            and c.audit.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss"
            and not c.audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "repository guard")


def run(*, summaries, output_dir, expected_head):
    _, _, _, wide, pairs, diag, _, c = context(); root = Path(__file__).resolve().parents[2]
    guard(root, expected_head, c); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins, protected = precheck(summaries, root); _, data, prompts = load_parent(summaries); tokens, targets = wide.training_tables(data)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False); records, states = [], []
    for seed in SEEDS:
        models = make_models(seed, wide, c)
        for arm in ARMS:
            print(f"[C308] model={len(records)+1}/15 seed={seed} arm={arm}", flush=True)
            r, state = train_one(models[arm], data, prompts, tokens, targets, seed, arm, pairs, wide, c); records.append(r); states.append(state)
    torch.save(dict(schema="fold-c308-core-lr-models-v1", identities=[list(i) for i in identities()], states=states), out/"trained-models.pt")
    states = load_bundle(out/"trained-models.pt")
    for i, seed in enumerate(SEEDS):
        models = make_models(seed, wide, c)
        for j, arm in enumerate(ARMS):
            k = 3*i+j; wide.replay_one(models[arm], states[k], records[k], prompts, data, c)
    metrics, s = analyze(records, data, pairs, wide, diag, c)
    torch.save(dict(schema="fold-c308-core-lr-eval-v1", records=records), out/"evaluations.pt")
    for n, v in (("architecture-plan.json", manifest()), ("dataset.json", data), ("length-datasets.json", prompts),
                 ("measurements.json", metrics), ("validation-summary.json", s)): (out/n).write_bytes(blob(v))
    artifacts = [dict(file=n, sha256=c.audit.sha(out/n), serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root, expected_head, c); precheck(summaries, root)
    p = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head, status="PASS" if s["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True, source_blobs=pins, input_sha256=protected, artifacts=artifacts,
        validation_summary=s, gate_f_candidate=False, production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    receipt = {k: p[k] for k in ("experiment_id", "stage", "commit_sha", "status", "artifacts")}; receipt["summary_sha256"] = c.audit.sha(out/"summary.json")
    print("=== C308 COMPACT RESULT RECEIPT ===", flush=True); print(json.dumps(receipt, indent=2, sort_keys=True), flush=True)
    return p


def verify_artifacts(outdir, summaries, expected_head):
    _, _, audit, wide, pairs, diag, _, c = context(); out = Path(outdir)
    p = c.audit.read_json(out/"summary.json"); validate_result(p); require(p["commit_sha"] == expected_head, "execution HEAD")
    for n, h in p["input_sha256"].items(): require(c.audit.sha(n) == h, "protected input")
    for a in p["artifacts"]:
        path = c.audit.safe_child(out, a["file"]); require(c.audit.sha(path) == a["sha256"] and path.stat().st_size == a["serialized_bytes"], "output bytes")
    with audit.no_neural():
        _, data, prompts = load_parent(summaries)
        require(c.audit.read_json(out/"dataset.json") == data and c.audit.read_json(out/"length-datasets.json") == prompts, "persisted inputs")
        archive = torch.load(out/"evaluations.pt", map_location="cpu", weights_only=True)
        require(set(archive) == {"schema", "records"} and archive["schema"] == "fold-c308-core-lr-eval-v1", "evaluation schema")
        metrics, s = analyze(archive["records"], data, pairs, wide, diag, c)
        for n, v in (("architecture-plan.json", manifest()), ("measurements.json", metrics), ("validation-summary.json", s)):
            require(c.audit.read_json(out/n) == v, "persisted:"+n)
    require(p["validation_summary"] == s, "summary reconstruction")
    return p, metrics


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--summaries", nargs=34, type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True); parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
