"""C248: experimental residual token reader vs equal-parameter EOS-only adapter."""
from __future__ import annotations
import argparse
import ast
from collections import Counter
import copy
import hashlib
import inspect
import itertools
import json
import math
from pathlib import Path
import time
import unittest
import torch
from torch import nn
from torch.nn import functional as F

EXPERIMENT_ID = "C248-v5b-residual-token-read-pilot"
STAGE = "V5-B-RESIDUAL-TOKEN-READ-PILOT"
BASE = "521eff1865cd13224ff5a2a247c466a6ba330d3e"
PARENT_EXECUTION = "6705aa76bf70ec2685100c47e1abe9cec3625523"
PARENT_SHA = "2f77f23ee7b77016ad44e1900b7396bbe07855e13429adc32cded0d0276ce404"
PARENT_ARTIFACTS = {
    "control-plan.json":"f9558bfead121a605f8cc2dd776eed5db6db981c1c20b675d44d49d4b95a502c",
    "measurements.json":"14d37a60a23db8475a0161c70cc7bc3c92e034b7f1329012746ebbd9349c62a1",
    "split-dataset.json":"e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346",
    "trained-models.pt":"809d248f31f56f7c07c2e53637277a3fd0c62edbaa409d6c47e565421cf7d79f",
    "validation-summary.json":"2301115ce19ca0422858054bd29de9b92f2ca2335e7e8e7d586006bb860a61b2",
}
SEEDS, FAMILIES = (234001,234002,234003), ("full","gru_only")
ARMS = ("token_read","eos_adapter")
SPLITS, VIEWS = ("TRAIN","HOLDOUT"), ("normal","evidence_blind","query_blind")
ROWS = {"TRAIN":64,"HOLDOUT":32}
BASE_PARAMS = {"full":13488,"gru_only":10160}
STEPS, BATCH, LR, CLIP, TOL = 400,32,.005,1.,1e-9
OWN = ("fold_lm/v05_benchmarks/model_c248_residual_token_read.py",
    "tests_lm/test_v05_c248_residual_token_read.py","tools/run_c248.ps1","tools/invoke_c248.ps1",
    "docs/experiment-ledger-addendum-c248-preregistration.md","docs/v5b-residual-token-read-v0.1.md")
OUTPUTS = {"readout-plan.json","split-dataset.json","trained-models.pt","measurements.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "bfaafd5c699690553aa072ba74b9707853a2e627b22a6d3d488b646f27047593"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c247_normal_exposure_control as parent
    return parent


def context():
    parent=parent_module()
    _,base,fitting,binding,factory,audit=parent.context()
    return parent,base,fitting,binding,factory,audit


def identities(): return list(itertools.product(SEEDS,FAMILIES,ARMS))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        identities=[list(x) for x in identities()],rows=ROWS,views=list(VIEWS),
        candidate="EOS-query residual read of real post-core tokens; GRU tokens in baseline",
        control="EOS-only bias-free16->24->16 GELU residual MLP",
        added_parameters=768,parameters={k:v+768 for k,v in BASE_PARAMS.items()},
        reader="q=Wq*EOS; alpha=softmax((K*H) dot q /4); residual=Wo*sum(alpha*H); no value projection",
        initialization="fresh common backbone; zero output projection in both arms; head seed=seed+248000",
        prefix_policy="all nonPAD slots including BOS/EOS; no fact parser, entity ID or answer-location oracle",
        core_policy="unchanged actual parent forward; local scoped hooks insert only pre-norm residual",
        steps=STEPS,batch=BATCH,lr=LR,clip=CLIP,optimizer="AdamW",betas=[.9,.999],eps=1e-8,weight_decay=0.,
        row_schedule="C244 alternating old32/added32;200 cycles;no erasure",
        precision="CPU float64",threads=2,deterministic=True,
        train_steps=4800,answer_presentations=153600,model_forward_calls=4980,row_presentations=162816,
        evaluation_forwards=180,checkpoint_writes=1,checkpoint_states=12,
        primary="all token_read Full cells pass original TRAIN+HOLDOUT criteria; controls independent",
        gate=dict(accuracy=.90,fact_pair=.80,query_pair=.80,order_pair=.80,evidence_drop=.35,query_drop=.35),
        comparison="paired reader-minus-EOS-control metrics;equal parameters,not equal FLOPs or architecture",
        source_pins=334,protected_inputs=526,direct_dependencies=24,own_tests=24,
        modules=133,loaded_tests=3122,focused_tests=3121,excluded_test=EXCLUDED,
        replay_tolerance=TOL,network_calls=0,gate_f_candidate=False,production_adoption=False,
        causal_mechanism_claim=False,core_superiority_claim=False,general_language_claim=False)


