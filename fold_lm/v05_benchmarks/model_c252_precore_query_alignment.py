"""C252: align the reader query with C251 pre-core memory; keep post-core residual."""
from __future__ import annotations
import argparse
from collections import Counter
from contextlib import redirect_stdout
import copy
import hashlib
import json
import math
from pathlib import Path
import sys
import unittest
import torch
from torch import nn
from fold_lm.v05_benchmarks import model_c248_residual_token_read as reader

EXPERIMENT_ID = "C252-v5b-precore-query-alignment"
STAGE = "V5-B-PRECORE-QUERY-ALIGNMENT"
BASE = "c217a7562c1c396d1a390e8e250083521ef027a5"
PARENT_EXECUTION = "9fb7e7cfec2521815258cf2f0c3b433bcea6419d"
PARENT_SHA = "55038562223ac2bf87db09d2f102d9bd0ca6aacaeaf1381186a836330e26578c"
PARENT_ARTIFACTS = {
    "measurements.json":"c98c5e6bbe313eac35895290d06f002756816918d7341de946941ab70ed0c398",
    "precore-plan.json":"2f72dec74e0fe27e9a9aba129dd1064b34a467363b5a8dc9f5a7a3a2c636fc87",
    "split-dataset.json":"e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346",
    "trained-models.pt":"0fce9c6e666360cf28a3723f870565a7aa1308bfa2a9a524c9a804080dc1e5c1",
    "validation-summary.json":"f4b5128aeb4d730a4227a2c820cdc21874ae269c3ea3c3f669d0202390227da2",
}
SEEDS = (250001,250002,250003,250004,250005)
SPLITS, VIEWS = ("TRAIN","HOLDOUT"), ("normal","evidence_blind","query_blind")
ROWS = {"TRAIN":64,"HOLDOUT":32}
TOL = 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c252_precore_query_alignment.py",
       "tests_lm/test_v05_c252_precore_query_alignment.py","tools/run_c252.ps1","tools/invoke_c252.ps1",
       "docs/experiment-ledger-addendum-c252-preregistration.md","docs/v5b-precore-query-alignment-v0.1.md")
OUTPUTS = {"alignment-plan.json","split-dataset.json","trained-models.pt","measurements.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "f662c4d9c5588bbc0662ae9f578dd59068354a76951bf7192f18f8e53166fd9b"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c251_precore_read as parent
    return parent


def context():
    parent=parent_module()
    base,fitting,binding,factory,audit=parent.context()
    return parent,base,fitting,binding,factory,audit


def identities(): return [(seed,"full","aligned_precore_read") for seed in SEEDS]


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        seeds=list(SEEDS),identities=[list(x) for x in identities()],rows=ROWS,views=list(VIEWS),
        memory="masked pre-core causal encoder states as in C251",
        query="pre-core EOS local encoder state",
        residual="unchanged post-core EOS pooled state plus learned reader output",
        comparator="accepted C251 pre-core-memory/post-core-query endpoints; all five seeds; no retraining",
        initialization="exact C251 bare and full-wrapper initial fingerprints; original head seed+248000",
        backbone_parameters=13488,added_parameters=768,parameters=14256,
        width=16,slots=48,steps=400,batch=32,lr=.005,clip=1.,optimizer="AdamW",
        betas=[.9,.999],eps=1e-8,weight_decay=0.,dtype="CPU float64",threads=2,deterministic=True,
        training="actual unchanged C248 train_one/fit; normal old32/added32 schedule",
        models=5,train_steps=2000,answer_presentations=64000,model_forward_calls=2075,
        row_presentations=67840,evaluation_forwards=75,checkpoint_states=5,
        new_reference_forwards=0,comparator_forwards=0,checkpoint_writes=1,
        gate=dict(accuracy=.90,fact_pair=.80,query_pair=.80,order_pair=.80,evidence_drop=.35,query_drop=.35),
        primary="all five candidate seeds pass both languages and TRAIN/HOLDOUT; comparator separately",
        source_pins=358,protected_inputs=575,direct_dependencies=28,
        own_tests=24,modules=137,loaded_tests=3218,focused_tests=3217,excluded_test=EXCLUDED,
        replay_tolerance=TOL,network_calls=0,production_adoption=False,gate_f_candidate=False,
        causal_mechanism_claim=False,external_validation_claim=False)


