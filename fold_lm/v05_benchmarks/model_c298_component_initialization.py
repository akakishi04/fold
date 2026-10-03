"""C298: backbone x added-reader initial states; complete targeted diagnostic."""
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

EXPERIMENT_ID = "C298-v5b-component-initialization-grid"
STAGE = "V5-B-COMPONENT-INITIALIZATION-GRID"
BASE = "fe56cfdd4d393ae5d6a3d268eaa66f19a0b5a578"
PARENT_EXECUTION = "18576c2df5f928d5904bd99bd39a2de58c5736da"
PARENT_SHA = "9bfceee367a11edfe9ae5b62f381cdaf183ef357109f5dff7b345a11e3180aba"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c297_init_order_grid.py"
PARENT_BLOB = "49497d433c6302cd2a65635564f254edbf169104"
LEVELS = (297001, 297002, 297003)
ORDER = 297101
FIT_RNG = 597000
TASKS = ("two_char", "triple", "quad")
OWN = ("fold_lm/v05_benchmarks/model_c298_component_initialization.py",
       "tests_lm/test_v05_c298_component_initialization.py", "tools/run_c298.ps1", "tools/invoke_c298.ps1",
       "docs/experiment-ledger-addendum-c298-preregistration.md", "docs/v5b-component-initialization-v0.1.md")
OUTPUTS = ("architecture-plan.json", "dataset.json", "triple-dataset.json", "quad-dataset.json",
           "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=9, train_steps=7200, training_rows=345600, model_forward_calls=8658,
            row_presentations=485568, core_forward_calls=34632, model_state_loads=9,
            checkpoint_bundle_loads=1, new_checkpoint_writes=1, network_calls=0)
DATA_HASHES = ("1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
               "432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",
               "86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b")
MANIFEST_SHA = "e89e471d5f6e50e028136cf667b7a20f797c444f63b2638c3e29f11736c9cb62"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(LEVELS, LEVELS))


def context():
    from fold_lm.v05_benchmarks import model_c297_init_order_grid as parent
    pair_source, audit, diagnostic, evaluation, transfer, training, c = parent.context()
    return parent, pair_source, audit, diagnostic, evaluation, transfer, training, c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_summary_sha256=PARENT_SHA,
        parent_source=PARENT_SOURCE, parent_blob=PARENT_BLOB,
        question="does the C297 fixed-order outcome follow backbone initialization, added reader initialization, or their combination",
        levels=list(LEVELS), order_seed=ORDER, fit_rng=FIT_RNG,
        architecture="actual C278 MeanFinalDualReadout;swap only untrained read module;train every parameter",
        parameters=14256, backbone_parameters=13488, reader_parameters=768, max_tokens=48,
        schedule="exact C297 first registered order297101 in every cell;800 updates;blocked;100 exposures per row per length",
        loss="ordinary mean CE", optimizer="AdamW", lr=.005, betas=[.9,.999], eps=1e-8, weight_decay=0., clip=1.,
        diagonals="all three same-component cells retrain from scratch;initial/final fingerprints and800 CE values exactly match C297;all-view logits<=1e-9 with exact argmax",
        diagnostic_gate="complete9 cells;component matching;diagonal reproduction;strict replay;original scoring;not capability improvement",
        gates=dict(accuracy=.90, query_pair=.80, evidence_drop=.35, query_drop=.35, two_order=.80),
        reporting="9 results;3 task matrices;54 partitions;12 accuracy/NLL grids with backbone/reader additive decomposition",
        limitation="same three C297 levels,one fixed first order;targeted follow-up not fresh replication;no winner selection or population-variance claims",
        parents=24, source_pins=634, protected_inputs=1161, own_tests=32,
        modules=183, loaded_tests=4526, focused_tests=4525, excluded_test=EXCLUDED,
        data_hashes=list(DATA_HASHES), dtype="CPU float64", threads=2, deterministic=True,
        capability_gate_applicable=False, gate_f_candidate=False, production_adoption=False, **WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}", MANIFEST_SHA) is not None and digest(manifest()) == MANIFEST_SHA, "manifest seal")


