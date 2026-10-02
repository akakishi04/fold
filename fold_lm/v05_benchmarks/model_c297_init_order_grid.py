"""C297: complete initialization x shuffle grid; training diagnostic, not a new capability gate."""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
from types import ModuleType
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C297-v5b-initialization-order-grid"
STAGE = "V5-B-INITIALIZATION-ORDER-GRID"
BASE = "8e76dbbaa2a58658b80f60e2d90ee9acbe23f8b8"
PARENT_EXECUTION = "3d52da4b565d05727b604560bbf60710dd9536e2"
PARENT_SHA = "d48c4c6725cecdf9e15034448186fe39b7e8b86b45f7a6418c839e2536f1093b"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c296_render_balanced_batches.py"
PARENT_BLOB = "ae4fd7a45ec9306b1b81a82f8707269f1d88277b"
INITIALS = (297001, 297002, 297003)
ORDERS = (297101, 297102, 297103)
FIT_RNG = 597000
TASKS = ("two_char", "triple", "quad")
SPLITS = ("TRAIN", "HOLDOUT")
OWN = ("fold_lm/v05_benchmarks/model_c297_init_order_grid.py",
       "tests_lm/test_v05_c297_init_order_grid.py", "tools/run_c297.ps1", "tools/invoke_c297.ps1",
       "docs/experiment-ledger-addendum-c297-preregistration.md", "docs/v5b-init-order-grid-v0.1.md")
OUTPUTS = ("architecture-plan.json", "dataset.json", "triple-dataset.json", "quad-dataset.json",
           "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=9, train_steps=7200, training_rows=345600, model_forward_calls=8658,
            row_presentations=485568, core_forward_calls=34632, model_state_loads=9,
            checkpoint_bundle_loads=1, new_checkpoint_writes=1, network_calls=0)
DATA_HASHES = ("1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
               "432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",
               "86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b")
MANIFEST_SHA = "6fc874b494cdc0b9dea5c55b57e482ef8eca50cc9790abc62840cf29e52bb903"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(INITIALS, ORDERS))


def context():
    from fold_lm.v05_benchmarks import model_c296_render_balanced_batches as parent
    _, audit, diagnostic, evaluation, transfer, training, c = parent.context()
    return parent, audit, diagnostic, evaluation, transfer, training, c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_summary_sha256=PARENT_SHA,
        parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
        question="how do fixed initial states and independent example-order streams affect this complete3x3 grid",
        initial_seeds=list(INITIALS), order_seeds=list(ORDERS), fit_rng=FIT_RNG,
        architecture="actual C278 MeanFinalDualReadout", parameters=14256, max_tokens=48,
        schedule="blocked200epochs*4;randperm96(order_seed+297000+epoch);length=epoch%2;profile=epoch%3",
        per_length_row_exposures=100, steps_per_cell=800, loss="ordinary mean CE only",
        optimizer="AdamW", lr=.005, betas=[.9,.999], eps=1e-8, weight_decay=0., clip=1.,
        held="same three initial states across columns;identical schedules across rows;fixed fit RNG in every cell",
        diagnostic_gate="all nine preregistered cells,matching,original scoring and strict replay complete;not model capability",
        gates=dict(accuracy=.90, query_pair=.80, evidence_drop=.35, query_drop=.35, two_order=.80),
        descriptive="three task pass matrices;54 final partitions;12 accuracy/NLL grids with finite-grid additive decomposition",
        limitation="three fixed levels per factor,one run per cell;interaction not population variance;no p values or best-seed selection",
        parents=23, source_pins=628, protected_inputs=1146, own_tests=32,
        modules=182, loaded_tests=4494, focused_tests=4493, excluded_test=EXCLUDED,
        data_hashes=list(DATA_HASHES), dtype="CPU float64", threads=2, deterministic=True,
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None and digest(manifest()) == MANIFEST_SHA, "manifest seal")