class AlignedPrecoreReadout(nn.Module):
    """Pre-core K/V and pre-core query; residual base remains actual post-core EOS."""
    def __init__(self,backbone,seed):
        super().__init__()
        self.backbone=backbone
        self.family="full"
        self.read=reader.ResidualHead("token_read",seed)
        require(sum(p.numel() for p in backbone.parameters())==13488,"Full backbone size")
        require(backbone.config.width==16 and backbone.config.max_tokens==48,"backbone shape")

    def forward(self,tokens,tasks):
        require(tokens.dtype==tasks.dtype==torch.int64 and tokens.ndim==2 and tokens.shape[1]==48
            and tasks.shape==(len(tokens),) and bool((tasks==0).all()),"NEXT token/task contract")
        valid=tokens!=256
        eos=valid.sum(1)-1
        require(bool((eos>=1).all()) and bool((tokens[torch.arange(len(tokens)),eos]==258).all()),"EOS")
        local,next_states,routes,norm_calls,handles=[],[],Counter(),[0],[]
        def capture_local(module,args,output):
            require(output[0].shape==(len(tokens),48,16),"encoder shape")
            local.append(output[0]*valid.unsqueeze(-1).to(dtype=output[0].dtype))
        def capture_core(module,args,kwargs,output):
            route=kwargs.get("route_index")
            require(len(local)==1 and len(args)==2 and torch.equal(args[1],local[0]),"actual pre-core context")
            routes[route]+=1
            if route==self.backbone.config.next_route: next_states.append(output)
        def inject(module,args):
            norm_calls[0]+=1
            cfg=self.backbone.config
            require(routes=={cfg.next_route:cfg.internal_steps,cfg.instruction_route:cfg.internal_steps},"core path counts")
            post=args[0]
            require(len(next_states)==cfg.internal_steps and
                torch.equal(next_states[-1][torch.arange(len(tokens)),eos],post),"post-core residual provenance")
            pre_query=local[0][torch.arange(len(tokens)),eos]
            q=self.read.query(pre_query)
            scores=(self.read.key(local[0])*q.unsqueeze(1)).sum(-1)/4.0
            alpha=scores.masked_fill(~valid,float("-inf")).softmax(-1)
            memory=(alpha.unsqueeze(-1)*local[0]).sum(1)
            return (post+self.read.output(memory),)
        try:
            handles.append(self.backbone.local_encoder.register_forward_hook(capture_local))
            handles.append(self.backbone.core.register_forward_hook(capture_core,with_kwargs=True))
            handles.append(self.backbone.readout_norm.register_forward_pre_hook(inject))
            logits=self.backbone(tokens,tasks)
        finally:
            for handle in handles: handle.remove()
        require(norm_calls[0]==1 and logits.shape==(len(tokens),256) and bool(torch.isfinite(logits).all()),"output")
        return logits


class Progress:
    def __init__(self,stream): self.stream=stream
    def write(self,text): return self.stream.write(text.replace("[C248]","[C252]"))
    def flush(self): return self.stream.flush()


def load_inputs(c251_summary):
    parent,base,fitting,_,_,a=context();path=Path(c251_summary).resolve()
    require(a.sha(path)==PARENT_SHA,"parent summary identity")
    p=a.read_json(path);parent.validate_result(p)
    parts=a.read_json(path.parent/"split-dataset.json")
    require(digest(parts)==PARENT_ARTIFACTS["split-dataset.json"] and {k:len(v) for k,v in parts.items()}==ROWS,"split")
    comps=a.read_json(path.parent/"measurements.json")
    require(parent.summarize(comps,fitting)==p["validation_summary"],"parent summary replay")
    require([(r["seed"],r["family"],r["arm"]) for r in comps]==[(s,"full","precore_read") for s in SEEDS],"parent identities")
    for r in comps:
        for split in SPLITS:
            measured=base.parent_module().discrete_metrics(parts[split],r["predictions"][split])
            require(all(abs(v-r["final"][split][lang][k])<=TOL for lang,m in measured.items() for k,v in m.items()),"parent discrete replay")
    refs=[dict(seed=r["seed"],family="full",initial_sha256=r["backbone_initial_sha256"],initial_train=copy.deepcopy(r["initial_train"])) for r in comps]
    for ref,comp in zip(refs,comps,strict=True):
        require(ref["initial_sha256"]==comp["backbone_initial_sha256"] and
            reader.metric_error(ref["initial_train"],comp["initial_train"])<=TOL,"parent initial semantics")
    return parts,refs,comps


