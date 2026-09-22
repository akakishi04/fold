"""C221: causal live dispatch of the frozen C220 stack; no new training."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import itertools
import json
from pathlib import Path
import unittest

import torch
from torch import nn
from fold_lm.v05 import memory_dispatch as live

EXPERIMENT_ID = "C221-v5f-live-coverage-dispatch"
STAGE = "V5-F-LIVE-COVERAGE-DISPATCH"
BASE = "013a718a5c5d17d585dc1082bae3b937e360007d"
PARENT_EXECUTION = "6bc455fa377ec9d3c70d6d1f0922c00680fd5a04"
PARENT_SHA = "45821b372bf0108e667274e2facd73b1f0a84f515a7d036e73874d9238fff5f7"
PARENT_VALIDATION_SHA = "f17175ab1f914df65a28014fbc2571c32cbeeade583ad7f38093a17a24c458cd"
PARENT_EPISODE_SHA = "99f84e9d05327c8c483b45928676009f6be198e5d568a285d2e893e1279e144f"
MANIFEST_SHA = "fb387b9c026ee852f4efbabab0c71cde93e03fea443f440f7b508b8fe3c3f4d8"
PLAN = (
    ("missing_alpha", "alpha", 2, None),
    ("out_of_scope_beta", "beta", 3, None),
    ("hot_alpha", "alpha", 1, 0),
    ("supported_alpha", "alpha", 0, 0),
    ("hot_beta", "beta", 1, 2),
    ("supported_beta", "beta", 0, 2),
    ("replace_alpha", "alpha", 0, 1),
    ("replace_beta", "beta", 0, 0),
)
CONTROLS = (
    ("hot_alpha", 2, "SUPPRESS_MISSING"),
    ("supported_beta", 3, "SUPPRESS_OUT_OF_SCOPE"),
    ("missing_alpha", 0, "BLOCKED_MISSING"),
    ("out_of_scope_beta", 1, "BLOCKED_OUT_OF_SCOPE"),
)
SEED_FAMILIES = ((218001,218002,218003), (219001,219002,219003),
                 (217001,217002,217003), (216001,216002,216003))
OWN = (
    "fold_lm/v05/memory_dispatch.py",
    "fold_lm/v05_benchmarks/gate_f_c221_live_coverage_dispatch.py",
    "tests_lm/test_v05_c221_live_coverage_dispatch.py",
    "tools/run_c221.ps1", "tools/invoke_c221.ps1",
    "docs/experiment-ledger-addendum-c221-preregistration.md",
    "docs/v5f-live-coverage-dispatch-v0.1.md",
)
OUTPUTS = {"dispatch-plan.json", "live-decisions.json", "intervention-decisions.json",
           "component-fingerprints.json", "validation-summary.json"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    # Lazy only to permit author-side unit testing without the historical regression tree.
    from fold_lm.v05_benchmarks import gate_f_c220_frozen_learned_stack as parent
    return parent


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
                parent_validation_sha256=PARENT_VALIDATION_SHA,
                parent_episode_sha256=PARENT_EPISODE_SHA,
                plan=[list(x) for x in PLAN], controls=[list(x) for x in CONTROLS],
                seed_families=[list(x) for x in SEED_FAMILIES], combinations=81,
                main_decisions=648, control_decisions=324, readable=486, suppressed=162,
                successful_main_calls=dict(coverage=648, selector=486, provider=486,
                                           reader=486, bank_reads=486),
                successful_control_calls=dict(coverage=324, selector=162, provider=162,
                                              reader=0, bank_reads=0),
                writer_forwards=3, successful_total_model_forwards=2109,
                exact_parent_answer_parity=True, actual_call_order_required=True,
                oracle_labels_in_dispatch=False, hard_provider_preconditions=True,
                new_training_steps=0, gate_f_candidate=False,
                device="cpu", threads=2, deterministic_algorithms=True,
                scope="same eight synthetic episode shapes; live Coverage-first call causality only")


class ForcedCoverage(nn.Module):
    """Control only: still call the frozen model, then replace its proposed class."""
    def __init__(self, model, forced):
        super().__init__()
        require(type(forced) is int and 0 <= forced < 4, "bad forced class")
        self.model, self.forced, self.original = model, forced, None

    def forward(self, x):
        logits = self.model(x)
        require(logits.shape == (1,4) and bool(torch.isfinite(logits).all()),
                "malformed Coverage output in control")
        self.original = int(logits.argmax(dim=-1).item())
        controlled = torch.full_like(logits, -1.0)
        controlled[:, self.forced] = 1.0
        return controlled


def request_for(parent, bank, state, query):
    role, factor, scope = parent.query_meta(query)
    features, _ = parent.coverage.target_summary(
        state, query_role=role, scope_id=scope, factor_id=factor, nuisance=(1.0,1.0))

    def provider(port):
        # Real runtime preconditions, independent of learned Coverage and of scorer labels.
        if scope in state.ended_scopes:
            return live.ReadOutcome("OUT_OF_SCOPE")
        records = state.h2.factors + state.hot_records
        if not any((r.scope_id, r.factor_id) == (scope, factor) and not r.assumed
                   for r in records):
            return live.ReadOutcome("MISSING")
        read = bank.read(state)
        if read.value is None:
            status = "NUMERIC_UNSAFE" if read.status.value == "NUMERIC_UNSAFE" else "OUT_OF_SCOPE"
            return live.ReadOutcome(status, bank_reads=1)
        return live.ReadOutcome("READABLE", parent.stack.selected_scalar(read.value, port), 1)

    query_x = torch.tensor([[1,0,1,1] if role == 0 else [0,1,1,1]], dtype=torch.float32)
    return live.QueryRequest(features.reshape(1,7), query_x, provider)


def build_requests(parent, predictions, writer_seed):
    """Rebuild the same C220 states without calling bank.read or consulting expected labels."""
    requests = {}
    for label, query, _, _ in PLAN:
        bank = parent.c216.build_bank()
        state = bank.initial_state()
        if label == "out_of_scope_beta":
            op = parent.memory.MemoryOp(parent.memory.MemoryOpKind.END_SCOPE, 0, "project")
            state, _ = bank.apply(state, op)
        elif label.startswith("replace_"):
            target, initial = (1, (2,2)) if query == "alpha" else (3, (1,2))
            state = parent.c218.oracle_initial_state(bank, *initial, f"c221:{writer_seed}:{label}")
            op = parent.c218.memory_op(parent.memory.MemoryOpKind.REPLACE, state,
                                      predictions[target], 3, f"c221:{writer_seed}:{label}")
            state, _ = bank.apply(state, op)
        elif label != "missing_alpha":
            target = 0 if query == "alpha" else 5
            op = parent.c218.memory_op(parent.memory.MemoryOpKind.ASSERT, state,
                                      predictions[target], 1, f"c221:{writer_seed}:{label}")
            state, _ = bank.apply(state, op)
            if label.startswith("supported_"):
                state, status = bank.commit(state)
                require(status.value == "COMMITTED", "registered commit failed")
        requests[label] = request_for(parent, bank, state, query)
    return requests


def parent_answers(combinations):
    expected_seeds = set(itertools.product(*SEED_FAMILIES))
    result, seen = {}, set()
    names = ("writer_seed", "coverage_seed", "selector_seed", "reader_seed")
    require(isinstance(combinations, list) and len(combinations) == 81, "parent combination count")
    for item in combinations:
        key = tuple(item[n] for n in names)
        require(key in expected_seeds and key not in seen, "parent combination identity")
        seen.add(key)
        episodes = item["episodes"]
        require(len(episodes) == 8, "parent episode count")
        rows = {r["label"]: r for r in episodes}
        require(set(rows) == {x[0] for x in PLAN}, "parent episode identity")
        for label, _, cov, answer in PLAN:
            row = rows[label]
            status = ("SUPPORTED", "HOT_REQUIRED", "MISSING", "OUT_OF_SCOPE")[cov]
            require(row["success"] is True and row["expected_coverage"] == status
                    and row["predicted_coverage"] == status
                    and row["expected_answer"] == row["predicted_answer"] == answer,
                    "parent episode semantics")
            result[key + (label,)] = (cov, answer)
    return result


def calls(rows):
    count = Counter()
    for row in rows:
        count.update(row["trace"])
        count["bank_reads"] += row["bank_reads"]
    return {key: count[key] for key in ("coverage", "selector", "provider", "reader", "bank_reads")}


def evaluate(requests, models, baseline):
    """Scorer labels are used only after dispatch_query returns; never sent to it."""
    main, controls = [], []
    names = ("writer_seed", "coverage_seed", "selector_seed", "reader_seed")
    for seeds in itertools.product(*SEED_FAMILIES):
        ws, cs, ss, rs = seeds
        context = dict(zip(names, seeds, strict=True))
        for label, _, expected_cov, expected_answer in PLAN:
            result = live.dispatch_query(requests[ws][label], models["coverage"][cs],
                                         models["selector"][ss], models["reader"][rs])
            expected_action = "ANSWER" if expected_answer is not None else (
                "SUPPRESS_MISSING" if expected_cov == 2 else "SUPPRESS_OUT_OF_SCOPE")
            expected_trace = ("coverage", "selector", "provider", "reader") if expected_answer is not None else ("coverage",)
            ok = (result.coverage, result.answer) == (expected_cov, expected_answer)
            ok = ok and result.action == expected_action and result.trace == expected_trace
            parity = (result.coverage, result.answer) == baseline[seeds + (label,)]
            main.append(dict(context, label=label, success=bool(ok), parent_parity=parity,
                             **asdict(result)))
        for label, forced, expected_action in CONTROLS:
            intervention = ForcedCoverage(models["coverage"][cs], forced)
            result = live.dispatch_query(requests[ws][label], intervention,
                                         models["selector"][ss], models["reader"][rs])
            expected_trace = ("coverage",) if forced in (2,3) else ("coverage", "selector", "provider")
            ok = (result.action == expected_action and result.trace == expected_trace
                  and result.answer is None and result.bank_reads == 0 and result.coverage == forced)
            controls.append(dict(context, label=label, forced=forced,
                                 original_coverage=intervention.original,
                                 success=bool(ok), **asdict(result)))
    return main, controls


def summarize(main, controls, writer_accuracy, fingerprints_unchanged):
    readable = [r for r in main if r["label"] not in ("missing_alpha", "out_of_scope_beta")]
    suppressed = [r for r in main if r["label"] in ("missing_alpha", "out_of_scope_beta")]
    mc, cc = calls(main), calls(controls)
    return dict(main_decisions=len(main), control_decisions=len(controls),
                main_success=sum(r["success"] for r in main),
                readable_success=sum(r["success"] for r in readable),
                suppressed_success=sum(r["success"] for r in suppressed),
                parent_parity=sum(r["parent_parity"] for r in main),
                control_success=sum(r["success"] for r in controls),
                suppressed_downstream_calls=sum(len(r["trace"])-1 for r in suppressed),
                main_calls=mc, control_calls=cc, writer_target_accuracy=writer_accuracy,
                fingerprints_unchanged=fingerprints_unchanged, writer_forward_calls=3,
                model_forward_calls=3 + sum(mc[k]+cc[k] for k in ("coverage","selector","reader")),
                new_training_steps=0)


def gate(s):
    return (s.get("main_decisions") == s.get("main_success") == s.get("parent_parity") == 648
            and s.get("readable_success") == 486 and s.get("suppressed_success") == 162
            and s.get("control_decisions") == s.get("control_success") == 324
            and s.get("suppressed_downstream_calls") == 0
            and s.get("main_calls") == manifest()["successful_main_calls"]
            and s.get("control_calls") == manifest()["successful_control_calls"]
            and s.get("writer_target_accuracy") == 1.0
            and s.get("fingerprints_unchanged") is True
            and s.get("model_forward_calls") == 2109 and s.get("new_training_steps") == 0)


def precheck(c220_summary, root):
    b = parent_module()
    a = b.audit
    root = Path(root)
    require(a.sha(c220_summary) == PARENT_SHA, "C220 summary changed")
    p = a.read_json(c220_summary)
    b.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS"
            and b.gate(p["validation_summary"]), "wrong accepted C220")
    require(len(p["source_blobs"]) == 158 and len(p["input_sha256"]) == 182, "parent coverage")
    registered = tuple((r["label"], r["query"], int(b.coverage.CoverageClass[r["expected_coverage"]]),
                        r["target_class"]) for r in b.episode_plan())
    require(registered == PLAN and b.EPISODE_PLAN_SHA == PARENT_EPISODE_SHA, "episode change")
    pins, protected = dict(p["source_blobs"]), dict(p["input_sha256"])
    for path, wanted in protected.items():
        require(Path(path).is_file() and a.sha(path) == wanted, "inherited input changed:" + path)
    for path, wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+path).decode().strip() == wanted,
                "parent source changed:"+path)
    protected[str(Path(c220_summary).resolve())] = PARENT_SHA
    for artifact in p["artifacts"]:
        path = a.safe_child(Path(c220_summary).resolve().parent, artifact["file"])
        require(path.is_file() and a.sha(path) == artifact["sha256"]
                and path.stat().st_size == artifact["serialized_bytes"], "parent artifact changed")
        protected[str(path.resolve())] = artifact["sha256"]
        if artifact["file"] == "validation-summary.json":
            require(artifact["sha256"] == PARENT_VALIDATION_SHA, "parent validation changed")
    for path in OWN:
        require(path not in pins, "OWN collides with accepted source")
        pins[path] = a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    dependencies = tuple(b.DIRECT_REPO_DEPENDENCIES) + (
        "fold_lm/v05_benchmarks/gate_f_c220_frozen_learned_stack.py", OWN[0])
    require(len(dependencies) == 16 and all(x in pins for x in dependencies), "unpinned dependency")
    protected.update(a.protect_tree_files(root, pins))
    require(len(pins) == 165 and len(protected) == 195, "C221 protection counts")
    require(digest(manifest()) == MANIFEST_SHA, "C221 manifest drift")
    return p, pins, protected


def regression_modules(root):
    names = parent_module().regression_modules(root)
    require(len(names) == len(set(names)) == 105, "parent module count")
    return names + ["tests_lm.test_v05_c221_live_coverage_dispatch"]


def regression_suite(root):
    b = parent_module()
    tests = list(b.c205._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    excluded = b.c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
    require(all(ids.count(x) == 1 for x in excluded), "historical exclusion identity")
    kept = [t for t in tests if t.id() not in excluded]
    require(len(tests) == 2370 and len(kept) == 2369, "C221 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE
            and p["diagnostic_execution_valid"] is True, "C221 result identity")
    require(len(p["source_blobs"]) == 165 and len(p["input_sha256"]) == 195
            and len(p["artifacts"]) == 5 and {a["file"] for a in p["artifacts"]} == OUTPUTS,
            "C221 output coverage")
    s = p["validation_summary"]
    require(s["main_decisions"] == 648 and s["control_decisions"] == 324
            and s["new_training_steps"] == 0, "incomplete C221")
    require(p["status"] == ("PASS" if gate(s) else "FAIL"), "C221 verdict drift")
    # Model-dependent downstream call counts are gate metrics, not INVALID criteria.
    require(p["gate_f_candidate"] is False and p["network_calls"] == 0, "scope drift")


def run(*, c220_summary, output_dir, expected_head):
    b = parent_module()
    a = b.audit
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip() == expected_head, "HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss", "branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(), "dirty tree")
    guard()
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    p, pins, protected = precheck(c220_summary, root)
    baseline = parent_answers(a.read_json(Path(c220_summary).resolve().parent / "combination-results.json"))
    coverage_parent = b.find_protected_input(p,"summary.json",b.PARENT_C219_SHA)
    models = dict(writer=b.restore_writer_models(p), coverage=b.restore_coverage_models(p,coverage_parent),
                  selector=b.restore_selector_models(p), reader=b.restore_reader_models(p))
    hashers = dict(writer=b.c218.model_sha,coverage=b.c219.model_sha,
                   selector=b.c217.model_sha,reader=b.c216.model_sha)
    def fingerprints():
        return {family: {str(seed): hashers[family](model) for seed,model in group.items()}
                for family,group in models.items()}
    before = fingerprints()
    predictions, forwards, writer_accuracy = b.frozen_writer_predictions(models["writer"])
    require(forwards == 3, "Writer batch count")
    requests = {seed: build_requests(b,predictions[seed],seed) for seed in SEED_FAMILIES[0]}
    main, controls = evaluate(requests,models,baseline)
    after = fingerprints()
    summary = summarize(main,controls,writer_accuracy,before == after)
    out = Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    artifacts = []
    for name,value in (
        ("dispatch-plan.json",manifest()), ("live-decisions.json",main),
        ("intervention-decisions.json",controls),
        ("component-fingerprints.json",dict(before=before,after=after)),
        ("validation-summary.json",summary),
    ):
        path = out / name
        path.write_bytes(blob(value))
        artifacts.append(dict(file=name,sha256=a.sha(path),serialized_bytes=path.stat().st_size))
    guard()
    precheck(c220_summary,root)
    for path,wanted in protected.items():
        require(a.sha(path) == wanted, "input modified:"+path)
    result = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
                  status="PASS" if gate(summary) else "FAIL",diagnostic_execution_valid=True,
                  C220_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,
                  artifacts=artifacts,validation_summary=summary,gate_f_candidate=False,network_calls=0,
                  limitations=["eight reused synthetic episode shapes, not an independent holdout",
                               "operation kinds and query feature construction remain oracle",
                               "explicit provider preconditions are deterministic, not learned",
                               "no acquisition, RETRACT/ASSUME, joint training or memory-cost claim"])
    validate_result(result)
    (out/"summary.json").write_bytes(blob(result))
    print("=== C221 RESULT ===",flush=True)
    print(blob(result).decode(),flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("c220-summary", "output-dir"):
        parser.add_argument("--"+arg,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
