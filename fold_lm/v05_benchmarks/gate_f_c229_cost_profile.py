"""C229: function-level attribution of the unchanged C228 update/query workload.

Profiler times are perturbed diagnostics, not speed comparisons or savings estimates.
"""
from __future__ import annotations

import argparse
import cProfile
import hashlib
import json
import math
from pathlib import Path
import sys
import time
from types import SimpleNamespace
import unittest

import torch

EXPERIMENT_ID = "C229-v5f-update-query-function-profile"
STAGE = "V5-F-UPDATE-QUERY-FUNCTION-PROFILE"
BASE = "3d35ba0af1a4d18a7702fb9d02575eec415f0bfc"
PARENT_EXECUTION = "0b78d33987d0e123efff58675693c4f19b81953e"
PARENT_SHA = "44ddf79b6ae1aadb5fb28e37e8528e40c1384b13a152283badbb9eb1be20e9a6"
PARENT_VALIDATION_SHA = "29779710b3826659244ea89f3c57f8dffdc0b824fe0247a205150b63ce8f617b"
PARENT_MEASUREMENTS_SHA = "36bf474db858daf9ccb6a01f5b13d4980edf1dda904c5d9c7bfa124501eb1aab"
DIMENSIONS, BURSTS = (2,16,64,256), (1,4,16)
UPDATES, TOLERANCE = 12, 1e-10
MANIFEST_SHA = "3f9ce8c054db73843455447d6dc74426be570e50857cc220a3927f8777bd3723"
PHASES = ("candidate_update", "candidate_query", "cached_update", "cached_query")
OWN = (
    "fold_lm/v05_benchmarks/gate_f_c229_cost_profile.py",
    "tests_lm/test_v05_c229_cost_profile.py",
    "tools/run_c229.ps1", "tools/invoke_c229.ps1",
    "docs/experiment-ledger-addendum-c229-preregistration.md",
    "docs/v5f-update-query-function-profile-v0.1.md",
)
OUTPUTS = {"profile-plan.json", "measurements.json", "function-profiles.json",
           "quality-checks.json", "validation-summary.json"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),
                       allow_nan=False)+"\n").encode("utf-8")


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import gate_f_c228_update_query_cost as parent
    return parent


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,
        parent_validation_sha256=PARENT_VALIDATION_SHA,
        parent_measurements_sha256=PARENT_MEASUREMENTS_SHA,
        dimensions=list(DIMENSIONS),queries_per_update=list(BURSTS),updates=UPDATES,
        initial_events=32,complete_events=44,live_factors=2,update_rank=2,readout_dim=2,
        cells=12,trajectories_per_cell=2,mode_order=["unprofiled_control","profiled"],
        profiler="stdlib cProfile; four separate phase accumulators; builtins and subcalls enabled",
        phases=list(PHASES),boundary="raw/index append + apply/commit or rhs refresh; query batches",
        excluded="initial setup, correctness oracle, serialization, report generation",
        output="complete function records with primitive/total calls and self/cumulative ns",
        attribution="rank by self time; never sum nested cumulative times",
        gate="current answers/state/provenance and exact parent final exports; profiler-call counts",
        tolerance=TOLERANCE,device="cpu",threads=2,deterministic_algorithms=True,
        new_training_steps=0,production_runtime_modified=False,gate_f_candidate=False,
        performance_superiority_required=False,profiling_time_is_speed_evidence=False,
        scope="diagnose unchanged two-factor bias-only workload; no optimization or new task")


class PhaseRecorder:
    """Run real callbacks; optionally profile. Refuse to replace an existing profiler."""
    def __init__(self, enabled):
        require(type(enabled) is bool,"enabled must be bool")
        self.enabled = enabled
        self.profiler = cProfile.Profile() if enabled else None
        self.invocations = self.elapsed_ns = 0

    def call(self, fn):
        require(sys.getprofile() is None,"another profiler is active")
        self.invocations += 1
        start = time.perf_counter_ns()
        try:
            return self.profiler.runcall(fn) if self.enabled else fn()
        finally:
            self.elapsed_ns += time.perf_counter_ns()-start
            if self.profiler is not None:
                self.profiler.disable()
            require(sys.getprofile() is None,"profiler was not restored")

    def report(self):
        rows = []
        for entry in self.profiler.getstats() if self.profiler is not None else ():
            code = entry.code
            if isinstance(code,str):
                filename,line,name = "<native>",0,code
            else:
                filename = code.co_filename.replace("\\","/")
                for marker in ("/fold_lm/", "/tests_lm/"):
                    if marker in filename:
                        filename = filename[filename.rfind(marker)+1:]
                        break
                else:
                    filename = "<external>/"+filename.rsplit("/",1)[-1]
                line,name = code.co_firstlineno,code.co_qualname
            rows.append(dict(file=filename,line=line,function=name,calls=entry.callcount,
                primitive_calls=entry.callcount-entry.reccallcount,
                self_ns=round(entry.inlinetime*1e9),cumulative_ns=round(entry.totaltime*1e9)))
        rows.sort(key=lambda r:(-r["self_ns"],r["file"],r["line"],r["function"]))
        return dict(enabled=self.enabled,invocations=self.invocations,
                    observed_wall_ns=self.elapsed_ns,self_total_ns=sum(r["self_ns"] for r in rows),
                    functions=rows)


