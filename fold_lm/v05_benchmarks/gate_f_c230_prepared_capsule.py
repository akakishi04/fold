"""C230: checked fixed-W reduced preparation reuse on the unchanged C228 workload.

Unprofiled original/prepared/full-factor arms. Audit PASS and speed advantage are distinct.
"""
from __future__ import annotations
import argparse
from contextlib import ExitStack
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
from fold_lm.v05 import prepared_capsule as prepared

EXPERIMENT_ID = "C230-v5f-checked-reduced-preparation-reuse"
STAGE = "V5-F-CHECKED-REDUCED-PREPARATION-REUSE"
BASE = "cec070222749e0e349717da91b7e9e8cc00e9e69"
PARENT_EXECUTION = "339697addb6a2b8c88bad5890456fcf7b41ce398"
PARENT_SHA = "b71769d8c22ef72436b5952406632deafd100c44ed72da8f4c71c93133a0fe37"
PARENT_MEASUREMENTS_SHA = "c96d4154a0aef79fb50b5a34e8c7f5fad10262ebb9a79e02614d0b2a36e74786"
PARENT_QUALITY_SHA = "a816a2829a9923afed5398ac65c616934aeff47dfef156676329d83435553904"
PARENT_VALIDATION_SHA = "08d0113b747fe902d99dedc3204775d22ae9e59cb4dc2f0fa80532ff6cb79551"
DIMENSIONS, BURSTS = (2,16,64,256),(1,4,16)
ARMS = ("candidate","prepared","cached")
UPDATES, WARMUPS, REPEATS, TOLERANCE = 12,1,3,1e-10
MANIFEST_SHA = "c93b9845cd10c4cab316b01da41f3e03f443f75b078c8912fc27c6c23c299b95"
OWN = (
    "fold_lm/v05/prepared_capsule.py",
    "fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py",
    "tests_lm/test_v05_c230_prepared_capsule.py",
    "tools/run_c230.ps1", "tools/invoke_c230.ps1",
    "docs/experiment-ledger-addendum-c230-preregistration.md",
    "docs/v5f-checked-reduced-preparation-v0.1.md",
)
OUTPUTS = {"reuse-plan.json","reuse-exports.zip","measurements.json",
           "quality-checks.json","validation-summary.json"}


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import gate_f_c229_cost_profile as parent
    return parent


def context(parent):
    update=parent.parent_module(); factor=update.parent_module(); dim=factor.parent_module()
    sym=dim.parent_module(); helpers=sym.parent_module(); backend=helpers.base_module()
    return SimpleNamespace(update=update,factor=factor,dim=dim,sym=sym,helpers=helpers,
                           backend=backend,audit=backend.audit)


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,
        parent_measurements_sha256=PARENT_MEASUREMENTS_SHA,parent_quality_sha256=PARENT_QUALITY_SHA,
        parent_validation_sha256=PARENT_VALIDATION_SHA,dimensions=list(DIMENSIONS),bursts=list(BURSTS),
        arms=list(ARMS),initial_events=32,updates=UPDATES,live_factors=2,rank=2,
        changed="opt-in checked fixed-W reduced LU preparation only; current bias recomputed each query",
        safety="SPD validation at preparation; capsule/context/cache identity/version and exact W guard per query",
        cache_scope="CPU float64 unbatched inference; explicit reprepare on matrix/context change",
        old_source_unchanged=True,answer_cache=False,silent_fallback=False,
        order="cyclic by trial plus update",warmups=WARMUPS,repeats=REPEATS,
        tolerance=TOLERANCE,common_setup_counted=True,full_raw_index_bridge_retained=True,
        cache_bytes="W,LU,pivots,version metadata and binding references; no hidden inverse",
        original_final_exports_equal_parent=True,profiled=False,timing_is_descriptive=True,
        new_training_steps=0,gate_f_candidate=False,superiority_required_for_audit=False,
        device="cpu",threads=2,deterministic_algorithms=True,
        stop="adoption-scope decision after this intervention, not an indefinite favorable-workload search")


