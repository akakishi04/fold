"""C306: paired full versus frozen-core training at lengths2/3/4; evaluate unseen5."""
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

EXPERIMENT_ID = "C306-v5b-broad-length-core-freeze"
STAGE = "V5-B-BROAD-LENGTH-CORE-FREEZE"
BASE = "73282101c89ac14cf5aa55d6d91c4bedc87b176d"
PARENT_EXECUTION = "9c8beb3c66548c1e68def4ea2ced93acc0067e6e"
PARENT_SHA = "dd8580fe7f544b2e94688c4236cb862cfc77bb57984b04e5116a2c2cd8cc4734"
PARENT_SOURCE = "fold_lm/v05_benchmarks/model_c305_saved_length_overlap.py"
PARENT_BLOB = "e822f5680193951cbc9270cb70cb0d4d5fcb12b6"
WIDE_SOURCE = "fold_lm/v05_benchmarks/model_c304_length_breadth.py"
WIDE_BLOB = "cacb5852a29171aa8079e634d929fdd54e7f4f58"
SEEDS = tuple(range(306001,306006))
ORDERS = tuple(range(306101,306106))
ARMS = ("full_train","core_frozen")
LENGTHS = (2,3,4,5)
STEPS,SLOTS,FIT_RNG = 1200,64,612000
OWN = ("fold_lm/v05_benchmarks/model_c306_broad_length_core_freeze.py",
       "tests_lm/test_v05_c306_broad_length_core_freeze.py","tools/run_c306.ps1","tools/invoke_c306.ps1",
       "docs/experiment-ledger-addendum-c306-preregistration.md","docs/v5b-broad-length-core-freeze-v0.1.md")
OUTPUTS = ("architecture-plan.json","dataset.json","length-datasets.json","trained-models.pt",
           "evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
WORK = dict(models=10,train_steps=12000,training_rows=576000,model_forward_calls=14160,
            row_presentations=783360,core_forward_calls=56640,model_state_loads=10,
            checkpoint_bundle_loads=1,new_checkpoint_writes=1,network_calls=0)
MANIFEST_SHA = "28a55839e6cf0c31ceac29fafb7e535b30d24259a0983589ebd4ae6121080b27"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("utf-8")


def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c305_saved_length_overlap as parent
    wide,c = parent.context()
    _,p301,_,diag,transfer,_ = wide.context()
    pairs = p301.pair_source(p301.context()[0])
    return parent,wide,pairs,diag,transfer,c


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,
        parent_sha256=PARENT_SHA,parent_source=PARENT_SOURCE,parent_blob=PARENT_BLOB,wide_source=WIDE_SOURCE,wide_blob=WIDE_BLOB,
        question="does freezing the random initialized recurrent core improve unseen-five reliability under identical2/3/4 training",
        seeds=list(SEEDS),orders=list(ORDERS),arms=list(ARMS),train_lengths=[2,3,4],eval_lengths=list(LENGTHS),slots=SLOTS,
        parameters=14256,trainable_parameters=dict(full_train=14256,core_frozen=10928),core_parameters=3328,
        changed="requires_grad for backbone.core only;optimizer excludes frozen parameters;no detach or forward change",
        model="exact accepted C304 LengthReadout with actual C278 reference initialization",
        schedule="300epochs*4;private randperm96(order+306000+epoch);length=2+epoch%3;profile=(epoch//3+epoch%3)%3",
        per_row_length_exposure=[100,100,100],profile_updates=[400,400,400],fit_rng=FIT_RNG,
        steps=STEPS,loss="ordinary mean CE",optimizer="AdamW",lr=.005,betas=[.9,.999],eps=1e-8,weight_decay=0.,clip=1.,
        primary="all5 core_frozen states pass every original five-character local and masked criterion",
        gates=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        reports="10 seed records,80 length/split partitions,40 paired normal count contrasts,gradient union/counts,core hashes",
        parents=32,source_pins=682,protected_inputs=1267,own_tests=32,modules=191,loaded_tests=4814,focused_tests=4813,
        excluded_test=EXCLUDED,dtype="CPU float64",threads=2,deterministic=True,
        limitations="different trainable dimension and clipping/backward work;C303/C304 old cohorts not concurrent controls;no core-necessity claim",
        gate_f_candidate=False,production_adoption=False,**WORK)


def validate_seal():
    require(re.fullmatch(r"[0-9a-f]{64}",MANIFEST_SHA) is not None and digest(manifest())==MANIFEST_SHA,"manifest seal")


