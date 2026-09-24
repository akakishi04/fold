"""C250: prospective paired initialization replication of the unchanged C248 recipe."""
from __future__ import annotations
import argparse
from collections import Counter
from contextlib import redirect_stdout
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
import unittest
import torch

EXPERIMENT_ID = "C250-v5b-fresh-seed-readout-replication"
STAGE = "V5-B-FRESH-SEED-READOUT-REPLICATION"
BASE = "4410c888f658621e7bbd5a8f655add32aa51dfa3"
PARENT_EXECUTION = "9d28b7420e69efe57555b7db2ccbb0eec6f3d302"
PARENT_SHA = "3b95e6ca6b7ba645e13367a483f55fd75a9e112f3f928b2e1cdaf69913be0500"
PARENT_ARTIFACTS = {
    "ablation-plan.json":"9fd82672124ff0227174d7a9df894c67ca9f1958a36fad6cbc575e1179dfa414",
    "contrasts.json":"c7bf603849b29a55a0fa7b7e4843b909df4fab7a41ab1081c4f77125b0438e22",
    "diagnostics.json":"2e849c3d6fda7bae1b9b89325f7515f51e18886e679914a32a470234fa9d6310",
    "logits.json":"c28e79ac452bfbc49a4904582abdc233db211ec703f1b8340f0756f389f792d0",
    "validation-summary.json":"7613f8266a32e67e683a3b0c86aac47437b18a4b677e808a4d5a0ef5442a7aed",
}
C248_SHA = "99778defedd9854815f94989567687c64930e3b505449a847dd030be5a47dab6"
SPLIT_SHA = "e6b19547f95d319ead4be43086f5de76f16b4b6ab6cd9bec2ed4da5f8df80346"
SEEDS = (250001,250002,250003,250004,250005)
FAMILIES, ARMS = ("full","gru_only"), ("token_read","eos_adapter")
SPLITS, VIEWS = ("TRAIN","HOLDOUT"), ("normal","evidence_blind","query_blind")
ROWS = {"TRAIN":64,"HOLDOUT":32}
BASE_PARAMS = {"full":13488,"gru_only":10160}
TOL = 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c250_fresh_seed_replication.py",
    "tests_lm/test_v05_c250_fresh_seed_replication.py","tools/run_c250.ps1","tools/invoke_c250.ps1",
    "docs/experiment-ledger-addendum-c250-preregistration.md","docs/v5b-fresh-seed-replication-v0.1.md")
