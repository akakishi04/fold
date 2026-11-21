"""C259: paired two-order versus six-order training of the unchanged aligned reader."""
from __future__ import annotations
import argparse
from collections import Counter
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
from torch.nn import functional as F

EXPERIMENT_ID = "C259-v5b-paired-order-coverage-training"
STAGE = "V5-B-PAIRED-ORDER-COVERAGE-TRAINING"
BASE = "db8fe078766353e3a3d8217eb6b595c22f10cfcd"
PARENT_EXECUTION = "e31d4c28a00bc11fb5db3c2ba1b093e4eae15538"
PARENT_SHA = "f6ccc7dc1b8c60c1f1e6bc7587bd9853eeb6bea6e1f7a010fd99de068bbd0ecc"
PARENT_ARTIFACTS = {
    "audit-plan.json": "a4f2cad192bd56dd73d867caf8453084cdd85e8e0f10f9d2496bfaa4a6c08aef",
    "query-position-cells.json": "d4bb64ac620e235b389447b52b4dea88b69466e4f77a3db8e363a0dfa330dea5",
    "row-attribution.json": "b94b0224805512c049d3a6dfcee23c682dc700c33df705a750a4f71ea8475e85",
    "signature-summary.json": "e40bfcd11890866e1f02e77b662151a2d414df35b6c7d12c357afd9fa93b1644",
    "validation-summary.json": "17d130b1b26545457a9419727548507d480aead01b02c8b6100d251969d95620",
}
SEEDS = (259001, 259002, 259003, 259004, 259005)
ARMS = ("two_order", "six_order")
SPLITS, VIEWS = ("TRAIN", "HOLDOUT"), ("normal", "evidence_blind", "query_blind")
ORDERS = ((0,1,2), (2,1,0), (0,2,1), (1,0,2), (1,2,0), (2,0,1))
STEPS, BATCH, TOL = 800, 48, 1e-9
OWN = ("fold_lm/v05_benchmarks/model_c259_order_coverage_training.py",
       "tests_lm/test_v05_c259_order_coverage_training.py", "tools/run_c259.ps1", "tools/invoke_c259.ps1",
       "docs/experiment-ledger-addendum-c259-preregistration.md", "docs/v5b-order-coverage-training-v0.1.md")
OUTPUTS = {"coverage-plan.json", "dataset.json", "trained-models.pt", "evaluations.pt", "measurements.json", "validation-summary.json"}
EXCLUDED = "tests_lm.test_v05_c204_live_v2_mixed_channel_loop.C204Tests.test_33_active_dispatcher_resolves_current_formal_state"
MANIFEST_SHA = "2ec7894fe267260d8bc16d1275d7407833c0592e0910f8149639f90c830bfdcb"


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
    from fold_lm.v05_benchmarks import model_c258_saved_middle_slot_audit as parent
    orders, base, factory, audit = parent.context()
    _, aligned, reader, _, _ = base.context()
    return parent, base, orders, aligned, reader, factory, audit


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA, parent_artifacts=PARENT_ARTIFACTS,
        seeds=list(SEEDS), arms=list(ARMS), orders=[list(p) for p in ORDERS],
        original_dataset_sha256="ca6eb1943b24cc73cbc5f4dd4af7008c2be11ed8e2c53e79a768593a67e3342b",
        extra_dataset_sha256="9ee8868f46838884874f44ea1d0f03fc481672aea8f9044eb764a81220514052",
        changed="training fact-order coverage only; same actual C252 aligned reader in both arms",
        initialization="one fresh full wrapper copied into both arms within seed; no accepted checkpoint",
        sampling="C256 logical144 rows; seed+256000+epoch randperm; three48-row blocks; paired base rows",
        order_schedule="two_order pair0; six_order pair(epoch mod3); each row selects its original order bit",
        coverage="every9 complete steps presents each base assignment/language/query in all6 orders once; fixed800-step tail",
        steps=800, batch=48, lr=.005, clip=1., optimizer="AdamW", betas=[.9,.999], eps=1e-8, weight_decay=0.,
        parameters=14256, dtype="CPU float64", threads=2, deterministic=True,
        primary="all five six_order seeds pass C257-equivalent final criteria on both assignment splits/languages",
        gate=dict(original_accuracy=.90, original_order_pair=.80, query_triplet=.80,
                  extra_accuracy=.90, evidence_drop=.35, query_drop=.35, six_order=.80),
        comparisons="paired HOLDOUT all6 accuracy and six-order consistency; descriptive, not a rescue gate",
        models=10, train_steps=8000, answer_presentations=384000, model_forward_calls=8240,
        row_presentations=435840, evaluation_forwards=240, checkpoint_bundle_loads=1,
        model_state_loads=10, new_checkpoint_writes=1, checkpoint_states=10, artifacts=6,
        source_pins=400, protected_inputs=659, direct_dependencies=35, own_tests=24,
        modules=144, loaded_tests=3382, focused_tests=3381, excluded_test=EXCLUDED,
        replay_tolerance=TOL, network_calls=0, gate_f_candidate=False, production_adoption=False,
        unseen_order_transfer_claim=False, causal_mechanism_claim=False, general_language_claim=False)