def load_anchors(rows,checks,parent):
    grid=[(n,q) for n in DIMENSIONS for q in BURSTS]
    require(isinstance(rows,list) and isinstance(checks,list) and len(rows)==len(checks)==12,"parent cells")
    require([(r["numeric_dimension"],r["queries_per_update"]) for r in rows]==grid,"parent row order")
    require([(r["numeric_dimension"],r["queries_per_update"]) for r in checks]==grid,"parent quality order")
    result={}
    for key,row,record in zip(grid,rows,checks,strict=True):
        require(parent.row_gate(row),"parent profile gate")
        require(set(record["inventory"])=={"candidate","cached"},"parent export arm schema")
        for mode in ("unprofiled","profiled"):
            require(len(record[mode])==12 and all(c["passed"] is True for c in record[mode]),"parent quality semantics")
        result[key]=record["inventory"]
    return result


def prepare_bank(bank,state,c):
    status,W,_,_,_,_=bank._read_parts(state)
    require(status.value in ("SUPPORTED","HOT_REQUIRED"),"cannot prepare unsupported state")
    return prepared.prepare(bank.numeric._capsule,W,context=c.factor.bridge_tensors(bank.numeric))


def read_prepared(bank,state,cache,c):
    from fold_lm.v05.memory_bank import BankRead
    status,W,b,h2,hot,hyp=bank._read_parts(state)
    require(status.value in ("SUPPORTED","HOT_REQUIRED"),"unsupported prepared read")
    value=prepared.response(cache,bank.numeric._capsule,W,b,context=c.factor.bridge_tensors(bank.numeric))
    # Keep the same result construction, finite validation and metadata as the reference.
    return BankRead(status,state.memory_revision,state.evidence_revision,state.h2.storage_epoch,
                    h2,hot,hyp,value)


def cache_export(cache,helpers):
    return blob(dict(schema="fold-c230-prepared-reduced-audit-v1",
        references="capsule/base tensors in state-and-bridge.json; no retained bias/answer",
        W=helpers.canonical(cache.W),LU=helpers.canonical(cache.LU),pivots=helpers.canonical(cache.pivots),
        tensor_versions=[version for _,version in cache.stamps]))


def trace_call(fn):
    trace=[]
    specs=((torch.linalg,"cholesky",0),(torch.linalg,"cholesky_ex",0),
           (torch.linalg,"solve",0),(torch,"cholesky_solve",1),
           (torch.linalg,"lu_factor",0),(torch.linalg,"lu_solve",0))
    with ExitStack() as stack:
        for owner,name,index in specs:
            original=getattr(owner,name)
            def wrapped(*args,_name=name,_index=index,_original=original,**kwargs):
                matrix=args[_index]
                trace.append(dict(operation=_name,matrix_shape=list(matrix.shape)))
                return _original(*args,**kwargs)
            stack.enter_context(patch.object(owner,name,wrapped))
        result=fn()
    return result,trace


def expected_trace(arm,n):
    names,width={"candidate":(("cholesky","cholesky_ex","solve"),2),
                 "prepared":(("lu_solve",),2),"cached":(("cholesky_solve",),n),
                 "prepare":(("cholesky","cholesky_ex","lu_factor"),2)}[arm]
    return [dict(operation=name,matrix_shape=[width,width]) for name in names]


def timed(fn):
    start=time.perf_counter_ns(); value=fn()
    return value,time.perf_counter_ns()-start