OUTPUTS = {"replication-plan.json","split-dataset.json","initial-references.json",
    "trained-models.pt","measurements.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "4f2bffab4fff98193a2756fe65d0403d955711f23b18e548698f45d7f93c9cee"


def require(ok,message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c249_frozen_read_ablation as parent
    return parent


def context():
    parent=parent_module()
    reader,base,fitting,binding,factory,audit=parent.context()
    return parent,reader,base,fitting,binding,factory,audit


def identities(): return list(itertools.product(SEEDS,FAMILIES,ARMS))


def reference_identities(): return list(itertools.product(SEEDS,FAMILIES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        c248_summary_sha256=C248_SHA,split_sha256=SPLIT_SHA,seeds=list(SEEDS),identities=[list(x) for x in identities()],
        rows=ROWS,views=list(VIEWS),recipe="actual unchanged C248 ReadoutPilot/train_one/fit and C244 replay",
        head_seed_rule="seed+248000 unchanged; linked to backbone seed",added_parameters=768,
        parameters={f:n+768 for f,n in BASE_PARAMS.items()},steps_per_model=400,batch_size=32,
        lr=.005,clip=1.,optimizer="AdamW",betas=[.9,.999],eps=1e-8,weight_decay=0.,
        row_schedule="old32/added32 alternating200 cycles; normal inputs only",dtype="CPU float64",threads=2,deterministic=True,
        primary="every new Full/token_read seed passes original TRAIN and HOLDOUT criteria in both languages",
        gate=dict(accuracy=.90,fact_pair=.80,query_pair=.80,order_pair=.80,evidence_drop=.35,query_drop=.35),
        models=20,train_steps=8000,answer_presentations=256000,model_forward_calls=8330,row_presentations=273280,
        reference_models=10,reference_forwards=30,reference_rows=1920,reference_split="TRAIN only before fitting",
        reference_policy="fresh backbone evaluated once; copied unchanged to both arms; no historical initial metrics",
        evaluation_forwards=330,checkpoint_writes=1,checkpoint_states=20,source_pins=346,protected_inputs=550,
        direct_dependencies=26,own_tests=24,modules=135,loaded_tests=3170,focused_tests=3169,excluded_test=EXCLUDED,
        replay_tolerance=TOL,network_calls=0,production_adoption=False,gate_f_candidate=False,
        no_seed_replacement=True,external_test_claim=False,core_superiority_claim=False)


class Progress:
    """Relabel inherited console progress only; no scientific code is patched."""
    def __init__(self,stream): self.stream=stream
    def write(self,text): return self.stream.write(text.replace("[C248]","[C250]"))
    def flush(self): return self.stream.flush()


def initial_reference(backbone,parts,seed,family,*,fitting,binding,factory):
    require((seed,family) in reference_identities(),"unregistered reference identity")
    before=factory.fingerprint(backbone);counts=[0,0]
    def hook(module,args,output): counts[0]+=1;counts[1]+=len(args[0])
    handle=backbone.register_forward_hook(hook)
    try: metrics,_=fitting.evaluate(backbone,parts["TRAIN"],binding,factory.fingerprint)
    finally: handle.remove()
    fitting.validate_metrics(metrics,64)
    require(counts==[3,192] and factory.fingerprint(backbone)==before,"initial reference mutation/workload")
    return dict(seed=seed,family=family,initial_sha256=before,initial_train=metrics,
        reference_forward_calls=counts[0],reference_row_presentations=counts[1])


def summarize(records,refs,fitting):
    require([(r["seed"],r["family"],r["arm"]) for r in records]==identities(),"model identity order")
    require([(r["seed"],r["family"]) for r in refs]==reference_identities(),"reference identity order")
    refmap={(r["seed"],r["family"]):r for r in refs}
    for r in refs:
        h=r["initial_sha256"]
        require(isinstance(h,str) and len(h)==64 and all(c in "0123456789abcdef" for c in h),"reference fingerprint")
        require((r["reference_forward_calls"],r["reference_row_presentations"])==(3,192),"reference workload")
        fitting.validate_metrics(r["initial_train"],64)
    gates={a:{f:True for f in FAMILIES} for a in ARMS}
    outcomes={a:Counter() for a in ARMS};seed_results=[];comparisons=[]
    for r in records:
        ref=refmap[r["seed"],r["family"]]
        require(r["backbone_initial_sha256"]==ref["initial_sha256"],"paired new backbone reference")
        require(r["parameters"]==BASE_PARAMS[r["family"]]+768 and r["block_updates"]==[200,200],"capacity/schedule")
        require((r["fit"]["steps"],r["fit"]["answer_presentations"],r["forward_calls"],r["row_presentations"])==(400,12800,415,13568),"model workload")
        require(r["checkpoint_roundtrip"] is True and r["prediction_replayed"] is True
            and r["weights_changed"] is True and r["head_weights_changed"] is True,"model integrity")
        for k in ("initial_metric_error","reload_max_error"):
            require(type(r[k]) in (int,float) and math.isfinite(r[k]) and 0<=r[k]<=TOL,"model replay error")
        require(set(r["final"])==set(SPLITS),"split schema")
        for s in SPLITS: fitting.validate_metrics(r["final"][s],ROWS[s])
        passed=True
        for lang in ("en","ja"):
            train=fitting.cell_pass(r["final"]["TRAIN"][lang]);held=fitting.cell_pass(r["final"]["HOLDOUT"][lang])
            outcomes[r["arm"]]["TRAIN_CRITERIA_MISS" if not train else "RECOMBINATION_MISS" if not held else "BOTH_PASS"]+=1
            passed &= train and held
        gates[r["arm"]][r["family"]] &= passed
        seed_results.append(dict(seed=r["seed"],family=r["family"],arm=r["arm"],both_languages_pass=passed))
    for i in range(0,len(records),2):
        r,c=records[i:i+2]
        for lang in ("en","ja"):
            a=r["final"]["HOLDOUT"][lang]["accuracy"];b=c["final"]["HOLDOUT"][lang]["accuracy"]
            comparisons.append(dict(seed=r["seed"],family=r["family"],language=lang,reader_accuracy=a,control_accuracy=b,delta=a-b))
    return dict(models=20,gates=gates,cell_outcomes={a:dict(v) for a,v in outcomes.items()},seed_results=seed_results,
        seed_pass_counts={a:{f:sum(x["both_languages_pass"] for x in seed_results if x["arm"]==a and x["family"]==f) for f in FAMILIES} for a in ARMS},
        comparisons=comparisons,train_steps=sum(r["fit"]["steps"] for r in records),
        answer_presentations=sum(r["fit"]["answer_presentations"] for r in records),
        model_forward_calls=sum(r["forward_calls"] for r in records)+sum(r["reference_forward_calls"] for r in refs),
        row_presentations=sum(r["row_presentations"] for r in records)+sum(r["reference_row_presentations"] for r in refs),
        all_replays=True,all_initial_replays=True,all_weights_changed=True,
        reference_forwards=sum(r["reference_forward_calls"] for r in refs),reference_rows=sum(r["reference_row_presentations"] for r in refs))


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(346,550) and set(OWN)<=set(p["source_blobs"]),"protection")
    require(len(p["artifacts"])==6 and {a["file"] for a in p["artifacts"]}==OUTPUTS,"artifact coverage")
    s=p["validation_summary"]
    require(tuple(s[k] for k in ("models","train_steps","answer_presentations","model_forward_calls","row_presentations","reference_forwards","reference_rows"))==(20,8000,256000,8330,273280,30,1920),"workload")
    require(all(s[k] is True for k in ("all_replays","all_initial_replays","all_weights_changed")),"integrity")
    require(len(s["comparisons"])==20 and len(s["seed_results"])==20 and all(sum(s["cell_outcomes"][a].values())==20 for a in ARMS),"cell counts")
    require(set(s["gates"])==set(ARMS) and all(set(s["gates"][a])==set(FAMILIES) and all(type(x) is bool for x in s["gates"][a].values()) for a in ARMS),"gate schema")
    require(p["status"]==("PASS" if s["gates"]["token_read"]["full"] else "FAIL"),"primary status")
    require(p["production_adoption"] is False and p["gate_f_candidate"] is False and p["network_calls"]==0,"scope")


def precheck(c249_summary,c248_summary,root):
    parent,reader,base,_,_,factory,a=context();root=Path(root)
    path=Path(c249_summary).resolve();prior=Path(c248_summary).resolve()
    require(a.sha(path)==PARENT_SHA,"C249 summary hash");p=a.read_json(path);parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS","accepted diagnostic")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items(): require(Path(name).is_file() and a.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items(): require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    require(protected.get(str(prior))==C248_SHA and a.sha(prior)==C248_SHA,"C248 inherited identity")
    require(str(path) not in protected,"parent double count");protected[str(path)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifacts")
    for item in p["artifacts"]:
        child=a.safe_child(path.parent,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"parent artifact bytes")
        require(str(child.resolve()) not in protected,"artifact double count");protected[str(child.resolve())]=item["sha256"]
    for name in OWN:
        require(name not in pins,"OWN collision");pins[name]=a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    helpers=("gate_f_c230_prepared_capsule.py","model_c231_byte_eval_contract.py","model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py","model_c234_context_binding.py","model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py","model_c237_frozen_signal_audit.py","model_c238_complete_cohort_sampler.py",
        "model_c239_order_holdout.py","model_c240_saved_position_audit.py","model_c241_assignment_holdout.py",
        "model_c242_balanced_recombination.py","model_c243_saved_recombination_audit.py","model_c244_two_partner_recombination.py",
        "model_c245_selective_evidence.py","model_c246_training_erasure.py","model_c247_normal_exposure_control.py",
        "model_c248_residual_token_read.py","model_c249_frozen_read_ablation.py")
    deps=set(factory.LM_SOURCES)|{OWN[0]}|{"fold_lm/v05_benchmarks/"+n for n in helpers}
    require(len(deps)==26 and deps<=set(pins),"direct dependency coverage")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(346,550) and digest(manifest())==MANIFEST_SHA,"counts/manifest")
    require(set(SEEDS).isdisjoint(reader.SEEDS) and len(SEEDS)==5,"prospective seed batch")
    reader.audit_recipe(base)
    return pins,protected


def load_inputs(c248_summary):
    parent,reader,_,_,_,_,a=context();path=Path(c248_summary).resolve()
    require(a.sha(path)==C248_SHA,"C248 input hash");reader.validate_result(a.read_json(path))
    parts,_=parent.load_inputs(path)
    require(digest(parts)==SPLIT_SHA and {s:len(v) for s,v in parts.items()}==ROWS,"fixed partition")
    return parts


def load_bundle(path):
    v=torch.load(path,map_location="cpu",weights_only=True)
    require(v["schema"]=="fold-c250-fresh-seeds-v1" and v["identities"]==[list(x) for x in identities()] and len(v["states"])==20,"bundle schema/order")
    return v["states"]


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==134,"parent modules")
    return names+["tests_lm.test_v05_c250_fresh_seed_replication"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite): yield from flatten(item)
        else: yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests]
    require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"test identities")
    kept=[t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(3170,3169),"suite counts")
    return unittest.TestSuite(kept)


