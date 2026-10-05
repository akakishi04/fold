"""C307: preregistered fresh-seed replication of the C306 training policies."""
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

EXPERIMENT_ID = "C307-v5b-core-freeze-replication"
STAGE = "V5-B-CORE-FREEZE-REPLICATION"
BASE = "0012e1fb0d293cf2082c545c92ee2d7f5a6f8e01"
PARENT_EXECUTION = "cb2bb51a8beaa888c3a8b1fca382cd20536c923b"
PARENT_SHA = "5435cf83c02b75c2dd1d3c21105dcdf30e8c567c9d8672993f7676166515cff3"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c306_broad_length_core_freeze.py"
PARENT_BLOB = "5ca6ce358a7f6fe5fc3daf3c172289d6a4f0a786"
WIDE_SOURCE = "fold_lm/v05_benchmarks/model_c304_length_breadth.py"
WIDE_BLOB = "cacb5852a29171aa8079e634d929fdd54e7f4f58"
SEEDS = tuple(range(307001, 307006))
ORDERS = tuple(range(307101, 307106))
ARMS = ("full_train", "core_frozen")
LENGTHS = (2, 3, 4, 5)
STEPS, SLOTS, FIT_RNG, SHUFFLE_OFFSET = 1200, 64, 612000, 306000
OWN = ("fold_lm/v05_benchmarks/model_c307_core_freeze_replication.py",
       "tests_lm/test_v05_c307_core_freeze_replication.py", "tools/run_c307.ps1", "tools/invoke_c307.ps1",
       "docs/experiment-ledger-addendum-c307-preregistration.md", "docs/v5b-core-freeze-replication-v0.1.md")
OUTPUTS = ("architecture-plan.json", "dataset.json", "length-datasets.json", "trained-models.pt",
           "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10, train_steps=12000, training_rows=576000, model_forward_calls=14160,
            row_presentations=783360, core_forward_calls=56640, model_state_loads=10,
            checkpoint_bundle_loads=1, new_checkpoint_writes=1, network_calls=0)
DATA_SHA = "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1"
PROMPTS_SHA = "ecf2c9784213ac8fcebfd9ac03bea42317629edcea330771c92c72d71777583d"
MANIFEST_SHA = "9662b7d5763768a09c75c961dc8f8453c40506eadcbb44639bbd50f7dca2ab8b"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS, ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c306_broad_length_core_freeze as parent
    audit, wide, pairs, diag, transfer, c = parent.context()
    return parent, audit, wide, pairs, diag, transfer, c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_source=PARENT_SOURCE,
        parent_blob=PARENT_BLOB, wide_source=WIDE_SOURCE, wide_blob=WIDE_BLOB,
        question="does the C306 core-freeze advantage recur in a preregistered fresh paired seed cohort without policy retuning",
        seeds=list(SEEDS), orders=list(ORDERS), arms=list(ARMS), train_lengths=[2, 3, 4], eval_lengths=list(LENGTHS),
        slots=SLOTS, parameters=14256, trainable_parameters=dict(full_train=14256, core_frozen=10928), core_parameters=3328,
        changed_from_C306="initialization/order seed pairs ONLY;not a rerun of C306;no retained favorable seeds",
        intervention="only core requires_grad and optimizer membership;core forward and input backward remain",
        schedule="300epochs*4;randperm96(order+306000+epoch);length=2+epoch%3;profile=(epoch//3+epoch%3)%3",
        shuffle_offset=SHUFFLE_OFFSET, fit_rng=FIT_RNG, per_row_length_exposure=[100, 100, 100], profile_updates=[400]*3,
        steps=STEPS, loss="ordinary mean CE", optimizer="AdamW", lr=.005, betas=[.9, .999], eps=1e-8, weight_decay=0., clip=1.,
        dataset_sha256=DATA_SHA, prompts_sha256=PROMPTS_SHA,
        primary="all five NEW core_frozen states pass every unchanged five-character local/masked criterion",
        gate=dict(accuracy=.90, query_pair=.80, evidence_drop=.35, query_drop=.35, two_order=.80),
        replication_reporting="separate new-cohort control/candidate;paired wins/losses/ties and all errors;no pooled replacement for either gate",
        reports="10 seed results,80 partitions,40 count contrasts,10 gradient summaries,paired-five contingency",
        parents=33, source_pins=688, protected_inputs=1281, own_tests=32, modules=192, loaded_tests=4846, focused_tests=4845,
        excluded_test=EXCLUDED, dtype="CPU float64", threads=2, deterministic=True,
        limits="fresh random seeds,not fresh tasks or blinded external replication;five pairs cannot prove universal reliability",
        gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None and digest(manifest()) == MANIFEST_SHA, "manifest seal")