def function_calls(report, suffix, name):
    return sum(r["calls"] for r in report["functions"]
               if r["file"].endswith(suffix) and r["function"] == name)


def report_valid(report, enabled):
    rows = report.get("functions",[])
    return (report.get("enabled") is enabled and report.get("invocations") == UPDATES
        and report.get("observed_wall_ns",-1) >= 0
        and bool(rows) == enabled
        and report.get("self_total_ns") == sum(r["self_ns"] for r in rows)
        and all(r["calls"] >= r["primitive_calls"] >= 0 and r["self_ns"] >= 0
                and r["cumulative_ns"] >= r["self_ns"] for r in rows))


def parent_adapter(rows, parent):
    require(isinstance(rows,list) and len(rows) == 12,"parent cells incomplete")
    require([[r["numeric_dimension"],r["queries_per_update"]] for r in rows]
            == [[n,q] for n in DIMENSIONS for q in BURSTS],"parent cell identity/order")
    require(all(parent.row_gate(r) for r in rows),"parent measurement gate failed")
    return {(r["numeric_dimension"],r["queries_per_update"]):r for r in rows}


def trajectory(parent,n,burst,profiled):
    """Same C228 states and operations, with profiling limited to four measured phases."""
    factor=parent.parent_module(); dimension=factor.parent_module()
    symbolic=dimension.parent_module(); helpers=symbolic.parent_module()
    backend=helpers.base_module()
    prefix,tail,complete=parent.ledger_parts(helpers)
    bank=dimension.dimension_bank(backend,n)
    adapter=SimpleNamespace(memory=backend.memory,c216=SimpleNamespace(build_bank=lambda:bank))
    bank,state,_=helpers.build_candidate(adapter,prefix)
    current,_=symbolic.build_symbolic(adapter,prefix,helpers)
    cache=parent.prepare(factor,bank.numeric,current)
    original_L=cache.core.L
    raw={a:prefix for a in ("candidate","cached")}
    indices={a:helpers.source_index(prefix) for a in raw}
    phases={name:PhaseRecorder(profiled) for name in PHASES}
    checks=[]
    for step,line in enumerate(tail):
        def candidate_update():
            nonlocal state
            raw["candidate"],event=parent.append_evidence(raw["candidate"],indices["candidate"],line)
            state,read=bank.apply(state,helpers.memory_op(backend.memory,state,event))
            require(read is None,"mutation returned query")
            state,status=bank.commit(state)
            require(status.value in ("COMMITTED","NOOP"),"bad candidate commit")
        def cached_update():
            nonlocal current,cache
            raw["cached"],event=parent.append_evidence(raw["cached"],indices["cached"],line)
            current,read=backend.memory.apply_memory_op(current,helpers.memory_op(backend.memory,current,event))
            require(read is None,"mutation returned query")
            cache=parent.refresh(factor,cache,bank.numeric,current)
        responses={}
        order=("candidate","cached") if step%2 == 0 else ("cached","candidate")
        for arm in order:
            phases[arm+"_update"].call(candidate_update if arm == "candidate" else cached_update)
            # Audit-only snapshots are outside all profiling/timing regions.
            before=helpers.blob(helpers.canonical(dict(state=state,current=current)))
            if arm == "candidate":
                responses[arm]=phases[arm+"_query"].call(lambda:[bank.read(state).value for _ in range(burst)])
            else:
                responses[arm]=phases[arm+"_query"].call(lambda:[factor.query_cached(cache.core,bank.numeric,current) for _ in range(burst)])
            unchanged=before == helpers.blob(helpers.canonical(dict(state=state,current=current)))
            require(unchanged,"query mutated state")
        reference=bank.numeric.full_reference(current)
        values=responses["candidate"]+responses["cached"]
        finite=all(isinstance(v,torch.Tensor) and bool(torch.isfinite(v).all()) for v in values)
        error=max(float(torch.max(torch.abs(v-reference.value))) for v in values) if finite and reference.value is not None else None
        equal=helpers.canonical(bank.to_memory_state(state)) == helpers.canonical(current)
        provenance=True
        for record in current.records:
            span=indices["cached"].get(record.provenance.source_id)
            if span is None:
                provenance=False
                continue
            event=json.loads(raw["cached"][slice(*span)])
            provenance &= (event["scope"],event["factor"],event["relation"]) == (record.scope_id,record.factor_id,record.relation_key)
        checks.append(dict(step=step+1,outputs=2*burst,max_abs_error=error,
            state_equal=equal,provenance=bool(provenance),factor_reused=cache.core.L is original_L,
            passed=bool(equal and provenance and reference.status.value == "SUPPORTED" and finite
                and error <= TOLERANCE and cache.core.L is original_L)))
    require(raw["candidate"] == raw["cached"] == complete,"raw mismatch")
    require(indices["candidate"] == indices["cached"],"index mismatch")
    helpers.validate_index(complete,indices["candidate"])
    cf,sf=symbolic.make_exports(helpers,bank,state,current,complete,indices["candidate"])
    cached=dict(sf,**{"rhs-reuse-cache.json":parent.cache_export(factor,cache,helpers)})
    return dict(checks=checks,quality_pass=all(x["passed"] for x in checks),
        retained_inventory={a:symbolic.inventory(f) for a,f in (("candidate",cf),("cached",cached))},
        reports={k:v.report() for k,v in phases.items()},profiler_restored=sys.getprofile() is None)