def schedule(order, rows, pair_builder):
    require(order in ORDERS, "order seed")
    pairs = pair_builder(rows)
    require(pairs.shape == (96,2) and pairs.dtype == torch.int64, "pairs")
    events = torch.empty((800,24,4), dtype=torch.int64)
    for epoch in range(200):
        perm = torch.randperm(96, generator=torch.Generator().manual_seed(order+297000+epoch))
        for block in range(4):
            step = 4*epoch+block
            events[step,:,0] = epoch%2
            events[step,:,1] = epoch%3
            events[step,:,2:] = pairs[perm[24*block:24*(block+1)]]
    for length in range(2):
        ii = events[events[:,:,0] == length][:,2:].flatten()
        require(torch.equal(torch.bincount(ii, minlength=192), torch.full((192,),100)), "row exposure")
    return events


def make_models(initial, c):
    require(initial in INITIALS, "initial seed")
    first = c.c278.MeanFinalDualReadout(c.factory.new_model(initial), initial, c.reader, c.c269.query_span_mask)
    models = [first, copy.deepcopy(first), copy.deepcopy(first)]
    for model in models:
        require(type(model) is c.c278.MeanFinalDualReadout and sum(p.numel() for p in model.parameters()) == 14256, "architecture/capacity")
        require(all(p.dtype == torch.float64 and p.device.type == "cpu" for p in model.parameters()), "precision")
        require(c.base.fingerprint(model) == c.base.fingerprint(first), "initial equality")
    for a,b in itertools.combinations(models,2):
        require(all(x.data_ptr() != y.data_ptr() for x,y in zip(a.parameters(),b.parameters(),strict=True)), "independent storage")
    return models


def fit(model, data, tokens, targets, initial, order, parent):
    require((initial,order) in identities(), "cell identity")
    require(tokens.shape == (2,3,192,48) and targets.shape == (192,) and tokens.dtype == targets.dtype == torch.int64, "training tables")
    require(torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)), "target alignment")
    events = schedule(order,data["TRAIN"],parent.pairs_from_rows)
    torch.manual_seed(FIT_RNG)
    opt = torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    model.train(); losses=[]
    for step in range(800):
        require(len(opt.param_groups) == 1 and opt.param_groups[0]["lr"] == .005, "constant LR")
        opt.zero_grad(set_to_none=True)
        x,y = parent.render_batch(tokens,targets,events[step])
        z = model(x,torch.zeros(48,dtype=torch.int64))
        require(z.shape == (48,256) and z.dtype == torch.float64 and bool(torch.isfinite(z).all()), "logits")
        loss = F.cross_entropy(z,y); require(bool(torch.isfinite(loss)), "finite loss")
        losses.append(float(loss.detach())); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True); opt.step()
        if (step+1)%200 == 0:
            print(f"[C297] initial={initial} order={order} step={step+1}/800 ce={losses[-1]:.6f}",flush=True)
    model.eval()
    return dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=FIT_RNG,
                ce_history=losses,event_sha256=digest(events.tolist()),schedule_events=events)


def check_fit(f,order,data,parent):
    require(all(type(f[k]) is int and f[k] == v for k,v in dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=FIT_RNG).items()), "fit workload/RNG")
    expected = schedule(order,data["TRAIN"],parent.pairs_from_rows); events=f["schedule_events"]
    require(isinstance(events,torch.Tensor) and events.dtype == torch.int64 and torch.equal(events,expected)
            and f["event_sha256"] == digest(expected.tolist()), "saved schedule")
    require(len(f["ce_history"]) == 800 and all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in f["ce_history"]), "loss history")