def configure(model,arm):
    require(arm in ARMS,"arm")
    model.requires_grad_(True)
    if arm==ARMS[1]: model.backbone.core.requires_grad_(False)
    return model


def make_models(seed,wide,c):
    require(seed in SEEDS,"seed")
    ref=c.c278.MeanFinalDualReadout(c.factory.new_model(seed),seed,c.reader,c.c269.query_span_mask)
    template=wide.LengthReadout(ref)
    models={a:configure(copy.deepcopy(template),a) for a in ARMS};seen=set()
    for arm,m in models.items():
        require(type(m) is wide.LengthReadout and m.backbone.config.max_tokens==SLOTS and m.backbone.core.config.slots==SLOTS,"architecture/frame")
        require(sum(p.numel() for p in m.parameters())==14256 and sum(p.numel() for p in m.backbone.core.parameters())==3328,"capacity")
        require(sum(p.numel() for p in m.parameters() if p.requires_grad)==manifest()["trainable_parameters"][arm],"trainable count")
        require(c.base.fingerprint(m)==c.base.fingerprint(ref) and list(m.state_dict())==list(ref.state_dict()),"matched initial states")
        require(all(p.dtype==torch.float64 and p.device.type=="cpu" for p in m.parameters()),"precision")
        ptrs={p.data_ptr() for p in m.parameters()};require(not ptrs&seen,"shared storage");seen.update(ptrs)
    return models


def schedule(seed,rows,pairs):
    require(seed in SEEDS and len(rows)==192,"schedule identity")
    pp=pairs.pairs_from_rows(rows)
    require(pp.shape==(96,2) and pp.dtype==torch.int64 and sorted(pp.flatten().tolist())==list(range(192)),"pair partition")
    for a,b in pp.tolist():
        require(rows[a]["target"]!=rows[b]["target"] and {rows[a]["query"],rows[b]["query"]}==set(rows[a]["entities"])
                and all(rows[a][k]==rows[b][k] for k in ("entities","values","permutation","language")),"intact pair")
    events=torch.empty((STEPS,24,4),dtype=torch.int64);order=ORDERS[SEEDS.index(seed)]
    for epoch in range(300):
        perm=torch.randperm(96,generator=torch.Generator().manual_seed(order+306000+epoch))
        for j in range(4):
            step=epoch*4+j;events[step,:,0]=epoch%3;events[step,:,1]=(epoch//3+epoch%3)%3
            events[step,:,2:]=pp[perm[24*j:24*(j+1)]]
    return events


def first_batch_probe(models,tokens,targets,events):
    """Discarded operational copies; checks no implicit detach of frozen-core inputs."""
    e=events[0];ids=e[:,2:].flatten();x=tokens[e[:,0].repeat_interleave(2),e[:,1].repeat_interleave(2),ids]
    results=[]
    for arm in ARMS:
        m=copy.deepcopy(models[arm]);m.train();m.zero_grad(set_to_none=True)
        z=m(x,torch.zeros(48,dtype=torch.int64));F.cross_entropy(z,targets[ids]).backward()
        grads={n:None if p.grad is None else p.grad.detach().clone() for n,p in m.named_parameters()}
        results.append((z.detach(),grads))
    (a,ga),(b,gb)=results
    require(torch.allclose(a,b,atol=1e-9,rtol=0) and torch.equal(a.argmax(1),b.argmax(1)) and ga.keys()==gb.keys(),"initial outputs")
    max_error=0.;core_receivers=0;encoder_signal=False
    for n,g in ga.items():
        h=gb[n]
        if n.startswith("backbone.core."):
            require(h is None,"frozen core gradient");core_receivers+=g is not None
        else:
            require((g is None)==(h is None),"noncore connectivity")
            if g is not None:
                require(torch.allclose(g,h,atol=1e-9,rtol=0),"noncore gradient:"+n)
                max_error=max(max_error,float((g-h).abs().max()))
                if n.startswith("backbone.local_encoder."): encoder_signal |= bool((h!=0).any())
    require(core_receivers>0 and encoder_signal,"missing backward path")
    return dict(max_logit_error=float((a-b).abs().max()),max_noncore_gradient_error=max_error,
                full_core_gradient_tensors=core_receivers,frozen_core_gradient_tensors=0,encoder_receives_signal=True)


def fit(model,data,tokens,targets,seed,arm,pairs,wide):
    require(arm in ARMS and tokens.shape==(3,3,192,SLOTS) and tokens.dtype==targets.dtype==torch.int64,"fit tables")
    require(torch.equal(targets,torch.tensor([r["target"] for r in data["TRAIN"]],dtype=torch.int64)),"target alignment")
    expected=manifest()["trainable_parameters"][arm]
    require(sum(p.numel() for p in model.parameters() if p.requires_grad)==expected,"fit trainable count")
    require(all(p.requires_grad==(arm==ARMS[0]) for p in model.backbone.core.parameters()),"core freeze policy")
    events=schedule(seed,data["TRAIN"],pairs);stats=wide.schedule_stats(events);torch.manual_seed(FIT_RNG)
    opt=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    model.train();losses=[];counts=[];union={}
    for step,e in enumerate(events):
        require(len(opt.param_groups)==1 and opt.param_groups[0]["lr"]==.005,"constant LR")
        opt.zero_grad(set_to_none=True);ids=e[:,2:].flatten()
        z=model(tokens[e[:,0].repeat_interleave(2),e[:,1].repeat_interleave(2),ids],torch.zeros(48,dtype=torch.int64))
        require(z.shape==(48,256) and bool(torch.isfinite(z).all()),"logits")
        loss=F.cross_entropy(z,targets[ids]);require(bool(torch.isfinite(loss)),"finite loss")
        losses.append(float(loss.detach()));loss.backward()
        received={n:p.numel() for n,p in model.named_parameters() if p.grad is not None}
        require(all(p.grad is None for p in model.backbone.core.parameters()) if arm==ARMS[1] else True,"frozen core received gradient")
        union.update(received);counts.append(sum(received.values()))
        torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad],1.,error_if_nonfinite=True);opt.step()
        if (step+1)%200==0: print(f"[C306] seed={seed} arm={arm} step={step+1}/1200 ce={losses[-1]:.6f} gradient_parameters={counts[-1]}",flush=True)
    model.eval()
    return dict(steps=STEPS,training_rows=57600,optimizer_creations=1,fit_rng=FIT_RNG,trainable_parameters=expected,
                ce_history=losses,gradient_parameter_counts=counts,gradient_union=dict(sorted(union.items())),schedule_events=events,**stats)