def summarize(records,fitting):
    require([(r["seed"],r["family"],r["arm"]) for r in records]==identities(),"candidate identities")
    cells=[];seed_results=[];comparator_results=[]
    for r in records:
        require(r["parameters"]==14256 and r["block_updates"]==[200,200],"capacity/schedule")
        require((r["fit"]["steps"],r["fit"]["answer_presentations"],r["forward_calls"],r["row_presentations"])==(400,12800,415,13568),"per-model counts")
        require(all(r[k] is True for k in ("weights_changed","head_weights_changed","checkpoint_roundtrip","prediction_replayed")),"integrity flags")
        for k in ("initial_metric_error","reload_max_error"):
            require(type(r[k]) in (int,float) and math.isfinite(r[k]) and 0<=r[k]<=TOL,"replay error")
        require(r["initial_sha256"]==r["c251_initial_sha256"],"matched complete initial weights")
        for field in ("final","c251_comparator"):
            require(set(r[field])==set(SPLITS),"metric split keys")
            for split in SPLITS: fitting.validate_metrics(r[field][split],ROWS[split])
        passed=True;oldpassed=True
        for lang in ("en","ja"):
            train=fitting.cell_pass(r["final"]["TRAIN"][lang]);held=fitting.cell_pass(r["final"]["HOLDOUT"][lang])
            old=all(fitting.cell_pass(r["c251_comparator"][s][lang]) for s in SPLITS)
            acc=r["final"]["HOLDOUT"][lang]["accuracy"];prior=r["c251_comparator"]["HOLDOUT"][lang]["accuracy"]
            cells.append(dict(seed=r["seed"],language=lang,train_pass=train,holdout_pass=held,
                comparator_joint_pass=old,outcome="TRAIN_CRITERIA_MISS" if not train else "RECOMBINATION_MISS" if not held else "BOTH_PASS",
                candidate_accuracy=acc,comparator_accuracy=prior,delta=acc-prior))
            passed &= train and held;oldpassed &= old
        seed_results.append(dict(seed=r["seed"],both_languages_pass=passed));comparator_results.append(oldpassed)
    return dict(models=5,candidate_gate=all(x["both_languages_pass"] for x in seed_results),
        seed_results=seed_results,seed_pass_count=sum(x["both_languages_pass"] for x in seed_results),
        comparator_seed_pass_count=sum(comparator_results),cells=cells,cell_outcomes=dict(Counter(c["outcome"] for c in cells)),
        train_steps=2000,answer_presentations=64000,model_forward_calls=2075,row_presentations=67840,
        all_replays=True,all_initial_replays=True,all_weights_changed=True)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(358,575) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"artifact coverage")
    s=p["validation_summary"]
    require(tuple(s[k] for k in ("models","train_steps","answer_presentations","model_forward_calls","row_presentations"))==(5,2000,64000,2075,67840),"workload")
    require(len(s["cells"])==10 and len(s["seed_results"])==5 and sum(s["cell_outcomes"].values())==10,"cell counts")
    require(type(s["candidate_gate"]) is bool and p["status"]==("PASS" if s["candidate_gate"] else "FAIL"),"primary status")
    require(all(s[k] is True for k in ("all_replays","all_initial_replays","all_weights_changed")) and
        p["production_adoption"] is False and p["gate_f_candidate"] is False and p["network_calls"]==0,"integrity/scope")


