"""C271: mean query-span versus final query-byte endpoint."""
from __future__ import annotations
import argparse,copy,hashlib,itertools,json,math,re,unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch
import torch
from torch import nn
from torch.nn import functional as F

EXPERIMENT_ID="C271-v5b-paired-query-endpoint";STAGE="V5-B-PAIRED-QUERY-ENDPOINT"
BASE="7d050e672758f97033fa23860af47d7a5d9cf15b"
PARENT_EXECUTION="456deac490990f4c7f4ceb1cdf241f0c606a77de"
PARENT_SHA="117c55f5498dec1b5e60c2a59fc571eeb485a3f6614f710348e29348e3433d5b"
C269_SHA="a97663b83c536d2ce8df4fb41d42493cbbfc35fe757b9b72fca1b63382f255b8"
PARENT_ARTIFACTS={"transfer-plan.json":"3fa2e3267b08c6ea528bfdb52bc7ad0e932e3215945e5231bdf38a48e453f016","triple-dataset.json":"432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73","eval-outputs.pt":"5e9c2b5c428e0dba4c3de5ecebd5f4e3281092bcb87a52489fdce30664201f43","measurements.json":"c0d66450ef2b451103db615f78be900156347f2689a0f01c6e2211062c10ce12","validation-summary.json":"20e26a038db3c4f1f54552f72a197bce587e9ba44500a0b03e918cc6d3c7bc93"}
SEEDS=tuple(range(271001,271006));ARMS=("mean_span","endpoint_span");STEPS=800;TOL=1e-9
OWN=("fold_lm/v05_benchmarks/model_c271_query_endpoint.py","tests_lm/test_v05_c271_query_endpoint.py","tools/run_c271.ps1","tools/invoke_c271.ps1","docs/experiment-ledger-addendum-c271-preregistration.md","docs/v5b-query-endpoint-v0.1.md")
OUTPUTS=("architecture-plan.json","dataset.json","triple-dataset.json","trained-models.pt","evaluations.pt","measurements.json","validation-summary.json")
EXCLUDED="tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA="15eeef060442ae4b17ce7d536a7a158b807170b693d3fc9f10fbea1710a9ac59"

def req(x,m):
    if not x: raise ValueError(m)
def blob(v): return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()
def digest(v): return hashlib.sha256(blob(v)).hexdigest()
def identities(): return list(itertools.product(SEEDS,ARMS))
def context():
    from fold_lm.v05_benchmarks import model_c270_frozen_triple_identifiers as c270
    c269,p267,core,base,aligned,reader,factory,audit=c270.context()
    return c270,c269,p267,core,base,aligned,reader,factory,audit
def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,c269_source_sha256=C269_SHA,parent_artifacts=PARENT_ARTIFACTS,seeds=list(SEEDS),arms=list(ARMS),parameters=14256,train_dataset_sha256="1e03cf4d6a72700de0d3973459737ffba7dbc843655ebb7439cdedb99805c2f1",triple_dataset_sha256="432846dfd78f5f03c7268753460b9ab71957906c7b400e700e8d4e1f0816af73",changed="reader query source only: mean of visible query-span pre-core states versus final visible query-byte pre-core state",endpoint="last byte position strictly before final '=' within C269 query_span_mask; causal local state",memory="unchanged masked pre-core causal states",residual="unchanged post-core EOS residual",loss="mean cross-entropy only in both arms",steps=800,batch=48,lr=.005,optimizer="AdamW",betas=[.9,.999],eps=1e-8,weight_decay=0.,clip=1.,schedule="96 TRAIN pairs; randperm seed+271000+epoch;24 pairs/batch;profile=epoch%3",epochs=200,row_exposures=200,profile_updates=[268,268,264],fit_rng="seed+272000 reset per arm",primary="all five endpoint_span states pass both original two-character and unseen three-character fixed gates; mean_span control separate",gate=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),models=10,train_steps=8000,training_rows=384000,model_forward_calls=9080,row_presentations=487680,core_forward_calls=36320,evaluation_forwards=1080,checkpoint_bundle_loads=1,model_state_loads=10,new_checkpoint_writes=1,raw_logit_payload_bytes=106168320,source_pins=472,protected_inputs=812,direct_dependencies=47,own_tests=24,modules=156,loaded_tests=3670,focused_tests=3669,excluded_test=EXCLUDED,dtype="CPU float64",threads=2,deterministic=True,replay_tolerance=TOL,network_calls=0,gate_f_candidate=False,production_adoption=False,unseen_name_transfer_claim=False,arbitrary_name_claim=False,causal_parser_claim=False)