def check_fit(f,seed,arm,data,pairs,wide):
    expected=dict(steps=STEPS,training_rows=57600,optimizer_creations=1,fit_rng=FIT_RNG,trainable_parameters=manifest()["trainable_parameters"][arm])
    require(all(type(f[k]) is int and f[k]==v for k,v in expected.items()),"fit metadata")
    events=schedule(seed,data["TRAIN"],pairs);stats=wide.schedule_stats(events)
    require(torch.equal(events,f["schedule_events"]) and all(f[k]==v for k,v in stats.items()),"schedule reconstruction")
    require(f["per_length_row_exposures"]==[[100]*192 for _ in range(3)] and [sum(r[i] for r in f["length_profile_updates"]) for i in range(3)]==[400]*3,"exposure")
    require(len(f["ce_history"])==STEPS and all(type(v) in (int,float) and math.isfinite(v) and v>=0 for v in f["ce_history"]),"loss history")
    union=f["gradient_union"];require(union and all(type(n) is str and type(v) is int and v>0 for n,v in union.items()),"gradient union")
    require(sum(union.values())<=expected["trainable_parameters"] and len(f["gradient_parameter_counts"])==STEPS
            and all(type(v) is int and 0<v<=sum(union.values()) for v in f["gradient_parameter_counts"]),"gradient counts")
    if arm==ARMS[1]: require(not any(n.startswith("backbone.core.") for n in union),"frozen gradient union")


def train_one(model,data,prompts,tokens,targets,seed,arm,pairs,wide,c):
    initial=c.base.fingerprint(model);core_initial=c.base.fingerprint(model.backbone.core)
    with c.p267.counted(model,c.core) as (calls,cores):
        fitted=fit(model,data,tokens,targets,seed,arm,pairs,wide)
        final=c.base.fingerprint(model);core_final=c.base.fingerprint(model.backbone.core)
        model.requires_grad_(False);raw=wide.evaluate(model,prompts,data,c)
    require(calls==[1308,67968] and cores[0]==5232,"train/evaluation counts")
    require(initial!=final and c.base.fingerprint(model)==final and ((core_initial==core_final)==(arm==ARMS[1])),"core/final state")
    return dict(seed=seed,arm=arm,parameters=14256,slots=SLOTS,initial_sha256=initial,final_sha256=final,
                core_initial_sha256=core_initial,core_final_sha256=core_final,fit=fitted,raw=raw,
                forward_calls=1308,row_presentations=67968,core_forward_calls=5232),{n:p.detach().cpu().clone() for n,p in model.state_dict().items()}


