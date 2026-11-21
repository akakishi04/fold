"""C244: two TRAIN partners per value, fixed-budget balanced-block learning."""
from __future__ import annotations
import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import inspect
import itertools
import json
from pathlib import Path
import time
import unittest

import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C244-v5b-two-partner-recombination"
STAGE = "V5-B-TWO-PARTNER-RECOMBINATION"
BASE = "432ecaa53da0f45806793865d88334fbbb90569f"
PARENT_EXECUTION = "1ff8bcfd4905b54c9f685eee26e197eb62394ab2"
PARENT_SHA = "adf53e7f0306ab9d3fa209f24fb4fa1dbdc3d717037a4e7931579e670acdd2ce"
PARENT_ARTIFACTS = {
    "audit-plan.json": "02f2420c59bfa7a232686ea42cf2ed47ee6c17ebe2714e81a2fbc169a8e70379",
    "diagnostics.json": "054369ba51d66be1166fff873ded22d31e683141a534937f5cfb4f4341c47347",
    "pair-audit.json": "67fcc06862d282150fc4f5f0815d88ae52a0928c4574c698292d4ed49fb2ed72",
    "row-errors.json": "2a89dc0e500523718bd020948a328da0418a1080c90278ed712ff5e854516620",
    "validation-summary.json": "beb8da05e254bb9872e6a555318dd62ce6deecd9b4b3c1e20aa5a0c3ccd63e0e",
}
C242_SHA = "d10aad6f47eb2cabc35d8b6519b22c05ab634922cbc81a9bea6147ea7794cfcb"
SOURCE_SPLIT_SHA = "9b5cc13cfe9dc9a139f23c44d87397f2af4f1174f1a9cf0fb4659d6ddfcad0b0"
SPLIT_SHA = "e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346"
MANIFEST_SHA = "e89a41c15ef3d702c7009a9b4fc22f4e28809dea3892c5d63cf02120a1e10b0b"
SEEDS, FAMILIES = (234001, 234002, 234003), ("full", "gru_only")
SPLITS, VIEWS = ("TRAIN", "HOLDOUT"), ("normal", "evidence_blind", "query_blind")
OLD_PAIRS = ((0, 1), (1, 0), (2, 3), (3, 2))
ADDED_PAIRS = ((0, 2), (2, 0), (1, 3), (3, 1))
HELD_PAIRS = ((0, 3), (3, 0), (1, 2), (2, 1))
ROWS = {"TRAIN": 64, "HOLDOUT": 32}
STEPS, BATCH, LR, CLIP, TOL = 400, 32, 0.005, 1.0, 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c244_two_partner_recombination.py",
       "tests_lm/test_v05_c244_two_partner_recombination.py", "tools/run_c244.ps1", "tools/invoke_c244.ps1",
       "docs/experiment-ledger-addendum-c244-preregistration.md", "docs/v5b-two-partner-recombination-v0.1.md")