def run(*,c249_summary,c248_summary,output_dir,expected_head):
    _,reader,base,fitting,binding,factory,a=context();root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"execution HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    pins,protected=precheck(c249_summary,c248_summary,root);parts=load_inputs(c248_summary)
    records=[];refs=[];states=[];raw=[];out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    for seed in SEEDS:
        full=factory.new_model(seed);gru=binding.parent_module().new_baseline(full)
        for family,backbone in (("full",full),("gru_only",gru)):
            ref=initial_reference(backbone,parts,seed,family,fitting=fitting,binding=binding,factory=factory);refs.append(ref)
            for arm in ARMS:
                require(factory.fingerprint(backbone)==ref["initial_sha256"],"shared backbone mutated between arms")
                model=reader.ReadoutPilot(copy.deepcopy(backbone),family,arm,seed)
                print(f"[C250] model={len(records)+1}/20 seed={seed} family={family} arm={arm}",flush=True)
                with redirect_stdout(Progress(sys.stdout)):
                    record,state,outputs=reader.train_one(model,parts,ref,arm,fitting=fitting,binding=binding,factory=factory)
                records.append(record);states.append(state);raw.append(outputs)
            require(factory.fingerprint(backbone)==ref["initial_sha256"],"source backbone mutated")
    torch.save(dict(schema="fold-c250-fresh-seeds-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for r,state,outputs in zip(records,load_bundle(out/"trained-models.pt"),raw,strict=True):
        backbone=factory.new_model(r["seed"])
        if r["family"]=="gru_only": backbone=binding.parent_module().new_baseline(backbone)
        model=reader.ReadoutPilot(backbone,r["family"],r["arm"],r["seed"])
        base.replay_one(model,state,r,outputs,parts,fitting=fitting,binding=binding,factory=factory)
    summary=summarize(records,refs,fitting)
    for name,value in (("replication-plan.json",manifest()),("split-dataset.json",parts),("initial-references.json",refs),
        ("measurements.json",records),("validation-summary.json",summary)): (out/name).write_bytes(blob(value))
    artifacts=[dict(file=n,sha256=a.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard();precheck(c249_summary,c248_summary,root)
    for name,wanted in protected.items(): require(a.sha(name)==wanted,"modified input")
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if summary["gates"]["token_read"]["full"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        production_adoption=False,gate_f_candidate=False,network_calls=0)
    validate_result(p);(out/"summary.json").write_bytes(blob(p));print("=== C250 RESULT ===",flush=True);print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(output_dir,c248_summary,expected_head):
    _,_,base,fitting,_,_,a=context();out=Path(output_dir);p=a.read_json(out/"summary.json");validate_result(p)
    require(p["commit_sha"]==expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items(): require(a.sha(name)==wanted,"postcheck input")
    for item in p["artifacts"]:
        path=a.safe_child(out,item["file"])
        require(a.sha(path)==item["sha256"] and path.stat().st_size==item["serialized_bytes"],"artifact bytes")
    parts=load_inputs(c248_summary);records=a.read_json(out/"measurements.json");refs=a.read_json(out/"initial-references.json")
    require(a.read_json(out/"replication-plan.json")==manifest() and a.read_json(out/"split-dataset.json")==parts,"plan/partition")
    require(summarize(records,refs,fitting)==p["validation_summary"]==a.read_json(out/"validation-summary.json"),"summary replay")
    for r in records:
        for split in SPLITS:
            measured=base.parent_module().discrete_metrics(parts[split],r["predictions"][split])
            require(all(abs(v-r["final"][split][l][k])<=TOL for l,d in measured.items() for k,v in d.items()),"saved discrete replay")
    return p,records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("c249-summary","c248-summary","output-dir"): parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True);run(**vars(parser.parse_args()))


if __name__=="__main__": main()