def training_plan(seed, step, arm):
    require(seed in SEEDS and type(step) is int and 0 <= step < STEPS and arm in ARMS, "batch identity")
    epoch, block = divmod(step, 3)
    generator = torch.Generator(device="cpu").manual_seed(seed + 256000 + epoch)
    indices = torch.randperm(144, generator=generator)[block*BATCH:(block+1)*BATCH]
    return indices, 0 if arm == "two_order" else epoch % 3


def training_tables(parts, factory, orders):
    rows = parts["TRAIN"]
    require(len(rows) == 144 and len({r["id"] for r in rows}) == 144, "TRAIN logical rows")
    tables = []
    for pair in range(3):
        rendered = [orders.render(dict(r, permutation=list(ORDERS[2*pair+r["order"]])), "normal").encode() for r in rows]
        tables.append(torch.stack([factory.prefix_tensor(text) for text in rendered]))
    tokens = torch.stack(tables)
    targets = torch.tensor([r["target"] for r in rows], dtype=torch.int64)
    require(tokens.shape == (3,144,48) and tokens.dtype == torch.int64 and targets.shape == (144,), "training tensors")
    return tokens, targets


def fit(model, tokens, targets, seed, arm):
    require(tokens.shape == (3,144,48) and targets.shape == (144,), "fit inputs")
    torch.manual_seed(seed + 259000)
    optimizer = torch.optim.AdamW(model.parameters(), lr=.005, betas=(.9,.999), eps=1e-8, weight_decay=0.)
    model.train(); trace = hashlib.sha256(); pairs = Counter(); first = last = None; start = time.perf_counter()
    for step in range(STEPS):
        ids, pair = training_plan(seed, step, arm)
        trace.update(ids.numpy().tobytes()); pairs[pair] += 1
        optimizer.zero_grad(set_to_none=True)
        logits = model(tokens[pair,ids], torch.zeros(BATCH, dtype=torch.int64))
        loss = F.cross_entropy(logits, targets[ids]); require(bool(torch.isfinite(loss)), "nonfinite training loss")
        loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1., error_if_nonfinite=True); optimizer.step()
        last = float(loss.detach()); first = last if first is None else first
        if (step+1) % 200 == 0:
            print(f"[C259] seed={seed} arm={arm} step={step+1}/{STEPS} answer_nll={last:.6f}", flush=True)
    model.eval()
    return dict(steps=STEPS, answer_presentations=STEPS*BATCH, first_loss=first, last_loss=last,
                logical_batch_sha256=trace.hexdigest(), order_pair_updates=[pairs[i] for i in range(3)],
                fit_seconds=time.perf_counter()-start)


