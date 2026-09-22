"""C224: raw-retaining H1/H2 versus full-history replay cost attribution.

Measurement PASS is not a storage-superiority verdict. No production module or neural weight changes.
"""
from __future__ import annotations

import argparse
from dataclasses import fields, is_dataclass
from enum import Enum
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import time
import unittest
import zipfile

import torch

EXPERIMENT_ID = "C224-v5f-raw-retaining-history-cost-audit"
STAGE = "V5-F-RAW-RETAINING-HISTORY-COST-AUDIT"
BASE = "52efcb66dae73b2e1f3b02eaf8fcc0beccbd577f"
PARENT_EXECUTION = "cdcc1d4211a149003f44dbdbd18a7e5367c013ab"
PARENT_SHA = "1b08cf76a1c233ce849f2b7fe81dbb7fa44120e59a75b32e2f42c4ebccdad2ca"
PARENT_VALIDATION_SHA = "b52c9d95bb89dca5061d2ccff4aab90276ea5dc4edba2d653b1d9fdc03d12db2"
MANIFEST_SHA = "0097887642e62a0c2e332d6b68a6dbcb769e829a1970387c3e0aa4ad28343103"
SIZES = (8,32,128,512)
REPEATS = 3
WARMUPS = 1
TOLERANCE = 1e-10
OWN = (
    "fold_lm/v05_benchmarks/gate_f_c224_history_cost_audit.py",
    "tests_lm/test_v05_c224_history_cost_audit.py",
    "tools/run_c224.ps1", "tools/invoke_c224.ps1",
    "docs/experiment-ledger-addendum-c224-preregistration.md",
    "docs/v5f-history-cost-audit-v0.1.md",
)
OUTPUTS = {"cost-plan.json", "memory-exports.zip", "measurements.json",
           "quality-checks.json", "validation-summary.json"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),
                       allow_nan=False)+"\n").encode("utf-8")


def sha_bytes(value):
    return hashlib.sha256(value).hexdigest()


def digest(value):
    return sha_bytes(blob(value))


def parent_module():
    from fold_lm.v05_benchmarks import gate_f_c223_request_freshness as parent
    return parent


def base_module():
    return parent_module().parent_module().parent_module().parent_module()


def ledger(size):
    require(type(size) is int and size >= 2,"size must be an integer >=2")
    chunks = []
    for i in range(size):
        factor = "alpha" if i == 0 else "beta"
        semantic = 1 if i == 0 else (i-1)%3
        kind = "ASSERT" if i < 2 else "REPLACE"
        chunks.append(blob(dict(schema="fold-cost-event-v1",kind=kind,factor=factor,
            scope="global" if factor == "alpha" else "project",
            relation=f"{factor}-class-{semantic}",source_id=f"cost:{i+1:08d}",time=i+1,
            text=f"{factor} の観測値を {semantic-1} と記録する。")))
    return b"".join(chunks)


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,
        parent_validation_sha256=PARENT_VALIDATION_SHA,sizes=list(SIZES),
        ledger_sha256={str(n):sha_bytes(ledger(n)) for n in SIZES},
        live_factors=2,query_trials=REPEATS,warmups=WARMUPS,numeric_tolerance=TOLERANCE,
        arms=["raw_retaining_h1_h2","full_history_replay"],
        raw_retention="identical full UTF-8 ledger in both arms",
        provenance_index="candidate-only source-to-byte-range benchmark sidecar",
        serialization="uncompressed canonical JSON plus original raw bytes",
        resident_metric="reachable Python objects plus unique CPU tensor storage estimate",
        process_peak_ram_measured=False,process_peak_vram_measured=False,
        learned_heads_exercised=False,new_training_steps=0,
        production_runtime_modified=False,gate_f_candidate=False,
        superiority_required_for_audit_pass=False,
        timing_is_descriptive=True,device="cpu",threads=2,deterministic_algorithms=True,
        scope="history-length scaling with two live factors; not many-factor scaling or a compression win")


def events(raw, meter):
    require(type(raw) is bytes,"raw evidence must be bytes")
    meter["raw_bytes"] += len(raw)
    for line in raw.splitlines():
        value = json.loads(line)
        require(value.get("schema") == "fold-cost-event-v1","event schema")
        meter["events"] += 1
        yield value


