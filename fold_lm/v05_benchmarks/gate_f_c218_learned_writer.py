"""C218: V5-F learned semantic Writer pilot with frozen Selector/Readers.

One changed scientific component: a learned Writer maps a structured observation descriptor to one
of six factor+relation classes. ASSERT/REPLACE operation kind remains oracle. Accepted C217 Port
Selectors and C216 Readers are frozen. Coverage classification remains absent.
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
from fold_lm.v05 import memory_writer as writer
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_f_c216_learned_reader as c216
from fold_lm.v05_benchmarks import gate_f_c217_learned_port_selector as c217

EXPERIMENT_ID = "C218-v5f-learned-semantic-writer-pilot"
STAGE = "V5-F-LEARNED-SEMANTIC-WRITER-PILOT"
BASE = "cb36cf3a277105ddb4af38f189e4aef79da018fd"
PARENT_C217_EXECUTION = "a6aac1273951b6e321573445e9f759f35fffb726"
PARENT_C217_SHA = "cb27e93c9a6dc9d03875938c55c37f146c12278dec4c9ebb5a20da150fd847ab"
PARENT_C217_VALIDATION_SHA = "7e46f83fc7c6702e36ede2d05f016018cf8d219c51248ef7d395815168409cf0"
PARENT_SELECTOR_CHECKPOINT_SHA = "ab8892e6562a4801a30fea853fdbc712d69d9c5077e32c0b8fab6e555fead215"
INHERITED_READER_CHECKPOINT_SHA = "bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af"
WRITER_DATA_SHA = "06f8df444119f0332168a956e7f32e9690b88fa9c39749d3ecc2283c70213714"
MANIFEST_SHA = "29b488831dc74e7060387a56368a48ca53aff5592ea767e397dc64db2264e034"

VALUES = (-1, 0, 1)
RELATION_CLASSES = (
    "alpha-class-0",
    "alpha-class-1",
    "alpha-class-2",
    "beta-class-0",
    "beta-class-1",
    "beta-class-2",
)
TRAIN_NUISANCE = ((-1, -1), (-1, 1), (1, -1))
EVAL_NUISANCE = ((1, 1),)
WRITER_SEEDS = (218001, 218002, 218003)
SELECTOR_SEEDS = (217001, 217002, 217003)
SELECTOR_FINAL_SHA256 = (
    "f06d20a68adb56317c92fcd401b41d28ef324739330fb5b687485c32429e633d",
    "d59d6f8b7cf9bbc00dbbffbb33829df5245b6021361b07ce802ada8cf73eac21",
    "ab42caf7444f5e6a29977b35e135d388f0336e12311832132313a1f846d69a3a",
)
READER_SEEDS = (216001, 216002, 216003)
READER_FINAL_SHA256 = (
    "6f1219b4277e3d4af6494ecf2280f2442887df05d5d133f2e2566b29bf804336",
    "1b7b2f96ad3e33d4ac0422cd7ca72b7f6e53707acf52aa17a44f188b7c2ed199",
    "3d26451e54a8e4327f2dcc9128e73c7e3fc60605c3e2d894876bd65057d2dd7f",
)
UNEQUAL_PAIRS = ((0,1),(0,2),(1,0),(1,2),(2,0),(2,1))
STEPS = 400
BATCH_SIZE = 18
LR = 0.02

OWN = (
    "fold_lm/v05/memory_writer.py",
    "fold_lm/v05_benchmarks/gate_f_c218_learned_writer.py",
    "tests_lm/test_v05_c218_learned_writer.py",
    "tools/run_c218.ps1",
    "tools/invoke_c218.ps1",
    "docs/experiment-ledger-addendum-c218-preregistration.md",
    "docs/v5f-learned-writer-pilot-v0.1.md",
)
OUTPUTS = {
    "writer-plan.json",
    "writer-dataset.npz",
    "writer-checkpoints.pt",
    "evaluation.json",
    "validation-summary.json",
}
DIRECT_REPO_DEPENDENCIES = (
    "fold_lm/v05/memory_bank.py",
    "fold_lm/v05/memory_bridge.py",
    "fold_lm/v05/memory_capsule_bridge.py",
    "fold_lm/v05/memory_reader.py",
    "fold_lm/v05/memory_port_selector.py",
    "fold_lm/v05/memory_writer.py",
    "fold_lm/v05_benchmarks/gate_e_c175_frozen_prediction_audit.py",
    "fold_lm/v05_benchmarks/gate_e_c205_phase0_batch_composition_attribution.py",
    "fold_lm/v05_benchmarks/gate_f_c215_h1_h2_chunk_commit.py",
    "fold_lm/v05_benchmarks/gate_f_c216_learned_reader.py",
    "fold_lm/v05_benchmarks/gate_f_c217_learned_port_selector.py",
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
        parent_c217_execution=PARENT_C217_EXECUTION,
        parent_c217_sha256=PARENT_C217_SHA,
        parent_c217_validation_sha256=PARENT_C217_VALIDATION_SHA,
        parent_selector_checkpoint_sha256=PARENT_SELECTOR_CHECKPOINT_SHA,
        inherited_reader_checkpoint_sha256=INHERITED_READER_CHECKPOINT_SHA,
        writer_data_sha256=WRITER_DATA_SHA,
        semantic_values=list(VALUES),
        relation_classes=list(RELATION_CLASSES),
        train_nuisance=[list(x) for x in TRAIN_NUISANCE],
        eval_nuisance=[list(x) for x in EVAL_NUISANCE],
        rows=24,
        train_rows=18,
        eval_rows=6,
        writer_input_width=5,
        writer_hidden_width=12,
        relation_class_count=6,
        parameters=150,
        writer_seeds=list(WRITER_SEEDS),
        optimizer="Adam",
        lr=LR,
        betas=[0.9,0.999],
        eps=1e-8,
        weight_decay=0.0,
        steps=STEPS,
        batch_size=BATCH_SIZE,
        sampling="full-batch deterministic",
        device="cpu",
        dtype="float32",
        threads=2,
        deterministic_algorithms=True,
        gate_train_relation_accuracy=1.0,
        gate_eval_relation_accuracy=1.0,
        gate_factor_blind_accuracy=0.5,
        gate_semantic_blind_accuracy=1.0/3.0,
        operation_kind="oracle ASSERT/REPLACE",
        downstream_assert_pairs=[list(x) for x in UNEQUAL_PAIRS],
        downstream_assert_rows_per_writer=24,
        downstream_replace_rows_per_writer=6,
        gate_assert_downstream_accuracy=1.0,
        gate_replace_downstream_accuracy=1.0,
        gate_wrong_semantic_control_accuracy=0.0,
        gate_wrong_factor_control_accuracy=0.0,
        frozen_selector_checkpoints=3,
        frozen_reader_checkpoints=3,
        selector_final_sha256=list(SELECTOR_FINAL_SHA256),
        reader_final_sha256=list(READER_FINAL_SHA256),
        training_steps_total=1200,
        training_examples_drawn=21600,
        learned_writer_forward_calls_expected=1212,
        frozen_selector_forward_calls_expected=3,
        frozen_reader_forward_calls_expected=72,
        model_forward_calls_expected=1287,
        learned_writer_operation_attempts=54,
        oracle_writer_operations=60,
        control_writer_operations=12,
        chunk_commits=96,
        reader_training_steps=0,
        selector_training_steps=0,
        coverage_classifier=False,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        scope=(
            "learned factor+relation Writer only; oracle operation kind; frozen accepted C217 "
            "selectors/C216 Readers; no Coverage classifier or language"
        ),
    )


def writer_dataset():
    metadata = []
    features = []
    labels = []
    split_codes = []
    for factor, factor_index, role in (
        ("alpha", 0, (1, 0)),
        ("beta", 1, (0, 1)),
    ):
        for class_id, semantic in enumerate(VALUES):
            target = factor_index * 3 + class_id
            for nuisance in TRAIN_NUISANCE + EVAL_NUISANCE:
                split = 0 if nuisance in TRAIN_NUISANCE else 1
                metadata.append(dict(
                    factor=factor,
                    class_id=class_id,
                    semantic=semantic,
                    target=target,
                    nuisance=list(nuisance),
                    split="TRAIN" if split == 0 else "EVAL",
                ))
                features.append((*role, semantic, *nuisance))
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
    require(sha == WRITER_DATA_SHA, "C218 Writer dataset content drift")

    train = arrays["split_codes"] == 0
    ev = arrays["split_codes"] == 1
    require(
        (
            len(metadata),
            int(train.sum()),
            int(ev.sum()),
            np.bincount(arrays["labels"][train], minlength=6).tolist(),
            np.bincount(arrays["labels"][ev], minlength=6).tolist(),
        )
        == (24, 18, 6, [3,3,3,3,3,3], [1,1,1,1,1,1]),
        "C218 Writer dataset profile drift",
    )
    return dict(metadata=metadata, content_sha256=sha, **arrays)


def model_sha(model):
    h = hashlib.sha256()
    for name, tensor in sorted(model.state_dict().items()):
        array = tensor.detach().cpu().contiguous().numpy()
        h.update(name.encode())
        h.update(str(array.dtype).encode())
        h.update(str(tuple(array.shape)).encode())
        h.update(array.tobytes())
    return h.hexdigest()


def new_writer():
    model = writer.MemoryWriter(writer.MemoryWriterConfig())
    require(writer.parameter_count(model) == 150, "Writer parameter count drift")
    return model


def fit(seed, train_x, train_y):
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)
    model = new_writer()
    initial_sha = model_sha(model)
    optimizer = torch.optim.Adam(
        model.parameters(), lr=LR, betas=(0.9,0.999), eps=1e-8, weight_decay=0.0
    )
    started = time.perf_counter()
    initial_loss = None
    final_loss = None
    for step in range(STEPS):
        optimizer.zero_grad(set_to_none=True)
        logits = model(train_x)
        loss = F.cross_entropy(logits, train_y)
        require(torch.isfinite(loss).item(), "nonfinite Writer training loss")
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
        fit_wall_clock_seconds=time.perf_counter()-started,
        training_forward_calls=STEPS,
    )


def accuracy(pred, target):
    return float((pred == target).to(torch.float64).mean().item())


def score_writer(model, data):
    x = torch.from_numpy(data["features"].copy()).to(torch.float32)
    y = torch.from_numpy(data["labels"].copy()).to(torch.int64)
    split = torch.from_numpy(data["split_codes"].copy()).to(torch.int64)
    train = split == 0
    ev = split == 1
    with torch.no_grad():
        train_pred = model(x[train]).argmax(dim=-1)
        eval_pred = model(x[ev]).argmax(dim=-1)
        factor_blind_x = x[ev].clone()
        factor_blind_x[:, :2] = 0.0
        factor_blind_pred = model(factor_blind_x).argmax(dim=-1)
        semantic_blind_x = x[ev].clone()
        semantic_blind_x[:, 2] = 0.0
        semantic_blind_pred = model(semantic_blind_x).argmax(dim=-1)

    eval_indices = torch.nonzero(ev, as_tuple=False).squeeze(-1).tolist()
    prediction_by_target = {
        int(data["metadata"][row]["target"]): int(eval_pred[i].item())
        for i, row in enumerate(eval_indices)
    }
    require(set(prediction_by_target) == set(range(6)), "EVAL Writer target map incomplete")
    return dict(
        train_relation_accuracy=accuracy(train_pred, y[train]),
        eval_relation_accuracy=accuracy(eval_pred, y[ev]),
        factor_blind_eval_accuracy=accuracy(factor_blind_pred, y[ev]),
        semantic_blind_eval_accuracy=accuracy(semantic_blind_pred, y[ev]),
        train_predictions=train_pred.tolist(),
        eval_predictions=eval_pred.tolist(),
        factor_blind_predictions=factor_blind_pred.tolist(),
        semantic_blind_predictions=semantic_blind_pred.tolist(),
        prediction_by_target=prediction_by_target,
        writer_scoring_forward_calls=4,
    )


def decode_write_class(class_index):
    if type(class_index) is not int or not 0 <= class_index < 6:
        raise ValueError("Writer class out of range")
    factor = "alpha" if class_index < 3 else "beta"
    semantic_class = class_index if class_index < 3 else class_index - 3
    scope = memory.GLOBAL_SCOPE if factor == "alpha" else "project"
    return factor, semantic_class, scope, f"{factor}-class-{semantic_class}"


def memory_op(kind, state, class_index, evidence_time, source):
    factor, _, scope, relation = decode_write_class(class_index)
    return memory.MemoryOp(
        kind=kind,
        expected_memory_revision=state.memory_revision,
        scope_id=scope,
        factor_id=factor,
        relation_key=relation,
        source_id=source,
        evidence_time=evidence_time,
    )


def oracle_assert(bank, state, class_index, evidence_time, source):
    op = memory_op(memory.MemoryOpKind.ASSERT, state, class_index, evidence_time, source)
    state, read = bank.apply(state, op)
    require(read is None, "oracle ASSERT unexpectedly returned read")
    state, status = bank.commit(state)
    require(status.value == "COMMITTED", "oracle ASSERT commit failed")
    return state


def oracle_initial_state(bank, alpha_class, beta_class, source_prefix):
    state = bank.initial_state()
    state = oracle_assert(bank, state, alpha_class, 1, source_prefix + ":alpha")
    state = oracle_assert(bank, state, 3 + beta_class, 2, source_prefix + ":beta")
    return state


def restore_selectors(checkpoint_path, parent_summary):
    payload = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    require(
        payload["schema"] == "fold-v5f-port-selector-checkpoints-v1"
        and tuple(payload["seeds"]) == SELECTOR_SEEDS
        and payload["config"] == dict(input_width=4, hidden_width=8, port_count=2),
        "C217 selector checkpoint bundle identity drift",
    )
    expected = {
        int(row["seed"]): row["final_sha256"]
        for row in parent_summary["validation_summary"]["selector_seed_records"]
    }
    require(tuple(expected[s] for s in SELECTOR_SEEDS) == SELECTOR_FINAL_SHA256,
            "C217 selector final fingerprints drift")
    models = {}
    for seed, state_dict in zip(SELECTOR_SEEDS, payload["state_dicts"], strict=True):
        model = c217.new_selector()
        model.load_state_dict(state_dict, strict=True)
        model.eval()
        require(c217.model_sha(model) == expected[seed], "Frozen selector changed")
        models[seed] = model
    return models


def find_protected_input(parent_summary, basename, expected_sha):
    matches = [
        Path(name)
        for name, sha in parent_summary["input_sha256"].items()
        if name.replace("\\", "/").endswith("/" + basename) and sha == expected_sha
    ]
    require(len(matches) == 1, "Protected inherited artifact resolution drift:" + basename)
    require(matches[0].is_file() and audit.sha(matches[0]) == expected_sha,
            "Protected inherited artifact changed:" + basename)
    return matches[0]


def restore_readers(parent_summary):
    checkpoint = find_protected_input(
        parent_summary, "reader-checkpoints.pt", INHERITED_READER_CHECKPOINT_SHA
    )
    payload = torch.load(checkpoint, map_location="cpu", weights_only=True)
    require(
        payload["schema"] == "fold-v5f-reader-checkpoints-v1"
        and tuple(payload["seeds"]) == READER_SEEDS
        and payload["config"] == dict(input_width=1, hidden_width=8, answer_classes=3),
        "C216 Reader checkpoint bundle identity drift",
    )
    models = {}
    for seed, state_dict, expected_sha in zip(
        READER_SEEDS, payload["state_dicts"], READER_FINAL_SHA256, strict=True
    ):
        model = c216.new_reader()
        model.load_state_dict(state_dict, strict=True)
        model.eval()
        require(c216.model_sha(model) == expected_sha, "Frozen Reader changed")
        models[seed] = model
    return models


def frozen_routes(selectors):
    x = torch.tensor([[1,0,1,1],[0,1,1,1]], dtype=torch.float32)
    routes = {}
    for seed in SELECTOR_SEEDS:
        before = c217.model_sha(selectors[seed])
        with torch.no_grad():
            pred = selectors[seed](x).argmax(dim=-1)
        require(c217.model_sha(selectors[seed]) == before == SELECTOR_FINAL_SHA256[
            SELECTOR_SEEDS.index(seed)
        ], "Frozen selector mutated")
        routes[seed] = {"alpha": int(pred[0].item()), "beta": int(pred[1].item())}
    require(all(route == {"alpha":0,"beta":1} for route in routes.values()),
            "Frozen selector route drift")
    return routes


def learned_assert_rows(prediction_by_target, writer_seed):
    bank = c216.build_bank()
    rows = []
    rejections = 0
    learned_ops = 0
    commits = 0
    for combo_id, (alpha_class, beta_class) in enumerate(UNEQUAL_PAIRS):
        state = bank.initial_state()
        valid = True
        try:
            learned_ops += 1
            state, read = bank.apply(
                state,
                memory_op(
                    memory.MemoryOpKind.ASSERT,
                    state,
                    prediction_by_target[alpha_class],
                    1,
                    f"writer:{writer_seed}:assert:{combo_id}:alpha",
                ),
            )
            require(read is None, "learned alpha ASSERT returned read")
            state, status = bank.commit(state)
            require(status.value == "COMMITTED", "learned alpha commit failed")
            commits += 1

            learned_ops += 1
            state, read = bank.apply(
                state,
                memory_op(
                    memory.MemoryOpKind.ASSERT,
                    state,
                    prediction_by_target[3 + beta_class],
                    2,
                    f"writer:{writer_seed}:assert:{combo_id}:beta",
                ),
            )
            require(read is None, "learned beta ASSERT returned read")
            hot = bank.read(state)
            require(hot.status.value == "HOT_REQUIRED", "learned beta must be hot")
            state, status = bank.commit(state)
            require(status.value == "COMMITTED", "learned beta commit failed")
            commits += 1
            committed = bank.read(state)
            require(committed.status.value == "SUPPORTED", "learned committed read unsupported")
            torch.testing.assert_close(hot.value, committed.value, rtol=0.0, atol=0.0)
            values = {
                "HOT": [float(v) for v in hot.value.tolist()],
                "COMMITTED": [float(v) for v in committed.value.tolist()],
            }
        except (ValueError, RuntimeError, AssertionError):
            valid = False
            rejections += 1
            values = {"HOT":[0.0,0.0], "COMMITTED":[0.0,0.0]}

        for placement in ("HOT","COMMITTED"):
            for query, target in (("alpha",alpha_class),("beta",beta_class)):
                rows.append(dict(
                    row_type="ASSERT",
                    combo_id=combo_id,
                    placement=placement,
                    query=query,
                    target_class=target,
                    valid=valid,
                    port_values=values[placement],
                ))
    return rows, dict(
        learned_writer_operation_attempts=learned_ops,
        oracle_writer_operations=0,
        control_writer_operations=0,
        chunk_commits=commits,
        write_rejections=rejections,
    )


def learned_replace_rows(prediction_by_target, writer_seed):
    bank = c216.build_bank()
    rows = []
    rejections = 0
    learned_ops = 0
    oracle_ops = 0
    commits = 0
    for target_class in range(6):
        factor, semantic_class, _, _ = decode_write_class(target_class)
        if factor == "alpha":
            alpha_initial = (semantic_class + 1) % 3
            beta_initial = (semantic_class + 2) % 3
        else:
            beta_initial = (semantic_class + 1) % 3
            alpha_initial = (semantic_class + 2) % 3

        oracle_ops += 2
        commits += 2
        state = oracle_initial_state(
            bank, alpha_initial, beta_initial,
            f"oracle:{writer_seed}:replace:{target_class}"
        )
        valid = True
        try:
            learned_ops += 1
            state, read = bank.apply(
                state,
                memory_op(
                    memory.MemoryOpKind.REPLACE,
                    state,
                    prediction_by_target[target_class],
                    3,
                    f"writer:{writer_seed}:replace:{target_class}",
                ),
            )
            require(read is None, "learned REPLACE returned read")
            result = bank.read(state)
            require(result.status.value == "SUPPORTED", "learned REPLACE read unsupported")
            values = [float(v) for v in result.value.tolist()]
        except (ValueError, RuntimeError, AssertionError):
            valid = False
            rejections += 1
            values = [0.0,0.0]

        rows.append(dict(
            row_type="REPLACE",
            target_relation_class=target_class,
            query=factor,
            target_class=semantic_class,
            valid=valid,
            port_values=values,
        ))
    return rows, dict(
        learned_writer_operation_attempts=learned_ops,
        oracle_writer_operations=oracle_ops,
        control_writer_operations=0,
        chunk_commits=commits,
        write_rejections=rejections,
    )


def control_replace_rows(control_kind):
    require(control_kind in ("WRONG_SEMANTIC","WRONG_FACTOR"), "unknown Writer control")
    bank = c216.build_bank()
    rows = []
    oracle_ops = 0
    control_ops = 0
    commits = 0
    for target_class in range(6):
        factor, semantic_class, _, _ = decode_write_class(target_class)
        if factor == "alpha":
            alpha_initial = (semantic_class + 1) % 3
            beta_initial = (semantic_class + 2) % 3
        else:
            beta_initial = (semantic_class + 1) % 3
            alpha_initial = (semantic_class + 2) % 3
        oracle_ops += 2
        commits += 2
        state = oracle_initial_state(
            bank, alpha_initial, beta_initial,
            f"oracle:control:{control_kind}:{target_class}"
        )

        if control_kind == "WRONG_SEMANTIC":
            forced_class = (0 if factor == "alpha" else 3) + ((semantic_class + 1) % 3)
        else:
            forced_class = (3 + semantic_class) if factor == "alpha" else semantic_class

        control_ops += 1
        state, read = bank.apply(
            state,
            memory_op(
                memory.MemoryOpKind.REPLACE,
                state,
                forced_class,
                3,
                f"control:{control_kind}:{target_class}",
            ),
        )
        require(read is None, "control REPLACE returned read")
        result = bank.read(state)
        require(result.status.value == "SUPPORTED", "control REPLACE unsupported")
        rows.append(dict(
            row_type=control_kind,
            target_relation_class=target_class,
            query=factor,
            target_class=semantic_class,
            valid=True,
            port_values=[float(v) for v in result.value.tolist()],
        ))
    return rows, dict(
        learned_writer_operation_attempts=0,
        oracle_writer_operations=oracle_ops,
        control_writer_operations=control_ops,
        chunk_commits=commits,
        write_rejections=0,
    )


def evaluate_rows(rows, routes, readers, *, placement_sensitive=False):
    total = 0
    correct = 0
    hot_total = 0
    hot_correct = 0
    committed_total = 0
    committed_correct = 0
    placement_mismatches = 0
    frozen_reader_calls = 0
    combo_records = []

    for selector_seed in SELECTOR_SEEDS:
        for reader_seed in READER_SEEDS:
            x = []
            target = []
            valid = []
            placements = []
            keys = []
            for row in rows:
                port = routes[selector_seed][row["query"]]
                x.append((row["port_values"][port],))
                target.append(row["target_class"])
                valid.append(bool(row["valid"]))
                placements.append(row.get("placement"))
                keys.append((row.get("combo_id"), row["query"]))

            x_t = torch.tensor(x, dtype=torch.float32)
            y_t = torch.tensor(target, dtype=torch.int64)
            valid_t = torch.tensor(valid, dtype=torch.bool)
            before = c216.model_sha(readers[reader_seed])
            with torch.no_grad():
                pred = readers[reader_seed](x_t).argmax(dim=-1)
            frozen_reader_calls += 1
            require(
                c216.model_sha(readers[reader_seed]) == before ==
                READER_FINAL_SHA256[READER_SEEDS.index(reader_seed)],
                "Frozen Reader mutated",
            )
            good = valid_t & (pred == y_t)
            local_total = len(rows)
            local_correct = int(good.sum().item())
            total += local_total
            correct += local_correct

            local_hot_total = local_hot_correct = 0
            local_committed_total = local_committed_correct = 0
            local_mismatches = 0
            if placement_sensitive:
                keyed = {}
                for i, placement in enumerate(placements):
                    if placement == "HOT":
                        hot_total += 1
                        local_hot_total += 1
                        hot_correct += int(good[i].item())
                        local_hot_correct += int(good[i].item())
                    elif placement == "COMMITTED":
                        committed_total += 1
                        local_committed_total += 1
                        committed_correct += int(good[i].item())
                        local_committed_correct += int(good[i].item())
                    keyed.setdefault(keys[i], {})[placement] = (
                        int(pred[i].item()), bool(valid_t[i].item())
                    )
                for pair in keyed.values():
                    if set(pair) != {"HOT","COMMITTED"}:
                        local_mismatches += 1
                    elif not pair["HOT"][1] or not pair["COMMITTED"][1]:
                        local_mismatches += 1
                    elif pair["HOT"][0] != pair["COMMITTED"][0]:
                        local_mismatches += 1
                placement_mismatches += local_mismatches

            combo_records.append(dict(
                selector_seed=selector_seed,
                reader_seed=reader_seed,
                accuracy=local_correct/local_total,
                hot_accuracy=(local_hot_correct/local_hot_total if local_hot_total else None),
                committed_accuracy=(
                    local_committed_correct/local_committed_total if local_committed_total else None
                ),
                placement_mismatches=local_mismatches,
            ))

    return dict(
        accuracy=correct/total,
        hot_accuracy=(hot_correct/hot_total if hot_total else None),
        committed_accuracy=(committed_correct/committed_total if committed_total else None),
        placement_mismatches=placement_mismatches,
        frozen_combo_records=combo_records,
        frozen_reader_forward_calls=frozen_reader_calls,
    )


def writer_seed_pass(record):
    return (
        record.get("train_relation_accuracy") == 1.0
        and record.get("eval_relation_accuracy") == 1.0
        and record.get("factor_blind_eval_accuracy") == 0.5
        and abs(record.get("semantic_blind_eval_accuracy", -1.0) - 1.0/3.0) <= 1e-12
        and record.get("checkpoint_roundtrip") is True
        and record.get("write_rejections") == 0
        and record["assert_metrics"].get("accuracy") == 1.0
        and record["assert_metrics"].get("hot_accuracy") == 1.0
        and record["assert_metrics"].get("committed_accuracy") == 1.0
        and record["assert_metrics"].get("placement_mismatches") == 0
        and record["replace_metrics"].get("accuracy") == 1.0
    )


def gate(summary):
    records = summary.get("writer_seed_records")
    return (
        isinstance(records, list)
        and len(records) == 3
        and [r.get("seed") for r in records] == list(WRITER_SEEDS)
        and all(writer_seed_pass(r) for r in records)
        and summary.get("all_writer_checkpoint_roundtrips") is True
        and summary.get("all_selector_checkpoint_roundtrips") is True
        and summary.get("all_reader_checkpoint_roundtrips") is True
        and summary.get("writer_data_sha256") == WRITER_DATA_SHA
        and summary["wrong_semantic_control"].get("accuracy") == 0.0
        and summary["wrong_factor_control"].get("accuracy") == 0.0
        and summary.get("learned_writer_calls") == 1212
        and summary.get("frozen_selector_forward_calls") == 3
        and summary.get("frozen_reader_forward_calls") == 72
        and summary.get("reader_training_steps") == 0
        and summary.get("selector_training_steps") == 0
        and summary.get("coverage_classifier_calls") == 0
        and summary.get("learned_writer_operation_attempts") == 54
        and summary.get("oracle_writer_operations") == 60
        and summary.get("control_writer_operations") == 12
        and summary.get("chunk_commits") == 96
    )


def precheck(c217_summary, root):
    root = Path(root)
    require(audit.sha(c217_summary) == PARENT_C217_SHA, "C217 summary changed")
    p217 = audit.read_json(c217_summary)
    c217.validate_result(p217)
    require(
        p217.get("commit_sha") == PARENT_C217_EXECUTION
        and p217.get("status") == "PASS"
        and c217.gate(p217["validation_summary"])
        and len(p217.get("source_blobs", {})) == 137
        and len(p217.get("input_sha256", {})) == 143,
        "Wrong accepted C217 parent",
    )

    protected = dict(p217["input_sha256"])
    for name, wanted in protected.items():
        require(Path(name).is_file() and audit.sha(name) == wanted,
                "Changed inherited protected input:" + name)

    pins = dict(p217["source_blobs"])
    for name, expected_blob in pins.items():
        actual = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
        require(actual == expected_blob, "C217 source pin changed:" + name)

    protected[str(Path(c217_summary).resolve())] = PARENT_C217_SHA
    selector_seen = validation_seen = False
    for artifact in p217["artifacts"]:
        path = audit.safe_child(Path(c217_summary).resolve().parent, artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C217 artifact:" + artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]
        if artifact["file"] == "validation-summary.json":
            require(artifact["sha256"] == PARENT_C217_VALIDATION_SHA,
                    "C217 validation artifact changed")
            validation_seen = True
        if artifact["file"] == "selector-checkpoints.pt":
            require(artifact["sha256"] == PARENT_SELECTOR_CHECKPOINT_SHA,
                    "C217 selector checkpoint artifact changed")
            selector_seen = True
    require(validation_seen and selector_seen, "C217 deciding artifact missing")

    find_protected_input(p217, "reader-checkpoints.pt", INHERITED_READER_CHECKPOINT_SHA)

    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()

    for dependency in DIRECT_REPO_DEPENDENCIES:
        require(dependency in allpins, "Unpinned direct dependency:" + dependency)

    protected.update(audit.protect_tree_files(root, allpins))
    pins.update({name: allpins[name] for name in OWN})

    require(len(pins) == 144, "C218 source pin count drift")
    require(len(protected) == 156, "C218 protected input count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C218 manifest drift")
    return p217, pins, protected


def regression_modules(root):
    names = c217.regression_modules(root)
    require(len(names) == len(set(names)) == 102, "Historical regression module drift")
    return names + ["tests_lm.test_v05_c218_learned_writer"]


def regression_suite(root):
    names = regression_modules(root)
    loaded = unittest.defaultTestLoader.loadTestsFromNames(names)
    tests = list(c205._iter_tests(loaded))
    ids = [test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded) == 1, "Historical dynamic test identity drift:" + excluded)
    kept = [test for test in tests if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS]
    require(
        len(tests) == 2260
        and len(kept) == 2259
        and not any(test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS for test in kept),
        "C218 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C218",
    )
    require(
        len(payload["source_blobs"]) == 144
        and len(payload["input_sha256"]) == 156
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C218 coverage drift",
    )
    require(
        payload["trained_writer_models"] == 3
        and payload["writer_parameters_per_model"] == 150
        and payload["training_steps_total"] == 1200
        and payload["training_examples_drawn"] == 21600
        and payload["learned_writer_calls"] == 1212
        and payload["frozen_selector_forward_calls"] == 3
        and payload["frozen_reader_forward_calls"] == 72
        and payload["model_forward_calls"] == 1287
        and payload["learned_writer_operation_attempts"] == 54
        and payload["oracle_writer_operations"] == 60
        and payload["control_writer_operations"] == 12
        and payload["chunk_commits"] == 96
        and payload["reader_training_steps"] == 0
        and payload["selector_training_steps"] == 0
        and payload["network_calls"] == 0,
        "C218 workload drift",
    )
    require(
        payload["production_runtime_modified"] is True
        and payload["gate_f_candidate"] is False
        and payload["learned_writer"] is True
        and payload["learned_port_selector"] is False
        and payload["learned_reader"] is False
        and payload["coverage_classifier"] is False,
        "C218 scope drift",
    )
    require(
        payload["status"] == ("PASS" if gate(payload["validation_summary"]) else "FAIL"),
        "C218 gate drift",
    )


def run(*, c217_summary, output_dir, expected_head):
    root = Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root, "rev-parse", "HEAD").decode().strip() == expected_head,
                "HEAD mismatch")
        require(audit.git(root, "branch", "--show-current").decode().strip()
                == "feat/sft-target-loss", "Branch mismatch")
        require(not audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    p217, pins, protected = precheck(c217_summary, root)
    data = writer_dataset()

    selector_checkpoint = Path(c217_summary).resolve().parent / "selector-checkpoints.pt"
    selectors = restore_selectors(selector_checkpoint, p217)
    readers = restore_readers(p217)
    routes = frozen_routes(selectors)
    selector_roundtrip = all(
        c217.model_sha(selectors[seed]) == SELECTOR_FINAL_SHA256[i]
        for i, seed in enumerate(SELECTOR_SEEDS)
    )
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

    save_json("writer-plan.json", dict(manifest(), source_blobs=pins))
    np.savez_compressed(
        out / "writer-dataset.npz",
        features=data["features"],
        labels=data["labels"],
        split_codes=data["split_codes"],
    )
    record("writer-dataset.npz")

    fit_records = []
    state_dicts = []
    for seed in WRITER_SEEDS:
        model, fit_record = fit(seed, train_x, train_y)
        fit_records.append(fit_record)
        state_dicts.append(
            {name: tensor.detach().cpu().clone() for name, tensor in model.state_dict().items()}
        )

    bundle = dict(
        schema="fold-v5f-writer-checkpoints-v1",
        seeds=list(WRITER_SEEDS),
        config=dict(input_width=5, hidden_width=12, relation_classes=6),
        state_dicts=state_dicts,
    )
    torch.save(bundle, out / "writer-checkpoints.pt")
    record("writer-checkpoints.pt")

    restored_bundle = torch.load(out / "writer-checkpoints.pt", map_location="cpu",
                                 weights_only=True)
    require(
        restored_bundle["schema"] == "fold-v5f-writer-checkpoints-v1"
        and tuple(restored_bundle["seeds"]) == WRITER_SEEDS
        and restored_bundle["config"] == dict(input_width=5, hidden_width=12, relation_classes=6),
        "Writer checkpoint bundle identity drift",
    )

    seed_records = []
    writer_roundtrips = []
    aggregate_counts = dict(
        learned_writer_operation_attempts=0,
        oracle_writer_operations=0,
        control_writer_operations=0,
        chunk_commits=0,
    )
    frozen_reader_calls = 0

    for seed, state_dict, fit_record in zip(
        WRITER_SEEDS, restored_bundle["state_dicts"], fit_records, strict=True
    ):
        restored = new_writer()
        restored.load_state_dict(state_dict, strict=True)
        restored.eval()
        final_sha = model_sha(restored)
        roundtrip = final_sha == fit_record["final_sha256"]
        writer_roundtrips.append(roundtrip)

        score = score_writer(restored, data)
        assert_rows, assert_counts = learned_assert_rows(score["prediction_by_target"], seed)
        replace_rows, replace_counts = learned_replace_rows(score["prediction_by_target"], seed)
        assert_metrics = evaluate_rows(assert_rows, routes, readers, placement_sensitive=True)
        replace_metrics = evaluate_rows(replace_rows, routes, readers)
        frozen_reader_calls += (
            assert_metrics["frozen_reader_forward_calls"]
            + replace_metrics["frozen_reader_forward_calls"]
        )
        for key in aggregate_counts:
            aggregate_counts[key] += assert_counts[key] + replace_counts[key]

        seed_records.append(dict(
            seed=seed,
            checkpoint_roundtrip=roundtrip,
            initial_sha256=fit_record["initial_sha256"],
            final_sha256=final_sha,
            initial_loss=fit_record["initial_loss"],
            final_loss=fit_record["final_loss"],
            train_relation_accuracy=score["train_relation_accuracy"],
            eval_relation_accuracy=score["eval_relation_accuracy"],
            factor_blind_eval_accuracy=score["factor_blind_eval_accuracy"],
            semantic_blind_eval_accuracy=score["semantic_blind_eval_accuracy"],
            train_predictions=score["train_predictions"],
            eval_predictions=score["eval_predictions"],
            factor_blind_predictions=score["factor_blind_predictions"],
            semantic_blind_predictions=score["semantic_blind_predictions"],
            writer_scoring_forward_calls=score["writer_scoring_forward_calls"],
            assert_metrics=assert_metrics,
            replace_metrics=replace_metrics,
            write_rejections=assert_counts["write_rejections"] + replace_counts["write_rejections"],
        ))

    wrong_semantic_rows, semantic_counts = control_replace_rows("WRONG_SEMANTIC")
    wrong_factor_rows, factor_counts = control_replace_rows("WRONG_FACTOR")
    wrong_semantic = evaluate_rows(wrong_semantic_rows, routes, readers)
    wrong_factor = evaluate_rows(wrong_factor_rows, routes, readers)
    frozen_reader_calls += (
        wrong_semantic["frozen_reader_forward_calls"]
        + wrong_factor["frozen_reader_forward_calls"]
    )
    for key in aggregate_counts:
        aggregate_counts[key] += semantic_counts[key] + factor_counts[key]

    save_json("evaluation.json", dict(
        writer_seed_records=seed_records,
        fit_records=fit_records,
        wrong_semantic_control=wrong_semantic,
        wrong_factor_control=wrong_factor,
    ))

    learned_writer_calls = sum(r["training_forward_calls"] for r in fit_records) + sum(
        r["writer_scoring_forward_calls"] for r in seed_records
    )

    summary = dict(
        writer_seed_records=seed_records,
        all_writer_checkpoint_roundtrips=all(writer_roundtrips),
        all_selector_checkpoint_roundtrips=selector_roundtrip,
        all_reader_checkpoint_roundtrips=reader_roundtrip,
        writer_data_sha256=data["content_sha256"],
        wrong_semantic_control=wrong_semantic,
        wrong_factor_control=wrong_factor,
        learned_writer_calls=learned_writer_calls,
        frozen_selector_forward_calls=len(SELECTOR_SEEDS),
        frozen_reader_forward_calls=frozen_reader_calls,
        reader_training_steps=0,
        selector_training_steps=0,
        coverage_classifier_calls=0,
        **aggregate_counts,
    )
    save_json("validation-summary.json", summary)

    guard()
    precheck(c217_summary, root)
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
        C217_summary_sha256=PARENT_C217_SHA,
        source_blobs=pins,
        input_sha256=protected,
        artifacts=artifacts,
        validation_summary=summary,
        fit_records=fit_records,
        trained_writer_models=3,
        writer_parameters_per_model=150,
        training_steps_total=sum(r["steps"] for r in fit_records),
        training_examples_drawn=sum(r["examples_drawn"] for r in fit_records),
        learned_writer_calls=learned_writer_calls,
        frozen_selector_forward_calls=len(SELECTOR_SEEDS),
        frozen_reader_forward_calls=frozen_reader_calls,
        model_forward_calls=learned_writer_calls + len(SELECTOR_SEEDS) + frozen_reader_calls,
        learned_writer_operation_attempts=aggregate_counts["learned_writer_operation_attempts"],
        oracle_writer_operations=aggregate_counts["oracle_writer_operations"],
        control_writer_operations=aggregate_counts["control_writer_operations"],
        chunk_commits=aggregate_counts["chunk_commits"],
        reader_training_steps=0,
        selector_training_steps=0,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        learned_writer=True,
        learned_port_selector=False,
        learned_reader=False,
        coverage_classifier=False,
        limitations=[
            "tiny synthetic structured-observation Writer pilot",
            "ASSERT/REPLACE operation kind is oracle and not predicted by Writer",
            "accepted C217 selectors and C216 Readers are frozen; no co-adaptation",
            "no RETRACT/ASSUME operation learning, natural language, memory-cost advantage or Gate F claim",
        ],
    )
    validate_result(result)
    (out / "summary.json").write_bytes(blob(result))
    print(
        "[C218] learned Writer "
        + " ".join(
            f"seed={r['seed']} eval={r['eval_relation_accuracy']:.3f} "
            f"assert={r['assert_metrics']['accuracy']:.3f} "
            f"replace={r['replace_metrics']['accuracy']:.3f}"
            for r in seed_records
        ),
        flush=True,
    )
    print("=== C218 RESULT ===", flush=True)
    print(blob(result).decode(), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c217-summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