class EndpointQueryReadout(nn.Module):
    def __init__(self,backbone,seed,reader,span_mask):
        super().__init__();self.backbone=backbone;self.family="full";self.read=reader.ResidualHead("token_read",seed);self._span_mask=span_mask
        req(sum(p.numel() for p in backbone.parameters())==13488 and backbone.config.width==16 and backbone.config.max_tokens==48,"backbone")
    def forward(self,tokens,tasks):
        req(tokens.dtype==tasks.dtype==torch.int64 and tokens.shape[1]==48 and tasks.shape==(len(tokens),) and bool((tasks==0).all()),"contract")
        valid=tokens!=256;eos=valid.sum(1)-1;rows=torch.arange(len(tokens),device=tokens.device)
        req(bool((tokens[rows,eos]==258).all()),"EOS")
        span=self._span_mask(tokens);pos=torch.arange(48,device=tokens.device).expand(len(tokens),-1)
        end=torch.where(span,pos,torch.full_like(pos,-1)).max(1).values;req(bool(span[rows,end].all()),"endpoint")
        local=[];nxt=[];routes=Counter();norm=[0];handles=[]
        def lh(m,a,o): local.append(o[0]*valid.unsqueeze(-1).to(o[0].dtype))
        def ch(m,a,k,o):
            route=k.get("route_index");req(len(local)==1 and torch.equal(a[1],local[0]),"pre-core context");routes[route]+=1
            if route==self.backbone.config.next_route:nxt.append(o)
        def nh(m,a):
            norm[0]+=1;cfg=self.backbone.config;post=a[0]
            req(routes=={cfg.next_route:cfg.internal_steps,cfg.instruction_route:cfg.internal_steps},"core routes")
            req(torch.equal(nxt[-1][rows,eos],post),"residual provenance")
            q=self.read.query(local[0][rows,end]);score=(self.read.key(local[0])*q[:,None,:]).sum(-1)/4
            alpha=score.masked_fill(~valid,float("-inf")).softmax(-1)
            return (post+self.read.output((alpha[:,:,None]*local[0]).sum(1)),)
        try:
            handles=[self.backbone.local_encoder.register_forward_hook(lh),self.backbone.core.register_forward_hook(ch,with_kwargs=True),self.backbone.readout_norm.register_forward_pre_hook(nh)]
            out=self.backbone(tokens,tasks)
        finally:
            for h in handles:h.remove()
        req(norm[0]==1 and out.shape==(len(tokens),256) and bool(torch.isfinite(out).all()),"output")
        return out

def make_arm(seed,arm,c269,base,reader,factory):
    req(seed in SEEDS and arm in ARMS,"identity")
    mean=c269.SpanQueryReadout(factory.new_model(seed),seed,reader);req(sum(p.numel() for p in mean.parameters())==14256,"capacity")
    if arm=="mean_span": return mean
    end=EndpointQueryReadout(copy.deepcopy(mean.backbone),seed,reader,c269.query_span_mask)
    end.load_state_dict(copy.deepcopy(mean.state_dict()),strict=True)
    req(base.fingerprint(end)==base.fingerprint(mean) and list(end.state_dict())==list(mean.state_dict()) and sum(p.numel() for p in end.parameters())==14256,"matched state")
    req(all(a.data_ptr()!=b.data_ptr() for a,b in zip(end.parameters(),mean.parameters(),strict=True)),"storage")
    return end

