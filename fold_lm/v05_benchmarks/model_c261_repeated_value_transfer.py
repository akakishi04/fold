"""C261: frozen repeated-value transfer; no model selection or further training."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C261-v5b-frozen-repeated-value-transfer"
STAGE = "V5-B-FROZEN-REPEATED-VALUE-TRANSFER"
BASE = "a2061c1cf321771241e262def1474cb8f59dcd79"
PARENT_EXECUTION = "5788a63a692983094a9c6311c58d1440005b7fca"
PARENT_SHA = "df6780749afa707fa0c6809e76710f39cdbeac6c1b69665a064248808b1f9ab6"
PARENT_ARTIFACTS = {
    "core-plan.json": "ee2ef5e828c22900a5e718ca867181dd7430a90b28eec7f112a61d3b8574e8ae",
    "dataset.json": "3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56",
    "evaluations.pt": "b109243f5b5d24ffe343586a50b97990524c7b572ec238b5e267863dbd542276",
    "measurements.json": "5839838218761bd608b5b79137a300649b3a5df11eb909474520a45608f3a8fa",
    "trained-models.pt": "727ffd1320266a239d21ce172279dc2cec3be6383db74cd4a1b09addbe36976c",
    "validation-summary.json": "250d099db6ec58b21db06d858e9c0e0ddf8349f66b0d1936001e3874875e26a2",
}
SEEDS = (260001, 260002, 260003, 260004, 260005)
ARMS = ("with_core", "without_core")
PARAMETERS = {"with_core": 14256, "without_core": 10928}
ORDERS = tuple(itertools.permutations(range(3)))
KINDS = ("pair_equal", "all_equal")
VIEWS = ("normal", "evidence_blind", "query_blind")
SPLITS = ("TRAIN", "HOLDOUT")
BATCH, TOL = 144, 1e-9
DATA_SHA = "1cf918049e4661bd11fc0aba90212e34eccd3e544c41b953f93ff5e3c1e59339"
MANIFEST_SHA = "bf8c32a5916d968871daeaa6ecf0c1fe38d75cd98b11d2d26096d578ff1a1301"
OWN = ("fold_lm/v05_benchmarks/model_c261_repeated_value_transfer.py",
       "tests_lm/test_v05_c261_repeated_value_transfer.py", "tools/run_c261.ps1", "tools/invoke_c261.ps1",
       "docs/experiment-ledger-addendum-c261-preregistration.md", "docs/v5b-repeated-value-transfer-v0.1.md")
OUTPUTS = {"repeat-plan.json", "repeat-dataset.json", "eval-outputs.pt", "measurements.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS, ARMS))


def context():
    from fold_lm.v05_benchmarks import model_c260_core_free_training as parent
    trainer, base, orders, aligned, reader, factory, audit = parent.context()
    return parent, trainer, base, orders, aligned, reader, factory, audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        seeds=list(SEEDS), arms=list(ARMS), parameters=PARAMETERS, dataset_sha256=DATA_SHA,
        orders=[list(p) for p in ORDERS], assignment_counts=dict(pair_equal=36, all_equal=4), rows=1440,
        views=list(VIEWS), batch=BATCH, changed="allow repeated values in new prompts; freeze all ten C260 final states",
        primary="all five seeds in BOTH arms pass new-task criteria; report each arm independently as well",
        anchor="raw-logit and exact-argmax replay of C260 final outputs; old capability misses do not invalidate replay",
        gate=dict(accuracy=.90, pair_singleton_accuracy=.90, pair_repeated_accuracy=.90,
                  pair_query_triplet=.80, evidence_drop=.35, six_order=.80),
        query_drop="descriptive only: duplicate targets change attainable blind accuracy; all-equal query is redundant",
        models=10, model_forward_calls=540, row_presentations=95040, core_forward_calls=1080,
        forwards_per_model=54, rows_per_model=9504, new_forwards_per_model=30,
        checkpoint_bundle_loads=1, model_state_loads=10, new_training_steps=0, new_checkpoint_writes=0,
        reference_eval_archive_loads_per_pass=2, formal_analysis_passes=2,
        output_logit_payload_bytes=194641920, source_pins=412, protected_inputs=685, direct_dependencies=37,
        own_tests=24, modules=146, loaded_tests=3430, focused_tests=3429, excluded_test=EXCLUDED,
        dtype="CPU float64", threads=2, deterministic=True, replay_tolerance=TOL, network_calls=0,
        gate_f_candidate=False, production_adoption=False, core_superiority_claim=False,
        general_language_claim=False, new_independent_benchmark_claim=False)


def render(row, view="normal"):
    require(view in VIEWS, "view")
    names = ("a", "b", "c") if row["language"] == "en" else ("甲", "乙", "丙")
    facts = ";".join(names[i] + "=" + ("?" if view == "evidence_blind" else str(row["assignment"][i])) for i in row["permutation"])
    return facts + ";" + ("?" if view == "query_blind" else names[row["query"]]) + "="


def dataset():
    rows = []
    for values in itertools.product(range(4), repeat=3):
        if len(set(values)) == 3:
            continue
        kind = "all_equal" if len(set(values)) == 1 else "pair_equal"
        for language in ("en", "ja"):
            for permutation in ORDERS:
                for query in range(3):
                    row = dict(id=f'{language}-{"".join(map(str,values))}-{"".join(map(str,permutation))}-{query}',
                        assignment=list(values), language=language, permutation=list(permutation), query=query,
                        target=48+values[query], kind=kind,
                        singleton=(kind == "pair_equal" and values.count(values[query]) == 1))
                    row["prompt"] = render(row)
                    require(len(row["prompt"].encode()) <= 46, "prompt length")
                    rows.append(row)
    return rows


def validate_dataset(rows):
    require(rows == dataset() and digest(rows) == DATA_SHA, "repeated dataset identity")
    require(len(rows) == len({r["id"] for r in rows}) == 1440, "row IDs")
    require(Counter(r["kind"] for r in rows) == {"pair_equal": 1296, "all_equal": 144}, "strata")


def check_logits(value, count):
    require(isinstance(value, torch.Tensor) and value.shape == (count, 256) and value.dtype == torch.float64
            and value.device.type == "cpu" and bool(torch.isfinite(value).all()), "finite CPU float64 logits")


def replay(left, right):
    check_logits(left, len(right)); check_logits(right, len(right))
    error = float((left-right).abs().max())
    require(error <= TOL and torch.equal(left.argmax(-1), right.argmax(-1)), "logit/argmax replay")
    return error


def replay_original(now, reference):
    require(set(now) == set(reference) == {"original", "extra"}, "anchor stages")
    errors = []
    for stage, count in (("original", 144), ("extra", 288)):
        require(set(now[stage]) == set(reference[stage]) == set(SPLITS), "anchor splits")
        for split in SPLITS:
            require(set(now[stage][split]) == set(reference[stage][split]) == set(VIEWS), "anchor views")
            for view in VIEWS:
                check_logits(now[stage][split][view], count)
                check_logits(reference[stage][split][view], count)
                errors.append(replay(now[stage][split][view], reference[stage][split][view]))
    return max(errors)


def score(rows, raw):
    validate_dataset(rows); require(set(raw) == set(VIEWS), "new views")
    for value in raw.values():
        check_logits(value, 1440)
    predictions = {v: x.argmax(-1).tolist() for v, x in raw.items()}
    correct = {v: [p == r["target"] for p, r in zip(predictions[v], rows, strict=True)] for v in VIEWS}
    losses = F.cross_entropy(raw["normal"], torch.tensor([r["target"] for r in rows]), reduction="none")
    cells, six = [], []
    for language in ("en", "ja"):
        for kind in KINDS:
            for permutation in ORDERS:
                ids = [i for i,r in enumerate(rows) if (r["language"],r["kind"],tuple(r["permutation"])) == (language,kind,permutation)]
                denominator = 108 if kind == "pair_equal" else 12
                require(len(ids) == denominator, "cell denominator")
                groups = defaultdict(list)
                for i in ids:
                    groups[tuple(rows[i]["assignment"])].append(i)
                require(len(groups) == denominator//3 and all(len(g) == 3 and {rows[i]["query"] for i in g} == {0,1,2} for g in groups.values()), "query triplets")
                acc = {v: sum(correct[v][i] for i in ids)/len(ids) for v in VIEWS}
                singleton = [i for i in ids if rows[i]["singleton"]]
                repeated = [i for i in ids if not rows[i]["singleton"]]
                sa = sum(correct["normal"][i] for i in singleton)/len(singleton) if singleton else None
                ra = sum(correct["normal"][i] for i in repeated)/len(repeated)
                triplet = sum(all(correct["normal"][i] for i in g) for g in groups.values())/len(groups)
                passed = acc["normal"] >= .90 and acc["normal"]-acc["evidence_blind"] >= .35
                if kind == "pair_equal":
                    require((len(singleton),len(repeated)) == (36,72), "singleton/repeated counts")
                    passed = passed and sa >= .90 and ra >= .90 and triplet >= .80
                cells.append(dict(language=language, kind=kind, permutation=list(permutation), rows=len(ids),
                    correct=sum(correct["normal"][i] for i in ids), accuracy=acc["normal"],
                    singleton_rows=len(singleton), singleton_accuracy=sa, repeated_accuracy=ra,
                    query_triplet_accuracy=triplet, evidence_blind_accuracy=acc["evidence_blind"],
                    query_blind_accuracy=acc["query_blind"], evidence_drop=acc["normal"]-acc["evidence_blind"],
                    query_drop=acc["normal"]-acc["query_blind"], answer_nll=float(losses[ids].mean()), passed=passed))
            groups = defaultdict(list)
            for i,r in enumerate(rows):
                if (r["language"],r["kind"]) == (language,kind):
                    groups[(tuple(r["assignment"]),r["query"])].append(i)
            require(len(groups) == (108 if kind == "pair_equal" else 12) and all(len(g) == 6 and
                    {tuple(rows[i]["permutation"]) for i in g} == set(ORDERS) for g in groups.values()), "six-order groups")
            full = sum(all(correct["normal"][i] for i in g) for g in groups.values())
            six.append(dict(language=language, kind=kind, groups=len(groups), all_six_correct=full,
                            accuracy=full/len(groups), passed=full/len(groups) >= .80))
    return dict(cells=cells, six_order=six, correct=sum(correct["normal"]), rows=1440,
                passed=all(c["passed"] for c in cells+six))


def evaluate_new(model, rows, factory):
    result = {}
    with torch.no_grad():
        for view in VIEWS:
            outputs = []
            for start in range(0, len(rows), BATCH):
                tokens = torch.stack([factory.prefix_tensor(render(r,view).encode()) for r in rows[start:start+BATCH]])
                logits = model(tokens, torch.zeros(len(tokens),dtype=torch.int64))
                check_logits(logits, len(tokens)); outputs.append(logits.detach().clone())
            result[view] = torch.cat(outputs)
    return result


def probe(model, ref, data, rows, parent, trainer, base, orders, factory):
    require(not any(m.training for m in model.modules()) and not any(p.requires_grad for p in model.parameters()), "frozen model")
    before = base.fingerprint(model)
    require(before == ref["final_sha256"] and sum(p.numel() for p in model.parameters()) == PARAMETERS[ref["arm"]], "final state/capacity")
    calls = [0,0]; cores, core_handle = parent.core_counter(model)
    def counted(module, args, output):
        calls[0] += 1; calls[1] += len(args[0])
    handle = model.register_forward_hook(counted)
    try:
        anchor = trainer.evaluate(model, data["original"], data["extra"], base, orders, factory)
        ae = replay_original(anchor, ref["raw"])
        require(base.fingerprint(model) == before, "anchor state mutation")
        novel = evaluate_new(model, rows, factory)
        restored = trainer.evaluate(model, data["original"], data["extra"], base, orders, factory)
        re = max(replay_original(restored, anchor), replay_original(restored, ref["raw"]))
    finally:
        handle.remove()
        if core_handle is not None:
            core_handle.remove()
    require(calls == [54,9504] and cores[0] == (216 if ref["arm"] == "with_core" else 0), "probe workload")
    require(base.fingerprint(model) == before, "frozen state changed")
    return dict(seed=ref["seed"], arm=ref["arm"], final_sha256=before, weights_preserved=True,
        model_forward_calls=54, row_presentations=9504, core_forward_calls=cores[0], anchor_error=ae,
        restore_error=re, anchor=anchor, novel=novel, restored=restored)


def analyze(records, refs, rows):
    require([(r["seed"],r["arm"]) for r in records] == [(r["seed"],r["arm"]) for r in refs] == identities(), "complete identities")
    measurements, results = [], []
    for r,ref in zip(records, refs, strict=True):
        require(r["final_sha256"] == ref["final_sha256"] and r["weights_preserved"] is True, "saved state identity")
        require((r["model_forward_calls"],r["row_presentations"],r["core_forward_calls"]) == (54,9504,216 if r["arm"] == "with_core" else 0), "saved workload")
        for key in ("anchor_error","restore_error"):
            require(type(r[key]) in (int,float) and math.isfinite(r[key]) and 0 <= r[key] <= TOL, "saved replay error")
        replay_original(r["anchor"], ref["raw"]); replay_original(r["restored"], r["anchor"])
        replay_original(r["restored"], ref["raw"])
        m = score(rows, r["novel"])
        measurements.append(dict(seed=r["seed"], arm=r["arm"], **m))
        results.append(dict(seed=r["seed"], arm=r["arm"], passed=m["passed"]))
    summary = dict(models=10, seed_results=results,
        seed_pass_counts={a:sum(r["passed"] for r in results if r["arm"] == a) for a in ARMS},
        joint_gate=all(r["passed"] for r in results), model_forward_calls=540, row_presentations=95040,
        core_forward_calls=1080, new_training_steps=0, new_checkpoint_writes=0, checkpoint_bundle_loads=1,
        model_state_loads=10, all_replays=True, all_weights_preserved=True)
    return measurements, summary


def check_parent(payload, parent):
    parent.validate_result(payload)
    require(payload["commit_sha"] == PARENT_EXECUTION and payload["status"] == "FAIL" and
            payload["validation_summary"]["seed_pass_counts"] == {"with_core":4,"without_core":3}, "accepted C260 negative")
    require({x["file"]:x["sha256"] for x in payload["artifacts"]} == PARENT_ARTIFACTS, "parent artifact contract")


def load_reference(path):
    parent,_,base,orders,_,_,_,audit = context(); path = Path(path).resolve()
    require(audit.sha(path) == PARENT_SHA, "parent summary hash")
    payload, measurements = parent.verify_artifacts(path.parent, PARENT_EXECUTION)
    check_parent(payload, parent)
    data = audit.read_json(path.parent/"dataset.json")
    archive = torch.load(path.parent/"evaluations.pt", map_location="cpu", weights_only=True)
    require(set(archive) == {"schema","records"} and archive["schema"] == "fold-c260-core-eval-v1", "parent archive schema")
    got, summary = parent.analyze(archive["records"], data["original"], data["extra"], base, orders)
    require(got == measurements and summary == payload["validation_summary"], "parent record replay")
    return data, archive["records"]


def validate_registration(source_count, input_count):
    actual = digest(manifest())
    print(f"registration_check = source_pins:{source_count}; protected_inputs:{input_count}; manifest_sha256:{actual}", flush=True)
    require((source_count,input_count) == (412,685), f"source/input counts: expected=(412, 685) actual=({source_count}, {input_count})")
    require(actual == MANIFEST_SHA, f"manifest hash: expected={MANIFEST_SHA} actual={actual}")
    validate_dataset(dataset())


def precheck(path, root):
    parent,_,_,_,_,_,factory,audit = context(); path = Path(path).resolve(); root = Path(root)
    require(audit.sha(path) == PARENT_SHA, "parent summary hash")
    payload = audit.read_json(path); check_parent(payload, parent)
    pins, protected = dict(payload["source_blobs"]), dict(payload["input_sha256"])
    for name,wanted in protected.items():
        require(Path(name).is_file() and audit.sha(name) == wanted, "changed input:"+name)
    for name,wanted in pins.items():
        require(audit.git(root,"rev-parse","HEAD:"+name).decode().strip() == wanted, "changed source:"+name)
    require(str(path) not in protected, "parent duplicate"); protected[str(path)] = PARENT_SHA
    for item in payload["artifacts"]:
        child = audit.safe_child(path.parent,item["file"])
        require(audit.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "parent artifact bytes")
        name = str(child.resolve()); require(name not in protected,"artifact duplicate"); protected[name] = item["sha256"]
    for name in OWN:
        require(name not in pins,"OWN collision"); pins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|260)_[^/]+)\.py"
    dependencies = set(factory.LM_SOURCES) | {n for n in payload["source_blobs"] if re.fullmatch(pattern,n)} | {OWN[0]}
    require(len(dependencies) == 37 and dependencies <= set(pins), "deciding dependency coverage")
    protected.update(audit.protect_tree_files(root,pins)); validate_registration(len(pins),len(protected))
    return pins, protected


def validate_result(payload):
    require(payload["experiment_id"] == EXPERIMENT_ID and payload["stage"] == STAGE and payload["diagnostic_execution_valid"] is True, "result identity")
    require((len(payload["source_blobs"]),len(payload["input_sha256"])) == (412,685) and set(OWN) <= set(payload["source_blobs"]), "protection")
    require(len(payload["artifacts"]) == 5 and {x["file"] for x in payload["artifacts"]} == OUTPUTS, "artifacts")
    summary = payload["validation_summary"]
    for key,value in dict(models=10,model_forward_calls=540,row_presentations=95040,core_forward_calls=1080,
                          new_training_steps=0,new_checkpoint_writes=0,checkpoint_bundle_loads=1,model_state_loads=10).items():
        require(type(summary[key]) is int and summary[key] == value, "workload:"+key)
    results = summary["seed_results"]
    require([(r["seed"],r["arm"]) for r in results] == identities() and all(type(r["passed"]) is bool for r in results), "result coverage")
    require(summary["joint_gate"] is all(r["passed"] for r in results) and summary["seed_pass_counts"] ==
            {a:sum(r["passed"] for r in results if r["arm"] == a) for a in ARMS}, "gate accounting")
    require(payload["status"] == ("PASS" if summary["joint_gate"] else "FAIL") and summary["all_replays"] is True and summary["all_weights_preserved"] is True, "status/integrity")
    require(all(payload[k] is False for k in ("gate_f_candidate","production_adoption","core_superiority_claim","general_language_claim")) and payload["network_calls"] == 0, "scope")


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == 145, "parent modules")
    return names + ["tests_lm.test_v05_c261_repeated_value_transfer"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]; require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1, "suite IDs")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require((len(tests),len(kept)) == (3430,3429), "suite counts")
    return unittest.TestSuite(kept)


def run(*,c260_summary,output_dir,expected_head):
    parent,trainer,base,orders,aligned,reader,factory,audit = context(); root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip() == expected_head,"HEAD")
        require(audit.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss","branch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected = precheck(c260_summary,root); data,refs = load_reference(c260_summary)
    rows = dataset(); validate_dataset(rows)
    states = parent.load_bundle(Path(c260_summary).resolve().parent/"trained-models.pt")
    require(len(states) == len(refs) == 10, "state count")
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False); records = []
    for i,seed in enumerate(SEEDS):
        pair = parent.make_pair(seed,base,aligned,reader,factory)
        for j,model in enumerate(pair):
            k = 2*i+j; ref = refs[k]
            model.load_state_dict(states[k],strict=True); model.eval().requires_grad_(False)
            print(f'[C261] model={k+1}/10 seed={seed} arm={ref["arm"]}; frozen repeated-value transfer',flush=True)
            records.append(probe(model,ref,data,rows,parent,trainer,base,orders,factory))
    measurements,summary = analyze(records,refs,rows)
    torch.save(dict(schema="fold-c261-repeat-eval-v1",records=records),out/"eval-outputs.pt")
    for name,value in (("repeat-plan.json",manifest()),("repeat-dataset.json",rows),("measurements.json",measurements),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard(); precheck(c260_summary,root)
    for name,wanted in protected.items():
        require(audit.sha(name) == wanted,"modified input")
    payload = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["joint_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,production_adoption=False,core_superiority_claim=False,general_language_claim=False,network_calls=0)
    validate_result(payload); (out/"summary.json").write_bytes(blob(payload))
    print("=== C261 RESULT ===",flush=True); print(blob(payload).decode(),flush=True)
    return payload


def verify_artifacts(output_dir,c260_summary,expected_head):
    audit = context()[-1]; out = Path(output_dir); payload = audit.read_json(out/"summary.json")
    validate_result(payload); require(payload["commit_sha"] == expected_head,"saved HEAD")
    for name,wanted in payload["input_sha256"].items():
        require(audit.sha(name) == wanted,"postcheck input")
    for item in payload["artifacts"]:
        child = audit.safe_child(out,item["file"])
        require(audit.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"],"output bytes")
    _,refs = load_reference(c260_summary); rows = audit.read_json(out/"repeat-dataset.json")
    archive = torch.load(out/"eval-outputs.pt",map_location="cpu",weights_only=True)
    require(set(archive) == {"schema","records"} and archive["schema"] == "fold-c261-repeat-eval-v1","eval schema")
    measurements,summary = analyze(archive["records"],refs,rows)
    for name,value in (("repeat-plan.json",manifest()),("measurements.json",measurements),("validation-summary.json",summary)):
        require(audit.read_json(out/name) == value,"persisted recomputation:"+name)
    require(summary == payload["validation_summary"],"summary replay")
    return payload,measurements


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("c260-summary","output-dir"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True); run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