def trajectory(c,n,q,trial):
    h,s=c.helpers,c.sym
    prefix,tail,complete=c.update.ledger_parts(h)
    bank,common_ns=timed(lambda:c.dim.dimension_bank(c.backend,n))
    adapter=SimpleNamespace(memory=c.backend.memory,c216=SimpleNamespace(build_bank=lambda:bank))
    index,index_ns=timed(lambda:h.source_index(prefix))
    original,original_ns=timed(lambda:h.build_candidate(adapter,prefix))
    fast,fast_ns=timed(lambda:h.build_candidate(adapter,prefix))
    symbolic,symbolic_ns=timed(lambda:s.build_symbolic(adapter,prefix,h))
    states={"candidate":original[1],"prepared":fast[1],"cached":symbolic[0]}
    reduced,reduced_ns=timed(lambda:prepare_bank(bank,states["prepared"],c))
    full,full_ns=timed(lambda:c.update.prepare(c.factor,bank.numeric,states["cached"]))
    reduced_LU,full_L=reduced.LU,full.core.L
    evidence={a:prefix for a in ARMS};indices={a:dict(index) for a in ARMS}
    phases=dict(common_numeric_setup_ns=common_ns,index_build_ns=index_ns,
                reduced_prepare_ns=reduced_ns,full_prepare_ns=full_ns,
                candidate_init_ns=original_ns,prepared_init_ns=fast_ns+reduced_ns,
                cached_init_ns=symbolic_ns+full_ns)
    for a in ARMS: phases[a+"_update_ns"]=phases[a+"_query_ns"]=0
    checks=[]
    for step,line in enumerate(tail):
        offset=(trial+step)%3;order=ARMS[offset:]+ARMS[:offset];responses={}
        for arm in order:
            start=time.perf_counter_ns()
            evidence[arm],event=c.update.append_evidence(evidence[arm],indices[arm],line)
            op=h.memory_op(c.backend.memory,states[arm],event)
            if arm == "cached":
                states[arm],read=c.backend.memory.apply_memory_op(states[arm],op)
                require(read is None,"symbolic mutation returned query")
                full=c.update.refresh(c.factor,full,bank.numeric,states[arm])
            else:
                states[arm],read=bank.apply(states[arm],op)
                require(read is None,"bank mutation returned query")
                states[arm],status=bank.commit(states[arm])
                require(status.value in ("COMMITTED","NOOP"),"bad commit")
            phases[arm+"_update_ns"]+=time.perf_counter_ns()-start
            before=h.blob(h.canonical(states[arm]))
            start=time.perf_counter_ns()
            if arm == "candidate": responses[arm]=[bank.read(states[arm]).value for _ in range(q)]
            elif arm == "prepared": responses[arm]=[read_prepared(bank,states[arm],reduced,c).value for _ in range(q)]
            else: responses[arm]=[c.factor.query_cached(full.core,bank.numeric,states[arm]) for _ in range(q)]
            phases[arm+"_query_ns"]+=time.perf_counter_ns()-start
            require(before == h.blob(h.canonical(states[arm])),"query changed state")
        # Independent current-state solve/provenance checks outside timed phases.
        ref=bank.numeric.full_reference(states["cached"])
        values=[x for a in ARMS for x in responses[a]]
        finite=all(isinstance(x,torch.Tensor) and bool(torch.isfinite(x).all()) for x in values)
        error=max(float(torch.max(torch.abs(x-ref.value))) for x in values) if finite and ref.value is not None else None
        parity=all(h.canonical(bank.to_memory_state(states[a]))==h.canonical(states["cached"])
                   for a in ("candidate","prepared"))
        provenance=True
        for record in states["cached"].records:
            span=indices["cached"].get(record.provenance.source_id)
            if span is None: provenance=False;continue
            event=json.loads(evidence["cached"][slice(*span)])
            provenance &= (event["scope"],event["factor"],event["relation"]) == (record.scope_id,record.factor_id,record.relation_key)
        checks.append(dict(step=step+1,outputs=3*q,max_abs_error=error,state_parity=parity,
            provenance=bool(provenance),passed=bool(parity and provenance and finite
                and ref.status.value=="SUPPORTED" and error<=TOLERANCE
                and reduced.LU is reduced_LU and full.core.L is full_L)))
    require(all(evidence[a]==complete and indices[a]==indices["candidate"] for a in ARMS),"retained raw/index mismatch")
    h.validate_index(complete,indices["candidate"])
    _,prep_trace=trace_call(lambda:prepare_bank(bank,states["prepared"],c))
    traces={}
    for arm,fn in (("candidate",lambda:bank.read(states["candidate"])),
                  ("prepared",lambda:read_prepared(bank,states["prepared"],reduced,c)),
                  ("cached",lambda:c.factor.query_cached(full.core,bank.numeric,states["cached"]))):
        _,traces[arm]=trace_call(fn)
    start=time.perf_counter_ns()
    cf,sf=s.make_exports(h,bank,states["candidate"],states["cached"],complete,indices["candidate"])
    pf,_=s.make_exports(h,bank,states["prepared"],states["cached"],complete,indices["prepared"])
    files=dict(candidate=cf,prepared=dict(pf,**{"prepared-capsule.json":cache_export(reduced,h)}),
               cached=dict(sf,**{"rhs-reuse-cache.json":c.update.cache_export(c.factor,full,h)}))
    phases["export_ns"]=time.perf_counter_ns()-start
    for a in ARMS:
        phases[a+"_stream_ns"]=phases[a+"_update_ns"]+phases[a+"_query_ns"]
        phases[a+"_cold_inclusive_ns"]=phases[a+"_stream_ns"]+phases[a+"_init_ns"]+common_ns+index_ns
    resident={a:h.resident_estimate(dict(bank=bank,state=states[a],raw=complete,index=indices[a],
               cache=reduced if a=="prepared" else full if a=="cached" else None)) for a in ARMS}
    return dict(phases=phases,checks=checks,quality=all(x["passed"] for x in checks),
        files=files,inventory={a:s.inventory(f) for a,f in files.items()},resident=resident,
        prepare_trace=prep_trace,query_traces=traces,extra_reduced_tensor_bytes=prepared.extra_tensor_bytes(reduced),
        reduced_factor_reused=reduced.LU is reduced_LU,full_factor_reused=full.core.L is full_L)


