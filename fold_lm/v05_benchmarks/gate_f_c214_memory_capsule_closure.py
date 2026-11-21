"""C214: V5-F semantic memory -> FOLD-R response-capsule correction closure.

Scientific question: when accepted C213 observed edit semantics are projected into the existing
fixed-port response capsule, do supported snapshots match an independent full-memory solve within
registered float64 tolerance?

No learned Writer/Reader/Port Selector, H1/H2 compiler, language parsing or model inference is used.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import unittest

import torch

from fold_lm.v05 import memory_bridge as memory
from fold_lm.v05 import memory_capsule_bridge as capsule_bridge
from fold_lm.v05_benchmarks import gate_e_c175_frozen_prediction_audit as audit
from fold_lm.v05_benchmarks import gate_e_c205_phase0_batch_composition_attribution as c205
from fold_lm.v05_benchmarks import gate_f_c213_memory_operation_contract as c213

EXPERIMENT_ID = "C214-v5f-memory-capsule-closure"
STAGE = "V5-F-MEMORY-CAPSULE-CLOSURE"
BASE = "fc23c3e8e33f692565f9b358f11d7cf6ea1a9713"
PARENT_C213_EXECUTION = "f59f615b5d409400c9fc5247270a37960ffac197"
PARENT_C213_SHA = "370ee39bcd32da4ce797ecfb21ce3b863013c788f6daaaf0fb9a10edac643b43"
PARENT_C213_VALIDATION_SHA = "fca1e55a4da9715292523c84bb490dda7dcb75aead4cf9ad98f76fc0a867b521"
CAPSULE_SOURCE_BLOB = "7f1090fe95b2e3eab3967d00c6730165e34fadfb"
MANIFEST_SHA = "dc2354bd35d94ef0d8b7e5f4c6bed820f5166f0ce20948df612b30d1b0465915"
TOLERANCE = 1e-10
OWN = (
    "fold_lm/v05/memory_capsule_bridge.py",
    "fold_lm/v05_benchmarks/gate_f_c214_memory_capsule_closure.py",
    "tests_lm/test_v05_c214_memory_capsule_closure.py",
    "tools/run_c214.ps1",
    "tools/invoke_c214.ps1",
    "docs/experiment-ledger-addendum-c214-preregistration.md",
    "docs/v5f-memory-capsule-closure-v0.1.md",
)
OUTPUTS = {
    "bridge-plan.json",
    "state-trace.json",
    "snapshot-comparisons.json",
    "control-results.json",
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
        parent_c213_execution=PARENT_C213_EXECUTION,
        parent_c213_sha256=PARENT_C213_SHA,
        parent_c213_validation_sha256=PARENT_C213_VALIDATION_SHA,
        capsule_source_blob=CAPSULE_SOURCE_BLOB,
        memory_bridge_schema=memory.SCHEMA,
        variable_dim=4,
        update_rank=2,
        readout_dim=2,
        supported_snapshots=7,
        safe_relation_count=3,
        numeric_unsafe_relation_count=1,
        out_of_scope_controls=1,
        numeric_unsafe_controls=1,
        hypothesis_isolation_checks=2,
        max_abs_error_tolerance=TOLERANCE,
        full_reference_comparison=True,
        learned_writer=False,
        learned_reader=False,
        port_selector=False,
        h1_h2_compiler=False,
        model_forward_calls=0,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        scope=(
            "project accepted C213 observed-memory edits into the existing fixed-port FOLD-R "
            "response capsule and compare supported readouts to a full-memory solve; no learned routing"
        ),
    )


def build_bridge():
    J=torch.tensor([
        [4.0,0.2,0.0,0.0],
        [0.2,3.5,0.1,0.0],
        [0.0,0.1,5.0,0.3],
        [0.0,0.0,0.3,4.5],
    ],dtype=torch.float64)
    eta=torch.tensor([0.5,-0.25,0.75,0.2],dtype=torch.float64)
    Q=torch.tensor([
        [1.0,0.0,0.5,0.0],
        [0.0,1.0,0.0,-0.25],
    ],dtype=torch.float64)
    U=torch.tensor([
        [1.0,0.0],
        [0.0,1.0],
        [0.5,0.0],
        [0.0,0.5],
    ],dtype=torch.float64)
    contributions=(
        capsule_bridge.PortContribution(
            "rel-alpha-v1",
            torch.tensor([[0.25,0.0],[0.0,0.0]],dtype=torch.float64),
            torch.tensor([0.4,0.0],dtype=torch.float64),
        ),
        capsule_bridge.PortContribution(
            "rel-alpha-v2",
            torch.tensor([[0.35,0.05],[0.05,0.10]],dtype=torch.float64),
            torch.tensor([0.2,-0.15],dtype=torch.float64),
        ),
        capsule_bridge.PortContribution(
            "rel-beta-v1",
            torch.tensor([[0.0,0.0],[0.0,0.30]],dtype=torch.float64),
            torch.tensor([0.0,0.45],dtype=torch.float64),
        ),
        capsule_bridge.PortContribution(
            "rel-unsafe",
            torch.tensor([[-10.0,0.0],[0.0,0.0]],dtype=torch.float64),
            torch.tensor([0.0,0.0],dtype=torch.float64),
        ),
    )
    return capsule_bridge.MemoryCapsuleBridge(J,eta,Q,U,contributions)


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
    bridge=build_bridge()
    state=memory.MemoryState()
    trace=[]
    comparisons=[]

    def compare(label):
        capsule=bridge.read(state)
        full=bridge.full_reference(state)
        row=dict(
            label=label,
            memory_revision=state.memory_revision,
            evidence_revision=state.evidence_revision,
            observed_factor_ids=list(capsule.observed_factor_ids),
            capsule_status=capsule.status.value,
            full_status=full.status.value,
            capsule_value=_value(capsule),
            full_value=_value(full),
            max_abs_error=None,
        )
        if capsule.status is capsule_bridge.CapsuleReadStatus.SUPPORTED:
            require(full.status is capsule_bridge.CapsuleReadStatus.SUPPORTED,
                    "full reference status mismatch")
            error=float(torch.max(torch.abs(capsule.value-full.value)).item())
            row["max_abs_error"]=error
        comparisons.append(row)

    def mutate(label,op):
        nonlocal state
        before=state
        state,result=memory.apply_memory_op(state,op)
        require(result is None,"mutation returned read")
        trace.append(dict(
            label=label,
            kind=op.kind.value,
            before_memory_revision=before.memory_revision,
            after_memory_revision=state.memory_revision,
            before_evidence_revision=before.evidence_revision,
            after_evidence_revision=state.evidence_revision,
        ))

    compare("initial")
    mutate("assert_alpha",_op(
        memory.MemoryOpKind.ASSERT,0,memory.GLOBAL_SCOPE,
        factor="alpha",relation="rel-alpha-v1",source="user:1",evidence_time=1,
    ))
    compare("after_assert_alpha")
    mutate("replace_alpha",_op(
        memory.MemoryOpKind.REPLACE,1,memory.GLOBAL_SCOPE,
        factor="alpha",relation="rel-alpha-v2",source="user:2",evidence_time=2,
    ))
    compare("after_replace_alpha")
    mutate("assert_beta",_op(
        memory.MemoryOpKind.ASSERT,2,"project",
        factor="beta",relation="rel-beta-v1",source="doc:1",evidence_time=2,
    ))
    compare("after_assert_beta")
    mutate("retract_alpha",_op(
        memory.MemoryOpKind.RETRACT,3,memory.GLOBAL_SCOPE,
        factor="alpha",source="user:3",evidence_time=3,
    ))
    compare("after_retract_alpha")
    observed_only_value=comparisons[-1]["capsule_value"]

    mutate("assume_temp",_op(
        memory.MemoryOpKind.ASSUME,4,"sandbox",
        factor="temp",relation="rel-hypothesis-unmapped",
    ))
    compare("after_assume_temp")
    assume_value=comparisons[-1]["capsule_value"]

    mutate("end_sandbox",_op(
        memory.MemoryOpKind.END_SCOPE,5,"sandbox",
    ))
    compare("after_end_sandbox")
    end_value=comparisons[-1]["capsule_value"]

    oos=memory.MemoryState()
    oos,_=memory.apply_memory_op(oos,_op(
        memory.MemoryOpKind.ASSERT,0,memory.GLOBAL_SCOPE,
        factor="unknown",relation="rel-out-of-scope",source="external:oos",evidence_time=1,
    ))
    oos_capsule=bridge.read(oos)
    oos_full=bridge.full_reference(oos)

    unsafe=memory.MemoryState()
    unsafe,_=memory.apply_memory_op(unsafe,_op(
        memory.MemoryOpKind.ASSERT,0,memory.GLOBAL_SCOPE,
        factor="unsafe",relation="rel-unsafe",source="external:unsafe",evidence_time=1,
    ))
    unsafe_capsule=bridge.read(unsafe)
    unsafe_full=bridge.full_reference(unsafe)

    controls=dict(
        out_of_scope=dict(
            capsule_status=oos_capsule.status.value,
            full_status=oos_full.status.value,
            value_exposed=oos_capsule.value is not None,
        ),
        numeric_unsafe=dict(
            capsule_status=unsafe_capsule.status.value,
            full_status=unsafe_full.status.value,
            value_exposed=unsafe_capsule.value is not None,
        ),
        assumption_readout_delta=max(
            abs(a-b) for a,b in zip(observed_only_value,assume_value,strict=True)
        ),
        end_scope_readout_delta=max(
            abs(a-b) for a,b in zip(observed_only_value,end_value,strict=True)
        ),
    )
    final_export=memory.export_observed(state)
    errors=[x["max_abs_error"] for x in comparisons if x["max_abs_error"] is not None]
    summary=dict(
        supported_snapshots=len(comparisons),
        supported_status_counts=dict(Counter(x["capsule_status"] for x in comparisons)),
        max_abs_error=max(errors),
        tolerance=TOLERANCE,
        all_full_reference_statuses_match=all(
            x["capsule_status"]==x["full_status"] for x in comparisons
        ),
        factor_count_sequence=[len(x["observed_factor_ids"]) for x in comparisons],
        final_memory_revision=state.memory_revision,
        final_evidence_revision=state.evidence_revision,
        final_evidence_time=state.evidence_time,
        final_export_observations=len(final_export.evidence.observations),
        final_export_factor_ids=[x.factor_id for x in final_export.bindings],
        assumption_readout_delta=controls["assumption_readout_delta"],
        end_scope_readout_delta=controls["end_scope_readout_delta"],
        out_of_scope_status=controls["out_of_scope"]["capsule_status"],
        out_of_scope_full_status=controls["out_of_scope"]["full_status"],
        numeric_unsafe_status=controls["numeric_unsafe"]["capsule_status"],
        numeric_unsafe_full_status=controls["numeric_unsafe"]["full_status"],
        non_supported_value_exposures=int(
            controls["out_of_scope"]["value_exposed"]
            or controls["numeric_unsafe"]["value_exposed"]
        ),
        learned_writer_calls=0,
        learned_reader_calls=0,
        port_selector_calls=0,
        model_forward_calls=0,
    )
    return state,trace,comparisons,controls,summary


def gate(summary):
    return (
        summary.get("supported_snapshots")==7
        and summary.get("supported_status_counts")=={"SUPPORTED":7}
        and summary.get("max_abs_error") is not None
        and summary.get("max_abs_error")<=TOLERANCE
        and summary.get("all_full_reference_statuses_match") is True
        and summary.get("factor_count_sequence")==[0,1,1,2,1,1,1]
        and summary.get("final_memory_revision")==6
        and summary.get("final_evidence_revision")==4
        and summary.get("final_evidence_time")==3
        and summary.get("final_export_observations")==1
        and summary.get("final_export_factor_ids")==["beta"]
        and summary.get("assumption_readout_delta")==0.0
        and summary.get("end_scope_readout_delta")==0.0
        and summary.get("out_of_scope_status")=="OUT_OF_SCOPE"
        and summary.get("out_of_scope_full_status")=="OUT_OF_SCOPE"
        and summary.get("numeric_unsafe_status")=="NUMERIC_UNSAFE"
        and summary.get("numeric_unsafe_full_status")=="NUMERIC_UNSAFE"
        and summary.get("non_supported_value_exposures")==0
        and summary.get("learned_writer_calls")==0
        and summary.get("learned_reader_calls")==0
        and summary.get("port_selector_calls")==0
        and summary.get("model_forward_calls")==0
    )


def precheck(
    c213_summary,c212_summary,c211_summary,c210_summary,c209_summary,c208_summary,
    c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,
    c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
):
    root=Path(root)
    p212,pins,protected=c213.precheck(
        c212_summary,c211_summary,c210_summary,c209_summary,c208_summary,c207_summary,
        c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,c201_summary,
        c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
    )
    require(audit.sha(c213_summary)==PARENT_C213_SHA,"C213 summary changed")
    p213=audit.read_json(c213_summary)
    c213.validate_result(p213)
    require(
        p213.get("commit_sha")==PARENT_C213_EXECUTION
        and p213.get("status")=="PASS"
        and c213.gate(p213["validation_summary"])
        and p213.get("source_blobs")==pins
        and p213.get("memory_bridge_schema")==memory.SCHEMA,
        "Wrong accepted C213 parent",
    )
    protected[str(Path(c213_summary).resolve())]=PARENT_C213_SHA
    validation_seen=False
    for artifact in p213["artifacts"]:
        path=audit.safe_child(Path(c213_summary).resolve().parent,artifact["file"])
        require(
            path.is_file() and path.stat().st_size==artifact["serialized_bytes"]
            and audit.sha(path)==artifact["sha256"],
            "Changed C213 artifact:"+artifact["file"],
        )
        if artifact["file"]=="validation-summary.json":
            require(artifact["sha256"]==PARENT_C213_VALIDATION_SHA,
                    "C213 validation artifact changed")
            validation_seen=True
        protected[str(path.resolve())]=artifact["sha256"]
    require(validation_seen,"C213 validation artifact missing")

    pins=dict(pins)
    capsule_blob=audit.git(root,"rev-parse","HEAD:fold_lm/capsule.py").decode().strip()
    require(capsule_blob==CAPSULE_SOURCE_BLOB,"Response capsule source changed")
    pins["fold_lm/capsule.py"]=CAPSULE_SOURCE_BLOB

    allpins=dict(pins)
    for name in OWN:
        allpins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    protected.update(audit.protect_tree_files(root,allpins))
    pins.update({name:allpins[name] for name in OWN})

    require(len(pins)==115 and len(protected)==217,"C214 source/protection count drift")
    require(digest(manifest())==MANIFEST_SHA,"C214 manifest drift")
    return p213,pins,protected


def regression_modules(root):
    names=c213.regression_modules(root)
    require(len(names)==len(set(names))==98,"Historical regression module drift")
    return names+["tests_lm.test_v05_c214_memory_capsule_closure"]


def regression_suite(root):
    names=regression_modules(root)
    loaded=unittest.defaultTestLoader.loadTestsFromNames(names)
    tests=list(c205._iter_tests(loaded))
    ids=[test.id() for test in tests]
    for excluded in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS:
        require(ids.count(excluded)==1,"Historical dynamic test identity drift:"+excluded)
    kept=[test for test in tests if test.id() not in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS]
    require(
        len(tests)==2116 and len(kept)==2115
        and not any(test.id() in c205.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS for test in kept),
        "C214 focused regression filtering drift",
    )
    return unittest.TestSuite(kept)


def validate_result(payload):
    require(
        payload["experiment_id"]==EXPERIMENT_ID
        and payload["stage"]==STAGE
        and payload["diagnostic_execution_valid"] is True,
        "Wrong/incomplete C214",
    )
    require(
        len(payload["source_blobs"])==115
        and len(payload["input_sha256"])==217
        and len(payload["artifacts"])==5
        and {a["file"] for a in payload["artifacts"]}==OUTPUTS,
        "C214 coverage drift",
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
        and payload["h1_h2_compiler"] is False,
        "C214 scope drift",
    )
    require(
        payload["status"]==("PASS" if gate(payload["validation_summary"]) else "FAIL"),
        "C214 gate drift",
    )


def run(
    *,c213_summary,c212_summary,c211_summary,c210_summary,c209_summary,c208_summary,
    c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,
    c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,
    output_dir,expected_head
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
        c213_summary,c212_summary,c211_summary,c210_summary,c209_summary,c208_summary,
        c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,
        c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
    )

    state,trace,comparisons,controls,summary=collect_fixture()
    out=Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    artifacts=[]

    def record(name):
        path=out/name
        artifacts.append(dict(file=name,sha256=audit.sha(path),serialized_bytes=path.stat().st_size))

    def save(name,value):
        (out/name).write_bytes(blob(value));record(name)

    save("bridge-plan.json",dict(manifest(),source_blobs=pins))
    save("state-trace.json",trace)
    save("snapshot-comparisons.json",comparisons)
    save("control-results.json",controls)
    save("validation-summary.json",summary)

    guard()
    precheck(
        c213_summary,c212_summary,c211_summary,c210_summary,c209_summary,c208_summary,
        c207_summary,c206_summary,c205_summary,c204_summary,c203_summary,c202_summary,
        c201_summary,c200_summary,c199_summary,c174_summary,c181_summary,c188_summary,root
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
        C213_summary_sha256=PARENT_C213_SHA,
        source_blobs=pins,
        input_sha256=protected,
        artifacts=artifacts,
        validation_summary=summary,
        capsule_source_blob=CAPSULE_SOURCE_BLOB,
        model_forward_calls=0,
        training_steps=0,
        fresh_seed_count=0,
        network_calls=0,
        production_runtime_modified=True,
        gate_f_candidate=False,
        learned_writer=False,
        learned_reader=False,
        port_selector=False,
        h1_h2_compiler=False,
        limitations=[
            "fixed predeclared relation-to-port registry; no learned Port Selector",
            "reference float64 capsule closure only; no H1/H2 bank or chunk commit",
            "hypotheses are intentionally excluded from authoritative numeric capsule updates",
            "PASS supports the semantic-to-numeric bridge only, not Gate F",
        ],
    )
    validate_result(result)
    (out/"summary.json").write_bytes(blob(result))
    print(
        f"[C214] capsule closure snapshots={summary['supported_snapshots']} "
        f"max_abs_error={summary['max_abs_error']:.3e} "
        f"oos={summary['out_of_scope_status']} unsafe={summary['numeric_unsafe_status']}",
        flush=True,
    )
    print("=== C214 RESULT ===",flush=True)
    print(blob(result).decode(),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in (
        "c213-summary","c212-summary","c211-summary","c210-summary","c209-summary",
        "c208-summary","c207-summary","c206-summary","c205-summary","c204-summary",
        "c203-summary","c202-summary","c201-summary","c200-summary","c199-summary",
        "c174-summary","c181-summary","c188-summary","output-dir",
    ):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":
    main()
