"""C220: frozen learned memory-stack integration.

This experiment introduces no new learned component and performs no training. It composes the
accepted C218 semantic Writer, C219 Coverage classifier, C217 Port Selector and C216 Reader
checkpoints through a minimal deterministic stack gate.

Operation kind remains oracle. The question is whether independently accepted learned components
compose without retraining across ASSERT/HOT/COMMIT/REPLACE plus MISSING/OUT_OF_SCOPE states.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import unittest

import torch

from fold_lm.v05 import memory_bridge as memory
from fold_lm.v05 import memory_coverage as coverage
from fold_lm.v05 import memory_stack as stack
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_f_c216_learned_reader as c216
from fold_lm.v05_benchmarks import gate_f_c217_learned_port_selector as c217
from fold_lm.v05_benchmarks import gate_f_c218_learned_writer as c218
from fold_lm.v05_benchmarks import gate_f_c219_learned_coverage as c219

EXPERIMENT_ID = "C220-v5f-frozen-learned-stack-integration"
STAGE = "V5-F-FROZEN-LEARNED-STACK-INTEGRATION"
BASE = "63cd2f39275086c50024bed206e3ca3da976219e"
PARENT_C219_EXECUTION = "5a613ed07c34d1735d20c5849464116cc00d333c"
PARENT_C219_SHA = "dbf54bd3cdc5b2fbd82a68a62bcdbaad806b8946b817776d94527a5bdcbaee14"
PARENT_C219_VALIDATION_SHA = "a380cbb38c686757d4a296c8e557d7b2f304ea72ce4b583185c02099958685d4"

COVERAGE_CHECKPOINT_SHA = "1ba50ab3b621b75a0b5c0528f2eb03c6f11e8a0000122563357709d386cee0a1"
WRITER_CHECKPOINT_SHA = "3313bb507527b7e4798333c8b8c7f1e0e2ea2f9f2cd513060b505184c87d5c9d"
SELECTOR_CHECKPOINT_SHA = "ab8892e6562a4801a30fea853fdbc712d69d9c5077e32c0b8fab6e555fead215"
READER_CHECKPOINT_SHA = "bf96cf6cec13bfdb9c71e374b0e11dd104365add1c5947f2123f4e4ea9f051af"

EPISODE_PLAN_SHA = "99f84e9d05327c8c483b45928676009f6be198e5d568a285d2e893e1279e144f"
MANIFEST_SHA = "12b5995967abba8c89f2a07c01e6e29afbd96b02db4a0561872a70201deeab52"

WRITER_SEEDS = (218001, 218002, 218003)
WRITER_FINAL_SHA256 = (
    "0edbd5ac2935f78952f8114ef500e9ce09aada4f5531a0e823ac25efd8991e1c",
    "46a6656547663e618fbf66eca0ae4412174000fc816e36dcfa1f11fc6e72260c",
    "fe5c7e397755b7e07957ad96bc3417258d0a6fb3f9530ecf57bbf0ccaa8ae39b",
)
COVERAGE_SEEDS = (219001, 219002, 219003)
COVERAGE_FINAL_SHA256 = (
    "ce326c60ca88e6adfc7aa4198e08784baadd9e8fb78f42f49b00635d0fcc30b8",
    "c1fede5f39bb5b7c4e7bd5f6a23ce40e20477fc42367af15e610318c0c5ca583",
    "1980b8590ff0cf75aa10e1076b00f9996ccf8f5c2e84ad5baa535f7c7aae2d07",
)
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

OWN = (
    "fold_lm/v05/memory_stack.py",
    "fold_lm/v05_benchmarks/gate_f_c220_frozen_learned_stack.py",
    "tests_lm/test_v05_c220_frozen_learned_stack.py",
    "tools/run_c220.ps1",
    "tools/invoke_c220.ps1",
    "docs/experiment-ledger-addendum-c220-preregistration.md",
    "docs/v5f-frozen-learned-stack-integration-v0.1.md",
)
OUTPUTS = {
    "stack-plan.json",
    "episode-sets.json",
    "combination-results.json",
    "component-fingerprints.json",
    "validation-summary.json",
}
DIRECT_REPO_DEPENDENCIES = (
    "fold_lm/v05/memory_bank.py",
    "fold_lm/v05/memory_bridge.py",
    "fold_lm/v05/memory_capsule_bridge.py",
    "fold_lm/v05/memory_reader.py",
    "fold_lm/v05/memory_port_selector.py",
    "fold_lm/v05/memory_writer.py",
    "fold_lm/v05/memory_coverage.py",
    "fold_lm/v05/memory_stack.py",
    "fold_lm/v05_benchmarks/gate_e_c175_frozen_prediction_audit.py",
    "fold_lm/v05_benchmarks/gate_e_c205_phase0_batch_composition_attribution.py",
    "fold_lm/v05_benchmarks/gate_f_c216_learned_reader.py",
    "fold_lm/v05_benchmarks/gate_f_c217_learned_port_selector.py",
    "fold_lm/v05_benchmarks/gate_f_c218_learned_writer.py",
    "fold_lm/v05_benchmarks/gate_f_c219_learned_coverage.py",
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def episode_plan():
    return [
        dict(
            label="missing_alpha", query="alpha", expected_coverage="MISSING",
            target_class=None, writer_target=None, operation="NONE",
        ),
        dict(
            label="out_of_scope_beta", query="beta", expected_coverage="OUT_OF_SCOPE",
            target_class=None, writer_target=None, operation="END_SCOPE_ORACLE",
        ),
        dict(
            label="hot_alpha", query="alpha", expected_coverage="HOT_REQUIRED",
            target_class=0, writer_target=0, operation="ASSERT",
        ),
        dict(
            label="supported_alpha", query="alpha", expected_coverage="SUPPORTED",
            target_class=0, writer_target=0, operation="ASSERT_COMMIT",
        ),
        dict(
            label="hot_beta", query="beta", expected_coverage="HOT_REQUIRED",
            target_class=2, writer_target=5, operation="ASSERT",
        ),
        dict(
            label="supported_beta", query="beta", expected_coverage="SUPPORTED",
            target_class=2, writer_target=5, operation="ASSERT_COMMIT",
        ),
        dict(
            label="replace_alpha", query="alpha", expected_coverage="SUPPORTED",
            target_class=1, writer_target=1, operation="REPLACE",
        ),
        dict(
            label="replace_beta", query="beta", expected_coverage="SUPPORTED",
            target_class=0, writer_target=3, operation="REPLACE",
        ),
    ]


def manifest():
    return dict(
        experiment_id=EXPERIMENT_ID,
        stage=STAGE,
        acceptance_base=BASE,
        parent_c219_execution=PARENT_C219_EXECUTION,
        parent_c219_sha256=PARENT_C219_SHA,
        parent_c219_validation_sha256=PARENT_C219_VALIDATION_SHA,
        coverage_checkpoint_sha256=COVERAGE_CHECKPOINT_SHA,
        writer_checkpoint_sha256=WRITER_CHECKPOINT_SHA,
        selector_checkpoint_sha256=SELECTOR_CHECKPOINT_SHA,
        reader_checkpoint_sha256=READER_CHECKPOINT_SHA,
        episode_plan_sha256=EPISODE_PLAN_SHA,
        episodes=8,
        readable_episodes=6,
        nonreadable_episodes=2,
        writer_checkpoints=3,
        coverage_checkpoints=3,
        selector_checkpoints=3,
        reader_checkpoints=3,
        checkpoint_combinations=81,
        decision_rows=648,
        readable_decisions=486,
        nonreadable_decisions=162,
        operation_kind="oracle ASSERT/REPLACE/END_SCOPE",
        learned_components_frozen=True,
        new_training_steps=0,
        writer_training_steps=0,
        coverage_training_steps=0,
        selector_training_steps=0,
        reader_training_steps=0,
        frozen_writer_forward_calls=3,
        frozen_coverage_forward_calls=9,
        frozen_selector_forward_calls=3,
        frozen_reader_forward_calls=27,
        model_forward_calls=42,
        learned_writer_operation_slots=18,
        oracle_initialization_writes=12,
        oracle_end_scope_ops=3,
        chunk_commit_slots=18,
        gate_writer_target_accuracy=1.0,
        gate_selector_route_accuracy=1.0,
        gate_coverage_teacher_accuracy=1.0,
        gate_integration_accuracy=1.0,
        gate_readable_answer_accuracy=1.0,
        gate_nonreadable_suppression_accuracy=1.0,
        gate_missing_oos_confusions=0,
        gate_placement_mismatches=0,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        scope=(
            "frozen composition of accepted learned Writer/Coverage/Port Selector/Reader; "
            "oracle operation kind; no joint training"
        ),
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


def _restore_bundle(path, schema, seeds, config):
    payload = torch.load(path, map_location="cpu", weights_only=True)
    require(
        payload["schema"] == schema
        and tuple(payload["seeds"]) == seeds
        and payload["config"] == config,
        "checkpoint bundle identity drift:" + schema,
    )
    return payload


def restore_writer_models(parent_summary):
    checkpoint = find_protected_input(parent_summary, "writer-checkpoints.pt", WRITER_CHECKPOINT_SHA)
    payload = _restore_bundle(
        checkpoint,
        "fold-v5f-writer-checkpoints-v1",
        WRITER_SEEDS,
        dict(input_width=5, hidden_width=12, relation_classes=6),
    )
    models = {}
    for seed, state_dict, expected in zip(
        WRITER_SEEDS, payload["state_dicts"], WRITER_FINAL_SHA256, strict=True
    ):
        model = c218.new_writer()
        model.load_state_dict(state_dict, strict=True)
        model.eval()
        require(c218.model_sha(model) == expected, "Frozen Writer changed")
        models[seed] = model
    return models


def restore_coverage_models(parent_summary, c219_summary):
    checkpoint = Path(c219_summary).resolve().parent / "coverage-checkpoints.pt"
    require(checkpoint.is_file() and audit.sha(checkpoint) == COVERAGE_CHECKPOINT_SHA,
            "C219 Coverage checkpoint changed")
    payload = _restore_bundle(
        checkpoint,
        "fold-v5f-coverage-checkpoints-v1",
        COVERAGE_SEEDS,
        dict(input_width=7, hidden_width=12, class_count=4),
    )
    models = {}
    for seed, state_dict, expected in zip(
        COVERAGE_SEEDS, payload["state_dicts"], COVERAGE_FINAL_SHA256, strict=True
    ):
        model = c219.new_classifier()
        model.load_state_dict(state_dict, strict=True)
        model.eval()
        require(c219.model_sha(model) == expected, "Frozen Coverage changed")
        models[seed] = model
    return models


def restore_selector_models(parent_summary):
    checkpoint = find_protected_input(
        parent_summary, "selector-checkpoints.pt", SELECTOR_CHECKPOINT_SHA
    )
    payload = _restore_bundle(
        checkpoint,
        "fold-v5f-port-selector-checkpoints-v1",
        SELECTOR_SEEDS,
        dict(input_width=4, hidden_width=8, port_count=2),
    )
    models = {}
    for seed, state_dict, expected in zip(
        SELECTOR_SEEDS, payload["state_dicts"], SELECTOR_FINAL_SHA256, strict=True
    ):
        model = c217.new_selector()
        model.load_state_dict(state_dict, strict=True)
        model.eval()
        require(c217.model_sha(model) == expected, "Frozen Selector changed")
        models[seed] = model
    return models


def restore_reader_models(parent_summary):
    checkpoint = find_protected_input(parent_summary, "reader-checkpoints.pt", READER_CHECKPOINT_SHA)
    payload = _restore_bundle(
        checkpoint,
        "fold-v5f-reader-checkpoints-v1",
        READER_SEEDS,
        dict(input_width=1, hidden_width=8, answer_classes=3),
    )
    models = {}
    for seed, state_dict, expected in zip(
        READER_SEEDS, payload["state_dicts"], READER_FINAL_SHA256, strict=True
    ):
        model = c216.new_reader()
        model.load_state_dict(state_dict, strict=True)
        model.eval()
        require(c216.model_sha(model) == expected, "Frozen Reader changed")
        models[seed] = model
    return models


def writer_eval_features():
    targets = (0, 5, 1, 3)
    rows = []
    for target in targets:
        factor, semantic_class, _, _ = c218.decode_write_class(target)
        role = (1.0, 0.0) if factor == "alpha" else (0.0, 1.0)
        semantic = float(c218.VALUES[semantic_class])
        rows.append((*role, semantic, 1.0, 1.0))
    return targets, torch.tensor(rows, dtype=torch.float32)


def frozen_writer_predictions(models):
    targets, x = writer_eval_features()
    result = {}
    forwards = 0
    correct = 0
    total = 0
    for seed in WRITER_SEEDS:
        before = c218.model_sha(models[seed])
        with torch.no_grad():
            pred = models[seed](x).argmax(dim=-1)
        forwards += 1
        require(c218.model_sha(models[seed]) == before == WRITER_FINAL_SHA256[
            WRITER_SEEDS.index(seed)
        ], "Frozen Writer mutated")
        mapping = {target: int(pred[i].item()) for i, target in enumerate(targets)}
        result[seed] = mapping
        correct += sum(int(mapping[target] == target) for target in targets)
        total += len(targets)
    return result, forwards, correct / total


def frozen_selector_routes(models):
    x = torch.tensor([[1,0,1,1],[0,1,1,1]], dtype=torch.float32)
    routes = {}
    forwards = 0
    correct = 0
    total = 0
    for seed in SELECTOR_SEEDS:
        before = c217.model_sha(models[seed])
        with torch.no_grad():
            pred = models[seed](x).argmax(dim=-1)
        forwards += 1
        require(c217.model_sha(models[seed]) == before == SELECTOR_FINAL_SHA256[
            SELECTOR_SEEDS.index(seed)
        ], "Frozen Selector mutated")
        route = {"alpha": int(pred[0].item()), "beta": int(pred[1].item())}
        routes[seed] = route
        correct += int(route["alpha"] == 0) + int(route["beta"] == 1)
        total += 2
    return routes, forwards, correct / total


def query_meta(query):
    if query == "alpha":
        return 0, "alpha", memory.GLOBAL_SCOPE
    if query == "beta":
        return 1, "beta", "project"
    raise ValueError("unknown query")


def coverage_feature(state, query):
    role, factor, scope = query_meta(query)
    feature, teacher = coverage.target_summary(
        state,
        query_role=role,
        scope_id=scope,
        factor_id=factor,
        nuisance=(1.0, 1.0),
    )
    return feature, teacher


def _capture(bank, state, plan_row, *, valid=True):
    feature, teacher = coverage_feature(state, plan_row["query"])
    readable = teacher in (coverage.CoverageClass.SUPPORTED, coverage.CoverageClass.HOT_REQUIRED)
    readout = None
    if readable:
        read = bank.read(state)
        if read.value is not None:
            readout = [float(v) for v in read.value.tolist()]
        else:
            valid = False
    return dict(
        **plan_row,
        actual_coverage=teacher.name,
        coverage_features=[float(x) for x in feature.tolist()],
        readable_from_state=bool(readable),
        readout=readout,
        valid=bool(valid),
    )


def build_episode_set(prediction_by_target, writer_seed):
    plan = {row["label"]: row for row in episode_plan()}
    episodes = []
    learned_ops = 0
    oracle_writes = 0
    oracle_end_scope_ops = 0
    commits = 0
    failures = 0

    # MISSING alpha.
    bank = c216.build_bank()
    state = bank.initial_state()
    episodes.append(_capture(bank, state, plan["missing_alpha"]))

    # OUT_OF_SCOPE beta.
    bank = c216.build_bank()
    state = bank.initial_state()
    try:
        state, read = bank.apply(
            state,
            memory.MemoryOp(
                kind=memory.MemoryOpKind.END_SCOPE,
                expected_memory_revision=state.memory_revision,
                scope_id="project",
            ),
        )
        require(read is None, "END_SCOPE returned read")
        oracle_end_scope_ops += 1
        episodes.append(_capture(bank, state, plan["out_of_scope_beta"]))
    except (ValueError, RuntimeError, AssertionError):
        failures += 1
        episodes.append(_capture(bank, state, plan["out_of_scope_beta"], valid=False))

    def learned_assert(label, target, commit):
        nonlocal learned_ops, commits, failures
        bank = c216.build_bank()
        state = bank.initial_state()
        valid = True
        try:
            learned_ops += 1
            state, read = bank.apply(
                state,
                c218.memory_op(
                    memory.MemoryOpKind.ASSERT,
                    state,
                    prediction_by_target[target],
                    1,
                    f"stack:{writer_seed}:{label}",
                ),
            )
            require(read is None, "learned ASSERT returned read")
            if commit:
                state, status = bank.commit(state)
                require(status.value == "COMMITTED", "learned ASSERT commit failed")
                commits += 1
        except (ValueError, RuntimeError, AssertionError):
            failures += 1
            valid = False
        episodes.append(_capture(bank, state, plan[label], valid=valid))

    learned_assert("hot_alpha", 0, False)
    learned_assert("supported_alpha", 0, True)
    learned_assert("hot_beta", 5, False)
    learned_assert("supported_beta", 5, True)

    def learned_replace(label, target, alpha_initial, beta_initial):
        nonlocal learned_ops, oracle_writes, commits, failures
        bank = c216.build_bank()
        valid = True
        try:
            state = c218.oracle_initial_state(
                bank, alpha_initial, beta_initial, f"stack:{writer_seed}:{label}:oracle"
            )
            oracle_writes += 2
            commits += 2
            learned_ops += 1
            state, read = bank.apply(
                state,
                c218.memory_op(
                    memory.MemoryOpKind.REPLACE,
                    state,
                    prediction_by_target[target],
                    3,
                    f"stack:{writer_seed}:{label}:replace",
                ),
            )
            require(read is None, "learned REPLACE returned read")
        except (ValueError, RuntimeError, AssertionError):
            failures += 1
            valid = False
            if "state" not in locals():
                state = bank.initial_state()
        episodes.append(_capture(bank, state, plan[label], valid=valid))

    # Target alpha=class1; beta remains class2 so wrong routing is detectably wrong.
    learned_replace("replace_alpha", 1, 2, 2)
    # Target beta=class0; alpha remains class1 so wrong routing is detectably wrong.
    learned_replace("replace_beta", 3, 1, 2)

    require(len(episodes) == 8, "episode-set size drift")
    return episodes, dict(
        learned_writer_operation_applications=learned_ops,
        oracle_initialization_writes=oracle_writes,
        oracle_end_scope_ops=oracle_end_scope_ops,
        chunk_commits=commits,
        operation_failures=failures,
    )


def coverage_predictions(models, episode_sets):
    result = {}
    forwards = 0
    correct = total = 0
    for writer_seed in WRITER_SEEDS:
        x = torch.tensor(
            [row["coverage_features"] for row in episode_sets[writer_seed]],
            dtype=torch.float32,
        )
        result[writer_seed] = {}
        for coverage_seed in COVERAGE_SEEDS:
            before = c219.model_sha(models[coverage_seed])
            with torch.no_grad():
                pred = models[coverage_seed](x).argmax(dim=-1)
            forwards += 1
            require(
                c219.model_sha(models[coverage_seed]) == before
                == COVERAGE_FINAL_SHA256[COVERAGE_SEEDS.index(coverage_seed)],
                "Frozen Coverage mutated",
            )
            predictions = [int(v) for v in pred.tolist()]
            result[writer_seed][coverage_seed] = predictions
            for row, value in zip(episode_sets[writer_seed], predictions, strict=True):
                actual = int(coverage.CoverageClass[row["actual_coverage"]])
                correct += int(value == actual)
                total += 1
    return result, forwards, correct / total


def reader_predictions(models, episode_sets, routes):
    readable_labels = [
        row["label"] for row in episode_plan() if row["target_class"] is not None
    ]
    result = {}
    forwards = 0
    for writer_seed in WRITER_SEEDS:
        by_label = {row["label"]: row for row in episode_sets[writer_seed]}
        result[writer_seed] = {}
        for selector_seed in SELECTOR_SEEDS:
            values = []
            validity = {}
            for label in readable_labels:
                row = by_label[label]
                readout = row["readout"]
                if row["valid"] and row["readable_from_state"] and readout is not None:
                    port = routes[selector_seed][row["query"]]
                    scalar = stack.selected_scalar(torch.tensor(readout, dtype=torch.float64), port)
                    values.append(float(scalar.item()))
                    validity[label] = True
                else:
                    values.append(0.0)
                    validity[label] = False

            x = torch.tensor(values, dtype=torch.float32).reshape(-1, 1)
            result[writer_seed][selector_seed] = {}
            for reader_seed in READER_SEEDS:
                before = c216.model_sha(models[reader_seed])
                with torch.no_grad():
                    pred = models[reader_seed](x).argmax(dim=-1)
                forwards += 1
                require(
                    c216.model_sha(models[reader_seed]) == before
                    == READER_FINAL_SHA256[READER_SEEDS.index(reader_seed)],
                    "Frozen Reader mutated",
                )
                result[writer_seed][selector_seed][reader_seed] = dict(
                    predictions={
                        label: int(pred[i].item()) for i, label in enumerate(readable_labels)
                    },
                    validity=validity,
                )
    return result, forwards


def integration_results(
    episode_sets,
    coverage_pred,
    routes,
    reader_pred,
):
    plan_by_label = {row["label"]: row for row in episode_plan()}
    combinations = []
    total = success = 0
    readable_total = readable_success = 0
    suppression_total = suppression_success = 0
    expected_coverage_total = expected_coverage_success = 0
    missing_oos_confusions = 0
    placement_mismatches = 0

    for writer_seed in WRITER_SEEDS:
        episodes = {row["label"]: row for row in episode_sets[writer_seed]}
        for coverage_seed in COVERAGE_SEEDS:
            coverage_values = coverage_pred[writer_seed][coverage_seed]
            coverage_by_label = {
                row["label"]: coverage_values[i]
                for i, row in enumerate(episode_sets[writer_seed])
            }
            for selector_seed in SELECTOR_SEEDS:
                for reader_seed in READER_SEEDS:
                    episode_records = []
                    combo_success = 0
                    combo_readable = 0
                    combo_suppression = 0
                    for label, expected in plan_by_label.items():
                        row = episodes[label]
                        predicted_coverage = coverage_by_label[label]
                        expected_coverage = int(coverage.CoverageClass[expected["expected_coverage"]])
                        actual_coverage = int(coverage.CoverageClass[row["actual_coverage"]])
                        gate = stack.gate_for_coverage(predicted_coverage)

                        coverage_ok = (
                            predicted_coverage == expected_coverage
                            and actual_coverage == expected_coverage
                        )
                        expected_coverage_total += 1
                        expected_coverage_success += int(coverage_ok)

                        if expected["target_class"] is None:
                            suppression_total += 1
                            action_ok = (
                                expected["expected_coverage"] == "MISSING"
                                and gate.action is stack.StackAction.SUPPRESS_MISSING
                            ) or (
                                expected["expected_coverage"] == "OUT_OF_SCOPE"
                                and gate.action is stack.StackAction.SUPPRESS_OUT_OF_SCOPE
                            )
                            ok = row["valid"] and coverage_ok and action_ok
                            suppression_success += int(ok)
                            combo_suppression += int(ok)
                            answer = None
                        else:
                            readable_total += 1
                            read_record = reader_pred[writer_seed][selector_seed][reader_seed]
                            answer = read_record["predictions"][label]
                            answer_ok = (
                                read_record["validity"][label]
                                and answer == expected["target_class"]
                            )
                            ok = row["valid"] and coverage_ok and gate.readable and answer_ok
                            readable_success += int(ok)
                            combo_readable += int(ok)

                        if (
                            expected["expected_coverage"] == "MISSING"
                            and predicted_coverage == int(coverage.CoverageClass.OUT_OF_SCOPE)
                        ) or (
                            expected["expected_coverage"] == "OUT_OF_SCOPE"
                            and predicted_coverage == int(coverage.CoverageClass.MISSING)
                        ):
                            missing_oos_confusions += 1

                        total += 1
                        success += int(ok)
                        combo_success += int(ok)
                        episode_records.append(dict(
                            label=label,
                            expected_coverage=expected["expected_coverage"],
                            actual_coverage=row["actual_coverage"],
                            predicted_coverage=coverage.CoverageClass(predicted_coverage).name,
                            expected_answer=expected["target_class"],
                            predicted_answer=answer,
                            success=ok,
                        ))

                    # HOT/COMMITTED semantic parity is checked independently of Coverage seed.
                    rp = reader_pred[writer_seed][selector_seed][reader_seed]["predictions"]
                    rv = reader_pred[writer_seed][selector_seed][reader_seed]["validity"]
                    for hot_label, committed_label in (
                        ("hot_alpha", "supported_alpha"),
                        ("hot_beta", "supported_beta"),
                    ):
                        if (
                            not rv[hot_label]
                            or not rv[committed_label]
                            or rp[hot_label] != rp[committed_label]
                        ):
                            placement_mismatches += 1

                    combinations.append(dict(
                        writer_seed=writer_seed,
                        coverage_seed=coverage_seed,
                        selector_seed=selector_seed,
                        reader_seed=reader_seed,
                        success_count=combo_success,
                        readable_success_count=combo_readable,
                        suppression_success_count=combo_suppression,
                        episodes=episode_records,
                    ))

    return dict(
        combinations=combinations,
        checkpoint_combinations=len(combinations),
        decision_rows=total,
        integration_accuracy=success / total,
        expected_coverage_accuracy=expected_coverage_success / expected_coverage_total,
        readable_answer_accuracy=readable_success / readable_total,
        nonreadable_suppression_accuracy=suppression_success / suppression_total,
        readable_decisions=readable_total,
        nonreadable_decisions=suppression_total,
        missing_oos_confusions=missing_oos_confusions,
        placement_mismatches=placement_mismatches,
    )


def gate(summary):
    return (
        summary.get("all_writer_checkpoint_roundtrips") is True
        and summary.get("all_coverage_checkpoint_roundtrips") is True
        and summary.get("all_selector_checkpoint_roundtrips") is True
        and summary.get("all_reader_checkpoint_roundtrips") is True
        and summary.get("writer_target_accuracy") == 1.0
        and summary.get("selector_route_accuracy") == 1.0
        and summary.get("coverage_teacher_accuracy") == 1.0
        and summary.get("checkpoint_combinations") == 81
        and summary.get("decision_rows") == 648
        and summary.get("readable_decisions") == 486
        and summary.get("nonreadable_decisions") == 162
        and summary.get("integration_accuracy") == 1.0
        and summary.get("expected_coverage_accuracy") == 1.0
        and summary.get("readable_answer_accuracy") == 1.0
        and summary.get("nonreadable_suppression_accuracy") == 1.0
        and summary.get("missing_oos_confusions") == 0
        and summary.get("placement_mismatches") == 0
        and summary.get("operation_failures") == 0
        and summary.get("learned_writer_operation_applications") == 18
        and summary.get("oracle_initialization_writes") == 12
        and summary.get("oracle_end_scope_ops") == 3
        and summary.get("chunk_commits") == 18
        and summary.get("frozen_writer_forward_calls") == 3
        and summary.get("frozen_coverage_forward_calls") == 9
        and summary.get("frozen_selector_forward_calls") == 3
        and summary.get("frozen_reader_forward_calls") == 27
        and summary.get("new_training_steps") == 0
    )


def precheck(c219_summary, root):
    root = Path(root)
    require(audit.sha(c219_summary) == PARENT_C219_SHA, "C219 summary changed")
    p219 = audit.read_json(c219_summary)
    c219.validate_result(p219)
    require(
        p219.get("commit_sha") == PARENT_C219_EXECUTION
        and p219.get("status") == "PASS"
        and c219.gate(p219["validation_summary"])
        and len(p219.get("source_blobs", {})) == 151
        and len(p219.get("input_sha256", {})) == 169,
        "Wrong accepted C219 parent",
    )

    protected = dict(p219["input_sha256"])
    for name, wanted in protected.items():
        require(Path(name).is_file() and audit.sha(name) == wanted,
                "Changed inherited protected input:" + name)

    pins = dict(p219["source_blobs"])
    for name, expected_blob in pins.items():
        actual = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()
        require(actual == expected_blob, "C219 source pin changed:" + name)

    protected[str(Path(c219_summary).resolve())] = PARENT_C219_SHA
    validation_seen = coverage_seen = False
    for artifact in p219["artifacts"]:
        path = audit.safe_child(Path(c219_summary).resolve().parent, artifact["file"])
        require(
            path.is_file()
            and path.stat().st_size == artifact["serialized_bytes"]
            and audit.sha(path) == artifact["sha256"],
            "Changed C219 artifact:" + artifact["file"],
        )
        protected[str(path.resolve())] = artifact["sha256"]
        if artifact["file"] == "validation-summary.json":
            require(artifact["sha256"] == PARENT_C219_VALIDATION_SHA,
                    "C219 validation artifact changed")
            validation_seen = True
        if artifact["file"] == "coverage-checkpoints.pt":
            require(artifact["sha256"] == COVERAGE_CHECKPOINT_SHA,
                    "C219 Coverage checkpoint changed")
            coverage_seen = True
    require(validation_seen and coverage_seen, "C219 deciding artifact missing")

    find_protected_input(p219, "writer-checkpoints.pt", WRITER_CHECKPOINT_SHA)
    find_protected_input(p219, "selector-checkpoints.pt", SELECTOR_CHECKPOINT_SHA)
    find_protected_input(p219, "reader-checkpoints.pt", READER_CHECKPOINT_SHA)

    allpins = dict(pins)
    for name in OWN:
        allpins[name] = audit.git(root, "rev-parse", "HEAD:" + name).decode().strip()

    for dependency in DIRECT_REPO_DEPENDENCIES:
        require(dependency in allpins, "Unpinned direct dependency:" + dependency)

    protected.update(audit.protect_tree_files(root, allpins))
    pins.update({name: allpins[name] for name in OWN})

    require(len(pins) == 158, "C220 source pin count drift")
    require(len(protected) == 182, "C220 protected input count drift")
    require(digest(episode_plan()) == EPISODE_PLAN_SHA, "C220 episode plan drift")
    require(digest(manifest()) == MANIFEST_SHA, "C220 manifest drift")
    return p219, pins, protected


def regression_modules(root):
    names = c219.regression_modules(root)
    require(len(names) == len(set(names)) == 104, "Historical regression module drift")
    return names + ["tests_lm.test_v05_c220_frozen_learned_stack"]


def regression_suite(root):
    names = regression_modules(root)
    loaded = unittest.defaultTestLoader.loadTestsFromNames(names)
    tests = list(c205._iter_tests(loaded))
    ids = [test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded) == 1, "Historical dynamic test identity drift:" + excluded)
    kept = [test for test in tests if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS]
    require(
        len(tests) == 2336
        and len(kept) == 2335
        and not any(test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS for test in kept),
        "C220 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"] == EXPERIMENT_ID
        and payload["stage"] == STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C220",
    )
    require(
        len(payload["source_blobs"]) == 158
        and len(payload["input_sha256"]) == 182
        and len(payload["artifacts"]) == 5
        and {a["file"] for a in payload["artifacts"]} == OUTPUTS,
        "C220 coverage drift",
    )
    require(
        payload["trained_models"] == 0
        and payload["new_training_steps"] == 0
        and payload["model_forward_calls"] == 42
        and payload["network_calls"] == 0,
        "C220 workload drift",
    )
    require(
        payload["production_runtime_modified"] is True
        and payload["gate_f_candidate"] is False
        and payload["operation_kind_learned"] is False
        and payload["joint_training"] is False,
        "C220 scope drift",
    )
    require(
        payload["status"] == ("PASS" if gate(payload["validation_summary"]) else "FAIL"),
        "C220 gate drift",
    )


def run(*, c219_summary, output_dir, expected_head):
    root = Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root, "rev-parse", "HEAD").decode().strip() == expected_head,
                "HEAD mismatch")
        require(audit.git(root, "branch", "--show-current").decode().strip()
                == "feat/sft-target-loss", "Branch mismatch")
        require(not audit.git(root, "status", "--porcelain", "--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    p219, pins, protected = precheck(c219_summary, root)

    writers = restore_writer_models(p219)
    coverages = restore_coverage_models(p219, c219_summary)
    selectors = restore_selector_models(p219)
    readers = restore_reader_models(p219)

    writer_predictions, writer_forwards, writer_accuracy = frozen_writer_predictions(writers)
    routes, selector_forwards, selector_accuracy = frozen_selector_routes(selectors)

    episode_sets = {}
    aggregate_ops = dict(
        learned_writer_operation_applications=0,
        oracle_initialization_writes=0,
        oracle_end_scope_ops=0,
        chunk_commits=0,
        operation_failures=0,
    )
    for writer_seed in WRITER_SEEDS:
        rows, counts = build_episode_set(writer_predictions[writer_seed], writer_seed)
        episode_sets[writer_seed] = rows
        for key in aggregate_ops:
            aggregate_ops[key] += counts[key]

    coverage_pred, coverage_forwards, coverage_teacher_accuracy = coverage_predictions(
        coverages, episode_sets
    )
    reader_pred, reader_forwards = reader_predictions(readers, episode_sets, routes)
    integrated = integration_results(episode_sets, coverage_pred, routes, reader_pred)

    writer_roundtrip = all(
        c218.model_sha(writers[seed]) == WRITER_FINAL_SHA256[i]
        for i, seed in enumerate(WRITER_SEEDS)
    )
    coverage_roundtrip = all(
        c219.model_sha(coverages[seed]) == COVERAGE_FINAL_SHA256[i]
        for i, seed in enumerate(COVERAGE_SEEDS)
    )
    selector_roundtrip = all(
        c217.model_sha(selectors[seed]) == SELECTOR_FINAL_SHA256[i]
        for i, seed in enumerate(SELECTOR_SEEDS)
    )
    reader_roundtrip = all(
        c216.model_sha(readers[seed]) == READER_FINAL_SHA256[i]
        for i, seed in enumerate(READER_SEEDS)
    )

    summary = dict(
        all_writer_checkpoint_roundtrips=writer_roundtrip,
        all_coverage_checkpoint_roundtrips=coverage_roundtrip,
        all_selector_checkpoint_roundtrips=selector_roundtrip,
        all_reader_checkpoint_roundtrips=reader_roundtrip,
        writer_target_accuracy=writer_accuracy,
        selector_route_accuracy=selector_accuracy,
        coverage_teacher_accuracy=coverage_teacher_accuracy,
        frozen_writer_forward_calls=writer_forwards,
        frozen_coverage_forward_calls=coverage_forwards,
        frozen_selector_forward_calls=selector_forwards,
        frozen_reader_forward_calls=reader_forwards,
        new_training_steps=0,
        **aggregate_ops,
        **{k:v for k,v in integrated.items() if k != "combinations"},
    )

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

    save_json("stack-plan.json", dict(manifest(), source_blobs=pins, episode_plan=episode_plan()))
    save_json("episode-sets.json", episode_sets)
    save_json("combination-results.json", integrated["combinations"])
    save_json("component-fingerprints.json", dict(
        writer=dict(zip(WRITER_SEEDS, WRITER_FINAL_SHA256, strict=True)),
        coverage=dict(zip(COVERAGE_SEEDS, COVERAGE_FINAL_SHA256, strict=True)),
        selector=dict(zip(SELECTOR_SEEDS, SELECTOR_FINAL_SHA256, strict=True)),
        reader=dict(zip(READER_SEEDS, READER_FINAL_SHA256, strict=True)),
    ))
    save_json("validation-summary.json", summary)

    guard()
    precheck(c219_summary, root)
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
        C219_summary_sha256=PARENT_C219_SHA,
        source_blobs=pins,
        input_sha256=protected,
        artifacts=artifacts,
        validation_summary=summary,
        trained_models=0,
        new_training_steps=0,
        model_forward_calls=writer_forwards + coverage_forwards + selector_forwards + reader_forwards,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        operation_kind_learned=False,
        joint_training=False,
        limitations=[
            "all learned memory components are frozen; no joint adaptation",
            "operation kind remains oracle",
            "structured synthetic descriptors, not natural language",
            "RETRACT/ASSUME integration and information acquisition are not tested",
            "no total-memory-cost comparison and no Gate F claim",
        ],
    )
    validate_result(result)
    (out / "summary.json").write_bytes(blob(result))
    print(
        "[C220] frozen learned stack "
        f"combos={summary['checkpoint_combinations']} "
        f"decisions={summary['decision_rows']} "
        f"integration={summary['integration_accuracy']:.3f}",
        flush=True,
    )
    print("=== C220 RESULT ===", flush=True)
    print(blob(result).decode(), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--c219-summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expected-head", required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
