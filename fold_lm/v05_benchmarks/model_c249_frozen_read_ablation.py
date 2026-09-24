"""C249: frozen inference ablations, not retraining or a new capability gate."""
from __future__ import annotations
import argparse
from collections import defaultdict
from contextlib import contextmanager
import hashlib
import itertools
import json
import math
from pathlib import Path
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C249-v5b-frozen-read-path-ablation"
STAGE = "V5-B-FROZEN-READ-PATH-ABLATION"
BASE = "812d8a0452962c569303bade157aa802de20ea65"
PARENT_EXECUTION = "23bcc949638ea3e927ec0bb3d846b9f42b552a56"
PARENT_SHA = "99778defedd9854815f94989567687c64930e3b505449a847dd030be5a47dab6"
PARENT_ARTIFACTS = {
    "measurements.json":"d2c7f99d79e6ac2ddc47e5d5d900ccaea4479b2325c0d0b35e7a9f05f587e382",
    "readout-plan.json":"bfaafd5c699690553aa072ba74b9707853a2e627b22a6d3d488b646f27047593",
    "split-dataset.json":"e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346",
    "trained-models.pt":"35e39b16f5a30f9a55d7718427294d4bba6255772ad7fdf183ea0275e310cdc3",
    "validation-summary.json":"7130fbc17973ea9189313c60df880ea5b9593c1e1e0871f5ddeb08898c0e0dff",
}
SEEDS, FAMILIES, ARMS = (234001,234002,234003), ("full","gru_only"), ("token_read","eos_adapter")
SPLITS, VIEWS = ("TRAIN","HOLDOUT"), ("normal","evidence_blind","query_blind")
ROWS = {"TRAIN":64,"HOLDOUT":32}
TOL = 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c249_frozen_read_ablation.py",
    "tests_lm/test_v05_c249_frozen_read_ablation.py","tools/run_c249.ps1","tools/invoke_c249.ps1",
    "docs/experiment-ledger-addendum-c249-preregistration.md","docs/v5b-frozen-read-ablation-v0.1.md")
