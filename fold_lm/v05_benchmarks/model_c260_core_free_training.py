"""C260: training-time core ablation; the accepted Full reference is not modified."""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import time
import unittest
import torch
from torch import nn
from torch.nn import functional as F

EXPERIMENT_ID = "C260-v5b-paired-core-free-training"
STAGE = "V5-B-PAIRED-CORE-FREE-TRAINING"
BASE = "e3311dd21eb5b7235e02dc0d6b59352086691fcb"
PARENT_EXECUTION = "78f0811c390d11256e748b1f955f505ad803de49"
PARENT_SHA = "e005a223fd138ef43e6a3a4664c31a7f2f64482f8325252ba11ad2fdf2562ab1"
PARENT_ARTIFACTS = {
    "coverage-plan.json": "2ec7894fe267260d8bc16d1275d7407833c0592e0910f8149639f90c830bfdcb",
    "dataset.json": "3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56",
    "evaluations.pt": "25282bfeace30ec5fd9be8e46c0aa7f8b3e243a8d0fa2606d656dae5d462e01d",
    "measurements.json": "b833dbdd66373396ba3345385bd92e48a002b1377a0993a217d34ae0d7898862",
    "trained-models.pt": "372fab6bbff0c7160c9b89ca8f7147db0f923ef1205f2799466a85f9b61ef3a7",
    "validation-summary.json": "117d4a99611e1aab0109f67e3d4d3012855b22d75d336833557db769519a8b16",
}
SEEDS = (260001,260002,260003,260004,260005)
ARMS = ("with_core","without_core")
PARAMETERS = {"with_core":14256,"without_core":10928}
SPLITS = ("TRAIN","HOLDOUT")
VIEWS = ("normal","evidence_blind","query_blind")
STEPS, BATCH, TOL = 800, 48, 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c260_core_free_training.py",
       "tests_lm/test_v05_c260_core_free_training.py","tools/run_c260.ps1","tools/invoke_c260.ps1",
       "docs/experiment-ledger-addendum-c260-preregistration.md","docs/v5b-core-free-training-v0.1.md")