def measure_cell(c,n,q,anchor):
    trials,quality,inventories=[],[],[];last=None
    for trial in range(WARMUPS+REPEATS):
        last=trajectory(c,n,q,trial)
        inv=last["inventory"]
        parity=all(inv[a]==anchor[a] for a in ("candidate","cached"))
        prepared_parity={k:v for k,v in inv["prepared"].items() if k!="prepared-capsule.json"}==inv["candidate"]
        valid=(last["quality"] and parity and prepared_parity and last["extra_reduced_tensor_bytes"]==72
               and last["prepare_trace"]==expected_trace("prepare",n)
               and all(last["query_traces"][a]==expected_trace(a,n) for a in ARMS))
        quality.append(dict(trial=trial,warmup=trial<WARMUPS,passed=valid,parent_export_parity=parity,
                            prepared_base_parity=prepared_parity,checks=last["checks"]))
        inventories.append(inv)
        if trial>=WARMUPS:trials.append(last["phases"])
    row=dict(numeric_dimension=n,queries_per_update=q,trials=trials,
        quality_pass=all(x["passed"] for x in quality),parent_export_parity=all(x["parent_export_parity"] for x in quality),
        repeat_exports_equal=all(x==inventories[0] for x in inventories),retained_inventory=last["inventory"],
        resident_estimate=last["resident"],extra_reduced_tensor_bytes=last["extra_reduced_tensor_bytes"],
        prepare_trace=last["prepare_trace"],query_traces=last["query_traces"],
        reduced_factor_reused=last["reduced_factor_reused"],full_factor_reused=last["full_factor_reused"])
    for a in ARMS:
        row[a+"_export_bytes"]=sum(x["bytes"] for x in row["retained_inventory"][a].values())
        for phase in ("init","update","query","stream","cold_inclusive"):
            row[a+"_"+phase+"_median_ns"]=statistics.median(x[a+"_"+phase+"_ns"] for x in trials)
    for other in ("candidate","cached"):
        row["stream_ratio_prepared_over_"+other]=row["prepared_stream_median_ns"]/max(1,row[other+"_stream_median_ns"])
    return row,quality,last["files"]