class ResidualHead(nn.Module):
    def __init__(self,arm,seed):
        super().__init__()
        require(arm in ARMS,"unknown arm")
        self.arm=arm
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(seed+248000)
            if arm=="token_read":
                self.query=nn.Linear(16,16,bias=False,dtype=torch.float64)
                self.key=nn.Linear(16,16,bias=False,dtype=torch.float64)
                self.output=nn.Linear(16,16,bias=False,dtype=torch.float64)
            else:
                self.hidden=nn.Linear(16,24,bias=False,dtype=torch.float64)
                self.output=nn.Linear(24,16,bias=False,dtype=torch.float64)
            nn.init.zeros_(self.output.weight)
        require(sum(p.numel() for p in self.parameters())==768,"head parameter count")

    def forward(self,pooled,states,valid):
        if self.arm=="eos_adapter":
            return pooled+self.output(F.gelu(self.hidden(pooled)))
        require(states is not None and states.shape==(*valid.shape,16)
            and pooled.shape==(valid.shape[0],16) and bool(valid.any(1).all()),"reader shapes")
        q=self.query(pooled)
        scores=(self.key(states)*q.unsqueeze(1)).sum(-1)/4.0
        alpha=scores.masked_fill(~valid,float("-inf")).softmax(-1)
        read=(alpha.unsqueeze(-1)*states).sum(1)
        return pooled+self.output(read)


class ReadoutPilot(nn.Module):
    """Owns a private backbone copy; hooks are per-call and always removed."""
    def __init__(self,backbone,family,arm,seed):
        super().__init__()
        require(family in FAMILIES and arm in ARMS,"model identity")
        self.backbone=backbone
        self.family=family
        self.read=ResidualHead(arm,seed)
        require(sum(p.numel() for p in backbone.parameters())==BASE_PARAMS[family],"backbone capacity")
        require(backbone.config.width==16 and backbone.config.max_tokens==48,"backbone shape")

    def forward(self,tokens,tasks):
        require(tokens.dtype==tasks.dtype==torch.int64 and tokens.ndim==2 and tokens.shape[1]==48
            and tasks.shape==(len(tokens),) and bool((tasks==0).all()),"NEXT-only token/task contract")
        valid=tokens!=256
        eos=valid.sum(1)-1
        require(bool((eos>=1).all()) and bool((tokens[torch.arange(len(tokens)),eos]==258).all()),"EOS contract")
        captured=[];norm_calls=[0];handles=[]
        def capture_gru(module,args,output): captured.append(output[0])
        def capture_core(module,args,kwargs,output):
            if kwargs.get("route_index")==self.backbone.config.next_route: captured.append(output)
        def inject(module,args):
            norm_calls[0]+=1
            states=None
            if self.read.arm=="token_read":
                wanted=self.backbone.config.internal_steps if self.family=="full" else 1
                require(len(captured)==wanted,"actual state capture count")
                states=captured[-1]
                require(states.shape==(len(tokens),48,16)
                    and torch.equal(states[torch.arange(len(tokens)),eos],args[0]),"actual EOS/pool correspondence")
            return (self.read(args[0],states,valid),)
        try:
            if self.read.arm=="token_read":
                if self.family=="full":
                    handles.append(self.backbone.core.register_forward_hook(capture_core,with_kwargs=True))
                else:
                    handles.append(self.backbone.local_encoder.register_forward_hook(capture_gru))
            handles.append(self.backbone.readout_norm.register_forward_pre_hook(inject))
            logits=self.backbone(tokens,tasks)
        finally:
            for handle in handles: handle.remove()
        require(norm_calls[0]==1 and logits.shape==(len(tokens),256)
            and bool(torch.isfinite(logits).all()),"readout invocation/output")
        return logits


