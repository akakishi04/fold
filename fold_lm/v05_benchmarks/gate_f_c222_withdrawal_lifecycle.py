"""C222: withdrawal/hypothesis isolation in the frozen live memory stack. No training."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import itertools
import json
from pathlib import Path
import unittest

import torch

EXPERIMENT_ID = "C222-v5f-withdrawal-hypothesis-lifecycle"
STAGE = "V5-F-WITHDRAWAL-HYPOTHESIS-LIFECYCLE"
BASE = "ccb655b8649c4f2bb20faf5f7753d3c14b8ef103"
PARENT_EXECUTION = "ed82010bede050c0209be8b540d83cc544fa6bd4"
PARENT_SHA = "70cee94a95b20d538d86a041a3518151f019e03d15594132720c041224859766"
PARENT_VALIDATION_SHA = "c3ed8f149357c27281122b3cab9876b371d8da25a57dd536fa4e1b32f0a7ab0c"
MANIFEST_SHA = "1b94c0af7c1d828f54c5519dd9169a9e2a7985ddd91b155a72d312d39e26a828"
# label, beta Coverage, beta answer, symbolic beta read, memory/evidence/time/epoch
PLAN = (
    ("anchor_only", 2, None, "MISSING", (1,1,1,1)),
    ("beta_hot", 1, 2, "SUPPORTED", (2,2,2,1)),
    ("beta_committed", 0, 2, "SUPPORTED", (2,2,2,2)),
    ("beta_replaced", 0, 0, "SUPPORTED", (3,3,3,2)),
    ("beta_retracted", 2, None, "RETRACTED", (4,4,4,2)),
    ("shadow_assumed", 2, None, "RETRACTED", (5,4,4,2)),
    ("shadow_ended", 2, None, "RETRACTED", (6,4,4,2)),
    ("project_ended", 3, None, "OUT_OF_SCOPE", (7,4,4,2)),
)
CONTROL_LABELS = ("beta_retracted", "shadow_assumed")
SEED_FAMILIES = ((218001,218002,218003), (219001,219002,219003),
                 (217001,217002,217003), (216001,216002,216003))
OWN = (
    "fold_lm/v05_benchmarks/gate_f_c222_withdrawal_lifecycle.py",
    "tests_lm/test_v05_c222_withdrawal_lifecycle.py",
    "tools/run_c222.ps1", "tools/invoke_c222.ps1",
    "docs/experiment-ledger-addendum-c222-preregistration.md",
    "docs/v5f-withdrawal-hypothesis-lifecycle-v0.1.md",
)
OUTPUTS = {"lifecycle-plan.json", "timeline-audit.json", "live-decisions.json",
           "forced-allow-decisions.json", "validation-summary.json"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import gate_f_c221_live_coverage_dispatch as parent
    return parent


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
                parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
                parent_validation_sha256=PARENT_VALIDATION_SHA,
                plan=[[label,cov,answer,status,list(clocks)] for label,cov,answer,status,clocks in PLAN],
                seed_families=[list(x) for x in SEED_FAMILIES], control_labels=list(CONTROL_LABELS),
                hypothesis_scope="sandbox", hypothesis_factor="beta", hypothesis_relation="beta-class-2",
                anchor_relation="alpha-class-1", anchor_answer=1, trajectories=3,
                snapshots_per_trajectory=8, queries_per_snapshot=2, combinations=81,
                main_decisions=1296, readable_decisions=891, suppressed_decisions=405,
                control_decisions=162, diagnostic_snapshots=24,
                successful_main_calls=dict(coverage=1296,selector=891,provider=891,reader=891,bank_reads=891),
                successful_control_calls=dict(coverage=162,selector=162,provider=162,reader=0,bank_reads=0),
                writer_forwards=3, successful_model_forwards=3405,
                operation_kind="oracle ASSERT/COMMIT/REPLACE/RETRACT/ASSUME/END_SCOPE",
                checkpoints_frozen=True, new_training_steps=0, production_runtime_modified=False,
                old_request_reuse_tested=False, total_memory_cost_measured=False,
                gate_f_candidate=False, device="cpu", threads=2, deterministic_algorithms=True)


def timeline(base, prediction, writer_seed):
    """One bank/state chain per Writer: no reinitialization between snapshots."""
    bank = base.c216.build_bank()
    m = base.memory
    state = bank.initial_state()
    prefix = f"c222:{writer_seed}"
    def apply(kind, scope, factor=None, relation=None, observed_time=None):
        nonlocal state
        op = m.MemoryOp(kind, state.memory_revision, scope, factor_id=factor,
                        relation_key=relation,
                        source_id=prefix if observed_time is not None else None,
                        evidence_time=observed_time)
        state, read = bank.apply(state, op)
        require(read is None, "mutation unexpectedly returned read")
    def learned(kind, target, time):
        nonlocal state
        state, read = bank.apply(state, base.c218.memory_op(kind,state,prediction[target],time,prefix))
        require(read is None, "learned mutation returned read")
    def commit():
        nonlocal state
        state, status = bank.commit(state)
        require(status.value == "COMMITTED", "registered commit did not execute")
    learned(m.MemoryOpKind.ASSERT,1,1)
    commit()
    yield "anchor_only",bank,state
    learned(m.MemoryOpKind.ASSERT,5,2)
    yield "beta_hot",bank,state
    commit()
    yield "beta_committed",bank,state
    learned(m.MemoryOpKind.REPLACE,3,3)
    yield "beta_replaced",bank,state
    apply(m.MemoryOpKind.RETRACT,"project","beta",observed_time=4)
    yield "beta_retracted",bank,state
    apply(m.MemoryOpKind.ASSUME,"sandbox","beta","beta-class-2")
    yield "shadow_assumed",bank,state
    apply(m.MemoryOpKind.END_SCOPE,"sandbox")
    yield "shadow_ended",bank,state
    apply(m.MemoryOpKind.END_SCOPE,"project")
    yield "project_ended",bank,state


def snapshot_audit(base, label, bank, state):
    """Scorer-only symbolic/export diagnostics; never supplied to the neural dispatcher."""
    m = base.memory
    semantic = bank.to_memory_state(state)
    def query(scope,factor):
        _, r = m.apply_memory_op(semantic,m.MemoryOp(m.MemoryOpKind.QUERY,
                               semantic.memory_revision,scope,factor_id=factor))
        return dict(status=r.status.value,relation=r.relation_key,
                    provenance=None if r.provenance is None else r.provenance.kind.value)
    exported = m.export_observed(semantic)
    return dict(label=label,
                clocks=[state.memory_revision,state.evidence_revision,state.evidence_time,state.h2.storage_epoch],
                beta=query("project","beta"), anchor=query("global","alpha"),
                shadow=query("sandbox","beta"),
                bindings=[[r.scope_id,r.factor_id,r.relation_key] for r in exported.bindings],
                export_provenance=[r.provenance.kind.value for r in exported.evidence.observations],
                h2_W=state.h2.W.tolist(),h2_b=state.h2.b.tolist())


def audit_ok(rows):
    if len(rows) != 8 or [r["label"] for r in rows] != [p[0] for p in PLAN]:
        return False
    for index,(row,(_,_,_,status,clocks)) in enumerate(zip(rows,PLAN,strict=True)):
        if row["clocks"] != list(clocks) or row["beta"]["status"] != status:
            return False
        if row["anchor"] != dict(status="SUPPORTED",relation="alpha-class-1",provenance="observed"):
            return False
        expected = [["global","alpha","alpha-class-1"]]
        if index in (1,2,3):
            relation = "beta-class-0" if index == 3 else "beta-class-2"
            expected.append(["project","beta",relation])
            if row["beta"] != dict(status="SUPPORTED",relation=relation,provenance="observed"):
                return False
        elif row["beta"]["relation"] is not None or row["beta"]["provenance"] is not None:
            return False
        if row["bindings"] != expected or row["export_provenance"] != ["observed"]*len(expected):
            return False
        shadow = dict(status="MISSING",relation=None,provenance=None)
        if index == 5:
            shadow = dict(status="SUPPORTED",relation="beta-class-2",provenance="hypothesis")
        if index >= 6:
            shadow = dict(status="OUT_OF_SCOPE",relation=None,provenance=None)
        if row["shadow"] != shadow:
            return False
    # These equality checks are diagnostics of hypothesis isolation, not query-read calls.
    return all(rows[i][k] == rows[4][k] for i in (5,6,7) for k in ("h2_W","h2_b"))


def score_decision(result, expected_cov, expected_answer):
    action = "ANSWER" if expected_answer is not None else (
        "SUPPRESS_OUT_OF_SCOPE" if expected_cov == 3 else "SUPPRESS_MISSING")
    trace = ("coverage","selector","provider","reader") if expected_answer is not None else ("coverage",)
    return (result.coverage == expected_cov and result.answer == expected_answer
            and result.action == action and result.trace == trace
            and result.bank_reads == (1 if expected_answer is not None else 0))


def evaluate(parent, models, snapshots):
    base = parent.parent_module()
    main,controls = [],[]
    for seeds in itertools.product(*SEED_FAMILIES):
        ws,cs,ss,rs = seeds
        context = dict(zip(("writer_seed","coverage_seed","selector_seed","reader_seed"),seeds,strict=True))
        for (label,bank,state), registered in zip(snapshots[ws],PLAN,strict=True):
            require(label == registered[0], "timeline label drift")
            for query in ("alpha","beta"):
                # Fresh request binds current state; historical request closures are not reused.
                request = parent.request_for(base,bank,state,query)
                result = parent.live.dispatch_query(request,models["coverage"][cs],
                                                   models["selector"][ss],models["reader"][rs])
                cov,answer = (0,1) if query == "alpha" else registered[1:3]
                main.append(dict(context,label=label,query=query,
                                 success=score_decision(result,cov,answer),**asdict(result)))
            if label in CONTROL_LABELS:
                request = parent.request_for(base,bank,state,"beta")
                forced = parent.ForcedCoverage(models["coverage"][cs],0)
                result = parent.live.dispatch_query(request,forced,models["selector"][ss],models["reader"][rs])
                ok = (result.coverage == 0 and result.action == "BLOCKED_MISSING"
                      and result.answer is None and result.bank_reads == 0
                      and result.trace == ("coverage","selector","provider"))
                controls.append(dict(context,label=label,query="beta",original_coverage=forced.original,
                                     success=bool(ok),**asdict(result)))
    return main,controls


def summarize(parent, main, controls, audits, writer_accuracy, unchanged):
    suppressed_labels = {p[0] for p in PLAN if p[2] is None}
    suppressed = [r for r in main if r["query"] == "beta" and r["label"] in suppressed_labels]
    mc,cc = parent.calls(main),parent.calls(controls)
    return dict(main_decisions=len(main),main_success=sum(r["success"] for r in main),
                control_decisions=len(controls),control_success=sum(r["success"] for r in controls),
                suppressed_success=sum(r["success"] for r in suppressed),
                suppressed_downstream_calls=sum(len(r["trace"])-1 for r in suppressed),
                post_retract_beta_answers=sum(r["answer"] is not None for r in main
                    if r["query"] == "beta" and r["label"] in {p[0] for p in PLAN[4:]}),
                anchor_success=sum(r["success"] for r in main if r["query"] == "alpha"),
                lifecycle_audits_passed=sum(audit_ok(rows) for rows in audits.values()),
                main_calls=mc,control_calls=cc,writer_target_accuracy=writer_accuracy,
                fingerprints_unchanged=unchanged,new_training_steps=0,
                model_forward_calls=3+sum(mc[k]+cc[k] for k in ("coverage","selector","reader")))


def gate(s):
    return (s.get("main_decisions") == s.get("main_success") == 1296
            and s.get("control_decisions") == s.get("control_success") == 162
            and s.get("suppressed_success") == 405 and s.get("anchor_success") == 648
            and s.get("suppressed_downstream_calls") == 0 and s.get("post_retract_beta_answers") == 0
            and s.get("lifecycle_audits_passed") == 3
            and s.get("main_calls") == manifest()["successful_main_calls"]
            and s.get("control_calls") == manifest()["successful_control_calls"]
            and s.get("writer_target_accuracy") == 1.0 and s.get("fingerprints_unchanged") is True
            and s.get("model_forward_calls") == 3405 and s.get("new_training_steps") == 0)


def precheck(c221_summary, root):
    parent = parent_module()
    a = parent.parent_module().audit
    root = Path(root)
    require(a.sha(c221_summary) == PARENT_SHA, "C221 summary changed")
    p = a.read_json(c221_summary)
    parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS"
            and parent.gate(p["validation_summary"]), "wrong accepted C221")
    require(len(p["source_blobs"]) == 165 and len(p["input_sha256"]) == 195, "parent coverage")
    pins,protected = dict(p["source_blobs"]),dict(p["input_sha256"])
    for path,wanted in protected.items():
        require(Path(path).is_file() and a.sha(path) == wanted, "inherited input changed:"+path)
    for path,wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+path).decode().strip() == wanted,"parent source changed:"+path)
    protected[str(Path(c221_summary).resolve())] = PARENT_SHA
    validation_seen = False
    for artifact in p["artifacts"]:
        path = a.safe_child(Path(c221_summary).resolve().parent,artifact["file"])
        require(path.is_file() and a.sha(path) == artifact["sha256"]
                and path.stat().st_size == artifact["serialized_bytes"],"parent artifact changed")
        protected[str(path.resolve())] = artifact["sha256"]
        if artifact["file"] == "validation-summary.json":
            require(artifact["sha256"] == PARENT_VALIDATION_SHA,"parent validation changed")
            validation_seen = True
    require(validation_seen,"parent validation missing")
    for path in OWN:
        require(path not in pins,"OWN collides with accepted source")
        pins[path] = a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    dependencies = tuple(parent.parent_module().DIRECT_REPO_DEPENDENCIES) + (
        "fold_lm/v05_benchmarks/gate_f_c220_frozen_learned_stack.py",
        "fold_lm/v05/memory_dispatch.py",
        "fold_lm/v05_benchmarks/gate_f_c221_live_coverage_dispatch.py")
    require(len(dependencies) == 17 and all(x in pins for x in dependencies),"unpinned dependency")
    protected.update(a.protect_tree_files(root,pins))
    require(len(pins) == 171 and len(protected) == 207,"C222 protection counts")
    require(digest(manifest()) == MANIFEST_SHA,"C222 manifest drift")
    return p,pins,protected


def regression_modules(root):
    names = parent_module().regression_modules(root)
    require(len(names) == len(set(names)) == 106,"parent module count")
    return names+["tests_lm.test_v05_c222_withdrawal_lifecycle"]


def regression_suite(root):
    parent = parent_module()
    helper = parent.parent_module().c205
    tests = list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    excluded = helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
    ids = [t.id() for t in tests]
    require(all(ids.count(x) == 1 for x in excluded),"historical exclusion identity")
    kept = [t for t in tests if t.id() not in excluded]
    require(len(tests) == 2402 and len(kept) == 2401,"C222 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE
            and p["diagnostic_execution_valid"] is True,"C222 result identity")
    require(len(p["source_blobs"]) == 171 and len(p["input_sha256"]) == 207
            and len(p["artifacts"]) == 5 and {a["file"] for a in p["artifacts"]} == OUTPUTS,"output coverage")
    s = p["validation_summary"]
    require(s["main_decisions"] == 1296 and s["control_decisions"] == 162
            and s["new_training_steps"] == 0,"incomplete C222")
    require(p["status"] == ("PASS" if gate(s) else "FAIL"),"C222 verdict drift")
    require(p["gate_f_candidate"] is False and p["network_calls"] == 0
            and p["production_runtime_modified"] is False,"scope drift")


def run(*, c221_summary, output_dir, expected_head):
    parent = parent_module()
    base = parent.parent_module()
    a = base.audit
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip() == expected_head,"HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard()
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    p,pins,protected = precheck(c221_summary,root)
    coverage_parent = base.find_protected_input(p,"summary.json",base.PARENT_C219_SHA)
    models = dict(writer=base.restore_writer_models(p),coverage=base.restore_coverage_models(p,coverage_parent),
                  selector=base.restore_selector_models(p),reader=base.restore_reader_models(p))
    hashers = dict(writer=base.c218.model_sha,coverage=base.c219.model_sha,
                   selector=base.c217.model_sha,reader=base.c216.model_sha)
    def fingerprints():
        return {family:{str(seed):hashers[family](model) for seed,model in group.items()}
                for family,group in models.items()}
    before = fingerprints()
    predictions,forwards,writer_accuracy = base.frozen_writer_predictions(models["writer"])
    require(forwards == 3,"Writer batch count")
    snapshots = {seed:list(timeline(base,predictions[seed],seed)) for seed in SEED_FAMILIES[0]}
    audits = {seed:[snapshot_audit(base,*row) for row in rows] for seed,rows in snapshots.items()}
    main,controls = evaluate(parent,models,snapshots)
    after = fingerprints()
    summary = summarize(parent,main,controls,audits,writer_accuracy,before == after)
    out = Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    artifacts = []
    for name,value in (
        ("lifecycle-plan.json",manifest()),
        ("timeline-audit.json",dict(trajectories=audits,fingerprints_before=before,fingerprints_after=after)),
        ("live-decisions.json",main),("forced-allow-decisions.json",controls),
        ("validation-summary.json",summary),
    ):
        path = out/name
        path.write_bytes(blob(value))
        artifacts.append(dict(file=name,sha256=a.sha(path),serialized_bytes=path.stat().st_size))
    guard()
    precheck(c221_summary,root)
    for path,wanted in protected.items():
        require(a.sha(path) == wanted,"input modified:"+path)
    result = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
                  status="PASS" if gate(summary) else "FAIL",diagnostic_execution_valid=True,
                  C221_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,
                  artifacts=artifacts,validation_summary=summary,gate_f_candidate=False,network_calls=0,
                  production_runtime_modified=False,
                  limitations=["one synthetic trajectory per frozen Writer, not independent unseen tasks",
                               "requests rebuilt from current state; no retained old-request/cache test",
                               "oracle operation kind and hypothesis construction; no hypothesis-to-answer path",
                               "no new training, acquisition, indexing or total memory-cost comparison"])
    validate_result(result)
    (out/"summary.json").write_bytes(blob(result))
    print("=== C222 RESULT ===",flush=True)
    print(blob(result).decode(),flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("c221-summary","output-dir"):
        parser.add_argument("--"+arg,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