OUTPUTS = {"two-partner-plan.json", "split-dataset.json", "trained-models.pt", "measurements.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c243_saved_recombination_audit as parent
    return parent


def context():
    audit_parent = parent_module()
    fitting = audit_parent.parent_module()
    _, binding, factory, audit = fitting.context()
    return audit_parent, fitting, binding, factory, audit


def identities():
    return list(itertools.product(SEEDS, FAMILIES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        c242_sha256=C242_SHA, source_split_sha256=SOURCE_SPLIT_SHA, split_sha256=SPLIT_SHA,
        identities=[list(x) for x in identities()], rows=ROWS, old_pairs=OLD_PAIRS, added_pairs=ADDED_PAIRS,
        held_pairs=HELD_PAIRS, views=VIEWS, steps=STEPS, batch=BATCH, lr=LR, clip=CLIP,
        schedule="zero-based even step: old block0..31; odd step: added block32..63",
        block_updates_per_model=[200, 200], presentations_per_train_row=200,
        optimizer="AdamW", betas=[.9, .999], eps=1e-8, weight_decay=0.0,
        parameters=dict(full=13488, gru_only=10160), width=16, slots=48,
        initialization="fresh exact C242 initial_sha256; no trained checkpoint reuse",
        train_steps=2400, answer_presentations=76800, model_forward_calls=2490, row_presentations=81408,
        evaluation_forwards=90, checkpoint_writes=1, dtype="float64", device="cpu", threads=2,
        deterministic=True, gate=dict(accuracy=.90, fact_pair=.80, query_pair=.80, order_pair=.80,
                                     evidence_drop=.35, query_drop=.35),
        nonqueried_value_lookup_train_ceiling=.50, query_only_train_ceiling=.25,
        comparator="C242 saved discrete metrics on exactly C244 HOLDOUT32; no NLL reconstruction",
        source_pins=310, protected_inputs=478, direct_dependencies=20, own_tests=24,
        modules=129, loaded_tests=3026, focused_tests=3025, excluded_test=EXCLUDED,
        replay_tolerance=TOL, network_calls=0, gate_f_candidate=False,
        general_language_claim=False, causal_mechanism_claim=False, core_superiority_claim=False)


def ceiling(rows, key):
    groups = defaultdict(Counter)
    for r in rows:
        groups[key(r)][r["target"]] += 1
    return sum(max(c.values()) for c in groups.values()) / len(rows)


def split_data(source, audit_parent, binding):
    audit_parent.validate_parts(source)
    require(digest(source) == SOURCE_SPLIT_SHA, "C242 source identity")
    old = list(source["TRAIN"])
    added = [r for r in source["HOLDOUT"] if tuple(r["values"]) in ADDED_PAIRS]
    held = [r for r in source["HOLDOUT"] if tuple(r["values"]) in HELD_PAIRS]
    require({tuple(r["values"]) for r in old} == set(OLD_PAIRS), "old block pairs")
    require(len(old) == len(added) == len(held) == 32, "block coverage")
    parts = dict(TRAIN=old + added, HOLDOUT=held)
    require(digest(parts) == SPLIT_SHA, "C244 split identity")
    for block in (old, added, held):
        require(Counter((r["language"], r["query"], r["order"], r["target"]) for r in block) ==
                {k: 1 for k in itertools.product(("en", "ja"), (0, 1), (0, 1), range(48, 52))}, "joint block balance")
    partners = defaultdict(set)
    for r in parts["TRAIN"]:
        a, b = r["values"]
        partners[a].add(b)
        partners[b].add(a)
    require(set(partners) == set(range(4)) and all(len(v) == 2 for v in partners.values()), "two partners per value")
    for split, rows in parts.items():
        require(len({r["id"] for r in rows}) == ROWS[split] and all(binding.render(r) == r["prompt"] for r in rows), "row identity/render")
        require(ceiling(rows, lambda r: binding.render(r, "evidence_blind")) == .25, "evidence-blind ceiling")
        require(ceiling(rows, lambda r: binding.render(r, "query_blind")) == .50, "query-blind ceiling")
    train = parts["TRAIN"]
    require(ceiling(train, lambda r: (r["language"], r["query"], r["order"], r["values"][1-r["query"]])) == .50,
            "nonqueried-value shortcut ceiling")
    require(ceiling(train, lambda r: (r["language"], r["query"], r["order"])) == .25, "query-only ceiling")
    for key in ("id", "prompt", "group"):
        require(not {r[key] for r in train} & {r[key] for r in held}, "partition leakage")
    return parts


def balanced_indices(count, step):
    require(type(count) is int and count == 64 and type(step) is int and step >= 0, "schedule inputs")
    return torch.arange(32, dtype=torch.int64) + 32 * (step % 2)


def fit(model,train_tokens,train_targets,seed,*,steps=STEPS):
    require(type(steps) is int and steps>0 and len(train_tokens)==train_targets.numel()>0,"training inputs")
    sampler=torch.Generator(device="cpu").manual_seed(seed+1000)
    optimizer=torch.optim.AdamW(model.parameters(),lr=LR,betas=(0.9,0.999),eps=1e-8,weight_decay=0.0)
    model.train(); started=time.perf_counter(); first=last=None
    for step in range(steps):
        ids=balanced_indices(len(train_targets),step)
        optimizer.zero_grad(set_to_none=True)
        logits=model(train_tokens[ids],torch.zeros(BATCH,dtype=torch.int64))
        loss=F.cross_entropy(logits,train_targets[ids]); require(bool(torch.isfinite(loss)),"nonfinite training loss")
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),CLIP,error_if_nonfinite=True)
        optimizer.step(); last=float(loss.detach())
        if first is None:first=last
        if (step+1)%100==0:print(f"[C244] seed={seed} step={step+1}/{steps} answer_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=steps,answer_presentations=steps*BATCH,first_loss=first,last_loss=last,
                fit_seconds=time.perf_counter()-started)


