"""C263: fixed 2x2 learning-rate by minibatch-order experiment; no accepted code edits."""
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

EXPERIMENT_ID = "C263-v5b-learning-rate-order"
STAGE = "V5-B-LEARNING-RATE-ORDER"
BASE = "9edbef91d9a5bc81427b93003bae9127032643be"
PARENT_EXECUTION = "28030ad02e69a9ae7236fca7f7e84a61f3c89c46"
PARENT_SHA = "9cda47219d6e376516044d5807e546a8c13110f584f139bda2a3da8800b2d93d"
PARENT_ARTIFACTS = {
    "batch-plan.json": "2e69e86ae813dcfde5f4096c1377c11cbe8907aa548d2c9cedcc6a0017bb279c",
    "dataset.json": "3a1aecac635fb127c42b85f138a94d1a5c8472db0780fa0b1b17328afd087f56",
    "evaluations.pt": "f360dccf8b5523b27755e87734b0ae1c1b4ab8628b4e9c3fb32ada20f102db2f",
    "measurements.json": "13ffc5ce99372df17914f5a8cc07e03ba63e74cd091a24e650db62c6273e5e8d",
    "trained-models.pt": "84ce31fe704c193a9a5f17a0e9023b9f6d4dc84fd25badafd118a95738595713",
    "validation-summary.json": "d2843f6443c759795f50f81e68fc35cf742c28f3657716812207b756aab4c864",
}
SEEDS = (263001, 263002, 263003, 263004, 263005)
RATES = {"standard": .005, "lower": .001}
ORDERS = ("forward", "reverse")
ARMS = tuple(rate + "_" + order for rate in RATES for order in ORDERS)
SPLITS, VIEWS = ("TRAIN", "HOLDOUT"), ("normal", "evidence_blind", "query_blind")
STEPS, BATCH, TOL = 800, 48, 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c263_learning_rate_order.py",
       "tests_lm/test_v05_c263_learning_rate_order.py", "tools/run_c263.ps1", "tools/invoke_c263.ps1",
       "docs/experiment-ledger-addendum-c263-preregistration.md", "docs/v5b-learning-rate-order-v0.1.md")
OUTPUTS = {"rate-plan.json", "dataset.json", "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "ca53314f0e2ccda5bc7950f031c443ad70bb4e6c6c7181b53f8e7c0768199305"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def identities():
    return list(itertools.product(SEEDS, ARMS))


def arm_config(arm):
    require(arm in ARMS, "arm")
    rate, order = arm.split("_")
    return rate, order, RATES[rate]


def context():
    from fold_lm.v05_benchmarks import model_c262_minibatch_order as parent
    _, c260, trainer, base, orders, aligned, reader, factory, audit = parent.context()
    return parent, c260, trainer, base, orders, aligned, reader, factory, audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        seeds=list(SEEDS), rates=RATES, orders=list(ORDERS), arms=list(ARMS), parameters=14256,
        model="unchanged C252 Full aligned reader; same complete initial state within each four-arm group",
        changed="learning rate within each chronology; chronology effect compared at each of two fixed rates",
        original_dataset_sha256="ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b",
        extra_dataset_sha256="9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052",
        schedule="C262 forward/reverse consumed blocks; seed+256000+epoch; fact pair epoch%3; tail01 versus10",
        optimizer="AdamW", steps=800, batch=48, betas=[.9,.999], eps=1e-8, weight_decay=0., clip=1.,
        fit_rng="seed+259000 reset per arm", pair_updates=[267,267,266], dtype="CPU float64", threads=2,
        primary="all ten lower-rate states pass unchanged C260 criteria; standard-rate gates separate",
        gate=dict(accuracy=.90, original_order_pair=.80, query_triplet=.80, evidence_drop=.35, query_drop=.35, six_order=.80),
        comparisons="20 rate contrasts,20 order contrasts,10 language-level disagreement interactions; descriptive",
        models=20, train_steps=16000, training_rows=768000, model_forward_calls=16480, row_presentations=871680,
        core_forward_calls=65920, evaluation_forwards=480, checkpoint_bundle_loads=1, model_state_loads=20,
        new_checkpoint_writes=1, source_pins=424, protected_inputs=710, direct_dependencies=39,
        own_tests=24, modules=148, loaded_tests=3478, focused_tests=3477, excluded_test=EXCLUDED,
        replay_tolerance=TOL, network_calls=0, production_adoption=False, gate_f_candidate=False,
        learning_rate_benefit_claim=False, core_superiority_claim=False, general_language_claim=False)