def profile_cell(parent,n,q,anchor):
    off=trajectory(parent,n,q,False)
    on=trajectory(parent,n,q,True)
    reports=on["reports"]
    observed=dict(
        candidate_reads=function_calls(reports["candidate_query"],"memory_bank.py","ChunkedMemoryBank.read"),
        cached_reads=function_calls(reports["cached_query"],"gate_f_c227_factor_reuse.py","query_cached"),
        candidate_applies=function_calls(reports["candidate_update"],"memory_bank.py","ChunkedMemoryBank.apply"),
        cached_refreshes=function_calls(reports["cached_update"],"gate_f_c228_update_query_cost.py","refresh"))
    expected=dict(candidate_reads=UPDATES*q,cached_reads=UPDATES*q,
                  candidate_applies=UPDATES,cached_refreshes=UPDATES)
    reports_ok=all(report_valid(on["reports"][p],True) and report_valid(off["reports"][p],False) for p in PHASES)
    parity=off["retained_inventory"] == on["retained_inventory"] == anchor["retained_inventory"]
    same_answers=(len(off["checks"]) == len(on["checks"]) == UPDATES
                  and off["quality_pass"] and on["quality_pass"])
    row=dict(numeric_dimension=n,queries_per_update=q,parent_stream_ratio=anchor["stream_ratio_h1h2_over_cached"],
        parent_export_parity=parity,all_quality_parity=bool(same_answers),profiles_valid=reports_ok,
        observed_calls=observed,expected_calls=expected,call_counts_pass=observed == expected,
        profiler_restored=off["profiler_restored"] and on["profiler_restored"],
        function_tops={p:reports[p]["functions"][:10] for p in PHASES},
        phase_diagnostics={p:dict(unprofiled_control_wall_ns=off["reports"][p]["observed_wall_ns"],
            profiled_wall_ns=reports[p]["observed_wall_ns"],profile_self_total_ns=reports[p]["self_total_ns"])
            for p in PHASES},profiling_times_are_speed_evidence=False)
    return row,reports,dict(unprofiled=off["checks"],profiled=on["checks"],inventory=on["retained_inventory"])


def row_gate(r):
    return (r["numeric_dimension"] in DIMENSIONS and r["queries_per_update"] in BURSTS
        and all(r.get(k) is True for k in ("parent_export_parity","all_quality_parity","profiles_valid","call_counts_pass","profiler_restored"))
        and r.get("profiling_times_are_speed_evidence") is False)


def summarize(rows):
    return dict(cells=[[r["numeric_dimension"],r["queries_per_update"]] for r in rows],
        audit_pass=all(row_gate(r) for r in rows),parent_export_parity=all(r["parent_export_parity"] for r in rows),
        all_quality_parity=all(r["all_quality_parity"] for r in rows),
        all_call_counts_pass=all(r["call_counts_pass"] for r in rows),
        profiler_restored=all(r["profiler_restored"] for r in rows),new_training_steps=0)


def gate(s):
    return (s.get("cells") == [[n,q] for n in DIMENSIONS for q in BURSTS]
        and all(s.get(k) is True for k in ("audit_pass","parent_export_parity","all_quality_parity","all_call_counts_pass","profiler_restored"))
        and s.get("new_training_steps") == 0)