def schedule(seed,rows):
    req(seed in SEEDS and len(rows)==192,"schedule")
    groups={}
    for i,r in enumerate(rows):groups.setdefault((r["language"],tuple(r["entities"]),tuple(r["values"]),tuple(r["permutation"])),[]).append(i)
    pairs=[]
    for k in sorted(groups):
        ids=sorted(groups[k],key=lambda i:rows[i]["query"]);req(len(ids)==2 and rows[ids[0]]["target"]!=rows[ids[1]]["target"],"pair");pairs.append(ids)
    pairs=torch.tensor(pairs);req(tuple(pairs.shape)==(96,2),"pair count")
    batches=[];profiles=[]
    for e in range(200):
        order=torch.randperm(96,generator=torch.Generator().manual_seed(seed+271000+e))
        for block in range(4):batches.append(pairs[order[block*24:(block+1)*24]].flatten());profiles.append(e%3)
    x=torch.stack(batches)
    return x,profiles,dict(batch_sha256=digest(x.tolist()),row_exposures=torch.bincount(x.flatten(),minlength=192).tolist(),profile_updates=[profiles.count(i) for i in range(3)])

def fit(model,data,tokens,targets,seed,arm):
    req(tokens.shape==(3,192,48) and targets.shape==(192,) and arm in ARMS,"fit tables")
    ids,profiles,plan=schedule(seed,data["TRAIN"]);torch.manual_seed(seed+272000)
    opt=torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.);model.train()
    for step in range(800):
        opt.zero_grad(set_to_none=True);logits=model(tokens[profiles[step],ids[step]],torch.zeros(48,dtype=torch.int64));loss=F.cross_entropy(logits,targets[ids[step]])
        req(bool(torch.isfinite(loss)),"loss");loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True);opt.step()
        if (step+1)%200==0:print(f"[C271] seed={seed} arm={arm} step={step+1}/800 ce={float(loss.detach()):.6f}",flush=True)
    model.eval();return dict(steps=800,training_rows=38400,last_ce=float(loss.detach()),**plan)

def train_one(model,seed,arm,data,prompts,tokens,targets,p267,c270,core,base,factory):
    initial=base.fingerprint(model);back=base.fingerprint(model.backbone);head=base.fingerprint(model.read)
    with p267.counted(model,core) as (counts,cores):
        plan=fit(model,data,tokens,targets,seed,arm);final=base.fingerprint(model);two=p267.evaluate(model,data,factory);triple=c270.evaluate_new(model,prompts,data,factory,p267)
    req(counts==[854,43584] and cores[0]==3416,"workload");req(final!=initial and base.fingerprint(model.backbone)!=back and base.fingerprint(model.read)!=head,"weights")
    return dict(seed=seed,arm=arm,parameters=14256,initial_sha256=initial,final_sha256=final,fit=plan,raw_two=two,raw_triple=triple,weights_changed=True,forward_calls=854,row_presentations=43584,core_forward_calls=3416),{k:v.detach().cpu().clone() for k,v in model.state_dict().items()}

def replay_triple(a,b,data,p267):
    err=0.
    for split,profile,view in itertools.product(("TRAIN","HOLDOUT"),("tripled","shared_prefix2","shared_suffix2"),("normal","evidence_blind","query_blind")):
        x,y=a[split][profile][view],b[split][profile][view];p267.check_logits(x,len(data[split]));p267.check_logits(y,len(data[split]));err=max(err,float((x-y).abs().max()));req(err<=TOL and torch.equal(x.argmax(-1),y.argmax(-1)),"triple replay")
    return err

def replay_one(model,state,r,data,prompts,p267,c270,core,base,factory):
    model.load_state_dict(state,strict=True);model.eval();req(base.fingerprint(model)==r["final_sha256"],"fingerprint")
    with p267.counted(model,core) as (counts,cores):two=p267.evaluate(model,data,factory);triple=c270.evaluate_new(model,prompts,data,factory,p267)
    err=max(c270.replay_old(two,r["raw_two"],data,p267),replay_triple(triple,r["raw_triple"],data,p267))
    req(counts==[54,5184] and cores[0]==216 and base.fingerprint(model)==r["final_sha256"],"replay")
    r.update(checkpoint_roundtrip=True,reload_max_error=err,replay_forward_calls=54,replay_row_presentations=5184,replay_core_forward_calls=216)