def schedule(seed, order):
    require(seed in SEEDS and order in ORDERS, "schedule identity")
    entries = []
    for step in range(STEPS):
        epoch, offset = divmod(step, 3)
        consumed = min(3, STEPS - 3*epoch)
        block = offset if order == "forward" else consumed - 1 - offset
        g = torch.Generator(device="cpu").manual_seed(seed + 256000 + epoch)
        entries.append((torch.randperm(144, generator=g)[block*BATCH:(block+1)*BATCH], epoch % 3))
    ids = torch.stack([x for x, _ in entries])
    pairs = torch.tensor([p for _, p in entries], dtype=torch.int64)
    counts = torch.bincount((pairs[:, None]*144+ids).flatten(), minlength=432).tolist()
    return ids, pairs, dict(chronology_sha256=digest([ids.tolist(), pairs.tolist()]),
        exposure_sha256=digest(counts), exposure_counts=counts,
        order_pair_updates=torch.bincount(pairs, minlength=3).tolist())


def fit(model, tokens, targets, seed, arm):
    _, order, lr = arm_config(arm)
    require(tokens.shape == (3,144,48) and targets.shape == (144,), "TRAIN tables")
    ids, pairs, plan = schedule(seed, order)
    torch.manual_seed(seed+259000)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, betas=(.9,.999), eps=1e-8, weight_decay=0.)
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
            print(f"[C263] seed={seed} arm={arm} step={step+1}/{STEPS} answer_nll={float(loss.detach()):.6f}", flush=True)
    model.eval()
    return dict(steps=STEPS, training_rows=STEPS*BATCH, lr=lr, order=order, last_loss=float(loss.detach()), **plan)