def precheck(c228_summary,root):
    parent=parent_module(); factor=parent.parent_module(); dim=factor.parent_module()
    sym=dim.parent_module(); helpers=sym.parent_module(); backend=helpers.base_module(); a=backend.audit
    root=Path(root)
    require(a.sha(c228_summary) == PARENT_SHA,"C228 summary changed")
    p=a.read_json(c228_summary); parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS" and parent.gate(p["validation_summary"]),"wrong accepted C228")
    require(len(p["source_blobs"]) == 208 and len(p["input_sha256"]) == 280,"parent coverage")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for path,wanted in protected.items():
        require(Path(path).is_file() and a.sha(path) == wanted,"changed inherited input:"+path)
    for path,wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+path).decode().strip() == wanted,"changed parent source:"+path)
    protected[str(Path(c228_summary).resolve())]=PARENT_SHA
    seen=set()
    for item in p["artifacts"]:
        path=a.safe_child(Path(c228_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path) == item["sha256"] and path.stat().st_size == item["serialized_bytes"],"parent artifact changed")
        protected[str(path.resolve())]=item["sha256"]
        wanted={"measurements.json":PARENT_MEASUREMENTS_SHA,"validation-summary.json":PARENT_VALIDATION_SHA}
        if item["file"] in wanted:
            require(item["sha256"] == wanted[item["file"]],"parent deciding identity")
            seen.add(item["file"])
    require(len(seen) == 2,"missing parent deciding artifact")
    parent_adapter(a.read_json(Path(c228_summary).resolve().parent/"measurements.json"),parent)
    for path in OWN:
        require(path not in pins,"OWN overlaps parent")
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
        "fold_lm/v05_benchmarks/gate_f_c227_factor_reuse.py",
        "fold_lm/v05_benchmarks/gate_f_c228_update_query_cost.py")
    require(len(dependencies) == len(set(dependencies)) == 27 and all(x in pins for x in dependencies),"unpinned dependency")
    protected.update(a.protect_tree_files(root,pins))
    require(len(pins) == 214 and len(protected) == 292,"C229 protection counts")
    require(digest(manifest()) == MANIFEST_SHA,"manifest drift")
    return p,pins,protected


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names) == len(set(names)) == 113,"parent module count")
    return names+["tests_lm.test_v05_c229_cost_profile"]


def regression_suite(root):
    helper=parent_module().parent_module().parent_module().parent_module().parent_module().base_module().c205
    tests=list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    excluded=helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS; ids=[t.id() for t in tests]
    require(all(ids.count(x) == 1 for x in excluded),"historical exclusion")
    kept=[t for t in tests if t.id() not in excluded]
    require(len(tests) == 2626 and len(kept) == 2625,"C229 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["diagnostic_execution_valid"] is True,"C229 identity")
    require(len(p["source_blobs"]) == 214 and len(p["input_sha256"]) == 292
        and len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS,"C229 coverage")
    require(p["validation_summary"]["cells"] == [[n,q] for n in DIMENSIONS for q in BURSTS],"incomplete C229")
    require(p["status"] == ("PASS" if gate(p["validation_summary"]) else "FAIL"),"C229 verdict")
    require(p["gate_f_candidate"] is False and p["production_runtime_modified"] is False and p["network_calls"] == 0,"scope drift")


def run(*,c228_summary,output_dir,expected_head):
    parent=parent_module()
    a=parent.parent_module().parent_module().parent_module().parent_module().base_module().audit
    root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip() == expected_head,"HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    _,pins,protected=precheck(c228_summary,root)
    anchors=parent_adapter(a.read_json(Path(c228_summary).resolve().parent/"measurements.json"),parent)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    rows,profiles,quality=[],[],[]
    for n in DIMENSIONS:
        for q in BURSTS:
            row,profile,checks=profile_cell(parent,n,q,anchors[(n,q)])
            rows.append(row)
            profiles.append(dict(numeric_dimension=n,queries_per_update=q,phases=profile))
            quality.append(dict(numeric_dimension=n,queries_per_update=q,**checks))
    summary=summarize(rows)
    for name,value in (("profile-plan.json",manifest()),("measurements.json",rows),
        ("function-profiles.json",profiles),("quality-checks.json",quality),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard();precheck(c228_summary,root)
    for path,wanted in protected.items():require(a.sha(path) == wanted,"changed input:"+path)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if gate(summary) else "FAIL",diagnostic_execution_valid=True,C228_summary_sha256=PARENT_SHA,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        production_runtime_modified=False,gate_f_candidate=False,network_calls=0,
        limitations=["cProfile perturbs latency; function times are diagnostic, not speed evidence",
            "self times avoid nested cumulative double counting; profiler overhead is not subtracted",
            "same two-factor bias-only workload; no optimization, broader task or Gate F claim"])
    validate_result(result);(out/"summary.json").write_bytes(blob(result))
    print("=== C229 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("c228-summary","output-dir"):p.add_argument("--"+arg,type=Path,required=True)
    p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__ == "__main__":
    main()