def row_gate(r):
    n,q=r["numeric_dimension"],r["queries_per_update"]
    return (n in DIMENSIONS and q in BURSTS and all(r.get(x) is True for x in
        ("quality_pass","parent_export_parity","repeat_exports_equal","reduced_factor_reused","full_factor_reused"))
        and len(r["trials"])==3 and r["extra_reduced_tensor_bytes"]==72
        and r["prepare_trace"]==expected_trace("prepare",n)
        and all(r["query_traces"][a]==expected_trace(a,n) for a in ARMS)
        and all(r[a+"_export_bytes"]==sum(x["bytes"] for x in r["retained_inventory"][a].values()) for a in ARMS)
        and all(t[a+"_stream_ns"]==t[a+"_update_ns"]+t[a+"_query_ns"] for t in r["trials"] for a in ARMS))


def summarize(rows):
    return dict(cells=[[r["numeric_dimension"],r["queries_per_update"]] for r in rows],
        audit_pass=all(row_gate(r) for r in rows),all_quality_parity=all(r["quality_pass"] for r in rows),
        parent_export_parity=all(r["parent_export_parity"] for r in rows),
        all_reduced_queries_reuse=all(r["query_traces"]["prepared"]==expected_trace("prepared",r["numeric_dimension"]) for r in rows),
        ratios_vs_original=[r["stream_ratio_prepared_over_candidate"] for r in rows],
        ratios_vs_full_cache=[r["stream_ratio_prepared_over_cached"] for r in rows],new_training_steps=0)


def gate(s):
    return (s.get("cells")==[[n,q] for n in DIMENSIONS for q in BURSTS]
        and all(s.get(k) is True for k in ("audit_pass","all_quality_parity","parent_export_parity","all_reduced_queries_reuse"))
        and s.get("new_training_steps")==0)


def verify_archive(path,rows):
    expected={f"{r['numeric_dimension']}/{r['queries_per_update']}/{arm}/{name}":item
              for r in rows for arm,inv in r["retained_inventory"].items() for name,item in inv.items()}
    with zipfile.ZipFile(path) as archive:
        require(len(archive.namelist())==len(expected) and set(archive.namelist())==set(expected),"archive members")
        for name,item in expected.items():
            data=archive.read(name)
            require(len(data)==item["bytes"] and hashlib.sha256(data).hexdigest()==item["sha256"],"archive content")


def precheck(c229_summary,root):
    parent=parent_module();c=context(parent);a=c.audit;root=Path(root)
    require(a.sha(c229_summary)==PARENT_SHA,"C229 summary changed")
    p=a.read_json(c229_summary);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS" and parent.gate(p["validation_summary"]),"wrong C229")
    require(len(p["source_blobs"])==214 and len(p["input_sha256"])==292,"parent counts")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for path,wanted in protected.items():require(Path(path).is_file() and a.sha(path)==wanted,"changed input:"+path)
    for path,wanted in pins.items():require(a.git(root,"rev-parse","HEAD:"+path).decode().strip()==wanted,"changed source:"+path)
    protected[str(Path(c229_summary).resolve())]=PARENT_SHA
    wanted={"measurements.json":PARENT_MEASUREMENTS_SHA,"quality-checks.json":PARENT_QUALITY_SHA,"validation-summary.json":PARENT_VALIDATION_SHA};seen=set()
    for item in p["artifacts"]:
        path=a.safe_child(Path(c229_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path)==item["sha256"] and path.stat().st_size==item["serialized_bytes"],"parent artifact")
        protected[str(path.resolve())]=item["sha256"]
        if item["file"] in wanted:require(item["sha256"]==wanted[item["file"]],"parent deciding hash");seen.add(item["file"])
    require(len(seen)==3,"parent deciding artifacts missing")
    folder=Path(c229_summary).resolve().parent
    load_anchors(a.read_json(folder/"measurements.json"),a.read_json(folder/"quality-checks.json"),parent)
    for path in OWN:
        require(path not in pins,"OWN overlaps parent");pins[path]=a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    deps=tuple(c.backend.DIRECT_REPO_DEPENDENCIES)+(
        "fold_lm/v05_benchmarks/gate_f_c220_frozen_learned_stack.py","fold_lm/v05/memory_dispatch.py",
        "fold_lm/v05_benchmarks/gate_f_c221_live_coverage_dispatch.py","fold_lm/v05_benchmarks/gate_f_c222_withdrawal_lifecycle.py",
        "fold_lm/v05/memory_request_lease.py","fold_lm/v05_benchmarks/gate_f_c223_request_freshness.py",
        "fold_lm/v05/state.py","fold_lm/capsule.py","fold_lm/v05_benchmarks/gate_f_c224_history_cost_audit.py",
        "fold_lm/v05_benchmarks/gate_f_c225_stateful_baseline.py","fold_lm/v05_benchmarks/gate_f_c226_dimension_scaling.py",
        "fold_lm/v05_benchmarks/gate_f_c227_factor_reuse.py","fold_lm/v05_benchmarks/gate_f_c228_update_query_cost.py",
        "fold_lm/v05_benchmarks/gate_f_c229_cost_profile.py",OWN[0])
    require(len(deps)==len(set(deps))==29 and all(x in pins for x in deps),"unpinned dependency")
    protected.update(a.protect_tree_files(root,pins))
    require(len(pins)==221 and len(protected)==305,"C230 counts")
    require(digest(manifest())==MANIFEST_SHA,"manifest drift")
    return p,pins,protected


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==114,"parent modules")
    return names+["tests_lm.test_v05_c230_prepared_capsule"]