def evaluate(model, parts, extra, base, orders, factory):
    before = base.fingerprint(model); model.eval()
    _, _, original = base.evaluate(model, parts, factory)
    additional = orders.evaluate_new(model, extra, factory)
    require(base.fingerprint(model) == before, "evaluation mutation")
    return dict(original=original, extra=additional)


def train_one(model, parts, extra, tokens, targets, seed, arm, base, orders, factory):
    require(sum(p.numel() for p in model.parameters()) == 14256, "parameter count")
    initial = base.fingerprint(model); back = base.fingerprint(model.backbone); head = base.fingerprint(model.read)
    counts = [0,0]
    def counted(module, args, output):
        counts[0] += 1; counts[1] += len(args[0])
    handle = model.register_forward_hook(counted)
    try:
        fitting = fit(model, tokens, targets, seed, arm)
        raw = evaluate(model, parts, extra, base, orders, factory)
    finally:
        handle.remove()
    require(counts == [812,40992], "training/final workload")
    final = base.fingerprint(model)
    record = dict(seed=seed, arm=arm, parameters=14256, initial_sha256=initial, backbone_initial_sha256=back,
        final_sha256=final, weights_changed=final != initial,
        backbone_changed=base.fingerprint(model.backbone) != back, head_changed=base.fingerprint(model.read) != head,
        fit=fitting, forward_calls=counts[0], row_presentations=counts[1], raw=raw)
    return record, {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}


def replay_one(model, state, record, parts, extra, base, orders, factory):
    model.load_state_dict(state, strict=True); model.eval()
    require(base.fingerprint(model) == record["final_sha256"], "strict final-state identity")
    counts = [0,0]
    def counted(module, args, output):
        counts[0] += 1; counts[1] += len(args[0])
    handle = model.register_forward_hook(counted)
    try:
        raw = evaluate(model, parts, extra, base, orders, factory)
    finally:
        handle.remove()
    error = max(orders.replay(raw[k][s][v], record["raw"][k][s][v]) for k in ("original","extra") for s in SPLITS for v in VIEWS)
    require(counts == [12,2592] and base.fingerprint(model) == record["final_sha256"], "replay workload/state")
    record.update(checkpoint_roundtrip=True, reload_max_error=error, replay_forward_calls=12, replay_row_presentations=2592)


