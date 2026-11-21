"""C217: V5-F learned Port Selector pilot with frozen accepted C216 Readers.

One changed scientific component: a learned Port Selector maps a query descriptor to alpha/beta
memory-port indices. Writer and memory construction remain oracle/deterministic, all accepted C216
Reader checkpoints are frozen, and Coverage classification remains absent.
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

from fold_lm.v05 import memory_bridge as memory
from fold_lm.v05 import memory_port_selector as selector
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_f_c216_learned_reader as c216

EXPERIMENT_ID = "C217-v5f-learned-port-selector-pilot"
STAGE = "V5-F-LEARNED-PORT-SELECTOR-PILOT"
BASE = "1d4fa83418be2455e072272798064d0a937c01f0"
PARENT_C216_EXECUTION = "99d4254c09f38a433374fb2a073403d6e0ec764a"
PARENT_C216_SHA = "7542625a054725d3a70dfa1c19f706fe8fce26af379e24b92aa1ae478483acc9"
PARENT_C216_VALIDATION_SHA = "dddd27d04917f810a68dc83aa98cddabf1cd78cd67357c52b913e2ff3fe239be"
PARENT_READER_CHECKPOINT_SHA = "bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af"
QUERY_DATA_SHA = "a9ec25d8079e27177567dd4ca85c7aee18f511eb8e8db6b774a61af82e91ac3d"
MANIFEST_SHA = "70af02a697ae8fc97f3d379bdab18dd49bf2261a319f7091819323de5c2b8ab4"

TRAIN_NUISANCE = ((-1, -1), (-1, 1), (1, -1))
EVAL_NUISANCE = ((1, 1),)
SELECTOR_SEEDS = (217001, 217002, 217003)
READER_SEEDS = (216001, 216002, 216003)
READER_FINAL_SHA256 = (
    "6f1219b4277e3d4af6494ecf2280f2442887df05d5d133f2e2566b29bf804336",
    "1b7b2f96ad3e33d4ac0422cd7ca72b7f6e53707acf52aa17a44f188b7c2ed199",
    "3d26451e54a8e4327f2dcc9128e73c7e3fc60605c3e2d894876bd65057d2dd7f",
)
UNEQUAL_PAIRS = tuple(pair for pair in itertools.product(range(3), repeat=2) if pair[0] != pair[1])
PLACEMENTS = ("HOT", "COMMITTED")
STEPS = 400
BATCH_SIZE = 6
LR = 0.02

OWN = (
    "fold_lm/v05/memory_port_selector.py",
    "fold_lm/v05_benchmarks/gate_f_c217_learned_port_selector.py",
    "tests_lm/test_v05_c217_learned_port_selector.py",
    "tools/run_c217.ps1",
    "tools/invoke_c217.ps1",
    "docs/experiment-ledger-addendum-c217-preregistration.md",
    "docs/v5f-learned-port-selector-pilot-v0.1.md",
)
OUTPUTS = {
    "selector-plan.json",
    "selector-dataset.npz",
    "selector-checkpoints.pt",
    "evaluation.json",
    "validation-summary.json",
}
DIRECT_REPO_DEPENDENCIES = (
    "fold_lm/v05/memory_bank.py",
    "fold_lm/v05/memory_bridge.py",
    "fold_lm/v05/memory_capsule_bridge.py",
    "fold_lm/v05/memory_reader.py",
    "fold_lm/v05/memory_port_selector.py",
    "fold_lm/v05_benchmarks/gate_e_c175_frozen_prediction_audit.py",
    "fold_lm/v05_benchmarks/gate_e_c205_phase0_batch_composition_attribution.py",
    "fold_lm/v05_benchmarks/gate_f_c215_h1_h2_chunk_commit.py",
    "fold_lm/v05_benchmarks/gate_f_c216_learned_reader.py",
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
        parent_c216_execution=PARENT_C216_EXECUTION,
        parent_c216_sha256=PARENT_C216_SHA,
        parent_c216_validation_sha256=PARENT_C216_VALIDATION_SHA,
        reader_checkpoint_artifact_sha256=PARENT_READER_CHECKPOINT_SHA,
        reader_seeds=list(READER_SEEDS),
        reader_final_sha256=list(READER_FINAL_SHA256),
        reader_checkpoints=3,
        reader_parameters=43,
        query_data_sha256=QUERY_DATA_SHA,
        train_nuisance=[list(x) for x in TRAIN_NUISANCE],
        eval_nuisance=[list(x) for x in EVAL_NUISANCE],
        query_rows=8,
        train_query_rows=6,
        eval_query_rows=2,
        selector_input_width=4,
        selector_hidden_width=8,
        port_count=2,
        parameters=58,
        selector_seeds=list(SELECTOR_SEEDS),
        optimizer="Adam",
        lr=LR,
        betas=[0.9, 0.999],
        eps=1e-8,
        weight_decay=0.0,
        steps=STEPS,
        batch_size=BATCH_SIZE,
        sampling="full-batch deterministic",
        device="cpu",
        dtype="float32",
        threads=2,
        deterministic_algorithms=True,
        downstream_pairs=[list(x) for x in UNEQUAL_PAIRS],
        downstream_unequal_pairs=6,
        placements=list(PLACEMENTS),
        downstream_rows_per_selector=24,
        gate_train_port_accuracy=1.0,
        gate_eval_port_accuracy=1.0,
        gate_query_blind_accuracy=0.5,
        gate_downstream_accuracy=1.0,
        gate_wrong_port_downstream_accuracy=0.0,
        learned_port_selector=True,
        learned_reader=False,
        learned_writer=False,
        coverage_classifier=False,
        training_steps_total=1200,
        training_examples_drawn=7200,
        selector_forward_calls_expected=1209,
        frozen_reader_forward_calls_expected=18,
        model_forward_calls_expected=1227,
        reader_training_steps=0,
        oracle_writer_operations=12,
        chunk_commits=12,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        scope=(
            "learned Port Selector only; frozen accepted C216 Readers; oracle Writer; "
            "no Coverage classifier or language"
        ),
    )


def query_dataset():
    metadata = []
    features = []
    labels = []
    split_codes = []
    for factor, target, role in (
        ("alpha", 0, (1, 0)),
        ("beta", 1, (0, 1)),
    ):
        for nuisance in TRAIN_NUISANCE + EVAL_NUISANCE:
            split = 0 if nuisance in TRAIN_NUISANCE else 1
            metadata.append(
                dict(
                    factor=factor,
                    target=target,
                    nuisance=list(nuisance),
                    split="TRAIN" if split == 0 else "EVAL",
                )
            )
            features.append((*role, *nuisance))
            labels.append(target)
            split_codes.append(split)

    arrays = dict(
        features=np.asarray(features, dtype="<f4"),
        labels=np.asarray(labels, dtype="<i8"),
        split_codes=np.asarray(split_codes, dtype="u1"),
    )
    h = hashlib.sha256(blob(metadata))
    for key in ("features", "labels", "split_codes"):
        h.update(arrays[key].tobytes())
    sha = h.hexdigest()
    require(sha == QUERY_DATA_SHA, "C217 query dataset content drift")
    train = arrays["split_codes"] == 0
    ev = arrays["split_codes"] == 1
    require(
        (
            len(metadata),
            int(train.sum()),
            int(ev.sum()),
            np.bincount(arrays["labels"][train], minlength=2).tolist(),
            np.bincount(arrays["labels"][ev], minlength=2).tolist(),
        )
        == (8, 6, 2, [3, 3], [1, 1]),
        "C217 query dataset profile drift",
    )
    return dict(metadata=metadata, content_sha256=sha, **arrays)


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


def downstream_fixture():
    bank = c216.build_bank()
    rows = []
    writer_operations = 0
    chunk_commits = 0

    eval_query = {
        "alpha": np.asarray((1, 0, 1, 1), dtype="<f4"),
        "beta": np.asarray((0, 1, 1, 1), dtype="<f4"),
    }

    for combo_id, (alpha_class, beta_class) in enumerate(UNEQUAL_PAIRS):
        state = bank.initial_state()
        state, result = bank.apply(
            state,
            _assert_op(0, memory.GLOBAL_SCOPE, "alpha", alpha_class, 1),
        )
        require(result is None, "alpha ASSERT returned read")
        writer_operations += 1
        state, commit_status = bank.commit(state)
        require(commit_status.value == "COMMITTED", "alpha commit failed")
        chunk_commits += 1

        state, result = bank.apply(
            state,
            _assert_op(1, "project", "beta", beta_class, 2),
        )
        require(result is None, "beta ASSERT returned read")
        writer_operations += 1
        hot = bank.read(state)
        require(hot.status.value == "HOT_REQUIRED", "beta must be hot")

        committed_state, commit_status = bank.commit(state)
        require(commit_status.value == "COMMITTED", "beta commit failed")
        chunk_commits += 1
        committed = bank.read(committed_state)
        require(committed.status.value == "SUPPORTED", "committed pair must be supported")
        torch.testing.assert_close(hot.value, committed.value, rtol=0.0, atol=0.0)

        for placement, read in (("HOT", hot), ("COMMITTED", committed)):
            for query, target_port, target_class in (
                ("alpha", 0, alpha_class),
                ("beta", 1, beta_class),
            ):
                rows.append(
                    dict(
                        combo_id=combo_id,
                        alpha_class=alpha_class,
                        beta_class=beta_class,
                        placement=placement,
                        query=query,
                        query_features=eval_query[query].tolist(),
                        target_port=target_port,
                        target_class=target_class,
                        port_values=[float(x) for x in read.value.tolist()],
                    )
                )

    require(len(rows) == 24, "C217 downstream row count drift")
    return rows, dict(
        oracle_writer_operations=writer_operations,
        chunk_commits=chunk_commits,
    )


def model_sha(model):
    h = hashlib.sha256()
    for name, tensor in sorted(model.state_dict().items()):
        array = tensor.detach().cpu().contiguous().numpy()
        h.update(name.encode())
        h.update(str(array.dtype).encode())
        h.update(str(tuple(array.shape)).encode())
        h.update(array.tobytes())
    return h.hexdigest()


def new_selector():
    model = selector.MemoryPortSelector(selector.MemoryPortSelectorConfig())
    require(selector.parameter_count(model) == 58, "Port Selector parameter count drift")
    return model


def fit(seed, train_x, train_y):
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)
    model = new_selector()
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
        require(torch.isfinite(loss).item(), "nonfinite Port Selector training loss")
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


def restore_readers(checkpoint_path, parent_summary):
    payload = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    require(
        payload["schema"] == "fold-v5f-reader-checkpoints-v1"
        and tuple(payload["seeds"]) == READER_SEEDS
        and payload["config"] == dict(input_width=1, hidden_width=8, answer_classes=3),
        "C216 Reader checkpoint bundle identity drift",
    )
    expected = {
        int(row["seed"]): row["final_sha256"]
        for row in parent_summary["validation_summary"]["seed_records"]
    }
    require(
        tuple(expected[s] for s in READER_SEEDS) == READER_FINAL_SHA256,
        "C216 Reader final fingerprints drift",
    )
    readers = {}
    for seed, state_dict in zip(READER_SEEDS, payload["state_dicts"], strict=True):
        model = c216.new_reader()
        model.load_state_dict(state_dict, strict=True)
        model.eval()
        require(c216.model_sha(model) == expected[seed], "Frozen Reader checkpoint changed")
        readers[seed] = model
    return readers


def accuracy(pred, target):
    return float((pred == target).to(torch.float64).mean().item())


def score_selector(model, query_data, rows, readers):
    x = torch.from_numpy(query_data["features"].copy()).to(torch.float32)
    y = torch.from_numpy(query_data["labels"].copy()).to(torch.int64)
    split = torch.from_numpy(query_data["split_codes"].copy()).to(torch.int64)
    train = split == 0
    ev = split == 1
    with torch.no_grad():
        train_pred = model(x[train]).argmax(dim=-1)
        eval_pred = model(x[ev]).argmax(dim=-1)
        blind_x = x[ev].clone()
        blind_x[:, :2] = 0.0
        blind_pred = model(blind_x).argmax(dim=-1)

    eval_rows = [query_data["metadata"][i] for i in torch.nonzero(ev).squeeze(-1).tolist()]
    predicted_port_by_query = {
        row["factor"]: int(eval_pred[i].item()) for i, row in enumerate(eval_rows)
    }
    require(set(predicted_port_by_query) == {"alpha", "beta"}, "EVAL query mapping incomplete")

    selected = []
    wrong = []
    target = []
    placement = []
    row_keys = []
    for row in rows:
        predicted_port = predicted_port_by_query[row["query"]]
        selected.append((row["port_values"][predicted_port],))
        wrong.append((row["port_values"][1 - predicted_port],))
        target.append(row["target_class"])
        placement.append(0 if row["placement"] == "HOT" else 1)
        row_keys.append((row["combo_id"], row["query"]))

    selected_x = torch.tensor(selected, dtype=torch.float32)
    wrong_x = torch.tensor(wrong, dtype=torch.float32)
    target_y = torch.tensor(target, dtype=torch.int64)
    placement_t = torch.tensor(placement, dtype=torch.int64)

    reader_records = []
    frozen_reader_forward_calls = 0
    for reader_seed in READER_SEEDS:
        frozen = readers[reader_seed]
        before = c216.model_sha(frozen)
        with torch.no_grad():
            pred = frozen(selected_x).argmax(dim=-1)
            wrong_pred = frozen(wrong_x).argmax(dim=-1)
        frozen_reader_forward_calls += 2
        after = c216.model_sha(frozen)
        require(before == after == READER_FINAL_SHA256[READER_SEEDS.index(reader_seed)],
                "Frozen Reader weights changed")

        keyed = {}
        for i, key in enumerate(row_keys):
            keyed.setdefault(key, {})[int(placement_t[i].item())] = int(pred[i].item())
        require(all(set(v) == {0, 1} for v in keyed.values()), "placement pair incomplete")
        placement_mismatches = sum(int(v[0] != v[1]) for v in keyed.values())

        hot = placement_t == 0
        committed = placement_t == 1
        reader_records.append(
            dict(
                reader_seed=reader_seed,
                downstream_accuracy=accuracy(pred, target_y),
                downstream_hot_accuracy=accuracy(pred[hot], target_y[hot]),
                downstream_committed_accuracy=accuracy(pred[committed], target_y[committed]),
                wrong_port_downstream_accuracy=accuracy(wrong_pred, target_y),
                placement_prediction_mismatches=placement_mismatches,
            )
        )

    return dict(
        train_port_accuracy=accuracy(train_pred, y[train]),
        eval_port_accuracy=accuracy(eval_pred, y[ev]),
        query_blind_eval_accuracy=accuracy(blind_pred, y[ev]),
        train_port_predictions=train_pred.tolist(),
        eval_port_predictions=eval_pred.tolist(),
        blind_port_predictions=blind_pred.tolist(),
        reader_records=reader_records,
        selector_scoring_forward_calls=3,
        frozen_reader_forward_calls=frozen_reader_forward_calls,
    )


def selector_seed_pass(record):
    return (
        record.get("train_port_accuracy") == 1.0
        and record.get("eval_port_accuracy") == 1.0
        and record.get("query_blind_eval_accuracy") == 0.5
        and record.get("checkpoint_roundtrip") is True
        and len(record.get("reader_records", [])) == 3
        and all(
            reader_record.get("downstream_accuracy") == 1.0
            and reader_record.get("downstream_hot_accuracy") == 1.0
            and reader_record.get("downstream_committed_accuracy") == 1.0
            and reader_record.get("wrong_port_downstream_accuracy") == 0.0
            and reader_record.get("placement_prediction_mismatches") == 0
            for reader_record in record["reader_records"]
        )
    )


def gate(summary):
    records = summary.get("selector_seed_records")
    return (
        isinstance(records, list)
        and len(records) == 3
        and [r.get("seed") for r in records] == list(SELECTOR_SEEDS)
        and all(selector_seed_pass(r) for r in records)
        and summary.get("all_selector_checkpoint_roundtrips") is True
        and summary.get("all_reader_checkpoint_roundtrips") is True
        and summary.get("query_data_sha256") == QUERY_DATA_SHA
        and summary.get("downstream_rows") == 24
        and summary.get("learned_selector_calls") == 1209
        and summary.get("frozen_reader_forward_calls") == 18
        and summary.get("reader_training_steps") == 0
        and summary.get("learned_writer_calls") == 0
        and summary.get("coverage_classifier_calls") == 0
        and summary.get("oracle_writer_operations") == 12
        and summary.get("chunk_commits") == 12
    )


def precheck(c216_summary, root):
    root = Path(root)
    require(audit.sha(c216_summary) == PARENT_C216_SHA, "C216 summary changed")
    p216 = audit.read_json(c216_summary)
    c216.validate_result(p216)
    require(
        p216.get("commit_sha") == PARENT_C216_EXECUTION
        and p216.get("status") == "PASS"
        and c216.gate(p216["validation_summary"])
        and len(p216.get("source_blobs", {})) == 130,
        "Wrong accepted C216 parent",
    )

    pins = dict(p216["source_blobs"])
    protected = {str(Path(c216_summary).resolve()): PARENT_C216_SHA}
    validation_seen = False
    reader_checkpoint_seen = False
    for artifact in p216["artifacts"]:
        path = audit.safe_child(Path(c216_summary).resolve().parent, artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C216 artifact:" + artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]
        if artifact["file"] == "validation-summary.json":
            require(artifact["sha256"] == PARENT_C216_VALIDATION_SHA,
                    "C216 validation artifact changed")
            validation_seen = True
        if artifact["file"] == "reader-checkpoints.pt":
            require(artifact["sha256"] == PARENT_READER_CHECKPOINT_SHA,
                    "C216 Reader checkpoint artifact changed")
            reader_checkpoint_seen = True
    require(validation_seen and reader_checkpoint_seen, "C216 deciding artifact missing")

    for name, expected_blob in pins.items():
        actual = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
        require(actual == expected_blob, "C216 source pin changed:" + name)

    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()

    for dependency in DIRECT_REPO_DEPENDENCIES:
        require(dependency in allpins, "Unpinned direct dependency:" + dependency)

    protected.update(audit.protect_tree_files(root, allpins))
    pins.update({name: allpins[name] for name in OWN})

    require(len(pins) == 137, "C217 source pin count drift")
    require(len(protected) == 143, "C217 protected input count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C217 manifest drift")
    return p216, pins, protected


def regression_modules(root):
    names = c216.regression_modules(root)
    require(len(names) == len(set(names)) == 101, "Historical regression module drift")
    return names + ["tests_lm.test_v05_c217_learned_port_selector"]


def regression_suite(root):
    names = regression_modules(root)
    loaded = unittest.defaultTestLoader.loadTestsFromNames(names)
    tests = list(c205._iter_tests(loaded))
    ids = [test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded) == 1, "Historical dynamic test identity drift:" + excluded)
    kept = [test for test in tests if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS]
    require(
        len(tests) == 2222
        and len(kept) == 2221
        and not any(test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS for test in kept),
        "C217 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C217",
    )
    require(
        len(payload["source_blobs"]) == 137
        and len(payload["input_sha256"]) == 143
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C217 coverage drift",
    )
    require(
        payload["trained_selector_models"] == 3
        and payload["selector_parameters_per_model"] == 58
        and payload["training_steps_total"] == 1200
        and payload["training_examples_drawn"] == 7200
        and payload["learned_selector_calls"] == 1209
        and payload["frozen_reader_forward_calls"] == 18
        and payload["model_forward_calls"] == 1227
        and payload["reader_training_steps"] == 0
        and payload["oracle_writer_operations"] == 12
        and payload["chunk_commits"] == 12
        and payload["network_calls"] == 0,
        "C217 workload drift",
    )
    require(
        payload["production_runtime_modified"] is True
        and payload["gate_f_candidate"] is False
        and payload["learned_port_selector"] is True
        and payload["learned_reader"] is False
        and payload["learned_writer"] is False
        and payload["coverage_classifier"] is False,
        "C217 scope drift",
    )
    require(
        payload["status"] == ("PASS" if gate(payload["validation_summary"]) else "FAIL"),
        "C217 gate drift",
    )


def run(*, c216_summary, output_dir, expected_head):
    root = Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root, "rev-parse", "HEAD").decode().strip() == expected_head,
                "HEAD mismatch")
        require(audit.git(root, "branch", "--show-current").decode().strip()
                == "feat/sft-target-loss", "Branch mismatch")
        require(not audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    p216, pins, protected = precheck(c216_summary, root)
    data = query_dataset()
    rows, downstream_counts = downstream_fixture()

    c216_dir = Path(c216_summary).resolve().parent
    readers = restore_readers(c216_dir / "reader-checkpoints.pt", p216)
    reader_roundtrip = all(
        c216.model_sha(readers[seed]) == READER_FINAL_SHA256[i]
        for i, seed in enumerate(READER_SEEDS)
    )

    train_mask = data["split_codes"] == 0
    train_x = torch.from_numpy(data["features"][train_mask].copy()).to(torch.float32)
    train_y = torch.from_numpy(data["labels"][train_mask].copy()).to(torch.int64)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=False)
    artifacts = []

    def record(name):
        path = out / name
        artifacts.append(dict(file=name, sha256=audit.sha(path),
                              serialized_bytes=path.stat().st_size))

    def save_json(name, value):
        (out / name).write_bytes(blob(value))
        record(name)

    save_json("selector-plan.json", dict(manifest(), source_blobs=pins))
    np.savez_compressed(
        out / "selector-dataset.npz",
        features=data["features"],
        labels=data["labels"],
        split_codes=data["split_codes"],
    )
    record("selector-dataset.npz")

    fit_records = []
    state_dicts = []
    for seed in SELECTOR_SEEDS:
        model, fit_record = fit(seed, train_x, train_y)
        fit_records.append(fit_record)
        state_dicts.append(
            {name: tensor.detach().cpu().clone() for name, tensor in model.state_dict().items()}
        )

    bundle = dict(
        schema="fold-v5f-port-selector-checkpoints-v1",
        seeds=list(SELECTOR_SEEDS),
        config=dict(input_width=4, hidden_width=8, port_count=2),
        state_dicts=state_dicts,
    )
    torch.save(bundle, out / "selector-checkpoints.pt")
    record("selector-checkpoints.pt")

    restored_bundle = torch.load(out / "selector-checkpoints.pt", map_location="cpu",
                                 weights_only=True)
    require(
        restored_bundle["schema"] == "fold-v5f-port-selector-checkpoints-v1"
        and tuple(restored_bundle["seeds"]) == SELECTOR_SEEDS
        and restored_bundle["config"] == dict(input_width=4, hidden_width=8, port_count=2),
        "Port Selector checkpoint bundle identity drift",
    )

    seed_records = []
    selector_roundtrips = []
    for seed, state_dict, fit_record in zip(
        SELECTOR_SEEDS, restored_bundle["state_dicts"], fit_records, strict=True
    ):
        restored = new_selector()
        restored.load_state_dict(state_dict, strict=True)
        restored.eval()
        final_sha = model_sha(restored)
        roundtrip = final_sha == fit_record["final_sha256"]
        selector_roundtrips.append(roundtrip)
        score = score_selector(restored, data, rows, readers)
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

    save_json("evaluation.json", dict(
        selector_seed_records=seed_records,
        fit_records=fit_records,
        downstream_rows=rows,
    ))

    learned_selector_calls = sum(r["training_forward_calls"] for r in fit_records) + sum(
        r["selector_scoring_forward_calls"] for r in seed_records
    )
    frozen_reader_forward_calls = sum(r["frozen_reader_forward_calls"] for r in seed_records)

    summary = dict(
        selector_seed_records=seed_records,
        all_selector_checkpoint_roundtrips=all(selector_roundtrips),
        all_reader_checkpoint_roundtrips=reader_roundtrip,
        query_data_sha256=data["content_sha256"],
        downstream_rows=len(rows),
        learned_selector_calls=learned_selector_calls,
        frozen_reader_forward_calls=frozen_reader_forward_calls,
        reader_training_steps=0,
        learned_writer_calls=0,
        coverage_classifier_calls=0,
        oracle_writer_operations=downstream_counts["oracle_writer_operations"],
        chunk_commits=downstream_counts["chunk_commits"],
    )
    save_json("validation-summary.json", summary)

    guard()
    precheck(c216_summary, root)
    for path, wanted in protected.items():
        require(audit.sha(path) == wanted, "Protected input changed:" + path)
    for artifact in artifacts:
        require(audit.sha(out / artifact["file"]) == artifact["sha256"],
                "Output changed:" + artifact["file"])

    result = dict(
        experiment_id=EXPERIMENT_ID,
        stage=STAGE,
        commit_sha=expected_head,
        status="PASS" if gate(summary) else "FAIL",
        diagnostic_execution_valid=True,
        C216_summary_sha256=PARENT_C216_SHA,
        source_blobs=pins,
        input_sha256=protected,
        artifacts=artifacts,
        validation_summary=summary,
        fit_records=fit_records,
        trained_selector_models=3,
        selector_parameters_per_model=58,
        training_steps_total=sum(r["steps"] for r in fit_records),
        training_examples_drawn=sum(r["examples_drawn"] for r in fit_records),
        learned_selector_calls=learned_selector_calls,
        frozen_reader_forward_calls=frozen_reader_forward_calls,
        model_forward_calls=learned_selector_calls + frozen_reader_forward_calls,
        reader_training_steps=0,
        oracle_writer_operations=downstream_counts["oracle_writer_operations"],
        chunk_commits=downstream_counts["chunk_commits"],
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        learned_port_selector=True,
        learned_reader=False,
        learned_writer=False,
        coverage_classifier=False,
        limitations=[
            "tiny synthetic two-port query-routing pilot",
            "query descriptor contains explicit alpha/beta role channels plus nuisance channels",
            "accepted C216 Readers are frozen; no Reader co-adaptation",
            "Writer and memory construction are oracle/deterministic",
            "no Coverage classifier, natural language, memory-cost advantage or Gate F claim",
        ],
    )
    validate_result(result)
    (out / "summary.json").write_bytes(blob(result))
    print(
        "[C217] learned Port Selector "
        + " ".join(
            f"seed={r['seed']} eval={r['eval_port_accuracy']:.3f} blind={r['query_blind_eval_accuracy']:.3f}"
            for r in seed_records
        ),
        flush=True,
    )
    print("=== C217 RESULT ===", flush=True)
    print(blob(result).decode(), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c216-summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