def audit_fit_contract(fitting):
    class Change(ast.NodeTransformer):
        changed = 0
        def visit_Constant(self, node):
            if isinstance(node.value, str):
                node.value = node.value.replace("[C242]", "[C244]")
            return node
        def visit_Assign(self, node):
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "ids":
                expected = ast.parse("ids=balanced_indices(len(train_targets))").body[0]
                require(ast.dump(node, include_attributes=False) == ast.dump(expected, include_attributes=False), "parent sampler changed")
                self.changed += 1
                return ast.parse("ids=balanced_indices(len(train_targets),step)").body[0]
            return self.generic_visit(node)
    change = Change()
    expected = change.visit(ast.parse(inspect.getsource(fitting.fit)))
    require(change.changed == 1 and ast.dump(expected, include_attributes=False) ==
            ast.dump(ast.parse(inspect.getsource(fit)), include_attributes=False), "fit differs beyond schedule/tag")
    require(all(getattr(fitting, k) == globals()[k] for k in ("STEPS", "BATCH", "LR", "CLIP", "TOL")), "fit constants")


def common_comparator(source, records, held, audit_parent):
    # Only the identical still-held rows are compared; no model call or invented NLL.
    positions = {r["id"]: i for i, r in enumerate(source["HOLDOUT"])}
    selected = [positions[r["id"]] for r in held]
    require(len(set(selected)) == 32, "common holdout membership")
    result = []
    for r in records:
        audit_parent.validate_record(source, r)
        pred = {v: [r["predictions"]["HOLDOUT"][v][i] for i in selected] for v in VIEWS}
        result.append(audit_parent.discrete_metrics(held, pred))
    return result


def train_one(model, parts, reference, *, fitting, binding, factory):
    before = factory.fingerprint(model)
    require(before == reference["initial_sha256"], "fresh initial fingerprint")
    tokens, targets = binding.tensors(parts["TRAIN"], "normal")
    counts, updates, blocks = [0, 0], [0], [0, 0]
    def hook(module, args, output):
        counts[0] += 1
        counts[1] += len(args[0])
        if module.training:
            step = updates[0]
            require(torch.equal(args[0], tokens[balanced_indices(64, step)]), "actual optimizer batch membership")
            blocks[step % 2] += 1
            updates[0] += 1
    handle = model.register_forward_hook(hook)
    try:
        initial, _ = fitting.evaluate(model, parts["TRAIN"], binding, factory.fingerprint)
        trained = fit(model, tokens, targets, reference["seed"])
        final, raw = {}, {}
        for s in SPLITS:
            final[s], raw[s] = fitting.evaluate(model, parts[s], binding, factory.fingerprint)
    finally:
        handle.remove()
    after = factory.fingerprint(model)
    require(before != after and counts == [409, 13280] and updates[0] == 400 and blocks == [200, 200], "training/workload")
    record = dict(seed=reference["seed"], family=reference["family"], initial_sha256=before, final_sha256=after,
        initial_train=initial, final=final, fit=trained, block_updates=blocks, forward_calls=counts[0],
        row_presentations=counts[1], weights_changed=True,
        predictions={s: fitting.prediction_record(raw[s], ROWS[s]) for s in SPLITS})
    return record, {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}, raw