def analyze(records, parts, extra, base, orders):
    require([(r["seed"],r["arm"]) for r in records] == identities(), "record identities")
    require(parts == base.dataset() and extra == orders.novel_dataset(parts), "dataset identity")
    measurements = []; seeds = []
    for r in records:
        require(r["parameters"] == 14256 and all(r[k] is True for k in ("weights_changed","backbone_changed","head_changed","checkpoint_roundtrip")), "model integrity")
        require((r["fit"]["steps"],r["fit"]["answer_presentations"],r["forward_calls"],r["row_presentations"],r["replay_forward_calls"],r["replay_row_presentations"]) == (800,38400,812,40992,12,2592), "record workload")
        require(r["fit"]["order_pair_updates"] == ([800,0,0] if r["arm"] == "two_order" else [267,267,266]), "order schedule")
        require(type(r["reload_max_error"]) in (int,float) and math.isfinite(r["reload_max_error"]) and 0 <= r["reload_max_error"] <= TOL, "replay error")
        raw = r["raw"]; require(set(raw) == {"original","extra"}, "evaluation stages")
        old = {}; new = {}; six = {}; accuracy = {}
        for stage in raw:
            require(set(raw[stage]) == set(SPLITS) and all(set(raw[stage][s]) == set(VIEWS) for s in SPLITS), "split/view coverage")
        for split in SPLITS:
            old[split], op = base.metrics(parts[split], raw["original"][split])
            new[split], np = orders.new_metrics(extra[split], raw["extra"][split])
            six[split] = orders.six_order_metrics(parts[split], extra[split], op["normal"], np["normal"])
            accuracy[split] = {}
            for lang in ("en","ja"):
                correct = sum(pred == row["target"] for rows,preds in ((parts[split],op["normal"]),(extra[split],np["normal"])) for row,pred in zip(rows,preds,strict=True) if row["language"] == lang)
                accuracy[split][lang] = dict(correct=correct, rows=216, accuracy=correct/216)
        original_pass = all(base.cell_pass(m) for v in old.values() for m in v.values())
        extra_pass = all(orders.new_cell_pass(c) for cells in new.values() for c in cells)
        six_pass = all(m["accuracy"] >= .8 for v in six.values() for m in v.values())
        passed = original_pass and extra_pass and six_pass
        reason = "ORIGINAL_CRITERIA_MISS" if not original_pass else "EXTRA_ORDER_MISS" if not extra_pass else "SIX_ORDER_MISS" if not six_pass else "PASS"
        seeds.append(dict(seed=r["seed"],arm=r["arm"],passed=passed,outcome=reason))
        measurements.append(dict(seed=r["seed"],arm=r["arm"],original=old,extra_orders=new,six_order=six,
            all_order_accuracy=accuracy,passed=passed,outcome=reason,fit=r["fit"],reload_max_error=r["reload_max_error"]))
    comparisons = []
    for i in range(0,10,2):
        control,treatment = records[i:i+2]; cm,tm = measurements[i:i+2]
        require(control["initial_sha256"] == treatment["initial_sha256"] and control["backbone_initial_sha256"] == treatment["backbone_initial_sha256"], "paired initial state")
        require(control["fit"]["logical_batch_sha256"] == treatment["fit"]["logical_batch_sha256"], "paired base-row schedule")
        for lang in ("en","ja"):
            ca,ta = cm["all_order_accuracy"]["HOLDOUT"][lang]["accuracy"],tm["all_order_accuracy"]["HOLDOUT"][lang]["accuracy"]
            cs,ts = cm["six_order"]["HOLDOUT"][lang]["accuracy"],tm["six_order"]["HOLDOUT"][lang]["accuracy"]
            comparisons.append(dict(seed=control["seed"],language=lang,control_accuracy=ca,treatment_accuracy=ta,
                accuracy_delta=ta-ca,control_six_order=cs,treatment_six_order=ts,six_order_delta=ts-cs))
    summary = dict(models=10,candidate_gate=all(r["passed"] for r in seeds if r["arm"] == "six_order"),
        seed_results=seeds,seed_pass_counts={a:sum(r["passed"] for r in seeds if r["arm"] == a) for a in ARMS},
        comparisons=comparisons,train_steps=8000,answer_presentations=384000,model_forward_calls=8240,
        row_presentations=435840,checkpoint_bundle_loads=1,model_state_loads=10,new_checkpoint_writes=1,
        all_replays=True,all_pairs_matched=True,all_weights_changed=True)
    return measurements,summary


def validate_parent(payload, parent):
    parent.validate_result(payload)
    require(payload["commit_sha"] == PARENT_EXECUTION and payload["status"] == "PASS", "accepted diagnostic identity")
    require(payload["capability_pass_claim"] is False and payload["causal_mechanism_claim"] is False, "parent non-claims")
    require({a["file"]:a["sha256"] for a in payload["artifacts"]} == PARENT_ARTIFACTS, "parent artifacts")


