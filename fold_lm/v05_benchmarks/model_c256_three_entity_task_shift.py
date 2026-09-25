"""C256: fresh three-entity bilingual assignment shift for the C252 aligned reader."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import time
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID="C256-v5b-three-entity-task-shift"
STAGE="V5-B-THREE-ENTITY-TASK-SHIFT"
BASE="0455a2aed54c54fd1dbc6008cf6f7b80f0521aae"
PARENT_EXECUTION="6b577da1edc7339dbfd68b3127870074de218e48"
PARENT_SHA="6c4e9a569a7c622259b501f209781b357d183dfbaf5750a6d6c939f5e59e3150"
PARENT_ARTIFACTS={
 "contrasts.json":"ecc69baf18f5824ad3c94be836ba55b2f05ace64f5b38d42825dbce37c48f228",
 "diagnostics.json":"111b4c2d98087f0d7e90cddda83ba53892eb74961cb4b0a564392eb36ccc51a4",
 "head-outputs.pt":"77a4e8a54e610a40cd7be3965e863d48e4f5058efebbc49637aa40d043cf1241",
 "validation-summary.json":"69394982329cd77f7ae0d9739f7fe97e898444e331b697fa507287120be99b63",
 "value-plan.json":"e5a6589105d534218c9056768c2af3e60da136a2dfb9f9fa8393bba9198a548a",
}
TASK_SHA="ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b"
SEEDS=(256001,256002,256003,256004,256005)
ARMS=("aligned_precore_read","eos_adapter")
SPLITS,VIEWS=("TRAIN","HOLDOUT"),("normal","evidence_blind","query_blind")
ROWS={"TRAIN":144,"HOLDOUT":144}
ENTITIES={"en":("a","b","c"),"ja":("甲","乙","丙")}
TRAIN_ASSIGNMENTS={(0,1,2),(0,1,3),(0,2,1),(1,0,2),(1,0,3),(1,3,0),
                   (2,0,3),(2,3,0),(2,3,1),(3,1,2),(3,2,0),(3,2,1)}
STEPS,BATCH,LR,CLIP,TOL=800,48,.005,1.,1e-9
OWN=("fold_lm/v05_benchmarks/model_c256_three_entity_task_shift.py",
     "tests_lm/test_v05_c256_three_entity_task_shift.py","tools/run_c256.ps1","tools/invoke_c256.ps1",
     "docs/experiment-ledger-addendum-c256-preregistration.md","docs/v5b-three-entity-task-shift-v0.1.md")
OUTPUTS={"task-plan.json","dataset.json","trained-models.pt","measurements.json","validation-summary.json"}
EXCLUDED="tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA="43948ceb676d536301d4e3a63a7ee1407f8bec44034db59f8b4f6e4872ae53b1"

def require(ok,message):
    if not ok: raise ValueError(message)

def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()

def digest(value): return hashlib.sha256(blob(value)).hexdigest()

def context():
    from fold_lm.v05_benchmarks import model_c255_value_residual_swap as parent
    from fold_lm.v05_benchmarks import model_c248_residual_token_read as reader
    _,_,c252,factory,audit=parent.context()
    return parent,c252,reader,factory,audit

def identities(): return list(itertools.product(SEEDS,ARMS))

def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        task_sha256=TASK_SHA,seeds=list(SEEDS),arms=list(ARMS),rows=ROWS,views=list(VIEWS),
        entities={k:list(v) for k,v in ENTITIES.items()},values=[0,1,2,3],assignments_per_split=12,
        orders=[0,1],queries=[0,1,2],
        split_policy="fixed balanced assignment split; every entity-position/value marginal is 3/12 in each split",
        candidate="C252 Full pre-core query+K/V reader with post-core residual",
        control="equal-parameter C248 Full EOS-only residual adapter",
        common_backbone="same fresh Full backbone state copied to both arms within seed",
        added_parameters=768,parameters=14256,steps_per_model=STEPS,batch_size=BATCH,lr=LR,clip=CLIP,
        optimizer="AdamW",betas=[.9,.999],eps=1e-8,weight_decay=0.,
        sampling="three deterministic 48-row blocks from a seed+epoch randperm of all144 TRAIN rows; same blocks both arms",
        dtype="CPU float64",threads=2,deterministic=True,
        gate=dict(accuracy=.90,order_pair=.80,query_triplet=.80,evidence_drop=.35,query_drop=.35),
        primary="all five aligned-precore seeds pass TRAIN and HOLDOUT in both languages; EOS controls reported separately",
        models=10,train_steps=8000,answer_presentations=384000,model_forward_calls=8120,row_presentations=401280,
        evaluation_forwards=120,checkpoint_writes=1,checkpoint_states=10,
        source_pins=382,protected_inputs=623,direct_dependencies=32,own_tests=24,
        modules=141,loaded_tests=3314,focused_tests=3313,excluded_test=EXCLUDED,
        replay_tolerance=TOL,network_calls=0,production_adoption=False,gate_f_candidate=False,
        external_generalization_claim=False,general_language_claim=False,core_superiority_claim=False)

def render(row,view="normal"):
    require(view in VIEWS,"view")
    names=ENTITIES[row["language"]];facts=list(enumerate(row["assignment"]))
    if row["order"]: facts.reverse()
    text=";".join(names[k]+"="+("?" if view=="evidence_blind" else str(v)) for k,v in facts)
    query="?" if view=="query_blind" else names[row["query"]]
    return text+";"+query+"="

def dataset():
    parts={s:[] for s in SPLITS}
    for assignment in itertools.permutations(range(4),3):
        split="TRAIN" if assignment in TRAIN_ASSIGNMENTS else "HOLDOUT"
        for lang in ("en","ja"):
            for order in (0,1):
                for query in (0,1,2):
                    row=dict(id=f"{lang}-{assignment[0]}{assignment[1]}{assignment[2]}-{order}-{query}",
                        assignment=list(assignment),language=lang,order=order,query=query,target=48+assignment[query])
                    row["prompt"]=render(row);parts[split].append(row)
    validate_dataset(parts);return parts

def validate_dataset(parts):
    require(set(parts)==set(SPLITS) and {s:len(v) for s,v in parts.items()}==ROWS,"row counts")
    require(digest(parts)==TASK_SHA,"task hash")
    require(not ({tuple(r["assignment"]) for r in parts["TRAIN"]}&{tuple(r["assignment"]) for r in parts["HOLDOUT"]}),"assignment overlap")
    for split,rows in parts.items():
        require(len({r["id"] for r in rows})==144 and {r["language"] for r in rows}=={"en","ja"},"row identity/languages")
        assignments={tuple(r["assignment"]) for r in rows};require(len(assignments)==12,"assignment count")
        for pos in range(3):
            counts=Counter(a[pos] for a in assignments);require(counts=={0:3,1:3,2:3,3:3},"marginal balance")
        for r in rows:
            require(r["prompt"]==render(r) and len(r["prompt"].encode())<=46 and r["target"]==48+r["assignment"][r["query"]],"row semantics")
    return parts

def tensors(rows,view,factory):
    return torch.stack([factory.prefix_tensor(render(r,view).encode()) for r in rows]),torch.tensor([r["target"] for r in rows],dtype=torch.int64)

def metrics(rows,outputs):
    require(set(outputs)==set(VIEWS) and len(rows)==144,"metric input")
    predictions={}
    for view,value in outputs.items():
        require(isinstance(value,torch.Tensor) and value.shape==(144,256) and value.dtype==torch.float64
                and value.device.type=="cpu" and bool(torch.isfinite(value).all()),"finite logits")
        predictions[view]=value.argmax(-1).tolist()
    target=torch.tensor([r["target"] for r in rows],dtype=torch.int64)
    nll=F.cross_entropy(outputs["normal"],target,reduction="none")
    result={}
    for lang in ("en","ja"):
        ids=[i for i,r in enumerate(rows) if r["language"]==lang];require(len(ids)==72,"language rows")
        acc={v:sum(predictions[v][i]==rows[i]["target"] for i in ids)/72 for v in VIEWS}
        order=defaultdict(list);queries=defaultdict(list)
        for i in ids:
            r=rows[i];a=tuple(r["assignment"])
            order[(a,r["query"])].append(i);queries[(a,r["order"])].append(i)
        require(len(order)==36 and all(len(g)==2 for g in order.values()),"order pairs")
        require(len(queries)==24 and all(len(g)==3 for g in queries.values()),"query triplets")
        require(all(len({rows[i]["target"] for i in g})==1 for g in order.values()),"order targets")
        require(all(len({rows[i]["target"] for i in g})==3 for g in queries.values()),"query targets")
        result[lang]=dict(rows=72,accuracy=acc["normal"],answer_nll=float(nll[ids].mean()),
            evidence_blind_accuracy=acc["evidence_blind"],query_blind_accuracy=acc["query_blind"],
            evidence_drop=acc["normal"]-acc["evidence_blind"],query_drop=acc["normal"]-acc["query_blind"],
            order_pair_accuracy=sum(all(predictions["normal"][i]==rows[i]["target"] for i in g) for g in order.values())/36,
            query_triplet_accuracy=sum(all(predictions["normal"][i]==rows[i]["target"] for i in g) for g in queries.values())/24)
    return result,predictions

def validate_metrics(value):
    require(set(value)=={"en","ja"},"metric languages")
    keys={"rows","accuracy","answer_nll","evidence_blind_accuracy","query_blind_accuracy","evidence_drop","query_drop",
          "order_pair_accuracy","query_triplet_accuracy"}
    for m in value.values():
        require(set(m)==keys and m["rows"]==72 and all(type(x) in (int,float) and math.isfinite(x) for x in m.values()),"metric schema")

def cell_pass(m):
    return (m["accuracy"]>=.90 and m["order_pair_accuracy"]>=.80 and m["query_triplet_accuracy"]>=.80
            and m["evidence_drop"]>=.35 and m["query_drop"]>=.35)

def metric_error(left,right):
    require(set(left)==set(right)==set(SPLITS),"metric split keys");err=0.0
    for split in SPLITS:
        require(set(left[split])==set(right[split])=={"en","ja"},"metric languages")
        for lang in ("en","ja"):
            require(set(left[split][lang])==set(right[split][lang]),"metric keys")
            for key,value in left[split][lang].items():
                old=right[split][lang][key];require(type(value) in (int,float) and type(old) in (int,float) and math.isfinite(value) and math.isfinite(old),"metric finite")
                err=max(err,abs(value-old))
    return err

def batch_indices(seed,step):
    require(seed in SEEDS and type(step) is int and 0<=step<STEPS,"batch step")
    epoch,block=divmod(step,3);g=torch.Generator(device="cpu").manual_seed(seed+256000+epoch)
    return torch.randperm(144,generator=g)[block*BATCH:(block+1)*BATCH]

def make_model(backbone,arm,seed,c252,reader):
    require(arm in ARMS,"arm")
    return c252.AlignedPrecoreReadout(backbone,seed) if arm=="aligned_precore_read" else reader.ReadoutPilot(backbone,"full","eos_adapter",seed)

def evaluate(model,parts,factory):
    before=fingerprint(model);model.eval();out={};pred={};raw={}
    with torch.no_grad():
        for split in SPLITS:
            logits={}
            for view in VIEWS:
                x,_=tensors(parts[split],view,factory);logits[view]=model(x,torch.zeros(len(x),dtype=torch.int64))
            out[split],pred[split]=metrics(parts[split],logits);raw[split]=logits
    require(fingerprint(model)==before,"evaluation mutation")
    return out,pred,raw

def fingerprint(module):
    h=hashlib.sha256()
    for name,t in sorted(module.state_dict().items()):
        v=t.detach().cpu().contiguous();h.update(name.encode());h.update(str(v.dtype).encode());h.update(str(tuple(v.shape)).encode());h.update(v.numpy().tobytes())
    return h.hexdigest()

def fit(model,train_tokens,train_targets,seed):
    require(train_tokens.shape==(144,48) and train_targets.shape==(144,),"fit inputs")
    opt=torch.optim.AdamW(model.parameters(),lr=LR,betas=(.9,.999),eps=1e-8,weight_decay=0.0)
    model.train();started=time.perf_counter();first=last=None
    for step in range(STEPS):
        ids=batch_indices(seed,step);opt.zero_grad(set_to_none=True)
        logits=model(train_tokens[ids],torch.zeros(BATCH,dtype=torch.int64));loss=F.cross_entropy(logits,train_targets[ids])
        require(bool(torch.isfinite(loss)),"nonfinite loss");loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),CLIP,error_if_nonfinite=True);opt.step()
        last=float(loss.detach());first=last if first is None else first
        if (step+1)%200==0: print(f"[C256] seed={seed} step={step+1}/{STEPS} answer_nll={last:.6f}",flush=True)
    model.eval();return dict(steps=STEPS,answer_presentations=STEPS*BATCH,first_loss=first,last_loss=last,fit_seconds=time.perf_counter()-started)

def train_one(model,parts,seed,arm,backbone_initial,factory):
    require(sum(p.numel() for p in model.parameters())==14256,"parameter count")
    require(fingerprint(model.backbone)==backbone_initial,"common backbone")
    wrapper_initial=fingerprint(model);head_initial=fingerprint(model.read);counts=[0,0]
    def hook(module,args,output): counts[0]+=1;counts[1]+=len(args[0])
    h=model.register_forward_hook(hook)
    try:
        x,y=tensors(parts["TRAIN"],"normal",factory);fit_record=fit(model,x,y,seed);final,pred,raw=evaluate(model,parts,factory)
    finally:h.remove()
    require(counts==[806,39264],"model workload")
    final_sha=fingerprint(model);head_final=fingerprint(model.read)
    return (dict(seed=seed,arm=arm,parameters=14256,backbone_initial_sha256=backbone_initial,
        wrapper_initial_sha256=wrapper_initial,head_initial_sha256=head_initial,final_sha256=final_sha,
        fit=fit_record,forward_calls=counts[0],row_presentations=counts[1],weights_changed=final_sha!=wrapper_initial,
        head_weights_changed=head_final!=head_initial,final=final,predictions=pred),
        {k:v.detach().cpu().clone() for k,v in model.state_dict().items()},raw)

def replay_one(model,state,record,raw,parts,factory):
    model.load_state_dict(state,strict=True);model.eval();require(fingerprint(model)==record["final_sha256"],"checkpoint identity")
    counts=[0,0]
    def hook(module,args,output):counts[0]+=1;counts[1]+=len(args[0])
    h=model.register_forward_hook(hook)
    try: final,pred,now=evaluate(model,parts,factory)
    finally:h.remove()
    require(counts==[6,864] and metric_error(final,record["final"])<=TOL and pred==record["predictions"],"reload metrics/workload")
    err=max(float((now[s][v]-raw[s][v]).abs().max()) for s in SPLITS for v in VIEWS)
    require(err<=TOL,"reload logits")
    record["checkpoint_roundtrip"]=True;record["reload_max_error"]=err;record["replay_forward_calls"]=6;record["replay_row_presentations"]=864

def summarize(records):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"identity order")
    outcomes={a:Counter() for a in ARMS};seed_results=[];comparisons=[]
    for r in records:
        require(r["parameters"]==14256 and r["weights_changed"] and r["head_weights_changed"] and r.get("checkpoint_roundtrip") is True,"integrity")
        require((r["fit"]["steps"],r["fit"]["answer_presentations"],r["forward_calls"],r["row_presentations"],r["replay_forward_calls"],r["replay_row_presentations"])==(800,38400,806,39264,6,864),"workload")
        require(type(r["reload_max_error"]) in (int,float) and 0<=r["reload_max_error"]<=TOL,"replay error")
        passed=True
        for split in SPLITS: validate_metrics(r["final"][split])
        for lang in ("en","ja"):
            train=cell_pass(r["final"]["TRAIN"][lang]);held=cell_pass(r["final"]["HOLDOUT"][lang])
            outcomes[r["arm"]]["TRAIN_CRITERIA_MISS" if not train else "TASK_SHIFT_MISS" if not held else "BOTH_PASS"]+=1
            passed &= train and held
        seed_results.append(dict(seed=r["seed"],arm=r["arm"],both_languages_pass=passed))
    for i in range(0,len(records),2):
        a,c=records[i:i+2];require(a["seed"]==c["seed"] and a["arm"]==ARMS[0] and c["arm"]==ARMS[1],"paired arms")
        for lang in ("en","ja"):
            av=a["final"]["HOLDOUT"][lang]["accuracy"];cv=c["final"]["HOLDOUT"][lang]["accuracy"]
            comparisons.append(dict(seed=a["seed"],language=lang,candidate_accuracy=av,control_accuracy=cv,delta=av-cv))
    candidate_gate=all(x["both_languages_pass"] for x in seed_results if x["arm"]==ARMS[0])
    return dict(models=10,candidate_gate=candidate_gate,
        seed_pass_counts={a:sum(x["both_languages_pass"] for x in seed_results if x["arm"]==a) for a in ARMS},
        seed_results=seed_results,cell_outcomes={a:dict(outcomes[a]) for a in ARMS},comparisons=comparisons,
        train_steps=sum(r["fit"]["steps"] for r in records),answer_presentations=sum(r["fit"]["answer_presentations"] for r in records),
        model_forward_calls=sum(r["forward_calls"]+r["replay_forward_calls"] for r in records),
        row_presentations=sum(r["row_presentations"]+r["replay_row_presentations"] for r in records),
        all_replays=True,all_weights_changed=True)

def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(382,623) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"artifacts")
    s=p["validation_summary"]
    require((s["models"],s["train_steps"],s["answer_presentations"],s["model_forward_calls"],s["row_presentations"])==(10,8000,384000,8120,401280),"total workload")
    require(len(s["seed_results"])==10 and len(s["comparisons"])==10 and all(sum(s["cell_outcomes"][a].values())==10 for a in ARMS),"summary coverage")
    require(p["status"]==("PASS" if s["candidate_gate"] else "FAIL") and s["all_replays"] and s["all_weights_changed"],"status/integrity")
    require(p["production_adoption"] is False and p["gate_f_candidate"] is False and p["network_calls"]==0,"scope")

def validate_registration(source_count,input_count):
    actual_hash=digest(manifest())
    print(f"registration_check = source_pins:{source_count}; protected_inputs:{input_count}; manifest_sha256:{actual_hash}",flush=True)
    require((source_count,input_count)==(382,623),
        f"source/input counts: expected=(382, 623) actual=({source_count}, {input_count})")
    require(actual_hash==MANIFEST_SHA,
        f"manifest hash: expected={MANIFEST_SHA} actual={actual_hash}")

def precheck(c255_summary,root):
    parent,_,_,factory,a=context();path=Path(c255_summary).resolve();root=Path(root)
    require(a.sha(path)==PARENT_SHA,"parent summary");p=a.read_json(path);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS","accepted parent")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items():require(Path(name).is_file() and a.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items():require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    require(str(path) not in protected,"parent duplicate");protected[str(path)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifacts")
    for item in p["artifacts"]:
        child=a.safe_child(path.parent,item["file"]);require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"parent artifact bytes")
        require(str(child.resolve()) not in protected,"artifact duplicate");protected[str(child.resolve())]=item["sha256"]
    for name in OWN:
        require(name not in pins,"OWN collision");pins[name]=a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    helpers=("gate_f_c230_prepared_capsule.py","model_c231_byte_eval_contract.py","model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py","model_c234_context_binding.py","model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py","model_c237_frozen_signal_audit.py","model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py","model_c240_saved_position_audit.py","model_c241_assignment_holdout.py",
        "model_c242_balanced_recombination.py","model_c243_saved_recombination_audit.py","model_c244_two_partner_recombination.py",
        "model_c245_selective_evidence.py","model_c246_training_erasure.py","model_c247_normal_exposure_control.py",
        "model_c248_residual_token_read.py","model_c249_frozen_read_ablation.py","model_c250_fresh_seed_replication.py",
        "model_c251_precore_read.py","model_c252_precore_query_alignment.py","model_c253_frozen_residual_path.py",
        "model_c254_paired_residual_swap.py","model_c255_value_residual_swap.py")
    deps=set(factory.LM_SOURCES)|{"fold_lm/v05_benchmarks/"+n for n in helpers}|{OWN[0]}
    require(len(deps)==32 and deps<=set(pins),"dependencies")
    protected.update(a.protect_tree_files(root,pins))
    validate_registration(len(pins),len(protected))
    validate_dataset(dataset());require(set(SEEDS).isdisjoint({250001,250002,250003,250004,250005}),"fresh seeds")
    return pins,protected

def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(v["schema"]=="fold-c256-three-entity-v1" and v["identities"]==[list(x) for x in identities()] and len(v["states"])==10,"bundle")
    return v["states"]

def regression_modules(root):
    names=context()[0].regression_modules(root);require(len(names)==len(set(names))==140,"parent modules")
    return names+["tests_lm.test_v05_c256_three_entity_task_shift"]

def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item

def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"test identities")
    kept=[t for t in tests if t.id()!=EXCLUDED];require((len(tests),len(kept))==(3314,3313),"suite counts")
    return unittest.TestSuite(kept)

def run(*,c255_summary,output_dir,expected_head):
    _,c252,reader,factory,a=context();root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c255_summary,root);parts=dataset();records=[];states=[];raw=[];out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for seed in SEEDS:
        source=factory.new_model(seed);backbone_initial=fingerprint(source)
        for arm in ARMS:
            require(fingerprint(source)==backbone_initial,"source backbone mutation")
            model=make_model(copy.deepcopy(source),arm,seed,c252,reader)
            print(f"[C256] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            record,state,outputs=train_one(model,parts,seed,arm,backbone_initial,factory)
            records.append(record);states.append(state);raw.append(outputs)
        require(fingerprint(source)==backbone_initial,"source backbone changed")
    torch.save(dict(schema="fold-c256-three-entity-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for r,state,outputs in zip(records,load_bundle(out/"trained-models.pt"),raw,strict=True):
        model=make_model(factory.new_model(r["seed"]),r["arm"],r["seed"],c252,reader);replay_one(model,state,r,outputs,parts,factory)
    summary=summarize(records)
    for name,value in (("task-plan.json",manifest()),("dataset.json",parts),("measurements.json",records),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=n,sha256=a.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard();precheck(c255_summary,root)
    for name,wanted in protected.items():require(a.sha(name)==wanted,"modified input")
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        production_adoption=False,gate_f_candidate=False,network_calls=0)
    validate_result(p);(out/"summary.json").write_bytes(blob(p));print("=== C256 RESULT ===",flush=True);print(blob(p).decode(),flush=True);return p

def verify_artifacts(output_dir,expected_head):
    _,_,_,_,a=context();out=Path(output_dir);p=a.read_json(out/"summary.json");validate_result(p);require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():require(a.sha(name)==wanted,"postcheck input")
    for item in p["artifacts"]:
        child=a.safe_child(out,item["file"]);require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"artifact")
    parts=a.read_json(out/"dataset.json");validate_dataset(parts);records=a.read_json(out/"measurements.json")
    require(a.read_json(out/"task-plan.json")==manifest() and summarize(records)==p["validation_summary"]==a.read_json(out/"validation-summary.json"),"persisted replay")
    return p,records

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ("c255-summary","output-dir"):p.add_argument("--"+n,type=Path,required=True)
    p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))

if __name__=="__main__":main()