def source_index(raw):
    result = {}
    offset = 0
    for line in raw.splitlines(keepends=True):
        event = json.loads(line)
        source = event["source_id"]
        require(source not in result,"duplicate source ID")
        result[source] = (offset,offset+len(line))
        offset += len(line)
    require(offset == len(raw),"index did not cover ledger")
    return result


def validate_index(raw,index):
    covered = 0
    for source,(start,end) in sorted(index.items(),key=lambda item:item[1][0]):
        require(type(start) is int and type(end) is int and start == covered and start < end <= len(raw),
                "index gap or invalid byte range")
        event = json.loads(raw[start:end])
        require(event["source_id"] == source,"index source mismatch")
        covered = end
    require(covered == len(raw),"index incomplete")
    return True


def canonical(value):
    """Audit export, not a production checkpoint format. Reject unknown fields/types."""
    if isinstance(value,Enum):
        return {"enum":type(value).__name__,"value":value.value}
    if value is None or type(value) in (str,int,bool):
        return value
    if type(value) is float:
        require(math.isfinite(value),"nonfinite export")
        return value
    if isinstance(value,torch.Tensor):
        require(value.device.type == "cpu" and bool(torch.isfinite(value).all()),"invalid audit tensor")
        return dict(tensor=True,dtype=str(value.dtype),shape=list(value.shape),
                    values=value.detach().tolist())
    if isinstance(value,dict):
        require(all(type(k) is str for k in value),"export keys must be strings")
        return {k:canonical(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):
        return [canonical(v) for v in value]
    if is_dataclass(value):
        return {"type":type(value).__module__+"."+type(value).__name__,
                "fields":{f.name:canonical(getattr(value,f.name)) for f in fields(value)}}
    if hasattr(value,"__dict__") and type(value).__module__.startswith("fold_lm."):
        return {"type":type(value).__module__+"."+type(value).__name__,
                "fields":canonical(vars(value))}
    raise TypeError("unaccounted audit object:"+str(type(value)))


def resident_estimate(root):
    """Snapshot data estimate only; excludes allocator/cache/process/library overhead and peaks."""
    seen,storages = set(),set()
    python_bytes=tensor_bytes=0
    def walk(value):
        nonlocal python_bytes,tensor_bytes
        if id(value) in seen:
            return
        seen.add(id(value))
        python_bytes += sys.getsizeof(value)
        if isinstance(value,torch.Tensor):
            storage=value.untyped_storage()
            key=(str(value.device),storage.data_ptr(),storage.nbytes())
            if key not in storages:
                storages.add(key)
                tensor_bytes += storage.nbytes()
        elif isinstance(value,dict):
            for k,v in value.items():
                walk(k);walk(v)
        elif isinstance(value,(list,tuple)):
            for v in value:
                walk(v)
        elif isinstance(value,Enum):
            walk(value.value)
        elif hasattr(value,"__dict__"):
            walk(vars(value))
    walk(root)
    return dict(python_object_bytes=python_bytes,unique_cpu_tensor_storage_bytes=tensor_bytes,
                total_estimated_data_bytes=python_bytes+tensor_bytes)


def memory_op(memory,state,event):
    return memory.MemoryOp(kind=memory.MemoryOpKind(event["kind"]),
        expected_memory_revision=state.memory_revision,scope_id=event["scope"],
        factor_id=event["factor"],relation_key=event["relation"],
        source_id=event["source_id"],evidence_time=event["time"])


def build_candidate(backend,raw):
    bank=backend.c216.build_bank()
    state=bank.initial_state()
    meter=dict(raw_bytes=0,events=0)
    for event in events(raw,meter):
        state,read=bank.apply(state,memory_op(backend.memory,state,event))
        require(read is None,"mutation unexpectedly returned a query")
        state,status=bank.commit(state)
        require(status.value in ("COMMITTED","NOOP"),"candidate commit failed")
    return bank,state,meter


def query_candidate(bank,state,meter):
    # No raw evidence argument is read on this path; report all fields of this real bank state.
    return bank.read(state)


def query_replay(backend,bridge,raw,meter):
    state=backend.memory.MemoryState()
    for event in events(raw,meter):
        state,read=backend.memory.apply_memory_op(state,memory_op(backend.memory,state,event))
        require(read is None,"replay mutation returned query")
    return bridge.full_reference(state),state


def exports(bank,state,raw,index):
    candidate={"evidence.ndjson":raw,"source-index.json":blob(index),
               "state-and-bank.json":blob(canonical(dict(bank=bank,state=state)))}
    baseline={"evidence.ndjson":raw,"bridge.json":blob(canonical(bank.numeric))}
    return candidate,baseline


def file_inventory(files):
    return {name:dict(bytes=len(data),sha256=sha_bytes(data)) for name,data in files.items()}


def measure(backend,size):
    started=time.perf_counter_ns()
    raw=ledger(size)
    ledger_ns=time.perf_counter_ns()-started
    started=time.perf_counter_ns()
    index=source_index(raw)
    index_ns=time.perf_counter_ns()-started
    validate_index(raw,index)
    started=time.perf_counter_ns()
    bank,state,build_meter=build_candidate(backend,raw)
    build_ns=time.perf_counter_ns()-started
    state_before=blob(canonical(state))
    expected=bank.to_memory_state(state)
    require(len(expected.records) == 2,"live-factor count changed")
    # Validate actual current provenance against the real retained source bytes, outside query timing.
    provenance_ok=True
    for record in expected.records:
        start,end=index[record.provenance.source_id]
        event=json.loads(raw[start:end])
        provenance_ok &= (event["relation"] == record.relation_key and event["scope"] == record.scope_id)
    candidate_trials=[];baseline_trials=[];checks=[]
    for trial in range(WARMUPS+REPEATS):
        results={}
        order=("candidate","baseline") if trial%2 == 0 else ("baseline","candidate")
        for arm in order:
            meter=dict(raw_bytes=0,events=0)
            started=time.perf_counter_ns()
            if arm == "candidate":
                result=query_candidate(bank,state,meter)
                replay_state=None
            else:
                result,replay_state=query_replay(backend,bank.numeric,raw,meter)
            elapsed=time.perf_counter_ns()-started
            results[arm]=(result,replay_state)
            if trial >= WARMUPS:
                target=candidate_trials if arm == "candidate" else baseline_trials
                target.append(dict(elapsed_ns=elapsed,**meter))
        cr=results["candidate"][0];rr,rs=results["baseline"]
        supported=cr.status.value == rr.status.value == "SUPPORTED"
        error=float(torch.max(torch.abs(cr.value-rr.value)).item()) if supported else None
        checks.append(dict(trial=trial,warmup=trial<WARMUPS,supported=supported,max_abs_error=error,
                           symbolic_state_equal=canonical(expected) == canonical(rs)))
    require(blob(canonical(state)) == state_before,"query mutated retained state")
    started=time.perf_counter_ns()
    candidate_files,baseline_files=exports(bank,state,raw,index)
    export_ns=time.perf_counter_ns()-started
    candidate_bytes=sum(len(v) for v in candidate_files.values())
    baseline_bytes=sum(len(v) for v in baseline_files.values())
    row=dict(history_events=size,live_factors=2,raw_bytes=len(raw),raw_sha256=sha_bytes(raw),
        candidate_files=file_inventory(candidate_files),baseline_files=file_inventory(baseline_files),
        candidate_total_export_bytes=candidate_bytes,baseline_total_export_bytes=baseline_bytes,
        storage_delta_bytes=candidate_bytes-baseline_bytes,storage_ratio=candidate_bytes/baseline_bytes,
        candidate_resident_estimate=resident_estimate(dict(bank=bank,state=state,raw=raw,index=index)),
        baseline_resident_estimate=resident_estimate(dict(bridge=bank.numeric,raw=raw)),
        h2_numeric_payload_bytes=sum(x.numel()*x.element_size() for x in (state.h2.W,state.h2.b)),
        ledger_build_ns=ledger_ns,index_build_ns=index_ns,candidate_apply_commit_ns=build_ns,
        canonical_export_ns=export_ns,candidate_build_work=build_meter,
        candidate_query_trials=candidate_trials,baseline_query_trials=baseline_trials,
        candidate_query_median_ns=statistics.median(t["elapsed_ns"] for t in candidate_trials),
        baseline_query_median_ns=statistics.median(t["elapsed_ns"] for t in baseline_trials),
        source_index_entries=len(index),provenance_resolves=bool(provenance_ok),
        raw_retention_equal=candidate_files["evidence.ndjson"] == baseline_files["evidence.ndjson"],
        quality_pass=all(c["supported"] and c["symbolic_state_equal"] and c["max_abs_error"]<=TOLERANCE for c in checks),
        query_state_unchanged=True,process_peak_ram_bytes=None,process_peak_vram_bytes=None)
    return row,checks,candidate_files,baseline_files


def row_gate(row):
    n=row["history_events"]
    return (row["live_factors"] == 2 and row["quality_pass"] is True
        and row["provenance_resolves"] is True and row["raw_retention_equal"] is True
        and row["query_state_unchanged"] is True and row["source_index_entries"] == n
        and set(row["candidate_files"]) == {"evidence.ndjson","source-index.json","state-and-bank.json"}
        and set(row["baseline_files"]) == {"evidence.ndjson","bridge.json"}
        and all(row[key]["evidence.ndjson"] == dict(bytes=row["raw_bytes"],sha256=row["raw_sha256"])
                for key in ("candidate_files","baseline_files"))
        and row["candidate_build_work"] == dict(raw_bytes=row["raw_bytes"],events=n)
        and row["storage_delta_bytes"] == row["candidate_total_export_bytes"]-row["baseline_total_export_bytes"]
        and row["candidate_total_export_bytes"] == sum(v["bytes"] for v in row["candidate_files"].values())
        and row["baseline_total_export_bytes"] == sum(v["bytes"] for v in row["baseline_files"].values())
        and len(row["candidate_query_trials"]) == len(row["baseline_query_trials"]) == REPEATS
        and all(t["raw_bytes"] == t["events"] == 0 for t in row["candidate_query_trials"])
        and all(t["raw_bytes"] == row["raw_bytes"] and t["events"] == n for t in row["baseline_query_trials"]))


def summarize(rows):
    return dict(history_sizes=[r["history_events"] for r in rows],measurement_points=len(rows),
        audit_pass=all(row_gate(r) for r in rows),
        all_quality_parity=all(r["quality_pass"] for r in rows),
        storage_smaller_sizes=[r["history_events"] for r in rows if r["storage_delta_bytes"]<0],
        storage_delta_bytes=[r["storage_delta_bytes"] for r in rows],
        raw_query_bytes_candidate=[r["candidate_query_trials"][0]["raw_bytes"] for r in rows],
        raw_query_bytes_baseline=[r["baseline_query_trials"][0]["raw_bytes"] for r in rows],
        new_training_steps=0,learned_model_forward_calls=0,gate_f_candidate=False)


def gate(summary):
    return (summary.get("history_sizes") == list(SIZES) and summary.get("measurement_points") == len(SIZES)
        and summary.get("audit_pass") is True
        and summary.get("all_quality_parity") is True and summary.get("new_training_steps") == 0
        and summary.get("learned_model_forward_calls") == 0)


def precheck(c223_summary,root):
    parent=parent_module();a=base_module().audit;root=Path(root)
    require(a.sha(c223_summary) == PARENT_SHA,"C223 summary changed")
    p=a.read_json(c223_summary);parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS"
            and parent.gate(p["validation_summary"]),"wrong accepted C223")
    require(len(p["source_blobs"]) == 178 and len(p["input_sha256"]) == 220,"parent coverage")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for path,wanted in protected.items():
        require(Path(path).is_file() and a.sha(path) == wanted,"changed inherited input:"+path)
    for path,wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+path).decode().strip() == wanted,"changed parent source:"+path)
    protected[str(Path(c223_summary).resolve())]=PARENT_SHA
    validation_seen=False
    for item in p["artifacts"]:
        path=a.safe_child(Path(c223_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path) == item["sha256"] and path.stat().st_size == item["serialized_bytes"],"parent artifact changed")
        protected[str(path.resolve())]=item["sha256"]
        if item["file"] == "validation-summary.json":
            require(item["sha256"] == PARENT_VALIDATION_SHA,"parent validation changed")
            validation_seen=True
    require(validation_seen,"parent validation missing")
    for path in OWN:
        require(path not in pins,"OWN collides with accepted source")
        pins[path]=a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    dependencies=tuple(base_module().DIRECT_REPO_DEPENDENCIES)+(
        "fold_lm/v05_benchmarks/gate_f_c220_frozen_learned_stack.py",
        "fold_lm/v05/memory_dispatch.py","fold_lm/v05_benchmarks/gate_f_c221_live_coverage_dispatch.py",
        "fold_lm/v05_benchmarks/gate_f_c222_withdrawal_lifecycle.py",
        "fold_lm/v05/memory_request_lease.py","fold_lm/v05_benchmarks/gate_f_c223_request_freshness.py",
        "fold_lm/v05/state.py","fold_lm/capsule.py")
    require(len(dependencies) == 22 and all(path in pins for path in dependencies),"unpinned dependency")
    protected.update(a.protect_tree_files(root,pins))
    require(len(pins) == 184 and len(protected) == 232,"C224 protection counts")
    require(digest(manifest()) == MANIFEST_SHA,"C224 manifest drift")
    return p,pins,protected


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names) == len(set(names)) == 108,"parent module count")
    return names+["tests_lm.test_v05_c224_history_cost_audit"]