def replay_one(model, state, record, raw, parts, *, fitting, binding, factory):
    model.load_state_dict(state, strict=True)
    model.eval()
    require(factory.fingerprint(model) == record["final_sha256"], "checkpoint fingerprint")
    counts, error = [0, 0], 0.0
    def hook(module, args, output):
        counts[0] += 1
        counts[1] += len(args[0])
    handle = model.register_forward_hook(hook)
    try:
        for s in SPLITS:
            m, logits = fitting.evaluate(model, parts[s], binding, factory.fingerprint)
            error = max(error, *(float((a-b).abs().max()) for a, b in zip(logits, raw[s], strict=True)),
                        *(abs(m[l][k]-record["final"][s][l][k]) for l in m for k in m[l]))
            require(fitting.prediction_record(logits, ROWS[s]) == record["predictions"][s], "prediction replay")
    finally:
        handle.remove()
    require(error <= TOL and counts == [6, 288], "replay/counts")
    record.update(checkpoint_roundtrip=True, prediction_replayed=True, reload_max_error=error,
                  forward_calls=record["forward_calls"]+6, row_presentations=record["row_presentations"]+288)


def load_bundle(path):
    value = torch.load(path, map_location="cpu", weights_only=True)
    require(value["schema"] == "fold-c244-two-partner-v1" and value["identities"] == [list(x) for x in identities()]
            and len(value["states"]) == 6, "checkpoint schema/order")
    return value["states"]


def summarize(records, fitting):
    require([(r["seed"], r["family"]) for r in records] == identities(), "record identity order")
    gates, labels = {f: True for f in FAMILIES}, Counter()
    for r in records:
        require(set(r["final"]) == set(SPLITS) and r["block_updates"] == [200, 200], "split/schedule")
        for s in SPLITS:
            fitting.validate_metrics(r["final"][s], ROWS[s])
        for lang in ("en", "ja"):
            train = fitting.cell_pass(r["final"]["TRAIN"][lang])
            held = fitting.cell_pass(r["final"]["HOLDOUT"][lang])
            labels["TRAIN_CRITERIA_MISS" if not train else "RECOMBINATION_MISS" if not held else "BOTH_PASS"] += 1
            gates[r["family"]] &= train and held
    return dict(models=6, full_two_partner_gate=gates["full"], gru_two_partner_gate=gates["gru_only"],
        cell_outcomes=dict(labels), all_replays=all(r["checkpoint_roundtrip"] is True and r["prediction_replayed"] is True
        and 0 <= r["reload_max_error"] <= TOL for r in records), all_weights_changed=all(r["weights_changed"] is True for r in records),
        train_steps=sum(r["fit"]["steps"] for r in records), answer_presentations=sum(r["fit"]["answer_presentations"] for r in records),
        model_forward_calls=sum(r["forward_calls"] for r in records), row_presentations=sum(r["row_presentations"] for r in records),
        general_language_claim=False, causal_mechanism_claim=False, core_superiority_claim=False)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["diagnostic_execution_valid"] is True, "result identity")
    require((len(p["source_blobs"]), len(p["input_sha256"])) == (310, 478) and set(OWN) <= set(p["source_blobs"]), "protection")
    require(len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS, "artifacts")
    s = p["validation_summary"]
    require((s["models"], s["train_steps"], s["answer_presentations"], s["model_forward_calls"], s["row_presentations"]) ==
            (6, 2400, 76800, 2490, 81408), "workload")
    require(s["all_replays"] is True and s["all_weights_changed"] is True and sum(s["cell_outcomes"].values()) == 12, "integrity")
    require(type(s["full_two_partner_gate"]) is bool and type(s["gru_two_partner_gate"]) is bool
            and p["status"] == ("PASS" if s["full_two_partner_gate"] else "FAIL"), "scientific status")
    require(p["gate_f_candidate"] is False and p["network_calls"] == 0 and all(s[k] is False for k in
            ("general_language_claim", "causal_mechanism_claim", "core_superiority_claim")), "scope")