OUTPUTS = {"core-plan.json","dataset.json","trained-models.pt","evaluations.pt","measurements.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "ee2ef5e828c22900a5e718ca867181dd7430a90b28eec7f112a61d3b8574e8ae"


def require(ok,message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c259_order_coverage_training as parent
    _,base,orders,aligned,reader,factory,audit = parent.context()
    return parent,base,orders,aligned,reader,factory,audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        seeds=list(SEEDS),arms=list(ARMS),parameters=PARAMETERS,removed_core_parameters=3328,
        changed="remove state-update core; reader residual base becomes pre-core EOS; train both from scratch",
        paired="identical surviving initial state and six-order logical batches; not parameter/FLOP matched",
        original_dataset_sha256="ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b",
        extra_dataset_sha256="9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052",
        schedule="C259 six-order policy; epoch=s//3,block=s%3; randperm144 seed+256000+epoch; pair=epoch%3",
        pair_updates=[267,267,266],steps=800,batch=48,lr=.005,clip=1.,betas=[.9,.999],eps=1e-8,
        optimizer="AdamW",weight_decay=0.,fit_rng="seed+259000,reset per arm",
        dtype="CPU float64",threads=2,deterministic=True,
        primary="all five without_core seeds pass both splits/languages; with_core gates and paired effects separate",
        gate=dict(accuracy=.90,original_order_pair=.80,query_triplet=.80,evidence_drop=.35,query_drop=.35,six_order=.80),
        models=10,train_steps=8000,answer_presentations=384000,model_forward_calls=8240,row_presentations=435840,
        core_forward_calls=16480,core_forward_calls_without_core=0,evaluation_forwards=240,
        checkpoint_bundle_loads=1,model_state_loads=10,new_checkpoint_writes=1,checkpoint_states=10,
        source_pins=406,protected_inputs=672,direct_dependencies=36,own_tests=24,
        modules=145,loaded_tests=3406,focused_tests=3405,excluded_test=EXCLUDED,
        replay_tolerance=TOL,network_calls=0,gate_f_candidate=False,production_adoption=False,
        core_superiority_claim=False,unseen_order_transfer_claim=False,general_language_claim=False)


def common_fingerprint(model):
    h = hashlib.sha256()
    for name,tensor in sorted(model.state_dict().items()):
        if name.startswith("backbone.core."):
            continue
        value = tensor.detach().cpu().contiguous()
        h.update(name.encode());h.update(str(value.dtype).encode());h.update(str(tuple(value.shape)).encode());h.update(value.numpy().tobytes())
    return h.hexdigest()


class CoreFreeReadout(nn.Module):
    """Same encoder and reader, with pre-core EOS residual and no retained core parameters."""
    def __init__(self,template):
        super().__init__()
        self.backbone = copy.deepcopy(template.backbone)
        self.read = copy.deepcopy(template.read)
        self.backbone.core = None
        self.family = "core_free"
        require(sum(p.numel() for p in self.parameters()) == PARAMETERS["without_core"],"core-free capacity")

    def forward(self,tokens,tasks):
        self.backbone._validate(tokens,tasks)
        require(bool((tasks==0).all()),"NEXT-only")
        valid = tokens!=256;indices = torch.arange(len(tokens),device=tokens.device);eos = valid.sum(1)-1
        require(bool((eos>=1).all()) and bool((tokens[indices,eos]==258).all()),"EOS")
        local = self.backbone.encode_local(tokens)
        pre = local[indices,eos]
        q = self.read.query(pre)
        scores = (self.read.key(local)*q.unsqueeze(1)).sum(-1)/4.0
        alpha = scores.masked_fill(~valid,float("-inf")).softmax(-1)
        memory = (alpha.unsqueeze(-1)*local).sum(1)
        logits = self.backbone.decoder(self.backbone.readout_norm(pre+self.read.output(memory)))
        require(logits.shape==(len(tokens),256) and bool(torch.isfinite(logits).all()),"output")
        return logits


def make_pair(seed,base,aligned,reader,factory):
    require(seed in SEEDS,"seed")
    template = base.make_model(factory.new_model(seed),"aligned_precore_read",seed,aligned,reader)
    before = base.fingerprint(template)
    pair = (copy.deepcopy(template),CoreFreeReadout(template))
    require(base.fingerprint(template)==before,"template mutation")
    require(common_fingerprint(pair[0])==common_fingerprint(pair[1]),"surviving initial state")
    require([sum(p.numel() for p in m.parameters()) for m in pair]==[PARAMETERS[a] for a in ARMS],"pair capacities")
    return pair


def batch_plan(seed,step):
    require(seed in SEEDS and type(step) is int and 0<=step<STEPS,"batch identity")
    epoch,block = divmod(step,3)
    g = torch.Generator(device="cpu").manual_seed(seed+256000+epoch)
    return torch.randperm(144,generator=g)[block*BATCH:(block+1)*BATCH],epoch%3


def fit(model,tokens,targets,seed):
    require(tokens.shape==(3,144,48) and targets.shape==(144,),"TRAIN tables")
    torch.manual_seed(seed+259000)
    opt = torch.optim.AdamW(model.parameters(),lr=.005,betas=(.9,.999),eps=1e-8,weight_decay=0.)
    model.train();trace = hashlib.sha256();pairs=[0,0,0];start=time.perf_counter();last=None
    for step in range(STEPS):
        ids,pair = batch_plan(seed,step);trace.update(ids.numpy().tobytes());pairs[pair]+=1
        opt.zero_grad(set_to_none=True)
        logits = model(tokens[pair,ids],torch.zeros(BATCH,dtype=torch.int64))
        loss = F.cross_entropy(logits,targets[ids]);require(bool(torch.isfinite(loss)),"nonfinite loss")
        loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True);opt.step()
        last=float(loss.detach())
        if (step+1)%200==0:
            print(f"[C260] seed={seed} step={step+1}/{STEPS} answer_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=STEPS,answer_presentations=STEPS*BATCH,logical_batch_sha256=trace.hexdigest(),
                order_pair_updates=pairs,last_loss=last,fit_seconds=time.perf_counter()-start)


def core_counter(model):
    calls=[0]
    def counted(module,args,output):
        calls[0]+=1
    core=model.backbone.core
    return calls,None if core is None else core.register_forward_hook(counted)


