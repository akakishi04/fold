"""C262: paired minibatch chronology with identical initial weights and exposures."""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C262-v5b-paired-minibatch-order"
STAGE = "V5-B-PAIRED-MINIBATCH-ORDER"
BASE = "d83c37ad2febed01d1f5c94d6f60fa87f42dafda"
PARENT_EXECUTION = "5de24467fd439378505a2357e898fc618de31d45"
PARENT_SHA = "555ea1f2a1ae6970283d9b7784b0e382f6f58be202d493c0157c706c1255f9bf"
PARENT_ARTIFACTS = {
    "eval-outputs.pt": "ad2b19919cae9a258aef91e6c50596ab3624ab4df6b86f1b251c9a5b75c81fd2",
    "measurements.json": "1f0b7d3e23f14ea744683cd90c504e82e95d307b6668cfaa3047e6310d25934b",
    "repeat-dataset.json": "1cf918049e4661bd11fc0aba90212e34eccd3e544c41b953f93ff5e3c1e59339",
    "repeat-plan.json": "bf8c32a5916d968871daeaa6ecf0c1fe38d75cd98b11d2d26096d578ff1a1301",
    "validation-summary.json": "fc1926548185238f6464bdf30900597d4147eb58be767be14aed901d6b6fa962",
}
SEEDS = (262001, 262002, 262003, 262004, 262005)
ARMS = ("forward_blocks", "reverse_blocks")
SPLITS = ("TRAIN", "HOLDOUT")
VIEWS = ("normal", "evidence_blind", "query_blind")
STEPS, BATCH, TOL = 800, 48, 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c262_minibatch_order.py",
       "tests_lm/test_v05_c262_minibatch_order.py", "tools/run_c262.ps1", "tools/invoke_c262.ps1",
       "docs/experiment-ledger-addendum-c262-preregistration.md", "docs/v5b-minibatch-order-v0.1.md")
OUTPUTS = {"batch-plan.json", "dataset.json", "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "2e69e86ae813dcfde5f4096c1377c11cbe8907aa548d2c9cedcc6a0017bb279c"


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
    from fold_lm.v05_benchmarks import model_c261_repeated_value_transfer as parent
    c260, trainer, base, orders, aligned, reader, factory, audit = parent.context()
    return parent, c260, trainer, base, orders, aligned, reader, factory, audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        seeds=list(SEEDS), arms=list(ARMS), parameters=14256,
        model="actual C252 Full aligned reader in both arms; copied complete fresh initialization",
        changed="chronology of the same minibatches only, not fact order within a prompt",
        data="C256 distinct assignment partition and C257 all-six orders; C259 TRAIN tables",
        original_dataset_sha256="ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b",
        extra_dataset_sha256="9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052",
        schedule="randperm144(seed+256000+epoch); three48-row blocks; fact-order pair=epoch%3",
        forward_policy="consumed blocks in ascending order", reverse_policy="reverse only consumed blocks per epoch",
        last_epoch="step798,799 use blocks0,1 versus1,0; block2 absent in BOTH arms",
        pair_updates=[267,267,266], steps=800, batch=48, optimizer="AdamW", lr=.005,
        betas=[.9,.999], eps=1e-8, weight_decay=0., clip=1., fit_rng="seed+259000 reset per arm",
        primary="both batch orders, all five fresh seeds pass unchanged C260 distinct-task criteria",
        gate=dict(accuracy=.90, original_order_pair=.80, query_triplet=.80, evidence_drop=.35, query_drop=.35, six_order=.80),
        comparison="reverse minus forward HOLDOUT accuracy/six-order score; answer disagreements and directional correctness flips",
        models=10, train_steps=8000, training_rows=384000, model_forward_calls=8240,
        row_presentations=435840, core_forward_calls=32960, checkpoint_bundle_loads=1,
        model_state_loads=10, new_checkpoint_writes=1, artifacts=6,
        source_pins=418, protected_inputs=697, direct_dependencies=38, own_tests=24,
        modules=147, loaded_tests=3454, focused_tests=3453, excluded_test=EXCLUDED,
        dtype="CPU float64", threads=2, deterministic=True, replay_tolerance=TOL,
        network_calls=0, production_adoption=False, gate_f_candidate=False,
        initialization_only_cause_claim=False, core_superiority_claim=False, general_language_claim=False)