def train_one(model, seed, arm, data, tokens, targets, c260, trainer, base, orders, factory):
    require(sum(p.numel() for p in model.parameters()) == 14256, "capacity")
    initial, back, head = base.fingerprint(model), base.fingerprint(model.backbone), base.fingerprint(model.read)
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
    record = dict(seed=seed, arm=arm, parameters=14256, initial_sha256=initial, final_sha256=final,
        weights_changed=True, backbone_changed=True, head_changed=True, fit=fitted, raw=raw,
        forward_calls=812, row_presentations=40992, core_forward_calls=3248)
    return record, {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def contrast(left, right, lm, rm, data, language, parent):
    a, b = lm["all_order_accuracy"]["HOLDOUT"][language], rm["all_order_accuracy"]["HOLDOUT"][language]
    flips = parent.compare_answers(left["raw"], right["raw"], data, language)
    require(b["correct"]-a["correct"] == flips["wrong_to_correct"]-flips["correct_to_wrong"], "flip reconciliation")
    return dict(seed=left["seed"], language=language, left_arm=left["arm"], right_arm=right["arm"],
        left_accuracy=a["accuracy"], right_accuracy=b["accuracy"], accuracy_delta=b["accuracy"]-a["accuracy"],
        left_six_order=lm["six_order"]["HOLDOUT"][language]["accuracy"],
        right_six_order=rm["six_order"]["HOLDOUT"][language]["accuracy"], **flips)


def analyze(records, data, parent, c260, base, orders):
    require([(r["seed"],r["arm"]) for r in records] == identities(), "identities")
    require(set(data) == {"original","extra"} and data["original"] == base.dataset()
            and data["extra"] == orders.novel_dataset(data["original"]), "data identity")
    measurements, results = [], []
    plans = {(s,o):schedule(s,o)[2] for s in SEEDS for o in ORDERS}
    for r in records:
        _, order, lr = arm_config(r["arm"])
        require(r["parameters"] == 14256 and all(r[k] is True for k in
                ("weights_changed","backbone_changed","head_changed","checkpoint_roundtrip")), "record integrity")
        require((r["forward_calls"],r["row_presentations"],r["core_forward_calls"],r["replay_forward_calls"],
                 r["replay_row_presentations"],r["replay_core_forward_calls"]) == (812,40992,3248,12,2592,48), "workload")
        require(type(r["reload_max_error"]) in (int,float) and math.isfinite(r["reload_max_error"])
                and 0 <= r["reload_max_error"] <= TOL, "replay error")
        fitted = r["fit"]
        require((fitted["steps"],fitted["training_rows"],fitted["lr"],fitted["order"]) == (800,38400,lr,order), "fit contract")
        require(all(fitted[k] == v for k,v in plans[r["seed"],order].items()), "registered schedule")
        require(type(fitted["last_loss"]) in (int,float) and math.isfinite(fitted["last_loss"]) and fitted["last_loss"] >= 0, "fit loss")
        m = c260.score(r["raw"], data["original"], data["extra"], base, orders)
        measurements.append(dict(seed=r["seed"], arm=r["arm"], lr=lr, **m))
        results.append(dict(seed=r["seed"], arm=r["arm"], passed=m["passed"], outcome=m["outcome"]))
    rate_contrasts, order_contrasts, interactions = [], [], []
    for i in range(0,20,4):
        rr, mm = records[i:i+4], measurements[i:i+4]
        require(len({r["initial_sha256"] for r in rr}) == 1, "four-way initial state")
        require(all(r["fit"]["exposure_counts"] == rr[0]["fit"]["exposure_counts"] for r in rr), "four-way exposures")
        require(rr[0]["fit"]["chronology_sha256"] == rr[2]["fit"]["chronology_sha256"]
                and rr[1]["fit"]["chronology_sha256"] == rr[3]["fit"]["chronology_sha256"]
                and rr[0]["fit"]["chronology_sha256"] != rr[1]["fit"]["chronology_sha256"], "chronology pairing")
        for lang in ("en","ja"):
            for a,b in ((0,2),(1,3)):
                rate_contrasts.append(contrast(rr[a],rr[b],mm[a],mm[b],data,lang,parent))
            oc = [contrast(rr[a],rr[b],mm[a],mm[b],data,lang,parent) for a,b in ((0,1),(2,3))]
            order_contrasts.extend(oc)
            interactions.append(dict(seed=rr[0]["seed"], language=lang,
                standard_disagreements=oc[0]["disagreements"], lower_disagreements=oc[1]["disagreements"],
                disagreement_delta=oc[1]["disagreements"]-oc[0]["disagreements"],
                standard_worst_accuracy=min(oc[0]["left_accuracy"],oc[0]["right_accuracy"]),
                lower_worst_accuracy=min(oc[1]["left_accuracy"],oc[1]["right_accuracy"])))
    by_rate = {rate:all(r["passed"] for r in results if r["arm"].startswith(rate+"_")) for rate in RATES}
    summary = dict(models=20, seed_results=results,
        seed_pass_counts={a:sum(r["passed"] for r in results if r["arm"] == a) for a in ARMS},
        rate_joint_pass=by_rate, candidate_gate=by_rate["lower"], rate_contrasts=rate_contrasts,
        order_contrasts=order_contrasts, interactions=interactions, train_steps=16000, training_rows=768000,
        model_forward_calls=16480, row_presentations=871680, core_forward_calls=65920,
        checkpoint_bundle_loads=1, model_state_loads=20, new_checkpoint_writes=1, all_replays=True, all_pairs_matched=True)
    return measurements, summary


def load_parent(path):
    parent, *_, audit = context(); path = Path(path).resolve()
    require(audit.sha(path) == PARENT_SHA, "parent summary hash")
    payload, measurements = parent.verify_artifacts(path.parent, PARENT_EXECUTION)
    require(payload["commit_sha"] == PARENT_EXECUTION and payload["status"] == "FAIL" and
            payload["validation_summary"]["seed_pass_counts"] == {"forward_blocks":0,"reverse_blocks":2}, "accepted C262 negative")
    require({x["file"]:x["sha256"] for x in payload["artifacts"]} == PARENT_ARTIFACTS and len(measurements) == 10, "parent artifacts")
    return payload


def validate_registration(source_count, input_count):
    actual = digest(manifest())
    print(f"registration_check = source_pins:{source_count}; protected_inputs:{input_count}; manifest_sha256:{actual}", flush=True)
    require((source_count,input_count) == (424,710), f"counts expected=(424, 710) actual=({source_count}, {input_count})")
    require(actual == MANIFEST_SHA, f"manifest expected={MANIFEST_SHA} actual={actual}")


def precheck(path, root):
    *_, factory, audit = context(); path = Path(path).resolve(); root = Path(root)
    payload = load_parent(path); pins, protected = dict(payload["source_blobs"]), dict(payload["input_sha256"])
    for name,wanted in protected.items():
        require(Path(name).is_file() and audit.sha(name) == wanted, "changed input:"+name)
    for name,wanted in pins.items():
        require(audit.git(root,"rev-parse","HEAD:"+name).decode().strip() == wanted, "changed source:"+name)
    for child,wanted in [(path,PARENT_SHA)] + [(audit.safe_child(path.parent,x["file"]),x["sha256"]) for x in payload["artifacts"]]:
        name = str(child.resolve()); require(name not in protected, "duplicate parent input"); protected[name] = wanted
    for name in OWN:
        require(name not in pins, "OWN collision"); pins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-9]|26[0-2])_[^/]+)\.py"
    deps = set(factory.LM_SOURCES) | {n for n in payload["source_blobs"] if re.fullmatch(pattern,n)} | {OWN[0]}
    require(len(deps) == 39 and deps <= set(pins), "direct dependencies")
    protected.update(audit.protect_tree_files(root,pins)); validate_registration(len(pins),len(protected))
    return pins, protected


