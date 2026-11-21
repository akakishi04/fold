"""C226: fixed-port numerical-dimension scaling; audit PASS is not superiority."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

import torch

EXPERIMENT_ID = "C226-v5f-fixed-port-dimension-scaling"
STAGE = "V5-F-FIXED-PORT-DIMENSION-SCALING"
BASE = "fee045a752043b8abaaa04c14db000ed7b0d4be4"
PARENT_EXECUTION = "6669add6de53247e60731a3f23e7bed9350deec3"
PARENT_SHA = "b54943514cebb06161851e6a79c9eb4e8fd6766429f6f2e0e2f34c79c52a78ad"
PARENT_VALIDATION_SHA = "94e2028aaaff24f9cc03480abde49c2e41674d833141745e6bc34f9852620a29"
PARENT_MEASUREMENTS_SHA = "50e82a0a655ab63ddf00da04edab1995c7b99064ae493ba5320a0d2f348362a2"
DIMENSIONS = (2, 16, 64, 256)
HISTORY_EVENTS = 32
RAW_SHA = "735d3c800017091f5dce4a91603ff40c61d6e8c24baa5c7ed504735e2d82f921"
TOLERANCE = 1e-10
MANIFEST_SHA = "77a17f1330f62a1278922d40cb7313c610a7caa29c653b618b5f1e43f872a093"
OWN = (
    "fold_lm/v05_benchmarks/gate_f_c226_dimension_scaling.py",
    "tests_lm/test_v05_c226_dimension_scaling.py",
    "tools/run_c226.ps1", "tools/invoke_c226.ps1",
    "docs/experiment-ledger-addendum-c226-preregistration.md",
    "docs/v5f-fixed-port-dimension-scaling-v0.1.md",
)
OUTPUTS = {"dimension-plan.json", "dimension-exports.zip", "measurements.json",
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
    from fold_lm.v05_benchmarks import gate_f_c225_stateful_baseline as parent
    return parent


def dimension_tensors(n):
    require(type(n) is int and n in DIMENSIONS, "unregistered dimension")
    J = torch.eye(n, dtype=torch.float64) * 4.0
    # Visible coordinates 0/1 have no direct edge. Hidden coordinate2 joins both,
    # and coordinates2..n-1 form a connected chain; no disconnected dummy padding.
    for i in range(1, n - 1):
        J[i, i + 1] = J[i + 1, i] = -0.25
    if n > 2:
        J[0, 2] = J[2, 0] = -0.25
    eta = torch.zeros(n, dtype=torch.float64)
    U = torch.zeros((n, 2), dtype=torch.float64)
    U[0, 0] = U[1, 1] = 1.0
    return J, eta, U.mT.contiguous(), U


def tensor_identity(tensors):
    h = hashlib.sha256()
    for x in tensors:
        data = x.detach().cpu().numpy().astype("<f8", copy=False)
        h.update(blob(dict(shape=list(data.shape), dtype="<f8")))
        h.update(data.tobytes())
    return h.hexdigest()


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
        parent_validation_sha256=PARENT_VALIDATION_SHA,
        parent_measurements_sha256=PARENT_MEASUREMENTS_SHA,
        dimensions=list(DIMENSIONS), history_events=HISTORY_EVENTS, raw_sha256=RAW_SHA,
        update_rank=2, readout_dim=2, live_factors=2,
        matrix_family="4I; edges (1,2)..(n-2,n-1) and (0,2) weight -0.25 when n>2",
        tensor_sha256={str(n): tensor_identity(dimension_tensors(n)) for n in DIMENSIONS},
        n2_parent_export_identity=True, candidate="unchanged ChunkedMemoryBank.read",
        baseline="unchanged incremental MemoryState + full_reference; no history replay",
        shared_retention="complete raw/index/bridge in both arms; compiled capsule retained in baseline",
        warmups=1, repeats=3, numeric_tolerance=TOLERANCE, check_true_preserved=True,
        trace="extra untimed cholesky/cholesky_ex/solve shape traces; wrappers restored",
        no_timing_or_storage_superiority_gate=True, device="cpu", threads=2,
        deterministic_algorithms=True, new_training_steps=0, learned_model_forward_calls=0,
        production_runtime_modified=False, gate_f_candidate=False,
        scope="fixed two-factor numerical reference; not many-factor or natural-language scaling")


def dimension_bank(backend, n):
    require(type(n) is int and n in DIMENSIONS, "unregistered dimension")
    # Template construction is explicitly included in candidate construction time.
    template = backend.c216.build_bank()
    if n == 2:
        return template
    J, eta, Q, U = dimension_tensors(n)
    bridge = type(template.numeric)(J, eta, Q, U, tuple(template.numeric._registry.values()))
    return type(template)(bridge)


class CaptureHelpers:
    """Delegate unchanged C224 helpers; capture actual built state for untimed instrumentation."""
    def __init__(self, helpers):
        self.helpers, self.captured = helpers, None
    def __getattr__(self, name):
        return getattr(self.helpers, name)
    def build_candidate(self, backend, raw):
        self.captured = self.helpers.build_candidate(backend, raw)
        return self.captured


def trace_query(fn):
    trace = []
    with ExitStack() as context:
        for name in ("cholesky", "cholesky_ex", "solve"):
            original = getattr(torch.linalg, name)
            def wrapped(*args, _name=name, _original=original, **kwargs):
                matrix = args[0] if args else kwargs["A"]
                trace.append(dict(operation=_name, matrix_shape=list(matrix.shape)))
                return _original(*args, **kwargs)
            context.enter_context(patch.object(torch.linalg, name, wrapped))
        result = fn()
    return result, trace


def expected_traces(n):
    def entries(names, width):
        return [dict(operation=name, matrix_shape=[width, width]) for name in names]
    return dict(candidate=entries(("cholesky", "cholesky_ex", "solve"), 2),
                symbolic=entries(("cholesky", "solve"), n))


def measure_dimension(parent, n):
    helpers = parent.parent_module()
    backend = helpers.base_module()
    captured = CaptureHelpers(helpers)
    # Injection changes only a local factory; accepted modules are never monkey-patched.
    adapter = SimpleNamespace(memory=backend.memory,
        c216=SimpleNamespace(build_bank=lambda: dimension_bank(backend, n)))
    row, checks, candidate, symbolic = parent.measure(captured, adapter, HISTORY_EVENTS)
    bank, state, _ = captured.captured
    bridge = bank.numeric
    identity = tensor_identity((bridge._J, bridge._eta, bridge._Q, bridge._U))
    full_state = bank.to_memory_state(state)
    cr, ct = trace_query(lambda: bank.read(state))
    sr, st = trace_query(lambda: parent.query_symbolic(bridge, full_state))
    supported = cr.status.value == sr.status.value == "SUPPORTED"
    error = float(torch.max(torch.abs(cr.value - sr.value)).item()) if supported else None
    row.update(numeric_dimension=n, update_rank=bridge.update_rank, readout_dim=bridge.readout_dim,
        actual_variable_dim=bridge.variable_dim, matrix_tensor_sha256=identity,
        candidate_linalg_trace=ct, symbolic_linalg_trace=st,
        instrumented_supported=supported, instrumented_max_abs_error=error)
    return row, checks, candidate, symbolic


def row_gate(row, parent):
    n = row["numeric_dimension"]
    if n not in DIMENSIONS:
        return False
    traces = expected_traces(n)
    return (parent.row_gate(row) and row["history_events"] == HISTORY_EVENTS
        and row["raw_sha256"] == RAW_SHA and row["actual_variable_dim"] == n
        and row["update_rank"] == row["readout_dim"] == 2
        and row["matrix_tensor_sha256"] == tensor_identity(dimension_tensors(n))
        and row["candidate_linalg_trace"] == traces["candidate"]
        and row["symbolic_linalg_trace"] == traces["symbolic"]
        and row["instrumented_supported"] is True
        and row["instrumented_max_abs_error"] is not None
        and row["instrumented_max_abs_error"] <= TOLERANCE)


def parent_anchor(rows, parent):
    require(isinstance(rows, list) and len(rows) == len(parent.SIZES), "parent measurements incomplete")
    require([r["history_events"] for r in rows] == list(parent.SIZES), "parent size order")
    require(all(parent.row_gate(r) for r in rows), "parent measurement invalid")
    return next(r for r in rows if r["history_events"] == HISTORY_EVENTS)


def anchor_equal(row, anchor):
    return all(row[key] == anchor[key] for key in ("candidate_files", "symbolic_files"))


def summarize(rows, parent):
    return dict(dimensions=[r["numeric_dimension"] for r in rows],
        all_quality_parity=all(r["quality_pass"] and r["symbolic_state_equal"] for r in rows),
        audit_pass=all(row_gate(r, parent) for r in rows),
        storage_delta_bytes=[r["storage_delta_bytes"] for r in rows],
        query_median_ratio_h1h2_over_symbolic=[r["candidate_query_median_ns"]/max(1,r["symbolic_query_median_ns"]) for r in rows],
        raw_query_bytes_candidate=[r["candidate_query_trials"][0]["raw_bytes"] for r in rows],
        raw_query_bytes_symbolic=[r["symbolic_query_trials"][0]["raw_bytes"] for r in rows],
        candidate_solve_dimensions=[r["candidate_linalg_trace"][-1]["matrix_shape"][0] for r in rows],
        symbolic_solve_dimensions=[r["symbolic_linalg_trace"][-1]["matrix_shape"][0] for r in rows],
        new_training_steps=0, learned_model_forward_calls=0)


def gate(s):
    return (s.get("dimensions") == list(DIMENSIONS) and s.get("audit_pass") is True
        and s.get("all_quality_parity") is True and s.get("n2_parent_export_parity") is True
        and s.get("new_training_steps") == s.get("learned_model_forward_calls") == 0)


def verify_archive(path, rows):
    expected = {f"{r['numeric_dimension']}/{arm}/{name}":item for r in rows
        for arm,key in (("candidate","candidate_files"),("symbolic","symbolic_files"))
        for name,item in r[key].items()}
    with zipfile.ZipFile(path) as archive:
        require(len(archive.namelist()) == len(expected) and set(archive.namelist()) == set(expected),
                "archive members drift")
        for name,item in expected.items():
            data = archive.read(name)
            require(len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"],
                    "archive byte identity drift")


def precheck(c225_summary, root):
    parent = parent_module(); helpers = parent.parent_module(); backend = helpers.base_module()
    a = backend.audit; root = Path(root)
    require(a.sha(c225_summary) == PARENT_SHA, "C225 summary changed")
    p = a.read_json(c225_summary); parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS"
            and parent.gate(p["validation_summary"]), "wrong accepted C225")
    require(len(p["source_blobs"]) == 190 and len(p["input_sha256"]) == 244, "parent counts")
    pins, protected = dict(p["source_blobs"]), dict(p["input_sha256"])
    for path,wanted in protected.items():
        require(Path(path).is_file() and a.sha(path) == wanted, "changed inherited input:"+path)
    for path,wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+path).decode().strip() == wanted, "changed parent source:"+path)
    protected[str(Path(c225_summary).resolve())] = PARENT_SHA
    seen = set()
    for item in p["artifacts"]:
        path = a.safe_child(Path(c225_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path) == item["sha256"]
                and path.stat().st_size == item["serialized_bytes"], "parent artifact changed")
        protected[str(path.resolve())] = item["sha256"]
        expected = {"validation-summary.json":PARENT_VALIDATION_SHA,"measurements.json":PARENT_MEASUREMENTS_SHA}
        if item["file"] in expected:
            require(item["sha256"] == expected[item["file"]], "parent deciding artifact changed")
            seen.add(item["file"])
    require(len(seen) == 2, "parent deciding artifacts missing")
    parent_anchor(a.read_json(Path(c225_summary).resolve().parent/"measurements.json"),parent)
    require(parent.REPEATS == 3 and parent.WARMUPS == 1 and parent.TOLERANCE == TOLERANCE,
            "parent measurement protocol drift")
    for path in OWN:
        require(path not in pins, "OWN collides with accepted source")
        pins[path] = a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    dependencies = tuple(backend.DIRECT_REPO_DEPENDENCIES) + (
        "fold_lm/v05_benchmarks/gate_f_c220_frozen_learned_stack.py",
        "fold_lm/v05/memory_dispatch.py", "fold_lm/v05_benchmarks/gate_f_c221_live_coverage_dispatch.py",
        "fold_lm/v05_benchmarks/gate_f_c222_withdrawal_lifecycle.py",
        "fold_lm/v05/memory_request_lease.py", "fold_lm/v05_benchmarks/gate_f_c223_request_freshness.py",
        "fold_lm/v05/state.py", "fold_lm/capsule.py",
        "fold_lm/v05_benchmarks/gate_f_c224_history_cost_audit.py",
        "fold_lm/v05_benchmarks/gate_f_c225_stateful_baseline.py")
    require(len(dependencies) == len(set(dependencies)) == 24 and all(x in pins for x in dependencies),
            "unpinned direct dependency")
    protected.update(a.protect_tree_files(root,pins))
    require(len(pins) == 196 and len(protected) == 256, "C226 protection counts")
    require(digest(manifest()) == MANIFEST_SHA, "C226 manifest drift")
    return p,pins,protected


def regression_modules(root):
    names = parent_module().regression_modules(root)
    require(len(names) == len(set(names)) == 110, "parent module count")
    return names + ["tests_lm.test_v05_c226_dimension_scaling"]


def regression_suite(root):
    helper = parent_module().parent_module().base_module().c205
    tests = list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    excluded = helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
    ids = [t.id() for t in tests]
    require(all(ids.count(x) == 1 for x in excluded), "historical exclusion identity")
    kept = [t for t in tests if t.id() not in excluded]
    require(len(tests) == 2530 and len(kept) == 2529, "C226 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE
            and p["diagnostic_execution_valid"] is True, "C226 identity")
    require(len(p["source_blobs"]) == 196 and len(p["input_sha256"]) == 256
            and len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS, "C226 coverage")
    s = p["validation_summary"]
    require(s["dimensions"] == list(DIMENSIONS), "incomplete dimension study")
    require(p["status"] == ("PASS" if gate(s) else "FAIL"), "C226 verdict drift")
    require(p["gate_f_candidate"] is False and p["production_runtime_modified"] is False
            and p["network_calls"] == 0, "scope drift")


def run(*, c225_summary, output_dir, expected_head):
    parent = parent_module(); a = parent.parent_module().base_module().audit
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip() == expected_head, "HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss", "branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(), "dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    _,pins,protected = precheck(c225_summary,root)
    anchor = parent_anchor(a.read_json(Path(c225_summary).resolve().parent/"measurements.json"),parent)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    rows,quality = [],[]
    with zipfile.ZipFile(out/"dimension-exports.zip","w",compression=zipfile.ZIP_STORED) as archive:
        for n in DIMENSIONS:
            row,checks,candidate,symbolic = measure_dimension(parent,n)
            rows.append(row); quality.append(dict(numeric_dimension=n,trials=checks))
            for arm,files in (("candidate",candidate),("symbolic",symbolic)):
                for name,data in files.items():
                    archive.writestr(f"{n}/{arm}/{name}",data)
    verify_archive(out/"dimension-exports.zip",rows)
    summary = summarize(rows,parent)
    summary["n2_parent_export_parity"] = anchor_equal(rows[0],anchor)
    for name,value in (("dimension-plan.json",manifest()),("measurements.json",rows),
                       ("quality-checks.json",quality),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size)
                 for name in sorted(OUTPUTS)]
    guard(); precheck(c225_summary,root)
    for path,wanted in protected.items():
        require(a.sha(path) == wanted, "protected input changed:"+path)
    result = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if gate(summary) else "FAIL",diagnostic_execution_valid=True,
        C225_summary_sha256=PARENT_SHA,source_blobs=pins,input_sha256=protected,artifacts=artifacts,
        validation_summary=summary,gate_f_candidate=False,production_runtime_modified=False,network_calls=0,
        limitations=["audit PASS is not speed or storage superiority",
            "two live factors, rank2 and readout2; no many-factor or learned-language conclusion",
            "coupled sparse SPD input is handled by unchanged dense full_reference baseline",
            "same full bridge including unused compiled capsule retained in baseline",
            "temporary n2 template setup included in higher-dimensional candidate build time",
            "canonical export/reachable data, not native checkpoint or process peaks",
            "no safety-check removal, optimization, training or Gate F claim"])
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C226 RESULT ===",flush=True); print(blob(result).decode(),flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("c225-summary","output-dir"):
        parser.add_argument("--"+arg,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
