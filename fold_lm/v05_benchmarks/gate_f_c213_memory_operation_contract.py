"""C213: V5-F memory operation/scope/revision/provenance contract.

This experiment introduces only the deterministic memory semantic bridge. It does not introduce a
learned Writer/Reader, Port Selector, FOLD-R numeric capsule, H1/H2 compiler, language parsing, or
model inference.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import unittest

from fold_lm.v05 import memory_bridge as bridge
from fold_lm.v05 import state as vstate
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_e_c212_deciding_holdout_execution as c212

EXPERIMENT_ID = "C213-v5f-memory-operation-contract"
STAGE = "V5-F-MEMORY-OPERATION-CONTRACT"
BASE = "8825f1e6600f563db5c17f0ac9a336624cd57c4b"
PARENT_C212_EXECUTION = "4d1436c1ba12721b1c802fb5d76e359b3a62841f"
PARENT_C212_SHA = "3685c37dd6e2c7fea92723548446b86f4ee8d068f7dd00afe3e2337f8bca8bce"
PARENT_GATE_E_DECISION_SHA = "41cb9aa4bc092934eff080cc07d16edbb692822526d5d81ae35ed8d7abccab0a"
STATE_BLOB = "aa3f4938f6b5d403d8ee05c4220f686695cef3f0"
MANIFEST_SHA = "daadfa2445e72512553e400373a0a479850bf8d5657713d068f0a164e488cc79"
OWN = (
    "fold_lm/v05/memory_bridge.py",
    "fold_lm/v05_benchmarks/gate_f_c213_memory_operation_contract.py",
    "tests_lm/test_v05_c213_memory_operation_contract.py",
    "tools/run_c213.ps1",
    "tools/invoke_c213.ps1",
    "docs/experiment-ledger-addendum-c213-preregistration.md",
    "docs/v5f-memory-operation-contract-v0.1.md",
)
OUTPUTS = {
    "contract-plan.json",
    "operation-trace.json",
    "read-results.json",
    "evidence-export.json",
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
        parent_c212_execution=PARENT_C212_EXECUTION,
        parent_c212_sha256=PARENT_C212_SHA,
        parent_gate_e_decision_sha256=PARENT_GATE_E_DECISION_SHA,
        memory_bridge_schema=bridge.SCHEMA,
        operation_kinds=[x.value for x in bridge.MemoryOpKind],
        read_statuses=[x.value for x in bridge.MemoryReadStatus],
        fixture_operations=6,
        fixture_reads=8,
        observed_mutations=4,
        hypothesis_memory_mutations=2,
        expected_final_memory_revision=6,
        expected_final_evidence_revision=4,
        expected_final_evidence_time=3,
        learned_writer=False,
        learned_reader=False,
        port_selector=False,
        fold_r_capsule=False,
        h1_h2_compiler=False,
        model_forward_calls=0,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        scope=(
            "memory operation/scope/revision/provenance reference contract only; "
            "no numeric capsule or learned memory policy"
        ),
    )


def _op(kind, revision, scope, *, factor=None, relation=None, source=None, evidence_time=None):
    return bridge.MemoryOp(
        kind=kind,
        expected_memory_revision=revision,
        scope_id=scope,
        factor_id=factor,
        relation_key=relation,
        source_id=source,
        evidence_time=evidence_time,
    )


def _op_json(op):
    row=asdict(op)
    row["kind"]=op.kind.value
    return row


def _read_json(label, read):
    row=asdict(read)
    row["label"]=label
    row["status"]=read.status.value
    if read.provenance is not None:
        row["provenance"]["kind"]=read.provenance.kind.value
    return row


def _export_json(export):
    return dict(
        evidence=asdict(export.evidence),
        bindings=[asdict(x) for x in export.bindings],
    )


def collect_fixture():
    state=bridge.MemoryState()
    trace=[]
    reads=[]

    def mutate(label,op):
        nonlocal state
        before=state
        state,result=bridge.apply_memory_op(state,op)
        require(result is None,"mutation must not return read")
        trace.append(dict(
            label=label,
            op=_op_json(op),
            before=dict(
                memory_revision=before.memory_revision,
                evidence_revision=before.evidence_revision,
                evidence_time=before.evidence_time,
            ),
            after=dict(
                memory_revision=state.memory_revision,
                evidence_revision=state.evidence_revision,
                evidence_time=state.evidence_time,
            ),
        ))

    def query(label,op):
        same,read=bridge.apply_memory_op(state,op)
        require(same is state and read is not None,"QUERY must be non-mutating")
        reads.append(_read_json(label,read))
        return read

    mutate("assert_alpha",_op(
        bridge.MemoryOpKind.ASSERT,0,bridge.GLOBAL_SCOPE,
        factor="alpha",relation="rel-alpha-v1",source="user:1",evidence_time=1,
    ))
    query("alpha_after_assert",_op(
        bridge.MemoryOpKind.QUERY,1,bridge.GLOBAL_SCOPE,factor="alpha",
    ))

    mutate("replace_alpha",_op(
        bridge.MemoryOpKind.REPLACE,1,bridge.GLOBAL_SCOPE,
        factor="alpha",relation="rel-alpha-v2",source="user:2",evidence_time=2,
    ))
    query("alpha_after_replace",_op(
        bridge.MemoryOpKind.QUERY,2,bridge.GLOBAL_SCOPE,factor="alpha",
    ))

    mutate("assert_beta",_op(
        bridge.MemoryOpKind.ASSERT,2,"project",
        factor="beta",relation="rel-beta-v1",source="doc:1",evidence_time=2,
    ))
    query("missing_gamma",_op(
        bridge.MemoryOpKind.QUERY,3,"project",factor="gamma",
    ))

    mutate("retract_alpha",_op(
        bridge.MemoryOpKind.RETRACT,3,bridge.GLOBAL_SCOPE,
        factor="alpha",source="user:3",evidence_time=3,
    ))
    query("alpha_after_retract",_op(
        bridge.MemoryOpKind.QUERY,4,bridge.GLOBAL_SCOPE,factor="alpha",
    ))

    mutate("assume_temp",_op(
        bridge.MemoryOpKind.ASSUME,4,"sandbox",
        factor="temp",relation="rel-temp-hypothesis",
    ))
    assumption=query("assumption_live",_op(
        bridge.MemoryOpKind.QUERY,5,"sandbox",factor="temp",
    ))
    stale=query("stale_query",_op(
        bridge.MemoryOpKind.QUERY,4,"sandbox",factor="temp",
    ))
    export_mid=bridge.export_observed(state)

    stale_mutation_rejected=False
    try:
        bridge.apply_memory_op(state,_op(
            bridge.MemoryOpKind.REPLACE,4,"project",
            factor="beta",relation="rel-beta-stale",source="doc:stale",evidence_time=3,
        ))
    except ValueError as exc:
        stale_mutation_rejected=str(exc)=="STALE_REVISION"

    observed_scope_end_rejected=False
    try:
        bridge.apply_memory_op(state,_op(
            bridge.MemoryOpKind.END_SCOPE,5,"project",
        ))
    except ValueError as exc:
        observed_scope_end_rejected="observed records" in str(exc)

    mutate("end_sandbox",_op(
        bridge.MemoryOpKind.END_SCOPE,5,"sandbox",
    ))
    out_scope=query("ended_scope_query",_op(
        bridge.MemoryOpKind.QUERY,6,"sandbox",factor="temp",
    ))
    query("missing_delta",_op(
        bridge.MemoryOpKind.QUERY,6,"project",factor="delta",
    ))

    ended_scope_mutation_rejected=False
    try:
        bridge.apply_memory_op(state,_op(
            bridge.MemoryOpKind.ASSUME,6,"sandbox",
            factor="later",relation="rel-later",
        ))
    except ValueError as exc:
        ended_scope_mutation_rejected=str(exc)=="OUT_OF_SCOPE"

    export_final=bridge.export_observed(state)

    require(assumption.provenance is not None,"assumption provenance required")
    summary=dict(
        operations=len(trace),
        reads=len(reads),
        observed_mutations=sum(
            x["after"]["evidence_revision"]>x["before"]["evidence_revision"]
            for x in trace
        ),
        hypothesis_memory_mutations=sum(
            x["after"]["memory_revision"]>x["before"]["memory_revision"]
            and x["after"]["evidence_revision"]==x["before"]["evidence_revision"]
            for x in trace
        ),
        read_status_counts=dict(Counter(x["status"] for x in reads)),
        final_memory_revision=state.memory_revision,
        final_evidence_revision=state.evidence_revision,
        final_evidence_time=state.evidence_time,
        live_records=len(state.records),
        tombstones=len(state.tombstones),
        ended_scopes=len(state.ended_scopes),
        mid_export_observations=len(export_mid.evidence.observations),
        final_export_observations=len(export_final.evidence.observations),
        final_export_bindings=len(export_final.bindings),
        hypothesis_exported=int(any(
            ref.provenance.kind is vstate.ProvenanceKind.HYPOTHESIS
            for ref in export_final.evidence.observations
        )),
        assumption_kind=assumption.provenance.kind.value,
        stale_query_status=stale.status.value,
        ended_scope_status=out_scope.status.value,
        stale_mutation_rejected=stale_mutation_rejected,
        observed_scope_end_rejected=observed_scope_end_rejected,
        ended_scope_mutation_rejected=ended_scope_mutation_rejected,
        learned_writer_calls=0,
        learned_reader_calls=0,
        fold_r_capsule_calls=0,
        model_forward_calls=0,
    )
    return state,trace,reads,export_mid,export_final,summary


def gate(summary):
    return (
        summary.get("operations")==6
        and summary.get("reads")==8
        and summary.get("observed_mutations")==4
        and summary.get("hypothesis_memory_mutations")==2
        and summary.get("read_status_counts")=={
            "SUPPORTED":3,
            "MISSING":2,
            "RETRACTED":1,
            "STALE_REVISION":1,
            "OUT_OF_SCOPE":1,
        }
        and summary.get("final_memory_revision")==6
        and summary.get("final_evidence_revision")==4
        and summary.get("final_evidence_time")==3
        and summary.get("live_records")==1
        and summary.get("tombstones")==1
        and summary.get("ended_scopes")==1
        and summary.get("mid_export_observations")==1
        and summary.get("final_export_observations")==1
        and summary.get("final_export_bindings")==1
        and summary.get("hypothesis_exported")==0
        and summary.get("assumption_kind")=="hypothesis"
        and summary.get("stale_query_status")=="STALE_REVISION"
        and summary.get("ended_scope_status")=="OUT_OF_SCOPE"
        and summary.get("stale_mutation_rejected") is True
        and summary.get("observed_scope_end_rejected") is True
        and summary.get("ended_scope_mutation_rejected") is True
        and summary.get("learned_writer_calls")==0
        and summary.get("learned_reader_calls")==0
        and summary.get("fold_r_capsule_calls")==0
        and summary.get("model_forward_calls")==0
    )


def precheck(
    c212_summary,c211_summary,c210_summary,c209_summary,c208_summary,c207_summary,
    c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,
    c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
):
    root=Path(root)
    p211,_,pins,protected=c212.precheck(
        c211_summary,c210_summary,c209_summary,c208_summary,c207_summary,c206_summary,
        c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,c200_summary,
        c199_summary,c174_summary,c181_summary,c188_summary,root
    )
    require(audit.sha(c212_summary)==PARENT_C212_SHA,"C212 summary changed")
    p212=audit.read_json(c212_summary)
    c212.validate_result(p212)
    require(
        p212.get("commit_sha")==PARENT_C212_EXECUTION
        and p212.get("status")=="PASS"
        and p212.get("formal_outcome")=="GATE_E_PASSED"
        and p212.get("gate_e_passed") is True
        and p212.get("source_blobs")==pins
        and p212.get("policy_episode_evaluations")==432,
        "Wrong accepted C212 parent",
    )
    protected[str(Path(c212_summary).resolve())]=PARENT_C212_SHA
    gate_seen=False
    for artifact in p212["artifacts"]:
        path=audit.safe_child(Path(c212_summary).resolve().parent,artifact["file"])
        require(
            path.is_file() and path.stat().st_size==artifact["serialized_bytes"]
            and audit.sha(path)==artifact["sha256"],
            "Changed C212 artifact:"+artifact["file"],
        )
        if artifact["file"]=="gate-e-decision.json":
            require(artifact["sha256"]==PARENT_GATE_E_DECISION_SHA,"Gate E decision changed")
            gate_seen=True
        protected[str(path.resolve())]=artifact["sha256"]
    require(gate_seen,"C212 Gate E decision artifact missing")

    pins=dict(pins)
    current_state=audit.git(root,"rev-parse","HEAD:fold_lm/v05/state.py").decode().strip()
    require(current_state==STATE_BLOB,"V5 state provenance contract changed")
    pins["fold_lm/v05/state.py"]=STATE_BLOB

    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    pins.update({name:allpins[name] for name in OWN})

    require(len(pins)==107 and len(protected)==203,"C213 source/protection count drift")
    require(digest(manifest())==MANIFEST_SHA,"C213 manifest drift")
    return p212,pins,protected


def regression_modules(root):
    names=c212.regression_modules(root)
    require(len(names)==len(set(names))==97,"Historical regression module drift")
    return names+["tests_lm.test_v05_c213_memory_operation_contract"]


def regression_suite(root):
    names=regression_modules(root)
    loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
    tests=list(c205._iter_tests(loaded))
    ids=[test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded)==1,"Historical dynamic test identity drift:"+excluded)
    kept=[test for test in tests if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS]
    require(
        len(tests)==2084 and len(kept)==2083
        and not any(test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS for test in kept),
        "C213 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"]==EXPERIMENT_ID
        and payload["stage"]==STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C213",
    )
    require(
        len(payload["source_blobs"])==107
        and len(payload["input_sha256"])==203
        and len(payload["artifacts"])==5
        and {a["file"] for a in payload["artifacts"]}==OUTPUTS,
        "C213 coverage drift",
    )
    require(
        payload["model_forward_calls"]==0
        and payload["training_steps"]==0
        and payload["fresh_seed_count"]==0
        and payload["network_calls"]==0
        and payload["production_runtime_modified"] is True
        and payload["gate_f_candidate"] is False
        and payload["fold_r_capsule"] is False
        and payload["learned_writer"] is False
        and payload["learned_reader"] is False,
        "C213 scope drift",
    )
    require(
        payload["status"]==("PASS" if gate(payload["validation_summary"]) else "FAIL"),
        "C213 gate drift",
    )


def run(
    *,c212_summary,c211_summary,c210_summary,c209_summary,c208_summary,c207_summary,
    c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,
    c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,output_dir,expected_head
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
        c212_summary,c211_summary,c210_summary,c209_summary,c208_summary,c207_summary,
        c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,
        c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
    )

    state,trace,reads,export_mid,export_final,summary=collect_fixture()
    out=Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    artifacts=[]

    def record(name):
        path=out/name
        artifacts.append(dict(file=name,sha256=audit.sha(path),serialized_bytes=path.stat().st_size))

    def save(name,value):
        (out/name).write_bytes(blob(value));record(name)

    save("contract-plan.json",dict(manifest(),source_blobs=pins))
    save("operation-trace.json",trace)
    save("read-results.json",reads)
    save("evidence-export.json",dict(
        mid=_export_json(export_mid),
        final=_export_json(export_final),
        final_state=dict(
            memory_revision=state.memory_revision,
            evidence_revision=state.evidence_revision,
            evidence_time=state.evidence_time,
        ),
    ))
    save("validation-summary.json",summary)

    guard()
    precheck(
        c212_summary,c211_summary,c210_summary,c209_summary,c208_summary,c207_summary,
        c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,
        c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
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
        C212_summary_sha256=PARENT_C212_SHA,
        source_blobs=pins,
        input_sha256=protected,
        artifacts=artifacts,
        validation_summary=summary,
        memory_bridge_schema=bridge.SCHEMA,
        model_forward_calls=0,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        fold_r_capsule=False,
        learned_writer=False,
        learned_reader=False,
        port_selector=False,
        h1_h2_compiler=False,
        limitations=[
            "deterministic memory-operation semantic bridge only",
            "no FOLD-R numeric capsule or correction-closure claim",
            "no learned Writer/Reader/Port Selector or language-to-operation mapping",
            "PASS establishes scope/revision/provenance boundary semantics, not Gate F",
        ],
    )
    validate_result(result)
    (out/"summary.json").write_bytes(blob(result))
    print(
        f"[C213] memory contract final_memory_revision={summary['final_memory_revision']} "
        f"evidence_revision={summary['final_evidence_revision']} "
        f"exported={summary['final_export_observations']}",
        flush=True,
    )
    print("=== C213 RESULT ===",flush=True)
    print(blob(result).decode(),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in (
        "c212-summary","c211-summary","c210-summary","c209-summary","c208-summary",
        "c207-summary","c206-summary","c205-summary","c204-summary","c203-summary",
        "c202-summary","c201-summary","c200-summary","c199-summary","c174-summary",
        "c181-summary","c188-summary","output-dir",
    ):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