def analyze(records,data,prompts,p267,c270):
    req([(r["seed"],r["arm"]) for r in records]==identities(),"records");metrics=[];results=[];contrasts=[]
    for r in records:
        req(r["parameters"]==14256 and r["checkpoint_roundtrip"] is True and r["weights_changed"] is True and type(r["reload_max_error"]) in (int,float) and math.isfinite(r["reload_max_error"]) and 0<=r["reload_max_error"]<=TOL,"integrity")
        req((r["forward_calls"],r["row_presentations"],r["core_forward_calls"],r["replay_forward_calls"],r["replay_row_presentations"],r["replay_core_forward_calls"])==(854,43584,3416,54,5184,216),"counts")
        exp=schedule(r["seed"],data["TRAIN"])[2];req(r["fit"]["steps"]==800 and r["fit"]["training_rows"]==38400 and all(r["fit"][k]==v for k,v in exp.items()) and math.isfinite(r["fit"]["last_ce"]),"schedule")
        two=p267.score(data,r["raw_two"]);tri=c270.score(data,r["raw_triple"],p267);passed=two["passed"] and tri["passed"]
        metrics.append(dict(seed=r["seed"],arm=r["arm"],two_char=two,triple=tri,passed=passed));results.append(dict(seed=r["seed"],arm=r["arm"],two_char_pass=two["passed"],triple_pass=tri["passed"],passed=passed))
    for i in range(0,10,2):
        ra,rb=records[i:i+2];req(ra["initial_sha256"]==rb["initial_sha256"] and ra["fit"]["batch_sha256"]==rb["fit"]["batch_sha256"],"paired state/batches")
        a,b=metrics[i:i+2];req(a["seed"]==b["seed"] and a["arm"]=="mean_span" and b["arm"]=="endpoint_span","pair")
        for task,key,all_splits in (("two_char","two_char",False),("triple","triple",True)):
            for x,y in zip(a[key]["totals"],b[key]["totals"],strict=True):
                if all_splits or x["split"]=="HOLDOUT":
                    contrasts.append(dict(task=task,seed=a["seed"],split=x["split"],profile=x["profile"],language=x["language"],rows=x["rows"],pairs=x["pairs"],control_correct=x["correct"],candidate_correct=y["correct"],correct_delta=y["correct"]-x["correct"],control_collapsed=x["collapsed_pairs"],candidate_collapsed=y["collapsed_pairs"],collapse_delta=y["collapsed_pairs"]-x["collapsed_pairs"]))
    summary=dict(models=10,seed_results=results,seed_pass_counts={a:sum(r["passed"] for r in results if r["arm"]==a) for a in ARMS},two_char_pass_counts={a:sum(r["two_char_pass"] for r in results if r["arm"]==a) for a in ARMS},triple_pass_counts={a:sum(r["triple_pass"] for r in results if r["arm"]==a) for a in ARMS},candidate_gate=all(r["passed"] for r in results if r["arm"]=="endpoint_span"),contrasts=contrasts,train_steps=8000,training_rows=384000,model_forward_calls=9080,row_presentations=487680,core_forward_calls=36320,checkpoint_bundle_loads=1,model_state_loads=10,new_checkpoint_writes=1,all_replays=True,all_pairs_matched=True)
    return metrics,summary

def load_parent(c270_summary,c269_summary):
    c270,*rest=context();audit=rest[-1];p=Path(c270_summary).resolve();s=Path(c269_summary).resolve();req(audit.sha(p)==PARENT_SHA and audit.sha(s)==C269_SHA,"parent hash")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("parent verification forbids model calls")):payload,metrics=c270.verify_artifacts(p.parent,s,PARENT_EXECUTION)
    c270.validate_result(payload);req(payload["status"]=="FAIL" and payload["validation_summary"]["seed_pass_counts"]=={"eos_query":0,"span_query":0},"C270 verdict");req({x["file"]:x["sha256"] for x in payload["artifacts"]}==PARENT_ARTIFACTS and len(metrics)==10,"parent artifacts");return payload