OUTPUTS = {"ablation-plan.json","logits.json","diagnostics.json","contrasts.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "9fd82672124ff0227174d7a9df894c67ca9f1958a36fad6cbc575e1179dfa414"


def require(ok, message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c248_residual_token_read as parent
    return parent


def context():
    parent=parent_module()
    _,base,fitting,binding,factory,audit=parent.context()
    return parent,base,fitting,binding,factory,audit


def identities(): return list(itertools.product(SEEDS,FAMILIES,ARMS))


def modes(arm):
    require(arm in ARMS,"arm")
    return ("residual_off","uniform_read") if arm=="token_read" else ("residual_off",)


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        identities=[list(x) for x in identities()],rows=ROWS,views=list(VIEWS),
        modes={a:list(modes(a)) for a in ARMS},
        off="return original pooled h instead of the learned head output",
        uniform="h+Wo*mean(H at nonPAD positions); keep trained states and output matrix",
        evaluation="intact all3 views/both splits; off normal; reader uniform normal; restore intact all3 views",
        weights="all12 accepted final states frozen; no seed/cell selection",dtype="CPU float64",threads=2,
        deterministic=True,model_forward_calls=180,row_presentations=8640,
        stored_logit_rows=5184,normal_contrast_cells=72,checkpoint_states_loaded=12,
        new_training_steps=0,checkpoint_writes=0,network_calls=0,
        source_pins=340,protected_inputs=538,direct_dependencies=25,
        own_tests=24,modules=134,loaded_tests=3146,focused_tests=3145,excluded_test=EXCLUDED,
        replay_tolerance=TOL,primary="diagnostic integrity independent of performance changes",
        original_capability_gate_unchanged=True,production_adoption=False,gate_f_candidate=False,
        causal_mechanism_claim=False,general_language_claim=False)


def finite_logits(x,n):
    require(isinstance(x,torch.Tensor) and x.shape==(n,256) and x.dtype==torch.float64
        and x.device.type=="cpu" and bool(torch.isfinite(x).all()),"logit shape/dtype/finite")
    return x


def normal_metrics(rows,logits):
    finite_logits(logits,len(rows));pred=logits.argmax(-1).tolist()
    loss=F.cross_entropy(logits,torch.tensor([r["target"] for r in rows]),reduction="none")
    out={}
    for lang in ("en","ja"):
        ids=[i for i,r in enumerate(rows) if r["language"]==lang]
        require(len(ids)==len(rows)//2 and len(ids)>0,"language coverage")
        m=dict(rows=len(ids),accuracy=sum(pred[i]==rows[i]["target"] for i in ids)/len(ids),
            answer_nll=float(loss[ids].mean()))
        for kind in ("fact","query","order"):
            groups=defaultdict(list)
            for i in ids:
                r=rows[i]
                key=(tuple(r["objects"]),tuple(sorted(r["values"])),r["order"],r["query"]) if kind=="fact" else (r["group"],r["order"] if kind=="query" else r["query"])
                groups[key].append(i)
            require(len(groups)==len(ids)//2 and all(len(g)==2 for g in groups.values()),"pair coverage")
            require(all((rows[g[0]]["target"]==rows[g[1]]["target"])==(kind=="order") for g in groups.values()),"pair targets")
            m[kind+"_pair_accuracy"]=sum(all(pred[i]==rows[i]["target"] for i in g) for g in groups.values())/len(groups)
        out[lang]=m
    return out


def original_metrics(rows,outputs):
    require(set(outputs)==set(VIEWS),"original views")
    m=normal_metrics(rows,outputs["normal"])
    for key in VIEWS[1:]:
        finite_logits(outputs[key],len(rows));pred=outputs[key].argmax(-1).tolist()
        for lang in m:
            ids=[i for i,r in enumerate(rows) if r["language"]==lang]
            accuracy=sum(pred[i]==rows[i]["target"] for i in ids)/len(ids)
            m[lang][key+"_accuracy"]=accuracy
            m[lang][key.replace("_blind", "_drop")]=m[lang]["accuracy"]-accuracy
    return m


def metric_error(actual,expected):
    require(set(actual)==set(expected)=={"en","ja"},"metric languages")
    errors=[]
    for lang in actual:
        require(set(actual[lang])==set(expected[lang]),"metric keys")
        for key,value in actual[lang].items():
            other=expected[lang][key]
            require(type(value) in (int,float) and type(other) in (int,float)
                and math.isfinite(value) and math.isfinite(other),"metric finite/type")
            errors.append(abs(value-other))
    return max(errors)


@contextmanager
def intervention(head,mode):
    require(mode in modes(head.arm),"unsupported intervention")
    count=[0]
    def replace(module,args,output):
        count[0]+=1
        pooled,states,valid=args
        if mode=="residual_off": return pooled
        require(states is not None and states.shape==(*valid.shape,16) and valid.dtype==torch.bool
            and bool(valid.any(1).all()),"uniform input contract")
        mean=states.masked_fill(~valid.unsqueeze(-1),0).sum(1)/valid.sum(1,keepdim=True)
        return pooled+module.output(mean)
    handle=head.register_forward_hook(replace)
    try: yield count
    finally: handle.remove()


def contrasts(rows,intact,changed):
    old=normal_metrics(rows,intact);new=normal_metrics(rows,changed)
    a=intact.argmax(-1).tolist();c=changed.argmax(-1).tolist();out={}
    for lang in old:
        ids=[i for i,r in enumerate(rows) if r["language"]==lang]
        out[lang]=dict(rows=len(ids),intact=old[lang],ablated=new[lang],
            accuracy_drop=old[lang]["accuracy"]-new[lang]["accuracy"],
            nll_change=new[lang]["answer_nll"]-old[lang]["answer_nll"],
            answer_flips=sum(a[i]!=c[i] for i in ids),
            lost_correct=sum(a[i]==rows[i]["target"] and c[i]!=rows[i]["target"] for i in ids),
            gained_correct=sum(a[i]!=rows[i]["target"] and c[i]==rows[i]["target"] for i in ids),
            max_logit_change=float((intact[ids]-changed[ids]).abs().max()))
    return out


def check_frozen(model,fingerprint,wanted):
    require(fingerprint(model)==wanted and not model.training
        and all(not p.requires_grad and p.grad is None for p in model.parameters()),"frozen state changed")


def audit_model(model,parts,ref,*,binding,factory):
    wanted=ref["final_sha256"];check_frozen(model,factory.fingerprint,wanted)
    counts=[0,0]
    def count(module,args,output):counts[0]+=1;counts[1]+=len(args[0])
    handle=model.register_forward_hook(count)
    views={s:{v:binding.tensors(parts[s],v) for v in VIEWS} for s in SPLITS}
    saved_tokens={(s,v):x[0].clone() for s,d in views.items() for v,x in d.items()}
    def forward(split,view):
        tokens,_=views[split][view]
        with torch.no_grad():x=model(tokens,torch.zeros(len(tokens),dtype=torch.int64))
        return finite_logits(x,len(tokens)).detach().clone()
    raw={"intact":{}};parent_error=0.;restore_error=0.;hook_calls={}
    try:
        for s in SPLITS:
            raw["intact"][s]={v:forward(s,v) for v in VIEWS}
            metrics=original_metrics(parts[s],raw["intact"][s])
            parent_error=max(parent_error,metric_error(metrics,ref["final"][s]))
            require({v:x.argmax(-1).tolist() for v,x in raw["intact"][s].items()}==ref["predictions"][s],"parent prediction replay")
        require(parent_error<=TOL,"parent metric replay")
        for mode in modes(ref["arm"]):
            with intervention(model.read,mode) as calls:
                raw[mode]={s:{"normal":forward(s,"normal")} for s in SPLITS}
            require(calls[0]==2,"intervention calls");hook_calls[mode]=calls[0]
            check_frozen(model,factory.fingerprint,wanted)
        for s in SPLITS:
            restored={v:forward(s,v) for v in VIEWS}
            restore_error=max(restore_error,*(float((restored[v]-raw["intact"][s][v]).abs().max()) for v in VIEWS))
            require(all(torch.equal(restored[v].argmax(-1),raw["intact"][s][v].argmax(-1)) for v in VIEWS),"restored predictions")
        require(restore_error<=TOL,"restored logits")
    finally:handle.remove()
    require(all(torch.equal(views[s][v][0],x) for (s,v),x in saved_tokens.items()),"input mutation")
    check_frozen(model,factory.fingerprint,wanted)
    require(all(not m._forward_hooks and not m._forward_pre_hooks for m in model.modules()),"hook leak")
    expected=[16,768] if ref["arm"]=="token_read" else [14,672]
    require(counts==expected,"model workload")
    changes={mode:{s:contrasts(parts[s],raw["intact"][s]["normal"],raw[mode][s]["normal"]) for s in SPLITS} for mode in modes(ref["arm"])}
    report=dict(seed=ref["seed"],family=ref["family"],arm=ref["arm"],before_sha256=wanted,
        after_sha256=factory.fingerprint(model),parent_metric_error=parent_error,restored_max_error=restore_error,
        parent_predictions_equal=True,restored_predictions_equal=True,forward_calls=counts[0],
        row_presentations=counts[1],intervention_calls=hook_calls)
    return report,raw,changes


def summarize(records):
    require([(r["seed"],r["family"],r["arm"]) for r in records]==identities(),"report identity order")
    for r in records:
        require(r["before_sha256"]==r["after_sha256"] and r["parent_predictions_equal"] is True
            and r["restored_predictions_equal"] is True,"replay/fingerprint")
        require(all(type(r[k]) in (int,float) and math.isfinite(r[k]) and 0<=r[k]<=TOL
            for k in ("parent_metric_error","restored_max_error")),"replay error")
        require(r["intervention_calls"]=={m:2 for m in modes(r["arm"])},"intervention workload")
        require((r["forward_calls"],r["row_presentations"])==((16,768) if r["arm"]=="token_read" else (14,672)),"individual workload")
    return dict(models=12,model_forward_calls=sum(r["forward_calls"] for r in records),
        row_presentations=sum(r["row_presentations"] for r in records),stored_logit_rows=5184,
        normal_contrast_cells=72,all_parent_replays=True,all_restoration_replays=True,all_weights_unchanged=True,
        new_training_steps=0,checkpoint_writes=0,capability_pass_claim=False,causal_mechanism_claim=False)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS"
        and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(340,538) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"artifacts")
    s=p["validation_summary"]
    require(tuple(s[k] for k in ("models","model_forward_calls","row_presentations","stored_logit_rows","normal_contrast_cells","new_training_steps","checkpoint_writes"))==(12,180,8640,5184,72,0,0),"workload")
    require(all(s[k] is True for k in ("all_parent_replays","all_restoration_replays","all_weights_unchanged"))
        and s["capability_pass_claim"] is False and s["causal_mechanism_claim"] is False
        and p["production_adoption"] is False and p["gate_f_candidate"] is False and p["network_calls"]==0,"scope/integrity")


def precheck(c248_summary,root):
    parent,_,_,_,factory,a=context();root=Path(root);path=Path(c248_summary).resolve()
    require(a.sha(path)==PARENT_SHA,"parent summary hash");p=a.read_json(path);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL" and p["validation_summary"]["cell_outcomes"]==
        {"token_read":{"BOTH_PASS":8,"RECOMBINATION_MISS":4},"eos_adapter":{"RECOMBINATION_MISS":12}},"accepted parent")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items():require(Path(name).is_file() and a.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items():require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    require(str(path) not in protected,"duplicate parent");protected[str(path)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifact contract")
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
        "model_c245_selective_evidence.py","model_c246_training_erasure.py","model_c247_normal_exposure_control.py","model_c248_residual_token_read.py")
    deps=set(factory.LM_SOURCES)|{OWN[0]}|{"fold_lm/v05_benchmarks/"+n for n in helpers}
    require(len(deps)==25 and deps<=set(pins),"direct dependencies")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(340,538) and digest(manifest())==MANIFEST_SHA,"count/manifest")
    return pins,protected


def load_inputs(c248_summary):
    parent,_,fitting,_,_,a=context();path=Path(c248_summary).resolve()
    parts=a.read_json(path.parent/"split-dataset.json")
    require(set(parts)==set(SPLITS) and digest(parts)==PARENT_ARTIFACTS["split-dataset.json"]
        and {s:len(v) for s,v in parts.items()}==ROWS,"partition")
    refs=a.read_json(path.parent/"measurements.json")
    require(parent.summarize(refs,fitting)==a.read_json(path)["validation_summary"],"parent measurement summary")
    require([(r["seed"],r["family"],r["arm"]) for r in refs]==identities(),"parent identities")
    for r in refs:
        h=r["final_sha256"]
        require(isinstance(h,str) and len(h)==64 and all(c in "0123456789abcdef" for c in h),"final fingerprint")
        require(set(r["final"])==set(r["predictions"])==set(SPLITS),"parent split schema")
        for s in SPLITS:
            fitting.validate_metrics(r["final"][s],ROWS[s]);pred=r["predictions"][s]
            require(set(pred)==set(VIEWS) and all(len(v)==ROWS[s] and all(type(x) is int and 0<=x<256 for x in v) for v in pred.values()),"parent predictions")
    return parts,refs


def make_model(ref,state,parent,binding,factory):
    backbone=factory.new_model(ref["seed"])
    if ref["family"]=="gru_only":backbone=binding.parent_module().new_baseline(backbone)
    model=parent.ReadoutPilot(backbone,ref["family"],ref["arm"],ref["seed"])
    model.load_state_dict(state,strict=True);model.eval();model.requires_grad_(False)
    check_frozen(model,factory.fingerprint,ref["final_sha256"])
    return model


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==133,"parent modules")
    return names+["tests_lm.test_v05_c249_frozen_read_ablation"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests];require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"test identities")
    kept=[t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(3146,3145),"suite counts")
    return unittest.TestSuite(kept)