def analyze(records,data,pairs,wide,diag,c):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"record cohort")
    metrics=[];parts=[];results=[]
    for r in records:
        arm=r["arm"];check_fit(r["fit"],r["seed"],arm,data,pairs,wide)
        require(r["parameters"]==14256 and r["slots"]==64 and r["initial_sha256"]!=r["final_sha256"]
                and ((r["core_initial_sha256"]==r["core_final_sha256"])==(arm==ARMS[1])) and r["checkpoint_roundtrip"] is True,"record state")
        error=r["reload_max_error"];require(type(error) in (int,float) and math.isfinite(error) and 0<=error<=1e-9,"replay")
        fields=("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls")
        require(all(type(r[k]) is int for k in fields) and tuple(r[k] for k in fields)==(1308,67968,5232,108,10368,432),"record work")
        require(set(r["raw"])==set(map(str,LENGTHS)),"lengths")
        scored={str(n):wide.score_length(data,r["raw"][str(n)],c) for n in LENGTHS};flags={n:v["passed"] for n,v in scored.items()};direct={}
        require(all(type(v) is bool for v in flags.values()),"gate flags")
        for n in LENGTHS:
            normalized=diag.normalize_task(scored[str(n)],"triple",r["seed"],arm)
            for split in ("TRAIN","HOLDOUT"):
                part=diag.partition([p for p in normalized if p["split"]==split]);direct[n,split]=part["direct_pass"]
                parts.append(dict(seed=r["seed"],arm=arm,identifier_length=n,split=split,length_trained=n<5,**part))
        results.append(dict(seed=r["seed"],arm=arm,length_pass=flags,quint_pass=flags["5"],all_lengths_pass=all(flags.values()),
                            fitted_train_direct_pass=all(direct[n,"TRAIN"] for n in (2,3,4)),trained_length_holdout_direct_pass=all(direct[n,"HOLDOUT"] for n in (2,3,4))))
        metrics.append(dict(seed=r["seed"],arm=arm,length_scores=scored))
    for i in range(0,10,2):
        a,b=records[i:i+2]
        require(a["initial_sha256"]==b["initial_sha256"] and a["core_initial_sha256"]==b["core_initial_sha256"]
                and a["fit"]["event_sha256"]==b["fit"]["event_sha256"] and a["fit"]["ce_history"][0]==b["fit"]["ce_history"][0],"matched pairs")
    counts={str(n):{arm:sum(r["length_pass"][str(n)] for r in results if r["arm"]==arm) for arm in ARMS} for n in LENGTHS};contrasts=[]
    for seed,n,split in itertools.product(SEEDS,LENGTHS,("TRAIN","HOLDOUT")):
        a,b=[next(p for p in parts if (p["seed"],p["identifier_length"],p["split"],p["arm"])==(seed,n,split,arm)) for arm in ARMS]
        contrasts.append(dict(seed=seed,identifier_length=n,split=split,rows=a["rows"],full_train_correct=a["correct"],core_frozen_correct=b["correct"]))
    return metrics,dict(seed_results=results,final_partitions=parts,contrasts=contrasts,length_pass_counts=counts,
        gradient_receivers=[dict(seed=r["seed"],arm=r["arm"],trainable=r["fit"]["trainable_parameters"],received_union=sum(r["fit"]["gradient_union"].values())) for r in records],
        candidate_gate=counts["5"][ARMS[1]]==5,all_pairs_matched=True,all_replays=True,**WORK)


