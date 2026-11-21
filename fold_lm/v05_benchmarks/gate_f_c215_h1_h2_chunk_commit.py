"""C215: deterministic V5-F H1 hot-memory / H2 capsule-bank chunk commit.

Scientific question: can the accepted C214 semantic/numeric memory path preserve readouts and
capability status across representation-only chunk commits, post-commit edits, and scope changes
without replaying hidden operation history?

No learned Writer/Reader/Port Selector/Coverage classifier, language parsing, or model inference.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest

import torch

from fold_lm.v05 import memory_bank as bankmod
from fold_lm.v05 import memory_bridge as memory
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_f_c214_memory_capsule_closure as c214

EXPERIMENT_ID = "C215-v5f-h1-h2-chunk-commit"
STAGE = "V5-F-H1-H2-CHUNK-COMMIT"
BASE = "17a56efba78dffa02feab107bec66d2bdcda80c0"
PARENT_C214_EXECUTION = "b4a020aeb006ec758e06ce1dc6d1b0ad5784e150"
PARENT_C214_SHA = "bd7a310fc89873b4571d1748a96fa1a121d147a0617d48e2d8824d4769deb37d"
PARENT_C214_VALIDATION_SHA = "974546ca0e93bd0b936a68cdfcc9068bbdf6d8a53be9c7f2e8c6edafc50b543f"
MANIFEST_SHA = "90327cc0691bc80d7faf78f77e36a501f178ac9f861b0524f6e174be3635f9bf"
TOLERANCE = 1e-10
OWN = (
    "fold_lm/v05/memory_bank.py",
    "fold_lm/v05_benchmarks/gate_f_c215_h1_h2_chunk_commit.py",
    "tests_lm/test_v05_c215_h1_h2_chunk_commit.py",
    "tools/run_c215.ps1",
    "tools/invoke_c215.ps1",
    "docs/experiment-ledger-addendum-c215-preregistration.md",
    "docs/v5f-h1-h2-chunk-commit-v0.1.md",
)
OUTPUTS = {
    "bank-plan.json",
    "state-trace.json",
    "snapshot-comparisons.json",
    "commit-controls.json",
    "validation-summary.json",
}


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
        parent_c214_execution=PARENT_C214_EXECUTION,
        parent_c214_sha256=PARENT_C214_SHA,
        parent_c214_validation_sha256=PARENT_C214_VALIDATION_SHA,
        memory_bank_schema=bankmod.SCHEMA,
        snapshots=9,
        commit_count=2,
        expected_storage_epoch=2,
        expected_final_memory_revision=6,
        expected_final_evidence_revision=4,
        expected_final_evidence_time=3,
        expected_status_sequence=[
            "SUPPORTED","HOT_REQUIRED","SUPPORTED","SUPPORTED","HOT_REQUIRED",
            "SUPPORTED","SUPPORTED","SUPPORTED","SUPPORTED",
        ],
        expected_hot_observed_counts=[0,1,0,0,1,0,0,0,0],
        expected_h2_factor_counts=[0,0,1,1,1,2,1,1,1],
        expected_total_observed_counts=[0,1,1,1,2,2,1,1,1],
        commit_readout_delta=0.0,
        max_abs_error_tolerance=TOLERANCE,
        out_of_scope_commit_control=True,
        numeric_unsafe_commit_control=True,
        operation_history_entries=0,
        learned_writer=False,
        learned_reader=False,
        port_selector=False,
        coverage_classifier=False,
        model_forward_calls=0,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        scope=(
            "deterministic H1 hot-memory / H2 capsule-bank chunk commit and capability-status "
            "semantics only; no learned memory routing"
        ),
    )


def build_bank():
    return bankmod.ChunkedMemoryBank(c214.build_bridge())


def _op(kind,revision,scope,*,factor=None,relation=None,source=None,evidence_time=None):
    return memory.MemoryOp(
        kind=kind,
        expected_memory_revision=revision,
        scope_id=scope,
        factor_id=factor,
        relation_key=relation,
        source_id=source,
        evidence_time=evidence_time,
    )


def _value(read):
    return None if read.value is None else [float(x) for x in read.value.tolist()]


def collect_fixture():
    bank=build_bank()
    state=bank.initial_state()
    trace=[]
    snapshots=[]
    commits=[]

    def snapshot(label):
        read=bank.read(state)
        full=bank.full_reference(state)
        error=None
        if read.status in (bankmod.BankReadStatus.SUPPORTED,bankmod.BankReadStatus.HOT_REQUIRED):
            require(full.status==read.status,"bank/full status mismatch")
            error=float(torch.max(torch.abs(read.value-full.value)).item())
        snapshots.append(dict(
            label=label,
            status=read.status.value,
            full_status=full.status.value,
            value=_value(read),
            full_value=_value(full),
            max_abs_error=error,
            memory_revision=state.memory_revision,
            evidence_revision=state.evidence_revision,
            evidence_time=state.evidence_time,
            storage_epoch=state.h2.storage_epoch,
            h2_reflected_evidence_revision=state.h2.reflected_evidence_revision,
            h2_factor_ids=list(read.h2_factor_ids),
            hot_observed_factor_ids=list(read.hot_observed_factor_ids),
            hot_hypothesis_factor_ids=list(read.hot_hypothesis_factor_ids),
            total_observed_factors=len(read.h2_factor_ids)+len(read.hot_observed_factor_ids),
        ))
        return read

    def mutate(label,op):
        nonlocal state
        before=state
        state,result=bank.apply(state,op)
        require(result is None,"mutation unexpectedly returned MemoryRead")
        trace.append(dict(
            label=label,
            kind=op.kind.value,
            before_memory_revision=before.memory_revision,
            after_memory_revision=state.memory_revision,
            before_evidence_revision=before.evidence_revision,
            after_evidence_revision=state.evidence_revision,
            before_storage_epoch=before.h2.storage_epoch,
            after_storage_epoch=state.h2.storage_epoch,
        ))

    def commit(label):
        nonlocal state
        before=state
        before_read=bank.read(before)
        state,status=bank.commit(before)
        after_read=bank.read(state)
        delta=None
        if (
            before_read.value is not None and after_read.value is not None
            and before_read.status in (bankmod.BankReadStatus.SUPPORTED,bankmod.BankReadStatus.HOT_REQUIRED)
            and after_read.status in (bankmod.BankReadStatus.SUPPORTED,bankmod.BankReadStatus.HOT_REQUIRED)
        ):
            delta=float(torch.max(torch.abs(before_read.value-after_read.value)).item())
        commits.append(dict(
            label=label,
            status=status.value,
            semantic_clocks_unchanged=(
                before.memory_revision==state.memory_revision
                and before.evidence_revision==state.evidence_revision
                and before.evidence_time==state.evidence_time
            ),
            before_storage_epoch=before.h2.storage_epoch,
            after_storage_epoch=state.h2.storage_epoch,
            readout_delta=delta,
        ))

    snapshot("initial")
    mutate("assert_alpha",_op(
        memory.MemoryOpKind.ASSERT,0,memory.GLOBAL_SCOPE,
        factor="alpha",relation="rel-alpha-v1",source="user:1",evidence_time=1,
    ))
    snapshot("after_assert_alpha")
    commit("commit_alpha")
    snapshot("after_commit_alpha")

    mutate("replace_alpha",_op(
        memory.MemoryOpKind.REPLACE,1,memory.GLOBAL_SCOPE,
        factor="alpha",relation="rel-alpha-v2",source="user:2",evidence_time=2,
    ))
    snapshot("after_replace_alpha")

    mutate("assert_beta",_op(
        memory.MemoryOpKind.ASSERT,2,"project",
        factor="beta",relation="rel-beta-v1",source="doc:1",evidence_time=2,
    ))
    snapshot("after_assert_beta")
    commit("commit_beta")
    snapshot("after_commit_beta")

    mutate("retract_alpha",_op(
        memory.MemoryOpKind.RETRACT,3,memory.GLOBAL_SCOPE,
        factor="alpha",source="user:3",evidence_time=3,
    ))
    snapshot("after_retract_alpha")

    mutate("assume_temp",_op(
        memory.MemoryOpKind.ASSUME,4,"sandbox",
        factor="temp",relation="rel-hypothesis-unmapped",
    ))
    snapshot("after_assume_temp")

    mutate("end_sandbox",_op(
        memory.MemoryOpKind.END_SCOPE,5,"sandbox",
    ))
    snapshot("after_end_sandbox")

    # Commit control: no H1 observed delta.
    noop_before=bank.initial_state()
    noop_after,noop_status=bank.commit(noop_before)

    # Capability control: unknown observed relation remains H1 and commit is rejected.
    oos=bank.initial_state()
    oos,_=bank.apply(oos,_op(
        memory.MemoryOpKind.ASSERT,0,memory.GLOBAL_SCOPE,
        factor="unknown",relation="rel-out-of-scope",source="external:oos",evidence_time=1,
    ))
    oos_read=bank.read(oos)
    oos_after,oos_commit=bank.commit(oos)

    # Numeric safety control: mapped but SPD-destroying update remains H1 and commit is rejected.
    unsafe=bank.initial_state()
    unsafe,_=bank.apply(unsafe,_op(
        memory.MemoryOpKind.ASSERT,0,memory.GLOBAL_SCOPE,
        factor="unsafe",relation="rel-unsafe",source="external:unsafe",evidence_time=1,
    ))
    unsafe_read=bank.read(unsafe)
    unsafe_after,unsafe_commit=bank.commit(unsafe)

    final_export=memory.export_observed(bank.to_memory_state(state))
    errors=[x["max_abs_error"] for x in snapshots if x["max_abs_error"] is not None]
    controls=dict(
        noop=dict(
            status=noop_status.value,
            semantic_same=noop_after is noop_before,
            storage_epoch=noop_after.h2.storage_epoch,
        ),
        out_of_scope=dict(
            read_status=oos_read.status.value,
            commit_status=oos_commit.value,
            state_identity_preserved=oos_after is oos,
            storage_epoch=oos_after.h2.storage_epoch,
            value_exposed=oos_read.value is not None,
        ),
        numeric_unsafe=dict(
            read_status=unsafe_read.status.value,
            commit_status=unsafe_commit.value,
            state_identity_preserved=unsafe_after is unsafe,
            storage_epoch=unsafe_after.h2.storage_epoch,
            value_exposed=unsafe_read.value is not None,
        ),
    )
    summary=dict(
        snapshots=len(snapshots),
        status_sequence=[x["status"] for x in snapshots],
        status_counts=dict(Counter(x["status"] for x in snapshots)),
        full_statuses_match=all(x["status"]==x["full_status"] for x in snapshots),
        max_abs_error=max(errors),
        tolerance=TOLERANCE,
        hot_observed_counts=[len(x["hot_observed_factor_ids"]) for x in snapshots],
        h2_factor_counts=[len(x["h2_factor_ids"]) for x in snapshots],
        total_observed_counts=[x["total_observed_factors"] for x in snapshots],
        commit_count=len(commits),
        commit_statuses=[x["status"] for x in commits],
        commit_semantic_clocks_unchanged=all(x["semantic_clocks_unchanged"] for x in commits),
        commit_readout_deltas=[x["readout_delta"] for x in commits],
        final_storage_epoch=state.h2.storage_epoch,
        final_h2_reflected_evidence_revision=state.h2.reflected_evidence_revision,
        final_memory_revision=state.memory_revision,
        final_evidence_revision=state.evidence_revision,
        final_evidence_time=state.evidence_time,
        final_h2_factor_ids=[x.factor_id for x in state.h2.factors],
        final_hot_records=len(state.hot_records),
        final_export_factor_ids=[x.factor_id for x in final_export.bindings],
        operation_history_entries=bank.operation_history_entries(state),
        noop_commit_status=controls["noop"]["status"],
        out_of_scope_read_status=controls["out_of_scope"]["read_status"],
        out_of_scope_commit_status=controls["out_of_scope"]["commit_status"],
        out_of_scope_commit_preserved=controls["out_of_scope"]["state_identity_preserved"],
        numeric_unsafe_read_status=controls["numeric_unsafe"]["read_status"],
        numeric_unsafe_commit_status=controls["numeric_unsafe"]["commit_status"],
        numeric_unsafe_commit_preserved=controls["numeric_unsafe"]["state_identity_preserved"],
        non_supported_value_exposures=int(
            controls["out_of_scope"]["value_exposed"] or controls["numeric_unsafe"]["value_exposed"]
        ),
        learned_writer_calls=0,
        learned_reader_calls=0,
        port_selector_calls=0,
        coverage_classifier_calls=0,
        model_forward_calls=0,
    )
    return state,trace,snapshots,commits,controls,summary


def gate(summary):
    return (
        summary.get("snapshots")==9
        and summary.get("status_sequence")==[
            "SUPPORTED","HOT_REQUIRED","SUPPORTED","SUPPORTED","HOT_REQUIRED",
            "SUPPORTED","SUPPORTED","SUPPORTED","SUPPORTED",
        ]
        and summary.get("status_counts")=={"SUPPORTED":7,"HOT_REQUIRED":2}
        and summary.get("full_statuses_match") is True
        and summary.get("max_abs_error") is not None
        and summary.get("max_abs_error")<=TOLERANCE
        and summary.get("hot_observed_counts")==[0,1,0,0,1,0,0,0,0]
        and summary.get("h2_factor_counts")==[0,0,1,1,1,2,1,1,1]
        and summary.get("total_observed_counts")==[0,1,1,1,2,2,1,1,1]
        and summary.get("commit_count")==2
        and summary.get("commit_statuses")==["COMMITTED","COMMITTED"]
        and summary.get("commit_semantic_clocks_unchanged") is True
        and summary.get("commit_readout_deltas")==[0.0,0.0]
        and summary.get("final_storage_epoch")==2
        and summary.get("final_h2_reflected_evidence_revision")==4
        and summary.get("final_memory_revision")==6
        and summary.get("final_evidence_revision")==4
        and summary.get("final_evidence_time")==3
        and summary.get("final_h2_factor_ids")==["beta"]
        and summary.get("final_hot_records")==0
        and summary.get("final_export_factor_ids")==["beta"]
        and summary.get("operation_history_entries")==0
        and summary.get("noop_commit_status")=="NOOP"
        and summary.get("out_of_scope_read_status")=="OUT_OF_SCOPE"
        and summary.get("out_of_scope_commit_status")=="OUT_OF_SCOPE"
        and summary.get("out_of_scope_commit_preserved") is True
        and summary.get("numeric_unsafe_read_status")=="NUMERIC_UNSAFE"
        and summary.get("numeric_unsafe_commit_status")=="NUMERIC_UNSAFE"
        and summary.get("numeric_unsafe_commit_preserved") is True
        and summary.get("non_supported_value_exposures")==0
        and summary.get("learned_writer_calls")==0
        and summary.get("learned_reader_calls")==0
        and summary.get("port_selector_calls")==0
        and summary.get("coverage_classifier_calls")==0
        and summary.get("model_forward_calls")==0
    )


def precheck(
    c214_summary,c213_summary,c212_summary,c211_summary,c210_summary,c209_summary,
    c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,
    c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,
    c188_summary,root
):
    root=Path(root)
    p213,pins,protected=c214.precheck(
        c213_summary,c212_summary,c211_summary,c210_summary,c209_summary,c208_summary,
        c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,
        c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
    )
    require(audit.sha(c214_summary)==PARENT_C214_SHA,"C214 summary changed")
    p214=audit.read_json(c214_summary)
    c214.validate_result(p214)
    require(
        p214.get("commit_sha")==PARENT_C214_EXECUTION
        and p214.get("status")=="PASS"
        and c214.gate(p214["validation_summary"])
        and p214.get("source_blobs")==pins,
        "Wrong accepted C214 parent",
    )
    protected[str(Path(c214_summary).resolve())]=PARENT_C214_SHA
    validation_seen=False
    for artifact in p214["artifacts"]:
        path=audit.safe_child(Path(c214_summary).resolve().parent,artifact["file"])
        require(
            path.is_file() and path.stat().st_size==artifact["serialized_bytes"]
            and audit.sha(path)==artifact["sha256"],
            "Changed C214 artifact:"+artifact["file"],
        )
        if artifact["file"]=="validation-summary.json":
            require(artifact["sha256"]==PARENT_C214_VALIDATION_SHA,
                    "C214 validation artifact changed")
            validation_seen=True
        protected[str(path.resolve())]=artifact["sha256"]
    require(validation_seen,"C214 validation artifact missing")

    pins=dict(pins)
    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    pins.update({name:allpins[name] for name in OWN})

    require(len(pins)==122 and len(protected)==230,"C215 source/protection count drift")
    require(digest(manifest())==MANIFEST_SHA,"C215 manifest drift")
    return p214,pins,protected


def regression_modules(root):
    names=c214.regression_modules(root)
    require(len(names)==len(set(names))==99,"Historical regression module drift")
    return names+["tests_lm.test_v05_c215_h1_h2_chunk_commit"]


def regression_suite(root):
    names=regression_modules(root)
    loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
    tests=list(c205._iter_tests(loaded))
    ids=[test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded)==1,"Historical dynamic test identity drift:"+excluded)
    kept=[test for test in tests if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS]
    require(
        len(tests)==2150 and len(kept)==2149
        and not any(test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS for test in kept),
        "C215 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"]==EXPERIMENT_ID
        and payload["stage"]==STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C215",
    )
    require(
        len(payload["source_blobs"])==122
        and len(payload["input_sha256"])==230
        and len(payload["artifacts"])==5
        and {a["file"] for a in payload["artifacts"]}==OUTPUTS,
        "C215 coverage drift",
    )
    require(
        payload["model_forward_calls"]==0
        and payload["training_steps"]==0
        and payload["fresh_seed_count"]==0
        and payload["network_calls"]==0
        and payload["production_runtime_modified"] is True
        and payload["gate_f_candidate"] is False
        and payload["learned_writer"] is False
        and payload["learned_reader"] is False
        and payload["port_selector"] is False
        and payload["coverage_classifier"] is False,
        "C215 scope drift",
    )
    require(
        payload["status"]==("PASS" if gate(payload["validation_summary"]) else "FAIL"),
        "C215 gate drift",
    )


def run(
    *,c214_summary,c213_summary,c212_summary,c211_summary,c210_summary,c209_summary,
    c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,
    c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,
    c188_summary,output_dir,expected_head
):
    root=Path(__file__).resolve().parents[2]

    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(audit.git(root,"branch","--show-current").decode().strip()
                =="feat/sft-target-loss","Branch mismatch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),
                "Dirty tracked tree")

    guard()
    _,pins,protected=precheck(
        c214_summary,c213_summary,c212_summary,c211_summary,c210_summary,c209_summary,
        c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,
        c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,
        c188_summary,root
    )

    state,trace,snapshots,commits,controls,summary=collect_fixture()
    out=Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    artifacts=[]

    def record(name):
        path=out/name
        artifacts.append(dict(file=name,sha256=audit.sha(path),serialized_bytes=path.stat().st_size))

    def save(name,value):
        (out/name).write_bytes(blob(value));record(name)

    save("bank-plan.json",dict(manifest(),source_blobs=pins))
    save("state-trace.json",trace)
    save("snapshot-comparisons.json",snapshots)
    save("commit-controls.json",dict(commits=commits,controls=controls))
    save("validation-summary.json",summary)

    guard()
    precheck(
        c214_summary,c213_summary,c212_summary,c211_summary,c210_summary,c209_summary,
        c208_summary,c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,
        c202_summary,c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,
        c188_summary,root
    )
    for path,wanted in protected.items():
        require(audit.sha(path)==wanted,"Protected input changed:"+path)
    for artifact in artifacts:
        require(audit.sha(out/artifact["file"])==artifact["sha256"],"Output changed:"+artifact["file"])

    result=dict(
        experiment_id=EXPERIMENT_ID,
        stage=STAGE,
        commit_sha=expected_head,
        status="PASS" if gate(summary) else "FAIL",
        diagnostic_execution_valid=True,
        C214_summary_sha256=PARENT_C214_SHA,
        source_blobs=pins,
        input_sha256=protected,
        artifacts=artifacts,
        validation_summary=summary,
        memory_bank_schema=bankmod.SCHEMA,
        model_forward_calls=0,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        learned_writer=False,
        learned_reader=False,
        port_selector=False,
        coverage_classifier=False,
        limitations=[
            "deterministic H1/H2 reference only; no learned routing",
            "H2 stores current protected-factor descriptors plus aggregate numeric update, not operation history",
            "fixed relation-to-port registry inherited from C214",
            "PASS establishes chunk-commit/capability semantics only, not Gate F",
        ],
    )
    validate_result(result)
    (out/"summary.json").write_bytes(blob(result))
    print(
        f"[C215] H1/H2 snapshots={summary['snapshots']} storage_epoch={summary['final_storage_epoch']} "
        f"max_abs_error={summary['max_abs_error']:.3e}",
        flush=True,
    )
    print("=== C215 RESULT ===",flush=True)
    print(blob(result).decode(),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in (
        "c214-summary","c213-summary","c212-summary","c211-summary","c210-summary",
        "c209-summary","c208-summary","c207-summary","c206-summary","c205-summary",
        "c204-summary","c203-summary","c202-summary","c201-summary","c200-summary",
        "c199-summary","c174-summary","c181-summary","c188-summary","output-dir",
    ):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
