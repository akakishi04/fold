"""C269: paired CE training; query representation is EOS state versus visible query-span pooling."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import torch
from torch import nn
from torch.nn import functional as F

EXPERIMENT_ID = "C269-v5b-paired-query-span-pooling"
STAGE = "V5-B-PAIRED-QUERY-SPAN-POOLING"
BASE = "edba206232f341059ecd8ab4b572896e0ddb7143"
PARENT_EXECUTION = "aa45ea5df68dcba70c99a009c46b7bf8468304a1"
PARENT_SHA = "9e9ea4dd0d20b0ae0b8d315549a1cf1aa13c79853b3dd129c0f01e395a2bf67c"
PARENT_ARTIFACTS = {
    "loss-plan.json": "cf16b504aa03e1e5f61c000c161b44c3a551fe7c103096c9119274947fb4e07b",
    "dataset.json": "1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
    "trained-models.pt": "c4f7bfa9a38bffe871efda54dc9c06d0f82b8acf2b84b42344d6417455daba47",
    "evaluations.pt": "59a17ceb9d228ff4472394b2e9ef11bcf30d5e6d0c448163ac325dc7b10cc6d6",
    "measurements.json": "b95667f0de648574afacab38ef21fa1d24d0ba9945ff504eba04f5c4e4f8a00e",
    "validation-summary.json": "2b20b57ccd87057405dd11600854d538b5ff933907665ee3c787243a4d96e209",
}
SEEDS = tuple(range(269001,269006))
ARMS = ("eos_query","span_query")
SPLITS = ("TRAIN","HOLDOUT")
PROFILES = ("doubled","shared_prefix","shared_suffix")
VIEWS = ("normal","evidence_blind","query_blind")
STEPS, BATCH, TOL = 800, 48, 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c269_query_span_pooling.py",
       "tests_lm/test_v05_c269_query_span_pooling.py","tools/run_c269.ps1","tools/invoke_c269.ps1",
       "docs/experiment-ledger-addendum-c269-preregistration.md","docs/v5b-query-span-pooling-v0.1.md")
OUTPUTS = ("query-plan.json","dataset.json","trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "cec2e2bfe254605c5c4a68c3f71bbaf7135de10a4a39af37a9d4b4aef469e2aa"

def require(ok,message):
    if not ok: raise ValueError(message)
def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
def digest(value): return hashlib.sha256(blob(value)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))
def context():
    from fold_lm.v05_benchmarks import model_c268_paired_query_loss as parent
    p267,core,base,aligned,reader,factory,audit = parent.context()
    return parent,p267,core,base,aligned,reader,factory,audit
def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        seeds=list(SEEDS),arms=list(ARMS),parameters=14256,
        dataset_sha256="1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",
        changed="query representation only: actual C252 pre-core EOS state versus mean pre-core states over visible final-semicolon-to-final-equals query span",
        query_span="positions strictly after final byte59 ';' and before final byte61 '='; no target/entity/split/profile/pair metadata",
        memory="unchanged masked pre-core causal states",residual="unchanged post-core EOS residual",
        loss="mean cross-entropy only in both arms",steps=STEPS,batch=BATCH,lr=.005,
        optimizer="AdamW",betas=[.9,.999],eps=1e-8,weight_decay=0.,clip=1.,
        schedule="96 TRAIN query pairs; randperm96 seed+269000+epoch;24 pairs/batch;profile=epoch%3",
        epochs=200,row_exposures=200,profile_updates=[268,268,264],fit_rng="seed+270000 reset per arm",
        primary="all five span_query states pass C267 criteria on both splits/all profiles; eos_query control separate",
        gate=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        models=10,train_steps=8000,training_rows=384000,model_forward_calls=8540,
        row_presentations=435840,core_forward_calls=34160,evaluation_forwards=540,
        checkpoint_bundle_loads=1,model_state_loads=10,new_checkpoint_writes=1,
        source_pins=460,protected_inputs=787,direct_dependencies=45,own_tests=24,
        modules=154,loaded_tests=3622,focused_tests=3621,excluded_test=EXCLUDED,
        dtype="CPU float64",threads=2,deterministic=True,replay_tolerance=TOL,network_calls=0,
        gate_f_candidate=False,production_adoption=False,unseen_name_transfer_claim=False,causal_parser_claim=False)
def query_pairs(rows):
    require(len(rows)==192 and len({r["id"] for r in rows})==192,"TRAIN row identity")
    groups=defaultdict(list)
    for i,r in enumerate(rows):
        groups[(r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"]))].append(i)
    pairs=[]
    for key in sorted(groups):
        ids=sorted(groups[key],key=lambda i:rows[i]["query"])
        require(len(ids)==2 and [rows[i]["query"] for i in ids]==list(key[1]),"both queries required")
        require(rows[ids[0]]["target"]!=rows[ids[1]]["target"],"distinct targets");pairs.append(ids)
    require(len(pairs)==96 and sorted(sum(pairs,[]))==list(range(192)),"complete pair partition")
    return torch.tensor(pairs,dtype=torch.int64)
def schedule(seed,rows,steps=STEPS):
    require(seed in SEEDS and type(steps) is int and 0<steps<=STEPS,"schedule identity")
    pairs=query_pairs(rows);batches=[];profiles=[]
    for epoch in range((steps+3)//4):
        g=torch.Generator(device="cpu").manual_seed(seed+269000+epoch);order=torch.randperm(96,generator=g)
        for block in range(4):
            if len(batches)==steps: break
            batches.append(pairs[order[block*24:(block+1)*24]].flatten());profiles.append(epoch%3)
    indices=torch.stack(batches)
    return indices,profiles,dict(batch_sha256=digest(indices.tolist()),
        row_exposures=torch.bincount(indices.flatten(),minlength=192).tolist(),
        profile_updates=[profiles.count(i) for i in range(3)])
def query_span_mask(tokens):
    require(tokens.dtype==torch.int64 and tokens.ndim==2 and tokens.shape[1]==48,"query span tokens")
    valid=tokens!=256;eos=valid.sum(1)-1;rows=torch.arange(len(tokens),device=tokens.device)
    require(bool((eos>=4).all()) and bool((tokens[rows,eos]==258).all()),"query span EOS")
    eq=eos-1;require(bool((tokens[rows,eq]==61).all()),"final equals")
    pos=torch.arange(tokens.shape[1],device=tokens.device).expand(len(tokens),-1)
    semi=(tokens==59)&valid&(pos<eq.unsqueeze(1))
    last=torch.where(semi,pos,torch.full_like(pos,-1)).max(1).values
    require(bool((last>=1).all()),"final semicolon")
    mask=(pos>last.unsqueeze(1))&(pos<eq.unsqueeze(1))&valid
    require(bool(mask.any(1).all()),"nonempty query span")
    require(not bool((((tokens==59)|(tokens==61))&mask).any()),"delimiter inside query span")
    return mask
class SpanQueryReadout(nn.Module):
    """Actual C252 parameterization; only query source changes to visible query-span mean."""
    def __init__(self,backbone,seed,reader):
        super().__init__();self.backbone=backbone;self.family="full";self.read=reader.ResidualHead("token_read",seed)
        require(sum(p.numel() for p in backbone.parameters())==13488,"Full backbone size")
        require(backbone.config.width==16 and backbone.config.max_tokens==48,"backbone shape")
    def forward(self,tokens,tasks):
        require(tokens.dtype==tasks.dtype==torch.int64 and tokens.ndim==2 and tokens.shape[1]==48
            and tasks.shape==(len(tokens),) and bool((tasks==0).all()),"NEXT token/task contract")
        valid=tokens!=256;eos=valid.sum(1)-1
        require(bool((eos>=1).all()) and bool((tokens[torch.arange(len(tokens)),eos]==258).all()),"EOS")
        span=query_span_mask(tokens);local=[];next_states=[];routes=Counter();norm_calls=[0];handles=[]
        def capture_local(module,args,output):
            require(output[0].shape==(len(tokens),48,16),"encoder shape")
            local.append(output[0]*valid.unsqueeze(-1).to(dtype=output[0].dtype))
        def capture_core(module,args,kwargs,output):
            route=kwargs.get("route_index")
            require(len(local)==1 and len(args)==2 and torch.equal(args[1],local[0]),"actual pre-core context")
            routes[route]+=1
            if route==self.backbone.config.next_route:next_states.append(output)
        def inject(module,args):
            norm_calls[0]+=1;cfg=self.backbone.config
            require(routes=={cfg.next_route:cfg.internal_steps,cfg.instruction_route:cfg.internal_steps},"core path counts")
            post=args[0]
            require(len(next_states)==cfg.internal_steps and torch.equal(next_states[-1][torch.arange(len(tokens)),eos],post),"post-core residual provenance")
            pre=(local[0]*span.unsqueeze(-1)).sum(1)/span.sum(1,keepdim=True).to(dtype=local[0].dtype)
            q=self.read.query(pre);scores=(self.read.key(local[0])*q.unsqueeze(1)).sum(-1)/4.0
            alpha=scores.masked_fill(~valid,float("-inf")).softmax(-1)
            return (post+self.read.output((alpha.unsqueeze(-1)*local[0]).sum(1)),)
        try:
            handles.append(self.backbone.local_encoder.register_forward_hook(capture_local))
            handles.append(self.backbone.core.register_forward_hook(capture_core,with_kwargs=True))
            handles.append(self.backbone.readout_norm.register_forward_pre_hook(inject));logits=self.backbone(tokens,tasks)
        finally:
            for handle in handles:handle.remove()
        require(norm_calls[0]==1 and logits.shape==(len(tokens),256) and bool(torch.isfinite(logits).all()),"output")
        return logits
def make_arm_model(seed,arm,base,aligned,reader,factory):
    require(seed in SEEDS and arm in ARMS,"model identity")
    control=base.make_model(factory.new_model(seed),"aligned_precore_read",seed,aligned,reader)
    require(sum(p.numel() for p in control.parameters())==14256,"control capacity")
    if arm=="eos_query":return control
    candidate=SpanQueryReadout(copy.deepcopy(control.backbone),seed,reader)
    candidate.load_state_dict(copy.deepcopy(control.state_dict()),strict=True)
    require(list(candidate.state_dict())==list(control.state_dict()),"state keys")
    require(base.fingerprint(candidate)==base.fingerprint(control),"matched complete initial state")
    require(all(a.data_ptr()!=b.data_ptr() for a,b in zip(candidate.parameters(),control.parameters(),strict=True)),"no shared parameters")
    return candidate
def fit(model,data,tokens,targets,seed,arm):
    require(tokens.shape==(3,192,48) and targets.shape==(192,) and arm in ARMS,"training tables/arm")
    ids,profiles,plan=schedule(seed,data["TRAIN"],STEPS);torch.manual_seed(seed+270000)
    opt=torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.);model.train()
    for step in range(STEPS):
        opt.zero_grad(set_to_none=True)
        logits=model(tokens[profiles[step],ids[step]],torch.zeros(48,dtype=torch.int64))
        loss=F.cross_entropy(logits,targets[ids[step]]);require(bool(torch.isfinite(loss)),"nonfinite loss")
        loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True);opt.step()
        if (step+1)%200==0:print(f"[C269] seed={seed} arm={arm} step={step+1}/800 ce={float(loss.detach()):.6f}",flush=True)
    model.eval();return dict(steps=STEPS,training_rows=STEPS*48,last_ce=float(loss.detach()),**plan)
def train_one(model,seed,arm,data,tokens,targets,p267,core,base,factory):
    require(sum(p.numel() for p in model.parameters())==14256,"capacity")
    initial=base.fingerprint(model);back=base.fingerprint(model.backbone);head=base.fingerprint(model.read)
    with p267.counted(model,core) as (counts,cores):
        fitted=fit(model,data,tokens,targets,seed,arm);final=base.fingerprint(model);raw=p267.evaluate(model,data,factory)
    require(counts==[827,40992] and cores[0]==3308,"training/final workload")
    require(base.fingerprint(model)==final and final!=initial and base.fingerprint(model.backbone)!=back and base.fingerprint(model.read)!=head,"weight change/evaluation integrity")
    return dict(seed=seed,arm=arm,parameters=14256,initial_sha256=initial,final_sha256=final,fit=fitted,raw=raw,
        weights_changed=True,forward_calls=827,row_presentations=40992,core_forward_calls=3308),{k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
def analyze(records,data,p267):
    p267.validate_data(data);require([(r["seed"],r["arm"]) for r in records]==identities(),"complete identities")
    metrics=[];results=[];contrasts=[]
    for r in records:
        require(r["parameters"]==14256 and r["weights_changed"] is True and r["checkpoint_roundtrip"] is True,"record integrity")
        require(tuple(r[k] for k in ("forward_calls","row_presentations","core_forward_calls","replay_forward_calls","replay_row_presentations","replay_core_forward_calls"))==(827,40992,3308,27,2592,108),"record workload")
        require(type(r["reload_max_error"]) in (int,float) and math.isfinite(r["reload_max_error"]) and 0<=r["reload_max_error"]<=TOL,"replay error")
        expected=schedule(r["seed"],data["TRAIN"])[2]
        require(r["fit"]["steps"]==800 and r["fit"]["training_rows"]==38400 and all(r["fit"][k]==v for k,v in expected.items()),"actual schedule")
        require(type(r["fit"]["last_ce"]) in (int,float) and math.isfinite(r["fit"]["last_ce"]) and r["fit"]["last_ce"]>=0,"loss record")
        scored=p267.score(data,r["raw"]);metrics.append(dict(seed=r["seed"],arm=r["arm"],**scored));results.append(dict(seed=r["seed"],arm=r["arm"],passed=scored["passed"]))
    for i in range(0,10,2):
        a,b=records[i:i+2];require(a["initial_sha256"]==b["initial_sha256"] and a["fit"]["batch_sha256"]==b["fit"]["batch_sha256"],"paired state/batches")
        for x,y in zip(metrics[i]["totals"],metrics[i+1]["totals"],strict=True):
            require(tuple(x[k] for k in ("split","profile","language","rows","pairs"))==tuple(y[k] for k in ("split","profile","language","rows","pairs")),"contrast identities")
            if x["split"]=="HOLDOUT":contrasts.append(dict(seed=a["seed"],profile=x["profile"],language=x["language"],rows=x["rows"],pairs=x["pairs"],
                control_correct=x["correct"],candidate_correct=y["correct"],correct_delta=y["correct"]-x["correct"],
                control_collapsed=x["collapsed_pairs"],candidate_collapsed=y["collapsed_pairs"],collapse_delta=y["collapsed_pairs"]-x["collapsed_pairs"]))
    summary=dict(models=10,seed_results=results,seed_pass_counts={a:sum(r["passed"] for r in results if r["arm"]==a) for a in ARMS},
        candidate_gate=all(r["passed"] for r in results if r["arm"]==ARMS[1]),contrasts=contrasts,train_steps=8000,training_rows=384000,
        model_forward_calls=8540,row_presentations=435840,core_forward_calls=34160,checkpoint_bundle_loads=1,model_state_loads=10,new_checkpoint_writes=1,
        all_replays=True,all_pairs_matched=True)
    return metrics,summary
def load_parent(path):
    parent,*_,audit=context();path=Path(path).resolve();require(audit.sha(path)==PARENT_SHA,"accepted parent hash")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("parent verification forbids model calls")):
        payload,metrics=parent.verify_artifacts(path.parent,PARENT_EXECUTION)
    parent.validate_result(payload)
    require(payload["status"]=="FAIL" and payload["commit_sha"]==PARENT_EXECUTION and payload["validation_summary"]["seed_pass_counts"]=={"ce_only":3,"ce_pair_margin":3} and payload["validation_summary"]["candidate_gate"] is False,"C268 valid negative")
    require({x["file"]:x["sha256"] for x in payload["artifacts"]}==PARENT_ARTIFACTS and len(metrics)==10,"accepted artifacts");return payload
def precheck(path,root):
    _,_,_,_,_,_,factory,audit=context();root=Path(root);path=Path(path).resolve();payload=load_parent(path)
    pins,protected=dict(payload["source_blobs"]),dict(payload["input_sha256"])
    for name,wanted in protected.items():require(Path(name).is_file() and audit.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items():require(audit.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    for child,wanted in [(path,PARENT_SHA)]+[(audit.safe_child(path.parent,x["file"]),x["sha256"]) for x in payload["artifacts"]]:
        key=str(child.resolve());require(key not in protected,"duplicate parent input");protected[key]=wanted
    for name in OWN:require(name not in pins,"OWN collision");pins[name]=audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-8])_[^/]+)\.py"
    deps=set(factory.LM_SOURCES)|{n for n in payload["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps)==45 and deps<=set(pins),"direct dependencies");protected.update(audit.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(460,787) and digest(manifest())==MANIFEST_SHA,"registration counts/hash")
    print("registration_check = source_pins:460; protected_inputs:787; manifest_sha256:"+MANIFEST_SHA,flush=True);return pins,protected
def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(460,787) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==6 and {x["file"] for x in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"];rr=s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rr]==identities() and all(type(r["passed"]) is bool for r in rr),"result identities")
    require(s["candidate_gate"] is all(r["passed"] for r in rr if r["arm"]==ARMS[1]) and s["seed_pass_counts"]=={a:sum(r["passed"] for r in rr if r["arm"]==a) for a in ARMS},"gate accounting")
    for k in ("models","train_steps","training_rows","model_forward_calls","row_presentations","core_forward_calls","checkpoint_bundle_loads","model_state_loads","new_checkpoint_writes"):
        require(type(s[k]) is int and s[k]==manifest()[k],"workload:"+k)
    require(len(s["contrasts"])==30 and s["all_replays"] is True and s["all_pairs_matched"] is True and p["status"]==("PASS" if s["candidate_gate"] else "FAIL"),"status")
    require(all(p[k] is False for k in ("gate_f_candidate","production_adoption","unseen_name_transfer_claim","causal_parser_claim")),"scope")
def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True);require(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c269-query-span-models-v1","bundle schema")
    require(v["identities"]==[list(x) for x in identities()] and len(v["states"])==10,"bundle identities");return v["states"]
def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item
def regression_modules(root):
    names=context()[0].regression_modules(root);require(len(names)==len(set(names))==153,"parent modules")
    return names+["tests_lm.test_v05_c269_query_span_pooling"]
def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"suite identities");kept=[t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(3622,3621),"suite counts");return unittest.TestSuite(kept)
def run(*,c268_summary,output_dir,expected_head):
    parent,p267,core,base,aligned,reader,factory,audit=context();root=Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True);pins,protected=precheck(c268_summary,root)
    data=p267.dataset();p267.validate_data(data);tokens,targets=p267.training_tables(data,factory)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);records=[];states=[]
    for seed in SEEDS:
        templates={arm:make_arm_model(seed,arm,base,aligned,reader,factory) for arm in ARMS};initial=base.fingerprint(templates[ARMS[0]])
        require(base.fingerprint(templates[ARMS[1]])==initial,"paired initial templates")
        for arm in ARMS:
            print(f"[C269] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            r,state=train_one(templates[arm],seed,arm,data,tokens,targets,p267,core,base,factory);require(r["initial_sha256"]==initial,"paired initial fingerprint")
            records.append(r);states.append(state)
    torch.save(dict(schema="fold-c269-query-span-models-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for r,state in zip(records,load_bundle(out/"trained-models.pt"),strict=True):
        p267.replay_one(make_arm_model(r["seed"],r["arm"],base,aligned,reader,factory),state,r,data,core,base,factory)
    metrics,summary=analyze(records,data,p267);torch.save(dict(schema="fold-c269-query-span-eval-v1",records=records),out/"evaluations.pt")
    for name,value in (("query-plan.json",manifest()),("dataset.json",data),("measurements.json",metrics),("validation-summary.json",summary)):(out/name).write_bytes(blob(value))
    artifacts=[dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS];guard();precheck(c268_summary,root)
    for name,wanted in protected.items():require(audit.sha(name)==wanted,"modified input")
    payload=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,production_adoption=False,unseen_name_transfer_claim=False,causal_parser_claim=False)
    validate_result(payload);(out/"summary.json").write_bytes(blob(payload));print("=== C269 RESULT ===",flush=True);print(blob(payload).decode(),flush=True);return payload
def verify_artifacts(output_dir,expected_head):
    _,p267,*rest=context();audit=rest[-1];out=Path(output_dir);p=audit.read_json(out/"summary.json");validate_result(p);require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():require(audit.sha(name)==wanted,"postcheck input")
    for x in p["artifacts"]:
        child=audit.safe_child(out,x["file"]);require(audit.sha(child)==x["sha256"] and child.stat().st_size==x["serialized_bytes"],"output bytes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("saved postcheck forbids model calls")):
        data=audit.read_json(out/"dataset.json");v=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
        require(set(v)=={"schema","records"} and v["schema"]=="fold-c269-query-span-eval-v1","eval schema");metrics,summary=analyze(v["records"],data,p267)
        for name,value in (("query-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):require(audit.read_json(out/name)==value,"persisted reconstruction:"+name)
    require(p["validation_summary"]==summary,"saved summary");return p,metrics
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("c268-summary","output-dir"):p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))
if __name__=="__main__":main()
