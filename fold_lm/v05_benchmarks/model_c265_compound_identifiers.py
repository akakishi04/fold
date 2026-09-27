"""C265: frozen compound-identifier transfer using only previously observed bytes."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import unittest
import torch

EXPERIMENT_ID = "C265-v5b-frozen-compound-identifiers"
STAGE = "V5-B-FROZEN-COMPOUND-IDENTIFIERS"
BASE = "d0af4709b7362f145ca55c2bfee5038b107e2961"
PARENT_EXECUTION = "6da6c182f328cccddbdfbd94e232141b0c68c0ea"
PARENT_SHA = "1c7e3d517bcf764f2b4eb89e432cb8ce303861359957f1fbfd77de9f19eb1503"
MODEL_SOURCE_SHA = "1fcceab38de3e34a3858828285fd43503df9e455e2fdb3bd31524b5035813e21"
PARENT_ARTIFACTS = {
    "deletion-plan.json": "a4cfef0b148d7f2130324127f51217d03c191bf788b87d07d52b1d67890095b1",
    "eval-outputs.pt": "3123aa3b0c2e74b1a069edeb56da5a52046fc5731f681656abf51d4200db55b3",
    "measurements.json": "34c43a5eea6aa235a7bcf8451f3742393a53255a63299c43874c5bf948b87f99",
    "provenance.json": "35f96556b849adeac41cc04cc77d91c94ba4e560783d0f58c67e3898ea479577",
    "two-fact-dataset.json": "8adacd9b13b87c9f6a2bd7e1bf0f735e9a1a63b521840ef301a855586643e6c1",
    "validation-summary.json": "171731535a0f725e5cfb5912828e8c082c5950507a9dade64cf43463fe304a14",
}
SEEDS = tuple(range(263001,263006))
ARMS = ("standard_forward","standard_reverse","lower_forward","lower_reverse")
PROFILES = ("doubled","shared_prefix","shared_suffix")
VIEWS = ("normal","evidence_blind","query_blind")
TOL = 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c265_compound_identifiers.py",
       "tests_lm/test_v05_c265_compound_identifiers.py","tools/run_c265.ps1","tools/invoke_c265.ps1",
       "docs/experiment-ledger-addendum-c265-preregistration.md","docs/v5b-compound-identifiers-v0.1.md")
OUTPUTS = {"identifier-plan.json","identifier-dataset.json","eval-outputs.pt","measurements.json","validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
DATA_SHA = "4bcc707da1814d765c4218f73203e175d092bea096becc593b789fbbcdb729bb"
MANIFEST_SHA = "1a6316f251e15e29e67d22eb2d6be02407a6fa4ea6a610759b332f5bd9de53a3"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS,ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c264_two_fact_deletion as parent
    source,c260,_,base,_,aligned,reader,factory,audit = parent.context()
    return parent,source,c260,base,aligned,reader,factory,audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID,stage=STAGE,acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION,parent_sha256=PARENT_SHA,model_source_sha256=MODEL_SOURCE_SHA,
        parent_artifacts=PARENT_ARTIFACTS,seeds=list(SEEDS),arms=list(ARMS),profiles=list(PROFILES),
        dataset_sha256=DATA_SHA,parameters=14256,
        changed="consistent two-symbol renaming: uu/vv, uu/uv, uu/vu for each original u/v pair",
        primary="all twenty states pass all three naming profiles; report every profile and arm",
        scoring="actual C264 score on fixed target/group metadata; only renamed bytes reach the model",
        gate=dict(accuracy=.90,query_pair=.80,evidence_drop=.35,query_drop=.35,two_order=.80),
        rows_per_profile=288,new_rows=864,model_forward_calls=600,row_presentations=86400,
        core_forward_calls=2400,checkpoint_bundle_loads=1,model_state_loads=20,
        new_training_steps=0,new_checkpoint_writes=0,logit_payload_bytes=176947200,
        c264_reference_archive_loads_per_pass=2,c263_reference_archive_loads_per_pass=2,formal_analysis_passes=2,
        source_pins=436,protected_inputs=736,direct_dependencies=41,own_tests=24,
        modules=150,loaded_tests=3526,focused_tests=3525,excluded_test=EXCLUDED,
        dtype="CPU float64",threads=2,deterministic=True,replay_tolerance=TOL,network_calls=0,
        gate_f_candidate=False,production_adoption=False,arbitrary_name_claim=False,causal_parser_claim=False)


def name_map(row, profile):
    require(profile in PROFILES and row["language"] in ("en","ja"),"profile/language")
    chars = ("a","b","c") if row["language"] == "en" else ("甲","乙","丙")
    i,j = row["entities"]; u,v = chars[i],chars[j]
    require(i < j and i in (0,1) and j in (1,2),"entity pair")
    second = v+v if profile == "doubled" else u+v if profile == "shared_prefix" else v+u
    return {i:u+u,j:second}


def render(row, profile, view="normal"):
    require(view in VIEWS,"view")
    names = name_map(row,profile); values = dict(zip(row["entities"],row["values"],strict=True))
    facts = ";".join(names[i]+"="+("?" if view == "evidence_blind" else str(values[i])) for i in row["permutation"])
    return facts+";"+("?" if view == "query_blind" else names[row["query"]])+"="


def dataset(rows, parent):
    parent.validate_dataset(rows)
    return {profile:[dict(source_id=r["id"],target=r["target"],
        views={v:render(r,profile,v) for v in VIEWS}) for r in rows] for profile in PROFILES}


def validate_dataset(data, rows, parent):
    require(data == dataset(rows,parent) and digest(data) == DATA_SHA,"identifier dataset identity")
    old_bytes = set().union(*(set(parent.render(r,v).encode()) for r in rows for v in VIEWS))
    texts = [item["views"]["normal"] for profile in PROFILES for item in data[profile]]
    require(len(texts) == len(set(texts)) == 864,"unique renamed inputs")
    for index,r in enumerate(rows):
        lengths = []
        for profile in PROFILES:
            item = data[profile][index]
            require(item["source_id"] == r["id"] and item["target"] == r["target"],"paired metadata")
            lengths.append(len(item["views"]["normal"].encode()))
            for text in item["views"].values():
                require(len(text.encode()) <= 46 and set(text.encode()) <= old_bytes,"length/new byte")
        require(len(set(lengths)) == 1,"profile length matching")


def replay(left, right, parent):
    require(set(left) == set(right) == set(VIEWS),"replay views")
    error = 0.
    for view in VIEWS:
        a,b = left[view],right[view]; parent.check_logits(a,288); parent.check_logits(b,288)
        error = max(error,float((a-b).abs().max()))
        require(error <= TOL and torch.equal(a.argmax(-1),b.argmax(-1)),"raw/argmax replay")
    return error


def evaluate_profile(model, items, factory, parent):
    require(len(items) == 288,"profile size"); raw = {}
    with torch.no_grad():
        for view in VIEWS:
            chunks = []
            for start in (0,144):
                tokens = torch.stack([factory.prefix_tensor(r["views"][view].encode()) for r in items[start:start+144]])
                logits = model(tokens,torch.zeros(144,dtype=torch.int64))
                parent.check_logits(logits,144); chunks.append(logits.detach().clone())
            raw[view] = torch.cat(chunks)
    return raw


def probe(model, ref, rows, data, parent, c260, base, factory):
    require(not any(m.training for m in model.modules()) and not any(p.requires_grad for p in model.parameters()),"frozen model")
    before = base.fingerprint(model)
    require(before == ref["final_sha256"] and sum(p.numel() for p in model.parameters()) == 14256,"state identity/capacity")
    counts = [0,0]; cores,ch = c260.core_counter(model)
    def counted(module,args,output):
        counts[0] += 1; counts[1] += len(args[0])
    hook = model.register_forward_hook(counted)
    try:
        anchor = parent.evaluate_new(model,rows,factory)
        ae = replay(anchor,ref["reduced"],parent)
        require(base.fingerprint(model) == before,"anchor mutation")
        renamed = {profile:evaluate_profile(model,data[profile],factory,parent) for profile in PROFILES}
        restored = parent.evaluate_new(model,rows,factory)
        recheck = max(replay(restored,anchor,parent),replay(restored,ref["reduced"],parent))
    finally:
        hook.remove()
        if ch is not None:
            ch.remove()
    require(counts == [30,4320] and cores[0] == 120,"probe counts")
    require(base.fingerprint(model) == before,"weight mutation")
    return dict(seed=ref["seed"],arm=ref["arm"],final_sha256=before,weights_preserved=True,
        model_forward_calls=30,row_presentations=4320,core_forward_calls=120,anchor_error=ae,
        restore_error=recheck,anchor=anchor,renamed=renamed,restored=restored)


def analyze(records, refs, rows, parent):
    require([(r["seed"],r["arm"]) for r in records] == [(r["seed"],r["arm"]) for r in refs] == identities(),"record identities")
    metrics,results = [],[]
    for r,ref in zip(records,refs,strict=True):
        require(r["weights_preserved"] is True and r["final_sha256"] == ref["final_sha256"],"saved state")
        require((r["model_forward_calls"],r["row_presentations"],r["core_forward_calls"]) == (30,4320,120),"saved counts")
        for key in ("anchor_error","restore_error"):
            require(type(r[key]) in (int,float) and math.isfinite(r[key]) and 0 <= r[key] <= TOL,"saved replay error")
        replay(r["anchor"],ref["reduced"],parent); replay(r["restored"],r["anchor"],parent); replay(r["restored"],ref["reduced"],parent)
        require(set(r["renamed"]) == set(PROFILES),"all naming profiles")
        # Targets and group identities are unchanged. These original rows are OFFLINE metadata only.
        scores = {profile:parent.score(rows,r["renamed"][profile]) for profile in PROFILES}
        passed = all(m["passed"] for m in scores.values())
        metrics.append(dict(seed=r["seed"],arm=r["arm"],profiles=scores,passed=passed))
        results.append(dict(seed=r["seed"],arm=r["arm"],profile_pass={k:v["passed"] for k,v in scores.items()},passed=passed))
    summary = dict(models=20,seed_results=results,joint_gate=all(r["passed"] for r in results),
        seed_pass_counts={a:sum(r["passed"] for r in results if r["arm"] == a) for a in ARMS},
        profile_pass_counts={p:{a:sum(r["profile_pass"][p] for r in results if r["arm"] == a) for a in ARMS} for p in PROFILES},
        model_forward_calls=600,row_presentations=86400,core_forward_calls=2400,checkpoint_bundle_loads=1,
        model_state_loads=20,new_training_steps=0,new_checkpoint_writes=0,all_replays=True,all_weights_preserved=True)
    return metrics,summary


def check_parent(payload, parent):
    parent.validate_result(payload)
    require(payload["commit_sha"] == PARENT_EXECUTION and payload["status"] == "PASS","accepted C264")
    require(payload["validation_summary"]["seed_pass_counts"] == {a:5 for a in ARMS},"parent gate")
    require({x["file"]:x["sha256"] for x in payload["artifacts"]} == PARENT_ARTIFACTS,"parent artifacts")


def load_reference(c264_summary, c263_summary):
    parent,*_,audit = context(); path = Path(c264_summary).resolve(); source = Path(c263_summary).resolve()
    require(audit.sha(path) == PARENT_SHA and audit.sha(source) == MODEL_SOURCE_SHA,"parent/source hash")
    with parent.no_model_calls():
        payload,metrics = parent.verify_artifacts(path.parent,source,PARENT_EXECUTION)
        check_parent(payload,parent)
        rows = audit.read_json(path.parent/"two-fact-dataset.json"); parent.validate_dataset(rows)
        archive = torch.load(path.parent/"eval-outputs.pt",map_location="cpu",weights_only=True)
        require(set(archive) == {"schema","records"} and archive["schema"] == "fold-c264-deletion-eval-v1","parent archive")
        refs = [{k:r[k] for k in ("seed","arm","final_sha256","reduced")} for r in archive["records"]]
        require([(r["seed"],r["arm"]) for r in refs] == identities(),"reference identities")
        expected = [dict(seed=r["seed"],arm=r["arm"],**parent.score(rows,r["reduced"])) for r in refs]
        require(expected == metrics,"accepted reduced-output semantics")
    return rows,refs


def validate_registration(source_count, input_count):
    actual = digest(manifest())
    print(f"registration_check = source_pins:{source_count}; protected_inputs:{input_count}; manifest_sha256:{actual}",flush=True)
    require((source_count,input_count) == (436,736),"source/input counts")
    require(actual == MANIFEST_SHA,f"manifest expected={MANIFEST_SHA} actual={actual}")


def precheck(c264_summary, c263_summary, root):
    parent,*_,factory,audit = context(); path = Path(c264_summary).resolve(); source = Path(c263_summary).resolve(); root = Path(root)
    require(audit.sha(path) == PARENT_SHA,"parent hash"); payload = audit.read_json(path); check_parent(payload,parent)
    pins,protected = dict(payload["source_blobs"]),dict(payload["input_sha256"])
    require(protected.get(str(source)) == MODEL_SOURCE_SHA,"model source must be inherited/protected")
    for name,wanted in protected.items():
        require(Path(name).is_file() and audit.sha(name) == wanted,"changed input:"+name)
    for name,wanted in pins.items():
        require(audit.git(root,"rev-parse","HEAD:"+name).decode().strip() == wanted,"changed source:"+name)
    for child,wanted in [(path,PARENT_SHA)]+[(audit.safe_child(path.parent,x["file"]),x["sha256"]) for x in payload["artifacts"]]:
        key = str(child.resolve()); require(key not in protected and audit.sha(child) == wanted,"parent artifact identity"); protected[key] = wanted
    for x in payload["artifacts"]:
        require(audit.safe_child(path.parent,x["file"]).stat().st_size == x["serialized_bytes"],"parent artifact size")
    for name in OWN:
        require(name not in pins,"OWN collision"); pins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-4])_[^/]+)\.py"
    deps = set(factory.LM_SOURCES)|{n for n in payload["source_blobs"] if re.fullmatch(pattern,n)}|{OWN[0]}
    require(len(deps) == 41 and deps <= set(pins),"direct dependencies")
    protected.update(audit.protect_tree_files(root,pins)); validate_registration(len(pins),len(protected))
    rows = parent.dataset(); validate_dataset(dataset(rows,parent),rows,parent)
    return pins,protected


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["diagnostic_execution_valid"] is True,"result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"])) == (436,736) and set(OWN) <= set(p["source_blobs"]),"protection")
    require(len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS,"output coverage")
    s = p["validation_summary"]; rr = s["seed_results"]
    require([(r["seed"],r["arm"]) for r in rr] == identities(),"result coverage")
    for r in rr:
        require(set(r["profile_pass"]) == set(PROFILES) and all(type(v) is bool for v in r["profile_pass"].values()),"profile flags")
        require(r["passed"] is all(r["profile_pass"].values()),"profile gate")
    require(s["joint_gate"] is all(r["passed"] for r in rr) and s["seed_pass_counts"] == {a:sum(r["passed"] for r in rr if r["arm"] == a) for a in ARMS},"joint gate")
    require(s["profile_pass_counts"] == {pr:{a:sum(r["profile_pass"][pr] for r in rr if r["arm"] == a) for a in ARMS} for pr in PROFILES},"profile counts")
    for k,v in dict(models=20,model_forward_calls=600,row_presentations=86400,core_forward_calls=2400,checkpoint_bundle_loads=1,model_state_loads=20,new_training_steps=0,new_checkpoint_writes=0).items():
        require(type(s[k]) is int and s[k] == v,"workload:"+k)
    require(s["all_replays"] is True and s["all_weights_preserved"] is True and p["status"] == ("PASS" if s["joint_gate"] else "FAIL"),"status")
    require(all(p[k] is False for k in ("gate_f_candidate","production_adoption","arbitrary_name_claim","causal_parser_claim")) and p["network_calls"] == 0,"scope")


def regression_modules(root):
    names = context()[0].regression_modules(root); require(len(names) == len(set(names)) == 149,"parent modules")
    return names+["tests_lm.test_v05_c265_compound_identifiers"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root)))); ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1,"test IDs")
    kept = [t for t in tests if t.id() != EXCLUDED]; require((len(tests),len(kept)) == (3526,3525),"suite counts")
    return unittest.TestSuite(kept)


def run(*, c264_summary, c263_summary, output_dir, expected_head):
    parent,source,c260,base,aligned,reader,factory,audit = context(); root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip() == expected_head,"HEAD")
        require(audit.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss","branch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected = precheck(c264_summary,c263_summary,root)
    rows,refs = load_reference(c264_summary,c263_summary); data = dataset(rows,parent); validate_dataset(data,rows,parent)
    states = source.load_bundle(Path(c263_summary).resolve().parent/"trained-models.pt")
    require(len(states) == len(refs) == 20,"state count")
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False); records = []
    for ref,state in zip(refs,states,strict=True):
        model = base.make_model(factory.new_model(ref["seed"]),"aligned_precore_read",ref["seed"],aligned,reader)
        model.load_state_dict(state,strict=True); model.eval().requires_grad_(False)
        print(f'[C265] model={len(records)+1}/20 seed={ref["seed"]} arm={ref["arm"]}; frozen identifier transfer',flush=True)
        records.append(probe(model,ref,rows,data,parent,c260,base,factory))
    metrics,summary = analyze(records,refs,rows,parent)
    torch.save(dict(schema="fold-c265-identifiers-eval-v1",records=records),out/"eval-outputs.pt")
    for name,value in (("identifier-plan.json",manifest()),("identifier-dataset.json",data),("measurements.json",metrics),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard(); precheck(c264_summary,c263_summary,root)
    for name,wanted in protected.items():
        require(audit.sha(name) == wanted,"modified input")
    p = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["joint_gate"] else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,gate_f_candidate=False,
        production_adoption=False,arbitrary_name_claim=False,causal_parser_claim=False,network_calls=0)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    print("=== C265 RESULT ===",flush=True); print(blob(p).decode(),flush=True); return p


def verify_artifacts(output_dir, c264_summary, c263_summary, expected_head):
    parent,*_,audit = context(); out = Path(output_dir); p = audit.read_json(out/"summary.json")
    validate_result(p); require(p["commit_sha"] == expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():
        require(audit.sha(name) == wanted,"postcheck input")
    for x in p["artifacts"]:
        child = audit.safe_child(out,x["file"])
        require(audit.sha(child) == x["sha256"] and child.stat().st_size == x["serialized_bytes"],"output bytes")
    with parent.no_model_calls():
        rows,refs = load_reference(c264_summary,c263_summary)
        data = audit.read_json(out/"identifier-dataset.json"); validate_dataset(data,rows,parent)
        archive = torch.load(out/"eval-outputs.pt",map_location="cpu",weights_only=True)
        require(set(archive) == {"schema","records"} and archive["schema"] == "fold-c265-identifiers-eval-v1","eval schema")
        metrics,summary = analyze(archive["records"],refs,rows,parent)
        for name,value in (("identifier-plan.json",manifest()),("measurements.json",metrics),("validation-summary.json",summary)):
            require(audit.read_json(out/name) == value,"persisted reconstruction:"+name)
    require(p["validation_summary"] == summary,"saved summary"); return p,metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("c264-summary","c263-summary","output-dir"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True); run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
