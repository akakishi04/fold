"""C231: prefix-only evaluation contract for the existing uncompressed V5-B byte model.

Untrained instrument checks only, not a language-quality benchmark or V5-G completion.
No memory optimization, downloaded data, accepted checkpoint replacement or training.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import unittest
import torch
from torch.nn import functional as F

EXPERIMENT_ID = "C231-v5b-byte-evaluation-contract"
STAGE = "V5-B-MODEL-EVALUATION-CONTRACT-AUDIT"
BASE = "5c60380b24b818d053b10a59aa30b0484c4c006f"
PARENT_EXECUTION = "58ec6d1497e4729d394307f5c1316d9e69f2ee8e"
PARENT_SHA = "3eeb739eaf37c8b0d1ef4f94d5eec46281ea8721c1cea67fb51234f8bd7fca7c"
PARENT_VALIDATION_SHA = "8f0ebfb7c769f1bc9eebceff02d51c55e1a94dd52ee0ec67b73650f2dda683a9"
SEEDS = (231001, 231002, 231003)
TEXTS = ("The lamp is on.\n", "A box holds two keys.\n", "箱は赤い。\n", "雨なので傘を持つ。\n")
SLOTS, WIDTH, GENERATE, TOLERANCE = 48, 16, 4, 1e-9
PAD, BOS, EOS = 256, 257, 258
MANIFEST_SHA = "745c97d3aab18c129494357cc91eb48a6e713294e437b17700be22da8bd3bf83"
LM_SOURCES = {
    "fold_lm/v05/language_task.py": "587162ffc35e1d854fa8d8577740a1e034537de2",
    "fold_lm/v05/modules.py": "3413c2de62e83dbf4a98af044a5ac2b242c99f87",
    "fold_lm/data.py": "2b0c9635bc67be9a6928d0ccf65e2751719dd2f0",
    "fold_lm/__init__.py": "8977a876cd0e934ec6113d5d323e4809fd4ea1cc",
    "fold_lm/v05/__init__.py": "a5306fe80fd99b46a2efcce0352d29f0030e0f98",
}
OWN = (
    "fold_lm/v05_benchmarks/model_c231_byte_eval_contract.py",
    "tests_lm/test_v05_c231_byte_eval_contract.py",
    "tools/run_c231.ps1", "tools/invoke_c231.ps1",
    "docs/experiment-ledger-addendum-c231-preregistration.md",
    "docs/v5b-byte-evaluation-contract-v0.1.md",
)
OUTPUTS = {"evaluation-plan.json", "byte-fixture.json", "untrained-models.pt",
           "measurements.json", "validation-summary.json"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blob(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode()


def digest(value):
    return hashlib.sha256(blob(value)).hexdigest()


def parent_module():
    from fold_lm.v05_benchmarks import gate_f_c230_prepared_capsule as parent
    return parent


def language_module():
    from fold_lm.v05 import language_task
    return language_task


def manifest():
    return dict(experiment_id=EXPERIMENT_ID, stage=STAGE, acceptance_base=BASE,
        parent_execution=PARENT_EXECUTION, parent_sha256=PARENT_SHA,
        parent_validation_sha256=PARENT_VALIDATION_SHA, lm_sources=LM_SOURCES,
        fixture_sha256=digest(list(TEXTS)), document_bytes=[len(t.encode()) for t in TEXTS],
        seeds=list(SEEDS), slots=SLOTS, width=WIDTH, modules=2, internal_steps=2,
        task_route="fixed TASK_NEXT=0; teacher route, not learned control",
        prefix_format="BOS + observed bytes only + prefix-boundary EOS + PAD",
        targets="one real next byte per position; no PAD/BOS/EOS scoring",
        generated_bytes_per_document=GENERATE, generation="greedy from first8 bytes; rebuilt prefix",
        batch_single_and_suffix_tolerance=TOLERANCE, device="cpu", dtype="float64", threads=2,
        deterministic_algorithms=True, new_training_steps=0, checkpoints="new untrained instrument models",
        model_families=1, forward_calls_per_seed=126, expected_total_forward_calls=378,
        meaningful_language_score=False, prepared_memory_used=False, gate_f_candidate=False,
        stage_progression="evaluation audit of existing V5-B only; no V5-G promotion")


def prefix_tensor(prefix):
    require(type(prefix) is bytes and len(prefix) <= SLOTS-2, "prefix outside fixed-slot contract")
    return torch.tensor([BOS, *prefix, EOS, *([PAD]*(SLOTS-len(prefix)-2))], dtype=torch.int64)


def document_rows(raw):
    require(type(raw) is bytes and 0 < len(raw) <= SLOTS-1, "invalid document bytes")
    # At position i the target is raw[i], while the model sees only raw[:i].
    tokens = torch.stack([prefix_tensor(raw[:i]) for i in range(len(raw))])
    return tokens, torch.tensor(list(raw), dtype=torch.int64)


def predict(model, tokens):
    require(tokens.ndim == 2 and tokens.shape[1] == SLOTS, "invalid input slots")
    tasks = torch.zeros(tokens.shape[0], dtype=torch.int64, device=tokens.device)
    with torch.no_grad():
        logits = model(tokens, tasks)
    require(logits.shape == (tokens.shape[0], 256) and logits.is_floating_point()
            and bool(torch.isfinite(logits).all()), "malformed byte logits")
    return logits


def likelihood(logits, targets):
    require(logits.ndim == 2 and logits.shape[1] == 256
            and targets.dtype == torch.int64 and targets.shape == (logits.shape[0],)
            and targets.numel() > 0 and bool(((targets >= 0) & (targets < 256)).all())
            and bool(torch.isfinite(logits).all()), "invalid likelihood inputs")
    per_byte = F.cross_entropy(logits, targets, reduction="none")
    independent = torch.logsumexp(logits, dim=-1) - logits.gather(1, targets[:, None]).squeeze(1)
    total = float(per_byte.sum())
    return dict(target_bytes=targets.numel(), nll_sum=total,
        bits_per_byte=total/(targets.numel()*math.log(2)),
        scoring_error=float((per_byte-independent).abs().max()))


def generate(model, prefix):
    result = bytearray()
    for _ in range(GENERATE):
        tokens = prefix_tensor(prefix+bytes(result))[None, :]
        result.append(int(predict(model, tokens).argmax(dim=-1)))
    return bytes(result)


def fingerprint(model):
    h = hashlib.sha256()
    for name, tensor in sorted(model.state_dict().items()):
        value = tensor.detach().cpu().contiguous()
        h.update(name.encode()); h.update(str(value.dtype).encode()); h.update(str(tuple(value.shape)).encode())
        h.update(value.numpy().tobytes())
    return h.hexdigest()


def score_document(model, raw):
    tokens, targets = document_rows(raw)
    logits = predict(model, tokens)
    single = torch.cat([predict(model, row[None, :]) for row in tokens], dim=0)
    cut = len(raw)//2
    changed = raw[:cut] + bytes(x ^ 1 for x in raw[cut:])
    changed_tokens, _ = document_rows(changed)
    changed_logits = predict(model, changed_tokens)
    score = likelihood(logits, targets)
    score.update(batch_single_error=float((logits-single).abs().max()),
                 suffix_error=float((logits[:cut+1]-changed_logits[:cut+1]).abs().max()),
                 generated_hex=generate(model, raw[:8]).hex())
    return score, logits


def new_model(seed):
    module = language_module()
    require((module.PAD,module.BOS,module.EOS,module.BYTE_VOCAB_SIZE)==(PAD,BOS,EOS,259),
            "tokenizer identity")
    torch.manual_seed(seed)
    config = module.LanguageTaskConfig(max_tokens=SLOTS, width=WIDTH, modules=2, internal_steps=2)
    return module.ShortByteLanguageModel(config).double().eval()


def row_gate(row):
    docs = row.get("documents", [])
    return (len(docs)==4 and row.get("checkpoint_roundtrip") is True
        and row.get("weights_unchanged") is True and row.get("forward_calls")==126
        and [r["target_bytes"] for r in docs]==[16,22,16,28]
        and all(all(math.isfinite(r[k]) and 0<=r[k]<=TOLERANCE for k in
                    ("scoring_error","batch_single_error","suffix_error","reload_error"))
                and math.isfinite(r["bits_per_byte"]) and r["bits_per_byte"]>=0
                and r["generation_replayed"] is True and len(bytes.fromhex(r["generated_hex"]))==4
                for r in docs))


def gate(s):
    return (s.get("seeds")==list(SEEDS) and s.get("all_contract_checks") is True
        and s.get("scored_bytes")==246 and s.get("model_forward_calls")==378
        and s.get("new_training_steps")==0 and s.get("meaningful_language_score") is False)


def pin_union(parent_pins):
    for path, expected in LM_SOURCES.items():
        require(path not in parent_pins or parent_pins[path]==expected, "LM parent pin conflicts")
    return set(parent_pins) | set(LM_SOURCES) | set(OWN)


def precheck(c230_summary, root):
    parent=parent_module(); a=parent.context(parent.parent_module()).audit; root=Path(root)
    require(a.sha(c230_summary)==PARENT_SHA, "C230 summary changed")
    p=a.read_json(c230_summary); parent.validate_result(p)
    require(p["commit_sha"]==PARENT_EXECUTION and p["status"]=="PASS"
            and parent.gate(p["validation_summary"]), "wrong accepted C230")
    require(len(p["source_blobs"])==221 and len(p["input_sha256"])==305, "parent counts")
    pins,protected=dict(p["source_blobs"]),dict(p["input_sha256"])
    for path,wanted in protected.items():
        require(Path(path).is_file() and a.sha(path)==wanted, "changed input:"+path)
    for path,wanted in pins.items():
        require(a.git(root,"rev-parse","HEAD:"+path).decode().strip()==wanted,"changed source:"+path)
    protected[str(Path(c230_summary).resolve())]=PARENT_SHA
    seen=False
    for item in p["artifacts"]:
        path=a.safe_child(Path(c230_summary).resolve().parent,item["file"])
        require(path.is_file() and a.sha(path)==item["sha256"]
                and path.stat().st_size==item["serialized_bytes"],"parent artifact")
        protected[str(path.resolve())]=item["sha256"]
        if item["file"]=="validation-summary.json":
            require(item["sha256"]==PARENT_VALIDATION_SHA,"parent validation"); seen=True
    require(seen,"missing parent validation")
    wanted_set=pin_union(pins)
    for path in sorted(wanted_set-set(pins)):
        pins[path]=a.git(root,"rev-parse","HEAD:"+path).decode().strip()
    require(all(pins[k]==v for k,v in LM_SOURCES.items()),"LM source identity")
    require(set(pins)==wanted_set and all(path in pins for path in OWN),"source union")
    protected.update(a.protect_tree_files(root,pins))
    require(len(protected)==305+6+len(wanted_set)-221,"protected union count")
    require(digest(manifest())==MANIFEST_SHA,"manifest drift")
    return p,pins,protected


def regression_modules(root):
    names=parent_module().regression_modules(root)
    require(len(names)==len(set(names))==115,"parent modules")
    return names+["tests_lm.test_v05_c231_byte_eval_contract"]


def regression_suite(root):
    p=parent_module(); helper=p.context(p.parent_module()).backend.c205
    tests=list(helper._iter_tests(unittest.defaultTestLoader.loadTestsFromNames(regression_modules(root))))
    excluded=helper.HISTORICAL_DYNAMIC_TEST_EXCLUSIONS; ids=[t.id() for t in tests]
    require(all(ids.count(x)==1 for x in excluded),"historical exclusion")
    kept=[t for t in tests if t.id() not in excluded]
    require(len(tests)==2690 and len(kept)==2689,"C231 regression count")
    return unittest.TestSuite(kept)


def validate_result(p):
    require(p["experiment_id"]==EXPERIMENT_ID and p["stage"]==STAGE
            and p["diagnostic_execution_valid"] is True,"result identity")
    require(set(OWN)|set(LM_SOURCES)<=set(p["source_blobs"])
            and all(p["source_blobs"][k]==v for k,v in LM_SOURCES.items()),"missing C231 sources")
    require(len(p["input_sha256"])==305+6+len(p["source_blobs"])-221
            and len(p["artifacts"])==5 and {x["file"] for x in p["artifacts"]}==OUTPUTS,"result coverage")
    require(p["status"]==("PASS" if gate(p["validation_summary"]) else "FAIL"),"verdict drift")
    require(p["gate_f_candidate"] is False and p["network_calls"]==0,"scope drift")


def run(*, c230_summary, output_dir, expected_head):
    parent=parent_module(); a=parent.context(parent.parent_module()).audit
    root=Path(__file__).resolve().parents[2]
    def guard():
        require(a.git(root,"rev-parse","HEAD").decode().strip()==expected_head,"HEAD")
        require(a.git(root,"branch","--show-current").decode().strip()=="feat/sft-target-loss","branch")
        require(not a.git(root,"status","--porcelain","--untracked-files=no").strip(),"dirty tree")
    guard();torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
    _,pins,protected=precheck(c230_summary,root)
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=False)
    rows=[]; states=[]; saved=[]
    for seed in SEEDS:
        model=new_model(seed); before=fingerprint(model); count=[0]
        def hook(*args): count[0]+=1
        handle=model.register_forward_hook(hook)
        docs=[];logits=[]
        try:
            for text in TEXTS:
                row,values=score_document(model,text.encode());docs.append(row);logits.append(values)
        finally: handle.remove()
        rows.append(dict(seed=seed,documents=docs,weights_unchanged=fingerprint(model)==before,
                         forward_calls=count[0],parameters=sum(x.numel() for x in model.parameters())))
        states.append({k:v.detach().clone() for k,v in model.state_dict().items()})
        saved.append((before,logits))
    checkpoint=out/"untrained-models.pt"
    torch.save(dict(schema="fold-c231-untrained-instrument-v1",seeds=list(SEEDS),states=states),checkpoint)
    restored=torch.load(checkpoint,map_location="cpu",weights_only=True)
    require(restored["schema"]=="fold-c231-untrained-instrument-v1" and restored["seeds"]==list(SEEDS),"checkpoint schema")
    for row,state,(before,original) in zip(rows,restored["states"],saved,strict=True):
        model=new_model(row["seed"]);model.load_state_dict(state,strict=True)
        row["checkpoint_roundtrip"]=fingerprint(model)==before
        count=[0]
        def hook(*args): count[0]+=1
        handle=model.register_forward_hook(hook)
        try:
            for text,item,logits in zip(TEXTS,row["documents"],original,strict=True):
                tokens,_=document_rows(text.encode()); actual=predict(model,tokens)
                item["reload_error"]=float((actual-logits).abs().max())
                item["generation_replayed"]=generate(model,text.encode()[:8]).hex()==item["generated_hex"]
        finally: handle.remove()
        row["forward_calls"]+=count[0]
        row["weights_unchanged"] &= fingerprint(model)==before
    s=dict(seeds=[r["seed"] for r in rows],all_contract_checks=all(row_gate(r) for r in rows),
           scored_bytes=sum(x["target_bytes"] for r in rows for x in r["documents"]),
           model_forward_calls=sum(r["forward_calls"] for r in rows),
           new_training_steps=0,meaningful_language_score=False)
    for name,value in (("evaluation-plan.json",manifest()),("byte-fixture.json",list(TEXTS)),
                       ("measurements.json",rows),("validation-summary.json",s)):
        (out/name).write_bytes(blob(value))
    artifacts=[dict(file=name,sha256=a.sha(out/name),serialized_bytes=(out/name).stat().st_size) for name in sorted(OUTPUTS)]
    guard();precheck(c230_summary,root)
    for path,wanted in protected.items():require(a.sha(path)==wanted,"changed input:"+path)
    result=dict(experiment_id=EXPERIMENT_ID,stage=STAGE,commit_sha=expected_head,
        status="PASS" if gate(s) else "FAIL",diagnostic_execution_valid=True,
        source_blobs=pins,input_sha256=protected,artifacts=artifacts,validation_summary=s,
        gate_f_candidate=False,network_calls=0,
        limitations=["untrained V5-B fixed-slot reference only, not completed v0.5",
                     "four authored text fixtures; no natural-language ability claim",
                     "prefix replay, fixed NEXT route, no persistent decoding or learned H1/H2 integration",
                     "no training-budget adoption, public benchmark comparison or memory optimization"])
    validate_result(result);(out/"summary.json").write_bytes(blob(result))
    print("=== C231 RESULT ===",flush=True);print(blob(result).decode(),flush=True)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("c230-summary","output-dir"):p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--expected-head",required=True);run(**vars(p.parse_args()))


if __name__=="__main__":main()