def balanced_indices(count,step):
    require(type(count) is int and count==64 and type(step) is int and step>=0,"schedule")
    return torch.arange(32,dtype=torch.int64)+32*(step%2)


def fit(model,train_tokens,train_targets,seed,*,steps=STEPS):
    require(type(steps) is int and steps>0 and len(train_tokens)==train_targets.numel()>0,"training inputs")
    sampler=torch.Generator(device="cpu").manual_seed(seed+1000)
    optimizer=torch.optim.AdamW(model.parameters(),lr=LR,betas=(0.9,0.999),eps=1e-8,weight_decay=0.0)
    model.train(); started=time.perf_counter(); first=last=None
    for step in range(steps):
        ids=balanced_indices(len(train_targets),step)
        optimizer.zero_grad(set_to_none=True)
        logits=model(train_tokens[ids],torch.zeros(BATCH,dtype=torch.int64))
        loss=F.cross_entropy(logits,train_targets[ids]); require(bool(torch.isfinite(loss)),"nonfinite training loss")
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),CLIP,error_if_nonfinite=True)
        optimizer.step(); last=float(loss.detach())
        if first is None:first=last
        if (step+1)%100==0:print(f"[C248] seed={seed} step={step+1}/{steps} answer_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=steps,answer_presentations=steps*BATCH,first_loss=first,last_loss=last,
                fit_seconds=time.perf_counter()-started)


def audit_recipe(base):
    class Labels(ast.NodeTransformer):
        def visit_Constant(self,node):
            if isinstance(node.value,str):node.value=node.value.replace("[C244]","[C248]")
            return node
    require(ast.dump(Labels().visit(ast.parse(inspect.getsource(base.fit))),include_attributes=False)==
        ast.dump(ast.parse(inspect.getsource(fit)),include_attributes=False),"fit AST drift")
    require(all(getattr(base,k)==globals()[k] for k in ("STEPS","BATCH","LR","CLIP","TOL")),"training constants")
    require(all(torch.equal(balanced_indices(64,s),base.balanced_indices(64,s)) for s in range(400)),"row schedule")


def metric_error(actual,expected):
    require(set(actual)==set(expected)=={"en","ja"},"metric languages")
    errors=[]
    for lang in actual:
        require(set(actual[lang])==set(expected[lang]),"metric keys")
        for key,value in actual[lang].items():
            old=expected[lang][key]
            require(math.isfinite(value) and math.isfinite(old),"metric finite")
            errors.append(abs(value-old))
    return max(errors)


def load_inputs(c247_summary):
    parent,base,fitting,_,_,a=context();path=Path(c247_summary).resolve()
    parts=a.read_json(path.parent/"split-dataset.json")
    require(digest(parts)==PARENT_ARTIFACTS["split-dataset.json"] and {s:len(r) for s,r in parts.items()}==ROWS,"partition identity")
    refs=a.read_json(path.parent/"measurements.json")
    require(parent.summarize(refs,fitting)==a.read_json(path)["validation_summary"],"parent summary")
    require([(r["seed"],r["family"]) for r in refs]==list(itertools.product(SEEDS,FAMILIES)),"parent order")
    for r in refs:
        h=r["initial_sha256"]
        require(isinstance(h,str) and len(h)==64 and all(c in "0123456789abcdef" for c in h) and h!=r["final_sha256"],"parent initial identity")
        fitting.validate_metrics(r["initial_train"],64)
        for split in SPLITS:
            m=base.parent_module().discrete_metrics(parts[split],r["predictions"][split])
            require(all(abs(v-r["final"][split][l][k])<=TOL for l,d in m.items() for k,v in d.items()),"parent discrete replay")
    return parts,refs