def load_bundle(path):
    value = torch.load(path, map_location="cpu", weights_only=True)
    require(set(value) == {"schema","identities","states"} and value["schema"] == "fold-c263-rate-models-v1", "bundle schema")
    require(value["identities"] == [list(x) for x in identities()] and len(value["states"]) == 20, "bundle identities")
    return value["states"]


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE and p["diagnostic_execution_valid"] is True, "result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"])) == (424,710) and set(OWN) <= set(p["source_blobs"]), "protection")
    require(len(p["artifacts"]) == 6 and {x["file"] for x in p["artifacts"]} == OUTPUTS, "outputs")
    s = p["validation_summary"]
    for k,v in dict(models=20,train_steps=16000,training_rows=768000,model_forward_calls=16480,row_presentations=871680,
                    core_forward_calls=65920,checkpoint_bundle_loads=1,model_state_loads=20,new_checkpoint_writes=1).items():
        require(type(s[k]) is int and s[k] == v, "workload:"+k)
    results = s["seed_results"]
    require([(r["seed"],r["arm"]) for r in results] == identities() and all(type(r["passed"]) is bool for r in results), "result coverage")
    by_rate = {rate:all(r["passed"] for r in results if r["arm"].startswith(rate+"_")) for rate in RATES}
    require(s["rate_joint_pass"] == by_rate and s["candidate_gate"] is by_rate["lower"]
            and s["seed_pass_counts"] == {a:sum(r["passed"] for r in results if r["arm"] == a) for a in ARMS}, "gate accounting")
    require((len(s["rate_contrasts"]),len(s["order_contrasts"]),len(s["interactions"])) == (20,20,10), "contrasts")
    require(s["all_replays"] is True and s["all_pairs_matched"] is True and p["status"] == ("PASS" if s["candidate_gate"] else "FAIL"), "status/integrity")
    require(all(p[k] is False for k in ("production_adoption","gate_f_candidate","learning_rate_benefit_claim","core_superiority_claim","general_language_claim"))
            and p["network_calls"] == 0, "scope")


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == 147, "parent modules")
    return names + ["tests_lm.test_v05_c263_learning_rate_order"]


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]
    require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1, "test IDs")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require((len(tests),len(kept)) == (3478,3477), "suite counts")
    return unittest.TestSuite(kept)