def train_one(model,parts,extra,tokens,targets,seed,arm,parent,base,orders,factory):
    require(arm in ARMS and sum(p.numel() for p in model.parameters())==PARAMETERS[arm],"arm capacity")
    initial=base.fingerprint(model);common=common_fingerprint(model);head=base.fingerprint(model.read)
    counts=[0,0];cores,core_handle=core_counter(model)
    def counted(module,args,output):
        counts[0]+=1;counts[1]+=len(args[0])
    handle=model.register_forward_hook(counted)
    try:
        fitted=fit(model,tokens,targets,seed)
        raw=parent.evaluate(model,parts,extra,base,orders,factory)
    finally:
        handle.remove()
        if core_handle is not None:core_handle.remove()
    require(counts==[812,40992] and cores[0]==(3248 if arm=="with_core" else 0),"training/final workload")
    final=base.fingerprint(model)
    require(final!=initial and common_fingerprint(model)!=common and base.fingerprint(model.read)!=head,"weights did not change")
    r=dict(seed=seed,arm=arm,parameters=PARAMETERS[arm],initial_sha256=initial,common_initial_sha256=common,
           final_sha256=final,weights_changed=True,common_changed=True,head_changed=True,fit=fitted,
           forward_calls=812,row_presentations=40992,core_forward_calls=cores[0],raw=raw)
    return r,{k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def replay_one(model,state,record,parts,extra,parent,base,orders,factory):
    cores,handle=core_counter(model)
    try:
        parent.replay_one(model,state,record,parts,extra,base,orders,factory)
    finally:
        if handle is not None:handle.remove()
    require(cores[0]==(48 if record["arm"]=="with_core" else 0),"replay core calls")
    record["replay_core_forward_calls"]=cores[0]


def score(raw,parts,extra,base,orders):
    require(set(raw)=={"original","extra"},"raw stages")
    for stage in raw:
        require(set(raw[stage])==set(SPLITS) and all(set(raw[stage][s])==set(VIEWS) for s in SPLITS),"split/views")
    original={};additional={};six={};all_order={}
    for split in SPLITS:
        original[split],op=base.metrics(parts[split],raw["original"][split])
        additional[split],ep=orders.new_metrics(extra[split],raw["extra"][split])
        six[split]=orders.six_order_metrics(parts[split],extra[split],op["normal"],ep["normal"])
        all_order[split]={}
        for lang in ("en","ja"):
            correct=sum(p==r["target"] for rows,preds in ((parts[split],op["normal"]),(extra[split],ep["normal"])) for r,p in zip(rows,preds,strict=True) if r["language"]==lang)
            all_order[split][lang]=dict(correct=correct,rows=216,accuracy=correct/216)
    old_ok=all(base.cell_pass(c) for split in original.values() for c in split.values())
    new_ok=all(orders.new_cell_pass(c) for cells in additional.values() for c in cells)
    six_ok=all(c["accuracy"]>=.8 for split in six.values() for c in split.values())
    return dict(original=original,extra_orders=additional,six_order=six,all_order_accuracy=all_order,
                passed=old_ok and new_ok and six_ok,
                outcome="ORIGINAL_CRITERIA_MISS" if not old_ok else "EXTRA_ORDER_MISS" if not new_ok else "SIX_ORDER_MISS" if not six_ok else "PASS")


def analyze(records,parts,extra,base,orders):
    require([(r["seed"],r["arm"]) for r in records]==identities(),"record identities")
    require(parts==base.dataset() and extra==orders.novel_dataset(parts),"dataset identity")
    measured=[];results=[]
    for r in records:
        require(r["parameters"]==PARAMETERS[r["arm"]] and all(r[k] is True for k in ("weights_changed","common_changed","head_changed","checkpoint_roundtrip")),"record integrity")
        require((r["fit"]["steps"],r["fit"]["answer_presentations"],r["forward_calls"],r["row_presentations"],r["replay_forward_calls"],r["replay_row_presentations"])==(800,38400,812,40992,12,2592),"record workload")
        require(r["fit"]["order_pair_updates"]==[267,267,266],"six-order schedule")
        require((r["core_forward_calls"],r["replay_core_forward_calls"])==((3248,48) if r["arm"]=="with_core" else (0,0)),"core workload")
        require(type(r["reload_max_error"]) in (int,float) and math.isfinite(r["reload_max_error"]) and 0<=r["reload_max_error"]<=TOL,"replay error")
        m=score(r["raw"],parts,extra,base,orders)
        measured.append(dict(seed=r["seed"],arm=r["arm"],parameters=r["parameters"],fit=r["fit"],**m))
        results.append(dict(seed=r["seed"],arm=r["arm"],passed=m["passed"],outcome=m["outcome"]))
    comparisons=[]
    for i in range(0,len(records),2):
        a,b=records[i:i+2];am,bm=measured[i:i+2]
        require(a["common_initial_sha256"]==b["common_initial_sha256"] and a["fit"]["logical_batch_sha256"]==b["fit"]["logical_batch_sha256"],"paired common state/batches")
        for lang in ("en","ja"):
            av,bv=am["all_order_accuracy"]["HOLDOUT"][lang]["accuracy"],bm["all_order_accuracy"]["HOLDOUT"][lang]["accuracy"]
            ac,bc=am["six_order"]["HOLDOUT"][lang]["accuracy"],bm["six_order"]["HOLDOUT"][lang]["accuracy"]
            comparisons.append(dict(seed=a["seed"],language=lang,with_core_accuracy=av,without_core_accuracy=bv,
                                    accuracy_delta=bv-av,with_core_six_order=ac,without_core_six_order=bc,six_order_delta=bc-ac))
    summary=dict(models=10,seed_results=results,seed_pass_counts={a:sum(r["passed"] for r in results if r["arm"]==a) for a in ARMS},
        candidate_gate=all(r["passed"] for r in results if r["arm"]=="without_core"),comparisons=comparisons,
        train_steps=8000,answer_presentations=384000,model_forward_calls=8240,row_presentations=435840,
        core_forward_calls=16480,core_forward_calls_without_core=0,checkpoint_bundle_loads=1,model_state_loads=10,
        new_checkpoint_writes=1,all_replays=True,all_pairs_matched=True,all_weights_changed=True)
    return measured,summary


def load_parent(path):
    parent,_,_,_,_,_,a=context();path=Path(path).resolve()
    require(a.sha(path)==PARENT_SHA,"parent summary hash")
    p,measurements=parent.verify_artifacts(path.parent,PARENT_EXECUTION)
    require(p["status"]=="FAIL" and p["validation_summary"]["seed_pass_counts"]=={"two_order":2,"six_order":4},"accepted C259 negative")
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS and len(measurements)==10,"parent artifact contract")
    return p