def expected_parent_flags():
    result = []
    for seed, arm in itertools.product(range(306001, 306006), ARMS):
        flags = {str(n): not ((arm == ARMS[0] and (seed == 306005 or (seed == 306002 and n >= 3)))
                             or (arm == ARMS[1] and seed == 306003 and n == 5)) for n in LENGTHS}
        result.append(dict(seed=seed, arm=arm, length_pass=flags, quint_pass=flags["5"], all_lengths_pass=all(flags.values()),
            fitted_train_direct_pass=not (arm == ARMS[0] and seed == 306005),
            trained_length_holdout_direct_pass=not (arm == ARMS[0] and seed in (306002, 306005))))
    return result


def verify_parent_policy(parent):
    p = parent.manifest()
    for key in ("arms", "train_lengths", "eval_lengths", "slots", "parameters", "trainable_parameters", "core_parameters",
                "per_row_length_exposure", "profile_updates", "fit_rng", "steps", "loss", "optimizer", "lr", "betas", "eps", "weight_decay", "clip"):
        require(p[key] == manifest()[key], "replication policy drift:" + key)
    require(parent.STEPS == STEPS and parent.SLOTS == SLOTS and parent.FIT_RNG == FIT_RNG
            and not set(SEEDS) & set(parent.SEEDS) and not set(ORDERS) & set(parent.ORDERS), "new cohort / fixed budget")


def make_models(seed, parent, wide, c):
    require(seed in SEEDS, "seed")
    reference = c.c278.MeanFinalDualReadout(c.factory.new_model(seed), seed, c.reader, c.c269.query_span_mask)
    template = wide.LengthReadout(reference)
    models = {a: parent.configure(copy.deepcopy(template), a) for a in ARMS}
    pointers = set()
    for arm, model in models.items():
        require(type(model) is wide.LengthReadout and model.backbone.config.max_tokens == SLOTS
                and model.backbone.core.config.slots == SLOTS, "architecture/frame")
        require(sum(p.numel() for p in model.parameters()) == 14256 and sum(p.numel() for p in model.backbone.core.parameters()) == 3328, "capacity")
        require(sum(p.numel() for p in model.parameters() if p.requires_grad) == manifest()["trainable_parameters"][arm], "trainable count")
        require(c.base.fingerprint(model) == c.base.fingerprint(reference) and list(model.state_dict()) == list(reference.state_dict()), "matched initial state")
        require(all(p.dtype == torch.float64 and p.device.type == "cpu" for p in model.parameters()), "precision")
        ptrs = {p.data_ptr() for p in model.parameters()}
        require(not ptrs & pointers, "shared storage")
        pointers.update(ptrs)
    return models