def regression_suite(root):
    helper=base_module().c205
    tests=list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    excluded=helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS;ids=[t.id() for t in tests]
    require(all(ids.count(x) == 1 for x in excluded),"historical exclusion identity")
    kept=[t for t in tests if t.id() not in excluded]
    require(len(tests) == 2466 and len(kept) == 2465,"C224 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE
            and p["diagnostic_execution_valid"] is True,"C224 result identity")
    require(len(p["source_blobs"]) == 184 and len(p["input_sha256"]) == 232
        and len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS,"C224 coverage")
    s=p["validation_summary"]
    require(s["history_sizes"] == list(SIZES),"incomplete audit")
    require(p["status"] == ("PASS" if gate(s) else "FAIL"),"C224 verdict drift")
    require(p["gate_f_candidate"] is False and p["production_runtime_modified"] is False
        and p["network_calls"] == 0,"scope drift")


def run(*,c223_summary,output_dir,expected_head):
    backend=base_module();a=backend.audit;root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip() == expected_head,"HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    _,pins,protected=precheck(c223_summary,root)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    rows=[];quality=[]
    with zipfile.ZipFile(out/"memory-exports.zip","w",compression=zipfile.ZIP_STORED) as archive:
        for size in SIZES:
            row,checks,candidate,baseline=measure(backend,size)
            rows.append(row);quality.append(dict(history_events=size,trials=checks))
            for arm,files in (("candidate",candidate),("baseline",baseline)):
                for name,data in files.items():
                    archive.writestr(f"{size}/{arm}/{name}",data)
    # Check archived bytes, not only the in-memory bookkeeping used to create them.
    with zipfile.ZipFile(out/"memory-exports.zip") as archive:
        for row in rows:
            for arm,key in (("candidate","candidate_files"),("baseline","baseline_files")):
                for name,item in row[key].items():
                    data=archive.read(f"{row['history_events']}/{arm}/{name}")
                    require(len(data) == item["bytes"] and sha_bytes(data) == item["sha256"],"export inventory mismatch")
    summary=summarize(rows)
    for name,value in (("cost-plan.json",manifest()),("measurements.json",rows),
                       ("quality-checks.json",quality),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard();precheck(c223_summary,root)
    for path,wanted in protected.items():
        require(a.sha(path) == wanted,"input changed:"+path)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if gate(summary) else "FAIL",diagnostic_execution_valid=True,
        C223_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
        validation_summary=summary,gate_f_candidate=False,production_runtime_modified=False,network_calls=0,
        limitations=["measurement PASS is not storage superiority",
            "canonical audit exports and reachable-data estimates, not native checkpoint size or process RAM peaks",
            "two live factors; revision history grows; many-factor lookup is not tested",
            "structured oracle operations and numeric reference; learned heads are not exercised",
            "same raw evidence retained; candidate source index is an explicitly costed benchmark sidecar",
            "no production optimization, compression, acquisition or Gate F claim"])
    validate_result(result);(out/"summary.json").write_bytes(blob(result))
    print("=== C224 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ("c223-summary","output-dir"):
        parser.add_argument("--"+arg,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