def load_parent(paths):
    parent,wide,_,_,transfer,c=context();paths=[Path(p).resolve() for p in paths]
    hashes=(PARENT_SHA,parent.PARENT_SHA,*wide.parent_hashes(wide.context()[0]))
    require(len(paths)==len(hashes)==32 and all(c.audit.sha(p)==h for p,h in zip(paths,hashes,strict=True)),"parent hashes")
    with parent.no_neural():
        p=parent.verify_artifacts(paths[0].parent,paths[1:],PARENT_EXECUTION);parent.validate_result(p)
        require(p["experiment_id"]=="C305-v5b-saved-length-error-overlap" and p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS","parent identity")
        require(p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(WIDE_SOURCE)==WIDE_BLOB,"parent sources")
        s=p["validation_summary"];require(s["diagnostic_complete"] is True and s["capability_gate_applicable"] is False
            and s["parent_flags"]==parent.expected_flags() and s["reconciled_totals"]==720 and s["reconciled_partitions"]==120,"parent scope")
        require(len(p["artifacts"])==3 and {a["file"] for a in p["artifacts"]}==set(parent.OUTPUTS),"parent outputs")
        data=c.audit.read_json(paths[1].parent/"dataset.json");prompts=wide.prompt_dataset(data);wide.validate_prompts(prompts,data,c,transfer)
    return p,data,prompts


def precheck(paths,root):
    validate_seal();p,_,_=load_parent(paths);parent,wide,pairs,diag,transfer,c=context();root=Path(root).resolve()
    pins=dict(p["source_blobs"]);protected=dict(p["input_sha256"])
    require((len(pins),len(protected))==(676,1257) and pins.get(PARENT_SOURCE)==PARENT_BLOB and pins.get(WIDE_SOURCE)==WIDE_BLOB,"inherited protection")
    require(all(pins.get(n)==h for n,h in wide.PINNED.items()),"backend/scorer source pins")
    for module in [parent,wide,pairs,diag,transfer,*wide.context(),*vars(c).values(),c.factory.language_module()]:
        path=getattr(module,"__file__",None) if isinstance(module,ModuleType) else None
        if path and Path(path).resolve().is_relative_to(root):require(Path(path).resolve().relative_to(root).as_posix() in pins,"unprotected helper")
    for n,h in pins.items():require(c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==h,"changed source:"+n)
    for n,h in protected.items():require(Path(n).is_file() and c.audit.sha(n)==h,"changed input:"+n)
    directory=Path(paths[0]).resolve().parent
    for path,h in [(directory/"summary.json",PARENT_SHA)]+[(c.audit.safe_child(directory,a["file"]),a["sha256"]) for a in p["artifacts"]]:
        require(str(path.resolve()) not in protected and c.audit.sha(path)==h,"parent input");protected[str(path.resolve())]=h
    for n in OWN:require(n not in pins,"OWN collision");pins[n]=c.audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    protected.update(c.audit.protect_tree_files(root,pins));require((len(pins),len(protected))==(682,1267),"protection counts")
    print(f"registration_check = source_pins:682; protected_inputs:1267; manifest_sha256:{MANIFEST_SHA}",flush=True)
    return pins,protected


def runtime_preflight(paths,root):
    precheck(paths,root);_,wide,pairs,_,_,c=context();_,data,_=load_parent(paths);tokens,targets=wide.training_tables(data)
    for seed in SEEDS:
        stats=wide.schedule_stats(schedule(seed,data["TRAIN"],pairs));require(stats["per_length_row_exposures"]==[[100]*192 for _ in range(3)],"real exposure")
    models=make_models(SEEDS[0],wide,c);report=first_batch_probe(models,tokens,targets,schedule(SEEDS[0],data["TRAIN"],pairs))
    print("initial_forward_and_backward =",json.dumps(report,sort_keys=True),flush=True)
    print("real_broad_length_core_freeze_preflight = PASS; science not started",flush=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True
            and p["gate_f_candidate"] is False and p["production_adoption"] is False,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(682,1267) and set(OWN)<=set(p["source_blobs"])
            and p["source_blobs"].get(PARENT_SOURCE)==PARENT_BLOB and p["source_blobs"].get(WIDE_SOURCE)==WIDE_BLOB,"result protection")
    require(len(p["artifacts"])==7 and {a["file"] for a in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"];rr=s["seed_results"];require([(r["seed"],r["arm"]) for r in rr]==identities(),"result cohort")
    require(all(set(r["length_pass"])==set(map(str,LENGTHS)) and all(type(v) is bool for v in r["length_pass"].values()) for r in rr),"flags")
    require(all(r["quint_pass"] is r["length_pass"]["5"] and r["all_lengths_pass"] is all(r["length_pass"].values()) for r in rr),"result flags")
    counts={str(n):{a:sum(r["length_pass"][str(n)] for r in rr if r["arm"]==a) for a in ARMS} for n in LENGTHS};gate=counts["5"][ARMS[1]]==5
    require(s["length_pass_counts"]==counts and s["candidate_gate"] is gate and p["status"]==("PASS" if gate else "FAIL"),"fixed primary gate")
    require(s["all_pairs_matched"] is True and s["all_replays"] is True and (len(s["final_partitions"]),len(s["contrasts"]),len(s["gradient_receivers"]))==(80,40,10),"inventory")
    require(all(type(s[k]) is int and s[k]==v for k,v in WORK.items()),"workload")


def load_bundle(path):
    p=torch.load(path,map_location="cpu",weights_only=True)
    require(set(p)=={"schema","slots","identities","states"} and p["schema"]=="fold-c306-broad-core-models-v1" and p["slots"]==64
            and p["identities"]==[list(i) for i in identities()] and len(p["states"])==10,"bundle")
    return p["states"]


def regression_modules(root):
    names=context()[0].regression_modules(root);require(len(names)==len(set(names))==190,"parent modules")
    return names+["tests_lm.test_v05_c306_broad_length_core_freeze"]


def flatten(suite):
    for test in suite:
        if isinstance(test,unittest.TestSuite):yield from flatten(test)
        else:yield test


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids))==4814 and ids.count(EXCLUDED)==1,"loaded suite")
    return unittest.TestSuite(t for t in tests if t.id()!=EXCLUDED)