def schedule(seed, rows, pairs):
    require(seed in SEEDS and len(rows) == 192, "schedule identity")
    pp = pairs.pairs_from_rows(rows)
    require(pp.shape == (96, 2) and pp.dtype == torch.int64 and sorted(pp.flatten().tolist()) == list(range(192)), "pair partition")
    for a, b in pp.tolist():
        require(rows[a]["target"] != rows[b]["target"] and {rows[a]["query"], rows[b]["query"]} == set(rows[a]["entities"])
                and all(rows[a][k] == rows[b][k] for k in ("entities", "values", "permutation", "language")), "intact pair")
    events = torch.empty((STEPS, 24, 4), dtype=torch.int64)
    order = ORDERS[SEEDS.index(seed)]
    for epoch in range(300):
        perm = torch.randperm(96, generator=torch.Generator().manual_seed(order + SHUFFLE_OFFSET + epoch))
        for j in range(4):
            step = epoch * 4 + j
            events[step, :, 0] = epoch % 3
            events[step, :, 1] = (epoch // 3 + epoch % 3) % 3
            events[step, :, 2:] = pp[perm[24*j:24*(j+1)]]
    return events


def fit(model, data, tokens, targets, seed, arm, pairs, wide):
    require(arm in ARMS and tokens.shape == (3, 3, 192, SLOTS) and tokens.dtype == targets.dtype == torch.int64, "fit tables")
    require(torch.equal(targets, torch.tensor([r["target"] for r in data["TRAIN"]], dtype=torch.int64)), "target alignment")
    expected = manifest()["trainable_parameters"][arm]
    require(sum(p.numel() for p in model.parameters() if p.requires_grad) == expected, "fit trainable count")
    require(all(p.requires_grad == (arm == ARMS[0]) for p in model.backbone.core.parameters()), "core freeze policy")
    events = schedule(seed, data["TRAIN"], pairs)
    stats = wide.schedule_stats(events)
    torch.manual_seed(FIT_RNG)
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=.005, betas=(.9, .999), eps=1e-8, weight_decay=0.)
    model.train()
    losses, counts, union = [], [], {}
    for step, event in enumerate(events):
        require(len(optimizer.param_groups) == 1 and optimizer.param_groups[0]["lr"] == .005, "constant LR")
        optimizer.zero_grad(set_to_none=True)
        ids = event[:, 2:].flatten()
        logits = model(tokens[event[:, 0].repeat_interleave(2), event[:, 1].repeat_interleave(2), ids], torch.zeros(48, dtype=torch.int64))
        require(logits.shape == (48, 256) and bool(torch.isfinite(logits).all()), "logits")
        loss = F.cross_entropy(logits, targets[ids])
        require(bool(torch.isfinite(loss)), "finite loss")
        losses.append(float(loss.detach()))
        loss.backward()
        received = {n: p.numel() for n, p in model.named_parameters() if p.grad is not None}
        require(arm == ARMS[0] or all(p.grad is None for p in model.backbone.core.parameters()), "frozen core received gradient")
        union.update(received)
        counts.append(sum(received.values()))
        torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1., error_if_nonfinite=True)
        optimizer.step()
        if (step+1) % 200 == 0:
            print(f"[C307] seed={seed} arm={arm} step={step+1}/1200 ce={losses[-1]:.6f} gradient_parameters={counts[-1]}", flush=True)
    model.eval()
    return dict(steps=STEPS, training_rows=57600, optimizer_creations=1, fit_rng=FIT_RNG, trainable_parameters=expected,
        ce_history=losses, gradient_parameter_counts=counts, gradient_union=dict(sorted(union.items())), schedule_events=events, **stats)


def check_fit(f, seed, arm, data, pairs, wide):
    require(arm in ARMS, "arm")
    expected = dict(steps=STEPS, training_rows=57600, optimizer_creations=1, fit_rng=FIT_RNG,
                    trainable_parameters=manifest()["trainable_parameters"][arm])
    require(all(type(f[k]) is int and f[k] == v for k, v in expected.items()), "fit metadata")
    events = schedule(seed, data["TRAIN"], pairs)
    stats = wide.schedule_stats(events)
    require(torch.equal(events, f["schedule_events"]) and all(f[k] == v for k, v in stats.items()), "schedule reconstruction")
    require(f["per_length_row_exposures"] == [[100]*192 for _ in range(3)]
            and [sum(r[i] for r in f["length_profile_updates"]) for i in range(3)] == [400]*3, "exposure")
    require(len(f["ce_history"]) == STEPS and all(type(v) in (int, float) and math.isfinite(v) and v >= 0 for v in f["ce_history"]), "loss history")
    union = f["gradient_union"]
    require(union and all(type(n) is str and type(v) is int and v > 0 for n, v in union.items()), "gradient union")
    require(sum(union.values()) <= expected["trainable_parameters"] and len(f["gradient_parameter_counts"]) == STEPS
            and all(type(v) is int and 0 < v <= sum(union.values()) for v in f["gradient_parameter_counts"]), "gradient counts")
    if arm == ARMS[1]:
        require(not any(n.startswith("backbone.core.") for n in union), "frozen gradient union")