def train_cell(model,data,triple,quad,tokens,targets,initial,order,parent,evaluation,transfer,c):
    start=c.base.fingerprint(model); back=c.base.fingerprint(model.backbone); head=c.base.fingerprint(model.read)
    with c.p267.counted(model,c.core) as (calls,cores):
        fitted=fit(model,data,tokens,targets,initial,order,parent)
        final=c.base.fingerprint(model); model.requires_grad_(False)
        raw=evaluation.evaluate(model,data,triple,quad,transfer,c)
    require(calls == [881,46176] and cores[0] == 3524, "actual train/evaluation count")
    require(start != final and back != c.base.fingerprint(model.backbone) and head != c.base.fingerprint(model.read)
            and final == c.base.fingerprint(model), "weight integrity")
    return dict(initial_seed=initial,order_seed=order,initial_sha256=start,final_sha256=final,
                parameters=14256,fit=fitted,raw=raw,forward_calls=881,row_presentations=46176,core_forward_calls=3524), \
           {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def decompose(matrix):
    x=torch.tensor(matrix,dtype=torch.float64)
    require(x.shape == (3,3) and bool(torch.isfinite(x).all()), "grid matrix")
    mean=x.mean(); ri=x.mean(1)-mean; co=x.mean(0)-mean
    residual=x-mean-ri[:,None]-co[None,:]
    si=float(3*ri.square().sum()); so=float(3*co.square().sum()); sx=float(residual.square().sum())
    total=float((x-mean).square().sum())
    require(math.isclose(si+so+sx,total,rel_tol=1e-10,abs_tol=1e-12), "grid decomposition")
    return dict(matrix=x.tolist(),mean=float(mean),initial_means=x.mean(1).tolist(),order_means=x.mean(0).tolist(),
                interaction=residual.tolist(),initial_ss=si,order_ss=so,interaction_ss=sx,total_ss=total)


def check_grid(records):
    require([(r["initial_seed"],r["order_seed"]) for r in records] == identities(), "complete grid")
    for initial in INITIALS:
        require(len({r["initial_sha256"] for r in records if r["initial_seed"] == initial}) == 1, "row initial equality")
    require(len({records[i*3]["initial_sha256"] for i in range(3)}) == 3, "distinct initial states")
    for order in ORDERS:
        require(len({r["fit"]["event_sha256"] for r in records if r["order_seed"] == order}) == 1, "column schedule equality")
    require(len({r["fit"]["event_sha256"] for r in records[:3]}) == 3, "distinct order streams")


def analyze(records,data,parent,diagnostic,transfer,c):
    check_grid(records); metrics=[]; parts=[]; results=[]
    for r in records:
        identity=dict(initial_seed=r["initial_seed"],order_seed=r["order_seed"])
        require(r["parameters"] == 14256 and r["initial_sha256"] != r["final_sha256"] and r["checkpoint_roundtrip"] is True, "record integrity")
        error=r["reload_max_error"]
        require(type(error) in (int,float) and math.isfinite(error) and 0<=error<=1e-9, "replay drift")
        keys=("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in keys) and tuple(r[k] for k in keys)==(881,46176,3524,81,7776,324), "record counts")
        check_fit(r["fit"],r["order_seed"],data,parent); require(set(r["raw"]) == set(TASKS), "task inventory")
        scored=dict(two_char=c.p267.score(data,r["raw"]["two_char"]),
                    triple=c.c270.score(data,r["raw"]["triple"],c.p267),quad=transfer.score_quad(data,r["raw"]["quad"],c))
        flags={t+"_pass":scored[t]["passed"] for t in TASKS}
        require(all(type(v) is bool for v in flags.values()), "task flags"); direct={}
        for task in TASKS:
            normalized=diagnostic.normalize_task(scored[task],task,r["initial_seed"],"order_"+str(r["order_seed"]))
            for split in SPLITS:
                part=diagnostic.partition([v for v in normalized if v["split"] == split])
                require(type(part["direct_pass"]) is bool and math.isfinite(part["final_normal_nll"]), "partition fields")
                direct[(task,split)]=part["direct_pass"]; parts.append(dict(**identity,task=task,split=split,**part))
        results.append(dict(**identity,all_tasks_pass=all(flags.values()),
            fitted_train_direct_pass=all(direct[(t,"TRAIN")] for t in TASKS[:2]),
            seen_holdout_direct_pass=all(direct[(t,"HOLDOUT")] for t in TASKS[:2]),**flags))
        metrics.append(dict(**identity,**scored))
    grids=[]
    for task,split,field in itertools.product(TASKS,SPLITS,("accuracy","final_normal_nll")):
        rows=[p for p in parts if p["task"] == task and p["split"] == split]
        require([(p["initial_seed"],p["order_seed"]) for p in rows] == identities(), "partition grid")
        values=[p["correct"]/p["rows"] if field == "accuracy" else p[field] for p in rows]
        grids.append(dict(task=task,split=split,metric=field,**decompose([values[k:k+3] for k in (0,3,6)])))
    matrices={t:[[results[3*i+j][t+"_pass"] for j in range(3)] for i in range(3)] for t in TASKS}
    s=dict(cell_results=results,final_partitions=parts,grids=grids,task_pass_matrices=matrices,
           diagnostic_complete=True,capability_gate_applicable=False,all_replays=True,grid_matched=True,**WORK)
    require(len(parts)==54 and len(grids)==12, "summary inventory")
    return metrics,s


def parent_hashes(parent):
    p295,audit,*_=parent.context(); p293=p295.context()[1]; p292,p291,*_=p293.context(); old=p291.context()
    return (PARENT_SHA,parent.PARENT_SHA,p295.PARENT_SHA,audit.PARENT_SHA,p293.PARENT_SHA,
            p292.PARENT_SHA,p291.PARENT_SHA,old[0].PARENT_SHA,*old[1].SUMMARY_SHAS)


def load_parent(paths):
    parent,audit,*_,c=context(); paths=[Path(p).resolve() for p in paths]; hashes=parent_hashes(parent)
    require(len(paths)==len(hashes)==23 and all(c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)), "parent hashes")
    with audit.no_neural():
        p,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); parent.validate_result(p)
        require(p["experiment_id"]=="C296-v5b-render-balanced-minibatches" and p["commit_sha"]==PARENT_EXECUTION
                and p["status"]=="FAIL" and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB, "parent identity")
        s=p["validation_summary"]
        require(s["quad_pass_counts"]==dict(blocked=2,balanced=3) and s["all_pairs_matched"] is True
                and s["all_replays"] is True and s["candidate_gate"] is False, "parent verdict")
        require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS), "parent outputs")
        data=[c.audit.read_json(paths[0].parent/n) for n in OUTPUTS[1:4]]
        require(tuple(map(digest,data))==DATA_HASHES, "data hashes")
    return p,*data