def validate_registration(source_count,input_count):
    actual=digest(manifest())
    print(f"registration_check = source_pins:{source_count}; protected_inputs:{input_count}; manifest_sha256:{actual}",flush=True)
    require((source_count,input_count)==(406,672),f"source/input counts: expected=(406, 672) actual=({source_count}, {input_count})")
    require(actual==MANIFEST_SHA,f"manifest hash: expected={MANIFEST_SHA} actual={actual}")


def precheck(path,root):
    _,_,_,_,_,factory,a=context();path=Path(path).resolve();root=Path(root);p=load_parent(path)
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items():require(Path(name).is_file() and a.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items():require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    for child,wanted in [(path,PARENT_SHA)]+[(a.safe_child(path.parent,x["file"]),x["sha256"]) for x in p["artifacts"]]:
        name=str(child.resolve());require(name not in protected,"input duplicate");protected[name]=wanted
    for name in OWN:
        require(name not in pins,"OWN collision");pins[name]=a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    pattern=r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9])_[^/]+)\.py"
    deps=set(factory.LM_SOURCES)|{n for n in p["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps)==36 and deps<=set(pins),"direct dependency protection")
    protected.update(a.protect_tree_files(root,pins));validate_registration(len(pins),len(protected))
    return pins,protected


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(406,672) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==6 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"artifacts")
    s=p["validation_summary"]
    for k,v in dict(models=10,train_steps=8000,answer_presentations=384000,model_forward_calls=8240,row_presentations=435840,core_forward_calls=16480,core_forward_calls_without_core=0,checkpoint_bundle_loads=1,model_state_loads=10,new_checkpoint_writes=1).items():
        require(type(s[k]) is int and s[k]==v,"workload:"+k)
    require([(r["seed"],r["arm"]) for r in s["seed_results"]]==identities() and len(s["comparisons"])==10,"summary identities")
    require(type(s["candidate_gate"]) is bool and p["status"]==("PASS" if s["candidate_gate"] else "FAIL"),"status")
    require(all(s[k] is True for k in ("all_replays","all_pairs_matched","all_weights_changed")),"integrity flags")
    require(all(p[k] is False for k in ("gate_f_candidate","production_adoption","core_superiority_claim","unseen_order_transfer_claim")) and p["network_calls"]==0,"scope")


def regression_modules(root):
    names=context()[0].regression_modules(root)
    require(len(names)==len(set(names))==144,"parent modules")
    return names+["tests_lm.test_v05_c260_core_free_training"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))));ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"suite IDs")
    kept=[t for t in tests if t.id()!=EXCLUDED];require((len(tests),len(kept))==(3406,3405),"suite counts")
    return unittest.TestSuite(kept)


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(set(v)=={"schema","identities","states"} and v["schema"]=="fold-c260-core-models-v1","bundle schema")
    require(v["identities"]==[list(x) for x in identities()] and len(v["states"])==10,"bundle identity")
    return v["states"]