def train_one(model, data, prompts, tokens, targets, seed, arm, pairs, wide, c):
    initial, core_initial = c.base.fingerprint(model), c.base.fingerprint(model.backbone.core)
    with c.p267.counted(model, c.core) as (calls, cores):
        fitted = fit(model, data, tokens, targets, seed, arm, pairs, wide)
        final, core_final = c.base.fingerprint(model), c.base.fingerprint(model.backbone.core)
        model.requires_grad_(False)
        raw = wide.evaluate(model, prompts, data, c)
    require(calls == [1308, 67968] and cores[0] == 5232, "train/evaluation counts")
    require(initial != final and c.base.fingerprint(model) == final and ((core_initial == core_final) == (arm == ARMS[1])), "core/final state")
    return dict(seed=seed, arm=arm, parameters=14256, slots=SLOTS, initial_sha256=initial, final_sha256=final,
        core_initial_sha256=core_initial, core_final_sha256=core_final, fit=fitted, raw=raw,
        forward_calls=1308, row_presentations=67968, core_forward_calls=5232), {n: p.detach().cpu().clone() for n, p in model.state_dict().items()}


def paired_outcomes(results):
    expected = identities()
    require([(r["seed"], r["arm"]) for r in results] == expected, "paired cohort")
    counts = dict(both_pass=0, full_only=0, frozen_only=0, both_fail=0)
    for i in range(0, len(results), 2):
        a, b = (results[i+j]["quint_pass"] for j in (0, 1))
        require(type(a) is bool and type(b) is bool, "paired flags")
        counts["both_pass" if a and b else "full_only" if a else "frozen_only" if b else "both_fail"] += 1
    return counts


def analyze(records, data, pairs, wide, diag, c):
    require([(r["seed"], r["arm"]) for r in records] == identities(), "record cohort")
    metrics, parts, results = [], [], []
    for r in records:
        arm = r["arm"]
        check_fit(r["fit"], r["seed"], arm, data, pairs, wide)
        require(r["parameters"] == 14256 and r["slots"] == 64 and r["initial_sha256"] != r["final_sha256"]
                and ((r["core_initial_sha256"] == r["core_final_sha256"]) == (arm == ARMS[1])) and r["checkpoint_roundtrip"] is True, "record state")
        error = r["reload_max_error"]
        require(type(error) in (int, float) and math.isfinite(error) and 0 <= error <= 1e-9, "replay")
        fields = ("forward_calls", "row_presentations", "core_forward_calls", "replay_forward_calls", "replay_row_presentations", "replay_core_forward_calls")
        require(all(type(r[k]) is int for k in fields) and tuple(r[k] for k in fields) == (1308, 67968, 5232, 108, 10368, 432), "record work")
        require(set(r["raw"]) == set(map(str, LENGTHS)), "lengths")
        scored = {str(n): wide.score_length(data, r["raw"][str(n)], c) for n in LENGTHS}
        flags = {n: v["passed"] for n, v in scored.items()}
        require(all(type(v) is bool for v in flags.values()), "gate flags")
        direct = {}
        for n in LENGTHS:
            normalized = diag.normalize_task(scored[str(n)], "triple", r["seed"], arm)
            for split in ("TRAIN", "HOLDOUT"):
                part = diag.partition([p for p in normalized if p["split"] == split])
                direct[n, split] = part["direct_pass"]
                parts.append(dict(seed=r["seed"], arm=arm, identifier_length=n, split=split, length_trained=n<5, **part))
        results.append(dict(seed=r["seed"], arm=arm, length_pass=flags, quint_pass=flags["5"], all_lengths_pass=all(flags.values()),
            fitted_train_direct_pass=all(direct[n, "TRAIN"] for n in (2, 3, 4)),
            trained_length_holdout_direct_pass=all(direct[n, "HOLDOUT"] for n in (2, 3, 4))))
        metrics.append(dict(seed=r["seed"], arm=arm, length_scores=scored))
    for i in range(0, 10, 2):
        a, b = records[i:i+2]
        require(a["initial_sha256"] == b["initial_sha256"] and a["core_initial_sha256"] == b["core_initial_sha256"]
                and a["fit"]["event_sha256"] == b["fit"]["event_sha256"] and a["fit"]["ce_history"][0] == b["fit"]["ce_history"][0], "matched pairs")
    counts = {str(n): {a: sum(r["length_pass"][str(n)] for r in results if r["arm"] == a) for a in ARMS} for n in LENGTHS}
    contrasts = []
    for seed, n, split in itertools.product(SEEDS, LENGTHS, ("TRAIN", "HOLDOUT")):
        a, b = [next(p for p in parts if (p["seed"], p["identifier_length"], p["split"], p["arm"]) == (seed, n, split, arm)) for arm in ARMS]
        require(a["rows"] == b["rows"], "contrast rows")
        contrasts.append(dict(seed=seed, identifier_length=n, split=split, rows=a["rows"], full_train_correct=a["correct"], core_frozen_correct=b["correct"]))
    return metrics, dict(seed_results=results, final_partitions=parts, contrasts=contrasts, length_pass_counts=counts,
        gradient_receivers=[dict(seed=r["seed"], arm=r["arm"], trainable=r["fit"]["trainable_parameters"], received_union=sum(r["fit"]["gradient_union"].values())) for r in records],
        paired_five=paired_outcomes(results), candidate_gate=counts["5"][ARMS[1]] == 5,
        all_pairs_matched=True, all_replays=True, **WORK)