def batch_plan(seed, step, arm):
    require(seed in SEEDS and type(step) is int and 0 <= step < STEPS and arm in ARMS, "batch identity")
    epoch, offset = divmod(step, 3)
    consumed = min(3, STEPS - 3*epoch)
    block = offset if arm == ARMS[0] else consumed - 1 - offset
    g = torch.Generator(device="cpu").manual_seed(seed + 256000 + epoch)
    return torch.randperm(144, generator=g)[block*BATCH:(block+1)*BATCH], epoch % 3


def schedule(seed, arm):
    entries = [batch_plan(seed, step, arm) for step in range(STEPS)]
    ids = torch.stack([x for x, _ in entries])
    pairs = torch.tensor([p for _, p in entries], dtype=torch.int64)
    exposures = torch.bincount((pairs[:,None]*144 + ids).flatten(), minlength=432).tolist()
    return ids, pairs, dict(chronology_sha256=digest([ids.tolist(), pairs.tolist()]),
        exposure_sha256=digest(exposures), exposure_counts=exposures,
        order_pair_updates=torch.bincount(pairs, minlength=3).tolist())


def fit(model, tokens, targets, seed, arm):
    require(tokens.shape == (3,144,48) and targets.shape == (144,), "TRAIN tables")
    ids, pairs, plan = schedule(seed, arm)
    torch.manual_seed(seed + 259000)
    optimizer = torch.optim.AdamW(model.parameters(), lr=.005, betas=(.9,.999), eps=1e-8, weight_decay=0.)
    model.train()
    for step in range(STEPS):
        optimizer.zero_grad(set_to_none=True)
        logits = model(tokens[pairs[step], ids[step]], torch.zeros(BATCH, dtype=torch.int64))
        loss = F.cross_entropy(logits, targets[ids[step]])
        require(bool(torch.isfinite(loss)), "nonfinite loss")
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1., error_if_nonfinite=True)
        optimizer.step()
        if (step+1) % 200 == 0:
            print(f"[C262] seed={seed} arm={arm} step={step+1}/{STEPS} answer_nll={float(loss.detach()):.6f}", flush=True)
    model.eval()
    return dict(steps=STEPS, training_rows=STEPS*BATCH, last_loss=float(loss.detach()), **plan)