def regression_suite(root):
    helper=context(parent_module()).backend.c205
    tests=list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    excluded=helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS;ids=[t.id() for t in tests]
    require(all(ids.count(x)==1 for x in excluded),"historical exclusion")
    kept=[t for t in tests if t.id() not in excluded]
    require(len(tests)==2666 and len(kept)==2665,"C230 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"C230 identity")
    require(len(p["source_blobs"])==221 and len(p["input_sha256"])==305 and len(p["artifacts"])==5
        and {x["file"] for x in p["artifacts"]}==OUTPUTS,"C230 output coverage")
    require(p["validation_summary"]["cells"]==[[n,q] for n in DIMENSIONS for q in BURSTS],"incomplete C230")
    require(p["status"]==("PASS" if gate(p["validation_summary"]) else "FAIL"),"verdict drift")
    require(p["gate_f_candidate"] is False and p["network_calls"]==0,"scope drift")


def run(*,c229_summary,output_dir,expected_head):
    parent=parent_module();c=context(parent);a=c.audit;root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    _,pins,protected=precheck(c229_summary,root);folder=Path(c229_summary).resolve().parent
    anchors=load_anchors(a.read_json(folder/"measurements.json"),a.read_json(folder/"quality-checks.json"),parent)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);rows,checks=[],[]
    with zipfile.ZipFile(out/"reuse-exports.zip","w",compression=zipfile.ZIP_STORED) as archive:
        for n in DIMENSIONS:
            for q in BURSTS:
                row,quality,files=measure_cell(c,n,q,anchors[(n,q)]);rows.append(row)
                checks.append(dict(numeric_dimension=n,queries_per_update=q,trials=quality))
                for arm,contents in files.items():
                    for name,data in contents.items():archive.writestr(f"{n}/{q}/{arm}/{name}",data)
    verify_archive(out/"reuse-exports.zip",rows);summary=summarize(rows)
    for name,value in (("reuse-plan.json",manifest()),("measurements.json",rows),("quality-checks.json",checks),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard();precheck(c229_summary,root)
    for path,wanted in protected.items():require(a.sha(path)==wanted,"changed input:"+path)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if gate(summary) else "FAIL",diagnostic_execution_valid=True,C229_summary_sha256=PARENT_SHA,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,network_calls=0,default_runtime_changed=False,
        limitations=["explicit fixed-W prepared path, not default serving replacement",
                     "CPU float64 inference, no autograd/concurrency/unsafe alias writes",
                     "same two-factor bias-only workload; descriptive timing, no Gate F claim"])
    validate_result(result);(out/"summary.json").write_bytes(blob(result))
    print("=== C230 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("c229-summary","output-dir"):p.add_argument("--"+arg,type=Path,required=True)
    p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))


if __name__=="__main__":main()