def precheck(paths,root):
    validate_seal(); p,*_=load_parent(paths); parent,audit,*_,c=context(); root=Path(root).resolve()
    pins=dict(p["source_blobs"]); protected=dict(p["input_sha256"])
    require((len(pins),len(protected))==(622,1131), "inherited counts")
    for n,h in pins.items(): require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h, "changed source:"+n)
    for n,h in protected.items(): require(Path(n).is_file() and c.audit.sha(n)==h, "changed input:"+n)
    covered=set()
    for module in [parent,audit,*parent.context(),*vars(c).values()]:
        path=getattr(module,"__file__",None) if isinstance(module,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            n=Path(path).resolve().relative_to(root).as_posix(); require(n in pins,"unprotected helper:"+n); covered.add(n)
    require(PARENT_SOURCE in covered and pins[PARENT_SOURCE]==PARENT_BLOB, "parent source coverage")
    entries=[(Path(paths[0]).resolve(),PARENT_SHA)]+[(c.audit.safe_child(Path(paths[0]).resolve().parent,a["file"]),a["sha256"]) for a in p["artifacts"]]
    for path,h in entries:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h, "parent input")
        protected[str(path.resolve())]=h
    for n in OWN:
        require(n not in pins, "OWN collision"); pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(628,1146), "protection counts")
    print(f"registration_check = source_pins:628; protected_inputs:1146; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def runtime_preflight(paths,root):
    precheck(paths,root); parent,*_,training,c=context(); _,data,_,_=load_parent(paths)
    tokens,targets=training.training_tables(data,c)
    for order in ORDERS:
        plan=schedule(order,data["TRAIN"],parent.pairs_from_rows)
        x,y=parent.render_batch(tokens,targets,plan[0]); require(x.shape==(48,48) and y.shape==(48,), "real batch")
    for initial in INITIALS: make_models(initial,c)
    print("real_three_initials_three_orders = PASS; science not started",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS"
            and p["diagnostic_execution_valid"] is True, "diagnostic result")
    require(all(p[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")), "claim scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(628,1146) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB, "result protection")
    require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS), "outputs")
    s=p["validation_summary"]; rr=s["cell_results"]
    require([(r["initial_seed"],r["order_seed"]) for r in rr]==identities(), "result grid")
    require(all(type(r[t+"_pass"]) is bool for r in rr for t in TASKS)
            and all(r["all_tasks_pass"] is all(r[t+"_pass"] for t in TASKS) for r in rr), "result flags")
    require(s["task_pass_matrices"]=={t:[[rr[3*i+j][t+"_pass"] for j in range(3)] for i in range(3)] for t in TASKS}, "pass matrices")
    require(len(s["final_partitions"])==54 and len(s["grids"])==12, "result inventory")
    require(s["diagnostic_complete"] is True and s["all_replays"] is True and s["grid_matched"] is True
            and s["capability_gate_applicable"] is False, "diagnostic flags")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()), "workload")