def train_one(model, seed, arm, data, tokens, targets, c260, trainer, base, orders, factory):
    require(sum(p.numel() for p in model.parameters()) == 14256, "Full capacity")
    initial = base.fingerprint(model)
    back = base.fingerprint(model.backbone)
    head = base.fingerprint(model.read)
    counts = [0,0]
    cores, core_handle = c260.core_counter(model)
    def counted(module, args, output):
        counts[0] += 1; counts[1] += len(args[0])
    handle = model.register_forward_hook(counted)
    try:
        fitted = fit(model, tokens, targets, seed, arm)
        raw = trainer.evaluate(model, data["original"], data["extra"], base, orders, factory)
    finally:
        handle.remove()
        if core_handle is not None:
            core_handle.remove()
    final = base.fingerprint(model)
    require(counts == [812,40992] and cores[0] == 3248, "train/final workload")
    require(final != initial and base.fingerprint(model.backbone) != back and base.fingerprint(model.read) != head, "weight change")
    record = dict(seed=seed, arm=arm, initial_sha256=initial, final_sha256=final, parameters=14256,
        weights_changed=True, backbone_changed=True, head_changed=True, fit=fitted, raw=raw,
        forward_calls=812, row_presentations=40992, core_forward_calls=3248)
    return record, {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def replay_one(model, state, record, data, c260, trainer, base, orders, factory):
    cores, handle = c260.core_counter(model)
    try:
        trainer.replay_one(model, state, record, data["original"], data["extra"], base, orders, factory)
    finally:
        if handle is not None:
            handle.remove()
    require(cores[0] == 48, "replay core count")
    record["replay_core_forward_calls"] = cores[0]


def compare_answers(left, right, data, language):
    counts = dict(rows=0, disagreements=0, correct_to_wrong=0, wrong_to_correct=0, both_wrong_different=0)
    for stage in ("original", "extra"):
        a = left[stage]["HOLDOUT"]["normal"].argmax(-1).tolist()
        b = right[stage]["HOLDOUT"]["normal"].argmax(-1).tolist()
        for row, av, bv in zip(data[stage]["HOLDOUT"], a, b, strict=True):
            if row["language"] != language:
                continue
            ac, bc = av == row["target"], bv == row["target"]
            counts["rows"] += 1
            counts["disagreements"] += av != bv
            counts["correct_to_wrong"] += ac and not bc
            counts["wrong_to_correct"] += bc and not ac
            counts["both_wrong_different"] += not ac and not bc and av != bv
    require(counts["rows"] == 216 and counts["disagreements"] == sum(counts[k] for k in ("correct_to_wrong","wrong_to_correct","both_wrong_different")), "answer partition")
    return counts


def analyze(records, data, c260, base, orders):
    require([(r["seed"],r["arm"]) for r in records] == identities(), "identities")
    require(set(data) == {"original","extra"} and data["original"] == base.dataset()
            and data["extra"] == orders.novel_dataset(data["original"]), "data identity")
    measurements, results = [], []
    for r in records:
        require(r["parameters"] == 14256 and all(r[k] is True for k in ("weights_changed","backbone_changed","head_changed","checkpoint_roundtrip")), "record integrity")
        require((r["forward_calls"],r["row_presentations"],r["core_forward_calls"],r["replay_forward_calls"],r["replay_row_presentations"],r["replay_core_forward_calls"]) == (812,40992,3248,12,2592,48), "record workload")
        require(type(r["reload_max_error"]) in (int,float) and math.isfinite(r["reload_max_error"]) and 0 <= r["reload_max_error"] <= TOL, "replay error")
        expected = schedule(r["seed"],r["arm"])[2]
        require(r["fit"]["steps"] == 800 and r["fit"]["training_rows"] == 38400, "fit budget")
        require(all(r["fit"][k] == v for k,v in expected.items()), "actual registered schedule")
        m = c260.score(r["raw"], data["original"], data["extra"], base, orders)
        measurements.append(dict(seed=r["seed"], arm=r["arm"], **m))
        results.append(dict(seed=r["seed"], arm=r["arm"], passed=m["passed"], outcome=m["outcome"]))
    comparisons = []
    for i in range(0,10,2):
        a,b = records[i:i+2]; am,bm = measurements[i:i+2]
        require(a["initial_sha256"] == b["initial_sha256"], "paired initial weights")
        require(a["fit"]["exposure_counts"] == b["fit"]["exposure_counts"] and a["fit"]["exposure_sha256"] == b["fit"]["exposure_sha256"], "paired exposure")
        require(a["fit"]["chronology_sha256"] != b["fit"]["chronology_sha256"], "chronology must differ")
        for lang in ("en","ja"):
            ac,bc = am["all_order_accuracy"]["HOLDOUT"][lang],bm["all_order_accuracy"]["HOLDOUT"][lang]
            flips = compare_answers(a["raw"],b["raw"],data,lang)
            require(bc["correct"]-ac["correct"] == flips["wrong_to_correct"]-flips["correct_to_wrong"], "score/flip reconciliation")
            comparisons.append(dict(seed=a["seed"], language=lang, forward_accuracy=ac["accuracy"],
                reverse_accuracy=bc["accuracy"], accuracy_delta=bc["accuracy"]-ac["accuracy"],
                forward_six_order=am["six_order"]["HOLDOUT"][lang]["accuracy"],
                reverse_six_order=bm["six_order"]["HOLDOUT"][lang]["accuracy"], **flips))
    summary = dict(models=10, seed_results=results, joint_gate=all(r["passed"] for r in results),
        seed_pass_counts={a:sum(r["passed"] for r in results if r["arm"] == a) for a in ARMS}, comparisons=comparisons,
        train_steps=8000, training_rows=384000, model_forward_calls=8240, row_presentations=435840,
        core_forward_calls=32960, checkpoint_bundle_loads=1, model_state_loads=10, new_checkpoint_writes=1,
        all_replays=True, all_pairs_matched=True)
    return measurements, summary


def load_parent(path):
    parent,_,_,_,_,_,_,_,audit = context(); path = Path(path).resolve()
    require(audit.sha(path) == PARENT_SHA, "parent hash")
    payload = audit.read_json(path); parent.validate_result(payload)
    require(payload["commit_sha"] == PARENT_EXECUTION and payload["status"] == "FAIL" and
            payload["validation_summary"]["seed_pass_counts"] == {"with_core":4,"without_core":3}, "accepted parent")
    require({x["file"]:x["sha256"] for x in payload["artifacts"]} == PARENT_ARTIFACTS, "parent artifacts")
    for item in payload["artifacts"]:
        child = audit.safe_child(path.parent,item["file"])
        require(audit.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "parent bytes")
    require(audit.read_json(path.parent/"validation-summary.json") == payload["validation_summary"], "parent summary contract")
    require(audit.read_json(path.parent/"repeat-plan.json") == parent.manifest(), "parent plan")
    return payload


def validate_registration(source_count, input_count):
    actual = digest(manifest())
    print(f"registration_check = source_pins:{source_count}; protected_inputs:{input_count}; manifest_sha256:{actual}", flush=True)
    require((source_count,input_count) == (418,697), f"counts expected=(418, 697) actual=({source_count}, {input_count})")
    require(actual == MANIFEST_SHA, f"manifest expected={MANIFEST_SHA} actual={actual}")


def precheck(path, root):
    *_,factory,audit = context(); path = Path(path).resolve(); root = Path(root)
    payload = load_parent(path); pins = dict(payload["source_blobs"]); protected = dict(payload["input_sha256"])
    for name,wanted in protected.items():
        require(Path(name).is_file() and audit.sha(name) == wanted, "changed input:"+name)
    for name,wanted in pins.items():
        require(audit.git(root,"rev-parse","HEAD:"+name).decode().strip() == wanted, "changed source:"+name)
    for child,wanted in [(path,PARENT_SHA)] + [(audit.safe_child(path.parent,x["file"]),x["sha256"]) for x in payload["artifacts"]]:
        name = str(child.resolve()); require(name not in protected,"duplicate parent input"); protected[name] = wanted
    for name in OWN:
        require(name not in pins,"OWN collision"); pins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[01])_[^/]+)\.py"
    deps = set(factory.LM_SOURCES) | {n for n in payload["source_blobs"] if re.fullmatch(pattern,n)} | {OWN[0]}
    require(len(deps) == 38 and deps <= set(pins), "direct dependencies")
    protected.update(audit.protect_tree_files(root,pins)); validate_registration(len(pins),len(protected))
    return pins, protected


