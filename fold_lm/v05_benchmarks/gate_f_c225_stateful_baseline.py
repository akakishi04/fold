"""C225: H1/H2 versus incremental symbolic state; measurement is not superiority."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import statistics
import time
import unittest
import zipfile

import torch

EXPERIMENT_ID = "C225-v5f-stateful-baseline-attribution"
STAGE = "V5-F-STATEFUL-BASELINE-ATTRIBUTION"
BASE = "a8763643d8e8237f0b267cc89edf49bff74b9440"
PARENT_EXECUTION = "41ca548ed065b3e6dedd50dbc42ebb1b8df5f512"
PARENT_SHA = "d47f17ed6a467e5203f3bf5e39e5d023cfa469320f4636ca05d13d0673b09f88"
PARENT_VALIDATION_SHA = "5be4146f3139b761837bcbe0cad25db02c46035351e3d76b1a75a1ebd00211f2"
PARENT_MEASUREMENTS_SHA = "2e09353e3899f45bb2ee3598a61e72e1602858ae446a43de306abd07acbb832a"
SIZES = (8, 32, 128, 512)
RAW_HASHES = (
    "c940705b4253e319dce5e0e178fe262be6a1c613669b4b93eb72359136023357",
    "735d3c800017091f5dce4a91603ff40c61d6e8c24baa5c7ed504735e2d82f921",
    "01e5c6e53a31c92b9d1fe8411b7fdbbd60d3fb709177c8d8d87ca4c95250cf4f",
    "e4c0e12499275f7925d3648eb16d7d8b3f25e0769a6bd7603ff4fc656b3b7999",
)
REPEATS, WARMUPS, TOLERANCE = 3, 1, 1e-10
MANIFEST_SHA = "0520afee3c0b25ca1da8f28be3534115d72b1abbe4252628312fd2d321b24e66"
OWN = (
    "fold_lm/v05_benchmarks/gate_f_c225_stateful_baseline.py",
    "tests_lm/test_v05_c225_stateful_baseline.py",
    "tools/run_c225.ps1", "tools/invoke_c225.ps1",
    "docs/experiment-ledger-addendum-c225-preregistration.md",
    "docs/v5f-stateful-baseline-attribution-v0.1.md",
)
OUTPUTS = {"comparison-plan.json", "stateful-exports.zip", "measurements.json",
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
    from fold_lm.v05_benchmarks import gate_f_c224_history_cost_audit as parent
    return parent


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
        parent_validation_sha256=PARENT_VALIDATION_SHA,
        parent_measurements_sha256=PARENT_MEASUREMENTS_SHA,
        sizes=list(SIZES), raw_sha256=list(RAW_HASHES), live_factors=2,
        repeats=REPEATS, warmups=WARMUPS, numeric_tolerance=TOLERANCE,
        arms=["h1_h2", "incremental_symbolic_full_solve"],
        raw_and_index="identical complete raw evidence and source-index bytes in both arms",
        shared_bridge="same complete MemoryCapsuleBridge object including its compiled capsule",
        baseline="retain current MemoryState once per event; full_reference per query; no replay",
        serialization="same canonical uncompressed audit export as C224",
        resident_metric="reachable object and unique CPU tensor-storage estimate; not process peak",
        timing="alternating query order; descriptive medians only",
        superiority_required_for_pass=False, new_training_steps=0,
        learned_model_forward_calls=0, production_runtime_modified=False,
        gate_f_candidate=False, device="cpu", threads=2, deterministic_algorithms=True,
        scope="attribute two-live-factor query costs beyond ordinary incremental state retention")


def build_symbolic(backend, raw, helpers):
    state = backend.memory.MemoryState()
    meter = dict(raw_bytes=0, events=0)
    for event in helpers.events(raw, meter):
        op = helpers.memory_op(backend.memory, state, event)
        state, read = backend.memory.apply_memory_op(state, op)
        require(read is None, "symbolic update returned a query")
    return state, meter


def query_symbolic(bridge, state):
    # Neither original evidence nor source index is an input; no full-history replay.
    return bridge.full_reference(state)


def inventory(files):
    return {name: dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
            for name, data in files.items()}


def make_exports(helpers, bank, state, symbolic, raw, index):
    common = {"evidence.ndjson": raw, "source-index.json": helpers.blob(index)}
    candidate = dict(common, **{"state-and-bank.json": helpers.blob(
        helpers.canonical(dict(bank=bank, state=state)))})
    baseline = dict(common, **{"state-and-bridge.json": helpers.blob(
        helpers.canonical(dict(bridge=bank.numeric, state=symbolic)))})
    return candidate, baseline


def measure(helpers, backend, size):
    require(size in SIZES, "unregistered history size")
    raw = helpers.ledger(size)
    require(hashlib.sha256(raw).hexdigest() == RAW_HASHES[SIZES.index(size)], "raw identity drift")
    started = time.perf_counter_ns()
    index = helpers.source_index(raw)
    index_ns = time.perf_counter_ns() - started
    helpers.validate_index(raw, index)
    started = time.perf_counter_ns()
    bank, state, cm = helpers.build_candidate(backend, raw)
    candidate_build_ns = time.perf_counter_ns() - started
    started = time.perf_counter_ns()
    symbolic, sm = build_symbolic(backend, raw, helpers)
    symbolic_build_ns = time.perf_counter_ns() - started
    before_candidate = helpers.blob(helpers.canonical(state))
    before_symbolic = helpers.blob(helpers.canonical(symbolic))
    expected = bank.to_memory_state(state)
    state_equal = helpers.canonical(expected) == helpers.canonical(symbolic)
    provenance_ok = True
    for current in (expected, symbolic):
        for record in current.records:
            span = index.get(record.provenance.source_id)
            if span is None:
                provenance_ok = False
                continue
            event = json.loads(raw[span[0]:span[1]])
            provenance_ok &= (event["scope"], event["factor"], event["relation"]) == (
                record.scope_id, record.factor_id, record.relation_key)
    trials = {"candidate": [], "symbolic": []}
    checks = []
    for trial in range(WARMUPS + REPEATS):
        results = {}
        order = ("candidate", "symbolic") if trial % 2 == 0 else ("symbolic", "candidate")
        for arm in order:
            meter = dict(raw_bytes=0, events=0)
            started = time.perf_counter_ns()
            if arm == "candidate":
                result = helpers.query_candidate(bank, state, meter)
            else:
                result = query_symbolic(bank.numeric, symbolic)
            elapsed = time.perf_counter_ns() - started
            results[arm] = result
            if trial >= WARMUPS:
                trials[arm].append(dict(elapsed_ns=elapsed, **meter))
        cr, sr = results["candidate"], results["symbolic"]
        supported = cr.status.value == sr.status.value == "SUPPORTED"
        error = float(torch.max(torch.abs(cr.value - sr.value)).item()) if supported else None
        checks.append(dict(trial=trial, warmup=trial < WARMUPS, supported=supported,
                           max_abs_error=error))
    unchanged = (before_candidate == helpers.blob(helpers.canonical(state))
                 and before_symbolic == helpers.blob(helpers.canonical(symbolic)))
    started = time.perf_counter_ns()
    cf, sf = make_exports(helpers, bank, state, symbolic, raw, index)
    export_ns = time.perf_counter_ns() - started
    cb, sb = sum(map(len, cf.values())), sum(map(len, sf.values()))
    row = dict(history_events=size, raw_sha256=hashlib.sha256(raw).hexdigest(), raw_bytes=len(raw),
        candidate_live_factors=len(expected.records), symbolic_live_factors=len(symbolic.records),
        symbolic_state_equal=state_equal, provenance_resolves=bool(provenance_ok),
        query_state_unchanged=unchanged, source_index_entries=len(index),
        common_raw_and_index_equal=all(cf[k] == sf[k] for k in ("evidence.ndjson", "source-index.json")),
        candidate_files=inventory(cf), symbolic_files=inventory(sf),
        candidate_total_export_bytes=cb, symbolic_total_export_bytes=sb,
        storage_delta_bytes=cb-sb, storage_ratio=cb/sb,
        candidate_resident_estimate=helpers.resident_estimate(dict(bank=bank,state=state,raw=raw,index=index)),
        symbolic_resident_estimate=helpers.resident_estimate(dict(bridge=bank.numeric,state=symbolic,raw=raw,index=index)),
        index_build_ns=index_ns, candidate_build_ns=candidate_build_ns,
        symbolic_build_ns=symbolic_build_ns, export_ns=export_ns,
        candidate_build_work=cm, symbolic_build_work=sm,
        candidate_query_trials=trials["candidate"], symbolic_query_trials=trials["symbolic"],
        candidate_query_median_ns=statistics.median(x["elapsed_ns"] for x in trials["candidate"]),
        symbolic_query_median_ns=statistics.median(x["elapsed_ns"] for x in trials["symbolic"]),
        quality_pass=all(x["supported"] and x["max_abs_error"] <= TOLERANCE for x in checks),
        process_peak_ram_bytes=None, process_peak_vram_bytes=None)
    return row, checks, cf, sf


def row_gate(r):
    n = r["history_events"]
    ci, si = r["candidate_files"], r["symbolic_files"]
    return (n in SIZES and r["raw_sha256"] == RAW_HASHES[SIZES.index(n)]
        and r["candidate_live_factors"] == r["symbolic_live_factors"] == 2
        and r["symbolic_state_equal"] is True and r["provenance_resolves"] is True
        and r["query_state_unchanged"] is True and r["common_raw_and_index_equal"] is True
        and r["quality_pass"] is True and r["source_index_entries"] == n
        and set(ci) == {"evidence.ndjson","source-index.json","state-and-bank.json"}
        and set(si) == {"evidence.ndjson","source-index.json","state-and-bridge.json"}
        and all(ci[k] == si[k] for k in ("evidence.ndjson","source-index.json"))
        and ci["evidence.ndjson"] == dict(bytes=r["raw_bytes"],sha256=r["raw_sha256"])
        and r["candidate_build_work"] == r["symbolic_build_work"] == dict(raw_bytes=r["raw_bytes"],events=n)
        and r["candidate_total_export_bytes"] == sum(x["bytes"] for x in ci.values())
        and r["symbolic_total_export_bytes"] == sum(x["bytes"] for x in si.values())
        and r["storage_delta_bytes"] == r["candidate_total_export_bytes"]-r["symbolic_total_export_bytes"]
        and all(len(r[key]) == REPEATS and all(x["raw_bytes"] == x["events"] == 0 for x in r[key])
                for key in ("candidate_query_trials","symbolic_query_trials")))


def summarize(rows):
    return dict(history_sizes=[r["history_events"] for r in rows], measurement_points=len(rows),
        all_quality_parity=all(r["quality_pass"] and r["symbolic_state_equal"] for r in rows),
        audit_pass=all(row_gate(r) for r in rows),
        storage_delta_bytes=[r["storage_delta_bytes"] for r in rows],
        storage_smaller_sizes=[r["history_events"] for r in rows if r["storage_delta_bytes"] < 0],
        query_median_ratio_h1h2_over_symbolic=[r["candidate_query_median_ns"]/max(1,r["symbolic_query_median_ns"]) for r in rows],
        raw_query_bytes_candidate=[r["candidate_query_trials"][0]["raw_bytes"] for r in rows],
        raw_query_bytes_symbolic=[r["symbolic_query_trials"][0]["raw_bytes"] for r in rows],
        new_training_steps=0, learned_model_forward_calls=0)


def gate(s):
    return (s.get("history_sizes") == list(SIZES) and s.get("measurement_points") == len(SIZES)
        and s.get("audit_pass") is True and s.get("all_quality_parity") is True
        and s.get("new_training_steps") == s.get("learned_model_forward_calls") == 0)


def parent_measurement_adapter(rows, helpers):
    require(isinstance(rows,list) and len(rows) == len(SIZES), "parent rows incomplete")
    for row,n,wanted in zip(rows,SIZES,RAW_HASHES,strict=True):
        require(row["history_events"] == n and row["raw_sha256"] == wanted
                and helpers.row_gate(row), "parent measurement semantics drift")
    return {r["history_events"]: r for r in rows}


def verify_archive(path, rows):
    expected = {f"{r['history_events']}/{arm}/{name}":item for r in rows
        for arm,key in (("candidate","candidate_files"),("symbolic","symbolic_files"))
        for name,item in r[key].items()}
    with zipfile.ZipFile(path) as archive:
        require(len(archive.namelist()) == len(expected) and set(archive.namelist()) == set(expected),
                "archive members drift")
        for name,item in expected.items():
            data = archive.read(name)
            require(len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"],
                    "archive byte identity drift")


def precheck(c224_summary, root):
    parent = parent_module(); a = parent.base_module().audit; root = Path(root)
    require(a.sha(c224_summary) == PARENT_SHA,"C224 summary changed")
    p = a.read_json(c224_summary); parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS"
            and parent.gate(p["validation_summary"]),"wrong accepted C224")
    require(len(p["source_blobs"]) == 184 and len(p["input_sha256"]) == 232,"parent counts")
    pins,protected = dict(p["source_blobs"]),dict(p["input_sha256"])
    for path,wanted in protected.items():
        require(Path(path).is_file() and a.sha(path) == wanted,"changed inherited input:"+path)
    for path,wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+path).decode().strip() == wanted,"changed parent source:"+path)
    protected[str(Path(c224_summary).resolve())] = PARENT_SHA
    seen = set()
    for item in p["artifacts"]:
        path = a.safe_child(Path(c224_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path) == item["sha256"]
                and path.stat().st_size == item["serialized_bytes"],"parent artifact changed")
        protected[str(path.resolve())] = item["sha256"]
        expected = {"validation-summary.json":PARENT_VALIDATION_SHA,"measurements.json":PARENT_MEASUREMENTS_SHA}
        if item["file"] in expected:
            require(item["sha256"] == expected[item["file"]],"parent deciding artifact changed")
            seen.add(item["file"])
    require(len(seen) == 2,"parent deciding artifacts missing")
    parent_measurement_adapter(a.read_json(Path(c224_summary).resolve().parent/"measurements.json"),parent)
    require(tuple(parent.SIZES) == SIZES and parent.REPEATS == REPEATS and parent.WARMUPS == WARMUPS
            and parent.TOLERANCE == TOLERANCE,"parent experiment settings drift")
    for path in OWN:
        require(path not in pins,"OWN collides with accepted source")
        pins[path] = a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    dependencies = tuple(parent.base_module().DIRECT_REPO_DEPENDENCIES) + (
        "fold_lm/v05_benchmarks/gate_f_c220_frozen_learned_stack.py",
        "fold_lm/v05/memory_dispatch.py", "fold_lm/v05_benchmarks/gate_f_c221_live_coverage_dispatch.py",
        "fold_lm/v05_benchmarks/gate_f_c222_withdrawal_lifecycle.py",
        "fold_lm/v05/memory_request_lease.py", "fold_lm/v05_benchmarks/gate_f_c223_request_freshness.py",
        "fold_lm/v05/state.py", "fold_lm/capsule.py",
        "fold_lm/v05_benchmarks/gate_f_c224_history_cost_audit.py")
    require(len(dependencies) == len(set(dependencies)) == 23 and all(x in pins for x in dependencies),
            "unpinned direct dependency")
    protected.update(a.protect_tree_files(root,pins))
    require(len(pins) == 190 and len(protected) == 244,"C225 protection counts")
    require(digest(manifest()) == MANIFEST_SHA,"C225 manifest drift")
    return p,pins,protected


def regression_modules(root):
    names = parent_module().regression_modules(root)
    require(len(names) == len(set(names)) == 109,"parent module count")
    return names + ["tests_lm.test_v05_c225_stateful_baseline"]


def regression_suite(root):
    helper = parent_module().base_module().c205
    tests = list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    excluded = helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
    ids = [t.id() for t in tests]
    require(all(ids.count(x) == 1 for x in excluded),"historical exclusion identity")
    kept = [t for t in tests if t.id() not in excluded]
    require(len(tests) == 2498 and len(kept) == 2497,"C225 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE
            and p["diagnostic_execution_valid"] is True,"C225 identity")
    require(len(p["source_blobs"]) == 190 and len(p["input_sha256"]) == 244
            and len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS,"C225 coverage")
    s = p["validation_summary"]
    require(s["history_sizes"] == list(SIZES),"incomplete comparison")
    require(p["status"] == ("PASS" if gate(s) else "FAIL"),"C225 verdict drift")
    require(p["gate_f_candidate"] is False and p["production_runtime_modified"] is False
            and p["network_calls"] == 0,"scope drift")


def run(*, c224_summary, output_dir, expected_head):
    parent = parent_module(); backend = parent.base_module(); a = backend.audit
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip() == expected_head,"HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    _,pins,protected = precheck(c224_summary,root)
    parent_rows = parent_measurement_adapter(a.read_json(Path(c224_summary).resolve().parent/"measurements.json"),parent)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    rows,quality = [],[]
    with zipfile.ZipFile(out/"stateful-exports.zip","w",compression=zipfile.ZIP_STORED) as archive:
        for size in SIZES:
            row,checks,candidate,symbolic = measure(parent,backend,size)
            # Canonical byte identity, not timings, must match the parent H1/H2 arm.
            require(row["candidate_files"] == parent_rows[size]["candidate_files"],"parent candidate export drift")
            rows.append(row); quality.append(dict(history_events=size,trials=checks))
            for arm,files in (("candidate",candidate),("symbolic",symbolic)):
                for name,data in files.items():
                    archive.writestr(f"{size}/{arm}/{name}",data)
    verify_archive(out/"stateful-exports.zip",rows)
    summary = summarize(rows)
    for name,value in (("comparison-plan.json",manifest()),("measurements.json",rows),
                       ("quality-checks.json",quality),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size)
                 for name in sorted(OUTPUTS)]
    guard(); precheck(c224_summary,root)
    for path,wanted in protected.items():
        require(a.sha(path) == wanted,"protected input changed:"+path)
    result = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if gate(summary) else "FAIL",diagnostic_execution_valid=True,
        C224_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
        validation_summary=summary,gate_f_candidate=False,production_runtime_modified=False,network_calls=0,
        limitations=["measurement PASS is not stateful-baseline superiority",
            "two live factors and two-dimensional numeric system; no large-scale conclusion",
            "common bridge includes compiled capsule even on full-solve arm; shared overhead is not removed",
            "same raw evidence and full source index retained in both arms",
            "canonical export and reachable-data estimate, not native checkpoint or process peak",
            "no learned heads, retraining, optimization or Gate F claim"])
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C225 RESULT ===",flush=True); print(blob(result).decode(),flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("c224-summary","output-dir"):
        parser.add_argument("--"+arg,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
