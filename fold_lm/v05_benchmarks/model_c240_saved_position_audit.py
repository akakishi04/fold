"""C240: analyze accepted C239 answer bytes; no model inference or training."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import unittest

EXPERIMENT_ID = "C240-v5b-saved-positional-rule-audit"
STAGE = "V5-B-SAVED-POSITIONAL-RULE-AUDIT"
BASE = "006551cd8b91e04534f253b5cf3942a12b84f7f8"
PARENT_EXECUTION = "c847609c8d045c9c5db4ec882bf336a9671180ff"
PARENT_SHA = "500af8c078c5a6114d1cb115b0dad9ee5ae7f622c41fce765f144668e2e041af"
PARENT_ARTIFACTS = {
    "holdout-plan.json": "4eca2f0276b521286729f1819abd929a035659a589488b332fe976d392b4dac0",
    "measurements.json": "872e534c5fb5f26fede0c4947b34344adc39a8e956bc453fed96763e757677c8",
    "split-dataset.json": "6f47a61c0ec4de616e77dab803ad964a9243e627b8a06f3e987d2824f8951731",
    "trained-models.pt": "2e3cf24b8feabead8f7470ebf271d27347ed0cf79aa873c30be68329a833d687",
    "validation-summary.json": "c65f6e6226630e5017c5cfa240116ad76106ec07a490d053216bde0a9a8b1849",
}
SEEDS, FAMILIES = (234001,234002,234003), ("full","gru_only")
SPLITS, VIEWS = ("TRAIN","HOLDOUT"), ("normal","evidence_blind","query_blind")
RULES = ("entity", "query_fixed_position", "first", "last", "constant_0", "constant_1")
TOL = 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c240_saved_position_audit.py",
    "tests_lm/test_v05_c240_saved_position_audit.py", "tools/run_c240.ps1", "tools/invoke_c240.ps1",
    "docs/experiment-ledger-addendum-c240-preregistration.md", "docs/v5b-saved-positional-rule-audit-v0.1.md")
OUTPUTS = {"audit-plan.json","row-audit.json","paired-orders.json","diagnostics.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "31d2b0579d65b354979ef1d98e3012a57a95820e2f12cd729c931c8d8525bc25"


def require(ok, message):
    if not ok: raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value): return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c239_order_holdout as parent
    return parent


def context():
    parent=parent_module()
    _,_,_,factory,audit=parent.context()
    return parent,factory,audit


def identities(): return list(itertools.product(SEEDS,FAMILIES))


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,parent_artifacts=PARENT_ARTIFACTS,
        identities=[list(x) for x in identities()],splits=list(SPLITS),views=list(VIEWS),rules=list(RULES),
        fixed_position_rule="query object0 selects rendered first value; object1 selects rendered second value",
        saved_predictions=288,normal_rows=96,rule_comparisons=576,order_pairs=48,diagnostic_cells=24,
        new_training_steps=0,model_forward_calls=0,checkpoint_loads=0,checkpoint_writes=0,network_calls=0,
        nll_recomputed=False,source_pins=286,protected_inputs=430,direct_dependency_union=16,
        own_tests=24,modules=125,loaded_tests=2930,focused_tests=2929,excluded_test=EXCLUDED,
        gate="integrity only; no required agreement with any rule",replay_tolerance=TOL,
        input_policy="exact C239 split and all three post-training prediction views; no logits inferred",
        rule_identifiability="TRAIN entity=fixed-position; HOLDOUT fixed-position=other entity for this binary fixture",
        causal_claim=False,capability_pass_claim=False,gate_f_candidate=False)


def rule_answers(row):
    values=row["values"]; q=row["query"]
    rendered=values if row["order"]==0 else values[::-1]
    return dict(entity=48+values[q],query_fixed_position=48+rendered[q],first=48+rendered[0],
                last=48+rendered[1],constant_0=48,constant_1=49)


def validate_parts(parts):
    require(set(parts)==set(SPLITS) and digest(parts)==PARENT_ARTIFACTS["split-dataset.json"],"partition identity")
    names={"en":("box","book"),"ja":("箱","本")}
    for split,order in zip(SPLITS,(0,1),strict=True):
        rows=parts[split]
        require(len(rows)==8 and len({r["id"] for r in rows})==8,"partition size/IDs")
        require(Counter((r["language"],r["target"]) for r in rows)=={(l,t):2 for l in names for t in (48,49)},"partition balance")
        for r in rows:
            require(r["objects"]==[0,1] and sorted(r["values"])==[0,1] and r["query"] in (0,1)
                    and r["order"]==order and r["split"]=="TRAIN","row semantics/provenance")
            facts=list(zip(r["objects"],r["values"],strict=True))
            if order: facts.reverse()
            prompt=";".join(names[r["language"]][k]+"="+str(v) for k,v in facts)+";"+names[r["language"]][r["query"]]+"="
            require(r["prompt"]==prompt and r["target"]==rule_answers(r)["entity"],"prompt/target relation")
    for key in ("id","prompt"):
        require(not {r[key] for r in parts["TRAIN"]}&{r[key] for r in parts["HOLDOUT"]},"partition overlap")
    return parts


def validate_predictions(pred):
    require(set(pred)==set(VIEWS),"prediction views")
    for values in pred.values():
        require(isinstance(values,list) and len(values)==8 and all(type(v) is int and 0<=v<256 for v in values),"unrestricted byte schema")


def pair_groups(rows,lang,kind):
    require(kind in ("facts","query"),"pair kind")
    groups=defaultdict(list)
    for i,r in enumerate(rows):
        if r["language"]==lang:
            key=(r["order"],r["query"]) if kind=="facts" else (r["group"],r["order"])
            groups[key].append(i)
    require(len(groups)==2 and all(len(g)==2 for g in groups.values()),"pair coverage")
    require(all(rows[i]["target"]!=rows[j]["target"] for i,j in groups.values()),"paired targets")
    return list(groups.values())


def discrete_metrics(rows,pred):
    validate_predictions(pred); out={}
    for lang in ("en","ja"):
        ids=[i for i,r in enumerate(rows) if r["language"]==lang]
        require(len(ids)==4,"language size")
        accuracy={v:sum(pred[v][i]==rows[i]["target"] for i in ids)/4 for v in VIEWS}
        out[lang]=dict(rows=4,accuracy=accuracy["normal"],evidence_blind_accuracy=accuracy["evidence_blind"],
            query_blind_accuracy=accuracy["query_blind"],evidence_drop=accuracy["normal"]-accuracy["evidence_blind"],
            query_drop=accuracy["normal"]-accuracy["query_blind"],
            **{("fact" if kind=="facts" else "query")+"_pair_accuracy":sum(all(pred["normal"][i]==rows[i]["target"] for i in pair)
                for pair in pair_groups(rows,lang,kind))/2 for kind in ("facts","query")})
    return out


def validate_record(parts,rec):
    require(set(rec["predictions"])==set(rec["final"])==set(SPLITS),"C239 split record schema")
    require(rec["checkpoint_roundtrip"] is True and rec["prediction_replayed"] is True
        and rec["weights_changed"] is True and 0<=rec["reload_max_error"]<=TOL,"parent replay flags")
    for split in SPLITS:
        computed=discrete_metrics(parts[split],rec["predictions"][split])
        require(set(rec["final"][split])=={"en","ja"},"parent languages")
        for lang,metrics in computed.items():
            saved=rec["final"][split][lang]
            require(set(saved)==set(metrics)|{"answer_nll"},"parent final metric keys")
            require(all(type(v) in (int,float) and math.isfinite(v) for v in saved.values()) and saved["answer_nll"]>=0,"parent metric finite")
            require(all(abs(saved[k]-v)<=TOL for k,v in metrics.items()),"saved prediction/metric mismatch")
    return True


def audit_record(parts,rec):
    validate_record(parts,rec); cells=[]; detailed=[]
    for split in SPLITS:
        rows=parts[split]; pred=rec["predictions"][split]
        for lang in ("en","ja"):
            items=[]
            for i,row in enumerate(rows):
                if row["language"]!=lang: continue
                rules=rule_answers(row); answer=pred["normal"][i]; other=48+row["values"][1-row["query"]]
                items.append(dict(seed=rec["seed"],family=rec["family"],split=split,language=lang,id=row["id"],
                    target=row["target"],other_entity=other,answers={v:pred[v][i] for v in VIEWS},rules=rules,
                    category="correct" if answer==row["target"] else "other_entity" if answer==other else "outside_supplied"))
            detailed.extend(items)
            cells.append(dict(split=split,language=lang,rows=4,
                categories={k:sum(x["category"]==k for x in items) for k in ("correct","other_entity","outside_supplied")},
                rule_matches={k:sum(x["answers"]["normal"]==x["rules"][k] for x in items) for k in RULES}))
    def key(row): return row["language"],row["group"],row["query"]
    held={key(row):(i,row) for i,row in enumerate(parts["HOLDOUT"])}
    require(len(held)==8 and set(held)=={key(r) for r in parts["TRAIN"]},"matched order keys")
    pairs=[]
    for i,row in enumerate(parts["TRAIN"]):
        j,other=held[key(row)]
        require(row["values"]==other["values"] and row["target"]==other["target"],"matched order semantics")
        a=rec["predictions"]["TRAIN"]["normal"][i]; c=rec["predictions"]["HOLDOUT"]["normal"][j]
        pairs.append(dict(seed=rec["seed"],family=rec["family"],language=row["language"],train_id=row["id"],holdout_id=other["id"],
            train_answer=a,holdout_answer=c,target=row["target"],same_answer=a==c,
            both_correct=a==c==row["target"],both_fixed_position=a==rule_answers(row)["query_fixed_position"] and c==rule_answers(other)["query_fixed_position"]))
    report=dict(seed=rec["seed"],family=rec["family"],cells=cells,discrete_replay=True,saved_predictions=48,
        normal_rows=16,rule_comparisons=96,order_pairs=8,
        identifiability=dict(TRAIN_entity_equals_fixed_position=True,HOLDOUT_fixed_position_equals_other_entity=True))
    return report,detailed,pairs


def summarize(reports):
    require([(r["seed"],r["family"]) for r in reports]==identities(),"diagnostic identity order")
    expected=list(itertools.product(SPLITS,("en","ja")))
    for r in reports:
        require([(c["split"],c["language"]) for c in r["cells"]]==expected,"diagnostic cell order")
        require(r["discrete_replay"] is True and (r["saved_predictions"],r["normal_rows"],r["rule_comparisons"],r["order_pairs"])==(48,16,96,8),"record workload/replay")
        for c in r["cells"]:
            require(c["rows"]==4 and set(c["rule_matches"])==set(RULES) and set(c["categories"])=={"correct","other_entity","outside_supplied"},"cell keys")
            require(all(type(n) is int and 0<=n<=4 for n in list(c["categories"].values())+list(c["rule_matches"].values()))
                and sum(c["categories"].values())==4,"cell counts")
    return dict(models=6,diagnostic_cells=24,saved_predictions=sum(r["saved_predictions"] for r in reports),
        normal_rows=sum(r["normal_rows"] for r in reports),rule_comparisons=sum(r["rule_comparisons"] for r in reports),
        order_pairs=sum(r["order_pairs"] for r in reports),all_discrete_replays=True,
        new_training_steps=0,model_forward_calls=0,checkpoint_loads=0,checkpoint_writes=0,
        nll_recomputed=False,capability_pass_claim=False,causal_claim=False)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE and p["status"]=="PASS"
        and p["diagnostic_execution_valid"] is True,"diagnostic identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(286,430) and set(OWN)<=set(p["source_blobs"]),"protection counts")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"artifact coverage")
    s=p["validation_summary"]; m=manifest()
    for k in ("diagnostic_cells","saved_predictions","normal_rows","rule_comparisons","order_pairs","new_training_steps","model_forward_calls","checkpoint_loads","checkpoint_writes"):
        require(type(s[k]) is int and s[k]==m[k],"summary count:"+k)
    require(s["models"]==6 and s["all_discrete_replays"] is True and s["nll_recomputed"] is False
        and s["capability_pass_claim"] is False and s["causal_claim"] is False
        and p["gate_f_candidate"] is False and p["network_calls"]==0,"integrity/scope")


def precheck(c239_summary,root):
    parent,factory,a=context(); root=Path(root); path=Path(c239_summary).resolve()
    require(a.sha(path)==PARENT_SHA,"C239 summary hash")
    p=a.read_json(path); parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="FAIL"
        and p["validation_summary"]["cell_outcomes"]=={"ORDER_HOLDOUT_MISS":12},"accepted parent")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for name,wanted in protected.items(): require(Path(name).is_file() and a.sha(name)==wanted,"changed input:"+name)
    for name,wanted in pins.items(): require(a.git(root,"rev-parse","HEAD:"+name).decode().strip()==wanted,"changed source:"+name)
    require(str(path) not in protected,"parent double count"); protected[str(path)]=PARENT_SHA
    require({x["file"]:x["sha256"] for x in p["artifacts"]}==PARENT_ARTIFACTS,"parent artifact contract")
    for item in p["artifacts"]:
        child=a.safe_child(path.parent,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"parent artifact bytes")
        require(str(child.resolve()) not in protected,"artifact double count"); protected[str(child.resolve())]=item["sha256"]
    for name in OWN:
        require(name not in pins,"OWN collision"); pins[name]=a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    deps=set(factory.LM_SOURCES)|{OWN[0]}|{"fold_lm/v05_benchmarks/"+x for x in (
        "gate_f_c230_prepared_capsule.py","model_c231_byte_eval_contract.py","model_c232_bilingual_learning.py",
        "model_c233_core_ablation.py","model_c234_context_binding.py","model_c235_frozen_binding_diagnostic.py",
        "model_c236_minimal_binding.py","model_c237_frozen_signal_audit.py","model_c238_complete_cohort_sampler.py","model_c239_order_holdout.py")}
    require(len(deps)==16 and deps<=set(pins),"dependency coverage")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(286,430) and digest(manifest())==MANIFEST_SHA,"count/manifest")
    return pins,protected


def load_inputs(c239_summary):
    parent,_,a=context(); directory=Path(c239_summary).resolve().parent
    parts=validate_parts(a.read_json(directory/"split-dataset.json"))
    records=a.read_json(directory/"measurements.json")
    require(parent.summarize(records)==a.read_json(c239_summary)["validation_summary"],"parent summary replay")
    require([(r["seed"],r["family"]) for r in records]==identities(),"parent identity order")
    for r in records: validate_record(parts,r)
    return parts,records


def analyze(parts,records):
    reports=[]; rows=[]; pairs=[]
    for rec in records:
        report,detail,matched=audit_record(parts,rec)
        reports.append(report); rows.extend(detail); pairs.extend(matched)
    summary=summarize(reports)
    require((len(rows),len(pairs))==(96,48),"output workload")
    return reports,rows,pairs,summary


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==124,"parent module count")
    return names+["tests_lm.test_v05_c240_saved_position_audit"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite): yield from flatten(item)
        else: yield item


def regression_suite(root):
    tests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests]; require(len(ids)==len(set(ids)) and ids.count(EXCLUDED)==1,"suite identity")
    kept=[t for t in tests if t.id()!=EXCLUDED]
    require((len(tests),len(kept))==(2930,2929),"suite counts")
    return unittest.TestSuite(kept)


def run(*,c239_summary,output_dir,expected_head):
    _,_,a=context(); root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"execution HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tracked tree")
    guard(); pins,protected=precheck(c239_summary,root); parts,records=load_inputs(c239_summary)
    reports,rows,pairs,summary=analyze(parts,records)
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    for name,value in (("audit-plan.json",manifest()),("row-audit.json",rows),("paired-orders.json",pairs),
                       ("diagnostics.json",reports),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard(); precheck(c239_summary,root)
    for name,wanted in protected.items(): require(a.sha(name)==wanted,"modified input")
    p=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,gate_f_candidate=False,network_calls=0,
        limitations=["Analysis of existing answers, not new samples or causal identification.",
            "TRAIN identity/fixed-position rules coincide; HOLDOUT fixed-position equals other entity.",
            "NLL and logits cannot be recomputed from argmax bytes; no model has been re-evaluated."])
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    print("=== C240 RESULT; SAVED ANSWERS ONLY ===",flush=True); print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(output_dir,c239_summary,expected_head):
    _,_,a=context(); out=Path(output_dir); p=a.read_json(out/"summary.json"); validate_result(p)
    require(p["commit_sha"]==expected_head,"saved execution identity")
    for name,wanted in p["input_sha256"].items(): require(a.sha(name)==wanted,"postcheck input")
    for item in p["artifacts"]:
        child=a.safe_child(out,item["file"])
        require(a.sha(child)==item["sha256"] and child.stat().st_size==item["serialized_bytes"],"postcheck artifact")
    parts,records=load_inputs(c239_summary); reports,rows,pairs,summary=analyze(parts,records)
    for name,wanted in (("audit-plan.json",manifest()),("row-audit.json",rows),("paired-orders.json",pairs),
                       ("diagnostics.json",reports),("validation-summary.json",summary)):
        require(a.read_json(out/name)==wanted,"persisted audit replay:"+name)
    require(summary==p["validation_summary"],"summary replay")
    return p,reports


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("c239-summary","output-dir"): parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__=="__main__": main()