def guard(root,head,c):
    require(c.audit.git(root,"rev-parse","HEAD").decode().strip()==head and c.audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss"
            and not c.audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repository guard")


def run(*,summaries,output_dir,expected_head):
    _,wide,pairs,diag,_,c=context();root=Path(__file__).resolve().parents[2]
    guard(root,expected_head,c);torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(summaries,root);_,data,prompts=load_parent(summaries);tokens,targets=wide.training_tables(data)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);records=[];states=[]
    for seed in SEEDS:
        models=make_models(seed,wide,c)
        for arm in ARMS:
            r,state=train_one(models[arm],data,prompts,tokens,targets,seed,arm,pairs,wide,c);records.append(r);states.append(state)
    torch.save(dict(schema="fold-c306-broad-core-models-v1",slots=64,identities=[list(i) for i in identities()],states=states),out/OUTPUTS[3]);states=load_bundle(out/OUTPUTS[3])
    for i,seed in enumerate(SEEDS):
        models=make_models(seed,wide,c)
        for j,arm in enumerate(ARMS):wide.replay_one(models[arm],states[2*i+j],records[2*i+j],prompts,data,c)
    metrics,s=analyze(records,data,pairs,wide,diag,c);torch.save(dict(schema="fold-c306-broad-core-eval-v1",records=records),out/OUTPUTS[4])
    for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[1],data),(OUTPUTS[2],prompts),(OUTPUTS[5],metrics),(OUTPUTS[6],s)):(out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=c.audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS]
    guard(root,expected_head,c);precheck(summaries,root)
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if s["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,
           source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=s,gate_f_candidate=False,production_adoption=False)
    validate_result(p);(out/"summary.json").write_bytes(blob(p))
    print("=== C306 COMPACT RESULT RECEIPT ===",flush=True)
    print(json.dumps({**{k:p[k] for k in ("experiment_id","status","commit_sha","artifacts")},"summary_sha256":c.audit.sha(out/"summary.json")},indent=2,sort_keys=True),flush=True)
    return p


def verify_artifacts(outdir,summaries,expected_head):
    parent,wide,pairs,diag,_,c=context();out=Path(outdir);p=c.audit.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"execution HEAD")
    for n,h in p["input_sha256"].items():require(c.audit.sha(n)==h,"protected input")
    for a in p["artifacts"]:
        path=c.audit.safe_child(out,a["file"]);require(c.audit.sha(path)==a["sha256"] and path.stat().st_size==a["serialized_bytes"],"output bytes")
    with parent.no_neural():
        _,data,prompts=load_parent(summaries)
        require(c.audit.read_json(out/OUTPUTS[1])==data and c.audit.read_json(out/OUTPUTS[2])==prompts,"saved data")
        archive=torch.load(out/OUTPUTS[4],map_location="cpu",weights_only=True)
        require(set(archive)=={"schema","records"} and archive["schema"]=="fold-c306-broad-core-eval-v1","evaluation schema")
        metrics,s=analyze(archive["records"],data,pairs,wide,diag,c)
        for n,v in ((OUTPUTS[0],manifest()),(OUTPUTS[5],metrics),(OUTPUTS[6],s)):require(c.audit.read_json(out/n)==v,"persisted:"+n)
    require(p["validation_summary"]==s,"summary reconstruction");return p,metrics


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--summaries",nargs=32,type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,required=True);parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__":main()
