"""C232: fixed-budget V5-B learning on grouped, authored bilingual combinations.

Same model/prefix evaluator as C231. No useful general-language or Gate F claim.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import time
import unittest

import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C232-v5b-grouped-bilingual-learning-pilot"
STAGE = "V5-B-GROUPED-BILINGUAL-LEARNING-PILOT"
BASE = "ed8bc28cc5de9e25277394fecf74ec990f08b645"
PARENT_EXECUTION = "06a1b674d58f16816a3f47ec36dc3843e7e1dc37"
PARENT_SHA = "53f9c163beeeab1617eb8946e902cb29c2bbc4a94fb869d3325381160107b522"
PARENT_VALIDATION_SHA = "316435e0a31e0559a73368171df186336852990f16e4aa55b322e776ba281938"
SEEDS = (232001, 232002, 232003)
STEPS, BATCH, LR, CLIP = 400, 32, 0.005, 1.0
LANGUAGES = ("en", "ja")
NOUNS = {"en": ("box", "book", "ball", "umbrella"), "ja": ("箱", "本", "玉", "傘")}
COLORS = {"en": ("red", "blue", "white", "black"), "ja": ("赤い", "青い", "白い", "黒い")}
DATA_SHA = "1a1b09c80c3877c662ee43bf91fb00b7a762d20a7b6b3f455f5ee208c7a79200"
MANIFEST_SHA = "09f2a463981d49680ca66940698baf363731adda9fda8718c5b59fdc281b80c4"
OWN = (
    "fold_lm/v05_benchmarks/model_c232_bilingual_learning.py",
    "tests_lm/test_v05_c232_bilingual_learning.py",
    "tools/run_c232.ps1", "tools/invoke_c232.ps1",
    "docs/experiment-ledger-addendum-c232-preregistration.md",
    "docs/v5b-grouped-bilingual-learning-v0.1.md",
)
OUTPUTS = {"learning-plan.json", "dataset.json", "trained-models.pt", "measurements.json", "validation-summary.json"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import model_c231_byte_eval_contract as parent
    return parent


def audit_module():
    parent = parent_module().parent_module()
    return parent.context(parent.parent_module()).audit


def dataset():
    rows = []
    for language in LANGUAGES:
        for noun_id, noun in enumerate(NOUNS[language]):
            for color_id, color in enumerate(COLORS[language]):
                texts = ((f"The {noun} is {color}.\n", f"A {color} {noun} is here.\n") if language == "en"
                         else (f"{noun}は{color}。\n", f"{color}{noun}がある。\n"))
                for template, text in enumerate(texts):
                    rows.append(dict(id=f"{language}-{noun_id}-{color_id}-{template}", language=language,
                        pair=[noun_id, color_id], template=template, text=text,
                        split="EVAL" if (noun_id+color_id)%4 == 0 else "TRAIN"))
    return rows


def validate_dataset(rows):
    require(rows == dataset() and digest(rows) == DATA_SHA, "registered dataset drift")
    train = [r for r in rows if r["split"] == "TRAIN"]
    ev = [r for r in rows if r["split"] == "EVAL"]
    require((len(rows), len(train), len(ev)) == (64, 48, 16), "dataset profile")
    require(not ({tuple(r["pair"]) for r in train} & {tuple(r["pair"]) for r in ev}), "pair leakage")
    require(all(0 < len(r["text"].encode()) <= 47 for r in rows), "fixed-slot overflow")
    return train, ev


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
        parent_validation_sha256=PARENT_VALIDATION_SHA, data_sha256=DATA_SHA,
        split="EVAL iff (noun_id+color_id)%4==0; group shared across languages/templates",
        documents=64, train_documents=48, eval_documents=16, seeds=list(SEEDS),
        model="unchanged C231 new_model; 13488 parameters; width16,48 slots,2 modules,2 internal steps",
        dtype="float64", device="cpu", threads=2, deterministic_algorithms=True,
        optimizer="AdamW", lr=LR, betas=[0.9,0.999], eps=1e-8, weight_decay=0.0,
        steps_per_seed=STEPS, batch_size=BATCH, gradient_clip_norm=CLIP,
        sampling="uniform TRAIN byte rows with replacement; CPU generator seed+1000",
        total_steps=1200, total_training_byte_presentations=38400,
        validation_selection="none; final step400 only; no early stopping or checkpoint selection",
        references=["same initialization", "per-language TRAIN-only add-one unigram"],
        generation="parent four-byte greedy method on fixed first8-byte EVAL prefixes; descriptive",
        gate="each seed, each language: final EVAL BPB strictly below initial and unigram; train BPB decreases",
        replay_tolerance=1e-9, gate_f_candidate=False, general_language_claim=False,
        checkpoint_reuse="C231 random checkpoints not resumed; new fixed seeds", network_calls=0)


def tensor_rows(rows):
    parent = parent_module()
    xs, ys, groups = [], [], []
    for row in rows:
        x, y = parent.document_rows(row["text"].encode())
        xs.append(x); ys.append(y)
        groups.extend([LANGUAGES.index(row["language"])]*len(y))
    require(bool(xs), "empty split")
    return torch.cat(xs), torch.cat(ys), torch.tensor(groups, dtype=torch.int64)


def unigram_tables(train_rows):
    require(bool(train_rows) and all(r["split"] == "TRAIN" for r in train_rows), "unigram may use TRAIN only")
    counts = torch.ones((2,256), dtype=torch.float64)
    for row in train_rows:
        counts[LANGUAGES.index(row["language"])] += torch.bincount(
            torch.tensor(list(row["text"].encode()), dtype=torch.int64), minlength=256)
    return (counts/counts.sum(dim=1, keepdim=True)).log()


def metrics_from_nll(nll, groups):
    require(nll.ndim == groups.ndim == 1 and nll.shape == groups.shape and nll.numel()>0,
            "invalid score shape")
    require(bool(torch.isfinite(nll).all()) and bool((nll >= -1e-12).all()), "nonfinite score")
    result = {}
    for index, name in ((None,"all"),(0,"en"),(1,"ja")):
        values = nll if index is None else nll[groups == index]
        require(values.numel()>0, "empty language subgroup")
        total = float(values.detach().sum())
        result[name] = dict(bytes=values.numel(), nll_sum=total,
                            bits_per_byte=total/(values.numel()*math.log(2)))
    return result


def reference_score(log_probs, tensors):
    _, targets, groups = tensors
    return metrics_from_nll(-log_probs[groups, targets], groups)


def evaluate(model, tensors):
    parent = parent_module()
    x, y, groups = tensors
    training = model.training
    model.eval()
    try:
        logits = torch.cat([parent.predict(model, part) for part in x.split(64)], dim=0).detach()
        scores = metrics_from_nll(F.cross_entropy(logits, y, reduction="none"), groups)
    finally:
        model.train(training)
    return scores, logits.detach()


def fit(model, train_tokens, train_targets, seed, *, steps=STEPS):
    """Training receives no EVAL rows, language labels or held-out metrics."""
    require(type(steps) is int and steps>0, "positive steps required")
    require(train_tokens.shape[0] == train_targets.numel() and train_targets.numel()>0, "empty training")
    sampler = torch.Generator(device="cpu").manual_seed(seed+1000)
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR, betas=(0.9,0.999), eps=1e-8, weight_decay=0.0)
    model.train()
    first = last = None
    started = time.perf_counter()
    for step in range(steps):
        indices = torch.randint(len(train_targets), (BATCH,), generator=sampler)
        optimizer.zero_grad(set_to_none=True)
        logits = model(train_tokens[indices], torch.zeros(BATCH,dtype=torch.int64))
        loss = F.cross_entropy(logits, train_targets[indices])
        require(bool(torch.isfinite(loss)), "nonfinite training loss")
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(model.parameters(), CLIP, error_if_nonfinite=True)
        require(bool(torch.isfinite(norm)), "nonfinite gradient norm")
        optimizer.step()
        if first is None: first=float(loss.detach())
        last=float(loss.detach())
        if (step+1)%100 == 0:
            print(f"[C232] seed={seed} step={step+1}/{steps} train_batch_nll={last:.6f}",flush=True)
    model.eval()
    return dict(steps=steps, byte_presentations=steps*BATCH, first_batch_nll=first,
                last_batch_nll=last, fit_wall_seconds=time.perf_counter()-started)


def learning_pass(row):
    return (row.get("weights_changed") is True and row.get("checkpoint_roundtrip") is True
        and 0 <= row.get("reload_max_error",math.inf) <= 1e-9
        and row.get("generation_replayed") is True
        and row["final_train"]["all"]["bits_per_byte"] < row["initial_train"]["all"]["bits_per_byte"]
        and all(row["final_eval"][lang]["bits_per_byte"] <
                min(row["initial_eval"][lang]["bits_per_byte"],row["unigram_eval"][lang]["bits_per_byte"])
                for lang in LANGUAGES))


def summary_for(rows):
    return dict(seeds=[r["seed"] for r in rows], all_learning_gates=all(learning_pass(r) for r in rows),
        total_training_steps=sum(r["fit"]["steps"] for r in rows),
        total_training_byte_presentations=sum(r["fit"]["byte_presentations"] for r in rows),
        general_language_claim=False, gate_f_candidate=False)


def gate(s):
    return (s.get("seeds")==list(SEEDS) and s.get("all_learning_gates") is True
        and s.get("total_training_steps")==1200 and s.get("total_training_byte_presentations")==38400
        and s.get("general_language_claim") is False and s.get("gate_f_candidate") is False)


def precheck(c231_summary, root):
    parent, a = parent_module(), audit_module()
    root=Path(root)
    require(a.sha(c231_summary)==PARENT_SHA,"C231 summary changed")
    p=a.read_json(c231_summary); parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS"
            and parent.gate(p["validation_summary"]),"wrong accepted C231")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    require(len(pins)==232 and len(protected)==322,"parent counts")
    for path,wanted in protected.items():
        require(Path(path).is_file() and a.sha(path)==wanted,"changed input:"+path)
    for path,wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+path).decode().strip()==wanted,"changed source:"+path)
    protected[str(Path(c231_summary).resolve())]=PARENT_SHA
    seen=False
    for item in p["artifacts"]:
        path=a.safe_child(Path(c231_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path)==item["sha256"]
                and path.stat().st_size==item["serialized_bytes"],"parent artifact changed")
        protected[str(path.resolve())]=item["sha256"]
        if item["file"]=="validation-summary.json":
            require(item["sha256"]==PARENT_VALIDATION_SHA,"parent validation identity");seen=True
    require(seen,"missing validation artifact")
    for path in OWN:
        require(path not in pins,"new source collides with accepted source")
        pins[path]=a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    dependencies=set(parent.LM_SOURCES)|{
        "fold_lm/v05_benchmarks/model_c231_byte_eval_contract.py",
        "fold_lm/v05_benchmarks/gate_f_c230_prepared_capsule.py", OWN[0]}
    require(dependencies <= set(pins),"missing deciding dependency")
    protected.update(a.protect_tree_files(root,pins))
    require((len(pins),len(protected))==(238,334),"C232 protection counts")
    validate_dataset(dataset());require(digest(manifest())==MANIFEST_SHA,"manifest drift")
    return p,pins,protected


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==116,"parent modules")
    return names+["tests_lm.test_v05_c232_bilingual_learning"]


def regression_suite(root):
    previous=parent_module().parent_module()
    helper=previous.context(previous.parent_module()).backend.c205
    tests=list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    ids=[t.id() for t in tests];excluded=helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS
    require(all(ids.count(x)==1 for x in excluded),"historical exclusion identity")
    kept=[t for t in tests if t.id() not in excluded]
    require((len(tests),len(kept))==(2722,2721),"C232 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE
            and p["diagnostic_execution_valid"] is True,"C232 result identity")
    require((len(p["source_blobs"]),len(p["input_sha256"]))==(238,334)
            and set(OWN)<=set(p["source_blobs"]),"C232 protection")
    require(len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"C232 artifacts")
    s=p["validation_summary"]
    require(s["total_training_steps"]==1200 and s["total_training_byte_presentations"]==38400
            and s["seeds"]==list(SEEDS),"incomplete training workload")
    require(p["status"]==("PASS" if gate(s) else "FAIL"),"verdict drift")
    require(p["gate_f_candidate"] is False and p["network_calls"]==0,"scope drift")


def run(*, c231_summary, output_dir, expected_head):
    parent,a=parent_module(),audit_module()
    root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    _,pins,protected=precheck(c231_summary,root)
    data=dataset();train_rows,eval_rows=validate_dataset(data)
    train,ev=tensor_rows(train_rows),tensor_rows(eval_rows)
    reference=reference_score(unigram_tables(train_rows),ev)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    records,states,saved_logits=[],[],[]
    for seed in SEEDS:
        model=parent.new_model(seed)
        require(sum(p.numel() for p in model.parameters())==13488,"model identity")
        before=parent.fingerprint(model)
        initial_train,_=evaluate(model,train);initial_eval,_=evaluate(model,ev)
        fitted=fit(model,train[0],train[1],seed)
        final_train,_=evaluate(model,train);final_eval,logits=evaluate(model,ev)
        generation=[dict(id=r["id"],generated_hex=parent.generate(model,r["text"].encode()[:8]).hex())
                    for r in eval_rows]
        after=parent.fingerprint(model)
        records.append(dict(seed=seed,parameters=13488,initial_sha256=before,final_sha256=after,
            weights_changed=before!=after,fit=fitted,initial_train=initial_train,initial_eval=initial_eval,
            final_train=final_train,final_eval=final_eval,unigram_eval=reference,generation=generation))
        states.append({k:v.detach().clone() for k,v in model.state_dict().items()})
        saved_logits.append(logits)
    checkpoint=out/"trained-models.pt"
    torch.save(dict(schema="fold-c232-trained-byte-models-v1",seeds=list(SEEDS),states=states),checkpoint)
    bundle=torch.load(checkpoint,map_location="cpu",weights_only=True)
    require(bundle["schema"]=="fold-c232-trained-byte-models-v1" and bundle["seeds"]==list(SEEDS),"checkpoint schema")
    for record,state,original in zip(records,bundle["states"],saved_logits,strict=True):
        model=parent.new_model(record["seed"]);model.load_state_dict(state,strict=True);model.eval()
        record["checkpoint_roundtrip"]=parent.fingerprint(model)==record["final_sha256"]
        _,restored=evaluate(model,ev)
        record["reload_max_error"]=float((original-restored).abs().max())
        record["generation_replayed"]=all(parent.generate(model,r["text"].encode()[:8]).hex()==g["generated_hex"]
                                         for r,g in zip(eval_rows,record["generation"],strict=True))
    summary=summary_for(records)
    for name,value in (("learning-plan.json",manifest()),("dataset.json",data),
                       ("measurements.json",records),("validation-summary.json",summary)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard();precheck(c231_summary,root)
    for path,wanted in protected.items():require(a.sha(path)==wanted,"modified input:"+path)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if gate(summary) else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=summary,
        gate_f_candidate=False,network_calls=0,
        limitations=["authored template corpus; held-out pairs, not unseen vocabulary or grammar",
                     "byte likelihood may improve through formatting; not proof of semantic composition",
                     "unigram is a weak calibration reference, not a matched neural baseline",
                     "fixed-route uncompressed V5-B only; no learned memory/compression/controller integration",
                     "no general benchmark, useful conversation, speed or memory superiority claim"])
    validate_result(result);(out/"summary.json").write_bytes(blob(result))
    print("=== C232 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("c231-summary","output-dir"):parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--expected-head",required=True);run(**vars(parser.parse_args()))


if __name__=="__main__":main()
