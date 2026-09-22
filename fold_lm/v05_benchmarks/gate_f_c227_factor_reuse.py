"""C227: checked-factor reuse comparator; measurement PASS is not superiority."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import statistics
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

import torch

EXPERIMENT_ID = "C227-v5f-checked-factor-reuse-attribution"
STAGE = "V5-F-CHECKED-FACTOR-REUSE-ATTRIBUTION"
BASE = "c7ff247634a180784936173844049205891acc9b"
PARENT_EXECUTION = "17284250b25bdb5160d5d3ffa95501a4f5070e03"
PARENT_SHA = "ba4465c8c84e8fd54da1f7096a18056b7e53e6689a6ba3df5e1f9c559a7fac08"
PARENT_VALIDATION_SHA = "ec05f980af138ef10f243c2a75788d50f7322f47bd5b8309b7e896c398ccaad7"
PARENT_MEASUREMENTS_SHA = "f312af884dc6ee11bf02bf8b1aa3022531b3d599307571172557abc242519f44"
DIMENSIONS = (2, 16, 64, 256)
HISTORY_EVENTS = 32
RAW_SHA = "735d3c800017091f5dce4a91603ff40c61d6e8c24baa5c7ed504735e2d82f921"
WARMUPS, REPEATS, TOLERANCE = 1, 3, 1e-10
ARMS = ("candidate", "symbolic", "cached")
MANIFEST_SHA = "4ea370a98b04bff4364f2ec8dccbc5fff658c1d4529a13ee6c3fc1d0c0cfa23d"
OWN = (
    "fold_lm/v05_benchmarks/gate_f_c227_factor_reuse.py",
    "tests_lm/test_v05_c227_factor_reuse.py",
    "tools/run_c227.ps1", "tools/invoke_c227.ps1",
    "docs/experiment-ledger-addendum-c227-preregistration.md",
    "docs/v5f-checked-factor-reuse-v0.1.md",
)
OUTPUTS = {"reuse-plan.json", "reuse-exports.zip", "measurements.json",
           "quality-checks.json", "validation-summary.json"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import gate_f_c226_dimension_scaling as parent
    return parent


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
        parent_validation_sha256=PARENT_VALIDATION_SHA,
        parent_measurements_sha256=PARENT_MEASUREMENTS_SHA,
        dimensions=list(DIMENSIONS), history_events=HISTORY_EVENTS, raw_sha256=RAW_SHA,
        update_rank=2, readout_dim=2, live_factors=2, arms=list(ARMS),
        new_comparator="checked Cholesky of full updated system once; cholesky_solve per query",
        cache_scope="one immutable final state and bridge; no answer memoization or update algorithm",
        candidate_unchanged=True, parent_two_arm_export_parity=True,
        retain_full_raw_index_bridge=True, cache_factor_and_rhs_counted=True,
        warmups=WARMUPS, repeats=REPEATS, query_order="cyclic rotation of three arms",
        numeric_tolerance=TOLERANCE, timing_is_descriptive=True,
        trace="separate untimed factor preparation and three query traces; wrappers restored",
        process_peak_ram_measured=False, process_peak_vram_measured=False,
        new_training_steps=0, learned_model_forward_calls=0,
        production_runtime_modified=False, gate_f_candidate=False,
        superiority_required_for_pass=False, device="cpu", threads=2,
        deterministic_algorithms=True,
        scope="factorization-reuse attribution on fixed synthetic states; not general cache correctness")


def bridge_tensors(bridge):
    tensors = (bridge._J, bridge._eta, bridge._Q, bridge._U)
    for key in sorted(bridge._registry):
        contribution = bridge._registry[key]
        tensors += (contribution.W, contribution.b)
    return tensors


def tensor_stamps(tensors):
    return tuple((id(x), x._version) for x in tensors)


@dataclass
class FactorCache:
    state: object
    bridge: object
    L: torch.Tensor
    rhs: torch.Tensor
    stamps: tuple


def prepare_cache(bridge, state):
    status, W, bias, _ = bridge._aggregate(state)
    require(status.value == "SUPPORTED", "cache preparation outside capability")
    matrix = bridge._J + bridge._U @ W @ bridge._U.mT
    rhs = (bridge._eta + bridge._U @ bias).detach().clone()
    require(bool(torch.isfinite(matrix).all()) and bool(torch.isfinite(rhs).all()),
            "nonfinite cache preparation")
    # Positive-definiteness is checked here, once for this exact immutable state.
    L = torch.linalg.cholesky(matrix)
    tensors = bridge_tensors(bridge) + (L, rhs)
    return FactorCache(state, bridge, L, rhs, tensor_stamps(tensors))


def query_cached(cache, bridge, state):
    require(isinstance(cache, FactorCache), "wrong cache type")
    require(cache.state is state and cache.bridge is bridge, "stale cache binding")
    require(tensor_stamps(bridge_tensors(bridge) + (cache.L, cache.rhs)) == cache.stamps,
            "mutated cache or bridge tensor")
    value = bridge._Q @ torch.cholesky_solve(cache.rhs.unsqueeze(-1), cache.L)
    result = value.squeeze(-1)
    require(bool(torch.isfinite(result).all()), "nonfinite cached result")
    return result


def cache_payload(cache, helpers):
    # State and bridge refer to the complete objects already exported in state-and-bridge.json.
    # Object addresses are runtime bindings, not portable numerical data.
    return blob(dict(schema="fold-c227-factor-cache-audit-v1",
        references="state and bridge in state-and-bridge.json",
        memory_revision=cache.state.memory_revision,
        evidence_revision=cache.state.evidence_revision, evidence_time=cache.state.evidence_time,
        L=helpers.canonical(cache.L), rhs=helpers.canonical(cache.rhs),
        tensor_versions=[version for _, version in cache.stamps]))


def trace_call(fn):
    trace = []
    with ExitStack() as context:
        for owner, name, index in ((torch.linalg,"cholesky",0),
                                  (torch.linalg,"cholesky_ex",0),
                                  (torch.linalg,"solve",0), (torch,"cholesky_solve",1)):
            original = getattr(owner, name)
            def wrapped(*args, _name=name, _index=index, _original=original, **kwargs):
                matrix = args[_index] if len(args) > _index else kwargs[
                    "input2" if _name == "cholesky_solve" else "A"]
                trace.append(dict(operation=_name, matrix_shape=list(matrix.shape)))
                return _original(*args, **kwargs)
            context.enter_context(patch.object(owner, name, wrapped))
        result = fn()
    return result, trace


def expected_trace(n, arm):
    names, width = {
        "candidate": (("cholesky","cholesky_ex","solve"),2),
        "symbolic": (("cholesky","solve"),n),
        "cached": (("cholesky_solve",),n),
        "prepare": (("cholesky",),n),
    }[arm]
    return [dict(operation=x,matrix_shape=[width,width]) for x in names]


def query_order(trial):
    offset = trial % len(ARMS)
    return ARMS[offset:] + ARMS[:offset]


def parent_adapter(rows, parent):
    require(isinstance(rows,list) and len(rows) == len(DIMENSIONS), "parent points incomplete")
    require([r["numeric_dimension"] for r in rows] == list(DIMENSIONS), "parent dimensions drift")
    require(all(parent.row_gate(r,parent.parent_module()) for r in rows), "parent row invalid")
    return {r["numeric_dimension"]:r for r in rows}


def original_exports_equal(row, anchor):
    return all(row[arm+"_files"] == anchor[arm+"_files"] for arm in ("candidate","symbolic"))


def measure_dimension(parent, n):
    require(type(n) is int and n in DIMENSIONS, "unregistered dimension")
    symbolic = parent.parent_module()
    helpers = symbolic.parent_module()
    backend = helpers.base_module()
    raw = helpers.ledger(HISTORY_EVENTS)
    require(hashlib.sha256(raw).hexdigest() == RAW_SHA, "raw data drift")
    started = time.perf_counter_ns()
    index = helpers.source_index(raw)
    index_ns = time.perf_counter_ns()-started
    helpers.validate_index(raw,index)
    adapter = SimpleNamespace(memory=backend.memory,
        c216=SimpleNamespace(build_bank=lambda:parent.dimension_bank(backend,n)))
    started = time.perf_counter_ns()
    bank, state, cm = helpers.build_candidate(adapter,raw)
    candidate_build_ns = time.perf_counter_ns()-started
    started = time.perf_counter_ns()
    current, sm = symbolic.build_symbolic(adapter,raw,helpers)
    symbolic_build_ns = time.perf_counter_ns()-started
    started = time.perf_counter_ns()
    cache = prepare_cache(bank.numeric,current)
    cache_prepare_ns = time.perf_counter_ns()-started
    before = helpers.blob(helpers.canonical(dict(bank=bank,state=state,current=current)))
    cache_before = cache_payload(cache,helpers)
    state_equal = helpers.canonical(bank.to_memory_state(state)) == helpers.canonical(current)
    provenance_ok = all((lambda event: (event["scope"],event["factor"],event["relation"]) ==
        (r.scope_id,r.factor_id,r.relation_key))(json.loads(raw[slice(*index[r.provenance.source_id])]))
        for r in current.records)
    queries = dict(candidate=lambda:bank.read(state).value,
                   symbolic=lambda:symbolic.query_symbolic(bank.numeric,current).value,
                   cached=lambda:query_cached(cache,bank.numeric,current))
    trials = {arm:[] for arm in ARMS}
    checks = []
    for trial in range(WARMUPS+REPEATS):
        values = {}
        for arm in query_order(trial):
            started = time.perf_counter_ns()
            values[arm] = queries[arm]()
            elapsed = time.perf_counter_ns()-started
            if trial >= WARMUPS:
                trials[arm].append(dict(elapsed_ns=elapsed,raw_bytes=0,events=0))
        available = all(isinstance(v,torch.Tensor) and bool(torch.isfinite(v).all()) for v in values.values())
        errors = {arm:float(torch.max(torch.abs(values[arm]-values["symbolic"])))
                  for arm in ("candidate","cached")} if available else {}
        checks.append(dict(trial=trial,warmup=trial<WARMUPS,available=available,errors=errors,
                           passed=available and all(e <= TOLERANCE for e in errors.values())))
    # Independent untimed traces: never mix instrumentation into the timing samples.
    _, prep_trace = trace_call(lambda:prepare_cache(bank.numeric,current))
    traces = {arm:trace_call(queries[arm])[1] for arm in ARMS}
    unchanged = before == helpers.blob(helpers.canonical(dict(bank=bank,state=state,current=current)))
    unchanged = unchanged and cache_before == cache_payload(cache,helpers)
    started = time.perf_counter_ns()
    cf,sf = symbolic.make_exports(helpers,bank,state,current,raw,index)
    cached_files = dict(sf, **{"factorization-cache.json":cache_payload(cache,helpers)})
    export_ns = time.perf_counter_ns()-started
    files = dict(candidate=cf,symbolic=sf,cached=cached_files)
    row = dict(numeric_dimension=n,history_events=HISTORY_EVENTS,raw_sha256=RAW_SHA,
        live_factors=len(current.records),symbolic_state_equal=state_equal,
        provenance_resolves=bool(provenance_ok),query_state_unchanged=unchanged,
        quality_pass=all(c["passed"] for c in checks),cache_prepare_trace=prep_trace,
        query_traces=traces,candidate_build_ns=candidate_build_ns,
        symbolic_build_ns=symbolic_build_ns,cache_prepare_ns=cache_prepare_ns,
        index_build_ns=index_ns,export_ns=export_ns,candidate_build_work=cm,symbolic_build_work=sm,
        cache_factor_shape=list(cache.L.shape),cache_rhs_shape=list(cache.rhs.shape),
        additional_cache_tensor_bytes=cache.L.untyped_storage().nbytes()+cache.rhs.untyped_storage().nbytes(),
        process_peak_ram_bytes=None,process_peak_vram_bytes=None)
    for arm in ARMS:
        row[arm+"_files"] = symbolic.inventory(files[arm])
        row[arm+"_total_export_bytes"] = sum(map(len,files[arm].values()))
        row[arm+"_query_trials"] = trials[arm]
        row[arm+"_query_median_ns"] = statistics.median(x["elapsed_ns"] for x in trials[arm])
    roots = dict(candidate=dict(bank=bank,state=state,raw=raw,index=index),
        symbolic=dict(bridge=bank.numeric,state=current,raw=raw,index=index),
        cached=dict(bridge=bank.numeric,state=current,raw=raw,index=index,cache=cache))
    for arm in ARMS:
        row[arm+"_resident_estimate"] = helpers.resident_estimate(roots[arm])
    return row,checks,files


def row_gate(row):
    n = row["numeric_dimension"]
    if n not in DIMENSIONS:
        return False
    inventories = [row[a+"_files"] for a in ARMS]
    return (row["history_events"] == HISTORY_EVENTS and row["raw_sha256"] == RAW_SHA
        and row["live_factors"] == 2 and row["symbolic_state_equal"] is True
        and row["provenance_resolves"] is True and row["query_state_unchanged"] is True
        and row["quality_pass"] is True and row["parent_exports_equal"] is True
        and row["cache_prepare_trace"] == expected_trace(n,"prepare")
        and all(row["query_traces"][a] == expected_trace(n,a) for a in ARMS)
        and row["cache_factor_shape"] == [n,n] and row["cache_rhs_shape"] == [n]
        and row["additional_cache_tensor_bytes"] == 8*(n*n+n)
        and set(row["cached_files"]) == set(row["symbolic_files"])|{"factorization-cache.json"}
        and all(row["cached_files"][k] == v for k,v in row["symbolic_files"].items())
        and all(inv[k] == inventories[0][k] for inv in inventories for k in ("evidence.ndjson","source-index.json"))
        and all(row[a+"_total_export_bytes"] == sum(v["bytes"] for v in row[a+"_files"].values()) for a in ARMS)
        and all(len(row[a+"_query_trials"]) == REPEATS and all(
            r["raw_bytes"] == r["events"] == 0 for r in row[a+"_query_trials"]) for a in ARMS))


def summarize(rows):
    return dict(dimensions=[r["numeric_dimension"] for r in rows],
        all_quality_parity=all(r["quality_pass"] for r in rows),
        parent_exports_equal=all(r["parent_exports_equal"] for r in rows),
        audit_pass=all(row_gate(r) for r in rows),
        query_ratio_h1h2_over_cached=[r["candidate_query_median_ns"]/max(1,r["cached_query_median_ns"]) for r in rows],
        cached_extra_tensor_bytes=[r["additional_cache_tensor_bytes"] for r in rows],
        cached_query_refactorizations=[sum(t["operation"] in ("cholesky","cholesky_ex","solve")
            for t in r["query_traces"]["cached"]) for r in rows],
        new_training_steps=0,learned_model_forward_calls=0)


def gate(s):
    return (s.get("dimensions") == list(DIMENSIONS) and s.get("audit_pass") is True
        and s.get("all_quality_parity") is True and s.get("parent_exports_equal") is True
        and s.get("new_training_steps") == s.get("learned_model_forward_calls") == 0)


def verify_archive(path, rows):
    expected = {f"{r['numeric_dimension']}/{arm}/{name}":item for r in rows for arm in ARMS
                for name,item in r[arm+"_files"].items()}
    with zipfile.ZipFile(path) as archive:
        require(len(archive.namelist()) == len(expected) and set(archive.namelist()) == set(expected),
                "archive members drift")
        for name,item in expected.items():
            data = archive.read(name)
            require(len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"],
                    "archive bytes drift")


def precheck(c226_summary, root):
    parent=parent_module(); symbolic=parent.parent_module(); helpers=symbolic.parent_module()
    backend=helpers.base_module(); a=backend.audit; root=Path(root)
    require(a.sha(c226_summary) == PARENT_SHA,"C226 summary changed")
    p=a.read_json(c226_summary); parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS"
            and parent.gate(p["validation_summary"]),"wrong accepted C226")
    require(len(p["source_blobs"]) == 196 and len(p["input_sha256"]) == 256,"parent counts")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for path,wanted in protected.items():
        require(Path(path).is_file() and a.sha(path) == wanted,"inherited input changed:"+path)
    for path,wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+path).decode().strip() == wanted,"parent source changed:"+path)
    protected[str(Path(c226_summary).resolve())]=PARENT_SHA
    seen=set()
    for item in p["artifacts"]:
        path=a.safe_child(Path(c226_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path) == item["sha256"]
                and path.stat().st_size == item["serialized_bytes"],"parent artifact changed")
        protected[str(path.resolve())]=item["sha256"]
        expected={"measurements.json":PARENT_MEASUREMENTS_SHA,"validation-summary.json":PARENT_VALIDATION_SHA}
        if item["file"] in expected:
            require(item["sha256"] == expected[item["file"]],"parent deciding artifact changed")
            seen.add(item["file"])
    require(len(seen) == 2,"parent deciding artifact missing")
    parent_adapter(a.read_json(Path(c226_summary).resolve().parent/"measurements.json"),parent)
    require(tuple(parent.DIMENSIONS) == DIMENSIONS and parent.HISTORY_EVENTS == HISTORY_EVENTS
            and parent.RAW_SHA == RAW_SHA and parent.TOLERANCE == TOLERANCE,"parent settings drift")
    for path in OWN:
        require(path not in pins,"OWN overlaps accepted source")
        pins[path]=a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    dependencies=tuple(backend.DIRECT_REPO_DEPENDENCIES)+(
        "fold_lm/v05_benchmarks/gate_f_c220_frozen_learned_stack.py",
        "fold_lm/v05/memory_dispatch.py","fold_lm/v05_benchmarks/gate_f_c221_live_coverage_dispatch.py",
        "fold_lm/v05_benchmarks/gate_f_c222_withdrawal_lifecycle.py",
        "fold_lm/v05/memory_request_lease.py","fold_lm/v05_benchmarks/gate_f_c223_request_freshness.py",
        "fold_lm/v05/state.py","fold_lm/capsule.py",
        "fold_lm/v05_benchmarks/gate_f_c224_history_cost_audit.py",
        "fold_lm/v05_benchmarks/gate_f_c225_stateful_baseline.py",
        "fold_lm/v05_benchmarks/gate_f_c226_dimension_scaling.py")
    require(len(dependencies) == len(set(dependencies)) == 25 and all(x in pins for x in dependencies),
            "unpinned direct dependency")
    protected.update(a.protect_tree_files(root,pins))
    require(len(pins) == 202 and len(protected) == 268,"C227 protection counts")
    require(digest(manifest()) == MANIFEST_SHA,"C227 manifest drift")
    return p,pins,protected


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names) == len(set(names)) == 111,"parent module count")
    return names+["tests_lm.test_v05_c227_factor_reuse"]


def regression_suite(root):
    helper=parent_module().parent_module().parent_module().base_module().c205
    tests=list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    excluded=helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
    ids=[t.id() for t in tests]
    require(all(ids.count(x) == 1 for x in excluded),"historical exclusion identity")
    kept=[t for t in tests if t.id() not in excluded]
    require(len(tests) == 2562 and len(kept) == 2561,"C227 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE
            and p["diagnostic_execution_valid"] is True,"C227 identity")
    require(len(p["source_blobs"]) == 202 and len(p["input_sha256"]) == 268
            and len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS,"C227 coverage")
    require(p["validation_summary"]["dimensions"] == list(DIMENSIONS),"incomplete C227")
    require(p["status"] == ("PASS" if gate(p["validation_summary"]) else "FAIL"),"C227 verdict drift")
    require(p["gate_f_candidate"] is False and p["production_runtime_modified"] is False
            and p["network_calls"] == 0,"scope drift")


def run(*, c226_summary, output_dir, expected_head):
    parent=parent_module(); a=parent.parent_module().parent_module().base_module().audit
    root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip() == expected_head,"HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    _,pins,protected=precheck(c226_summary,root)
    anchors=parent_adapter(a.read_json(Path(c226_summary).resolve().parent/"measurements.json"),parent)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    rows,quality=[],[]
    with zipfile.ZipFile(out/"reuse-exports.zip","w",compression=zipfile.ZIP_STORED) as archive:
        for n in DIMENSIONS:
            row,checks,files=measure_dimension(parent,n)
            row["parent_exports_equal"]=original_exports_equal(row,anchors[n])
            rows.append(row); quality.append(dict(numeric_dimension=n,trials=checks))
            for arm in ARMS:
                for name,data in files[arm].items():
                    archive.writestr(f"{n}/{arm}/{name}",data)
    verify_archive(out/"reuse-exports.zip",rows)
    summary=summarize(rows)
    for name,value in (("reuse-plan.json",manifest()),("measurements.json",rows),
                       ("quality-checks.json",quality),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size)
               for name in sorted(OUTPUTS)]
    guard(); precheck(c226_summary,root)
    for path,wanted in protected.items():
        require(a.sha(path) == wanted,"protected input changed:"+path)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if gate(summary) else "FAIL",diagnostic_execution_valid=True,
        C226_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
        validation_summary=summary,gate_f_candidate=False,production_runtime_modified=False,network_calls=0,
        limitations=["measurement PASS is not speed/storage superiority",
            "factor reuse only for the exact frozen state; not general invalidation or concurrency",
            "no answer memoization; identical answers could also be cached",
            "complete shared bridge including unused capsule remains in both symbolic arms",
            "descriptive three-trial timings; canonical exports and reachable data, not process peaks",
            "no learned inference, production optimization, many-factor or Gate F claim"])
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C227 RESULT ===",flush=True); print(blob(result).decode(),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ("c226-summary","output-dir"):
        parser.add_argument("--"+arg,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