def load_bundle(path):
    p=torch.load(path,map_location="cpu",weights_only=True)
    require(set(p)=={"schema","identities","states"} and p["schema"]=="fold-c297-grid-models-v1"
            and p["identities"]==[list(i) for i in identities()] and len(p["states"])==9, "bundle")
    return p["states"]


def flatten(suite):
    for test in suite:
        if isinstance(test,unittest.TestSuite): yield from flatten(test)
        else: yield test


def regression_modules(root):
    names=context()[0].regression_modules(root)
    require(len(names)==len(set(names))==181, "parent modules")
    return names+["tests_lm.test_v05_c297_init_order_grid"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==manifest()["loaded_tests"] and ids.count(EXCLUDED)==1, "loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED]; require(len(kept)==manifest()["focused_tests"], "focused suite")
    return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head
            and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(), "repository guard")


def run(*,summaries,output_dir,expected_head):
    parent,_,diagnostic,evaluation,transfer,training,c=context(); root=Path(__file__).resolve().parents[2]
    guard(root,expected_head,c); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected=precheck(summaries,root); _,data,triple,quad=load_parent(summaries)
    tokens,targets=training.training_tables(data,c); out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    records=[]; states=[]
    for initial in INITIALS:
        for order,model in zip(ORDERS,make_models(initial,c),strict=True):
            print(f"[C297] cell={len(records)+1}/9 initial={initial} order={order}",flush=True)
            r,state=train_cell(model,data,triple,quad,tokens,targets,initial,order,parent,evaluation,transfer,c)
            records.append(r); states.append(state)
    torch.save(dict(schema="fold-c297-grid-models-v1",identities=[list(i) for i in identities()],states=states),out/"trained-models.pt")
    loaded=load_bundle(out/"trained-models.pt")
    for i,initial in enumerate(INITIALS):
        for j,model in enumerate(make_models(initial,c)):
            k=3*i+j; evaluation.replay_one(model,loaded[k],records[k],data,triple,quad,transfer,c)
    metrics,summary=analyze(records,data,parent,diagnostic,transfer,c)
    torch.save(dict(schema="fold-c297-grid-eval-v1",records=records),out/"evaluations.pt")
    for n,v in (("architecture-plan.json",manifest()),("dataset.json",data),("triple-dataset.json",triple),
                ("quad-dataset.json",quad),("measurements.json",metrics),("validation-summary.json",summary)):
        (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c); precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
           source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
           capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","diagnostic_execution_valid","artifacts")}
    receipt["summary_sha256"]=c.audit.sha(out/"summary.json")
    print("=== C297 COMPACT DIAGNOSTIC RECEIPT ===",flush=True); print(json.dumps(receipt,sort_keys=True,indent=2),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    parent,audit,diagnostic,_,transfer,_,c=context(); out=Path(outdir); p=c.audit.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"]==expected_head, "execution HEAD")
    for n,h in p["input_sha256"].items(): require(c.audit.sha(n)==h, "protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"])
        require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"], "output bytes")
    with audit.no_neural():
        _,data,triple,quad=load_parent(summaries)
        for n,v in zip(OUTPUTS[1:4],(data,triple,quad),strict=True): require(c.audit.read_json(out/n)==v, "persisted data")
        archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c297-grid-eval-v1", "archive schema")
        metrics,s=analyze(archive["records"],data,parent,diagnostic,transfer,c)
        for n,v in (("architecture-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",s)):
            require(c.audit.read_json(out/n)==v, "persisted:"+n)
    require(s==p["validation_summary"], "summary reconstruction")
    return p,metrics


def main():
    p=argparse.ArgumentParser(); p.add_argument("--summaries",nargs=23,type=Path,required=True)
    p.add_argument("--output-dir",type=Path,required=True); p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__ == "__main__": main()