def make_grid(c):
    references = {s:c.c278.MeanFinalDualReadout(c.factory.new_model(s),s,c.reader,c.c269.query_span_mask) for s in LEVELS}
    for model in references.values():
        require(set(model._modules) == {"backbone","read"}, "component boundary")
        require(sum(p.numel() for p in model.backbone.parameters()) == 13488
                and sum(p.numel() for p in model.read.parameters()) == 768, "component sizes")
        require(all(k.startswith(("backbone.","read.")) for k in model.state_dict()), "state coverage")
    require(len({c.base.fingerprint(m.backbone) for m in references.values()}) == 3, "distinct backbone levels")
    require(len({c.base.fingerprint(m.read) for m in references.values()}) == 3, "distinct reader levels")
    grid = {}
    used = set()
    for bs,rs in identities():
        model = copy.deepcopy(references[bs])
        model.read = copy.deepcopy(references[rs].read)
        require(type(model) is c.c278.MeanFinalDualReadout and sum(p.numel() for p in model.parameters()) == 14256, "architecture")
        require(all(p.dtype == torch.float64 and p.device.type == "cpu" for p in model.parameters()), "precision")
        require(c.base.fingerprint(model.backbone) == c.base.fingerprint(references[bs].backbone)
                and c.base.fingerprint(model.read) == c.base.fingerprint(references[rs].read), "component provenance")
        require(list(model.state_dict()) == list(references[bs].state_dict()), "state order")
        ptrs = {p.data_ptr() for p in model.parameters()}
        require(not ptrs & used, "independent grid storage"); used.update(ptrs)
        if bs == rs:
            require(c.base.fingerprint(model) == c.base.fingerprint(references[bs]), "diagonal initialization")
        grid[(bs,rs)] = model
    return grid


def fit(model,data,tokens,targets,bs,rs,parent,pair_source):
    require((bs,rs) in identities(), "cell identity")
    require(tokens.shape == (2,3,192,48) and targets.shape == (192,) and tokens.dtype == targets.dtype == torch.int64, "tables")
    require(torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)), "target alignment")
    events = parent.schedule(ORDER,data["TRAIN"],pair_source.pairs_from_rows)
    torch.manual_seed(FIT_RNG)
    opt = torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    model.train(); losses=[]
    for step in range(800):
        require(len(opt.param_groups)==1 and opt.param_groups[0]["lr"]==.005, "constant LR")
        opt.zero_grad(set_to_none=True)
        x,y = pair_source.render_batch(tokens,targets,events[step])
        z = model(x,torch.zeros(48,dtype=torch.int64))
        require(z.shape==(48,256) and z.dtype==torch.float64 and bool(torch.isfinite(z).all()), "logits")
        loss=F.cross_entropy(z,y); require(bool(torch.isfinite(loss)), "finite loss")
        losses.append(float(loss.detach())); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True); opt.step()
        if (step+1)%200==0:
            print(f"[C298] backbone={bs} reader={rs} step={step+1}/800 ce={losses[-1]:.6f}",flush=True)
    model.eval()
    return dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=FIT_RNG,
                ce_history=losses,event_sha256=digest(events.tolist()),schedule_events=events)