def train_one(model,parts,ref,arm,*,fitting,binding,factory):
    require(factory.fingerprint(model.backbone)==ref["initial_sha256"],"fresh common backbone")
    before=factory.fingerprint(model);head_before=factory.fingerprint(model.read)
    tokens,targets=binding.tensors(parts["TRAIN"],"normal")
    counts=[0,0];updates=[0];blocks=[0,0]
    def hook(module,args,output):
        counts[0]+=1;counts[1]+=len(args[0])
        if module.training:
            step=updates[0]
            require(step<400 and torch.equal(args[0],tokens[balanced_indices(64,step)]),"actual optimizer tokens")
            updates[0]+=1;blocks[step%2]+=1
    handle=model.register_forward_hook(hook)
    try:
        initial,_=fitting.evaluate(model,parts["TRAIN"],binding,factory.fingerprint)
        initial_error=metric_error(initial,ref["initial_train"])
        require(initial_error<=TOL,"zero residual parent initial metrics")
        trained=fit(model,tokens,targets,ref["seed"])
        final={};raw={}
        for split in SPLITS:final[split],raw[split]=fitting.evaluate(model,parts[split],binding,factory.fingerprint)
    finally:handle.remove()
    after=factory.fingerprint(model)
    require(before!=after and factory.fingerprint(model.read)!=head_before
        and counts==[409,13280] and blocks==[200,200] and updates[0]==400,"training integrity")
    r=dict(seed=ref["seed"],family=ref["family"],arm=arm,backbone_initial_sha256=ref["initial_sha256"],
        initial_sha256=before,final_sha256=after,initial_train=initial,initial_metric_error=initial_error,
        final=final,fit=trained,block_updates=blocks,forward_calls=counts[0],row_presentations=counts[1],
        weights_changed=True,head_weights_changed=True,parameters=sum(p.numel() for p in model.parameters()),
        predictions={s:fitting.prediction_record(raw[s],ROWS[s]) for s in SPLITS})
    return r,{k:v.detach().cpu().clone() for k,v in model.state_dict().items()},raw


