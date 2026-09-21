"""C216: V5-F learned Reader pilot over oracle-selected memory ports.

One changed scientific component: a learned Reader maps an already-selected scalar FOLD-R memory
readout to a three-class semantic answer. Writer, Port Selector, Coverage classifier, memory
semantics, H1/H2 placement and numeric capsule algebra remain deterministic/oracle.

The held-out split is by alpha/beta value pairing, not by rows. Every marginal value is present in
TRAIN, but three pair compositions are withheld completely from Reader training.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time
import unittest

import numpy as np
import torch
from torch.nn import functional as F

from fold_lm.v05 import memory_bank as bankmod
from fold_lm.v05 import memory_bridge as memory
from fold_lm.v05 import memory_capsule_bridge as numeric
from fold_lm.v05 import memory_reader as reader
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_f_c215_h1_h2_chunk_commit as c215

EXPERIMENT_ID = "C216-v5f-learned-reader-pilot"
STAGE = "V5-F-LEARNED-READER-PILOT"
BASE = "7726b805e45fae6ddd14d51d20378138d66ff9c2"
PARENT_C215_EXECUTION = "663f42ca21f977b6530e4df8709fc306c2ebd8c9"
PARENT_C215_SHA = "96b3e5b9cf465b9dea33920de095fc5d7d8e4c0cba960d64597c95fc15eda237"
PARENT_C215_VALIDATION_SHA = "1aa90b651d2f25a2ae72173e2e4e072236572e4057f40a35180a592980e90bd3"
DATA_SHA = "ab0c6da658576d12fc786ad3dfcef94f3acc063d8263dd175d67eec7af6a14eb"
MANIFEST_SHA = "91e8afd97d667b67f1164e87628f62b4bcf2347e2884537ec3e54c2baa6b385c"

VALUES = (-1, 0, 1)
EVAL_PAIRS = ((0, 1), (1, 2), (2, 0))
PLACEMENTS = ("HOT", "COMMITTED")
QUERIES = ("alpha", "beta")
SEEDS = (216001, 216002, 216003)
STEPS = 400
BATCH_SIZE = 24
LR = 0.02
ZERO_EXPECTED = 1.0 / 3.0

HISTORICAL_REGRESSION_RUNNER = "tools/run_c167.ps1"
HISTORICAL_REGRESSION_RUNNER_BLOB = "7c5d6e9838d4ce7bd2bfec0e43458eb749fd1789"

OWN = (
    "fold_lm/v05/memory_reader.py",
    "fold_lm/v05_benchmarks/gate_f_c216_learned_reader.py",
    "tests_lm/test_v05_c216_learned_reader.py",
    "tools/run_c216.ps1",
    "tools/invoke_c216.ps1",
    "docs/experiment-ledger-addendum-c216-preregistration.md",
    "docs/v5f-learned-reader-pilot-v0.1.md",
)
OUTPUTS = {
    "reader-plan.json",
    "reader-dataset.npz",
    "reader-checkpoints.pt",
    "evaluation.json",
    "validation-summary.json",
}
DIRECT_REPO_DEPENDENCIES = (
    "fold_lm/v05/memory_bank.py",
    "fold_lm/v05/memory_bridge.py",
    "fold_lm/v05/memory_capsule_bridge.py",
    "fold_lm/v05/memory_reader.py",
    "fold_lm/v05_benchmarks/gate_e_c175_frozen_prediction_audit.py",
    "fold_lm/v05_benchmarks/gate_e_c205_phase0_batch_composition_attribution.py",
    "fold_lm/v05_benchmarks/gate_f_c215_h1_h2_chunk_commit.py",
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def manifest():
    return dict(
        experiment_id=EXPERIMENT_ID,
        stage=STAGE,
        acceptance_base=BASE,
        parent_c215_execution=PARENT_C215_EXECUTION,
        parent_c215_sha256=PARENT_C215_SHA,
        parent_c215_validation_sha256=PARENT_C215_VALIDATION_SHA,
        data_sha256=DATA_SHA,
        historical_regression_runner=HISTORICAL_REGRESSION_RUNNER,
        historical_regression_runner_blob=HISTORICAL_REGRESSION_RUNNER_BLOB,
        semantic_values=list(VALUES),
        pair_count=9,
        train_pairs=6,
        eval_pairs=3,
        eval_pair_classes=[list(pair) for pair in EVAL_PAIRS],
        rows=36,
        train_rows=24,
        eval_rows=12,
        placements=list(PLACEMENTS),
        queries=list(QUERIES),
        oracle_port_selector=True,
        reader_input_width=1,
        reader_query_features=0,
        reader_status_features=0,
        answer_classes=3,
        hidden_width=8,
        parameters=43,
        seeds=list(SEEDS),
        optimizer="Adam",
        lr=LR,
        betas=[0.9, 0.999],
        eps=1e-8,
        weight_decay=0.0,
        steps=STEPS,
        batch_size=BATCH_SIZE,
        sampling="full-batch deterministic",
        loss="CrossEntropyLoss",
        device="cpu",
        dtype="float32",
        threads=2,
        deterministic_algorithms=True,
        gate_eval_accuracy=1.0,
        gate_train_accuracy=1.0,
        gate_hot_accuracy=1.0,
        gate_committed_accuracy=1.0,
        zero_readout_expected_accuracy=ZERO_EXPECTED,
        placement_prediction_mismatches=0,
        learned_reader=True,
        learned_writer=False,
        port_selector=False,
        coverage_classifier=False,
        model_forward_calls_expected=1215,
        training_steps_total=1200,
        training_examples_drawn=28800,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        scope=(
            "learned Reader only over oracle-selected scalar port readout; "
            "oracle Writer/Port Selector; no language mapping"
        ),
    )


def build_bank():
    J = torch.eye(2, dtype=torch.float64) * 4.0
    eta = torch.zeros(2, dtype=torch.float64)
    Q = torch.eye(2, dtype=torch.float64)
    U = torch.eye(2, dtype=torch.float64)
    contributions = []
    for factor, port in (("alpha", 0), ("beta", 1)):
        for class_id, semantic in enumerate(VALUES):
            W = torch.zeros((2, 2), dtype=torch.float64)
            b = torch.zeros(2, dtype=torch.float64)
            W[port, port] = 0.25
            b[port] = 0.75 * semantic
            contributions.append(
                numeric.PortContribution(f"{factor}-class-{class_id}", W, b)
            )
    bridge = numeric.MemoryCapsuleBridge(J, eta, Q, U, tuple(contributions))
    return bankmod.ChunkedMemoryBank(bridge)


def _assert_op(revision, scope, factor, class_id, evidence_time):
    return memory.MemoryOp(
        kind=memory.MemoryOpKind.ASSERT,
        expected_memory_revision=revision,
        scope_id=scope,
        factor_id=factor,
        relation_key=f"{factor}-class-{class_id}",
        source_id=f"oracle:{factor}:{class_id}",
        evidence_time=evidence_time,
    )


def dataset():
    bank = build_bank()
    metadata = []
    features = []
    labels = []
    split_codes = []
    placement_codes = []
    query_codes = []
    combo_ids = []
    eval_set = set(EVAL_PAIRS)
    pairs = tuple(itertools.product(range(3), repeat=2))
    selector_calls = 0
    writer_operations = 0
    commits = 0

    for combo_id, (alpha_class, beta_class) in enumerate(pairs):
        split = 1 if (alpha_class, beta_class) in eval_set else 0
        state = bank.initial_state()

        state, result = bank.apply(
            state,
            _assert_op(0, memory.GLOBAL_SCOPE, "alpha", alpha_class, 1),
        )
        require(result is None, "alpha ASSERT returned read")
        writer_operations += 1
        state, commit_status = bank.commit(state)
        require(commit_status is bankmod.CommitStatus.COMMITTED, "alpha commit failed")
        commits += 1

        state, result = bank.apply(
            state,
            _assert_op(1, "project", "beta", beta_class, 2),
        )
        require(result is None, "beta ASSERT returned read")
        writer_operations += 1
        hot_read = bank.read(state)
        require(hot_read.status is bankmod.BankReadStatus.HOT_REQUIRED, "beta must be hot")

        committed_state, commit_status = bank.commit(state)
        require(commit_status is bankmod.CommitStatus.COMMITTED, "beta commit failed")
        commits += 1
        committed_read = bank.read(committed_state)
        require(
            committed_read.status is bankmod.BankReadStatus.SUPPORTED,
            "committed pair must be supported",
        )
        torch.testing.assert_close(
            hot_read.value, committed_read.value, rtol=0.0, atol=0.0
        )

        for placement_id, (placement, read) in enumerate(
            (("HOT", hot_read), ("COMMITTED", committed_read))
        ):
            for query_id, query in enumerate(QUERIES):
                selector_calls += 1
                selected = float(read.value[query_id].item())
                target = alpha_class if query_id == 0 else beta_class
                metadata.append(
                    dict(
                        combo_id=combo_id,
                        alpha_class=alpha_class,
                        beta_class=beta_class,
                        split="EVAL" if split else "TRAIN",
                        placement=placement,
                        query=query,
                        target=target,
                    )
                )
                features.append((selected,))
                labels.append(target)
                split_codes.append(split)
                placement_codes.append(placement_id)
                query_codes.append(query_id)
                combo_ids.append(combo_id)

    arrays = dict(
        features=np.asarray(features, dtype="<f8"),
        labels=np.asarray(labels, dtype="<i8"),
        split_codes=np.asarray(split_codes, dtype="u1"),
        placement_codes=np.asarray(placement_codes, dtype="u1"),
        query_codes=np.asarray(query_codes, dtype="u1"),
        combo_ids=np.asarray(combo_ids, dtype="<i4"),
    )
    h = hashlib.sha256(blob(metadata))
    for key in (
        "features",
        "labels",
        "split_codes",
        "placement_codes",
        "query_codes",
        "combo_ids",
    ):
        h.update(arrays[key].tobytes())
    content_sha = h.hexdigest()

    train = arrays["split_codes"] == 0
    ev = arrays["split_codes"] == 1
    profile = dict(
        rows=len(metadata),
        train_rows=int(train.sum()),
        eval_rows=int(ev.sum()),
        train_pairs=len(set(arrays["combo_ids"][train].tolist())),
        eval_pairs=len(set(arrays["combo_ids"][ev].tolist())),
        train_class_counts=np.bincount(arrays["labels"][train], minlength=3).tolist(),
        eval_class_counts=np.bincount(arrays["labels"][ev], minlength=3).tolist(),
        selector_calls=selector_calls,
        writer_operations=writer_operations,
        chunk_commits=commits,
    )
    require(content_sha == DATA_SHA, "C216 dataset content drift")
    require(
        profile
        == dict(
            rows=36,
            train_rows=24,
            eval_rows=12,
            train_pairs=6,
            eval_pairs=3,
            train_class_counts=[8, 8, 8],
            eval_class_counts=[4, 4, 4],
            selector_calls=36,
            writer_operations=18,
            chunk_commits=18,
        ),
        "C216 dataset profile drift",
    )
    return dict(metadata=metadata, content_sha256=content_sha, profile=profile, **arrays)


def model_sha(model):
    h = hashlib.sha256()
    for name, tensor in sorted(model.state_dict().items()):
        array = tensor.detach().cpu().contiguous().numpy()
        h.update(name.encode())
        h.update(str(array.dtype).encode())
        h.update(str(tuple(array.shape)).encode())
        h.update(array.tobytes())
    return h.hexdigest()


def new_reader():
    model = reader.MemoryReader(reader.MemoryReaderConfig())
    require(reader.parameter_count(model) == 43, "Reader parameter count drift")
    return model


def fit(seed, train_x, train_y):
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)
    model = new_reader()
    initial_sha = model_sha(model)
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=LR,
        betas=(0.9, 0.999),
        eps=1e-8,
        weight_decay=0.0,
    )
    started = time.perf_counter()
    initial_loss = None
    final_loss = None
    for step in range(STEPS):
        optimizer.zero_grad(set_to_none=True)
        logits = model(train_x)
        loss = F.cross_entropy(logits, train_y)
        require(torch.isfinite(loss).item(), "nonfinite Reader training loss")
        if step == 0:
            initial_loss = float(loss.item())
        loss.backward()
        optimizer.step()
        final_loss = float(loss.item())
    return model.eval(), dict(
        seed=seed,
        steps=STEPS,
        examples_drawn=STEPS * len(train_x),
        initial_sha256=initial_sha,
        final_sha256=model_sha(model),
        initial_loss=initial_loss,
        final_loss=final_loss,
        fit_wall_clock_seconds=time.perf_counter() - started,
        training_forward_calls=STEPS,
    )


def accuracy(predictions, targets):
    return float((predictions == targets).to(torch.float64).mean().item())


def score_model(model, data):
    x = torch.from_numpy(data["features"].copy()).to(torch.float32)
    y = torch.from_numpy(data["labels"].copy()).to(torch.int64)
    split = torch.from_numpy(data["split_codes"].copy()).to(torch.int64)
    placement = torch.from_numpy(data["placement_codes"].copy()).to(torch.int64)
    query = torch.from_numpy(data["query_codes"].copy()).to(torch.int64)
    combos = torch.from_numpy(data["combo_ids"].copy()).to(torch.int64)
    train = split == 0
    ev = split == 1
    with torch.no_grad():
        train_pred = model(x[train]).argmax(dim=-1)
        eval_pred = model(x[ev]).argmax(dim=-1)
        zero_pred = model(torch.zeros_like(x[ev])).argmax(dim=-1)

    hot = ev & (placement == 0)
    committed = ev & (placement == 1)
    with torch.no_grad():
        hot_pred = model(x[hot]).argmax(dim=-1)
        committed_pred = model(x[committed]).argmax(dim=-1)

    eval_indices = torch.nonzero(ev, as_tuple=False).squeeze(-1)
    keyed = {}
    for local_index, row_index in enumerate(eval_indices.tolist()):
        key = (int(combos[row_index]), int(query[row_index]))
        keyed.setdefault(key, {})[int(placement[row_index])] = int(eval_pred[local_index])
    require(all(set(v) == {0, 1} for v in keyed.values()), "placement pair incomplete")
    placement_mismatches = sum(int(v[0] != v[1]) for v in keyed.values())

    return dict(
        train_accuracy=accuracy(train_pred, y[train]),
        eval_accuracy=accuracy(eval_pred, y[ev]),
        eval_hot_accuracy=accuracy(hot_pred, y[hot]),
        eval_committed_accuracy=accuracy(committed_pred, y[committed]),
        zero_readout_eval_accuracy=accuracy(zero_pred, y[ev]),
        placement_prediction_mismatches=placement_mismatches,
        train_predictions=train_pred.tolist(),
        eval_predictions=eval_pred.tolist(),
        zero_predictions=zero_pred.tolist(),
        scoring_forward_calls=5,
    )


def seed_pass(score):
    return (
        score.get("train_accuracy") == 1.0
        and score.get("eval_accuracy") == 1.0
        and score.get("eval_hot_accuracy") == 1.0
        and score.get("eval_committed_accuracy") == 1.0
        and abs(score.get("zero_readout_eval_accuracy", -1.0) - ZERO_EXPECTED) <= 1e-12
        and score.get("placement_prediction_mismatches") == 0
    )


def gate(summary):
    records = summary.get("seed_records")
    return (
        isinstance(records, list)
        and len(records) == 3
        and [r.get("seed") for r in records] == list(SEEDS)
        and all(seed_pass(r) for r in records)
        and summary.get("all_checkpoint_roundtrips") is True
        and summary.get("data_sha256") == DATA_SHA
        and summary.get("oracle_selector_calls") == 36
        and summary.get("oracle_writer_operations") == 18
        and summary.get("chunk_commits") == 18
        and summary.get("reader_query_features") == 0
        and summary.get("reader_status_features") == 0
        and summary.get("learned_reader_calls") == 1215
        and summary.get("learned_writer_calls") == 0
        and summary.get("port_selector_learned_calls") == 0
        and summary.get("coverage_classifier_calls") == 0
    )


def precheck(c215_summary, root):
    root = Path(root)
    require(audit.sha(c215_summary) == PARENT_C215_SHA, "C215 summary changed")
    p215 = audit.read_json(c215_summary)
    c215.validate_result(p215)
    require(
        p215.get("commit_sha") == PARENT_C215_EXECUTION
        and p215.get("status") == "PASS"
        and c215.gate(p215["validation_summary"])
        and len(p215.get("source_blobs", {})) == 122,
        "Wrong accepted C215 parent",
    )

    pins = dict(p215["source_blobs"])
    historical_blob = audit.git(
        root, "rev-parse", "HEAD:" + HISTORICAL_REGRESSION_RUNNER
    ).decode().strip()
    require(
        historical_blob == HISTORICAL_REGRESSION_RUNNER_BLOB,
        "Historical regression runner changed",
    )
    require(
        HISTORICAL_REGRESSION_RUNNER not in pins,
        "Historical regression runner unexpectedly already parent-pinned",
    )
    pins[HISTORICAL_REGRESSION_RUNNER] = HISTORICAL_REGRESSION_RUNNER_BLOB
    protected = {str(Path(c215_summary).resolve()): PARENT_C215_SHA}
    validation_seen = False
    for artifact in p215["artifacts"]:
        path = audit.safe_child(Path(c215_summary).resolve().parent, artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C215 artifact:" + artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]
        if artifact["file"] == "validation-summary.json":
            require(
                artifact["sha256"] == PARENT_C215_VALIDATION_SHA,
                "C215 validation artifact changed",
            )
            validation_seen = True
    require(validation_seen, "C215 validation artifact missing")

    for name, expected_blob in pins.items():
        actual = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
        require(actual == expected_blob, "C215 source pin changed:" + name)

    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()

    for dependency in DIRECT_REPO_DEPENDENCIES:
        require(dependency in allpins, "Unpinned direct dependency:" + dependency)

    protected.update(audit.protect_tree_files(root, allpins))
    pins.update({name: allpins[name] for name in OWN})

    require(len(pins) == 130, "C216 source pin count drift")
    require(len(protected) == 136, "C216 protected input count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C216 manifest drift")
    return p215, pins, protected


def regression_modules(root):
    names = c215.regression_modules(root)
    require(len(names) == len(set(names)) == 100, "Historical regression module drift")
    return names + ["tests_lm.test_v05_c216_learned_reader"]


def regression_suite(root):
    names = regression_modules(root)
    loaded = unittest.defaultTestLoader.loadTestsFromNames(names)
    tests = list(c205._iter_tests(loaded))
    ids = [test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded) == 1, "Historical dynamic test identity drift:" + excluded)
    kept = [
        test
        for test in tests
        if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
    ]
    require(
        len(tests) == 2186
        and len(kept) == 2185
        and not any(
            test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS for test in kept
        ),
        "C216 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C216",
    )
    require(
        len(payload["source_blobs"]) == 130
        and len(payload["input_sha256"]) == 136
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C216 coverage drift",
    )
    require(
        payload["trained_models"] == 3
        and payload["parameters_per_model"] == 43
        and payload["training_steps_total"] == 1200
        and payload["training_examples_drawn"] == 28800
        and payload["model_forward_calls"] == 1215
        and payload["oracle_selector_calls"] == 36
        and payload["oracle_writer_operations"] == 18
        and payload["chunk_commits"] == 18
        and payload["network_calls"] == 0,
        "C216 workload drift",
    )
    require(
        payload["production_runtime_modified"] is True
        and payload["gate_f_candidate"] is False
        and payload["learned_reader"] is True
        and payload["learned_writer"] is False
        and payload["port_selector"] is False
        and payload["coverage_classifier"] is False,
        "C216 scope drift",
    )
    require(
        payload["status"] == ("PASS" if gate(payload["validation_summary"]) else "FAIL"),
        "C216 gate drift",
    )


def run(*, c215_summary, output_dir, expected_head):
    root = Path(__file__).resolve().parents[2]

    def guard():
        require(
            audit.git(root, "rev-parse", "HEAD").decode().strip() == expected_head,
            "HEAD mismatch",
        )
        require(
            audit.git(root, "branch", "--show-current").decode().strip()
            == "feat/sft-target-loss",
            "Branch mismatch",
        )
        require(
            not audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(),
            "Dirty tracked tree",
        )

    guard()
    _, pins, protected = precheck(c215_summary, root)
    data = dataset()
    train_mask = data["split_codes"] == 0
    train_x = torch.from_numpy(data["features"][train_mask].copy()).to(torch.float32)
    train_y = torch.from_numpy(data["labels"][train_mask].copy()).to(torch.int64)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    artifacts = []

    def record(name):
        path = out / name
        artifacts.append(
            dict(
                file=name,
                sha256=audit.sha(path),
                serialized_bytes=path.stat().st_size,
            )
        )

    def save_json(name, value):
        (out / name).write_bytes(blob(value))
        record(name)

    save_json("reader-plan.json", dict(manifest(), source_blobs=pins))
    np.savez_compressed(
        out / "reader-dataset.npz",
        features=data["features"],
        labels=data["labels"],
        split_codes=data["split_codes"],
        placement_codes=data["placement_codes"],
        query_codes=data["query_codes"],
        combo_ids=data["combo_ids"],
    )
    record("reader-dataset.npz")

    fit_records = []
    state_dicts = []
    initial_models = []
    for seed in SEEDS:
        model, fit_record = fit(seed, train_x, train_y)
        fit_records.append(fit_record)
        state_dicts.append(
            {name: tensor.detach().cpu().clone() for name, tensor in model.state_dict().items()}
        )
        initial_models.append(fit_record["initial_sha256"])

    bundle = dict(
        schema="fold-v5f-reader-checkpoints-v1",
        seeds=list(SEEDS),
        config=dict(input_width=1, hidden_width=8, answer_classes=3),
        state_dicts=state_dicts,
    )
    torch.save(bundle, out / "reader-checkpoints.pt")
    record("reader-checkpoints.pt")

    restored_bundle = torch.load(
        out / "reader-checkpoints.pt", map_location="cpu", weights_only=True
    )
    require(
        restored_bundle["schema"] == "fold-v5f-reader-checkpoints-v1"
        and tuple(restored_bundle["seeds"]) == SEEDS
        and restored_bundle["config"]
        == dict(input_width=1, hidden_width=8, answer_classes=3),
        "Reader checkpoint bundle identity drift",
    )

    seed_records = []
    roundtrips = []
    for seed, state_dict, fit_record in zip(
        SEEDS, restored_bundle["state_dicts"], fit_records, strict=True
    ):
        restored = new_reader()
        restored.load_state_dict(state_dict, strict=True)
        restored.eval()
        final_sha = model_sha(restored)
        roundtrip = final_sha == fit_record["final_sha256"]
        roundtrips.append(roundtrip)
        score = score_model(restored, data)
        seed_records.append(
            dict(
                seed=seed,
                checkpoint_roundtrip=roundtrip,
                initial_sha256=fit_record["initial_sha256"],
                final_sha256=final_sha,
                initial_loss=fit_record["initial_loss"],
                final_loss=fit_record["final_loss"],
                **score,
            )
        )

    save_json("evaluation.json", dict(seed_records=seed_records, fit_records=fit_records))

    learned_reader_calls = sum(
        fit_record["training_forward_calls"] for fit_record in fit_records
    ) + sum(record["scoring_forward_calls"] for record in seed_records)

    summary = dict(
        seed_records=seed_records,
        all_checkpoint_roundtrips=all(roundtrips),
        data_sha256=data["content_sha256"],
        train_rows=data["profile"]["train_rows"],
        eval_rows=data["profile"]["eval_rows"],
        oracle_selector_calls=data["profile"]["selector_calls"],
        oracle_writer_operations=data["profile"]["writer_operations"],
        chunk_commits=data["profile"]["chunk_commits"],
        reader_query_features=0,
        reader_status_features=0,
        learned_reader_calls=learned_reader_calls,
        learned_writer_calls=0,
        port_selector_learned_calls=0,
        coverage_classifier_calls=0,
    )
    save_json("validation-summary.json", summary)

    guard()
    precheck(c215_summary, root)
    for path, wanted in protected.items():
        require(audit.sha(path) == wanted, "Protected input changed:" + path)
    for artifact in artifacts:
        require(
            audit.sha(out / artifact["file"]) == artifact["sha256"],
            "Output changed:" + artifact["file"],
        )

    result = dict(
        experiment_id=EXPERIMENT_ID,
        stage=STAGE,
        commit_sha=expected_head,
        status="PASS" if gate(summary) else "FAIL",
        diagnostic_execution_valid=True,
        C215_summary_sha256=PARENT_C215_SHA,
        source_blobs=pins,
        input_sha256=protected,
        artifacts=artifacts,
        validation_summary=summary,
        fit_records=fit_records,
        trained_models=3,
        parameters_per_model=43,
        training_steps_total=sum(r["steps"] for r in fit_records),
        training_examples_drawn=sum(r["examples_drawn"] for r in fit_records),
        model_forward_calls=learned_reader_calls,
        oracle_selector_calls=data["profile"]["selector_calls"],
        oracle_writer_operations=data["profile"]["writer_operations"],
        chunk_commits=data["profile"]["chunk_commits"],
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        learned_reader=True,
        learned_writer=False,
        port_selector=False,
        coverage_classifier=False,
        limitations=[
            "tiny synthetic three-value semantic decoder pilot",
            "Port Selector is oracle and query IDs never enter the learned Reader",
            "Writer and memory construction are oracle/deterministic",
            "held-out split tests pair composition, not unseen semantic values",
            "no natural language, memory-cost advantage, or Gate F claim",
        ],
    )
    validate_result(result)
    (out / "summary.json").write_bytes(blob(result))
    print(
        "[C216] learned Reader "
        + " ".join(
            f"seed={r['seed']} eval={r['eval_accuracy']:.3f} zero={r['zero_readout_eval_accuracy']:.3f}"
            for r in seed_records
        ),
        flush=True,
    )
    print("=== C216 RESULT ===", flush=True)
    print(blob(result).decode(), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c215-summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