def run(*,c248_summary,output_dir,expected_head):
    parent,_,_,binding,factory,a=context();root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c248_summary,root);parts,refs=load_inputs(c248_summary)
    states=parent.load_bundle(Path(c248_summary).resolve().parent/"trained-models.pt")
    records=[];logits=[];effects=[]
    for i,(ref,state) in enumerate(zip(refs,states,strict=True),1):
        print(f'[C249] model={i}/12 seed={ref["seed"]} family={ref["family"]} arm={ref["arm"]}; frozen ablate/restore',flush=True)
        model=make_model(ref,state,parent,binding,factory)
        record,raw,changes=audit_model(model,parts,ref,binding=binding,factory=factory)
        records.append(record)
        identity={k:ref[k] for k in ("seed","family","arm")}
        logits.append(dict(**identity,outputs={m:{s:{v:x.tolist() for v,x in data.items()} for s,data in d.items()} for m,d in raw.items()}))
        effects.append(dict(**identity,contrasts=changes))
    summary=summarize(records);out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for name,value in (("ablation-plan.json",manifest()),("logits.json",logits),("diagnostics.json",records),("contrasts.json",effects),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=n,sha256=a.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard();precheck(c248_summary,root)
    for name,wanted in protected.items():require(a.sha(name)==wanted,"modified input")
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        production_adoption=False,gate_f_candidate=False,network_calls=0)
    validate_result(p);(out/"summary.json").write_bytes(blob(p));print("=== C249 RESULT ===",flush=True);print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(output_dir,c248_summary,expected_head):
    torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    _,_,_,_,_,a=context();out=Path(output_dir);p=a.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():require(a.sha(name)==wanted,"postcheck input")
    for item in p["artifacts"]:
        child=a.safe_child(out,item["file"]);require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"artifact bytes")
    records=a.read_json(out/"diagnostics.json");parts,refs=load_inputs(c248_summary)
    require(summarize(records)==p["validation_summary"]==a.read_json(out/"validation-summary.json"),"summary replay")
    require(a.read_json(out/"ablation-plan.json")==manifest(),"saved plan")
    stored=a.read_json(out/"logits.json");effects=a.read_json(out/"contrasts.json");rows=0;cells=0
    for seq in (stored,effects):require([(r["seed"],r["family"],r["arm"]) for r in seq]==identities(),"artifact identities")
    for rec,saved,effect,ref in zip(records,stored,effects,refs,strict=True):
        require(rec["before_sha256"]==rec["after_sha256"]==ref["final_sha256"],"saved final identity")
        raw=saved["outputs"];require(set(raw)=={"intact",*modes(ref["arm"])},"saved modes")
        tensors={}
        for mode,data in raw.items():
            require(set(data)==set(SPLITS),"saved splits");tensors[mode]={}
            for s,d in data.items():
                require(set(d)==(set(VIEWS) if mode=="intact" else {"normal"}),"saved view schema")
                tensors[mode][s]={v:finite_logits(torch.tensor(x,dtype=torch.float64),ROWS[s]) for v,x in d.items()}
                rows+=sum(len(x) for x in tensors[mode][s].values())
        for s in SPLITS:
            require(metric_error(original_metrics(parts[s],tensors["intact"][s]),ref["final"][s])<=TOL,"persisted parent metrics")
            require({v:x.argmax(-1).tolist() for v,x in tensors["intact"][s].items()}==ref["predictions"][s],"persisted parent predictions")
        changes={m:{s:contrasts(parts[s],tensors["intact"][s]["normal"],tensors[m][s]["normal"]) for s in SPLITS} for m in modes(ref["arm"])}
        require(changes==effect["contrasts"],"persisted contrasts");cells+=sum(len(x) for c in changes.values() for x in c.values())
    require((rows,cells)==(5184,72),"persisted workload")
    return p,effects


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("c248-summary","output-dir"):parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True);run(**vars(parser.parse_args()))


if __name__=="__main__":main()