def run(*, c262_summary, output_dir, expected_head):
    parent,c260,trainer,base,orders,aligned,reader,factory,audit = context()
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip() == expected_head, "HEAD")
        require(audit.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss", "branch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(), "dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected = precheck(c262_summary,root)
    parts = base.dataset(); data = dict(original=parts, extra=orders.novel_dataset(parts))
    require(all(digest(data[k]) == manifest()[k+"_dataset_sha256"] for k in data), "task hashes")
    tokens,targets = trainer.training_tables(parts,factory,orders)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=False); records,states = [],[]
    for seed in SEEDS:
        initial = base.make_model(factory.new_model(seed),"aligned_precore_read",seed,aligned,reader)
        initial_sha = base.fingerprint(initial)
        for arm in ARMS:
            print(f"[C263] model={len(records)+1}/20 seed={seed} arm={arm}", flush=True)
            r,state = train_one(copy.deepcopy(initial),seed,arm,data,tokens,targets,c260,trainer,base,orders,factory)
            require(r["initial_sha256"] == initial_sha and base.fingerprint(initial) == initial_sha, "initial template")
            records.append(r); states.append(state)
    torch.save(dict(schema="fold-c263-rate-models-v1", identities=[list(x) for x in identities()], states=states), out/"trained-models.pt")
    for r,state in zip(records,load_bundle(out/"trained-models.pt"),strict=True):
        model = base.make_model(factory.new_model(r["seed"]),"aligned_precore_read",r["seed"],aligned,reader)
        parent.replay_one(model,state,r,data,c260,trainer,base,orders,factory)
    measurements,summary = analyze(records,data,parent,c260,base,orders)
    torch.save(dict(schema="fold-c263-rate-eval-v1", records=records), out/"evaluations.pt")
    for name,value in (("rate-plan.json",manifest()),("dataset.json",data),("measurements.json",measurements),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n, sha256=audit.sha(out/n), serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard(); precheck(c262_summary,root)
    for name,wanted in protected.items():
        require(audit.sha(name) == wanted, "modified input")
    p = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        production_adoption=False,gate_f_candidate=False,learning_rate_benefit_claim=False,core_superiority_claim=False,general_language_claim=False,network_calls=0)
    validate_result(p); (out/"summary.json").write_bytes(blob(p))
    print("=== C263 RESULT ===", flush=True); print(blob(p).decode(), flush=True)
    return p


def verify_artifacts(output_dir, expected_head):
    parent,c260,_,base,orders,_,_,_,audit = context(); out = Path(output_dir); p = audit.read_json(out/"summary.json")
    validate_result(p); require(p["commit_sha"] == expected_head, "saved HEAD")
    for name,wanted in p["input_sha256"].items():
        require(audit.sha(name) == wanted, "postcheck input")
    for x in p["artifacts"]:
        child = audit.safe_child(out,x["file"])
        require(audit.sha(child) == x["sha256"] and child.stat().st_size == x["serialized_bytes"], "output bytes")
    data = audit.read_json(out/"dataset.json"); value = torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
    require(set(value) == {"schema","records"} and value["schema"] == "fold-c263-rate-eval-v1", "evaluation schema")
    measurements,summary = analyze(value["records"],data,parent,c260,base,orders)
    for name,item in (("rate-plan.json",manifest()),("measurements.json",measurements),("validation-summary.json",summary)):
        require(audit.read_json(out/name) == item, "persisted replay:"+name)
    require(p["validation_summary"] == summary, "saved summary")
    return p,measurements


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("c262-summary","output-dir"):
        p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--expected-head",required=True)
    run(**vars(p.parse_args()))


if __name__ == "__main__":
    main()
