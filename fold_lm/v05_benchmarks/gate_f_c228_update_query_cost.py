"""C228: bias-only update/query costs; audit PASS is not performance superiority."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import statistics
import time
from types import SimpleNamespace
import unittest
import zipfile

import torch

EXPERIMENT_ID = "C228-v5f-bias-update-query-amortization"
STAGE = "V5-F-BIAS-UPDATE-QUERY-AMORTIZATION"
BASE = "0972ccf71ffaabfb3b45ca84489758be9a4c51cf"
PARENT_EXECUTION = "1ada3a45be61e524cf09ff9fa7c6d56efcbf29ee"
PARENT_SHA = "4e2a5282f5923b80272afd6476bf2a5ff62a672825cee6d442b0bac4325f9b75"
PARENT_VALIDATION_SHA = "bbb5ffefd2a0aad3c5e332ba1f50e2a87e15463267129bf657512a044c198d05"
PARENT_MEASUREMENTS_SHA = "68234a510756ac5d80a5a1ee770a393ad8dce656a8c395ce8ca73be80b3eac16"
DIMENSIONS, BURSTS = (2, 16, 64, 256), (1, 4, 16)
PREFIX_EVENTS, UPDATES, WARMUPS, REPEATS = 32, 12, 1, 3
TOLERANCE = 1e-10
PREFIX_SHA = "735d3c800017091f5dce4a91603ff40c61d6e8c24baa5c7ed504735e2d82f921"
LEDGER_SHA = "493140c7cbc874c90066da8defe3785a0b667f6c2e2edbdbcc2b55bd5e595f11"
MANIFEST_SHA = "bd9e450beebb183dd953928a1e5894bcbd76f33aa25de3bcca27ef05277b1096"
OWN = (
    "fold_lm/v05_benchmarks/gate_f_c228_update_query_cost.py",
    "tests_lm/test_v05_c228_update_query_cost.py",
    "tools/run_c228.ps1", "tools/invoke_c228.ps1",
    "docs/experiment-ledger-addendum-c228-preregistration.md",
    "docs/v5f-bias-update-query-amortization-v0.1.md",
)
OUTPUTS = {"update-plan.json", "update-exports.zip", "measurements.json",
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
    from fold_lm.v05_benchmarks import gate_f_c227_factor_reuse as parent
    return parent


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
        parent_validation_sha256=PARENT_VALIDATION_SHA,
        parent_measurements_sha256=PARENT_MEASUREMENTS_SHA,
        dimensions=list(DIMENSIONS), queries_per_update=list(BURSTS),
        initial_events=PREFIX_EVENTS, updates=UPDATES, prefix_sha256=PREFIX_SHA,
        complete_ledger_sha256=LEDGER_SHA, update_kind="beta REPLACE; bias-only; W invariant",
        arms=["h1_h2", "checked_factor_rhs_refresh"],
        baseline="reuse checked full Cholesky iff aggregate W equal; refresh rhs/state binding",
        raw_and_index="both retain same complete ledger and append source byte ranges",
        timings="one warm trajectory plus three measured; alternating arm order per update",
        warmups=WARMUPS, repeats=REPEATS, tolerance=TOLERANCE,
        cold_setup="shared numeric bank construction counted in both cold totals",
        total_metric="update plus query phases; setup recorded separately and cold-inclusive",
        validation="every query versus untimed full_reference; state/provenance after every update",
        traces="untimed replay of all12 rhs refreshes; checked preparation and final query shapes",
        original_initial_exports_equal=True, all_retained_data_counted=True,
        new_training_steps=0, learned_model_forward_calls=0,
        production_runtime_modified=False, gate_f_candidate=False,
        superiority_required_for_pass=False, device="cpu", threads=2,
        deterministic_algorithms=True,
        scope="two-factor bias-only updates; not matrix-changing updates, answer caching or concurrency")


@dataclass
class RHSCache:
    core: object
    aggregate_W: torch.Tensor
    matrix_stamp: tuple


def prepare(parent, bridge, state):
    core = parent.prepare_cache(bridge, state)
    status, W, _, _ = bridge._aggregate(state)
    require(status.value == "SUPPORTED", "cache outside capability")
    retained = W.detach().clone()
    return RHSCache(core, retained, parent.tensor_stamps((retained,)))


def refresh(parent, cache, bridge, state):
    require(isinstance(cache, RHSCache), "wrong rhs cache")
    core = cache.core
    require(core.bridge is bridge, "changed bridge binding")
    require(parent.tensor_stamps(parent.bridge_tensors(bridge)+(core.L,core.rhs)) == core.stamps,
            "changed cache/base tensor")
    require(parent.tensor_stamps((cache.aggregate_W,)) == cache.matrix_stamp, "changed matrix guard")
    status, W, bias, _ = bridge._aggregate(state)
    require(status.value == "SUPPORTED" and torch.equal(W, cache.aggregate_W),
            "matrix-changing update is outside this comparator")
    rhs = (bridge._eta + bridge._U @ bias).detach().clone()
    require(bool(torch.isfinite(rhs).all()), "nonfinite refreshed rhs")
    updated = parent.FactorCache(state, bridge, core.L, rhs,
        parent.tensor_stamps(parent.bridge_tensors(bridge)+(core.L,rhs)))
    return RHSCache(updated, cache.aggregate_W, cache.matrix_stamp)


def cache_export(parent, cache, helpers):
    return blob(dict(schema="fold-c228-rhs-reuse-audit-v1",
        core=json.loads(parent.cache_payload(cache.core, helpers)),
        aggregate_W=helpers.canonical(cache.aggregate_W),
        matrix_versions=[v for _,v in cache.matrix_stamp]))


def ledger_parts(helpers):
    raw = helpers.ledger(PREFIX_EVENTS+UPDATES)
    lines = raw.splitlines(keepends=True)
    prefix = b"".join(lines[:PREFIX_EVENTS])
    require(len(lines) == PREFIX_EVENTS+UPDATES, "ledger count")
    require(hashlib.sha256(prefix).hexdigest() == PREFIX_SHA, "prefix identity")
    require(hashlib.sha256(raw).hexdigest() == LEDGER_SHA, "ledger identity")
    tail = lines[PREFIX_EVENTS:]
    for line in tail:
        event = json.loads(line)
        require(event["kind"] == "REPLACE" and event["factor"] == "beta", "wrong update")
    return prefix, tail, raw


def append_evidence(raw, index, line):
    event = json.loads(line)
    require(event["source_id"] not in index, "duplicate appended source")
    index[event["source_id"]] = (len(raw),len(raw)+len(line))
    return raw+line, event


def anchor_equal(inventories, anchor):
    return all(inventories[a] == anchor[a+"_files"] for a in ("candidate","symbolic"))


def parent_adapter(rows, parent):
    require(isinstance(rows,list) and len(rows) == len(DIMENSIONS), "parent rows incomplete")
    require([r["numeric_dimension"] for r in rows] == list(DIMENSIONS), "parent order")
    require(all(parent.row_gate(r) for r in rows), "parent measurement gate")
    return {r["numeric_dimension"]:r for r in rows}


def timed(fn):
    start = time.perf_counter_ns()
    value = fn()
    return value, time.perf_counter_ns()-start


def trajectory(parent, n, burst, trial):
    dimension = parent.parent_module()
    symbolic = dimension.parent_module()
    helpers = symbolic.parent_module()
    backend = helpers.base_module()
    prefix, updates, complete = ledger_parts(helpers)
    bank, common_ns = timed(lambda:dimension.dimension_bank(backend,n))
    adapter = SimpleNamespace(memory=backend.memory, c216=SimpleNamespace(build_bank=lambda:bank))
    (index, index_ns) = timed(lambda:helpers.source_index(prefix))
    (built, candidate_init_ns) = timed(lambda:helpers.build_candidate(adapter,prefix))
    bank,state,_ = built
    (built, symbolic_init_ns) = timed(lambda:symbolic.build_symbolic(adapter,prefix,helpers))
    current,_ = built
    (cache, cache_prepare_ns) = timed(lambda:prepare(parent,bank.numeric,current))
    cf,sf = symbolic.make_exports(helpers,bank,state,current,prefix,index)
    initial = dict(candidate=symbolic.inventory(cf),symbolic=symbolic.inventory(sf))
    raw_by_arm = dict(candidate=prefix,cached=prefix)
    indices = {arm:dict(index) for arm in raw_by_arm}
    update_ns = dict(candidate=0,cached=0)
    query_ns = dict(candidate=0,cached=0)
    checks = []
    initial_L = cache.core.L
    initial_current, audit_states = current, []
    for step,line in enumerate(updates):
        order = ("candidate","cached") if (trial+step)%2 == 0 else ("cached","candidate")
        responses = {}
        for arm in order:
            started = time.perf_counter_ns()
            raw_by_arm[arm], event = append_evidence(raw_by_arm[arm],indices[arm],line)
            if arm == "candidate":
                state, read = bank.apply(state,helpers.memory_op(backend.memory,state,event))
                require(read is None,"mutation returned read")
                state, status = bank.commit(state)
                require(status.value in ("NOOP","COMMITTED"),"bad commit")
            else:
                current, read = backend.memory.apply_memory_op(
                    current,helpers.memory_op(backend.memory,current,event))
                require(read is None,"symbolic mutation returned read")
                cache = refresh(parent,cache,bank.numeric,current)
            update_ns[arm] += time.perf_counter_ns()-started
            started = time.perf_counter_ns()
            responses[arm] = ([bank.read(state).value for _ in range(burst)] if arm == "candidate"
                else [parent.query_cached(cache.core,bank.numeric,current) for _ in range(burst)])
            query_ns[arm] += time.perf_counter_ns()-started
        # Validation is not included in either arm's timing samples.
        audit_states.append(current)
        reference = bank.numeric.full_reference(current)
        supported = reference.status.value == "SUPPORTED"
        all_values = responses["candidate"]+responses["cached"]
        finite = all(isinstance(v,torch.Tensor) and bool(torch.isfinite(v).all()) for v in all_values)
        error = max(float(torch.max(torch.abs(v-reference.value))) for v in all_values) if supported and finite else None
        equal = helpers.canonical(bank.to_memory_state(state)) == helpers.canonical(current)
        provenance = True
        for record in current.records:
            span = indices["cached"].get(record.provenance.source_id)
            if span is None:
                provenance = False
                continue
            event = json.loads(raw_by_arm["cached"][slice(*span)])
            provenance &= (event["scope"],event["factor"],event["relation"]) == (
                record.scope_id,record.factor_id,record.relation_key)
        checks.append(dict(step=step+1,query_results_checked=len(all_values),
            state_equal=equal,provenance=bool(provenance),factor_reused=cache.core.L is initial_L,
            max_abs_error=error,passed=bool(equal and provenance and supported and finite
                and error <= TOLERANCE and cache.core.L is initial_L)))
    require(raw_by_arm["candidate"] == raw_by_arm["cached"] == complete,"raw retention changed")
    require(indices["candidate"] == indices["cached"],"index differs")
    helpers.validate_index(complete,indices["candidate"])
    before = helpers.blob(helpers.canonical(dict(state=state,current=current)))
    audit_cache, prepare_trace = parent.trace_call(lambda:prepare(parent,bank.numeric,initial_current))
    def audit_refreshes():
        replay_cache = audit_cache
        applied = 0
        for snapshot in audit_states:
            replay_cache = refresh(parent,replay_cache,bank.numeric,snapshot)
            applied += 1
        return applied
    refresh_count, refresh_trace = parent.trace_call(audit_refreshes)
    _, candidate_trace = parent.trace_call(lambda:bank.read(state))
    _, cached_trace = parent.trace_call(lambda:parent.query_cached(cache.core,bank.numeric,current))
    unchanged = before == helpers.blob(helpers.canonical(dict(state=state,current=current)))
    start = time.perf_counter_ns()
    cf,sf = symbolic.make_exports(helpers,bank,state,current,complete,indices["candidate"])
    cached_files = dict(sf,**{"rhs-reuse-cache.json":cache_export(parent,cache,helpers)})
    export_ns = time.perf_counter_ns()-start
    files = dict(candidate=cf,cached=cached_files)
    counts = dict(updates_per_arm=UPDATES,queries_per_arm=UPDATES*burst,
                  quality_results_checked=sum(x["query_results_checked"] for x in checks),
                  rhs_refreshes=refresh_count,
                  initial_factorizations=sum(x["operation"] == "cholesky" for x in prepare_trace),
                  update_refactorizations=sum(x["operation"] in ("cholesky","cholesky_ex","solve") for x in refresh_trace))
    phases = dict(common_numeric_setup_ns=common_ns,index_build_ns=index_ns,
        candidate_init_ns=candidate_init_ns,cached_init_ns=symbolic_init_ns+cache_prepare_ns,
        cache_prepare_ns=cache_prepare_ns,export_ns=export_ns)
    for arm in ("candidate","cached"):
        phases[arm+"_update_ns"] = update_ns[arm]
        phases[arm+"_query_ns"] = query_ns[arm]
        phases[arm+"_stream_ns"] = update_ns[arm]+query_ns[arm]
        phases[arm+"_cold_inclusive_ns"] = phases[arm+"_stream_ns"]+phases[arm+"_init_ns"]+common_ns+index_ns
    return dict(phases=phases,counts=counts,quality=all(x["passed"] for x in checks),
        checks=checks,initial_inventory=initial,query_state_unchanged=unchanged,
        refresh_trace=refresh_trace,prepare_trace=prepare_trace,candidate_query_trace=candidate_trace,cached_query_trace=cached_trace,
        files=files,inventory={a:symbolic.inventory(f) for a,f in files.items()},
        resident=dict(candidate=helpers.resident_estimate(dict(bank=bank,state=state,raw=complete,index=indices["candidate"])),
            cached=helpers.resident_estimate(dict(bridge=bank.numeric,state=current,cache=cache,raw=complete,index=indices["cached"]))),
        extra_cache_tensor_bytes=cache.core.L.untyped_storage().nbytes()+cache.core.rhs.untyped_storage().nbytes()+cache.aggregate_W.untyped_storage().nbytes())


def measure_cell(parent,n,burst,anchor):
    require(n in DIMENSIONS and burst in BURSTS,"unregistered cell")
    trials, quality, inventories = [],[],[]
    last = None
    for trial in range(WARMUPS+REPEATS):
        result = trajectory(parent,n,burst,trial)
        same = anchor_equal(result["initial_inventory"],anchor)
        valid = (same and result["quality"] and result["query_state_unchanged"]
            and result["refresh_trace"] == [] and result["prepare_trace"] == parent.expected_trace(n,"prepare")
            and result["candidate_query_trace"] == parent.expected_trace(n,"candidate")
            and result["cached_query_trace"] == parent.expected_trace(n,"cached"))
        quality.append(dict(trial=trial,warmup=trial<WARMUPS,passed=valid,
                            initial_parent_parity=same,checks=result["checks"]))
        inventories.append(result["inventory"])
        if trial >= WARMUPS:
            trials.append(dict(result["phases"],**result["counts"]))
        last = result
    row = dict(numeric_dimension=n,queries_per_update=burst,trials=trials,
        quality_pass=all(q["passed"] for q in quality),
        initial_parent_parity=all(q["initial_parent_parity"] for q in quality),
        repeat_exports_equal=all(x == inventories[0] for x in inventories),
        retained_inventory=last["inventory"],resident_estimate=last["resident"],
        extra_cache_tensor_bytes=last["extra_cache_tensor_bytes"],
        refresh_trace=last["refresh_trace"],prepare_trace=last["prepare_trace"],cached_query_trace=last["cached_query_trace"],
        candidate_query_trace=last["candidate_query_trace"])
    for arm in ("candidate","cached"):
        row[arm+"_export_bytes"] = sum(x["bytes"] for x in row["retained_inventory"][arm].values())
        for phase in ("update","query","stream","cold_inclusive"):
            row[arm+"_"+phase+"_median_ns"] = statistics.median(t[arm+"_"+phase+"_ns"] for t in trials)
    row["stream_ratio_h1h2_over_cached"] = row["candidate_stream_median_ns"]/max(1,row["cached_stream_median_ns"])
    return row,quality,last["files"]


def row_gate(r):
    n,q = r["numeric_dimension"],r["queries_per_update"]
    inv = r["retained_inventory"]
    return (n in DIMENSIONS and q in BURSTS and r["quality_pass"] is True
        and r["initial_parent_parity"] is True and r["repeat_exports_equal"] is True
        and r["extra_cache_tensor_bytes"] == 8*(n*n+n+4)
        and r["refresh_trace"] == [] and len(r["trials"]) == REPEATS
        and r["prepare_trace"] == [dict(operation="cholesky",matrix_shape=[n,n])]
        and r["cached_query_trace"] == [dict(operation="cholesky_solve",matrix_shape=[n,n])]
        and r["candidate_query_trace"] == [dict(operation=x,matrix_shape=[2,2]) for x in ("cholesky","cholesky_ex","solve")]
        and all(t["updates_per_arm"] == UPDATES and t["queries_per_arm"] == UPDATES*q
            and t["quality_results_checked"] == 2*UPDATES*q and t["rhs_refreshes"] == UPDATES
            and t["initial_factorizations"] == 1 and t["update_refactorizations"] == 0
            and all(t[a+"_stream_ns"] == t[a+"_update_ns"]+t[a+"_query_ns"] for a in inv)
            for t in r["trials"])
        and all(inv["candidate"][k] == inv["cached"][k] for k in ("evidence.ndjson","source-index.json"))
        and "rhs-reuse-cache.json" in inv["cached"]
        and all(r[a+"_export_bytes"] == sum(x["bytes"] for x in inv[a].values()) for a in inv))


def summarize(rows):
    return dict(cells=[[r["numeric_dimension"],r["queries_per_update"]] for r in rows],
        audit_pass=all(row_gate(r) for r in rows),all_quality_parity=all(r["quality_pass"] for r in rows),
        initial_parent_parity=all(r["initial_parent_parity"] for r in rows),
        stream_ratios=[r["stream_ratio_h1h2_over_cached"] for r in rows],
        new_training_steps=0,learned_model_forward_calls=0)


def gate(s):
    return (s.get("cells") == [[n,q] for n in DIMENSIONS for q in BURSTS]
        and s.get("audit_pass") is True and s.get("all_quality_parity") is True
        and s.get("initial_parent_parity") is True and s.get("new_training_steps") == 0)


def verify_archive(path,rows):
    expected = {f"{r['numeric_dimension']}/{r['queries_per_update']}/{arm}/{name}":item
        for r in rows for arm,inv in r["retained_inventory"].items() for name,item in inv.items()}
    with zipfile.ZipFile(path) as archive:
        require(len(archive.namelist()) == len(expected) and set(archive.namelist()) == set(expected),"archive members")
        for name,item in expected.items():
            data = archive.read(name)
            require(len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"],"archive bytes")


def precheck(c227_summary,root):
    parent=parent_module(); dim=parent.parent_module(); sym=dim.parent_module(); helpers=sym.parent_module()
    backend=helpers.base_module(); a=backend.audit; root=Path(root)
    require(a.sha(c227_summary) == PARENT_SHA,"C227 summary changed")
    p=a.read_json(c227_summary); parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS" and parent.gate(p["validation_summary"]),"wrong accepted C227")
    require(len(p["source_blobs"]) == 202 and len(p["input_sha256"]) == 268,"parent counts")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for path,wanted in protected.items():
        require(Path(path).is_file() and a.sha(path) == wanted,"changed inherited input:"+path)
    for path,wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+path).decode().strip() == wanted,"changed parent source:"+path)
    protected[str(Path(c227_summary).resolve())]=PARENT_SHA
    seen=set()
    for item in p["artifacts"]:
        path=a.safe_child(Path(c227_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path) == item["sha256"] and path.stat().st_size == item["serialized_bytes"],"parent artifact changed")
        protected[str(path.resolve())]=item["sha256"]
        expected={"measurements.json":PARENT_MEASUREMENTS_SHA,"validation-summary.json":PARENT_VALIDATION_SHA}
        if item["file"] in expected:
            require(item["sha256"] == expected[item["file"]],"parent deciding identity")
            seen.add(item["file"])
    require(len(seen)==2,"missing parent deciding artifact")
    parent_adapter(a.read_json(Path(c227_summary).resolve().parent/"measurements.json"),parent)
    ledger_parts(helpers)
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
        "fold_lm/v05_benchmarks/gate_f_c226_dimension_scaling.py",
        "fold_lm/v05_benchmarks/gate_f_c227_factor_reuse.py")
    require(len(dependencies)==len(set(dependencies))==26 and all(x in pins for x in dependencies),"unpinned dependency")
    protected.update(a.protect_tree_files(root,pins))
    require(len(pins)==208 and len(protected)==280,"C228 protection counts")
    require(digest(manifest())==MANIFEST_SHA,"manifest drift")
    return p,pins,protected


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==112,"parent module count")
    return names+["tests_lm.test_v05_c228_update_query_cost"]


def regression_suite(root):
    helper=parent_module().parent_module().parent_module().parent_module().base_module().c205
    tests=list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    excluded=helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS; ids=[t.id() for t in tests]
    require(all(ids.count(x)==1 for x in excluded),"historical exclusion")
    kept=[t for t in tests if t.id() not in excluded]
    require(len(tests)==2594 and len(kept)==2593,"C228 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"C228 identity")
    require(len(p["source_blobs"])==208 and len(p["input_sha256"])==280 and len(p["artifacts"])==5
            and {x["file"] for x in p["artifacts"]}==OUTPUTS,"C228 coverage")
    require(p["validation_summary"]["cells"]==[[n,q] for n in DIMENSIONS for q in BURSTS],"incomplete C228")
    require(p["status"]==("PASS" if gate(p["validation_summary"]) else "FAIL"),"C228 verdict drift")
    require(p["gate_f_candidate"] is False and p["production_runtime_modified"] is False and p["network_calls"]==0,"scope drift")


def run(*,c227_summary,output_dir,expected_head):
    parent=parent_module(); a=parent.parent_module().parent_module().parent_module().base_module().audit
    root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    _,pins,protected=precheck(c227_summary,root)
    anchors=parent_adapter(a.read_json(Path(c227_summary).resolve().parent/"measurements.json"),parent)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    rows,quality=[],[]
    with zipfile.ZipFile(out/"update-exports.zip","w",compression=zipfile.ZIP_STORED) as archive:
        for n in DIMENSIONS:
            for q in BURSTS:
                row,checks,files=measure_cell(parent,n,q,anchors[n])
                rows.append(row);quality.append(dict(numeric_dimension=n,queries_per_update=q,trials=checks))
                for arm,contents in files.items():
                    for name,data in contents.items():archive.writestr(f"{n}/{q}/{arm}/{name}",data)
    verify_archive(out/"update-exports.zip",rows)
    summary=summarize(rows)
    for name,value in (("update-plan.json",manifest()),("measurements.json",rows),
                       ("quality-checks.json",quality),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard();precheck(c227_summary,root)
    for path,wanted in protected.items():require(a.sha(path)==wanted,"changed protected input:"+path)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if gate(summary) else "FAIL",diagnostic_execution_valid=True,C227_summary_sha256=PARENT_SHA,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        production_runtime_modified=False,gate_f_candidate=False,network_calls=0,
        limitations=["bias-only matrix-invariant replacements; not general changing relations",
            "full factor/rhs/matrix guard plus raw/index/bridge retained",
            "three descriptive trials; no process peak measurement",
            "answer caching and specialized solvers not implemented; no Gate F claim"])
    validate_result(result);(out/"summary.json").write_bytes(blob(result))
    print("=== C228 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("c227-summary","output-dir"):p.add_argument("--"+arg,type=Path,required=True)
    p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))


if __name__=="__main__":
    main()
