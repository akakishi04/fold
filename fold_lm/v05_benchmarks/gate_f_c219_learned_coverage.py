"""C219: V5-F learned Coverage classifier pilot.

One changed scientific component: a learned classifier predicts target-specific memory coverage as
SUPPORTED / HOT_REQUIRED / MISSING / OUT_OF_SCOPE. Numeric safety remains deterministic and
NUMERIC_UNSAFE is intentionally outside the coverage taxonomy.

Writer learning is not exercised. Accepted C217 Port Selectors and C216 Readers are frozen only to
verify that readable coverage states still yield the expected semantic answer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time
import unittest

import numpy as np
import torch
from torch.nn import functional as F

from fold_lm.v05 import memory_bridge as memory
from fold_lm.v05 import memory_coverage as coverage
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_f_c216_learned_reader as c216
from fold_lm.v05_benchmarks import gate_f_c217_learned_port_selector as c217
from fold_lm.v05_benchmarks import gate_f_c218_learned_writer as c218

EXPERIMENT_ID = "C219-v5f-learned-coverage-classifier-pilot"
STAGE = "V5-F-LEARNED-COVERAGE-CLASSIFIER-PILOT"
BASE = "51dcf53120d7f86656c13b70d1da00cb0c7a351b"
PARENT_C218_EXECUTION = "ce5ae96f5fe3a08213ee41bffa17ba97c10bb368"
PARENT_C218_SHA = "50ec397534901bb865731b615232c555cfcf0222571f42b09098eae77f49f021"
PARENT_C218_VALIDATION_SHA = "a0b235393fe3cd267534ecaa6de7190b534eb59a5fb8b95b1de083b6b4563359"
INHERITED_SELECTOR_CHECKPOINT_SHA = "ab8892e6562a4801a30fea853fdbc712d69d9c5077e32c0b8fab6e555fead215"
INHERITED_READER_CHECKPOINT_SHA = "bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af"
COVERAGE_DATA_SHA = "3e9c74b7675439c3118f6a87bc7594455360512e906d69c1c739cae9edc34d65"
MANIFEST_SHA = "466ee5cd488a08ef9b8dacc6bf9f544ba4ca83ff2ab80dc2af421a6be9db43aa"

TRAIN_NUISANCE = ((-1, -1), (-1, 1), (1, -1))
EVAL_NUISANCE = ((1, 1),)
COVERAGE_NAMES = ("SUPPORTED", "HOT_REQUIRED", "MISSING", "OUT_OF_SCOPE")
COVERAGE_SEEDS = (219001, 219002, 219003)
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
STEPS = 400
BATCH_SIZE = 24
LR = 0.02

OWN = (
    "fold_lm/v05/memory_coverage.py",
    "fold_lm/v05_benchmarks/gate_f_c219_learned_coverage.py",
    "tests_lm/test_v05_c219_learned_coverage.py",
    "tools/run_c219.ps1",
    "tools/invoke_c219.ps1",
    "docs/experiment-ledger-addendum-c219-preregistration.md",
    "docs/v5f-learned-coverage-pilot-v0.1.md",
)
OUTPUTS = {
    "coverage-plan.json",
    "coverage-dataset.npz",
    "coverage-checkpoints.pt",
    "evaluation.json",
    "validation-summary.json",
}
DIRECT_REPO_DEPENDENCIES = (
    "fold_lm/v05/memory_bank.py",
    "fold_lm/v05/memory_bridge.py",
    "fold_lm/v05/memory_capsule_bridge.py",
    "fold_lm/v05/memory_reader.py",
    "fold_lm/v05/memory_port_selector.py",
    "fold_lm/v05/memory_coverage.py",
    "fold_lm/v05_benchmarks/gate_e_c175_frozen_prediction_audit.py",
    "fold_lm/v05_benchmarks/gate_e_c205_phase0_batch_composition_attribution.py",
    "fold_lm/v05_benchmarks/gate_f_c216_learned_reader.py",
    "fold_lm/v05_benchmarks/gate_f_c217_learned_port_selector.py",
    "fold_lm/v05_benchmarks/gate_f_c218_learned_writer.py",
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
        parent_c218_execution=PARENT_C218_EXECUTION,
        parent_c218_sha256=PARENT_C218_SHA,
        parent_c218_validation_sha256=PARENT_C218_VALIDATION_SHA,
        inherited_selector_checkpoint_sha256=INHERITED_SELECTOR_CHECKPOINT_SHA,
        inherited_reader_checkpoint_sha256=INHERITED_READER_CHECKPOINT_SHA,
        coverage_classes=list(COVERAGE_NAMES),
        numeric_unsafe_excluded=True,
        feature_schema=[
            "query_alpha", "query_beta", "target_in_h2", "target_in_h1_hot",
            "scope_live", "nuisance_1", "nuisance_2",
        ],
        coverage_data_sha256=COVERAGE_DATA_SHA,
        train_nuisance=[list(x) for x in TRAIN_NUISANCE],
        eval_nuisance=[list(x) for x in EVAL_NUISANCE],
        rows=32,
        train_rows=24,
        eval_rows=8,
        train_class_counts=[6, 6, 6, 6],
        eval_class_counts=[2, 2, 2, 2],
        input_width=7,
        hidden_width=12,
        class_count=4,
        parameters=148,
        seeds=list(COVERAGE_SEEDS),
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
        gate_train_accuracy=1.0,
        gate_eval_accuracy=1.0,
        gate_state_blind_accuracy=0.25,
        gate_tier_blind_readable_accuracy=0.0,
        gate_scope_blind_missing_oos_accuracy=0.5,
        readable_eval_rows=4,
        nonreadable_eval_rows=4,
        gate_readable_answer_accuracy=1.0,
        gate_nonreadable_suppression_accuracy=1.0,
        gate_missing_oos_confusions=0,
        frozen_selector_checkpoints=3,
        frozen_reader_checkpoints=3,
        training_steps_total=1200,
        training_examples_drawn=28800,
        learned_coverage_forward_calls_expected=1215,
        frozen_selector_forward_calls_expected=3,
        frozen_reader_forward_calls_expected=9,
        model_forward_calls_expected=1227,
        writer_training_steps=0,
        selector_training_steps=0,
        reader_training_steps=0,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        scope=(
            "learned Coverage classifier only over bounded target-specific memory summary; "
            "frozen Selector/Reader; oracle state construction; no Writer learning or "
            "numeric-safety classification"
        ),
    )


def _query_spec(query_role):
    if query_role == 0:
        return "alpha", "scope-alpha", 0
    if query_role == 1:
        return "beta", "scope-beta", 2
    raise ValueError("query_role out of range")


def _assert_target(bank, state, query_role):
    factor, scope, semantic_class = _query_spec(query_role)
    op = memory.MemoryOp(
        kind=memory.MemoryOpKind.ASSERT,
        expected_memory_revision=state.memory_revision,
        scope_id=scope,
        factor_id=factor,
        relation_key=f"{factor}-class-{semantic_class}",
        source_id=f"coverage:{factor}",
        evidence_time=1,
    )
    state, read = bank.apply(state, op)
    require(read is None, "coverage fixture ASSERT returned read")
    return state


def build_state(query_role, class_id):
    if type(class_id) is not int or not 0 <= class_id < 4:
        raise ValueError("coverage class out of range")
    bank = c216.build_bank()
    state = bank.initial_state()
    factor, scope, _ = _query_spec(query_role)

    if class_id == int(coverage.CoverageClass.SUPPORTED):
        state = _assert_target(bank, state, query_role)
        state, status = bank.commit(state)
        require(status.value == "COMMITTED", "coverage SUPPORTED commit failed")
    elif class_id == int(coverage.CoverageClass.HOT_REQUIRED):
        state = _assert_target(bank, state, query_role)
    elif class_id == int(coverage.CoverageClass.MISSING):
        pass
    elif class_id == int(coverage.CoverageClass.OUT_OF_SCOPE):
        op = memory.MemoryOp(
            kind=memory.MemoryOpKind.END_SCOPE,
            expected_memory_revision=state.memory_revision,
            scope_id=scope,
        )
        state, read = bank.apply(state, op)
        require(read is None, "coverage END_SCOPE returned read")
    else:
        raise AssertionError("unreachable")
    return bank, state, factor, scope


def coverage_dataset():
    metadata = []
    features = []
    labels = []
    split_codes = []
    for query_role, (factor, _, _) in enumerate((_query_spec(0), _query_spec(1))):
        for class_id, class_name in enumerate(COVERAGE_NAMES):
            for nuisance in TRAIN_NUISANCE + EVAL_NUISANCE:
                split = 0 if nuisance in TRAIN_NUISANCE else 1
                _, state, factor_id, scope = build_state(query_role, class_id)
                feature, teacher = coverage.target_summary(
                    state,
                    query_role=query_role,
                    scope_id=scope,
                    factor_id=factor_id,
                    nuisance=(float(nuisance[0]), float(nuisance[1])),
                )
                require(int(teacher) == class_id, "Coverage teacher/status drift")
                metadata.append(dict(
                    query=factor,
                    coverage=class_name,
                    nuisance=list(nuisance),
                    split="TRAIN" if split == 0 else "EVAL",
                ))
                features.append(feature.numpy())
                labels.append(class_id)
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
    require(sha == COVERAGE_DATA_SHA, "C219 coverage dataset content drift")

    train = arrays["split_codes"] == 0
    ev = arrays["split_codes"] == 1
    require(
        (
            len(metadata),
            int(train.sum()),
            int(ev.sum()),
            np.bincount(arrays["labels"][train], minlength=4).tolist(),
            np.bincount(arrays["labels"][ev], minlength=4).tolist(),
        )
        == (32, 24, 8, [6,6,6,6], [2,2,2,2]),
        "C219 coverage dataset profile drift",
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


def new_classifier():
    model = coverage.MemoryCoverageClassifier(coverage.MemoryCoverageConfig())
    require(coverage.parameter_count(model) == 148, "Coverage parameter count drift")
    return model


def fit(seed, train_x, train_y):
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)
    model = new_classifier()
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
        require(torch.isfinite(loss).item(), "nonfinite Coverage training loss")
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


def score_classifier(model, data):
    x = torch.from_numpy(data["features"].copy()).to(torch.float32)
    y = torch.from_numpy(data["labels"].copy()).to(torch.int64)
    split = torch.from_numpy(data["split_codes"].copy()).to(torch.int64)
    train = split == 0
    ev = split == 1
    with torch.no_grad():
        train_pred = model(x[train]).argmax(dim=-1)
        eval_pred = model(x[ev]).argmax(dim=-1)

        state_blind_x = x[ev].clone()
        state_blind_x[:, 2:5] = 0.0
        state_blind_pred = model(state_blind_x).argmax(dim=-1)

        readable = ev & ((y == int(coverage.CoverageClass.SUPPORTED))
                         | (y == int(coverage.CoverageClass.HOT_REQUIRED)))
        tier_blind_x = x[readable].clone()
        tier_blind_x[:, 2:4] = 0.0
        tier_blind_pred = model(tier_blind_x).argmax(dim=-1)

        nonreadable = ev & ((y == int(coverage.CoverageClass.MISSING))
                            | (y == int(coverage.CoverageClass.OUT_OF_SCOPE)))
        scope_blind_x = x[nonreadable].clone()
        scope_blind_x[:, 4] = 0.0
        scope_blind_pred = model(scope_blind_x).argmax(dim=-1)

    eval_targets = y[ev]
    readable_targets = y[readable]
    nonreadable_targets = y[nonreadable]
    missing_oos_confusions = int((
        ((eval_targets == int(coverage.CoverageClass.MISSING))
         & (eval_pred == int(coverage.CoverageClass.OUT_OF_SCOPE)))
        | ((eval_targets == int(coverage.CoverageClass.OUT_OF_SCOPE))
           & (eval_pred == int(coverage.CoverageClass.MISSING)))
    ).sum().item())

    return dict(
        train_accuracy=accuracy(train_pred, y[train]),
        eval_accuracy=accuracy(eval_pred, eval_targets),
        state_blind_eval_accuracy=accuracy(state_blind_pred, eval_targets),
        tier_blind_readable_accuracy=accuracy(tier_blind_pred, readable_targets),
        scope_blind_missing_oos_accuracy=accuracy(scope_blind_pred, nonreadable_targets),
        readable_gate_accuracy=accuracy(eval_pred[
            (eval_targets == 0) | (eval_targets == 1)
        ], readable_targets),
        nonreadable_suppression_accuracy=accuracy(eval_pred[
            (eval_targets == 2) | (eval_targets == 3)
        ], nonreadable_targets),
        missing_oos_confusions=missing_oos_confusions,
        train_predictions=train_pred.tolist(),
        eval_predictions=eval_pred.tolist(),
        scoring_forward_calls=5,
    )


def find_protected_input(parent_summary, basename, expected_sha):
    matches = [
        Path(name)
        for name, sha in parent_summary["input_sha256"].items()
        if name.replace("\\", "/").endswith("/" + basename) and sha == expected_sha
    ]
    require(len(matches) == 1, "Inherited artifact resolution drift:" + basename)
    require(matches[0].is_file() and audit.sha(matches[0]) == expected_sha,
            "Inherited artifact changed:" + basename)
    return matches[0]


def restore_selectors(parent_summary):
    checkpoint = find_protected_input(
        parent_summary, "selector-checkpoints.pt", INHERITED_SELECTOR_CHECKPOINT_SHA
    )
    payload = torch.load(checkpoint, map_location="cpu", weights_only=True)
    require(
        payload["schema"] == "fold-v5f-port-selector-checkpoints-v1"
        and tuple(payload["seeds"]) == SELECTOR_SEEDS
        and payload["config"] == dict(input_width=4, hidden_width=8, port_count=2),
        "Selector checkpoint bundle identity drift",
    )
    models = {}
    for seed, state_dict, expected_sha in zip(
        SELECTOR_SEEDS, payload["state_dicts"], SELECTOR_FINAL_SHA256, strict=True
    ):
        model = c217.new_selector()
        model.load_state_dict(state_dict, strict=True)
        model.eval()
        require(c217.model_sha(model) == expected_sha, "Frozen selector changed")
        models[seed] = model
    return models


def restore_readers(parent_summary):
    checkpoint = find_protected_input(
        parent_summary, "reader-checkpoints.pt", INHERITED_READER_CHECKPOINT_SHA
    )
    payload = torch.load(checkpoint, map_location="cpu", weights_only=True)
    require(
        payload["schema"] == "fold-v5f-reader-checkpoints-v1"
        and tuple(payload["seeds"]) == READER_SEEDS
        and payload["config"] == dict(input_width=1, hidden_width=8, answer_classes=3),
        "Reader checkpoint bundle identity drift",
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
    query_x = torch.tensor([[1,0,1,1],[0,1,1,1]], dtype=torch.float32)
    routes = {}
    for seed in SELECTOR_SEEDS:
        before = c217.model_sha(selectors[seed])
        with torch.no_grad():
            pred = selectors[seed](query_x).argmax(dim=-1)
        require(
            c217.model_sha(selectors[seed]) == before
            == SELECTOR_FINAL_SHA256[SELECTOR_SEEDS.index(seed)],
            "Frozen selector mutated",
        )
        routes[seed] = {"alpha": int(pred[0]), "beta": int(pred[1])}
    require(all(x == {"alpha":0,"beta":1} for x in routes.values()),
            "Frozen selector route drift")
    return routes


def readable_reference(selectors, readers):
    routes = frozen_routes(selectors)
    rows = []
    for query_role, query in enumerate(("alpha","beta")):
        target_class = 0 if query_role == 0 else 2
        for class_id in (
            int(coverage.CoverageClass.SUPPORTED),
            int(coverage.CoverageClass.HOT_REQUIRED),
        ):
            bank, state, _, _ = build_state(query_role, class_id)
            read = bank.read(state)
            expected_status = "SUPPORTED" if class_id == 0 else "HOT_REQUIRED"
            require(read.status.value == expected_status, "Readable bank status drift")
            rows.append(dict(
                query=query,
                coverage_class=class_id,
                target_class=target_class,
                port_values=[float(v) for v in read.value.tolist()],
            ))

    total = correct = 0
    records = []
    reader_calls = 0
    for selector_seed in SELECTOR_SEEDS:
        for reader_seed in READER_SEEDS:
            x = torch.tensor(
                [(row["port_values"][routes[selector_seed][row["query"]]],) for row in rows],
                dtype=torch.float32,
            )
            y = torch.tensor([row["target_class"] for row in rows], dtype=torch.int64)
            before = c216.model_sha(readers[reader_seed])
            with torch.no_grad():
                pred = readers[reader_seed](x).argmax(dim=-1)
            reader_calls += 1
            require(
                c216.model_sha(readers[reader_seed]) == before
                == READER_FINAL_SHA256[READER_SEEDS.index(reader_seed)],
                "Frozen Reader mutated",
            )
            local = accuracy(pred, y)
            total += len(rows)
            correct += int((pred == y).sum().item())
            records.append(dict(
                selector_seed=selector_seed,
                reader_seed=reader_seed,
                accuracy=local,
            ))
    return dict(
        accuracy=correct/total,
        rows=len(rows),
        frozen_records=records,
        frozen_selector_forward_calls=len(SELECTOR_SEEDS),
        frozen_reader_forward_calls=reader_calls,
    )


def seed_pass(record):
    return (
        record.get("train_accuracy") == 1.0
        and record.get("eval_accuracy") == 1.0
        and record.get("state_blind_eval_accuracy") == 0.25
        and record.get("tier_blind_readable_accuracy") == 0.0
        and record.get("scope_blind_missing_oos_accuracy") == 0.5
        and record.get("readable_gate_accuracy") == 1.0
        and record.get("nonreadable_suppression_accuracy") == 1.0
        and record.get("missing_oos_confusions") == 0
        and record.get("checkpoint_roundtrip") is True
    )


def gate(summary):
    records = summary.get("coverage_seed_records")
    reference = summary.get("readable_reference", {})
    return (
        isinstance(records, list)
        and len(records) == 3
        and [r.get("seed") for r in records] == list(COVERAGE_SEEDS)
        and all(seed_pass(r) for r in records)
        and summary.get("all_coverage_checkpoint_roundtrips") is True
        and summary.get("all_selector_checkpoint_roundtrips") is True
        and summary.get("all_reader_checkpoint_roundtrips") is True
        and summary.get("coverage_data_sha256") == COVERAGE_DATA_SHA
        and reference.get("accuracy") == 1.0
        and reference.get("rows") == 4
        and summary.get("learned_coverage_calls") == 1215
        and summary.get("frozen_selector_forward_calls") == 3
        and summary.get("frozen_reader_forward_calls") == 9
        and summary.get("writer_training_steps") == 0
        and summary.get("selector_training_steps") == 0
        and summary.get("reader_training_steps") == 0
        and summary.get("numeric_unsafe_classified") == 0
    )


def precheck(c218_summary, root):
    root = Path(root)
    require(audit.sha(c218_summary) == PARENT_C218_SHA, "C218 summary changed")
    p218 = audit.read_json(c218_summary)
    c218.validate_result(p218)
    require(
        p218.get("commit_sha") == PARENT_C218_EXECUTION
        and p218.get("status") == "PASS"
        and c218.gate(p218["validation_summary"])
        and len(p218.get("source_blobs", {})) == 144
        and len(p218.get("input_sha256", {})) == 156,
        "Wrong accepted C218 parent",
    )

    protected = dict(p218["input_sha256"])
    for name, wanted in protected.items():
        require(Path(name).is_file() and audit.sha(name) == wanted,
                "Changed inherited protected input:" + name)

    pins = dict(p218["source_blobs"])
    for name, expected_blob in pins.items():
        actual = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
        require(actual == expected_blob, "C218 source pin changed:" + name)

    protected[str(Path(c218_summary).resolve())] = PARENT_C218_SHA
    validation_seen = False
    for artifact in p218["artifacts"]:
        path = audit.safe_child(Path(c218_summary).resolve().parent, artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C218 artifact:" + artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]
        if artifact["file"] == "validation-summary.json":
            require(artifact["sha256"] == PARENT_C218_VALIDATION_SHA,
                    "C218 validation artifact changed")
            validation_seen = True
    require(validation_seen, "C218 validation artifact missing")

    find_protected_input(p218, "selector-checkpoints.pt", INHERITED_SELECTOR_CHECKPOINT_SHA)
    find_protected_input(p218, "reader-checkpoints.pt", INHERITED_READER_CHECKPOINT_SHA)

    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()

    for dependency in DIRECT_REPO_DEPENDENCIES:
        require(dependency in allpins, "Unpinned direct dependency:" + dependency)

    protected.update(audit.protect_tree_files(root, allpins))
    pins.update({name: allpins[name] for name in OWN})

    require(len(pins) == 151, "C219 source pin count drift")
    require(len(protected) == 169, "C219 protected input count drift")
    require(digest(manifest()) == MANIFEST_SHA, "C219 manifest drift")
    return p218, pins, protected


def regression_modules(root):
    names = c218.regression_modules(root)
    require(len(names) == len(set(names)) == 103, "Historical regression module drift")
    return names + ["tests_lm.test_v05_c219_learned_coverage"]


def regression_suite(root):
    names = regression_modules(root)
    loaded = unittest.defaultTestLoader.loadTestsFromNames(names)
    tests = list(c205._iter_tests(loaded))
    ids = [test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded) == 1, "Historical dynamic test identity drift:" + excluded)
    kept = [test for test in tests if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS]
    require(
        len(tests) == 2298
        and len(kept) == 2297
        and not any(test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS for test in kept),
        "C219 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C219",
    )
    require(
        len(payload["source_blobs"]) == 151
        and len(payload["input_sha256"]) == 169
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C219 coverage drift",
    )
    require(
        payload["trained_coverage_models"] == 3
        and payload["coverage_parameters_per_model"] == 148
        and payload["training_steps_total"] == 1200
        and payload["training_examples_drawn"] == 28800
        and payload["learned_coverage_calls"] == 1215
        and payload["frozen_selector_forward_calls"] == 3
        and payload["frozen_reader_forward_calls"] == 9
        and payload["model_forward_calls"] == 1227
        and payload["writer_training_steps"] == 0
        and payload["selector_training_steps"] == 0
        and payload["reader_training_steps"] == 0
        and payload["network_calls"] == 0,
        "C219 workload drift",
    )
    require(
        payload["production_runtime_modified"] is True
        and payload["gate_f_candidate"] is False
        and payload["learned_coverage_classifier"] is True
        and payload["learned_writer"] is False
        and payload["learned_port_selector"] is False
        and payload["learned_reader"] is False
        and payload["numeric_unsafe_classified"] == 0,
        "C219 scope drift",
    )
    require(
        payload["status"] == ("PASS" if gate(payload["validation_summary"]) else "FAIL"),
        "C219 gate drift",
    )


def run(*, c218_summary, output_dir, expected_head):
    root = Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root, "rev-parse", "HEAD").decode().strip() == expected_head,
                "HEAD mismatch")
        require(audit.git(root, "branch", "--show-current").decode().strip()
                == "feat/sft-target-loss", "Branch mismatch")
        require(not audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    p218, pins, protected = precheck(c218_summary, root)
    data = coverage_dataset()
    selectors = restore_selectors(p218)
    readers = restore_readers(p218)
    selector_roundtrip = all(
        c217.model_sha(selectors[seed]) == SELECTOR_FINAL_SHA256[i]
        for i, seed in enumerate(SELECTOR_SEEDS)
    )
    reader_roundtrip = all(
        c216.model_sha(readers[seed]) == READER_FINAL_SHA256[i]
        for i, seed in enumerate(READER_SEEDS)
    )
    reference = readable_reference(selectors, readers)

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

    save_json("coverage-plan.json", dict(manifest(), source_blobs=pins))
    np.savez_compressed(
        out / "coverage-dataset.npz",
        features=data["features"],
        labels=data["labels"],
        split_codes=data["split_codes"],
    )
    record("coverage-dataset.npz")

    fit_records = []
    state_dicts = []
    for seed in COVERAGE_SEEDS:
        model, fit_record = fit(seed, train_x, train_y)
        fit_records.append(fit_record)
        state_dicts.append(
            {name: tensor.detach().cpu().clone() for name, tensor in model.state_dict().items()}
        )

    bundle = dict(
        schema="fold-v5f-coverage-checkpoints-v1",
        seeds=list(COVERAGE_SEEDS),
        config=dict(input_width=7, hidden_width=12, class_count=4),
        state_dicts=state_dicts,
    )
    torch.save(bundle, out / "coverage-checkpoints.pt")
    record("coverage-checkpoints.pt")

    restored_bundle = torch.load(out / "coverage-checkpoints.pt", map_location="cpu",
                                 weights_only=True)
    require(
        restored_bundle["schema"] == "fold-v5f-coverage-checkpoints-v1"
        and tuple(restored_bundle["seeds"]) == COVERAGE_SEEDS
        and restored_bundle["config"] == dict(input_width=7, hidden_width=12, class_count=4),
        "Coverage checkpoint bundle identity drift",
    )

    seed_records = []
    roundtrips = []
    for seed, state_dict, fit_record in zip(
        COVERAGE_SEEDS, restored_bundle["state_dicts"], fit_records, strict=True
    ):
        restored = new_classifier()
        restored.load_state_dict(state_dict, strict=True)
        restored.eval()
        final_sha = model_sha(restored)
        roundtrip = final_sha == fit_record["final_sha256"]
        roundtrips.append(roundtrip)
        score = score_classifier(restored, data)
        seed_records.append(dict(
            seed=seed,
            checkpoint_roundtrip=roundtrip,
            initial_sha256=fit_record["initial_sha256"],
            final_sha256=final_sha,
            initial_loss=fit_record["initial_loss"],
            final_loss=fit_record["final_loss"],
            **score,
        ))

    save_json("evaluation.json", dict(
        coverage_seed_records=seed_records,
        fit_records=fit_records,
        readable_reference=reference,
    ))

    learned_calls = sum(r["training_forward_calls"] for r in fit_records) + sum(
        r["scoring_forward_calls"] for r in seed_records
    )
    summary = dict(
        coverage_seed_records=seed_records,
        all_coverage_checkpoint_roundtrips=all(roundtrips),
        all_selector_checkpoint_roundtrips=selector_roundtrip,
        all_reader_checkpoint_roundtrips=reader_roundtrip,
        coverage_data_sha256=data["content_sha256"],
        readable_reference=reference,
        learned_coverage_calls=learned_calls,
        frozen_selector_forward_calls=reference["frozen_selector_forward_calls"],
        frozen_reader_forward_calls=reference["frozen_reader_forward_calls"],
        writer_training_steps=0,
        selector_training_steps=0,
        reader_training_steps=0,
        numeric_unsafe_classified=0,
    )
    save_json("validation-summary.json", summary)

    guard()
    precheck(c218_summary, root)
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
        C218_summary_sha256=PARENT_C218_SHA,
        source_blobs=pins,
        input_sha256=protected,
        artifacts=artifacts,
        validation_summary=summary,
        fit_records=fit_records,
        trained_coverage_models=3,
        coverage_parameters_per_model=148,
        training_steps_total=sum(r["steps"] for r in fit_records),
        training_examples_drawn=sum(r["examples_drawn"] for r in fit_records),
        learned_coverage_calls=learned_calls,
        frozen_selector_forward_calls=reference["frozen_selector_forward_calls"],
        frozen_reader_forward_calls=reference["frozen_reader_forward_calls"],
        model_forward_calls=learned_calls
            + reference["frozen_selector_forward_calls"]
            + reference["frozen_reader_forward_calls"],
        writer_training_steps=0,
        selector_training_steps=0,
        reader_training_steps=0,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        learned_coverage_classifier=True,
        learned_writer=False,
        learned_port_selector=False,
        learned_reader=False,
        numeric_unsafe_classified=0,
        limitations=[
            "tiny synthetic target-specific coverage summary",
            "state features are structured runtime metadata, not natural-language understanding",
            "Writer is not exercised; accepted Selector/Reader are frozen references only",
            "NUMERIC_UNSAFE remains deterministic and outside Coverage classification",
            "no memory-cost comparison or Gate F claim",
        ],
    )
    validate_result(result)
    (out / "summary.json").write_bytes(blob(result))
    print(
        "[C219] learned Coverage "
        + " ".join(
            f"seed={r['seed']} eval={r['eval_accuracy']:.3f} "
            f"blind={r['state_blind_eval_accuracy']:.3f} "
            f"scopeblind={r['scope_blind_missing_oos_accuracy']:.3f}"
            for r in seed_records
        ),
        flush=True,
    )
    print("=== C219 RESULT ===", flush=True)
    print(blob(result).decode(), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c218-summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