def load_bundle(path):
    value = torch.load(path,map_location="cpu",weights_only=True)
    require(set(value) == {"schema","identities","states"} and value["schema"] == "fold-c262-batch-models-v1", "bundle schema")
    require(value["identities"] == [list(x) for x in identities()] and len(value["states"]) == 10, "bundle identities")
    return value["states"]


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["diagnostic_execution_valid"] is True, "result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"])) == (418,697) and set(OWN) <= set(p["source_blobs"]), "protection")
    require(len(p["artifacts"]) == 6 and {x["file"] for x in p["artifacts"]} == OUTPUTS, "outputs")
    s = p["validation_summary"]
    for k,v in dict(models=10,train_steps=8000,training_rows=384000,model_forward_calls=8240,row_presentations=435840,core_forward_calls=32960,checkpoint_bundle_loads=1,model_state_loads=10,new_checkpoint_writes=1).items():
        require(type(s[k]) is int and s[k] == v, "workload:"+k)
    results = s["seed_results"]
    require([(r["seed"],r["arm"]) for r in results] == identities() and all(type(r["passed"]) is bool for r in results), "result coverage")
    require(s["joint_gate"] is all(r["passed"] for r in results) and s["seed_pass_counts"] == {a:sum(r["passed"] for r in results if r["arm"] == a) for a in ARMS}, "joint gate")
    require(len(s["comparisons"]) == 10 and s["all_replays"] is True and s["all_pairs_matched"] is True, "comparisons/integrity")
    require(p["status"] == ("PASS" if s["joint_gate"] else "FAIL"), "status")
    require(all(p[k] is False for k in ("production_adoption","gate_f_candidate","initialization_only_cause_claim","core_superiority_claim","general_language_claim")) and p["network_calls"] == 0, "scope")


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == 146, "parent modules")
    return names + ["tests_lm.test_v05_c262_minibatch_order"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]; require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1, "test IDs")
    kept = [t for t in tests if t.id() != EXCLUDED]; require((len(tests),len(kept)) == (3454,3453), "suite counts")
    return unittest.TestSuite(kept)