def load_parent(path):
    parent,_,_,_,_,_,audit = context(); path = Path(path).resolve()
    require(audit.sha(path) == PARENT_SHA, "parent summary hash")
    payload = audit.read_json(path); validate_parent(payload,parent)
    for item in payload["artifacts"]:
        child = audit.safe_child(path.parent,item["file"])
        require(audit.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"], "parent artifact bytes")
    saved = audit.read_json(path.parent/"validation-summary.json")
    require(saved == payload["validation_summary"] and saved["attributed_rows"] == 8640, "parent summary contract")
    require(audit.read_json(path.parent/"audit-plan.json") == parent.manifest(), "parent plan contract")
    return saved


def validate_registration(source_count,input_count):
    actual = digest(manifest())
    print(f"registration_check = source_pins:{source_count}; protected_inputs:{input_count}; manifest_sha256:{actual}",flush=True)
    require((source_count,input_count) == (400,659), f"source/input counts: expected=(400, 659) actual=({source_count}, {input_count})")
    require(actual == MANIFEST_SHA, f"manifest hash: expected={MANIFEST_SHA} actual={actual}")


def precheck(parent_summary,root):
    parent,_,_,_,_,factory,audit = context(); path = Path(parent_summary).resolve(); root = Path(root)
    load_parent(path); payload = audit.read_json(path)
    pins,protected = dict(payload["source_blobs"]),dict(payload["input_sha256"])
    for name,wanted in protected.items():
        require(Path(name).is_file() and audit.sha(name) == wanted, "changed input:"+name)
    for name,wanted in pins.items():
        require(audit.git(root,"rev-parse","HEAD:"+name).decode().strip() == wanted, "changed source:"+name)
    for child,wanted in [(path,PARENT_SHA)]+[(audit.safe_child(path.parent,a["file"]),a["sha256"]) for a in payload["artifacts"]]:
        name = str(child.resolve()); require(name not in protected,"parent input duplicate"); protected[name] = wanted
    for name in OWN:
        require(name not in pins,"OWN collision"); pins[name] = audit.git(root,"rev-parse","HEAD:"+name).decode().strip()
    pattern = r"fold_lm/v05_benchmarks/(?:gate_f_c230_prepared_capsule|model_c(?:23[1-9]|24[0-9]|25[0-8])_[^/]+)\.py"
    deps = set(factory.LM_SOURCES) | {n for n in payload["source_blobs"] if re.fullmatch(pattern,n)} | {OWN[0]}
    require(len(deps) == 35 and deps <= set(pins),"direct dependency coverage")
    protected.update(audit.protect_tree_files(root,pins)); validate_registration(len(pins),len(protected))
    return pins,protected


def load_bundle(path):
    archive = torch.load(path,map_location="cpu",weights_only=True)
    require(set(archive) == {"schema","identities","states"} and archive["schema"] == "fold-c259-order-coverage-models-v1", "checkpoint schema")
    require(archive["identities"] == [list(x) for x in identities()] and len(archive["states"]) == 10,"checkpoint identities")
    return archive["states"]


def validate_result(payload):
    require(payload["experiment_id"] == EXPERIMENT_ID and payload["stage"] == STAGE and payload["diagnostic_execution_valid"] is True,"result identity")
    require((len(payload["source_blobs"]),len(payload["input_sha256"])) == (400,659) and set(OWN) <= set(payload["source_blobs"]),"protection")
    require(len(payload["artifacts"]) == 6 and {a["file"] for a in payload["artifacts"]} == OUTPUTS,"artifact coverage")
    s = payload["validation_summary"]
    for k,v in dict(models=10,train_steps=8000,answer_presentations=384000,model_forward_calls=8240,row_presentations=435840,checkpoint_bundle_loads=1,model_state_loads=10,new_checkpoint_writes=1).items():
        require(type(s[k]) is int and s[k] == v,"workload:"+k)
    require([(r["seed"],r["arm"]) for r in s["seed_results"]] == identities() and len(s["comparisons"]) == 10,"summary coverage")
    require(type(s["candidate_gate"]) is bool and payload["status"] == ("PASS" if s["candidate_gate"] else "FAIL"),"status")
    require(all(s[k] is True for k in ("all_replays","all_pairs_matched","all_weights_changed")),"integrity flags")
    require(all(payload[k] is False for k in ("gate_f_candidate","production_adoption","unseen_order_transfer_claim","causal_mechanism_claim")) and payload["network_calls"] == 0,"scope")


def regression_modules(root):
    names = context()[0].regression_modules(root)
    require(len(names) == len(set(names)) == 143,"parent modules")
    return names+["tests_lm.test_v05_c259_order_coverage_training"]


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def regression_suite(root):
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]; require(len(ids) == len(set(ids)) and ids.count(EXCLUDED) == 1,"suite IDs")
    kept = [t for t in tests if t.id() != EXCLUDED]
    require((len(tests),len(kept)) == (3382,3381),"suite counts")
    return unittest.TestSuite(kept)


