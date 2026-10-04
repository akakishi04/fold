"""C299: initialized recurrent core crossed with the remaining backbone; fixed reader."""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import sys
from types import ModuleType
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C299-v5b-core-initialization-grid"
STAGE = "V5-B-CORE-INITIALIZATION-GRID"
BASE = "315e24172119cd85f040def1ca01a7e4c6a0dfed"
PARENT_EXECUTION = "026dc1983cbdf7c54e6bb6ba6302f04430b17a36"
PARENT_SHA = "a57e5f2fc3071c630b6cd083f855511b035a4d8478c91e22f86fe97c373add6e"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c298_component_initialization.py"
PARENT_BLOB = "a1f64f270dcba45e25168841d76113a1b195aebc"
LEVELS = (297001, 297002, 297003)
READER_SEED, ORDER, FIT_RNG = 297001, 297101, 597000
TASKS = ("two_char", "triple", "quad")
OWN = ("fold_lm/v05_benchmarks/model_c299_core_initialization.py",
       "tests_lm/test_v05_c299_core_initialization.py", "tools/run_c299.ps1", "tools/invoke_c299.ps1",
       "docs/experiment-ledger-addendum-c299-preregistration.md", "docs/v5b-core-initialization-v0.1.md")
OUTPUTS = ("architecture-plan.json", "dataset.json", "triple-dataset.json", "quad-dataset.json",
           "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=9, train_steps=7200, training_rows=345600, model_forward_calls=8658,
            row_presentations=485568, core_forward_calls=34632, model_state_loads=9,
            checkpoint_bundle_loads=1, new_checkpoint_writes=1, network_calls=0)
DATA_HASHES = ("1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
               "432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",
               "86bcb41813fc76896e54abb4991675acbaba085bfde382c6683d8e62cd15876b")
MANIFEST_SHA = "796fc20a254a8d65111d22f4b2754ae12f43975d869c9ca2fd8b7a6e90c7e846"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(LEVELS,LEVELS))


def context():
    from fold_lm.v05_benchmarks import model_c298_component_initialization as parent
    grid_parent,pair_source,audit,diagnostic,evaluation,transfer,training,c = parent.context()
    return parent,grid_parent,pair_source,audit,diagnostic,evaluation,transfer,training,c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_summary_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,
        question="does fixed-reader/fixed-order transfer follow recurrent-core initialization or remaining-backbone initialization",
        levels=list(LEVELS),reader_seed=READER_SEED,order_seed=ORDER,fit_rng=FIT_RNG,
        parameters=14256,core_parameters=3328,remaining_backbone_parameters=10160,reader_parameters=768,max_tokens=48,
        intervention="cross UNTRAINED backbone.core with all other backbone state;added read initialized identically;all parameters trained",
        schedule="exact C297 order297101;blocked200epochs*4;100 exposures per row per trained length",
        loss="ordinary mean CE",optimizer="AdamW",lr=.005,betas=[.9,.999],eps=1e-8,weight_decay=0.,clip=1.,steps_per_cell=800,
        diagonals="all three reproduce C298 reader297001:exact initial/final hashes,800 losses,events;all-view logits<=1e-9 and exact argmax",
        diagnostic_gate="complete9 cells,component provenance,diagonal reproduction,strict replay,saved reconstruction only",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        reports="9 results,3 task matrices,54 partitions,12 finite-grid accuracy/NLL decompositions",
        limits="same three observed levels,one order and reader;not fresh replication,population variance,core necessity or architectural superiority",
        parents=25,source_pins=640,protected_inputs=1176,own_tests=32,modules=184,loaded_tests=4558,focused_tests=4557,
        excluded_test=EXCLUDED,data_hashes=list(DATA_HASHES),dtype="CPU float64",threads=2,deterministic=True,
        capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def remaining_fingerprint(backbone):
    h=hashlib.sha256(); entries=0
    for name,tensor in sorted(backbone.state_dict().items()):
        if name.startswith("core."): continue
        value=tensor.detach().cpu().contiguous()
        h.update(name.encode("utf-8"));h.update(str(value.dtype).encode());h.update(str(tuple(value.shape)).encode());h.update(value.numpy().tobytes());entries+=1
    require(entries>0,"empty remaining backbone")
    return h.hexdigest()