def load_parent(paths):
    parent, audit, wide, _, _, transfer, c = context()
    paths = [Path(p).resolve() for p in paths]
    hashes = (PARENT_SHA, parent.PARENT_SHA, audit.PARENT_SHA, *wide.parent_hashes(wide.context()[0]))
    require(len(paths) == len(hashes) == 33 and all(c.audit.sha(p) == h for p, h in zip(paths, hashes, strict=True)), "parent hashes")
    with audit.no_neural():
        payload, _ = parent.verify_artifacts(paths[0].parent, paths[1:], PARENT_EXECUTION)
        parent.validate_result(payload)
        require(payload["experiment_id"] == "C306-v5b-broad-length-core-freeze" and payload["commit_sha"] == PARENT_EXECUTION
                and payload["status"] == "FAIL" and payload["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "parent identity")
        require(len(payload["artifacts"]) == 7 and {a["file"] for a in payload["artifacts"]} == set(OUTPUTS), "parent outputs")
        summary = payload["validation_summary"]
        require(summary["seed_results"] == expected_parent_flags() and summary["candidate_gate"] is False
                and summary["all_pairs_matched"] is True and summary["all_replays"] is True, "parent outcomes")
        verify_parent_policy(parent)
        data = c.audit.read_json(paths[0].parent / "dataset.json")
        prompts = c.audit.read_json(paths[0].parent / "length-datasets.json")
        require(digest(data) == DATA_SHA and digest(prompts) == PROMPTS_SHA, "data hashes")
        require(prompts == wide.prompt_dataset(data), "same prompts")
        wide.validate_prompts(prompts, data, c, transfer)
    return payload, data, prompts


def precheck(paths, root):
    validate_seal()
    payload, _, _ = load_parent(paths)
    parent, audit, wide, pairs, diag, transfer, c = context()
    root = Path(root).resolve()
    pins, protected = dict(payload["source_blobs"]), dict(payload["input_sha256"])
    require((len(pins), len(protected)) == (682, 1267) and pins.get(PARENT_SOURCE) == PARENT_BLOB
            and pins.get(WIDE_SOURCE) == WIDE_BLOB, "inherited protection")
    require(all(pins.get(n) == h for n, h in wide.PINNED.items()), "backend/scorer source pins")
    for module in [parent, audit, wide, pairs, diag, transfer, *parent.context(), *wide.context(), *vars(c).values(), c.factory.language_module()]:
        path = getattr(module, "__file__", None) if isinstance(module, ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            require(Path(path).resolve().relative_to(root).as_posix() in pins, "unprotected helper")
    for n, h in pins.items():
        require(c.audit.git(root, "rev-parse", "HEAD:" + n).decode().strip() == h, "changed source:" + n)
    for n, h in protected.items():
        require(Path(n).is_file() and c.audit.sha(n) == h, "changed input:" + n)
    directory = Path(paths[0]).resolve().parent
    for path, h in [(directory/"summary.json", PARENT_SHA)] + [(c.audit.safe_child(directory, a["file"]), a["sha256"]) for a in payload["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path) == h, "parent input")
        protected[str(path.resolve())] = h
    for n in OWN:
        require(n not in pins, "OWN collision")
        pins[n] = c.audit.git(root, "rev-parse", "HEAD:" + n).decode().strip()
    protected.update(c.audit.protect_tree_files(root, pins))
    require((len(pins), len(protected)) == (688, 1281), "protection counts")
    print(f"registration_check = source_pins:688; protected_inputs:1281; manifest_sha256:{MANIFEST_SHA}", flush=True)
    return pins, protected


def runtime_preflight(paths, root):
    precheck(paths, root)
    parent, _, wide, pairs, _, _, c = context()
    _, data, _ = load_parent(paths)
    tokens, targets = wide.training_tables(data)
    verify_parent_policy(parent)
    for seed in SEEDS:
        stats = wide.schedule_stats(schedule(seed, data["TRAIN"], pairs))
        require(stats["per_length_row_exposures"] == [[100]*192 for _ in range(3)], "real exposure")
    models = make_models(SEEDS[0], parent, wide, c)
    report = parent.first_batch_probe(models, tokens, targets, schedule(SEEDS[0], data["TRAIN"], pairs))
    print("initial_forward_and_backward =", json.dumps(report, sort_keys=True), flush=True)
    print("fresh_seed_replication_preflight = PASS; unchanged C306 training policy; science not started", flush=True)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["diagnostic_execution_valid"] is True, "result identity")
    require(p["gate_f_candidate"] is False and p["production_adoption"] is False, "scope")
    require((len(p["source_blobs"]), len(p["input_sha256"])) == (688, 1281) and set(OWN) <= set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE) == PARENT_BLOB, "result protection")
    require(len(p["artifacts"]) == 7 and {a["file"] for a in p["artifacts"]} == set(OUTPUTS), "outputs")
    summary = p["validation_summary"]
    results = summary["seed_results"]
    require([(r["seed"], r["arm"]) for r in results] == identities(), "result cohort")
    for r in results:
        require(set(r["length_pass"]) == set(map(str, LENGTHS)) and all(type(v) is bool for v in r["length_pass"].values()), "length flags")
        require(r["quint_pass"] is r["length_pass"]["5"] and r["all_lengths_pass"] is all(r["length_pass"].values()), "derived flags")
        require(type(r["fitted_train_direct_pass"]) is bool and type(r["trained_length_holdout_direct_pass"]) is bool, "direct flags")
    counts = {str(n): {a: sum(r["length_pass"][str(n)] for r in results if r["arm"] == a) for a in ARMS} for n in LENGTHS}
    gate = counts["5"][ARMS[1]] == 5
    require(summary["length_pass_counts"] == counts and summary["candidate_gate"] is gate and p["status"] == ("PASS" if gate else "FAIL"), "candidate gate")
    require(summary["paired_five"] == paired_outcomes(results) and summary["all_pairs_matched"] is True and summary["all_replays"] is True, "matching/paired outcomes")
    require((len(summary["final_partitions"]), len(summary["contrasts"]), len(summary["gradient_receivers"])) == (80, 40, 10), "inventory")
    require(all(type(summary[k]) is int and summary[k] == v for k, v in WORK.items()), "workload")


def load_bundle(path):
    data = torch.load(path, map_location="cpu", weights_only=True)
    require(set(data) == {"schema", "identities", "states"} and data["schema"] == "fold-c307-replication-models-v1"
            and data["identities"] == [list(i) for i in identities()] and len(data["states"]) == 10, "bundle schema")
    return data["states"]


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from flatten(test)
        else:
            yield test


def regression_modules(root):
    modules = context()[0].regression_modules(root)
    require(len(modules) == len(set(modules)) == 191, "parent modules")
    return modules + ["tests_lm.test_v05_c307_core_freeze_replication"]


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) == 4846 and ids.count(EXCLUDED) == 1, "loaded suite")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require(len(kept) == 4845, "focused suite")
    return unittest.TestSuite(kept)


def guard(root, head, c):
    require(c.audit.git(root, "rev-parse", "HEAD").decode().strip() == head
            and c.audit.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss"
            and not c.audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "repository guard")


def run(*, summaries, output_dir, expected_head):
    parent, _, wide, pairs, diag, _, c = context()
    root = Path(__file__).resolve().parents[2]
    guard(root, expected_head, c)
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    pins, protected = precheck(summaries, root)
    _, data, prompts = load_parent(summaries)
    tokens, targets = wide.training_tables(data)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    records, states = [], []
    for seed in SEEDS:
        models = make_models(seed, parent, wide, c)
        for arm in ARMS:
            print(f"[C307] model={len(records)+1}/10 seed={seed} arm={arm}", flush=True)
            record, state = train_one(models[arm], data, prompts, tokens, targets, seed, arm, pairs, wide, c)
            records.append(record)
            states.append(state)
    torch.save(dict(schema="fold-c307-replication-models-v1", identities=[list(i) for i in identities()], states=states), out/"trained-models.pt")
    states = load_bundle(out/"trained-models.pt")
    for i, seed in enumerate(SEEDS):
        models = make_models(seed, parent, wide, c)
        for j, arm in enumerate(ARMS):
            k = 2*i+j
            wide.replay_one(models[arm], states[k], records[k], prompts, data, c)
    metrics, summary = analyze(records, data, pairs, wide, diag, c)
    torch.save(dict(schema="fold-c307-replication-eval-v1", records=records), out/"evaluations.pt")
    for n, value in (("architecture-plan.json", manifest()), ("dataset.json", data), ("length-datasets.json", prompts),
                     ("measurements.json", metrics), ("validation-summary.json", summary)):
        (out/n).write_bytes(blob(value))
    artifacts = [dict(file=n, sha256=c.audit.sha(out/n), serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root, expected_head, c)
    precheck(summaries, root)
    payload = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head, status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True, source_blobs=pins, input_sha256=protected, artifacts=artifacts,
        validation_summary=summary, gate_f_candidate=False, production_adoption=False)
    validate_result(payload)
    (out/"summary.json").write_bytes(blob(payload))
    receipt = {k: payload[k] for k in ("experiment_id", "stage", "commit_sha", "status", "artifacts")}
    receipt["summary_sha256"] = c.audit.sha(out/"summary.json")
    print("=== C307 COMPACT REPLICATION RECEIPT ===", flush=True)
    print(json.dumps(receipt, indent=2, sort_keys=True), flush=True)
    return payload


def verify_artifacts(outdir, summaries, expected_head):
    _, audit, wide, pairs, diag, _, c = context()
    out = Path(outdir)
    payload = c.audit.read_json(out/"summary.json")
    validate_result(payload)
    require(payload["commit_sha"] == expected_head, "execution HEAD")
    for n, h in payload["input_sha256"].items():
        require(c.audit.sha(n) == h, "protected input")
    for artifact in payload["artifacts"]:
        path = c.audit.safe_child(out, artifact["file"])
        require(c.audit.sha(path) == artifact["sha256"] and path.stat().st_size == artifact["serialized_bytes"], "output bytes")
    with audit.no_neural():
        _, data, prompts = load_parent(summaries)
        require(c.audit.read_json(out/"dataset.json") == data and c.audit.read_json(out/"length-datasets.json") == prompts, "persisted inputs")
        archive = torch.load(out/"evaluations.pt", map_location="cpu", weights_only=True)
        require(set(archive) == {"schema", "records"} and archive["schema"] == "fold-c307-replication-eval-v1", "evaluation schema")
        metrics, summary = analyze(archive["records"], data, pairs, wide, diag, c)
        for n, value in (("architecture-plan.json", manifest()), ("measurements.json", metrics), ("validation-summary.json", summary)):
            require(c.audit.read_json(out/n) == value, "persisted:" + n)
    require(payload["validation_summary"] == summary, "summary reconstruction")
    return payload, metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summaries", nargs=33, type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