def precheck(c243_summary, c242_summary, root):
    parent, fitting, _, factory, a = context()
    root, path, old = Path(root), Path(c243_summary).resolve(), Path(c242_summary).resolve()
    require(a.sha(path) == PARENT_SHA, "C243 summary identity")
    p = a.read_json(path)
    parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS", "accepted C243 state")
    pins, protected = dict(p["source_blobs"]), dict(p["input_sha256"])
    for name, wanted in protected.items():
        require(Path(name).is_file() and a.sha(name) == wanted, "changed input: " + name)
    for name, wanted in pins.items():
        require(a.git(root, "rev-parse", "HEAD:"+name).decode().strip() == wanted, "changed source: " + name)
    require(protected.get(str(old)) == C242_SHA and a.sha(old) == C242_SHA, "protected C242 identity")
    require(str(path) not in protected, "parent duplicate")
    protected[str(path)] = PARENT_SHA
    require({x["file"]: x["sha256"] for x in p["artifacts"]} == PARENT_ARTIFACTS, "C243 artifacts")
    for item in p["artifacts"]:
        child = a.safe_child(path.parent, item["file"])
        require(a.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "parent bytes")
        require(str(child.resolve()) not in protected, "artifact duplicate")
        protected[str(child.resolve())] = item["sha256"]
    for name in OWN:
        require(name not in pins, "OWN collision")
        pins[name] = a.git(root, "rev-parse", "HEAD:"+name).decode().strip()
    helpers = ("gate_f_c230_prepared_capsule.py", "model_c231_byte_eval_contract.py", "model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py", "model_c234_context_binding.py", "model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py", "model_c237_frozen_signal_audit.py", "model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py", "model_c240_saved_position_audit.py", "model_c241_assignment_holdout.py",
        "model_c242_balanced_recombination.py", "model_c243_saved_recombination_audit.py")
    deps = set(factory.LM_SOURCES) | {OWN[0]} | {"fold_lm/v05_benchmarks/"+h for h in helpers}
    require(len(deps) == 20 and deps <= set(pins), "direct dependency coverage")
    protected.update(a.protect_tree_files(root, pins))
    require((len(pins), len(protected)) == (310, 478) and digest(manifest()) == MANIFEST_SHA, "counts/manifest")
    audit_fit_contract(fitting)
    return pins, protected


def load_inputs(c242_summary):
    parent, _, binding, _, _ = context()
    source, refs = parent.load_inputs(c242_summary)
    parts = split_data(source, parent, binding)
    for r in refs:
        h = r["initial_sha256"]
        require(isinstance(h, str) and len(h) == 64 and all(c in "0123456789abcdef" for c in h)
                and h != r["final_sha256"], "parent initial/final semantics")
    return parts, refs, common_comparator(source, refs, parts["HOLDOUT"], parent)


def regression_modules(root):
    names = parent_module().regression_modules(root)
    require(len(names) == len(set(names)) == 128, "parent module count")
    return names + ["tests_lm.test_v05_c244_two_partner_recombination"]


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1, "suite identities")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require((len(tests), len(kept)) == (3026, 3025), "suite counts")
    return unittest.TestSuite(kept)


