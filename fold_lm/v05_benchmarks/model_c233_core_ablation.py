"""C233: same-backbone GRU-only ablation against accepted C232 checkpoints.

A capacity-reducing diagnostic, not a parameter-matched architecture contest.
Only the ablation is newly trained; accepted model weights and data remain fixed.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import time
import unittest

import torch
from torch import nn
from torch.nn import functional as F

EXPERIMENT_ID = "C233-v5b-backbone-matched-core-ablation"
STAGE = "V5-B-BACKBONE-MATCHED-CORE-ABLATION"
BASE = "b0823af9f073c891ca6fa556c3bd93da0c2510cb"
PARENT_EXECUTION = "5fced21f02448e5b1047ef661186ce9b5c6bdb02"
PARENT_SHA = "df75e3956a6bfaa37aaebdb12f3d189a10010576f0d9fa8709e5e399e1da75d2"
PARENT_VALIDATION_SHA = "d7084ad67ee1072aa1c985c5d62ae958ce7771994db18bd29530442486e04ded"
PARENT_MEASUREMENTS_SHA = "ca14020688c9993edde9d176d596c7ffc1704ddbf78ab55520abbc48f5351c04"
PARENT_CHECKPOINT_SHA = "c26e7bb71a9e9a882561165ef91e94b9c2ff257a0d39aa8166654c995e042a7b"
DATA_SHA = "1a1b09c80c3877c662ee43bf91fb00b7a762d20a7b6b3f455f5ee208c7a79200"
SEEDS = (232001, 232002, 232003)  # Paired with the already accepted C232 initializations.
STEPS, BATCH, LR, CLIP, TOL = 400, 32, 0.005, 1.0, 1e-9
SHARED = ("byte_embedding", "local_encoder", "readout_norm", "decoder")
FULL_PARAMETERS, BASELINE_PARAMETERS = 13488, 10160
MANIFEST_SHA = "01459cd555cc15193b1289767cd824d159999faff130d537d16c5895f3f83d39"
OWN = (
    "fold_lm/v05_benchmarks/model_c233_core_ablation.py",
    "tests_lm/test_v05_c233_core_ablation.py",
    "tools/run_c233.ps1", "tools/invoke_c233.ps1",
    "docs/experiment-ledger-addendum-c233-preregistration.md",
    "docs/v5b-backbone-matched-core-ablation-v0.1.md",
)
OUTPUTS = {"comparison-plan.json", "baseline-models.pt", "comparisons.json",
           "replay-audit.json", "validation-summary.json"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c232_bilingual_learning as parent
    return parent


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
        parent_validation_sha256=PARENT_VALIDATION_SHA,
        parent_measurements_sha256=PARENT_MEASUREMENTS_SHA,
        parent_checkpoint_sha256=PARENT_CHECKPOINT_SHA, data_sha256=DATA_SHA,
        seeds=list(SEEDS), changed="remove fixed-routing iterative core; retrain remaining backbone",
        common_initial_weights=list(SHARED), full_parameters=FULL_PARAMETERS,
        baseline_parameters=BASELINE_PARAMETERS, parameter_matched=False,
        training="baseline only, from matching C232 common initialization, not trained full weights",
        steps_per_seed=STEPS, batch_size=BATCH, lr=LR, gradient_clip=CLIP,
        optimizer="AdamW", betas=[0.9,0.999], eps=1e-8, weight_decay=0.0,
        sampler="TRAIN byte rows with replacement; CPU generator seed+1000, as C232",
        total_new_training_steps=1200, total_new_byte_presentations=38400,
        dtype="float64", device="cpu", threads=2, deterministic_algorithms=True,
        eval_split="unchanged C232 four held-out pairs; diagnostic reuse, not fresh confirmation",
        selection="final step400; no tuning, early stop, replacement seeds or checkpoint selection",
        baseline_qualification="TRAIN loss decreases; each language EVAL beats own initial and unigram",
        core_advantage="full BPB strictly lower than qualified baseline in all six seed/language cells",
        replay_tolerance=TOL, generation="same C231 four-byte greedy replay, descriptive only",
        full_retraining_steps=0, gate_f_candidate=False, general_language_claim=False,
        speed_claim=False, capacity_confound=True, network_calls=0)


class GRUOnly(nn.Module):
    """Same embedding/GRU/norm/decoder, with no iterative core or dormant core weights."""
    def __init__(self, source):
        super().__init__()
        self.config = copy.deepcopy(source.config)
        require(self.config.width == 16 and self.config.max_tokens == 48, "backbone config")
        for name in SHARED:
            setattr(self, name, copy.deepcopy(getattr(source, name)))
        require(sum(p.numel() for p in self.parameters()) == BASELINE_PARAMETERS, "baseline size")

    def forward(self, tokens, tasks):
        require(isinstance(tokens, torch.Tensor) and isinstance(tasks, torch.Tensor), "tensor inputs")
        require(tokens.dtype == tasks.dtype == torch.int64 and tokens.ndim == 2
                and tokens.shape[1] == 48 and tokens.shape[0] > 0
                and tasks.shape == (tokens.shape[0],) and tokens.device == tasks.device,
                "input shape/dtype/device")
        require(bool(((tokens >= 0) & (tokens < 259)).all()) and bool((tasks == 0).all()),
                "byte IDs or NEXT-only task")
        valid = tokens != 256
        context, _ = self.local_encoder(self.byte_embedding(tokens))
        context = context * valid.unsqueeze(-1).to(context.dtype)
        eos_index = valid.sum(dim=1) - 1
        pooled = context[torch.arange(tokens.shape[0], device=tokens.device), eos_index]
        return self.decoder(self.readout_norm(pooled))


def common_state(source):
    return {k: v for k, v in source.state_dict().items() if k.split(".")[0] in SHARED}


def new_baseline(source):
    model = GRUOnly(source).eval()
    wanted, actual = common_state(source), model.state_dict()
    require(set(actual) == set(wanted)
            and all(torch.equal(actual[k], wanted[k]) for k in actual), "common initialization changed")
    return model


def score_error(actual, expected):
    errors = []
    for lang, count in (("all",316),("en",164),("ja",152)):
        a, e = actual[lang], expected[lang]
        require(a["bytes"] == e["bytes"] == count, "EVAL byte count")
        for key in ("nll_sum", "bits_per_byte"):
            require(all(type(x) in (int,float) and math.isfinite(x) and x >= 0
                        for x in (a[key], e[key])), "invalid metric")
            errors.append(abs(a[key] - e[key]))
        require(abs(e["bits_per_byte"] - e["nll_sum"]/(count*math.log(2))) <= TOL,
                "saved BPB semantics")
    return max(errors)


def read_parent_measurements(path):
    parent = parent_module()
    rows = parent.audit_module().read_json(path)
    require(isinstance(rows,list) and len(rows) == 3
            and [r["seed"] for r in rows] == list(SEEDS), "C232 record identities")
    for r in rows:
        require(r["parameters"] == FULL_PARAMETERS and parent.learning_pass(r)
                and r["fit"]["steps"] == STEPS and r["fit"]["byte_presentations"] == STEPS*BATCH,
                "C232 accepted record contract")
        require(all(isinstance(r[k],str) and len(r[k]) == 64
                    for k in ("initial_sha256","final_sha256")), "parent fingerprints")
        score_error(r["final_eval"], r["final_eval"])
    return rows


def load_parent_states(path):
    bundle = torch.load(path, map_location="cpu", weights_only=True)
    require(bundle["schema"] == "fold-c232-trained-byte-models-v1"
            and bundle["seeds"] == list(SEEDS) and len(bundle["states"]) == 3,
            "C232 trained checkpoint schema")
    return bundle["states"]


def replay_full(model, state, record, tensors, eval_rows):
    parent = parent_module(); factory = parent.parent_module()
    model.load_state_dict(state, strict=True); model.eval()
    require(factory.fingerprint(model) == record["final_sha256"], "accepted full weights changed")
    metrics, _ = parent.evaluate(model, tensors)
    error = score_error(metrics, record["final_eval"])
    generated = [dict(id=r["id"], generated_hex=factory.generate(model,r["text"].encode()[:8]).hex())
                 for r in eval_rows]
    require(error <= TOL and generated == record["generation"], "accepted full replay failed")
    require(factory.fingerprint(model) == record["final_sha256"], "full evaluation changed weights")
    return metrics, error


def fit_baseline(model, train_tokens, train_targets, seed, *, steps=STEPS):
    """Same C232 optimizer/sampler recipe; only TRAIN tensors are arguments."""
    require(type(steps) is int and steps > 0 and train_tokens.shape[0] == train_targets.numel()
            and train_targets.numel() > 0, "training workload")
    sampler = torch.Generator(device="cpu").manual_seed(seed+1000)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, betas=(0.9,0.999), eps=1e-8, weight_decay=0.0)
    model.train(); first = last = None; started = time.perf_counter()
    for step in range(steps):
        indices = torch.randint(len(train_targets), (BATCH,), generator=sampler)
        optimizer.zero_grad(set_to_none=True)
        logits = model(train_tokens[indices], torch.zeros(BATCH,dtype=torch.int64))
        loss = F.cross_entropy(logits,train_targets[indices])
        require(bool(torch.isfinite(loss)), "nonfinite baseline loss")
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(model.parameters(),CLIP,error_if_nonfinite=True)
        require(bool(torch.isfinite(norm)), "nonfinite baseline gradient")
        optimizer.step()
        if first is None: first = float(loss.detach())
        last = float(loss.detach())
        if (step+1)%100 == 0:
            print(f"[C233 GRU-only] seed={seed} step={step+1}/{steps} train_batch_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=steps,byte_presentations=steps*BATCH,first_batch_nll=first,
                last_batch_nll=last,fit_wall_seconds=time.perf_counter()-started)


def baseline_qualified(r):
    return (r["weights_changed"] is True
        and r["final_train"]["all"]["bits_per_byte"] < r["initial_train"]["all"]["bits_per_byte"]
        and all(r["final_eval"][lang]["bits_per_byte"] <
                min(r["initial_eval"][lang]["bits_per_byte"],r["unigram_eval"][lang]["bits_per_byte"])
                for lang in ("en","ja")))


def summary_for(rows):
    require(len(rows) == 3 and [r["seed"] for r in rows] == list(SEEDS), "comparison seed order")
    deltas = [r["full_eval"][lang]["bits_per_byte"] - r["final_eval"][lang]["bits_per_byte"]
              for r in rows for lang in ("en","ja")]
    require(all(math.isfinite(x) for x in deltas), "nonfinite comparison")
    return dict(seeds=list(SEEDS), baseline_qualified=all(baseline_qualified(r) for r in rows),
        full_win_cells=sum(x < 0 for x in deltas), baseline_win_cells=sum(x > 0 for x in deltas),
        tied_cells=sum(x == 0 for x in deltas), delta_full_minus_baseline_bpb=deltas,
        all_replays=all(r["checkpoint_roundtrip"] and r["generation_replayed"]
                       and 0 <= r["reload_max_error"] <= TOL and 0 <= r["full_replay_error"] <= TOL
                       for r in rows),
        total_new_training_steps=sum(r["fit"]["steps"] for r in rows),
        total_new_byte_presentations=sum(r["fit"]["byte_presentations"] for r in rows),
        full_parameters=FULL_PARAMETERS, baseline_parameters=BASELINE_PARAMETERS,
        full_retraining_steps=0, parameter_matched=False, general_language_claim=False,
        gate_f_candidate=False)


def gate(s):
    return (s.get("baseline_qualified") is True and s.get("full_win_cells") == 6
        and s.get("all_replays") is True and s.get("seeds") == list(SEEDS)
        and s.get("total_new_training_steps") == 1200
        and s.get("total_new_byte_presentations") == 38400 and s.get("full_retraining_steps") == 0
        and s.get("parameter_matched") is False and s.get("general_language_claim") is False)


def precheck(c232_summary, root):
    parent = parent_module(); a = parent.audit_module(); root = Path(root)
    require(a.sha(c232_summary) == PARENT_SHA, "C232 summary changed")
    p = a.read_json(c232_summary); parent.validate_result(p)
    require(p["commit_sha"] == PARENT_EXECUTION and p["status"] == "PASS"
            and parent.gate(p["validation_summary"]), "wrong accepted C232")
    pins, protected = dict(p["source_blobs"]), dict(p["input_sha256"])
    require((len(pins),len(protected)) == (238,334), "parent counts")
    for name,wanted in protected.items():
        require(Path(name).is_file() and a.sha(name) == wanted, "changed inherited input:"+name)
    for name,wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+name).decode().strip() == wanted, "changed parent source:"+name)
    protected[str(Path(c232_summary).resolve())] = PARENT_SHA
    fixed = {"dataset.json":DATA_SHA, "measurements.json":PARENT_MEASUREMENTS_SHA,
             "trained-models.pt":PARENT_CHECKPOINT_SHA,"validation-summary.json":PARENT_VALIDATION_SHA}
    seen = set()
    for item in p["artifacts"]:
        path = a.safe_child(Path(c232_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path) == item["sha256"]
                and path.stat().st_size == item["serialized_bytes"], "parent artifact changed")
        if item["file"] in fixed:
            require(item["sha256"] == fixed[item["file"]], "deciding artifact identity"); seen.add(item["file"])
        protected[str(path.resolve())] = item["sha256"]
    require(seen == set(fixed), "missing deciding artifact")
    require((parent.SEEDS,parent.STEPS,parent.BATCH,parent.LR,parent.CLIP,parent.DATA_SHA)
            == (SEEDS,STEPS,BATCH,LR,CLIP,DATA_SHA), "parent training contract changed")
    for name in OWN:
        require(name not in pins, "OWN collides with accepted source")
        pins[name] = a.git(root,"rev-parse","HEAD:"+name).decode().strip()
    deps = set(parent.parent_module().LM_SOURCES) | {
        "fold_lm/v05_benchmarks/model_c231_byte_eval_contract.py",
        "fold_lm/v05_benchmarks/model_c232_bilingual_learning.py",
        "fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py",OWN[0]}
    require(len(deps) == 9 and deps <= set(pins), "missing deciding dependency")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected)) == (244,346), "C233 protection counts")
    require(digest(manifest()) == MANIFEST_SHA, "C233 manifest drift")
    return p,pins,protected


def regression_modules(root):
    names = parent_module().regression_modules(root)
    require(len(names) == len(set(names)) == 117, "parent module count")
    return names + ["tests_lm.test_v05_c233_core_ablation"]


def regression_suite(root):
    previous = parent_module().parent_module().parent_module()
    helper = previous.context(previous.parent_module()).backend.c205
    tests = list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids = [t.id() for t in tests]; excluded = helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
    require(all(ids.count(x) == 1 for x in excluded), "historical exclusion identity")
    kept = [t for t in tests if t.id() not in excluded]
    require((len(tests),len(kept)) == (2754,2753), "C233 regression counts")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"] == EXPERIMENT_ID and p["stage"] == STAGE
            and p["diagnostic_execution_valid"] is True, "C233 identity")
    require((len(p["source_blobs"]),len(p["input_sha256"])) == (244,346)
            and set(OWN) <= set(p["source_blobs"]), "C233 protection")
    require(len(p["artifacts"]) == 5 and {x["file"] for x in p["artifacts"]} == OUTPUTS, "C233 outputs")
    s = p["validation_summary"]
    require(s["seeds"] == list(SEEDS) and s["total_new_training_steps"] == 1200
            and s["total_new_byte_presentations"] == 38400 and s["all_replays"] is True,
            "incomplete workload or replay")
    require(p["status"] == ("PASS" if gate(s) else "FAIL"), "C233 verdict drift")
    require(p["gate_f_candidate"] is False and p["network_calls"] == 0, "scope drift")


def run(*, c232_summary, output_dir, expected_head):
    parent = parent_module(); factory = parent.parent_module(); a = parent.audit_module()
    root = Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip() == expected_head, "HEAD mismatch")
        require(a.git(root,"branch","--show-current").decode().strip() == "feat/sft-target-loss", "branch mismatch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(), "dirty tree")
    guard(); torch.set_num_threads(2); torch.use_deterministic_algorithms(True)
    _,pins,protected = precheck(c232_summary,root)
    directory = Path(c232_summary).resolve().parent
    records = read_parent_measurements(directory/"measurements.json")
    states = load_parent_states(directory/"trained-models.pt")
    data = a.read_json(directory/"dataset.json"); train_rows,eval_rows = parent.validate_dataset(data)
    train,ev = parent.tensor_rows(train_rows),parent.tensor_rows(eval_rows)
    reference = parent.reference_score(parent.unigram_tables(train_rows),ev)
    out = Path(output_dir); out.mkdir(parents=True,exist_ok=False)
    rows,baseline_states,saved_logits,replays = [],[],[],[]
    for seed,record,state in zip(SEEDS,records,states,strict=True):
        initial = factory.new_model(seed)
        require(sum(p.numel() for p in initial.parameters()) == FULL_PARAMETERS
                and factory.fingerprint(initial) == record["initial_sha256"], "paired initialization drift")
        model = new_baseline(initial)  # Copy INITIAL common weights, before loading trained full state.
        before = factory.fingerprint(model)
        full_eval,replay_error = replay_full(initial,state,record,ev,eval_rows)
        require(score_error(reference,record["unigram_eval"]) <= TOL, "unigram replay drift")
        initial_train,_ = parent.evaluate(model,train); initial_eval,_ = parent.evaluate(model,ev)
        fit = fit_baseline(model,train[0],train[1],seed)
        final_train,_ = parent.evaluate(model,train); final_eval,logits = parent.evaluate(model,ev)
        generation = [dict(id=r["id"],generated_hex=factory.generate(model,r["text"].encode()[:8]).hex())
                      for r in eval_rows]
        after = factory.fingerprint(model)
        rows.append(dict(seed=seed,initial_sha256=before,final_sha256=after,weights_changed=before!=after,
            full_eval=full_eval,full_replay_error=replay_error,initial_train=initial_train,
            initial_eval=initial_eval,final_train=final_train,final_eval=final_eval,
            unigram_eval=reference,fit=fit,generation=generation))
        replays.append(dict(seed=seed,full_initial_sha256=record["initial_sha256"],
                            full_final_sha256=record["final_sha256"],full_score_error=replay_error))
        baseline_states.append({k:v.detach().clone() for k,v in model.state_dict().items()})
        saved_logits.append(logits.detach())
    checkpoint = out/"baseline-models.pt"
    torch.save(dict(schema="fold-c233-gru-only-v1",seeds=list(SEEDS),states=baseline_states),checkpoint)
    bundle = torch.load(checkpoint,map_location="cpu",weights_only=True)
    require(bundle["schema"] == "fold-c233-gru-only-v1" and bundle["seeds"] == list(SEEDS), "baseline schema")
    for r,state,original in zip(rows,bundle["states"],saved_logits,strict=True):
        model = new_baseline(factory.new_model(r["seed"]))
        model.load_state_dict(state,strict=True); model.eval()
        r["checkpoint_roundtrip"] = factory.fingerprint(model) == r["final_sha256"]
        _,logits = parent.evaluate(model,ev)
        r["reload_max_error"] = float((original-logits).abs().max())
        r["generation_replayed"] = all(factory.generate(model,e["text"].encode()[:8]).hex() == g["generated_hex"]
                                         for e,g in zip(eval_rows,r["generation"],strict=True))
    summary = summary_for(rows)
    for name,value in (("comparison-plan.json",manifest()),("comparisons.json",rows),
                       ("replay-audit.json",replays),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts = [dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size)
                 for name in sorted(OUTPUTS)]
    guard(); precheck(c232_summary,root)
    for name,wanted in protected.items(): require(a.sha(name) == wanted, "modified input:"+name)
    result = dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if gate(summary) else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,network_calls=0,
        limitations=["same-backbone ablation, not matched parameters or compute",
                     "13488 full versus10160 baseline parameters; capacity and recurrence not separated",
                     "same observed C232 split reused; no independent confirmation or general semantics",
                     "baseline unqualified means inconclusive, not evidence for the full core",
                     "no public benchmark, learned-memory integration, speed claim or Gate F completion"])
    validate_result(result); (out/"summary.json").write_bytes(blob(result))
    print("=== C233 RESULT ===",flush=True); print(blob(result).decode(),flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("c232-summary","output-dir"): parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True); run(**vars(parser.parse_args()))


if __name__ == "__main__": main()