def precheck(c251_summary,root):
    parent,base,_,_,factory,a=context();path,root=Path(c251_summary).resolve(),Path(root)
    require(a.sha(path)==PARENT_SHA,"parent hash");p=a.read_json(path);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL" and
        p["validation_summary"]["seed_pass_count"]==2 and p["validation_summary"]["comparator_seed_pass_count"]==2 and
        p["validation_summary"]["cell_outcomes"]=={"BOTH_PASS":4,"RECOMBINATION_MISS":6},"accepted parent")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items(): require(Path(name).is_file() and a.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items(): require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    require(str(path) not in protected,"parent duplicate");protected[str(path)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifact identities")
    for item in p["artifacts"]:
        child=a.safe_child(path.parent,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"parent artifact bytes")
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
        "model_c251_precore_read.py")
    deps=set(factory.LM_SOURCES)|{OWN[0]}|{"fold_lm/v05_benchmarks/"+n for n in helpers}
    require(len(deps)==28 and deps<=set(pins),"direct dependencies")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(358,575) and digest(manifest())==MANIFEST_SHA,"counts/manifest")
    reader.audit_recipe(base)
    return pins,protected


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(v["schema"]=="fold-c252-precore-query-v1" and v["identities"]==[list(x) for x in identities()] and len(v["states"])==5,"bundle identity")
    return v["states"]


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==136,"parent module count")
    return names+["tests_lm.test_v05_c252_precore_query_alignment"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite): yield from flatten(item)
        else: yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests];require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"suite IDs")
    kept=[t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(3218,3217),"suite counts")
    return unittest.TestSuite(kept)


def run(*,c251_summary,output_dir,expected_head):
    _,base,fitting,binding,factory,a=context();root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c251_summary,root);parts,refs,comparators=load_inputs(c251_summary)
    records=[];states=[];raw=[];out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for ref,comp in zip(refs,comparators,strict=True):
        model=AlignedPrecoreReadout(factory.new_model(ref["seed"]),ref["seed"])
        require(factory.fingerprint(model)==comp["initial_sha256"],"exact C251 wrapper initial state")
        print(f'[C252] model={len(records)+1}/5 seed={ref["seed"]}; pre-core memory + pre-core query / post-core residual',flush=True)
        with redirect_stdout(Progress(sys.stdout)):
            record,state,outputs=reader.train_one(model,parts,ref,"token_read",fitting=fitting,binding=binding,factory=factory)
        record.update(arm="aligned_precore_read",c251_initial_sha256=comp["initial_sha256"],c251_comparator=copy.deepcopy(comp["final"]))
        records.append(record);states.append(state);raw.append(outputs)
    torch.save(dict(schema="fold-c252-precore-query-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for r,state,outputs in zip(records,load_bundle(out/"trained-models.pt"),raw,strict=True):
        model=AlignedPrecoreReadout(factory.new_model(r["seed"]),r["seed"])
        base.replay_one(model,state,r,outputs,parts,fitting=fitting,binding=binding,factory=factory)
    summary=summarize(records,fitting)
    for name,value in (("alignment-plan.json",manifest()),("split-dataset.json",parts),("measurements.json",records),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=n,sha256=a.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard();precheck(c251_summary,root)
    for name,wanted in protected.items(): require(a.sha(name)==wanted,"modified input")
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        production_adoption=False,gate_f_candidate=False,network_calls=0)
    validate_result(p);(out/"summary.json").write_bytes(blob(p));print("=== C252 RESULT ===",flush=True);print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(output_dir,c251_summary,expected_head):
    _,base,fitting,_,_,a=context();out=Path(output_dir);p=a.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items(): require(a.sha(name)==wanted,"postcheck input")
    for item in p["artifacts"]:
        child=a.safe_child(out,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"artifact bytes")
    parts,refs,comps=load_inputs(c251_summary);records=a.read_json(out/"measurements.json")
    require(a.read_json(out/"alignment-plan.json")==manifest() and a.read_json(out/"split-dataset.json")==parts,"plan/partition")
    require(summarize(records,fitting)==p["validation_summary"]==a.read_json(out/"validation-summary.json"),"summary replay")
    for r,ref,comp in zip(records,refs,comps,strict=True):
        require(r["backbone_initial_sha256"]==ref["initial_sha256"] and r["initial_sha256"]==comp["initial_sha256"]
            and r["c251_comparator"]==comp["final"],"comparator/initial identity")
        for split in SPLITS:
            measured=base.parent_module().discrete_metrics(parts[split],r["predictions"][split])
            require(all(abs(v-r["final"][split][lang][k])<=TOL for lang,m in measured.items() for k,v in m.items()),"child discrete replay")
    return p,records


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("c251-summary","output-dir"): p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))


if __name__=="__main__": main()