def summarize(records,fitting):
    require([(r["seed"],r["family"],r["arm"]) for r in records]==identities(),"record order")
    gates={a:{f:True for f in FAMILIES} for a in ARMS};outcomes={a:Counter() for a in ARMS}
    for r in records:
        require(r["parameters"]==BASE_PARAMS[r["family"]]+768 and r["block_updates"]==[200,200],"capacity/schedule")
        for split in SPLITS:fitting.validate_metrics(r["final"][split],ROWS[split])
        for l in ("en","ja"):
            train=fitting.cell_pass(r["final"]["TRAIN"][l]);held=fitting.cell_pass(r["final"]["HOLDOUT"][l])
            gates[r["arm"]][r["family"]]&=train and held
            outcomes[r["arm"]]["TRAIN_CRITERIA_MISS" if not train else "RECOMBINATION_MISS" if not held else "BOTH_PASS"]+=1
    comparisons=[]
    for i in range(0,len(records),2):
        reader,control=records[i:i+2]
        require(reader["backbone_initial_sha256"]==control["backbone_initial_sha256"],"paired backbone")
        for l in ("en","ja"):
            comparisons.append(dict(seed=reader["seed"],family=reader["family"],language=l,
                reader_accuracy=reader["final"]["HOLDOUT"][l]["accuracy"],
                control_accuracy=control["final"]["HOLDOUT"][l]["accuracy"],
                delta=reader["final"]["HOLDOUT"][l]["accuracy"]-control["final"]["HOLDOUT"][l]["accuracy"]))
    return dict(models=12,gates=gates,cell_outcomes={a:dict(c) for a,c in outcomes.items()},comparisons=comparisons,
        all_replays=all(r["checkpoint_roundtrip"] is True and r["prediction_replayed"] is True and 0<=r["reload_max_error"]<=TOL for r in records),
        all_initial_replays=all(0<=r["initial_metric_error"]<=TOL for r in records),
        all_weights_changed=all(r["weights_changed"] is True and r["head_weights_changed"] is True for r in records),
        train_steps=sum(r["fit"]["steps"] for r in records),answer_presentations=sum(r["fit"]["answer_presentations"] for r in records),
        model_forward_calls=sum(r["forward_calls"] for r in records),row_presentations=sum(r["row_presentations"] for r in records))


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(334,526) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"artifacts")
    s=p["validation_summary"]
    require((s["models"],s["train_steps"],s["answer_presentations"],s["model_forward_calls"],s["row_presentations"]])==(12,4800,153600,4980,162816),"workload")
    require(all(s[k] is True for k in ("all_replays","all_initial_replays","all_weights_changed"))
        and len(s["comparisons"])==12 and all(sum(s["cell_outcomes"][a].values())==12 for a in ARMS),"integrity")
    require(set(s["gates"])==set(ARMS) and all(set(s["gates"][a])==set(FAMILIES) and all(type(v) is bool for v in s["gates"][a].values()) for a in ARMS),"gate schema")
    require(p["status"]==("PASS" if s["gates"]["token_read"]["full"] else "FAIL"),"primary gate")
    require(p["gate_f_candidate"] is False and p["production_adoption"] is False and p["network_calls"]==0,"claim scope")


def precheck(c247_summary,root):
    parent,base,_,_,factory,a=context();root=Path(root);path=Path(c247_summary).resolve()
    require(a.sha(path)==PARENT_SHA,"parent hash");p=a.read_json(path);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL" and p["validation_summary"]["comparison_counts"]==
        {"BOTH_TRAIN_PASS":2,"CONTROL_TRAIN_PASS_ONLY":2,"NEITHER_TRAIN_PASS":8},"accepted control")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items():require(Path(name).is_file() and a.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items():require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    require(str(path) not in protected,"duplicate parent");protected[str(path)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifacts")
    for item in p["artifacts"]:
        child=a.safe_child(path.parent,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"parent bytes")
        require(str(child.resolve()) not in protected,"duplicate artifact");protected[str(child.resolve())]=item["sha256"]
    for name in OWN:
        require(name not in pins,"OWN collision");pins[name]=a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    helpers=("gate_f_c230_prepared_capsule.py","model_c231_byte_eval_contract.py","model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py","model_c234_context_binding.py","model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py","model_c237_frozen_signal_audit.py","model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py","model_c240_saved_position_audit.py","model_c241_assignment_holdout.py",
        "model_c242_balanced_recombination.py","model_c243_saved_recombination_audit.py","model_c244_two_partner_recombination.py",
        "model_c245_selective_evidence.py","model_c246_training_erasure.py","model_c247_normal_exposure_control.py")
    deps=set(factory.LM_SOURCES)|{OWN[0]}|{"fold_lm/v05_benchmarks/"+n for n in helpers}
    require(len(deps)==24 and deps<=set(pins),"direct dependencies")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(334,526) and digest(manifest())==MANIFEST_SHA,"counts/manifest")
    audit_recipe(base)
    return pins,protected


def load_bundle(path):
    value=torch.load(path,map_location="cpu",weights_only=True)
    require(value["schema"]=="fold-c248-residual-read-v1" and value["identities"]==[list(x) for x in identities()]
        and len(value["states"])==12,"bundle identity")
    return value["states"]


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==132,"parent module count")
    return names+["tests_lm.test_v05_c248_residual_token_read"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests];require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"test identities")
    kept=[t for t in tests if t.id()!=EXCLUDED];require((len(tests),len(kept))==(3122,3121),"suite counts")
    return unittest.TestSuite(kept)