def run(*,c259_summary,output_dir,expected_head):
    parent,base,orders,aligned,reader,factory,a=context();root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c259_summary,root);parts=base.dataset();extra=orders.novel_dataset(parts)
    tokens,targets=parent.training_tables(parts,factory,orders)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False);records=[];states=[]
    for seed in SEEDS:
        pair=make_pair(seed,base,aligned,reader,factory)
        for arm,model in zip(ARMS,pair,strict=True):
            print(f"[C260] model={len(records)+1}/10 seed={seed} arm={arm} parameters={PARAMETERS[arm]}",flush=True)
            r,state=train_one(model,parts,extra,tokens,targets,seed,arm,parent,base,orders,factory)
            records.append(r);states.append(state)
    torch.save(dict(schema="fold-c260-core-models-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    loaded=load_bundle(out/"trained-models.pt")
    for i,seed in enumerate(SEEDS):
        pair=make_pair(seed,base,aligned,reader,factory)
        for j,model in enumerate(pair):
            k=2*i+j;replay_one(model,loaded[k],records[k],parts,extra,parent,base,orders,factory)
    measurements,summary=analyze(records,parts,extra,base,orders)
    torch.save(dict(schema="fold-c260-core-eval-v1",records=records),out/"evaluations.pt")
    for name,value in (("core-plan.json",manifest()),("dataset.json",dict(original=parts,extra=extra)),("measurements.json",measurements),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=n,sha256=a.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard();precheck(c259_summary,root)
    for name,wanted in protected.items():require(a.sha(name)==wanted,"modified input")
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,production_adoption=False,core_superiority_claim=False,unseen_order_transfer_claim=False,network_calls=0)
    validate_result(p);(out/"summary.json").write_bytes(blob(p));print("=== C260 RESULT ===",flush=True);print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(output_dir,expected_head):
    _,base,orders,_,_,_,a=context();out=Path(output_dir);p=a.read_json(out/"summary.json")
    validate_result(p);require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():require(a.sha(name)==wanted,"postcheck input")
    for x in p["artifacts"]:
        child=a.safe_child(out,x["file"]);require(a.sha(child)==x["sha256"] and child.stat().st_size==x["serialized_bytes"],"artifact bytes")
    data=a.read_json(out/"dataset.json");v=torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
    require(set(v)=={"schema","records"} and v["schema"]=="fold-c260-core-eval-v1","evaluation schema")
    measurements,summary=analyze(v["records"],data["original"],data["extra"],base,orders)
    for name,value in (("core-plan.json",manifest()),("measurements.json",measurements),("validation-summary.json",summary)):
        require(a.read_json(out/name)==value,"persisted recomputation:"+name)
    require(summary==p["validation_summary"],"summary replay")
    return p,measurements


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("c259-summary","output-dir"):p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))


if __name__=="__main__":
    main()