def run(*,c261_summary,output_dir,expected_head):
    _,c260,trainer,base,orders,aligned,reader,factory,audit = context(); root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip() == expected_head,"HEAD")
        require(audit.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss","branch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected = precheck(c261_summary,root)
    parts = base.dataset(); data = dict(original=parts,extra=orders.novel_dataset(parts))
    require(digest(parts) == manifest()["original_dataset_sha256"] and digest(data["extra"]) == manifest()["extra_dataset_sha256"], "task hashes")
    tokens,targets = trainer.training_tables(parts,factory,orders)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False); records = []; states = []
    for seed in SEEDS:
        initial = base.make_model(factory.new_model(seed),"aligned_precore_read",seed,aligned,reader)
        initial_sha = base.fingerprint(initial)
        for arm in ARMS:
            print(f"[C262] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            r,state = train_one(copy.deepcopy(initial),seed,arm,data,tokens,targets,c260,trainer,base,orders,factory)
            require(r["initial_sha256"] == initial_sha and base.fingerprint(initial) == initial_sha,"template pairing")
            records.append(r); states.append(state)
    torch.save(dict(schema="fold-c262-batch-models-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for r,state in zip(records,load_bundle(out/"trained-models.pt"),strict=True):
        model = base.make_model(factory.new_model(r["seed"]),"aligned_precore_read",r["seed"],aligned,reader)
        replay_one(model,state,r,data,c260,trainer,base,orders,factory)
    measurements,summary = analyze(records,data,c260,base,orders)
    torch.save(dict(schema="fold-c262-batch-eval-v1",records=records),out/"evaluations.pt")
    for name,value in (("batch-plan.json",manifest()),("dataset.json",data),("measurements.json",measurements),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard(); precheck(c261_summary,root)
    for name,wanted in protected.items():
        require(audit.sha(name) == wanted,"modified input")
    p = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["joint_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        production_adoption=False,gate_f_candidate=False,initialization_only_cause_claim=False,core_superiority_claim=False,general_language_claim=False,network_calls=0)
    validate_result(p); (out/"summary.json").write_bytes(blob(p)); print("=== C262 RESULT ===",flush=True); print(blob(p).decode(),flush=True)
    return p


def verify_artifacts(output_dir, expected_head):
    _,c260,_,base,orders,_,_,_,audit = context(); out = Path(output_dir); p = audit.read_json(out/"summary.json")
    validate_result(p); require(p["commit_sha"] == expected_head,"saved HEAD")
    for name,wanted in p["input_sha256"].items():
        require(audit.sha(name) == wanted,"postcheck input")
    for x in p["artifacts"]:
        child = audit.safe_child(out,x["file"])
        require(audit.sha(child) == x["sha256"] and child.stat().st_size == x["serialized_bytes"],"output bytes")
    data = audit.read_json(out/"dataset.json"); value = torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
    require(set(value) == {"schema","records"} and value["schema"] == "fold-c262-batch-eval-v1","evaluation schema")
    measurements,summary = analyze(value["records"],data,c260,base,orders)
    for name,item in (("batch-plan.json",manifest()),("measurements.json",measurements),("validation-summary.json",summary)):
        require(audit.read_json(out/name) == item,"persisted replay:"+name)
    require(p["validation_summary"] == summary,"saved summary")
    return p,measurements


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("c261-summary","output-dir"):
        p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--expected-head",required=True); run(**vars(p.parse_args()))


if __name__ == "__main__":
    main()