def run(*,c247_summary,output_dir,expected_head):
    _,base,fitting,binding,factory,a=context();root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c247_summary,root);parts,refs=load_inputs(c247_summary)
    records=[];states=[];raw=[];out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for seed in SEEDS:
        full=factory.new_model(seed);gru=binding.parent_module().new_baseline(full)
        for family,backbone in (("full",full),("gru_only",gru)):
            ref=refs[list(itertools.product(SEEDS,FAMILIES)).index((seed,family))]
            require(factory.fingerprint(backbone)==ref["initial_sha256"],"source initial identity")
            for arm in ARMS:
                model=ReadoutPilot(copy.deepcopy(backbone),family,arm,seed)
                print(f"[C248] model={len(records)+1}/12 seed={seed} family={family} arm={arm}",flush=True)
                record,state,outputs=train_one(model,parts,ref,arm,fitting=fitting,binding=binding,factory=factory)
                records.append(record);states.append(state);raw.append(outputs)
    torch.save(dict(schema="fold-c248-residual-read-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for r,state,outputs in zip(records,load_bundle(out/"trained-models.pt"),raw,strict=True):
        backbone=factory.new_model(r["seed"])
        if r["family"]=="gru_only":backbone=binding.parent_module().new_baseline(backbone)
        model=ReadoutPilot(backbone,r["family"],r["arm"],r["seed"])
        base.replay_one(model,state,r,outputs,parts,fitting=fitting,binding=binding,factory=factory)
    summary=summarize(records,fitting)
    for name,value in (("readout-plan.json",manifest()),("split-dataset.json",parts),("measurements.json",records),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=n,sha256=a.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard();precheck(c247_summary,root)
    for name,wanted in protected.items():require(a.sha(name)==wanted,"modified input")
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["gates"]["token_read"]["full"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,production_adoption=False,network_calls=0,limitations=[
        "Experimental readout, not adopted production architecture or fact slots.",
        "EOS query summarizes the whole prompt; no explicit object parsing. Attention is not proof of binding.",
        "Capacity matched, not compute matched; no speed, core-superiority or unique-cause claim.",
        "Internal adaptive fixture. A pass does not prove general language or unseen vocabulary."])
    validate_result(p);(out/"summary.json").write_bytes(blob(p));print("=== C248 RESULT ===",flush=True);print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(output_dir,c247_summary,expected_head):
    _,base,fitting,_,_,a=context();out=Path(output_dir);p=a.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():require(a.sha(name)==wanted,"postcheck input")
    for item in p["artifacts"]:
        child=a.safe_child(out,item["file"]);require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"artifact bytes")
    parts,refs=load_inputs(c247_summary);records=a.read_json(out/"measurements.json")
    require(a.read_json(out/"readout-plan.json")==manifest() and a.read_json(out/"split-dataset.json")==parts,"plan/partition")
    require(summarize(records,fitting)==p["validation_summary"]==a.read_json(out/"validation-summary.json"),"summary replay")
    for r in records:
        ref=refs[list(itertools.product(SEEDS,FAMILIES)).index((r["seed"],r["family"]))]
        require(r["backbone_initial_sha256"]==ref["initial_sha256"],"saved common backbone")
        for split in SPLITS:
            m=base.parent_module().discrete_metrics(parts[split],r["predictions"][split])
            require(all(abs(v-r["final"][split][l][k])<=TOL for l,d in m.items() for k,v in d.items()),"saved discrete replay")
    return p,records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for n in ("c247-summary","output-dir"):parser.add_argument("--"+n,type=Path,required=True)
    parser.add_argument("--expected-head",required=True);run(**vars(parser.parse_args()))


if __name__=="__main__":main()