def run(*, c243_summary, c242_summary, output_dir, expected_head):
    _, fitting, binding, factory, a = context()
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root, "rev-parse", "HEAD").decode().strip() == expected_head, "execution HEAD")
        require(a.git(root, "branch", "--show-current").decode().strip() == "feat/sft-target-loss", "branch")
        require(not a.git(root, "status", "--porcelain", "--untracked-files=no").strip(), "dirty tree")
    guard()
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    pins, protected = precheck(c243_summary, c242_summary, root)
    parts, refs, comparators = load_inputs(c242_summary)
    records, states, raw = [], [], []
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    for seed in SEEDS:
        full = factory.new_model(seed)
        baseline = binding.parent_module().new_baseline(full)
        require((sum(p.numel() for p in full.parameters()), sum(p.numel() for p in baseline.parameters())) == (13488, 10160), "model sizes")
        for family, model in (("full", full), ("gru_only", baseline)):
            i = len(records)
            require((refs[i]["seed"], refs[i]["family"]) == (seed, family), "paired identity")
            print(f"[C244] model={i+1}/6 seed={seed} family={family}; two balanced blocks", flush=True)
            r, state, logits = train_one(model, parts, refs[i], fitting=fitting, binding=binding, factory=factory)
            r["c242_same_holdout_discrete"] = comparators[i]
            records.append(r)
            states.append(state)
            raw.append(logits)
    torch.save(dict(schema="fold-c244-two-partner-v1", identities=[list(x) for x in identities()], states=states), out/"trained-models.pt")
    for r, state, logits in zip(records, load_bundle(out/"trained-models.pt"), raw, strict=True):
        model = factory.new_model(r["seed"])
        if r["family"] == "gru_only":
            model = binding.parent_module().new_baseline(model)
        replay_one(model, state, r, logits, parts, fitting=fitting, binding=binding, factory=factory)
    summary = summarize(records, fitting)
    for name, value in (("two-partner-plan.json", manifest()), ("split-dataset.json", parts),
                        ("measurements.json", records), ("validation-summary.json", summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n, sha256=a.sha(out/n), serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard()
    precheck(c243_summary, c242_summary, root)
    for name, wanted in protected.items():
        require(a.sha(name) == wanted, "modified input")
    p = dict(experiment_id=EXPERIMENT_ID, stage=STAGE, commit_sha=expected_head,
        status="PASS" if summary["full_two_partner_gate"] else "FAIL", diagnostic_execution_valid=True,
        source_blobs=pins, input_sha256=protected, artifacts=artifacts, validation_summary=summary,
        gate_f_candidate=False, network_calls=0, limitations=[
            "Coverage and block schedule change jointly; not a unique causal attribution.",
            "Only two partners among four digits; no general-language or all-shortcuts-eliminated claim.",
            "Comparator uses the same HOLDOUT32, not C242's full HOLDOUT64; NLL is not reconstructed."])
    validate_result(p)
    (out/"summary.json").write_bytes(blob(p))
    print("=== C244 RESULT ===", flush=True)
    print(blob(p).decode(), flush=True)
    return p


def verify_artifacts(output_dir, c242_summary, expected_head):
    parent, fitting, _, _, a = context()
    out = Path(output_dir)
    p = a.read_json(out/"summary.json")
    validate_result(p)
    require(p["commit_sha"] == expected_head, "saved HEAD")
    for name, wanted in p["input_sha256"].items():
        require(a.sha(name) == wanted, "postcheck input")
    for item in p["artifacts"]:
        child = a.safe_child(out, item["file"])
        require(a.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "postcheck artifact")
    records = a.read_json(out/"measurements.json")
    require(summarize(records, fitting) == p["validation_summary"] == a.read_json(out/"validation-summary.json"), "saved summary")
    require(a.read_json(out/"two-partner-plan.json") == json.loads(blob(manifest())), "saved plan")
    parts, refs, comparisons = load_inputs(c242_summary)
    require(a.read_json(out/"split-dataset.json") == parts, "saved partition")
    for r, ref, comp in zip(records, refs, comparisons, strict=True):
        require(r["initial_sha256"] == ref["initial_sha256"] and r["c242_same_holdout_discrete"] == comp, "initial/comparator replay")
        for s in SPLITS:
            measured = parent.discrete_metrics(parts[s], r["predictions"][s])
            for lang, m in measured.items():
                require(all(abs(r["final"][s][lang][k]-v) <= TOL for k, v in m.items()), "child discrete replay")
    return p, records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("c243-summary", "c242-summary", "output-dir"):
        parser.add_argument("--"+name, type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