def precheck(c270_summary,c269_summary,root):
    c270,*rest=context();factory,audit=rest[-2],rest[-1];root=Path(root);p=Path(c270_summary).resolve();s=Path(c269_summary).resolve();payload=load_parent(p,s);pins,protected=dict(payload["source_blobs"]),dict(payload["input_sha256"]);req(protected.get(str(s))==C269_SHA,"C269 protected")
    for n,w in protected.items():req(Path(n).is_file() and audit.sha(n)==w,"changed input:"+n)
    for n,w in pins.items():req(audit.git(root,"rev-parse","HEAD:"+n).decode().strip()==w,"changed source:"+n)
    for child,w in [(p,PARENT_SHA)]+[(audit.safe_child(p.parent,x["file"]),x["sha256"]) for x in payload["artifacts"]]:
        key=str(child.resolve());req(key not in protected and audit.sha(child)==w,"parent input identity");protected[key]=w
    for x in payload["artifacts"]:req(audit.safe_child(p.parent,x["file"]).stat().st_size==x["serialized_bytes"],"parent artifact size")
    for n in OWN:pins[n]=audit.git(root,"rev-parse","HEAD:"+n).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-9]|270)_[^/]+)\.py"
    deps=set(factory.LM_SOURCES)|{n for n in payload["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]};req(len(deps)==47 and deps<=set(pins),"deps")
    protected.update(audit.protect_tree_files(root,pins));req((len(pins),len(protected))==(472,812) and digest(manifest())==MANIFEST_SHA,"registration")
    print("registration_check = source_pins:472; protected_inputs:812; manifest_sha256:"+MANIFEST_SHA,flush=True);return pins,protected

def validate_result(p):
    req(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"identity")
    req((len(p["source_blobs"]),len(p["input_sha256"]))==(472,812) and set(OWN)<=set(p["source_blobs"]),"protection")
    req(len(p["artifacts"])==7 and {x["file"] for x in p["artifacts"]}==set(OUTPUTS),"artifacts")
    s=p["validation_summary"];rr=s["seed_results"];req([(r["seed"],r["arm"]) for r in rr]==identities() and all(type(r["passed"]) is bool for r in rr),"results")
    req(s["candidate_gate"] is all(r["passed"] for r in rr if r["arm"]=="endpoint_span"),"gate")
    req(s["seed_pass_counts"]=={a:sum(r["passed"] for r in rr if r["arm"]==a) for a in ARMS},"seed counts")
    req(s["two_char_pass_counts"]=={a:sum(r["two_char_pass"] for r in rr if r["arm"]==a) for a in ARMS} and s["triple_pass_counts"]=={a:sum(r["triple_pass"] for r in rr if r["arm"]==a) for a in ARMS},"subgate counts")
    for k in ("models","train_steps","training_rows","model_forward_calls","row_presentations","core_forward_calls","checkpoint_bundle_loads","model_state_loads","new_checkpoint_writes"):req(type(s[k]) is int and s[k]==manifest()[k],"workload:"+k)
    req(len(s["contrasts"])==90 and s["all_replays"] is True and s["all_pairs_matched"] is True and p["status"]==("PASS" if s["candidate_gate"] else "FAIL"),"status")
    req(all(p[k] is False for k in ("gate_f_candidate","production_adoption","unseen_name_transfer_claim","arbitrary_name_claim","causal_parser_claim")),"scope")

def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True);req(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c271-query-endpoint-models-v1" and v["identities"]==[list(x) for x in identities()] and len(v["states"])==10,"bundle");return v["states"]
def flatten(s):
    for x in s:
        if isinstance(x,unittest.TestSuite):yield from flatten(x)
        else:yield x
def regression_modules(root):
    names=context()[0].regression_modules(root);req(len(names)==156-1,"modules");return names+["tests_lm.test_v05_c271_query_endpoint"]
def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests];req(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"exclude");kept=[t for t in tests if t.id()!=EXCLUDED];req((len(tests),len(kept))==(3670,3669),"suite");return unittest.TestSuite(kept)

def run(*,c270_summary,c269_summary,output_dir,expected_head):
    c270,c269,p267,core,base,aligned,reader,factory,audit=context()
    root=Path(__file__).resolve().parents[2]
    def guard():
        req(audit.git(root,"rev-parse","HEAD").decode().strip()==expected_head and audit.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss" and not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"repo")
    guard()
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c270_summary,c269_summary,root)
    data=p267.dataset()
    p267.validate_data(data)
    prompts=c270.prompt_dataset(data,p267)
    c270.validate_dataset(prompts,data,p267)
    tokens,targets=p267.training_tables(data,factory)
    out=Path(output_dir)
    out.mkdir(parents=True,exist_ok=False)
    records=[]
    states=[]
    for seed in SEEDS:
        models={a:make_arm(seed,a,c269,base,reader,factory) for a in ARMS}
        init=base.fingerprint(models["mean_span"])
        req(base.fingerprint(models["endpoint_span"])==init,"initial")
        for arm in ARMS:
            print(f"[C271] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            r,state=train_one(models[arm],seed,arm,data,prompts,tokens,targets,p267,c270,core,base,factory)
            records.append(r)
            states.append(state)
    torch.save(dict(schema="fold-c271-query-endpoint-models-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    loaded=load_bundle(out/"trained-models.pt")
    for r,state in zip(records,loaded,strict=True):
        replay_one(make_arm(r["seed"],r["arm"],c269,base,reader,factory),state,r,data,prompts,p267,c270,core,base,factory)
    metrics,summary=analyze(records,data,prompts,p267,c270)
    torch.save(dict(schema="fold-c271-query-endpoint-eval-v1",records=records),out/"evaluations.pt")
    for n,v in (("architecture-plan.json",manifest()),("dataset.json",data),("triple-dataset.json",prompts),("measurements.json",metrics),("validation-summary.json",summary)):(out/n).write_bytes(blob(v))
    artifacts=[dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in OUTPUTS];guard();precheck(c270_summary,c269_summary,root)
    for n,w in protected.items():req(audit.sha(n)==w,"modified input")
    payload=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,gate_f_candidate=False,production_adoption=False,unseen_name_transfer_claim=False,arbitrary_name_claim=False,causal_parser_claim=False)
    validate_result(payload);(out/"summary.json").write_bytes(blob(payload));print("=== C271 RESULT ===");print(blob(payload).decode());return payload

def verify_artifacts(outdir,expected_head):
    c270,_,p267,*rest=context();audit=rest[-1];out=Path(outdir);p=audit.read_json(out/"summary.json");validate_result(p);req(p["commit_sha"]==expected_head,"HEAD")
    for n,w in p["input_sha256"].items():req(audit.sha(n)==w,"postcheck input")
    for x in p["artifacts"]:
        child=audit.safe_child(out,x["file"]);req(audit.sha(child)==x["sha256"] and child.stat().st_size==x["serialized_bytes"],"output bytes")
    with patch.object(torch.nn.Module,"_call_impl",side_effect=RuntimeError("postcheck forbids model calls")):
        data=audit.read_json(out/"dataset.json");p267.validate_data(data);prompts=audit.read_json(out/"triple-dataset.json");c270.validate_dataset(prompts,data,p267)
        v=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True);req(set(v)=={"schema","records"} and v["schema"]=="fold-c271-query-endpoint-eval-v1","eval schema")
        metrics,summary=analyze(v["records"],data,prompts,p267,c270)
        for n,val in (("architecture-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):req(audit.read_json(out/n)==val,"persisted:"+n)
    req(summary==p["validation_summary"],"summary");return p,metrics

def main():
    p=argparse.ArgumentParser()
    for n in ("c270-summary","c269-summary","output-dir"):p.add_argument("--"+n,type=Path,required=True)
    p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))
if __name__=="__main__":main()