def run(*,c258_summary,output_dir,expected_head):
    _,base,orders,aligned,reader,factory,audit = context(); root = Path(__file__).resolve().parents[2]
    def guard():
        require(audit.git(root,"rev-parse","HEAD").decode().strip() == expected_head,"HEAD")
        require(audit.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss","branch")
        require(not audit.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    pins,protected = precheck(c258_summary,root); parts = base.dataset(); extra = orders.novel_dataset(parts)
    tokens,targets = training_tables(parts,factory,orders)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False); records = []; states = []
    for seed in SEEDS:
        initial = base.make_model(factory.new_model(seed),"aligned_precore_read",seed,aligned,reader)
        initial_sha = base.fingerprint(initial)
        for arm in ARMS:
            require(base.fingerprint(initial) == initial_sha,"initial template mutation")
            print(f"[C259] model={len(records)+1}/10 seed={seed} arm={arm}",flush=True)
            record,state = train_one(copy.deepcopy(initial),parts,extra,tokens,targets,seed,arm,base,orders,factory)
            require(record["initial_sha256"] == initial_sha,"paired initialization")
            records.append(record); states.append(state)
    torch.save(dict(schema="fold-c259-order-coverage-models-v1",identities=[list(x) for x in identities()],states=states),out/"trained-models.pt")
    for record,state in zip(records,load_bundle(out/"trained-models.pt"),strict=True):
        model = base.make_model(factory.new_model(record["seed"]),"aligned_precore_read",record["seed"],aligned,reader)
        replay_one(model,state,record,parts,extra,base,orders,factory)
    measurements,summary = analyze(records,parts,extra,base,orders)
    torch.save(dict(schema="fold-c259-order-coverage-eval-v1",records=records),out/"evaluations.pt")
    for name,value in (("coverage-plan.json",manifest()),("dataset.json",dict(original=parts,extra=extra)),("measurements.json",measurements),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=n,sha256=audit.sha(out/n),serialized_bytes=(out/n).stat().st_size) for n in sorted(OUTPUTS)]
    guard(); precheck(c258_summary,root)
    for name,wanted in protected.items():
        require(audit.sha(name) == wanted,"modified input")
    payload = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,status="PASS" if summary["candidate_gate"] else "FAIL",
        diagnostic_execution_valid=True,source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,production_adoption=False,unseen_order_transfer_claim=False,causal_mechanism_claim=False,network_calls=0)
    validate_result(payload); (out/"summary.json").write_bytes(blob(payload))
    print("=== C259 RESULT ===",flush=True); print(blob(payload).decode(),flush=True)
    return payload


def verify_artifacts(output_dir,expected_head):
    _,base,orders,_,_,_,audit = context(); out = Path(output_dir); payload = audit.read_json(out/"summary.json")
    validate_result(payload); require(payload["commit_sha"] == expected_head,"saved HEAD")
    for name,wanted in payload["input_sha256"].items():
        require(audit.sha(name) == wanted,"postcheck input")
    for item in payload["artifacts"]:
        child = audit.safe_child(out,item["file"])
        require(audit.sha(child) == item["sha256"] and child.stat().st_size == item["serialized_bytes"],"output bytes")
    data = audit.read_json(out/"dataset.json")
    archive = torch.load(out/"evaluations.pt",map_location="cpu",weights_only=True)
    require(set(archive) == {"schema","records"} and archive["schema"] == "fold-c259-order-coverage-eval-v1","evaluation archive schema")
    measurements,summary = analyze(archive["records"],data["original"],data["extra"],base,orders)
    for name,value in (("coverage-plan.json",manifest()),("measurements.json",measurements),("validation-summary.json",summary)):
        require(audit.read_json(out/name) == value,"persisted recomputation:"+name)
    require(payload["validation_summary"] == summary,"saved summary replay")
    return payload,measurements


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("c258-summary","output-dir"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True)
    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