def train_cell(model,data,triple,quad,tokens,targets,bs,rs,parent,pair_source,evaluation,transfer,c):
    start=c.base.fingerprint(model); back=c.base.fingerprint(model.backbone); read=c.base.fingerprint(model.read)
    with c.p267.counted(model,c.core) as (calls,cores):
        fitted=fit(model,data,tokens,targets,bs,rs,parent,pair_source)
        final=c.base.fingerprint(model); model.requires_grad_(False)
        raw=evaluation.evaluate(model,data,triple,quad,transfer,c)
    require(calls==[881,46176] and cores[0]==3524, "train/evaluation count")
    require(start!=final and back!=c.base.fingerprint(model.backbone) and read!=c.base.fingerprint(model.read)
            and final==c.base.fingerprint(model), "weights")
    return dict(backbone_seed=bs,reader_seed=rs,initial_sha256=start,backbone_initial_sha256=back,
        reader_initial_sha256=read,final_sha256=final,parameters=14256,fit=fitted,raw=raw,
        forward_calls=881,row_presentations=46176,core_forward_calls=3524), {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def check_components(records):
    require([(r["backbone_seed"],r["reader_seed"]) for r in records]==identities(), "complete component grid")
    require(len({r["fit"]["event_sha256"] for r in records})==1, "common schedule")
    for seed in LEVELS:
        require(len({r["backbone_initial_sha256"] for r in records if r["backbone_seed"]==seed})==1, "backbone row")
        require(len({r["reader_initial_sha256"] for r in records if r["reader_seed"]==seed})==1, "reader column")
    for key in ("backbone_initial_sha256","reader_initial_sha256"):
        require(len({r[key] for r in records})==3, "distinct components")


def diagonal_checks(records,anchors,data,evaluation,c):
    require(len(anchors)==3 and [r["initial_seed"] for r in anchors]==list(LEVELS)
            and all(r["order_seed"]==ORDER for r in anchors), "anchor identities")
    checks=[]
    for seed,old in zip(LEVELS,anchors,strict=True):
        row=[r for r in records if r["backbone_seed"]==r["reader_seed"]==seed]
        require(len(row)==1, "diagonal coverage"); new=row[0]
        require(new["initial_sha256"]==old["initial_sha256"] and new["final_sha256"]==old["final_sha256"], "diagonal fingerprints")
        require(new["fit"]["ce_history"]==old["fit"]["ce_history"]
                and new["fit"]["event_sha256"]==old["fit"]["event_sha256"]
                and torch.equal(new["fit"]["schedule_events"],old["fit"]["schedule_events"]), "diagonal training reproduction")
        error=evaluation.replay_error(new["raw"],old["raw"],data,c)
        require(type(error) in (int,float) and math.isfinite(error) and 0<=error<=1e-9, "diagonal logits")
        checks.append(dict(seed=seed,order_seed=ORDER,matched=True,max_logit_error=error))
    return checks


def analyze(records,anchors,data,parent,pair_source,diagnostic,evaluation,transfer,c):
    check_components(records); metrics=[]; parts=[]; results=[]
    for r in records:
        identity=dict(backbone_seed=r["backbone_seed"],reader_seed=r["reader_seed"])
        require(r["parameters"]==14256 and r["initial_sha256"]!=r["final_sha256"] and r["checkpoint_roundtrip"] is True, "record integrity")
        error=r["reload_max_error"]
        require(type(error) in (int,float) and math.isfinite(error) and 0<=error<=1e-9, "replay")
        keys=("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in keys) and tuple(r[k] for k in keys)==(881,46176,3524,81,7776,324), "counts")
        parent.check_fit(r["fit"],ORDER,data,pair_source); require(set(r["raw"])==set(TASKS), "tasks")
        scored=dict(two_char=c.p267.score(data,r["raw"]["two_char"]),triple=c.c270.score(data,r["raw"]["triple"],c.p267),quad=transfer.score_quad(data,r["raw"]["quad"],c))
        flags={t+"_pass":scored[t]["passed"] for t in TASKS}; require(all(type(v) is bool for v in flags.values()), "flags")
        direct={}
        for task in TASKS:
            normalized=diagnostic.normalize_task(scored[task],task,r["backbone_seed"],"reader_"+str(r["reader_seed"]))
            for split in ("TRAIN","HOLDOUT"):
                part=diagnostic.partition([x for x in normalized if x["split"]==split]); direct[(task,split)]=part["direct_pass"]
                parts.append(dict(**identity,task=task,split=split,**part))
        results.append(dict(**identity,**flags,all_tasks_pass=all(flags.values()),
            fitted_train_direct_pass=all(direct[(t,"TRAIN")] for t in TASKS[:2]),seen_holdout_direct_pass=all(direct[(t,"HOLDOUT")] for t in TASKS[:2])))
        metrics.append(dict(**identity,**scored))
    diagonals=diagonal_checks(records,anchors,data,evaluation,c); grids=[]
    for task,split,field in itertools.product(TASKS,("TRAIN","HOLDOUT"),("accuracy","final_normal_nll")):
        values=[p["correct"]/p["rows"] if field=="accuracy" else p[field] for p in parts if p["task"]==task and p["split"]==split]
        require(len(values)==9, "numeric grid"); decomposition=parent.decompose([values[i:i+3] for i in (0,3,6)])
        for old,new in (("initial_means","backbone_means"),("order_means","reader_means"),("initial_ss","backbone_ss"),("order_ss","reader_ss")):
            decomposition[new]=decomposition.pop(old)
        grids.append(dict(task=task,split=split,metric=field,**decomposition))
    matrices={t:[[results[3*i+j][t+"_pass"] for j in range(3)] for i in range(3)] for t in TASKS}
    summary=dict(cell_results=results,final_partitions=parts,grids=grids,task_pass_matrices=matrices,diagonal_checks=diagonals,
        diagnostic_complete=True,capability_gate_applicable=False,all_replays=True,components_matched=True,**WORK)
    require(len(parts)==54 and len(grids)==12, "inventory"); return metrics,summary


def load_parent(paths):
    parent,pair_source,audit,*_,c=context(); paths=[Path(p).resolve() for p in paths]
    hashes=(PARENT_SHA,*parent.parent_hashes(pair_source))
    require(len(paths)==len(hashes)==24 and all(c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)), "parent hashes")
    with audit.no_neural():
        payload,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION); parent.validate_result(payload)
        require(payload["experiment_id"]=="C297-v5b-initialization-order-grid" and payload["commit_sha"]==PARENT_EXECUTION
                and payload["status"]=="PASS" and payload["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB, "parent identity")
        s=payload["validation_summary"]
        expected={"two_char":[[True]*3 for _ in range(3)],"triple":[[True]*3 for _ in range(3)],"quad":[[True]*3,[False]*3,[True]*3]}
        require(s["task_pass_matrices"]==expected and s["diagnostic_complete"] is True
                and s["capability_gate_applicable"] is False and s["grid_matched"] is True and s["all_replays"] is True, "parent outcome")
        require(len(payload["artifacts"])==8 and {a["file"] for a in payload["artifacts"]}==set(OUTPUTS), "parent outputs")
        data=[c.audit.read_json(paths[0].parent/n) for n in OUTPUTS[1:4]]
        require(tuple(map(digest,data))==DATA_HASHES, "data hashes")
        archive=torch.load(paths[0].parent/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c297-grid-eval-v1", "parent archive")
        parent.check_grid(archive["records"])
        anchors=[r for r in archive["records"] if r["order_seed"]==ORDER]
        require([r["initial_seed"] for r in anchors]==list(LEVELS), "anchor coverage")
    return payload,*data,anchors


def precheck(paths,root):
    validate_seal(); payload,*_=load_parent(paths); parent,pair_source,audit,*_,c=context(); root=Path(root).resolve()
    pins=dict(payload["source_blobs"]); protected=dict(payload["input_sha256"])
    require((len(pins),len(protected))==(628,1146), "inherited counts")
    for n,h in pins.items(): require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h, "changed source:"+n)
    for n,h in protected.items(): require(Path(n).is_file() and c.audit.sha(n)==h, "changed input:"+n)
    covered=set()
    for module in [parent,pair_source,audit,*parent.context(),*vars(c).values()]:
        path=getattr(module,"__file__",None) if isinstance(module,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            n=Path(path).resolve().relative_to(root).as_posix(); require(n in pins,"unprotected helper:"+n); covered.add(n)
    require(PARENT_SOURCE in covered and pins[PARENT_SOURCE]==PARENT_BLOB, "parent coverage")
    for path,h in [(Path(paths[0]).resolve(),PARENT_SHA)]+[(c.audit.safe_child(Path(paths[0]).resolve().parent,a["file"]),a["sha256"]) for a in payload["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h, "parent input"); protected[str(path.resolve())]=h
    for n in OWN:
        require(n not in pins,"OWN collision"); pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins)); require((len(pins),len(protected))==(634,1161), "protection counts")
    print(f"registration_check = source_pins:634; protected_inputs:1161; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def runtime_preflight(paths,root):
    precheck(paths,root); parent,pair_source,*_,training,c=context(); _,data,_,_,anchors=load_parent(paths)
    require(tuple(parent.INITIALS)==LEVELS and tuple(parent.ORDERS)==(297101,297102,297103) and parent.FIT_RNG==FIT_RNG, "parent factors")
    tokens,targets=training.training_tables(data,c); plan=parent.schedule(ORDER,data["TRAIN"],pair_source.pairs_from_rows)
    x,y=pair_source.render_batch(tokens,targets,plan[0]); require(x.shape==(48,48) and y.shape==(48,), "real batch")
    models=make_grid(c)
    for old in anchors:
        seed=old["initial_seed"]
        require(c.base.fingerprint(models[(seed,seed)])==old["initial_sha256"]
                and torch.equal(plan,old["fit"]["schedule_events"]), "real diagonal initial/schedule")
    print("real_component_grid_and_diagonal_initialization = PASS; science not started",flush=True)


def validate_result(payload):
    require(payload["experiment_id"]==EXPERIMENT_ID and payload["stage"]==STAGE and payload["status"]=="PASS"
            and payload["diagnostic_execution_valid"] is True, "diagnostic identity")
    require(all(payload[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")), "claim scope")
    require((len(payload["source_blobs"]),len(payload["input_sha256"]))==(634,1161) and set(OWN)<=set(payload["source_blobs"])
            and payload["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB, "result protection")
    require(len(payload["artifacts"])==8 and {a["file"] for a in payload["artifacts"]}==set(OUTPUTS), "outputs")
    s=payload["validation_summary"]; rr=s["cell_results"]
    require([(r["backbone_seed"],r["reader_seed"]) for r in rr]==identities(), "result grid")
    require(all(type(r[t+"_pass"]) is bool for r in rr for t in TASKS)
            and all(r["all_tasks_pass"] is all(r[t+"_pass"] for t in TASKS) for r in rr), "flags")
    require(s["task_pass_matrices"]=={t:[[rr[3*i+j][t+"_pass"] for j in range(3)] for i in range(3)] for t in TASKS}, "matrices")
    require(len(s["final_partitions"])==54 and len(s["grids"])==12 and [v["seed"] for v in s["diagonal_checks"]]==list(LEVELS), "inventory")
    require(all(v["matched"] is True and v["order_seed"]==ORDER and math.isfinite(v["max_logit_error"])
                and 0<=v["max_logit_error"]<=1e-9 for v in s["diagonal_checks"]), "diagonal attestation")
    require(s["diagnostic_complete"] is True and s["all_replays"] is True and s["components_matched"] is True
            and s["capability_gate_applicable"] is False, "diagnostic flags")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()), "workload")


def load_bundle(path):
    value=torch.load(path,map_location="cpu",weights_only=True)
    require(set(value)=={"schema","identities","states"} and value["schema"]=="fold-c298-components-models-v1"
            and value["identities"]==[list(i) for i in identities()] and len(value["states"])==9, "model bundle")
    return value["states"]


def flatten(suite):
    for test in suite:
        if isinstance(test,unittest.TestSuite): yield from flatten(test)
        else: yield test


def regression_modules(root):
    names=context()[0].regression_modules(root); require(len(names)==len(set(names))==182, "parent modules")
    return names+["tests_lm.test_v05_c298_component_initialization"]


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
    parent,pair_source,_,diagnostic,evaluation,transfer,training,c=context(); root=Path(__file__).resolve().parents[2]
    guard(root,expected_head,c); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected=precheck(summaries,root); _,data,triple,quad,anchors=load_parent(summaries)
    tokens,targets=training.training_tables(data,c); out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    models=make_grid(c); records=[]; states=[]
    for bs,rs in identities():
        print(f"[C298] cell={len(records)+1}/9 backbone={bs} reader={rs}",flush=True)
        record,state=train_cell(models[(bs,rs)],data,triple,quad,tokens,targets,bs,rs,parent,pair_source,evaluation,transfer,c)
        records.append(record); states.append(state)
    diagonal_checks(records,anchors,data,evaluation,c)
    torch.save(dict(schema="fold-c298-components-models-v1",identities=[list(i) for i in identities()],states=states),out/"trained-models.pt")
    loaded=load_bundle(out/"trained-models.pt"); replay_models=make_grid(c)
    for k,key in enumerate(identities()): evaluation.replay_one(replay_models[key],loaded[k],records[k],data,triple,quad,transfer,c)
    metrics,summary=analyze(records,anchors,data,parent,pair_source,diagnostic,evaluation,transfer,c)
    torch.save(dict(schema="fold-c298-components-eval-v1",records=records),out/"evaluations.pt")
    for n,v in (("architecture-plan.json",manifest()),("dataset.json",data),("triple-dataset.json",triple),
                ("quad-dataset.json",quad),("measurements.json",metrics),("validation-summary.json",summary)):
        (out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c); precheck(summaries,root)
    payload=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(payload); (out/"summary.json").write_bytes(blob(payload))
    receipt={k:payload[k] for k in ("experiment_id","stage","commit_sha","status","diagnostic_execution_valid","artifacts")}
    receipt["summary_sha256"]=c.audit.sha(out/"summary.json")
    print("=== C298 COMPACT DIAGNOSTIC RECEIPT ===",flush=True); print(json.dumps(receipt,sort_keys=True,indent=2),flush=True)
    return payload


def verify_artifacts(outdir,summaries,expected_head):
    parent,pair_source,audit,diagnostic,evaluation,transfer,_,c=context(); out=Path(outdir)
    payload=c.audit.read_json(out/"summary.json"); validate_result(payload); require(payload["commit_sha"]==expected_head, "execution HEAD")
    for n,h in payload["input_sha256"].items(): require(c.audit.sha(n)==h, "protected input")
    for a in payload["artifacts"]:
        path=c.audit.safe_child(out,a["file"]); require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"], "output bytes")
    with audit.no_neural():
        _,data,triple,quad,anchors=load_parent(summaries)
        for n,v in zip(OUTPUTS[1:4],(data,triple,quad),strict=True): require(c.audit.read_json(out/n)==v, "persisted data")
        archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c298-components-eval-v1", "evaluation archive")
        metrics,summary=analyze(archive["records"],anchors,data,parent,pair_source,diagnostic,evaluation,transfer,c)
        for n,v in (("architecture-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):
            require(c.audit.read_json(out/n)==v, "persisted:"+n)
    require(summary==payload["validation_summary"], "summary reconstruction"); return payload,metrics


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--summaries",nargs=24,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True); parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