def make_grid(c):
    refs={s:c.c278.MeanFinalDualReadout(c.factory.new_model(s),s,c.reader,c.c269.query_span_mask) for s in LEVELS}
    for m in refs.values():
        require(set(m._modules)=={"backbone","read"} and isinstance(m.backbone.core,torch.nn.Module),"component boundary")
        require(sum(p.numel() for p in m.backbone.parameters())==13488 and sum(p.numel() for p in m.backbone.core.parameters())==3328
                and sum(p.numel() for n,p in m.backbone.named_parameters() if not n.startswith("core."))==10160
                and sum(p.numel() for p in m.read.parameters())==768,"component sizes")
        require(all(k.startswith(("backbone.","read.")) for k in m.state_dict()),"state coverage")
    require(len({c.base.fingerprint(m.backbone.core) for m in refs.values()})==3,"distinct cores")
    require(len({remaining_fingerprint(m.backbone) for m in refs.values()})==3,"distinct remaining backbones")
    grid={};used=set()
    for rest,core in identities():
        m=copy.deepcopy(refs[rest]);m.backbone.core=copy.deepcopy(refs[core].backbone.core);m.read=copy.deepcopy(refs[READER_SEED].read)
        require(type(m) is c.c278.MeanFinalDualReadout and sum(p.numel() for p in m.parameters())==14256,"architecture")
        require(all(p.dtype==torch.float64 and p.device.type=="cpu" for p in m.parameters()),"precision")
        require(remaining_fingerprint(m.backbone)==remaining_fingerprint(refs[rest].backbone)
                and c.base.fingerprint(m.backbone.core)==c.base.fingerprint(refs[core].backbone.core)
                and c.base.fingerprint(m.read)==c.base.fingerprint(refs[READER_SEED].read),"component provenance")
        require(list(m.state_dict())==list(refs[rest].state_dict()),"state order")
        ptrs={p.data_ptr() for p in m.parameters()};require(not ptrs&used,"shared storage");used.update(ptrs)
        grid[(rest,core)]=m
    return grid


def fit(model,data,tokens,targets,rest,core,grid_parent,pair_source):
    require((rest,core) in identities(),"cell identity")
    require(tokens.shape==(2,3,192,48) and targets.shape==(192,) and tokens.dtype==targets.dtype==torch.int64,"tables")
    require(torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)),"target alignment")
    events=grid_parent.schedule(ORDER,data["TRAIN"],pair_source.pairs_from_rows)
    torch.manual_seed(FIT_RNG);opt=torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    model.train();losses=[]
    for step in range(800):
        require(len(opt.param_groups)==1 and opt.param_groups[0]["lr"]==.005,"constant LR")
        opt.zero_grad(set_to_none=True);x,y=pair_source.render_batch(tokens,targets,events[step]);z=model(x,torch.zeros(48,dtype=torch.int64))
        require(z.shape==(48,256) and z.dtype==torch.float64 and bool(torch.isfinite(z).all()),"logits")
        loss=F.cross_entropy(z,y);require(bool(torch.isfinite(loss)),"finite loss")
        losses.append(float(loss.detach()));loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True);opt.step()
        if (step+1)%200==0:print(f"[C299] remaining={rest} core={core} step={step+1}/800 ce={losses[-1]:.6f}",flush=True)
    model.eval()
    return dict(steps=800,training_rows=38400,optimizer_creations=1,fit_rng=FIT_RNG,ce_history=losses,event_sha256=digest(events.tolist()),schedule_events=events)


def train_cell(model,data,triple,quad,tokens,targets,rest,core,grid_parent,pair_source,evaluation,transfer,c):
    start=c.base.fingerprint(model);rr=remaining_fingerprint(model.backbone);cc=c.base.fingerprint(model.backbone.core);read=c.base.fingerprint(model.read)
    with c.p267.counted(model,c.core) as (calls,cores):
        fitted=fit(model,data,tokens,targets,rest,core,grid_parent,pair_source);final=c.base.fingerprint(model);model.requires_grad_(False)
        raw=evaluation.evaluate(model,data,triple,quad,transfer,c)
    require(calls==[881,46176] and cores[0]==3524,"train/evaluation counts")
    require(start!=final and rr!=remaining_fingerprint(model.backbone) and cc!=c.base.fingerprint(model.backbone.core)
            and read!=c.base.fingerprint(model.read) and final==c.base.fingerprint(model),"weights")
    return dict(remaining_seed=rest,core_seed=core,reader_seed=READER_SEED,initial_sha256=start,remaining_initial_sha256=rr,
        core_initial_sha256=cc,reader_initial_sha256=read,final_sha256=final,parameters=14256,fit=fitted,raw=raw,
        forward_calls=881,row_presentations=46176,core_forward_calls=3524),{k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def check_grid(records):
    require([(r["remaining_seed"],r["core_seed"]) for r in records]==identities(),"complete grid")
    require(len({r["fit"]["event_sha256"] for r in records})==1 and all(r["reader_seed"]==READER_SEED for r in records)
            and len({r["reader_initial_sha256"] for r in records})==1,"fixed reader/schedule")
    for seed in LEVELS:
        require(len({r["remaining_initial_sha256"] for r in records if r["remaining_seed"]==seed})==1,"remaining row")
        require(len({r["core_initial_sha256"] for r in records if r["core_seed"]==seed})==1,"core column")
    for key in ("remaining_initial_sha256","core_initial_sha256"):require(len({r[key] for r in records})==3,"distinct levels")


def diagonal_checks(records,anchors,data,evaluation,c):
    require(len(anchors)==3 and [r["backbone_seed"] for r in anchors]==list(LEVELS)
            and all(r["reader_seed"]==READER_SEED for r in anchors),"anchor identities")
    checks=[]
    for seed,old in zip(LEVELS,anchors,strict=True):
        rows=[r for r in records if r["remaining_seed"]==r["core_seed"]==seed];require(len(rows)==1,"diagonal coverage");new=rows[0]
        require(new["initial_sha256"]==old["initial_sha256"] and new["final_sha256"]==old["final_sha256"],"diagonal fingerprints")
        require(new["fit"]["ce_history"]==old["fit"]["ce_history"] and new["fit"]["event_sha256"]==old["fit"]["event_sha256"]
                and torch.equal(new["fit"]["schedule_events"],old["fit"]["schedule_events"]),"diagonal training")
        error=evaluation.replay_error(new["raw"],old["raw"],data,c)
        require(type(error) in (int,float) and math.isfinite(error) and 0<=error<=1e-9,"diagonal logits")
        checks.append(dict(seed=seed,reader_seed=READER_SEED,matched=True,max_logit_error=error))
    return checks


def analyze(records,anchors,data,grid_parent,pair_source,diagnostic,evaluation,transfer,c):
    check_grid(records);metrics=[];parts=[];results=[]
    for r in records:
        identity=dict(remaining_seed=r["remaining_seed"],core_seed=r["core_seed"])
        require(r["parameters"]==14256 and r["initial_sha256"]!=r["final_sha256"] and r["checkpoint_roundtrip"] is True,"record integrity")
        err=r["reload_max_error"];require(type(err) in (int,float) and math.isfinite(err) and 0<=err<=1e-9,"replay")
        keys=("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in keys) and tuple(r[k] for k in keys)==(881,46176,3524,81,7776,324),"counts")
        grid_parent.check_fit(r["fit"],ORDER,data,pair_source);require(set(r["raw"])==set(TASKS),"tasks")
        scored=dict(two_char=c.p267.score(data,r["raw"]["two_char"]),triple=c.c270.score(data,r["raw"]["triple"],c.p267),quad=transfer.score_quad(data,r["raw"]["quad"],c))
        flags={t+"_pass":scored[t]["passed"] for t in TASKS};require(all(type(v) is bool for v in flags.values()),"flags");direct={}
        for task in TASKS:
            normalized=diagnostic.normalize_task(scored[task],task,r["remaining_seed"],"core_"+str(r["core_seed"]))
            for split in ("TRAIN","HOLDOUT"):
                part=diagnostic.partition([x for x in normalized if x["split"]==split]);direct[(task,split)]=part["direct_pass"]
                parts.append(dict(**identity,task=task,split=split,**part))
        results.append(dict(**identity,**flags,all_tasks_pass=all(flags.values()),
            fitted_train_direct_pass=all(direct[(t,"TRAIN")] for t in TASKS[:2]),seen_holdout_direct_pass=all(direct[(t,"HOLDOUT")] for t in TASKS[:2])))
        metrics.append(dict(**identity,**scored))
    diagonals=diagonal_checks(records,anchors,data,evaluation,c);grids=[]
    for task,split,field in itertools.product(TASKS,("TRAIN","HOLDOUT"),("accuracy","final_normal_nll")):
        values=[p["correct"]/p["rows"] if field=="accuracy" else p[field] for p in parts if p["task"]==task and p["split"]==split]
        require(len(values)==9,"numeric grid");d=grid_parent.decompose([values[i:i+3] for i in (0,3,6)])
        for old,new in (("initial_means","remaining_means"),("order_means","core_means"),("initial_ss","remaining_ss"),("order_ss","core_ss")):d[new]=d.pop(old)
        grids.append(dict(task=task,split=split,metric=field,**d))
    matrices={t:[[results[3*i+j][t+"_pass"] for j in range(3)] for i in range(3)] for t in TASKS}
    summary=dict(cell_results=results,final_partitions=parts,grids=grids,task_pass_matrices=matrices,diagonal_checks=diagonals,
        diagnostic_complete=True,capability_gate_applicable=False,all_replays=True,components_matched=True,**WORK)
    require(len(parts)==54 and len(grids)==12,"inventory");return metrics,summary


def parent_hashes(parent):
    p297,p296,*_=parent.context()
    return (PARENT_SHA,parent.PARENT_SHA,*p297.parent_hashes(p296))


def load_parent(paths):
    parent,_,_,audit,*_,c=context();paths=[Path(p).resolve() for p in paths];hashes=parent_hashes(parent)
    require(len(paths)==len(hashes)==25 and all(c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)),"parent hashes")
    with audit.no_neural():
        p,_=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION);parent.validate_result(p)
        require(p["experiment_id"]=="C298-v5b-component-initialization-grid" and p["commit_sha"]==PARENT_EXECUTION
                and p["status"]=="PASS" and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"parent identity")
        s=p["validation_summary"];expected={"two_char":[[True]*3 for _ in LEVELS],"triple":[[True]*3 for _ in LEVELS],"quad":[[True]*3,[False]*3,[True]*3]}
        require(s["task_pass_matrices"]==expected and s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False
                and s["components_matched"] is True and s["all_replays"] is True,"parent outcome")
        require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"parent outputs")
        data=[c.audit.read_json(paths[0].parent/n) for n in OUTPUTS[1:4]];require(tuple(map(digest,data))==DATA_HASHES,"data hashes")
        archive=torch.load(paths[0].parent/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c298-components-eval-v1","parent archive")
        parent.check_components(archive["records"])
        anchors=[r for r in archive["records"] if r["reader_seed"]==READER_SEED]
        require([r["backbone_seed"] for r in anchors]==list(LEVELS),"anchor coverage")
    return p,*data,anchors


def precheck(paths,root):
    validate_seal();p,*_=load_parent(paths);parent,_,_,audit,*_,c=context();root=Path(root).resolve()
    pins=dict(p["source_blobs"]);protected=dict(p["input_sha256"]);require((len(pins),len(protected))==(634,1161),"inherited counts")
    for n,h in pins.items():require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in protected.items():require(Path(n).is_file() and c.audit.sha(n)==h,"changed input:"+n)
    covered=set()
    for module in [parent,audit,*parent.context(),*vars(c).values()]:
        path=getattr(module,"__file__",None) if isinstance(module,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):
            n=Path(path).resolve().relative_to(root).as_posix();require(n in pins,"unprotected helper:"+n);covered.add(n)
    require(PARENT_SOURCE in covered and pins[PARENT_SOURCE]==PARENT_BLOB,"parent coverage")
    for path,h in [(Path(paths[0]).resolve(),PARENT_SHA)]+[(c.audit.safe_child(Path(paths[0]).resolve().parent,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h,"parent input");protected[str(path.resolve())]=h
    for n in OWN:require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins));require((len(pins),len(protected))==(640,1176),"protection counts")
    print(f"registration_check = source_pins:640; protected_inputs:1176; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def runtime_preflight(paths,root):
    pins,_=precheck(paths,root);parent,grid_parent,pair_source,*_,training,c=context();_,data,_,_,anchors=load_parent(paths)
    require(tuple(parent.LEVELS)==LEVELS and parent.ORDER==ORDER and parent.FIT_RNG==FIT_RNG,"parent factors")
    tokens,targets=training.training_tables(data,c);plan=grid_parent.schedule(ORDER,data["TRAIN"],pair_source.pairs_from_rows)
    x,y=pair_source.render_batch(tokens,targets,plan[0]);require(x.shape==(48,48) and y.shape==(48,),"real batch")
    models=make_grid(c)
    for old in anchors:
        s=old["backbone_seed"];m=models[(s,s)]
        require(c.base.fingerprint(m)==old["initial_sha256"] and torch.equal(plan,old["fit"]["schedule_events"]),"real diagonal initial/schedule")
        module=sys.modules[type(m.backbone.core).__module__];path=Path(module.__file__).resolve()
        if path.is_relative_to(Path(root).resolve()):require(path.relative_to(Path(root).resolve()).as_posix() in pins,"core implementation pin")
    print("real_core_remaining_grid_and_diagonal_initialization = PASS; science not started",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS" and p["diagnostic_execution_valid"] is True,"result identity")
    require(all(p[k] is False for k in ("capability_gate_applicable","gate_f_candidate","production_adoption")),"scope")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(640,1176) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB,"result protection")
    require(len(p["artifacts"])==8 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"outputs")
    s=p["validation_summary"];rr=s["cell_results"]
    require([(r["remaining_seed"],r["core_seed"]) for r in rr]==identities(),"result grid")
    require(all(type(r[t+"_pass"]) is bool for r in rr for t in TASKS) and all(r["all_tasks_pass"] is all(r[t+"_pass"] for t in TASKS) for r in rr),"flags")
    require(s["task_pass_matrices"]=={t:[[rr[3*i+j][t+"_pass"] for j in range(3)] for i in range(3)] for t in TASKS},"matrices")
    require(len(s["final_partitions"])==54 and len(s["grids"])==12 and [v["seed"] for v in s["diagonal_checks"]]==list(LEVELS),"inventory")
    require(all(v["matched"] is True and v["reader_seed"]==READER_SEED and math.isfinite(v["max_logit_error"]) and 0<=v["max_logit_error"]<=1e-9 for v in s["diagonal_checks"]),"diagonals")
    require(s["diagnostic_complete"] is True and s["all_replays"] is True and s["components_matched"] is True and s["capability_gate_applicable"] is False,"diagnostic flags")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"workload")


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c299-core-models-v1" and v["identities"]==[list(i) for i in identities()] and len(v["states"])==9,"bundle")
    return v["states"]


def flatten(suite):
    for t in suite:
        if isinstance(t,unittest.TestSuite):yield from flatten(t)
        else:yield t


def regression_modules(root):
    names=context()[0].regression_modules(root);require(len(names)==len(set(names))==183,"parent modules")
    return names+["tests_lm.test_v05_c299_core_initialization"]


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==manifest()["loaded_tests"] and ids.count(EXCLUDED)==1,"loaded suite")
    kept=[t for t in tests if t.id()!=EXCLUDED];require(len(kept)==manifest()["focused_tests"],"focused suite");return unittest.TestSuite(kept)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    _,gp,ps,_,diag,evaluation,transfer,training,c=context();root=Path(__file__).resolve().parents[2]
    guard(root,expected_head,c);torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(summaries,root);_,data,triple,quad,anchors=load_parent(summaries);tokens,targets=training.training_tables(data,c)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);models=make_grid(c);records=[];states=[]
    for rest,core in identities():
        print(f"[C299] cell={len(records)+1}/9 remaining={rest} core={core}",flush=True)
        r,state=train_cell(models[(rest,core)],data,triple,quad,tokens,targets,rest,core,gp,ps,evaluation,transfer,c);records.append(r);states.append(state)
    diagonal_checks(records,anchors,data,evaluation,c)
    torch.save(dict(schema="fold-c299-core-models-v1",identities=[list(i) for i in identities()],states=states),out/"trained-models.pt")
    loaded=load_bundle(out/"trained-models.pt");replays=make_grid(c)
    for i,key in enumerate(identities()):evaluation.replay_one(replays[key],loaded[i],records[i],data,triple,quad,transfer,c)
    metrics,summary=analyze(records,anchors,data,gp,ps,diag,evaluation,transfer,c)
    torch.save(dict(schema="fold-c299-core-eval-v1",records=records),out/"evaluations.pt")
    for n,v in (("architecture-plan.json",manifest()),("dataset.json",data),("triple-dataset.json",triple),("quad-dataset.json",quad),("measurements.json",metrics),("validation-summary.json",summary)):(out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS];guard(root,expected_head,c);precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,
        artifacts=artifacts,validation_summary=summary,capability_gate_applicable=False,gate_f_candidate=False,production_adoption=False)
    validate_result(p);(out/"summary.json").write_bytes(blob(p));receipt={k:p[k] for k in ("experiment_id","stage","commit_sha","status","diagnostic_execution_valid","artifacts")}
    receipt["summary_sha256"]=c.audit.sha(out/"summary.json");print("=== C299 COMPACT DIAGNOSTIC RECEIPT ===",flush=True);print(json.dumps(receipt,sort_keys=True,indent=2),flush=True);return p


def verify_artifacts(outdir,summaries,expected_head):
    _,gp,ps,audit,diag,evaluation,transfer,_,c=context();out=Path(outdir);p=c.audit.read_json(out/"summary.json");validate_result(p);require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items():require(c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"]);require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with audit.no_neural():
        _,data,triple,quad,anchors=load_parent(summaries)
        for n,v in zip(OUTPUTS[1:4],(data,triple,quad),strict=True):require(c.audit.read_json(out/n)==v,"persisted data")
        archive=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c299-core-eval-v1","archive")
        metrics,s=analyze(archive["records"],anchors,data,gp,ps,diag,evaluation,transfer,c)
        for n,v in (("architecture-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",s)):require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(s==p["validation_summary"],"summary reconstruction");return p,metrics


def main():
    p=argparse.ArgumentParser();p.add_argument("--summaries",nargs=25,type=Path,required=True);p.add_argument("--output-dir",type=Path,required=True);p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__=="__main__":main()
